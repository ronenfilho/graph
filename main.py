import sys
from pathlib import Path

# Garante que a pasta raiz esteja no path (se necessário)
sys.path.append(str(Path(__file__).resolve().parent))

# Importa a função da subpasta
from scripts.deputado_extraction import extraction_deputado
from config import RAW_DATA

def main():
    print("Iniciando extração dos deputados...")
    extraction_deputado(RAW_DATA)

if __name__ == "__main__":
    main()
