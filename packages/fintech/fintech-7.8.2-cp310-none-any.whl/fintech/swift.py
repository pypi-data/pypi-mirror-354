
###########################################################################
#
# LICENSE AGREEMENT
#
# Copyright (c) 2014-2024 joonis new media, Thimo Kraemer
#
# 1. Recitals
#
# joonis new media, Inh. Thimo Kraemer ("Licensor"), provides you
# ("Licensee") the program "PyFinTech" and associated documentation files
# (collectively, the "Software"). The Software is protected by German
# copyright laws and international treaties.
#
# 2. Public License
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this Software, to install and use the Software, copy, publish
# and distribute copies of the Software at any time, provided that this
# License Agreement is included in all copies or substantial portions of
# the Software, subject to the terms and conditions hereinafter set forth.
#
# 3. Temporary Multi-User/Multi-CPU License
#
# Licensor hereby grants to Licensee a temporary, non-exclusive license to
# install and use this Software according to the purpose agreed on up to
# an unlimited number of computers in its possession, subject to the terms
# and conditions hereinafter set forth. As consideration for this temporary
# license to use the Software granted to Licensee herein, Licensee shall
# pay to Licensor the agreed license fee.
#
# 4. Restrictions
#
# You may not use this Software in a way other than allowed in this
# license. You may not:
#
# - modify or adapt the Software or merge it into another program,
# - reverse engineer, disassemble, decompile or make any attempt to
#   discover the source code of the Software,
# - sublicense, rent, lease or lend any portion of the Software,
# - publish or distribute the associated license keycode.
#
# 5. Warranty and Remedy
#
# To the extent permitted by law, THE SOFTWARE IS PROVIDED "AS IS",
# WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF QUALITY, TITLE, NONINFRINGEMENT,
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, regardless of
# whether Licensor knows or had reason to know of Licensee particular
# needs. No employee, agent, or distributor of Licensor is authorized
# to modify this warranty, nor to make any additional warranties.
#
# IN NO EVENT WILL LICENSOR BE LIABLE TO LICENSEE FOR ANY DAMAGES,
# INCLUDING ANY LOST PROFITS, LOST SAVINGS, OR OTHER INCIDENTAL OR
# CONSEQUENTIAL DAMAGES ARISING FROM THE USE OR THE INABILITY TO USE THE
# SOFTWARE, EVEN IF LICENSOR OR AN AUTHORIZED DEALER OR DISTRIBUTOR HAS
# BEEN ADVISED OF THE POSSIBILITY OF THESE DAMAGES, OR FOR ANY CLAIM BY
# ANY OTHER PARTY. This does not apply if liability is mandatory due to
# intent or gross negligence.


"""
SWIFT module of the Python Fintech package.

This module defines functions to parse SWIFT messages.
"""

__all__ = ['parse_mt940', 'SWIFTParserError']

def parse_mt940(data):
    """
    Parses a SWIFT message of type MT940 or MT942.

    It returns a list of bank account statements which are represented
    as usual dictionaries. Also all SEPA fields are extracted. All
    values are converted to unicode strings.

    A dictionary has the following structure:

    - order_reference: string (Auftragssreferenz)
    - reference: string or ``None`` (Bezugsreferenz)
    - bankcode: string (Bankleitzahl)
    - account: string (Kontonummer)
    - number: string (Auszugsnummer)
    - balance_open: dict (Anfangssaldo)
        - amount: Decimal (Betrag)
        - currency: string (Währung)
        - date: date (Buchungsdatum)
    - balance_close: dict (Endsaldo)
        - amount: Decimal (Betrag)
        - currency: string (Währung)
        - date: date (Buchungsdatum)
    - balance_booked: dict or ``None`` (Valutensaldo gebucht)
        - amount: Decimal (Betrag)
        - currency: string (Währung)
        - date: date (Buchungsdatum)
    - balance_noted: dict or ``None`` (Valutensaldo vorgemerkt)
        - amount: Decimal (Betrag)
        - currency: string (Währung)
        - date: date (Buchungsdatum)
    - sum_credits: dict or ``None`` (Summe Gutschriften / MT942 only)
        - amount: Decimal (Betrag)
        - currency: string (Währung)
        - count: int (Anzahl Buchungen)
    - sum_debits: dict or ``None`` (Summe Belastungen / MT942 only)
        - amount: Decimal (Betrag)
        - currency: string (Währung)
        - count: int (Anzahl Buchungen)
    - transactions: list of dictionaries (Auszugsposten)
        - description: string or ``None`` (Beschreibung)
        - valuta: date (Wertstellungsdatum)
        - date: date or ``None`` (Buchungsdatum)
        - amount: Decimal (Betrag)
        - reversal: bool (Rückbuchung)
        - booking_key: string (Buchungsschlüssel)
        - booking_text: string or ``None`` (Buchungstext)
        - reference: string (Kundenreferenz)
        - bank_reference: string or ``None`` (Bankreferenz)
        - gvcode: string (Geschäftsvorfallcode)
        - primanota: string or ``None`` (Primanoten-Nr.)
        - bankcode: string or ``None`` (Bankleitzahl)
        - account: string or ``None`` (Kontonummer)
        - iban: string or ``None`` (IBAN)
        - amount_original: dict or ``None`` (Originalbetrag in Fremdwährung)
            - amount: Decimal (Betrag)
            - currency: string (Währung)
        - charges: dict or ``None`` (Gebühren)
            - amount: Decimal (Betrag)
            - currency: string (Währung)
        - textkey: int or ``None`` (Textschlüssel)
        - name: list of strings (Name)
        - purpose: list of strings (Verwendungszweck)
        - sepa: dictionary of SEPA fields
        - [nn]: Unknown structured fields are added with their numeric ids.

    :param data: The SWIFT message.
    :returns: A list of dictionaries.
    """
    ...


