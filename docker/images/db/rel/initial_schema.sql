CREATE TABLE teams
(
    id           INTEGER PRIMARY KEY,
    abbreviation VARCHAR(4) NOT NULL
);

CREATE TABLE countries
(
    id   INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE colleges
(
    id   INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE players
(
    id           INTEGER PRIMARY KEY,
    name         VARCHAR(100)                      NOT NULL,
    age          INTEGER                           NOT NULL,
    height       FLOAT                             NOT NULL,
    weight       FLOAT                             NOT NULL,
    draft_year   INT                               NOT NULL,
    draft_round  INT                               NOT NULL,
    draft_number INT                               NOT NULL,
    college_ref  INTEGER REFERENCES colleges (id),
    country_ref  INTEGER REFERENCES countries (id) NOT NULL
);

CREATE TABLE entries
(
    id         INTEGER PRIMARY KEY,
    season     VARCHAR(8)                      NOT NULL,
    gp         INTEGER                         NOT NULL,
    pts        FLOAT                           NOT NULL,
    reb        FLOAT                           NOT NULL,
    ast        FLOAT                           NOT NULL,
    net_rating FLOAT                           NOT NULL,
    oreb_pct   FLOAT                           NOT NULL,
    dreb_pct   FLOAT                           NOT NULL,
    usg_pct    FLOAT                           NOT NULL,
    ts_pct     FLOAT                           NOT NULL,
    ast_pct    FLOAT                           NOT NULL,
    player_ref INTEGER REFERENCES players (id) NOT NULL,
    team_ref   INTEGER REFERENCES teams (id)   NOT NULL
);
