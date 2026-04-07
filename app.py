import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Ansiedade Sob Controle", layout="centered")

arquivo = "dados.csv"

# 🎨 Função cor do termômetro
def cor_nivel(n):
    if n <= 3:
        return "green"
    elif n <= 6:
        return "orange"
    else:
        return "red"

# 🧠 Gerador simples de título (simula IA)
def gerar_titulo(situacao, pensamento):
    base = (situacao + " " + pensamento).strip()
    return base[:40] + "..." if len(base) > 40 else base

st.title("🧠 Ansiedade Sob Controle")

# 🔁 Session state (para limpar campos)
st.session_state.update({
    "situacao": "",
    "pensamento": "",
    "acao": ""
}) 

# 📍 Registro
st.subheader("📍 Registro de Hoje")

nivel = st.slider("Nível de ansiedade", 0, 10)

# 🎨 Barra visual tipo termômetro
cor = cor_nivel(nivel)
st.markdown(f"""
<div style="width:100%; background:#ddd; border-radius:10px;">
<div style="width:{nivel*10}%; background:{cor}; padding:10px; border-radius:10px;"></div>
</div>
""", unsafe_allow_html=True)

situacao = st.text_area("Situação", key="situacao")
pensamento = st.text_area("Pensamento", key="pensamento")
acao = st.text_area("Como agi", key="acao")

# 🧠 título automático
titulo = gerar_titulo(situacao, pensamento)
st.write(f"📌 Título sugerido: **{titulo}**")

if st.button("Salvar registro"):

    data = {
        "data": datetime.now(),
        "nivel": nivel,
        "titulo": titulo,
        "situacao": situacao,
        "pensamento": pensamento,
        "acao": acao
    }

    df_novo = pd.DataFrame([data])

    if os.path.exists(arquivo):
        df_novo.to_csv(arquivo, mode="a", header=False, index=False)
    else:
        df_novo.to_csv(arquivo, index=False)

    st.success("Registro salvo com sucesso!")

    # limpa usando rerun (melhor abordagem)
    st.session_state.situacao = ""
    st.session_state.pensamento = ""
    st.session_state.acao = ""
    st.rerun()

    # 🔁 limpar campos
    st.session_state.situacao = ""
    st.session_state.pensamento = ""
    st.session_state.acao = ""

st.divider()

# 📊 Evolução
st.subheader("📊 Sua evolução")

if os.path.exists(arquivo):
    df = pd.read_csv(arquivo)

    st.line_chart(df["nivel"])

    # 📌 histórico clicável (melhor que gráfico clicável)
    st.subheader("📚 Histórico")

    opcao = st.selectbox(
        "Selecione um registro",
        df.index,
        format_func=lambda i: f"{df.loc[i,'data']} - {df.loc[i,'titulo']}"
    )

    registro = df.loc[opcao]

    st.markdown("### Detalhes do registro")
    st.write(f"📅 Data: {registro['data']}")
    st.write(f"🧠 Nível: {registro['nivel']}")
    st.write(f"📌 Título: {registro['titulo']}")
    st.write(f"📍 Situação: {registro['situacao']}")
    st.write(f"💭 Pensamento: {registro['pensamento']}")
    st.write(f"⚡ Como agi: {registro['acao']}")

else:
    st.info("Nenhum dado registrado ainda.")

st.divider()

# 💰 Integração com e-book
st.subheader("📘 Aprofunde seu controle")

st.markdown("""
👉 Acesse o método completo:

[📥 Ansiedade Sob Controle](SEU_LINK_AQUI)
""")
