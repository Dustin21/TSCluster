import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap


class Visualizations:

    def __init__(self, data, labels):
        self.data = data
        self.labels = labels

    def scatter_3d(self, plot_name):
        x = self.data['X1']
        y = self.data['X2']
        z = self.data['X3']
        colors = LinearSegmentedColormap('colormap', cm.jet._segmentdata.copy(), np.max(self.labels))
        cs = [colors(i) for i in self.labels]

        fig = plt.figure(figsize=(8, 8))
        ax = fig.gca(projection='3d')
        scatter = ax.scatter(x, y, z, s=0.5, c=cs, edgecolors='none')
        ax.set_xlabel('X1')
        ax.set_ylabel('X2')
        ax.set_zlabel('X3')
        azim = 135
        elev = 25
        ax.view_init(elev, azim)

        plt.savefig(plot_name)
        plt.show()

    def pairs_plot(self, plot_name):
        labels = pd.DataFrame(self.labels)
        df = pd.concat([self.data.reset_index(drop=True), labels], axis=1)
        df.columns = ['X1', 'X2', 'X3', 'clusters']
        sns.set(style='ticks')
        sns_plot = sns.pairplot(df, hue="clusters", plot_kws={"s": 1},
                                vars=["X1", "X2", "X3"], diag_kind="kde",
                                palette="husl", size=5)
        sns_plot.savefig(plot_name)

    def pairs_density_plot(self, plot_name):
        sns.set(style="white")
        g = sns.PairGrid(self.data, diag_sharey=False)
        g.map_lower(sns.kdeplot, cmap="Blues_d")
        g.map_upper(plt.scatter)
        g.map_diag(sns.kdeplot, lw=3)
        g.savefig(plot_name)
