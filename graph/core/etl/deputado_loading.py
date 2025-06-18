import os
from rdflib import Graph
import networkx as nx
import sys
from pathlib import Path
from graph.core.data.neo4j.neo4j_utils import save_graph_to_neo4j
from graph.core.data.utils import convert_to_networkx, plot_graph
from graph.core.data.rdf.rdf_utils import load_rdf_graph
from rdflib import URIRef

# Adiciona a raiz do projeto ao sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from graph.config import PROCESSED_DATA, ID_LEGISLATURA, ID_DEPUTADO


def filter_graph_for_deputado(rdf_graph, deputado_id):
    """
    Filtra o grafo RDF para incluir apenas as triplas relacionadas a um deputado específico.
    Retorna o nome do deputado (se encontrado) e o grafo filtrado.
    """
    deputado_uri = URIRef(f"https://dadosabertos.camara.leg.br/recurso/deputado/{deputado_id}")
    filtered_graph = Graph()
    nome_deputado = None

    for s, p, o in rdf_graph:
        if s == deputado_uri:
            filtered_graph.add((s, p, o))
            # Tenta identificar o nome do deputado (assumindo predicado 'foaf:name' ou similar)
            if "nome" in str(p).lower() or "name" in str(p).lower():
                nome_deputado = str(o)
            print(f"[INFO] Tripla adicionada: {s} {p} {o}")

    print(f"[INFO] Grafo filtrado com {len(filtered_graph)} triplas.")
    return nome_deputado, filtered_graph

def main():    
    print("########################")
    print("## Carga - Deputados ##")
    print("########################")

    nt_file = os.path.join(PROCESSED_DATA, f"deputados_legisl_{ID_LEGISLATURA}.nt")
    
    rdf_graph = load_rdf_graph(nt_file)

    nome_deputado, filtered_graph = filter_graph_for_deputado(rdf_graph, ID_DEPUTADO)
    nx_graph = convert_to_networkx(filtered_graph)
    plot_graph(nx_graph, title=f"Deputado: {nome_deputado}", file_name=f"deputado_{ID_DEPUTADO}-{nome_deputado}_graph.png")

    # Salva no Neo4j    
    save_graph_to_neo4j(rdf_graph)

if __name__ == "__main__":
    main()
