import streamlit as st
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Calculadora IMC - Kensei", page_icon="⚖️")

st.title("⚖️ Calculadora de IMC")
st.write("Insira seus dados abaixo para calcular o seu Índice de Massa Corporal.")

# Criando colunas para organizar os inputs
col1, col2 = st.columns(2)

with col1:
    peso = st.number_input("Digite seu peso (kg):", min_value=1.0, max_value=300.0, value=75.0, step=0.1)

with col2:
    altura = st.number_input("Digite sua altura (m):", min_value=0.5, max_value=2.5, value=1.75, step=0.01)

# Botão de ação
if st.button("Calcular IMC", use_container_width=True):
    # Cálculo do IMC: peso / (altura * altura)
    imc = peso / (altura ** 2)
    
    st.divider()
    st.subheader(f"Seu IMC é: **{imc:.2f}**")
    
    # Lógica de classificação e feedback visual
    if imc < 18.5:
        st.info("Classificação: **Abaixo do peso** ⚠️")
        cor_barra = 0.2
    elif 18.5 <= imc < 25:
        st.success("Classificação: **Peso ideal** ✅")
        cor_barra = 0.5
    elif 25 <= imc < 30:
        st.warning("Classificação: **Sobrepeso** 🟠")
        cor_barra = 0.7
    else:
        st.error("Classificação: **Obesidade** 🚨")
        cor_barra = 1.0

    # Gráfico de Barras para Visualização das Faixas
    st.write("### Posicionamento nas Faixas")
    fig, ax = plt.subplots(figsize=(10, 2))
    
    # Criando as barras coloridas das faixas
    ax.barh(0, 18.5, color='skyblue', label='Abaixo do peso')
    ax.barh(0, 6.5, left=18.5, color='#90ee90', label='Peso ideal')
    ax.barh(0, 5, left=25, color='#ffcc00', label='Sobrepeso')
    ax.barh(0, 15, left=30, color='#ff4d4d', label='Obesidade')

    # Adicionando o marcador do usuário
    ax.axvline(x=imc, color='black', linestyle='-', linewidth=4)
    ax.text(imc, 0.6, 'VOCÊ', color='black', ha='center', weight='bold')

    # Estilização do gráfico
    ax.set_yticks([])
    ax.set_xlim(10, 45)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.5), ncol=4, fontsize='small')
    st.pyplot(fig)

    # Barra de progresso visual (normalizada entre 0.0 e 1.0 baseada em um limite de IMC 50)
    valor_progresso = min(imc / 50, 1.0)
    st.progress(valor_progresso, text=f"Posicionamento na escala (IMC {imc:.1f})")
    
    st.caption("Nota: Esta é uma ferramenta educacional. Consulte um profissional de saúde para avaliações clínicas.")

with st.sidebar:
    st.header("Sobre")
    st.info("App desenvolvido na Aula 7 da Kensei Cyber AI Academy para estudo de interfaces Python.")