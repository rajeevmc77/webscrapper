import asyncio as asy
import classes.BrowserAsync as b
import classes.MguruParser as p
import classes.FileManager as f
import re
import time

class MGuruProcessorAsync:
    def __init__(self, loop = None, url='https://mguruenglish.com/login'):
        self.browser, self.fileMgr, self.parser, self.loginUrl = b.BrowserAsync(loop), f.FileManager(), p.MguruParser(), url

    async def getStoryURL(self,storyName,baseURL='https://mguruenglish.com/stories/books?level=', storyPageUrl = 'https://mguruenglish.com/stories/pages/'):
        level=1
        while level < 4:
            res = await self.browser.get(baseURL + str(level))
            if not res:
                return  None
            storyUrl =  self.parser.getStoryUrl(res, storyName)
            if storyUrl:
                storyNum = storyUrl.split('/')[-1]
                return storyPageUrl + str(storyNum)
            level = level + 1
        return None

    async def getStoryPages(self,storyURL):
        page = 0
        audioFilePath = {}
        if not storyURL:
            return None
        while True:
            url = storyURL + '/' + str(page)
            res = await self.browser.get(url)
            page = page + 1
            if not res:
                continue
            mp3Path = self.parser.getMP3Url(res)
            if not mp3Path:
                break
            audioFilePath[page] = mp3Path
        return audioFilePath

    async def savemGuruAudioForStory(self,story, audioUrls, downloadFolder='./data/download/'):
        if not audioUrls:
            return
        storyName = re.sub('[\W_]+', '', story)
        savePath = downloadFolder + storyName
        for key in audioUrls.keys():
            audioUrl = audioUrls[key]
            res = await self.browser.get(audioUrl)
            if not res:
                continue
            saveFile = savePath + '/' + storyName + '_' + str(key) + '.mp3'
            self.fileMgr.saveFile(saveFile, res)

    async def process(self,sourceStoryList = './data/data.csv'):
        print( 'StoryName,TimeTaken')
        async with self.browser.createSession() as s:
            await self.browser.Login(self.loginUrl)
            storyList = self.fileMgr.getCSVFileAsPandas(sourceStoryList)
            for index in storyList.index:
                startTime = time.time()
                storyUrl = await self.getStoryURL(storyList['Story'][index])
                if storyUrl:
                    storyUrl = storyUrl.strip()
                storyPages = await self.getStoryPages(storyUrl)
                await self.savemGuruAudioForStory(storyList['Story'][index], storyPages)
                duration = time.time() - startTime
                print(storyList['Story'][index],duration)


