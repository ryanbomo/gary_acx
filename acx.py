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
import math,re,bs4
from urllib.request import urlopen

def main(filterList, numRatings, amzRank):
    ## create URL
    url = createURL(filterList)
    ## get list of results
    results = buildResultsList(url)
    ## check for valid results to user modified query
    validResultsList = checkResults(results, numRatings, amzRank)
    ## write narrowed results to ledger
    writeLedger(validResultsList)

def createURL(filterList):
    ## create URL based on user filters
    url = "http://www.acx.com/tsAjax/ref=acx_ts_sb_an?field_genreExclusions=NONE"
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
            
    url += "&keywords=&pageIndex="
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

def buildResultsList(url):
    firstPage = url +"1"
    #go to website
    resultsList = []
    page = urlopen(firstPage)
    soup = bs4.BeautifulSoup(page)

    # get page numbers
    numResults = int(soup.find('input', {'id': 'jsValueSearchCount'}).get('value'))
    pageNum = math.ceil(numResults/30)
    print(pageNum)
    
    # create array list of results pages
    listResults = []
    for i in range(pageNum):
        ender = i+1
        thisURL = url + str(ender)
        listResults.append(thisURL)

    # visit each results page and grab match links
    for i in range(len(listResults)):
        thisPage = urlopen(listResults[i])
        soup = bs4.BeautifulSoup(thisPage)
        result_1 = soup.find_all("div",class_="resultInfo")
        for j in range(len(result_1)):
            address = result_1[j].find_all("a",href = True)
            resultsList.append(address[0]['href'])
    return resultsList

def checkResults(listResults, numRatings, amzRank):
    coreURL = "www.acx.com"
    # check each result
    for i in range(len(listResults)):
        #build result URL
        print(listResults[i])
        thisURL = coreURL + listResults[i]
        print(thisURL)
        print("\n")
        #open each result page
        page = urlopen(thisURL)
        soup = bs4.BeautifulSoup(page)
        #get amz rank and number of ratings
        result_1 = soup.find_all("div", class_="titleDetailField")
        result_2 = result_1.find_all("div", class_="titleDetailFieldValue")
        #check ratings and append if pass
    print(numRatings)
    print(amzRank)
    print("got here")

def writeLedger(validResultsList):
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


    
