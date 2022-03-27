from asyncore import write
import cloudscraper
import json
from math import fabs
import streamtape
import time
import requests
from bs4 import BeautifulSoup
import os,re
import concurrent.futures
from functools import partial

login = '3d2cb17b4037b64a9cf3'
key = 'goX9YaPq0OTvZp'
parent_folder_id = 'KYRpxWMB3_k' 

def huya_message(targeturl):
    req = requests.get(url = targeturl)
    html = req.text
    bf = BeautifulSoup(html,'lxml')
    achorname = bf.find_all(class_ = 'host-name')[0].text
    subscribe = bf.find_all(id='activityCount', class_ = 'subscribe-count')[0].text
    avatarImg = bf.find_all(id='avatar-img')[0].get('src')
    return achorname,formatSubNum(subscribe),avatarImg
def formatSubNum(subNum):
    subNum = int(subNum)
    if(subNum>=10000):
        return(str((int(subNum/1000)/10))+'万位订阅者')
    else:
        return str(subNum)+'位订阅者'
def updateThumb(indexList,thumbLinks):
    for firstFile in indexList:        
        firstFile['thumbUrl'] = getLink(firstFile["thumbUrl"],thumbLinks,firstFile['linkid'])
        id = firstFile['linkid']
        with open(os.path.join('json/video',f'{id}.json'),"r",encoding="utf-8") as f:
            fileList = json.load(f)  
        for file in fileList:
            file['thumbUrl'] = getLink(file["thumbUrl"],thumbLinks,file['linkid'])
        with open(os.path.join('json/video',f'{id}.json'),"w",encoding="utf-8") as f:
            json.dump(fileList,f)
    with open(os.path.join('json','index.json'),"w",encoding="utf-8") as f:
        json.dump(indexList,f)
    
def isHas(indexList,folderName):
    for file in indexList:
        if(file['folderName']==folderName or file['folderName']=='已经删除'):
            return True
    return False
def takeCreateTime(elem):
    try:
        ts = int(time.mktime(time.strptime(elem['created_at'], "%Y年%m月%d日 %H:%M:%S")))
    except:
        print(ts)
    return ts
def sortByCreateTime(indexList):
    if len(indexList)==0:
        return
    try:
        indexList.sort(key=takeCreateTime,reverse = True)
        return indexList
    except:
        return indexList
def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path) 
def getThumb(linkid):
    try:
        thumbData = streamtape.get_thumbnail(login,key,linkid)
        if thumbData['status']==200:
            return thumbData['result']
        count = 0
        while not (thumbData['status']==200):
            thumbData = streamtape.get_thumbnail(login,key,linkid)
            count = count +1
            if(count>3):
                return ''
            if thumbData['status']==200:
                return thumbData['result']
            time.sleep(1)
    except Exception as e:
        print('getThumb:',e)
        return ''
# def getThumbByFile(file):
#     try:
#         if(file['thumbUrl']==''):
#             linkid = file['linkid']
#             thumbData = streamtape.get_thumbnail(login,key,linkid)
#             if thumbData['status']==200:
#                 file['thumbUrl'] = thumbData['result']
#             count = 0
#             while not (thumbData['status']==200):
#                 thumbData = streamtape.get_thumbnail(login,key,linkid)
#                 count = count +1
#                 if(count>3):
#                     file['thumbUrl'] = ''
#                 if thumbData['status']==200:
#                     file['thumbUrl'] = thumbData['result']
#                 time.sleep(1)
#         print(file['name'])
#         return file
#     except Exception as e:
#         print('getThumb:',e)
#         return ''
# def updateFirstThumb(firstFile):
#     try:
#         id = firstFile['linkid']
#         with open(os.path.join('json',f'{id}.json'),"r",encoding="utf-8") as f:
#             fileList = json.load(f)
#         newfileList = []
#         with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#             for result in executor.map(getThumbByFile, fileList):
#                 newfileList.append(result)
#             with open(os.path.join('json',f'{id}.json'),"w",encoding="utf-8") as f:
#                 json.dump(newfileList,f)
#         if(firstFile['thumbUrl']==''):
#             firstFile['thumbUrl'] = getThumb(firstFile['linkid'])
#         return firstFile
#     except Exception as e:
#         print(e)
# def updateThumb(indexList):
#     newindexList = []
#     for file in indexList:
#         newindexList.append(updateFirstThumb(file))
#     with open(os.path.join('json','index.json'),"w",encoding="utf-8") as f:
#         json.dump(newindexList,f)
#     # with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#     #     for firstFile in indexList:
#     #         executor.submit(updateFirstThumb,firstFile)
            
