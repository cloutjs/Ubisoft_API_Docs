import requests, string, random, base64

class UbiAPI(object):
    # DECLARE HEADERS AND ADD AUTH TOKEN
    # ////////////////////////////////////
    def __init__(self, auth):
        self.session = requests.Session()
        self.headers = {
            'Ubi-AppId': "2c2d31af-4ee4-4049-85dc-00dc74aef88f",
            "Ubi-RequestedPlatformType": "uplay",
            "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3",
            "Authorization": auth
        }


    # CREATE A NEW ACCOUNT
    # ////////////////////////////////////
    def create_account(self, name=None, email=None, password=None, proxies=None):
        if name is None:
            name = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(7))

        if email is None:
            email = f"{name}-{''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(7))}@gmail.com"

        if password is None:
            password = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(12))

        data = {
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

        r = self.session.post("https://public-ubiservices.ubi.com/v3/users", json=data, headers=self.headers, proxies=proxies)
        return r.json()


    # GET AN USERS PROFILE BY ID
    # ////////////////////////////////////
    def get_profile_by_id(self, user_id=None, proxies=None):
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


    # CHANGE THE AUTH TOKEN
    # ////////////////////////////////////
    def auth(self, token=None, login=None):
        if token is not None:
            self.headers["Authorization"] = token
        
        if login is not None:
            self.headers["Authorization"] = self.login(login)


    # LOGIN TO AN ACCOUNT EMAIL:PASSWORD
    # ////////////////////////////////////
    def login(self, account=None, proxies=None):
        headers = self.headers
        headers["Authorization"] = "Basic " + base64.b64encode(bytes(account, "utf-8")).decode("utf-8")
        r = self.session.post("https://public-ubiservices.ubi.com/v3/profiles/sessions", json={"Content-Type":"application/json"}, headers=headers, proxies=proxies)
        if r.status_code == 200 and r.json()["ticket"]:
            headers['Authorization'] = "Ubi_v1 t=" + r.json()["ticket"]
            return headers['Authorization']


    # CHANGE ACCOUNT NAME
    # ////////////////////////////////////
    def change_name(self, user_id=None, name=None, login=None, proxies=None): # LOGIN = "EMAIL:PASSWORD"
        if login is not None:
            headers = self.login(login)

        body={"nameOnPlatform": name}
        check_1 = self.session.post(f"https://public-ubiservices.ubi.com/v3/profiles/{user_id}/validateUpdate", data=body, headers=headers, proxies=proxies)
        check_2 = self.session.put("https://public-ubiservices.ubi.com/v3/profiles/", data=body, headers=headers, proxies=proxies)

        return [check_1.json(), check_2.json()] # RETURNS LIST INDEX [0, 1]


    # GET USER BY NAME
    # ////////////////////////////////////
    def get_user_by_name(self, name=None, proxies=None):
        r = self.session.get(f'https://public-ubiservices.ubi.com/v2/profiles?nameOnPlatform={name}&platformType=uplay', headers=self.headers, proxies=proxies)
        return r.json()


if __name__ == "__main__":
    # [OPTION #1] LOAD THE API
    # ////////////////////////////////
    account="EMAIL:PASSWORD"
    ubi = UbiAPI(UbiAPI().login(account=account))


    # [OPTION #2] LOAD THE API
    # ////////////////////////////////
    'EXAMPLE OF AN AUTH TOKEN: "Ubi_v1 t=ewogICJ2ZXIiOiAiMSIsCiAgImFpZCI6ICJhZmI0YjQzYy1mMWY3LTQxYjctYmNlZi1hNjM1ZDhjODM4MjIiLAogICJl"... (more random characters)'

    token="AUTH TOKEN"
    ubi = UbiAPI(token)


    # [EXAMPLE] HOW TO GET AN USER BY NAME
    # //////////////////////////////////////
    print(
        ubi.get_user_by_name(
            name="tristan", 
            proxies=None
        )
    )
