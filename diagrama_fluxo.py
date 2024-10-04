'''
    SISTEMAS DE CONTROLE I

    Esse programa é um protótipo desenvolvido para realizar
    a montagem dinâmica e o cálculo de um sistema de controle.
'''

# importando bibliotecas utilizadas:
from sympy import symbols, Matrix, pretty
import os, time

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

# criando matriz de sinais e sistemas:
matriz_de_fluxo = []
num_sinais = int(input('\nO Sistema possui quantos sinais? '))
matriz_de_fluxo = Matrix.zeros(num_sinais, num_sinais) #matriz quadrada

# ==================================================
# CLASSE SISTEMA

# declarando classe e seus métodos:
class Sistema:
    def __init__(self, matriz):
        self.matriz = matriz

    # cria uma nova conexão entre sinais
    def adiciona_conexao(self, sinal1, sinal2):
        # Recebendo os coeficientes do numerador:
        num_coef = input("Digite os coeficientes do polinômio do numerador, separados por espaços:\n")
        num = [float(coef) for coef in num_coef.split()]
        # num = list(reversed([float(coef) for coef in num_coef.split()]))
        #
        num = num[::-1]
        eq_num = sum(coef * s**i for i, coef in enumerate(num))

        # Recebendo os coeficientes do denominador:
        den_coef = input("Digite os coeficientes do polinômio do denominador, separados por espaços:\n")
        den = [float(coef) for coef in den_coef.split()]
        # den = list(reversed([float(coef) for coef in den_coef.split()]))
        #
        den = den[::-1]
        eq_den = sum(coef * s**i for i, coef in enumerate(den))

        # Gerando a equação simbólica
        eq = eq_num/eq_den
        self.matriz[sinal1, sinal2] = eq
        
        self.desenha_diagrama()

    # cria uma nova conexão entre sinais
    def remove_conexao(self, sinal1, sinal2):
        pass
    
    # busca e lista todos os ganhos de caminho à frente do sistema:
    def lista_caminhos(self):
        pass

    # busca e lista todos os ganhos de laço do sistema:
    def lista_lacos(self):
        pass

    # desenha o diagrama (temp: desenha a matriz de fluxo):
    def desenha_diagrama(self):
        print(pretty(self.matriz))

    # calcula a FT resultante do sistema e exibe resultado:
    def calcula_FT():
        pass

# ==================================================
# FUNÇÕES DE INTERFACE

# menu de seleção dos sinais, usado para adicionar ou remover conexões:
def menu_selecao():
    pass

# exibe menu principal:
def exibe_menu():
    os.system('cls')

    print('SISTEMAS DE CONTROLE')
    print('''
1 - Selecionar Sinal
2 - Listar Ganhos do Caminhos à Frente
3 - Listar Ganhos de Laço
4 - Desenhar Diagrama
5 - Calcular FT
6 - Encerrar
    ''');
    return int(input('\nEscolha uma opção: '));

# ==================================================
# EXECUÇÃO DO PROGRAMA

print('\nCriando Sistema...'); time.sleep(0.2)
sistema = Sistema(matriz_de_fluxo)

opc = 0
while True:
    opc = exibe_menu()
    
    if opc == 1:
        print('Abrindo Lista de Sinais...'); time.sleep(0.2)
        os.system('cls')        
        menu_selecao()
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
        print('Desenhando Diagrama...'); time.sleep(0.2)
        os.system('cls')
        sistema.desenha_diagrama()
        input()

    if opc == 5:
        print('Calculando Função de Transferência...'); time.sleep(0.2)
        os.system('cls')
        sistema.calcula_FT()
        input()

    if opc == 6:
        print('Encerrando Programa...'); time.sleep(0.2)
        os.system('cls')
        break


