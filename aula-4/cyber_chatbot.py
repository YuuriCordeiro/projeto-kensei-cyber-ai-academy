import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def iniciar_chatbot():
    """Configura e inicia o loop do chatbot de cibersegurança."""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("Erro: GOOGLE_API_KEY não encontrada no arquivo .env.")
        return

    genai.configure(api_key=api_key)
    
    # System Instruction: Define a personalidade e o escopo da IA
    system_instruction = (
        "Você é o tutor oficial de Cibersegurança da Kensei Cyber AI Academy. "
        "Sua especialidade é análise de logs, pentest, defesa ativa e criptografia. "
        "Responda de forma técnica, porém didática. Se o usuário enviar um log, "
        "tente identificar anomalias imediatamente."
    )
    
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=system_instruction
    )

    # Inicializa a sessão de chat com histórico vazio
    chat = model.start_chat(history=[])

    # Cores ANSI
    COR_USUARIO = "\033[97m"  # Branco Brilhante
    COR_IA = "\033[92m"       # Verde
    COR_META = "\033[90m"     # Cinza para metadados
    RESET = "\033[0m"

    print("="*60)
    print("Kensei Cyber AI - Chatbot de Segurança Ativo")
    print("Digite 'sair' para encerrar o chat.")
    print("="*60)

    while True:
        try:
            # Usuário em branco
            user_input = input(f"\n{COR_USUARIO}Usuário > {RESET}").strip()

            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("\nEncerrando sessão. Mantenha-se seguro!")
                break

            if not user_input:
                continue

            # IA em verde
            print(f"\n{COR_IA}Especialista Gemini > ", end="", flush=True)
            
            # Envia a mensagem e recebe a resposta em modo streaming
            response = chat.send_message(user_input, stream=True)
            
            for chunk in response:
                print(chunk.text, end="", flush=True)
            print(RESET) # Reseta a cor e quebra linha

            # Exibe contagem de tokens (disponível após o fim do stream)
            usage = response.usage_metadata
            print(f"{COR_META}[Tokens: Entrada {usage.prompt_token_count} | Saída {usage.candidates_token_count} | Total {usage.total_token_count}]{RESET}")

        except KeyboardInterrupt:
            print("\n\nSessão interrompida pelo usuário.")
            break
        except Exception as e:
            print(f"\nErro na comunicação: {e}")

if __name__ == "__main__":
    iniciar_chatbot()