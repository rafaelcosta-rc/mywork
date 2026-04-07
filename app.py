import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Ansiedade Sob Controle", layout="centered")

# Estilo visual (premium simples)
st.markdown("""
    <style>
    body {background-color: #F2F2F2;}
    .stButton>button {
        background-color: #1f2937;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Ansiedade Sob Controle")
st.write("Registre, entenda e evolua sua ansiedade diariamente.")

arquivo = "dados.csv"

st.subheader("📍 Registro de Hoje")

nivel = st.slider("Nível de ansiedade", 0, 10)
situacao = st.text_area("Situação")
pensamento = st.text_area("Pensamento")

if st.button("Salvar registro"):
    data = {
        "data": datetime.now(),
        "nivel": nivel,
        "situacao": situacao,
        "pensamento": pensamento
    }

    df_novo = pd.DataFrame([data])

    if os.path.exists(arquivo):
        df_novo.to_csv(arquivo, mode="a", header=False, index=False)
    else:
        df_novo.to_csv(arquivo, index=False)

    st.success("Registro salvo com sucesso!")

st.divider()

st.subheader("📊 Sua evolução")

if os.path.exists(arquivo):
    df = pd.read_csv(arquivo)
    st.line_chart(df["nivel"])
else:
    st.info("Nenhum dado registrado ainda.")

if os.path.exists(arquivo):
    media = df["nivel"].mean()
    st.write(f"📈 Média de ansiedade: {round(media,1)}")

    if media <= 3:
        st.success("Baixo nível de ansiedade. Continue assim.")
    elif media <= 7:
        st.warning("Nível moderado. Atenção aos padrões.")
    else:
        st.error("Nível alto. Considere agir e buscar suporte.")
