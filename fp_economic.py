##import statements
import pprint, json
import pandas as pd

##Dtype warning may pop up when run. Columns that cause the error are later deleted. Ignore.


with open("CAINC30__ALL_AREAS_1969_2018.csv", "r") as exc_da:
    #print(pd_excel_data.size())
    pd_excel_data = pd.read_csv(exc_da, encoding = "utf-8") #data to dataframe
    pd_excel_data = pd_excel_data.drop(["TableName", "LineCode", "Region"], axis = 1) #dropping etranious information
    pd_excel_data = pd_excel_data.drop([99138, 99139, 99140], axis = 0) #dropping rows at the bottom that do not contain data
    pd_excel_data = pd_excel_data.drop(pd_excel_data.loc[:, "1969":"2017"].columns, axis = 1) # Dropping years we will not use
    pd_excel_data =  pd_excel_data[pd_excel_data["GeoName"].str.contains("GA")]
    #print(pd_excel_data)

    CAINC30_dict = {}
    for row in pd_excel_data.itertuples(): #iterates through each row in dataframe
        county = row[2][:-4] #removes ', GA' from each county
        if county not in CAINC30_dict:
            CAINC30_dict[county] = {} #creates subdict
            CAINC30_dict[county][row[3].title()] = row[5]
        else:
            if row[3][-1] == "/": #remove weird backslashes at end of rows
                CAINC30_dict[county][(row[3][0:-2] + " (" + row[4] + ")").title()] = row[5]
            elif row[3][-1] == ")": #if it already has units, don't add units
                CAINC30_dict[county][row[3]] = row[5]
            else: #if it doesn't have weird backslashes or units attached
                CAINC30_dict[county][(row[3] + " (" + row[4] + ")").title()] = row[5]
            #there is no case of both weird backslashes and units

json.dump(CAINC30_dict, open('economic_data.json', 'w'))
#pprint.pprint(CAINC30_dict)
