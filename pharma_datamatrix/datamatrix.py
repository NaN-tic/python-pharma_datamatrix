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
This function contains code to identify the barcode type: GS1-GTIN or IFA-PPN.

Possible knowed separators:
    Default value is 29. It's the <GS> char
        u'\x1d'
        ^[
    Some scans change the GS for a Ç, that is the code 199
        u'\xc7'
    Some scans change the GS for a |, that is the code 124
        u'\x7c'

"""

from .gs1_gtin import gs1_gtin
from .ifa_ppn import ifa_ppn


def read_datamatrix(barcode: str, separator=29) -> dict:
    """
    The function takes barcode string and return parsed objects in a `dict`.
    Optionally user can pass bool value to validate the barcode
    Parameters:
        barcode: string type. This is the barcode string with the <GS>
        seperators.

    Returns:
        dict: Returns dictionary object with SCHEME, PPN, GTIN, EXPIRY, BATCH,
        SERIAL & NHRN as keys for valid requests or relevant error strings.
    """
    # Most barcode scanners prepend ']d2' identifier for the GS1 datamatrix.
    # This senction removes the identifier.
    if barcode[:3] == ']d2':
        barcode = barcode[3:]
        result = gs1_gtin(barcode, separator)
    elif barcode[:2] in ['01', '21', '17', '10', '71']:
        result = gs1_gtin(barcode, separator)
    # MACRO 06 or MACRO 05
    elif barcode[:6] == ('[)>'+chr(30)+'06') or ('[)>'+chr(30)+'05'):
        # Removes the leading ASCII seperator after the scheme identifier.
        barcode = barcode[7:]
        result = ifa_ppn(barcode, separator)
    else:
        result = {'ERROR': 'INVALID OR UNSUPORTED BARCODE', 'VALUE': barcode}

    return result
