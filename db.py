import os
import psycopg2
import tornado.gen


def cached(func, cache={}):
    def decorated():
        if func.__name__ not in cache:
            cache[func.__name__] = func()
        return cache[func.__name__]
    return decorated


@cached
def get_connection():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        raise ValueError('DATABASE_URL environment variable needs to be defined and not empty')
    return psycopg2.connect(db_url)


def create_emoticon(name, content):
    conn = get_connection()
    sql = "INSERT INTO emoticon (name, content) VALUES (%s, %s)"
    cursor = conn.cursor()
    cursor.execute(sql, (name, content))
    last_id = cursor.fetchone()[0]
    conn.commit()
    return last_id


def get_emoticon(name_or_alias):
    conn = get_connection()
    sql = """SELECT e.content
    FROM emoticon e INNER JOIN emoticon_alias ea ON e.id = ea.emoticon_id
    WHERE e.name = %(name_or_alias)s OR ea.name = %(name_or_alias)s
    LIMIT 1"""
    cursor = conn.cursor()
    cursor.execute(sql, {'name_or_alias': name_or_alias})
    emoticon = cursor.fetchone()
    if emoticon:
        return emoticon[0]
