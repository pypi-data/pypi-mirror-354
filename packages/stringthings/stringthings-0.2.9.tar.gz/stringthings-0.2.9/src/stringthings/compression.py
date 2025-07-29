# -*-coding: utf-8 -*-
"""
Created on Mon Jan 01 13:53:33 2024

@author: Martín Araya
"""

__version__ = "0.2.8"
__release__ = 20240510

__all__ = ['expand', 'compress']


def expand(keyword_values, default_value=0):
    """
    `expand` receives a list of values or a space-separated string containing
    the values of the property keyword in the eclipse compressed format '3*0.257' and
    returns the expanded '0.257 0.257 0.257' property as a space-separated string.

    :param keyword_values: str or list
    :param default_value: str, int or float
    :return: str
    """
    if type(keyword_values) is list:
        if list(set([type(each) for each in keyword_values]))[0] is list:
            keyword_values = ' '.join(
                [item
                 for row in keyword_values
                 for item in row]
            )
        else:
            keyword_values = list(map(str, keyword_values))

    keyword_values = ' '.join(keyword_values.strip().split())
    default_value = f'*{default_value} '
    if '* ' in keyword_values:
        keyword_values = keyword_values.replace('* ', default_value)

    keyword_values = ' '.join(
        [' '.join([each.split('*')[1]] * int(each.split('*')[0]))
         if '*' in each
         else each
         for each in keyword_values.split()
         ]
    )
    return keyword_values


def compress(keyword_values):
    """
    `compress` receives list of values or a space-separated string containing
    the values of the property keyword and returns the compressed property
    '0.114 3*0.257 0.362' (instead of '0.114 0.257 0.257 0.257 0.362') as a
    space-separated string.

    :param keyword_values: str or list
    :return: str
    """
    if type(keyword_values) is str:
        keyword_values = keyword_values.split()
    elif type(keyword_values) is list:
        if list(set([type(each) for each in keyword_values]))[0] is list:
            keyword_values = ' '.join(
                [item
                 for row in keyword_values
                 for item in row]
            )
        else:
            keyword_values = list(map(str, keyword_values))
    else:
        raise TypeError('incorrect input format, string or list expected.')

    compressed = []
    i = 0
    while i < len(keyword_values):
        r = 1
        while i + r < len(keyword_values) and keyword_values[i] == keyword_values[i + r]:
            r += 1
        if r == 1:
            compressed.append(keyword_values[i])
        else:
            compressed.append(f'{r}*{keyword_values[i]}')
        i += r

    return ' '.join(compressed)
