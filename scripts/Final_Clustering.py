import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
import warnings
warnings.filterwarnings("ignore", message="KMeans is known to have a memory leak")
warnings.filterwarnings("ignore", message="indexing past lexsort depth may")


### SETTING ###

RPT_MODE = "0.1C"

time_lower = 6
time_upper = 14

SOC_Range = [9,10,11,12]

###############
SOC_Range = [str(i) for i in SOC_Range]


Data = pd.read_csv("data/output/pulse/Final_Point_Data.csv", index_col = (0,1,2,3))

X = Data.loc[RPT_MODE, "0":"16"]
Y = Data.loc[RPT_MODE, "SOH"].groupby(level = ["Path", "Number"]).mean()
X_seek = X.loc[X.index.get_level_values('Time').isin(range(time_lower, time_upper+1, 2)), SOC_Range]


X_group = X_seek.groupby(level = ["Path","Number"])

X_mean = X_group.mean()
X_std = X_group.std()

Cells = X_std.index


n_clusters = range(1,11)

J = []
Labels = []
Centers = []
SOH_ERROR = np.zeros(len(n_clusters))
for i in n_clusters :
    kmeans = KMeans(n_clusters = i, random_state = 42, n_init = 'auto')
    kmeans.fit(X_std)
    
    
    for j in range(i) :
        Cell_cluster = Y[kmeans.labels_ == j]
        SOH_MSE = ((Cell_cluster - Cell_cluster.mean())**2).sum()
        SOH_ERROR[i-1] += SOH_MSE
    
    J.append(kmeans.inertia_)
    Labels.append(kmeans.labels_)   
    Centers.append(kmeans.cluster_centers_)


fig = plt.figure(1, figsize = (12, 6))
gs = fig.add_gridspec(1,2)
ax = [fig.add_subplot(gs[i]) for i in range(2)]


ax[0].plot(n_clusters, J)
ax[0].set_xlabel("N_clusters")
ax[0].set_ylabel("J")


ax[1].plot(n_clusters, SOH_ERROR)
ax[1].set_xlabel("N_clusters")
ax[1].set_ylabel("SOH_ERROR_SUM")

WCSS = pd.DataFrame(data = {"WCSS": J}, index = n_clusters)
WCSS.to_csv("data/output/clustering/Within Cluster Sum of Square.csv")

plt.show()

Good_n_clusters = input("Enter the Best N_clusters : ")
Good_n_clusters = int(Good_n_clusters)

Good_label = Labels[Good_n_clusters-1]

sorted_label = [2, 1, 3, 0]

Good_sorted_label = np.zeros_like(Good_label)
for idx, cluster in enumerate(sorted_label) :
    Good_sorted_label[Good_label == cluster] = idx
    

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_std)

lda = LinearDiscriminantAnalysis(n_components=2)
X_lda = lda.fit_transform(X_std, Good_sorted_label)

color_dict = {0 : "blue",
              1 : "orange",
              2 : "red",
              3 : "green"}


fig = plt.figure(2, figsize = (8, 8))
ax = fig.add_subplot()


tree = DecisionTreeClassifier(
    criterion = "entropy",
    random_state = 427
)

tree.fit(X_pca, Good_sorted_label)


for cluster in range(Good_n_clusters) :
    X_cluster = X_pca[Good_sorted_label == cluster]
    
    ax.scatter(X_cluster[:,0], X_cluster[:, 1], color = color_dict[cluster], label = "Cluster " + str(cluster + 1))
    
ax.set_xlabel(r"PCA 1 (=$\Delta\eta^*$)", fontsize = 14)
ax.set_ylabel("PCA 2", fontsize = 14)
ax.legend()

pca1_lim = ax.get_xlim()
pca2_lim = ax.get_ylim()

mesh_x = np.linspace(pca1_lim[0], pca1_lim[1], 100)
mesh_y = np.linspace(pca2_lim[0], pca2_lim[1], 100)

mesh_X, mesh_Y = np.meshgrid(mesh_x, mesh_y)

mesh_X = mesh_X[:, :, np.newaxis]
mesh_Y = mesh_Y[:, :, np.newaxis]

mesh = np.concatenate((mesh_X, mesh_Y), axis = 2)
mesh = mesh.transpose(2,0,1)
mesh = mesh.reshape(2, -1)
mesh = mesh.transpose()

tree_pred = tree.predict(mesh)
tree_pred = tree_pred.reshape(100, 100)

mesh_X = np.squeeze(mesh_X)
mesh_Y = np.squeeze(mesh_Y)

contour = ax.contourf(mesh_X, mesh_Y, tree_pred, alpha = 0.2)

boundary = []
for j in range(99) :
        if (tree_pred[:, j] != tree_pred[:, j+1]).any() :
            boundary.append(j)
    
boundary_value = [mesh_x[value] for value in boundary]




fig = plt.figure(3)
ax = fig.add_subplot()


for idx in range(Good_n_clusters) :
    Cells_in_idx = Cells[Good_sorted_label == idx]
    difference = X_std.loc[Cells_in_idx.to_list()] - Centers[Good_n_clusters - 1][sorted_label[idx]]
    distances = (difference**2).sum(axis=1)
    low_distances = distances.sort_values(ascending = True).head(5)
    
    ax.scatter(Cells_in_idx.get_level_values('Number'), Y[Cells_in_idx])
    
    Cell_for_core = low_distances.index.to_numpy()
    Cell_for_random = np.random.choice(Cells_in_idx, size = 3, replace = False)
    
    print("Cluster", idx+1, ":", len(Cells_in_idx))
    print("Core Choice   : ", Cell_for_core)
    print("Random Choice : ", Cell_for_random)
    print()

ax.set_xlabel("Cell Number")
ax.set_ylabel("SOH")

Compact_Result = pd.DataFrame({"Culster" : Good_sorted_label + 1,
                                "LDA 1" : X_lda[:,0],
                                "PCA 1" : X_pca[:,0],
                                "SOH" : Y}, index = Y.index)

Compact_Result = Compact_Result.reorder_levels((1,0)).sort_index()

plt.show()

Compact_Result.to_csv("data/output/clustering/Clustering Result.csv")






