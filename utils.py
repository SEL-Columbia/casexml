#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 fileencoding=utf-8
# maintainer: katembu
import os
import codecs
from urlparse import urlparse
import httplib

from datetime import datetime
import const as CONST


def transmit_form(form, domain_url):
    ''' Submit data to commcare server '''

    xml_form = form.render()
    headers = {"Content-type": "text/xml", "Accept": "text/plain"}

    xml_form = xml_form.encode('utf-8')
    url = domain_url
    up = urlparse(url)
    conn = httplib.HTTPSConnection(up.netloc) if url.startswith("https") \
        else httplib.HTTPConnection(up.netloc)
    conn.request('POST', up.path, xml_form, headers)
    resp = conn.getresponse()
    responsetext = resp.read()
    if resp.status == 502:
        print "Retrying ..."
        transmit_form(form, domain_url)
    elif resp.status == 201:
        print "Thanks for submitting %s " % responsetext
    else:
        print "Bad HTTP Response: [%s] %s " % (resp.status, responsetext)


def save_casexmlform(form):
    ''' save templates of casexml '''
    xml_form = form.render()
    try:
        STORE_FORM = CONST.STORE_FORM
        STORE_LOCATION = CONST.STORE_LOCATION
    except:
        STORE_FORM = False
        STORE_LOCATION = u"/tmp"

    if STORE_FORM:
        print "Saving Form in output folder"
        f = codecs.open("%(path)s/casexml_%(date)s.xml" % {
            'path': STORE_LOCATION,
            'date': datetime.now().strftime("%Y_%m_%d_%H-%M-%S.%f")},
            'wb', encoding='utf-8', buffering=1)
        f.write(xml_form)
        f.close()


def check_file(file_name, ftype):
    exist = True
    if not os.path.exists(file_name):
        exist = False
    if file_name.split(".")[-1] != ftype:
        exist = False

    return exist
