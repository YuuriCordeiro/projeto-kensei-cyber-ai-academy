import streamlit as st

# Configuração do título da página
st.title("Aula 7: Minha Primeira Interface com Streamlit")

# Exibição de um texto explicativo
st.write("Este é o início da nossa jornada criando interfaces para ferramentas de Cibersegurança.")

# Campo para o usuário digitar o nome
nome = st.text_input("Qual é o seu nome?", placeholder="Digite aqui...")

# Lógica do botão
if st.button("Clique aqui para uma mensagem"):
    if nome:
        st.success(f"Parabéns, {nome}! Você criou seu primeiro botão interativo no Streamlit. 🚀")
    else:
        st.warning("Por favor, digite um nome antes de clicar no botão!")