#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db

import tweepy
import comment


class ShowTimeline(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!<br>')
        
        CONSUMER_KEY = 'JhyigwId8U3Pn4nobdQ'
        CONSUMER_SECRET = '1rBJsJFIFwyAvgPNvO20GUFp3IV5zOJWa1tiBsZoQ'
        ACCESS_KEY = '264046987-VRaRbOwwfcobBqI5kqTOPgbhxJ7FRgXr1iwab4'
        ACCESS_SECRET = 'fJ6ddZW1QDAOPlrtxsieUrZOO6R4tuthPPRrQqmjs'

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)

        tl_list = api.home_timeline()

        self.response.out.write("<br>ics2010b4's timeline<br>")

        for tl in tl_list:
            self.response.out.write(tl.text)
            self.response.out.write('<br>')


class LastIdDataBase(db.Model):
    last_id = db.StringProperty(multiline=False)


class Init(webapp.RequestHandler):
    def get(self):
        init_id = LastIdDataBase(last_id = '0')
        init_id.put()
        self.response.out.write('init ok!')
        

class HelloWorld(webapp.RequestHandler):
    def get(self):
        CONSUMER_KEY = 'JhyigwId8U3Pn4nobdQ'
        CONSUMER_SECRET = '1rBJsJFIFwyAvgPNvO20GUFp3IV5zOJWa1tiBsZoQ'
        ACCESS_KEY = '264046987-VRaRbOwwfcobBqI5kqTOPgbhxJ7FRgXr1iwab4'
        ACCESS_SECRET = 'fJ6ddZW1QDAOPlrtxsieUrZOO6R4tuthPPRrQqmjs'

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)

        query = db.Query(LastIdDataBase)
        result = query.get()

        if(result.last_id=='0'):
            mentions = api.mentions()
        else:
            mentions = api.mentions(since_id = result.last_id)
            self.response.out.write(result.last_id)
            self.response.out.write('<br>')

        if(len(mentions)!=0):
            result.delete()
            mem_id = LastIdDataBase(last_id=mentions[0].id_str)
            mem_id.put()

        for mention in mentions:
            if(mention.text == '@ics2010b4 Hello'):
                status = u'@%s world!' % mention.author.screen_name
                api.update_status(status)
                self.response.out.write('ok')

            
def main():
    application = webapp.WSGIApplication([('/', ShowTimeline),
                                          ('/hello', HelloWorld),
                                          ('/init', Init)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
