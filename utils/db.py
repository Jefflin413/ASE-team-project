"""http://flask.pocoo.org/docs/1.0/tutorial/database/"""
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from collections import defaultdict
from datetime import date, datetime
from click.testing import CliRunner
import os.path
from os import path



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
    if path.exists("utils/schema.sql"):
        with current_app.open_resource("utils/schema.sql") as f:
            db.executescript(f.read().decode("utf8"))
    else:
        pass



@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    # click.echo("Initialized the database.")

def get_streaming():
    """get the data of specific user"""
    db = get_db()
    res = db.execute(
        "SELECT * FROM streaming"
    ).fetchall()
    if not res:
        return None
    db.commit()
    
    ret = []
    for row in res:
        ret.append({'id': row[0], 'name': row[1], 'category': row[2]})
    return ret


def create_stream(id_, name, category):
    """create an stream"""
    if name is not None:    
        db = get_db()
        db.execute(
            "INSERT INTO streaming (id, name, category, current_watching)"
            " VALUES (?, ?, ?, ?)",
            (id_, name, category, 0),
        )
        db.commit()
    else:
         pass

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
    db.commit()
    
    ret = []
    for row in res:
        ret.append(row[0])
    return ret

def get_current_watching(id_):
    db = get_db()
    res = db.execute(
        "SELECT current_watching FROM streaming"
        " WHERE id = (?)",
        (id_,)
    ).fetchall()
    db.commit()
    if not res:
        return None
    current_watching = res[0][0]
    return current_watching

def update_current_watching(id_, increase=True):
    db = get_db()
    res = db.execute(
        "SELECT current_watching FROM streaming"
        " WHERE id = (?)",
        (id_,)
    ).fetchall()
    db.commit()
    if not res:
        return None
    current_watching = res[0][0]
    if increase:
        current_watching += 1
    else:
        current_watching -= 1
    
    db.execute(
        "UPDATE streaming"
        " SET current_watching = (?)"
        " WHERE id = (?)",
        (current_watching, id_),
    )
    db.commit()

def delete_stream(id_):
    """delete a stream"""
    db = get_db()
    db.execute(
        "DELETE FROM streaming"
        " WHERE id = (?)",
        (id_,),
    )
    db.commit()

def insert_watch_history(watcher, streamer, UUID):
    if streamer == None:
        return
    
    db = get_db()
    res =  db.execute(
        "SELECT category FROM streaming"
        " WHERE id = (?)",
        (streamer,),
    ).fetchone()
    
    if res == None:
        return
    category = res[0]
    #today = date.today()
    #time = today.strftime("%Y/%m/%d")
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    db.execute(
        "INSERT INTO watch_history (UUID, watcher, streamer, category, start_time)"
        " VALUES (?,?,?,?,?)",
        (UUID, watcher, streamer, category, time),
    )
    
    db.commit()

def update_watch_history(UUID):
    # use to add end_time into watch history
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    db = get_db()
    db.execute(
        "UPDATE watch_history"
        " SET end_time = (?)"
        " WHERE UUID = (?)",
        (time, UUID),
    )
    db.commit()

def get_watch_history(watcher):
    db = get_db()
    res = db.execute(
        "SELECT streamer, start_time, end_time FROM watch_history"
        " WHERE watcher = (?)",
        (watcher,),
    ).fetchall()

    ret_list = []
    if res:
        for row in res:
            if row[2]:
                ret_list.append("streamer id: " + row[0] + ", from " + row[1] + " to " + row[2])
            else:
                ret_list.append("streamer id: " + row[0] + ", from " + row[1])
        return ret_list
    else:
        return None
    
    

def get_analytics_category_all():
    db = get_db()
    res = db.execute(
        "SELECT * FROM watch_history"
    ).fetchall()
    if not res:
        return None
    
    ret = defaultdict(int)
    for row in res:
        category = row[3]
        ret[category] += 1
        #rows.append({'UUID': row[0], 'watcher': row[1], 'streamer': row[2], 'category': row[3], 'start_time': row[4], 'end_time': row[5]})
    
    ret_list = list(ret.keys())
    ret = [{"x": k, "value":v} for k,v in ret.items()]
    
    return ret, ret_list

