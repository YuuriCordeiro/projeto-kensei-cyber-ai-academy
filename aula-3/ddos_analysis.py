import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Caminho do arquivo
BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / 'cybersecurity_attacks_cleaned.csv'

def analyze_ddos_attacks():
    # Carregar o dataset
    df = pd.read_csv(FILE_PATH)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # --- GRÁFICO 1: Top 10 Países (DDoS no último mês) ---
    ddos_df = df[df['Attack Type'] == 'DDoS'].copy()
    if not ddos_df.empty:
        max_date = ddos_df['Timestamp'].max()
        start_date = max_date - pd.DateOffset(months=1)
        last_month_df = ddos_df[ddos_df['Timestamp'] >= start_date].copy()
        last_month_df['Country'] = last_month_df['Geo-location Data'].str.split(',').str[-1].str.strip()
        top_10_countries = last_month_df['Country'].value_counts().head(10)

        plt.figure(figsize=(10, 6))
        top_10_countries.plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title(f'Top 10 Países com mais DDoS\n({start_date.date()} a {max_date.date()})')
        plt.xlabel('País/Região')
        plt.ylabel('Quantidade de Ataques')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(BASE_DIR / 'top_10_paises_ddos.png')
        plt.close()

    # --- GRÁFICO 2: Ataques por Mês (Linha) ---
    # Agrupando por mês (usando a frequência 'ME' para Month End)
    monthly_attacks = df.resample('ME', on='Timestamp').size()
    
    plt.figure(figsize=(10, 5))
    monthly_attacks.plot(kind='line', marker='o', color='firebrick', linewidth=2)
    plt.title('Tendência Temporal de Ataques Totais')
    plt.xlabel('Mês')
    plt.ylabel('Total de Ocorrências')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(BASE_DIR / 'ataques_por_mes.png')
    plt.close()

    # --- GRÁFICO 3: Tipos de Ataque (Pizza) ---
    attack_counts = df['Attack Type'].value_counts()
    
    plt.figure(figsize=(8, 8))
    attack_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title('Distribuição Global por Tipo de Ataque')
    plt.ylabel('')  # Remove o label do eixo Y que o pandas coloca por padrão
    plt.tight_layout()
    plt.savefig(BASE_DIR / 'tipos_ataque_distribuicao.png')
    plt.close()

    print(f"Análise concluída!")
    print(f"Gráficos salvos em: {BASE_DIR}")
    print("- top_10_paises_ddos.png\n- ataques_por_mes.png\n- tipos_ataque_distribuicao.png")

if __name__ == "__main__":
    analyze_ddos_attacks()