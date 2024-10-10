from sympy import symbols, Matrix, pretty, sympify
import time, os

from itertools import combinations, chain

# Definindo variáveis simbólicas:
s = symbols('s')

# ==================================================
# CLASSE SISTEMA

# declarando classe e seus métodos:
class Sistema:
    def __init__(self, num_sinais):
        self.inputs = []
        self.matriz = [[0 for _ in range(num_sinais)] for _ in range(num_sinais)] # matriz quadrada
        self.matriz_poly = [[0 for _ in range(num_sinais)] for _ in range(num_sinais)]
        
        self.sinais = {'R': 0, 'C': 1}
        self.caminhos = []
        self.lacos = []
        self.ganho_caminhos = []
        self.ganho_lacos = []
        self.nao_tocam = []
        self.ganhos_nao_tocam = []
        self.delta = 1

        # definindo
        self.__setup()
    
    # ==================================================
    # MÉTODOS PÚBLICOS:

    # retorna a lista de sinais:
    def lista_sinais(self):
        return list(self.sinais.keys())
    
    # retorna a lista todos os ganhos de caminho à frente do sistema:
    def lista_caminhos(self):
        nomes_sinais = self.lista_sinais()
        
        # descreve os caminhos pelos nomes dos vértices:
        nomes_caminhos = []
        for caminho in self.caminhos:
            nome = []
            for valor in caminho:
                nome.append(nomes_sinais[valor])

            nomes_caminhos.append(nome)

        return nomes_caminhos

    # retorna a lista todos os ganhos de laço do sistema:
    def lista_lacos(self):
        nomes_sinais = self.lista_sinais()

        # descreve os laços pelos nomes dos vértices:
        nomes_lacos = []
        for laco in self.lacos:
            nome = []
            for valor in laco:
                nome.append(nomes_sinais[valor])

            nomes_lacos.append(nome)
        
        return nomes_lacos
    
    # retorna a lista dos conjuntos de ganhos que não se tocam:
    def lista_lacos_nao_tocam(self):
        indices_conj = []
        for conj in self.nao_tocam:
            indices = []
            for laco in conj:
                indices.append(self.lacos.index(laco)+1)

            indices_conj.append(tuple(indices))
            
        return indices_conj

    # calcula a FT resultante do sistema e exibe resultado:
    def calcula_FT(self):
        pass
    
    # informações gerais do sistema:
    def status(self):

        print(f'INFORMAÇÕES DO SISTEMA')
        print(f'\nSinais:')
        sinais = self.lista_sinais()
        [print(sinal, end=' ') for sinal in sinais]
        print()

        # imprime caminhos:
        print(f'\nCaminhos:')
        try:
            next(self.exibe_lista(self.lista_caminhos(), '->'))
        except StopIteration:
            pass
        
        # imprime laços:
        print(f'\nLaços:')
        try:
            next(self.exibe_lista(self.lista_lacos(), '->'))
        except StopIteration:
            pass
        
        # imprime o grupo de laços que não se tocam:
        print(f'\nLaços que não se tocam:')
        try:
            next(self.exibe_lista(self.lista_lacos_nao_tocam(), 'e'))
        except StopIteration:
            pass
        
        print(f'\nMatriz:')

        print(f'\nMATRIZ DE ADJACÊNCIAS:')
        self.exibe_matriz(self.matriz)

    # exibe as tabelas de conexões:
    def exibe_matriz(self, matriz):
        print(f'\n{pretty(Matrix(matriz))}')

    # gera uma nova conexão entre sinais:
    def adiciona_conexao(self, conexoes):
        # remove os espaços em branco:
        lista_sem_espacos = conexoes.replace(' ', '')
        
        # testa se a entrada é válida:
        for caractere in lista_sem_espacos:
            # só permite passar números positivos e os caracteres aprovados:
            if not (caractere.isdigit() or caractere in '>,RVGHC'):
                print('Entrada Inválida!'); time.sleep(0.2)
                return None
        
        # passando no teste, retomamos o processo:
        
        # separa as conexões:
        lista_conexoes = lista_sem_espacos.split(',')

        # adiciona cada um na sua posição:
        for conexao in lista_conexoes:

            # identifica o valor referente a chave escrita:
            sinal1_k, sinal2_k = [valor for valor in conexao.split('>')]
            sinal1, sinal2 = self.sinais[sinal1_k], self.sinais[sinal2_k]

            # se a conexão for válida, então adiciona na matriz de adjacências:
            if ((sinal1) > len(self.matriz)-1 or (sinal2) > len(self.matriz)-1) or sinal1 == sinal2:
                # print('Entrada Inválida!'); time.sleep(0.2)
                # return
                continue
            
            # armazena os inputs:
            self.inputs.append(tuple([sinal1_k, sinal2_k]))

            # cria a conexão:
            self.matriz[sinal1][sinal2] += 1

            # inicialmente, os ganhos da matriz_poly são unitários:
            self.matriz_poly[sinal1][sinal2] += 1   
        
        # atualiza informações do sistema:
        self.__setup()
        self.__setup_ganhos()

    # preenche a tabela de ganhos, de acordo com as conexões:
    def add_polinomio(self):
        
        inputs_adicionados = []
        # adiciona cada um na sua posição:
        for conexao in self.inputs:            
            eq = 1
            
            sinal1_k, sinal2_k = conexao[0], conexao[1]

            sinal1, sinal2 = self.sinais[sinal1_k], self.sinais[sinal2_k]
            # print(sinal1_k, sinal1,sinal2_k, sinal2); time.sleep(3)
            
            # x = input(f'Polinomio da conexão: {conexao}')
            
            os.system('cls')
            eq = input(f'Polinômio da conexão {sinal1_k}>{sinal2_k}:')
            if eq == '':
                eq = 1
            if ((sinal1) > len(self.matriz_poly)-1 or (sinal2) > len(self.matriz_poly)-1) or sinal1 == sinal2:
                # print('Entrada Inválida!'); time.sleep(0.2)
                # return
                continue
            

            if conexao in inputs_adicionados:
                self.matriz_poly[sinal1][sinal2] += sympify(eq)
            else:
                self.matriz_poly[sinal1][sinal2] = sympify(eq)

            inputs_adicionados.append(conexao)

        self.__setup_ganhos()

    # ==================================================
    # MÉTODOS PRIVADOS (MÉTODOS AUXILIARES)

    # MÉTODOS DE CONTROLE:
    
    # atualiza confirurações gerais:
    def __setup(self):
        self.__atualiza_sinais()
        self.__atualiza_caminhos()
        self.__atualiza_lacos()
        self.__atualiza_lacos_nao_se_tocam()

    # atualiza a lista de sinais
    def __atualiza_sinais(self):
        # tamanho da matriz:
        len_matriz = len(self.matriz)

        # adicionar os vértices entre 'R' e 'C':
        if len_matriz > len(self.sinais):
            sinais = [('R', 0)]

            for i in range(1, len_matriz-1):
                sinais.append((('V' + str(i)), i))

            sinais.append(('C', len_matriz-1))
        
            self.sinais = dict(sinais)

    # atualiza a lista de caminhos:
    def __atualiza_caminhos(self):
        # matriz_up = self.matriz.upper_triangular()

        caminhos = []

        # Começar a busca do nó 0 e retorna lista de conexões:
        caminhos = self.__encontra_caminho(self.matriz, [[0]])

        # Atualiza lista de caminhos:           
        self.caminhos = caminhos

    # atualiza a lista de lacos:
    def __atualiza_lacos(self):
        lacos = []

        # Começar a busca do nó 0
        lacos = self.__encontra_laco(self.matriz, [[0]])
                    
        self.lacos = lacos
    
    # Verifica as combinações de laços que não se tocam:
    def __verifica_colisao(self, vetor):
        
        # teste todos os pares de conjuntos dentro do vetor:
        for conjunto1 in vetor:
            for conjunto2 in vetor:
                
                if conjunto1 == conjunto2:
                    continue
                    
                # se houver um valor de interseção, então há colisão
                valor_comum = set(conjunto1).intersection(set(conjunto2))
                if len(valor_comum) > 0:
                    return True
                    
        return False

    def __atualiza_lacos_nao_se_tocam(self):

        # método que retorna uma lista de combinação
        comb = list(chain.from_iterable(
            combinations(self.lacos, r) for r in range(1, len(self.lacos) + 1)
        ))

        # mantém apenas os conjuntos com 2 laços ou mais:
        comb = list(filter(lambda x: len(x) > 1, comb))

        # verifica se há colisão em cada conjunto:
        nao_tocam = []

        for i in comb:
            if not self.__verifica_colisao(i):
                nao_tocam.append(i)

        # atualiza atributo:
        self.nao_tocam = nao_tocam
    
    # atualiza os atributos de ganho
    def __setup_ganhos(self):
        self.__ganho_caminho_frente()
        self.__ganho_laco()
        self.__ganho_nao_tocam()



    # FUNÇÕES AUXILIARES PARA CALCULAR A FT EQUIVALENTE:

    # Calcula os ganhos de caminho à frente:
    def __ganho_caminho_frente(self):
        self.ganho_caminhos = self.__multiplica(self.caminhos)

    # Calcula os ganhos de laço:
    def __ganho_laco(self):
        self.ganho_lacos = self.__multiplica(self.lacos)
    
    # Calcula os ganhos de laço que não se tocam:
    def __ganho_nao_tocam(self):
        
        ganhos_nao_tocam = []
        for i in self.nao_tocam:
            grau = len(i)
            ganho = 1
            for j in i:
                id = self.lacos.index(j)
                ganho *= self.ganho_lacos[id]

            ganhos_nao_tocam.append(tuple([ganho, grau]))
            
        self.ganhos_nao_tocam = ganhos_nao_tocam

    #
    def __delta(self):
        delta_ = 0
        
        for i in self.ganho_lacos:
            delta_ += i

        for i in range(self.ganhos_nao_tocam):
            if i[1]%2 == 0:
                delta_ += i
            else: 
                delta_ -=i

        self.delta = 1 + delta_

    #
    def __delta_k(self):
        pass
        


    # MÉTODOS AUXILIARES:
    
    #
    def exibe_lista(self, lista, marcador, trava = False):
        for id1, item in enumerate(lista):
            print(f'{id1+1}. ', end='')
            for id2, v in enumerate(item):
                print(v, end=f' {marcador} ' if id2 < len(item) - 1 else '\n')      
            
            if trava:
                yield

    # busca todos os caminhos à frente possíveis:
    def __encontra_caminho(self, mat, lista_init):
        # copia a lista de entrada:
        lista_caminhos = lista_init.copy()
        
        # verifica cada combinação de caminho,
        while True:
            candidato = []

            # retira a primeira combinação incompleta disponível da lista, se houver:
            for index, caminho in enumerate(lista_caminhos):
                if (len(mat)-1) not in caminho:
                    candidato = lista_caminhos.pop(index)
                    break
                

            # se não houve nenhum candidato, a expansão acabou:
            if len(candidato) == 0:
                break
            
            # usa o último vértice para procurar novos caminhos:
            ult_vertice = candidato[-1]

            novos_caminhos = []
            for i in range(ult_vertice, len(mat)):
                if mat[ult_vertice][i] != 0:
                    # adiciona o nova combinação a lista de novas caminhos:
                    novos_caminhos.append(candidato + [i])

            # adiciona a nova combinação à lista de combinações
            lista_caminhos += novos_caminhos
            
        return lista_caminhos

    # busca todos os laços possíveis:
    def __encontra_laco(self, mat, lista_init):
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
            for i in range(len(mat)):

                if mat[ult_vertice][i] != 0:
                    
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

    # realiza uma multiplicação dos ganhos entre as conexões listadas:
    def __multiplica(self, lista_conex):
        ganhos = []
        for i in lista_conex:
            ganho = 1
            for j in range(len(i)-1):
                prox = (j+1)%len(i)

                sinal1 = i[j]
                sinal2 = i[prox]

                ganho *= self.matriz_poly[sinal1][sinal2]

            ganhos.append(ganho)
        return ganhos

