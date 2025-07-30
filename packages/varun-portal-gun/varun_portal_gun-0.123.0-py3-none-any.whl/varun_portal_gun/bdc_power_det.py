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


    loaded_model = joblib.load("/Users/vyelluru/Desktop/bdc_power_det_v5.sav")
    result = loaded_model.predict(df)

    arr = []
    arr2 = []
    for i in range(13):
        arr.append(result[i][0])
        arr2.append(result[i][1])

    df['BDC_IF_DETECT_COMB_RAW'] = arr
    df['TMP_BDC_LNA_COMB_SCALED'] = arr2

    #print(df)


    df2 = pd.DataFrame(columns=columns)

    TEMP_BDC_COMBINED_SCALED = 55

    temporary_p_out = -31.5
    for i in range(13):
        #sgt_attn_cmd - diff by temperature, check bdc_gain 40 df
        sgt_attn_cmd = 10.0
        df2.loc[i] = [pol, sgt_attn_cmd, temporary_p_out, TEMP_BDC_COMBINED_SCALED]
        temporary_p_out = temporary_p_out + 3.5

    encoder = OrdinalEncoder(categories=[['lhcp', 'rhcp']])
    df2['pol'] = encoder.fit_transform(df2[['pol']])


    loaded_model = joblib.load("/Users/vyelluru/Desktop/bdc_power_det_v5.sav")
    result = loaded_model.predict(df2)

    arr = []
    arr2 = []
    for i in range(13):
        arr.append(result[i][0])
        arr2.append(result[i][1])

    df2['BDC_IF_DETECT_COMB_RAW'] = arr
    df2['TMP_BDC_LNA_COMB_SCALED'] = arr2

    #print(df2)

    columns_lhcp = ['sgt_sn', 'pol', 'f_in', 'sgt_attn_cmd', 'vva', 'p_in', 'f_out', 'p_in_meas', 'p_out', 
       'BDC_IF_DETECT_L_RAW', 'BDC_IF_DETECT_L_SCALED', 
        'TEMP_BDC_L_RAW', 'TEMP_BDC_L_SCALED', 
       'TMP_BDC_LNA_L_RAW', 'TMP_BDC_LNA_L_SCALED',
       'CURRENT_BDC_LNA_L_RAW', 'CURRENT_BDC_LNA_L_SCALED',
       'CURRENT_BDC_RFA_L_RAW', 'CURRENT_BDC_RFA_L_SCALED',
       'CURRENT_BDC_IFA_L1_RAW', 'CURRENT_BDC_IFA_L1_SCALED',
        'CURRENT_BDC_IFA_L2_RAW', 'CURRENT_BDC_IFA_L2_SCALED',
       'CURRENT_BDC_IFA_L3_RAW', 'CURRENT_BDC_IFA_L3_SCALED']
    
    columns_rhcp = ['sgt_sn', 'pol', 'f_in', 'sgt_attn_cmd', 'vva', 'p_in', 'f_out', 'p_in_meas', 'p_out', 
       'BDC_IF_DETECT_R_RAW', 'BDC_IF_DETECT_R_SCALED', 
        'TEMP_BDC_R_RAW', 'TEMP_BDC_R_SCALED', 
       'TMP_BDC_LNA_R_RAW', 'TMP_BDC_LNA_R_SCALED',
       'CURRENT_BDC_LNA_R_RAW', 'CURRENT_BDC_LNA_R_SCALED',
       'CURRENT_BDC_RFA_R_RAW', 'CURRENT_BDC_RFA_R_SCALED',
       'CURRENT_BDC_IFA_R1_RAW', 'CURRENT_BDC_IFA_R1_SCALED',
        'CURRENT_BDC_IFA_R2_RAW', 'CURRENT_BDC_IFA_R2_SCALED',
       'CURRENT_BDC_IFA_R3_RAW', 'CURRENT_BDC_IFA_R3_SCALED']
    

    if pol == 'lhcp':
        final_df = pd.DataFrame(columns=columns_lhcp)
        final_df = pd.concat([final_df, df, df2], ignore_index=True)
    else:
        final_df = pd.DataFrame(columns=columns_rhcp)
        final_df = pd.concat([final_df, df, df2], ignore_index=True)
    
    print(final_df)