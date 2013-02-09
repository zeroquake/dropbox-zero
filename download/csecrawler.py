import os, os.path, sys, re, commands, pickle, tempfile, getopt
import socket, string, random, threading, time, traceback
from optparse import OptionParser
import StringIO, urllib2, logging, datetime, unicodedata, urlparse, string
MAX_LEVEL=2
HREF_RE = re.compile('href\s*=\s*[\'"](.*?)[\'"]')
DEST_RES = [
    #only chair  
    #(re.compile('/[cC][hH][aA][iI][rR]'), re.compile('[eE][dD][uU]')),
    #(re.compile('/[cC][hH][aA][iI][rR][sS]'), re.compile('[eE][dD][uU]')),
    #(re.compile('/[cC][hH][aA][iI][rR][sS]/'), re.compile('[eE][dD][uU]')),
    #(re.compile('/[cC][hH][aA][iI][rR]/'), re.compile('[eE][dD][uU]')),
    #cis
    #(re.compile('(//|w.)[cC][iI][sS]\.'), re.compile('[fF][aA][cC][uU][lL][tT][yY]')),
    #(re.compile('/[cC][iI][sS]/'), re.compile('[fF][aA][cC][uU][lL][tT][yY]')),
    #(re.compile('(//|w.)[cC][iI][sS]\.'), re.compile('[cC][hH][aA][iI][rR]')),
    #(re.compile('(//|w.)[cC][iI][sS]\.'), re.compile('[cC][hH][aA][iI][rR][sS]')),
    #(re.compile('/[cC][iI][sS]/'), re.compile('[cC][hH][aA][iI][rR]')),
    #(re.compile('/[cC][iI][sS]/'), re.compile('[cC][hH][aA][iI][rR][sS]')),
    # (re.compile('(//|w.)[cC][iI][sS]\.'), re.compile('[pP][eE][oO][pP][lL][eE]')),
    #(re.compile('/[cC][iI][sS]/'), re.compile('[pP][eE][oO][pP][lL][eE]')),
    #cs
    (re.compile('(//|w.)[cC][sS]\.'), re.compile('[fF][aA][cC][uU][lL][tT][yY]')),
    (re.compile('/[cC][sS]/'), re.compile('[fF][aA][cC][uU][lL][tT][yY]')),
    (re.compile('(//|w.)[cC][sS]\.'), re.compile('[eE][dD][uU]')),
    (re.compile('/[cC][sS]/'), re.compile('[eE][Dd][uU]')),
    #(re.compile('(//|w.)[cC][sS]\.'), re.compile('[cC][hH][aA][iI][rR]')),
    #(re.compile('(//|w.)[cC][sS]\.'), re.compile('[cC][hH][aA][iI][rR][sS]')),
    #(re.compile('/[cC][sS]/'), re.compile('[cC][hH][aA][iI][rR]')),
    #(re.compile('/[cC][sS]/'), re.compile('[cC][hH][aA][iI][rR][sS]')),
    #(re.compile('(//|w.)[cC][sS]\.'), re.compile('[pP][eE][oO][pP][lL][eE]')),
    #(re.compile('/[cC][sS]/'), re.compile('[pP][eE][oO][pP][lL][eE]')),
    #cse
    #(re.compile('(//|w.)[cC][sS][eE]\.'), re.compile('[cC][hH][aA][iI][rR][sS]')),
    #(re.compile('(//|w.)[cC][sS][eE]\.'), re.compile('[cC][hH][aA][iI][rR]')),
    #(re.compile('/[cC][sS][eE]/'), re.compile('[cC][hH][aA][iI][rR][sS]')),
    #(re.compile('/[cC][sS][eE]/'), re.compile('[cC][hH][aA][iI][rR]')),
    (re.compile('(//|w.)[cC][sS][eE]\.'), re.compile('[fF][aA][cC][uU][lL][tT][yY]')),
    (re.compile('/[cC][sS][eE]/'), re.compile('[fF][aA][cC][uU][lL][tT][yY]')),
    (re.compile('(//|w.)[cC][sS][eE]\.'), re.compile('[eE][dD][uU]')),
    (re.compile('/[cC][sS][eE]/'), re.compile('[eE][Dd][uU]')),
    #(re.compile('(//|w.)[cC][sS][eE]\.'), re.compile('[pP][eE][oO][pP][lL][eE]')),
    #(re.compile('/[cC][sS][eE]/'), re.compile('[pP][eE][oO][pP][lL][eE]')),
    #computer science
    #(re.compile('/[cC][oO][mM][pP][uU][tT][eE][rR][_][sS][cC][iI][eE][nN][cC][eE]/'),re.compile('[cC][hH][aA][iI][rR][sS]')),
    #(re.compile('/[cC][oO][mM][pP][uU][tT][eE][rR][_][sS][cC][iI][eE][nN][cC][eE]/'),re.compile('[cC][hH][aA][iI][rR]')),	
    #(re.compile('/[cC][oO][mM][pP][uU][tT][eE][rR][-][sS][cC][iI][eE][nN][cC][eE]/'),re.compile('[cC][hH][aA][iI][rR][sS]')),
    #(re.compile('/[cC][oO][mM][pP][uU][tT][eE][rR][-][sS][cC][iI][eE][nN][cC][eE]/'),re.compile('[cC][hH][aA][iI][rR]')),
    #(re.compile('/[cC][oO][mM][pP][uU][tT][eE][rR][_][sS][cC][iI][eE][nN][cC][eE]/'),re.compile('[pP][eE][oO][pP][lL][eE]')),	
    #(re.compile('/[cC][oO][mM][pP][uU][tT][eE][rR][-][sS][cC][iI][eE][nN][cC][eE]/'),re.compile('[pP][eE][oO][pP][lL][eE]')),
    #eecs
    #(re.compile('(//|w.)[eE][eE][cC][sS]\.'), re.compile('[cC][hH][aA][iI][rR][sS]')),
    #(re.compile('/[eE][eE][cC][sS]/'), re.compile('[cC][hH][aA][iI][rR][sS]')),
    #(re.compile('(//|w.)[eE][eE][cC][sS]\.'), re.compile('[cC][hH][aA][iI][rR]')),
    #(re.compile('/[eE][eE][cC][sS]/'), re.compile('[cC][hH][aA][iI][rR]')),
    (re.compile('(//|w.)[eE][eE][cC][sS]\.'), re.compile('[fF][aA][cC][uU][lL][tT][yY]')),
    (re.compile('/[eE][eE][cC][sS]/'), re.compile('[fF][aA][cC][uU][lL][tT][yY]')),
    (re.compile('(//|w.)[eE][eE][cC][sS]\.'), re.compile('[eE][dD][uU]')),
    (re.compile('/[eE][eE][cC][sS]/'), re.compile('[eE][Dd][uU]')),
    (re.compile('/[cC][oO][mM][pP][uU][tT][eE][rR][_][sS][cC][iI][eE][nN][cC][eE]/'), re.compile('[fF][aA][cC][uU][lL][tT][yY]')),
    (re.compile('/[cC][oO][mM][pP][uU][tT][eE][rR][-][sS][cC][iI][eE][nN][cC][eE]/'), re.compile('[fF][aA][cC][uU][lL][tT][yY]')),
    (re.compile('/[cC][oO][mM][pP][uU][tT][eE][rR][_][sS][cC][iI][eE][nN][cC][eE]/'), re.compile('[eE][dD][uU]')),
    (re.compile('/[cC][oO][mM][pP][uU][tT][eE][rR][-][sS][cC][iI][eE][nN][cC][eE]/'), re.compile('[eE][dD][uU]')),
    (re.compile('[cC][oO][mM][pP][uU][tT][eE][rR]'), re.compile('[sS][cC][iI][eE][nN][cC][eE]')),
    #(re.compile('(//|w.)[eE][eE][cC][sS]\.'), re.compile('[pP][eE][oO][pP][lL][eE]')),
    #(re.compile('/[eE][eE][cC][sS]/'), re.compile('[pP][eE][oO][pP][lL][eE]')),
    (re.compile('(//|w.)[cC][iI][sS]\.'), re.compile('[eE][dD][uU]')),
    (re.compile('/[cC][iI][sS]/'), re.compile('[eE][dD][uU]')),
    (re.compile('/[cC][mM][pP]/'), re.compile('[eE][dD][uU]')),
	#(re.compile('[lL][cC][sS][.][sS][yY][rR]'), re.compile('[eE][dD][uU]')),
    (re.compile('[cC][oO][mM][pP][uU][tT][eE][rR][-][iI][nN][fF][oO]'), re.compile('[tT][eE][cC][hH][nN][oO][lL][oO][gG][yY]')),
    (re.compile('[cC][oO][mM][pP][uU][tT][aA][tT][iI][oO][nN][aA][lL]'), re.compile('[sS][cC][iI][eE][nN][cC][eE]')),
    (re.compile('[aA][cC][aA][dD][eE][mM][iI][cC][sS]'), re.compile('[1][9][8][0][1][.]')),
    (re.compile('(//|w.)[cC][mM][sS]\.'), re.compile('[eE][dD][uU]')),
    (re.compile('/[cC][mM][sS]/'), re.compile('[eE][Dd][uU]')),
    (re.compile('/[cC][oO][mM][pP][sS][cC][iI][eE][nN][cC][eE]/'), re.compile('[eE][Dd][uU]')),
	(re.compile('[cC][oO][mM][pP][uU][tT][eE][rR][-][iI][nN][fF][oO][rR][mM][aA][tT][iI][oO][nN]'), re.compile('[Ss][yY][sS][tT][eE][mM][sS]')),
	




    ]
