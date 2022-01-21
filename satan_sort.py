#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PURPOSE:  Sorts complete Hellboy/B.P.R.D inventory into three categories
#           Run after abe_scrapien.py
# USAGE:    python3 satan_sort.py output-file.csv

import csv
import sys


def inventory_maker(input_file, field_names, rows):
    """Make new csv from list input."""
    with open(input_file, 'w') as f:
        print(f"Creating {input_file}...")
        hellwriter = csv.DictWriter(f, fieldnames=field_names)
        hellwriter.writeheader()
        hellwriter.writerows(rows)
        f.close()


def main(input_file):
    """Read and sort primary inventory created by scraping."""
    with open(input_file, 'r') as f:
        print(f"Reading {input_file}...")
        hellreader = csv.DictReader(f)
        fieldnames = hellreader.fieldnames
        print(fieldnames)
        hellboy = []
        bprd = []
        others = []

        b0 = 'B.P.R.D.'
        b1 = 'B.P.R.D'
        b2 = 'BPRD'
        h = 'Hellboy'

        for row in hellreader:
            if (b0 in row['title'] or b1 in row['title'] or b2 in row['title']):
                bprd.append(row)
            if (h in row['title'] and b0 not in row['title'] and
                b1 not in row['title'] and b2 not in row['title']):
                hellboy.append(row)
            if (h not in row['title'] and b0 not in row['title'] and
                b1 not in row['title'] and b2 not in row['title']):
                others.append(row)

        f.close()

    hellboy.sort(key=lambda hellboy: hellboy['publication-date'])
    bprd.sort(key=lambda bprd: bprd['publication-date'])
    others.sort(key=lambda others: others['publication-date'])

    inventory_maker("hellboy-inventory.csv", fieldnames, hellboy)
    inventory_maker("bprd-inventory.csv", fieldnames, bprd)
    inventory_maker("world-of-hellboy-inventory.csv", fieldnames, others)


if __name__ == '__main__':
    main(sys.argv[1])
