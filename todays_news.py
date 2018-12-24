"""
Gets top headlines + summaries from NPR and chosen sections of NYT.
Gives option for keywords/length of article, then offers to bring up the
article in your web browser
David Bauman, 2017 - 12 - 17
"""
from helper import keywords
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import time
import webbrowser


def main():
    #which NYT sections you'd like
    nyt_allowed = ["world", "us", "politics", "technology", "science", "health", "sports", "arts"]
    print("New York Times section choices: %s" % nyt_allowed)
    print("At the following prompts, please enter sections one at a time. When finished, enter nothing")
    nyt_choices = []
    while True:
        choice = input("NYT section: ")
        if choice == "":
            break
        elif choice not in nyt_allowed:
            print("Please enter a proper section.")
        elif choice in nyt_choices:
            print("This has already been added.")
        else:
            nyt_choices.append(choice)

    #clear the terminal window and get lists
    nyt_strings, nyt_urls = NYT(nyt_choices)
    npr_strings, npr_urls = NPR()
    os.system('cls' if os.name == 'nt' else 'clear')

    #print NYT stuff
    for i in range(len(nyt_strings)):
        if nyt_choices[i] == "us":
            section = "US"
        else:
            section = nyt_choices[i].title()
        print("The top three posts from The New York Times - %s section" % section)
        for item in nyt_strings[i]:
            print(item)
        print("\n")

    #print NPR stuff
    print("The top three posts from National Public Radio")
    for item in npr_strings:
        print(item)
    print("\n")

    #allows choice of articles to get more info (keywords, article length, and offers to bring up article in web browser)
    time.sleep(1)
    print("Which article would you like to know more about?")
    print("Please enter in the following format: source, number\ni.e. : world, 1 or npr, 3\n")
    while True:
        source_url = ""
        next_step = input("Source, number: ")
        if next_step == "":
            break
        tokens = next_step.split(",")
        source = tokens[0]
        article_num = int(tokens[1])

        if source == "npr":
            source_url = npr_urls[article_num-1]
            source = source.upper()
        elif source not in nyt_choices:
            print("Whoops, check the source")
            continue
        else:
            for i in range(len(nyt_choices)):
                if nyt_choices[i] == source:
                    source_url = nyt_urls[i][article_num-1]
            if source == "us":
                source ="NYT - US"
            else:
                source = "NYT - " + source.title()
        if source_url != "":
            best, length = keywords(source_url)
            print("The keywords from %s are: %s" % (source, str(best)[1:-1]))
            print("The article is approximately %d words long." % length)
            open_sesame = input("Would you like to be brought to the webpage? Y/N ")
            if open_sesame.lower() == "y":
                webbrowser.open_new(source_url)

def NYT(lst):
    return_strings = []
    return_urls = []
    for item in lst:
        print("Collecting data from NYT - %s section" % (item.upper() if item == "us" else item.title()))
        string_lst = []
        url_lst = []
        page = urlopen("https://www.nytimes.com/section/" + item)
        soup = BeautifulSoup(page.read(), "lxml")
        info = soup.find_all("div", {"class": "story-body"})
        for i in range(3):
            current = info[i]
            a_tag = current.find_all("a")[0]
            if "href" in a_tag.attrs:
                url = a_tag["href"]
            else:
                print("Houston, we have a problem")
                exit()
            string_lst.append("%d. %s\n      %s\n\n" % (i+1, current.a.contents[0], current.p.contents[0]))
            url_lst.append(url)
        return_strings.append(string_lst)
        return_urls.append(url_lst)
    return return_strings, return_urls

def NPR():
    lst = []
    url_lst = []
    print("Collecting data from NPR")
    page = urlopen("https://www.npr.org/sections/news/")
    soup = BeautifulSoup(page.read(), "lxml")
    info = soup.find_all("div", {"class": "item-info"})
    acc = 0
    for i in [0,3,4]:
        acc += 1
        a_tags = info[i].find_all("a")
        a_tag = a_tags[1]
        try:
            s = "%d. %s\n      %s\n\n" % (acc, a_tag.contents[0], a_tags[2].contents[1])
        except IndexError:
            s = "%d. %s\n      %s\n\n" % (acc, a_tag.contents[0], a_tags[3].contents[1])
        if "href" in a_tag.attrs:
            url = a_tag["href"]
        else:
            print("Houston, we have a problem. NPR")
            exit()
        lst.append(s)
        url_lst.append(url)
    return lst, url_lst
main()
