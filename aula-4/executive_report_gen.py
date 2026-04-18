import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

def configurar_ia():
    """Configura o Gemini com uma persona de executivo de Cibersegurança."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Erro: GOOGLE_API_KEY não encontrada.")
        return None
    
    genai.configure(api_key=api_key)
    
    # Instrução de Sistema para garantir o tom executivo
    system_instruction = (
        "Você é um CISO (Chief Information Security Officer) sênior. "
        "Sua tarefa é transformar dados técnicos brutos e estatísticas de logs em "
        "relatórios executivos estratégicos em formato Markdown, focando em riscos e recomendações. "
        "Sempre que houver imagens disponíveis, insira-as no relatório usando a sintaxe ![Legenda](nome_do_arquivo.png)."
    )
    
    return genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=system_instruction
    )

def gerar_relatorio(caminho_csv=None):
    model = configurar_ia()
    if not model: return

    # Define o diretório base como a pasta aula-4
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if not caminho_csv:
        caminho_csv = input("\nDigite o caminho do arquivo CSV de logs (ex: aula-3/cybersecurity_attacks.csv): ").strip()
    
    if not os.path.exists(caminho_csv):
        print(f"Erro: Arquivo '{caminho_csv}' não encontrado.")
        return

    try:
        # 1. Análise de Dados com Pandas
        print(f"Lendo e analisando dados de {caminho_csv}...")
        df = pd.read_csv(caminho_csv)
        
        # Extração de métricas (ajustado para as colunas comuns em datasets de cyber)
        total_eventos = len(df)
        top_ataques = df['Attack Type'].value_counts().head(3).to_dict() if 'Attack Type' in df.columns else "Dados não disponíveis"
        paises_origem = df['Country'].value_counts().head(3).to_dict() if 'Country' in df.columns else "Dados não disponíveis"
        
        # 2. Geração de Gráficos com Matplotlib
        print("Gerando gráficos estatísticos...")
        if 'Attack Type' in df.columns:
            df['Attack Type'].value_counts().head(5).plot(kind='bar', color='skyblue')
            plt.title('Top 5 Tipos de Ataque')
            plt.ylabel('Frequência')
            plt.tight_layout()
            plt.savefig(os.path.join(base_dir, 'top_ataques.png'))
            plt.close()

        if 'Country' in df.columns:
            df['Country'].value_counts().head(5).plot(kind='pie', autopct='%1.1f%%', colors=plt.cm.Paired.colors)
            plt.title('Distribuição de Ataques por País')
            plt.ylabel('')
            plt.tight_layout()
            plt.savefig(os.path.join(base_dir, 'distribuicao_paises.png'))
            plt.close()

        # 3. Construção do contexto para a IA
        stats_contexto = (
            f"Resumo da Análise de Dados:\n"
            f"- Volume Total de Alertas: {total_eventos}\n"
            f"- Top 3 Vetores de Ataque: {top_ataques}\n"
            f"- Top 3 Geocalizações de Origem: {paises_origem}\n"
        )

        prompt = (
            f"Com base nestas estatísticas:\n\n{stats_contexto}\n\n"
            "Crie um relatório executivo em Markdown detalhando o panorama de ameaças e 3 ações prioritárias. "
            "IMPORTANTE: Você DEVE referenciar as imagens geradas: 'top_ataques.png' e 'distribuicao_paises.png' "
            "dentro das seções apropriadas do relatório utilizando a sintaxe de imagem do Markdown."
        )

        # 4. Geração do Relatório via API
        print("Solicitando geração de relatório estratégico ao Gemini...")
        response = model.generate_content(prompt)

        # 5. Salvamento do Relatório
        output_path = os.path.join(base_dir, "relatorio_executivo.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"\nRelatório gerado com sucesso em: {output_path}")

    except Exception as e:
        print(f"Erro durante o processamento: {e}")

if __name__ == "__main__":
    # Permite passar o caminho via linha de comando: python script.py dados.csv
    if len(sys.argv) > 1:
        gerar_relatorio(sys.argv[1])
    else:
        gerar_relatorio()