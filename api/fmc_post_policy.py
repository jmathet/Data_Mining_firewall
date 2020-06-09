#
# Generated FMC REST API sample script
#

import json
import sys
import requests
from complete_json import complete_json

server = "https://fmcrestapisandbox.cisco.com"

username = "admin"
if len(sys.argv) > 1:
    username = sys.argv[1]
password = "sf"
if len(sys.argv) > 2:
    password = sys.argv[2]

r = None
headers = {'Content-Type': 'application/json'}
api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
auth_url = server + api_auth_path
try:
    # 2 ways of making a REST call are provided:
    # One with "SSL verification turned off" and the other with "SSL verification turned on".
    # The one with "SSL verification turned off" is commented out. If you like to use that then
    # uncomment the line where verify=False and comment the line with =verify='/path/to/ssl_certificate'
    # REST call with SSL verification turned off:
    r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username,password), verify=False)
    # REST call with SSL verification turned on: Download SSL certificates from your FMC first and provide its path for verification.
    # r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username,password), verify='/path/to/ssl_certificate')
    auth_headers = r.headers
    auth_token = auth_headers.get('X-auth-access-token', default=None)
    if auth_token == None:
        print("auth_token not found. Exiting...")
        sys.exit()
except Exception as err:
    print ("Error in generating auth token --> "+str(err))
    sys.exit()

headers['X-auth-access-token']=auth_token

api_path = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/accesspolicies"    # param
url = server + api_path
if (url[-1] == '/'):
    url = url[:-1]

# POST OPERATION

post_data = complete_json("data_api_test.xlsx")

try:
    # REST call with SSL verification turned off:
    r = requests.post(url, data=json.dumps(post_data), headers=headers, verify=False)
    # REST call with SSL verification turned on:
    # r = requests.post(url, data=json.dumps(post_data), headers=headers, verify='/path/to/ssl_certificate')
    status_code = r.status_code
    resp = r.text
    print("Status code is: "+str(status_code))
    if status_code == 201 or status_code == 202:
        print ("Post 1 was successful...")
        json_resp = json.loads(resp)
        id_resp = json_resp['id']
        print(id_resp)
        print(json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': ')))
    else :
        r.raise_for_status()
        print ("Error occurred in POST 1 --> "+resp)
except requests.exceptions.HTTPError as err:
    print ("Error in connection 1 --> "+str(err))
finally:
    if r: r.close()


 
api_path = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/accesspolicies/" + str(id_resp) + "/accessrules?bulk=True"    # param
url = server + api_path
if (url[-1] == '/'):
    url = url[:-1]
 
# POST OPERATION
with open('base_request.json') as f:
  rule_model = json.load(f)

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
print(rule_model)

post_data = [rule_model]

try:
    # REST call with SSL verification turned off:
    r = requests.post(url, data=json.dumps(post_data), headers=headers, verify=False)
    # REST call with SSL verification turned on:
    #r = requests.post(url, data=json.dumps(post_data), headers=headers, verify='/path/to/ssl_certificate')
    status_code = r.status_code
    resp = r.text
    print("Status code is: "+str(status_code))
    if status_code == 201 or status_code == 202:
        print ("Post 2 was successful...")
        json_resp = json.loads(resp)
        print(json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': ')))
    else :
        r.raise_for_status()
        print ("Error occurred in POST 2 --> "+resp)
except requests.exceptions.HTTPError as err:
    print ("Error in connection 2 --> "+str(err))
finally:
    if r: r.close()