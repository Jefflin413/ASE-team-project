CREATE TABLE user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT,
  usertype TEXT NOT NULL
);

CREATE TABLE watch_history (
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
  FOREIGN KEY (id) REFERENCES user(id)
);

INSERT INTO user (id, name, email, usertype)
VALUES( 'test1', 'test1' , 'test1@test', 'Personal');

INSERT INTO user (id, name, email, usertype)
VALUES( 'test2', 'test2' , 'test2@test', 'Personal');

INSERT INTO user (id, name, email, usertype)
VALUES( 'test3', 'test3' , 'test3@test', 'Personal');

INSERT INTO user (id, name, email, usertype)
VALUES( 'company1', 'company1' , 'company1@test', 'Company');

INSERT INTO streaming (id, name, category)
VALUES( 'test1', 'test_stream1' , 'Gaming');

INSERT INTO streaming (id, name, category)
VALUES( 'test2', 'test_stream2' , 'Life');

INSERT INTO streaming (id, name, category)
VALUES( 'test3', 'test_stream3' , 'Sports');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'nonuser', 'test1', 'Gaming', '2020/11/30');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'nonuser', 'test1', 'Gaming', '2020/11/30');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'nonuser', 'test1', 'Gaming', '2020/11/20');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'nonuser', 'test1', 'Gaming', '2020/11/20');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'nonuser', 'test1', 'Gaming', '2020/11/28');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'nonuser', 'test1', 'Gaming', '2020/11/29');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'test1', 'test2', 'Life', '2020/11/30');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'test2', 'test3', 'Life', '2020/11/29');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'test1', 'test2', 'Life', '2020/11/28');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'test2', 'test3', 'Life', '2020/11/20');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'nonuser', 'test3', 'Sports', '2020/11/11');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'nonuser', 'test3', 'Sports', '2020/11/12');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'nonuser', 'test3', 'Sports', '2020/11/20');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'nonuser', 'test3', 'Sports', '2020/11/20');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'nonuser', 'test3', 'Sports', '2020/11/20');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'nonuser', 'test3', 'Sports', '2020/11/20');

INSERT INTO watch_history (watcher, streamer, category, start_time)
VALUES( 'nonuser', 'test3', 'Sports', '2020/11/30');
