import schedule
import time
import os
from executive_report_gen import gerar_relatorio

# Configurações: Altere o caminho e o horário conforme necessário
ARQUIVO_DADOS = os.path.join("..", "aula-3", "cybersecurity_attacks_cleaned.csv")
HORARIO_EXECUCAO = "09:00"

def job():
    print(f"[{time.strftime('%H:%M:%S')}] Iniciando automação diária...")
    if os.path.exists(ARQUIVO_DADOS):
        gerar_relatorio(ARQUIVO_DADOS)
    else:
        print(f"Erro: Base de dados não encontrada em {ARQUIVO_DADOS}")

# Agenda para rodar todo dia no horário definido
schedule.every().day.at(HORARIO_EXECUCAO).do(job)

print(f"Serviço de agendamento iniciado. Relatório será gerado todos os dias às {HORARIO_EXECUCAO}.")
print("Mantenha este terminal aberto para a execução automática. Pressione Ctrl+C para encerrar.")

while True:
    schedule.run_pending()
    time.sleep(60) # Verifica a cada minuto