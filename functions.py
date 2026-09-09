import random
import datetime
import os


# limpar terminal
def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def validar_cpf(cpf: str) -> bool:
    # Remove pontos e hífen
    cpf = cpf.replace(".", "").replace("-", "")

    if len(cpf) != 11 or not cpf.isdigit():
        return False

    # Rejeita CPFs com todos os dígitos iguais
    if cpf == cpf[0] * 11:
        return False

    soma = 0

    for i in range(9):
        soma += int(cpf[i]) * (10 - i)

    resto = soma % 11

    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto

    if int(cpf[9]) != digito1:
        return False

    soma = 0

    for i in range(10):
        soma += int(cpf[i]) * (11 - i)

    resto = soma % 11

    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto

    if int(cpf[10]) != digito2:
        return False

    return True

# criar conta
def create_account(d: dict) -> None:
    name = input("Insira seu nome: ")
    while len(name) < 3 or not name.replace(" ", "").isalpha():
        name = input("Insira seu nome: ")
    create_user = input("CPF (xxx.xxx.xxx-xx): ")

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
        or not validar_cpf(create_user)
    ):
        print("ERRO! CPF inválido. Use um CPF válido no formato xxx.xxx.xxx-xx")
        create_user = input("CPF (xxx.xxx.xxx-xx): ")

    if create_user in d:
        print("CPF já cadastrado!")
        return

    create_password = input("Crie uma senha: ").strip()

    while len(create_password) < 6:
        print("ERRO! Senha precisa ter pelo menos 6 caracteres.")
        create_password = input("Crie uma senha: ").strip()

    balance = 0

    d[create_user] = {
        "name": name,
        "password": create_password,
        "points_balance": balance,
        "money_balance": 0
    }

    print("Conta criada com sucesso!")

# login
def login(d: dict) -> tuple[bool, str]:
    login_cpf = input("CPF (xxx.xxx.xxx-xx): ")
    
    while (
        len(login_cpf) != 14
        or login_cpf[3] != "."
        or login_cpf[7] != "."
        or login_cpf[11] != "-"
        or not (
            login_cpf[:3].isdigit()
            and login_cpf[4:7].isdigit()
            and login_cpf[8:11].isdigit()
            and login_cpf[12:].isdigit()
            )
        or not validar_cpf(login_cpf)
        ):
            print("ERRO! CPF inválido. Use um CPF válido no formato xxx.xxx.xxx-xx")
            login_cpf = input("CPF (xxx.xxx.xxx-xx): ")

    if login_cpf in d:
        attempts = 0

        while attempts < 3:
            login_password = input("Digite sua senha: ").strip()

            if (login_password == d[login_cpf]["password"]):
                print("Login realizado com sucesso!")

                print(f"Bem vindo {d[login_cpf]['name']}, seu saldo é de {d[login_cpf]['points_balance']} pontos.")

                return True, login_cpf

            attempts += 1

            print(f"Senha incorreta! Tentativas restantes: {3 - attempts}")

        print("Acesso bloqueado!")

    else:
        print("CPF não encontrado!")

    return False, None

# converter pontos
def convert_points(d: dict, current_user: str) -> None:

    print(f"Seu saldo é de {d[current_user]['points_balance']} pontos.")
    
    try:
        points_to_convert = float(input("Quantos pontos deseja converter: "))

        if 0 < points_to_convert <= d[current_user]["points_balance"]:

            confirm = input(f"Tem certeza que deseja converter {points_to_convert} pontos em R${(points_to_convert/10):.2f}? (sim/não): ").strip().lower()

            match confirm:
                case "sim" | "ss" | "s":
                    d[current_user]["points_balance"] -= points_to_convert

                    money = points_to_convert / 10

                    d[current_user]["money_balance"] += money

                    print(f"Novo saldo de pontos: {d[current_user]['points_balance']}")
                    print(f"Saldo em reais: R${d[current_user]['money_balance']:.2f}")

                case "nao" | "não" | "nn" | "n":
                    print("Conversão cancelada.")

                case _:
                    print("Apenas sim ou não.")

        else:
            print("Saldo insuficiente!")
    except ValueError:
        print("Somente números")


# sacar dinheiro
def withdraw_money(d: dict, current_user: str) -> None:

    money_balance = d[current_user]["money_balance"]

    print(f"Você possui R${money_balance:.2f}")
    
    try:
        withdrawal = float(input("Quanto deseja sacar: "))

        if 0 < withdrawal <= money_balance:

            confirm = input(f"Tem certeza que deseja sacar R${withdrawal:.2f}? (sim/não): ").strip().lower()

            match confirm:
                case "sim" | "ss" | "s":
                    d[current_user]["money_balance"] -= withdrawal

                    print(f"Saque de R${withdrawal:.2f} será realizado em até 48 horas.")
                    print(f"Novo saldo: R${d[current_user]['money_balance']:.2f}")

                case "nao" | "não" | "nn" | "n":
                    print("Saque cancelado.")

                case _:
                    print("Apenas sim ou não.")

        else:
            print("Saldo insuficiente!")
    except ValueError:
        print("Somente números")


# logout
def logout() -> tuple[bool, None]:

    print("\nDeseja fazer Logout?")

    confirmation = input("Sim ou Nao: ").strip().lower()

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
def delete_account(d: dict, current_user: str | None) -> tuple[bool, str | None]:

    if current_user is None:
        print("Nenhum usuário logado!")
        return False, None

    confirmation = input("Tem certeza que deseja excluir sua conta? (Sim/Nao): ").strip().lower()

    match confirmation:
        case "sim" | "ss" | "s":

            password_confirmation = input("Digite sua senha para confirmar: ")

            if password_confirmation == d[current_user]["password"]:
                del d[current_user]

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

#Assistir videos para ganhar pontos
def watch_videos(d: dict, current_user: str) -> None:
    watched_videos = 0

    while True:
        hour = datetime.datetime.now().strftime("%H:%M")

        print(f"""
    ┌─────────────────────┐
    │       {hour}         │
    │                     │
    │     -SOUL UP-       │
    │                     |
    |                     |
    |                     |
    │                     |
    │   1-Assistir Video  │
    │                     |
    |                     |
    |                     |
    │                     |
    │       2-Sair        │
    │                     |
    |                     |
    └─────────────────────┘
    """)

        try:
            watch = int(input("Escolha uma opção: "))

            match watch:

                case 1:
                    video_time = random.randint(10, 120)

                    watched_videos += 1
                    d[current_user]["points_balance"] += video_time

                    print(f"Vídeo assistido: {video_time}s")
                    print(f"Você ganhou {video_time} pontos!")
                    print(f"Saldo: {d[current_user]['points_balance']} pontos")

                case 2:
                    print(f"Você assistiu {watched_videos} videos")
                    print("Saindo . . .")
                    break

                case _:
                    print("Somente 1 ou 2.")
            
            input("Pressiona ENTER para continuar . . .")

        except ValueError:
            print("Somente numeros.")