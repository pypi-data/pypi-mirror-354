
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
        b'eJzsvQdcVFfaMH7vncLADEVE7Dp2BpihCghq7AJDU9AoapiBucDoMINTLKhYEGliw44l9mDvvSTn5N03eTfZzWZLEjbZTbLZjUncbDa7Ketu4vecc2eGGZkxZt/3/f2/'
        b'/+/3iVzu6e05TzvPc+4fmMf+ieB3AvzaxsLDwBQzFUwxa2AN3HqmmONFz4sNokOsNdwg5iV1zBLG1nsex0sNkjp2HcsH8FwdyzIGaSETWKkKeLgqaMrEoqmzlVUWg8PE'
        b'Ky3lSnslryxYbq+0mJXTjGY7X1aprNaXLdJX8JqgoKJKo82V18CXG828TVnuMJfZjRazTak3G5RlJr3NxtuC7BZlmZXX23ml0IBBb9cr+WVllXpzBa8sN5p4myaobIDH'
        b'sAbD70D4lZOhmeDRwDSwDVyDqEHcIGmQNgQ0yBoCG4Ia5A2KhuCGkIbQhrCGHg3hDT0bIhp6NUQ29G7o09C3oV9D/4YB5QPpdMhWDWxk6phVg2oCVw6sY55lVg6qY1im'
        b'dmDtoEKP96VM4HqVKK/Mc445+O0Hvz1JZ8R0ngsZlTzPJIP3f8pFskSOvOkUz/QZxThGwms6Xouv4BbclJ8zAzfi1nwVbs2aVaCWMqPQ/sypYnwP7Ud3VKyjP2TGt0vw'
        b'HVtWLt6EN+bijSwTlMWiVg6dz0lScY5IkuNEllmbFZslYcTP4lYxiw5CBTscpE9V6GwPkqTGTVBawoTgZpGiJA9fzYKyg8hM4g50BrXg5thq6NBGqCMIXUK30VoOXbbO'
        b'dQwn1V/C99Igy0UFaly62IGeRyfxpcWKxQ6W6Y03i9DGMHwc+joMskYtw+2oBW2O06qjSX/xZgU6SSICmP7DxaiuH95Xxj4Gnv1dU1dJ1lFYRebHrWN5f+caso0Axqs4'
        b'WEOWriFH142t5Qo93n2tIelIZLc1HCys4eA5AYyiYA7DKHU5h2K1DI08vEzEiJN7SWBhTbWcSIhcMkvGhBWNgjidqS0/XohsGCVmZCt1AcwEnakxcSzTwZiCIDrU1Lda'
        b'L78/gmE+GPUldzXhjUGrGVMgJLzN72bPB2zJDJ2gS3zXmhYQK0S/tvxvodtDF+uZgvfZ7+f0nMsznYwjDhL64A78AixeS9yMqCjcHJepxs2ooygqOxdvjtXgBnwpS52d'
        b'yzLm0MBx+GZktwWQu8adKSyA9yZiyPSXy90TzD3VBFf62iTSbhOsyLOSHlAonrYUbyucqZ7NMTCbaA2+ivdHoA5HD0gagOpWF0INwwY9wwzDJ/ExRxjErhwSWzgTYk01'
        b'lcxUfHqeg9SNr4nwZdwGtcaVo/VMHLqT6wgn8YcnjcVtMHQ1zNVVRm3UOnpBNDrXD20tzJ2BWyUMt4LVDBowETfSPYrXoXY92RIxWoDjppwZUagjNpNuUg3smTvDJGhd'
        b'bhZtE21AV6PQJRjeWHx8OTP2OVxn5P+xnrPtgsQ3D+1Y8HpCCIpX1Ot/m/Xb9ft/t0Z0/tJLkrAYmfRUxqx33qyP3TwvOXUEG6jKGXT3m5/ef3/ovXen/HHQfeu4n+Yk'
        b'BcyueeP67A3yy0duTe7fZ/x/XZ8RePt8vytZNSdvv3q3PnTAZz9bJ3316qPis/2r2or6/6x2/fTCyNV3Xlz5cN73sZ3HDuZNGzj72H3Vl22/jpvyaaTmr03/+kK6ZXbK'
        b'mqzhKomdIFQe7xupxa0xuHXIvFx1NsEh4fi6CDeMwKfsFPu8gOrwCzHZatyYlZMnYeQjROgCh/fj/TNoeoVMEaNRZceg/QFOFBOK14gsqB3vsBP8gjYq8C45mboSvMsB'
        b'WKE5jmN64JsidKYEb7T3gSyBaNdKmOhmvBlvhD01hrUvQxci0AUV18lFqawEWFRy+uffeBC4exg5ttxqqeHNQEsoldIAheGXjO8MtvJmA28tsfJlFquBZLUp4SEbH8bK'
        b'2CD4iYTfEPghf8PhbxgbxgWxVqmrZpWoUyoU7gwoKbE6zCUlnfKSkjITrzc7qktK/u1+q1hrAHmXkAdp7hnSuQh4KLGU41gpS55iVvo9eTpIr9Ex3LYiqjYmG7dqs9So'
        b'OQ72/6a4bJYZgS5ISuJqvLYj+Sd2/qWIlyd8AfAEBrZYBL9iI1Msgb9SA1ccYAhpYMpZg9ggWR9YLKPvUkPAellxIH2XGQLhPUggweUiQ5BBDmE5hAGTQFhhCIawwsBS'
        b'PiK0UzqTzlgencFPvoc9WSby6BYZcoALU6QxLtoOFQkoSNQoAhQkBhQkoihITNGOqFZc6PEOKKjcFwoSdUNBYgHHp/cEJA2zGz9yYe55yVjG+MIJm8RWACn5p97+TPda'
        b'6X3dNkOj/lPdxorT/H0IF784H5/fklA/Y9+hnT1ezte/oDdJTrIndf8l3ho7UDE1euBG+ZyMNZ/26Tuzz7qXdicFMxdFd7f0iJj5ikpqJ6wL2oU3pThQY4ybVMZImVB0'
        b'XFQzCV+1E9qNL+CdSldyCr4FtJZRxIoCZhXTncejteO0uCUHWAeVlAGOYr8MNXPL8Hm8Qdi5B/ABdJ1gMHwMb9dmoTOAgdO4vqgp3d6blM9DHaglH28NBv5AzEjwPhbf'
        b'HLXE3pchSHIL2hGjzqRMBbqukOHLHFqPN/RUcR4wKvK12SjIdspKSoxmo72khG6qEHiEFcPmAbgVwzYSP6oJFYBA48onbCdJp9jGm8o7xYQF7AxYwlttwC1ayQJZCQ3s'
        b'YF0tkyqtweQR6t4nCnjMc+2TsBPd90m3Vsu4x/aDG/BSnIBXzjnBjqOUTwRgx1GwE1FQ42pFhR7vvsCO8QN2jlgCBfvx3Sly3ArLtAkIOLqK9uDNhZnCss4ooOTwGXxI'
        b'2gNdHmisTesjtsVDqTevmD7TESCMKov9UKPP0T/QhZVVlptKxc0Jat3nujmv9HntRWvhnhDmYJLMvmmOSixAxF50Zr4LZJ5F56WMADFN+LSdcG/oGm6D9i9BxGa8WaPG'
        b'90ZUOzF2v1oxqkfNsyjCTlGkEcBpQxs9IGcJvmgnhDZntXVKkTZfzTLcEnYi3ofvCUvL+YQTQJYVvN1o56ucoEJwXVCpglWwNeHuxXJnEaoS04XvFJv1VXwXbFjDhGbC'
        b'3ZBBgYLwD2UuoAg56AMofLTzv4KQujGdfiEjCt4T8I0JXYDRBRRWkydY8OOMI4YrRLZEKPF6+ue+oeKBjmtOdMS/HX+05sN4cVL1VYY5/blsydgVKhHd7XgrPjxbi5sm'
        b'ubEJhYuYVfYhJPUIOpooAIUe/gBceAHF/AoKE+jsPA0ARVYs3pfuhgl0Vuckk/4xBUCArTsEVCgATXisjM0bAiTCApOl7pQs0Zsc3eBA5AEHEW5gIDNd6cYQe58IDO4m'
        b'/SOJdAEYCMPMlov/u4iCdVbvDQ4SAVGsEPUnclwRblSrNTMyNXhb9izcmF8ocKWZwKBqWMaO7wRKe3KOaCiQhG5ke8EPupfnA6/ggyLjFv1+kS0Pyox85vRnuk8Bhkzl'
        b'0X+K1WfqTRR6qvWNfzzDv6C/r/tZaWxZ7LYofbb+pD6sjHk10iqauqf3eXt8rMFgyNQ3tcjK388JYBLiQ9d9vQxYTCKnoxuorQ/lAF3sH7qMNwgsIGqyUQhEm3i8x4OY'
        b'HcqjEDhaYR8KqeEj8NEurEShrxfa5wJAkAf2U3oZAHD8AoVBO97WBYP16BKld3Ez0R0XSZszRKBoYrRX5SQpYr/sowCnUkc14Rrd9CzIJKNMooLlHoVxNcFOuBFyeeIp'
        b'gVS5wbPbXgCU1UXMKJQSwaTKBaXhO3xAqXdr3SQ6b2xFBWo3tmIb2X9PghP7BE9RnlEpf1Zsy4aIyQWxWn1mxQMAoP8qrSyP0L8gudCnd7za0GcRAaEW/Un+NM+9qtad'
        b'1c9/Zc5P5+MiXIBNuOCV3740R/SrHq+9uIdlxJGhs8cvdxIsAJQdI7vAAl0eIhCsu+gQXXEWHS+iC+5a7Tq8Hlb8Mm6hK4524sMS3BKbhVtBapM+xy1ZOGwobqb4qhA1'
        b'9yC8kZsvmorX9Z2Nj/iGgychMGD8bXarE3kRwT7MHg5QEQTQURPShU1IFlqqQyQstX+IAC6nCxiIaOxwo6xWH8DwWCMqLs9KRHpVMOHCCI0EoSSopERQxcG7oqRksUNv'
        b'ElIEHCorAzCqsFiXd8qcPJeN8lWd0nIjbzLYKGtFSSlFoRRCac9c6PiJ8pcwEDI1hWQgpJyMEXNiVvgJ4RQyhSRMEiGjeoCFM1Vyl+giU3C90TkdairwL71omMekF65Y'
        b'bBARaWUfVyzZzhikz4O0coitY0GSkRUSxBvYKZ1qBuy+/GHEFL7UaLeAHBintfIG4fUTgZP4hDTxMHw2b61xVNiq9Q5bWaXexCuTIImM6KEih7fX2HnlNKvRZu/g6Kx/'
        b'8hMY8Vd7YFa1FrPdkpEHs6yMmmiw8jYbzLHZvrxaOQuEUKuZr6zizaoMj4Ctgq+Ap11vNvgsZ9bb8W2rSaMsgDWyQNnZFqv5afL5qmwRbzTzyonmCn0pr8rwSsvQOqw1'
        b'pXwNbyyrNDvMFRlTZ6lzSKfg76xCuzoLZDdNxkQzTBifUQRE0hQ3cZHeoFFOt+oNUBVvshHSaaLtmm1LLFaoucbVhtWeUWi36vFBPqPAYrOX68sq6YuJN9pr9JWmjHzI'
        b'QZuDmbfB3xqHR3FXoHQp6R0R35XOjkCURlnssEHDJo/OKxP8piRmaHmzuUaj1FqsUHe1BWoz1+hpO7yzPV45Hd822Y0VyiUWc7e4UqMto4g38eWQNokHbnQRqTfKGaVy'
        b'pSmn8wA7+Gi53UZGSaa0e27l9BxVxlR1rt5o8kwVYlQZWQKc2D3TXHGqjGn6ZZ4JEFRlFMIuhk7yngmuOFXGJL15kWvKYY5I0HvWSMwiAsPqPEcVVABROfgo0ZcsIrMm'
        b'TD9EZk2amEfSeN5aDrgCXgufzZpWpJ5sgbVxTj7dC0ZzJcAaqcc57Zl6R7VdTdoBpFOqcbbpfPead1/xZO69BpHYbRCJ3QeR6GsQicIgErsGkeg5iEQfg0j0N4hEj84m'
        b'+hlEov9BJHUbRFL3QST5GkSSMIikrkEkeQ4iyccgkvwNIsmjs0l+BpHkfxDJ3QaR3H0Qyb4GkSwMIrlrEMmeg0j2MYhkf4NI9uhssp9BJPsfxOhugxjdfRCjfQ1itDCI'
        b'0V2DGO05iNE+BjHa3yBGe3R2tJ9BjPYaRNdGhP1kNfLlegE/Trc68MFyi7UKELPWQVCdmY4BsDEP8pMrUG0FhAzYz2yrtvJlldWAr80QD7jYbuXtJAekl/J6aylMFASn'
        b'GAnHwKsFcjfRYSMEpQa4hoxn8dFKK8ybzUYbIFhPoLEmY5XRroxykl5VRjFMN8lXConmCpJvGj5qMhkrgEbZlUazskgPdNGjQCFdA5JSQPW6npV1kXF1MfQCEEYUKe6V'
        b'4CwPSSO6F0j0XyDRZ4Ek5SSrww7J3cvR9GT/FSb7rHC0/wKjaYFcvUCX6ZwDXwL8CY2z88vs7hfARO7XJM+sNnc2YSEm8UCOKzwiRmQUG82wGmT9aTskqQaiCOkFLO0V'
        b'TPQOAvrR2+xA7azGcjuBmnJ9JfQfMpkNeuiMuRTA1r3idis+WgFAlGU2GJdolNME+uEZSvQKJXmFkr1Co71CKV6hVK9QmldojHfr8d5B794keHcnwbs/Cd4dShjtg01R'
        b'Rs10zqrNyWiouhgjX4lOXslXkot98pfmRmU+0vN9t0b4Ll/xXqyY/zE8Id0fd/ZjMif6b9mLT3uabIAqfWXzIgEp3UhASncSkOKLBKQIJCClCxuneJKAFB8kIMUfCUjx'
        b'QPUpfkhAin86ltptEKndB5HqaxCpwiBSuwaR6jmIVB+DSPU3iFSPzqb6GUSq/0GkdRtEWvdBpPkaRJowiLSuQaR5DiLNxyDS/A0izaOzaX4GkeZ/EGO6DWJM90GM8TWI'
        b'McIgxnQNYoznIMb4GMQYf4MY49HZMX4GMcb/IABBdpMV4n0IC/E+pYV4p7gQ78GmxHsJDPG+JIZ4vyJDvKdsEO9PaIj3Go+zi9OsfJXBthywTBXgbZvFtAQ4iYzCqQUT'
        b'1ZRa2W1WvhyIoJnQPJ/Rib6jk3xHJ/uOHu07OsV3dKrv6DTf0WP8DCeeIPRFZny7utzO25T5BfmFTgaOEHNbNQ/ysMBMdhFzj1gX+faIms6X4tuE0j/GNlQI8U6uwRVK'
        b'9AolZRQ4lSsehbupXRK6RyV2jwIxx0SEYr2d8KXKQgdUp6/igYzq7Q4bYWuF0Sir9GYHkBdlBS+AKZBDX2oAlUcRIyHuRgMt9oOZfdTvgyj5rrt7Rqpi6podJTDfSifL'
        b'S6eynKQ7J1l4T/R4JzJhl6bqIZuR1yGzEr27lWhRrUTVKhyXEJMQKzmd7pTYqk1Gu3WQW4cX5q3NI5r9VS61pKDN40QcK/2Ok3CcNEH2uoOeLG1S4d02Yl/SFIs6xIws'
        b'hUP3nq3tPex/UJ23XhXYGTSxrMziMNtBfOgMmQRrLogd+mre9EkvQZlHdOIP+00BKKgC1oLoS5WC4AMwbATMA1mIMrZTTFggK7EA+uo2RMyqEjgaS6WZVxZaTKa4TEBJ'
        b'ZrW2hihYuoJdSC7jWW2xUihGFGkEfdqMNocQQdI8w8Kmm070fgKDLzQ0aZa6sKzShG/D4puAKfEMZkziTXyFgQxEeHVqXbreE50CUoZrJijDTzhC3rm3XVKbUuCKnLJf'
        b'l5bKKfVRXp3Ie5AZdpedygXOGmhzJiNkoG9Gc7lFqVZOtNpdXXHGZJlJycciSbZEX9kSu2VL8pUtqVu2ZF/ZkrtlG+0r2+hu2VJ8ZUvpli3VV7bUbtnSfGUDJiO/sCgB'
        b'IrTCwhBml6eRid0iIaDM5QFhulSxSodG2aWKhUgBll26UY2SMOwusVvQuXYtozInJidjmsO8iJri8tYKwFA1BKuQ+EmzlMljBDpb7spCdMK+4p1wIyT5qDCjmMoDZODW'
        b'Kj1JdIOIrxQ3qPgrlvikYr4TBRB6QjHfiQJIPaGY70QBxJ5QzHeiAHJPKOY7UQDBJxTznSiA5BOK+U4kxcY8qZjvRLrc8U9cb9+ptOCTAcU/pCQ8EVT8pNKCTwQWP6m0'
        b'4BPBxU8qLfhEgPGTSgs+EWT8pNKCTwQaP6m04BPBxk8qLfhEwPGTSnf8EyEHUgvt+HbZIiBdS4H42ilnupQ32viMaUDiu7AfoEO92aQnykXbQn2lFWqt4CGHmSdcUZe2'
        b'0Uk5CcKb6CgnejE3knPRUkgimLeLICujJpprBI6YHOgBMs412oE08gbgQPT2x5Ifw8PdC3dh8sfTrCZ81eZkE7xSMunxTrkduBK3XEUpiZryOz6FAOdIndQcSD9QGsJD'
        b'l1PuuYoQeDtvhGmxuxXFWcDq2o3lxkV6T+xfTOVAtwLZk80QpEePg0RPNmkaL4gWvLGUJOXAqpGTMZvA2fhn1DyVw9BvaFlvclQt4itdmmxKBCkXpwIuLs8a7Y+HJXY1'
        b't/3ysH1lf3QQ+yd0Ed1V23Ly8KY4ysjijdoAfAjtYnqVihXoMG7qxssqXLysnfXmZbdLt8u3yw3c9p7bewo8bWtAoDQwyBDbIGkIbuhZLjLIDYr1gcDbinmJIdgQsp4x'
        b'hBrCWrliKYR70HA4DQdAuCcNR9CwDMK9aDiShgMh3JuG+9BwEIT70nA/GpZDuD8ND6BhBelBOWcYaBi0XlYcTHva87GfQMPg1qBAWaDMoG7gnD0WG5SGIbTHIcLotgdt'
        b'Z8vJCAPo01VyaGsglNNQ0zkJ9eYIg9IBhmGG4bR0qCEO0iQNMurrEU7TRhhGrg8sDoPYHtCzUYYo6FkPaKWnQdXqclMIaQgtlxiiDTHrZVBLOJUIKlXxnbIpxMR7cuHs'
        b'h3FBSo9/rmilgE4EHySvHB0SKzE6shLXl0+opTdxsviEmmsQsUCl+ITY23xCrZeJtU1XdmuqK7uVWN5YE0gWYvfwCTUNIHChCugM0huWAIaylhgNnYFlgCfMdvIaohdk'
        b'mBITMHr2yk5ZmQO2kLlseaeMGKsa9SanTYa83Ai8XUkVbN9K2nanaOqsmYLRh3UMPMpkHsAY5PylZjvTmMdcpQIbpA1BDQHlQU7rIFmjrI5ZFVgTuFJGrYMCqUWQrDaw'
        b'0ONdsA76ijhZeM0c+ZcldNVYw9uoe5h7vo3UsKGM13Qr0i0iHcQPfZWya5rSnY5hgGKIOsjpeeacL73Z3q0G8i9qEmAGuwsvqTTKiaQ84JAyJbUYVDqqlYBJU5UGY4XR'
        b'buveL2c33CvkuxdCsu8euA89fqAPo3+oD96gka7MoX9JF6bH5bhSnR2z+e4LoTsE4wO90CiLKoEGwA7glTZHqYk3VMB4nqoWwaJEEFahJqUeqoCw0H+lyQL0yKpRZtmV'
        b'VQ4QWUp5n7XonYMv5e1LeXLoq4wy8OV6h8muon6Baf7Xwrkl0pWTnW/KMqI1jHKfNXpoG1X+anFtp3QXtNrci0ncEC1WZZRgubII37bWgADuryKnrVQ6lbYIZwLVCDDi'
        b'xC5RfIVGOTohPlaZmhDvtxqP/ZyunEYCShog1ZUbzbBroI/K5bweOhZt5peSg88lKZpkTUK0qvtUPYWJsULweRhT2yPnIjuBYap1OQ97zWcc1Ek0G23FLbnodAFuzMKt'
        b'2jjcVEAMTTNzVLglNk+NmvHmnBmZ84vRmcy83NysXJbBW9HzCksFPkxrVYqDTQWieIYp0MVaJjuEWtE+eYpQqybysXrxJtyUA5QVNdGKPapdv1zB4JNKWuv1eYEFD0RK'
        b'6ll3MDySoTbSqBGdQDe7nLRQywKoQaOOJj4w6KyYSZkvtaFDEdTJjFZjDgqYtobtQ1z5FNm8mnGMJ9UcQ7fQLV+Dxo1QbUss6eBG1WyPvqEbVnlQHrqId40zDhpay9pq'
        b'oZ5X+lkGvvbTwDXxYVN/kVPbdv9nIbETz4u055lUdkbq0NnPt6smZ3w1RjxI9HH4q6itB9o2JWtS6nOHXh/8ulFpbLnzydALBScWzhp4ub5m1jffvvW8LGpZ8Bfnbxyp'
        b'm/7V+W/qD74QvAhXhn/f5w1DVa32wwvL//GX7Gua8uTl3zNl+qjfvXJRpaAeXSzeNQG1CA6YStxAHEtETOgIUXktaqX2uBK0Dl1HLfk5qvnxXSvKMv1wnbgmO5VWshC3'
        b'pMphSlW5LpvdXqhhGbollq1KscMiMKmzHcQFwHPpWCZyCDqN14rlkfiknVjyoUtD0I0YdVSmmhvdn5GivZwabSunRuUDcSOqhxo81gptxLvC0VkRLOdRVE+NNPF1Ozoc'
        b'o1Hh5lgG7USNUMdpLmlCIbUKNqBT1HN1s8cSSZk4tCd8iQjdQQdxnX0UZKtGd3LJaJ38G+mqc4UZJh7XS/HmWZopuNk+AvKmF+O7ZFgtsdEakhG34s0xJCOuh8m0SYKh'
        b'yRN0/GgzuoKPkbxUtwmtq6XMcrQ3HO0S4frhFjt1nD3au4o2jTah/Z7sI9MPXRdD17fhy4IBZdC/6dnW5fdCrU9Jo8xq6UopSxzYhCdxYJNRJzaI4aQQG8TW9HCR5cf8'
        b'b4IEw1PibGadQB4TyWMSeUxmXL42U5gn2zPLhFJdlUxyl6KV+PDa+YRx2oUyawft9mHi2r2/XjbPrPOXmpeSnq1kFkIgsELF5qnYTnlJFyth7eOeOw9vpbEmfVWpQT++'
        b'B9TyN8FV1aNNV+pDJ3J31uZiBKKAaBjUFrNpuaqD7RQZLGU/pnNBJW4Gw1ffrMQpNwLKW7Pg5eFgoQdCER8deKqWK4WWQ0u82Qq/zfd2N696IuPxozvinILAEhdd99uF'
        b'fu4u9J2kt/FuRuDfb9LNU/trcqC7yWF+2YR/b+JlJS7HNn9tK7va9sta/HsDV5R4Sg/+2h/WteI/wI/46YWXFwL1peMaGLcv3b/tg+CqupsPwuKbkyXUd3dg+D8FJ6jK'
        b'8gfMLza+vvFDxUuKfUbGMHj8IfE7uvsqjrol50dGP4a8x6OdAvLm0F1KJxdpRR50w4W4RQkUdZszn+TVFlBCtpSHPxOzmlkdMaomzAON0QxCmd6P19THvRhz4TESJtZG'
        b'opi1zNqQTh/osVu9qqDOAOfmFAz8pTa7leftnbJqi81OWOZOcZnRvrwzQMizvFO6RE+lUHkZMO6WKkE6Fdn1FZ0SC4C8tUzusQQEg4e4loE4DjXI3VJlsPv2gBDh8oby'
        b'EOeqyxsVsOoKWHU5XXUFXWl5raLQ411wjPrqPYkP2XKiwWAD4YFwwAa+lGxA+F/mtJFT8tSi/ynESyr8UMlFr6x0VPAeAh3Mjs0IApFScHsgspmNt2uU+QDg3eohmKCK'
        b'nMwYq6otViKHuoqV6c0g3JCiIBhZ+TK7abmydDkp0K0S/RK90aQnTVJZgFhY2jRkpEaiY4Nt5qzSKU+ROrvVAVU7bEZzBe2RuxplNF246KeYkWnO0VYShUj3vnfLH2XX'
        b'WyugDYMLJZHySqI1tBHZxLbYQWa31KovW8Tbbar0pxf5BZhNV070oizKefScdIG/YqTldCX1cpj3g74OfmsRtki6spD+Vc5zWt75ze/aSulKovOEpaKi6DxPyzu/Zcnm'
        b'AyEWnsp5+Va7/3zC9oSswgttI1aZVZivTkpISVHOI3pOv6WFPQ3i6cQiddYU5Tzn4eGCmHmenhz+G+9CBUTgFgJKUpGn/bDf4oA8YDIrYWvAdrWVWY3VdichI3BKPLzp'
        b'3pposlkAfnmDT10BgBPJTciOiV4FRBdbo5wiKAzoFh1aaNdXVRFPOPNQv6oDuhkAsKAD1c6tZTDSy4j0MK1LjUDe+GWw4s4N170e8i/PYueFbUI3P2+vtBgAk1Q4qgDQ'
        b'oC/6RbABYdPwMDtlvNICdN5nPcKQyKahmhCbMEyjzaNLGuU0QGouhOSzFs9tR/QmAOrkqqUyEwxYuGXJxvsuqXNetGQpoz0XjlXGVtrt1bb0uLilS5cKN2RoDHycwWzi'
        b'l1mq4gSWM05fXR1nhMVfpqm0V5mGxbmqiEuIj09KTEyIm5KQFp+QnByfnJaUnBA/OjVpzHhdyQ9oKQgV7O5aGJ5H77XA+9BNtNaWo8pWa/jxecSbLwZ1xDLM8EJJ5RjU'
        b'5CDae7wJbcdrk/A1IkQkMAl4A95BBf5fz3fe69B/SezQmVMZB1HMLkEbgrUuyj4DN8bg1txs9cwCfBhdmqmePTOK+Jo+C8I//AGij7ahc4F4xzPB9Eol3DKew5dA9CWi'
        b'YYAIdzASvIdT4JZMelvSYtSBbuNLmpjZ5B4O4oALtUP9ao4ZjI6J8U28U0q1DvgmZ8WXQMjOnYW3VNPhuQdXgBvzoNS64cB0zKqGR35ONt4hZnAzWifHR/GRWsG8ph6d'
        b'S5Jrls5VZaPb6GAQE5jN4YN4R5KDsAtSvN+CL2VBaZYRoV0grl5k0RrxQAeRnvH1LJMcN47H1+I0uAmajUUd2SBJN7KMcrpE3B9fF+7HOYW34GZ8KQ7fDIpmGS6TTVkx'
        b'gU5sdLSUHHSEbcnTxa5armLoXVWoHl+abQvGO/AVoV0ZapXP56ZL8H56lhKFblTagkt74x3BwRq8FV/JwRdi8DYR03u5CJ0eim4KK74/Dm+Wa6AGmLcsMiciphe+AX25'
        b'LQ6djs8aDzguiW17IGfm5efUP8sNQvFhkvdTsx7+/mTMMe1fPhgovoPWHO4f6HjLHIsGHLnTEae89O2yDxJ61vWaPS7+VuCwopqo3zVmOFT7dXt+PTKpQT1j9YtJL//h'
        b'/eTdDxJ+Oj3n7dfeViSfGKOunKz91DhVW/zLyzcOLRg778QbX3/20H5La+mM/n45fveu5ub+N6vurZ9hnvPettY3P5wz9dufx5z8Z2jo89Etf7qgklI9CnoeXZ/m0sYQ'
        b'VUxZjqCMQYfNVDsxRIF3aX3qJmKS8A60U4I3ox3oBcqzPmNCa7opZXAHahfL8F4HvVSkQJHpydainSXA2QpsbW0fWkkO2pYYk6fOysrVxuJWFctE4tvoDt4jTkR3UAN1'
        b'm01IXA5pVy1RmdAXsoSnuOXl+LzX1R8h/+59PH7daIP0BkOJwMNRtnmkk21WZCpYGRvJkqfnj5hcxgN/+7A1Pd3sb1cdAnseLCgbihmXgRu5HsQ6nzwWkMdz5FFCHjry'
        b'0JNHKeOl3vDtDywX6uyqROduotTdRLC7Rb27HcrVG0gVnlz9yLd8cPW+hqUK7FQYiN2fk1PqDBb4X1dQqq+if8kFKnxnoPOwt4zvlBNuBXhEYgom9MQ92LIgD1RMtDFh'
        b'LlQ8k7D2QV7MfQiw96FOBj+MMPjlYU72Poiy93Jg74Moey+nLH1QrbzQ4915dLQ54Mnsvd5tzqcUrld6CiZ2KvGEEHIrgZLCnAF/CtyB3vNWQcJBxCorrBZHNaQC46zv'
        b'TpksVaVGs97Fq0QDGxNNiaxAY4n47zb9JB10S8TdaiIS8v+TR/7/LI94brV0slBCjFvx9QNyidfeFMoLUa4KfDJn837AHNRvc8LeF9pxbndnnMDfmi1EkWOlHKzZN1+6'
        b'1EIYSGOV3uSHA573BINYkCt8m8T67THBUkJ/Sy2WRaS/JEajzHVCl56GlZbShbDwIO37Pk40E3koLSU+wakbI4AAwhypbl6XsazfTriRZLpyls2hN5nozgDAWWIxlrl3'
        b'4zwPW9snioROJOu9DNQLb56nPe4PCm2k+GOCm5fV5/8Fctckfilf4bTZ+X+y1/8FsldSSnxiWlp8UlJy0uiklJTRCT5lL/LvyQKZxKdAphSOjdkR4klmETAJE3Q5F1bn'
        b'MY5kwqnha7O1Wbm4OTbLyc4C+3ouhl419Lg8tRrdCUzWon1UhokExv5ElzxFhakapWJ8koOojfPxlTlaTXYu8LNZboHNXechEIU85bQW3BKITlQNcZADKLRLj3bZ8nPH'
        b'48P5znuQSAvPgkDTiDfjRhCsgkAOgUohfKNwPtqH9qIjgUTk2SnPM4IARPhlvG0UPmXLxq1ZuflaeOL1eTPixUyfSSK8sSZeEFfu4J1oiy06d14PvCmK8O+aLHQmimUG'
        b'V0gki/EaIVN9DG6R42to00wZblXngbjF4e3oCBOeJEKHClPoeTbePgVfgLlw3zlKbitCV2aSS0cTUItkPrq0DG1GpxyE1w+Yhu86O5YVq8KtErw9mYnAR0T41qokulA3'
        b'B4iqr4no3cM5qc8tYBzk0C2hYr5cyjBFzMjFRXbU7EiCuOXsCjmZHpjHrfhaJsiarbgNXyEiaAs6BaEcvCmTSGHz+8p6oo3Tc0DqJpfBDEfb0vAleMlilszPwjeKhOtQ'
        b'z6A6dDWJCuJ455wEJaoT4nfgE/iwcDcrZGLjFlSavn306FHUSPHCFQI8Kc47ioWD+vKigLDfcPSg3nRKO49xTIBI/WINmZhWp9ieGTub3J4clz0LgCETbwzFlwujVAAR'
        b'me7bklXoKp09qTl4QeIcKhb3wLcqCkFGzhYxLD5N7nm9jk+jdXOonUL2KHRZ7lyfmV2QIvOcHbwdr3POEDqLt4kZ1DArcO7gMgdxXUGX8bWZXRLwjCi8o1DmLes+00uK'
        b'W2aGoGv4Ir00GZ9dhRpt2er83DgCPHlOiVeFd0vwnVp0+Rl8z0GESXwOHcY3YoS7cVRSRo7ucQnJAC4n8RF6Q/DS1fncy1Jm2RtGW8/fzlGJtwvmDdDfg/g6vuTUcghG'
        b'FwBeuCkuP3dG1NRwZ42e9g14PzqhgPHf60vv5EFH8O6yGE1WbDTLSNFmLmRVHN4fTDUv6KzRoiVH+DvQFZbhrGzaHJ1KRGcanS5Z6lEIJvNqHFqH9giahXV56CAt+Dy6'
        b'KhTMn00xwkq8YbT3KNHhdHxpZqzxlOW+xJYGgtOWIcsWbBmXJ5qoqP9zX0tKe27mt9qL/3p3zbCjx6cdPn5pQvbw9TsbFx7XR+W8JAnLfFV9v+ODnNuvm6cm/eWdv/19'
        b'+U+m/ebaB9u2tRhutMZq9/UZOPvAL7I/faez45Ipu+ngOxcnfNq76s1H2ueUqj/dOjo9cfLF9V8/L6oMGahpbx8/f5Hh5y9Pe/XXu2bvHl7bq+0/Y+KDzs9YOmBizZrL'
        b'v7RO/ao1ZMbmSHvczbfSjy74sPX+sp9udYR/2/Rp5fL3c4+3qT+rlWwb9H59j7/jN7a+Na5sXOJbRU0vpUsXzb/3Tp/aoLifjk3f93pt0Gu1oXnL8+7/edzKT0/fCP38'
        b'N9MHjw0X5XxXlfxt82Hd3fsrU28U81+9dfNXbZ8/c/hEr7XfvFfzL/6mrWLWpf84+Jsj80qfsU6v+f6DYTXqFRPVS+vGmfZkfbK3edcz4SZz+UfDVMFULTEZn6r01EpQ'
        b'nUTo/HJ0A++2E8FbCzDV4k8vIclBbXgzOqQWLvjdhC/j6156CXTqWaKaEMtWsIIW5B7ahm9oPWw9QmeL8FqAWttz1M5jZS9tTLQGncunlh5M4FwOHUP1+Aa95IvHN/DB'
        b'GA3B8rEEkDZxqB0fUKNmKTUyAfjfgzZoc6LxOtwiZbgFbOpkvJdWa0LXF6JTObmxHCPWstDgNnQR70Y7hCvn1uUSwxG3iYd0JVcSM2oFPkFNN1C9GBADMQWx5j1uDEIM'
        b'QXAz2kgNQeYl1HidEmpWexh4zMU7qbWLFF1FJ2xkd6kJ2aLXot8WASbaIkLncT26KlyheFcn1sZGPTfXQ++Cm3HrE67XUoX9D+lhfGlkQojaoUsSp1qZ2YQ7WE31Mpyg'
        b'k+nSzATRO8/EVCtDQjIuhB0EqREQR2xPSL4wmovkUHBBtCS3hryFszW9vdQdXe0KmhyFoE3hyaOcPCrIg9zlaDWSx0K3hsWXEifgaa5cDhLqLHdXzLtrWuhuJ9jdRJc6'
        b'h3yAoNhTnRN93Ic6x9/4yiQejBc5M/e+j13SENDA0JNUtiGIKmHkDWL3feySRmkds0paE7hSQpUuUqpokdRKCz3efV02SRrqfh97iMDh7SoXTfqr8NGCWNnoWUwRjZ23'
        b'QtzvMiPQ6XhNBCOg8VvZchtqxXfyZItFjCiETZuAtlJFeGbo8ELUWoRbZ+Wi/ZEz8JUCfGVWcEp8PMMM7C1CawEnHKeMDD5nwMcLcWvR6HjYVqcWJAN/JVvM4ueBMpwQ'
        b'PoGwAx9Gd8pRg6tClpFEs2hvBNRAdG6z0Z7Bwv3rDD6QPHYCOkJJU2901TAH3cFH8DGAoZFMH3xPJ5Czw6Nrl6ObWk18cuJojpHWsuiAtJLSrITkYuGyc3RsFr3vnN52'
        b'PmmFkWn7TGJ7ADkiBh6t2jwxW5wQNvXUtrz0T2ZMnzgl9P3csWvPLpibNjmmWaRZ/6uf/O5XVy1bBryYUZz1s49Dhx1u+dfDfyxfOXNd36D4zFGbvggSj7yUsSt+6JGT'
        b'+skb/qzNLOj5673Mbw1HB/+554OzPbfdEf8kuCD1yPFZ8966H/KzwfPP/WzkK2vnvxRYMfzbVZeHpAyMzho/yzL4dUlR8XcLf2IoGfxy9hs7a42/+Ghuz7+1vfLG/SNf'
        b'f5139fXQ4jm/+3n+iE2Pvv/gnk3+btWaBdZ/TFn56cjYxgJLxJc1994zGjuu97+++UH//m0lb1+La16+3/6XldNEZ5pv1F3/Tvppf13DwxRVOMWxi2pgscgHBgIYDh+o'
        b'RIfZWfhEip2sf6glA1AsOoePO9EsulgaTBHsXLSrwgO/oi0jAMWOykZ3KUrMmLnSZWlnKeiOXjs0lHLgU7hlvotS5Yi7jBnR4XnCLdoHA/EJbV4sMHyb8UFbHDopZkLQ'
        b'XVEJakBNgg3hYdwxAogZ2oVv0fvpxYNYdHgYS2kLah+INghXbMdMFmonN2yL8Xmh+atT8B16vT1umos2d11vjzvsFPsDa3UVaMpmdEDraR7LMpHojLh/eTY1JMEn0OVi'
        b'7WO2kuGR6MpCETrdfw4luPhoHm7rRnBj0W4XzcWbw9BeoVO7+kXRW72p0eOMOGr2GDpI9Fwoahaueb4KHO02J7nNwhtcFNeUPF4Y9P6V0egk2ge0xpPSNOFdQvLpaD29'
        b'jv8WPu6+kh9dAJaZLuvS6Wg3ujZf631X8Hh0U6CqR6dl42smwtfhTflZEkjdwllCUcPToeD/1jX/Ltsb4VJ/Sq6OusmVLC6EIGSKlMkl5IRUceTnkZjjvpeJuO9kYu5f'
        b'Mgn3T4WUe8gFcP/gZNy3XCD3DRfEfS2Wc1+JFdzfw4K5v4lDuC/DQrm/hoVxX3A9uL+Iw7nPpT25P0sjuAfSXtxnskjuU6439wnXh7vP9eU+5vpxf+L6c3/kBnAfcQO5'
        b'P3CDuA+5wdIPxENCuEhoJIwQPw8LHqH7AtUL6KI3nQGCbtvWKbHZ9VZ7pwjy/VgSJ7FWk3ezm5JZ3OSMUjJy6+wZQsn6OSkZs1b55pMNjoTu/i8Yf61XiR7+sZuaQnD4'
        b'sru8S5zqXpNTC2Pl7Q6rmaZVKfXkNMFDqfNUmnjlIn65DeqptvI2YmIpaIuc6i+b+wjAqTrypUF//HTAJOjcSHdKl9t5H9otL8Is9Zw8D4t9eqkzMOhbTagF70SbURO6'
        b'QBjaZ9FFkNPRBXRqBmqUMH3QGtEK/PxwShfRxYRhuE3CoD0so2E0+JjKQRHShbwioNmyxajlWbUE5NidWo1GxESgJhHqKJxMif0rQwGbM7qxLKPL+U3/nsJ3i9A22Pvn'
        b'CLlvflYoLR2Kd5QCiT2KDycy0aMlafjgCgc5RCxeiPYA0362wi3+xYHUcFM4JT6O9qOtnrR8Gl4L5BzVZVBFgQwdn0cwCDsVbaSCYfg84TtHTbgd3wBOYVwxKcahVnZA'
        b'8BDj3r8uZ211BF7/OTH3tSEhaEJY/QfflC9R3WGODsIDt7zLyM1vvpH+r43nPlTcCgzgJ89+v/Zvq+Vc/2cdfMTs+X9N+92IPhcPNf7i5bmjf/Wrr9a80Tp1v2bWgLO9'
        b'b29Ycrz2wG/3DF1xMXlI5T9+/4XpVuCI3xa8U/PoswvWzz/vfHePfOzqb8vfyt/U/ycf99Z8MmKzKk4lFehCPVkaj6PYadYc90ksOtFPuJ743sQ4QOKL8AX3BcXDBuMX'
        b'7NSeYSdaHxmjyeWS8G0Y6AusNqaQIveqhXgvEEThIx8c+U7OCTnPAa90q79gc16P907skkjQDuPjNudoLa0ofEmwk7JRsoZ3RggfbjmITqukP4BG/Fg96m0lZLtRzDvU'
        b'jXnFpnARMT4PZ8NFBOcq6I/0uz4SMeeBSJyFf9Ai0gqPj7xRVEj7E1GUs+YOtlNcrbdX+r/OfTzjvC2bHG+Sbz9I3Ve6i5/qSndAWR+IWB9Hm11YiyAQm34JeTOZPPHX'
        b'0/vFkUGkK7PKldHkLVoJCNgmKNEJZuKXEfdbolOO1tQYq6NjaUNOFGn1rZK2kTsGDW5FuN5aVmlcwmuU+URvv9Ro491okNZBB0Cz65XlFhOg/x/AaWThArvhNJnzExjX'
        b'wnFHTGYsiPzrcFNBJvAz2bk5qKMoE53BjbEaYDEy8YaAapDcGx1qhnh0bMHbtWRb7eazczW4Cbi+ItxIvn8F/Iw6ilw0o8VXA9BOK75MNUro9HQlbkOnqHZBZMLtwAKu'
        b'Q4fxBSomjMR30a2YAPKtIrR9GbMMd6B6QbbZii7jbTPtMfkcw85k8F58Gl81Lmv/lrFdg+T6N0PH5SYEcRMVORdX1Cyt+fo3X6+LO3/h4vkLYRNvqadMScs//07VuyP3'
        b'l7zy/a8eBCWKt+15TdEeI7uY+21l0BsHP4r/sP8Y2/FqW0rp6vaTRb/KPilm3/6vqLUb989wvL73g9jJyey4zP060cdfT1m77q9RraMs4UP+rr3TKZaFfF2wd+SY1W8v'
        b'/GWyRbb60YcfV0SvHjgvv2l+r09+KfnszGvJhY9C9/K9fqF897Neimu7Lvadvr92V/ven/Z+PSAtUuFQhVLsg3dY02HWCXspTkXnh7PoLHDxmyiLmYLb0QnCzgIfeBzd'
        b'pJ+Fk+EWbhXe9Yyg9DkGLGo9voQvL3WaogSWJqMTHDqCDuJjAnZrxuvUuMUcA7U0gWggzeMGmPF1Whzm8SD9NE1TrCaLpsonw+Kf5/BtvGUFZSRFqDkJ+N9N+cKXDeQz'
        b'HBM4vBtvWUArl6NGvBa3sGgnUWKqiQjHRfcopPxrDTCuuwj5UJXM1ODNdISh8aKKPmoqsGiHxeMWdHth163ww/qE0oLLrPj5mDiAkYjyLLVGxQGrf1BEvJRSnV/JSEPP'
        b'a9E1fJew8nEgG0rHcr3x6SyaujgfndBSgF0tJSAbGMGhQ6gZ3aapZnzOCMPd3xe3OmdjEtcHX8QbhA/9XAIpw/MLWEZ8Fzhu1KYSkjcA5Y7BF9E20jlYCil6gYuFZal/'
        b'kmboB3C4B94Wk+1MkXasG2kzqxWBRLcjo75DCjaMPommJoxqfAY84taIH9UEu5EsqUO43t751QM746WB8d/TDk7I23Xl/RJ4PCIofoAbxTNrIx/5+g6CV/sqp+f2VIa4'
        b'/bvdoQHROP+pJMIfDn57PnYBFjHaN1jKSkqoQ1KnrNpqqeat9uVP4wxFrPSpUQ9VBVEumtIpOhKBk4/4H1fUPXFRreRM7g+M8+Ne5G6DIDGIPY84mL2IR9wIKRBimEPR'
        b'j/sbIlaIgpy1RD5SxIWRd9GAR/1mhKTK+vdjqX1kFIvabeSTk7aQEBETPAFvHMjhQ/g6WksPwhKy0H45esFORNiFveXkpKaAnNAMSBQPw6fR9f+FTzL5dCPpfrwZkCd8'
        b'KXDHRHyKeM+gBmYIM8SI2yhDa0aX8JW5I7QadD5+NBTHV9nF5WgnpS8DeuL1rk/kJQ11KY2W4I303AY1oHZ8eT7ajVuyYgm7lSQGFreFy8ZbVxtjZXPENgKw6D3lZ7r5'
        b'L57fcqgtoX4xWxbwB+54vULeN2Ni7J8ijkf8qT5Hl6INks/Z/mfmUObZuoT6Q3WHdmRtY4f3fO3FPSFMpbTHuK9jVBKKHtPR2kG4rtrpOSl4TaIbyVQfEoBOiF24pjDQ'
        b'KdyvRntoYo9pq4GZv+6lbVdnORUDWSp8Flj/NY8J91Z8lpatxRfwyakzyCGwkLiA4/FWfOFJjjIKELOAqeFLiEUERUGRHihINjyEIx/SEAPCEbPWFe7NJO4UkwKdUqfj'
        b'WrdvQJGb6awr3ZuBlBzCPYZQQt7z8SE9+sGj07hRGhOVrc7sgTfGZqPWOOE4V4l3SiJwHbrWDZbCnH9t6ZzHhR9jyVUXAKycQbQ+sFjEi+kX9Bjy7bxWrlgCYRkNB9Kw'
        b'FMJBNCyn4QAIK2g4mIZlEA6h4VAaDoRwGA33oOEgaC0AWgs39CRf3zOMg43CGnoZIqFthTOtt6EPudzDMJ6m9TP0h7QQEgJ+l3jqiA0DDAMhLtTwDMSJocRgg5JcwbE9'
        b'aDu3XVQu2i7eLiE/hr7lHMSRvyL3XyFWeIqFHB5P8ePvhiH7Qo2MYeh2SRtrGLY9CJ7DXXXB+wghL7yNdL+Ncr9FGVTwjHaHY9xvse43tftN436Lc7/Fu98S3G+J7rck'
        b'15vnGAzJ+7hjrGH0Pq64Bx/O9zCk9GWe73mIqWNpKNUVojkiqMmk4Aslg7kNMKQZxsDs96LGlAF0viWGdEMGxEUa+tKLDCd0BpYARdNPA06b+qx3OxvwllUEs0wp/c6i'
        b'1H0iIHmqE4Gn/BpZkHAicGuG04x+dt1YA5ctnNErCjcyfVgmKn7UQd1z4cFC5F8HrGS/5Zg55xf8Y9ir4xYw9FQ8AO0e7/Et1Z7o1IxML886wEYtAUxhhSwMrx1L6zk/'
        b'dChDiGv8xBTd7IC+zMeuPv6NPIwdMTskNnI2c+RN6cCNLwWviVf02Cban3zsPJv5XjP77ZQv7p+LZ3vNfHvv9p/vV89NSXxH91LpZ01jD/1CXjfzpTG3bmS+/nnBpNd7'
        b'n0q++er7n+lOv/HtF2+2V1b8a8z993P2bvo+PXp2zj8D2tR9ZXv7qQIpD9cT+Ll24WtDahEjG4yaijg7Pow20dTheCu6iVrQuRxgfC8QXbh0FNcDHZ9E1dTx6IDU44i0'
        b'b4RgvC2Wgehxnbqeq9F+fMMttzdO8p6YEX0llWh/JP1KH27D9XmC33tMlFrIdBJEIsjWe4B4LD6CdlK1c41eLfQWcPbmpVTBvpGcObaL0KGR+DjVwg9i8T5XJvQCOo43'
        b'56LTxERihwgdATZ3DUX83LRq1BIHPG8W+fy0DNUNws0cWo9aJHbCMYIgcAfdQi1Ls+zoVmwWpeykvs35QGWa8vEmjZQZo5WinXPxNQF/PzVv2uXaPsiDLkgTg1iZpA91'
        b'cXdpdcn3At175zGvdkGL2imhdlWdYmKW26noOoAzWzoDjeZqh53eMdbFsnrau0usRMFkXUse6xkXt7rOq59xj1OYyJ/7+sBc917+GN9hSQnpvl/H3YkQpI67nu24/dcH'
        b'dF2T2s19V2PVEoTzNF0pF7oSXOI5h367NMXVpYeDPJrv7rqueaq217u85rtWzF/D090ND8xyZXbZhf677QaWECAqqTL6993OdjcbSaQTZbnVUvXfbk+/zG97ue72Imh7'
        b'xGr4x7bmdA6Xltgtdr3Jb1MF7qb6FpGMLutiv+39z5wEVPgiVRzT/UuJguVYPNFcM5W3OJ3i5CSTQJXqh1FvpahnYnWmpcEhjDF6WKzERu6HOz9gPvm8b6Z+uyGqPF+v'
        b'KL+vu8982d63cPfLYWzfdX3Tfsnohko+rJSrWDtRwS/FzX0IrvNEdPgavvc4sluR/QTGl0qM7k8JuvBa0GzycdyaHp4Y4undxAu7MbinfN2k0a3yTx7Bv//vpC7nqk0a'
        b'IaZs9JayvaY5gd89Rycmce21VEkZhVl2gN64d98BiY3YSUZUrBU+ybzFMOfF3Wg3urylQ/TaNX2mPuZT8gVKEbPwtnTtGwEqTiBQt3F94eNr5l4vdAddcK4ZvtCPijKr'
        b'gJw145aRULApWq0hctA6Lmn4uCeJMqEl1FbaWMOXlJosZYvcnwN0re6A+TV9PSbfO7fXh20l1Mi3u1TTxnipSbbBY063RfdleuK/Xa/d6lp3AmiuD92KYOVF/xNfNvV1'
        b'pkVXvnn4N+wDUaZOUaArWd9/EUOPgIaizbAup8Tk0701TA067jTpQDcK8Vp0imNQ/TBmBbMCn8DrHIR/Wo1uR3hwmNRytigqT82CCLqfSUZN0pD5Kmpu+lPqEVoZIp+g'
        b'M/0qfAJDTSfvZeVHjZM0BjPV+p6/nRNjahIcRdExO+e6F8rLfBJgZ+EiAj1el0IdwnuC8F58bqx1DRQWvEUPPyt2yf2oZbJL9B+Km4yB75eytg1kmrU5I15PCF8XHyF+'
        b'472D4o+49Gp5jFz9lfg3S+5V50yd1Lef0brxo+Pr7BmX/lme9PmyceXDX16y/bX19dmWPyQcmnAsMSRw4e1APOWK/N5rr33Zw/Hdzff+I7A98K0zc1f9YcS+UUf+vLqw'
        b'Q/0fs8PaVXmhO1bM/viNc/eO/eLsl1xd/2kzxv7izmrHy0M2NB1QBQjmBc3oipWI+Blol8pTf6pCR2iG3H75HqwsujPXzcteWU0xZDm6OpHsthyQnp/ADbL4IL3HaULJ'
        b'UHm0k911ezYORpfE+AK6iM/h47F0E6fjXfgcNRkhDC+57Os0iOauSqXMM2hjPDopHYDq8H7BFOEG3tFfsHHIQgdcZg7okoiqSGbg9r5ORUaVzaXKkA9XuT8w7lddKi1Z'
        b'ajU6PwSr9NjfshIxy7GDgCvt5zSJU8Cb+OuaMI/dR4t6f8Vab62w+eE6OesO7y2/HR7zH9/yYYd9HX893mhemdhjR3qdMjs/Y0xd/NyfMRbTMy8JbHYx3ewSusHFtZJC'
        b'j3d/aF7SbbNL8+i+JmbqNxExAR/MiCYMxgfQDSroUturMBBADsbMUM9W4/ORxGgloAc3CO9TGne8cp+xkcs0/1nxOVGSbUFvv/TuS+e33Gi7UXdjd0a9aveQ+ht1HXVj'
        b'WrM2Dtm99pKEOWWUjW4w//UrINrkVBTdGwgg2AICTDvuQGeiEMAMtV9hmf6VYtSIb+LnXavyZGW5tIR6ftDVD/NY/RCTmOqpvCaeZhW04lIPy0H6PWqqovJG8R1iIfax'
        b'nHTld8LD+PjK+/w2cLcO+F/4CQw1MGQapFQlQZY/4Ecu/1N+7l6S17XMCSBzdhTCKgMOYET4FotvLM/FTZFGx3++y9iIfj1QkvuZTquP4qNKtQJHpvtMZyyP/tNfdJ/o'
        b'FpU/MHym45rjU5IcF4/FO84vOX8soSlBnFR9nGUWX/77F4qPxP/Zxb0+lWGM1/fIiWrRY5UjPPe4VbAcIqarNb08JrqrjFDVLv+wtNu9psSD3fL4mvbZ7GNNfTf1CTly'
        b'8L+6Y4VtLXFubMmPXFmfCqLuG9tzZRejg71hYfGOpEwRIwlg0cElaN1ytN346N0BIhvxCHkp/dvPdFnulc3Uf6rT6O/rHsDqPtCFJd/VV5bnlIWXCUzcia0Bf39zNWxh'
        b'astyayXerM2Z8Ey0YORt7/P03x7uDClxXrvqsa6enLesRkwcyft4TLNXAZfawntndkrL9WV2i9UP9hZb9/nbze3wWPr4ykc0+Fh5v11ShQpGyl02y8RcuTO4SyZfxC/v'
        b'DF5icZRV8lZaJME7mNgpLyNX2PDkK7IJnoHETpnBaBPuniGmz52SJXo7ua2Yd9hBEiW36pJt2qngl5VV6smdrySqmOYkdlIJnUGuu2OMBg93+3k0h91oN/EqGT2bsxLa'
        b'Y80gDx+3KOd1ysgnSEiVnXLy5nJzp9H0GivaXqL1CKk5gHhbllqWUY/8Tkl1pcXMd4rK9cs6JXwV+Ygu1yk2QslOUamxDAIBEydPzp+VV9Qpnpw/c6qVODJZLzOPKUHI'
        b'UpL1JWeEFDk5b06WUrtstkFWLvvvssciZ/XeG6tMYI8/j1hF9KmV4rH6/teTljL0wKkAH8IdNnw1FMAJ78FHOXycjca30Dq6DWv6GNG5TJt9CWTAV+QsE4D3ciGJ+Q4y'
        b'45n4Cg+srAkf0QIhzMzVZOXOwI156Ews3hyXPSMzNjsOGF3gx1yuU7htnmIyOm+jh2OxIwfjthnQTR2w5bmoBbcLlhL3UAPelZQcHwjMNTuKQW2h+IzAsB9Dd+KTOHQa'
        b'b2KYJCYJHcOHaE2VtegkFBhXwTFsFIO2r5opXGlyN7hPTajbEpZl5MUcPpuH1wrtbOiB1kOpAnxAyrAqBu2Yjy4KJuINKuD/yW0qo8V4N77ISPAFFrfhu/g8ncbelmim'
        b'CJjN2710k4yx8Yxwa8wL0ulQ2xx8CgTMaPK9+ENlwhHQ7lV4jVaj1uCzaDfxLsxV4+YclumNjoonAIffQOt8PlDJTIDFOGjTzVfNHCAYxINEUlcAlU7uI2LYWAaK78Zb'
        b'aBcn2IkTYCO+LonTZAlnZKGoVVTK4920uv/U9maA0808odLNTzDLGTpNz2bhZqhNrApgWDWD9gyYSJc4KBhvA96VflRpKrosjmXRTWhqHa3o5YzxzEqGWfabeJ01QbRC'
        b'GCvamDwgKRmd5+JBHtMwaG86dIuctg1Hbei0fSYxBstVs0xgAod2D1gh6ODnahlgOQv69dBFN1kqnAM8gNdPJjWNnAxrHceg9lV4K+3UBNwyTDB3y5LE4jsgNW/ghuH6'
        b'AlrXktX0BEE3d7JOkSMPdC7AuhA+KTklDQO9JJO1oxjdFHwC1uAD87XZvROpj84mLbVRC0HrReNr0HpaX0RmGlPNMGn/WaVLPL1SyQgWgsdBbm+FGvGdWo4Oc1ccOiFc'
        b'43+9ZJGW3HDTkicA1ya0lgJYP7RdjJp7DBcGdwz4xK1QwbwSKR3c7l74Dl29VLTeoM1GW6j/TkuesH4h1aK0XjW0P6cCejKAvQqOMrqxf189SBBjR6ItqD4pMX5yDykd'
        b'387FqYJn3F28o9oJrlxOGADrRRZvjxxIT5rRQXwC3U4aHY92QJfYRHL17RF0VrBkupCDjsZoieU3i+rQUUZq5PqiA/gwHX4EPo/vJKXG4+24BUqmQffRpgm0YED6FLwx'
        b'D8CPwF4zOscwirGisNHohrCv2tDRpVBwFmqGaUtniCdsMB32c3PQCXQOrdUK+1FFDOwVYaJeZfgmHfbd8TLqEvKTcp2iShsqLAMsQh26mZSaPALXM7S+PTZ0Xjgqz8Hb'
        b'ySZoBGIuQSfxQUZaxvW3wfDIfGnwxRVQDN8GCspmQDfUK2h8ZN4yrRadrgUawVnYCTB9F2l8PL4TBfnnrIRejwVIxI3C/OLz6HSxluCxjXgjG6ZhpD25QLQ+gnZ5cEQN'
        b'83f42xGmS9nXV+WExG1FvdGleADrCRKGnQSLwA6kVc21QLUtOdnk8ARdRDtFxDanfVY2repqxjRmIwD15Whd0Dv9Uhi6fkm4EV2idZ1AZwEJTGbQ8zLUJEz0Lh7EzuYc'
        b'tK8M2Jjn2DjAnNsFg1trHwa2Ztgck27lWnGJUFUYasUbtFnE6AdtRNfEYmCp0MVI6nzbr7AHbpNIydbRMJowdJJaCON6HiCYOL3NzATJWD1bMIzDjbmxWQQFz1kwPTyg'
        b'P7qK1tN9hg7hM8vQKZXbrRbEZLybQztQO7rddW12/GKqU60eJNXFZlSlCMCdhw6Pwm3SEHwW6AITi/fjs9TxB50MdmhzzH29z/eAwoiZEeikxIHaAF8QMBmNboXhlhnE'
        b'7Uc8B9Ux4nB2gXWusA+v5Nm1RbgV3RgCkID3wIrap1D7kb74DqrTanLRTW+vcJYZkS8xRscKq9mQPgi3yxeiDrLXyHY7aaZYIA6vmRKDW9CWCXG5eFOmOlsQAxPEzMgi'
        b'SaIEbaTD/eXifkwyYGJHf938HsMVwnCHRUpwe4AItxNyB/+LgcKRKu3oyEJS5VF8xbtOjhk5S5KUUUEHJK1FZ7Qz1OiKRiq4Hd/BjQnCZjk9A71QCES4VcIsQ+e4FeyA'
        b'SOQkqyf5gdpZsDBzySQcY/BldK+czkKPcvy8t7t9TOBqlhmMWsT4KmpaSYv3xNfwTtxOnJHPQGW34f/SSurVPmgV2kl2tCYrD0pmoV0GdaKY6Y/2ik3ZuI1O4dAa3EzO'
        b'Cg/jA1D2Dvx3DKXW4+hsGj7rUXgMvqNO5KBwu7gqCZ2jsKngYRJg2oHtNTJGdDZXcGC+jRrRGi1uGowbYt3LFtpTtLBkCZ3iXHReg9pE6DhaQxQEg6fBPJDRLp2H2ynq'
        b'orAUlzU/jBpkDEBXxLiZR6dp4XmyAbhdYsIniKwA/yFE+zISnUzFLVw1AsFrEbNo2WrnLW7pOq1anYVOR6FT1myyw3pOEOHtGVXCzB9FG/ALuF3BTiE+3fAfHV4tMBp7'
        b'CnG9VlM12sub1YSv4FN03qrRUdYWHGydACgJNhw+wyEBU8bK5QxkqDzaXxf7cWqeQN6D4wDbt4iyEGxNC2MZ4bwBbXgM2gDsWSZxu9+ozVdD/wrmSBhlfzFg+J3oeaqz'
        b'HOYYwb4BW1SnzzS/l2bnixk63kk9URM6JU6bKGhO26Yai4b8XWL7BpjaCQvPLnhzruWXE8ICvnjH8WB4Vdv1Q+tvDjj07je/nrR2585J8z6/9O6zy/oEbr89Zcag/b2H'
        b'Hl016TvZ7yz/8db7IuVfv1m2aO7YKa/+a2zGgQcbA2++fPJEAP+b74JWDOsX/YdRnW/O2fP8Z/8R8YvY1qLT0j/rm7QPRtWePr3wg3+E9uq5aN93VeuGv3jiNXbXmZ0l'
        b'vY60/vzXsuV5I8Pyp71c+Ju26xu+Kbpu7pW6b/3QX2453jZuaNKWO3nFQ/+pvJQ3dOuYV2pHBUwJmRQyxtgyQFN0oPcYbsynH+1+ZfEr5oZRU/Ii08eOsN4s+HjjK3Nf'
        b'GTPq46maiE/nR9wo2vLToc8q5XmRU89OOjtmbviNkBv6cRlHGo3tGxvm3e67VbX5q/c3DynctmJD/OK/ndgU1fHlxVll37XMLDn0wLiU++W+B8vr7mHVc1kVDdevHpHO'
        b'ejZ0xuawt5b+IS94dsNrf+z71XOBizN+/kL/B0G/z64Ym10x4IuFH/7hVo9Fz7UtlN++feRhy8qM37y97u+PTs+T/P6jjDe/qam5Wv/a95HnvlxwofW1glEf5Y65VJ9x'
        b'fdS18C9XbQ3Y8wU+vcuwd/CxjFc3H0Ntk+pPbHsUGzj1oO2Vn0997qM339819Lcpv/3VlpKsf6X//uaW3//rWmBwbcyXmmf+9tyHof/6xcLvP7KOb1n1UkdIzXcP1VOu'
        b'zrx/asp75ad3ZRae2JN35eF3gx+8/nAY87mqJ1WCyRcR14H8tEU+LC+IgQFuQvsFl+pmQGcHY/LUqIPc+Yf2srkR6IjgHNaA2/Et4H9AXgDR4Ao+LZ7CojvozEJqT4CP'
        b'oH14D2oJrVZYAVm1hi4Ziq8GB0qZCHRQZJmKtlDz30VQboscdcRmOtSoGZ0SVL498E0ROlMUJNi8rsHrlnWZxFbjzdRODa2NE1zcruMz+CZuTUUtcU6jWBk+wqGWwkzB'
        b'lfpGrnEc3kXVxYKaT5bLGbhnqG8FOo9upcGmCkANMLol7MRCvIXqhLkqfM9l+oa2DxGs34aPEsyZ9/UFsi44k6PjxdTREW0ZKKTtGqOnph+QmIzOUssPfKJC8ARpRrfR'
        b'DqowB6bqjOfVfWIZrqugKnB0bD56wW2H0YTOeltroDURtK7S8Wir26SjCWbay1rjWjz1JETrxsDqtRBnylYqtRAbauckTEV3YsZI0NXRBtosbgDO8iBRi3apRC9N7NKK'
        b'rphLJ3tOIL4L03IeN3W5i1BfkckBNL00Fu3HJwd6mohQ+xB8Y7GvjwP8aFvWTpHeIKhslsHDpbJhVodrIlkxG059zokHOXGkc/9w4Wy3H4iTfRoycLjz3sAg+ktU9f04'
        b'JRtC04mdM8kbRspzYWwEvHOs7EF4ZE1wlyYG+uOpw7cSlduPdcXjhFJduv0r8DjJuUxd1rp++v3Sl92zV1/8H7lTFaDwqSymQeJWAbJUU/FULnjdD/KUzOOailGCpiLL'
        b'JKLakk1SnemcbSUj6AUJNe0NNOsEapPgNeggMB/MICL/UGpZhLfMQG0MyDcngbVj+qL16DilYngXPhyRJMYHYDYSmcT+abSJs89SaSPqUKlOsbufhaEHelvEgSSyOmqR'
        b'zvRtcKnAsW7Io2ZoYS+m6TOmFs4SWDi8FbWBvCkmd9GUDWfKhqBdtH+F+PjSpGQp2cl4EzBnPLrj/JjNlIIAYjeQKRmqi30mulaou31lDzILURqbzvQuO07oxZw5NJKZ'
        b'U6OLHS3PF3IeD1cw5A6bOTN1sVfm9RVy3igOJpFRL87RmTrHDxRyrrUHEe4gs6mPTqHKSRdy3lRTliFsZ5jOFCZNFSLnBtAuxVtVOtPtpN7OY8ZreO0SykTOQmeW4RfE'
        b'jGQJi27GonV0gANRHa5fhNuT4uOBkxzOoG3T8EHa7mtaama3DIfqhvaMtAkshO254cBBVOONAgtxfZBLSLyN1+L2oFVGCFyF/1NRG+ViFij64XbpECtx5oH/PVErje6L'
        b'LjlwG9sTbWMYNaNOQhdpkxmJgiZgZZYuZ0e5TRjA8OBZuA3vAHFoD7CrO0AGwxsYdAUflAsrd6IG0G8buwIB+z2QGYh3s1Q6i5fhw26z6sw05+mqukKQAm4WJRXlFKoJ'
        b'j8birWx4Ml4v1HbNOjYmAB8l2JM4/OxB92iHF6ENSegUDHQGwyxnlqN1/6e5KwFr4lrbk0kIAcIqqOAWFZWwi4qgVtmVRUAQ3A2BBIiGLSGKWkXcUFFxRQFRUXDDBcV9'
        b'bc+p9nrbXlvr/avRW6vWLtZat1prbf3POTMJCSSIbe/z/+ThJJPMnPnmzMyZ9zvne793IlPP6RQlaKDBWoz98aTzSVBNZnjJ+fBMJocz/tnINGFR3DhmYPnD7tMyKMFT'
        b'ErmQ9lARf38JR40zfp5puJOzZnQ89HdY/M6MK31HF18JjLa6d/xe5/zlW6hnvCTPRGer1Mblq1X0Ne3I7V6r4AdWisXXrj0dPidzyzsuKXvdP03t2P3rqLGeHaoG1VUk'
        b'5n8VMKZyx5Rnwlr7x76fv0y1/zLVxevFr24LY7ST5vLqr3anw1N/2zzo631jNtYf5jT1b4r+aPOp1Oi4LRvDd37OdRv/z6P+v33+c8WO2u7SXI/zCx+86D3ybsWIbo+y'
        b'In61+eHiPV6t5tLvmwQfpF5I3eN9c7r7lMX23k8Sur4fOe3sHuU/z/fNn/zby63SZR3c7WPDZy9JDo9yOh9yOXRJ1T8E2vPfV0cvGjA1I9MqIcJZEnR55ondR9csy37a'
        b'a3L31Pdivjj367NP4u0LP3/ww613XGaXeA3tkPrFnRTlouLX3F8ez/uRUyPuXOiFr7mFcN+IVqEbeWNbzCUjZLCU4AYO2OxPwgDifTy9HPGT6CgNKuBuUM7ghgas4INx'
        b'haWfAbcdPVYXEtzgArZ1Y0M8wXm4nksJxtKFbsj3xI5POgJC+ME6GvudOKczpvFbg+pQLjjgAkvJ/p3BgngJPIeTZmGK/jIOZib1Ag3wIBO7WQnXJrRUlXg3oxmDDRUx'
        b'+GWJJ16tA6iI9uJSXHiAA7bhlNbMxPYBuBdsGQjxcRiEp0SNZ7INbAd70Z2K9Z1IQgIybtlxfBewgNdlOjhC1gkUwX0G8k14MIlyyuf14YJ9yO1pJCYUg1NwCWr++Tpk'
        b'Q2BNTFdyHKAGzEd+pj68lEUroN6fASxHYTmTbRj9VIewwzpY2QI7gN1wKwMZFyCHfldzVSykqc1lUE25BQOjNoPTlghhjPL29cXj1MhesBadoj1cuA5BmKOkKlALzyG8'
        b'ZRwaS8Jie0zmDQNVsQyEbQBr0AWB1uoKD8FVsRYUj+aALXC1hkGeO3yQp85SHNJ7spEBqGEWkgsSnu6Im8Q4DOHMXMNIBBKGABdOJidrkBzu1IFUDjimw6mFYYViclgI'
        b'bdYQi6tBtQnERuAarMogpo2ah6CrDmUlxOtx1nIhQ1CrHwSPeXkS0kcuqGHzKCF/XhfU0K6pMh6O5SNoK9MIbQlVPI6QJikTECrCWMsZvTqiV2f0wst2qKTJP01QkxOT'
        b'YAG9ePf4XXlfW3cT0NYca9qZI3htzcXhEQIac8wQnrFrxjN49wbxbm3Y3Bz+dgwVD1tDJ2dTU6ktdoXaBsMU9LaGvMWjT1X4U6cW/DAS4quajQsS9kvigXEosFagCwnV'
        b'fcITTkwgJSGG4TgtErlBJvHJrC+ZANQKJYmhSaGjJWMnJEYma7lqeaGWh9MPaG3YH5IjxyYTXEiOkIGcfz1Fhgpr1Xnj5jpB4bktBy7t+LY8MDsL9G/rzHcQCCyZc8wn'
        b'IS/8Fi/eY9qRxybZsDZIsiHg0y95lvSvAgH9QmBF/yKwpp8LbOifBUL6mcCWfiqwo58I7OnHAgf6kcCR/onvhGr7kf/QztMO7b+zRecIZppgE9wvMXw8WFBwq4/DWO7E'
        b'sXBdq8lrnYSNOqSlLi9vvT3Rq7XXvcto/SfuSksrnswdgWhM2rDP5MksZQK9Rq+VzJpQdoSsRq8tWbYjy1ij154sO5BlAdHwtSYavkJWo7cDWXYmy9ZEw9eaaPgKWY3e'
        b'TmS5M1kWrufJ+mC7ZK6b6fV8TMqZZitzc6W22WHaCbvcRbfcCf3XcVZxZH1ZUrslSSNlU2pf6pBpRZR+ifIu+s2K6OjyCN1HMNEBt4es50pOKeM8CEttkevQS9abaOw6'
        b'yrqS+OR+rMZubHzkywoj/vdYne4r+okR2BV5YFUUrHolzZXhm0TRUp7TaMFzLKahs0JX6FNeujpPiZW6MXseZzFmhEZxFmV5fiGTyJtQ6Vskl1bh4FWxpdaKVWzD+kbs'
        b'RzKnLGASq2KlI1nmDC13ei76LkcuU2hy0HeCfGT5zDyVTNWs8mtSXtc4YZcuV7oVcrqs2YliG33CrvYK7GaJubcft1tgFzf0nxbYfbO+bistXZNZBP6kvq7BCdHbgbOt'
        b't2EF+tmcDbkiqTI/W+pjypRgUUY22mUGyWnettxv22q/JpR936JF3qj2i65FJv1zRFSqSClNxxLz6KNhRm2xb4tc1YxAnUkrjE0nbesRYNAUJoxnDUH3wxu0hs3pCptO'
        b'M2FOa7idusImK23WGv4LusK6e55pdmZJpJCxJ2zAm06YrqNgc36zSyKVPEuhRi2MOijUj5HLyVukYU+bJhfn3v5T8r32zHhLraMjJQoq5mP53ve79aE0OIwGnIA7k9rS'
        b'70X40khkd3GIEFTDaoeuYlJpua8z5aGMoamQtMnjp7uwGWSb+MiFaVGpJsG4WqJkY1jz1nwhrIOnmXqXTxdSnYsO86jENOGrbqGMsYNBJdekrQaeic5Y8QQSYn0CLLUB'
        b'te7jSaUzU/iUUFhDYzVfGZXPZKL26gIPkErhydEt6432SjaM154Py63ABlAhJLUtiLWiHGTuXCwx/IPdGMbE6EB43rQycLMbqDNxemfWxGM2YAcbQvGJ3JpylvEtKYc0'
        b'71kz/Ziwcgt1sqk6PXTeja7CHimkwlOgwQYudQfrFQuPK2j1CowdpeU+H5+2pUOFkWPm/DF16e75bh4lfjkdBYE3P6A5rtvpvgWun4rz9lntV2/NOSS7erLpUlRqXPcT'
        b'67d+rylqWvKvHsek79sej7rmWHHz4vCP5z7ru/1Sdnz28sGPq+fxLj90nXo7q0h9ufHO1vuvxp79oH6BKvJk0fVvdn2z6ujDrwa/mPdi7iaPKaMOFG+8H/h75XCxNXEq'
        b'wS45xPzIOHe4xcj15HWBe0AN8b/j/OLwUHinYWLjgXBwZDzx4JS5Cr3nCk4L2avKguoBN/HgQTmoIl5l2jzk+5U5JLRwYLH72h2UML7QQeS27tIR4J3hSsKBHwbXML8e'
        b'RS7XNlA2HbV6s4NtCZYxHuAGcBCeAmW58DDyy/QOoho0MA720dTuqPJVsS1GAvAwANgQTdaZCHahWsqQn77I0GUl7uo0UF6IObFwEdjcm8GuPrAJHlOToQ3sBR8vjiNg'
        b'1odPjQaLLEEN3Br0t4F/PaMS3yvN7h1VbBdmxzIqdXLB1qxosOGSXjwYQQ7T4sHv4eJ9XABcQFx8gIsLuLhIUW9W1xG0pxJbo0MSc3Xh+CXNL5GpsfPW5r8N6dFaokdN'
        b'ZmlyKcgWhoTZvC8DDWH8VRsawm/NwxRKDCCUWaPG64x62b2FBQQQvKWarJ6eqINLZvc7Sb/fHsx+/5p2MXvMPAkCSWb3OVW/zy7MPg2A1J/dH8JCZvcn1e/PoxktSVuS'
        b'Xd9eHzlb18o6fGLWApneAjc8vGEAYf60QLLe+zG3zyyjfaJW1gMfg32KaYYvTYZL9BG28RlcA1Nw1Dq+h0mIbQwqyHQVTkpBsz6rNUl7LMwU6mPYLdpLTvnZwqndWlNy'
        b'LLHZXqkpsvLbKE0ZKku1qhIrTekpzZ7eIk9DbjVaJnRttJKhTg4BtYwZWH6k/Y6ffkdDRMl5Odh9YHxtnDWOJUhL0/M0hayAkxoBVXNtg/+wWIocN4lMkUmkdApZIG58'
        b'UGx7k4yYqNmy2Jx4JjAw/ovWSz9J2/Lp+gcaeDIiD52+jHmfxrBdGbze6kYVeYSmq+QZ2blY2oZ18EhmPJOGNl8HarUiK5dcCoyATCsVM7VIYXhUCuTrZJlRqdH5MP3J'
        b'SQ4M1rsyeE/9xd54dESngozX0MsgZ5jzvshVqSDbYzEt3HZBwe0X48o0PiB81Aq5+u+T0vLA0lFE9Eos8vTMwf41OpxZnp5/WlxL5EGEtHwYPaq3qboNIa12bf+2slYi'
        b'M3Jc5mStfNtnhhH3o01xKw+9uFV/sWhS/wDz4lSG/BH2NGrkzOEocomhRKk+YvToCRPwkZnKkIv/8qWzckh+XbkKP6a8iXKd3i02MCigbYPaVNwyHiRh7hY/3Z1i0iwG'
        b'DBnqdKHdD/A3L7lmyLbRDRkZ3CboW3RH5qoVjFF5maYVzGTT0JVB2gNvQJIMS4vw53aKN+G/UKNK1GS0TJGRXaggCl3qZv241ves2Tp9RP2xHrZcgzpXfQXoClaI2CZC'
        b'PVQOuuMiU3zGSgvT5XgE0rSemI8IXS5MGlSlJme6PNt0+/uIBrRYjexNqsmcrSmUoycHTjYtSs1TqYlRZuoYOEQUqsnMlqdr8K2HNgjVFObh59t0MxsMGiKKzpUpZijQ'
        b'xaxUog0YlTt1iyM3s3WgKZPfvoEGm6pGYWBWztuZFWSqvrdrl2DSkM1N/4aWN/nlWOZKxkOFLex+6yvR8PAzVehoPHDb6m2Sps/WZInNX36Gm4sG9zF/ARqt2D/Y3Jro'
        b'Msv1ay0gyvw4qGU1geaqCWyrGnRR6I+vjTqCDFcze2jBRpWZOC6zDzSWDYh6OPYTwQMIk6K+VdeVeyQzz1izD+xmsiHWs0ePQmYJYRyPWLQoz0X/6DIX4WdQkHlRzWaa'
        b'onE1AS2qCWizGsJoNFJZ9CDSihH4eTPI7GZ6BiSzaWQK6anxFyIPdJOzlzg67eabQaPCapPoaRHOfvIWGWC7yJQkkcc4WJetQjcpsmWgeVMMyJfNlem/Zo3SVaWerlGp'
        b'WxvVFtwzBy8JlGw/8tNDtFCjUf/2YRhCJx0iisdvokkB/lPav1kAs1kA2cz82dDxVFkIyS5j17mt64CQWNEm+A2t2Ho9873YKLlKlesXpZJqUKH09YtSIHRnvtciq5vv'
        b'q3A95vsnvAPzHVRbe0a9UmQ2AmGo7zffNRHbEGaTmTbDXOMhFCuXF2Jkgd8RwApsE9+l5xUNEeEJZISfMjFqRV+gNjd/UvFGmB3MbCVVivBCm1tkKArxDYnKNuEeQ4nG'
        b'azIfSMXeGKf7DOgfGIiuNPM2YTYyMgi/tXlFZkrR0UahTqWtlQifGZ0h/CaaFGh+Rbab0wnJtnFF65jWQ0Rh6BODhCcFDG5zff2tTTYxntVrs711/G12S+b8mO+sMWsb'
        b'QbSw0Hh0esz3iOmKDFRhdDjatYk7shXnGs/dm5xZuxFD6G6Uf+DgMWvselKEvdQH1oE1Op4cPDpJT5WDS+eRrepnsjkyM79SiROCmJQIYD9oAOUMhY/H48AdYAPYCjb7'
        b'ki2iRnXEjF8H/3nQZ9SYZJZfexoshDjLeCmW7iC6HTWejG7GjqlAr8rnL9KRo8EJNli5Xwc29Wa3Jfy9URpKgwPWvL1BqRdc6RUzeg48CVcl4FhDsC9mNJMhiYKHQFkS'
        b'VTTQKmvKYMIq2jcinv6A/8jXmmRCylDuo4gwZghcBA6bSoWEaxnFTFfocyHB+Rw8AbgSVArFcriSjBsqXKf9m1Jr0afnV6WaVZfjQZrDB1nPf9MmhWSceUxtDpodcFv8'
        b'6Csb5Suu1VptiHKifWDfj+ovUxctNbGXv5wxc96AoRenJHbfk3545CH/cwmDuir2LLvoqrwZ0/94Wu/YJWVh6/Iqb/NGX1bWhxdL0hO/UDae/feDtTN+Uswc8uRI/tqn'
        b'2y4EZH/5pGzQio5bw2BVxcG7Wy786/C8aXvurnRuCPgsOiF1HP+jrTW/3bb+43JlVeyw9DkdxuzskRfRO8IlJyn2p8RbI+69x937Q8nzzMp4ydl7fn3+Z+iVs8stJ9/8'
        b'z+uHr+7ZN80Kuz0lXiwgoZPCIXALyyNxhOfZLMopYAv5UQwWwyMGqoRlYAc4PBWWkYmpbj3ARi+4LCEa7AMlsIJH8ZV0L7AUHCZZRGNjwFHD1EtLQIVuAq0/ReaUwALQ'
        b'COpMTSoxM0pW0/VzSmKwkUy5DeeFs+mX5vi0TMB0EKyHywlVJB8uxDNgBgqGjHwhXIxWaoSnQGkhkXjd6cmNjYvmUBywlE7ieMKyuNYUEOHflOIcB8aRmawofEMXG74E'
        b'CZgUgrPpuROCB5Obh4QfklksmuNG3gXz6dc03VX/ebZQP2Gj53iwWT+aR7FxfLfBFJbVW9kv5hlUQuo0ZoBMMzWP1WutiXksI1PNU0BIciccj0SV8vTJnd4i86KqAFVg'
        b'1HXiw+jRquvsw3SdF7ta4E4wcWx8Wtwd3yEMjbkn6vbK1RrM9F3JmcGj0JXFmRthxRBESEB+SR9Ya8MdDjdRyJxxqNM8RLixKbB2ZDLeqi9OdMCBpyl4ZGAx2ZFLIOns'
        b'RL4jpJOmuWUwdMoeYNEIlsghB1spefoM0qW+A8+C1SzvA3WsK6kMuKA3qeVnJ5IXknooSvN2y45nuBh1SQ6YypEdPjfNOzvBignz52USfkdn1+I0b//IzsyaB3oQfofH'
        b'JxPThPdCs5g1F8oJv2N8zvg07w+dCpg1v0gj/I78B45p3q/sNcyawWmE3xFU5ZLm3UDbM1865hN+R+LPPdOUsvxeTAu+CxbLkxMTE+EusI2iOBEU6h72gq1M0oNTcDuo'
        b'GODv7+85D/0G61BzplmQzQah7r0+ORFr8WEi3070C1gOq8jTxBVnN9RRRkAVPM1yRkBjHlPtfrgCHEfVgoO2LGkEnMkkp8sOnIark1GnsASdW3R2z8FFGpzAKkXMGcCb'
        b'BxYRyk4kXMOc2x15cAtcxwEbOhAaCFzBZ9jAR4eiLnIdZnvADeAYXKHjfIDSIkK7SOPzkhNFXHVfdNqaXPigFtRxSQ4B96RZes7HBFDBkj6KQT1DysDN/WoEIQo5dJOl'
        b'KS/lsy1r40GIQiL7tDThy6QubK6CIxSsRU0rhIexUQspKTwHljGprMc4Ux4UNSpydNq7D0b1ZB/oa7PBtuREsE0My0E9RQ2ZawNru8OdbN6BDLhYbTvAHzQV8FCDN2Ce'
        b'9xpYpvifu9256j7oJt0QvDFnTSwmgCzJ2lw3+mXcxKorTzwf3OZ5n+RMnzGCt3z1lcYw1bWuX0eMCl7iUzDQDgSJHcv+uXbQ635z/ph1JjHadcPkBh/XY4Uj7W/V741u'
        b'WH7r7hR3xxTh1KTvFfL1Lrb1Z9fnRjc9/sq1x3B65BEt/7uze++4/f6KL/3x8HOHlH8+c5ywK6yDNM01/NONE9esLlm9ZvXjLUW+sRfC+oXtev1dY+1ay4LYoedHuv/a'
        b'IbNmHhzmF7Hy484jK4b+0fNV8tW6e+MHusT3V3gWzgu9MStmvOhC0r8KfrxUPT4zJO3b2UvTFvN+UOZcdw86pKxUdLp99cXEO2sHuYzITXqS1/edzcs+n3WD62sXdyFl'
        b'0Ic790zrPSzn29Pn/ZoeXR750VRZj3GHbU7t+u7XTiXhBdy1KrEzSfk3sxAnbTN6ljXlGD7O9A+zyHASueGbA457kQekTyJczUf47DQNcF7u3YzkzQlQD44hJBQH12Vy'
        b'KF5PDqhxhBVMSEhj5FRWEBHuhKvYbIExkJE1HOeBwQ/DRoXHYB3LG4m1Jo/QnmBJ99hWpNpeHpaUKNLCygrsIsIzboU4tiXaKwbW6yJOwoMZicr9oCSMkDlGddTTOcBq'
        b'FxJKIgEnkdVsUAw4BZcZxNVMY+VlhqNNMOMElPo3k07Q5XmKcCdwMlMXY7qHM5bcJgEzGXAD4fymgbPIDAxLQE0cK+RZlMmI/TSA+bAiNpoTYEj2sAMLuWGgypU0vAdo'
        b'Go8QT21oC5ZHFw/ycwDcaR8bPQGcNKB42M3lRsRPI1FBQdMpA2rH5J66SBlYkcoKWiKQW0pYEqtiwclxbEAOWA9WMwE7GwtDdYwNhK4qWc5GB9TwxP4mewSVjIg7YT3Z'
        b'gJ2cSeQMWsKKKYaUGRx1BCtzdYFHnv3NBKq8IVsgEYEhEGVGK4jCy+exUETIcaAF5PnuwHJYMavCgfAqaKKYTOtfzQwLwqv4ht+Ff8+6K4I3NMO4cCCR+DhKn/dCYCX4'
        b'hWfNCqERnNBKYs20/S3E1rg6ObcSw5fTRrOia4b7UmP08N9TXMtEAEXTEqCYlhuzjNdgyg3YI7EguldmlcYGj8lHD6wGJt/OwclCVjkMwfBKrB7GAQvgucHkeQeqQigs'
        b'HFaUOJIqigeMGPHUCB+4xl2vGZYA9ihelNpy1TjuYUzA5XdGn7UGIcJ41Z5j/7a2G15SXd3UEHRiyNJtN3reEV219p1Zdlz21OXhl1cn2zzx3Ov4Yu27I9IfOowJkg7e'
        b'+LH46bdhcQO5cw5dmN9jfa+OVsMEH45ZEHSs7tbK3V+4laQNG7JUvsBn8v0Bs55clO7rGrxOUDvl+9R+IY35888prhx/eERR5Qpune/6KuzsAccZ6/+h2pZ393rBZsXO'
        b'++VVF5anOXS/53bqxqSDrv1qZmyt3vuDvd2xQDeuRGzPyl+hPrietFwwbMCiYRxwADbCpcyvx6f0TEOYhNEM0+uFWQSRjndYJ3Tb45+WId93PysGFpZF0sk6RRQbCYEh'
        b'qNjEKIFVJpLb1x0egJuMpMZAOWgiYmNwUxjpIAbDhXaGYmHII1mD5cKyYBVj3X54YBbei18CegacZfXCvOBRsrU3ODeC6IU1Z7uFuydzs7LgMtI1+oLjyESsF2YFaljJ'
        b'sEHzmJ5pP9ztRTTD9IphklguWDwNnmAyA5yClROI9K+fO1jHSoZ5WJBtB6DjKoGH3onVX3xEMwx5VIvJtvyIECyfjBoNHkrUSYZViEijZaGmP697IIFNcBv7QIK1YD95'
        b'pISAdTOIXQgantBJhgXD8r9FMYzIWpFuzb9Vt0YV9/Jpl2gY7iT0omGqmVTbXK8io333QN+p3Vt1SVRJxxtmRcJ0+0N9njGdg1lkM3vjz/Fip5bcr1kUZUgAe496Y3Ti'
        b'KYok8i6U56gZBlcLPTDHv+QEt+McnUNFT9x1j6cYATAHvpDIdXV8TYv/nPyXkIcfMLzXvNcirtNMwVA3DiMnuxKcBafVephmQdmCI/CMG406znpQI+bEK2LXzeCoOyH4'
        b'2xgsiVw1NHdhCIK/nRrfv9bZ3z7jwVfcukeOV+5RYlWJZGBFkvvYMTdla/iq+x+nr8+ursn748NX+4b7hQ/nRYVOqSkf+VvpgVGZWVXVvwm/OFxbktV3ysjiU5FR4yt4'
        b'ry8FfDal5pfYXaLKW/c3fElHPrf9Nj5Dvr5+5k+dHy0IX1X0Uf9dZ+6usBle8PkSwaGHv382p+/1fkD9fKJ9l4iz5f/4rsulb2pTrvXq6FS8piBqUBNvT+PqQYXpA6+G'
        b'Rc929ru+8cgnVys+nhv808k73B7X7yZXS0vjzlR+FvUf5yfSKZ/uLvg6UWWzfq7/qbW7+nz7+pvNsTMudEsvj7m54bMdA37WRmU9jMvM6Tnththu+HEru90XkhNWuj0L'
        b'C31tQ2tk/X9bJmaSUoNtoAI9esriOHAPqMMJ3FDXcYYitzzY3iHcYPDHj54I1zJjPzndGU7udtDkrsuk3YDwasvBnJyBrcdiuvx3LsO3LlDnw9Xfi6YKwk0VSCTKPKlM'
        b'IiGdDx7wot1oeiBHhId4XvNpPMQjcnNzdvZ0HkH3G8IhQ0HD7Lh9bahiekYQR3VNf/9xtbREYjCK4/b/oA04quv62xdbivsfkn445DsTUmV4RHCmDY6EB+XoMbAsIQ4s'
        b'A+WWlJ0rgs6p3cZOVRx6kshVl6PVsobZdFsWbAf8nS1exx/45aFDyCjl8pD0YKdxjUnXu8mvRM5+NWlRtdPkT1b0Ldge19t24NNJc2d9XZJVc/XOcvHvBx0lij7eV6+7'
        b'+I3deqk24lCfpQ056uTU7TFek2/c01xfKqVLarc5Sj/dtngx7Dj0QcF7jv02f/b+3QVedO6JuyVZt/psBc4Rxc/K7jzjCvI9ntt1QogC96opvhH4mZyAh6SxQLENOAz2'
        b'TKLh7nHRTCb60rDo2AQfeAiv4zAcy3w6wjOYXr53AnGNhorhIuboMV7HI53o6J2474IN3WEpPMf4fNVwcafY6NGeoy0pPo8GW94VIGfiEDNa2SCSwLKBGj8+xUmm4A4X'
        b'5E6RfA/rEFyp8SoQx1hQnFgKbgILeMRiR7ACrCYCd9g/WIGQhniwPw1Xw9PDGU/jCHoqb1MbrGAd7QeX0KARrIDVjPTpLrjJLZb0lYyfZAeXcwH6Mh4hnv0EbyTAFR3Y'
        b'CQNwik9S/pXBVcSAaJ9kgkVHsSBL2KFXKA2PwOPgGBkhFsEt/mjl5d757ArWCCkdB8tpcMQxmTiDbumwDq1xWAiWzizQZKIeu0BYoOFQnWA5F6x414npa6rmYn4DzqOA'
        b'jwXrrVZlI8QFt9uFk74mBR6Yh1veLxb1MKvwcDDYGYC/sKS6uPPAQrhLaJQKudv//d3V8mazekOHY6L/aeZO4ERLAltrfZ5/7LgJOcO5LbEQz51BDaTL6aHlKuW5Wh6O'
        b'1dVaFGrylXItT6lQF2p52FXS8vLy0c9cdaFKa0GU4rW89Lw8pZaryC3UWmSing+9qfDUPlYIydcUarkZ2SotN08l0/IzFcpCOVrIkeZrubMV+VoLqTpDodBys+VFaBVU'
        b'vbVCraOIavn5mnSlIkNryTBo1VobdbYis1AiV6nyVFrbfKlKLZco1Hk4+lBrq8nNyJYqcuUyibwoQ2slkajlyHqJRMtnovUM0tjTzNn+GX9+jIsHuLiDi9u4wCpuqi9x'
        b'8T0uvsbFj7j4BhdYsFT1Ey7wPJHqP7i4j4uHuLiFi+9wgSXgVI9wcQ8XT3DxFS5u4uIGLnCCT9VzXPxgdPqsdX1qxIvWfSpZ46UgEwfmZmT7ah0kEvYz+9x56cYui/Kl'
        b'GdOlWXKWjSyVyWXxYgHBiVhIVqpUskKyBElqrVG7qwrVWKRby1fmZUiVaq0wCccI5sgjcZurXuhar0WkvVYwLCdPplHKh+MRfpLggEfxLAV0y0vNeTBNLsX/Bdrl4v0='
    ))))
