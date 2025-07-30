import fei_ws.config as config
from datetime import datetime, date
import time
import re

NAME_REGEX = re.compile(r"([A-Za-z']\.|\b[A-Za-z']{1,3}\b|'[tT])", re.UNICODE)
ROMAN_REGEX = re.compile(r'\bM{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$', re.IGNORECASE)


def normalize_name(value, roman_numerals=False):
    def _transform(match):
        word = match.group()
        if len(word) == 2 and word[1] == '.':  # If word is a letter followed by a .(dot) Then use capitals
            return word.upper()
        if word.lower() in config.FEI_WS_LOWER_CASE_WORDS:
            return word.lower()
        if word.upper() in config.FEI_WS_UPPER_CASE_ACRONYMS:
            return word.upper()
        return word

    if not value or not isinstance(value, str):
        return value
    value = value.title()
    value = NAME_REGEX.sub(_transform, value)
    if roman_numerals:
        value = ROMAN_REGEX.sub(
            lambda match: match.group().upper() if match.group() else match.group(), value)
    return value[0].upper() + value[1:]


def parse_xml_date(value):
    if not value:
        return None
    try:
        return date(*(time.strptime(value, '%Y-%m-%d')[0:3]))
    except ValueError:
        return None


def parse_xml_datetime(value):
    if not value:
        return None
    try:
        return datetime(*(time.strptime(value, '%Y-%m-%d %H:%M:%S')[0:6]))
    except ValueError:
        return None


def create_dict_from_xml(el):
    if el is None:
        return {}
    result = {}
    for key, value in el.items():
        if re.match(r'^(19[0-9]{2}|2[0-9]{3})-(0[1-9]|1[012])-([123]0|[012][1-9]|31)$', value):
            result[key] = parse_xml_date(value)
        elif re.match(
                r'^(19[0-9]{2}|2[0-9]{3})-(0[1-9]|1[012])-([123]0|[012][1-9]|31) [0-2][0-9]:[0-6][0-9]:[0-6][0-9]$',
                value):
            result[key] = parse_xml_datetime(value)
        elif re.match(r'^\d+$', value):
            result[key] = int(value)
        elif value == 'true':
            result[key] = True
        elif value == 'false':
            result[key] = False
        else:
            result[key] = value
    return result