IGNORE_POSTFIX = [
    "pdf",
    "mp3",
    "css",
    "docx",
    "jpg",
    "png",
    "gif",
    "doc",
    "wmv",
    "mp4",
    ]
IGNORE_KEYWORDS = [
    "news",
    "newsletter",
    "Library",
    "research",
    "oit",
    "admissions",
    "extensions",
    "extension",
    "alumni",
    "news",
    "newsletter",
    "research",
    "oit",
    "admissions",
    "extensions",
    "extension",
    "admission",
    "library",
    "medicine",
    "policies",
    "support",
    "provost",
    "maps",
    "life",
    "about",
    "calendar",
    "parking",
    "copyright",
    "privacy",
    "disclaimer",
    "nursing",
    "law",
    "events",
    "magazine",	
    "tuition",
    "sports",
    "athletics",
    "jobs",
    "disability",
    "housing",
    "careers",
    "financial",
    "purchasing",
    "mp4",
    "job",
    "pharmacy",
    "teaching",
    "course-overviews",
    "courses",
    "course"
        

    ]
IGNORE_SPECIAL = ["?", "#"]
def ignore_postfix_matched(absURL):
    for ignore in IGNORE_POSTFIX:
        if  absURL.endswith(ignore):
            return True

    return False
def ignore_special_matched(absURL):
    for ignore in IGNORE_SPECIAL:
        if absURL.find(ignore) > 0:
            return True

    return False