def getfileList(fileDict):
    try:
        firstLinkId = fileDict[0]['linkid']
        with open(os.path.join('json/video',f'{firstLinkId}.json'),"r",encoding="utf-8") as f:
            fileList = json.load(f)  
    except Exception as e:
        fileList = []
    return fileList
def isNeedUpdate(fileDict,fileList):
    if(len(fileList)==len(fileDict)):
        return False
    else:
        return True
def clearReJson(indexList):
    res = []
    for i in indexList:
        if i not in res:
            res.append(i)
    return res
    
def getJableTumbUrl(html_file):
    thumburl = ''
    soup = BeautifulSoup(html_file.text, "html.parser")
    for meta in soup.find_all("meta"):
        meta_content = meta.get("property")
        if not meta_content:
            continue
        # if "og:title" == meta_content:
        #     info['title'] = meta.get("content")
        if "og:image" == meta_content:
            thumburl = meta.get("content")
    return thumburl
def getJableTumb(url):
    countNum = 0
    while True:
        try:    
            countNum +=1
            if(countNum>3):
                return ''
            htmlfile = cloudscraper.create_scraper(delay=10).get(url)
            thumburl = getJableTumbUrl(html_file=htmlfile)
            return thumburl
            # thumbUrls.append(info['image'])
            # titles.append(info['title'])
            # break
        except Exception as e:
            print(url,e)
            time.sleep(1)
def getLink(thumbUrl,thumbLinks,id):
    # m = re.findall(r"\S+-\d+",folderName)
    if id in thumbLinks.keys() :
        link = (thumbLinks[id])
        return link
    else:
        if thumbUrl == '':
            thumbUrl = getThumb(id)           
        return thumbUrl
def getFileInfo(fileDictInfo,thumbLinks,folderName,achorname,subscribe,avatarImg,file):
    if file in fileDictInfo:
        return
    file['achorname'] = achorname
    file['subscribe'] = subscribe
    file['avatar-img'] = avatarImg
    file["folderName"] = folderName
    file['name'] = file['name'][:-4] #侧边标题名称
    file['link'] = "https://streamtape.com/e/"+file['linkid'] # 视频链接videoUrl
    linkid = file['linkid']
    file['thumbUrl'] = getLink('',thumbLinks,linkid) #封面图链接
    timeArray = time.localtime(file['created_at'])
    file['created_at'] = str(time.strftime("%Y年%m月%d日 %H:%M:%S", timeArray))
    return file
def getFolderInfo(indexList,thumbLinks,achorname,subscribe,avatarImg,folder):
    parentfolder_id = folder['id']
    folderName = folder['name'] #作为标题名称
    print(folderName)
    # if(isHas(indexList,folderName)):
    #     continue
    data = streamtape.subfolder_conent(login,key,parentfolder_id)
    fileDict = data['result']['files']
    if(len(fileDict)==0):
        return '',[],indexList 
    fileDictInfo =  getfileList(fileDict)
    fileList=[]
    firstFileId = ''
    if isNeedUpdate(fileDict,fileDictInfo):
        if len(fileDict)>0:
            flagInIndex = False
            flagInIndex = isHas(indexList,folderName)
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                for result in executor.map(partial(getFileInfo, fileDictInfo,thumbLinks,folderName,achorname,subscribe,avatarImg), fileDict):
                    file = result
                    fileList.append(file)
                firstFile = fileList[0]
                firstFileId = fileList[0]['linkid']
                if not flagInIndex and not firstFile in indexList and not len(firstFile) ==0:
                    indexList.append(firstFile)
                return firstFileId,fileList,indexList    
    return '',[],indexList  
