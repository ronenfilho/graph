import requests
import pandas as pd
import os

def save_to_csv(data, filepath):
    """
    Salva a lista de deputados em um arquivo CSV.
    """

    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False, encoding="utf-8")
    print(f"[INFO] Arquivo CSV '{filepath}' salvo com sucesso!")

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

    print("########################")
    print("## Extração - Deputados ##")
    print("########################")

    idLegislatura = "57" # Legislatura atual

    deputados = fetch_all_deputados(idLegislatura)
    filepath = os.path.join(directory, "deputados_legisl_"+idLegislatura+".csv")
    save_to_csv(deputados, filepath)

def transformation_deputado():
  '''Transformação - Deputados Federais'''
  print("########################")
  print("## Transformação - Deputados ##")
  print("########################")

  return True

def load_deputado():
  '''Carga - Deputados Federais'''
  print("########################")
  print("## Carga - Deputados ##")
  print("########################")
  return True

if __name__ == "__main__":
  # Defina o diretório onde os dados serão salvos. Para falta no Google Drive. 
  #directory = '/content/drive/MyDrive/1-Acadêmico/___IA - IFG - 2025/Disciplina/202501 - Linguagem de Programação Aplicada/_IFG - Ling. Programação - Projeto 1/dataset'

  #Para falta localmente
  directory = './dataset'

  extraction_deputado(directory)
  #transformation_deputado()
  #load_deputado()

  # Extração - Partidos

