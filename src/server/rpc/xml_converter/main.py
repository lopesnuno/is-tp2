from csv_to_xml_converter import CSVtoXMLConverter

if __name__ == "__main__":
    converter = CSVtoXMLConverter("/data/all_seasons.csv")
    print(converter.to_xml_str())
