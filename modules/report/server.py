import logging
import json
import uuid

from flask import Flask, jsonify, render_template
from pathlib import Path
from colorama import Fore

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


app = Flask(
    __name__,
    template_folder=str(Path(__file__).parent / "templates"),
    static_folder=str(Path(__file__).parent / "static"),
            )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/reports")
def data_reports():
    try:
        #print(f"Procurando em {path_jsons}")
        #print(f"Existe? {path_jsons.exists()}")
        #print(list(path_jsons.glob("*.json")))
        
        data = [] 
        for file in REPORTS_DIR.rglob("*.json"): 
            data.append({ 
                "name"    : file.name,
                "tamanho" : file.stat().st_size,
                "path"    : file.relative_to(REPORTS_DIR).as_posix()
                    })
        return jsonify(data)
        
    except Exception as e:
        logger.warning('[!] ERRO AO ABRIR O ARQUIVO')
        print(f"{Fore.RED + '[!] ERRO AO ABRIR O ARQUIVO'}")

        return jsonify({
            "error": str(e)
        }), 500

@app.route("/reports/<path:filename>")
def report(filename):

    try:

        report_file = (REPORTS_DIR / filename).resolve()
        
        
        if REPORTS_DIR not in report_file.parents:
            return jsonify({
                "error": "Acesso Negado"
            }), 403
        
        if not report_file.exists():
            return jsonify({
                "error": "Arquivo não encotrado"
            }), 404
        
        if not filename.endswith(".json"):
            return jsonify({
                "error": "Formato Inválido"
            }), 400

        with open(report_file, "r", encoding='utf-8') as f:
            data = json.load(f)

            return jsonify(data)
        
    except Exception as e:
        print(Fore.RED + f"[!] Erro {e}")
        logger.error(e)

        return jsonify({
            "error": str(e)
        }), 500




if __name__ == "__main__":
    app.run(debug=True)