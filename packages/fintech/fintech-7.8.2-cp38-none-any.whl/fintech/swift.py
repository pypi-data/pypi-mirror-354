
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
        b'eJzVfAdcVFe6+Ll3CjAUUQERFUdFZegyiIBKEBu92LAhDMMAo8MM3pkBW7AgAlIFrNg7qChir8n5kvxTzCab7G6ypLnJZtM0yW7KJqb4P+fcAVExb9++33u/95wf1+GU'
        b'73z9+8453+Uj9Mg/CfmJIT/mSeSRixaifLSQy+Vy+Y1oIa+T7JfmSg5wgk+uVCcrQ8vk5qBFvE6eKyvjNnA6Ox1fxnEoVz4bOeSp7O7pFLMz4mfMURaacq0GndKUp7QU'
        b'6JRpKy0FJqNyht5o0WkLlEUa7TJNvi5IoZhToDd3j83V5emNOrMyz2rUWvQmo1lpMZGhglmntMHUmc1kmjlIoR3WC30l+fEmP46UhKXkUYEquAq+QlIhrZBVyCvsKuwr'
        b'HCoUFY4VThXOFS4V/SpcK/pXDKgYWOFW4V7hUTGowrNicIVXxZCKoRXD8rwZ4fZPe1eiMvT08FWKNd5lKAMd5GejNcPLEIdKvUuHzydsIgRvVElStL05yZGf/uRnIEVF'
        b'yrg5G6nsUwz25HtxoARJJyE5QtmGE5kZyOpDGlXug6EaqlLhiCYpHSqhNlUFtfFz0wLlaOx0KdyE4/i0irMOIUPxNQlnjk+Guhx8GmqSoYZDingenzHCPi33iDgHdCMx'
        b'i/KDIxz5D/iRN8BGN1cpIXTzhG6uh26e0c2V8ja68/uie8RjdMeIdH/pZIdW9CMUKLOTNrv7Itb4SgRhhkVBvmUHvOGYJTa+P88eKfMIoOxsQ9jU/mLjvpFS9HMM4WpM'
        b'tkExsAi1IgOdttx1sPROxp3RCP1l7D/4C+N+H/01Z3AgHe+N2smdsUPKEP0z494VcuZlItY8Ycw/+jX343y/RrUDf53vhrxQF7IGkI55AQFEAmfHQnVwuq8vbA6OC4TN'
        b'uHWOb0Iy1AcExQcmJHPI2M9hMr458jE+23UTHUb5THmM8iQ9nOT+PU72AO3hpKPIyWfTXSLi+QiEQrKTTg0ehqyBVC2axgQTAmr8E6EGqpLS4+ID4uei0MTZ7qGwDTfP'
        b'wdV4K8qX2cE+3Ka2upMZSZ5wRo0vEui4FcEJaF2Oz+Za3UgPXCdTtqrxOdq3B4Ubl01ebaWo+OGDwepQuto2NGqJFp+ETitVdLcJ+Ao0yRAKQrMsQXidnOH557WOCTWc'
        b'L0Ku2U5twxaJcuQDBxb1R3FU4kO9XDOR/jXzDKlZQ35/Oab2i+xPs5fmJWlu5QU1+mriNJ9nD9AW5Bly7mQnaH6Xp5oVr1GlJWpO6Y5zbQPzP81N0CxCjdo4jUnXKN18'
        b'5MyxkNgFNaqhynlR38S+kHLUZUbD5dOxzzrt1qM5Ce63fyhU8ZahFPedwRMcCZdUydZAPyJoHrnjCunKZHt81d4ymEo0XUk42YKbYDPUQw3R0EgOdxTjdhXXxfuqVBKB'
        b'SqTXgyePex6T8gTTKp1RmSe6tyBziT7PEt2lYL4rK1dj0dFxZicq35FOnBPnytlzvpwg7wahknTJijUGq67LLitLsBqzsrocs7K0Bp3GaC3KynpsXRUnUB0RZPRBoYyi'
        b'8F0o/A9ceTnHcwr2FN3G+SLc7h8X4JeCa1PjpfMD4mXIA9ZLB6caZ2j5Xqon7UOfie/o0WeeeQYJ0We+R58lTJ/5UsmTPGI34If1WZ7CtMoeapZBE1F5fAKuBqJAqAln'
        b'7dAyCW+DJmJg+KZXMAo2wXamuNChgFNM3eAK7gxCQbADTuj/OHe1xBxEum+XvP9F9sJnGvAOfK6htam1rCNuZPnlsvjd3It5VL2c8m4bOLS97VuNfcyFsSrO4kUmOZPF'
        b'/RMCoTI+KUWGHHEHNCziYQ/eu9Qmmr5kzjjf5SgKOM9g0liYhKmaIz8nTkrkKyh6pCtl0uqS5epy9BaBDhKoR1LxvSTKCzR89RIrne7fI9a3HhKrkor1JGz3tYnVATel'
        b'sigSwKEhhVK8BR8ZZx3EZI93Q9tofMNsCQ+RIj4HwVE47WH1pMw8lA9tuBxvp30c4nUIWnELPs4cQfpyfAlu9KNdEsTnEy8xO4OJxjzGy4hbzJYJFJwRQdt0CVspFs7J'
        b'8FnYRXt4xJvIDNwJJ6zUrGBnGKzDx2CnGc6Np0vhMgSd0DyKzRyahK8sj2JdMtK1EcE5vBVuWj1InxGfyouCS2aBTSNAT+JTeCfTheX4iJshibihcRQT4uKg03GSSNgG'
        b'3GC3cgnrIqgQj0UgboHDDKIznMWbHHGN2aym89YiaIfTGSKzNi5YYOfDphGa8S4El/BxaGbTBo4djk+pWZ8d6WtBcBlX5onTtkMbPxHaoNPspCDrwXkuDPbFsWnjSKQu'
        b'C011FBj38VEEF2fgTnHaVR2BX53kCB3jaScJ5xKoS2G0LSN8xBujHBWhlGzYxjnMwOsYQLzZddosvNURLjCyoZzj4OgEBlD7NO4swgfN0FniQtE4wPnDGdzI+nLwcXx+'
        b'PrSaHZzhDAV5kwuHCybWNxhvxeehjHdcboULxE1DBzc6H06yPthLqKsZRNjlKFjovB2cN5zxEQnYBtVhcCPVbIGLjrSvlix4ciVTnyxc4YevOpldnAlHJDJu8jyoZ+pD'
        b'0K0blELaXTgkceBiUuEQo0ufCzfz4SrpWE7JusQFEbkcFo3+cDZuh0NyR+ciXCNFklFcTEJ/1uMvnYGP4iqqHURzihDxDXVKBg7OKeH0UjhA9DdMjvg8otpRBAOmHWUk'
        b'pbqBG2OoBshEXTwL7TFsXoQe6vCJSDN0QGc/ysR2LmzaEpEVh6c8PRHOmOGCrauNU0OloFKy4LbENJAL45Hv7XCngvcVuizWOE3izkXwyPN2uEEdmd+qFdOZ5EHcJB5F'
        b'3A4PmKdP9gxmjetHe3IxxFfcjr4Vcjj3kxGssXm6FzeNR8rb0Ybpi4rWurHGglnDuDgeud6OPik5nVAYwRprY725JB6FkOmO2Zq4aazx9/2VXBqP7Ekj/7vYNxNY48WF'
        b'I7k5FM9ow9BvZzcaWWOUwoebT/GMvmVIkjQNYI2FljHcYopndEDxJEP4UtbokeLLZVM8I285pKz42o41vurtTwIEiiGNadV+f4pmjXezA7gCinzkLf/xM4IyWaMsMpgz'
        b'8Cj7duSdCROGHRWThduJ47giSlFkjWv4jJ32rPG90lCO+NS025EBeSGxwmrWeCVnPLeCkhl5y7M6uHABa9Tkh3NreFREYAZ9v7ZFzDUOCxHcOkp7ZIDcl39tHGt8I34i'
        b't5FHcWSke4ndUQVr1Kknc5WUIZGGuG0rD2lYo+D3FFfDowLS6H4zfruzKA7zFK6BcikywOGz0YHiyFjXWK6ZR/MJ8tr3retnssbMoOncDsq6SMOwl8LXp7NGf+VMbjeP'
        b'VpDpK96KuTeKNcakxnH7KT/H1wxeNm+plTW6rEzijlPWjQ8Y0Zmg8WKN9+1TuZOUdePvTJHkZotaV5mRzp2hrBvvZP+d+zKRIZ/EzOLOUdaNdxr7uedHrszu8IHioWq4'
        b'bnZUUMNz4mIiVVa6R8iD/Xyam6Pg4kzstD83OaOAKft8aJuG28cRJ32xxCxh/sIfyqJEF7RbAY2jZxM/Q3w2tftmbmTOHJWULR7s/P+43RJC5cRbQ7/z+X0pa4wY+SK3'
        b'nwTz2xNqRt1YcsLEGt/KeIU7LCFaM8Fp6J+L/ywax4DUW9xxCSF9gpOTNsXP+8n5NkmCxV0e3dOgPNl/YvfyWI5CV5ajR3OUMSlWusv09RuLq1OhjiSEVfHJQVBF0kY1'
        b'iaHZ0rGDRaQ75/I0xbF/2yU7yX6RRtTAphh75EoapaZsp2ODliIWCHGdU2BicCLUpZIcDB/B6+1hI7+yAJdZaSYC68l2rwZ34nM0/4bdcJFbQMJ8OgnJ1HF5LoIr/nJo'
        b'9yW5a2UwyVWc8iX9cEMJc7hTwqACd0pJQN9L7BlF4Q14i0AZxpCJC5NRIrP3J2YbMtZmi42rBtshkpLa7/fNDogo0CAGR6LH+9UhBNMd+BDCjUijx1usdGc3X47LE1la'
        b'XE94UZOI64Pj8SlfDimnKC0yl5Ii0VcfwhtWq0nuSOjYg3AzyimFJivNveH49IH+vsX5BATdupLNVrwUDVRJoGZ+KVsZrxshoTsMOAitdJehlcAm0Zc3psBBNT5LWHIA'
        b'ziG8DxlwawRbDm/ywQfUaurUhyBCeT4JZbvEjUyHM5Sp1XIEVXCVaD9aOqNYTC03+EC9Opx82ZhHqES59noRv+v4mDkxYY2J4pYiSsilSBJBMqgtIn6783CzOpxgsRWq'
        b'yFYC6UZMYGIz4N1eibgBn0oi04Kh1p9DjgtJ5CgqVfHMxqDRXaUO59EcAmQXynPFLWzrBNtK+qnD5Si0CJF8In+Itxhmmpa6QXViLOwlfJIhqTeHD8IeL4aCN96XoQ7n'
        b'EC4vIeigAjiAt4uaU9VvsD/JSJqoSKAqBZ+SIqfJkn5qMU7ii7ghWY1JcM+B0wjvR4Z5eDNbjeQnCqhO6o/XJ9DtjgRucLhF6WhNpkAvwjGtOSk+PpmeS/RsL+PxJt8g'
        b'lV9ykCqQV+AjOnwUjuLDvr641cNfhZvhsL8bbvZwh8OD8DGe5Cturnj/3NmGH+7fv/9tElNDTxSXbfh87kxR46bPhy3+KUELA+OkSBrD4TYlPq9yY4xbMD7d7By/UrBS'
        b'D7SXG6VYzBRiFnTgeuh0gT3eYtcFTuUUxyj18JBBpzMRRq3Yc4Pzd5IzubvnWM0uM0IFq+ixhuMdYt6K906ESvNyvAsftSpoanqVU+KmUcziQvE5OEYDfi00l5D8liVp'
        b'Izxi2MRS2J1CUi1oWwPnnDmWNoWWQCOjyS8m09ElGl90xPXErS7kFuENa1jH2tzBZosTHFOU0HTwOjd0EN4k+ufNmmlmi2WxooSusp5TenuLzvYk1KRDp8XeT4BzNCu9'
        b'wQ1Rz2e0uhTNNcNZC1HxQ7EcUX6oN5FsTwQWrnC0T8MtzmQTIZnAxaXniJa0yYemsJm4fbkTxXgXNxaOThXt5RTeF+/oIot0IjsTyUQuHq4uE/VxvQMRamc/aIHLAskr'
        b'JS7cBLxtvMi78ihcTfpw81w4SwPISG4K1HqI8w4Rlh43L5/oxtbCFzhvfAk3M7mOfLq/WTEpUhRRI6fkCxja/oUmRwVJzspph2QAFxKqYLjNg/VkK9Ekhw6yRQpAAbgS'
        b'TjO1n0B80RVc3U+xHG9eUMwhKUnXcC1sghsiG/YVOzu6uCR1kzQLdumvVWVKzVtJVKnd6JfZODn1rzFOm+7ujOcdS9Z81fjxlz98rt/y+sgR0+JnTu145/KUKXG5rQ3H'
        b'ohpmHZ3h5vDhoPSvHX9wbravVzu/c2uF981vuvYeFvLTWl46YSfHQydt+sXT86W/xmy6c+gOfjfuraFeBZpVKfG5U/bV7X+h5diOmS8vDPjqUNnoNLvIX9Ky3lys9VzU'
        b'vDlunt8rrR2GhYd//DLlxbiSiMi/b3u+YlXCnueuHz9zp+BAyMdDFi1fMvTZu9UNWbHRzT/X5bbGvZz65+2OJ5d3NRUciVsaUDHglHzMFsuY96qfL15d/fZ7C/1rcl3+'
        b'oJ8cVeg7ce6f6g1ph/ELseH5Q4W5H8zddPd+yE8h7789a0nrK/vqykvcvx/qefUZv3d8vt2eOXzD8CHFkuyJ9rOXnT5Y+tXIe9vXXeuYLHX8PFz9ytwfit8ZtX/YPtcf'
        b'zr2y79m/vpG/e7zq7oWIC++vHPX+0fCP+y/KHDY2tGVv2dT2PR3ffPZqA9zK2nJ04VNffP7WiiE/hFQovg3PeH3Pd6kDJt+N3x609Exc4lt/H3PoF49j7XjwL6WvD1z8'
        b'zM8wYYTxyKh/fqCyZ1vyjNk5UI2vRQekEIcD9WRT64hPEI86O5p1j4Wr+f5B8QF+qiDSSZwxypnrqZQuSR3Muhc7wFWyGd5MwtSGXqc4uHIM64ZjfviofxBxaVW4MYHA'
        b'luM6PpDsNmos1Obj4Dy0JAb4xkFtIodi8TZ7svTK/PEWanILAknki0/2gwNRyXZILuXtoROxo6W0krH+cfj81AA/qCIoEVdZL0EDJ0qgxXWShRnyYdyEzyamBhL3fbU/'
        b'X0wspRJ2qOwfPV140kMle3L/gxOJAeKJhEXQGM0a8RCdHUysoGlOrIKz5+ScG+fE23NOnAtPvklo2wBOwdFjKXtOwX4GcPL7UvrDu5Lfuj/kO+8ifucVdnKOvy/nnchv'
        b'HrwrgSeVS9nBlgd5ysnHk8Cn3104wQk9OOZy6o1ar6OQJ1On4gTnbvoYqKmo+1DkplvvQxFf0hKtVtmORIJVvnCNBDX/lKQgUR7+cjQTn7TDzZ74gooTnVQZnIY2DW5P'
        b'jA8g6YgUkegHlQsfyzqdu5PDODHrpCfp6PGz9DznniyU/80sVMJOfqXfFRLACmWvf2lUfGal5uELD3aLsrJIp0yeExkWojQJ7Eto0ENTH/ol3qIUdBarYKSwDHqzhYLI'
        b'0RiXKTVarclqtCjNFo1FV6gzWszKkgK9tkCpEXRkTpGgM5NGXe5D4DRmpdVs1RiUuXomOY2g15mDlFMMZpNSYzAoZ09Pm6LM0+sMuWYGR7eCiFlLoNAxhodAsWNOcZTW'
        b'ZCzWCWQUveexGvVaU66O4CXojfnm36BtygMsVioLCGr0ginPZDCYSshMCsCqJaTrop4MIpDwMFcnZAm6PJ2gM2p1UbZ1lb5TrHkE93yz2da3SvXIzMfnEHlkZ6eYjLrs'
        b'bKVvrG6VNf+Jk6kIKJkP1oslLQad3rJKU2B4dLRNVg8GJ5qMFpPRWlioEx4dS1pzdEJvOswUkb4H52gMGkJBlqlIZ4xi7CQTjHkawnizxpBreni8DZlCEZdpOq2+kKgC'
        b'oZQyqq+hWqtAObTyATYZcLhAsBr7HE3Px6PYk8C0agvIMDP5zVr4JKy1BpNZ1432dGPu/wGUc0ymZbpcG84P6cs8Yg8WnZHRoMzX5RBolv/dtBhNln+BlGKTkE/8i7Ds'
        b'fyk1ZmthllbQ5eot5r5omU3tRjnTajFrCwR9HiFLGSx6XaXJaFj5P0qTzQnojcxKqaNQ2kjTGfsii10z/AZVsTqDxmxh0/9vENU7Z4jqCWe9Y1GPvysymS2PArBphs6s'
        b'FfRFdMqTPDeVtU6f8wSMaeSyaLqVK4NELrKUwfAEDbMt+kAdH17ryar5n+a7oCNRlBhdlJJ4GTJyFlzTLssRF+hrPPVFhPisZbpeoupGiLDAANfMZp3ht6ZaSIB/AhNt'
        b'cOiIvpF9LOImWo25OmPfEdO2LImRfcTqhxcmY34LRn7xw3F3JpU2HM6zmImnyiNJDO3ua2KRQARAfJ6m73XTbN06Y2CKEPQk7B9a+zG8+47/NkV4JAd4aPIT8wFxrp4s'
        b'3ffE+NgpKU9WuyyToM/XG6lKPe5DUm19OUwhiQErZwi6wtySJ9p6b8j/gkKLw/+TzqRAQ6JNny5vpi4HrhGz7sMn/A8gRs2A2Rn1cw/hNYf0/LaxGTWFugfezpYXK31T'
        b'SHOfemoVilhe9NiMeTqhRGfMpWa5qkSnXdbXbLOuSBPVO7EmAHpl9X3MWGQ0ZkYp5xqXGU0lxgdZd27vfYAmN5c0lOgtBTRJ1ws0S9UJeq1Sn/tbGX4U2cVqCqnbJDjN'
        b'KXik/OvhiVG2fU4U2Rf0FRkeHv3QsT/d0Xk8duwfJ5baZBrYoT4KCd8aXLpwuHhknjqSHWAqQ+RzSirSc5B4vLtrYHYKtOFOssWdiCbi2oVsbI2MHa+7hnh8slCS5o7E'
        b'k9iG0FG2MhrYhtcjLTTCbutI2tDC0RN83OyvenTXOmK4zMuIO1RO1tF0uYYR+AruhEtQHZwQH4g3ByckJwYmQG1iigyNg1q5Pxw0sCNtXOup909IhrY1Pf0D8F4JPgPn'
        b'B7HKkAHQhFvVEYkJj5x5w/pAdl2xctGaRHaoja+YHpxrQ9kAsa7koC8chWp/qE1OCCzBx3lkD5d5vBkOBzCK4GzoYg3sp9DjoSaR7MmhPjgOaiVo+AAp7DDDCVYAB5fh'
        b'EOztNYretVTR+w0ff9wEG2ST7IutY8hApVT20Ch2F5GSzCEVvoZvDJbhXXAFWhhMfBq2THpoYXrfQIb6ZLvDRVkMPob3sFsNeziE6/yDoJYADCKsqgpQyREBdGoItEjx'
        b'oemFjJGLx0G5bVB8MmymYwa5462CNAQhsRbjEj7hpxzat+ik+DQ7jpSRURfUobSyanspXodyp0azCyYFQfsskRM+5/KInPDBWKY1qXgd3qcOlVEtwQcWoQKCSiuDuQAa'
        b'CP/qyXpNdkRXUcgKJ/E2owNfnAzbBzwm2hK4yY62vfrZ2UR7NOSBaOPsVLx4S1JenC4fqMZni+SIS0K4fXa0eBy9E2+BI6SdnZz7GNAyXIbr2WHsyoGjupVhPJT1KMMl'
        b'uKCSMyoCh0IjGd2sVhdJEJeI8KnxcJEd8Grx5jmlC9RqOCND3CyEz0UTlrFT6W2wwRJNr3gEMiWVyNVroFiOliqHBj2ZcZbMmIfwBe+JzBaDE/BxtZoWFB18+imC3AGN'
        b'CKcd9rur1ZSBhzJhPzIMh3ZmpFmjB6EAaqRL5rqscPJBVlfqE2SueNtyM4EyHU1fDpfZyJTE/rTQNCJEvsWuWbcaqSRMeLAJH4Gz9Gqkll79WPAZjlC+g8db4coEURTl'
        b'cI2IsmZxYlCgHxUvbpeifvMkBqgayg6hJsBWKKcHUDIklUIbHOTwvpWwh0iC3ah1Dp4WAZseMA2Xwy7WEzkPzsKuwb3YBvWJTB3tPD3gZtqTDC/V2Sbk0BD7JXDxAW8n'
        b'4ErxmuBirgL2hffiLlyFbcywnGdAS9+mCsfwYdkkYspi0YY/cW/bbJLIwW1EFDugg4EI8BvxRDOOlxAr9ieOgd6PeflF2USWm4YMcF1mpVVu6cTTHunbtFfh07IYOLOW'
        b'iXwYlIWq1dTY9nnDPlSAj8MF8bZW44KIXDxDihvztwsRSOXGvFX4otLE+MCUIGLevt3nt3AErg3BFVIi4uP4JnN6WXgrPkqvwlSB8bAOtkmRgx2P63ALQZo5+POZY7pl'
        b'yQ0jkoSdeD+buRLW4boeRUnM6NYTvH4p0yR8A5+A/bgNl/snBCYG+qXQ+t5++RId4dB+5gAXWnDZw1ewhHH0qg8fIA4rSYoboQkOMC5BeSacHVvc94WtReaCGzMZUgGz'
        b'lxPPMw2uPeJ5VHCdBZsRuIzoJnMiuK53oPHTroJDMoLxTmhmsWIVPofbbHfb+OxgEifp1fZqaGcaSQywDu/094XNRGInHr0BVqQyZOAcvowPTbZ7zGmtMjCfpQqG3aLT'
        b'8uMe+CznEWJZTzter4fqpO57zPwoDreE4m1WFeXtOlwJhweF9bAfVxGTgM1J9H4gkTI6FG+Xxy9yEAPb5ig4SgiJC0jAu6EzNVCOHBN52AsXbYHvWj9Y7y9etcLBoT23'
        b'rTNxG0MFd8A1YsfVibYb3LXOHD6ID6eLeO5bOsOfXeHjfcruW3w/oiOUTTkrCZ8fLTbwyObhvHQsUSVbAdMmYpAt3UpmxWVUy1rwOoYbvb7e1a2f1dBk00/YhxuZbzPj'
        b'9bE+uY4kVZmNZsPeNcx1402wi18INx5RvKfwBeIp2N33ediCqzRQY3OK+BrRD+YqLuO9sN6R1qBCqxTOkLwmFWqYK3YlmOz1IyZE6zsDUSCXwhAU8BWnB2I4g9u67WDW'
        b'ILECZLoDrZsICSmOzn5PvQwxNcTrYDfs6VP31+IypvqaEtH+NuKrkcQMtpNwiOtnwhaUtXammDftwNUZfasybsC7iC4vg3LR5W7EW71xZwgtPz1uxmXIhPARawa1QBL9'
        b'rpmJlkFtfHoaPhsyexZUsrrxoEBfqAz2s92Vz6aaURkwL45KcsVYpivpcQG0j7iWxLlpUEus9ubq/riW+JZ6djm+s79UzC3D50f9Va1DLD/BO/BF2NOHSuDjQ6VjYddK'
        b'W5SY4iWHmijcGUbjdTqJEnCsu4KvjIiueS0+QDs5Fifa4dQ06zgKfWv+JJICVsbDFhJpm3FlMXnU4s34VDhul+GzObNkQy05+Px4jkhMvmDAPPHWd/eEVMLDpt4Ar8IO'
        b'EhCZAC55LkgU6yAc4jkkz+L9JBYWCEfhenxqMTHhR+NgBdFNqhpxKwN7NINIq6LHQ25YICpbay5JdqrCe5GZhneJueZ5XGV9LI/bOlRM4+AUSffoGyIkEm8c+FgmNxIf'
        b'k4ZA5xKVlCmueeoSfMVfHb6chMUEQlyxs2gD16JhnzpMTtO3WWOQDjcQ38auma/gbYkBgjqsmHAjBuHWGSsZugJuhvbBkwi2xC5YHD0Lm0NUHGNTIUkLOjKXkE4iCG4G'
        b'SaZwa5CVXm0VeQ1zhFpiu3VQrYGKYKifDWeccUfYuLS4bs2bFThv1qPqRESyTwG7oBU6xRTuOtwcg7dH4BME5TVoTSzUisW4e3AHPgi7gvCJcNzBI94DEWd1Hh9jQdd7'
        b'tCyP8P4EibulqHQQPmOlNcg+07zMrGJ+lm9cgB8zwAzb4ksdxOUzAu1IznN9gnUClWTaNMeUZKgNTCucZzMQqMqIS5gbN0ekBbemQWVyYFBKUqoM4WNwRoHLS0fb6mVG'
        b'4kMFcMPV9lpBED43Q9SsY2tgD1HXU7T8e+fMEQifmB1MplCi3MOgJkz+qGYVkkyJih2fisBHH6jWRVq2ZkvSbsJWW81wCXHanSVwgdVyXMRVeA8XVurByB9IHOg1YopH'
        b'/oP4gSsyGaYOpXiTGS4U9ZMTUFUWFTdmIl4vhrhL+DJUirEFdk7rCS1DCKYsTjaY/R5LQ8b72ZKQ2jhW0qV3qRnCm/PJ1xWlf7TOea3ebbpbe9Z7k9978+pE9cmAMtiw'
        b'/+q6n2ell0bw7SfGLRnXv+n5Nx1Xf3r4oz+tGDnXQbNBX1sR2VK1M2VS/36b1HYf7mwae196H+GqsqzrezPD+7/xWfvpG22rvvrj6g++SHhtWmDpG+9gxwFLPpzrc739'
        b'26M7pl1MNLW9uDOhbuv1+ar8F94Ykp931sNzfKv7X86rD50ulme7f7Yw5dwvQ+Y3jZl9IvDuqOE/Pfe8m/vLv/7l8C+XE/YcvhT8wizF2LwXXorav/G5+/sKp7wU9s8z'
        b'C73Laj0Mk5Y7/O7YVC7Ibvv61TMKt7t1/PLW6K/fbf94G967xvfrTM/NZ5/PXzem7We7fI/qFSMLX7gzoHPt+rshE0+dabni4328tDLhe9l3ivHznrE7PuRtP26eRXm7'
        b'4/DHrX8bcuPZT25qT9j95Tu/S+5/CzBXPHNq/ReDFO/W3xomf0vyzzERhftCJ9yuDFo3GRtSamfGnzDXn37xD7/uLq+oS9n+9KWXlmbdOujlcfcf727e+YHh/OVXFQFX'
        b'PIYNUXx+79wddLP8u00LvlPlJGwp+6icL+Ejk+Htfh43ler0D9a+FGX/56RMj4A33pl+J73/9rv3vBdsv3v35V3vrnruQ/Otb65n3hyvXmX3z3nfH3jlx6To9In/nKr7'
        b'5ITiyqzSZ8ce/8OGZfVTFy+b2u5+6pv3FloaP/mi9tiCpGP7HZy9r/y92jO1M3x/7Ken3b/NiJ5y44OP15iiym8t26/eul+dMnzapi9fyXtqz/Or614bvaYdX/7m+NkL'
        b'NzPuLogd9Iz/W4k35wy+GLZsxLyqO/LcpVUrJAtPj/7dtUFh07967fw33Opft36xdnlqx3B+z3OfzzTcf01Aa6r+/tHZsreDrr792cSl3ll33O+lpdz61LXkI/cvXxj0'
        b'jCrz1McFz3z60abnU8aNK+4/b9PVCdJffWoOtHzm9bPn1b9/bnzvlwzpWo17tOnuxW9DM17fnzNs5vcuM8u/lL6PfsePmbvjx2vD/ta5O0UzJ3n4Tylbt5zMeWv95696'
        b'rj3yzs0fvnwP2j+6clx9Y8qIpw9s/OrHvw75dnv/pwLcBo9cGzR9RdvPusUjzpqmtxrvvqko+Wnx2K+XP92WVu/93u3K1EOKwHvNq8/NHHK75unn3s3/NL3zm+OTXK5V'
        b'/TTz0OnPvllXMeXplv45wt8aX8/xbRj1/Mub70w+Ob5r3IjqiWW/RH7UNf37vyz7tf7Do3EX70sqp+th8SSVi4Xt8s+PDxELR2iFB3V+xHwH4Qtz4Jw0LhgOsVeIoHGR'
        b'1N8vSEUMGB8iuQNyWMDjI3hLFisTgW1ykmY9VLviqdTCDekSxwUWFq6vxXK2NRbj/bbiFN+RrE8Hu/1tlSmT8AbiwmhlSsZQC3UsS3F5HlSzghmj0KtkBqojRNxbU/r7'
        b'x1GUjj1WoUICZAurURk2C1r9U5KJa6p7KgQR+Jf5kgUxrPLF2UWaSBxecCBuNCEkL+GDxuENjKTlniRWbchOJFj10NQvRJIPrfiCRXxPwBe22FICJ9gu5gSKlWLfhVCo'
        b'8mfcgg6SqcvxSV493INxcg6+FiC+mOMw1vZqDk8CQMsKkaCrsJ8kOZ20IAefKup+n2sSyUtuSCXyKaqB/2plzb/5UDn/1+E89ipRoSUyLIRV7MTQGpS1aL49J7V9FKw6'
        b'h36kHM85cQNo1Q35X8HzXJ+fbxUu9qyqx57zZJU6dKwn+d/lF7lMwfX+iFBcxHlPgid+vpAPcuGUHK39kXKunKfElXNh9URSbih5uhEorrzrfQUn58TqISmrFCLr8k48'
        b'xWaAuDqvYGuSH57WGsl58uFGkhY5xUbEicyV82JtkoJA9+TcSL8XgUtn0Noll1/lUpECF767ksmVd+EZDF7oR3iY0l16JKXnyb1Kjv7r8lNxgmu3BNlajVRytAmtQ1/7'
        b'PPrGli80lNqqk0gWcAXqA2lWh5BXkYTktS2LHntvjqpADAVJsyIdfScbLeRzuYWSXF4sY+9yZSfjrGpImC4IJuHecPGsnKmTYCsC0uUqNUaljvYHpaikXfZZWfRyISur'
        b'S5GVJb58Tb47ZWUtt2oMth67rKxckzYrS9TRBw9GK80U6wl2rLjMnmdHDlF4X4SjC1y0ODpQGgMFm0kGk71nOVTIZYsyVdwM/fGWCM7sReZGXiubXH85BdJcp3/wTefA'
        b'iY5//mjj+Ds/3Zja8OkPSBG7/cMX3bbMWufv42X4bPKov9v9OP/OutfDzF8NfXXPj8IHFUdz/rFlWt0f3lF+0XFl5B+Xtr1z02viN0lDxu4SDvzwiZA85f1Bl/65c7sw'
        b'6rsop9FLfJ76uMmz5PCLL/9wYPqIxp0/BbxQ/uwHm3xOT87UTfr9+Zj0w25Xqz5M+eTcoPm30qquP3c0oTbKede5go/ePPBKgPlW5zMjE7+dn1c+90/z88uSL7ydV5H5'
        b'/dufrJtaN+b6NOGWw7Hdy6M7BiYmFh65rMt0Hhp0Kck8bPYE2Zuhz4f9+PmipVt+V32lOVT92dMJ73T93vm9P5Sm/W1Xy9uvlv7oevRX5aUjwx3vHdg8x2fg+hVu77/S'
        b'Ly9h3tyyuyqphSbwnrBFMgY3kZyf7CsiENTNKLUMJ+3JcPzBW6y0yLbnTVZ74st3Wui+sYD3cPTDG0bSdJe4+p73XYfTdwROx+NNDFK6BZ8z41NxKYGxmT3ZZn9ooFcE'
        b'h6CBqDfT8gH/jU5UzjLaJz+YcyT6ajBpcrOymGcsoqbhQb1UGOd9n+dpvSHxhbyrvasd2c6IH+7f+vaj3Mnm5X6S27ulUi/ruxat4TlhULcBEKPjiVU8cCP9/3sYwwme'
        b'PeZGF6fxWax6vBP0qGOBvURcHbiaHopAVWoS2bzU2yEXKd4xWDIM9kXqJVcmS8x5lJV1p4a9MM5lQ4zrpjfbf782r8TZknNk0+0D1/Bz80/uOWIZM3y146XW5zKun0n7'
        b'48n6eat/ynt1UNbsH0onlE9v+3Hurl8zJp/bGBJaXrd3lGTsbvWgdp8ZY4z1I4Rm01uGjqv3Pun3/Ouel7TxKjsL223vcJjG3kpNxVukbKdkR4L4WR6O4xbYZKGHnstm'
        b'zE9MDYQOOig1kCfKdw2fgGoJPhAJnUxHo0vwRpEyepxGPCelDF/FDQMk3rDNh+UtWbALb06MT8bHSHZjK8wtWiwmXOdxDdn70b+aoI2z/dEERxUPDe6wjiVOeW7L2d9U'
        b'gNrpvf+mAj3tY4kP1GfAVf8EGS430fN3sje+gcu7LcP7vznH+HeVR/qbtqQ36i02W6IHG8jZvrv+VxKwFtEPEgb36LuyS2LQGbuktAC1S2axFhl0XVJ600oCql5LnrSI'
        b'sEtitghdspyVFp25S0rrULokeqOlS8beje6SCRpjPpmtNxZZLV0SbYHQJTEJuV3yPL3BoiO/FGqKuiSr9EVdMo1Zq9d3SQp0K8gQAl6hN+uNZgutPOuSF1lzDHptl51G'
        b'q9UVWcxdTmzBUPGmu8tZzKH0ZlNEeMi4LkdzgT7PksXCXpez1agt0OhJKMzSrdB2OWRlmUloLCKBTm41Ws263AcWLZLtLYTT7/SYTKB/JUKgx0wC9a0Cvb8VxtIH1XKB'
        b'HjAL9GZDoH+NQaAn9QINiEIwfdDzVYGquuBHH/Q1dYHqtUDLlQU1fYTQBz2iFOhL9wK1aIHqrsDOS8fTBz1UEfx7HAKVjkOPQ/hxRi+HwPru2Xf/KYIu16ws23ebD73n'
        b'lffwX2FRGk0WJe3T5aao7AVqUDT6awwG4ueYHtBo1KUgQhAsZnqZ3yU3mLQaA+H/LKvRoi/UsdRDiOxm3iPpQpf9JDHJiKYJDUtmpNRERV1zdSNY23P/H5BCJCo='
    ))))
