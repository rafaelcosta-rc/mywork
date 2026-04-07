if os.path.exists(arquivo):
    try:
        df = pd.read_csv(arquivo, on_bad_lines='skip')

        # 🔥 valida estrutura
        colunas_esperadas = ["data", "nivel", "titulo", "situacao", "pensamento", "acao"]

        if not all(col in df.columns for col in colunas_esperadas):
            st.warning("Arquivo antigo incompatível. Criando novo...")
            os.remove(arquivo)
            st.rerun()

    except:
        st.warning("Arquivo corrompido. Reiniciando base...")
        os.remove(arquivo)
        st.rerun()
