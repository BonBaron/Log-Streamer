from urllib2 import HTTPError
from tornado import httpclient
from tornado.httpclient import HTTPRequest

client = httpclient.HTTPClient()
request = HTTPRequest(url='http://127.0.0.1:8888/read_log', method="GET")
try:
    response = client.fetch(request)
    print(response.body)
except HTTPError as err:
    res = err.response
    if res:
        print(res.body)
