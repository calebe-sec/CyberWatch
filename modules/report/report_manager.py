import os
import json
import uuid

from datetime import datetime

class GerenciadorRelatorio:
    BASE_DIR = 'reports'

    def __init__(self,target: str):
        self.target = target.replace(".", "_").replace(":","_")
        self.data_hoje = datetime.now().strftime("%Y-%m-%d")
        self.hora_agora = datetime.now().strftime("%H%M%S")
        self.pasta_dia = os.path.join(self.BASE_DIR, self.data_hoje)
        self._garantir_pasta()

    def _garantir_pasta(self):
        os.makedirs(self.pasta_dia, exist_ok=True)

    def _nome_arquivo(self, extensao: str) -> str:
        nome = f"scan_{self.target}_{self.hora_agora}.{extensao}"

        return os.path.join(self.pasta_dia, nome)
    
    def salvardados(self, results: list) -> str:
        caminho = self._nome_arquivo("csv")
        cabecalho = ["port", "status", "service", "version", "banner", "title", "content_type"]
        linhas = [cabecalho]

        for result in results:
            web = result.get("web_enum") or {}
            linha = [
                result.get("port", ""),
                result.get("status", ""),
                result.get("service", ""),
                result.get("version", ""),
                result.get("banner", ""),
                web.get("title", ""),
                web.get("content_type", ""),
            ]
            linhas.append(linha)

        try:
            with open(caminho, "w", encoding="utf-8") as f:
                for sublista in linhas:
                    linha_str = ",".join(str(elemento) for elemento in sublista)
                    f.write(linha_str + "\n")
            print(f"[*] Relatório CSV salvo em: {caminho}")
        except Exception as e:
            print(f"[!] Erro ao salvar CSV: {e}")
    
        return caminho
    def recuperadados(self) -> list:
            try:
                arquivos = [
                    f for f in os.listdir(self.pasta_dia)
                    if f.startswith(f"scan_{self.target}_")
                    and f.endswith(".csv")
                ]
            except FileNotFoundError:
                print(f"[!] Pasta não encontrada: {self.pasta_dia}")
                return []
            
            if not arquivos:
                print(f"[!] Nenhum relatório encontrado para '{self.target}' em {self.data_hoje}")
                return []
        
            arquivos.sort(reverse=True)
            caminho = os.path.join(self.pasta_dia, arquivos[0])

            dados = []
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    linhas = f.readlines()

                    if not linhas:
                        return dados
                    
                    cabecalho = [c.strip() for c in linhas[0].split(",")]

                    for linha in linhas[1:]:
                        linha_limpa = linha.strip()
                        if not linha_limpa:
                            continue

                        elementos = linha.split(",")
                        linha_com_tipos = []

                        for item in elementos:
                            try:
                                valor = int(item)
                            except ValueError:
                                try:
                                    valor = float(item)
                                except ValueError:
                                    valor = item
                            linha_com_tipos.append(valor)

                        registro = dict(zip(cabecalho,linha_com_tipos))
                        dados.append(registro)

            except Exception as e:
                print(f"[!] Erro ao recuperar dados: {e}")

            return dados
        
    def salvarjson(self, results: list) -> str:

        report_id = str(uuid.uuid4())

        report = {
            "report_id": report_id,
            "result" : results
        }

        caminho = self._nome_arquivo("json")

        try:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=4, ensure_ascii=False)

                print(f"[*] Relatório json salvo em: {caminho}")
        
        except Exception as e:
            print(f"[!] Erro ao savar o json: {e}")
        
        return caminho
        
    @staticmethod
    def listarRelatorios(base_dir: str = "reports") -> None:
        if not os.path.exists(base_dir):
            print("[*] Nenhum relatório encontrado")
            return
        datas = sorted(os.listdir(base_dir), reverse=True)
        for data in datas:
            pasta = os.path.join(base_dir, data)
            if not os.path.isdir(pasta):
                continue
            arquivos = os.listdir(pasta)
            print(f"\n {data} ({len(arquivos)} arquivos)")

            for arq in sorted(arquivos):
                print(f"     └─ {arq}")
                
