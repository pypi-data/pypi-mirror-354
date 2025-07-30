
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
        b'eJzsfQdcW9f56L1XAwFieuEtbwRI7O04Bi9ADNvgEbANAkkgIwTWwDbexjaY4QXeextvG++ZnJM2o9npSGjaZjfOaDOaNs9tk/edcyUhWZKT9N/f+733+z3Glc5e3/nW'
        b'+b5zP2Ae+RHA/0T4N4+Hh4YpZiqZYlbDarh1TDGnFRwSagSHWdNojVAramSqxWZlCacVa0SN7FpW66PlGlmW0YgLGd8quc/DFX6TM4qmzJbV1GqsBq2sViezVGll05da'
        b'qmqNsql6o0VbUSWrU1dUqyu1Sj+/oiq92Z5Xo9XpjVqzTGc1Vlj0tUazTG3UyCoMarNZa/az1MoqTFq1RSvjG9CoLWqZdklFldpYqZXp9AatWelXMcRpWMPhfyj8+5Oh'
        b'VcGjiWlim7gmQZOwSdQkbvJpkjT5Nvk1+TdJmwKaApuCmoKbQppCm/o09W3q19S/aUBTWNPApkFNg5uG6IbS6ZCsGNrMNDIrhjX4LR/ayMxhjnCFzPJhjQzLrBy6cthc'
        b'mDyYhkq5IL/CeX45+B8E/31IR4R0jgsZuX++QQLfD/gKmMlT/eBbWW6bj5GxjoOv+PpitB634o0FuTNwM24vQJfxZjluz541XSFmxk0R4vvoEm6Ws9aBkFtvCjRn5+FN'
        b'uC0Pt7GMXzYXiXaii8l1cs7aj9TWuDBFlR2VLWKEwjA5iw6iNnTOSqZqOL6HtpIkBd4IpUVMIG7B+5YI8vFmARSWQZZ6dA1vRq24JaoOOtQGlfihbg6fxDfQFbwV36aZ'
        b'fIp180Ig02Upal68yIq7F0kXWVlmAFSD2hLxLejoKMg2Y0gVakWbo1WKCNJbUi/ajKEaH2bwaCFqxEcWV7CPAOZg+8RpyAry68f8vBXUDbatHtsMALyCg9VjHavH0dVj'
        b'V3K21at6dPVIJ/q7rd5wfvWqlT6MlGHCypVluWnRyQyNFIwRMJAx/C+CsqjLw3R8ZHqYLxMMkXfKy6Tx4VI+8qZByMBnTNWkMsO/U7OZLsZAIGGvIEz4t1Bm4pd9bi74'
        b'krsW+4/oEazBFxJKJ+5iL/ow4X+bXBb3TpyoKoSh0TkTvg7qDGKD6xa8y34fVhGhYHoYq4KsfJdMC6vWGj0jPBy3RGcpcAvqKgrPycObo5TZipw8ljEGVaKbvk/EoQtu'
        b'U+9vH/VkfupdNw5DJl7n75ha7ken1uPGELtNrTTfRFq3kli0vr9f4UzFbI7hBH5TGLyfVVv7kviL6ARqKoQK8O0Zo5hR6CS6zBe4WB1cOBPiqyDqADMFXUyxhkL8AHRr'
        b'Eu6AeitxVzQTLcOHaDRaK8drcAeMXIE2KBhF2gpafTbqGlqYNwO3ixhuGT4ylR0iSLDKSf4NKtxN9kGkCuB3Y+6McNQVlUV3pRISduAuEVqLu/B5awjkDojEXagbRug7'
        b'dzwzHm8p1X8cc1pk3ktGd+4P81+ODUQx0vXq3+uLm7oKg54ZGLZ77lPqjNkDTswe+ub6rO03p+DshvWvJIRu2YI+fG/Z/bPtpqfHFWz5a8j536/X7Xr96NP7n7t76HKT'
        b'QHrut8N+IxpUkDlsTt9Rs44F+l1/ofbT8Rsun+nbkHNtueI3sz/N+oW44/6vu15uvX/g18sfKlaM1b9fMG7U2dvzLMFfrpkUaTzXOerAM9/WPhCk/LUiWy6yENwgWglj'
        b'bI9sQLtwe54ih6CPUHxDgJt0aKeFoB10Ax3pE5mjwM3Zufl9R4kYf3SJw/tT4y0E2fkNR7sjlfIcfNAYaUMuQXi1oJYbaxlGCt/VoEZ/mLxJbJYV0EFLNMeE4FsCdA5Q'
        b'10FaAz4A6OEiTHYL3ozbYEulNqA2Fl0yJcm5Hi5cbiIQI/enH//BgwDfw/7jdabaBq0RCAglTUogK9r6CT0BJq1RozWVmrQVtSYNyWomeI6ZIGGDWQnrB7/94T8Qfsln'
        b'KHwGc6GsSWyvWS7oEfOFe3xKS01WY2lpj39paYVBqzZa60pL/+N+y1mTD/kuIg/S3JOkc4Gkc1jGiVmO9aNP60iyCOjggMgc3I6b8H5VtgK1RMPW3xSdwzJj0CVRKVqd'
        b'57IfyY/Q9kkpppYwAsAEaNhiAfwL9UyxCD7FGq7YRxPYxOhYjVAjWudbLKHfxRqfdZJiX/pdovGF7348zdUJNH4afwj7QxjQCISlmgAISzUsxblBPeKZdLby6ew9+B52'
        b'ZIXAqVtkuD52VJHA2Ik5VMTjH0GzAPCPEPCPwIF/hBT/CFYKbfhnnSf8I3DDP0IetUvjRICb340XTSzL/TYoj9Ef/yKONRdAylfsy5+VvVT+Sdk2TbP607K2yrPaTyBc'
        b'/PQ8fHFL7PoZ+w7vCHm2QH1KbRCdZk+XvSjcGjVUOkU5tM1/bvrqT8MGzgxbOzDlTbbuh+eeD14puCMXWwiRS0OHfCJVCnRwvI04RoqZIHRC0GCKpOn4FmyI3ZGUdtYs'
        b'JBkEjDRK4LMK3abbETfGo70q3JoLbIJczEiGTUEt3JKVuNVCqJd/nC4PCDRgLlU2OgdoN4UbOEVpGQBJU3Fj6Jxg1FoAfICQEeF9LL5VjTfye/w0uomvRiqyKPsgicVn'
        b'8BUOrZPPlHNOICnwtLcohPZISkv1Rr2ltJTuISmZ9eJglvyKWSHbEMSvutKei987oh6hWWvQ9QgJk9fjU681mYEfNJFVMRF618Xa2yVwbwogjyDHpiCNlDg2xclgp03h'
        b'1l4F9wjoO2AszgZjOs4GYRylcAKAMM4BYQIKYdxKgQ3CdI9CGOMFwqxRZMWu5OJGf9idrbDgrdF4c2EWv3wzps+sRwcJ1XsSHxaHoCbUoQ9bEsKZY6DU9aaTn5V9Ura/'
        b'/KXy53XRoZHqXPXnZcEVVTpDubAlVlH2l7K5z4e99PRuljn4jGRZvya5kAef04CwefBA19B2CiIEQNDxGZYRkD4zFd0FCrYRcO1mpaKOoOQAfAiw8qCVQuBFz/pQWCnC'
        b'O30dkBI9g8LKIrSfpqHbuBPdVBUoWNSG2xiuns1Aa/AGfkk5j9ABGLFSa9FbtDU2ACEIjSn3Y6VsQ6hjqRxZ+KqEdMF7hEZ1jbYXJkzBfDOhDoigwEDIcIUDGA4GOgOD'
        b'hxb+6zjHjefxChGRZJE2TEQbPEDEHKCxABQOiEjHLfrOp//JQ2nn3+8SgHAHh8/LuJY4a8xbMcdihPF1uv5ahjlXLSn71z65wBIGBQvwvWlT8GEnnEEAYnGqhZCOeQl4'
        b'/SPwAMCAD+JTFCCm4TUUr8TgAyMAIGamOSGP/FU2EugdLcDCm90XvvKRhTe7LryIX1eywj2ierXB6rb8Aqfl7+uAATLVVQ4Y2BPsGQYcjXnHCUk8DBA+mNUJfwZecKM8'
        b'rK1qVygQ5VuV8H0U2o9PEKmsCDcrFMoZWTmzcHNBIc9qZgHXqWQZC747yMdXjM8N4QHnPPDDbRRyTJPdsYkDcEx4u/7NJ74VmfPJZmZWfVb2KYCOQRfRP0KdpTZQoKlT'
        b'N28/velP2lPqT8peKX+JAlWO+rQ6uIJ5oX8LO2X3gIuWmCiNRpOllujeNbBM4sqgm7NHAttIpG10VIhvEcaul62bFEUZO3xhHE+orqPmYAJ0EfiGE9wZp1I81F+idAM7'
        b'dL3MhoZa8Skem3Xg6/iIDRMBujlqAz3cyNI28lEzOg9kCx/Dh3nSRenWqnC5jXQIvfKEPICKrXWEFeylWgY/4PsklOdrCLABDZ/HGSvxBMkBlW5bABBUL8miwEkE9BoH'
        b'cG4PdQZO13bc5DNX3EQFYwduYpvZny+PCT1CpSBff3RUntCcAxEPnupRqbMqPwegebG8StdXfUp0KWxAjEJDgGaj+rT2rJb7SPaCouy8et7zc381Dxfh6diAp4f/5pm5'
        b'gl+HULIkfi5okXm8nSydwY0iioGuoL1O0IDW5NGFbMB7LbDMFnzMCcGgJrydYp/5UjVujSqBcrgdRDDxAm4UujaHh7ImfB/dIwzPFHywl+fx9/O89I9DVsDAmy0mG6Ii'
        b'8jljCQaWXwrA0BDYiz9IFlqqS8Cvr3cwAAamFwLIQKwOCGh3QU+PVC/n8k1EKpcHEMaKEEAQK/xKS3kNGnyXlpYusqoNfAqPKSUVADuVtaalPRIbI2WmzFKPWKfXGjRm'
        b'yi9ROkkRJQVI2ic70n2sBMUPgUxKIRkCQboSTsjafrlAiVQkFQVLrIRBUOENNf42AQQ3oWOMRMqVPbnUuwhCkKGLCMIVCzUCInLs44pFnYxGfAhEjsNsIwviiITyX749'
        b'4ilGQORLH/adrC3XW2pBkItWmbQa/usDnkt4QJp4GDpba2qwVprr1FZzRZXaoJXFQxIZ0ENprtbSYNHKppr0ZksXRyf9wS9hwN/uhklV1Rotten5MMmy8AyNSWs2wxQb'
        b'LUvrZLNAijQZtVU1WqM83SlgrtRWwtOiNmo8ljOqLfiOyaCUTYclqoWys2tNxp+Sz1Nl1Vq9USvLMFaqy7XydJe0dJXV1FCubdDqK6qMVmNl+pRZilzSKficVWhRZIMA'
        b'pkzPMMKEadOLgB4aojOq1RqlbJpJrYGqtAYzoZIG2q7RXF9rgpob7G2YLOmFFpMaH9SmT681W3Tqiir6xaDVWxrUVYb0AshBm4OZN8Nng9WpuD1Qvpj0jsjfMltHIEop'
        b'K7aaoWGDU+dlsV5T4tJVWqOxQSlT1Zqg7rpaqM3YoKbtaG3taWXT8B2DRV8pq681usWV683pRVqDVgdpmVrgNKtJveG2KLk9TTZNC7CDj+ksZjJKMqXuuWXTcuXpUxR5'
        b'ar3BOZWPkadn83BicU6zx8nTp6qXOCdAUJ5eCJsYOql1TrDHydMz1cZq+5TDHJGg66yRmGoCw4p8aw1UAFG5+BhReFSTWeOnHyKzMzPySZpWa9IBqoCvhXOypxYpJtXC'
        b'2tgmn+4FvbEKYI3UY5v2LLW1zqIg7QDOKVfa2rR9d5l3T/Fk7l0GEec2iDj3QcR5GkQcP4i43kHEOQ8izsMg4rwNIs6ps3FeBhHnfRDxboOIdx9EvKdBxPODiO8dRLzz'
        b'IOI9DCLe2yDinTob72UQ8d4HkeA2iAT3QSR4GkQCP4iE3kEkOA8iwcMgErwNIsGpswleBpHgfRCJboNIdB9EoqdBJPKDSOwdRKLzIBI9DCLR2yASnTqb6GUQiS6D6N2I'
        b'sJ9Meq1OzePHaSYrPqirNdUAYlZZCaoz0jEANtaCkGQP1JkAIQP2M5rrTNqKqjrA10aIB1xsMWktJAekl2vVpnKYKAhO1hOGQavgyV2G1UwISgMwDelz8LEqE8yb2Uwb'
        b'IFiPp7EGfY3eIgu3kV55ejFMN8lXDonGSpJvKj5mMOgrgUZZZHqjrEgNdNGpQCFdA5IynSpmnSvrJeOKYugFIIxwUtwlwVYeksa4F4jzXiDOY4F4WabJaoFk93I0PcF7'
        b'hQkeK0z0XiCRFshT83SZzjnwJcCf0DiLdonF8QUwkeNrvHNWsyMbvxCZWiDHlU4RY9KL9UZYDbL+tB2S1ABRhPQClnYJxrkGAf2ozRagdia9zkKgRqeugv5DJqNGDZ0x'
        b'lgPYOlbcYsLHKgGIso0afb1SNpWnH86hOJdQvEsowSWU6BJKcgklu4RSXEKprq3HuAZdexPr2p1Y1/7EunYoNtEDmyILn2mbVbON0ZD3MkaeEm28kqckO/vkLc2Byjyk'
        b'F3hujfBdnuJdWDHvY3hMujfu7OdkjvPesguf9lOyAar0lM2FBCS5kYAkdxKQ5IkEJPEkIKkXGyc5k4AkDyQgyRsJSHJC9UleSECSdzqW7DaIZPdBJHsaRDI/iOTeQSQ7'
        b'DyLZwyCSvQ0i2amzyV4Gkex9EClug0hxH0SKp0Gk8INI6R1EivMgUjwMIsXbIFKcOpviZRAp3geR6jaIVPdBpHoaRCo/iNTeQaQ6DyLVwyBSvQ0i1amzqV4Gkep9EIAg'
        b'3WSFGA/CQoxHaSHGJi7EOLEpMS4CQ4wniSHGq8gQ4ywbxHgTGmJcxmPr4lSTtkZjXgpYpgbwtrnWUA+cRHrhlOkZCkqtLGaTVgdE0EhonsfoOM/R8Z6jEzxHJ3qOTvIc'
        b'new5OsVzdKqX4cQQhF5txHfqdBatWVYwvaDQxsARYm6u04I8zDOTvcTcKdZOvp2ipmnL8R1C6R9hGyr5eBvXYA/FuYTi06fblCtOhd3ULrHuUXHuUSDmGIhQrLYQvlRW'
        b'aIXq1DVaIKNqi9VM2Fp+NLIatdEK5EVWqeXBFMihJzWA3KmInhB3vYYW+9HMHur3QJQ81+2ekaqYemdHBsy3zMby0qnUkXTbJPPf45y+E5mwV1P1kE3P75KYiP7TREwo'
        b'TETFyp+JEJMOE1HQ94jMdQa9xTTMocILdlXmEbu5FS7KPAHHcv8WiziO+56L516mRme4e0WUGbdH4o1RqEtYRLR5SdxKfH3mf1GdVyX37fHLqKiotRotID70BGbCmvNi'
        b'h7pOa3jQj1fmET34w0GTAQpqgLUg6lIZL/gADOsB80AWooXtERIWyDQWvn57ByJm1fAcTW2VUSsrrDUYorMAJRkVqgaiYOkN9iK59DmqYhlfjCjSCPo0681WPoKkOYf5'
        b'TTeN6P14Bp9vKHOWorCiyoDvwOIbgClxDqZnag3aSg0ZCP/VpnXp/R5nE5DS7TNBGX7CEWpte9sutcl4rsgm+/VqqWxSH+XVibwHmWF3WahcYKuBNmfQQwb6TW/U1coU'
        b'sgyTxd4VW0y2kZR8JJJki/OULc4tW7ynbPFu2RI8ZUtwy5boKVuiW7YkT9mS3LIle8qW7JYtxVM2YDIKCotiIULFLwxhdrU0Ms4tEgKyPC0gTLsqVmZVynpVsRDJw7Jd'
        b'N6qUEYbdLnbzOtfeZZTlRuamT7Uaq6kBrdZUCRiqgWAVEp85S5aQytNZnT0L0Ql7irfBDZ/kocL0YioPkIGbatQk0QEinlIcoOKtWNzjinlO5EHoMcU8J/Ig9ZhinhN5'
        b'EHtMMc+JPMg9ppjnRB4EH1PMcyIPko8p5jmRFEt9XDHPiXS5Yx673p5TacHHA4p3SIl9LKh4SaUFHwssXlJpwceCi5dUWvCxAOMllRZ8LMh4SaUFHws0XlJpwceCjZdU'
        b'WvCxgOMlle74x0IOpBZa8J2KaiBdi4H4WihnulirN2vTpwKJ78V+gA7VRoOaKBfNC9VVJqi1Ugs5jFrCFfVqG22UkyC8DKuO6MUcSM5OSyGJYN5egiwLzzA28BwxOdAD'
        b'ZJyntwBp1GqAA1FbHkl+BA+7F+7F5I+mmQz4mtnGJrikZNHjHZ0FuBKHXEUpiYLyOx6FANtIbdQcSD9QGsJD6yj3XEMIvEWrh2mxOBTF2cDqWvQ6fbXaGfsXUznQoUB2'
        b'ZjN46dHpINGZTZqq5UULrb6cJOXCqpGTMTPP2Xhn1JyVw9BvaFltsNZUa6vsmmxKBCkXR4yx800R3nhYYl53xysPO5j7iLo/LERdy8y5+XhTNDCyEfOJmbLKh+lXLpQO'
        b'T3RjY6V2NnYh68rGdoo7/Tv9NVxnn84+PDvb7qOJahI1BTT10Qk0/hrpOl9gaYVakSZAE7iO0QRpgtu5YjGEQ2g4lIZ9INyHhvvSsATC/Wi4Pw37QngADYfRsB+EB9Lw'
        b'IBr2h/BgGh5Cw1LSAx2nGaoZtk5SHEB72eeRX1/N8HY/jaKJs/VWqJFpRtDeBvKj6vTrZHVkZD70aS81st1Xo6TWcCLqehEMZX00ozSjadkgTTSkiZok1DEjlKaN0Yxd'
        b'51scDLEh0KdxmnDoUwi00Ucjb7d7FgQ2BelEmghN5DoJ1BJKRYBKeUyPZDIxyp5UOPthtJ/M6cceLePxB+8q5JKjS2Qitmym0eT4ntpmR5Nv1DCDyAFy6QNiVPOA2hwT'
        b'k5re7KZke3ZTCnnEkizEzuEBtQUg0CD36fFTa+oBJZlK9Zoe3wpADEYL+Rqo5oWWUgNwdpaqHkmFFfaMsWJpj4TYnerVBpsNhr9OD8xcaQ3s1yrado9gyqyZvJGHKRUe'
        b'FRInEPSz/VP7nEzmEY8m3yZxk1+Tj87PZgIkaZY0Mit8G/yWSxwmQL7UBEiy0ncuoxHQ6RV+S7wiXGaN/GTz3dQ3aM3Ug8sx13pqxVChVboVcYtIA1lDXSPrnaI0m+8W'
        b'4BOi+7E5h9nmSm20uNVAfsIzAQ1Y7EhIrpRlkPKAMCpk1AZQZq2TAdpMlmn0lXqL2b1ftm44VsdzL/hkzz1wnHD8SB8Sf6wPrmCRJsuln6QL06Jz7am2jpk994UQGYLe'
        b'gTgoZUVVgPAB+rUys7XcoNVUwnh+Ui28+QgvmUJNMjVUAWG+/zJDLRAfk1KWbZHVWEE+Kdd6rEVtG3y51rJYS054ZeEarU5tNVjk1HUvxfta2LZDmmyS7ZusgqgIwx0H'
        b'i06qRbm3WuxbKc0OrWbHYhJPwVqTLJw3U6nGd0wNIG17q8hmF5VGRSvChkA1PIzYMEu4tlIpS4yNiZIlx8Z4rcZpL6fJppKAjAZIdTq9EXYN9FG2VKuGjkUYtYvJKWd9'
        b'kjJBGRshd5+qn2A1LOU9FaamBjMyhqn7fFWZITtwLGN9AiLRunH1uDUPnZ2Om7NxOz6DDqui8cbpxJI0K1eOW6PyFagFb86dkYXOZeXn5WXnsQzeig5Ja58optWOFUiZ'
        b'MIapKiksyy2IiWasE4napxlfQ+ucKu6tFG/CG3OBkKKNj9a6bmkguiBl8DW8idZ8a5yE+MJJ2mrLpCOr5YyV4GJLAtpCzPVK8Ua7c1WWUhGRA02g80ImaZ7YjA9mUNcw'
        b'ftRF1PUufKyszPByvwn8qK3F0Dp07niZW/+g520watLHNvlsp+6hmyZ/dFmD7uqjyiNF5gaoZs20t4e+9Hvf1THS9e+duH7l1oaOG2sFkjd8oqNH5h+SDZyU/G1C38A1'
        b'fz25bf20UevGbNy2zngnc++Tt97sv+yb1W9OKT+c/5vTaVVB357+y7cHM0KmfznoXbX5OeHmT9UH/e/PGPzbDa+P/tdXh17oKVK9f2lp1+Kjv+8fv2v8D4ci5be+elsu'
        b'pVa0+PTsHNQaja+j9Q5nSQETNEagm4kuWmRkfVvkQ1FrQe4gvNppMVlmEG4UNujRHd4Yd0dytj9MpjzPboyL2ob0Q01CCbpm4qvZjk6roR6XxWMZDb7af4TQP2wSb0u5'
        b'Gd9C9yIVaANqCc9ScIwY7eEU6PhE3pVr+8xCqKF3rfBmXyYUnRfAat5L5125WgBq7kYq0WHoC24B7kyMznLxhXgztflFHen4Nmolbl6OFRLL8A4mtF6A7tbhrZZwyOWD'
        b'D68gI7bxa6SntvVl8C68m4nB68VK1FVtIa6m1gF4DRlWa1TdgAglyQt7YHMk5GVkZlEAuo2v0PFnLUJNJB9VZELLCjE+qofe7xTg9cAP3qWV4bWThpOW8YahtsZtrOIg'
        b'dEOIWlE3PsMbS/r9h35ovY4r1MaU8B/MKma5mBVTdzOxzeksEJ7E5UzCkRQx2xBiJ8sOh5Z8e0eofSnxDTORbWvKIA/CMpgmMXZvGeLW+ThbZQlfqreSTEcpWokHv5sH'
        b'pPuEF2dWM7uHOVuyunfVxZ6Ztf1TK1LSp+XMQt5yns2Xsz3+pb1chCnMMW1OfkbjDeqaco16QgjU8g2p0alFe9pDG1a31WXnAMKBWmgUtUbDUnkX2yPQ1Fb8pK7p+K75'
        b'lTo4C089M2XBoy+UN2XDl4fD+R7wRTx04OdMSlCpKz/htfkBjublj+U4/tOO+JbaCbrXLgxydGFgptqsdXAAP7vJKnuTDkbaW5NDHU2O8sof/MzGK/nGJaV2lzRvbct6'
        b'2/bKU/xnbUtLnUUGb+2P6l3xH2FEvPTCxb+A+sJxTYzDF+6neBe4+bzYq3XzLrg+61+8e+2v/CbxnkxVus+Z19tebnvfFCh9RrpPz0w4LHy7zztyjromoUZ0AB98BGs3'
        b'RtuwNuDjkxRrN9RTEpDrhLLxLXzIgbZno8OP803zKSXbytk9aRX8jmsIdkJkNANfZsCjNYU5FuQpeIyFyTWTgzhAjKuZd1z80NxqlPv1+Ni2Jm/DLzZbTFqtpUdSV2u2'
        b'EE65R1ihtyzt8eHzLO0R16up4OlfAfx6bQ0vkAos6soeUS0AvKnC32kRCN4OtC8E8epo8ncIkgEOH/9A/nIFXaBtzf2bpbDmUlhzf8eaS+ma+6+UOomTfxB5ECczNBoz'
        b'yAuE6dVoy8nWg78Kmw2cTEst9n+CREnlHSqsqGVV1kqtkwwHM2PWgwwk470aiDhm1lqUsgIAbbd6CA6oIScv+pq6WhMRPe3FKtRGkGdIUZCFTNoKi2GprHwpKeBWibpe'
        b'rTeoSZOU/ScWlGYlGame6NBgg9mqtIlQpE63OqBqq1lvrKQ9clQji6CLFvETZmSqbbRVRP/h3ne3/OEWtakS2tDYkREpLyNaQTMRR8yLrGR2y03qimqtxSxP++lSPg+v'
        b'abIMF5oiK6HnoPO9FSMtp8moF0PJj/oyeK2F3x5pskL6KSuxWdZ5zW/fRmkyotOEpaLSZ4mzZZ3XsmTjgdwKT1lJgcniPR+/NSEr/4W2ESXLLixQxMcmJclKiB7Ta2l+'
        b'P4NEmlGkyJ4sK7EdDs6PLHH21PDeeC8aIDI2H5CRipztg70WB8QBk1kFWwO2q7nCpK+z2EgYgVPilU33VobBXAvwq9V4VA8AOJHchOAY6AU9dLGVssm8joBu0ZGFFnVN'
        b'DfFuM470qi2gmwEACzpQZ9taGj29IkgN07pYD4RNuwRW3Lbh3OshP/m1Fi2/Tejm11qqajWASSqtNQBo0Bd1NWxA2DRamJ0KrawWKLzHevghkU1DlR9mfph6s1OXlLKp'
        b'gNTsCMljLc7bjqhKANTJBUgVBhgwf/eRWeu5ZJnt+qPaCtpz/thkfJXFUmdOi45evHgxf4WFUqON1hgN2iW1NdE8sxmtrquL1sPiL1FWWWoMo6LtVUTHxsTEx8XFRk+O'
        b'TYmJTUiISUiJT4iNSUyOT51QVvojiglC+9xdBkPzrcSKBG/FZweYc+U5CmV+VDaR2bqSQkH4G10oqorGq+mFLfgEPoy2x8O3WHx7NDyucVS8/5dMxJQt68cwE8ukVyxh'
        b'jJVoYasb8AWVnaDPwM2RuD0vRzGTOLg+gW7ODCd+o3NA0IcPIPNoG7rgi7er0E6q7Ufnx4hwN9qE1oGwS0RBH0aEd3NSdB93WMeQrrTi8/ge7laCVElUJq1Q/Vx0iFx/'
        b'wjHD0XEhvmVSWSeQqq7i5lzcDZJ13iy8pc5lhPj8oqjpuDkfKmhTzaqDR0FuDt4uBCEYrfXHx6pXUvsZa/U4f6U8B91BB/0Y38Xocg6HD+IruJO6yuFtfXW4Oxu31U9S'
        b'sYwA7WTRatTsayXS8tyleI0/bo5W4o3QYhTqQifTcoC3aWYZ2TSRcJyVXvqEmgoWo5PQ++7oCJbhstgktLM/nVl5vpipiwX2RFZm+HXyHMZKjIRCcRtabQ7A2/HVbHzK'
        b'CL1mGck8bloK3kGvbsIH0BF8lmQICFDCul7NzYrAlyLxNgEzYKkAnQ1BHfySr85Frf4gb69XQu9h6rLJtAiYfvimMGjxSj3b0yUy74GMs998XfFKnh+KCRa9m5z98E+f'
        b'5D94pfHG134L1BMvDpYrf593Jubklv7jT0XLur9b8l5sn8Z+s/9w6YbvqKKyPmnhD00pXaoH0l+dTXoqxbDx4aiHMfMO5De+wLa+VI50v9QdSn1ZnzG4eGZBZPEbe068'
        b'HNCOnzuS+fvrn73xxa4/Xpn1r2823Vyx3Prk8d+vDDj6zsWbiYMvbfzy4JyiC8OzTZGLO2bJxfT+mzK8jUWt5K4qMQj4ThoYvC3ZQsHlbIZB5aaNyEDniJIhMl6EN+P9'
        b'q2hVJi7N/0m5ix6GKmHwXbSOaiHwYXIrF2Fo0QZ828HU2jja1HxaC27vg7ZE5i/PV2Rn56micLucZfrjO8I4vG8VfwHDnXqxKio8C7oBi1dagc5wS/F5X5erOgL/0+ty'
        b'vHrH+qk1mlKeg6Os8lg7q5wlZaWshO1Pn86/Qnr/h4Rt6ONgfHvrsCkwAnjtQjFjt18jN3qY5pHHfPJYQB6l5FFGHmryKGdc9Bme/Xz9+Tp7KylzNFHuaCLA0aLa0Q5l'
        b'5cklZHIXVv7tsc6svKcRyX17pBpi0GdjkXoCeMbXHhSra+gnue1E2+NrO8Wt0Pb4EzYFmENi48X3wTHMCj8nHEwUL8F2HEwc++mVaL0cfSDw9EE2rj6YcPW6YBtP70d5'
        b'en/g6f0cPL0/5en9Vvo78fSbfR7P06sdNnoy/tKjn8C5TiHuDXxuGZBPmC9gSoElUDtf8EfYhihZpanWWgepwC2r3clRbU253qi2MygRwLtEUMrKE1Yi7TvsOUkHHQKw'
        b'W01EIP7/Qsj/y0KI8zZLIwvFxzj0XD8ijLjsS748H2WvwCNHVvIjNp5em+P3Pd+Obavb4nim1lhL9DYmyrYaPTOji2sJ16ivURu8sL0lj7FyBWHCs52r1x4TDMX3t7y2'
        b'tpr0l8QoZXk26FLTsKy2fCEsPIj4no8NjUQISkmKibWpwggggARHqivptYD12gkHgkyTzTJb1QYD3RkAOPW1+grHbixxMqB9rBxoQ7Cuy0Bd60qcjWx/VFIjxR+R1lxM'
        b'Of8vELYytYu1lTZDnP8vcP1fIHDFJ8XEpaTExMcnxCfGJyUlxnoUuMjP46UwkUcpTMYfD4+QkktG+xNJKrdimJGxEnVuaIJVlZ2HW6KyHeIUSFF49bLZj0pRq9Bd3wR0'
        b'MN9KDvIKUGMx7qby01N4jUOEwpdjrcRaBR9E+4QqZU4ecLBOFaP1uANENDf5rBW3+oKM0orvW8lJEz6Db6BOc0Fege0GLCKkzcFboMBm3AyylB9IH1ApbrYCu32zcB7a'
        b'h/ago74MOoN3+OcnGazkzHOk/5PmHNyenVeAbuIDKnIBUoyQCcsU4DZlsJUcWI5D19Elc0Qe3hSO2xeOVUUrs9G5cJYZXikSDV1OL7QtnIz3pOMj/vg62jRTgtsV+SBn'
        b'cUxovAAdRqfwCXpijVejcxaYjbZI1YJY24k1iDvo6kxyH2gsahUtQUfH0vpQyyx8CLUOsPUsO0pO7hbti48K8G10EZ2mC/W8P8e8VUU0tWVRJxNA5A2lMjRaM9xfzDBF'
        b'g2qZInwfHbWSa6hQB2op8SdzBJO5FV/PyiXXPHbgq+jCYCJ6tqIzEJGLN2UR6WveQMk0dAjdopebDgSJ8Qzuhm/Z+OhAeIAAaSX8ox+IeLwkPgf+K8JpbrwXN06mN6dG'
        b'oyPoHhONm8YYvvvhhx92jBIx/0oeQMAqqnOUgT+U14p9mLkNVLaU/j1mJmMlB4V4Xwi6vAKtIaf67TbJPStqNrnYODpnFgBFFm4rDJcDaGQ5rjGWo2t0FsXGgPmR+KyV'
        b'aNMBElr7FkIXcwQMi8/i9iEgg6Ezo6zpkBgRg9b52xZqZi/MSPCmRePdJ+k83iYEEXmW71NqfJ1elcviO/iAXQBuU80Ix9sLJbyoG0wu6uNl3Sf7iQPR0RVUDsf7J0wy'
        b'5ygK8mBIqpX10fk2UVeOd4nQlTTcRuX8PpqZkTl5gfgYufZGLmb80X0Od6Mdc+nNvZ8mFXDP9t8bwNSp+/w+bF+fbQzVL/gCjO3A3Tb1Bm4OW0TsKwDC8MbogrwZ4fwl'
        b'Oi5WDHg/OinFW1AbPsnfkHspPTlSmR01txbEfzHazEXPW24l1/qMRLfQeRWVETl8CrWZ2JQRaItcQBPzOdRMSuG7VnuxJXg/rTAV3cJNtnKB+DwUqxxPVQdhg5UwQtSC'
        b'drkO8Rg+q7848AhjngAC0z8TTs3f8kQ+nhi8vrL+d/X7Vn2/LQz1OyWfWeczKDBm5MyoEZqZh604qXFyyIzCFMW0Q+/P61ryyq0jb+/+x8dv/v7tWW8cCEzum5u350FW'
        b'x9Nr3rv45b6cOX8wtIfl6fp+15741ej6ftn/3LycefDr+mOi3auHHDpxasWvpdYb+nFPWLrShooKV1SdV355u/Afb8hGTUuy7Pxg4j8yBg/sLPr388ENV46cPNBW4dMj'
        b'NO7L/fu87twnduqtr71k7nje8qpppiw7/9J77IPKe6o/nnjRdP7ErDVbrWvOvrDpzPH8Q7rpxo7fiCv/OWlp9q4/NIy6I7vxwdAn//TCHe2dpVeuftu/6H5uxorr+6+L'
        b'fhO4LOWpIcnhLwq7f/fFROXtnak3Iz7Z1VT4z4H9/piYXq/6LvD72qLX51wfe/P7y4l3luCW8obG0rfjO1574qPPnvzLRdPxA9vlAdTSAl+psqkkevURuBGvF+gA8e7m'
        b'lRK3+5c7KSWi0NVeKwleKYFuDbZQTc1xfBOAbNMSf3fFBDqgoioH1JkCKNTJCidoNroVLjDgk2g/fz/orTTUNgOdiIxQ8nYdvk9x6Di6W0qv51phjotUEnSPdmZGEXDa'
        b'xClWWC1UPdWCO9BBVW6EmOHM6N58NjkTNVEtxji8DW1DZ3LzojhGqBqBt7DoMr5uobeFqdHtAUAZiCUHoLBDZEzi5dw4oAIbLMRoAlDpkSze7CNCidaiM26GHwNH0YyA'
        b'de+js47TwdaMR2068J4lvH3MUbxnrBm2Gdpeka8Ip4eIMO8heIsAXcTXl9GLFPERiQK1VvXqXojmJQXtfMzlWfLg/5IixpNKJpAoH3plcqqWKSJ8wir6y0ltSple1Qy5'
        b'0JhXzNAQR+xMhkFqX1ZMrU2I5Ql/41kohAOpLYofR29AG+Ci8uht1abIkfLKFC156MijkjzIdYwmPXksdChYPOlwfH7Kjch+fJ06R8VaR00LHe0EOJro1eYY4FHsos05'
        b'FeGszfE2tAqRE+9FTsldb0oXNfk0MfT0lG3yozoY/yah46Z0UbO4kVkhbvBbLnLoXMRU5yJaKfZ2Mx9pZDjzKIMXyDN4Xy4XMMKJz3CEb+j/lIkporHxKhEjMYwVEvr8'
        b'MHcsQ5G4aUG4GbVLFgnwDj0jCGRT0MV+VmJchTYAaO8rRO1FsF1O4O2z8mbgq9Px1VkBSTExDDN0gACtQfvwLspi4dW4CR8qxO1FiTG4JQHYK0nl0kUsbMgWdIaSanRm'
        b'hrlwmJJWNwuokyiCRXtSUCvPUqzGa4EIkYvR8Q0luRn9XCivsz4weRE+ijehE/g4jGYsEzYHXebra8drKlRoMzqsjEmIS+QY8UoWHXgyipJYDdo5kN5DHop2Addpv4jc'
        b'X64fuDVYaP4Ysrz9x6+mFKTnC2OlVz/I/rj7aWVo5sRJv8o4VdX14KwoILT53BcLB+0cMuJBCudz6MiRD1NSurszdxz8ZsGBL56NmcSKqqPiFqx9pm998m99ytpPfRKW'
        b'UDe94W1J0S8uRRwa/UzP1gPqxeOet7At79y4nDvwg5lvziwZteadRVEpI/CEd/60LHDqPuFnd2pSmroOzM68MHzqb5cWlCzbtyotyMfYeHvTvH+Xm/718aff7f7qd7Wb'
        b'gtK/r1h27uVRVZ27CqKy49UZ61688avPPtq/N+5M/9r33st98/Mvxnxx96/f1f9ixYLWH0Ye/PrpM6F/ObzqoeDQr6e/UPNHeSivBz4PnOkp3JoVhFujfRgOHWFn4asK'
        b'C5n7IYP8eNw6Dp8D9Aq4NSiRmuiNwHdg2lsdyFJchQ8Aai3Bh3kTuDOmBtSKLi+z4dZH8WoBOk4tDuctwDsfIVF4XdkYgQ5txXwOvA/6dk6VHwW83uZodFrIBKId+AC6'
        b'JygNV9P+x9UrcCs5WxHh7dmMcBhLjh7wAUoBBuEdUnoH9gnowKbeW7Bn4HZKsYqBmz1D7p13XDqvVZJr52Fk3ZTsoStB/ion+1e0Grfkskx/dE44OBNtoki/PAbvULla'
        b'RAJfdY4JXShAZ2fh2zylvYIa0SWe1vrMecQgkSe1oSWUbI/EHXnEsrXXthEm5SZqHSZYgG5F0dlHm3T4uguhRRd0swWGgBGUwCiXAMuWh/a7EBi0PcM2oXgvsXq13ZOP'
        b'tuC9jDCVRZfQHtxCqXQouilUjV7kes8vPohP8G0fSlmpwldg97bDoAvIZaloC1eLDk75aej3f3QDv93Whr9vn1IqXS+liiZ0iNo6UotHIaFSHAefPNWSApLmf4WUdvEH'
        b'CyTE20dKHOmO3/eEI4RcINefI/TM2fKG7wBPs3x6qUWPD6+iNveIzBa1ydIjgHw/l0CJTHXku9FBh2odxIjSIXL/6znW5q1E6dBq5jcyLyZCfEf/i8ZaAmqsJXz4kZuO'
        b'gXfBsthdQGy6WoNNhWLSWqwmI02rkanJUYCTRuYnqdFl1dqlZqinzqQ1E3NIXtVj012ZHfp7m97Hk/r7UdW+gVeYke6UL7VoPaimXMiq2HninMzq6fXswIV2grTfincA'
        b'3dmILgFfehnoEeyrMzNQM1qLb4iYMLRasAyt8+PfPXIIcMIm3BEdBauqZJRCtIc/E+2ejNdSsota5ygAtSiVuUsETF+0UYC6ssootb7Un6ManC81FdLTIVWMlbKzTVkh'
        b'5mDg7W1FxSPx9nJ0F2TJI3FMRKIoJRKfphQwGl3Dd4jcFoFuoB02wQ3fRReo0sYcMKAQ7UfrXKkxOoA2UA2Dcc4Sm1hnwnsK2ZQ+I6z8aSKwtIX4DL7MF+JQOztEk6Z/'
        b'77sexrwGMnxzdljeSyMCM2OD1723+w/9l4izv1Y+47tF0lfsb/xG8up7i1f0q6yqzZkUUdeR+/1f1098r+XFDfHDnrstnOR3OixvX96kvPlBEsWYJWc/tejfr3vivbt/'
        b'1Q766OpO+eVxqvi1O34IePXa7hndNYP/+cd///3XN6SLv/jLGweDmpYveifmiftX9KP/HBYiF1Pr8UkluBFI0w3c4mwQaLcGXI32UVlkltQH8C+5JxiEhMP8XcGF5bws'
        b'sqEEA83I42CMp5LwLVaFDlZTamMKQO1AzQApo/NGVbaCY/y1HCDKu/gqtUSUzpj9iIWhCgrssgsRy/A5mxgVgloj0ZFMZ7pEqBK6tlAu/hHk4cU6UW0uJduNYsyRvRjT'
        b'IBSE8tw6fBL8Rw5hpf8Wi/pyTkjEVjj/R00XTfD48BHMdMCL8aKt0i62R1intlR5v0Y9jbFdV02OJMkrFsSOq9SFj71K3XYc+Z6A9XAc2YusCN4wq+vJN4PBGW39dJ81'
        b'MoA0WbZOFkG+RcgA55p5xTdBSNolxA+W6IEjlA36uogo2pANM5o8q5HN5LI/jUN5rTZVVOnrtUpZAdG1L9abtQ7sR+ugA6DZ1TJdrQEw/o+gMrJcDt9AByqT8O8VUMI2'
        b'uBGZBTtjehbwHzl5uairKAudw81RSuAHsvAGH9yEjtaNQWsp6stOLlTBRsrJU+KNwKIVgQzfGj0DeA9FOOoSMip8zQd3oza0IxKtofx5kAmfBoH+DNUBCAzsaBngx01o'
        b'h5W4B4ypR1sifWoTGWYJs2RYIpUB5ldpIws4hgUm8sZMBu/BrahDv/7Ye5z5FKmu7tUn8lIDUUzwvvnpE29M3rpz8vs+y1dPnxiSpsrqm8Xm3B7xcn1WZ9FnB99PCf3D'
        b'O6M+9htzaetfftMx9Nu/jRyY0HG1uK0nZMzO7pKqkBDZ7HEhadaxNxe8saF77R+FX7/21LOBfz790dPPLHnjje7krb7z9741fm1d9devls9dtfyNV00T1626Pez3KDXh'
        b'n9dDP0u9HNmwsnbtt7N/p4/9aPNb5ZvF4yylTYIXfxX0xrLkOerL8iDKno1Am+vo7AKgJ7PoCqCd82gNPkTZK80TMDXAbRIOUIkv0bvoW7kVqK2Q4gZVSCLuxlcW29Qv'
        b'vugkPgPYGx1F23neD69B24DbJTVsjALBJ98HdXFDlpbwNiH35CQNUpTZNNkfX8SX8jh8J4u/bF8TOlAVhTYV8G8N8J84JJTDu4D1a6FIsc5UQApHFxCfnpVA7DZzEYtH'
        b'0IJ+JeMJVZAr8WYyMFkNExQjqEQnhtNOCdDaTBs6JahUD/zoKKh1Pe1UP6Cc7ZHR5HBBoZRz6EQmYLuDArQen9NRBn/hyImUvY4GWU08Phxd4QYAkbtA02YPHaHiAdMa'
        b'CqDp25dDh7XoIk0bhA9XERHFNhOZaLuFC4uaQHskBdbc+V1R7CJ8El1KlvNzeEeMr/A9ghZB/jifz0XhnQ2PU9D8CF52wsVCslddbV/Iry+vYpFQpx0pMKZ2lUkwxDYE'
        b'OPAmKc1j4i7bSwQsjIsSxHsnuzg+b+9l8vXw+OERhN3Y3+WlAi4Ny20e0lMY4k/vcDsGxGH7kYv4Dw7++zxysxSxkdfUVpSWUt+fHkmdqbZOa7Is/Sl+R8QonprTUC0M'
        b'ZYEptaEj4Nnwvv91Fdlj19FEXqPwAVnGbQy9NEDoxwJLwHA/CDnGzm7/0HcMB5IF971Y8DM/hYECKV/fo3VCrf2jpayYcUrtfQ/ND0NmDEoOHCzh3/WIT+E7YWbyxkZz'
        b'YKCgPp4JGMrhww2Ifw/jPLRN5o9OWQiu8SdnKdOnK8T4TiYzJE44ajre9n/idUfu55A++fR46Yn+LPFpGcGswltGjMT76IEDiOCrk1VKdDEGyEN4thBfYxctWcAf96yN'
        b'WGl/vRyv0xmqxfuLGMrTEg+QUbg1G3BTehVuixeC0NrK5WTiw/olqL/QTOA5pz3ws7J5T1/ccrgjdv0itsLnA+7Eeqn/wPSMqI/7nuj78frcsiSVn//czsPPn2iMXW9K'
        b'Otx4eHv2NnZ0H/qeioUZIfNe6ZCLeJ1KUz+8LtKm5LYqqPviINRK05ZMmj/OxwX3gLDQOYpiWEn+cl4FHsUy+NpMqgJfWUsJgwqfRutVVOhW4EaH3B2FL1Oc5Yuv15Aj'
        b'2k0D8HGaOJ/TAnO5/nE+K1KQpICB0ZYSiwWKkUgfHBhpNFHdEgwkhKdpmWOjCXuEpECP2OZH5vZSJXIdnGm5Y6OQkiM4e+2rbb/vOfOFvJ7w3AImMjxHkRWVg9qj6SHr'
        b'6DxGhneI+lYNcAOcfrZP89fOF2xEkksmACo5jWCdb7FAK6RvnGPIu+bauWIRhCU07EvDYgj70bA/DftAWErDATQsgXAgDQfRsC+Eg2k4hIb9oDUfaC1U04e8rU4TBTuC'
        b'1fTT9Ie2pba0AZowcqGGRkHTBmkGQ1qgRgmpYuowI9QM0QyFOHINBtskhBLDNTJy+UWnXyfXKdAJOoWdIvKrGajjII58ChyffCz/FPI5nJ7CR79rRuwLgrr8eut5tIxm'
        b'pHvcf/bUjNrXRzN6H1ccog3VhmjGDGQO9TnMNLI0NNYeojn6UuND3pVIAnPiY7vyox81S/Sh8yTSyDURENdfM9B20YdvKdAm9VTggambt5ua3VWC4A0cxfR9gmKHcl30'
        b'85Xr5MfdMc2PV64HjBMxdWW89URUv0j+mBtXtzFPlydwzPSywKXmeXzkDukKdsugL0VMjDq9rVLJWMnlIbPQQZ3z+0KzXIRFQBitPkxhJbBklyXBg/EWWtGF4lHMS9OB'
        b'mWTKRi4KlTB/tneSevTpJ1+YwJnJAEJzC4a2XQpYHSMV/mnTpDLhtUMvDZNOrMjYqoxhQ7a9Pajp47989Eppw92tL4j9+5cUfOjbviCs0++VX7w8ZWF9U+jCe3OPv54n'
        b'LvWpWP/Lpj//cXL6B69m+FS+Yfnb72ZcKu958tT+gXOtm+W+VEJehVrH0JctJQmyFQJGUsRZ+vhSCRntQxtQB4jfF4hSGe3CxxnxOC4EHUOnKS84EB/IoQeM/Z985Ijx'
        b'9hwLNaI4D2zn7kekaHR+hm1uxgwUVeGmWCror1xOjuwIko1EO3BXuIKfQ8g1YIhw/DTgt2WkwisTG/gXQ6F2vBmtRRuIJT45stsrQIezR/EnqfefMvdmmh2Uh84ykGO7'
        b'AIQgvIP2vDoUXSQu+BujM9CxbPJiZQlu4dA6vAPYTnLxEGpTClDrYqiD0ttsDt0F/Ly5AOjAxgK8SSlmUlVitAMd78Nj2Z/MUPY6gg9zxt5xYtZPJGHDqEO4TS3KNoQ6'
        b'9swjL1HklZg9Imqd1CMkxq090t4zLGNtj6/eWGe10Ou3eplNZ2NxkWkt+b6aPBoZO5+5xqWf0W504E0XdtND/36Od7WolHTcq59rBmfbFc7tONy9h/TeHerm7ao0qQiK'
        b'+RmetwGlzrPntUuT7V16OMypeXdPb+XP8bD2K+1dK28NT3M0PDTbntluV/mz23W4WRPwKa3Re3d1znE0259IFjKdqbbmPx6nvT31Eq/t5Tna60vbI1a3/2Fr4lJLrUVt'
        b'8NrUdEdTA4tIRrt1rtf2/ude0x5Zao5xf1MgpRR94wWyD8kbxJmy3N+OSeHp0LtzfCZ+xVIbrKjt4/wYfVRAi8hMLkxLHHSPvLg2S92pCf9YpZbqPin7hPl678DCXc8O'
        b'XDswJZ4RRJVdF322YpqctRCbKHQLb8DHnHEcQXD4EOp+FMkVoE2P4UupsEcRGn3FmR2hzSaMaEOIM4L46Q7VhW5454KLXtK92gc/wM9/WQLy6OTuLgHZlmt+tJAJZmJA'
        b'NF9teCu9oJBOx6BBb4Sur6CAyqbG6M8e/afQTE7kn33lOf4tw1s0c5/ehXahbyZd2dIleOm62v7exYU94oNv75JzlBoNVqOrj64Uv0qlAididBuf4a90uZ+GdhPdTwSb'
        b'olCSE4O1XDy6gk89TrwIKqX2xfoGbWm5obaiuveFePYlndcw0GneXXO7vL1VRA1j3SUNIno7qTO2wmOu20qfdllp7y267E37YhO4sr/NVQDLLfifCLws4/kAiS43s+of'
        b'igPsWz7AJQ7v128KQ6XgZcvGoTOQs4GJVjYMxOvoyVEc2oZWozMw0GUgJVqW4e1DqVXGBHQf37Cxj2vpcbfNxrQoPF/BMgloozgQHcPnqEFm+5PC5f9ggymnumjKdIYa'
        b'GL5WlM89O2FyEDUwnGsqW8RQQ92+fYLtdzg5jAyJiaFtV7tcj3QY7/ZDjdD6HgZto+iQulPitfVoEy+Bg/yNN660ieDoENqtX7v2itDcDLk+T58x5uX0QBQTJihL35w5'
        b'YPav02Nml6s/FL8U9cnB5399rNxP9avgRS0fnhht6dZY/rzKhPr946+DQ96L2f1s8/bMSiQfOalIHTZqcvoXz+0un63Mzf2069lA6+2No/Z8deG3RX9K/Wh4944/rDp3'
        b'WS7b88Lsv68v6V8d++s/vZNdumTDL0UdIe+8tmrln86OPPWLaXIfXl96Bm1m7HpN1IF3UqUt0WwWlNEMCcOU/uQMZ6ObTRxXRPfZqEX4rOd9BvOG2p6ybTQWtVJudDza'
        b'leEfYWNrK/o5qhyOuoX4gl+Shb4I+hRqLqBma4SfbcM7USfeiM6C0GyvWczEoNPiIVPQVbp7J+OLeJvN3AxY4W6bRUBgX8qTj4K1uqSyneZb0FWbYgHfwZvkjjdne9Vm'
        b'iksXm/S2N5+68J+lxECMY4cB/znIZjgmZRuCnXYfLej6kma1qdLshbvkTJ2um70DHvPcNvsJlxdiujWXXyF02o8uB7q21/VSNzjH63qF9IxJBNtc6NjmIrrNhStFtm1e'
        b'5Qmri9y2uTif92DeHxqCNpcgYiM9HBb2DNpBxVdeX3cGNw2PnKGYrSBWHT5oW00INwxdxKf0rzdcE5jJrZLrJf8kaqot6K1n3nnm4pabHTcbb86NWi/fLt01Yv3Nxq7G'
        b'1PbsthG71nSLmLNpkqXT5gB1JuJQiACEr1aqVkEbGxYU8OYdLDO4Soia0RV03b4Sj9dei0upbwRd72Dn9TYEUrMKlymnWXldtdjJpI6allElkStC7xLysY/kpKu9HR56'
        b't9XeHepttWnT3hd7PEMt75gmMVUwkCX3+RlL/hOVAqJ8fmlJn8ukaH8hWdgdLCPAt4mTdl7AVH3bsreE9HLOJ946+lmZSv38x+HvZ/O8VtlnZXpdxI7Pyh6UVes+13xW'
        b'xrXEJMVbLx+PsV6sv3g8dmOs8MBH8XU6hrEUSv/Xp3t7edKfZGfi8n5totBzWtm+zitrkvCmNMR8s5/TFPeW4ava4R1+djrWcRc8at3WsSPMeR09N/KAqP+9r2gKv31F'
        b'tg0s+u9vYPtq0ivqDuMjPrCceHt8loDBJ/FakQ+L1qILT+hz3/0nYyZ+EZ2ieZ+VZavvl9jXNEv9aZlS/UnZ57Cun5cFq6t0uRWhFTx3dmqopL9iB+xVamJwF+8NV+Wi'
        b'/egusXiezyYX4y0//QW7PYGltvtGnZbUhZduIEvaEOY0zy4F7BoI143YI9apKyy1Ji8IWmja623zEg/+xW6L3trXedG9dkYexJvp9lrtEoPdnoBe8bpau7QnoL7WWlGl'
        b'NdEisa7BuB7/CnKFi5a8JTXWORDXI9HozfzdK8T4l7wo3kIu59VaLSBUkotkyd7skWqXVFSpyTWnECWX0EMvE1ErmogziadrgMnxVzGtkVgnxfb42e9Y0Wuc/NJLaA6L'
        b'3mLQ9kjISzZI5h5/8s3u702j6SVOtKY40xFSxoe4HpbXLqFO6T2iuqpao7ZHoFMv6RFpa9R6Q49QD+V6BOX6CjnX45MxaVLBrPyiHuGkgplTTJdJ08Sjx43jJStLeAIz'
        b'cSuxXRQspvbJbJNEJ/kZvK/bnhLYqnbdUxU87zty1Qr2O46Z++WkxemNaUsZ/laLq4FokxlfCzKhPdkihsMn2Ah0s4LuvyR8f5bZUg+J+Ko/y/jgPcBK7ghE90ZbybLg'
        b'fWhfSSRhd86FZ+Ups/OAzJ6ZgZvz0bkovDk6Z0ZWVE40cLLAadldh3BHiXSSTw21cSotQftwxwz41uA7hMnDhxV8h+7iJrQ9Hq3LJEbM7DgGWMJjaActYsX7UuPxcXwU'
        b'wDyeiR+MD1MbZXwPdTTER+PbCTEcw4YzqBO1LaSnHUa0BZ10+F6wjH8xh9bjzfg8asV3KcVYjG6hnfEL0dqEGDHDysnlm3dwKz3sWmwdyNu8JgpVuJMR4Uss7sAXrHQy'
        b'v1oUyRTBWgaHakbuTQIWnqKUo/jAmPjcVQkxIDhGMMAGnsEnqX/bYrw9T6VUKImb3ZSEPAU1cB2AjgknoqNoF62xKWsEM5FhUg7VVo//NLWGNw4fhw7go/Eq34QYAcNG'
        b'MWgX3phIPXyI3TUCQaE5WplNeEoBLF4QaheUD+BvFPnsiQEM8LHBZSbt8hfT+jKULaqNSY7Px90JMT4Mq2DQbtS5jLcrO4zvzAHWNAp1WXCnkBFGseiWgr/0Zc3oCcxy'
        b'hgl7jauIO6efz0MNakI7MuLR6iUJ6CJIXEoG7cFX0UWaNgNYqQPE3DcPxCHf2AR0kkO7jJW0smenqBjgMCVlNdoIcYCGH2PkIHwjXj8CqoL1jmbQXjPeSWsKQJum8cZj'
        b'2SK8qwYE4g3cqLIsWtPtJ4kHJSN7d2614cLkpXxNc0CWvhWPD8YnAJ9Jpms7J+fN/bap6lTkQpZWvImsKLqI1omYQLROMAFvQK20xqoBqUwdw8SUjWqIO67T8TUCtVm3'
        b'ID54VkISR4e5E28ppse6Ofg0XjvUxFea3wthg1CnELWEllDgwvfwodB43IUuJSSJ6dh2DcJNdG8FowucrTBZPnR4CPSnTpAiiKKdaR4dyhBc925MxfKzzCTbXt0EEum6'
        b'eLSnPI4AaxQBsG24kdY3C9+fbYNWDmB4P4DrZRZ3rsS7+S1yRoEPx8fjE4kxMDNxFDTNfKVN6OioSBWx0GNVIE+K9dzAEnyIwsuKDHw3XofuJpNCKdD7IB74BuNd+JwN'
        b'9lrQBYaRjhf4pwTjG+gg786I16Fb8Svrk8l+TAPgQGsr6X5EV/H1TBU/V3JiZy4NFuAj+GA/2IVH6MA3B/uSizNiYpYaDX1DlYw1BCInTqqLFyYmJzC0tt2z1Dwff3kY'
        b'ugC9IH6FKhHaiVoZcQU3eLGc92i4NBvvjF85NzkBoCod+jAD36RTETx+ngqdwqdU5HyBq2UnAjDctd3Pg48kxOOzyckJ0O/xAIlD0DY6uzNYtF1FUFkbbmNh36xjxH04'
        b'X9SC7tFO/13UwPwNwPpQzpL6hzMDeF4UbcYna1A3upYUkyBi2EwGHawCzEJdtO7NU4JoAMs/Cq0RAKd6j0V78X50jNbmN3Aa0wb9fG1CvV/66ME8IGZoQSLtRptNMQmA'
        b'CSYx6FD/GL6ZU8HonAqfAPm0JRf4mAVsNDqt4k+/BoUxsHIxhzKt816MF9qA6GYV2qUifpFX8G0RIxSy6KAZHaf4dTbwRBtwhzWFN5Z9CrVbiY7SF1ivrdRFoSh5ZhYI'
        b'v4rZvPUZbs6DejYxzLRQn8Fo3WwKHHhdGt7p8CslRzS70ocATC5E53pvir6/kLetnd5vpaF9SpHNr/YiPkvan7UImM4oJmpyIjW5DceX0W6VyyHdYCHeDGRGyIxBp0VW'
        b'tCGTToUBit/FrTOIB4xw4EhGGMrOHz6cn6UNY/FVlamuCLcDOODd0NZIdJPihgDcHO/sH42bjXzHxxSI9A3pFDIGJSzAZIEa/cniwR8s7np6CVMI3o1vRcJk5OFNWYoc'
        b'IvDtV4LMFytkxhaJ4nAbWkMH/FToYAbgVxKzomZIfHoEDyL4ELrhDxWfiQIOG92HP3LlE8UvwfjWYpdqC2eQWjlm7CxRPDqcyo+qc8hcVTm6NgNIK4vPAu0E0neZ9jiy'
        b'BG8vzIMy+CqsJreMHYIODOALXUW30TZV6opZ/FwcZ/AV2QA60+Seo/suPuhX0U06F8NRqxBfA5BZz6OTQ6ipEDq+Vx5ArJLhrwGf572q7+LrK4zoBtnkyux8KJytiBMy'
        b'g9EeoQGo1w5+o+3Cq8fgvZEiASlAyuzB2yidFBrR7nTsWpqD0nuFNXj7cIqUVsbi7bgV7UKEw9IzetS9nMctu4zEdmNjlB1Q1qP7LBPUR7AQn59H9Xxa8WLUkRxr0wkc'
        b'kFGXYSG+gHfglsBI/vouAC7eKoIZgq4KIT6c3zVA38bivYC/TsLeQLfhD6ajjWIndGQ48WXZEgFcSTVTbaije3xy+pMqhSJ75GB0NjyH2Lj1mSjAnWZ0hG7niXW4Ce/1'
        b'RwelxP0F/vDRJF6F14puoJ29bie+JcTDU2AAEt1Cl28pbL0bZljC7oAAYqy5icHnZPUUxu5k+TNQuURWslx6PaaEp/kz8BrYvq0MvgHjrmVqUdNwOm4x3gnThc5lEX/0'
        b'NlWBIieyinRTBnvrImDsNqqrlOSOZl+DgrLFgQNeXvJN0j1+p2bCPtuAzqxCB6jatGFmmv6XBT4i8z+B172zUDH/jbeNb04PFr+b+tymN6/kvb8htLz+xXt/7dsTGt65'
        b'4uTnJTfCfOUZs/p+9MbNEbL9kZqvhBMuPI2/lIz3uT/u5I5fTOl86c+pH7ywLzZj59xv/3bol7eGX04+cjjueFHJoMg+lru7Ri58PesXC18b9vBzs1zxixdPjz2wqjD2'
        b'0l8eTA5YuVcW8KXc/LT2zEe/63z9xLPbJbvzT4S8OvnZ7t923GhJzlv0csT5dN8pH8sCxpVM/nhEyf6EKdcyivNHbv1iy9D8+pbP135ef3mapvbw1xO2ip5fOc5ncmBm'
        b'Uvr40aYbr70XsvXo+rTnJm+alJ+SKjednv7nK8/vXruvX6pP6l8/XPv8lOfHjGsduXPEnLOVf+535LMxCz/Y/FXML4435y7dl/f9hREf/OqYOved7w6Pyom8Y/jN3B+O'
        b'vTSn6usr6e2D9z9YunHYa3U75lwevK4o5Pq8vMlPZN65OHDx6YuDNPJXT327/NnqpVNfLqv4bmH9q0c/PyAwnhyz/HcVL//uWM+cBfmWVY0Xnhu0d8u/T846867vn7a8'
        b'Mqe7O0/z91WL9ta2nMuTWjPvjak0VgQu1sSN+FO/m8kh9558MGb/Bz5v676e1PXlqenvXfrwyRf+mvbhyZGvmrq+MW+1pr/92y2lWf+K+9OdLaX/vh5gXan4euyT38x+'
        b'f/G//rjw+3dNE1pWoK7Ahn//a8zkazM/+dVJ46jfth7rerOs+OSL/1gVofh361vH5H2oG9Y4vINeneaMsieQex8c5gPoUpWFAKcfOrcsMmMCUZxzaA+bV4238KZdbfi0'
        b'HFgjkCTQ2ZliRjiZRXcX8K5b4xfge2VDUWtQndSEr6D2oPoAXzHTFx0U1ObgFt6U4PgUtMcfdUVlzQGKa1PvhuBbAnQOX3uCv/7+OlDvS3YLsfH9bDZiwEbR5AV4D2yx'
        b'1mibfaoEH31qJodao/B62r/o+hqqG+a1e5I8vKs/p1HV0jGllyxX4XN4fQEZVD2bgU7OpWX0wOOcthue5cp412uziZqkTUZt8ymBxWt8Od4HcCzaS4vha8oAhy3HUXyT'
        b'2nJMSeGv+T8HFK/b5iw+EW101o1nGHhn6ft9yS0XBdlRgieoYYWz5QXaFkvrKZ0HwyV5iuU0j5PpBb4QSG1C9IloPzH0IEcTRHoh9st0+OjQEpaJTBWha8vxXerOF7Zs'
        b'It43zKEGdVWC+hbx7hc7mOpel0B8od7ufdGKtvJD24pOo2be2MNu6YFPFRFjD8BNni7G/9nGpT0CtYZX2yyBh0Nts4pRhrL9WSEbSq3yiHt1MPzbfrlQ1u2XxH0qGRrM'
        b'jiau2GwYlCH/UlbCDWJlbCAtQ2yNSd5gmj+Y7Qsh7nNJ/4aAXp0M9MdZVW8ieref69jG8aV6VfhX4HGa6IWITOvQC61m3hrkYoLs0gvvJ+hUA8i/HYppEjk0gCzVVjz+'
        b'HN1NW0EakTGPaivG8dqK35RQDjFlln+Z4YvBIxleLUi5h0aA6M2oA0AOHWGYYcwwdDma9/Y6h7eJUAdTPRNkEJBC2lE3T6F39AuOF4LQupFh4pi48jjawodCKmrMfbW6'
        b'LHditY7hr1CZRiNlTEVZ1E1lFc+t/pajmpMlHyepB0+eJuFpILoWNTcehAuQMpl5aH/F8gZK2cfCntkbnwAcLNrJpOEtWjO6RCspNonJtYApM8aURR2OTuVrTllO3xPD'
        b'dK4sy92TM5Tvw5FkGhn+w/Iyg0/AED7n0Hj66hfZkjll0udjffmcIQ0BJHJi1Ywy6bNpFj7n35L9CBtQJh5YFvVaUR6fM2E6jazb37cs9z1xAh95ph/tkqQ8vCy3WzOS'
        b'oWqP+eK5wDhmgGTZPouw2KJ6FjDX1Ug6wzONJtQBsl0M0c2MZtC28b60zW+DRzGTGWbJ3yRlmavVS/lz1REpY9EZoV84ZRFwYxidH3+8vw7v9YtbTGYQ/tB1dI0mFOIb'
        b'arxXvARQHIOuw99EzN+BMwQdqsEd7EwTwygYRfIK2qBplYjI/9NvZZZJYxb68jemxurwOtwB7CH8ivAxYG1ZvAEY3gh8nYeP1fjabNTBZhfCfDJDUTNezTNdV+sAD5Fz'
        b'007iA9Fru4xP8V7wmXg36p6BdxbSIyMWb2VDF6TxYuYFtB+fiPRBB+OpLw26hNZQ8FiAjiNgkRh0KQ6YNmapMJJGy/2l6AyHWiLJufIytAV30ONbuhybsqlOo+z1aWW5'
        b'b858klcnf/CHKxXMd/HUFuHrs/rKmG7GnAA7J37ykzVb08ntLRsq678Y/cqb2UOagv9Yx0wOGPo+dxNFr9n3S1PA9vUfxk1764sQn0OTU0XvC5snxSwY90xmQvo3q25/'
        b'0yO/8Vpq484I/8P9iz5Z11YVfvTQe88MONLn1e+q5k7t87ezuo/OiItV+/8wMuuvryk7l/1m8rg5J9Zv0p4UbPw07VpOUe2A4x3XLt67+MyGpdrz+9ZvyGxK7FlUZFL/'
        b'7eSnt5fMfxO/Zbq1oeeroK8eDv7+qQ9Km9+ofX3WTsG686qucetiFi18vzMflbYv2av+xdtjTkTmX7joMzz+dwfzN3xt/t/NXQlcU8fWv7kJIUDAgGziQlxAwqIsirhv'
        b'QFUUUHBfIJAEomExiwKtCirgBm6ouItgta7gioq2nWlfX19tv9Zn22faamtra2u17bO1re2r3yw3IQkJou37fZ+RSe4299y5c8+cc+f8z3/lf06ee9zly7hRL4w8p0mM'
        b'O63xectbJT47p3hr7fypN1YmxG3S9Rqw9dKGd/26Jd2bvqvmyuHa2Pc8k+8WF6r+4fLFwzfveb6Qdv3Bsd0bt98Cec9dGzj86vLllYHfxK7IjfinzJ/M7c5Cw4rD+WIh'
        b'OAJW0QljWA9XUzh2S495ZMofbvBJjgjFg9EZFm0vnUfCwp+bjlSSKdY8czi1JHrAJorniUnEQ2vhiHBTmCY8CXdQohu4bQq4PBYPq5Ow+4mG5qqJPMZrNB8cRw59Czl3'
        b'GmwB63DmKIxWX81jhEtZcN6/F9wYTmwtsLc/OMHZWvHggE0YK7a13MAOIshC9DhhScL4cO8Yhg+P88A+8QhiY/iLucATU9hJd7g9Jk1GoOy94dlRuH4Cz4cb4Mv03aXv'
        b'DEHXABGF71ekS1LgRgvGIvwuifEK4oOjUfAYtWIOwSMlJjMGmzDRYJ8n058gNmHLRFiD/KldrdGflkaKBjYQQaaB4/MssgjAJuQwE5sBNoNdVJAmuC1vRufWaizsmK6g'
        b'gUzEFxYugwezUAcYF96vH35LjQSFL/Hh5okTyT1RIo10notoJdGslTyLgNYuNLmMsscoskt1khNsHs8IWB7YAy+CDSQQYB4yXjfhqf5pPS2g++GgkvS9znBrkUVYAQkp'
        b'WI78dtuwAtgMj5D7HwnXCbAh2h80mm1RZImCM/NorG5jFra17RhmvJH9qV0Gy31oXPA2PY5HQhaVD2g1qpBFNURAEwet0WSGhfZDjuk6i8RBsMlgilDo0LSYAAfiEasq'
        b'19qq0op5AtaUHsCb2FTe6OOLPv7og5c9SKoAb7KHF/dHPreF3dgvhN1xEhwx68rzZgSPRXw8WypmRQTRVeLRar9gASzi1dqRujV87Qwq7tsxkmqsps9sToLaBRsl6GsD'
        b'+Uom/7Xb8YKfDS6LBOZqMZEZDdYlUbw4gNcoMoVzmn7h+SUaBEkAWTjeisRhkOl5MrdL5vqM4ozU0VNGT8pIn5makGbk65R6owCj941u3Ia0hPQ0Yv6Ry6OW5Z/PDKFd'
        b'iopw1oTJ4ks8nxp15eQh8HD3EHqLJM6mfBBCErwitP78IPDC20zrWdvtps89wX1hqAfP4w+hk388TSz/MtwyBD0luwa3qnknRpLOnxWuaDMLbSJiIVnRrGhkBTWdCM1q'
        b'J9O3gjX/4lc5K/ogQxgjJzqpBApnhchMKuuicCV4FzFHKutOlj3IMiaV7USWJWRZREhnXQnprJgjle1Mlr3JsishnXUlpLNijlTWjyz7k2VxjUDFYKkUXXaxNUKMaJnv'
        b'rgjowuzzwNgPbrmradkP/W1jq3mKIA7v7UzSIrlVdqqUqFwINS0hjEXbXAj9q4BgZUSzJLg1FD2reJXUARBXuiPzv5eiN6GG9VR0I7GXwRw1bFJywqOtVvDodBNlKdpE'
        b'eWGlIZjdA/M2yfMVuO+rbZklrRZC0zFKm6NqQr8KsnQFGswojcHlODEv5cjEiYGVhXqam5ogzW3yJWtxEJLM2ejCcY5hjh7uJ5kZFtFcoZitR6FaZOQvyEfr8pQKtSEP'
        b'rRMVIskXF2gV2lZyWrussNYJqEypv12Q4+TKTfi6mRNQdYQXViUTfPZDh3lhcSM/My/sk2lh21DA2gXYPyMtrMXNMMuBk4e3IwXa7EiGfKlcU5grj7AnymBpdi46ZTZJ'
        b'0d0+S237JLV2CGmfokWeSFKL+iHNZhyfOE2qkWdhGnT00zJBtKyfTeplSq9mVwpr0UnbhkRbNIUd4TlB0LPwBIpcR3S49jMwOKLI7SAdrt1KWyly/wQdrul5p81Ol6Rq'
        b'BXfDYp50w0xKgkthzS1JtcoctQ61MFJOSIeR7hQuNXC3zZCPU0k/E+tsJ/rOROGGXxw0SviFmeLaET0YEqYBtszLtEsOy2XcQjbj5HGwPtAib2n5KLEEVM0kdfomejMh'
        b'zLjebqMyh80VxzMGDCQHVdKeduqER8AJi3oJF4tlPtS9hWLYMB+WkooPu+IXGn/39UjNDBfl6hkDDhfMgZXF9oQFLZPHWXgXllS2oBmscgN1kylDrlSIKWg/nc3DSAt9'
        b'KEMz824EZ+BRu40wPiwN1+WsNNVWCte7gC3oXOdJfctE+H3QK9PFmZnhZ+JyqJRw/ZJR9mrrmQVXtXpyNkKedQP1sCKC1HovD7+NafblSzInVskncDfqch4st1dtL9AQ'
        b'YnJXrCq9AI64wVWzJeqpB3bzdOuwUVhaHXHloicYJU6YrH4cXTO654+fsuNqMnPEPo0e6cIBo2TXXpv9dsUO3V5Nk+La+VNvVh2t1TTX/Pxj87CZY7/y+6jx04rZvb91'
        b'TcrPDvxyREnn9xQD1rxY1Pnm12O//3bPZz5LX9n5fIXP4/SvDuYpvgnq51OTUbN2W97S+fdn3HX5Y8XeypuVq69O0P7OczoYt+xsncyVvMk1zO3F+Y+gEu6gHY76j6AG'
        b'nKYve6twiAB9j72gt1WI9xRQTiJre8BToWY3FFWRBhtJOjomENYK4IkFbmQveHgWKKeOaEV3W18UngEHiDP6XGhnE2wc3emzBDieAncSLzkNnMvBDuRCsC2Mz3nJCgk5'
        b'LA0ehI3U79MtS3Kibl+cB7kCH14IceNBmVcbT75hGr3IvSlkSmEcXL/UxvdUg3oC7imBx5CQa1NAHbZaI+ApeFZHXk6gpYnEho0QMpPASmewu7fvX2bPm6GNGIFh4bAt'
        b'Y8YQZluesJXlljLekuyj5iUTkSwyORxw3r6Mi1dw8SouAC4gLl7DxesM82SOGFFHKnG3uiYZ0pM67IBZ+HOlzHWrJG5tJX8a+KFrhtlgcghYm4qkoHDI1nNZkN/iVe2Q'
        b'33YcEakycZFaWE8OhZphEupRDxsJiC3wrPyvJkvJ4Xlnm88bSM/750h3uRMLMpB95PCc88zn7ErPaWFDPRvfqyADmUEOzyc3ny+k1VCS28JOn57YV2VqZZNp4lAChVmC'
        b'APy+wsJ6eWYyYbPT4+icOVbnRK1stnksziljKWaZvPwwB8gmZ/MtRMHx5vjpJRGyiaggM004kQPLuaquJHuvWCU2R587tRt9zic9RfCTk1eHGZOUmB2yo4RJZOen4Uuy'
        b'5EdqUyXmSzIDi0PDpaGWCGe0TEDTaCdLthdiy1IxMIlGx/0984mGSNMK8rDXQN1rnEeNgynLswoMeo6GSIfsU0dtg/9hyg8lbhKFWkUIYfSc/W19UVx7k9SQqNlyuCxx'
        b'dkxf/G+8mcBI3p4rFxVr4cBIQ0wsKY5dGct2pWZ6m4dUGjI6S6vMzs3HBC2cX0dyxdkVtLUf6HTqnHzSFSgNShsuLp1UbXlVauTi5DjgWjG5LlHkJscONnsw+ExRsnD8'
        b'QsRE4Iv3MDP4ZjtyukivVJPjMSUUbru4wR2nlFJZXxC+arVS99cRQoVgAiRC3SSThobmYbcaXU5xaOgzU0RJQwgdVARlVXqaqtuhg+rQ8U9LziR1QCrliJypX8fEsIJt'
        b'tEvRFGKmaIqSSWdHRTumWLKEfnC30aCkl6POJ4ISevX4SZNmzsRXZi9VLP5XKC/OI4lmlVo8RIUT/jWzN2whUHT7ArXLG2X9boQ+Lf1NT4pdsaghZMk2hU4fE+mYOMwS'
        b'KGN6U2TxmKC16InM16mpUAUq+zxcivmoZ5D2wAeQbLvyIvy7gxRE+N9oq0p05CWZOjtXryY8U7pWFrS2z6zDOiOkUZjKWWlAytVcAerBainXREhD5aEnLmFqRLpcn6XE'
        b'Lx7ts2JFSFF3oYlBNYa8Bcpc++0fIY2x2Y2cTW5QlRj0SjRy4IzL0mkFWh0RykEdA4ZIRxtUucosA3700AGjDfoCPL4tcHDAwCHS8fkK9SI16swaDTqAcrXpbK7cwdGx'
        b'9kR++gYaZK8atYVYeU8nVpy9+p6uXQaThmxt+ie0vN2V6bQn4zeENnI/dU+0vHyVFl1NCG5bs0zyrBJDjsxx97M8XDooyHEHtNoxarCjPVE3y+/flgaTbhxoW02so2pi'
        b'26sGdQrz9bVTR5zlbg4vbbBVZXauy+GAxgH5kIbjfhF7ANmkSLeaVHlIGh1jHQ7YrThBTMWOhkK6hGyckCS0qMxHf6ibS/EYFNcOm7sZYWhdTbRNNdHtVkPAiFZcgSGE'
        b'IDAejzcDHR5mBi/SQxOmEk2NV0hD0EPOdXF02x03g0GLORMxHT33K1xqYdslTJ0iDZkOG3K16CFFsgxwLIoFbrK1MvNqTihTVboFBq2urVDtmXuOzEtiSnbc8jObaKOt'
        b'XvZ3zIYhCM8h0mT8JZ0dHTm344dF08OiyWGO74YJOsqZkNwydpvb6wcEV4oOwV9ox7b7OdZi45RabX7/RK3cgApNv/6JamTdOdZaZHfHugrX41g/4RM4VlDtnRlppYRc'
        b'ZIQh3e9YNRHZkM2msC+Go8ZDVqxSqceWBf5GBlZsu/ZdVkHRECmeM0b2kwpbrWgFanPHNxUfhGG99Ci5RooX2j0iW63HDyQq2zX3KJoZ70l/kIrDsZ0eERMVG4t6mmOZ'
        b'MIwYCYS/2u2RKjm62kSkVNrbiQCR0R3CX9LZsY535NSciQ61nR5tgkgPkY5Bv6glPDt6ULv7mx9tcoj1ZF677W0CXnNH0vvjWFljwDUy0caMTka3x7FGzFJnowrHj0Wn'
        b'tvNEtoFMt03SztE47VrIJzC1SNXXCU1aPpdl5wR4aXErwA1cCsQYNxZs8QS7yFEfelFsamRwKbNaMItGLS8GjYMw7I5A7uDRErAX1gSR3XckUahuZL+3ogZLJBTy6DED'
        b'7l6AGdkoFK9kEcEhlsAmcNoEhUsHxymkGR7n0WklrzEU4d0494DTvvlihiSOXwKP+YYhQTFBYUo6PI8jA8HRCZNo0iIG1bh2ClM0wCUH7htPMD9+o1PYYb6rKAHijIcz'
        b'YygBIjgEL4N6eymKcD3gIqwcR6corCgQq8B2sQw0CdR9eR846XAq525vDiqvHj4f0w7evDLhSOBBj0V7/9Fs+Kpzg/tr40dq5GWRXaeO0co9/QcF9xXF/qIJfuPv+Q8Z'
        b'dYX8xvM3hx245DNkY6M2+z9Hrr4x58rqa6FJZ0s/uP9J599yBs6av6cf++bI4jK31+apb8XcWrKi4X5u/G99Xg9823nH5uh3r5SfGB82tPf78c8F7GvYHtPbveH9fgtc'
        b'H9cnfBy86YJ82V3t9oSckdNzby//buhSt+qy2H/tn6u6o0n7bahcMebxvlNl2VlrDXcG/7vs5vfVsVf+iLo9BoLy4zn7x80IAn6/3n4sftUt9Ge3Tx4/t2HWSpmITBjN'
        b'8S8K65eHOgrNNUwAH/DkWIpwueABasyUejy4OhmcBMcnkzmoSOfFYXD187AyZTw4KmCEGrYXPOVOM2muh8fAWhM9YCC4YJm+czU4RWIMu4GWLjS+1d4UUnSoeRIJHPMi'
        b'tcZ6LDQnRJrk3Ns6IRI8sZAiSVbCDf0w7V5yJ30b1r2XIA0yBc1gD9iYNHE8j2GnoN6yhheqhqfawjXEf1F+cBzdRuaucA+1mrtaxqSICH+egOfB60OSI+HfOGDQlZu3'
        b'YknYYQD69sXMQ2Lz/IxcoUi2Ss/R+tYah2RbTFa5PJXgMoFFJa3ZO81XMt/ujFVtL8sZKyspHeM0SKIlHHDEVArMiZY6SDukXYgOtlKSWPi2XHdBVEmOzHJiRFIVy4zK'
        b'1OS6u1MUwTg1OKAzYChulQBjLIPBKd4SPdxOYRw4rH8eUkXn3NBiD8N0ZvrcIIqzPBsnBZVD0uhxPHiRgafTIYWGR8W8wPtFlYaT+c5O8Z1McdER8OKsmAFeYA8FXCjh'
        b'KrCGBuY3Y7RUzIDOagrRyAZngqmSDBYyYoG/kJFmTpwf70cxEwH+EkYq+o7HFGZOnCUeROPx/whEK+M2sWiluKdkHt1zsY+Y8U/9TcCkZoYn94qjeypGoJUibye8Mmw8'
        b'hxr5w9uN8ZYWOzOSzPD/KLLonlN0aGX6DbxSc82Jw2E8wDiMwmInnB6yarqMw49vgbWJg3qlpaamMgwvngFlcCs8RsYSd7gysqBzTCSmAeTBBgaW+UCO5G8fPLQwLRWt'
        b'PQi3MSx4EXNVXALnKGB+SyysJqBgDtjh7ccDFzAFIAEj184AyzGwA7wUQbEd4DJcRdrSFe4CdXhuCMlQ25PpCc+DHWSUgjtTnWJQ+8ZHRzPRSODzZPcCUNsTbuaRJGr7'
        b'IpgIcAFeotDwNVPhbnguyIzR4PAZYGMqhRU38GBZRnFaqhQDg0/5CEFdcBIZ+OaNBTvMie0IOAPWwOPshNR0Cp8gABtPF0YiqhMwmZma12eE06Z1jcLxG/ec8Uo35wUc'
        b'Bv442AiOoJbFVM4H0PIKRg6qZpBaumb4MCGFDO7NcwaGldDenIVGyQbQBCvSUsE+GcMMWeIG6zrDRiJ1kJM7Ur3bdO4xkQLU5EcYeClaqc6qHsjq0PjMvCxIztvI0ex+'
        b'4LL6QWBlXJ/fy3et2LR8j++hPd6iSey9Cyc3zNGu/OQ3afKot10OeRbck0yOD5s5dG/LgxstxTUTt25Sy6fduvbWlpavPzGoXJuCP9z2evBnk7TlyX3WHl34t1MVTZND'
        b't2W9n7BqjvvAa/wm1dQ3Xt1cfDkhe8l6leejHtJ3qhZIH9bNv+AfcSJ37Ly308fN6tO91G/T/a3xdUnHG4Zf/WOksZ/st8zU93bfGFpxt1Ofi4861//kd6T67q1371Yv'
        b'2/y48Zup3T6/Kg+8dFX+7pHpmw8uj5oysah6zarH4tqyUSu+GbFcVlEbkTPvE8kb8y4d1njtat5xe3jaW3O+3jTzByWQJb9kmDap7MHw84KM3leSMnT/Pj2h6LdLM2If'
        b'14QPglXhze7nN/7ymZ/fNP1nW/8u89b3w71s+3y4xu4ABmrmW4dBgNNBNLZ9NzhcFEaGRbRNBC9mY4TGRnTLzpNxaage1ILN8CSygibyGEFPHtgtBgdJMH//EviiJU0s'
        b'WDuGLfaD58jGaXNhSxo4acMkkJhAGWu3gu1CYo3B/fCQDfRCmuDkMhtQ3gBw0h+cgRUeFH7BRZXAYyFkI69bDyvsBTwUGYMekMMkaCQKHsW0hClgV2JruBaNnoEtMwlA'
        b'YDRYF2GDDymFtb3GwpPUYjgPjsE6G3CGrjMNiXEDNaR54BaPeXC3U6s9Ak6OgBUUS1udOBXbrVHgbCsywwOs4I8BpziIika/DAMzwGmw0YpKq/ccmuBxL1geiasApUvN'
        b'qAyPJfx4PSylpygDlUstIRmwfioXGaMC2ykCpwysRPVf7mbCXdDoG7C/LyWTqcvxT7LkSgQvh7IFs2dRfMlGuB5jZKxQNnAH3EHjc8CFCSR2SDhwFgkwApvSLOLXTAFG'
        b'4+FBB5EpT0jmRxhUiIlS0tZEKRRwBL8sMkwkrIiEuEs4vClGRkgINoJF364WlIkS7o98vhR2ZW+LurnyhKyAQ01IuFB59hehC/szi/5ErhwrGDEc2lKN2b8IG9IxbJ10'
        b's7VOSpk91vkBbU+j1WFr4r/DPKZCghtsjRX7tFvOySSXCSwH9eMc0G71KOKItwrBUR0ZdpDLBI9REi14dgDl0QLL4Qo02mITZhosHR2GrkQPzxYxRfwCgvDzgfULw6aM'
        b'wExahEWrkVXL+jQJdIfRtrrwqOFVOPWqJD7nQw/J0v2fCmpqxn1c6ibZsK/0namuDaMmXOzpHRbQJ7nxsiy513uX3nvnI8+0MeM1DW9MmPXl1u8WRM0vOXysvmJPn+0q'
        b'T16WIWytpG7sG1/PStLu9hwQvKGyutei5n79u8X5p+x4/mFwdN2QFwdUSz9ek59zNe/yP985HQRu3vjxbOGHO1f/1O369YqRazMvvV/8qPZRX03Tc2Uxh09A3q93nQf/'
        b'bWCesrOsE1EMCVov1Fjoqa0yMWkdfwE2EZULj4ADxSYWLfzULRtKSLRWwJUkv15OKvIL1ob7ykwkWWy34GyiEMYsBpcIQRYo927lyGJhC9zVlUL8YQXSuZiCCx6d2crC'
        b'hfHvp5HOwHUEI6uhEtNoxYEjZiYtzKN1AOk9YuycgGcIwH91DKzn2LTYUGQukq0po4daUmkxnZLh4Uh+zvgwok5KpGAnEj0bHjGxabG9kdf/IjlzyhzQ0sqkxXRCmryZ'
        b'UGmBWkrE5Q/2BSFN9ALawNFpsX6gFFymimwVGj+SzDRvLikxmE0Lvgz2UQxWWchIwvh7EJ4wUWqx/sFwC72mMvgi6o9kMIoYaR6Ohsynx+5DVspxJFqdh5lViw2HNc5/'
        b'CaUWIYEieiy0rR5bxkT0ap9VCyuEVlYt7WKmfWRWkdVpAwWmxLelNp/P7fBomU6FdIM1RIOitVjylSzzskVoFTOMJUyrA/GG5xmSNluvzNNRnJUNW5bnn/JyO3BPLqGi'
        b'J1bLWQyhxxJKCJ2V0JKu6rGv7FnpscR4LHksQHVJF3sNFfGIEe8Bjhp0ZtPMaRHYxLgHsHCzGp6X8ZLV56YUO+kCkN071uWbhOrzFKD84aJbvSvv/bJK9+kw1+6dRo2+'
        b'M+X36IQG709dN1a4GKsGxKa8fbRp+dnrv3458su+vw8zFPv5OxkWjah+2GnuxivvRH64LGbOWxcC9nTRR3xi2LwuMsLlj3rl/qFDvzs4bXT0y++7zf1gzbd3PY4l5tYc'
        b'OKF3WZ89JvD7lb3nfb8pO7n49S5+LV9dWC2RL3rw/HerFXtF/3N9wbArTc2/zvBfEnR92ADXpNfG3OofnXwicavUZ6vHugvHUjf1eD3tYVDeiNNB2RnvLDheBIc+LLqp'
        b'mNGzc4Hq9OTp5S07fa4t+DZu08fs7Yg7c9/856YHy3TvBF28Vd2YGHT/H3dudCnJq49ZFFx/VnLmnrdz4A5BV83rp7oHDLyzffm5jMQ5qsjdJ2V8kigErs0VwLXImuPF'
        b'MXA50hhKEdF+Hhmg3PSGB54E5yxe8cCWAcSkAafgTrCu9Z0N98YmS829sxHNbPvKpet/pzM+dYFUDt/0MNotCIxUlJGhKZArMjKIysFeARPAsixvAK/HYxYpFyHPixUF'
        b'SL0DQr1HevdleUOwEhom4nu4BS9jFrE87Yfmp5BvZDMyLN7ZBPw/aAOe9l/mhxhLSjiBSfbYO6MsKbukaI0AjQ/NYC1Yjyzf1SkTka+53pnx6IIc4iP87jFgv3qiWz5P'
        b'tx7t6XyU7b4ac3R6Oz3++b5k1DjNmlFZg72mN0653l15NYHxLfl99sqdXnPeXhe8cP/E3u4DHsxeUvxFWc7ua7fWyP5zwjNDHRR+7bpP//S9b9bFNwWtOpKnS5u2f0LY'
        b'nI9uG66vkrNldfs85e/uKy+HvkO/XfiKZ99d7736+fIwNr/587Kcm0F7gXf8sh/X3vqRLyoMeZi4FtkQJDHXBnYYHodTUrALleTMuIGTbDJ4CR6CTUnE9AarYC24kJQS'
        b'AS4CtBLvigdsT9jCR9f+IqBuArgM60bSdiA5HKtIO3gN6s3vAdeNJEPvGFgPtieNnxQKLoMTk5wZoYAVoSdlBzFI4LYlqIq1/YUMKHXjpTGwHh4eSZ/E43CTX9gEJ6Z/'
        b'MC+JQUbEqr7ExAnMG0Lo3nCKmnXIwJCxcIMT3IAciotkMM+YH6Wz2O46ngWnvUEj2J1JNhtgvW8S0ZTUKULDcgZcz08ONOjxa5KE/gGmCQFwppAH9gbBDRTHvhk0CAhx'
        b'6zjOthJ3ZpGT1ARPI9fuImlUHyfCg70mvJDbxRWcYkHVEixADallqO+EtIlol5NisGrxQgM8tVC80MBj/JAEYN3wGZSnvrwv3JpEUhvg62DQrdnBBoL9cL8cNOhxfjth'
        b'9GLc5P2TkIbBZAfr8RK6d5ucma59BGDFXNhklaC4+//9w2X7rLk8Qd/YUT+tmAhCH+ououl8SHp97J6J+SNsDaA+1HQgGifQyNco840CHIxrdNIbCjVKo0Cj1umNAuwR'
        b'GQUFhWgzX6fXGp0IJ7pRkFVQoDHy1fl6o5MKKT70pcVz95iUo9CgN/Kzc7VGfoFWYRSq1Bq9Ei3kyQuN/BJ1odFJrstWq438XGUR2gVV76rWmaCfRmGhIUujzjY6U1Ss'
        b'zuimy1Wr9BlKrbZAa3QvlGt1ygy1rgCHFxrdDfnZuXJ1vlKRoSzKNrpkZOiUSPqMDKOQhuNZ5JJn6d3+Ef/+Hhd3cfEZLj7FxZe4+AQXd3CBZ3603+LiNi5u4eI+Lq7j'
        b'4mNcfI2Le7i4gQtMsab9Ny6+w8UXuPgBFzdx8REujLh4gIufcPGN1e1zNavUX+ItVCrZ9kikwjG32bn9jJKMDO43N+A8CuCWpYXy7AXyHCWHLZYrlIpkmYiYiZhlVa7R'
        b'cCyrxJA0uqIW1+p1mJHaKNQUZMs1OqN4Cg7/y1Mm4NbW/mxqN5sAeqNoWF6BwqBRYvw5dbEFzkhz2XaxQd4EDP+/ghpKfQ=='
    ))))
