
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
        b'eJzVfAlcU1e6+L03ISC7iBsoxp2wQ0AFEXFDdlBwXyAkF4iGBG4SwX1BBQREBRQFxQ0VEGUTN8SZczqdzqsz05l5nba0fXW62VrbTqd2mbbT/r9zbkBQ7H/ee795v/fM'
        b'j2s467cv53yX95gB/zj4iYQfYzg8NMxqJotZzWpYDbeXWc3xkg1SjaSQNUzSSHmrQmajzOi3huNlGqtCdg/LW/NcIcsyGlkKMyxbYf0db5uyIiYqVZ5j0Jh1vNyQKTdl'
        b'8/LkzaZsg14epdWbeHW2PFel3qjK4v1sbVOztca+sRo+U6vnjfJMs15t0hr0RrnJAEMFIy+3rMkbjTDN6GerHm8BXQ4/HvBjR8DPhEcRU8QWcUWSImmRVZGsyLrIpmhY'
        b'kW2RXZF9kUORY5FTkXPR8CKXohFFrkUji0YVjS4aUzS2yK3IvWhc0fhMD4q0zXaPYqaQ2T5hi2ybRyGTwmybUMiwzA6PHRNWAnkA0UyFJFHdRz0WfobDzwgCgpRSMIVR'
        b'2CTqbOD7viSOka68AxROt1e6rmHMU6AR1yozcSkuSYpfgotxeZICl8eg/fjqsmRfGTN9kRTfXb9ewZrdYSjqxCc9jDEJ+CAuS8BlLGMbg24FcKjVIVXNWgCQwI9LHwCJ'
        b'hAYsUOH/Q4NMFwuubLEEcOUAV5biylFc2R2cBde9T+M6/Rlc54q4vjjNmrE3zQWmpOt6o9QMbdyeAgTwnEEI4BOg2CI2/tp9GOMc7w1t6fHxq+eIjWZHK8bGtINjItPt'
        b'TTtXMTpbaGxPHyN97MJEy2R/mf43riuwnY1hdcOgo9RUw7ZaM/LWFfqgt4JenvU2Q5t9rb50qnJiPZPnP2J/HBNo7GR6GbMvdIROxBeA5qX+Szw916JufMA/2hcfQI2p'
        b'nrEJuMLHL8Y3NoFl9E7D5gioZRBpbfvwDSCkJWRlMiX9xGN/lnjPCIrsGeLZicR7b64jM45JZp0C0n3+7hLHmP2gkQ9SAsxl3nG4DFXhM7gkfkl0jE/MMiYoLmUkqkpF'
        b'paiaybKyxvW4B10wuxKBuRC+RYmuw/KokcGH5uZpcLt5NOnowmdHK1En6TnJADEOb0Q1qJpOWhuAy5VBZNBRJhw3qPFVdM1MwCxA1agRV1oxqAiVM36MX6gvhXaqly3j'
        b'yryktHFO9wkLixAZ2Jg+gpnCRGbaM+lrTdEco83/KFJqVEHPwoibn6R/lL4hM151L9PviKcqWvUw3UWdnanLeJQeq/pdpmJpjEqRHKdq4S+xTSOyPtLEql7mfhN4vvV6'
        b'UAzn4v+rpa+njDnj86Kro7P3yZvH2yobC4dr9AGSLDcmev/IMqfbCs40gSjWOdyJGuyAXIoEsy8+inZ5AaM5ZiQqkto4aEyEDpPThwFND+AKXCZhpKEsvpKH2gqGKdhe'
        b'zlOhkAiE5U8ejcx3o8IzBcMWXi/PFK2XnzFfm2mK6LWlpilNozLxxIAa7QmPJ9mz9qwza8N6sgLhtUD4rJD0Wm1S6cx8r3VammDWp6X12qWlqXW8Sm/OTUt7ZlMFK1iT'
        b'71bkQVaZTNZ3JOu/48zJWI6V0Se1ELPmonbvaB+vRFSeFLM6xyfGihmFd0vH4rbIKDVnET3pEHIMZqJfjjlqBCQgxxyVYwmVY26HZCgj0KcYg+VYlmgmVnARvuKHK1l0'
        b'yh+UkfHVW9FWgE2NKyW4A6TNn/HfxJiJwYpA+9FukK6xuJAhwjV3hTZo32OJkehr4/u3P0n/t4xoVbxqQ+ZDzcN0nyPRqug/fpbuksW0jw2rOTG2cOysNUz5f1g/svtW'
        b'wZrcYI49aseV3rG+uDgmfmdQohVjh9o4fDICNVvY8BSdaSulcq+dyMxMnUFlotwkAs142bNS4KVg289JKeVMr5WGz9CaBDJIIGZHwQ3gHicQbzSAhWS6dz8LXxvEwkmE'
        b'OjdQPTrQx0TqGXxYxh2VSnKk6DAuQruolrpGmVF9otE0I0DKcBmgwuiMmao2qP+1QDW+Q7pYhuMZ3IgbUBPV4MSpegNPOiQMl8XgZjdcbB4J7avQnrm40M9omklW0zO4'
        b'CdXOFVc7j47hLtxoIn0cwxlgFq52EY3IrbH46hR814g7Q8hWqJDBHZM30b4VqNvOGh+kXVbQtZfBnQYwPmS3BXZgfjpQlVGg02DJyynZ4m6ns9NjwAt2mAMJIGDPcAc+'
        b'4WV2o31g1m7iy/gi7QZYwD7hzqXoEKUHPjPV0Q/vMxqVZOZOBl+ZKTOPIVBe8sCnUZsnnQV4oxMMvuGLSumGq6IXoUZv2mUNXbUMvglic4KCic9MQzfn5OEOo70t7Iav'
        b'scEB6eZRpGc/alOw6+0ESnx0gcHXA9Bx81jSVYwq0vBhfM0Ot4WQXnDTEnQSgCRLBuPmKBXqsLMNIojjo+ywIHyDLjkpDO8el2GHuyjieB/LgsG6IxLl1Ei0C51F5Ubc'
        b'ke9IIDnDes9V0WnoiAEV4qaNxmEOuJUseZedERBJ90JHVO4j59vlmXEXBHW4jZ06DF8QJxWhWlt2idFOMJEpNawHqkA1lFiT8FUVrsPtRhO+bkc6y1lv3IJuimiX4hpu'
        b'DCoyOjoAQSRW7Bx0Ad2m1DeiOghK6mOhy5FlJMPYSOutooy0O6IifAu3QU8ewewG6xeDm0UCX4rIAdbstnPIRWVSRjKZjZwyj/aMWI4awGoQAQHhyWUAhOubaE8BOm+e'
        b'vxhEOFjGcJlEto/2QVeUga+h41OJBFiJwti+PoxiNXxONr5D5LQNdzgRAl5hg9Fx1CaS95r3ys3orBGkXOxsYpWofa5CTt3Y+/wINphjPO/PuBcQl5TnRxt/lTqSncUx'
        b'Y+7PiJd/nvRDCG38LH8UG84xs+7PKEueL60VHflU6Rg2EkzI/QifJFmkzpk2Psx3YxdyjPx+hC7fP/qXgaK/jBjPgpt0vh/xKN99+cwNtHHhyglsPMcE3I+4PDLT7vXl'
        b'tLHZbSKbzDE2MHLKQn5CFm0M2jaJTSVwRth7/EF914U27nCZwq4kcEZcdhseIpfRRqsZ09i1BM6IR5KF+pfn0kY0UcGmEzhD7ZOcFkvE6RudvcEhMJH3Q8usbRxLZ9HG'
        b'UsaXzSbAh+qi+Qmrg2hjlq8fq+OY9Puh8e6c+9lxYrCXG8DmEoxC761B6wpsaOPfOCULNjUZNrK9MuzIItr48sgQtoCgGeqzLXD+/FG0cYt8JruNY3KhUf/O2BKRyFfS'
        b'QtldBPfQssDvVraIpOPlYexejom+H/poObd1WgRtPGycwxYTgoTe41wKLoykjf78XLaMY7JhZM65Am42bdRujmQPESqFxmd42XiwtNHdMJ+t4piVsNGKBNVLGbTxCLOQ'
        b'rSGkC9VZb8jxSKWNdVsXs3UcUwDTt0a72q2hjSHSaPY0oWdImfPU2L+IcVLjrHj2EiFdiE7Su9pNZFzJ6iT2MiFdSFmus12ZG22cxixhWwnpQi6H7h6X5EMbW5NT2E5C'
        b'upBHDovT30ykUh+Na8Ew7sKHjHa2RPPs2cgk1EyNvQwf3GnOsxMcHUBZh7NztHi3aKJOb4XQqM0WTOv1fKOEGg1vVIav0AUXo8IYR9wDtgZsN7EAVewkz0UKKQXBoPg1'
        b'WycBXGf7yJJlEd608be637Cnwdfdn2mfbmUKXEAbJXEvs+clIDsz740oyTgoCn695z32kgQIMLMs+PeqN5YNHVkHM4yYtpGEhcm0+idTk+yBUQnZbeQzUcnsRDMJDD1w'
        b'lwGVJoHBqsAlMQl++Op6XAKB4ah06XRUGkBBVSk4GicFjFLlHBjnI8a0qWMhU4G2gBkfC+opMxlqXKbh86vG4kNx/nH4YBLEWzZ4L7cZXQqj5oq1WTob3UYdqJPE2uwq'
        b'Bl0ePZX2rMkL9/aMy/b1wsX+EJzYZ0mcFlhTvqGyMCW6HYo6YP8wJgyX4S6BRCEUhBtZVgQ5eYDMYFg9Nk1sfC0Ici2GcQ5YHjZh89QIMZ4KXj+aHa4MoJ6AUaGrwP2p'
        b'5JdWvA8VJ+G9cTTsrSC5ZByq8I9BLZ4sIzdZOW5DnWLy0IYLF0WiPUrCEFTFZMwEx0jS65wY1LWA9faEBUgaCmlUjJQZoZBAXnIGjCrZHN+ZNB6C6b40Qq0fL3qeFtwT'
        b'AKBUgIUlqUc9o9uBSsTdzruOWoIPKZXk+ykmCzWjMjonCFXjCnQd31EqIfpFZ5gN4A1Oi3MqtuI61DFXOYP8UsNo0nC1eTyF1h3VoW5DXCwBL1FkjGOuZBY6alGOBNzk'
        b'FIGLlTMIGMcZPhdwI1FGPrqjjouHnAkm+eNyb5axWw3+Yj3uFHlzZvU23LlWSVJYCCQygUti9HECFaOLyhXKGQTGWiZrOrpMlU0DAJ7BeyChL4VEJMGKkXqw6GwKbqFk'
        b'WhiPuyfjm8oZoAiojsleu0HM89vkk71jUKUSeIJLElGLlLGfI3HCh9FZulvuqInAxHIl6iKDTzM61C2h0LtBrlaI7i7FpfGxJKOR4B4W1aJ96Ko5iQwtcZUY42NiEshJ'
        b'A00kSRLp6afwSvBT+HK2qIEHj74X1UA0ed7TEzWO8lZAqnne2xVVjRqJz49GFzkGHXB1RuC18TmRpbUJ6DS+pfVO9I2WMtJIFjUtRj1UxJPUIA+nIM5zEMzEzJxiJy+f'
        b'SBFw9h82Ee3CHY5iRxerCF5ClQmCyzZuJa7GHZY5PWCaTqCjYkTTHcWiy1OMMEs0TBPWADcpELdxqSO4+P3GPLMtiURvs/K1zmJYcByXrWK2g3vPx51WNB6bOHK2GBle'
        b'RFfR3unTIKzCnQ4sDZKCvLAYX6duwadwc46dox2qAPu5ml0zaSvtcAnIV6CrRpNtPon97rDjzOgUBc+MLwdNXkg6yDa7WTnQqEi0uGdw91ZUgotwh0nAnSQI7WHdt+N6'
        b'EeeaPNQNZrzBiNtNMgbiHgYEvmUDFbh03DF9hdbOxgHMo2QmG432pYpoXcEnU3CzHkLXPHsC+gl2uoNeDKsakqbiC7PtHO0hGZHMZmNgdfE4YA4+47YQ0OpwEiCOlDiy'
        b'M63nWHIGdNpbQuBzwu3EXUxi56HyYArBNCdUOHu1MY9ug7pYj8U76GIF41GPwmy0Ffl0BNC9GU0njDUudsD1drRD4sIGoIOOVNh9cIMmKQ9Xgob4wC/tELdRLpywm4dK'
        b'nWzzNrGMFF9GlRCdoXJVtIITNasQ7cV7Vo/pV7lZEBYTNOOloAN1+EC/yqEjuF337U8//fQgz2IjNwVtnL5wFaNwtSQX6Do6NRxdGyCPi8BgkMX8/ALxXZCiARJpm0nB'
        b'i0YX8eGFuGegRELycpouGYBvQOh8CF8aIJPopiU7OoYq8CmlMEAkQRbbRe51WKu2opZBQslbNKAKlaD9yX6DhHK2JczGe9YtEhwGyCTa4yVudg3XoE58yXWAXKIiEe8p'
        b'fqgMTMCBAZIJYfN5utuOWZBadAIZBwomrtaKUNbbFOCyHQPFchg6IQJShspx1c75TwQzTpTLbHRxbR5uGCiWalQhLncIjEvngq1PBJOIopgRhkJm24mrBkhm1CqqOttg'
        b'p3Z8FSzVQNFsgmCFgKHCNfjuVn6AcEYtoAva4GZUmhI9QDpZVEmlcy7E+eWbxj4Rz5lSbc27s1jjJbDBF8NL1h25mfh+pPP+5ltvfs3gtrqgrPnxL4y8N82b47gpeyam'
        b't7twa+ajBQHzQkr2vb/rF+8Ot7GZ0VswgT+3nfHY81CYHv/HdV99lbZzxbW3T/zmnRdPztsYtTM8wPnD+4GP5u4+HO+oeannJec3/e45mH57Zpfbi8eqFo56/DGzeltB'
        b'xYPoVeWvGk2t0ofyN2Z+NeIrW7zy3FvFmg8yf2P78oWoEx9vCO+adTO9yjHv8ctrRvmfeHXE9C90qas2Ba848XDCmrzPne5/cf3Q5on1saMmrfKpHOV9KLvR9cEXTQvn'
        b'Vn0a1zmuZuEf6+/JfwzJWHF9qVto6LKrr3507cKj+W9s0fya93q0PDrig9bGhw9elE57sKYtY83fa289Mvl0X2mt+MXrVn9+fdKZdZs+cf7h9dY3mS53lf7TZf/+0+3i'
        b'RJdDx7qmp897+0LmWLT92/1bJadT6p2/Nc0/+aF91GsR712O/rj1RfdPTs5817A65WTHq6/mTfpS6xEufHrwZNKEGaF/3XG+8etD5jmdH7bNtc/Xf/DKrj/fnRH42t1Y'
        b'r4+it3y6yOGo9tVPCg7/YV75e+sLU74rPD2B++XIe29tZzPXNfw1eK/CxjQOeDl6FNqDS33wdVydCJ4MV/iAu0bN4K935NAzoFkaVOntF+PjpfDDFTmBPriEYcbIpetd'
        b'p9NuXGiA4KwmZNARIIQ9RWPp4eCUMTJvP/CUJbCsbAq+jQ5yvjyqMBG5RDdAXg85j47z8YzG5XEsYwP7bpbjZhMR9U0sPhgXk+CVYM3IwCFfl3I26OJWE/HtI6eMUdmR'
        b'0x1YFpeAXFdImBGzJbjWQ2qiMU0LqjWkoINxSb4g0ptA2A/IFDZPn1U976Gwen7/k/MtF/F8yySo9EaVeLtCj7k2kdB5viNrw8pYV9aes2HtWUcOvklsoc2FdWTJgaYN'
        b'a0t/XOHjDP/3feA75yh+52ytZSyZbcuO4lw4Gw5CdfhIOSms4cyOgh4ZfNxgdfLdkRXsmSfHo/YDARtwrPZ83BSs4NCHHV1qAdN3wHbXdeABmxfh+incNnwcPmc5YvNX'
        b'QKjknRjvJ3LDWwYp0GVrCHua/BWsaLhKIICvWOgSF+MDgS6E8agW3y4YlLyQ3WmusZChyQu5bWGevW/JdOhPZrjnJjMSesQq/SoHFrWVD/iXTLhmlKsGX4DRW7XNubw8'
        b'ITU0OEBuEOiXIL9BUwf9EmOSC7zJLOjJWjqt0USWyFDpN8pVarXBrDfJjSaVic/h9SajPD9bq86WqwQe5uQKvBEaec2g5VRGudloVunkGi1lmUrQ8kY/+Tyd0SBX6XTy'
        b'lEXJ8+SZWl6nMdJ1+ALgrxpWIWN0g5ai5+LiKLVBv4kXYBS59zPrtWqDhge4BK0+y/gzuM17AsVmeTaARi4cMw06nSEfZpIFzGpAnQ97/hK+QEMNL6QJfCYv8Ho1H2bZ'
        b'V+45z5wJsGcZjZa+LYqnZj47B/iRnp5o0PPp6XLP+fwWc9ZzJxMWEDSf7DcfWnS81rRFla17erSFV08Gxxn0JoPenJPDC0+PhdYMXhiIh5EAMvTgDJVOBRikGXJ5fRgl'
        b'J0zQZ6qA8EaVTmMYPN4CTI4Iy0Jerc0BUQBMCaGGGqo2C4RCm59AswKfzxbM+iFHkwuVMPqENc3qbBhmhN/MOc+DWq0zGPk+sBfpNf8HQM4wGDbyGgvMg+RlOeiDiddT'
        b'HORZfAasZvrfjYveYPonUNlkELLAvggb/5diYzTnpKkFXqM1GYfCJYXojXyx2WRUZwvaTEBL7i9aXblBr9v8P4qTxQho9VRLiaGQW1Dj9UOhRe+qfgar+bxOZTTR6f83'
        b'kBoYLIT1u7OBvqjf3uUajKanF7BIBm9UC9pcMuV5lpvwmtdmPAdi4rlMqj7hWgGeC7bS6Z4jYZZNn4jj4L2eL5r/aboLPHhRULowOVgZGLkUd6s3ZogbDDWe2CJAPm0j'
        b'P4BVfQABCXS422jkdT831QQO/jlEtKxDRgwN7DMeN86s1/D6oT2mZVvwkUP46sEbw5ifWyNr02C/u5hwG5/PNBnBUmVCEEO6h5qYKwADwOapht432dLN630TBb/nQT9o'
        b'72fgHtr/WwThqRhg0OTnxgPiXC1sPfTEmPnzEp8vdmkGQZul1RORetaGJFn6MqhAggLLowQ+R5P/XF0fuPI/IdDi8P+kMclWgbcZ0uQt5jNwN6j1EDbhfwAwogZUz4id'
        b'GwRXKvT8vLLpVTn8E2tniYvlnonQPKScmoVcGhc9M2M5L+Tzeg1Ryy35vHrjULONfK4qbGBgDQsMiOqHmLFGr18XJl+m36g35OufRN2agXmASqOBhnytKZsE6VqBRKm8'
        b'oFXLtZqfi/DDIHlV5RCzCTClZj9VDjh4YpglzwmDvGAozzB4dP/tEcnkRjFP3x6tEK90J0okmt0c+ZZuvylyo3gDUzXGyu93nDPDRKbH90qWMvR0yh2dQrtQB6TWs5lN'
        b'6PRs1IbP0NEjHGXBMcwYWhs3LFQnjvbC59FxZdAWfJsR70xQdapZTs7o0Onp3k8lqajYTsZMnGDlpkZlCntaR5iP7+AOXOofG+OLDqy1949NiPONxeVxiVZMIC6XeeMr'
        b'6Ai9HMGN6IwL2uPpPWCECzolQa0zURW94EENAOru/ssT1La5//6kHh+hNw3TpjnExdM7kpvo0pN7krm4W9zjbhK6hku9cXlCrC8+g0o5xgbf5NAB3IWO0jIX5Xh0iewQ'
        b'g8viIAvHFf7RuHwCPiNhJrhIcc0sfI0ij3tmxQ0YRi7tSjRB5MZsirdV+DZH8zQYtGqOz6AxB/AefIJcbiUmsIwCdVuhE46A2kRyBL7MZ9CuQDB0fW4MjJuSbhWJmjIo'
        b'AazCRnr74XJYyy82AZf4KGSMO66V4uYgdM5tvXjFVB7t4u1nj3bTYTEJ+AAZNXqkNABX2tNrRmtUiq89zbhJq0W+JY4Tz1EPBa9UBuEeA7mGOsZo8A3cKF4BncaFHv4B'
        b'z/Jo1WR6mI6Kx69QBi1ZYUXPvrNHoH3i/dQd1MXiSmuGCWBQvXeALWql7MrGZVn9/Fyc3cfOCaiJdqfy7hZutmx+wkzchI7R09TFLviWErXnjk+WMWw8g67gDnRRvJLZ'
        b'jwtxN/Thm9sZenG3MdeXLrl6HrreJwCoZ2wf/9EFd4q4FO3nlMpcD1wtYdg4BrW4og6KwXxUmKFU4tbt86wYdimDOkdl00OYQNSKG5VKAQToAkxJYtDVMFRK11o1ZhbM'
        b'aEeH0SmYs5xBXYnhtNAMX8pWKZUzNOR27SyzcYEnhXkkPjhHqQTmNxPinWN0uBOfF+933UaHq5mVRC/H/S57HWMGhWYcNdFGWGARgw5vXYT3TqUjTy1zdi2TRDJMbnp8'
        b'QaaWUUhErt1Ax13JtVo5uTtciY6xgHYNh6o1arG/G+T3eJyfrxfwdLIqDl2RMk7LJbox+IbIvsqJa1w8yDmTFSOVsqg+NYxKLd6zXfeMstiNtegK7mLMpCiQQ2fRnqeV'
        b'RY129WlLHm4zk3rdZHxp4WB9QU1o72B9QZ2L6c4s6tzwjMJcjuxTmFB7CvcaW6NSGYwviHe62WAljlEyfW7tuGEVMwukMT3+mMKV3MQQ3XfH3fh0XIxvoh9ojWffKag7'
        b'KpLihmmooQCX04sLa3zIilxSKnxj5uDzUmaYNYcOcmIJ1ibUIMMV6MwAWqH6INH2XAP7Vd/PBdyAKvrYsCyJLhyJihZ7x/rG+XpF5SWSOmqnLAkfJaFmFN1ENcLgu3Gg'
        b'C7mCdY+XDk9AR6xQO71Ix/V4N+4Z4hYdleB2lt6kTw0xk2NqUrMXFTLpWV1GN2fQPZeixkBRO9FBarfRCTfLQC+1FWrGN3GJWAO3FzUNs1QaoMvJlmIDfBLvo8YyH53C'
        b'uwR0aKireXwYHxXJcx73aPttAW7m+237MVRE4UU9qD3RYg924+onBgEdjKJgkNsk1IUaXQbfM+OiyWYFdOeiEtt+8kcnAD0q/PGBeHLCHkeoHYSOyWLwOVxNr6ByY9Ax'
        b'QCjaJxZdmZzkK2Ps4jh8yhAm7nQYd+d6x9B78MVx/TfhqGYRnbsKlaAzqejmoMt1XLmazpUA5/Z6e5IKC3Kp2FdlgfeFU2JtxeVqUgVyAN96UgnSXwZydJt4OdkBruQQ'
        b'yPP5AYLmiPaI17r7QdRqLBKaj1ssEhqhFC10x3hcawfOP4XBlaoUXMuJLNyDdgWLwjc5uV/4UBVqprYsHx/0tBPQbXcZcdQQB6Az88WKiqNbJ+FKltTRLrP3RU24ifIq'
        b'CCx+9xNZ3+/SJ+oyfI2qYLBs2DgTeTMiPT3ePdZPtBTLciY+T8Tx3QJ0ZAwWCw2WLkS7cCU+NgddtSblFkxakrgAPq4BFRsosnlOgyS2a77FH+VuRR0BGbhDQioxGcN4'
        b'B/NyMv/mfHTBCOKDy2OWJKP2gJSluJjW4/v5euJify9LjUIK8J3Fe3Gxz/JowiUqCkuifUgnmI24Zcm4XMqgu1uHo/JVztTtrpoNgRTwtTr0WbaOx+JVfYR9GuoIzsXX'
        b'poJDW0LKUk7gAxTjxLxE0oOKNrHU/Vxxw51mWpNyZH4mrkTFMUSRcBUq3gSPctCDFlCXxhnoCtiFjKWmDHQthAV+yFYFrgWnMFY0FDXOcX3lJLJNuCKN88J16CCVh0kR'
        b'uM7iEHAzutPvEtbOoN1mLT7Qz96gvD7u4ivRNFAZkSEbKlBxmoLO4WNmSg8Q4Z6pMOg8uvVMqJKKu8T6ibvo4FzljDx8EYE2s7GAN+pMFSOUKnQNNSmD0S4fGY1R+I2c'
        b'WGbQjK+iMmXwpqjlQKpIBjVmocvUvG6fj+qAiLgVtaFDDPXI7QtRG1WoEWCiuqEzEGxIC/RFQcwAhue0eQGVCm6hHdChFDhX6o8rUnCrA2oLRoWbA5Oj+4Rlqe/ypU8L'
        b'AEhhvS0+gTp4KnWbwIjfQs0A7zYGzP/1bcvtxYucNnzHhJpnoLYdSRzDjWJwEy7SitraA0Q9j0hIsIMZk7HDyUxfFMF7TbjH6EteHFjqSS7tQF1SQuJWDNp9ha81qk4E'
        b'80remEIttvioXWICLvddbhFpXLIiOnZZdKoFm8ZkXJzg65cYn2SFStERBl3ErbZAjkJHSnA/VLaDvGTB+DEQ05z3g3DdUuRyA/eEgwi26MxWRAMZ1IwOzFFwYmRxKA13'
        b'WOQInfLvF6NwXCf6oB50ZkO/IE3FJ5/YiRNiBUGPqwe+IyVlB1207OA6G5yOD1KDXrAhun+qDUTzQxp0dBHViFQuc0PnnPE5I+7KdZLBSiXstB3rRXPegvauEI09AHSn'
        b'39pnhIivQp0jFbpDBgZggmtQw0JURUvhAGlKkWsTZpG41ICbLIEpWP+rlJ/Lw5dDz3BUZ4lKV0sUMhG6i/BphtATlayzhJ4h+DjtsgKRPktiz2gPS+wJwaZoCPNQIyqG'
        b'6HNlf/CpyqNkKwDXQ4PPE/iqJfjEu3A9hcET1KlWqQyZYok/7WSiRjXh5hyYc2mbJf5chJsBISqFlyLWAWgFUgtkY7dTecYn7BIJXFq5Ba6k4QqLEh6MR6cALnQo3QKX'
        b'Oxar98ahyqUEsJmo0QLX6ADLLrjBiNrEmHYyLl6EmiW0OU2Yaies8+1zPFm4gVbTVPNWUbkMTW19Ssck9tF+B7o6mtrQOnS1z4geXC8CdQyCU9LniQ9brOiauQopRSUb'
        b'ny8AQwMu1GJnGNFb2qT7KoPt1BYTgzvRdXGps5n4MtgYXLveYmRQ03KxmqcpFh0RrcxxncXIoJ5ZlitbVBO3nFqZO/iCxcqsx7cBdPr+SXsa+E9RxSZH+M2U0gVjIXo+'
        b'QdQLZLC5T8HGRFEafL9U6lLMiul968oJjPaPURukRnL1HHBpnzl1Tem4Ra4R5o8/uTetcuobv3nhkrrsREJ8d4tn2IZfLHzv1pVjNktej7SxlvwpYNaddgjbMrw7Xc7v'
        b'/EVE8bcfFVZsfqnQKW7H7qR3k15y+mtg2snP1o0uC377q1dXLHtQF/Zg9rpaxbLHhTcXnarpRs2rNv9p4Zvv/PuHLiF/+MrX8MlLb6xedmvbtT//bvm/rcm62DSpbP9X'
        b'h7rzNhm3R8ia30htCvwg7Rf7Hd6MNYyZ8PfXp/t9eOmVDz5PrJ776vGUcRWXlh4Yl9CSssflwk8R14srT/YUvfqG9vVolfq1qbPqE2zeYtY6fjbhs5vni1/+3m/3g/UN'
        b'M4K/fjx97+dob2ZjHbvh8SND3Srfd6Oqi/aOt9nq9Oh79ONa9Uyn4z2vnXOudhs+wd/UsHtxuL3uJLPRw2qtIqJN/f7+jcKPF1Zul65Pk3yzO3cNOin9JviGep/sm3O5'
        b'FXvWSK9Lf1e10/abmoWd3Nd5qgrhkyVf3Pjy20Px4++tKvi25OS5iLc04We1qb/M2NzdkXG7tvzNN+1Vf2jYtmF++OOxwom/Va40HG/7vXPK/nF1fsE3Lh76k0/ZufS8'
        b'6pxzd9eOGP++qv7lwkXr/TMqDtzY9vtvPjz68jf5H+To52R88Y9PO9K/+/77HTlZP9jrPR7/8VjKP6J+/8lG16Y3W855uPf6fyt9dXXuHa8XNmVO+upd/mbav2XxPW9t'
        b'qX1xm+OtgPtnxu+0ea/jrJPncLf4QlnWTvmDB1MfbEyc/L0su2Faz/17Lu2PWzZ882VRQX2lsaSuOe+zyam9VXdfvaNF/nte+zE35+2/aA+sPJM776MJL7i/ElRTk2Zz'
        b'691jYf8I9z+1c7jD5UfNX/OnlSv/sfLRO8dPSn9c+NfPdLteX5/fpkz7yK/n9Y2Pz254lPnm4RGm874Lfp/5Q1TD3t9++9ujv0pEN6Tehk/fdv42Y8yCxV8u+7btg4d4'
        b'9qbP64f/sG/Zt915ryTolh5rTlrycWp7Y+0ln6leJs+/huV6BHyCNn25vibp+22O5/Rb33Dqyv+kbtn42+zXvbY/Xfjk+j8OX026sXv2ntj33FODJiXs+MP0117hj/as'
        b'9hRenzI16e2fZrY7v/kg+E/145NLH2+76PptwdbF5yaVbovJWD9v/NIen5O3Xvp8V8cH6/7yH4su9v59XUH4vjdGvi/v7f7l51bhw2y7XSZ6ZaVNXDBi/qnOS95eBnXL'
        b'qxUOx+sqnD7Midj/xwU7Pvvh9/VHriz9+m1Janem86K5CkcTSUxRFQTfF739lqI6WqIDzoJ4ZDBfo1GXNHotTyuE0G60F3V5e/kpwKHgC2gPwwxbxUF+eA1fMZFsCJLW'
        b'2RAcXcBVliqh/hohdG6KiaYAtZNin5QB8e6kCgh8YJdYQbQf3F69pQgI3UanLIVAvEC3xw2uSlzqQ4qT0Gl0YUCBUoraROI31ehE1K4aqhwIt6AjdIvhgEG1d2ICuMyD'
        b'+AyuAluJbnL5qG4WLTVyg5AiDryxP4QrkFV15nN+8egqxQ1fxh24Og4gI4gBoLUUOacASdZkHa1igsy03P9JaIogoIPYNBNX0/qn6egq500pR14maAD0LnPKCBmdGae3'
        b'Et+t2xAU3/9uHW5DRyla6NhCUgMI6BxYEgche66v5dXLcKlk3XbFiH+2nOm/+FA4/PfXeeZtwBxTaHAALZPyIZU/O5mVNqzU8nGkJVHkI2U51p514cg3e9aW49ihPmJp'
        b'FRk/hiNFUmTkGFJSxdmyAz/iCo7irOesJX5sOEdWzso48o6iMztG4sw60j2krAfMdyVlV5zcUq5F3mKE3Th7zp5CQAu26E7wwxG4SbXUJPhdRku4KBwwS8bZ0gIwW3Yc'
        b'zB8F/W6wohSwfQK5MyeWipFv5NVGgoHgRBKrvuouKTm5H1DV9d/nlYIVnPu4Rfc6QrhEmphdzF+nDKz/IsK5fuUKS+kXrvAF7QkkSlTN50rwTXSMG/RiK2F0JFmMhCg8'
        b'+TsIzGpOw66WaLgUZlgWYONMbx9oZZawSBAMwncTxPsIKjSCpdCK18hVejlP+v0SFdJem7Q0coGTltZrm5Ym/sED+G6flpZnVuksPdZpaRqDOi1NlMQnD4olCWMqADpa'
        b't2fD0VO1ZCPaa+eIr5vshq3DbQRDX8Gid/64XmZlDFGwUdqVF6s4oxtMTZq0e07FzUQc6booKzwvY7omra51//Z38ufP+7V1svMt18UXiqu4t5JfSY9TRr3r9Le2MvbM'
        b'4VOB9R+eyv/qs631//HmS6kJE4++1LZlfObOulOtq//x0e+uTjsW+KdhOb8tmPLjdn3cISfpvttlq95ZeadsUsnol53+7jltnaI9a89Lv6zgo+pfOD/rh9pDozqvNt/y'
        b'8DpQ5eK/7K2H3V8vKAqqfiHJmNq45OK8ylE5YVLTx4Evj/vSp/Ull+1HV6mqQ/78Rnqlb9cbqmNzvg69n9ubNHXxOCNSZP1p7cPsxvG1a/587ZUP6uxqPzmxX3GiS/HG'
        b'+y/7N+779Njjsq9SH+2IfdDZXHurobD13sjXSo69/Te/+PfW52L5cPtJI5tXXuC+kP/wwDBv3fKxvf+ukJpI7LkNgsTaaHwEEk+IPWdBrL0FnaU1nDIed/W9V+4VGvPk'
        b'rfLwAtMUMcLvQoftvMiJDNh0MgrGZKEbHDMBdUjx1UzIK0luPsdFii7NMqKW6ETf/nRnOD4kQa1gPfeCYFP5dvkXmkoZTaie/6AmEORVZ1Bp0tKo/SNv2zCjiD0KBptD'
        b'SjlJiaezjbP1IOtlZbFMEtckGLmT2W7PCqP7xBhUhwPZfmIGhv9r0GOFMf1KQzYnLlMsDH3kN9AwEG7M4nEtZOTkVKwkKR6VoAprxhE3jRgrGY9vo2btxautEqMGBh4O'
        b'vTr+xUDHPZHO+/+wMzPfwfSDT0bD/vtnutELe3zGNyw/su1RS0j3w337miK2bOx69e6ft30Tuu+nzy+0Rof4N3x842Hj1L2HFabHdWNv3F97M296YNAXBQ6Hz+nWdbx9'
        b'6uH1CRXJY3yWrlZYU09K3mqtpS+BJ9F02xpcbfsoXMnhSwEQIHhQOT2LSuOSfCFvgVFJvhwTnTIcd0vIe0f4pOiPD6BzYN0obuSkFJVT3BLULhIPB5bWHS+ww3fiYhJG'
        b'xtGiZSlng2ucqYyiQtwJGw/4qyN2CljnHIcPQcsNGufEg5ZcHvyHSST4BIdaC3C5iWaw+5PQHu9YK5LW+qRCKl8c0yfcHv/iYOC/KjnSn1UHrV5rsqgDoR7jYMOKztFG'
        b'4rOTIR9GGNsv7PJeiY7X90pJnW6vlcmcq+N7peRCGryhVg1PUmvZKzGahF6rjM0m3tgrJeU6vRKt3tRrRf8OQa+VoNJnwWytPtds6pWos4VeiUHQ9MoytToTD7/kqHJ7'
        b'JVu0ub1WKqNaq+2VZPMFMASWt9UatXqjiRTo9cpyzRk6rbrXWqVW87kmY6893TBILAjodRCDHa3RMGtGQGCvnTFbm2lKo56r18GsV2ertODN0vgCde+wtDQjeLdc8FUy'
        b's95s5DVP1FlE20MgpkIIJA8f8iBuSiDRu0BeDBTIZZRA5FMgp0wCMZ0COXUTyKWuQM6ZBX/yIGGwQCJagdRvC+SPoQhENAVP8iCnswJ5z1Eg1zICeVtRkJMHkUyB2Gsh'
        b'hDxmkod3vzUg3BnWbw3+HjXAGtC+72z6/sRHr3NamuW7xQx+55Y5+I8XyfUGk5z08ZpEhY1ArAxx4CqdDowclQOiBb22wATBZCQ1D70ynUGt0gH9l5r1Jm0OT6MHIbSP'
        b'eE95/F6bcDFOiCC/0XhEyoGWirLm7EoMLfv/AHpYgJk='
    ))))
