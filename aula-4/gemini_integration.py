import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da API Key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key or api_key == "SUA_CHAVE_AQUI":
    print("Erro: API Key não configurada. Adicione sua chave no arquivo .env")
else:
    genai.configure(api_key=api_key)

    # Inicializa o modelo (Utilizando a versão 2.5 Flash disponível na sua chave)
    model = genai.GenerativeModel('gemini-2.5-flash')

    def testar_conexao():
        prompt = "Olá Gemini! Sou um estudante de Cibersegurança e acabei de configurar meu ambiente. Pode me dar uma dica rápida de como IA pode ajudar a detectar ataques de Phishing?"
        
        try:
            print("Enviando prompt para o Google AI Studio...")
            response = model.generate_content(prompt)
            print("\n--- Resposta da IA ---")
            print(response.text)
        except Exception as e:
            print(f"Ocorreu um erro na requisição: {e}")

    if __name__ == "__main__":
        testar_conexao()