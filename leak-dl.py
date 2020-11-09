#leak-dl.py by e-operator
#part of leak-dl-NG Next Generation https://github.com/e-operator/leak-dl-NG
from pprint import pprint
import nitter_scraper
from nitter_scraper import NitterScraper
from colorama import init, Fore, Style
import datetime
from datetime import timedelta
from selenium import webdriver
import urllib.request
import cfscrape
import argparse
import hashlib
import time
import os
import re

#init colorama
init()

#setup argparse
parser = argparse.ArgumentParser()
#parser.add_argument("--cooldown",help="Time in seconds to wait between downloads. Values <3 may result in download failure.",default=3,type=float)
parser.add_argument("--no-remove-dupes",help="Do not remove duplicate files in ./pastes after all downloads are complete.",dest='noremovedupes',default=False,action='store_true')
args = parser.parse_args()

users = ["leak_scavenger"]

print(r" _                _          ______ _     ")
print(r"| |              | |         |  _  \ |    ")
print(r"| |     ___  __ _| | ________| | | | |    ")
print(r"| |    / _ \/ _` | |/ /______| | | | |    ")
print(r"| |___|  __/ (_| |   <       | |/ /| |____")
print(r"\_____/\___|\__,_|_|\_\      |___/ \_____/")

print("Starting...")

#handle leftover log.log on incomplete shutdown (KeyboardInterrupt)
try:
    os.remove("./log/log.log")
except:
    print()
else:
    print("Deleting old download list...")

#save tweets containing URLs to file ./log/log.log
for user in users:
    for tweet in nitter_scraper.get_tweets(user, pages=100):
        print()
        pprint(tweet.dict()["text"])
        f = open('./log/log.log', 'a', encoding='utf8')
        f.write(tweet.dict()["text"] + '\n')
        f.close()

#open that file
s = open("./log/log.log", "r", encoding='utf8')

#find ghostbin pastes and store in list
ghostsort = re.findall(r'ghostbin.co\S+', s.read())

#find pastebin pastes and store in list
pastesort = re.findall(r'pastebin.com\S+', s.read())

#close log.log
s.close()

#setup selenium for ghostbin because cloudflare >:(
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
browser = webdriver.Chrome(options=options)

#to tell whether or not to wait for initial cloudflare warning
run = 0

#download all ghostbin pastes it can
for x in ghostsort:
    now = datetime.datetime.now()
    file_savename = now.strftime("%m-%d-%y-%H-%M-%S")
    print(Style.BRIGHT + "[" + Fore.GREEN + "+" + Fore.RESET + "] " + Style.RESET_ALL + "Paste URL Found: " + Fore.GREEN + x + Fore.RESET)
    try:
        browser.get('https://' + x)
        if(run!=0):
            content = browser.find_element_by_css_selector('pre')
            f = open('./pastes/' + file_savename + ".txt", 'w', encoding='utf8')
            f.write(content.get_attribute('innerHTML'))
            f.close()
        else:
            time.sleep(30) # wait for cloudflare to piss off & give time to solve hcaptcha
    except:
        print(Style.BRIGHT + "[" + Fore.RED + "-" + Fore.RESET + "] " + Fore.RED + "Download error: Possible 404" + Fore.RESET + Style.RESET_ALL)
    else:
        print(Style.BRIGHT + "[" + Fore.GREEN + "+" + Fore.RESET + "] " + Fore.GREEN + "Downloaded!" + Fore.RESET + Style.RESET_ALL)
    run = run + 1
    time.sleep(1)

removed = 0

if args.noremovedupes == False:
    def md5(f):
        return hashlib.md5(open(f,'rb').read()).hexdigest()

    print(Style.BRIGHT + "[" + Fore.CYAN + "?" + Fore.RESET + "] " + Style.RESET_ALL + Fore.YELLOW + "Removing duplicates..." + Fore.RESET + Style.RESET_ALL)

    md5_dict={}
    for root, dirs, files in os.walk("./pastes"):
        for f in files:
            if not md5(os.path.join(root, f)) in md5_dict:
                md5_dict.update({md5(os.path.join(root,f)):[os.path.join(root,f)]})
            else:
                md5_dict[md5(os.path.join(root, f))].append(os.path.join(root, f))
        for key in md5_dict:
            while len(md5_dict[key])>1:
                for item in md5_dict[key]:
                    os.remove(item)
                    removed = removed + 1
                    md5_dict[key].remove(item)

    print(Style.BRIGHT + "[" + Fore.GREEN + "!" + Fore.RESET + "] " + Style.RESET_ALL + Fore.GREEN + str(removed) + " Duplicate(s) removed!" + Fore.RESET + Style.RESET_ALL)

os.remove("./log/log.log")