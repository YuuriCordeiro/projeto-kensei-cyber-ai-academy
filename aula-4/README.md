# Aula 4 - Integração com IA Generativa (Google Gemini)

Nesta aula, exploramos como utilizar o modelo **Gemini 2.5 Flash** para automatizar tarefas de Cibersegurança, desde a análise de logs até a geração de relatórios estratégicos para diretoria (CISO).

## 🛡️ Configuração e Segurança

- **`.env`**: Armazena a `GOOGLE_API_KEY` de forma segura.
- **`.gitignore`**: Configurado para impedir que a chave de API e ambientes virtuais sejam expostos no repositório.
- **`requirements.txt`**: Lista de dependências (Google AI SDK, Pandas, Matplotlib, python-dotenv e Schedule).

## 🚀 Scripts de Interação e Chat

- **`gemini_integration.py`**: Script inicial de teste para validar a conexão com o Google AI Studio.
- **`ask_gemini.py`**: Permite fazer perguntas rápidas pelo terminal com tratamento de erros e listagem de modelos disponíveis.
- **`cyber_chatbot.py`**: Chatbot interativo com histórico de conversa.
    - **Persona**: Tutor especialista em Cibersegurança da Kensei Academy.
    - **Features**: Respostas em *streaming*, interface colorida no terminal e monitoramento de consumo de tokens.

## 📊 Análise de Dados e Relatórios

- **`text_analyzer.py`**: Processador de arquivos em lote.
    - Lê todos os arquivos `.txt` de uma pasta.
    - Gera um JSON estruturado com resumo (3 frases), análise de sentimento e 5 palavras-chave por arquivo.
    - Saída: `analise_completa.json`.
- **`executive_report_gen.py`**: O ápice da automação.
    - Usa **Pandas** para processar CSVs de ataques.
    - Gera gráficos com **Matplotlib** (`top_ataques.png` e `distribuicao_paises.png`).
    - Solicita à IA a escrita de um **Relatório Executivo em Markdown**, incluindo as imagens e recomendações estratégicas.

## 🌍 Tradução Técnica Contextual

- **`translator.py`**: Tradutor inteligente para PT-BR.
    - **Glossário Integrado**: Mantém termos como *Phishing, Malware e Ransomware* no original.
    - **Modos**: Aceita texto direto, arquivo individual ou processamento de pasta inteira.
    - **Output**: Arquivos traduzidos são salvos com o sufixo `_pt.txt` dentro da pasta `aula-4`.

## ⏰ Automação

- **`auto_report.py`**: Script de agendamento que utiliza a biblioteca `schedule` para rodar a geração do relatório executivo todos os dias em um horário específico, garantindo dados sempre atualizados para a gestão.

## 🛠️ Como Executar

1. Certifique-se de estar com o ambiente virtual ativo.
2. Instale as dependências:
   ```bash
   pip install -r aula-4/requirements.txt
   ```
3. Configure sua chave no arquivo `.env`.
4. Para rodar o chatbot:
   ```bash
   python aula-4/cyber_chatbot.py
   ```
5. Para gerar o relatório executivo:
   ```bash
   python aula-4/executive_report_gen.py
   ```

## 📈 Resultados Gerados

Os artefatos produzidos pelos scripts (como `analise.json`, `relatorio_executivo.md` e gráficos) são salvos automaticamente dentro desta pasta para manter a organização do projeto.

---
**Foco**: IA Generativa para Defesa Ativa e Governança de Cibersegurança.
```