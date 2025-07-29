import inspect
import re
import json
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Any, Callable, Iterable, Mapping, Protocol, TypeVar, get_args, get_origin

T = TypeVar('T')


class GoogleMoney(Protocol):
    """
    Represents an amount of money with its currency type, as defined by Google.
    
    See https://developers.google.com/actions-center/verticals/things-to-do/reference/feed-spec/google-types?hl=fr#googletypemoney_definition
    """

    currency_code: str
    """ 3-letter currency code defined in ISO 4217. """

    units: int|float
    """ Number of units of the amount (should be integers but float are accepted). """

    nanos: int
    """ Number of nano (10^-9) units of the amount. """

    
def parse_bool(value: bool|str) -> bool:
    if value is None or value == '':
        return None # type: ignore
    elif isinstance(value, bool):
        return value
    elif not isinstance(value, str):
        raise TypeError(f"value: {type(value.__name__)}")

    lower = value.lower()
    # same rules as RawConfigParser.BOOLEAN_STATES
    if lower in {'1', 'yes', 'true', 'on'}:
        return True
    elif lower in {'0', 'no', 'false', 'off'}:
        return False
    else:
        raise ValueError('Not a boolean: %s' % lower)


def parse_datetime(value: datetime|str, *, accept_localized = False) -> datetime:
    if value is None or value == '':
        return None # type: ignore
    elif isinstance(value, datetime):
        return value
    elif isinstance(value, date):
        return datetime(value.year, value.month, value.day)
    elif not isinstance(value, str):
        raise TypeError(f"value: {type(value).__name__}")

    from zut.config import get_lang
    if accept_localized and get_lang() == 'fr_FR':
        m = re.match(r'^(?P<day>[0-9]{1,2})/(?P<month>[0-9]{1,2})/(?P<year>[0-9]{4}) (?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{1,2})(?::(?P<second>[0-9]{1,2}))$', value)
        if m:
            return datetime(int(m['year']), int(m['month']), int(m['day']), int(m['hour']), int(m['minute']), int(m['second']) if m['second'] else 0)

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f %z') # format not accepted by fromisoformat (contrary to other non-ISO but still frequent "%Y-%m-%d %H:%M:%S.%f")


def parse_date(value: date|str, *, accept_localized = False) -> date:
    if value is None or value == '':
        return None # type: ignore
    elif isinstance(value, datetime):
        return value.date()
    elif isinstance(value, date):
        return value
    elif not isinstance(value, str):
        raise TypeError(f"value: {type(value.__name__)}")
    
    if accept_localized:
        from zut.config import get_lang
        if get_lang() == 'fr_FR':
            m = re.match(r'^(?P<day>[0-9]{1,2})/(?P<month>[0-9]{1,2})/(?P<year>[0-9]{4})$', value)
            if m:
                return date(int(m['year']), int(m['month']), int(m['day']))
    
    return date.fromisoformat(value)


def parse_float(value: Decimal|float|int|str|GoogleMoney, *, accept_localized = False) -> float:
    if value is None or value == '':
        return None # type: ignore
    
    if isinstance(value, float):
        return value
    elif isinstance(value, Decimal):
        return float(value)
    elif isinstance(value, int):
        return float(value)
    elif isinstance(value, str):
        if accept_localized:
            from zut.config import get_lang
            if get_lang() == 'fr_FR':
                if re.match(r'^\-?[0-9]{1,3}(?:[ 0-9]{3})*(?:,[0-9]+)?$', value):
                    value = value.replace(' ', '').replace(',', '.')
        return float(value)
    else:
        return float(getattr(value, 'units') + getattr(value, 'nanos') / 1E9)


def parse_decimal(value: Decimal|float|int|str|GoogleMoney, *, decimal_digits: int|None = None, reduce_money = False, accept_localized = False) -> Decimal:
    if value is None or value == '':
        return None # type: ignore
    
    if isinstance(value, Decimal):
        decimal_value = value
    elif isinstance(value, (float,int)):
        decimal_value = Decimal(value)
    elif isinstance(value, str):
        if accept_localized:
            from zut.config import get_lang
            if get_lang() == 'fr_FR':
                if re.match(r'^\-?[0-9]{1,3}(?:[ 0-9]{3})*(?:,[0-9]+)?$', value):
                    value = value.replace(' ', '').replace(',', '.')
        decimal_value = Decimal(value)
    else:
        decimal_value = Decimal(getattr(value, 'units') + getattr(value, 'nanos') / 1E9)
        if decimal_digits is None:
            decimal_digits = 9

    if decimal_digits is not None:
        decimal_value = round(decimal_value, decimal_digits)

    if reduce_money:
        # Reduce to 2 digits if possible
        expo = decimal_value * 100
        remaining = expo - int(expo)
        if remaining == 0:
            return round(decimal_value, 2)
        
        # Reduce to 5 digits if possible
        expo = expo * 1000
        remaining = expo - int(expo)
        if remaining == 0:
            return round(decimal_value, 5)
    
    return decimal_value


