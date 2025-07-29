import requests

def get_policies(auth):
    endpoint = "/appsec/v1/policies"
    url = auth.base_url + endpoint
    headers = auth.auth_headers("GET", endpoint)
    response = requests.get(url, headers=headers)

    if response.ok:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


def get_policy_details(auth, policy_id):
    endpoint = f"/appsec/v1/policies/{policy_id}"
    url = auth.base_url + endpoint
    headers = auth.auth_headers("GET", endpoint)
    response = requests.get(url, headers=headers)

    if response.ok:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")