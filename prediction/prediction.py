import os, sys
import pickle
import pandas as pd 

from torch_geometric.data import Data


sys.path.append(os.path.abspath(os.path.join('..', 'src')))

from src.data_preparation import DataPreprocessor
from src.graph_data_loader import get_edges, get_nodes



class Predictor:
    def __init__(self, model_path='../../../../../models/gcnae.pkl'):
        
        raise Exception(str(os.listdir('../')))

        self.model = self.load_model(model_path)
        self.df = DataPreprocessor(data_path='data/data.xlsx', swap_rate=0.0).get_dataframe()
        self.predictions = None

    @staticmethod
    def load_model(model_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model

    
    def predict_sample(self, sample_dict):
        sample_dict = self.fill_sample_dict(sample_dict)
        graph_data, new_sample_index = self.get_graph_data(sample_dict)
        
        self.predictions = self.predict_graph(graph_data)
        return self.predictions[new_sample_index]


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


    def get_graph_data(self, sample_dict):
        new_sample_index = self.add_sample_to_dataframe(sample_dict)

        nodes = get_nodes(self.df)
        edges = get_edges(self.df, edge_bw_swapped=False)

        print("Nodes: ", len(nodes))
        print("Edges: ", len(edges))

        graph_data = Data(x=nodes, edge_index=edges.t().contiguous())

        return graph_data, new_sample_index


    def fill_sample_dict(self, sample_dict):
        # base_sample = {
        #     'athlete_id_real': None,
        #     'specific_gravity': 1.016,
        #     'in_competition': True,
        #     'adiol': 27.22,
        #     'bdiol': 144.12,
        #     'androsterone': 2254.7,
        #     'etiocholanolone': 2364.2,
        #     'epitestosterone': 6.08,
        #     'testosterone': 5.92,
        #     't_e_ratio': 0.85,
        #     'andro_t_ratio': 380.86,
        #     'andro_etio_ratio': 0.95,
        #     'adiol_bdiol_ratio': 0.19,
        #     'adiol_e_ratio': 4.48,
        #     'adiol_corr': 34.03,
        #     'bdiol_corr': 180.15,
        #     'androsterone_corr': 2818.38,
        #     'etiocholanolone_corr': 2955.25,
        #     'epitestosterone_corr': 7.6,
        #     'testosterone_corr': 7.4,
        #     #     'total_observations': 4,
        #     'is_male': False,
        #     #     'sample_id': 40,
        #     'athlete_id': 153
        # }
        
        # base_sample.update(sample_dict)

        sample_dict = self.fill_corrected_scores(sample_dict=sample_dict)
        sample_dict = self.fill_ratio_scores(sample_dict=sample_dict)

        return sample_dict

    @staticmethod
    def fill_ratio_scores(sample_dict):
        ratio_mapping = {
            't_e_ratio': ('testosterone', 'epitestosterone'),
            'andro_t_ratio': ('androsterone', 'testosterone'),
            'andro_etio_ratio': ('androsterone', 'etiocholanolone'),
            'adiol_bdiol_ratio': ('adiol', 'bdiol'),
            'adiol_e_ratio': ('adiol', 'epitestosterone'),
        }

        sample_dict.update({
            name: numerator / denominator
            for name, (numerator, denominator)
            in ratio_mapping
        })

        return sample_dict


    @staticmethod
    def fill_corrected_scores(sample_dict):
        raw_hormones = ['adiol', 'bdiol', 'androsterone', 'etiocholanolone', 'epitestosterone', 'testosterone']

        specific_gravity = sample_dict['specific_gravity']

        sample_dict.update({
            f"{hormone}_corr": sample_dict['hormone'] * (1.02 - 1)/(specific_gravity - 1)
            for hormone in raw_hormones
        })

        return sample_dict