def parse_list(value: list|str, *, separator='|') -> list[str]:
    if value is None:
        return None # type: ignore
    elif isinstance(value, list):
        return value
    elif not isinstance(value, str):
        raise TypeError(f"value: {type(value.__name__)}")
    
    value = value.strip()
    if value == '':
        return None # type: ignore

    if value.startswith('{'):
        return parse_postgresql_array_literal(value)
    elif value.startswith('['):
        return json.loads(value)
    else:
        return [element.strip() for element in value.split(separator)]


def parse_dict(value: dict|str|None, *, separator='|') -> dict|None:
    if value is None:
        return None
    elif isinstance(value, dict):
        return value
    elif not isinstance(value, str):
        raise TypeError(f"value: {type(value.__name__)}")
    
    value = value.strip()
    if value == '':
        return None

    if value.startswith('{'):
        return json.loads(value)
    else:
        result = {}
        for element in value.split(separator):
            element = element.strip()
            try:
                pos = element.index('=')
                key = element[:pos].strip()
                value = element[pos+1:].strip()
            except ValueError:
                key = element
                value = None
            result[key] = value
        return result


def parse_func_parameters(func: Callable, *args: str):
    """
    Convert `args` (list of strings typically comming from the command line) into typed args and kwargs for `func`.
    """
    if not args:
        return tuple(), dict()
    
    # Determine argument types
    signature = inspect.signature(func)
    var_positional_type = None
    var_keyword_type = None
    parameter_types = {}
    positional_types = []
    for parameter in signature.parameters.values():
        parameter_type = None if parameter.annotation is inspect.Parameter.empty else parameter.annotation
        if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            var_positional_type = parameter_type
        elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
            var_keyword_type = parameter_type
        else:
            parameter_types[parameter.name] = parameter_type
            if parameter.kind in [inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD]:
                positional_types.append(parameter_type)
    
    # Distinguish args and kwargs
    positionnal_args = []
    keyword_args = {}
    for arg in args:
        m = re.match(r'^([a-z0-9_]+)=(.+)$', arg)
        if m:
            keyword_args[m[1]] = m[2]
        else:
            positionnal_args.append(arg)

    # Convert kwargs
    for parameter, value in keyword_args.items():
        if parameter in parameter_types:
            target_type = parameter_types[parameter]
            if target_type:
                value = convert(value, target_type)
                keyword_args[parameter] = value

        elif var_keyword_type:
            keyword_args[parameter] = convert(value, var_keyword_type)

    # Convert args
    for i, value in enumerate(positionnal_args):
        if i < len(positional_types):
            target_type = positional_types[i]
            if target_type:
                positionnal_args[i] = convert(value, target_type)

        elif var_positional_type:
            positionnal_args[i] = convert(value, var_positional_type)

    return tuple(positionnal_args), keyword_args


def parse_postgresql_array_literal(value: str) -> list[str]:
    """ Parse an array literal (using PostgreSQL syntax) into a list. """
    # See: https://www.postgresql.org/docs/current/arrays.html#ARRAYS-INPUT
    if value is None:
        return None # type: ignore
    
    if not isinstance(value, str):
        raise TypeError(f"value: {type(value.__name__)}")

    if len(value) == 0:
        return None # type: ignore
    elif value[0] != '{' or value[-1] != '}':
        raise ValueError(f"Invalid postgresql array literal '{value}': does not start with '{{' and end with '}}'")
        
    def split(text: str):
        pos = 0

        def get_quoted_part(start_pos: int):
            nonlocal pos
            pos = start_pos
            while True:
                try:
                    next_pos = text.index('"', pos + 1)
                except ValueError:
                    raise ValueError(f"Unclosed quote from position {pos}: {text[pos:]}")
                
                pos = next_pos
                if text[pos - 1] == '\\' and (pos <= 2 or text[pos - 2] != '\\'): # escaped quote
                    pos += 1 # will search next quote
                else:
                    value = text[start_pos+1:pos]
                    pos += 1
                    if pos == len(text): # end
                        pass
                    else:
                        if text[pos] != ',':
                            raise ValueError(f"Quoted part \"{value}\" is followed by \"{text[pos]}\", expected a comma")
                        pos += 1
                    return value

        def get_unquoted_part(start_pos: int):
            nonlocal pos
            try:
                pos = text.index(',', start_pos)
                value = text[start_pos:pos]
                pos += 1
            except ValueError:
                pos = len(text) # end
                value = text[start_pos:]

            if value.lower() == 'null':
                return None
            return value

        def unescape(part: str|None):
            if part is None:
                return part
            return part.replace('\\"', '"').replace('\\\\', '\\')
        
        parts: list[str] = []
        while pos < len(text):
            char = text[pos]
            if char == ',':
                part = ''
                pos += 1
            elif char == '"':
                part = get_quoted_part(pos)
            elif char == '{':
                raise NotImplementedError("Parsing sub arrays is not implemented yet") # ROADMAP
            else:
                part = get_unquoted_part(pos)
            parts.append(unescape(part)) # type: ignore (part not None => result not None)

        return parts

    return split(value[1:-1])


