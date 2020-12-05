CREATE TABLE user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT,
  usertype TEXT NOT NULL
);

CREATE TABLE watch_history (
  UUID TEXT NOT NULL PRIMARY KEY,
  watcher TEXT,
  streamer TEXT NOT NULL,
  category TEXT NOT NULL,
  start_time TEXT,
  end_time TEXT,
  FOREIGN KEY (streamer) REFERENCES user(id)
);

CREATE TABLE streaming (
  id TEXT NOT NULL,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  m3u8_URL TEXT,
  current_watching INTEGER NOT NULL,
  FOREIGN KEY (id) REFERENCES user(id)
);

CREATE TABLE audience_comment(
  watcher TEXT, 
  streamer TEXT, 
  message TEXT, 
  sent_time TEXT, 
  FOREIGN KEY (watcher) REFERENCES user(id),
  FOREIGN KEY (streamer) REFERENCES user(id)
);

CREATE TABLE advertise(
  streamer TEXT, 
  category TEXT, 
  valid_until TEXT, 
  image TEXT
);


INSERT INTO user (id, name, email, usertype)
VALUES( 'test1', 'test1' , 'test1@test', 'Personal');

INSERT INTO user (id, name, email, usertype)
VALUES( 'test2', 'test2' , 'test2@test', 'Personal');

INSERT INTO user (id, name, email, usertype)
VALUES( 'test3', 'test3' , 'test3@test', 'Personal');

INSERT INTO user (id, name, email, usertype)
VALUES( 'company1', 'company1' , 'company1@test', 'Company');

INSERT INTO streaming (id, name, category, current_watching)
VALUES( 'test1', 'test_stream1' , 'Gaming', 0);

INSERT INTO streaming (id, name, category, current_watching)
VALUES( 'test2', 'test_stream2' , 'Life', 0);

INSERT INTO streaming (id, name, category, current_watching)
VALUES( 'test3', 'test_stream3' , 'Sports', 0);

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b907305a-35e7-11eb-9844-0e6eb579fb2b', 'nonuser', 'test1', 'Gaming', '2020-11-30 00:00:00.000', '2020-11-30 01:00:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b90737f8-35e7-11eb-9844-0e6eb579fb2b', 'nonuser', 'test1', 'Gaming', '2020-11-30 02:00:00.000', '2020-11-30 03:00:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b9073a64-35e7-11eb-9844-0e6eb579fb2b', 'nonuser', 'test1', 'Gaming', '2020-11-20 04:00:00.000', '2020-11-20 05:00:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b9073c30-35e7-11eb-9844-0e6eb579fb2b', 'nonuser', 'test1', 'Gaming', '2020-11-20 06:00:00.000', '2020-11-20 07:00:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b9073d2a-35e7-11eb-9844-0e6eb579fb2b', 'nonuser', 'test1', 'Gaming', '2020-11-28 08:00:00.000', '2020-11-28 09:00:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b9073e9c-35e7-11eb-9844-0e6eb579fb2b', 'nonuser', 'test1', 'Gaming', '2020-11-29 10:00:00.000', '2020-11-29 11:00:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b9073fb4-35e7-11eb-9844-0e6eb579fb2b', 'test1', 'test2', 'Life', '2020-11-30 12:00:00.000', '2020-11-30 13:00:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b90740c2-35e7-11eb-9844-0e6eb579fb2b', 'test2', 'test3', 'Life', '2020-11-29 14:00:00.000', '2020-11-29 15:00:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b90741d0-35e7-11eb-9844-0e6eb579fb2b', 'test1', 'test2', 'Life', '2020-11-28 16:00:00.000', '2020-11-28 17:00:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b90742d4-35e7-11eb-9844-0e6eb579fb2b', 'test2', 'test3', 'Life', '2020-11-20 18:00:00.000', '2020-11-20 19:00:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b90743d8-35e7-11eb-9844-0e6eb579fb2b', 'nonuser', 'test3', 'Sports', '2020-11-11 20:00:00.000', '2020-11-11 21:00:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b90744dc-35e7-11eb-9844-0e6eb579fb2b', 'nonuser', 'test3', 'Sports', '2020-11-12 22:00:00.000', '2020-11-12 23:00:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b90745ea-35e7-11eb-9844-0e6eb579fb2b', 'nonuser', 'test3', 'Sports', '2020-11-20 06:00:00.000', '2020-11-20 07:30:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b90746ee-35e7-11eb-9844-0e6eb579fb2b', 'nonuser', 'test3', 'Sports', '2020-11-20 07:00:00.000', '2020-11-20 08:30:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b907481a-35e7-11eb-9844-0e6eb579fb2b', 'nonuser', 'test3', 'Sports', '2020-11-20 08:15:00.000', '2020-11-20 09:45:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b9074932-35e7-11eb-9844-0e6eb579fb2b', 'nonuser', 'test3', 'Sports', '2020-11-20 06:37:00.000', '2020-11-20 10:59:00.000');

INSERT INTO watch_history (UUID, watcher, streamer, category, start_time, end_time)
VALUES( 'b9074a4a-35e7-11eb-9844-0e6eb579fb2b', 'nonuser', 'test3', 'Sports', '2020-11-30 15:25:00.000', '2020-11-30 16:44:27.000');

INSERT INTO audience_comment (watcher, streamer, message, sent_time)
VALUES( 'test1', 'test_stream1' , 'awsome!', '2020-11-30 16:25:00.000');

INSERT INTO audience_comment (watcher, streamer, message, sent_time)
VALUES( 'test2', 'test_stream3' , 'pogchamp', '2020-11-23 09:14:00.000');

INSERT INTO audience_comment (watcher, streamer, message, sent_time)
VALUES( 'test3', 'test_stream1' , 'kappapride', '2020-11-08 23:41:37.000');
