import json
import os

ARQUIVO_LISTA = "lista_de_compras.json"


def carregar_lista():
    if not os.path.isfile(ARQUIVO_LISTA):
        return []
    try:
        with open(ARQUIVO_LISTA, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (json.JSONDecodeError, IOError):
        print("Aviso: não foi possível carregar a lista. Iniciando lista vazia.")
        return []


def salvar_lista(lista):
    try:
        with open(ARQUIVO_LISTA, "w", encoding="utf-8") as arquivo:
            json.dump(lista, arquivo, ensure_ascii=False, indent=2)
    except IOError:
        print("Erro ao salvar a lista de compras.")


def mostrar_menu():
    print("\n=== Lista de Compras ===")
    print("1. Adicionar item")
    print("2. Ver itens")
    print("3. Remover item")
    print("4. Sair")


def adicionar_item(lista):
    item = input("Digite o item para adicionar: ").strip()
    if item:
        lista.append(item)
        salvar_lista(lista)
        print(f"Item '{item}' adicionado à lista.")
    else:
        print("Nenhum item inserido. Tente novamente.")


def ver_itens(lista):
    if not lista:
        print("A lista de compras está vazia.")
        return
    print("\nItens na lista de compras:")
    for indice, item in enumerate(lista, start=1):
        print(f"{indice}. {item}")


def remover_item(lista):
    if not lista:
        print("A lista de compras está vazia. Nada a remover.")
        return
    ver_itens(lista)
    try:
        escolha = int(input("Digite o número do item a remover: "))
        if 1 <= escolha <= len(lista):
            item_removido = lista.pop(escolha - 1)
            salvar_lista(lista)
            print(f"Item '{item_removido}' removido da lista.")
        else:
            print("Número inválido. Tente novamente.")
    except ValueError:
        print("Entrada inválida. Digite um número válido.")


def main():
    lista_de_compras = carregar_lista()
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            adicionar_item(lista_de_compras)
        elif opcao == "2":
            ver_itens(lista_de_compras)
        elif opcao == "3":
            remover_item(lista_de_compras)
        elif opcao == "4":
            print("Saindo... Até logo!")
            break
        else:
            print("Opção inválida. Digite 1, 2, 3 ou 4.")


if __name__ == "__main__":
    main()
