import streamlit as st
from openai import OpenAI

# Configuração da página
st.set_page_config(page_title="Kensei OpenAI Chatbot", page_icon="🤖")

st.title("🤖 Chatbot OpenAI - Aula 7")
st.markdown("Interface de chat moderna utilizando Streamlit e a API da OpenAI.")

# Sidebar para configuração da chave
with st.sidebar:
    st.header("Configurações")
    api_key = st.text_input("Insira sua OpenAI API Key:", type="password")
    
    # Seletor de modelo
    model_choice = st.selectbox("Selecione o Modelo:", ["gpt-4o-mini", "gpt-4o"])
    
    st.info("Sua chave não é armazenada permanentemente e é usada apenas para esta sessão.")
    
    if st.button("Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()

# Inicializa o histórico de mensagens no estado da sessão (session_state)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens do histórico usando os componentes de chat (bubbles)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Lógica de entrada do usuário
if prompt := st.chat_input("Como posso ajudar hoje?"):
    if not api_key:
        st.error("Por favor, insira a sua API Key na barra lateral para começar.")
    else:
        # Adiciona mensagem do usuário ao histórico e exibe na tela
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Chamada para a API da OpenAI com suporte a Streaming
        try:
            client = OpenAI(api_key=api_key)
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Streaming da resposta para uma experiência mais fluida
                for response in client.chat.completions.create(
                    model=model_choice, 
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                ):
                    full_response += (response.choices[0].delta.content or "")
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
            
            # Adiciona resposta da IA ao histórico
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Erro na comunicação com OpenAI: {e}")