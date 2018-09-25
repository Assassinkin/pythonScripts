This script is used to punish people who send phishing links with letting them get what they want: tons of fake logins and passwords.


shout-out to the creator of [this video](https://www.youtube.com/watch?v=UtNYzv8gLbs&list=WL&index=14&t=0s)

### How to use this:

1. Generate a new word.json list `python3 words_gen.py`
2. open the phishing site send a fake login + password
3. Open developper tools and get the request used to send the creds you entered
4. extract the url where the request gone
5. extract the login and password fields in the html form from the request where you did extract the url
6. populate the script with the `url`, `login_reference` and `password_reference`
7. Choose hoow many time to send fake data `loginAttempts`
8. run the script: `python3 antiphishing.py`


***ENJOY***
