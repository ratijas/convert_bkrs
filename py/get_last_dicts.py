#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""downloading latest version of bkrs."""

from __future__ import unicode_literals, division
import os
import re
import sys

DEST_DIR = "downloads"
BKRS_DSL = "bkrs.dsl"
BRUKS_DSL = "bruks.dsl"
VERSION_TXT = "version.txt"
URLS_TXT = "urls.txt"


def downloaded_less_than_day_ago(files=(BKRS_DSL, BRUKS_DSL)):
    """downloaded_less_than_day_ago() --> bool

    check if modification time of dictionaries.
    if less than day ago, return True.
    """
    for f in files:
        if not os.path.isfile(f):
            return False
        ctime = os.stat(f).st_ctime
        if (time.time() - ctime) / 60 / 60 / 24 > 1:
            return False
    return True


def init():
    try:
        if not os.path.isdir(DEST_DIR):
            os.makedirs(DEST_DIR)
    except OSError, e:
        raise OSError("cannot create a folder: '%s'" % DEST_DIR)
    os.chdir(DEST_DIR)


def search():
    """search() --> (bkrs.gz url, bruks.gz url)

    """
    print "looking for last dictionaries..."
    import urllib2
    response = urllib2.urlopen("http://bkrs.info/p47")
    html = response.read()
    import lxml.etree as ET
    html_dom = ET.HTML(html)
    gz_links = [link.get("href")
                for link in html_dom.findall(".//a[@href]")
                if link.get("href").endswith(".gz")]
    gz_links = filter(lambda s: "examples" not in s, gz_links)
    if len(gz_links) != 2:
        raise Exception("cannot find one or both links!")
    version = re.search("([0-9]{6})", gz_links[0]).group(1)
    with open(VERSION_TXT, "w") as f:
        print >>f, 'v%s' % version
    bkrs_url = "http://bkrs.info/" + filter(lambda s: "bkrs" in s, gz_links)[0]
    bruks_url = "http://bkrs.info/" + filter(lambda s: "bruks" in s, gz_links)[0]
    with open(URLS_TXT, "w") as f:
        print >>f, bkrs_url
        print >>f, bruks_url
    print "found urls:"
    print "--> %s\n--> %s" % (bkrs_url, bruks_url)
    return bkrs_url, bruks_url


def download(urls):
    """download(list_of_urls) --> list of file names

    download files from urls,
    return their absolute paths in local file system.
    """
    print "downloading files..."

    import progress_bar

    file_names = []
    for url in urls:
        file_name = os.path.basename(url)
        file_names.append(os.path.abspath(file_name))
        import urllib2
        response = urllib2.urlopen(url)

        # with progress animation
        meta = response.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "downloading: '%s', bytes: %s" % (file_name, file_size)
        with open(file_name, "wb") as f:
            file_size_dl = 0
            block_sz = 8192
            pbc = progress_bar.ProgressBarController(0, file_size)
            while True:
                buffer = response.read(block_sz)
                if not buffer:
                    urls.append(url)  # retry later
                    print "\nretry later..."
                    break
                file_size_dl += len(buffer)
                f.write(buffer)

                pbc.set_value(file_size_dl)
                print str(pbc) + "\r",
                sys.stdout.flush()
            print ""
    print "downloaded!"
    return file_names


def unarchive_and_remove_bom(files):
    import gzip
    for f in files:
        with gzip.open(f, 'rb') as f:
            file_content = f.read()


def clean():
    if os.path.dirname(os.path.abspath(os.getcwd())) == DEST_DIR:
        try:
            # os.remove()
            pass
        except OSError, e:
            pass


def main(force=False):
    try:
        if not force and downloaded_less_than_day_ago():
            print "словарные базы загружены менее суток назад.\n"\
                  "чтобы всё-равно скачать новые базы, запустите\n"\
                  "%s -f" % sys.argv[0]
            return
        init()
        urls = search()
        file_names = download(urls)
    except:
        try:
            clean()
        except:
            pass
        raise


if __name__ == '__main__':
    import sys
    is_force = "-f" in sys.argv
    main(is_force)
