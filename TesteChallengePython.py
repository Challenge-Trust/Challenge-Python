#saldo provisório
import random
saldo = random.randint(100, 1000)

#limpar o terminal tanto no windows, mac e linux
def clear_screen():
    import os
    os.system("cls" if os.name == "nt" else "clear")

clear_screen()

print("Bem Vindo ao Conversor de pontos")

# armazenar login e senha
cpf = []
senha = []

#poder selecionar mais de uma opcao, apos a outra
while True:
    print("""Selecione a opção desejada:
          1 - Criar Conta
          2 - Fazer Login
          3 - Realizar Transacao
          4 - Sacar Dinheiro
          5 - Sair""")

    opcao = int(input("Opção: "))

    #criar conta
    if opcao == 1:
        nome = input("insira seu nome: ")
        criar_usuario = input("CPF (xxx.xxx.xxx-xx): ")
        cpf.append(criar_usuario)

        criar_senha = input("Crie uma senha: ")
        while len(criar_senha) < 6:
            print("ERRO! Senha precisa ter pelo menos 6 caracteres.")
            criar_senha = input("Crie uma senha: ")

        senha.append(criar_senha)

    #fazer login
    elif opcao == 2:
        login_cpf = input("Digite seu CPF: ")
        login_senha = input("Digite sua senha: ")

        if login_cpf in cpf:
            indice = cpf.index(login_cpf)

            tentativas = 0
            while tentativas < 3:
                login_senha = input("Digite sua senha: ")

                if login_senha == senha[indice]:
                    print("Login realizado com sucesso!")
                    print(f"Bem vindo {nome}, seu saldo é de {saldo} pontos.")
                    break
                    
                else:
                    tentativas += 1
                    print(f"Senha incorreta! Tentativas restantes: {3 - tentativas}")

            if tentativas == 3:
                print("Acesso bloqueado! Muitas tentativas.")
        else:
            print("CPF não encontrado! Crie uma conta primeiro.")
    
    #conerter pontos
    elif opcao == 3:
        converter_pontos = float(input("Insira a quantidade de ponts a ser convertida: "))
        if converter_pontos <= saldo:
            saldo -= converter_pontos
            converter_pontos = converter_pontos / 10
            saldo_reais = converter_pontos
            print(f"O seu novo saldo de pontos é de {saldo}.")
            print(f"O seu saldo em reais é de R${saldo_reais:.2f}.")
        else:
            print("insira uma quantidade de pontos válida.")

    #sacar dinheiro
    elif opcao == 4:
        print(f"{nome}, voce possui R${saldo_reais:.2f}")
        saque = float(input("Quanto voce deseja sacar: "))
        if saque <= saldo_reais:
            print(f"O depósito de R${saldo_reais:.2f} será realizado em até 48 horas.")
            saldo_reais -= saque
            print(f"Seu novo saldo em reais é de R${saldo_reais:.2f}.")
        else:
            print("Insira um saldo válido.")

    #Fechar programar
    elif opcao == 5:
        print("Finalizando sistema.")
        break

    else:
        print("Opção inválida!")