"""
When we want to change the value of our payload, we can use these format to change the value
in our payload giving us flexibility in our payload.

The Main string format function is at the end of this file. Functions before it are helper functions
for complex logic.
"""


import uuid
import string
from random import randint, SystemRandom

from .built_in_exceptions import InvalidPayloadException


def replace_timestamp(data, current_timestamp):
    '''
    11 characters
    <time_stamp>              --->   '16712345678'
    abc<time_stamp>def        --->   'abc16712345678def'
    <time_stamp>@yahoo.com    --->   '16712345678@yahoo.com'
    '''
    return data.replace("<time_stamp>", current_timestamp)


def replace_unique_timestamp(data, current_timestamp):
    '''
    11 characters
    <timestamp>              --->   '16712345678'
    abc<timestamp>def        --->   'abc16712345678def'
    <timestamp>@yahoo.com    --->   '16712345678@yahoo.com'
    '''
    unique_string = ''.join(SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(5))
    return data.replace("<timestamp>", unique_string + current_timestamp)


def replace_uuid(data):
    '''
    <uuid>              --->   'abcd-1234-qwer-5678'
    <uuid>@yahoo.com    --->   'abcd-1234-qwer-5678@yahoo.com'
    '''
    uuid_data = str(uuid.uuid4())
    return data.replace("<uuid>", uuid_data)


def get_index_start_end_index_and_count(data):
    '''
    Get index of "<" and ">" and count which is after "_" but before ">"

    return:
        start_index = the index of "<"
        end_index = the index of ">"
        count = the number/string after "_" but before ">"

    Example:
    sample<numbers_5>payload

    < = index 6
    > = index 16
    count = 5
    '''
    start_index = data.index("<")
    end_index = data.index(">")

    '''
    From function's example:
    [0] = numbers
    [1] = 5
    We use '1' below to indicate the second item after splitting the payload
    '''
    count = int(data[start_index:end_index].split("_")[1])

    return start_index, end_index, count


def replace_numbers(data):
    '''
    <numbers_5>          --->   '12345' (random)
    abc<numbers_5>def    --->   'abc12345def' (random)
    '''
    start_index, end_index, count = get_index_start_end_index_and_count(data)

    generated_number = ""

    for _ in range(count):
        generated_number += str(randint(0, 9))

    return data.replace(data[start_index:end_index + 1], generated_number)


def replace_random(data):
    '''
    <random_5>          --->   'a1b2c' (random)
    abc<random_5>def    --->   'abcz1x2cdef' (random)
    '''
    start_index, end_index, count = get_index_start_end_index_and_count(data)

    generated_random_text = ''.join(SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(count))
    return data.replace(data[start_index:end_index + 1], generated_random_text)


def replace_random_upper(data):
    '''
    <random_5>          --->   'a1b2c' (random)
    abc<random_5>def    --->   'abcz1x2cdef' (random)
    '''
    start_index, end_index, count = get_index_start_end_index_and_count(data)

    generated_random_text = ''.join(SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(count))
    return data.replace(data[start_index:end_index + 1], generated_random_text)


def replace_spaces(data):
    '''
    <spaces_5>          --->   '     '
    abc<spaces_5>123    --->   'abc     123'
    '''
    start_index, end_index, count = get_index_start_end_index_and_count(data)
    generated_spaces = ""

    for _ in range(count):
        generated_spaces += " "

    return data.replace(data[start_index:end_index + 1], generated_spaces)


def replace_empty(data):
    '''
    <empty_5>          --->   '     '
    abc<empty_5>123    --->   '     '
    '''
    # start_index and end_index are not used so replace it with '_'
    _, _, count = get_index_start_end_index_and_count(data)

    generated_spaces = ""

    for _ in range(count):
        generated_spaces += " "
    return generated_spaces


def replace_phone():
    generated_phone_number = ""
    for _ in range(10):
        generated_phone_number += str(randint(0, 9))
    return generated_phone_number


def replace_tin():
    tin = ""
    for _ in range(0, 12):
        random_number = randint(0, 9)
        tin += str(random_number)
    return tin


def replace_int(data):
    '''
    Returns an integer type
    '''
    try:
        integer = data.split("_")[1].replace(">", '')
        data_int = int(integer)
        return data_int
    except ValueError:
        raise InvalidPayloadException(payload=data, message="")


def string_format(data, current_timestamp=None):
    '''
    Describe here
    '''
    basic_replacements = {
        "<null>":  None,
        "<empty>": "",
        "<empty_array>": [],
        "<skip>": "SKIP",
        "<bool_true>": True,
        "<bool_false>": False,
        # Add basic replacements without complex logic here.
        }

    if data in basic_replacements.keys():
        return basic_replacements[data]
    elif "<time_stamp>" in data:
        return replace_timestamp(data, current_timestamp)
    elif "<unique_timestamp>" in data:
        return replace_unique_timestamp(data, current_timestamp)
    elif "<uuid>" in data:
        return replace_uuid(data)
    elif "<numbers_" in data:
        return replace_numbers(data)
    elif "<random_" in data:
        return replace_random(data)
    elif "<randomUpper_" in data:
        return replace_random_upper(data)
    elif "<spaces_" in data:
        return replace_spaces(data)
    elif "<empty_" in data:
        return replace_empty(data)
    elif "<phone>" in data:
        return replace_phone()
    elif "<tin>" in data:
        return replace_tin()
    elif "<int_" in data:
        return replace_int(data)
    else:
        return data
