# NOTES:
# You can use https://en.wikipedia.org/wiki?curid=<id> to get to a page!


# Simple example of streaming a Wikipedia 
# Copyright 2017 by Jeff Heaton, released under the The GNU Lesser General Public License (LGPL).
# http://www.heatonresearch.com
# -----------------------------
import xml.etree.ElementTree as etree
import codecs
import csv
import time
import os
import re

# http://www.ibm.com/developerworks/xml/library/x-hiperfparse/

PATH_WIKI_XML = './'
FILENAME_WIKI = 'enwiki-20170820-pages-articles-multistream.xml'
FILENAME_ARTICLES = 'articles.csv'
FILENAME_REDIRECT = 'articles_redirect.csv'
FILENAME_TEMPLATE = 'articles_template.csv'
ENCODING = "utf-8"


# Nicely formatted time string
def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


def strip_tag_name(t):
    t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t


pathWikiXML = os.path.join(PATH_WIKI_XML, FILENAME_WIKI)
pathArticles = os.path.join(PATH_WIKI_XML, FILENAME_ARTICLES)
pathArticlesRedirect = os.path.join(PATH_WIKI_XML, FILENAME_REDIRECT)
pathTemplateRedirect = os.path.join(PATH_WIKI_XML, FILENAME_TEMPLATE)

totalCount = 0
articleCount = 0
articleCount2 = 0
redirectCount = 0
templateCount = 0
bracketTypos = 0
emptyPages = 0
title = None
start_time = time.time()

with codecs.open(pathArticles, "w", ENCODING) as articlesFH, \
        codecs.open(pathArticlesRedirect, "w", ENCODING) as redirectFH, \
        codecs.open(pathTemplateRedirect, "w", ENCODING) as templateFH:
    articlesWriter = csv.writer(articlesFH, quoting=csv.QUOTE_MINIMAL, delimiter='$')
    redirectWriter = csv.writer(redirectFH, quoting=csv.QUOTE_MINIMAL, delimiter='$')
    templateWriter = csv.writer(templateFH, quoting=csv.QUOTE_MINIMAL)

    articlesWriter.writerow(['id', 'title', 'links'])
    redirectWriter.writerow(['id', 'title', 'redirect'])
    templateWriter.writerow(['id', 'title'])

    for event, elem in etree.iterparse(pathWikiXML, events=('start', 'end')):
        tname = strip_tag_name(elem.tag)

        if event == 'start':
            if tname == 'page':
                title = ''
                id = -1
                redirect = ''
                inrevision = False
                ns = 0
            elif tname == 'revision':
                # Do not pick up on revision id's
                inrevision = True
        else:
            if tname == 'title':
                title = elem.text
            elif tname == 'id' and not inrevision:
                id = int(elem.text)
            elif tname == 'redirect':
                redirect = elem.attrib['title']
            elif tname == 'ns':
                ns = int(elem.text)
            elif tname == 'page':
                totalCount += 1

                if ns == 10:
                    templateCount += 1
                    #templateWriter.writerow([id, title])
                elif len(redirect) > 0:
                    redirectCount += 1
                    redirectWriter.writerow([id, title, redirect])
                else:
                    articleCount += 1
                #    articleCount += 1
                #    articlesWriter.writerow([id, title, redirect])

                #if totalCount > 10000:
                #    break

                if totalCount > 1 and (totalCount % 100000) == 0:
                    print("{:,}".format(totalCount))
                    elapsed_time = time.time() - start_time
                    print("Elapsed time: {}".format(hms_string(elapsed_time)))

            #elif tname == 'text':

            #    if ns != 10 and len(redirect) == 0:

            #        articleCount2 += 1

            #        if type(elem.text) is str:

            #            # search for links in elem.text

            #            stripped_text = elem.text.replace('\n', '')


            #            row = [id, title]

            #            for m in re.finditer('\[\[', stripped_text):

            #                end = stripped_text.find(']]', m.start()+2)
            #                if end != -1:

            #                    link = stripped_text[m.start()+2 : end]

            #                    if '\n' in link:
            #                        print("oops")

            #                    row.append(link)

            #                else:
            #                    print("Couldn't find matching end brace (or double stacked):", id, "at:", m.start())
            #                    bracketTypos += 1


            #            articlesWriter.writerow(row)

            #        else:
            #            print("Text field is not a string:", id)
            #            emptyPages += 1

            elem.clear()

elapsed_time = time.time() - start_time

print("Total pages: {:,}".format(totalCount))
print("Template pages: {:,}".format(templateCount))
print("Article pages: {:,}".format(articleCount))
print("Article pages 2: {:,}".format(articleCount2))
print("Redirect pages: {:,}".format(redirectCount))
print("Bracket typos: {:,}".format(bracketTypos))
print("Empty pages: {:,}".format(emptyPages))
print("Elapsed time: {}".format(hms_string(elapsed_time)))
