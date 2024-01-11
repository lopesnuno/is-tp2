import xml.etree.ElementTree as ET


class Team:

    def __init__(self, abbreviation: str):
        Team.counter += 1
        self._id = Team.counter
        self._abbreviation = abbreviation
        self._players = []

    def to_xml(self):
        el = ET.Element("Team")
        el.set("id", str(self._id))
        el.set("name", self._abbreviation)

        players_el = ET.Element("Players")
        for player in self._players:
            players_el.append(player.to_xml())

        el.append(players_el)

        return el

    def __str__(self):
        return f"{self._abbreviation} ({self._id})"


Team.counter = 0
