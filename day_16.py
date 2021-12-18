import heapq
import sys
import itertools
import more_itertools
from collections import defaultdict, Counter, deque
import re
from queue import PriorityQueue

import numpy as np
from more_itertools import sliding_window
from networkx import Graph

import binascii

hex2bin = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

bin2hex = {v: k for k, v in hex2bin.items()}


def parse_hex(s):
    '''
    >>> parse_hex('D2FE28')
    '110100101111111000101000'
    '''
    x = "".join([hex2bin[c] for c in s])
    return x


def bits2char(bits):
    '''
    >>> bits2char('110')
    '6'
    >>> bits2char('100')
    '4'
    '''
    x = bits
    while len(x) < 4:
        x = '0' + x
    return bin2hex[x]


def binary2literal(binary_string):
    '''
    >>> binary2literal('011111100101')
    2021
    '''
    ret_val = 0
    x = 1
    for c in binary_string[::-1]:
        if c == '1':
            ret_val += x
        x *= 2
    return ret_val


class Buffer:
    '''
    >>> b = Buffer('D2FE28')
    >>> b.buffer
    '110100101111111000101000'
    >>> b.pos
    0
    >>> v = b.read_int(3)
    >>> v
    6
    >>> t = b.read_int(3)
    >>> t
    4
    '''

    def __init__(self, hex_string):
        self.buffer = parse_hex(hex_string)
        self.pos = 0

    def read_int(self, bits):
        return int(bits2char(self.read_next(bits)))

    def read_next(self, bits):
        s = self.buffer[self.pos:self.pos + bits]
        self.pos += bits
        return s

    def set_pos(self, pos):
        self.pos = pos

    def peek_next(self, bits):
        return self.buffer[self.pos:self.pos + bits]

    def read_literal_int(self, chunk_size):
        '''
        >>> b = Buffer('D2FE28')
        >>> b.set_pos(6)
        >>> x = b.read_literal_int(5)
        >>> x
        2021
        >>> b.pos
        21
        >>> b.peek_next(10)
        '000'
        '''

        s = ''
        while True:
            c = self.read_next(chunk_size)
            s += c[1:chunk_size]
            if c[0] == '0':
                break

        return int(binary2literal(s))

    def next_packet(self):
        '''
        >>> b = Buffer('D2FE28')
        >>> p = b.next_packet()
        >>> p
        {'version': 6, 'typeid': 4, 'value': 2021}
        >>> b = Buffer('38006F45291200')
        >>> p = b.next_packet()
        >>> p
        {'version': 1, 'typeid': 6, 'packets': [{'version': 6, 'typeid': 4, 'value': 10}, {'version': 2, 'typeid': 4, 'value': 20}]}
        >>> b = Buffer('EE00D40C823060')
        >>> p = b.next_packet()
        >>> p
        {'version': 7, 'typeid': 3, 'packets': [{'version': 2, 'typeid': 4, 'value': 1}, {'version': 4, 'typeid': 4, 'value': 2}, {'version': 1, 'typeid': 4, 'value': 3}]}
        >>> b = Buffer('8A004A801A8002F478')
        >>> p = b.next_packet()
        >>> p
        {'version': 4, 'typeid': 2, 'packets': [{'version': 1, 'typeid': 2, 'packets': [{'version': 5, 'typeid': 2, 'packets': [{'version': 6, 'typeid': 4, 'value': 15}]}]}]}
        '''
        # read the version
        version = self.read_int(3)
        type_id = self.read_int(3)

        if type_id == 4:
            literal = self.read_literal_int(5)
            return {
                'version': version,
                'typeid': type_id,
                'value': literal
            }
        else:
            length_type_id = self.read_int(1)
            if length_type_id == 0:
                total_length = binary2literal(self.read_next(15))
                stop_pos = self.pos + total_length
                subpackets = []
                while self.pos < stop_pos:
                    p = self.next_packet()
                    subpackets.append(p)

                return {
                    'version': version,
                    'typeid': type_id,
                    'packets': subpackets
                }
            else:
                num_sub_packets = binary2literal(self.read_next(11))
                subpackets = []
                for i in range(0, num_sub_packets):
                    subpackets.append(self.next_packet())
                return {
                    'version': version,
                    'typeid': type_id,
                    'packets': subpackets
                }


def get_int(binary_string, start_index, bits):
    return int(bits2char(binary_string[start_index:start_index + bits]))


def get_version(binary_string, packet_start_index):
    '''
    >>> get_version('110100101111111000101000',0)
    6
    '''
    return get_int(binary_string, packet_start_index, 3)


def get_typeid(binary_string, packet_start_index):
    '''
    >>> get_typeid('110100101111111000101000', 0)
    4
    '''
    return get_int(binary_string, packet_start_index + 3, 3)


def parse_literal_packet(version, typeid, binary_string, start_index):
    # typeid of 4 is a literal packet
    # read groups of 5

    # 110100101111111000101000
    # VVVTTTAAAAABBBBBCCCCC
    last_index = 0
    chunk_size = 5
    data_start_index = start_index + 6
    s = ""

    bits_read = 6

    def next_chunk():
        start = data_start_index + last_index
        end = start + chunk_size
        # skip the first bit
        return binary_string[start + 1:end]

    while binary_string[data_start_index + last_index] != '0':
        s = s + next_chunk()
        bits_read += 5
        last_index += chunk_size

    s = s + next_chunk()
    bits_read += 5

    return {
        'version': version,
        'typeid': typeid,
        'binary': s,
        'decimal': binary2literal(s),
        'bits': bits_read
    }


def parse_operator_packet(version, typeid, binary_string, start_index):
    '''
    >>> parse_operator_packet(1,6,'00111000000000000110111101000101001010010001001000000000', 0)
    :param version:
    :param typeid:
    :param binary_string:
    :return:
    '''
    #
    # 012345678901234567890123456789
    # 00111000000000000110111101000101001010010001001000000000
    # VVVTTTILLLLLLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBBBBBB

    current_index = start_index + 6
    i = binary_string[current_index]

    current_index += 1
    if i == '0':
        # next 15 bits are a number that represents the total length in bits
        # of the subpackets
        total_length = binary2literal(binary_string[current_index:current_index + 15])
        current_index += 15
        subpackets = binary_string[current_index, current_index + total_length]

    else:
        # next 11 bits are the number of subpackets
        num_subpackets = binary2literal(binary_string[next:next + 11])


def parse_packet(binary_string, start_index):
    '''
    >>> parse_packet('110100101111111000101000',0)
    {'version': 6, 'typeid': 4, 'binary': '011111100101', 'decimal': 2021}
    >>> parse_packet('00111000000000000110111101000101001010010001001000000000',0)
    '''
    v = get_version(binary_string, start_index)
    t = get_typeid(binary_string, start_index)
    if t == 4:
        return parse_literal_packet(v, t, binary_string, start_index)
    else:
        return parse_operator_packet(v, t, binary_string, start_index)


def parse(hex_string):
    b = Buffer(hex_string)
    p = next_packet(b)
