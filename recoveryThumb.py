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
ids = ['JUL-874','JUL-887','SSIS-331','IPX-828']

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
# https://jable.tv/search/RAPD-004/
# https://popovideo.vercel.app/play-video.html?v=KXy2l77KlRSbMR
# login = '3d2cb17b4037b64a9cf3'
# key = 'goX9YaPq0OTvZp'
# parent_folder_id = 'KYRpxWMB3_k' 
# data = streamtape.subfolder_conent(login,key,parent_folder_id)
# folders = (data['result']['folders'])
# for folder in folders:
#     folderName = folder['name']
#     m = re.findall(r"\S+-\d+",folderName)
#     print(m)
    # data = streamtape.subfolder_conent(login,key,folder['id'])
    # print(data['result']['files'][0]['linkid'])

# for k in links.keys():
#     # print(links[k])
#     req = requests.get(f'https://popovideo.vercel.app/play-video.html?v={k}')
#     soup = BeautifulSoup(req.text,'html.parser')
#     print(soup)
#     folderName = soup.find(id = 'vid-title').text
#     print(folderName)
#     m = re.findall(r"\S+-\d+",folderName)
#     print(m)
