import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def configurar_tradutor():
    """Configura o modelo Gemini com foco em tradução contextual de alta qualidade."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Erro: GOOGLE_API_KEY não encontrada no arquivo .env.")
        return None

    genai.configure(api_key=api_key)
    
    # Instrução de Sistema para garantir uma tradução superior ao Google Translate
    system_instruction = (
        "Você é um tradutor poliglota especialista em Português do Brasil (PT-BR). "
        "Sua tarefa é detectar o idioma de origem e traduzir o texto de forma natural, "
        "respeitando gírias e o contexto cultural. "
        "IMPORTANT: Mantenha os seguintes termos técnicos de Cibersegurança em sua forma original (Glossário): "
        "Phishing, Malware, Ransomware, Firewall, Pentest, Exploit, Payload, Log, DDoS, Botnet, SOC, EDR. "
        "Evite traduções literais para estes termos; prefira adaptações que façam sentido para um brasileiro."
    )
    
    return genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=system_instruction
    )

def obter_conteudo():
    """Permite ao usuário escolher entre digitar texto ou ler um arquivo."""
    print("\n[1] Digitar/Colar texto")
    print("[2] Ler de um arquivo .txt")
    print("[3] Processar pasta inteira (.txt)")
    opcao = input("Escolha o método de entrada (1, 2 ou 3): ").strip()

    if opcao == '1':
        return 'texto', input("\nDigite o texto para tradução:\n> ").strip()
    elif opcao == '2':
        caminho = input("\nDigite o caminho do arquivo .txt:\n> ").strip()
        if os.path.exists(caminho):
            return 'arquivo', caminho
        else:
            print("Erro: Arquivo não encontrado.")
    elif opcao == '3':
        pasta = input("\nDigite o caminho da pasta com arquivos .txt:\n> ").strip()
        if os.path.isdir(pasta):
            return 'pasta', pasta
        else:
            print("Erro: Pasta não encontrada.")
    return None, None

def executar_traducao():
    model = configurar_tradutor()
    if not model:
        return

    tipo, valor = obter_conteudo()
    if not tipo:
        return

    arquivos_para_processar = []

    if tipo == 'texto':
        arquivos_para_processar.append(("entrada_direta", valor))
    elif tipo == 'arquivo':
        with open(valor, 'r', encoding='utf-8') as f:
            arquivos_para_processar.append((valor, f.read()))
    elif tipo == 'pasta':
        for nome in os.listdir(valor):
            if nome.endswith(".txt") and not nome.endswith("_pt.txt"):
                caminho_completo = os.path.join(valor, nome)
                with open(caminho_completo, 'r', encoding='utf-8') as f:
                    arquivos_para_processar.append((caminho_completo, f.read()))

    for caminho, conteudo in arquivos_para_processar:
        try:
            print(f"\nTraduzindo: {os.path.basename(caminho)}...")
            prompt = f"Detecte o idioma original e traduza para PT-BR:\n\n{conteudo}"
            response = model.generate_content(prompt)

            if tipo == 'texto':
                print("\n" + "="*60 + "\nRESULTADO:\n" + response.text + "\n" + "="*60)
            else:
                # Salva na pasta aula-4 (mesma pasta do script)
                base_dir = os.path.dirname(os.path.abspath(__file__))
                nome_arquivo = os.path.basename(caminho)
                base, ext = os.path.splitext(nome_arquivo)
                novo_caminho = os.path.join(base_dir, f"{base}_pt{ext}")
                
                with open(novo_caminho, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"Salvo em: {os.path.basename(novo_caminho)}")

        except Exception as e:
            print(f"Erro ao processar {caminho}: {e}")

    print("\nProcessamento finalizado!")

if __name__ == "__main__":
    executar_traducao()