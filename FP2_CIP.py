#this code requires plotly, geopandas, and dependencies to run
#this code creates a map showing opioid use for all counties in georgia

# import necessary libraries
import pandas as pd
import numpy as np
import geopandas
import shapely
import shapefile
import plotly
from plotly.figure_factory._county_choropleth import create_choropleth
import xlrd
# Check your version
print(plotly.__version__, geopandas.__version__,shapely.__version__,shapefile.__version__)


with open("opioid_dat.json") as opd_json:
    opioid_dataframe = pd.read_json(opd_json)
    opioid_dataframe = opioid_dataframe.transpose()
    opioid_dataframe = opioid_dataframe["total_claims"]
    opioid_dataframe.sort_index(inplace = True, axis = 0)
    opioid_dataframe.fillna(0, inplace = True)
    #print(opioid_dataframe)

with open("state_and_county_fips_master.csv") as sc:
    sc_df = pd.read_csv(sc)
    sc_df = sc_df[sc_df["state"] == "GA"]
    sc_df["name"] = sc_df["name"].str[0:-7].str.title()
    sc_df.reset_index(inplace = True)
    sc_df.set_index(sc_df["name"], inplace = True)
    sc_df.drop(["state", "index"], axis = 1, inplace = True)
    #print(sc_df)
fin_df = pd.concat([sc_df, opioid_dataframe], axis = 1)



#df_sample = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/minoritymajority.csv')
#df_sample_r = df_sample[df_sample['STNAME'] == 'Georgia']
#print(df_sample_r)

values = fin_df['total_claims'].tolist()
fips = fin_df["fips"].tolist()

endpts = list(np.mgrid[min(values) + 1:max(values):14j])
print(endpts)
colorscale = ["#08396C","#0A4C79","#0C6185","#0F7892","#11919E",
              "#14AAA7","#1AC19A","#1DCC91","#32D386","#47DA7F", "#5CE07C", "#72E67E", "#8CEB89", "#ADF09F", "#CAF4B7", "#E1F8CE"]
fig = create_choropleth(
    fips=fips, values=values, scope=['Georgia'], show_state_data=True,
    colorscale=colorscale, binning_endpoints=endpts, round_legend_values=True,
    plot_bgcolor='rgb(229,229,229)',
    paper_bgcolor='rgb(229,229,229)',
    legend_title='Opioid Prescriptions by County',
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},
    exponent_format=True,
)
fig.layout.template = None
fig.show()
