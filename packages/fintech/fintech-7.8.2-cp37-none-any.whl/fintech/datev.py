
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
        b'eJzsvQdYW9f5OHzv1UCAGAbvKW8ESIgNxgu82NgGLzxAIAlkC4E1bINt4s022GA8470nNt4zPSdp0jZJ82vaNCVJM9oMJ2matkmbX5o233vOvRKSEcTpv9/z/L/n+Sxz'
        b'pbPH+553nfec+wfG5Z8I/qbDn3UyPHRMPlPC5LM6VsdtY/I5veioWCc6xlrG6cR6yVZmldSqXsrppTrJVnYLq/fSc1tZltFJcxnvUqXXtxt9ZibnzVqoKCvX2U16RblB'
        b'YSvVK+ZW2krLzYrZRrNNX1yqqNAWr9KW6NU+PnmlRqsjr05vMJr1VoXBbi62GcvNVoXWrFMUm7RWq97qYytXFFv0WptewTeg09q0Cv264lKtuUSvMBhNeqvap3i4MKRR'
        b'8DcC/nzJsHTwqGFq2BquRlQjrpHUSGu8amQ13jU+Nb418hq/Gv+agJrAmn41QTXBNf1rBtQMrBlUM7hmSM3QmmE1ww0j6FTINo6oZbYyG0dWSTeM2MrkMhtGbmVYpnpE'
        b'9cjFMGkw/G1KUXaxY045+BsKf8GkA2I6r7mM0jfbJIPff7RzjJhR5DBMYeavI9WMfSxEJqWYcQOuy8lEN3Pm4VrclKPETWkL5qqkzMRZYvwI3Z+sZO1kUCV4Gz5hTcvC'
        b'O3FjFm5kmXBc75PGoQ58A51WcvaBkAfdMg/PSAtPC8PNEkYsZtERdBeftZP5QXfQw2CSpsJ1UIGEQfvN/rhelO2DmqA0aSGdQfWoAdeHV0CXGtMkzGp82gd1cug6bvCz'
        b'j4YcQal4L+S4Jke1a1fbcedq+Wo7ywzCzSkxItQ4Ex2GvtJRoRMq1ICaIzJUoaS/s0txMwl7McPGidFW3I7PFrMueDjMMWeFBGg8yJgfBzTDMAFgbC3g60YOAMZSgHEU'
        b'YGw1JwDM4Aow0vjAHgAbxQOsU+PFyJnaQKmiMPwLAB2N/HqCCH5qFD5MoXyUTwgf6RvlzQQyLw3zLSyUv1zZj4+8mS5mZEyg3Gt6Yfh8RTFzjjH5QHQ4O1j8Vf4vYZre'
        b'n/hX7mbkGWkWY/KGhLV++9kOLyZw/4zCqLejPhsxhI+WFP01oC2AnTtr+XvsvxcXLf2e6WLsKkjAO0dPBUA1RMwLCcH1EakqXI/O5YWkZ+lW4uZwdZoqPYtlzAHeU/AF'
        b'dMltun0dI57OT7f7+mDIZBt8ndPJ9TmdpU/iv7THdMqzLaRViqH4Pr6KO3LnqxZyDJdsFDH4WXRlsD2IjkeHNuVCFWPRjeXMWD2+RaMHmfGB3PnceLyZYUqZWfjMAjup'
        b'Hm1Bh8fhVqg4Ah0KYyIqUAdfS3vCM7gVRqvKWcCoUBO6Yx9EojexI3Kz5uEmCcPhK+jIenY4bsEP7BMhbTY6C2sCUD4sAzfiusx5IehceCpdg2p8bi6qk0Bj7RPs/SCv'
        b'EnXCNHfCICd7VTGT1602Fv9+CWc9Bknqv45e/spofzQ9cPv7+4233pm18Kv+w9m650dr3pswOO+gz/NvdNS+qLrr7TW61P+FgUG7X8hK7/zrg2lbh8Z9+crhAtErvz3g'
        b'3/ygMeZayanWP+39ecfhhb+OPTsZSx7Hhx6e+EbKL0JUevPusEMft6wd/0nIz768kTfs0nHdsOzqmq37Bz3z4Og3X/3yqyXXd04b4XNj8cuzMjZHvB2bND9+T8euW3+8'
        b'XL5BPwl9p1ZKbGSZoyNL8LkM3BSGm7IARxThsNKD8G0RrvFDm22EVqwOxo/waXw1LF2Fa9MysyWML7rKAaS24X00A76KDqD2MLUyPQy1TBIISgDeJCqfkULb8MHbw33J'
        b'LNpVoQPRFkBPjumH74rQpSp0zDaE9OIYvr8RJr0eN+NGWFL4xoxEFl1dmankurgQpYVgj9KXfv0HD4KI3w6cbLCUV+nNwCcoB1ID99CvmdrlZ9GbdXpLgUVfXG7RkaxW'
        b'BcHeqTI2iJWxPvAZCH/+8CHfQfAdyPVnLVJHzUpRl5Qv3OVVUGCxmwsKunwLCopNeq3ZXlFQ8B/3W8lavMhvCXmQ5qaRzvmTzmEFJ2U5VkqfdtLfsZmLw9JxU0aaCtVH'
        b'pANfiEhnmfFo8yB0VVJQipucq5L8Ewvf1lJ46AmnBy6vY/NF8Cc2MvkS+JbquHwvnX8NY2B1Yp1km3e+jP6W6ry2yfK96W+Zzht++/CM1SDS+eh8IewLYSAiEJbr/CAs'
        b'17GUNQZ0SefTecqm8/b437Aui0VCV8ggvRzEQsM4uDVUwlMeUa0IKI8YKI+IUh4xpTyiarEnQs4JpM2d8oh5Qv7nfhKgxIyiwr4hfKjtGcb4/j8KRVZgxMy+xprPCl8u'
        b'+qRwt65W+2lhY8lF/ScQzn9uGe5oHdMSuX3eoWPt/Z7P0Z7VmiTn2fOFPxfvCh8hn6Ue0ei7OGnTp4OHzB+8ZUhCNFPxs8Bn2Bal1DaS4PajcZYw4KXNAvvDzWFSJgCd'
        b'FlWhZ/FDiv5SdG9KmDNZxIxA2+ThIq9x8TS1Gj+oyMBn4nFDJkgDSikjQ/Xcugj0yDaYjK8CbyLkKiMNXYKactGpBG7IUtRoI6IHuoTqbaghBzi9mJGg6/3wIRbfxSfR'
        b'UZqMT+Th2jAgeAdUqWlk5cvwdQ5tW4BalJwLHoo8LSiKll2yggKj2WgrKKALR04mPz+QJR8pK2arAniAqx25+AUj6RJb9SZDl5gIcF1ea/QWK8h6FgIcizeP+EK7BNkt'
        b'fuQR4FwJpJGlzpVwJtBlJfRor5hzwXgneqkF9DJwAnJxlK2JALk4ilwiilxctcgTW2N6QS57OE/q0HFf3AQQ2QnTTBgybs5N5UE3by7ldNPwMSkAotJ48mAzS3F9yutz'
        b'PiskqPaSISIoTJup/bwwsLjUYCoS10eqCr8oXPzS4Jef2y9ljjySDR5c+ZNspZgH323ZzAxaNdqMHzgxA+9cYBvDUCHvLkhrnUCRm3HzqNFqVQWgGCG+Q6vFaPtCvMVG'
        b'mPCgqdMcGJLmJ6EIEoAP2/qTBo7noqsZOSoW3wJOuYZNzkBtPAg5j9gAZK9EbzPa9GUCQhCqxRT5sHK2KsgJGmcWvioxBXCX2Kwt0/fEAc7Sz4kDFPyB8Ch2gv+Ivyv4'
        b'PbTx/w6B6RUHwuC3HAT1HQIO2PGzvaNAzTTj9SPVrDUKCt05vtIdBap9HUjweSFXH2XXvKk5qRFHV5wWMZdWygpkMqWIrv8yLSvgQLvdiQJ5eDtFgXK8FV1zYADAH11P'
        b'dkUBtMmf1jEmcRBBAbQXX6aEgiKBFG8R+Fvvyx8Abu0J8JInAG51B7iEhyaBa5dkjdZk9wB2kQvYg52wJyJdqRP2BwI9w97ZnOfVH8XDnoi5rEH8lBSgxBX6rFClO/Ql'
        b'2fZIsmZ24Xv4GtGt8vA+Oa5VqdTzUtMX4NqcXF6STAWhUs0yNvzAWwpZd9hDSA3e6KCDbLjji9HejTHpFuOc3UqRdR6UGHljz2eFnwLKmAyhA0O1qVoToMrFuZ8WVmhr'
        b'95zXn9V+Uvhq0cuGiN0h2nTteW1gMfOzQenbtj6/f1CHTROu0+lStTLDey8zx1qYjYWBu+92gUBI2NUq3IGOCdIaKJm3Q13ENZ9iG1HO0OnBeCdFuhvpLhwJ1+CTFOvs'
        b'aNeGbqQbj6670R20Ax3nmdPewExAO3wKt6Z1ox06jq5RpMTtS/HZMFUqSKYuvGljlANFxL3KejxuSu0VRMTrZkwmH0GeC2Sr/ARs4fO4EiKe53Qj5JPYDxSpmytRrCSU'
        b'ssyJlXuCXLHSvR03vcudGFEl10mM2Fq2Tz3Lzc4g9oiOomzjsoWYF2w0d+5kaFNLVKM+B3z5eVGpob/2rP7sa9y1IYM0Kh1BmDrtef1FPfczdeFl7bKXFv9iGc7Dc7EJ'
        b'zw0JfvW1nywW/XoAZUBZ/xu48tv+AvtZjx/YeNJTge93Y8E5fIbCT4yOoVNO2SNlHIVuNbpIyyajFtyKG8LTcBMoVlLQJjpWcGPRQXyIls1CLZNdhJrFaAsINXj7UM9A'
        b'74tCgUhutVkE6kQ0bsYWyPYH+gQUyr+bZJAsDmrn9wMIwLrAfgBBdyfsm9wo0hPVK7lsC9G1lX5EaiLcDhQFn4IC3vQFv+UFBavtWhOfwpNHWTFgTUm5pbJLJkhJVioJ'
        b'dUkNRr1JZ6XCEGWJlDZSVKR9clDaPnUifghkUnLJEEhhGSdmhQ/nL5NL5JJAmZ2uxhO4DZ/1JZqF32qiW8jkXOFE/MizXkEkLDe9gssX60REjzjE5UvaGJ30KOgRx9it'
        b'LOgYMipheXdJZ5mBcFd+23+mvshoKwe9LCLDotfxPx8H0rX3mDTxbdBCvaXKXmKt0NqtxaVak14RDUlkNN/KM/W2KpteMdtitNogkigZj38Ko/16P8xQRrnZVp6UDTOs'
        b'CEnWWfRWK8yv2VZZoVgASqHFrC8t05uVSS4Ba4m+BJ42rVnnsZxZa8P3LSa1Yi7ApxzKLiy3mJ8mn6fKVumNZr0i2VyiLdIrk9zSkjLslqoifZXeWFxqtptLkmYtUGWS'
        b'TsH3glybKg20KnVSshkmTJ+UB/zPFJG8SqtTK+ZYtDqoSm+yEq5oou2arWvKLVBzlaMNiy0p12bR4iP6pLnlVptBW1xKf5j0RluVttSUlAM5aHMw81b4rrK7FHcEitaS'
        b'3hF1WiF0BKLUiny7FRo2uXReEdlrSlRSht5srlIrMsotUHdFOdRmrtLSdvRCe3rFHHzfZDOWKNaUm3vEFRmtSXl6k94AaSl6kClXkXpDhCilI00xRw+4g08abFYySjKl'
        b'PXMr5mQqk2apsrRGk2sqH6NMSuPxxOaa5ohTJs3WrnNNgKAyKRdWMHRS75rgiFMmpWjNqxxTDnNEgu6zRmJWERxWZdvLoAKIysQnif1iFZk1fvohMi0lOZuk6fUWA9AJ'
        b'+Jm7KG12nmpGOcBGmHy6FozmUsA1Uo8w7alae4VNRdoBglOkFtoUfrvNu6d4Mvdug4jqMYionoOI8jSIKH4QUd2DiHIdRJSHQUT1Nogol85G9TKIqN4HEd1jENE9BxHt'
        b'aRDR/CCiuwcR7TqIaA+DiO5tENEunY3uZRDRvQ8ipscgYnoOIsbTIGL4QcR0DyLGdRAxHgYR09sgYlw6G9PLIGJ6H0Rsj0HE9hxErKdBxPKDiO0eRKzrIGI9DCK2t0HE'
        b'unQ2tpdBxLoNonshwnqyGPUGLU8f51js+Iih3FIGhDnDTkidmY4BqLEe1CJHoMICBBmon9laYdEXl1YAvTZDPNBim0VvIzkgvUivtRTBREFwppFIC3oVz+6S7VbCUKpA'
        b'YkhahE+WWmDerFbaAKF6PI81GcuMNkWIwHqVSfkw3SRfESSaS0i+2fikyWQsAR5lUxjNijwt8EWXArkUBiRlLrWzulbWzcZV+dALIBghpLhbglAeksb3LBDVe4EojwWi'
        b'FSkWuw2Se5aj6TG9VxjjscLY3gvE0gJZWp4v0zkHuQTkExpn06+zOX8AJXL+jHbNanVm4wGRogd2XOISMT4p32gGaBD403ZIUhVEEdYLVNotGOUeBPKjtdqA21mMBhvB'
        b'GoO2FPoPmcw6LXTGXARo64S4zYJPlgASpZl1xjVqxWyef7iGotxC0W6hGLdQrFsozi0U7xZKcAslureucQ+69ybSvTuR7v2JdO9QZKwHMUURMl+YVasgaCi7BSNPiYKs'
        b'5CnJIT71luYkZR7Sczy3RuQuT/FuoljvY+gjvTfp7Mdkjuq9ZTc57WmyAan0lM2NBcT1YAFxPVlAnCcWEMezgLhuahznygLiPLCAuN5YQJwLqY/rhQXE9c7H4nsMIr7n'
        b'IOI9DSKeH0R89yDiXQcR72EQ8b0NIt6ls/G9DCK+90Ek9BhEQs9BJHgaRAI/iITuQSS4DiLBwyASehtEgktnE3oZRELvg0jsMYjEnoNI9DSIRH4Qid2DSHQdRKKHQST2'
        b'NohEl84m9jKIxN4HAQSyh66g8aAsaDxqCxpBXdC4iCkaN4VB40lj0PSqMmhcdQNNb0qDxm08QhdnW/RlOmslUJkyoNvWctMakCSScmfNTVZRbmWzWvQGYIJmwvM8Rkd5'
        b'jo72HB3jOTrWc3Sc5+h4z9EJnqMTexmOhhD0VWZ8v8Jg01sVOXNzcgUBjjBza4Ue9GFemOxm5i6xDvbtEjVHX4TvE07/hNhQwscLUoMjFOUWik6aKxhXXAr3MLtE9oyK'
        b'6hkFao6JKMVaG5FLFbl2qE5bpgc2qrXZrUSs5UejKNOa7cBeFCV6Hk2BHXoyAyhdihgJczfqaLEfzOyhfg9MyXPdPTNSE1P37ChA+FYIIi+dSgNJFyaZ/x3l8pvohN2W'
        b'qm/ZpGylzEL24yzEQ8VCbG78HgjZArYQm2mXxFphMtosw5z2PfZJWx5xx9joMEdSW56IY2Ucx4kj7aSeaHSjwkqcPepQLd4fjs6JGVkcVz0y8b9kxjMovbt8kouLy+1m'
        b'G6gNXf4pAGte3dBW6E2PB/BGPGL6/nboTIB+GYgUxEaq4BUewF0jUBzIQkyvXWIi+rgZ8e5D/IIyXqApLzXrFbnlJlNEKlAksyqjithXuoPdNC5pUUa+gi9G7GiEelqN'
        b'VjsfQdJcw/yam0PMfrx8zzeUskCVW1xqwvcB9iaQSVyDSSl6k75ER8bD/xSMLt2/owT9KMkxIVTeJwKhXljaDqVNwQtFgurXbaQSlD4qqhN1DzLD4rJRtUCogTZnMkIG'
        b'+stoNpQrVIpki83RFSEmzUxKPhFJskV5yhbVI1u0p2zRPbLFeMoW0yNbrKdssT2yxXnKFtcjW7ynbPE9siV4ygYyRk5uXiREZPCAIbKunkZG9YiEgCJLD/TSYYlV2NWK'
        b'bkssRPIo7TCNqhVEXndo3bzJtRuMisywzKTZdvMq6vWqt5QAgaoiRIXEpyxQxCTybNbgyEJMwp7iBbzhkzxUmJRP1QEycEuZliQ6UcRTihNVeisW1Vcxz4k8CvVRzHMi'
        b'j1J9FPOcyKNYH8U8J/Io10cxz4k8CvZRzHMij5J9FPOcSIol9lXMcyIFt6ZPeHtOpQX7RpTeMSWyT1TpJZUW7BNZekmlBftEl15SacE+EaaXVFqwT5TpJZUW7BNpekml'
        b'BftEm15SacE+EaeXVLri+8QcSM214fvFq4B1rQXma6OC6Vq90apPmg2cvpv6ATnUmk1aYlu0rtSWWqDWEj3kMOuJUNRtbBQ4JyF4yXYDMYs5iZyDl0ISobzdDFkRkmyu'
        b'4gVisp8HxDjLaAPWqNeBIKK1PZH8BB3uWbibkj+ZZjHhm1ZBTHBLSaW7OwYbSCVOtYpyEhUVezzqAMJIBW4OrB84DRGhDVR4LiMM3qY3wrTYnHbiNJB0bUaDcZXWlfrn'
        b'UzXQaT92FTN45dFlH9FVTJqt5zULvbGIJGUC1MjGmJWXbHqX11xtw9BvaFlrspet0pc6DNmUCRImaZkAct0PSroW4ojdl5xLXGbue5Rzh9DDCyum4IPWzGy8E7VrI6i8'
        b'ixszvJgBRWL5oClusq7cIeuuZN1l3TZpm2+br45rC24L5mXeJi9deI2kxq8m2CDS+erk27xB7hXrJTo/nf82RhegC2zi8qUQ7kfDQTTsBeFgGu5PwzIID6DhgTTsDeFB'
        b'NDyYhn0gPISGh9KwL4SH0fBwGpaTHhg43QjdyG2yfD/ay+AnPt66UU0+OlUNJ/RWrFPoRtPe+vOjavNpYw1kZF706Sg1pslbp6ZucRJ6vCIQynrpxurG0bIBughIk9TI'
        b'6OGLIJo2Xjdhm3d+IMT2gz5N1IVAn/pBG8E6ZZPjJIF/TYBBogvVhW2TQS1BVE8oUWq6ZDOJA/aM3IXfRvgoXP45ohU8deFP/7jlUEos5HCPhRxCeUz9sInb3WMZr1w4'
        b'lQWl/DHxt3lMnY2Jx013KUuMo5QlljzICYrHxBHiMfHQeEyQQunV5aPVrQG6ZSkw6rq8i4F6mG3kp7+WV3AKTCD+2Uq7ZMV2WFjm4souGfE6NWpNgpOGr8EIEl9BGSzq'
        b'Utp2l2jWgvnZtIeWBAgXywTs8xH+qAvPVOaJs0reNdIanxovg4/gHSSrlW1lNnpXSTfIqHeQN/UOklV7L2Z0Ijq74q/JWQi3SSP/0vjuGav0VnomyznVRurhUKxX9yjS'
        b'I2ISKCLaMkX31EwSTmMBsSF2IeG4lzBHWrOtRw3kX0gK0Aibg0Ip1YpkUh6oSbGCegQq7BUKoKnxCp2xxGiz9uyX0A0nVDz3gk/23APn7scP9CH2h/rgjg6TFJn0m3Rh'
        b'TkSmI1XomNVzXwgHIrQfOIdakVcK3ACQX6+w2otMel0JjOepauFdS3i1FWpSaKEKCPP9V5jKgTNZ1Io0m6LMDspLkd5jLVph8EV621o92f1VhOj0Bq3dZFPSw3gJvcNC'
        b'WAaTFDOEX4piYj4McW46upgdlb3V4lhCkxzYanUCk5z9K7coQngXllX4vqUKVPHeKhIcpiZRvYvIKFANjyMCYQnRl6gVsZGacEV8pKbXalzW8CTFbBJQ0ACpzmA0w6qB'
        b'Pioq9VroWKhZv5bsgK6JU8eoI0OVPafqBzyI5fwRhbXPBDKKhCCWqSjMnD9kLGOfwpBDS7hGjhuy0MW5uDYNN2VE4Dr4hTpX5eSmZipxQ3i2CtXj5sx5qehSanZWVloW'
        b'y+Bd6Ki8PMxGq928SM4MTr0mYeYWZuav0wjV7peP7llrTq6kKhXvxHWZwD1R3ZO1bquUM/gU3k+r7ZcjYwJDDnsxhYXy70bOYOzjIHL2Op3rIapUtSqUHE9Bl8VMLN4a'
        b't0xqDVPQg2C0ivZFXozc9oWUURTKi1RJjJ3QQNwpCffUM1wLdTaEk741Khc6u4Xr8RmWQXcsvuhaJj5sfLjrVYm1Cuop/fDmiJff8t6kkW9///St63d3tN7eIpLN//Lv'
        b'Yz4Q++yOtOU2H6uQbZi2J/ztYaPD09rG2d4fkP+v3w+/+WZDdpCv/fzCtq7fJC89u8je/Ixf/aYte5mAC295rcsLeCvvm7qujrjGCe83D8t646Nb40Ye/Pj7y7bPiia1'
        b'vhhwNFR55xcfKOXUX1YBUDiMGiIyVOos5xmPgPEigyKW+svic7gDX6KusPmugGSZoXiruAofGs8f1bqjecYX5lOZZRf8aQegmrGLxDJ8G52wKUiOExuySDWucGOZgaPL'
        b'UKPYF+0Oo/7+pXgTuhqmCklVcQx6EC9FBziVt8FG+NMwVIsfQAUEWOhYqACvIHRZhBvQ5RH0NIoZNynC1EpcHw4db8SHpegiF4234320B0vGoJ2ogZziohDSoLMESFIm'
        b'aI0IPchHnTYlZArzpo6hRD6LELopwJdhNKgGP8TbpWoA5y3beDI71/HuSWRUDeGhapIXN+Fm3oK5G+bWKvErRhdp9wejTVEkI5H3wtEDfAemQQVto70ivH3jEr62Hegq'
        b'PkRy1eATjh4I4uFQdFuMGtD2FbzU6fMfHjXrPqZCnU7JamCeYTZIWSkbyMqEJzlRJqOnymQcSZGyVf0c7Nh5fCXb0RHqcErWhIWcAbNMJ49k8khhHGdjZjB9e63K+FLd'
        b'lSQ7S9FKPJyyeUy6T/wumU3M/pGurq09u+p0bWaFP+pSSvqzgVnJe9Cz2Uq2y7egW3JweNJybjPXJZts0pYV6bRT+0E9fyN1urTnSPtWoOVCbQ6+HwI8QqcqN5sqldCY'
        b'SFde/IMd28Z3zKfAKUt47pclFR79ieiWBj++HcW3zxfy0PzTthtQ4C4/9NH4IGfjyj5ljB/VjVK+G94FDvbdRweGOjswJEVr1Ts5/o9q0OBo0MHp+2hwhLPBsb1KAz++'
        b'aVmBIBv00bKiu+Ve5Ycf0bKA/fICF3Gij9bHdkP6B0QOD31wO1xAz7pxNYzzrNuPOlrgqK7H0YLpimqOnpPd8Otb/LmlUsPnzP80vtL4gfwn8kNDmKknxMM3vfVHq5Kj'
        b'fEGCb6c6SXM3WV6Or+HtaDs6aSNUEh9agyljQAfwQ0+kGd8O7ev4mVcBWUOuJ5Gegc/EqkAXakUz9OLpz/Xi5L8YHhNgdq3Exx5o4SbmbbdjZz3qV/p0eQlrkvfjl1pt'
        b'Fr3e1iWrKLfaiFDcJS422iq7vPg8lV3SNVqqW/oWg2heXsbrnCKbtqRLUg7Ybin2FaBBeuXvgMhsAlxfp67o5zy5789fk2DwF4DuWysHoMsB6L4U6HIKdN9quaAxGkBj'
        b'fEfiQWNM1umsoBIQuVanLyLrDf4XCy5wCj112H8KpZGqNFQf0SpK7SV6FzUNZsRqBDVHwZ9oIBqXVW9TK3IAp3vUQxZ+Gdl5MZZVlFuIdukoVqw1g8pCioK6Y9EX20yV'
        b'iqJKUqBHJdo1WqNJS5qkEj5xoLSqyUiNxIYGK0uoUtCSSJ096oCq7VajuYT2yFmNIpQCK/QpZmS2MNpSYuHo2fce+UNsWksJtKFz0CBSXkGsglaicVhX28nsFlm0xav0'
        b'Nqty0tMr8jyeTlIkuzERxVK6D7q8t2Kk5UkKeohh6Q8eZei1Fn5ZTFLk0m/FUsGxrtf8juUzSUFsmgAqqmAudXWs67UsWXCgmsJTsTTHYus9H78kISv/g7YRrkjLzVFF'
        b'R8bFKZYSO2avpfl1DEpncp4qbaZiqbA5uDxsqetBjd4b717+RI3mAwpSkat7cK/FgWDAZJbC0oDlai22GCtsAucieEqOW9O1lWyylgP+6nUeLQCATiQ34TQmeqsOBbZa'
        b'MZM3A9AlOibXpi0rI2fazGN6NQjQxQCIBR2oEJaWzkjv9dHCtK41AkfTrwOICwuuZz3kX3a5Tc8vE7r49bbSch1QkhJ7GSAa9EW7ChYgLBo9zE6xXlEOrN1jPfyQyKKh'
        b'9g0rP0yj1aVLasVsIGoOguSxFtdlR6whgOrk1qJiEwyYv7DIqvdcslC4s6i8mPac3zaZXGqzVVgnRUSsXbuWv5BCrdNH6Mwm/brysghetozQVlREGAH469SltjLT2AhH'
        b'FRGRGk10VFRkxMzIBE1kTIwmJiE6JlITGx+dOLWwoA/bA+F+PQ8MBmXbiRKFLkrwLWumMl2lzibH88KyybFVhhmXKynFVyrs5JQYeha1o6Zo4Njb8UkmkonEe4dRPf5C'
        b'PLlboWOkaHqh3LwwjLEnMvQc+hG0O8OhbFUFzcO15LqRdNV8chp6fgg5KboItHr4AlaPdqMr3njPKnyPP3jWODIed4JKS3Q+L0YyOxPv5+SFqXaqze3ZiJ7FnWpy8YUM'
        b'7SYHaKFmcpUJx4xCp8T4LmpbRs0co9GeMNwJ2nPWAtxS4TI8GNxcXJsNpRozFlTAIyczfcVovEfM4Hq0xRefxJ1yO9mUiMFXCnzVynR0Hx3xYbzTObTdho+gbfgEf6XS'
        b'frwHNeHONKiCZUToJgT3smgT2oNuU4sIPqHFF31xbYQadNeO0dB2ODqXDopyLcso5kjE6BHaZCcOMgmoAx/BnRGhLCPHZ7lUNg5vm0+n91w6uYPoTbuvotC0ung6QxvG'
        b'1wrRVasf3oNvQNsy3AHNy5Zxc9AjfIDev4TOxeBmksHPD9/op8a78I1MfDUM7xYxgypF6GIK2kIrkqBTQ3zVUAfMXxqZG9GMcGYAviMOKNpg9PVK5awHIFfViXrVq1k+'
        b'SBMoeS8+7dt3P8l+/OrW23/1WaGd3jFMqX4r64LmTMvAyWcjFJ3frHs/MnjrgIXvXL3tPTZvUsi3loRzGY/lv7gYtyTBVPft2G81yw5nb/0Z2/ByETL81HA08RVj8rD8'
        b'+Tlh+b86cPoVvyb84vGUt2599qs/7fv99QXf/W3nnY0b7NNOvVXtd+Ltjjuxw67WfXlkUd6VUdrfplnC1t59XbhvIxlkyA5ibRmB2lVu5hZ8GTdTQXPMcB8nOk4HOLka'
        b'IMKiJbgZXZXRY6rjo2PcLC4yG7G5iGWV63nDzQN8AHcQuXYf/HhCtoW1UT+FvwHkCrqJjoVlq9LSsjLCcZOSTV3GDMT3xVGAdceoiQgfw+14U0Z4SCr0A+CHLnB2fLYS'
        b'nUS1bmKp/396B06vB2R9tDpdAS/IUbl5gkNuTiVnZGXsQPp0/Yjp/R4ytirYKfd21yGYLPx48XkJ49jbyycPcm2HZRl5LCePFeRRQB6F5KF1l8Y9H/X15evsrqTA2YTW'
        b'2YSfs8VCZztUki+mor2rJP+7Ca6SvKcRKb275Dri1idISl1+vPzrCEq1ZfSb3Gai7/IWNnOL9V2+RFoBGZG4evF9cA6z2EcgxcTMEuggxelEnPdxE+j9QaQPEIT6QCLU'
        b'GwIFkd6HivS+INL7UJHel4r0PtW+gki/DUT6Zq++RXqt01NPwd9g9BSC6yxyuIHPrQDuCfMEMilIBFrXS/mI1BCuKLGU2ysgFYRlbU9uVF5WZDRrHfJJKIguoZSx8nyV'
        b'aPhOb07SQafi26Mmogj//zrI/5d1ENflNYkAio9x2rV+QBdxW498eT7KUYFHgWzpD7h49tocv975doQlLsTxMq25nNhrLFRqNXuWRdeWE6HRWKY19SL1Lu3DyRV0Cc9u'
        b'rr32mFAmvr9F5eWrSH9JjFqRJWCXloYV5UUrAfCg4XveGDQTHSghThMpGMAIIoACR6pb2u0A22snnIRxkmKB1a41mejKAMRZU24sdq7GpS7+s32qgQJhdQcDPVi31NXH'
        b'9gcVNVL8CWXNzZPz/wJdK0W/Vl8i+OH8//rW/wX6VnScJiohQRMdHRMdGx0XFxvpUd8i/3pXwiQelTAFvwGMRfSOusWDZhaGL1xiZeygazFS3BCZQfY5w9My8b0hgvw6'
        b'z5MO9Qx64B0DoiPVoIZacYurBoX3R/ty8sxx9jgimx5BD+My1OlZILumZWaLNvZRK7nOzBudKcAn7dNJ0e0T0CZrTlaOcG8RqX4RNFWLm3GtZgBoUz6gc0A3IeZO7jJ0'
        b'CB1AJ7wZdAG3+2ajTRn03sJcdBtfsqajA4txU1pWTga580gjZganiHAjuoFv0EyoLQfvt4Zm4Z0hRExXp6FLISwzKgrdLpFIUJOUZpo4E13zxbfQzvky3KTC59GlbFCw'
        b'OCYoWoSOoXsrqcKowc/GwFx070vHB4Cqg27MJ/d7RqIGybpUvI3qwQZ0Eh+wptNegU40MVxJrgvtj0+I8D10bxQF0/lJ5BJfRtMuLpRfCUli+LtIT+SF+ErRHdCMmTwm'
        b'D5SJRjtxMtLjTpMvmSaYzV34Vmom1I1b8Q2iejagCxDKxDtB/BfhbbidWTZENkePHvLq9h68Yx7uZDi0mWHSGHJP1307kRrL5yVGMzCBFxmihHuPtJP9u5TZ43GrKAG0'
        b'iggmQjHe9M3333//3Exy+yyTIJ5dKO+Ij+c33SfNkBL5c648tFB+WZ/H2Mk+ILq5Fj0kk9NE0QDXpoYvJDcRR6QvAGxIxY25IUrczKK6RanO24eV6CadP6nZb3niPHrD'
        b'aiY6OisX74lOFzFsJT4KPcQX0Y5UexJB7vPDB/kCiAh45hN8GV5CMCZjgczD7KDLeLeYQTULvJeEolZ6v5oV3Q1x6rsZ80LwnlyZn5taO22AVBHsj88ssVMt7cjwDdZ0'
        b'VU4WjAg1IkCgbF69ZZR4nwRdr1pP9Xt8EjXNCOOvzlRKGV/0iPNDm3CnxofevPtpVg73fP4dP6ZCG/zW4i+Ngxk7uSsbt65Mwp2COUM5kfgnpBLUwnUROVnzQoTqFro6'
        b'TzyLzshxyyq0g84UejgEHQlTp4WDui9FzbgpkIvA1+ZRVMKPuIgMqhBygZMsbAJqGqwUURtBND64trsQurCBi5jQj6aMRS14l1AoIQAKwaSeo4d/QqVz3Ye3ARCrE98Y'
        b'afQqf5e1TgO9SLvkT8tbpmTj6YHbS9b8ds2hZ/69ezAacFY5v8JrqL+GU7YHRp177a5WKa0bc/x0Rf7O6S/cmf+XQ/ZZndF/fuXMrc4LJ6eMuKzcdyDm9V0TNouw9v3E'
        b'PZfvdg2OPPByyJdhqz5I+zx0999HVXr96tyfUn2j2MTpWfP+eXbIpxXvZFd9Mt8+yef0t68tW/7e2jNf3EmevdP0ifrFzV9sjYsKOfftrtFflc5qnjLkRf/r3m8n7P/8'
        b'tmF/lfr1lVf2fzxh1+OdH56dvnt4MZ7yq5wNe++n7fkwL+sCN/Yz+ZJW1aKMZ/csmP7K0bcnXfB79e81f92tuff32euSK15cWn13V+Uv1lnLV32mOlu9f8u35qRy3/Mj'
        b'/l5xLcE0t83bEHFw86G1EVbLvNdG/yM69P6qNZ+0fzniu3fPHr/yxeY//vUXb3z5gV9Y/WO/av2LmSm32h79i/3iFQuKW6n0o44aszLRaeru4bA+4LuojlogRuLDNmKS'
        b'CQvA550WiFGrexogxCuoRwM+GYHaHBaIanTW6fYhluFN6By1LuBadBl1ZnQ72KAzaCcTsFBkwh2og79etwPdRtvCQtWrUQvvueG9hEOnZlfY6FpNR/fD1ITKhxNs2pmJ'
        b'D3Aqyxp6A+QKWLYXMjJDpQw3Hh1bzsaj4zn83ZN30Fa0HV3IzAoHGoi24b0ZLLqG9qEbtMXp6BS+ClyBd9UA3rVhDX7ATZRPpPYXdABfl3pw6WAYRTneZ5X4rUPX6Tyh'
        b'zfjcLMiIbo/37KtxZBnv+FIzbo6VLDEVYVnU4NMPFvtV3CKCsd8bQseJrq/0zwgPWYS3dRtZKkUb+rglSxn4XzK3eDK8+BMTQ7cGTo0veUQyeIZ+OLlgeuk2wJC763jz'
        b'Cw1xxH9kJKT2Z6XUi4R4lARBmNxSLOP8qY+JD0fCVYPcDBvdrQrmGjlvMtGRh548DORRQh7kvkWL0WlGcZowXCw1Xk9zmbEPX6feWbHOWZPR2Y6fs4lum80qeOS72WzO'
        b'hrrabHobWrFEkLTIXrj7JeeSGq8ahm6RsjU+1NLiWyN2XnIuqZVuZTZKq6QbJNSyIqWWFUm11NNtsKTyUcyTYpw/L8YNA/Ynm0qYcqH8dlYwk0djf91PzFxngFZPL5Rb'
        b'C30YO3/VqjLUippkq0WMSGrxZxP80FVqNkZ7jagjFzXl4aYFWfPwjbn4xgK/OI2GYUYMyhgkQptR+wI7NSG2DVLl4qa8WI0Wn8L1MSBFyVazwHsb11DyPwGfQtdzZ4P0'
        b'wtfFMpJQFh1IG8G3vw1twSf4u8zRyQBmMj5ZyL9FoA7dxcfxCXyKI68U2DCBGYw6tbTGEtSGd2agLfPVmpioWI6RVrPoMGrH+2jqSNysE+4Mx7tGO68NNww1/mtokcT6'
        b'BWRZJrk+K+dBtihSfvMPGV+cmd6QNzp0QdGHyfsWD9n35sWFk8bNTYpMeD1y3edjxw1rfk6kiYz8a0LCby+0fPjL/3244WbwCyXt4iFjSk8dXi3x2frWuytfL545Y9CI'
        b'e6kRvpuPDx4oGVP3+t0zJW++6xu1fMbMy5n7T39VfV57/sbu6SvfLBne8v7gj8pVSeP9t+h//9PlP5mbHX3stwHjyy6eUU/56bSme8G/fXVZyenqyCHV1tXfNX6zKv7j'
        b'MyO+v3qn7jcDjw86oo5JjS2cvQ3dTvvb42cbJp8vX/X12i+vN2ptt4J2fiH64o3m58oONPxr3HLLi52fjzy68XvRx9HzfrU8XxlESSM+jc6uoFf1e+F7ICRy6Di7AB1H'
        b'l/lbL2vMQLYdZPVqEKWq19AOmhi9Dl/sJqqoJQzoKjdxGkNpZSbeEu+JpuKW4dRLrhDV826EN/BDoJyUP9nQflcD+Sr+YsdheEtSRnZ4WpYOXcLNEei8mPFHD0UF81P4'
        b'ARzDz8pwQwa9512MGvNGsug4voDu0NvgUT0whibHbdYDQIaDyslt1mnoAC2eJR5B74qfNcD1qnhUO5xyvEjA0Qx3J8iBxMyOLomH4callOMVxuKTGd1OjtkwIpIvaKUI'
        b'XUwPpJOhLw7L8OhfGGaeRfgrvrWQNleJLqFdxFGVuiuiK6W8u2LASNEK0FZ28feUPigT+OuawYJLJOGu69EmOp44WG3nMlC93dV4X4lvZPCTdTU70OVi+6H4HrnYXoVO'
        b'8qmNkxMz0G4YoNvd3hXLaGoZOgqyOGqYCNXinTnkDlTUwpWvsTwdxf0/ui/f4VHD345PmZOumzlFENZD3Rap86KYMCaOg2+eUcmBLvMfMWVX/I4BCfGujjJnuuMj5cSc'
        b'PzeQ8wFm5upPwzfPMymvbvbQ5cVboK1dEqtNa7F1iSDfj+VIEks5+V3mZDxmJ/ehjMcEj0uscDEmZTybmN8oenH84Tv6X/DBEtxxvv2wh+mAP1hlc5zdEEywJsEyYtHb'
        b'7BYzTStTaImF38XQ8lTWccUqfaUV6qmw6K3Ep5G34AgmKavTLC+YczxZtZ+02Jt4OxjpTlGlTe/B4uTko1LXCXPxh6fv5NCh0zNRA24HTacOXbWNw7vRtUVAFa+iC/NQ'
        b'rYQ4/orWD/bh1e9WdNMfty5GxwCIakZtx/vthGisXk74axDeJ1uNGhapcHuGWi1i+qM6ETq3bCBlzD8zi6hJ5jnvdZkPF4/m38mDT8UXUMZctoCUk47Be4rQA3wSH49i'
        b'QmMlCei0mbI7dAjtnERVMtyKblO1DBS566Cz0k3a3WgL2sOzcQ2qc3JffAi38jr+kXwT1drwphCGA7VtId7KvyPlPH62KpcwbLQ5CnQ61MQOT2KMFe9g1loP6csPvpv1'
        b'svCikfjoe9NH1J/c+554zycH6g98MCHrLF7wcsLzoa92rM+N0816J2PFv/8seXHquK6Wc+9t/nijduLH215O//nsWcvyMs0VaW0vvHS74ye65/45qbhg5Yj8Kc8o3pi0'
        b'7vrRYzWtPz1RPC9niuXX1mN3I75/Z0D+wQcL1l/65d4DU1/VZH4yddrYsxNTbm1TSnmd5Qq+ks/7+k3PemJHVILO8qL4ZmWIcPsvi85LGekKbiy+EmYjAFw9HV0MU2dx'
        b'aWgTjPYsmzF2Pk+GW2TzgGvxL7ngGCDuvnoOxJsdGynFLxgeSxo9hw941hQeojZazRDcUUz5D+U+VtwoMKCYIUrpDxCMXrwOtdYCstS6Xx3C00iTWNSfiuT94ZtQPLKf'
        b'GgQ0zoVsCEWzf6RD4mp4/PEJynS4F5dEoQkl2yWu0NpKPd+JHscIV1CTnUbyZgSp8150ca/3oguU6n0R62GXsZtYEbph1a4hv0wmV7L19IfNSMcnKdIMilDyK1QBtNbK'
        b'27MJQdKvI6dbiXk3VF1lrAgNpw0JlNHi2TpsJTf46Zw2aa2luNS4Rq9W5BAT+lqjVe+kfrQOOgCaXaswlJuA0vdBygiInIf5nKRMls2/p+k0kIIHYanh5DDLAXwyFeSN'
        b'9KxMdC4vFYSt2nA1yACpeIdXBUiBnfZQKBGYWJkByyg9awk6rcZ1II7lga7eEDEPpA1VCLnCJQPf9ELt0ybzasButB0fRDUgm7eiC1TZF5lYtEWGH9BXIqHjMtQZ5sXg'
        b'uxXMOmbdGPwsNRuhM9kTwnI4YqY7zc5nQOA6jpuNmS98x1g7IXnxR1OmNCX5c5HymS9mD1xcffxNUYXUf/oLEsY7ZFPo8aPTP8g17UqtLXv7f+YlxY9fMu7uX17+pmlf'
        b'dNvzs+8uCFjz69caxq0//bWh6Nf/zku/k+WrGsM9v3Jiyr1XT36lrKtNfP/i0cjNn56r+fuYgQl56/2HN05UTVkfvL9iinnXF9Xi968Zb0kr3/932lJ8Ufb1dzn7/iVD'
        b'ZdZxb1h1i2K+Oyz+7NLO4NiNpvc7nvdJWhb7WezPXx90YUXinqG/UgZQUoMvBW3AZ/FuOuWA9vEsuozal1FaoE0Fqn1xPBE2hZecgVzLbURHFlOnjEVobybuxNfXgizb'
        b'rqCmF290hkMnJs/nqdh9vG8aLVwH0ro0GzUWc8PXjuJfirQdHTeQl7mFq9OS59IMvriDw/fn44e8GH4SnULPZoSjnTlAiW7iM+SlAL7TObzPF9XZCEhSE9aTCiJyVES1'
        b'qsCPuNAFvPFl5YQswiuUatxMB4XrpAEaUQk6NJeqCWhnJd7dfbn6ilLUyI1Fj8p4+fwwujAmLILsIqjUSo4ZhC4H4CMiQJpdgfR8kDoNXafSdQTobNLJ+HgwN6iwH6+c'
        b'bOqvUsdmOBHVuz+HjuE6CZ0N74V6opsIk5GCa9FBbrB8Ki/nHscX7Xl2F0GYSsF4Hy1pRG1yvkfQIDrrj9u48Ln4el+GmR8g1S7kWUyWrrtnC/l486YVGT2EA3QZ5FPe'
        b'VBIEsVV+TvJJSme7vR/A4k6j++gkx+ftpts2eHz/BN3eOtDtfQFuDTsOOs+ER7ZlFvlJjg0DLRH+KSX8Fwd/wU+cqSfu8Lry4oICepanS1ZhKa/QW2yVT3OOiHi8U2cZ'
        b'an2hkjBlOnQE/Gz0/6+bxvqEo4W8tuMPjOAlIxOLOWINY9j+4zhBofjBJ+cvkgOwGXagWs7254bPHRrvP4w3/TfMTLeStyFa/f1F9GVkfiM4UHN3TqcvOkT38HV82Bdk'
        b'F0DgHRNwoy/Z+phLtjyGR4nHlg/9L71mqOTJoxc99we9svn32m1Bh/A1cshkNIOODhhtmsjbanbie2EZatShiYXC4WZ8k13NLqJsAXXiMwO6X+GG60fx5hgW1dJNwsXj'
        b'EejAaeFEKooWg6LZwNni0v0rje8OrBZZCepVSj7/rHDZcx0tx1ojt69mi73+wJ0+M2273HdIUnL4R/1P9/9oe2ZhXIaP7+K2Yy+d3hq5/djWY3vSdrPjgl9+7nccs3J5'
        b'v3XGk0oJb8hAp/EdxylCKXo4lxwinI/v8NbqNhtQIzdSsUONrmbYeRr0KHaii7W6swjt5FTeeDdPdc/hGlyf4aYv4yZ8sHwl2kbt2eOnTCNbqHzici4wWl/U55ESOShD'
        b'IIPoC4gvAaUiA12pyDhiZiVUQwxPy1rn4hB3iUmBLil/psvTa40qSdQ6J3qTsqM5R/2bhM/7rkId7557C5/wCQtJVy3Qp4ano6YIfi9Ugdsl/SXojBv6DBC+rX91vdsi'
        b'jNzvADjJ6UTbvPNFejF9vRtDXuzWxOVLICyjYW8alkLYh4Z9adgLwnIa9qNhGYT9aTiAhr0hHEjD/WjYB1rzgtaCdMHk1XC6cFgPrG6AbiC0LRfSBukGk7ssdCqaNlQ3'
        b'DNL8dWpIldJTLGLdcN0IiCM3ULA1YigxSqcg9060+bRxbSKDqE3cJiEf3RADB3HkW+T85mP5p5jP4fIUP/lbN/pQANTl013Pk2V0Y3rG/WdP3dhDwbpxh7j8fvogfT/d'
        b'+CHM0eBjzFaWhiY4QjRHf+oSyJ/vkcGceAm3bQygzoJedJ4kOqUuFOIG6oZQM7Wmy7sA+Il2Noix9Ky1m0ncXfjnXQ6l9MV9UqchXNKnIfwpXonlwxvCozPFPhPYQGLy'
        b'NiXYq/n958pljVODWA3HzC30j9lQxkd+M2DD6KXslxJGo13fKpnKv9wUHZoz3+00uZuKB2SiAZ9c4MXklsgCl/LVzMkfM/fXXC38Kkw5P2Iw87Gji/RUnTHO+xprJV3X'
        b'KG+NaLzqt0kjF7+bnVIovnn05ZHy6cXKWXefE89MNawyHbj3zOOv04cGlL4WM3nXeHnVscCVCfHRt948/j8Niddf+8ULQV7vnOywzx2YWrXu64Ev7K/OjhrS+cdPr3QW'
        b'vjh/2tnDQ5a8U6P0pmIVPhdBzbMt3oTRiBhZHmcbmcKTtO0D0RZQUa9kZoWPRrdBeprI9cMtfrzz8Al8UiFsAZbi3SrXLcDNEnqmeT66udxxnhrdmOk6L17M+CGSUpA1'
        b'99N9svFT5/Cns8NCVPg2usHng1yDhosn45r1/GZaiyYdqgvH54hrRBO1JDeSDbWDImCN15bwWv4x3NSP7MydTxByZaGLDGTaI0IncuKpmBqF7sWBxi6NAlkyjbykWIbr'
        b'ObRtJN5qI4pNDHqE96CGtVDeRk2wl5OgItScA5S/LgfvVEuZxAwpah/rxRPVp5b5us9ej3Ql1lFS1kciYwfTM9iC+ZKtCnIukSfeUsibG7sk1E2oS0y8TLvk3dtL5vIu'
        b'b6O5wm6j12B51tkllmryewN5PMM4RMGNbv2M6EH0X3eTCD3072nPuUoKSKf7OGaazAkLwrUV5wnr4d0XefY4bKqGWjMIRXnKU85+Ba4z10eXZjq69O1Il+Z7Hq9WP/25'
        b'bieU+mh2jrPZEWmO7A7nxh/VqvN0M0GbgjJjX2eM052NDiRiv8JgKS/7j8boaE27ro/Wspyt9aetEbfXH9OWcFBcWmArt2lNfTQ019nQkDyS1eEc67G1/7PDyj04EMf0'
        b'fC0fZQi1OSBJJvxBTLZiP/cv4bnEtTwpI9cAW1IUhueIBzDGhy3viqzkior3xvuTV8Gmatt0IR9laOWGTwp/W/cJ89eDQ3L3PT+EvuS18JbkM81PlSy90gLvnhroQsqe'
        b'pGNzgyklw5tX9CFsUq2Lki36MjEH2VpIpMuqfq5k4D89xJzbg9ZccbMa9mzk8ffw77+k3vQAVk/1RgDWiQUSyzRWQfppenPNn+bw17wNkaW+VUyRk709xPjMBw9FVnIP'
        b'3M/vfT83nX9vb4tu8XP70D50veWc6OVbWvqGw0wvZuUD6RY0WcnZyBta8S50Hrf0AatEb+CJBFidQ3lPl134JLq1HG0lxphQlZpoHVu46Dn4XF+KQ0AB9ek1VukLikzl'
        b'xau63z/ngOuyqiEu0+2e2+3NqBLqjOpJh9jJuJkXmuCxuAeIz7uBuPc2nUvSAWViSXC8KVUEcBb9p+/K9LSvQ+E81+sf7MXI33uBBPiMvUQn+E8eqMDH0AXIW4VODGaq'
        b'8OVg3hluC9kMvQDjW69ey6xHdfigfQKNNyxwEw6JPHJRlBeSrWJBxqiT+qMOfJC6QR7MlDAnSVemF4ZHpBUx1LHvQVQO97z6H97UsW/wgQI5Y58E0RvRA5BxhOuHBP8+'
        b'3rtPwBRXnz6Qi/bjNosPPrAaXaa0j+76TMdNk/EjUErdFet0dBbfNB7K+p3ISkCmOPNg/CuqIKTpL35vY8S0uTXFVd66yFTzpunv/15Ru3L+vF1DV0alZre83bbt7rO/'
        b'+5fh43I0oPmXW2orBpcdr92z7ZD/mVr5+yna2sAP20ZNCHrwq4NB46uv7ntojl89M7ranPX1G1f3pv3si0cfXfSVRSx9RTf2nylLBxa/9tt3TafCbDuQ5MSDGRUz/vEd'
        b'+/NzY/95fK3Si5o+V6ALk91MjAEafGyJqGQYfpaKf+gS3o/OuN9GhJpRE5VL1Qk2sjBRw4hlwjpLzve40sgyyzXTo3Qx+H6Bb6gguuajNmeto1CnGF/JRbepzIjuZuL7'
        b'1MuBCK4Ab3QRlGCoE231o9VKGQ06Lx0+cR0VuqtnRuag/W7H6ipZKb+sGyrQAXwCX3e3FpSvGNj9DtpejYrSgrUWo/BuUTcZs4AQa44dCTLmUMFvS85WBbosOlrQ/c3H'
        b'WkuJtRcKzlla3Nd4MzyW9Vjjp91ePNmjuexisbAc3bZZhTfh0rNmzjfhiumOjwRWt5iubgld3eJqSW/vwpb0WN3SbOqdPAU9KEDkHsKy1aOYUdqFVAWlPq+4Lj8sbJ5q'
        b'oQpdRkfxDTHj1Y8bGTTTaFg0SWIlL9GdntlMbE0t6M2fvP2TjpY7rXe23lm8uyF8u3Lf6O13tp7bmtiU1jh63+ZOCXNxkqzytb8AGyZYtHARAuygNhEE2ECdKlhmGODq'
        b'qVIxqkVXwx0z37fRWFpADx5Q+Aa6wtfkT10a3KaYZnWoKN0ebPS1xdTK04Nyi/n4J/JS+O6Ch7EHfPcH9QZf2rhn8BJTcY0EACylFgICZK+nBPJTXAIjyebhSYxMNktR'
        b'LoFmO8uI8D1WgjZl9Z9rXPqRL2clhmXp11mfFWZoX/oo5IM0Kkp9Umjc81mh0RDa/lnh48JVhs91nxVy9Zq4aPu1Uxp7x5qOU5F1keRd1yxjmyf/x99nd4uZT+Xa4faG'
        b'amKIcwFnf1dwWmS87wpxkRzgMqvdZZ4Orp7PqvYB5t3wKO8B5tbBrmD23KHHOijgGeAx/HqWCCta8p8Cu+eKdgCbEE5/tAkfA3DjPXhHeXSqiJF4sWgLfoS2GFtufSay'
        b'kqMqf84CiSzNCfFU7aeFau0nhZ8DzD8vDNSWGjKLg4pBODOxzGt3zo6QDXxrKaxg0qY33juc+BtLFjLccjYeX0fPPv27bLv8C4QbPF0A7iZMVxGAVw12mVm3Ap6h3SU1'
        b'aItt5ZZeaLTYsqc3MLfBY20PMDf0dwVzr51RBvCOst1+swT0XX7dmvQqfWWX35pye3Gp3kKLRLoHo7p8i8mNKXryTtJI10BUl0xntPJXnRD3W/Iidhu55lZvt2nX0atZ'
        b'yb5Ql1y/rrhUSy4OhSiljG4/WcilDhYiI3m6UJdsRC2hNRK3ocguH8eVJkady/nvfJrDZrSZ9F0y8k4LkrnLl/xynKum0fSuJFpTlOUQKeNFjvoVla+jh7+7JBWl5WZ9'
        b'l8igXdcl0ZdpjaYusRHKdYmKjMVKrssrecaMnAXZeV3iGTnzZ1kukqYvMS5mCwJA6qlLMIUMSbhyV0o9hNkamUH2lFKv2yoSCVW6r6JiXurtWr2B/aaonmM02qTFoYsY'
        b'4RgIuptoRfdH45sBgDscPs2GoqOD7YJL5d5iq21NKsi8NwPwDV+W8cIHOH/UgC/RGzaS16GHYcQ18VKIAbWmZqnTsubh2mx0KRw3R6TPSw1PjwABFoQrx0kd3LpUPmM0'
        b'auK3/hvSoKbWecxa3AhCN5OFt+GLfMpZfCI1OkYjRteqGXYig1pxSz9+A+rcRtQaTTyC66dEM9FzUCstsDIZX4T8HHqIdzFsCIPahuOT9EZudGwV2kxcMregZ3nbLcv4'
        b'5nP4MtqCttOy+LIB34XC0lj0kGGV5NTToRF076ogBt0k/qZHQHRszIolb4q/yuJWfBrfohP6y+wwJi/cX8oEFqYovey8GpHGSqAyFtcFMWwog9rRlmB+A+XKZLwlQ63K'
        b'xJvU5FxblgrXZ7LMIHRSPB0fW00rNC9SMNND8sj9q8t8hgcx/OZaO65bD1WKlqMdDBvOoH34Fm6nJNGGLg4NIzd7pPGCZMC4bNQkKrKielqdLWoQEy6PILebDr+hHME7'
        b'fAegi4VQm1fKSIZVMWg/uo07aDsjK5Zm4JYxeCd9PY84nEV38Z1yWpHIayqzgTnJMprCqLWVNp75igG00TGog0GPUBvDqkGBmmjnxawjuaAWqZXpWSoWn9Aw3pEc2hdQ'
        b'QKv6bVY607Y4XwRzlv5lYhxfVUgWOkWqEqO9eDvDRjDoYP/xvHdbC+5ArSCcl6KtoA/Qjfod3Nj+K2hlC8JBeE74iuhVmbuWjRQ82s+gI/hBdEwco5hI52tPdBj1xAvB'
        b'N/HmDHLzSQPeyXsR+6Mz6BraJpo6LY5WOCYqkakw3WKZwsIoU9pMhuLc0IUlUBsXupAOcm852kePd0nRJtTCV5edmV0OWCKg11DUJkb1PoDLBB+iktBVKC5FbePpyPYN'
        b'CheuTyE30AnlefD5hwdUiBLwuem0LzXyIGZcIKAIU7jh3bS1/OAWokP9o6M0UtsiOrR2dAdd591vrqM96AxgayC+SpCVA2S9xuI2L1gH1M/v4OSx0bEaBt1kGTaKINVp'
        b'GwV7KeqcH5aB7s0kDnMsIzVyQ/Cz0fzK2JKNaqLjNcziPIZNgK6jbXgPBUsVfrSUIJ7/XEC9enSFYeSTRYHogUE4ibg0HYpxy6IZdhI5dHMoht/uPtYPAADTNGYRpQnn'
        b'xYw8UDQAlgAd8PteMiZQfFtC7vMdqCvmUQO3RQ2Ljo9h8INYWhlof/g+xTLdhtXQBXxzMjn4mQGIUcwNM6JGvgdbo6uhlDgL7WfYJOhCRDCdhUy8m83IQBcZdCOX4crZ'
        b'6ahew1Oc+7o1UIDDTTAYdjJMlwhfoxvUqDUvFVQ1clK1kewlSIM5b9SBrtMub1u+nvkqoYNQgIV56xYKWsZ+1IzPoU5NjGQI2sOwKQwg5M4AOnGrAEo7ccOozMx0srch'
        b'wg9ZdBAyt9HqfjNhDtO4jOVgwYbGJa0TKHQ7emAitYnwFSCU7AwGHWXRft5J8ww+kJgBhEQ6E91huBVsBL6EN9O6PnxmMCzXcA5mc0O6sVqYzV2zKjJi0P004vIiFrPo'
        b'yDp8wE5uMRmKzi/GrRKylz9GzahVG6gDrDxpCD0TMD8VlFwQvWrn4hbiAoZrs8KB5jDMnCCvYQPX8wjdUYUvO09wsujCNEaG93Fozyxc133j8veRHCNedl5K7KFj54sZ'
        b'qrFNRFcsuBXiVjLhTHjhYnoAJQ9IOe9Lj9oKu/eWgLuImfHovMQ+ALXz830Tt4JaPa8I7Y/V4HqgXUHs8smlNM2CbwD5z8NNYtS+lmHxfujmYFRL3StwYyKq5Y8g485o'
        b'cgrZsYLH50iM+NwUOsXrcDu6ig/60uOwV4BFAMfs1NMKLKXoYBhMRxbeie7MSVWl84pfpJiZkCeJQndm0BHnBA5lYkwfegGObEgfWS0QqXuMGh/0IkfkZqBHQEKD0RVK'
        b'VZaicyMcdR6O666TYyYskEST2aW98kI3gXjMU0mDl8OoLsLyQDvQJjpk4MlLc/E2tBl4cRNw9PXscHLKgxaL80VHMhaQ2XiwFMqdArKRgM7ShnX4BGpzHPN2zATeMoMZ'
        b'hRrE+GYxkDNSw3B8Hz3AB0HoFOFOdJ/4ol0FRkq35i7h5hKyvNVp2biJnE5NU0WJmWHogNiEOgL4hbndC8B1ENDBEoAeMOhBopbS5lR8vNhZFHckkaIcFD0oLhuIb/FF'
        b'dwAB2oMbKLEbbmSMK0ooVTGhnWriqOiEXkAsbgwWrQxezBO+M/gY2kztAcr1o5hR+DK+wF9PdWIefhjG34sFmNUPbxF8GoajG2JyCzRu49dY43x0Ax8kS6NmKbpHvHIe'
        b'AcskXdKWwfAbiDRyfPwqWNtncSsvdJybgA5kTEd7VKo0dDEknay24Oki3IZ2oRq+V40DgI8flEP1LXHoOoOur4/g/WVuoHN2l0OVTAA+iDctFJnGjqe9MeBbqVY/Pw6d'
        b'NgAAd5JJ78Q3KaKJ1/ky/fPWENYa/o/q/jzzikD3USduEBFfuIByplwh4c8m34LYVhDcUsnZ78aMHBXpZCbQF8UwMbDcYxuojVI+dzz7mohJ/Zf/dPM7CcEhoXylErwV'
        b'36SmUhG6W8VUafsbrZNHi6z/BGZ1xTB8+a9+Zg5ODpS+9+nhF1YHvRUc3FjzbMefkzaPG8xp3/X+p8F/fIup/5L25j/4Dpx/pOWF4MxHXAAe++Xw73K/aJw9PPzew3OX'
        b'lYv2eic9f/7CPxe88aD2wWi/Nu/5ZcaTmW/+Jaj+XNqMPWerV73X+cvkoeN+fl56+JlF3le/+PTqp9/HaYd+kPtBS8bCX1xRnsh67sPB+7NP9/vl8893vtF6e0t81urf'
        b'hF5OrJv5kcI+cenMj0YvfTZm5s3kA9lFu/7UMiJ7Tf3nWz5fc22OrvzYX6fukrxUPdFrpn9KXNLkcZbbr73fb9eJ7ZNenLlzRnZCotJyfu7H11/av+XQgESvxD//cctL'
        b's14aP7FhzN7Riy6WfDyg6Tc/HfUHbX1G5P5fhRz8rmDGT/em4X23/z3jxbb2yt+d3/XvtP1XXvujsWRo/KTXv/7p3ZytS1b8zBw4P/ltW2zoxH52778gw9uXnzvfcmry'
        b'ia6v+135cMiCrU3vX/jdlIDO9f539ki/uTz+wJW0G+X3J7/xwO/h4VJTyt+PLLy0pfl/d9geHni2TNH5j4alG3JNZUVng/+iSrQOs94e21r3zeWXHtR9+a+0iMfDp70U'
        b'1zoqffuc7T7N479Pq/5tv2kDKtszmo40XHzrZzdnf5fywd7//WjWd58+Kjv7l1W74v93/62gR3/4x8K/ee3927zPg7Nv/M9nH1/pd21PSsFU+6d1K8Zl/WnS65P2PPpO'
        b'FBrwr7KHnyqDefvrXlDRdwqOAcChtkV48Ay4idqp3o2uBs8OywY5cbuU4dABNitZSn0z16NtxbhhiR9RJqSMeCYLVOcMquUdBQ4yQaghoEJuAamnCbhnS8AaP28p0x8d'
        b'EZUz+Db1c8W3x4/3lUA/zoWnOmy6/fBdEbqEjpfyjv2dw2H1NOD2qW7eoXjzNJocOYdcKR/B+4fCYm0HdnaCQw3RYuotNgRfQK3UIkyNfWKQRLM4Hb43mfrQVk/BHbCo'
        b'WNBc9jLcGjYZqNpJ/sa1e/heVpgaqNn17qPPnAqkpCO8v8YdDT6JLuAOKX8WjxzEixxOK506rZR4a6xE+2kS8daYq6DOGiPj8G1iFI/CB91u6RfLiMjG3xl3GZrYgRpS'
        b'wnM8uVc0opN0boFYnsF3oJmDM3J6Olho46njh18pbib+HGR7gqgxxJe4QeHPWz3DEiUA3VMqWt3kKFznYhg9tMhpGyV2Uc0U3jX4rE7ffTSCnIt4gO+TsxH4ZjLvXncM'
        b'tBaoRvDnwMciBJeOjajR043zP9rLs0uk1fFWG+Jo6rTaPMOoiVuumA2irnY+1F03yPHhgtgeH4gb6hXIjiMnodnBUIL8yVkZN5RVsP60RCDrT3MG0tyBbH9SO1fl122O'
        b'gb64ef4SQ9uPPWTG8aW6DfiX4XGemISIUOs0CW1i3hzq5gfs1gvPu+XU3Me/ZYmpkTjNfSw1VPS+Z1765PacgnnSUDGRN1SctfDnoTRxU0bNsy9leBsgYTzzktA+UKWI'
        b'nDqSGYlaQAymVoF7E7yVoaiVLEtYmI/wDSrT4hZtNjqB70dDZVFM1OBCWvtrQ2Xk6juNZsLnZfaRuQzdoWutEiIX7l05yhzNy6rDsjey33DM4o7lyjEf580XJLf7qAbV'
        b'R8eIicsIiPfF6J6a7xu+aoqOASqWBRSQ0RejVlrJ0ER620mgZuDdJS9KNHzN7y3pR4afoDH8wbi2Usb34XSMEClVLPpqXTGf8y/L/RiAWIhmtre9NDSez7kqVIg0SCSq'
        b'JBmfM0UH7J9hZJq4V2ZLTSP4nCO0Pnyk4fX1e5cY+cif53vxXVoTYFySupLfMwRNeCvem0uERnxfs4BI2ZI1xAZwGWRHOvD2KNQRrdGIGXZcv7UM2o0759GGn/Mbw8wk'
        b'4BqdYzu1IoA3g6zAO8fiA+gWv6HKVA3BzVQDsYDEVKcH2nfQh1z6Av/X4yM0ZQNuxUciUQ0+KCXupvB/Ht5K4Sgdiw7heiVuBaxRMSqNhTarXUPvKlJo1lQnSFanMLz4'
        b'tB3fiYWK9pCPBCSkHckxRKYCJZ9qGuhaWsTaOERqGsGMmJlHhz4O71/Gb5VC8f3d26X4IiASVZuubAzJVRFpjMW78O1lbBA6NosCfRg+4I+Ook1hsDrWMevGCghZgPfi'
        b'XSPQXnQBApVM5chAfiu5BgTAXdZZ/G4ysx54CN20pVDZOlMYz8LWOJSv5A3I84cnfBwtOB+0XTVevzVQZI2Bzq986VzZriRyYYp21o6SNX8a9+rracNrAn9fwcz0G/EB'
        b'dwdFbD70U4vfnu1/jJrz5p/6eR2dmSj5QFw7Q7Ni4k9SYpL+9sy9v3Upb7+WuHVvqO+xgXmfbGssDTlx9P2fDDoe/MtvShfPDv7qouHDC9L8jGffGZP659fUbet/M3Pi'
        b'otPbd+rPiOo+Tc8rH3Sq9WbHw46f7KjUXz60fUdKTWzX6jyL9qszn95bt/x1/Kbl7o6uvwT85dth/17yh4LaX5X/z4K9om2XM85N3KZZvfKDtmxU0LTuoPaF3/0/7V15'
        b'QFPH1r9Z2ANEREEQiYo1YXNBEFwBQUEQUEBUrBBIgGhYzCK41BUFRBARERfErSruuwgurzPd/LraVdPXVrv42lrbWlvbZ7dvlpuQQBKx7bf88YhOcpO5M3Pnzj1zzsz5'
        b'nd+QAwFJJ07a+Ya835K07nt1+W+nL/zR70545LKJF5STw88q+7zinic4P3dxY9P89I/KY8Pr1YNGNV6ue9Ojf8K9jJ0Nrx5uCrveK+nu4pK8/3L47OG1e72Wpd58cKx5'
        b'07ZPQOGUd0LHv7V6dYXvV2FrCv7xrcRTgxeK7dHEbc0Pw11EfWZWgmNUkTgC6sE6stOPbBNRkD/2JzzHRTm2wJNkyk5PKjZ2Gx/tibQI7iTiYukF9+QiJQGNrUOgQe9+'
        b'mQ33ksnRBzYjixLNo9MIXrEG1mA0eVQyPMMDxyfATbT6DnRqHY7ThF0VqzgM3A222C7nDgLbwQ4NNtLBeWTtPQswPn99cjcPVVbfalUSrSUX7kVDEDUoAC8+HE8Dpzho'
        b'+O6C20lrs4RG3iZgA7hCPE6k3mQS5sK1hKQnUTK9F4HJk/XLvrP43vKBJEOgk5sRCRBZTXIbUjqGB46mhFN8UN10olqcIOpLcgZxNz0AK6jiUQUuFpOuMlVOwqKwerLK'
        b'hzqltiIb61lkeO4w1RewrtAxnyqHDT4oV3VX5cXNBakvcBfYQnS7WUMnIHUiLjA4GC9Uo3bCVnEaD272TCdeBguKYTvrrwqvpIiDTNxVnYcRPQ7URYIrJFNtgg3D52JF'
        b'EoehOATPUD1vP1jjQ/f4Ua69hn3+cHiEeBRkwpZAE4eCctChdyow9igQ9SI3bpY6niqjbrA8kADGsC7qBq5osC8KQFpVrbFG5isnOpmxRnaeS+6ScFAQ1aSQUbvLyDsW'
        b'HAbtFF3WrJ0X4B8sARvEnSF75Bz9HnKP9sP42OWO6FPZpvqUSsDhc/UwfXeiTbmjV1/08kQvfOxCIPvuJIcb+x+/9LFnBFxHjoiLN08FXHsCplri0qm14IoteKhZQUwZ'
        b'O6ydQMk3ZhSlBpPdsy5VohJ4tKAN5C2J/FNhjUTi0ZV0FLvfqhbhhLjkEl9d7Kars9c7b+o/4e0l4vZIkVHYa4d4YpDterKZS7b6dIKslKgZUdOy0manxKbqeGq5RsfH'
        b'qHqdE/tDamxaKlEByeXRDvrrcRpUmOYsEPcVvgZ7nrBXj+BQNi58F2cXW3d7oZ0+IoMtub22Ji9HHr3t9Ijb5Vf9S2jjwnHnecaQhZdcsNvVWLTbMEIk4gbw5sCjYLPJ'
        b'XrOe10Q9oSv/Kr/BlfCTuurfZVzDJ16NncwPab4Y9+Cax5fZyewNbKwOMkeCVhGwbKzO5NiFHGM2VldyLCTH9oSt1ZGwtQpYNtbe5NidHDsStlZHwtYqYNlYPcixJzkW'
        b'NPDzGNwqWb+d3AZbjEeZ7yzz6sfsdsHIDfbYW3/sgf5v5dZyZENYsLUdCULkVOFaIcxzIJyuhGkV/eZAeFP5BOliP0eIe0M2sIZTQTV+QYUz0vcHyQYTTtVesv7EvfIp'
        b'llM1ISn2UaMJPjlNT/aJfqKEqiIxJs3APEjSIhke5IqunIwmB/5pGCbNEh+hT8U56mIlJmrG6G4c8JayS+KAu/ISDY35TKDeXeIQG1O3diFhldjpHFg2L0yEw34k+8L2'
        b'NDInpsSR5S3S8RYUoe8K5TKFthB9Z1+Crqe0WCVTdZK8dmNXNQ0ApQ+w7YBsJ0d2u9fJEADqcfyq5RL+7fs95lfFXf6n+VUfT6/ajUrVLN79T9KrGt0EQztwiG4rrUA/'
        b'W2pDkUiqLCmQBplrSoQotwBVmUsCYVtne7VO9mqG2PUJeuSxZK9o/NGYwTGTZ4qU0hzMNY4+GodhlgR3CXBMicvMtsK06aRvxSONusJM49mGoGfgMVSzlmhlzQdEsEQ1'
        b'20NaWbOFdlLN/gVaWf1zTrudHokUMvaGhTzuhumFAxsomj0SqeT5CjXqYSSqkEQjwylQpGVvm7YIB2x+YvZWV7psckVD1w9uxRcGPl9WSklQIt3ASb03cXauMZ2pnrsV'
        b'aYsmHKtrIwXCBHCOFPlyXh9GjGxS0fK8cVHJsxkSfzcXbIeHzBGkdpZI+E5ooeAC3E8LbikRwP2w0Z2U/G2agCxhZBfLExUyIcu8ejUQtpmUDCrBZn3pRpaFcYNBG6h0'
        b'AntGJ9PFiFy63JKdoghs5towWizs4QV4Jtpsi+MDUo2LWgk3OviCjWDLBCdSWtp8B7Is9Gbh8sCPR6AunUhaCQ/zTFtZgTpETxLbacx1aeV5J7BPAw+QgquC6bpM3VCF'
        b'ctSKYur6DToSXE3KHQ5q2WLFelvFpMx2cMQJVk4EJxUtt5sZNVY9a39+PujVjl4gUhA7XfHHyIaogT/c4sY1ZOcL+px0SbMdFSl55/nM19ZtV7coT8nemVt48cy1mqNN'
        b'yraGn35oGzd70r88Pjh5a13m4K8dE4pyfe9MWNL7umzU+gNlvT/+ctJ3X++63Wf5P3YsXdfnj7R/HfxqSHCfhqyG6q2Fy+d/M+uuw+9rWio+rqh6a6rqV47NwfAVCWKJ'
        b'I7GmsuFhyrsqMTEbYSPY4Q3XzqNW7kkerOxGMsuPEtrDQw40JGdlAVhlKAVZ58fZcWbD+MImPjwxZg6pLWTGImQI7YSnulqiyA7tA49SQ3RHCNiJLMhAHxYIfpQbgsPd'
        b'0cAdHYtiUQnb4/VGMrKQS+ExcmLAMg2ong8vG6w+ZPHBi7CS1DwBVpWC6kDQ1tWgR9Y8bJ5Fg6ZeAAcVyAQ+DhtMzU9kfC530mBsixK2YFLe0ngX0BwYH4S399RkiSIe'
        b'x9/GWm2QLTMNlNuB5n6g6m9T5Q3YRfzAGFlsK5howhbLse1kjqUssiTyp+FIT86K1A4LPLIXcdKOkw6cXMLJZZxcwclVhnm8Z6t9TwpxNrkmCZKXamzzG5lyK5mbJvHU'
        b'ure8p3g7xyyDwmQFmZaO97sJ3rGzJiNCWfyVVULZnkEeDVyfRtqTlUbN0jfq0YAuLSDawJ9hVtXrSVZqzTTU6ktr/ctEtvwspBtZqXGeoUZvWqORBvXkF8nPQgqQldqk'
        b'htrEnUqStCui9Mmocg1oS71KYqV+maF+L7xAYaS3/AnaWIcsvd5ipcZ8kxpR/xp0HeMxzKVAZLLWYXCHTcrlsQ3B/uT4aSX+sNh3n2wu4UAMXNZYdSTRcgV5AoN3uY1F'
        b'73I9taiNW495iOSYcrGnNEQk85OwEBmzDnUrErMQGbDC/oEif2PIMjomGGiUyZhDheiutBmYmqLn9p2hojGi1OJCbCVQ4xqHMWNxx9KcYq2GJfdRI33UUt/gP0ykIcdd'
        b'IlPkEZoVDatvm14U298kMiPqtnw2SJsZVRf/xRtogaTWTLcRYUYGi0is5x6xbLoY9ytVy7s9mCJxVI5KnltQhGlPWDuOhGoz29DOcaBWK/KLyFCg5CLdGK7UIoXxVSmQ'
        b'SZNvgcFEb6qMIDc5LMJgseCaRkgC8XKInhUX5zDQ4uZaMrLIqFSQ8zHREu678IieEzXlmV4QvmqFXP330SyJMa0QIUSSiPz9C7EZjS5nsb//nyZeEokJyVIQ5Sp6kqKt'
        b'kCz16PwnpTwSWaBqskR5FNyzZpiAM6wSH4kNxEcjJKLMESMtExcZAzzY26iV08tRFJGGEqrymGnTZs/GV2YuUiv+K5EuLiRxXuUqPDEFElYzg/Vr1KCR1htklY3JdC2E'
        b'Pi3D9E+K2WZRtceYwwlVHzLcMh2XMRxGvzJk9Jigb9ETWaRW0EYV55lnt5LNRyOD9Ac+gQS7lZbhzz0k9sF/USaFqMmimCK3QKMg7E3qTm6x7s+sxTKDRCMwP7Jci4Sr'
        b'oQA0ghUitouQhCpET1xselCaVJMjxwuN5rmmgkRouNC4nEpt4QJ5gfn+DxKFdMlGapNq85ZoNXI0c+BAx6KZxSo1aZSFMkaNEUVp8wrkOVr86KETorSaYjy/LbBwQugY'
        b'UXyRTLFIgQazUolOoAxo6i5XbuHsMHNNfvIOGm2uGIVRswqfrFnh5sp7sn6JIB3Z2fWP6XmzX6bRkYxXBLu0+4lHovHl56nQ1Yhx3xraJM1Zos2XWB5+xqeLRg+xPABN'
        b'Mo6IsJQTDbOiYd3JJemPoV2LCbNUTJi1YtCgMFyflTLCjbNZvLQIk8LMXJfFCY2F6yEJx34i+gDSSZFs1YtycSqdYy1O2J1oQMxvjqZCeoR0HHECOpQXof9omIvwHBRu'
        b'hSLdgCM0LWZkl2JGWi2GQA5NGPjEhHYvBs83oRZPM0AU6amx6URS4y9EYvSQs0Mc3XbL3aBVYSZCzPHOfgoUGel2sekzROIMuL9AhR5S1JZRlptihI7sLMzwNdsofVHq'
        b'BVqVunujrKl7ltRLokr2XPMzqGhRJov7PdNhCI5zjCgJv4kyRw5/uuenjaSnjSSnWb4beoAoq0Lqae+RsWxtHBD0KDoFv6GM3fNZlmJxcpWqaNhklVSLEmXwsMkKpN1Z'
        b'lloku2VZhcuxLJ9wBZYFlLWakVSKLUBKGJL9lkUTaRvS2WTmm2Gp85AWK5drsGaB35GCFWZVv8spLhsjwjvGSH/Kw1or+gL1ueWbik/C4F16llQpwgdWz8hVaPADiVKr'
        b'6h7FLOOc9AMpOBDr6UEhI8LC0Eiz3CYMFkYNwm9WR2SeFF3tZCRUrGUicGN0h/CbKDPMckZWzOlJRq2MaD0QeowoGn2imnDmyNFW8xsebXKK6ead1f7Ww6vZM+n9sSys'
        b'MawaqWjRUUno9liWiDmKXFRg/CRUtZkn0gQg3T1GOkub9PkiLvU7zvsuOjglloYd6L9C1glqY+zHgb0E1AbOUlKl1yP51Gtzcn7ywuXJFGa3BBwITcAYO1gHN1OcXc4C'
        b'kv2I1IMJxK63AyaWFYzsRbODVWAj3AQ2weMEgRfMBA+G24g7q3fMEJZOpgEcMcIubwFtpLg+Psuoh7LP6pSX3KQM4SlMmQQbwYW+ASg/pt1Lxl6A4OjUaSRCURoDT4Hq'
        b'GUzZKId8x8UE5PNs/yTu87ZM2cn4QsHxZzJiJQyhS5wJyuFBc4GIUCnJ4EBaHN2LMKEYrAHbBJI4b0X65ki++jYqxK2ucG3ttKm86cLyI49eu/TvqgXxD4+vnvKywz8d'
        b'J//0mn0/z88idry8wcluzxmHXZFu3yk/GbHsjYiVOw60Hv69fUPyvMW718ffhc33F7d+E/ngqe3Hsn/0u/3izi2Nb6yPflA6+zb/x/wkVcxbo5s+9JmiyZjz6/Xo/aFz'
        b'Jm8fe23xw//6SBF6v4a3oTG06LPII4tmZ5b7BrwVNv3uTJDRcnfQkJ8S1qRPe/WZA8UjRpSsCWrXrvuIefuC9uenJg+cF6wcEdd+40Dj9KVblo7bXa1eEfHxC+tie3cM'
        b'uBbTtsvBV3D3j37rM9M2Xr3fNuVeeJXEnrjnzYPlUtRfp4z57LhBi0E92TaaCffBlZRcSQsOUkwHPACbaYzydR6wIgM0BcCq5HhwlM/YKrmDQDWoJRtjUrABrqMbY2Bz'
        b'uAm0I26mZhjKUQLr1NTnCW6C1Vb3i8BK2EbAIGDrgHmGqEfTtEG8AOOgR7CW9ckEGyPhVk/Y0I3iDtPbCcAlgkoBZ+ElsBWWw9MJifEchjuD4z96UXdUhuBviseNndjI'
        b'PhXeMDbZp1rBJNsTnjo+x4XjR6Ig4c/YS9CR3aPiEh9DL/Tel+PGWSIw7MZIZbIkkyAcnavV2A3baGPK4YkaLuEbFdIZitNwJfPN7k41DTLenTJppXlIBomohB2LmAq+'
        b'IaLSf9h+uol/fEu6s+YNoeL/nB12wF85lReZHZgerWWjzsAaeEitdQdHp4cOhzV8Bj0fnGfgHni5E5USFQzPO/EYuB8eZDKYjDLYSJHj1Znwaio9KzSVAzswSL8SVpPK'
        b'dmVibMmsdJvh0qUviUspaCJjPtgdMorjgQEQWxk5qAXnKPS1ceL0kFEe4/kMRZy0wX2kkIs+2NnhUBpXlC14zjmC4kAWpQsZEVPm61qSLUgTBVBwgct47BtS5uNYkq38'
        b'elgBzVlegn0wmqLsU7ITH6b605yqXIwtOVSIvlSOzx5Jc/oIMbZE7OsozBac68NiS66rsQ+DyEUgzA78t6cT/TJxCW7SrTE8UXbgbx6RNISFClz0SE1JScEgkjmcGEyv'
        b'uZ+NOgH2pY0LGY5pBeFm2MaB+xm4iquhqItWD7gzNQUN2pJCLjiAfgBr+pGbAnYuBo2p0+Y5Toc1nUgVcA6epoDwk+AIaCJQFV9wnOPHgHo0wTZSCMYZNHnWpaIyykOY'
        b'gcxAcJFPsUKn4N7CED6zxBNDhTzganJnFcMnYdQJaAIXMPIEbimlUPdWsHZkJ8oEbvHkwHUYZrIfVpCr6qsEV1NTRDzMftgOzvSxBXtAcxYN1NCh6QWr42EzvGgSm08M'
        b'NlEsCO7v9/pjvxNxkmN2duKdElvatdeC8JdlWtvs7MCbw7P1QHLYFJqKu3aWjIFrGClsU5AimkTYdWd4sF1k9tzXY4ppLIEVTrhHwW4JjngAOsY844RGcrsHGa6weTxY'
        b'o3YOIb22hwuOYFB5B6xT1N89xFVHILnz7XOjCzexLL3vJeX866V/D3ZxWLFqdWrKjOszRAMHDvzBr/rN8D17ZmXYXnt248mlg8vDmdApu3Pec+kVK7v2/S+LxhffeW2w'
        b'vCHlxSFX/9l3fvy6oKdnXCvN2OYfd2RnyxsZp5ZNf/2WRL5r5uTZ11N01V+uHuXtuuv+7X23K2e+Yrs9ef4zG2c+Wrk7u/WDmKaAt6MLmh0TK8/LNZHF8ydH66Lbo5d4'
        b'f3LRP8KppvzhH9eTYp91sQ398NHl3Kbl2WffzfI8+PHe9gMV41/J/P3ewjULr7UOG3M4eXjrkq8HH16iqa1Z8rBpeNSG1nG/rB1aalvPXdX8bfDqfuuahqpfyavkvdK4'
        b'beZ959tv/jwn7cU5p59e0X7ps483Jar8il760S/85qaau8oNse/ejC6be/DS4pannmvZ2njv5ZmvywZrpt2+O+ydjYtWS2QSdw0OJ/5U7z50orY8SSNFYSOaqNPBTgpR'
        b'bYB7XQMS3Jzx/I9y2MMOLtgE1sDLFCt6ARzKR0peIofx8+MP5IBmpBtSdkB4eCg8nhCY42QcghBsBqfJrwX2OLKNHrJiA6sJ8jUT0mjdiXBnRIIZIMl8J1GsjYOXjLIl'
        b'7IKtcD0LJckEh6ijzGCwj0I6T6DfVhpFLt0BT2AsCRr2z9IMmxwycBjv05oubkHeXkU0TuJhhdQI9WKLrmzVcu6gVHTpJHjDpYkEjWLi5MMHtcTPBz1zdaSD+oHjc1lS'
        b'S1AJNhLFy8NGQ2NkdqQmmIBNwAaRC1jDi1bEkAzT+UjtNUKZoOf9IEGaZMGjBOExF25WJxjDTJzBZZdneDE58CL19dkGNhD0a6ejD1wtpr4+40qJYugGrvQ3YEjAjqXE'
        b'oQg096UIk4M+YF8CIbmvM44UOQxeIf5GOaIxXcFDsB62UX+jg1NINw0Cx0uNXa+owxQ8OYn6TGmGWQwhZ10LW6jXwoq6a2ElWOtiqce4Qi51+xeyyFmM9BAiLQzrYEKk'
        b'lXVSMQrZ/9TpH5Nb2HL5LAJEyLr/Y/8jlmOM6EPWaczMX1o3QjOsgvXvqoKtZHaZxj7sWikqB7Ps/IfXjPz97/Oa2SURljJ4ICadspqZZzRbnY1JzcBJNKETsdim8Sf8'
        b'ZAfh+U6OsqWgneKI65BIXIWxnGD/sjKmTBhGqcvaoqWYoww0LSQUZekRiucXvMFVn0S/HfEQYYIyMFwYk/++i3D53mjfW0xlfT0vZSEncqp4tzp2lfvuOOno8pyAAsm9'
        b'HTlD3T7MvPeq93SPMjefL640PL/z5/Nun6dPcS08tGdo/J0zjN31Kx63fln36YXGG6FT3xRP+REAV+758DeSv74hSZhwQZmeHZ3eUPnT8JUlQbpj0zt+qc38NKZ8yYPR'
        b'R8euKdmxs/J8/xtfrJsYcvDYw7cLamrcbMd+vTDmx2nLIn9/xOHeGH00KZFlJ0vyBvUBcXBtWCc5GawHB6ncaZkz34iazB2epexk1XA/dZBsC/PEv4MdBSwBGbc/vDqG'
        b'IvWrxyFVq7r/OEJAZkQ/VgTOUwTfHrAxFE1/HWj2IARnnexmMniVSP4kYXYCrAMdlKLMQE8G62OJTAeb+s4i/GSuQspQxvWH+0fRlm+ZPJNEDwZb7DoDCPPyYfMcCm07'
        b'BA4UYoIyJ2R9U44y7mAfB1Lr7Gf4hAuMC2ooQRllJwNXexNJXQi39CbsZHAnqKQMZVyPWNafVNx3fic5GS+C0JMhNbORtHcCU0D4yeKGsgxlXE9wNYTUOQ7WgGNkHm7J'
        b'MYpA4Q/2kDM5YhfcpP5gB8tQxg2UwH1/Cz0ZIdQiAty/uwBfwQQNss5QhuXg385Q5svXRzVe2eX1qRmuMn0TUOWm8BsKxOOStySJW1fwnZZhjBF4PfAnxTyEOhuFRl6o'
        b'phC6Loxkvf7SykYP7tUFlAzksUse9rZ8LppMuX3FPScgw3fRkyMqdRtLQfINYONEtUEPtWF8Bzl7cbFYTJdwkhTvuN7kq73RJPQP7bHY2o4iECmMzS8dcaOpolC5ZjF/'
        b'wpCnJ4hi46Ys/Ny2atCeKvftgW+VPXh324ezqs7fjFD7Phj/e7g2fessG23Yt1P+qOtfURSX1/vOb99uWJX/4YBNzu0Bv325boj0rN/zG3dVfaP8KCnD5tqvM4ZpZku+'
        b'PzF2buiLMxc/mrr1/qnkEgfXiM/7vRHx6WqPuarXxn50QTIj8ZtT1bviHl78bv2+MOB+ZumGbe+Orn9t0pHhU57y+8Vvwc6vZtdGz+rlqfXe4zd+/ZT+CbpRZz9/JuuF'
        b'gKKy1zJry95vnLXbvVhxLn302sM73vls1PmdU4tqPh+/kHft7foHK9QvJAyoHPuCY02b95Fmh8tXrv/QvPjEsdh7Y194riLsJS/v+8rofbbjU9/6nYmBecFxjhKeBs8M'
        b'YYwKViO9KyORE87A2jGglgi5MLBSStbswLP8LuFYGuAu6s5+EjQUkiW4GNDCrsIZr8GBeq/ua2je/zMj7YkTJGd4+ifNbEJAwPZZWcpiqSwri8gZHBmI8eJyuZxRHBGS'
        b'K7YcN669l8jdy999ovvQcVjqjLfnuTg9tYJZpHrb8HDxdNysLCOh4vX/4Oo5qncMzyZuKRblNNzvF5FdedMEcA/S8NGcuBFWJSeCKrDRDkPd61z68XyUsEIRN3sSR40h'
        b'vb/m3vapikCKhLvNobV//PSNMDJOuT4yJ8It42R0bmlDfMUPP1+wHz2kbXu/aZ/EbJvsVfDJ1kffv8xLHtN6s0/qo6zBV96a2tR6JmDeoQmbJ1XlJAgzPrhzIDBmy8y2'
        b'86+8ctoN8rmTogaD3VFOThWhYTdyKsa7hO9d85JDPn9uyQvOP11JmLC2VPjbddf1b/jap4pv3jqH9AS8/OyEF33RZJuMdxEwqzEH1DqB01x4aDY8RQmZGmADOJWQHARP'
        b'gXIXnBPPyr3gJR7YsxRUUXTHsQGwmvYCNkCw4WvHjPR0ceMNSEgl/Hhj4Or5Ce6gPX6a/zQ7Bok4+7RCDV6XWbQswU4Mq4fZMpxUBu6Ljyffgv0ewRH9AqbaMJwEBjbJ'
        b'kmk1+wFSKwjPHqoFQ9v7RDlJuEirawVXqdW5zQs2q40yJIJdjvFcpB5umkA0iNlTvRKIYKQ2Xy7c7ALX85LAadBKpmQFmq/P4hzwlIqNoAjbZlDl44JbMSG+jWMVJ+lQ'
        b'QW8uPJsI1lHqgjrYjkxelKGEzRAO6hzBGS44iwPK0SBN9WClL8pzWgAqSxdq4ZmFgoVaDuMBN4LzYh7YwOlPOVzPwG3aBBKSAl8LVsngGSewnQv3Rudr/FCOcNjiizt8'
        b'WAKSKuhi52BbH39hx3j78cEa0A5bTIJJ+/zfP1ddHzOHxwgZMzKnE8VCSFed7Wn0JWJPYgtUwJvQVdXxo8oAETa+Op5SXqTjY5dqnY1GW6KU6/hKhVqj42OTT8cvLkE/'
        b'89Qalc6GLDXr+DnFxUodT1Gk0dnkIWmH3lTYAwOTp5RoNTpeboFKxytWyXS2yPjRyNFBobREx0N2lc5Gqs5VKHS8AnkZyoKKd1So9YBdnW2JNkepyNXZUWSzWuekLlDk'
        b'abLkKlWxSueM7Di1PEuhLsZOojpnbVFugVRRJJdlyctydQ5ZWWo5an1Wls6WOlV2ClB6oT6q7/Dnr3GCKepUH+Lknzj5BCc3cfIZTj7GyRc4wdt5qo9w8hVO3sXJDZx8'
        b'jpMvcaLDCSZLVX2Dk7s4uYWTezj5ACfv4+Q9nHyLk/s4uWNy+xwN0vTnGCNpSn57ZJ+HPadzC4J1wqws9jM7yzzyYo+ReZu7QJovZ/HhUplcliSxJ4of5qZFxizLTUtU'
        b'Q50j6nGVRo3NX52tsjhXqlTrBDOwE2ehPBb3tuqBvt+6wB909uMKi2VapXwChi+QNQQ+F4murkNstDtZ0vhvRRS2Fg=='
    ))))
