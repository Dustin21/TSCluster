from sklearn.manifold import TSNE
import os

class DimensionReduction:

    def __init__(self, data):
        self.data = data

    def run_tsne(self, perplexity, dim=2):
        if type(perplexity) is list:
            x_embedded = []
            for perp in perplexity:
                tsne = TSNE(n_components=dim, perplexity=perp).fit_transform(self.data)
                x_embedded.append(tsne)
            return x_embedded

        elif type(perplexity) is float:
            x_embedded = TSNE(n_components=dim, perplexity=perplexity).fit_transform(self.data)
            return x_embedded

        elif perplexity is None:
            x_embedded = TSNE(n_components=dim, perplexity=30.0).fit_transform(self.data)
            return x_embedded

    def run_largevis(self):
        path = 'outputs/clean_minmaxNormalized_features.csv'
        if os.path.isfile(path):
            os.system("start /wait cmd /c C:/Program Files/R/R-3.3.2/bin/Rscript.exe " +
                      "C:\Users\dustin.johnson\PycharmProjects\PowerfulInsightEngine" +
                      "\Rscripts\Dimension_Reduce_Optimized.R")
        else:
            print("File required by R does not exist.")
            exit(1)




