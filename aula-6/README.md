# Aula 6 - Agentes Inteligentes com n8n

Nesta aula, avançamos para a orquestração de fluxos utilizando o **n8n**, criando um agente autônomo capaz de utilizar ferramentas externas para resolver problemas complexos e consultas de informação.

## 🤖 Configuração do Agente

- **Trigger**: `When Chat Message Received` (Permite testar o agente via chat interno do n8n).
- **Modelo**: `Google Gemini Chat Model` (Configurado com Gemini 1.5 Flash).
- **Memória**: `Window Buffer Memory` (Para manter o contexto da conversa).
- **System Prompt**: "assistente generalista que usa ferramentas quando precisa."

## 🛠️ Automações Incluídas

### 1. Agente Inteligente (`agente_n8n.json`)

- **Calculator**: Habilita o agente a realizar cálculos matemáticos complexos sem alucinações.
- **Wikipedia**: Permite que o agente busque informações atualizadas e fatos históricos diretamente na enciclopédia.

### 2. Agente Pesquisador Investigativo (`agente_pesquisador.json`)

- **SerpAPI**: Realiza buscas em tempo real no Google.
- **HTTP Request**: Ferramenta que permite ao agente "navegar" e extrair o texto de páginas web encontradas na busca.
- **Wikipedia**: Busca por fatos e dados históricos consolidados.
- **System Prompt**: "pesquisador investigativo."

### 3. Agente Analista de CSV (`agente_analista_csv.json`)

- **Trigger**: Telegram Bot (recebe CSV anexado e texto).
- **Code Tool (Pandas Analyzer)**: Executa Python (Pandas) para analisar o CSV.
- **Calculator**: Para cálculos matemáticos.
- **System Prompt**: "analista de dados que responde perguntas sobre CSVs."

### 4. Agente de Investigação de Segurança (`agente_investigacao_seguranca.json`)

- **VirusTotal**: Consulta a reputação de IPs e domínios em bancos de dados de ameaças globais.
- **URLScan**: Realiza a análise técnica de URLs para identificar phishing e sites maliciosos em tempo real.
- **System Prompt**: "analista de segurança (SOC) investigativo focado em reputação de IoCs."
- **Classificação**: O agente classifica automaticamente o alvo como Seguro, Suspeito ou Malicioso.

### 5. Agente Consultor de Design e Software (`agente_design_software.json`)

- **Persona**: Especialista híbrido em Design de Interiores, Arquitetura e UI/UX.
- **Objetivo**: Transformar ideias brutas em planos técnicos estruturados.
- **Memória**: Simple Memory para refinamento iterativo de projetos.
- **Tools**: Wikipedia (pesquisa técnica) e Calculator (dimensões e métricas).

## 📂 Como Usar
1. Abra seu n8n.
2. Importe os arquivos `.json` desejados.
3. Configure suas credenciais do Google Gemini no nó do modelo.
4. Para o Pesquisador, configure também a credencial da **SerpAPI** (Google Search).
5. Para o Analista de CSV, certifique-se de que o nó `Code Tool` está configurado com o script Python e os `Input Data` corretos.
6. Para o Agente de Investigação, insira suas chaves de API nos nós de ferramentas (VirusTotal e URLScan).