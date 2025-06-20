# 🧠 Semantic ETL Pipelines for Heterogeneous Knowledge Graph Construction  
### Estudo de Caso: Políticos do Brasil – Deputados Federais

---

## 📌 Visão Geral

Este projeto implementa uma pipeline **ETL Semântica (Extração, Transformação e Carga)** para a **unificação de dados heterogêneos** sobre deputados federais do Brasil. O objetivo é construir um **Grafo de Conhecimento (HKG - Heterogeneous Knowledge Graph)** que permita análises avançadas e integração semântica para sistemas de perguntas e respostas (QA Systems) e plataformas analíticas.

---

## 📊 Arquitetura do Pipeline

A estrutura segue o modelo representado abaixo:

Data Source (Extraction) → Business Layer (Transform) → Knowledge Graph (Load) → Presentation Layer


![Semantic ETL Architecture](./graph/docs/images/etl_semantic_pipeline.png)

[Consulte a arquitetura detalhada do pipeline no arquivo `graph/docs/arquitetura.md`](graph/docs/arquitetura.md)

---

## 📁 Estrutura do Projeto

```
graph_nous/
│
├── graph/               # Código principal da aplicação
│ ├── config.py          # Configurações globais (variáveis, paths, env)
│ ├── interface.py       # Interface Streamlit (frontend)
│ ├── main.py            # Execução local via terminal
│ └── core/              # Lógica de negócio e manipulação de dados
│    ├── etl/            # Extração, transformação e carga de dados (ETL)
│    └── data/           # Lógica de persistência e tecnologias específicas
│    │     ├── rdf/      # Manipulação de dados RDF (triplas, .nt, .ttl)
│    │     └── neo4j/    # Conexão e visualização de grafos Neo4j
│    │
├── dataset/             # Dados usados no projeto
│ ├── raw/               # Dados brutos (ex: CSVs originais)
│ └── processed/         # Dados processados (ex: .nt, .graphml)
│
├── docs/                # Documentação do projeto
│ ├── arquitetura.md     # Arquitetura do sistema
│ ├── requisitos.md      # Requisitos funcionais e não-funcionais
│ └── images/            # Imagens usadas na documentação
│
├── tests/               # Testes automatizados (unitários, integração)
│
├── .env                 # Variáveis de ambiente sensíveis (não versionar)
├── .gitignore           # Arquivos/pastas a serem ignorados pelo Git
├── README.md            # Você está aqui :). Descrição inicial do projeto
├── requirements.txt     # Dependências para produção
├── requirements_dev.txt # Dependências adicionais para desenvolvimento/testes
└── setup.py             # (Opcional) Empacotamento do projeto como módulo Python
```

[Consulte a estrutura detalhada do projeto `graph/docs/estrutura.md`](graph/docs/estrutura.md)

## 🚀 Como Executar

### **Pré-requisitos**

- **Clonar o projeto**

     ```bash
     git clone git@github.com:ronenfilho/graph_nous.git
     ```

- **Python 3.11+** instalado

- **Instale o Neo4J (https://neo4j.com/)**

- Arquivo `.env` configurado com as variáveis de ambiente necessárias

# 1. Criar ambiente virtual

```
python -m venv venv
# (Windows) ou source venv/bin/activate (Linux/Mac)
venv\Scripts\activate  
```
# 2. Instalar dependências

```
pip install -r requirements.txt
```

# 3. Rodar o projeto

```
python graph/main.py
```

## ▶️ Como Executar o Projeto Streamlit

Este guia apresenta os passos para rodar a interface do projeto utilizando o **Streamlit**.

### **Passos para Execução**

1. **Navegue até o diretório do projeto**

     No terminal, acesse o diretório onde está localizado o arquivo `interface.py`:
     ```bash
     cd caminho/para/seu/graph_nous
     ```

2. **Execute o Streamlit**

     Inicie a aplicação com o comando:
     ```bash
     streamlit run graph/interface.py
     ```

3. **Acesse a interface no navegador**

     O Streamlit abrirá automaticamente a interface no navegador.  
     Caso não abra, copie o link exibido no terminal (geralmente `http://localhost:8501`) e cole no navegador.

# Resultados

## Grafo - Nó Deputado

![Grafo - Deputado](./graph/docs/images/img_grafo_deputado.png)

## 🧰 Tecnologias Utilizadas

### 🐍 Python
- **Versão:** 3.11+

---

### 📊 Manipulação e Extração de Dados
- `pandas==2.3.0` — Estrutura de dados e análise tabular  
- `requests==2.32.4` — Requisições HTTP para APIs públicas

---

### 🌐 Semântica e Grafos RDF
- `rdflib==7.1.4` — Construção e serialização de triplas RDF  
- `rdflib_neo4j==1.1` — Integração de triplas RDF com o banco Neo4j  
- **Ontologias:** OWL / SKOS — Enriquecimento semântico e modelagem de conceitos

---

### 🧠 Banco de Grafos
- **GraphDB** — Armazenamento semântico e consultas SPARQL  
- **Neo4j** — Grafo orientado a relações e visualizações dinâmicas

---

### 📈 Visualização
- `matplotlib==3.10.3` — Gráficos analíticos e plots de dados  
- `networkx==3.5` — Modelagem e análise de grafos em Python  
- `pyvis==0.3.2` — Visualização interativa de grafos (HTML / Streamlit)

---

### 🌍 Interface Web
- `streamlit==1.45.1` — Construção de dashboards e aplicações web interativas

---

### ⚙️ Utilitários
- `python-dotenv==1.1.0` — Gerenciamento de variáveis de ambiente (.env)  
- `setuptools==80.9.0` — Empacotamento e instalação como módulo Python

---

### 📦 Criação do requirements.txt

```
pip freeze > requirements.txt
```

- **Gegar versão resumida** 
```
pipreqs . --force
```

---

## 🧪 Próximos Passos (TODO LIST)

- [✅] Carga de Deputados Federais (Brasil).
- [ ] Integração com dados de partidos e proposições legislativas.
- [✅] Normalização com identificadores globais (ex: **Wikidata**, **ORCID**).
- [✅] Geração automatizada de triplos RDF a partir de dados limpos.
- [✅] Visualização e consulta semântica com **Neo4j**, **Protégé** ou **SPARQL endpoints**.

---

## 👤 Autor

**Ronen Filho**  
Especialização em Inteligência Artificial Aplicada — *IFG Goiás*  
Projeto acadêmico voltado à unificação semântica de dados sobre políticos brasileiros.


