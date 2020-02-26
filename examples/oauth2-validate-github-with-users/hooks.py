"""
Example hook to validate GitHub user login.

To be used with --oauth2-authorized-hook option

See also https://kube-web-view.readthedocs.io/en/latest/oauth2.html
"""
import aiohttp
import logging
import os

async def oauth2_authorized(data: dict, session):
    authorized_users = os.getenv("OAUTH2_AUTHORIZED_USERS").split(";")
    token = data["access_token"]
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.github.com/user", headers={"Authorization": f"token {token}"}
        ) as resp:
            user_info = await resp.json()
    login = user_info["login"]
    logging.info(f"GitHub login is {login}")
    if login not in authorized_users:
        # not authorized to access this app!
        logging.info(f"User {login} is not authorized to access.")
        return False
    logging.info(f"User {login} is authorized to access.")
    return True
