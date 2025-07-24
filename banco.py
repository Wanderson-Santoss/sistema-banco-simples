import os
import time
import textwrap

# Limpa o terminal
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Exibe o menu principal e retorna a opção do usuário
def exibir_menu():
    limpar_tela()
    menu = """
    ========== MENU PRINCIPAL ==========
    [1] Realizar Depósito
    [2] Realizar Saque
    [3] Ver Extrato
    [4] Cadastrar Novo Usuário
    [5] Criar Conta Corrente
    [6] Listar Contas
    [0] Encerrar Sistema
    => """
    return input(textwrap.dedent(menu))


def deposito(saldo, valor, extrato, /):
    limpar_tela()
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print("✅ Depósito realizado com sucesso.")
    else:
        print("❌ Valor inválido para depósito.")
    time.sleep(2)
    return saldo, extrato


def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    limpar_tela()
    if valor <= 0:
        print("❌ Valor inválido.")
    elif valor > saldo:
        print("❌ Saldo insuficiente.")
    elif valor > limite:
        print("❌ Valor excede o limite permitido por saque.")
    elif numero_saques >= limite_saques:
        print("❌ Limite diário de saques atingido.")
    else:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        numero_saques += 1
        print("✅ Saque realizado com sucesso.")
    time.sleep(2)
    return saldo, extrato, numero_saques

# Exibe o extrato das movimentações e saldo atual
def mostrar_extrato(saldo, extrato):
    limpar_tela()
    print("=========== EXTRATO DA CONTA ===========")
    if not extrato:
        print("Nenhuma movimentação registrada.")
    else:
        for item in extrato:
            print(item)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("========================================")
    input("\nPressione Enter para voltar ao menu...")

# Cadastra novo usuário, garantindo CPF único
def novo_usuario(usuarios):
    limpar_tela()
    cpf = input("Informe o CPF (apenas números): ")
    if localizar_usuario(cpf, usuarios):
        print("❌ Usuário com esse CPF já existe.")
        time.sleep(2)
        return
    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (rua, nº - bairro - cidade/UF): ")
    usuarios.append({
        "nome": nome,
        "cpf": cpf,
        "nascimento": nascimento,
        "endereco": endereco
    })
    print("✅ Usuário cadastrado com sucesso.")
    time.sleep(2)

# Procura usuário por CPF
def localizar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

# Cria conta para usuário existente
def nova_conta(agencia, numero, usuarios):
    limpar_tela()
    cpf = input("Informe o CPF do titular: ")
    usuario = localizar_usuario(cpf, usuarios)
    if usuario:
        print("✅ Conta criada com sucesso.")
        time.sleep(2)
        return {
            "agencia": agencia,
            "conta": numero,
            "titular": usuario
        }
    print("❌ CPF não encontrado. Não foi possível criar a conta.")
    time.sleep(2)
    return None

# Lista todas as contas cadastradas
def listar_contas(contas):
    limpar_tela()
    print("========== CONTAS CADASTRADAS ==========")
    for conta in contas:
        print(f"Agência:\t{conta['agencia']}")
        print(f"Número da Conta:\t{conta['conta']}")
        print(f"Titular:\t{conta['titular']['nome']}")
        print("-" * 40)
    input("\nPressione Enter para voltar ao menu...")

# Função principal do sistema
def iniciar_sistema():
    saldo = 0
    extrato = []
    saques = 0
    LIMITE_SAQUE = 500
    MAX_SAQUES = 3
    AGENCIA = "0001"
    usuarios = []
    contas = []

    while True:
        opcao = exibir_menu()

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = deposito(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, saques = saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=LIMITE_SAQUE,
                numero_saques=saques,
                limite_saques=MAX_SAQUES
            )

        elif opcao == "3":
            mostrar_extrato(saldo, extrato)

        elif opcao == "4":
            novo_usuario(usuarios)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = nova_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "0":
            print("Finalizando o sistema...")
            time.sleep(1.5)
            limpar_tela()
            break

        else:
            print("❌ Opção inválida. Tente novamente.")
            time.sleep(2)

if __name__ == "__main__":
    iniciar_sistema()
