
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
        b'eJzsfQdcm8f58KsJiGlLbINfzBQgsbcXHpiNbfAIHiCQANlCYA0PEjveCOOBbRzjFeMRG68Er5gkTuLcpW2SNi1ylVilTeu26T/NaEsap03zT9vv7l5JSEhynDTt1+/3'
        b'+4Q43Xvrfe7uuXvG3T33W8ruw7H8frYTOYcpOVVLNVO1LDlrO1XLVnD6uZSLj5x9jkVRl1jWZ42PnMOmFLxzyH/JlmotpfVZxkbhfDnXMf1WFgr1UIwrhUXJedWU13Yx'
        b'/8uNgjmFNXMX061tcr1KQbc10boWBT1/g66lTU0XKdU6RWML3S5rXC1rVkgFgpoWpdaaVq5oUqoVWrpJr27UKdvUWlqmltONKplWq9AKdG10o0Yh0ylo5gVymU5GK9Y3'
        b'tsjUzQq6SalSaKWCxkl2dY1A/964gd5HTifVyepkd3I6uZ28Tn6nR6dnp1enoNO706fTt9Ov078zoHNC58ROYaeoM7AzqDO4M6QztDOsM7xz0mHKEG4INkw0eBo8DL4G'
        b'rsHfIDAIDT4GL0OggTJwDAEGkYFn8DOEGoIM3oYQA9/ANrAMYYZJhglNEag7PDdGsKmucMcm3hjpRbGpJyIcQ1FIpGMIi9oUsSmymop2G7eOWs95jFrH8moSsysb7Ts7'
        b'DP0LcQPwLRhSTYkFlSpP9HTdn5Oq5mBfffJXnDJKH4O88Gwd6ILdcPtc2FVVvgAa4J4qMdxTsmi+hE/Fz+XCVzdmiFl63K5z4c5EbUkF3At3V8DdLHAFHKAEJWwwCC+B'
        b'nWK2PhClkS4Fu8pWFpUkl/AoLpcFTsJjYJce9xA4DTfDp8pQjAR2oRJ4lB/cxdGB3kr9JpQZvwAeX6QG3XBXcjsCaHcJb2YIJQDX2eAGuA5OMNAeg6fBeZTmmg88+CQw'
        b'rFujh9fX+KzRs6hguI8DdsPLwQjaaPy+rala0A32pZRJEnNRBIIa7sMBHlR4DBdsCwM3Gll2DRdubbiLyDkU1okaD/UzF/UyhXrXA2GCF8IBb4QDvqjf/REGTED4IUR4'
        b'EIhwIBjhQCjq/3DDpKZw0v9o0HR5jOt/Nul/llP/s536mLWJbel/l3G2/m8Z3//BLvo/gul/uIhP+VBUQGrclvwKQRZFAo/OZVN41kgtavB7b8lcJvCM3osKQGGpi7+X'
        b'da5NywTOYfMo9EunFm3IKa+eR12gVAIUnCUP4T6YSM1sX/Nx/J/Zz6fR0XmUygtF+LCPsAY9qPrVFfXpv0h/bVohE3yA+rN/rz8rd9Oi+6x/LJ27KpQaofQSDF4XvAYP'
        b'op7vTlmQkAB3pRRL4C5woSahtALuS5aWCNiS0goWpfb3mlaQ6dB13tY678Jd523pOp5Dt1G445q8bV3D/c93jYeLrvGp1OC21Qchpwy8zKteKFkMh7zZFJtDwRNwB+jV'
        b'T0BRVQjhq9kIqc96R1PR8OnVJLQGnqfgwTnVC1FMCzVXv16Piy8Ct4LgQUQppsOhFCoF7AUn9SIUDroXgl3wIGo4NBDPSigJPMfRY3QBg2LwXHXFArgHXgXHeBT7cdak'
        b'ZtCnj0NxAfAm3IdHY1IZGj9d5QsSwIXkYjI5SFlieIEHtsLOGqb8yzPgQXAdVQ4MgQNTqam1cEBZ/0UGV2tCsfs+iT721rQTW7pOHbx+cHVoNAeuondulj47MffYFtaK'
        b'd3dE/WWDj5AzWzJb0ujbyFkmaIxf4rvNd/65zuCWsHm+jfF/Te//alVc394pPxOdC/s+r7hpykyBVuB98aPE7J4T84Vv98ddO3PkDX/RB8/K5uhDly+ha4KXxe9eWh0m'
        b'PFqpUOWvGdqTtcN3Uc4vdsYN+P6o5VzZ5nKPhrW68PYhXahp0lOVi30Ol7Khz49nrwku8Pvpj58ajL7wG+ro29v+6Df/96d3Zaada5fWv9bk3/Ejj4z2cxzqck9xwqnr'
        b'Yt6DSDxzwOfzy+CeJLinQlKaXAIOz+VRE+EQB3aCHvj8Azwjg2PwFXVSacRaCTSUlFfyKG9wlQ1PgJ2aByEounpdWZJUXDpvZZJlavSHmzltyQUP8KSUlgme8satrpck'
        b'olERVMemJsAXOeAKJSTxHvA8whQ0baKO2h0KDnMobh4LXAXPg06x7wg7QaxBQ5n6lo7WFzk0vXns82XQ1CZNW4dCjegvoexSRJUVa6eP+GoUarlCU6dRNLZp5B2Oj2xc'
        b'VjPCvS82U6NPsKigsJ6avrj9y3uXG4remxTb32ScJDFNkoxSfr5zWYy737OH1ZNlFob0TDPTU3qK+tL2l/SUmAMn99T28/q1xsAkU2DSKOU9YS7LTMcNBD4XcTFiUDs0'
        b'xyguNIkLjXSh2yxeJEt0P6d/7inBWcG4dAO8gXXD8TnGwFxTYO4o5eGY+B6dfpdOH8wY4hjpqSZ66viX6IyByabA5FGKZ8s3u3/2AO9U6dnSU/5n/ce/jDvQYvcyDskU'
        b'e97vtN/AWiOdbaKzrRl+FxY9HJM1xEV/i17wvu1tjJltDJtjCpszLJpjFgYdzj2Q21dkFEabhNHDPtGf4QlHg2ccsd8In+mDEY+6Oo1eXVc34l1X16hSyNT6dhTyLRHD'
        b'Dzn1DpihwXOSZiJyxnX+DJy+Dzlf4N5/nMViiUap78K57xdsUHat3r16s/com8cSmb0nGnK68nbn3ef6by7bUrG9YnOF2dPf7Ck0eH8xyqN4AY6hm6uYPy0mTCe8Mqjr'
        b'foUsjsOkbeO4GzBt4R2mFJjfRty2nFXLQf9cJVXLQ798ObvWQ+5loJpYcu52r1pP4uNt96xlwvjIJ0BUiGVgN3HkHujJmzCSXPTkiZ585CzCTQtG+AtJo1WS3vvwH2jM'
        b'NHLsAOJaqcgmDBCL4XEP44IpUjQmcIi97xrH3m/kEgLHcSJwXCcixtnEtRA4l3E2Ard9PIHjuCBwXIb3MIdxKVUH4hBn1vvw4oIp5UeScyxtE4r5aa/Xsbemnjh1MK+b'
        b'xc9/LObXn4TE0Sfznp7w/ed4F+RbPw1KzahnZfn8cPNHS+DnZ1MXb9GlT/m4/M2NsgGZSjHLzLnBkR72+s3VO4q+Xa8XHAkebLh+4aDXO3FF/S+8Vv+jI3xKUScKvZst'
        b'5j/ATGgwHBInIYaQ4QaT+JQ/OAeuLuF0wO72B6EowfSZdWPxwcDAoXySOR7gyAYyja8Ep+DpMtidCi6UIx5ZzKc8wS72+qng9gNMSOsrwVOYVpaVoMmZ4uf6LmeHwu42'
        b'Ere0+nHQXYW4Xy7Fg8fBzhgWfBGc8H6ACf+CDfOSJGCfspiwzZ7wBhtsD6XFPPeDj2edlcmYG/Gsq1Oqlbq6ug5/Bnmk1gAy7+opZt7Vsank1MvThoJNSYXGgIQebq9P'
        b'3yqzKKS37J4o9q4otn+VUZRmEqUNFhpFWT0sc+SU46sHpgykDUw53oYSe5sjJqMfgVkYjEbfhDiU83DZgbJ+rlEUaxLFDlu/oxwUSVJohLZZiD/C1SpUTSNcLMONeKxV'
        b'aLRI3NNgmUETZKsXRpz6ejytMJPJFDyZjK/TMpxSQ6YTMqFo2SxWFJ4P3Dvf1UTxGcblw14S6opfAaeR7WpYdtiGJTMom9hkSLJd8JwcLxdcpPMgRcOOvYljGZIu49wP'
        b'SRtYDkNSn4ye4CDcCo95g53zEePXjTC+OwXuqy6G3Ri1F8xHjCibmgFP8SeAo61Kr1dELO0clOvtKfDYW5kn4pJPHTx1MA0N2bdCureX9v16+U7R9yt3Jmbzdyp2+/hc'
        b'CpWdrtg9c1p56i/ZMZ97Dnedi+/bkuFLfWH0PpLcLeaSsRbfsLxMCy8xL7SOJXgRbn6Au716PXwJXkf80D64TyppJ7wPmwrbxAWIbQI7QH82GZLN4GQOM7CQbHiVDC48'
        b'sq6BzQ8wU9oEX4TXy+C12VUSFsVeyyqEr04Us+1GEu5D6zBCZLFZoVPqFK1oJE20YZ0tjAymAstgmsOhRCF9uuOPDwsT0fe9sNjhuPyhGmNcoTFslils1rBoljk4vLfj'
        b'8KYDm/rlxuAkU3DScECS3ZDgabCcOsJVy1oV4wcCjwwE2zjA8pEriHBfa1XMUEAwzeawWCEY4V063+kgOOSVRF3yy+P8l9ImJ+HLzUBIRE/gFrwa5D1uEMC+7PHjYLlE'
        b'+ZFgHTMM/vHUAkS12pNOPMIwOFE+c0V56qb4bb7FktmpnOYw6hOp4Cc958UcRjbYD7eBHWX2wyCTzV4PLj7+AKs8wG1wVGE3EMBu2Gc3GHaAo/BZQmGKSh0ozFG4FQ2E'
        b'8sfFnPHEg0NQfgzntS5wXuuA83kWnK98BJyPxnRF0JdpDKCHydeeCBCM10jxi3lrZSq9E96PJwBZjohvA6uFcqQBFQjzJ2Msd+98V+ivwXKx67mfoD3HNvdjDQTVxP0P'
        b'zv9O6kCeC7TnVepTMGJdh7vAYayQq4d7aqBBIpEuKC5dBA1V1YyQX4zkfSmL0sGXvfiesWSoZMO+pvEjxTpMcJB1qER6KRckLeNolSiP50v+x95KJ5L/CwevHlSGChnZ'
        b'v+EfE4uMb/Jzi2XL+e9f2dmdmbY2/cXU1996N92Uqrsmf+17P8RDaun+B2nvpNZcTUvt//iP+zkfNez8NHgwtZ51omVtevrZVG5G+/MIsY6LLv5lBxLHsRbR9wlwakxe'
        b'hhdjUqwCcxncTyRmcBPujbMMOBU4byM9Q+DagygUr58JXnZBeqaAfWTADVUz4/YmvBVsN+JYxeBVRG3OgCOEqYtYyk+SII6ueY2Np4MH07+WqbMJUiN8fTuWrDt8LdjP'
        b'PJLxuNEyHpdyqJApPR39MQNcY7DEFCzBXFch6z0sKs4whs00hc0cFs00T6JHKfaEeSzG7ZmD6FJ/5tmC4WAp+r4XKR5OnH5HZEyca4wsMkUWDYcUjaJyU+4HiHoF9wKi'
        b'7gZE9ccYA+JNAfHD1q/dmPZgxjSeqsYNZruqeVAWcmaVEqfjce1Ys1accC1lpWVLHkrLvnuqxgxre7WiI0vHIWpFog+2UDKsRuT829WIzY9CyTiVyi/29/K0eFr8Wfzb'
        b'WKCK2hF1Yj8ac88clCDy9FRaeurlpu3puZ9eXBoasip085/b9/PKfZbeSadX+n7wQurrF1+n3nkn/d30qGMvbw499suwopqC1UdW960KWdXXuvmTyEX9/7t09fDywB/d'
        b'OcKiLoeJFv2EZ+Hi6tjAsBqcKRvHxu1KI6NgRtwaZohEZ1l5Mzg0j9ArsKMuAHYjvm2PBFE0PsVfyY4G1/xJocFwD2WVpEAPuIClKXYoeDoGodsj6CYwutG0nYDkgUiH'
        b'ToMonN8YKcHPZDS1WUZTC4cKn9wX1B+N/uRnVxunpJumpBtD03v45uj4s/n3ojPuRmcYo7NM0Vl4JMURZ39Zz5y+WHPIpOPe90LEd0PEAzHGkBRTSEpPoZmOtWl7gmN6'
        b'NvYvNgYnm4KThwOSnWmi26FDKKLdyJmLR864amABT9tOWRQszWjkTMRjw73znQ0aTEgQgmpwp4l9sSCKudm6uhFBXR2zxIf8PnV1a/QyFRPDUH/PRjTim9s0G0Y8LaKg'
        b'VhNLZr0mpUIl1xLJj7C9hAUg8wWp+tdNoHaaKKxZ7bBoU6px/OtMR1v/7guDDXguNBSbg0ORExRmmGcODDYUjXL5vqh33TkBHN/kUcqFI+D4irHPyRHwfRNw3oc4ATxf'
        b'NHs/mkOwhywZhM6Fu7xLK+DeenAupZRFefqw6zPjnDgA/PmsHs9irHEKLHYtV86Rc+W84+xaHpvqpeT8fj7l4iP3cFz+dXyq9ZB7VlOI/fAa4c9VIx5tw5eiOYoGpa5N'
        b'o1CnlGkUcsb7YQDBlw/xHPblxMUKTYe+Wdsu02sbW2QqBZ2BojC8X/qUK3QdOgVdpFFqdRfYBL0+/D4arZ8fmUhRZW1qXVtBJUInOqFQrlFotQiZ1LoN7fQitU6hUSta'
        b'WhVqcYHdg7ZZ0YxcnUwtd5lPLdPB2xqVlJ6PkLEN5V3cplE/SjpXha1WKNUKulDdLGtQiAsc4grK9JqOBkWHQtnYotarmwvmLpKUY6DQ76JqnaREXqmRFhSqUYMpCmoQ'
        b'q6tKKVwtk0vpeRqZHBWlUGkxA6wi71Vr17ZpUMkd1ndodAXVOo0MnlQUzG/T6ppkjS3Eo1IodR2yFlVBFUpBXodaXot+O/R22a0PDeswdFh/S1sAQUFSulavRS9W2QFP'
        b'p7mNSS8oU6jVHVK6rE2Dym5vQ6WpO2TkPQrL+xT0PHhbpVM202vb1E5hDUptQY1CpWhCcbMUSEBejctNsASJrXH0PAXCHXi2SafFtcRN6pyanlcuLpgrqZApVfaxTIi4'
        b'oITBE519nDVMXFAkW28fgR7FBdVoukJAKuwjrGHiglky9Wprk6M2wo+OrYZDVmMcllTqW1EBKKgcnsUK89W41ZjmR4ElsworcZxCoWlCkyLyVi8pKaqRzG5DfWNpfDIW'
        b'lOoWhGu4HEuzF8v07ToJfg+aXRuklnda/A7t7ioct71DJdKdKpHuXIl0V5VIZyqRPlaJdPtKpLuoRLq7SqTbAZvuphLp7iuR4VSJDOdKZLiqRAZTiYyxSmTYVyLDRSUy'
        b'3FUiww7YDDeVyHBfiUynSmQ6VyLTVSUymUpkjlUi074SmS4qkemuEpl2wGa6qUSm+0pkOVUiy7kSWa4qkcVUImusEln2lchyUYksd5XIsgM2y00lshwqMTYQ0XjSKBVN'
        b'MmZ+nKfRw5NNbZpWNDGX6fFUpyZ1QLOxQo+mEctDuwZNyGj2U2vbNYrGlnY0X6tROJqLdRqFDqdA8Q0KmaYBNRR6nKPErJFCwpC7Qr0WE5QOxB4VLIFnWzSo3bRa8gI8'
        b'6zE0VqVsVeroBAvpFRfUoubG6RpQpLoZpyuCZ1UqZTOiUTpaqaZrZIgu2mWoJn2AY+aTRV77wsbIuKQWQYEmjASc3SHCkh9FxTpnSHefId1lhgx6lkavQ9HO+Uh8pvsC'
        b'M10WmOU+QxbJUCFj6DJpc8SXIP6EhOkU63U2D5qJbN4M+6RaWzKmI2YpEDlutguILahVqlFv4P4n78FRHSgIk140Szs8pjs+oulHptUhaqdRNukw1jTJWhD8KJFaLkPA'
        b'qBsQ2tp6XKeBZ5sREpWo5cq1UrqIoR/2T+kOTxkOT5kOT1kOT9kOTzkOT7kOT3mOb091fHSEJs0RnDRHeNIcAUrLcsGm0AkLLa2qtTAa4jHGyFWkhVdyFWVln9zF2aYy'
        b'F/FVrt+G+S5X4Q6smPs6PCTeHXf2TRKnu3+zA5/2KMnQVOkqmQMJyHYiAdnOJCDbFQnIZkhA9thsnG1PArJdkIBsdyQg226qz3ZDArLd07Ecp0rkOFcix1UlcphK5IxV'
        b'Ise+EjkuKpHjrhI5dsDmuKlEjvtK5DpVIte5ErmuKpHLVCJ3rBK59pXIdVGJXHeVyLUDNtdNJXLdVyLPqRJ5zpXIc1WJPKYSeWOVyLOvRJ6LSuS5q0SeHbB5biqR574S'
        b'aIJ0khVSXQgLqS6lhVSLuJBqx6akOggMqa4khlS3IkOqvWyQ6k5oSHWojwXEIo2iVa7dgGaZVjRva9tUaxEnUVA9d36hhFArnVajaEJEUI1pnsvgdNfBGa6DM10HZ7kO'
        b'znYdnOM6ONd1cJ6b6qTiCX21Gt5ub9IptHTV/KpqCwOHibm2XYHkYYaZHCPmdqFW8m0XNE/RAG9jSj+ObWhmwi1cg/Up3eEpo2C+Rblil9lJ7ZLmHJTuHITEHBUWimU6'
        b'zJfS1XpUnKxVgcioTKfXYraWqQ3dKlPrEXmhmxUMmiJy6EoNILbLosTEXSkn2b42sYvyXRAl12U7JyQqprHWoRHzTVtYXtKUTTje0siMP93Oj2XCMU3Vl6yCyguemiKs'
        b'fZyHnWLKstypKcFOKdZw8rTtKqVOU4Y1YSxGcYn1aBalZQVRWjI6NLzMo100XmkpxkrLUEPxKJ8KSjEHJox6cEP8RinkoDABFRTes2iUmzphNuuvDSzKX7RL0TO7a9Xu'
        b'VZ82szKCwh5QyDEU4T9Gi4g1a/D04x1avIG1qzgxGVzgUp7Z7E3wBjj9f1WRKChsbGzTo4ZQN4/4zULYxgg8snaF6sNARo2IFehfhs1B+NeKmBqsEKcZkQuNHiWa81AS'
        b'vLNvhIuZL00N8n5+GwUsamV4qbYWtYKublOpUorRZKiWlHVg1c7Y49j0WrCkrJZmsmEVHp64tUqtngnAcfbPzHCfhzWOjGjBvGjWIkl1Y4sK3kZop0LskP1jwSyFStEs'
        b'xxVhvBZ9z5g/3SKaFVhbgogamBdVWGYVq7xIM/yYReoc049Z5E0iJWBJEyVG41pHJBJLCeR1KiVKQHxKdVMbLaELNTorKJaQEjXOOS4QJ0t3lSzdKVmGq2QZTskyXSXL'
        b'dEqW5SpZllOybFfJsp2S5bhKluOULNdVMsTeVFXXpKGAMqZjMJutIIHpToHoga5QoKnaqgSm9VJ6TAmMAhlctmplpTQWFawCP6PtHetGujypvKBIr15NTlEpNM1obuzA'
        b'8xkOn7WIzsxjKHyTNQnWRrsKt+ANE+WiwIJaIongimtaZTjShiKuYmyo4i5b+sOyuY5kUOgh2VxHMij1kGyuIxkUe0g215EMyj0km+tIBgUfks11JIOSD8nmOhJny3tY'
        b'NteRpLtTH9rfrmNJxocjintMSXsoqriJJRkfiixuYknGh6KLm1iS8aEI4yaWZHwoyriJJRkfijRuYknGh6KNm1iS8aGI4yaWjPiHYg6KrdbB242rEelah4ivjvDE6xRK'
        b'raKgCJH4sdkPTYcytUqG1ZraVbIWDSq1WYFSqBWYHxvTc1ooJ57wCvVNWCNnm+SstBRF4Zl3jCDTCYXqDoYXx0uJaDKuUOoQaVTIEQci042LHjcPO2cem8nHx2lU8Hmt'
        b'hU1wiCkmC0tNOsSV2CQ6QkkkhN9xKX5Yamqh5oj0I0qDufcmwre3YgKvUyhRs+hsKuoSxGTrlE3K1TL72b+WSKA21bU9m8HIrXZLmPZsUpGCEWoUygYcVY56Da/JaRnO'
        b'xj2jZq+WRnCjN8tU+tbViharDp0QQcLFLUFcXKVmqWvuGW8N77BjHG/j+IXjOehoOw46xxxIu+SgQyZM/Wu6Pf+cE47Z53BH9pnG7PNtOAReBIdV2vJKuDeFMNJwd5kH'
        b'FdjA9SmDtxy4aB8rFx3HRly0yJGLRnwzv9e711vO7hX2CjE/fZl3DjG5lzys2b3QnzzGwDP4GoRNHLn3di/HzUO1XHyyW+6znZL7XvY7h95xybZTsZZP4vxRXIBTnAeJ'
        b'm4DiJjrFeZI4IYoTOcV5kbhAFBfkFCcgccEoLsQpzpvEhaK4MKc4H1y/JrY8fLtnra+lTYTj/rwuTzonQLkEDi0Ta2Bb2oYrj3BqGz9r+/YKellNuI09iGstMfIcEg4u'
        b'eY2VKI8zMPs48aHfAFSqh3yyU6n+8niUimfwJIeDJ5JU9Hav2gAUNgHVIgrVYgJ5s/DyFEdpx3LA2M/g38STR2/3HFfyRCILbRcnjHjOwWfsZlcv/jJFQNt9rME0M5Ey'
        b'B+cdUlzgaebjkYEHwYdYINOsxD68hZsIRGKfDzE4H+LW/xDvDB5Lrmm2JtfgfWWaepwEt/eH+MDthxiTxR4jApl8LZqbNXVK+YhXI5oh1Trs9ZMxg7BOhVhcXcuIZ6Me'
        b'TR7qxg0jnvgUh1Kmsmz48W5SIq62rhVNXC3k3SOcuYsWMjuKNHj/aKMnNfbBryeb356irFtt7U/4k4O/LIQEXIMHaljm2C+/SUD26yE07hKM26/nRfbreTrt1/Ny2pPn'
        b'ucnLsl/PZZz9fr3P8elbh17AnxKm2soOhZbYR7D1nZJsTGlUSJ2yOAXkIyFO1kqPNXm+xTICmqixOs9iesHS9jK1zqkE/EmYheZXnXV2F0vpQpwfzcSNNNmUTevbaUSP'
        b'cmi5slmp0zrDZQHD1tuuoWCiXUNgW7T6Ghiyvg4GRzTLp8vJLwZhXkq5NdYCmNY1LJh6Y7qJqK6UrmlBlBSNJgWt1TeoFPJmVJ9HKoXZEcSI/KgkWoaKQM8M/LSqDVF1'
        b'jZQu0dGteiT4NShcliKzVL5BoVunwIv2dIJc0STTq3RiYhgj131fWIZXPj3b4qMbsdY3wbZWbKctFrsrxTo0863YqrV1JrbD0aahE5idR6vhbU2HQuW2IMumvnwis2L+'
        b'DhXD4IhlpkpQNEvprLTUZDonLdVtMXZzQz5dhB9o8oCLa1Kq0ahBMNIbFDIEWKJasQ4vXK/NlmZK0xLFzk31tTvjfZjDihdnBFA0NVTl0V7vE11SS+lnUlhJBs/A52B3'
        b'Bbg8HxpK4J6yFNg1H++WL4aHS8rFsDu5UgJ2wX3lC4rBleLKioqSChYF94N+nza4FW4mJb/W5EOFUEuF7Pn1PuX0dEqPTxOB7tTJrsvdC7vKETsBuhxL9eFRcPsGHyp/'
        b'Gim0pMCTCqCGuNz6ep+YvDJKL8aFboMXwHHbyf3d8Fl8er9YKkksRa8Az3Kp7OV8bRI8TOwPkHI+jvdA7Mnvqzzp+uSV+TpKPxVX+8W2WFfAQQMqszsZA7hbvNiuxvx1'
        b'4AWNN7gmhHuUf89IY2n7USlNj+fu2VfgB1J9Zv7hq2q+3w9YL8qpF+nXvcxPUK+PXChL6cp4PWFy1JS5Ru3pv/bee8Df9X5zQnePl7eY/kFBgHrqzxUrq8H33v9s0xNL'
        b'JxQu/PxS/IGGW3/8xUfnl/m/d0778Tt36ltv//VPfwr/w1fJT/0i/slA9Ytrjdue/fjFv+x887k/Pvd82wioKPD556SX1q7lfxp+bunvD/zp3C6/hq3C1z/zgFUZkzee'
        b'FfuQowPwuUawG3SnlIFz1dZDoBzKP5bTBLubH0zGzXo9RgO6q+y7m0WFNYMBuI3bUR3BlLI9H+z2Rq0urtBbzg4ECsAp0Mn1DK8kZ9vAVs9EVIpD/7KoIPgK2BrF9UaY'
        b'9iI5vKaGe1KTJAnFkqQmNsUHR9kS7nIGivNwDziHSrB1J9im4VITwbMc2J0nYLZX9wb4JknFcFcyMIRRKPtldsYkMEDeHwP3goOgGxsMsPXhBnCUT01cywEvw1PghQcE'
        b'hwxgVxCuLQoxWFhbDKsFDygqFe7gS1PgGeagUpfXelyp7uREKU4F98CXwPNwXxJOSWt5vuBoPTleAQ7Cg7APJ8WcMn69ZCW8gl4ODnPgjomwi8AId6xF7YFe7shTh8Gj'
        b'rWCIC7orNWLBtzi2jhmI8UfWySnTCVZ67Hh21tdis2CtBxWFTzb5mqMlPVxTAG0WBvVk9Gh7tH35+5/sfdIojDcJ4wei7gqThoVJ74XFDMcWG8NKTGElw6IS85QklNV/'
        b'LEve/k29m4zCOJMwbmDCXcthKpRlnjGs2BRWPCwqNkeJz0eejjRGpZmi0lBmPyazzpbN/k05xrBcU1jusCjXPCWxXzrQcC8q525UjjEqzxSV5yqz/TuLjGHzTGHzhkXz'
        b'7sdn4arFmGNS8G+UOSqaZI6OJTV2Os7ly2xdx/vnNXj3uWYNdvCpLI0WO5i/0+ioh+1ux+Yl6i0fu03ubnrkQ5xlgGJOfX1hOfpV5cFiNbLwtvbvzv1ODQuc8cqjXvAr'
        b'9OA4nC5hWenPREJ/nqBW2aLIAgirUswa8a4bY/WQuIubm4i7NGmmLz2nqmStDXLZdLu2sgZNQOnI6zdTfTWmCMlmivTclxYybCnXyrIlIPIul7SpVRvEF1gjHHlb4zcA'
        b'tpkBVlBnYwidYdV0OnapFUwRSkIOlGIwj9dZoZzMQMkU6ALIbw6df50jq/joIAY7tmSaFUbxQ3nNbwltCwOtV52VoXt0OMMcmnKlFczQWTKtwsYf/muN6FVn5RAfHawI'
        b'lETTixMQcKLdcpbfCrDtDGCedRaO89HhonG32pprhbW5ot1yrP9Kf/rU2bGyjw5jNO7SMdST2lDva3hhN6Dajo6tR84htuVEm9VEwX/mPNsjmSjgVCr36AZYWrx0/tq5'
        b'OoUC2xzAJ0iZw9aW02yf9l/bbVZc2pzbt+U6jyq56Cm98Scxm3BImjR4YozD6IdPYy7DymJwNzIcxulM8BToLl/mxGMQBkMFbri1FOBRh2eRurqOADsaRUII04CPymLS'
        b'VOpFhYQjcp95fLoxONEUnDhQPVA9KDKlFRols0ySWcbgWcMBs5xMArgil4xFAEwiGYQ5ixHG6e1xGKdXU5aDYCVe/4kzYGTK6fVKpC765XLEghEPy0TIHPTia3UahUI3'
        b'4tneptVhiXSE26jUbRjxYNJsGOGvlRGFkXcjkovbWhlFEkcnax7htaHpQdPobYcrflZcwdU/xHVt4BEhta/l9LWnwd/ANggwkhsCDByDl8GjyY8guzdCdr9xyO5DkN3b'
        b'Cdl9nBDae5OPBdldxtmfx/78PZ4LZVChXK5F0j4WWeWKBjz9oW+jZVMyrSDbPx5BH0S0FUTVIKNb9M0KOw0Mam+tskGFzWTiA3VYmaJV6KR0FZoVnMrB83ArXpBWtra3'
        b'abDiyJqtUaamGxQ4Ky1XahSNOtUGumEDzuBUiGytTKmS4VcS4R1vaddKcU2VeGkBzU2WIi0KEFymUxmoaL1WqW4mENmKoRMJKiQ+QosUWWrbgrWhzrA7pU/QyTTN6B1y'
        b'62SP89N4sUSLlQnaNXrcug0aWeNqhU4rzn90HR0zCvLpQge+gF5GtoescJcNvzmfJsfKln3t4TK3pTCDLp+uJr/0MstWZ7fprYMzn8ZLPairiO5omf1WZ7d58XDOp2cj'
        b'l15WpdG5T8cMeJSU8ZB3JNMl1VWSjLTsbHoZXt5xm5uZJfLpxYU1kpI59DLLnokVScvsj865f/nY5II1ZMwDjQuyP7DhNjuajlBjtqChgYartlGjbNdZWASMp9ikERlb'
        b'hSptG8Jfhdylcg+hE06NabWKGK8lnS2l5zAaPjJEp1TrZK2t+Di8eopbXR8ZDAixEADtlqElVxLzuTLUrOuUiCdQrEc9bhlwzuXgT2WbTsEMEzL4FbqWNjmaSZr1rQjR'
        b'ECyy1WgAokGjQK3TqKDbEH/lshymSnjQENWllqmmUmsHkpQuQpOadUJyWYr9sMOKToTq2DhwowpVmLELrFW4zllvMQ3c1kggZ1aTp7bodO3a/JSUdevWMfYJpXJFilyt'
        b'Uqxva01hpIoUWXt7ihJ1/nppi65VFZ1iLSIlLTU1Iz09LWVOWm5qWmZmamZuRmZaalZORt70+rpvoVacWMmsE14H2+Hz2nIxeDmkVCKtxEffk8CFZIqKqea1pKQRm57w'
        b'sl91BqI6YA+VRqVFw4tENXfcn0t5Upsn8WfW+4CWKkqPLbKAQXi8qMzKuyyABmyBslSyEJusWZiAzVcsgQb8g1gacAA8PRc85wUPwU6JHpuvyNkIb8WAQ/A63Et0NB4U'
        b'Dx5h+/jB3cTSLni2BT4Pr0vhnrISbPADlY3tW7Kpyfop4BkufBFeUeun4YTn0pZhE0u7KxbBnvZysX3N5kNDJcq3G+7ZVLaoHfFWVeWl8BCXgrvAVm94ttRTj81xwCPL'
        b'l3hLxfAleKIU3AYnBZRXKRuehCfBC8Q+qXLJJng9Fh4oQQWwKA44zAKb40GXHuuScmrh097QkCKFXeidyeBCKXqbgUXR/vp5PC4w5BCTqNmR3vB6SiKLYs8AfcWs7CfA'
        b'JdKsC2dijeedtTy6XlXblkcRcMAV+IxA64ta6ibzRs/l8MAi9jwlOEAMC1fDLnARx/v6SuF+eLMcXk2CBzhUMNi2dgMHXA4Bu4g14yp4a6q3tAQOcnADVGALVXs4VCB8'
        b'gev/WIYS3qjkaAFK9vOhN1qHywRgpg//vjxy44w7J57+3rL1O2YW5ixcfiho1/0pHgG3Vuh/G1sxL/83w1ueavuyKv3sTz7iCZaueetvoe9mJW2+VbuO82Dm0F8/bCmR'
        b'1O1tuLDnd+KlP0nI+n3BV384eyvnw8pfBl8fek+9673Lbd7ypesWLH183ruaYyvUvy0W5cWeNl8QxVYu7s1XnP7RmwbN+RentVfM/N7svzftv/HVuZoAbsnvDny0q8Y/'
        b'IeP3Wcd8VJcjj93/ScXaz5anRrFf87r7P5wj21K9f4Jt62EzqPAwfG4mUZ4eBJsdtafgivABNq8RqoRnbQhr0SR6wJcZZWJSBg+bmgVPkdKE8FlwBCtRwXaenR4VK1G1'
        b'4KUHeDyBW0s32Hj8aHDCnsWHB2AXsfUi3LAhqVIyHRwsKakoS4Z7xFjPepubngsuEksTYCAdHCxLTgDPJhUjXEe9DS6xN+SA0+KAf8VuqkvdI3YcLGba7FMIZHJ5HcP1'
        b'dQhtTP1YoIMqslxAhdF9Qf28ft3ZjcbQLFNoVg/fLAztSzFhrV66WZrWU9Q3wyhKGlM45ux/ovcJozDGJIzp15ni84cWGOOn3xVOHxZOJ0rA2XeajbEVxrBKU1jlsKjS'
        b'PEXcw+9Zt9/fLM5Enk3GgDjz9Fk9/OHgfGNAgTkmEQVuMGINYQLyrd3vZxanWdPRMcin3++LIMIWMnLNCdIBzSBrQHMZW1rNM4pizZKMwcLBWYOzLteikOlGUaI5KHQ4'
        b'SNy3vIdjDhD1+t0LEN8NEA9ED2iMAemmgPR7AXl3A/KG4owBhaaAwmHr105wmsAITpgZZ/Zbn8cOVhVqLmAHG/XWYDZdcxk7V7DzrBtRy67HcOfUj33oMfM8miEsgLnq'
        b'KzGWwSBlp6S06Cm9vns95b9df4mFr4tehUgKp/wK/ThirxEfOd4cb+FuR3wZmcX6yJe1kl9s5VEx4mXZl9SoGPHGHCbi6/GuZaYfbF3QaNvCgT4BVvKJe/KQhysB7zAx'
        b'5Y2EObzKzyKW2L0ME5Cwhy21E4v9TQFExBO4EPG8iYgncBLxvJ3EOMEmb4uI5zLOYb1/n8fDRTyZbUMSzVjEfQRBZi4+fsikphE3hfALySiIQ5TZ34WAuchkulnTpm9H'
        b'sUh4kjlzJ22tDUq1zMqvJiJWNpEwWgyfhRVwtvMWGECbKsmpJKxa+v8y6f/LMqn90M3HHcWE2FTXXyObOox1Jj8TZC3AJYO+7GtOQrh9HTOXMO+xTB+WMEbGUbdhDaiG'
        b'SDFq17LJujYsRChbZSo3UtCyh5wFQbKl69MgbiHGsx4Db0Nb22oMLw6R0hUW7JKRZ7qtYRXqeLrNtUCFEATJxLnZqWkWzTNGBCTQ4+KWjZ0TcQuEbdLNpxdp9TKViowM'
        b'hDhr25SNttG4zO6YyUPVApZJ27EbyNH3ZfZHUb5WcMfZxwnvDgce/gtk71mKdYpmy3bV/y9//xfI3xnZqem5uakZGZkZWRnZ2VlpLuVv/Hm4UM53IZTTzF6flgzLrSaL'
        b'T83/aUESpU9HgeV+cFtZSQXclVxilVbq8he4kqufBC97ZdbA/YzkOAT6wK7xEnWVDzyg1ufi+JvgZXC5TFpagQQWW8kuywXdsNtrsgqcBy/Bl/SFWNIVgpPaqooqi/VN'
        b'/IIlsAdl2AcNSLgWIHn1FfiqLyoUhb1QvRwcB0fBGS8KXIJPeVeCHdP1WKwCnRFgm7Z0E0AiaUlFVRm23ZnKpUJmISFVwmxnTgbXy7WJmXBHBdybgHd6SEvAlQQWNbmZ'
        b'xwM3UVXx+grcAY4v94a3wN6FnnCPpBJJ3mwKvqCYmMEBpyaG6OPxu54Cl8FZ1By2y0OKS+CW6ckl4OZCfIFIGujmrZ+2kpQHuthwv7aUAFWSLIZ7eOgd20TwDAe+lAif'
        b'Jl3FnWK5qmZxzvp5nBCK0ZfsTg+rhk97o56toWrAkEiP7cXNplDTnJ/sjRsKteh+eKu4HBUOD8KbWCHRDS6hp3K4txiL5MtDPeeBzfAWURWAvfA6OKZYCa+jhxKqBF4O'
        b'Zd6zBXY1gtspGcifRqXVTyapM4LgyUwUhTd8plAp8DQ4qfrin//8Z5m39a6cXxW/EjCb2V/Vmme5f6fozWlT070o/SwUuB4chXtx8+yxKHGKkxfjS5hSShchlCiGu6sT'
        b'xAgxlgiKbTcvicHzpP34at8VUniY6Eg6VsKBangooxTe0HEoFrxMwcvwxRSyv2zydDDgbemkhWMo4+miccCz8AAXIckir6hpj82Gm/VYloLPw+1pYwqRBbDLNwEeqvZ0'
        b'VH/MCOT7gRNgL9EelSLh/qq2VFIFb8CnK1IwFlVaFCBi2McDN6aBXUQLhdKdVyVhC3YppWL+cjBEeYNX2fC6rJpcFvTlukr263xq/WDJVN+fL/1zoJ4iOid4UoaVU1jf'
        b'tV5fKlnI7JZDKAa7UqoqFiRYyrPflgZPgPM+sAecmkDaC56EQxlJ0pLkRBbFB/vYzZNT4FZ4Qo/XcDPBSW80MFTlZSyKrWHlVi0Sc5hzstubwUW7TKglDSngNniZXH2l'
        b'14ObKBvcUWLJBy+AE6SSvAi42VZHsAPctlSSNVf5yYf72NqNSGJc7PHjKwvLKmFqwOc5XT+tOxpUKlblFr2zjFanJi5MihIlBh26Lmv+i8G3+9kXf32g/Hj+nm0/k4mN'
        b'xz499qvwJ+Unt0+IfvvO7pzXT0RHv38s79LlkI1faQ5Gin85vPODx/pOvTbzr1/8apcg+G+V2Re8Ug/+8Yz6k/CsC3F3lhiOrXpzRo0wzmtx2eDRyxeP+CyQGz0X3L6o'
        b'1f5gbp3mo4vNvW9ubN0V+WVn0d/+9qtDC1K8n/NXxH80uvWE+HLfiLTh960fJ054YCwYuF01caffz49fPflruvj+nTeaD4nSK+pKrl42vfuA3rbgyGTebzdo773w5raP'
        b'qjJ93x4KP563dMbWC11PfvaEd/MrgxfLvZXnWlbUlrX+pilu5+LfJP/ilOaLs6dNPnVDutJVRw42C66vvdG0eqXm7TSpfrrpg1Otqzc9/apocR5ryZOr0n9VK9llVL97'
        b'9/38wTWsbm3Qrc9G2tZtav60orv6kmT1q7+Tf5H/TvSWn6esFEi+eiVp568+PlXFnreuqZ/7xrQFH0++7bnpz6q/i33Jxr3CDWjKurEY67DG6a+OwZ0P4slsAw+yiQYL'
        b'ngGvOO2HIyosBdhDNFgSL9DvuAuwEV4iCizQCQ+Re3/yFoItUZvK7DZl+i/mqPzSyAa+1RpgSEokO/jwfNvk9RgbPCNYReLSCxuSpJhYJGNM3MteAA5KwNXUB3hOgkOp'
        b'VFk5OFmYyKfYK1g5cEsFyVOJpr2b4FJ5RbK0Hk2kZSxwDb4KniNasIJm+AwiK3ssu/X4T7DXg5fjwY4qZrviUDC24uox3X5v39i+vihwmUl2BfTAUyjh+idcLqgLJERt'
        b'twjsA1e1eGRKMNEjjTwB9nAS4fNgEF5/nLRMvTCsLDmB0cjBK+Ag0cqBy4niwO9aK+deXYcHNeElNm92pbPzwyqfMcm+I9hBFzQWQXR3z7MZ3d0mbyospi+sf+5A5uVp'
        b'xtA8U2ge1t1Z1XRTjcEJpuAEo1BsEooH5piSZ9yJMibPviucPSycTRR1hXfKjbHzjWELTGELhkULzFOkFkWdrYxpxmCxKVhsFCaahIkDNSbJzDtpRsmcu8I5w8I5pIxZ'
        b'd1YYYxcaw6pNYdXDomrz1BKs2cs1BuSZE7Aab6MxINZO8RefdHYj8j9hDIgxCyN68vvk/bONwgSTMAGbm04xhyf0TRsQGcOlpnApMS6Ng+eymJ2JQ9HoT/6C+LbYGGt3'
        b'YVF8kq3E0L7CA/k9+eac/J6i4fAMoyhzWJR5f+zJHEH3VfcHHVl2fNm9iJS7ESmDHGNEpikis0eAKt2XOCyMQd8BIfqrvSeZdlcybaiR2V5xJ90kKTKK55nE896Iuisu'
        b'GxaXEaDK3+gwxj5mDKs1hdUOi2rfyy0Ymjc0707RG4tfqzJOrTFNrTHmLjLlLsKtkmkMyCKaTNaEqeasAgxUmlGUfj8q9mxoj59ZGNyb38810Wl3hWnDwjRzbMagzBib'
        b'01NpDg7D9rUjpYPcG15D04eDSns4GNwYU1giYz3fHDnFFCkd0JoiM3rmoeRYS9ufZwqXGIOlpmDpYOzd4Jzh4Jz3IuOHE8qNkRWmyIrhkIr7weF9zf3NKOddYr7bnJTS'
        b'59HvYQxJGA5JMIdG9HsM8M763Q2VDodKzWIJiuMd8fvifkLyYM2dhuHIEvRFb0vO6JljEsX0VxtFYnNAcJ+XKWCKRekaZwxIMwWkDVu/dkpWIaNkfQE7L2LnJezgM3aa'
        b'l7HzCmVVsj6ifnX8iMOvGq9ttSlcf4LZHHeDrBYrXX9MOShd0XBbI2CxlEQn+p91v1P96yWvQhb1Gsuv0J/TaDXCgT+2aw8PUI660sOUwcPgZeCSiw/ZBh9y0ZSvgWW5'
        b'/pDHprrGnXjayCd6UZ6TXpTvpPvkbeJb9KIu49zfwOFKCPNjhDABl4M4e7rQh6pXneG0UjUkNHIFZqLnN3Jm1vuUpyF+H++Jh1dhr68W7PFcw6E4ftGtrFyBhEgb00Ev'
        b'OFgN9tTAPYsqFsCb8+FNuB2cWuSbnZpKURHBHLAF7oRnyF2ksA8ONlXDPTVZqXBXJpJ/wCuwx3MNC/bXrWPY0m1wZ7W1MBbFS3wc9rHAUS3YSYQBQUk7vugQHIRHqanU'
        b'1BV5hAH0BzvhADwDn0FzfRy8togKgS+nEzPNYO/kBWXS1Mz0LDbF35QWygJPw2dryJuaIuCVpFJyLSDi2AdtVwMm8JTvLv4VpY1CiP2a6IsT1S9Vvp4asPznVz+7PbV0'
        b'18H7dV+wBz5M9vtdTE9C1cf+g7q3Aw3vLjr6vyV/2fzFb+6fpe++FfanH/3xcuOTvSfrMzyutvXnPi7fvE3S+szP9vzq+od3uuC8r375s3PNK1/z/NvxXx8N/3RkSnno'
        b'9nM+qewXrjye9sc/PLns9Y9K5bWTdnU3eOTnpf0mJrpz/v2Lh7tDb/aVPBd69PrM9sc+Kb8x6Y2//6wq4LTwp9fpk3872/xesGzylZ6KDzb+j8fntxLT3kqa9enzL7e0'
        b'Xr+ftuKvv//8b/988Pz/rq3hBX74z6+eTV4amJbzww+E3R6pb/rtnvPhR30z/vzKa/K3o7fFXvnxcuHPT763M3vlul9+b/FfR3WrTbt+GvROx57fnvjxb59uX3tvefCJ'
        b'gWHFF4LJUU/+jX33b60JCXvFEx/gDlgDexeR+0M9uKCPYoPTrEWZSwk7UQpehs8R3gdzPithJ2J+wGV4nTA/CBsGmizcz5PLLfxPPDwkfIA3sIPtSDY8wRxsAC+JXPA/'
        b'4JSSsI/gFDiET2XYc4+B8zH/KIUD5MoIKWLBjpdVJiNRbl8KuMilFs32A69w6iKExFi+AGyZBrvLyA2Q3MhZ4AILnE4vJBeXrQCn420Xk10EL+Gyyc1kr8AzZJ2TBXfm'
        b'4DskrTdIVkaQOyThKXiEWZ09Ap4SlzHnViLBkPXoShC4wg1vmE/2TBbAPaCzbNyhlImrOD4c1FQ3k0lr5MvApfEruFbeN2wdXsA9Bo8zLzwKb87C549sJ0yQ9JvkH8lZ'
        b'CXaBm0xz5IDn7ZnfWvAM5n/hMTbTL/vWe9qYQMQABoEz7A1IhHuFuX7jDAbCcu0lvvNyQxsLXIWd8BTJrEDS136HSwng4WL2+uYIEjsLdINnkLCGaluFr+cAPSUUuw1c'
        b'yRBP/DcylFi4tKinnLhJjzrmykT7PZ1MCOEf37Hwj0t9qeDJh1UHVPvVvWrMUWB+rLlfdnzVQKJRmGUSZuEbKyebw+nj+YgXmxR1vKxnrjkssmd2z+z74ZHHc3Hg5OMl'
        b'lkCzMKQv0xSefFeYPCxMNodP7o86gpKMsumwiWZR2CgH/d4XhfRWjPKQb5RPBU7qK+wtNYniRz1wgKcloLdq1As/C2wJ4ka9cYAPFRjSM7uPc9LnqM9wbLYxJMcUkmMU'
        b'5ZpEuaO+OIEfFRg66o99Adg3AfsmYp8Q+0TYF4h9QciH3hKM/SHYXzkaiv1hzAsE/XLMLk8bjp1uDJluFM0wiWaMhuMEk1BiDG8EfohEqYdFeX2z+2b388gtm+uNdK6J'
        b'zjVOyjNNyhudjBPRJFEOScQ573PaZ2ApcxWncVKOaVLOaBRONAUlGo3GvhgMTcVoLPbHYWhK+gpH4/FTgvVJjJ8SrU9J+CmZvETcN+d4xagEB0hxVVOwLxX70rAvHfsy'
        b'sC8T+7KwLxv7crAvF/vysC8f+wqwbyr2TcO+6dg3A/so5PTwR2exqNDwHt79gMDDPgd8+lb0rRjINkakmyLSjQEZpoCM4YAMa1z1yaVHl/Y3D8jOrjLF5Rgjck0RWDow'
        b'BeQNB+Tdj4zF3LCUOD1FZlHo4fID5f1C9Lf4VPjZcKNIYhJJhsnXHBxx+PEDj/dnMTLJveDUu8GpgyFDecbguabgucMBc+3YSz+GvbxChgOz8qkd4Wl1Mo1uhIOGwjfj'
        b'Jf2svOQ4NhJfDO88yK5g/vG4jX/E98/4sljJmJv7153vbKc1Vomd8sqhbvkV8jj/dTv7m8XsL3/npIhnrHnorIfeLQuaKss6g0ah02vUJK6VluH1crtli0daa6ZXKzZo'
        b'UTntGoUWnxVi1kMsCzxa2yK3ZXHE1Rrx+PVvFbOqhMFp2IAA/5odf54u+VrmEO4JD7gVdMOnwD7QhYjTAXBtCWI8roIdHuDSAmDgUSFgM+dxuYQok5Pgi4gvPAi3xyEu'
        b'X4qYhV4fssdtzgpwjHC8oHuJBD5VJpVyKBEq7wZ8iQMuyOAOwi13BVi043y1ykezgNJjvqfFD2y1ZPWg5izngmdY4HAVOD3CqiMsazzYLLMoNOGZEKzTTMlvJbpONeyT'
        b'WBngpfAc5oERA9wGDzJa8m0+cZh8zkY8FtF1lgQRRjdqDbiN+Gqwbxlmm9lgD2vSJjBEGPcnp2A9eRk83Irh5xSyHpfFKc+97sHRYlHyt9e+PLT/qgCkBuz8k6Zk1ede'
        b'TwTqH/gu1xcI9HcXSf3nB+SsCYjaJn+z7KigopB9d1v0mzv+9EH0C5c8btzvv7Q3tXdeQk1xxGdK7853VrJydRevrzzkWbR465aJ8+CPTm2ZcHD4e3956dk/1/yGO3dH'
        b'b4j24ubhuCv39H82CadV1VX9YXfLuz984rc9b4s+i78WCN/pu1+x/8SO9wPXvD9x0T+f+Z9XRSkr393/0ZNxBZ7Z5q19Ob9MffXNx+o99J+xNvemRv39DTGf2Yz2CrgF'
        b'Ox0OtfKpiY2I7cLb0YpXExUcYlWeElruPOJTC2TkyqMtseSw78Yn5idJK8AJGRu12wCrDOyH+5njxEfWIwTqTkFcEhiC58tKJGzKW8GG/fA43E5O3sL9cCDVxVFZMCQA'
        b'O7gI/4bgbsJFwldyW8eYRLAV7rNcNQ7Otos9H5mP8bTxMTbuRaatwwPXbmK1hBDuJdCyc22hPyFBiI+IFZ+tvBeTezcm1xiTb4rJx1dfF7IYd385IujB5slRJ9ceXTsc'
        b'lz3EGao2Ti40TS7sKTZPTkYke3IO8sUlnledVg1mDHkY42aa4mb2zO1L2F/VU0VKN8Vk3ovJvxuTb4yZaoqZipmi2SzGtRQfFtEnOx5H+KKQsJP8o/zhySmDwsFGY0i+'
        b'KSR/mHzNIZP7PUwhCfdC0u6GpA0mGEMKTCEFwyEFOIJ33O9eSMrdkJRBPsPWDJPvqAeXDurBdoTiM/rlZxGAw3Gz0Hconvm1gnk/eFKPz7c6+vOZIwWzNPT7Dkd/5vr/'
        b'R65/ega97wJrhNsu07U4XIloE/a3YnrEs1yJiI3deBg8ybW4fNu1iOP0CP+GaxERZfo1h+Vij9YYccJ0Qitbi30qlT2ZenSrLLgR8umSJjoR+xJpxFhomd0AmAAp1mMT'
        b'WnhxPFHaoWxPTCYvslBCjeu1dS2+oUBuW9GXaRpblGsVUroKb0BYp9QqbNSOlEEqQJLL6KY2FWJrvoZ0ebggXZ7MpajwHLgBDiQVo5lsfjES3korysGFmmJwBRqSpUig'
        b'EhYXw50e7Sx4VZ+EkkvBJVYZmvdKK6SwC4m2NdCA5PAFSHaTJGCLsnMXlcHnPcBTgaCfECa4P6YFHkxFE9slsr7BUbHQdPTCcrIAh2jgEDyZhKBLB0PrqfWT2onWZX5V'
        b'XlIV2xtep1gLkXg5IVt5vf42R/sARX10hXtiAbEvcfPgg3l/Ky8ffI0XMsTKqd9cOjh3VkM9FRNyd4dkYlLD26bYw6/TNxNiFyZNUgz+/asNP9k36pX/y9lK/muN+eIE'
        b'9aVfrGn3e+WxLvVfdlbO++XF39b8oOirtGN//9Ef+6ipi4dvHTpcXSfM/m35+7B45c+Vb87szN8/y4P36c3ADyYF9g1t+DH7+TO+0VN/+MKsg18kiqpv07sVKcMK7q+n'
        b'x+nOvzBj6/ZnHv/QtGTRkv/NPPuS7uf0hNqMFYfKS26+8bMLH5w82/fDZfxnZ3QuT5B9+cqq7338+Fs/uZS0oTg+ddvBocGkn9zf6hk6t+TXny97Qf5XdtAvi0dmQbE/'
        b'URo05ML+JHhhEe4pxAfmsMCz8MUcIuWu9GnA4j4Wwkt48OoEyhN2szfC208w6oqDCrJZ4cY6y/KUFzg/FxxmgzOojwi5ygCnQS8poSuZTVUU8SvZk55ApITkvhmHcKEb'
        b'xUhLSLQ3HIT7K9jwNrgeRQR0uMurvSwZ7K1irhH1ngk3h7NhHzijYDZeX4C94DAuIaUKUTTwypP8TezEMPgMic0omo35C7EU7iP18oedJamc5mWzSJ3B1ll1NjJKaTAZ'
        b'LYLXHzCHCXzBYFIK3rohkYrZlH8hesVJDtihLmLMYlwtKyE6jpRKHgX3gkv8qezgKSyiJSoMgTvKrBg+x4PyErHBKfjyUgbePoSWh7CaiGkOzXL+LHYI7FKS2PzJeFtB'
        b'G3x+TB/BQnzeoSkMvEda+QxMPEoCj/LBADt5w1qx97dVJHhTDitTDA3m4tHf4WujC/iRUN9rFupbGkCJgnpzDk8/ML0/hrFXgWW4vPfCooan2JmQEAaiRNMOTOsXMdYi'
        b'SKKB9OfyL+YPyo1JBaakApf5QiZhKf+I33G/Hp5ZGHw4/0D+/qm9U+8JE+4KEwaCjMJUkzB1lBJMSDKHRfXF98cMcAaWG8PyTWH5PbPNcUnnV59efar1bCsqPDCNOEcE'
        b'fdw+uTkkHBfcXzOQaQxJNYWkDpOvWRR8uORAyf6y3rIe8nc/POJ4zsnpR6cPxBjDU0zhKbiMeDOi7p5HPftFGLA+P4f3sAOTiGN5T0RUX03/lLPx55NPJw/oBmuMU/JN'
        b'U/KH5hgjCk0Rhai00KQ7C82TIk8WHy3urzlSebyyr3KUg0JJFHE+xc4DyiHMlYNkTJfBoxwrTERb9L2YoCI+7/t8bpHA6/u+LOQyzIIXwyx87oZjGI8vWG60CcIME+HJ'
        b'whewOiDLPzEHsZmyXsD6uP+jXcD6b7pg/IhXCvWc3zSO2GLADt9xaWcVDtEpy0fMY37Y6F84zvY6Pqgtb2usqyMWRUY82zVt7QqNbsOj2CzBR4zJLn+y8kT0BoT1Ik0n'
        b'Fv1HlqCxYDB+9XmsD+XI6bCZBvwtzlDOcbB1Ocpl+wYgdEKOJ+UXaFjSzxnQ3ikYfmy5OTJqIG941kqEv371LIS2yH1A3Ptzi8wLFo5yovF9lw9zPuWNZRrl4tBSFhU2'
        b'pS/EHCAZDpCYRdmjPHZY7qcUch5gx1CKePPQqD5PcwC+BNUsykIJQnNQgtCcB9gxlKAEkXF9S81k6dEsmoESRBYi8LD7gLiGSpQmhO5Zbw5IGg5IMotSUJqQNJQkJO0B'
        b'dohdT/sEeThBAU5QgBMUkATBk3tazAGJwwGJTIJgnCAYJwguMMxDCcKj+xLMAdLhACkDRjgBI5yAgVxD2agnyxfLFA91+aTV+6r7tYMZd4RvZJgj6AHhUPSdjDfkuOVr'
        b'SMvXkEasYd1fsMi8dPkoR+I7C+V/VBd3g7WEUS4JX8liOjt6sPpO7BsedyabwyP7dH2JgxwEQ/Xw4seGZQr8+mby+maSuRkDW4dPkHCqWL7po9S3dzFEtkK5JLyBneVb'
        b'hAD+l101K9Q3YpRy52Qz7R097Btp9I00+UaOsoN80YT6tc6nHMpvsnP6sUsSameAbgHYpS1BjIXWz49D+Uaw4Snw0iSio0nzAMe9wYAOds8Ge+Bub7xZbz7epDcpnRsN'
        b'doE+1xfGk5ulWbYL4636uv9Ll8W7ssThUUl472J4LaeaQvW9SlFRVBQ3jbQJuAUvTimTwlsoYjA1C5UAn2etSQU9JHaxFDHxzNJmJQ8+22hZ2dRXkoVP2CsKhd0liLtL'
        b'WAR3Z3ApT9DNLgXPgi5l/cybbO0KlOaKdhE2/HHq4BoWJ3vQx7AEblixW7zbO+TqBc5HzVMuPxk6/0+rhv4hLeqXNqleXNi3sO8w6+1lb28//RTvUm2QT3XorqH80OqQ'
        b'/NDaIzGhQx09FZ5N99EMWf5V4L2MmWIeYfoaQI9XkhT2xjAbrYidNHgMHmMWmQ6Dgcn2i0xwz3TM1w0Imf1boUhEkoKTBXZbsSRt4BaJFFUnMCtM8OV1lkUmdhu4LSGR'
        b'8JkN4EW8xXhvErhJYlewFeBwsFuLIz7tGgUSMxV1eLN9h8MTYfKw0RlMtWdOoEQhVtbLMOe+MOhw7oHcvjknS4+WHik/Xs5sLTLMwQxawYGCvnUDXkZhukmYPha0ntnc'
        b'gwL8A/E0FmsODu+b17e4b17vxh4uSmUos9dbjHAxECN8xqzSOHaE0V1g1oMhWULMdjhAH4XA16ooK9fxZACLFYa5CZfOd3pvtQPuB1h+P7uP7TJ729llTse2RNDAZG/3'
        b'whaaFVw5ZztFLDM7Wi3mkTg+ivNwiuOTOE8U5+UU50HiBCjO2ynOk8Qx1pzHx3mROD8U5+8UJ0AweyCYA7Z71nrLMwysJpZ8IoLfxxIuxJaV5ZkkPBCF+2G/gW/wMgia'
        b'uPIgFOIvz0IhXJQ2BNsy7hX0sns5TZxebi8P/8lFTWwUhn85tl8mlHG5TAo7lzveLw897q+k5GG9vIMseXivALmTrGUhfwSTFvkibb7JNh8tj0LuFNtztM0XY/PF2nxx'
        b'Nl+8zZdg84ltvkSbL8nqs6+DPPk4+xmWXHKcjS06KyYqJsiloTYU6hdSLj6OU7Cj/WdLGSn/ShkEGpHF6DFj80bQ5CFPRT0cSKxXe5Be5cnTUEiQXESMeWWPeNUhvlFW'
        b'pFQpiAFQh41FNuWdgWIWk+w2FmHzylz0DsrAtqjw8HYij3/7diInYsWhnImVgNlOtC6CS1Zl/l5a76PUxTO771OX7qFCUKs9N7/er4UVwgR2ztzI+oJNtTfmyAr8Cmso'
        b'fSoKnLEGvmQznHoeMIZTHXTr+Jy6B1Xd7BkAdoAjpKS/pU2h5lDU+tPc+lmXZ3hRH1jhJFOl8k+KP/C0WBf6h2u5x97KRiTt6sHYp1n8vpD8IwWPHWbsWXWxfhe64P3Q'
        b'+b97CZGshSHXX/ukIZI+Jj7Ge106kXftyPUjr6lun/3HxMVDsT7i5IG4zLS1W1WynT9/oxf0gJG3YrzusXoVWz7mf7p0wXpVe2R4zw/8Prh6ftsTP9gyP/xHd37Gpn54'
        b'Z9KrnvvEXox6pksLBkF3VQl4BRxDPA2H8qxh68B5RL3I5ovn4HPgJugGz5VXJKPyL7Apfjx7wmM+zGrHZvAy2DLOxino5MJT8LQn3DyLWZY4PFc5flUC7kti47aLDeW1'
        b'wBuwmyntSgI2xIVpbFKChEmH0gRP4qpmT50JTzKJrsNr3hje5BLEYeEdOIggT/DsgMc44BToCiZbWErgxZKxNBXgMkVNgJ1V8BAHnAmAvWQRJAc85QO6U2AXDfpTSuBu'
        b'FuUJd7HBdnACvPoAqz7bwEAu6F6HWJMbwSU6oj0De8C+KsQFdFXBvVI+lVfGB0+tBt1i/tfIbxg3nSyNTrQNPUdTo9hGHiaByydQk2N6uL3ezM5X0ZHHjj+GHgWjAoqO'
        b'7tP2TzVOTjVNTu3xMQsn90fdFUYPC6MHfAY1dxPyhhPyhlRvNN6dvmB4+gKy17XAGDbVFDZ1WDTVHJuGzXhOMU9JGpg9sHBg9lkpMUoaFUuMfFp+Imny5qiYfh62dtqD'
        b'/uyIPaN3GOGRI10jXHwieMRnbBemum3ES6lu1+vIzR6uljIYTYRlVf7hbZKCGYNtlN2S/LIJLFYu5gMe2flOV96Pe6VT1/wKqW9ix9NiN5FXh5vKnd0/u8pbDf8Vsu2N'
        b'E9Zuttj9mzR2tYWTpT+ppgsl+eamE33r7DvwG8A4h+1gFzPFCmSkHZDOljul39wKqqDOhlTfALx5CDzNHusM/GVEibUM62Hafw0orzo8COpalW5NTrqAqRTDNGYLMwjr'
        b'bugmTVvrtwWmxREY2fpvAEyFIzAiAgw+pP3tQLGgE79O16aTqb4BHPMdcH2ZFY1Ca3A51hPfboH6b9j54mTT0hVzwmOYkwlzyD6NhJ+y6lULQpoYPuTzDnI0sOWXdH3y'
        b'W43hlDIajLC02Sjm1zeeZERgbPdyYUjsrz9pOCf6fj0/bmelKPCHIaEhizPAOxmLWG/W83+cSc3VHnrPc1bBn8SsB0iWpQTwGuwipIzQsc3gpBtaBp5rdCd5MpYmJ9jP'
        b'z2OGLtMohmTJJ1Ihk3o39i8wBZM1hQhz+KS+NOZQQ+Zxy4mUgUJjMFYMfnt7l85QVLPtV70bJ/7HVr0//Cf6/BcqdR7JvKoFFT/04yG5t3+qH7VZZdZuzyZ75v65f/p6'
        b'cSMpmDV7g3Lq7GQuQcSfHdsyhoj56z4Jjfn1J7zdPktnChoFP02P4+98p7x9WsKXrTNXhWwNzf0ptWu2p2LF78RsgogID5/ztyLiLnjRLVMF92gYxctpuH8BXhxMlEhZ'
        b'DWAvxQdb2RlwJzzvVkPiX0dO9ys7FHUNqrbG1R2hdtjiGEVwN8WCu+0TqYTksxsHF5niC+7FF96NL7wTfWedMb7KFF+FWaA+hTEgZph8nTB3hEcOsH+N0mM2Vnq4h2ap'
        b'owakFSExPm/k2vluNSDjJ1K8QvrZE5RV6jvM3H5ENXH+gxjsdHDE1S4Fy00dpzP+wvqEQyXcp+Qzjq2vYo6Er4dX48ElGu5CNeqgOrLnky1rtfBVuBNcAs+BHtTej1OP'
        b'J1fosU0ycT4YtEl7SNIDL1cUIzStSaiUsKhM0MX3g0dAJznVHddmOdU9tbU8LmkxRY4o90jIEWXPJ56UCX++NLdYRelzMMYfnVIDu6WBzM0ZFst8zDllC8bbn04Gp+AR'
        b'ATwaJBnTNxf4Chn1qFU5OgHeYJcWgevKyrUCnhYvTP1lWHPsraloSBp3RP2lSDLbd3Zao3+ScHZ8tS9ML0IjcqYPS7z7Z8n0i0tf3CljcbJ7wPaLZ5be2Bm1I+9Y6OvS'
        b'36TIPmgrWvjm1ovXuibIG+O1QcLlvEsxy7Mu1qrUl2Zp6vb7v56cee+6IqPwvdf2vu+3VrdOl55S/9r/3FLMvB3240b5zLUfsxdfPvXallXZF58WvSs4J4j7P9V9CUCT'
        b'R9r/m4P7FAJEznATSLjCLSK33CCIt3IlQBQBCeB9X3ijeEREiYoaERUvijedabfadtuETReW1tZtu1+3u90ubu3xtbvb/8y8AcJl7W73+76/xEned+add45nnnnmmXl+'
        b'zzaXzUVv7niPkxXS+rfgQA+Rt+h31O+mh+dhprCQWprqv/bzYr4BGeMWnvChziZ/FF6tWQSyyjwZZJ3GKAPN41aYqaCTbbgw+Dk+c5IPz4CzI7PbCEM5BUYzlXTRczxY'
        b'0ex3N8fEFy9FW73JCbihjF3ADTa8GglOkHw9FkCULeJAx7JxtoQuQEca2DfErPSpQNCu7zgVtpB6eBqDi7p2CnA/aGWuBjvBA6Lqra2Ft0eZGoC92cwqW38+e8IlIx6G'
        b'w44QkDS1skZaK1ljqcM9yB3CwphDzimsKCdXvLM+gwSNif0OLnjz27Wfy9NOwgdXH16tEB3a2LhRWXt1ffv67jx1QJwmIK5xY4/4UQlY1rPsibOPij9N7RytcY5WcaOH'
        b'J2+llcZBgGZujZ2wk4X+Eq8Z3TRS20V2J/TazVDZzcB7SyJ57fHIlkilXq+DUOUgfOLmrwrIUrtla9yyVY7Z/VzHPq6glytQc/01XH8V1x/daTGj7ynz1NwgDTdIxQ3q'
        b'x5YGCjcVxxN9NBxPJeeqQ7tD5zw1P0bDj1FzYugYNQkHbYaqq8OV9WmuzC6qKZNNKFXoD3FmLWvOwqx5XOMuwhx5xTBHrrP6n936PmokoDrMo1hZJeyJJnJypI4xpJUj'
        b'OjnMp5mlbMKl2RMcqdMjXJo9jkvrjePE7A16Wi49Ydzk+riJgE8NsmibvRvgvBloQnx2JxKMXSgXZ7CbaB1pZI1bUVK/HHAS9UQdVecLW+gTxkfBLnAdXKqD+2g2zrGX'
        b'XnLvY8piUWRr6eoTbwZr94UaQf/jDx537j2+uShUlNGx53bTbTl/O1/uuj0u83aTNCzn9YpfcY7eFrxq2vI5tfuxydeeHUg8xpt25h5rwJ4AjG4C0LAmpkIMyqEcXoEX'
        b'2aAhHhx4wRDdpDNECXjOKCoid8gQxcXFNJRjTU116uP69HJ9lLadNt36au4MDXdGo16/nSOWmJ37HZzkwYMs9Oupu5dCpNTDf9iE2NJfh8ANRmwkarBUVoOP1o4VPwwo'
        b'WskyLIDMHkvlpHxSTOWrKK2CBSMUWjMY+LTPTwW/mAxihMo1isaHp3qieWbr0LgBonKsdTYilG7wv0npE0vUNEFjcgcd+jNgE7wOmlD1nCgneAO+Ii1ebcgmnkgdP7p1'
        b'4s0YRLuXN/O3B8k37zpt/ehL8fxfvdbTad/gqpA7+LzT+7hr7xSfNw2t/1LM2h3MyBedaY+//2Xxn8Unf93/OOxE0HapvwzNkybU/LopMWedhyjjJc6TGFDD50lo4jUh'
        b'e3BaCrbRoZCR24SM87RkvMia4kxtnE6Itd/OtXGNwlNpTU8OmIq9+x1dsGnV8bSWtMakfq6H3FSRr0xWc0UargjRuqePIk/pif9UdoEqy0AdyjZ+CcoeWx3jEUIfVrHO'
        b'xbQ+cU2qMMHv1CH4hS9J8P8p+vdBZf0cn+IZNQiGOek2Snf7hTB6Ay2r1/vfHAATCeRDAwBLPKEBYFOecA48IgL3QFcKi9IzYIAt0rnSx/99X082A6Wo5L114s0oNAjO'
        b'kUHguv1i0+1tBxnmcm7U1GnzjzKS5sAkh4BpU9vnTeXmvN4rb+/nklUl41OFcW/5XcS/ya4KvM1Nz/DVp8CFDRjpJBI2oXXZpMSvN0T8WvyOAq3DSS31c3VoZlQMGQCh'
        b'2gFQMWoAuChEl1nKJGVSp+fFjI6M7jC1IE7tE6/xiVe5JajtElSWCTokbjiGxAf0S4tKaqtqJpRUDHVom6bsRZiyJy3lSkzc63WIe9nPIe5fDLAAF7vZKJDqNI9h8S1o'
        b'cAgCE0EAIzB0xIDZiL55mWT1gFl9VV1JuaSG1CJo9GXwgEkJdk0gqayV1ATpXgQPGIqlMtqnAMadGNCrL6rFLmgldbVFq4h7U3yob8BUsqqkvAg738S3zpOU2DIsaMB4'
        b'yCeAVKwDFHyBpKiV1lZIUH/hk4Y1WMtZg3VME7nGzRowLC6qXIazHDDBv4agcMlt4vCEvC+4RszA5xExgmJx1SoCSDygV11eVSkZYJUWrRrQkywvklbwmQNsKXpygFUs'
        b'LUEXBnEJCdn5WbMH2AnZuUk1tZgn1jHGrNxxm+Ozz1/toIaAII5RZC8YG1vgGZNqMC41/N9cwztMwDJK6DX8+6l4DzbQjBFYtHZNrJRmIe5oZXcYXAZXZbDLokaPYsLz'
        b'DN/14D59dOik71RZbT2KgbdMGJRBWQ5sZpqDk1BZF4WiWfB4lR82Kb/sk5Lpn5o5CzaAm+BBFrgsgAcC0malCNIC0HocrQOHkNRg00LThBx4itjEwT014DZsmoV+roHn'
        b'wREqkwnOkIndBRwzExG4iI5MhjeGfzi2koiwDtPSRNhsazMlokSgBV6nxd7rcdNQcibFtmb4UOAwPIMKSJRbzcL5w0b0DMoktWwBE14Bm+AF+rlNi2PRc/pUJXzI4FPg'
        b'SBK4QFQCMz19aHiAUDYF94JWPXiNgQSNa4m0jwCBHzWbemRMWRYW/4YbShExGh5aCq6gzBiUZB3DF0nVcVIC8geOrQbb0v2F/hhvMFMId2cwKDvQthC2smPBFnCN5Lgv'
        b'lUfFUpZ2zOpCx3UOjhQx8YOXwRZzlCOLgvcSGAJ8Lv4SuEtgNQzBPQyL0BDgn0ovdmEnywLsYxXDC8H0xvxGO0pAzSs35hWuuyZJ1SJ67AZb+ShDA2qhFUNIgePBUE53'
        b'8xG0Dt8Gt8JraO0swFYkbAED3IFtYpJZWPgMah0VaG4YWJibUOBPkc4DWxwSRSGgE/vIBCcY/qitS+0I4lu9j4GfP1pTvMJPyxQyKKMgJpCLte4VVjmlUYepnhksy0Lf'
        b'ldlCuunMovxxTqipL7kyAihwIqWKdlfwAJwB22kjP1RHRKYKfbCD6R4Lb5PMPmViLdGgPiO2sOJ8USlF3p4PjsA9opAw3LtgJ262I+AUPEQcBcDGqRbp2G/BHoIEmIny'
        b'3CIxB9tYMbBBSrJUxEZS1ZTK3qKw0KpinjXdEUZgK+xCWaLBiCRNVNNjcB9oJ71b7gQu0zlmETLLxYpVRGn24DAb7I4wp5vqaIEnelyfEoNTuH5yuA000gXaRcGr2ufp'
        b'jgQ74HHzalZEAthNCtS2zoryoFKMjalCx+qNK+i2zwA7wCFRMCJc2A7acR2Pls+kgfP2SqZqKZeJ1ntwix68zoCHZTl0Qe6CLnBMFBqI4QCrGMHoOcEamtZOuMFdfunY'
        b'mpJBZcHt+lLm1Pm5dNRBtKA8JQpHD8HOHEYELv9ZN/K21YbwtpYKd4OrFGUKOuZGsywLqui3PYDbUtFzTAq0uTGiEIEkwK2EfMH9DfPT6UHJx+AcpvACfMWSZYMqT7uL'
        b'eEeKHe3Kl6FuqJgdzqK7IQbshJ2i8BCMKbgQ53ccnAaHSUFkOQI/jBEID6SjsdABTuuXMB3gfaggdO8Lm13Qc4ibtIL7jGmoIDFJxPzJ2HJhejpWhsEbmcwqRqxFCb2s'
        b'QA/GogeYlFMsIxrRIw+00Kcwj1rClnTM0fbi0wxx4JK+NdPITUvbxsZrqOdUeYa5ZeGcuQl2NDnCEyZgE7gRGKKH7XBOMuJRIVA/0J11Kh+esAfH0YI4DZ+xYMEHDHAC'
        b'O0TD2QmXJVN7qe+qGLzCpZfWLaZ7Ht4vAldwdixqsQcjgQIKsNOZbu0LFnPSEXdBNLENnmIuYQSAg2yS0TwZlwqkfJJMCgujP5sjonnBHBN4Nqg0PRUbyrDZDNQyzYtp'
        b'JcH5etANm/SouOXYNNqNRxup3RBoYV1yU+CubOEc2uoMNviAG5kCxIQQz7QycLAC98jI9YD7eYgIU+BJGm0Tn/yQM8ERfXhnxAtyrBfGIsoR6VOFGdx4Oy0bPTFtEWzS'
        b'pzzhVcTABPAumokIxOn9LDRSxpxwyULTxwlwmU15gna9OngTHKRN3i7pwxNwzyyMOcSm8kzYVozFoBGRCqailfAVsCt9NlZ2LAUtDHgcUbXYhmbVF1d5jsGMBS1MVHjP'
        b'bD1pIthOGm49OIOmlxMmVCFoQSSOPkbcOnyyYh58CC77oVbJhPtThGm0lsNUFMSmvGbrBcNWuIPUWs/cgQqhGgrZloXR1fODKUKI02YHwhMG1IIyCjxEH7A5j5x1Rows'
        b'YmyOG8HeICblla8nAtvs6J5X8H3SZ6HJ1amewJHehwdQWYmkGwIvI6LKQxPzPjSzr2U4FiG+hVuhDu6emZ6PG0EEzjHgOQreRKyD9kdzDvXt1TGgvNhqHex1AXvYsGsW'
        b'mjUIY3gFHEJj/IQZBc4HUuAe+mSCK3RLbgXn8vEI90/NQk+nwqtrhMFsygE0sytgI9hET0dH4S4uPMGiwpNR96JPGNhGu+/ZCh/AK7qPdxgLg5no8RPs5cbgKK22uhOx'
        b'CO5BibfAQ5QUrVA6XGho4JOgOQQbSA6XfCM4ZmHNWmrvROjbuhzeAE0saqkX1o/BzkrS0gmhy/1o5zaIsAJSV4JugsTrCG6x4W407W4mJZaI18MTiME85KIhTLgpbK3D'
        b'a4j6OZiFM6koKbWMWrZ2Ci187PYrTBcKU0EHbF3qk4ZHmnUsCx425dJDuXU+bIcnTKmV4DwFbqIPF40ewmYurynVResJr8dgPeA+bfmfWzNDZmbGxEP/CgMNPCQmNMMW'
        b'QltxXBOKQ6WUIdrK2GxdRJGyyQLXwD0sKnMaVUVVhcDzBJ0YHg3egMS2FAzMuzc9W0hKp8fjObBh5zo9st1S5efJULE6vfWp2Monq+5mZNCMQwxaHcElxEvbwS6sLQS3'
        b'wBHphm+X6ck2oXWRc9vFc7+dWfV+IIcqPPS3xpaorryVbWs9nkx7ktp0fu3V2gC7P7IWPDoWP3g68NP0zc61/DX8Ne89tvvxcYxnl0fwOtvT9oFWadkuLvzmAxu/eCio'
        b'XhT2PVW1549XvWPXfVL49bw3dldd7zHX+826779z8hDuFzrP+KT72tMbn0e0LyzqeGP9l7+ub0ncwuTAM1csWt+qfKXtm+dbfzB9bcE/HwqrvKrBoSzwZ8mTOp+42wey'
        b'LRJL24Tzckwrqg89e3SbG2UT4mXFCnu+4or+nP+S5a+z7vrmnbYWA43p61H8MM6KN3M+SNmdmfSB2KfS63Xh7u73clq8Xl++u/tJzgdxu6fZrDh2uvsE59tP14nWpq5o'
        b'dfsynFOWsmLOlMy53zFyo+Wy7S5ur8PIz54Z8p3zXyvZ8fGK3OiDMufsQx9fbPlYmht9tkG24+P5udEXGj4ze92kbdWsKZvOBDwufrjr8n8pX5/aabNj7Xqjbz9/63GM'
        b'0+xP//HkBOSaPPzDe+2Nu9mLMmck9Zrn3fI/8t7fu//0bE/Sf8VrrorvHhE7f7BL/eNf3ru26laW1aPCuMuHv0sMfefB6b3+dVfv287Kd1/w3uznn3L5D/r8LXMdN381'
        b't+fuXGXzgPXspJ1J/zjO+GTZnT8/2HTu94/Yb38S+Vl7wOHdmZdbJZHeV436dpRtlvj+9Y9tW9YLwNdFn+5bcVAuW/z+V5nBFxa+2fzg/pdzz9j9tfHjJ8/cPmj6qLhf'
        b'5ftt3wFzZ9PPnhZdiVyVWPr3iBs1n7/u3fZdSJ7minBV8m6/qWWJ63e8m/rXpP+KTAt48PcDA+0uX/nlrju57O2qlL8K7zWZraqSf2LQ+3fl3jvnOr7JLvjTmz5ttm/E'
        b'PJStXKr5Jslu5RvvnrEp2NXe8NXXLm3vBKxoDODT7o/AHSG4Nv5EJBqvW4fORNbBToIGsRTd3OWHtyBjZjBBMyPTHxwh5zJzoDIByjFaK17P6FPsRAYSDNrBJXL+0QXc'
        b'9QJ7LKpNa9C0s8+iHt6AJ82M9CkOaGVVcXm05e718Fkm4KIgpS4EtGk3wKbAOyxwGV5bT9vQ3vJBQtoRNOHuGWXOCvfm0YgUB6zAXrAnAAUXtFathvAsE+wBJ8BuUkoj'
        b'VMSLqKaLXYbU6oaZTHEC3Elw2qCScNJsVDsLCbOeEQf2wYPEOtfEJGkY13Yx2EfsKaSgieyjge0YOGUR3DKM48bAcCpt5MFwcB6c055WZVLGQnxWdRlsJxuJ7uA6PD5u'
        b'J9HYi23omUc7gr1gm689NXoDXNU5XUrOliJOtps0rh2840Enc43UOV6Kz5aitlGQLp4BdyC5dA9eBu0jyyqwPxso64ZawS9SD3Qt5JLtSHgtv2zU9gO4hSZJeguCDRrA'
        b'XthEesPRnqUL7GYHHtKQHfvBIRporQsq0YpkTwC8jN3c6h5pFYEj/7aR8WiYMlaRWLzGbEQHhS6Jeuz3elqEDxvK2U3jFNAp6nUKUznFdaMgq2d+o/ETjp1cv9Wk2eS4'
        b'WYuZmuOl4XgpORp+ZLevhp+k5iQ1MvqtOViFPJfxxN5d5ZH8iPPu1DenqvJmP3Z821Htka+2n6Oxn6PizOm3dlLY9lp7q629+zncY+mH0rHlMcpZkaQUqbkBGm6Azg30'
        b'V98p1QTEqv3iNH5xam68hhs/Eh/W6d0xozue3ozRuU2MnSvUfgkav4SeXDU3RcNNGRu9lM6yJ1jNTdZwk8dGl6r9pmv8pnfXjHsniS5X+83Q+M3osVJzEzXcxLHRZWq/'
        b'GI1fTA+Dfvrpz3v3crVfosYvsadYzU3VcFMnK3mQmpuk4SZN9m6mmpug4Sb8zGip2i9W4xfb4zZx5kPRri+u9ySZS9R+0Rq/6G5UsTgNN+4nnh7baj/RJWMyfyZ0sLF9'
        b'TqFgcEwQRXHdGtcovJS2bf6d7mq7MI1dGN5vn8/o5wuVHKVMKesUdet3198z75E9YvbINBHpfRGzeiNmqXLz1RFzNBFz1AFzNQFzVfx5cn15/XHzfjsneenhDdhFtLhj'
        b'aa9dhMougmzIx6idZ2icZ6gQdTq4tMTgt0Qo53QmdyzpFt+r7BVmqIQZ/fyATv0OZzm7xfzlEjm5yfMVYUofjbtIC6WcrB1KCuYFgzMGT/GGvV8v10+Z3DmrPU0liOkW'
        b'qQRJPe499Wpuloab1c91bjVuNlbMoHd2VNwl3QYo1r2n9FGBJnmxOn6JJn6JOmKJiitWFYv7uU4KFvpLVs7QeExT86I1vGg1N5q8RbshavuK/XX77mx1UIYmKOMR6oBZ'
        b'Gu6s/p9O4KTQV9S3mffxwnt54d36at4MDQ8VasbIK2M0HlFq3jQNb5oa4/aMzTFTHZSmCUp7FDdUsZ9IMNI0CdoEaeqgmZqgmcM8YpLnEY/J1nCzx1d6pjooUROkO1bH'
        b'vCBdHZSiCUrRiR71fNojPXVQliYoS5UzS83N1XBzx2eRpQ5K1wSlP5qr5uZruPn9XIdBvg3f9hll42r3HAfolw33OQ4GSSCgbKY2ph9OV4SpOfxGLcSCzlaGCb2VgUWV'
        b'nwfLh2eVcZh8ewgYwahZpR1vZ+ymho5gzLJ5kVngi4NfdG/jhFEQdc18xmgbgOEduw0UjXZE9uqwAp5qMNDu1TEmULz/RzD4RiveedR4xbs3rXj/ZwA+idyfizok48Po'
        b'eorewCNr93aM7QKa9Kg00EQ5U87gKuwgyzZnF0t0h1oBu6ip1NS1gTReT1cNuCRiUwmuVDAVjARHWvP0miFWl8VWGBYWmtqvCqLIGbp5y/HN7yqMCwsrNGFCWucyJXId'
        b'3gJYRgUWTetKF2i30eWzRKIQth48i34foUrAA9BOr7G354BrohB92OWKFdmUxNGb5HK4GntzpUR6vMIMwYwcOuu7GVNQG8ybZlpdWBFmspEuxOM1+OYmJza6+cqyjXTK'
        b'lZVmFJeq9jbJKaxYW8eiU77NxTfLXS1yCjOCPMR0SmaeMVrQds9jWBaa2q5Jp1M2B+CbKcvQKlcActbSNyMicJE63S14hYIba5MpegXe6gvOE+1HPtYS6dUzPNHSAB4C'
        b'F2kFxkkkT+4VBQayKYYH6gq4FxyaOY+8uEyAjcz6w0yoQrffpyzQnp+5DM9m4LVvri9e+Xr605DTu8D5pfCEMQUbUIeBLvRJgZfpJX4baImEJ/QpvM1BgVfQxy+Nbtlb'
        b'sCESNjHQeqGdElJCJjxH3vvrBKzSjpjNiC3MaHZMoP3kzgEX4TWCiYP+9DAAMQXug0Zwy4qGMzQBd9PwEQgk6zeQYxC3wokeIRt22o8+2cjMAnvSQp1JudNy4a08IdYv'
        b'MOBBBjwJt1n5gYY6C8w2wIVFfgaUHpNaRa0yDCeVt4Vd8wEaDUnZ1Gpq9UJIa2ECwUNwF1xiUtPgNnzUEz4UEN5F+sQ9DFsHPnVhxRZWRDtG0UihuRVRaNiIOvCp508X'
        b'SD9JYjBlq9EQt39fdPlweu7WWMsdZfop8ac+ZQTtqpq+Y82uRacvdWzZ94fe3pP+NdRbQr+wRb1ZpvC5anZgWutTG9fBlRu/WvmtZt2agvhd+wa6j3Pc3vjhM+Zx5V++'
        b'mr95wZ59DnZbUur2rt7MPuI7Z0WPnoVR1jPP+tC3SkQLjh4La7C4pYq6vmDBnz3e+fDCjx6n99yKEF/u2v+F5I8Bfc6/Mb9bf+BK5rx/Mj5a/9a3io/viussOnfYLkuc'
        b'P+9C2Tebk/sCWXsiS4/fLwi6vOHVtlc7jn536+pt1tFp5xa1XG6XmP2461xh13u+a8vb3Lcmr330p6/2e7tWHHYIvl3pyP1+Cqdh6Z9Oltz3fvpq8Ywfrv/XimfvuhnN'
        b'a/7qH+leHU85Z944cutdr4qkspDd9XEfx6RfqDjVtvrrg1M/vB34iXz/9MJv9i7+zPFIY16j9ZHKQ0+sp23cfPJhSOgCdfpbX370TuTDb967FgpCN5ae+Gy65OEUs0+n'
        b'r3947aO3Vl+Q/faH5X+4F3r9r4Pf5nds//GfZtm7DjZJBXzuc4ygGcKqm+iE5y6w1Vr31PiBGWSlZ4X41AFymDdL6IsXQbeYDvAYit8K9tHHyuXrNo5e1O6Gh8G1xfAM'
        b'jfF0FnbjpRRe49EGkQsqatEAukOOi6GVZxe8gxd3mVgZix1iY4DsOBZsXwuurAWHySuksMUSu5faBbsJ+vUuBqW/gemWAy4Qo0ggBw/rx+sA4A7jIRVAdB5tgHkWyAtw'
        b'UfywCv4KgwUOAgVa928ni+GZcH8IPh5fBY7jE/L08fhw2EiawSm/Dr/BdgVB+6Y392znsR3AcXietqVsgYpMjFWpxfom+ytWniwZfAV0gK4KUgA3qICn8JIatruSVTVe'
        b'U8OrsIFuDCW4UDLOHBMvmA+CneB0eSApCbhXj7L354OLq4cXsDQuefdKkk0s7EAr5rEWm2hJvWcD6owusJOsvOE9lOc1tMRNEfj74z1cVFp4kSVADdIUDU6TOulZzKNN'
        b'SMEJsGWMGWk0AxynG/UBYlmkC+H+dD2KzWSAbndwak0Nic0CTfDwqKO6zLWws2q10XMhfnY7yvIuAYKf+FBwAewm54LBFXiQftsWsN8MlVpHR7J8IdhDZRBfQmB3MCLn'
        b'0aoCHT0BvOMNugJgC9EBoCxPYGvdAN31fZI52JZQQBPueYOgYV9BRvOZaXAnOAfRLP5SFqo6uFADbGxntcZ8RBbD12SJv5CGFhpcYEdx7BpFjbUHIw9HKhiHYhpjyGmY'
        b'p5acw2Z9lh69lh6KWUrmVYN2g36OPfnY4ZO96RoOv48T0MsJ6GSoOcEaTnBncKeoU6ThhKNorA9w78Wg0WGdHipOTLdHP4fXmKHgtDloXIM6g9ScUA0ntI8zrZczrTtO'
        b'zYnRcGK0ufr2cQJ7OYGdU9QclJmoM74zoTNBw4n4yZfaNSbI2Rqur5rjp+H49XGCejlBna5qToiGE9KZ25nXmafhRGqTtRgfzD6c3cfh93L4SpRGoOEIlLnKPCVKEzSq'
        b'/HmdHjf9+4JTe4NTH/mog/M0wXkqznzV3Pn/QqrwTk8VZ3p3sE5bhHWjikRpOFF9nNheTmwPqjWqbAKdwlFZQ9eyjxPRy4notlJzojWc6KHHXTrdRrVjPA2UTnfQyFsj'
        b'Or1UnPjuZHLfbqgBTDRcH7QYQA2qdFMGKd00HOFLxGoJYDDcMcjqGeXIt36Og28jKI79oTC5j9raXWPt/izScYonipjiOUiCKGqKzRAlqS29NZbeKktvRF/0PbWll8bS'
        b'S2Xp1W9tp7H2VFrT6PVPtStYPSW7z2darw9e7LWYKIqaLVTcAGWCihuG1uTseybPWAx+EkYnQuEziuFKQptkfMcGwwyRUB+V4JjJIRN5gtqSp7HkqSx5/ePfb2d/bNWh'
        b'VQp2mxnts6eRTcDyFa4qjsfIYfZ+D5+2zE43jUdon0d0r0d091y1R5LGI4kYFxVjL+p2Do0m48+JvQSwGzkkNgrXDYNDjB2+X+K1FLZKI0up+XYvMpL7T9nMEVMbBlli'
        b'oK8YDKGGzUVr5uFfdmNg24hNeI0JPuzkiQMvHHjj81OGQ0a3Q7/wySlicErjtWFTK3Kon5x5JodBybm5AdOCnLjcuMyC2fNzkvIGWDJJ7QAbI4cPmGgj8pJm55GFKGnC'
        b'f09tOg6pzQ73ygjkhgB3SBB7NFSbvgXGVXth4EZxHBsj+slw6OcED+oxOSHPKBQ8x0FDIiJbRw85ShCgsgzo54SgBI5hKIFj2HMcNGSMwV8TYfy1UIy/Forx10IJ/pou'
        b'dJoAQ6f5Y+g0fwyd5j8OW80XJxDgBAKcQEAS2Dg1pvRb+qgsfWh0NhuMzmaD0dlsghqSBg1ZZv6D1GSBMdMsh4Eh614QGpqYzRikJgvs2WYBg9Rkgam+WdAg9ZKBJcss'
        b'EaNS/3RoTjm7KjiKcpVjQL+ze7+nT7+Hd78XX+mhWIC/3JVixZKRHx7eSrYiaujL1UtRqzAdukL5eMgX9LvhK0cMxDBbYdzv6asMUWQMulg6onGJAzfOVKt+jpNcNshC'
        b'v55yHOR5g3roF25+V4VIIUPp/QcN8B1DysZFYY2zGTTC18aUjQPGlZCnDZrga1PUYXKZIkS+dNAMX5tTNo4qp6BBC3xhOfLwFHxtRdm4KRJwQQet8TVnJN4GX9tiDyAl'
        b'uAaDdviaO3I9FV/bUzbOCpYiUb5m0AFfO45cO+Fr55H0LviaR9nYyxMUbHnUoCu+dhuJd8fXHqTd5Wn9ji4kkTe+SQ0Hnt6O5oMUChDtI47g6CIXydcpUzUuYX0u03pd'
        b'pqldpmtcpqsdYjQOMf1cBzlLnqG01TgG9jmG9jqG0g4/1NwIDTdiUI/lgLJCQUP6oHE8w8x3kPo3whRmoJnjIPVzA9o+EG/CmYFNibpLIz3Kcja8yGUtgAfh1VEqIBPt'
        b'91dLMLTVFB1oKwYGtDrMPmxx2KCUiULtt5g59KuDdR7NSJcMhrIyosQu5BS6UYNFKVtssM1otDZqAZtJSfS0QFfGE4Bg6YlNUJzpuDgDEmeG4szHxRmSOAsUZzkuzojE'
        b'TUFxVuPijEmcNYrjjIszIXE2KM52XJwpbhMxD7eB2K6Fia5QyTEA1lKzoTRirg5kkzk1wb8Xwz6NyW3qv5PbmnF32hj7GWLXBibRQdJHgE0aLBosS43EDuN6zAKlMmow'
        b'J/3puM1wgSVNER1Oo/MkdgesBtMGs1I9sfO2Mf7jFkwR2xNoDLcBGo80PSvp+6OjwMexq46hKF5JRZFMxvPJqZLV1ktqZEWVYjybSyWV/FHPjLrwnY0x0EurapYX1fLQ'
        b'r6piWVWFpFZCoNsrq2p5FVX4mDevqKREUl0rEfOKV9M47r6jUdBrSilsLjNgVCSul8rw8e8BE+1PcorbkHZPjm6zxKX1A6xllejecolYWrcc3TOsRiVfWVUjJqIMfSIc'
        b'nxIvMdTprmHPfHJK14xpJ3un3k79nQbErBr3Dhv1ix5qU31i12Gm9c+H6H2X8RhNsRHRFBuO0xQbjdMGG24w0mqKJ4zTter4/TPWBJj4qZXSWikxT9e6bBnqNGmlrLao'
        b'skTy8oj4wy0cpUXU18LBVJWSnLVH5YswvEc8fUAfJVguqeFP7OQ9jqe1eKC9ufDqqjFcSThPLC2T1k4A1D+6FLhzh8uBfr+oFCh6sjJU8ooqqsuLhBMVJZJXUo5eWYKy'
        b'mLw4Q+Q1cZvQsTyfTETVqEiSyn+hRUJ/qkUQXUfRAzJ5Dq+iqFhSwfNBP4Xp6HVrJNKScjQQ/Xn5srqiiorVpFhSmihkE5ZidNFJ2/oE6zTFBIXXFgSNrSheBgGOxLnM'
        b'DMgY6g5tsyAmkVdUUr6sCjcFKhMqdI0E8YBJ/CXUFVdIxFomMDqXHBRWVUoqtTkRdwnomm4pLeuYuI1Ta3nL62S1vGJEKtpmLpbUrpRIKnkhPB+xpLSorqKWT7hQxKQV'
        b'HeIfdLPTVzypWNthop/qsCGmQz8+dMWrkZRJZaiFEbNDPJGQk4BXp+22uso6mUT8Ex4gJrLataC3h1SZlnj3KCKwdNMyFsedIrYV8GjgariHBjXQuv5Dv9baZ+elZAxr'
        b'G2fp+l3fHmtqCY6AMyRPqb8N5YMRFMz35pzO86XqYijsFfEGkOtmCprs6Hx1c8Wnx/N1M26tNoVtC8zpw8RleJuG8gms/3RBWykqKzYyswY3wcnxhcUQDCN6T1TWbWwd'
        b'IIZu0GACTqPy0If5++aSPSXLwDnWyRfysqm6EHRTVgsP6+YLT7gNZ53ql6eL67AJHjACRxhgL8ntt0FGGGg0MNArZ0GjtZAu5hIoh/cnKiZsGNEzz0qBDxxHFbPLBJyF'
        b'N8ExGtzQAG8+UYaB+h/Ggpwkqi4S3QyNhbcnytdnSIs6K8VXpJPnHXDJBDbA26FSnz/HsWRdKIuP35mx78B07Fdj+8kf25I+rnZUpB8FOyIYxY8Zln55x5ZYzdS7VCc4'
        b'kjLn+8N93/739B/syn2c9gsD+ZumlkUuzO8d/GHGhx0bvzv0Dm/ajTv9awoOhCfYPlrz5zuXzgTm3cjoFfym4fjRsly7+7/Znvtgkfu0G9a3H3xe/KHtNtHv325r/DP3'
        b'WMgn+gcdHK7AjIdvLhrYefKbzcuniMuyPrZdfCPp7zfWixf17n1/zwesz/aHitTTWnjTY27ZzFy71IZvTB+MurqqCOvBtRR0AZwb1oTDplqin67zA8rhk2EebsM4hobw'
        b'8kpyNCwSthCd7ygy1KNcoBzsELLh1RgXWqF+DLXezfEa9WJ4jwU6uCLiBSKpELT4+fOnyUaAhsHWKHJ8zRU91zai7DeCBxhAYTqN1v22wCNwt47OGhyYwQCnwGW4jVaO'
        b'nwCNeeN3JeDObBa4opdO6hkcIhyrPa+DZ1mwiQkuP8dIMOFwH7jNhOfoFYUQ3oBdMrLZgq4yyPpCqE9lgm0GaEQdgE2/sHqEQABOGRI0RqMirtBiXKyaSrl7KdwVJYoS'
        b'Jf90ZVul2i1U4xZKIAyJ7/PawxtppxZK115rP5W1H8E/nKm2T9HYp6g4Kf0eARj/0FWbesTNelyvtVBlLSTJU9X2aRr7NBUnDa+8rRV5ijwl9/TitsVqV5HGVUQgErVv'
        b'20B7x1BO6SXuvMnjyWr7mRr7mSrOTLQebU1tTj2e3pKOHjIaemj1wZjDMQr0Rk+VtSft0F1tH6+xj1dx4p86upCk/+aLXfkXnM84q12DNK5BP+Mxd0/cOljRiT7jvTJe'
        b'w5ox7Emk5gYObuLgFg66cPDKT9tqD/tjHGOvPUnf85FoKsMexHXdeWdPZTByiYvtXzr8xc6I4DPqbUZR1B3zOMN/ASjSuGBYZp4MQW+krYYA9PJRW+kgHdIS+5DYOwEE'
        b'478IFGlaoCNJv3zp5uHSnRounfOY0hFpcaRs/woQ45BE/fJlwntZOtCHLnSZhgTYcQ3289uKXYBk7JcvzxJUnq+GIRDnb9KWy4Eul46U/i+VqXyoTEjcfvkyFeE2UjGG'
        b'2shnREwvGovvKft3e3BIPH750olH96A9Vq3ryNX/WnnKhsozJGG/fHnKxpcH9dywpK5THj6TbGXQmxrDBt1ZJSydYiKRk7boPoSCI0Y6EBD6RHGAXegZNRg3mDSYYsVB'
        b'g3mp6TAgxFgs7l8eEKKcz/xaz2oC1UGcWIxduFZKVurSCBpTL+XMNQkt9OjEWL1TJBajZQ1aHBVp18nEJyv2dSfgldVU1VXTGp4iXknV8mJpZRF2GjsuS0SsvsPYsb4C'
        b'nq8u1C26Jhi6KFFxVdUyXFSshSIrOboYtaurf4a2Y/hFUby8quV4zUwrq7DPPy3kbFFxVR3tohZThkQ8Wdvgf8lVNTwJbhKxtLQUrfEQZ6JXn6MrpW1v4rYWNVuZ1qPh'
        b'BAs//A8tZkuKKsla9kWKjKAwneU7z6eqmrjkrZh8Ia/brvQidRyT4PnEFddISsor6yrLZFqtBvFrOGFBR+hAJpOWVRJS8CdtopOx1kk0T6pbKyla4KPF/IS5Di3cg0gn'
        b'h0UOr9/xm4L4Aqxe5IklxbX4PShFCVpaS/FFyWQqB0KVUvK8TFJL2i4i8iVoJhnDWxB15tihIpXIol6a5lBZpbXaDOh2J3eG9R8+eVUVFVjnUcXn+foux0olVJ3Vvr6T'
        b'aqdIjUflSN8ayXImat5KYUAKmpEqf07WNJKvVoVRJSMV1qL7vtTzeHDST+sOV39e5rB2hgzfquKlkpJaHunBicdAXnZEWGCQVpWMNcX06PR/uWKMgiuJGqMlq6+SlkiG'
        b'CT5eUiEpK8Xp+LyFQcGLXybLYG031kno6kgrSUHxqE9MzMycPx/XbCI31vhfddHq5cQJtqQGT4MC3nLUzsO6IJ0CBb+4QNruwdBJo/sL3xmtGaRHS8DQSJmwWLSQF48q'
        b'icc+zgO9XhQ46etHAcQM6Ul1hgm6i0ZkpUxKF6qqdMK3FomXIsog7YEfIJ7Ai1bh3xPzxok1rKMykREVsbSkvFZahqsiKymvgPcQJ6/gjx+zk+Yp5CG6yauV1CHmOpwB'
        b'omApT9tEiEMtRyMuKV84u6i2WILV7uJJckLkQjuxrahbvkxSPnH7C3miMcnI24rqStfU1UrQzFEpRuQ6p6pGRgo1SR4hUby4utJySXEdHnrogbi62io8vy2b5IHQKF5q'
        b'pVhaL0XEXFGBHshfLiuqXSMbU/NJng6bqMg/v4HCJ8pGqlOs5T+vWBET5ffz2iWSNORI0/9Ey094czZNyVg/PqbcP5sSdatfWoNq44PbdrhMRcVr6sr4k5Of7uO8cM/J'
        b'CXBUwqDIyVIiMqsMKJqcpEZnEzZZNmEvygYRxXD9XpBHhG6ySasWOSqzCeo16YSmBbBCHE77i8gDSCZFvHWIlfvk0XPspBP2CD5WFC8BXfDoKyTj+KSjS0kl+o/InIfn'
        b'oIhJWa4OstbobILHZBP8wmwICBc9ZcyJmy1MTeT55OfVom8834RO+tgwaBf9aFI+4dT4Bs8HDXItiaNun7wZ6mqQiFyCZosE7S8BT0e2S8rP5fnMhW3lNWiQorKETF4U'
        b'HbywkcyGb2sLNZSVbFldjWx8oV4k7k0mXhJR8uUlv2ERLW7UVtfLyTAEAS2Kl4W/eAuDAxe//GPB9GPB5LHJe2MIWk0rQmqv8dL8RXRAcNfQI/gLJRyfbnIuliKpqakM'
        b'SK4pqkNBhX9AshRJd5NzLZJ8cl6F85mcP+EXTM6gXvRmxJWSypEQhnj/5KyJlA3JbOKJizFZ4yEpViKpxZIF/kYCVtgL5bviqlVRPHwCA8lPpVhqRTdQm0/eqfghDGhH'
        b'P1VUwcMXL3yiRFqLByQKXyju0Sh+OCX9g2QswHK6UBQUFoYobfIyYQA9VCD89UKKLC1CtU1GTOVFiQgEH+oh/MVbGDZ5Qi2b07K4F1H0EDhgFC8e/aIl4YXB4S9MPzy0'
        b'ySOjt7Jf2N5DkIPaJ+n+mZxZY6BBJKLFx2Wh7pmcIxZLS1CGqQno1ROMyFHbyYbUpNvJz9xZBDl3MHFphV1gFn2IDd4BzbHpcC9og62jMZmWQnrHOEtIY+5vqigX/NFw'
        b'A425ZW0Lb4PNYJsOUBTcQqPC7YywpQQUZalYXxL9ATuIBjKCWwsjYBM4CA/qURg+KjmdfvuFSLg1HZ4Gx3TA+AgU3z3YRXIzSiP+4eY1zi9fuD6ziKojhiA7wR541A8l'
        b'T8uE+7OxxRHoSMucRdwGUPAa2JNLrQoxWlBblgGvENCaraZZMafZDWZUdZH1+9yHphx64xvcdoIPh3ZodVwEoBecJpml0Dtvup4C4D5w3JQPtsIbZHtG+mHhDZbMjEFR'
        b'8568f+7gtSwYa7pj+WeHQjIVHaadPSa8Oae2mOevNEk86FubaJYANhVW76hsuBXvk15g5e3z+eL3zNKd1332wz8/evDuFyavRbuWLJd7LNp8ctdqL/OlCbxd2yqyTltE'
        b'LjUsTF+//Oot794Myacrg6u/i7u7hrVzy1n9IzvX/+U3fargqgWLD9znfu83b8mKD27H/HXRgaXu6lJet7q80kLktfqLVWnrsqvm/WmHxwMTX8Gs69s/r5pTfiHqh/7p'
        b'X330t++ufVXsvfpPPm0/GBv5eDd+scTmwbOuk0bbPyg62v9l4ep6xuqus4u2TL+Y8pHTsZvvlij/eMRY8NRTnvDsjW8b3gnb+bvItarMH5/az/qxyvhH1dof9YTR6bzH'
        b'yXxDsq1aEgR3+PnXxem6Z50JWgkISSAzEyqKdbFEKsEuGmjkogA2+8FdYHtsdiroYFP6FUw3X3ia7KTK7KXjoESmwXa2IdgfRMyEQPeKlRPsovqAS2M3UsHBDQQIpAo2'
        b'rqfdEhCfBOAcvDTKL0EVOE3DlBwDjfCKDNOCELT4++Dk8AC2umpkgU5wB94l0DHgYn1oekYqg2LmMkCzoS+4C5R8i1/SKzk2xuSNIIOMseM2HdaND4GDXNNu4eY4UzyB'
        b'yiVQuQL7rnOQ16qI77p+B+wzyIbf7+0jN6VBpT0U9W2CTpbaLkRjF4Ij8xn93n6KWmxv02ndKe4Ou1nRI+qJ7xFpwmb2hWX2hmU+KlGH5WrCctXCPI0wT+U9W86Wzzlu'
        b'2u/gotBvidY4CBoTGxP7bZwVHiobL/TRvtWv39tXjlO1RjVHHY8eTvkHvD06Q20fq7GPVXFisQvcRcpIlW1oI6vf2lYu1jj7q6zxR+snQePgp7YTaOwEnXq9dqEqu9An'
        b'zr4qvyy1c7bGOVvFzR5ksmyC+gMjO426PVSBST3WKKA/2ATJR2mt5gpVXOF3Txw8cLGCRoJ+Zz/5cmWC2jlQ4xyo4gbivdBBForA32zWFGE/R9iYqOF4KPI02ABHqOKE'
        b'ok8nm/4e/nz3xI6HAVaEI0G/vbdcqGSp7QUae4GKI9BmPUWIvmXYFSZkT0mwpaCtcUIgC/JMEvxY0E8P/w7hJppTr5kbJ/qwXuOaJLqzXnPXQ7/pLWMLest4ZJcDGz7+'
        b'LJiAMcQ2smf8QmJbiveMFdQIBPIsBwYDN+IvFfxi1jB/pCZwvkMmTuJ8h631YqbXQDXoa906/M94MivlM2v+RI3xjewywazuSc/qFslsypC3lKJiCzOOx1rR8AGBsipZ'
        b'3azQwDwBhvJDHIyxfs4MGl0Az8Yb4Y40E+wIAt6bS82FB8E2MqlX1YvyQgPxEwzEG1+Bdyl4c+NC8pbHbusY35W2GFCBRWunlmlxYwvmgE2iEH3sagduxTAATPCABmts'
        b'5TJFIWwMPgk3YeQAAz2SywkTfco04lt9ildo+oOrgLblXzzXkuKV36eo6sIM/UABbSLuvADdFO9moZsC/QxzOuUcUzOKG/IFReUUCnJkq+iUkaamFNew1ADdNP0sI4JO'
        b'+f5sE4qT+J4BZVloajYtmE7ZGoNuekAWuilY7ZKjvWliQJlGv8VGRRKcL1tJSzfgPLjumpeTk4N6ZxlUJlJgM1S4EgxJ0DYPNIgCA9HYZMCGUNhGwc3wMrhIGoQvleXl'
        b'TM9BXcoE51EEUKIGwbuIa6eCe1q8gdvwuBZzANwB3fAiabAN4Hq4KBB0F2shBw7ll9FiUzPcswAj/8P9Ga6UqxO4S94TBa6AqyI2RrQEzcFUMDiL8sFDMinTAYMHUP5L'
        b'hJQQtsD9NF7uK6Bj1SicAPAQYwXcKqEhQuc5u+Xl8FjYw2s4OGSjD07DvXW0fHaNAe4OQQWAe+DUsJf4beAwbdCPmzsh2hA1ajIDsQnB22sS6Zb9izG6maGPb5r+cdl6'
        b'mjAl4LRLXg64AeT43DbcShUhEYDkkRRpQ/mIndiIjtfplTvTyecmlKPUCj6qcio8v94EnoYdHBLjBlpMZGYi1F5MuEcGLlHw/kxnqU02i03OK9W94ntu9m0ki1meXPzR'
        b'bUdvj6fVeg+2HpqhOO/w2C1k1h/P1BkktXFCGsxv13zSKq74OL/+lldQh2ThtDdOrI35InvVFo5Vyu9+tTh2fbD+jqbfLHz0/vR7X808WmPusHCwJcT44tegqyjJ4Mj+'
        b'isyPNFbRn+wUGsb6d9wyqZ774bzS47WqNyvcnyR/NnPh4Hb3i1/KJKtfVy8Mfv44fafbSs8Zj3YVpPw1+N0GJ+WKKVsCQplnk2e+lWj3+31vHMo2PMkynG52+qpbjseH'
        b'G9raa1n/FQtN98mfzJEvqKxWFofNdj+zdK/9qk8kGS2nbr4fPjB91l/+uTu0/O9v79zetLh126HgiPbs53+POi/lr+V4R7yet+adN1uazhX9+j3L8h3f3PjdEueSvdVH'
        b'3765IDn5x3fz+V//qpxVIbwX+G5rYXvtm+yOB83nj7hxUwveXl93Man+3Dc2S37caLwy3zn9n39X+r4bqpHeX/3pj17PfjxUNesv6QNbX3lPf5uB4ZKHDKs/NKxd9zmf'
        b'Q2SvKcvhhUlOsIF9ebqy1zKtQTi4sSTOj8hzG+EZFGsI7zLROuFBAJERwSGwOxRJ+RkMii2BZ1wRYyoqJZKlRxhQ0D6fwMWMdOL2ibk6WUhExGRwBV7QQRmAV0EThs8D'
        b'e4GSGL3XCeG5saCxYcHYVp2XpGfkDY+R44J2YK/D0JHAUNACrzCAIpZL3h6ybP2QbzxK3wKtbLYwRWZgB30csAu0OGlPLAJlja79P2oTJal1SfwiDFEwBE8A2xI2MN3Q'
        b'quMmgfdbZGeAnp8F7o+FBwAdKauIhAxfEYC2IdEZMZrjWHyGh4tJ9aUl6emjUAHM4dYwsJUV7wRayNtrVjnrAtpZ1BlhRAAP2EHwE+LMweV0XTgA84Tp61mJsEFADnWC'
        b'be6Ir+0JYMGHo8EAYFMd6CQNF26UOHJaMkPIZIBT88At2un1Xf8YrYE/aIc7tUb+VSXwDC1h35EiNoOf3QqvjQF5QEzvHjhIOxK7C1vB9jGnQqsF9LlQ3N0nnPmGLy3g'
        b'YPbD4+keifuKwu56RiQbWYFYWlJLRGkLrRF+rgs11aFRD7trNunneWh4gTQElpoXqeFFDlJuU/jPcNCYQrvnWnV8esv0YZdgxK+0zfEFLQuUrseXNCY/DQjHPsEubuzY'
        b'2Jgk91HMUdv7qTmCpxyXPo5XL8dLUXNh5ZmV/VyHfq6zwva4BcpDwxV2WvdyQ1Tc6d0cFTeph0N7e5ndNr+ToeYGa7jBfdyIXm5E9xQ1d5qGQG+1WPRxhb1cobJIzQ3U'
        b'cAM7rZAsb63hhuI4c607sFk0hF8nEzsb03BDaKu8FI1j0ES5dsd3J3QnaLix2mQtmWqur4br28cN7OViSACCT6aFBOBGjCp4bLedipvWkzz+ZnlPiiYxvy9xSW/iElVB'
        b'mTqxXJNY/tLJnIZaYkknqky4hhvex53ei9oJVTuWFNVZYY3+5p12anNSY2doTqRpRz6oJoktqcfNW8wVNUqGogZV6MURzv1cF1S+wVCHQNtnlIOP3XMcfBtGcZ0P1cvL'
        b'1XbeGjvvZ+EONnyMZ8fHKHaIPvCvCMrFrbW8uVyxVu0s0jiLEDlZcwcpkylhTz28Lsw8M/PFfePy4m4l7aDxxJgF3CgNN6qPG9vLxZgFWnC/EYIaoqvBKUZCVAUjT1QF'
        b'FHxrNaoKSr9n1kaeYYhIvQ5mDnIorlOj6XjvWC8+iEq8Y/30cPsULybqKK3RfJLL/7C9fA5eNz3HvFrXx6w+pesDTk/r6YOtNfPDvmb1h718jHUM9Mt7+ShDi4VvqTGL'
        b'hYmcAxlk1WEwH38Z7PZLQdJcTgqacdG0uhzeBBdnp4DLiLv78/WpFLjDoHohuEHjTe9lwy2waQNoAZfIiXlWBQNsCYabiGwaA/dt8DOgIuBpjAYFjsBtRDBjw0NA6ZfN'
        b'pBh14FwulmAb4E3p9m+DmLJnKNrI6s6+WXexPcPNpgdAVrzFrP61HpdBAyeFVcVUSxaL92qjoOLgPx7Mm7LsvP8/Uk1z9+S63dof/NoD2brPyp4zmxwVpnueGrnXvGmX'
        b'/5folREdZp+FiHb94XIj3PNdvued96Y17zdbv77mTtLXvZq+5F9HOPwQeOi90rSp8keGjzPlTbvP5J6ZtTmz+cf5r1be87wQ8ptFp21idhTv/mwb33fmFGfr+JXNP7in'
        b'pDxZXL++4+Hi/eUB98NStv02re9cbo2wvvRPP2zMffs9Ievb+2wnZY/5uoq/dYRd+PupO01vfMmxrTa/8sWvRN1u8cnza1Z9tSLri48M5MnJXx/lWxCBQQL2w/1+8Cg4'
        b'hZsfNVM4A1ypdqfnxAvMWDyNYXEAXA4kQDV7mOvhfVPyKJDD0wEkfpcAnOcxKf0spmOcC5mMF4IdSCZGkojAPxUFTCROuZrATia8B9uQOIKl/5gpFBI7bq7UarTKQKsR'
        b'uMAEZ/3hWRoh6DJahijTBRj8ZlcGkmfArnKTWCaUw4eWdPFug2MA+8bYFZAthNvhPibGU/KFZwzJ8/AVqKzBUzoP7NQ6EqW9iBaAzaT8NpEQdY8gFe4T2oOd+pT+Eqa7'
        b'PjhEJB0e6AT3/QKQpHYEXkVCoz+fSVnAVhbYLoWXaV3gsUXweDoWhAKygHydHqUfzbSbhupGxKC9cw3SaeIVwQeIfo04THA6OYVEsuCOIFTqfaTdulCdKf14Jtcljcah'
        b'ug5OxiH57BV4aBTCsn0KkZBk8CY84kdggxaAdvRSoGQK4H1w8t9G8x3SotCcz5DgLg5zPllRPe1X9IxWYZfmSnFsD4cfizkUo/CgjSuw3ihSGd8x82pme2a3h1owQyOY'
        b'QW72xL+RBtIe1aoTZ2sSZ5NbT+xdVW7havsIjX2EihOB8VZNm03x9IVEF2u7Y1GHog5GH47us/bptfZR2qqtAzXWgdinp1+/vavcW+GhZCkXqe2jNPZRjQn9Xn4Xlp1Z'
        b'dnp52/IR5dhxYzlbLkYTCc5YMVsZQk9BKvLp59gdSz2UelALX9mY/tTBqSW8NaY5RumhdgjQOATgPLz7ufaths2GCg4umNx81HuYNn4k0L7HyVU+W+HW5n1BcEagrO2c'
        b'rXaL0rhFdSeqneI0TnEot6l+Pbn9js6tKc0pitnHs1qy5FmDLHSXRJHgGQ6eU6PuTRRgVdxEtwdZQ2WSYT74uo1tUrje6+HspGlGr8cwUEhPhUb0VPj1T86HNHngXYph'
        b'HdukxOGCFv2yTdQQKOda3k/6Rf0PuUklniP57DE22PQlqT6T/M7iW41FljFmULrwMi9h1tLOIH6+ayXLZTQ+zFdDrcOf8gtq1XU6Azf/prH/6E65ijtl2MTeFcso7zJH'
        b'48iw2WaWGOrEctCUMrdpmKtgKRLkqztLevIeWfek9k91VPh1W3fndRs9SkCkaT4Lwx+h8DkJB/WpmFjGIMsbQ878ZPBMT+dJNr6byxgFMBOGAWYiMMBMBAaYiSAAMw7u'
        b'cp9+S+zYlIaoccAQNQ4YosYhrCF9DMBMKAaYCccAM+EYYCacAMxYOzSiHAgEEycIJbAWoQTWouc4aEgYkyAGJ4hl4BSxjOckJGl03xKI3xKM3xKM3xI8DudmggSGpHXR'
        b'SDTPZMhlndb0LzrEiE618kR5omKqxjW820jjGt/nmtLrmqJ2TdO4pqkd0zWO6f3ObnKxIlLjHtntpXGP63Of2es+U+2eqnFPVTunaZzTnrEYTum4e7gZuJFRiAb/8DsG'
        b'9esYZsJB6pcJnxngPJ/r5lzJijRzGqR+OqhnkKaQu6vMnNVmzhoz50EmxwwxqZ8MnrEoc5fx6UdQTlgQyQegFchlw0odPcrMngmbQEscn5ElVZlKWbL5eP/zhu36A7/O'
        b'2ppjuf2zmv++ffifx7pUCy7/5VfhKz5550h6k5GDtd1AYsIXv2oMfDrwnX7FqlSDNOnFax52j1pkDyK/Xev81rwD+/r3Xp73j565b+ibWQVIy5i8z26szYl+/PEP33fn'
        b'zfrqW6uWCMkf7pV81v554j8ezv590tnISxHhJ9Ywq+tvTLX/exf4uGD7mVqX5R88W7LGYfXT00/E64x/EM8c2LCkI45j1ufwic/vlnplR/71b4wP2b/TnGOYSRNLmlWH'
        b'1y3o9a1W7ZrdHtKt99vFp9a2MVnvHwRZ54NS32/qyrlzhbV58Zy1Lo0rfrz3IKG9b03r16+6LPY6di6hxu7kgk8HfzU4b8PvHl2OWh1ywWSByoa/QN/f/Lhoadej7z79'
        b'+skrzCdtds0Z4dXJiz+cvv8Lje+33LdnfNB3dur8jLpqoJE2NTfnv3LmyPyvay61vPv4jN0FqZOp6pN7G7uO7Ki2qH9u8s7SupPr7fgsolUBm+B1cAWcYcA9GQyKEUHB'
        b'/ZVATlRO4DbYkgK64OFxO6NsQ3jC6LknRfz3nAJH6W3O7fDWBO7XmbCT7zGWHxq+MPhPcN9/gV970LJVLPk3jnGPYeEDhgUFFVVF4oKCNcO/iND1W9awsSPi4iGUmc0g'
        b'28DIrt/CqkHWGLxr5d6Vctfd6xrWyWVymSJYUdQWenxNyxrlrOaN8o2dHuivptv1Zl33rJurrvnf9O9J7El8ZPVqymspvcEZquCMJ1x7ebC8qCX0uFGLkSJNzfXvtFNz'
        b'I1TRWWq7LFXubFX+HE3u3F67uSq7uU9seQqrg5WHK1WWHoMsijuPMWhMWXEa4w7bNMQ3xH83aMAwSmX0W7k0Cs+ZqoTJat5MDW+m2ipFY5WiMk3BkkvEFCOPQeoXCXy8'
        b'jRCP+rnBMxw8H7k3mxFtZD9IvShonPMMfz0fubuB4YF/viiQ2z7DX89H7mYxKGPLQWYN2wgxs/+L4TMSPqd/s1Bh99pqi1trRHG9lCZqO1GD6aC+oRES2iYLbGtYRo4o'
        b'v/9o+IyEz3XvLzUgrZtLavO/Hz4j4XP691Bbjk0kw+Z8u+NmxFtTwNo+XqjdJncaYBYU/Ivb4v8ZRoZn3MLRBzsmEkKnMLEQOsS88HpW9hmlVZQFMRiWWNT/vxf8Yibe'
        b'eCl92SiORb3KMo+bwpI+Xvw+S3YT3awKWbJ8X6QxM84yaW3Br/QSq6cu6vlD4pKiwD+9Y3oyQ1n1h+Kl4o89nZJns/3++2vlj8q3WjjSYPHjgxdiD+6+pBR7HlK+PuuD'
        b'tu9EBl89+WvmJ8+k7/3Np+r71ryLLumhR9c0rVsf4vj+zUUhF5veOpW/VsT/9FGMgbnw/dmfmp/4QPLkevr9D8q89TghpoKo6j+esTiwibGDW7TX6LxPUMJrzHTOvKJ9'
        b'Zl0/WPdc/9uFnm8qVrp92drTFbjeMopvQW+rnHOGrVjJko3Ps+1NN7CEDykTcJ0JlXCPKT3L3wU3E9OzhfAaSuUOjmRnC7HjqHsscBrJBUqSzQx4wh/sAQfgAYyTgbff'
        b'DChzKxZoADucvQzJnpp/WU56KrgcnembaUDps5mGUA7biTvvlZK5qAQ74LUAfYqRR8GzCVOe4yUu2LIo1A/ucU7ToxjpFJRb+hDN0mp4DRzEDgH3o1fBvYwcD8qEz4SN'
        b'8Ay9D5UP7oN22Ug8vLaIMk5lgk54z5JkwJ0Fu9KJWElvRJnD3axMRha8B+4RiQeegpvAqXQTeH7kmGGpGcl7RtxaopSkD+jpwbNgC2VqzcTqTDe6Pa+DYzKwByWpppPY'
        b'mlPG4AYT3CQg3MT/0zYp6EJJrpvCzWWgYeWKOnhjhemKOgZlBw+wwF54ch15Vwk8PyedgJrjulAVYBfqmGYmPAMerCeQ4vBUKGzGrR6QLvQ1qsb1hQfwtQHl4MEGW8Eu'
        b'sIPv89JC1f9JGUuHSfkQaSt26N8L5K1REBOGo1BFihg6yBKYb9lTetabsvBfvxmnz8y518z55Cq1mY/GzGdTcj/beGfGlgzVFNdzEWq2QMMWqNiCfrbZplT8p/PDRTX6'
        b'08/2Vk306WcLVRN9+tnuqtGfQf0FlnpoHvn/KlzFo0w5m7J1dmZcBlgVksoBNraoHtCrrauukAywK6Sy2gE23mwZYFdVo2iWrLZmQK94da1ENsAurqqqGGBJK2sH9ErR'
        b'TIO+arABxoAesX0eYJWU1wywqmrEA/ql0opaCbpYXlQ9wFojrR7QK5KVSKUDrHLJKpQEZW8slQ2h1w3oV9cVV0hLBgxooEDZgImsXFpaWyCpqamqGTCrLqqRSQqksips'
        b'IzpgVldZUl4krZSICySrSgaMCgpkElT6goIBfdqmcmT+lmEmWfiifzzeCD2SwBg/JhxFihP8Q9Q5hcEQs/As9v9z+ItNwFicetXYKI5Hvcozj/NnfW9Yio2+S8r9BywL'
        b'CrS/tdLJ9/baa151UcmyojKJFiqySCwRZ/ENiT5wwKCgoKiiAgljpGewxnDAGFFLTa1spbS2fEC/oqqkqEI2YJqL7U+XS5IwpdTEMrXETZM57tnvDaOXV4nrKiQxNclM'
        b'GmxCth4FgywGg4HrzB6kcGBOmZhtMhhkV1gyOIOUTrjElTKa0mfo0GvoIE9TG3prDL0HKSYjVCWI6fHq8XrV5zUflSANffoNLfuNbRsEKjuR2jhEYxyiYof0U5YqyrKR'
        b'q6bsNZS9auhDivf/ALDDanA='
    ))))
