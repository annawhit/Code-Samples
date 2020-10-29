import requests, re, pprint, json
import numpy as np
from bs4 import BeautifulSoup

with open("ZCL.html") as zip_code:
    zip_code_dat = BeautifulSoup(zip_code, "html.parser") #opens static file
    zip_code_dat_parsed = zip_code_dat.find_all(class_="inner_table")[0] #pulls table with zipcodes
    zip_code_dat_parsed = zip_code_dat_parsed.find_all("td")[5:] #finds tr (table row) tags. ignores first 5 b/c they hold useless info.
    zip_code_txt = [c.text for c in zip_code_dat_parsed] #turns trs into text
    #print(len(zip_code_txt))
    zip_code_txt = [zip_code_txt[x:x+4] for x in range(0, len(zip_code_txt), 4)] #creates a list of lists. each list is split in to [zip code, city, county, random text]
    #print(zip_code_txt)
    #print(zip_code_text_list)
    city_to_county = {}
    counrty_to_city = {}
    for line in zip_code_txt: #iterates thru list
        #print(line)
        city = line[1]
        county = line[2]
        #print(city)
        #print(county)
        #print(city, county)

    #there's two dictionaries being created here. one is for use in another folder (city_to_county), the other is to check for cities that
    #exist in 2+ counties. this is to deal with a double-counting error in 'Opioid_parser.py'

        if county not in city_to_county: #if not in dictionary, add to dictionary
            city_to_county[county] = []
            city_to_county[county].append(city)
        else: #if already in dictionary, append
            if city not in city_to_county[county]:
                city_to_county[county].append(city)

        if city not in counrty_to_city: #if not in dictionary, add to dictionary
            counrty_to_city[city] = []
            counrty_to_city[city].append(county)
        else: #if already in dictionary, append
            if county not in counrty_to_city[city]:
                counrty_to_city[city].append(county)
    #pprint.pprint(city_to_county)
    #pprint.pprint(counrty_to_city)
    json.dump(city_to_county, open("zip_codes.json", "w")) #write to json file
