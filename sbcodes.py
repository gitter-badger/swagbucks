#!/usr/bin/env python

import json
import os
import requests
import sys

path = os.path.dirname(os.path.realpath(__file__))
conf_file = u'{}/sbcodes.json'.format(path)

with open(conf_file, u'r') as f:
    conf = json.load(f)

c = requests.get(u'http://sbcodez.com/')
code = c.text.partition(u'<span class="code">')[2].partition(u'</span>')[0]
print(u'Current code is {}'.format(code))

if code == conf.get(u'last_code'):
    print(u'I already submitted this code.')
    sys.exit()

url = u'http://www.swagbucks.com/'
params = {u'cmd': u'sb-gimme-jx'}
data = {u'hdnCmd': u'sb-gimme', u'pcode': code}

for name, urqm in conf.get(u'urqm').iteritems():
    cookies = {u'__urqm': urqm}
    r = requests.post(url, params=params, data=data, cookies=cookies)
    print(u'{}: {}'.format(name, r.json()[0]))

conf[u'last_code'] = code

with open(conf_file, u'w') as f:
    json.dump(conf, f)
