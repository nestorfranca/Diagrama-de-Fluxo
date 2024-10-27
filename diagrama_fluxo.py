'''
    SISTEMAS DE CONTROLE I

    Esse programa é um protótipo desenvolvido para realizar
    a montagem dinâmica e o cálculo de um sistema de controle.
'''

# importando bibliotecas utilizadas:
from sympy import symbols, Matrix, pretty
import os, time
from sistema import *
from grafico import *

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
2 - Adicionar Ganhos
3 - Listar Ganhos do Caminhos à Frente
4 - Listar Ganhos de Laço
5 - Calcular FT
6 - Encerrar
7 - Plota Gráfico
    ''');

    resp = input('\nEscolha uma opção: ')
    return int(resp) if resp.isnumeric() else 0;


# ==================================================
# EXECUÇÃO DO PROGRAMA

print('\nCriando Sistema...'); time.sleep(0.2)
os.system('cls')

sistema = Sistema(num_sinais)
print('Para adicionar novas conexões, utilize a simbologia a seguir:')
print('''
    R>V1: indica um caminho do sinal da entrada R para o sinal V1;
    V3>V1: indica um laço de realimentação do sinal V3 para o sinal de entrada V1.

''')

# R>V1, V1>V2,  V1>V2,  V1>V4,  V2>V3,  V3>V2,  V3>V4,  V4>V5,  V5>V4,  V5>V4,  V5>V1,  V5>C
# 1,    s,      2*s,    2*s,    s,      -1,     1,     1/(s+1), -1,     -4,     -1,     1  
# R>V1, V1>V2, V2>V3, V2>V4, V3>V4, V3>V2, V3>V1, V4>C, C>V4
conex = input('Insira as conexões a serem adicionadas, separadas por vírgula:\n')
sistema.adiciona_conexao(conex)

opc = 0
while True:
    opc = exibe_menu()
    
    if opc == 1:
        print('Vendo Status...'); time.sleep(0.2)
        os.system('cls')
        
        sistema.status()
        input()

    elif opc == 2:
        print('Adicionando Ganhos...'); time.sleep(0.2)
        os.system('cls')
        
        sistema.add_polinomio()

    elif opc == 3:
        print('Listando Ganhos do Caminho à Frente...'); time.sleep(0.2)
        os.system('cls')
        
        print(f'GANHOS DE CAMINHO À FRENTE:\n')
        g = sistema.exibe_lista(sistema.lista_caminhos(), '->', True)
        for ganho in sistema.ganho_caminhos:
            next(g)
            print(f'Ganho:')
            print(f'{pretty(ganho)}\n')

        print(f'\nMATRIZ DE GANHOS:')
        sistema.exibe_matriz(sistema.matriz_poly)
        input()

    
    elif opc == 4:
        print('Listando Ganhos de Laço...'); time.sleep(0.2)
        os.system('cls')
        
        print(f'GANHOS DE LAÇO:\n')
        g1 = sistema.exibe_lista(sistema.lista_lacos(), '->', True)
        for ganho in sistema.ganho_lacos:
            next(g1)
            print(f'Ganho:')
            print(f'{pretty(ganho)}\n')
        
        # imprime o grupo de laços que não se tocam:
        print(f'\nLaços que não se tocam:')
        g2 = sistema.exibe_lista(sistema.lista_lacos_nao_tocam(), 'e', True)
        for ganho in sistema.ganhos_nao_tocam:
            next(g2)
            print(f'Ganho:')
            print(f'{pretty(ganho[0])}\n')

        print(f'\nMATRIZ DE GANHOS:')
        sistema.exibe_matriz(sistema.matriz_poly)
        input()

    elif opc == 5:
        print('Calculando Função de Transferência...'); time.sleep(0.2)
        os.system('cls')

        print(f'FUNÇÃO TRANSFERÊNCIA EQUIVALENTE:\n')
        sistema.calcula_FT()
        input()

    elif opc == 6:
        print('Encerrando Programa...'); time.sleep(0.2)
        os.system('cls')
        break

    elif opc == 7:
        grafico = Grafico(sistema)

        grafico.gera_plot()
        grafico.draw()
        # grafico.draw_caminho(grafico.lacos, 2)

    else:
        print('Opção Inválida...'); time.sleep(0.2)

