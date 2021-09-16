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


def pharma_datamatrix(barcode: str, separator=29) -> dict:
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
        result = {'ERROR': 'INVALID BARCODE'}

    return result