def ignore_keywords_matched(absURL):
    for ignore in IGNORE_KEYWORDS:
        if absURL.find(ignore) > 0:
            return True

    return False
def getURLs(currentURL, content, foundLinks):
    currentNetLoc = urlparse.urlparse(currentURL).netloc    

    allURLs = re.findall(HREF_RE, content)

    newURLs = []
    for newURL in allURLs:

        try:
            absURL = urlparse.urljoin(currentURL, newURL)
        except:
            continue

        if absURL in foundLinks:
            print "drop %s already in db" % absURL
            continue

        if ignore_postfix_matched(absURL):
            print "drop %s not an HTML file" % absURL
            continue
        
        if ignore_keywords_matched(absURL):
            print "drop %s keywords ignored" % absURL
            continue

        if ignore_special_matched(absURL):
            print "drop %s  machine generated" % absURL
            continue
                
        newNetLoc = urlparse.urlparse(absURL).netloc    
        if currentNetLoc[-7:] == newNetLoc[-7:]:
            newURLs.append(absURL)
        else:
            print "drop %s cause it's out of site" % absURL
            continue

    return newURLs
def getWebPage(url):
    content = ""
    try:
        me = urllib2.urlopen(url, timeout=30)
        content =  me.read()
    except:
        print "error getting URL %s" % url
        return ""

    return content


