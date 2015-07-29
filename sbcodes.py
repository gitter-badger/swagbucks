#!/usr/bin/env python3

import datetime
import json
import os
import pathlib
import requests


def log(message):
    t = datetime.datetime.utcnow().replace(microsecond=0)
    print('{} {}'.format(t, message))


def main():
    log('Starting up.')
    conf = {}
    home = pathlib.Path(os.environ.get('HOME')).resolve()
    conf_file = home / '.config/swagbucks/sbcodes.json'
    if not conf_file.parent.exists():
        conf_file.parent.mkdir(parents=True)
    if conf_file.exists():
        with conf_file.open() as f:
            conf = json.load(f)

    c = requests.get('http://sbcodez.com/')
    _, _, code = c.text.partition('<span class="code">')
    code, _, _ = code.partition('</span>')
    code = code.strip()

    if code == conf.get('last_code'):
        log('I already submitted the code {!r}.'.format(code))
    else:
        url = 'http://www.swagbucks.com/'
        params = {'cmd': 'sb-gimme-jx'}
        data = {'hdnCmd': 'sb-gimme', 'pcode': code}

        for name, urqm in conf.get('urqm', {}).items():
            cookies = {'__urqm': urqm}
            r = requests.post(url, params=params, data=data, cookies=cookies)
            log('{}: {}: {}'.format(name, code, r.json()[0]))
        conf['last_code'] = code

    with conf_file.open('w') as f:
        json.dump(conf, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    main()
