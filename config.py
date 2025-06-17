from pathlib import Path

# Diretório raiz
ROOT_DIR = Path(__file__).resolve().parent

# Diretórios de dados
DATASET_DIR = ROOT_DIR / 'dataset'
RAW_DATA = DATASET_DIR / 'raw'
PROCESSED_DATA = DATASET_DIR / 'processed'
