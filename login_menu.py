import globals
from utils import clear_console, wait_for_user


def login():
    clear_console()
    print("\nLogin de Usuário")
    email = str(input("\nDigite o seu e-mail: "))
    password = str(input("Digite a senha: "))

    if email in globals.registers and globals.registers[email].get('password') == password:
        print("\nLogin realizado com sucesso!")
        globals.passed_login = True
    else:
        print("\nE-mail ou senha incorretos! Tente novamente.")


def register():
    clear_console()
    print("\nCadastro de Usuário")
    name = input("\nDigite o seu nome completo: ")
    email = input("Digite o seu E-mail: ")
    password = input("Digite sua senha: ")

    confirmation_password = input("Confirme sua senha: ")
    while password != confirmation_password:
        print("\nSenha incorreta!\nDigite novamente")
        confirmation_password = input("\nConfirme sua senha: ")

    globals.registers[email] = {
        "name": name,
        "password": password
    }

    print("\nCadastro realizado com sucesso!")
    wait_for_user()
    login()


def login_menu():
    # Menu do Usuário
    print("\nBem vindo(a) ao Menu do Usuário!")
    print("\nSelecione uma das opções abaixo:")
    print("\n1 - Login\n2 - Cadastro")
    option = int(input("\nOpção: "))

    # Página de login
    if option == 1:
        login()
    # Página de cadastro
    elif option == 2:
        register()
    else:
        print("\nOpção inválida! Tente novamente.")

    wait_for_user()
    clear_console()
