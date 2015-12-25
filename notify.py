#!/usr/bin/env python
# coding: utf-8

import webapp2
import datetime
import env
import urllib
import json
import uuid
import logging
from google.appengine.api import urlfetch

ENDPOINT = 'https://todoist.com/API/v6/sync'

MESSAGE = u'Bully\'s day'
DUE_DATE = u'21:00'


def add_todoist_item():
    commands = [{'type': 'item_add',
                 'uuid': str(uuid.uuid1()),
                 'temp_id': '',
                 'args': {'content': MESSAGE,
                          'date_string': DUE_DATE}}]

    payload = {'token': env.token,
               'commands': json.dumps(commands)}

    headers={'Content-Type': 'application/x-www-form-urlencoded'}

    result = urlfetch.fetch(url=ENDPOINT,
                            payload=urllib.urlencode(payload),
                            method=urlfetch.POST,
                            headers=headers)
    if result.result_code != 200:
        raise Exception(u'status code is ' + str(result.result_code) )

    logging.debug(result.content)


def is_training_day(date=datetime.datetime.now()):
    if date.day % 3 != 0 and date.day != 31:
        return True
    return False


class NotifyHandler(webapp2.RequestHandler):
    def get(self):
        today = datetime.datetime.now() + datetime.timedelta(hours=9)
        if is_training_day(today):
            try:
                add_todoist_item()
            except Exception, e:
                logging.error(e.message)

        self.response.write('added task')

app = webapp2.WSGIApplication([
    ('/task/notify', NotifyHandler)
], debug=False)
