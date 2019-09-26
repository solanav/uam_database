import requests
import time
import json
from pprint import pprint

mock_user = {"users":[{"name":"","surname":"","image": "","id": "-1"}]}

user_list_start = '<li class="listentry"><div class="user"><a href="'
user_list_end = '</ul><div class="clearer"><!-- --></div></div></div><span class="skip-block-to" id="sb-8"></span></aside>    </div>'

name_start = 'width="16" height="16" />'
name_end = '</a></div><div class="message">'

userid_start = 'href="https://moodle.uam.es/message/index.php?id='
userid_end = '">'

image_start = '<img src="'
image_end = '"'

count = 0

def removeduplicate(it):
    seen = []
    for x in it:
        if x not in seen:
            yield x

def main():
    s = requests.Session()

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://moodle.uam.es/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    username = input("Email: ")
    password = input("Password: ")

    data = {
    'username': username,
    'password': password
    }

    for key in headers:
        s.headers[key] = headers[key]

#    print('Starting...')

    ### Get Alteon-moodle and MoodleSession cookies
    init_response = s.get("https://moodle.uam.es/")

    # Get the login token
    login_token = init_response.text.split('logintoken" value="')[1].split('"')[0]
    data['logintoken'] = login_token

    # Add cookies to session

#    print()
#    print("MoodleSession : " + str(s.cookies['MoodleSession']))
#    print("Alteon-moodle : " + str(s.cookies['Alteon-moodle']))
#    print("logintoken    : " + str(login_token))
#    print()
#
#    print('Gotten initial cookies and token...')
#    print()

    ### Get SessionId cookie
    s.post('https://moodle.uam.es/login/index.php', data=data)

#    print()
#    print("username   : " + str(data['username']))
#    print("password   : " + str(data['password']))
#    print("logintoken : " + str(data['logintoken']))
#    print()
#
#    print('Gotten session ID...')
#
#    print()
#    print("MoodleSession : " + str(s.cookies['MoodleSession']))
#    print("Alteon-moodle : " + str(s.cookies['Alteon-moodle']))
#    print()

    while(1):
        get_users(s)
        time.sleep(1)

def get_users(session):
    global count

    ### Get user page
    user_page_response = session.get("https://moodle.uam.es/my/index.php")

    out_file = open('data.html', 'w')
    out_file.write(user_page_response.text)

    count += 1

    ### Getting user list

    user_list_start_index = user_page_response.text.find(user_list_start)
    user_list_html = user_page_response.text[user_list_start_index:].split(user_list_end)[0]

    # Split it
    user_list_html = user_list_html.split("\n")
    user_list = []

    for html in user_list_html:
        tmp = User(html)
        try:
            tmp.parse_user()
            pass
        except:
            pass

        user_list.append(tmp)

    # Open last file
    try:
        with open('users.json') as json_file:
            data = json.load(json_file)
    except:
        nu_file = open('users.json', 'w')
        json.dump(mock_user, nu_file)
        nu_file.close()

        with open('users.json') as json_file:
            data = json.load(json_file)

    # Add the new users
    for user in user_list:
        if (user.generate_json() not in data['users']):
            if (user.userid != -1):
                data['users'].append(user.generate_json())
                print(user)
                print()

    # Save data to file
    with open('users.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)



class User:
    def __init__(self, html_data):
        self.name = ""
        self.surname = ""
        self.image = ""
        self.userid = -1
        self.html = html_data

    def __str__(self):
        return "Name: " + str(self.name) + "\nSurname: " + str(self.surname) + "\nImage: " + str(self.image) + "\nUserID: " + str(self.userid)

    def generate_json(self):
        return {"name": str(self.name), "surname": str(' '.join(self.surname)), "image": str(self.image), "id": str(self.userid) }

    def parse_user(self):
        full_name = self.html.split(name_start)[1].split(name_end)[0]
        self.name = full_name.split(' ')[0]
        self.surname = full_name.split(' ')[1:]
        self.image = self.html.split(image_start)[1].split(image_end)[0]
        self.image = self.image.replace("f2", "f1")
        self.userid = int(self.html.split(userid_start)[1].split(userid_end)[0])

if __name__ == "__main__":
    main()
