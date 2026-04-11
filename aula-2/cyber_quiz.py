import random


def mostrar_pergunta(numero, pergunta, opcoes):
    print(f"\nPergunta {numero}: {pergunta}")
    for indice, opcao in enumerate(opcoes, start=1):
        print(f"  {indice}. {opcao}")


def obter_resposta():
    while True:
        escolha = input("Escolha uma opção (1-3): ").strip()
        if escolha in {"1", "2", "3"}:
            return int(escolha)
        print("Entrada inválida. Digite 1, 2 ou 3.")


def main():
    perguntas = [
        {
            "pergunta": "O que é engenharia social?",
            "opcoes": [
                "Ato de invadir um software diretamente",
                "Manipular pessoas para obter informações",
                "Criar senhas fortes",
            ],
            "resposta": 2,
        },
        {
            "pergunta": "Qual é a melhor prática para senhas?",
            "opcoes": [
                "Usar a mesma senha em todos os sites",
                "Anotar a senha em um papel visível",
                "Criar senhas longas e únicas",
            ],
            "resposta": 3,
        },
        {
            "pergunta": "O que significa VPN?",
            "opcoes": [
                "Virtual Private Network",
                "Verified Private Network",
                "Virtual Public Network",
            ],
            "resposta": 1,
        },
        {
            "pergunta": "Qual ação ajuda a prevenir phishing?",
            "opcoes": [
                "Clicar em links de e-mails desconhecidos",
                "Verificar o remetente antes de abrir",
                "Compartilhar dados pessoais em redes sociais",
            ],
            "resposta": 2,
        },
        {
            "pergunta": "O que é malware?",
            "opcoes": [
                "Software malicioso que danifica sistemas",
                "Sistema de backup automático",
                "Rede segura para acesso remoto",
            ],
            "resposta": 1,
        },
    ]

    random.shuffle(perguntas)

    pontos = 0
    print("=== Quiz de Cybersegurança ===")
    for idx, item in enumerate(perguntas, start=1):
        mostrar_pergunta(idx, item["pergunta"], item["opcoes"])
        resposta = obter_resposta()
        if resposta == item["resposta"]:
            pontos += 1
            print("Correto!")
        else:
            resposta_certa = item["opcoes"][item["resposta"] - 1]
            print(f"Errado. A resposta certa era: {item['resposta']} - {resposta_certa}")

    print(f"\nSua pontuação final: {pontos} de {len(perguntas)}")
    if pontos >= 3:
        print("Parabéns! Você passou no quiz.")
    else:
        print("Você não passou. Estude mais sobre cybersegurança.")


if __name__ == "__main__":
    main()
