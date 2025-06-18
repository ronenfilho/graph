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

---

## Detalhamento por Pasta

### `graph/`
Contém toda a lógica principal da aplicação, configurações, e interface com o usuário.

- `config.py`: Define variáveis globais como URIs, caminhos de arquivos e IDs de referência.
- `interface.py`: Implementa a interface gráfica usando Streamlit.
- `main.py`: Permite execução direta da aplicação sem interface web.

### `graph/core/`
Reúne a lógica de negócio e serviços relacionados à manipulação de dados.

#### `core/etl/`
Módulo de **ETL (Extract, Transform, Load)**:
- `deputado_extraction.py`: Carrega dados de arquivos, APIs ou outras fontes.
- `deputado_transformation.py`: Limpa, filtra e normaliza os dados.
- `deputado_loading.py`: Insere os dados no destino final (Neo4j ou RDF).

#### `core/data/`
Organizado por tecnologia de persistência:

##### `data/rdf/`
- `rdf_utils.py`: Geração de triplas, serialização `.nt`, exportação para GraphML.
- `io_utils.py`: Utilitários para entrada/saída em RDF.

##### `data/neo4j/`
- `neo4j_utils.py`: Funções de conexão ao banco, execução de queries Cypher, e visualização com pyvis.

---

### `dataset/`
Armazena os dados utilizados na aplicação.

- `raw/`: Arquivos brutos (ex: `deputados_legisl_57.csv`).
- `processed/`: Arquivos derivados ou processados (ex: `deputados_legisl_57.nt`).

---

### `docs/`
Documentação do projeto.

- `arquitetura.md`: Diagrama e explicação técnica do sistema.
- `requisitos.md`: Lista de requisitos funcionais e não-funcionais.
- `images/`: Recursos visuais para os documentos.

---

### `tests/`
Local onde são armazenados os testes automatizados da aplicação, organizados por módulo.

---

### Arquivos da Raiz

- `.env`: Contém variáveis de ambiente privadas (não deve ser versionado).
- `.gitignore`: Arquivos e diretórios ignorados pelo Git.
- `README.md`: Descrição geral do projeto, como instalar e rodar.
- `requirements.txt`: Lista de pacotes obrigatórios para rodar a aplicação.
- `requirements_dev.txt`: Lista de pacotes adicionais para testes e desenvolvimento.
- `setup.py`: Permite empacotar o projeto como uma biblioteca/módulo Python instalável via `pip`.
