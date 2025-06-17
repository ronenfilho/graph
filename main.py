from etl.io_utils import load_csv
from etl.rdf_utils import build_rdf_graph_from_dataframe, save_graph_as_nt
from etl.neo4j_utils import save_graph_to_neo4j
from scripts.deputado_extraction import main as deputado_extraction_main
from scripts.deputado_transformation import main as deputado_transformation_main
from scripts.deputado_loading import main as deputado_loading_main


def main():
    print("##############################")
    print("## Semantic ETL Pipilines - ##")
    print("##############################")
    print("\n")

    print("Iniciando extração dos deputados...")
    deputado_extraction_main()
    print("Extração dos deputados concluída!")    
    print("\n")    

    print("Iniciando transformação dos deputados...")
    deputado_transformation_main()
    print("Transformação dos deputados concluída!")
    print("\n")

    print("Iniciando carga dos deputados...")
    deputado_loading_main()
    print("Carga dos deputados concluída!")
    print("\n")

if __name__ == "__main__":
    main()