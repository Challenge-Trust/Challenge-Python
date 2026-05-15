from functions import *

clear_screen()

print("Bem Vindo ao Conversor de pontos")

# armazenar usuarios
users = {}

logged_in = False
current_user = None

while True:
    print("""
        Selecione a opção desejada:
        1 - Criar Conta
        2 - Fazer Login
        3 - Converter Pontos
        4 - Sacar Dinheiro
        5 - Fazer Logout
        6 - Excluir Conta
        7 - Sair
        """)

    try:
        option = int(input("Opção: "))

        # criar conta
        if option == 1:
            create_account(users)

        # login
        elif option == 2:
            logged_in, current_user = login(users)

        # converter pontos
        elif option == 3:
            if not logged_in:
                print("Você precisa fazer login primeiro!")
                continue

            convert_points(users, current_user)

        # sacar dinheiro
        elif option == 4:
            if not logged_in:
                print("Você precisa fazer login primeiro!")
                continue

            withdraw_money(users, current_user)

        # logout
        elif option == 5:
            if logged_in:
                logged_in, current_user = logout()
            else:
                print("Nenhum usuário logado!")

        # excluir conta
        elif option == 6:
            if not logged_in:
                print(
                    "Você precisa fazer login "
                    "para excluir a conta!"
                )
                continue

            logged_in, current_user = delete_account(
                users,
                current_user
            )

        # sair
        elif option == 7:
            if logged_in:
                print(
                    "Você precisa fazer logout "
                    "antes de sair!"
                )
            else:
                print("Encerrando...")
                break

        else:
            print("Opção inválida!")

    except ValueError:
        print("Somente numeros de 1 até 7")