class SWIFTParserError(Exception):
    """SWIFT parser returned an error."""
    ...



from typing import TYPE_CHECKING
if not TYPE_CHECKING:
    import marshal, zlib, base64
    exec(marshal.loads(zlib.decompress(base64.b64decode(
        b'eJzVfAlYVEe2cN3bC013s4iAG2q70zSbNiAgEjSiQLOJuC9N091AS9Pgvd2CS3BBZRcU9wXcUHFlURGDmqlKMskkk5lMNsPkzZiY72WSmJjFLGom/lV1W0XF/PPe+977'
        b'3tOvr91VdarOfk5VnesN8MQfEf7E4Q8fgx8msADkggWMiTGxG8AC1iw6IDaJDjKcl0lslpSB5YAfsJA1S02SMmY9Y3Yxs2UMA0zSWcA1V+1y1yyfNTdxeqaqoNDksJpV'
        b'hTkqe55Zlb7CnldoU0232OxmY56qyGDMN+Sag+XyzDwL/2CsyZxjsZl5VY7DZrRbCm28yl6Ih3K8WeWc08zzGIwPlhuH9kJfhT/D8EdBSLDhRzkoZ8rZclG5uFxSLi13'
        b'KZeVu5bLyxXlynK3cvdyj3LP8n7lXuX9y73Lfcp9yweUDywfVD64fEi5X/nQnGGUcNkLwypAGXhh+ErX1cPKwFywengZYEDpsNLhs3p9LwauG9SiVGNvbjL40w9/+hN0'
        b'xJSjs4BalmqV4e8r41ggjlPg5qzAd0YuAY4xuBFe5NFlVI0q05JnogpUm6ZGtYmz04OkYBVsHhcvRlfR4Wg14yBEm1DjGrQb7uATU9BmVJOCahggT2RhK2yEF43ME1L1'
        b'eoDHHMIWBjPm/8OWHC8n+UyFCJPPYvIZSj5LSWZK2Vm9vv/r5M8UyO8eLc1ZJBqIZZYV6DVoKKCN3wezWUYR+ZZlfRejTRs3THNdWsJg0WZlKe+oC4VG90mS5AzWE2tr'
        b'VvI4mxi0AKscN1+ZNkh8e4LfOAA+Hvcde2F8ftH7jNUVd3Sm7GZaXSpWu8dlTfhoQnrOc4A2twV+77HNg5nCpF9nfp23YGg76AGOQNyRrkdrsRyqYaMiZKa/P6oKSQhC'
        b'VbAl0z8pBdUFBicGJaUwwObhOnnG1Kd47fKA6EjCa8JnkCN6yE3mX+JmXl/cfDjxQ24qBG6eYd2BHwADQ+ccXe2YOAU4gogytUZGYBpqNDpUgyqTZyYkBibOBhN0s5Ji'
        b'fOC2TFgNt4NciQtqQpvQWocvgbiM2mClFnaKATycDmALWDYQbXH44C7U4OKmhedwR2UygPtBPtyJuhwEGXQ2WqmdAMDieAB3ACPqhFsdRNvgCVQXE52CGiQABINgtH4l'
        b'RfXtUgXwBkAWOqfzuZGJBkGcB+39wWj8b+iS/XPWJk8GFmUjI+ENuOWn0cyXWf/IWpqTbHgzJ/gTtSHB8EWWlzEvx5p9M+vukiTDWzlqrySD2jPVcNp8nDnRP/cfpiTD'
        b'QrDVmGAoNG8VVzW3HgudOr9G7aeaE/391FdTj7pPr+/6nXKfBUx/x+fsG9+qWTtxG+ggNrwTCswqdYojKAALnAWoKckHlotl8AiqsmNVBZmwYSHmaBWqQzUiAM+WiKMY'
        b'2MYsUTM9rL9aLeKIXHo9WPy46xuTwxWuNNtUOYLPC+aLLTn22B45dWh6k8FuJuN4JX4oRyoZT0bG+OMPJ30whVrUI1lusDrMPS56Peew6fU9Cr3eaDUbbI4ivf6pddUM'
        b'RzSFk5AHmWUUmR8zHXj+XcqyjJQhTzEj/ZU8HVhxwKK4HE1CYEAqrE1LhPvgxsBECfBF68SDZqLq6Ua2lx6K+1Bw7FAeKjhL3YUIKzhLFVxElZotFc3q9b2YhIgnFPzB'
        b'5I8ruDTVQRCH9bDNihqwEQQBdAZdCSqG1YL2VaN6tAE1YLsLAajSM0ReIujrBlQtc+oeXIsOBMMN6KDlomeDiA/G3dHhcV9mLXip/s5UuAueq29paClrqxi3sasscR/z'
        b'Wg7RN2XO9WQR2HFc5lvXrmbsQzCQbS7s0CQFoYpE1OSZnCoBCtjGov1Y0audcupLAagYehSCtHOshQY7FTdRe2WAGAsai1r+UNRiKroeicmcbbFzZBBHHJWa7SVeliMB'
        b'rpeMCbjmoYw/6EPGJCoOmOuHZTw5gUqZBplABgwpEMMtcDM8S+3QJ8CLCWOB//WI5MljVmwodBCth/vRi+g8b0+AlyNCxYDNBugoOo9OUoizs72ZSBYMvB4ROBrNHzmI'
        b'CmVIFGzk7V7jI0IZwJoBapmYSAdHpvoyMSyIvB5xc02GckqK4HTOZWh4OzqHdkeEigCbC9BJeHKB4BbcBzI4TILrsW96vOP2h3w6Hu15AVbzdlifNpFgYwPoRA66RMdP'
        b'5Icw01iguh5rTfNesCVBGL9PhXbi8ecCJoaygC3E86O6bDp+cPFQJoEFnnh+13xNrDslFzWEorM8OgeP5IUT/GEZQB0L0D4KET91GJPMgtDrsUpJqFuaRmDQNlQBMAS6'
        b'ODI8VIIhNgD84+AwCvG7pSomnQWy67HJU9HYYDHVTrhrQgbPoVYjXQGjdAptHUqHs/qRTCaRQOypaO+UfFeBhDPoxGzU4ciOHE9Ixn4bdYRk0PHTR49m5hH+x96M2zeu'
        b'q8AxmEoMHoSbMQA8NGU8IRo7ZkzQMXScwhwRj2UWETHEvqn+/fS3UgWU6tFRf54fPEZLlliD1/REp+jwWT7+TBaRQlSNLzQCb8cA3OilQWfxAqhl1XgiNbgHoItoZ6QQ'
        b'sZUa7AtA3PWomwMGDVItpgBoPawKwxBjtONDXTDAXoC61ji5+k1JIJNH5BalTJTNDnMREKqILUYdPGyTK+WYBHSeCZtTRIcfdg1mrCzIwgjJ89OCRHT+0sGoXsEloHNU'
        b'R+FRgDpRpXN+hWsoU0TkHFUTee45t3zBQ+xPDlSgtpGTwwkAzp5EE2EZHb55upbBRpqO0Rk9ybvQR0DnQoKXQo72wK4JRGZoB+Pqb6XavrRgpgJd0KRS2aCNDGMvpe3T'
        b'RmXwqGO5d7E7Qf8go/F2UEz7o+2wm3cdAXe6oVYy1VUmAm4pELi0Be2CNYplueicA13A6oDamDFhg+l8c0wqXrFSytkJzC5mGNrrKxjQi4uDsAGdGIE6FaSrltHMhIeE'
        b'rgvwBNzFuy/1c8M8FEmYyTilWU89KhbXPlfefRQ65ebOAJErE+fBCsp2Dl0O4N3hEVjptoxQdJEJfkEqTNc9CV1VuA1dUgRrxEA0iomD6+AxgZvrV/fjuaTl1ACKADoN'
        b'u+ERwZ5eLIadGL9mVBURJgVsDvYHePLjTnphxSCeN4VpqeFgU2uHnbCBAsrReSOPE5JD2P10eBAenmHCYHkcRWUsbPXj0YV4eNHZd4LRJi9XewgamxbGlBArjQoMPW3/'
        b'Ey/kSP0jmNUsKLoe9ab+zf7p8bRx1IwoZi2xzqibQa9P7hgo2JQqmtnAgoTrUcmLNOnVatpoLIphKohhRimLbavS1tDGESGxTA0L8q5Hncqaolw7mjZ+LpvC1BOTjDo1'
        b'os5FNo42pqycymxjwTy8utsu2RZ32vhW6TRmFzHEKOu0DwObV9FGMT+D2ceCEgxeUJbi50cb98YkMgeIDYafmhAsmbWUNv4wJYU5TswmXDnms/gdDG38aEwqc4oYR3iy'
        b'+K+FEYJXmRiSzrQSAwgPnJNifXu6QGbeLOYcUfNw5azvho2YRtVi5CJUxivssExOtELJxOnRFZrOuYqSFFzcFHc3rEf9sB4dH03lkETCQwfqtK8p5kVUlzVo7VLBCzWi'
        b'ZliPTQCrIfaORDW3MSPhJbhXLaYIHPP6PbNPhCmdVBNV0i9HYClvf505gKP59YlvBv/RP0UYOW3eH5gjIuxRJr4ZcStqfgxt/Jv7H5njIkz+xED/cM20lc/Ow8lulm4E'
        b'yX4H5Ej+gzubnCdTFbK69KlUZWyqYwT+rsO6Xw2r09BmbBw4B0aViSnBqBLnk75Z4nFwp5Uiv9YhotnOdUm+8qJ7rJAG35viCvCeJvT6opzkl2cMB9QMBofCZl2IDm1O'
        b'wzmZDG3Aqp6/QoMaqP34x8+HHfAcSczRwXHMfABPwSqcGg0i/L/MwxqNP05mK0K8YSPOV5S5Ig9UC4TE6SisZ2EHuqTHaESDaNQ1niNMo4i8Mk9MiFT9Ob/YenJIutB4'
        b'YI4U4CTV888zSpSR44oA1ZcQHGdatKEAVazEK24FhkhY5iD55nK0Ll5HU+U6tFkCD6MaHawLSYSn/Rmgskvc0aVcOkEKugzbtWFgFNxMIinIXoQu0HQFeyatBu+86NYW'
        b'VYck4r1HF2rtrxahGnYC1Unsw06n4L2HUQfo3oNdLbjqvSyjhe3iGLQP/2gCVtiC2ijRGRLUqdWCUriLqCfINaIWOlEi56PVStHZqbj5IFg6D+s8Ge43Jl8bAVArPE1C'
        b'Nt5xt2U6hpMFWmEnatGhLnQ4ieCWKgjHvUgUiS5iz0ZgFWi/XBshhu2z8fjdwLwaXaXbdtQNW2C7LhnDhKDaIahFwwDFAuzbUC28rGYprHIM2qSNYNG+Ugy7B+TAHTNo'
        b'O9wDWwK1EVKXTEIkyF2NOqmK9MPQx3BGtxu14w1MigSIhzHwUG4SBRIrYI02goGnUzDQPpC3GlZQ9fCcuFJDxIEqU/EC8LQYKCeLPOCedKpY8ABsQNu18AJA5WPJT2DF'
        b'3D5EIX18YTeqTodlyUlkHyRCVxi4F9t6mSOFQDaPQGv55MTEFCU8Sk4xHm5A/YPVASnB6iBWDpvN8CjWwCP+/rDFV6PGGdQRjTfc5uuDjgyAx1gAq7w94YGBk6w/379/'
        b'f+IgiaCNfkuT0/E+nwrZgHYO0MAqj9SgBDEQxzHY1A74qb2FOHViHKrg0UWFG+cgTqmRGRUFDwtxatd0dBp1jH7eXei6wKjTJ1I+xUZNQB25rBPkCqMpcaUQz8MmWMer'
        b'5BhAcGHDJ8N1tMeBrtr5CFS2zCEneeKLjGoRbBZc3xWcblXx+J92dKEYnZPQBGME2h8mMHfDSB12mnvCcZcbQ4P8BBm6JETEFnQeHlOEwzZ3BazDznYBs3AlVl/SNxFd'
        b'QVd4nIMct8uLSZZzmfHLhvUCYfV4d8KjE8/jLrLcOkY1VEO54ZWB2duhS7Jz6BxJ1a4wQ+BuL8FSOsb58KjdLgWrsYY0AlQHz4+mZsmjQ6hdkYGOytzw7kI0kUlYoqDC'
        b'90XlaCNGfgM87VimJMjvYcbhLKOJguXjjVqzYupsdyXetYgmMYmwcw61sP4jFqOOacM8OJwMidyZiUM8heSgCR2OQx3waIwHaiehZSQzBef/XRQ79dihPN7dtS6j68AL'
        b'OOVZ9zyV1fRFkTzOMeSCrLYyKg0nJDV7F8xR+MIm2iHyYkJj0UHBcrago8Uksz+D/XYgCEQ78wUfWYaaY2C1h3zZcgaI0RlJFgNrsQ03CnJahzajcsVw2PiInl2ow3Kj'
        b'4g3A1+FwM6P55OKtXakvxyk3fbU7kX3j/KIXN9zz9HEbKjm4cERB/BTFfsnULXGmMXkxh+Iqti0c8fYYiY9b0JgYmcfv+l/fnbzuQuWNP11ds2qsOsVjU0mpdd26UEl1'
        b'8DBmVIt3wpbSrf5vmn7dPVUSrlyulr/5+Q3lmatTfdQtbZHKf+556Sfdj2n3Uo3bs0/NPDrCsjtgfvP89xJupJSfvH39l1eW+nosXZHz6WWfL/a4pXx64mJW0JmGQR81'
        b'ynZ7cTdet6u0KzI/0lk/iyypj9Tc6Xi5y2/MH2LbO35+v6K2dInfpr8ZRkQGylf8cKR/wk/uVRNf3zl95ayZpduqfjg86XMu/azsn7f/edJt2cR5qyfBV7dkzO13uu3z'
        b'tXz2K0cVp25tfPHrmtKrnxyrPDds3UfNscDtbxbTPc1PGyMmHEgZ0u/axZY3gr7+cENDwNHTg/90LnxOZcfg7LdzvmradHhSHvdZ/d3L1679/ONO48f5614tLfX69/uX'
        b'tEfT19/6t5CDr//z7yOX9vjWygff3lM6q8Wrp2VZRVlp5ajJk86UX/d+NeQ+qLPt7VqRppbRfbp/oiuqDkzFLgfVucDteJergCexhzWitXZy2AFr4PYYTXCiDq0LDFAH'
        b'o7pAVAnAQJV4iXSwnWjF4IW+2Jsex8m486iHnvMsQ/vtxLjnecNuTTB2bJV4ZimOf/vx7EFYUXfQ1VETnr9BF+ifgGp1DJDhzhS0ewVubLITrQ6Fa8frElMCUlyAVDwJ'
        b'bWVl7qjJTiIe3BmHA3ZCYACeGe9dalCdCKC2if0nidBeP3+7sEuD2yy6tCAGwCOoi13OTFGiQ2rZk+cOz3qoJc/uf3RW4SWcVdg5g403CAfw9MiiBD/kU2WMlPFmlIyM'
        b'lTPujDd+ykUyxouR4Tbcysjpx5P+ffBLRr+7s87frNSFZaT3lfi3L+PJylgxI5aSky9fPIOUzs+udWd8WXfcRr6Lz3NK8Og0TNkbtV6HJM+mTs1wbg/oo1M9D5zHJd5X'
        b'+zgu8ccd7uhYP+eZWIg6xBWHOk1qcrAgF40UzICnXOC2yeiKmhH8divapNMlwh0zA3GmIgY4JMJqtOWppNTtQd6YLCSl5BAePH0Mn+P2MEll/9UD4x8K8ORyVa8/6USQ'
        b'vMrw+LUJvYtZUWRWpWRGhYWqCjn6ZULwY6CP/Ui0qziz3cHZyFxWC28nU2QbbPkqg9FY6LDZVbzdYDcXmG12XlWcZzHmqQycGcMUcWYeN5pNj01n4FUO3mGwqkwWKkMD'
        b'ZzHzwaopVr5QZbBaVbPi06eocixmq4mn85hLsMCNeBYyxvrYVPRcVBhlLLQtN3N4FLktctgsxkKTGePFWWy5/G/QNuURFitUeRg1ck2VU2i1FhZjSDKBw4hJN0c/e4og'
        b'zEOTmdNz5hwzZ7YZzdHOdVX+Uxw5GPdcnnf2rVQ/Afk0DJZHVlZqoc2claXyn2pe6ch9JjARASHz0XpTcYvVbLGvNORZnxztlNWjwbpCm73Q5igoMHNPjsWt2WauNx08'
        b'QaTvwdkGqwFToC8sMtuiKTsxgC3HgBnPG6ymwsfHO5EpEHCZZjZaCrAqYEoJo/oaanRwhEMrHmEzFx3J4xy2PkeTA/Vo+sRzOox5eBiPfzkKnoW10VrImx+gHW8z/R9A'
        b'ObuwMN9scuL8mL7MwfZgN9soDapcczaezf6/mxZbof1fIGV5IZeL/QuX/7+UGt5RoDdyZpPFzvdFyyxiN6oZDjtvzOMsOZgsVYjgdVWFNuuK/1GanE7AYqNWShyFykma'
        b'2dYXWfQq4jeommq2Gng7Bf+/QVTv7CH6YTjrHYse+ruiQt7+5AROzTDzRs5SRECe5bmJrM2W7GdgTCKX3fBAuebiyIWXslqfoWHORR+p4+NrPVs1/8N858w4imKji1Zh'
        b'L4NHZqBuY362sEBf44kvwsTr8829RPUAIcwCK+rmebP1t0DtOMA/g4nOeciIvpF9KuLqHDaT2dZ3xHQui2NkH7H68YXxmN+aI3f543F3BpE2OpJj57GnysFJDOnuC7CI'
        b'wwLAPs/Q97rpzm6zLSiVC34W9o+t/RTefcd/pyI8kQM8BvzMfECAteCl+wZMnDol9dlqpy/kLLkWG1Gpp31ImrMvmyokNmDVdM5cYCp+pq33nvlfUGhh+H/QmeQZcLTp'
        b'0+XNMGejbmzWffiE/wHEiBlQOyN+7jG8MnHPbxubzVBgfuTtnHmxyj8VN/eppw6uiOZFT0HMMXPFZpuJmOXKYrMxvy9o3lxkiO6dWOMJemX1fUAstNkWR6tm2/JthcW2'
        b'R1m3qfc+wGAy4YZiiz2PJOkWjmSpZs5iVFlMv5XhR+P9rKGAuE2MU2beE0VkjwNGO/c50Xhf0FdkeHz0Y7cCZFfn/tStQIpQoTN+pHDeHxdgV+Y/5yWcqPvInMfsAbxS'
        b'PyoIOEi5lN7oAzvi4Xq8150EJsFO4fppf3/h8D29qDC55XkzEEpsNoTCvdoJIHiGcP49Su1Qka3oJVQN12nUSTHeT2xaRwyXDF4iVSvpRUVAhAeqDklKDIJVIUkpuqAk'
        b'VKtLhWWLJWA8qpVqpmQI59UVqeiA5mG/BHitgrtgowi2wo0iBz3wOMoE6UJQ45NH4Xa4k/bDRrRn5YMDb80qeMB54A3Pm4TjZLjBB1VrUK0WnUxJCmKBDHWxsCrgOXqP'
        b'AC+h43CvDk8+H5YnohqMYi2qC0lAtSIw3EuMdrkH03EqVAYvkmHOMWNgSxrajCpDMMqjNZIYuNffMY5gewGtH/Vw3AjYQIoh6DVFagoD1LBbAvfAXf0dpBwJ7pgM9/Sa'
        b'Ex2CG/HI6pBEPHR0liTOAq9SVqIGdDxfE4xq8WTBSSmocohfoFoKhqC9YngYnUJdlJXaDL1zTGIKqsIDFqHzYICPOBRuRbVUcvAYas3Cgps/vQ/B6eAuepZpWwC3aSeI'
        b'w+LIiREwYfa00umnoX2o4zFJwQMKQVLrMoQz4mrUnKSdIBGjZnqBkIcuwbVU6eLhVViDGtTkziwUhCYWCsfY9Qtn6LLRticlW2wWVKMcHYQnH0oWnYQdD+4yzvqqWeFY'
        b'pA5V6LWwvQjthZVSwCQDeCYBnaOEaHhyTQMMsIHexuTnwApajITWwW35VCPQMbSul0r4wTq1lIJmuhZrtUXGoSLA6AA8jWrgbtru7TZIq0Wt6EypBDAZAJ4bmEAPhmcE'
        b'eWu1XDF6EQOkAXgWVsKDAn5d8JgZg7SjJtSEYeYAeEGN9grsqoUNaJ9WyywIxQgeAvkYnTPC5dk+2Oqm1UpQYyzuOQysc72plS6IHwACsZXG9TetzlIkAocn4WJ35GI+'
        b'zZfBXAbxo9AmOnLX/H6kXDXywISS5ALzQKAWUdLD0D4luS2p9UFnCE8ZTPkuFm6HG+EpOgCWo8OoSzcWtgcHBRA5wzNi4DFHZEV7x1LUUjBLdYmkfkucUCpmYJOoRO28'
        b'2L8M143BXJsLm51sw+pWRimVof3oCGHcqLlOvi2CLY6RBGhTMuwkJhBv7sv47LAbz0443A9WonbMY7cSJ4st0HmhcQXumkM4vBq1ORmMNsIOOrvWjBp72ZcEHnjMZtGO'
        b'JcKx/hFs3G1YEHD3cEESSnfHWMKNllDPh/BRaEsftrwAHhVE1q1YgCUWhjYJEkPrAygKcAO8GNvbb2Q9ZuF5sIoayLLV87RaMTwygt4o5rm4U2A31ATX6xKDUoOxPftj'
        b'az0zRji2HQLLxbAZXYiiLHCdg7aRS7ASsTooUQxcXVi4ORgJxSbWsR60dDNrSLFyRulIIFxgbcdcO+wU4wq0h8ixYI6gAA3wJFYAoiNwf7/eOtLPlxptOqqE5RrYKE4K'
        b'0gUFpJKyYI9ckRm2ZAn+dNvzsx7ey9JLWVQ3bXgquf8bkiyGWwehY9T3YW05aKED49c8HNrr/hZ2oo2UBxx6EW3XURcBN4ck5egfOaAAowSe9AuhXh7tRa3wjC5Et0r8'
        b'6Cp7hQQbFA1ZZ2AtrH/iurf/ILiL3Paiw2PpZZHGvApVP7hz3DuZXjvCrVi+akJXuzKDcoWwBOtiXQiqSian97hxKLzAgAlwpzRxFGqnEkmHR6J1aHNCYFJaUPRsKVDo'
        b'WNQ4bR6NV3noBLr64GoUG0lnpPNqdFsYtlJa8NU+Cbv1audd67J4ctsKu2AT5f9zcB064rx2T+XRZue1+4uwht4dPwfbp9HqgF6VAUGoVSgOOCajcX0q2hSvQEcCcQow'
        b'C8yC6+A+bGTElbwA1y7hJ8Etgi8JGOJ0U2iLRMFJ50rJ7SEOWtiYL1K7GeGJ3UUDtrdGWjgZhNnSSJVOPl1GCw3SB+ZY/zJYDYTbrq1o7zgcyXa6wCrUjX/XAT3siKHW'
        b'0z8Dz9MRKoKNz+GO46AwFjjmAaFsdjyPpYJqE2emw/bQWRmoAktvpn9wkD9mQEBiCr0CxrKYReyjInBOAiGdsndmQiDpxDFONzsd1YoBvLqqH3Yw29F+eu/7VyDc+xaF'
        b'LbNuDdcCQVO2oS2ZTzJQjw5SBpbAQ053hA5osUw6wooC9DjqzMTOLswgmFYF2oETGNyTPo+hvu4M2i5zRJCu01iIBzChFYloC9qBtsGK5fhRC6vg6Qh4RgLbszPs2fD8'
        b'aFgbzmDhS+fDbnhMKIPIGECmNEY7p4T16BBWFrKgCW7z0zkj5EYHA6R6NiBVsIk0s0w3GjU84cm9UB0Nr/2WOO0ch87G3oaOY9ZWoSr2RCqqJ+uqkp1Eeq6m+cgqXWjv'
        b'bARjs6lXPlIPN9AKC/z10sjHMxLUFEEzElQXo3aWKu4PGKiNWAaPB2O/nkRIO4OECrIpi+BFbZgUnptKExEzPIaTCdJh0/bXhi1fAHdiZsRhH40qYCXVsIQUWIfRRa3j'
        b'SGUGCQXt6AA8o2YEyVStROW4ezzabcK903FOYEfbHdNw12JMQ5UCc6Iai706BNXNQq1usC1sfHrCA93LCJqT8VCfsOgPOHUKe6UmOdozN5S6cZkxEp6EuyZhU1kNVsPO'
        b'4ZRGxZoR8GQEbDPHs4D1BegEdrLtgho15GRgf1uLOiQAlIJSuA9toi8IZMZLeVomnuFPLuyIe5zbS5fR+nFiMDfIBW7n8EykTDq8VKNITUG1QXOIgcCjgdhGUOXchKTZ'
        b'CZkCMbAlHVWkBAWnJqdJaCYohxuDU50lIavw1Ouwal5Bp4R6+rgCyjRfWBmLm09LMgwY290AI3sFnsJANFZ0w935OnR6wZO5QgvaQFXMJxVuEVSsAW18LN/AaRudf0ES'
        b'Tno6itEFUqegwN87mTDJDCGw70NH4QkeXSjykAKWCUeVzFh4tpRWEVkWsnESfiP+ejnl/guZf6rzjvcu/cF49MXclTm5vqZB75rvtMCRwXL/zYdaFf94ZVr/FHtiZHfr'
        b'+IbkfUsWj8xcvMtzT/+GopEfvvx12bDJy74xHfp2Wti3n773svY+M+DKysmKgZWf3/7y7JXSW++dnKufbZMHfL5j/qi05CUfv3eq+/U/Tki5/cqa7j/mv/XvS091LO5a'
        b'vvxUt+NC+piP8+f9acvEt84MH3j+d0sjmvf8w+p+rdWw8IvZN/KvfD1q7mc9cblN0dtPf1o5a9Gtt+epucx5x/6wduTR+7H5L7+d88V709zWTN88MCq4S/ZtYtNL/yb6'
        b'ABTX7g3uOXBzyADDv+e0zAlf/ZfY3114+ftJlSe+WTzt/McvPH9x0Me2si/X3ptcNzNx5+ebvt64J7OuZPmB3w8uGVIs2jvjpT2dkpg53S+889rdxudv121dVm7qVtrc'
        b'P0qDX3nbfBZ5/PBrwEfBH8dKf4q5eA9eVn0kKQpxvz3N/NOV0Y25lw6XdL55suTgngFvDvv4p6p/G7f86jVRdv82l1eujP7R3NZybce1uS8P81o172Z2a773sNh2y5W5'
        b'sbeNB2fEn55m/vCTc/JJX/1p6nsNUZmfZv/tnXFf3zUNFN169X7V/G9c399xoOGse9jFF67tHL161Ygb8r9W3v1iX15Lv18WjTJ9enjIp20nz7SF/3R3wJlvr52c+VX9'
        b'jKDYVyJfuBl+Yvove24X3syovDO8KTTgzW1v//nUj0HDp7gEfeBXvvKnH+Ndu0fnb15xtWbnCXlV9J2Dw8v+pizJ+0vnt5P9L5XBg19F5q0qcb1359K73x9759p80e2F'
        b'qb9s0k76c9eXJ7777EZJWsKi0cveqJjUta5h18y/BY4s7d/9o7bLoY2vWeBzaVh9kM8XbnktmRUrNP470lK237nw5i/pt9+79U7ruH8MPfDVz/fOfHrW468vHZMcQwPP'
        b'X/7si7cWvf/O3S+W3Ki5YT/btLXh1yv7bo96ybXJteSFmd98WFVe+JqdXbGj831Z98iuwKaGFbErf0xpdXhsvAP1n/76y+cxaSslBUujxkXfW3hi6R9urgET2ZzJre8s'
        b'09ZUb6v7+OTJSbD4O+nJ7q+jI19ZXjPk1iftt5YUdG3+MrvJUMatPHK+6Ye3c8Nuzrt7Kfztv/96wD9mxd0jJ9I/2H4sc2Tna5kjXistnWUcl3Nn/bt3FXeHfz9in33y'
        b'JdcfRYZbilUXs2dMmfF9+49Xf0Zr701Z8X34uzduJk54d9zPeTO3vzXsur55yJDoyKX3X9T3F/0z5t77zWn+81eJP7i7ftc376nd6UsuClRvclYuYHdCfFWQNGUmGAAv'
        b'iBPgenSMvuSC09ZqVK8JCA5ersYxAWev81nY7PucnW75LsEdPprgxEd1E3A/vEhrJzLHUvCl/dBa5xryEbQ+Aqc3h1Ed7dTAc6hOF+gPoh4VR6wIRO20LCMInZ/0sG4j'
        b'MBxWP6jbUKEqoT5iL/Y5T9RH9C+WkfKIF9BRO/FJyejCIE1qyrCQwCS0Gbt72MUWoxNaO/HlrvM9dTgpDAnCqT8A0mI22JwkzHsFXUGVOrgDtmKsHhaEeISKctEhDzov'
        b'qooZ6QzisGOiEMRhQyjtg0fnoo2aYMKsCUo8MTzFalElR2tFcMbVBC8JL40kpwZ6P3hnZDFvH0Epwn7+EOrAksAJUZHw3hF53wL4xIhF6Moadf9/tbTjP/lQu/3X53nq'
        b'LZcCe1RYKC0ZsZHyhzWyeWJG+CunBSDkr5hhGSUpG2HF+F85w7Is09df+W2Zu5JCDGZIwQj5PpCWnkj/KZMoGaFFGCFei+chM9/3ZNlfxSL2n2Ix+4tYwt4Tu7B3xDL2'
        b'Z7Er+5NYzv4oVrA/iJXsbbEb+73Ynf1O7MF+K/ZkvxH3Y2+Jvdiv2f5kbdmX7gNUjBSvK2Y8mYGMp8gd46vEK/jh1fzue9MCFU9Wfl+K/yW0Eaqk9wl+SpZg64WxlEtw'
        b'D0soJB8xK8UjpKyUHY1/SZ0lM0oKK8XjlPS7H17NG/cPxnSSdul99r5cjGn+VS5WUh6K17LfyT3JCqTYRonno3OwnMcDkahFPWJy5tmrQOa/Lmw1w3k+EDddaisRM8kU'
        b'wLrRt/oopSFqbomGO7Hd4uxhVwA9QQgiuRsAg4tEOJetQm1PvQhG1CaOzEy2Q2byEjJYwJqYBSITS18vFvV40kNcWuDCxXNcIXd3uHCsS1WQc9armE0qg01lJv04lRL3'
        b'yPR6cg6u1/fI9XrhbWP8XanXL3MYrM4eF73eVGjU6wW9fvSgJJMkklT+0QNeGZCxdLMcvQx2KtxRp13hism8gpoCUoM451uEIahJKoFHUtXMdIus+oaIj8PgNdErJq+a'
        b'/effp6I4T+n1xTtfTuUvuV7+ABwsloWfK/r4JcUv7XFbItfisNfaPH/Usk/2aG69HpmQ15w2qeN+Usc9y+XwbYe3rttw8x9nfyjxOD324vurHD+c3dTvp0yfnD+/ceeT'
        b'53b6K0YvZk4O+inyg7f1g69sGPqaxx1VY4H6k+ZF+ucD6pf9dMu2bfRev4CS6L+8tmHOkRubvUyrBnNFUydNaBR/579a5z0z+43jrbMvWocvtT4nvTZF2YYGGmaMf3Wz'
        b'cf3+l70n1Q5a7svfjPG9Fu374ZjADrdTrSfnoeiI1sogq9HlxWso1r2oYlTYso8cpabRy9bP2vex34DFo/6SsPXV73PVt3bnfbz1s4mzZzZnxjffkczVbxU3HVOj3X5X'
        b'Z40rSw6YuXtRSHX+Rxvm/DLk1lSfhWxnXjlboPe4HTed/WTJtbqrc1ctzZ3AqcVCOdxxGzoJD6TjTQDea0QCnIcfWmKnJdplcD088vB9TrjBTIVB3+dMhxV2erZ1Eb2o'
        b'UwSQjRmOJg9f+9REDIcdYnQ2Gx6nUwV6SXh4Gq2HlxNSg/wfBJ5+qF4EW1PgZWwR1DC8/hudtJQm1c9+UOeLddtaaDDp9dTzluIH68uyYYyKeIv7xD/IWE/WU8ZKiYd8'
        b'6kM85pMf4kGf/BCPij9SseDvZHewo6OeWnrPW8amKRl/BqxhV/sy3IBenojF9vTID/X772ETww18aKhkceKWaJFf8M1nvBOJjozXwmpyBoZ3mKfR4bRkWAnrXID7INHQ'
        b'4gDL6qBqEW/G4/KmVg99dbz7+jjPTW+vySl2s2c3b7p+sBu+vPSrwOZRd64tfCklvPuLjRtP5Lxw/sPfF+dfubsD3i+eFeU+78ievzd/fvGLljEbtqjtt/cNunh9Udey'
        b'ceMnfFvituVw4OKO9xq/2Dn8lZsD352RrXah6YhnrA3vP+vpG5pp9ATLBWcN7Sw6jjpRMx2CW3d66NKCUBsZkxbEgsFcP9Qtggdxzw6aqcGN7mi/QJrOkYnVG9ZSwrxE'
        b'w4JDqfGgCwF2ZyEqrILrpWJWNnk4LWGFOHuL4GCVrtd/LaBQs6iecxMKaPcwjCdqe+p/HkC1cC9NtdAWF3hWkyQBk9FORgfQriS454GdDPtvzmj+s8oj/k3Lstgsdqdl'
        b'kZAkc5M7y10DRWANWCNeww16qO2qHpHVbOsRkxrLHondUWQ194jJZSKOxxYjfpI6uR4Rb+d6JNkr7Ga+R0xKLXpEFpu9R0JfEe6RcAZbLoa22Ioc9h6RMY/rERVyph5p'
        b'jsVqN+MfBYaiHtFKS1GPxMAbLZYeUZ65BA/B08stvMXG20lxVY+0yJFttRh7XAxGo7nIzvco6YIThMvcHjchX7PwhZERoeN7FHyeJceup+Gyx81hM+YZLDiE6s0lxh5X'
        b'vZ7HIbUIB0ipw+bgzaZH9iyQPYwjh2jcePIgRyQcPR0m8Z+bQB7k9o0j2suR81qOxE2O/D8FHDnJ58jZNBdCHiRv5ogKcwHkQV7X5ogf5khVLqclj1DyIP9hBhdGHiry'
        b'IIrJEe3lwsljInloHroDIh3XB+5g+p2n3QEdcVf24CX9Hk+93vnd6VXvDs55/D8tUdkK7SrSZzalqmUccTYkdzBYrdjXUW0gBzc9ciwKzs6TW+seqbXQaLBiKWQ4bHZL'
        b'gZkmLlzUAxY+kWz0yGKEFCWWeYC5GIilMpZoHFjj7cnSzPf/AXYI3rE='
    ))))
