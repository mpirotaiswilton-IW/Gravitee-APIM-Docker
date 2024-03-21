import requests
import json
from os import listdir, getcwd

host_name = "localhost:8083"
base_url = "http://%s/management/organizations/DEFAULT/environments/DEFAULT" % host_name
specs_dir = getcwd() + "\\api-specs\\"
spec_file_names = listdir(specs_dir)

api_uuids = list()
stdl_plans_uuids = list()
mltapi_plans_uuids = list()

get_headers = {
    'Authorization' : "Basic YWRtaW46YWRtaW4=",
    'accept' : "application/json"
}

post_headers = {
    'Authorization' : "Basic YWRtaW46YWRtaW4=",
    'Content-Type'  : "application/json",
    'accept' : "application/json"
}

delete_headers = {
    'Authorization' : "Basic YWRtaW46YWRtaW4="
}

# Import APIs to Gravitee using the OpenAPI spec files


print("Importing APIs to Gateway using OpenAPI files in " + specs_dir + ":")

for spec_file_name in spec_file_names:
    print("Importing: " + spec_file_name + "...")

    with open(specs_dir + "" + spec_file_name) as api_spec:

        api_post_content = {
            'format': "API",
            'type': "inline",
            'payload' : api_spec.read(),
            "with_documentation": True,
            "with_path_mapping": True,
            "with_policy_paths": False,
            "with_policies": [
            ]
        }

        post_api_res = requests.post(url=base_url + "/apis/import/swagger",
                                        headers= post_headers,
                                        json= api_post_content)
        print("response: " + str(post_api_res.status_code))
        if post_api_res.status_code != 201 :
            print(post_api_res.content)

get_apis_response = requests.get(url= base_url + "/apis",
                        headers= get_headers)

for api in json.loads(get_apis_response.content):
    # print(api['id'])
    api_uuids.append(api['id'])

# Create plans for each API

print("Creating plans for each API :")

for api_uuid in api_uuids:
    
    get_api_response = requests.get(url= base_url + "/apis/" + api_uuid,
                        headers= get_headers)

    api = json.loads(get_api_response.content)

    path_operator = {
        'path' : "/",
        'operator' : "STARTS_WITH"
    }

    flow = {
        'path-operator': path_operator
    }

    security_def = "{ 'propagateApiKey': True }"

    standalone_plan_post_content = {
        'name': "Standalone App",
        'description': "API plan for an app meant to only consume this API",
        'flows': [ flow ],
        'paths': {},
        'security': "API_KEY",
        'securityDefinition': security_def,
        'status': "PUBLISHED",
        'type': "API",
        'validation' : "AUTO"
    }

    multiapi_plan_post_content = {
        'name': "Multi-API App",
        'description': "API plan for an app meant to consume this as well as other APIs",
        'flows': [ flow ],
        'paths': {},
        'security': "API_KEY",
        'securityDefinition': security_def,
        'status': "PUBLISHED",
        'type': "API",
        'validation' : "AUTO"
    }

    create_stdl_plan_res =  requests.post(url=base_url + "/apis/" + api_uuid + "/plans",
                  headers=post_headers,
                  json=standalone_plan_post_content)
    
    print("Creating plans for api \"" + api['name'] + "\":")
    print("Standalone plan: " + str(create_stdl_plan_res.status_code))
    
    if create_stdl_plan_res.status_code == 201:
        stdl_plans_uuids.append(json.loads(create_stdl_plan_res.content)['id'])

    create_mltapi_plan_res =  requests.post(url=base_url + "/apis/" + api_uuid + "/plans",
                  headers=post_headers,
                  json=multiapi_plan_post_content)
    
    print("Multi-API plan: " + str(create_mltapi_plan_res.status_code))

    if create_mltapi_plan_res.status_code == 201:
        mltapi_plans_uuids.append(json.loads(create_mltapi_plan_res.content)['id'])

# Create Applications with single  subscription


print("Creating applications:")

app_names= [
    "Oracle Cloud Finance Invoices",
    "Pet Store"
]

for i in range(len(stdl_plans_uuids)):
    stdl_app_content = {
        'name': app_names[i] + " App",
        'description': "Standalone application for " + app_names[i]
    }

    print("    Creating application \"" + stdl_app_content['name'] + "\":")

    create_stdl_app_res = requests.post(url=base_url + "/applications",
                  headers=post_headers,
                  json=stdl_app_content)
    
    print("response: " + str(create_stdl_app_res.status_code))
    # print(create_stdl_app_res.content)

    stdl_app_uuid = json.loads(create_stdl_app_res.content)['id']

    print("    Creating subscription for " + stdl_app_content['name'] + ":")

    create_stdl_plan_sub_res = requests.post(url=base_url + "/apis/" + api_uuids[i] + "/subscriptions?plan=" + stdl_plans_uuids[i] + "&application=" + stdl_app_uuid,
                  headers=post_headers)
    print("response: " + str(create_stdl_plan_sub_res.status_code))
    
# Create Multi-Api App with multiple subscriptions

mltapi_app_content = {
        'name': "Centralized App",
        'description': "An application that 2 subscriptions for 2 different APIs"
    }

print("    Creating application \"" + mltapi_app_content['name'] + "\":")

create_mltapi_app_res = requests.post(url=base_url + "/applications",
                headers=post_headers,
                json=mltapi_app_content)

print("response: " + str(create_mltapi_app_res.status_code))

mltapi_app_uuid = json.loads(create_mltapi_app_res.content)['id']
for i in range(len(api_uuids)):

    print("    Creating subscription for " + mltapi_app_content['name'] + ":")


    create_mltapi_plan_sub_res = requests.post(url=base_url + "/apis/" + api_uuids[i] + "/subscriptions?plan=" + mltapi_plans_uuids[i] + "&application=" + mltapi_app_uuid,
                    headers=post_headers)
    print("response: " + str(create_mltapi_plan_sub_res.status_code))

print("Initialization now finished. Exiting Program...")