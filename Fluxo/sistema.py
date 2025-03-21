from sympy import symbols, Matrix, pretty, sympify, simplify
import time, os

from itertools import combinations, chain

# Definindo variáveis simbólicas:
s = symbols('s')

# ==================================================
# CLASSE SISTEMA

# declarando classe e seus métodos:
class Sistema:
    def __init__(self, num_sinais):
        self.num_sinais = num_sinais
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

    # calcula o valor de delta geral:
    def calcula_delta(self):

        # soma os ganhos:
        soma_ganho = 0        
        for i in self.ganho_lacos:
            soma_ganho -= i

        # print(f'ganho: {soma_ganho}'); time.sleep(3)

        # soma dos ganhos que não se tocam:
        soma_ganho_nao_tocam = 0
        for i in self.ganhos_nao_tocam:
            if i[1]%2 == 0:
                soma_ganho_nao_tocam += i[0]
            else: 
                soma_ganho_nao_tocam -= i[0]

        # print(f'nao_tocam: {soma_ganho_nao_tocam}'); time.sleep(3)

        # return 1 + soma_ganho + soma_ganho_nao_tocam
        self.delta = 1 + soma_ganho + soma_ganho_nao_tocam

    # calcula o valor de delta para cada caminho:
    def calcula_delta_k(self):
        deltas_k = []

        # identifica quem o caminho encosta:
        for T in self.caminhos:
            delta_k = self.delta
            
            # elimina os ganhos de laço:
            for id, laco in enumerate(self.lacos):
                if set(T).intersection(set(laco)):
                    delta_k += self.ganho_lacos[id]
            
            # elimina os ganhos de laço que não se tocam:
            for id, nao_tocam in enumerate(self.nao_tocam):
                for laco in nao_tocam:

                    # basta um laço do grupo 'nao_tocam' encostar no caminho
                    if set(T).intersection(set(laco)):
                        ganho = self.ganhos_nao_tocam[id]
                        
                        if ganho[1]%2 == 0:
                            delta_k -= ganho[0]
                        else: 
                            delta_k += ganho[0]
                        break
            
            # salva o valor de delta do caminho:
            deltas_k.append(delta_k)
        
        return deltas_k

    # calcula a FT resultante do sistema e exibe resultado:
    def calcula_FT(self):
        # calcula delta:
        self.calcula_delta()

        if self.delta == 0:
            print("INDETERMINADO! Delta igual a Zero.")
            return
        
        # valores de delta de cada caminho:        
        deltas_k = self.calcula_delta_k()

        # calcula FT equivalente:
        sum = 0
        for k in range(len(self.caminhos)):
            sum += (self.ganho_caminhos[k]* deltas_k[k])
        
        FT = sum/self.delta
        
        return FT

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

    # exibe os valores da lista inserida, separados por um marcador
    def exibe_lista(self, lista, marcador, trava = False):
        for id1, item in enumerate(lista):
            print(f'{id1+1}. ', end='')
            for id2, v in enumerate(item):
                print(v, end=f' {marcador} ' if id2 < len(item) - 1 else '\n')      
            
            if trava:
                yield

    # gera uma nova conexão entre sinais:
    def adiciona_conexao(self, conexoes):
        inputs_adicionados = []
        inputs = []
        # remove os espaços em branco:
        lista_sem_espacos = conexoes.replace(' ', '')
        
        # testa se a entrada é válida:
        for caractere in lista_sem_espacos:
            if not (caractere.isdigit() or caractere in '>,RVGHC'):
                print('Entrada Inválida!'); time.sleep(0.2)
                return None
        
        # passando no teste, retomamos o processo:
        
        # separa as conexões:
        lista_conexoes = lista_sem_espacos.split(',')

        # adiciona cada um na sua posição:
        for conexao in lista_conexoes:

            # identifica o sinal referente a chave inserida:
            sinal1_k, sinal2_k = [valor for valor in conexao.split('>')]
            sinal1, sinal2 = self.sinais[sinal1_k], self.sinais[sinal2_k]

            # verifica se a conexão é válida, então adiciona na matriz de adjacências:
            if ((sinal1) > len(self.matriz)-1 or (sinal2) > len(self.matriz)-1) or sinal1 == sinal2:
                # print('Entrada Inválida!'); time.sleep(0.2)
                # return
                continue
            
            # cria a conexão (inicialmente, os ganhos também são unitários):
            if conexao in inputs_adicionados:
                self.matriz[sinal1][sinal2] += 1
                self.matriz_poly[sinal1][sinal2] += 1   
            else:
                self.matriz[sinal1][sinal2] = 1
                self.matriz_poly[sinal1][sinal2] = 1

            # armazena os inputs:
            inputs_adicionados.append(conexao)
            inputs.append(tuple([sinal1_k, sinal2_k]))
        
        # atualiza lista de inputs:
        self.inputs = inputs
        
        # atualiza informações do sistema:
        self.__setup()
        self.__setup_ganhos()

    # preenche a tabela de ganhos, de acordo com as conexões:
    def add_polinomio(self):
        inputs_adicionados = []
        
        # adiciona cada um na sua posição:
        for conexao in self.inputs:            

            sinal1_k, sinal2_k = conexao[0], conexao[1]
            sinal1, sinal2 = self.sinais[sinal1_k], self.sinais[sinal2_k]
            
            os.system('cls')

            eq = input(f'Polinômio da conexão {sinal1_k}>{sinal2_k}:')
            if eq == '':
                eq = 1
            if ((sinal1) > len(self.matriz_poly)-1 or (sinal2) > len(self.matriz_poly)-1) or sinal1 == sinal2:
                continue
            
            if conexao in inputs_adicionados:
                self.matriz_poly[sinal1][sinal2] += sympify(eq)
            else:
                self.matriz_poly[sinal1][sinal2] = sympify(eq)

            inputs_adicionados.append(conexao)

        self.__setup_ganhos()


    # ==================================================
    # MÉTODOS PRIVADOS

    # MÉTODOS DE CONTROLE:
    
    # Atualiza confirurações gerais:
    def __setup(self):
        '''Atualiza confirurações gerais'''

        self.__atualiza_sinais()
        self.__atualiza_caminhos()
        self.__atualiza_lacos()
        self.__atualiza_lacos_nao_se_tocam()

    # Atualiza a lista de sinais
    def __atualiza_sinais(self):
        '''Atualiza a lista de sinais'''
        
        # tamanho da matriz:
        len_matriz = len(self.matriz)

        # adicionar os vértices entre 'R' e 'C':
        if len_matriz > len(self.sinais):
            sinais = [('R', 0)]

            for i in range(1, len_matriz-1):
                sinais.append((('V' + str(i)), i))

            sinais.append(('C', len_matriz-1))
        
            self.sinais = dict(sinais)

    # Atualiza a lista de caminhos:
    def __atualiza_caminhos(self):
        '''Atualiza a lista de caminhos'''
        # matriz_up = self.matriz.upper_triangular()

        caminhos = []

        # Começar a busca do nó 0 e retorna lista de conexões:
        caminhos = self.__encontra_caminho(self.matriz, [[0]])

        # Atualiza lista de caminhos:           
        self.caminhos = caminhos

    # Atualiza a lista de lacos:
    def __atualiza_lacos(self):
        '''Atualiza a lista de lacos'''

        lacos = []

        # Começar a busca do nó 0
        lacos = self.__encontra_laco(self.matriz, [[0]])
                    
        self.lacos = lacos
    
    # Verifica as combinações de laços que não se tocam:
    def __verifica_colisao(self, vetor):
        '''Verifica as combinações de laços que não se tocam'''

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

    # Gera uma combinação de laços que não possuem sinais em comum:
    def __atualiza_lacos_nao_se_tocam(self):
        '''Gera uma combinação de laços que não possuem sinais em comum'''
        
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
    
    # Atualiza os atributos de ganho:
    def __setup_ganhos(self):
        '''Atualiza os atributos de ganho'''

        self.__ganho_caminho_frente()
        self.__ganho_laco()
        self.__ganho_nao_tocam()

    # Calcula os ganhos de caminho à frente:
    def __ganho_caminho_frente(self):
        '''Calcula os ganhos de caminho à frente'''

        self.ganho_caminhos = self.__multiplica(self.caminhos)

    # Calcula os ganhos de laço:
    def __ganho_laco(self):
        '''Calcula os ganhos de laço'''

        self.ganho_lacos = self.__multiplica(self.lacos)
    
    # Calcula os ganhos de laço que não se tocam:
    def __ganho_nao_tocam(self):
        '''Calcula os ganhos de laço que não se tocam'''
        
        ganhos_nao_tocam = []
        for i in self.nao_tocam:
            grau = len(i)
            ganho = 1
            for j in i:
                id = self.lacos.index(j)
                ganho *= self.ganho_lacos[id]

            ganhos_nao_tocam.append(tuple([ganho, grau]))
            
        self.ganhos_nao_tocam = ganhos_nao_tocam

    
    # MÉTODOS AUXILIARES:
    
    # Busca todos os caminhos à frente possíveis:
    def __encontra_caminho(self, mat, lista_init):
        '''Busca todos os caminhos à frente possíveis'''

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
            for i in range(len(mat)):

                if mat[ult_vertice][i] == 0:
                    continue
                
                novo_caminho = candidato + [i]
                
                # caso tenha virado um laço, novo_caminho é ignorado:
                eLaco = False
                for index, valor in enumerate(novo_caminho):
                    if novo_caminho.count(valor) > 1:
                        eLaco = True

                # adiciona o nova combinação a lista de novas caminhos:
                if not eLaco:
                    novos_caminhos.append(novo_caminho)

            # adiciona a nova combinação à lista de combinações
            lista_caminhos += novos_caminhos
            
        return lista_caminhos

    # Busca todos os laços possíveis:
    def __encontra_laco(self, mat, lista_init):
        '''Busca todos os laços possíveis'''

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

                if mat[ult_vertice][i] == 0:
                    continue
                    
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

    # Realiza uma multiplicação dos ganhos entre as conexões listadas:
    def __multiplica(self, lista_conex):
        '''Realiza uma multiplicação dos ganhos entre as conexões listadas'''
        
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

