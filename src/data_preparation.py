import random
import pandas as pd 


class DataPreprocessor:
    def __init__(self, data_path='data/data.xlsx', swap_rate=0.01):
        """
        :data_path: path to data file
        :swap_rate: probability of swapping a given sample"""
        self.data_path = data_path
        self.swap_rate = swap_rate

    def get_raw_dataframe(self, data_path=None):
        return pd.read_excel(data_path if data_path else self.data_path)

    def get_dataframe(self):
        df = self.get_raw_dataframe()
        df = self._rename_columns(df.copy())
        df = self._swap_samples(df.copy(), self.swap_rate)
        df = self._map_gender(df.copy())
        df = self._map_in_competition(df.copy())
        return df

    @staticmethod
    def _rename_columns(df):
        """
        Rename columns to match the data model.
        """
        rename_dict = {
            colname: colname.lower().replace(' ', '_')
            for colname in df.columns
        }

        rename_dict.update({
            'ID_random': 'athlete_id_real',
            'Total Observation': 'total_observations',
            'In Comp': 'in_competition',
            'SpecificGravity': 'specific_gravity',
        })

        df.rename(columns=rename_dict, inplace=True)
        return df 

    @staticmethod
    def _map_gender(df):
        df['is_male'] = df['gender'].apply(lambda x: True if x=='M' else False)
        df.drop('gender', axis=1, inplace=True)
        return df
    
    @staticmethod
    def _map_in_competition(df):
        """
        Map in competition column to boolean.
        """
        df['in_competition'] = df['in_competition'].apply(lambda x: True if x=='Y' else False)
        return df

    @staticmethod
    def _map_athletes(row, index_mapping):
        if row.name in index_mapping.keys():
            return index_mapping[row.name]
        return row.athlete_id_real

    def _swap_samples(self, df, swap_rate=0.01):
        """
        Swap samples with given probability.
        """
        df_reduced = df[df['total_observations'] > 3] # remove samples with less than 3 observations

        swap_rate = swap_rate if swap_rate else 0.01

        indices_to_swap = random.sample(list(df_reduced.index), int(len(df)*swap_rate))

        reordered_indices = [*indices_to_swap]
        random.shuffle(reordered_indices)

        new_athletes = df.loc[reordered_indices, :].athlete_id_real

        index_mapping = {
            sample_index: swapped_athlete
            for sample_index, swapped_athlete
            in zip(indices_to_swap, new_athletes)
        }

        df['athlete_id'] = df.apply(self._map_athletes, axis=1, args=(index_mapping, ))
        df['is_swapped'] = df['athlete_id'] != df['athlete_id_real']
        

        return df
        
    @staticmethod
    def _map_total_observations(row, observations_mapping):
        if row.athlete_id in observations_mapping.keys():
            return observations_mapping[row.athlete_id]
        raise Exception("Athlete ID not found in observations mapping.")

    def _update_total_observations(self, df):
        """
        Update total observations for each athlete (after new samples generation).
        """
        observations_per_athlete = df["athlete_id"].value_counts().sort_values().to_dict()
        
        df['total_observations'] = df.apply(
            self._map_total_observations, 
            axis=1, 
            args=(observations_per_athlete, )
            )
        
        return df


