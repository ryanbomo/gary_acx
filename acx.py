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
##This program assumes no copyright of any referenced work, and any usage of 
##copyrighted work is being done under Fair Use for educational purposes or with 
##respect to the license of the work.  Where outside work may have been used
##either explicitly or for inspiration, it has been listed in the "Other files
##referenced/used in this one:" section of the header.
import math

def main(filterList, numRatings, amzRank):
    ## create URL
    ## get results
    url = createURL(filterList)
    numPages = getNumPages(url)
    ##visitACXURL(url,numPages)
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

##def visitACXURL(url,pageNum):
    
    ## for each page
        ## for each book
            ## check ratings number and amzscore
                # if good, record to outward file
    

def ui():
    ## user interface level
    ## currently just calls main with test values
    filterList = parseUserPreferences(grabUserPreferences("user_pref.csv"), 9)
    numRatings = 50
    amzRank = 20000
    main(filterList,numRatings,amzRank)


    
