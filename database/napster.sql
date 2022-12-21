CREATe DATABASE napster;

CREATE TABLE IF NOT EXISTS UserList (
    nickname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    public_key VARCHAR(64),
    UNIQUE (nickname),
    PRIMARY KEY (nickname)
);

CREATE TABLE IF NOT EXISTS Content (
    distro VARCHAR(255) NOT NULL,
    version VARCHAR(255) NOT NULL,
    arch VARCHAR(255) NOT NULL,
    MD5 VARCHAR(32) NOT NULL,
    size INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    nickname VARCHAR(255) NOT NULL,
    PRIMARY KEY (distro),
    FOREIGN KEY (nickname) REFERENCES UserList(nickname)
);

CREATE TABLE Network (
    ip VARCHAR(15) NOT NULL,
    port INT NOT NULL,
    nickname VARCHAR(255) NOT NULL,
    PRIMARY KEY (ip, port),
    FOREIGN KEY (nickname) REFERENCES UserList(nickname)
);

CREATE TABLE Stats (
    last_login INT NOT NULL,
    mean_st FLOAT,
    min_st FLOAT,
    max_st FLOAT,
    std_st FLOAT,
    nickname VARCHAR(255) NOT NULL
);

INSERT INTO UserList (nickname, email) VALUES ('jesus',  '2153068058@cua.uam.mx');
INSERT INTO UserList (nickname, email) VALUES ('alex',   '2153068307@cua.uam.mx');
INSERT INTO UserList (nickname, email) VALUES ('mario',  '2183034471@cua.uam.mx');
INSERT INTO UserList (nickname, email) VALUES ('oscar',  '2173071702@cua.uam.mx');
INSERT INTO UserList (nickname, email) VALUES ('uriel',  '2143067227@cua.uam.mx');
INSERT INTO UserList (nickname, email) VALUES ('keveen', '2173071766@cua.uam.mx');