'''
A Static Blog Hosted In Company Network Shared Drive.

I am keeping a blog about my work in company. It serves as a venue for reflection and reference. It is only accessible from company network, as all the html files are kept in company's shared network folder.

First, this script creates the main.html. The script scan for new html files in blog directory and incrementally appends new content summary to the main page. If ever I want to generate the entire main page anew, just delete it and run the script again.

Html files are generated from org files in emacs. convert.el can convert org file to html file.

;; convert.el
(defun exportToHtml (path)
  (find-file path)
  (org-html-export-to-html)
  )
(exportToHtml "c:/blog/tg.org")
(exportToHtml "c:/blog/GoalFy15.org")
;; end convert.el
'''
import glob,re,os,time,operator

# CONSTANT
BlogDir = os.path.dirname(__file__) 
mainFileName = os.path.join(BlogDir,"main.html") 
MainPageTemplate = '''<h1 class="title">AO1's Blog</h1><hr>'''


class Page(object):
    contentInLines = ""
    path = ""
    summaryLength = 100
    def __init__(self,path):
        #TODO : use with to open and close file
        self.contentInLines = open(path,'r').readlines()
        self.path = path
    def summary(self,length = summaryLength):
        return """<div>
<a href="{path}"><h2>{title}</h2></a>
{content} ...
<br><br>modified: {modificationDateTime}
<hr>
</div>""".format(title = self.getTitle() ,
                 content = self.getContent()[0:length],
                 path = self.path, 
                 modificationDateTime = self.getModificationDateTime() )

    #WARNING: this method needs to be overriden.
    def getTitle(self):
        for line in self.contentInLines:
            titleBeginMarker = """<h1 class="title">"""
            titleEndMarker = """</h1>"""
            if  titleBeginMarker in line:
                line = line.replace(titleBeginMarker,"")
                line = line.replace(titleEndMarker,"")
                return line
        return "Untitled"
    def getModificationDateTime(self):
        return time.ctime(os.path.getmtime(self.path))

    #WARNING: this method needs to be overriden if your title appears in a different way.
    def getContent(self):
        isContent = False
        content = ""
        for line in self.contentInLines:
            contentBeginMarker = """<h1 class="title">"""
            contentEndMarker = """<div id="postamble" class="status">"""
            if isContent:
                content += line
            if contentBeginMarker in line:
                isContent = True
            if contentEndMarker in line:
                # remove all html tags
                content = re.sub(r'<.*?>', '', content)
                return content

        return "WARNING : Content not found or empty"
        
def findNewPages(directory,mainModificationDateTime):
    listing = glob.glob(directory+'/'+'*.html')
    newPagesDict = {}
    for filename in listing:
        # print filename,time.ctime(os.path.getmtime(filename))
        # print "main.html",time.ctime(mainModificationDateTime)
        # print "now",time.ctime(time.time())
        creationTimeStamp = os.path.getmtime(filename)
        if creationTimeStamp > mainModificationDateTime:
            print "new",filename,
            newPagesDict[Page(filename)] = creationTimeStamp

    sortedNewPages = sorted(newPagesDict.items(),key=operator.itemgetter(1))
    newPages = [page for (page,timestamp) in sortedNewPages]
    newPages.reverse()
    return newPages


def updateMainPage(mainFileName,newContent):
    if newContent == "":
        return #nothing to do

    updatedContent = ""
    originalContent = ""

    if os.path.exists(mainFileName):
        mainPage = open(mainFileName,'r')
        originalContent = mainPage.readlines() #exclude the last line </body></html>
        header = originalContent[0]
        originalContent = "".join(originalContent[1:]) #exclude the last line </body></html>
        mainPage.close()
    else:
        header = MainPageTemplate        

    updatedContent += header
    updatedContent += newContent
    updatedContent += originalContent

    # write updated content to main.html
    mainPage = open(mainFileName,'w')    
    mainPage.write(updatedContent)
#    print updatedContent
    
    

if __name__ == "__main__":

    mainContent = ""
    mainModificationDateTime = 0

    # get existing main content and modification date of main.html
    if os.path.exists(mainFileName):
        mainModificationDateTime = os.path.getmtime(mainFileName) #use time.ctime to convert to human readable format

    # get pages newer than main.html in blog directory
    newPages = findNewPages(BlogDir,mainModificationDateTime)
    
    # append a summary of each page to main content
    for page in newPages :
        mainContent += page.summary()

    # update main.html
    updateMainPage(mainFileName, mainContent)
    print "Main page generation completes"
