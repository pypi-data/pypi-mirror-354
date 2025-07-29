# -*-coding: utf-8 -*-
"""
Created on Mon Jan 01 13:53:33 2024

@author: Martín Araya
"""

__version__ = "0.2.8"
__release__ = 20240510

import numpy as np
import pandas as pd
import datetime as dt
from .errors import UndefinedDateFormat

__all__ = ['format_date', 'is_date']


def is_date(date_str, format_in='', verbose=False, return_format=False):
    """
    returns True if the string 'dateStr' is a valid date, otherwise returns False.
    """
    if type(date_str) is str and len(date_str.strip()) == 0:
        return False

    if format_in != '':
        try:
            format_date(date_str, format_in=format_in, verbose=verbose, return_format=return_format)
            if return_format:
                return format_date(date_str, format_in=format_in, verbose=verbose, return_format=True)
            return True
        except:
            return False

    else:
        try:
            format_date(date_str, format_in='', verbose=verbose)
            if return_format:
                return format_date(date_str, format_in='', verbose=verbose, return_format=True)
            return True
        except:
            pass

        formats = ['DD-MM-YYYY', 'DD-MMM-YYYY', 'YYYY-MM-DD', 'YYYY-MMM-DD', 'MM-DD-YYYY', 'MMM-DD-YYYY', 'YYYY-DD-MM',
                   'YYYY-DD-MMM', 'YYYYMMDD', 'YYYYMMMDD', 'DD-MM-YY', 'MMM-DD-YY', 'MM-DD-YY']
        separators = ['-', '/', ' ', '\t', '_', ':', ';', ', ', '.', '#', "'"]
        for f in formats:
            for sep in separators:
                f_in = f.replace('-', sep) if sep != '-' else f
                try:
                    format_date(date_str, format_in=f_in, verbose=verbose)
                    if return_format:
                        return f_in
                    return True
                except:
                    pass

        formats = ['YYYYMMDD', 'YYYYMMMDD']
        for f_in in formats:
            try:
                format_date(date_str, format_in=f_in, verbose=verbose)
                if return_format:
                    return f_in
                return True
            except:
                pass
    return False


