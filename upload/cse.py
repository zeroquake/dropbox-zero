#!/usr/bin/env python
# -*- coding: utf-8 -*-

#{{{ imports
import os, os.path, sys, re, commands, pickle, tempfile, getopt
import socket, string, random, threading, time, traceback
from optparse import OptionParser
import StringIO, urllib2, logging, datetime, unicodedata, urlparse
#}}}

MAX_LEVEL=3
HREF_RE = re.compile('href\s*=\s*[\'"](.*?)[\'"]')

DEST_RES = [
    re.compile('[cC][sS]'),
    re.compile('[cC][sS][eE]'),
    re.compile('[cC][oO][mM][pP][uU][tT][eE][rR]]'),
    ]

#{{{ getURLs
def getURLs(currentURL, content, foundLinks):
    currentNetLoc = urlparse.urlparse(currentURL).netloc    

    allURLs = re.findall(HREF_RE, content)
    newURLs = []
    for newURL in allURLs:
        absURL = urlparse.urljoin(currentURL, newURL)

        if absURL in foundLinks:
            print "drop %s cause it's already in db" % absURL
            continue

        newNetLoc = urlparse.urlparse(absURL).netloc    
        if currentNetLoc <> newNetLoc:
            print "drop %s cause it's out of site" % absURL
            continue

        if absURL.endswith("pdf") or absURL.endswith("mp3") or absURL.endswith("css"):
            print "drop %s cause it's not an HTML file" % absURL
            continue

        newURLs.append(absURL)

    return newURLs
#}}}


# #{{{ getWebPage
# def getWebPage(url):
#     orig = StringIO.StringIO()
#     req = pycurl.Curl()
#     req.setopt(req.URL, str(url))
#     req.setopt(req.WRITEFUNCTION, orig.write)
#     req.setopt(req.FOLLOWLOCATION, 1)
#     req.setopt(req.ENCODING, "gzip")

#     try:
#         req.perform()
#     except:
#         print "error getting URL %s" % url
#         pass
        
#     req.close()
#     content = orig.getvalue()
#     orig.close()
#     return content
# #}}}

#{{{ getWebPage
def getWebPage(url):
    try:
        me = urllib2.urlopen(url)
        content =  me.read()
    except:
        print "error getting URL %s" % url
        return ""

    return content
#}}}

#{{{ scanOnePage
def scanOnePage(level, link, links, foundLinks):
    print "scanning", link
    content = getWebPage(link)
    newURLs = getURLs(link, content, foundLinks)

    for newURL in newURLs:
        for oneRE in DEST_RES:
            if re.search(oneRE, newURL):
                return newURL

        foundLinks.append(newURL)
        links.append((level+1, newURL))
#}}}

#{{{ scanOneSite
def scanOneSite(url):
    links = [(0, url),]
    foundLinks = [url,]

    while len(links) > 0:
        level, link = links.pop()
        result = scanOnePage(level, link, links, foundLinks)
        if result:
            return result

    return "not found"
#}}}

#{{{ main
# when run as a script
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
    options, args = parser.parse_args()

    inFile   = open(options.inputFile, "r")
    outFile = open(options.outputFile, "w")

    for line in inFile.readlines():
        url = line.strip()
        result = scanOneSite(url)
        outFile.write('"%s","%s"\n' % (url, result))
        outFile.flush()
        
    inFile.close()
    outFile.close()
#}}}    
