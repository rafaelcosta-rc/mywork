import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Ansiedade Sob Controle", layout="centered")

arquivo = "dados.csv"

# 🎨 Cor tipo termômetro
def cor_nivel(n):
    if n <= 3:
        return "#22c55e"   # verde
    elif n <= 6:
        return "#f97316"   # laranja
    else:
        return "#ef4444"   # vermelho

# 🧠 Gerador simples de título
def gerar_titulo(situacao, pensamento):
    base = (situacao + " " + pensamento).strip()
    return base[:50] + "..." if len(base) > 50 else base

st.title("🧠 Ansiedade Sob Controle")
st.write("Registre, entenda e evolua sua ansiedade.")

# =========================
# 📍 FORMULÁRIO (CORRETO)
# =========================
st.subheader("📍 Registro de Hoje")

with st.form("form_registro", clear_on_submit=True):

    nivel = st.slider("Nível de ansiedade", 0, 10)

    # 🎨 barra estilo termômetro
    cor = cor_nivel(nivel)
    st.markdown(f"""
    <div style="width:100%; background:#ddd; border-radius:10px;">
        <div style="width:{nivel*10}%; background:{cor}; padding:10px; border-radius:10px;"></div>
    </div>
    """, unsafe_allow_html=True)

    situacao = st.text_area("Situação")
    pensamento = st.text_area("Pensamento")
    acao = st.text_area("Como agi")

    titulo = gerar_titulo(situacao, pensamento)
    st.write(f"📌 Título sugerido: **{titulo}**")

    salvar = st.form_submit_button("Salvar registro")

    if salvar:

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

# =========================
# 📊 GRÁFICO
# =========================
st.divider()
st.subheader("📊 Evolução da ansiedade")

if os.path.exists(arquivo):
    df = pd.read_csv(arquivo)
    st.line_chart(df["nivel"])

    # =========================
    # 📚 HISTÓRICO (Clicável)
    # =========================
    st.subheader("📚 Histórico")

    opcao = st.selectbox(
        "Selecione um registro",
        df.index,
        format_func=lambda i: f"{df.loc[i,'data']} - {df.loc[i,'titulo']}"
    )

    registro = df.loc[opcao]

    st.markdown("### Detalhes")
    st.write(f"📅 Data: {registro['data']}")
    st.write(f"🧠 Nível: {registro['nivel']}")
    st.write(f"📌 Título: {registro['titulo']}")
    st.write(f"📍 Situação: {registro['situacao']}")
    st.write(f"💭 Pensamento: {registro['pensamento']}")
    st.write(f"⚡ Como agi: {registro['acao']}")

else:
    st.info("Nenhum dado registrado ainda.")

# =========================
# 💰 CTA (E-book)
# =========================
st.divider()
st.subheader("📘 Aprofunde seu controle")

st.markdown("""
👉 Acesse o método completo:

[📥 Ansiedade Sob Controle](SEU_LINK_AQUI)
""")
