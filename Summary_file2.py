import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
#regions
northwest_ga = ["Bartow", "Catoosa", "Chattooga", "Dade", "Fannin", "Floyd", "Gilmer", "Gordon", "Haralson", "Murray", "Paulding", "Pickens", "Polk", "Walker", "Whitfield"]
mountains_ga = ["Banks", "Dawson", "Forsyth", "Franklin", "Habersham", "Hall", "Hart", "Lumpkin", "Rabun", "Stephens", "Towns", "Union", "White"]
atlanta_ga = ["Cherokee", "Clayton", "Cobb", "Dekalb", "Douglas", "Fayette", "Fulton", "Gwinnett", "Henry", "Rockdale"]
threerivers_ga = ["Butts", "Carroll", "Coweta", "Heard", "Lamar", "Meriwether", "Pike", "Spalding", "Troup", "Upson"]
northeast_ga = ["Barrow", "Clarke", "Elbert", "Greene", "Jackson", "Jasper", "Madison", "Morgan", "Newton", "Oconee", "Oglethorpe", "Walton"]
middle_ga = ["Baldwin", "Bibb", "Crawford", "Houston", "Jones", "Monroe", "Peach", "Pulaski", "Putnam", "Twiggs", "Wilkinson"]
csavannahriver_ga = ["Burke", "Columbia", "Glascock", "Hancock", "Jefferson", "Jenkins", "Lincoln", "Mcduffie", "Richmond", "Taliaferro", "Warren", "Washington", "Wilkes"]
rivervalley_ga = ["Chattahoochee", "Clay", "Crisp", "Dooly", "Harris", "Macon", "Marion", "Muscogee", "Quitman", "Randolph", "Schley", "Stewart", "Sumter", "Talbot", "Taylor", "Webster"]
heartofg_ga = ["Appling", "Bleckley", "Candler", "Dodge", "Emanuel", "Evans", "Jeff Davis", "Johnson", "Laurens", "Montgomery", "Tattnall", "Telfair", "Toombs", "Treutlen", "Wayne", "Wheeler", "Wilcox"]
southwest_ga = ["Baker", "Calhoun", "Colquitt", "Decatur", "Dougherty", "Early", "Grady", "Lee", "Miller", "Mitchell", "Seminole", "Terrell", "Thomas", "Worth"]
southern_ga = ["Atkinson", "Bacon", "Ben Hill", "Berrien", "Brantley", "Brooks", "Charlton", "Clinch", "Coffee", "Cook", "Echols", "Irwin", "Lanier", "Lowndes", "Pierce", "Tift", "Turner", "Ware"]
costal_ga = ["Bryan", "Bulloch", "Camden", "Chatham", "Effingham", "Glynn", "Liberty", "Long", "Mcintosh", "Screven"]


#code
with open("opioid_dat.json") as opioid:
    opioid_dataframe = pd.read_json(opioid)
    opioid_dataframe = opioid_dataframe.transpose()
    opioid_dataframe = opioid_dataframe["total_claims"]
    opioid_dataframe.sort_index(inplace = True, axis = 0)
    #print(opioid_dataframe)

with open("economic_data.json") as econ:
    econ_dataframe = pd.read_json(econ)
    econ_dataframe = econ_dataframe.transpose()
    #print(econ_dataframe.loc["Mcintosh", :])
    PCNE = econ_dataframe[" Per Capita Net Earnings  (Dollars)"]
    NEBPR = econ_dataframe[" Net Earnings By Place Of Residence (Thousands Of Dollars)"]
    PCPI = econ_dataframe[" Per Capita Personal Income  (Dollars)"]
    PCPCTR = econ_dataframe[" Per Capita Personal Current Transfer Receipts  (Dollars)"]
    PCIMB = econ_dataframe["  Per Capita Income Maintenance Benefits  (Dollars)"]
    PCUIC = econ_dataframe["  Per Capita Unemployment Insurance Compensation  (Dollars)"]
    PCRO = econ_dataframe["  Per Capita Retirement And Other  (Dollars)"]

overall_df = pd.concat([opioid_dataframe, PCNE, NEBPR, PCPI, PCPCTR, PCIMB, PCUIC, PCRO], axis = 1)
#print(overall_df)

northwest_ga_df = overall_df[overall_df.index.isin(northwest_ga)]
northwest_ga_df["Northwest Georgia"] = 0
northwest_ga_df = northwest_ga_df.groupby("Northwest Georgia").aggregate({"total_claims":'sum', " Per Capita Net Earnings  (Dollars)": "sum" , " Net Earnings By Place Of Residence (Thousands Of Dollars)": "sum" ,
        " Per Capita Personal Income  (Dollars)": "sum" , " Per Capita Personal Current Transfer Receipts  (Dollars)": "sum" , "  Per Capita Income Maintenance Benefits  (Dollars)" : "sum",
        "  Per Capita Unemployment Insurance Compensation  (Dollars)": "sum", "  Per Capita Retirement And Other  (Dollars)": "sum"})
northwest_ga_df.rename(index = {0: "Northwest Georgia"}, inplace = True)
#print(northwest_ga_df)

