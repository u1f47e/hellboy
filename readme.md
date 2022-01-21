# Hellboy Single Issue Comic Book Inventory Maker
This collection of scripts will scrape issue links from darkhorse dot com and pull issue-level metadata into three separate inventory lists. A complete list of all Hellboy related titles is also created.

## Collect links

![the lobster](https://static.wikia.nocookie.net/hellboy/images/5/5e/Lobster.jpg/revision/latest/scale-to-width-down/600?cb=20091215025205)

Run `python3 linkster_johnson.py <filename.csv>` 

This is currently configured to only pull Hellboy links, but could be adjusted to work on any darkhorse title.

## Scrape metadata

![abe sapien](https://static.wikia.nocookie.net/hellboy/images/0/08/HonE_Abecover.jpg/revision/latest/scale-to-width-down/500?cb=20121017150954)

Run `python3 abe_scrapien.py <input-links.csv> <output-file.csv>`

Should probably work on any darkhorse comic page without adjustment.

## Sort issue metadata and create separate files

![satan](https://static.wikia.nocookie.net/hellboy/images/d/df/Hellboy_-_Satan.JPG/revision/latest/scale-to-width-down/658?cb=20130206091316)

Run `python3 satan_sort.py <output-file.csv>`

Currently configured to only sort Hellboy and B.P.R.D. issue metadata.