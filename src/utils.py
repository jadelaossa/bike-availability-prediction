import os
import pickle
import pandas as pd
from sklearn import base


def save_object(file_path, object):
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    
    with open(file_path, 'wb') as f:
        pickle.dump(object, f)
        
def load_object(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)
    
def tweak_bicing(df_):
    
    columns_to_drop = ['post_code', 'lat', 'lon', 'capacity', 'max_temp', 'min_temp', 'avg_atm_pressure', 
                       'avg_wind_direction', 'max_wind_speed', 'max_streak_wind_direction']

    return (df_
            .astype({'station_id': 'category', 'post_code': 'category'})  # to be treated as categorical variable by algorithms like XGBoost
            .drop(columns=columns_to_drop)
            )

class TweakBicingTransformer(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, ycol=None):
        self.ycol = ycol
        
    def transform(self, X):
        return tweak_bicing(X)
    
    def fit(self, X, y=None):
        return self
    
def get_rawX_y(df, y_col, drop_set):
    raw = (df
           .set_index('year')
           .drop(index=drop_set)
           .reset_index()
          )
    return raw.drop(columns=['year', y_col]), raw[y_col]