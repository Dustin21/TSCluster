from IO import ImportFromCSV
from FeatureExtraction import FeatureExtraction

if __name__ == '__main__':
    data = ImportFromCSV("C:\\Users\\dustin.johnson\\PycharmProjects\\PowerfulInsightEngine\\data\\20170717_Kingston.csv").\
        read_csv()
    features = FeatureExtraction(data, is_tidy=False).\
        feature_select(column_id='UserID', column_sort='Time')
    features.to_csv("C:\\Users\\dustin.johnson\\PycharmProjects\\PowerfulInsightEngine\\data\\features.csv")
    print(features.shape)
