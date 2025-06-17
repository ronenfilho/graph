import os
import pandas as pd

def load_csv(filepath):
    """
    Carrega o CSV dos deputados em um DataFrame pandas.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"O arquivo {filepath} não foi encontrado!")
    return pd.read_csv(filepath)