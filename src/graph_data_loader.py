import os
import torch
import numpy as np
import pandas as pd
from itertools import cycle
from torch_geometric.data import Data
from src.data_preparation import DataPreprocessor


def graph_loader(split_type='mutually_exclusive', swap_rate=0.01, edge_bw_swapped=False):

    assert split_type in ['mutually_exclusive', 'shuffled'], "Invalid split type: %s. \
    Use 'shuffled' or 'mutually_exclusive'" % split_type

    data_root = 'data/splits/' +split_type    
    train_path = data_root+'/train.xlsx'
    print("Reading train data from ", train_path)
    test_path = data_root+'/test.xlsx'
    print("Reading test data from ", test_path)
    
    # generate training graph
    train_df = DataPreprocessor(data_path=train_path, swap_rate=swap_rate).get_dataframe()
    train_df = train_df.sort_values('sample_id')

    train_nodes = get_nodes(train_df)
    train_edges = get_edges(train_df, edge_bw_swapped)
    train_data = Data(x=train_nodes, edge_index=train_edges.t().contiguous())

    # generate test graph
    test_df = DataPreprocessor(data_path=test_path, swap_rate=swap_rate).get_dataframe()
    test_df = test_df.sort_values('sample_id')

    test_nodes = get_nodes(test_df)
    test_edges = get_edges(test_df, edge_bw_swapped)
    test_data = Data(x=test_nodes, edge_index=test_edges.t().contiguous())

    return [train_data, test_data]

def get_nodes(df):
    feature_vec = df.drop(['athlete_id', 'athlete_id_real', 'sample_id', 'swapped_with_sample_id', 'total_observations'], axis = 1)
    feature_vector = torch.tensor(feature_vec.values.astype(np.float32))  # nodes
    return feature_vector

def get_edges(df, edge_bw_swapped):

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
        
        if edge_bw_swapped:
            # if swapped, edge between the node and the one with which it has been swapped
            if not pd.isna(row['swapped_with_sample_id']):
                swapped_edge = torch.tensor((curr_sample_id, row['swapped_with_sample_id'])).unsqueeze(0)
                edges = torch.cat((edges, swapped_edge), dim=0)   

    return edges.long()