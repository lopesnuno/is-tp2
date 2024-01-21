import os.path
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from .csv_reader import CSVReader
from .entities.college import College
from .entities.country import Country
from .entities.player import Player
from .entities.season import Season
from .entities.stats import Stats
from .entities.team import Team


class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):

        players = self._reader.read_entities(
            attrs=["player_name", "season"],
            builder=lambda row: Player(
                name=row["player_name"],
                age=row["age"],
                height=row["player_height"],
                weight=row["player_weight"],
                college=row["college"],
                country=row["country"],
                draft_year=row["draft_year"],
                draft_round=row["draft_round"],
                draft_number=row["draft_number"],
                season=row["season"]
            )
        )

        stats = self._reader.read_entities(
            attrs=["player_name", "team_abbreviation", "season"],
            builder=lambda row: Stats(
                gp=row["gp"],
                pts=row["pts"],
                reb=row["reb"],
                ast=row["ast"],
                net_rating=row["net_rating"],
                oreb_pct=row["oreb_pct"],
                dreb_pct=row["dreb_pct"],
                usg_pct=row["usg_pct"],
                ts_pct=row["ts_pct"],
                ast_pct=row["ast_pct"],
                season=row["season"],
                player=row["player_name"]
            )
        )

        root_el = ET.Element("NBA")

        players_by_season = {}
        for player in players.values():
            season = player.get_season()
            if season not in players_by_season:
                players_by_season[season] = []
            players_by_season[season].append(player)

        for season, season_players in players_by_season.items():
            season_el = ET.SubElement(root_el, "Season")
            season_el.set('season', season)

            for player in season_players:
                player_el = ET.Element("Player")
                player_el.set('id', str(player.get_id()))
                player_el.set('name', str(player._name))

                ET.SubElement(player_el, "name").text = player._name
                ET.SubElement(player_el, 'country').text = player.get_country()
                ET.SubElement(player_el, "age").text = str(player._age)
                ET.SubElement(player_el, "height").text = str(player._height)
                ET.SubElement(player_el, "weight").text = str(player._weight)
                ET.SubElement(player_el, "draft_year").text = player._draft_year
                ET.SubElement(player_el, "draft_round").text = player._draft_round
                ET.SubElement(player_el, 'college').text = player.get_college()
                ET.SubElement(player_el, "draft_number").text = player._draft_number
                ET.SubElement(player_el, "season").text = player.get_season()

                for stat in stats.values():
                    if stat._player == player._name:
                        if stat._season == player.get_season():
                            stat_el = ET.Element("Stats")
                            ET.SubElement(stat_el, "gp").text = str(stat._gp)
                            ET.SubElement(stat_el, "pts").text = str(stat._pts)
                            ET.SubElement(stat_el, "reb").text = str(stat._reb)
                            ET.SubElement(stat_el, "ast").text = str(stat._ast)
                            ET.SubElement(stat_el, "net_rating").text = str(stat._net_rating)
                            ET.SubElement(stat_el, "oreb_pct").text = str(stat._oreb_pct)
                            ET.SubElement(stat_el, "dreb_pct").text = str(stat._dreb_pct)
                            ET.SubElement(stat_el, "usg_pct").text = str(stat._usg_pct)
                            ET.SubElement(stat_el, "ts_pct").text = str(stat._ts_pct)
                            ET.SubElement(stat_el, "ast_pct").text = str(stat._ast_pct)

                            player_el.append(stat_el)

                season_el.append(player_el)

        assert len(root_el) == len(players_by_season), "Extra content found after root element"

        return root_el

    def to_xml_str(self):
        root_el = self.to_xml()

        try:
            # Convert the XML element to a string
            xml_str = ET.tostring(root_el, encoding='utf8', method='xml').decode()
            dom = md.parseString(xml_str)
            pretty_xml_str = dom.toprettyxml()

            # Save as a file
            file_path = os.path.join('/data', 'allSeasons.xml')
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(pretty_xml_str)

            print("File 'allSeasons.xml' created successfully!")
            return pretty_xml_str
        except Exception as e:
            print(f"Failed to create file: {e}")
            return "Failed"



