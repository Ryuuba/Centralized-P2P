CREATE TABLE IF NOT EXISTS users (
    nickname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    public_key VARCHAR(64),
    last_login INT
);

CREATE TABLE IF NOT EXISTS content (
    nickname VARCHAR(255) NOT NULL,
    distro VARCHAR(255) NOT NULL,
    ver VARCHAR(255) NOT NULL,
    arch VARCHAR(255) NOT NULL,
    MD5 VARCHAR(32) NOT NULL,
    size INT
);

INSERT INTO users (nickname, email) VALUES ('jesus',  '2153068058@cua.uam.mx');
INSERT INTO users (nickname, email) VALUES ('alex',   '2153068307@cua.uam.mx');
INSERT INTO users (nickname, email) VALUES ('mario',  '2183034471@cua.uam.mx');
INSERT INTO users (nickname, email) VALUES ('oscar',  '2173071702@cua.uam.mx');
INSERT INTO users (nickname, email) VALUES ('uriel',  '2143067227@cua.uam.mx');
INSERT INTO users (nickname, email) VALUES ('keveen', '2173071766@cua.uam.mx');