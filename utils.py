import os


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def wait_for_user():
    input("Pressione Enter para continuar...")
