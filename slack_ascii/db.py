import os
import psycopg2
import tornado.gen


def get_connection():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        raise ValueError('DATABASE_URL environment variable needs to be defined and not empty')
    return psycopg2.connect(db_url)


def create_emoticon(name, content):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO emoticon (name, content) VALUES (%s, %s) RETURNING id"
    cursor.execute(sql, (name, content))
    last_id = cursor.fetchone()[0]
    conn.commit()
    return last_id


def create_alias(emoticon_id, alias):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO emoticon_alias (emoticon_id, name) VALUES (%s, %s) RETURNING id"
    cursor.execute(sql, (emoticon_id, alias))
    last_id = cursor.fetchone()[0]
    conn.commit()
    return last_id


def get_emoticon(name_or_alias):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """SELECT e.id, e.content
    FROM emoticon e LEFT JOIN emoticon_alias ea ON e.id = ea.emoticon_id
    WHERE e.name = %(name_or_alias)s OR ea.name = %(name_or_alias)s
    LIMIT 1"""
    cursor.execute(sql, {'name_or_alias': name_or_alias})
    emoticon = cursor.fetchone()
    if emoticon:
        return {'id': emoticon[0], 'content': emoticon[1]}


def remove_emoticon_or_alias(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM emoticon WHERE name = %(name)s", {'name': name})
    if cursor.fetchone():
        cursor.execute("DELETE FROM emoticon WHERE name = %(name)s", {'name': name})
    else:
        cursor.execute("DELETE FROM emoticon_alias WHERE name = %(name)s", {'name': name})
    conn.commit()


def replace_emoticon(name, content):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE emoticon SET content = %(content)s WHERE name = %(name)s RETURNING id"
    cursor.execute(sql, {'content': content, 'name': name})
    updated = bool(cursor.fetchone())
    conn.commit()
    return updated


def get_help_info():
    conn = get_connection()
    cursor = conn.cursor()
    sql = """SELECT e.name, e.content, a.name
    FROM emoticon e LEFT JOIN emoticon_alias a on e.id = a.emoticon_id
    ORDER BY e.name"""
    cursor.execute(sql)
    emoticons = []
    emoticons_by_name = {}
    for name, content, alias in cursor.fetchall():
        if name not in emoticons_by_name:
            emoticons_by_name[name] = {
                'aliases': [],
                'content': content
            }
        if alias:
            emoticons_by_name[name]['aliases'].append(alias)

    for name, emoticon in emoticons_by_name.iteritems():
        emoticons.append({
            'name': name,
            'aliases': emoticon['aliases'],
            'content': emoticon['content']
        })

    emoticons.sort(key=lambda o: o['name'])
    return emoticons
