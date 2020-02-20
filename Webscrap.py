#!/usr/bin/env python
# coding: utf-8
# import requests
# from bs4 import BeautifulSoup
# import re
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
# }
#
# login_data ={
#     'username': 'test_teacher',
#     'password': 'test_teacher'
# }
#
# with requests.Session() as s:
#     url =  'https://mguruenglish.com/login'
#     res = s.get(url,headers = headers)
#     res = s.post(url,data=login_data,headers = headers)
#     source = BeautifulSoup(res.content,'html5lib')
#     nameDiv = source.find('div', text= re.compile('Sheebu - the Sheep'))
#     atag = nameDiv.find_parent('a')
#     print(atag.get('href'))
#     storyUrl = 'https://mguruenglish.com/stories/pages/22/0'
#     res = s.get(storyUrl,headers = headers)
#     source = BeautifulSoup(res.content,'html5lib')
#     audioFilePath = source.find('audio', attrs={'id':'audiofile'})['src']
#     audioFileName = audioFilePath.split('/')[-1]
#     audiofile = s.get(audioFilePath,headers = headers, allow_redirects=True)
#     #with open('/rajeev/webscrap/'+audioFileName,'wb') as file:
#     #        file.write(audiofile.content)
#
#     #print(audioFilePath, audioFileName)
#     #display(HTML(res.content.decode("utf-8")))

# str = "Anaya's-123  Thumb"
# re.sub('[\W_]+', '', str)
import classes.Browser as b
import classes.MguruParser as p
import classes.FileManager as f
import re

browser, fileMgr, parser, loginUrl = None, None, None, None

def init():
    global browser, fileMgr, parser, loginUrl
    browser, fileMgr, parser = b.Browser(), f.FileManager(), p.MguruParser()
    loginUrl = 'https://mguruenglish.com/login'

def getStoryURL(storyName):
    global browser, parser
    level, baseURL , storyPageUrl = 1, 'https://mguruenglish.com/stories/books?level=', 'https://mguruenglish.com/stories/pages/'
    while level < 4 :
        res = browser.get(baseURL+str(level))
        storyUrl = parser.getStoryUrl(res.content, storyName)
        if storyUrl:
            storyNum = storyUrl.split('/')[-1]
            return  storyPageUrl+str(storyNum)
        level = level + 1
    return  None

def getStoryPages(storyURL):
    global browser, parser
    page = 0
    audioFilePath = {}
    if not storyURL:
        return  None
    while True:
        url = storyURL +'/'+ str(page)
        res = browser.get(url)
        mp3Path = parser.getMP3Url(res.content)
        if not mp3Path:
            break
        audioFilePath[page] = mp3Path
        page = page + 1
    return  audioFilePath

def savemGuruAudioForStory(story, audioUrls):
    global browser, fileMgr
    storyName = re.sub('[\W_]+', '', story)
    savePath = './data/download/' + storyName
    for key in audioUrls.keys():
        audioUrl = audioUrls[key]
        res = browser.get(audioUrl)
        saveFile = savePath + '/' + storyName + '_' + str(key) + '.mp3'
        fileMgr.saveFile(saveFile,res.content)
    pass


def main():
    global browser, fileMgr, parser, loginUrl
    init()
    with browser.createSession() as s:
        browser.Login(loginUrl)
        storyList = fileMgr.getCSVFileAsPandas('./data/data.csv')
        for index in storyList.index:
            storyUrl = getStoryURL(storyList['Story'][index])
            print(storyList['Story'][index], storyUrl)
            print(getStoryPages(storyUrl))
            savemGuruAudioForStory(storyList['Story'][index],getStoryPages(storyUrl))


if __name__ == "__main__":
    main()




