from sympy import symbols, Matrix, pretty

# Definindo variáveis simbólicas:
s = symbols('s')

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