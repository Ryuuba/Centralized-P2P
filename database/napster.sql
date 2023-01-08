CREATE DATABASE napster;

use napster;

CREATE TABLE IF NOT EXISTS tblUser (
    nickname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (nickname)
);

CREATE TABLE IF NOT EXISTS tblContent (
    distro VARCHAR(255) NOT NULL,
    version VARCHAR(255) NOT NULL,
    arch VARCHAR(255) NOT NULL,
    SHA256 VARCHAR(64) NOT NULL,
    size BIGINT NOT NULL,
    target VARCHAR(255) NOT NULL,
    PRIMARY KEY (SHA256)
);

CREATE TABLE IF NOT EXISTS tblUserContent (
    nickname VARCHAR(255) NOT NULL,
    SHA256 VARCHAR(64) NOT NULL,
    url VARCHAR(255) NOT NULL,
    FOREIGN KEY (nickname) REFERENCES tblUser(nickname),
    FOREIGN KEY (SHA256) REFERENCES tblContent(SHA256),
    UNIQUE(nickname, SHA256)
);

CREATE TABLE tblUserNetworkData (
    ip VARCHAR(15) NOT NULL,
    port INT NOT NULL,
    nickname VARCHAR(255) NOT NULL,
    FOREIGN KEY (nickname) REFERENCES tblUser (nickname)
);

INSERT INTO tblUser (nickname, email, password) VALUES ('jesus',  '2153068058@cua.uam.mx', 'jesus0000');
INSERT INTO tblUser (nickname, email, password) VALUES ('alex',   '2153068307@cua.uam.mx', 'alex0000');
INSERT INTO tblUser (nickname, email, password) VALUES ('mario',  '2183034471@cua.uam.mx', 'mario0000');
INSERT INTO tblUser (nickname, email, password) VALUES ('oscar',  '2173071702@cua.uam.mx', 'oscar0000');
INSERT INTO tblUser (nickname, email, password) VALUES ('uriel',  '2143067227@cua.uam.mx', 'uriel0000');
INSERT INTO tblUser (nickname, email, password) VALUES ('keveen', '2173071766@cua.uam.mx', 'keveen0000');
INSERT INTO tblUser (nickname, email, password) VALUES ('geo', 'agmedrano@cua.uam.mx', 'geo0000');