import re, os, urllib.request, urllib.parse, urllib.error

class pod():
    
    def __init__(self, rssUrl, friendlyName, downloadUrlRegex, outputFolder = "./", prepend = "", append = "", downloadedLogsFolder = "./", fileExtensionsRegex = "\.mp3"):
        self.rssUrl = rssUrl
        self.friendlyName = friendlyName
        self.loggingName = re.sub("[ _-]","",self.friendlyName)
        self.targetRegex = downloadUrlRegex
        self.prepender = prepend
        self.appender = append
        self.outputFolder = outputFolder
        self.downloadedLogsFolder = downloadedLogsFolder
        self.extRegex = fileExtensionsRegex
        
    def getDownloadedAlreadyFilename(self):
        return self.downloadedLogsFolder + self.loggingName + ".downloaded"
        
    def isAlreadyDownloaded(self, filename):
        if os.path.exists(self.getDownloadedAlreadyFilename()):
            with open(self.getDownloadedAlreadyFilename()) as f:
                for line in f:
                    line = re.sub("\n","",line)
                    if line == filename:
                        return True
        else:
            with open(self.getDownloadedAlreadyFilename(),"w+") as f:
                return False
        return False
        
    def addAlreadyDownloaded(self, filename):
        with open(self.getDownloadedAlreadyFilename(),"a") as f:
            f.write(filename+"\n")
            
    def removeAlreadyDownloaded(self, filename):
        f = open(self.getDownloadedAlreadyFilename(),"r")
        lines = f.readlines()
        f.close()
        
        with open(self.getDownloadedAlreadyFilename(),"w") as f:
            for line in lines:
                if line != filename+"\n":
                    f.write(line)
                    
    def generateDownloadedList(self):
        self.downloadAnyNewFiles(False)
        
    def downloadAnyNewFiles(self, actuallyDownload = True):
        print("-"*50)
        print("Downloading '"+self.friendlyName+"' feed @",self.rssUrl)
        
        req = urllib.request.Request(self.rssUrl, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
        htmlLines = html.decode("utf-8").split("\n")
        
        print("")
        
        print("Finding files...")
        for line in htmlLines:
            result = re.search(self.targetRegex,line)
            
            if result != None:
                fullUrl = self.prepender + result.group() + self.appender
                onlyFilename = re.search("(?<=/)[^/]+"+self.extRegex+"$", fullUrl).group()
                
                if not self.isAlreadyDownloaded(onlyFilename):
                    print("\nNext filename found")
                    try:
                        print("\tDownloading",onlyFilename,"\n\tfrom",re.sub(onlyFilename,"",fullUrl),"\n\tto",self.outputFolder)
                        self.addAlreadyDownloaded(onlyFilename)
                        
                        if actuallyDownload:
                            urllib.request.urlretrieve(fullUrl, self.outputFolder+onlyFilename )
                    except:
                        print("\tSomething went wrong, reverting logs\n")
                        self.removeAlreadyDownloaded(onlyFilename)
                else:
                    print(onlyFilename,"has already been downloaded")
        
        print("")
        
