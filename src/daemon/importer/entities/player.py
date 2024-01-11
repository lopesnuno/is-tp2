import xml.etree.ElementTree as ET


class Player:

    # gp, pts, reb, ast, net_rating, oreb_pct,dreb_pct,usg_pct,ts_pct,ast_pct,season
    #,player_name,team_abbreviation,age,player_height,player_weight,college,country,draft_year,draft_round,draft_number,gp,pts,reb,ast,net_rating,oreb_pct,dreb_pct,usg_pct,ts_pct,ast_pct,season
    def __init__(self, name, age, height, weight, college, country, draft_year, draft_round, draft_number, season):
        Player.counter += 1
        self._id = Player.counter
        self._name = name
        self._height = height
        self._weight = weight
        self._college = college
        self._draft_year = draft_year
        self._draft_round = draft_round
        self._draft_number = draft_number
        self._age = age
        self._country = country
        self._season = season

    def to_xml(self):
        el = ET.Element("Player")
        el.set("id", str(self._id))
        el.set("name", self._name)
        el.set("age", self._age)
        el.set("country_ref", str(self._country))
        el.set("height", str(self._height))
        el.set("weight", str(self._weight))
        el.set("college_ref", str(self._college))
        el.set("draft_year", str(self._draft_year))
        el.set("draft_round", str(self._draft_round))
        el.set("draft_number", str(self._draft_number))
        el.set("season", str(self._season))
        return el

    def get_id(self):
        return self._id

    def get_college(self):
        return self._college

    def get_country(self):
        return self._country

    def get_season(self):
        return self._season

    def __str__(self):
        return f"{self._name}, age:{self._age}, country:{self._country}"


Player.counter = 0
