import logging
import os
import sys

import psycopg2
import pytoml as toml
import tornado.options

import db


def main(force=False):
    CURRENT_DIR = os.path.dirname(__file__)
    file_name = 'default-emoticons.toml'
    file_path = os.path.join(CURRENT_DIR, 'fixtures', file_name)
    with open(file_path, 'r') as f:
        try:
            emoticons = toml.load(f)
        except toml.core.TomlError:
            raise
            raise SystemExit(
                'LOAD_ERROR: Error reading source file, verify there are no '
                'syntax erros and you are using single quotes instead of '
                'double quotes for the content.')

    for name, emoticon in emoticons.iteritems():
        aliases = emoticon.get('aliases', [])
        content = emoticon.get('content')
        if not content:
            logging.warn('Empty "content" for emoticon "%s". Skipping.', name)
            continue

        try:
            emoticon_id = db.create_emoticon(name, content)
        except psycopg2.IntegrityError:
            if force:
                logging.warn('Emoticon "%s" already exists. Overwriting', name)
                # Remove first to cascade-delete any existing aliases
                db.remove_emoticon_or_alias(name)
                # Then create the replacement
                emoticon_id = db.create_emoticon(name, content)
            else:
                logging.warn('Emoticon "%s" already exists. Skipping.', name)
                continue

        logging.info('Created emoticon "%s"', name)

        for alias in aliases:
            db.create_alias(emoticon_id, alias)
            logging.info('-> Added alias "%s"', alias)

if __name__ == '__main__':
    tornado.options.define('force', default=False)
    tornado.options.parse_command_line()

    force = tornado.options.options.force
    main(force=force)
