
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
        b'eJzVfAlYVEe2cN3bC8guIqKitDsNNKCNJOKGGwLNpuKaKDS9QEvTjbe7wQ03RDYRBFQUXFCJK8qiKO5WJU5mSSaZJTFk3yaZ7DPJTBLN8k7VBUXF/PPe++d978nX1+ZU'
        b'napTZ6+qc3kfPfRPAp9o+NimwEOPlqFMtIzTc3p+K1rGGySHpHpJIyeM1ksNskKUh2yhT/EGuV5WyG3hDE4GvpDjkF6+APXLUjrdMbgsWBwXk6rIseodZoPCalTYswyK'
        b'lDX2LKtFEWOy2A26LEWuVpetzTSEurikZplsPX31BqPJYrApjA6Lzm6yWmwKuxW6CjaDontMg80GaLZQF92wXuQr4DMcPq50CQI8ilExV8wXS4qlxbJiebFTsXNxv2KX'
        b'Ytdit2L3Yo9iz2Kv4v7F3sUDin2KBxb7Fg8q9iseXDykeGixf/Ew43C2cOeC4SWoEBUErPVeP7wQLUbrAwoRhzYM3xCwoNf3cGAXLDxTKUnS9eYoB5/+8BlASZIyri5A'
        b'SuckszMFePLo6acptekhP8nHIMcY+EqqyMllpJyUJifMIyWkIllJKuIWpqjkaNwcaTauIdfJkRVKzjEU+oaSqqdtcYlkB9meuJQ0ku0cconjcYsLPq/jHpKrdw8Vyyhj'
        b'OGDN/4MxRu9uBnAlEmAADwzgGAN4tmhuA7+g1/dfYsCIRxgQLTLAdaDc2Ir8QHLpIT+MsSAGTPKSZAmcM+OKee5yEdj5lLP5OhVwerrb2QmhItC6Vpr1JOcFOpseEjvi'
        b'aXQCmV0A/EWMn/Ri2CfAzHfH/Z3vGF8y5F1k7gcN82x7uRYntLo1Nn3CG8IpYbgIvmn62rPWk1uyYsE73E9LugYPRl3IEUZFcXQWqQFRlIfNCwwkZWGxKlKGT6QGxieS'
        b'ypBQ0owb41TxiRyyePabSjpjHmG5U8+6qTkxdiOj5B5TuX+ZqVl9MfXe4PeY6ioyNSLAE/kj5Jc7JDNhnP9o5AgFID5BdpNLsJbtwRqyPT2OlCbMi40LiVuIJmgWDMS1'
        b'qbgc70KZMidykLSNcAwElFlZ5LwaX5BS5P64Cq0iTeQEa5m8jjSo8Tnasp804r0oewM56KAKNn5ZlnoCnW53JilBOnJiHAPjOnJcQWrwqYEyUFoU2i2/nHwX5IOQc655'
        b'nZvKf7oILHliABoN/+cactZz6pnItCE/W2rTAkRzev6n6R+nrzQmaH9nDK0O1MZqP0n31mUZzRmfpcdrXzQq58dplSkabbPhOHdyQObH+njtU6haF6u1GqqlZU0tx8Jn'
        b'Lt2u9Fcsivp65q2kZzxiqjpvujUMRst0qQkD32s5r+TtAYz49b6uwCVlokMVBGLn0UBcTNrxDqkz3kbq7EOoarQuxR3AzjJSSbZLkL9KOonDrQBqVHJdfKBSKRGoXHo9'
        b'eHjc8Z1iFKxrDRaFUXSAobZ8k9E+rcuFebc0vdZuoP1sblTKI904N86Lc+YCOUHeM4RS0iXL05odhi6ntDTBYUlL63JNS9OZDVqLIzct7ZF5lZxANUWQ0QcdZRQd35+O'
        b'/7YXL+d4Ts6e/A88D3rFoZ/obw7qRkfig6QxODYkKAlXJIOuyJAv2SwFWRYNVpFrMTq+l0ZK+1B38DL31J1nPkQC6s4zdZcwFec3SBb0+v44de+Z4EF1lyc5KAAXzRpN'
        b'asAiVAg3jFGRElzN4OTo+NmkBswwDMlwdRjeQzpE+PU4cobUMEX0WheKi/BuU2P7r2Q2aiZPrnz50/RlN6pwHT5XdaLmRGFr7MiizsK4Bu55I9U8N+M7CZK/ONCe7c4j'
        b'f/eDkmO6EIsvhgTHw8xxCUkyXDEcueJWnuyPxiXdEutLFZhAulxFuRvNVq2dCZ5aAApy46QgdsHlntClTIhdMr0hw2QXaCeBei4l30vQvEAjSS9pU/Tge9J+9RekPZLy'
        b'cQvegS/jzeN6JM5iUAiHhuZI8U58Dbc4/Cj7tpFifMBmjyTH8fVwKeIzEHmG7IpljgG3zbNC0zpyJZxDvAGRE/iSs8MXWjKexiegBT8DTRLEZyJyCh+eyZBcxwTb7E/g'
        b'I+QSHc6CyMnx+JID/AJSzCDt0DTAJ5xHvJWiNE9iKKsT7TZybiI5tJHOgwsRaZ/syuYhZbJ42vTUmnAZtGxF8B1fY0gK3IGbbMLEKZMoEgx3uj85ydaEG5CMtDvGkw58'
        b'mtIAnhDMvdwuLriYbMqkrbg+nNKBd8OY+Lgvmw4X9cf1NpvanVRQxI2InHHDV1nTxgkRFEuCD9IF432IXCSbRjqY86gg+/AxNuOB6HAnaK1HpBPYXyOSc7g/PgArdwNf'
        b'vNMFpiTnuYhxuM4xiMYVfHmFqxCJK8lZRuoziFzIwkWOwRTxMsjNlbROhDB1lLZCQiCBaVsZQRNI0yJXlwkYVkYZQHZz/Uingw3qR9ozXEnHeNJuZmhFHAdzixPi63jb'
        b'XBtpzyfnAz0oMY1csD8EAkbpDnJxrK2f+3JcS1romNe5SCC9lCG64UukwXWVYwhpIR0IGlu5MfhcCpOFKQAftLkKa8kOO0Wr44ZL8SFG5aSZQ212uqRzrrSlggsmraSN'
        b'qQM540vqbR7uUTnAFImMmzqWXGcNwIzzBdCQj697cEjSj4seOpnRN4uUkgZoIIfw2VV0YRe5UFIIxFP6SK2dHHZ1z9XgYrxdiiSjuGhcTS6Iirw7VQmqgisnUDXKRRDr'
        b'j88WiagMIXWgycbgCDnijaDi0TGi5rVNJDWgCtbxTPNAJ9vyyVk2kyMV77fBMtrxUdLoSXl4hovQxzCZkYZx+IyNdEDjNtLKGk9y6rH4pFLBwuGWtd7u/VGWFKXcyLkd'
        b'leLHgOVTfNY1SnKlKPxGzpJgpYkB26b49pvAr5aiXABKfPMYMN42OGAAvwkcxI2CuoEjNjDgLfuQVa6SEimKvlFwe22rjAF3qIa5b5NUSZHiRsESz/gZDDg9LMCUiuqk'
        b'KB16zk8IZsAvl45YtR4dkiIv6Dm+Vs2Ad9aMmvw6Ok7pLLjt/2IqAy6NGhOWK2mhdBb4pWbPY8Dzg8apDOgipbNgiVy9ggEbU5SLX+RuUDptfgOEKJGkqGBTs+R5AN60'
        b'LZFMG8GAg2NVBXskL1HibXUekjUM+Duf0LCv+NsAhJ6hCf0ZcGt8uPb33Dt0Rbbby1UhDOiROmHEQO5jAN603U6siWVAzw0RS+egr+gybbcT4jkGdIt9YlgG+g6AN211'
        b'vmVjGfC36kkF1TySwdptS4buimfAiaujkr/hnQEIY67zGsaAL+dNkUTyXjJgiM2vX4lezM3Sp29s5PwASFf0ZTgDFg2aMUmBFDLgku32UpMgLnPhLKUOBQIQZrcuzGbA'
        b'hVPmDPoagX7lwuwxheJEH2nmztrDPQlAmH3k5wsY8Ko+duhHfDTEgRvZtzdkpjBgQGzCrGWSFBmwLrtuxk2RpHmaJKdb/BIA3sxeYnpBy4C/XjFvzkpJugxYl317co2V'
        b'Acf4z08+hbIAeDP7dsCvXURLKYbIWm1zdTEoqe25gREdjmVJXy6+glwFj5D+7mCt/bmpQ2OY88ONYGWFpJ1cyA8gW2wS5jWC8RUwcmqy4c4EbKXdFgb56jnqAWq5kfgS'
        b'vqaUMhqGJd0ato5/0gkWm39bO1BU8m1Bzydv5aMh8t2w1q1TezNgnsdv5nyGYgF401q39PtZDLja/MLcHJTiBByw+kXYxz4+ZY9GSNw80h0SMsr+f+yFKAVy9HAeMzbJ'
        b'QbPOdHxoA94SgcuTYTtXSUrjEkNJKeSevunScbhtNSN/iqeEJUIvRa92i5zeX0yYIyTOCPZA4dHGjWafaG/E3IqGlLlqwjQw1D6yJxlSN2eylV8zEJcxh+SPi624ffRK'
        b'fI5m8dxShE+TKrxJdEg15JgpOBAy35KwJBlyy8zykHjiQlLBhEq2xOMa3B45DMiIQlEBpEqgbGOEVEVI6RIV0UvWhkgHR4tAr2QnBNms11dj1iaMnheD2ChR6/F5vMtH'
        b'HU71oRppzdMdNC1Nc87RsIy6ku5oNbgyLI4cJ3W4OZBDCrvMA9eNE1O4PRqyiZRPU0dQ/FqUIaxlLJyCCxcGw0YNdsNkO6QvFaFhcVI0QCkh2/EzuJTpqwyCfBuuxae6'
        b'9ylIl44vi6OeQblLyFU1bqMbm4PInB7K4M4QmPd74Rq1miIcQJnmBAbPXor3TSJ71Go5VWq0cio5L0aIU1ZS7uqsjqTd65CelOJytlvHlQNxlSaekpZEdiTH5ZCdMuSR'
        b'K3nSNEHMZDu9R+KqlepIOv9eZMC1wSLePnx9mSYBcMJIRTCHXJf5400QQzJxhZJnmKOi8V4brldH8rQ3Mk6CEExJySZX8bVUXKeOpDTWo8w83CYKuWNIOinX4CZ8AZgl'
        b'Q9LhHD6Mt0KmwLZrTSp8OB4I4VhulJWaykxzo5s0OA6EQUqTcLMUuU1dNFLiSQrnM76qcBU5J8lQ4w46wCFkBos+L87VgjtVpDwhH1+Jp3slCbnG4fonySFHErQmwOqq'
        b'bQlxcYn0tIPtTuneNDAUbyINyqDEUKWKd8FNBsgcn8FHAwPxCd9gJaQbR4N9cK3vQHJ0ED7GI1zm44UPDdKYv/v555+Prxb18JA13e3VqTOQmMbsh5z+enDShsWqWCmS'
        b'RnP4JOQlW5U+ohe76rfU5u4bKTioPzrAjSK78RVGvQupopHbgxwl9WJrB6fEjeSIGPT3gPdrJ+3uGwLExmtc8IhsMb2owJc8bB4RZLfgEP1YANmJxVQM9lC1M22rcE20'
        b'w4UmsJc5RRY5w+YLgw1JA+QDa3FjPjknYzncCEhwdjDEgtG5kIkNxefJOXeOpVQTvGG/Q+ebimsHuXqA12xzxZXgcZdxT+ES3Mn0IAifFGx2U7BLPk0Zr3L+C/B1hrQU'
        b'N8Ns9pnkmks+nWszp8AlpJpREkiO4lOk3U6OJQogWkC8xg2FXUK1mPptI9fwYRts/4tIm12OOLAMUjlyvHhAQIrwFjABsskdNiGSJ7jYUFgAnTCPbMXHIfMNJjWr3OgK'
        b'9nHj8F6jKIRG4HonrGG7uxvsbiSTuThZkMivJtKhJ+2ey8hBAXJQiQf3RCTezZASV6ZAA9kC6RaNMyO5GVKyWUSqXrIaeHyVXGAz4Q5uOG4byZomP4l32VzwJlwmSq0a'
        b'll0azExJG0M2u7osxoW0ReLNhQ+cJ1r1LnIhG3zjYWpKISgE78UX2YqW5ZEmXO7pssKxKo9DUkjtcAUpmiQilUWT3a4e2eRSz4LSF5tuvNsgtdVztPXK8uqpyW9Ee23L'
        b'zHs18unvxnaWV1ZKzxyr2OrRb8Rv7KbAL660XFJGx4zb77l8s/FUYLXm1cCiiu/m+Hwv+95dOcr4q9dzX/jiM/WX19TteR+eaYz84yBPt62TVrvdlYVX/3qz22tpba42'
        b'3XJb1qGi5/LjR7resbtNfPFAxnBlduv67R67o4d98E1SQXJ2hdY8L2jk0hMhx261mXa+cnnyiFFvvvvNH57yDfhE6fD+9jBuO+JZpEx7rezrW35/+f3MyKIfFrYN/HXe'
        b'ztqf9W8rW27NST785sgTrf7x5wbVzf7DXnvYF6qM/Ozr4dWTFhyrfPmvNW3Bhh+fl2v+2tbg/P2V96pO3WmcYN647bXiv93a/Pf45R6Tfd9aePvLG7dli14b2zgqr8B5'
        b'g/m2+6bPFQnNV8vuJA96eRX/91v/HLok5cKupV/gC3cnyO98MoA/mPd9dt1b321vH9tU4zvulcnWZ1//0zNTMk+den+28Y+23OfPq/Om7XeftOvOz6MSz2945c9nVw3/'
        b'LrzY5ZvIxS/t/0ey99T98XtCV+b2a/p0dc3Lx58rOpU7Z7rL2i0BLRvuylWvNA3Fe5XOdnqwLMNb6SlPSBK4JEj8wfWCRewku8D5WuPsCubTIZocJI3gmEPjQoKUoXR/'
        b'UAo7KoV0BdlKTrADAlxkxLvYYdEFd/G8iJ0WzcU77OL2E+9bGhxKSvyNpBQmkeMdvAqfn2yn6rVaOUsTEhgbQbaQCg0HwegUvwafltqp7o9IJYc0cYkQS8uCEp2QXMo7'
        b'p06006ObVf7r6DYehiOlTmBX20mlBA2YLCH1QESDnUWbill6zUayO1kFxpHHzSCbnZTOD59UPO6hlD2+/f7phrd4umEXtBabVjzJZ4ccq2kyNNOFc+bknA/nxjtzbpwH'
        b'D98kFObNuXD05MuZc2Efb07+s5R+eC/4recHvvMe4nfexUnO8T/LeTf4zZf3gvGkcik7O/OFpxx+/GB8+t2DE9zQ/ZM0t96k9TpWefzqlJzg3rM+NtQs1HPAct3n8Qcs'
        b'QdA+bURs99FKGAST3UoIhsFJCZDkUekEy9FcfNoJAlsH3qnkmPdYa5+oiQshZ7MhiYEsDdfnkp2PJKzuPflkCmIJKz3SR48e6hvd7yWw/L+UwEpYAiv9Rw5M4KLo9S+F'
        b'ytSm0D54FcPud9bkGhSJqZMiwhVWgX2ZEPoA6gO/gP0IBrtDsNCxzCabnQ6RobVkK7Q6ndVhsStsdq3dkGOw2G2K/CyTLkuhFQyAkysYbAA06B8YTmtTOGwOrVmhNzFx'
        b'agWTwRaqmGG2WRVas1mxYE7KDIXRZDDrbWwcw2qQvQ5GoX3MDwzFjlfFXjqrJc8gQC96A+WwmHRWvQHoEkyWTNsvrG3GfSrWKLKANHr1ZbSazdZ8wKQDOHSwdEPU44dQ'
        b'AQ/1BiFNMBgNgsGiM0R1z6sInOEwAu2ZNlt321rlQ5iP4oA80tOTrBZDeroicKZhrSPzschUBHSZ9+ebCRCzwWRfq80yP9y7W1b3O2usFrvV4sjJMQgP9wVohkHovQ4b'
        b'JaTvzhlasxZWkGbNNViiGDsBwWLUAuNtWrPe+mD/bmJyRFpmG3SmHFAFWCllVF9ddQ6BcmjNfWoWk6NZgsPSZ296Lh/FnjCmQ5cF3WzwmyPncVTrzFaboYfsORb9/wGS'
        b'M6zWbIO+m+YH9GUR2IPdYGFrUGQaMmA0+//utVis9n9hKXlWIRP8i5D9v3Q1NkdOmk4w6E12W19rWUDtRjHXYbfpsgSTEZalCBO9rsJqMa/5H11TtxMwWZiVUkeh6F6a'
        b'wdLXstg9xi+saqbBrLXZGfr/jUX1TiSi7oWz3rHonr/LtdrsDw/QrRkGm04w5VKUx3luKmuDKeMxFNPIZdf2KNdiiFwwldn8GA3rnvS+Oj441+NV8z/Nd8EAURSMLkoB'
        b'XgZ6zidXdNkZ4gR99ae+CBaflm3oJaoegoAFZnLFZjOYfwnVDgH+MUzsHof26JvYRyKuxmHRGyx9R8zuaSFG9hGrH5wY+vzSGJl5D8bduVTa5KjRbgNPZYQkhjb3hZgr'
        b'gADA52n7njelu9lgUSUJoY+j/oG5H6G77/jfrQgP5QAPID82HxBxTTB134hxM2ckPV7t0qyCKdNkoSr1qA9J7m7LYAoJBqyIEQw5+vzH2nrvkf8FhRa7/yedSZYWok2f'
        b'Lm+uIYNcAbPuwyf8DxBGzYDZGfVzD9CVCi2/bGwWbY7hvrfrzosVgUkA7lNPHUIuy4sewVhkEPINFj01y7X5Bl12X9g2Q642qndiDQP0yur7wHjKYlkepVhoybZY8y33'
        b's259732AVq8HQL7JnkWTdJNAs1SDYNIpTPpfyvCjYGurzaFuE2hKzXqoMO1BxKjufU4U7Av6igwP9n7gxoDu7HzRwzcGsWKhT6mSp7cBsXOc082vjwsRz9sHzGWHn37v'
        b'zE5PsAQuROxQK3H4eNzO40rShNBkNBm2nKWs81c2OTuc/zg0PeG3mQ7ETtTIFXIUb8W15nsn5GTn06wgxGURvhD8yL51RMBUuWyIi5fSjdURqNaSvaQ8LD5OhcvC4hM1'
        b'qnhSoUmSeU1D40mFPHgS3uygRyv4iIDLg++3I298AFetkeAWfNTCjr3NeJerJh5vIU33TszF43JJpHiLXkdK57Jj8URytOdknCdnxi100P04vobPklpSHkwqEo1kU7yK'
        b'R86kk8dl/rjZMZpRQMpxPT2PjyPbNbAtJ5VhsaRCggK800iplNSlk0MOWrpGGqctUtt7daQ3NKX0cmR0sGzKTFzmGEsPbsnhQb36TMdlyeJdRlIih5T4igzvwyd9xFKL'
        b'bZmh0P2BqYFlcdBxdLos2pUUivPuWk4uBIeSCpgxND6RlIYo5SPJVjSU1EuB+FqeCWUV3haCN5OG7o5xiaQM+qFBA6XhnuQ6GwhfCRnRl9zwRXxCNmQ03sWUJGODGzk+'
        b'VT2B3j7sQXrcCNhUUnpcT+oekhQpWUIlVTWQYXribbhxtU49QcZuGbLwM7EOWvRIavsFkhqnGZ4IhaNwfFDD5DoYN6WCXBvJtofkOne1eF9weGE0Eys+xPcSa/wgJS+e'
        b'617Hm7zUuC1XjrgEUo+vIXxmTXp3zU/KUNIwDRoRu6rJjtCyKVX4iEbUBNzge18TyE5SpJSzs5Zla+xqda4EcRp8Hhcj3Ixr+7EGtRSXq9WkRYa4+dM2InyObBdLGIYG'
        b'4lNqtQAoyRm4FoGyFZMLYjlCB9mSDzhtgLMoOxt+98tjKHZSRCrIIXxFraY3K4dR9kJ8laHMxBdINa6Zq1ZTFh5BZjWpYxYaPn4QCgFzjglM9y8pWIsYX+eT7bjDxg0G'
        b'XZqD5ozHF8Vr+cD+tEAypbogPcSuzEZKiWhoV8h5d3qrUhE2BrcwfjqTOh7vAvvZIpaNHJq2ThMasl4VRAWMz0iR5yKJ2Y1sF9ldic9P1rDyL6k0EZ/l8EFcNhpkQVck'
        b'H0c6e/h2BJ8Bvs0l18Trj4t4/9wexqWTYsq566SB6WMsOZ/Rp92RQgXY3cBpMDq7s2kn7RndPAafVEGZXEROiePXL8YNPUx2wjXAZXyRXGQltPgk3oQL8QXc9DijnYtP'
        b'MIUJJafM6WTHPXmsIIcdSjrCcbJ7Qi9k+H3PI+ZMKrFYmJKKG6bgGnLpnvRItSsz9KWk3p0U2R9n6LgzleFH4f2JVrxJrRYvHrPwKbxNvJvXerBSzjh1utkpJxUpfRj/'
        b'fHDFAE2cKikUTD1QtGdJlg4NxcVS3ER2kUqxSGpSf3qbphz0hCpOivo58XjHMlFq+OLMgB6J4gMOkGgoOSFezl+IGybqCm5a3UtXgjOYLjgFrA+OH5qu0qiCkmixsWem'
        b'xDBmJXN/uFJBTjx4ewu8ws1Schw3oaEJUlytJxXsmhdfCyKnH77o7b7kjZ8s8wAfxzw46ZxgfNjvnJ1H/c4lOxvIg2ydKN6n4h0QatSk6F7fIJ0MuHhRYHdV+UM92F04'
        b'mHb1vbtwsodzgLmgkWQfOdbr1li8MiYnyV4J2Z4OrpiRcp604rOaeL91D/ks0popdtgDxJ1jboucLujltvCedWK0Kib74VOe0HMHSrYlcbg+lLQ4QihPOkkTPiyyHpBx'
        b'KRgFKUugtwUA5Mi2pWgC3iOPI+XkKDPa8aR+BSwpNmRSQXyySo5cNTw5gI9CdGVXxlWB+eyuFgY6e+++VuJJOmSi9ZwNwptIuab78pfs8Ofw4UlTu+80C1bS+/8BqKcC'
        b'QOI5iWcX7OSwL6nSmfusUQgnx0Xv1zRtQI9yTZ8IujUMH2RaF2FfwfRRKrunj24FDi9ocZDSAFd+iAlBcrPADl6UCm0muSwLjicHZj+gbVoL+AZ2tVYIDrPUxtEbDeYG'
        b'lXibqNz7I5KzcIkrLXYlJyB/IZdJHXOb+LgylNRwy5fQWlHVYHKQSW5hFN4u8n0wudBL5cGbFDIjxAP60fqKJ/evTA85EZyOWPKQg4/h3X2p+4CnRWVPwt1VZlW5EGZL'
        b'STupIXucqJ2gNLJfxWyGHMHtS3opMCjFoYc0+DS4GOqojP3H28HDtodL6DqQ1QzDL6TEHR2VbQOtIhVx81JwW/iC+aSE1auHqgJtziDAoO6L9QXUUZSELIqlkmOqMS82'
        b'hLaA+9AsTCEVUgis6/rjCh8IJ/QW3RVocKZVPAnpbk8OtyJRAfaGJZFdg/pUABnp7I7QkHY9A+lXewQN0fMmgYBw8xCdyI5mfJJsok0cxIWUURC7wUbKHBNp27lhq0kN'
        b'LomDuLyb1OKSPHhU4DLcHInPyHBbxnx7Bj4/kaPSOog3y5fi82CeVOZeq4HH3WOSY0/BoHifCeIf1aP1Q/AuTU/phDyNx+1zg8glfFw02824CrdoQoMXPxj8cCe+wAxp'
        b'Ngjukqge+ebewfP0BjazsGhhzzpxaxrNG66SEuZXNKmk8KHkbUhBT+7WAi6OJm/Qux13pqzqI3nDl5YrpWJCXjIL71RHroIwGD/TiS7uNL4otlzDdSuAZY3qCDnL2gzk'
        b'bCIzD1/S7qeOyAOGROPKcQi0hdSL2dURvB043h5BWhBETnIaVyPcRjbPVnJizN22agC0jofGGHKcbIM0ipzH7Y7ZFLdj7TRXyGDKQfjlYaRyAWlxx60R41NiezRwvmrR'
        b'/N5qNYl0UM0C/T7oAn52H36GWeLoELILn5I7NCAetB6XBYu6cc0bVONUJG7lEe+LO5wROanBxxjG5Fl4Dz4lw1tAvzagDUsk7K2GsbiadNpYkf78QHrfSS1x8QNKvVhF'
        b'9pB6J7xrSoEjik5yzJc0uCYlkgrVItFUhmeBaSyOjV8YmyquB59IISWJqtCkhGQZwsdIiwsuWo6Pdtfa4MNTxpIaGW4gl9m7DGNIqZhFFULXElIEDqcGN8uorSB8iuyf'
        b'AHhM1S4sStaEAhOuPKRqe3AJG2CdxyhR0ZYP7aVoKfio6NaOeWTQItwOVvdxISiRi3DRO4KZVCCyVDw2dODj08TQgVv7s5Gigsw20pHrKYdxSvMGcGNhv3ZdXMI+UzaL'
        b'KWvwpftBJYE0smQmbQa++HDWgQ/hsz15R0sMKwUzvXPuR85mhK9vFH3kSJ1a6T/Hq/mnuv373+y8/OY/3v1634ctFX/bf/MGJy9c2jI+c6vzCDS6/rjeqTzm6bCofn9K'
        b'fGdgVm7E+GWNw0rRCP6Duhsjx458b9xXEn/vry4Zv1zvHXNk74YfL10+eemTP9caZ0wsyLQsUDxz6KuVi27WGvec/OAvmTd3l15o2mfKb/3TWy+mtrwVmpro5/6pu8ut'
        b'1/96d92oln2JzUHv/ySNNN9+5c62fnFZRX+68OTerG/LF39h2bvmueYRL9SOTHb9dOGweb/55u2PIldF/V5y2vdY+hH3od8WlH39Wt2ND9+Jemd47qvH7n7w0z+VU/Kz'
        b'HbN0ydPGrl98K/Xch24pTeXXc42Og0EfRuEz/e5Ovn2g5Wvvy52//6Zi+K3jf6paHf6y2n399rs7VQvSX/jVyAPKFQeHdr6rE35a0LrWf0VY4eteL/bL59+YlEtK5d82'
        b'54676X5jqseLF6dvHRo3e3L6Qa/Ij24dee+Fpl/N1X+S9eJ7JPnFV2dd+fVfqnzj3MstBabnQq0dr71hlPgW1CdXlN4dEbz2xrHWt8LrR8xKGCzkGg/fnFrUYFzlH1P+'
        b'ZVvzNx99WeqREal+u9T3+8+myVKfzfdYn7z/S/8vPonodC8Z80HdR8WXN2QZf4j4ovnN30/bo17T9O0Xz/4mdPFEexOJj513YuDb+5+7+GJF06IrY/Kzv+743YUhyeW+'
        b'B4vHuq3+eOzpjPUx57iBMzd+fvz6e9P+/uPpD9a9mq1/Cy0PLA1bbfMffOnIvh9/8H/row+fDvoovmEdtzDyi1+1XY5d43TFI7vpH9nlkRkLn7fM7lhU8sTh5mXv/q58'
        b'3oIf/jB/clj5R182/TTIc+Bdl5ciF6UNvHvdd9Q7mi0bg9eWfD7x7b//ZfeKW6+6DCk4HjR56og3v7tkf3/6jcFpZ/5sH/1xxbbnkk6efqpo199uum9+e7vuM+OG7Oln'
        b'0tbZLwz/Ifjw9YsuBwMCzn8TvvilQ77Dxu0YE2Qf99XCd5KePT0ub9KXt74f+dHXfo4//qpxcd6SXaq3Cz/53G1jU33+rJ9P1Vz76O5x9bV5I2b9wUc+4seSsvbd15ac'
        b'+GyPp89zx34XEDPw/TtbXa7aZiv/8Klm1w2yqzNmonz9wvfejHHv+qHD/vGms5vbvziQ++WhWZ+/dfU9t69CLQcTpr/zaf/KI//MGzD7g8/HTIgYq48tP+P97cRXhnx4'
        b'u45cffnl7XEfen/7x3Kfn38Y9tdZv7H86KpON8XqI5Uednam0KrPI/txNa0jYWUfzAeCDQ/CHdJYSML32tmpSDOuIvXBQaFKSC5OgiUj1G8pD9bbigvFl5+2jobd5QFy'
        b'vY96liuQeNNcNoAU4q3dE4nlKqSCU+F9+Iz4btTJdZDfhwTG9iNV94tWIFc6ykhYHzVYLKkhJ8iVe2U1kCovJWfFmppNMNPue/UrPcUr+FyChNQvwVftLI7twMfswUmJ'
        b'IUn4TDzZQcs0O/n8dHycVc3gLYvJGQ24wTAVbFLzedwyPRRf8bfTkJ6PG2drSIWeVGnuLc8zXJK5jlxjuOR6AX6md8YwTBXEA+2sVOfiOgxRXckYJ8enedyIa9USLRsY'
        b'l2XOZu8BQe5zjL4L1P0ikC8+xdZFGshJfBnXroecYrsGUrDcntfLpkgl+KCzcsC/Wn7zX3wo3f/74zzy7lKOfVJEOCvriaa1KRvREmdO2v3jwkp46I+U4zk3zpuW5sD/'
        b'LjzP9fnzjYuHMyv9ceb8WDkP7esH/3v8KJe5cL1/xFE8RLzHjSf+fCof5MEpOFogJOW8OD+JF+fBio6knD88fWAUL97rZxdOzoklRlJWTgTz8m48pcZbnJ13YXPCh6cF'
        b'SXKe1vqMBIicUiPSBLhyXixgcoHR/TgfaB8CM1AMWuDk8ZNcKq7Ag+8pd/LiPXg2Bi94Ag+TeuqTpPR8uVdd0n9ffkpO8OqRIJurmkqOpqJoE/pq9C+/ELiGPBP/9LTu'
        b'IiZSqaK5H0JDciWkExdxj7yyR9Uhmg5Pa4oN9E1ytIzXc8skel6sju/yYqfmrKJImCMIVuFOgHiOzlRL6C4QMugVWovCQNtDk5TSLue0NHrxkJbW5ZKWJr4yDt/d0tJW'
        b'ObTm7hantDS9VZeWJurr/QdbN00oK4E6Vo3mzLMzo0C8jbS7epALdtd+1POA00lSCd0GGkYOymW4I1rJxZh+//RVmW0oYL+yPndqZWcSSfGa8/bX7QMmu772/taJnwX5'
        b'TN5a4Oo9LCCasyt3JPRXyi7OPHxz91tq741Vlc95OCeqv33x5Tf2hn1bkBU0NiDug9irUw1TFy0+uizRcXexLvOA6f3ZC0J9fn76jPL5u/y3oV/PtxxdUdz4bPkHx9b7'
        b'vL/DZ+ng6ecCZ0+wHXzu4ks/v171wfljwZd8A8tqM56Y98YnDf/kywcHte65nXpi3rEZNb4566Psew071vgu0ZcO/+3plt8M+dTc8mvf1z9r+e3wu/65sRv/oBk919+G'
        b'lZkDJree+9OifU+98ucb7zaUR7w63rEgXLUgoSbsepPvX68c1yjVNW8dO9c87M2XEj93Mpy5uONNiHTaT77dMlTemu51MnbOhP4lTu9e/QHNvLNI1bxPKbWz8vPhpAl2'
        b'BqBET8LmZAO47Bor85QrJmU+8oKtdLTReQ5pZcFMCTucS65B4ICp++/pFRKGAnC7lJwlJzR2dkBeCxupazbcHJuk6slIUX9SxZND9JRox0rQdqb03v9GnypnWe/jH8xX'
        b'gsqarVp9WhpzlNOodfhSpxXBDf+Z52mNIrhG3svZy6m3i5N+L3frdmF35c4+ydSFBm5E63lOGNSj0WBFPKj5fR/R/9+zTE7wu2c/dHK6zxfrHj8LfbzXoBnFJHLdgMvp'
        b'+QgpTSbVsDXBpbjSCXkMlgwjh5xNaU7Pwn4BOl7InD/s1niPLdFe217eaMx3t2c0bXun8Qp+dsnp5jf2N9nHBqxzvXji2cVXW1L+fLpy0bq7xhcGpS34bsMTRXNOfr9w'
        b'30+Lp57bGj6haMeBUZJxDepBZ0bHjLVUjhBqra+aWy/f+cjzuZf8LrqPUTqxCllhTiZ7wTWZ7pPwMVyucYJw3cZDplSOD7Au02ErV6FJVpFW2i9ZxYNuXZHoQiHmX8VH'
        b'WLZkiaeodG2gzvRFqERcwdbmLRmOz+UyK1i3guzSxCUGkc2ruot0080sESK7I5I13X+9AbKy0/SMy1XJkyq8fyUzE9Jhz+r58w46cujen3eYSXaykXEd3rk0OF6GOA1y'
        b'J5dIHd6f26Pyw//NucR/VY+kv2gkJovJ3m0kdIHI3bmnGFgSshHRHyQMvqf6ii6J2WDpktLC0y6Z3ZFrNnRJ6Q0rBE6TDp60eLBLYrMLXbKMNXaDrUtK60+6JCaLvUvG'
        b'XrrukglaSyZgmyy5DnuXRJcldEmsgr5LbjSZ7Qb4JUeb2yVZa8rtkmltOpOpS5JlWA1dYHgXk81ksdlpxVmXPNeRYTbpupy0Op0h127rcmMTThBvuLvcxVzJZLM+GRk+'
        b'vsvVlmUy2tNYSOtyd1h0WVoThLk0w2pdV7+0NBuEvVwIYnKHxWEz6O8bt7js4QJ9tUgYTx/07FigLlOgDlGgN7bCOPpgOk6vMgR6XCmo6IOeOQr04Fygf91CoLm6QK+I'
        b'BFqeLNADFYEqtRBIH/RtJ4G+oCXQ8CjQV60EBX1Q1RWoegr00E54gj6C7/kGKp1+93zD9zGP9Q2s5x3nnj+E0OWVltb9vdtV3hlifPCvxCgsVruCthn0SUpngXogGue1'
        b'ZjM4QKYV9HymywVEItht9Eq/S2626rRmkMZ8h8VuyjGwJEOY1MPKhxKDLucpYjoxjaYuLG2RUnsVNc/LB6h25v4DnJyY3g=='
    ))))
