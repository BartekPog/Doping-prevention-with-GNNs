import os
import argparse
import numpy as np
import pandas as pd
from sklearn.utils import shuffle
from data_preparation import DataPreprocessor

def main(args):

    shuffled_path = 'data/splits/shuffled/'
    exclusive_path = 'data/splits/mutually_exclusive/'

    if not os.path.exists(shuffled_path):
        os.makedirs(shuffled_path)
    if not os.path.exists(exclusive_path):
        os.makedirs(exclusive_path)

    df = DataPreprocessor(args.datapath).get_raw_dataframe()

    shuffled_splits(df, args.split_percentage, shuffled_path)
    exclusive_splits(df, args.split_percentage, exclusive_path)


def shuffled_splits(df, frac ,path):

    # For generating shuffled train and test sets, where an athelete in the test set 
    # may also be present in the training set (other samples of same athlete).

    np.random.seed(100)
    shuffled_df = df.sample(frac=1)
    train_df_shuffled, _ = np.split(shuffled_df, [int(frac*len(shuffled_df))])
    train_df_shuffled = train_df_shuffled.reset_index(drop=True)
    test_df_shuffled = shuffled_df.reset_index(drop=True)

    train_df_shuffled.to_excel(path + 'train.xlsx', index=False) 
    test_df_shuffled.to_excel(path + 'test.xlsx', index=False) 

def exclusive_splits(df, frac, path):

    # For generating mutually exclusive train and test sets, where athletes belonging 
    # to the test set are not included in the training set.

    train_df, test_df = np.split(df, [int(frac*len(df))]) # train: upto athlete_id 32790
    train_df = train_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)

    train_df.to_excel(path + 'train.xlsx', index=False) 
    test_df.to_excel(path + 'test.xlsx', index=False) 


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Split data into train and test")
    parser.add_argument("--datapath", default='data/data.xlsx', 
                        type=str, help="Path to the given excel data")
    parser.add_argument("--split-percentage", default=0.7, type=float, 
                        help="Percentage of data to be used for training")
    

    args = parser.parse_args()
    main(args)
