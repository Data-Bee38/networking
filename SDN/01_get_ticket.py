#import necessary modules for script to run correctly

import json
import requests

# define the API endpoint we want to query

api_url = "http://localhost:58000/api/v1/ticket"

# supply our credentials in the request header

headers = {

    "content-type": "application/json"
}

body_json = {
    "username": "cisco",
    "password": "cisco123!"
}

# execute our query

resp = requests.post(api_url, json.dumps(body_json), headers=headers, verify=False)

# print our request status code

print("Ticket request status: ", resp.status_code)

# gather our response details

response_json = resp.json()

serviceTicket = response_json["response"] ["serviceTicket"]

# display our result

print("The service ticket number is: ", serviceTicket)

# be a good corporate citizen and clean up after ourselves

resp = None
response_json = None
serviceTicket = None