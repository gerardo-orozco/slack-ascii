# -*- coding: utf8 -*-
import json
import logging
import os

import tornado.gen
import tornado.web

from slackclient import SlackClient

EMOTICONS = {
    'shrug': u'¯\\_(ツ)_/¯'
}
SLACK_TEAM_API_TOKEN = os.environ['SLACK_TEAM_API_TOKEN']


class APIHandler(tornado.web.RequestHandler):

    def error_response(self, body=None, status_code=500):
        self.set_status(500)
        self.finish(body)

    def help_message(self):
        message = 'Available emoticons:\n'
        for name, emoticon in EMOTICONS.iteritems():
            message += '*%s*: %s' % (name, emoticon)
        return message

    @tornado.gen.coroutine
    def post(self):
        slack = SlackClient(SLACK_TEAM_API_TOKEN)
        text = self.get_argument('text')

        if text == 'help':
            self.finish(self.help_message())

        try:
            emoticon = EMOTICONS[text]
        except KeyError:
            error_message = '`%s` not found. Enter `%s help` for a list of ' \
                'available ASCII emoticons'
            command_name = self.get_argument('command')
            self.error_response(error_message % (text, command_name))

        channel_id = self.get_argument('channel_id')
        user_token = self.get_argument('token')
        slack.api_call('chat.postMessage', **{
            'token': user_token,
            'channel': channel_id,
            'text': emoticon.encode('utf-8'),
            'as_user': True,
        })
        self.finish()
