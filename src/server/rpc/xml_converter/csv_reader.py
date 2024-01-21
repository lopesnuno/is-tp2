from csv import DictReader


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
