import typer
from pathlib import Path
from typing import Optional

from typing_extensions import Annotated
import os
import joblib
import pandas as pd

from sklearn.preprocessing import OrdinalEncoder
import random

app = typer.Typer()


@app.callback()
def callback():
    pass

@app.command()
def predict(path: Annotated[str, typer.Option()] = None):
    print("Here are your input files: " + path)

    for filename in os.listdir(path):
        print(filename)



@app.command()
def run_model():
    print("Loaded Model")
    loaded_model = joblib.load("/Users/vyelluru/Desktop/bdc_power_det_v4.sav")
    X_test = [[1.00000, 17.7500, 4.413225, 1858.00], [1.00000, 17.7500, 4.413225, 1858.00]]
    result = loaded_model.predict(pd.DataFrame(X_test))
    print(result)
    print("Success")


#Setting up inference X_test
'''
BDC Power - -80 to -32 p_in * 2 pol's * 2 temps (52 rows)
creating an X_test df
'''
@app.command()
def bdc_power_det_test():
    columns = ['pol', 'f_in', 'sgt_attn_cmd', 'vva', 'p_in', 'f_out', 'p_out', 
            'TEMP_BDC_SCALED']
    p_in_arr = [-80, -76, -72, -68, -64, -60, -56, -52, -48, -44, -40, -36, -32]

    p_out_arr = [-31.8, -28.1, -24.1, -19.9, -15.7, -11.5, -7.7, -4.6, -0.5, 3.5, 8.1, 10.6, 13.9]
    TEMP_BDC_SCALED_arr = [40, 55]
    #sgt_attn_cmd_arr = [12.75, 9.5, 18, 12.25, 10, 17.25]

    df = pd.DataFrame(columns=columns)

    for i in range(52):
        if i < 26:
            pol = 'lhcp'
            offset = round(random.uniform(-1, 1), 3) * 2.5
            if i < 13:
                TEMP_BDC_SCALED = TEMP_BDC_SCALED_arr[0] + offset
            else:
                TEMP_BDC_SCALED = TEMP_BDC_SCALED_arr[1] + offset
        else:
            pol = 'rhcp'
            offset = round(random.uniform(-1, 1), 3) * 2.5
            if i < 39:
                TEMP_BDC_SCALED = TEMP_BDC_SCALED_arr[0] + offset
            else:
                TEMP_BDC_SCALED = TEMP_BDC_SCALED_arr[1] + offset
        p_in = p_in_arr[i % 13]
        f_in = 28.75
        sgt_attn_cmd = round(random.uniform(9.5, 17.25), 1)
        vva = 4080
        f_out = 4320000000
        p_out = p_out_arr[i % 13]


        df.loc[i] = [pol, f_in, sgt_attn_cmd, vva, p_in, f_out, p_out, TEMP_BDC_SCALED]


    X_test = df.iloc[:, [0, 2, 6, 7]]

    encoder = OrdinalEncoder(categories=[['lhcp', 'rhcp']])
    X_test['pol'] = encoder.fit_transform(X_test[['pol']])

    X_test = X_test.to_numpy()
    print(X_test)

    X_test = pd.DataFrame(X_test)

    loaded_model = joblib.load("/Users/vyelluru/Desktop/bdc_power_det_v5.sav")
    result = loaded_model.predict(X_test)
    print(result)
    print("BDC PD Success")