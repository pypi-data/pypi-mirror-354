
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
        b'eJzsfXlAk0fa+JsTSLiEAOF+kTNAwn17gYrcqCHeggECREPAHB5YrWdF8QCPAh4VrFWsWvEsWlvtTN1t+3X7kdIWZLutu91tt7vdXdq6tV/36G9m3iQECfbY/b7952fL'
        b'ZO7zmeeamef9mLL5xzH/frUOOYcpOaWj4igdS87yo3TsZZz5TtS4f3J2CovxRZljlEIUy1nGm0ylmGOy0F81KjuTvYw/mZJzLSVUrGUOk6ll1hpoqpbnVCfhf7tRMCu7'
        b'bPYCur6h2qhR0Q01tKFORc9db6hr0NK5aq1BVVVHNyqrVilrVTKBoKxOrbfkrVbVqLUqPV1j1FYZ1A1aPa3UVtNVGqVer9ILDA10lU6lNKhopoFqpUFJq9ZV1Sm1tSq6'
        b'Rq1R6WWCqgCb8QWiPyGekreRU06Vs8rZ5ZxybjmvnF/uUO5Y7lQuKBeWO5e7lLuWu5W7l08q9yj3LBeVe5V7l/uUi8t9y/3K/csDDlMKf4WPwkPhqHBQuCi4CjeFQOGp'
        b'cFY4KbwUlIKjcFeIFDyFq8JX4a0QKsQKvoKtYCn8FAGKScmBeAFWOmoDy/xHJ1UbFEQpAkfDiqBRP01lB2YHhVEhdmJrqKmcYKqGhSaaXVJlu5R+6M8TD5VLVr+WkghK'
        b'NI7IvzGLTXGpjmA3aoXzYj89ZQxDkWFrwfOwBe4qLZoHm+HeUgncm6+YK+XDa0YqcjYX3s6CuyUsoz/KGg73Burzi+E+uKcY7mFRoBccE+SzQe9alYRt9EE5QsFJ2F2Y'
        b'H5vPS4fnKS6XBU7APvi8MQiloaS9oBklpoFT+VK4C1XCo1zhbk4JeBkeRhXgJcqHO8BLoAXujm1EndqTz6PAYY4AXGGDq+EGYyiu5hrYCTpQlsvOCfAwaF672givrHZe'
        b'bWRRPnA/B+yZl4y6OxnlrIHHp4MWsD8ufUOhNBr3Gu7HYQfKP4wLtiXAziqWzbT5W6btEHKm+ZWjqUPryUWrSaFVdEAr7oTWWojW2gWtrxta6UkIDjzRenuhtfZBa+2L'
        b'1tlfEZDsb15nVpmDzTqz0TqzbNaZPWZFWdlsss7jYideZ59x6xzIrHPmej7lzHVkUfSKoiG+N0Ui6TIOxW18gU1RKzRZmwRMZHSlE+W+TuBArVhR9H7pJiby74k8yjEg'
        b'2IGasULzh4x11FlKI0DRI0Vi7gP+bxHM/DryS/b1hNccZ7A0GJM8GdfJ6nWg6Hhfre8/ZijnxVIk2lf+pdshN1bUCPVk0R9rnhAtoYYpowyv4IGktWhxW+LmRUXB3XF5'
        b'keCwFO4GZ8uiCorh/lhZvrSgmEVp3ZymwhOwZcwaCS1DNuA1EprXiDdmfSi8QslC6xpw/41rsP3RNXAYtwbOJTo8iUYvDIEp8Ih8PjyzXLqATbE5FDwOeiOMOD8Ce3BM'
        b'Di/DPrQgoVTodLCVxINjsL1GPh9F1i2FbdTsGaDVOAlvXdjmDw/iYhRC5XHrVjO1HIPHUR0Hw5zQJEkpKdgsNYpxLafgVnhTXgyugN3z4F4exd7ACgDdGmM4SoxYngdb'
        b'0Ja7BPfEFKI9satoXhQ4G5uHNz0lg2d5YKs8nlTv4A0ugSto41znU9QUaoo/PK3+5PVZXP37KPGJjL31bS8JQLx4R+k7hcO5q6PSHbeKsn3SWo5eaSmUySMnzXn17r27'
        b'Cxsfqp/gB//83dRLHTXfvpHx6d/c3nh6etc77OgYp1c+Pab40/a36/f9yr9v/v2c5IzEGR6H1bF7rgf71s6f4Xm3cPibdumv4xNKnt/leD/Q9/X+bxeufvnC7+oD9q+/'
        b'tTOz27Tuwr0aWfiy6AWG4pd/+2D6vV9KDlwqzvzyF22c/UfSyu7erL74y4FJOV5/NfjDusl/+AxOeV/Y0zHgmfJ77Qsfmd6OBAnbimb/Qf/k9Kw5Td9Rt38XVfD7f0p4'
        b'DzCuqmsEnYVwbwzcWywtSAIdCKFRHrCPA3eC0/DmA4ypwC6EiXbFFMDrcLMUNucXlfAoIbjERmt8voDJcX4WOBMjkxTEEGQHnlnHo9zgZk4D7AMHHwTj7QcvgReFePKN'
        b'CEF1T0G7gU1Ngjc54ALohW0PfAlKPQO2o+2yO8wN7od70CbOYIFLsKVC4jLMjpLo3FGen+joXTCE05tH/w17T6nRNTSptIiGEuosQ5RVtWbasItOpa1W6Sp0qqoGXbXO'
        b'AxVk4xrYCPC+2Ux98QSL8vbriDi4rDn3g4Dwrpr3A6Rtjq2sIU9x29QhenJrbkfCwfx7XsFdvC79oFeMyStmiI7o8boYeDawV983a0CSbaKz7eS6R4d2zX5WYJPSw+tZ'
        b'2x+ZNuiVbvJKNycP0okmOrE3qY8zQE+xrcUw6BVr8opF2bpn9vCeLXjWzbYmbk+dtaYhOvyMa7drz5oBOpXJ81u/0P6wlBvcPsVLQlPYzAG/Wf2iWV8EUoGykSBK5NOe'
        b'3pbekTvgGdrvHPoVRgU6jAskrsN8Zo6GHSoqdEZtRcWwsKKiSqNSao2NKOYnrpQrclaMWSodRgtkIYgzHefKQM7/bKYebmCxWKKHFHJ+7erTsmqzcITNY4nuCT1aMn7N'
        b'ddtePOTods/R85sveBTP3RL6Vo/R1lF+DHVOmMoZg+Ss7CTBurzD1DLMTCJWUs7SceRsHRf98eIpHR/9Osg5Oke5QEEls+RcjIFXsnROJMTDIR2Twid+jKtZCnYyR+5A'
        b'ws6Eg+KisCMJu8iddK61bKdaiXCYP5/M6mdy1IUSMtVVHJsuci14uA53kcUweIdx9RRpgCEGnDIbblbLRcSAY0MMuGPQPiebS4jBuNiJCTJnHDHgMgT5L3HcAAEbLSSi'
        b'qNnsBZT6o+gSnl6JUj44u+tK1TNvuoOA1zY75SxatKVa4tl69xh09PwF52zNq2WBr+2TRHl6v7lC8J7PWz3Cd/6reXlD/MyoUOHr3hEdzaxmh4W+4BRLFS7Ysszztb13'
        b'rxXFvyQSv7OlNcmFWrzL+dyfjRL+A8wGs8Hl6hgrFxTDp9zAaU4kONnkCg8/wJwPuA3OwsOjWTjRQso5luMwCbQx6Ufg81QhbCmaCroRhyjhU45gN3sd2A2eeoAZkTUZ'
        b'GCnBPYX54AJF8dOD1Wzf5eAiQWHwKj8AtJQitpBL8eAxcArsYMGb4HDOA0wkdSu8Y6R5CQrMNVKO8CobbHdwk/Am3gs8C9YiW2DYsaJCrVUb0EZzY2BEZokgGGoFRTDU'
        b'iIFNxcZfnHp2ap+PKSbb5B7Vyj3k3LFySCRuL2wrHBSFm0ThXSsHRAm92SZRCkJdQZNPrOpc1TO5J6GjAeUVDgUGox/Bh54+5jJd3PdE4SMcSiTWeVr3P3+Yq1dpaoa5'
        b'WCQZdlij0umR9KIjA/W2DoGPt/MKvKGZbYzZVR3mbpfi1GTk/A1tY4RdWSE/Ygd/hWHtMD+cek4Yz6li29se1dbtwWyOZLZ5a7DH8EmcoDFckO02QZuAnc0hW2Nc7MR8'
        b'krUDNlvDiCVN5xKNEO5FkLMPMSWdKXFwvxyxJ0UIxObNnY/Zpumwmz/JOFe9I+0aW5+DSgRN+exK1RG0ZdyBGG2a28+e9/UVe/yPWHyyUzn51T0hzjc1zs6n97hvig6d'
        b'Gyk8/Ta9puiSe5/Mi/+2gXr9H3y9IU/CfYBlJHgRnoUdhUxroNvNAtOOCQ/weiyBbRvhFUS698P9Mmkj2hiYOvuBLti8iQt2xMKnCXCDi8n5oMUdjsI3gm14C557gMfb'
        b'sBG8Uljqv1jKothrWNmIOUCSjg0s40WyADKiE7Uqg9qgqkew7GGFZWscAedUMzjPwnDXYTixoXPDgGf0B37h/RGZfWWmiOwBv5x+Uc6Qj397U1tT+6a2TV3VAz4x/e4x'
        b'NkDK02HJb5irVdarHgVNHgFNK2Rihl0Xh5wqC2R+u5n6eiaHxRL/WMg8yA+lnhXKOP9xxF3zg6AzBoPI0VkbrOBphs0n4DOPgie4CXaqVw7KGQD9taSCwekMgNoHT50a'
        b'AWiVo+fcOOHpD935Rrrz7TudrtQiDf+5N16VcB5gNt5/KXjJDJ4MbKoWs9flg8MEPHPgbdhqBz43wR1Iut2RAm8RIM+Cl0EXaKmAz46FT7BDwnkUsXIIMI5Co94ONOrH'
        b'QGOCGRpLvgcaQxG2bRe0CTqS33GnbbElAURdPG6Qt0apMY4Dx0cxZRp20pFTR9lgymIEj8E/Ah51kRii7WJIAoccK4bEsiWVzP1fwZLjGAjeODjklRjx5gtFcuGLWK9S'
        b'BpulUtm8vAIFbC6VE7kN7MtS5CEpTsaiDPBlJz54uZxgVmPYgkdBtygNtj8CuuVx6pa8Yyx9AypRvOf9K1WdCHDPv4ZAF1S/+RrF93PfHbLj6JaQI5PeVDrWJO+4LPed'
        b'Kd7hO0XkK/5SnOObs2hrhzh+c8rcesHcDxaK6vgxHzifnstfnsrnb8//wFlAew7FFzv+5jWRcMtL2VtCjm9J4ry8jHLvEn5+M8Ysa4Fb8EC4VQjaDdrgs1YpKJZHmIvE'
        b'FeD6mI3ADmpcV5jzIASlpW6c/ugugIeC8EZAuwBeg5fINkDMzY11hAfRw77RbdCNuB+CxPejbbIPsSFWJiQnDUldL3C+lw+xsuLDfGMjFpaGXcx7hQmSbbKE2SZfLOJQ'
        b'4sldYT3cQR+pyUf6AZYwpg/4zegXzfhlAN06C2HtruQzWd1Z7/nIPgiS9EdPuyMyRc8eCMrtF+ciCA4MGeFTk7zwThp0DzG5h3SFveceabOfHJj9hMX8RzaSTb8dKDOG'
        b'twgR2djBmKueMgsRCMc/XIhx/Aj14xA9s7FsVTZjWQ8OUdkQpZoVubPKOP9GFc0PQO6cEvWOvm8oPe5R9VMHCbJ+q+u/xeAkgntvhLKLfEOuymI4M4PyXDxPH6EXxH7b'
        b'dTV+204BZ6Zk7sIt7mv8tw4l3P1ImeOr/PqThDlR2xPPcRa/stLZGQG8c8j5AufuxrVn4xuvU1ThFOGCfb9B/AYGslpwrahwE7g6BpDXgfYGAuMxsA1uQRDq9KQNng5n'
        b'MeC5F7SD07AlFrSvy4d7pXyKX84OjYBthLdHxQ7AY5j5hlfATgsDzvYFW8BuBBE/QLrEEEHTNjw1kl31Bh1C/K6jiB+HCTQvY6B5pI5D+Qd3eHeHdlWfWdW9amByosk3'
        b'sZU/FBp5JrM7czA0yRSa9H5oSlshAmxxwAlhp3BQLDGJJT1hA+K41mwkcWMxG8FPWOoXfEoc3rVgwCe23z12PH2YEJQJdbCB5HzsFGDkR5mpAxaHaxEke/wYIMZkTcIZ'
        b'5lUQJp5fo1ZpqvW6CBzLLvnsnwi8JW5Y7sD8E5okQUUFc2qB/M4VFauNSo05xa2iokat0xs0aq1K24DEf0LpHKsQYqht0K0fdjTLB0zluiLKIgsQtivNujnxuIa98CIo'
        b'DeqqCqXBoFNXGg0qfUXF92EoG2WB2OJgIVqfiZfxKeq+p08zRjzNeUM+vsjx9mueM+Tl05z7kMt3ifirO8cl9q8CjovkoYDvEvXQneci/ZJCDlkkovMHx4pmCguKmxCt'
        b'2RdXwKIcndkrOODoOMKG/32FMeE0lh0NAkfHk3PlPDlfxtbxfanF1GRK7jDfjRr3T+5oOWay/Ooc5U46p1oBoyeYrUUMyvrPNqKEb0WzVJVqQ4NOpY0r1KmqGe9n7mQd'
        b'P8Po4FuPBSpdk7FW36g06qvqlBoVnYSScHe/dS5SGZoMKjpXp9YbzrJ1xSjys5+hHfDXTg+0sxu0hoasErTMdFR2tU6l16M11RrWN9IKrUGl06rq6lVaSZZNQF+rqkWu'
        b'QamttltOqzTAWzqNjJ6LYKIBlV3QoNP+kHz2KlulQhBHZ2trlZUqSdaYtKxCo66pUtWkUlfVaY3a2qzZCmkR7hT6VcgN0vzqEp0sK1uLJkyVVYaYPU1c9ipltYyeo1NW'
        b'o6pUGj1mATWkXa1+TYMO1dxkaUNnyJIbdEp4QpU1t0FvqFFW1RGPRqU2NCnrNFmlKAdpDs28Hv02GW2KWwKVa3HvsMqRNncERcnoJUY9alhj03k6YcKUxKxClVbbJKML'
        b'G3So7sYGVJu2SUnaUZnbU9Fz4C2NQV1Lr2nQjourVOuzylQaVQ1Ky1EhUWkVrjfKHCWxpNFzVAh24Kkagx6PEk/p+Nz0nCJJ1mxpsVKtsU1lYiRZ+QycGGzTLHGSrFzl'
        b'OtsEFJRkyRHWQJ1U2SZY4iRZOUrtKsuUoznCwbGzhmNWYRiWlhjrUQUoqgiewjreVXjWmOlHkfk52SU4TaXS1SAsiLzyhfm5ZdKZDWhtzJNP9oJaW4dgDddjnvY8pbHR'
        b'IMXtICRXKTO3afaPmXd78XjuxwwicdwgEscPItHeIBKZQSSODiLRdhCJdgaRONEgEm06mzjBIBInHkTSuEEkjR9Ekr1BJDGDSBodRJLtIJLsDCJpokEk2XQ2aYJBJE08'
        b'iORxg0geP4hke4NIZgaRPDqIZNtBJNsZRPJEg0i26WzyBINInngQKeMGkTJ+ECn2BpHCDCJldBAptoNIsTOIlIkGkWLT2ZQJBpEyZhCjGxHtJ51aVaNk8OMcnRGeqGnQ'
        b'1SPEXGjEqE5LxoCwsQpJ1ZZAow4hZIT9tPpGnaqqrhHhay2KR7jYoFMZcA6UXqlS6irRRKHgLDXmUFRShtxlG/WYoDQhfihrITxVp0PzpteTBjDWY2isRl2vNtBRZtIr'
        b'yVqCphvnq0SJ2lqcLxee0mjUtYhGGWi1li5TIrpoU0BO1gCnzCVnUbaVjZJx6RLUC4QwonDxMQnm8igpfHyBxIkLJNotkETn6IwGlDy+HElPnrjCZLsVpkxcIIUUKFYy'
        b'dJnMOeJLEH9C4gyqdQarB2EiqzfJNqvemo1ZiBwVIse1NhHhWUvUWrQaeP1JOzipCUVh0ouw9Jhg4tggQj9KvQFRO526xoChpkZZh/qPMmmrlagz2koEttYVN+jgqVoE'
        b'RPnaavUaGZ3L0A/bUOKYUNKYUPKYUMqYUOqYUNqYUPqYUMbY1uPHBsf2JmFsdxLG9idhbIcSUuywKXTUfPOs6s2MhmSUMbKXaOaV7CVZ2KeJ0qyozE56qf3WMN9lL34M'
        b'KzbxGB6TPhF39mMyJ07c8hg+7YdkQ6jSXrYxJCB1HAlIHU8CUu2RgFSGBKSOYuNUWxKQaocEpE5EAlJtUH3qBCQgdWI6ljZuEGnjB5FmbxBpzCDSRgeRZjuINDuDSJto'
        b'EGk2nU2bYBBpEw8ifdwg0scPIt3eINKZQaSPDiLddhDpdgaRPtEg0m06mz7BINInHkTGuEFkjB9Ehr1BZDCDyBgdRIbtIDLsDCJjokFk2HQ2Y4JBZEw8CIQgx8kK8XaE'
        b'hXi70kK8WVyIt2FT4scIDPH2JIb4CUWGeFvZIH4ioSF+zHjMXczVqeqr9esRlqlHeFvfoFmDOIks+ey52VJCrQx6naoGEUEtpnl2oxPtRyfZj062H51iPzrVfnSa/eh0'
        b'+9EZEwwnHiP0VVp4q7HGoNLTpXNL5WYGDhNzfaMKycMMMzlKzG1iLeTbJmqOqhLewpT+Ebahlok3cw2WUOKYUFLWXLNyxabwOLVLwvioxPFRSMzRYKFYacB8KS03ouqU'
        b'9SpERpUGox6ztcxo6Hql1ojIC12rYsAUkUN7agCJTRE1Ju7qalLsezPbqd8OUbJf9/iMRMU0Ojs0Yr5pM8tLprIGp5snmfEn2vixTDiqqRpmZRHdaclZga4Ea8dKsTMX'
        b'O/Mo81mbbj52sBZwmKdv1KgNjOaxDCvGWIzqEOvWzGrDBRYH69T0WRa1oQSrDX2b80b4lHfckFfUFw5csWtz3pcCytt/hBs/aSbrYSWLchPtUrXObFn5VS0ryduvJZfR'
        b'G5JLii/DM+V6uDemMBvuigVnuZRjKnvTGvo/oDiskQiHBdlVVQ1GrQHJKJ/dwjPjmoOgixFwlI0qzWdejNoQz+23frMQvNUjJgbrxmlGxEK7RY1wHMqCb78OczGzpStH'
        b'3r/eQhGKeoZ3aqjTqmh5g0YTl4eQn1Za2IRVOaPBUXSatbBwCc0Uwyo7jKj1ar2RicBptmFme8/BGkZGlGAaylFI5VV1GngLgZkGsT+2wawclUZVW40HwnjN+p1Rf6JZ'
        b'FMuyzAQRLTDvqTJjEYt8SDP8l1nKHNWHmeVLIhVgyRJlRvvYQCQQcw2kOY0aZSA+tbamgZbS2TqDpSvmmHwtLvlIJM6WaC9b4rhsSfayJY3LlmwvW/K4bCn2sqWMy5Zq'
        b'L1vquGxp9rKljcuWbi8bYmdK5WUJKKKQWRjMVqtIZOK4SBSgi1UINVuUvrRRRo8qfVEkA8sWLayMxqKBRcBntLujy0gXxRRl5Rq1q8gDDZWuFuHCJoy/cHyOgk7OYCh6'
        b'jSUL1j7bizfDDZNkp8KsJUTywAPX1StxohVE7KVYQWWiYomPK2Y/kQGhxxSzn8iA1GOK2U9kQOwxxewnMiD3mGL2ExkQfEwx+4kMSD6mmP1EXCzjccXsJ5Lljn/settP'
        b'JQUfDygTQ0rCY0FlglRS8LHAMkEqKfhYcJkglRR8LMBMkEoKPhZkJkglBR8LNBOkkoKPBZsJUknBxwLOBKlkxz8WclCq3ABvVa1CpGstIr4GwgOvVan1qqxcROJHsR9C'
        b'h0qtRonVmPqVyjodqrVWhXJoVZj/GtVrmiknRnjZxhqsgbMiOQstRUkY844SZDoqW9vE8N746BAh42K1AZFGVTXiQJSGR5IfwcPjC49i8kfTdBp4XW9mE8ak5JGDpBoD'
        b'4kqsEhyhJFLC79gVN8wjNVNzRPoRpcHceg3h0+sxgTeo1GhaDFaVdD5iqg3qGvUqpS32X0IkTquq2pbNYORUmyNLWzYpV8UIMSp1JU4qQquGz+D0DGczMaNmq4ZG/UYt'
        b'KzXG+lWqOovOnBBBwsXhm9oMU62rtM8jqywOZh316RYeOdSGR04b8qLH8sjiSVMeJo5yyGn+owwyfj8Cj5SD/fqiErgvDj9F2QX3FDpQXpXcCFdnXuIYLtnFwiX/BnVp'
        b'mmg8l4z4Yv5kCrlC/CfnINcT/zGcc4ZDEBVEyScreAoXhafl+v1KluWGjY5H3ns6+VFygVyYwdY5kLAzCruQsCMJu6KwGwk7kbA7Ck8iYQEJe6CwJwkLSViEwl4k7EzC'
        b'3ijsQ8IuuCfJbLmYPANwHdN7z+/5c5L7ZgjIeEIVbPOIuHK/R0bkNnZG0J8A/bGS2eZaHKy+sXX7ZzihmsMUzNVA/BTQHdXvIA94pH53eTjKw1M4kgeDHiRPoPk5xCQU'
        b'PwmNLoiMzsPaE095cAbL/OTQVeGWzJPTOIe1Tk95iE5U6+C0XRIx7DgLv8uZKV/w2ccoqclHYAnTDHpjXsoKzvJ0WHDS4Ss7n+HLMjo19uHbuEQ0kTh/hoH4M3yv5zN8'
        b'/XM0u05nya7TY2cVzoLfAX6GH+F95oxLOwwLlNVrEJbUVairh52qEK7SGrDXVckIUxUaxGwa6oYdq4xoG2ur1g874qv5aqWGufEyLCTXYyrqEQqpK6lytIFp3BS5trWZ'
        b'slzItH2ySx7+sdAKcxUOaL6YZ3/8ZIH5TpljmcDmThlaM4WjzZ0ypzG3xxyzncidsnGx1jtltRK28Vk0R4J8pvPqJpWePGW2zrqaXOyowq+YM5HQo6ynRycm0/xIGSE2'
        b'rO4yv4I2z5BSaxDgq1dROQj/GCzYTyKjs3F+hKmqaHIvljY20ghfp9HV6lq1QS+zNGOdc/utMMlMC9ZDmu9pI+XRNsYuZiZdRH5xE3Piiiyp5ob1TFuYOmG6gKiKjC6r'
        b'Q5QCwaWK1hsrNarqWtQ/u6WYGy2MCItK0kpUBIWZ/tCaBkSldDI630DXG5EgU6kipZTmzleqDGtV+JCZjqpW1SiNGoOEvBlPH50rMxBm0jPNProKayWjrGeZNtpMiaWU'
        b'BWAzafPq662Ti5+gN+joKOYmzCp4S9eExGxLQfPdrkwiQ2F+AxVj1si8R6NUtTI6JSE+lk5LiLcWs9kRmXQuDtAkgIvXqLUIylAf6PUqJWo4Wqtaiw9K16TKkmUJ0RKZ'
        b'4HvuEzszD5Juek1CME6lx+cGC67ypZQRPx8Dt0Ev2AZbisH5ubA5nwtegHsL4+CuufiqcV6RBLbElkjBbri/aF4euJBXUlycX8yiYBvocm5ohDdIxd+sdKbEFBUVv+DZ'
        b'WSc8wynjVEzIdqlLrNXa1gn3wV1FiLaBXWMrBSfAfgpuX+9Mzakh1Z5c70ghkhsfv0ZfNYWfRJGHrEKJF2wBV51G37HmyaTRBagB8AKXSl3G18Ons8ljXFLH00sdKIS1'
        b'3OP5izXLso3mMffAzeDlRzqHJqGZdBA2o3pbYnEn90gW2Awa3NAJweUn5qmvaK9w9M+hiuJe3XDlY/wqxRc8AylOyJ4ZQaHHfn76NXfAem3P6bkJ4sC36lJ2bAlpw3ep'
        b'vU5ndjhFHH1TDLjJO31hQISzvuNSB9xa7ap3j+Tw43d0/tcznEHe9W1Tm4UtKzuWn1/0/ILfiddcCrl3d+V/9bC8SpWVK+aucKxx+83dVVlZR/70xDrNp3d+Iy8J+2X2'
        b'J6vv/KKK9eX9aWnUG6u7R/qUtwz8t72p83XBf2PPkjiTC6PFRWAPaImzvPXqiYP7OZRbOKcmAHY8QGBBlas2gJZS2xVnwUOOlB/cxm2CveA6ebzKAr2LhWjiwUF4XlJs'
        b'NL8/8AI7uY7wNNxKKgI3wItLUVVw3/TJNkvNorxDuEK06cjNV/hiGbwQ46+SRuVJ2RQfHGFLwSmwh1wOTwPttag8Xlewy9G8tB7gBQ5sCQfnySsJNzl4JgZcBC0yCdwd'
        b'S6EKzrOTFsLNTAe2VIMjoAW/nCULCU5o8VryKY81HPBycsADfF8ZnJ2fkgAv4yGbmS3cSzMwIKiDO/iyqaCVPLtwBoeK8IBawM3i2GgZzgj3wv0xOCOt57nETSLtwqPg'
        b'wmycDzNuseAVsBcNX4qaBe0cuONJpwf4Xis8XgOP2bTKsHhgJ3ia8gN9XNDiDc5KBD/htSimnY++FMWdH55kIVhj38iZKOZG7xoHKgS/i3MZCpW2ct91p+95erfpOzIP'
        b'PjngGdkTMuAZ84FfWH943oBffr8of2hyDMrrxuTJOLhpwDOiZxJ5/oHyzBnwy+sX5Q2FSM4EdQcNhCSgrK4oa6sBv0nCWa3VpQ34pfeL0ocmR5+R9VQOhqSZQtIGQjLG'
        b'FbDWnTvgN6dfNOd+ZAruZNhQWBz+DRkKCcVlhkLDW7nvjXlm4sJcI27CzgbsPIEdrM7WbcIOuXz7JPW4m8aYxV5h/mdz4Zhc1t2HGSKcaQpyvkMT+bDUgcWqYn1NYffH'
        b'PsHt5idQl4RTOGNu0bMsmDyAYHIFNZ8a/y+MQpwKq0TCGhZWjLIfSFrBoyfSCm1+MjlFo6yvrFZOswEIS9QklgWAqI6ywUDpO4HMXd9vzbTLXLGFz4hCNLBa2qDVrJec'
        b'ZQ1zqhuqflK/a5h+Cyqs/Mz4buvasHMAOSIUSZ6U4T6eqDhSwfQwmOkhU4WdDv6kntUxPXOrGMsFPa57PmOnMOGdwASmg5LHck7/cle3M111qrAwOo/rpN+YOSw/Us50'
        b'0TdHqVdZOaV/uUu1li5ZuKjHdSkQRepO4BDpSuiE/Na/2CkzsDlWmDm0x/WJxmtpnablR5ab+zYhT/fv6ZtzhQ0b+Lj+heJlHIU12TuBMjOsfQ/rOEE/ra9lsKJjGtv8'
        b'XGf0nfC/97HOD3gnzClRn/q5kqePRhF//8cU5ulv12vM28oi35DkMp6n1uvmjA8Pnwd3OvnU2z3caWtqJGzCo9Dz4NPwmUArIbYlwuCQgTwgC8iAuy1EGFxJH1W1MDQ4'
        b'btaED3YdKjAyqKgYdrchqySGUFXMo+JXXwVOlNi/I/nEtM5pAz7RZ+W9osGEbFNC9oA0x+ST0++eM+5lrj0yxDzMxaSHgYCL2OlFTgRr9KnL1/lOP+6pC8EAB/iTqZNC'
        b'KUciGHYw4yTmoQpfb9CpVIZhx8YGvQGLSsPcKrVh/bADk2f9MH+Nksj7wiokkDXUM3oAjkFZO8xrQDtWVyW0WVtXy9piejmNa98IFwI3F/OzS0eFG5LvBRj8FO5I2ndS'
        b'OCS7msFQWOZqA4bOCAyFNmDoPAbghNnOBAzHxdqCoXEqgjhBdnW1HgmUWKqqVlViXIP+rzLf06RV5GkJMVSGBFoinSrpOmOtykboRjOlVyMhl2YeDWF5Wq8yyOhStNME'
        b'GInV4zM4dX1jgw7L/pZsVUotEmBxViTs6lRVBs16unI9xnoC5RqlWqPEVRL5EN/S1SPRvRr1CSEgtJ/NVZhlYlyHABU16tXaWoI2rcXoaLIo0WgEuebe1WFV0fi2BVEG'
        b'pa4Wlam2YDecn8b6XD2WN/WrjXj0lTpl1SqVQS/JFDyiK8iks8cQN3opOaFebsmGa8qkycuVpd/7fsVaigHHTFpOfuml5tuT1nQLmGbSWHuMpoaI90ttb0ta82JAzqRn'
        b'IpdeWqozjMYzoI2SGA+pI5bOl5dKkxJSU+mlWCNszc3APxLxs8uk+bPopeZj1eUxS21f04xWPrpNsBKCCdC4oO2dbWt2tJHQYOsQqCBw1Ffp1I0GM83B64ofpxHYytbo'
        b'G9B6q6qJPgQtD07F+F5DTOGRyZbRsxilCAHJyXKDsr4ev0/VTraqRwhwoIVDDTSaQataTYzvKdE0rFUjOqJah2bcDHAy0lpJg0HFgBEBbpWhrqEa7YxaYz1aSNSWchUC'
        b'QARUKjS6KhXdgEguKcd0EQMV0d7omW6r9TZNyuhctOksG4qUsgVDrNtBoIJNBVZp0AAYK4F6FZNzhdkwYEMV6Qlz4DOlzmBo1GfGxa1du5axbCSrVsVVazWqdQ31cQzf'
        b'GKdsbIxTo8VYJ6sz1GtC4yxVxCXExyclJibEzUpIj09ITo5PTk9KTohPSUvKmLai4ns1Lx4lRkyRwNl1WfoiSQG4ppPKSmLzsbB5FkmtYXJeHdwjMGJbPuA46IR7kjBm'
        b'kyVQCSHwRaLAuL2GRznm8fnUjBVF5wwbKCN+H1gwxVBokR/nwWZssapAmuEwHz/xnh+F30UvhM34BxE0cABcdIKH4V5wwoiflc4BB5ZAbN9rf6gLInoOFA92sp2zwVZi'
        b'GDADHgBn4BUZEoPz8TvymCh4Gf3uLUZCejB4jgtv+j5hnIa7ezKvAF4phHuKFbC1EY3NZmBzYXMJKrSnUNGInNKiAjoQHuZSiOJuRfI/3AxvGsnz7J0bwG6hLBpcQjNz'
        b'C5wQUE4FbHgCXGKTZLjDB3X7Sj64BtpRNSyKA9pZYPMq2EFMAsLb4NkwIWyOk8FdqN1YI3gOnC1AEn8zi6Ln8LjwUIhRhPKtLtkAr8RFsyh2HgseAWdTwcl8xuLdcgfK'
        b'ecZvOBS9IrYtP5Uis7OYB7v1Lqjda/lwj7gGteq4jD0nHjxDZgdcB4fBZZzu4iKDbfAa3J1dBC/FwAMcymc9B5wHl2qNNO5cH9zLFspQHWjq8vG8cCgveAOcAOe5bjng'
        b'qHrfgW0c/R2Uc4RfWt9a7LE13nnHwNPs351Zx/3ZXq14oeaYaWb/Zd3dHrhv4PcbN3Jfm/2noqN/CS9+58HKj377u2dufbF+zq9X/q4y8g9vuKqcXG5+3Khb4BB1gn7x'
        b'zoILi5IWtDQlnv+0bNtXf5/sF2sqbvjn6+ci/qmavmPh77tvzHHe3Tl/LijbOj/CJbHIN6pq94wMuXFZlvNLizN0s5P/e75s3sL0yvrFv2z55sMn7/815cZKj44w18jP'
        b'in7/x7vqv12Sfef50Sfn1GFJm6jY9qBVv/9IwidP7RXgIJdol6oUFltCRLlUqnyA5WywDfSsLiwSwWfs6Vpiknhw/0pwkrEM8IIvOINVTGPUS2APPMt1zJ9DmDd4Bm71'
        b'wuxdF/pvHItXBm4xltj2gwMrY0qk+fnFhbFwr4RFecNbYCs4wE3MySUvrOvhNvhiYWyRPCoPdQUtNTjHXg9ug3aJ+79iYc2udgY7Y0x5WZ9dC5TV1RUMlzHsaeUpRyMJ'
        b'W/l7M1tZJKD86C5el+HMxu6NA74prfwhT9+OOJNntMkzcUiW0JrbMd0kimHUM2kHnxjwDOsyDEZmmiIz++aZIqcNeE4j2pSZd2pN4cUDfiX9opKhyZJWfuvaNrchSTLy'
        b'bDK5RwxNy2nl9/tkmtyzhsKiUeR6E1a1RCHfmjbXIUmCJR8dhnzGNpcPPX2HomQ9ul5WD7bblmEShQ9Jk3qze3N6lqDwNJMoesjbd9Bb0rGslTPkLmp3bXMddJeY3CU9'
        b'oT26AffEQfcMk3tGX8R77tk2nPEkhjO+TFnuMF7BzlXsXMPOdey8iJ0+7NzAzs0JeGmbxcDzvmL0Hz1q0EEHsfMabhtz2Ng+wnfY1kipE9bqPCS6nS9/tIYH3w3s4adT'
        b'fcJsDkfiNOxcje95mrmmYReG17QE+cp68sslhiWczEfuVaphIeZ0EH+HL+Qxg7aOt0pgQ4bcLWSoFbPcDvZY7sPEXiZir/FRGovYNXVSTELsN7Z7SuzcJrubmW7BGKZb'
        b'iJhum0M2WwYcsdeCbCFhusfF2lo/MTbwxjLdSusdTJqxoodY1dn4DQwTohF/gHYD4koRD6O0tf2L+ZxYulbXYGxEqYj9VQqqGuor1VqlhWOKRsxUNGEdGM4B6xOsl3xx'
        b'g1YBWYAF5P/P5T+Oy7cF2kx8vsfEWDVaj3D7Y6Cayc9EWQoQlm3p91xftVbH7AqmHvNGMMcxXKq2Aes9dIQv1TLc5toGzCaq65UaM9+69DEXchH3bv9KrrUHeD8y7Vc2'
        b'NKzC7eMYGV1sXh0lCdMNlSvRRCMZkjmo1GIpIj01PsGsLMITj0QaXHzp6GVcayPW7Z5JK/RGpUZDIAUtzJoGdZUVGpfa3N0dIwiZ0cPYaSLvBZfa3ucdJ8rg7I+IM2Nu'
        b'if4fSCc5qrWqWvMdnv8vofwECSUpNT4xPT0+KSk5KSUpNTUlgUgouNWxYgp/nJhCMwfEBauQrIFQ9v1NhlhW7UbKiKWRtCbwdGF+Mdwdm28VOezJGU+6xoKXnZLhM4i7'
        b'J+ZrdqzxigDPM6LGqKBRO9mISQM8XgRvecQWygqKEfv2+JpBC2xxAmdqIowzUElj9Wp9aXGp2cjV/hglbIW7FiKnGe6HzUjkECDuHFWHwjfky8AxcAQ860SBc/BpYQnY'
        b'jMQcLJDBkxF6fQHcm19cWojtAL4Ab8+L51LiHA7c4wD3ER4+C5wG2/TRxXBfFGZUZRuK88GFKBYVXMvjEfvmONNMcBH0CeGLYN98R7hXWhILzrIpjwxeEgd0wx7QZcTc'
        b'75PwPGJZr9gcWefHPgEvI8lmPja/nABaeOtC/EjHMpaAp8wdy4+VYCvOIngJtMJnOfAl8Hw6WaavFnGIynQkY6PzDvECitiKBucCq4Vgjy9a3DKqDF4NJtNcDW4tFIKT'
        b'8BU8VWg62+CLeUWoengQXsMiWgs4h0JFcF8ellCW+TrO4YBmIo7C0zmTUZefgZjHyKfyn5Qa8fMKcEGdnbQQc1dIRn1yoRHzGiE5lfCgDtxirFRLozXffPfdd0rURQxL'
        b'K2oaiv68cRVzGn9rPp+cxo/EGIoO1LpTRsxfNcELLDwve83SbF7sAmyTPq5AgeAgD+6RR0kQNORZTdBLngCXwHUyc3yty3LY4mDEjF7lPL0cHk4q4FCsKvgSPE/B8+DU'
        b'DHIVIQ7sW5IKe4XmBZo/CiyOduYFAcMBLhJOFU6LQS942YjkdKocFdlnlQsL50XBw3JHRgTE8h+4VYVFwOlefNf6qcQMPTwLX4bb9QXS0uI4DD0lZiFQIpgCO3jgauET'
        b'5DlMgDO4FIO2wL64guJlEj4lBLfZ8IomlthSz8kuZb/Gp9b15tfHpj+5SpjMXKxAIsylJniFEfrnM1cqEFTBXXGlxfOimMrG3FuAx2VI/jrjDFvTN5CtKQY3iBXBF2Nk'
        b'+bFIMuaD/ew4tE+OE4G5aRq2K7W0kIhEbB0rHfYulHDIHINXlKsk/mNKvQCfJvCyHh5emCkbLeScRZqakQO7zANcCnZbR7h2mjrwm508/S7EZHf/SvDc/OJSMMP9+J8e'
        b'ekc9J5o03SMnb4RuahPmXgwqvvlSZEmYX+nXC7/xHPnom4+PHV9zTvXHfI+hP21I+iqo4duOTVsf+NAOurLN/7iX/t7irZ9XKZ76aB1c+cK0SwOXsnhLP/7L11RvKbVm'
        b'07asxHKH6b+6WPQzwfaX3jm4J/dBqUtp7hy/SSu/OdX2G2nXL90bfv38kaChgba9zX/qDpUlHbyr+MVfQn/r8Qvf42tlN5QVXz4dWvLdubNTdD+fFxNxYe6D675v55Y/'
        b'mBRY9+Cez64bA8f6H3jfCj3crSyMmH/3z9cG/xi9/O7u8jlzVma+lrdU+8zlfZqf7772q7/wnzr4KnvWX/pk8KNbGabvtv/90+JNr2zK+fv2xvKw61feyZ5ybfUHi2qe'
        b'PRRQonB9xTfBuD940ZVJH3wU8NrVpfkZa7WfRftEfppa6DutTetwbllg6WfzwDPp9ar0X25Sxp1+5eiRptXvD78c+fbGj6f159dt//qVU3/jXdqZmZDTfPz+0jcaspd9'
        b'2PfcmVu3b3225OPnO4xlyeWfjvD//rH/2aG5x/5klLgQuXkOOAdugZa18EbcqGFgIsyDttQH+HyDFqoL7V6aiEFI72UszMNbixgrZTfnUY/I8ut88WWRcniZMce6b2p9'
        b'YSp4weYOj9sCjgYcyiS3RNaCbbqYaPMdD6cmsG8xGzznX8cYGO4si4PPwUMxMkwpYjFA7mNLp4KLDzA85iRFw4vzC4ui+RR7OSsNHBU/YIzkg6fAPnCuqDiWTXFV8Hoh'
        b'C1xeBk6TztTDm6BjBjiDKIvldgf/CXYkvKkgw4Y34O4Mcg3EegcEnJHZXAMBe8BOchHE6Bg85obHihSbs6VF8DrRYjSFwBt6vEulmN6RSZ4Eu0A7bOWAXngKbmdMMLeD'
        b'7eBkYaxFRQGfwkibvd4N7pV4/bu1FBOrLzDGp83W4uzoMFyxumJUjhv2GaPHGE0guoxsNqPL2CSk/MK6ZvckYwPNA74ZrXxGbTFlwCdqwFPSM2swdropdvqdEFPszAHP'
        b'mURvkX2nyBQ+d8BvXr9o3tBkGaO3YIpNHfCRDHhG95QNSmeYpDPuJJikswY8Z5FiOXeWm8LnD/jJ+0XyoSn5WLeRbnLPGIrCioyNJvdwG9VHZAzWraDQEyb3sHuegR3V'
        b'XTMHPaNMnlH3/KN6RAP+stZZH/r4M7dYboT2Vb8kMYWbLcWjwuaCWC2TfTBzKC2zNbffP+kdUfJ9s9ckSr4XSHd5H106GBhnCozr5QwEJrcKhjy9O6IHPMPOevYsGZRO'
        b'NUmn9lUNSHPuJJqkuQOSOa+HDEgKSZtFrzeZwhcP+C3pFy35ID3rxpw7ua8veLV0YErZQLoCjyzZ5J6C9TEpWbi9BJMo8X5I+Bnfbt9W1yFPn/bMtswu7iCdYKITBjwT'
        b'hsKTepWm8LTWkiEfv0EfWX+QrJf7otMlp75p/d4FrRzcrbBBv2iTH+pc9FDQ5MEgmSlI1qM3BSW1zrnn49eR1pVh8pcO+Mh6wwd80j4IiuyPKhoIKu4XF9/38e+o7apF'
        b'2VHqUExch0OXwzviqCHfwC6HHl6364CvbEgiRbG8Ttdv7kfF9pbdqTQF5bfOGYpNap01KAozicK65CaRZMjdp8PJ5D7ZrDGKeM89wUZJ5Mkoie5i52fY+Tl2XsfOG9h5'
        b'k7IoiX6gfuhR4MdNPaotsiqMhrHzS+QssSqMsCHN1QIWS00URmrWA+L+WIXRWX4GdUOYzeVUWd7D4n/Wj6Hg20y2yp3DlMJB4aTgks+hsBWMWX0XBcv6URRemc1taC0/'
        b'iFLYmFdW8MeobHjZfKLIGRdrezu65HukCldGqohqYNjVuerG2A+C0qkyEhuzmJE1epet0oiq0yjCXwRLwPOgDb6gB3sdV3MojisrHewsZNT9F8DB1XKwtwzuVRTPg9f8'
        b'AubCawqX1Ph4igr04YAt/knMocJLumlyuLcsJR7uTo6vLkRc6GoWQqu305nky1PgaUs1iDW6EceLZoEjCeAG822VTtjeAK4sC2C+fYJY76Pkmy4I516cMtUTPgufQ8gr'
        b'ghLDXnCFedDcCo8vL5TFJyemsCnYGsHfxALPbAK7jJj8ITx+AXTGFOBPhQQ42HwspA+cU28+cIWtT0RAU9v63t4yJNHEOxvfSf2jzw4Xbt3mHr6DbEB2LiLk1U5h5e6D'
        b'wXf2yv/p8p3P2quez//qUsG8dx9+/umn6W+u+sJFdk0wNGjYQC2MvXO4x+Nb/cHc735TGvjd+pm/P/vespAoUMUa7Jn5IOEhXTtJVpvdfGvN4ZRjG59p80z8vVfuf91S'
        b'LGb9bOlsk2R/xK0//vwTh3tf0kt3aV6h/rDizYyiI38+9reN5xp7X/9LUdmF7N9+fndRSnL5G2cuv1/41Yt+s5cXRE9rmve39eWsd/v/8M6DU7KIWy1tf/986Im0X61/'
        b'6Z+DR7XXEjzmGUVL/vyBYo3sPb+SmUv8PX/jtf21yK/3rerzPLJpyue9/Aw/+Ya4ugcPz30SsHDN7zJuzUt7dU96Zuicpz59+SO26E9OqgMOt2+f+zp75HiV6TZnf+vG'
        b'f1BDd2e1VwdLPB5gcEmJB8fJN4Uc0MJ5ssFJlgKcCGSMp74IziMO/FlE0c20HhN60O1KUp+ALywZQ+Tl8Bw7Epz3ekA+NnUUHncdS+ctGUErpvNz/ZkDhkOojWdt7tTu'
        b'p8EuhlNqpBgDxJfC4dOFJbFIdtkfB55XFXEpV/AKp0IaQLqhhF3hcAeCuZZC8l0sbhALnEQMQAcp7ODQYP4yQ6+UYQ/wpxnA0/AgSS6t19t8ZuZpvvkzM9nwAOncyvD5'
        b'FDhfOOY6L+UNLnD94WVX5pbs4WCwpdB8Gxt2ciy3dD1WctC4mvMIz8NeDA9mwecnYPcIq3dqCmkQ3kotJuZoLVenwdPgIJ9yC+KUS3MZXu85+MraQiunNzWB4fVmg24y'
        b'G7PBLtBsZXSawHFyHDMNHCKpM+FuBc3Fn8Sx/SDOSdhOUhuzNo2ait4EmomRXXgVnCdcZI5DPRZM4L7SfB7lCS87glZ2g2yyxON/kWHysDBM47/fMuxQwXxYx/YKERND'
        b'+KMTDH80ssiF8glu17RpDmpbOZgRqe1Sdq7siR70TDF5pgz50ycyOzNbZw0FhJwo7CxsnT3kF9Q2875/0In0znQcHXwivzOfRLfOHPIUdyQP+sea/GMHPGOH/IO7QnCm'
        b'ETbt5zEk8hvhoN/7InF7cVvxCA/5R/iUV0BHdlvBoCjSJIocccBxjua49tK20hEnHCOw5oowiSJGhCjuC2fKS9zBOeHc6dwfnjogThsQpY+44MyulJfviBv2uWPfJOzz'
        b'wD5P7BNhnxf2eSMfacIHh8Q4VNJWMuKLK/fDlQu6qjFzONUUO7U/fJpJPG1ANH3EH2cOQJnNPQ7E4SCUfVCU0Tmzi0c+9LNugE4fCMgYCcaJNElMQ4mcM87dzj2LBujU'
        b'gYC0kRCcOBkljoRiXxjuAJ6XcByKQPHt+R3ZI5E4FGUJSXAo2hKKwaFYUr2kY9aJ4s7iESmOkuExxmFfPPYlYF8i9iVhXzL2pWBfKvalYV869mVgXyb2ZWHfFOybin3T'
        b'kO+L6cjXyh/JYVG+/q28++5e7c5tzp3Le1IHAhPfdU8yR3TITyzqXNRV26PsXjkYkWaKSBsITH/XPePjoPDW3CGRb3tRW1G3Z9eCZ/3fF0m/4FDBEfd9Ats3tG3oSkF8'
        b'9aBPvMknvlfclzHgM7vffbYN9+XKcF83CGAzJzb6YZ7eoNQZhjkIqH8cq+VqYbUe4bJGsPMFci6wzNbK/4GtlbuwWLGYx4r9sbffTvDjqIvCTM5/8BpknYT97WEB8wbV'
        b'YHlaZj6R0ZgVyTqVwajTkrR6WokPzGz00OSwil6lWq9H+Rp1Kj2+AM0osM0adr311MuszcaHTo8egGkYtT2uvnK9gXxD05avc7TD1xklFLFAfiwFtMCnwX6EuS/BA+Dy'
        b'QkRiL4FzCaB5HmjmUWKwmbNBUcfoE6+Bl8FteBDxsrLpT1IylRvRd/qDG2rC7UlkoGWhFFFLmYxDiRAdBWfhqaWEVSyPYFPNYqx9XFF0WeDPGKCu9/Uj5UCLA8UFz4H2'
        b'jSzQnlo4zKogyQXwHKLZVkUV2B/IjgM90UQnlQEvw6sWHrDem0URFhCeX0BYPTG8BPvMeixX+JQOsaAHMkmdS0BnvpzhGxfCVjbYywoALWAP4VwLwQ1Emw6S3m8E2znZ'
        b'rA3wQqT6y67NLD0+vc7adhFfYl1xp/Xn7iDotc1OWzsS7hZ1YwPzLM5MiSdn5pa5jkvdY06/ueJnK07PzZX3+K5/69W3ut+6qaG9+1PXFP11Us7porneVzJbH6RUrrhf'
        b'M5e6sXdb9Yvh2W/t/NUnfm96vMXWLQuqio9J+PNV5W+rHGuEKpcaB4nLb3528hl4aFK3d88BzzMFsurDr37wM82K21eUz5dVOqqSlcnUkU9A3c8c//qk4LXvup2jnY99'
        b'Rv33Vf+orzIlfHIdo3p1ofUiLX/hmKu0XaCT6FRCHesQ0beYqAe3wR52KLiOKDMGm5XgokuMrJhNsaeA66CHVThfzug1mjN18CDYgtgnzA7kS9mUUMWGXZngItGOrAXP'
        b'xxIdil/0mKfQjA4F9mWZGaxKcGOUDSI8UFk5p4E/T+L4g0m1o5VUWwm0Ul+BN5oNgTbHEAL9LsUQ6PluBOUiWhkuOVPSXTIYlm4KS38/LLOtCFHc4JATazrX9Eek9nH6'
        b'5APB2a15Q8GxPetMwWnIFxF9RtOt6U0aiJjROvtg6RcOVHjWiDOqZzAs2RSWPBiWaQrLfD9sCqnJL7BD2RmBaLvY7wS/k98fHNfr2Vv1vjhzSBzc5WASRw2KE0zihN6o'
        b'98RZOAqJ04PiOJM4rpf/vjhtxIFLe7fmIVodGXNGcxI1aorI6YtEDmnZjQqfisiwOLDV+SddScaX3HUs5PzW9krybLcfaX3/Eip4ljXMbVQa6sZ8o8UqV2owUuaZv9GC'
        b'n0vjr3/ir1nxrd9p4f8bv9OyHaHnKzboGWNSvXIN9mk0toh69PUv7nsmnV9DR2NfNI2on545oMQoWLUOmzbA533RsiZ1Y3QsqciM63XM8aAeW4atth46KnVVdeo1Khld'
        b'is9A16r1Kit+J2VIh0h2JV3ToEEM5CPIe/yXSh1LjPhSPehFqOt2TB7i1efmIWa9oLgInC3LAxdg82ywN1aG2Og8+JRDY+4a8kmkmrlOhQgBFBTL4C4kyJTBZvwlV8Sp'
        b'g9v+0ihsxqsQXkeyiS+8TFAsvA1aS9D2PkcUt/BWGEfDAltBewk5q+JMgzdiUNfWgdZp2FlJZO+4OnArphS2w8NsijWfgkfoGPXu23yW/q8o8URq1/F5r64EM0THfhU2'
        b'nCxyyq6X3J0VF3Trk0VuJ+/f/S/tdVFT9NVPvG99I/lnw4mIwu2fLlj9sHd/Gry1/spXb7PubmNPf/Pjlye/NXt58dG313Kf4HkPgt/cBt3DL+enQJNi3U7O+k/uz5u9'
        b'LKThw91X3z3ov3DqPvX+4oq2M293XL1awV1/cHG4c9nn75f0BlEbnD6PyO3ZnjQ98sb5c6KjtfTJ9o6NL9bsfuevB2d++PE75zP++dqZtyr++fGBnas2SD8vn7328y+/'
        b'alI/1bamKnCo4OSXey9+mP7RuguRG2/Wrpf+8VZBdce1v016Mka+xzHkbYeRP+/t9VL+j0MbJ3I5213iRr6VB59Xwh1kqShK5MdNY4EXXNIYJLp/+Xos35GvJq8Enfgr'
        b'Ni3sjeAKfIGk8z1C4BV4da10AXyFUb87gTNs8KwGNDNScnMMbIXH4QVSyS4kJvNL2AFgfzJ5RwGugE4kCbagBBk4C17JJzmEsJeNZhU+SxDwTIR3uwpjwb7SeXAr8z0i'
        b'4Qw27AiYRST0J+H1ZE4GriKuFD/z3MSOTgHbyNGAJzwHnsZ0ViKD+8nY3OLBttWcWnh1NulcFtgMT7mBV2xoC6IrrXA/SU1yWB8Thw+lpTIJG6H9E+BmIQfsiKogJAmi'
        b'bsvSphLpNq6ER/GnsH3AZXid9DkB7AQ3CjGoIzh3hQf4lJOIDbrBjjWk5knwCLy5KRfrB8xzksMWI+7mJfMBgrfTqBSqcSJy6CJ4jGn2lXlg9zpwlukZahb0sGNBn6tE'
        b'+FPFSCE1Ru/OkCcu3vbDLlbahIOEMLkxH2YdKXCnRN7taW1p7dPapnWFDXpGmjwjP/AL6Z9seXbp6UWSp7ZN7RINekaYPCN6Ei9mns3srR6MyTLFZI3JLA7A0txR11ae'
        b'WX98cAqjEO/xHvSMN3nG3/ML6Qrr4fQsG/DLRPQqIgZ/GuZ0faeggzsk9seFu8reF8cjsSIy+b7Ipz2/Lf9w4X3/wBNpnWn4hUxP2KB/nMk/bggROMdOxy7RMdcxldwL'
        b'DOmafCayO/JMbHdsj6G3bGByZt+sdwOz78wfCgg6kdeZ11V2rOQhhwrKYZkCs7/E7XwUmP1+YPa3emyz4q67x+w43t04wexpTgx9c2LoG4f1g3TBRB9rlUkYuueNi+JH'
        b'f99ZJBKs9t2A6J74yx/5/SQikbTzI6kzwkQO6tpRinyKbfTYRIdv8unasfMMTnNiroaqVXpdD448iZ3nGLqNbXkMc2Yr5peQj5fo8OdbEdY3/5PwmB82+vOyZyoSv2+q'
        b'bqiqqGDeDjs26hoaVTrD+h/yjpa8TiIXKIlSfMTKHpC5IoYmRf8np1X4GPvRg6rRlWuwONiKin4ji5jt+YLLdnH/0pFy9ermnNXfyTItXnYvKKQnoz+n/AsOy3UF6/7s'
        b'3KF58x9yQl0iRijkfMXDsSNc5P2igEX5Tb7nLh0SpX7BY/ulNxd8wad8Q+65xw6JUlCMb1pzPooJirjnnjAkmo5igrJZzSX4A0j0PfeYIVEcihInNOeNxmTgmCwS4xN8'
        b'zz2aifHJap6DYvxD77nLmIr8UUWFXzuyXGayvuSj3nfKu/WXkl71fCPpXiB91vNG6KtJb1TjEZSx7s9TDC1a9pAjdclhfUFhF4+hDI0B+78sZ+HBh16Svxr+hsOd4Hv+'
        b'QZ2GjuhLHFSX3LRgsUmpwtXUshC7W4HvwnJKWS6JDyjs4npQAhf7H1ayU1xyWX+lsPu1luXrEvhlKu5YqMkl6CHb2yVmhELOVxzKNfgrHGRsHxFu/pkSnj4foXS9qyuH'
        b'wsephwPZsFsIt5G7No75cI8Q9BgwtROS6yAvi+fiayABidxQT3jkP/rx03HnIeMfNTow3E9jKDiArbCGUAvgpRDwlB/DMV3MBXsKZaA3Hh5noza48DprNdwOrxoxIYc9'
        b'8+GWmCWygkc+Or4DnDJiKQ2eBEfhNtiSH4vloCQu5Qha2OAEvFqACPjzap+PtrD1+O3pKz+/wbylFL/2+mZWUbdBVhVf5Z50espcnxjt8tN74n81w/h5xx+2dm7tLO5s'
        b'fbexElH1asE2fllym1f12viZjtN+xREuOiPg1AqpX3QIS+qAhEd4lOS8WTH4mL5WbDHGMAWYP8J3aT3iMUb1tnFgP1Hd7ndi7EBchm185gg/0M1yiL96EWFf4LYKeGBU'
        b'c4vVtuAoeK6hCT7P0OIz4YiQY0ggycvZS+BWFXjKbcK3m86NOhVi1VUV5Ap1OMv8PXNs5haTzRmTKJGYoW/Ns+57epOvfc86UdBZcLRogJi+ReQvqy2rY22P04Bn4mh4'
        b'3YBnVPOsD928hnz8O+Z0LGjd2MpFac2FthLVMBe3OsxnnpJ/zxdYcd+IE8K2+QLrk+4slt+P/abZGKh0N/9+9SGqd5rwEaNhCfgRJtogbLPRKu4y3mRKzvGjsMmwDLaO'
        b'T8J8FHYgYQcSdkRhJxJ2JGEBCgtJ2ImEGZNhPGISjGc1GYbDQtSeA2rPnfkSuDxRwUpmySeZW3cxp3owBsHkSSRVZE51w2EFX+GkECRz5V7mWHd5MorlolLeFsNbZjNf'
        b'2LQXJxkbQcOG0XiWP7knMfolMPs5j/gt6ZZfriX/I7+PxpOw3EfmFk/Jxbh8BUvui9PRr59tGyjsbymH/AE2/kAbf5A8GLm0TUyIjX+yjT/Uxh9m4w+38UfY+CNt/FE2'
        b'fsmo/9HxyqNl7NkseYyMrfNY5jmZWuYhj8XwO19CjftnQZcW88vm/NIfmp+04mU2+sU8EBYkO8hlBCa8iUk2BwIDPHkcifORx+vEtZ5Ifk9BfBLikZW5SFxWIz6eGnOQ'
        b'btUrYJNnWNlrc5COjYxxUUv4a8R86/G5w//m8fn4z8gLmOPzj0LJQXl81KwVRX/K5zAXKbMz9lJiFkXfWrhC21QcxUT+zecJ1jdsKu+lBOWG0zmxlBG/mNEj8e4EppjW'
        b'u6fkKE8EL1p0aggvtzhQ8lpHd9gKTpGaKhInU7MoKq+KvyLn5rInqE8tvST4TP2RazpHj1nBD97df6XqKCYn4AC2f/RWgXPI+dN75gYVuobuduYURfi87lpz1aNyRd6v'
        b'ldSlzvOn44PWxYcJtt57a8HvZqSmcWYmxxStjRcW1UZXOb6+rKbvRtGrzq+ej6UTvPtWuu/32vFz/qeXWOs/bwx6adrr/wiI35TJqc2kXo0SObXsljgxl8BugN3gNPOd'
        b'eSmHcixjw54cgxgeYVIPwR5wCrSAi0WgC17A58D8SPakKh2Rb+FmVPr2uKdmXHC83hFepshZcHUNuMCoIafaqCGZKQv35dVJ4E2mrp0VBsbiUEyUlMmDcvgEcEF72RS+'
        b'mKg0y8DuTKanYC85VEbkELwErk2CRzmgeza8Ro5lRfAYuDaarRicx0e1/pPgYQ54NgxuIcJzJjgL94OWOCTdIqYIXwvbzYavzADbwYsZD6QoA5qTS7APtKxF1RCGCVUG'
        b'9pciKryrFO6T8amMQn4U3AmeBs+Cbgn/e/hpvFfGmRXysG6usXaF1lMMNV02iQoOa+UeEuLbTqKji5FX8IWAokO7pgwEx7c6D3kGd4UMeIb2OPfqBqIy+jSvVw1Mm0eu'
        b'OGUN+E3pF00ZCk/ANn4mD02O6ZnZM79Lhi0PDYWEE4M/5p8gGjcxFBLWxWvlHnaxIbiMiDfMIxfqh7n4fc+w86hMpW0YdlJrG40GYhzWnqKTEfrMZ1E2ln9SEWqKY9sc'
        b'Qy2dxGKlY6Ev/ccKfUf40dTzwpSfZvbHbDWEV4GHNoG5ENtVshj7wffvRq2bLDmyhLEdEjBqC3+ctRCZ7hD1yCd+f2QvXSpsp34i4ybTUMQs9hhDOnHvBMYxHQyy6eB4'
        b'Oz+yf80EkRUUHte1Oahrug7KjAe/Dcy3FLK86PmX+1NnMZ2DobaiXj2hmRrcnQLcnVHTOd5YIUTX6Brq/+39UK57XD+Kx/ZDRPqB33P9q70wGxLiVxgaDErN47owdwxM'
        b'Lz2y1GzYqAwXtLwTm7A//2H7N+NpP4+h/d7lbNK3+AXu+otL9QyZfxDLPKKIX/DHwABWA6Xe9d8XWXrcVt9SrkW62+y01XfxllP8Q+3g9Tutb4tB1/aZ1yShZT4HZa1l'
        b'+4qV9zUs6p/zefO670hYD/ALhzXgOHjKLr0AN8KsJAM8DY/CronkK6IAGp5kSxdGDeNgXg+ThWoPShzQvrFtY9e8QZ/IIf8AfIc0+cTUTnx/tyfb5CPtd5f+dOM489G6'
        b'ytk2J1FVHj/hJOo/qkr4AR8zN8NHpCuXci9SIfjZrBH7Pz+ZXJ+4tnAaKt30JtplrK+V6pfvv8jSY06w8PD0UejIES/aUo0E/6L4qviDEs8yL9eX/zAj8fiWJBfq4R3e'
        b'07/gxPtL2AQwahCjcYgBDLiLNREvgRiJs4jpwgJ/pgC+iDX+0VIZvAL7sEi/lZ2EeKL2CeVytwryNFDdpKqo1DRUrRr2tYGhsUkElqLNsNToQUXF4tvavQpTZNZgZLYp'
        b'MvtO6J21A5Glrdx2lzaXDtU77mHjgGmYRx7SfY8IvhCL4IuQs8hWBK9H4OT7o0XwR5EN1nx8VUNZBI/DjGVpKpnzfwNQ448FzSZib1MPWZ9z7he7zF0R/FtBHEWubkyB'
        b'B+E2cI5LVYFbVBPVFDeX6LHmJlWCc2wqB2ynNlAb4uBmYp81F74Cn4MtEU+Oee2WXxZVImVRyWAX3xXsrSYvxD73woLNXJHTjBUanyYjRd48xTaVMG+e1PPZv1w0vDyb'
        b'MmIuK3DdPGKuFbavn2uxd2J++mSGwjGGWrthpwAegc+Dw4xykSiTbiWoLQoy2A0Pm5VkBfDQOrWk83c8/cso08XNjleqnkF7JOqt+6sPbAnZH3Io2+3+NhZ7fodY/MR6'
        b'sTin49Dmk6f3uJtW5J6TzMjw5Xctci9z9uUmvVoGfjGJe9al5np07Yq839asaK556pxqy9liFfeeBwh4bevdWQsW0E7yXX/wW97X4nGc1oW81dh+efHsGfXVO4/e3Vcd'
        b'qnePPF1/eu4S1s5VW/su9bVyaqJly189f73oehH9JDVzr0/LlMgP5sy4V/lJZYSR/uXDZA4nrf8tA/9tZ2raLwLu7wyVODAKt555M7HSbK2Tzckapxa+EkMudCwFu+Fu'
        b'G6EHntdbLLi6gf1EeIDt4GmxecvvBfsm3vPwBbifsR3r4yKMNktHTLXzsuOwxZgrXHjxCXj4AT5ERjXsAZfIxVosHyHYAOcLwF5LpXwqF7wQD57nBwS6koFEIHHmNnMh'
        b'FB4GXRYDHXC3mJwtzt+QbtYNumjM2sGGsDwJ164EgwHdasATMRRrdWqDatjdBs2QGIJdrjDY5as1HlRgSOusD/2D74lpQqUOru9KOvhkj+HixrMb++SDcdmmuOw71a9X'
        b'wVUfBEX1S7IGgqb0i6dYCVqPB75u6SO9xOmddcXJ5JPRN3PAZ/o9/6AOw9GMHt6Av/SDybL+uJKByaX9AaVD4oBBcaxJHPuuWIaP3Fw6XZhwj/xdccIQczmza/KAKLxH'
        b'dNH/rH/vogHJNJNo2nui8C+9UE9t0ByfQXNcpa5Wb5dy8i2ozozrMILSVSNnmQ2ue2j0+AnnWIf4YdQpYRynpIprj4SRWxwsi7aF6Fow8mMnc82ojzvmFgcPoT4bVGir'
        b'c0FIjpvNI6hvXOzEepbxNpocSsj1A/C81hPchFfBQUROg6lguHkWMSNNcB284FACz4BrMWiKjJQxv4gUmaoF7bAFXMa4ESNGEbih/n/NfQdcVMf2/91GBykLLH3pLCy9'
        b'gyJVOiLFGsUFFliluQvYeyVYsIMaWayLiqJYsOtMiuls1mRhTXymvcS85AWjCXl5xf/M3AUWNCZ5v7zP5+/LG3bunT5nyjn3nO/5/tN2piwBvUxzONpd0jokal9jl9SS'
        b'xMtqdb320l/Ny0wVWUa59TH5QTKDnabuLkkGoZtMyoK//3vZFNGDLH3KWKgf6A/RxQwvLe/FHojRx6bHAK0SouPMoBwqasBpNthkBy+/gOBX6RA8MVEfRfDkCSH4IJrg'
        b'B3KtKDsnNc9HyfNR2HRZ9+ipeBObOfdtHfscnAZYFM/pM3evk5xe24Be8wAdatMf0QCV4s1a6v3sV1WZPkUz08PH6zycaD4KJEOs9L8wzooVg+E1gFhprz9yxvJQMaPI'
        b'bfiAI8I9tg656SOCw4I9Q0J0+v8TovtdFziauIjRyWnQivbFnVxwFPXDiXLilkkePGZyZPjz7M5H57pL2hAZ7XlHe5Fnl27sagkJXrVab11x2qdz5xqIGG9+xmkNSUyW'
        b'9ie23JpnJ5q32u1UxOZl8cHmdu+UvoMRMs2o/k8MT7y5fGjCfsc3VH1q+BsqTUPG5KuJlpCsdQhp5DGhplgtNb1kRXHttk9AtNNv6yr3VFipbf3R7b7f0UXO2Z/RnNLP'
        b'85AXKiapeKHNHI2nz0nPXtugXvMgHcIy+h2ENbbZRiN0NiyuqsbZalBQo0tqszCpPf6jpBY7ltSGN5RqSleOTHY2fe3exvmfkFnFb1/rhsiMKKc0Zhvmjwer/Keiy08a'
        b'i+LoM8AaO3heImr/ji2LQSmWulR3l7yCaG0HTWvvcIGjaWlCvMFhy9zXuW+NE/WKxXNXPcpqqesfiOXxCnhRs6jP8jkP7kehvQqPtNt4vUzYOWHI6JZriC7cv0pgnCEC'
        b'05qQFmndUmgpjKdDYaPeECITaomscpjI+mxd5KGnWB0pXZ4ns3oilMIElU9ir1uS0jap1zxJh6oMxlCVRq9MVFJXI33uQWmgQ040MWHxg7QOBQt1iWk+JqZHf5CYSOkt'
        b'ej6UwjiUJRhHmywS40VixogNGjWmI2Kz+eLFGtOGmvqSCrGUjETw6GiIxrgEY2GKq+vE0mDdSIjGoFQio0EusTWkhtMgqsPOW8T1daJFxAUJ1ufQmIgXlVSIsMMN/Ogc'
        b'SYn1yIM1RkMglpJSHfitbpKiTlJXKUbDijVNpPU4aMDBc5zK5GgMsFdIXKTGGP8awrwijwnWLKkvRLqMgVVRMIBNcc0iAvOl4dRW1FSLNawy0SINR1wlklQKmBq2BOXU'
        b'sIolJSiin5CUNLkwp0DDTpqclyLdjGdqC2MM+4XHHPMDj2upIQPK3RT5soT1SfGxQBUahRn8TxixZ1aswzMrtoRmxL73X874WfoxRQWJHB5QK7T6ET3ovrFOBi+Ok3LA'
        b'GdhEMeExhi9sB7tpFYKD4wWyugb0ujwGXjBmUPpwH9MMbjKox4sb7Icb4Gk/bHrV6ZOWHZCePQVuypmVCDqFcFtgxpQ0YUYg4qvQJV6gRdeAO2eZJKWAjeSQqodH4Hm4'
        b'E6sILaFqwdbswkX04bUqShAaFsSmGFU53hTY6QIv03CWV5eBw6FoiYiKQ6lQsBVeIOASYEstXI/SMymGABE+2CWErxANBnASoGOQtjMDe8ArqB0MyngmEx2OZ+FWomNf'
        b'6gpOoqx6FANb9wkosBvuAy8T5g7ssQG0GR0q5Xp2OJviwLMMrF9eToZzdq0vVbAIHa/mc93kE6QU0fRHw7kRbEUlMijG7CRfVAg8GEOrU2zwkWYG+AdgAJpsuDvFH76c'
        b'xaBswRF2/HR4lBbNlfGp+PGfM6nauY4s3graKAGe9wFdqEAWauIJcF5IgRawC2wijr3ADsSR7vLDgJXptMLCuPkysIVVDE/ADlKk/kIbSljhokfx5zo6CcNp5tvVE+xC'
        b'JepTDM84fwq0zoomm7kU8VByxPtgF7qIq1pDsYUMcKXOkIZZYcRRy4LQeRQ01/JMdIq2t11go0loGOiiKIZPZgAF9vnAq2ROPKel+gUIZBkZ2YhFNwxmghb/yaScpKoM'
        b'atf0qxw0akZHy4ookrreFhzDxaAZ5y8ORGQFDuSQJq30dcNGAu7wAGwkuo8bmO5gFbxJiloehDi02p36VPxc4b24dLooB9gFj4aGRaAW8WArGq3dIX5krOLhDrNMjOXZ'
        b'BLfSppFmELOO61hxritJeS5GUVRt/E0O2pzz3pzIp8ubCRonoOIQbdnCzQEYOuGVmQSNZY4YMZykvJwhQ0YGZQ+PI+LaxQYvF2gxb9zSzFF2RF/wQh3qWUt9CVl2lTXz'
        b'tJnpeTMD3Qm1rKi5cCtpSvZkK8oj/m10nM1dNnP8VLop8DLYvDI0BBNrBryKurYnJIcsUvFssIUQqhBuyg5nIjo9x4C7ksBmmgnZnrIiNDyI+FmZHYJy1XjRYEpXEavd'
        b'6ZcpBEfhHtiIiFFPwrSDCk+6sqvwonNoJM4GLztGoZZzpCRbPewspymuwhW+DM5QlMl4ljlom06vxctooZ1C+dCAlc6KQRQx1ZmsJjsHrJlLf+48PkEATrApE3OWNewE'
        b'dI99xmHHPAsYaPBNtgcJaNttxKzvDQ6NDMNt3wuOoeJawXE38ioP7opGzYCbbERwWyYijRKmg1EYocowuA2cQ7kQNYGNCbGoDRbgEmmdLWy0yszEXz+Z8Cq/hhHvDtfT'
        b'zT6QGIByoEZzoHw8JsB9C+gLzrpFGLUmG66ajGYL7f56VkxDeJTeAeKtl1BP4ndRiJZt3MbZ0+vVDxzgg+6gMA6qfT+8mUiBNnASKkhpWWBtAWK30MSzKmE7xYI3cJr1'
        b'UlKaRXQqtbniZX20VOdxSnnae/xW32RcGlr9VplJFJDzJ9Ir74YP3JSJthB0KwIvw6tzGIFW9aSYVxPtqCADdBebO3dZ65xqulFB8Bxoy0wXpnPAJbiTYrMZoM0eXqHp'
        b'Ywc4WUCMqGzBugAqAG5PIOr8aHI3GMOt2K48K1uYlwYbJ/tPpZX0EZkJ0YZDUamW+g6+K2m79C1wnSnBXAIbYunVYABbmGB3Grg64jsp3YFFsT22ocNzrslfQnNoTrgG'
        b'dsI2uFMPLcEyISWs0avHn7Y94w0zRzm0gdtyQGe+K5vyBCc49eELyZB6o0PrAGyaEg5XwZNB8GU2xbZEO+900m0HsBPuyiyAW/DGgrbiVgp2gauFRPMvZhZYMxYqDLRA'
        b'OYPynMyRGAhJAWHofOuE+43RaHQDObiBxh1uBFtIAaCdD9r90HBkw61p/hk0Gx0cm8GmvAo4IUuDSX/ZkQ5UWOlqvN299B9vHy1ZX0CzcAjuR1dH0Ai2gpsUuDm5kHQa'
        b'XMoGPc8UCo67MimvQk5owyzSLNSVRtiVOQUdqIz8YoxLdR20g5Pk3URwClzPRwfxFg7s9KKYSxmOYA04TCqeVgzPZhaS4VhhDo+iswUch9dJb3LAJnhhDCYbg3LxLAdN'
        b'bHgxu5yQykxwVAL3m1JU7gRwjQLXbMFNGpq4sxjewKs7ID0H5Uv3D2GjjXi9GOxjV4LzYAPJnOO1Eu5n4QXSCa5T4Dq46k8IpxqcWDIqL5NyGLcC7GdXVcaSLbQCNoJ2'
        b'dDNBBJogoSRwvQ3ZUeaAY/OwAclwY8eBbfCIFWteJpum64P8ZUTwAjrAOhfKZSk8RlAfwNUcjHRFQJ4RVQXSCGyO+WADuMBGRL8ZttFLD3HFcD8HG55Egqsom8hhiLU+'
        b'lQub0DXEGe6aT6EDt5scMAvgKjSb1+GqTH//dHDKJwNr61vFs+CuSHCNtldsN7OE+00oKkUEzlPgPLuSliKvQ6fG+UxduCLYnDKVVZkxkWxOMeh2JjM1RZsTPDEfrTrY'
        b'aetJ412EG1HcgkpMXCZw0VT6TEYb93FwDTaxsN/PkhqqBu3zV2n8sEZ4Ebagq1oaxmbbnDnZnzSR7+LkwEan5iF4iojLF2d5MHrnX0RLNL76k0WaFX306QP2joe0VMoD'
        b'XlpCLUHXkEbJ8YX1TFklGoodr/vs3jMrX5Vr/kakJH+fG0fz8ho+58SDo5/5K27bTLm8SH0gWbmkZNJG22OBcT///WeLJ/9cYimNsHsvwLvh2M6H7z19eu8TleqTn06u'
        b'dK1j9RaBHxYylnyU8cviv+hVrO3qvnPpcJrEYO0O6foPbylnHFwys+MtU98rvmv6NJ0Mk06ft2P1g2rPnjhXu2YKmC9ouLTjy39Up5wrXjlu7hv3n+7+wkl1PSQm50mR'
        b'hfvB5YcO2cc0nSv5NObyfZOD++5ue33Jgrf8XlE47iyPTn/1b747eZHmXjzgYWmvl7jT9XxzrSa+pdigvLn2o/iWMoPQtKhy/jsh66I9DkSa/9Uu8epAekDQuhQPoZ2B'
        b'04ZahuExh/rtrkLbG1P8TD7N+1TW8475af6nJ1b3ig3URm3QN6lnTkvtWtePk4E/69OIpIHmrjL+xyKDhdtrJ1tc+0jZbapvPnVH6/HeL98I9TnVIVmvuuh+2LODt70m'
        b'9eG6f8152zyssfJvb3x1f2Zi0daHHbEVD+P6Vbucf1z5ltEXdS5Z7k9XRLx9tHzS4Nwv3xW6dz5xyCt8+6TZAoe0NypFEe1PnlZ8G3Pu7TcbB3+YVVyhupr2pOM7rwuP'
        b'l4Sde21DjVXsktn3lOPcHAYtl8+PKBRHz5zwKC7r0sdlN/6z6O15M375bMqJ5cte8oudzj9XHfxh5edO99/8t5EPCEhadMjq1fxr2zPXfT7jxpxH47/7IuV2zpyQ+mtu'
        b'X8WmLHrX/H4z+7O4TatcDT67aViYcOdnd+m9/HWXnl4QKZzvB6+7vmbCtfJ/ubwaH/1aapJpG+/18m8/M77fceak1fQZv1RmVr9vFBPjeu7qD5FPYVyl4g6j5+ZTRk5a'
        b'x5VxdwVWxOkZ2DN+wVifZ1iJaqoRrUYFr8AuAtsVYOHmh78UMcEeE7CPkU2tIIpc/vCAN7p/IV5FD5wDRyh2MgOt3iuQdkrnnokYgaZxtSZStEluGddgaqhHccEGFmhj'
        b'1TSAI+SzxwS4HR6FrXC1MegQpg2pe1nAKyy0xmLoDyeb66KGFZXBcbCOBplwBI00lllTAFCApsBAeMWBNu8xgIeZoAm2gOs0vsUZf0/aS9xhuJqW0xpkM0vhETfyvQLu'
        b'AOdL0EJGnYM34fkGRgJYAw/QORvhzflECfoK4nyGsczA0el0zlfC7WgYE3g4mEYygY0lRO86Sy+XqLdFRQ8pt8HmJaTDXi/BV4Y+84C1cLeOp75scIKIln3AAXAg2H2s'
        b'Thqtj5YKu2mw9YPT0Ivz4OAYnTRaIQ1u8iUA7wXwHNprmzBOypZszC6BrUPCagu4ivKL5oCLDbWk1ugCPFvPSLTnRFawwaZA2EIG24SNjlZdu94laGtcxaqBa+BJMmTL'
        b'2d5E/82rdEQDDl1Bz8Pr/2djq9FgHSxRaanGdEQYhaJEAnWbrTUCtqac3bRIXqFKpwi1U0IPCnJuzWg2+phr26LXZtxqvN9UxfVScNWCaKUgusdXKUhRclOaGfetuB/b'
        b'u/d6TLrDfd/uTbve/IK3HZUehSr7qb3cqX1WTnKbu1be+MtP5vZM/EkIlSRPUYSqeIHDsY5QRUOXRBkYr/JLUPESR1JFdHl3TOxJVPEm6jwjJl6VKr+kW3kqXtrYF/NQ'
        b'GbdCVLxJY1+Uqfwm9EhHF09eVKj8Jt6yVPGSx74oV/nF3WKgHA9+bx1VKr/kW8UqXvpzWxWs4qU8tw6mipf0u19IVH7xt9yeUxR54fpr/XheUWKV3/ge1NyEX80xtue/'
        b'OojDRf3o72Bt8yiG4rnJvRQ27QFd7mrbCKVtRL/Av0PWFdqj19Nw2eyW7A6zNypTHTVFGTWlN69QFTVVFTitVzC9Ra+lodWsz9appWz7CrWtr9LWV1F6Zl7HPJVtFPk8'
        b'GadyntiLyMHBpS2uLU4xtWtSx5ye0pvVl6tV/ll9gsAuvQ7nFvYBs99M0O/kJo9Q+CjdQzFy3SQtgcqZx/Xb9R/gr5h+Sp6fYlLXlI4MtTCuJ1QtTLnlfqtBxcvp4zm3'
        b'GbUaySeqeKFq3pwe/dvut8ruFCknzVYlzlFGzVHzSnuLS/t4Tu0s+STFRKVHrIo/XskbT0rVfpeyuWR/1r5nsio46w4atCl9L3rlJNeTN7SbqfmRSn5kj56KP1GJ1wNd'
        b'fJzSI0bFj1Vio/mxZWSrgjPuJJAW/+qrka4maV9lqIJT6XX1vDxoLU5+tiOpquBhuh9TXKYqOG3oxag8GXc4quCc3twpKl7es9lyVMGZd6apeIV9PIcBgbXA5jFl7Wr7'
        b'hLK25mFQGru9mTsy5RFKrmCPrn2KMS0Wx9fHPwbZgnfNZ/BaDmPZ6xEUnBiSkuMPylOsGQx7jIb3R4xYiJS8VU9AdRiHjVaUHf70UkHR0ADkowsW5VKF+sMfXRijRLh/'
        b'AmrLaBEunxorwvWmRbhrvbTKexEGi/uXxFH0lxgiGz0xww+xknKAGXlnynlmLc0NnIHN8Dw8AF4BO1HUjrKDp5YSpnuhCbgItziFouJCqBCwyodU8FKu1j+y3rcWsQ72'
        b'FNGqWZdtSD+MiA7+26JUmpP/QrgcWwZM75pt5/twkR0tZwBXwGl4IzSMjfXLKVTtuRLQDZoJA5EHz+eFhulhToIKhKvEiEk5QYt+3LX+lKd+tXDArIAuXpVqjochKqgs'
        b'yuLDQB+6IR/ZaL1NT3UJ+iDFl075INKU9hTdIIvj1ZTRKQ+aaN1H2xjP9E+ppVPeTEP8EkUZBDUs8/8k3ZxOWT9R+3DqjbTelEr6YUuqVh+y7OVZD1+yo0XlCzzBVsJY'
        b'F4JONjhXQHEaGKjDrbCF7vt+dFPoDg0KYqO7yBGK4YHFs43LSM3zE4nxAxUk8g+4GOVIy3ZAoyUL7EXMufZTP2xJo0VvhxemeIGjcL8R9g6EHQStcqZFwXtBF9wMb2TD'
        b'/XgYL2FEuiPwFK1NoJiXPw1egjsRMftT/v7zSb1ntIjZQRGH53PsuBRhVOFZuBlxuTvhbvw/DmIrN1DF6C52AV6HnYSYRODCArALngA76Y/HRRZE9FcXVjViDhgDNtHK'
        b'TnnwECG1JLA+PN8fsa9h4AAqczvDMhquJx0Nhd1OqDoan4FaBI+BU3RHj8LN08E6VM9JFFtMLZ4IV9Ev1htngGNgPdYFw4pgqJdHybZCJucdgbZTXtMMbiyLoAGenL7J'
        b'KP0FLyIGxUg6KNkY6MyULUStn3r9zvVCjATNXXb1vMEaA4NNNu1TN9uHH+hp/nriwLkzXnPSswa++LDos6f1s64Yl5Ubbmm8Xl92/9r759//NPJoSHtYi/FbLjZNkYeO'
        b'nglfMevNsNwv4k58ViycfsL8gbVZ1N24wgf5rOmsRQVVVfpZq08Xhq8+cXG6xYTGe58tFzQWf/aL3uIi940Sz7/ZTr3LvLHlsrDPrLRJM37r7FXtzvsvvnH4UOoXH91T'
        b'dYo/2Sq7FPQo692v5Zn3rtRdfEnPc/a363pmFS+dctGv0+nKTOvVP1vtfK3/krB1wZMaO/U3zpsGi77m/Xxx4RzFJ8V/9+25mf/J06NmBSbhS6MH5Hcdc16JNon+ovuz'
        b'b3qFlrbdlxvfZ/0yPyx1/Ge3hecGl5teuRx0qjVjRUpkvGDzB8dbVDbbvAePfvXjjpVVf6cmfvTz9ab5TxgfdjfPHWdVPi54a+S/46ZG7mxavnv23/8S6/315DVPU17/'
        b'UQW7Ff9s8Zu48+i00FtZl278FBQy/9vdxwqe/syYZzjr7Y8WCXhPsAxxFjwEb4KmhTFFL7AZAXsqYTut5untSMyKcvx9GeA0InADeAFxbeBAOuHYAqInjwLrgxvBIXA2'
        b'HRwjVp9OoNl/yGgHbAdbsOFO3RQ24eZykyowI5GdDRSJ2LXTFrgFoxImsFAtF+EFmlU7DQ4uxdj1GHCwkZGCeDW9FUy3INBNrHa8wEkfuDn5eRwnzW9OySMGpNzFEOuj'
        b'pfuxKBY8jdbWErQpXwA3aetSOTwUo1VkZayU0WqsMrCdRju8npg97C0dXLGnvxDZTGc7TANrab7pDFq5h4gbdCzMWZ5FWoF74skCp1BnCP82FzE2mH9D3Fu5NeHfbGAr'
        b'7Ux8Vx3YSMaIGv8Mc5YENxEL2SjYAg8P80kmBdlaFEgPQDNvhuhE2UkKCQW7x/Ju4CbcR1jFfNAZgZipNKEvPBcQgL8GolbCDhbKegCcIh7QUSdOg9M6Fk7mYMuIkdN4'
        b'2B5GG1yh/fYsSbU1k0OxmYw0dJgddAA08AZmq3cN2/NmgfO00h44uIhoGkM5OABX6eoHpqLoaBVBoh+YCVfTk3Aa42UTlhzz4/AUoULMkzNh2xMfighfD4Bf4UsxUypK'
        b'QiTVBF8hzfNeaDNiUgWPg2YtU2loQdPDFf/UISxy21jKEEORgxNw+++yntJBjtCwsRmCxmyEpcRxwlMasGhk7Jm2FNe2uW5ntJyxM67PwemBORdrM6vNPZTmHvIpCuYZ'
        b'/Q79Pq49+c9We/9WcwXoTqfmBiq5gV0MFTekK6QrtJcbiV7T8IwKdyXXX82N6PJQc+N6PPq5fDn3uEO7g9o1WOka3BWs4oarubFKbmxPgoobN1yqr5Lrq+YGKblBXRYq'
        b'bmhXYlcSBgV5caX9iPNlq3m+Sp6viuun5gYrucFdripuWFdeV34vN5q8x6zAzsl0EQr0UqjIU6CXwWNbnN/lcSngbIA6JF0Zkn7HRxWSr+bO6J02479NF9nlqeZO6AnR'
        b'GYEIpWtED2p/jJobr+TG30I9TcKvHRVS1Ck1N0rJjeqxVHHH03lc2l263EbGK1HFnUhPxKh6orq81NzEnknklS3dZcT40Zd5FeqzmyK4l+v/G++G53kg0jHY8jHlKLAa'
        b'jKK49tsjWnxUVu5Poh0tPAdiKAvrIfK4a+6NCIaO3TX36rOyVVt5Kq08FVYqK+EDLbPGUbDVPrFKn9ghblTUOk7NC1QkqXkRiNVk3zS+bPyYxRCkMB5RDNcUjGFtPQlj'
        b'P1hY7zXebtySdNec36dbi6393kXbF8nZx03bTVW2Ac1sLZyo3LWX6zGsvdrL9ezz8Dme3Z7d5ab0CFd7jFd6jO+ZpvJI0SrsF2NHc7YOzcbPauz8DpwWoq4zCqblJmZE'
        b'bqHg70OMyD8QIzLDlsGwxOo6f8gyxJs0RmNQRJsiyKQJuPAMHKQyiJYlsTWUJuMn2TiYwMCO5MjNX8B4iO5DT4lF00NsSSKwex7+Cm1iSJyiR+EgGgcxuHSDIZOwoV9Y'
        b'D4YYRtGWL8RegSjyEtVKovSGlZU0JkW5CXkJ2UUFM3JT8jUsmbhOw8aokRpj7Yv8lIJ8mmO7OQzU8n8Soj0DuYKd6ZEAm2HLVjEJ5Mqg3jiMpYKCR24U17Hf3LuPG/KI'
        b'w+SGbUp+pEc5evSbB/Zxw9ATx4hNWSOIKqEYUSWcIKpowVKEGCwlQBc+xRc/EZIn1k795j40xIp18KaUnwxYpgGDRkzTXMZPBsamEwft2aaBgyZ6psE/UCgYNGeZJjMG'
        b'KBw+MqOcXdu57RW9joH9zu79nj79Ht79XgKFh3wm+tPhriiVzxn54eGtYMtjhv64esnr5CZDMWdXuUfLzH43HHPsd/WQF8iN+j19FWHyrEcu5o6WA25cO8s+rlOrbICF'
        b'fj3gOrTmD3DQLwzE69oe2i5DSQMG9PETA8rapd0KlzBgiONGlDVKLee2ZAwY47gJ6nKrTB7WMm/AFMfNKGvHXqfggXE4Yj6S2QLHLSlrt/Yk3MYBKxznjry3xnEblLm1'
        b'BDd+wBbHeSNxOxy3p6yd21ny5JYlAw447jgSd8Jx55H0LjjOp6ztW5Pk7JaYAVccdxt5747ijzzQkOOuYDVRlOgHb/zQ09vRDFFAAYNydGlZpkhXukSoXWKVLrEqlwkq'
        b'h7h+nkNLlsJG6RikdgxXOoarHCNVvKhHHJaD2abMQaNEhqnvYwqHg2nMIFPHJxQKaMMQ8jF8NVgXCC6U6Bq/cSjzAtbMjAmjOP0ht+aPMWpInMUY7AymFONKsN0Q3z5j'
        b'HPq/PsFLGDc6ls8aE2dH6ztT+c5EV9SwcFwYO59D41YMiR+knJf0hjE3DAjmBo4borgRiRuQuDGKm5C4IYmborgZiRuR+DgUNydxYxK3QHFLEjchcSsU55K4Kd2LfJeh'
        b'luZbB+C26pGeGZGQmedIPfMv34ZgOrg8+2YspsNvlGP7e8vx1/mdzIhg5PMLmUQARGvyGWO/lmGG+XZjRpR2K29GRtueYEZYjMxcvkM0g2jtsrCHzDBOviNOMZzXMt9J'
        b'alXOMywTuGoMCABbZk6KxBXd25aUETjeoWf8kkqRTMb3wW7IG8RSmai6FO/aEnG1wMjItwCjO9L+ALF7y5piWU2luI52UokdGVbWYCVM7ChRXFtH+7YkiJO+AUbSBRRW'
        b'4dYYikobJDKskKkx1v4kepUGtL849JhVWtagYc2vRs+qxKWS+ir0zKAWtWphjbS0xGAMZRMZ1hpKV11+yGMoMU/DI8tGY8pB46JHNJtNh11LGBTo+AStNnSmCnVcTRQa'
        b'jhKmGSQYEhHbM0911edFj9ASM0qvltRJiO2fFh15aGwl1bI6UXWJeAR6c3gwYrTQnCNuO3FOrZ4p9srpk0hrt9Je1wW0g7wEvlbFmAZK5tfXYvvlSH6ppFxSJwsYUwvt'
        b'x15bD/Yt+oJa0OuhOqr5osraCpH/86qK5pdUoCpKiAfQYQ+a2pl8fp/ot3yfbEQ0qMohP/Iv7FH42B4hEqGdPyZPmsqvFBWLK/k+6Keu/0tBwBhPlGRSZKSW0U0hY+ET'
        b'otMVwXBFiAxj+FkE+gjnSg3MGvYbSncLrZV8UUkF9gRK6iSOWNES0QKj1hdXiku1a2J0rlwU1lTTPkRRToKLiuJ0T7UriR6T9LphT6oi7bAUi+sWisXV/DC+TyntjFJA'
        b'FmHUcMOHlg49THSMLynVDmjo2AEdWl9aD5zaGF8qLpfI0IigtYyWPJlOIb9eO6z11dhT5m86kx9Hy5V/ZJtTPRPjKap2btaOiTyqHhtcgEZwBBwmNpK5cJPWQ0MusZDU'
        b'uoBAvO+UALhK1y/c+ngT8/krSKGPbLjUF0vQzS9+ruNn4TYU8fEOd6c10EXGz/21QokHeN1C22pN4BFwEl4g5f5jpQl1a2IIReXOzfq6ZglVPx6XexB2zn5uW7XeKPyI'
        b'2aiOQWcP2GS8rAG0L2aSUieV6FF3JA7YvaDwaHoo7aiysqDouWWm++XrFFU6EayC2wzBbnBFq8243syACqLc8UeMrF9eEtNO9urAobTnlQY3ZWcPCaXGtPCiMRaAHYb7'
        b'SkmxKZOMqXeyhFjhUFhUsIi2Y52VVPW8Un3ShLTcZVSRV8BJY9ABu+Cm4ImSa6pXWDIsev2Y6lr//gSzRFcT/YEfsm/z3n9g+NJLjuNfXVqZY/b6l07Q/evlKSXb5+bv'
        b'N98AnqqdH7MyNIlnf7w15/bVrwN6qMJHP3JyBmY9WTJ1Y+ytaNYBkx/Lsj9p8j3x14eu7xs5+yze8Gb3bOd3O1sv39u27XPOG8Fbv3cMdX28/4cFC9buZvsFTf1WOO2x'
        b'5lQVvFXJ06v3V9xRdOR/3mb6+dwqtl/oR9/M/27O4uyrzPsHbzr6mp5+WWBE+0lZA69IhoVlQ7rUN7GwTCaj0XM68sHp0UA80fA40VWALeAYkenBo+Bcsm4pmVBuTXQD'
        b'XGALG54JB/uI5sAcyzlaoZvQY7TMLZzGpGXJHAhUnRDuFmmx6sBh6RMsy65OnUXEgeHVtEAQyGcWEtlPNjziqxVrwcYYItkCBzPAFtqRSucieIoWWVaBs2NFlifKaCy7'
        b'DXOtiYwtmjNaxEaVPglA7wPg5pmgPZq+hPrDbnhRRqSvKJZFrqT+elQ2WKcPXgHtsPFPZs8Ino/F0PE6Gs7HlsaUfbTIjnL3ai9RCA5Xq9zCMRJPv5VNc93eldtXqqy8'
        b'Fa4qKz+C3ZOqsk/r5ab1eQRi7B5Xkkht66OkfbolqKz8SbJ0lX1GLzcDsULt+Qre4dkq11CM50OXuWL7CpWVl8JCZeVLEk9S2af2clO1Lk32Z6KUhnTKxdsX74yTo1I9'
        b'afdwKvvEXm7iA0cXkuQPFe4qOO7c7qxyDf7tpO6ezewPzfnPesF4D/O57+OgFwdKHHyAAxUO7v62+dqw/4sxJmxEKvApliagq6YMb6JPf8bmknYMRh7xMpb3h/yL4Q3q'
        b'kF4Idc54wn+HPVQ+hJszfPH6NQCiEbIawh8qRF3QQdGhr3VDd6vnIPv899hD2laaFOlc3H4NRQbD10/HLesYbpnzmJaR681Iu/6rJq0bAtYZuty9qD2zcHtGgHVc6PYM'
        b'3baeGaj/CwISuwhdBV/UljmoLY+HEXZm7JtBt8mBbpPO9fHPag+6Mb6oPSI8Nn9nDI2Nz8jdUjQWJkr2ZzXKsGjoNviilpWOnjV7LOfXuTj+aRQ0dLl8UVvKn20Lmq3h'
        b'a6lOWwRMImakBY7DpnM5JSyd2jGWNrGdI84HDXVsXfUIf4j9MRgSB4TY/aBpoVmYybDlq/6faPm6TsCsL0SNMUooLcVOcarFC3VnHa0O4h4nBfETdAQz2aLSUnT7Rnd2'
        b'kZadIl5vsC8FIb9cWlNfS/PZIn5JTVWxpJq4ZjdC5OQ7DA3mK+T76qKYoTgBSkOJimtq5uOqMY9PGAi6WuwIfoRJHS4ohp9fU4VZKVoEgH1CaAHERMU19bQTHzxH4tKh'
        b'vmD2BbudF+MulUrKyhArgfYAmokZ3UjteBDHPqjb5VoPFqXDPFCJqJqwQC/iR4MjdLg4vk9NLXE6VDnCz+mOA83rPLPs+D4JxVJxSUV1fXW5TMucEr8WpCEj8yKTScqr'
        b'ydQEkD7qFKT1J8WX6LZagvg8xNORUob4t2Ay6BHRw2wcLjlYIMRCFn6puLgOl4tSlCAOTIIjJUOcJaECCUkvE9eRvkdFozmbhE1qiZBmLGlJxLKY4TlFZUvqtAnocSBP'
        b'htlUn/yaykrMmtYI+L6+VZhXR9Uv9vUdZvJJi0aVQD8aKSIVdbfaPzAN7a/VLyqKhjnTcp41MtJgLfTZc9NjYqVT65JvAD97mEkm5FxTPE9cUscnI0jTUP7kqIigYK0A'
        b'C8unaOoNeH41o0yWY8YIExpqJCXiYYJJFFeKy8twOgF/VnDI7OcVEaId5nox3TxJNWkIXgXJydnZM2bglmJHV7iptaLFVcQtlliKN18hvwqNyzDLrVNhyOgKtcOHoQ1G'
        b'jyd+MlogQlNX4BBlkWrpq0IiajSmfZwHFR8aNPvZ1TNfvHhIvKNDZugpotBqmYSutKaMlCoqnYdmhvQHJyC+vUSL8G96bdOCn1GJZEQSJSmpqJOU46bISioq4TW0s1QK'
        b'Ykby+PPRvOTXievRYh9OgChAwtd2Aa2wKkSRKYX+BaK6YjGWvpVqc6LpoJ3kVNZXzRdXSLWPQ8c8JqWJ6suW1NeJ0c6EnR3yp9ZIZaRSbZ6wGH5CfVmFuLgekyJKkFBf'
        b'V4P3x/naBOEx/PTqUkmDBE1+ZSVKUFglE9UtkY1puTZ1xPOa8NsdinxeNolOtVUvrjbqeflf3K9o0vGRoRkzMiQooGcai8nG1PvMTOo2r0yKavfBfR0uU1S8pL5cMDJ9'
        b'usn5kZ4jEzjqRXC058g0VQeKRqZkdLIIz5HhH0mGBnW4fp00UbqPh6uOHpUY1Tu8YWlBDNCK0f4i+zM6g9FaHFrqPvn0Hjm8wY5gIsTwk1CET8fQmeGTiaLiavR/NK18'
        b'vOdEzX42W8jobCFjsoWMykaAFegtY2pCgX96Mt+nML8O/cX7S/hwsmHgBTppSiFZyfgB3wcRpXaK0bCOdKNeio78ErRbJGl/Cfk6Z11KYR7fZxo8UiFFRIbqChupSgfT'
        b'YSTz8GNtpUNZZfPrpTLBqOPv145PcnSOnITDR1jCKAnt888EgioRw8/Bf/izQoJm/3qyEDpZCEk2MhpDcBTaI1Mbxxds3XEm2BQoCf6DXsw2GlklaWKptDpwklRUj4LK'
        b'gMBJEnSajawK8npkLeB0I/SPM4wsAN2ciOpTKtChgtbyCOmTstCZU0oXM9Q4dGqKxXV458V/0QERMer8Ka5ZFMPH34/Q/l+GT0n0APUhaFQiDJpBpxJV8nFkVIoSSR0m'
        b'GBSOOn5oJBD8hv5BMgrxue4fGhwRgUZ6pA4MuoEqwH9GzUCZCLVuEiJa3YcElgONAP7DnxURNHZZaJeE7gwNAYLE8BPRL/rknBUSOer9MGmRJKO/AIzq7xCMiDYlPR4j'
        b'ixODhaAjJDEhBw3HyAoplpSgDOlJqChEIb/h/VIrhXcsYabdZxF9k6zzM/K1GIPdoCMiE27OMIRbdM2qx8PTJFObBcdDzDLHUnaTkhQz2gjUsHYqsfamwP5iYuwNd8FO'
        b'WiPY0TaukDUdi7mXfWJZRGsirwDnptFuNKkieDMAngWHSN0VoAm8TIyw4+CpwBH4DBY4QAr7Lmx5+RPWAIcKEsWWj6+miF83sMss0g+lzcA+NLB6JDiVkU0DNlKo5CuW'
        b'oCmPWhRmWO6RQOxN+zwn0/CM6Z3O96YbzvqBItgixsKCIbG2LjZjunC+NL0gjRZf6gI0wi2g1UQAzoMzRHom2be1lynTQ+zm3w56vJL7dgaM505YGLK4/oMViZ3t8tjZ'
        b'LT57jBLV1jJvfql1b8+8p68//fHYu+dBmIP+htWPr5T/PfMn1kl1XdPn/yi4xcyKffetDX4JGv/kR3u/mnu8ah/ccCrp9rfnc1M/6tAclW/32fzxqw95jvMK2N/XFpgo'
        b'Mn3HPYxc/suD07u+v/d554NFX19+ssTrg9ATiX+ZZvJ92jHJZ/ndd8P/eWjmD1X/Mv+2w2t/YeP3sxsvLt/hbPWPwZT1mZ+/+XhjhWlvi0ooOxi+0fSXzbGtP+ZsmxK9'
        b'Y1r+zcP/8Fna9/E75dLahsCrn+SmGy/73D77rz287wp+kn8rTO1875XpXdM+nLKxvnb91v98nn61aJ2B57SgScZWAgNayfU62A4v0r5RaJPAudVMf2ziSOTY4GIDbNR6'
        b'N493oq0Cz08kr+oc4/1g4+R0cIpN6VUKoJzpBm6UEDm0XdZoSbtZttYoMKqKxn5sAgpTIoXWC3+xHDoOXiQuwuEBsDrC2BfuBztHIUAO4z/CK3AzEfOPDwDrZJgK/H0I'
        b'Cuc2FpUL11rAZhboqoIbiQh+HjwN9mZmxWalMyhmHsMXtINrgnF/pnMo7EhWx8pvtM2KxmRYXDlk6JfB0KLjOVN8odolSLEAY9c7tNSprNzvO3j3efu0mGCEMw95Q7uw'
        b'i6W2DVPahvV7+3Xkd1l1lfZEnK28FXorsTciVR2RrYzIvlOiishT+ef3ehe0sFumtppgZ9x6reNp59zbk/usneUeKmsvUrRvC36N/XzvH07wBZZET1TZx/dy47G/mZcU'
        b'0b024c2sPiubllK1c4DSOUBlFUBAKNUOfkoHP5WtsIujsg3/2Nm31y9H5Ty5lzd5gMmyDu4Piu7x6A1KuWX1QVAKVtckRkZWSp7/gB7Lwp+oM3oouR7yfKLj6f8B11/J'
        b'De9iq7jhPz/Rpxw9H1MMVIqznyJJ5RzUywv65wALPfjnEwOK54reWfj323srWCp7YS9XiN9Z+P9CwAahqU0ym4IeLsnO1Ktso2QH1qtmBsk2rFdtOPi3s1FyOOtVH4Pk'
        b'INarQRz0m5axj6Nl7CNSKkx9f8hWaQwVjPIzPcpyiYVmfh6WtOPPoBjfa4oDgxGM5ezBGJww+I9oDWL3lc9HGycAwGwt2jinkCrUG0bB/NNdTUsHqTGugFyeOdo86aPN'
        b'IpdNmRfYkFOqvyKNthZKQLvLaVn9lPAgDEnBnmwMzzCWOwt0UAzPwZfBHmM0aNPg6gpqWhzcQjLqx7Lz6UwMiJEZZNjECdJ+Rt6PXc7IrXxEzqT4MAe6IJ51VShcBdq0'
        b'5kfiENhFm0cdBPvghVBHcFRrslTiB9pIMaeW6VFHjJ3xOZm1Y/kk2oDoa645lcWZRD6T92V70OYotwstqGYj8tDkjYYpdErXAFPqjn0Y/kZd+Yt/Bp1y4zwTam5aMH4o'
        b'nBRdT6f0qTKi3plLvulWLh3vSKc8JTWiFgkE5OHFFDH9cF+9PvXFHEfSJDGvWAv30AQPTM/Pzc2lKEYyBc6WgdXZZQTsoxisTQ8NCiIIPkcoqAA34OpYP5KpEm2VV/Jz'
        b'KbQdxhSBYxRcDc/ICJxKPit02MSJ4qTDdmLi1B5Jg85cEizB9k2owG64Bds3zYBricGQLdph24gDMn80vK6gVUTP3wE0g83ExAzumUaFLAQHSfL8XNhJWyqh/b2d8i+X'
        b'Eq05uBvsgLtHGyalws3gAmyaRhtAtaAbRH4uH4N6dFvrgZZxoF0MaHdmLnDTUl1nZXBTKoFiPg+0pkME3NzCgNpU74GXqfDJ0hB6XGVhBlSY2I08TI0zpTFa4BGogBfy'
        b'8bhS1mh81lIi0FhICqldbk0VmORiWl4mnmmkxXQ55cfIzwVyNGcxy43hhTzYDvZMI2ZTxqg3cplpKBo4JjiJXcSchtfR66MSw6inbOIs8K+rph4tiK0BQeZxsYbf/1Cx'
        b'6gffI4J5V/lXugrmqc91/dwV4x5c91bgQ83TezJLB1+H5GS3Lxcs/MtXS1f+fHPAyFDoKrq3g/qn5UH/WV9+bx73jyUGzQOdLmu/8NvzZpH03wdZlYmrCoxnNlUmvP/q'
        b'zpfYxy978vfeP8QeOPWfFp97F79uPJH0TUmz68N1+5KKlsxiXQv97sut1zZTb+u/Gbez4GKCya7dG9YevvJZ/96K6AuLT62rvue6dolFTFD4zraYNWeaPzHebrr2Wvr2'
        b'L39O/kLz3psfhAk73fesSLCxir5ondluVHfK6GMbsDH157M7zJfMPfxa3+2+D1cULf/syNeNfW//s/KbrnkHv+tOenfNUyvFFZelfW/EXtE/sedVl34Tvcn5D5MsMh2L'
        b'9VPf3v5wQ+rGlSWdH36/KeL1DSEF0/r39xybFlK1P0gS8ebfv7p7fucl2axvvn13qRUs+NHrvdMt750qnmz29teVr7lB1RsP/D7JWzLrU3hOOiNCfCVBkvT6w+p10QU3'
        b'n1LT701RLL0t4JJbijfYtvJFn8php632lmIGDhPLlOx0uMqP3HvQBcbAGe6BV5lguyG6w2CKqBoPLqNLcBaDYrsyYtFO8wq6hnfQJi1nvcERGoUaI1AjitiPUahLxtEe'
        b'eJvBekzzupZOJ+ERcDbUgGgtzIF7wb6x0EjYaoY/d3kKxxDshltoz7Hn4NoaHVMksN8eeywyp19eEqGFprVEagBXaVOk5RlE38E4naGrFQEPwr1aS6QMrRe9mx7SEVMp'
        b'tPs2E1sp0ANPEvWMKj1vrcKEVl2iJkCrMFENaZ+3pNR27VUTXzSPc9BpcIVHjIdCJsBLmQQYAhwB14fMlMzAWlYi6PEhSYAcbIPHiJkSuGw14qmdVQO74HEaXOMm7I6n'
        b'i6kE3VozJbPlrORscJIkWAS3uhP9CVp7gmc1pD9RA7aSRqaKKnQNjxLBGXAQ7odttOVRO1wDLum4EqyYRyyPXvGkbbUOCOBJWoNjSH0DzeIFrQrHNNBE9Dxmp8LLoxVQ'
        b'iPbJgslE/yTN+b9wOT9y7cCf/7Tu5snlU8fdPDasJEgTLsTdPHZ5ZNzH91Dzg5T8INq0Xc2Pbk7DwOKLMO44hit34sut989UuLbOaZ70IDASI5afXNmc0uIjn6q091Ny'
        b'hQ+4LrSxilx6fGH7wj6eQx/PWW7TOq6Px1fz/NElsAvdBMPUvAk9XDUv5RYX4/UWHJ/RPqOLoeKFqHlRSl5Uj4WKWM+3jcPWIziTQqTiBXVZdln18sLxCzPsi56gmE9R'
        b'8QK7mF2sXl4YVthOUzsGKx2DRxfVk9iT1MuLJ+/bsluzVTxfNS9IycOmRzza9IgXNbaB8T22al7GrUnPfV5xK02dXKhMLlQnz1Emz+ktKlclV/yRlE50v+e0z+lCPYhE'
        b'46FEQ4J6GY/Gq91KPv2wkxIDtjuREdT+hzuQTHRVzORSBaOX5/trD1EhfTwX1KCBcIcgm8eUg4/tYATFc97e0FKhsvUejHSwFjwaR7nGDExiUC5ubRWtFfKlKufQZuP7'
        b'VrwHHl7HU9tTf3WcScm/MjmkW2rPCKUnNnzixaBRUPKw4RPGuhihhSGSGLAw9EfNM/S0HbQcaZ7C75GVoWcEoiuv7dkDXIrn1GzyLDL4i1VeCDL42KUgtUdE/wVLx2Qn'
        b'xYXBsBz4oyY7ZbgsJmOMR5dh338EjZ6jxYBlazXHsWcXvWH8V70/F/9VymGMuYc/i9qsn1NPfLgpYBs4QRy/56aBC+i+tVmAzijQUZCmdV6uR6XBDfq1cCNsI1bvfnAX'
        b'usbtBCexjSIFjsMrrEoGWMOFnbTd+Y2ZRn76YJsVMe2OhTvoW+lFcAglban1m8ykGHkU3Ac2B0t4kxo5sif4Oj6wgvbxZ4GdCrUEv5YYlW3nKjRVpHm8/7IdK+Dfp179'
        b'enIB+2/l3hn+2KOfd1Zci4VX21s8YP3qFskawa73WPusX22aFbfJJT+gxRA2TJPv79u1qowTurFrX2KS97bgXa5p5pf6gYlzsYnJ0SwTE85b7ZsTQIuv+67sVr6Qo1dk'
        b'qKdXzTctELx8L4uzoe4lUcBWwQbP99i3RQGNk/17Tdf960v242kGVy0DBtNKut13Gf7187k2vKZG122euzzTbPKX+4SC7NtzN3HnBDQPZJTnlvYm/DxOEbclfXWCsw+r'
        b'wOr1W3PfFr7f/PqdVgYVFuUV5RIpGEdkETOchWT00e2hnB3JAKfh2fH0qb83JQYfAlpbEdDNMIBNzOXo1kCf5j7o7F5PEmD/8eCKs14O09EatNKZu8F5e3yaCwPS7NJJ'
        b'CmPYxYTXliWRky4M7JmHLjXnF/pHg6u0HMUQHMeapa/o0wf65ry8TCE2ZL2ImIMsdFobxzNhCzwOjpLLTII33IHLD5zsz6QcwGV02vvK7IgEBnSCIxh9dAu8AhozR/kH'
        b'QcxVG7nwzAbt6NLbhH1/YBDgLZP05jDdYQfYSE5Sk0rKL7CmFBvc+gcImOgYb2OB9XAd3EkMu8HRENCaiS8TgTkcKj1ObzzTFh7i0ofwZdAxM3OYdHMXGHKZoB0cBDvJ'
        b'oDnAq+hW0QS30KPmFqCXyOTBq7QvELAvHF3Zhq9ZU2MJNBc4C3eQNoOj6M512I+2A6Zq/fWAgimEa8HR/zMY1JB8YMTpu8Z0+JSWiRpolyFMrYwow5Xi2uyN3B65N257'
        b'nNxDbeWttPJWJJ5J7Ug9k92R3eOhFk5UCifeSnwj43bGnTp1coEyueBje9det0iVfRQ2q0XbtUmryX4zdM5b2dK+iNVWPkorH4WN2ipIaRXUb+8q91CwFC+p7GOak/q8'
        b'/I7Pb59/rKrVqIWN9m2cWV7wES/oEYvyDnvAtd2bvj19d+YDB6e2yNbItrjWOIWH2iFQ6RDYx7NvM2g1kHMPmI0qpN/JVe523Lvd+7iwXaio6ypQucX0JN91SriV1+fo'
        b'3JbWmiYvOJAzyKKcExlKp4QfcD1/cUr4yCnhFxnWD3qNY5niwXnNwygl1FDXEaOU9Zvaj/TA024XRxlxEv/x2HTQha2DJrOUz2DwsNvFP+KjhPiKEBhojIuwsaYIa8nI'
        b'pJ/j8r/CwTc4+A4Hj3DwBAeDOAebSDpoUHMCdG4wfMoxye8cAfe59pyODErXqPN3aIjeYRAXVXXiKhktjSIHos2waabFnygN1Rl3PNKrxv6jx/9dhjbAhk6ySgYx33zE'
        b'Zpua/2CCncaz2pNaFp8tuZ3/ptWt9H47R7nfZavL+T2GbyZhl/FTsNlwXDxjkOVt6vWIQgH2F4+esnE8jzFk1xmB7TqjiF2n1sE9tv10iNiUOWLXGY7tOiOJXaeVQ7+5'
        b'Vx83GD2xCt2UNPIkDj+JZ5BH2mxBOFuIroHo0JMfDFAHBiimWTajVXbW6hH5pbF12Jfcbqd2jVS6RvYYKl0T1a5pStc0lWuGyjFT4+zWHq12j1a6R/d4Kd0T1O6pSvdU'
        b'lXu6yjkD9dcpk/GYYvCyGI9YuKxBvXqGqf9PFA4f6+MnA+TJYDUr2tRpgELBDw0M1IhWd6Wp8yCTa+o3QKHgMWKiXB7j6IgPqyVFcJ9smOnlUKbwsoE9Ex34m+wFjBzJ'
        b'U7ibIUtCs3Mv9KR4yrvVa+LND1rb5P7L1vpCymuhkV+3p++f8wsbHshK23c+Ivj2/LYj39/rf7jGS6pp/X7hXnX2lwXVR/3O/HDyge19PcNdC4zEN3P5Lie+cln1/sKu'
        b'pd9W3L+ocP/a6vBD65TBPSXmd9/1+Bf7QUV5z+CTEGfl++9E39kV9KqyYmLiRzFbbK5u+SbTszP/k+MBppLE/H3KAzbnj1h/5/Nukom61uwb/gZui0WwZX7z/G/3TzB7'
        b'+b2b9zjrzr5vbcaxs+BGXGiYVSns+0JP9lZy7kaHnruHm/Nf/8D9XHaxppc14YM9TM2XFjmvldx58pGH7U9ltuunRL81/qe7Pcdcj79r+vjUvCLLsNii721V+5b9ZLzA'
        b'dcXbr5/5qdJd9Vp3ldvJGWffOi/ydPrB8PVDsz+pf7gMOjfkOudFffPTd0vfvVf09HZT9/qd3xz8D/Xtzxnf594TsMgVAFxYXg2bEEPNiKLAZcQGb10koI0azkwoetZ1'
        b'sDHYbbAAdhPMy3S4Cryi6xULHKzT/SyCjtnNAo+xS9HghcH/YuH/F1uFB302xpN/z+wZY3YPbC9fWSMqLSqShqAtnJyXiYhI/4POyzDK1HqArW9o2z/OsjmkaWGLa9Oy'
        b'Vpk8RC5qD9+/RDFl/8qzHl3SHtez9T1Tzi7qDridfMcSpqlCsj7m2beEtIhaw/cbyjMQ/9Vli1jI3vE5Stuc3ryC3sKpyrxpKttpH9vw5ZY7q3vNPbD/oumMASPKktuc'
        b'sN16U+JgmIWhxyCFAx9vQ/9BCgUDOBgsYIw3tG+e+oRCfwZXMDwM7VtsnlDoz0AOgzIyH2RK2YZ+g9RI+BMJ0YI1Mh8gLwfqDCmel8JYaRu6yWRQz8CQN2gjZRk6ouQo'
        b'/ImEA/P0SWF5pJiR8DEd4sIekZc/DyTwGIbpjH5LlyMmvf6TVPxUlWVar0kafd6+nOCYbE29am2V7KP9TuKkYaKx/u++i/xv6AUvmLmjP7k975jB5EECe0IjFM34BTMY'
        b'5vjLi07wR0wd8HXipF4sddU4QY8luReRz5adRo8m/bhZvDndCMRzk1cu+buHkVsU29uxWj5rXO/10I8yftY3v3F8wOj+tHRz9vzHJxSH3suceqq/S/zGQVZqQNFdG39z'
        b'nniJ+deHHk6OfFx//NBXh+MXPHr69tR/Vxa+n/202qPhfN4KRXfmnAJ1q2Met23NuoB7Lx3LyDqRsrD/ywT7l++Zc8NMhL5Rd3nAfe66YK+W4g3R9kLzs8De82KfaBs8'
        b'K1meNMj/ad4gt63mMuU2/wgfMSRYTgWawGqwGt/tJ+Ov9Zsz9SmwBlw2BueYUIEetxFxG7zyErwaDOWZk/3hWZwU8wEW8BoLtGfD1bREbg/oKkKlbYPbklZgORYWoOpT'
        b'ZpYsZ3ByEv15+RQ8Pj0zPdvXDu7K1qf02EyDBaCRvIpEDONW2BSoh/0nUIx8Ch4GN2aQ/TITXAbb/TI44CSGVcukYIt5PrnAM8DqJAxZvhVVhvFafWqMBUzYDC+FEp5m'
        b'BrgON8h03s+He4zSmaBruTN5724NzmWmC+ENuDrdXytBNIMvs3J4zjTf0QY762jQ/AvgAg2aDztn053dkl1NWOK0IX5tPbhmYsWE52Ej6KH5oq1gM3b0jhLVahPBqyVG'
        b'oJsJzoOtBUSUa2AP5CjFORPEhCjApoUL6mH3ApMF9QzKFm5jgc1VcDM5GfLgRqNMAo2Fu0OAoNAM7WPCQ7A1j5wMYsRud+DRDwTrTDLR8bEVfwzHD/QpBw82WAsOegp8'
        b'fveh8P/lGaGz+n3IaRE/9O8F58UoaycckMMC37mfop3gsT3Fseoz5apNndFN6cAilanPqkl9bKONWauzei1cj0TdZQvvsU3Rf5+wXf7C9v4L2/8Ttvug3kxzDtpbR8Kf'
        b'SDiwiE+ZcFdN1hFXuWhYleJqDRtr7Ws4dfW1lWINu1Iiq9OwsTBWw66pRa9ZsjqphlO8uE4s07CLa2oqNSxJdZ2GU4YOOfRHipXqsIfZ2vo6DaukQqph1UhLNXqI06gT'
        b'o0iVqFbDWiKp1XBEshKJRMOqEC9CSVDxRhLZkGG7Rq+2vrhSUqLRpyEAZBpjWYWkrK5ILJXWSDWmtSKpTFwkkdVgPWyNaX11SYVIUi0uLRIvKtEYFhXJxKj1RUUaPVrP'
        b'eeQwkGFqn/uif3z+mDnAHtVkmKl5+vQp/hRuwWCUsvA2PDp8RMI/sjPj0+u2gV4Cj7rNM05wZ/1iUIZV+0sqAjTmRUXa39qrwy/22ji/VlQyX1Qu1sIkiErFpTkCA8Jl'
        b'afSLikSVlejsI23HzJjGCI2ntE62UFJXodGrrCkRVco0JnlYy7pKnILHUipiaqefJgT6xjK+qqa0vlIcJy1n0oY5siwUDLAYDMYj1DX2gBllbLpK/wd2pTmDOzDHlTK0'
        b'UBs4KA0cWjLUBt5KA+9eYdxtL+ijEmb0GZj3G9n02oaqjMJ62WH9lHkz70PKntT2/wB1zJMH'
    ))))
