import pandas as pd
import numpy as np
#from counts_to_csv import analyse_data

def load_csv(csv):
    df = pd.read_csv(csv, header=None, sep=',')
    return df

df = load_csv('data_raw/data_growth_curves_1.csv');

data_raw = np.array(df,dtype=float)
plt.figure(3)
plot_curves(data_raw)
plt.figure(0)
analyse_data(data_raw, 18, 0, 1, 0.45)
plt.figure(1)
analyse_data(data_raw, 18, 0, 1, 0.5)
plt.figure(2)
analyse_data(data_raw, 18, 0, 1, 0.6)
