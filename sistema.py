from sympy import symbols, Matrix, pretty
import time, os

from itertools import combinations, chain

# Definindo variáveis simbólicas:
s = symbols('s')

# ==================================================
# CLASSE SISTEMA

# declarando classe e seus métodos:
class Sistema:
    def __init__(self, num_sinais):
        self.matriz = Matrix.zeros(num_sinais, num_sinais) # matriz quadrada
        self.matriz_poly = Matrix.zeros(num_sinais, num_sinais) # matriz quadrada
        self.sinais = {'R': 0, 'C': 1}
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
            sinais = [('R', 0)]

            for i in range(1, len_matriz-1):
                sinais.append((('V' + str(i+1)), i))

            sinais.append(('C', len_matriz-1))
        
            self.sinais = dict(sinais)

    # atualiza a lista de caminhos:
    def atualiza_caminhos(self):
        matriz_up = self.matriz.upper_triangular()

        caminhos = []

        # Começar a busca do nó 0
        caminhos = encontra_caminho(matriz_up, [[0]])
                    
        self.caminhos = caminhos

    # atualiza a lista de lacos:
    def atualiza_lacos(self):
        lacos = []

        # Começar a busca do nó 0
        lacos = encontra_laco(self.matriz, [[0]])
                    
        self.lacos = lacos

    # atualiza confirurações gerais:
    def setup(self):
        self.atualiza_sinais()
        self.atualiza_caminhos()
        self.atualiza_lacos()

    # retorna a lista de sinais:
    def listar_sinais(self):
        return list(self.sinais.keys())
    
    # retorna a lista todos os ganhos de caminho à frente do sistema:
    def lista_caminhos(self):
        nomes_sinais = self.listar_sinais()
        
        # descreve os caminhos pelos nomes dos vértices:
        nomes_caminhos = []
        for caminho in self.caminhos:
            nome = []
            for valor in caminho:
                nome.append(nomes_sinais[valor])

            nomes_caminhos.append(nome)

        return nomes_caminhos

    # retorna a lista todos os ganhos de laço do sistema:
    def lista_lacos(self, lacos):
        nomes_sinais = self.listar_sinais()

        # descreve os laços pelos nomes dos vértices:
        nomes_lacos = []
        for laco in lacos:
            nome = []
            for valor in laco:
                nome.append(nomes_sinais[valor])

            nomes_lacos.append(nome)
        
        return nomes_lacos

    # ==================================================
    # FUNÇÕES AUXILIARES PARA CALCULAR A FT EQUIVALENTE:

    def lacos_nao_se_tocam(self, vetor_lacos):
        comb = list(chain.from_iterable(
            combinations(vetor_lacos, r) for r in range(1, len(vetor_lacos) + 1)
        ))

        comb = list(filter(lambda x: len(x) > 1, comb))

        nao_tocam = []

        for i in comb:
            colisao = False
            for laco1 in i:
                for laco2 in i:
                    if laco1 == laco2:
                        continue

                    valor_comum = set(laco1).intersection(set(laco2))
                    if len(valor_comum) > 0:
                        colisao = True
                    
            if not colisao:
                nao_tocam.append(i)

        return nao_tocam
    
    # ==================================================
    # calcula a FT resultante do sistema e exibe resultado:
    def calcula_FT(self):
        pass

    # informações gerais do sistema:
    def status(self):

        print(f'INFORMAÇÕES DO SISTEMA\n\n')
        print(f'Sinais: {self.listar_sinais()}')
        print(f'Caminhos: {self.lista_caminhos()}')
        print(f'Laços: {self.lista_lacos(self.lacos)}')

        print(f'\nMatriz:')
        print(f'\n{pretty(self.matriz)}')

        print(f'\n{pretty(self.matriz_poly)}')
        for i in self.lacos_nao_se_tocam(self.lacos):
            print(self.lista_lacos(i)) 

    # cria uma nova conexão entre sinais:
    def adiciona_conexao(self, conexoes):

        # remove os espaços em branco:
        lista_sem_espacos = conexoes.replace(' ', '')
        # print(lista_sem_espacos); time.sleep(3)
        
        # testa se a entrada é válida:
        for caractere in lista_sem_espacos:
            # só permite passar números positivos e o caracter '>':
            if not (caractere.isdigit() or caractere in '>,RVGHC'):
                print('Entrada Inválida!'); time.sleep(0.2)
                return None
        
        # passando no teste, retomamos o processo:
        
        # separa as conexões:
        lista_conexoes = lista_sem_espacos.split(',')

        # adiciona cada um na sua posição:
        for conexao in lista_conexoes:
            sinal1_k, sinal2_k = [valor for valor in conexao.split('>')]
            
            sinal1, sinal2 = self.sinais[sinal1_k], self.sinais[sinal2_k]
            # print(sinal1_k, sinal1,sinal2_k, sinal2); time.sleep(3)

            if ((sinal1) > self.matriz.rows-1 or (sinal2) > self.matriz.rows-1) or sinal1 == sinal2:
                # print('Entrada Inválida!'); time.sleep(0.2)
                # return
                continue
            
            self.matriz[sinal1, sinal2] += 1

    def add_polinomio(self, conexoes):
        
        # remove os espaços em branco:
        lista_sem_espacos = conexoes.replace(' ', '')
        
        # testa se a entrada é válida:
        for caractere in lista_sem_espacos:
            # só permite passar números positivos e o caracter '>':
            if not (caractere.isdigit() or caractere in '>,RVGHC'):
                print('Entrada Inválida!'); time.sleep(0.2)
                return None

        # separa as conexões:
        lista_conexoes = lista_sem_espacos.split(',')

        # adiciona cada um na sua posição:
        for conexao in lista_conexoes:
            eq = 1
            
            sinal1_k, sinal2_k = [valor for valor in conexao.split('>')]

            sinal1, sinal2 = self.sinais[sinal1_k], self.sinais[sinal2_k]
            # print(sinal1_k, sinal1,sinal2_k, sinal2); time.sleep(3)
            
            # x = input(f'Polinomio da conexão: {conexao}')
            
            os.system('cls')
            eq = input(f'Polinômio da conexão {sinal1_k}>{sinal2_k}:')
            if ((sinal1) > self.matriz_poly.rows-1 or (sinal2) > self.matriz_poly.rows-1) or sinal1 == sinal2:
                # print('Entrada Inválida!'); time.sleep(0.2)
                # return
                continue
            
            self.matriz_poly[sinal1, sinal2] = eq

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


