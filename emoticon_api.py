import db


def create(name, content):
    if not content:
        return 'Please specify the emoticon you want to use.'

    existing = db.get_emoticon(name)
    if existing is not None:
        return '`%s` is already assigned to an emoticon.' % name

    new_emoticon_id = db.create_emoticon(name, content)
    if new_emoticon_id:
        return 'Emoticon `%s` added' % name
