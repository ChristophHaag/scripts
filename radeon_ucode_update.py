#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
import urllib.request
import datetime
import locale
import os
import subprocess

scriptfile = "download_missing_radeon_ucode.sh"

locale.setlocale(locale.LC_ALL, 'C') # everyone has this, right?

baseurl = "https://secure.freedesktop.org/~agd5f/radeon_ucode/"


class LinkObject():
    def __init__(self, url, date):
        self.url = url
        self.date = date


def get_html(url):
    #with open("h", "r") as f:
    #    return f.read()
    with urllib.request.urlopen(url) as response:
        html = response.read()
        return html


def get_links(soup, currenturl):
    retlinks = []
    retsublinks = []
    cells = soup.find_all("td")
    for cell in cells:
        link = cell.find("a")
        if not link: continue # not in a cell that contains a link

        if str(link["href"]).endswith("/"):
            if link.contents and not link.contents[0] == "Parent Directory":
                newurl = baseurl + link["href"]
                #print("> get links from " + newurl)
                retsublinks.append(newurl)
            continue

        if link.contents and not link.contents[0].endswith(".bin"): continue #everything that isn't a firmware file

        datecell = cell.next_sibling
        changedate = datetime.datetime.strptime(datecell.contents[0].strip(), "%d-%b-%Y %H:%M")

        linko = LinkObject(currenturl + link["href"], changedate)
        retlinks.append(linko)
    return retlinks, retsublinks


def get_all_links(url):
    retlinks = []

    soup = bs(get_html(url), 'html.parser')
    links, sublinks = get_links(soup, baseurl)
    retlinks.extend(links)

    for sl in sublinks:
        soup = bs(get_html(sl), 'html.parser')
        links, _ = get_links(soup, sl) # only one level deep
        retlinks.extend(links)

    return retlinks

links = get_all_links(baseurl)
for l in links:
    #print(l.url, l.date)
    pass

files = []
timestamps = []
for root, directories, filenames in os.walk('/lib/firmware/radeon/'):
    #for directory in directories:
    #        print(os.path.join(root, directory))
    for filename in filenames:
        joined = os.path.join(root,filename)

        files.append(joined)

        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(joined)
        ts = datetime.datetime.fromtimestamp(int(mtime))
        timestamps.append(ts)
        #print("last modified: %s" % ts)

fileswithoutdir = [f.split("/")[-1] for f in files]

with open(scriptfile, "w") as f:
    f.write("#!/bin/sh\n\n")
    for webfirmware in links:
        fn = webfirmware.url.split("/")[-1]
        if fn not in fileswithoutdir:
            print(fn + " is not installed and can be downloaded")
            f.write("echo \"Downloading " + webfirmware.url + " to /lib/firmware/" + fn + "\"\n")
            f.write("wget " + webfirmware.url + " -O /lib/firmware/" + fn + " \n\n")

        if fn in fileswithoutdir and webfirmware.date > timestamps[fileswithoutdir.index(fn)]:
            print(fn + " is installed, but a newer version can be downloaded")
            print("Installed   : " + str(timestamps[fileswithoutdir.index(fn)]))
            print("Downloadable: " + str(webfirmware.date))
            f.write("echo \"Downloading " + webfirmware.url + " to /lib/firmware/" + fn + "\"\n")
            f.write("wget " + webfirmware.url + " -O /lib/firmware/" + fn + " \n\n")

subprocess.call(['chmod', '755', scriptfile])
print("Now run ./" + scriptfile + " as root")