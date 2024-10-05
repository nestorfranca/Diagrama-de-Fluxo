'''
    SISTEMAS DE CONTROLE I

    Esse programa é um protótipo desenvolvido para realizar
    a montagem dinâmica e o cálculo de um sistema de controle.
'''

# importando bibliotecas utilizadas:
from sympy import symbols, Matrix, pretty
import os, time
from sistema import *

'''
    NOTAS PARA CRIAÇÃO DA MATRIZ:

    Sinal -> Vértices da matriz. Representa o ponto de conexão
    entre os sistemas.

    Sistema -> Valor do vértice. Representa a FT do sistema
    que conecta dois sinais.

    * O Triângulo superior da matriz representa as conexões
      de caminho entre os sinais.
    
    ** O Triângulo inferior da matriz representa as conexões
       de realimentação entre os sinais.
'''
# Definindo variáveis simbólicas:
s = symbols('s')

# determinando quantidade de sinais:
num_sinais = int(input('\nO Sistema possui quantos sinais? '))


# ==================================================
# FUNÇÕES DE INTERFACE

# exibe menu principal:
def exibe_menu():
    os.system('cls')

    print('SISTEMAS DE CONTROLE')
    print('''
1 - Ver Status
2 - Listar Ganhos do Caminhos à Frente
3 - Listar Ganhos de Laço
4 - Calcular FT
5 - Encerrar
    ''');

    return int(input('\nEscolha uma opção: '));


# ==================================================
# EXECUÇÃO DO PROGRAMA

print('\nCriando Sistema...'); time.sleep(0.2)
os.system('cls')

sistema = Sistema(num_sinais)

print('Para adicionar novas conexões, utilize a simbologia a seguir:')
print('''
    1>2: indica um caminho do sinal 1 para o sinal 2;
    2>1: indica um laço de realimentação do sinal 2 para o sinal 1.

''')

conex = input('Insira as conexões a serem adicionadas, separadas por vírgula:\n')

sistema.adiciona_conexao(conex)

sistema.setup()

opc = 0
while True:
    opc = exibe_menu()
    
    if opc == 1:
        print('Vendo Status...'); time.sleep(0.2)
        os.system('cls')
        sistema.status()
        input()

    if opc == 2:
        print('Listando Ganhos do Caminho à Frente...'); time.sleep(0.2)
        os.system('cls')
        sistema.lista_caminhos()
        input()
    
    if opc == 3:
        print('Listando Ganhos de Laço...'); time.sleep(0.2)
        os.system('cls')
        sistema.lista_lacos()
        input()

    if opc == 4:
        print('Calculando Função de Transferência...'); time.sleep(0.2)
        os.system('cls')
        sistema.calcula_FT()
        input()

    if opc == 5:
        print('Encerrando Programa...'); time.sleep(0.2)
        os.system('cls')
        break


