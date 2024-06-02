import json

DOC_URL = "https://scim2-cli.readthedocs.io/"
INDENTATION_SIZE = 4


def formatted_payload(obj, indent):
    indent = INDENTATION_SIZE if indent else False
    return json.dumps(obj, indent=indent)
