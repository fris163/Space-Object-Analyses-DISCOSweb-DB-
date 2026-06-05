
# API Pull Script for all Space Objects from the Discos Web API

# This pulls the name, mass, and entry date for each active space object in the DiscosWeb database.

# Quick Summary: accessing 'data' dictionary key on each page, which iterates over each space object, and then entering the 'attributes' key
# to pull the 'name', 'mass', and 'firstEpoch' values. Inputting each object as a dictionary into a list (all_data).

import pandas as pd
import requests
import time

## API Settings
my_API_key = "[PUT YOUR API KEY HERE]"
URL = 'https://discosweb.esoc.esa.int'

all_data = []
pagenum = 1
while True:
    response = requests.get(f'{URL}/api/objects?page[number]={pagenum}&page[size]=100', headers={
        'Authorization': f'Bearer {my_API_key}',
        'DiscosWeb-Api-Version': '2',
    },
    params = {
                # Add filter = 'active', to get only maintained (active) orbiting objects; see DISCOSweb API for all parameters
        },
    )
    
    pagenum +=1

    print("We are on page number: ", pagenum)

    time.sleep(0.3)

    if response.status_code == 200:
        
        for item in response.json()['data']:
            
            single_object_info = {}

            for key, value in item['attributes'].items():

                if key == 'name' or key == 'mass' or key =='firstEpoch':
                    single_object_info[key] = value
                
            
            for key, value in item['relationships']['reentry']['links'].items():
                if key == 'self':
                    single_object_info['reentry_link'] = value

                    
                
            all_data.append(single_object_info)
                


    elif response.status_code != 200:
        print(f"Unexpected error {response.status_code}: {response.text}")
        time.sleep(60)
        pagenum -= 1
    
    if pagenum == 910:  # there are 909 total pages
        break


print("Done, total pages: ", pagenum - 1)

# Convert the data to a dataframe and save as a csv

obj_data = pd.DataFrame(all_data)
obj_data.to_csv(r'C:\Users\[USER]\Desktop\SpaceObjects.csv', index=True)
