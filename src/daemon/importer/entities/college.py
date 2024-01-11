import xml.etree.ElementTree as ET


class College:
    def __init__(self, name):
        College.counter += 1
        self._id = College.counter
        self._name = name

    def to_xml(self):
        el = ET.Element("College")
        el.set("id", str(self._id))
        el.set("name", self._name)
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id: {self._id}"


College.counter = 0
