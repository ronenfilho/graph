import os
import pandas as pd

def load_csv(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    return pd.read_csv(filepath)
