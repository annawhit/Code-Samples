##import statements
import requests, pprint, re, csv, json
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from sodapy import Socrata


client = Socrata("data.cms.gov", "iAZuBNXP1aQwk9l7lH4I8MAMA" ) #API key should be valid. was working as of 10/25/2020, site does not mention expiry
client.timeout = None #must be set to none or you will get a timeout error. it is calling ~750,000 records across multiple requests. it will take time
client_dict = {}
initial = 0
for cli in range(1,17): #must be done because can only call <= 50,000 records at once
    if cli == 1:
        client_dict[cli] = client.get("77gb-8z53", nppes_provider_state = "GA", limit=50000)
    else:
        client_dict[cli] = client.get("77gb-8z53", nppes_provider_state = "GA", limit=50000, offset = initial + 1)
    initial += 50000


opd_fin_dict = {}
opioid_list = ["HYDROMORPHONE HCL", "OXYCODONE HCL/ACETAMINOPHEN", "HYDROCODONE/ACETAMINOPHEN", "ACETAMINOPHEN WITH CODEINE", "OXYCODONE HCL", "BUPRENORPHINE","MORPHINE SULFATE/NALTREXONE", "MORPHINE SULFATE", "FENTANYL", "HYDROCODONE BITARTRATE", "TRAMADOL HCL", "TRAMADOL HCL/ACETAMINOPHEN"]
for client_ofinterest in client_dict: #iterate thru all records. keep only ones where opioids were persribed
    for provider in client_dict[client_ofinterest]:
        if provider["nppes_provider_state"] == "GA":
            #pprint.pprint(provider)
            if provider["generic_name"] in opioid_list or provider["drug_name"] in opioid_list:
                if provider["nppes_provider_city"] not in opd_fin_dict:
                    city = provider["nppes_provider_city"]
                    opd_fin_dict[city] = {}
                    opd_fin_dict[city]["total_claim_count"] = int(provider["total_claim_count"])
                    opd_fin_dict[city]["drug_list"] = []
                    opd_fin_dict[city]["drug_list"].append(provider["drug_name"])
                else:
                    opd_fin_dict[city]["total_claim_count"] += int(provider["total_claim_count"])
                    if provider["drug_name"] not in opd_fin_dict[city]["drug_list"]:
                        opd_fin_dict[city]["drug_list"].append(provider["drug_name"])

json.dump(opd_fin_dict, open("opioid.json", "w"))

#pprint.pprint(opd_fin_dict)
#cross refrences with zip_codes to create a dictionary with opioid perscription data by county in GA
with open("zip_codes.json", "r") as zip_codes:
    zip_codes = json.load(zip_codes)
    opd_dict_final = {}
    bad_cities = ["Atlanta", "Commerce", "Duluth", "Acworth", "Augusta"]
    #print(zip_codes)
    for city in opd_fin_dict:
        for county in zip_codes:
            if city.title() in zip_codes[county] and city.title() not in bad_cities:
                if county not in opd_dict_final:
                    opd_dict_final[county.title()] = {}
                    opd_dict_final[county.title()][city.title()] = opd_fin_dict[city]
                else:
                    opd_dict_final[county.title()][city.title()] = opd_fin_dict[city]

    ##hardcode statements for cities that exist in two counties
    opd_dict_final["Fulton"]["Atlanta"] = opd_fin_dict["Atlanta"]
    opd_dict_final["Colombia"]["Augusta"] = opd_fin_dict["Augusta"]
    opd_dict_final["Duluth"]["Gwinnett"] = opd_fin_dict["Duluth"]
    opd_dict_final["Jackson"]["Commerce"] = opd_fin_dict["Commerce"]
    opd_dict_final["Acworth"]["Cobb"] = opd_fin_dict["Acworth"]

    #for county in opd_dict_final:

    pprint.pprint(opd_dict_final)





##looking at differiences between two data types. instead of writing na, they just leave out key
#for line in opd_dat:
    #if line['npi'] == '1003000423' or line['npi'] == '1003000407':
        #print(line)
        #pass
#for line in opd_dat:
    #print(line)
#pprint.pprint(opd_dat)


