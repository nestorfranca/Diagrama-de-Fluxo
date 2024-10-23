from sistema import *

class Grafico:
    def __init__(self, sistema):
        self.sistema = Sistema(10)
        self.pesos_x = []
        self.pesos_y = []
        self.nos = []
        self.pos = {}
        self.caminhos_frente = self.sistema.caminhos
        self.ignora = None 
        self.max_len = 0
        self.conta_caminhos = 0

        self.__setup()

    def __setup(self):

        self.pesos_x, self.pesos_y = self.setPesos()

        self.nos = list(self.sistema.sinais.keys())
        # self.pos = dict([self.nos[i], (self.pesos_x[i], self.pesos_y[i])] for i in range(len(self.nos)))
        for i in range(len(self.nos)):
            self.pos[self.nos[i]] = (self.pesos_x[i], self.pesos_y[i])

        self.ignora = max(range(len(self.caminhos_frente)), key=lambda i: len(self.caminhos_frente[i]))
        self.max_len = len(self.caminhos_frente[self.ignora])
        self.conta_caminhos = sum(1 for caminho in self.caminhos_frente if len(caminho) == self.max_len)

    def setPesos(self):
        # Aplica os pesos em X
        pesos_x = len(self.sistema.matriz)*[-1]
        # [-1,- 1,- 1, ..., -1]

        pesos_y = len(self.sistema.matriz)*[None]

        #----------------------------------- Pesos em X -------------------------------------#

        # Muda os valores se eles estiverem no caminho principal
        for index, value in enumerate(self.caminhos_frente[self.ignora]):
            pesos_x[value] = index
        # [0, 1, 2, 3, 4, 5, -1, -1, -1, 6]

        # Para o caso de um segundo caminho a frente de mesmo tamanho com um indice
        for index, value in enumerate(self.caminhos_frente):
            if index == self.ignora:
                continue
            
            dif = list(set(self.caminhos_frente[index]) - set(self.caminhos_frente[self.ignora]))
            if dif == list():
                continue
            
            for i in value:
                if i == dif[0]:
                    anterior = value[i-1]
                    posterior = value[i+1]
                    pesos_x[i] = (anterior + posterior) / 2

        # [[1, 2, 3, 4, 6, 1], [3, 4, 7, 3], [5, 9, 8, 5]]
        # Vai ser os ganhos de laços
        ganhos_lacos = [[1, 2, 3, 4, 6, 1], [3, 4, 7, 3], [5, 9, 8, 5]]
        qnt_lacos = len(ganhos_lacos)

        for index, value in enumerate(ganhos_lacos):
            dif = list(set(ganhos_lacos[index]) - set(caminhos_frente[ignora]))
            # primeiro = ganhos_lacos[index][0]
            primeiro = pesos_x[ganhos_lacos[index][0]]
            for ind, i in enumerate(value):
                if i == dif[0] or ind == len(value) - 1:
                    continue
                ultimo = pesos_x[i]
            pesos_x[dif[0]] = (primeiro + ultimo) / 2 

        '''

        #----------------------------------- Pesos em Y -------------------------------------#
        '''
        # Preenche pesos_y
        pesos_y = len(matriz)*[None]
        # Aplica os pesos em Y
        for i in caminhos_frente[ignora]:
            pesos_y[i] = 0
        # [0, 0, 0, 0, 0, -1, -1, -1, 0]

        c = 0.5
        for index, value in enumerate(ganhos_lacos):
            dif = list(set(ganhos_lacos[index]) - set(caminhos_frente[ignora]))
            # primeiro = pesos_y[ganhos_lacos[index][0]]
            for ind, i in enumerate(value):
                if i == dif[0] or ind == len(value) - 1:
                    continue
                c -= 1
                # ultimo = pesos_y[i]
            pesos_y[dif[0]] = c / 2
            c = 0.5
                    
        # Caminho do mesmo tamanho do maior, porém com outros indices
        for index, value in enumerate(caminhos_frente):
            if index != ignora and len(caminhos_frente[index]) == max_len:
                dif = list(set(caminhos_frente[index]) - set(caminhos_frente[ignora]))
                if dif != None:
                    for i in dif:
                        pesos_y[i] == 1  
        return pesos_x, pesos_y


    def draw_arrow(self, ax, start, end, color='black', curvature=0, alpha=1): # Mudar a transparencia dependendo se vai ser mostrado algo ou não
        ax.annotate('', xy=end, xycoords='data', xytext=start, textcoords='data',
                    arrowprops=dict(arrowstyle="->", lw=1.5, color=color, shrinkA=13, shrinkB=12, connectionstyle=f"arc3,rad={curvature}", alpha=alpha))