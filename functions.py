import os
import random


# limpar terminal
def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


# criar conta
def create_account(users: dict) -> None:
    name: str = input("Insira seu nome: ")
    create_user: str = input("CPF (xxx.xxx.xxx-xx): ")

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
            login_password: str = input(
                "Digite sua senha: "
            ).strip()

            if (
                login_password
                == users[login_cpf]["password"]
            ):
                print("Login realizado com sucesso!")

                print(
                    f"Bem vindo "
                    f"{users[login_cpf]['name']}, "
                    f"seu saldo é de "
                    f"{users[login_cpf]['points_balance']} "
                    f"pontos."
                )

                return True, login_cpf

            attempts += 1

            print(
                f"Senha incorreta! "
                f"Tentativas restantes: "
                f"{3 - attempts}"
            )

        print("Acesso bloqueado!")

    else:
        print("CPF não encontrado!")

    return False, None


# converter pontos
def convert_points(
    users: dict,
    current_user: str
) -> None:

    points_to_convert: float = float(
        input("Quantos pontos deseja converter: ")
    )

    if (
        points_to_convert
        <= users[current_user]["points_balance"]
    ):
        users[current_user][
            "points_balance"
        ] -= points_to_convert

        money: float = points_to_convert / 10

        users[current_user][
            "money_balance"
        ] += money

        print(
            f"Novo saldo de pontos: "
            f"{users[current_user]['points_balance']}"
        )

        print(
            f"Saldo em reais: "
            f"R$"
            f"{users[current_user]['money_balance']:.2f}"
        )

    else:
        print("Saldo insuficiente!")


# sacar dinheiro
def withdraw_money(
    users: dict,
    current_user: str
) -> None:

    money_balance: float = users[
        current_user
    ]["money_balance"]

    print(f"Você possui R${money_balance:.2f}")

    withdrawal: float = float(
        input("Quanto deseja sacar: ")
    )

    if withdrawal <= money_balance:
        users[current_user][
            "money_balance"
        ] -= withdrawal

        print(
            f"Saque de "
            f"R${withdrawal:.2f} "
            f"será realizado "
            f"em até 48 horas."
        )

        print(
            f"Novo saldo: "
            f"R$"
            f"{users[current_user]['money_balance']:.2f}"
        )

    else:
        print("Saldo insuficiente!")


# logout
def logout() -> tuple[bool]:
    print("\nDeseja fazer Logout?")

    confirmation: str = input(
        "Sim ou Nao: "
    ).lower()

    if confirmation == "sim":
        print("Logout realizado com sucesso!")
        return False, None

    return True, None


# excluir conta
def delete_account(
    users: dict,
    current_user: str
) -> tuple[bool, str]:

    confirmation: str = input(
        "Tem certeza que deseja excluir "
        "sua conta? (sim/nao): "
    ).lower()

    if confirmation == "sim":

        password_confirmation: str = input(
            "Digite sua senha para confirmar: "
        )

        if (
            password_confirmation
            == users[current_user]["password"]
        ):
            del users[current_user]

            print(
                "Conta excluída com sucesso!"
            )

            return False, None

        print("Senha incorreta!")

    else:
        print("Exclusão cancelada.")

    return True, current_user