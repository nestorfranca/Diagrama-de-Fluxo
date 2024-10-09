import graphviz
from IPython.display import Image, display

dot = graphviz.Digraph()

# Define a direção do gráfico: Left to Right e espaçamento entre nós e arestas
# dot.attr(nodesep='1.0')

matriz = [
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
]


# Criação dos nós
dot.node('R', 'R')
dot.node('C', 'C')
# Agrupando os nós intermediários em sequência, para que fiquem em ordem
with dot.subgraph() as sg:
    sg.attr(rank='same')
    for i in range(1, len(matriz) - 1):
        sg.node('V' + str(i), 'V' + str(i))

# Gera as ligações diretas na ordem R -> V1 -> V2 -> ... -> C
for i in range(len(matriz)):
    for j in range(len(matriz)):
        if i == 0 and j > i and matriz[i][j] == 1 and j != len(matriz) - 1:
            dot.edge('R', 'V' + str(j), constraint = 'true')
        elif i == 0 and matriz[i][j] == 1 and j == len(matriz) - 1:
            dot.edge('R', 'C', constraint = 'true')
        elif i != 0 and j > i and matriz[i][j] == 1 and j != len(matriz) - 1:
            dot.edge('V' + str(i), 'V' + str(j), constraint = 'true')
        elif i != 0 and j > i and matriz[i][j] == 1 and j == len(matriz) - 1:
            dot.edge('V' + str(i), 'C', constraint = 'true')

# Gera as realimentações com linhas tracejadas e cor vermelha
for i in range(len(matriz)):
    for j in range(len(matriz)):
        if i == len(matriz) - 1 and j == 0 and matriz[i][j] == 1:
            dot.edge('C', 'R', style='dashed', color='red', constraint = 'false')
        elif i == len(matriz) - 1 and i > j and matriz[i][j] == 1:
            dot.edge('C', 'V' + str(j), style='dashed', color='red', constraint = 'false')
        elif i != len(matriz) - 1 and i > j and j == 0 and matriz[i][j] == 1:
            dot.edge('V' + str(i), 'R', style='dashed', color='red', constraint = 'false')
        elif i != len(matriz) - 1 and i > j and matriz[i][j] == 1 and j != 0:
            dot.edge('V' + str(i), 'V' + str(j), style='dashed', color='red', constraint = 'false')

# Renderiza diretamente no formato PNG e exibe
image_data = dot.pipe(format='png')
display(Image(image_data))