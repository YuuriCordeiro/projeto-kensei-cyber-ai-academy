while True:
    nome = input("Digite seu nome: ").strip()
    if nome:
        break
    print("Nome inválido. Por favor, informe um nome não vazio.")

print("Olá, " + nome.upper())