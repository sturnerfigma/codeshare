##Script to read through a CSV and leverage Figma's SCIM API to remove the user and disallow them rejoining the organization.
##The target for the CSV should be Guest users identified by customer
##The result is the user will not be able to take a link and rejoin Figma.


#imports necessary libraries
import csv
from pip._vendor import requests
import json


#You must have saml/sso  configured and in place to leverage the SCIM API
#make sure to replace the [custom tenant id] with your id from your SSO settings
#make sure to generate your scim api token, replace [API Token]

TENANT_ID = '[Custom Tenant ID]'
BASEURL = 'https://www.figma.com/scim/v2/'
API_TOKEN = 'Bearer [API Token]'
GET_USERS_URL = BASEURL + TENANT_ID + '/Users'

#parses through csv
with open('userstoremove.csv', 'r') as userstoremove:
    csv_reader = csv.DictReader(userstoremove)
    #below is the statement that will loop through the csv 1 row at a time
    for row in csv_reader:
        #below prompts terminal with user we are connecting to
        print("We will now remove " + row['email'] + " with SCIM.")
        #below is the body request json we are going to send to Figma
        bindreqdata = {"schemas":["urn:ietf:params:scim:schemas:core:2.0:User"], "userName": row["email"], "givenName": row["givenName"], "familyName": row["familyName"], "displayName": row["displayName"], "active": False}
        bindjson = json.dumps(bindreqdata)
        #below is the binding post request to connect to the existing user
        res = requests.post(GET_USERS_URL, headers= {'Authorization': API_TOKEN, 'Content-Type': 'application/json'}, data = bindjson)
        completedres = res.json()
        print("We have added the User " + completedres["userName"] + " to your SCIM log with a deleted status, this will prevent them from joining your organization.")
        
        
    
