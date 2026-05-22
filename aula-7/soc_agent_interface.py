import streamlit as st
import requests
import json
from datetime import datetime
from fpdf import FPDF
import io

# Configuração da página
st.set_page_config(page_title="Kensei SOC Agent Interface", page_icon="🕵️", layout="wide")

def generate_pdf(data):
    """Gera um relatório de investigação formatado em PDF."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "Kensei Cyber SOC - Investigação de IoC", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 10, f"Data/Hora: {data['time']}", ln=True)
    pdf.cell(0, 10, f"Indicador (IoC): {data['target']}", ln=True)
    pdf.cell(0, 10, f"Classificação: {data['classification']}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Detalhes Técnicos da Investigação:", ln=True)
    pdf.set_font("courier", "", 10)
    details = json.dumps(data['result'], indent=4, ensure_ascii=False)
    pdf.multi_cell(0, 5, details)
    return pdf.output()

if "history" not in st.session_state:
    st.session_state.history = []
if "last_investigation" not in st.session_state:
    st.session_state.last_investigation = None

st.title("🕵️ Kensei SOC Agent Interface")
st.markdown("Envie um IP ou URL para o agente de segurança do n8n e obtenha uma análise de reputação.")

# --- SIDEBAR PARA CONFIGURAÇÕES ---
with st.sidebar:
    st.header("⚙️ Configurações do Agente n8n")
    n8n_webhook_url = st.text_input(
        "URL do Webhook do Agente SOC (n8n):",
        placeholder="Cole a URL do seu webhook aqui",
        type="password" # Para ocultar a URL se for sensível
    )
    st.info("Certifique-se de que seu agente n8n está configurado para receber requisições POST.")
    st.markdown("---")
    st.markdown("Este app se comunica com um agente n8n que utiliza ferramentas como VirusTotal e URLScan para investigar IPs/URLs.")
    st.markdown("Você pode configurar o agente SOC no n8n conforme a `aula-6/README.md`.")
    
    st.divider()
    st.header("📜 Histórico")
    if st.session_state.history:
        for item in reversed(st.session_state.history):
            with st.expander(f"🕒 {item['time']} - {item['target']}"):
                st.write(f"**Status:** {item['classification']}")
                st.json(item['result'])
    else:
        st.info("Nenhuma investigação realizada nesta sessão.")

# --- INTERFACE PRINCIPAL ---
st.subheader("Insira o Indicador de Compromisso (IoC)")
ioc_input = st.text_input("IP ou URL para Investigar:", placeholder="Ex: 8.8.8.8 ou example.com")

if st.button("Investigar IoC", use_container_width=True):
    if not n8n_webhook_url:
        st.error("Por favor, insira a URL do Webhook do n8n na barra lateral.")
    elif not ioc_input:
        st.warning("Por favor, digite um IP ou URL para investigar.")
    else:
        with st.spinner(f"Enviando '{ioc_input}' para o Agente SOC..."):
            try:
                # Prepara o payload para o webhook do n8n
                # O nome da chave 'ip_or_url' é uma suposição baseada no uso comum de agentes
                # Pode ser necessário ajustar para o nome exato que seu webhook n8n espera
                payload = {"ip_or_url": ioc_input}
                
                # Faz a requisição POST para o webhook do n8n
                response = requests.post(n8n_webhook_url, json=payload)
                response.raise_for_status() # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
                
                result = response.json()
                classification = result.get("classification", "Desconhecido")

                # Armazena o resultado no histórico e no estado da sessão
                st.session_state.last_investigation = {
                    "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "target": ioc_input,
                    "result": result,
                    "classification": classification
                }
                st.session_state.history.append(st.session_state.last_investigation)

            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao conectar com o webhook do n8n: {e}")
                st.error("Verifique se a URL está correta e se o n8n está rodando e acessível.")
            except json.JSONDecodeError:
                st.error("Erro: A resposta do webhook do n8n não é um JSON válido.")
                st.text(f"Resposta recebida: {response.text}")
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")

if st.session_state.last_investigation:
    invest = st.session_state.last_investigation
    st.divider()
    st.subheader(f"✅ Resultado da Investigação: {invest['target']}")
    
    if invest["classification"] == "Malicioso":
        st.error(f"Classificação: **{invest['classification']}** 🚨")
    elif invest["classification"] == "Suspeito":
        st.warning(f"Classificação: **{invest['classification']}** 🟠")
    else:
        st.success(f"Classificação: **{invest['classification']}** ✅")
    
    st.write("Detalhes da Resposta:")
    st.json(invest["result"])

    # Geração e Download do PDF
    pdf_bytes = generate_pdf(invest)
    st.download_button(
        label="📥 Baixar Relatório Completo em PDF",
        data=pdf_bytes,
        file_name=f"investigacao_{invest['target'].replace('.', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

st.caption("Desenvolvido para a Kensei Cyber AI Academy - Aula 7")