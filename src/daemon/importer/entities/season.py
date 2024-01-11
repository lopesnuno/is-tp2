import xml.etree.ElementTree as ET


class Season:
    def __init__(self, year):
        Season.counter += 1
        self._id = Season.counter
        self._year = year

    def to_xml(self):
        el = ET.Element("Season")
        el.set("id", str(self._id))
        el.set("year", str(self._year))
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._year}, id: {self._id}"


Season.counter = 0
