import csv
from pip._vendor import requests
import json
import logging

# Configure logging
logging.basicConfig(filename='updateusers.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Define tenant ID and base URL for the Figma SCIM API

tenant_id = 'insert tenant'
baseurl = 'https://www.figma.com/scim/v2/'


# Define authorization token
token = 'Bearer insert token'


# Construct the users endpoint URL
users_endpoint = baseurl + tenant_id + '/Users'


# Open the CSV file containing the users to update
with open('usertoupdate.csv', 'r') as usertoupdate:
    csv_reader = csv.DictReader(usertoupdate)


    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Construct the URL to get user information based on email
        get_users_url = users_endpoint + "?filter=userName eq \"" + row['email'] + "\""
        print(get_users_url)
        try:
            # Make a GET request to fetch user information
            get_user_id = requests.get(get_users_url, headers={'Authorization': token}, data={})
            completedrequest = get_user_id.json()


            # Check if the user exists
            if completedrequest['totalResults'] > 0:
                resource = completedrequest['Resources'][0]
                users_url = users_endpoint + "/" + resource['id']
                print(users_url)
                print(resource)
                logging.info(users_url)
                logging.info(resource) #log the users_url


                # Construct the patch dictionary to update user seat type
                patchdictionary = {
                    "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
                   "Operations": [
                        {
                            "op": "remove",
                            "path": "title"
                        },
                        {
                            "op": "remove",
                            "path": "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User:department"
                        },
                        {
                            "op": "remove",
                            "path": "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User:employeeNumber"
                        }
                    ]
                }

                 # Convert the patch dictionary to JSON
                patchjson = json.dumps(patchdictionary)
                # Make a PATCH request to update the user seat type
                patch_attributes = requests.patch(users_url, headers={'Authorization': token, 'Content-Type': 'application/json'}, data=patchjson)
                
                # Check for status code 422
                if patch_attributes.status_code == 422:
                    print('Error: Received status code 422')
                    logging.error('Error: Received status code 422, which means the attributes are not present for this user')
                else:
                    patch_response = patch_attributes.text
                    print('User has been patched, here is the JSON:')
                    logging.info('User has been patched, here is the JSON:')
                    print(patch_response)
                    logging.info(patch_response)

            else:
                # Print message if user is not found
                print(row['email'] + " not found!")
                logging.info(row['email'] + " not found!")
        except requests.exceptions.RequestException as e:
            # Print error message if request fails
            print(row['email'] + " not found!", e)
            logging.error(row['email'] + " not found!", e)
