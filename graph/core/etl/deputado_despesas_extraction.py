import requests
import pandas as pd
import os
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil

sys.path.append(str(Path(__file__).resolve().parent.parent))
from graph.config import RAW_DATA
from graph.core.data.io_utils import save_to_csv


def print_thread_info(stage=""):
    pid = os.getpid()
    process = psutil.Process(pid)
    thread_count = process.num_threads()
    print(f"[THREAD INFO] {stage} - Total de threads ativas: {thread_count}")

def fetch_despesas_deputado(deputado_id, nome, ordenar_por="ano", ordem="ASC"):
    despesas = []
    pagina = 1

    while True:
        url = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{deputado_id}/despesas?ordem={ordem}&ordenarPor={ordenar_por}&pagina={pagina}"
        headers = {"accept": "application/json"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json().get("dados", [])

            if not data:
                break

            for d in data:
                d["deputado_id"] = deputado_id
                d["deputado_nome"] = nome

            despesas.extend(data)
            pagina += 1
        except requests.RequestException as e:
            print(f"[ERRO] {nome} ({deputado_id}): {e}")
            break

    return despesas

def extraction_despesas_parallel(directory, max_workers=1, st_callback=None):

    def show_progress(current, total, width=30):
        percent = current / total
        bar = "#" * int(percent * width) + "." * (width - int(percent * width))
        text = f"[{bar}] {current}/{total} deputados ({percent:.2%})"
        if st_callback:
            st_callback(text)
        else:
            print(f"\r{text}", end="", flush=True)

    filepath = os.path.join(directory, "deputados_legisl_57.csv")
    df = pd.read_csv(filepath).drop_duplicates(subset=["id"])
    total = len(df)

    print(f"[INFO] Extração paralela iniciada com {max_workers} threads para {total} deputados...\n")

    all_despesas = []
    processed = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_deputado = {
            executor.submit(fetch_despesas_deputado, row["id"], row["nome"]): row["nome"]
            for _, row in df.iterrows()
        }

        for future in as_completed(future_to_deputado):
            nome = future_to_deputado[future]
            try:
                despesas = future.result()
                all_despesas.extend(despesas)
            except Exception as e:
                print(f"\n[ERRO] Falha ao processar {nome}: {e}")

            processed += 1
            show_progress(processed, total)

    print("\n")  # Quebra de linha após a barra de progresso

    if all_despesas:
        save_path = os.path.join(directory, "deputados_despesas_legisl_57.csv")
        save_to_csv(all_despesas, save_path)
        print(f"\n[INFO] Extração finalizada com sucesso!")
        print(f"[INFO] Total de despesas processadas: {len(all_despesas)}")
        print(f"[INFO] Arquivo salvo em: {save_path}")
    else:
        print("\n[AVISO] Nenhuma despesa foi encontrada.")

def main():
    print("##############################################")
    print("## Extração Paralela - Despesas dos Deputados ##")
    print("###############################################\n")

    start_time = time.time()

    print_thread_info("Antes do processamento")
    extraction_despesas_parallel(RAW_DATA)
    print_thread_info("Depois do processamento")

    end_time = time.time()
    elapsed = end_time - start_time
    mins, secs = divmod(elapsed, 60)
    print(f"\n⏱ Tempo total de processamento: {int(mins)} min {int(secs)} seg")

if __name__ == "__main__":
    main()
