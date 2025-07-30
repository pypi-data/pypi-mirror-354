
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
        b'eJzsvQlcVNe9OH5nZd+HffGyM8AM++4GIrKjAkZRgyMzwCgMZBZQjEaNhkFAwRVcAhgX3FETxSXGnNM2S9M+RkxEmr7YJn1tXtOWJCZp09f0f865M8MMDCa2fcv/8/mR'
        b'eOfc71nu95zzPd/tbB9TJn8c/e+X69DjECWlKqgaqoIlZe2gKtgyzjobatqflH2OxYSUNlIOm5LxzuljmiiVzUo2gvClXEOa7Sz0biUz5mFRG3k2O4T8bzfbZmeWLVxG'
        b'1zdINXUyuqGaVtfK6MUb1bUNCjpHrlDLqmrpRknVekmNTGxrW1YrVxnSSmXVcoVMRVdrFFVqeYNCRUsUUrqqTqJSyVS26ga6SimTqGU08wGpRC2hZRuqaiWKGhldLa+T'
        b'qcS2VX4mNfJH/+xwI7yHHq1UK6uV3cpp5bbyWvmtVq3WrTattq12rfatDq2OrU6tzq0ura6tbq2CVvdWj1bPVq9W71afVt9Wv0OU1lfrqXXVWmuttA5artZJa6t109pr'
        b'bbTuWkrL0TprBVqe1lHrrfXQ2mm9tHwtW8vS+mj9tC7V/qjJrTf7s6k2X0Nzbg6wodjU8/6GdxQOMIRZ1Bb/LQGlVLAFaDO1gbOCambZ1ArZxVWmXeeD/rnhinJJb2+k'
        b'hLbFddYofDGQTXG9ClBoTeF/zHKlNKEoKH4BXoDtcBu4A9tKCpdALewsEcLOvPLFIj4VvpAL3wB71wtZGtx8sA8cBa+o8orgbthRBDtYlG2eD7jCBkN5oEfI1njgNC+C'
        b'4ewCB/BqXnQej+JyWaBvCbxMsoPjYAjeKkARItiGCuBRjmAoGu7iFINzuSh7AE7TqoLHQTvcFd2IsOpARdiCq2Af7GeDV5MLNMEoiTPo16AUV+yBtvk5Dbz6nP1zGhZ4'
        b'GZykPOEeDuiAd2wQvkEo5SxwwROlvLAa7IkpEEVirOEe0A72WFG+IVzwoptrFcuk4XwNDbcXPQ74tKLGQ/3JRb1JoV60Qj1ug/raDvW1A+pfJ9TTLogO3FB/u6O+9kR9'
        b'7Y362VfrV+1L+hkNijYrYz+zST+zTPqZbdKjrC1sfT9PgRr7uWZqP3tO62d/pp9ro60oe9RO81Oet39z9gqKAOeisnHCfrtN0R+wixjgHzNsKGeKinV2k9l/6tvMANlN'
        b'PAr90l3VW+y3StypM1SdLQKfZXtxH7tS8yfcVswfY1+Lu1jQyKrDnOOzzb2sIathNm/+mvgP4/PX/CdFwH9u/tJpv5OkhVr8iPWd1zxBIzVOaUQoYgk84Yv6tj1mSQS4'
        b'Dvoi4K6YXBHcBc6UReQXwT3R4jxRfhGLUjjZzFkVY9ZBdoYaK3EH2ek7iGfWORTunmo7Ywdw/2UdMG2gWU3rAPtiJW5BjTt6qGD7rNKlInjQehmbYnMoeAzcidC44jwL'
        b'4bZSNkUFw5fBfioYnLAhGcBJeAgOlC5FMbXUavDaQvgG7Ne4MANnx2y4D7HxmLVsKqYgg6SHJ+FVeADuQy0kegacokTgDDzBxPTXwP2lRUvALUfYyaPYm1h+sUs1YTjm'
        b'uAyNQTSwogpgBzizArYVol44E51LhrsYnuGB7W5NGlyrYHB4PbjKp6jZ4Hg1ehwAnfLrUQK26mco8pNvvzvy7pxj29oG9l3dtz4pmOOlfu7A/BX29tZLPF8aO2b/6rv2'
        b'cYX29q/Zv9aR1OFQJ+w4tirJPnn+jYC5/TZ+SR3HPjzXS59tDyntWed1tcc7dr6tytausNzd923+oDd/ccLYr6onqIXD670k4q3n1DvPSn8vza/afu5gZnnn+4oPBMk9'
        b'LcPytMWjPb8Ks9lWyF7btEPupaht/c+1n0oXKl+MGPm388s/k7018sbtHf7in7IS260knhFlaz4Ly/F4SfDz6OLCBJc4t/fu9rKo629mdHuIhLzHmPXUxsPzBbAzCnYW'
        b'ifKjwTEwjLiPKxzmwNbNYNdjzFb5cGdMVL4IavMKi3k1EZQduMxG/doDdz3GzAOcAVvLosTC/KgFYL+exTnBrZyG7LLHmAH65K+zw42tQbxoFziMCmNTLvAmB1wAp/NJ'
        b'CbAdvLoa9c8uuCcBHoQdHIqbxgKX4XnYJnQYZ0cIlWi4Uv/gQ+WAHjS9dfLvW4/Z1cqGFpkCSUwii8VIjsqa5o47KGUKqUxZqZRVNSilLeavbFzWV3iIb6U+f55Fefj0'
        b'hO1bpc350C+0v/oDP1G3dRerK2nMzatrzhgd1JXTE7c376H7rH5ev+q+e9QYHTbofsn/jP+Qajh7VJipozOnJnlIB/cvfMXWBDzIG2weCU+5756qj3tAx+vo+KGEYc4o'
        b'Pds0v/q+ezRKM7BgkPdK/itOpmVwB2uZMsbo0NOOA46DTaN0MpPgE5/gkZCkG9zh8lt2upAFoz7ZI4LsCX/KXzwRQAk8D6V2p/bkjLoFj9gHf4mHvhKPfaHjOJ9pkXGr'
        b'ykqlRlFZOW5XWVlVJ5MoNI0I8g92kyN6rDHrJyXmAkrMO6Z0xTycPg09/rKV+mYTi8USfE2hx68cPdvXb7WbYPNYgod2ru1pv+I67Sgas3Z6aO325895FM/Z8PatCjOs'
        b'w/xI6qxdEseMvRm1xjWY2/IOUTKsMyKNUcqq4KB/XDlVwUO/fCm7wkpqraWqWVLODpsKJsTdYV1hQ0I8FLJFfJmlZVdzpHz0ZkcUJS56s0Jv9htZSFe0GecvJVUqJm1b'
        b'xTHBhGtgtNUYExajvB3CJVKkTMzrkY7aZtRRN3MJr+eY8HquCVfnbOHqef0U6MzCljON13MZYcu15xJpGVu0Jro1iU/JbV/czFKtRjFHL+8/8u7sYwP70tpZbuoruex3'
        b'vMLo9rSXXcIq7Jb+bPuZ9Hb/0vMvSZLKKm2r3HNjgpteF9ondSylV/asCeqlA1bJwku7nReHx/emeKTEv1m3RjrIzfq5B/XJbJcdiXOEfMJRHMAV2B5l1G2i4Om1fMoJ'
        b'nOK0PAdvPcbqL9LYdm9mUoAu2I9TcSj7aI4VOLn2sTdO0BrvXwDbC5HOJ6yG3XzKGuxib0gCZwjHswEXAdYPOwryQJ8YXEA8MJXtjbjbjcdemF+dKVkI2kvyouGwOo9L'
        b'8eBRFrwJdjIlo69tS4sS5SKFD3HTNqRVwFfZYIfGXcibmfh5Bh5FaH7curJSrpCrKytbnBjyEBsAhAutYbjQhJpNRcdemnNmzrCnLipT5xzRxd1v37NuTOB1qKC74IEg'
        b'VCcI7V83KogbytQJkrpYYwFBfet71w8GDcb1NKC0dmP+s9CP7UM3T32efu77gtAJDiXwUroZBzx/nKuS1VWPc7G5MW7VJFOqkGWixDJX6WGsAh+P3zV4BDPjNhCP26no'
        b'r8QpE9Hjr1upr1VsFivwKQbtl5jy9vNDqBN2MZwqtqWhstY4VJiBUs0mw4RtphJxbMwUHtMhgwYEewtHP0ymQI3DZMfUYWL8vMkw0USh8PPwDNxtB64Hw05ETbuR9gf3'
        b'lOYyZLdk8VIR0pHmwQG+izM8ImfVU2zVXJQpVXbxyLuJaAQN7ItDY2h/nMfnB2LhBqRN2JfX2duf8w78r7CcfrFH4eoVn/WsPda4+k37o97UBSVQ2XpzPYVcQoVr4VBz'
        b'wTyVnsL15A2HwdBjbCKAPtAGXkeKVBvcA/eIRY1YNIevQILZZwsX7ISdMkLnLeCGO6FzQuS3Uhk6P7boMVHc0NgLKSgRsZDqjMrrZ2U2w0Eh24SocQ8ZKBpJiBqZWq6W'
        b'1SOidjVShRFG6DpZT9fZmAB71H2bejfp3CI/9AkdCUsfLtOFZY76ZI0IssY8fQ+1dLcc2tK9pV866hk14hxlQq08Ja7hOFchqZdNpVEeoVEjiUbjOlpApspApd9upb5a'
        b'wGGxvJ6WSvfyg6jjdiLO/zWGbpFSI1EY7rUBL9tZJFMf1SShwjca5TUtLzCEmjF7DsPqn0CoPykO65/rUbj5GNKDr+zdlqD4wJ/6bofNpwHPCDkMI94tB7cxJ3ZLNqXU'
        b'qyWPsdULhuGQyxQ6xVSKbIYLhFL7vAmlLgZXmhhKXQV3GDgyvJAm5EzltBxClJNUqbJAlSozqozTU2Xx91BlMGK/h2y7bXsS7znTpuyTEKQSG4HjvCZJnWYaWU5lnYnm'
        b'dGlEp5Yy4Z5FiC5nPQVdKrHfwzLXJPTIMXJNbFpS1dz/Bs5ZPZUeedPokVesicUd3+YIerDTpAxqRSLxktz8cqgtKWWstlxkwIm58GUWpYav2/DhCbCNsFvwMrIkOs2o'
        b'uDLWAruF17jyP4e/zlFJUaYb232OvBtPjLob+y7vkye5cbwEqkOx8fMzbT9eF3Gr7fI+3c7AZbu3DRwceGlgX2h7G4uDSD3ha+sDB9yGgCbh/diyy3Gx9HtrWJ9K4f3e'
        b'H7cJP7C5fqR7AFG7A/XXb13ke4b1thboEIRMmkJ6MwiegOeRKbQ7iTGFDmcircPItmFfPBkPSB+5+BhL1HB4cYV+PBwB18zGBB4PL1g/xg4S8PrmKDQcYuEFPe/Gw0FT'
        b'ROLiZ6cy2gmPAvuFjHICr7t8r3Zi1MjH+ZpGbDC1OOgplHklY+UZZqx8vpxDeQX1hwxy73uKPsRWxrxRn/kjgvm/8KO7shH/7k88nTGQcc9T/GGAcCRy7l2BLnLhaEDO'
        b'iFfOBI/yD5zgUy7ueCw9cA7UOQf2h7zvHG4yoqyYEYUZxJShZIK0FaXn9QZDYg4eVeY411OTjP6bZ56S0TMDytRTY66GcIinhjjS9Mwde2Y4/32usenMnVMsf8ZpBY/Q'
        b'+bGa+ZhbB+4MPNaNaP3kPhHi2eerd4yUn8cui/lJha/8tGfdleWXf/fiPbH95bP29nHzV7/W8Vrh2B/eXvuW4Jxkx8NVP10Fy+BiWMeRfjN4NZb65bsVnOZnYjk16VRH'
        b'k8uqu5Re+QD9wSwjDYeCLj1PP8PEusN+0A/awXZ4vsSEPB38CHk2w90L0SjebhedBztFfIr/LDt4Dmhn9O7+ueBV2J4CjhPNXK+Wr3BBBPEDDExMEDRtomUj81WlViLO'
        b'7zjJavG7mY5dy6F8Z/V4DAT3S0+vH1g/GhSv847v4o8Fh59OH0h/EJygC074IDipu6Aruyd0zMuvz67X7oGXUOclHAwZ9YrpykRmN2NtI8oOSf6cT3mF9i8b9YwecY6e'
        b'LiRmpGYiIkyIORsT8xS8NQZqRmbx1zWIml2fhprFGA128affIYoWOmATBGtQyLi3raxkJidQ2L6y8jmNpI6JYUSadRUaSDUNyo3j1nrLQKUMIWyiWi6rk6qIIUBULSLX'
        b'yDAk6H8fxzHxARBlVG8pl+L4JNw7O6hHbp5azE60uWOe3ujh4aNdNObuqc35ist3CHvszHGIfmzLcRB+bct3iPjGmecgIk2uwYRWC3bl2eUXwd0x+SxqHRiytmevAQeC'
        b'pokn/PflUjygWVOcAewKrpQj5Up5R9kVPDb1DDVESfnrHKhpf1IrwxSR4bfCaqM1Y/4vVCDhvvFbQbZsrVzdoJQpYgqUMikT/NSZ9MmneDx/67pMpmzR1KgaJRpVVa2k'
        b'TkYnoCiM4bf2hTJ1i1pG5yjlKvUZtnIhAn76E0TGX/W6UlRBg0LdkFGMuoyOyJQqZSoV6jCFemMjXa5Qy5QKWW29TCHMMHlR1chq0FMtUUgt5lNI1PC2sk5ML0Yd3oDy'
        b'LmtQKn5IOkuFrZfJFTI6U1EjWSsTZpjFZRRolC1rZS0yeVWtQqOoyVhYLirESKHf8lK1KE9arBRnZCpQg8kyypCOVBeTuV4iFdOLlBIpKkpWp8KaUx35rkLV1KBEJbcY'
        b'vqFUZ5SqlRLYJ8tY3KBSV0uqakmgTiZXt0hq6zJKUAryOdTyKvTbojHJbnhZ24yxw94pWo8IAonpCo0KfbjOBHk6bsaY+IwCmULRIqYLGpSo7MYGVJqiRUK+I9N/T0Yv'
        b'grfr1PIauqlBMQ22Vq7KKJPVyapRXJYMGT7rcbkRepDQEEcvkiHagSeq1SpcS9yk01PTiwqFGQtFRRJ5nWksAxFm5DF0ojaNM8CEGTmSDaYR6FWYUYpYAkJSZhphgAkz'
        b'siSK9YYmR22EX81bDUPWYxoWFWvqUQEIVAhPYHfgetxqTPMjYF5WZjGOk8mU1YjxoGDpM3k5ZaIFDahv9I1PxoJcUYtoDZejb/ZciaZRLcLfQRxsrVj/TX3YrN0twXHb'
        b'm1Uiflol4qdXIt5SJeKZSsRPViLetBLxFioRP1Ml4k2QjZ+hEvEzVyJhWiUSplciwVIlEphKJExWIsG0EgkWKpEwUyUSTJBNmKESCTNXInFaJRKnVyLRUiUSmUokTlYi'
        b'0bQSiRYqkThTJRJNkE2coRKJM1ciaVolkqZXIslSJZKYSiRNViLJtBJJFiqRNFMlkkyQTZqhEklmlZgciGg8KeWyagnDHxcpNbCvukFZjxhzgQazOgWpA+LGMmQbG14a'
        b'lYghI+6nUDUqZVW1jYhfKxAc8WK1UqbGKVD8WplEuRY1FHrNlmP1QyZixF2mRoUFSgtSQTKegSdqlajdVCryAcz1GBlbJ6+Xq+kIvegVZlSg5sbp1qJIRQ1OlwNP1NXJ'
        b'a5CMUtNyBV0mQXLRJEMp6QMcs5hMKJkWNinGRRUIC8QwInB2swh9fhQVOj1D/MwZ4i1mSKCzlBo1ip6ej8QnzlxgosUCk2bOkEQyFEkYuUzaHOklSD8hMLVsg9oYQJzI'
        b'GEwwTaoyJmM6IkuGxHGNCSA0o0KuQL2B+598B0e1IBAWvYhLm73Gm78i9iNRqZG0U8qr1ZhqqiW1CH+USCGVIGQUaxHZGntcrYQnahAR5Smk8iYxncPID9O3eLO3BLO3'
        b'RLO3JLO3ZLO3FLO3VLO3NPOvx5q/mmMTZ45OnDk+ceYIxSVZUFPoiKX6VlXpFQ3hpGJkKVKvK1mKMqhPM8UZWZmF+BLLX8N6lyW4mSo2cx2eED+TdvY0ieNn/rKZnvZD'
        b'kiFWaSmZmQhIniYCkqeLgGRLIiCZEQHJk9w42VQEJFsQAckziYBkE1afPIMISJ5ZjqVMq0TK9EqkWKpEClOJlMlKpJhWIsVCJVJmqkSKCbIpM1QiZeZKpE6rROr0SqRa'
        b'qkQqU4nUyUqkmlYi1UIlUmeqRKoJsqkzVCJ15kqkTatE2vRKpFmqRBpTibTJSqSZViLNQiXSZqpEmgmyaTNUIm3mSiAGOc1WiLVgLMRatBZi9eZCrImaEmtmMMRashhi'
        b'ZzQZYk1tg9iZjIZYs/roUcxRyuqlqo2Iy9Qjvq1qqGtCmkRG6cLFmSIirdQqpawaCUEFlnkWwfGWwQmWwYmWwUmWwcmWwSmWwamWwWkzVCcWM/T1Cni7sVotU9Eli0tK'
        b'9QocFuaqRhmyhxllclKYm0AN4tsEtEi2Ft7Gkn6K2lDDwPVag+Et3uwtIWOx3rliknma2yVuOih+OgiZOXXYKJaosV5Kl2pQcZJ6GRKjErVGhdVapjZ0vUShQeKFrpEx'
        b'ZIrEoSU3gNAkixwLd7mUZPvexBbKtyCULJc9PSFxMU22Do2Ub1qv8pKmrMbx+kZmwvEmYWwTTnqqxlkZxWeslTnYw7cIP3Ip/TyZMg8/8rEXkadqrJOrlXj9rpDFOAex'
        b'D03vGCwijkHGh7YZx2UYHINC7Bj01uZO8CmPmDH3iM+tuF6O2twvbCkP3wlurMsC1jdrWZSToE3WtaB93Zc1rAQPn7Ycxj2I3Y1C8MpCFV4X1xYNznApWal1MnuLCm79'
        b'H/QP1gptxm0zq6oaNKh+ippxxyxERIwdI2mU1X3qzngHsf/4W59sRFb1SFfB/mCasaTQoJAjVoaS4JWp41ysUynLUPCr2whQXs+oSA21Chld2lBXF5OLeJxCVNCCPTaT'
        b'r5NcM+OZggqayYY9c5gfq+QqDQPAcabvzChehB2JjMXAfCirXFRaVVsHbyNqqkNajulrRpasTlYjxRVhgno3zmQ4Xm9xZRhaglgQWMWU6ZmFwQykGTVLb0xOur30ZiRR'
        b'/rEBiRKj4aomhoa+BPK5OjlKQEJyRXUDLaIzlWoDKnpIngLnnALEyeItJYuflizBUrKEackSLSVLnJYsyVKypGnJki0lS56WLMVSspRpyVItJUNaS0lpWRwCFDAdg7Vn'
        b'GQHGTwOiF7pIhjiwwbdLa8T0pG8XARlaNjhbxTS2AAx2POPEnexGujCqMCNHo1hPtk7IlDWI5bVgNoXhWeV0YhojuKsNSbCT2RJcTzdMlIUCMyqIgYErrqyX4EgjiViK'
        b'MZLKTNnin5TNciRDQk/IZjmSIaknZLMcyZDYE7JZjmRI7gnZLEcyJPiEbJYjGZJ8QjbLkThb2pOyWY4k3R37xP62HEsyPplQZqaUuCeSygyxJOMTiWWGWJLxieQyQyzJ'
        b'+ESCmSGWZHwiycwQSzI+kWhmiCUZn0g2M8SSjE8knBliyYh/IuWg2FI1vF21HomuZiR81UTVbZbJVbKMHCTiJ7kfYocSRZ0EeytV6yS1SlRqjQylUMiwmjXpvtRLTszw'
        b'MjXV2NFmZHIGWYqiMOedFMh0RKaihVGx8QwhYsZFcjUSjTIp0kAk6inRU/jw9MyTnHxqnLIOXlPp1QSzmFwyX1StRlqJ0VAjkkRE9B2LVoW+pnppjkQ/kjRYKa8m6ng9'
        b'FvBqmRw1i9roec5DurNaXi1fLzHl/hXEsDR6pE3VDMYcNZmZNFWTcmSMrSKTr8VRhajX8FSbitFsZlbUTL3NCG/0ZUmdpn69rNbgGidCkGhxeJ1NsXK5ZaUYL7JtMVEc'
        b'b+P4VINiHGyiGKeMudPmirGXy+xv4ifV4hTfSa14FnrA1o3goKqwGO4G1wNjiHoMOwqsKPe1XHvQwzZTju0NyjGfjZRjgblyTNRhPvpnh/9J2ejphv9hhfk875wVk9UG'
        b'/SeltTytg9aNrJu3MayFqeDi3ZlS6x2U1Oa87Tn9srYKPoHaIai9CdSKQB0Q1NEEak2gTgjqbAK1IVAXBHU1gdoSqBuCCkygdgTqjqAeJlB7jG81W+q5w7rCwayebt/z'
        b'z+a81zlbk5oHatn6unOl3iZ1dzRvPfTPFv1jVRta0coYMi/d55yNoXRpkJZZ6oe39TmjL1hJfU2+4CQNRvE8rTXZ+OdK4v122FQ4I5gLqps/qpuLEQu38wEGw0W/ddBR'
        b'61TNk87aYW0s0XUj36ZaGDJunY332iwoXfZtjC1t8mcA0ww3ZLa8mqU4w1MuxuSNba1P8XoY5bM4hJfbEqtGaP8pRuJT3A+f4mWek8mVNYbkSryGUrkGJ8Et/SneXPcp'
        b'plSh1bitRNqEGKyyUi4dt6lCbE6hxkFHCTOSKuuQnqquHbeu0iAOoKjaOG6NF7XLJXX6BS921XKkmlbWI+5TW1xlbTIU8KfIyqwtlGGlpek+XLKhj4U6m6u1Qo3HbOfj'
        b'V9uSRWOITNtsjYvGbMiiMWuTRWM2JsvDrLfY6BeNTYGarsD8Cm+pM2tZ/JfHVEXeIlOR3crG/pCThSBVMvG0LNMA6ci6ktTTk82Yrt+njDgodp/pN0Lr21OiUE8rAf9F'
        b'ZCHGpzawXaGYzsT5EYusosnqWVrTSCNBkUJL5TVytWo6Xno0jD1oGQsm2jIGxkmi78Eh6ftwMCeddLqQ/GIUFsUUGmL1iKks44LFKhZoSByK6bJaJOLQCJHRKs3aOpm0'
        b'BtXnB5XCrMBhbHFUEi1BRaB3Bn+6rgGJW6WYzlPT9Rpkka2VWSxFoq/8Wpm6WYYnyekIqaxaoqlTC8k29dSZ+0I/ZNLpBfoQXYW9rBHGuVkT76xwplIMwy3dQK0qY2fi'
        b'XfENSjqCWemzHt5WtsjqZixIv1AtnRiTWPFCxTA0ouc+EbIaMZ0UFxtNp8TFzliMyXhPp3PwC01ecHHVcgUaNQhHeqNMghCLVMia8URxU7I4URwXKZzeVN+zMNqe2XmV'
        b'y3Kp+w9qPkU1rim86JBFafB6Ov81cC9sLwLnF0NtHuwsiIFti/Fy6dxCIWyPLhaBXXBP4ZJccCG3uKgor2gu6GNRsBv02zeA7X6k2H0C+9jX2LEUtXhNnWdkAaXBC/wr'
        b'4BBstVgu3A3bCmEn7AfbokCbWeGo5B0b7anIhaTcSpXNqm0sGi/FjbaPiKI04RTefFULjxr24+LNuLliUWQ+Kh9cgzvBRS6VvIqvik8mu4pJKdUtVmGelBdF0Wvs/5Sw'
        b'itLgHYBeYCd8kWAHLsE9UzCEWlRyezTGskO4zAQ5cENpB664g53yhNebuap+VNBbVsLNe950ALFfvW2/8A8nzuwrG3K0G1oU0+38qUPq3QNHrObb60LzQlbt9Hl/qeBv'
        b'z//1jT+7f3R3m5wr/MnxxftZf/zp5x1fflP0xx2jLo/iPzz6OCz4390e7hecW9qRfzny5PqldY796w723RsuLGeX7n7h5s5PTsFd91NCmt86l5m7v/lIdoXLN77Zl5rs'
        b'HC6f2vjccNS6h1+tev3Pr/CXOFmfdnr0ZrRf6ByhPVka7qGBL4L2yS39HMoplAMORFW7sx+jBqbgwFy4DbSXkD4HL+Xou51F+cAXuS32RWRjXGwN3w5vgj6aKiwyrEJ3'
        b'B61c6wT4Iiklr9oDlYH0u1MepIuZ7mVRHoFcO7gDtukX4sJXwaUoUUQu0MK9IjbFB4fZIomSLFFfB7tAKypDDE/DE/p+RX3qCi5yYDs4CzrJOt8GcMQ2SiyEu2AvPBxN'
        b'oRLOsxOUC5ntSV3wPLgG2uEehOl2eMTYkXzKtYkDXg+KeYzXXsOe1Y64vkgbjfEp16OqJwJUU7iTL/bSkG0kQqAFuGlQQZFinAqR7p4onIqGx9xVPAe5gFReDm8ocbJO'
        b'cCEFe37RV0Xom+AQB2Ja20Gws1slMnwVnvec1IF9wDAX4XwTnBXa/gP7X7GOMHXvK9lD52IQxeabAHUUs0C5yYoKxBv/HMaCRV3c+870QzePblVP+r4XRt3CBwPvuUV9'
        b'6BMyEpo76pM3IsgbC4pCaZ2YNGn7toy6hQ263MPbWVCaRaM+uSOC3LFA4emAgYDRwDiU1BEl7VLjvVY4qbG4lFGf1BFB6lhQ5HHx4NoHgSm6wJTRwLRpGYxl54z6LBoR'
        b'LHoUnoSRDBkLicG/gWOBwTjPWHBoF/d9s20zDsyK6Ab8aMSP5/ADn4GgVOEHVrmUaupJi6axq32N/s9k7fQMrfopzjIbPf6OmvWbEisWq4r1FYWfT7uxuJ8fi9TyDI7Z'
        b'5gCWgaP7EY7+PLWOmv5XStnUCFnFQta4XeWkGoVsPNwWxMaj9TtEZ9dJ6tdKJXNNKmIAubAM5ET1lD3wF93zZ5Y9f6uXcfqCDfpQBJKdUlGDom6j8AxrnCNtqPqH8K5l'
        b'8LatNOpd09FWvmTe9AaMBSgJ2TeHMe6rPFzJ4DuLwZcp0AK6/0z7OlWa62Y/HFlP8+aNu+cfx6ArfKJ2969C3KbSoEz9cJR9zNr32cPPMgh7Z0lUMqNu9q9D0KCn/XAE'
        b'/VES5T6cgCAWPKN+90+iWM2gaF2p1wB/OIY07nVjE64+vFqP6Ywa5D+JqX442VeaKJk/HNtg3OGTNCq+5y/W0+j3qKkzYG3cWrQGPQ6w9TubDNur/7X7mqadOGNxX9OZ'
        b'ge/YKrxz1X9EjLdL4/17zD5UvKdpsXvhK78dLi9jPRfLqeFTib/k/3jfeiGjJ80Cg3AQCeqztiXM/K6plM+DQ4+xZAHHkC612yjnO6NqwS0zOQ+GXWbc7GxViZlKZWWL'
        b's4mQIRAiubHugjfJ5dtQXr49iX1ze+eOekaeKR0SPIjL1MVljoqydJ5ZI85Z03Y1WxJ1zKZmLN4YingFU8S0D4exJvcGfZVn83R7gwjr6OYHUgN20Ryh7biVnrUxG4D4'
        b'KrVSJlOPWzc2qNTYqhvnVsnVG8etmDQbx/lNEuJIsatCtmVDPeNg4aglNeO8BjS4lVV2Jp3taOjsDkxpXMtHliHqc9BvVLXWOmnZWltMjVpnLUdro7WqdiRUaYeo0tFI'
        b'lfaEKu1MqNLehP7sttjrqXIK1JQqv/olz4LjJFMqVSHLGJt3UtlazKTQ/1X6BbO0jCxN+AG+E2LZE7NcQtdqamQm3grUrio5svZpZkMVdjyoZGoxXYKG6bRyMLesx7Oq'
        b'8vrGBiV2shiyVUkUyHLHWZHVr5RVqes20ms34gzTCpE0SeR1EvxJYuji5dYqMa6pHPvHEbPQF6l3FuAyp5WBitao5IoagpGxGDqSdHnkD2iRHH1ta7E3cDru09JHqCXK'
        b'GvQNqYER4/w09virsOGtek6DW3etUlK1XqZWCdN/uD+LofZ0OtNMotMryRqH1TNlw19Op8mWp5Xfu/FpxlKYwZVOl5JfeqV+Ge6M6Q2DMJ3G8xWoq4ifZaXpMtwZ8+Jh'
        b'm04vQE96ZYlSPXM6ZmCjpEyAfCOazistESXEJSfTK/EcxYy5GW6QTi/LLBPlZdMr9RP/q6NWmm7rmvnjk0wEe5OYFxoXZLqZYMbsiO2gxqxFQwMNV1WVUt6o1otvTKf4'
        b'hBMytjLrVA2IfmVSi44wRE44NRaedeTYRdLZYjqb8YaRIRpUqpbU1+NdxoqgGf1iZDAgwkIINOqHllRODn6UoGZtliMhLduAelw/4KaXg/+KG9QyZpiQwS9T1zZIESep'
        b'0dQjQkO4SNajAYgGjQy1TpWMbkC6j8VymCrhQUPcfCqmmnKVCUpiOgcxNQNDsliK6bDDTkFE6vhYy6o6VGHmREuVzHLONfpDLRuqCObMlOjsWrW6UZUeE9Pc3Myc0yWW'
        b'ymKkijrZhob6GMY0iJE0NsbIUedvENeq6+uCYwxFxMTFxibEx8fFZMelxsYlJsYmpiYkxsUmpSSkzV1T+dQuONdiDVYgwNkmcFZVKMwXiYvxLuUocCaaokJKYbcrrxZe'
        b'9iLH3cET5V4JFLgOblFUHBUHekuJJ6vEhhycRIVnrYn+aF4NpcHHWM2Dl3ILDIrGEqjFh7Hli5Z6gO340IKlEXi7/zNQi3+Q/gH2gks28AA4AY5qsBJZGoCUlatwN9gP'
        b'rxOvhhXFg71se3AF3CZHR4KevCXwqhh2FuThoxFQ6Z7J+Lg3NlKFTnLhzWfhoAbbvU30bHi1AHYUlcOuxkJhXbVpBRdDbTHK3VFQ3ogeJYX58ACXgrvAdjt4QgqGNPjY'
        b'JNAPu+EbdmJhPrgN+mwpm6VB+WzYBy6HkGh4Ex5WwKt5KD+L4oAesB8cYoGtoG+2Bqtc8DS4BA/YQW2MGLahr0aDM0mgLx92QC2LohfxuAJ4RiNACRPg6+CaAByEV2Mi'
        b'WRQ7l5Vcu4w07q2FfDzruGZZ2Jq6vXn2lIZsRr8I29NUDvAAfI358kpP61XsRfwE0jbwvEsJjnRwECPcXysEx63h5Si4l0N5buSA80ALzuv7HJwCHXZiVARqujzcKhzK'
        b'Hd7JgTe4TvDWs/L60Rieahil/Lb1l/UjBY7bY52pkd6D7N+UfvifK1a17M8rbGwV75+/9sOfsTpaH+115Ly5sP7e15pvj3ztP3fNVodN4pXan0oPbtnBsv7m+OnghL9G'
        b'HDzWe3/XH3b8/tvXDo0WPu/z8Nnxn9r026VcX+h2bfO3v/hr1jXli0caHpXtP6tccurswhvvLm1su33W2f1sdtnZw4q3HFjlrWl/bWlbsrD/4/6PG986l9lfnf1OWqdK'
        b'sdnPd+L23wpXftf70b9vn6Be+I79p/GoiO1SIZ84CBty4KtmXkbQBk9jT2O1POUxPkwRXIq2MxKrmcctCg7Aywk8uKcZbCfnXcD2FngauxtNfY29EdjdCLVSoowjrfrF'
        b'bOJyM9HEpWrG47YHnGQS3QSHQHtUsSgvr6ggGnYKWZQHOAn3w9vcePAiOEIcivA1OrkgOiIXYcOirOFxV3COvbEqSuj8zxweaNFThx9mB9UZTxSwlUillYzK1+JmVMEn'
        b'gUT9/51e/S+0pXzofl6/+vTmgc2j3kld/DE3754YnVvkiFv8mDiuK6dnnk4QxbjqUvY9P+oW0q9+EJ6uC08fXqILn3vPbS7xrC24W6MLLRr1KR4RFI8FCbv4Xc3dTmPC'
        b'RBTYonMOG5ub1cUf8UzXOWeMhUQi4EYddrtFoFBTt+OYMM6Qjg5BIU23w0M377EI8aByiDWIDyNM0wlCx0QJQ5lDWYMV6H2uThA55uF9z0PYs6qLM+YsOOTY7fjAWahz'
        b'Fg4GDypHneMfOKfpnNOGw953zjSxYFwYC+YkZVjjewo/TuPHIH6cwY+z+IE1cOV5/Lgwg81j0hm43ddM/tGT55Qor2NLyFI3CLExlIVi//5X7OmzwT6+b4in7/On9vfh'
        b'GfXT/BTqul0mmyO0GbeX4tXQepVx3IExBAyvfEk9+cUnqcnGbfQrVqpk43ZYbUPKMl7PyjSCsf5VtiYyydkgk3Zj68jKknV0iJwFiywhPJ3MIgf22mhdkKWED/QlBzhX'
        b'OxP7yNbMPrIj9pGtiX1kZ2IJ2W6x09tHU6BmE8t7rJ5sH0mMS1Jo5iDHH2AFLMT7ypjUNFJFUCciBR+pVxLTI7CxChZN1ygbNI0oFlkekumivaF+rVwhMSh7kUgPjCRa'
        b'CqOkYB+TcSE9RtDoGJlWEnaU/D+D7v/PBp3pEE3HHcVAjB7b7zHszMY0k58BGQqwqN2u/J618DN+juEZzHf0bEIPYwwERQP25ymJCaCwrNg3N2ANXF4vqZvBhFj5hN0A'
        b'yDCzvB9gRowxd2PwXdvQsB7jiyFiukhPXRLyTjesXYc6nm6wbI0gAkEGZWpybJzepYoJAVnDuLiVkzsFZkTCyFzT6XKVRlJXR0YGIpymBnmVcTSuNNlo8ESbWs+czbuB'
        b'7GleaboZ4XutXpx9iuVrtuT9/4DhmiVrltXoFyz+P+P1/4DxmpAcG5+aGpuQkJiQlJCcnBRn0XjFf0+2aPnTLFqaWVQyWIUPv59o4s5fY9+c5k1p8EmcYAfSu/sK8org'
        b'rui8QgU4azBQLRmlL4DXbRJhB3hFg5cqrLOjsUVqYo2CO/C2PbgO2zQpWFe/Bl5KLxDnFyGdPw/bEhQ4OmPRoB2224DTsG2RZgFG6wg8CE+qSopKmHP+5HiVA/rOM7AL'
        b'ZdkDtchCtUUGHSoVvd8oXQWOgsPgFRsKnIMH7YqRvTlIlrLK54Db8DWNKh925hWVFOAjAmO5lFcWB1k9O+AwsfrgdrgXXlFFFsHdEWQZQ2WMOA9ciGBRs2p4PKEnueAh'
        b'fMl6O3gd7F5qDTtFFYXFyG5lU64JHDAAXy7VRKAUMjC4GbXH5HIXfDbwa0vx4fNxoJ0Hj8ELG+AReIrcBTEnDXTpkcpL8YsW4rPsBfAVDrwFuuF+0l19K/CtBn9mcag1'
        b'dYpZkRQ5Lj97M7xix6fgbW+qjCpbAPo0qYzpdAnctMN9AS+AQdSk3fB6LrLeO+E++Bq26NvBOfRWCHfnYpN2lbf1IngO3CCGNrwN9sAheBWFjq2k8qg8cL6KOZpf67o8'
        b'AUHvrMC+DdibxRzlfxG87IcP7EeUc5aKoWLgSXit7s9///vfZ6/G9PW7cqf5awqX8myYRT3fZWBrPTXGnl5j/3F+AEV6FyOUgpupU+8LyY1ehm/niMkvR2SRCztKI4SI'
        b'OHL1t3G0lCDjElwjTclXOKxGrXiJbN8DJ+OqS+GBhHwOfB10Uix4Hpn68FotWdeE6PQNeM0OdRfurKUM4YBjXEw71qSpzJsJXIR7uRRoLbdZsQl2kesc4MlE0DfpVVgS'
        b'AQ+Uwlcpa70bQe9DmOfOd5yPeoLMKHWCffB1Vb6opCgGW8zFjBNhE9xBCWEPD7w6G+4jg2ctosuuKOZkMiGfskO43oxgw6sNYDu5YkJaX8JuDG1zoBolbr9Y/vdF+5nF'
        b'WmgsnAB98KreecQs00LkBtti4IvpJUVLIvRFmq6GgsfAaXvYFSAmR6KBQda6KHFedCSL4oM9bB/QHQOugIskTgS3wYsFxLhmK0EvuMVKRQ16TsghsWWoiXaaZK1JjQFX'
        b'QT+5UgHeWVZmyLgWvsJKDU5jHDNtjYvMqlkABlE1WdXytwb+k6VqQkba6Ub2yaVzSmCs82vHSsKLDp8ShgrCcr7Leus7+5z2/LYfdS2zjqyRZDT9CMz7Xd8nn90fOAOz'
        b'T/zot5ua//Ry35e9m11y7r7IrXa/3Bf8+w+WlRdN/Cww/Z5bU8XlpVf3PTy2PWBiZYO1/N7rD2q8s63+fv2bY1khbY0feH3jBl4oagy83eP8a25J0Vb74MpFpR3bNW/9'
        b'4Rcfal8KL4prfLvTqUjbKxiW/P3R3eYfP1RfLBn52DM/9YuclnX0r33SfCsLYw8Nfng1fKnb+oN31cue/+Rx6YvXyqR773T9R2ZahNx9T1nNqYr33k2oWaj4S8oh9WBL'
        b'n5f9XzYvmd+4+4j7gZjH7+z6yYvs5mda3jp3f9lo/Hs1TQF/Crp+dTy8JP72n3K/+Xnlp7uXBB38+LO9c9IuBPtLo+oEm8c7gu8t+fmrF5t07g84fe9+61L+o7/K/jT6'
        b's0fPrr4c2bnsjV/8PuP1B59f+Mn+0XOKS5d53614vuBHv7w+evPe3woOnE1qOas8cfyZvHd8f/WLWaXLlZqRQaEDc1rpqw6IWbbHFIBD8A2zRWfV8HwaWYEFdoNzDRad'
        b'Qe7wIBWFfUE+DcSF4wf3gssGVxB8Few3WXqGWFAHOXY92hFoC8QiMORtXDXmtIxTlwq7mFVn58HZoKhIvGgsmoInnCmbFWxwUvwMOVUyA57mRYmx0IjGJLibDU/DAyLY'
        b'VvcYM6yq5X4FhZF8ir26ejYrxRrcIS4j/4RUcK6wKJoNd4BuilvAQtR+EmwnuMCXV8ajIWVYJ8Z/no3kTGu4F+wg88OItZ3Ln1xRpob7TReVqXgOi8F5svSssRLJnWOI'
        b'40xOJZvNI1eB3Y+xOHJs8VfhcSnC0o/43U6Di5QL7OKAoSJ4kDla/hbC6KDByRUGT1LW2MkVuljo/q92cs3s/cKcnqgWW7dacoE5YjfLpKHf4mnmf5mMIK6wOWzGFbbF'
        b'jvIJ6V84mIgPsx/1TuviM16v2aOeEaNuwsHsB9HzdNHz7gbqohfcc1tA3F6Zdwt1oYtHfZaMCJaMBYkZtxeTbc6op3DULXKw7IFovk40/26cTpR9zy2bZMu6u1oXunTU'
        b'p3REUDo2Ow+7xlJ1zmljEdgPtlnnHGriOQuPwq459Pa8zjnkoZt/j7R/wX23iIe+EYOCUV9xV/ZDT19mNdyN4GHpLaEuVH+HBsqpz4Vdepl708dS0rtyRnwT7gkSH+mD'
        b'OkHiQ3+63+PIygf+MTr/mCHOqH9il+2Ym0dPpM4t5IzbYMUD0RydaM5w1ago6268TpQzKlz0duA9YQH5ZuHbLbrQFaM+FSOCig9TM24supvz9rI3S0Znl42mluNqJeqc'
        b'k7AvLykDfy9OJ4h/FBh62nvAu8txzM3zUHp3ej/3AR2no+PuucWNhSYMSXShKV3FY54+9zzFIwHiIe51m8s2w3NHPPK7OBitkAc+kTr0v1vkWEDQgwCxLkA8qNIFJHQt'
        b'eujp05PSn6bzFY16iodC73mmfBgQPhJROBpQNOJV9MjTt6emvwYlRwWPRcX0WPVb3fOKGPP277ca5A043vMWjwlFCMo77PgoInqo7O5aXUBe16Kx6ISu7AeCEJ0gpL9U'
        b'JxCOOXv22Oicg/TOxrD3neNM/ItujH8Ru+CVN/DjJn7cwg+8AUr5OmXwL/5A1+JUwsefmupoNPoaf44eM9J6hdHfiM8Zfs6WxZITf6Oc9SV5Pq2/cZCfSg3bZXI4VYYD'
        b'CPCf8Z6oFsrcN3iI0lppbbRcclMUW2tP7iFx0LL090Xx2FSbcUPJZj7xA/JM/IB8E48fbwtf7wecAp35VOLpRocjY3Q8yGfu5ooNo7zr2M9TZQT6hZK5hyvWI7MyclM8'
        b'c6sUuFRlowKdzXCv9XMciuPISgVvlDKTRuejwI5S0FkGO8uLlsxaAl9bDF8rd0iOjUXs3ZMDthXBPuYWt6OR8BTSUk6Xws6ypFi4KxFp+9bPsWA/OJJM9BF46Xl4x1AU'
        b'i+JFNi9ngcO+QEt04VSkvw3AjmbmcihqNpI0u8lEn1z6HHwFnnQAw4iZhVFeBZuIRmQHh7cUiGMT45PYFH9LArzGAi9HgbNkxi4XbIX7o/LhDXBWf6uS/k6lhWC3PL59'
        b'G1eFLAxqX8+dztKfFiPl50ONa8ol/i7nPcusT3xn+8Ld3l/sys/5dZfb2c98PQtWtcx/PvtH867sfDXyYdHCkJ/+/LOff7ah/oWyPmdVK33nYh/HS1t+3ubSX2KK079s'
        b'v96+4dcdn/Cks8sbF4SFxKic0tufO8YL/Dws+efv/i4h6rXeRfkf/GZZFW+/okul6v3phjesngno/GDRK50ev3E88NkLYVX7NZsbmr/ky2PH/tRbcfW531a9/3bL/U1f'
        b'SD/4esinZnVt5NyNP/7a9frplV+0yf89/N5fZy37vHLZ0b/9edjnK4lzRNryV65cdFledVFun3G2M8b3nvuO92r+mLNuYsupuf7pi0auCpuvu/7yo+4M733vXr7TuqjY'
        b'qem+7sz1vd/cyd1me+HORx8lXS+bfajsD//+R46g4aPUFumDPxR9HSN0fYyHcDO8zkWaxO7VsD3GimKD46zyeniGXFURCQZykKCPh71I1jNyflUmI1FfAa/DHjM5L8ph'
        b'h29KYxaBHYHH50xdNg4GwYBRynssZlSlO6B7M3wD9E1bn18Nr61j5sJugzagBR3gWEFxNLJe9sSAs1zKEdzhVMLBSKLfgKsr5sP2AmTedpNLtLgBLHAc9nkyN9rsgy/6'
        b'RBUgKnxx8gPkRpsuIVFY1PBAUEsMuYfL9BIueKSE6BfgLLgQVVAIhotNtoTgebQLXN9MeJSZZ9sNtPBAgX5zB9LnRGEkkes6DjgPbwQTnY9e4VJQiGyiAxanALHK5wqv'
        b'MZ/cjUyXK/CMFG/1MFnD7xTAedYf7mYuD+tC9lnfPHCiQCwyU/qaVEwHDSOd7NLkvB44J6hjb4R3NpBYVgDYj+8NA4eX470C+nvDnOAV5hjygZA5BaY3oMwHN9gbwNYy'
        b'0l6zIrHRjypbkoc4DuhCNbzGboCnwSmh63+j+uRqUJ+mX3U1blXJXHNlunyPgRBt6SijLU0sd6A8Zx2q667bp+jiYLWkpl/Su24w8r5b0pgv3Zfem96VPeYX2FfQW9C1'
        b'cMwnoHvBI9+AvtTeVAye1ZfXm0fAXQvG3Lx6Eh/4Rut8o++5RY/5zuoPxIkm2LSP65jAZ4KDfh8JvA4VdRdN8FB4gk+5+/Vkduc/EITrBOETVhhmrYcdKukumbDBEFtj'
        b'qjCdIGzCDsE+t6fcvXo4ffa99iOhyaNeKaOC1AkHnNiRcveecMIhZxxywSFXHHLDIQEOueOQBwqRT3jiNy/8VtxdPOGNC/fBhdv2S7GeOEcXPWckdK7Oa+6oYN6EL07s'
        b'hxLrMfbH7wEo+T1BWu+Cfh65EG3DKJ066pc2MQtH0iQyBUVyTtsP2A8uH6WTR/1SJgJxZBCKnAjGoRCMAG6XUPwWhuB783oyJ8LxW4ThTYjfIg1vUfgtmhQv7MnuK+ot'
        b'mhBhkBjXMQaHYnEoDoficSgBhxJxKAmHknEoBYdScSgNh9JxKAOHZuPQHByai0Kfz0OhLv5EFovy9u3iPXJ2P2Tfbd+7ejB51D/+vnOCHtBT2re8d3l/zaBkYN2DsBRd'
        b'WMqof+p957SPA0K7csYE3ocKuwsH3PqXveL7vkA0waFmhT3y9D+0qXtTfxJSsR94xuo8Y4e8htNGPReOOC80UcYcGWXsPKFqZvZONc5TqSVK9TgHUfTTaV6OBs1ritL1'
        b'MWW+1JUZKxdY+tvh/oYvdXBgsaLx7XDRT7ve9WW+mLpol8b5X1sHXS1kf/ubaQ5d5lwAtWGXrn5irE7vr1bK1BqlgsTV0xI872ri/v5Bc5b0etlGFSqnUSlT4V0XjF9d'
        b'P1GgMk6W6p3sluYap86j1jGzExidtRvVMgvzAGb6orUFfZHc7gIvC+F5gAxgsAeJ0stwL7jyDBIOl8Fp+Co4twRoeZQX2MrZBNtXEMUMnJplB67Vw31ISRZT4np4mfh0'
        b'58ADxUiXtH4OtIOX5jwjQga1WMyhBKCNA86ANjuihW6u5eh107iChpoAilm/dAMJ1hMkLzy/BbRbUVxwkgUORXPGWZXkGmBPsHs+9oKBPfCK3hMWw2U8ZM+8MJ/RLZ9b'
        b'xmiXWLeEu4huuTgMnDK61l5KZqWWw/PMlaY3XPNLGXWUDTqz/Vl+sL+GfAn0LgG34D6COidzDrzD2pQLjstDMn/NUl1G8W2pjQe65tiy45xzasJeuPVHm9svLa9o4azk'
        b'dWeO+WWGHfvZ9rG2nWMPf7M3zPm1t20PV780Ebbxo1W/s53D9Tra+u2G8o9+vPTQUC/rvA29pv/NltKrHYXbL992FUQtsTpy63HfuY2ZA7knrZa0l5Wojv3h8Bt/uPbj'
        b'Yqvgw18l+tJHKgsb3l5mf2v2x7dcbrb9OcjtwZbfhM3afeuWwy6lR8bB5/fM0W585P3RO76LmtPrJbw/fG6z53hk9PJP9Ff75VbLp64GAoeeiefAnevAcWadz5nnfZAy'
        b'gZeyHZToLwhxAVqiA8Lts+DhKHERGzXXILgBtrMKpJC5xHTD+g3g9nqkn2ElI0/EpuxkbNgPL4A3GFXvArwKjuqdNGtKp7lp4C3QQ/QweAAp74dfsJ6maNnB00LrH6wG'
        b'WBvVAKPwl6gq8WA1YWh6CBH+jyhG+C91IhwdieJQ4enigeIHIam6kNQPQtK7C7sW9HiOzQrsa+ptGglLHuYMl47OyuzKHZsVPbhBNysFhcIiT9cN1A0lDFuNhs3vWtgT'
        b'sbdkwooKzZiwR6U9CEnUhSQ+CEnXhaR/EDJbX56Pf4+kNwypEF4+ffxe/sismCG3oar3vdLHvGb1W+m8Ih54xem84oYi7ntlYBCv1/GBV4zOK2aI/75XyoQVl/boykUq'
        b'QXhCv5T5uC4sazgcPfTfd6JC5yCJ7+XfZf8P7Xf4wlwI6NvsE9P9DgudnvIulBMo4xnWOLdRoq41uzLLaMziXTsHePors/CJF/guZnzhIN94bZbRQv5XXJv1Kw7Lwtqa'
        b'SWGA+bJK0oRDdXWmYuGHH9uAK5tO51XTkTgUSSNhqmJmcTHDl23Ah9/gSc1IcYu8MTKafEgveZSW50RV+MhwqXEmVqKsqpU3ycR0CZ44bparZEbpQsogFSDJJXR1Qx0S'
        b'5d8jKqZfRW1drBGicJY9vBGVixjI4lxkceQXFYIzZbngQjncBbXRYmQM5MKXrBpXwq1EsNi75hQgdpNfJIZtyCorQ6Z9e8yS3EJ4CXaKIvDpjwXwmhU4CC8sIXNLy+ER'
        b'0FO5EO4D57AnmuLUscB2PjzETI2dXAOPRSHMNlCwI3bDs81kDgRPjYH9USULXdkUaykFDzeUyOOtV7JUv0WRf8+GnUsu24JY59cL7q0TdAcFLTz2X2yrF+armzzUdo7e'
        b'F/qzbg7zVv14z+9KWsZ+Yhu3Lv6TDd/88Ze//Knozov16yb2/Mfcatk22asNs4JaI9W/43EqOi9VBJ/d+0JzVcMvK27+4YH7+0f2bf/jji9v/v63ghe+WhU/dPlA/tjg'
        b'4O23dVuLwS67MUcquaMn+rd8zb/91qd6w5vvev3qsC0958Cz8863NTr+beTuW+v+7cqOs/ca7Hf0/eK939e/3ZmzZvevTotfuiEq/+S49yfAes7Xf3npQemZ327+sjbw'
        b'7RdtCgNh8ILlbjm/+88fPWjMvrGJSvs47UBBmdCJ4d+3AuApZGK+TDoIqVQpLHBxUTmxBiPBVbAdm6fYYswLgcfw7ant7M3g+nzGCEbWoBW8Cl9txstJozNi2JQNOM0G'
        b'rwSBVmJCu4HD8DIpoA1Z+uANKb+Y7ReAJAcxwQ8irQEVj+LEebAtvBwlsYNDbHgbnoXbiMlYDc6GFkSD3SVI9jjDo2IWZTefDXs2Mqjz4Ulkr6L8MSVIgIDXovhb2JFB'
        b'BURwJYNt9liGC8XIEj0OXyd1c4rl1MCX4XEigcCr8BrYxoguJLfAEDyOZddi8Bqpm18gOB0Vg+faRQq4XSxkI7HSxwE7wQFwk3xdDlCzEeM8ppiH6n2EP5vtOZ8xhFeh'
        b'0joKkBDD5B2YyKdsBGwwsAoeYHI+Nx+7OJhGqYSv87PYXnBHJjPPcQIcjYTD9cz120YbGuyqZW6S60cW+G0GLx5VNZcPBtnRxS1Cu3/U/rWjzKYPGNnHxSO/xcHIxPEr'
        b'kXp8FiP18p0pgcehlO6UQ3O75/aH3HcL/9AncCTIsAvdzZ3Ezeme0y+47xY2GH8p/Uz6kPR+VIZZMi8/bIAecezi6R3g+2Y/cIvQuUUMetx3i33oE9gfMsgZXDXqk45s'
        b'47AofN/Xqfpe2x5uj3TMyxfn7S8bTHzfKxaZQuGJjwSeh/K68w4UPPL170vpTcH7+AZD7vvGjCFRad1r3S846jillIf+gf1Bp8MHwk9HD0QPqofKRoPSh7Pv+2feXTrm'
        b'F9CX25vbX3a0+BsOFZDFGvHP/Bx/5iP/TBT8VoUPKfpRqutCd96P3XkLA2wYOWnDyMnHMwjLqa2PvcdGM4qRn1YsfC2eWdP/3WBBYXf1JiQ8vfC62Ke+BPUgP4w6ZRfH'
        b'ETIHN41zFpYvLSaXUynlGHfrYv2fkMf8sNE/tynnAePNlNKGqspKsm1/3LpR2dAoU6o3/pCDAfBWSLIKmLjniblI1AVSZ6Hgf2S6DOv3U2fKJhsfX8zXYjwSCyOoqmeR'
        b'g9o+57IdnL+wphzdBzhnVHczdCtWPQwIHEwbyXr2MYfluIb1aGHO2JKlX3OCHcK+5GHABBcFP89nUT5BD51FY4Lkxzy2T6o2/3M+5R340Dl6TJCEIN4p2jwECQh76Bw3'
        b'JpiHIAGZLG0xvpeOfugcNSaIQSCvOG3uJCQNQzIIxHPWQ+dIBuKZoV2EIL7BD53FTEG+qKCCr6xZDgtYX/AR4r2lA6rLCW+6vZPw0J8+43Yj+M2Ed6QY+TLWoyXlY8tX'
        b'fcMROWSxMPZlCHsc/uJZFq5x8OXSN0Pfsbo766FvQK+6J/IyB5VSqlu2QieR4QJqWEj/rcSrtjklLIf4Lyj8xOWgCC4Of7OWneSQw/qSws+vFCxvB/8vkjFKwfcdAr5h'
        b'ezhEfcmhHGd9jkOTZz7ng24/VR5iwCpHR9gVzKEc/NlwQOFE7MYUcB522oFBNZZNdnj9yWK86sQtyy+eGwxvzvlfvJB62rWq03dMWxUTmzgLvARv4Bv0Aik4xA+Eu3I1'
        b'zN4JsJddIAZDsUkUFQd7uPAa67kiFrF6w5eCV6Py8TxFCOicnKqAJ7hkLiMdvIYXaOVFY1sogYvvlaasQTs7PwnulaeUBbFVeOz/7d4wc6d1XHs3i3P+pXurO4QdK97r'
        b'+WL+6vPDmgvVOz7ln616q+wQ2A9uH7bJcwj3SIrOPbX7cqzgclP8qVh1fO62960SGk9xqPpKF3tpnZDH6BI3wT7QHcWsCKDqg8ghMr4FjKG2D+yGvUaxlgxP6yVbD7hO'
        b'jMUiO0/jgoEk0IbXDIiiVxChKIVvgC6jd3gl2IYdxOyGNLCH5KxQQLIuDkeC7eGU9Wq2LMx6xu3g9o1KGVKxZZV4gWiL2RsRcssoRsjNd6EEXoxY0mY/cvM4lNqd2pPd'
        b'l9+bf6RwlBxojqRWRndGT/Ogzahb/OT7hlG3CG32Qyf3MU/fnkU9y7o2d3FRnLbA1KAa5+IPjvOZ4y6+52ZsNywUzDANZJvcif2CM4vl87SXS5pRqLP+98t/x4dD2pkc'
        b'DhmDN3aTYWKDj4mUcaXsHZSUc55rPGCRR6A8BOWbQPkEaoWg1iZQKwK1QVBbE6g1gTLHRHLNjn7k6o+JnITaInysED5OO6wr7KSxWlY1S+qMcLPXw13wMY/SOAJ3Q3BH'
        b'HNbytTZa22quVIAgTtJ4BOGitO74CEX9cY34iEZONQc9uegfz/BP6koOb7TVhzlTwoZ4wy/XkH7K71Q4eZd6HHWSU1JPnH8fS+qF49Gvt+k30LuPIR8K+5qE/UzC/tIA'
        b'9JxlAqFNwoEm4SCTcLBJOMQkHGoSDjMJh5uEIybDU+srFR5ln2RJI4+y8aGUMleZizQKa8XrwqlpfwYWajiwUp8++oemJ18R6E9rZA4gsK22kooQFbiTIzWtSM/zpGIE'
        b'8djoalMrTBi3qUQiXpKDDF2zGXujNwGrMdibbDJjjw+E5KLC8dXwfOM8vdW/bJ5+x1SZwaGmygxbZp5+vApvWW1UWM9fYx/3nA+zeLPPp4PyYr2dbrV4jaJonjMDXPLM'
        b'86w/s3MFvFjJpruF0RRzk/cdcNPG7LA3s3VQiDm3W1GlNdbg1EJnuA9uIyW9kRlMZVOpTVbUmqzHS+dQvzVgSTiafIl0gqXCyxwSMugj7yYjuXJ5X+jLLH6PV3pvxopn'
        b'ErI2zPfOEXjzewo9F4QvsK1KduMsiPPs+vH+P4C7i0MoaVzNEc6KD0PPx24WRsfOKeo4Rrv1SuKPFQrtheeX0nEew+uc97jvfIv/28usjZ81BmxKf/s3frFbQm2d8FXH'
        b'PVKfstzZQhsytbzBCu5lLp6PCRJxKOsyttomiZFNx+HOUtAOLhUWRUuL2RQ/nO2yFAkQbCyCV+eDN+zA7eopeyNbudb+85mzzYbhhdXYHbkEHJ7eXKHevNpE8DI5jiwJ'
        b'vgIPIxF8BF7Bgi4qQsQkRMk8/bizlyHrk0zGHtmyApWXQOO1x51kKhvZei7wCF6nfC6FzP+K5LATpUEm+DZ9qiJwnkKJDnDAK6A1hMG9vwK8DNpjkBmaNwscgh14t+Uu'
        b'fIn4IGx/jP0pLzjCW6C9GRVBdCVUENhTgsRwWwnoc4a7xXwqrYAPDsIheFPI/x71GQ+RaSeiuRqHk/mRaBspRpCucqFmhXRx99vhBVaCIytQ0PZzW4oO7p89Oiu2y37M'
        b'bVZ/4D234EH7IeW9iLThurer7s1dQlZVZYz6zB4RzB4LjcPHkwWNBUUNLhhc2i/Gh6aNBYaSs8r0PwE0/sRYYEg/r4t7wMFE1jJG2TiPrPgf5+INY+P2k8uBFA3jNnJF'
        b'o0ZNjv625OJkzDT9hNeTKx7DNpntWunCYqViWy31aW21Xr6QOmOX+I8dWbaDOauIV4lrOtMhRSa4G04pymSbnqlUcbiCOaPIb/Lo6mmnEomVWmrKretPiaVDpWlPPAW2'
        b'2Wyzc79i7vnHMPgGmOA7/ZAy8T+DrG2lkVCeAtNFCFMlPj+Hwc8/z1CGYf/Uvwo9m0pM4pX18hkP0rKAXT7GbvKsLw9s/dLVyob6fx6tanO0JBueAq0ic7QEBC28V++f'
        b'RUp/khe/Ut2gltQ9BUaLzYbHysMr9ae2leFyDFsAZ0Tvf3Kq+gcoEzxGmehYxaG2rsShNdG+9FpGb3i/gU89kvvh413rft0cScnvzFrNVmHlIfQmz2A3stxOxOaz31n7'
        b'k/ycsJeK/dYtS8h6P76c9c4aewf+z+2p2X+xenZ3nJD1GJ8JpkkDF5DobbWyJIQmJVAWODWT0cYco+Viym8nD/DCUwxYzkhdKS+/Q5u7N/cvuecZPubrh9fBJvbN6cUL'
        b'kAczdZ6iEWfRP36I1/Svl7JNZrWqXP+BWa3/RS/FtJWh070UeiJ5R8pNdmHTuDfqlic+pskCkGXAs4q9gRTLavaSXz+/nUtIJGPXiiPvqosNRKKOz2W/E11d2Cv4ieDU'
        b'+4WLy1Mfj1Pv5PN/rqZUjlaFwtVC9mNsjcIBeBbrMU+kkB6kvB6Eh2A3mVzIgkOJ2PsfKRKzKL43uA62sxPAzewZDX+nSrLRUt4iq1xb11C1vsXbpEfNowhdRerpqtGV'
        b'iojGS8+HynXhGQ/CM3XhmXeD7zaPhpd0cQ85dDv0yO45h0wjrHEe2Ub4PaZ9FjbtZ0ZkuamdX49IzPup7fypXAhrw19iTydj4hxiLh6gqjn/DUQ2jRNNnyPUH6Q9sPAb'
        b'1mcxb+ATryvDQrwo4h/La4ZacA4lbYTHWqgWCTjBrMM4Aa96A+wSAL1geBO1CZwE/eQo62dhH8/MuEHkVBYBXgNXikUsKhG08R2Rfn6R7ILb4s2jrK2X8qn5awrLFztS'
        b'ZDeXmlvC/hGf2vBIJXP7hddhp19RmnQERmS3EyvUzNnbZnu69BTKbOPy5emPtR6AvbbwsBz0Mu5MMlt2GgwiK2QfsgeM/jnGNyeWyp27dTyyUuTws3lH3p2NRo9uZ2BT'
        b'OGeBaIHDgrgqJ1+3BeGlDnBdDj82V/Jek2RNhMc5ydvbd9EvCsJ6bq7d5vOS4D/qVPyXgv7oWj08267wTpuLVBGu8rDzKF0eui2kMPTs38obUwRpWYVbb3WIVnLqfDM+'
        b'9GvaUT//SGpcfYXDSW/voVtDGSHtvu2/T11z6tf3DoCKN8ve5H7Bid2/4fLbKrCZs7+ourj6CuvKpqarsWXx2Pf3ljRc8l/hQivio1tRoiTzbfA66BHDPcb5tvmJzGRf'
        b'J9zZQoPhqcfPIBMLmWyPMQsPBefm6BmAg3JGIVEM2omd1Qh2zrOL1Nth+gLhtgR8iNJVLry0Hl4joicGDojJkmFsgyGSAOfzQaehTD4VC05UgLN8Pzi4jPAUjxZXB3jO'
        b'dH0reyNog68yLsyrqHJHwLnZZgtV2Q3I3tsm5Fq0lzCVG086RjpHs1KulrU4mwx3AiHsZohhN182uVL+gV3ZD31njXnRRITt29ifsPeFQfWlzWc2D5fej8m8K327Cqz/'
        b'MCBiRJgxGjB7xGu2UdQNuup8o0c9RZc5Q9lXbXSeacML7nnOe+gb0KM+kjbIu+cr+jBIPBJTPBpUMuJXMubl98ArWucVfd9LjOfjHHodmPfB0vtecWPMYtP+oFFB6KDg'
        b'ku8Z36Hlo8K5OsHc+4LQz90RmiZMj88wPa5EWaOyKFP5BsZnuCwSc75pTbHKhOF9rXH9B+a59vGDqVfsxJziKq4l6UaWirAMzh3i2sEckF3NJfyPa7ZUhEf4H9eE//FM'
        b'OB13C0/P/6ZAZz48dfopZlbFZNHZC+AwuArwXSCzkIS7QM1aCLaTE/cJIyyFp1dGofbSwAvgOqXhwPMEvKlESNhjC7ymRI822C8vYtmyybWbmo++PHL1u3fjDV7+E7FN'
        b'8c3x56tfmrjZk9Hb7h3VuxT9VnNk1Qmnht6T2VQ/eo+iEm7ZPnwPqe3MCfY74S4b0B6Dt1gneAI0YsjibRblW8sF2ir/J9D8VhOaJ5v4zTqaQAjNxzI0P7HYjfL2f+AV'
        b'ofOKGPQYch/mj3rN6+I99PQb8/Wf4FBe/r8KDjvLG/EUjziLTWjOanJdqzIJP9xZ0xQ6lRXFWO9GkVs6lfAIPnID4f0XPoTIjcUKexpJa43KNKO3/6+5N4GL4kj7x3su'
        b'7mNgBhg5h0sYGG4EREVuuREBb4UBBhhFQAYU8VZEFA8QFfCIgxeDJ3jibapymOwmYRwTjiQbN9dustksRo1J9s3mV1U9wIBgdN+8/8/fkJ7u6uqnq6qfqnqep+r5PkMT'
        b'HTEmsrX4TRdxHDYk6hOu0/0/4LqXEu1o5iK7YdrgVrAfNKIq2M1aQNkZggaZx5vP2HIc9tWl+dnBd8MQE53d2LmnYVsr7963k3bmzXvvDUrnTdtws/0pVz7cwV1nZVP/'
        b'ATvjdb101ZsfvRN6sLNxWVCugXrh19k67wdSaY4mf/vKdfCLvcQirS41tEhLM5EhWfPQcJKF1pcbTibsFKJhp4U8ij+hfhpinj4rR4WrkvfAyqvP1kHBOZhQH9MncFFk'
        b'KmPVggDEYa7up1y7rXy7ub5abGXwEmw1uswGw1w2ZB2bjRlt7OKWDNqJMLctwNz2A/WKLOc+muWGxpYiStt+TYY4Xc0gx/k/YLeXEPIG2Y32MQF71qR7zYb7AuJYFEeX'
        b'AVvgNbAJdIINspVPHVhyLHDd4f7j4LuhiO1OILbz29LeeK26gWHQLAidMGXe7KifDxtlnjEy8l1snW5hw9q5OAoJGtZUynz9aI81aPAi240PpBsSH+MQsJe5iBE8MRiJ'
        b'5eNyHGeQ4zRes1ma8EIalhNofcMRdwjXiTVcVzTEdb1WDoqAM6z2mA7X00ldQSpxhNo9stspSmUV1c2N0uI0vVGc1q+TL8ktLykbcwLV02IxmsGwJ+P4hVupzWNLMY8N'
        b'vCKPkVc26bhRbYb+LJEp7b5JHDmJSyd27uw3HrbfLZWu6jdeUVKRWygtIyXwG3np32+Yi/FwpcXl0jI/7Qv/fr08mZwGssWeof2cFZJyHPdLWlEuqSTxp/COkn4jaWVu'
        b'oQRHR8JJJ0hOvBPer99gEIhWlqeFYneS5CiXlRdJUVvjbS5leP4vW4oPeCV8VDyylH49HIsYk+w3xGeDUHEkmaBpk/f5l+Uw8GYYjDyUU1JJ0PL6OaWFJcXSfla+pLKf'
        b'I10mkRWJmP1sGXqyn5Ujy0UXuhFRUamZKRn97KjUWTFlZXhYwaanEToabnPcTx4XU4OOo00UWdvCm1rxrEHVGuTr/X9hErB5riPn0tpaoxVeWqpcrOMrmTLTJpUi2xYi'
        b'18M9cnjFFEcAKuNQTHiS4WEADpFtC5mmpfLyFegmvAya4A1DBqULDzBNwBUaclWgZ+CJvc3Ouscle8cnp8HaFHBWDHf7JKTFiRN8kL6FJH0NsghonE3BxgVGUfAq3E/E'
        b'IEHJDNiYhk5cPKqoZNAOG2g31ZpicC4gEByy8WVTDDcKNBbDo2TGMwLVYAvSFaAS3KACqADQtJZWLBVJ09EDLYa+TIrhToG9oBGeJ4MW3K9bNoisUAi2IVnMcD4TnoM3'
        b'4U4ivhXkzQ4IZIIaXx2KIaLAPngJ7KDdWI+s8sdehDuSJ7EpDuycGchAKqASdJJ2DLDypDIo3ygON9upJNuC3vcCG9FouD0gENbCFl8GxfBA6ifohMcJHg28AG9XJXp7'
        b'ecNtcxfD3clecHsSg7ICx9nhoJZBiO5xEVLh1IY5zNLsNTnzqijioQC3pMBjqG6NC3xZFENMgWb0JQ4QxdQ/DV7whLVIVQJbveNpxcYU7GTlgKOOhODKqZaUmJobyRJm'
        b'L/w5YD3tBLwcHIAXUCE74SVfXYrhhXTxcEsat2RDFKxGCpIY3JmFt+uyxQxw3aqckIqKnU6toQTBLN/sWZGrFtCk7AzAUUTp4GyAdCCGNxq7bcEFuvVq8uE1vLc/GV6D'
        b'TUiF1/djguZc0E6I2axJoPZSA/H63Owl0+cY0xUFbcXmiNh5oAAd6LP7YLfRI2LChBzYAo7SrgyoijqgBjSAg0znFHCAkDssJr7OlYbh2UbVixxp4chsLtgYEJgCTgZR'
        b'pNn2Rc0m38F1CrydmAB3yJBWWIc3gmLPAxNQzQoDtfAMode3eDJVSv3kqZOdbd6gX0ZL8rAtIysgcIZZEJPUtMnRtwJPAWvN9DE1WJcyuBzLgPXgMmUN9rLBdngK0K4p'
        b'8IIrPBAQOG1BkA6pWnMAvEDzZz3c5IUpgIYSRIT+iCalrBBdJ1KWIAGPcqEqo3Wo7IUhS+dQhJoxvAPrA/wnTcZci+q23wQqSLMvDUT8RjMtE7XaBT44y4B7ncFG8lgY'
        b'rF4bMAl0hiHpneGPbSMHnGkeaxbAds9E7CnCoHRksG4Zc8L6qXRf3In6xOaAYMEq/FAIZr+6SaTkqznwFOY+xHnbETNtB+dR/5zK4lpq4IXBxjS4OyBYD3bgThmKmIMb'
        b'SVzIwUZwFhxLpFtLhDrVUezCa8RlWcBDa+jetVyf4lK+KYzs7KLLgQn0BzWHSquA4Gw7JOpjai1gqyWps+lUcAeVA2MPJSLmyAXbC5k2cDe8RKqWCDtAfUAwaFgdiJhq'
        b'CioFevkBcmsJaAKnEhM5aLRA8zizhBEOX0NfBb8rx6o8IJgBLgSikk/FjNjsQnqICbhsnIgHtR14vVaHB68aMPWTCkmhT8aspp5QvTG63OwVflaOdA+Rg21wM7jouxgc'
        b'DuRQjEgKHInSp5GV2sB+CVLMEtIz8QoyC95moPfcnEtozfWcQe1A7WAizE44bppM04qEly0QKXDdJhCNBFEU6ig3BWSzfHx+WiLcviwuSYdiLmb4uCymLXMGEyhf6mGs'
        b'QXb2wq41QrqXLYbN4GhivBhcskSMxmYzwBF4wZZUOg9cnoC9vND3uYg9vfjgHPECAAozuBMDvKTPE8+Kg9tSvWbTW/thbbIYDTsUNcNc18YCNJNBCdaBlpxB5KlJIk+8'
        b'rN3MBPtQ5dqGI9GJ1mDHMKEMsXVR05LlNPSWyDwDNupQaSvRoCWGl9AIjZfwo8ChsMRRex3QJMMGZydQruAUpwJ94U3k61iBo+mwLg2jEqDBy3wdPMhYxICHaRbfYVWV'
        b'mAG2roA7ER/AFgp2BKLH8HJwNjw8TRtEjXTiRHCBck3lyPBUQXeEA7AlEx40pMAZeIMCt9FfShCNab0TnPX0RA2SDHfFeSXQyrYfe9oUamIGx18viFS4M9yGCqRm2plw'
        b'sxceMDGmWVrPDjbBg7oUqEZMdgf9LVxNI4032IGNz1FkwtPwDjUxk4PYuYtUKh+2gXOJaeAwvOClQ4Nz3SpIJb0vbia8np6cVpiCcc+Yqxm28FQReUYKasGlxMzVoIFu'
        b'iRMUvFRqSRoC9e0m2DaIVEe3hFMC+oIOoI4Nr2SnEQImaJ4+Cg8aozEN1FPgJvrLA1vJ2AqOLYDnccf2jkfv9Yz38meDA3zKBhxgF62fTsoVjSYWeJBFGcGNFLiF/spA'
        b'A8GRA1fAaXhpxMPMtXno2YPsZaAulJ4iOoES3oZ16OwyUFIySgYOgxsaUHQ7cIt2Pxn8hJQpj7XEPYNWlY8vQTzcyKJg13rKgXKAO/RJlVfC49M8aah0xFjEYsLQWULZ'
        b'gstsNKLtA1fooews2AhvwYMc1CkoJHmAG/4W9KRwEOyKh3VMaiKXWkotrYSaPtAIa/MSvbziwRn3BLGNJ+ppvHAW3AtOaghOAAdT4UEjKgJuo8Al9LcO7Kdtzccy4SYk'
        b'JcA7oGmEHz847EKz4S3YukxuHMA1RkMT6nvwLLg+g3DYzbUGFJ9qztDjZhsZmIbTs1YCbFgL61iUCWykSqiSbPAaDcjXgfh6AxLb4jBe3Y7EVK8EMbMKFVNow4YdOvnE'
        b'pP4vAxdGN4uihHMmrf60MtDCnB6GuHAbuIOtV3jhhqqiqsAF2C57c/NrTDlefvn6O+W+/fNKeBFGbxdMTD6QXNh/srW+e1YCa++/T4YnJrYu3PbJs7U8l9jI/pteq+KO'
        b'vZf45p9uCxdzHZyyzEv6lh/d8ek8J1fnVf/zW99rhy8/nvLbjOjXfL7bvf+9GMd+/5mzCj/c/9kXk9QWZ3c8qv1h3UcfPf2zB8/ngw/6FrcqQUmbMHpOjX/zslWCldEF'
        b'vzq11tf0vvP0mwX+1d99nrS+PdswZ2dfQscu3tOvnhSm/vPvDXOc3o1d9c9M3W+XFxo8zNrx69Nzi/NnfOAXciceLPZveNK12fd17sSGmSu4JwWRHP0bdtWymg5d/dV2'
        b'1R5RSkfJkc2+kJvf0PFZRHOunu6sI19OjQqprebotr7PNXF8veKYSUC1c3vJA6eokAO/2O7yq/4iLuSvwkN5em2zjkBZTenESX8VR4VsrX5sAjg1pWb6TbbVrjWlE/Tn'
        b'GLXO+flqQqdIUfCVQnfRztUzM3w/9VBunsb6TPXPXVdunf6r7KPq6TFvzLX/fsX0mDPzt7Vs6z/fG6rM678S1CRc15kZ80vCndWbj+Z7bvKfHf59sONpRfczWXaP7m8T'
        b'dHf3lhQbPUrI100pYn/Xo+MWPkcljz0/S2645m9FS5VP5i+M8c9qavy5alpGSNbf2+4UX6Ck+vzgPRMuhzVLpjryPj91u6WyyGh1eP7j6OoFSV9+XPmv740+Wbi9tMnx'
        b'k4v6v4T9pY0T+SjbN+tX3/Yv095NsA9YNdVxtX9M5bvc1xrYn0/+x9+M/sp5tH7Tuw9dj62PSSncPvDLnZPMTGhTMxAkNf6X4NfVv77u/nTGDJMjgrcKzhzduPLbP13V'
        b'/7N4nmvpx/fPf1w9s+Lhov+cspbm9vH/svuOadrTdXkfinj0Hq89QWWjYcHI/i4k4FSTPV6rQSexLZTCYwmeKelFXtgP+AAj2dKJ7EMOXZGLRC/cycElsQ7FjmaAW966'
        b'JAgnvBAEToM601KjMqQZ7DRdYayvAzaHUHxwhFWCJuBTZC8X08HHELSL48hqBjgQ58OkzOB1FqJ4CdQSjyzYBdpgF72LOhUqh/yD4FVL2iNrJ2z0BXU+2EFIBtrxCgU8'
        b'xgR1qG/doNcwdsHd4DxZEUGTASrppng0syYz8zhwB9lBB2tnI8kvdTpU4tqtYESA3fAkjd9xHTQlamO6mcxlekEFvEZWTlzQRLsVz+764Pggqgu4BjeQzXeO8Ab2FSeb'
        b'7/DWO2sDplkK3EQqHc0Ge+lVIdfCEetCSA2i98olceF+elMfvVPOcP7wXjmwLYqsL62eEjScJRkN59XDW+VSBQT6LZifgWOY4sU7rDRhrzLcBqv4qAU8J3PAlXQ/Otzp'
        b'HXu8XYEM4sNGb3AOTXHE8D0phDTHGnggFGkmIpuRfscuq+h2Pg7OJGm25ZnwtHblHYdb/tfeWiNhSliSvLwq42EjELokZqnbbI2LsgVl76QBNQtQ2QXdt4voQoeUu/Pq'
        b'DT7hWzXrHDFsMTxorOZPVPJ7RJNVosldHipRjIofU8/o4/E/sXbudom9x/9gwjsTutMz/mSrcslUW8/u5s/u5dkpLNU8N7xMlNiQiNePECVFjDJALfAZumoPUK7okKl8'
        b'wtWeEWpB5HCuoA639uldkWrBdK004ilWpPaMujtLLYgbfWMJonHXXy2IHX0jX+05ratsJHlyo1DtOf2uuVoQPfpGgdoz7C4DPfHwZd+xTO0ZfTdHLYgfs1R+akHMmO9g'
        b'qgVRL31DpvYMv+s0Bilyw3G8eoxFSqr2nNqFihsx7hOjaz5uIw6ReuplY2H5KJQSOCkmKi1bvTucH1gF9Ym82uUdAV06XSuumdyV32N2hyT2hKSpQtK6Z2WqQ2arfeZ0'
        b'i+Y26zSvaDHptbJrzm9Y12PlobLyUOadX9K+5L5VCFnIDFPbT+9GvGDjcCTsQJhydkds++KuvDvF14rveyX1inw6dNrtm9mHTH43Q5+dkyJI6a5yDsAIfrEa7lQw23Rb'
        b'dR/i9U5PlcBTGduR1p5wXxzWFXBfHHPX+e4KtSClV2B/xKDFQDFdLQi4L1jcpfu68938e1mq2EXqyMWqkMX3BXndOXm9ArtWliJWOV3lMkUtnKoSTCVUNWtXlletO627'
        b'UtV+SfdQi6X1vuiWnUJHsaLVpEcYrBIGd+mohdNVuDPQ5MNULqFq4RQV9uMfTSNZ7ZdwL4KUeNxbw1WN0txKUPvNoDvVWM+gjpj6fEVmqP2GmH4UuUS1X9zgjRHPJNzj'
        b'qP1SumemqQWznn8sRe2XeG+OWpDZK7AZEFmILB9TFo5WTygLCwGG45nQlLgnURGk4ov2a/vLGNKGciz0vhpYDR4yn0Oq2UacLEcMmacGjeXYyTLNgsGwxmCAr+JVQ4zl'
        b'zTrulNIwYOTG3aGFmXyKhikgSzLYokvV6mqWZBgjLLl/AFjNSEuukBptyXWjLbl/r6Jh/xQhy42Ks4Kp4TVn+XoksjSmg8uo+PaUfQA8RKtANfDaatAYD+uxAkJNEIDt'
        b'Fabo1LAqLqAgFZHyp/xhTQ6tnpvpYdci3w2BeUkhC2Iosu/mXKA+SeSuXSP2TCulFfk1qWsZPzGpuYqM1VPk3EUaW9mpBfMDAhFJsM/Ik8q1BJdJ8nRYPyEgUAclNxUj'
        b'9U3Ko62UA8tIuCluR2FeUvxkP5qu2NgM1z2kNKA8yaPAhi7Btbl0okJWaPTAvJzO+VORMQ5p7z5TXCxWxYXQOQvjjUhiacZycV9OAJ1zMc8QaUiU3sCCQnGQUyadc3Ki'
        b'AUlUWFcldayU0Yk2EbqkSA8XLxXPdtTVrH9dBneSkU4Nd2aCs0iyOcKmOCsY4LoeOEmrZruTkFTVkhTgi83WLhTYA5VF5MUFFHbDoKgN09cxZ+vHaPZIQUU4UnlbwC28'
        b'EYCqKnIhyX4V8Bg8GJRqgFVi9Ge/giRbMCRI2axejFvvKvrj59DgPI0uoAupm8cCEd96UV5m2eSF1tNIeDRht0ehuHMKl47gtVICT6Ks+/B/HKQ81nDgdVQp+2D6mzWD'
        b'pkDQyPbFq8mUHTwaRCodxEPVGNz2BDrzNDuf4GlNpeclm7qBa+leWE9lwAaGObwODlbgHjw9AdR42qQQCIfKtaCRMJvftFRwOgX7Lq+iVjGnErOPOzgM68Fpo0TUk1dT'
        b'q+fNI8MH+Q7CMBrFsnt5qVE2n0dDWAG95bnvryV9h1FzWvb1x5dZcrwi49VVc3lfRAoI59d8lrSAHcGuNuCbpR2L5TUVl39ldhMkxr1rElz4hLK9W6nn/c2llglLf0kN'
        b'eKs35uDN346c/9f6ANn0o6l7LjUcLPV0vzNX7LNt9ucxH87yyJLNPNeZ3RKrsC+91/D5A6rNZEnyXWXf+yua3zpe6PXwlM+/aj/KceUsz/V67eLfziVYhvzlLzo7vp69'
        b'5LJh5qdbN/c+/rP6wqofy+2j/7H6fv/+K0dUGZ/rpd77SXgiV/Qp0/U/1ytc30ypXW0/ZV/tn/3EU+6zz4T6Ft26er8u7Ge3qq+/sSl5U3SQGdv2w96+w/faN+nu+/51'
        b'05XN7yverrvbOePrqMOr7pntfiKKuPa3rw6sNX1UmbR+0Xv6qSGLXX6c+trm93fvWDKx/sg2w4f8t74pK2pXTGm7VJXxrcXMtlPrFp07/a3xt/mif76x++kbBb1L99z6'
        b'6HbB3me110Mepb4jfzLt7fXsqLUr/y62X/hu+4IJ7aurDPdeBCsF527OeRZcdfStzw2fXl/7mU6OSEAcVVwqYNMLd4DOALuxo8pGcIYoQxYScINs9ktBasMBpIghGfsy'
        b'E+8QFROtI8OLqw2jYLwcu5uetyW6GrheJKUVBi9PcIH2FAowIdteVoDrcB/WFJJBExNb8+BOuBPDLkawEHfCY0T694N7wWZwOg80JBA4RTSj6KxjOqWJSVC2ZehFl0br'
        b'kmBv1bC7ELq9ixRyzoJwXA5PbLo9BxrBLgZQULCF3DPNwsQPI9VDs8kV73CNkRCFZ40rVOA3YPhIuH12Cr0OZDmXbQN2gx30/p0NsM0eq3q7wEk3GkOSWObNXVngjAWo'
        b'JhUpjYWdSDPbh/SzQe2MaYZ01E6iehXAayG4eGHTxnBT2sGiwS7gqRXD8Ev+wRpFKLCUaL5Ia+wywCTgRoPnnJhQJ28hSiCs4aUgbSmuAO4Te3vjdT9UTNjOgo3r4TlC'
        b'x9QMHsIfhbhUgcvw+gi3qlS4k7RYwhwTkmlXIodiMwULGOA1uAdso/E8D+XZDe7cA+d1NJv3pq4lvIfafm/+uBsFg0Ab3iuINwruldHoIXsq4BWNoh3vDFoHFe2K5U/w'
        b'PlRnj5SxdE2iaaLPcgBpm6AJNtJIoSVIq6c1RbgDXF03qCo6r6YRQS6Bw3YamPUQcIqiYdZRT9n0Ut5aWtgS/WzsnFBlMiz34GuiK+qxaOTv+VYU36q+vHGygrEnrNfG'
        b'7iGXjzc493BdVFwXRZqSeV63XbeXb03+rDSidQ9fhMS1Hr6Piu/TwVDz/Tv8OwK6+cHoNo05qXRW8b3u84M6XO7zw7pc+vhCBb/NptWmx9FP5ejX4afmT+rhT1Hxp3RF'
        b'qPlhQ1Q9VHyPHr6viu/bYabmB3REdkRh2JAXv7QPabTsHoGHSuCh5nv28P1UfL8ORzU/sGNWR3o3fzK5j6X8xlSahBLdFCtnKdFNv9ElTu9wuerd6d3jH6/yj7/nrvZP'
        b'v8+f1z1n3n+bL7jD9T5/Wpe/VgsEqRyDulD5Q3v44Sp++F1U0yh821ZZhirVww9R8UO6zNX8qfQzDq0OHU7D7RWp5k+nP8SI94R0TLzPj+yKJbes6CojhY6W09Wozk5K'
        b'v26+1+/cG/rOA8G2fuaPKVsR71kIxbduCGp2V/Ocn0y2NXMdCKXMLAbZ4wHXDTEMffWAO7GXZ9XDc1XxXJW8+zzxQ40exlGye9ynqNynDGqZkhbT+wIfZdR9QRDSItl3'
        b'DK8ZPmYxRDE4+p9jDOMJxbCIxQATZhZNhg2GzVEPuMJe7bdYWTdVNlQq2G3GrcZqK+96tgYjVeHYzXcZ2sLazXftdXFvS25N7nBSuUzqcZmqcpnaNUftEqPZw5+D4zBa'
        b'2dQbPr895yWQXMjenBFALsexjjGqr30/qGT8jJSMeVYMhjnekfNKXiPYUiliECldxPgGyTa/EX+mb/CGfpHVKLQW4qZYZoi3mbjiAw47X+aGd67oDXqKDZ7hPSvEI4qG'
        b'acFuCWSHLtktSXaykd1G/UZZMyNmRSRnZcybGZPez5JLy/vZGKOy31BzIz0mI50oWKQF/ne2rucAWqxwow67b4txe1YwCULLjzqmxhMfOVF82z6uWy/f/wmHyQ+sjX6k'
        b'Q9m69HF9evmBKMU2qDZpGIAlAAOwTCIALBpsFTHGVvHWRlvxwClikmJh18d1pxFZLPxqY57qsYy9nxowjWcynuoZGk9/as029nlmpGPsN0Chw49clnE045EJZe/Yym8t'
        b'7Lb16bN37nN173Nx65soUroo5qOfdmdlnmLx8ImLm5KtCB38cZyoKFcYDV7ZOypcmuf3OeEr2z5HF0WGwqDP1UMZqEh65MC1NR9w4k8w7+XbtcgHWOjsId+mJX2Ag84w'
        b'TrBja0CrHGX1HtDFKXqUhUMrD1MY0MfXBpQFyq3gNycMGOJrI1TZFrkisHnJgDG+NqEsbLvt/AZM8QV3+GEzfG1OWTi1RuEyDvDwNX/4vgW+tkQPt+Tiwg9Y4WvB8PUE'
        b'fG1NWdi3shTRzVUDNvjadvjaDl/bD+d3wNdCysK6JUrBbg4dcMTXTsP3ndH1IxfU5LgqeMcnyvSDG050dbM1Qd8+g0HZOjSvUcarHIJ6HKaoHKaoHaapbcL6BDbNSUpL'
        b'la1vj+0kle0ktW2wWhDyiMOyMalNfGYQyTD2+IHCx2dxTF9j20cUOgy7dkSAqyXakiuH4mawwI7i+fPhnhFquKHm97ETxtkw08LZYGB0DQ36hCn6X5fgKZiOvMpjjrw+'
        b'wzqtSxPUp/JsyTZP/VrTfHYeu1p/0DIwn82kpBwNPofuCHwOTp4eStXXStUlqQYo1VArVY+kGqFUY61UfZJqglJNtVINSCoXpZpppRqSVHOUytNKNaJrnGc3WKs8/iEm'
        b'SdMhR4LLscSaeu5fngXBh7B7/s7zeBIvpGP5snSqtM6PM3Yx8uxrmcSGQ+/JM8SBXfP18wRa7W6K7uvXmpDvMaFabz53+PuesR6kRbblsnCI2HxOnk31UOCH+WarrPQL'
        b'RA79NBpVYkrML/tHoC9ibODBW8LcIolcLnSfWSIvXyEtk0uK8/CgLpMWi0Y8M+LCIwODQNKxHHEo15IceUmRtJwOwIqDWBaV4H2WOIimtLScjuNKgCxHxRYtw0YtkW6/'
        b'viRvhUyO91/2G2pOyTZKPTquHkpm5eWv6GctLUZpy6R5soplKE2vFJV8ZUlZXq6eVusPxc7YQGlvnh+Mq0tc1nDzs1HDc1Dj6ZD9zcaaCBqIXbcNRc5dq09MaXpapjR9'
        b'LaOZ3jp9jSltVKq2C8dfH7HGQPuML5aVy4irngb8efBryIrl5ZLiXOnLY30ONV2oBit0ODgtpqzZhIpjzbpH0ltfUYZl0jLR2GEHI4SafcA0LrSwohR7TgcL82QFsvIx'
        b'IEhHlgJ/taFy4Ii8LygFuj1eGYqFkqLSQonXWEWZLMwtRK/MJXFvx43rquGbsduEvit0T0bsiookLf4vWmTS77UIYlg6RGh07GxhkSRHWiR0R6faUVdF3qPimRKmkI9Z'
        b'ipFFJ23r7q/VFGMUXlMQ1GlChUkEKgpTmeGTNBQdl24W1PvTJbmFOJ4tKRMJd4w69zhIsBU5RdI8Te8eSWUmOpYU05FxESUCBIuu6ZbSjAljt3F8+VC8YommmXOk5Sul'
        b'0mJhoNA9jw5pKiLDS8i4FR0cGOhmp6+EsjzNBwv4vQ82OJpo4sJqroRl0gKZHLUwGsXQYEfYSSys0Hy2imIcn/V3sG2f99sype3nA37Eluzbsz47KVUwk6rAvldhruDq'
        b'oLOoJhjHTOItmkRH+4Dbk9LosH+gBe6nQ/9tCTfiroY7CNFJAXzKnaLct0ZkL7wTYENHFDSELTkvJoo3bGYOhxOEx1gUPFJqBI/DzX6EboqA2Li5a+ZnJ308O5WqmEZh'
        b'RKBYeGZMwoORR9BxYlqaVpxC0AVqDUErOFtMyHqsJZb3uT6O2Um+dlyqArsyLARnId0IsKVkNOV4z3Rtchvgbn2wrxjsI+RWpZJVgzhJdnZRSXAZXftMsAvsG6uUsDZ5'
        b'yEhXuHxUKa8YgmOgVbMfd1kasdu7/2KeLY6cFUjvPDcHx8LGIusepzFEefqMoHkdnDaEtfBYpcz5BsWSYy+DbyIfbvkg0YTpaKTz8IeT2Tu2/mB/sSXp866A4k+uf0G9'
        b'FVUZr4rbOnNTsl4d+O3y7p/Y+qIvj/Fustec/kTfzX1fVm+154DH+YLlYcyFn2fue1+c+C/vTV/tuSe7EK/eHPjm/Sf7YwP+9P6fn3zR1rsxpznndMuH2w/fCd8jO+5b'
        b'b9u4xrXlUKz8/opzFw8v/fOvd6Pza959sv7K453lgriG+BvJoWvv37vO8C6x2TAlMPqWyICYBeNBLazHpkNYDWqH+JG2HcLL4Abtr3sEXoANeF/GStg1ymFXp4Tsp4if'
        b'ALZhMkJ4RZsBOZQDRiw8D2+C28SGCI+Yw7PwtjWxRI42QzomELvdVDZQaHADwY1oigAHlsMWYrerBG1gE20jXQNqsJmUARQVYAexAVeBi+DGoMkPXge7KTYTG/064V66'
        b'HodmznKqItbc0abcQHiKhmI6A8+As9aIUep84kZZH0G76IkPlhrAHbCHlvDl8IAXvAivyIl5GiUkEZHfS4dKBtW64DC4Da//wVovARsyG5QvRoIsWdGQvI8qJ1DOE1tz'
        b'laJjxWqnSRgfqY9nWV/etL5hvZrnpnS8z/MkiEoz1NZx3fy4XhcfjKjkSDL1WLmr6Mh+Efd5XiRbvNo6oZufgNTM1nSl4NgitWMARlmiaa5rWKfmTVSa3ed5kMyxausZ'
        b'3fwZmmg2BxNRTn0656qGVY1hCkTVlQ4SqLaO7OZHPrR1IFleibijqM2+1V7t6Pf7WZ1d69kfcoXPB0DpxGaJC/hwER8u4cNlfLiCD1d/38tvKPTJKE+/cb6QCMmN8qno'
        b'3m8/YafSCQzGLAaOfjLrlWLMkU3YOn5Up+HU/w4QqmAQvWhIzhwP9ma4CoOoN5moClrgRbSUOygqjoGv9N8DQmmAeYyytOTQly/nXFzOw0PltB9VTiJrDZfyf1NA/axB'
        b'yfTlS7cAl24YzciBLt2gIPhcI/5v0JbYWUhqffmSLUYlezyEajTvAL1q+osNXUItufePKh0SZV++dBLcbt2MwXZzHxaBJaNBvuR/3PcdFEJfvpx5I7+vNTZQakmvf1Dj'
        b'6WcNSrQvX7KC50uGvuuQZKxVMhGTmIZpI/GQa2JKLkurLBj1nPgmkqCW+louxjpEIcdBN/RJYEsc1tK41iTfaMjhWPcPczguEDGfcszHUMkj8vJwkKVi6Upt/kB97KXC'
        b'LcUgBYrOjO0hkrw8pC4gpUOi0T9J1CQcHUMsLCgrqSilTSISYW7JshxZsQSHdXqOJGJUjyHIOA+x0EMb7A5dEzw9lCmnpGQpLio22xANiS5G+arSV7AiDL0oVJhesgzr'
        b'orR1B0cJ0SDNSXJKKuggUpgDpHnjtQ3+F1tSJpTiJsmT5ecj3QmNVLRWN7JSmvYmgaVQsxVoYqCMoVDhf0hJzJUUEx3xRQYCvyAttVjoXlJKgmYVja8ga7crrfw9N0AI'
        b'3SNyyqS5hcUVxQVyjbWAREIZs6DDfCCXywqKCSt4kzbRIqwJpSaUaddKhhRnpCSPSXVQIfYjHzlo8pBejN/kJxJje5wwT5pTjt+DcuQilVWGL3LHU+UJV8rI83JpOWm7'
        b'kMkvwTOx2CGb2P9GdxWZVB760jyHyior1xCg252kDNkV3NNLioqwLaFEJPTwWIaNNag6qzw8xrX6kBqPoEgnDZOcgZq32MsnDs1Lxa9Cmobo05gGSuSkwhrYvpd6HndO'
        b'+mnt7uotTB6yepDuW5KzRJpbLiRfcOw+kJ4aEuTrp7G9YtMq3Tu9X64YIxzsQ0dZn1aUyHKlQwwfKS2SFuTjfCLhAj//RS9D0l/zGSukdHVkxaSguNdHRycnz5uHazZW'
        b'oDn8r1SyahkJUyctwxOfWLgMtfOQjUWrQP4vLpDm82C8jJHfC6eMtLjRvcVnsKeMWSxa/ItElcR9H9NArw/wHff1IyANBu2PWt0EpaIeWSyX0YUqyR/zrZK8JYgzSHvg'
        b'B0isPkklPh97bBzbcjmCiJyYXmW5heWyAlwVeW5hEbyJRvIi0fN9dlyaXkLEN+nl0go0uA4RQBwsE2qaCI1Qy1CPi8n0ypCU50ixOTtvHEqIXeiwV0UVy5ZKC8dufy9h'
        b'wKhs5G2SivyqinIpmjlwoEjh7JIyOSnUODQCQ4URFfmF0pwK3PXQAxEV5SV4fls6zgOTQoXxxXmyFTLEzEVF6IHMZXJJeZV8VM3HeTporCK/egMFj0VGplWsZa9WrJCx'
        b'6L1au0wmDTnc9L/T8mMmZtCcjO3Oo8r9ypyoXf38MlQbd9y2Q2WS5FRVFIjGZz/tx4XBruMz4IiMfpPHy4nYrNhHMj5LjSQTNB6ZoBeRQUwxVL8X0AjRzjZu1SaPIDZG'
        b'vcad0DSQK2iE05wReQDJpGhsHRzK3dPpOXbcCXsY0SVUGIUuhPQVknHcE9GltBj9j9hciOegkHGHXC0smJFk/EeR8X8hGQIbQ08ZsyMyvOKjhe6Z6eXoF883k8Z9bAhm'
        b'hn40JpOM1DhB6I46uYbF0WcfvxkqypCInItmiyjNmVioJdvFZM4Sus+BxwvLUCdFZQkcvyhaCDfDxIaSNYUaJCVfWlEmf75QLxL3xhMviSj58pLfkIgWMWIJ6eVkGILZ'
        b'EypMwT/CBf6+i17+MX/6MX/y2PhfYxAMSCNCaq6xMv4iPiBIQegR/IMyPp9v/FEsTlpWVuwTWyapQIcib59YGZLuxh+1SPbxxypMZ/zxCb9g/AHqRW9Go1JMIRLC0Ng/'
        b'/tBEyoZktryxizFe4yEpViotx5IF/kUCVtAL5buckspQId6ygOSnfCy1ogTU5uN/VPwQhmCin5IUCfHFC5/IlZXjDomOLxT3aNwpnJM+IYTFWE73CvALCkKcNn6ZMOQT'
        b'KhD+eSFH5ktQbWPRoPKiTAQ0Cn0h/CNcEDR+Rs0wpxniXsTRg3BWocJIdEZLwgv8g1+Yf6hrk0dGLhG/sL0HQbI0T9LfZ/zBGkNjIREtMiIFfZ7xR8QcWS4iGB+FXj1G'
        b'j/ydaNWaZdp31jMpdqU3BwOdm5VZ0hGkg+bEwi7rQZCRIYgR2BxBnvluNZvSs12jS4VnF91izKBhC9Z42cBasCExXjyIexIJW0j2y8utKLH7Dh1KmL2mITuShuZYnTGF'
        b'RLyG58AGb8obnIedZMeYJ2gCVxKHsX6ugDYaUQrUZhJqb4etZfyUI9GlfCVT6lyZVIUXtu/B2/BqkJMneiQBx7vC/gTgTEIyjXNM4Z38s6jKQP0CcBLcIuALqZwUgmfc'
        b'Eb/MKEFSZptMVeD1CIm151hgxphKHKzDAbzxktZsrYVPuBO0GIngftBAVlRkzW2BbDmTQVEHql7bN/NGCgznHpp2JGuy27RA/nHF0ROtX7r9fU5Ebp1gG+j8PPpCevfZ'
        b'uvJae9W8/3H+W6OPyFs095vy+++//913ayyzuLdOXHbyfXpg3xs2GalHe7YfW+wZ5+33D0/K34G/MDPx49TvAvas2vv6o0kJkTMPGaX3PDYVzNt97Os3vDPv/WNg3Qft'
        b'j+Vf/E/erf3Hd8B3JL/4KJtDp1W9c6vJdMk/v9pz7uiu+XuO/jny+5pTuqu/+m7qt/sqf1xREOB3eXKxX5vX5DORLm/WffpD8p1tt349Mz8x1774F+b3ZfOr9azOB73t'
        b'EMqVbF3wYMuM/cqvD1/YXjf7sK1f6OU5xpN6Yz8o/PtvO9Y81c04HT2FzRLpkXVKR9g1HMFMZ7IjDmAGumAdWeC0ASdnVYDD2EF+yDv+CDhP7klCwAFPuC01HpxhUzoG'
        b'oKmI6QSaFxA/chOn/GHI5I5kLe/4vTziuBA+OYlelySLkg5rx1uWhBvmEj+KKNAkBscDR0MnD+Iml80gy6bghIGNZ5Ecf34vd5wN7sZuH/Us0OEHFQQoAGxbClrhdrgr'
        b'MSmeQTFnMTymgEsi0z8yWCP29BIOu7uP8t80GrJ1D3q8x2vCk860p4Ti+w6+yuU4uIxNc7mK59xn49br5t5shAFBXRQrWsUdrAdWgX1unu3pHbyOvK6gzqK7AXcju4Nm'
        b'9AQlq4KS7+Wqg2apvdK73TKa2c2zW4x6bRwUOi1Te2zEKhtxQ3Svhb3CRWUxkdD1aMa3j4S2hB4cyvAlXpGcrrYO7+aH40BwC5WTuy0n1bN6eZbNeT323ir0x/MmuM09'
        b'Np4qG0+1lbiDc99q0if2Ht2eKWr71G5B6gCTZeHX5zu5y6XbN+Yu775vDHZuIN62PJXAa0CHZebVy/eqj+7hu6j4Lop04hPhpcJ/kzrYav6kn57oUrauP1AMRMfeUxml'
        b'tvftFvj+e4CFEv79RI8SOKJ7Zl591m5Kltpa3M0X43tmXr8QbF7gbxkloqC+QzSTgiL9qOks6K8XFcqCoRx0/gZTP1rAesNQL5rHeoPHQef0aqspvdo6vJqAtwu8ktvu'
        b'KCYYXm59IRMsYWkBXqbZMBh+zyh0eJXt9Tiy1dhxOwhiPlsTt4NTS9XqaBCj//DYHWXfUKPC8zk8N6250tPabVs2VToBNWp4thHPbh6Nwwirq2CjvAIDWO3MKWFTqFsz'
        b'1masH/bsDZJMMkRNNQfcBO0U0iRgB4FFWm7JTMfPYA/MG3pwIwUvrdDMbT4z1jKE1A8cNBvZiKIiaDLrdMEdjR8uqLGhpI4rSbLJvAKN0y48uJTKBdeWERKfFOhSGUsm'
        b'kKgiIWultCttxnwuNbcyiqJKs41cc1bR3pqHc7mUIiKGJCqrVtE532IZURt4QTg+gNF7zmw6545gI8rFniSKMyJZdM433Q2o6CIxRXGzjYrWRtI59+kaUJ+keJNEKlZM'
        b'J6qDdKlCXwdcJKNNfDbdeoVgI2hInzlzJvo00aATnqfARniMxm1Ds+0esCvA1xeD2MHjoCmRghtnLyJYTCWZAekzKYyZAreCkygdHFtAHvKUuwx6+1bN0/j6cjRQevAA'
        b'vFROO/pGgl3Y17fKljizpoFOJxIYNB+2o5nlYBzxhdUH2yMCsIv18izKH7Zmkqw5c8BRiMGbvVaDg5SXhQGRbaJ9PUc46YKr8Dh2PT6RQL51GjwDatNnChEbgIsWEnBe'
        b'B7TK02n/5E1uOKy2xlcX7vce9NU9TMe4II382EaP+i7YGXdN8c5CB7o910TpUUl+E3FiUo0sggYZBA3TJOm4NZEIoQs3UxIx3EJI8FZbUM3JmZh3F8bHpNLiFbzlpJ8+'
        b'EyhEFBW6VjffELZmgVoaVXKvEDTKjQNQWzHB6XB7lBXeAOdl9p+ZcuR4pbJ0re3hjHdSoC/Xbkp88PX7W/bsn2XpGLbJef3dlo/jOPKlPplf1cpP2HcJw46ur3mwPvvQ'
        b'WzpftibEnZhrd+eZ/79X/8T4oP6ukXmnt2jAweKnK8tW/AUerPwfdtzx6grlV7O/+6dhp+y4ZYcl37PKbeN+j18WpLIS7M4kUCu/PjJT6lC38ZT/R9xj0xpvz8z9PtHn'
        b'KpXo18TsuMk3lM++93bt0XMBP307O//R1d6Pxd45V39d/aE0ZFJTnXN1r+/qyS0VbxcJJq5a9PWxSyGzT3yTMX96hg4nc+GXvUEeky98+s6FtYdYH7t+Fyf4sHV3hnPN'
        b'pxf/w5/lYJX59rqPPHk6H07t9fxs1e51qdu+mf3dF1Tq34MDnwp/bT//8KfAGD9+xOeiFb6vvXnu6Jwd651XL02NSL/Vt2VDbvH9Sx1d0YXNJT+tcgmz/u3cWs+P0wre'
        b'/8e2b9yn/vZbknTSdUm9evOkA6GHGbHnv7Hv/DfbJ3/fmp/V3+w6ZreipdincsO3aivjX8o/5X8u4tPBW+rgNVCrJYaMFkJAIzUoh+hW0c6YJws9PYlg4+UHG3SQ5H2D'
        b'CRpsjIhAtGoauIIE3CQGxXZEksttBhKcWpDYgR8sjgWnNPEZYFP2YIiGy9No1J0jsBr7mQ87/aJz9HinLdhB9qzBTVO8BqVueGFkFD9hDEcf7Mqn46zvsaADCdJ+ufAE'
        b'xQCKcAdSgiUVkWgcuIXeo+WVuxi9gGwm2wWv6wz65Q5trJsKWtg2qK8fooGUmhbxkIB9dvoI12F4Yg7Znue0HDdlKtzlDi+P3i2HxXK6fEeKE4dkyWDU+5E4WauBeOL7'
        b'L0gcEVXQBGwGSkdWJNixnDjbloATcPOwxy7x19WB21kl4AbcTUikQwU4l6gddNBkLTiRzoq2h22kmlPA1US8XQ6cgjdHb5k7Dg/QWFVXUQtf1XLH5YALeGveUXiGNIPu'
        b'SrBl0B/XAZzW+OOCy5nkDSK4CTER8cK+lDZ66564+AkOKw52w9Pg3GBrc8CN5/YgnhSL9F5a0sCDklCova0LRyev4g6LGPKsPFkuHSW4nalBV3KgJtjUc3D4QcNeoUuP'
        b'0Fcl9KURXXqEk+vjcOSNykPTcCgPO6HC4uB8pWPL4vrYhz7BOJrH6fX1Mc3uitkqa08VX/yQ70C7cSrK2la2ruwV2PQK7BWWLabo6R6BFxL4OpDUF3hfMK2Lf18Qc5eP'
        b'oewz2ua1zutgqAX+PYIQlSCky0xNIGOOmLaY0g8pJWqBb4d5B69bMAnfMGkx0QT5SFMLfDqYHaxuQSB2gIrrsfVT2fqNJNUV2RXVLQgn948ktySrBR49Al+VADvlCmin'
        b'XEHI6AKGd1ndFyTcjR0zvfBuXE90pio6syd6sSp6cXdWgTq68FVy2tH1Xty6uAPVILhHME2FmgTVMhy1VytPMfeYnQrHM7EjLaj5wxWIJvsTTRRlSka3wGO8RESkV4CD'
        b'rwxMsvG1fEzZuFs9C6IE9g0rmgvVVm4/BttYiAZMKcfQgVgG5eB0pLClULFabR9Qb9jHEzx0mdg2o3XGuO1MKI/zcUi1elyDVK7YJVgQ2iMIVwmwSzBGdxrmhUGWGDDT'
        b'90LF03e1emY+XDyl5yOevmsQ4quJDckDfEpgV2/0fMiMF29zJCEzfr8jfMkajn/2LMbhFT1ZU7Fm8JgaFQRtKAgvidPC0aCfszWeVjgYms4Q8vlwCIM/APm87MfRUvfz'
        b'YQx0Uyrc0bnlZPiaZxySj2bGoRkMTVSgPSMOnIW1Ym+RDgUvhsbBGt3SvAlEEAO3pqIhsREJjjVo+MaB0VlFDLCJDZtp5JWTcMM8T10q3Bzjm4C9sIUWDDc7wtueUJme'
        b'yqQYs5CcCI6skn3D/4gt/xrdPZoye0tapwHw5d5KzFnKNzNrOJpyztvkPxv+/t3Cbq/0WItT9d6fm5daTD86/RuJjUXOEv8vK5/95dNbf5pWtWHZkoHdX4flSzdKy5s5'
        b'GTtDP1yXdKprvyosYatH+d85yxKvrl2UdmtyZvfh0sUrfz2U86/XluoEXZi1/GN3j57J1t23St+0+K6GWhCbtF+++fq/kDx2M1u6ozSRzS3hnlu0eVupya9vdr99+z9H'
        b'Z5w6vmvjQM97P3xRc8VM92vBr9/mNMvbq+ss6w2dn7zxN3XKX9Lbe37tVyV0m5z03crKN3J03dH93ra2+tabYQy9luA3gk+JTGmojlq4e6mnHzeOxJRiBzPAuQJwmJ7v'
        b'u2BNJp5oNV6XeuAOOqtjrvVE8xSZJ8/AE8tIhm1iphOaaFOYtqDaiMacuGINruEAcmLveLgN3ISb0WxqCDuY8GaUgI6tu8MRizOXVhI8xpq1PkwkgbcxwTGoBPQcB6qn'
        b'sRLFGN5hWxLYV4CkAcNwJmxGGsBWIivAOkOwH7/DJ9WL6RaDJ3oPeB120KU/LIGbyAzYmi/SjpkVCOhZHm5JdEGFj4c7vXTA7TBKZzHTGZy1Iw8vQPPhBk8fuH0B2Iek'
        b'Lm8RE03jR1hgC7iWQOwzE9Lg3kS84d4nhZO5lNKZyrQqt6ARJU65wc2JQ/yqPwG28JnYS2Iuub0QHGKhIu8kbQZPwX2UTiRTgLS5FjJtByJt4zUkAG1dPyxlIQnLLZeW'
        b'ba44uHkSUAwOvAEvIuFIyRSDJnjmfw16OKj/0wOSLkHwGhqQ5JIVdBCtnyl6Wk5wpPiWTcENwU1hDWEKlwc8N2Xk+RntM84ntyd3uTwQT78b+XbC6wn3yh9EZ3xi7djt'
        b'FKy2DsHoEmhsNmoxOmiCpnSeVVNoQ2jj1B6eu4rnrrR8wPPts3ZUuChZyoVq69D6qN6Jnm1LW5eeXNZi0MxuzkNjNH5WkaEM/FDgO8Ci3AIf8q2a4hvi9yU+tLE7EtwS'
        b'fCSsJUzp8sDGp1dgfUSvRU/BP2QyikqfnaPCqc2t1a1N3CpWlndkqJ1Cu6If2EXcndVra38kriVOkXEo5RmLso9kdNtFPMKv+cwuAp3+IsfbM9/wMo8x4LxpwInh6WvH'
        b'Py578rvjPt3edLTjEVgGY7S2A1sLL221kMEQ4EDHrxKsi8RMErGJWYKOxUHic+gNTVVMcp4iMh+NamDAoLShDV5iV/8pBonHWC5dJqexCX4YrJbI7A+0WGq1Im63DaP/'
        b'0a15HrfmkF+vI55EFzEIhsEjNtuY+4MRZWLRymqNal7Vmft6+ju8u/F9E2wVntd419K79N+JesJimKRhQIywcMYzlpvxxMccksBGp49mMQbBDYIwuEEIATewce7jetMA'
        b'CDZBtYnD4AaTMLhBMAE34Nn0cSf28v1QCi+gNmo4JQynhDNIkuYxX/yYvzZKwmDKD3qo7AMU0ySZ0SLv5D0iZ/1WNgeiWyf0OAarHIO79FWOkT2OcSrHOLVjgto2sd/e'
        b'qXVyj/NklfPkrokq54ge5xkq5xlq53i1fcIjFsMukfGYYgiSGI9YmNYznQqGsdcTCh8f6+KUAZLyrJg12djuhxUM9P4W5wfG9s+YfGPPx0j5cXiEz4Z99cs8SuXDeupV'
        b'0MShjK2ZsBGHWxAxUmRfZr5ByWPQ91BkcKQNH6RsDue+VbBxy4kn62WGZz/sv71p20qfsM3P9P0enUzOyPE5qc96bafp64mhRStljWXC79Y8/vXrj/+6cl7Xljn3gM+m'
        b'yF9fT/Vh6757/LuPmE82f/6V/cN//nVujNtX809fm38jd1nupCfvT7HmnJj2zfcfvn+I8q5c5/2z3ZfvXX13y/fdN9/6WXLN+p8L//FGd9XtmN6yU95bHrSZ7ZRFph9Q'
        b'HZo1Xz2xzjdUmTB5QO/M2wtT46TmN3S33OqfvOdHxdOPk7KP/GOzj/K9m+8u3efoeSzgTa/zl7/+IW93KN9vvfJvb0+MiEy8ftTi0/qjFZZfNOvzplwMetZnuONPEd8H'
        b'pH2+6Zepsiq90+EXXQNSgxMKIxiNTof8ZMXx+0r2BE5Y0+gUtGvvtGSDH1VBNhLw/hOnzY/1F3Dfm/7x93k3vtn16RPZFw7f827WDfzs8AVY8mfdmSLWEyzOTC0DF2Ad'
        b'Ut/AQT9GCAV3gfNhZKGBB/aWkwUOcA20jHQzWwuukRWLGdOkz69WyKCCXrCAm8JFLqN7oN4LD/8X/f2/GCFc6HktnPx7bqgYNWj062VlFZVI8rKyqobOyIQ3DXHqf9CE'
        b'F0gZWwywdfWt+kzN6/3rVjY7bl/TIlf4KyStkw5WKdMOrO906Sjrcuys6ErrrLzo/Xr0PXMYd98/6ROBdbN/s6Rl0kF9RQJSmzqskObXPTVFZZXSPSujO3O2atac+1Zz'
        b'PrEUKswbi7u5Ljge31zGgAFlzq+PaLCojXwWaKbv8iOFDs/c3fS9nlHo8GMGY6q+df3sJxT6+XEdw0XfutnyCYV+BlIYlAH3GbOMre/5jBo+PiVH1GMNuAPk5kC5PiWY'
        b'qDRUWQXUGj3V0dMXPLMsY+nbouzo+JQcB5boEmKzCJnh4w/kSIg9Ijd/GogQMPTjGX3mDseNur1i1cIZavO4bqM4etLcHiGI1qPe0ONF22jWMOz6mVlZ/+Waxf8Nv2CJ'
        b'NHvkathYs4sZE88ugzyCBTp5JEWraH4MBheviNAH7IjGfRU/NCwYnNIJpa4bRnBYsmVN/6bkOHBZyYC/dEe8AZgp2PzZ1Afzua/r60b+tTSkYY6701e3Dv/pOu8/P/3r'
        b'zajK+BMx3D9/nRh3Lzdme+CEC1/eS1fEvZn+4IJl/MIYT2uv/5T7ZT3bM+38hX07f8v66NuC01Xv/ufT0u8Kr/00061p2ulzAaIv74Xpmiy60n6PFXQt71NpU821HDcO'
        b'P9BIrFPqnva6c3a138TmnJrJlnOdcnYaGxR1Qvut6qM/Xr37Y/Fup9c+O7HN+92Gz5BKgZuxNA2exlJ5Kl5B35GoSxmCC4FgExPJ9UeNiflJDDfDm4n2YH+qF+zEGZH8'
        b'TpnBmxj37go4SKiscYKnQR3YDXdjmxM2eepSJrAm0Jxlb+BIg6lfY81LjE/2SIYtRbqUDpupB04vIwOi/yIS+0SHYpSAM+kUPDYDXH5C4FXbqULPBGyy3x+dSMFmd3Cb'
        b'RnbfBU+Bqzioxi70MgwobiiC+3KYsJ69gmTwcoHH5Vq3DeKLwBkm6EByPq1ugJoSw0Qy89FWPxMR0nm2s1LACXCTKFp8cAVeSOTBjuG9DfBcHKlqMTglJ9prnEbTMuKB'
        b's+AcE17yQOUmutKZhfNBHcpRqslhAC5O12WCS2ieraFtr53goh7KcsEI1K5cXgEvLjdaXsEIXEdZwd0ssANugltpSgoKh/XBwI64OhT6OAcCYDUTHgV1QQShff2qdYjO'
        b'LinY7ZOI5oNdeHkafwhdysaFDTb7wi6R+0vPBv+/nBy0ur07mSbCB/+9YKIY4YyqN8JLeD46/IaGgMfWFIfXa8zvMbZXGdsfqlQbu2+I7WUbbE3amNRt5ng85AFb/DHb'
        b'GP19ynb4jO32GdvrU7bzM535XA4aWYePT8lxoFJIGfE3pGqZlxz6WUXS4n429lzq55RXlBZJ+9lFMnl5PxtbjPrZJaXoNkteXtbPyVlVLpX3s3NKSor6WbLi8n5OPhq0'
        b'0E8Z3uiIw6eXVpT3s3ILy/pZJWV5/Tr5sqJyKbpYJintZ1XJSvs5EnmuTNbPKpRWoiyIvIFMPoi+0q9TWpFTJMvt16URbOT9hvJCWX55lrSsrKSs37hUUiaXZsnkJdgX'
        b'o9+4oji3UCIrluZlSStz+/WzsuRSVPqsrH4d2ndheCqQ4/Eh+0X/hMLhD0EOODioPBV/g99+w2vTZgxGHgsPwiOPA+T4KkMynrte19WJsKJetzKMcGL9opeP3Y9yC737'
        b'uVlZmnPNVPCLteZaWCrJXSopkGpQfiR50rwUkR7Rqvp1s7IkRUVo5iNlx3pXvwFqz7Jy+UpZeWG/TlFJrqRI3m80C3tCLJPG4LYsC2dqPj/NCLS8MnVZSV5FkTSsLJZJ'
        b'OzqScLIDLAaD8QhVjT1gQhkab9D9gV3EZfAHFjtS+mY9ejYqPZvmhAd6bt3isNcnQneVOKFXj9tnYNltFaA2COxmB/ZR3HrBh5Q1edX/A4fQsus='
    ))))