mountains_ga_df = overall_df[overall_df.index.isin(mountains_ga)]
mountains_ga_df["Georgia Mountains"] = 0
mountains_ga_df = mountains_ga_df.groupby("Georgia Mountains").aggregate({"total_claims":'sum', " Per Capita Net Earnings  (Dollars)": "sum" , " Net Earnings By Place Of Residence (Thousands Of Dollars)": "sum" ,
        " Per Capita Personal Income  (Dollars)": "sum" , " Per Capita Personal Current Transfer Receipts  (Dollars)": "sum" , "  Per Capita Income Maintenance Benefits  (Dollars)" : "sum",
        "  Per Capita Unemployment Insurance Compensation  (Dollars)": "sum", "  Per Capita Retirement And Other  (Dollars)": "sum"})
mountains_ga_df.rename(index = {0: "Georgia Mountains"}, inplace = True)


atlanta_ga_df = overall_df[overall_df.index.isin(atlanta_ga)]
atlanta_ga_df["Atlanta"] = 0
atlanta_ga_df = atlanta_ga_df.groupby("Atlanta").aggregate({"total_claims":'sum', " Per Capita Net Earnings  (Dollars)": "sum" , " Net Earnings By Place Of Residence (Thousands Of Dollars)": "sum" ,
        " Per Capita Personal Income  (Dollars)": "sum" , " Per Capita Personal Current Transfer Receipts  (Dollars)": "sum" , "  Per Capita Income Maintenance Benefits  (Dollars)" : "sum",
        "  Per Capita Unemployment Insurance Compensation  (Dollars)": "sum", "  Per Capita Retirement And Other  (Dollars)": "sum"})
atlanta_ga_df.rename(index = {0: "Atlanta"}, inplace = True)

threerivers_ga_df = overall_df[overall_df.index.isin(threerivers_ga)]
threerivers_ga_df["Three Rivers"] = 0
threerivers_ga_df = threerivers_ga_df.groupby("Three Rivers").aggregate({"total_claims":'sum', " Per Capita Net Earnings  (Dollars)": "sum" , " Net Earnings By Place Of Residence (Thousands Of Dollars)": "sum" ,
        " Per Capita Personal Income  (Dollars)": "sum" , " Per Capita Personal Current Transfer Receipts  (Dollars)": "sum" , "  Per Capita Income Maintenance Benefits  (Dollars)" : "sum",
        "  Per Capita Unemployment Insurance Compensation  (Dollars)": "sum", "  Per Capita Retirement And Other  (Dollars)": "sum"})
threerivers_ga_df.rename(index = {0: "Three Rivers"}, inplace = True)

northeast_ga_df = overall_df[overall_df.index.isin(northeast_ga)]
northeast_ga_df["Northeast Georgia"] = 0
northeast_ga_df = northeast_ga_df.groupby("Northeast Georgia").aggregate({"total_claims":'sum', " Per Capita Net Earnings  (Dollars)": "sum" , " Net Earnings By Place Of Residence (Thousands Of Dollars)": "sum" ,
        " Per Capita Personal Income  (Dollars)": "sum" , " Per Capita Personal Current Transfer Receipts  (Dollars)": "sum" , "  Per Capita Income Maintenance Benefits  (Dollars)" : "sum",
        "  Per Capita Unemployment Insurance Compensation  (Dollars)": "sum", "  Per Capita Retirement And Other  (Dollars)": "sum"})
northeast_ga_df.rename(index = {0: "Northeast Georgia"}, inplace = True)


middle_ga_df = overall_df[overall_df.index.isin(middle_ga)]
middle_ga_df["Middle Georgia"] = 0
middle_ga_df = middle_ga_df.groupby("Middle Georgia").aggregate({"total_claims":'sum', " Per Capita Net Earnings  (Dollars)": "sum" , " Net Earnings By Place Of Residence (Thousands Of Dollars)": "sum" ,
        " Per Capita Personal Income  (Dollars)": "sum" , " Per Capita Personal Current Transfer Receipts  (Dollars)": "sum" , "  Per Capita Income Maintenance Benefits  (Dollars)" : "sum",
        "  Per Capita Unemployment Insurance Compensation  (Dollars)": "sum", "  Per Capita Retirement And Other  (Dollars)": "sum"})
middle_ga_df.rename(index = {0: "Middle Georgia"}, inplace = True)


csavannahriver_ga_df = overall_df[overall_df.index.isin(csavannahriver_ga)]
csavannahriver_ga_df["Central Savannah River Area"] = 0
csavannahriver_ga_df = csavannahriver_ga_df.groupby("Central Savannah River Area").aggregate({"total_claims":'sum', " Per Capita Net Earnings  (Dollars)": "sum" , " Net Earnings By Place Of Residence (Thousands Of Dollars)": "sum" ,
        " Per Capita Personal Income  (Dollars)": "sum" , " Per Capita Personal Current Transfer Receipts  (Dollars)": "sum" , "  Per Capita Income Maintenance Benefits  (Dollars)" : "sum",
        "  Per Capita Unemployment Insurance Compensation  (Dollars)": "sum", "  Per Capita Retirement And Other  (Dollars)": "sum"})
