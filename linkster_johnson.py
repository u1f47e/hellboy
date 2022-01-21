#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PURPOSE:  Scrape issue links from darkhorse dot com
#           Run first.
# USAGE:    python3 linkster_johnson.py filename.csv
# baseurl = "https://www.darkhorse.com/Hellboy/Comics/?page="

import csv
import sys
import urllib.request as ul
from bs4 import BeautifulSoup


def link_collector(url):
    """Get issue hrefs and store them in a csv."""
    req = ul.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    client = ul.urlopen(req)
    htmldata = client.read()
    client.close()
    pagesoup = BeautifulSoup(htmldata, 'html.parser')
    page_links = []
    for d in pagesoup.select('div.list_items_container div'):
        try:
            issue_links = []
            href = d.select('a')[1]
            issue_links.append(f"https://www.darkhorse.com{href['href']}")
            page_links.append(issue_links)
        except IndexError:
            pass

    return page_links


def main():
    with open(sys.argv[1], 'w') as f:
        hellwriter = csv.writer(f)
        header = ['product_link']
        hellwriter.writerow(header)

        for i in range(10, 0, -1):
            link = f"https://www.darkhorse.com/Hellboy/Comics/?page={i}"
            print(f"Collecting links for page {i}...")
            rows = link_collector(link)
            hellwriter.writerows(rows)
        f.close()


if __name__ == "__main__":
    main()
