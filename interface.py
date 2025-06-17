import streamlit as st
import pandas as pd
import os

from scripts import deputado_extraction, deputado_transformation, deputado_loading
from config import RAW_DATA, PROCESSED_DATA, IMG_DATA, ID_LEGISLATURA

st.set_page_config(page_title="ETL - Deputados", layout="centered")
# Exemplos de emojis para títulos:
# ⚙️ Engrenagem
# 🏛️ Parlamento
# 🗂️ Arquivo
# 🧩 Quebra-cabeça
# 🧑‍💼 Deputado
# 🗳️ Urna
# 📈 Gráfico
# 🧠 Inteligência
# 🔄 Atualizar


st.title("⚙️ ETL de Deputados Federais")
st.markdown("### Estudo de caso: Dados Abertos da Câmara dos Deputados")

csv_path = os.path.join(RAW_DATA, f"deputados_legisl_{ID_LEGISLATURA}.csv")
nt_path = os.path.join(PROCESSED_DATA, f"deputados_legisl_{ID_LEGISLATURA}.nt")

# Menu principal com abas
menu = st.sidebar.radio(
        "Menu", ["🏛️ Início", "🧑‍💼ETL - Deputado"],
        help="Selecione uma opção para iniciar o processo ETL."
        )

if menu == "🏛️ Início":
    st.image(
        os.path.join(IMG_DATA, "etl_semantic_pipeline.png"),
        caption="Pipeline ETL Semântico",
        use_container_width=True
    )
    st.header("Bem-vindo ao ETL de Deputados Federais!")
    st.markdown("""
    Este projeto demonstra um pipeline ETL completo para extrair, transformar e carregar dados dos deputados federais da Câmara dos Deputados do Brasil.
    
    **Passos do ETL:**
    1. **Extração**: Coleta os dados dos deputados via API.
    2. **Transformação**: Converte os dados para o formato RDF e gera um arquivo N-Triples (.nt).
    3. **Carga**: Carrega os dados no banco de dados Neo4j e gera visualizações gráficas.
    
    Use o menu lateral para navegar entre as etapas do processo.
    """)

if menu == "🧑‍💼ETL - Deputado":
    tab1, tab2, tab3 = st.tabs(["🔁 Extração", "🔁 Transformação", "🔁 Carga"])

    # Aba de Extração
    with tab1:
        st.header("🔁 Extração")
        if st.button("Executar Extração"):
            deputado_extraction.main()
            st.success("✅ Dados extraídos com sucesso!")

        # Visualização de arquivos gerados
        st.markdown("---")

        if os.path.exists(csv_path):
            st.markdown("**📄 CSV - Deputados**")
            df = pd.read_csv(csv_path)
            st.dataframe(df.head(20))
        else:
            st.warning("CSV não encontrado. Execute a etapa de extração.")    

    # Aba de Transformação
    with tab2:
        st.header("🔁 Transformação")
        if st.button("Executar Transformação"):
            deputado_transformation.main()
            st.success("✅ Transformação e exportação concluídas!")

        # Visualização de arquivos gerados
        st.markdown("---")

        if os.path.exists(nt_path):
            st.markdown("**🧠 RDF (formato .nt)**")
            with open(nt_path, "r", encoding="utf-8") as f:
                nt_preview = f.read(2000)
                st.code(nt_preview, language="turtle")
        else:
            st.warning("Arquivo RDF .nt não encontrado. Execute a etapa de transformação.")


    # Aba de Carga
    with tab3:
        st.header("🔁 Carga")
        if st.button("Executar Carga"):
            deputado_loading.main()
            st.success("✅ Carga concluída!")

        # Exibir imagem após a carga
        st.markdown("---")
        image_path = os.path.join(IMG_DATA, "deputado_204445-Fernando Mineiro_graph.png")
        if os.path.exists(image_path):
            st.markdown("### 🖼️ Visualização do Grafo do Deputado")
            st.image(
                image_path,
                caption="Grafo do Deputado",
                use_container_width=True
            )
        else:
            st.info("Imagem do grafo não encontrada. Execute a carga para gerar a imagem.")

# Footer
st.markdown("---")
st.markdown("Projeto de demonstração para pipelines ETL com RDF e Neo4j | Especialização em IA - IFG 2025")