def format_date(dates, format_in='', format_out='', verbose=True, year_base_in=1900, return_format=False):
    """
    `format_date` receives a string containing a date or a list of strings
    containing dates and changes the date format to the format specified by
    the user. By default, the out format will be 'DD-MMM-YYYY'.

    The input and output format can be stated with the keywords formatIN
    and formatOUT followed by a string containing the characters 'D', 'M'
    and 'Y' to identify day, month and year and the characters '/', '-', ' ',
    '\t' (tab) or '_' as separators.

    If the keyword format_in is not entered, the program will try to infer
    the date format from the provided data.

    syntax examples:

    stringformat.get_date('31/DEC/1984', format_in='DD/MMM/YYYY', format_out='MM-DD-YYYY')

    verbose parameter set to True will print a message showing the input and output formats.
    """

    def np_date_only(numpy_date):
        return numpy_date.split('T')[0]

    month_string_to_number = {'JAN': 1,
                              'FEB': 2,
                              'MAR': 3,
                              'APR': 4,
                              'MAY': 5,
                              'JUN': 6,
                              'JLY': 7,
                              'JUL': 7,
                              'AUG': 8,
                              'SEP': 9,
                              'OCT': 10,
                              'NOV': 11,
                              'DEC': 12}

    month_number_to_string = dict(zip(month_string_to_number.values(), month_string_to_number.keys()))

    separator = ''  # initialize
    format_in = format_in.upper().strip()
    format_out = format_out.upper().strip()
    # define if input is a list/tuple of dates or a single date
    sample = str(dates)
    output = list
    if type(dates) is list or type(dates) is tuple:
        output = list
        if type(dates[0]) is str:
            for i in range(len(dates)):
                dates[i] = dates[i].strip()
            sample = dates[0].strip()
        elif type(dates[0]) is np.datetime64:
            dates = np.array(dates)
        elif type(dates[0]) is np.str_:
            dates = list(map(str, dates))
            sample = dates[0].strip()

    if type(dates) is pd.Series:
        dates = dates.to_numpy()

    if type(dates) is np.ndarray:
        output = list
        sample = dates[0]
        if 'datetime64' in str(dates.dtype):
            dates = list(np.datetime_as_string(dates))
            dates = list(map(np_date_only, dates))
            format_in = 'YYYY-MM-DD'
            separator = '-'

    if type(dates) is np.datetime64:
        format_in = 'YYYY-MM-DD'
        dates = np.datetime_as_string(dates)
        dates = np_date_only(dates)
        sample = dates
        output = str
        separator = '-'

    if type(dates) is pd.Timestamp:  # pd._libs.tslibs.timestamps.Timestamp
        dates = dates.date()

    if type(dates) is dt.date:
        dates = str(dates)
        if format_in == '':
            format_in = 'YYYY-MM-DD'

    if type(dates) is dt.datetime:
        dates = str(dates).split()[0]
        if format_in == '':
            format_in = 'YYYY-MM-DD'

    if type(dates) is str:
        sample = dates.strip(' "\'')
        dates = [dates]
        output = str

    # look for the separator, empty string if not found
    if separator == '':
        for sep in ['/', '-', ' ', '\t', '_', ':', ';', ', ', '.', '#', "'"]:
            if sep in sample:
                separator = sep
                break

    # separate the 1st, 2nd and 3rd components of the DATEs in three lists
    if separator != '':
        # separate the 1st, 2nd and 3rd components of the DATEs in three lists
        date_list = separator.join(dates).split(separator)
        date_list = [date_list[0::3], date_list[1::3], date_list[2::3]]

    else:
        l = 0
        if max(map(len, dates)) == min(map(len, dates)):
            l = max(map(len, dates))

        if format_in != '':
            x, y = 0, 0
            for i in range(1, len(format_in)):
                if format_in[i] != format_in[i - 1]:
                    if x == 0:
                        x = i
                    else:
                        y = i
                        break
            date_list = [[d[:x], d[x:y], d[y:]] for d in dates]
            date_list = [[date_list[i][0] for i in range(len(date_list))],
                         [date_list[i][1] for i in range(len(date_list))],
                         [date_list[i][2] for i in range(len(date_list))]]

        elif l == 6:
            date_list = [[d[0:2], d[2:4], d[4:6]] for d in dates]
            date_list = [[date_list[i][0] for i in range(len(date_list))],
                         [date_list[i][1] for i in range(len(date_list))],
                         [date_list[i][2] for i in range(len(date_list))]]
        elif l == 8:
            date_list = [[d[0:2], d[2:4], d[4:8]] for d in dates]
            date_list = [[date_list[i][0] for i in range(len(date_list))],
                         [date_list[i][1] for i in range(len(date_list))],
                         [date_list[i][2] for i in range(len(date_list))]]
            if int(max(date_list[0])) <= 31 and int(min(date_list[2])) >= 1900 and int(
                    max(date_list[2])) <= 2050 and int(
                max(date_list[1])) <= 12:
                pass  # DDMMYYYY
            else:
                date_list = [[d[0:4], d[4:6], d[6:8]] for d in dates]
                date_list = [[date_list[i][0] for i in range(len(date_list))],
                             [date_list[i][1] for i in range(len(date_list))],
                             [date_list[i][2] for i in range(len(date_list))]]
                if int(max(date_list[2])) <= 31 and int(min(date_list[0])) >= 1900 and int(
                        max(date_list[0])) <= 2150 and int(max(date_list[1])) <= 12:
                    pass  # YYYYMMDD
                else:
                    raise UndefinedDateFormat(
                        f'Unable to identify date format, please provide with keyword format_in.\n: input:\n{dates[0] if len(dates) == 1 else dates}')
        elif l == 9:
            x, y = 0, 0
            for i in range(9):
                if not dates[0][i].isdigit() and x == 0:
                    x = i
                elif dates[0][i].isdigit() and x > 0:
                    y = i
                    break
            date_list = [[d[:x], d[x:y], d[y:]] for d in dates]
            date_list = [[date_list[i][0] for i in range(len(date_list))],
                         [date_list[i][1] for i in range(len(date_list))],
                         [date_list[i][2] for i in range(len(date_list))]]
        else:
            raise UndefinedDateFormat(
                f'Unable to identify date format, please provide with keyword format_in.\n: input:\n{dates[0] if len(dates) == 1 else dates}')

    # if format_in is not defined try to guess what it is
    if format_in == '':
        date_str = [False, False, False]
        date_max = [None, None, None]

        for i in range(3):
            for j in range(len(dates)):
                try:
                    date_list[i][j] = int(date_list[i][j])
                except:
                    date_str[i] = True
                    break
            if not date_str[i]:
                date_max[i] = max(date_list[i])

        order_in = [None, None, None, separator, None, None, None]
        found = ''
        if True in date_str:
            order_in[5] = 3
            found = found + 'Ms'
        for i in range(3):
            if date_str[i]:
                order_in[1] = i
                found = found + 'M'
            elif date_max[i] is not None and date_max[i] > 999:
                order_in[2] = i
                order_in[6] = 4
                found = found + 'Y'
            elif date_max[i] is not None and date_max[i] > 99:
                order_in[2] = i
                order_in[6] = 3
                found = found + 'Y'
            elif date_max[i] is not None and date_max[i] > 31:
                order_in[2] = i
                order_in[6] = 2
                found = found + 'Y'
            elif date_max[i] is not None and (12 < date_max[i] <= 31):
                order_in[0] = i
                order_in[4] = 2
                found = found + 'D'
            else:
                pass

        if None in order_in:
            for i in range(3):
                if date_max[i] is not None and date_max[i] <= 12:
                    if 'D' in found and 'M' not in found:
                        order_in[1] = i
                        order_in[5] = 2
                        found = found + 'M'
                    elif 'M' in found and 'D' not in found:
                        order_in[0] = i
                        order_in[4] = 2
                        found = found + 'D'

        if 'Ms' in found:
            found = found[2:]

        if 'D' in found and 'M' in found and 'Y' in found:
            format_in = []
            for i in range(3):
                if order_in[i] == 0:
                    format_in.append('D' * order_in[4])
                elif order_in[i] == 1:
                    format_in.append('M' * order_in[5])
                elif order_in[i] == 2:
                    format_in.append('Y' * order_in[6])
            format_in = order_in[3].join(format_in)
            if verbose:
                print(' the input format is: ' + format_in)

        else:
            raise UndefinedDateFormat(
                f'Unable to identify date format, please provide with keyword format_in.\n: input:\n{dates[0] if len(dates) == 1 else dates}')

        if return_format:
            return format_in

    # read input format from formatIN
    else:
        order_in = [None, None, None, None, None, None,
                    None]  # [day, month, year, separator, day_digit, month_digits, year_digits]
        for sep in ['/', '-', ' ', '\t', '_', ':', ';', '#', "'"]:
            if sep in format_in:
                order_in[3] = sep
                break
        index_dmy = [format_in.upper().index('D'), format_in.upper().index('M'), format_in.upper().index('Y')]
        for i in range(3):
            if index_dmy[i] == min(index_dmy):
                order_in[i] = 0
            elif index_dmy[i] == max(index_dmy):
                order_in[i] = 2
            else:
                order_in[i] = 1
        order_in[4] = format_in.upper().count('D')
        order_in[5] = format_in.upper().count('M')
        order_in[6] = format_in.upper().count('Y')

        for sep in ['/', '-', ' ', '\t']:
            if sep in format_in:
                test = sep
                break

    # set formatOUT by default if not provided
    if format_out == '':
        format_out = 'DD-MMM-YYYY'
        order_out = [0, 1, 2, '-', 2, 3, 4]
        # if speak and formatIN != formatOUT :
        #     print(' default output format is: DD-MMM-YYYY')

    # read format from formatOUT
    else:
        order_out = [None, None, None, '', None, None, None]
        # [day, month, year, separator, day_digit, month_digits, year_digits]
        for sep in ['/', '-', ' ', '\t', '_', ':', ';', '#', "'"]:
            if sep in format_out:
                order_out[3] = sep
                break
        if 'D' in format_out.upper():
            index_d = format_out.upper().index('D')
        else:
            index_d = 2
        if 'M' in format_out.upper():
            index_m = format_out.upper().index('M')
        else:
            index_m = 2
        if 'Y' in format_out.upper():
            index_y = format_out.upper().index('Y')
        else:
            index_y = 2
        index_dmy = [index_d, index_m, index_y]
        for i in range(3):
            if index_dmy[i] == min(index_dmy):
                order_out[i] = 0
            elif index_dmy[i] == max(index_dmy):
                order_out[i] = 2
            else:
                order_out[i] = 1
        order_out[4] = format_out.upper().count('D')
        order_out[5] = format_out.upper().count('M')
        order_out[6] = format_out.upper().count('Y')

    date_out = [date_list[order_in.index(order_out[0])],
                date_list[order_in.index(order_out[1])],
                date_list[order_in.index(order_out[2])]]

    if order_out[5] == 0:
        date_m = ''
    elif order_out[5] == 5:
        date_m = order_out[1]
        for i in range(len(date_out[date_m])):
            date_out[date_m][i] = str(int(date_out[date_m][i])).zfill(2) + month_number_to_string[
                int(date_out[date_m][i])]
    elif order_out[5] > 2 >= order_in[5]:
        date_m = order_out[1]
        for i in range(len(date_out[date_m])):
            date_out[date_m][i] = month_number_to_string[int(date_out[date_m][i])]
    elif order_out[5] <= 2 < order_in[5]:
        date_m = order_out[1]
        for i in range(len(date_out[date_m])):
            date_out[date_m][i] = month_string_to_number[date_out[date_m][i]]

    date_out_formatted = []
    number_format = [None, None, None]  # [year, day, month]
    for i in range(3):
        number_format[order_out[i]] = order_out[i + 4]
    for i in range(len(date_out[0])):
        # print(number_format)
        if number_format[0] == 0 or number_format[0] is None:
            date_str = ''
        elif type(date_out[0][i]) == int and number_format[0] == 2 and date_out[0][i] < 10:
            date_str = '0' + str(date_out[0][i]) + order_out[3]
        elif type(date_out[0][i]) == int and number_format[0] == 3 and date_out[0][i] < 10:
            date_str = '00' + str(date_out[0][i]) + order_out[3]
        elif type(date_out[0][i]) == int and number_format[0] == 3 and date_out[0][i] < 100:
            date_str = '0' + str(date_out[0][i]) + order_out[3]
        elif type(date_out[0][i]) == int and number_format[0] == 4 and date_out[0][i] < 10:
            if year_base_in == 0:
                date_str = '000' + str(date_out[0][i]) + order_out[3]
            else:
                date_str = str(date_out[0][i] + year_base_in) + order_out[3]
        elif type(date_out[0][i]) == int and number_format[0] == 4 and date_out[0][i] < 100:
            if year_base_in == 0:
                date_str = '00' + str(date_out[0][i]) + order_out[3]
            else:
                date_str = str(date_out[0][i] + year_base_in) + order_out[3]
        elif type(date_out[0][i]) == int and number_format[0] == 4 and date_out[0][i] < 1000:
            date_str = '0' + str(date_out[0][i]) + order_out[3]
        else:
            date_str = str(date_out[0][i]) + order_out[3]

        if number_format[1] == 0 or number_format[1] is None:
            date_str = date_str + ''
        elif type(date_out[1][i]) == int and number_format[1] == 2 and date_out[1][i] < 10:
            date_str = date_str + '0' + str(date_out[1][i]) + order_out[3]
        elif type(date_out[1][i]) == int and number_format[1] == 3 and date_out[1][i] < 10:
            date_str = date_str + '00' + str(date_out[1][i]) + order_out[3]
        elif type(date_out[1][i]) == int and number_format[1] == 3 and date_out[1][i] < 100:
            date_str = date_str + '0' + str(date_out[1][i]) + order_out[3]
        elif type(date_out[1][i]) == int and number_format[1] == 4 and date_out[1][i] < 10:
            if year_base_in == 0:
                date_str = date_str + '000' + str(date_out[1][i]) + order_out[3]
            else:
                date_str = date_str + str(date_out[1][i] + year_base_in) + order_out[3]
        elif type(date_out[1][i]) == int and number_format[1] == 4 and date_out[1][i] < 100:
            if year_base_in:
                date_str = date_str + '00' + str(date_out[1][i]) + order_out[3]
            else:
                date_str = date_str + str(date_out[1][i] + year_base_in) + order_out[3]
        elif type(date_out[1][i]) == int and number_format[1] == 4 and date_out[1][i] < 1000:
            date_str = date_str + '0' + str(date_out[1][i]) + order_out[3]
        else:
            date_str = date_str + str(date_out[1][i]) + order_out[3]

        if number_format[2] == 0 or number_format[2] is None:
            date_str = date_str + ''
        elif type(date_out[2][i]) == int and number_format[2] == 2 and date_out[2][i] < 10:
            date_str = date_str + '0' + str(date_out[2][i])
        elif type(date_out[2][i]) == int and number_format[2] == 3 and date_out[2][i] < 10:
            date_str = date_str + '00' + str(date_out[2][i])
        elif type(date_out[2][i]) == int and number_format[2] == 3 and date_out[2][i] < 100:
            date_str = date_str + '0' + str(date_out[2][i])
        elif type(date_out[2][i]) == int and number_format[2] == 4 and date_out[2][i] < 10:
            if year_base_in == 0:
                date_str = date_str + '000' + str(date_out[2][i])
            else:
                date_str = date_str + str(date_out[2][i] + year_base_in)
        elif type(date_out[2][i]) == int and number_format[2] == 4 and date_out[2][i] < 100:
            if year_base_in == 0:
                date_str = date_str + '00' + str(date_out[2][i])
            else:
                date_str = date_str + str(date_out[2][i] + year_base_in)
        elif type(date_out[2][i]) == int and number_format[2] == 4 and date_out[2][i] < 1000:
            date_str = date_str + '0' + str(date_out[2][i])
        else:
            date_str = date_str + str(date_out[2][i])

        date_out_formatted.append(date_str)

    if output is str:
        return date_out_formatted[0]
    else:
        return date_out_formatted