def getJson():
    mkdir('json')
    try:
        with open(os.path.join('json','index.json'),"r",encoding="utf-8") as f:
            indexList = json.load(f)  
    except Exception as e:
        print(e)
        indexList = []
    try:
        with open('link.json','r') as f:
            thumbLinks = json.load(f)
    except Exception as e:
        print(e)
        thumbLinks = []
    # indexList = clearReJson(indexList)
    updateThumb(indexList,thumbLinks)
    achorname,subscribe,avatarImg = huya_message(targeturl="https://www.huya.com/wanzi")
    countNum = 0
    while True: 
        if countNum>3:
            folderDict = {}
            break
        countNum +=1
        data = streamtape.subfolder_conent(login,key,parent_folder_id)# 第一层folder
        if data['status']==200:
            folderDict = data['result']['folders']
            break
        else:
            time.sleep(2)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for result in executor.map(partial(getFolderInfo,indexList,thumbLinks,achorname,subscribe,avatarImg), folderDict):
            firstFileId,fileList,indexList = result
            if not firstFileId == '':
                print('write',firstFileId+'.json')
                with open(os.path.join('json/video',firstFileId+'.json'),"w",encoding="utf-8") as f:
                    json.dump(fileList,f)
        if(len(indexList)>0):
            print('write','index.json')
            indexList = sortByCreateTime(indexList)
            with open(os.path.join('json','index.json'),"w",encoding="utf-8") as f:
                json.dump(indexList,f)
            for f in os.listdir('json/index'):
                if f.endswith('json'):
                    os.remove(os.path.join('json/index',f))
            n = 48  #大列表中几个数据组成一个小列表
            for i in range(0,len(indexList),n):
                with open(f'json/index/index{i}.json',"w",encoding="utf-8") as f:
                    json.dump(indexList[i:i+n],f)
            jableList = []
            tktubeList = []

            jableKeyList = []
            tktubeKeyList = []
            elelist = [] 
            eleKeyList = []
            for idkey,value in thumbLinks.items():
                if('jable' in value):
                    jableKeyList.append(idkey)
                elif('tktube' in value):
                    tktubeKeyList.append(idkey)
                else:
                    eleKeyList.append(idkey)
            for indexDict in indexList:
                if indexDict['linkid'] in jableKeyList:
                    jableList.append(indexDict)
                elif indexDict['linkid'] in tktubeKeyList:
                    tktubeList.append(indexDict)
                else:
                    elelist.append(indexDict)
            with open(f'json/category/jableindex.json',"w",encoding="utf-8") as f:
                json.dump(jableList,f)
            with open(f'json/category/tktubeindex.json',"w",encoding="utf-8") as f:
                json.dump(tktubeList,f)
            with open(f'json/category/otherindex.json',"w",encoding="utf-8") as f:
                json.dump(elelist,f)
# try:
#     with open(os.path.join('json','index.json'),"r",encoding="utf-8") as f:
#         indexList = json.load(f)  
#     indexList = indexList[::-1]  
# except:
#     indexList = []
if __name__ == '__main__':
    getJson()

# with open("./record.json",'r') as load_f:
#     load_dict = json.load(load_f)
# print(type(load_dict.keys()))
# for folder in load_dict.keys():
#     title = folder
#     fileList = load_dict[folder]
#     for fileInfo in fileList:
#         print(fileInfo['name']+'in'+folder)

