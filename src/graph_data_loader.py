import torch
import numpy as np
import pandas as pd
from itertools import cycle
from torch_geometric.data import Data
from src.data_preparation import DataPreprocessor


def graph_loader(swap_rate=0.01):

    swapped_df = DataPreprocessor(swap_rate=swap_rate).get_dataframe()
    swapped_df = swapped_df.sort_values('sample_id')

    nodes = get_nodes(swapped_df)
    edges = get_edges(swapped_df)
    data = Data(x=nodes, edge_index=edges.t().contiguous())

    return data

def get_nodes(df):
    feature_vec = df.drop(['athlete_id', 'athlete_id_real', 'sample_id', 'swapped_with_sample_id', 'total_observations'], axis = 1)
    feature_vector = torch.tensor(feature_vec.values.astype(np.float32))  # nodes
    return feature_vector

def get_edges(df):

    edges = []
    for index, row in df.iterrows():
        curr_sample_id = row['sample_id']

        # edges between nodes having the same 'athelete_id'
        sub_df = df.loc[df['athlete_id'] == row['athlete_id']]
        group_sample_ids = list(sub_df['sample_id'])
        group_sample_ids.remove(curr_sample_id)
        group_edges = list(zip(cycle([curr_sample_id]), group_sample_ids))
        if torch.is_tensor(edges):
            edges = torch.cat((edges, torch.tensor(group_edges)), dim=0)
        else:
            edges = torch.tensor(group_edges)
        
        # if swapped, edge between the node and the one with which it has been swapped
        if not pd.isna(row['swapped_with_sample_id']):
            swapped_edge = torch.tensor((curr_sample_id, row['swapped_with_sample_id'])).unsqueeze(0)
            edges = torch.cat((edges, swapped_edge), dim=0)   

    return edges.long()