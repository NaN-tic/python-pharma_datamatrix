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
Each PPN requires two Modulo 97-calculated check digits for additional data
integrity.
To calculate the check digits, the ASCII value of the alphanumeric characters
is used and multiplied by an ascending weight factor. The weighting of the
digits starts on the left with two and increases by one for each following
digit. The results of each multiplication are summed up and divided by 97,
and the remainder are the check digits. If the remainder is only one digit, a
leading zero is added.
"""


def ppn_check(ppn: str) -> bool:
    i = 0
    weight = 2
    digit_sum = 0
    for i in range(10):
        digit_sum += (ord(ppn[i]) * weight)
        weight += 1
    print(digit_sum)
    check_digit = digit_sum % 97
    # PPN last two chars are converted to int to remove any leading zero.
    return check_digit == int(ppn[-2:])
