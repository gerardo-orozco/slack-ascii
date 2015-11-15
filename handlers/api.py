# -*- coding: utf8 -*-
import json
import os
import tornado.gen
import tornado.web
from slackclient import SlackClient
import emoticon_api

EMOTICONS = {
    'shrug': u'¯\\_(ツ)_/¯'
}
SLACK_TEAM_API_TOKEN = os.environ['SLACK_TEAM_API_TOKEN']


class APIHandler(tornado.web.RequestHandler):

    def help_message(self):
        message = 'Available emoticons:\n'
        for name, emoticon in EMOTICONS.iteritems():
            message += '*%s*: %s' % (name, emoticon)
        return message

    @tornado.gen.coroutine
    def post(self):
        slack = SlackClient(SLACK_TEAM_API_TOKEN)
        text = self.get_argument('text').split(' ')
        text = [o for o in text if o]  # remove empty strings
        name, text = text[0], text[1:]

        if name == 'help':
            return self.finish(self.help_message())

        elif name == 'add':
            message = emoticon_api.create(*text)
            return self.finish(message)

        elif name in 'rm':
            message = emoticon_api.remove(*text)
            return self.finish(message)

        elif name == 'set':
            message = emoticon_api.replace(*text)
            return self.finish(message)

        # default to fetch an emoticon
        message = emoticon_api.get(name, *text)
        if message is None:
            message = 'Emoticon `%s` not found. Enter `%s help` ' \
                'for a list of available ASCII emoticons'
            command_name = self.get_argument('command')
            message = message % (name, command_name)
            return self.finish(message)

        channel_id = self.get_argument('channel_id')
        user_token = self.get_argument('token')
        slack.api_call('chat.postMessage', **{
            'token': user_token,
            'channel': channel_id,
            'text': message.encode('utf-8'),
            'as_user': True,
        })
        self.finish()
