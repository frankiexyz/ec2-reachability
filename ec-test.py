#!/usr/bin/env python

from __future__ import print_function
import requests
import re
from multiprocessing import Pool
ec2_url = requests.get("http://ec2-reachability.amazonaws.com/").text
regex = r"\<img src=\"(\S*)\">"
http200 = []
nonhttp200 = []
def check_url(url):
    global http200
    global nonhttp200
    output = None
    try:
        output = requests.get(url, timeout=3).status_code
    except Exception as e:
        print("{} timeout\n{}".format(url, e))
        nonhttp200.append(url)
    if output != 200:
        print("{} status code != 200".format(url))
        nonhttp200.append(url)
    else:
        http200.append(url)
urllist = re.findall(regex, ec2_url)
p = Pool(5)
pool_output = p.map(check_url, urllist)
