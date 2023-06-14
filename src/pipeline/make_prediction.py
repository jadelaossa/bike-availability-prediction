import numpy as np
import pandas as pd
from src.utils import load_object, TweakBicingTransformer

import matplotlib.pyplot as plt



metadata = pd.read_csv(r'src\pipeline\artifacts\metadata_sample_submission.csv', index_col='index').rename(columns={'ctx-1': 'ctx_1', 'ctx-2': 'ctx_2',
                                                                                                         'ctx-3': 'ctx_3', 'ctx-4': 'ctx_4'})

bicing_info = pd.read_parquet(r'data\processed\bicing_info.parquet')
meteo_stats = pd.read_parquet(r'data\processed\meteo_stats.parquet').query('year == 2023').drop(columns='year')
calendar = pd.read_parquet(r'data\processed\calendar.parquet').query('year == 2023').drop(columns='year')
    
bicing = (metadata
          .merge(bicing_info, on=['station_id'], how='left', validate='many_to_one')
          .merge(calendar, on=['month', 'day'], how='left', validate='many_to_one')
          .merge(meteo_stats, on=['month', 'day'], how='left', validate='many_to_one')
)

bicing_pl = load_object(r'models\features_transformation_pipeline.pkl')
X_sample = bicing_pl.transform(bicing)

model = load_object(r'models\model.pkl')

y_pred = model.predict(X_sample)

metadata_pred = (pd.DataFrame(y_pred)
                 .reset_index()
                 .rename(columns={0: 'percentage_docks_available'})
).to_csv(r'src\pipeline\artifacts\metadata_pred.csv', index=False)