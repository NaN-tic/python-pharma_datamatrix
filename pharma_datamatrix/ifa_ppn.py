# encoding: utf8
###############################################################################
#
#    MIT License
#
#    Copyright (c) 2021 PinchofLogic
#    Copyright (C) 2021 NaN Projectes de Programari Lliure, S.L.
#                            http://www.NaN-tic.com
#
#    Permission is hereby granted, free of charge, to any person obtaining a
#    copy of this software and associated documentation files (the "Software"),
#    to deal in the Software without restriction, including without limitation
#    the rights to use, copy, modify, merge, publish, distribute, sublicense,
#    and/or sell copies of the Software, and to permit persons to whom the
#    Software is furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THES SOFTWARE.
###############################################################################
"""
ASCII Code representation of a PPN code:
[)><30>06<29>9N 110375286414<29>1T12345ABCDE<29>D160617<29>S12345ABCDEF98765<30><4>

Actual Format including the ASCII chars is as below:

MACRO 06: The header [)> + ASCII 30 + ASCII 06 + ASCII 29 will be transmitted
by the barcode reader before the data in the message and the trailer
ASCII 30 + ASCII 4 will be transmitted afterwards.
OR
MACRO 05: The header [)> + ASCII 30 + ASCII 05 + ASCII 29 will be transmitted
by the barcode reader before the data in the message and the trailer
ASCII 30 + ASCII 4 will be transmitted afterwards.

<29> is the GS separator. It’s used before the start of each identifier string.

Identifier	Name	        Ex
9N	        PPN Code	    110375286414 (12 digits)
1T	        Batch	        12345-ABCDE (upto 20 digits)
D	        Expiry date	    160617 (YYMMDD)
S	        Serial number	12345ABCDEF98765 (between 12-20 chars)
8P	        GTIN	        08701234567896 (this is optional)

"""

# The Expiry validation module
from .expiry_date_validation import expiry_date_check
from .ifa_ppn_validation import ppn_check


def ifa_ppn(barcode: str, separator=29) -> dict:
    result = {'SCHEME': 'PPN'}
    while barcode:
        if barcode[:2] == '9N':
            result['PPN'] = barcode[2:14]
            if len(barcode) > 14:
                barcode = barcode[15:]
            else:
                barcode = None
        elif barcode[:1] == 'D':
            result['EXPIRY'] = barcode[1:7]
            if len(barcode) > 7:
                barcode = barcode[8:]
            else:
                barcode = None
        elif barcode[:2] == '1T':
            if chr(separator) in barcode:
                for i, c in enumerate(barcode):
                    if ord(c) == separator:
                        result['BATCH'] = barcode[2:i]
                        barcode = barcode[i+1:]
                        break
            else:
                for i, c in enumerate(barcode):
                    if ord(c) == 30:
                        result['BATCH'] = barcode[2:i]
                        barcode = None
        elif barcode[:1] == 'S':
            if chr(separator) in barcode:
                for i, c in enumerate(barcode):
                    if ord(c) == separator:
                        result['SERIAL'] = barcode[1:i]
                        barcode = barcode[i+1:]
                        break
            else:
                for i, c in enumerate(barcode):
                    if ord(c) == 30:
                        result['SERIAL'] = barcode[1:i]
                        barcode = None
        elif barcode[:2] == '8P':
            result['GTIN'] = barcode[2:16]
            if len(barcode) > 16:
                barcode = barcode[17:]
            else:
                barcode = None
        else:
            return {'ERROR': 'INVALID BARCODE', 'VALUE': barcode}

    if 'PPN' and 'BATCH' and 'EXPIRY' and 'SERIAL' in result.keys():
        if not expiry_date_check(result['EXPIRY']):
            return {'ERROR': 'INVALID EXPIRY DATE', 'VALUE': result['EXPIRY']}
        elif not ppn_check(result['PPN']):
            return {'ERROR': 'INVALID PPN', 'VALUE': result['GTIN']}
        else:
            return result
    else:
        return {'ERROR': 'MISSING MAIN KEYS IN BARCODE', 'VALUE': result}
