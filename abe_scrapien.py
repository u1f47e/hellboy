#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PURPOSE:  Scrape issue level metadata from darkhorse dot com
#           Run after linkster_johnson.py
# USAGE:    python3 abe_scrapien.py input-links.csv output-file.csv

import csv
import re
import time
import urllib.request as ul
import sys
from pprint import pprint
from datetime import datetime as dt

from bs4 import BeautifulSoup


def read_html(url):
    """Post a url and retrieve html."""
    print(f"Requesting: {url}")
    req = ul.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    client = ul.urlopen(req)
    html_data = client.read()
    client.close()

    return html_data


def issue_metadata(data):
    """Read parsed page-level html and extract comic metadata."""
    print("Making soup...")
    soup = BeautifulSoup(data, 'html.parser')
    details = soup.findAll('div', {'id': 'product-details'})
    meta = soup.select('div.product-meta dl')
    row = [""]

    for d in details:
        try:
            titles = d.findAll('h2', {'class': 'title'})
            title = titles[0].text
        except (AttributeError, ValueError):
            title = 'ERROR'

        row.append(title)

    for m in meta:
        try:
            date_search = re.search(r'\w*\s\d{1,2},\s\d{4}', m.text)
            result = date_search.group()
            date = dt.strptime(re.sub(r'(,)', '', result),
                               '%B %d %Y').strftime('%Y-%m-%d')
        except (AttributeError, ValueError):
            date = 'ERROR'

        row.append(date)

    try:
        writers = soup.find('dt', text="Writer:").findNext('dd').string
    except AttributeError:
        try:
            writers = soup.find('dt', text="Creators:").findNext('dd').string
        except AttributeError:
            writers = 'Not Found'

    try:
        artists = soup.find('dt', text="Artist:").findNext('dd').string
    except AttributeError:
        artists = 'Not Found'

    try:
        colorist = soup.find('dt', text="Colorist:").findNext('dd').string
    except AttributeError:
        colorist = 'Not Found'

    try:
        cover = soup.find('dt', text="Cover Artist:").findNext('dd').string
    except AttributeError:
        cover = 'Not Found'

    try:
        upc = soup.find('dt', text="UPC:").findNext('dd').string
    except AttributeError:
        upc = 'Not Found'

    row.append(writers)
    row.append(artists)
    row.append(colorist)
    row.append(cover)
    row.append(upc)

    return row


def main():
    infile = sys.argv[1]
    outfile = sys.argv[2]

    with open(outfile, 'w') as f:
        print(f"Creating {outfile}")
        hellwriter = csv.writer(f)
        header = ['owned', 'title', 'publication-date', 'writers', 'artists',
                  'colorist', 'cover-artist', 'upc', 'url']
        hellwriter.writerow(header)

        with open(infile, 'r') as h:
            print(f"Opening {infile} to read urls...")
            hellreader = csv.DictReader(h)

            for line in hellreader:
                link = line['product_link']
                pagedata = read_html(link)
                issue = issue_metadata(pagedata)
                issue.append(link)
                print("Writing row data:")
                pprint(issue)
                hellwriter.writerow(issue)

                for remaining in range(5, 0, -1):
                    sys.stdout.write('\r')
                    sys.stdout.write(f"Waiting {remaining} seconds...")
                    sys.stdout.flush()
                    time.sleep(1)

                sys.stdout.write('\n')
            h.close()
        f.close()
    print('\rDone!')


if __name__ == "__main__":
    main()
