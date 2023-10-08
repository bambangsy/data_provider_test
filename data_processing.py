import pandas as pd

class Table:

    def setdata_as_df(self,data):
        self.df  = data

    def readCSV(self, file):
        self.df = pd.read_csv(file, sep=';', header=0)


    def removetop(self, top):
        self.df = self.df.drop(range(top))
        return self.df

    def remove_index(self):
        self.df = self.df.reset_index(drop=True)
        return self.df

    def add_id(self):
        # Add an ascending ID to the "NO" column for rows where "TYPE" is not NaN
        self.df['ID'] = self.df['TYPE'].notna().cumsum()
       

    def add_asc_id(self):
        self.df['ID'] = range(1, len(self.df) + 1)

    def add_monocolumn(self,colname,value):
        self.df[colname] = value

    def set_header_from_first_row(self):
        self.df.columns = self.df.iloc[0]
        self.df = self.df.iloc[1:]
        return self.df

    def remove_rows_with_nan(self, column_name):
        # Remove rows where the specified column has NaN values
        self.df = self.df.dropna(subset=[column_name])
        return self.df

    def rename_column(self, current_column_name, new_column_name):
        # Rename a specific column
        self.df = self.df.rename(columns={current_column_name: new_column_name})

    def display(self):
        print(self.df)
class TableSelect:
    def __init__(self, data):
        self.df = data

    def select_column(self, column_name):
        self.df = self.df[column_name]
        return self.df

    def display(self):
        print(self.df)

# Create an instance of the Table class and perform DataFrame operations


def getTable(data):
    file = Table()
    file.readCSV(data['data'])
    file.removetop(3)
    file.remove_index()
    file.set_header_from_first_row()
    file.add_monocolumn('LOCATION',data['name'])
    return file.df

def combineTable(dfs):
    # Use pd.concat to combine the DataFrames vertically (along rows)
    combined_df = pd.concat(dfs, axis=0)

    # Reset the index of the combined DataFrame
    combined_df.reset_index(drop=True, inplace=True)
    combined_df = combined_df.copy()  # Make a copy to avoid modifying the original DataFrames
    combined_df['ID'] = combined_df['TYPE'].notna().cumsum()
    return combined_df



def splitTable(file):
    data2 = TableSelect(file)
    data2 = data2.select_column(['ID','LAYANAN','IP LAYANAN','HOSTNAME LAYANAN'])
    file2 = Table()
    file2.setdata_as_df(data2)
    file2.rename_column('ID','STORAGE_ID')
    file2.add_asc_id()
    file.dropna(subset=['TYPE'])
    return file, file2.df


senayan = {'name':'senayan',
           'data':'senayan.csv'}
sigma = {'name':'sigma',
           'data':'sigma.csv'}
tamantekno = {'name':'tamantekno',
           'data':'tamantekno.csv'}

senayanTable = getTable(senayan)
sigmaTable = getTable(sigma)
tamanteknoTable = getTable(tamantekno)
combined_dc = combineTable([senayanTable,sigmaTable,tamanteknoTable])

server, layanan = splitTable(combined_dc)



class Cluster:
    x = []
    y = []
    z = []



#CLUSTER MODEL 1
def cluster_model_1(df, location):
    # Filter the DataFrame by the 'LOCATION' parameter
    filtered_df = df[df['LOCATION'] == location].copy()  # Make a copy to avoid SettingWithCopyWarning

    # Perform data transformations on the copied DataFrame
    filtered_df['KAPASITAS TB'] = filtered_df['KAPASITAS TB'].str.replace(',', '.').apply(pd.to_numeric, errors='coerce').fillna(0).astype(float)
    filtered_df['USAGE TB'] = filtered_df['USAGE TB'].str.replace(',', '.').apply(pd.to_numeric, errors='coerce').fillna(0).astype(float)

    # Perform aggregation on the copied DataFrame
    aggregated_data = filtered_df.groupby('TIPE').agg({'KAPASITAS TB': 'sum', 'USAGE TB': 'sum'}).reset_index()

    # Create a Cluster object and populate its attributes
    cluster = Cluster()
    cluster.x = aggregated_data['TIPE'].tolist()
    cluster.y = aggregated_data['KAPASITAS TB'].tolist()
    cluster.z = aggregated_data['USAGE TB'].tolist()

    return cluster

# cluster 1
location = 'senayan'  # Change this to the desired location
cluster1 = cluster_model_1(server, location)
cluster1 = {'x': cluster1.x,
            'y': cluster1.y,
            'z': cluster1.z}

# cluster 2
location = 'sigma'  # Change this to the desired location
cluster2 = cluster_model_1(server, location)
cluster2 = {'x': cluster2.x,
            'y': cluster2.y,
            'z': cluster2.z}


# cluster 3
location = 'tamantekno'  # Change this to the desired location
cluster3 = cluster_model_1(server, location)
cluster3 = {'x': cluster3.x,
            'y': cluster3.y,
            'z': cluster3.z}


cluster_group_1 = [cluster1,cluster2,cluster3]

