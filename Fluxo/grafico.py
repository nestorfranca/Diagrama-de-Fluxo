import math, numpy as np
import matplotlib.pyplot as plt
from sistema import *

class Grafico:
    # def __init__(self, num_sinais, matriz, sinais, caminhos, lacos):
    def __init__(self, sistema):
        self.num_sinais = sistema.num_sinais
        self.matriz = sistema.matriz
        self.matriz_poly = sistema.matriz_poly
        self.pos_x = []
        self.pos_y = []
        self.nos = []
        self.pos = {}
        self.sinais = sistema.sinais
        self.caminhos = sistema.caminhos
        self.lacos = sistema.lacos
        self.ganho_lacos = sistema.ganho_lacos
        self.principal = None 
        self.max_len = 0
        self.conta_caminhos = 0

        self.ax = None
        self.transparencia = [0.2, 1]

        self.setup()

    # ==================================================
    # MÉTODOS PRIVADOS:

    # Configurações da classe:
    def setup(self):

        self.principal = max(self.caminhos, key=lambda caminho: len(caminho))
        self.max_len = len(self.principal)
        self.conta_caminhos = sum(1 for caminho in self.caminhos if len(caminho) == self.max_len)
        
        self.pos_x = self.define_pos_X()
        self.pos_y = self.define_pos_Y()

        self.nos = list(self.sinais.keys())
        # self.pos = dict([self.nos[i], (self.pos_x[i], self.pos_y[i])] for i in range(len(self.nos)))
        for i in range(len(self.nos)):
            self.pos[self.nos[i]] = (self.pos_x[i], self.pos_y[i])
    
    def gera_plot(self):
        # Criar a figura e remove os eixos:
        fig, self.ax = plt.subplots(figsize=(len(self.matriz), len(self.matriz)));
        
        # define o limite Y com base na maior altura possível de ocorrer:
        limite = self.pos_x[-1]/2
        self.ax.set_aspect('equal');
        # plt.grid()
        plt.ylim(-limite*1.25, limite*1.25); # Colocar o menor e maior peso para y
        self.ax.set_axis_off()

    # Define coordenada X dos nós:
    def define_pos_X(self):
        # Inicializa as posições do eixo X em "-1":
        pesos_x = len(self.matriz)*[-1]
        # [-1,- 1,- 1, ..., -1]

        # Define o maior caminho de frente como o caminho principal:
        for index, value in enumerate(self.principal):
            pesos_x[value] = float(index)   # posição X é equivalente ao índice no vetor
        # [0, 1, 2, 3, 4, 5, -1, -1, -1, 6]

        # Define posição do eixo X das ramificações do caminho de frente principal:
        for value in self.caminhos:
            
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
    def define_pos_Y(self):
        # Inicializa as posições do eixo Y em "None":
        pesos_y = len(self.matriz)*[None]

        # Aplica os pesos em Y
        # Define posição Y do maior caminho de frente como 0:
        for i in self.principal:
            pesos_y[i] = 0
        # [0, 0, 0, 0, 0, 0, None, None, None, 0]

        # Define posição do eixo Y das ramificações do caminho de frente principal:
        for value in self.caminhos:
            
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
                pesos_y[d] = round(0.5 * distancia, 2)

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

                # [1, 3, 4, 7, 1]
                if v == dif[-1]:
                    fim = value[i+1]
            
            # distância da coordenada X dos nós de início e fim do laço:
            distancia = self.pos_x[fim] - self.pos_x[inicio]
            for d in dif:
                pesos_y[d] = round(0.5 * distancia, 2)

        return pesos_y

    # desenha as setas entre os nós:
    def draw_arrow(self, ganho, ax, start, end, color='black', curvature=0, alpha=1): # Mudar a transparencia dependendo se vai ser mostrado algo ou não
        ax.annotate('', xy=end, xycoords='data', xytext=start, textcoords='data',
                    arrowprops=dict(arrowstyle="->", lw=1.5, color=color, shrinkA=13, shrinkB=12, connectionstyle=f"arc3,rad={curvature}", alpha=alpha))
        
        # Texto:
        altura = -(curvature * (math.dist(start, end)) / 2)
        deg = math.atan2((end[1] - start[1]), (end[0] - start[0]))

        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2

        text_pos_x = mid_x
        text_pos_y = mid_y
        if curvature == 0:
            text_pos_x = mid_x
            text_pos_y = mid_y #+ 0.1

        else:
            if deg != 0 and deg != math.pi:
                text_pos_x = mid_x - altura*math.sin(deg) #+ (0.1 if math.tan(deg) > 0 else -0.1)
            
            text_pos_y = mid_y + altura*math.cos(deg) #+ (0.1 if math.cos(deg) > 0 else -0.1)

        
        ax.annotate(pretty(ganho), 
            xy=end,       # Ponto final da seta
            xytext=(text_pos_x, text_pos_y),   # Posição do texto no meio da seta
            # xytext=(mid_x, mid_y),   # Posição do texto no meio da seta
            ha='center', va='center',
            fontsize=5,  # Tamanho da fonte
            color='black',  # Cor do texto
            fontweight='bold',  # Estilo do texto (negrito)
            bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3', alpha=0.75))  # Estilo da caixa

    # Desenha as linhas de conexão entre os vértices:
    def draw_connections(self, vetor_foco = [], alpha = 1): 
        
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
                        
                        # for k in range(num_conexoes):
                        curvature = 0.0
                        G = self.matriz_poly[i][j]
                        
                        # curvatura para ramificações do caminho de frente:
                        if (end[0] - start[0]) > 1 or ((i in self.principal) ^ (j in self.principal)):
                            curvature = -0.5
                        
                        # curvatura para laços:
                        if (end[0] - start[0]) < 0 and ((i in self.principal) or (j in self.principal)):
                            curvature = -0.5

                        # Definindo as cores das conexões:
                        if start[0] < end[0]:   # Ligação para caminho a frente
                            color='black'
                        elif start[0] > end[0]:  # Ligação para realimentação
                            color='red'
                        
                        self.draw_arrow(G, self.ax, start, end, color, curvature=curvature, alpha=alpha) # Colocar a transparência

        else:
            # Varredura das conexões por todos os vértices:
            for i in range(len(self.matriz)):
                for j in range(len(self.matriz)):
                    
                    if self.matriz[i][j] == 0:   # não tem conexão
                        continue
                    
                    # coordenadas dos vértices:
                    start = self.pos[self.nos[i]]
                    end = self.pos[self.nos[j]]
                    

                    curvature = 0.0
                    G = self.matriz_poly[i][j]
                    
                    # curvatura para ramificações do caminho de frente:
                    if (end[0] - start[0]) > 1 or ((i in self.principal) ^ (j in self.principal)):
                        curvature = -0.5
                    
                    # curvatura para laços:
                    if (end[0] - start[0]) < 0 and ((i in self.principal) or (j in self.principal)):
                        curvature = -0.5

                    # Definindo as cores das conexões:
                    if start[0] < end[0]:   # Ligação para caminho a frente
                        color='black' 

                    elif start[0] > end[0]:  # Ligação para realimentação
                        color='red'
                    
                    self.draw_arrow(G, self.ax, start, end, color, curvature=curvature, alpha=alpha) # Colocar a transparência
 
    # Desenha os nós
    def draw_nodes(self, dict, zorder, alpha):
        for label, (x, y) in dict.items():
            self.ax.scatter(x, y, s=400, color='lightblue', edgecolor='black', zorder=zorder, alpha=alpha)
            self.ax.text(x, y, label, ha='center', va='center', fontsize=12, zorder=zorder, alpha=alpha)


    # ==================================================
    # MÉTODOS PÚBLICOS:

    # Plota o sistema:
    def draw(self):
        # Plotando o fluxo completo:
        self.draw_nodes(self.pos, 1, self.transparencia[1])
        self.draw_connections([], self.transparencia[1])
        
        plt.show()
    
    # Plota o caminho em destaque:
    def draw_caminho(self, vetor, valor):
        dep = vetor[valor]

        dep_d = dict()
        for value in dep:
            dep_d[self.nos[value]] = tuple([self.pos_x[value], self.pos_y[value]])
        
        # Plotando o caminho em destaque:
        self.draw_nodes(dep_d, 2, self.transparencia[1])
        self.draw_connections(dep, self.transparencia[1])
        
        # Plotando o fluxo completo:
        self.draw_nodes(self.pos, 1, self.transparencia[0])
        self.draw_connections([], self.transparencia[0])
        
        plt.show()