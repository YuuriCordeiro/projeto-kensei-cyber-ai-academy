def ler_numero(prompt):
    while True:
        valor = input(prompt).strip()
        try:
            return float(valor)
        except ValueError:
            print("Entrada inválida. Digite um número válido.")


def converter_celsius_para_fahrenheit(celsius):
    return (celsius * 9/5) + 32


def converter_fahrenheit_para_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9


def main():
    print("=== Conversor de Temperatura ===")
    print("1. Celsius para Fahrenheit")
    print("2. Fahrenheit para Celsius")

    while True:
        opcao = input("Escolha uma opção (1 ou 2): ").strip()
        if opcao in {"1", "2"}:
            break
        print("Opção inválida. Digite 1 ou 2.")

    if opcao == "1":
        celsius = ler_numero("Digite a temperatura em Celsius: ")
        fahrenheit = converter_celsius_para_fahrenheit(celsius)
        print(f"{celsius:.2f}°C é igual a {fahrenheit:.2f}°F")
    else:
        fahrenheit = ler_numero("Digite a temperatura em Fahrenheit: ")
        celsius = converter_fahrenheit_para_celsius(fahrenheit)
        print(f"{fahrenheit:.2f}°F é igual a {celsius:.2f}°C")


if __name__ == "__main__":
    main()