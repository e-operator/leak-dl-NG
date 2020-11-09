#leak-dl.py by e-operator
#part of leak-dl-NG Next Generation https://github.com/e-operator/leak-dl-NG
from pprint import pprint
import nitter_scraper
from nitter_scraper import NitterScraper
from colorama import init, Fore, Style
import datetime
from datetime import timedelta
#from selenium import webdriver
import urllib.request
import cfscrape
import argparse
import hashlib
import time
import os
import re

#init colorama
init()

parser = argparse.ArgumentParser()
parser.add_argument("--cooldown",help="Time in seconds to wait between downloads. Values <3 may result in download failure.",default=3,type=float)
parser.add_argument("--no-remove-dupes",help="Do not remove duplicate files in ./pastes after all downloads are complete.",dest='noremovedupes',default=False,action='store_true')
args = parser.parse_args()

users = ["leak_scavenger"]

print(r" _                _          ______ _     ")
print(r"| |              | |         |  _  \ |    ")
print(r"| |     ___  __ _| | ________| | | | |    ")
print(r"| |    / _ \/ _` | |/ /______| | | | |    ")
print(r"| |___|  __/ (_| |   <       | |/ /| |____")
print(r"\_____/\___|\__,_|_|\_\      |___/ \_____/")

print("Starting..")

try:
    os.remove("./log/log.log")
except:
    print("log.log not detected; skipping deletion...")
else:
    print("Deleting old download list...")

for user in users:
    for tweet in nitter_scraper.get_tweets(user, pages=100):
        print()
        pprint(tweet.dict()["text"])
        f = open('./log/log.log', 'a', encoding='utf8')
        f.write(tweet.dict()["text"] + '\n')
        f.close()

s = open("./log/log.log", "r", encoding='utf8')

firstsort = re.findall(r'pastebin.com\S+', s.read())

for x in firstsort:
    now = datetime.datetime.now()
    file_savename = now.strftime("%m-%d-%y-%H-%M-%S")
    print(Style.BRIGHT + "[" + Fore.GREEN + "+" + Fore.RESET + "] " + Style.RESET_ALL + "Paste URL Found: " + Fore.GREEN + x + Fore.RESET)
    try:
        urllib.request.urlretrieve("https://" + x, './pastes/' + file_savename + ".txt" )
    except:
        print(Style.BRIGHT + "[" + Fore.RED + "-" + Fore.RESET + "] " + Fore.RED + "Download error: Possible 404" + Fore.RESET + Style.RESET_ALL)
    else:
        print(Style.BRIGHT + "[" + Fore.GREEN + "+" + Fore.RESET + "] " + Fore.GREEN + "Downloaded!" + Fore.RESET + Style.RESET_ALL)

    time.sleep(3)

removed = 0

s.close()

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