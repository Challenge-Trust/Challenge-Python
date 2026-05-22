import os
import random


# limpar terminal
def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


# criar conta
def create_account(users: dict) -> None:
    name: str = input("Insira seu nome: ")
    create_user: str = input("CPF (xxx.xxx.xxx-xx): ")

    # validar CPF
    while (
        len(create_user) != 14
        or create_user[3] != "."
        or create_user[7] != "."
        or create_user[11] != "-"
        or not (
            create_user[:3].isdigit()
            and create_user[4:7].isdigit()
            and create_user[8:11].isdigit()
            and create_user[12:].isdigit()
        )
    ):
        print("ERRO! CPF inválido. Use o formato xxx.xxx.xxx-xx")
        create_user = input("CPF (xxx.xxx.xxx-xx): ")

    if create_user in users:
        print("CPF já cadastrado!")
        return

    create_password: str = input("Crie uma senha: ")

    while len(create_password) < 6:
        print("ERRO! Senha precisa ter pelo menos 6 caracteres.")
        create_password = input("Crie uma senha: ")

    balance: int = random.randint(50, 1000)

    users[create_user] = {
        "name": name,
        "password": create_password,
        "points_balance": balance,
        "money_balance": 0
    }

    print("Conta criada com sucesso!")

# login
def login(users: dict) -> tuple[bool, str]:
    login_cpf: str = input("Digite seu CPF: ")

    if login_cpf in users:
        attempts: int = 0

        while attempts < 3:
            login_password: str = input("Digite sua senha: ").strip()

            if (login_password == users[login_cpf]["password"]):
                print("Login realizado com sucesso!")

                print(f"Bem vindo {users[login_cpf]['name']}, seu saldo é de {users[login_cpf]['points_balance']} pontos.")

                return True, login_cpf

            attempts += 1

            print(f"Senha incorreta! Tentativas restantes: {3 - attempts}")

        print("Acesso bloqueado!")

    else:
        print("CPF não encontrado!")

    return False, None

# converter pontos
def convert_points(users: dict, current_user: str) -> None:

    print(f"Seu saldo é de {users[current_user]['points_balance']} pontos.")
    
    points_to_convert: float = float(input("Quantos pontos deseja converter: "))

    if points_to_convert <= users[current_user]["points_balance"]:

        confirm: str = input(f"Tem certeza que deseja converter {points_to_convert} pontos em R${(points_to_convert/10):.2f}? (sim/não): ").strip().lower()

        match confirm:
            case "sim" | "ss" | "s":
                users[current_user]["points_balance"] -= points_to_convert

                money: float = points_to_convert / 10

                users[current_user]["money_balance"] += money

                print(f"Novo saldo de pontos: {users[current_user]['points_balance']}")
                print(f"Saldo em reais: R${users[current_user]['money_balance']:.2f}")

            case "nao" | "não" | "nn" | "n":
                print("Conversão cancelada.")

            case _:
                print("Apenas sim ou não.")

    else:
        print("Saldo insuficiente!")


# sacar dinheiro
def withdraw_money(users: dict, current_user: str) -> None:

    money_balance: float = users[current_user]["money_balance"]

    print(f"Você possui R${money_balance:.2f}")

    withdrawal: float = float(input("Quanto deseja sacar: "))

    if withdrawal <= money_balance:

        confirm: str = input(f"Tem certeza que deseja sacar R${withdrawal:.2f}? (sim/não): ").strip().lower()

        match confirm:
            case "sim" | "ss" | "s":
                users[current_user]["money_balance"] -= withdrawal

                print(f"Saque de R${withdrawal:.2f} será realizado em até 48 horas.")
                print(f"Novo saldo: R${users[current_user]['money_balance']:.2f}")

            case "nao" | "não" | "nn" | "n":
                print("Saque cancelado.")

            case _:
                print("Apenas sim ou não.")

    else:
        print("Saldo insuficiente!")


# logout
def logout() -> tuple[bool, None]:

    print("\nDeseja fazer Logout?")

    confirmation: str = input("Sim ou Nao: ").strip().lower()

    match confirmation:
        case "sim" | "ss" | "s":
            print("Logout realizado com sucesso!")
            return False, None

        case "nao" | "não" | "nn" | "n":
            print("Logout cancelado.")
            return True, None

        case _:
            print("Apenas sim ou nao.")
            return True, None


# excluir conta
def delete_account(users: dict, current_user: str | None) -> tuple[bool, str | None]:

    if current_user is None:
        print("Nenhum usuário logado!")
        return False, None

    confirmation: str = input(
        "Tem certeza que deseja excluir sua conta? (Sim/Nao): "
    ).strip().lower()

    match confirmation:
        case "sim" | "ss" | "s":

            password_confirmation: str = input("Digite sua senha para confirmar: ")

            if password_confirmation == users[current_user]["password"]:
                del users[current_user]

                print("Conta excluída com sucesso!")

                return False, None

            print("Senha incorreta!")
            return True, current_user

        case "nao" | "não" | "nn" | "n":
            print("Exclusão cancelada.")
            return True, current_user

        case _:
            print("Apenas sim ou nao.")
            return True, current_user