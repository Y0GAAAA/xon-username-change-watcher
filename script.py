from bs4 import BeautifulSoup
from database import XonoticIdUsernameDatabase, UserNotFoundException

import requests
import util

DB = XonoticIdUsernameDatabase('./players.db')
URL = 'http://xdf.teichisma.info/rating'

response = requests.get(URL)
if not response.ok:
    raise Exception(f"could not fetch player ratings: {response.reason}")

parser = BeautifulSoup(response.text, 'html.parser')
rows = parser.find_all('tr')

for row in rows[1:]:
    username_html = row.contents[1]
    username = util.get_readable_username_from_html_fragment(username_html)
    unique_identifier = username_html.a['href'].split('/')[-1]
    
    previous_username = None
    try:
        previous_username = DB.get_username(unique_identifier)
    except UserNotFoundException:
        DB.set_username(unique_identifier, username)
        continue

    if previous_username != username:
        print(f"{previous_username} --> {username}")
        DB.set_username(unique_identifier, username)

DB.close()