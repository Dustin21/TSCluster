import pyodbc
import pandas as pd


class ImportFromSQLServer:

    def __init__(self, server, db, sql_query):
        self.server = server
        self.db = db
        self.sql_query = sql_query

    def submit_query(self):
        conn = (
            r'Driver={SQL Server};'
            r'Server=' + self.server + ';'
            r'Database=' + self.db + ';'
            r'Trusted_Connection=yes;'
        )
        connection = pyodbc.connect(conn)
        dat = pd.read_sql(self.sql_query, connection)
        df = pd.DataFrame(dat).set_index('UserID')
        return df


class ImportFromCSV:

    def __init__(self, filename):
        self.filename = filename

    def read_csv(self, index_name='UserID', header=0):
        if index_name is not None:
            df = pd.read_csv(self.filename, delimiter=',', header=header).\
                set_index(index_name)
            return df
        else:
            df = pd.read_csv(self.filename, delimiter=',', header=header)
            return df
