from sympy import Matrix, pretty
from time import sleep

# Exemplo de matriz de adjacência com ganhos
matriz = Matrix([ [0, 1, 0, 1],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1],
                  [1, 0, 0, 0]])

print(pretty(matriz))
def encontrar_lacos(matriz):
    lacos = []

    # Número de nós
    n = matriz.shape[0]

    # Percorrer todos os nós para identificar laços
    for i in range(n):
        # Verificar se existe um laço começando e terminando em i
        if matriz[i, i] != 0:
            lacos.append([i])

        # Verificar laços com mais de um nó
        for j in range(n):
            if matriz[i, j] != 0:  # Conexão de i para j
                for k in range(n):
                    if matriz[j, k] != 0 and k == i:  # Laço retornando para i
                        lacos.append([i, j, k])

    return lacos

# Encontrar laços e seus ganhos
lacos = encontrar_lacos(matriz)

# Exibir os laços e os ganhos correspondentes
for i in range(len(lacos)):
    print(f"Laço: {lacos[i]}")


from itertools import combinations, chain


v = [[1, 2, 3, 2], [2, 3, 2], [4, 5, 4]]

vv = [[1], [2], [3], [4]]

comb = list(chain.from_iterable(
    combinations(vv, r) for r in range(1, len(vv) + 1)
))

print(comb)