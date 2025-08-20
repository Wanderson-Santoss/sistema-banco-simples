import os
import time
import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

# ----------------- FUNÇÕES AUXILIARES ----------------- #
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar(segundos=2):
    time.sleep(segundos)

# ----------------- CLASSES ----------------- #
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Valor inválido para saque. @@@")
            return False
        if valor > self._saldo:
            print("\n@@@ Saldo insuficiente. @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Valor inválido para depósito. @@@")
            return False
        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([t for t in self.historico.transacoes if t["tipo"] == Saque.__name__])
        if valor > self._limite:
            print("\n@@@ Valor do saque excede o limite permitido. @@@")
            return False
        if numero_saques >= self._limite_saques:
            print("\n@@@ Número máximo de saques atingido. @@@")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"Agência: {self.agencia} | C/C: {self.numero} | Titular: {self.cliente.nome}"

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

# ----------------- MENU E FUNÇÕES ----------------- #
def exibir_menu():
    limpar_tela()
    menu = """
    ================ MENU ================
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q] Sair
    => """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def selecionar_conta(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        pausar()
        return None

    if len(cliente.contas) == 1:
        return cliente.contas[0]

    print("\nO cliente possui mais de uma conta. Escolha uma:")
    for idx, conta in enumerate(cliente.contas, start=1):
        print(f"[{idx}] Conta {conta.numero} | Agência {conta.agencia}")

    while True:
        escolha = input("Selecione o número da conta: ")
        if escolha.isdigit():
            escolha = int(escolha)
            if 1 <= escolha <= len(cliente.contas):
                return cliente.contas[escolha - 1]
        print("Opção inválida. Tente novamente.")

def depositar_cliente(clientes):
    limpar_tela()
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        pausar()
        return

    conta = selecionar_conta(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)
    pausar()

def sacar_cliente(clientes):
    limpar_tela()
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        pausar()
        return

    conta = selecionar_conta(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)
    pausar()

def exibir_extrato_cliente(clientes):
    limpar_tela()
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        pausar()
        return

    conta = selecionar_conta(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for t in transacoes:
            print(f"{t['data']} | {t['tipo']} | R$ {t['valor']:.2f}")
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("========================================")
    input("\nPressione Enter para voltar ao menu...")

def criar_cliente(clientes):
    limpar_tela()
    cpf = input("Informe o CPF (somente números): ")
    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        pausar()
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    clientes.append(cliente)
    print("\n=== Cliente criado com sucesso! ===")
    pausar()

def criar_conta(numero_conta, clientes, contas):
    limpar_tela()
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        pausar()
        return

    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("\n=== Conta criada com sucesso! ===")
    pausar()

def listar_contas(contas):
    limpar_tela()
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        for conta in contas:
            print("=" * 40)
            print(conta)
            print("=" * 40)
    input("\nPressione Enter para voltar ao menu...")

# ----------------- MAIN ----------------- #
def main():
    clientes = []
    contas = []

    while True:
        opcao = exibir_menu()

        if opcao == "d":
            depositar_cliente(clientes)
        elif opcao == "s":
            sacar_cliente(clientes)
        elif opcao == "e":
            exibir_extrato_cliente(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            limpar_tela()
            print("Encerrando o sistema...")
            pausar()
            break
        else:
            print("\n@@@ Opção inválida! @@@")
            pausar()

if __name__ == "__main__":
    main()