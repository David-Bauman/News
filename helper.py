from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import *


def tag_visible(element):
    return not (element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]'] or isinstance(element, Comment))


def text_from_html(body):
    soup = BeautifulSoup(body, 'lxml')
    texts = soup.find_all(text=True)
    visible_texts = filter(tag_visible, texts)
    return " ".join(t.strip() for t in visible_texts)


def keywords(url):
    lst = clean(text_from_html(urlopen(url).read()))
    counts = assemble_counts(lst)

    best = []
    for i in range(3):
        temp = max(counts, key=lambda key: counts[key])
        best.append(temp)
        counts[temp] = -1

    return best, len(lst)


def assemble_counts(lst):
    counts = {}
    for word in lst:
        if len(word) < 5 or word.title() == "Continue":
            continue
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts


def clean(line):
    cleanline = ""
    acc = 0
    for i in range(len(line)):
        ch = line[i]
        if ch == "W":
            if line[i:i+47] == "We’re interested in your feedback on this page.":
                break
        elif ch =="F" and acc == 1:
            if line[i:i+35] == "Facebook  Twitter  Flipboard  Email":
                break
        elif ch == "l" and acc == 0:
            if line[i-34:i+1] == "Facebook  Twitter  Flipboard  Email":
                cleanline = ""
                acc += 1
                continue
        if ch.isalpha():
            cleanline += ch.lower()
        else:
            cleanline += " "
    return cleanline.split()

