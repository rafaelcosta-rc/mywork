import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Ansiedade Sob Controle", layout="centered")

arquivo = "dados.csv"

# =========================
# 🎨 Cor tipo termômetro
# =========================
def cor_nivel(n):
    if n <= 3:
        return "#22c55e"
    elif n <= 6:
        return "#f97316"
    else:
        return "#ef4444"

# =========================
# 🧠 Título curto (máx 4 palavras)
# =========================
def gerar_titulo(situacao, pensamento):
    texto = (situacao + " " + pensamento).strip()
    palavras = texto.split()[:4]
    return " ".join(palavras)

# =========================
# 🔥 RESET AUTOMÁTICO CSV
# =========================
def carregar_dados():
    if not os.path.exists(arquivo):
        return pd.DataFrame()

    try:
        df = pd.read_csv(arquivo, on_bad_lines='skip')

        colunas_esperadas = ["data", "nivel", "titulo", "situacao", "pensamento", "acao"]

        if not all(col in df.columns for col in colunas_esperadas):
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
# FORMULÁRIO
# =========================
st.subheader("📍 Registro de Hoje")

with st.form("form", clear_on_submit=True):

    nivel = st.slider("Nível de ansiedade", 0, 10)

    # barra visual
    cor = cor_nivel(nivel)
    st.markdown(f"""
    <div style="width:100%; background:#ddd; border-radius:10px;">
        <div style="width:{nivel*10}%; background:{cor}; padding:10px; border-radius:10px;"></div>
    </div>
    """, unsafe_allow_html=True)

    situacao = st.text_area("Situação")
    pensamento = st.text_area("Pensamento")
    acao = st.text_area("Como agi")

    titulo_sugerido = gerar_titulo(situacao, pensamento)

    titulo = st.text_input("Título do registro", value=titulo_sugerido)

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
# LEITURA SEGURA
# =========================
st.divider()
st.subheader("📊 Evolução")

df = carregar_dados()

if not df.empty:

    st.line_chart(df["nivel"])

    st.subheader("📚 Histórico")

    idx = st.selectbox(
        "Selecione um registro",
        df.index,
        format_func=lambda i: f"{df.loc[i,'data']} - {df.loc[i,'titulo']}"
    )

    r = df.loc[idx]

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
