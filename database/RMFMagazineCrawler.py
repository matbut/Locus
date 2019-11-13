import csv
import os
import re
import sys
from urllib.parse import urlparse

import dates
import requests
from bs4 import BeautifulSoup


def crawl(url, file_name):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    magazine = soup.find("div", {"class": "responsive-magazyn"})

    title = magazine.find("h1")
    date_time = magazine.find("div", {"class": "article-date"})
    lead = magazine.find("div", {"class": "article-lead"})
    content = magazine.find("div", {"class": "article-content"})

    for div in content.find_all(class_='instagram-media'):
        div.decompose()
    for script in content.find_all('script'):
        script.decompose()

    article_date_time = dates.to_datetime(date_time.contents[0])
    article_title = title.contents[0]

    content_text = re.sub('\\s+', ' ', content.get_text())

    article_content = lead.contents[0] + content_text

    article = [urlparse(url).netloc, article_date_time, url, '\"'+article_title+'\"', '\"'+article_content+'\"']
    save_to_file(article, file_name)


def save_to_file(article, file_name):
    header = ['page', 'date', 'link', 'title', 'content']
    if os.path.exists(file_name):
        open_mode = 'a'
    else:
        open_mode = 'w'

    with open(file_name, open_mode) as csv_file:
        writer = csv.writer(csv_file)
        if open_mode == 'w':
            writer.writerow(header)
        writer.writerow(article)
    csv_file.close()


if len(sys.argv) == 3:
    crawl(sys.argv[1], sys.argv[2])
