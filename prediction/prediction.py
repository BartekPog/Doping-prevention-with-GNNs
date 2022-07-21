import pickle
import pandas as pd 

from torch_geometric.data import Data

from src.data_preparation import DataPreprocessor
from src.graph_data_loader import get_edges, get_samples



class Predictor:
    def __init__(self, model_path='../models/gcnae.pkl'):
        self.model = self.load_model(model_path)
        self.df = DataPreprocessor(data_path='data/data.xlsx', swap_rate=0.0).get_dataframe()
        self.predictions = None

    @staticmethod
    def load_model(model_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model


    def predict_graph(self, graph_data):
        return self.model.predict(graph_data)


    def add_sample_to_dataframe(self, new_sample):
        same_athlete_samples = self.df.athlete_id == new_sample['athlete_id']

        new_sample_id = int(self.df.sample_id.max()) + 1
        new_sample_count = same_athlete_samples.sum() + 1


        row_idxes = self.df[same_athlete_samples].index
        col_idx = self.df.columns.get_loc('total_observations')

        self.df.iloc[row_idxes, col_idx] = new_sample_count

        new_sample.update({
            'sample_id': new_sample_id,
            'total_observations': new_sample_count,
        })

        new_df = pd.DataFrame([new_sample])
        new_df = new_df[self.df.columns]

        df = pd.concat([self.df, new_df])

        self.df = df.copy()

        self.df = self.df.iloc[10:].copy()


        sample_df_index = self.df[self.df.sample_id == new_sample_id].index[0]


        

        return sample_df_index

        # return 0

    def get_graph_data(self, sample_dict):
        new_sample_index = self.add_sample_to_dataframe(sample_dict)

        nodes = get_samples(self.df)
        edges = get_edges(self.df, edge_bw_swapped=False)

        print("Nodes: ", len(nodes))
        print("Edges: ", len(edges))

        graph_data = Data(x=nodes, edge_index=edges.t().contiguous())

        return graph_data, new_sample_index

    def predict_sample(self, sample_dict):
        graph_data, new_sample_index = self.get_graph_data(sample_dict)
        
        self.predictions = self.predict_graph(graph_data)
        return self.predictions[new_sample_index]
