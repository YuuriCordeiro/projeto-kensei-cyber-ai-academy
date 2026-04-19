import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def configurar_ia():
    """Configura o modelo Gemini para o projeto TextFix AI."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Erro: GOOGLE_API_KEY não encontrada no arquivo .env.")
        return None

    genai.configure(api_key=api_key)
    
    # Instrução de sistema para definir o comportamento do editor
    system_instruction = (
        "Você é o 'TextFix AI', um assistente avançado de escrita. "
        "Sua função é corrigir gramática, ortografia, pontuação e melhorar o estilo do texto. "
        "Você deve ser capaz de adaptar o texto para diferentes tons: normal, formal ou gerar um resumo."
    )
    
    return genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=system_instruction
    )

def executar_textfix():
    """Interface de terminal para interação com o TextFix AI."""
    model = configurar_ia()
    if not model:
        return

    print("\n" + "="*50)
    print("      ✨ TextFix AI - Seu Editor com Inteligência Artificial")
    print("="*50)
    print("Instruções: Escolha um modo e insira seu texto.")

    while True:
        print("\nMODOS DISPONÍVEIS:")
        print("[1] Normal (Melhoria geral e fluidez)")
        print("[2] Formal (Tom profissional e acadêmico)")
        print("[3] Resumo (Síntese dos pontos principais)")
        print("[4] Sair")
        
        opcao = input("\nSelecione o modo (1-4): ").strip()

        if opcao == '4':
            print("\nEncerrando o TextFix AI. Mantenha seu texto impecável!")
            break
        
        if opcao not in ['1', '2', '3']:
            print("Opção inválida. Por favor, escolha entre 1 e 4.")
            continue

        texto_entrada = input("\nDigite ou cole o texto abaixo:\n> ").strip()
        
        if not texto_entrada:
            print("Aviso: O texto de entrada não pode estar vazio.")
            continue

        # Construção dinâmica do prompt baseada no modo escolhido
        modos = {
            "1": ("Melhoria Normal", "Corrija a gramática e melhore a clareza deste texto mantendo um tom natural:"),
            "2": ("Refinamento Formal", "Reescreva este texto de forma estritamente formal, polida e profissional:"),
            "3": ("Resumo Estruturado", "Crie um resumo conciso e organizado destacando os pontos essenciais deste texto:")
        }
        
        nome_modo, instrucao = modos[opcao]
        prompt = f"{instrucao}\n\n{texto_entrada}"

        try:
            print(f"\n[IA] Processando no modo: {nome_modo}...")
            response = model.generate_content(prompt)
            
            print("\n" + "-"*50)
            print(f"RESULTADO ({nome_modo.upper()}):")
            print("-" * 50)
            print(response.text.strip())
            print("-" * 50)
            
        except Exception as e:
            print(f"\n[ERRO] Não foi possível processar o texto: {e}")

if __name__ == "__main__":
    executar_textfix()