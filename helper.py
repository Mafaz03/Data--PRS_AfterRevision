import numpy as np
import pandas as pd

def load_dic_file(filename):
    with open(filename, 'r') as f:
        content = f.readlines()
    df = pd.DataFrame([[float(j) for j in i.split("\t")] for i in content[1:]])
    df = df.rename({0: "X-Position", 1: "Y-Position", 2: "U-Displacement", 3: "V-Displacement"}, axis=1)
    return df

def extract_displacement_jump(df, interface_x=650):
    df_filtered = df[(df['U-Displacement'] != 0) & (df['V-Displacement'] != 0)]
    
    left_region = df_filtered[df_filtered['X-Position'] < interface_x]
    right_region = df_filtered[df_filtered['X-Position'] > interface_x + 50]  # Avoid interface zone
    
    # Average vertical displacement near interface from left and right
    left_avg_v = left_region['V-Displacement'].mean()
    right_avg_v = right_region['V-Displacement'].mean()
    
    # Displacement jump at interface
    delta_v = np.abs(left_avg_v - right_avg_v)
    return delta_v