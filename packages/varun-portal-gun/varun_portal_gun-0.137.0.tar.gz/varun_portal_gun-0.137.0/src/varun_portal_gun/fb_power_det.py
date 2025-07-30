import joblib
import pandas as pd

from sklearn.preprocessing import OrdinalEncoder
import random

import warnings
warnings.filterwarnings("ignore")


def fb_power_det(room_temp_file):
    room_temp_df = pd.read_csv(room_temp_file)
    print(room_temp_df.to_string())


    columns = ['pol', 'sgt_fb_attn_cmd', 'p_out', 'TMP_BUC_FB_RAW']
    df = pd.DataFrame(columns=columns)

    pol = room_temp_df.iloc[0, 1]

    sgt_fb_attn_cmd = 14.5

    p_out = room_temp_df.iloc[0, 9]

    for i in range(42):
        if i < 21:
            TMP_BUC_FB_RAW = -40
        else:
            TMP_BUC_FB_RAW = 55

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