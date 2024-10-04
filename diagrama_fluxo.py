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

# # determinando quantidade de sinais:
# num_sinais = int(input('\nO Sistema possui quantos sinais? '))

# ==================================================
# CLASSE SISTEMA

# declarando classe e seus métodos:
class Sistema:
    def __init__(self):
        self.matriz = Matrix.zeros(2, 2) # matriz quadrada
        self.sinais = ['R', 'C']
        self.caminhos = []
        self.lacos = []

        # definindo caminho unitário entre entrada e saída:
        self.matriz[0, 1] = 1
        self.setup()
    
    # atualiza a lista de sinais
    def atualiza_sinais(self):
        # adicionar os vértices entre 'R' e 'C':
        if self.matriz.rows > len(self.sinais):
            len_sinais = len(self.sinais)
            self.sinais.insert(-1, ('V' + str(len_sinais)))

    # atualiza a lista de caminhos
    def atualiza_caminhos(self):
        pass

    # atualiza a lista de lacos
    def atualiza_lacos(self):
        pass

    #
    def setup(self):
        self.atualiza_sinais()
        self.atualiza_caminhos()
        self.atualiza_lacos()

    #
    def adiciona_sinal(self, pos):
        novo_tam = self.matriz.rows + 1

        # cria uma nova matriz, com o novo tamanho:
        nova_matriz = Matrix.zeros(novo_tam, novo_tam)

        # reposiciona os valores da matriz antiga
        for linha in range(novo_tam):
            if linha == pos:
                continue

            for coluna in range(novo_tam):
                if  coluna == pos:
                    continue
                
                # ajustando nova posição:
                linha_ant = linha if linha < pos else (linha-pos)
                coluna_ant = coluna if coluna < pos else (coluna-pos)

                # preechendo nova matriz:
                nova_matriz[linha, coluna] = self.matriz[linha_ant, coluna_ant]

        # atualizando matriz:
        self.matriz = nova_matriz

        self.setup()



    # cria uma nova conexão entre sinais
    def adiciona_conexao(self, sinal1, sinal2):

        # Recebendo os coeficientes do numerador:
        num_coef = input("Digite os coeficientes do polinômio do numerador, separados por espaços (valor padrâo: 1)\n")

        if num_coef.strip() == "":
            num_coef = "1"

        num = [float(coef) for coef in num_coef.split()]
        num = num[::-1]
        eq_num = sum(coef * s**i for i, coef in enumerate(num))

        # Recebendo os coeficientes do denominador:
        den_coef = input("Digite os coeficientes do polinômio do denominador, separados por espaços (valor padrâo: 1)\n")
        
        if den_coef.strip() == "":
            den_coef = "1"

        den = [float(coef) for coef in den_coef.split()]
        den = den[::-1]
        eq_den = sum(coef * s**i for i, coef in enumerate(den))

        # Gerando a equação simbólica
        eq = eq_num/eq_den
        self.matriz[sinal1, sinal2] = eq

        self.desenha_diagrama()

    # remove uma nova conexão existente entre sinais:
    def remove_conexao(self, sinal1, sinal2):
        self.matriz[sinal1, sinal2] = 0

        self.desenha_diagrama()

    #
    def listar_sinais(self):
        print(self.sinais)
    
    # busca e lista todos os ganhos de caminho à frente do sistema:
    def lista_caminhos(self):
        caminhos = []
        
        return caminhos

    # busca e lista todos os ganhos de laço do sistema:
    def lista_lacos(self):
        lacos = []
        
        return lacos

    # desenha o diagrama (temp: desenha a matriz de fluxo):
    def desenha_diagrama(self):
        print(pretty(self.matriz))

    # calcula a FT resultante do sistema e exibe resultado:
    def calcula_FT(self):
        pass

# ==================================================
# FUNÇÕES DE INTERFACE

# menu de seleção dos sinais, usado para adicionar ou remover conexões:
def menu_sinal():
    os.system('cls')

    print('CONFIGURAÇÃO DO SINAL')
    print('''
1 - Adicionar Conexão
2 - Editar Conexões
3 - Remover Conexão
4 - Voltar
    ''');

    return int(input('\nEscolha uma opção: '));

# exibe menu principal:
def exibe_menu():
    os.system('cls')

    print('SISTEMAS DE CONTROLE')
    print('''
1 - Selecionar Sinal
2 - Adicionar Sinal
3 - Listar Ganhos do Caminhos à Frente
4 - Listar Ganhos de Laço
5 - Desenhar Diagrama
6 - Calcular FT
7 - Encerrar
    ''');

    return int(input('\nEscolha uma opção: '));

# ==================================================
# EXECUÇÃO DO PROGRAMA

print('\nCriando Sistema...'); time.sleep(0.2)
sistema = Sistema()

opc = 0
while True:
    opc = exibe_menu()
    
    if opc == 1:
        print('Abrindo Lista de Sinais...'); time.sleep(0.2)
        os.system('cls')        
        # sistema.adiciona_conexao(1, 2)
        sistema.listar_sinais()
        # opc2 = menu_sinal()
        input()

    if opc == 2:
        print('Adicionando Sinal...'); time.sleep(0.2)
        os.system('cls')
        sistema.adiciona_sinal(1)      
        input()
    
    if opc == 3:
        print('Listando Ganhos do Caminho à Frente...'); time.sleep(0.2)
        os.system('cls')
        sistema.lista_caminhos()
        input()
    
    if opc == 4:
        print('Listando Ganhos de Laço...'); time.sleep(0.2)
        os.system('cls')
        sistema.lista_lacos()
        input()

    if opc == 5:
        print('Desenhando Diagrama...'); time.sleep(0.2)
        os.system('cls')
        sistema.desenha_diagrama()
        input()

    if opc == 6:
        print('Calculando Função de Transferência...'); time.sleep(0.2)
        os.system('cls')
        sistema.calcula_FT()
        input()

    if opc == 7:
        print('Encerrando Programa...'); time.sleep(0.2)
        os.system('cls')
        break


