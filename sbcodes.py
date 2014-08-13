import flask
import requests

app = flask.Flask(__name__)
app.config.from_envvar(u'SETTINGS_FILE')

@app.route(u'/ping')
def ping():
	c = requests.get(u'http://sbcodez.com/')
	_, _, code = c.text.partition(u'<span class="code">')
	code, _, _ = code.partition(u'</span>').strip()
	if code == app.config.get(u'LAST_CODE'):
		app.logger.debug(u'I already submitted the code {}.'.format(code))
		return u''
	url = u'http://www.swagbucks.com/'
	params = {u'cmd': u'sb-gimme-jx'}
	data = {u'hdnCmd': u'sb-gimme', u'pcode': code}
	for name, urqm in app.config.get(u'URQM').iteritems():
		cookies = {u'__urqm': urqm}
		r = requests.post(url, params=params, data=data, cookies=cookies)
		app.logger.info(u'{}: {}: {}'.format(name, code, r.json()[0]))
	app.config[u'LAST_CODE'] = code

if __name__ == u'__main__':
    app.run(host=u'0.0.0.0', debug=True)