csavannahriver_ga_df.rename(index = {0: "Central Savannah River Area"}, inplace = True)


rivervalley_ga_df = overall_df[overall_df.index.isin(rivervalley_ga)]
rivervalley_ga_df["River Valley"] = 0
rivervalley_ga_df = rivervalley_ga_df.groupby("River Valley").aggregate({"total_claims":'sum', " Per Capita Net Earnings  (Dollars)": "sum" , " Net Earnings By Place Of Residence (Thousands Of Dollars)": "sum" ,
        " Per Capita Personal Income  (Dollars)": "sum" , " Per Capita Personal Current Transfer Receipts  (Dollars)": "sum" , "  Per Capita Income Maintenance Benefits  (Dollars)" : "sum",
        "  Per Capita Unemployment Insurance Compensation  (Dollars)": "sum", "  Per Capita Retirement And Other  (Dollars)": "sum"})
rivervalley_ga_df.rename(index = {0: "River Valley"}, inplace = True)


heartofg_ga_df = overall_df[overall_df.index.isin(heartofg_ga)]
heartofg_ga_df["Heart of Georgia-Altamaha"] = 0
heartofg_ga_df = heartofg_ga_df.groupby("Heart of Georgia-Altamaha").aggregate({"total_claims":'sum', " Per Capita Net Earnings  (Dollars)": "sum" , " Net Earnings By Place Of Residence (Thousands Of Dollars)": "sum" ,
        " Per Capita Personal Income  (Dollars)": "sum" , " Per Capita Personal Current Transfer Receipts  (Dollars)": "sum" , "  Per Capita Income Maintenance Benefits  (Dollars)" : "sum",
        "  Per Capita Unemployment Insurance Compensation  (Dollars)": "sum", "  Per Capita Retirement And Other  (Dollars)": "sum"})
heartofg_ga_df.rename(index = {0: "Heart of Georgia-Altamaha"}, inplace = True)


southwest_ga_df = overall_df[overall_df.index.isin(southwest_ga)]
southwest_ga_df["Southwest Georgia"] = 0
southwest_ga_df = southwest_ga_df.groupby("Southwest Georgia").aggregate({"total_claims":'sum', " Per Capita Net Earnings  (Dollars)": "sum" , " Net Earnings By Place Of Residence (Thousands Of Dollars)": "sum" ,
        " Per Capita Personal Income  (Dollars)": "sum" , " Per Capita Personal Current Transfer Receipts  (Dollars)": "sum" , "  Per Capita Income Maintenance Benefits  (Dollars)" : "sum",
        "  Per Capita Unemployment Insurance Compensation  (Dollars)": "sum", "  Per Capita Retirement And Other  (Dollars)": "sum"})
southwest_ga_df.rename(index = {0: "Southwest Georgia"}, inplace = True)


southern_ga_df = overall_df[overall_df.index.isin(southern_ga)]
southern_ga_df["Southern Georgia"] = 0
southern_ga_df = southern_ga_df.groupby("Southern Georgia").aggregate({"total_claims":'sum', " Per Capita Net Earnings  (Dollars)": "sum" , " Net Earnings By Place Of Residence (Thousands Of Dollars)": "sum" ,
        " Per Capita Personal Income  (Dollars)": "sum" , " Per Capita Personal Current Transfer Receipts  (Dollars)": "sum" , "  Per Capita Income Maintenance Benefits  (Dollars)" : "sum",
        "  Per Capita Unemployment Insurance Compensation  (Dollars)": "sum", "  Per Capita Retirement And Other  (Dollars)": "sum"})
southern_ga_df.rename(index = {0: "Southern Georgia"}, inplace = True)


costal_ga_df = overall_df[overall_df.index.isin(costal_ga)]
costal_ga_df["Coastal"] = 0
costal_ga_df = costal_ga_df.groupby("Coastal").aggregate({"total_claims":'sum', " Per Capita Net Earnings  (Dollars)": "sum" , " Net Earnings By Place Of Residence (Thousands Of Dollars)": "sum" ,
        " Per Capita Personal Income  (Dollars)": "sum" , " Per Capita Personal Current Transfer Receipts  (Dollars)": "sum" , "  Per Capita Income Maintenance Benefits  (Dollars)" : "sum",
        "  Per Capita Unemployment Insurance Compensation  (Dollars)": "sum", "  Per Capita Retirement And Other  (Dollars)": "sum"})
costal_ga_df.rename(index = {0: "Costal"}, inplace = True)

fin_df = pd.concat([northwest_ga_df, mountains_ga_df, atlanta_ga_df, threerivers_ga_df, northeast_ga_df, middle_ga_df, csavannahriver_ga_df, rivervalley_ga_df, heartofg_ga_df, southwest_ga_df, southern_ga_df, costal_ga_df], axis = 0)
#print(fin_df)

fin_df.fillna(0)
fin_df.to_csv("Economic_Date_by_Regional_Comission.csv", index = True)
