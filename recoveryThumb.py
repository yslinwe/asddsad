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
    "BOOQRyBd2JuV0J","QWYGp3Mo3ds0LrD","wYGQbX6LwgFxG3","PvMKbw0aWrFgwx","BJrq1oaKa3Cyoyr","weLG8382W3clbW","lxgM6ZmGvqcZ0q","OWkdmQpg68FZ8VV","0z911xRxeZtAdq","qM8o3P741LTzpBq","AKJA9aX2L0sXrW1","02dZGPyykYtZky","GAJyok9DXOF1Gey","DPpxLL92AAck77K","rBOpGLWZP8tbZM8","o97ZbjJDxLtJaxz","WwY4YL9mxAubxrD","8Rdlxex3egFjGW","17vB2emaDWSe48o","pD1DdO9KzQtrZxm","VyK2m19AAGCKpV3","0zvMZKOejmCLrz","9ovQLjolaOsaQ0o","ssis-285","j7j1MggAYBSLvj","23D9L4lgq6sQ3j","QgWDljV99Gc000m","miaa-599","meyd-747","dk98lL0jlLuk6YP","m3kKpLV3kzHbJA6","k9DlQL2MoxFO7eb","3rrB1dmyzeTdz4X","6XvkWa3jvZILmk","hmn-136","meyd-748","6XleAOy4oZI9zLo","KXy2l77KlRSbMR","B4YjAd3RyZuyOXP","llVO9Vv6WkUBem","P89wY2KaGMU0mR1","jul-884","RXwB4vejBaIdv0X","880BdeL8G6ior7M","XkbMzQrA0dUDk41","Rem1PPpWPjcdG1l","p13Rybp2JOSr38x","Y6JYZq0JyMhprz","G3eXQk7d7oI1MRP","0zV0J7BVdaiKvR","wlxegXjxKWCJZLr","4PYVq1LPwACKe17","ZXmLxQJX0yUMBx","ez3y04da3oCYVlg","wlArOQQOLbTJbOA","7j4Z7YlJbaCA7qB","DkblBlgWBwcBv7","wgDWr4KPPaIJmbw","WQkGyaLdAdibVeW","YBXr7mW7xaIvXWO","xPOdvV7K8vikOGP","xoko88Amb4T9DG","mgWqejbDbwIbrYA","GjW9yyg6ZOUVyl","9pzrWyerpdTY9G","4GKqqjvB3XSKj0X","OJlKQX4qkztZd2D","Wogae8woGpUbPlY","Me7dVbqkD2tmZqP","zQ21V9PDLghYY2J","b3lQZJjo8RcPzXP","qjvPA382b1sz8v8","KQZwbYAKqRH0q9l","3qbXK3vzb9Tddj8","3Jy9GBABg8cdJGy","J38ArVOblPujjQB","l2Xya0O0odf717g","kZxQGdeQzDHOOZJ","2oKOvd3R1pcP1b","YDVbbk82PGFvg6O","bpxY4oQMl7UPrlz","k2Q9Gaw0GaTDXo","XkPRJBe2GgcDRxa","re81VDKRZvfbQm0","D0prmBYoOGtkKGR","WXAzM9YMOmFbbO1","4v1ma4KoDAtKKLj","lOy0DJlLdXT7qlG","WwPL8Zvvl2spWl","ssis-269","P8KmW6L6VAsbmd","ggz9o6MdjXTq7W7","MazPlVeokRUm339","zXDB6jdPP7ukwM","GK9oPwagdWh1R9l","opgl7gAV9bcK1R","QP3WZlZMaaT0DqM","r30Dx4p361fbDrB","lAVdOkqYrGHvxQ","8R9akj77k0togvY",
]
# for key in keys:
url = f'https://raw.githubusercontent.com/popoYSL/asddsad/main/json/index.json'
req = requests.get(url,timeout=10)
indexList = json.loads(req.text)
for indexDict in indexList:
    if indexDict['linkid'] in keys:
        folderName = indexDict['folderName']
        m = re.findall(r"[a-zA-Z]+-\d+",folderName)
        if(len(m)>0):
            ids.append(m[0])
with open('link.json',"r",encoding="utf-8") as f:
    links = json.load(f)
with open('json/index.json',"r",encoding="utf-8") as f:
    indexList = json.load(f)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for result in executor.map(partial(getlink, links), indexList):
        linkDict = (result)
with open('link.json',"w",encoding="utf-8") as f:
    json.dump(linkDict,f)
with open('json/index.json',"w",encoding="utf-8") as f:
    json.dump(indexList,f)