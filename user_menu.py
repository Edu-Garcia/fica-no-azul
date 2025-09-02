from utils import clear_console, wait_for_user


def add_transaction():
    print("\nOpções:\n1 - Adicionar Entrada de Saldo\n2 - Adicionar Saída de Saldo")
    option = int(input("\nOpção: "))
    print("Atualizar saldo")


def transaction_history():
    print("Lista do histórico de transações")


def undo_transaction():
    print("Desfazer transação")


def manage_transaction():
    print("\nGerenciar Transações")
    print("\nOpções:\n1 - Adicionar Transação\n2 - Histórico de Transações\n3 - Desfazer Transação")
    option = int(input("\nOpção: "))
    if option == 1:
        add_transaction()
    elif option == 2:
        transaction_history()
    elif option == 3:
        undo_transaction()
    else:
        print("Opção inválida! Tente novamente.")


def check_balance():
    print("\nConsultar Saldo")
    print("\nSeu saldo é de R$")
    print("Gráficos com histórico e oscilações do saldo")


def investor_profile():
    print("\nDefinir Perfil de Investidor")
    print("\nTipos de perfis de investidor:\nConservador\nModerado\nArrojado")
    print("\nDe acordo com seu perfil de investidor, estas são as recomendações de investimentos:")
    print("- Tesouro Selic 2030\n- CDB Banco Ítau\n- Tesouro IPCA+2050")


def simulate_investiment():
    print("\nSimular Investimentos")
    value = int(
        input("\nQual o valor a ser aplicado? (Caso queira voltar ao menu, digite 0) "))
    if value == 0:
        return

    print("Selecione o ativo desejado: ")
    active = str(input(
        "Opções:\n1 - Tesouro Selic 2030\n2 - CDB Banco Ítau\n3 - Tesouro IPCA+2050\n"))
    months = int(input("Por quantos meses esse valor ficará investido? "))
    print(f"\nApós {months} meses, seu investimento de R$ {value} no ativo {active} terá rendido R$ X, totalizando R$ Y.")


def financial_goals():
    print("\nMetas Financeiras")
    print("Opções:\n1 - Criar novas metas\n2 - Visualizar minhas metas\n3 - Atualizar/Modificar minhas metas")
    option = int(input("\nOpção: "))
    if option == 1:
        print("Criar novas metas")
    elif option == 2:
        print("Visualizar minhas metas")
    elif option == 3:
        print("Atualizar/Modificar minhas metas")
    else:
        print("Opção inválida! Tente novamente.")


def user_menu():
    print("Selecione uma das opções abaixo: ")
    print("1 - Gerenciar Transações\n2 - Consultar Saldo\n3 - Definir perfil de Investidor\n4 - Simular Investimento\n5 - Metas Financeiras\n0 - Sair")
    option = int(input("\nOpção: "))

    if option == 1:
        manage_transaction()
    elif option == 2:
        check_balance()
    elif option == 3:
        investor_profile()
    elif option == 4:
        simulate_investiment()
    elif option == 5:
        financial_goals()
    elif option == 0:
        print("Saindo...")
    else:
        print("Opção inválida! Tente novamente.")

    wait_for_user()
    clear_console()
    return option
