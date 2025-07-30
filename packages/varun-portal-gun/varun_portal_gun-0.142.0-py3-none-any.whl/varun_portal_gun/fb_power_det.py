import joblib
import pandas as pd

from sklearn.preprocessing import OrdinalEncoder
import random

import warnings
warnings.filterwarnings("ignore")


def fb_power_det(room_temp_file):
    room_temp_df = pd.read_csv(room_temp_file)
    #print(room_temp_df.to_string())


    columns = ['pol', 'sgt_fb_attn_cmd', 'p_out', 'TMP_BUC_FB_RAW']
    df = pd.DataFrame(columns=columns)

    pol = room_temp_df.iloc[0, 1]

    sgt_fb_attn_cmd = 14.5

    for i in range(42):
        if i < 21:
            TMP_BUC_FB_RAW = -40
        else:
            TMP_BUC_FB_RAW = 55
        
        p_out = room_temp_df.iloc[i % 21, 9]

        df.loc[i] = [pol, sgt_fb_attn_cmd, p_out, TMP_BUC_FB_RAW]
    

    encoder = OrdinalEncoder(categories=[['lhcp', 'rhcp']])
    df['pol'] = encoder.fit_transform(df[['pol']])


    loaded_model = joblib.load("/Users/vyelluru/Desktop/fb_power_det_v2.sav")
    result = loaded_model.predict(df)

    arr = []
    arr2 = []
    for i in range(42):
        arr.append(result[i][0])
        arr2.append(result[i][1])

    df['PWR_BUC_IF_FB_RAW'] = arr
    df['TMP_BUC_PA_COMB_RAW'] = arr2

    print(df)


    columns_lhcp = ['sgt_sn', 'pol', 'f_in', 'sgt_attn_cmd', 'vva', 'sgt_fb_attn_cmd',
       'p_in', 'f_out', 'p_in_meas', 'p_out', 
       'PWR_BUC_LO_RAW', 'PWR_BUC_LO_SCALED', 
       'PWR_BUC_IF_FB_RAW', 'PWR_BUC_IF_FB_SCALED',
       'PWR_BUC_RF_FB_L_RAW', 'PWR_BUC_RF_FB_L_SCALED', 
       'TMP_BUC_L_RAW', 'TMP_BUC_L_SCALED', 
       'TMP_BUC_PA_L_RAW', 'TMP_BUC_PA_L_SCALED',
       'TMP_BUC_FB_RAW', 'TMP_BUC_FB_SCALED', 
       'TMP_BUC_RF_FB_RAW', 'TMP_BUC_RF_FB_SCALED', 
       'CURRENT_BUC_2X_RAW', 'CURRENT_BUC_2X_SCALED',
       'CURRENT_BUC_VGA_RAW', 'CURRENT_BUC_VGA_SCALED',
       'CURRENT_BUC_LNA_L_RAW', 'CURRENT_BUC_LNA_L_SCALED',
       'CURRENT_BUC_PA1_L_RAW', 'CURRENT_BUC_PA1_L_SCALED',
       'CURRENT_BUC_PA2_L_RAW', 'CURRENT_BUC_PA2_L_SCALED',
       'CURRENT_BUC_DR_L_RAW', 'CURRENT_BUC_DR_L_SCALED']

    columns_rhcp = ['sgt_sn', 'pol', 'f_in', 'sgt_attn_cmd', 'vva', 'sgt_fb_attn_cmd',
       'p_in', 'f_out', 'p_in_meas', 'p_out', 
       'PWR_BUC_LO_RAW', 'PWR_BUC_LO_SCALED', 
       'PWR_BUC_IF_FB_RAW', 'PWR_BUC_IF_FB_SCALED',
       'PWR_BUC_RF_FB_R_RAW', 'PWR_BUC_RF_FB_R_SCALED', 
       'TMP_BUC_R_RAW', 'TMP_BUC_R_SCALED', 
       'TMP_BUC_PA_R_RAW', 'TMP_BUC_PA_R_SCALED',
       'TMP_BUC_FB_RAW', 'TMP_BUC_FB_SCALED', 
       'TMP_BUC_RF_FB_RAW', 'TMP_BUC_RF_FB_SCALED', 
       'CURRENT_BUC_2X_RAW', 'CURRENT_BUC_2X_SCALED',
       'CURRENT_BUC_VGA_RAW', 'CURRENT_BUC_VGA_SCALED',
       'CURRENT_BUC_LNA_R_RAW', 'CURRENT_BUC_LNA_R_SCALED',
       'CURRENT_BUC_PA1_R_RAW', 'CURRENT_BUC_PA1_R_SCALED',
       'CURRENT_BUC_PA2_R_RAW', 'CURRENT_BUC_PA2_R_SCALED',
       'CURRENT_BUC_DR_R_RAW', 'CURRENT_BUC_DR_R_SCALED']
    
    if pol == 'lhcp':
        final_df = pd.DataFrame(columns=columns_lhcp)
        final_df = pd.concat([final_df, df], ignore_index=True)

        final_df['sgt_attn_cmd'] = room_temp_df.iloc[0, 3]
        final_df['f_in'] = room_temp_df.iloc[0, 2]
        
        for i in range(42):
            temp = i % 21
            temp = 2 * temp
            temp = -50 + temp
            final_df.iloc[i, 6] = temp

        final_df['f_out'] = room_temp_df.iloc[0, 7]

        final_df['TMP_BUC_PA_L_RAW'] = final_df['TMP_BUC_PA_COMB_RAW']

    else:
        final_df = pd.DataFrame(columns=columns_rhcp)
        final_df = pd.concat([final_df, df], ignore_index=True)

        final_df['sgt_attn_cmd'] = room_temp_df.iloc[0, 3]
        final_df['f_in'] = room_temp_df.iloc[0, 2]

        for i in range(42):
            temp = i % 21
            temp = 2 * temp
            temp = -50 + temp
            final_df.iloc[i, 6] = temp

        final_df['f_out'] = room_temp_df.iloc[0, 7]

        final_df['TMP_BUC_PA_R_RAW'] = final_df['TMP_BUC_PA_COMB_RAW']