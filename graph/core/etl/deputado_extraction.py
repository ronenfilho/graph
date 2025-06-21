import requests
import pandas as pd
import os
import sys
from pathlib import Path

# Adiciona a raiz do projeto ao sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from graph.config import RAW_DATA, ID_LEGISLATURA
from graph.core.data.io_utils import save_to_csv


def fetch_deputados(ordem="ASC", ordenar_por="nome", pagina=1, idLegislatura=57):
    """
    Faz a requisição à API da Câmara e retorna a lista de deputados de uma página específica.
    """
    url = f"https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura={idLegislatura}&ordem={ordem}&ordenarPor={ordenar_por}&pagina={pagina}"
    headers = {
        "accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("dados", [])
    except requests.RequestException as e:
        print(f"[ERRO] Falha na requisição: {e}")
        return []

def fetch_all_deputados(idLegislatura=57):
    """    
    Faz a requisição de todas as páginas de deputados.
    """
    deputados_total = []
    pagina = 1

    while True:
        deputados = fetch_deputados(pagina=pagina, idLegislatura=idLegislatura)
        if not deputados:
            break

        deputados_total.extend(deputados)
        print(f"[INFO] Página {pagina} processada com {len(deputados)} deputados.")
        pagina += 1

    return deputados_total

def extraction_deputado(directory):
    '''Extração - Deputados Federais'''
    
    idLegislatura = ID_LEGISLATURA

    deputados = fetch_all_deputados(idLegislatura)
    filepath = os.path.join(directory, f"deputados_legisl_{ID_LEGISLATURA}.csv")
    save_to_csv(deputados, filepath)

def main():
    print("##########################")
    print("## Extração - Deputados ##")
    print("##########################")
    print("\n")

    extraction_deputado(RAW_DATA)

if __name__ == "__main__":
    main()    