# método recursivo:
'''
def encontra_caminho(matriz, inicio, caminho, caminhos):
    
    # armazenamos o vértice atual:
    caminho.append(inicio)

    # se for igual ao último vértice, armazenamos o caminho
    if inicio == matriz.rows-1:
        caminhos.append(list(caminho))
    else:

        # percorre todos os vértices, em todos os caminhos possíveis:
        for prox in range(matriz.cols):
            if matriz[inicio, prox] != 0 and prox not in caminho:
                    encontra_caminho(matriz, prox, caminho, caminhos)
                    
    # remover o vértice atual para permitir outras combinações
    caminho.pop()

def encontra_laco(matriz, inicio, laco, lacos):

    # armazena o vértice atual:
    laco.append(inicio)

    # Percorree todos os vértices, em todos os caminhos possíveis:
    for prox in range(matriz.shape[1]):
        if matriz[inicio, prox] != 0:
            if prox not in laco:
                encontra_laco(matriz, prox, laco, lacos)
            # se o próximo vértice estiver presente no vetor, então temos um laço:
            else:
                # encontra valor de origem do laço e remove os vértices anteriores a ele:
                # Ex:  [0, 1, 2, 4, 5, 2] --> [2, 4, 5, 2]
                i = laco.index(prox)
                novo_laco = laco[i:]
                novo_laco.append(prox)

                # testa se laço já existe:
                # if novo_laco not in lacos:
                repetido = False
                for lac in lacos:
                    # testa com lista de valores sem repetição:
                    if set(novo_laco) == set(lac):
                        repetido = True

                if not repetido:
                    lacos.append(list(novo_laco))
                    
    # Remover o nó atual para permitir outras combinações
    laco.pop()
'''
# métodos não recursivo:
def encontra_caminho(mat, lista_init):
    # copia a lista de entrada:
    lista_caminhos = lista_init.copy()
    
    # verifica cada combinação de caminho,
    while True:
        candidato = []

        # retira a primeira combinação incompleta disponível da lista, se houver:
        for index, caminho in enumerate(lista_caminhos):
            if (mat.rows-1) not in caminho:
                candidato = lista_caminhos.pop(index)
                break
            

        # se não houve nenhum candidato, a expansão acabou:
        if len(candidato) == 0:
            break
        
        # usa o último vértice para procurar novos caminhos:
        ult_vertice = candidato[-1]

        novos_caminhos = []
        for i in range(ult_vertice, mat.cols):

            if mat[ult_vertice, i] != 0:
                # adiciona o nova combinação a lista de novas caminhos:
                novos_caminhos.append(candidato + [i])

        # adiciona a nova combinação à lista de combinações
        lista_caminhos += novos_caminhos
        
    return lista_caminhos

def encontra_laco(mat, lista_init):
    # copia a lista de entrada:
    lista_lacos = lista_init.copy()
    
    # verifica cada combinação de laco,
    while True:
        candidato = []

        # retira a primeira combinação incompleta disponível da lista, se houver:
        for index, comb in enumerate(lista_lacos):
            # verifica se é laço:
            if (len(comb) == 1) or (comb[0] != comb[-1]):
                candidato = lista_lacos.pop(index)
                break
        
        # se não houve nenhum candidato, a expansão acabou:
        if len(candidato) == 0:
            break
        
        # usa o último vértice para procurar novas combinações:
        ult_vertice = candidato[-1]

        novas_comb = []
        for i in range(mat.cols):

            if mat[ult_vertice, i] != 0:
                
                novo_laco = candidato + [i]

                # verifica se é um laço:
                for index, valor in enumerate(novo_laco):

                    # se achar um laço, remove os valores em excesso:
                    # Ex.: [0, 1, 2, 3, 4, 2] ==> [2, 3, 4, 2]
                    if novo_laco.count(valor) > 1:
                        novo_laco = novo_laco[index:]
                        break
                    
                # verifica se já não existe o laço:
                repetido = False
                for laco in lista_lacos:
                    if set(novo_laco) == set(laco):
                        repetido = True

                # adiciona o nova combinação a lista de novas lacos:
                if not repetido:
                    novas_comb.append(novo_laco)

        # adiciona a nova combinação à lista de combinações
        lista_lacos += novas_comb

    return lista_lacos


