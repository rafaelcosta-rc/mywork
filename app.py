import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Ansiedade Sob Controle", layout="centered")

arquivo = "dados.csv"

# =========================
# 🔐 CONTROLE DE ACESSO
# =========================
if "usuarios" not in st.session_state:
    st.session_state.usuarios = {}

email = st.text_input("Digite seu e-mail para acessar")

if email:

    if email not in st.session_state.usuarios:
        st.session_state.usuarios[email] = {
            "data_inicio": datetime.now()
        }

    data_inicio = st.session_state.usuarios[email]["data_inicio"]
    dias = (datetime.now() - data_inicio).days

    if dias <= 7:

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
        st.write(f"Dia {dias+1}/7 do seu acesso inicial")

        # =========================
        # BARRA GRADIENTE (CORRIGIDA)
        # =========================
        st.markdown(
            '<div style="width:100%;height:15px;border-radius:10px;background: linear-gradient(to right, green, yellow, orange, red);margin-bottom:8px;"></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div style="display:flex; justify-content:space-between; font-size:12px; color:gray;">'
            '<span>Muito baixa</span>'
            '<span>Baixa</span>'
            '<span>Moderada</span>'
            '<span>Alta</span>'
            '<span>Muito alta</span>'
            '</div>',
            unsafe_allow_html=True
        )

        # =========================
        # FORMULÁRIO
        # =========================
        st.subheader("📍 Registro de Hoje")

        with st.form("form", clear_on_submit=True):

            nivel = st.slider("Nível de ansiedade", 0, 10)

            # Feedback automático
            if nivel <= 3:
                st.info("Nível baixo de ansiedade")
            elif nivel <= 6:
                st.warning("Nível moderado")
            elif nivel <= 8:
                st.warning("Nível alto")
            else:
                st.error("Nível muito elevado")

            situacao = st.text_area("Situação")
            pensamento = st.text_area("Pensamento")
            acao = st.text_area("Como agi")

            titulo = st.text_input("Título do registro", placeholder="Digite um título curto")

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
        st.markdown("📘 [Revisar método completo](SEU_LINK_AQUI)")

    else:
        # 🔒 BLOQUEIO
        st.warning("Seu período inicial de 7 dias terminou.")

        st.markdown("""
        Para continuar utilizando o app completo e acompanhar sua evolução:

        👉 Assine o plano mensal por apenas R$9,90
        """)

        st.link_button("Assinar agora", "SEU_LINK_KIWIFY")
