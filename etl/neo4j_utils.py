from rdflib import Graph
from rdflib_neo4j import Neo4jStore, Neo4jStoreConfig, HANDLE_VOCAB_URI_STRATEGY
from config import NEO4J_DATABASE, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from neo4j import GraphDatabase


def connect_neo4j(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD, database=NEO4J_DATABASE):
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

    store = connect_neo4j()
    g = Graph(store=store)
    g += original_graph
    g.commit()
    g.close()
    print("[INFO] Grafo RDF salvo com sucesso no Neo4j!")

def visualize_rdf_graph_neo4j(ciphertext, uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD):
    """
    Executa uma consulta Cypher no Neo4j e retorna os resultados.
    """
    driver = GraphDatabase.driver(uri, auth=(user, password))
    results = []
    with driver.session() as session:
        cypher_query = ciphertext
        records = session.run(cypher_query)
        for record in records:
            results.append(record.data())
    driver.close()
    return results    