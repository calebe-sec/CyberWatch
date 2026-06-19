import datetime

import pytest

from modules.report.report_manager import GerenciadorRelatorio


@pytest.fixture
def base_dir(tmp_path, monkeypatch):
    """Redireciona BASE_DIR para uma pasta temporária durante o teste."""
    destino = tmp_path / "reports"
    monkeypatch.setattr(GerenciadorRelatorio, "BASE_DIR", destino)
    return destino


RESULTADOS_EXEMPLO = [
    {
        "port": 80,
        "status": "open",
        "service": "http",
        "version": "nginx/1.18.0",
        "web_enum": {"title": "Bem-vindo, visitante", "content_type": "text/html; charset=utf-8"},
    },
    {
        "port": 22,
        "status": "open",
        "service": "ssh",
        "version": "OpenSSH_9.3",
        "web_enum": None,
    },
]


def test_init_cria_pasta_do_dia(base_dir):
    GerenciadorRelatorio("1.2.3.4")
    hoje = datetime.datetime.now().strftime("%Y-%m-%d")
    assert (base_dir / hoje).is_dir()


def test_salvardados_grava_csv_com_cabecalho_correto(base_dir):
    g = GerenciadorRelatorio("1.2.3.4")
    caminho = g.salvardados(RESULTADOS_EXEMPLO)

    conteudo = open(caminho, encoding="utf-8").read()
    assert "port,status,service,version,banner,title,content_type" in conteudo
    assert "nginx/1.18.0" in conteudo


def test_salvardados_preserva_campos_com_virgula(base_dir):
    """Regressão: o CSV era escrito com ','.join(...) sem nenhum tipo de
    escaping, então um título de página com vírgula quebrava o
    alinhamento das colunas ao reler o arquivo."""
    g = GerenciadorRelatorio("1.2.3.4")
    g.salvardados(RESULTADOS_EXEMPLO)

    dados = g.recuperadados()
    registro_80 = next(r for r in dados if r["port"] == 80)
    assert registro_80["title"] == "Bem-vindo, visitante"


def test_salvarjson_grava_relatorio_valido(base_dir):
    g = GerenciadorRelatorio("1.2.3.4")
    caminho = g.salvarjson(RESULTADOS_EXEMPLO)

    import json
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)

    assert "report_id" in dados
    assert dados["result"] == RESULTADOS_EXEMPLO


def test_recuperadados_retorna_tipos_convertidos(base_dir):
    g = GerenciadorRelatorio("1.2.3.4")
    g.salvardados(RESULTADOS_EXEMPLO)

    dados = g.recuperadados()
    portas = {d["port"] for d in dados}
    assert portas == {80, 22}
    assert all(isinstance(p, int) for p in portas)


def test_recuperadados_sem_relatorios_retorna_lista_vazia(base_dir):
    g = GerenciadorRelatorio("alvo.sem.scans")
    assert g.recuperadados() == []


def test_recuperadados_pega_o_mais_recente_do_mesmo_dia(base_dir):
    g = GerenciadorRelatorio("1.2.3.4")
    g.salvardados([{"port": 21, "status": "open", "service": "ftp", "version": "v1"}])

    # Força um segundo relatório "mais novo" no mesmo dia
    g.hora_agora = "235959"
    g.salvardados([{"port": 22, "status": "open", "service": "ssh", "version": "v2"}])

    dados = g.recuperadados()
    assert dados[0]["service"] == "ssh"


def test_recuperadados_busca_em_dias_anteriores(base_dir):
    """Regressão: antes a busca ficava restrita à pasta do dia atual, então
    relatórios salvos em dias anteriores nunca eram encontrados por
    'reports -t <alvo>'."""
    ontem = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    pasta_ontem = base_dir / ontem
    pasta_ontem.mkdir(parents=True)
    (pasta_ontem / "scan_1_2_3_4_010101.csv").write_text(
        "port,status,service,version,banner,title,content_type\n"
        "21,open,ftp,vsFTPd,,,\n",
        encoding="utf-8",
    )

    g = GerenciadorRelatorio("1.2.3.4")
    # Garante que não existe nenhum relatório criado hoje
    import shutil
    shutil.rmtree(g.pasta_dia, ignore_errors=True)

    dados = g.recuperadados()
    assert dados and dados[0]["service"] == "ftp"


def test_listar_relatorios_nao_lanca_excecao_sem_pasta(base_dir, capsys):
    GerenciadorRelatorio.listarRelatorios()
    saida = capsys.readouterr().out
    assert "Nenhum relatório" in saida


def test_listar_relatorios_lista_arquivos_existentes(base_dir, capsys):
    g = GerenciadorRelatorio("1.2.3.4")
    g.salvardados(RESULTADOS_EXEMPLO)

    GerenciadorRelatorio.listarRelatorios()
    saida = capsys.readouterr().out
    assert "scan_1_2_3_4_" in saida


def test_alvo_com_pontos_e_dois_pontos_normalizado_no_nome_do_arquivo(base_dir):
    g = GerenciadorRelatorio("2001:db8::1")
    assert "." not in g.target
    assert ":" not in g.target