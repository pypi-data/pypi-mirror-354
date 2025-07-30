import joblib
import pandas as pd

from sklearn.preprocessing import OrdinalEncoder
import random

def bdc_power_det():
    columns = ['pol', 'f_in', 'sgt_attn_cmd', 'vva', 'p_in', 'f_out', 'p_out', 
            'TEMP_BDC_SCALED', 'temperature']
    p_in_arr = [-80, -76, -72, -68, -64, -60, -56, -52, -48, -44, -40, -36, -32]

    p_out_arr = [-31.8, -28.1, -24.1, -19.9, -15.7, -11.5, -7.7, -4.6, -0.5, 3.5, 8.1, 10.6, 13.9]
    TEMP_BDC_SCALED_arr = [-40, 55]

    df = pd.DataFrame(columns=columns)
    temperature = 0

    for i in range(52):
        if i < 26:
            pol = 'lhcp'
            offset = round(random.uniform(-1, 1), 3) * 2
            if i < 13:
                TEMP_BDC_SCALED = TEMP_BDC_SCALED_arr[0] + offset
                temperature = -40
                sgt_attn_cmd = 13.0
            else:
                TEMP_BDC_SCALED = TEMP_BDC_SCALED_arr[1] + offset
                temperature = 55
                sgt_attn_cmd = 19.5
        else:
            pol = 'rhcp'
            offset = round(random.uniform(-1, 1), 3) * 2
            if i < 39:
                TEMP_BDC_SCALED = TEMP_BDC_SCALED_arr[0] + offset
                temperature = -40
                sgt_attn_cmd = 19.5
            else:
                TEMP_BDC_SCALED = TEMP_BDC_SCALED_arr[1] + offset
                temperature = 55
                sgt_attn_cmd = 18.5
        p_in = p_in_arr[i % 13]
        f_in = 28.75
        vva = 4080
        f_out = 4320000000
        p_out = p_out_arr[i % 13]


        df.loc[i] = [pol, f_in, sgt_attn_cmd, vva, p_in, f_out, p_out, TEMP_BDC_SCALED, temperature]

    temperature = df.iloc[:, 8]
    X_test = df.iloc[:, [0, 2, 6, 7]]

    encoder = OrdinalEncoder(categories=[['lhcp', 'rhcp']])
    X_test['pol'] = encoder.fit_transform(X_test[['pol']])

    X_test = X_test.to_numpy()
    print(X_test)

    X_test = pd.DataFrame(X_test)

    loaded_model = joblib.load("/Users/vyelluru/Desktop/bdc_power_det_v5.sav")
    result = loaded_model.predict(X_test)


    BDC_IF_DETECT_COMB_RAW_arr = []
    TMP_BDC_LNA_COMB_SCALED_arr = []
    for i in range(len(result)):
        BDC_IF_DETECT_COMB_RAW_arr.append(result[i][0])
        TMP_BDC_LNA_COMB_SCALED_arr.append(result[i][1])
    print(result)


    X_test['pol'] = X_test.iloc[:, 0]
    X_test['sgt_attn_cmd'] = X_test.iloc[:, 1]
    X_test['p_out'] = X_test.iloc[:, 2]
    X_test['TMP_BDC_SCALED'] = X_test.iloc[:, 3]

    X_test['BDC_IF_DETECT_COMB_RAW'] = BDC_IF_DETECT_COMB_RAW_arr
    X_test['TMP_BDC_LNA_COMB_SCALED'] = TMP_BDC_LNA_COMB_SCALED_arr
    X_test['sgt_sn'] = 1
    X_test['f_in'] = df.iloc[:, 1]
    X_test['vva'] = df.iloc[:, 3]
    X_test['p_in'] = df.iloc[:, 4]
    X_test['f_out'] = df.iloc[:, 5]
    X_test['temperature'] = temperature

    X_test = X_test.iloc[:, 4:15]

    for row, index in X_test.iterrows():
        if X_test.iloc[row, 0] == 0.0:
            X_test.iloc[row, 0] = 'lhcp'
        else:
            X_test.iloc[row, 0] = 'rhcp'
    print(X_test.columns)
    print(X_test.to_string())