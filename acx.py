##Author: Ryan Bomalaski
##Author ID:
##File: acx.py
##
##Purpose: 
## Create a crawler script that can take search parameters for acx.com
## and return a list tailored to the user.  ACX does not currently allow you to
## set a rating or sales rank threshold.  The goal here is to crawl through ACX
## and only return works that hit a certain threshold.
##
##Future Features:
## 1. Author List - A list of authors that the user can input to look for recent
##  additions.  Newer books might not necessarily be ranked or sell well, but 
##  finding them early can give the narrator a leg up.
## 2. Good Reads - Gary would like me to incorporate Good Reads at some point.
##  Not sure in what way to do it, but this is a later thing to be worked out
##  down the road.
##
##Other work referenced/used:
##  1. N/A
##
##This program assumes no copyright of any referenced work, and any usage of 
##copyrighted work is being done under Fair Use for educational purposes or with 
##respect to the license of the work.  Where outside work may have been used
##either explicitly or for inspiration, it has been listed in the "Other work
##referenced/used:" section of the header.
import math
import bs4,requests

def main(filterList, numRatings, amzRank):
    ## create URL
    url = createURL(filterList)
    numPages = getNumPages(url)
    ##visitACXURL(url,numPages, numRatings, amzRank)
    print(url)
    ## compare results with previous results on ledger
    ## check new results' sales ranking and number of ratings
    ## add new stuff to ledger

def createURL(filterList):
    ## create URL based on user filters
    url = "http://www.acx.com/ts#field_genreExclusions=NONE"
    templateList = ["&field_gender=ACXGD", "&field_comp=ACXCR",
                    "&field_genre=ACXFG", "&field_fiction=ACXFN",
                    "&field_language=ACXLG", "&field_accent=ACXAC",
                    "&field_narrativeAge=ACXVA", "&field_vocalStyle=ACXVS",
                    "&field_length=ACXPL"]
    for i in range(len(filterList)):
        temp = ""
        if filterList[i] != "$$":
            temp += templateList[i]+str(filterList[i])
            url += temp
            
    url += "&keywords=&pageIndex=1"
    return url

def grabUserPreferences(fileName):
    userpref = open(fileName, 'r')
    read_data = userpref.read()
    userpref.close()
    return read_data

def parseUserPreferences(userPrefString, numPrefs):
    prefs = userPrefString.split(",")
    for i in range(len(prefs)):
        if "\n" in prefs[i]:
            prefs[i] = prefs[i].replace("\n", "")
    return prefs

def getNumPages(url):
    ## go to URL and get num results
    numResults= 10
    ## test vale for numResults right now
    numPages = math.ceil(numResults/30)
    return numPages

##def visitACXURL(url,pageNum, numRatings, amzRank):
    
    ## for each page
        ## for each book
            ## check ratings number and amzscore
                # if good, writeLedger(infoString)

def writeLedger(infoString):
    ledger = open("ledger.csv",'w+')
    ##write info
    ledger.close()
    
## Gets search pref from user_pref.csv
## gets min number of ratings and min amz rank from input, makes them an int

def ui():
    filterList = parseUserPreferences(grabUserPreferences("user_pref.csv"), 9)
    print(''' We will now ask you for your non-acx preferences.  These include minimum
number of ratings and minimum allowable amazon sales rank.  This program does
not store these values in this iteration.  You should remember them for each
time you perform this search.''')
    try:
        numRatings = int(input("What is the min number of ratings?\n"))
    except ValueError:
        print("Not a number, using default number of ratings (50)")
        numRatings = 50
    try:
        amzRank = int(input("What's the maximum amz rank?\n"))
    except ValueError:
        print("Not a number, using default min rank of 200000")
        amzRank = 200000
    main(filterList,numRatings,amzRank)


    
