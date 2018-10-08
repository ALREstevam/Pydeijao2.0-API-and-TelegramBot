import urllib


class DowloadHtmlPage:
    def downloadToFile(self, link, tofile):
        myfile = urllib.request.urlopen(link).read()
        with open(tofile, 'wb') as writeFileObj:
            writeFileObj.write(myfile)