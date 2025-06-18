## 📊 Arquitetura do Pipeline

A estrutura segue o modelo representado abaixo:

Data Source (Extraction) → Business Layer (Transform) → Knowledge Graph (Load) → Presentation Layer

![Semantic ETL Architecture](/graph/docs/images/etl_semantic_pipeline.png)

---

### 🔍 1. Camada de Extração — *Data Sources*

Integra diversas **fontes de dados heterogêneas**, como:

- JSON da API da Câmara dos Deputados  
- CSVs de bases públicas  
- Dados em XML, RDF ou HTML  
- Arquivos TXT, planilhas e outros

---

### 🛠️ 2. Camada de Transformação — *Business Layer*

Aqui ocorre o processamento semântico com apoio de **recursos linguísticos**:

- 🔹 *Data Cleaning* — limpeza e padronização dos dados
- 🔹 *Format Normalization* — conversão de formatos para RDF
- 🔹 *Semantic Enrichment* — enriquecimento com ontologias
- 🔹 *Entity Mapping* — correspondência de entidades (ex: nomes, partidos)
- 🔹 *RDF Triple Generation* — geração dos triplos semânticos

---

### 🔗 3. Camada de Carga — *Knowledge Graph (HKG)*

Após a transformação, os dados são carregados em um **grafo de conhecimento heterogêneo**, permitindo inferências, consultas SPARQL e integração com bases externas.

---

### 📈 4. Camada de Apresentação

O grafo pode ser explorado em duas frentes principais:

- **QA System** — sistema de perguntas e respostas sobre os dados políticos
- **Analytics** — visualizações, estatísticas e dashboards interativos