def get_postgresql_array_literal(values: Iterable) -> str:
    """ Parse an Iterable into an array literal (using PostgreSQL syntax). """
    # See: https://www.postgresql.org/docs/current/arrays.html#ARRAYS-INPUT

    if values is None:
        return None
    
    escaped: list[str] = []
    for value in values:
        if value is None:
            value = "null"
        elif isinstance(value, (list,tuple)):
            value = get_postgresql_array_literal(value)
        else:
            if not isinstance(value, str):
                value = str(value)
            if value.lower() == "null":
                value = f'"{value}"'
            elif ',' in value or '"' in value or '\\' in value or '{' in value or '}' in value:
                value = '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
        escaped.append(value)

    return '{' + ','.join(escaped) + '}'


def get_visual_iterable_literal(values: Iterable, *, separator = '|'):
    def cancel():
        from zut.json import ExtendedJSONEncoder
        return json.dumps(values, ensure_ascii=False, cls=ExtendedJSONEncoder)

    target_str = ''

    for value in values:
        value = to_str(value)
        
        if separator in value:
            return cancel()
        
        if not target_str:
            if value.startswith(('{', '[')):
                return cancel() # avoid ambiguity with postgresql literal or with JSON dump
            target_str = value
        else:        
            target_str += f'{separator}{value}'
    
    return target_str


def get_visual_mapping_literal(values: Mapping, *, separator = '|'):
    def cancel():
        from zut.json import ExtendedJSONEncoder
        return json.dumps(values, ensure_ascii=False, cls=ExtendedJSONEncoder)
    
    target_str = ''
    
    for key, value in values.items():
        key = to_str(key)
        value = to_str(value)
        
        if '=' in key or separator in key or '=' in value or separator in value:
            return cancel()
        
        if not target_str:
            if value.startswith(('{', '[')):
                return cancel() # avoid ambiguity with postgresql literal or with JSON dump
            target_str = value
        else:        
            target_str += separator + (f'{key}={value}' if value else key)
        
    return target_str


def get_duration_iso_string(duration: timedelta):
    # Adapted from: django.utils.duration.duration_iso_string
    if duration < timedelta(0):
        sign = "-"
        duration *= -1
    else:
        sign = ""

    days, hours, minutes, seconds, microseconds = _get_duration_components(duration)
    ms = ".{:06d}".format(microseconds) if microseconds else ""
    return "{}P{}DT{:02d}H{:02d}M{:02d}{}S".format(
        sign, days, hours, minutes, seconds, ms
    )


def _get_duration_components(duration: timedelta):
    days = duration.days
    seconds = duration.seconds
    microseconds = duration.microseconds

    minutes = seconds // 60
    seconds = seconds % 60

    hours = minutes // 60
    minutes = minutes % 60

    return days, hours, minutes, seconds, microseconds


def to_str(value: Any) -> str:    
    if value is None:
        return ''
    elif isinstance(value, str):
        return value
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, (float,Decimal)):
        return format(value, 'f')
    elif isinstance(value, (list,tuple,set)):
        return get_visual_iterable_literal(value)
    elif isinstance(value, Mapping):
        return get_visual_mapping_literal(value)
    else:
        return str(value)
    

def convert(value: Any, to: type[T], *, accept_localized = True, decimal_digits: int|None = None, reduce_money = False, separator = '|') -> T:
    if value is None:
        return None # type: ignore
    
    element_to: type|None = None
    try:
        from types import GenericAlias
        if isinstance(to, GenericAlias):
            type_args = get_args(to)
            to = get_origin(to)
            if to == list or to == tuple or to == set:
                if len(type_args) != 1:
                    raise ValueError(f"Only one generic type parameter may be used for {to}")
                element_to = type_args[0]
            else:
                raise ValueError(f"Generic {to} not supported")
    except ImportError:
        # GenericAlias: was introducted in Python 3.9
        pass
    
    if isinstance(value, to):
        return value # type: ignore
    
    if to == bool:
        converted_value = parse_bool(value)

    elif to == float:
        converted_value = parse_float(value, accept_localized=accept_localized)

    elif to == Decimal:
        converted_value = parse_decimal(value, decimal_digits=decimal_digits, reduce_money=reduce_money, accept_localized=accept_localized)
    
    elif to == date:
        converted_value = parse_date(value, accept_localized=accept_localized)
    
    elif to == datetime or to == time:
        converted_value = parse_datetime(value, accept_localized=accept_localized)
    
    elif to == list or to == tuple or to == set:
        converted_value = parse_list(value, separator=separator)
        if converted_value is not None:
            if element_to:
                converted_value = [convert(element, element_to, decimal_digits=decimal_digits, reduce_money=reduce_money, accept_localized=accept_localized, separator=separator) for element in converted_value]
            
            if to != list:
                converted_value = to(converted_value)  # type: ignore

    elif to == dict:
        converted_value = parse_dict(value, separator=separator)
    
    elif callable(to):
        converted_value = to(value) # type: ignore

    else:
        raise NotImplementedError(f"Don't know how to convert type {type(value).__name__} to {to}")

    return converted_value # type: ignore
    