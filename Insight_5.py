import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px

max_rows = 200
max_cols = 5
pd.set_option("display.max_rows", max_rows, "display.max_columns", max_cols)

with open("opioid_dat.json") as opioid:
    opioid_dataframe = pd.read_json(opioid)
    opioid_dataframe = opioid_dataframe.transpose()
    opioid_dataframe = opioid_dataframe["total_claims"]
    opioid_dataframe.sort_index(inplace = True, axis = 0)
    #print(opioid_dataframe)

with open("economic_data.json") as econ:
    econ_dataframe = pd.read_json(econ)
    econ_dataframe = econ_dataframe.transpose()
    #econ_dataframe.sort_index(inplace = True, axis = 0)
    #print(econ_dataframe.loc["Mcintosh", :])
    pop_dat = econ_dataframe[" Population (Persons)  (Number Of Persons)"]
    pcap_net = econ_dataframe[" Per Capita Net Earnings  (Dollars)"]
    print(pcap_net)
    net_place_res = econ_dataframe[" Net Earnings By Place Of Residence (Thousands Of Dollars)"]
    per_cap_income = econ_dataframe[" Per Capita Personal Income  (Dollars)"]
    opd_dataframe = (opioid_dataframe/pop_dat)
    opd_dataframe.columns = ["total_claims"]
    #print(opd_dataframe)

    #opioid_dataframe.rename(column = {0: "total_claims"}, inplace = True)
    #print(opioid_dataframe["total_claims"])

def pcap_function():
    pcap_df = pd.DataFrame({"total_claims" : opd_dataframe, " Per Capita Net Earnings  (Dollars)" : pcap_net})
    pcap_df.dropna(inplace = True)
    pcap_df = pcap_df.round({"total_claims":6})
    #print(pcap_df)
    opd_series = np.array(pcap_df["total_claims"]).reshape(-1, 1)
    #print(opd_series)
    percapnet_series = np.array(pcap_df[" Per Capita Net Earnings  (Dollars)"]).reshape(-1, 1)
    counties = np.array(pcap_df.index)
    #print(percapnet_series)
    percapnet_lm = LinearRegression()
    percapnet_lm.fit(percapnet_series, opd_series)
    percapnet_sq = percapnet_lm.score(percapnet_series, opd_series)
    return " Coefficient of Determination between Per Capita Net Earnings (Dollars) and Opioid Perscription Rate: {}".format(percapnet_sq)

#Net Earnings By Place Of Residence (Thousands Of Dollars)
def net_place_res_function():
    net_place_res_df = pd.DataFrame({"total_claims" : opd_dataframe, " Net Earnings By Place Of Residence (Thousands Of Dollars)" : net_place_res})
    net_place_res_df.dropna(inplace = True)
    opd_series = np.array(net_place_res_df["total_claims"]).reshape((-1, 1))

    net_place_res_series = np.array(net_place_res_df[" Net Earnings By Place Of Residence (Thousands Of Dollars)"]).reshape((-1, 1))
    net_place_res_lm = LinearRegression()
    net_place_res_lm.fit(net_place_res_series, opd_series)
    net_place_res_sq = net_place_res_lm.score(net_place_res_series, opd_series)
    return " Coefficient of Determination between Net Earnings By Place Of Residence (Thousands Of Dollars) and Opioid Perscription Rate: {}".format(net_place_res_sq)

def per_cap_income_function():
    per_cap_income_df = pd.DataFrame({"total_claims" : opd_dataframe, " Per Capita Personal Income  (Dollars)" : per_cap_income})
    per_cap_income_df.dropna(inplace = True)
    opd_series = np.array(per_cap_income_df["total_claims"]).reshape((-1, 1))
    per_cap_income_series = np.array(per_cap_income_df[" Per Capita Personal Income  (Dollars)"]).reshape((-1, 1))
    per_cap_income_lm = LinearRegression()
    per_cap_income_lm.fit(per_cap_income_series, opd_series)
    per_cap_income_sq = per_cap_income_lm.score(per_cap_income_series, opd_series)
    return " Coefficient of Determination between Per Capita Personal Income (Dollars) and Opioid Perscription Rate: {}".format(per_cap_income_sq)


print(pcap_function())
print(net_place_res_function())
print(per_cap_income_function())
