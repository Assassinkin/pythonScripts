import requests
import os
import random
import string
import json

chars = string.ascii_letters + string.digits +'!@#$%^&*()]}{[=+'
random.seed = (os.urandom(1024))
email_domains = ['gmail.com', 'yahoo.com', 'live.fr', 'hotmail.com', 'aol.com', 'outlook.fr', 'trash.com', 'greed.com', 'sloth.com']
names = json.loads(open('names.json').read())
surnames = json.loads(open('surnames.com').read())
words = json.loads(open('words.json').read())

# Update this with the url where the post request is carrying the login and password.
url = 'Some url you have a grudge against :p'
#how many false login and passwd you want to flood the phishing site with.
loginAttempts = 100
# how the login field is referenced in the phishing web page
login_reference = 'login'
# how the password field is referenced in the phishing web page
password_reference = 'password'

for i in range(loginAttempts):
    username = random.choice(names).lower() + random.choice(surnames).lower()
    username_extra = ''.join(random.choice(string.digit) for i in range(random.randint(1,4)))
    email_domain = random.choice(email_domains)
    _pass = random.choice(names).lower()[:random.randint(2,8)] + str(random.choice(words))[:random.randint(2,8)]
    _pass_extra = ''.join(random.choice(chars) for i in range(random.randint(1,4)))

    login = username + username_extra + '@' + email_domain
    passwd = _pass + _pass_extra

    requests.post(url, allow_redirects=False, data = {
        login_reference: login,
        password_reference: passwd
    })
    print(f'sending username {login} and password {passwd}')
