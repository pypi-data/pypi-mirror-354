
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
        b'eJzFfAdYlMe68HzbKEsv0mHpLMvSFhFRRBSUjoUFbPQFVmHBLXYjtggCCtZFUNeOfRELdpxJr2zWhIVjEk1yUk5yTjAxxyQ3J/lnvg/s9/7n/P+59/Ik4+zMvDPvvH1m'
        b'3t3PwRN/7JF/f1yGi51gNlCCCKCkZlPuQMmaz55lAZ77m80aSzG1kJGWEj5uZc/n+oGxIy0T8P/lGHYqaz7PD8zmjELIqPlmfmD+oxkEoJJrsUHI+1VmOTs/bVquoKa2'
        b'XFMtE9RWCNRVMsGM5eqqWoVgmlyhlpVVCepKyhaVVMrCLS1zq+Sq0bHlsgq5QqYSVGgUZWp5rUIlUNfioUqVTDAyp0ylwmCqcMsyryf24Y3/55Otf4CLQlBIFbIK2YWc'
        b'Qm4hr9Cs0LzQotCykF9oVWhdaFNoW2hXaF/oUOhY6FToXDim0KXQtdCt0L3Qo9Cz0GsnkHpKXaQOUnOpmdRVai3lSG2lllJHqZXUQuosBVK21E7qJOVKbaRu0jFSvtRd'
        b'ypOypJTUQ+oltY/xJsReaK7wzvV8TECFjzeQej/+LPV5XBeAJO8knwDg+4LWCpDA9gEVlEWlkJVd9iTb7PH/jmS7HJrTlUBoll1tjuvvKViAA0wcHijOtJNJgSYAN/r7'
        b'KFETaszJnIkaUEuOELWkSWckog1iHghO4aCb8DJcJ6Q0hJ5oPbyQpUrLQltQcxZqpkA5umSZxoJ6dB7qyqgnUHAYRWEdLibZF2I0MG0AphcXU8QM088C042P6WaNaWWL'
        b'qWaPqeoY4zBCISr3CRFTsDCFqCcoxHqKFlQSi6bQc62PKFT1f6dQJkOhIDUPWIHUCWxBcfVhqzhANzbFELKZ55lhsj2wjGEaf8mxAHZAJ+cXF1tdnjIyUjUejwO6LN7k'
        b'4rCZXCk4DqotCYlZrpNOW3wdCMC94B9YF6PgnL9Q1UTfOvPbKXOnUlswuTj6TvRb/LOAbp7l+oPtqSqhD2vGXep31zbrL8AQ0ITjDtiYZoaZ1RQxMwS2orUhaHNEqhht'
        b'hsdzQ9Kz0Naw8DRxehYFFLYWCVPgoac4whndcjnhCJvmCOEGiGE/ojn730jzDc/S3Ow5mvMZmr+Raws8AbCziS0O080uAZoIQslytBbvtFmUgZpRY+bM1LSwNCmIzpjt'
        b'DHfkwia4EwtdDzYpZmg/rp3TuBDqtIQjnQRe4gDUjc4AeBwsRm3wjIasCusFqE0Cz3OANBDAvWBRYjTd7orWzpVE4/79NQDuAmVe6BjdLkDnY9B2LuxFNwAIB+Fw5xoa'
        b'2UY2HzgBMNnNs9gqdLWcYfvYHEeAVanqZ6tiz043HpCHfZXEVq3BPXNOmXrK9r1lB7tesYPVb70BeLea8/5sZdW4ysrKMMN+nb3OdbZ5T7gHm52ZFVpmrorskfLZ68WH'
        b'eLlZfo7s9aypkfwpAVw/uOd1O8uYIpeQbW97vjPmlXfqqfqjUZyenvqqvxdPi3zX9Z1bUGe7VBquMnc8J5K6xhmpl9PseQObhawH7hgLqq6aj+kozNKIQ7HIsIAHJuMm'
        b'jrmd4oEb7q4TxWJSb0ZbUTMbcMaj82g/BbvhoSIhZ4gVIlRa4zGPCxXhn6C+vn5ozMQKZe0KmUJQwVjtcNVSeYV60pAlbZKLykvUMqUtHswiUHW4+Lke3E+mgJ1j69im'
        b'FdqZTWvujBH0+8b3Sg2+U4xjpvbbTTWN8dCWt1UPjBHp1ANjJF3qhukmJw+trC2nIcXk5LI7tS1VK9NN0c3Uyrucuxbr7bvc9dLeqN6Z+rn9XpONTkkNKYOOAp2z0TG4'
        b'3yr4RyJ3SiJ4Qt4Qd0lJtUY2ZFZUpNQoioqG+EVFZdWyEoWmDrc8s0UeLooFZJNKG9JoO1r4k94Yov714OFUiqIc79m4NC2q5w+zuJTTIN+hafw9ju2GLJO57aC548/3'
        b'uYBrN/rpVxWRle08f3CIH84uY71IOSuIcrKIi6LVk3pCPVlPmUS291PKJ2U/pYisJDatns+1/udO4xEKj9STl60hdtIa3rRG27EpEQcXAPEEtFdDjDu6qkTX0XYcVESs'
        b'gNdBxDxruhlen4UuYL3BOjMNrgfhM6zk2W9+wlKRKMFJPsDogtMrb9RT69zWt2e2C76bf9RumnXXMj/RjC3jN6S5+L2n49yutfzwLOxrd7pNAYtcXttH0ULqgSueYe7i'
        b'8aJ0MWpIy8wWqbmAD7tZaO9SdEHIfpaBJNgZ5d4Qn5HHiuraErXSZVQgwxiBHM6lgLP77qy2LJ2/TmV0EjWkfGLrZHLFQtfOb+UOOrprx26f1G/lq7R7LExKQpghbrms'
        b'VK5Wkn0rHV8gQLQEMQLkMlqIRgXoVyxAs7EAuf+rArSDFwAO8yPYjBea4Eg9WFLFATP6alzL2oGGkAltwl57v0odGwnbyjmAVQrQUbgN3qQhJIucqK/NNRwQ2Vdjmmk2'
        b'iYFoSYPnaYAutIkCLBlAx7Fb2UFDuEldqK/jXuKAur6aAnG9vWYMblyOtnkTgFmwjQ1YlQCdRMdhBz1etMSN6o/egOWob7WpuMOPts1uSA8bVepxkbAH6TBOCoBOoC3h'
        b'NIAh1p3SzmrkgMl9q7XBc1QaZ4LSRXjGhwDMmsgCrFqywBF3enhdvCc1P38HBwjw/DGRVvT86JqDrwqdHxsZCK/jDWDZQz1wVzANUL3Sh7pbs58DivtWF3jVqjXEJkId'
        b'bEdaGgSHM0e4GGYDQOeLEUOmz/x8qWXBhznADuNUPl5E4wTXZ8xVKcdGLqOJhHE6hbbH0sOTpvhTDT5nCR9Wu1oEshl/dGZcEurRREVKYAPeMtyJcUKdk2mA77MCqInm'
        b'esKG1a65RrmGGGLUDW9IaQh0MxfvGjskHFkdQpdpkOmqYMoUf5XwYbU278NyZt+XEtFJlUoSuQp14zXWAHQG70xHA8y3F1JxRX2EESpt0C92NONmwEYLeokJ8ArmHNwD'
        b'UK9ZNT1+pVMoFebxDh5/S6VdHOjGiMahCbCJBoBNkWYYoAOgy9boCg0xc6GYmhHUTzincg0ICGe23YQujkc9KitLuAdewNtAF6iYebMZeXUNp17h3sEAt1QFU9R+NEr+'
        b'cPMMvjI2MgduIGQ6ije1HF6lx+umR1K9K/9MeK0ycXpr6AU0aBvq5aNuzLk2eA6D4FCUXW1DA1jPjKb60r7FAHgP+Zt86AWmoR0SvmV0JA4LejDj0C7KAvUup1nKR7vg'
        b'KT66GBU5tYLMtJGiXObQQKg+HzapUM9Sm/IasokDlAj1rKJp4oyOoo0qC2ss08dQG5nxJhVbjI7QcPOS4Hb+Yg26mIx3gru6qUB4JJDuEsyEB1V8pRqegkSAkJbyLkTr'
        b'6Cnt0U0sjWp0iV+BJ8N9LZQIroV7mODlCDVLZWNtOQZtZgE2l0rIiKSRnwTPwsu4wwbtWkEBtgU1ORZtoiFkEdNw++Isb7KnXiocbpvCzLSOb8m3roPNZrEcwPanJueH'
        b'anA4A0LgqUQi2bAzEWtCHUCn/fwZ+ToEu8uwosfMhy08gMM7bBga0W6G0e3oUiWRPWwqtnAZpTsndWf61qGmXBUhuK3UmpDvDBUDNxbRYg7PoOO1KnQR9xXAw6TzBCWB'
        b'+2C30JZRpqSxVJzFMNFXVYHmjBXdeLt8HBWz9A/ciBk7NobR7Hiv8ZSnE8XFWqoyJUwIpRv5vvFUTLYNbrylMjma1dKNG4MnUg+W2XGxgqq0ineX0I1r7CdRVRoP3Ijn'
        b'TPx2HN3osCCJ6sz142LNVBUs/p6R2/aIKdSDHDFuxCM9oiqZaN8ymcoUSLhYIVVas34nJhZcOI0K8I3DjXj1OQYzxuiapVJ9S5OxW+xb5Gr5wJJubF6VSb0iy+Ni5VlU'
        b'IJi4kG7cI8imdB5zcOOtRSa5YxDdGFM7g/pOUMnFWrBIW/Yxl27sWTKLui1ZhBvxSIfILJqPcA+6lKPiW9rAHbOxRFhRkwsn0R3F6DA6ylfaWM9Hp7AM2VMJCSsZBuvD'
        b'cFcPurRUhTpc2bQsi1iT6b7gKHQVawA2kjPQPiKUOyg/pJsv5DDHIu7rVOSc8WZ4p0tdlxywY2iy8g0qcnIydpN9taalHxfQjZ8vfptqyMrBjbdqC0KUC+jG4JXvUgUi'
        b'qRnefq22yMblqdMKdzQaqSJizh05P3LosyOI4f7PnBJ54NmQKChbI8B1C+xfj8OmHOw4tqLGtKxw1IiD6uXwyJhiTnA6vEDvbx4OQr6bRoLG4szf05YyJ4XVU8zBz1n+'
        b'JDgI+5OjG2D0Ye0K2JARkYG2wI05OWlcYI42sJbbwJNM7zG0Dl6DPfA8Pr3Abm9AzQHwlAZeo3tj0fqZohAxhQ6GooaIbC6wqmTbot3oKs31QowoBsX4x8MLBbhogdeV'
        b'tEskRfQSrCPumNGTi63klTymEeJjbp29N6ZOsdW7pdaANhs+Kei0JBJ37pMCuA2UzIXn6LsDeBFdMcugjw5bsbW6SS4GMuDWiDR4OoQCAjXXppKRS4zlJAkOe9A2EYA7'
        b'QClsht0aH5qUXfCYCB9k6RsFfLJN4yCdGXAUslEzvJrOuN3T6Ah6mZzS0BW0jj6mcVYzPYcL0FYJ8QFwLzyED3GgOoWie0LmwLMSCR6xCe7DaINKtB3Tk0blMDyYIZHw'
        b'AKbMMQAPgIWWXvQmp8AtEkksAEtjAdSCcngQm2YSKQTHRmekE9yy0RbCHZs6T7SHHbcIrqfBZviPlWBjCncT1NqBDDUvp8FirFBjRmZ2bDzaEoFaRBTgz8VWEDbAw0IW'
        b'HVjDE7xwSSyLxGzYC1cs92Y0eHsdvCqJxeidcwHY2VbmwwZGUU8uRNtXuaAmfJLL4gKONwUPJo2cVgtWwNOSWArgWKEXwE5QNZOn8cDtlXjBdhHmBtq1IAQ1ZsPTHGCV'
        b'gAXkiJymUgSq95DAi3jyzagFh0SgGnUGMVJ3UBRog66hpsx0cipkoxsU7MAhXo8mm3Y8m2GvCh1A+zLT0rLIxdGjg3pIuDA0K1woZlnCIzJ4FEeeh0NC4PExIiHcgQ6L'
        b'nOCOMc7osAs8xgJws5Md1DnkV//8xx9/GIQcYD7NgQhjdYsgA9D4zcOn+6vwUpEoW5zKAZzJFDyRyBI60X3KPLhtMlyvslZqiNXaR/nD09G0my1dgOWk2x/12DBdFykh'
        b'vKRk3NJhe3gRXmShnhGwG8SrT6AnjC6uhkfxhBiKsXU+8IgXzZO0QngZXfBVLdZYktjyKiXIT6Sny4PtMmu0Dvuypeg8lw5EfOHpmXTfQqRH522wj+zBfdYUHQlEL86g'
        b'l1oGj6N6kMW34cOt2BrPpebBDRn0AcrHZ/y8CpXacimJhK5Tnqvl9JYmooZgtHMs6SDLrKUE8Cy6QXdZyKfPw+zrUSvReRLQ3aA84OnxTKynweEBOqfmiaMBhZUAK+l5'
        b'eJHRgmvwaATqsOObW1sCwB5HpU6wYcKelkS4PjYXR3yLrQjSe6hgeD2YCR72oWvFfq58GysLDDKBSltkR7evyUmT4YNDj63SBm/GhhpnxihUYuD4/CW4GZ3DEQDbj0oK'
        b'm84w4eYEdANdgbtVi+k14EXKG+6JoilTgW5YYG0/rLJk+LONEnCcaIynpmKLsBee4NM9bAcq0lxFL4MOpYrRdmysw2AbNgJhbHSCDqng7nw72GRruXgJVoyd5RwcgmD7'
        b'1y2j17GEevgyVsaWx7tJ5MjDhm5xVT9gR7Ti0+GW2ROy/ZPsTv9tn+3n3bdeu7rq3fd1CxwCHBzO1ulZg2+CPcoMm6RzHOpca9jf+rgNcWC3YGhe20zp57/oJWu9ek8W'
        b'Daz86cTRq9/fgF2fvLzW+zUwW1//Fnez03SqYOOeh12GuFV/+e2o19nm1yzTb/b8smJiUbBv98c7xisOvv7t5AWJ5aFHT637vf3XM6qBdXdakurKH+6v8NldeulUhfTE'
        b'tNXCmA8OXAz9u0ip2dNE5Zfw3p1u7fFK1K7QspYZmw7u6fT4ttjksX3q1mudpXuvJ887/EXxofoI/u8Zwzs/mb5u9p3vfqpK1zTOW7c0oFD2myLr6F/f7FxneSlIc9XW'
        b'kLrsr1Pe9Zn1Y97wfu6qrOHptwb+mJxXWXYgPgL+ySlhz1tdH4k7t7+1q+tm2kdLDiycPrz0NZfL4y3efut64+8z90bavB12p/s9C9mXv782Pfgz7R/ffPvOsd3Hz3zp'
        b'+OrHqtXh4zafO769vf3Nls2TXPb/Ojklq7714Owvv4vyeXgsHN7OGKvrGoq85hdx46fPp6WYmR0fklzfcOzmF3MqFQOX5148lP55xi+FBzLVOdeCaz9oX2Hf0r9i8G3j'
        b'7bSi+LQfrp2a98e8S+Ma1/yuXBU/d5uleMusdzbON7v6w5D69tpOx8jKUk7ie6rPd25+yTajdsK9Bfps2atoeUpH3PVNd+/xN+YuDj/SLDR/QCzmSniZQk1h2XU4PG3M'
        b'RFvDsN2GJ7HhzmA/oK/AT6kiReFpYaHCcNyJGnFLr6WrgFOIOtEB+pICrR0XxXd48kKNwl4bvUxPj8Pis36icGwwG/HM8AjU8eAWlhi1wPP0VVxlFtybERaSCg9AbJEz'
        b'KGCOF18eiTY8ILoZig6aZaRlhWaZAdiN43EOyxwey3xAQhKkQ+1sUWpYKJ4YB+jNaCsbNqOjwHECG3WgLosHRIVmoXqkz8gRY1NeBVhLqKQidF1o/czdyb9eqEghGPmr'
        b'r3907+LA3LuolSUKVQnzYKMkF2j09csZFn398iCZBdwCWzkmFw9tpsFFiGtOrlrPfqcgk2+gruSAS5d9V5TOs5XTWtBmQwaltr004CI2uIgHXCIMLhF3A0Nbk7Wubdmm'
        b'oFCt2/Yck7ObNqStcMA53OAc3qUacJYYnCV3vf10Ue2VuhJdqXYRHm7fNn1k+DAPeHrvH9c+ThfTkdCabHL31i5uD26davLw2R/fHq8r60jsiuqK7vcIb02+4xuo5ZoE'
        b'gbpS3WKdBVPFM9JVD4EuuSPBJInTeRs9I01efrryjgWmyLE6D6On2OTtr1N31Oi5vU491qYAYVfuoSy9rFfdU2PyFOjc2nMGPKMNntH6sR95jh8FjYjRuRs9w0Y/hkt0'
        b'bh055FO10SuagI1pzxzwjDB4Rui5H3nGjoy7Fx6lDzy5UJs8OprAiiJ1Yzoy8af9C9oX7C9qL7obGqFz7sgYtgFe/vsz2zOHARWaRJmmpt5nU6Fp1ANAeaVTdwOCD2To'
        b'Aw0B47QpJh9/Xdr+NSZBgG7OAVs9yyiQ6DUGwcQPBZK7TNuAINYgiNVrBgQJ99Mo4Bc0nInjPz/Mtrw2q2EW192hlTdsBfyDW23pPXfmYGKHhJ21OW6jVxlDJhicAltT'
        b'dNxPXNz3abqcT/rgDWvz2q10UoOryBQascf2U7cQrY/J1ZNuLTK6ju11MrgmfOg69r418ArDW8FSY9GW2B8Ub3SMvxs2uc+pT37LxxA2E7N7TFumzuW2k5DIhrCtqD9k'
        b'0kfOkzCHdbz2iQMeIoOHqGvagIfktofEFJHSV/7G+Fu1hog8LYdeK++2a9gP+URIn7gANB+yekqqX3AF+KyOkNi6+En1oFWBLqaS/vFg5FKZRVHu98H/w8XgTl4gOMKP'
        b'ZAspxpFf8lyWkRaWBtthC46dcADQsQrtf+qUZT16wCFPwpOsR05Z5IUOPP9GF2P96NTF+TeeuipwNJyGQxDLGcRYqAQlTz/l0u/Dy+tkgqzc8TGRglolXYkOt7RMUwuU'
        b'MrVGqSAw1XKVmgwtLVEsEpSUldVqFGqBSl2iltXIFGqVYGmVvKxKUKKUYZg6pUyFG2XlliUqgUalKakWlMtpRpYo5TJVuCCpWlUrKKmuFsxOmZEkqJDLqstVNKxsGeZ6'
        b'GYYkY6ot6QcFpqesVrFEpsQ95EVao5CX1ZbL8PpKuaJShXFNerzCckEVXpY8eVfUVlfXLsUjyEBNGd6KLN7SUoz3WC5TFillFTKlTFEmix+ZRxCSpKnA61eqVCN9K4R4'
        b'9PPjMI2Ki7NrFbLiYkHIFNkKTeVTAIREBL3H807BLdUyuXpFSVU1GTFCv8cDMmoV6lqFpqZGpiT9uFYqUz6Jl4os8nhAaUl1CcaoqLZOpoint44HKSpKMDFUJdXltUJL'
        b'4inwQjXMOsmyMnkNZgPGlmxwtLtMoyQ7W/54pXx0uEqpUTwaQZ6Y4ukSw2rKqnCXCn/S1DyJRVl1rUo2ikaKovx/AYXS2tpFsvIRHJ7iTx6WIbVMQeMkqJSV4hnU/7O4'
        b'KWrV/wRqS2qVlViXlIv+h7BTaWqKypSycrla9SLcZhNZE0zXqFVlVUp5BUZTEMFYBkGtonr5vw3HEUWQK2gJJgoiGEFVphhFk34F+i+wnCKrLlGpaZD/HSSfdFXxj0zl'
        b'kzbvkQ7X1arUBGiEQzJVmVJeR4b9Z9aF0F8mL30CG2IV1SWjjM3HVhFPWV39BHefY//Tcz4tCv8UjZQybH2xoMYLsKbh3lnoWtmiUmai0TFEB/EGihbJniDl6GJ4G9Xo'
        b'mkolq352uBob/f9k8yOwZMRjRJ6z2hkaRblM8dgCj0yPbe4LbPzTC+Axz8JVLnnadk8nHECHK9QqrKEV2GmR7tHBdUpMLKzfJS+ef8ZIt0whzlaGP4nZU2s8h9NjXzHC'
        b'nGf8xVMAT/kOZrwcL/HiwWlTkrKfZnlRrVJeKVcQ1j6vXzkjfaW0MGAFEExTymrKlz6lH/+EAP3TilZVgq3gC1V9uqwUXcOqoPi3L0rEi5ZZot9PrZmLe54XXEVJjeyx'
        b'lo/EIIKQbNz8SC40yjraJz43Kk+mXCpTlBOxXrFUVrZoFEIlqyuJfzKIwUBPREcjo+YpFAviBVLFIkXtUsXjqKb8yRiqpLwcNyyVq6tIECRXkmhCppSXCeTlJFKKx2fG'
        b'khpiFvB6uVXPJPaFW8aPxHzxgqQXWrJwy6eu8G3As1f4WUzSUXEoe8U/KLpmNSZgGXP3/XoyxxWw7cgdZNjZiMmAvqZFJ2C3D+xhkVTHONsJU7PooYvyeHYBlCt9TW6Y'
        b'Ox3Ql3dzfVGzBB50iyYn/V2gjJup8cVVCTyN9oqE6ahZlJ0Jd6L14cwJXcQDvj5cd0Wc0EpDzgFwI1yrQk0R6WliuDkiPStDnI5a0OnFGdlcEIVaeKIUJZ2Gx4KdsFOE'
        b'+8fYkBGk2wHuY0M9PIp20Pe+8PpMt2furNkC2BznC0/Tt7slhZqMzOzHF9MLZpKr6Q1os8aTQPego2gXaiJZfSLUkpUuZgFzdJkFN6+uoxFFOrwemT8NNWdko7VoO2xB'
        b'WyNSUQsb+DhwkPYlCf08gOpRF7zxaCBsIS8mjRE1yRjjABF3IroIezXB5NoD7Sp8aphWxDwqZGdRQAivceEedB1uYibdixdseWI0HtcUkYZ2zcJjA4q5kx2Qnn5asA9O'
        b'EIWjFjxdeHoWagwT8oAH6uCMWwkPQR1aR5MSc6axbmRUWhbaHBYJe/A4F2dOZHE5/daDjsWOfcS7QzVPs44PT9EysjrwJUn14mgOuXQE5Wi3hqbjqqWY7ZhNqbDzGT5t'
        b'Sx+5uVyGNkrmqqO5gFz1V8G9ZozIbUJXJqPt+KgZCTyoyPFCeroYeBYefZartfBkHNovYFIaNo5Pfoqt6AZqx4x9SYzPWORICJvmwQ4JPFfHA1RmIGoA8MwU2EOjEgB3'
        b'hEjQ+vnwHH3RCxZZ1NJzUvDYBNQEL5Q9LQiw1V3IY/I09sIDJRJJHRtQGeicM6ZoItxN9wTCBnhKIkF6LqBmoYZZAJ6Ps2Eun3cF2kkkSgySU4yuAXgWXYlnbobXw21w'
        b'N4Y5h2HyYIMFgBfnoOPMw8ipAnhaAlttJBR5ngCL4N4FzPUzRqFLooZHJYSMh0B1bTqtoj8uG2OppAqIik6U2IqZlyw8dk+kCs+QQp6GzqasQYeYJESxffxe9mQA6ooz'
        b'm+euBEI2rUjeK7GMoZPwOqZ6C0NWc6RlwZ222TR5olzh1YxwcShhLzzDAbZ5bCwgV6qDImmcRUswOD6DcwGHQ7Ei4f5F8AbmBbEVKZGJo1TbV4upZhZLs6gSboGbRom2'
        b'Bl7HRIM9UtqMrGIvfKxzrRXPqNx0dGJk5uq0whHiZk3EtI2EBxjmH4kcN0pZdAzuxaSdgE5pAknXeXu04zk1xYbv4KiivowO0BvSwLN2EnRZ9YgHB2G7JojQtcU+68kZ'
        b'4Gbxsxo8BzXRLJiGml+SwAOLR9nFhlraqpTkhz2v1XvQ1RG1htvhLhp+ngaekxSivRKibvtBVR66oPEjKJxLKcxIE2eHYzUOGbkDBR5wE2cF3u4R2AO3MUk26+EmpBMl'
        b'SElGpDiNAyzMWHAL2jaWlgNeok3ISXYc1rziak4aDzBXKU1Qj5oeMdIHf94fvJhWSnQO9fAy4DZ0/lkJiS6gJQQbq9NVonRxhjg0m6RM21ayl8ETMthiSW/aSoQ2jjyg'
        b'jjyeYpKRZzqPTE4w2gq3zTGnNzfLF+v+E+NSMQ5PvrPOCWE4eQGdQVcYIwG3EB8SljJqe0LLuPAkPI62My6iGe2DZzLgYQvy8Pzo1RkvcZ6WNtiFDtUwD7PwDDo8+jg7'
        b'8jLbC5sZYvaORVefeiTcXw47ArEjEZI51hXASxmjhIGNWGDR5kxyLa7KyCDEiIa7eWnoNJumVARGeRPGJTUsPUfMA/yM1IUsjOMR1MhYt06HueQp8/E7JjqSyLYdh9Zh'
        b'XaUv3rfCJrMnnkexo7gMD0ZNoxFduRCdFYWIHz2S18CDbFvYjv0PcRUlrjOffs6Hh9IiWIA852OKHqDVavIUuJ+Po4DZALWZz0Zn0caRd9x81O40YlHOuacUo3rmabp+'
        b'/Hw+PIGOKXkYteM4HkC74pkoAXZUMAmVAPaiM2JPc1rySiws5m9nCejUgGLVJOYBFG1ZCveh7cmwHu3G7gBuBUXqNcz82zFml7CrvpoVySbsArWZBRopwSdyLI4iMlFL'
        b'2swZ8FzkbGx76YzxcHEI3n3oyHvtbKIiDTx0ICwvlWycJu3M1DDSiXUnQzoDtXAAvLnSHuviPn/6jbZwASfAHtDxUaYmYRqgXWjMKr+naYca1ozQLscCk4jehj5YAnti'
        b'iN+ZOQ/2YHNXirWR9OTBbdGkh8Lmzh4dxh6pCl3SkATJDLQN4MCiIQ214WBkB2xIRDuX4H9bsPc5HQvPcOG50lnqUnhhLDahzbw5qBN2MTJ5EJOsYXRStAe7ZHgGatFm'
        b'LCd0ulmRBEtZxLw4Wll5RaxQ2AXPMUqxzQvtf8aewwa0s9omn4mMTrjieAYdKH9W2SfABno7XiTPcnSnLvAs3qlTOh1H5MejCy8KR4LgMXhIjNcntBzPT3oyGIFbc0aC'
        b'EUyBI0IOkwfQjc7nSGIXYwOfDveik2RzOP5ihGIv1qHDkkVodwyPjkVkuegq09O4DDVIYpZgkkzGaoGd7nFXRpCC7NFGjDHSY2efJw3DQhyEGoUU46iPW7JxXxTumpYN'
        b'sRDviw3WTCFxdRLS83Fw2oT53hSBts5GemvYPVscEzUjdVT2ZonzZj0rT8RyWqI9IbCDSRc+4YttEkZ1FYCXVq4SwZvMFtvRARzYxMJuFmCNQZvDSRB+xZ5BqRvPcQie'
        b'xM7jJSBCDS9hlae/G4Et8Y1EFZ3gPivEDx4kb2HEUuY/hUC+2AzuhNvUmgTGBu6FDfzsLNQizkNtWKEYTUGN+anp0tRcelMx8PgM1JAlDs/OzOGSbBy9JdyohOtGtN9K'
        b'/BKT7wzgZvfw5XAtLWOpcFcl2u4G18LTXLIfAE+ivVEYhLZkx3PQsWekzMGhGu6exwjhKVlURojzsyKGjVI7Pbc1aqgmSQUX6aSCS9SkyhjYFEzz0iEQrlehi3W2PNzT'
        b'SEF9QpDfGDrhR/5m7HGgcsYu84uLFqfzPlZ4pDhNmjDh779eavzra4oPbi/p7N9w/mKHw6bPPuJavkq9WTDU05T32cFzdaKAYmmutH+zR2vvn08IPjk8biJoMLu7zuWu'
        b'W+9n79z/LuevH3cJSv/83TvjKm/+KKl877u//rD17u0adt7vvF9/SbluO0nwM+8f/JhVxuMDxZ3jxeyfP7jcT+XHf2VWemC17tM9fwad1hdi++/cUB+pOfqnAxrHlPyW'
        b'zHzeRNVne++Az7olJ78/6KY3+7VMdfHdobxtsW/1vf/6F2+iravefre04uu2m68/2GW/IsfzvdjltcV57danzt/iTrj51nfuUdb8kp8GzM6vCPzUtembs+WS12N7wCe7'
        b'tZ/mv9T0TcQGF9fgcfqv5467EHxmp2tWlP6XghBb/fn39xXP+THB/2/Fv7EX7y+7sfHdsS1rpv8c/3lsyqruQ9fOClJ/isn9osBr36zf4hdt+Ejvd2uwNGvtWLcvee8/'
        b'zHzvq2nvZC/40y+tw9OsburuT9hQ+5qy+8h9RxgRHe726Uc/+97b7TQptmI/ez672u+ORH8kIVrvtTz5Z5uzSwr+du5O2S+Wb098++2wh3O89WHdYT2rdv7Z921R2NnQ'
        b'QbOfkOL9a4t+Hn/uTt7guaaT/+F0e2nBPOv6/nlvtitOdi4p03z5Zd30lGbnxERx/6mdjYdqEr9PuPfxN8c/9l2Vf++T93tP9s/MfX2KNOAt8/aI1lfHi5bl3FnH+e7k'
        b'3vtNnxh3t5Rkb1b4li8/EfrasWW/bXv4boZqxqaCqs8v6P7y8bYvf3OZGPpamqoxo8RMHjx90Wa9S/+P93xO/Ho9EaW/X7Lp/e1DR/yPf7lyxUuHD154++S1ZQkT24Ik'
        b'w2/+/X3D1+cmddzJcpiQGv4XgfGr3D+fXeyZL0+Z8eqalLK3Ns7+FnhfrRjn8eFbq/3vvkq9vb13c65H3juvPSz/XDOp7WHjJfnZwFdU6z/p/2V4oJP34Xd7FqT1O1K1'
        b'BTffXHFvQd/eoDlfhXzxxmce9z9ZP/XjIoWyIvqOi+L4tex5Me73q5o+qlXlvhJ92vDdu3V5n313/c+rlWG7ftj906umzlVjblJfPpz1feel3d93ztmvWWRxZekuzVc/'
        b'5X68NG9ZlmZ/1j6jh/2Y3FtX35b2ff1xQa7Dp5+blv7xHwvG3Pn1i1c/nfmPl7sP//pDacqsNU5NZxL+I2HsyVd3fr2m9OOWHvVMq/1tX146NRiXYfwks+B69rdXrrx3'
        b'o+Qfmq8cXpXHdex4/af+K55ff9/u3mmTdvKDw9JL8PqefU2Fr7npf1vYn/ZA/PaCgHL3h5wPlzjnoKvDiybmOid8Y5/v/Gl+3Br+3uEh58Kr3BmHF7i//Wbtndo9Ed/Z'
        b'ZA2zNyq/P/BVajPnP4Ku3r7u3b6V8+kJ5Q8uS9tTXpfrFSts22ZqmiXbM+dyQ27+fux7oWm918/LRAU9xXnSXuNfAoa2rFoG/Hu4ts2/HfsDJOxyEiz5UmjDZBG8PH/N'
        b'SHYCtpnEak6FDTgWc4EXOal1SEsnOKiXofMip7DQcCF2UQBYzGHhGK0JnXhAe8hW23mP8yMKcIDTCACdH7F5ygPattenwqNkjflyOgeCzn+Ykkj35cxPyoDnxoaFpD7O'
        b'fYC9y5jMiRu57iQx44msjMpUfLgVot1MYoa2Eu4mCRCrax+nQDDpD8tt6dyKKHt4XITOwu7srLB0tAXg+S+zlqLmwAfEdFI1czJwdGqLuiLE+BiwlBVejdrpb0+FoaYF'
        b'GRihRxkftpFsb3i4cnouPS08gbd/nUQU+Uj7KKRAe8PpLdVgz7VWhEl1LJqmFg+eYkn4s2hIEQ9uG/0+C/1tFngmgIX2ukfTG3IKjkQ95PgIT9cRr7ZiHo6qnCdy2LAD'
        b'6oSC/++sjf/mQkXkSfD8X/2Tf099P6dGPT4mUkmeiekEkW95zPdzFDzg5Lo7sS3R6BjQkGxydmmYZnJybUgxuXk1pJvGuDRMv+Pq2coZdPTSlutSBhxDDY6hgx7BXRyj'
        b'h7g12eTisXtl28rtq1s5JndfXVK7qNXsExePQSdPk6MLmVUnGXAM/sAx2BQUemzhgYV6R32JMSiuLac1SSu76+Kp42xf/YmHYNAzvEujLzREJN/2TDF5+u3Pas/qCrzt'
        b'GXk3IsYkFJtCwkzBIjyFKSzSJI4yhUeTUhRhCg03hYXfd7P2dd/DHfYE7j66gA4vkzhau8joGmpy86Y/enjrAjsmmqZMf110S/RGmXHKLINnojZFF2rwFONV5xgjEvEy'
        b'OiHJB8EgYqMbnjhCW9Vhiz/2+6Ub3dLvBUXpA3tZvWx9aK+sL+ly1Rv+l2uNQdmmEHFXiZ7VxR8MIBuYqV/ctcIYEH/fjOPrruUOWwJPX1220SPaFDNeF270jCI5Iwqj'
        b'V4xpbLwuwugZPZpDEjuh3y/a6CkZ/Uy6DZ7Rv9Bb6PQaZo0RuJs8hV0xw2xcu+sZgCnprF/ca693NwZNHObixmEe8PLXJQ+bkbo58ArUlQ9bkLol8MLcGuaTug3wCsWT'
        b'2JK6HfASdSUP25O6A/AK6XIadiR1J+Al7iofdib1Mcw8LqTuyoxxI3V3Zk4PUvcEXkE69bAXqXszOPiQugB4hXeph31J3Y8Z40/qAUw9kNSDQGCwKVhoCg37QYQ/aznD'
        b'4YRk9u1xTOLIgIfY4CEeFI3Vy3qTekv0C/vGvmH/RnTfBENstlGUo00meTqmgKD2lLuiCL358UmjLYHaFFNY1PHM3qmGsEQtRzvX4Bpi8vbvSjcEjxsITuhNGgie0mdv'
        b'8J6qZWPC+QZ1Te0XROozDIJELdfkE9C+YsAnyuATNeAjMfhI7voFdlEHgrVTSUpSuY6Ph3j7aNl4vvaFA96RBu/IAe9og3e0Xta9sG+qMXa6aRRgmA3wZI8HGUcHfRg7'
        b'/W6I+Cz/OF+f0p3eRxlDprRba3mDwhh9nlE4FWNc0G5jCpfok/QlXQvxxwUGV9Hd2AmYClP08oHYNENs2hsBxtic+2zKLUbrpF1kcAvtmmryFPT7RmHJMbl6aRUGV/GA'
        b'a4zBNUaf+6Fr/CN1COxywro76Bc9DKiYNMqUMQtPEjOb+hFQ/rkUbvTKpe6OwHeVGlyj9GEG18QB12kG12l9mg9ds8hM4Ua3yLue3vvT2tP6gyb3BRo9U7XUvcCQLvuz'
        b'Lsdd9PYn3Q8VmUKEZ82Om+mpk5aDWIF8LwV3B/f69hAV0lxWGIOyntKTlI5JJMFL/AHW+uhxurAPPCNo/UswuiXcdfUki4YY3UJx9Z53OMYyMt6UMKV/YiZGPjKLIO+T'
        b'TZB3y6bu+gZtT//SzZsYpzVta3SqAReRwUWkd7rk1e3VqxmISjFEpbzh9L7Xm179+XMH0uYZ0uZ95ir4xMVr0Du8P2LaGy6GiBlG75n9rjMH3UP7RZlG96x+pyyS3zTP'
        b'6Bwy6BSk03QVGoIn3nZKMDkxX24MvO0UgqnfmmLyDdyeftdDoPMe8Ih8bj6SyeZt8IjUOxg8Yoj59NXlGl2EJB8usT2xSzLgEWHwiNAnX0rvTu9V9eT0lRhjppsCQo6l'
        b'H0jvUh3KGQiYYAiY0Jvc528MmDYQkGkIyHxjtjFgpjZlMDC0K+p4GclP6/X9KHCijhrmcHwzKVP0uF6qO6Q3pc+3r+RW4OXMrkCsoZYgKlZf0kvpLQfDx/cG9lF9rF6h'
        b'MTz5Ppct9NNxsQEJCOmKPTTJNGlqvzDeGDDBFCjsyjtSiC1Vl9uhHOxBgxKwhuNB1gP+sabYOB1Ht8AgkJDsMy+jZ4Q+xuA57iPCQX+d2ugmIqll8w2uoQOuUUSgAgZc'
        b'x917ljb3Z3KBm9ffc7nAznnQzk83tsvb4B932268yW7Mbus2a63stl3AXUe3hqyfH0SBkOgfAQvvbzB0nCEu1RSS2BdsCEn7kU2NzyDCIMokwhCISzYZ9avKCju9D0Ks'
        b'pY6cDx09pRFmTKaZ3RCHvIX9Exlm/7RjJmlsxS9yxLTvpYttZNwkwGSklXAoyuEhwAVJS3P4V9PS9vLE4DQ/jv3Uu9xoFtqPJMDaCeaTHyIBStZsSsmezVJyZrOV3EqO'
        b'RZWQO2RHPwDSyWHKFKWyVinfioF/9WHeBenIQTmSCCYrF5QoBDIyKJymXraQN2ReVEReRIuKhiyLipjfEcF1q6KixZqS6pEe26KiCrlSpa6WK2SKWtxgVlRUXluGK85F'
        b'RSSLTF5WVKJWK+WlGrVMVVRET86kA9J0ixstCGoq8t2ll8EXVlH0CPqW1xLtgZv5NuiSmm+BQ9Rsb7FYOfJV/Ai0n8eFPSIhNU1ewd3JVsnxHCGpzbK2gWw02S6l8uPP'
        b'HhSat06LsKE6J7Nk8ywObPhh1fWctubWkFkBP75lO8z/LaJMZCP4+71TlV990vblih2qjSd7T5y8fGXRKkPcXP9go9/r31la2rxyd/3Xy6f8uDQk/mb4lYX9f1186Tfj'
        b'xr/P+3ypbpNUd9Y+66ux/9gvL5jvV/rLp0cDWSmRhoeTXh08+XJh8tSBpi5x0PKjzW82vzMY+pl0T/u+l83c2qLmJcGzldA4YUPArK0sebl2zhfa5U7alB1aWa42oyt6'
        b'dzecn9IyZ/r6weSmyy9rvuTFts8zVfytePflTauPboz9EXh5fmb+ut6QYhscl+LD7rznObV56JvGYaf5xc0Z8+9dOb38RO7htzwOl3/00WLH6uK45cHvWezu5NRGfcMX'
        b'FrS1puUdWZ6f9ZcPWrlzdjhPaJz3qXFvpdMn33/xheiVPz47k967373k5QU/nX3Psfb2Yd74nWOyfkr5oDvym/2vbFq4tzDlwY8e+2pmFb+OhBw6sRq1pqPtqCmTAlRc'
        b'MOoEaAvaBG/SB5oaCWwe+fGE4vwRntE/ngB3rnpAbubjCuBhfigO/MmZ49EvLPjAHrgri4POotMS5mjVscxOBU+nZqNL8Jr40fuEPWplQz0fbhK6MSpq/l8W/33hOjmQ'
        b'CCbTf/XP/TFxOlal6tqSciz/yaNBuhkuf8dBehiwdh7mmFm4DNo6tEY3LdX6Nq1qV+midSUHxnas6JrZsaY7QK/s9e3W9M7sXtYTfiv5DQeUaozOvOPqro3WlrSP7bDQ'
        b'pRtcw/UuBte4/onZBpfs/lm5/dI8w6x8o0v+nTECncN2Rb9dAI5YXAso7B8cnFqT2pwbpjzk8CxCHtpxLPyGASmszAWWJivb1jHDbFJz89RWMLUgYVcsU5PE9vKY2uSp'
        b'fXl07S4NwSU1GoKu0RB0jYagazQEqeGwzNoOw5gxdXcvDDVSDw7FcCP1mHEYcqSeRCVTGJr+ZM5AWzB1GnqkHhbdy+vLM9m7aCu6Yl9U/cEWD+w398QRr4MrbmH+u8/n'
        b'+eFW74d2mZRFPnUf0P8MF7KApd2ghV2rSju2dZHBwu8haxnbwv0hIOUwXf7IBpb+pLAb5tCtS8xw/QGLsojuXI5dlUU03XmfNPw8LONTFmnUoIPPYat+8TSjYLrRIbXf'
        b'KpVxYJuTPJOtwCtWjsk+bMaBOQ2xsMD8+9zXC4XX6QUu7bFbSx4tiKqrEkbcmpCi7IhXs/s7Kf5Vr3aQFw3O8RPY8p27qriql3DLjFdKZS0JNusmuybfTJz8Xb2l+ZWN'
        b'0YPT+z9iT349euebu8YEvF3TezbKw9Hx6PLZ196ZGLF2Pcf64vbKHMcazp6dNssHzybERf3loGpxzPXfLm/7+sa38YPalCXfCLfyXhZM3eJQmdtlmGw4ONUW1YvuXP/h'
        b'I8OKzefeaHnroRnqcDyxeIPQ7AH5latMEdpP/5pTDnllyzAD6MgUPjzHQl3oAmymh0yDR1B7Ro4YboQHUDcZmiNmYTt0jQ0PeDsxtmob6oGHYBN5jEQtHuRFDbbArWbA'
        b'xoHtjXZyHhBOsn3TR76LwuOgxqksc9dw5gboINqFjmY88StRKtjAF7JQa+GqB+SxDfbCG/Dokz8jhVdqpn9HCh6AF+jbGHQa22OtKJ0LKNgcmAGQFl30E/r/5ybyf/2+'
        b'44Vy6T9qVJ83qS80r3KFXI21JWvUvE7HxW/1JEriOpqsnQasvQ3W3p3LjNYh9dNMHMtNmWsz++19D8fd5oR9zPH5E8f6IW8llxv9EJDyJ7ocXsEHVk71OU98e0EwxK6W'
        b'KYY4JK9+iKvW1FXLhjgkmQrHmvIyXJK87SG2Sq0c4pYuxxHPEIekVQ6x5Qr1EJf+GZUhrrJEUYmh5Yo6jXqIXValHGLXKsuHeBXyarUMf6gpqRtir5DXDXFLVGVy+RC7'
        b'SrYMD8HTW8pVcgWOqhRlsiFenaa0Wl42ZFZSViarU6uGrOgFo5mEtCFr5mZIrqqNi42MGuKrquQV6iI6whuy1ijKqkpwxFZeJFtWNmSBIzUcBdbhoI2nUWhUsvLHRoe+'
        b'iyr+L/8EAsZWZI0W5He4VDm4+OOPP/6BzYUthWNTYi+eLn+gy3/FehAzecuSl+QObrnzkwLZv5qP/nzSkB2JQ+n6iKP91b3i6R/EEyhq1QLSJyvPFporSYhOgtWS6uoR'
        b'sVHGkyZLTF6lWkWy7IZ41bVlJdWYsrM0CrW8RkYH0cqaUWl4HMYOmU9k4uNJShVgQnRVJi6G2RRF3WdxKM6wFeBb15v9wEnnUU7Dc62Ahf2AuYfB3EObPmAebDAP7g+b'
        b'dCsIhRjD0k3mdoOWY/pdJEbLmH5OzCCwa3X9ELjTq/0f9PJfOA=='
    ))))
