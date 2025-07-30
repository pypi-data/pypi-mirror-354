
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
        b'eJzVfAlAU1e68L1Z2Pc17EHWEMIWQEBlE5QdFcXihgGCRCBgFlHccCUoKAhqQNS4xz0qIlVa7Tmd1u6JTWuGtlOeM5122s6UtrY6baf9z7kXFJT2zfv/mff+Fy4n555z'
        b'vrN8+7nnu/kjMe7DHP3+dgdKDhAVxCJiBbGIrCC3EYsYYqaGRUzyqWCcIgniHDl2L7OpYDIIMfsUyp973Go1IbdZzEDlZhWsie23kKjUXPxULyRRwS4iLLfxzH4QWxUt'
        b'zJ41n1tbV6GsEXPrKrmKKjF3zlpFVZ2UO0siVYjLq7j1ovJq0QpxhJXV/CqJfKxthbhSIhXLuZVKablCUieVcxV1qKlMLuaO9imWyxGYPMKq3GfcmnzRvzVGxGcoaSaa'
        b'yWZGM7OZ1cxuNms2b7Zotmy2arZutmm2bbZrtm92aHZsdmp2bnZpdm12a3Zv5jR7NHs2ezV7N/scIFTeKneVk8pCZa7iqGxVLJW9ykrlrLJRWapcVYSKqXJQuajYKjuV'
        b'h8pNZa3yVJmpGCpS5aXyUTlW+iLUW2zwZRAt3hPRucHPkmAQ630nlqISv4klJLHRd6NfERHwq3UNxBpmCdFAIlQzCsrHE9YR/TtjJJiNckMRwTMvqLFAd0DBJDAzpNpI'
        b'azTSFELpj26msjPhLthSmDcXqmBbIQ+2ZS+YIzAjQuz5mSx4SzKLRyoxkiPgeXhKnp0Pd8PWfNhKwuuwm7DKZgAd6IgpJ8fNwGlsBmqU7HNsRrNACCMQEtkITeYIqZYI'
        b'mdYImbYIgfYIlY4I1c6VThTaEF+1PMWFGxgU2shn0MZ4BjXkRsYo2iate4y2Ff8M2vJptB3PNyNsCMJiOn95zQfsUoIq9KhlYFwub2Mvt3GMTaELPwy0JBwIIspq5fI8'
        b'j3W+dGF/IptA36EPZi0PH8jeQJwhaqxQcexaDuuBE5HKXfp9yDeM/mhQ2kTWWOLVTlOTOvcUKyJ1ecyHsrPSbIIqnrXyW/uuIgWHMWeY/JlTYsUhhghlBKqAB2aAPkTC'
        b'XZFzQ0PhzsgsAdwJzswPzcmHe8IjsgUrgSYnnySk9pYzokDvBEqxxhbdiCnFpCiFqURUMh/Tgvlvp0XV07Qwn4QW1jQteBx7wpsgOFHFaemlxSIaA2mgtR4hoJWfC1th'
        b'S97crOzwbNAEby4gYnKLXEHXfLAL7CNWsM3hEWdwWemKQGZvgLuF4DrUghcREsAZYhU8la3EnLtqk5kQ9BXBnbj8EFHNXKJ0QcWgBewBp4QxZTH4Zj9RDnqTlfaYcZyX'
        b'uU+BnWwkIUSEfCk1y7N11gQCsogyez0mfEEJzQenCpyJQPQdJV3ka51aT0jOblIx5GtQSd+SpIOvTz+0ueVo5+XOtR4BTLiSu6PJ5ZWaSoelgfMZ7sydMQ8UypiFl6Oj'
        b'NGdrGZ8XiN6uJM+tyBHxlueJLoi1IuIse6ci+rROkBrDJJtucOaZFncHdmSaijiGDE5RQnvmXcOSod/ZKFKcb/y41SPhXYK/2fP1XRE8xgNvvJqdqTXWCHW8fKUgDDGQ'
        b'tJFBuIJmloUUdD1wxxw2WG7vtwpheCfcA1uRDkkkweUsIY81xAjlyWxRiyeJHPMUt6mp6Qe36ZWyukaxlFtJK/sIeYOkUpE8ZEVp8tIKkULcOC7PwMDNKHnURIxkkISD'
        b's0reHtfS2Nqonrtzk2rTR25cvX/SwAKDf7rBbabRbabeYabJzUtdsbdG78bXKPRuQq1CNdvk4qUWdxSqMk0u7gey9mapxZp0zVxNeq9E66pdpXPUys976hYMRA/MHRD2'
        b'LdL7pBpc0owuaai9M7d9hsbV4BxidA7R24R8izlRhlmRZzbEXi2qUYqHzEtLZUppaemQdWlpeY1YJFXWo5KnEICZdjkXo0Bmhwsxk4xfaABuVI8Xilc6kyRJ5xHit5Jh'
        b'O3eVpKW6tbrJeoTBJl1M1k6qqS2JrYnDLPum3M352/Kb8k0W9iYLZ5X1oxE2wXaYWNpUSP/JMRfus+QT5+wSmbPKGZMpgvW4CQPbTkoVkI9VAWMStcy0nES4UQnzGXFn'
        b'bGSOqoJJ6x6rgsqnVcHjiY1TBWYFtERegjdgD+xECk1AgF2+gunweUq2oQ4ehSdgJ/KLIglwDnREpsLTStwLOFUBXhiV1Yq4CLgD7JPUFOhY8lRUubD0eyyFRzslJDO+'
        b'HahBX2vLZlGcc96JXWc6L6f4q+K2P995xurN8rLPWJ8ve8ViPrQocn7zdrcdMTTNOnzAnkc+8ML6AF4BO/g5AnjOFqqy8wrYhDW4zICHwAUOj/k0r2DXbYxRhqxpHqms'
        b'qRMpGsffUKKRMCoa80nC1fNA/t58TYBGbnDhG134iHntXRCr2AaaOIj7u63b2SZnz/ap6riO5K5kvY2/zOEJL8uwpRtiV4jLJAoZVngy50n4l2Jgmn+xBpgwHT5utYpi'
        b'YDyhIsTBnphRfz35l3Lwfstw4rxdEpNSqpEuzmQsgwgdjrcJ6s7Q2CjxbK2R8j8mV8RHsQh4CfQzygh4CnalUwCfhrmQCQyCMxz/Zn6a2Xa+0g1zzDGoWoEBSALuljPE'
        b'BDwDW2dQ7efHuJPTGUTCcPz5kKuLl9EDJMAjoAu3ZxLwaBFjBQHPwZOgnwKwLuaQqYhiw8nnCyqVny6iBgBHN4ABuWIqmlECvM6QEvAsPDqNam8X6kVmMAjucHJern52'
        b'ux/Vvgaxnwa3ZxBQY8WoQwOAg3T7n119yCwG4TCc/KVvSan7eiUH99/kBPbIYV8cWsEcuJcBthLwKjgupyCmz/Ij8xhE1HByeIZD5JZl1BLAoVo5BcAm4NYqBthGwL5C'
        b'eJwCeG21PzmHQVggAFK7MNqGkqplyP71yWV4BHB2OZ7S+RkpVPPU5CnkfEyD5Ddrmpf+MYrqfwk4GQmvKqPRiq2dGcj8wqvIc7xCG/H1QeRzmAbJX6YtCX5XQAEg47LX'
        b'g4JgEPbgBgPZWNhnLqAAvlUEk0swEZLziA8W/zmJwlE1vGohlwvRAOAy2MXYRMCL4FAZ1b6GDCWXYxok1rh+wzxdS+PoNLxCTwlRrauMAXoIOACvTaUg0rL4ZAWDSEUQ'
        b'3nPMPsuh1yAkqPbmBBiAzzPAQQI+3wA7KYCA2nCyCpMt8csF/7F8aDE9xCDsRE7FVbmNFSLcIXiKAa+RsemZFIR3QCRZwyCWoyEYaza6VFEQ8+HhOGsZ5lSwA15jgFME'
        b'8qt3wFMUxMqZUWQ9JnVi+MKN6ZfdlR4YT8fBYdBtDS/HYaBtyxjIF2ciLbefdkvDYkikL+YMJ76Z8MGyqkU0ai+CY/CatVUM5m+1ggH3k5ZAQ9B1p2ELOGoN+zGlfFkM'
        b'uJ0kwS13CsOxQA1fkMOrDXYM4rk5DHiU5MMLCqrKF7Rayi1toY4kZgA1A94i4wtBL8UooNeRsF6lhP2o890eDHiZDFpbTk99EKhgv9xapkA81AdaGVBN+iJntYOeyYup'
        b'WKjgdWuSyFnMgG1otP1QRfVZhzzcnXI7W4RWj1lMNjkDXob9VE1+CRhEFXZoZS1wP9OSTE0Huyllz6mdhipWsQg2uMaAA2QE043mfM1ytGDbetCK8Pc8vMYMIFOhxpKW'
        b'08vzoQ4zOZKKw/GMegJeIJFVoWzHluAlSORjzYjSGEYl0hCLXEanDfaCrZgR2cSmYkryrvjCo0pPDNMP2gHC4GV41R4xxN4sBrxIxiKn8xitdrY7Q60c9lO1+UIGPEsK'
        b'fZN59hQlQ+fHkmuw1CbaWMTPzVlCFVq4TSXXM4j64cTzmRqX3eE0zckEsgmLa2KrdNg8VEwVlq9MIrcxiCxUuPJty4HlVGHetOmkCktqYl6VoN7Ziip0cEghWxlEFSp0'
        b'E/l97EkVnpmeRrZjEU18M3Z5pp0NVSi0SSe7ECug0csVDWQVVVhglUGqsWwmvun6h02+CqqQ7TSL7GUQa9DobguiPqNVqWpjFqnBUhl33vJhozyJVuBr8kktlqO48wGX'
        b'sqZxqMJvJIXkeSwqcTWzdq742JIqvFw9l9RhaYj7kr/JOTCVKox2KCL7ML/HfbnogwK2G+0A3ATHUuTWVogpvFKYNmQqOAJ2UT4DE6iRuNnZIkcEdDIdER9dmkMzRSs8'
        b'HYtU1PUGZJOTwFXM0fzIEkpGmTXwMpICpC0R254AJxmwi5yyCe7gsagpVCteIXuZaK3T8pxzUm44UIXpWa+RGmTdh6eGT28pLqukCj+JfoM8wURKZmr4utc4cjeqMNvq'
        b'LVLLRAiYmjfrWNAerwkbNPaY+7MRJfvYo1tpFrWNJirZ/5MbZjPiWc8suEDJpfi6KBLsKkT6fg9syc6PgC2RDMJtOdwKVawQ8OIyat1x9dQGmohabchLC0yl90hxKRbU'
        b'Bjqq+PSmw8lWBCVFsDUIvpAbCQcX5MLdhdloNw23MdaC7eB5Wuluh4fWgatIofSxCLIEGcxwcN4GdNKVrT6gWxLDD0U7G1UkcsZsVjDtJXBUU3XDm6WwHR4EV9FMkhDd'
        b't8EDMsqA4CQmidq4c6NWpwnPb5pBFy6IMMcPAxyiZs2duqJkKqHE7pRDUJwwCne4F+xoIERZM5UBlPSLHXKpPdMe/NAkF+yB25dGZoMLoSTBVbDt4DYOteOEHWvXC2Mx'
        b'QJd/OVFWBHqU+EkW2GWeyEcbetiaDy7Ca2hruysym0U485iwtSqQ0kll4BbUCukdqbM1UR4CWqjyqkp4UQiu4B3skYoEosYN7KXYXwiugUGhELc/zEeb2xVKcIuaQhxf'
        b'KRSaYT8FNKUQK8HuPKo97AZHZwrjcXs1cnBuEBUh9RRa64JYXgG5OXhOBTRN7OqZCUkENXoy1MwTxuPBu5lwFyGOA01K7BmDM7lJcaAjNw+BRMI2PklYL0IKEewDV3gM'
        b'iiDrwAF4WRiPdAToKYQtRCXyObbRzn47UAFUhed40GoBsQLeMqNmIkV8oIsHzXAX2sHmswmWL4mMXWc4rQheQKq3TxhPYqs0Dxn8Kh+EIYqn2hMSwPFSPqYGbCkAF1iE'
        b'zQymPbzUQOEjJQC8IAT9lLUg4xDlab8v0BGerl8Od+Xl4G0wE75IgoPggouyADfsWA+a5Hlwd1h2dj5+lvb4cURoBC8sP4InYFiBk2JwCp4CJ0JDwRk3Pg90wRN8F9Dl'
        b'5gpPuIPTDLQVd3EAGnCupubRL7/8Ul09yoCVHa7GqKUEzbTnvWSgK4tfIMhiEaxUEpwFN6x4LnTdYT/wfPY0ua1MySQY8DAZAFvtKFNjDfcWJlfCq3Z0TT/Jg13gFAW0'
        b'YWaAP3KAr44CvUjy4+AtCukzEP4GnyuWIyCSwFrPLzSFHqe/OAlsAT3yVUorVANuklxWI4WhShskiWdmI6PWAPvYBHZO/O0RQ+O6fHhyig/yqFCNLe7vMhkDT8Im2rqe'
        b'tZAHV1rbWYM9DIK5iFwcl0bNe0EdH/Qgn1xh1cBCA71AekM1uE5VLQJdoCuwBlfhgTaTXCQrvbSjca4KXt2InP6rChnsQ6sCL5JeaK/YTRv5Y3bgrBxeUZgRJDhMxNnD'
        b'PU7IB8ELK4an5yKfoM/awtYKKf6pZJYT1NK2esASIekUdghX2eDZ95AhM2ls5MFb4FgZvGFtZ2OJgKaR2QvAdto3uA5vzoHbwBFk4WXIiWLakVPhCwFUh47LwUF4U4pq'
        b'4BVkj5hTyDQw4E0hwyIGqEXF8lXUQKCf9A2LoLu7ANA2EvT4yK1oWu0luYHwJkUrhRKeTne3piqYTmQUaEFOBoXZC9VwvzdyfjuR7IQT4aBtHiU4yufQDmGXvdUquBls'
        b'WU0SLOSagLaUtdRIs5E2bQG7wdUna4IacFHydkwPIf8EidM/eN6H5s8o/GOqw0eRH2RbfOxg8fHsjQRj0WdVmhe+nydWOO1k7Q3wZ90M2h7kHqu67+nuvVA/wnzk85Nv'
        b'5b3gr8MX9+q6Kh6+9fa6uspX16p8S95PFj089su9qLeaGn7/afnAR37Ct9Ly5jhwv1q5bvrx3Wc/tlyk03/beuTA11Ljjqre2mtlN2986l7o626/Ku2b1kdvJOy/uDY5'
        b'KOq+8/HSroiHnKNzVQ43/9zls+6ltPcbA2IjK6KK9HlV8/z2W/741o8/zlr5wELgtEB1bdDmjGue7aF3Yt93+sf1C78MNj+KfWmF94vNj76MOlvPls/8tNL4ynfrt391'
        b'v/Hoy+/aftCx6NYCXUT2F/fD/bivTjGUyn44oIp0HvzjyOKXF17MeeG9us/+8dJP0t9N4z/3/jfvcL/qKWr8XecXL7+0A37cF5Ze9oeK/YlD+ZU/H853nRtqHn/tRkv0'
        b'vW/PsO9fZPxYG/hX6Y2chzql4OIX8rC6Ux5edzaHroj9av1Xq6O+HflwdcUH39ze3dLUrZYd0v18Jlsx7+WXftg45+3Su2+fdnyuI+tAX557313HP3za+sXI6gs7vjlU'
        b'HPz2Q2Xv6sGqLxf0Gvlvv/OloOBYCdP1RsnWY3/65fQrtjcvVk9Jefhczx1Z6jtu2brPfS809u2N+6Xo5kLJL8zvO+M2bSI+f/dk15tzeRbU88HaOlfEeVfgrvACpM7g'
        b'nnCkuME5rLlbGx/gowGwFbaBPn5EdngYLwLVI81NcLjhsaxl8MzyB5QjrM0AbWAH56lniHGgk6qGW8EBsJ0fgbRmiwIcRQOYgd0MwQxw5QEW55IKcDw3HNwCHaFZsC2X'
        b'JCzQ8GvhjqAHmMEVpWBPbnZ+WLYg35wwYzEsJEseYC8EHM0C/fys8DC0MdgHtqBZIXW8h0k4T2PCg3Dz7AfUPgYNvTO3UIAEbTWJ15EG20Ezz/apBzX/9USOE+7op6np'
        b'8UMeJ/pBikImkspF9OlW4yRl1COfHubo01C06wkaIXJJ24Xk1/RXO8vk7qXOM7rzUM6Fo/bWuwSb/IM0ohPuWkdttNb5hHc7q/25DjvcLKtr4z13wV13gcE90ugeOUJE'
        b'OyYPB4W1Z6g5HQWmYJzx6CjsKDS5eqhDu5bdc4246xqhlRtchUZX4QghQK19p2iie1doRJoyTVlvNQJw7Jg9DnLEjPD2PTK1Z6omtntG74z2DJOnr3pVb0j7TJOX35Gk'
        b'niRNeXdKbwqaWIw2xugVgRr4oxUFuiZ/jRM128QNQl2v0pSdsKRvqJGoGy+uJqNnhnqGSZigztD4Gryj9N5RJp8pmoqepeqlpqg4VOpl8BbovQUm3wCNoqdWXatjD7hc'
        b'sdXZmgJ52vnH8jX5OvGA4kqtrtbkzdV49Bbe84656x2jizN4Jxq9E/XU9aTLyFjUpafBO1zvHf6kNEKISj26C9WFuKxG7xODLtyfW2/ePe/Iu96ROrbBO97oHa+nrseQ'
        b'wxHR2nJd0JmV51eO74HulR+Fyty689R5qOzI0p6l3aW9pSOEvUfycFgkqnLtzlXnjtgRPgFH8nryRggyLI00zcz6mkmGZSNmIH1yyAdUOkKlw4Eh2qCjubogQ+BUdabJ'
        b'L0CT3btphGD6JJu4gZqSE/Y6hp4rRJeRK9QpDdzp9J2BuobpJve48Xe58bh2hpE7Q8+dgTLDfv6In4o7bEYYbE+ndrMRGyIgpN1+FJ0jhJljMpUgwoaGX7I7a6eTG0Kn'
        b'GUOnGVyC2jPVQg3b5O45QrAQrZXUl9ZVF6z10/phtLLUxb02mgUGDt+E1myvtjd5hKLluCabON5UVameE4cuIyduwMXAmUHfGThxj0zO7mrLrhR9cJLeGV/D4am3XW5L'
        b'XvYzhs9FvOnWladxN7jw0IV5m9dVqg9N1rviC/Glxqx3+j0v/l0vvnaWwUto9BLiQReSpsjM2xV3El+uM0YWj86t2MAJ//vIQgYle6OSOO6hqsWQzXjhneyx6tPqAe8l'
        b'lo/XDDK8ZZhMFczEzfEBHX1ewPhPn7b+m567HrAUEBfspjF5JL1jvpXLzc0ORzsSeBPuQTsv5ApvAVcnbF9tx/aIu1Gyz3Z0+4pPgYlnz4ErbR9vZ1n/9u3sNh7ju1o0'
        b'PSvuuM8cjHs5VzQxyoAKXVhbL+bmz0+MjeLWyahMTMQE0Ak32QquTKxQyqS4rxqJXIG7KBNJq7mi8vI6pVTBlStECnGtWKqQcxuqJOVVXJFMjGDqZWI5KhRXTOhOJOcq'
        b'5UpRDbdCQnGESCYRyyO4aTXyOq6opoZblDknjVspEddUyKl+xGsQ+5SjXnCbmgldUcdYdKvyOulqsQy1wsEVSqmkvK5CjOYlk0hXyH9jbWlPZrGWW4WmhqM6Kutqauoa'
        b'ECTuQFmOli5O+vUuBAiHFWJZqUxcKZaJpeXipNFxuaFpyko09xVy+WhdI+8pyGdhED2WLy+ok4qXL+eGposblSt+FRiTAC/zyXjpqKRGLFE0iqpqnm49SqsnjXPrpIo6'
        b'qbK2Vix7ui0qLRPLxq9DjicyeeMyUY0IraC0rl4sTaLQiQCklSKEeLmopqJuYvvRydTSc8kQl0tqESuglWJETda0XCnDGFr7ZDYL4YkqmVI6aWt8IplEpahPZXkVaiZH'
        b'd8raX5t1eU2dXDw27Uxpxf+CKZfV1VWLK0bnPIFfipE8KMRSag3cFeIy1Jvi/++1SOsU/8RSVtfJViD9Iqv+/3Q1cmVtablMXCFRyCdbSxGWG+5spUJeXiWTVKJlcSNp'
        b'rcutk9as/W9d06gSkEgpKcWKgju6NLF0smVRB6u/sap0cY1IrqDA/3csarwvkvTYnI23RY/1XX2dXPF0B6OcIZaXyyT1GOTXNDemtVhS9iszxpZLIRpjroXIcqGhamp+'
        b'hcNGB33CjhPH+nXW/C/jXSZGVhQJXRIXaRnUch4cLK8uoweYrD3WRWjxpdXicaQamxBCQQ0clMvFNb8FqkAG/leQONoPbjH5ZJ+xuLlKaYVYOrnFHB0W2chJbPXEgVGb'
        b'3+pjxeqJdnc2pjY8UamQI01ViZwYXD0ZYL0MEQDpPNHk484ZrRZLBQWyiF+b/YSxn5n35PZ/lBGe8gEmAP+qP0DDStDQkwNmp6cV/DrbldbJJCskUsxSz+qQwtG6Mooh'
        b'kQBzZ8nEtRUNvyrr43v+Jxiabv5fVCZVImRtJlV5s8VlcBCJ9SQ64b9hYlgMKDnDem7CvOajmt8WNqmoVvxE2436xdzQAlQ8KZ8qZfWUX/QMRLFY1iCWVmCxbGwQl1dP'
        b'Bi0X14uSxjvWqINxXv0kEIul0qVJ3AXSamldg/SJ110xfh8gqqhABQ0SRRV20iUy7KWKZZJyrqTitzz8JLQFFdVitYnmNL/qqZjriYBJo/ucJLQvmMwyTGw94fzQjvjV'
        b'gNu+HDpOOSr+C+ZA9RT64K1qFmv0NK41+lFuHUGd07DgkaW+sA9cZRDENGIa1MRSbadtHD2kMztaYkaG0W2zC8AlYQy8WEfQAZw1zlT8M2y3ALv5vBzYyi/IiwCDofRz'
        b'Qr4Z4e/H9gTqmTwb5RTqzCMQtMFdkTnZArAzMic/V5AD23IjLAvYRDRsM+PXCuhDrhvwRDV/rBpVNsQ5gcNMoBPkUwdPnn6go6bymaOzarBFiZ+1wk7Yvo4+IXOBfeMO'
        b'ybaArRT8fLgXHoS7+NF82JafI2AQFjgyZSd4XkTP8hbos8C9Z8PW3ALQ5gUvwz2RWbCNSfg5saA6wUOJY1BBpzNsetKsG5wDbfi8tgUfkQby2dP9YbMyGM/nPHvNWDtw'
        b'RF6Am1EnmgX5JMEDg2zQYw87qD5DQB/sftLnTrAP4WsPPrRETQOXs1PB1hnUuWgKGADX+RGwDXUWkZMPW8J5ZoQXWtUA0LHAcdALO6ljZNAGWsEVfoQDPE61zc6HO3FT'
        b'd1dWFNwB2ijyucPBFU+opwG7J5AvBmymDkFCQYe7MGYuOINPJRGzrYGDdIDG9bme44kVWkITa9MSCgxelMMtwhiwzZ6Nzx2JqjSSPlPZBfbDNrjbHXaaIzYloqRpFPHh'
        b'FriL9AMvPkPeRQkUdUE3fB5eo8kbMWMcdW/CvTwGdSxkVQP3CcGVejOCzCPADkTPi3UIwdRp7NEcV1Q1B+C4enCYqAYH59HdDoAXABqQ7w3aJ3LFfgXPjOrWEg19SSis'
        b'ZxJkLmEOboILCIM7qOMrnlWxUAh1bIKcR8BbOaAPXAfb6TOvfvCiv1AoQ0CFCG1wD7gEOhZRc7EJA9sR1BUEVUyAlumgP9KakrKQDQFC4Ux4Ax+5HiOq4Une6ElyeqpQ'
        b'CFRcjMjjRA3oQWJARXVI3YlwLKp28vLaQDmhxE/VYFcJaIlcIUedZBKZNWlUS0a0A4HYIiFq1ndeF13NCB6TXvxluB9uwUet/VLYRp8rW0A1A+wrXktLZD9QwVOLwc7c'
        b'CEEYpjO4yCLsi5k1y0uoVW4Ez8Pz+EkWm4CX3FksEhwJge2IHNS58/NpijG0gUOwBVxYa01VMLi8x1gTwvOI91sTKe5eBw7ZjRNAXzAwQQDBcahFfWMuqodH7cawW5QJ'
        b'LinhFmpCaeAM1DxGbhgiR/8suJ3qPAjsBxce9+4Cjz0ltnBHHn1AewWeWY+6ODx/jA43YD8l0EqwHW4e6yF59mQCDfrX0Vx+xT8c0axp+SjNMuBFSsdUx61/PAXY5vK0'
        b'lO8GgxR42HxwRSh0gHQYAlEFtsioNSTDM+BAbragIAKJc+jYqYwXaIYvwj4WOOkGT9PHtJ2Fy/m5uWtgK0+QzSIszRlgdygdshQtt6PfApiVFea+KoM+GGfZZNBUnAK1'
        b'FBVhN9hJvboCL4RAFeaQ3UETOQR0gk6aiTrAVYTnVhY/R5ArCCuArSRhv4Iphu2whdaD+6LB8aeCOfZQYQNeeUVwgAX2wm2giw77OAK08PmJbR3rx8V91IYog3C7m+Ag'
        b'bKZVBdgdyfQap4fCytlIJTchLUWpFR1isN25kUhkD44PgamFx5R+qN4cNAeMRoqMRYmAzbCTihRJhQPUcS/cstFrLHABdNbQsQu1oFvJo7i8cSnGD4Uc0IIYFu7Mw+d0'
        b'uUlAg3ERAw6YZcPjdpTSTASDoA/NIys8hwtPFQrMCOtcBjwMb8bRs70Jr8NTo5EV4AXbx8EVfDkSWerRcVMMnicdsOEPDlIxG4GLaOhOfPBMx+vArYVjITuwB/ZRtIzM'
        b'tgG7CsHpxKeji1gh0gVUME42OAVubiq0Ri5BEVEEd1QhccPl0WXB8CZoHVUqzuAcLeBHfGCvtcytDLkh8AxyDODZcFpjXSDhIFLX20YjzAX+UEcxXwbbcjRGqYw1UBBP'
        b'UOi1RRNEdgseQDqzGdkEsIcohaehZjREEGptwNUouB3sZOLDUKIOqsB15UI8/h5XKzkiDGzLnjsHXIkqmofWjV/liRCEQlVkGBVLAq4hShZhWVGFF2fhlVPonZsVjgNN'
        b'kATlLpgD2xDVb61zRFbzKjhJxY9sDhxzmSKcPrVwIGiremYt4qZdhajXnmdxWFI7qvhi5kvA1VhshuYi+7IAXADNdrRW2B9ZhGtIrPlqo8DFaUlKHLyE+AExbCdQZcMO'
        b'pJG7gGo1StqQEboQDy6ywZWyRfXzFGXgWhyJCG9WgthES1MAobzscY/8cnAxIwsxChW91UGyc8eChcyQgHaWMsJAXxzFhoHgTK5jydNKHajhWUqk+YtK0DjgBuh6SuZP'
        b'gyu0dWurR6I6tsaFyPG4MAcZPowj5Iv0iybxUJILkX/iDF6kBqgA11ioTUv2M86JxJfHolXYDqTuO4Xxq5COzyHWIEN/UQRu0FXbEaecFsbC5nAzyicRo5nvphFyrhhu'
        b'FsauRvhIJeLgAXBGyaW1+pl5kWjCUEdgwwC3BoMr2UIeSYc67bfFZIlGVbOQCDSDw3BPuTId1TCnu1sjZ2UXIvauSLinCOpsweXY6DlZo1wHd8yYM09QPO9pZkJa6YgV'
        b'7BHDS5Rht0GIu+xTAc6h6a4n1oM2OuCnHhy0B+fiwWUGwXAj8pCdOQvOgj5ahLbAw+B8ClJ055AJ2UhstIdqJTL2xIJccEpOvWs0LxQf0GMluZAePHrm6PALBeaIWGeW'
        b'KKfhlQ/mwB3WBfmwTVA8Kh+wZWFWjiXYuyBrPr0icGYOVOULIgryCtk42FtnBbaD85Gj/JwIrk3H4dljb2rBnaCZjgTbgzyIk4hxL8ATsIuNXRVEAeSL9iNIKrrhGtgL'
        b'diFe7nqa12BrEt2iB/msJ7AC3RU6kdmi4DlaA7xgPxsHPvXbkgS8Ao8y4HUylh1L1cmxopPD/np7MwIeS2TAFjJYAfqoOESJ7P1jpJyFLGhOM+OCW36dV6ai8vsP/LJ7'
        b'YyV741vePSGRpOdauVhtdrMQCGZHcE+eTo5L3xf+3PHYnZUJ3AROCXBKX7LeZP38fM2ygdse0p/Yj6x/Iuw2/BhT/VVrwwcu7+0/suIPDwcvdft9nnLl7TywM7n50boE'
        b'04ZpV99wYZ5K+JlV/4misr/knZvfHpGxv3gz57r8/hzNtjuB98Punz657o7jG8LzspMH64tHov/qf4R5n7s08W7tt39z7XLOlA2r3RoLfuJ/k/S7weGeZX/jHvmm6xLj'
        b'L1sbjox8veC1P8Y9+LnvT8Pv2M6I/bI+uOS+W0nH+m1CIv6Hj8QOD6p3Pux9/9WqGcb3mR6aj6p2vX33Bweea35J81mb75/7sCvttb+fPfWJT0cj85rgG6vPF30aU3Jn'
        b'9bdVoprIq9MuXv6j6lBqeM/fetN/8br9oiN8jrvDviFq7Z+Oeiz+U/eWWcuslG8FFN+e71v9g03ID3bi8sbhd23+HrhoE/f7PxHTzl2+5b/6bdVHg6d+au0q6rnv+Enf'
        b'qcCskoRjD9b89ONt/mkbt80b3hFlr7tztORv/t8InB96bOGzFloeDuI4LglYs3t47Za4LcotkQ6DqfWHhmdZNZT8sN39x7cLl2z/LFv+WeZ9108+/PLgGmU9497rC999'
        b'83cv3Xm+wuINyXrN0WPFPg25iX9vfX++46yY1z/5+f5c747y7Z+H5yyc2Rh++x+tXyy7eOLKlb0PmRF/jd6uFPDfWX23P4SfeMH1arLrrNT3HErXzbqw32aw67vD5yXV'
        b'v8z84vjJsgt73n8j6ff33d83gn1nzzU1Xo04V/zx9vodMR3FL52ay/Y/v/L1Ux6XXo78hhGx+NuX/X1iDxo5F99/UPFa/mt7uzlDwsvfTf1++I2kG4vnLU+ZF3g/evp7'
        b'LoNTDjE/vqi/NCCxXvbWhUvT32te/nJz8g8jngVdkdN2Zc/hbL4393XVRc/ZvxS8/nVg+J/cT9meg6+fOL947zeLXrkp+cuD/1hpeLB96gPvDUWvmk5bDuyrPP/eie8W'
        b'9xV8+ssHHOYfel55L25R/hy7i7mlSQ8zRL7rgxql7t8a/sB7ofvj6JP3bf/UapX4cVziB++e7P2qJKkosl9cHPfB7xbM7Hs4++1hYDv9r698O/iXq+5Ojd8dOnP1Hxn2'
        b'b3zhWUd23Dx3Kud47Uf/+DrlTkmiXYjqR8WNR4VdWt/ZU864ypaaVTv5fLXv2N2Vi5tic+Uy8M1bMzJ87M0b+39/6J0FAWWy9HiZ3LZh9ruJm5ja197/vev3v/tJ/03Y'
        b'rhVrh5bmfvK8Tvht01+nHdGZr1f0fH6gIy5b8Evd9+zV/xG4vv0L4BBx4tC9F5ofLX7+YbbFF9v2rFv20P1DwZ/Pvrr1A96OPwt+/mrXP35a0mD/eetHyr9ZNX685qNb'
        b'usorv7/R9FPhkbaLS1/TfvJxyMIv5RsDru557sF35SmMQ8dkR3h2VGATVM+EF/kR89dgjYnDmrDORl6YO+hnZaXDg1TQFtQhP24rPwz0giMRPGSb0B6whAFOosaDVNBW'
        b'HTJ+W5H96g6bGLbFWtYA+x5QLuMh30w6JgsHZMHrq3BMFtgZQlVWZ8XnhsPmteMjspDf20u9A1dm7zkaLeYM9o0LGIPHoh5gh3U58qr20KFZj8OyQJ+QiswCujgq6Iu/'
        b'FnbzC9CONj88B+4m0AjPMxqQW3uDeiV1oRQMIId4Z6SAQFPbCq43MCLA3g1UNFlcJVDHgqu5aGKP12UfxVwx241e1v46qH3iVXiBJuRUuIJm+lXXizNm80fxZYb83BZw'
        b'niEMKqRWhXYULfAsfrVPle0Mdz95ta92+gMcsO0EB0vgVbSappm5yD2rpwwcg3CdzmIuAp087v9zTNm/OZFj5nr2qSsdozL2mfCqYq0iMTaqcfwNFbfmY0nHrUnNCBfO'
        b'gZS9KQbnQKNzoCrD5OqummVy4agyTR4+qhyTm7tqtonjPUJUMWznkV/TX+0sk7NPe5K6QpNpcA4zOoeNEKRjhMkrRD1dyzJ4CYxegvYMk7vXgXV713Vs6NqA2nv6a9K6'
        b'+e3mqBQ39jG5eJuc3fHIGiH9Qu/XhIjhOI80BYedXnlspc5ZJzIEJxiDEzoK29PalWrxsLu3hrV3Q/sGkxd3hGB4RJu8I/TeEVqlbpkxMsPgnWn0ztR7Z5q8pxzJ78nX'
        b'Bhm8o4xUINpwZKyJJzCFhptC+Kh3U3iUSRBtiojBKT/SFBZhCo8Y8bD19xwhUKJmd7NHvAlPP01gj4/axySIUbPV1QZOGLpMHr6jpV6+miD1dPV0U/rsV/mAf6fckD7P'
        b'mD7P4J2iztSEGbwFaFolhsgUdKHhURnP4B2OLtyDQO8RiS4cSMVWV3Xbd9ujUv2UHL0HvoaDozXVuqABxgBzgNkXNiC+nTZYdSfgRp0huMAYXGAKFWhFOoa24ry1KTBC'
        b'k4PGmatbpSs632gITDIGJo2Ys/BCWHghI1aEt7+mQO8Vgy5TbCKaRoTBOxpdOLhNqveJRZcpLgmVRxq8Y9D1JOgtfpo6Uz8FlQnR9aT4ceO/j+Ki22eE4cb1NHnztLEj'
        b'TJQb9g7UrNSs1LnqVg046uR9nobg6cbg6SNsVDdiRvgEaDJGzHHegvAJ0lSMWOK8FeETomWNWOO8HeEThvqyx3kHwoevzRhxxHknwidU6zLijPMuhI9AWzHiivNudD/u'
        b'OM+h23jgvCfdpxfOexM+wRrFiA/O+9Jz8MN5LuEToVWM+OP8FLpNAM4H0vkgnA8mgkJMITxTWPgIH98TY4maNRKBEezYm0DHqNGcP0KwPYJN/Dhtkk48kDYgGpjZt/J2'
        b'3B3HOzF3XF6eZogvMPALjfxCOqbQFBiszlRnDvMjdRbnk8fKgtSZpvBoXdD5vIGZd8NT1Cz1IgMnlAqd1OYYQ6bqQ2YMpOlD0m87GnxnqpkIrf7BGrF2pkZi5EbpcvXc'
        b'FDXb5BeoKeptvOcXfdcv2uAnNPoJsdSEDU8J0pJHQ9QzcQhnuaZCU3HCGrX29VMz8QAze1fe84266xtl8I0x+sYgWfUIQ+vAa5h5N362Pn62aayDESaBxvjPAYZDBZes'
        b'z1rrMgcC+nJuk4bQdGNoeret2kzDNvFitV664oEFBt5MI28mWuhz3XamCKEuTSfSzTy/EhUsNXD4w/HTECbTB9L7JPfis+/GZ98JNMQXGuMLv2aSHrFqFySfHmHamSZv'
        b'rt4/GrMxx0ctNXIE9zixdzmxuvkGTpKRk6SnrnEyHKR1uesl0HsJTFNiEK+jqcdmk6bceajX2CIcuRkwH0duohRHbs4nh0e71ZYZOdG6cCMn5R5n1l3OrNtKAyffyMnX'
        b'UxceIELvEYWuYW/fI9k92frg1NtIHWUZvbPU5HBQqKZI63jJ/ay7zvGM53nPo6UnSk2hvEvmZ8115Bmr81YmSgP4Xw+5EjLgfzmM0gHKG1JDcL4xOP9Z+c7sSVYn48jb'
        b'TI2AjrwdjpmKbpC6idR7R1K6ZYbeA1/DHG88u1C9Rxi60N2wb4TeNwKtLirJNCP99mz99Dy0+Kh8vHi/Arx4lGKSFpDD/sHtOR05wx6+IwQP62mk3jft3aSRG9z5Rnc+'
        b'4i1Xf53LdZ8rPgNKQ3SmMTqTKrrj8o7P6z76hYsM2YuN2Yupsv/gcE3uPjiSE3VDzUAfOeuOuyFyjsF3rtF3rp4z1+QZpkcXP8/gmW/0zNe75OPo0MV611B0mVyC9S7B'
        b'GqV2mTFkusFlhtFlht5lhsmFfuc+yOASanQJ1buEIn5ozzT5B1Hz9uJqfI1eUb896mgjnZPRKxZbMH/N/LvuPIM7D8dIp/SkaIUGr0ijV+QI4eKRoMu4nnMlZ0B+ubCv'
        b'8LbobuxsfexsU2Do6ZxjOVr50cIThfcCp90NnDaQcTvAEDjLGDjrXmDe3cC8O0WGwLnGwLlIxoPCNAu00drysdjjAX9D0HRj0PQRws6HTjTkCIvln0eaYqYOkH2hA5m3'
        b'/W+LXgoazNMGaTI0GY8+ColGKEUNxqemsKlagT4hC12m0JTbIYbQbETVxFxMT5Qi2vLzcJ6PAcgglDIx2KNHj5BSjo7XiQZIXXmflSkiUVs9EHSbvM24zRjkGSIyjBEZ'
        b'I2wmb8oIgRING7UODNXGH0vWJJuSZ2oy9LwkQ+A0feA0UxBPW3xsmWYZMiOaDK3H0cJHX/vgJXExgK0xIB4LVKIpPkHD0iw1cIU4SNlHT/Gr0TtSF2vwnkrfGajL5IE0'
        b'310Pvt6Dj+ONlxg5Yfc40XeREAYaOFONnKl6zlSUGZ6cqsP4lxcYtkEmhyl6hymaOK2vMSDB4JBodEjUOySaHNwO2O61VYsNDoFGh0C9Q+Cws4cqX26D3KT3fJwXRLPe'
        b'i55S7GxOhxE7DLHwqes/ET78T7t0+DRl+WQunAy/1TfBdduL2x8jRuOMRSySdMJBxP/K5F8Wj4x/EOmIZRxxzS6NyZxwrDwWfvwtfuhzgBDjH0IjFjEqyEXMCkYRYbmC'
        b'xxxyoE60qWhfWaZMVif7wY8+46awIRsN3hVXcEVSrhjXRxTwWEMWpaU4KKC0dMiqtJT+pTKUtyktXaUU1YzWmJeWVtSVl5ZS9KQDxClkJ2JkPzPsHjRZOX4Y2PT4b9gm'
        b'Wj92UfD0kcLpqYS1HbyusLZEm6YCgYzaWoC9eQwiEh4xY4NTC3jkLMnyQ+vY8i2o00V/+XRDR3YhjHLY/teE7M70hqo35vVf6drw8cNrTQOr7qseuGxuT0gNmhMUoZ3X'
        b'W5+hsl7YyEvZa8nOCePuTZn2/cGpwu+LPvxzf5n14mtxizdV2p96zeXPGT7H3/Q4p9duHHYHBy8Vnjs9Z9GLu587NG992J6s7m/4R392/URy9O8PkzfItn/l88rPb513'
        b'jyvTfHahbcovc36589x3N3e6ZLxlf+rjPx4+qExc8seYTvGH56KW6jdmmP2j47vk6/e3fVTv0TXX4zrLM2fHuftzzCr08xzCui+uftth1p86AnpX7uRE72Zdtnzr5cB5'
        b'L8cuUl2oCugPmPllashl649e9q1oeeGzgO/Lm9SQu8oCvuzY6vRqVEHv7cBTUW0eb5bZffvc7Sn7da2u58tsv4jsWPi3MNPt4H5d2yH391zndWxZaf+G+qTowMp7h1gf'
        b'pW7tVHgKPql95+MLD36o6fK/O1tbumDlvAP5V0pOXXD4Juh4Xk/OX99bv6nhTfnbwi8PcOysGv+6440HBa5fr+t646Xd3Wu/t3szZk3dyo081gPqie3RwtVwC9q17soj'
        b'CTKBgLv5QENtgeGLsAtsB21Z4395afR3l+LBwAPqML8dXgAvWoehjSreJVs4PW7mB66y4CVm4AMqguHgXHhEDi5kFQhC4eHksQ21I2xnAh3cDA/wPGiNYPGbyb9vX4m3'
        b'89xU6tP0zIfeUCLhqqkTVZSWNj7OUVtJAZP6mZlH9E/NhBO2riMsc0t3k72TSt4e09LQ2qD237letV4tV8s1MRrRibjuxt5G7dyeTepNukD0Jxvw71MOzO1bczmiL+J2'
        b'xu2MO04vZb2cdTcmTx+T9xHHUx2jFvXGdVv2WmpyDJwInbuBk6CfXmBwL9DPm69fUGyct/Cu+0K9+8KP3Lgapw5plxQpceSccp4jkYfk5NKe1uWqSlelPxoxJy2Rg+fk'
        b'1y44aaMXzDJwZxu5sw1OWUanLL1NFmX/zCxDR4jfTBxYlsgA/mZiY8G1MtnYt7uNMHHOw1tdSeeCedp4OieMHzCjc6kzbxdTuWEKgo1zFASVoyCoHAVB5SgInEOOv60D'
        b'gjGn854+CGo0HxKG4EbzsVMR5Gg+jcwgETR1Z0FDW9J5Cno0Hx4zYHa72OTorq7Uxk+WHbHHDYmxRG/hjfZeThxUR18j1mZTUBVK9Ba+Iw55pCV+Kef/8msZg7ByMFk6'
        b'qNzb5eq49mq95RSD5RQjQjRjDdMSecP/rvRrJmEVgMbB3w6tbiMsqmq1ObobYZCWeMfwTHJo7df46wFOxuAmtqVci51pKenOBHD2TBcwadfCZYiBrNK/zrGYVM5dJnE2'
        b'njgc+D2mJ9KNzZ78xpi3wSNJB+wh/Lck/1Iv5IRlEnHDLs2CKeno92PJt6KiqtBbtW0z7LakcjJupViYNu/j6Ket3d4WbypZOfsK/H7H/p07cndGZ2WpVwavjfz24vR1'
        b'X39+IeDV3St7whoNnY2n2qbX/AVmtG4Kqzr3gjSxoHh/3v43d93as+iDGVZv3nqYwOFssYie92W7/6u+O5lW3qLQVeDvPYnVe7kXloS+sIHIXetTdFjDM6eMDDgLusKp'
        b'X/cspE7zzaNBL2ENrjCgFlyF56jnwHAfuFaTW7gC7BXAy7hloYCBbMcgExytyaVf7z0TrgC74BkPHPOAD+1BG9hjTtg5MX2lDfRT0z3wBBgEV6rwe7ijb+Emwz3U09hI'
        b'W9Ce++RnQ0G3krDmMWB7VBD1mJdbvmTcj4qCQ2H0b4p6JdL280AY6OQnwFs5bByBA9WwHWzjBfy6Ofsff4g6qWAEjBnAZ83fpKZQIpUoaFNI5yhT+AExagqRvHgSbOem'
        b'AvxnsnW5Z+t719b30BqDbajRNrRploll1Zy3JU/v6H8ywcAKN7LC9axwE8tPP/EysWybsvHfiNk6Nhtpj/+htNGasHFpKhz3OiV3iFkjlg6x8Ft3Q2yFsr5GPMTC4aVo'
        b'fyQpRyl+c2qIKVfIhthlaxVi+RALB98PMSVSxRCb+o26IbZMJF2BoCXSeqViiFleJRti1skqhswqJTUKMbqpFdUPMRsl9UNskbxcIhliVonXoCaoeyuJXCKVK/DrNkNm'
        b'9cqyGkn5kLmovFxcr5AP2VADxtDhvUO29P5JIq9LiI+KHrKWV0kqFaXUnmHIViktrxJJ0D6iVLymfMiytFSO9hX1aJdgppQq5eKKJ+qYevK+/Dc/XC6tRfPGEqx85LHk'
        b'Y/foVz6IWexJUsbEmu9/f/ovU93YSr5kY5k2hXhpil1aFPMHi7FfKR1yKC0dzY+aqh88Kyf+XDVXWqfg4jpxRQHPQpaMpRbt/EQ1NcjGUgTCMQtDVoiHZAo5DsAeMqup'
        b'KxfVIPaZp5QqJLViav8nqxlj+SdbxR8sptN7y2SZjKC3s/INKBlhkiQ5wmCRLOQFosSGsLZtMh9h5ZiRLiPEuHSRDWHpeM/C666FlzrHYBFitAgZIRhknD48+Xbw7eCX'
        b'Ql8O1YfnoMtk4WCyclOF692FBqtYo1WsnhVrIhz0hEM7x0B4GglP/dhFTe//AMk4yAw='
    ))))
