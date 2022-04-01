# from ipaddress import v4_int_to_packed
# import sql_link,json,os

# sql_link.create()
from random import random
import re
import os,json
from time import time
import requests 
from bs4 import BeautifulSoup
import streamtape
import cloudscraper,random,time
import concurrent.futures
from functools import partial

ids = []

def getlink(links,info):
    # if not info['linkid'] in links.keys():
    folderName = info['folderName']
    m = re.findall(r"[a-zA-Z]+-\d+",folderName)
    if(len(m)>0):
        k = m[0].lower()
        # if 'ppv' in k:
        #     return links
        print(m[0])
        if m[0] in ids:
            count = 0
            while True:
                count +=1
                if count > 10:
                    break
                url = f'https://jable.tv/search/{m[0].lower()}/'
                print(url)
                htmlfile = cloudscraper.create_scraper(delay=10).get(url)
                soup = BeautifulSoup(htmlfile.text, 'html.parser')
                imgs = soup.find_all(class_='lazyload')
                if len(imgs)>0:
                    thumbUrl = imgs[0]['data-src']
                    print(thumbUrl)
                    links[info['linkid']] = thumbUrl
                    info['thumbUrl'] = thumbUrl
                    break
                time.sleep(random.randint(1,3)) 
    return links
    
keys = [
    "bpxY4oQMl7UPrlz","k2Q9Gaw0GaTDXo","kZxQGdeQzDHOOZJ","WXAzM9YMOmFbbO1","02dZGPyykYtZky","QP3WZlZMaaT0DqM","r30Dx4p361fbDrB","mgWqejbDbwIbrYA","b3lQZJjo8RcPzXP","re81VDKRZvfbQm0","XkPRJBe2GgcDRxa","GjW9yyg6ZOUVyl","3Jy9GBABg8cdJGy","3qbXK3vzb9Tddj8","l2Xya0O0odf717g","QWYGp3Mo3ds0LrD","WwPL8Zvvl2spWl","BJrq1oaKa3Cyoyr","ggz9o6MdjXTq7W7","ssis-269","PvMKbw0aWrFgwx","4GKqqjvB3XSKj0X","4PYVq1LPwACKe17","Me7dVbqkD2tmZqP","wlxegXjxKWCJZLr","MazPlVeokRUm339","GK9oPwagdWh1R9l","wgDWr4KPPaIJmbw","7j4Z7YlJbaCA7qB","Wogae8woGpUbPlY","qM8o3P741LTzpBq","G3eXQk7d7oI1MRP","weLG8382W3clbW","o97ZbjJDxLtJaxz","0zvMZKOejmCLrz","17vB2emaDWSe48o","k9DlQL2MoxFO7eb","DPpxLL92AAck77K","m3kKpLV3kzHbJA6","B4YjAd3RyZuyOXP","6XvkWa3jvZILmk","8R9akj77k0togvY","hmn-136","meyd-748","meyd-747","miaa-599","ssis-285","jul-884"
]
# for key in keys:
url = f'https://raw.githubusercontent.com/popoYSL/asddsad/main/json/index.json'
req = requests.get(url,timeout=10)
indexList = json.loads(req.text)
# with open('json/index.json',"r",encoding="utf-8") as f:
#     indexList = json.load(f)
for indexDict in indexList:
    if indexDict['linkid'] in keys:
        folderName = indexDict['folderName']
        m = re.findall(r"[a-zA-Z]+-\d+",folderName)
        if(len(m)>0):
            ids.append(m[0])
with open('link.json',"r",encoding="utf-8") as f:
    links = json.load(f)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for result in executor.map(partial(getlink, links), indexList):
        linkDict = (result)
with open('link.json',"w",encoding="utf-8") as f:
    json.dump(linkDict,f)
with open('json/index.json',"w",encoding="utf-8") as f:
    json.dump(indexList,f)