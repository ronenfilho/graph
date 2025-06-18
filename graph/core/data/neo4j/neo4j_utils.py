from rdflib import Graph
from rdflib_neo4j import Neo4jStore, Neo4jStoreConfig, HANDLE_VOCAB_URI_STRATEGY
from graph.config import NEO4J_DATABASE, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from neo4j import GraphDatabase
from pyvis.network import Network
import tempfile
from collections import defaultdict


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

def data_rdf_graph_neo4j(ciphertext, uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD):
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

from pyvis.network import Network
import tempfile
import streamlit as st
import os
from neo4j import GraphDatabase

def draw_neo4j_graph(cypher_query, uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD):
    """
    Executa uma consulta Cypher no Neo4j e exibe o grafo no Streamlit usando pyvis.
    Espera que a query retorne: source, target, rel (tipo da relação).
    Nós com mais conexões terão tamanho maior e cores diferentes.
    """
    driver = GraphDatabase.driver(uri, auth=(user, password))
    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
    
    # Contadores de conexões por nó
    node_degrees = defaultdict(int)
    edges = []

    with driver.session() as session:
        results = session.run(cypher_query)
        for record in results:
            source = str(record["source"])
            target = str(record["target"])
            rel = str(record["rel"])

            # Contabiliza grau
            node_degrees[source] += 1
            node_degrees[target] += 1
            edges.append((source, target, rel))

    # Define estilos baseados no grau
    for node, degree in node_degrees.items():
        size = 10 + degree * 2  # aumenta tamanho conforme grau
        color = "#ff9999" if degree > 5 else "#99ccff"  # cor diferente se for "mais relevante"
        net.add_node(node, label=node, size=size, color=color)

    # Adiciona arestas
    for source, target, rel in edges:
        net.add_edge(source, target, label=rel)

    driver.close()

    # Salvar grafo como HTML temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        tmp_path = tmp_file.name

    # Exibir no Streamlit
    with open(tmp_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=650)
    os.remove(tmp_path)