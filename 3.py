# coding=utf-8
import matplotlib.pyplot as plt

import seaborn as sns
sns.set(style='whitegrid')

# Сферические кластеры
from sklearn.datasets import make_blobs
X, y = make_blobs(n_samples = 150, n_features=2, centers=3,
 cluster_std=0.5, shuffle=True, random_state=0)
plt.scatter(X[:, 0], X[:, 1], c='lightgreen', marker='o', s=100)
plt.grid() # прячет сетку с sns.set(style='whitegrid')

'1'
plt.show()


from sklearn.cluster import KMeans
#2
km = KMeans(n_clusters=3, init='random', n_init=10,
max_iter=300, tol=1e-04, random_state=0)
y_km = km.fit_predict(X)
plt.scatter(X[y_km == 0, 0], X[y_km == 0, 1],
s=100, c='lightgreen', marker='s', label=u'кластер 1')
plt.scatter(X[y_km == 1, 0], X[y_km == 1, 1],
s=100, c='orange', marker='o', label=u'кластер 2')
plt.scatter(X[y_km == 2, 0], X[y_km == 2, 1],
s=100, c='lightblue', marker='v', label=u'кластер 3')
plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1],
s=250, c='red', marker='*', label=u'центроиды')
plt.legend()
#plt.grid() # прячет сетку с sns.set(style='whitegrid')

#plt.show()


#3
km = KMeans(n_clusters=3, init='k-means++', n_init=10,
max_iter=300, random_state=0)
y_km = km.fit_predict(X)

distorts = [] # внутрикластерные искажения (инерции) (SSE)
for i in range(1, 11):
    km = KMeans(n_clusters=i, init='k-means++',
    n_init=10, max_iter=300, random_state=0)
    km.fit(X)
    distorts.append(km.inertia_)

plt.plot(range(1, 11), distorts, marker='o')
plt.xlabel(u'Число кластеров')
plt.ylabel(u'Искажение')
plt.show()


#4
from sklearn.cluster import AgglomerativeClustering
ac = AgglomerativeClustering(n_clusters=3,
affinity='euclidean', linkage='complete')
y_ac = ac.fit_predict(X)
plt.scatter(X[y_ac == 0, 0], X[y_ac == 0, 1],
s=100, c='lightgreen', marker='o', label=u'кластер 1')
plt.scatter(X[y_ac == 1, 0], X[y_ac == 1, 1],
s=100, c='orange', marker='s', label=u'кластер 2')
plt.scatter(X[y_ac == 2, 0], X[y_ac == 2, 1],
s=100, c='lightblue', marker='v', label=u'кластер 3')
plt.legend()
plt.show()


#5
# Кластеры-полумесяцы
from sklearn.datasets import make_moons
X, y = make_moons(n_samples=200, noise=0.05, random_state=0)
plt.scatter(X[:, 0], X[:, 1], c='orange', marker='o', s=100)
#plt.grid() # прячет сетку с sns.set(style='whitegrid')
plt.show()


6
from sklearn.cluster import DBSCAN
db = DBSCAN(eps=0.2, min_samples=5, metric='euclidean')

y_db = db.fit_predict(X)
plt.scatter(X[y_db == 0, 0], X[y_db == 0, 1],
s=100, c='lightblue', marker='o', label=u'кластер 1')
plt.scatter(X[y_db == 1, 0], X[y_db == 1, 1],
s=100, c='red', marker='s', label=u'кластер 2')

plt.legend()
plt.show()


#7
# Сферические кластеры 3д
from sklearn.datasets import make_blobs
X, y = make_blobs(n_samples = 150, n_features=3, centers=3,
    cluster_std=0.5, shuffle=True, random_state=0)
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(X[:, 0], X[:, 1], X[:, 2], c='orange', marker='o', s=100)
plt.show()


from sklearn.cluster import KMeans
X, y = make_blobs(n_samples = 150, n_features=3, centers=3,
    cluster_std=0.5, shuffle=True, random_state=0)
km = KMeans(n_clusters=3, init='random', n_init=10,
max_iter=300, tol=1e-04, random_state=0)
y_km = km.fit_predict(X)

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(X[y_km == 0, 0], X[y_km == 0, 1], X[y_km == 0, 2],
           s=100, c='lightgreen', marker='s', label=u'кластер 1')
ax.scatter(X[y_km == 1, 0], X[y_km == 1, 1], X[y_km == 1, 2],
           s=100, c='orange', marker='o', label=u'кластер 2')
ax.scatter(X[y_km == 2, 0], X[y_km == 2, 1], X[y_km == 2, 2],
           s=100, c='lightblue', marker='v', label=u'кластер 3')
ax.scatter(km.cluster_centers_[:, 0],km.cluster_centers_[:, 1],
           km.cluster_centers_[:, 2],s=350, c='red', marker='*',
           label=u'центроиды')
plt.legend()
plt.show()
