import matplotlib.pyplot as plt
import numpy as np
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D

# Função da curva (parábola)
x = np.linspace(0, 10, 100)
y = 0.1 * (x - 5)**2  # curva parabólica

# Crie o gráfico da curva
plt.plot(x, y, 'b-')  # curva azul

# Escolha o ponto intermediário da curva (por exemplo, no meio da lista de pontos)
idx = len(x) // 2

# Texto a ser colocado
texto = "Texto na curva"

# Transforme o texto em um caminho de texto
text_path = TextPath((0, 0), texto, size=0.5)

# Calcule o ângulo da tangente no ponto escolhido
angle = np.arctan2(y[idx + 1] - y[idx], x[idx + 1] - x[idx])

# Use Affine2D para rotacionar o texto de acordo com a curva e posicioná-lo no ponto escolhido
trans = Affine2D().rotate(angle).translate(x[idx], y[idx])
patch = PathPatch(trans.transform_path(text_path), color='black', lw=1)

# Adicione o texto ao gráfico
plt.gca().add_patch(patch)

# Ajustes do gráfico
plt.xlim(0, 10)
plt.ylim(0, 3)
plt.gca().set_aspect('equal', adjustable='box')

# Mostre o gráfico
plt.show()
