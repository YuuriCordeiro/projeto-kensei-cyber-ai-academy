import os
import shutil

PASTAS = {
    "imagens": {"jpg", "jpeg", "png", "gif", "bmp", "svg", "webp"},
    "docs": {"pdf", "doc", "docx", "txt", "xls", "xlsx", "ppt", "pptx"},
    "videos": {"mp4", "mkv", "avi", "mov", "wmv", "flv"},
}


def criar_pasta_se_nao_existir(caminho):
    if not os.path.isdir(caminho):
        os.makedirs(caminho, exist_ok=True)


def classificar_extensao(extensao):
    ext = extensao.lower().lstrip('.')
    for pasta, extensoes in PASTAS.items():
        if ext in extensoes:
            return pasta
    return None


def organizar_arquivos(diretorio):
    criar_pasta_se_nao_existir(os.path.join(diretorio, "imagens"))
    criar_pasta_se_nao_existir(os.path.join(diretorio, "docs"))
    criar_pasta_se_nao_existir(os.path.join(diretorio, "videos"))

    resumo = {pasta: [] for pasta in PASTAS}

    for nome in os.listdir(diretorio):
        if nome.startswith('.'):
            continue

        caminho = os.path.join(diretorio, nome)
        if os.path.isfile(caminho):
            _, extensao = os.path.splitext(nome)
            pasta_destino = classificar_extensao(extensao)
            if pasta_destino:
                destino = os.path.join(diretorio, pasta_destino, nome)
                shutil.move(caminho, destino)
                resumo[pasta_destino].append(nome)
                print(f"Movendo '{nome}' para '{pasta_destino}/'")

    print("\nResumo dos arquivos movidos:")
    for pasta, arquivos in resumo.items():
        if arquivos:
            print(f"- {pasta}: {len(arquivos)} arquivo(s)")
            for arquivo in arquivos:
                print(f"  - {arquivo}")
        else:
            print(f"- {pasta}: 0 arquivos")


def main():
    diretorio = input("Digite o caminho do diretório a organizar (ou pressione Enter para usar o atual): ").strip()
    if not diretorio:
        diretorio = os.getcwd()

    if not os.path.isdir(diretorio):
        print("O caminho não é um diretório válido.")
        return

    organizar_arquivos(diretorio)
    print("Organização concluída.")


if __name__ == "__main__":
    main()
