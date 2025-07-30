import joblib
import pandas as pd

from sklearn.preprocessing import OrdinalEncoder
import random

import warnings
warnings.filterwarnings("ignore")

def bdc_gain():
    #fill input df 1 for room temp p_out correction
    # i know the p_out = 1, i need pol, eq_setting, f_out, TMP_BDC_LNA_SCALED from user files
    # essentially check gain_bdc_*_25 file

    columns = ['pol', 'eq_setting', 'p_out', 'f_out', 'TMP_BDC_LNA_COMBINED_SCALED']
    df = pd.DataFrame(columns = columns)

    ### HERE
    pol = 'lhcp'

    ### HERE
    eq_setting = 11.2

    p_out = 1

    ### HERE
    f_out = 3570000000.0


    ###HERE
    TMP_BDC_LNA_COMBINED_SCALED = 24.54213
    

    df.loc[0] = [pol, eq_setting, p_out, f_out, TMP_BDC_LNA_COMBINED_SCALED]

    encoder = OrdinalEncoder(categories=[['lhcp', 'rhcp']])
    df['pol'] = encoder.fit_transform(df[['pol']])


    loaded_model = joblib.load("/Users/vyelluru/Desktop/bdc_gain_v6.sav")
    result = loaded_model.predict(df)

        
    df['sgt_attn_cmd'] = result[0][0]
    df['TMP_BDC_COMBINED_SCALED'] = result[0][1]

    print(df.to_string())



    #fill input df 2 for normal calibration
    # i know p_out = 1, TMP_BDC_LNA_SCALED. i need pol, eq_setting, f_out from user files.

    columns = ['pol', 'eq_setting', 'p_out', 'f_out', 'TMP_BDC_LNA_COMBINED_SCALED']
    df = pd.DataFrame(columns = columns)
    
    TMP_BDC_LNA_COMBINED_SCALED = -40
    df.loc[0] = [pol, eq_setting, p_out, f_out, TMP_BDC_LNA_COMBINED_SCALED]

    TMP_BDC_LNA_COMBINED_SCALED = 55
    df.loc[1] = [pol, eq_setting, p_out, f_out, TMP_BDC_LNA_COMBINED_SCALED]


    encoder = OrdinalEncoder(categories=[['lhcp', 'rhcp']])
    df['pol'] = encoder.fit_transform(df[['pol']])

    loaded_model = joblib.load("/Users/vyelluru/Desktop/bdc_gain_v6.sav")
    result = loaded_model.predict(df)
        

    arr = []
    arr2 = []
    for i in range(2):
        arr.append(result[i][0])
        arr2.append(result[i][1])

    df['sgt_attn_cmd'] = arr
    df['TMP_BDC_COMBINED_SCALED'] = arr2

    print(df.to_string())