def get_analytics_category(category):
    db = get_db()
    res = db.execute(
        "SELECT * FROM watch_history WHERE category='" + category + "'"
    ).fetchall()
    if not res:
        return None
    
    ret = defaultdict(int)
    for row in res:
        date = row[4].split(' ')[0]
        ret[date] += 1
        #rows.append({'UUID': row[0], 'watcher': row[1], 'streamer': row[2], 'category': row[3], 'start_time': row[4], 'end_time': row[5]})
    
    ret = sorted([{"date": k, "value":v} for k,v in ret.items()], key = lambda x: x['date'])
    
    db = get_db()
    res = db.execute(
        "SELECT DISTINCT category FROM watch_history"
    ).fetchall()
    
    ret_list = []
        
    for row in res:
        ret_list.append(row[0])
    
    return ret, ret_list

def get_analytics_user_all():
    db = get_db()
    res = db.execute(
        "SELECT * FROM watch_history"
    ).fetchall()
    if not res:
        return None
    
    ret = defaultdict(int)
    for row in res:
        streamer = row[2]
        ret[streamer] += 1
        #rows.append({'UUID': row[0], 'watcher': row[1], 'streamer': row[2], 'category': row[3], 'start_time': row[4], 'end_time': row[5]})
    
    ret_list = list(ret.keys())
    ret = [{"x": k, "value":v} for k,v in ret.items()]
    
    return ret, ret_list

def get_analytics_user(userid):
    db = get_db()
    res = db.execute(
        "SELECT * FROM watch_history where streamer='" + userid + "'"
    ).fetchall()
    if not res:
        return None
    
    ret = defaultdict(int)
    for row in res:
        date = row[4].split(' ')[0]
        ret[date] += 1
        #rows.append({'UUID': row[0], 'watcher': row[1], 'streamer': row[2], 'category': row[3], 'start_time': row[4], 'end_time': row[5]})
    
    ret = sorted([{"date": k, "value":v} for k,v in ret.items()], key = lambda x: x['date'])
    
    db = get_db()
    res = db.execute(
        "SELECT DISTINCT streamer FROM watch_history"
    ).fetchall()
    
    ret_list = []

    for row in res:
            ret_list.append(row[0])
    
    return ret, ret_list
    
def update_user(id_, name=None, email=None, profile_pic=None, usertype=None):
    
    db = get_db()
    sql = "UPDATE user SET "
    if name and email and profile_pic and usertype:
        sql += "name = '" + name + "',"
        sql += "email = '" + email + "',"
        sql += "profile_pic = '" + profile_pic + "',"
        sql += "usertype = '" + usertype + "'"    
        sql += " WHERE id = '" + id_ + "'"
        print(sql)
        db.execute(sql)
        db.commit()
    else:
        pass

def insert_audience_comment(watcher, streamer, message):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    db = get_db()
    db.execute(
        "INSERT INTO audience_comment (watcher, streamer, message, sent_time)"
        " VALUES (?,?,?,?)",
        (watcher, streamer, message, time),
    )
    
    db.commit()

def get_audience_comment(streamer):

    db = get_db()
    res = db.execute(
        "SELECT watcher, message, sent_time FROM audience_comment"
        " WHERE streamer = (?)",
        (streamer,),
    ).fetchall()

    ret_list = []
    if res:
        for row in res:
            ret_list.append(row[2] + " " + row[0] + ": " + row[1])
        return ret_list
    else:
        return None

def insert_advertise(streamer, category, valid_until, image):
    
    if streamer is not None:
        db = get_db()
        db.execute(
            "INSERT INTO advertise (streamer, category, valid_until, image)"
            " VALUES (?,?,?,?)",
            (streamer, category, valid_until, image),
        )
    
        db.commit()
    else:
        pass
    
    
def get_advertise(streamer = None):
    db = get_db()
    
    if streamer:
        res = db.execute(
            "SELECT image, valid_until FROM advertise"
            " WHERE streamer = (?)",
            (streamer,),
        ).fetchall()
        ret_list = []
        if res:
            for row in res:
                if row[1] > datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]:
                    ret_list.append(row[0])

        if ret_list:
            return ret_list
        else:
            res =  db.execute(
                "SELECT category FROM streaming"
                " WHERE id = (?)",
                (streamer,),
            ).fetchone()
    
            if res == None:
                return []
            category = res[0]

            res = db.execute(
                "SELECT image, valid_until FROM advertise"
                " WHERE category = (?)",
                (category,),
            ).fetchall()

            if res:
                for row in res:
                    if row[1] > datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]:
                        ret_list.append(row[0])
            return ret_list
    
    return []

