from bs4 import BeautifulSoup
import re

class MguruParser:
    def __init__(self):
        pass

    def getStoryUrl(self, content, storyTitle = 'Sheebu - the Sheep'):
        storyURL = None
        source = BeautifulSoup(content, 'html5lib')
        titleDivTag = source.find('div', text=re.compile(storyTitle, re.IGNORECASE))
        if titleDivTag:
            storyURL = titleDivTag.find_parent('a').get('href')
        return  storyURL

    def getMP3Url(self, content):
        source = BeautifulSoup(content, 'html5lib')
        audioFilePath = source.find('audio', attrs={'id':'audiofile'})
        if audioFilePath:
            audioFilePath = audioFilePath['src']
        return audioFilePath