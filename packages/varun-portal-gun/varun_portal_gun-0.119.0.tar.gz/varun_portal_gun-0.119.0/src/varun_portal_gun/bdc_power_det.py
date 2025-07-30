import joblib
import pandas as pd

from sklearn.preprocessing import OrdinalEncoder
import random

import warnings
warnings.filterwarnings("ignore")

#Task: no correction needed, just generate results for -40 and 55 C, use sgt_attn_cmd from bdc_gain df. 

def bdc_power_det():
    columns = ['pol', 'sgt_attn_cmd', 'p_out', 'TEMP_BDC_COMBINED_SCALED']

    df = pd.DataFrame(columns=columns)

    ### HERE - bdc power det room temp
    pol = 'lhcp'

    ###HERE - bdc power det room temp
    p_out = 1


    TEMP_BDC_COMBINED_SCALED = -40


    temporary_p_out = -31.5
    for i in range(13):
        #sgt_attn_cmd - diff by temperature, check bdc_gain 40 df
        sgt_attn_cmd = 20.5
        df.loc[i] = [pol, sgt_attn_cmd, temporary_p_out, TEMP_BDC_COMBINED_SCALED]
        temporary_p_out = temporary_p_out + 3.5

    encoder = OrdinalEncoder(categories=[['lhcp', 'rhcp']])
    df['pol'] = encoder.fit_transform(df[['pol']])

    print(df)

    loaded_model = joblib.load("/Users/vyelluru/Desktop/bdc_power_det_v5.sav")
    result = loaded_model.predict(df)

    print(result)



    TEMP_BDC_COMBINED_SCALED = 55

    temporary_p_out = -31.5
    for i in range(13):
        #sgt_attn_cmd - diff by temperature, check bdc_gain 40 df
        sgt_attn_cmd = 10.0
        df.loc[i] = [pol, sgt_attn_cmd, temporary_p_out, TEMP_BDC_COMBINED_SCALED]
        temporary_p_out = temporary_p_out + 3.5

    encoder = OrdinalEncoder(categories=[['lhcp', 'rhcp']])
    df['pol'] = encoder.fit_transform(df[['pol']])

    print(df)

    loaded_model = joblib.load("/Users/vyelluru/Desktop/bdc_power_det_v5.sav")
    result = loaded_model.predict(df)

    print(result)