import requests
import json
from os import listdir, getcwd

host_name = "localhost:8083"

base_url = "http://%s/management/organizations/DEFAULT/environments/DEFAULT" % host_name

bearer_token = "b74d25cf-131d-4b13-8d25-cf131deb132e"

specs_dir = getcwd() + "\\api-specs\\"

all_specs = listdir(specs_dir)

print(all_specs)

test_get_headers = {
    'Authorization' : "Basic YWRtaW46YWRtaW4=",
    'accept' : "application/json"
}

test_post_headers = {
    'Authorization' : "Bearer " + bearer_token,
    'Content-Type'  : "application/json"
}

# test_get_response = requests.get(url= "http://%s/management/v1/organizations/DEFAULT" % host_name,
#                         headers= test_get_headers)

# print(test_get_response.status_code)
# print(test_get_response.content)

test_get_response = requests.get(url= base_url + "/apis",
                        headers= test_get_headers)

print(test_get_response.status_code)
print(test_get_response.content)

with open(specs_dir + "Oracle_cloud_finance_openapi_INVOICES.json") as api_spec:



    test_post_content = {
        'format': "API",
        'type': "inline",
        'payload' : api_spec.read(),
        "with_documentation": True,
        "with_path_mapping": True,
        "with_policy_paths": False,
        "with_policies": [
        ]
    }

    test_post_api_req = requests.post(url=base_url + "/apis/import/swagger",
                                    headers= test_post_headers,
                                    json= test_post_content)
    print(test_post_api_req.status_code)
    print(test_post_api_req.content)

r = requests.Response()
r.status_code = 400