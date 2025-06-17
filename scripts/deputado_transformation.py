import sys
from pathlib import Path
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD
import os
from rdflib_neo4j import Neo4jStore, Neo4jStoreConfig, HANDLE_VOCAB_URI_STRATEGY
from etl.io_utils import load_csv

# Adiciona a raiz do projeto ao sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import RAW_DATA, PROCESSED_DATA


# Namespaces
SCHEMA = Namespace("http://schema.org/")
POL = Namespace("http://purl.org/ontology/politico/")
BR = Namespace("https://dadosabertos.camara.leg.br/recurso/")

def load_csv(filepath): 
    """
    Carrega o CSV dos deputados em um DataFrame pandas.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"O arquivo {filepath} não foi encontrado!")
    return pd.read_csv(filepath)

def create_rdf_graph():
    """
    Inicializa e retorna um grafo RDF com prefixos.
    """
    g = Graph()
    g.bind("schema", SCHEMA)
    g.bind("pol", POL)
    g.bind("foaf", FOAF)
    g.bind("br", BR)
    return g

def add_deputado_triples(g, row):
    """
    Adiciona as triplas RDF de um deputado ao grafo,
    representando partido e UF como nós (recursos).
    """
    deputado_uri = URIRef(f"https://dadosabertos.camara.leg.br/recurso/deputado/{row['id']}")
    partido_uri = URIRef(row['uriPartido'])
    uf_uri = URIRef(f"https://dadosabertos.camara.leg.br/recurso/uf/{row['siglaUf']}")

    # Deputado
    g.add((deputado_uri, RDF.type, SCHEMA.Person))
    g.add((deputado_uri, SCHEMA.name, Literal(row['nome'])))
    g.add((deputado_uri, SCHEMA.memberOf, partido_uri))
    g.add((deputado_uri, SCHEMA.addressRegion, uf_uri))
    g.add((deputado_uri, SCHEMA.identifier, Literal(row['id'], datatype=XSD.integer)))
    g.add((deputado_uri, FOAF.page, URIRef(row['uri'])))
    g.add((deputado_uri, SCHEMA.image, URIRef(row['urlFoto'])))
    g.add((deputado_uri, POL.legislatura, Literal(row['idLegislatura'], datatype=XSD.integer)))

    if pd.notna(row.get('email')):
        g.add((deputado_uri, SCHEMA.email, Literal(row['email'])))

    # Nó Partido
    g.add((partido_uri, RDF.type, SCHEMA.Organization))
    g.add((partido_uri, SCHEMA.name, Literal(row['siglaPartido'])))

    # Nó UF
    g.add((uf_uri, RDF.type, SCHEMA.Place))
    g.add((uf_uri, SCHEMA.name, Literal(row['siglaUf'])))

def build_rdf_graph_from_dataframe(df):
    """
    Cria e retorna o grafo RDF completo a partir do DataFrame.
    """
    g = create_rdf_graph()
    for _, row in df.iterrows():
        add_deputado_triples(g, row)
    return g

def save_graph_as_nt(g, output_path):
    """
    Salva o grafo RDF em formato N-Triples.
    """
    g.serialize(destination=output_path, format="nt")
    print(f"[INFO] Arquivo N-Triples '{output_path}' salvo com sucesso!")

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
        # Estratégia para lidar com URIs de vocabulário
        # Se você quiser ignorar URIs de vocabulário, use IGNORE
        # Se você quiser manter URIs de vocabulário como estão, use RAW
        # handle_vocab_uri_strategy=HANDLE_VOCAB_URI_STRATEGY.IGNORE,
        handle_vocab_uri_strategy=HANDLE_VOCAB_URI_STRATEGY.MAP,

        batching=True
    )

    store = Neo4jStore(config=config)
    g = Graph(store=store)
    g += original_graph
    g.commit()
    g.close()
    print("[INFO] Grafo RDF salvo com sucesso no Neo4j!")


def main():
    """
    Fluxo completo: carrega CSV, cria grafo RDF e salva N-Triples.
    """

    print("########################")
    print("## Transformação - Deputados ##")
    print("########################")
    print("\n")

    idLegislatura = "57" # Legislatura atual'

    #filepath = os.path.join(directory, "deputados_legisl_"+idLegislatura+".csv")
    csv_path = os.path.join(RAW_DATA, "deputados_legisl_"+idLegislatura+".csv")
    output_path = os.path.join(PROCESSED_DATA, "deputados_legisl_"+idLegislatura+".nt")

    df = load_csv(csv_path)
    g = build_rdf_graph_from_dataframe(df)

    # Salva como .nt
    save_graph_as_nt(g, output_path)

if __name__ == "__main__":
    main()
