 # Today's News  

[![GitHub Issues](https://img.shields.io/github/issues/David-Bauman/News.svg)](https://github.com/David-Bauman/News/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-green.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## What is this?

This program is a Python based web scraper that provides summaries of the top 3 articles from National Public Radio and from selected sections of the New York Times. It then further provides the ability to get more in-depth information on a specific story, culminating in an option to have that article loaded into a browser.  

## How do I use it?

It's easy! Just clone the repo, run `$ python3 todays_news.py`, and follow the onscreen prompts.

## To Do
- Handle NYT changing site layout, breaks current scraping on some sections (US often) some of the time
- Format user input (to allow "NPR" to equal "npr")
- Catch improper inputs (if user accidentally enters "world 1" as next step, no comma, it should just reprompt or, linked w/ above todo, fix it so that we can accept "world 1")
- Debate cost/benefit of switching to NYT API, NPR API

