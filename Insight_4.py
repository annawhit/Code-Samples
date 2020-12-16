import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

with open("opioid_dat.json") as opioid:
    opioid_dataframe = pd.read_json(opioid)
    opioid_dataframe = opioid_dataframe.transpose()
    opioid_dataframe = opioid_dataframe["total_claims"]
    opioid_dataframe.sort_index(inplace = True, axis = 0)

with open("economic_data.json") as econ:
    econ_dataframe = pd.read_json(econ)
    econ_dataframe = econ_dataframe.transpose()
    econ_dataframe.sort_index(inplace = True, axis = 0)
    #print(econ_dataframe.loc["Mcintosh", :])
    pop_dat = econ_dataframe[" Population (Persons)  (Number Of Persons)"]
    PCPCTR = econ_dataframe[" Per Capita Personal Current Transfer Receipts  (Dollars)"]
    PCIMB = econ_dataframe["  Per Capita Income Maintenance Benefits  (Dollars)"]
    PCUIC = econ_dataframe["  Per Capita Unemployment Insurance Compensation  (Dollars)"]
    PCRO = econ_dataframe["  Per Capita Retirement And Other  (Dollars)"]

    opd_dataframe = pd.DataFrame(opioid_dataframe/pop_dat)
    opd_dataframe.columns = ["total_claims"]
    #print(opd_dataframe)

def PCPCTR_function():
    PCPCTR_df = pd.concat([opd_dataframe, PCPCTR], axis = 1)
    PCPCTR_df.dropna(inplace = True)
    opd_series = np.array(PCPCTR_df["total_claims"]).reshape((-1, 1))
    PCPCTR_series = np.array(PCPCTR_df[" Per Capita Personal Current Transfer Receipts  (Dollars)"]).reshape((-1, 1))
    PCPCTR_lm = LinearRegression()
    PCPCTR_lm.fit(PCPCTR_series, opd_series)
    PCPCTR_sq = PCPCTR_lm.score(PCPCTR_series, opd_series)
    return " Coefficient of Determination between Per Capita Personal Current Transfer Receipts (Dollars) and Opioid Perscription Rate: {}".format(PCPCTR_sq)

def PCIMB_function():
    PCIMB_df = pd.concat([opd_dataframe, PCIMB], axis = 1)
    PCIMB_df.dropna(inplace = True)
    opd_series = np.array(PCIMB_df["total_claims"]).reshape((-1, 1))
    PCIMB_series = np.array(PCIMB_df["  Per Capita Income Maintenance Benefits  (Dollars)"]).reshape((-1, 1))
    PCIMB_lm = LinearRegression()
    PCIMB_lm.fit(PCIMB_series, opd_series)
    PCIMB_sq = PCIMB_lm.score(PCIMB_series, opd_series)
    return " Coefficient of Determination between Per Capita Income Maintenance Benefits (Dollars) and Opioid Perscription Rate: {}".format(PCIMB_sq)

def PCUIC_function():
    PCUIC_df = pd.concat([opd_dataframe, PCUIC], axis = 1)
    PCUIC_df.dropna(inplace = True)
    opd_series = np.array(PCUIC_df["total_claims"]).reshape((-1, 1))
    PCUIC_series = np.array(PCUIC_df["  Per Capita Unemployment Insurance Compensation  (Dollars)"]).reshape((-1, 1))
    PCUIC_lm = LinearRegression()
    PCUIC_lm.fit(PCUIC_series, opd_series)
    PCUIC_sq = PCUIC_lm.score(PCUIC_series, opd_series)
    return " Coefficient of Determination between Per Capita Unemployment Insurance Compensation (Dollars) and Opioid Perscription Rate: {}".format(PCUIC_sq)

def PCRO_function():
    PCRO_df = pd.concat([opd_dataframe, PCRO], axis = 1)
    PCRO_df.dropna(inplace = True)
    opd_series = np.array(PCRO_df["total_claims"]).reshape((-1, 1))
    PCRO_series = np.array(PCRO_df["  Per Capita Retirement And Other  (Dollars)"]).reshape((-1, 1))
    PCRO_lm = LinearRegression()
    PCRO_lm.fit(PCRO_series, opd_series)
    PCRO_sq = PCRO_lm.score(PCRO_series, opd_series)
    return " Coefficient of Determination between Per Capita Retirement And Other (Dollars) and Opioid Perscription Rate: {}".format(PCRO_sq)



print(PCPCTR_function())
print(PCIMB_function())
print(PCUIC_function())
print(PCRO_function())
