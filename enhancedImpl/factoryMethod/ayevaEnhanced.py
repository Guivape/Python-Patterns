import json
import xml.etree.ElementTree as etree
import os

class DataExtractorMeta(type):
    REGISTRY = {}
    def __init__(cls, name, bases, clsdict):
        super().__init__(name, bases, clsdict)
        ext = getattr(cls, 'EXTENSION', None)
        if ext:
            DataExtractorMeta.REGISTRY[ext] = cls

def get_extractor_class(ext):
    return DataExtractorMeta.REGISTRY.get(ext, None)

class BaseDataExtractor(metaclass=DataExtractorMeta):
    EXTENSION = None
    def __init__(self, filepath):
        self.filepath = filepath
    @property
    def parsed_data(self):
        raise NotImplementedError

class JSONDataExtractor(BaseDataExtractor):
    EXTENSION = 'json'
    def __init__(self, filepath):
        super().__init__(filepath)
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    @property
    def parsed_data(self):
        return self.data

class XMLDataExtractor(BaseDataExtractor):
    EXTENSION = 'xml'
    def __init__(self, filepath):
        super().__init__(filepath)
        self.tree = etree.parse(self.filepath)
    @property
    def parsed_data(self):
        return self.tree

def dataextraction_factory(filepath):
    _, ext = os.path.splitext(filepath)
    extractor_cls = get_extractor_class(ext.lower().lstrip('.'))
    if not extractor_cls:
        raise ValueError(f"Cannot extract data from extension: {ext}")
    return extractor_cls(filepath)

def extract_data_from(filepath):
    try:
        return dataextraction_factory(filepath)
    except ValueError as e:
        print(e)
        return None

def main():
    sqlite_factory = extract_data_from('data/person.sq3')
    print()

    json_factory = extract_data_from('data/movies.json')
    if json_factory:
        json_data = json_factory.parsed_data
        print(f'Found: {len(json_data)} movies')
        for m in json_data:
            print(f"Title: {m['title']}")
            if m.get('year'): print(f"Year: {m['year']}")
            if m.get('director'): print(f"Director: {m['director']}")
            if m.get('genre'): print(f"Genre: {m['genre']}")
            print()

    xml_factory = extract_data_from('data/person.xml')
    if xml_factory:
        liars = xml_factory.parsed_data.findall(".//person[lastName='Liar']")
        print(f'found: {len(liars)} persons')
        for l in liars:
            print(f"first name: {l.find('firstName').text}")
            print(f"last name: {l.find('lastName').text}")
            for p in l.find('phoneNumbers'):
                print(f"phone number ({p.attrib.get('type','N/A')}): {p.text}")
            print()

if __name__ == '__main__':
    main()
