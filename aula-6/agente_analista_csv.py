import os # Já presente
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

# Carregamento das variáveis de ambiente do arquivo .env
load_dotenv()

def iniciar_analista_csv():
    """
    Configura e inicia o loop do chatbot analista de CSV.
    Solicita o caminho do CSV, carrega-o e interage com o Gemini
    para análise de dados via execução de código.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key: # Já presente
        print("Erro: GOOGLE_API_KEY não encontrada no arquivo .env.")
        print("Por favor, crie um arquivo .env na raiz do projeto com GOOGLE_API_KEY=SUA_CHAVE_AQUI.")
        return

    genai.configure(api_key=api_key)

    # Input inicial para o caminho do arquivo CSV
    csv_path = input("Por favor, digite o caminho completo do arquivo CSV (ex: dados.csv): ").strip()

    if not os.path.exists(csv_path):
        print(f"Erro: O arquivo '{csv_path}' não foi encontrado.")
        return
    
    try:
        df = pd.read_csv(csv_path)
        print(f"\nCSV '{csv_path}' carregado com sucesso. Dimensões: {df.shape}")
        print("Primeiras 5 linhas:")
        print(df.head().to_string())
        print("\nColunas disponíveis:")
        print(df.columns.tolist())
    except Exception as e:
        print(f"Erro ao carregar o CSV: {e}")
        return

    # Inicialização do cliente Gemini com code_execution habilitado
    # O modelo Gemini 1.5 Flash (ou superior) possui capacidade nativa de execução de código.
    # A instrução de sistema é crucial para guiar o modelo a usar essa capacidade.
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash', # Ou 'gemini-1.5-pro' para maior capacidade
        system_instruction=(
            "Você é um analista de dados especializado em CSVs. "
            "Seu objetivo é responder a perguntas sobre o arquivo CSV fornecido. "
            "Você tem acesso a um ambiente de execução de código Python. "
            "O DataFrame do CSV já está carregado e disponível como a variável global `df`. "
            "Sempre que precisar analisar os dados, gere o código Python apropriado usando a biblioteca 'pandas' e o DataFrame `df`. "
            "Não peça o arquivo CSV novamente. "
            "Apresente a resposta de forma clara e concisa, interpretando os resultados do código. "
            "Se o usuário pedir para ver o código, mostre-o. Caso contrário, apenas a resposta interpretada."
            f"\n\nInformações sobre o CSV carregado:\n"
            f"Colunas: {df.columns.tolist()}\n"
            f"Primeiras 5 linhas:\n{df.head().to_string()}\n"
            f"Descrição estatística:\n{df.describe().to_string()}"
        )
    )

    # Iniciar a sessão de chat. O SDK do Google Generative AI automaticamente
    # executa blocos de 'tool_code' gerados pelo modelo e alimenta os resultados de volta.
    chat = model.start_chat(history=[])

    print("\n" + "="*60)
    print("Kensei Cyber AI - Analista de CSV Ativo")
    print("Faça suas perguntas sobre o CSV. Digite 'sair' para encerrar.")
    print("="*60)

    # Loop de chat interativo
    while True:
        user_question = input("\nVocê > ").strip()

        if user_question.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando a sessão do analista de CSV. Até mais!")
            break

        if not user_question:
            continue

        try:
            # Envia a mensagem para o modelo. O SDK gerencia a execução de código
            # e a interpretação dos resultados pelo modelo.
            response = chat.send_message(user_question)
            
            # Imprime a resposta final interpretada pelo modelo
            print(f"Analista > {response.text}")

        except Exception as e:
            print(f"Erro na comunicação com o Gemini: {e}")
            print("Por favor, tente novamente ou digite 'sair' para encerrar.")

if __name__ == "__main__":
    iniciar_analista_csv()