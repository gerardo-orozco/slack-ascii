# -*- coding: utf8 -*-
import json
import os
import tornado.gen
import tornado.web
from slackclient import SlackClient
from emoticon_api import EmoticonAPI


class APIHandler(tornado.web.RequestHandler):
    """
    A request handler to respond to the slash command as configured in slack
    by the slack team.
    """

    @tornado.gen.coroutine
    def post(self):
        command_name = self.get_argument('command')
        emoticon_api = EmoticonAPI(command_name)
        text = self.get_argument('text').split(' ')
        text = [o for o in text if o]  # remove empty strings
        name, text = text[0], text[1:]

        # Print the available emoticons as a slackbot ephemeral message
        if name == 'help':
            return self.finish(emoticon_api.get_help_message())

        # Add a new emoticon
        elif name == 'add':
            message = emoticon_api.create(*text)
            return self.finish(message)

        # Add a new alias to an existing emoticon
        elif name == 'alias':
            message = emoticon_api.alias(*text)
            return self.finish(message)

        # Remove an existing emoticon or alias. When an alias is sent,
        # only the alias will be removed and the original emoticon will
        # still be available.
        elif name in 'rm':
            message = emoticon_api.remove(*text)
            return self.finish(message)

        # Replace the emoticon that a given name represents. The original name
        # is required for replacing the emoticon.
        elif name == 'set':
            message = emoticon_api.replace(*text)
            return self.finish(message)

        # Fetch an emoticon by it's name or one of its aliases and send it
        # to the source channel as if the authed user had posted it.
        try:
            slack = SlackClient(os.environ['SLACK_TEAM_API_TOKEN'])
        except KeyError:
            return self.finish('`SLACK_TEAM_API_TOKEN` is not set in the server')

        emoticon = emoticon_api.get(name)
        try:
            emoticon = unicode(emoticon)
        except UnicodeDecodeError:
            emoticon = emoticon.decode('utf-8')

        message = '%(command)s %(name)s %(emoticon)s %(text)s' % {
            'command': command_name,
            'name': name,
            'emoticon': emoticon,
            'text': ' '.join(text)
        }

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
