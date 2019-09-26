import requests
import json
import threading
import os

IMAGE_PATH = 'images/'

NUM_THREADS = 32
DEFAULT_IMAGE = 'https://moodle.uam.es/theme/image.php/essential/core/1545157517/u/f1'
DEFAULT_IMAGE_NEW = 'https://moodle.uam.es/theme/image.php/essential/core/1568281597/u/f1'

def download_image(session, link, image_name):
    # Check if id exists
    if (image_name == -1):
        print("\t[ERROR] No image name")
        return

    # Check if link empty or default image
    if (link == '' or link == DEFAULT_IMAGE or link == DEFAULT_IMAGE_NEW):
        return

    # Check if file exists already, if so don't redownload it
    if (os.path.isfile(IMAGE_PATH + str(image_name))):
        return

    r = session.get(link)
    with open(IMAGE_PATH + str(image_name), 'wb') as f:
        f.write(r.content)
        print("[OK] Downloaded")

def main():
    s = requests.Session()

    if not os.path.exists(IMAGE_PATH):
        os.makedirs(IMAGE_PATH)

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

    mail = input("Email: ")
    password = input("Password: ")

    data = {
    'username': mail,
    'password': password
    }

    for key in headers:
        s.headers[key] = headers[key]

    print('Starting...')

    ### Get Alteon-moodle and MoodleSession cookies
    init_response = s.get("https://moodle.uam.es/")

    # Get the login token
    login_token = init_response.text.split('logintoken" value="')[1].split('"')[0]
    data['logintoken'] = login_token

    print()
    print("MoodleSession : " + str(s.cookies['MoodleSession']))
    print("Alteon-moodle : " + str(s.cookies['Alteon-moodle']))
    print("logintoken    : " + str(login_token))
    print()

    print('Gotten initial cookies and token...')
    print()

    ### Get SessionId cookie
    s.post('https://moodle.uam.es/login/index.php', data=data)

    print('Gotten session ID...')

    print()
    print("MoodleSession : " + str(s.cookies['MoodleSession']))
    print("Alteon-moodle : " + str(s.cookies['Alteon-moodle']))
    print()
    
    with open("users.json") as user_list:
        data = json.load(user_list)

        current = 0
        total = len(data['users']) - 1

        for user in data['users']:
            download_image(s, user['image'], user['id'])
            print(str(current) + "/" + str(total))
            current += 1

if __name__ == "__main__":
    main()
