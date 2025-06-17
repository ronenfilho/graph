from rdflib import Graph
from rdflib_neo4j import Neo4jStore, Neo4jStoreConfig, HANDLE_VOCAB_URI_STRATEGY

def connect_neo4j(uri="bolt://192.168.0.48:7687", user="neo4j", password="Adsumus@9", database="neo4j"):
    """
    Conecta ao banco Neo4j usando rdflib-neo4j e retorna a store.
    """
    config = Neo4jStoreConfig(
        auth_data={"uri": uri, "user": user, "pwd": password, "database": database},
        handle_vocab_uri_strategy=HANDLE_VOCAB_URI_STRATEGY.MAP,
        batching=True
    )
    return Neo4jStore(config=config)

def save_graph_to_neo4j(original_graph):
    """
    Salva o grafo RDF diretamente no Neo4j usando rdflib-neo4j.
    """
    config = Neo4jStoreConfig(
        auth_data={
            "uri": "bolt://192.168.0.48:7687",
            "user": "neo4j",
            "pwd": "Adsumus@9",
            "database": "neo4j"
        },
        handle_vocab_uri_strategy=HANDLE_VOCAB_URI_STRATEGY.MAP,
        batching=True
    )

    store = Neo4jStore(config=config)
    g = Graph(store=store)
    g += original_graph
    g.commit()
    g.close()
    print("[INFO] Grafo RDF salvo com sucesso no Neo4j!")