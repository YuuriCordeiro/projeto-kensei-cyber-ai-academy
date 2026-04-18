import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def analisar_texto():
    """Recebe um texto e retorna uma análise estruturada em JSON via Gemini."""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("Erro: GOOGLE_API_KEY não encontrada.")
        return

    genai.configure(api_key=api_key)
    
    # Inicializamos o modelo 2.5 Flash que é excelente para extração de dados
    model = genai.GenerativeModel('gemini-2.5-flash')

    print("--- Analisador de Pastas Kensei Cyber AI ---")
    caminho_diretorio = input("\nDigite o caminho da pasta com arquivos .txt: ").strip()

    if not os.path.isdir(caminho_diretorio):
        print(f"Erro: O diretório '{caminho_diretorio}' não foi encontrado.")
        return

    # Filtra apenas arquivos .txt na pasta
    arquivos = [f for f in os.listdir(caminho_diretorio) if f.endswith('.txt')]
    
    if not arquivos:
        print("Nenhum arquivo .txt encontrado na pasta informada.")
        return

    resultados_lote = {}

    for nome_arquivo in arquivos:
        caminho_completo = os.path.join(caminho_diretorio, nome_arquivo)
        print(f"Processando: {nome_arquivo}...")

        try:
            with open(caminho_completo, 'r', encoding='utf-8') as f:
                texto_entrada = f.read()

            # Prompt estruturado
            prompt = (
                f"Analise o texto a seguir: '{texto_entrada}'. "
                "Retorne um JSON com exatamente estas chaves: "
                "'resumo' (string com exatamente 3 frases), "
                "'sentimento' (string indicando se é positivo, negativo ou neutro), "
                "'palavras_chave' (uma lista com as 5 palavras mais importantes)."
            )

            # Chamada da API
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )

            # Armazena o resultado usando o nome do arquivo como chave
            resultados_lote[nome_arquivo] = json.loads(response.text)

        except Exception as e:
            print(f"Erro ao processar {nome_arquivo}: {e}")

    # Salva todos os resultados em um único arquivo consolidado
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(base_dir, "analise_completa.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(resultados_lote, f, indent=4, ensure_ascii=False)
        
    print(f"\nProcessamento concluído! Resultados consolidados em: {output_file}")

if __name__ == "__main__":
    analisar_texto()