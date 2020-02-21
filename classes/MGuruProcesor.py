import classes.Browser as b
import classes.MguruParser as p
import classes.FileManager as f
import re
import time

class MGuruProcessor:
    def __init__(self, url='https://mguruenglish.com/login'):
        self.browser, self.fileMgr, self.parser, self.loginUrl = b.Browser(), f.FileManager(), p.MguruParser(), url

    def getStoryURL(self,storyName,baseURL='https://mguruenglish.com/stories/books?level=', storyPageUrl = 'https://mguruenglish.com/stories/pages/'):
        level=1
        while level < 4:
            res = self.browser.get(baseURL + str(level))
            if not res:
                return  None
            storyUrl = self.parser.getStoryUrl(res.content, storyName)
            if storyUrl:
                storyNum = storyUrl.split('/')[-1]
                return storyPageUrl + str(storyNum)
            level = level + 1
        return None

    def getStoryPages(self,storyURL):
        page = 0
        audioFilePath = {}
        if not storyURL:
            return None
        while True:
            url = storyURL + '/' + str(page)
            res = self.browser.get(url)
            page = page + 1
            if not res:
                continue
            mp3Path = self.parser.getMP3Url(res.content)
            if not mp3Path:
                break
            audioFilePath[page] = mp3Path
        return audioFilePath

    def savemGuruAudioForStory(self,story, audioUrls, downloadFolder='./data/download/'):
        storyName = re.sub('[\W_]+', '', story)
        savePath = downloadFolder + storyName
        for key in audioUrls.keys():
            audioUrl = audioUrls[key]
            res = self.browser.get(audioUrl)
            if not res:
                continue
            saveFile = savePath + '/' + storyName + '_' + str(key) + '.mp3'
            self.fileMgr.saveFile(saveFile, res.content)

    def process(self,sourceStoryList = './data/data.csv'):
        print( 'StoryName,TimeTaken')
        with self.browser.createSession() as s:
            self.browser.Login(self.loginUrl)
            storyList = self.fileMgr.getCSVFileAsPandas(sourceStoryList)
            for index in storyList.index:
                startTime = time.time()
                storyUrl = self.getStoryURL(storyList['Story'][index]).strip()
                self.savemGuruAudioForStory(storyList['Story'][index], self.getStoryPages(storyUrl))
                duration = time.time() - startTime
                print(storyList['Story'][index],duration)


