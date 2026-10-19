from functions import *

clear_screen()

print("Bem Vindo ao Conversor de pontos")

# armazenar usuarios
user = load_accounts()


logged_in = False
current_user = None

while True:
    print("""
        Selecione a opção desejada:
        1 - Criar Conta
        2 - Fazer Login
        3 - Assistir Videos
        4 - Converter Pontos
        5 - Sacar Dinheiro
        6 - Fazer Logout
        7 - Excluir Conta
        0 - Sair
        """)

    #Se inserir letra nao quebra o cóigo
    try:
        option = int(input("Opção: "))
        match option:
            # criar conta
            case 1:
                if not logged_in:
                    create_account(user)
                else:
                    print("Você precisa fazer logout para criar uma conta.")

            # login
            case 2:
                if not logged_in:
                    logged_in, current_user = login(user)
                else:
                    print("Você já está logado.")

            case 3:
                if not logged_in:
                    print("Você precisa fazer login primeiro!")
                else:
                    watch_videos(user, current_user)

            # converter pontos
            case 4:
                if not logged_in:
                    print("Você precisa fazer login primeiro!")
                else:
                    convert_points(user, current_user)

            # sacar dinheiro
            case 5:
                if not logged_in:
                    print("Você precisa fazer login primeiro!")
                else:
                    withdraw_money(user, current_user)

            # logout
            case 6:
                if logged_in:
                    logged_in, current_user = logout()
                else:
                    print("Nenhum usuário logado!")

            # excluir conta
            case 7:
                if logged_in:
                    logged_in, current_user = delete_account(user, current_user)
                else:
                    print("Faça login primeiro!")

            # sair
            case 0:
                if logged_in:
                    print("Você precisa fazer logout antes de sair!")
                else:
                    print("Encerrando...")
                    break

            case _:
                print("Opção inválida!")

        save_accounts(user)

        input("Pressiona ENTER para continuar . . .")

    except ValueError:
        print("Somente numeros de 0 até 7.")