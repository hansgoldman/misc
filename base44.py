################################################################################
# Filename: base44.py
#
# Description: Methods to encode and decode integer numbers (base 10) into a
#   base 44 system and back again.
#
# Author: Hans Goldman
# Create Date: 2/12/2015
# Last Modified by: Hans Goldman
# Last Modified Date: 2/12/2015
################################################################################

import string


# Declare "constants"
ALPHABET            = string.ascii_lowercase + string.digits
ALPHABET_DICTIONARY = dict((character, index) for (index, character) in enumerate(ALPHABET))
BASE                = len(ALPHABET)
SIGN_CHARACTER      = '-'


def encode(base_10_number):
    """
    Returns a string representation of an integer number in base 44
    :param base_10_number: An integer that you want converted into base 44
    :return: A string representation of the given integer in base 44
    """
    string_list = []

    if base_10_number < 0:
        return SIGN_CHARACTER + encode(-base_10_number)

    while True:
        base_10_number, r = divmod(base_10_number, BASE)
        string_list.append(ALPHABET[r])

        if base_10_number == 0:
            break

    base_44_string = ''.join(reversed(string_list))

    return base_44_string


def decode(base_44_string):
    """
    Returns an integer from a given base 44 string
    :param base_44_string: A string that you want converted from base 44 to base 10
    :return: An integer representation of the given base 44 string
    """
    result = 0

    if base_44_string[0] == SIGN_CHARACTER:
        return -decode(base_44_string[1:])

    for character in base_44_string:
        result = result * BASE + ALPHABET_DICTIONARY[character]

    return result
