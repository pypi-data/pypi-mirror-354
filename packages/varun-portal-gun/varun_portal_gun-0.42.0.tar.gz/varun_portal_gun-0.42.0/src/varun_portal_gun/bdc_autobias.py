import joblib
import pandas as pd

from sklearn.preprocessing import OrdinalEncoder
import random


def bdc_autobias():
    columns=['pol', 'dac_name', 'sweep_dac_value', 'TEMP_BDC_COMBINED_SCALED', 'TMP_BDC_LNA_COMBINED_RAW'
             'CURRENT_BDC_LNA_COMB_RAW', 'CURRENT_BDC_RFA_COMB_RAW', 'CURRENT_BDC_IFA_1_COMB_RAW', 'CURRENT_BDC_IFA_2_COMB_RAW', 'CURRENT_BDC_IFA_3_COMB_RAW']
    
    df = pd.DataFrame(columns=columns)

    #fill input df 1 for room temp correction
    # i know the 5 currents and dac_name, i need pol and temp_bdc from user files
    # essentially check autobias_fw_bdc_*_25 file.
    CURRENT_BDC_LNA_COMB_RAW = 1035.0
    CURRENT_BDC_RFA_COMB_RAW = 1035.0
    CURRENT_BDC_IFA_1_COMB_RAW = 414.0
    CURRENT_BDC_IFA_2_COMB_RAW = 1345.0
    CURRENT_BDC_IFA_3_COMB_RAW = 1345.0

    for i in range(5):
        #### HERE
        pol = 'lhcp'

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

        df.loc[i] = pd.DataFrame([pol, dac_name, TEMP_BDC_COMBINED_SCALED, CURRENT_BDC_LNA_COMB_RAW, CURRENT_BDC_RFA_COMB_RAW, CURRENT_BDC_IFA_1_COMB_RAW, CURRENT_BDC_IFA_2_COMB_RAW, CURRENT_BDC_IFA_3_COMB_RAW])


    encoder = OrdinalEncoder(categories=[['lhcp', 'rhcp']])
    df['pol'] = encoder.fit_transform(df[['pol']])

    loaded_model = joblib.load('bdc_autobias_v5.sav')
    result = loaded_model.predict(df)
    
    arr = []
    arr2 = []
    for i in range(5):
        arr.append(result[i][0])
        arr2.append(result[i][1])


    df['sweep_dac_value'] = arr
    df['TMP_BDC_LNA_COMBINED_RAW'] = arr2

    print(df)


    #fill input df 2 for normal calibration
    # i know 5 currents, dac_name, temp_bdc. i just need pol from user files.