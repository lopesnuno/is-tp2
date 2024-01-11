import xml.etree.ElementTree as ET
from .player import Player
from .season import Season


class Stats:

    # gp, pts, reb, ast, net_rating, oreb_pct,dreb_pct,usg_pct,ts_pct,ast_pct,season
    def __init__(self, gp, pts, reb, ast, net_rating, oreb_pct, dreb_pct, usg_pct, ts_pct, ast_pct, season, player):
        Stats.counter += 1
        self._id = Stats.counter
        self._gp = gp
        self._pts = pts
        self._reb = reb
        self._ast = ast
        self._net_rating = net_rating
        self._oreb_pct = oreb_pct
        self._dreb_pct = dreb_pct
        self._usg_pct = usg_pct
        self._ts_pct = ts_pct
        self._ast_pct = ast_pct
        self._season = season
        self._player = player

    def to_xml(self):
        el = ET.Element("Stats")
        el.set("id", str(self._id))
        el.set("gp", str(self._gp))
        el.set("pts", str(self._pts))
        el.set("reb", str(self._reb))
        el.set("ast", str(self._ast))
        el.set("net_rating", str(self._net_rating))
        el.set("oreb_pct", str(self._oreb_pct))
        el.set("dreb_pct", str(self._dreb_pct))
        el.set("usg_pct", str(self._usg_pct))
        el.set("ts_pct", str(self._ts_pct))
        el.set("ast_pct", str(self._ast_pct))
        el.set("season", str(self._season))
        el.set("player_name", str(self._player))
        return el

    def get_id(self):
        return self._id

    def add_player(self, player: Player, season: Season):
        self.append(player, season)


Stats.counter = 0
