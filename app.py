import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.title("Diário de Ansiedade")

arquivo = "dados.csv"

nivel = st.slider("Nível de ansiedade", 0, 10)
situacao = st.text_area("Situação")
pensamento = st.text_area("Pensamento")

if st.button("Salvar"):
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

st.subheader("Evolução da ansiedade")

if os.path.exists(arquivo):
    df = pd.read_csv(arquivo)
    st.line_chart(df["nivel"])
else:
    st.info("Nenhum dado registrado ainda.")
