import os
import pandas as pd


def save_to_csv(data, filepath):
    """
    Salva em um arquivo CSV.
    """

    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False, encoding="utf-8")
    print(f"[INFO] Arquivo CSV '{filepath}' salvo com sucesso!")

def load_csv(filepath):
    """
    Carrega o CSV dos deputados em um DataFrame pandas.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"O arquivo {filepath} não foi encontrado!")
    return pd.read_csv(filepath)