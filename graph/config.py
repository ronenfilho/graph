from pathlib import Path
import os
from dotenv import load_dotenv
from pathlib import Path


# Carrega o .env apenas uma vez ao importar
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')

# Diretório raiz
ROOT_DIR = Path(__file__).resolve().parent

# Diretórios de dados
DATASET_DIR = ROOT_DIR / 'dataset'
RAW_DATA = DATASET_DIR / 'raw'
PROCESSED_DATA = DATASET_DIR / 'processed'
IMG_DATA = ROOT_DIR / 'docs/images'

# Variáveis de configuração
ID_LEGISLATURA = int(os.getenv("ID_LEGISLATURA", 57))
ID_DEPUTADO = int(os.getenv("ID_DEPUTADO", 204445))
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")
