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
    df2 = pd.DataFrame(columns = columns)
    
    TMP_BDC_LNA_COMBINED_SCALED = -40
    df2.loc[0] = [pol, eq_setting, p_out, f_out, TMP_BDC_LNA_COMBINED_SCALED]

    TMP_BDC_LNA_COMBINED_SCALED = 55
    df2.loc[1] = [pol, eq_setting, p_out, f_out, TMP_BDC_LNA_COMBINED_SCALED]


    encoder = OrdinalEncoder(categories=[['lhcp', 'rhcp']])
    df2['pol'] = encoder.fit_transform(df2[['pol']])

    loaded_model = joblib.load("/Users/vyelluru/Desktop/bdc_gain_v6.sav")
    result = loaded_model.predict(df2)
        

    arr = []
    arr2 = []
    for i in range(2):
        arr.append(result[i][0])
        arr2.append(result[i][1])

    df2['sgt_attn_cmd'] = arr
    df2['TMP_BDC_COMBINED_SCALED'] = arr2

    print(df2.to_string())



    columns_lhcp = ['sgt_serial', 'pol', 'vva_dac', 'eq_setting', 'EVM', 'ACLR_LO', 'ACLR_HI', 'p_in', 'measured p_in', 'sgt_attn_cmd',
                'p_out', 'gain', 'f_out', 
                'BDC_IF_DETECT_L_RAW', 'BDC_IF_DETECT_L_SCALED', 
                'TEMP_BDC_L_RAW', 'TEMP_BDC_L_SCALED', 
                'TMP_BDC_LNA_L_RAW', 'TMP_BDC_LNA_L_SCALED', 
                'CURRENT_BDC_LNA_L_RAW', 'CURRENT_BDC_LNA_L_SCALED', 
                'CURRENT_BDC_RFA_L_RAW', 'CURRENT_BDC_RFA_L_SCALED', 
                'CURRENT_BDC_IFA_L1_RAW', 'CURRENT_BDC_IFA_L1_SCALED', 
                'CURRENT_BDC_IFA_L2_RAW', 'CURRENT_BDC_IFA_L2_SCALED', 
                'CURRENT_BDC_IFA_L3_RAW', 'CURRENT_BDC_IFA_L3_SCALED', 
                'BDC_EN_DET_LO', 'BDC_LHCP_EQ1_SW_A','BDC_LHCP_EQ1_SW_B', 
                'BDC_LHCP_EQ2_SW_A', 'BDC_LHCP_EQ2_SW_B',
                'BDC_LNA2_VGG_L', 'BDC_RFA2_VGG_L', 'BDC_VGG_AMP_L1', 'BDC_VGG_AMP_L2', 'BDC_VGG_AMP_L3']
    
    columns_rhcp = ['sgt_serial', 'pol', 'vva_dac', 'eq_setting', 'EVM', 'ACLR_LO', 'ACLR_HI', 'p_in', 'measured p_in', 'sgt_attn_cmd',
                'p_out', 'gain', 'f_out', 
                'BDC_IF_DETECT_R_RAW', 'BDC_IF_DETECT_R_SCALED', 
                'TEMP_BDC_R_RAW', 'TEMP_BDC_R_SCALED', 
                'TMP_BDC_LNA_R_RAW', 'TMP_BDC_LNA_R_SCALED', 
                'CURRENT_BDC_LNA_R_RAW', 'CURRENT_BDC_LNA_R_SCALED', 
                'CURRENT_BDC_RFA_R_RAW', 'CURRENT_BDC_RFA_R_SCALED', 
                'CURRENT_BDC_IFA_R1_RAW', 'CURRENT_BDC_IFA_R1_SCALED', 
                'CURRENT_BDC_IFA_R2_RAW', 'CURRENT_BDC_IFA_R2_SCALED', 
                'CURRENT_BDC_IFA_R3_RAW', 'CURRENT_BDC_IFA_R3_SCALED', 
                'BDC_EN_DET_LO', 'BDC_RHCP_EQ1_SW_A','BDC_RHCP_EQ1_SW_B', 
                'BDC_RHCP_EQ2_SW_A', 'BDC_RHCP_EQ2_SW_B',
                'BDC_LNA2_VGG_R', 'BDC_RFA2_VGG_R', 'BDC_VGG_AMP_R1', 'BDC_VGG_AMP_R2', 'BDC_VGG_AMP_R3']


    if pol == 'lhcp':
        final_df = pd.DataFrame(columns=columns_lhcp)
        final_df = pd.concat([final_df, df, df2])
        final_df['pol'] = pol
        final_df['eq_setting'] = eq_setting
        final_df['f_out'] = f_out
        final_df['p_out'] = p_out

        final_df['vva_dac'] = 4080
        final_df['p_in'] = 46.0

        final_df['TMP_BDC_LNA_L_SCALED'] = final_df['TMP_BDC_LNA_COMBINED_SCALED']
        final_df['TEMP_BDC_L_SCALED'] = final_df['TMP_BDC_COMBINED_SCALED']

        final_df = final_df.iloc[:, :19]
        final_df = pd.DataFrame(final_df)

    else:
        final_df = pd.DataFrame(columns=columns_rhcp)
        final_df = pd.concat([final_df, df, df2])
        final_df['pol'] = pol
        final_df['eq_setting'] = eq_setting
        final_df['f_out'] = f_out
        final_df['p_out'] = p_out

        final_df['vva_dac'] = 4080
        final_df['p_in'] = 46.0

        final_df['TMP_BDC_LNA_R_SCALED'] = final_df['TMP_BDC_LNA_COMBINED_SCALED']
        final_df['TEMP_BDC_R_SCALED'] = final_df['TMP_BDC_COMBINED_SCALED']

        final_df = final_df.iloc[:, :19]
        final_df = pd.DataFrame(final_df)
    
    print(final_df)
    print(final_df.to_string())