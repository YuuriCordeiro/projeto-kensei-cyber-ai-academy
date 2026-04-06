import random
import string


def pedir_sim_ou_nao(pergunta):
    while True:
        resposta = input(f"{pergunta} (s/n): ").strip().lower()
        if resposta in {"s", "n"}:
            return resposta == "s"
        print("Resposta inválida. Digite 's' para sim ou 'n' para não.")


def pedir_tamanho():
    while True:
        valor = input("Digite o tamanho da senha (mínimo 4): ").strip()
        if not valor.isdigit():
            print("Digite um número válido.")
            continue
        tamanho = int(valor)
        if tamanho < 4:
            print("O tamanho deve ser pelo menos 4.")
            continue
        return tamanho


def gerar_senha(tamanho, usar_maiusculas, usar_numeros, usar_simbolos):
    letras_minusculas = list(string.ascii_lowercase)
    letras_maiusculas = list(string.ascii_uppercase) if usar_maiusculas else []
    digitos = list(string.digits) if usar_numeros else []
    simbolos = list("!@#$%^&*()-_=+[]{};:,.<>?/") if usar_simbolos else []

    caracteres = letras_minusculas + letras_maiusculas + digitos + simbolos

    if not caracteres:
        raise ValueError("Nenhum conjunto de caracteres selecionado.")

    requeridos = [random.choice(letras_minusculas)]
    if usar_maiusculas:
        requeridos.append(random.choice(letras_maiusculas))
    if usar_numeros:
        requeridos.append(random.choice(digitos))
    if usar_simbolos:
        requeridos.append(random.choice(simbolos))

    if len(requeridos) > tamanho:
        raise ValueError("Tamanho insuficiente para incluir todos os tipos selecionados.")

    restante = [random.choice(caracteres) for _ in range(tamanho - len(requeridos))]
    senha_lista = requeridos + restante
    random.shuffle(senha_lista)
    return "".join(senha_lista)


def main():
    print("=== Gerador de Senhas ===")
    tamanho = pedir_tamanho()
    usar_maiusculas = pedir_sim_ou_nao("Incluir letras maiúsculas?")
    usar_numeros = pedir_sim_ou_nao("Incluir números?")
    usar_simbolos = pedir_sim_ou_nao("Incluir símbolos?")

    try:
        senha = gerar_senha(tamanho, usar_maiusculas, usar_numeros, usar_simbolos)
        print(f"\nSenha gerada: {senha}")
    except ValueError as erro:
        print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
