import matplotlib.pyplot as plt
from sistema import *

class Grafico:
    def __init__(self, sistema):
        self.num_sinais = sistema.num_sinais
        self.matriz = sistema.matriz
        self.pos_x = []
        self.pos_y = []
        self.nos = []
        self.pos = {}
        self.sinais = sistema.sinais
        self.caminhos = sistema.caminhos
        self.lacos = sistema.lacos
        self.principal = None 
        self.max_len = 0
        self.conta_caminhos = 0

        self.ax = None
        self.transparencia = [1, 1]

        self.__setup()

    # ==================================================
    # MÉTODOS PRIVADOS:

    # Configurações da classe:
    def __setup(self):

        self.pos_x, self.pos_y = self.__define_pos_X(), self.__define_pos_Y()

        self.nos = list(self.sinais.keys())
        # self.pos = dict([self.nos[i], (self.pos_x[i], self.pos_y[i])] for i in range(len(self.nos)))
        for i in range(len(self.nos)):
            self.pos[self.nos[i]] = (self.pos_x[i], self.pos_y[i])

        self.principal = max(self.caminhos_frente, key=lambda caminho: len(caminho))
        self.max_len = len(self.principal)
        self.conta_caminhos = sum(1 for caminho in self.caminhos_frente if len(caminho) == self.max_len)

        # Criar a figura e remove os eixos
        _, self.ax = plt.subplots(figsize=(len(self.matriz), len(self.matriz)))
        limites = [abs(min(self.pos_y)), abs(max(self.pos_y))]
        limite = max(limites)
        plt.ylim(-limite*2.5, limite*2.5) # Colocar o menor e maior peso para y
        # ax.set_axis_off()
    
    # Define coordenada X dos nós:
    def __define_pos_X(self):
        # Inicializa as posições do eixo X em "-1":
        pesos_x = len(self.matriz)*[-1]
        # [-1,- 1,- 1, ..., -1]

        # Define o maior caminho de frente como o caminho principal:
        for index, value in enumerate(self.principal):
            pesos_x[value] = float(index)   # posição X é equivalente ao índice no vetor
        # [0, 1, 2, 3, 4, 5, -1, -1, -1, 6]

        # Define posição do eixo X das ramificações do caminho de frente principal:
        for value in self.caminhos_frente:
            
            if value == self.principal:
                continue
            
            # verifica os nós que não estão no caminho principal:
            dif = value.copy()
            for v in self.principal:
                if v in dif:
                    dif.pop(dif.index(v))

            if dif == list():
                continue
            
            # salva os nós do caminho principal que começa e termina a ramificação:
            for i, v in enumerate(value):
                if v == dif[0]:
                    anterior = value[i-1]

                if v == dif[-1]:
                    posterior = value[i+1]

            # valor coordenada X dos nós da ramificação:
            distancia = pesos_x[posterior] - pesos_x[anterior]
            deslocamento = distancia/(len(dif) + 1)
            for i, d in enumerate(dif):
                pesos_x[d] = pesos_x[anterior] + (deslocamento * (i+1))

        # Define posição do eixo X dos laços:
        for value in self.lacos:

            # verifica os nós que não estão no caminho principal:
            dif = value[:-1].copy() # remove o último nó
            for v in self.principal:
                if v in dif:
                    dif.pop(dif.index(v))

            if dif == list():
                continue
            
            # salva os nós do caminho principal que começa e termina a ramificação:
            for i, v in enumerate(value):
                if v == dif[0]:
                    anterior = value[i-1]

                if v == dif[-1]:
                    posterior = value[i+1]

            # valor coordenada X dos nós do laço:
            distancia = pesos_x[posterior] - pesos_x[anterior]
            deslocamento = distancia/(len(dif) + 1)
            for i, d in enumerate(dif):
                pesos_x[d] = pesos_x[anterior] + (deslocamento * (i+1))

        return pesos_x

    # Define coordenada Y dos nós:
    def __define_pos_Y(self):
        # Inicializa as posições do eixo Y em "None":
        pesos_y = len(self.matriz)*[None]

        # Aplica os pesos em Y
        # Define posição Y do maior caminho de frente como 0:
        for i in self.principal:
            pesos_y[i] = 0
        # [0, 0, 0, 0, 0, -1, -1, -1, 0]

        # Define posição do eixo Y das ramificações do caminho de frente principal:
        for value in self.caminhos_frente:
            
            if value == self.principal:
                continue
            
            # verifica os nós que não estão no caminho principal:
            dif = value.copy()
            for v in self.principal:
                if v in dif:
                    dif.pop(dif.index(v))

            if dif == list():
                continue
            
            # salva os nós do caminho principal que começa e termina a ramificação:
            for i, v in enumerate(value):
                if v == dif[0]:
                    inicio = value[i-1]

                if v == dif[-1]:
                    fim = value[i+1]

            # distância da coordenada X dos nós de início e fim da ramificação:
            distancia = self.pos_x[fim] - self.pos_x[inicio]
            for d in dif:
                pesos_y[d] = round(0.15 * distancia, 2)

        # Define posição do eixo Y dos laços:
        for value in self.lacos:

            # verifica os nós que não estão no caminho principal:
            dif = value[:-1].copy() # remove o último nó
            for v in self.principal:
                if v in dif:
                    dif.pop(dif.index(v))

            if dif == list():
                continue
            
            # salva os nós do caminho principal que começa e termina a ramificação:
            for i, v in enumerate(value):
                if v == dif[0]:
                    inicio = value[i-1]

                if v == dif[-1]:
                    fim = value[i+1]
            
            # distância da coordenada X dos nós de início e fim do laço:
            distancia = self.pos_x[fim] - self.pos_x[inicio]
            print(f'distancia: {distancia}')
            print(f'dif: {dif}')
            for d in dif:
                print(f'd:{d}')
                pesos_y[d] = round(0.15 * distancia, 2)

        return pesos_y

    # desenha as setas entre os nós:
    def __draw_arrow(self, ax, start, end, color='black', curvature=0, alpha=1): # Mudar a transparencia dependendo se vai ser mostrado algo ou não
        ax.annotate('', xy=end, xycoords='data', xytext=start, textcoords='data',
                    arrowprops=dict(arrowstyle="->", lw=1.5, color=color, shrinkA=13, shrinkB=12, connectionstyle=f"arc3,rad={curvature}", alpha=alpha))

    # Desenha as linhas de conexão entre os vértices:
    def __draw_connections(self, vetor_foco = [], alpha = 1): 
        
        if len(vetor_foco) != 0:
            
            for index, value in enumerate(vetor_foco):
                if index == len(vetor_foco) - 1:
                    continue
                
                for i in range(len(self.matriz)):
                    if i == value:    # [1, 2, 7, 1]
                        j = vetor_foco[index + 1]
                        
                        num_conexoes = self.matriz[i][j]

                        # coordenadas dos vértices:
                        start = self.pos[self.nos[i]]
                        end = self.pos[self.nos[j]]
                        
                        for k in range(num_conexoes):
                            curvature = 0.0
                            
                            # adiciona uma curvatura para 'entrar' nas ramificação do caminho de frente:
                            if k != 0 or abs(start[0] - end[0]) > 1 or ((i in self.principal) ^ (j in self.principal)) or ((start[0] - end[0]) > 0):
                                curvature = -0.5 if abs(start[0] - end[0]) > 0 else 0
                                if k > 1:
                                    curvature = -0.5 * k
                        
                            # Definindo as cores das conexões:
                            if j > i:   # triângulo superior
                                color='black' # Ligação para caminho a frente
                                self.__draw_arrow(self.ax, start, end, color, curvature=curvature, alpha=alpha) # Colocar a transparencia

                            if i > j or start[0] > end[0]:  # o triângulo inferior
                                color='red' # Ligação para realimentação
                                self.__draw_arrow(self.ax, start, end, color, curvature=curvature, alpha=alpha) # Colocar a transparência

        else:
            # Varredura das conexões por todos os vértices:
            for i in range(len(self.matriz)):
                for j in range(len(self.matriz)):
                    
                    if self.matriz[i][j] == 0:   # não tem conexão
                        continue
                    
                    num_conexoes = self.matriz[i][j]

                    # coordenadas dos vértices:
                    start = self.pos[self.nos[i]]
                    end = self.pos[self.nos[j]]
                    

                    for k in range(num_conexoes):
                        curvature = 0.0
                        
                        # adiciona uma curvatura para 'entrar' nas ramificação do caminho de frente:
                        if k != 0 or abs(start[0] - end[0]) > 1 or ((i in self.principal) ^ (j in self.principal)) or ((start[0] - end[0]) > 0):
                            curvature = -0.5 if abs(start[0] - end[0]) > 0 else 0
                            if k > 1:
                                curvature = -0.5 * k

                        # Definindo as cores das conexões:
                        if j > i:   # triângulo superior
                            color='black' # Ligação para caminho a frente
                            self.__draw_arrow(self.ax, start, end, color, curvature=curvature, alpha=alpha) # Colocar a transparencia

                        if i > j or start[0] > end[0]:  # o triângulo inferior
                            color='red' # Ligação para realimentação
                            self.__draw_arrow(self.ax, start, end, color, curvature=curvature, alpha=alpha) # Colocar a transparência
 
    # Desenha os nós
    def __draw_nodes(self, dict, zorder, alpha):
        for label, (x, y) in dict.items():
            self.ax.scatter(x, y, s=400, color='lightblue', edgecolor='black', zorder=zorder, alpha=alpha)  # Ponto do nó => O alpha define a
            self.ax.text(x, y, label, ha='center', va='center', fontsize=12, zorder=zorder, alpha=alpha)  # Rótulo do nó


    # ==================================================
    # MÉTODOS PÚBLICOS:

    # Plota o sistema:
    def draw(self):
        # Plotando o fluxo completo:
        self.__draw_nodes(self.pos, 1, self.transparencia[0])
        self.__draw_connections([], self.transparencia[0])
        
        plt.show()
    
    # Plota o caminho em destaque:
    def draw_caminho(self, vetor, valor):
        self.transparencia[0] = self.transparencia[0] / 5
        dep = vetor[valor]

        dep_d = dict()
        for value in dep:
            dep_d[self.nos[value]] = tuple([self.pos_x[value], self.pos_y[value]])
        
        # Plotando o caminho em destaque:
        self.__draw_nodes(dep_d, 2, self.transparencia[1])
        self.__draw_connections(dep, self.transparencia[1])
        
        # Plotando o fluxo completo:
        self.__draw_nodes(self.pos, 1, self.transparencia[0])
        self.__draw_connections([], self.transparencia[0])
        
        plt.show()

    
