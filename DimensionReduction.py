from sklearn.manifold import TSNE


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

