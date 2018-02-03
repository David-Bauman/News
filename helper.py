"""
First two functions (tag_visible and text_from_html) are from user jbochi on
stackoverflow: https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text/1983219
David Bauman, 2017 - 12 - 17
"""
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import *
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.find_all(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def keywords(url):
    html = urlopen(url).read()
    text = text_from_html(html)
    lst = scrubit(text)
    counts = assemblecounts(lst)

    best = ["",0]
    for sublist in counts:
        if sublist[1] > best[1]:
            best = sublist

    best2 = ["",0]
    for sublist in counts:
        if sublist == best:
            pass
        elif sublist[1] > best2[1]:
            best2 = sublist

    best3 = ["",0]
    for sublist in counts:
        if sublist == best or sublist == best2:
            pass
        elif sublist[1] > best3[1]:
            best3 = sublist

    return best,best2,best3,int(len(lst))

def assemblecounts(lst):
    counts = []
    for word in lst:
        if len(word) < 5:
            pass
        elif word == "continue" or word == "Continue":
            pass
        else:
            low = 0
            high = len(counts) - 1
            Valid = False
            while low <= high:
                middle = int((low + high)/2)
                if word == counts[middle][0]:
                    Valid = True
                    break
                elif word > counts[middle][0]:
                    low = middle + 1
                else:
                    high = middle -1
            if Valid:
                counts[middle][1] += 1
            else:
                counts.insert(low,[word,1])
    return counts

def scrubit(line):
    Valid = True
    cleanline = ""
    acc = 0
    for i in range(len(line)):
        ch = line[i]
        if ch == "W":
            if line[i+1:i+47] == "e’re interested in your feedback on this page.":
                Valid = False
        if ch =="F" and acc == 1:
            if line[i:i+35] == "Facebook  Twitter  Flipboard  Email":
                Valid = False
        if ch == "l" and acc == 0:
            if line[i-34:i+1] == "Facebook  Twitter  Flipboard  Email":
                cleanline = ""
                acc += 1
        if Valid:
            if ch.isalpha():
                ch = ch.lower()
                cleanline += ch
            else:
                cleanline += " "
        else:
            break
    cleanlist = cleanline.split()
    return cleanlist
