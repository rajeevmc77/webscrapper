#!/usr/bin/env python
# coding: utf-8

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




