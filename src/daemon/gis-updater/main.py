import sys
import os
import time
import xml.etree.ElementTree as ET
from geopy.geocoders import Nominatim

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60
ENTITIES_PER_ITERATION = int(sys.argv[2]) if len(sys.argv) >= 3 else 10
XML_PATH = "/xml"


def get_colleges(xml_path, iterations=None):
    college_names = set()
    iterations = 0
    for file in os.listdir(xml_path):
        if file.endswith(".xml"):
            file_path = os.path.join(xml_path, file)

            tree = ET.parse(file_path)
            root = tree.getroot()

            elements = root.findall(".//College")
            for el in elements:
                name = el.find("name").text.strip()
                college_names.add(name)

    return list(college_names)


if __name__ == "__main__":

    while True:
        print(f"Getting up to {ENTITIES_PER_ITERATION} entities without coordinates...")
        # !TODO: 1- Use api-gis to retrieve a fixed amount of entities without coordinates (e.g. 100 entities per iteration, use ENTITIES_PER_ITERATION)
        colleges = get_colleges(XML_PATH)
        # !TODO: 2- Use the entity information to retrieve coordinates from an external API
        # !TODO: 3- Submit the changes
        # time.sleep(POLLING_FREQ)
        print(colleges)

