from xml_converter.csv_to_xml_converter import CSVtoXMLConverter
from xml_converter.validator import validate
from database import database
import xml.etree.ElementTree as ET
import os


def import_csv(path, db_file_name):
    try:
        xml_file = CSVtoXMLConverter(path)
        xml_to_str = xml_file.to_xml_str()

        try:
            valid = validate(xml_to_str)
            if valid:
                file_path = os.path.join('/data', 'allSeasons.xml')
                result = database.storeFile(file_path, db_file_name)
                return result
        except ET.ParseError as validation_error:
            print(f"Ignoring validation error: {validation_error}")
            file = os.path.join('/data', 'allSeasons.xml')
            result = database.storeFile(file, db_file_name)
            return result

    except ET.ParseError as parse_error:
        print(f"Ignoring parsing error: {parse_error}")
        file = os.path.join('/data', 'allSeasons.xml')
        result = database.storeFile(file, db_file_name)
        return result

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Handle other unexpected errors
        return f"An unexpected error occurred: {e}"


