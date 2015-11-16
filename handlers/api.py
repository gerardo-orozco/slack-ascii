# -*- coding: utf8 -*-
import json
import os
import tornado.gen
import tornado.web
from slackclient import SlackClient
from emoticon_api import EmoticonAPI


class APIHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        command_name = self.get_argument('command')
        emoticon_api = EmoticonAPI(command_name)
        text = self.get_argument('text').split(' ')
        text = [o for o in text if o]  # remove empty strings
        name, text = text[0], text[1:]

        if name == 'help':
            return self.finish(emoticon_api.get_help_message())

        elif name == 'add':
            message = emoticon_api.create(*text)
            return self.finish(message)

        elif name in 'rm':
            message = emoticon_api.remove(*text)
            return self.finish(message)

        elif name == 'set':
            message = emoticon_api.replace(*text)
            return self.finish(message)

        elif name == 'alias':
            message = emoticon_api.alias(*text)
            return self.finish(message)

        # default to fetch an emoticon
        slack = SlackClient(os.environ['SLACK_TEAM_API_TOKEN'])
        message = emoticon_api.get(name, *text)
        if not message:
            message = 'Emoticon `%s` not found. Enter `%s help` ' \
                'for a list of available ASCII emoticons'
            message = message % (name, command_name)
            return self.finish(message)

        channel_id = self.get_argument('channel_id')
        user_token = self.get_argument('token')
        slack.api_call('chat.postMessage', **{
            'token': user_token,
            'channel': channel_id,
            'text': message,
            'as_user': True,
        })
        self.finish()
