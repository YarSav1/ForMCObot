# Здесь можно внутри кода менять параметры в бд, только и знай, что вставлять

import requests
from bs4 import BeautifulSoup

# Fill in your details here to be posted to the login form.
from config.functional import form_send, payload

url = 'https://minecraftonly.ru/forum/private.php?do=newpm'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/87.0.4280.88 Safari/537.36',
           'accept': '*/*'}
# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    p = s.post('https://minecraftonly.ru/', headers=HEADERS, data=payload)
    html = s.get(url, headers=HEADERS, params=None)
    if html.status_code == 200:
        # print(html.text)
        soup = BeautifulSoup(html.content, 'html.parser')
        tkn = soup.find('input', {'name':'securitytoken'})['value']
        form = form_send(tkn, 'YarSav', 'awd')
        a = s.post('https://minecraftonly.ru/forum/private.php?do=insertpm&pmid=', data=form)
        print(a.text)
        if 'Следующие пользователи не найдены:' in a.text:
            print(123123123)
        # print(soup)
        # print(s.request('body', 'https://minecraftonly.ru/forum/private.php?do=insertpm&pmid='))
        # awd = s.get('https://minecraftonly.ru/forum/private.php?do=insertpm&pmid=', data={'recipients': 'YarSav'})
        # print(awd)
