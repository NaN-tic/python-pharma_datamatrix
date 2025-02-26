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
The function parse the GS1 Datamatrix barcode used for medicine packs.
The barcode scanners in the default setup outputs the scan is in below format:
]d201034531200000111719112510ABCD1234<GS>2110EW354EWER
(01)03453120000011(17)191125(10)ABCD1234<GS>(21)10EW354EWER
(01) = GTIN Identifier - Fixed 14 chars
(17) = Expiry Date Identifer - Fixed 6 Chars
(10) = Batch Identifier - Variable length.
       (upto 20 chars usually between 4 - 10 Chars)
(21) = Serial Number - Variable length.
       (upto 20 chars - Usually between 12 - 20 Chars)
(710 or 711 or 712 or 713 or 714) = Optional NHRN identifiers.
The symbology identifier ]d2 and for the second FNC1, when used as a separator
character is <GS> Group-Separator.

"""

# The GTIN validation module
from .gs1_gtin_validation import gtin_check
# The Expiry validation module
from .expiry_date_validation import expiry_date_check


def gs1_gtin(barcode: str, separator=29) -> dict:
    result = {'SCHEME': 'GTIN'}
    if chr(separator) in barcode:
        while barcode:
            if barcode[:2] == '01':
                result['GTIN'] = barcode[2:16]
                if len(barcode) > 16:
                    barcode = barcode[16:]
                else:
                    barcode = None
            elif barcode[:2] == '17':
                result['EXPIRY'] = barcode[2:8]
                if len(barcode) > 8:
                    barcode = barcode[8:]
                else:
                    barcode = None
            elif barcode[:2] == '10':
                if chr(separator) in barcode:
                    for i, c in enumerate(barcode):
                        if ord(c) == separator:
                            result['BATCH'] = barcode[2:i]
                            barcode = barcode[i+1:]
                            break
                else:
                    result['BATCH'] = barcode[2:]
                    barcode = None
            elif barcode[:2] == '21':
                if chr(separator) in barcode:
                    for i, c in enumerate(barcode):
                        if ord(c) == separator:
                            result['SERIAL'] = barcode[2:i]
                            barcode = barcode[i+1:]
                            break
                else:
                    result['SERIAL'] = barcode[2:]
                    barcode = None
            elif barcode[:3] in ['710', '711', '712', '713', '714']:
                if chr(separator) in barcode:
                    for i, c in enumerate(barcode):
                        if ord(c) == separator:
                            result['NHRN'] = barcode[3:i]
                            barcode = barcode[i+1:]
                            break
                else:
                    result['NHRN'] = barcode[3:]
                    barcode = None
            else:
                return {'ERROR': 'INVALID BARCODE', 'VALUE': barcode}
    else:
        return {'ERROR': 'INVALID SEPARATOR DEFINED', 'VALUE': separator}

    if 'GTIN' and 'BATCH' and 'EXPIRY' and 'SERIAL' in result.keys():
        if not expiry_date_check(result['EXPIRY']):
            return {'ERROR': 'INVALID EXPIRY DATE', 'VALUE': result['EXPIRY']}
        elif not gtin_check(result['GTIN']):
            return {'ERROR': 'INVALID GTIN', 'VALUE': result['GTIN']}
        else:
            return result
    else:
        return {'ERROR': 'MISSING MAIN KEYS IN BARCODE', 'VALUE': result}
