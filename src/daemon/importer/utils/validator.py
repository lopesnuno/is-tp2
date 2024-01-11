from xmlschema import XMLSchema


def xml_validator(xml):
    # Load XML Schema
    schema = XMLSchema('utils/xsd/validator.xsd')

    if not schema:
        raise Exception('No schema found!')

    try:
        schema.validate(xml)
    except Exception as e:
        raise Exception(e)

