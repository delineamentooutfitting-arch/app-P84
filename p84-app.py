import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Desenhos P84",
    page_icon="📄",
    layout="centered"
)

RAW_LOGO_URL = "https://raw.githubusercontent.com/delineamentooutfitting-arch/app-P84/main/SEATRIUM.png"

URL_PLANILHA_DESENHOS = "https://raw.githubusercontent.com/delineamentooutfitting-arch/app-P84/main/DESENHOS%20P84%20REV.xlsx"


@st.cache_data(ttl=600)
def carregar_dados_desenhos(url):
    return pd.read_excel(url, engine="openpyxl")


def render_logo_titulo(titulo, subtitulo=None):
    col_logo, col_texto = st.columns([0.12, 0.88])

    with col_logo:
        try:
            st.image(RAW_LOGO_URL, width=60)
        except:
            pass

    with col_texto:
        st.markdown(
            f"<h1 style='margin:0'>{titulo}</h1>",
            unsafe_allow_html=True
        )

        if subtitulo:
            st.caption(subtitulo)


def top_bar():
    render_logo_titulo(
        "Desenhos P84",
        "Consulta de Revisões de Desenhos"
    )


def buscar_desenho(df, termo):
    filtro = df["DESENHO"].astype(str).str.contains(
        termo,
        case=False,
        na=False
    )
    return df[filtro]


def ordenar_revisoes(revisoes):
    numericas = [r for r in revisoes if str(r).isdigit()]
    letras = [r for r in revisoes if str(r).isalpha()]
    return sorted(numericas, key=int) + sorted(letras)


def main_app():

    top_bar()

    try:
        df = carregar_dados_desenhos(URL_PLANILHA_DESENHOS)
    except Exception as e:
        st.error(f"Erro ao carregar a planilha: {e}")
        return

    termo_input = st.text_input(
        "Digite parte do nome do desenho (ex: M05B-391):"
    )

    if termo_input:

        resultados = buscar_desenho(df, termo_input)

        desenhos_encontrados = resultados["DESENHO"].unique()

        if len(desenhos_encontrados) > 0:

            st.markdown("### 🔍 Desenhos Encontrados:")

            for desenho in desenhos_encontrados:

                st.subheader(f"📄 {desenho}")

                revisoes = resultados[
                    resultados["DESENHO"] == desenho
                ]["REVISÃO"].drop_duplicates().tolist()

                revisoes_ordenadas = ordenar_revisoes(revisoes)

                st.markdown("**Revisões disponíveis:**")

                if revisoes_ordenadas:

                    cols = st.columns(len(revisoes_ordenadas))

                    ultima_revisao = revisoes_ordenadas[-1]

                    for i, rev in enumerate(revisoes_ordenadas):

                        destaque = (
                            "background-color:#ffd966;color:#000000;"
                            if rev == ultima_revisao
                            else "background-color:#e0e0e0;color:#000000;"
                        )

                        cols[i].markdown(
                            f"""
                            <div style="
                            {destaque}
                            padding:6px;
                            border-radius:6px;
                            text-align:center;
                            font-weight:bold;">
                            {rev}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    for i, rev in enumerate(revisoes_ordenadas):

                        if rev == ultima_revisao:

                            cols[i].markdown(
                                """
                                <div style="
                                margin-top:6px;
                                color:#ffd966;
                                font-weight:bold;">
                                ⬆ Esta é a última revisão disponível
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                else:
                    st.info(
                        "Nenhuma revisão encontrada para este desenho."
                    )

                st.markdown("---")

        else:
            st.info(
                "Nenhum desenho encontrado com esse trecho."
            )


if __name__ == "__main__":
    main_app()
