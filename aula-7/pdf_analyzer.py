import streamlit as st
from openai import OpenAI
from pypdf import PdfReader
import io
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Kensei PDF Intel Analyzer", page_icon="📑", layout="wide")

st.title("📑 PDF Intel Analyzer")
st.markdown("Faça upload de documentos para análise automática, classificação e chat contextual.")

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    api_key = st.text_input("Insira sua OpenAI API Key:", type="password")
    model_choice = st.selectbox("Selecione o Modelo:", ["gpt-4o-mini", "gpt-4o"])
    
    st.divider()
    st.header("📜 Histórico de Análises")
    if "analysis_history" in st.session_state and st.session_state.analysis_history:
        for item in reversed(st.session_state.analysis_history):
            with st.expander(f"📄 {item['filename']} ({item['date']})"):
                st.markdown(item['summary'])
    else:
        st.info("Nenhuma análise no histórico.")

    st.divider()
    if st.button("🧹 Limpar Tudo"):
        st.session_state.clear()
        st.rerun()

# Inicialização do estado da sessão
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

# Upload do arquivo
uploaded_file = st.file_uploader("Selecione um arquivo PDF", type="pdf")

if uploaded_file:
    # Extração de texto do PDF
    if not st.session_state.pdf_text:
        with st.spinner("Extraindo texto do documento..."):
            reader = PdfReader(uploaded_file)
            extracted_text = ""
            for page in reader.pages:
                extracted_text += page.extract_text() + "\n"
            st.session_state.pdf_text = extracted_text
            st.success(f"Texto extraído: {len(extracted_text)} caracteres.")

    # Botão para disparar a análise inicial
    if st.button("🚀 Analisar e Classificar Documento"):
        if not api_key:
            st.error("Por favor, insira sua API Key na barra lateral.")
        else:
            client = OpenAI(api_key=api_key)
            with st.spinner("IA processando resumo e classificação..."):
                try:
                    prompt_analise = f"""
                    Analise o texto a seguir extraído de um PDF:
                    1. Forneça um resumo executivo em tópicos.
                    2. Classifique o tipo de documento (ex: Relatório, Contrato, Técnico, etc).
                    3. Identifique o nível de sensibilidade (Baixo, Médio, Alto).
                    
                    Texto:
                    {st.session_state.pdf_text[:4000]} 
                    """
                    response = client.chat.completions.create(
                        model=model_choice,
                        messages=[{"role": "user", "content": prompt_analise}]
                    )
                    st.session_state.analysis = response.choices[0].message.content
                    
                    # Salva no histórico do estado da sessão
                    st.session_state.analysis_history.append({
                        "filename": uploaded_file.name,
                        "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "summary": st.session_state.analysis
                    })
                except Exception as e:
                    st.error(f"Erro na análise: {e}")

# Exibição dos resultados e Chat
if st.session_state.analysis:
    st.divider()
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📊 Insights do Documento")
        st.markdown(st.session_state.analysis)

    with col2:
        st.subheader("💬 Conversar com o PDF")
        
        # Container para mensagens de chat
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if question := st.chat_input("Pergunte algo sobre este documento..."):
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                client = OpenAI(api_key=api_key)
                context_prompt = f"Com base no texto abaixo, responda à pergunta do usuário.\n\nContexto: {st.session_state.pdf_text[:8000]}\n\nPergunta: {question}"
                
                full_res = ""
                placeholder = st.empty()
                stream = client.chat.completions.create(model=model_choice, messages=[{"role": "user", "content": context_prompt}], stream=True)
                for chunk in stream:
                    full_res += (chunk.choices[0].delta.content or "")
                    placeholder.markdown(full_res + "▌")
                placeholder.markdown(full_res)
                st.session_state.chat_history.append({"role": "assistant", "content": full_res})