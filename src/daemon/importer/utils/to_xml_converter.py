import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from utils.csv_reader import CSVReader
from utils.validator import xml_validator
from entities.country import Country
from entities.team import Team
from entities.player import Player
from entities.college import College
from entities.entry import Entry


class CSVtoXMLConverter:

    def __init__(self, file):
        self._reader = CSVReader(file)

    def to_xml(self):

        # read college
        colleges = self._reader.read_entities(
            attrs=["college"],
            builder=lambda row: College(row["college"]),
            is_valid=lambda row: (str(row["college"])).strip() not in ['None', '', ' ', 'No College']
        )

        # read countries
        countries = self._reader.read_entities(
            attrs=["country"],
            builder=lambda row: Country(row["country"]),
        )

        # read teams
        teams = self._reader.read_entities(
            attrs=["team_abbreviation"],
            builder=lambda row: Team(row["team_abbreviation"])
        )

        # read players
        players = self._reader.read_entities(
            attrs=["player_name"],
            builder=lambda row: Player(
                name=row["player_name"],
                age=row["age"],
                height=row["player_height"],
                weight=row["player_weight"],
                draft_year=row["draft_year"],
                draft_round=row["draft_round"],
                draft_number=row["draft_number"],
                country=row["country"],
                college=row["college"]
            )
        )

        # read entry
        entries = self._reader.read_entities(
            attrs=["player_name", "team_abbreviation", "season"],
            builder=lambda row: Entry(
                season=row["season"],
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
                player=row["player_name"],
                team=row["team_abbreviation"]
            )
        )

        # generate the final xml
        root_el = ET.Element("NBAData")

        players_el = ET.Element("players")
        for player in players.values():
            players_el.append(player.to_xml())

        teams_el = ET.Element("teams")
        for team in teams.values():
            teams_el.append(team.to_xml())

        countries_el = ET.Element("countries")
        for country in countries.values():
            countries_el.append(country.to_xml())

        colleges_el = ET.Element("colleges")
        for college in colleges.values():
            colleges_el.append(college.to_xml())

        entries_el = ET.Element("entries")
        for entry in entries.values():
            entries_el.append(entry.to_xml())

        root_el.append(players_el)
        root_el.append(teams_el)
        root_el.append(countries_el)
        root_el.append(colleges_el)
        root_el.append(entries_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        final_xml = dom.toprettyxml()

        try:
            xml_validator(final_xml)

            return final_xml

        except Exception as e:
            raise Exception(f'Error while validating XML: {e}')