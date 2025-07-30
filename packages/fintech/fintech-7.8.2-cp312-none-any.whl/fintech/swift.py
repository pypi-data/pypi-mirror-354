
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
        b'eJzVvAdclEf6OP6+2yhLr0tfOkuHRRBsIKB0VBRbFBdYYGVZcIso9soiIk1xEZW1L9ZVLBgbzqSYXHLHiokLyd1pLpd2lxwmJjH9P/O+i4Ka+3/v8/t+f4W7vM478zwz'
        b'zzzztJl53v0bMeaPafr3m+XosZcoJRYR5cQispTcSixiiJnLLYgX/koZp0i6JLcoZTIIMfuUqWUlobBYzEA1nFLWKMxmEr2biZ/ikMRqtsVWAedHsWXB/MwZc/lV1aUq'
        b'qZhfXcZXVoj5s1YrK6pl/BkSmVJcUsGvEZVUisrFkZaWcyskilHYUnGZRCZW8MtUshKlpFqm4CurEahcIeab+hQrFAhNEWlZ4jWGcm/0HxdPdgA96ol6sp5Rz6xn1bPr'
        b'OfVm9eb1FvWW9dx6q3rrept623q7evt6h3rHeqd653qXetd6Xr1bvXu9R71nvddeQu2pdlU7qM3VZmqe2lrNUtuqLdWOaiu1hdpZTaiZaju1k5qttlG7qV3UXLW7mqNm'
        b'qEm1h9pLbV/mjdhrvs6bQTR4jrJunY8FwSDWeo++o7LPaJkk1nuv9ykg/F9SW0usYi4kakmLMgEjr2TsMtmj/xzxZFnUyq4mBGZ5UnNUbshlEEa5NSotyzlrwSFUAaiY'
        b'JwfnYCNsyM+ZDdWwKV8AmzLnzYrgEMHprFAHeAtsB80CUuWBQKvhHviqIjM3cRHcBXfmwp0kYZnJAHpvcKqEHEOAwygBG9Fjj309IgLxhUC8YiNumCHeWSCecRHPrBGf'
        b'bBHH7BFHHcscKO4gsWl4KljrGBR3yDHcYYzhA7meYeLOc7VPuVP+/8+dHJo7vU4cqQfBIwj+MqvPklMJqrKIw6y5zcSlZVKOUzFdmWxhUdFK8FHdsvCf1i6nKw9msXK6'
        b'CDvUuiyctcyd6CGklqjaju/GeuxAJI9UPQj+mnE5Zs+0k6QU65b/BE2mlrHMFsHHfijfNl9KUNW6zG+yf/AO8WHMekD+uuBhQRsxTKjCUUN0hDVapsao2fAaaA8JgTui'
        b'MiLgDtAzNyQrFzaHR2ZGZOWShMzWYsqimeNWgzU64WK8GkxqNfBKEGXMp/xm/rfxu+J5fpu9wG8uze9YO1vCkyB42lcUOYFeSnqWsHl5CprmzrBsuBM25Mz1mJ2RGZ45'
        b'j4jNLnAGu+eCRrCHKGebwe7V8LTKCSPcKFovBFdQ56CHKKtaATaD0yoX1ABa4BmgE4KLuOkAAfXwUqVsiQqTwktaJozFIB0EEvlXS+DeFXRf+z3BWdgO1UDPJohIIlII'
        b'tlOk7vLkEgjAfFb+hhxjhiu94F+YORJYgbS81a8cLp1ISLqPiRmKVahmp3d/19uTD2xqONR+vn31BH8m72h0WZcw2unRnuQfku2P530SGs/haHYEab9w+kTqytlu+YZf'
        b'0IztTh2WbxTbcb98d9EfZkFiLnfu4Ov7Qcfr72wkNya5zTEeS45bY+mvKct52FKcUf/BX1+3Uto6gim3rfZHEDZJrl+BjwWMx3w8rSZreJSLGCjIVUWEIkFhEM6gngXO'
        b'gEZzsA32PHbDQFvgrXWI0ztgM9zJJFj5YFsiCc5XFghYw4wQAWUlnj0UePH4Gzdu/NFlcpm8uk4s45fRhjpSUSspU04dtqSscFGpSCmuG1NmYOQa9HiykXiURhJ2ji0T'
        b'Gus0s3ds+NCFP+Cb1DfP4Dt90CV1wC7V6OKhKW2V3nUJ0yrvugh1SvVMo5OHRtyar043OrnuzWjN0Ii107WzNRKds26F3l7nrp/XF9M3W79owCt50ClFnT7kyNc6DzoG'
        b'D1gFf4NlT46FT8AZZq8USVXiYbOiIrlKVlQ0zC0qKpGKRTJVDap5bqYcrOt8PFe5Da60RY+xM/LHQHHo8cNG4rtUkiQdH9q4NlZu5I4w2KTTENehMfEhy3ZrrtHcdsjc'
        b'8ckjNsG2G337UYEFp43jRxzmRjBLGC/T0lKspQzsoyg9JZ/qKWOcXWRajNNCVGaO0UjGeqZJT5+rfaqnW5/X06cEPNVTTp4KG8vVmXAbbCcJEdQTEUSEZwClQyFZE2A7'
        b'k4AdoJWIIqLADdiqcsZydQYegzdhO5sAV8BurERgZ5pENfsfDMVE1Lzi7wFYNQ61CxpbyTejmEejj0efKdusv6ZJcmtcUKCZ1Hmyf3LQ9jzt2fdmLUGi/Tkxa5uF7hW+'
        b'gKSkdq5tVlhWBFRn5niy89gEF5xnwANwJ+gWMJ9fRxzfjC7iMJdevzJptUhZN/aFks9wWj5H5pKEs/ve3NZcrb9WMegUhgTK1snIQzLYyW1hDzm6aya0Tx2w8pXbPZMt'
        b'OWbRMLtUXCxRyrHjkzu+RJ4ogaLlyRXL01gSwkYF6kckUAVIoNz/U4Fq5/gTR7iRTMoszVrpSMat3MQkZvVXLWAeWEwbw6NQPVOhjI9mEYxiImABPA53g3oKPoFwJidm'
        b'7UAOpr+KF+3Gp1YxQ1SLoUmCISbgMbAJ9sBT8RT4siQXcrJsOoeoQd3nBSxV4fmAE4w5GJ5JMMoJuBuFCafgZXiMQqiq4ZHJ8cjJEP3rFqSmh9CWtmEKbFYoEzA9MsJq'
        b'Hjy5woOC/qHCg0zjNHKI5P51PO6uGIr6hWA7vIqhGQSjmvAFB+GpVHCDgl9S7kVmyBJJgo/gJcHeKh7u/WhUngJenIDpB1sI2JMCe5GYnKcwDuf4kDkOMg6xDNHDPRym'
        b'wnIFd8RuoDDYCGMrAY6BC/AiuAiOUChH1vDJWUmFTMKuf51xxZ3ltKDvhq8WK+TUINXESjE8nQx6KPDyQn9y7qJtHLQC64we4rkUi5xh9xTYq4rBM0Y+rBLsgr0MuJtC'
        b'2F8USC6YOshES7COVzLVnZ5EPWwFr1IoaNrIVQWCjfBiXA2FcSwuiHxlehoLrcI63rSuLJqiE7BXqFAI8RAbiLS58Cw4EUmBuycJyGV1PUhi+xULVl8iqTmDvfB6MtU/'
        b'WjawjxDA7bAP7gE3KZTNnqFkaWgV8oO3FQusi2kxKvNGgR/GMEMYXcSSQHgVqK0oeE5eBFlRvA8vnEKz5kQytcyRoDMB9iqsLNEM4CXSPCuu1pOCDkyPJKV5JJtIRr3n'
        b'EaTKHc/4JjIep7lySkrBceSywVV4BRkTWpA6omPIGu8qvNQKXs6CcmrO0VNTuPD8BIyBwlHYEMcE11dS4I3RQlJZ9xECv63QWN/dQE3ADY2xkWsZixcNdpCKXAvQBrZS'
        b'/F4Pj0zmwsvUAsFtJNSBYyRsBL0UHry4JEEBe2tt8EQOkWDfgrBYxAi8sEXwKlNhYQ31uMtb5DJ4Nh5cAxdotbvu5MBdoYKXkYGG50keOBroB69ShDsuYii4ciVG0pDe'
        b'sM8bXIRd9MKf2JCpUMIrXNzWRII+0BoGrsFOyuwm5MKtChtrxFAmm8ziToG7mSpsdViwT4nqbUiCaUE6uSdHT6WIgxrQwkP1K/Ck+kikyNpIeHIuRZzIAe7mWteAnSyC'
        b'6U/CY7JkcAjspPW5FfTBo1i4kT7UEDPNUSiFQk1abA6CW/AE0vY4DsEoI+AuFGj1gM2IeDwtETwAjmIZZFOqN8sPXigNp/r0tXNTwPOw1xaz8CwJOsHxONgbQE05qcZO'
        b'gQwG3XaSBB2wAcV0oE1gSy3l/YUTyFV+B0mksgqeckoQVemck0CuXf+QQSxDIhTwdgJVqahOJDfmbUFhN5LC6Ak2VOXfGZPIre53OYQdkoSqqmyqMowzmVQvfxfZSwQZ'
        b'7BVNVX5TOZXcGS9EmntbwYvurqUq/5WbTLbMWY8NpIKXWEOTtGN6Krl7KQpsohFk8iM7qnLDsnRS42fJRlqp4K1fSov6uqkzyf0u11ElonP5O2uoylVZmaSWcRiV+isX'
        b'+IVEUJXxkhxSV/YLiVSocoG4IoOqNF+XR56eboc1pdIouEQPNN1iNqkPWsdCqlBpfOWrV6jKSV4F5MU517HAVy5IZctpQ4tc90IF1xILhhVp75FsBU9SgjQDNPO5chtr'
        b'JEj2ZDpzSg7cR0tfG+gGO5G9vFKLXCiWaFFoGDxcS63hLGS1WpAeIFOJhXM3yQ73A6ckAhZFwPvJb5L7U0OYaKa1vJS1S6hKVcUdUlu7C5ueao3nch6tm6K3yaNMrPO3'
        b'qxdEWoZSlT1Z75A6j4tMNP1qI7/fb9wmhj0anZShxx62aUvJoraTRBn7f2Dj+MJGhkM8HyAF5al8MMsuOCaARtgUlo+sYzNsyMyNhA0o6HZZxgq2hieoyWnWMKkIa2TN'
        b'KquPShPpHYRVqjneMEZrl9eGb63NJ0xmOS8xOyob7srPZBPm/kjZtjJWgyZ4g1oeDuiEh0Evck1oX0NWgS0LCXDaFXRSGu0Or1mHhaCQXx0lIFB4ZFXOtK2U0b7hNDwK'
        b'LyPEy3GIjCQiCW3698gxERQlP+WyCPQvv8ZDJZ1O1tKVwI5DWCFV0vqvzfl0wzqCEqiVsA0eEZbPiMYAbUjfjwO1yo+y3itjsqntRDM+HcgGzVGZ4EwIEsdauZJtsxhu'
        b'owxVATKCwjR4Lo5yoURxXIyKj4s6cHNZGNrVUucKaJubCQ+vYhGOAiZ62w7bqEnAE1AHtwrXwF7T7q0EdARTVCXHJghRGHgKXMC7vW5CCrbPoFE6UaAhhHthn5CyXUT5'
        b'JNhNEbKSg7oCJ0mk7QQ4RCwvX0krTFMs2C1cBV+Nx/AaotQWbFZ54vJmcGZq9ivTsjB5efTy2NQwJyK7dYEe6poK+V9EYXM8JqKTEFuDHSp8CgUvrwMXsnMQUhRsQuzp'
        b'DCMJ7iJkBeEF0CVg0OPeZAFE6BnYG49CJeSOy6bkU4rKd48Qoolficd0dhHlNoD2O+Aa2tTBRrTNy2UTLG9Sag8OJ4AbFA7cvwCcEvrBrfFIh8B+osLciZpDMjwNzobh'
        b'ZYENeaAXOfszLMJqCtMW6hi0v9gJt/kKgQZ5sMt4DC0hRS5+IyVdG5DjgI05WXi7yIQ3Se8s0OUUpcpBTTmJoFmRk5mZi4+QRvfus0MiBaG5kQLYGRrBsATHxOA4Epaj'
        b'ISGgxyVMgMKno2FOYLeLMzzqiuJHAuxwsgNay2jpk99+++0HP1oeieklVt6TlxIUAUu8QU9YXkQGi2AlkyXwFDiJ1OK4wIlmxyXkstQKa7kKW62DJDxg6+8DrtNt2+Ng'
        b'C+y1odsukxsmCGAz2EW76Hb/JbDXhHaTlINDYfCGJ7Uk5nViBcKhLV0CuOSTAw5RSgi2gYt5ihUqSxxfXkMeGl7nwxZAayhawjPwMHJntfAim4pKGFG+sMOFbtxdMR2F'
        b'EfCiNUlFBMjS7o61hrtpUtrQ8pzm2nBBM7LKi0j2lMVOcCO9LodXWSiUlrU4MLpBIhVs90Rh9jU6NmmDLS64EY+2iQSX/Pi1kCY0CsXtZ2GvUg4v4hjvJgm7RB5Qx6b6'
        b'nJOJ3Di8oOQQJDwKriPdQKLZnkBNPRVecuCaW1sSBDOBtIcXMsrgXlMAtbMABT4rrDD9+0i4NTIYXF1JCR07eQnXxsoCoUwiUeB6PtPJ3HQQA05EI98uR8ET04b0hy0J'
        b'YeAcRYIU3qhELfACdkN+JFL0KyngUhWlThMKfRUrqHHAZXINbPFG4e9NusOr4OZ6hSW9ZG2IGwv5oMOZQgoG+2Efl2piOpDg8JJocKyMUvcwoJkI28FVM6RG4UQ4OF5D'
        b'WdvZghLQaGu5YiWJA+5LLByZNKG9Am1Q4RFkl849nZUf2J7pBtslhr/+RCr+glTrZpO8qSBbdi/Z7syvRu8/BbdbsGI/cQTSlpaJpH1XhtTYmxl/dOvWmcUx/unksJn+'
        b'XuOQ1tPvo5wM6ZCvTf8/5MNWF7Z9tG3JLye/eO+U/Nv7H+/44pFF1eMhm9npuxa8a9Fh+X5M4utJ+xf2Cjbfv/maYC1zUegXk+8n/PVbTXv8VP2x28O65nMfSAff/eSf'
        b'P25XXLr/fnzOtpDPa7weaXNeDc9Ld3l8yJgxc7gn9h8N78V0fDMruHT/wFBUKa/+7cmsMpH165X7/2742u3xsT8mvzUx5JFZcvDiz3ZpudrBvwsGWO9/daF/7nZ92WZn'
        b'/XeMy8O2Xm+lfe29LuiLgo//yv/0j4UHrs35NGLgl4jHB7X/2viXWxVGW9nrv7LdFA/dKk/Wb1i3LGTroP9HtwuP1W9emvjTrdyK4gPSzb8VNr89O6HDJ/GnxPS8U29I'
        b'+Iejr4c5ll/cl97oU/RF9pDdaznqP757Var+bf0/Vv96+bGvspb39ZPMPdHzJO+84eJ5RP5J4o0L8rtHnoR8vb+4OWyxpOLerPLCgvIlm99qLp1Rf1h/1exy1i+KvWf3'
        b'bDDU3b3c+M/uyKULO9eM3GPqv3x/y6qDCb+lff2DROH6c3N80i3tJc7Xwjd2D3r/0vjd8c+bvjv5xzVDruDsL+/cDX77r7+RfQv3m5/bIDB/jI1mJGiHHbAxPA/ZNNg8'
        b'TRCOjDc4haw3uLroMTbvMUheLoflV0ZmhocKImFzOGwgCB6ftRQ0gy76sO1ICGgYc9iWSM5hgfNr4Xa6tWceaAuLRKazAfUNtsk5YBcjAnX02J3y3OBacHZ4SAZsyiYJ'
        b'c6gFHWj01Q5Q/ZhShu3poDc7Mzc014wAWyZyWAxzO9hHnQOaAf3isIzwUNQtbEAmuRlZm8NMwnESE3YBtLd6jDU9CvTA7dn5EVjPjiM1SAF77ATWzx2m/OcPBX7wTX8b'
        b'Nz49iHGgDz6UcpFMIaKvcOpeUkcdy1xlUMcyj9MYhFtgC8vo6qHJMbgKUMmJp/EccAoy+gZqRYdcdfa6GK1nC6tlQasNBspoXX/fNcLgGnHPNepBYGhLmobXmmcMwgW3'
        b'9nyjs5smpHXpfedIg3OkTnHPWfjA208b01muFWmLNZUIyL515lPoEQ7h6d2d0Jmgjeua0pJmdPfWrOgMbkk1evh0J3UmaUu6pulidLEDHpEtaR/4BmrYRn6gtli7QmtB'
        b'F1GfVNGDr03bN8UonKhJ03rf9Yw2evlpS/ctMUZPQBUedz0jjN7+WuW+Kj27z+mCtTFAoJt7OFcv7lNeqDJ68rVunfn3PWMNnrH6Ce95Jo4iR8UhZPe7nuGjFZFCVOG2'
        b'Lx+/Sw1esRjVpTPnvmeUwTNKz37PM94E+TAyRh94avkzaIwdFo3eXfbloPfuJZ1L9hc9CI1CNc77skdsCC//7pzOnBGCDE0hjakZj5hkaCb5mCC9ssgHAcG6wEPZ+kBD'
        b'QIIm3ejjr83ct8HID9AuPGSrZwzyhXqVgT/5Hl/4gK67z4838OP1qvf4U0YyScIvaCQHRYl+aAELW61GGGx3hxbOiBXhH9xiS819fz5ifEj4OZseG71iMGSSwSmwJV0j'
        b'1LKHXN07VTpnfVCPD546S1PYaaWdZ+CFGUOjOm2H3UKMPE+qrmiQN6HPycCbco83YcSa8ApHE0IyZNE6bSAoyeCY9CA8ud+pX3LbxxA+G627S2uO1nXQSYBFRdBaNBAy'
        b'ddB5KlpxLadz8n2PMINHmG7G+x5CY1R6f+mdxNvVhqhC0+CFg7zwR/OxvI45IzQfthor2y87JXxee6iTtrGKI8fHzi/TlFQMnkhQx9HfpzJI0h2t0X9+hLibE0Ac5UYx'
        b'BSQd4VxG/9ufnRmeiYItFB+gYA10pYAT4/Zk1qMbopXoscfatCfDV3zEi5d8ZdZP92is/7Y9WpmA8W0VIsOSP+ZvFuaRgi8afyNMXTOvrhHzc+cmxkXzq+VUITZyHOq4'
        b'l0wlXy5WquQy3JdUolDiLopFskq+qKSkWiVT8hVKkVJcJZYpFfzaCklJBV8kFyOcGrlYgSrFpeO6Eyn4KoVKJOWXSqiVE8klYkUkP0WqqOaLpFJ+QfqsFH6ZRCwtVVD9'
        b'iFehZS5BvWAY6biuqNsMGqqkWrZSLEdQ+CJcJZOUVJeKEV1yiaxc8W/mlvKMitX8CkQavoEvq5ZKq2sRJu5AVYKmLk76/S4iEA9LxfIiubhMLBfLSsRJpnH5ISmqMkR7'
        b'uUJhaqsTPIf5Ig5aj2XL8qpl4mXL+CHTxXWq8t9FxkuAp/lsvOmoRiqWKOtEFdLnoU1r9Qw4u1qmrJapqqrE8udhUW2xWD52HgpMyMuBi0VSEZpBUXWNWJZEsRMhyMpE'
        b'iPEKkbS0ejy8iZgqmpY0cYmkCokCmilm1MtAS1RyzKHVz6iZD49WyFWyl0Lji6kk6on6VJVUIDAFelNV/R7VJdJqhXiU7HRZ6f8DJBdXV1eKS000j5OXQqQPSrGMmgO/'
        b'XFyMelP+3z0XWbXyvzCVldXycmRf5JX/l85GoaoqKpGLSyVKxcvmUoD1hj9TpVSUVMglZWha/Cja6vKrZdLV/1vnZDICEhmlpdhQ8E1TE8teNi3qPu/fzGq6WCpSKCn0'
        b'/zcmNTZmSHrqzsb6oqf2rqZaoXy+A5NkiBUlckkNRvk9y43XWiwp/h2KsedSikaFaz7yXGgoqfR3JMw06DNxHD/W74vmf8x3uRh5UaR0SXxkZRDkHHi9pLKYHuBl8NgW'
        b'ockXVYrHLNUoQYgFUnhdoRBL/x2qEjn432GiqR8M8XJiX/C42SpZqVj2co9pGhb5yJf46vEDI5h/10f5yvF+dyZebXi0TKlAlqoMBTG4+WWINXK0AMjmiV4+7ixTs1gW'
        b'kSeP/D3qx439At0v9/8mQXguBhiH/LvxAI0rQUO/HDFzekre74tdUbVcUi6RYZF60Ybkm9qKKYFECsyfIRdXldb+rq6P7fm/INA0+H9oTCpEyNu81OTNFBfD60itX2IT'
        b'/jcQhtWA0jNs58bRNRe1/Htlk4mqxM+snSku5ofkoeqXyqlKXkPFRS9gFIrltWJZKVbLulpxSeXLsBXiGlHS2MAadTAmqn8JxmKZbEkSf56sUlZdK3sWdZeO3QeISktR'
        b'Ra1EWYGDdIkcR6liuaSELyn9dxF+Etoqiqqw2UQ0za14Lj92PGKSaZ+ThPYFL/MM46HHXYrZEM9fiuXS2X3vCxjUhVd0oUeIRVwCfaO0bg19rB/t8lqcWXUMocKbZLjR'
        b'Z3leLOhlEMQkYtKMSXTKhTt99xRdyCmP8eEQ1AmzOdwMDlGZe7DDEV//sITUBRy4ZDErTJAFd4bl5UTCBmkMPuwK4xC+Pmz3afCwwIq6oLJgrgVbwWbYGJWVGQF2RGXl'
        b'ZkdkwabsPDYRA5s4YQIf6rImFh4HN+HpNWFj2h3AQSbQM8AlKk/BahI8nf30GqhyvukiKBTupLJk4ZFlQOsP2kYvfEYveyaDzXT7ISFoh41hsCk3K4KBJnUQbIFXGWDH'
        b'goUUnaDNJgN3nwl3ZueBJnxs5xSVAZuYhI8DC2rg2TQqbxd0w+tQbQKcBU9gWHwB2RCFCA4IY08GrTNUgXi81lp43QQXvooGo67p8nJJQgCus8G+QIUKny/AY+DwJBPk'
        b'RGAaHd/FIcCAZexkuNGMggMb4UmITyybUF+RcDe4kpULG8IFHMIDdrHAEXCxmGIl6AiH3Sawyaszc+EODOPqzIqGlyT0XPfVwdNjlm4x3Ddm7cB+2EtdR4B6sHG9MBbJ'
        b'kw88BfYSpSvBLvpm7VYkaK0D119cLLDfnpIZR6BJEMay8U34BtBFVBSjLqkL0X2wA83iGjgN282QmBLR4MZC6pLMBvbA7mfrC/rAbtMKkyxq/VMtwDZ4S/n8+oKGJQLT'
        b'LVpPKur6KLgoBBdqOASZQ4CzMtBO3xJeBTtmoHrq3DcPHCQq2XAH1S24AbvnjJGLGniREos5IgGHRj0OOuB5jylCYQ2TILMJcIaAW+iEVjOwM95ZKIR6NkHOIcDFuamm'
        b'yy24AxwAO7lCoRyh5BPgHNw3habxmjO+D4YNCOsCwiokwGU3sI8e6BaWSaGQxFOB7eAwUSmLo3IBxeCMlVCIuCkMBkcIqTudIWE/15UIx8rq3TnLZkkiraxACy6Dnmxw'
        b'RoG6SSfSQVcFnbqUYY9TpydGBx0NOlK7lBAwKa0wB9vi8b1hE81Rc3twAGoYYA8XtFHtmfAoPJYdGRGKVxkegxpwlkXYFjKlTgk0zTrQIcYHVmyPRILFIkE3uEiO3q3W'
        b'w0ugjyh+xri4Egpp7QzYOB+eHMO4XNhEKQ3YA89A/Tg1hDc9xqghuAI0qHvcyyKkN7cKQPsYJh+rogaWzYoPhsfGcBjoa2lNu6GIM3WOlL/rBd21MKX7zLZm0stwHBzE'
        b'y5AKt6qCsQjWLBlF3wtOvVSnkfKcpW6+6uBBV2rNQKs7XrRXgqgbd394bpQEhfQFVa+bQI3vBa/GC4VI70qKQTdRgYZT0xbgODzolp0ZkRcJd6xHah1CXzAwCQ+caHwM'
        b'Mb+JzqtrgVoJvg8WRGSyCAtkvc0YYFcgpNOqLQU2VAZ4NKfI4y33WIJWzCbQJqEWcloAvZDw8jzqUDKRt2ishAT4UQKSJKTkA+jgAaQ8WRHZEaF508EO/HGCbTlTvAae'
        b'pMyl08xVY7ITpsND2QCzC1+Ae+SwQBviYyO9NM1+8OJziQxz1ppSGZRsG9CtpDpEKnK2mDYTYFcC9irPTFBoCRucAsdCKbJZU0uf5XPAzbAbJ3TIQYMKf5QSBNrmm4WM'
        b'S3wYzXq4Bq5RPAwF28AJ08W7FbhF3b2DLrgxXxWKWiVIF9qqkSMY5QxogM1RcEcOvmrKxlyIBXs5mRbwDGXcJsHtsBVJL2ralRGelR/BIbjZDMoFnaG902k7sAleFTzN'
        b'EjBlCAANG2kqdTbcBHU1psQD0L4K5x6Aw6A7j17wXTkL4+FWUxaKKQcF3gBXaEe9dQW8AhpNeTLRZmMzZaA+gDIxlfDoynJPLooGCogC2AZOIC3D9bBtIdifAm+azInY'
        b'jFbtluWwnSvnEESuF+xBHkcM9RQ46LYDas4EnLiMs5YtplASVyGhM26iC40RHZk5dF4BNh182A73Ij8AuypBM1E0DekO7n4OOGMOeqOZqL/zVkBHVCeAZtV8HAPAg7Bb'
        b'gVYFNmXOngUuRBfMgWr8dUZIZEQImnloJqLnOpUOUYCVQx1emIFnTbF1dkY4bkEqkz1vFmxiEeDWGnvQ5AVPUMkPvGw2HSUFKV1U5dEEpa7wWB3UPmUd3Dp7HO82WZps'
        b'EbhWaTutBvTGYb8zG1k6UA97aAO5dym4kmaFm0jK1p0FxxaocBrOau84ZOTVmUgwOpAzV69EjyawA5yJB2fZ4ELxHORNu5XF4NIEEi06ZyG4AY7Q7uViBbwajTp61mcC'
        b'aEViQt3tc2Ff9qiD5BTVgh2MUNAcTmd63tgAz44a8ygkHiZbnr+GElKz9fDkWE1PRjKNVR2JqSlTohUR2BzkOmaeoeAWFVEsBsdgy2hogpT6xPjQZCHspoYQLgeNJqiF'
        b'4yITP9gjYFEM80Wt5+CVamH8CmTWszDDLgbRw6uR9T8ojONQ7vwYCkjEfuAonWrSDI96I67vEcatRCxJRk4e3gJdFBofuTStZzYiGuoJyh9ccIfnBSQthK+KUaR3k4la'
        b'Y1DjDJxneWCpCl/vwAOSxVzYBBvR2jdGRdjA5gKotwbn42JmZYxK4JyIwjnPSxUyTN2WcB9Aa0s5AnBj/jqwH2wEpxDha4m1Gb7UyE5xsCPPDpyKB+cZBMOFQKFLK5IZ'
        b'bP7dyqxgF6L/FPIe64n18DS8pYqmvWMX1Cioj0vmhOArZmwo55tGh1fgJpqC+RFmCPSYjyqRUv6oBG4ecrARhSZVgQ3zM7KylPMy5tLzAT2zoDo3IjIvJ5+Ns5n1lsj0'
        b'XRGYRBvewHTBa1CHvy7AXxYsg4foWOYUovEAkuEzOM5rFcJOApxakInwKIvWAzvmjApbMVIik7B5o3CeSuw6isRk01h5A60VlLyJ6Q7ARXganMRpO5etSdAKXyUY8AoZ'
        b'BzfC0xRhi9fVKuDlGltOLTyLmhrIoAiwhcqtkzivncpU/A2ZjwuxbccK31UUJNjtfVw6bdqGFmNQfPwPwKJbsI3YxpAI4gZAk2hiNNNsuxfj+N+gInjV5LuHbnQ+ui30'
        b'Oj5lq+Pj3Y7zfw3/lVFYmbnyb58ObFp1IX/RLxeLhpd8rnpY/f6puMSuJx9c+uv8PRHH3aLffVRE3E85d+EtztcGjzcuOp2uzXjrL7eXxKS96fbxO4KrlYHLe0qFmkiv'
        b'+0y7JULL3dJvfpW8diLokd3EBqb9hrQczVby83+uUiepsk6odHdb6lYwIiYdWTW5+f13w2w+33f+dtbHOefL4gT5j2LSzKVfX3md/+FblVPtztTqglPrpjsf3l6xRVr1'
        b'y5afwx81p+Zt+yD84HzR4W8TT3x5KPpV31sp8cm3s5a3v5Lwk/XfvY0rh8vCv4+Rl7eucf1l8s54103vNX354RNuYEl9o538D7NOC9PeXxGufeV7+01bJpHpsj9W6hZY'
        b'l7cu/vbD1I41TlcvxfzrHx1Fqb+K4JsFYYNvX1/y1t/eZpwZefKrgtPY/+tH+tIzD/WTL3B+mFlxKUW57bNQw5E0/8Nvqr2D6zZXHKzY9Fnm4RPqs/a/vDEQUba+pi74'
        b'yd5/WC1fGt+6/JOgP70plr7ybXzWji8vNBTXhnfP5eziRR3SHSl0Kc++tOKrC7uiHewP3LkSxOi7ML3cq7P1Ye2q8InMoYdV33i9P/P9f84ZStoi/CCnJLLnn59Kq07M'
        b'XSmtfb90y4w/qLzLf/jTV3+c6LT/WG+V7vqe72599+b1og/8N33v8dbQv1aA+dHrVSn1u99i7/lmddcmTvof9vfX/fmd+V+u/fOT++E5WfWKm5cZbcnv9dg++ExzJvYL'
        b'84YlfOEXjDPfay59+lb7hMDoDVEPQ+pdOh5utnz189k2P791IOfJrs9e7/kaxvywQftz9oIl+Wsa3+1kTbs582LTloMpN+ZNGAwPerC1/XNFrNunP8WlJ7r1fiU++vDr'
        b'VWabwi5nv3JM/cUHR3tuJuRMXsyN+3XTG/PSflZPfVRoMfN+xVyt5pejd0NXhX73WsSZ1/mfnQv7y03h3yP7vhp4FOr3toXaw8YQmZfy8z/FvKo/7Z705rs3Ps34sKvk'
        b'u8y+bVPjbj4OWpEgWL7uH99dOfHZr9U2og0OKJTcoHFw21D/GjPtnS/riUfFjissV7z3S827i8AXiSPf9v225Hi5oZcdPft0z8Jzi78aTrgdtGbrhKON9gW9JzPWOdyC'
        b'kalT61/9OPTPf5HM/fvSu1GTGAo969aPnu/0C9prn7SF3K6Cr89/ffVH5+x/u/Da/ezfYv7oKvhO0Ffyxj2zkQ/svVJW3olc2RZ82zEloeOftTE/wuFzfFndlD8YFv7t'
        b'7P23gsOG5t+YYZxyGaw/d+3SPJe9fQ1/mtN2ufX9vacdJy+LWn3xW4vLKTXfm60R2FBZN/AsPAlumtJ5XGTIImKbiOIsV3CZlRGnekzlAd4E1+3DQiMFyPEQhAWsX72Q'
        b'AY5lODzGMSEbnAbbw3A2EbziNj6h6Ba8RWX9BKa7PE0Y4oBd80E7I4Kb/pgyhhf9pj5LF8qdgpOFUHxB9QzOo8j8LGyd+TSd6WkyEwmvUNlO68DOcC+ncWlDppShNSuo'
        b'bCV4DmxKCsvLDc+Cu/C2bftKcJVRS4Kr1OgzYT0befQdUREEwaldDa4zIoEGtFGZTBsQ6vZsRBc1pzlheFa20czymYsp1FjEFPWYiMEdHGKEVrtQ84VnsyaGmbjFAafF'
        b'ExhCeDWYoic2Dp7KgGrTZ2FPPwqbPpGecT08mAx70QqgwKtAXjP6PeRkFhPeShTw/5cTnf6HHwosUi+eodKZIaN/475xq1ImxkXXjX2hkql+5dDfuMk4hBNv77TWaYOO'
        b'Aeo0o7OreobRiadON7p5qbOMLq7qmR/yPFtYQ45emlJt+j3H0CGPYB1r0COiJc3o6rF3Teua9nUtLKO7rzalM6zFbMjVw+jkaXR0xV1qhe85BhuDQk8sP7Rc76gXDQZN'
        b'bM1vSWlRacQPXD21rLZ1Qx78Ic9InUq/1BCVds8z3ejp153bmasLvOcZ/SAqziiIMIaEG4PDUCfG8GhjRIwxMhY/w6KMoZHG8MhHbta+7vvYI56Eu482YJ+XMSJWw9ZU'
        b'DvJCjW7eVIWHtzawc7Jx+sw3w26H3SkZnD7H4DlNk64NNXhGoHEXDkZNQwOhCsGgZzhGijC4oc6jUDcVXbaoYsAvy+CW9TAoRh/Yx+hj6kP7xP0pVyvu+F+tHgzKM4ZE'
        b'6ER6ho47FICnMVu/Qlc3GJD0yIzl665hj1gSnr7aPINHrDEuEY0ROegZg7OrZAavOOOEJFQTNegZO5pvFT9Jkz7gFzvoKaRqupaMAcGz6fIaYbjw3Y2eAl3cCBOVHngG'
        b'IMY661f02evdB4Mmj7BR5QiH8PLXpo2Y4bI54RWoLR2xwGVLwgut3AgXl20Ir1DUiS0u2xFeYbq0EXtcdiC8QnROI4647ER4RehKR5xx2YXuxxWXeTSMGy6703164LIn'
        b'4RWkVY544bI3TYMPLvMJr0idcsQXl/1oGH9cDqDLgbgcRAQGG4MFxtDwr8PQu4Y1Eok5Z985kc6vuucRMRQ2QS/uS+kT6Zf3T7hjfye2f5IhPm8wLB8nqXXmGAOCOtMf'
        b'hEXpzXumjtYEatKN4WjdenL6Ug3h0zQszSIDL4TKrNNlGYIT7gZP6Uu5Gzy9397gnaphIs75BmnFutQBfrQ+e4A/TcM2+gRoCzrr7vvEGHxi7vkIH/gF6shDwZpUnMtX'
        b'oi3VchGMt4+GiTtN7Vx+3zva4B19zzsWkZp6fnl/6t34mcZRnBEmgbp7CvXeM6jB+JkPQiLOcXu4+vQ+//NZ/eRgyPROaw1Hyx4SxOkL++YNClIR+Qs6bYyRQn2KXqRb'
        b'jl6XGHhhD+InIaZM10vux2ca4jPvBAzG5z9ikm5xGidNpcEtVJdq9OQP+MYYkBDxvDQyAy/iPi/OwIvTz32Pl/RUSwJ1TncRj/1iRwgyLpM0Zs9BncQVkN8QpP9cElV6'
        b'zSUfmPB1xQZejD7cwJt2nzfDwJvRr3qPl4t7ijS4RT/w9O7O7MwcCEruDxz0zNCQDwNDdPbnXHtc9fan3I8UGUME58x6zPTkKcshpFO+V4LPB/f59mKtUl2VDQbljlOd'
        b'9H1TcY5kujbiLjIIsQmoFH7XM4pSyykGtykPeJ544BA0UVR86B2JKI1OMk6Z3j9zYHIOmkJ0Lp6CTx6eglse+cA3qC3roZs3Nl0bWjdoFfdcw/ROV7zOe/Wp7sWk33H6'
        b'k9dbXgPzF93LXPyQxx9y9RryjhyImnHH1RA1a9B79gBv9pB76EBYzqB77oBTLs4HXGxwDhlyCtKqdEsNwZPvOU0xOtGfDAfecwpBrG9JN/oGtmU98OBrve96RL/QH84E'
        b'9TZ4ROsdDB5x2Kb6aufedRXgfNJpndN0wnseUfq0K1nns/oUvfn9ortxM40BISeyDmXpFEfy7wdMMgRM6kvr9x8MmHE/IMcQkHOnYDBgtiZ9KDBUF9NTgpM6+3zfD5ys'
        b'JUdYLN8c0hib0EeeD+lL7/ftF90OvJqjC0R6aknExOtFfaTecigysS+wn+xn9AkGI9MesZkCPy0bmZGAEF384anGqanatAFB0t2AScZAga7wyFJktLRpOrfD+V97EUFT'
        b'kK4jQOu7/vHG+IlalnaJgS/EKZteg55R+jiDZ8J7eO2Q+t11C8O5mK8YeKH3eTFYnALe5yU8fJ45I7PZhJvXo7lsws55yM5PO0HnbfCfeM8u0Wjnste61VojvmcX8MDR'
        b'TZ375HEMERL7NcFAcxwKTTBMzDCGTOsPNoRkfsMkE7OxEITlYCEIRE8mhvpRYYX8oIFtXeDFGvTyKJhoRmdn2g2z8CXZfyEr87/ss/Gt1rKX+Wg5/qhonG9uw/BTCTp9'
        b'U8QiSYfvCfTAOZwO/2kO535OOHGam8Acd0E3mrD5DZ7fXkKMf+KHWMQoJRcxVzMsygTMYTvqZpDKmpSny+XV8h996LtCiky5KQlSXMoXyfhi3B6ZJ2ANmxcV4cvVoqJh'
        b'y6Ii+td5UNmqqGiFSiQ1tZgVFZVWlxQVUYymE2IpLuDTgLoXhm1GpCrwd35biY+sYihw+qLrVCzUc23gFSXXw8ICBaZ5EXJTGBcFuzls2AVPC8gZkty7wyzFctRJ76Qn'
        b'4taZ+TDZaWvtn4tPfM/Y6lIXdej7WYxpm366Y76CmZ0cEHmn7f4naru9ryRu83mrt4Fp7jP1X1+9s+bapJ86VH3+iReOTDx55EavK1zmoBg8+5eH4U/6q+N51yrXnpt+'
        b'cmBRfjvzTN4iwT3tzyufWN6rcek7VVj7hvHW+kXZgTMW/brA3bn6Ub/942/Cqks6PAuBeeXBq4Z//O1zv9C7fpVvq4dePfFgelravd12V6zzb5Rl8H94u3X6Pk1Khyb1'
        b'4ILk1gXTOxek+Jz3Yb4WymlI5QXtWrZ7AeSt8HR8LTPH/kRM6v7XPVd4c19LDxe5hS1I96pc8CYn/vy2qn8uc11jrD4xtS/4IVE/cTrzzarX27cFlCatmVOa4xysXPnu'
        b'u7NXxlz57I3cz7+Ju37mwcc7GlmJBcqCdN10x9Wz7cTCTcLF/1J+Y/Fb/jv/GiytGLb6tMPlk/utv/04+dc7y3f+9K95l+8tfdtQ89fuiz4fZ6/8U9OpqK9WVtc2hgpY'
        b'j+m7F3ggBDbmkAQ5BR6aSMBdMtDwmDrw7Q0GF5/7KRJ4xRvUs/Bd7unH1IH7Odg3mxuKon683XgK5wN6WaAjCJ7zAL1UKF+SCU4rwJmMvIintw32sIWZVAf0DmCnwI1W'
        b'QPN/+/ifi9PxVoSfTP1tfOGPDtCRykirRaVFRXVPS1Ro/jOS2V9RaB5OWDuPsMwsXIdsHVpiG2s1vjvWdiq0sVrRoQlddbrZ+zacD9DL+3zPq/pmn1/VG3k77Y4DzLgb'
        b'm/Mhz10TqxF1Tuiy0GYZeJF6VwNv4sDkPINr3sCcuQPzCg1z5t91nf+hC1/r0C4bsAtAkQlvAYncgINTS0qrs3r6dyyORch3diwLvxErc76l0cq2xWWEiUtunpoyuhQk'
        b'0MXTJWF8H4cuJaf2F1KlBxQGG5coDKpEYVAlCoMqURi4hKIvazuEY0aX3b0QlqkcHIrwTOW4BIRpKqeQaSTCpt7MaWwLukxhm8rhsX2c/kKjvaumTBf/suLXtghwwNwT'
        b'RbYOPFRD//8Rl+OHar2/t8shLeYj10H/s5RBWNoNWdi1KDQTWirvWfh9z1jFtHD/nsDPb5iEpT9+2I2w8PvISjNUfswgLWL3r0YuyCKWanyEK56MiLmkRSY55OBz1Gog'
        b'YsYgf+agQ8aAVQbtmHak8NI4xGscxzQ3Ju2YnIYZyHT+97mll4qt00tc1TN3hU+fnwkr3ogrpph8lYAk7bCrsvsWP/5TV3WIE0Oc505mShYXCFiKtaimYNo1cdOUTYWW'
        b'W5J5abemTRjunJs5sCr4nD7DbvBYTpLozS+31I+0+WUn1+xLeL3kk/lrvvvovQ9ydnlZPz5m+21W/fUv/+qyyypJ0u2VGzxpvt/qxfdvL81ctitfEh3Nspjzccisj3Zy'
        b'neZ/WFN/CDBz5yd55KcESQQbzv7lkkf3T9YCM/rk5kYZaKR+Cg3uBb351AWaGcEFFxjIwOnAXupjL9CrXJOdHwHPI7D8/IiFoImBzNB1JjgEND70kcNW0MABjfh6ERm+'
        b'MmUuvqswI2wcmN6zUCf0D5QEwE3ZmbngALyCP9zCX22h4a5SxyTF4HwAapsf+fRH1rgCBmxZCC4/po6z26FapMjMjUoZ/yNscLMl9UGX3dqqsCw2bAJb8FU31MBNoF3g'
        b'//vG8f/4EcdL5dJ/1Jy+aExfalglMomSNqx0iTKsM9Hj543EN+4E29Fo7XTf2ttg7b1/1aB1yMYZRpZlfc6mnAF736MT77HC/8zy+YBl/T1nDZsd+z2Bn4+p50gdl7By'
        b'2pg/5nMe/jBTKpYNs/DXJMNspapGKh5m4bQpFEhKStATfxEwzFQo5cPs4tVKsWKYhZNKh5kSmXKYTf3kzzBbLpKVI2yJrEalHGaWVMiHmdXy0mFOmUSqFKOXKlHNMLNO'
        b'UjPMFilKJJJhZoV4FQJB3VtKFBKZQonTyIc5NapiqaRk2ExUUiKuUSqGragBY+m0tWFrOtCUKKonxkfHDHMVFZIyZREVww1bq2QlFSIJiuuKxKtKhi2KihQozqtBURtH'
        b'JVMpxKXPLA91BrXs3/7x+bTByBl94J+yU+Sjx2+//fYLMhe2JClnYnsx/vmIev4n1gPbytsWnBQ34rYbNyWA+aP56A+RDdsVFZnKJoP1o3vZ+F+T5MuqlXzcJi7NE5jL'
        b'cdyNg1SRVIosLUX7JFxlidgrVypwzt0wR1pdIpIizs5RyZSSKjEVqsqlo9LwLKodNp9Mh8FT5XKCjrsVmegxwiRJ8hGDRbJGrAiu9Uazr1lZHNJpZJEVYWF/39zDYO6h'
        b'ybpnHjwQPvV2EAwxhGcZze2GLF0GXIWDlnEDrLghwq6F9x7hTg31/wHY+R70'
    ))))
