# This script gets the reentry data (if it exists) from a given space object using a DISCOSweb ID number.
# The data is stored in its own link for each object, so if you have 20,000 objects, 20,000 links must be accessed.


# First, import the Space Object data to get the IDs.
df = pd.read_csv(r'C:\Users\[USER]\Desktop\SpaceObjects.csv')

df = df[df['mass'].notna()].reset_index(drop=True)   # Dropping all objects without a known mass


# Getting a list of the DISCOSweb Ids (they are contained in a link)
DiscosIDs = df['reentry_link'].str.strip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,:;()[]!@#$%^&*_-+=|\\/?`~ ').astype(int).tolist()  


# Re-entry data are stored on a different link but are key matched with objects
# This block pulls all re-entry data for a given ID



my_API_key = "[YOUR API KEY HERE]"
URL = 'https://discosweb.esoc.esa.int'

reentry_data = []

# Variables for tracking counts when pulling
linknum = 1
data_num = 0

for id in DiscosIDs:  # For each ID, go to a link using that ID, and pull the reentry data

    while True:

        try:  # A try-except clause here because it takes so long, so we might get time-out errors

            attempt_num = 1

            response = requests.get(f'{URL}/api/objects/{id}/reentry', headers={
                'Authorization': f'Bearer {my_API_key}',
                'DiscosWeb-Api-Version': '2',
            },
            params = {
            })
          
        
            if response.status_code == 200:

                if response.json()['data'] != None:

                    reentry_data.append({**response.json()['data']['attributes'], 'DiscosID': id})
                    print("We are on link number: ", linknum, ", out of 39,756, RETRIEVED DATA: ", reentry_data[data_num])
                    data_num += 1
                
                else:
                    print('No reentry data for object: ', id)
                
                linknum +=1
                break
                
            
            elif response.status_code != 200:
                print(f"Unexpected error {response.status_code}: {response.text}")
                time.sleep(60 * attempt_num)
                attempt_num += 1

        except requests.exceptions.Timeout:
            print("Request timed out. Retrying...")
            continue



print("Done, total links: ", linknum)

# Save the resulting list

pd.DataFrame(reentry_data).to_csv(r'C:\Users\[USER]\Desktop\ReentryData.csv', index=True)

