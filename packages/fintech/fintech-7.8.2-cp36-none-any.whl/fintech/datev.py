
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
DATEV module of the Python Fintech package.

This module defines functions and classes
to create DATEV data exchange files.
"""

__all__ = ['DatevCSV', 'DatevKNE']

class DatevCSV:
    """DatevCSV format class"""

    def __init__(self, adviser_id, client_id, account_length=4, currency='EUR', initials=None, version=510, first_month=1):
        """
        Initializes the DatevCSV instance.

        :param adviser_id: DATEV number of the accountant
            (Beraternummer). A numeric value up to 7 digits.
        :param client_id: DATEV number of the client
            (Mandantennummer). A numeric value up to 5 digits.
        :param account_length: Length of G/L account numbers
            (Sachkonten). Therefore subledger account numbers
            (Personenkonten) are one digit longer. It must be
            a value between 4 (default) and 8.
        :param currency: Currency code (Währungskennzeichen)
        :param initials: Initials of the creator (Namenskürzel)
        :param version: Version of DATEV format (eg. 510, 710)
        :param first_month: First month of financial year (*new in v6.4.1*).
        """
        ...

    @property
    def adviser_id(self):
        """DATEV adviser number (read-only)"""
        ...

    @property
    def client_id(self):
        """DATEV client number (read-only)"""
        ...

    @property
    def account_length(self):
        """Length of G/L account numbers (read-only)"""
        ...

    @property
    def currency(self):
        """Base currency (read-only)"""
        ...

    @property
    def initials(self):
        """Initials of the creator (read-only)"""
        ...

    @property
    def version(self):
        """Version of DATEV format (read-only)"""
        ...

    @property
    def first_month(self):
        """First month of financial year (read-only)"""
        ...

    def add_entity(self, account, name, street=None, postcode=None, city=None, country=None, vat_id=None, customer_id=None, tag=None, other=None):
        """
        Adds a new debtor or creditor entity.

        There are a huge number of possible fields to set. Only
        the most important fields can be set directly by the
        available parameters. Additional fields must be set
        by using the parameter *other*.

        Fields that can be set directly
        (targeted DATEV field names in square brackets):

        :param account: Account number [Konto]
        :param name: Name [Name (Adressatentyp keine Angabe)]
        :param street: Street [Straße]
        :param postcode: Postal code [Postleitzahl]
        :param city: City [Ort]
        :param country: Country code, ISO-3166 [Land]
        :param vat_id: VAT-ID [EU-Land]+[EU-USt-IdNr.]
        :param customer_id: Customer ID [Kundennummer]
        :param tag: Short description of the dataset. Also used
            in the final file name. Defaults to "Stammdaten".
        :param other: An optional dictionary with extra fields.
            Note that the method arguments take precedence over
            the field values in this dictionary. For possible
            field names and type declarations see
            `DATEV documentation <https://www.datev.de/dnlexom/client/app/index.html#/document/1003221/D18014404834105739>`_.
        """
        ...

    def add_accounting(self, debitaccount, creditaccount, amount, date, reference=None, postingtext=None, vat_id=None, tag=None, other=None):
        """
        Adds a new accounting record.

        Each record is added to a DATEV data file, grouped by a
        combination of *tag* name and the corresponding financial
        year.

        There are a huge number of possible fields to set. Only
        the most important fields can be set directly by the
        available parameters. Additional fields must be set
        by using the parameter *other*.

        Fields that can be set directly
        (targeted DATEV field names in square brackets):

        :param debitaccount: The debit account [Konto]
        :param creditaccount: The credit account
            [Gegenkonto (ohne BU-Schlüssel)]
        :param amount: The posting amount with not more than
            two decimals.
            [Umsatz (ohne Soll/Haben-Kz)]+[Soll/Haben-Kennzeichen]
        :param date: The booking date. Must be a date object or
            an ISO8601 formatted string [Belegdatum]
        :param reference: Usually the invoice number [Belegfeld 1]
        :param postingtext: The posting text [Buchungstext]
        :param vat_id: The VAT-ID [EU-Land u. USt-IdNr.]
        :param tag: Short description of the dataset. Also used
            in the final file name. Defaults to "Bewegungsdaten".
        :param other: An optional dictionary with extra fields.
            Note that the method arguments take precedence over
            the field values in this dictionary. For possible
            field names and type declarations see
            `DATEV documentation <https://www.datev.de/dnlexom/client/app/index.html#/document/1003221/D36028803343536651>`_.
    
        """
        ...

    def as_dict(self):
        """
        Generates the DATEV files and returns them as a dictionary.

        The keys represent the file names and the values the
        corresponding file data as bytes.
        """
        ...

    def save(self, path):
        """
        Generates and saves all DATEV files.

        :param path: If *path* ends with the extension *.zip*, all files are
            stored in this archive. Otherwise the files are saved in a folder.
        """
        ...


class DatevKNE:
    """
    The DatevKNE class (Postversanddateien)

    *This format is obsolete and not longer accepted by DATEV*.
    """

    def __init__(self, adviserid, advisername, clientid, dfv='', kne=4, mediumid=1, password=''):
        """
        Initializes the DatevKNE instance.

        :param adviserid: DATEV number of the accountant (Beraternummer).
            A numeric value up to 7 digits.
        :param advisername: DATEV name of the accountant (Beratername).
            An alpha-numeric value up to 9 characters.
        :param clientid: DATEV number of the client (Mandantennummer).
            A numeric value up to 5 digits.
        :param dfv: The DFV label (DFV-Kennzeichen). Usually the initials
            of the client name (2 characters).
        :param kne: Length of G/L account numbers (Sachkonten). Therefore
            subledger account numbers (Personenkonten) are one digit longer.
            It must be a value between 4 (default) and 8.
        :param mediumid: The medium id up to 3 digits.
        :param password: The password registered at DATEV, usually unused.
        """
        ...

    @property
    def adviserid(self):
        """Datev adviser number (read-only)"""
        ...

    @property
    def advisername(self):
        """Datev adviser name (read-only)"""
        ...

    @property
    def clientid(self):
        """Datev client number (read-only)"""
        ...

    @property
    def dfv(self):
        """Datev DFV label (read-only)"""
        ...

    @property
    def kne(self):
        """Length of accounting numbers (read-only)"""
        ...

    @property
    def mediumid(self):
        """Data medium id (read-only)"""
        ...

    @property
    def password(self):
        """Datev password (read-only)"""
        ...

    def add(self, inputinfo='', accountingno=None, **data):
        """
        Adds a new accounting entry.

        Each entry is added to a DATEV data file, grouped by a combination
        of *inputinfo*, *accountingno*, year of booking date and entry type.

        :param inputinfo: Some information string about the passed entry.
            For each different value of *inputinfo* a new file is generated.
            It can be an alpha-numeric value up to 16 characters (optional).
        :param accountingno: The accounting number (Abrechnungsnummer) this
            entry is assigned to. For accounting records it can be an integer
            between 1 and 69 (default is 1), for debtor and creditor core
            data it is set to 189.

        Fields for accounting entries:

        :param debitaccount: The debit account (Sollkonto) **mandatory**
        :param creditaccount: The credit account (Gegen-/Habenkonto) **mandatory**
        :param amount: The posting amount **mandatory**
        :param date: The booking date. Must be a date object or an
            ISO8601 formatted string. **mandatory**
        :param voucherfield1: Usually the invoice number (Belegfeld1) [12]
        :param voucherfield2: The due date in form of DDMMYY or the
            payment term id, mostly unused (Belegfeld2) [12]
        :param postingtext: The posting text. Usually the debtor/creditor
            name (Buchungstext) [30]
        :param accountingkey: DATEV accounting key consisting of
            adjustment key and tax key.
    
            Adjustment keys (Berichtigungsschlüssel):
    
            - 1: Steuerschlüssel bei Buchungen mit EU-Tatbestand
            - 2: Generalumkehr
            - 3: Generalumkehr bei aufzuteilender Vorsteuer
            - 4: Aufhebung der Automatik
            - 5: Individueller Umsatzsteuerschlüssel
            - 6: Generalumkehr bei Buchungen mit EU-Tatbestand
            - 7: Generalumkehr bei individuellem Umsatzsteuerschlüssel
            - 8: Generalumkehr bei Aufhebung der Automatik
            - 9: Aufzuteilende Vorsteuer
    
            Tax keys (Steuerschlüssel):
    
            - 1: Umsatzsteuerfrei (mit Vorsteuerabzug)
            - 2: Umsatzsteuer 7%
            - 3: Umsatzsteuer 19%
            - 4: n/a
            - 5: Umsatzsteuer 16%
            - 6: n/a
            - 7: Vorsteuer 16%
            - 8: Vorsteuer 7%
            - 9: Vorsteuer 19%

        :param discount: Discount for early payment (Skonto)
        :param costcenter1: Cost center 1 (Kostenstelle 1) [8]
        :param costcenter2: Cost center 2 (Kostenstelle 2) [8]
        :param vatid: The VAT-ID (USt-ID) [15]
        :param eutaxrate: The EU tax rate (EU-Steuersatz)
        :param currency: Currency, default is EUR (Währung) [4]
        :param exchangerate: Currency exchange rate (Währungskurs)

        Fields for debtor and creditor core data:

        :param account: Account number **mandatory**
        :param name1: Name1 [20] **mandatory**
        :param name2: Name2 [20]
        :param customerid: The customer id [15]
        :param title: Title [1]

            - 1: Herrn/Frau/Frl./Firma
            - 2: Herrn
            - 3: Frau
            - 4: Frl.
            - 5: Firma
            - 6: Eheleute
            - 7: Herrn und Frau

        :param street: Street [36]
        :param postbox: Post office box [10]
        :param postcode: Postal code [10]
        :param city: City [30]
        :param country: Country code, ISO-3166 [2]
        :param phone: Phone [20]
        :param fax: Fax [20]
        :param email: Email [60]
        :param vatid: VAT-ID [15]
        :param bankname: Bank name [27]
        :param bankaccount: Bank account number [10]
        :param bankcode: Bank code [8]
        :param iban: IBAN [34]
        :param bic: BIC [11]
        """
        ...

    def as_dict(self):
        """
        Generates the DATEV files and returns them as a dictionary.

        The keys represent the file names and the values the
        corresponding file data as bytes.
        """
        ...

    def save(self, path):
        """
        Generates and saves all DATEV files.

        :param path: If *path* ends with the extension *.zip*, all files are
            stored in this archive. Otherwise the files are saved in a folder.
        """
        ...



from typing import TYPE_CHECKING
if not TYPE_CHECKING:
    import marshal, zlib, base64
    exec(marshal.loads(zlib.decompress(base64.b64decode(
        b'eJzsvQdUW1e2MHzvVUF0jHEBN7kjQKIXA264AaIaXIILCCRARghQAYO7sQ2mGnfcey/Y2I7tuEzOyUzqJPMm00KS95JMMokTTzJJpmQyL5Nvn3MlIRmJOFmz/vX9a32U'
        b'K51e9j67nX3O/SNj98PB/yz4NybDQ80UMGVMAatm1dwWpoDTCFYJ1YJGtmqCWqgRNTIVYqNiGacRq0WN7GZW46bhGlmWUYvzGPdymdu36zzmzs6ft1haWaU26zTSqlKp'
        b'qVwjzak3lVfppfO1epOmpFxarSqpUJVpFB4e+eVaozWvWlOq1WuM0lKzvsSkrdIbpSq9WlqiUxmNGqOHqUpaYtCoTBop34BaZVJJNatLylX6Mo20VKvTGBUeJaMtQxoH'
        b'/2Pg35MMSw2PJqaJbeKaBE3CJlGTuMmtSdLk3uTR5Nnk1eTd5NPk2+TXNKTJv2loU0DTsKbhTSOaRjYFNgU1jWoaXTqGToVk3ZhmppFZN7ZBvHZMI5PHrB3byLDM+jHr'
        b'xy6FSYPhl8kEWSX2cxoE/0NJB4R0XvMYmWeWTgLf35oiYG6I3eFbUcbrbgGMeQJ8DRk5Crfi7dkZubgZt2fL8IEK3J62KEcuZqbOE+KHwaUy1kyqRBfxqZXGtEzcgdvm'
        b'JGXiNpbxSONQT+VCGWcOgAwxk9cp08LSRIxQyKbgy+go6k01k5lZj0/iyyRJju4k4+24LVPE+OAWQdZ01Aplx0KWWhM+ilpxS1g1dGYTPoTboB4P1MuhG6tRN+1ohT86'
        b'AFmue6Hmuhoz7q3B+9Fxrxozy4zAnQLUFjsZOjqJdPQyOoM6UCvqDFfKQ0h3cSdqzR6KOt2YUZOEqBFdiS9hLRMmgP9R1gkrIhDj4cX8OIiVjrJAi20GZF3HAbRYCi2O'
        b'Qotdz1mgVWoPLdL46AHQGstD62ypG+O19gMxIy0KWyFcz9DIDWMEjDBigwhAqKuPGsJH7k+TMH7BNyGuKOMfRhEfOesZISMpCuCYWUVh64YKGJ0HRB7wChSOnvpoMsO8'
        b'P/Ur7lakTN7F6ghCXFzUzfa4MdKIQP209+I2lv2TodFFY77y3e3LBv+F2RC2Y8Qew4dMH2MOI3N8JrQQINUanhscjFvCU+W4BZ3PD07PhKk+qg9TpMnTM1lG7+s+fXyY'
        b'w1x7Woc7i59rx5XBkJku9bTNJTfoXG55EvNFA+bSK8tAEszD4YFP+U3NWyhfzDGcwIBbGXwYHcdHzf4kaQfuQC15kHUivlDITJzoxkc/uwBfzFvIMWvRYaacmRfgx0fv'
        b'x3uEeBcMJxy1VTHhwxZR/Medc/AevAtGK0cn0RlGHo+um0eQhCMFlXmZubhdxHBr0Cl8gh2NtuPb5qlkIvcl1sNEtoUqAU23Z+QGo/NhqXT1KfB5QHIR2oxb8AnzEMg7'
        b'TIOPo14xwyTnFjLJ6Nh07ZbADwXGo5B0Q7J5xRvj/VGE39b3383sm/JSy5HNE6VdCULxOz4nztWG+J0f3/zi9IQVGknjn3ImSfe/V/untzfUDvde/uHBpIdTXnnzgE/n'
        b'/ddijEWnd43a90r1psUxN84J8ILA+JBNaxafjEtfsHXJy8NmVIcleSamR62V/3bP73JbxmStb1qwJ/7fDZv++dc3TM/c+Ocj9W9UXa0dEwpXl9edevDsPw/K//nZKH/z'
        b'NEPlHpnIRBZZ5gTUpcTtobg9U55OKIU/vm1KEuCm4sU0Hd9DR1JD0+VAiTYtSsvIEjGe6BqHD+N9Cj69N+CZUIUsPdRCRHzxxqnoqKDKG92j6eiqdronmUAzrPuWcI4Z'
        b'gu/ONArQ5ZVuJkLC1qOz82CyW3AnboN1NA1fl7DoGj6Nb8u4Pi5YZiAYKvOkHz/+cZ75dnhyqaGqQaMHxkBZjgLYhaZ2Rp+3QaNXawyFBk1JlUFNMNIoJUg7Q8L6sxLW'
        b'A36Hw78P/JJPf/j04wJYg5jUTZBZJugT84X73AoLDWZ9YWGfZ2FhiU6j0purCwt/cqdlrMGNfCdLhzY3k3TOh3QOSzkxy7Fi+jSPJzHnUAtbnhGajtuVQMxbwmG9d4Sn'
        b's8xkdE1UiK4rbKuR/Agtn8ZyeGgIbwe+rmYLBPAv1DIFIvgUlzIFbmrvJqaUVQvUwi3uBRL6XaQWb5EUuNPvbmoJfPfgWWmpQO2u9oCwJ4SBeEDYU+0FYS81S0mCT594'
        b'IZ2orEf/hqVYIrD0ggzQw0ofIhgra4byPLERNAuA2AiB2AgosRFSYiNYL3RFbAQDiI2QJ9x/KxQxL82EhQ+U9501KYx2SDInMGZBykrRt58VvVb8SdFOdWl6s+rToray'
        b'S5pPIOaV4iuq8tIMVUDZOY3wy7yRq0Yu27RqY8j+qNmTlG5zujxztt0UnOvoGr91/P5N0QJmmdb39z3DZWITYR7oDmplQymn80ZdhNmFihlfdEbQMDyBXxVX0KHVoTZW'
        b'2DBNwHiFCdzQJXzRFEjJ0/LxSvzsetyaAZxfJmYkqIVbje4O41P3JqK7hEIp09BlhhEncPPR1kB8f7hpJKT6rYU125oNvF3IiPAhFt+bju9OwodMhO4NmZQCSx0dlKdS'
        b'sUCCb3BoS8EGGWeHfoInkVJoxcY+SWGhVq81FRbS9eJF5r3AjyW/YlbINvjyYFZYc/HrRNQnNGp0pX1CIqj1udVqDEaQ6QwELgZ3Ht8t7RIcN3iTh69tAZBGltkWwFk/'
        b'uwUwoL0Szg7PbZilsGBWKWfBK44yMQHgFUfxSkDxilsvcCYQMC7wyhwK36X4FLrsidsBGB3AeXFnXiqATIvuANRycyhjm4mPi4eUo2PaNVODWdqXyZ8++qyIoNhLpeH+'
        b'oaoM1eMiv5LyUl2x8KvSlkhNZB3z1vNehwKZQ19Kpq5eIhNSOonv4IdqpQM+4KuoZ7Ui3kTIQI5xDO4FEtyJOxXyagupDVovzMUX0VZ8Gx3g0a43Ae1Ee3GPA37chUFc'
        b'MpHx4cMTJimzE/BmOctwtezscfgYD0LOKTYAtSvTmLQmTaUFIQixYoo9WC+2wd8GGlsWviohBXCfUK+q1AzEAc4wxIYDFPx+8Cixgf+ojz34nbTxH6MtZU+NA3gfvls/'
        b'AAcsCDBqrRUFYNJPaf/5RoTIGAWFvgl6xzkOPC7iWqLMEX+oPBpxKkIYXX1GwFxeJSl8vU0moCCMAdZ43YIHuDXRShoAiNdNRNKeh54F9ukMFdA53A24cASdo2QCb4uD'
        b'rBY8mBLGYwJqm2zhba5pAEDdOBDqZU9A3egIdREPUgLcPlGtSmd2AnuBHeyH2hCASHflNgQ44OccAWzNOScBUTwCEMmWLRX+FDLAWqp0RAFRlpngFoD+Au4m6lQ+bpbL'
        b'Fbmp6Ytwc3YeLzmmghCpYBlTfCq+7y7Ge3GzOQQKrWUyn8QafB8fzHiCdKDbM7QNnm8zxmwo82LX558VfQqIoysNGR6iSlXpAGUu5XxaVK1q3nNBc071SdHrxa/+8bXS'
        b'8J3BqnTVBZVfCfPyiPQtjS909y5N3Lh2/raAbUXi12OY+hl+yfExIAMSTQ8fCEInbULaxqVWOQ2ktPn4FOUbCZGVDsRn/lxgR3tFlPaMRLufGYBxwfgMRbqtiUB7KAE7'
        b'ge+jgwThRqvsSE8vvkDR0QMfxftC+9nSKhkwpgD80IocQqfiUj9Wis3VRLDr50s6D4sU58c2eFvwhM9jT4d4ltOPik/iPRCkfqZE8ZGoFZU2fNzjb4+Pju04KFmOtIiq'
        b'szZaxDazgypVDrRI6BQRBVnamjoRL9JsHfahUpVa9hjQ5JXi8tIA1TnNuV9x1wN794d/fCBw+chiTfH+VYEV3bOuP/NabNsv226+FpsR6xX7WpzX1qj3vca0xc5aQflP'
        b'7AjfF45+buE/M4Jz7RAAd6HDlOycQIcp+JLxnVyA7bIV9mzlNmqh8so6vN8Lt4bhXQhoVjvoUeKV3ETUhPaYiA4onZJJZBm0M8UmzgSaC50DfDC6BEK40WSw0CQy3YzJ'
        b'jw0AqgR0yaefUJAsVhrn/QPAZ+3gPgweZhvc2x3o0BPVy7gsA1GqZd5EYCKMDlQDj8JC3roF370KC2vMKh2fwhNFSQlgTFmVob5PYhGQjFQI6hOXajU6tZHKQZQbUopI'
        b'0ZD2yUpfXaoUthkykEnJI0MghSWckLX8cj4SL5GXyE9CdfJ5qGVCka+nVY+QeHFFaOvEAbyQ/FBxxkGN4AqERPhXux3iCkS7GbVklVjt3sg2sqBSeFCR3btPPE8PxLr+'
        b'24C5mmKtqQr0sHClQaPmvz4iQ3xE+vyt/2KNocFcZqxWmY0l5SqdRhr9iIzjW68MjanBpJHON2iNJhlHlYpHvwC4/60b5kZZpTdVJWXB3EqDZ6sNGqMRZlZvqq+WLgIF'
        b'0KDXlFdq9LIku4CxTFMGT5NKr3ZaTq8y4XsGnUKaA5CpgrKLqwz6p8nnrLIKjVavkc7Wl6mKNbIkh7QkpdnQUKxp0GhLyvVmfVnSvEXyDNIp+FyUZ5KnqbMMiqTZepgs'
        b'TVI+8Dtd+OwKlVohXWBQqaEqjc5IuKCOtqs31lYZoOYGaxsGU1KeyaDCRzVJOVVGU6mqpJx+0Wm0pgZVuS4pG3LQ5mDejfDZYLYrbg0U15HeEdVZaukIRCmkBWYjNKyz'
        b'67w00mVKVJJSo9c3KKTKKgPUXV0FtekbVLQdjaU9jXQBvqczacuktVX6AXHFWmNSvkanKYW0FA0IkhWk3mBLlMyaJl2gAczBp0pNRjJKMqUDc0sXZMiS5skzVVqdfSof'
        b'I0tK4/HEZJ9mjZMlzVettk+AoCwpD9YudFJjn2CNkyWlqPQV1imHOSJBx1kjMRUEh+VZ5kqoAKIy8Cliq6ggs8ZPP0SmpczOImkajaEUKAR8zVuSNj9fPqcKYGOZfLoW'
        b'tPpywDVSj2XaU1XmapOctAOkplhhadPy3WHencWTuXcYRNSAQUQNHESUs0FE8YOI6h9ElP0gopwMIsrVIKLsOhvlYhBRrgcRPWAQ0QMHEe1sENH8IKL7BxFtP4hoJ4OI'
        b'djWIaLvORrsYRLTrQcQMGETMwEHEOBtEDD+ImP5BxNgPIsbJIGJcDSLGrrMxLgYR43oQsQMGETtwELHOBhHLDyK2fxCx9oOIdTKIWFeDiLXrbKyLQcQ6DKJ/IcJ6Mmg1'
        b'pSqePi4wmPHR0ipDJRBmpZmQOj0dA1BjDahB1kC1AQgyUD+9sdqgKSmvBnqth3igxSaDxkRyQHqxRmUohomC4FwtkRM0cp7dzTYbCUNpAFkhaQk+VW6AeTMaaQOE6vH8'
        b'Vaet1JqkwRa2K0sqgOkm+YohUV9G8oG4r9Npy4BHmaRavTRfBXzRrkAehQFJyaE2VfvK+lm4vAB6AQQjmBR3SLCUh6TJAwtEuS4Q5bRAtDTFYDZB8sByND3GdYUxTiuM'
        b'dV0glhbIVPF8mc45SCUgndA4k2a1yfYFKJHta7R9VqMtGw+IFA2w4zK7iMlJBVo9QIPAn7ZDkhogirBeoNIOwSjHIJAfldEE3M6gLTURrClVlUP/IZNerYLO6IsBbW0Q'
        b'NxnwqTJAojS9WlurkM7n+Yd9KMohFO0QinEIxTqE4hxC8Q6hBIfQNMfWIxyDjr2JdOxOpGN/Ih07FBnrREyRBi+0zKrRImjI+gUjZ4kWWclZklV8cpVmI2VO0rOdt0bk'
        b'LmfxDqKY6zEMku5KOvsxmaNct+wgpz1NNiCVzrI5sIC4ASwgbiALiHPGAuJ4FhDXT43j7FlAnBMWEOeKBcTZkfo4FywgzjUfix8wiPiBg4h3Noh4fhDx/YOItx9EvJNB'
        b'xLsaRLxdZ+NdDCLe9SASBgwiYeAgEpwNIoEfREL/IBLsB5HgZBAJrgaRYNfZBBeDSHA9iGkDBjFt4CCmORvENH4Q0/oHMc1+ENOcDGKaq0FMs+vsNBeDmOZ6EEAgB+gK'
        b'EU6UhQin2kKERV2IsBNTIhwUhghnGkOES5Uhwl43iHClNEQ4jMfSxfkGTaXaWA9UphLotrFKVwuSRFLevJzZcsqtTEaDphSYoJ7wPKfRUc6jo51HxziPjnUeHec8Ot55'
        b'dILz6GkuhhNBCHqFHt+rLjVpjNLsnOw8iwBHmLmxWgP6MC9M9jNzu1gr+7aLWqApxvcIp39CbCjj4y1SgzUU5RCKTsqxmFbsCg8wukQOjIoaGAVqjo4oxSoTkUuleWao'
        b'TlWpATaqMpmNRKzlRyOtVOnNwF6kZRoeTYEdOjMDyOyKaAlz16ppsR/M7KR+J0zJed0DM1ITU//sSEH4llpEXjqVpSTdMsn89yi770Qn7LdUfcsmZck4A3FIM0h52zIx'
        b'nxuIJ5VMYiC2NwOxtRuIQZXfCyHWUwMxv/aJjNU6rckwymbxY5+07pGN53VWAyW17gk4VsJxnDCSOovhlkj8LL6ZZSTeHtvD0HkhI4nj1rP47H/Qtucxu6Skyqw3gT7R'
        b'55MCSMDrIapqje4RsVY+Ip4N3wbNBaSoBEmDGE2lvB4EKK0FQvSIWGL7hEQecrDs3YP4RZW8lFNVrtdI86p0uvBUIFN6ubKBGF36g/2EL2mJskDKFyPGNUJSjVqjmY8g'
        b'afZhfiEuILZAXujnG0pZJM8rKdfhe4AQOhBU7INJKRqdpkxNRsN/tVhi+r9HWZSmJOtkUCWASIkay3q3anJSXlKy6IP9liuLJkjld6IDQmZYcSaqK1hqoM3ptJCBftPq'
        b'S6ukculsg8naFUtMmp6UfCKSZItyli1qQLZoZ9miB2SLcZYtZkC2WGfZYgdki3OWLW5Atnhn2eIHZEtwlg0Ej+y8/EiIUPKAIQKwhkZGDYiEgDRTA0TUap6VmhXSfvMs'
        b'RPIIbbWXKqREiLeq4rwdth+M0ozQjKT5Zn0F9XPVGMqAajUQSkPiUxZJY6bxvLfUmoXYiZ3FW/CGT3JSYVIB1RHIwA2VKpJoQxFnKTZUcVUsarBizhN5FBqkmPNEHqUG'
        b'KeY8kUexQYo5T+RRbpBizhN5FBykmPNEHiUHKeY8kRSbNlgx54kU3BGDwtt5Ki04OKK4xpTIQVHFRSotOCiyuEilBQdFFxeptOCgCOMilRYcFGVcpNKCgyKNi1RacFC0'
        b'cZFKCw6KOC5S6YofFHMgNc+E75VUAOuqA+ZrotJqnUZr1CTNBz7fT/2AHKr0OhUxOBpXqcoNUGuZBnLoNURS6rdAWjgnIXizzaXEVmYjclZeCkmE8vYzZGnwbH0DLyWT'
        b'TT4gxplaE7BGjRqEEJXpieQn6PDAwv2U/Mk0gw7fMlrEBIeUVLrlU2oCqcSma1FOIqdCj1PFwDJSCzcH1g+chsjVpVSiriQM3qTRwrSYbMbjNBB/TdpSbYXKnvoXUN3Q'
        b'ZlS2FzN4jdJuc9FeTJqv4dUNjbaYJGUA1MhumZGXbFxLa/YGY+g3tKzSmSsrNOVW6zZlgoRJGqaAXEfEX+IyZQjjxV85+a54CvHXQPyyBxN+g+Fxz6nwG2gmAjfaizfN'
        b'M2Zk4Y4VeF84lYBxm9KNGVYs9MKnJjhIwEOtEvAq1lEC3i3e7bnbUx2ze+juoepYdZzar91NHd8kavJuGloqUA9VB2wBebhAqBGph6mHb2HUI9Qj27kCMYQDaTiIht0g'
        b'PIqGR9OwBMJjaHgsDbtDeBwNS2nYA8LjaXgCDXtCeCINT6JhL9KDUk49WT1li6TAm/Zy6BO/7uqp7R7qhCbO0luhOlgto7314Ue122M3W8pBTjf6tJYKaXdXT6OucyJ6'
        b'2sIPyrqpQ9VhtKyvOhHSRE0SehbDn6bJ1Yot7gV+EDsE+hSujoA+DYE2hqoj261nC3yafEtF6ih19BYJ1OKv9qdOLkl9krnEN3tO3uJvwz2kdj/WaClPd/iTQA45eK2K'
        b'qFOPqIM2wbJHxLOjX4V4RNxxHhHvkEcUeQjyPSIuEY+Ir8Yj4l8hc+vzUKlrgWQZCrXqPvcSIBx6E/nqo+L1mkIdSH6m8j5JiRnWlL6kvk9CXE+1Kp3FXcOzVAvCXmEl'
        b'rOfyPsG8RQuzSiQWfPJg7NyAZjBPnERybxI3eTS5lXpYnIIkzZJGZp17g3ithDoFuVOnIMl696WMWkCPWAn/Rs47OEwD+Unj+6Nt0BjpiSvb5Gmpi0OJRjGgyICIRFA6'
        b'VJXS/rlItJy1AsJCDEOWw1yWSVHpTQNqID/BKUAPTFZqJFNIZ5PyQDlKpNQFUGqulgL9jJeqtWVak3FgvyzdsIHBeS/4ZOc9sG1//EAfYn+oD47wT5Rm0E/ShQXhGdZU'
        b'S8eMzvtCuA2h88AlFNL8cqD8gM4aqdFcrNOoy2A8T1UL71vCq6hQk1QFVUCY779UVwVcyKCQppmklWZQVIo1TmtRWQZfrDHVacj2rzRYrSlVmXUmGT1ql+AaFha8T5TO'
        b'sXyTlhD7YbBt19HO7ihzVYt1zSRasdVoAyY52VdlkAbzPiwV+J6hAdRuVxVZfKUSqY5F5BGohscRC6kI1pQppLGREWHS+MgIl9XYLdpE6XwSkNIAqa5Uq4dVA32U1mtU'
        b'0LEQvaaObIHWxiliFJEhsoFT9QN+w178mQTPBX6MlGESjo1oyCiPdGPMhCSMwlv9cWsmupSDm9NwuzIcb88hnqSpGTLcGpaFj6XLUQvuzMhNRZdTszIz0zJZBnehY15V'
        b'+DQ6TOvNaPBigIUG5xhrMuYtUfL1luJt85zUiy6p8lJxB96eASwRbX+y4i31Xgx6Fu+j9SZ5uTN+DBPxq/KGsA/nrmbMhKOn4DM11rNSGXg/OS6VqpCHkNMo6IqQiVsu'
        b'NobiM/TAF63k8yI3Biit36+yVV4rp/rwnUNncNeKAb1rZcnAcTNuI76D0MM22WK7zqE7Bk90PQjf0W548aTIuBrqMbUkj3ntbfeNEV5b3z/z7I2723bd3iyQ/NrtcviE'
        b'rKJ5UbdezEkQPjiaPvxIu9/eSen+q1Zvrd3gs09+678yi49n/fZC4ieSv1248m1pjjBguSD58efL38udPrri/aCbqsqRmWhc+IFLv6xKS4678lrV9+8++vvPM6bMHFfZ'
        b'KVNEfSjz4t1o76JDeBtqxY0z+085ChjfyYLSGbiXZlm8SIpaU5Zl89DkQckyQbhR2BCJbvG1nMYX0zxhOmWZ1iNTw1CTEF3ylqDD4dThFm9fiS6i1mwHwLHM8PHC+XM8'
        b'0VF0hrrsrkI7a0LlwalyfBy1c4wYHeDk6GQlbQS1JYZBBXaQ8kdXBFK8GbeuRdupR2cF6kZHQhUy3BKGD4YzUP4SF417GkwTSQ9u4Yf4Ogy10w46Ysa/VjACHUD30U50'
        b'10REskV4M9oIDRHBi0hdJQGkrxYQAy7hrWIFuom7aKUCiTsZVGtYiILkwu24M5TkkhpFqBWd9jbgqybC5mf4DCf5qBUTWpZDu2ifALXj83gremikU7R2TgVqzUDNtpYt'
        b'8l4Qui2Ebp+v4+VIj59wRKtf6CQiA/U2JY73zAZmrZgVs36sxPIkh8ck9ACZhCMpYrZhiJUZ246sZFk7Qj1NyWowkONehlnkMZs8UhjreZg5zODuqhK+VH8ls22laCVO'
        b'TtY8It0nLpfMRqZ7rL1P68Cu2vyZWcs/9SUl/VnLrGKoSMJmydg+z8J+ucHqQit0mLk+SbJOVVmsVs0YAvUYSZ127VnTvrVQckttVq4fDBxCLa/S6+pl0JhAXVXygx0r'
        b'4zvmUWiTJJz3y7AAHgHWLn07jm+fL+Sk+aedEN9CR+lhkMZH2BqXDSph/KhuWIbvXmhl3oN0IMjWgcAUlVFj4/c/ZdzuhVY+P0iDY2wNTnQpC/z4sUoKLZLBIC1L+1t2'
        b'KT38+Ja9Cu2EiUFan9gP6R8QOJz0weFEAT3fxjUxtvNtP3SeYMsPn20SZGlv1m0R0SOx7NdzPiviushppfLSx8x/tf2y7QOv570OaZkZx4Vv/f0bGWci2XAjurQcCPMG'
        b'/NyTtBlvxYdHmMg+1/iZXnbsgCfK+ORkK13ej9oGO3DmVkhWkP2xow3wO7XBz45W0QwuHPw5F779i+ExhcCDuNYDJdzIvONw0GxA/TKPPjfLiuTd98VGk0GjMfVJqquM'
        b'JiIQ9wlLtKb6Pjc+T32fuFZFFUnPEhDLqyp5BVNgUpX1iaoA1w0lnhZYkF75WOExn4DW06YnettO5vvwdyCU+lhA7tnsBSD3ApB7UpB7UZB7rveyaIuloC2+K3KiLc5W'
        b'q42gDhCZVq0pJqsN/kos/m9SDfXUfwqFkaozVBdRScvNZRo7FQ1mxKgFFUfKH2Qg2pZRY1JIswGjB9RDln0l2WHRVlZXGYhmaS1WotKDukKKgqpj0JSYdPXS4npSYEAl'
        b'qlqVVqciTVLpnnhPGhVkpFpiK4N1ZanSoiGROgfUAVWbjVp9Ge2RrRppCAVWyFPMyHzLaMuJvWJg3wfkDzapDGXQhtpKgUh5KbH+GYm2Yawxk9ktNqhKKjQmoyzx6ZV4'
        b'Hk8TpbMdWIh0Gd3vXOGqGGk5UUpPMCz7wXMMLmvhl0WiNI9+SpdZvOpc5rcun0QpsV0CqKhyuczeq85lWbLgQC2Fp3RZtsHkOh+/JCEr/4W2ESZNy8uWR0fGxUmXEXul'
        b'y9L8OgaFc3a+PG2udJllE3BF6DL7UxquG+9f/kSF5gNSUpG9b7DL4kAwYDLLYWnAcjWWGLTVJgvfInhKDljTtTVbZ6wC/NWonWr/gE4kN+EzOnpfDgW2QjqXNwHQJToh'
        b'z6SqrCTH2PQTXBoD6GIAxIIOVFuWllpLb+xRwbTWaYGfaVYDxC0LbmA95CeryqThlwld/BpTeZUaKEmZGfR/0hdVBSxAWDQamJ0SjbQKGLvTevghkUVDbRtGfphao12X'
        b'FNL5QNSsBMlpLfbLjlhCANXJfUQlOhgwfxWRUeO8ZJHlNqKqEtpzfnskudxkqjYmhofX1dXxN08o1JpwtV6nWV1VGc5LluGq6upwLQB/taLcVKmbGG6tIjwyIiI6Kioy'
        b'fG5kQkRkTExETEJ0TGREbHz0tBlFhYPYHZzfheCfxZvCu0WjjBmydLkC9MfNWWFpRIM8H8Ywk/JE5fmVZlIoF3Uroxl6u8TmSCYSncOnqPp+Xy1kJBFD3ZhZRRlrllYz'
        b'5iSS6TpuQZuUVqaei5vJbSLp8oXkFOvCYHIwdAmo8fChdEMn8H0G1MOr7niPGV8xEws/qMRBuBd3rN1AFT43RoS7OS8f3GqeTGrviUVbca+C3G9BjstC3eSuEo4Ztw7d'
        b'RKeFoHXfMZmJpqMGdXon7gXVOXMR3lFNh2gbXg5uzoKSbcpF1fDIzkjHe4QM9Pseuos2e+JT6CDuob1BR0KyPUHtPYoupUPqUQ/GPZ3DR2uG86kn0WkT7k2DOlhIPckI'
        b'0D4WbZyZSe9DQu0y3OWJm8MVeDu0G4bOp4N+3MwyUn+0ZYFIGBNkJk4woKYeRbtxb3gIy3BCYSobV4Jb+Xsq0t0Yr7CXheSCodczJYyZXrFyCp/JMXrjPfgmbRcgkL+c'
        b'W4CvoYdmqozvRVuKSbq3twJ34ZsZ+Foo3ilgRuDzgfUCdKkcn6MXOuXiOzM8FWl41wLoVHtmGpkaATMM3xH64l0TtX/8/cec8QDkeyaOk78+3QdFeImKkmZW9k3p2XS3'
        b'xm/KlZ8NCxt/07Nl5JtbN36YF1GTs3LS7vd3XT6bHKq9ilN+q8tPXT3leOyHu/bHHU673/HKMF/Z8DWnfvvRq7g5b0bOmVc/mho68VGXqadxzOP3hYIb1RvZjp7vkp/f'
        b'PfPAlkkPfvnO3by30wK+fSPptS//vee739398wce/1P98QeeDYF1K7Wrv2NmvB7yRqBZJqYGAIDyRnKHgYOVxRvtnywoxafxFRNBm1lamCorStobHQAiTGi0CHe6407e'
        b'4NKOtwUQg0vJCEeTiwQfQt18gw+q3fGz6IITswPeGjSO3vmxBm9DV0Oz5CZZWlqmMgy3y1hmOL4njMK3R1B7TCHq1CvDguuWpUJPAIjoIlcfgR86CKU+P/HKGNenYj1U'
        b'anUhL8ZRqXmKVWpOJQdjJexw+rT/FdL7PCRsw1Cb1Ntfh8Vc4c0Lz0sY607dUvJ4hjwKyINc2GFYTh4ryGMleRQ6yuLOz/d68nX2V7LC1kShrQlvW4srbe1QOV5FBXt7'
        b'Of6tKfZyvLMRydz7vNTEo88iJ/V589KvNShWVdJPcnuJps/dsmVbounzJLIKSIjEoYvvg22YJR4WQkxMLH5WQpxOhHkPB3HeBwR6X4tI70dE+lI/i0DvQQV6TxDoPahA'
        b'70kFeo/1nhaBfgsI9J1ugwv0KpsvnpS/qOgpxNZ55FwDn1sKvBPmCSRSkAdU9pftEZkhTFpmqDJXQyqIyqqBvKiqslirV1mlkxAQXEIoW+W5KtHubY6cpIM2pXdATUQJ'
        b'/n8ayP+fNRD75ZVIAMXH2GxaP6CJOKxHvjwfZa3AqTi27AccOV02x693vh3LErfE8RKtvorYagxUZtU7l0TrqojIqK1U6VzIvMsGcWUFTcK5M6vLHhPKxPe3uKqqgvSX'
        b'xCikmRbsUtGwtKp4FQAe9HvnW4J6ogElxEVEWoxfBBFAfSPVLet3c3XZCRthTJQuMppVOh1dGYA4tVXaEttqXGbnJTuoEmghrI5goGfqltl70v6gmkaKP6GqOfhr/l+g'
        b'aaVo6jRlFm+b/6dt/V+gbUXHRUQlJERER8dEx0bHxcVGOtW2yI9rFYzIIwOvaZHyW7/iDBGT/Mwwch1dxu4gM2MmuhZqSR2tTMvELWFpNlXKmQZ1HaQ3dN89Bu0X85fA'
        b'7q1ZSdQn3ImezevXn4TosjmB6k+4GV1XKtIzQW7trxnvQw+d1M6gVtzqjs6WK8yzoHASPo/PG7Mzsy0XFRH9bAneAbk7cTOoUh6gdECNEL6TtxwdQgfQSXdyK+1eT9wx'
        b'LWs0wyucd9GVJcZ03J6Wma0ktxtFCJmR+DnvFAFu80Bn6DWGUPJZd2NIJu4IJnK6Ig1dDmaZcWUifHGVCN9Em81SmgvfQQ88QRTvWCjB7fIs0LC4yGLGP1qAjs9BW+j1'
        b'ncl4E7oDE9IWasRHLVd4kmuF0M2F5A7PSNQqWr0A7+a7dhxvHmHpWlqYDLeLvPARJgCfFODnclCXjpxWCEvimPICIskVZZxaSm/9RC11+Z5ihsnHZ93gcb3eHAOxVXiv'
        b'wJNMEkxlF342FXTMdrwL3yR6Zyu6CKEM1D0Kd6QStWt5oGQB7h5HtW3cha5Mwb3wLQ0dGcWk4YfJtJlqBdpBMCPSHV9nIqfie/SqU3QNHZ3GX3Xqjc8z4TFTKE7Vq92Y'
        b'tcMBIaRFXiU1axiqEk+dnkdmoN2il6eGLSY3CoenLwKop+K2vGAZwD6Vv0A4E7fJ0C06R+KR6JLee8UI3GseSXt1Fh/Lw3ui0wUMi5tm4ksMvoRurDZPp/gVgpo8LcBY'
        b'2I8bkjh8wMlkoCt4p5BBTYvcn4nEnWayd4E2TsRb+/Xb3GC8Jw+QWuKozc4cJvaBGndTldc/Bj9nTJdnZ8LA0NaRyvAsizYrw/tF6AY+jK6YyaXPxWgfOhjKX2UjEzOe'
        b'6CHqROc43At6/HV6ne4cz+y4b4XN3ky1aujbIz/nDjH8qJ7NGY97LXYM6oBBEAlvD8/OzA221Lc4lV1t5yxxGJ31guHvxcfpDbOLx+IHoYDHN1PCQM0Xo04uHJ9Dh+m1'
        b'tAa8xaykWiBnYPHJrAS8KVomoLaBCnRlMhRbinbZiqlqacqQCHTXVgjtRY0Jy3AXf7JnD97GOYyyTgJjxAdn6r75/vvvn4kSMq+t8yPUxmuyfx2jffuTd0XGZNCTXvrZ'
        b'jRU7pmfhWX5by2pfrD204d87R6Jh52QLq92CfCI4tVLSnV/+bs8vpblzfxPwm9GbWoy5X45+7sRb3f/405tvvxV7fVO7suXK+Fd1xWkfvlS9tD5tz29GLDv7+k7RvPUq'
        b'JXf+f0ynvl/w3xsDvp7+aPYU6YJzsk/9YueM2fdn9UZF7LU0098OfjSlq/DnHz4aGjjt+vF/jWanC/9sys/97nLJJy9vGytO/HPirxQGWWLrOz2vC5Zov6t45r2o/6pX'
        b'Tw/fccrtD38Z8ajpePZ/n/lFg/rKoq4uc9ultzo+u/nLY1nHTr0W1NT73fF7E15TNOatHPLOo45xV03/FfX8u9/+ws131dLTxx70Kb7ZHPT82BOvfie+GPL84/qkX5/Y'
        b'0P2Jdva/3vlH1vsrWtfViQvf+9504evMz1N/P25N54NNv3+357ji/gtX55YuvHvmf//tOz+r5uyXZ2XeVO3H5+eXWywRt0fZu3zgc8/QC/lQTyG+ZrNETChycICghoiy'
        b'WFpTYOwqB7ePAlj0vBniYhHf1F20eaGS+my0jrW4bfguFujQGXSG3tGFTuKHgHQh1GmDYdyf4VagG+g0viym13ChfXjfulAFbo5ZBKyAIFcHJ4f1eIre/bgUbUMPlBkh'
        b'YoZbwSbOjgeqS80Wi/GmfHQxIzOMY4R4D9qtZNH1Saibr3EXOoxbgDO0407dJOqsIV7LTa0YQvf6GnBrliuHjpAl3gn4OeqqgbrwkYkDNgWZIAO/JxibzJtgzsXojeiy'
        b'ATWmZskJz6ITPQTvEKAeFWrhr5g7jdvQZWVYcL+FBTXi2/XldYPcjyXz+w/ZXJxZX3yInaFfDacWmHwiHmygv5yXxf7Sb4UhN9bxNhga4ogDyVhIDWDF1I2EuJT4Q5jc'
        b'SCzhfKiTiQdHwg0jHKwb/a1abDZevN2kmDyImGIgl+EbNORRSh5lNluKM3ON29NcXOzB11liq7jYVlOZrR1vWxP9hhstPAocDDfnQuwNN66GViKyiFuEUTveYy5qcmti'
        b'6C4p2+RBzS2eTULbPeaiZnEjs07cIF4rouYVMTWviNaLnW2Rk8rHDZDlfHhZrstDQAS91SK3It2+FQImn8YeXidk4HNp15yisMNT1jKUj+Jj+Ay+bkTtkhpYDbcFjMCH'
        b'TQjHJyhLQ3t9/PJQez5uX5SZi2/mLJmIby7yjouIYJgxIwRoUw46QW/uL0AH1XnA9Xrw3fzYCNwSA9KUpIbFx/zRWV4e3JyCz1trwvvwIZYRhbDowNwNVNhAF9F+3Ih6'
        b'xZnrQFYCMRTtomKFCJ1djU/i06JhgKVTmJGLOcrGKvQipSIiJioWHwWpkhGvZ9GRZfg+bWnEBnSHXg2ega/YXQ2egg9rubRskfET0t2LL83LTsoSzPa6+WJS71HGfeGW'
        b'WS1zX519rlx27pNL84JOzT2Vrlry5u0PR47eJMjJzTWMTn6rfUfsG18fOTp9LPYSBVy69tJqgXjy4y8uvXruk5Ex1Tl9V4QXPlg6LGdnUeWZJX+YKYla0Tgh/spreYZD'
        b'xgPGig/vj3lx8+vZosAz1Ru+KIv4YNLSj9vf90i/L99SO27+g9kvVv655t+Pkg/d9v480fi31pe/PHjxjx83P1w5beb9L8f98XJc+LHc4gc9kzIPb84JrKuf9sWdA7/B'
        b'v/hgevLV2DHv3j+VtuHFZ385tProvg9mvrwv+S8ntiz45MWZpqAs3T/KZP6UWq7FO/EDegu/G8Phe/XoBLtIiR/SNHwFt4+gpHQR2gnUlFBSM9pFKeks3JWbo+MpqY2O'
        b'4ssWzzgTOuxvpaT4ZM2TxNQbPVhMOcQc4hnYGo6a85/wP8zGm/jb2o8NA9KYFRQSBjJfZzi6IGR80ANB4Xy8n3axBD2LduFWsoVSEyZihGNZdILDV0xElgomL3cgd1aj'
        b'63ijtXJyazU+jzr5a6+b0PY5oQp0Ch92uBBeUKUpoqb2ufJsZQa+C8n27o/D0WXhqEJgN3QL5Ty6hI8pHVwbC3E7y/ivEqBLIPseMxETNj5Sgbc7s+/j9gYLWx2O9/D8'
        b'5SG6DQpBK3T4Etpr563oO1awEvSOXjo6EJc247tKBX64rN8pknLXo7idgigK3yiy8Ba0eaXFgI8P4WP8ndw3avBh60X264aRq+zJPfZX1vGceSs+vNJ6fybatdh6a+/Z'
        b'OfxdvDdRs4zIdrgjOy21WgSpO7gqseLpqO5PvWfewbGGvw2fMih1P4MKJ+yH+i5SD0YhYU4cB588s/IC2sz/CinL4rcOSIj3d5TY0q2/Yk7I+XDDOQ9gaPZuNXzzPKNy'
        b'62cRfW68KdrYJzKaVAZTnwDy/ViuJDKQ+1oNFTbmo7NxIMp8VsHjMmu5FpMyn43Mb6Uu/H/4jv4HHLEsRvxvPxpgQ+DPUZmsxzcstlidxURi0JjMBj1Nq5SqiKnfzuLy'
        b'VGZyaYWm3gj1VBs0RuLYyJtyLLYpo80+b7HrODNvP2m61/EGMdKd4nqTxonpycZLxZb/J13izTKyTHbiHSxqxXtBS9sOq2cnur4EXYdFfzF3MdqKmkXMSLRRsEY/mX/n'
        b'Ry86PRvvAhgqxEGMAp/mqE6/ADeji5TJotYlcrxXqVAImAC0fdIQATqfs5ay598v4ZiESPKtKEMw2ZuhO81SfA132wqKJ6De1XhPMbqPT+ETUUxIrCgBHRrDv7akHXfN'
        b'By3NqqKh06vDn8mkPHE1biu3MF8gRs9lWpgv7hnDb/3uxBfn9Gtx9/DmBD8ZZbQeaA/enEd4NiShdpaIsqPzcrSBN3uFxq2Q4bOAkZltx30aZ/nNLav7Ir1mUeY329ez'
        b'14PyNh3Xz3nTaG5eYRb/PL5ujt/tl1+794+tJY+WhATnf/nCvyKv7fq6BaW/Mn/R8vyMz6u3Hx0ZuCRu/1+/eXd+WN6NR8eaju0qUwafP5CYoJ2xJuyz03Ne7stvWfuu'
        b'cZl2xp2Pl8YlPsYS7Pnnj30zUie9lXXRsgMbhw6anflg70MP8dbkXBMZavK0MUBsbRf+4pYxEyePpSllqHFBqCKTg3GeY5finUqQSHp4FefgKEQ2dvm3WXCMpwbtiuFA'
        b'bnqI9vPsYcfkZU50BaDwl0aCsoBOyCi9nURmnL6WJKfOng/JI2TiH6AWLjwPVcZCss763xPCE0idUBBAZfIA+CTkjuyq+gOBs6MZlqJZP9IpsQoeHz5Blo64cEu0NCFj'
        b'+4TVKlO580vQ4xjLzdNkv5G8D0Fsuwhd6PIidIvz4PsC1sleYz+lIkTDqKol33Q6e5r19IfNSMcTpWml0hDyLUQKhNbIW7UJNdKsJidZiZE3RNGgrQ4Jow1ZyKLBuY3Y'
        b'SK7wU9ss0ypDSbm2VqOQZhNDep3WqLGRPloHHQDNrpKWVumAzA9CxxzeL2CjY5IserU72oguAnamwtLISQVZIz0zA53PT90wHl3GzWEKkD1S8Ta3anwy2UxOIaajU6hN'
        b'CSspPVOBt4NUlo+byXuc8Ca0BcQNeTC5q0WJb7mhvSELqBtKLroA5HEXtNISloOPAh/SsWizF75L7YZeaLMSdy0NBb1lNRCka7GUXNaiG+bQbI5Bl0PZhQw+MHKldu3b'
        b'j0XGHkibEGaa3k5dPrYePRwQvKH4EzZhju/PXhAx26OYvDNeqaJtPtu3RMyJiyvtSN+Zrjv63eMvRBqVrPx4hblsTkq2h/bsV1c6Lq1pkX18o2frzyaWJ/n94Xhu5Lot'
        b'n0Qkztq9of6s/lHRgs2xWb/tmr7mo5f2dhz2n3LjY3HNWE/JvnWfHzi17e2pX8UMOb7sO29zleRQeNnspOFxW/+y5v2bb9aOvfzlyU3Pi5eN/tX6oV/kPFhfdyB21M2H'
        b'Ml8qNy0HgesMnWZ8C58BdI9n0RV8XElpQCiznh6ZaqUvLkMHUY8Et3Lr8E0VlUWz0BY/vAlE7F58o87i9eGOznIIdCDUTW8mz6qbTWvYrmbDQPXJ4kbjJnTGKuq2gU42'
        b'kbynLUyRBg8gVrgHRP41QXyGDuBirXFqZRjqyOZfAOA5i8P7oYDl/QtH0S0ZKR6ejQ6hU3KiW3EhsUW8nH5tEb7F4v2EU8gUuDOMSPq+EYKy8DDaM9S6OosnrnkVlvvU'
        b'BbiZf8fHadyEH8hGh4aTnQS5QsYB6TsqQFtrl9KiI3DHOCpehy+rAZVNnMyNwLdWUum/amiy0oahmXXuARw6jhr5d85EoBaWqCdZ1J7bTeYjhRuZjq/S0dbhw8AnLdIv'
        b'voduW+XfLnSZtrpg/gTaIX/UDMAQo3NcGN6ZOphZ5gfotB1tFpJ16+jcQn7decOKhJ7BAaIMkilvKPGH2AZvG+0kpbMc3glQ7UigB+kkx+ftJ9oGeHz/BNFuHO7wjgCH'
        b'hqFy28llA9lE4M/Hx/KVE4ptiGeo8Ybs5RimkUciebgqxZ+pJ255BvIOR8N0fgQ0+1yC03ylpDagVpYfmYj/4OB/6BMn8YnTvbqqpLCQnhfqk1Qbqqo1BlP905xVIn71'
        b'1CmHGniooE3ZGp0mfsoD/uPWt0GRxUDeBPJHxuKNIxEKOWJwY9iASZxFX/nBJ+cj8AKMYtjhCi82gBudExTvM4q3vFwegm8Y08LS9IVyo4+PgPEew+Hj+BBqot6BC1AL'
        b'aLfdaJ8nOmciZMmTbLzkkA2X0VHCiXHo7P937y9yyzITv6RZgaxhKjnIMp4ZD2u12cy/XgodwpeUCtQTARglxFtrgBbVoNvP8N6Il/EDdI2afVDzDDuzz6RAvvTFiWG4'
        b'NY3Q5LZoIVCy8RLUyqWnirS7P5cIjQQHq1rwZ/QwySfqDNVrxY/h+6rS8tLHwmv78/Yv/PW+/Qe7f6bbGzC8J3hOV6ZbiccctzmhuyYJUqfs3xTtzYzGvrc0c2Qinope'
        b'xWcqQy0GbzHeXklPKW6ZwJunH8pn279bbjraCTRpLbJo7MdxN24i9nDeGj4cHycG8doZtOK8tfiUVSMXMfNEVCPn8C1aNANdRofJXi1NDMQ3JSs4Dd6BTgx2eMUL9C2Q'
        b'dDSFxG+Bkqvh9uRqErHmEvIkhKfBbFsgwj4hKdAn5s+OOXtlUh2JqrWhOCk7nrPWv9Hy+7696Mjvpu5FhwNwa1locLo8NSwdtYfzu65SvFcUMAtdc0ChYZZP41f2l2JE'
        b'kIshAC85tWCLe4FAI1QL1aItjFqsdmvnCkQQltCwOw2LIexBw5407AZhLxr2pmEJhH1o2JeG3SHsR8NDaNgDWnOD1vzVQ8nb5tRRsCZYetWGe4GXJW2EeiS5BEMdTdOC'
        b'1KMgzUcdA6liemBGqB6tHgNxvupYiBNCiXFqKbmwYrfHbm63oFSwW7hbRH7VgaUcxJFPge2Tj+WfQj6H3VP45Hf1+EO+UJdHfz1PllHHDYz7aU918KGhatkhrmCIxl8z'
        b'RB0SyKwa2sg0sjQUag3RHAHU/5A/SiSBOXFTh6nlMGvDqGeiG50nkVqhDoe44epAaqiI73MvBM6lmg/SMjUTOZjeHXUM3r9RTN8FKLYZ3EVPb3B3TrM8eIP7kAkiYlpP'
        b'+Hx+UYZc78afK29m25iRLFO0f2WR/herR/CRjH4t+w3HlEfMVI3KXRjImMMJ1u8kNMH6es8L6BT1D3BQKIFetLoxeWUSP/EYWtGmuokMEK5ZXkzRhK9nipiPrZ38mjy0'
        b'NX2PeKvZsI5NY9qe994Y4SU4HHM6glv2l8djvX421T/1u2FTjqV4LNv11Z3eya/OnzIqbKluetfUmAZVTkjCiPgR598ak37un8UvB++ZHx+4dkzbsKBxR9YM/XPbTLcx'
        b'h9Le/O/CBT9vefQNc+5oYIFur8yd0qdhoegc//YuuYCRAI1ryudMuEvAmxu34RP4CKjDVzMyYZUfJ9LaVG4I3ulNRd8SfEPqiVo2DDhkLsG78TG6a5mDr5Q8oWfjNp1l'
        b'ZiYHisrzQIylCvlpIMEXoKlL+FlCZ0OD5fwcQr4Ro4XJkyvo4UB0aJ6C7y5qp8brthWgjzND8EEByJg7xlMb7Eh0z7s/Uya6tAhkjCF4jwCdjBjLW2kvCNEZ1BoO0msa'
        b'eduxBD+H9+AWDm3Bd9aa6NvYHiaTiamDSiiPhapQZ/ZwdBSmaHs27lCImWlKMdqrxId4+vrUcmb/ce+x9nQ7Ssx6iCTsSHrs22IsZRv8bYvliZch8sbNPhH1TuoTEufW'
        b'Pq/+DS19VZ+7Vl9tNtE7tpwbCUQGcs2nYQ15rGes4udah36GD6D/bzpIoU7697SnekWFpNODnGydzVnPdNu1YjvUPbr/htAB51sVUGsaQdCnPGvrXWg/c4N0aa61S9+O'
        b'tWt+4IluxdNOgkehDUqDNLvA1uyYNGt2q0/lj2p1i/VANUGbwkrtYMea022NDieqhrTUUFX5k8ZobU21epDWMm2tBdDWiLftT2hLXGiqMql0gzSUY2soMJ9ktfrkOm3t'
        b'p5vlnb77kWMGvviPMobe+dzS8yy1I+syQyxsZ67ZLaGXHUk9sRJiRzDaV9/7Tmgk9u1/fbeACL6pqt3q4D8pVV6lnxR9wnx1MPB3V/P2vxC4OTDhTbbolujTDWdlrIno'
        b'cfga0K2rA6iZlZRJ8U4LNUOt+PAgsidVxCjpoi8vs5KuxUTYbBhiTwp+6unpvAH05qqDqdJJI0QF/Q8pPE8hPFgAdjZQSA5kzPqN70bdyGX/mk8nBIcpS5j3lhAEZTdO'
        b'0z73pz9yRuJJ+Mf/LeffDbxD/VJxhipDtar0U+brypELRwKoop8VMupEcfju72UcveukuqTGBqnpaOuTwLJAaqqAahB5eB/aQ6w/IfJA9FBBthE2c9EMPjmYBuFbSB2J'
        b'tQ2awmJdVUlF/5vurBBd3hBoN9GOuR1evyqiHrDOlIk2xsGg0QqPpQOAe8EBuK7btC1IK3yJWcH6OlYBQFjwU9/FOXAPyeKP8Yz+H+xjEIkO5hcV6oasZqjDHSi0233R'
        b'RSF+GAJsiWlAz6FOqgBnj0slXkInAPhrmDUbRtCNIHQ0Ko+4bdq9A544kOYHZ8lZJgZtF/vgzkDaWFQxlUVzVGlFYXuH+DLUpTBPnc29IL693oe4FC7NL9/FmIndxq8m'
        b'yXrHkYNfoQU/7O42QnvTiGdqtwc+AB+XDA1QmurW6kigB/26tchIVWt8IZP6+X3RQDuzmptbpDu8RMXQyN/48T1sm1sU9vfEGEabMT1ZYOyAyj77+Nzk9uPk/fRz/7Ez'
        b'JmfWe/v/LerwmLRh46z39SGKC1oRFuJuyaRxGSnvvv54zXOdVb8Q/eON3j2e7m+u/2u3/+79mw92uHNx6UkvzNhU2XPt6PbDvz4YpZm4LX7F8REfb1z187LKVzb7TvHp'
        b'/ei3R+M+CNjyaSquOD3561uzlxz5ufGiafPPA08+3FQzL+l/mSP6CW+MzZK5UUNihq4ctG60DZ1wtHviB/gk3XlCN/F+vM3xfqR1+DwvvZ7lTMT8Lg/Ce6xL8Xj2QLpp'
        b'WYr4rDv1JUAH0G780DPEIufaqgUk2TQO9QqBAu9E3SZCwLUrURdIqOjIfPr6bYIb5Jhou7VqMROBLohHrzdTGb0aX8u2eaOx+AH1GIBCVJQFkXU/EUOtJgZ0Gx2kRgYg'
        b'+jf6X4nr0uopLqwzaC0vPHUQSAsJVedYKQikQRa3Mi+2wc9ujdKCjm9jVhnKjC5IPWfocCQJ7fBYPoAknHF4I+aA5rJKhJbVK2YGvpiXnoezvZhXSPejREAMhJQYiCgx'
        b'EK4XubJvDXS0F2dRZ6cGfEKBdgnQYfSAuHCNw5czqPJK3bHS8XW0JzRXvliOrpjQQSHjNoQbi46WaSesPsUYIyHHy6lhPL9+XPR5UXnp5+rPixTDlSqP0lTV50WfFmWV'
        b'7MjwL5GUvpfhxhz/SCJ59QrwbSmB7cHcKtBSiDkFAVpQtw82Hh1gRpULUbMu3Dr3g9u1xYX0eASFsJ89hHU+1N/CYZJpVqtG0+9iR9+jTO1DA0i9kI9/Ii+FcCdB9QEQ'
        b'7vZ3BWHauHMAEy7fJAIQi6lpgYDZ7SnBXP40XJ0HJ+mnJEiVV7KAQHMvywjwc2wmuoHuad3eH8YZiV3aeLXzsyKl6qU/BX+QxoteRZ8VaUtD9n5W9KioovSx+rMiriUi'
        b'Ltp8/XSEuae253Tk9khhdPUthjEt/e8q72HXp/SLpU/leOLwzmxiw7ODZ4A9PA0S3rOGOHEOs5vW/jJPB1jnR2oHgfMOeFQNgPOukfZwdt6hR8Tc4RziMfySFlkWtegp'
        b'oT1A6Ba5hDZhhWPw4eQ8+WK8JzpVwIjIvQJtLNrMonNaQ5pIaKTHJjYnflZ04PM0G8hTVZ8WKVSfFD0GsD8u8lOVl2aUWNfvOcbtn3nPwfqlBzJ6R3sRV+hMdJV4Q8fj'
        b'bV5P/5rdPp9Cyw2jdvB2kLsbCLwbRtpNrEMB58DuE5eqSkxVBhdUWmjY5QrKO+FRNwDKrQH2UHbZGZkv78nb79hLfHr7vPsV7wpNfZ93bZW5pFxjoEUiHYNRfZ4l5FYX'
        b'DXlpaqR9IKpPotYa+etYiH8weTO8idy7qzGbVKvp1bFkV6nPS7O6pFxFLjYlUYPugcmG0gPkfSLiyxTZ52G9bkWrtjudvpTmMGlNOk2fhLxXg2Tu8yTfrKe+aTS9x4nW'
        b'FGUgFyP0uZGDiMVVq+nR9D5RdXmVXtMnKFWt7hNpKlVaXZ9QC+X6BMXaEhnX5zZ7zpzsRVn5fcI52QvnGS6Qpi8ydtYNq1BMtlWMZESWq4DF1HWZbZKUSn6KAkTwYeSA'
        b'xVPCi8ff66hNdGRjhGrNX5ZF8KQTX8AdiUZ8y3e8L6AMh8+wIRw6QN2N0Sl0zt9oqoVEfNOTvNX7DOOGD3A+MvQcPV9mRgcmhRKfyMvBqZmKtMxc3JyFLofhzvD03NSw'
        b'9HAQdUGwsp4s8luCdy3zmoPaG6hPQto6fBDvyoVvDasNTGY5ekB9oXAH3oaPRBPXZhYdwVenMmhXLT7O+y+3g9R1NprTZDJMNBMNWc/RMYAUdwd3QhmOYZNRVzCDdqMb'
        b'arpl5Y8vLLf5irLoITrMeBZw+ArqCKVVzmpAV6CgGBrb6i5j0J71QymNic1Ft3ln2Fghg04mi/A1Fu/CO8bxisacECYfhLxx/kUTrnkvY3iftNML8qAqEPdEHiEM2itc'
        b'Rn3SZPi5aqVCriCH7DLluCWDZUagU3gz3iqcNQNtp/VFxI1nZgHkZMai5bvShjO8v1h3CboBFQqgb41rwxi0X4R20Ns86tAmkF5wM9qBt4Yr0ngh0he1C4rxVbyV1thY'
        b'NoIJY5jgRFnR2m8mzLTUeLoc3YQa3aDG3kA5g7pRWyWd9bR4EKs7UPdM+m4gYRiL7qKjaC/fueSZzFqYqYKZRQtfm2vpHGrOxQejY1APqGRr8SUFwEC4kopW6E4s3kv8'
        b'r2CwN6tZxj2SQ/vxPn7i8sekM7tBT9nkX7Tqq8QcCwreBnH7GqkMYC70CwcZCu+ZSvu1Fh2ZxfuZwQgXZYnRNm4iOppH63phBVVvgv+WXqT79+IqyxBPjEWbomPioFuL'
        b'q2DO9qDr6DKdNHwEd6JeZTraX0cuLsUdSuob5oO2CGbo+d4dDpzGVEON+ZVFUbLZsXyN691QB1QIqAXwvwcD3Yc2ruGvfDk8co2S3PLSmmXBMIJ3oSwThHYLUYsbOkMr'
        b'EKOT+ALUADhWgHbB6PbjC7P4BdaED6mhR6cm00p4OPpUCxJi0UbaIb9Cf2YScVRki5a/tWwNr9Cm4D34YnQUwdlQFoa4Nxkd5C+oOb14tAVnobfzRfg6i3fjfbB46Mzc'
        b'qxwSHQv6NxuIeqLIrfiX8EN+23Y7aFaXQpXEm48lC/C0WMsFouOF/AnFA/hkQXQ8Kbh8VQL0vnIG7Tx+LhRdCCUX3qThFmCWRWgr45Us8INFuo82qMdHUScUhL6g3d6J'
        b'gCFFuIM2WC8lx9nokpShC8KMsYyXn2AY3jWTDvpWuYTYaXLmlxZlvFuwjMcRdN7sGx0PtJ6FSbsBlXXj4+geTzFapw+BfpDDh0oRM2mJuIQbtRo/R/swXIvPQzHAK9yN'
        b'ziZBHwSoh6aUo93jlUp0iQGa14NuVLGzjOguP1EHl6K7UIj0u21kMmBjHb5CW2oAlfyOklC1NrIDsa5aPJRzH6elva6csob5K1Q7NqhouL621HLqYyM+ORL1RsSIoK5T'
        b'aHMKQ4x6eAetrQYfjgH9YEV8OtmiFuAHLDo42XKRc3LmAoZYY1Tjizzer2ngAY/bZiWSyoAgjMCn5zDo2Nw1vIljF9phUgJpETOcz/SVbDh+GECreZwcyADgEvLLi5LV'
        b's3z5ataHSZVpqDk6DJBNKGShR/fdaYI/CM3NeJcIPwS4KxgFbkRXzMS8hW8U59DDCwtTQdWVk4OkrehCSTjQ+8wwID8Ms8DfbVRIEI8XW9AWqe3kaR66RbZq9nOwEi95'
        b'918GrZjCER4oVXgVZaREejI8fT9SNhnvEgPl3cQA9QrDF+fQhTazvFb5xC4d8BkhMwe3TUYXROYJCTwi7Mw14NZccjJGCPA9IPRnV6DuQoo/IbXoiDIftxNMeDAGd5Oz'
        b'0QcZWjvehE95PnlImiWQujw5W6RFjWKKFgLgf5vwQU+IvwFdfQB/KUP5A8yX3PDhUNwanok7UuXpvM4XKWSSh03JF0XFonY64gafUQzg76yfjSpafjpUwI+4KBidxgfd'
        b'pi0kHgvwh5sFlGlMxSeCB9TIMWHTpywSRYeV8iR4qyJcmSsnrKsLSl5i8H1DDZ9ycnZQXuZ8dDkXtwNPX8OOxmd96DSsV0YoF9FZAL34Kj4NoMVnxlKXAL8pSy1H0L3w'
        b'pv5pGIdahfgW3h1AUWSDB8gLB71VwEYZdA/+5qFWWhrIzLVysqYVaVlQLk2ONgZECZlRAAUdrJoWHr4PR8Tjg4JZ+Ah8vw9/nu6UNLPVuNG+bBDeE8VB2YPCysm4kT/5'
        b'fISbjlsBRfeDespo0fF6esgX9aLtEiUQsAP4QZitz75DBatwdwJtMxyfx6fRLgHeNpSaAdCzAnrmaig6MyWUv64LEIro6/gMvhvMMqPRTSFuwcfxZTqX0z3xFXxQhBrx'
        b'eWjuOfhbg7bwhPG5iUCJW7kGdJNhKpiKaryX95I5mYiuKuXyNHQpOJ0ssqGi6FkCoMTnVXQOxxkL8UGvmfgY1HcD/gB6d63uNcdAVECdoY7HUKLQIYrfaA9+iHcYvb0J'
        b'ZWpaBesOX2bRcYpdwRkeDFQu/d+gIp1o/QyGOoMGLtTjVkEQBvWgiqmaj7opuoLYdT0PZLZUchy9zYCPKbPltJ/SUULcI0D3qSVT5zeJ/ZUbJiKS/t3VWQYQIYghAu9P'
        b'KUYXhcHJ1JaqWa598EgvNP4TxFrhV5dW/Pot/Zs5fuL3pr2oPBhX805Oyorfpbz1j5uzlMdyjj1WvvVsdaT/Tvnxlz789Z33N34Y+qHnC41/SUhm3nj+i5fPa2qGTP66'
        b'vjTqiNEwc8ri7VmC3zXuODzEe9HnP+/bkXtnXFLgvJgFE/ecvxFveksT/vcoTf6INx5eaFs69W7Oo6oPv/0mo+eNofNfvfry8o/Hxk9QF3SnJI8ZEt8+scbz+5iXN+W+'
        b'c8u/5bVZiYtvNb+WcqvgUYuu8bVnts/90/i3Lz/2e8v9LY3m2ZeOFHws6rq/Y93i4fP+PiduarLU0BP3/vgufHPGgrkdKR3PTFMYTvzu41MvnT9waPg0wbSKjw69VP+S'
        b'KFQ5YcT4fW0lpcOGffr10XeeHx6+YHfJG3/43/85ZFgS513ywet1Y3Lfee8jw2czz/11WNDM9rO/MifWeBz+dc/LoR+5pxRkhvx1X/3bw2o2J6x4p+1f8qXSafdDpqYu'
        b'//DSkmmzO5bhJa/0jt1T9mdj+N//8u7rMYV71gtWKv4q/aii+xeVwf9T8XH0b4O/yX6gePPq3psr1D7razqrmi+3e69LeSCLfban9e3rh3f8ft7nbVu/6Ks79P4ajff/'
        b'7PPxXTVmbPq/T356b876sK9O7YybOeytnvi4D8v8Z17VF74U/u/nhlSul3114UK9/MtR6ytiHvZO++LnM45d6Hxm5nqPrssBfzLIPlc3bI/5W1LGqN9883ffSSmfjFmP'
        b'ZEOp20BS5fQnvfN5lwG0G58ibgP4YRnVsNH+FN9QYk7n1maiA2ymL95DPRcWoDOA361Z6DA+D1qEmBHOZdF9dAhv4g1rTfhIBGr1rfYy4Buo3bfWG92c6C5mAtBRQRW6'
        b'kE5NxEa0H932ROfDUq2W3CHUxHtXAOt78wZqmo2RoevUNexIpNU7jEXXApdQF1op6q5AreHUgRYfGwcSJj7JoVYQ1/fz3rln8JGV9DweIcnj8DbgbpmcGj2LLtDzDWgz'
        b'Op8MCwpGB2TnQC0724y7qYct2jFksc3jzID30SPYi2Kpiyw+g+7XA4etjaJnrcnpQNwzjCatkeO7vDcHpKBdU4kzx6JoE38c9DY74G0Bo7yFErwvhU5ZNeoId/S8IG4X'
        b'xydRzws5Osq/D+B0RraD5wXDDPHAJ6nrRX2oiWyG4fvovge98X/vWLJ/QbQY4trMGzeZ0GkidGsUvkmP3HnhSylP2D/RdRZyUfsn7snmp/EW3pkQqkAdZU+cFsyZwB8G'
        b'ARp80ubsgZrciRBBfD3QHa2zy+9/tDNon0Cl5s0zJobpN89sYBTERVjI+lNvPA/qOuxv/eX82QG/EBfk5sdOImey2SAoQf69WAkXxEpZH1rCj/WhOf1obj82gNTONXj3'
        b'212gLw5eyMSv6scedeP4Uv22egAkc4HYfgjS22w/G5k/BDn4JDv0wvkuOjXr8S9wYppENrMeSy0TrvfSB2zcjWWetEzIeMvEnCoqDTIRCzRev2KHM7ytj4q2B/DxISDf'
        b'tgAPJhWMHYF7eGH4OCgmt9CuUkQs1oFMIO5u4Evsxl3oXDS6hDdClVFM1Eh8gTYyIpPqFRHvLa3LaCpR8XLoK8Z1xCay9GeT1476b/eRvFTmh7YTE4SQsNygOKZkBD5E'
        b'q16KOz2iY8TkOgV0D19kNPjEBFpL9DgxfbXJzyT1YVcMpXzVK0YOoS95yRnXELa+ZiEfubzWm76h5dhitW79sMV85MEAyrwlRenVujF1CoZ6FBeAZJKXCRLcIiLqimpn'
        b'ok6ilW/HnbSPCcOmRMfg2xHETjKJQTuXoKu0LiPItMTRNqJGPWE9U2/RHG6A7nsdXUQ3Jwj5TdCH5byk2IUvhuODMGfHANroFvyNXsinbEd75+GDaUCoIPAs/FWgZl4U'
        b'64xHt/AugRBAKmdAzLlLG/7FaqqOS5kx9V5N80bzptqi0CLQmveQX1CB8DbUuIxBN0vwHr6NI2gX3oR2zcTHoa4xzBjo5QVablm9n91mpwS11gAZTieiOKGJaahpaR4Q'
        b'xYNyIiKxuIv1R1v0fOeacNvcUGiNPwAjxKf46Jv4LMiKFwuI93k9U79uEm+yaa0SoosTcQ9H94DROT+64UpNth7NwSXXIinmskuK6IZqr5HHoGq30rCaeZn8LuuXmTyY'
        b'd8hMumujR/CRGSL+RTw7xhrCDOvL+MgipScFMyOv1W3IyOYj3S2o47euRtfoUcNHvjqen8tZkyszBOO9+chTk/jIHRMbdN+PKeEjfznDkjNF41W7vIbRin/zgdAI7Icp'
        b'HJ1f2ZWWJYj0m3fx8WslZVO21BdM/F3PnOUfH5Au+WbhpLI3XwlaPHxhuNHvBXbphKxNCewHfmuTMsvHD7/12czfn3slpnflcWVvetGfdj4ztSPoF4FLd+dMuXblw1fO'
        b'/eoLv6/Kzzx/cfOnv76iz1V+kfNGxl8vnHi//eKXvzv3WduqqE/LR2lWNF6aV3uod+FLH+25kdmw8NgvU7s9z2648ODXq+7EJa58M36/fMPZ3778zwWbNpw4uD636u7j'
        b'6ws/2fm3VGFaftr/ae864KI61v3ZAixVpAhiWwkoS5EqYEO6Lj2isQsLu8gidYuFaBRFURF7x4ANS1TsWME4ExMTk5vEFHVvbtQYY0y8RhPzLPeZvClnl91ld0Vv3u+9'
        b'3+89V2bPOTtn2pkz830z3//7j/7a95xXa6PDtMmTt5/7+pEdb23osufjr+xYketW+a9GyTLbytru/e/mf7AvymuXZ2xraWCw/0L/4GM1G3/t/XDZKY++c8CAacPzu22M'
        b'yv9wR83VgB/Ot9m7Pnjc937XyqOzPv318Wz/0vkLTvY6f+H4N5cm/VRb5nrnzT8FEpEnsSAEy8CGsbhjlZsxu2G3jyvBbjJNycEeSoGUEeSPZ6jjYCto44L1YCE4TCZ9'
        b'kbW3vhX62GAMjNnpSX7zhc3R7Waco7lZXBU4CyhZUASYj/RoNOOmY60Uuz1O4zAucUkKHmielUvEGGUWkhjgurQUAm9fwsEYIm+wQ0z3tTfCo+NNiWP5cDk14kTv3Wki'
        b'YAyE2LMWKkcAXoRorkzggK2TFKSEA/xBFUq9RYxtVbSGKmmzSAkHxiEprJayGYF1fTPoyma3cfweaHBsJKJALlhJUtYC+snykosv3IxXYfaDozNIJgJwwgPUjod7WBkH'
        b'CzjusJFYmMLTJaC5owRTjz4N2Hj0WBiRJqRgKZcgPokkkQeaWGECNGWRso6VqIwlHLgOaaWLkYhTNoz6mGmEC5AQVxs8MnDAALyAjUoK9ybCPTy4BpzyJvVJANsBS3yE'
        b'TV0Po0FF39y1ux9FHjSB3eAAibY81Yrhc8eBRg5oSE6m5rmHQP3g9p1/AVjpAc5wy8CW7sSQaDLY4gNqu6ZlWrQxiHmDmBEMRQJzi1ZYJZIqWA1bkbSKlNVWKrgdhPuR'
        b'GFqL/UWYENsC4AEkufn5kEZ0R0LoEgP72qWlvkjiEsAGLdzioEjPwRCs78sFTQETtXvKndof42OLPSJ25RqKXQoHDp+r9SngRoQuN/Tphj6e6IPPnYh/ATcSw4X9wx+t'
        b'sxwHrh1HyMV7qQ5cAcF/VTq1Czc4YzPGbRZAXvq2bgdQcN+EPLXWYDfNKEuUAqGdREP1n+i4mSSaQf4rVjFEdn0xuitD5GHMkYoNfRVYdKXGv8QqGBsEawRaM1HtEd6h'
        b'IgaWFJKFjbqIGQfZ6SfbwGSXUOOQkxU3Ki49Z/T4rKRsDU8pU2n42FuAxp79ITtpdDYRKklL0Lb89/1PKDB7WyBuVlx8Ac+5a6dwWFZOfCdHJ2s3gbON1tOENekJ1gYf'
        b'Ox7tIfSMa/Sr9uNs5cRx43kmksUoHlLhVmhNiI6SARCDSJ1H8yb0Ay0G29Ra3hZljDFbLH9tF8Km2kX7Le2vO7Kps5H6IWEagy26FGBYjL2OO9ZB6ljNSJ2kXVjuWGdy'
        b'3pWcY+5YF3LuSs4xd6wbOXcn55g7ths59yDnmDvWk5x3J+eYO9aLnPcg5w5r+QUMLpW05xbuWmsMgilylPbqzhQ5YbgIe95be+6B/jZwl3OkIhZIbkM8LNnXdKlxLrCV'
        b'CqV9KS8s+s2WsLzypd7S16oFE5xxa0h96jg1VIlwqHFEKgRhrEXxu0r7EHsPf5YBNjUj6dl6A+z1aC2RKfqJ0r8K/TApCGZ5kpRKcS+XG/NNGpz4j8YQcJbWCR2V5SnL'
        b'ijHhNEauY5e+lDkTuxSWlauoV2sCYzfytGwermmjsWWZyjDND3tIdpYF1PMoJvyRFkzX8KaVomslMqlcXYKuCcpRbWaUKaRkkKBmsfqUsYZurbS+w22RHmbH7hXb69xa'
        b'vYg0tlrEv/mQ11nSWNzWr0wa+2LO2A78sCZB/K/IGavX/rpyYO/jFkqBfjZXhlKhpLi8UBJkqiiDhPmFKMt84uPbMoWtZQZbE2y1L9EiL2SwRV2PukNOTH5DWCzJw2Tp'
        b'6FDfw7RogJHvZsrHZrIUhkUnbesXptcUJgrPFgR1/xfw55rjyjXt5cEcf24nuXJNJtrOnyt8da5c7StOm52eCeVS9oGFv+iBaccF1gc2eyZUyKbKlaiF0RiFhjLSnQKF'
        b'avaxqUuxL+qXpqTtQpdgQkSUklaYM91hMVdG6V28J1hipMXyJOGMBcfAWq0r1IWxDs5wGWgjia6Pdmf8MBjCtWhoGncKpXwdBpYgadtisoTHRZ+NthEsDi13gDsLepN0'
        b'J1RQ9fpdWWnx6JhQRo2x6P3AOXjSKF3QAPbStPWUEH2eW3ASLLYH215jt1GeeFCO2pUTSwN9p6QwxLkv3NJN1wyoaqcMyiwOyNZPbh5cYQvWDZtEN2X60PUCZlJF4Heu'
        b'o2j14aKecLtRMeGKgVmU8bZd3zMqZYs92AFPpJJ0vxlC14ucRZUOdhJ/amMOm1JijZLN7UpS9dPqNAZJngb77OHi7nCPXLbropVyKUri2B/Pgz6+5Bgf6pD4efTc4X4L'
        b'4n+s4l4dFz90+mI7gf3YBNGX70nXNqnvX436tPcih4pW64PNQwasGfFWw5S8iosTZ0/YebOFPwSGldy/pekfaZsel1/oX3/sTtcbC6fccPyjakZl1Zi3in7Ozl9yye22'
        b'x+33jxzMfHv58V43hj+LflLxbM7mCSf5rc85l3tEnT5qLbIjGk7Y0ABWx4Sr4fZAPSVTDE+TGO6z4ukSeAyoN4AzguNgO9Uh6+R5oFY+O9Ogd1kxfeBGPtJpToNldHvh'
        b'HdgcqKesWiHJj+qrSFflwZMq1ovjaVBHMOdg87hAlhmXb08U6eED4HytHq20gs1Ij4bLuhGtLxbp49XtKiFcBI9wkU4oB4uJ8jkkAazWV/aPoghU4Ufq/pDxlKqmDbYm'
        b'6PTTibCFVVGRfqqAq1SoLIxwWCKWW5Eetz9QHIRSaVGSxQskyaYRKTbImkkH1TbgbZ/Yv0x81yEj8Zuip9DNZeIJ/S3Hup0Kl9LiEk+mujMt2ywSOMwQ457EwSkcnMbB'
        b'GRycxUErDtoY5sV2sILOJOJoUCcRulGJn52epjePuWbgG65jyV+IeSvQYgh1opIF3NsYniFDLs5JjyEXX7LIkNs5QGWBlrxUT26yUKhx2kI9621UAiIHvBI3LSshWch1'
        b'oi7XPjTXV2fmZevLz0FSkYUcp+hy7EFz1JOdXiK3am1uSPSxkJtEl5tfu3gkMcarviL3r1YYsZC/VJe/F16/0JNYXilHrcRiIcepBjmi9tVJOfp9mEthzmR9Q2dFm5HP'
        b'YwuCrc/x20rMaLGlP9miwg4fuKx+ake8/zoUOOhs0a3M2qLzSBX4v1u5dJpcSYZZJDvLrUQivwy1kj6VUockMbWSDonsHyj01wdEo3OCsEaR9IlhiNRKi4H5Njqv2eky'
        b'GizMLivB+gHVp7FXNhbVLMkrU6tYxiIlkkTNtQ3+h9lBZLhJpPICwh2jYiVtw0qx7U28TKJmm8r6nDMh5OJ/Yh3XkcSS0hYaqaeqCP20hCrmlRb9dqUCeYcXU+gXl6eQ'
        b'5ReWYi4XVoMjnudMFrS9HyiV8qmlpCtQxpQOtF1KoVy/VnKkzEw1Q8uiVVJCyUOOHKTTVXBOoaJAvAKiJfrFMXRMv/nm1CvSK+XkfswehdsuelDn2acKDCuEay2XKf86'
        b'7ig/zJVEWJ5EQn//EqxAo+rM8vd/ZTYpoR9hjgqiBEwvk7QF5qhO3f+yPE5CM/xT5nicBnSuGAZYDotsTn46NqdQkXBiaJh5NiZ9PAj7GNUyWh15KSko4V5PTE8fPx7X'
        b'zJTXWfyvXDKrhPislSnwxBRIqNp0eq9egcIsF8gixZThKgh9W4K1b4rJYlGxR5+YCmUfHmKeY0wfPaNdE9J7TdBV9EaWKuW0UGUFpim7pEWoZ5D2wDcQx72Smfi4k2xF'
        b'+F+cQSJKshwmzy9UyQkllbKdMK3jO2s2zSBhKKZ8lqnR4KpLAPVguZBtIjRClaA3LmlM0GiJKk+GlxhNE2gFCVF3oW5Gi9Ul02SFpts/SBhuFI3kJlEXVKpVMjRzYKfN'
        b'wjfKFEpSKDNpRAwWxqkLCmV5avzqoRvi1KoyPL9NM3PDwMFCcalUPl2OOnNxMbqB0ropjWpu5u5IU0V++QaKMpWMXK9YJS9XrGhT6b1cuwwiDdne9C9oeZMXR9OejNcC'
        b'jcr90j1Rv/oFClQbP9y2ujJJ8irVU0Xmu5/+7cIoX/Md0CBi6CBzMVE3Kw3uyJhJfxxonEykuWQiLSWDOoWufhbSiNaPZrZqgwwSM1EvsxMai+5DIxx7ROQBJJOisVU7'
        b'lPtl0znW7ITdDh7ElO1oKqRnSMbxS0WnslL0h7q5EM9B0RZY33WwQ8NkwoySCbOYDEEoGtAK+hEuwUQ83ww0e5sO0UhvTRpDRmp8QeiHXnK2i6PHbr4Z1ApMr4hp69mj'
        b'QKGebJc0ZpTQbyzcWahALykqS4T5ouiBKdsT011mC6VNSjlNrVB2LJQlcc+ceElEyc5LfjoRLc5gWb9zMgyBfw4WZuAv4cSwkMmdvy2M3hZGbjP/NLS4UlaEZM+xsmyp'
        b'HxDQKboFf6GIHeOZH8VGyhSK0uBkhUSNguIBwclyJN2ZH7VIdPNjFU7H/PiEMzA/QFnKGY1KSYVICENjv/mhiZQNyWxS08Uw13hIipXJVFiywN9IwIq0KN/llc0cLMSb'
        b'xEh+KsBSK7qA2tz8Q8U3YcwvvUtSLMQnFu/Il6vwC4lCi+IehTjjmPSAJByI5fSg8NDISNTTzJcJY4xRgfCXxR5ZIEG1TUaDiqVIBKWMnhD+Ek6MNB+RHea0zKkWerQW'
        b'Pz1YGI+OqCQ8MSzKYnzdq01uMdy2s9jeWlQ2eyd9PuYHa4zGRiJafFwGejzmR8Q8eT5KUJyAsjbxRhrgqjtaL7NuhwYFEetlwRDr3MDKca8zFNu5ajbcmwqXdXuNAuF0'
        b'KLhV8CS567VYQhM1sik912GW/0SGQnwOwuPwXKoY23OBBria4PMyZeSGSyMopDf7tdxJ69J6sKDjBtAaA9dYlQ4nkD2wJIUYDxeAU7PbYc+M/QSb2Rj0vAXOJ0k55hKr'
        b'58KmwZIh6zljGMrFuA+c8w5A8TGbYCY2FgT7U9KJ+yPYCNpGY5dktaOYmRG2U+FmHwISEkdnMv42WgbFdfaQUWPP07ZZcIOxv6MToInulwWKR4+kuxFv6O/w1YFNDqJU'
        b'0CovPTabq7yBUvmm9snC5cOKMEPhnU9S9vVJ+Cj38d5lK264nnS8Kh5e3LcqpMfAyFFLAxdV5Cu4YwdNvBh6pH5Y7NKqm61R14de+Nyu2fmN+weuB3y7Pq85a1/ghaXH'
        b'HO/NKDr2dVhA/KgpM5N6LXEUzN6xs0x0pleBV8POZzuejlSOGrH5brT0YO+6CE6fjSO3LQwP71f4hfuc23OPpUycd2zYvw4eXpuU0rA+RXNy45ndjUvLQkMlqTZeX1vV'
        b'tZQ9jyos+OxpnIfr7lpe666G1+fc8fD6bkvv3yYXjzt19XdrH9DPNebmlT/Dqxv2VpybMmLEyMzjIgHFhezrnc7iQiq6scx8JaCK7Dflw5PDWAI+uA68Q4EhxwDrRX4e'
        b'bHAKgEsyxWA/9oHBZ6yLud65lG4J1IGV8EQHdEiMO18AFkymHubeToAHqKGT+c2imWIb8LYatJGtNJUIbNXzldQH7mdTpq6SRsJNJO9CsHeuEj/adrK+iK6Urg/Usl42'
        b'1klha2qamMNwR3F6Cfwnw5aOsA6Hv8jvN7ZZI1tUePvVYItqLpMpIJR7fI4Tx4d4TMLH2H7Qjt2e4hLrQy/03Y3jwql00G3ESKTSDAN3He0L1dh8XG9PyvalCi7i6yXS'
        b'7uNTV5MikxtTG731N6YMSmka00G8L2FrIqaGr/O+9CLSooL/e6RFfJMjP4tb6cOj1vchkSs9d00KoJiHYfJBSjVYD2swErmOz6A3gzMHrAdbKKqFQOBqwAZ3cNrPHj2S'
        b'scxYuBDWEGCDTyCoyh44JiqEApXPYODG+hSS1U/2FKhyKN3a71ObrnT0f8sZLA2PcISNBJPCyPJKSPIZEfBUOPqbSRAsTL4rpO4EHrpS64YQ69DgTFE3Cj5ZkkcNP0KS'
        b'P1POTJtBL/aaRmEqId2anS57JtKLa22o2UFIZDhvxoSR7ATUHAuawPJ41pM8OBxEaiIB9eLwEHjEF5MYcuBOBlaBEzSZGLETg2ZIz5A3dsUllLxJG22gCuzMTk8A29oB'
        b'LxxwWg1PkAq5zLUNZ5EujC9YjUY+SlwIj4BVqXAlPBROoT6Dy+nlQ2C/Z3EKXEMRKiJwkOBrZ8LWAIxGAYdBjQ6RwoDjoIoW7HllMXMVV9o1eeYV53CG3ASqijFznNiW'
        b'q4dG4abAarCTYEUo9qUvNfQISW6Omz5ZRS/2nelGjF9CpgzKbpvCgoKC484z8zhM9KGRvh47PCrZWb+hH6N0dAOnwlEduWAfBtwdhrsJwOOHPuzjsQ5xF6izKOqjKoh9'
        b'PAXJnEsKFb0YMFP7eOzCEjOc6MWs2ewjnz4gOd8pl83vTBDckJ0FDnpkZaGnk4gqiR7PPuq+owUsAEuzsxhMRbWLSQGbYRU8C1tZRwOxg3U/JUWimxYPII+7MgOsRgmu'
        b'Aet0KabC46QEgwrZtrHeIHZ9bTTtNRMT3bNxTAYuYAq8JKCRS6vgzlY28r74yy6zGHll7Bm+cgh6jC6nepasOpUBY92Srvf44Fqvi/MTQNvtAL+njI+d/07B5K6hERmF'
        b'fveKqr+/3LjoCZP4SVRWef+M7W4XL198/HH9jOu/Bm762OeL+Ou7wrmnDud99WGd27Py+k2TRt16pA5b8bR/xraED+d/Oe7WHsll4fpp4q+sBcVW7tUND2ISf78QuGuP'
        b'74o9dz46OyZiy+GBDVO+KuGl/zCk+mz9qpUR4gk+IwK+mxy/e2fJ5VtBmgmjfjgvFke91Sc6Pebzaz+WbfEdPrqkh+TK3c0eR55cmLVNvG5n9rfbzuxX1JS2pfzSff0/'
        b'Ppg/wPvRk99/mxcaM2Hrt0+Hz+cM8DwXtfLaxnXTuw5RvxO24herhInivWHpg25e2NDodf3x1U9jlJPWP79RNC1+zZg7badjki/9lPz964N+/qq7JO3cM03w7YaTjbz7'
        b'yfd3Pnxk81uGghl4UOSmwuKdPdg9F832cAc8a3HGR/M9XO1FJAxpHGgMSO0+BAsR6EcBPMMFq7LgAopZPejULyAlE6xLT+Mw/L4cdNsSsIbcNzcBnkwNDILNemy8s+Aa'
        b'fwr9PI0GtX0YFQPqK/UAuLDeiRBegk0MPKHn7kENt+qgxMIkK9tRoJFk8hYaUuuwwU5LIgtdwQY3O3IpwcMRuL039bE6BrRqoStgfQmB7bjnVmihK8SkaByoZ6ErRzLJ'
        b'7b5I9j6AadtRs0iH6MA1Z5KIuU4R2IktxDPfSDJCtmBUS6MLxQGfsVEiyS0TntQheqVKIh1NB2vCwWnwTqoBqMUJLODFw3nZ1D9kPdwGm4LB/nZQC4togUcSSYy4rmAV'
        b'trpL1Qe1OM3hJYK9sIq6Sz8E13iD2mBvcNYA0sJDo6IDqSRnnJCYJC3GlJ4EqcIBDaAanCXN6+sJG1JhXVxCO1KFWxaLRE8hHsLhoThy7xK4wxChxAPNYF0/ApcJd4xo'
        b'b+WJYImh4dVwcNSs0zrL4lyZVpwr7SjOlWPxjWVj4zpzKVzAmcXwYjCJMxLneqKrzki8a6emdGb/uCyLmx0mq2RBJs4sbAATv7C0a0SwsszsZrpqHTjesCzX01iWm8c0'
        b'GLpbNM4UpYO5h/5iqrfq/6d66yD9maZ6s8lQE7TgGf/SdqI3sBGsYcnejKjemllQK6FMP02p22JHBbLMbf7wEHHWgaSSjdKAScUUuArOuJCJUgY3xWLmNkzbdtobbh5s'
        b'J19xK8BKiTWBNx8NHPYJYW6zujG1v9VHjZ7RTJ70eyZtErPSj1e8KUzo7jnYx77gAT/gA1+5b8unR64f9eqSWbTwfuonP9z7u/81VeW4EfGZl4HHfMHxtv4P5nwg/3vh'
        b'R4N3OLvuHc9/UpVbe+k/P161w/b7S+/Ch+cFrj/lL4zoYlX98+HnA4v+bFvzwfjqgt/Kxs1w/OiftxNLciVTFw4/Wrjg9y++3Ozi3nP61VvVz+rnxD59xvm8Jtxt7Q+i'
        b'LiosQOSVgxrUZDNisHNfQtlW6kWHvBqkrx5qJ23LQAIG5WzbBN4mAxKoGQS2UE62iL4sJxvYB/bR0a5+BmjTEbJlwWYdJxs4lE9jnAhF04OW8A2u6qnjfEMyIfU5sBjs'
        b'd9FytsETsFXL2+YJThBNvWQWukpZ2/bms6RtEtBCLDzFYI84NdnOmLMNzi+hk+WG1CJK2gZroljWNpENmQ/7lLkHpGAUtiFlGxIwl5OZpC9YNJOSto1RsqRtE3qTOx3A'
        b'DlitY21DUeoZwtvmCLbQSXBPLlzAEreNBCtZ3rbJqDZETYFbYig21R3F0s7C5aCZtvb6LrCJ8sjlaFnbMIfVX0LbRjjAyBDu33EIn8sEeVtmbsMj4V/O3NaHr3WmPM/o'
        b'c8sEh5u2CJY43PgU1EN+Jxg/Ls0cf2WIXIwRfdgWTg/W1wmD1SMM8eaukpUoKS7PiF+t67+1ftKJx9iCuyePXVgRWPO5aKbldvPrPJ0afsCeHOEMlyHUm9MhuNkHk6jB'
        b'RaCJSqhWjKMXF64pgSdFnAy5T9tGnrIHmqO+yA5OWn6mFMQ6J029EvmkKvT9TCE/xndyjDBp5IiK29ZLvCtcRRHjU/Pv7Av/eVxiwPghU+98e6vxwW/feMzJdfvywtPo'
        b'a0MeLZJOf//pgyh4fP/wiF+Pn236V8MG1wJ3yR/STfcmb3ms3Hejx+8HptydEHBk9/AWr+8OP6prvikv8uQ2VLyXmjHzwrS/Rd9Z/Xh2oXf14sFzHzSIv82+afVmXY3V'
        b'd38bUfyo7vvbh18f59119exVFdYDD7uPkty9uOe6re9Dv4ajwSUPC1P752x+fH5g2cxLXe49bPvwcHK/ax8X7ii1m3XOT/7Z1QqfVquPBnhOuvvF5d/+/NRq7L2UwfEL'
        b'J1w+/vmC8MoDn2/acvfYxI9a1CnzV6QvdWxZfW15smPltq3/sgo8WhDoOkfEU+GJI3zIdFiLRDImlBPNwOXjYSMZ5ILAPBeyKtgjyZD+ZwA8TMXvtfKx8G1Y09EnOl3k'
        b'mwz3dlyp6/Hf09NeOkBDEFf7ppkMCAhZkJNTXCaR5uSQIQjDrhkvLpfLieAI0ZBjzXHhCryEbl7+bsPd+g/FA9IwAc/Jvt9cZrrisu7l4mm4OTl6443X/4LacxRf6N5N'
        b'XFI8MVH3wz/G6jPA4SGJD9f6glqwAgvxmXAl3JMGloAVNoxTd16vt8BW+d7xs7mEKyD8j+e9lnxoh141qzNTGz3dz9dtvfGr+A+wMmHjqVlpGdYNz6+8P2iM+7ro13ct'
        b'SfZ6ciBm6MOLCzKKKi7AWWv/uLL44DGXbj/dW+rxzqffZ22/6vLeVy2nRAGvN7k3//PX08XvhVS9m/XZ4pDCzwCQ1Pb6j+gbi13/9uONivPunKhvHr579JfVmRKn7eee'
        b'JVX8wdnxlV9G5FAkRxAlcm3EWDwVZ2bCFfJUQgRtD45w4Z6RiaSb28PaitTMIHgYR8kM8ivkMl3hWR7YBg84UC6Bd3ycaPXR3WCNKB2rwqj2LrzeSEhbSefAJtQ4+8F8'
        b'eCRVnO6fbsOgEU4wHLSRaTkrFb0ltaARNgRbM5xsBunV8wKIjAOrvNLwOtPyFCuGk8rAjSq4j67J16P8VhPuQLgMbs9JxzB7exEXrkTT/VFKHds0gqOkEcBusJfEsBNz'
        b'wSE/UEXkDHt4TpxK9PddfFYxdIJLeRmlCUTOyIUHwRG6fYS3jo4hAanRxp0kHf8aPE5Ig0eiYu/CSCYUycGVC4/Z8aliWoEJDlCEchThIGgmEezAUS44BldOICodtwjz'
        b'fcEjDmDxjAo1PFqRP9ChQs1hPOAKHiHFJTkpe6JHgr1iiGErbEjH/iHtwWYu3A63ziauwlCFF8A63PzBqWhwwa2B9Om0VPwEevjw0Y/b4g08XPf6n3+5jN812xeMNCYG'
        b'nnasDCGrdRRQT1GEpAHrqA68GGNRyIdKBGTE6aPhFctKNXxsuK2xUqnLi2UafrFcqdLwsVKo4ZeVo595SpVCY0VWtTX8vLKyYg1PXqrSWBWgIQ99KbCdB6aAKVerNLz8'
        b'QoWGV6aQaqyReqSSoZMSSbmGhzQvjZVEmS+Xa3iFspkoCkreTq7UAoI11uXqvGJ5vsaGQqaVGntlobxAlSNTKMoUGkek6SllOXJlGTZF1TiqS/MLJfJSmTRHNjNfY5uT'
        b'o5Sh0ufkaKyp6Wb7KEor2kvxCz7+GQc/4OAbHPwdBzdxcBUHt3DwLQ4wI5/iBg7+gYO7OPgSB1dw8D0OfsTBNRx8h4N/4uAnHFzHwT0caHDwNQ6+wsF9HDzAwW2Dx2en'
        b'G1KfJOoNqeS3Z4ICbJ+dXzhA45yTwx6zU80zL/YcKcD50yRTZSzwXCKVSTNEAiL9YbpdpO6ydLtEPtTYoRZXqJRYQdZYF5flS4qVGodR2FS0RJaEW1vxq7bdjEAWGsHQ'
        b'kjKpulgWY82wqwx8LhrAjLtYlBvxkPBfIHfg4Q=='
    ))))
