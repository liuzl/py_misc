#!/usr/bin/python

import os
import sys
from io import BytesIO

from selenium import webdriver
from PIL import Image


def crawl(url, filename):
    global browser
    global debug
    browser.get(url)
    #"https://zh.wikipedia.org/wiki/%E9%9B%BB%E5%AD%90%E8%A8%88%E7%AE%97%E6%A9%9F"

    js = 'return Math.max( document.body.scrollHeight, document.body.offsetHeight,  document.documentElement.clientHeight,  document.documentElement.scrollHeight,  document.documentElement.offsetHeight);'

    scrollheight = browser.execute_script(js)

    if debug:
        print(scrollheight)

    slices = []
    offset = 0
    while offset < scrollheight:
        if debug:
            print('offset:', offset)

        browser.execute_script("window.scrollTo(0, %s);" % offset)
        img = Image.open(BytesIO(browser.get_screenshot_as_png()))
        offset += img.size[1]
        if scrollheight < offset:
            slices.append(
                img.crop((0, offset - scrollheight, img.size[0], img.size[1])))
        else:
            slices.append(img)

        if debug:
            browser.get_screenshot_as_file(
                os.path.join(dirname, 'screen_%s.png' % offset))
            print('scroll:', scrollheight)

    screenshot = Image.new('RGB', (slices[0].size[0], scrollheight))
    offset = 0
    for img in slices:
        screenshot.paste(img, (0, offset))
        offset += img.size[1]

    screenshot.save(os.path.join(dirname, filename))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage python %s <url> <pngfilename>" % sys.argv[0])
        sys.exit(1)
    url = sys.argv[1]
    filename = sys.argv[2]

    dirname = 'results'
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    debug = False
    
    options = webdriver.ChromeOptions()

    #chrome headless option
    options.add_argument('headless')

    browser = webdriver.Chrome(options=options)
    crawl(url, filename)
    browser.quit()
