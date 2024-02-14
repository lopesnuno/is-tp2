import asyncio
import time
import uuid
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from utils.database import storeFile_imported_documents, storeFile_converted_documents, get_db_converted_files
from utils.to_xml_converter import CSVtoXMLConverter
from utils.reader import CSVReader
import csv


def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']


def generate_unique_file_name(directory):
    return f"{directory}/{str(uuid.uuid4())}.xml"


def convert_csv_to_xml(in_path, out_path):
    converter = CSVtoXMLConverter(in_path)
    file = open(out_path, "w")
    file.write(converter.to_xml_str())


class CSVHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        self._output_path = output_path
        self._input_path = input_path

        # generate file creation events for existing files
        for file in [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames]:
            event = FileCreatedEvent(os.path.join(CSV_INPUT_PATH, file))
            event.event_type = "created"
            self.dispatch(event)

    async def convert_csv(self, csv_path, chunk_size=4000):
        # here we avoid converting the same file again
        # !TODO: check converted files in the database
        if csv_path in await self.get_converted_files():
            return "File already converted."

        print(f"new file to convert: '{csv_path}'")

        reader = CSVReader(csv_path)
        reader.split_files('out_split')

        while True:
            split_csv_files = [f for f in os.listdir('/csv') if f.startswith('out_split_') and f.endswith('.csv')]

            if not split_csv_files:
                print("Waiting for more files...")
                time.sleep(5)
                continue

            for split_csv_file in split_csv_files:
                split_csv_path = os.path.join('/csv', split_csv_file)
                if os.path.exists(split_csv_path):
                    xml_path = generate_unique_file_name(self._output_path)

                    convert_csv_to_xml(split_csv_path, xml_path)

                    storeFile_converted_documents(split_csv_path, xml_path)
                    print(f"new xml file generated: '{xml_path}'")
                    storeFile_imported_documents(file_path=xml_path)

                    os.remove(split_csv_path)
                    print(f"split csv file deleted: '{split_csv_path}'")


    async def get_converted_files(self):
        return get_db_converted_files()

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            asyncio.run(self.convert_csv(event.src_path))


if __name__ == "__main__":

    CSV_INPUT_PATH = "/csv"
    XML_OUTPUT_PATH = "/xml"

    # create the file observer
    observer = Observer()
    observer.schedule(
        CSVHandler(CSV_INPUT_PATH, XML_OUTPUT_PATH),
        path=CSV_INPUT_PATH,
        recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
