CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

CREATE TABLE public.colleges (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name            VARCHAR(250) NOT NULL,
    latitude        DOUBLE PRECISION,
    longitude       DOUBLE PRECISION,
    geom            GEOMETRY(Point, 4326),
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.players (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name            VARCHAR(250) NOT NULL,
	age             INT NOT NULL,
	country         VARCHAR(250),
    college_id      uuid,
    height          INT NOT NULL,
    weight          INT NOT NULL,
    draft_year      INT,
    draft_round     INT,
    draft_number    INT,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.seasons (
    id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    year            varchar(50) NOT NULL UNIQUE
);

CREATE TABLE public.season_player (
    id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    season_id          uuid NOT NULL,
    player_id          uuid NOT NULL
);

CREATE TABLE public.stats (
    id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    season_player   uuid NOT NULL,
    gp              FLOAT,
    pts             FLOAT,
    reb             FLOAT,
    ast             FLOAT,
    net_rating      FLOAT,
    oreb_pct        FLOAT,
    dreb_pct        FLOAT,
    usg_pct         FLOAT,
    ts_pct          FLOAT,
    ast_pct         FLOAT
);


ALTER TABLE players
    ADD CONSTRAINT players_college_id_fk
        FOREIGN KEY (college_id) REFERENCES colleges
            ON DELETE SET NULL;

ALTER TABLE season_player
    ADD CONSTRAINT season_player_fk
        FOREIGN KEY (player_id) REFERENCES players
            ON DELETE SET NULL;

ALTER TABLE season_player
    ADD CONSTRAINT season_player_season_fk
        FOREIGN KEY (season_id) REFERENCES seasons
            ON DELETE SET NULL;

ALTER TABLE stats
    ADD CONSTRAINT stats_season_player_id_fk
        FOREIGN KEY (id) REFERENCES season_player
            ON DELETE SET NULL;


