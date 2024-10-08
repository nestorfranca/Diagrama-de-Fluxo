from sympy import Matrix

# Exemplo de matriz de adjacência com ganhos
matriz = Matrix([ [0, 1, 0, 1],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1],
                  [1, 0, 0, 0]])

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
