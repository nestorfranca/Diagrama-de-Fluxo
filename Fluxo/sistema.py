from sympy import symbols, Matrix, pretty

# Definindo variáveis simbólicas:
s = symbols('s')

# ==================================================
# CLASSE SISTEMA

# declarando classe e seus métodos:
class Sistema:
    def __init__(self):
        self.matriz = Matrix.zeros(2, 2) # matriz quadrada
        self.sinais = {'R': 0, 'C': 1}
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


    # cria uma nova conexão entre sinais:
    def adiciona_conexao(self, conexoes):

        # remove os espaços em branco:
        lista_sem_espacos = conexoes.strip().replace(' ', '')
        
        # testa se a entrada é válida:
        for caractere in lista_sem_espacos:
            # só permite passar números positivos e o caracter '>':
            if not (caractere.isdigit() or caractere == '>'):
                print('Entrada Inválida!')
                return None
        
        # passando no teste, retomamos o processo:
        
        # separa as conexões:
        lista_conexoes = lista_sem_espacos.split(',')

        # adiciona cada um na sua posição:
        for conexao in lista_conexoes:
            sinal1, sinal2 = conexao.split('>')

            if sinal1 > self.matriz.rows or sinal1 > self.matriz.rows:
                print('Entrada Inválida!')
                return
            
            self.matriz[sinal1, sinal2] += 1


    # determina um novo sistema entre sinais:
    def definir_sistema(self, sinal1, sinal2):

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
