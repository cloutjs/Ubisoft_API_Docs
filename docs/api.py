import requests, base64

class UbiAPI(object):
    def __init__(self, auth):
        self.session = requests.Session()
        self.auth = auth
        self.headers = {
            'Ubi-AppId': "2c2d31af-4ee4-4049-85dc-00dc74aef88f",
            "Ubi-RequestedPlatformType": "uplay",
            "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3",
            "Authorization": "Basic " + base64.b64encode(bytes(auth, "utf-8")).decode("utf-8")
        }

        r = self.session.post("https://public-ubiservices.ubi.com/v3/profiles/sessions", json={"Content-Type":"application/json"}, headers=self.headers)
        if r.status_code == 200:
            self.headers["Authorization"] = "Ubi_v1 t=" + r.json()["ticket"]
            self.session_headers = self.headers
            self.session_headers["ubi-sessionid"] = r.json()['sessionId']
            
            
    # CREATE A NEW ACCOUNT
    # ////////////////////////////////////
    def create_account(self, name=None, email=None, password=None, proxies=None):
        body = {
            'age': None,
            'confirmedEmail': email,
            'country': "GB",
            'dateOfBirth': "1989-01-18T00:00:00.00000Z",
            'email': email,
            'firstName': None,
            'isDateOfBirthApprox': False,
            'lastName': None,
            'legalOptinsKey': 'eyJ2dG91IjoiNC4wIiwidnBwIjoiNC4wIiwidnRvcyI6IjIuMSIsImx0b3UiOiJlbi1HQiIsImxwcCI6ImVuLUdCIiwibHRvcyI6ImVuLUdCIn0',
            'nameOnPlatform': name,
            'password': password,
            'preferredLanguage': "en"
        }
        r = self.session.post("https://public-ubiservices.ubi.com/v3/users", json=body, headers=self.headers, proxies=proxies)
        return r.json()


    # GET AN USERS PROFILE BY ID
    # ////////////////////////////////////
    def get_user_by_id(self, user_id=None, proxies=None):
        r = self.session.get(f"https://public-ubiservices.ubi.com/v2/profiles?userId={user_id}", headers=self.headers, proxies=proxies)
        return r.json()


    # GET AN USER AVATAR BY ID 
    # ////////////////////////////////////
    def get_avatar(self, user_id=None, proxies=None):
        r = self.session.get(f"https://ubisoft-avatars.akamaized.net/{user_id}/default_146_146.png?appId=c5393f10-7ac7-4b4f-90fa-21f8f3451a04", proxies=proxies)
        return r.json()


    # GET AN USERS UNITS OR UNIT TRANSACTIONS BY ID
    # ////////////////////////////////////////////////////
    def units(self, user_id=None, transactions=False, proxies=None):
        if transactions:
            r = self.session.get(f"https://public-ubiservices.ubi.com/v1/profiles/{user_id}/global/ubiconnect/economy/api/units/transactions?offset=0&limit=11", headers=self.headers, proxies=proxies)
            
        if not transactions:
            r = self.session.get(f"https://public-ubiservices.ubi.com/v1/profiles/{user_id}/global/ubiconnect/economy/api/units", headers=self.headers, proxies=proxies)
        return r.json()


    # LOGIN TO AN ACCOUNT EMAIL:PASSWORD
    # ////////////////////////////////////
    def login(self, account=None, proxies=None):
        headers = self.headers
        headers["Authorization"] = "Basic " + base64.b64encode(bytes(account, "utf-8")).decode("utf-8")
        r = self.session.post("https://public-ubiservices.ubi.com/v3/profiles/sessions", json={"Content-Type":"application/json"}, headers=headers, proxies=proxies)
        if r.status_code == 200:
            return [r.json(), "Ubi_v1 t=" + r.json()["ticket"], r.json()['sessionId']] # RETURNS LIST INDEX [0, 1, 2]


    # CHANGE ACCOUNT NAME
    # ////////////////////////////////////
    def change_name(self, name=None, account=None, proxies=None):
        if account is not None:
            login = self.login(account=account, proxies=proxies)
            self.session_headers["ubi-sessionid"] = login[2]
            self.session_headers["Authorization"] = login[1]

        check_1 = self.session.post(f"https://public-ubiservices.ubi.com/v3/profiles/{login[0]['userId']}/validateUpdate", data={"nameOnPlatform": name}, headers=self.session_headers, proxies=proxies)
        check_2 = self.session.put("https://public-ubiservices.ubi.com/v3/profiles/", data={"nameOnPlatform": name}, headers=self.session_headers, proxies=proxies)

        return [check_1.json(), check_2.json()] # RETURNS LIST INDEX [0, 1]


    # GET USER BY NAME
    # ////////////////////////////////////
    def get_user_by_name(self, name=None, proxies=None):
        r = self.session.get(f'https://public-ubiservices.ubi.com/v2/profiles?nameOnPlatform={name}&platformType=uplay', headers=self.headers, proxies=proxies)
        return r.json()


    # ADD A FRIEND
    # ////////////////////////////////////
    def add_friend(self, friend_name=None, account=None, proxies=None, new_login=False):
        user = self.get_user_by_name(name=friend_name, proxies=proxies)
        if new_login:
            login = self.login(account=account, proxies=proxies)
            self.session_headers["ubi-sessionid"] = login[2]
            self.session_headers["Authorization"] = login[1]
        
        r = self.session.post(f"https://public-ubiservices.ubi.com/v3/profiles/{login[0]['profileId']}/friends", json={"friends": [user['profiles'][0]['profileId']]}, headers=self.session_headers)
        if r.status_code == 200:
            return True
        return False
