from sympy import symbols, Matrix, pretty
import time, os

# Definindo variáveis simbólicas:
s = symbols('s')

# ==================================================
# CLASSE SISTEMA

# declarando classe e seus métodos:
class Sistema:
    def __init__(self, num_sinais):
        self.matriz = Matrix.zeros(num_sinais, num_sinais) # matriz quadrada
        self.sinais = ['R', 'C']
        self.caminhos = []
        self.lacos = []

        # definindo caminho unitário entre entrada e saída:
        # self.matriz[0, 1] = 1
        self.setup()
    
    # atualiza a lista de sinais
    def atualiza_sinais(self):
        # tamanho da matriz:
        len_matriz = self.matriz.rows

        # adicionar os vértices entre 'R' e 'C':
        if len_matriz > len(self.sinais):
            for i in range(2, len_matriz):
                self.sinais.insert(-1, ('V' + str(i)))

    # atualiza a lista de caminhos:
    def atualiza_caminhos(self):
        matriz_up = self.matriz.upper_triangular()

        caminhos = []
        lacos = []
        # Começar a busca do nó 0
        encontra_caminho(matriz_up, 0, [], caminhos)
                    
        self.caminhos = caminhos
        self.lacos = lacos

    # atualiza a lista de lacos:
    def atualiza_lacos(self):
        lacos = []
        # Começar a busca do nó 0
        encontra_laco(self.matriz, 0, [], lacos)
                    
        self.lacos = lacos

    # atualiza confirurações gerais:
    def setup(self):
        self.atualiza_sinais()
        self.atualiza_caminhos()
        self.atualiza_lacos()

    # retorna a lista de sinais:
    def listar_sinais(self):
        return self.sinais
    
    # retorna a lista todos os ganhos de caminho à frente do sistema:
    def lista_caminhos(self):
        return self.caminhos

    # retorna a lista todos os ganhos de laço do sistema:
    def lista_lacos(self):
        return self.lacos

    # calcula a FT resultante do sistema e exibe resultado:
    def calcula_FT(self):
        pass

    # informações gerais do sistema:
    def status(self):
        print(f'''INFORMAÇÕES DO SISTEMA
              
Sinais: {self.listar_sinais()}
Caminhos: {self.caminhos}
Laços: {self.lacos}

Matriz:

{pretty(self.matriz)}
        ''')

    # cria uma nova conexão entre sinais:
    def adiciona_conexao(self, conexoes):

        # remove os espaços em branco:
        lista_sem_espacos = conexoes.strip().replace(' ', '')
        
        # testa se a entrada é válida:
        for caractere in lista_sem_espacos:
            # só permite passar números positivos e o caracter '>':
            if not (caractere.isdigit() or caractere == '>' or caractere == ','):
                print('Entrada Inválida!'); time.sleep(0.2)
                return None
        
        # passando no teste, retomamos o processo:
        
        # separa as conexões:
        lista_conexoes = lista_sem_espacos.split(',')

        # adiciona cada um na sua posição:
        for conexao in lista_conexoes:
            sinal1, sinal2 = [int(num) for num in conexao.split('>')]
            if ((sinal1-1) > self.matriz.rows-1 or (sinal2-1) > self.matriz.rows-1) or sinal1 == sinal2:
                # print('Entrada Inválida!'); time.sleep(0.2)
                # return
                continue
            
            self.matriz[sinal1-1, sinal2-1] += 1
    # ==================================================
    # METODOS EM TESTE...
    '''
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

    
    # desenha o diagrama (temp: desenha a matriz de fluxo):
    def desenha_diagrama(self):
        print(pretty(self.matriz))
    '''


def encontra_caminho(matriz, inicio, caminho, caminhos):
    caminho.append(inicio)

    # Se chegamos ao último nó, armazenamos o caminho e o ganho
    if inicio == matriz.shape[0] - 1:
        caminhos.append(list(caminho))
    else:

        # Percorrer todos os nós possíveis
        for prox_no in range(matriz.shape[1]):
            if matriz[inicio, prox_no] != 0 and prox_no not in caminho:
                    encontra_caminho(matriz, prox_no, caminho, caminhos)
                    
    # Remover o nó atual para permitir outras combinações
    caminho.pop()


def encontra_laco(matriz, inicio, laco, lacos):

    # Se chegamos ao último nó, armazenamos o laco e o ganho
    laco.append(inicio)

    # Percorrer todos os nós possíveis
    for prox_no in range(matriz.shape[1]):
        if matriz[inicio, prox_no] != 0:
            if prox_no not in laco:
                encontra_laco(matriz, prox_no, laco, lacos)
            else:
                i = laco.index(prox_no)
                novo_laco = laco[i:]
                novo_laco.append(prox_no)

                # testa se laço já existe:
                # if novo_laco not in lacos:
                repetido = False
                for lac in lacos:
                    if set(novo_laco) == set(lac):
                        repetido = True

                if not repetido:
                    lacos.append(list(novo_laco))
                    
    # Remover o nó atual para permitir outras combinações
    laco.pop()
