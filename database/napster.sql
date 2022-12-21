CREATE DATABASE napster;

CREATE TABLE IF NOT EXISTS UserList (
    nickname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    public_key VARCHAR(128),
    password VARCHAR(255),
    PRIMARY KEY (nickname)
);

CREATE TABLE IF NOT EXISTS Content (
    distro VARCHAR(255) NOT NULL,
    version VARCHAR(255) NOT NULL,
    arch VARCHAR(255) NOT NULL,
    SHA256 VARCHAR(32) NOT NULL,
    size INT NOT NULL,
    PRIMARY KEY (SHA256)
);

CREATE TABLE IF NOT EXISTS UserContentRelation (
    nickname VARCHAR(255) NOT NULL,
    SHA256 VARCHAR(32) NOT NULL,
    url VARCHAR(255) NOT NULL,
    FOREIGN KEY (nickname) REFERENCES UserList(nickname),
    FOREIGN KEY (SHA256) REFERENCES Content(SHA256),
    UNIQUE(nickname, SHA256)
);

CREATE TABLE Network (
    ip VARCHAR(15) NOT NULL,
    port INT NOT NULL,
    nickname VARCHAR(255) NOT NULL,
    FOREIGN KEY (nickname) REFERENCES UserList(nickname)
);

CREATE TABLE Stats (
    last_login INT,
    mean_st FLOAT,
    min_st FLOAT,
    max_st FLOAT,
    nickname VARCHAR(255) NOT NULL,
    FOREIGN KEY (nickname) REFERENCES UserList(nickname)
);

INSERT INTO UserList (nickname, email, password) VALUES ('jesus',  '2153068058@cua.uam.mx', 'jesus0000');
INSERT INTO UserList (nickname, email, password) VALUES ('alex',   '2153068307@cua.uam.mx', 'alex0000');
INSERT INTO UserList (nickname, email, password) VALUES ('mario',  '2183034471@cua.uam.mx', 'mario0000');
INSERT INTO UserList (nickname, email, password) VALUES ('oscar',  '2173071702@cua.uam.mx', 'oscar0000');
INSERT INTO UserList (nickname, email, password) VALUES ('uriel',  '2143067227@cua.uam.mx', 'uriel0000');
INSERT INTO UserList (nickname, email, password) VALUES ('keveen', '2173071766@cua.uam.mx', 'keveen0000');