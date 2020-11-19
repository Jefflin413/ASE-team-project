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
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP,
  FOREIGN KEY (streamer) REFERENCES user(id)
);

CREATE TABLE streaming (
  id TEXT NOT NULL,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  FOREIGN KEY (id) REFERENCES user(id)
);

INSERT INTO user (id, name, email, usertype)
VALUES( 'test', 'test' , 'test@test', 'streamer');

INSERT INTO streaming (id, name, category)
VALUES( 'test', 'test_stream' , 'Gaming');



