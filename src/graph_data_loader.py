from json import load
import os
import torch
import numpy as np
import pandas as pd
import itertools
from itertools import cycle
from torch_geometric.data import Data
from torch_geometric.data import HeteroData
from src.data_preparation import DataPreprocessor

def load_df(split_type, swap_rate):
    assert split_type in ['whole', 'mutually_exclusive', 'shuffled'], "Invalid split type: %s. \
    Use 'shuffled', 'mutually_exclusive' or 'whole'" % split_type

    if split_type=='whole':
        train_df = DataPreprocessor(data_path='data/data.xlsx', swap_rate=swap_rate).get_dataframe()
        test_df = DataPreprocessor(data_path='data/data.xlsx', swap_rate=swap_rate).get_dataframe()
        #train_target = np.zeros(len(train_df))
        train_target = ~train_df['swapped_with_sample_id'].isna()
        train_target = torch.tensor(train_target.values.astype(np.int32))
        test_target =  ~test_df['swapped_with_sample_id'].isna()
        test_target = torch.tensor(test_target.values.astype(np.int32))

    else:
        data_root = 'data/splits/' +split_type    
        train_path = data_root+'/train.xlsx'
        print("Reading train data from ", train_path)
        test_path = data_root+'/test.xlsx'
        print("Reading test data from ", test_path)
    
        # get training data
        train_df = DataPreprocessor(data_path=train_path, swap_rate=swap_rate).get_dataframe()
        train_df = train_df.sort_values('sample_id')
        train_target = ~train_df['swapped_with_sample_id'].isna()
        train_target = torch.tensor(train_target.values.astype(np.int32))

        # get testing data
        test_df = DataPreprocessor(data_path=test_path, swap_rate=swap_rate).get_dataframe()
        test_df = test_df.sort_values('sample_id')
        test_target = ~test_df['swapped_with_sample_id'].isna()
        test_target = torch.tensor(test_target.values.astype(np.int32))

    return train_df, train_target, test_df, test_target

def get_samples(df):
    feature_vec = df.drop(['athlete_id', 'athlete_id_real', 'sample_id', 'total_observations'], axis = 1)
    if 'swapped_with_sample_id' in feature_vec.columns:
        feature_vec = feature_vec.drop(['swapped_with_sample_id'], axis=1)
    feature_vector = torch.tensor(feature_vec.values.astype(np.float32))  # nodes
    return feature_vector

def get_athletes(df):
    athlete_vec = df.loc[:, ['athlete_id', 'is_male']].drop_duplicates()
    return torch.tensor(athlete_vec.values.astype(np.float32))  # nodes

def get_athlete2athlete_edges(df):
    athlete_vec = df.loc[:, ['athlete_id', 'is_male']].drop_duplicates()
    num_athletes = len(athlete_vec)
    perm = list(itertools.permutations(list(range(num_athletes)), 2))
    edges = torch.tensor(perm, dtype=torch.long).t().contiguous()
    return edges

def get_sample2athlete_edges(df):

    id_pos_mapping = df.loc[:, 'athlete_id'].drop_duplicates().reset_index(drop=True).reset_index().set_index('athlete_id').to_dict()['index']
    edges = []
    for index, row in df.iterrows():
        athlete_id = row['athlete_id']
        edges.append((index, id_pos_mapping[athlete_id]))
    edges = torch.tensor(edges, dtype=torch.long).t().contiguous()
    return edges

def get_edges(df, edge_bw_swapped):

    edges = []
    for index, row in df.iterrows():
        curr_sample_id = row['sample_id']

        # edges between samples having the same 'athelete_id'
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

def graph_loader(split_type='mutually_exclusive', swap_rate=0.01, edge_bw_swapped=False):

    train_df, train_target, test_df, test_target = load_df(split_type, swap_rate)

    # generate training graph
    train_nodes = get_samples(train_df)
    train_edges = get_edges(train_df, edge_bw_swapped)
    train_data = Data(x=train_nodes, edge_index=train_edges.t().contiguous())

    # generate test graph
    test_nodes = get_samples(test_df)
    test_edges = get_edges(test_df, edge_bw_swapped)
    test_data = Data(x=test_nodes, edge_index=test_edges.t().contiguous())
    
    train_data.y = train_target
    test_data.y = test_target
    
    return [train_data, test_data]

def heterogeneous_graph_loader(split_type='mutually_exclusive', swap_rate=0.01):

    train_df, train_target, test_df, test_target = load_df(split_type, swap_rate)

    train_data = HeteroData()
    train_data['sample'].x = get_samples(train_df)
    train_data['sample'].y = train_target
    train_data['athlete'].x = get_athletes(train_df)
    train_data['athlete', 'knows', 'athlete' ].edge_index = get_athlete2athlete_edges(train_df)
    train_data['sample', 'belongs_to', 'athlete'].edge_index = get_sample2athlete_edges(train_df)

    test_data = HeteroData()
    test_data['sample'].x = get_samples(test_df)
    test_data['sample'].y = test_target
    test_data['athlete'].x = get_athletes(test_df)
    test_data['athlete', 'knows', 'athlete' ].edge_index = get_athlete2athlete_edges(test_df)
    test_data['sample', 'belongs_to', 'athlete'].edge_index = get_sample2athlete_edges(test_df)

    return [train_data, test_data]