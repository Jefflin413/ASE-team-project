"""http://flask.pocoo.org/docs/1.0/tutorial/database/"""
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from collections import defaultdict

def get_db():
    """get the database"""
    if "db" not in g:
        g.db = sqlite3.connect(
            "utils/sqlite_db", detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db():
    """close the database"""
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """initiate the database"""
    db = get_db()

    with current_app.open_resource("utils/schema.sql") as f:
        db.executescript(f.read().decode("utf8"))



@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """init_app"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_streaming():
    """get the data of specific user"""
    db = get_db()
    res = db.execute(
        "SELECT * FROM streaming"
    ).fetchall()
    if not res:
        return None
    
    ret = []
    for row in res:
        ret.append({'id': row[0], 'name': row[1], 'category': row[2]})
    return ret


def create_stream(id_, name, category):
    """create an stream"""
    db = get_db()
    db.execute(
        "INSERT INTO streaming (id, name, category)"
        " VALUES (?, ?, ?)",
        (id_, name, category),
    )
    db.commit()

def update_stream(id_, m3u8_URL):
    """update m3u8_URL for a stream"""
    db = get_db()
    db.execute(
        "UPDATE streaming"
        " SET m3u8_URL = (?)"
        " WHERE id = (?)",
        (m3u8_URL, id_),
    )
    db.commit()

def get_streaming_m3u8(id_):
    """get the data of specific user"""
    db = get_db()
    res = db.execute(
        "SELECT m3u8_URL FROM streaming"
        " WHERE id = (?)",
        (id_,)
    ).fetchall()
    if not res:
        return None
    
    ret = []
    for row in res:
        ret.append(row[0])
    return ret

def delete_stream(id_):
    """delete a stream"""
    db = get_db()
    db.execute(
        "DELETE FROM streaming"
        " WHERE id = (?)",
        (id_,),
    )
    db.commit()

def get_analytics_category_all():
    db = get_db()
    res = db.execute(
        "SELECT * FROM watch_history"
    ).fetchall()
    if not res:
        return None
    
    ret = defaultdict(int)
    for row in res:
        category = row[2]
        ret[category] += 1
        #rows.append({'watcher': row[0], 'streamer': row[1], 'category': row[2], 'start_time': row[2]})
    
    ret = [{"x": k, "value":v} for k,v in ret.items()]
    return ret
