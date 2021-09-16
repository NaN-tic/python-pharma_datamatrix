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
The function perform validation on the GS1-GTIN(14) based on the check digit
detailed in the link below:
https://www.gs1.org/services/how-calculate-check-digit-manually

"""


def gtin_check(gtin: str):
    reverse_gtin = gtin[-2::-1]  # Reversing the string without the check-digit
    digit_multipler3 = []
    digit_multipler1 = []

    for i, l in enumerate(reverse_gtin):
        if i % 2 == 0:
            digit_multipler3.append(int(l))
        else:
            digit_multipler1.append(int(l))

    digit_sum = (sum(digit_multipler3) * 3) + sum(digit_multipler1)
    nearest_ten = round(digit_sum/10) * 10
    check_sum_digit = nearest_ten - digit_sum
    if check_sum_digit < 0:
        check_sum_digit = 10 + check_sum_digit
    return check_sum_digit == int(gtin[-1])
