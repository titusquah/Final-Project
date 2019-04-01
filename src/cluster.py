import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pandas.plotting import scatter_matrix
from sklearn import manifold
from surface_interpolator import interpolated_sample

data = interpolated_sample()

#mds = manifold.MDS(n_components=2, max_iter=500)
tsne = manifold.TSNE(n_components=2)
pos = tsne.fit_transform(data)

plt.scatter(pos[80:, 0], pos[80:, 1], color='k')
plt.scatter(pos[:-80, 0], pos[:-80, 1], color='g')
plt.show()