#{{{ isSubDomain
def isSubDomain(url):
    dummy = url.split(".")
    if len(dummy) == 2:
        return False

    if len(dummy) == 3 and string.lower(dummy[0]) == "www":
        return False

    return True
#}}}


#{{{ simplifyURL
def simplifyURL(url, reSet):
    urlInfo = urlparse.urlparse(url)
    if isSubDomain(urlInfo.netloc):
        localPart = ".".join(urlInfo.netloc.split(".")[:-2])
        for oneRE in reSet:
            if re.search(oneRE, localPart):
                return "%s://%s" % (urlInfo.scheme, urlInfo.netloc)

    print "url", url
    lastPos = 0
    for oneRE in reSet:
        matched = re.search(oneRE, url)
        if matched.end() > lastPos:
            lastPos = matched.end()
        print oneRE.pattern, lastPos
        
    cuttingSlash = url.find("/", lastPos-1)
    print cuttingSlash
    if cuttingSlash == -1:
        return url
    else:
        return url[:cuttingSlash+1]
#}}}

def scanOnePage(origURL, level, link, links, foundLinks, outFile):
    print "scanning %s at level %s" % (link, level)
    content = getWebPage(link)
    newURLs = getURLs(link, content, foundLinks)
    foundOne = False
    for newURL in newURLs:
        for oneReSet in DEST_RES:
            allMatched = True
            for oneRE in oneReSet:
                if not re.search(oneRE, newURL):
                    allMatched = False
                    break

            if allMatched:
                resultURL = simplifyURL(newURL, oneReSet)
                if not resultURL.endswith('/'):
                    resultURL += '/'
                outFile.write('%s\n' % (resultURL))
                outFile.flush()
                foundOne = True
                return foundOne
        if level < MAX_LEVEL:
            foundLinks.append(newURL)
            links.append((level+1, newURL))

    return foundOne

def scanOneSite(origURL, outFile):
    links = [(0, origURL),]
    foundLinks = [origURL,]

    foundOne = False
    while len(links) > 0:
        level, link = links[0]
        links.remove((level, link))
        if scanOnePage(origURL, level, link, links, foundLinks, outFile):
            foundOne = True
            return
    if not foundOne:
        notfoundFile.write('"%s","%s"\n' % (url, "not found"))
        notfoundFile.flush()
if __name__ == "__main__":
    usage = """usage: %prog [options]"""
    parser = OptionParser(usage = usage)
    parser.add_option("-i", "--input",
                      dest   = "inputFile",
                      help   = "the input file with URLs to scan",
                      )
    parser.add_option("-o", "--output",
                      dest   = "outputFile",
                      help   = "The output csv file",
                      )
    parser.add_option("-x", "--notfoundoutput",
                      dest   = "notfoundFile",
                      help   = "The not found output csv file",
                     )
    options, args = parser.parse_args()

    inFile   = open(options.inputFile, "r")
    outFile = open(options.outputFile, "w")
    notfoundFile = open(options.notfoundFile, "w")

    for line in inFile.readlines():
        url = line.strip()
        scanOneSite(url, outFile)
        
    inFile.close()
    outFile.close()
    notfoundFile.close()

