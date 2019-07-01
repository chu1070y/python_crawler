import ssl
import sys

from datetime import datetime
from urllib.request import urlopen, Request


def crawling(url='',
             encoding='utf-8',
             err=lambda e: print('%s : %s' % (e, datetime.now()), file=sys.stderr),
             proc1=lambda data: data,
             proc2=lambda data: data):
    try:
        request = Request(url)

        ssl._create_default_https_context = ssl._create_unverified_context
        response = urlopen(request)

        receive = response.read()

        return proc2(proc1(receive.decode(encoding, errors='replace')))

    except Exception as e:
        err(e)
