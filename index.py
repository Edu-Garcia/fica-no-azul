import globals
from login_menu import login_menu
from user_menu import user_menu
from utils import clear_console

# Main Program
clear_console()

while not globals.passed_login:
    login_menu()

while not globals.logout:
    result = user_menu()
    if result == 0:
        globals.logout = True
        globals.passed_login = False
        clear_console()
