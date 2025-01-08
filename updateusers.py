import csv
from pip._vendor import requests
import json


# Define tenant ID and base URL for the Figma SCIM API
tenant_id = 'tenantid'
baseurl = 'https://www.figma.com/scim/v2/'


# Define authorization token
token = 'Bearer inserttoken'


# Construct the users endpoint URL
users_endpoint = baseurl + tenant_id + '/Users'


# Open the CSV file containing the users to update
with open('update_users_with_seat.csv', 'r') as usertoupdate:
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


                # Construct the patch dictionary to update user seat type
                patchdictionary = {
                    "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
                    "Operations": [{
                        "op": "remove",
                        "path": "title",
                        #comment or uncomment the below value attribute to read from csv or set to manage in Figma "null" value
                        #"value": row['seat_type']
                        #"value": "null"
                    }]
                }


                # Convert the patch dictionary to JSON
                patchjson = json.dumps(patchdictionary)
                # Make a PATCH request to update the user seat type
                patch_user_seat_status = requests.patch(users_url, headers={'Authorization': token, 'Content-Type': 'application/json'}, data=patchjson)
                patch_response = patch_user_seat_status.text
                print('User has been patched, here is the JSON:')
                print(patch_response)
            else:
                # Print message if user is not found
                print(row['email'] + " not found!")
        except requests.exceptions.RequestException as e:
            # Print error message if request fails
            print(row['email'] + " not found!", e)
