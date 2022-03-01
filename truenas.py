import requests

class TrueNAS:
    endpoint = ""
    api_key = ""
    verify_certificate = False
    requests_header = dict()

    def __init__(self, endpoint, api_key, verify_certificate=False):
        if not api_key:
            raise ValueError("API key cannot be empty")
        self.endpoint = endpoint
        self.api_key = api_key
        self.verify_certificate = verify_certificate
        self.requests_header = {
            "Authorization": "Bearer " + self.api_key,
        }
    
    def validate_password(self, username, password):
        body = {
            "username": username,
            "password": password,
        }
        r = requests.post(
            self.endpoint + "/api/v2.0/auth/check_password", 
            headers=self.requests_header, 
            json=body,
            verify=self.verify_certificate
        )
        
        return r.status_code == 200 and type(r.json()) == bool and r.json() is True

    def update_password(self, id, password):
        body = {
            "password": password
        }
        r = requests.put(
            self.endpoint + "/api/v2.0/user/id/" + id,
            json=body,
            verify=self.verify_certificate
        )
        return r.status_code == 200


    def get_user_info(self, username):
        params = {
            username: username
        }
        r = requests.get(
            self.endpoint + "/api/v2.0/user",
            headers=self.requests_header,
            params=params,
            verify=self.verify_certificate
        )
        return r.json()
