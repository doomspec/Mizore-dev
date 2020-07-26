import sys
import numpy as np


def dec2bin(number, length):
    """Converts a decimal number into a binary representation
    of fixed number of bits.
    Args:
        number: (int) the input decimal number
        length: (int) number of bits in the output string
    Returns:
        A list of binary numbers
    """

    if pow(2, length) < number:
        sys.exit('Insufficient number of bits for representing the number {}'.format(number))

    bit_str = bin(number)
    bit_str = bit_str[2:len(bit_str)]  # chop off the first two chars
    bit_string = [int(x) for x in list(bit_str)]
    if len(bit_string) < length:
        len_zeros = length - len(bit_string)
        bit_string = [int(x) for x in list(np.zeros(len_zeros))] + bit_string

    return bit_string
