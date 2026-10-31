import random
import datetime
import os
import json
import requests
import oracledb

RATE_API_URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
USER = "RM570451"
PASSWORD = "171207"
DSN = "oracle.fiap.com.br:1521/ORCL"
DB_TABLE = "soulup"
JSON_FILE = "accounts.json"


def clear_screen()->None:
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

# conexão com o banco Oracle
def connect_db() -> oracledb.Connection:
    return oracledb.connect(
        user = USER,
        password = PASSWORD,
        dsn = DSN
    )

# executa INSERT / UPDATE / DELETE com commit. Retorna True se deu certo
def execute_db(sql: str, params: list) -> bool:
    try:
        conn = connect_db()
    except oracledb.DatabaseError as erro:
        print("ERRO! Não foi possível conectar ao banco: ", erro)
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return True
    except oracledb.IntegrityError:
        conn.rollback()
        print("CPF já cadastrado!")
        return False
    except oracledb.DatabaseError as erro:
        conn.rollback()
        print("ERRO! Falha ao acessar o banco: ", erro)
        return False
    finally:
        conn.close()

# tabela -> dicionário (mesmo formato usado no programa)
def tabela_para_dict() -> dict:
    conn = connect_db()

    try:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT CPF, NOME, SENHA, SALDO_PONTOS, SALDO_REAIS FROM {DB_TABLE} ORDER BY CPF"
        )

        contas = {}

        for cpf, nome, senha, pontos, reais in cursor:
            pontos = float(pontos)

            contas[cpf] = {
                "name": nome,
                "password": senha,
                "points_balance": pontos,
                "money_balance": float(reais)
            }

        return contas

    finally:
        conn.close()

# tabela -> json    (gera o arquivo accounts.json a partir do banco)
def tabela_para_json() -> None:
    try:
        contas = tabela_para_dict()

        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(contas, file, ensure_ascii=False, indent=4)

    except oracledb.DatabaseError as erro:
        print("ERRO! Não foi possível ler o banco: ", erro)
    except OSError:
        print("ERRO! Não foi possível salvar o arquivo JSON.")

# carregar contas (banco; se falhar, usa o arquivo json)
def load_accounts() -> dict:
    try:
        return tabela_para_dict()
    except oracledb.DatabaseError as erro:
        print("Aviso: não foi possível ler o banco: ", erro)

    if not os.path.exists(JSON_FILE):
        return {}
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print(f"Aviso: não foi possível ler {JSON_FILE}. Iniciando vazio.")
        return {}

# salvar contas no arquivo json (sempre a partir do banco)
def save_accounts(d: dict = None) -> None:
    tabela_para_json()

# cotação dólar (API pública AwesomeAPI) -> retorna quantos reais vale 1 dólar
def get_usd_rate() -> float | None:
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

    cabecalho = {
        "Accept": "application/json"
    }

    try:
        resposta = requests.get(url, headers=cabecalho, timeout=5)
    except requests.exceptions.RequestException:
        print("Falha de conexão com a API de cotação.")
        return None

    print(f"Status: {resposta.status_code}")

    if resposta.status_code == 200:
        dados = resposta.json()
        return float(dados["USDBRL"]["bid"])

    print("Falha")
    return None

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

    # grava no banco primeiro
    cadastro = f"""
        INSERT INTO {DB_TABLE} (CPF, NOME, SENHA, SALDO_PONTOS, SALDO_REAIS)
        VALUES (:1, :2, :3, :4, :5)
    """

    if not execute_db(cadastro, [create_user, name, create_password, balance, 0]):
        return

    d[create_user] = {
        "name": name,
        "password": create_password,
        "points_balance": balance,
        "money_balance": 0
    }

    tabela_para_json()

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
                    money = points_to_convert / 10

                    new_points = round(d[current_user]["points_balance"] - points_to_convert, 2)
                    new_money = round(d[current_user]["money_balance"] + money, 2)

                    # atualiza o banco primeiro
                    atualizar = f"""
                        UPDATE {DB_TABLE}
                        SET SALDO_PONTOS = :1, SALDO_REAIS = :2
                        WHERE CPF = :3
                    """

                    if not execute_db(atualizar, [new_points, new_money, current_user]):
                        print("Conversão não realizada.")
                        return

                    d[current_user]["points_balance"] = new_points
                    d[current_user]["money_balance"] = new_money

                    tabela_para_json()

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
        withdrawal = float(input("Quanto deseja sacar (em R$): "))

        if not 0 < withdrawal <= money_balance:
            print("Saldo insuficiente!")
            return

        print("Sacar em:\n1 - Reais\n2 - Dólar")
        currency = input("Opção: ").strip()

        rate = None
        if currency == "1":
            message = f"R${withdrawal:.2f}"
        elif currency == "2":
            rate = get_usd_rate()
            if rate is None:
                print("Não foi possível obter a cotação do dólar. Tente novamente mais tarde.")
                return
            print(f"Cotação atual: US$1 = R${rate:.4f}")
            message = f"US${withdrawal / rate:.2f} (R${withdrawal:.2f})"
        else:
            print("Opção inválida!")
            return

        confirm = input(f"Tem certeza que deseja sacar {message}? (sim/não): ").strip().lower()

        match confirm:
            case "sim" | "ss" | "s":
                new_money = round(money_balance - withdrawal, 2)

                # atualiza o banco primeiro
                atualizar = f"""
                    UPDATE {DB_TABLE}
                    SET SALDO_REAIS = :1
                    WHERE CPF = :2
                """

                if not execute_db(atualizar, [new_money, current_user]):
                    print("Saque não realizado.")
                    return

                d[current_user]["money_balance"] = new_money

                tabela_para_json()

                print(f"Saque de {message} será realizado em até 48 horas.")
                print(f"Novo saldo: R${d[current_user]['money_balance']:.2f}")

            case "nao" | "não" | "nn" | "n":
                print("Saque cancelado.")

            case _:
                print("Apenas sim ou não.")

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
                # exclui do banco primeiro
                excluir = f"DELETE FROM {DB_TABLE} WHERE CPF = :1"

                if not execute_db(excluir, [current_user]):
                    print("Conta não excluída.")
                    return True, current_user

                del d[current_user]

                tabela_para_json()

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

                    new_points = d[current_user]["points_balance"] + video_time

                    # atualiza o banco primeiro
                    atualizar = f"""
                        UPDATE {DB_TABLE}
                        SET SALDO_PONTOS = :1
                        WHERE CPF = :2
                    """

                    if execute_db(atualizar, [new_points, current_user]):
                        watched_videos += 1
                        d[current_user]["points_balance"] = new_points

                        tabela_para_json()

                        print(f"Vídeo assistido: {video_time}s")
                        print(f"Você ganhou {video_time} pontos!")
                        print(f"Saldo: {d[current_user]['points_balance']} pontos")
                    else:
                        print("Não foi possível salvar os pontos.")

                case 2:
                    print(f"Você assistiu {watched_videos} videos")
                    print("Saindo . . .")
                    break

                case _:
                    print("Somente 1 ou 2.")
            
            input("Pressiona ENTER para continuar . . .")

        except ValueError:
            print("Somente numeros.")