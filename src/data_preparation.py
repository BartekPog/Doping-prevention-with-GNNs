import random
import pandas as pd 


class DataPreprocessor:
    def __init__(self, data_path='data/data.xlsx', swap_rate=0.01, swap_within_gender=True):
        """
        :data_path: path to data file
        :swap_rate: probability of swapping a given sample
        :swap_within_gender: Shoud swapping happen only within gender"""
        self.data_path = data_path
        self.swap_rate = swap_rate
        self.swap_within_gender = swap_within_gender

    def get_raw_dataframe(self, data_path=None):
        return pd.read_excel(data_path if data_path else self.data_path)

    def get_dataframe(self):
        df = self.get_raw_dataframe()
        df = self._rename_columns(df.copy())
        df = self._map_gender(df.copy())
        df = self._map_in_competition(df.copy())
        df = self._swap_samples(df.copy(), self.swap_rate, self.swap_within_gender)
        
        return df

    @staticmethod
    def _rename_columns(df):
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
        df['in_competition'] = df['in_competition'].apply(lambda x: True if x=='Y' else False)
        return df

    @staticmethod
    def _map_athletes(row, index_mapping):
        if row.name in index_mapping.keys():
            return index_mapping[row.name]
        return row.athlete_id_real

    def _get_swap_mapping(self, df, swap_rate=0.01):
        df_reduced = df[df['total_observations'] > 3] # remove samples with less than 3 observations

        swap_rate = swap_rate if swap_rate else 0.01
        swaps_number = int(len(df)*swap_rate/2)

        indices_to_swap_from = random.sample(list(df_reduced.index), swaps_number)

        indices_to_swap_to = random.sample(
            list(df_reduced[~df_reduced.index.isin(indices_to_swap_from)].index), 
            swaps_number
        )

        from_to = {
            from_id: to_id
            for from_id, to_id in 
            zip(indices_to_swap_from, indices_to_swap_to)
        }

        to_from = {
            from_id: to_id
            for from_id, to_id in 
            zip(indices_to_swap_to, indices_to_swap_from)
        }

        swap_index_mapping = {**from_to, **to_from} # Make sure the mapping is two-directional

        athlete_id_per_sample =  df.loc[swap_index_mapping.values(), "athlete_id_real"].copy()

        swap_mapping = {
            sample_id: {
                'swap_sample_id': new_sample_id,
                'new_athlete': athlete_id_per_sample[new_sample_id]
            } for sample_id, new_sample_id 
            in swap_index_mapping.items()
        }

        return swap_mapping
    
    @staticmethod
    def _map_sample_swapping(row, swap_mapping):
        if row['sample_id'] in swap_mapping.keys():
            
            mapping = swap_mapping[row.name]
            row['swapped_with_sample_id'] = mapping['swap_sample_id']
            row['athlete_id'] = mapping['new_athlete']
        return row

    def _add_sample_indexes(self, df):
        """
        Add sample indexes to dataframe.
        """
        df['sample_id'] = df.index
        return df

    def _swap_samples(self, df, swap_rate=0.01, swap_within_gender=True):
        """
        Swap samples with given probability.
        """
        if swap_within_gender:
            return pd.concat([
                self._swap_samples(df[df['is_male'] == False].copy(), swap_rate=swap_rate, swap_within_gender=False),
                self._swap_samples(df[df['is_male'] == True].copy(), swap_rate=swap_rate, swap_within_gender=False)
            ])

        swap_mapping = self._get_swap_mapping(df.copy(), swap_rate=swap_rate)

        df['sample_id'] = df.index
        df['athlete_id'] = df['athlete_id_real']

        df_swapped = df.apply(self._map_sample_swapping, axis=1, args=(swap_mapping, ))
        
        return df_swapped

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


