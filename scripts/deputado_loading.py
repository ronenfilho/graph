from rdflib import Graph
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path
from etl.neo4j_utils import save_graph_to_neo4j
#from rdflib_neo4j import Neo4jStore, Neo4jStoreConfig, HANDLE_VOCAB_URI_STRATEGY
from rdflib import URIRef

# Adiciona a raiz do projeto ao sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import PROCESSED_DATA

def load_rdf_graph(nt_file):
    """
    Carrega o arquivo N-Triples em um grafo RDFLib.
    """
    g = Graph()
    g.parse(nt_file, format="nt")
    print(f"[INFO] Grafo RDF carregado com {len(g)} triplas.")
    return g

def convert_to_networkx(rdf_graph):
    """
    Converte grafo RDFLib em grafo NetworkX para visualização.
    """
    nx_graph = nx.DiGraph()
    for s, p, o in rdf_graph:
        s_label = str(s)
        p_label = str(p.split("/")[-1])
        o_label = str(o)
        nx_graph.add_edge(s_label, o_label, label=p_label)
    return nx_graph

def plot_graph(nx_graph, title="Visualização do Grafo RDF"):
    """
    Plota o grafo com Matplotlib.
    """
    pos = nx.spring_layout(nx_graph, seed=42)
    plt.figure(figsize=(15, 10))
    nx.draw(nx_graph, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=8, font_weight="bold", edge_color="gray")
    edge_labels = nx.get_edge_attributes(nx_graph, 'label')
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels, font_size=7)
    plt.title(title)
    plt.axis("off")
    plt.show()

def filter_graph_for_deputado(rdf_graph, deputado_id):
    """
    Filtra o grafo RDF para incluir apenas as triplas relacionadas a um deputado específico.
    """
    deputado_uri = URIRef(f"https://dadosabertos.camara.leg.br/recurso/deputado/{deputado_id}")
    filtered_graph = Graph()
    for s, p, o in rdf_graph:
        if s == deputado_uri:
            filtered_graph.add((s, p, o))
            #print(f"[INFO] Tripla adicionada: {s} {p} {o}")
            #print(f"[INFO] Grafo filtrado com {len(filtered_graph)} triplas.")
    return filtered_graph

def main():    
    print("########################")
    print("## Carga - Deputados ##")
    print("########################")

    idLegislatura = "57" # Legislatura atual'
    deputado_id = 204445  # ID de Abílio Santana

    nt_file = os.path.join(PROCESSED_DATA, "deputados_legisl_"+idLegislatura+".nt")        
    
    rdf_graph = load_rdf_graph(nt_file)
    # Salva no Neo4j    
    save_graph_to_neo4j(rdf_graph)

    filtered_graph = filter_graph_for_deputado(rdf_graph, deputado_id)
    nx_graph = convert_to_networkx(filtered_graph)
    plot_graph(nx_graph, title="Deputado: Fernando Mineiro")

if __name__ == "__main__":
    main()
