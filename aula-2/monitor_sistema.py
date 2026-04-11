import os
import time

try:
    import psutil
except ImportError:
    print("Erro: a biblioteca 'psutil' não está instalada.")
    print("Instale com: pip install psutil")
    raise


def limpar_tela():
    comando = "cls" if os.name == "nt" else "clear"
    os.system(comando)


def mostrar_status():
    cpu_percent = psutil.cpu_percent(interval=1)
    memoria = psutil.virtual_memory()
    uso_memoria = memoria.percent
    total = memoria.total / (1024 ** 3)
    usado = memoria.used / (1024 ** 3)

    print("=== Monitor de Sistema ===")
    print(f"Uso de CPU: {cpu_percent:.1f}%")
    if cpu_percent > 80:
        print("ALERTA: Uso de CPU acima de 80%!")
    print(f"Uso de memória: {uso_memoria:.1f}%")
    print(f"Memória total: {total:.2f} GB")
    print(f"Memória usada: {usado:.2f} GB")
    print("Pressione Ctrl+C para sair.")


def main():
    try:
        while True:
            limpar_tela()
            mostrar_status()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nMonitoramento encerrado.")


if __name__ == "__main__":
    main()
