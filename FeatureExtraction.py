from PrepareData import Prepare
from tsfresh import select_features
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute


class FeatureExtraction:

    def __init__(self, data, is_tidy=False):
        self.data = data
        self.is_tidy = is_tidy

    def feature_extract(self, column_id='UserID', column_sort='Time'):
        if not self.is_tidy:
            data_tidy = Prepare(self.data).tidy_data(id_vars=column_id, var_name=column_sort)
            extracted_features = extract_features(data_tidy,
                                                  column_id=column_id,
                                                  column_sort=column_sort)
            return extracted_features
        else:
            extracted_features = extract_features(self.data,
                                                  column_id=column_id,
                                                  column_sort=column_sort)
            return extracted_features

    def feature_select(self, column_id='UserID', column_sort='Time'):
        features = self.feature_extract(column_id, column_sort)
        features_imputed = impute(features)
        return features_imputed
