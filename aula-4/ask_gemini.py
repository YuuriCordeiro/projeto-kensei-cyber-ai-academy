import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def configurar_ia():
    """Configura a API do Google Generative AI."""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("Erro: GOOGLE_API_KEY não encontrada no arquivo .env.")
        return None

    genai.configure(api_key=api_key)
    
    # Configuração do comportamento da IA (System Instruction)
    system_instruction = (
        "Você é um especialista sênior em Cibersegurança da Kensei Cyber AI Academy. "
        "Sua função é analisar logs, explicar vulnerabilidades e sugerir remediações técnicas "
        "de forma clara, didática e profissional."
    )
    
    return genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=system_instruction
    )

def executar_prompt():
    """Solicita uma pergunta ao usuário e exibe a resposta da IA."""
    model = configurar_ia()
    
    if model:
        pergunta = input("O que você deseja perguntar ao Gemini? ")
        
        try:
            print("\nConsultando o Google AI Studio...")
            response = model.generate_content(pergunta)
            
            print("\n" + "="*50)
            print("RESPOSTA DO GEMINI:")
            print("="*50)
            
            # Verifica se a resposta foi gerada com sucesso
            if response.text:
                print(response.text)
            else:
                print("O modelo não retornou uma resposta. Isso pode ocorrer devido aos filtros de segurança.")
        except Exception as e:
            print(f"\n[ERRO] Ocorreu um problema na requisição: {e}")
            print("\nTentando listar modelos disponíveis para sua chave...")
            try:
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                print(f"Modelos que você pode usar: {models}")
            except Exception as list_error:
                print(f"Não foi possível listar os modelos: {list_error}")

if __name__ == "__main__":
    executar_prompt()