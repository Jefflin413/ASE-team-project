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
  start_time TIMESTAMP,
  end_time TIMESTAMP,
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
VALUES( 'test1', 'test1' , 'test1@test', 'streamer');

INSERT INTO user (id, name, email, usertype)
VALUES( 'test2', 'test2' , 'test2@test', 'streamer');

INSERT INTO user (id, name, email, usertype)
VALUES( 'test3', 'test3' , 'test3@test', 'streamer');

INSERT INTO user (id, name, email, usertype)
VALUES( 'company1', 'company1' , 'company1@test', 'company');

INSERT INTO streaming (id, name, category)
VALUES( 'test1', 'test_stream1' , 'Gaming');

INSERT INTO streaming (id, name, category)
VALUES( 'test2', 'test_stream2' , 'Life');

INSERT INTO streaming (id, name, category)
VALUES( 'test3', 'test_stream3' , 'Sports');

INSERT INTO watch_history (watcher, streamer, category)
VALUES( 'nonuser', 'test_stream1', 'Gaming');

INSERT INTO watch_history (watcher, streamer, category)
VALUES( 'nonuser', 'test_stream1', 'Gaming');

INSERT INTO watch_history (watcher, streamer, category)
VALUES( 'test1', 'test_stream2', 'Life');

INSERT INTO watch_history (watcher, streamer, category)
VALUES( 'test2', 'test_stream3', 'Life');

INSERT INTO watch_history (watcher, streamer, category)
VALUES( 'nonuser', 'test_stream3', 'Sports');
