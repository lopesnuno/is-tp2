CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

CREATE TABLE public.teams (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name            VARCHAR(250) NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.college (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name            VARCHAR(250) NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.countries (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name            VARCHAR(250) UNIQUE NOT NULL,
	geom            GEOMETRY,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.players (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name            VARCHAR(250) NOT NULL,
	age             INT NOT NULL,
	team_id         uuid,
	country_id      uuid NOT NULL,
    college_id      uuid,
    height          INT NOT NULL,
    weight          INT NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.draft (
    id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    year            INT NOT NULL,
    round           INT NOT NULL,
    number          INT NOT NULL,
    player_id       uuid NOT NULL
)

CREATE TABLE public.seasons (
    id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    year            varchar(50) NOT NULL UNIQUE,
)

CREATE TABLE public.season_player (
    id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    season_id          uuid NOT NULL,
    player_id          uuid NOT NULL
)

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
    ast_pct         FLOAT,
)


ALTER TABLE players
    ADD CONSTRAINT players_countries_id_fk
        FOREIGN KEY (country_id) REFERENCES countries
            ON DELETE CASCADE;

ALTER TABLE players
    ADD CONSTRAINT players_teams_id_fk
        FOREIGN KEY (team_id) REFERENCES teams
            ON DELETE SET NULL;

ALTER TABLE players
    ADD CONSTRAINT players_college_id_fk
        FOREIGN KEY (college_id) REFERENCES colleges
            ON DELETE SET NULL;

ALTER TABLE draft
    ADD CONSTRAINT draft_player_id_fk
        FOREIGN KEY (player_id) REFERENCES players
            ON DELETE SET NULL;

ALTER TABLE season_player
    ADD CONSTRAINT season_player_fk
        FOREIGN KEY (player_id) REFERENCES players
            ON DELETE SET NULL;

ALTER TABLE season_player
    ADD CONSTRAINT season_player_fk
        FOREIGN KEY (season_id) REFERENCES seasons
            ON DELETE SET NULL;

ALTER TABLE stats
    ADD CONSTRAINT stats_season_player_id_fk
        FOREIGN KEY (id) REFERENCES season_player
            ON DELETE SET NULL;


