import random, string
from .api import *

# LOADING API
# /////////////////
account = "email:password"
ubi = UbiAPI(account)
auth_token = ubi.auth


# EXAMPLES
# /////////////////
print(
    ubi.get_user_by_name(
        name="godly", 
        proxies=None
    )
)

print(
    ubi.add_friend(
        friend_name="godly",
        account=account,
        proxies=None,
        new_login=True
    )
)

print(
    ubi.login(
        account=account, 
        proxies=None
    )
)

print(
    ubi.change_name(
        account=account,
        name="random name",
        proxies=None
    )
)

print(
    ubi.get_avatar(
        user_id="user id",
        proxies=None
    )
)

print(
    ubi.get_user_by_id(
        user_id='user id',
        proxies=None
    )
)

name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(7))
print(
    ubi.create_account(
        name=name,
        email=name + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(7)) + "@gmail.com",
        password=name + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(7)),
        proxies=None
    )
)
