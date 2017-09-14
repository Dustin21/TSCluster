from sklearn import preprocessing
import numpy as np
import pandas as pd


class Prepare:

    def __init__(self, data):
        self.data = data

    @staticmethod
    def __drop_vars(data, index_id):
        dropped_index = data.drop(index_id, axis=1)
        features_dropped = dropped_index.loc[:, (dropped_index.std(axis=0) > 0.01)]
        features_dropped = pd.DataFrame(features_dropped)
        features_dropped[index_id] = data[index_id].reset_index(drop=True)
        return features_dropped

    def tidy_data(self, id_vars='UserID', var_name='Time'):
        data_melt = self.data.melt(id_vars=id_vars, var_name=var_name). \
            sort_values([id_vars, var_name]). \
            dropna()
        return data_melt

    def process_data(self, norm_type='z_norm', index_id='UserID', use_index=False, drop_null_features=True):
        if drop_null_features:
            data_drop_na = self.__drop_vars(self.data, index_id).\
                dropna()
        else:
            data_drop_na = self.data.\
                dropna()

        data_filter = data_drop_na[data_drop_na.astype('bool').mean(axis=1) > 0.1]

        if norm_type == 'z_norm':
            norm = preprocessing.normalize(data_filter.drop(index_id, axis=1), axis=0)
            norm = pd.DataFrame(norm)
            norm[index_id] = data_filter[index_id].reset_index(drop=True)
            norm.columns = data_drop_na.columns
            if use_index:
                norm.set_index(index_id, inplace=True)
            return norm
        elif norm_type == 'minmax':
            norm = preprocessing.minmax_scale(data_filter.drop(index_id, axis=1), axis=0)
            norm = pd.DataFrame(norm)
            norm[index_id] = data_filter[index_id].reset_index(drop=True)
            norm.columns = data_drop_na.columns
            if use_index:
                norm.set_index(index_id, inplace=True)
            return norm
        else:
            print("You have selected no normalization.")
            print("z_norm: Z-normalization")
            print("min_max: Min Max scaling")
            data_filter.set_index(index_id, inplace=True)
            return data_filter
