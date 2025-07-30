
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
        b'eJzsvQdYW9fZOH7v1UBsjBfecrwQILGX8cQLEMsGj+ABAkmgWEhYA9t4G2zAgBfghRfxxMZ77+ScJE3a9GvaNP0akjazSZzxtVlNmrbJ/z3nSkKyJOLk1+95fv/n+Rlz'
        b'uWev97zrvO+57zGP/BPA7zT4NU+Ch5opYsqZIlbNqrk6pojTCI4K1YJO1jRWLdSIaplqxqxYzGnEalEtu5nV+Gi4WpZl1OICxrdc5vPdOr+Z0wtnLZBWGtVWvUZq1Eot'
        b'FRpp/mpLhdEgna0zWDRlFdIqVdlyVblG4edXWKEz2/OqNVqdQWOWaq2GMovOaDBLVQa1tEyvMps1Zj+LUVpm0qgsGinfgFplUUk1q8oqVIZyjVSr02vMCr+y4U7DGgW/'
        b'I+DXnwytCh71TD1bz9UL6oX1onpxvU+9pN633q/evz6gPrA+qD64PqS+X31off/6AfUD6wfVD64Pqx9SP7R+WP1w7Qg6HZJ1IxqYWmbdyJrQtSNqmYXM2pG1DMusH7F+'
        b'ZIHTewxMIp0OQW6Z8zxz8DsUfvuTDgnpXBcwMv9cvQTepWMEjLAiVswwJQF7VbGMdQxETh6KtuIm3JiXPRc34JY8GW7JnCyZny8XMxNmCfGDhahLxlrJINHpoXirOTMH'
        b'b0d3Zbg5BzezjF8mhy6i/bhexlkHQh5RfIkSXQrMjMoUMUIhi45A5iZaWowv4WNKSJDjRigsYoL64Qt4myAX7cI3oDSZVrwzyBc14W1RVbjOHzrVDLX4oSscuhowgXYW'
        b'bcTHGMhxOQA1rFxhxVdWBKywsiZ8nxmMdwhQ8xjUCp2VEoAbsBA1oR3RSnkE3o6b8Q4S8okqY4aNFaLaJaFl7CPQOcw+a3qyjPwiMj9tGbXDbEvINgAUr+NgCVm6hBxd'
        b'NnY9V+D0blvCikeXkHRmkNsSjuKXcPocHyaAYUJikp71/3h9KkMjW4UcQzLGLHh7QFpwCR+ZHiBhQiAuZtDINQPXruQjP1EKGfgrjRHXRrSULWW6GL0fRL8xLEz4FTd6'
        b'NMO8M+EL7nrstfQyRu8LCV9l7WcvDj4ZyEwriXvT9Fy6ho/+ReoXwW0b7o3i8t9mvw/7Q8RfmR7GqiDrcw8fg58m3BQ9Nzwcb4vOkONtqKswPCsH74hSZMqzcljGEDxq'
        b'se/kqXif2xr424edza+B6zZiyApo/R1zzD32HGs9bROx2xwH5JpILygg4/OoTl0wD3Wz8gUcwwkYfGhpsbUfpGQtTyyIQvegijHMGNyN71lJLfh6AD5WiW8VzIOECmYW'
        b'6vSnuZWRI3Arur4MKo5moqPRJRqLbqgqcWsc3gMzIGfkskTaZu5YeUEO3o875uIWEcOtYYfrcbd1AqRMRTfzyX6IVAIoN2bPDUddURmwR9FhtEvMKHCXCG1GVyZYYcGZ'
        b'Jahbga7E62B8k5hJE+J0FTEtQnMH6aMxcemvY4NQTMAW1Rs5PXVdBcHPDgnbv+hJ1fRBpZXzr1tGz/v65iycWZMwb+fOX77/zpoHzU1/9lN88erXV9+cfOjD1oCEqpIT'
        b'adbFmpvT0p5a3rbpnWMWn/Zn+i/vHJ85I/LG69F/2/Te7fijZ9XDHuxZflaz+7WtVx68rdr7fHF0+JR/H5zatODhqXWdQR0nKsK/qH2j6N/qt0NHvfTWnz/elfJlS75M'
        b'ZCFIYgw6gC4qcUskbsmRZxEkEho+F98U4Hpf1G0hiA1dRxdrItNTsuS4ITM7V8T4o0scPoT3yS0Eg6DL+NSwSIUsK5JiGVwfKWKC8UaBsQTtpC3U4I5sfzJ7VkAM26I5'
        b'ph/ahC/j2wJ0zpjEt7BThdpgsrepYSl24GbAmaksujQQd8u4Hi5cZiLwIvOnf37Gg4Ded4MmaU3GGo0BiAolVwogNZrqKT2BJo1BrTEVmzRlRpOaZDUTZMZMkbAhrIT1'
        b'g59B8BsEP+RvKPwN4UJZk9hes0zQI+YL9/gUF5ushuLiHv/i4jK9RmWwVhUX/+x+y1iTD3kXkQdpbirpHKWFWMqJWY4V0yf3L46Dzccy35OQ9QmSfg3vxmcjs3CLMlOu'
        b'nY62RQM22B6dxTLj0CVRsQrtddmb5J/Q9tdcAQ8NYRWATVCzRQL4FeqYIhH8Fau5Ih91UD2jZdVCtajOt0hC38VqnzpJkS99l6h94d2Pp8pagdpP7Q9hfwgDaoFwgDoQ'
        b'wgFqliKJ4B7xPDp3uXQuH34Pu7NM4NQtMngfO9ognIyjYh4nCRoEgJOEgJMEFCcJKR4SrBcWOL17w/ucDQm64iQhj/f3ZwHiXvu+GBBxwA/auYwu/OUIzpwHKaNefHLw'
        b'kk9KXi79qGS3ukH1cUlzebfmIwgXPbMEX9wZu2Xuwc49/Z7LU51W6UVn2DMlvxTuihoRMEsxotl/UdrGj8OGzAvbPCTlVabqFyHrRINlYstIqHU8akRNkYR4NqKrPAGN'
        b'FDPB6KSgZgNuoDsJb0Y3YKcqcS1ushNZARMQJfAJRAcsg8lOOrU+Nv4pJW7KBp5CJmYkaBu3KmqwhVA3aeI6gtCUmegcg3YsZ8Qp3JCKQssQUnFrOtqKmvKAVxCK0SZG'
        b'hA+y+DY+O5qmojq0eRCLTkfKMyiXIcFXOVRXjE/IOCdoFXjadhR4eyTFxTqDzlJcTLdXAJn6ohCW/IhZIVsTzIOAwp6L31aiHqFZo9f2CAlP2ONTrTGZgX00kaUxEYrY'
        b'xdrbDSJRgeQR7NgvpJHFjv1yKsTrfnFrvYx7ZFc4wG+iDfy0nA34OEoQBQB8HAU+AQU4br2gwOndG0FkvACfVQ7viwAftvjjFliw7cBI3QLqjncUZPDrOjd/HqGQU3Gn'
        b'GBg6tEmXPW8Ua46BYl98v/KTEgKJ4WVRoZGqbNWnJSFlFVp9qXBbrLzkf0oWvRj28jP7638fxBxdItlQ/bpMSOEKoOoC6uKhBnWiQw7IQcfxSYsUcuhwHbCOVwDD71g0'
        b'Ge9QyKtsuHzoeiHaEiGkaHweuo93oiZf1EgByQZF6CLebaH0+tRo9EA5clSenGW4anb6QryDX2nOI9AADi3XWHQWTaUNbggKZEr92AC2JtSxZo4sfFVCCgc9QoOqUtML'
        b'KqYQvplQB6BQGCFsQZkDRo4EeYcRD+39r2GpuscGlAh4H44algGcoIPoMIUVb3CSVq3ze/YZgTkOyhyfd8wzlHxa0h3KbYuzxvwx5niMML7qJMucD5aUbTghE1jCoGBy'
        b'AGoFKAlFHc7oRT+HgsiTETU8gFDwGIrqnCEEtQ2kNaDLGnRmPu604RobiCxLslFS7ygEoMHsDg3lj0CD2RUaRPxik2XvEVWr9FY3mBA4wcQAB2CQma5wAMaBPpCHh6a9'
        b'448pPGAQFpvVCn8GDnEDDdbWhCtoiHKt0WSuj8rxLSL+FeIGuVwxNyNrPm7IK+AZ2QzgaRUsY8H3fHHrKvFCdNoqI3v09IQCO9pxByXxQh6YAlCd7s79SZw5F4p0mv/5'
        b'ScnHAE96bcSgCFWGSk8hqUrV0H5Gc1r1Ucl/lUZROMtSnVGFlDEvDdrGzto/+KIlJkqtVmeoJHtitG9nC5ikocFHN71s40pnbmApy4hvoZ0OtpGyjEPRQUqUVk5GHQ46'
        b'B0DXwAOjz1rLWDKO/WgnPuMEj3ZgXIjuEnjEW/A5nvLdXSN1AsZQ/IAQvvNoLwXXuWEzbEQPqnpgI3xL8VWZjfYIvfKbPNSKrVWEzewle3o/4CkllJ+sCbTBDp/HGX/x'
        b'FM0Bqm77AlBZL82jEEtkmUoHxLaHeodY11bd5EFXLEYlcgcWYxvYny//CT2CqiBX18xKOXMWRFTlTFKqMso/LfmoXVfyy9IK7QDVadGlsMExcjUBpkbVGU23hntJXnJe'
        b'teTFRb9aggtxPtbj/PDXnl0k+H0/IGxBjPiF4KqbOUDWKN/SkY9u8zAyaIwDXY1HDZRVSlMsQE0gwTkjInxiMF9yGyTtJrsgPyoTt8jFjHgZNwY3ruZh5ozZRNKG25gp'
        b'ykmhc6jRMzz0hdZAYjBbTDaURvQCjCUEZIwAgJCaoF7cQrLQUl0CftG9wwawRb1gQdg+qwMsWvpAZI80JuNyTUQ1IAskzBuhpiDV+BUX80o9eA8oLl5hVen5FB7DSsoA'
        b'oMqNptU9EhuzZqYMWY9Yq9Po1WbKk1GiSxEshVnaQzuy7lOA4wdEpqiADIggawknZG0/XJAkQBQgCpFYSYXVIHIqnvS3yzySAK4EbR/mXeQhehQXkYcrEqoFRMQ5yBWJ'
        b'2hi1+CiIOJ1sLQvij4RCt2+PeJYBMP7q7wbM1JTqLEYQI6OVJo2af33IcxwPSRPfhS7QmGqs5eYqldVcVqHSa6TxkETG811AtsZSY9FIZ5t0ZksXR+f84Qsw3q/3w5wq'
        b'jQaLMS0X5lgaPl1t0pjNMMMGy+oq6XyQYU0GTUWlxiBLcwqYyzXl8LSoDGqP5QwqC75r0iuk+bBCRii7wGgyPE4+T5Ut1+gMGul0Q7mqVCNLc0lLU1pNNaWaGo2urMJg'
        b'NZSnzZovzyadgr/zCyzyTBD4FGnTDTBhmrRCIJz66OnLVWqFdI5JpYaqNHozIad62q7BXG00Qc019jZMlrQCi0mFj2jS8o1mi1ZVVkFf9BqdpUZVoU/Lgxy0OZh5M/yt'
        b'sToVtwdKV5LeEelfausIRCmkRVYzNKx36rw01mtKXJpSYzDUKKRKownqrjJCbYYaFW1HY2tPI52D7+otunJptdHgFleqM6cVavQaLaSla4BrXU7qDbdFyexp0jkagB18'
        b'XGsxk1GSKXXPLZ2TLUubJc9R6fTOqXyMLC2ThxOLc5o9TpY2W7XKOQGCsrQC2MPQSY1zgj1OlpauMiy3TznMEQm6zhqJWU5gWJ5rrYQKICobHyfqluVk1vjph8jM9Om5'
        b'JE2jMWkBU8BrwcLM2YXyGUZYG9vk072gM1QArJF6bNOeobJWWeSkHUA5pQpbm7Z3l3n3FE/m3mUQcW6DiHMfRJynQcTxg4jrHUSc8yDiPAwiztsg4pw6G+dlEHHeBxHv'
        b'Noh490HEexpEPD+I+N5BxDsPIt7DIOK9DSLeqbPxXgYR730QCW6DSHAfRIKnQSTwg0joHUSC8yASPAwiwdsgEpw6m+BlEAneB5HoNohE90EkehpEIj+IxN5BJDoPItHD'
        b'IBK9DSLRqbOJXgaR6DKI3o0I+8mk02hVPH6cY7LiI1qjqRIQs9JKUJ2BjgGwsQZkK3ugygQIGbCfwVxl0pRVVAG+NkA84GKLSWMhOSC9VKMylcJEQXCmjvALGjlP7qZb'
        b'zYSg1ADPkLYQH68wwbyZzbQBgvV4GqvXVeos0nAb6ZWlFcF0k3ylkGgoJ/lm4+N6va4caJRFqjNIC1VAF50KFNA1ICn5VC3sXFkvGZcXQS8AYYST4i4JtvKQNM69QJz3'
        b'AnEeC8RL001WCyS7l6PpCd4rTPBYYaL3Aom0QI6Kp8t0zoEvAf6Exlk0qyyOF8BEjtd456xmRzZ+IdI1QI7LnSLGpRXpDLAaZP1pOySpBqII6QUs7RKMcw0C+lGZLUDt'
        b'TDqthUCNVlUB/YdMBrUKOmMoBbB1rLjFhI+XAxBlGtS6aoV0Nk8/nENxLqF4l1CCSyjRJZTkEkp2CaW4hFJdW49xDbr2Jta1O7Gu/Yl17VBsogc2RRo+zzarZhujIetl'
        b'jDwl2nglT0l29slbmgOVeUjP89wa4bs8xbuwYt7H0Ee6N+7sp2SO896yC5/2ONkAVXrK5kICktxIQJI7CUjyRAKSeBKQ1IuNk5xJQJIHEpDkjQQkOaH6JC8kIMk7HUt2'
        b'G0Sy+yCSPQ0imR9Ecu8gkp0HkexhEMneBpHs1NlkL4NI9j6IFLdBpLgPIsXTIFL4QaT0DiLFeRApHgaR4m0QKU6dTfEyiBTvg0h1G0Sq+yBSPQ0ilR9Eau8gUp0Hkeph'
        b'EKneBpHq1NlUL4NI9T4IQJBuskKMB2EhxqO0EGMTF2Kc2JQYF4EhxpPEEONVZIhxlg1ivAkNMS7jsXVxtklTqTavBixTCXjbbNRXAyeRVjArf7qcUiuL2aTRAhE0EJrn'
        b'MTrOc3S85+gEz9GJnqOTPEcne45O8Ryd6mU4MQShLzfgu1Vai8YszcvPK7AxcISYm6s0IA/zzGQvMXeKtZNvp6g5mlJ8l1D6R9iGcj7exjXYQ3Euofi0fJtyxamwm9ol'
        b'1j0qzj0KxBw9EYpVFsKXSgusUJ2qUgNkVGWxmglby49GWqkyWIG8SMs1PJgCOfSkBpA5FdER4q5T02I/mtlD/R6Ikue63TNSFVPv7EiB+ZbaWF46lVqSbptk/j3O6Z3I'
        b'hL2aqu/YtNwuiYkoQ03k5M9ETLn4oxSiaTQRFX6PyFyl11lMIx0avBBXXR6x5FvnossTcCz3b7GI47jvuXju11ZqG3ID3w6Q4h1mYqLSGIW6hIwkiVuPDhr+w/o8v+ll'
        b'ZUarwQLyQ09QOiw6L3eoqjT6hwN5bR5Rjn83dCaAQSXwFkRdKuUlHwBiHaAeyEJ0sj1CwgOZxsPr13chYn4lz9IYKwwaaYFRr4/OAJxkkCtriIalN9iL5dIWKoukfDGi'
        b'SSP406wzW/kIkuYc5nfdHKL44zl8vqH0+fKCsgo9vgurrweuxDmYlq7Ra8rVZCD8q03t0vseZ5OQ0uwzQTl+whJqbJvbLrZJebbIJvz1qqlsYh9l1onAB5lhe1moYGCr'
        b'gTan10EG+qYzaI1SuXS6yWLvii0m00BKPhJJssV5yhbnli3eU7Z4t2wJnrIluGVL9JQt0S1bkqdsSW7Zkj1lS3bLluIpG3AZeQWFsRCh5BeGcLsaGhnnFgkBaY4GMKZd'
        b'Fyu1KqS9uliI5GHZrhxVSAnHbpe7eaVr7zJKsyOz02ZbDcupTa/GVA4oqoagFRKfPl+akMoTWq09C1EKe4q3wQ2f5KHCtCIqEJCBmypVJNEBIp5SHKDirVhcX8U8J/Ig'
        b'1Ecxz4k8SPVRzHMiD2J9FPOcyINcH8U8J/Ig2Ecxz4k8SPZRzHMiKZbaVzHPiXS5Y/pcb8+ptGDfgOIdUmL7BBUvqbRgn8DiJZUW7BNcvKTSgn0CjJdUWrBPkPGSSgv2'
        b'CTReUmnBPsHGSyot2CfgeEmlO75PyIHUAgu+W7YcSNdKIL4Wypqu1OjMmrTZQOJ7sR+gQ5VBryLaRfNTqgoT1FqugRwGDWGLetWNNspJEN50q5YoxhxIzk5LIYlg3l6C'
        b'LA2fbqjhWWJyogfIOEdnAdKoUQMHorI8kvwIHnYv3IvJH00z6fF1s41NcEnJoOc7WgtwJQ7BilISOeV3PEoBtpHaqDmQfqA0hInWUva5khB4i0YH02JxaIozgde16LS6'
        b'5Spn7F9EBUGHBtmZzeDFR6eTRGc2abaGly00ulKSlA2rRo7GzDxn451Rc9YOQ7+hZZXeWrlcU2FXZVMiSLk4YhWTa4rwxsRGweOuVyZ2GPcX6omxQIBOm7Nz8fZoysUW'
        b'BeFmpQ8zsFQYgFry3PjYADsf+xTryse2idv82/zVXFv/tv48P9vio46qF9UH1vfXCtT+6oA6X+BphRqROlAdVMeog9UhLVyRGML9aDiUhn0g3J+GB9CwBMIDaXgQDftC'
        b'eDANh9GwH4SH0PBQGvaH8DAaHk7DAaQHWk49Qj2yTlIUSHvZ/5EfX/WoFj+1vJ6z9VaolqpH094G8aNq82tjtWRkPvRpL/VEi69aQa3pRNQTJATK+qjHqMfSssHqaEgT'
        b'1Uuon0goTRunHl/nWxQCsf2gTxPU4dCnftBGf7Wsxe7fEFQfrBWpI9SRdRKoJdQmA8T0SGYSo/AZBQu+i/aTOv2zR0t5BMK7L7nk6BKZiOG1iRgfPaS24cQE6yG10yCC'
        b'gCzgITG1eUitnImhTW92U7I9uymFPGJJFmLo8JBaAxBokPn0+KnU1YCTTMU6dY9vGWAGg4W8Bql4qaVYD6ydpaJHUmaFTWMoW90jIeasOpXeZoThr9UBN1dcCRu2grbd'
        b'I5g1fx5v5WFKhUeZxAkE/Wy/1FqHGOe4eFn51ovr/ep9tH42wyBJg6SWWedbE7pWQg2DfKkxkGS9b4HTewyjFlAbNuHXrTABLrNH/mXy3dXVaMzUu8wx5zpqz1CmUbgV'
        b'cYuYCEKHqlLaO1UTbX5lgFiIFsjmuGabM5XB4lYD+ReeDvjAYsdGMoV0OikPmKNMSo0IpdYqKeDPZKlaV66zmN37ZeuGY5U894JP9twDx1nHj/Qh8cf64AoeE6XZ9C/p'
        b'wpzobHuqrWNmz30h1IbgeaASCmlhBWB+2AUaqdlaqteoy2E8j1ULb0jCi6hQk1QFVUCY779UbwQqZFJIMy3SSisIKqUaj7WobIMv1VhWashZrzRcrdGqrHqLjLoVpnhf'
        b'C9u2mCidYXuTlhFlYbjjiNFJySjzVot9S020Q6vZsZjEi9FokobzBivL8V1TDYjd3iqyGUhNpDIW4UegGh5GbBgmXFOukCbGxkRJk2NjvFbjtKcnSmeTgJQGSHVanQF2'
        b'DfRRulqjgo5FGDQryXlndZIiQREbIXOfqsewOg7gfSMG+IQwUoZJian+Jkw6Xs9Y0yAyJFGMm3JQd+KifNyQiVuU0bgxn1icZmTLcFNUrhxtwzuy52agcxm5OTmZOSyD'
        b'd6GjAcZ++Gla6bzCACaMYcJjBpUvEKxWM9bJVP2THkNrdamzchnUirfjxmygp6jx0WrrVgcwqBZdpdUeHmzzypv9L/8pY7IYK0HHqAFtWhBidXbwylDII4jDDDovZJKW'
        b'iM1T8C7qm0Yr+X6izQlQe4edNCKX79uwfniTe9/yCnAD1NgURXrXLFvg6Nhk3M4y6JbJH11GN0y67ShAYK6BavadujPi5Td8N8YEbHnn5I2rt7e23szv2CyQzHvuV00N'
        b'/cMzXnglZ/JWNPpv/y68XGWsuzh27u5Xtiys+HqN+Y+l0RMzo37fVTTfp7Jz2WuTv08M5/yWcZO6DaPenjtZX/DOhKdwT8yBuqmGhCc73tq9Sn/4hzu/O9f0MHvk1KMy'
        b'2c3N38oCqN0+3jqyZFUZaur13BQwweME2mnh1LAb7caXcQdqynNexvnRLDMU1wpr5kp415Rr6HCkP0ylLMdurzsQ1fuFCyVT0V3LaMgRnToD6nBZNJYZNBrVQi3++Ba+'
        b'RJ1U0KYZ/nhHaaQ8PEPOMWJ0gJOvRLUW6tTUhq6hp6EOslDoJtprW6xQdF6Am9BO3MY7k91HJ0ZCvvZIhQxvA/5MjLq5eHQH3aQdza40oybiZEZXaPoGskZiJrRagO7F'
        b'LLCEQ45ZC1EzOoN2kxHbWDbSW9sKAyThLWIF2pRhIYCEW9AptIcMrCkqQgH1dpC8uAXviCR5pWZRILqh5udxH9qGNpGsVJM5VQwzIYem0V4B3lKJTtJBoi0WfMipZeJT'
        b'pxzu48MMRTeFqAlieWtJv5/pB9frHUNNTgn/wWxg1opZMXV3E9uc3oLgSVzeJBxJEbM1/ezk2OEnk2vvCDU3Jb5ppmnkMZ080sljBmN3yZnJ9G3PLOFL9VaS7ihFK/Hg'
        b'3POQdJ/olpmNzP6R3g1b3TvuYvPM2n6pUSnp4VrmKd5XjM2VsT3+xb28hCnMMYlOrk2T9KrKUrVqSj+o5UtSo1OL9rTvbLjdVpedDwgHmqGWGw361bIutkegNpY9VtfK'
        b'+a75FTv4C089M2UQPA3lTZnw8t0ovgd8EQ8deKyW6/iWg4tduQqvzQ92NC/rk+/4yR2xrY5vsZ2se+3CUEcXhqSrzBoHH/CTmyy3N+lgq701OcLR5BivXMLPa1xSbPeC'
        b'89a2tLdtr5zFz5vrgGJnAcJb+2N6V/xH2BEvvXDxQaAOd1w943C4+z/yQLBX7+aBYNy3XUidflUvr+Ydoyq0nzK/bf5187sBzwYc1DFTOoV++15PTZdxlJLhK6hdyuNx'
        b'dGMKoHJnRI47UTfNhQ4wQEWaCoa54nI7Jl88oS/nN59isrecXZ02wM+EmhAnbEYz8GUGP1pTmGNVnoTHeNbu1bwRft7sw9HNrX6ZX4+PbbfyVv5is8Wk0Vh6JFVGs4Ww'
        b'0D3CMp1ldY8Pn2d1j7haRSVT/zJg5I2VvMQqsKjKe0RG2AOmMn+n9SCIPci+JvPIcvs7JM1Ax1UEQfxlENogGxj4NwQAGAQAGPhTMAigS++/PqDA6d1J3vyTyIO8OV2t'
        b'NoNAQbhitaaU7Er4X2Yzl5NqqHH/Y4icVCCi0oxKWmEt1zgJeTBDZh0ISVLe/4HIa2aNRSHNA6h3q4egh0pyRqOrrDKaiGxqL1amMoDAQ4qCsGTSlFn0q6Wlq0kBt0pU'
        b'1SqdXkWapPIBMbY0K8hIdUTbBnvPVqVNxiJ1utUBVVvNOkM57ZGjGmkEXbyIx5iR2bbRVhBFiXvf3fKHW1SmcmhDbcdTpLyU6A/NRF4xr7CS2S01qcqWayxm2cTHVwPw'
        b'cDtROt2F3EgX0xPTpd6KkZYnSqnDw+IfdXvwWgu/TSZKC+hf6WKbEZ7X/PbtNFFKtJ+wVFQ8XexshOe1LNmAINjCU7o4z2Txno/fopCVf6FtREkzC/Lk8bFJSdLFROPp'
        b'tTS/r0FknV4oz5wpXWw7RlwaudjZqcN7473ogAjhfEBKKnI2JfZaHBAITGYFbA3YruYyk67KYqNuBE6JjzjdW9P1ZiPAr0btUX8A4ERyE1qkp7cL0cVWSGfySgS6RZ8o'
        b'sKgqK4lznOEJr+oEuhkAsKADVbatpdbR+41UMK0rdUDzNKtgxW0bzr0e8i/XaNHw24Rufo2lwqgGTFJurQRAg76olsMGhE2jgdkp00iNQPw91sMPiWwaqh0x88PUmZ26'
        b'pJDOBqRmR0gea3HedkSXAqBObm8q08OA+YubzBrPJUtsdzcZy2jP+QOWSRUWS5V5YnT0ypUr+bs2FGpNtNqg16wyVkbzfGi0qqoqWgeLv0pRYanUj4m2VxEdGxMTHxcX'
        b'Gz0zNiUmNiEhJiElPiE2JjE5PnVKSfGPaC4IRXT3NAzNtRJpQZKG7pizZVlynUaRS3z7IlEXyIhjC0QVZnTFSkgciIbH8eV4eIuVRDOxuHstVQEcmCZiEoJCGGZaSfYn'
        b'Q9cwVqK21c9C25V2+j4XN5BbVLLk8/LnydNGLJgXTtxPF+IG8gcIP4iUF3xxO2pdxVu2NM5FT+MrxME/cgg6jxt9GBHezwWIpPQOD9TxRB6+oiBXeBCH3MhBIfCnJQek'
        b'4lHohBDf1g6xTmPITQEnUAe+ApJ3zny8s4oMrXdg+bghF0o1K+dXwSMvOwsfwm24XcjgbWizPwzzdpmVGPFEzkBH/RXB/WVZ6C464sf4ZnH4CGpHJ2iqCnXH4yuZUIMY'
        b'7WEZAdrLoo0gft/jL4hqTPTzxw3RCtwIrUbhU4NQVxbMYQPLSOeIhOgMvmslhyPoXCK6ia9ER7AMl8GWxSWhS/PpxF7p58OEDRgOzGtJVJBfKMPfS3UEb8ON5kDcjq9B'
        b'yyATH1KyjGQJN8fC8FecHELX8VWSITBQgXfha2V52fhSJN4tYAavFqDugilWyoXdAmn/oL+C1NGSk0kmBu1C7QJmIL4lDA7Ejbozy38vonf1XONmyf9L6YemhQhf+fil'
        b'9+P/8VHuS/9Ve/MLv2Wd03/bIryiTApKP5Ie+rejf9j41btzZ/x2sjhS/mbIn5p9IyYPGLO19nbb9otvPtX6okqZ8MZ7/1P/6qtdya+P/qUy+48vv/7V1aMiuW5G5IHf'
        b'TossevXqrc4//e1Sbudnb3z9sHrvn6/O/9eXW2+tW2tNO/XG6+9OuFViVU5RDXxn6m8kK1f996is65FLB3bJxPw9Dc14K259VFEzdKhAK0KnLOPocMdPU3rQWgxAR2CV'
        b'40V4RzQ+Qq8b8cNb0GlnhU0Y2kd1NkIJvim0EOMsdA3fFjn0Fb1MbrwW2Nw7MpoH1+PTqC0yV56ZmaOMwi0ydGIVywzCd4VxaD+uo17UsinLlFHoSGl4BnQGFhGd5Vaj'
        b'3fiQy/UhQT/3dh+vvrV+KrW6mOfjKBs93s5GZwSwAayEHUSfzj9CeieJhK3p72CDe+uw6TsCeWVEEWM3eCO3jJiWkMdS8lhGHsXkUUIeKvIoZVzUH569hP35OnsrKXE0'
        b'UepoItDRosrRDmXz1aQKFzb/9fHe2XxP45P59gSoiT2gjW3qCeSZYXtQrKqkf8l9LJoeX9sZcJmmx5+wLsAwEgsxvkeOQZf5OeFlorUJsePlBYTX93Ph9oOA3w+2cfwh'
        b'hOPXhtj4fT/K7/sDv+9H+X1/yuP7rfcvcHp34vd3+PTN76scln5S/uamx+BqZxEvCT63FEgrzBswrMAuqJxvLiQsRZS03GS0VkEqcNIqd1JlrCzVGVR25iUC+JoISnV5'
        b'okuUBA6zUNJBh9zsVhORo/+fgPL/ZwHFebtNJAvFxzjUYz8iqLjsT748H2WvwCO3tvhHLEW9Nsfvf74d25a3xfEMr8FI1D0mytIaPDOqK42Eo9RVqvReWOLFfdjKgqDh'
        b'2VrWa48JpuL7W2o0Lif9JTEKaY4NulQ0LDWWPgULD+K/5zNHAxGQUpJiYm0aNAIIIN2R6hb32tF67YQDUU6UzjdbVXo93RkAONVGXZljNy52MsPtU0a0IVrXZaAeeoud'
        b'TXV/VIojxR+R5FwMQv8vEMTSNSs15TZznv8njP1fIIzFJ8XEpaTExMcnxCfGJyUlxnoUxsi/viU0kUcJTcqfLa8eL6IXpu7UrtF3rS9jrEQSQy3mFGVmDt4WlemQtsiV'
        b'RA4RC90OtElZG9A934TV6JqVsJ6VlarJU2wylkPAQrUjqPA2dxnuRg8GKBVZOcDfeqnYLrs14SZfdAoa2m0lh1P4HN6Sbs7LwSdUefZr2qCFhXgnFNmBG0Di8gPRBKqE'
        b'8K2CJeggOoCO+TLoLN7jn4tP4TtWyj7fleGb5izckpmQlpOnJDctxQiZsHQBMPdX8EkqwuCjuNXPHJGDT6LLeHs4YegVmehcOMuMKheJfPBFevsurs9E1/3xDbR9ngS3'
        b'yFFnfm4U6uKY0HgB6hyNO+mxNz6bia9Cxb2H3plR6N6YTHRtHrl9OBY1iVYJJlBBuTK0P+1XTl4mvm+MkpH7UQfgYwJ8B19HJ+lKjV/NX4J7Ma9SP2p0KUNvZR2DzlT7'
        b'owbcKmaYQqYQxMRWaxJpege6h7v8yTzBlO7CNzJAGm3BrfgakVCb0kegsxDOxttBSBAwS4ZI5sBUneOvbu3GR4z4ij/hcTOZzNQ59NLVIeieJJ56l8SCkH6+lGattASB'
        b'gLR3En/3qxGf0n/7ww8/xGbxd/AelZVlr52Twx/pp0rF9Eg/f/TKqHGCLMY6mzS1D9/EN8jktKAWvMkm1WdELSAXNUdnzQeoyMDNBeEygI0Mci8zvZRZhq7T+RMbApfi'
        b'M/iAlejjheLKAtwenyVgWNzN4Af4OkDbhUwruQUM3UP3syHqhD8sFVmneb1wI/EwReg83i1kUP183ydj8S167y+004g7bAJyAr4B0vnccNxeIOGlYbssPHWgOCgIb6KS'
        b'utGMrpuz5Hk50QSGcqkwLGBkeJ8IHUUX0VV0NcdKHHlW4M1jI+nlObgW3cySiRl/9IDDV0bhE/Qu4oGDcrnnxMyqZ8zW/m+EtWWkMtapFAJRHerCV2w6EGr5QaAMN0bn'
        b'5cwN52/jcbKHYIkMfyoA7y7GO2UA6/T+ylp0EB+qRNsiFZlRESwjRju46PGr6V29s/Gu/kpy5n8EH2UZzsSm4H3zZAJabnEgPuCH7ziXAhg8SCEyJRIdJuXw3WK+WEkq'
        b'HWZxJuqwDfNKdu8oAey26260qjjzVJCnpo6/t3Tn5FxBbMiWcr0xqWPD97uj6iLzC46/HZQwvGTm8e66V0JPTPuzOLl2Zr+5Bfqi7dOevzXv86Q/b3sh/q+/PvXhpfar'
        b'Z2sTRQW7Tk78/diqkpSoScdQe/KwMbNbZaL1ZTmTGpfO/t33Y0ZNm3hNrps+XvrP0yN+P/KpbRMXJbcqbm+fOEJcsL7ipOJvdwq+mTdm//gxM5IsHe9N+2basIeDC79/'
        b'kam5efzU+eZSnx7h+UPN3yy5lD3J2DWp4uNbuerL5akv7Rp76o9/2/hV/FvjjRN/aTp/cu6mXdZN3Z9v/9WW7Z0n8w2HFojLv5zx5PR9f6oZM2nCzWMjpr71Urfq7uqr'
        b'7V8PKjS+kf9WzoeVue14ZO4Hvwj84olnP7W+uvdXf9fknjdN/GD97C0rc3b8ibtf+8Ow+V+9di7j/AO9KPrPF4/vW/bewr+/PNaS9/rHwX/PN12Y4icLpIqLWdMnAQK9'
        b'io88amKC9uOtVHGRgY6gjZ40F1RtIUCb8I4CLVVcFOOL+J5dcTEEnXIYmwglRtzFm4CcH0Muh+tOdjLpCV4g0GtF/P1dXdpJkREKvB+38RYivk9y6ARun07vBYtC9ZK8'
        b'6EgFQf1RBJa2c3K0J8hCdVjH0L2RyuyIdHxPzHBL2WR8roC/d/XixHHobHZOFGBEJYsuoDPocgQMjdCgPNWIInwSSITdKES8lpsgRXeovcc4vyhqPIIPJUVFKNxsR/CN'
        b'PHqYmJmhoUYh6GCWh7PEsfg8tTCZAsir1kz2l5yQL5jlSasFTD+8UwDb+wrqphY2YcIYZVS4FjU7aWPS5vRx/ZYs5D+kmvGkpAkiCoheeZwqagoJj7CB/nABNjVNr7KG'
        b'3MjMq2poiCOGKiMhdQArpuYqxHSFv0EtFMJB1JjFj6M3qg12UXv0tmpT7QTw6hUNeWjJo5w8yEWQJh15POVQuXjS6vg8zpXOfnydWkfFGkdNTznaCXQ00avfIVfkF7no'
        b'd05HeNfveBtomciJCyPH7K7Xv4vqfeoZetbK1vtRrYx/vdBx/buoQVzLrBPXhK4VUS2MmGpeROvFBU7v3g7fSWOjmEdZviCe5fvzIMJIPJMvYkqyPxnsxxTS2OHlhGp/'
        b'NEw0rUQ/JGwQQ692w81ot9KMWiQrBJGogREEsSkjUB29sR3dQi1lBailELfMz5mLr+UD3TwINDMwKSaGYUYMBiSC7uAWqnsPNasLMOTcxibG4G0JwHNJVrD4KHqwgCav'
        b'W7G2AHeinbbKWEYUwQL/dg1tohQFHQJsg66ImXR0gtz4jttm03hd/Gh8DJ8AYMLHq8YzYUNQI+VCAWNtMysrIhQxCXGJHCNez6LD6DB+QBMnRayPdLlavaYAH8K3Vbrn'
        b'UzYJzB9AjurgSbPy0nKFsQHX3sv84MozitD0aTN+Nf10RdfDblFgaMO5z54aunf46IcpnM/Rp59+PyXlypX0PUe+XHb4s+diZrCi5VFxyzY/O6A6+Q8tpz8KS6jKr3ld'
        b'Uvj8pYijY5/t2XVYtXLCixZ225s3L2cPeW/eq/MWj9n05oqolNF4yptvrQmafVD4yd3KlPquwwuWHE2/MGr2H1bnLV5zcMPEYB9D7Z3tS/5davrXBx9/u//z/zZuD077'
        b'vmzNuV+PqWjblxeVGa+aXvfLm7/65C+HOuLODjK+8072q59+Nu6ze3/9tvr5dcuafnjiyBfPnA39n84N3wmO/j7/pefaZaEUPQFW3o5O0u8Z+ESMZTj0NDs/cICFMADj'
        b'BqAOHsnmFlI0exkdmslbMNbioxxumjfQBccCx3XBMoYifHQ01W6j54xjJf68hd6RQt6I8aAE3yLqdVRX5Eqn+gEupw3dG493KXOjcoYA87cjGp0RMkHovqB4RjrtIWo0'
        b'p+AmchYjGj2DEY5k0dNT42jBifjOgkily6XdhWiTD96tpS1Xo3q0L1Ihi8bnbPfo2y7RR3fx05Ts+ayUKKkB5iTUYbPBZJlB6JxwGDqOrlL0Pxx3rFe6Gljireg8E/qU'
        b'AHVnoWYL2SWip/BuG53dhK56oLWUUd/Fz8cl/8XERBY3JQfZzFnFTPBIwTK0G++wEB5qKG5LUCrk+DDQYWdKOxGd4OniCXTIpFwhinLW/efF0zTxdHyaXPpPb/yfZeLv'
        b'/A/O5Sn4oepUJT6Bj7veZD4e1dGi8bPnKicMITzd9jxyITnayRlT0YnHw8H/R98RsJvn8F8NoORK20uuogkxohaT1G5SSEgVx8FfnnQFEExNf4SUgPHnDSTEW1lKHOmO'
        b'n3eEo4VcEDeII0TN2TyH7wBPuHx6SUaPD6+jNveIzBaVydIjgHw/lUqJTOTDOiaDgxgZHRSJEiNy0+w5QoyesBOjjcxr3j9J4N7t/wWTLwGlOsLv/uKmeuD9uyx2txKb'
        b'Cldv06yYNBaryUDTKqUqckLgpKh5LO26dLlmtRnqqTJpzMS4ktcA2VRaZoda36YO8qQVf1Tjr+f1aKQ7pastGg8aKxfaKnaeQCdTfXqjM1CajhnAfO9BO1AjuoR3o8sL'
        b'AXFeQmfH4D1zUYOICUMbBWsSWXr2LRhGThhFzNDhjIJRoCbURZUBC9HpKZTooqaF8lEM3qNUKATMANQogAxLKLUOMhEa/na1hCkJeLqmkrES02LUElTuKCd+ArejO4Gl'
        b'gF6O46fjmIhEUYoVH+blvu5BFofwthdvpAJc81P0+BnV4y3ZdrqOm9U2arxiHj1WHoXvpOJzUUqKXoh0J0UNlFOoSMOtaEd0AU/AOdTCDg9G7brS14JE5i2Qbjj1Tc7L'
        b'o4M4kOze+UZbVBK4Wx39rO9OScKiqtac6hHrXxi9YMXWpHeOJhznvun4oaPfoltHL77b/IvPFc/uHDirefx/nek8ed6n7nzUx5aud6smv3PLWP7xh9cOyS5PUI7ZvOeH'
        b'wN9cHzL3cmXk4r+un1yY+6elB04Gpa3Y+mHwW59+9/wK/LfvuNyJ4wdtE8jE9BR1Vi6+iO7CUrkftuItsQEU52nw8RBA/7briHGzdBk3Jhlv4tFsA76M68eja5GKHA7G'
        b'epoF6QeEAvp9lq0g3e8BqsZ/DYRbLWP8NRw+im+ju5Q6oqcnxfVanCvRDlfhAnWhQ1Rsiuuf0PuZFxEjzKEECjcoZOIfwSdebBxV5mKy1ygSfaIXieqFglCei4e/BCWS'
        b'49qAf4tFYZwTJrEVzv1RA0gTPN5/BFkdfiwTSFsTXWyPsEplqfB+sXs6Y7srmxxekg9EiB2Xuwsf63J3G/J6R8B6OLjsxV8ElZhV1eRNr3fGZI/vGkcGMlGaqZVGkLcI'
        b'KaBjM68iJzhKs4r43RKNcYSiRlcVEUUbsiFLk2eFs5ncLqh2qLlVprIKXbVGIc0jWvmVOrPGgRBpHXQANLtKqjXqgRj8CHYji+jrht0k/OcP8tF13BGZEWVGu3BjfgYw'
        b'KFk52airMAOdww1RAJlMBt7qUyVCl3ilWT06S/izxij0YH5WjgI3AgtXCJJ+U/RcYFDk4eR6GSW+7gMb5uoQipkycDc6CJjkLNUUCPSWFBZtjlzIf4HqFm4fHwlgsIpB'
        b'J9HtVbilH8Wia7Lxtcg8FT4DcDWPwQeGjNbNu9fJmq+THv/9h8ktaeSLUFs3pMnylxVMyGUPsitYcV3h9dMCQWhb7JMfvRvYuEt2a8CHz+rGvf/896OOPL8kJFP/9Jqv'
        b'S+aMmJx5WVtTGTm+R1Wwd82NhlnpG/+YktVQVv77r58OKBcd8n2/3wTftINnDwh83pPtOXwvM/vmazU5/SX/ffKH+F999fdzGz5YPeZfb/yzU/7mh4NKJ0+onvWLC/Mv'
        b'/vmFE6GJG+pqX/vk+sPm300ddvWta7/78uDOgfWCX37gM4uZuPT547JgXnNyD9i1bTDfhFcUJqOn0W4WnffHJ2nq3A1oH/EQsn1GTgJ/2xdx65Y+SVm6UnzWiq/gqyvl'
        b'EWsXU52NLzrFoWNpQ/gr13ejoyLik7Mb1eXCAoGYlMsNR3UC3loFkuk386IUmUC9OmgGf3yRw3dR92TKioZBcpsyCm3Pw415+Bz5uoH/NA7vW4WO8ThyaxA6Q6qQoIbo'
        b'POJctJ6LKI7iGd3T+Aa6SmiITAH8by0/wOAYQXkKvkRLs7Ci0LvCyN7r4AH0LtKRJVVJI6PJ0YRch+8rZBxw7kcEaAu6EME3vAdfXU748i2hAG8g5IkncYM10XxRdDRc'
        b'6YBV3wH4GNrEoU58J41OihQdGk0VR5cttjlJ58JwO+6iFY9CB1Y7GGhgn58qBAZaV0NLBoOotBV6dbKcdAzaRKe5KHwWn+tL0fMjeNwJdwvJLna1qiE/vryqRkK9hwKA'
        b't7WrXkIgtibQgVlJaR5zd9m+eGBhXJQp3jvZxfF5ey+5r4bHD48g+NpBfXwBwaUbMpvj9iyG+Pk7vKEBwdj+yUT8Hw5++z9y5RWx01cby4qLqUtSj6TKZKzSmCyrH8cd'
        b'ihjmU7MdqtuhPDWlVXQ8PF8/4D+ueOtzVU0J8HiPsYk0Ek4o9GPFPwjJ3P0wYBzMJst9Lxb8xL/CIAEAgK2WQdEAFD8IBcwPw+cOTQ4aJmGpCsSCTqObQB/IpyrNQUEC'
        b'JnAEhzsNc3kLvkvKpf7otIVgFX+8bRk5dcknpy3D44RjcBva9b/0wSa3r4XZq3clRD65vNFoOzo3riAJ7YX30czobHSDnln0K1ipVKCLMYlQdMgEfJ1dgU4V0tOHpYCM'
        b'DjoUP+l4k+2zejJ8k6qgzOjSENyUGUWsKu/j5nghSLlNXFYSvqV7u/2+yEzg9dNZqZ+ULHnm4s7O1tgtK9gyn/e4TcUntwT4D0mbHvXBgJMDPtiSXZKk9PNf1Nb54sna'
        b'2C2dtZ3tmbvZsf1ffuZ1jnlqab9V92JlIqqlrgbk0NnrMnmbIFYufoqcJiaokp0RDbo+BDBNJWqhaEiED+D7vfryVcOIxjye/96PKgXfoWcv20fhGw5Rfa2UR4zn8EV8'
        b'ghzrbk9ZQROXchplUl9+MQEgZAEjoykmNg4U/wxyxj9jicKX4BshPE1rHBtJ2CMkBXrENoc1ty9DkXvoTGsdG4GUHM3Z/SM32n7e8c410iPYMfg4OhUZniXPiJqC92Sh'
        b'lmj+mFaK94gGVOITbtA00PbX/IXzRR+R5LILAFlOLajzLRJohPRbewz5yl4LVySCsISGfWlYDGE/GvanYR8IB9BwIA1LIBxEw8E07AvhEBruR8N+0JoPtBaq7k++06eO'
        b'gu3CqgeqB0HbAba0weowcrGHWk7ThqqHQVqQWgGpYuqXI1QPV4+AOHIdB1svhBKj1FJyCUebXxvXJtAK2oRtIvKjHqLlII78FTj+8rH8U8jncHoKH31Xjz4YDHX59dbz'
        b'aBn1E+5xP++pHnOwv3rsQa6onyZU0089bghztH8nU8vS0Hh7iOYYQO0YeY8lCcyJj+3qkYHUwtGHzpNILVNHQNwg9RDbhSO+xUCMVLOBOaa+5m76eVcRg7eVFNMvKYod'
        b'WnnRY2vl3b5dTP65u8T52b5d7EtPzUPOK0uyX4lczJ+afze9mQljmZgRy0qCJkbO5yPHTlnLfgvbpTFVtfizgsm2D9NuWoBqnR3s89C9DBdXOEAnTT5MQbkkpHw9rYdd'
        b'OYYB2ij5RUBJaYh4HPOhvY/UpVA3fHgrZyYUUzu3e0Tzs4EbYwIEhxJOxHCL//bpyIBnJoRm/Hvg+KPpfotbv7h1ZdyvZo8fFrVIP3nXhIQaVX5EyuDkwV2vj8g6/Y/S'
        b'9tnJQ9aOaB44dNThNf0/a57qM+Jg5qt/7ny5eM7z2x5+y5w+MqRo8i9kvrzCtxXfHUs/EIWuoAeZcgEjKeQsqB2f4r9ndnhxIIjIF7Jz8DV0kjBoE7h+RYj/XGMh2rrc'
        b'1SVei3fRg8oiYOiofqTLJCCi9xiZ+7yMGyKqwOdxB+9yuBUEjM2843pkuJzPBpkq+w0eLpyEL4+haoSMKdQ/HsgoaqFK7maBBt9j+uEOAeosGUqVxMPygdV15MlB3cx6'
        b'dAiytAvQMXwZ3aY9r5yL7qGmaGBX8R18LpN8dlqCt3GoDuq/aiF3HqGL+OBK1LQS6qGUGWpDO/KIzX4e3q7AF1GdmEkl/gKJaA+Pgx+buez1Th/pjNvjxKyfSMKGUS91'
        b'm5aVrQl1bKBHPh/J60R7RNTaqUdIjGV7AnpPwgzGHl+docpqoZeC9TKezibpItNm8r6RPGoZO8+5yaWf0W5U4tU+WE8Pvf0p/r+iYjIMr8630znbTnFux+GDPrz3flM3'
        b'F1yFSUmwz09wBw4sdp5Lr12aae/SdyOdmnd3P1f8FP9zv+LelfPW8BxHwyMy7ZntVps/uV2H7zcBpuJKnXf/6yxHs4OIlCHVmoyVP3uc9vZUq7y2l+NobwBtj9j0/tTW'
        b'bCsqLrYYLSq916byHU0NKSQZ7ba/Xtv7z7lye2TFOcb9u4eUimwQAI86Mw6iS6JCZtTwJKpU6cMETEoREyejLyPyGF1F0jaBmSjIl09YTr7lm6FqU4d/cEumVAVoPyr5'
        b'iPmiY0jBvueGbB6SspgpeVXsc/KXMtYSCfnRBQM+ApivFO33jPxsiG8EvtUHJ0vFP4rkiPuzA8ktIKxrTT9nNPH4bt4FbrjoQh96TvdGHv4A//6XpCmPrIe7NGVbwssS'
        b'IRPCPOMvZjbqF+UtMtBJuu2fSGpg/9nJsF8+1L0/+CmRmd7XEjmK/xjzTvWiZ/YN6kL70NWdXYKXb6gyVBL6acmn7oo3SV6ScRaiMlyxPtBGt9DOhV5XD3WAyEmFlB2F'
        b'xZkbiN4oQq4gpxObuXh0aVhfQkpwMbVr1tVoikv1xrLlvR/3sy/zkpohTrPvmtvlQ7YiapDrLq/sZlxUILvgscht9c/0sfre23fZw3YAIDNh/7CtAEBA8J/6eqmncysK'
        b'AiXDvmE/9T8nYPJLpubEzWColK0HHqUdnYW8MnyxhqkRBFJT0PykKnQWhj80eA2zxg/v581BDvOb08nUNRNtR4cKw3PlLJOAGsVB6BLaRQ1Ej6qA1R1wVUh8O7/2qWKo'
        b'maNgTS73aWVjIFOl6v9GGDMzgHf5nDF4kv3SJ5ulI9oyhDd2tIGQs4kj6sT7/fCBwGUUdVJthy+6vpSX7NcM7RXsZ0/QxVQ8y5obIcfkb3817tdERxwmKEnbkT54we/T'
        b'YhaUqt4Xvxz10d6dL/7+eGnW4NszDz5xS+b7p6jXjxysev7fd6RPDB/fGnbpudh5H2WnzFI3RASU1VWc+ndKwcu/DO7fWiO7NONPhncbtP+6k/jaytx//KJb803xWb1f'
        b'g/Zy+7p39jxfFPB18srfDT7cueJZtTD5q9+MemvHE00LNsp86BESPo+Oh1PtKHqANirwDod61DyP8ov+6IogHt92u/9JKEGHg3h+cVsuMNC9/CI6iO553ngPjLzNRje+'
        b'afGPsPHEjkpHoSuh+IwQX1CgnXQ7y8WBvAFdM96Mr9O1JsYOLfZ6xUwMOiMePgwd5TXY5/Gxucqo8Ay0a5GTN+LB2XSzLy9awmsrSnGnQ1uRViNzfGrcq0JUXLzSpLN9'
        b'6dWFbS0mtmocOxLY1qE2G7YAtibEafvRgq6fr1aZys1emFLO1Oa691vhscRt75/s41ufbo3nlgmdtqXLcbLtm8XUR8/xzWIhPdYSwa4X0l0vojtduF5U4PTeF+0Wue16'
        b'cS7Vl6G96AgsILkgchQDUtbmUfF4MxWN6WEMgEI32hg5V76AXSAntiY+/biRcSW6997aIDKTezOXrPuMaMR2oj8+++azF3fear1Ve2tR1BbZvtFbbtV2tS+vTW3JbB69'
        b'b1O8gOkeKVn6QhoQdXoGeph8ExhEnkx0DrXEhCMAHWp5wjLDKoSoQYY77CvUt2JcXExdNygchDjDgT6IGn24TD7NyqvBxU5Wf/RD1FQj5Yr3u4R87CM5KRS0w0PnBgX7'
        b'+/gQsFtHvAMB0VfXiwAMxFSVQUDB5z8FCu7qB1Euv+BkuyqngcS5D10okMN6E99zfIfNwW34mu6tU59wVCuS8NvLn5QoVeGa8Hczed6t5JMSnTZizyclD0uWaz9Vf1LC'
        b'bYtJirdePhFjvVh98USs/4eNsfzXzS33Av5RvqyX230s8xiXr5ITtaLTkg9wXnKThLcAIqanA51mu7cMX9Ue74C117HA++BhdFvg1jDvC+y5yYdEgeJ9qafx+11k2/Gi'
        b'n7HMHlk99x3vvMx41zx85yncAsuM2+MzBIzIh0Wbi9B1XdSXzzLmeArcCZ+UZDqWOUP1cYlC9VHJp7DULc99WhKiqtBml4WWEYbPhzmd7fPP20rY22Q98El0B++UokPK'
        b'7AjeajtW+/ifHO4JKrZdvOq0zC48ew1Z5powp9l2KWDXfrju2h6xVlVmMZq8YHmhqcPbTj8Aj5VugNA0wDsgeO2aLJg3Qu61SSbmyD2BvaL9cs3qnsBqo7WsQmOiRWJd'
        b'g3E9/mXk4hoN+YxsrHMgrkei1pn5G2eIaXOPqFplIXcXa6wWEGjJ/bpk9/YEaFaVVajI7a8QJZPQwzcTETVM5E5RT7ckk2O4IlojMbCK7fGz3yyjUzv54S+mOSw6i17T'
        b'IyEfISGZe/zJm92jnUbTK6xoTXGmp0kZH+JUWWpcRZ3we0RVFUaDpkegVa3qEWkqVTp9j1AH5XoEpboyGdfjM33GjLz5uYU9whl582aZLpOmrzCP6FLIkpJ1Juc+ZuJm'
        b'ZLtHWUztrdl6iVbyn+CnBbYmXPdZmU2kmrBu8FXubyImRrX4l4MyeWvqMehKkBlfx5dHBQNwcfgkG4GbhtDzKXQFb1WYLdX4OqqbFoyv+bOMDz7ABeFL86xkjfDTCuJi'
        b'1KJE58IzchSZOXNxQy46F4V3RGfNzYjKisYtwwfmAPtmd47CrYsDZqDra6nlRPQYdAO3zoW3GrQ5l8nBey2U/kfiKxnxCegAuh8jZNgJDGodh1ppiUC8H12MB7iPZ9Ce'
        b'hHh0CjfzHEN3MJTAR9GWGID5cAa1FeKbPFJpwAfGU1PXsjKiW2UZ/yIOnx/4JF/ubiLugoLtETFihpUBsxGPt/P2ZpuKiB2DEm+ZBYxnIvk2/CUWt2YOoPP4ef8I7TDm'
        b'NMOElDzx5OAIhhqh4dNJeGd8QsVTMbDrIqCDBegWPRJaAhLHdqVCriBuhKgRncqR423ZLDMYHRdOM6PTtMq/JEjjdnEbGaaqZNIL+kKboXsX6k6C/h1El2MEDBvFoH0c'
        b'3k2t8dKAH98VSa5cycTb8R7gVYBVDUYtglJ0HF2jVW7xGzzpJcEicqfK8FnzRtt6uVM9Eyb3aWmMD8PKGbS/Cl+lbUX64I3A9PqZ6OeVhFEsuo13rKEVnVo7ddoq9luG'
        b'iSkJ/SpVwNC5w9cLpkFFN1E9ughinIJBBxIDaU0FU9DJSEXgk7KsHBCyfGM5tK8A7aM1dXPKmIlcOAsT55e0RsnXVJyM78UnBOEOdBHWO5oBsXvLYLoKLKodCaw/MISt'
        b'5AyUWDBs5cbEorO0sjmjhYNKBfQynoAvtaH8lKHTaDO+HZ9gRieSGDpl7YnoPvWzLIXZf6Ak19I04e1KdAgyEhu2IFQnmIKuyWidnZbUsc8xb4PoWRL32vIxtjpPmHBr'
        b'fMJ6qJKjIwUGFdXzF9/UoZPoIl9prv1gg2WGorbidUK0DVjKq/xsXUMXEIDaumVJYjrGfRX4Fj3jLZXjZlt5YvQ+jqxjUJUgZfEK2qE7Ff2zv2aJ7q1kbWTQZN6/Eu9Y'
        b'hRri48oUBGxhiHuY5XS/5qzCBGjRWdRAoJYDqL3M4jZ0AbfwA2nALbg2PnE83hQDkxMHJZV4GxVIx+EWdBbE5Dp8ixgesoxYxw3B11fQ9tYsGhefPBxvJYVSiH/k5em0'
        b'74lWVEthcBa6mom3oQsMEzBJEDIQdfHn4fejlsQnK9eSTTkR4CNoPC1lWjJeSScKX04AzHBGyASECAaiG2gzHfHNGgngQylZguzAKDkPtuhA7rr4ZHQ/L4Ghde03oV38'
        b'Bj9lQKegD2YYWwPeoQQYKeOGoS1mOu2j8dby+GQz2pgAkJUGtcBqXadDqsKNK5TKmYmom2E4IzttGDpG4w0r0T5o6GR4AnR6EsDiSpZ2eiQIq/dBLoSV78yB1WqGGerP'
        b'+aIDg2mn10TXjP9I8BEB7EEXkpbwgC0TB6ErMfgK2pUgYth0Bspuj7fyLgQIYBGkCxG+l0XO0wX4Pos6stADWttbgjklyWwYCzs3a+D4LL42PT6M95H67ixIAGQwg0FH'
        b'FXNon4ei2/NhHRdMzAbWZhkbzWK+mhJd2KpWpoTM5CTFmiwbMN+ONyoz8ZGZxCJIKGRB1rqDTtJJlqADuINY/jIA4zs0CnQetfH2wzfHqajTxbwMkKflxBG2KUAZDdg+'
        b'JwrQD2zFUJ9hqBsfoFA4Bu1eADJ4EDqJW/jtIMH7ONQeAPvIcZn2W7MEE7GA9lIfqA63IaeLaHMY9RoGoN6Ob0RtQJfpNps80Zf3V0BNpFb7ERnQGiEzDp0RWbVWCsXo'
        b'OtpDbMTm6nE9ceoBRBbKLs0p5ke+R4COKgvVGtwC0ID3Q3Nz0X6KGlD7BPw07wMulfZ6gbPMuDyRjvPni3fgI7gLd/iT66WZMMC599EhPW+ecjU7KRI3RefADq4NypBn'
        b'8XJjrJAZXyiKS7Dh41dyhq5axVQQqjF83zKpDcXfASxxA3cA840eMInoDHpgwodorQW+aL+91o05vbVyzPj5oni8aTwFi2R0MU45F9dlAHmlTsb3knEHFZQriZN3QQ7e'
        b'hbbOJZ7b3Bp2OGqq4W2t61D9SOX8qfgkPxknGHwV7Z5H6VUgPjZKmWnEe1xc7VlmFGoS4uuz5Dzp3IiOD8MdgYSIMri7Bt2dhY7wTujX8VZ0iuxwRWYuFMyUxwmZYcTz'
        b'HW0R6qf6UtQgSbHiDgFxgmZQYwG6lzqMrkMerkf7XIpyULTDr1pYidrwCereXbIcH8RN8KKDFX1CZwjhWZW2fHyXGHVSKNkqoz0O7i94Kl9IG4yOAxGAVyksxedH4RNq'
        b'Cli4UYKPR/I3lwFI2Yw1hqNruB3dE+JthHaQLRaEj67DHbAz0B1meRi6MwQfpBA7Ae3E93ETsCTLGbQLb10Oc0/pM0xwB76glOMLQ+SZqDs8i2y3/tMEgI1v4P380sMk'
        b'XcQdAQR+GHRxProKa7CDjqYf2lih5B1XoZp6h0sNuhtKm9XgLajFHChnAgFLwQbE52ZlUxh7ssSv+jAXTmAs26gay5OLKeUluAmGbmTQTtRpxIfQaZ54teB2AHt0Dt8Y'
        b'lkGc7puVeXLaUekwIezF0+geVYIOVo9jX4Hy0nLW8qeUyjWD+N06AN3Cp6gitgaYn+gavAk16U7evcuY/wmM76wX6pb+7iVD/+kh4rc/Pvz8itA3+vdvrj908a9pm8aG'
        b'caq3fP+pDRq3ST/gyT073vMfNO/Izuf7Zz/ggvGYvw3/V8H/NM8e/tndqDv3u87LFu71TXvuzNl/zv/DvYZ7owPbfOdV6o5n//Hz0G1dmTPaT69f/vaV30wfOvaXZ8SH'
        b'Nyz0vfQ/H1/6+Ick1dB3C97dqVzwqwuyYznP/CVsf+7Jfr957rkrf2i9uTk5Z8VrEedTG2d+ILVOWDzzg9GLDyXMvD79QG7prs92jsit3vbp5k+rL89RGzu/mLJL9OL6'
        b'CT4zg9KT0iaNNd185Z1+u45tmfiLmdtn5Kakykxn8j+8+uL+zQcHpvqk/vX9zS/OenHchKYn9o5e2F3+4cCW114Y9Z5qmzJ2/+/CO/5VPOOFvZl4383vZ/yibc/q18/s'
        b'+j5z/4VX3teVD02e+OrXL9zOq31y2UuGkHnT37Qk9rP6fo60b55/5szOE5OO9Xzd78JfhsyvbXnn7OuTg6+sCbrVLv72/LgDFzKvGe9O+sO9wPuHK/Tpfz+y4NzmHf/Y'
        b'arl/4FCl9Mo3TYvXFugrS0/3/1yeah5mvjmmtfHb8y/ea/zbvzOjHw6f+mJS66isLXO2+O0Y90Pm+v/uN3Xg6j3KliNN3W+8dH32v9Lf3fuPD2b96+MHlac/X74r+R/7'
        b'b4Q+eO+bBV/67P1y7qf9c6/99pMPo/tdbk8vnmL9uHHZ2JzPJr46sf3B94KIfv82qv4g60/v0Ee30Qly+zH1KgB2644n44b9uMFmx9qJWyNzYXt0yomnxgE2B5/A22ka'
        b'bkCnVwF/hB74g3AhZoQzWXSvzJeaO/Q3LkZNwVUBJtg7LcHVgb5igMsj6MEC4pWAT/H307UOQqf9URdqnBqVYVci98O3BQD5jbiRWg4PB4R2l9i3qfEdu4kbiy7BLmji'
        b'bUBOZQJuaopeii5H89a0EnyMQ00DtTTZAITzKtVB+9l1hpIcTh2JzlgI9tH0D1bmoZsLyNCq2emowUIV0THosiKSYh5nR3O8ZRXvBfl0eSJQXeCL99l9yi+vyeEPpG7l'
        b'kzsAgbGrm0gdzonJie8a/oLAJnx0ok0LjzYGOSviy4T8rdR3QGTYC72VVjubidhsRArQDj7XIXwGn4ZcxT5OhiI2KxF0HW+iroRTs/BlYpICk3eUHIUQ0YaYX9smITJV'
        b'hK6X4gN0HdJTJvPaVVfV6shZQtSA9mfznipNuFVpdzHZldLrBIk3VfIXEh4FtHOZGKZsRc24MdrJMAXfRHs9fVfgJxvB9ghUal7JswoeDiXPBkYRyg5ihWwotS4kzuUh'
        b'8Gv74UJZtx8S97FkRAg7ljiiA0fnR38DWAk3lJWyQbQMsZAmeUNo/hB2AIS4TyWDagJ7dTbQH+fTARPR1f1Ujz6OL9V7anAVHmc4u/32RsfPH4f2YTjt0ifvZ/3T4FHP'
        b'f2qLqRc5dIgs1W38zBN/0piUeVS3MYHXbfithS0iIR0o0R8KjWV4xSKhUzW4Dp1ChK3FrbNGAid/CXVTnsCMd+QjcnQCMZeGMEMmh/Fc6D10b0a8kDqT34tj4oCuN9Em'
        b'fOZKmJCZ4WLgpwOOCWcy9NhwvBgiQzqEEBlVpR3Pc7ezdevYb+OyOKJoSc3vzzPwgE324d3xIIowcsAr7UwZ3ssfaQ40DoxPAK43cQXaC7R9I6qjtbw4WswE5B+k9gor'
        b'10TxVdeVhzDS7GlCpqok6lV2Ot+JbJ9+jHRAMtEeRLUDW0BzfpMSyIQtesOHyS+Jip7P8Tk/nxbAhIWpyZGq/qsNBj7nST8/ZsDwL3wI1/CKcAOfc5LcnxkQEENEGv2U'
        b'FQY+8r8LoEtjYW6lJdlPr8tlqDTjJ0FdBTnAY84HoYqw5KJqoj04iR7wstt+dGdJfExFMlHnjCWfkrkpos2G9RvDzBzwZ1ioktJtU1fa9ApngPW6TtkK1KiogdWrRQf5'
        b'+Tu6CBB0hx/DzKxE1wmvfwc9zbPmu9Ct6bhDTNjAWHSDAVmyHR/mReVNwP/W4VaAnXJ8Qs7Ih0XRtt9bTE57S0TMtJKoTPMKhn6iD5DiDUCOrcAWwQ/IbHgrLNJWdA0o'
        b'ymEeNhqkIEKS2lD3ghHMCEA5u/iLfO/hhiz+RBew+c6B9iPdxBi+77cq2QL5erSVcHIs3sWG4v1Kem6Na/M0xH1IP2EVswqdHMhnbwLhog2dJTCOr65mVkPEMT5lP8Rf'
        b'oSfd4bhtDbMGbcaH6LkyXZ+iEdCudL4P0Yn8UGrgtdTP/HYZ2UeZetjGc8t1A9vzheYEGEJTzbOVu9Jy8bSQreXVn72iGftfr2YOrw/5cxUzM3DEu9wtFL3p4AumwPYt'
        b'78fN+eNn/XyOzkwVvStsmBGzbMKz6QlpX26482WP7OYrqbV7I/w7BxV+VNdcEX7s6DvPDn66/2++rVg0u/9X3dq/nBUXKQ/96YmMv76iaFvz2swJC09u2a45JWj8OKvQ'
        b'OPhE6/WL9y8+u3W15vzBLVvT6xN7VhSaVF+d+vjOqqWv4j+abm/t+Tz48+/+v+auBK6pY92fnIQQIGBY3MAlbkjYRHBB3BVUZFXctxhIgGhkSYiKoigubIKKGyqiuFtc'
        b'QMUFt3dn2nq9XW7ba681bb2ttnaxtrZ2sdbqm+UkJCFBaHt/7xmZ5JwzZ+abOWdmvpn5/t/f5/nMe/Ki9zLfnbqDv/ZkzLG+a0OyF9zdGg/kZUt3K1673edwQPypOsfu'
        b'Ybf2xq//Qbf299PnX3S+Hz4qb+R5zbjws5r2b3ilis/Nyd1euWDqnbVR4RW6ngO2X9n0TscuMQ+nV21985XKQe+6xz/IzUr9h9NnP9946J6XdPvxiT2bd94Fi8bfHDj8'
        b'vYKCwu5fD1qTnnZH1okYAMEKcMXRbCu7B6izuZM9Eewi6gV6DV+B54kpQnzQmFn+eMhqYNFk9YSE81YDqvuYm9ejKZkadRjVnYkq4C0ZTO010dSMMz9dAusoo9BBBzTX'
        b'QCNwHHZght1Dx/IYj9H8meg9PdkBHqfAqsOqodi3Ft4hL0ZqxkqwN4/tyYPbyMZnN3hUQdS02dNsWqDmw53U0PVs3mgsRgBerzjJg0USNBiXwlqSRQooCza3kAHnAtkw'
        b'eBwJgFuWbO5KjjwKNcejgfF0BbTDDIEPODqXjuuNqSPMuKHIGpRHH34y2ACOL4HrKDHUHrBjPDW1JTrP0umsu7wDqQZ1lNLK6pWqMyfhflDjBNfTp1DLogdghl9t5w1O'
        b'Y+UiNoAgzFYkgVpLu1ii7kyZihSeMgURkwd2T0XKx4TA4GC8yo1khMewHnkV6WNHwWqqOZVMRM2Us9OVwVVNprrEUPfKYlKb48BxEYlUHuPACFjeJKT7VqeB3URSJFZD'
        b'H2qGkAB2wi1GOwTQMDgHr8gED4XFnMmDmbkDKOhoafHgKiJvl+sg2ICExoqrNM6kuoJX0HMlRGhnumFTX+wOw6jALZVYqnCwdgZVzw74LKNGwWguA1aZGQWfzSKl8oSX'
        b'ZgT4YwgJPAKPGP0qdetjNJ9o1XabAJsTWvtVILupYp6ANXpQ8CLalxf6dECfTuiDj92INwUvEsOD+yOfz4Vd2M+EXbGzIDGL9LAXIj7elxWzIoJXW+bWpNng7M2s7VqQ'
        b'ucn4rgEF39pQpra2sClnlSWqI6y0oK9N5Cue/NfuxAcdrVBnxPBYi6njqDEysVLGBsoGkdFA1fgL71pRs04CN8N2YsRghNgLkD1lsp9oEMsTR08eHSefMjMxKsnA16ly'
        b'DALs1sDgwl1IipqSRJRGUliqj/55RxralSgIxDWHDdpEfIl7m9FlDm4CN1c3oZdI4mh0nyEkVjZCy8/3Ag98zXietb5u/DwUfCv0d+O5PRc6dIrUc9R2lUgvRB0+2Bhv'
        b'tPh0YCRT+LNCPZttdBvZbXQjrMl7BVvbEXLbdsZvJWv6xS9zVPZGGjPGibRLFSgdlSITla+T0pmge8Qcla8rOXYjx5jKtx05lpBjEaH6dSZUv2KOyteTHHuRY2dC9etM'
        b'qH7FHJVvR3LciRyLtwpSGSyVsnMVu1WI8TsLXJXenZl9bhjpwh37GI87or+DvHKesg8Hf3ck3qNcCtsVSlKdCCEwoelF15wI6a6AIINEsyS4NpQ9yniFdKYgLnRF84Se'
        b'yl6EkNdd2YXMAXw5Qt6Y+Kin2y1Q4lOMBLHoEmXjlfphqhTMj6XIUOKXX23N42lx4D8Fg9U5Siz0KzNZl6nBRN4YY489GVNGUuxJWZWVQ515E8C9lYNpLfZtKXM0OHHc'
        b'bpj4iPtJNpxF1LkqpkBSpi428BdmoHOLVEq1fhE6J8pCki/J1Cq1TZTANrl4Lf10GX2mO6EZljO3j+xi8tPVFjZe7HTg+1az8eLK/sNsvC8n421GvGvT38AfJOM1eygm'
        b'ObDX9RakQJftyZAhVWiy0hVBtkQZIk1JR1mmEN/mLXMDt0wNbIMGuA018lJqYPQ+UjfQkeOmSTWKZMxCj36ae9aWBVv5rKZ0djalsBSd1K1fqFlV2BCeEwS1iZcQE9sj'
        b'IbbtkMIeMXErSYhtJtpETPwnSIiN7Z5WOz2SqpXcAwt72QMzdhac72/uSKpVpal1qIZRJ4X6MvI6BUr13GPTZ2Af3H+I67cdXVwpFbl7L+GPIusL8/r0ZPTYOCcVnEbT'
        b'7CbuWydBM7ZfpEtakPKuGyWWwE3DSZpzBnotfsAm4u37Yb/lJjDEKW7nWNhog04XHOpnlibhuTFPdm+WGB6ER5xJum/7iwdF8kIYvMKxV5NAaXrVsABeogkHI23WkprY'
        b'bM5hLi24AIpcQI27J0n2skQ4ZiDbCVtTaKrmjGL0A9HJ3HCxLfLfCdEBSeYJrYLnkJ6/0QlV13Z4hm4GuoniB+LVrPnzA/dHz6Pec8HmMFBOEwS7wRZrRuGmGZ6VmOdc'
        b'wIEseIIk/CDfpdtehuwABZZ6Chk9ttgH1djYgUt5u8gyYT/jZMYi1UZQ6wKLwGUH9RXVYL5uA0qF1/lE0JuX3Nn+4qhJN/KDto7u8WOdwya/+Ts21LCx+0L38SbW+FYP'
        b'dBv4xYjbyTeO6tK2uMzsfztb9p/3fv9xvuuevRpY4JNRVhcWeLFsReVvX8ZFbnnXb9fduFfH5B1p97czy9dPf+Jy56Ow40+ORIyc2i/72L5n++dc1jxO0l2f1e5R92fh'
        b'eT6+EwNu/NTOoTQ85bsYmTOZj2SBCwubWIm5SeUkPK0sSicTz07zQIGVSfoCcAIvhruB/WTmyB8fbZ4CPNSR+O5jusNKATzVlU4v4TY5XE+mp+BovOUMFRwHlYPJqvzK'
        b'nuBEALjKmnMOK+Apck3vRzw7RbcH27jpM9iXC45wDgVh+Xg6FQSliXQ2iGI3gD0074PgrCeZ4eelW87xwUlQw7npA+fh6vF4YhoMdlvMTeEWz7wcbDI3BGmwZXTJAlzM'
        b'D4Jn4DkdWbJAJ2KJPhskZOLAWkewB56FDX+Zem9CcmLPEmZzuXxmDGEX5gmbmIYp6zBx4Go6MtL3IsXDDu/wNRz8Dw7+hgOAA4iDV3HwGsO8nHhH1JpEXC3KJEO9JcEe'
        b'mU32VjG3W3CB17wcbcHmOctNSpRdfN5UJBNFfzblZUZAjE+1QEDcegBompEP1kyjsivUDKNQT7tZSUD0gzZS0aaaaH857cluvrNN+Xan+f454mMuY4Ec6Ux285xnytOH'
        b'5mmmV/0xomWBHKlGdvNTmPLza1KeFNYo27aTK5vQrkZ1xa4ESpME3ngxw0yj+YMFdpKbJkT28kyzyBPVskkPMstTxlLANlkZMdnkxqfwzUTBZu+4LROj3HgUkO0q7NKC'
        b'5aaxzsQBsjhVbDKCd2iVETw3sfrJwaPVNFQqTMfZWhYqErktJFTmpFPNksQkVCY8tX+g1N8c2I2OCVYcRTKn0CF6LhUDM5O0fi5oyihCmpS5CM8o6BQcu5zj0NmK5Ex9'
        b'DsftpEO6q726wf8wj4oKV4lSnUpYdnI43dyyUFx9E8eaqNrSOId6NtRi/C/axAqlaGma13+Q2eRG6meknrE/zTGvV6rCN2usUr/RyVpVSnoGZr3h5nzErZ5NQZveA51O'
        b'nZZBXgXKLdOM4EwnVZuXSo2mP2l2CGyM05r+5CEPGmKa3eCc+ssC8aKJkTEZxzBRJqfYm5CRt1JN7sc8W7juwoe0nqcr1bJAuNRqle6vY9nyw6xShA9LJvX3X4Sn3Kg4'
        b'uf7+f5h3S+pHOLaCKFVVW5JugWOrVfe3lfFKaoepyx7jVXDrxLBAjLTIe+Vn4r3qL5PO7h9qn7fKHHXCPUa9ihZHnUEEJVT3kXFxM2fiktlytIv/ZSlyFxE3vSotHqoC'
        b'CamdaaZsJlBoywK1SMZluW5CW0s/Y0uxKRZViMwpvFD2YSH22djMMTrGVSSzZoLOohaZoVNToTJTbZObKRegN4PUB76B+CpWLMW/W8nrhP+NtkhERxbQ1CnpOWpC3qVr'
        b'opZr3mbtphkk7Y+5s1V61LmaEkBvsFrKVRHqoRahFhc1NWiKIidZhRclbVONBUnR60J9qGr0ixaq0m3Xf5A0zCoayU2hT12mz1GhkQP7rZZOy9TqiFB20hgQIR2tT01X'
        b'Jetx00M3jNbnZOLxbaGdGwZGSKMzlOrFavQyazToBkqAp7MquZ27B9kSue0VNNhWMmozsRa1TaxwW+m1rV6GkIpsqvqX1LzNk1Pom4xXD63kbvObaF78VC0qjR+uW5NM'
        b'iuRl+jSZ/dfP/Hbp4D72X0CLiP2H2IuJXrOMfs25RenFgdbJDLKXzKCWkkEvhal8LaQRbh7NbtGGWCRmo1x2BzQOQ4h6OO4X0QeQTor6VmNX7pdEx1i7A3YTRDFCOhZz'
        b'mNIjpOP4xaBDVQb6Q6+5FI9B4fb5NpvAjZbJhFolE9piMgQHaUHA6EdYFyPxeDPQ7m0m3CS9NWoq6anxCakfauTcK44eu/1q0GsxESUaLcZyvwKlZrpd1NTJUr/p8GC6'
        b'FjVSJMsA+6KYQTabEjOd5oQyJqVbqNfqmgvVkrpnT70kqmTrNT+TijbaYiOgdToMAZdGSOPxl3R2aMjc1t8WSm8LJbfZfxpG1CqnQnLHePrc0ntAIK3oFvyFIjaPZ78X'
        b'm6DSajP6jdMq9CjQBPcbp0banf1ei0S331fhdOz3TzgD+x1USzmjXikqHSlhqO+33zUR2ZDOprQthr3KQ1qsSpWDNQv8jRSsQS3qd8mZSyOkeF8Z6U+pWGtFJ1Cd23+o'
        b'+CaMKKZ3KTRSfNDiHSnqHNwgUdiiukeB1Dgm/UESDsR6elBY/0GD0JtmXyaMYEYC4a8W38hUBSrtONSptBSJYKDRE8Jf0tmD7Efkujkjx2wLb7QRnR0hHYN+UU14dujg'
        b'FuObmja5xXKjr8X6NmK+uTvp87HfWWOsN1LRxoyOR4/Hfo+YrE5BCUaPRVnbaJHNUNp4S98mE9aH/fkELR4ifBR1MWk5o8cbHUNARTChpMS4yVp4woSqA3v8yF1+Iyi/'
        b'ZYivkyS2sx/1lSKE52BVTHQgOAFfMcL9wGU9ueFZVEcmkGEkId3mhLJLXDnr20pwBJaC47CSwwEGh8KrRACwOwoWx8TC4wkmQBiBUsMquJ1CIPnEAeiMurmVDhukaZwD'
        b'0DJYAmsDUHRMspiAbQrB8YlxxBHTFAbWg1LsG1+2dIBTGqjlE7TRYAfMLCnpyiculzqE3jBuYS2HDbA0bjIoNfe7RLfbUGIT6BaGBbVkGdgplsEDcvWvm19jddiT6I5p'
        b'S8rKr03kKySvpv186YU6aEODapPX9lw2xmHN79rXRePDN44Ce9YV1qkLNm6aUB2fJ7rW7xd22qVv3ny2eENt5MUDJTe8fzrw/cPJH5dvr0wfsL79lZtL7geeWXrBb8Dz'
        b'rf3d3vns7/N+Fv3SWai/4fZ+w+G0WQ/Vh1Kr77tpu5w9nr3rl2fzXQ5EHXrwwXs/qM6m/r5Q/cGyBd/7/3SsWO9V9WHAms//eeeXt5Y/yb/zL+36Ia9Er/W9/UyyR/Kh'
        b'i0+Dh4du2K/Vey7HTBXrSmTDvqj6MehfHv2ufl+8PDQrg/2idPeHLzZ7tast+XvH/C+mTeyh4MtEZNNpGajzxk6Z/cCaJnhJ9DjqBOksrO6BQZ1wPzxnhJfAcniYQm5O'
        b'gd2xAbA4YWBsNDguYIQatqcA7KCO8jdOizHbUoMNEUZ8STTcTB09rcoYQHeaLLeZIuZZbzQVdqYWk5uYQZyfp3Y9LT09CeCpYfA83Qjb6bnQnNnwMKatMnIbpsFd1NPH'
        b'mvGwJCY2modEOsRO5vlrwdbmoBDxX+QtHVvDkc0tvHltsbmVzySICEehgOfG6028PuHf2NzQmdvYYnnehLcQf0t4y8SmLRuFUhlv4TKkaSEb23Ob7WY5tUlwmcAskSZv'
        b'pqaSLLC5pVXZ0/6WloXM9tEgxIMUtlZiCgUmD1JtYXVKR6Jno0QselFcpOZ8gn1oL6rpi/rDCQ1CbAlf78WjSAWwCVTAXTr9pIEhGPeK3q3oubwVoBDWU7gINsiP7A5L'
        b'XNCRPn46Mx0cGEU60gDJgiR8jx/YhO33L+HmUwZ3kpw+0azgPQn+WcCEKHx8J7pzgPUieDSDgDrADnh5AaPKBydIDxsNN4FiAgIB29qB80wK6qKLSDpr0hwZMXOVxdiK'
        b'65MdKTQjLUTCSCfw+UzWfPHdAWJq5Z+xGJ3Mk7PopKb7SAGNeVbkynTK+paH7R7eUoTTmO1T0Emv9gJ0UrwtPITGfGeBM+Mlfh+bCIgPD42iMR3mYgzITAdsNxA01pue'
        b'vBcgZMRZUQKMQPnGh88VrRIeyEtKTExMQ6XjRTJg9fhoCmg95QrXhoWEhPAGY7KMg9jqfX0+HVfOi5ySEhmM7DuMugZ8pcyVQF3hWrAZXKDwEYodiYfVPNA4B1RRbMcp'
        b'eBruRKli8Ag4BzcwoMIjmTwp0TRYgTeRUDvvwfSYzCPw4Kmwcg4G78wBpaFMKAurSVS3UcMJBgRsGRnEBDn2oCj81bNHG8EeA8E5ivcADSGQokp6wOrIpEQpH5xfjG2k'
        b'2wtBDagMoGjjumBQZUR7UKgHrM5lJ06CRRSLgatZ5+rESPJ6Y2RQ7FgvT1qjn/qLGMmEKkeMIQqaLaAgcDmodUQVSnov9HocZRSwEJ4micj6eDF+mnl89Bp3eeozinOB'
        b'dnAwKE5KBPtkoHE5w0SscIE1SniJei65CIpAuc41LAQUwPMCVOG1DLwSC3er42cF8XRo2GZ+812waPNwjPtYl/Zvp+LH3QvDez9bV7WmoqC6w9HqIlEc+7Dx9ASXTXO0'
        b'az/+TRo/6i2no+6ZDyWTIgNmDt17+fGdy7lbY7dXqBXT7t58Y9vlrz7WpzrX+97a8Zrvp3HadfG9S49nv35mff0k/x3J70cVzXEdeJNfnzr1+t+25F6NSlmxMdX9aTfp'
        b'22ULpT/XLGjsFHQqfey8t6ZMmNW7a8W32yNrYk4eHP7e85GGYNlv8xPf3XNn6PoH7Xpfeup54KeOteUP7r7zoDx/y4u6r6d2ufeeovuV9xTv1E7fcqSg/+TYpeUlRS/E'
        b'latHrfl6RIFsfWVQ2ryPJdfnXXlF41F1Ydfnw5PemPNVxczvVUAWf0w/LW714+EXBfJeb8bIdT+cnbj0tyszBr3YGjgYlgVecL24+cmnHTtOyfnPQpHMi9hOzIdXVlgN'
        b'aNfgCZu2E6ARDYLE4sMnLICMkuiSCF7yimLBZjHcR4EMZ8G1TKQSxXrCIh4j6MFD913Oo0iQhmGgJsaMKxGsARfZXHBiJQUGXIUblEagyFJQZ8SpHgKHCZdwVhZcHWPD'
        b'w7o0alasgxO8Ck7S0X8/3AIaCZjDb7jRHgVFv0auzocb+lh4O4WNuWGwChQTlARqkTXZzYxu1H0FPrAGXKBAi2vwpI8F4IQFp3x7IqmvUETuxhWoWBTtIfCwtKaBl2ZS'
        b'tMklUIdaHHY7AbdncgpKT3COZCD318dgQ5Zr3k14Dzewhj9GoaVoknNwFziLoR6wHq6xYNOEG0EBKWWwvD1JY0OYCe3htoIfuTKZ0lXDElcC9OgCTlva08BteVTAHaCB'
        b'5RAcYIM3Z7YT0Zc8Rn9YBFbHmLNTwgIRizLXUV/uJ8E1cJrCdtL41kY9GwD1+J4AzvmZV7TJMIkvQ0NXKiiyY83yEgeFhGKGaC3LmmstWQKOV5lFuoqEFREreQkHdMVA'
        b'CwmBWrDo29mMpFLC/ZHPfaEP+7moizPSGQQcCEPCWduzT4RO7C8s+hM5czRrRHtozuRmuxBWnG5YYfG3VlhWMdUt+Ty0zlSrw4rFf53YTau31l9ss5o5UlYzuA9W9iQs'
        b'W80pzYTwiJHVLAisJmPZSngC7jSjKIMVYBsPFHQDF6krnlLUmMoDPPIIUdnSZFBG0JGR3nEBCUtBIcdRBmtBoTr5fi8HHQZ4DFrU0YKlzNOzVy/Pj3jZvE0SD80kR2Hv'
        b'9OvKmtLXCl51qnDJ9q3q2aPf3ocvetwvmJDs+b7LjTd3fhfT/91nR+vjfctnLdvkVT9BJPFZ7lT/3YxrZUdvdR69kM19dTQQfnG7uImm7KHex1dycuqtsK8j9hrC3o58'
        b'cun8yPNZR3YX/VT1we3t8sfzr5QlxU35nec27cjAXc/nHXh+fMDwf7r/erdu7MwVvAIYPu7DjrJ2pG3CGtT1nDCRlE3tzkPNaiOoIZ3HDHgMoKlkYFd4yoynjF2RAuso'
        b'8L4MNKYTErPiQNZhEiEhy04it84NmUUYyOAxQXC0GQHZeNRiydxo7SS4ijCcpS7h5jCU4QyNGPU53PjcmIgpyjxGJqBOz8hQ1rU7IQ/uOglD5IoxN1mnwYSdLBCsoV3q'
        b'wTxwwchOhorVF+6g7nedlHTcKIPFhHqNkJOh/mU7JSjbkkcF240ebxFHURYsA6v6mijKSkfRKishFJrlhJ9sOSwkFGWgMoIOOzuQ3AUx4ARYO9JEVMaCmh7gFC3VEeym'
        b'C9OUkUrTZROWshGggt5dzcBDFuRBG8BaNGpNgLVkqMzpAgqoaA7wGlhHicqUAX8JTRmh0iKdnX/zzi6fCerZMlMZ7ieamMq0S5iW8WBLLbLtjs7pApt3T6uYey/lJjNm'
        b'jDoOS1wIxYix5Cte5mGNC8tlGHNwWCvMGi8yxMl4jmqRjqK7rBjI3P/UXLkVT+gKCnrgnnwaQyjHhBKemBCEdZD9UcIxMR5yXghQKtIlHkNF1IdXvyHJcIdeZ9LiHBhX'
        b'bxZu6QxXyXjx6gkrovk6H6QeO35UElV+kcKiby2+G/TvXoUPnxTpPhnGbhx1nZ/IzC2RZ/Q8xEwvGnD8UH3ugtQyB0PqF7tfVH736N5HX6yY73Xztdz8+vwvS5SLX7/4'
        b'fM+ns/5969GbRxd+lTD4DdHjik9GzvBtLH28OKN978cxw/+lr/371ec3F6wdN/PpxFuPVk7sxFZnvxowT/emLDP8XsHGOYPdewZG5D/qFv1z8aOqK69Dj9q3r//jS58b'
        b'909OmtGrg0d+RbZwYL3gWF2O8uZ36yp+9Ks+00/9Rn3QzqfaO9rXho6ou37dFwp3Lg07UNYo++z3/ftG3/ufzZ918Ls0P6tPQszbL94asuObkqGgw7YLAQcc075pKHv7'
        b'5s5Yw5ib55K65C3w+Kau4z9Xam7u6+vc2L1zbipSzmR8usZSAQ/5SgWwFGksvHAGloPNbpTfkZloWhma27XJ8ch8R6LPdPPoZPLm3T3PapUHDXhHmy/U+Px3Xr42B6jD'
        b'4Rsbn82AAFdFcrkmU6GUy0mHgxdAGW+WZXkDeN1esKhrEfI8WJG31Mvb32ukV1+WF4G7oGEivpuLbz6zmOVpb5laHd/AyuVmKz3e/w/qgKf9wNRosaSEow4vDjNfjrJP'
        b'i0YU/tMKD1AKNqIBoDghFhSDjY6MG9wKCzrzuw6B5WrPeRcEuo0oYt79z7oWD0FKh5fDi1++lRRt+sBr9ava3ifnHzo99B8Hxy57Nnvtbo85b23wzd4f61k24HHMity7'
        b'm9P23LxbIvv9lLtc3Sfw5u32/absvVETWd+nqHaRLmna/okBcz78XH+7SMGurtnnrnhn37p1YwuDFn9wb1Wv+C8/zX7dgTf9o6zrKV9uSfi0a2T+j1vuPvq1D1802e+D'
        b'outInSCj5ybXODwuJyQoMZCDMCO7gNMsPOoHVpEYy8C6qTGJ8FxCEJpwoHiYXNQdXuaDGnhhKMcvmjicVgFW4/GSKKqCYbDcg99N3onqHXvg+oyY6Dj/OEdGCC9IBawo'
        b'ADaSFrdgQjdY2k+IdItdDC+JgQd44DxRGOBWcCguYKIDbJjE8GLw+v0ONInDI8G4eeAs4dVLHIXyw0htFxkLN2E/lHRQXg239tXhCKAwnYvhHM2Cuu6jyHU3CbwWQ/pK'
        b'Onlyi0A/Svjx8NxEMmjnxoNtMWAnPBXd5ElwDSyjZAElPBFRRSdEJHIaltiThWfRRLWIROjqD0rQ7KckMMupLxfBGZxhwVl4nk98EvSO6YOunxaDoiXZengmW5yt58Er'
        b'oIrpCDfykfqwBZ6gM8mr08HOGOJYAakXx3FxMBXBLhbuB8fgIcKwBc93HIZrvl8M6nDK0Yx0Iz5yBEhNY3x6C8AaV3jRwvNy1//7tmbd9Jxe0v3Y6I2akBcEku4qop6H'
        b'CPkAntCJ+SOstaHeVHMgHVB3A1+jyjAIsHGvwSFHn6VRGQQatS7HIMCzJoMgMwtd5utytAYHwlBvECRnZmoMfHVGjsEhFfWD6EuLbQEwg0mWPsfAT0nXGviZWqVBmKrW'
        b'5KjQwSJFloG/TJ1lcFDoUtRqAz9dtRRFQck7q3VGmKlBmKVP1qhTDI4UiaszuOjS1ak5cpVWm6k1uGYptDqVXK3LxOaKBld9Rkq6Qp2hUspVS1MMTnK5ToWkl8sNQmre'
        b'Z+ZRn6VP+0f8+xEOHuDgUxx8goP7OPgYB1/iAPOiar/Bwec4uIuDb3FwGwcf4eArHDzEwR0c4D0n7Q84+A4Hn+Hgexz8Bwcf4sCAg8c4+AkHX1s8PmdTD/sk0m4PS2I+'
        b'FaVii96U9GCDRC7nfnOj0VNv7liapUhZqEhTcehmhVKljJeJiM6IaWwVGg1HY0u0SoMzqn9tjg5TgxuEmswUhUZnEE/GxoWLVFG47rW/GGvRykzfIBq2KFOp16gwAp6W'
        b'QOCI+jPrF26wF8Hj/y8X2tYI'
    ))))
