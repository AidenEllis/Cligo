from jinja2.filters import FILTERS
from jinja2 import Template
from cligo.output.colors import colorFilter


def outputData(template: str, string_format=False):
    if string_format:
        template = str(str(template).replace("{", "{{")).replace("}", "}}")

    FILTERS["color"] = colorFilter

    return Template(template).render()
