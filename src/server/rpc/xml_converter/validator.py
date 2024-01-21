from xmlschema import XMLSchema


def validate(file):
    schema = XMLSchema('/data/validator.xsd')
    try:
        schema.validate(file)
    except Exception as e:
        raise Exception(e)
