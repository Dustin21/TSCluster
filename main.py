from IO import ImportFromCSV
from FeatureExtraction import FeatureExtraction
from PrepareData import Prepare

# if __name__ == '__main__':
#     data = ImportFromCSV("data\\20170717_KingstonHydro_ELEC_FULL.csv").\
#         read_csv()
#     data_clean = Prepare(data).process_data(norm_type=None)
#     del data
#     features = FeatureExtraction(data_clean, is_tidy=False).\
#         feature_select(column_id='UserID', column_sort='Time')
#     features.to_csv("data\\features.csv")
#     print(features.shape)

feature_data = ImportFromCSV("data/features.csv").read_csv(index_name=None)

feature_normalized = Prepare(feature_data).\
    process_data(norm_type=None, index_id='id', use_index=True)

# feature_normalized.to_csv("data\\clean_unNormalized_features.csv")

from DimensionReduction import DimensionReduction

test = DimensionReduction(feature_normalized).run_tsne(perplexity=30.0)

print(test)