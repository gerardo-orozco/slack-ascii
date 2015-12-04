import db


class EmoticonAPI(object):

    def __init__(self, command_name):
        self._command_name = command_name

    def get(self, name):
        emoticon = db.get_emoticon(name)
        if not emoticon:
            return

        if '\n' in emoticon['content']:
            # Displaying multiline emoticons/ascii art improves readability
            emoticon['content'] = '```%s```' % emoticon['content']

        return emoticon['content']

    def create(self, *args):
        try:
            name, content = args[0], ' '.join(args[1:])
            name = name.lower()
        except IndexError:
            content = None
        if not content:
            return 'Please specify a name and the emoticon ' \
                'text. Example: `%s add foo (o_o)`' % self._command_name

        existing = db.get_emoticon(name)
        if existing is not None:
            return '`%s` is already assigned to an emoticon.' % name

        try:
            content = content.encode('utf-8')
        except UnicodeEncodeError:
            pass
        if db.create_emoticon(name, content):
            return 'Emoticon `%s` added' % name

    def remove(self, *args):
        if not args:
            return 'Indicate the name of the emoticon or alias to remove'
        db.remove_emoticon_or_alias(args[0])
        return 'Removed `%s`' % args[0]

    def replace(self, *args):
        name, content = args[0], ' '.join(args[1:])
        if not content:  # not exactly two "arguments"
            return 'Please specify a name and the emoticon ' \
                'text. Example: `%s set foo (o_o)`' % self._command_name

        updated = db.replace_emoticon(name, content)
        if updated:
            return 'Updated `%s`' % name
        return '`%s` does not exist. Are you using an alias?' % name

    def alias(self, *args):
        try:
            name, alias = args[0], args[1]
        except IndexError:
            return 'Indicate a name and an alias: `%s alias foo bar`, ' \
                'where `foo` is the original name and `alias` is an ' \
                'additional name.'

        emoticon = db.get_emoticon(name)
        if not emoticon:
            return 'Emoticon `%s` not found. Enter `%s help` ' \
                'for a list of available ASCII emoticons'

        if db.get_emoticon(alias):
            return '`%s` is already taken' % name

        if db.create_alias(emoticon['id'], alias):
            return 'Aliased `%s` -> `%s`' % (alias, name)

    def get_help_message(self):
        emoticons = db.get_help_info()
        if not emoticons:
            return 'Sorry, there are no emoticons loaded yet :-('

        message = ''
        for emoticon in emoticons:
            # start with the emoticon name
            msg_line = '*%s*' % emoticon['name']

            aliases = ', '.join(emoticon['aliases'])
            if aliases:
                # attach the aliases part of the message
                # only if there are any aliases
                msg_line += ' (aliases: %s)' % aliases

            # finally, append the emoticon
            if '\n' in emoticon['content']:
                msg_line += '\n```%s```\n' % emoticon['content']
            else:
                msg_line += '\n>%s\n' % emoticon['content']
            message += msg_line
        return message
