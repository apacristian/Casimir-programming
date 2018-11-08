import pandas as pd
import numpy as np
import counts_to_csv

def load_csv(csv):
    df = pd.read_csv(csv, header=None, sep=',')
    return df

df = load_csv('data_growth_curves_1.csv');

data_raw = np.array(df)
print(data_raw)