import typer
from pathlib import Path
from typing import Optional

from typing_extensions import Annotated
import os
import pandas as pd

from .bdc_autobias import bdc_autobias
from .bdc_gain import bdc_gain
from .bdc_power_det import bdc_power_det


app = typer.Typer()


@app.callback()
def callback():
    pass


@app.command()
def predict(path: Annotated[str, typer.Option()] = None):
    print("Here are your input files: " + path)

    for filename in os.listdir(path):
        full_name = str(path) + "/" + str(filename)
        print(full_name)
        if full_name[-3:] == "csv":
            df = pd.read_csv(full_name)
            print(df)
        print(filename)

        


#Setting up inference X_tests
#plan have enough in df to run prediction then build out the rest based on pol

'''
BDC autobias
2-calls to model, one for room temp, and one for 40/55 C
'''
@app.command()
def bdc_autobias_test():
    bdc_autobias()
    print("BDC Autobias Success")



'''
BDC gain
1 row per entry
'''
@app.command()
def bdc_gain_test():
    bdc_gain()
    print("BDC Gain Success")



'''
BDC Power - -80 to -32 p_in * 2 pol's * 2 temps (52 rows)
creating an X_test df
'''
@app.command()
def bdc_power_det_test():
    bdc_power_det()
    print("BDC Power Det")

