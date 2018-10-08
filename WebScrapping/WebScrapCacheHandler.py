import urllib
import json
from WebScrapping.DownloadHtmlPage import DowloadHtmlPage
import os
import datetime
from dateutil import parser
from datetime import datetime
import datetime as dt
import time
from WebScrapping.MyWebScrapping import BandecoWebScrapper



def myconverter(o):
    return o.__str__()

class WSCache:

    def __init__(self, url='https://www.pfl.unicamp.br/Restaurante/view/site/cardapio.php'):
        self.jsonInfoPath = 'info.json'
        self.localFilePath = 'local.html'
        self.localFilePath2 = 'local2.html'
        self.jsonData = 'cache.json'
        self.url = url

    def get_data(self):
        size = self.page_size_no_download()

        print(size)
        if size is None:
            size = self.page_size_download()

        print(size)

    def page_size_no_download(self):
        import urllib.request
        site = urllib.request.urlopen(self.url)
        return site.length

    def page_size_download(self):
        DowloadHtmlPage().downloadToFile(self.url, self.localFilePath2)
        size = os.path.getsize(self.localFilePath)
        self.log_new_download(size)

        self.localFilePath2, self.localFilePath = self.localFilePath, self.localFilePath2 #swap

        return size

    def last_download_size(self):
        with open("replayScript.json", "r+") as jsonFile:
            data = json.load(jsonFile)
            return data['lastDownloadSize']

    def content_is_different_from_last(self):
        with open(self.localFilePath) as f1:
            with open(self.localFilePath2) as f2:
                return f1.read() == f2.read()


    def hours_passed_since_last(self):
        with open("replayScript.json", "r+") as jsonFile:
            data = json.load(jsonFile)
            d1 = parser.parse(data['downloadDate'])
            d2 = datetime.datetime.now()
            fmt = '%Y-%m-%d %H:%M:%S'
            diff = d2 - d1
            diff_minutes = (diff.days * 24 * 60) + (diff.seconds / 60)
            return diff_minutes

    def log_new_download(self, size):
        with open(self.jsonInfoPath, "r+") as jsonFile:
            data = json.load(jsonFile)
            data['lastDownloadSize'] = size
            data['downloadDate'] = dt.datetime.now()
            jsonFile.seek(0)  # rewind
            json.dump(data, jsonFile, default=myconverter)
            jsonFile.truncate()


c = WSCache()
c.get_data()