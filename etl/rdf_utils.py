from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD
import pandas as pd

# Namespaces
SCHEMA = Namespace("http://schema.org/")
POL = Namespace("http://purl.org/ontology/politico/")
BR = Namespace("https://dadosabertos.camara.leg.br/recurso/")

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
    Adiciona as triplas RDF de um deputado ao grafo.
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