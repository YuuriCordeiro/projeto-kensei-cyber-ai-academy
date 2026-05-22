# Aula 7 - Interfaces Modernas com Streamlit

Nesta aula, iniciamos a transição de ferramentas de linha de comando para interfaces gráficas web utilizando o **Streamlit**. O Streamlit permite que profissionais de segurança e cientistas de dados criem dashboards e ferramentas interativas de forma extremamente rápida usando apenas Python.

## 🛡️ Objetivo

O foco desta etapa é aprender a construir o "Front-end" das nossas automações de IA, permitindo que usuários não-técnicos possam interagir com nossos modelos e scripts de análise de logs.

## 🚀 O Primeiro App (`app.py`)

O arquivo inicial demonstra os conceitos fundamentais de reatividade e componentes:

- **`st.title`**: Define o título principal da aplicação.
- **`st.write`**: Renderiza textos e informações na tela.
- **`st.button`**: Implementa uma lógica de ação baseada no clique do usuário.
- **`st.success`**: Exibe notificações visuais de sucesso.

## ⚖️ Calculadora de IMC (`imc_app.py`)

Uma ferramenta prática que utiliza:
- **`st.number_input`**: Captura dados numéricos com validação.
- **`st.columns`**: Organiza a interface em colunas.
- **`st.progress`**: Fornece um feedback visual da escala de saúde.

## 🛡️ Cyber Dashboard (`dashboard.py`)

Um painel analítico completo para cibersegurança que inclui:
- **Sidebar**: Filtros dinâmicos por tipo de ataque e país.
- **KPIs**: Métricas principais (Total de alertas, vetores principais).
- **Visualizações**: Gráficos de barras e linhas integrados.
- **Data Management**: Uso de `st.cache_data` para carregamento otimizado de CSVs.

## 🤖 OpenAI Chatbot (`chatbot_openai.py`)

Integração com a API da OpenAI para criar um assistente inteligente:
- **Chat Bubbles**: Interface nativa de chat do Streamlit.
- **Session State**: Mantém o contexto da conversa durante a navegação.
- **API Key Input**: Permite ao usuário configurar sua própria chave de forma segura na interface.
- **Streaming**: Respostas geradas e exibidas em tempo real.

## 📑 PDF Intel Analyzer (`pdf_analyzer.py`)

Ferramenta de análise de documentos que utiliza:
- **`pypdf`**: Para extração de texto de arquivos PDF.
- **RAG (Augmented Generation)**: Chat contextual que responde baseado no conteúdo do arquivo.
- **Classificação**: IA identifica automaticamente a categoria e sensibilidade do dado.

## 🕵️ n8n SOC Agent Interface (`soc_agent_interface.py`)

Uma interface dedicada para interagir com agentes de segurança do n8n:
- **Integração com n8n**: Envia IPs/URLs para um webhook do n8n.
- **Análise de Reputação**: Exibe a classificação e os detalhes da investigação retornados pelo agente SOC.
- **Configuração Simples**: Campo para inserir a URL do webhook na sidebar.

## �️ Como Executar

1. Certifique-se de estar com o ambiente virtual ativo.
2. Instale a biblioteca necessária:
   ```bash
   pip install streamlit openai pypdf requests fpdf2
   ```
3. Execute a aplicação a partir do terminal:
   ```bash
   # Para o app inicial:
   python -m streamlit run "aula-7/app.py"
   # Para a calculadora de IMC:
   python -m streamlit run "aula-7/imc_app.py"
   # Para o Dashboard de Cyber:
   python -m streamlit run "aula-7/dashboard.py"
   # Para o Chatbot OpenAI:
   python -m streamlit run "aula-7/chatbot_openai.py"
   # Para o Analisador de PDF:
   python -m streamlit run "aula-7/pdf_analyzer.py"
   # Para a Interface do Agente SOC (n8n):
   python -m streamlit run "aula-7/soc_agent_interface.py"
   # Para o Gerenciador Doméstico:
   python -m streamlit run "aula-7/tarefas_domesticas.py"
   ```

---
**Kensei Cyber AI Academy**: *Construindo o futuro da defesa cibernética com inteligência artificial.*