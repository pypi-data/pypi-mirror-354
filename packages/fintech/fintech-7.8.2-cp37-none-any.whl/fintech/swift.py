
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
        b'eJzVfAdcVMe6+JyzhaUjAqICrqiRZWmygIq9hi6Kgn1Zdg+wsuzCObsi9g4ICAoqgg3FgiJSrFgzk/qS3OSW3BiSm3CTlxtzU2+6uSn/mTmLgmL+9733e+/3nvvjuEz5'
        b'5uvfNzPf4QPQ558E/0zHP8Jk/DCApSAHLGUMjIHdDpaynOSY1CBpZPjRBikn2wby5ELYMpaTG2TbmK0M58Cx2xgGGORpwDFX5fAj55SWET93oTLfYrCZOKUlW2nN5ZSp'
        b'xdZci1k512i2cvpcZYFOn6fL4cKcnBbmGoXesQYu22jmBGW2zay3Gi1mQWm14KG8wCntMDlBwNOEMCe9vx11Jf4JwD/OBP1s/CgBJUwJWyIpkZbISuQlDiWKEscSpxLn'
        b'EpcS1xK3EvcSj5JBJZ4lg0u8SrxLfEqGlPiWDC0ZVjK8xK/EPzuAEq3YEFAKtoENI9bK1wdsA2lg/YhtgAEbAzaOWIzZQwmVpOh7ucfgn0H4ZzBBQUo5mAZUihSTAn8P'
        b'K5IA3Jb5k1Nm0svCGGAbjRsnTkCdqByVzUuaj0pR5TwVqgz2il+UGioHY+dI0W10E55RMbbheChsHRsixC9ZnYx2o4pkVMEAp3gWtqGjqEnP9BGfZy8CKYQHDObC/4cH'
        b'2Z52WplSCaaVxbQylFaW0spsZO20bn+U1pGP0TpdpLUyUw7qAv2wUDKTtq2YDmhj+goWfJnngr9lhkwLkouN6mJH8E1+IG7LDFmxrlhsTF0rBYZob6yKmUlfjWNBMzA5'
        b'4ebZeb7Sbzxxo/GbsV+xl8fZCvcCkyPuyM2pc7/JZLrjrsh3It/Of1lsTg/6asWH/kEj2NQe5pfFaUIg6Aa2cNyBGtC59Zjt5eHzg4LQrvC4ULQLNi8MQtXwQEIyqgoJ'
        b'iw9NSGaA2d1xCmwP6sdeh16aIwh7CWtBtuQBA5nfZGDOowx0eIyBziIDUyPdWZ1kAgARmaagIUOBLZRowNnBwzDWFepEVIHKkubHxYfELwKRiWnesHYhLIf7wAxUkSNz'
        b'wCpxyME2hMy4BLeirRpYhs7DK3gN2AwKPWGdjazpnR6mWc7Ai6T5MMhDu2GFzYswpw1WpWnQSbgvkkDYD/STHG1EqeBtuD0B1ciwKoN18HBYymSK6ntW56UsGwSAR6Yp'
        b'fNVGUYK+UYOzmyVxRNaTJaFrgHFoeaZE0OHfN03c/0nmvcxV2Um6V7LD9gbp4nR/z/TU52ablD9lfZqZoPtdtmpBvE6Vmqg7z51hzg7OuWdI0C0De/VxOgu3V7rrZNvp'
        b'iJlLKlR+yvTYr2c+n3LKbW71tWdcDg0FC5O831/yjYq1EjcA96JTM5wxp1TJttBgtCsPHQxngTcskSqyUamVWBQ6koB2YobuQlWokjAWG+hEBrbDg0+pmG42SKWS8EQw'
        b'fR4sfvzoMzmbt6zlzMps0YmFCUXGbOvUbifqobQGnZUj4wSi6iDQhXFhPBgFE8Tw8l4QKkm3bLXOZOO6HbRa3mbWarudtVq9idOZbQVa7WPrqhieqAovIw8CZRSB70bg'
        b'v+fByhmWkdOnjThDeMSAmtRxIcEpsHJefEge3B0vAz5oi3ToJLR1rp616590AGXG/uKBMrPUG0iwMrNUmSVUmdmNErsyZ/dV5l6A/ZVZnkIVB511y8YGVopqsM6HgtDh'
        b'KrH5lD/auxG1oBpsV+EgfLnF5oGbE2DVqtkKu56FjY80flQoSIUw3NPw2qpPMpfeqYZ18GJ1c03ztva4wB3XtsUfYl7MJhrlkt2TJAEHKn6qUwTOwW6TCnkErIc31Amh'
        b'qDQ+KUUGnGH72kksOoxdwHa7KAaSMeV0t7Mo0GyTRWelEiWqDYJdGCmWJ+/0QJpSKp1umYHLMlp5Mogn/kfF9pEgy5PA1EeMZLr6gRjf7CfGEbglfpbQK0QaIUIYsADu'
        b'HJ4vhXuwnzptw+4ReMED7sIm2GmNiZACNguzNBg20R50CrW6CQmoBXcxgOUAatZPEn3CsSnovIB2uuAeCWBzADoHD8Au6hOWTYMdQtoG63gCzowFpx9p8yHQWkbHCbAj'
        b'FnewgLXgKeg6rLL5EnC34H7YKSwxo4vRZCW4DeCQVjlEnHdLM0cI30i6ZLhrO0AXYVMYRRB7k/oCISaOp7MwyJYo7IAIRHQataxCnTJ0xDaO4IH9GuqELavF5ZrgrvX4'
        b'1/JhuBPjgv0Tuoj2r6EwFWjPCCFykaAh0zYB1Irq0QHakw0vxKLONSvwJEwzrAfoqvN8yg4f2BCNOiOScI8D7mkA6BrcCjdT9OcpUQ1ea49ecHHCa6FLTNRMeJZOQ/Xw'
        b'0EjnsWgPT1kPTwF0JRwTQKZNzUFtzvAsOobao0knjtWSmHxxWouLizM8AS86RRKy0X7GETufY2JfLWqf6zwtAV2mZKMdDIO9cJdtKCG7At5GZwV0AN1CnUVuBJlGRp0H'
        b't1GXnYRa5wlT0x1dURsBepuJsYbZl5u/0BmecSi0ocsA97QzY1Ad2kEnwVot6hJGuznzVjKpjglgC0T+V4aifUIROmZFV5xJVyWjhiXwuDir1C9YmPWUmytmiETGTIHH'
        b'scLRjt2slwCPwWY3VzcGSByZ6fNnifHkoswgGJPdXAsJUVeZMB+4n8okdn6aMzwIt7kWwAopkIxipo/CixA1RLvz5wg6LU+1pgCg8+ahos5cwFGqQcjwssZEyQGbjZV6'
        b'1Gzak7gKXhUmRWLJy0QV7IBnQygLrIGoTUCX4lA76nQnfGtlouaiKiqoiehqkFC0EF22d51lNO6wU6WkIWxPnCcTxYKgntVTDL7SO9G00SfXi5nAAt+e1Quz6iYey6SN'
        b'Izf6MJNZMKFn9awNvrrjE2gjE+DLTMfeocess9wt0qbRxvuDhjGzWaDsMV/S3V24fSNt3J7jz8SxwKPH/I5h8apoMarm6QKYJBZE9Kx8r8BX4W+jjT85jGRSWaDoCWgo'
        b'WuzitIg2rjAFMgsJnm7rubsb28fSxh/ixzCLCZ5T38hdPMbZlzaOGP8Us5zgaR5bdLeoOZ02TolWMZkET9W+3LvLywfRRl1AMA4CYHqPMclUp76ooY2Fc0KZXIJ8/Nur'
        b'70ZNCaKNpVPCGBMLMnscmyx1kXJX2ug0KoIpIBSpNmb5rmjS0sY2Pw2DvWhqzxK/TF/W5k8bD26MYtYQMh1fXn935G2Rn1eWxTDrWVDQo4rPuet5O1wUR/4EZjOhXXV9'
        b'7d3xKjltVKybxGxnQVxP/KG1dfk7h9HG+kFTmFLCEKNiVV3Q2YW0cXLWNKaCBbk9ji8W+yrXcLQxa+10pppwyfEPxb5ert6i4KJmMrUsWNyzBOUv5mr8aOMxy2ymjrBu'
        b'6LjcxWv8JLTRNm8uc4gFa3riC9bdna/IpY0FmjjmGOFntHbd3UmN7rRRuzCZOUNYx+01LF7gJErzjkcK00JYFz1RXxcdaaKNL/mnMm2EdXMqsuv8tiTSxjULFzAXCeu8'
        b'84vrUjMdRWPYBff6CXPRbmcnYnAuzHRndIr2+KC9fs6wHHXwbq7YSgcxU2bBRtpTrFeiTi06hK4UCRLqKdRBCtHod2OH1SZwEtQpoIvE6muZQHRGoZJSDKLWPc8ckmBS'
        b'nfP0vq7hSaLeh7/EHMOxu6fo37IWz/YQRbJoyctMkwSrztid1sXTklaJnJrxCnNGgukf/6zFN8srf+CMOgoAcctGNisgW/af2ZaQ1eSPJSJPpdjIXiUcleNsoHwe3kFV'
        b'obL45DBUxsAOnBb6ZErHwptoH0X2tYk4DwyJxt8yXZgIZzGhTZnjCDxSYxmyT3FXLgfUK3uguiWJ8ag0PBHtnoeTLAXazhZjV32WepdQHnbBTngRp9iqsYBZAmALrJ4r'
        b'uvMSuH+wOgjnpaXhKahuigy45Ejc/dEJMTG6CisRnorRn7gmFsQa3XnCJ4rHP/DWSOHxe2ybmS7PzponNv6SIwcuyvuYwZku58P8APW7TrAdNeA8fhTJ7eBeoINHXG0k'
        b'b0Q1aXwiTXqryFYyEVaFx8PzQQxs5YDSKnMbgQMETSE6sU/VwKvJUTRagCx0CZXRDDMUHV2lxhsnVBGnwTtRvI+Kl4LBKgmqmI9JIKyHh2FnukYxpncLMRkrIE0IjqTD'
        b'k5opOE50kH3HUWCCDfC6jWyaBZWfZhanIROOgBwvVC1Gj2vw8DoNl6HBQoWNYBXag3aL2G2GO9ElDWzfFEOm1AHDLMx3wtyA9bAhMYGglSKKxW3IxgLJhDEK0Wx2KJZq'
        b'UC3cEUMQOAg4dBPdEjfY51EJrE1MwrPCUaV6cBwD8M4GtcKTi1UspWp58loNaofHYrB94xwiey2eSVBfNzNAk5UeQ1BsADkmHN+oSW1lcQpQjrcgyTIgDWDS0RUcLS/k'
        b'ULo4HKH2aSReMdgS4CGQC4+jEtswih88nK0mAkFlKfD8SmcpcJkicYdbnhLRPx4GSzSwGVv/ZZrMAdNsP0r2aNg6C5UnJZBtjATdYuBmeBMzt3qILZEESH9WSIqPTybH'
        b'DA82kEFhse6q4OQwVSjrBE9y8BQ6BZuCgmCzj1oFa/EmwgvW+nijpiHwNIv9jZcHPIYjtumHX3/9lTFjPVz8mQPWw5AoSTAQKa5fiurUKaFxUiCdzmDObYNnYQ3cqfKi'
        b'uAfCDq3gytuI5znCoCZ4ddRQBeXGhNC1qNNN7LnMjPFUZcMaEeIWtB+1oU77rFuMHzquRtUTaWj3xIbSLuBportCZ2DHCNgwW8xyT8PTOL0ptDmRnPQ6sxRVK/VYsX0o'
        b'D8eHCehyEc5MaHK2Eu4fmasSDfNUAV6yE3e5MjRfKkRXI+EeeJJisxHthO3Obs6wCrvVpQxm4sFlsBFWi6pdpU8UrE5FJBu8yeCd9y6/GZgKQvhKuMWJdJHltjAp+Uq8'
        b'WW+jEFdALAjUaeXRRZKX3mI2JQ2HZfCESPxV1Ii2C6jDKof7UTtgsGGgKnk4hVk4F6ewCle8i5CMZ7AptMbBymiR9EZ0zIA6bYUuhIR6IoeqsRE8nWVGTeios5sL3p5I'
        b'JjGL0f74BHhKzLkq5wbgNIjHuaXEjQlcPz7Rg0JzgecgSZ1QB4klgQwDO2fMQHtFRl4ajg4JhXQheJmB15UBMzBhBNxGTzfBSRTaXkaGzitnrhDNthGednWmPRJPBm2P'
        b'joCXx4uWfikH78ZriBHhbD8EhMBKvSiTJqxHu2C5u1PhagZI0YU0nMPByqnBFKDnVLTjAUGYD9vjDajNeF/eJBPOYdtaXDt7xd6bKe9M93ghZ/Wb3zEvZLB+t7707vGP'
        b'KzQGOjntilOFyd6srA5MjPshqLXuJDN6iCrkyJ1Tx44d/9v8M1+B4tJXdl95Kfq65vbPr23K+XPrq5+e50+nNrx0zkEO/Sbv/FkdsfelLS5vOby149qe1olRr8PswG8m'
        b'jdkj2xC7ddiFI+9PXPDnrOLh/iFbYuO+O/rjzrWVOtN88+wOvtNQyf0xMNQaHZB36LAmoWTC/b+Flg8J/XtZzZpxZ0MmLQ1Ouv+79Hf+OerqxkEdIf9+Ye++uPTypuc9'
        b'Ry9VP1vcNfL3XR36sqnSp/Z8M1ZTuqn87hsbQioOrZ9/ofLepeZPl7+VbtgW6L1aZVj3u5EZ3+Zzd9/dMcT3+V3z/m3EG9xp/V9tO6Y4PB/W9m8xjp91vL2154WdfwF3'
        b'3eA73efO/God9NkYZXj+vDtbu159NXKn9q/DP6/a7LZ+Zs8fh9rq0+p++mZoTnLC0WU32t4tHvXLqZgPhy5b4T828ujfnhn15ud373+z6sUt349KvlTS8kljzJs/F14V'
        b'6mbJlv56fde1XxYtmFHyh7zwVW1xL698oaFi99JD3wUf+uMI2c++io134M/TlrQ2ex4tVimsJLgwa/DetTwkBTsoVBWCvXMn9sPwHHbEo2AzHWFADQXqsPiQYFUYHgE3'
        b'Y7UpA8BXKV0Jj/lbidKaR7L2cx3xTEeLLsD2QTOtVJ26lqAt6jDsB8vwllqOdljw1iUUtU+2UvfbCC/Am4mxsSFBcagykQEKvHQxNsn9Vup+K+DpBYnxycHJDkC+0FvK'
        b'KpbDeivZrsOtCHtusmPPmIIhY6uuQFUSMHiSBDWgtmlWGj9gKdyTOC+UGY0OA3Y1M2PiCJXi0eOHJz1Usif3Pzyy8BSPLKy8zizoxLNzenJRQJKjmW6MgpEzXowLq2Bc'
        b'GDcWf5M44TZPxo0h51QKxon+eOGPB/6/94O/s27id9bJQc6Q2U6MD+vJKlipTIpnezA+uE2OP8MwXPLdjeFdwMPzLpe+KPU5I3kyVSqGd+2li4KaBXpPS2579T0tCSY6'
        b'gZ3Ufvt5SbgKB0F1SlKYKAR4xaCWg6dhiwOsha1rVAz1XVnjYX0i9oad8SE4eZFi59qQjsr7JaauvXnkbDExJafo4PFz9GzXB4kq+8REVUJPzKTf5mOgTso+/1KJvASl'
        b'rv/FBr0tKS7glMkLJ0ZFKC08/RIZ1m9qv1/irUqes9p4M4FlMgpWAiJLZ85T6vR6i81sVQpWnZXL58xWQVmUa9TnKnU8h+cU8JyAGzlDP3A6QWkTbDqT0mCkItPxRk4I'
        b'U84wCRalzmRSps1JnaHMNnImg0DhcGuwfPUYChlj6geKHnSKo/QW82qOx6PIfY7NbNRbDBzGizeac4TfoG3GQyyKlbkYNXKRlG0xmSxFeCYBYNNj0rnYJ4MIxTw0cLyW'
        b'57I5njPruVj7usqgGbZsjHuOINj71qoemfn4HCyPzMwUi5nLzFQGzeTW2nKeOJmIgJD5cL2ZuMXEGa1rdbmmR0fbZfVwcKLFbLWYbfn5HP/oWNyaxfF96RAIIgMPztKZ'
        b'dJgCraWAM8dSduIJ5mwdZrygMxks/cfbkckXcZnN6Y35WBUwpYRRAw3V23jCoeKH2GSgplzeZh5wNDkhj6VPDNOmz8XDBPybLf9JWOtNFoHrRXuO2fB/AOUsiyWPM9hx'
        b'7qcv6dgerJyZ0qDM4bIwNOv/blrMFuu/QMpqC5+D/Quf97+UGsGWr9XznMFoFQaiJY3YjfJpm1XQ5/LGbEyWMlz0ukqL2VT8P0qT3QkYzdRKiaNQ2knjzAORRS8efoOq'
        b'mZxJJ1jp9P8bRPVNFmIfhLO+seiBvyuwCNZHAdg1gxP0vLGATHmS5yay5oxZT8CYRC6rrle5MnDkwkuZTE/QMPuiD9Wx/1pPVs3/MN95DkdRbHSxSuxl8MgF6IY+L0tc'
        b'YKDxxBdh4rV5XB9R9SKEWWBCNwSBM/3WVCsO8E9goh0OGTEwso9F3ESb2cCZB46Y9mVxjBwgVvdfGI/5LRg5q/vH3aeJtFFTtlXAniobJzGke6CJBTwWAPZ5uoHXTbV3'
        b'c+bQFD7sSdj3W/sxvAeO/3ZFeCQH6Df5ifmAONeIlx54YvzMGSlPVjuthTfmGM1EpR73IfPsfVlUIbEBK+fyXL6h6Im23hfyv6DQ4vD/oDPJ1eFoM6DLe5rLQjewWQ/g'
        b'E/4HECNmQO2M+Ll+eC3EPb9tbGZdPvfQ29nzYmVQCm4eUE9tfAHNix6bkc7xRZzZQMxybRGnzxtotsAV6GL7JtYYQJ+sfoAZy8zmFbHKReY8s6XI/DDrNvTdB+gMBtxQ'
        b'ZLTmkiTdyJMsleONeqXR8FsZfizeturyidvEOC3MfaTMq//EWPs+JxbvCwaKDP1HP7gZIDs5n8duBuLEepuMWaQ4K2KOO8h0MU70Fo/VHVkpUIDNScz0TFOgdzIQD2Cb'
        b'Ycs02MkCcjYHJoFJsAPupcMv6R2AC+gZ46zMDHkp3ygOR0fhBXhGE4m6ltqPwuGh2fQyAnZ6w1Z1/60q3qeOHBEKL8iGhaIGlQstEYPbxqDjqDw8IT4U7gpPSE4MlYUm'
        b'oMrEFBkYhyrlalSFztKCAVSJUapXwy54mYyyj/GERySwDZUvpqfL0yQe/Y7GHeVuBZIJ8Bo6SA/7pEsV4vn34kmoUm0//573FD0eHzsbNqByNapMTghlgQJdgy3oGAt3'
        b'wZvLRDxPusNGAjweVSTiXTiqCo9DlRIwwnMRuiRFdaga3hbvH27Ag9MS0RnU8nAwuZIpC8fojlbLJq8Ms40l45rj4PFegOvgdTqMXlukJDNABW/IYD1sWklhFsIG18Sh'
        b'6FLf5cm1BB44OlM2HTahczYlQXIzanZSh6FKDCssIRmVhajkYHimGjVI4Qke3bAFiIfOTf540KG1dFx8MtpFhg3xlkYsgBWU155SeHEg2WWgLtmwMbPFE9V9WTM0kfBI'
        b'ErloOAAM/rCW3p5EusIdarQN7XlMSsugWK2AtsOqdKwzJTIZvVLIxeRcE6+GdltnoxoH4Aq7QASIgNukomzg6UH95JoNd1LB1obTI1QeXooTBTsS7nko2SyFiqULGuFu'
        b'1KKBHQVywCQFWQFsDUMn6YJzMlbgdnRzPKD3Mnn6YJsfweMcPJnXTxsC4HasDKTMRyUXDaUKnlmv0RRIAJMIGwcBeB4HX9qTwcJ6jQa1yQCzgEVXALy4EZ0Sj65voQrY'
        b'rNHweNI82OYEsPE0oC1igcFFdC0RT+vA09JHegJ4Wesh1qWVqLQazRh/cpNyHOShHSEi+/ejSmeNZj3cRZh4AphyY8TSusE+IAQoXZyUmX7HxpmBzZ2cw2fMERiQnQPm'
        b'gDlS2C7ethsHASWoLnYoyEySKcKASkJ5HWSCNeT+pDKcMlKB6jagEyzcB49kUtbAE+iAf2JYaDARLWyVAngu3D1dYoJX4E6RMZWTUEdifAgW0yZYK5Uy8OiypVgQ9BLh'
        b'Aty3qZdpLegy5lo2uiryZtsouLeXbb7wMGFIGayzBVJfMkk9oOnBy1Jieh0WDJ8wUYluK+zsDUEXMXt5eEMshYANwb3MRfs9MHexzTRT4Aui4b5EuN/rCdaKLvrSui39'
        b'jCKNxjfFLgXnWdSG1y2a1osXPAL3DmTCWOIdVI5eqILgFmwXF2zMoKY9DF5Zk6iG5U8wbXQWbqMUTIbXUSMm4RQ8KF4t5sKb8ACV5PdFbsAPvL5MFpEZklToA1Re1Bmg'
        b'TqtrYnxoShi276DeA9vhqKYAlkjhyWlLxfu4k7A1gVyYqULjpcDRIQg2sXA3drLXRIFdHQmPisJEF1KoMIfBXaKNHNSC/ooSTebug4fRTmqV63xWqhNCE0ODU0g1L6oZ'
        b'7Z4j4VA9PG17ihxQojZU1/+eFrMNnpeC4bDcnCSFe7EjPU1ZNDIgb6ALXaC0OmIWu6FWbF4Eo7GofpUaHZY95njgmU3Uh6PWNWrRj0ByB5rZZ2CwXgbPwa1wN72aGgE3'
        b'Oyb2ufZGF81s8TK4j/pPZ7QVHlbDsxPoFXH/C+IwE8WkEON+qp/Hii0mDgttwTAI2xfBSzGix1qCzj/0WPHwODVCHBGvw87e605Uu4zeeDbA7Zgj5DhYXwCvP+A9LMMG'
        b'gT3TZliXRK4EEgm7I+EBeTzaNYZKYh46mIKJiQtJ0GNsQuXAOZFFR0ywgfaGKjLtF7KwaT2VALmRxRGJsmLIAtTSe8uLquBOaQADj69E50XtuYCDyVHxph+dHEdshtz0'
        b'w1J3MdJ0olMRsHweY+1TkmCvRzAvES8BD6G9sE3UsDGwmWoYOgn3iNVwx0xoTx/lRAe8sHIu86EOMAU1wC5nFvsJeBWnOmm5sJFOmjY+pI/ajTETrYNX4SXsIqg7vcE7'
        b'YV+YDJuIM4SHUCt1P2noKobGYyOrk5PYjHMZ/L2ZTlmUj1lcg1V4B6ohBZ6enFiIeihrWn8DwIrRgC0AXYR7qGF+5+oIPMC91Q6ZmUlHXBcC6m8s6Kx5YL3PziBqnzWa'
        b'urKR6Ioa1aADXJEDCTZAq0T7qBJHY7p3PtBiZ/1jSnwLnqcQ1gzDPqkzAtYMkWAIZ4AlGl23LcIdwSGoUTDDWqxfqDJ+firsiEhbgAVI6sXDQoNQaXiw/SY9jfiN0pD0'
        b'OCI/qiTz40JID/YmiYtSUSV2/7fXDYKVUcH02tw8D5sLuBfmhlPKyStHAeqHFmQsJ0UpZWjr41oAa2GzPTYMwnS1wc4oEqTnx8F9ODZk9pZqlPmZSQ+DQwNqg9twANeE'
        b'2WjdxoXsZFQDS+PRHhwQa2HpavyoxFnb+RjYKoMdWQusWfBSNEMrAmCLfAlsHSY6tovkHrkXaOhoDDIcXcQxkCjDYBW6ge0FnUa1omzlWjZYpxBV/tyYsX3DH2pkSPhb'
        b'Do/Q7hzWr79OwJ2wEeuENIEuW4iahV4a0QHYjomEx5xowoyux+c8lrqhFniDJm+oVkUzswRUjUrUYdj31zyWvWXBHSopFf1w2D5YE1OI42ACj65i2pbDHdRofFEX2qeJ'
        b'gsclcpq1cd7ptF0BK6ZqolZjXkwPRJV4F7B+McVXB/cyGF/UBnDgjNkA8G4Ax38VI15pX5+vx53jcN/cUbAEJ1CrPG3kMgnrBDzvTIvOd2OtQlVpxDjaXGF71LjUuF61'
        b'WxCavuBRbcI6fdQJx4jDEWKdTXMu9qTn5Djb8QLrwXrYaa8BaEoLhudiYDsLWJ+58BpAZ7HTaKKBOnlmHDwnA4NmgY1gI9ov0HcLpi9E9QKpkw9fEBQXEkwNL6Pfyhmh'
        b'ISscsO3uwFlyLJ6R5AR3OKcko8rQdLtpoLKMuIRFcQtFQmBzKipNDg1LScI6D0/jaHbdjKd4wHJ7NQ1W5uogUudthKWk1BtWDxM93hl4CAu1Bkt+Jw5fJJBipXrKG0+j'
        b'97e3guf006/9w4l+TfCivWNUcFd//Rq6iFQQZ1BpjchcRYo7LrsyIA/uxrknE4V2G20qmhnVDH40YuSj5kcCRiY8SJeR4K3HKQFdLnDHrG9B+1lUxjyFvdExMfLXwT3w'
        b'ohhQYEfag4CCSlCVqMrbDPD246nHcHScph7Dn6YFX0aY9yUQBPzV7P6tbeHLZq+nvW5+e+/zj4+0T9FMiJlVOk4aUb39xqHpL472KIhRtL+0Vbll++veIUuHjfvsRb4p'
        b'2JHzah7cmDv1TvnnQS+HdBieCXRWa+84fTj4K2bJ3/70WXu7V+q56ymHz/7zzLKPVhuDz3489uvqyeOKd2R0fpU9LH9a2Kvy5BPXl727f0/nyfp772c1Hz4cZDl8fmGy'
        b'r+sn3FfPv/VqwweL2uqTz586tYYx3W07/63/B6NG/PPZ5/w+7PoBNb9/INK26wMmuTbw6X22s25Buh9//bp6wlsfr1njf3h7lc/6T7uk331cfcf2DNfzy4eXE7+6+sML'
        b'Y0rfaX3Dv3LK4ZF/nTS+aX6iafOptd+MN/3t6zVndxXrhmz/2dmUcffss+bPx/18xmGkOlr5+Udrj29xLwxv49iW+6l3Bj9XPmluyg8777435EJi6VrHdzoKlkF/edGw'
        b'd5Rv9mz0+VxxderV8c8cfP9awdNjTtjaLI7XX0ye/Zy6s/TCmT89U7+jpOqzkB8L9u5jFs13rXrurweHTJr0VoJQz62xhq709/x+/a76yz9M+PPw7OdOv6ia45ry78Pe'
        b'efuMcdjzM75cc/izhdO6Rsa+CKcekFWtj6yaYn6WW9c+/sryy7fVeas+2VP+hemo5I9vvff9Ms0HaROKX098uiU2bUqYZf7Vv7zVtfPyxaNfO5rzfndp7Mgrf5x1Lfy1'
        b'mpU1X1/6oeKVN+tzF72S0+gsCej+x9e+r5VNPTY7t807asKPg6M3Pb1qIzIufA+cP/DsF7Gd24N/Plb/808B736ddaB0heP17wv/eOqHm6YMx01g5T93/KFrx9kdy72D'
        b'/arPe3/lmns+ve1+xL1d0+o//khf9tO53MwN2ktHweFn/n76/V8/vhf0peyZ6yfC+Ov3snIC7i3Z2P7mvTnRlxqSn964c/fFOffeqg1/I+Fu7TTL4k9HVyR+GfnOpJFf'
        b'DtG5+L+qDdwd2nq7S//9L0NHrlw855V1DlNutnhbz8x5ef78uPR7qT0Nd5bcaREmNVxBN/7+5ZKKro+59/7ybqgmnfu06/Vbh3ves35f9sWGTc/aVriPr7SkvrQ56v6t'
        b'eebGl0M2jD+Q82V8wpGOryM7q9/OH/axxf3MnLUbT3k9e/XGicJRG24FTrzwQcDSn/ZZVx29sLXzOc1fWxvTPvthaOCROyZJdGnMF/94k3Hfxo4PNHz4qSwyavSf4su7'
        b'jr/v+OdhP99Nfekff3+mqzKj8ZvUo6cv3E/7w/jaqT+4F35kavvibZWblVjqfHRikzpsPt4Cl4pVHcQhYnsegndWOAaj47TeZGM0OqQODlNhawbAcUm6NwtPrkatVvF1'
        b'HDdUrQ7jYHVvxUpvtcpTaKuVZnHlGZNwYCtBDb1FKaQiZaZAO9HF6NjEPsUo+aiDLbbA/eIbTAc9GHutDGwqxqB7S2XUU+naq1FjoRrW+RKP/khNSniIlZZw1WSo1SnJ'
        b'IQloNwly1xS+bJHDStqFKhaPSQxHtSk4KOAQIS9iw5ahLrFK5mSBNhFj9ICcBHjSPUKSkx5GZzo5wUbs/caNfZgcoJMCrb7hUUUhpnU7vCUySw5bWA28AW+KcNuFqeK7'
        b'Ohsm2N/WIe/qtMJa+k4Xj7ZLcMpcAU+YEnGuVUDjFQu8J0slsGS6avC/Wkrzn3yoXP/rcB57uSjfOjEqgpbohJDak01gsYKR2j9utByHfKQMy7gwniz55sI4sSwz0Ecs'
        b'6yHjfVlSoENG+pJyHtaJ6fsRIbiJs54AS/woWDdGychZ8sqTB+Mr8WDc6BpSJgDP9yKFP6zSXipEXorCq7EurAvFgBYL0ZXwD0vwJvU6gfh3OS0fonjgWXLWiRYfOTF+'
        b'eL4P7h+GIUoxtQ8x92DFMiXyjbwpRSjgycFNSm99kZScHfepK/qvy0rF8B690qJr7SVSIk1gM/hydN8KJBrTa9AJ2GwvQUJVoSSXA2AGbBtWIEHX0DFLv5fliKynE3hk'
        b'/8SRl6zBUtbALJUYWPHdum4PegROy4P4OTxv4X8cIR6KU73h7dU+nEGpMys50h+WopJ2K7Racoug1XY7abXi29T4u4tWW2jTmew9DlqtwaLXakVlfPighJJ65iqMHS0b'
        b'U7B0R+WNU5e9zm7oitV5AjriSEgM5e3GF46OymXwkq+KmWss03kwwnA8eUbO+ilV11JQqsec977uHDzJ+a0Ptkd/+s9bs6rv/QCcZh54/8WZu2rZd1Jfz0z8YmjZtBdf'
        b'yHLYfurguo9yP3/lwD+nRnnXVI3mm96VL6l6w7s5Pe0vv7xx92BO94Tf1zo/N+1AntNXt+7cfO1G7fDmN3VB/wi8rzr67NVRc9Kfdw912vPKOznjwlx+iRld/NnHu1pl'
        b'uwJP3k32Koo9ffNO1s6ET8fELFr1J+PrTXOGH3VbkX1Qf0Tms+T4C5Hqlo7nY4ebOp6LmfRpxwuZ16Y6+PFRH4/Zq0+Z8GHF12WHFy9dpX419JNVPQXPcPWf1HWp6var'
        b'Tr2U8d6CcuvKP52sPRj/RVr3n3eb7536blvkm+88a/7u5ZKIbx2eCf158evui5oCDyqePfHlyo3A8I/0RdznKqlV3IBURSO86dufhLcUEwDOt68vpz4OnfeF2/u8t4p2'
        b'm3rfW0XXrFZ60n5p1XLnYOxaiUMXR+EhI2CnFGf5h9EF1Aj3WpV0dwCvcgI8H5cS+iDJhF3w7CBULYFt6xKxhlNF9/xv9Jlymso++UF9IdZak0Vn0GqpIyQF/cCHOKYo'
        b'7HxIVSGpM/RQeDj0c2Myu4uSeM3DIzeBDS4MP6RXmbEBsVjDH/qDQf895DG87wPToa8Tgt4axU/D+noIIg68d6uAx2E5rIJH4R6y05+XBMtglQNwGyrxH+VsdFvTIhU4'
        b'PLLi2/n+z49z2zrdY+fvN2UXuVqzduy813gDbl/1WVC75v7dZT3J4279fceOs+8uvfT2+9q8W/ePwE1FaYub6rUnP970RlqiYlTavXsTNQXPDL3GjxpX+NE49z0n1ndl'
        b'N0x54zWH535nlPlefplROYgvSm+RbCIvmKKWtHnz6G7HAcfdDhZvw1rhVXFIg2NG4rxQ1I4xnjcvlIUH0GUwCN2QwEZ3WE8zjaJ1HoSwhdjTVZGzMFhJ6fKUBKAqDS1+'
        b'HaFZJhbOokueQC5lFf5xVrJZGo6u++BoflH78A8bOKtYVI330adoUrAIbYEnhHh20iN/+WCJCHeQFXWpE2SASUS3TXjrhVpH9ep1wH9zQvCfVRrpb1qC0Wy02i2BeArg'
        b'qmDEAKmQhGwC5AP4oQ/0XNktMXHmbimpFu2WWW0FJq5bSq5FcUQ06vGTVPx1SwQr3y3LKrZyQreUFI10S4xma7eMvtrcLeN15hw822gusFm7Jfpcvlti4Q3d8myjycrh'
        b'X/J1Bd2StcaCbplO0BuN3ZJcbg0egsE7GQWjWbCSMrFueYEty2TUdzvo9HquwCp0u9AFI8Vr6W5XMeExCpYJMRHjup2FXGO2VUtDV7erzazP1RlxONNya/TdjlqtgMNb'
        b'AQ5WcpvZJnCGh5Yskh3AEy/BjyOPEPIgJ4c8icM8eeeIJ5cPPM0ZyeaeJ26TJ+ccPDla58mhOU/+EgRPFIwnCsyTY2OevGbOk2MkPog8yNtIPHl/ih9DHuRAjSeWzBPF'
        b'5UkGzpP3xHhyO8arHzgCIh3HB47g/tw+joD2/ajo/csB3R5arf273QP+OCy7/59GUZotViXp4wwpKgVPHAyJ4DqTCfs3qgfECrqdsBB4q0Bu3rvlJoteZ8L8X2AzW435'
        b'HE0f+Im9zHsk5HcrJouJwlTyG01IpCy2T1HXPLyIj2X+Hx69S5k='
    ))))
