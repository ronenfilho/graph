import os
import matplotlib.pyplot as plt
import networkx as nx
from graph.config import IMG_DATA


def get_file_path(base_dir, filename):
    """
    Retorna o caminho completo para um arquivo.
    """
    return os.path.join(base_dir, filename)

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

def plot_graph(nx_graph, title="Visualização do Grafo RDF", file_name="img_grafo.png"):
    """
    Plota o grafo com Matplotlib, inclui data/hora e salva como imagem.
    """
    pos = nx.spring_layout(nx_graph, seed=42)
    plt.figure(figsize=(15, 10))
    nx.draw(nx_graph, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=8, font_weight="bold", edge_color="gray")
    edge_labels = nx.get_edge_attributes(nx_graph, 'label')
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels, font_size=7)
    plt.title(title)
    plt.axis("off")
    save_path = os.path.join(IMG_DATA, file_name)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[INFO] Grafo RDF convertido para NetworkX com {nx_graph.number_of_nodes()} nós e {nx_graph.number_of_edges()} arestas.")
    print(f"[INFO] Grafo RDF plotado e salvo como {save_path}.")

    