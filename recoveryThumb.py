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
    "Ox7xKAPozyik72","QWYGp3Mo3ds0LrD","LMYqbJolpvSRk87","4DqlozJ6PeiKX4y","xkK3ZegKJGHkLpY","r9GGZZlPjdUM9Q","Qgb8w6BKzxS0XGM","midv-073","gVMoRJBJveIqjqp","drpt-009","4B9dB2pyYDiJ3A","hmn-136","meyd-746","meyd-748","meyd-747","miaa-599","dVBkRgRPjjtkplD","ssis-285","jul-884","4PYVq1LPwACKe17","wlxegXjxKWCJZLr","wgDWr4KPPaIJmbw","7j4Z7YlJbaCA7qB","GjW9yyg6ZOUVyl","mgWqejbDbwIbrYA","4GKqqjvB3XSKj0X","Me7dVbqkD2tmZqP","b3lQZJjo8RcPzXP","Wogae8woGpUbPlY","kZxQGdeQzDHOOZJ","bpxY4oQMl7UPrlz","WXAzM9YMOmFbbO1","3Jy9GBABg8cdJGy","l2Xya0O0odf717g","3qbXK3vzb9Tddj8","XkPRJBe2GgcDRxa","re81VDKRZvfbQm0","k2Q9Gaw0GaTDXo","MazPlVeokRUm339","WwPL8Zvvl2spWl","ggz9o6MdjXTq7W7","ssis-269","8R9akj77k0togvY","PvMKbw0aWrFgwx","BJrq1oaKa3Cyoyr","r30Dx4p361fbDrB","QP3WZlZMaaT0DqM","voLXmKy4RPf4rB6","egM7jopb2zhYdjP","KAVOl1LJX8I0X6x","AXpOp4erwOsXojQ","2rGoywVjZYsZkpw","bKggRjbJLMHPrvZ","Xwm4Oa4yrAFALq","YL9dJGkoXlivlGx","oeQzwM04OYHx7d","Z1xLYWPpjzfgW6","4BWrKRv8V3SZxw","agLdOD72aYUxK7d","3rDmbYgO1BIdbXK","GK9oPwagdWh1R9l","zl7qaXKWGJiY1bQ","aGJLkJ4pPMtxBXo","02dZGPyykYtZky","qM8o3P741LTzpBq","weLG8382W3clbW","G3eXQk7d7oI1MRP","o97ZbjJDxLtJaxz","0zvMZKOejmCLrz","17vB2emaDWSe48o","m3kKpLV3kzHbJA6","DZDMelAVq7C3MY","k9DlQL2MoxFO7eb","DPpxLL92AAck77K","4wA12qgZ4PuKRXr","ZwgLwAD4ymCqAM7","6XvkWa3jvZILmk","B4YjAd3RyZuyOXP"
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