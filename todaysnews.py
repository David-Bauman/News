"""
Gets top headlines + summaries from NPR and some select sections of NYT.
Gives option for keywords/length of article, then offers to bring up the
article in your web browser
David Bauman, 2017 - 12 - 17

note that the first time the program is run it will print out instructions
for BeautifulSoup. Follow it by changing the code in NYT() and NPR(). i.e.
BeautifulSoup(page.read(),"lxml"). The proper parser depends on your system
"""
from helper import *
from bs4 import BeautifulSoup
from urllib.request import *
import os
import time
import webbrowser
def main():
    #which NYT sections you'd like
    nytallowed = ["world", "us", 'politics', 'technology', 'science', 'health', 'sports', 'arts']
    print("New York Times section choices: world, us, politics, technology, science, health, sports, arts.")
    print("At the following prompts, please enter sections one at a time. When finished, enter nothing")
    nytlst = []
    while True:
        choice = input("NYT section: ")
        if choice == "":
            break
        elif choice not in nytallowed:
            print("Please enter a proper section.")
        elif choice in nytlst:
            print("This has already been added.")
        else:
            nytlst.append(choice)

    #clear the terminal window and get lists
    os.system('cls' if os.name == 'nt' else 'clear')
    nytstrings,nyturls = NYT(nytlst)
    nprstrings,nprurls = NPR()

    #print NYT stuff
    for i in range(len(nytstrings)):
        if nytlst[i] == "us":
            section = "US"
        else:
            section = nytlst[i].title()
        print("The top three posts from The New York Times - %s section" % (section))
        for item in nytstrings[i]:
            print(item)
        print("\n")

    #print NPR stuff
    print("The top three posts from National Public Radio")
    for item in nprstrings:
        print(item)
    print("\n")

    #allows choice of articles to get more info (keywords, article length, and offers to bring up article in web browser)
    time.sleep(1)
    print("Which article would you like to know more about?\nPlease enter in the following format: source,number\ni.e. : world,1 or npr,3\n")
    while True:
        sourceurl = ""
        nextstep = input("Source,number: ")
        if nextstep == "":
            break
        tokens = nextstep.split(",")
        source = tokens[0]
        article = int(tokens[1])

        if source == "npr":
            sourceurl = nprurls[article-1]
            source = source.upper()
        elif source not in nytlst:
            print("woops, check the source")
            pass
        else:
            for t in range(len(nytlst)):
                if nytlst[t] == source:
                    break
            sourceurl = nyturls[t][article-1]
            if source == "us":
                source ="NYT - " + source.upper()
            else:
                source = "NYT - " + source.title()
        if sourceurl != "":
            one,two,three,length = keywords(sourceurl)
            print("The keywords from %s are: %s, %s, %s" % (source, one[0],two[0],three[0]))
            print("The article is approximately %d words long." % (length))
            opensesame = input("Would you like to be brought to the webpage? Y/N ")
            if opensesame == "Y" or opensesame == "y":
                webbrowser.open_new(sourceurl)
        print("\n")

def NYT(lst):
    allthestrings = []
    alltheurls = []
    for item in lst:
        stringlst = []
        urllst = []
        url = "https://www.nytimes.com/section/" + item
        page = urlopen(url)
        soup = BeautifulSoup(page.read())
        info = soup.find_all("div", {"class": "story-body"})
        for i in range(3):
            s = "%d. %s\n      %s\n\n" % (i+1,info[i].a.contents[0],info[i].p.contents[0])
            stringlst.append(s)
            newinfo = info[i].find_all("a")
            newurl = ""
            string = str(newinfo[0])
            Valid = True
            for l in range(len(string)):
                if Valid:
                    try:
                        if string[l] + string[l+1] + string[l+2] + string[l+3] + string[l+4] + string[l+5] == 'href="':
                            x = l + 5
                            while True:
                                x += 1
                                newch = string[x]
                                if newch == '"':
                                    Valid = False
                                    break
                                newurl += newch
                    except IndexError:
                        pass
            urllst.append(newurl)
        allthestrings.append(stringlst)
        alltheurls.append(urllst)
    return allthestrings,alltheurls

def NPR():
    lst = []
    urllst = []
    url = "https://www.npr.org/sections/news/"
    page = urlopen(url)
    soup = BeautifulSoup(page.read())
    info = soup.find_all("div", {"class": "item-info"})
    acc = 0
    for i in [0,3,4]:
        acc += 1
        newinfo = info[i].find_all("a")
        try:
            s = "%d. %s\n      %s\n\n" % (acc,newinfo[1].contents[0],newinfo[2].contents[1])
        except IndexError:
            s = "%d. %s\n      %s\n\n" % (acc,newinfo[1].contents[0],newinfo[3].contents[1])
        lst.append(s)
        newurl = ""
        string = str(newinfo[1])
        for l in range(len(string)):
            try:
                if string[l] + string[l+1] + string[l+2] + string[l+3] + string[l+4] + string[l+5] == 'href="':
                    x = l + 5
                    while True:
                        x += 1
                        newch = string[x]
                        if newch == '"':
                            break
                        newurl += newch
            except IndexError:
                pass
        urllst.append(newurl)
    return lst,urllst
main()
