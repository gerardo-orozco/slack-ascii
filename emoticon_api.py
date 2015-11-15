import db


def create(*args):
    name, content = args[0], ' '.join(args[1:])
    if not content:  # not exactly two "arguments"
        return 'Please specify a name and the emoticon ' \
            'text. Example: `/ascii add foo (o_o)`'

    existing = db.get_emoticon(name)
    if existing is not None:
        return '`%s` is already assigned to an emoticon.' % name

    new_emoticon_id = db.create_emoticon(name, content)
    if new_emoticon_id:
        return 'Emoticon `%s` added' % name


def get(*args):
    name, additional_text = args[0], ' '.join(args[1:])
    emoticon = db.get_emoticon(name)
    if emoticon is None:
        return

    emoticon = '%s %s' % (emoticon, additional_text)
    return emoticon


def remove(*args):
    if not args:
        return 'Indicate the name of the emoticon or alias to remove'
    db.remove_emoticon_or_alias(args[0])
    return 'Removed `%s`' % args[0]
