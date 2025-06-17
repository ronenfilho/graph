import os

def get_file_path(base_dir, filename):
    """
    Retorna o caminho completo para um arquivo.
    """
    return os.path.join(base_dir, filename)