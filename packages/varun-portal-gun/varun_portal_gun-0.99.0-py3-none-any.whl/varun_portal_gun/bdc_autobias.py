import joblib
import pandas as pd

from sklearn.preprocessing import OrdinalEncoder
import random

import warnings
warnings.filterwarnings("ignore")


def bdc_autobias(room_temp_file):
    room_temp_df = pd.read_csv(room_temp_file)
    print(room_temp_df)

    columns=['pol', 'dac_name', 'TEMP_BDC_COMBINED_SCALED'
         ,'CURRENT_BDC_LNA_COMB_RAW', 'CURRENT_BDC_RFA_COMB_RAW', 'CURRENT_BDC_IFA_1_COMB_RAW', 'CURRENT_BDC_IFA_2_COMB_RAW', 'CURRENT_BDC_IFA_3_COMB_RAW']
    
    df = pd.DataFrame(columns=columns)

    #fill input df 1 for room temp correction
    # i know the 5 currents and dac_name, i need pol and temp_bdc from user files
    # essentially check autobias_fw_bdc_*_25 file.
    CURRENT_BDC_LNA_COMB_RAW = 1035.0
    CURRENT_BDC_RFA_COMB_RAW = 1035.0
    CURRENT_BDC_IFA_1_COMB_RAW = 414.0
    CURRENT_BDC_IFA_2_COMB_RAW = 1345.0
    CURRENT_BDC_IFA_3_COMB_RAW = 1345.0

    #### HERE
    pol = 'right'

    for i in range(5):
        dac_name = 0.0
        match i:
            case 0:
                dac_name = 0.0
            case 1:
                dac_name = 1.0
            case 2:
                dac_name = 2.0
            case 3:
                dac_name = 3.0
            case 4:
                dac_name = 4.0
            case _:
                break
        
        #### HERE
        TEMP_BDC_COMBINED_SCALED = 25

        df.loc[i] = [pol, dac_name, TEMP_BDC_COMBINED_SCALED, CURRENT_BDC_LNA_COMB_RAW, CURRENT_BDC_RFA_COMB_RAW, CURRENT_BDC_IFA_1_COMB_RAW, CURRENT_BDC_IFA_2_COMB_RAW, CURRENT_BDC_IFA_3_COMB_RAW]

    encoder = OrdinalEncoder(categories=[['left', 'right']])
    df['pol'] = encoder.fit_transform(df[['pol']])

    loaded_model = joblib.load("/Users/vyelluru/Desktop/bdc_autobias_v5.sav")
    result = loaded_model.predict(df)
    
    arr = []
    arr2 = []
    for i in range(5):
        arr.append(result[i][0])
        arr2.append(result[i][1])


    df['sweep_dac_value'] = arr
    df['TMP_BDC_LNA_COMBINED_RAW'] = arr2




    #fill input df 2 for normal calibration
    # i know 5 currents, dac_name, temp_bdc. i just need pol from user files.
    df2 = pd.DataFrame(columns=columns)

    for i in range(10):
        dac_name = 0.0
        match i % 5:
            case 0:
                dac_name = 0.0
            case 1:
                dac_name = 1.0
            case 2:
                dac_name = 2.0
            case 3:
                dac_name = 3.0
            case 4:
                dac_name = 4.0
            case _:
                break
        
        if i < 5:
            TEMP_BDC_COMBINED_SCALED = -40
        else:
            TEMP_BDC_COMBINED_SCALED = 55

        df2.loc[i] = [pol, dac_name, TEMP_BDC_COMBINED_SCALED, CURRENT_BDC_LNA_COMB_RAW, CURRENT_BDC_RFA_COMB_RAW, CURRENT_BDC_IFA_1_COMB_RAW, CURRENT_BDC_IFA_2_COMB_RAW, CURRENT_BDC_IFA_3_COMB_RAW]


    encoder = OrdinalEncoder(categories=[['left', 'right']])
    df2['pol'] = encoder.fit_transform(df2[['pol']])

    loaded_model = joblib.load("/Users/vyelluru/Desktop/bdc_autobias_v5.sav")
    result2 = loaded_model.predict(df2)
    
    arr3 = []
    arr4 = []
    for i in range(10):
        arr3.append(result2[i][0])
        arr4.append(result2[i][1])

    df2['sweep_dac_value'] = arr3
    df2['TMP_BDC_LNA_COMBINED_RAW'] = arr4




    #Note pol when creating final df here
    columns_lhcp =['sgt_serial', 'pol', 'block', 'dac_name', 'sweep_dac_value', 'current_avg', 'vdd_key', 
                'BDC_IF_DETECT_L_RAW', 'BDC_IF_DETECT_L_SCALED',
                'TEMP_BDC_L_RAW', 'TEMP_BDC_L_SCALED',
                'TEMP_BDC_LNA_L_RAW', 'TEMP_BDC_LNA_L_SCALED', 
                'CURRENT_BDC_LNA_L_RAW', 'CURRENT_BDC_LNA_L_SCALED',
                'CURRENT_BDC_RFA_L_RAW', 'CURRENT_BDC_RFA_L_SCALED',
                'CURRENT_BDC_IFA_L1_RAW', 'CURRENT_BDC_IFA_L1_SCALED',
                'CURRENT_BDC_IFA_L2_RAW', 'CURRENT_BDC_IFA_L2_SCALED',
                'CURRENT_BDC_IFA_L3_RAW', 'CURRENT_BDC_IFA_L3_SCALED']

    columns_rhcp =['sgt_serial', 'pol', 'block', 'dac_name', 'sweep_dac_value', 'current_avg', 'vdd_key', 
                'BDC_IF_DETECT_R_RAW', 'BDC_IF_DETECT_R_SCALED',
                'TEMP_BDC_R_RAW', 'TEMP_BDC_R_SCALED',
                'TEMP_BDC_LNA_R_RAW', 'TEMP_BDC_LNA_R_SCALED', 
                'CURRENT_BDC_LNA_R_RAW', 'CURRENT_BDC_LNA_R_SCALED',
                'CURRENT_BDC_RFA_R_RAW', 'CURRENT_BDC_RFA_R_SCALED',
                'CURRENT_BDC_IFA_R1_RAW', 'CURRENT_BDC_IFA_R1_SCALED',
                'CURRENT_BDC_IFA_R2_RAW', 'CURRENT_BDC_IFA_R2_SCALED',
                'CURRENT_BDC_IFA_R3_RAW', 'CURRENT_BDC_IFA_R3_SCALED']

    final_df = []
    if pol == 'left':
        #fill up current values and scaled
        final_df = pd.DataFrame(columns=columns_lhcp)
        final_df = pd.concat([final_df, df, df2])
        final_df['pol'] = pol
        final_df['block'] = 'rx'
        final_df['vdd_key'] = 'vdd1'

        mapping = {
            0.0: 'BDC_LNA2_VGG_L',
            1.0: 'BDC_RFA2_VGG_L',
            2.0: 'BDC_VGG_AMP_L1',
            3.0: 'BDC_VGG_AMP_L2',
            4.0: 'BDC_VGG_AMP_L3'
        }
        final_df.iloc[:, 3] = final_df['dac_name'].map(mapping)

        final_df['CURRENT_BDC_LNA_L_RAW'] = final_df['CURRENT_BDC_LNA_COMB_RAW']
        final_df['CURRENT_BDC_RFA_L_RAW'] = final_df['CURRENT_BDC_RFA_COMB_RAW']
        final_df['CURRENT_BDC_IFA_L1_RAW'] = final_df['CURRENT_BDC_IFA_1_COMB_RAW']
        final_df['CURRENT_BDC_IFA_L2_RAW'] = final_df['CURRENT_BDC_IFA_2_COMB_RAW']
        final_df['CURRENT_BDC_IFA_L3_RAW'] = final_df['CURRENT_BDC_IFA_3_COMB_RAW']

        final_df['TEMP_BDC_LNA_L_RAW'] = final_df['TMP_BDC_LNA_COMBINED_RAW']

        final_df['TEMP_BDC_L_SCALED'] = final_df['TEMP_BDC_COMBINED_SCALED']

        final_df['CURRENT_BDC_LNA_L_SCALED'] = final_df['CURRENT_BDC_LNA_L_RAW'] / 20695
        final_df['CURRENT_BDC_RFA_L_SCALED'] = final_df['CURRENT_BDC_RFA_L_RAW'] / 20695
        final_df['CURRENT_BDC_IFA_L1_SCALED'] = final_df['CURRENT_BDC_IFA_L1_RAW'] / 20695
        final_df['CURRENT_BDC_IFA_L2_SCALED'] = final_df['CURRENT_BDC_IFA_L2_RAW'] / 20695
        final_df['CURRENT_BDC_IFA_L3_SCALED'] = final_df['CURRENT_BDC_IFA_L3_RAW'] / 20695

        final_df = pd.DataFrame(final_df.iloc[:, :23])

    else:
        #fill up current values and scaled
        final_df = pd.DataFrame(columns=columns_rhcp)

        final_df = pd.concat([final_df, df, df2])
        final_df['pol'] = pol
        final_df['block'] = 'tx'
        final_df['vdd_key'] = 'vdd1'

        mapping = {
            0.0: 'BDC_LNA2_VGG_R',
            1.0: 'BDC_RFA2_VGG_R',
            2.0: 'BDC_VGG_AMP_R1',
            3.0: 'BDC_VGG_AMP_R2',
            4.0: 'BDC_VGG_AMP_R3'
        }
        final_df.iloc[:, 3] = final_df['dac_name'].map(mapping)

        final_df['CURRENT_BDC_LNA_R_RAW'] = final_df['CURRENT_BDC_LNA_COMB_RAW']
        final_df['CURRENT_BDC_RFA_R_RAW'] = final_df['CURRENT_BDC_RFA_COMB_RAW']
        final_df['CURRENT_BDC_IFA_R1_RAW'] = final_df['CURRENT_BDC_IFA_1_COMB_RAW']
        final_df['CURRENT_BDC_IFA_R2_RAW'] = final_df['CURRENT_BDC_IFA_2_COMB_RAW']
        final_df['CURRENT_BDC_IFA_R3_RAW'] = final_df['CURRENT_BDC_IFA_3_COMB_RAW']

        final_df['TEMP_BDC_LNA_R_RAW'] = final_df['TMP_BDC_LNA_COMBINED_RAW']

        final_df['TEMP_BDC_R_SCALED'] = final_df['TEMP_BDC_COMBINED_SCALED']

        final_df['CURRENT_BDC_LNA_R_SCALED'] = final_df['CURRENT_BDC_LNA_R_RAW'] / 20695
        final_df['CURRENT_BDC_RFA_R_SCALED'] = final_df['CURRENT_BDC_RFA_R_RAW'] / 20695
        final_df['CURRENT_BDC_IFA_R1_SCALED'] = final_df['CURRENT_BDC_IFA_R1_RAW'] / 20695
        final_df['CURRENT_BDC_IFA_R2_SCALED'] = final_df['CURRENT_BDC_IFA_R2_RAW'] / 20695
        final_df['CURRENT_BDC_IFA_R3_SCALED'] = final_df['CURRENT_BDC_IFA_R3_RAW'] / 20695

        final_df = pd.DataFrame(final_df.iloc[:, :23])

    print(final_df.to_string())