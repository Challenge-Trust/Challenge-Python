
#limpar o terminal tanto no windows, mac e linux
def clear_screen():
    import os
    os.system("cls" if os.name == "nt" else "clear")

clear_screen()

import random

print("Bem Vindo ao Conversor de pontos")

# Armazenar usuarios
usuarios = {}

logado = False
usuario_atual = None

while True:
    print("""\nSelecione a opção desejada:
    1 - Criar Conta
    2 - Fazer Login
    3 - Realizar Transacao
    4 - Sacar Dinheiro
    5 - Sair""")

    opcao = int(input("Opção: "))

    # CRIAR CONTA
    if opcao == 1:
        nome = input("Insira seu nome: ")
        criar_usuario = input("CPF (xxx.xxx.xxx-xx): ")

        if criar_usuario in usuarios:
            print("CPF já cadastrado!")
            continue

        criar_senha = input("Crie uma senha: ")
        while len(criar_senha) < 6:
            print("ERRO! Senha precisa ter pelo menos 6 caracteres.")
            criar_senha = input("Crie uma senha: ")

        saldo = random.randint(50, 1000)

        usuarios[criar_usuario] = {
            "nome": nome,
            "senha": criar_senha,
            "saldo": saldo,
            "saldo_reais": 0
        }

        print("Conta criada com sucesso!")

    # LOGIN
    elif opcao == 2:
        login_cpf = input("Digite seu CPF: ")

        if login_cpf in usuarios:
            tentativas = 0

            while tentativas < 3:
                login_senha = input("Digite sua senha: ").strip()

                if login_senha == usuarios[login_cpf]["senha"]:
                    print("Login realizado com sucesso!")
                    logado = True
                    usuario_atual = login_cpf

                    print(f"Bem vindo {usuarios[login_cpf]['nome']}, seu saldo é de {usuarios[login_cpf]['saldo']} pontos.")
                    break
                else:
                    tentativas += 1
                    print(f"Senha incorreta! Tentativas restantes: {3 - tentativas}")

            if tentativas == 3:
                print("Acesso bloqueado!")
        else:
            print("CPF não encontrado!")

    # CONVERTER PONTOS
    elif opcao == 3:
        if not logado:
            print("Você precisa fazer login primeiro!")
            continue

        converter_pontos = float(input("Quantos pontos deseja converter: "))

        if converter_pontos <= usuarios[usuario_atual]["saldo"]:
            usuarios[usuario_atual]["saldo"] -= converter_pontos
            reais = converter_pontos / 10
            usuarios[usuario_atual]["saldo_reais"] += reais

            print(f"Novo saldo de pontos: {usuarios[usuario_atual]['saldo']}")
            print(f"Saldo em reais: R${usuarios[usuario_atual]['saldo_reais']:.2f}")
        else:
            print("Saldo insuficiente!")

    # SACAR DINHEIRO
    elif opcao == 4:
        if not logado:
            print("Você precisa fazer login primeiro!")
            continue

        saldo_reais = usuarios[usuario_atual]["saldo_reais"]

        print(f"Você possui R${saldo_reais:.2f}")
        saque = float(input("Quanto deseja sacar: "))

        if saque <= saldo_reais:
            usuarios[usuario_atual]["saldo_reais"] -= saque
            print(f"Saque de R${saque:.2f} será realizado em até 48 horas.")
            print(f"Novo saldo: R${usuarios[usuario_atual]['saldo_reais']:.2f}")
        else:
            print("Saldo insuficiente!")

    # SAIR
    elif opcao == 5:
        print("Finalizando sistema.")
        break

    else:
        print("Opção inválida!")