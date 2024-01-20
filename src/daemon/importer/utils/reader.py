from csv import DictReader, DictWriter
import os

class CSVReader:

    def __init__(self, path, delimiter=','):
        self._path = path
        self._delimiter = delimiter

    def loop(self):
        with open(self._path, 'r') as file:
            for row in DictReader(file, delimiter=self._delimiter):
                yield row
        file.close()

    def read_entities(self, attrs: list, builder, after_create=None):
        entities = {}
        for row in self.loop():
            e = tuple(row[attr] for attr in attrs)
            if e not in entities:
                entities[e] = builder(row)
                if after_create is not None:
                    if e in entities:
                        after_create(entities[e], row)
                    else:
                        print(f"Key {e} does not exist in the dictionary.")
        return entities

    def split_files(self, output_prefix):
        output_dir = '/csv'
        file_handles = [open(os.path.join(output_dir, f"{output_prefix}_{i}.csv"), 'w', newline='') for i in range(4)]
        writers = [DictWriter(file_handle, fieldnames=self.get_fieldnames()) for file_handle in file_handles]

        for writer in writers:
            writer.writeheader()

        for i, row in enumerate(self.loop()):
            file_index = i % 4
            writers[file_index].writerow(row)

        for file_handle in file_handles:
            file_handle.close()

    def get_fieldnames(self):
        with open(self._path, 'r') as file:
            reader = DictReader(file, delimiter=self._delimiter)
            fieldnames = reader.fieldnames

        return fieldnames
