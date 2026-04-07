import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Ansiedade Sob Controle", layout="centered")

arquivo = "dados.csv"

# =========================
# 🧠 Gerador de título (até 4 palavras)
# =========================
def gerar_titulo(situacao, pensamento):
    texto = (situacao + " " + pensamento).strip()
    palavras = texto.split()
    return " ".join(palavras[:4]) if palavras else ""

# =========================
# 🔥 Carregar dados com proteção
# =========================
def carregar_dados():
    if not os.path.exists(arquivo):
        return pd.DataFrame()

    try:
        df = pd.read_csv(arquivo, on_bad_lines='skip')

        colunas = ["data", "nivel", "titulo", "situacao", "pensamento", "acao"]

        if not all(col in df.columns for col in colunas):
            os.remove(arquivo)
            return pd.DataFrame()

        return df

    except:
        os.remove(arquivo)
        return pd.DataFrame()

# =========================
# UI
# =========================
st.title("🧠 Ansiedade Sob Controle")
st.write("Registre e acompanhe sua evolução.")

# =========================
# BARRA GRADIENTE (LEGENDA)
# =========================
st.markdown("""
<div style="
    width:100%;
    height:15px;
    border-radius:10px;
    background: linear-gradient(to right, green, yellow, orange, red);
    margin-bottom:10px;
"></div>
<div style="display:flex; justify-content:space-between; font-size:12px;">
<span>0</span><span>10</span>
</div>
""", unsafe_allow_html=True)

# =========================
# FORMULÁRIO
# =========================
st.subheader("📍 Registro de Hoje")

with st.form("form", clear_on_submit=True):

    nivel = st.slider("Nível de ansiedade", 0, 10)

    situacao = st.text_area("Situação")
    pensamento = st.text_area("Pensamento")
    acao = st.text_area("Como agi")

    # 🔥 sugestão dinâmica
    titulo_sugerido = gerar_titulo(situacao, pensamento)

    titulo = st.text_input(
        "Título do registro",
        value=titulo_sugerido,
        placeholder="Sugestão automática aparecerá aqui"
    )

    salvar = st.form_submit_button("Salvar")

    if salvar:

        df_novo = pd.DataFrame([{
            "data": datetime.now(),
            "nivel": nivel,
            "titulo": titulo,
            "situacao": situacao,
            "pensamento": pensamento,
            "acao": acao
        }])

        if os.path.exists(arquivo):
            df_novo.to_csv(arquivo, mode="a", header=False, index=False)
        else:
            df_novo.to_csv(arquivo, index=False)

        st.success("Registro salvo com sucesso!")

# =========================
# DADOS
# =========================
st.divider()
st.subheader("📊 Evolução")

df = carregar_dados()

if not df.empty:

    st.line_chart(df["nivel"])

    st.subheader("📚 Histórico")

    # 🔥 opção vazia inicial
    opcoes = ["Selecione um registro"] + list(df.index)

    escolha = st.selectbox("Escolha", opcoes)

    if escolha != "Selecione um registro":

        r = df.loc[escolha]

        st.markdown("### Detalhes")
        st.write(f"📅 Data: {r['data']}")
        st.write(f"🧠 Nível: {r['nivel']}")
        st.write(f"📌 Título: {r['titulo']}")
        st.write(f"📍 Situação: {r['situacao']}")
        st.write(f"💭 Pensamento: {r['pensamento']}")
        st.write(f"⚡ Como agi: {r['acao']}")

else:
    st.info("Nenhum registro ainda.")

# =========================
# CTA
# =========================
st.divider()
st.markdown("📘 [Acessar e-book](SEU_LINK_AQUI)")
