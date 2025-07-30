
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
        b'eJzMvQlAk0f6Pz5vDu4jkHBfQUAJJOFUEfBAULlRREU8IJAgUQRMiFfRehMENSBq8Iw3Kire1lbbzrTdXtsvcdM2S7e7dne7PXa3pVt3t9v2u/3PzBuQy9b2293fH8Iw'
        b'mZl35pnjmfk8zzwz7x/AoB+u7f+XO7BzAChBCVgGShglsw2UcFRcEw+M8qPknGEAuMD0f9e4KLkcoOKfwf4LA6lWA63LIg4Ot1PyhqbfwuBQe9WwXBig5M8Fjtskdl8v'
        b'd5o7Y3aaeGWtUletEtdWiuurVOLZ6+qramvEM9U19aqKKnGdomKFYplK7uRUVKXW9qdVqirVNSqtuFJXU1Gvrq3RihU1SnFFtUKrxaH1teI1tZoV4jXq+ioxKULuVDFu'
        b'UMUi8Z8zaQ0BpqoRNDKNnEZuI6+R32jXaN/o0OjY6NTo3OjS6Nro1ujeKGj0aPRsFDaKGr0avRt9Gn0b/Rr9GwMaAxuDGoMbQxrFjaGNYxrDGsMbIxrHNo47APQ++kC9'
        b'nz5UH64P0Xvq/fUOenu9WO+q5+nd9U56od5F76j30gfogZ6rF+iD9RH6sXqRnq930wfpffXeemf9GL2dnqNn9GH6cXqPykjcTw4bIjmgKXxo22+QOAIOaIgcGopDJEND'
        b'GLAxcqNkLgh7bNwasJa7EKxhcL9w8isGj4J4/CckjWVnGzpzgcQtv9oBf5sl4k6bwBBfmXR1TDjQhWMv2o+uw9OoGTUV5M5BerSroCRKgnZlzZstswPjZvDQ87N9JVyd'
        b'P05atH58TpY0S4aa0O4Q1JLHB25oJzc/GDXqvHB0cQbaQ+L5gMdDW2MYeAzdHq8LIWUcR7dmR+PHWvLystAuSRYPeKK9cJsHF96ZhTokHF0AThWAulB7TnwCTpGDdhfg'
        b'fNxDNancFNgaSYvXzCwgsVl5bKQbujQP7ubGTYTncQaBOAE8hZo1WhKPC4pFd1ELA5yyOLAbPaekdYUXgmCbM7rqjm5oYRO6VYeur4LN7q4ABIbBs8U8e3TCQcJQYtDz'
        b'cB/cippzs1ELF3DRPbR/JQMPoV1wK05BRuQSdD0mB16MzIJXV8vQzhzUApsKCGlwV0y+TGIHZs2wb0B3QnFyP5x8BTSgHegapiy3ADZN5QN+A4NOFaKDON4bx/NdM6Kz'
        b'ZdI8GTq5Qs4AFy+uEzyeZnt4OqciOlMahZpy0fFFpFrOyMBBl5L8KphBXZ/Q3/W92NkX34i7H49YHh6pdnhEO+BRDPB4dsbj2RWPXXc8lj3weBfiseyFR7EPHst+ePQH'
        b'YG4IwqM8BPNAKB7ZYZgvyIgfp4/US/RR+mi9VC/Ty/Ux+lh9nD5en6BPrEygIx7PH03Ow0Y8h454ZsSI54wY1cxGjm3Ejxo3MOKXDR/xgaOM+NnsiB/nZQ9cAEjyjC6r'
        b'do33BDQwwZUD8AQau8W1zGWqby0b6LbUEQgAEK+uKcvdM38pG6hYxgP4f6R+VlmuqNwHnAPVTjj4wwZf3kNPMM3AfDjub5ybcXPH3ADVjjji+clGptseiGP9EsS/iS/3'
        b'jmeDf7nhb+7t7kxkn9jH9d/FKD0d9AJdDI7IxGP0Ocx6zTFzIiPhOXQS7YzJxGMJniuKzM5De6TyLFl2HgNq3B0n58N2XToZmCb1OG19GtylWb1Kp0W3UDe6jq6im+gK'
        b'uoGuuTu4OLk5ujrDPVAPW+JjE+MnxI1PgLdgNw/Ae4sc0UX4vI8ui/DCbnQzOSc3Oz8rLwftwYzfgnZixmlCuzA5kdIouUQWDS/DzoJE2FWIM7iKDqBWtA8Z8ISxF7Uv'
        b'AMAn1tUTXecMGYJkYfIhfdFAhiCHTNZ4EDJ44PEruXSQ4KWniTdskHAdR+l2HMIdMRA4G7m2QTJq3OOnRd4og4SXryG9rDZd/ytPOwf7wg785dDrqUdCt69iuBN6Xrvd'
        b'0rpZMT6spbR5rsoVcWZW//6NTWvHb2ks7+WMhcnL/ZI7fGIrdAFzXdHEwHiT44UPziivGMo1sdxlyeBYrWd9dYSE/5DMXEmwFe7E/bwTNzSeTeTwMG8SA69AvftDwt3Q'
        b'VArPRctxHzSh8/CIlAF2cDdHFuP4kEwM6BAeJd3RsshMZoqMg6MOcmSc1IdkxoX7loNoGdqVm1IQxwd2JQy6GB1GH5oGGlBzJryIH7+M7nI2MDPhc2ibhNfLiZRo8DgH'
        b'jxwtaRrxpk2bvvZKrdTUrlfViCvZxVyuVdUppvRydWrleuJwSOol2PlqE+ibyQEi7wMT2yYaE1snt0/WZ1iFXuzXY8kHkztSD6eahZEWYeS7Qvl9odwsjLUIY0kinwPJ'
        b'bclGdafILJRbyCf+XWHSfWGSWZhsESb3uCR/SbpLY48diV2vY41ipUqLQYWql6fQLNP22peWanQ1paW9zqWlFdUqRY2uDoc8qgzp3rIyMa6PxoMEemKHEp9BYlcR4r8i'
        b'5M/gMExQH/g+54Gbj17dtKJlxSbnPg6fEVmdPfUTmya1THrAc9+UszlvW96mPKuDu9VBqHf+qg9P6IKhoZsK2N8vySDb7ygFXW7J3JkVnNFG5UbCLlwbu/Aow9hV8gYY'
        b'hv/fZxinURjGM19HgjzsYId/vDaXj0fXOQDPwhPlNBy2wwtT5sMtOTiGkQDUGFVPgQHEs1wI7MAo41oBjuEDeCOcrxORsX0TPpOUuxE1k/AZAO0bh/axEeez4ek0f2eM'
        b'MRgPAJ9F3bBTR/pSXVy+FnZGk/A5mDXg9WU0eE6oJ7yNjNFyO8AsAuhsxlQd6X60Y9FKtT3aS5h7PcgLLKKZwx2oNRfjj2vwBq6cFEjRjSkSR7bcgzPh/pQN03Enoe34'
        b'A0/AGzoyoWFPEzQ9hTajPSTuNP5giHCCLt3wrAMHk7gN7cbZoQP4g+7CbbTq6KIA3kDPoubxJOoW/qxFR+lD6OR4TMCz8DS8idE+OoI/5egaLQs9A3fBK+hZuB9eJHF3'
        b'8QfpWdrxHNK8ERfWNtudrAX4syaWbfxL0DAGryB7sjkELTsXwed0hCM2onPw+Nx1OTijcWBc9hK2BQ7DaxI8jR9ZjPksFsTiqWc/jYidGwJvYJizFx3AMXAPKJ09U+dL'
        b'nricD/dU4Z68pkXXVjOAgzqZcPT8JDqDjlgC6MAJJmMaj+dloAEsweiggWnirAaX7RqYVk6LI5YpqiiXs6zO7eXIY3uZCpaLifyDeZiy8NdOqdVqbX1F7cq6KetDVDUV'
        b'tUpVKZmZ5KnVtRWKau0U+aMExeTpYHaK6vGdxH6Mqzo9Opd3hnSGGD2I2xmiIQSqX81Yx2i7sO+Pd5Ycej3+yPG9N4zn9o43hm6P2y7ZPml7xPbx22XbJ28P256wfYXb'
        b'MtnsjXhZ6HbRL0DrlnQdkc545bblTF1MBe98ZUZn/gefKGUVkW2cT8teOr/VvrPREX+W/I/dOX+XTTv4udaHpjuvbg+dn2zXeWn/lf2OB2TjW8bnfnzz4av1V2Vlr3w6'
        b'9rf5810mfiEre/HMza2TdsVtf377yb1v83+55OPQtMVf2SXUVeJ6RcZ8KPoCLym0P87CPagtWg6vBEnQTinA60IXJyF2KV1QHFDbQgwmkT4r1z43nw+c4RUOOgLb1tO1'
        b'YQo6IEXN0gp4BCNtDPLtlnLCgnMfhlG2Q83wJMbRrRSVoJ15GBY0wa5sPhAmclEbPF9LC6ifZgf1FLrYljS6nvmgZyT2w1aX0RytPe1esuawXdzrPKhb1w/+Qpecb21L'
        b'zmy85HjhqdnVz+rja3CwBoV2irqLXhA98gSG9PE5PqF9ADv6WX12wMPzgH2bfatju6M+zeru1we4rjKryOvArLZZxvTW3PZcA2P19jcqDGqD2urrd8zxoKMpvJNr9pVa'
        b'fKWGtD4u8AlgY3FmwRHHlhxc0lF6uJQQIaFOq6OBZ6ggWWa1ZRmVpnSzKNIiijQwOGNBwLuCiPuCCFNlp8IsiLUIYjERAkrRwNjEH1Madsy+kyzYFSRbBMk4lVBE1tLW'
        b'Se2TelwC6Whl2cS+l9H2OtXUlmqx7Fyl0mpIh2p8HtPG7EJoWwmJADSkbQkK1K4G/StiAV4RA8jC9wPOz7osHnCUgYtuKdwnWBUJjOQPWRX/8zCy6klgpCMra/CdPEE4'
        b'sKr5oKzhKc85rAShXpkJDMDBk1tWlj1n6QQwk4aWxXsAMSiOtasrk8p5mWzS96OdgAiI53MFZS7/8IsEdD4OmgxPJ8Sic+giLhnuBeVz4Fl1VMwvgbYex1Y3zibz1uam'
        b'43uf2bvKL4yLlot3bBK9Uh275M098/ZLDvEzfOJOx9on1MfLy16w2898sTzpcvOVvecyAzv3exySJPXmjy0K2Hl87NnuU7HX47PGWOLOxJ7qHtNcxKySveouHe9SdUn5'
        b'RiXH/KLLYRnYN93/rOE9CYdCWnQQtqGzBJWia/C5flyK7sC7D4NodOaCaHmWNEoix2IMxrX3cG18xbyl6A5qlfAfPzXwAQtGbRODR0WVqmJFaYVGpVTX12pKMRIdGUQn'
        b'iSbbJFHPAQKhXmtIaFrbstYYurNB32DUGrWmhI61h9d2jjm4wbjB6hNo0Fk9vQ5I2iSt0e3R+nSruzfh5iCj9tjGgxs7l5lDJlhCJtAgNrFAaEgzTDdMb7c3hhnLjauM'
        b'5YfHmQWhhFPDe4Thpjlm4TiLcFxn4n1hTI9LzBCO5Vaolb32FbW6mnrNuh/BsFLCsCNru2go22ox2/oTxvwB5+diWw3RzI2+4K+3sStVOzyS+JhRWPXnVwtUDmdV/iis'
        b'msGyamMVZtWk5XjclC32XcizceUmdwEQ16XYgboyl7e9c4ENcG3GQGwrUa1g2LgzDsShnRNp8gnePOCQ6sMF08pyNS5LAAWcq93QuQTCqo2ceBCvgRdoUofxeIUUr8So'
        b'piz3Rd1UQCFrA9xTk4BJ4MJTCSABi/BHaNpjri7AN7DbHswuc/md62xAQVyAFu1OwPVwdUkEiWmwmWaQjQ6nJOCOgLf548F4LN+xhS1dLgKRLm8RugKP+uSz8wg6kwaP'
        b'J+AmwYjz1gQwAQuVJ2nqkBmBIAkjDFxcg/+kOLa4nEKPBAI8u10mgolidJOmtCwNBdMyXiPNs3jTlLGAok60Zx06nUCg4lZ0KgkkVcImmnirWwTIXMvhYyLG6GbMY4lY'
        b'BttRK7wGqFC6exKYFA6v0dSOagmYnXSMi8f/GP8IPts+8JAKg5FruDHtliSDZLgvjqZNKpCCYtALMMGcSfJ8lmBohEediCAbkjAdTE9Npn0BL0Sv0eIGzk1IB+nIiM7S'
        b'bNFF1J1MxMTJ8FYGyEBt63QYSYOUZY5a0pZXwmaAGfY6Vm7ZBlvgJS1tNXRkJpgJL6NtNOu18HABAak58OQsMCsOXqGhrjJ0k7BxKuzIBJk6LLHQXDbBu9mI1Brq4Z4s'
        b'kAW3w61szA64GUstpIoYTe3Ixj26dxwL5o/CnYHoGiZ+OurIATnJ8CD7xEl0HGO0a0SYOBudC3LRdnSMNsvfl9gBl0BfOyAuy01PqmKbcPZsXNtrDBFK0Ok8kKcopGk/'
        b'DMYrjbgVALzS/FlZyDahYqIvukaqejIoH+RXhNCUkYqxIDf1ChfnOp1TspTNFV3zwX9kfJzVFICC6fA2Tbu4KAoUZe7h41zLP40W2sadyRnuRdfsiRSTPBvMxqJFM009'
        b'OcUPxCrbObjLUwUaJ3Y0wfOlaC/R9MNbaNscMAceraGJI7CUIVj8NzucODeibDWbWIqh6XFn3HYKdLgQFMKDaDtN/NJ6NxBYtosPYsuq/5crZfnSD+2Bzc64PYPh3rlg'
        b'7mI/dvTuRi3znEljtkuLQBFem27RLMyMP0gU19njqjSkLJxsI+6KAnY6kzFyDB2fB+b5QzZxuzwEpCa+zuDyGpyDZLY2ugLvTXTGzekDm+eD+QnoCk37zoowkCFOx+Fl'
        b'nK9dN7AtX1cCbzrj5oTPZS8ACxrENGWvtw+QRsp4uOUD57n62lhiG2pPcybcdmdOMSh2QHtp2kUbY8Bi0W5S4/KU5RFsrsz0bNhMnjGtWQgWLhfQlB/UjAdVRf8EmC0L'
        b'b80NYIHHiwUJQFk3kyw/nk+PqWADP7WPBWW8pTzM7eW/1zoDCYdthLNKdBE284ioEF0CSmBbDm3fxEAsJjTj9i1auwgsgsdXV3/13XffJQbzgYOvvx0uzqV6biibc6Fu'
        b'AqieHc7HNStcExYE1A7bXwPaObhh33vtl9vbsgrgbMEvlv12hXNn5+2Tt7fcjnlwr+L3E/syTtx6OrelyT78RcM/Pj7+SkDc0tS6zc6l9z9Jl/kLS/+28Zd/fvPyr956'
        b'OO/51jFTf5+SN3b5azUxfUfcLkXwdVn3uFs2Fr52OfbtTy6/3f7+11MmRxZvXvTRd9pjRxZtcT37il4c1XI8x+oq+0vaYmvzFMVUT8i4ODXGSgNf7Kx783bWH3YHrIG3'
        b'JX/I918TVXf6retXlrVMXvGXSae2+73pfK1YIC/Put3i9UHUO9v+bE0tF9Rs2T7pj9sXWb0/K1twu3HDB4zb9llJl1ZtXbVl7uG7F+ye2tb5i7io9z7456Gj3slPfa3l'
        b'+NQfebYw4+jfrl8wXEqO39X+xr0l7z7991+9/fzYtcG+b99O3Vx6Vf5sm8c7Xz93bM0zRz5aeO+vJYrFv70kOJr83fZvMg6+bu6u2ZHtPbd1S/H2YF1rVOCbk1d/ydyd'
        b'v+zY141YViRgDB6IhtewrHYTGqX5ZA9hj5TBMuEFDroU8xQVCbPQVthCwJxMrrBBORE69TCUjOQuzBanc9CuaLQrT5ZNtnc8sSC4A93mokZ4AR6m4mgMMuGpphm15GTB'
        b'i+sn4Tk7ieO3FLU+JNs/QTjiohZezMyXRZJNILSHCzxq8YJl4MLuOeEShyeQGVmMRMaPWCx+BJJ63Wz4SFdRSgSb9cO+U2jYyWGhYSZ3MDSM27lBz0LBB0Jvg8bIGDTt'
        b'Ew9MbZtqFoZbhOEE/AVafQIM9UOQIsZOfm4EDs7p4xKfb4DR5hOHmWy+yOhOmy82odvmS0q5Xcj60jJeKGd92Xmvaljf3Pk9xSWsd3Fpj6KCeh/QUvjER0uhPloK9dFS'
        b'qI+WQn20FOqjpRBfHyBfaVE0gi2KetmiaCIsKYtwYfas3y/QOOAPDTcV9vujZJ3l/f6ECd2afn/q1BeYfn8GM4t5deBbLlPA9MweyKyIWcCQ4m1flzBlDCGBfnUgJBT2'
        b'ObJ+/yBjeb8/bKxJ0++XxnRzWD9gA5JTXxgzKIA4+qw+F+DlrZ/Rx3FxDXo/JLJT2Dm3s7xzbpevOSTeEhLfB+w84qjTOgvj+nqrj68xrlWHH/aKe+AbZAp4NzT+fmh8'
        b'd6I5NMkSmnQ73hw62ew72cg38knrBJv8OhNPhZh9Y0mINTDUNL0j2+BoFQYb11mEks653Z5dC+4LE3uEidYAsXF8HxeIxn/1oTCQChSPHDr4DLo+LvZjMP9A6GNI1NJZ'
        b'dmKaOMMfvOTvlBHJfWkcg91+hTgXj+zHyxBU+z1IhJiAneEsoSQJ6wCRH4genMswHkRAeLzzswr8+xyjwQW3SdwflCDItiUYJEFw/+MSxIiNxdGEfXtWgvhzgivA816k'
        b'oGRldeykKTYJ4t85zliEBw6xqg25f2vItkHkxrSChFgemAgvUAkemhRqS/duvpYIcp8Uv0V2nI7vXfdItfhmrsuRliNvvuG7+URLrJlK8y+1Q5FLItFJHt+X5XnJORIa'
        b'YIu0kP/SDZdp53qvGZf79rxZ/lq/oJ74nYdxwXkJ85AUn76RQyd2PK1zQ8jEHjFPwht1cu3fB2InVn921GjrNbqKeh0WP0s1qkqVRlVToVr/PXF0wl0I2Al3Og+IfMl+'
        b'T2tqe6o+w+ruiWffxKZ1LesGzb5WAZ55DIWGwnYHY6KJY/IwcQ4nmQVhTyBb2/XytLjkJ+eHVMIP30P9liG8kcZjGE/CAo93fjapOgk8gVTNGyZV/z/gCe4oPGGXz25b'
        b'7IRH0GVnDZEMdmFJpQvADrSZRznj9lMYeOLhFZvVk+0e5gxmqk9bBVwtUUH+69IKlgVWPWKBlmm6FqvldKycu/Pyjje8vkiIq49feEl3oulMrOraJlVHoXGr36Yo3555'
        b'vIS6MwwQfuoed9hNwqFQZAnSQwNVTO2Hzw4opm47PCTbAqgDnUGXqWYKtiXalFOsZioA7Zdwhw8gUt0BlvAdpot5xBCPjaHskGdjh9nD2EHoQ+CGKZHdKKVLQmd6Z3o3'
        b'71xWV9Ztzvn8znyWQ4SyHqGsU2kWJliECT0uCUNZoOJHscB0wgKPpbdpCAMU/LcZ4Em0wHw981/WAj/hwlBER/onY91AZ14yIOKneCOXlXm+ceCB3zj7ELnLZfdEPzYw'
        b'u5gD3lxH9cG5joF2QM3b/hGjVePv56NzqF53L9Hsntsb18zY7Y+Lj+2q3PbFcr+V2mS/Fb6v+zYXJfv5vDCj9cV48VLXj07HqrZ+MuZo/p9Ef4qS2+2QV4qb+VGvG3/x'
        b'u9ccrrdGbPd7+2iU+LPyv6z6XOlS+aCaAR+tEJk/34JZhgycsbXwIryQmyddBDFW5uUw8Co66U4ZJtRjHmqWot0xcA86X5CHduVnwS4e8CnkTZgAD/4ITa5rjWptfalS'
        b'pypVKupV64d+pWyy0sYmi3l2rtHWAGlPgLSzqGuhOWCiJWCiwQGzi3Ftj3Ac/nRmXC44X2CWTrZIJ7/A3Jem9UjTrGJJZ9pxV0OW1UdsimvbYNhg9cUIK8CoNqo7mY7q'
        b'w9VmnygDr88VZ97nhhlRnzNES8sjdPQ6VqsUSkzSuh+zs5JJWGpohfaAIUraRbwftDb4WU0OWCVtvxUp+bHrH7LbCDfxWCtKzE8cvR3dWbHXO1TaUZ7ijmJvwHMchUtw'
        b'CG8E33A38mw8NWrc43dWHEfhKT4LtlLdE/B3ID7qWlZYEpXAck/FctY2qzWrTLp5XjRQr93SxNcSjceu+9pDr0/AC8pKpm51/5Jyw2W8i7Nv0+xfWF8rURbDnYbPlXmK'
        b'xa/wihBP2MRcXd6xvCNl0nLj+U3fynf775BWGqtdtROK13iUuoYJ08ctcPpVvOnuhQ9WL9i8UvJBhhUUvbwQWV/bvNy5uD1y4tbqT5S/uM6fx3v7Ycl+//1ldm95g82L'
        b'x7Q9PGfbrA1Hz7mRDVW0CV6NsQcceIKZh7aiY6wRT2MYfCYnKxodZU0nGXhsZQTdY4Gtrh45qEmKH9xVwICc5Q6ohQO3FcNNNNeZ6DQ8geP0JehGDF7oeHkMfB6vug+J'
        b'4m1M2SLUnAdvFMEu3FNwGzNr+RyJ85MK2sOHPNHJ9cvdAxztskw1iKGHfGPFbhs/1/GAMOCAtE3aKm+X69OtQu8DSW1JrcntyfqMB+5efYDnGvO+T5Cx0lRu9pFYfCSt'
        b'PANjiLMGRmC+zSNylXd7knFV22TDZGtAiEliIowuPSU1B8gNGR/6+D8QBBlcjUpTllkgtwjk7NeKY1UHqzqWH17eOalzUnfRualdU83ByWZBikWQ8oUj39ftIcCOPhNL'
        b'iqJAfcGgqcCRTAWY/7NJHe0qdPW1lY9fXtnmcaQzQtmgHW1NIZkThrRJB0m5mZ0SSLPU4jkhgnD9Ezs/qyB20DEWdLtNGSqIDeyZ0DWXPyCIEftRUMn/LwLPEfOD9yjz'
        b'Qwg7P2SNeYMziRvJBYIyta9/Ijs//DFBHHyBuwmAurLAvwrt2MAVMY7+txkx6S0pf6mSDZTXOkdOJUbmgrLq9bkhbODLas/YEEBm9rLFxwW2wOWioAkJTB3ZewjUL53G'
        b'BmY0JFau4PZQneqHE2yWozNy7H2vMJhLxWXSDVX1bODZFIlyO8dESh9zJ24qG3hEM2VCNPMVwQvxV7JtKtmnM1PjKzh9pKBCz4ApbGCld8q0tZyPCZ2FDzeEsYGipb4T'
        b'poMykufi/5kkZgMnZEoFBznd5PExHbx4NjBugsB3AphGGiSXsV/IBtZ7TMsXMbjx68riVykL2MBxUt7GcI6A1Kj6UpStPb9yc1V+yIkleVZb5G62ui/zl+/kVBGSGvZU'
        b'e9na03NC7JeMldTdUy1YwwZ+Zj9bMwtMIwU5nZg+jw38eIYy/gjHwOCCKqNW2xqZ47xsbBjHyODH7cA6W9O9LfFOPMUtJnk2oBU2kuKnu3HyOEkUarlPW80GChPWZ0/h'
        b'fMxgkla7cG3VvBGbMKWM8yrpzUKNazkbGBE1pv7fjJ4EcpbN3gDUUe1X+NrFmB/Ktd/sm5tSg2JdTke88fS4OV/n9L41aUZta7TgrwJT+g43uw1AF3On8vW207Ok5yLT'
        b'/vB6ZFS64O/B/8ps7Wv8F49f8+lfpjBJfVMurflz16HnXrxZJ1x2YJzvOw+kY49gwryWb3kLmD4zoqK62o5Ny/69/6nnfm/kNVe11O3c94a8Iqciq6Qh8osp+2bNzb7i'
        b'XTvlUN07Z6vuW9e/Fxj9sWt+pFdzy/PLXq39o8tH/lnr/nqu6ptvJ+VLTi7+S0jVi8UfeGVHrbqZddp50RuTV8zIi/3ivRWfHZ2iO3d56XsPjp8L1Gz+4PO2UEVl8eJ8'
        b'+Pwlp9+UZRcumH3IfVLk25yN2//lsDHolxu/TEkvq5nV8az5vHfnyV/L5Cd//fmsfS7nO+9zls15Luivv0AOU3rWdfzz7wv/vCoW7TgY9NI7R//5QUP63S/i3vMaX/Hl'
        b'N5ffeXfnp0s8vzz7p8LJzD+Kno5uPvbthwUn5lw+3vBvu32/3huq95BwKa4UrI5jcWU/pkSnxrOwEm6GJ1kTpwur3XKkWI7blbMRbmeAA7zAWReO2h+SedgZHYD3otFu'
        b'O3g9JooBPB2DmtAdpcTzJy5xT7IKki0Y8eCfQYuhB5nqyxU1K0qraqvVZAFZPzKILou/tmmj6/hA5GNIMNQTKx99Rp8dEIgMG3rcw/HH6hNuKrL4RPUIoohq1svIbXWm'
        b'tkMGhTG0VWVUtKpNaWavCLMgotOjc845r27Pc/63OeZIvMIR8yGBh2GO0aN1nnFO60JTnFkUbhaEk2CRQdNKLKE8hAZFqzfOyt+oYc0Y8BOFrfbGOBOnY6JpTueY4wvM'
        b'AdJuj+7yKz5m/0lmwaQhT+mnWz08DUpjkWlOx0Kz99hOD7N3VKfC7BVj9ohhI8uN8a3LTB6tS8weY3CIJyl6HPa4exim71yjX2P1CzKK8KqdZtJ0Tj++xuwXY/GLMdgZ'
        b'7B48ijD7RVn8ogx2RDfsZeAZioxxRoVZILYIxFaBt9HP6GeK6wg8HIibAX8fGSQa/gwbEE8qPcYiGDMigDS2D80kviPocJBZMLY/08d/789iFW5IiyCU9tfotA5/Js5Y'
        b'zj7zPYSNyPV7iE/wp4gmaURS3Heewn4EZkq77xnR4xlhFXkZHY2OptAOl8MueIgYmD4uEIqGJ3vgItpTsLPAmGZ2Cba4BPe4BJOQvJ15TQUtBfqCB2Oi9HnGcLNLiFUY'
        b'MARHOfTy1qkUmu+HTo+2dcoGs5OG6EZHYaBLJDVRiFEEtZD/g+qJ/4CigopWg5FJ/2G8LwngZTV1KnJYD5RgWOQIlA7UnJtTyVVytjmWkCN5PCV3Gxh6zK6ET8N5I8Lt'
        b'aDh/RLg9DbcbEe6g4mGhjlvJUdpvcxgKsUoc9WAtU+JETG8xzLVPUyo1Kq02v8JuUG3oGkpqsxv0q136j9thMEgOEXGowEgPFlU6UEiIaWxyGgYJ7SkktBsBCe1HwD67'
        b'jfY2SDhq3I9Tw/Dz6U65bwk8ORcQ+3S4LRSEomej2aMecxuK+dr92LfwsFm3O84NxrrMWLkg68hni/XRdWD/zkvzFLluD7jid3IXarIWh+cu4udcedj23Zff7S2NTeM4'
        b'Ht33hmT6jncyIx1mf/GGA1zjeevwrDet9X0tJ6Pe2XDybsoHzx/Wd5T8c0bB/5qvvNGn/u34p1xm/T2semnKFzOEF05Xvvvty7Osf/bMCvnk07wP2teHzS8/aVKea5UL'
        b'zkys5kW4mrIkTnRxE+Wi43jlg1skZPGzrXx1vIfkpBNqhxfgvQHLW3gPXmWtb9H+WFZqvACb4Z1oOWsWjK6JqGUwPASffUgOtsH9k9Emcm5tpTyLzRw9y4FN6Do6RcuO'
        b'R1unRMtlZMMAHoHP2sFTnNh4ZKKLNrxZUIQz34P25MjgHrjHHjh7c9ABdBE1wh0zaParpzXA5gK8rqNd0RJ4ngfc4S54wZFb31DAnnU5A5+Noimk8BwPFMMtdg4cP3hw'
        b'Cd0pRifRs6gD3VwMm2OQPgZTSI/6eaLTXLQ5R8ZWYJMabsLxckl2noychGvmLIQ70K0EePv/LOBu2jRYwLUvLa1RrSktXe9u4xS5LYCu468Adh1faw8Cggz2VqEfnmc8'
        b'oq2igAP5bfmmCWZRlEUU1SOKwhNjH+B4xBnr6T9rQPCxpINJpmLT0m7P7qLuktuFPeHTzAFploA0Q0b/44lnk08kH089lWoWxVpEsT2iWKswhBQQ15/iUcz7PoHGBaYK'
        b's08Uhgzv+sTf94nvTrhtb/aZZvGZZuBZxeMMvHZXa1Ao/udkDZXgf27WkAj8z4VscDsPmrSde7kV1VqNnFSfV6GuX9frUFdLbOuVql47bb1GparvddHVPNo7ebyajDRp'
        b'Gf0ZpCpbgZ0RzUnsu7UHASsZs8Kxzp5hpjFk4v6/uT/XrE9F/GOO48ENtzTuUJmZ6Z+FPOks1ACWD0TRiZbJP8f0OpTa7D8lTC9Pq6quJMZmQMwecHBIrVasLFcqpqwX'
        b'9LdMf4grY1seN4HOjK68TYD21Y8ofxkuH5fJLyWdKWE0xGx4UNkaHemQEcW64RRf2ooVdfn/+GIr2WIdS/tHzxMX7T6o6KKupT++6Cq2aPtSdrg+ccGCQU2d2JU6WsED'
        b'C85awJ5uZPfk8Fr7/1AxMtqOHDdfPXa+kaMdi4M8L8459HoiNRJvUR0fspmwxS/pV6D21zz0O3sJQ2f/tZIwPDnDXeg52wRNZucKmYQziLHJ7Deg1VdrB22krvfqb9Qh'
        b'wXS6JBId4ewqB+AbaKg3ZhzONvuMs/iM6xGMGzQB8WlvjTar0A2FQSf7iCrtMQV6kq4kUw2dSxQO/w1cSMdsu2MUOO+WxMUwhPzg6dQBz3GKlarS0l6n0lL2NgTsdykt'
        b'XaVTVLMxdFLE86ymtk6lqV9HJ18N2QzR1BCntr+yva7kyKNCq61QVVeXlkp4mL3YgMEnIB/t5U8bmHWXkqbqh3v/JPGv2hqn/7fPCUxjMhhr/IQ+rrtrYB/4YWcM8Akx'
        b'VPWETMIfs3eyxTtZPwsvdYaknsAE/DELEy3CRH2GFada2yNOwR+zT6rFJ1WfafUKMhT3BE/EH7NXksUrST/zgatXH4frGkkO6Ax3vuACN++W4sfG09FDzWMrgL82N0uS'
        b'neIrk9sBp+Uc1LgmZwizONv+f7kFD8p9Ho+QupIhyLyd2+7eLsB/ru3uak4lB/tsv12cM5i/LgwgZYrsxxJcjxFx/6F6AcbDvG2Ow1A3j1zCQRC80q7L/gwu98LANidF'
        b'93ylA45zHBFnT+OccJzziDgHGueC41xHxDnSODcc5z4izonGCXCcx4g4ZxrnieOEI+JcaJwIx3mNiHPFbeCE50DvbQ4lbmwbKrH80eUzVDKhLeWCpSDfEXKJO83dbxtQ'
        b'uSv9cf54SrswsHlVIrD1i3tXwNCSleNwnuRIEFcZOKLVPWieQZji4BEUe9K4EBwnHhEn7C+t3b7doZLbzusKHUqPMhJLPxzbhQqk39307pWOyrARFIhoKeG4lIgRpXgp'
        b'uXSVlGAprIJCg6/HOQ1WLdlC2TtShsSQLX81lop7eWT6GG22yK+wB49+3IBtfTiMnX0OQ+9PwQuYI17CuLgizMC9EKRRgd4OD2c3urDZjyLeOTiOIrDhEIcRi5f9Rgfb'
        b'wjZq3OCF7YN/4RYaUlnyk1WjrlcrqtXryVUxVSqxwtY0agxDFTUV5K6Z4Y8k1yk0ipVi0kzJ4hlq/JSGPpo1PS1fXKsRK8TxsnpdXbUKZ0IjKms1K8W1lSMyIj8q9vlI'
        b'8rBUPD0rXUKyiExLTy+Yl19Umj8vb/qMQhyRlp9Tml6QMUMiHzWbIlxMtaK+Hme1Rl1dLS5XiStqa1bjKV+lJFfgEDIqajV4iq6rrVGqa5aNmgutgUJXX7tSUa+uUFRX'
        b'r5OL02rYYLVWTO06cH64PuLVuM2UGPWNJMfWPGT8JFO6iK//Qp/+5q2qrVbi4fW4h214ln3e9gW30dwCWULchAnitNzZmWnieMmwXEetE1uSOLK2jtwNpKgepQH7C8XV'
        b'sZWIfaNT/CT59KNSNq/+bz89PxZqsrmx/p+Q15CFakANMwjVueSzt9gcngZ3kz1hqZwcYMgJZBYgfQ69jycEnuDB59AVGd3g+IdgDwhkgG+d1xr5/IwlQJeMA0ORHl4g'
        b'W8Nds5GeaABiUBP2Fcxl85iXSey08/Ky8hh0HLUDuBOdcEQ3URNsZO8Qqqc3qghmr9K5cEPDgI7MP3NQI9pOrL+jc8h54dw5mY8UAKhNAs9BPdwN5qbZowNor4Tmkz+L'
        b'XsICutOeqt5cbdsLK4mne/riF/xXSC2TfYBORuZb1I1ODc4c6XOXw3vZqAWTHFOYiXbm2oFZ6LQdujKtljVEa0FH0E7tKj56Dt4jZ5RwLeD5Nermp9r5Wj+8IC1MMO5q'
        b'S0l5jezw7FC/9rf0rL/UvyowfXxf+EenZ6a/y1myjZe5yWX5rKc+mfn5jAUFSxteK5R3Gbdsmr+p7Onwp9sE/5q3YSvInePu+ELmP/9Z7//3p/73A78XwlN/nxC6xOPT'
        b'lttnPlvxzPwdJe3/UN+3D967VJVxefrdze/8/chJ6PTGXl/ev17+y61ZRWPfe2rD86/qpnLfN+/d8EqXz5Wk1/d9fuD6q2/+efWnZ2bfdfrnu4XKmO8uvSc5f+iVP09I'
        b'+3fZmBlfRblal3C/O9cL/zrtf88Vn5KsW/qN/tcRX14/ufHLtc8v/mgpeLf25TddBfumlAjVBW1VH6bUta6YGTDT6+T6sb0OvV3qY/zPVVcvjrnpess1sclcsFVTu/B0'
        b'Y8rdaev+zXzttED02QmJJz0wIClELc64tSV5OlkU2hnDiUHXgBds5DnA7YuoFsoftlejZnqaAN5yH3SggANvPxTjBPE58GyOPDtPmoWFiS5i88/epOQPr/Nq4NUqusOD'
        b'DqGLuax1KrwJG1lTPdgVQg8ewCOR8LkctDszD+3G4519PgydAF5oGxfdLginpFbDswsHHzQF8FgMe9D0Anr2IRk/6+FeIR4+OIdoRC5oYvOLycE1203PIqDrMjALXrGH'
        b'e2SsBg1tThfnFMhgU4EIXqLDy3kOB+2Og/upAgqdhC1oG2y2kRRZAPjoIIPuLIV3afw81Aa3EhUXfhLehdsAFx1icA22wItUxqqeDA+RpynLTnXHT9/hMFF17FGNu/AI'
        b'PAGbI9CeIUo0R259VsRDonqGB9E5PJybcZyE3qhFW5jNzCkXRMNrfLR9sZJVtl30cKe6tlwG3UM3MCHHGGhAl9NpLDqbAS/iaHmeHTyPOnDsTXLDVUsqrUWKDO2FzbAV'
        b'Hkd78si5DmKd4raMm+zAo7UIU6yAzeUTCwjeJmjbLZ070x2eZvWEt5fB47iKNwhlUtzY+bJMHnCDndwM2CWSuP+cm3Lk8N6A3m6w9g5LXmqMHEpLsajPTsLy/hAqkL7J'
        b'sALpUkfgG2Z4ypRo9om0+EQaeFYfctDdY/z7/uGmpWb/RIt/Yo8o0Sr07t+sM2raphimfOgf3hMx3eyfbvFP7xGlW4XknK3HZHrYeGJHw+GGzlX3Q2J7QmLfJwlTzP6p'
        b'Fv/UHlGq1dvfwLUKgwzJRqVpXmeiKdcsjLMI4/oA30PywCfAmNa+5sDTbU+z5GAJx0tiDQl/NyQW59Yt6lZc97kdfnvVc+PMIdMtIdONPCPvQXhkhyP2VGDKD6xvW9/a'
        b'0N5AqhH4rs+4+z7jOnmdFWafeItPPCEwlZKTbPZPsfin9IhScL1wGR5yq3/QMclBSUf04WhDuiHd6uV3oLSt1FRk9oqyeEWRJ+WdOkvMLOqz+occkx2UdfLM/jKLvwwn'
        b'tykXA0PwP8f+bzbF49goA88iCLMGimmk7Z84nEaKx5nsraIAqyjEkGPimUURFlEE+8XBLJJYRBL2i51ZNM4iGveFIz/U8yHADnm4zwWEEjWmqwH/DlIieLBKhBbi7CLO'
        b'aCL1D+9LDR9qZFiVDVJpDtqvOgmoSmnYOAsheoiLYECxSYbbUw4MM5VoHn5252fVdZ5xTAXPuaU5/Rhd5zZW18kvJbj78Xo3WyP1692KHyn8jEWHS2x6t68jigbwOkFS'
        b'GNv2Q6lIjUqhlNXWVK+TyHFxXGVtxY9UiOKneKXl6oonpnHREBoX9tMYTmjEAsH3kvgjtaa0AQkef2LiluIUmrMknhIV/f2A/qfSRtpNoyHc9aR0KYY02pL+RpMPFhh+'
        b'KomBI0hczgwiloxECQcvAQpW50V5/4kJVzK27QuWcEtQzKbBbft9osf/lXCqvOZobgPbVPXENC8bTnNCP80xTyLi/F/pXjaI7tofQ/fy4XTH9dMt+2Fh6qeP5HMMpfWJ'
        b'yVxJeOwG6Oex2CKqPMBkDd4LE9tGm7iaXnb7WPL+/7CNUCnhfH1ihAiaTtQHWrF62HSmValW0mt6y1WsVmHEg+TqXpsqZa66Zhlumxk6Ta14tmLdSlVNvVachttipMQb'
        b'iRsMNxt+cPUEebw8VvL9MvFoN3rw84tsF6iio2j/jGiKNNFtpOdNY+B5plh9J/8yR5uC4yfz/0T2QdgdEH9Lip93bHwZM21ebmZ1pW/K9lWuv4oX145PmD4heKHP4aA3'
        b'X/g1BxxeuDrT2WFBmYRHwfl0dA8eI8h9ANLC02IW1T5b8nAMTjEV7oc3hsks0ydwbSILOohOs5ZtO5Rof//dssg4k4vuYeRtx2fve7waHJlDpQ4O3ITalzIxsBs++9gd'
        b'GHuy80GuzXLvH7O2AApyyQFQuuviDES+7ZN7hJHWcMm74Yn3wxO7i64vfIH3ksOr9T3hiebwIkt4kSGjPQ9jyPYNPYLwn7QnQ7YVRhBSN2Q3Zonzf8VKZwvL3QT9PcGp'
        b'ImLhzGAO/G+eKiIc2DhiwM9V1bNaTl11vXqlot62lOu0NqUevYG7XqOo0SoG3aRdvm5ERiSPZKo9Ti7Lw2lwVvifYplKU/YDqqfRNhRtJzFec95NNUqxa8bF7Cx5GujG'
        b'48CwDXY/pE+aWUI1Sv3aJHg+RB2AZnG15FLOHdM+Yi/fOzdnb9NxYWZMhbKs2PUlQc/LvBn3RaoMnzzFm5WMeca3EXVxpsiD58ea7uX/ae02+Y4yu7fqgaHOTa2NlHCo'
        b'3KlDF9GWIYqLXLiTVVxMQ9tZ8flk/MIRwrO0hFWfscIzvA1vfs8R2UE2n1pVfWl/P1HMtt6vf+yPiKLsmGVjxwbCjj3CMGvAWGOKqd4cILUESA0ZVh9/g9aY2LqufZ0p'
        b'vm2jYeP7wZE9kpnm4FmW4Fk9vrP6Jake+hl8fInl0F2PYdPHnFt6i3Dr4ylezww5w7QKM64vYdIfcP5zF009kfThNrQST7zC7yBolUg+BIhYgmKHwJAnZUY5nqaJzkkz'
        b'EQw7fzWwdm0Bj8zqDgB6soJsJ/Wfrvivnb76IJcZZa9lYPqp1aiXqWsU9biWauXj8FeNao1t8Y6Tx42i0X68Gl/J6sppA/afQsUFycWFqlU6tcbWvkrsq6gXK1Xl6nrt'
        b'qFsHZPLDFGhrV/bLFGqMvBTV2lqaAZs120WVKo328RsLugqWovTpWRjTqVfpSH4YL0cS/CbW9FOFy8qqVxBE9/1z6GimiQ75uilkBnqmDh3PyUcttou/82VzMuXZeeSc'
        b'V1NMIdLnzsnkFkrguSzx0nLNGHRIs1G91BFMX+a+Eu1FBh253x8+H4xuoeZicsX9gMr9UR4AXkX75mGgso9ZhW44LIAXK+hlTCtm1aBrLrjb5WgX6gTwaBC6Q+8Uh8fQ'
        b'9qe0brr5mcTebh7SS+cjPTxTgPagZniuKFNKymjJykU7GTyDn5KshfvD0ZkiDkD74C2X2Ti3Vl0UzmdZ4YrBivq6gRxnLwhEV2Xz7cHsp+3gqWyoV8sWl/G1BwirXCw4'
        b'9Hoymf7Nt/ZGYGi286sc4weBO0SvqFpcXC74Kb4d+0r+GX6uS/EL9KCrLi4urp7zS7uDLhNX+s3+3fLbvy0/7pkf/pQxueO8ddPynpUVNS2cgy86CRe+sOOXn4kqiza8'
        b'/G1k5bWyg9ntIcbNG0FL3/kZCQFvv9915M3i910frktNafnday5/XPXC32N5CXU3AXjr6DjtXUeJI3uPYSe8Cpvw8tavAYW75zrXcNAhdAXepVemJqPD6Igz2oq6osgd'
        b'OWRRsa09IARe46HLleFUXwqPjkVdK5C+/zIGeir93lJW4XyRA6/lDNL31kW5CLhe8PlsVim8KwdeHbKsAS/pNLKqidFtVtG7s45L8CS8Ttqfvq8AA0poFLNWlZfRKdQ5'
        b'REsOfFEXahTzlirgeVYVfzMO15Xoiv1QI54aWFXxQlbXG4QOBhFFMbyBTuTZ2RTFRdU/dPp307Cl8tGcQu5xHLLwDImiS6XZtlSWuZBjElMJLG3A64tXMfN+cFRP9Hxz'
        b'8AJL8IIe3wVDFJe2Y8Nzu8OvS80BUy0BRDXmlcPQhTT9hQqzJMscnG0Jzu7xzSYa3anWgJDDk94NiLkfENPNMweMtwSMJ0/MZp/INwcXWIILenwLhpUiMU7pDDMHyC0B'
        b'cpI8k00+7YUE8+Dl2qYNZf8Z8O9g83h2yR5YLR6/blPr+CEL94MRC/eQ9msiC3cDGDhpWODCMOTumSdyflZ7qA7HGHDZbfKPUSIO6OfwIvHEi/dxIp6TwwHsmh1H1TSP'
        b'lpXv0x/8aPXBNta+kEcu1HliAk8NJTBl1KUmfV768P3yUUiVcHt5KzWqyl47rXpZjUrZ64gXSZ1Gg+XsmRWDXwzk0l+NNkDu3ek3/KCgw2HAaonRu9LbOjl6t0oXCkF4'
        b'GIIMM+zYwHccBVTgEP4ImMHbyLdBkFHjhkCQju+FIOzLhljRha7mg3USjzf6IG3DruX9zw7cbvH4/XvakuxT9BHcCyRMQfQ6cnG6ooaoPhS2uPLlGJWMCkeIaQlGCHML'
        b'kibExlGjEmLwoSRqLHXNsscWP9CByeKZ1Ypl4jVVKpvJCq4wqfOjFP2VelzxNbX1oxSjUeGK1GiTxWnDZcIyW3V+AM8MXB8wCM845evIZSJTYTc8NBTPIL1tvZyXKarF'
        b'gYU2cMLEe8K95D7IHHQtG0SgU27oIDqzQEfUM/ASNGblyGVR2XgRHJzDQM6Z2fMi2UvN8/MYdLcKoNNBLqhzvSsVTR/OznQYxxUzeKrMflCRCnRE9ZGfSSDMaLKpLAld'
        b'z86b+8jaAcDmuY7oeYxvjCw9p0tqULOMpKF7x1kEAkXPJy9KGWTlkCnNzpVnyaLsAGqWuPjCs6uQfhrFaPZCuH+ISURWONolJeCqYG4k2p2L9uRIJbJsPliPzjrCXSXk'
        b'9hmqx7LDK/MWWjIXbVYA3hQGXghk34CENqGTY6PZh/MYeG4dcEAdnKfGoIv0nUVK1LwyOjvP1oZMGdQD4TguOpSGtqmjI5q49PhU1+3x21snk4Mv248kTc3b+RJ8p2IV'
        b'2O/S+b5gXNmxioSUcsXH7acPvJT+XmJo537py+98c3Tlh7q13GeC998O+vy2tyBDBPYWf9pYdnHxjfdvfvrFnkbp5HDD2L1ruG7LK9/fMW/ql66/Kr7PnV+8pOPCq3MD'
        b'1n0kWWLW/K7tf94umHpBdXxKa8j4ojGafMPayper/rHv7WfzsAiBrv31Xtj4FzfGrhGvUd9P+d9ev9/83TkkfoLDuRQJ+w6UInQUbc+Bz6ALZC8bcMqZOG/UScFN+cJk'
        b'5+yGx2Cv4Gj2yMjdZfjZRyDOGV2rJiAuEBkovnHIleZk5UVh7MzxaQAOsJkDN8N969i97Dv5qHUI+CqFbaxOAT2/iFI3Ee50oxnDI/Aie4MDuqligZkRXg8ldgfkhOtZ'
        b'uIcH7Ko5Y/zhLmokge7BW+PoMdgC9rZ9KbMBnQHCGC4G1gZ4ioJDd9TuSZSOgzfhwycnS1CHxOX/tHNO1oeR2+bOBE7YJpn1wsEYwxZI0ZnMtnle7kr0iklkU7iQed9/'
        b'bM+42Wb/ORb/OT2iOVahT3sqicljTBmnci3hE9kvNFmO2T/X4p/bI8odsbH+/vCNdR9jyiMtyX2htEcopWlmmf0zLf6ZPaJMdju90lRhFkZZhHS3OsEaFGVc0jnBHBRv'
        b'CYo3zOxPUmUWxliEMexZnaCwY4sOLupYcngJSeBnzDiWfTC7I/dw7n1hZI8wkpYyzeyfZvFP6xGlsXvVgWJrcPi7wfL7wXJzcKwlONYaGtVnz5N49gHsfAF4ocKHxKEb'
        b'1E7AN7C9Yaiyxp1Ffp8Q51Pi/Bn8lO3oR+YPQzekbRjxK4JDRuu/swQdmoBtUxr3YY4rw0QT7PczOT8bgiTamOOOE8EttzT+jz1zIyFnbmw1fmKU9urQXZ5QAgfwYknB'
        b'wQCaGLytI+ERM/9znHxc3kyJt2YreZbcsKPZDtgDZMraitJSah6gIe9ypDYJvdxydcVjDRN67fs3LYk2nSrpel2H6LQo/h8kOXxFn+qvrMd/5vC7x7DZYtBQ2wno8QK2'
        b'MYl9nXYel04PA6cLeBxXQR8gjgNw89IvMCaY+KaKzvBObU9IQo9/4u2EV7lYwurkdqf3cRm3SV8A7DwkzoOEidbkKX3cRNeIPvCTnC/4/Xn18UhYNQNEgYYkq4CcPLGK'
        b'Uvr4HNHkLwB2HhKHnsQXBhgirYKxPYKxVlEyTiBMxQmEqQ+Jo0/HCQbnkEZySGdIFunMQ+rSTMjxCKuAnOG3ijLIe0lmkjTYfUhd+n4SNp+YHkHM4/PxFRvWWgUJPYIE'
        b'q2gGTuM7i6TB7kPq6jNxGu9gQ7FVENcjiLOK0nEa7xkkDXYfUlc/cxg9Mwk9mZSeTEpPJqHHwYG02eMcUX/X8YzRPa5jza5jLa5j+ziOrpjtH+OQoxvjBlKJQFCEMdMq'
        b'iO3Bn/h0ltIgSmkQpRS7+rz+ISI0hQ0qxctV3Ae+z3lUFAmRDunCWaQLs0g52H1IXdqLg9PMIWnm0jRzaZq5JI2NljCTtjOx26Fn7KQXinpcs82u2RbX7D5OsGt4H/jp'
        b'DiE5hxnIacqQHppIemgS6aBJpH8m6WeRX/asC0EWEbXrtLn5aHfMLNRG0B5wWs9Bu5Xw9Ii3eJGfL/PJeRfPoeddlJwSnpJbwleDEjslr8Qe/zko+SWOSrsSJ6U9OQ/S'
        b'zm93aBe0M5XcdkGXw7DTF7FYdnTWCyq5SscRZx/IeRFX29kVl2FnH9xonCuOcxsR507j3HGcYEScoN1N5WE7eW5PDyu46z0qHZQew8+TDKPFs92N1kTQ5TnsRAqRekle'
        b'HpV8pfAHchFiukTbhoeKyCs1KzlKr20OJV64LRh6CsZb6bMNlPgofbHrS861lPjZ0vnjWH9lAA4JUAZiN5CcUCkJ0tvhJ4NxXLAeYF8I9oUoxThGTL+H4u+hyjH4+xhb'
        b'PmE4JIycLSkJt4VE4JAIm38s9o+1+cdh/zibPxL7I2mOEuyTUF8U9kVRXzT2ResdsU+KfVK9A/bJsE+mjKMn/skNBjHbHEvkSh5Vg8T32qWtpEdXzg8RHsmqyUawp1fY'
        b'9/piuZi8VXCZRkEEYlaarVg3cARi2EGDoWdhNDiDlap6dYWYHJFTsPueFaxQjgOInI3zZHcLqteJa2tYyXk0yVbC6bUrXa2o1ql6HUv7qejlzphXmP91alV9fV1yTMya'
        b'NWvkqopyuUqnqa1T4H8x2npFvTaGfK9cq1FVPvLJlAp19Tr52pXV5G7m9NzZvdzMeTN7uVkZhb3c7NkLe7k5hQt6ufNmFc88x+nlswU79Jc7ZIdowOKf3EC0j4tRDUdr'
        b'PxjZsPvSDcPez6xkVtBctKIGjmkwRnrMQNZ61vMfxSk5DZz1WKYf+SboJn4DMzR0A6PkNjCrMWhpYJQ8JZ9Sw5gG1+FRvtxhVNr5PaJnSMx6PEWt55MLFEkJNbhUpT3r'
        b'J3Yww2loAKUDKi5c30E1eVx98RMDh/aUDnTgOn5QOpriafg5I9sYfnTMaPgDj1Pn0F5mlUkKNg8a8j2bT+xwSKYneeYWyBLj4yYOZhGlSi7OqiS6HbG2TlWhrlSrlNJR'
        b'NUDqeqIvwmi//0QRLblfqciyo6K+XqMu1z1Gh5RMopPLlKpKBQadAyxSJl5Tpa6oIrmr2XbCjGYrBzPPyLp9QsbF117qGmow9Kg24yK0475m5L1M7Cdkav/kO/zzNVce'
        b'G5svse8VDC+WmLcoquuqFL1O80lNZmg0tZpevrauWl2vscO92MvX1eEpQGPPkMtwWcnKg8B4cgZ4OIYlA0E8SI9OrXbd2X4eMNr9LQGwLwJWvhVh9EWNwa0hYZaQREMm'
        b'K62uJa88NaXdF0b0CCM6i9+VTb4vm2yWTbXIpuIAKjam3l5rHiyh+gYYucYZHU6HnQx8nIkxwpBqSLWK/IxzTWmdXPw743LO+ZzbXLM01SJNvV1okU4zR6ZZItPM4Wnm'
        b'oOlm0XTDDMOMB/iBea35hhnW4AjjMpOqo+ZwDRY0na2hkrPBJ4LNoXGW0Dhyv4MB//60k/O0WR8nMvU3Vr/E9PchNp6LhmyaDx77dASuq1OJy/DIqsCiTLU8g/1fVibX'
        b'nPtxdNoM+Ox/BJ1fDaGz/1aBrwOokfHoHDeEIE4/QdNHEPQkk+7yARTjPHA7ApeO014HhbaUHkXsdVCtrautUdU89sqC4ZX6hoxUf7ZSysPL3w2Oux8cZw5OsJBPak9Q'
        b'/x0GX1dQk2DdynKVhnSErQfEddWKCmKnqKgXV6sU2npxvEQunqdV0bmiXKeurpepa3CPaXCpyrIywuoK5XIdTkgSDM1laHMNrGX0tlmHgTeRg4E3kTvZrg5iRrF3+I9Y'
        b'O37w2Whz/rw6IjOz871qbUWVomaZSqyhQeUKYuZRyxo14lQKcZ2mdrWaGCyWryOBIzIjJo91KgxL0nEnanDTTFfUrKAmCtr6WizR09m55olmYtss3E9SKSWpjPSOjs68'
        b'7DxPFoQB0wTcO+Q86CiGYDglRk9VtY8gklSsVeMlzZYNeYxYrw4+Vfq4OtoySq7U1VQkl9nQ2ygWZd+7B1FeW0te3SyuHLzZoaNdoRzWDaOuUWtUGjy9rMbQS1FOzHAf'
        b's+3xg8ajbvn0+CLcCTumRssys8iLCltyFpBNAbQ7E3sL5kUGumRLs2R2YKWnA3oenUB7dRL8CDLUT4bNqBvdmAOb5ZHZMvL27j3R+WSHvFCGsOSSOIu/TAD1VDGP4+7C'
        b'57XyvGy0b42dJ0A70F13eIArH+9CjziidkEC3SuQzrLtFkTmy6JyZIX9GefwsUDkAJ+Fe9EBKv1tdEjS0nfp5PEz0CXAh3sYTEwTuqKjBgMXkUk5F+5C7ZPgvXloF9o3'
        b'L48BDgUMuj7GzfY+34PL0TOEIj7gQiMDT6Bn4CZ4eT77/KmJ8Kg2Uy7jwwtkLyEHXuIBD0ww7JqWyhrb7lLVaCPJ24A06Bbgb2DQxSB4q0htn/YLrpa8JOv8/j275lzJ'
        b'R7Gihv+5ciQpK2D+v/kTpoCXWu4Ui/ddFJ/5aPsvCxe89PUZ6b+y/rLzJV13hmzh1YI1Hz310eU/BXy74/h16W6H2A8aZvUtesXzV7eeijumdV0Q8W/ff1z/zeJccbMj'
        b'70Xfw2dfDkrbNPH6+pcZ5sKJ9BvlYz54r+/epIpXD3/RdO8Pd/44o+pt3f1PUv0m+uRGfQs9X/jT00dr16xM/vzZGaW/7n3Np26n4Zu2PSv/pv7swSdT3qrOy/6s/uNu'
        b'x+JD3fNyxs9reGdOySnt2Lcvnw2Z4vDepKy0WV+P/f3OWwc+9tjtHg5bUMu3X3foP/NOvNNo2fCqbt7ffvnNN79K+yhRXRiydnbcB3997XPr3gbel99y//BV1iGXaokH'
        b'3QoQok0u9A1JqNke8GQM7IBXcUft9mYPFV6Du+C5aBnaiZpiMtEuLqiPdJnJtUP6XNZk+DkFMsHmGJyAAbwYZgnur2tPodN0A2JFILwbnZ2Xi2NCGR28Ao/gtJdYa2KT'
        b'Au4mmxt59uhiDLDjcRzgpiXs3sRpdAdtzqE04Sd9mLQJ8ATshkZqyjwF7YI7nQf2VVKmDt1ZyYSXqW0KHx6HrdFySQG8FWUbkMAdXeWuQ1vQPrq5ggPvQhO7dcHjMcvQ'
        b'ZngMNc9m7yprQlvh8Wjbc7x8Bh5AO2B3KmTfPTUXt8oZsveRJZXDphh0fSVhUpyPWMxDN9HWgofkght0Bu0rynnEs3BXDMuyUeg5PjoDD6Mtq2Eze3na8cQVbIXJdl4T'
        b'Q967d8hZyUGH3Nf2CsTOc3IKZAzgrM7CjcERs+SfL6uw3ULK5M5nr2JD7aWUvkkZK3PycnLy5KhJmgN3FVDaouBuPnn3xeUsdI89Z3lh4jrUnA8vSu0AL4OBd2A7vAuv'
        b'oKsSwc+upSVO//Q3dF/Hi51fS4cuKesDbZhi1Fi61bPPttVTJAAePgec25x7AsebBRMsggk9gglW76ADtW21popTVWbvGIt3zLveife9E83eEyzeEwxcq8D7gEubS09Q'
        b'fHe6WZBkEST1CJKs3n6GCmNYa1V7FU7h439gbdtak7PZR2rxkQ6cvkxjt4mmmv2nWfyn9YimWQPD3w2U3Q+UdSq7J3atvF1iDsy0BGa+G5h3PzDPHFhgCSwwOFrDxp2d'
        b'dGLS8ZRTKQYuuXnTN8DiG4UBt1+wwc7qH2gg2zfHcg/mdnqbA2MtgbHkJVAy6hgyMMQ35VhCYjHIDxhjnGhK7LQ/NdkcEGcJiCOmuYEH1rWtM/myt6x1Ku/7xPf4xFtD'
        b'I4x2xCx3hjGytaD/arYks0hqEUl76McqDDRxLeL4+8L4HmG8VRJvSLeIxpIjkjOt4nATzzTvbMmJkuOLTy02i+NxOnIacyx1MCE+IaY1PT5y/CGvmYo0FtACv7L6BA05'
        b'8OisqQY/ZQ+JvaRt+GHGabjHv39gfMf0v3GXHml0/8F3SD3W+dmshecBKg0QsW+Iwf+A5QI1vOXbDP559DUi9hiQ9r/2gChXht1W+Z95lcgH74wGRNNZJGW74YSVnAje'
        b'xsCGgKMB0cSGRwk41drE+pG4x2YqMgzQDoOvo8PVkSiqaCQ0VhD4NQQt9oO3WoIqiZ3MOoJ7R1KmqKhirWhXqlbWatZRs55KnYYFgFrFsh+hZXmkNRkqxA065Vav0CxT'
        b'1Q+k/F7DmJoByxh24PcbxvQjdoKzVdrBusufZAJMbVXyHF2B7+xQ8o5f6dF62xs3tzwdBJKK7zE4cHHR/FlsYMCYm+AvgV/gAT1tVfGELfnsS8Hr0F6tqysHVK9l0G6A'
        b'LorhLh25qh51BE7OGQxes8eoiQkNa4Ijs0G5otkLZPMXYFhJbGoemfbipWt9sCAZHoVX1av372e0ZG/6em/I9sJnibVI/W/ufBjqvW2b77+4dqunbNm873i5adE23/P1'
        b'ioSU8l9aTk9tCmidIJ49JmJnwb2U9/4W9hRn7/bSs63v/cN8xJg0NTrkgPWu/6TfbX3w8Rf+SdeyFl+eb/dwjvHcrJaroo/2ffa2/Wtv/f7X29d/9HlL8keTd57Wvr0o'
        b'+NdzFs84H/jN0+M9Nv7tTzFJt/Ymleqc5oa87fvWlcycibK7jnO4C04fOPC2qbgh9/m23wY09QY/I9lqBw9vXpx3JPrvS1eM/Sj2O43p+Tu/04g655yt7Hlroy549evq'
        b'sKfMbs9udjjse+6Pwt+hrx5ytv52Ws9bGokbC4qex7jH9MhIV4WxvAyjhA4aGwWvPE1slPi1/ajYfT632htdfEguZqmGXb4jcUiSow2JbEEX0AnW2PZqFmSNmuwB3A7P'
        b'sC8EaR9Lc0EmdHDNcFiBNoewyAJexuDuNmtR3GWHThJchZ5ZY3txCM7sMGu33ITR/PnogRf2yOAJ4AyvctAFuLuEvnZkbig5gob0MbL4ibZ3hzhsYKFmF9pRzWIyDOtZ'
        b'WNaNGidSkxVoQFvLHkEyGx7TwTYKydKKH5K3ltdPQY1UnsrC1MOL8OLEQW3CQVfhTqY0xgGeQi3wWbbIRoyJGqOplQ0f2C2Hd9w5wXPRTmqBo+LCTpsBzjy0u98Amt5G'
        b'chNdorgOtgQvjJbm4fyO1mPKYRcWa9zhXq4mDR2WOP44COUIBl0FaztjZ5Nz17vZFkXbd4qP8m34SOkBAsOPTTk4xRwQbQmIJi8sCjDWH97AGqxYA0IMOVbfQItvNIYj'
        b'3sEHqtuqW2vaawgCCuwDPI84NrKz4nLV+apzy7uW3/dN6vFNsgaGHMs5mNORdzivMw2jn55AWXfY9cjbhVdl3TICZrIOZnXkHM7pDLdEpZgDU25X3A9M6wlMs4p83xXJ'
        b'74vkj+6P9Q1kdY8+7ZNNM+4LJT1CCT3s1zmjxycOf6gJc3HPolLLoiqzpMocrLYEq3t81QR5zPj/qHsTgKiue3/83tkAWYXBAYZ9H5YBBVwQUBRkH5TFPQIygCgCzoAo'
        b'4pLERBQXVIyoGEfFiEsU9z2ac7qkadrM0OmT8prWpFtemr6S1val9rX9n++5M8PMMLg17e/94+Rw7z3nnvs937N9zznf7/fTF3o+Vh86Vec7tTMTCtY8QMH5QEBp1kpi'
        b'yM/4eqVOVqnzV+r9lVovJfduZG+hzjeBvOjld8zlsIumqbe1P1Xnla73SicEEVlmbXeVZqFOItcTUcdNbg7Gwu3o0s3c53AkzgGxWHgSLwJhxqreIknFqbcwRsumgvEv'
        b'oB/9jSpJqz5lxnIx2sZYbzS2mZlcryWcULLmJzkk1nQSY3XCIoJdUyXvRVI7VMv4iie8sNongjD5pGqZgFbBkFNZfUOZYeNPPcSvWK6mm5ijNyyH3MpM2q/ccVurxLjP'
        b'bhWRC5UB6G9bmEe0bWboQ5O0HvAjneZUiEbZu/J4XG8ckcS14omPpEGnZvcJzo87XkgalTRBK+bQ8CyO0kxYUkMMGFgfZLijqu18yxNl1dI21oK9pmvuSE2Vac5ylbSN'
        b'1ZhLljbftD4yqw9pMnPGp2TbeEdYJc/8jSP0WM3iXnDUzvpAjqQwHXxtJHe0ioSK1gkmyXB1rZqwtXIFlala+cmBEa12EXT3MeIJGyETcjXoUbu6sa62srapjOsL6tqG'
        b'etpHhhxK1jdy5ytcnXJWv0NCKoAO2XMnryTS0sYj0GT8O+RS1qiqIrJZVRl9pdXTWOEWj+dBdW9j6JjJ6eRVaebrPGL0HjHDjN34SDIcdm3qE5/3G5BM1komkyaglyaQ'
        b'AdJ7ETsYKjtdcKKgP/RqrC50pj50Zndmd+avgqM1ssG4KX3r+tbdFN/1u0n+fSD8yOUD8m+Yz8YuZL9i2JBF7GMakt7rt4h95BvUk0eGI4lvp9PoQxLTTiFYax0gqwUl'
        b'bFKzY9eyoUbN7/lHhfSgQqBotefYEBnRKoiIIZXCi5CpwNewjMeNbSaL7sARx0WEYSrqd9x4NMU9WAq8C2UMulWDcZP61P2JV5PPbD6/uY/8eyD4lvMD8k8rUWjdFKML'
        b'ZjLshV0TKNZYo0s1zzAKgLPhJ3YwAgSGqTmqR3d1uzJwvUvIdTGRS+/BzZIaBm1CqiRQk9Gb2y+46qwNSdNJ0rRuaRx9Nm2z5zDc2KdhbP3XxipZy468kTWnvo1dRf/S'
        b'CiD0sylneCo48eXatYHtr7BGthuKISorqwNvUc6mUsDtcpLkj6FcIbx8H3pFD5A5OrM/Qec1Re81BWYvaVcrmU4lMq2b7F9ZJNa8SLyUVFXNswpTZVkYclttuzCJOq+p'
        b'eq+pxsKUDlDgmacUBr5pGFbJ0LWdZzWsBlq0K7OhbRVN0+BqWbSRay6+2HLWY41PORc0tBEKRoptZZ09MhwRFlStsWAB3MJJnNEMe9Twwxs/mx30C+pZ3Jd0fvqA32QY'
        b'LWaxg0FhvX79YVflA0EzyYjiOZt99HQ+mQ4LjaeXxjI4GQ//OOHmKZVXb1l5cNvIM6j7EsKlAZqkw6laSaTWLfJf2egEJs5DP0p7ZpursexAcAtJVLWsQaf2X0Sn0JxO'
        b'XtqzO0eNJX/htgUIXW0idMyBE2aEp88HJrf/FgOOrXEeDsIsxnnuwQaoalikQSOVSG15S7fNyBUG+l6elQCuQ/fC+G0wp5nSWb5F1WigSUSf4Y8MrVTCsOib41nLvmks'
        b'OpkyKpRKiymD3m+CAWqqoeA2h1tYxGhKdXRT17BwKOl9RSdJ0EtAQ3Y0b0x1Byd9T+PMqDrkvHGpNj2tKcFczZXEbK6mD16HosBuDa3Cg2372jSZ3N7x08fWb6AKx71Q'
        b'FcaqNr5Atambl1vO9HD/JnSdzTb7uIn98Qb2Oz5/BUAnUr36LPZzFJmxnz7oMBM+vP26heBRUdOsk8TqJbFat9inVMBy5qlrBrsms5eKGSvWC5+T9ZwGyJCLoqEphwjk'
        b'VeAlqUpp1ouEtqrDpthNKmV1c51FpdD73cCBVMb2TMeOj/pEKtOKZf/ODmXQL+p4Vo1yxTGrUfqgCxrZ60+fSLqeXneB/0SncrRR247PXdvQ0eK4jvb8NetYVtakaq5S'
        b'1q4l7HA3scP07CAMMYvGqGHh+KmDvoEPfeMGfOP6hf1qne90ve90suiRBvQk9wl10litOPaRb2BPbp+nzlcOEUHdkzVhsPTiILe14in/b1jNs8Fq3nOymq5YeHEvzGsn'
        b'Ih3XNTSoOGZ7mJg98vAY9Kfn5HaTzjdF75ti5LanTirXiuUct8N0vnH/l7gtssFt0QvNIGEvymw7CoViOWTB/Wno4nttdnHTovzzEU4ICScEVpyIfhFONJltGpmXs421'
        b'LunzplxK2yn14iOgvBvZZbNIR+P5Y8dX8wzcHRKRxkeYQ+ZnKmcdshS2RCM8HxK2rGioqwJ3AKsrauuVVeZbNQbNV1MNjCsr4/IllTDeVAnGRxdN+6M2mrpofJp5U1+n'
        b'852p953ZmfmJNEgT2hvVV6WTJuql4DL5VxGxfcrzK2+G6SJm6iNmAsZkZve0Qd/g7jmaJNhQ1vlO1ftO5R5MI0lXc92GLLJ808CtRtpTIJgSGduiuKNFW7YxPhjXkGOJ'
        b'5RT1rcaicdL7mzDaSg1MoTNlU09r96q+xPOpOsk0vWSa1m3aS9A77un01jwPvY0Nagt66f0d6EzHbK5nTJ0p34yoJrMUFiRZTONPHQ5qOL3WBZZt9CmEVyy3JJzevwet'
        b'L8CM0UcroWEdauhp6Gs6v1EnSdVLUrVuqd/UOk21/hlU1tY3WVBJ798HKj2MVFK/bT3Jezd3bda6hX8TlFU/kzIHOjtVcB7OzeYrePItixWkb2czuFbmPIobtwxUYKlp'
        b'e4w9yxgsUMiYye2lqVzNm4eSZ8teRMlXCjgRuHVUgTZabJCOsY3O2y6yGqH5zxonaaMTKsCWmnkSTBWVa+trAhsbWjhV54nxnNVEc2NjAwCtPOHFy4fYiWQ09Tc20iH7'
        b'Nc0V9U21rVVcc+V86Q3ZkZxqapvUQ/yqdY1W89mIPz1uTB2pEEqBRYUYnnwXKmSZoUI8fLrn7ZveOZ0aCuTofHL1Prlace7gBL/Omm6lprIv6/hqnX+ibkKSfkJSJ5/K'
        b'6Ia18Ox+P53XDL3XjKeI62eomA3VK4uzMklW/d1AqLquoQlww3yBAy6W2j3kvrq6qrKpdm1VGah1EOGorkLdVMYpeQwJyppVdar5wBHwi21m3Gzq80P2pkMiR6pVwakN'
        b'U80ietqgAq/f3IxWAQG4XFatgKAOggYI1kAAzU7VAgG4I6SLcdVrEIC/PlU7BLCeUO2CoBOCLggOQtADwdsQHKd0QnAKAjCBV/UDf/7VcOGjLKYNp5ICFk7auEYCQATq'
        b'CIGlxbRIABbTEIxjvOPbcx4FhGqdfAf9AtoVg35BJJAGtOcPesxrzxiUZpKr4AitU8AjZ3H7gu5MTYimRiuV3/TQOqfqnFP1zqnDPA/nScPM0wIwRk0zJY1iPP06swfd'
        b'YLTg7HQ9qZ2uJ7XTJWF7pskyOVrrFj0ongiWyQlgmJwAdskJ1CyZS5CidUsZ5rET5rLDQr5XEckHwsc0JMnGMS6SQWevYV6Ys/8w86IB0O29cwn8kexcNCyA5wqWZgnM'
        b'qNQ6B+ucg/XOwWBkGwd2t88IIKcQkt6UI0SQhusyYZgncE6ESkk0QdLBAycHZz+wdrYdTGCdC+HYyXYoYp3BQ5kxEPGco8BO3hDY88CO2hTYC+BqrMCJdZZBLobgGVmx'
        b'AJ5nIxDxoYg2gnEsvGsKnpYOXKIZA5GRZTYDJ6tMRc5TiYA5RuD2z8TaOROJcqzAnXVOBgpGBaKnRICEOjogERFwNSoQWVaPWUUJgRsvEHA24NQf0D6xVI134l1x1AIc'
        b'3cd77L14zRPxddsA5X/ngQqkpRE49T7KbxdUC5S8rfYGsEL+VkYpOC+0CVYoInF2o+LszIAMrePszYAMreMczIAMrePGmQEZWsc5mgEZWsc5mQEZWsc5mwEZWse50LgJ'
        b'JE4yKo6DKPQicd6j4txonA+Jk46K42AIfUmc36g4DobQn8QFjIrzoHGBJC5oVBwHLBhM4kJGxXmagQ5ax02gceEkLmJUnITGRZI42ag4LxoXReKiR8V507gYEhc7Ks6H'
        b'xslJXNyoOCmNiydxE0fF+dK4SSQuYVScH41LJHFJo+I44/nJ1Hh+ChjPK6eSMEg5DQznlclUqJ4+5Ap+5UpGnPZ+CoLAKAN2q0QGHEarZGA7RQ25KivqQcxcXmWwFm6q'
        b'pdqwRnMrCtFntCMGiytO7bTKUkHWoJZraWEFZwlmHobLQait4FzjKRsqm2Hf2JSzRW4NKmOGtU2c5gb3qlHLdXZ6QUmGIYfyMYycLW5yqg3mYhWBy6meCcmOU04294Ac'
        b'w33SWFaDkX6TqgoYYpFfhZr6BADiqBHXWpJTRV1dYDNsXdStBzHewrWyxcsWiyvY3ID14h/byCrhgADWLapxsHYZsTnfbt/MPmsN02S2KhlL0cdqVcNXMm38shFoULgT'
        b'WNwJLe5EFnd2Fnf2FncOFndGNx7MaCV1EutokdbJ4s7Z4s7FdMcnd64WcW4Wd+Mt7twt7jws7sQWd54WdxMs7iQWd14Wd94Wdz4Wd1KLO1+LOz+LO3+LuwDTHVlDlgWa'
        b'7lhyF2SRMth418bThDA2/rPkeQbzShPd6RNsFLYJNKG23lAKLduKWqQkaenxqqA+aMy3RJZvqZzIW8zKMOP9EbZNcIQ9yt8oaCoYeYuskK32QdXuTYVmudqRL9vw8tA0'
        b'zzKPNqEl1C3L7GwmLc6hjb/S1HK2W0HZqnm5oJ7Gpytxe4XqDMn/SRI3LI4aRJ8+TFKtiDlDbNkQr6zsSZj12ysqwOJ1xGiWuhKQyYacisgiqna1wTeAiFPb50C1+WW1'
        b'yiFhWXNVkwrAgDgPVUOuZcsr6leVmdyCqqB2VYDTpboMgRoCCmUDToiHXCy96w7ZlXH2GSTHxmZVY4O6inyCroztqEZjU8WQqGy1uoZ+ehV4ahWWVXF/qN9WZ+NrZWCr'
        b'QF6qXAG2BRSxvqKpWU2W56oqUM2rqAMsrfrqBkIxZWhtdW0l9X5CVuTcFGKKrljdNFKgIXFZXUNlRZ2lK3xCL1nlq2rIAl9URodwkg39W8bxxbfMiuVlZTA8G9IKyfVq'
        b'9dA4QqSqSQ0+XejewpAdqReokyGXdGPNcDVhp65qggjZOM46CYaGIdGqFkKC2gyvwMbWCrd+hkGPG+1H1s1Qq60SKzLpDm1LWdnPYY/lC9aoNgGnnOVsd5MmvadFK0/T'
        b'BsCPWpUt0/mU6X3KtOKyTyR+Bzft26Sp5I7mOwWgpy3osjch2HEgdRHRgLsQakK5C7RAuRsBsjvu0OtgAXln/BsQQh47DQYG01jDi4aH/sHUg4PhoeWfMBm8H2xMavhD'
        b'Qe9cjGmMxIVGwt8g031MPPyVGeh75B9CPxMaxqUypg6RnU45kXI8rRfWQuPjaLA3rzOjO4yw4tiMwzP6EnTSOL00DpAI0wYDgjUlh1oBdXDQ2+9YwOGAPrHOW673pm6w'
        b'uU37wajY8zF9MTcFNwXagNRuwSfSYE0iSWbylv0K+4l/jDa2RLtgiS52ic5/qd5/qdZr6SdiaXeGJrRPqBPL9WI4MCO/QUlQZ6smtDemX6STTNFLpmjd6E8yBRRjHF/S'
        b'xcV32LFdR3hZty6juwV3vgVChAmoKqWEGmTVrxpxNBzDYUQ0NRgcPIPFvpIIWrXV64n4ZCbWvLDvC7otfIp5CfI9+Yw5TFy4Jb4eGDitbmgacTxN4a5f2DG26vzLkOYF'
        b'pI14x7aE1RtNGUBwvwhhdJP/0ssQJrXBM3NoPSvKDJDZL0ra01D1xiTNH0gb8VUps4Gq909TRxvb/ZehLsiSuv9MD+Tg1tXNyw0+wag3ISDJYPJogE57Kul0ZcZlRE0H'
        b'YCHVSF6DRRDFTLIBxiYPLB55Vl1bBR80rEpI7iTBiEGkSbJQB0YZWBkVQy5rm+hfI4ZeFFWqj+Kg6aJemJ/al+FnJPBzwMTPxNGgNGP0lfRZC9LjSJD5whB5hMbvvsww'
        b'GW1JaoqFL34AdalabumV35rk2UWZGXEZmbNKXobkD16GZDnf3DvQUuPAXkSbm5kEarDLNfoysjIYlQdmUKAazjy2rqVivdrgWD6wvqqmAo5TXnRoICX53ssUaJJl94sy'
        b'dj+jXaxZmQyyaGBk8fwFi1+G4x++DIFJlgNrBJ1CGxpWwaqfc7KvCqxobGwAl4FkgdDMueV/0b5GyPr+y1A3Faj7k/Ho/IlricmR2otSwYFFqD56GSqmAxXBrMUIv5oM'
        b'WBU1VWa9p3HFejUYYQfOTc9RkAGu7oXoM7jS+sHL0Jdmow5H6KprqLEkKzAyryhzzgvj4RKyfvgy1KVbUseZsdcrY5saYsmfEVEtMDLzRcnikMZUH78MWRmWZPnZxKkI'
        b'jCx4SVZpX4amLEvB1oR2G8SZ/pMlYD34+TIMFBxWydzSorkvLIQRynQvQ2CuZX90p1MKXTQbvJq9RO3pX4aQAsvai7KeIGA1DsaNcB05q7AwL0eRVZK58MVmMsOY8eOX'
        b'IXAuEPhLE6d+b02g5TaCPHAOGWezqgjJ9XQFozZt8XLzhcH3ARQK+nVk8YKcOSWzCzMyYwKz5s+OCZxblFOQrigsSY8JhGLmZS6SxVD7wznQjlcY8hwrt4zCAjI4cNnN'
        b'SS/IyV/EXReXzjK/LSlKVxSnzy7JKaRpyRfotnNLrRpcTTTWVQAAHAew8uLt8T9ehsvzLTuM3Nhhgs3mWW5/hustFXTAqVCTLF68HQy8DIWLLHvMZOt2wO00yQPTR9wz'
        b'5ijmFJIazVBkweQLjfclhIEfvQyxS4HYcBOxkhIqFHI7YKTRKKG1NrzwwoX08aGXoabMato1IPJQ56ccLVUjZyDmS/kXb3wPX4a+5ZZd3I/jlnHmAJ8xgXC2Y0MUMOl3'
        b'AXWcjckIVeoGC2NnFwstVwvb0EaReRz14MhrY811tMi16RTEcke5jSljzFKZTkdU483vzOkqs/lUYzpJMf+PpDCdqVjudbM2OteT6UWc9xc4hzLJ8twqZOREzPYqRS6z'
        b'V30b6uAfQDyAOpjhOdCtY8BtULFQwXxus5MmohubwA2TTY1jTVWTcWe6VWpd6WaRVeQ1NZwffL2FAQPEjaB1ns2ChvlUrTS1T3zeuz/jarY2MlUrzX0g/pZ3Z8ZgaLQm'
        b'qy+jP/Sq7GbJ3aW60Fx9aK4J5Bm24mYMTky66tct6HHWe8kHxV5dBQ/FCQPihP4MfeIcnThLL87SirMsMKFtN3NYPYFJscHaoYSzcBzdtkGLa3TbNhq+NcDACm8a7N6e'
        b'oki5kLHuVyrxWLrflqc3ltrcNbZVL2U81U/JsyEB7IDbMHq2N+yNl9kqDBejggqL4grjIdF7hMKGdBypr4fSmAFpDLcfqhXLP5FIu2ftXde1rtP1KQw2WtuYldfJ/G6l'
        b'WQloNYD2OD2NMRZFSJuRbQPuuqp6UhQbG+s0ogVK4m9VkgRqmh+jl07SiicNSrw611DqFbIQWzqHdOeeagkOuVidvtCOQfvRSBeCctPeM+RsefgiMpy92BnEURXY8g6J'
        b'DOcuQu7YRUBPXQRw6EJhdoacLE5cRIYDFwE9PHGxOlpxND9ZERmOZOxHTmS40xAXyxMXVQDP0LhVoXAVwaMGEWPqBlrCY6puQ6+wVkzQwXHGl1ZIKiIH0AuEYILc2XeY'
        b'eXagZBn/8G4TOkjRsJDnXwK6fCR8TMN2hRWiSQogkaQBEEka4JCkvTgmis0czOEtZgC8RToFIEmnACTpHCDKSJphnsAzblgoksR/xZDgMQQkiYsZiMigOBcQRPIpgkg+'
        b'RRDJBwQRkUUaKLEfLbEfLTEJaRoOMwXs9od5rOe0YSF/QvJXDAkeQ9A+Z9jeguKZQPEsSvEsSvEscwgXrtipUOwZUOwZUOwZtNgj3xkUhwE2SwRAs0QAMksEBWYxV7UE'
        b'vnhSvnhSvpCQqlo+8yvmCSZDgqmQYCokmDoqQQIkSIIESZAgiSbwDe02YdEA+ogvoI/4AvqI77T2fKuCREJBoqAgUVCQKFoQ808Au8SUXWLKLhLSr4y0xWEe33MeOywU'
        b'+oNKKISPaUiaoxMjDekmrQ28AQ2Kp5KspKRqSPAYgvY8K2LygRgFRbxRUMQbBYd4Y66fGgv6qXGgnxoH+qlxVD/1eThv3nmAb/7AN3/gm38SIXVMzBwxCz3QFIj4AFRj'
        b'Csbxnb3hyjrglPtAB2FBwXLHtXg76nNudJLl4p3Rinw5OOXCe/hM1Aoh6k9eaKHlZ5zTOLhPvrmW31ZmMZ/HVIGGn9Vst1hIn/NHPRfR54JRz+2UQpKbfTuvmlWKttov'
        b'dlDakftxABBSzVPakyeONM6BXDmBzt9iZ6UjnY2chjysBrj8WnWTBWIpzzjZzeQmO9ZCXOSROxMhYBRQZhJCa0CwNFPDMa6eBHRna8ihTNlsUGV3AEuzirrapvVDwdbH'
        b'3UBPmbm2ldpoFS3nUZ12Yyb2xjyM9tGBZngCvjZyNYELbIGZNIybSQ3Ht0Eyephr+BNOj2VDtPT3MqebKuDiWIsKm7QZFxZvwsJiHcPYMBh6rtVMyst+eBt8eMNLfNiw'
        b'6Ex92Q+3j/1hk5wZQz/8fMZRRl7wVCEgBKTZpgsEhDFbCZUcd/ANtkVbGBAOM/S+cTpJvF4C89k3ZVtECKP0jWFdRCWYUesRA5VUKNzFN1jYjxhAEXlWJ4nTS2AOeb61'
        b'wopnrhXGYBS3XuiECgziGSvQ3AeYyfDOzGDUhums2lIpkLXhd2tkzDGreAPojpTEmy+T+VbxjtQIVGD5VOXaZFLZs6WISN4wLW81Zt7DRv6zNq5nuTFvBThtizXf51kN'
        b'aA3LR+A3Iqy4GWGZXNlQxaEKcJ7EKHCT0ZsslXvJshfgieiASEVv1Qy4mgkBtaiCNkWE9MbGqnql0YWYo9knuKRjWgbzK5TKUcsQWuUkYj/fzCyV6oVE923WSWboJWA+'
        b'Mb6U/cQnRBtarPMp0fuUaMUlgx7+eo8QTVPv+gGPeK1H/KA0XC+NBhvCAWmKVpoyKIVIcpOolSZSW6wSnU+p3qdUKy4ddBOTYfihW9SAW1TfdJ3bFL2bUfXEbcpT+iBo'
        b'J470wVE9b6u1859R/S4c+p23LQ7Q5VsP34DFONLr9q7vWq91C3yK7SlAIVuOYSATtDEZVitjG6MZT2G7nJE0S5h3X3EBf3S2FqJ7eTtdYZQ2FjgKqt7gEgf4NMQ2mft+'
        b'UMEKszXWVtGbGpoq6siwDUpt6jRyAZJDw+rGNECfUkNeWxitdBr361vTnd6T3aMwPaCckbFDfHXzahvLXyHN3TbPadQxvsEgFYZjHy7P/gwS6KTT9CSUJOslyVq3ZMP6'
        b'18V6/TtiIEe7zUiPMS0VuZVjPs9Q/6oiHt03slo0AvNNS8ZkaCe2JKqNQO1PmVHmZDIwuTEETlRU1/omkJ/OI1HvkdieMUgWO+u0gdPJTydJ0UtS2rNtPBoWsM4TQaI1'
        b'BCLWOR6uRgUiK/HXDkxxxgrcWecgSDcqILlMhyvrgBOTo0mAjs5HRxzXWgrJHXEgJ+MreHuMnGUy8Lt2+eic1EJcNqom/xFa5QEfc3GZ/OPRf/we4WI+QJ0pRUo7pb3S'
        b'QTlO6ah0UjqTKxelq9JNOb7HZbGgndcuJMKvOxF5hUQQFrbbAzJhu3u7d7Ud4ApSYdqOogdaCtP29LnnVkY54bzEhmGMncHgxDpuHI3jDE6s4xxpHGdwYh3nROM4gxPr'
        b'OGcaxxmcWMe50DjO4MQ6zpUrbzVfGUpK6kZTxtWS8a/KzXJw6WV3s4vdSGp3A1rheMI1lmIVutMrQCr0cOBwJfnUQ7sIgILaHSnWowvhqRvlqke7uN2zfUK7pN2r2lMp'
        b'2+oABjFddl0TzkdZgc5NhK+RWuArY0YhVHrSd+zPx45+h9AiH5V+gjKaDoiThpyg0xlNJ4bYuUNsoUw4xMuaNcTLyRziZRaTvyVDvNnZQ/xZWYohfkZe3hA/a9bcIX5O'
        b'MbnKLiLB7Ow5Q3xFIbmam0+SFBWSoDgTIhbnqQA/hbyRM1fmMsSblTXEy8hTLYB5lZdD8s4uGuLl5wzxFIVDvLn5Q7wi8rc4U7WEJpi9mCQoJcTkjJoJqIXEFgaEIXCC'
        b'v42IRNQJPkPWawLqAp9vwwW+wMGGU3vyRDDKzT1/k8DgAt9mnMkFPp1TzGgbmVPMHKULFM255A6/moovQOduwtsL5XgXvoduFOBd0fOyFZhzoD0Pt5NeL88hAd6eH5NT'
        b'MC+bdPpc8J2NzgiYNPyaK7rqgN6p/XSggEfdzC6v2XPkw0lHj+8/s/94l1f98fb7W/eyLkVeB9n15z4NLtgZlm//E2F2neBz5awfe3z04Cc8Jum8w/v7EmV86o16ETqd'
        b'4ojOxGTj19FhIybKeHybj95Vo07qJTzVs4XQdhC9V4h3EEpYxh4d4a1Du9Q0g3Dy4mnUgfbgPXmxaA/aY4fPKBjHCTy8bQ2+SFactvYLoQKttKDF5s3QqAIN/VI9iTGA'
        b's/sxYkl3jNYjnPyobFSo85mr95mrFc+1Unw2+iTjpmq7EYVt1WcwM9lwvUzN3w3A48+i6jJMSS0MBzlOCKvwY9kAcKT8jOAbQxKHFUe3g5y54JLCrzQZ2pD/XIxt723o'
        b'GHZcx9jG3ybYJtwm2mZHusg40kUEZAQSttuRUYkbh0QUOdat2oV2GzKKb3e06jYOtNvYj+o2DqO6hv0mB0O3sRlnDmFm2W1MGGtm3SZA0ZxE7tD1wPo8Cg4MfQW3x8bK'
        b'52XnluL2wuJIaLqlc1vQ1mzUtwpv5TN4d6Mj7qyY1jwdOtxt/Da+PvIu6UyFsfMNWAG5pANuJ612QSTevgBpXO1JxxQw6Ba66OicPJPiFdSX2zFODOM2HF7utHVSGNNM'
        b'IXQu4u1patRdCZgFHGIBPoH66AtfsQ4MaU7xgXUqp8HqIm5OxwdT8U3c0aYkvdoAiGUFX2DHLCq2W48OyKgdLHoNdafm5RTkxeBdMjLr32IZRwUPvxNcTnfS8H58A7dH'
        b'ZwPSAbluR8cS4uPR1vI8Jhhd46P3WvHZ5omQrpNZio/hvmgFeKvfVVBqBpQQKY+NxO1xUTkFLNMgsycfOY76udJ1LsLtebgjJz9OxKBr+KJIwnMpnEV7EsXKWlSN340G'
        b'tseKmLlzROg2b/IGdJSicOHreKs8mkVXuVqxY+zX8MbhW23NMFDhw/gc3lk8ioB5kXhPDN4+N9JEJrq60o5BPWj/uAUJ6HYztAp0V44PF5MMjhA6IpnIifhIM/TnzZtn'
        b'qz3w0bX4soBh0SGGSEmazOZ0eKMfHQhGh9B+MnbtipHj3QCF1kgSlkSSeu+IiSkozca7C41wEsYmwjK4l++E93hkNcPohm41peTRmJX4jWgZ3pFPSu2RxcdHcRe+R9HF'
        b'8AUJPmniMb6KbzOMYx4PvYXvo14OXa09bWIx4J7hDnSmJHL5lJGy048zTKGbXSOLL9AipWagXXg/mDKhK+hkK1OAzqBrlJgUdG4uqalLLWvD5+CraHsLvtwkYpylPHQo'
        b'CPXQrtKI3kLn1eQ5aeQx8yNzY0kTItMH950RDseuW0Aqdz++OY6REiLhTfwG3rEZvYnPRgN7CLuI0LmnODKSTAntcQoDr7i2iragMw4MOoNfawZLsxh0ar3jCsKR6/iq'
        b'Gt9Yg3a1qJzW4OsMI0ngo63odASlPgjdmYo7SPsv2IB2x8oJx4WMOzrARxfwbrSb9p7s6QIYBwIfNFbnn64IZyg8CD4Q56JeI6RTzR4At3sb7649tY7PqkH5yjOj5UBX'
        b'agOKd3vzd1tnfpTl/p6D9uPt1yq3/X3H35kJeatf189nJ5ZUnNF/enuBn1tR+IS/K13PLv3s0fz3i7SpX/3lvzeu3hb3myPeTl+Up9euir+Of9Py0SfCmsTQjCk/D/7d'
        b'5z+Ybhf9w49OV3Z8vNv+3MJDUd+Z5znx2BZp9/eO3Ow95zB/Zmno/l9v+/R0kvr2DOGT2i1zp+esWvv5xN9vaf++sOmG+JMqt4abX2TfS7jPD8q7Mvt/+l9VRF19Z9/K'
        b'tl8NLLv05Zf/lRby1h//S9z3m74dC1I+m1bD8z16pf230R+ePX8meb5o3aV3v1/a8vhH/LjPLr+dvPgP/adX1G658esB1m7zJ7ua7/7nJe3KP+g/6t/214UFkS38I28c'
        b'va7aUDOnet1ff+9w6PMVJ5pWBdxtUk658F+tGe8MVf5gyqm7aT/p2BnmuPHLpRGFX3j/+U819mun8jZMzE+Yd+y2irlef+qxa2qDxnt68idffE9U7+55y+6R4l7opgvZ'
        b'b4Ts1ufnuPzty9sTvu1fdMT+/tbabSm/S7gz7k+RVzoDluoKf7Hls/0bXSKvd34wrmTv5yWanYnB90J6J/7gJ9k1GSfKf/7H0E1DP8qc5brhdr79P8Ki5zpecN/01ZWW'
        b'v+6JW33+Z+ID/U+Sqi5vCPffzDg+1rw37YYs5DGIdkvJOPweJ5j0k75uIZjUol1UMHFjAkhHRrvjFLHZ7hUCxhFd5OFTSWg3BdHwRdvFHM5GFu5vNsfZiBFTyQVdxq/n'
        b'uuA+1NHi4jxOha+p8fUmZxEjXsMvTgh/7EF7bog0Lxvf5GDU2HT8xlIK8BGDTxThjnyyQuMzfPweSwab99ARdR0FK1mF7qJ9hDAi08lweza65AKkXeDhkwsIadTRwRU/'
        b'/BbqiFzuuhZfb8TXmslXHSW8FYviOYy2Y8ujDZAt4eiMCB3mxeLT+CAF1kOnVswj8mFMlN9smZwOnAzjFShYJkJ9j2FTGXXm++alOsgLRAxvPZuCz0zhkOnetc8lvXoH'
        b'GYMIyYJpbD2ZZC6hbejUY+hjmxfj7XnoUhgZ38h7y9i4GrSdQp/gQ7xg9XTBWqc1zfiGK+l8O13tncfhfte1pJfj6y1rCOUFAhGprP0lHIrLCXQmJzoW78qfyDLr0Rui'
        b'RSw+Xz6OK9d+fC0Eg6jYl43eJQLERnZOJu6j+Hz4hgzdRCe9UEchSXE+uwCRqVmeW8BnfNA1QcssdJcWf3KGGFLsJtM24T867WXHOM7k4bci8E2uTregXtQJgC4w0IQm'
        b'G8aZCfkC5xB03IBWQybwi6gjDhqXkMGn54rKecHVqRzQzC3UtYjEGUZKdDFKyDgW8vAB1IXvUni+VUSi2EY+0JtCuI92F4IIURBL5HPCuQB8SoCvoCN4CwfjslsynqTU'
        b'tNKU0EoFjAvq42eg7maKZui5DO+kIIi78llmqliUw5Og7jVcQe7OFdjFQUFI5or8QjIn7CGJfHCPYE2ZF63TRNS9DHXMLykcmbtcivkFJeg8lwORSvARwi15LJF68vAu'
        b'tItP2uEOHj6N7stpB5Kht+KJ6H44vDA3JocIMoz9VN5ywpsdFLmHjSU10cFFoXZg+tli+EwOaZdRkUL8KtofSHEDHfFeX5JNL0mkiEHb4wxzhpDw44ZQWERaLnBjfosP'
        b'R0zHUhMIpzu6wMcd0lWPpwDv7/H4qMOVWx5VovuwQoLVEdqO9sRZHhlGk9lrV8g4dEyIbj0GV7yo25s0aOPL6D63vjK9Teaq9nyZiMln7NBlIlnceSynvXsZiYC5bg9Z'
        b'bZECZhfAVBSXhy9MIEXYzR1OZqFLdmiPSE6HJVHaeq51IICBvGd4R8RMIMPA/aqif7kDJqP5qLUDJnpU52m1WOHO6OgaqpzTuxiu82O8gjtbNRF9UzgnW7DTnMPtNI+g'
        b'ez+S+IODYc7BGqTIZul+8hydT5beB1SoHklgSTO+gKVA4nEPAxIGAhL6s67mP3B/EPTAXZ+Y8aBKF5CvD8h/eYzxRxI/8GGfS74R0Zc0EBCv9Vf0K6+ufpCjn6zQ+ldq'
        b'iyo7s8C//SsP/eQDfvK+lvNtN2fdnHdzlj5uxgOJzi9H75fTOeeRt1+P30PvqAHvqL7JOu9Jeu9JnaJByJsdn8eVa+aDyTpzx2UBYcdaD7f2RfRP0gVM1gdM7nR6JJEe'
        b'bN3Xuretq61TMOgh6V6rqenZrPWQkx/JojtKW7zA8FtUZviFlet8KvQ+FVpxxSMP74ceoQMeoZpSnUe03gMcBI3PZwnD8rgrSkauzidP75OnFec98g0+lns4V7NB55ug'
        b'903odBj08AVeZLAaSa9v3/K+NX3L9UETb3prg2aRH6VgMCxaM18zv6/k4qKzi/rX62LT9bHp2tj0YT4bPhtQQ6QZgBpCQtCUIyGZ6QI0MVwZ+luubuCKog3LeLBWF1ag'
        b'81HofRRaseKRhz/QOJfVTP/x5HxtCPwMXJuuC1PofAr1PoVaceEjjyDNUq3HRPIjWUfGnG490Xq8rbdNHzHlYUTqQESqLmKGPmJGZ4ZeHKoVhz6KiKaXjwLCqBFwcGSf'
        b'VB+cRK5dTQbFXIzRtNdgmOwXdGzx4cWHlvYspYlCInqTe9MehkwZCJmiC5mmD5kGqQMHAyNoakMeBmvh8AjOfjk0jsvSGmbeeF49GBDEERWuCdU0E6q1ERUPsr6V/zBj'
        b'yUDGEu3Scl1GhT6jQhe8XB+8HEjudDVou3E7DuMNTveMJvoCOK1SlUD8FNjYcqysaDJZ24vUlSuqVlc9LyqU2YgAXb/c8J9pXHjmgHADti8eMNz2xdeGPYxVfixL3Xj9'
        b'G8Jvah+E4mOddkhl7rmkO/Jf2EwIPBRQzo912G7JPuMp+9cWuugvai7Z+5TDfdvfe2Kp+x4JCtImXzlcAQINyEeBkaqqCmVsQ33detkLm2JzhiRDjmUGo6yyWuWLEfo3'
        b'SzOC2C0GimNsWXrVqkcKYU71i2vFf/spWue2CYX9YzNzQv8Sat8F1l0mo82Xo4jTHAEXGM1NDdXVL0YVX2BRz3HUKqi5KZZkFAj+QEYs0YBSaqD/TzBO5f3CDVEEBI5Y'
        b'EkRRS4LaaoPpwGqwDCG1WlUP/o+U/yQLncrMRsgXI9MByHQ3KlFwVl9g5VADAK0m89B/gnNhL9zgnICkEYuQCEuEVyPiGWeJZk6YGV0jp9+g0gT6cAY/d3y6aQsH9FbA'
        b'vhtZumnLjNq0ZUdtzDKbWMOmrc24FzvrEClsn9qvBbrZbSQZ9WsGVIOthdVZzEaegw06RsMWE8rYTTwD1TbjLECKm1kbIMXwn8Ecpop6/rI0ilAHqlc0NNcpQeGEDLC1'
        b'1bVghl9TAaYUNvNqMjhaC5xdV1UBBlyBGdQVEDS8BhUoonAm/zAN15I+zNkq1aptZqauoojJ5eUlquYqMr3Xcr0/alVDfVMDGfUrV0UF1tUuV1WQzMHEbW1FbR30PJuZ'
        b'gcVW06hRjrxm1EbnUIw507n1ZhZpNnPjjOpMBM6pqFMTCkfjB8N/Fs3F1LnMmgtfUau/8TWrhhXtubfmHvlw6tHj+4M62JwvRK95T13ChJ/ms6frZCxd085CxxZy668J'
        b'K9B2y9VX+kbSKd2MndKggCOorqlqag216JXqyroyysARDQxIRddJcIBC10mBjG9gzwyt2PwcyaA9aSmi0bOscqP9i+oB6DE81/fcyIvqasYAOv5KIMu6g3hkHXyjh0b7'
        b'HWTMGZcpfNuoDJugh/INkOJCeizEGs5SAT3B6hz0XwAn/rxnqSnkLh0f8TSt3WX4vKExwOHO9vyo3Bh0toQ7aYAHhflw0IHOoe2O0/AlWW0P3sOqZ5Bctsbf4U5Pb2Wf'
        b'3z+xY2YAK9rxl7zuT33fFH+naqeT0znviv8NnxP+pkLjX6JTvLMu/KbLm+WiH05gIpY42pWdlvHpRoJ7BrphYx/BCZ3Ps95HwGfSKfCwOGqTYxTexeESc7uTLsU8JgBd'
        b'EeCL+NZ8mgi/Vq0ybjeYGju+gy7RBr92/fOcrpIuoH6uLqA2dIEUQxdQBTJesEj2zGc1pfqwVO7yE/8obXSuzj9P75+n9cobDI/SKPuSjq/qXdWZ0VXYSf5ZHLzSDjP+'
        b'aQsbw8HriN9x1XefrwsRen2gC61ljMC3a0gf8oZO84zgG4O7jYBC8ugpRWJtel5eoQM6EcsyAlcWncZ9y2iEKz6SmBetwJqFEJPAoiuNjrWneUd5ajh1CcB2Rz5MOfrq'
        b'/uNL/uN12a6Jb1x64+SED74o/+/ynEpFBe8PXqu8VnoVd/8mXpjQeJ1hHqY5DB+dyTH3GeY45o7cTexrnWCbrbTii7mKHxTYDy8OtB8fPczYCMT88ZOGmacG9kxQWJ9S'
        b'K0nQjvhwN5I8ZiuwJFn1AbSBMYh1hVpvMLTSJaTOHaBWxw6+sep+jRlLI5HKZDwq2wiIdMP7N0o3ow7SbY2ZZJLdc/xjvho2sAc/+u6RD2W/TTz66vbj+4+TQY8VvTVx'
        b'Uvz56q1fkQk3gWn4T8G3F54lEy6oWebhUxNM26pT0PHn2ZMVpMt4ZjXLo6ORmRa2tU4FVb+mLdDbUKkzgxgvqU0NbGM7sjERj7QjMyWOsT8YBK1oFWOYfjePNf1+o3Pw'
        b'U1rQ/zPpeKt1+7ElpAkUJbXaR558NXDbef6T39WDnBb0xsTuVxP8GJf7vPk/dTSqvVuJYJzau/VOFKfvTivd0VDpc0il+xpsZJ9f3npK7qEWAlZm0L+6cgFC5f965ZpI'
        b'shwcUr8U8NUgyXzg3EklcNAhS/a+/OiuML/2mNPCB5MCl+16xJZefPO39tWP6lgm6M+ie4pUIv6AxsLMGYW4IwaOhQQzWRYfR9fw6bzHVOfjCjonNo0fTx080DVnw/iB'
        b'zsbR863x6B37aNSJT9JD3FgRY4/v8NDeSajXRiujViij9jup+QltZSFcK/tTPrQyaoLy0HfygO9kDrPJEvHo+VvfU74aYdH68v4trU8FMr6FQpivsb5vQxP0tKkQBgqp'
        b'LtRvvlElVdTuQRVWTYqp7d7tPu127dJ2PlkT+Lb7tftX+5qUxZz/5cpiNc+jLJai4HSQ9qEzuDMPvYmuG5SYQIGJTeMUmOAML9ItzVGFr+FrrqCqQnVo3ObhV1EvD99G'
        b'fSqqOOaCOyKoGk02aXuF6PzTdGmISP4m6sCn1zmia2hbiUxENZZc0dEENSjBMAVhuJNBOxPCqXoPulcAqtzNhPIWGT7GoL1L0B6qWIWP4h601xFfJ3NY2iZ8jUHH0dY8'
        b'LuodN3xSDRYP6L4bbmfQmyTxBS5Kg3aWOUK7TENn8UUGdeP7qIuKnqsbVqgpDDA+ifcxaAfpjfupns2H9iJGPJ/MtoHldc5zJ3FqbYRfZ5pAvUhAdbXewCcZ9Fbuao6p'
        b'h9CREK40+BRhHZQHH0NHm+HcFp1Ax9dQZlnxCPc3qfDV4uxoqnewHW+nzEKdqNth48ZELuOdM9QJM9AbuDMhXsCwhB94CxlArjTHc5+6HE7WVSNac0Lcb8SHmDd3AT6Q'
        b'kFtsx5TibhG+lof3NUOfbCAfu5NALiauxmeYie4r6NNGdHQNBoObOLx1DhNXUVf39T/+8Y+37YTML6Wk8DPLnX6a6sg0z4KvvoH2V+aZPoPbs2NgUbkrLrc0Em8n7aE4'
        b'Uob3LKhBR7JzCmBxV0CaCLpeBGUT1Tu/kpHXPJNks6h1PGj0LhhJhE4FyaA9ASfiCg08MlcEhJZ0Dt1xwpcXoUPN5cDaA/jNWGfywl5ntCXeXoi3lOK3RXh3ifMcdx/7'
        b'lCJ0B93Db+OLmTXrHKola8bhu6IWe7TDodAJ9ePXcW88vrdBFoDbp8vxYRHe6Y0OzpahK2mJ+JAX6kadDs0g86/DJ9E9YaAjfhW/6sxMtOej/lJ0eTE+IELb8TZ0IApt'
        b'xffwHrS7RFq7CfXhLVJ0b2WwFN1AO9Eb6Hr1BryVPzGSkLErAF/K8CjAt1PoQESbWkSAD5uY0SBg3MpT9+VtYmiLSbTD23BHATo/F7fnkMLHVaLX8fa5VKHTpHCG3s1W'
        b'FBTQdfsFfMOxcrovzbDDPpuJrAxhyZoxF6VXMM1zycPJqB3tE5ICHHJgAp3Ixfxl6ELUKrQPnce38XF2InoNn5qeQCpkfzmZnc7jw6UR+ORiQvMWzxL0WhVqr8EafNNu'
        b'Bbrrth5vX9icSPtjVYUFlQYSs2Nzhe6eoJCNzsjID3rWubYUB3xDvLhExtIxJqKeatF1kIkO786JIWMFqVwJ7gmwF8QjTRJViPSbjU7kxeYWFGfTnYMc0OeMlpbMpyrg'
        b'xhZP3ozJzZfnxEaRxrFD5lQrKG0GhWgf9Da693yqevGJDgw6EkUoo+PPNnS9Ih3vBo1FluGh3ezs3KpmgCwvwEcrovGVoGzCtJ0FXNuPy82JLeKUbEfpbWajsyWN0O3n'
        b'FsXO5zHrS1zXt+H9zaXcULYN9XOKkzn43dx5BpVbwx5Ndn4hLax8nv1afH1edm6BIiZWQRV6oaeZtDXp2Ix3Fo1Hp0LwZVr9l7L4zMyN4Oq/vC5VVEIETqoy64yP2OVx'
        b'ii58xh7dFuN+HmkTpO6bQZNSig7hm8WFsgK0qzAnJqd0gQ0lYoa09rNoC6nXfXjn0kB0Dt1EvdlB6H52UAK6KGDwZfT6bPyqOzokRzdoJU8lA9Q9MmJecXWwx5dd8ZWm'
        b'Nc3z8RGWEav5hU3VdIBDHeg+ulpcmQiDFZ+McOcZfF6JDjSDJ5U81ao8WSzdsVLE5KyxL420tox/JdAevRaOtlJNU3SSdJvXi9GuEryrlPQLIT6Ht0Sx6DBqx2c45d3j'
        b'6NUwElx0XOvCko+9BQPKq2o6Ia0KWYA78snTfLRvKoN3o0vJlHW1YYTXIypEjugs2r2Yhy/IgzhlZFB0uU+a2W30lpnC2xH/lVxzuuFBBprLsjyT6hg6uJJOTPPwWTKL'
        b'BuLXQRNLyAj8WXSizr0ZtLh88F28n2sd0TJ0VsA44fbNbnzSpzY2g+YR6hPXRoPuM2yOxeSA7hNkEj1FyISjLcJqdAxfb6YaVleT0Mm8Ecgg+8kzcDePjJqncB9lf8n0'
        b'5dEmdSQnUobjNXzXIryNUoj24B3ZebMiSIsg9AlYInq+iTubYRWK+/AtlirM3YxVUM0r0Ss8T3wrgk6sm5jVuINhqHqaYDKLzhSTyQe4EZ+Gz+SRGexiLI0iRT45I5nG'
        b'LMZvJeKO1jQuIo1F55biw82BQEXv1AgjjaR5osMO0H+FTBDaL3TAJ/Npd8d30OvoIhlP2knn3F6oILPJ9rjRHBIyCvSqHSkDvsvN6a/hq/gW6AvKyPjjkB8+jYdOvbKY'
        b'xq2oqIfZPhmUdq/YMTz8LhvLorO1u37xO1YdSqbKks90u+bnNQzNdFs2I/7Xu4K8POwdJuY8yX6S/6M5Z59EnP1Z69Kgb2fPVwa76J4UXdv2qTav5E9feEj+EDKd/fJL'
        b'udQz7ydffvTDKQk/JzebWzc7OPH3bdo+Rxzw4760hw6LPj8THj7XdVIt6nv/g66M3x1J2TZJd+VQ7o0JQerH730Q/L/aFfL/0IYfXMmLxu4r/zYw/dDFhd9dV3jRJ7/m'
        b'O4PrurMkcwtvxvjfn/b32EmySYfeT/zo1sdNhwPibmVMSOi7d7jQh3eQl1Di9EDn0FU7T79nwfgM17DGEn+3zQJFec2icb/NSf/21rcyzw32elYHH5Ql7D/hPm/8+Ksf'
        b'lsZtm/Z4keJy/3feeS1z16EvkgWnStD6aUcrFadjDpZcrwhqLjz6P3/J+NWfH2yrHAzI+cR74/pywd9FJ0u36bdO/aFI8o/prTvePbRn2eGP3B9GBN8OOolFJ3xUX0ba'
        b'barT/foj1+ahnbHVZ1YF/3lF0d/uF9S9en/XxbAj13seFt1ZdObon37WsXTJDr/Pv/+n4xfc//NnfZdv/CysIfruje1lf/hqxW82Lfjpxl/JW6YMH+1zPHrk7yd/ULK/'
        b'9Z6dX9VF19dbozIXLPnZ5J9//ddJt7fWf9Y3967nd2p7//jX1L2/yEiJ3uh/+sNpde+nD5Rk9v71xLtzHuz68PtXfjWrMHlBrP73r214V8f/qD7i+/WBQz/4af+9PzeG'
        b'ro88/ne3pWccP7nWnLfbrn6gqCr2T9elax/6r+1N/nH9D6de2LbD5aJvWnr470rw/UmPggqPuSz4n8lfD/7X15v3vvvd9W9lnT/4YfGt3+wWH93/yp29P8i75Pf292/F'
        b'lL1Z0X9kzYS77zOrflT64zf9O95SpxR2fOm3e/V7Fz//3pNfXZFtd3yk/SL2ve8kRMRUhrWeKe0/eNyxu1S4MuR3O7Q1MZtP634z97tfCcumdZX9wW/7H2QfblSkzV5/'
        b'bH/Z8bYH37v4/vtfOV8ZPvodaX1v2W+nruzb4Cjf/fvOb2+5svnjOt+P38df8aMfrWP9fGeMux/3tf2xz3919M9LOjpWrOn+4sf3N3fH3rsRNv9wSb97aXXlx86/XveL'
        b'GKdNSV8d2LQj8Kh4V797wLGfHPveH35Z88oBpwNv/+EPZ6q+fbF3+I8Bf2yKe284SxbGqY0exOeczBRT7RhHR9QPiqloXxrVsEVv4TcE0/G+PKMqMbq9kEbMWIf3NGWa'
        b'DZ/78WtUX1Kwdh2nvmzSXSbj0bugv1zeQHVhyUdfizQaHgjJrHeTiGTXeGtxv4Jqd2asmWY+rnujGzCss/gMpwb7+uR1JMOTLeaDuge6aMga3Q8y6VYLGMdcdI8qV6/L'
        b'5BRX0btro6umUvKEjGglzx+dRldovjK8QxQdJSd/YhjGISF+ERlxyOLqDtUAnorbedGl9nKY8mLImIp282LxrghOs/mCCz6bB+IwulBj0A91nc+vw1syqeItPoxOeoJC'
        b'LEhVhZxUjW/hcyB+i5iAPAGR5u6EUfKK0cXSaGGpgQgROs9LQK/H0ahlMQXR6A7ewqlXc7rV7+Q+BnuZGKRRq9Eu+zXOZGmzB19Wg42FDXVnfE2E3sPdqINqhMrQRXQg'
        b'2nhEg46iPdwxjXsOH2ki59LmER+5Ks94KoSv5RTSyh6Pt/HRzpIkWtn4eEQ8ImLcjrhYfIiM2WRYz7NjXAv5KyYto1nw8JuLogtjyITUQaMcG4hI8x4P30Dn8Am6XSKt'
        b'RLvMRKATuIvKQPhCLd2kCXLHO/Ly0dGRyQ7vnMM13r3yOqpp3xxLmtRtc037ya20Tsli756KsP7APIOuMmgqT0ZvPI6FSCLatdre4zGp3ZbgO6B5u3Aj1fVG1yXzrfW8'
        b'0V102qDrHY96H8N2Dbs4iUhPmlozDWQL9eMmfJmjfwc+g29Hy2W50SmkrW2n86Ar3sJvQIdDOX37ftzbQkR5wjlafEekcarn4SO+PNoFw9CbG3FH8vSRuXlxGm2uDU1E'
        b'IOgoRvfMRBjUL6J5zsIX51uKMK8lEhFmBT5AlaflRADeZUOGwQe8DEKMmwNtP7gTdXkT2sy1vCdEtuA3Be54C+k2sF4S4JPzrTmcvuSpm/Dk86epCYNDxvJZ+Gpefg4Z'
        b'dorYKNSDO2hHcHslMS8mkgwdeURsYtEtdI63XpIui/zXKTD/ewM1uHQw10QYjV1rpUQ95GqFTsc5azHt7FnF0m3FzSJu87okiAkM7Wl7GBA3EBDXb3fTXReQog9IAcVh'
        b'/64Nw8y48UvYQUmIpo07FvvEP1Iry/+g6aMNOtlinf8Svf8SrdeSR5H5WnHYYGhkb74+NKl/ef+a/uX60GmdBYNhMb1L+4P7J/YH68OSOhWDktA+lwHJZK1kMok6XXai'
        b'TBc2WR82eZjPeE0ZTM7W5r+iTYbfYNikfuVAWLI2LPnmJu280oEZpdoZpfTr2R+k6WSLdP6L9f6LtV6LH3l4d2d1Z2nmHCrsKRzwiNZ6RBt0stfqwjJ1PnP0PnO04jmD'
        b'foHdxZoJvb46P7neT/7QL2nAL6m/UueXrPdL7hw36DGhO0rrEUp+gwEyAzf4uoBEfUBif5E+YGpnNuflY+rejV0bNWsGJJFaSSSlZ662+BWd7BWd/zK9/zKt17JBiV/X'
        b'5r5wfVSqVgK/B5HflSO5dl6JblapflYpeUJfU2jnLdDPK9fJynX+FXr/Cq1XxSMPv87k7po+YZ9S08a5gxhmnMfHcF+eAjrcZl8e5rF+mexXfF7AHHCTRsJhhuc9B9Sj'
        b'4ybrxNGdCk3WoDRJK03qr9dJM/XSTDgIL2fp15fp/Mv0/mVar7JhPjwEJ23xWglpATrJVL1k6jAj8IwZlMV3uwwGh3bbdds9kkWT66C4h0FJA0FJuqAp+qApD4NSB4JS'
        b'dUEz9EEzOl0GfYKOxR6OPRTXE9dpN+gT1h2tqdH5yPU+cnJLNelb9qZ0pWhCOE16Wklm9UNTbNJ5hOs9wvvczSqySOdTrPcp1oqLH3lICF2guz/icEUzad+mzk20THN0'
        b'/ll6/yytF/hJ7d7QvaEv8WaGNiBdF5CuD0gfkKRrJek0YZ7OP1/vn6/1yn9+FXFJVxr4eX2F1dScbjjRoAufog+fwj0Z5HqKwJNcBoQe23x4c1/L+Q0PBN9y7t6sC1Do'
        b'AxTkG96r2E+CY7SxS7TLqvTLanWxtbrglfrglVrflaQGSCypAe+AYy6HXbQRS3ReS/VeAMVEfefB4fQUTbImuW/FTb4uJEUfkkIfDQZEd7f1ZfcV3GQfhH4rWhug4L7W'
        b'mU0aq2dA52KNfV+IzlOu9wS0J0gf072xb6HBMiB7kLa2FX32Oo+Jeo+JkCUUIOLYxsMbD23u2Uyz8Q7p9tFk9yl13gl6b2pz8Qpnc7FE57NU77NUK176iKuMnmRNS29b'
        b'f4k2KffmK4PSINIhZ/Rl9S/7is96AVg1hJ0CwkiSNEXrEUF+XD/V+aTqfVK14tRH4NI0BGp4Dkt9mkZ3ZnRmPJL6dyd0N/W09iWQf036uFm66Nn66NlgW+H1UJY8IEu+'
        b'OVUny9DLMsinfKEvQNhJXS16daVqMgc8ZFoPGQCKZQz6hWiWH1rSOadzziNpcM8MvTSOfMErott1UBw6zPfwdh9mjMEjcHw7LIRbEeMX2p01bAfX9oxPUI9vt++wA9yN'
        b'Y7wDexy7HYcd4c7JGOcMdy7krZ7C7sJhV7hzY0Ki9MFTtMFThsfDvTvjG9w9edgDrsWMX7TWN7vf5YGdNi5b6zv/gwUf5H497AlxExif4G6vYQlcezHSgJ647rhhb7jz'
        b'YXz8u8XDUrj25a794Nqfuw6A60AmOFYjHQ6C62BGFnveSR85Sxs5azgEnoRyNISR607hcAx5T+8d89A7fsA7vl+s856s955sZnEy6Bev9SMR/eseeOn8cvV+uZ1zBt0m'
        b'HBy3b1x3kiZS5xat53w8xkyitgiaDJ2bbNBN3OX00C1kwHCv51xFSnw7ncyOrAK4I6tjsOdPvRNFQxBHLQ6q1pn0ac1c9ryIucE3NC+D0DPKaMGWTdMTk2O5sabgKDhj'
        b'E7OWlgzzgli2mFoa/P8z/MasI+Bg/ZpDuiPzvqNLujdfxlJ/TYrn0P1j28Hxj+jfqvsHWro/4dnQ0k2vbqpSBVZW1NVRDF2wHDBgCpPWUAvNoKLOAlqXAyxSKjnEuorA'
        b'+qqWUZlyOuuR5eVzVzfl1FeTlri8rqFylUxugEE26v02q6uqm+tA+XZ9Q3NgS0U91XlV1q6tVY7WjbUgoraeJqymHpUN7uaq1JwPOg5FLxAAZAJrlerRmrOjHiQ3Vqgq'
        b'VgeCI+jkwByqf0t6sroWoIbJd0AXtyKwslnd1LCay9ZUtBxlebkMQCrGVFkm/DHyAy5r6wPXTpFPIqyYRdjYAsxsWlHRZKJ2RCvaZo6GslH8Y2q2wOkekwwADdmCRUZv'
        b'fjWqhuZGiltmM0dS9Kbayua6ChWnXa1urKo0+bdWB0aCD9MYwgLyWQoZsL6R3FY1VcpltBLG0K4GhjZVGevFUO/UKqWe0NxMGEnyh1a33lj7ygbqS7ARkLNt5WlRAaPr'
        b'9Jl6GOMUzZxxOFnsduKd6GCe2QE22obauSNsuoI+HYA6HY0OFzbaWbtc6GxsBjxdsDvuEHLneoH2fDg9vL0mHnf5+Gd7hK3ZiC8WoTfQu7NR15JZOU3oHPgAsU9VxPhl'
        b'4Ju4Bx/HPRnoTkArOusWj4+n0OMXQV4O0zl1vh0ZwVf+eFkCR01oiQfuIGv47CXFkWAODS4+wLGKHRO8UgAHEKvouy4tQsbeLUHEzCzPXxCazNSWCG8L1CdITMpP9JwW'
        b'7rQOVjQhflI5K9spy/9+t5fX/IT3M1Z6F3Wv8vrQa8fdV29/eiLzs7Avs28v3KKKiV/mKeXjSZr/Ovfp5MRqu4lrJ01Y1XI5pvzb1b+ZFLjM+TdVl95/5QPFwmaJ9pfB'
        b'08LfVLyjmFMyvXjhlfflUZ/Fjc9QyaTvfH+cV/GWII+PHTx+q7xQ/tFnr/22/OJnVeXZ1Tuy2uMFVOUye3/wjMgSmSO31XCGrJ/fQx2F6HyU2V4fbPRVb6L2987CGG6L'
        b'Lxi/Cg4Drs3lbJvvJq6Z4vl8mjBGNZgOvI2aV3uhA/iuGo5DYyO5NHgbPsZnxuNOPupHHZl0tw8fRtdn1dqb7wde461twqc50/vt6AiD3rEzWuZTs/yCGdxOYDvagrtw'
        b'B2eTjy6FbGTnoF3oIN0mIBf7WxdvjjbfL7uVSZmRj86hHrpFiY8vLLDwsBC6gFKOO0sizTZ6ivEb5jb9eNcUurGXj+6DAkVhbgy6G2dzpwfvwG89U991ZB3vAF6aaMe2'
        b'UiE1Padr948Ybu2+LGyMtfvgiEUrWQrpJVGAGVvI/so/gszUspns4Kw534om0rIMfHWzAYUgMwdQI0fvQvaRNACSTyVSb2AomBMfautpo6bSSQMBSbqAKfqAKd0CuhZj'
        b'x0/unt09WyM4lNOT08c7rOhWEJleU6bzSdL7JGnFSYMhEZqUvkTOsNVNrHULAblwjQ5cfYdYule2ULyWP03EG614PY4/SunWxLGTlqrWs8NY1gvklWcE36yqNTtkRybk'
        b'MjIj2/aNS4UY1uQOjnMGxzc5gxP+y53BgRDztcCGEFNcVW9ABqVTmMn0sVnNCTVVdFohc2DmrJzZxSa0Fvm4sSSBquW1leqyyrpakksytSoyQr5UA8hg5Qo5TSHPhHA2'
        b'TVZulu0YuRq4m0zNomJMdlEA/KuuomQ2qJTwgMyxNufA5Orm+sqn0CCfU5pfTiG1mhvrGiqUxtIbGWIzUwDaNEFkwfRssIRUN9c2gcmTGVG2Z+ZnUjV7dkl5zMu+WvrS'
        b'r+bMfdlX0xcufumvZmS8/KuzXvbVhZmTXv7VhPLAMeTX53g5cQzLtJxqKs4ZpMkqZUxglKH5R1mYt1na31HzE9vi31hWdXNUFRRDe6QNv4gB3QJYMHCjwtoEebxFb6GG'
        b'fxwyK9edyAfX1la8HKdmlZTaICGZg49Rc2MMRwfX3WqVz5BxbSlpeiqoKNjqJqJ+9eIn98+Kj19gcPR1yQV3qx15TEwUgzUMOoSvelLdibAZ6AS+Eh8fX4t3CBleDoPf'
        b'TpDRVwrQiaZohRz0mN5io/DdPLQtlUYEobvu0YpcHol4jW1BF6YuxIepFsxivEsQrYDDENTOBk5OwYdWywRUVYSNj6O6PPgyvoneETJ8HzYVbcd9VB/EYaMniexvwjfQ'
        b'fdQFx3EH2CB8FZ2jX5tXsEY9ScVj2AZmJu5DN9BlfJYr0oWCRjW+7qqCUycefoeNioylZBBJ6Di+siCP00lkiLTjzqmkvOaGdlBFyyWbGapmSdjQK+NRjY0S1NliIBHt'
        b'R1s4EufN5dR0zi1Epw0k4vNVBgpRJ+rntESvofeaKSW+zgZK8Ll5lLv1/vh1I/We6Di6gbeiPTI+R87JpVmGL66u5763Au2mHFmTg44YWfIa6jV+8A0ezbQcnUIXHNc6'
        b'qGcXCxi+AxuH9uBdNGY+en2So7PKFXXnMgw/hp2B30JvUWYtDN5MMrzq6IKu1LIM34mdMS2qOYtElOZPzIMFRTE15qPqboc3kUUGg0+gfW1kCbOTkHwXdaGeEnLThe/i'
        b'XryPLGC6SCMQMiT/fqeFCnyFMr7YG18tJowlUq8/s5LJaUN3OIWfq2jfZLwfbAZ3FhPCoC1tZ9MzKmvz973JV0vAfvi3JUf33duBZrp993+iz3215NNx0Xm/3eBQ9sCu'
        b'33trR/ml9h+PC156af5D3wmt/aWH775a+JtfNu7flWF/J+h7H9Vv+sdfPu4s2xQUntu+xKF5vJvm53WLe3zb92adceh3/v4fryQW/W5n9sL0YeePf/6Fo2DZ+OwVn2z9'
        b'VW91RcGnn4lXVWd+wv9xSaxm9ckpPU2X3ln1ZzTJ4yfz/Q5+dvTAvcaQujv/Pf0HiYWXTp7/fGXOps/XLvvzu16/TvhoReYvat77w4ZXf/h2n2vJnt9+suBv8mj1lv8u'
        b'nvib6Wzbx7+484Ovf3fvhDbrf47d/JF6+j8W/+3NZVv9BDf9113Yxv6v9hdZ7N0Zf1rD/L5w48DOn//g+8Vef/nH4wNocMF320589ZeIcz4RPhcD1NLlp37/mkxMVxFJ'
        b'+OyavM1KM4UD0DaIWkQXJ674TBTnLw2/k21UNkBX8FEa678a7Y7eWGJmK+kUw7eLxcfpikoRusGoNIHfwRfSpwRxq5aL+Oxi6ocS708VMgK0lcWvo2uc6oOLBB00ujtL'
        b'Q+eoxzN0Ce2Poke3uXh39cg6yRH30aUSvoSOcYoIe5ODokEnF9Yf+F18xB538NCrcMJPM0fvkF75rtoRXwMVuw6GLG924L4cfJkumJJwJ34DdTQmgW/Qbcy4ctyJXp1H'
        b'o2QOXhAhIhGk7baTRfZefCuYns47zCerMBIHOW5n8HuheF+wI9UMaJkmQUdjQe/B0ocYvogucEu7LtSOt6mpwh96hyyt9uMj6NQCWtIk/C56XU3IbQdqyHByFXoYGaIu'
        b'0q/iYzG4g7wpJG+eJoPQLdwzbRmNQddnoqNkvCCDNIsuMOml+GjlCs7BW/tCfEa9dg18rRv0S7tIhyGLRapw3oZ7SBT5FnqLEczGO9AdP2q3jW/y/SxWsNzqdRyhvX/e'
        b'CrJceY59Y1iuwBwzYtiqJkJ163hLI0HyiC7uInnc4q4+nC7u9AHx/e79Qf3u+oBEWNj5dM4YDIjuaxoISOjMeuThM8z4jp/UTZIl9K8dCEjVBqQOhkX1Zw6GyvqThvms'
        b'XzJZzfgl/zw59XbITeXd2lvyu/JhPuPp80jiC6s8shYMCT899cTUvpLzS26GaWNm6kLS9SHp3faDASHHNhzecGhjz8ZuAfmkYZVpfzNUFzBDHzBD6zXjKzvIYNiemRCs'
        b'KRnwlGk9ZT8Rew16BhnvAK9wvTY0USuB30gmAl1Akj4gSeuVNOjt1+OtqR7wjtF6x4ydoGrAO1rrHW0rASmNT8wjT++uRdrgZK0n/AyoinzPybZeeGTrK/C+JnzAM1Lr'
        b'GTkojXgojR6QRvdl6KQT9dKJWvHEbypB2IBnhNYzwlaCX00I6KwdTJhydXo/+fdA8C2HB+TfYMKMfgBxC0q3QDwDn1qzWLOFs4hz3ORkvrxSOfJH2wGJGKO7aG7tHAJr'
        b'59Ft8X1YNqsYk6vozWTdLIOV8djBN7pkNhrlgdClugSOSyRWcA5DgrLCHMWQY9ns0qKiTMXsnMxiDtzQBPMw5NhYUVtv8JWkOgGnSeNGfARxp00m11aq4xBQV1YfWMJB'
        b'UHQIONOh+wyUYTKf/wN6IjBOPkMzRFUCR1EWjvJPghOtdVZohi6M1F9T3M+/mfCgUuuRS34cUKCvJqlfeLP0g7DBCdJRl8N2AqnLMEOC9rxhJ75zNACn2Q7GpTlXkjb7'
        b'T4QzeQYoOjg+/IrPSqPBJVx0e94jT78RALo0AKCbSQHoZlIAupkcAB0coQ66xWrdYgfFs0ganwxI4wN+5SBsz7VCRUwEjMHJ0OEmQ3+bTAEGzZHuMuFDWfRDWfRDWewo'
        b'CEFA3vOkyHuetNuSkALZmUPqAb6fFPD9pIDvJ51GIfXM4fIAY9ALMAa9AGPQa0Z79rC9q3PiMPPUIJDxDuq213rFkZ9mmmba8em907m79hxADrENFWILL8QMOYR1hslk'
        b'dGDPpLOz2WF+C+vsN8z8nwxVfMbFs31Bd4jW2V/n7K939h/mSQGE5WnBV+SlAFPSZC6HEq1zsM45WO8cPMyb7gwDse0QXg6xmYqDTIHD5BIi591yXKvEfRZ76yzjkyWo'
        b'HT/eYk3qZPj7xzYyJB0Qg0nuCFDKYj6ApHAAKT0CA0QKdw1AKQ7kH1wDYArApXDPR67dlOOV7koPei1WepquJygl5NqLXnsrfZRSpW+P42JBlbBdVM0q/bZaWUoCvEqX'
        b'XRerdOxy6rLvcod/5/3fIQP5ORN4lgP5p4wxnNLylSGj4D3seEyVUBm6lVGGnQ+3gjix5/LvcuziVfNI7h7kf7cu91ruzp181b3LoWtctUAZcT7SxndjASAGvtzu0O7c'
        b'7t4urrZXRo2iwIGCnogowMD4apEyeqs94CquYxdz+InyIXcYT2erqpS1TRTzp7pK9WSSxZbC6ASBdJPTItETebOqPrlW3ZCsblLSv5Pi4ydNSoZtjuR1amUyzF7y+PiJ'
        b'5P8EeXyCjD8kUBQWFQwJsnOysocEpUVZc8+wQ7yMTBI6wCfLChX5i84IVCDSDgnptuKQA93cUdWSS2F1XUWN+kU+OxE+K1DFwrwnhyCODxNvjqKYA4t7wbymyYRWeamm'
        b'0QyLM+anP5m1oqmpMTkurqWlRa6uXRcLGz4qcBcXW2lwSyWvbFgdp6yKs6JQXrlCHj9JTr4n443kf4ZHsVhUddRf3JBDfuHs9PyyWTmzn4QD0bNn5VAKyd+5FethZiyC'
        b'g1h1E8lUHp9IQiJ9QGZnWNViDqAvAWh1Ks5RZOVnls1KL5md/ZxZTZTxObpMRf7/2HsPuKiO9eH/bKEXQXpfkLb03hHpZenVAtIRFEVZsFdsIKKoqIgoC6KgoqKiIhbI'
        b'jImaeJNdcm7kmnJNuekFEvNLYkzyn5mzSxNSfjf3vvd9/1f2M7ueMmfKM8+ZeWbm+zz1nnRjaHmZUBhCDFQT44gtWxQnXERicsUxscdiQgkMxnHNmFQeTw2nz9RTnSkL'
        b'j68yIRYsbuVhU8TtWx6Bj06KxJdE4l4ejs9N/3DXp/Z/IKePFAoKi3IrSytI8ZO6/A+DFDy3u3tqAgWzX3gXGlQeUlmpHgevyTa4wYPgdsmyD//OJXSKj8tiJ7Ip4tey'
        b'02OapqFTPFLMLi+rrECNgnEOOVHbOMlOTgBVrOVT+ib1lX8QFZDAkTmgnOYZgXLjgQGr+P8OYMBpBab7LpqiD9822pHHLeUTTEZLjZ8AF1CW1dMhSrZ4aAq4AIugBLC3'
        b'GeJnpkh5FByg+i8HBxTz2e9WKUwxHxfNIPhK1haOm5XLJxXDrFHB75pfmYVLqVy+vKwcG/hxE5ZiWIV+z1/oyJukD3i2YeH8X78M65PfvMKXZ2snLMELXlZ6O3nZ/Y4o'
        b'GRXFsw2N+u2LpaoIX+zA+63nTK8mebbRqX/oDtdfueP3ajwcxeRETzfhKZ20YWY3GDpiQWFeRVm57My0U6W4W8DcNllslpeXlJWXVKxhXJTa2uHOhh1KEO5u2E09B2aH'
        b'OyH4GtwlsMMTnnb4XW7Hdxpbk+Xl5Obk4ie9ZOpoxpZvuZBLpbGOHfYih5mop8sYw66VZm0K/ixTPjZCgqCdtnjIogG/iXhN0simpsVK8ZjTpmkMBsskjGmvk6mumKA6'
        b'uoJvigV6+B86V4kn2vEcNJn7I6sHC3MrsEChTK2ZDNnF69emYXTi+UMUz6rcculiQ3yrFCJKSoeXUliI81pZWsjLrUDdx7zKiqmTFRqcGh6ZkDwvOzEtOTEhJTw7NCEs'
        b'PIWkcnShH+GFTrFaUFpIjBJiyicxODpeBoeW1ZvMLiWd+Zx6XdzYbCiZYWdiGJustJukU+ymXVlIamg5006FpBAn3etrx+ROdknJsqkBogweF3W8mQlUvJZwGS88LXma'
        b'Wd1lvJRVJRVrC8tLScVV/EriGYU4TVtCDSa6Ird0Dblxeg1nN73MSrm+TIWM4X6x5EurZBT9yyywmCZHFcxCyXE+jCfcOwELPa3WIjE9N+ONikfaOxTKxHdSvFPXCRkL'
        b'jW8p0SHB8by8wtKyZYtwTL8xM6w0RQdPI57McbIKYBVhA8B6DsWGJ7KsWLYU2M7QDbYnw3OjiyLhbSU9tvoscIBZFokvUCgGe4VSr2ygBrRR8BzogDVkmz08pZ+NXS+C'
        b'3fAa+rsMariUGtwGu2ayMaXgEuEJzIRHdAVjRBZ8oG1jBQfsBpe0GS9ZIgW4P2UaF2ZCcGPMixleOgevKStZwj18tnQyFV7SZ2Y48fRmYSUrSA3cZtybnZpviSdF8Ywo'
        b'OMliBblsqkzAx4/PcBjnvW4sZaP8iuVqasnYf52tY3yarS3qHu92hrscsJsxxgebozzlU86Ch7VY4ERRBElHCbgEO4Qyl2mJ8DwF91pFknn5AiXi7674tF2O6s86IRRh'
        b'ISnBrtTxTtSinGLiYA3Kr3MyrI5NiuIkx4AeUIOxNvA6OLnGigL9XBXYmA8PlViMvMEVPkKR1A7pLU28pQxcNG7f6SnZn56YKP5oRG09dZgTfO1qhUYWd6dQT0Gzue/7'
        b'/QtVlOo8NO7948f73/0jtyVRRbHW8m/p7PUn+39QFbMS9p3YPTPmfv0yT/ueu9z6QO5Pb4t4rw+cvHGMm+H54a6ZNiOf6b1wxvLxp0P+DUaxr7ZtKc/S41T6fXCbu9jN'
        b'eSTd0fv7HboZwerub7w665z5qhjWz9cXdZ4qvv9lyI2NLz+7833Vg7u7r664uICvefWZUOHrYSP9zT/Ena+q+sZ/04fbBB9+uPF8UdI77wWVfPT20su/sHYqeKES4Ksx'
        b'CyX3gIZEeydHskwyKhy0s13swVmCcdUDZ8A17CLTB7biGUm8sboG7FWg1JM5rk6gi/HQtB9eYjYSjy7flBOwV4J9s8g0oBu4ABpBbUICODBp4ens2U/wAENQypVOk8Lb'
        b'HqxglzASq0AHHhY4wQ41x1GfO3hPNeiaR5Zw+sFTKiqCDUUTtpnjBZywDt4mV4DO1Yw/JXgOVk2cgaT8mH3ZV8B5sF06QTnZHRJsgXVceDlRgZkGbIaX/e2dwHHYGu1g'
        b'N8F/FdjuwyxjrYNX1o1zrZURzgJH4QWwnZn0PQFq/dGjcAvuQefj8gtZEeDYhieMj0CBDlIcsagM8ortWK7gYCFf9Z+aGsDWwvFbVMa51phyJDfe404CiwHOFdhTmrpi'
        b'XdtOS4mGM63h/FDDZ1DDp1dvwPKevDgxbcg3bKDoXvEIh6U5F68fReEwE8pThqbNRvXyQwZmIi+xAb9ebshs1pRbTLX0xu3P0rMQlYr13NDnbVPbxsVDPgE31XrR38DK'
        b'gZXDHJZdAlmrmkjWqiaStaqJrMd6RmIzZ7Ee/uAtkRTLjqxuRamyiyTXR5Hro8j1UazHRrxhiq3jNmTr2MhtVhtycG3k0vr8x1r6eNtZFKsx4qGx46CxY2ehxNiDNvZg'
        b'jj7W1q8PG9IxbsgUWYhcRRa0jlWndpeBWMcNfXq9b/qjr0luhoY5lK47cwH6jBtxq43b6fTrg9dpl7+qUZP2If3O2o3D4/ROauKmowy7/1w3KcQnxwklX+q6erDCH3GT'
        b'Usx4BJHLxgOZ6TweTFVUMr8HdaioyjvwpcTvgdPvGC1NdmCCrbUpUcHJj7hh4SGpj7ihyeFhfIWptriV/yjzRv9IIb84t3xRobB8EWcSD3GGLMMiFBxUnJaHiGmICtXq'
        b'1fLEeDGDcA81qjWLZvwbqYfb+Ox3O6cyXgQXFKAe9fi9NLLO2xQG89Fu//M2kCKeHx6U+OWMopVzplj56CDtRI+6QMCbeZ7f+4SePj5B+aiTnocGQ2WVFWNDowpcKxXS'
        b'gePvGpJLB1OM0PyOUXnu0rF7xyeHOc7LFfKKSstysbkNDatK0JFllUvzCqceweDHLRs1AuH+sGyJdTCJbarVkkwqJgxVxydDNlCtKFzNjMNwqTBuIJYyG5Gm2VmErikp'
        b'wIOIsaIoLyRby1DKmDzwbFFCy0nWyCDBIjnCycnJgj/N8IZZPEp2yeViaRJWlFfmV1Si2MdiduJFyNZejzs/ZXyj9xDJrFxeWigTAenCdjSewplFQ76lqCinjMM2OTwi'
        b'HK9BCM+OT4sLCU924MlGw6nhc1P505Z3IdkWhwu7cFmBY0WZI/oaVz62ZcuZbYK/EsPqqQwM6GhhOd5eON7A8KvR4X+j9gdcwr9mHhh1yyGV6iljKy4rLUAqdUpLAg+V'
        b'SnhyfHDs81aDqXfS/U5LQkFlYTbeVccUBfofD/+PCKxUbnC7qChchOQCCUhOTnzZMqwpfmWL4eqKsafjyHAsaOCIt/VhBTEqukXlZUtRURXkTrMXsLSSMdguKllZuEwm'
        b'+ahpFuBF0Lb5ZcuEJai4cEyo4ErIUVTK0yaMiWa8mYs/PptMUsvyFhfmVzD6YOqBdUqCj5eLKxFuVDkkPzgNDlJHV9L8ErsTbptIKU4ZT1FlOWlrpLWT7Y3TWxeYN5wf'
        b'L0U6mhfyVhWX5BeT3ZJr0FNKS1Hjyy1nxvTMxVPrFqGwLL+EVMKobWF5eRlqyGRrCipaaWWjhsCI/dSFOablnHjxZUjVLl9eWpJPtmdgMw9pT+N3f07ddkIZnZErVYro'
        b'6fjlz7NFId+Bh7sAPNuEtGQ+rgzcFeDZhoTHT9MO7cZtZ/Xi2/2OTbaja92DR1U9TnfqWLJ/bQ/Nb5o4zBgTBzhfVqYJdozf3Qn74FXSsSWj8KuLFKiw9QTP68ANy6UY'
        b'0OJWbbgdGzcMVsmczouCIqR2EdAH6xg8Lxpq9pJ149kezLkroAWcl2J9QbszofraF6RW4v154OpKKJpkFDEHO7FdhA1rwVbFyngcxVZFcBDWSt2XK6LLU6WcSoGjXXqU'
        b'Q0zarzlzd5SHInCeAhfCNUHtUtBKVluj9J5TkppC0FMvkdXeoA5eJfTQANCUP8XzwN5Vv/ZIgk11ikZBku0owpQvT/m5aMPu1dqMCebSPHCZGFrgeXCFLD8He5Mq1+Au'
        b'KmjCKEmMdnaMScDmFiYWObgfble2MgCnlcdsHHPgFjSW3Q/blDRmorFveyoQFSSBmpCNKJIqcBb9nUDfO5bgsfOpkLyFYFdIeUlS0uKF5VaZ4MiSYg0K7gk0Bs3gErzO'
        b'zGtuzkhVgVeXq7LRmHkzxYY3Wc7wFthGAL1g57LSKVIGjy5iEgdrDEDNHLAvD2xnUiVN03bYBhvwb7xIPmcG3MmjQFeSpr4G3FaJO/ywzSkZr9HnbtQia/Q91CoL8OMO'
        b'rQbXR61O/HSG35y2vLIyFdYvV5sB96dKi3zMIIXK41gqtkXhupHBXmWkY7AFdCri51DqsFoXngP1JpWzSb4s4blfpWzju1In1CaS550GFWqRgT6V4SiKXHAqWhCPTSro'
        b'rwmcJTsE6kBXIhEbFK2AoGeRLB2QE8aAXTORtO2CB5JBLdjFgv0r1CLBoWjG1HYAXnaVRTUaTdSYPSN9Qmxguwpo0LaCp3RABzipq4Pd2F+hwJE4TXASCfzOykAU55rF'
        b'hZO42OBGGM4YG7bCBvSongBUO1VwGypgsl0B7M+j4M5k1WRwNJSkygwcmi2tinaUFGwEjI3mxzg6pcPq50pLlja1iU0UFdqxyplgH+z0r5yHq30bqA9GVxKMKIpv1Lw4'
        b'Oebb8PrviT05Rhul/Cy8wgBvb4BtM4h1cTHoxAZGCt3UCKrJElRm8/plR3jbHovHbnjA3cUFbMsRUBaesBlc4YDbABUGnx2fWlJX6M4WPkLDTdWl97en3oiHLtqVzasO'
        b'eGywdHSsZsnnhLyX0XdR2/xsqL0c39Gk3n3znZyVd5r4gk3737Re8d6dpY7hL284Jly/4YvsX2bk3pF/UJi+Q/PRC4cvVJo90/1+a+EnIXkvvTb7VEP6yz99G65d9eIZ'
        b'bvDB+fMFdYss2ja+r3QhVvvD5uq8OZIEYYoVp9L/vEvSkQVfbC9OzXp8bubZsIQe23Zl13SF5qFTjY0v9sc4VBumtvp8Z2koTA596fAL195/Y0Fkgf2ZyryUnvCRbZ9+'
        b'NvLShcozHP9LMZ9x9MO+zVa+s/T4F9pPv2Td1Vv+VvqxfvW53l80P3z2fmRYzojyoRu6gmsvvqe5qdLn4dwHn3u6n7DZciJ7hYedgqP6ok8a0kNfSxw8Z9fU4rlr0eNK'
        b'wVcfcf762crWn/tmK2l89/Lq3affyFGz7DLe+/FXtseTz+0x/yJxKGzLsn72w1dyP/1610da68yin9L/OBPX/WzWwfya8zE/f7osXf/846AdK82D39c69j/1Bftq5mqd'
        b'fSDYrXgAddaWnQ2QtzG/PeuTOTvuGq++uKPr7tMHHRFFIdvnvTTzwBq6ecaaL9dUHlar3OtyYs+THW8NLDG4lGR4b/mdBdZ5VW3dp6oTlK9XrfH87nX37xavuKa5U+n4'
        b'DZ03VP9Wu8ks8NQHC/X5usRImZrpSozuOqBtPPdxK+gh+zGMnbGX9HFszSJ5YvgELabE7lcMD1lh02c27CdkTXhxIwOxvK4A+8YRMLNZZEsKamsiYkxcCfZgdiExNS7m'
        b'SjelLId1xFSpjDTaWVC7Sl1NuRy2OsMr6PVaoSZPaa/gpMQx/tfXwW4krGOQTIscFcLIDHchMayB7RaTAJ5KsJUYV7egFBCb7yl4I8g+qWTinn1wGR5kNpo0ggtgG9nj'
        b'IqcKu6V7XGBzPtmIkeysD0RwP/Y4Fg26uJR8KdsCNJST7Rvx4CoqSYyZhKeXE6woG9QwhdK+ArbJdpOErB2z5lbOemKFz3eYomJ53piLtOZeqX/70FWMpfbEfMPxAERw'
        b'REtVg6MTZM0gIzcvg1XotAM4zS1Wp7gOLNAHWmA7MWaDLpUyDCUeZwKGpwyxFbhrOWNMrwrTdAHHZOZ0bEyHR0qZBB4ApxMEsdGgxnkyLNsF9DoAkbyzQQbD1DwC9oIj'
        b'RHKiHObA9pgER3lKPYwTCBpnkRKcB25XZIAtE5gI5vAMOWcLb8Kt8mAbqHWOc+SjNASyeWXgJl/v/8QSdZwgWS9zelSSxRSWuKmYhR9JfcEXOTK+4K07rSV6rrSeKzY8'
        b'+w+ZzGpMF0V0hnXFSal+EY+nsTvzLNtVaZ6rFEzI86xXGzK3HeeevF79saUtbenx0NJn0NKn10RiGUlbRoo1zIe0DBqCOj3FbqFiuzCxFv48trCpF9QLhnQsRAWDOnZi'
        b'HbvOjQPag87hYufwxxbW+NywPGXp2h0/OCsEXWdo3uLc5CwxtKcN7cWGUd3yPTMGPAddouoVhnkT/JozXs1R1qy9sC1cZYTDsg4j7tAJTg2FmOcXzmI4Z74i+UEta7GW'
        b'9ZCRxTBZay61hwcTM3gIMYOHEDN4COux0Sx8r8vQLJsOvza/1oD2gEbF7x9P3MJCosmQRZNOoskg0WSQaDJYj/VM0eVjJMQxICTmOfLxknnDcTHqmeIYI2QxhpMYCa+N'
        b'sAtZBhEsDGXzx0lLZjCFiRLTJNo0SayfxMwVpIkdAsWWs8Va+INXyhs3bBDruXRnYNreoGec2DPuMc+xW3uQ5ynmefZa0n4C9C1OXIBCgt9Lk1ik0xbpYuP0x3iTUKec'
        b'WM8RfbrtB7Tp4ORBt2SxWzJ58jjAJE63omYoS7SO+e7ecE990Dtd7J0+JEtuPJPcWIlpHG0aJ9aPGzKe1ZyAs4suV+hRZX5JMx5CMh5KMh5KMh7KemzMa46ljV2kt6T2'
        b'ZNKeEb9517Ayrnr/h1r8QS1+p5VEy4XWcsEgP4shM2vM73tsZl4f9Q8dQ7GRY2eFRMeD1vF4qBM2qBM2kHGvSJyeJc7OHwpPFCfPF2cWIPnSLcLRo7CejQoXRcFuUMEF'
        b'L32C2M5fohVAawXg3UeuqMkMc/C3g0tXdK/uoEOQ2CFoyMyiUSjykEmVxMyFNnOpD2mIInA/y05VsZYH+gzZuteH0dpWQ6RWY8VaLugzZGlfH9YQ91jPoF5p3IzJzGnZ'
        b'cGOG8/LFz+90+j36CQ8mnke6/THVVI+nVV6iJk6rZDmwWMlkOuTfFf6pky6dSrOp2+rBqhMnXeRlpoHNKDgoT1bcMmvlFaoVq1HvZnTt7WRgyb/EQdjTnOcsGcmFywoK'
        b'y4W/NaVA7JdSmwm2mOUKeXPjYn/DMGJKPW8YsY+vDKXI3G8HvCUY28KRNN4zCvaLUpth+xwtCTZ7gjpwTk0HXAPVzACjHnbCy2iEcZOMMcaPMsgQI5BHLCoxUbF4nGIH'
        b'T3Bl45TWXBLBvAhYh09VOKF+m9NKFMRE4y24t9mU5UI5b9BRyWyq7wG7+DhyNPKsQXGYoidvTGcMHLvANjXpOhawE9wma1lYtqaGxMDTFsymnhhiCclRFbqVMwaelKAK'
        b'd+wGKRq0oWqCxynQP8uDgQVcg+2lDCnADOyinMFhPcZogMaZy1WUysE1eBa7FjmNjUInwUUSHTwb6mvPt4sLdZKjuGtYqM9ZA5sZI8gWWBsswD3TeDlKPpfSZatWABF5'
        b'0uoVailo3HtiLjYWoeHs3nxj4rAD9cX3ggsp2IcJ2A/aZH5M0GC8imzd14Qn4C1sV4mezWzqlwdbyLOKFNZLIQGKLBki4FAps+P+KDg7Q4Yz6INbGLwAPOXBlO05cBzs'
        b'JLap04qoc45UtwHsYUxa9WiUeJyxHhVlMKQALrxGXKQEwH3cFFAHG9KQMB3ETlIUE0DdBhbsUZM6kPk8fQ91M9GPTbnkxK92K2MsbiV6FtQc9l5cIXkXhMnMwfDyaMpl'
        b'Hg97GlLeHmQ2cdm8gkyMY3EjZh2mFlHrqSyzDawatoia6t96VgFVwNrONhg9cgrFd3Y0zn3s3TyyMYYd/wn2xnOa9UghuKA8tmRZIZ9Tjvuzj7il6D+MxsX4o9Gl5bhJ'
        b'rXWcQsWWk3Y85jM3oLREWJFftnT57CzU+r7B9HakZcXORcznnnY365rSJaVey17hALtXeJMvcQmjXcJGLyCvE1I22qaqlLGSC0Ul5sQ+3chmDr6cqkuJVi3AdsvMs/JF'
        b'FOPepMcnaZKPHBY8Ac4TJznwuh0R1pWrC4j1C+zJZ0uNX2ecGDnogrvAZXRyhRqoN+JQHG2Wv4BLHnffToH6PsqImElnLyzGnniJ4DfDbngVC2PhJilh4vgapoVpeGBz'
        b'F7wBaxkoBZLai0SklGE9PAuxZTAXXFagONasQHAOVvNZDMXjwvJYYTw4bwMbuBRbhcWDZ4v+LcKAfbuW1+B38i68T4URg/LdHNl795+VgnPjpcC9hPncS+0OvhZ9Kbq3'
        b'YMB9IGTA/WaJxCOK9ogavYDZeUdc/OgZqayEV2fAPniBjUvUB5wGN4gmsQFnylTK7SI5uAoxy+V0DmP83q1hDi+rwqursxWQFjmAK/gMuFmJ85MPW8zwJoukDfFU0lzY'
        b'SJScORAFqdja2cOLseAk2I0adAx7Puw3JSd15WfBy84x8Fosi5JTxh6aWPAQbFtfAtpU2MJfkBY78Mj51tx5ZW9GaCxMnslPUrDK3pV3N1Ldv+RYu+/ak5GDb8R95X7L'
        b'6Lu3XlJSa6zS/r517m1t/nydNfcEkgyWHFf7U8GWZ0d/3vZzzR5t4Ysniw41vJ26+d13P1//d+8bH7yq/sPZb1O+8C669Gppxzvu+p/Bv2/NfvOW49KXelv3/JxT8enx'
        b'm582qf6wIuVFroOctRZsl9x/yeWUyzM5ucPBK3x1PjoKHC7y4DnblYfl5vW++nJn1b2nW6szP2bF7nlzi9xZnxe/uZhZOhwf2qOzlh7JXgyKz4XGxt1/GPGNY+fcZd4f'
        b'zI31dP46OPej0o43/pIf+9g552fTZ996Nie9KBKfLute9+qH8x8rdnxm+Y1ceG7Ne98Vdne9+W2StkigtShl5lVbteulSR8fqpmXrthf+8P299NWeM6hXbirXnrvVOKL'
        b'fd4mjxwP6B2Vdz4dldvQmK3wTPVMyo7Ky+/Ni37gsOv0wNPd+eVLIwe03rx6IqH7lxndD3IdQusqqw9+V3vjTfj2BxeoDzVc30yqqHzzraOVOkVZRq+c0n/fNOJHvS03'
        b'Xqg3+36GzeK+5Nfl/sJPc195t633k8BvPROPtIQdS/jMY8eS1awG3ZAZXcXn1hWAH6J74s8qVJ5xXqLT7ZhXWnUlbl/JsR0jVhVvjRwKvXGjKnzYIEv3Ly8FG/Aun9BX'
        b'fnY3cdPb/qaP3lGqcje8bDj/578PXN+xQvnDlgwXG6siHZeOmd/UjzSP/M0s7sz8vZ8EtH0c0NQ56/3gRfFn3R8vSPjA3+Tds6+vH6i03ic4Lww4HPzF0+sr4eOdX36g'
        b'c+dv4kfVLVTihaeXir7NufA/hUHU9YAdHyZ/dnzWs4+0hP2bP9rz+Zfyw1mW35vazH3vh6DgD36w/HDn+Xdn7g4MzzluXR784UtGz1w27M3/se/c8kzlc2/ovDBfIPox'
        b'tu38nTuNeqyfPt8o8d+66yfjXdZfBrU8TE96+6dXryj89A+DnI3H7616Znlph87DbVolrZ9UGz8LGuwRRSy01q5dnnbnbtWl5aKvXl76jrLd1ttZqTftV1tmv5XiHJF/'
        b'fqvz8q2f7nnl3U0VYZ98eaYtdmWas8bPekq/CBrNGryHb7JG3Lb0Gj5afv61vWnXCqtXW900/fJ+hpKpgc6CVR+XPv06i6X/Va3x51/208v+/svWTw+ZprdUiJYVlxy+'
        b'8nmnwveHtda2/XIiJenho+ELdn2H73tunPvDnYxnniH/qHww4zXaqPWLWzVr/+E7/NGu+T++/+3JknvucudcBp7qbjm3umzn/wy/eiv0AeuL1rbipXJdq796ed79XZ+X'
        b'sb5at810447Aj0PuCzkPo9ctaw+2CWB9pXW5Nb2sPbJCFBP7snrqC+0fzxn5/gP04yT+Ma/1p1Ui5b+z/BPXH7uv/uTjYzerhsoU1qq9UjionnrfMk3hzJqXZis6/mL8'
        b'8YaoD/Y9CxAc5/5jb/s7oqfrYz9urfTbFT90uEW0+lql2UuzrTyCZj1r0fr5swMfvLq35OGLVrcXmO7dsKmZ9XOcx9dh4AbU04/p9WvoVP/2dti+NJNLvgMbDip3LDz4'
        b'+My2vQZiyTtv3/7orUAr5bcvuC5btvVT7yHF7/vDf6rc+/7izd+rh84JCjzx46edP8xeVLdpyevrj1yWfGx05/OfjzqbnvCevdq9+o3U6kfKX2R9+F2Yrt37X6W+/ejH'
        b'9Fs6wR1i/Xnr01b2LRHXHG9+8he1d9YLdn34F/FiXZ1fzol39V/48RWfhZd/cev7SfTZh3n5Td9A/a7Pm+/d/W77vVWBDjbf+t56Sdn7F7nwJwvkymP5S4jHlXVwv52K'
        b'HepRE28kjD1SwGVTZuAyF14AJ2EvMdo5snDfmjFGRsDdUnvkhpnEWKm1Cd60d+IYTV65yWbMgaBvzRIBrBOMnpvhEqvCWaSSwKz87APNayZDbEADbOCEgeMryTpSUA02'
        b'pz9veQQiNXmp4RH1BM4RnyngIDiAV9TCvZnwEvaq4ugUFYs6s7qxXDUg4pPk+sFGuM9+1NMQei1sJt6GdqoS46B2JGwRjt8srgb7M1U4c8B1sJMkp1wR1gudUAocy+P5'
        b'wQVKaNxxmSzdheiF7AHPyqeg180WYq1cKwf2CGRWZnlBZjbbLktKxIFVC2C/INYuzUWeYmexvMFl0MiYfmvBSTaqDmc0uEE3xcGzYC/bCvWJtzBm2l2wAV6QOmgBVahH'
        b'hOriLHsN6CkgyTeLgf0qsNoRXoS7BXALaOJQCrCHnYDhtKTAw7ngzNgFl9H7UQ1Uw1bYhnpXyRtIbduBq/AKAfc64C49cWQHu0A7Y79FA5h5TASO0YUb0eOV2RmwVY8p'
        b'//0BmUK7aLhnOUEs7Y0HZ+BNBUoDdHMqNEE9KRQDeDxeQDz3UJRc5Wx4i82B12NI5rJLneBlAbyUoAJO28pTStoe8Br2ElWDip6Yh3fBbi8h9t6khKpHDvXOeuF5uIcN'
        b'a8vXkgg2ecPjOG1KfOwPVsBBebspD65ztFhchlF0Xk1qN4c7XWRsKHYQidzIGxOWd9s78ZVt7cDpxe5caqY+B26G1+EJJuc1eeCCipMAXuXD2grQgrKuzl6QLse48Wpc'
        b'uVoYXwg2s5h+TScUsRg3PqdArQ68jLKLS9weJ54qkKM0dTmo77MzlCm2A5qZgngHUOMsc0mYDs9RRqCKC07B7hjSjIo2FAidosEFVXQJRanLI4G5yQkKhW1kJTnSR52g'
        b'XyXGMXYFOBeFhFPIZxXBFsoglRuJRok1jMydAp2FQr6eC07jbQpcNwEXiMwtg1thlUDmBFMONcEGWBvBCYjNISKTAmqwr0B+jP2YDyVwBo1dy1A29zDAqD3rfYTRdnyd'
        b'MNTdAw0sUBcNq8gZdbAdt9DatXpyFEuFAjdRUpmF7U7gquV4P2SwLwNPw+BV22QQ2zgrAtbiRqwL98h8LB0EJ8nJNO+5E3wsgSteGhydeV6Mfb8T1sKzKraoGFbE8tmU'
        b'cg5og01s9OCzQUwjQiWPdQA/Js4RdfCvsCglVzaeVIF1jJgcKQQ3VZz4dqjKarnqSN2VsEscOCRyT9AId9ijSnKKZtwxzgDY16qIk8cKIzfbg+tr0LNXxKOeJ+r1HgQd'
        b'LNiit5YR4BNoNLFbhY8dPcNaOUouIgk2stBo+RJk/KBlVMKbzOTIarCPy8yOLIW3SJ5TwVbYhqQfnFkWjmelalgounawmYhHAGyaK2DmaeUpFZST6hg27ADtruRsgRDu'
        b'xNVTHouZiGrO8DrYzlGEIicCUtPMiESKoHghFote1EaSfZkK2OOIht+Xsavm7GgOxQa3WUbgCjhKWrE2aFRmpsjWxcq4bRmV5FQyuAD242GRFzwuHRZtgXtJlE5Oc8d2'
        b'0eDZvBW5nFK4byE5qQN6vZlEOrNQ026Vm8MGp2ejKsEvKh+4K00Ia+PhPqRrSTNFsoi1lzZSu/DwGlhLLkOtoGqJEO7hK4PzDvAq1uGXYlmg1pYy0ODagT2wnYieC7gY'
        b'h2JhzqJqEoWks/BwElxmGnN/AWzCs2QLChnfe/CcdPLqPNwfiGfuV8LLqHZALUuTtTAItJF8wyOgDjMaL1UorZCnWOA4hV5DPEbg2sB5cBuNSGCNLTwcjNoIPI4ugIfA'
        b'cRLvYnh1GUq1bcwqu9XwLJtSAAfYvmCrOml+aMDZlI732SRge1cNnjijZrDhJStOQSHcRsTGuzhpnDdTE7BlEWeGGbxMWNvgMDgtEMbz0YsKqVVGL8rBq5Q+OMt1Ra/K'
        b'XuYtXQUOws2MXsdF4mcGjiK5DcxgklCNRuZbpOqRlJlyAWiFV5BMgLPzGNpcO2jGOzD2xiJ1Xcei2OksRyvQTbRTKugDNUJYtw7sEyjBmlV4ChI/RQse4IAWqwKm+M6D'
        b'y2HY7THYCY5IfaSudSD1Eb1Ka3S6zbckkM0DB/UYGl0PaFqrUqmmBLa7oUI1ZwUDkSW5JT0Mdgnhbkd4E7U/iq3NmpVbxLh866eCmYxEr0Dn8fv9dI4fxypyAcP4OwoP'
        b'GYw6js0sR0qeOI51hSefYMdh4GY0atQYXe4Md8U58LNhT3QcUtxSj4c+AfJI1+wDfaRQg8Eh5mLsq5mZZJRfygnMDHiCXbcu2YR3rWAH6GNuW8ER7PB6kuvWNHhe0Rk0'
        b'AWaOdK1umgpxH+e4AjWW9aAK++Tr4YATbKmPRnBi/mL00DHNqp4C9npx4uBhL1JTrmCLPJIHaTuj5oSzkTJviGLEoBklvxefRT2OfViXH2KBPXKgiYjpAmtD5kaiRTz9'
        b'YR1HCV5DfS/c9FZYgvbJfu2y1UgGiFs7DyfyrluGXkdXZRnAzzkJT+IcXOWAdnhlOYOH35Mxd5znW6xnQZuf1PMtOAFaGInrSYFbVfBlR9MwmPMaC3QK4FFSy2Wpaipw'
        b'F9PJQUqsnUMpUuwklKdOqYJPhT1IwccURbLQnT0s7DQb3GJexh1gpxZSX7Wb+HzlGKwmcEdCG2zjwOq1oI7IXRnoAkeQGq8DOymKZUjB7XbwFCn81XbwgjAeXnRGnQik'
        b'qTXhNi6lsZgDdoWyyZNtfFGX6LKDk9Mq0IjVwBHyVisi6xX84LYglZi4ElSsFJvPMgX11qQ48sAJTSHS7bBGSZYnDuokd1L6sJ7rZwgYv31wm4GPiiPKE3afeQbUmbK1'
        b'9JEKIHu1WiNgG/YPaR+PSqsFnMdSjRrvIbAblaU+6ZTtThQ628HuKL4haMIK6CY7CvZ5MEKxA/UctsLLjvGMPcU8eAMLHkwF15kOzk14NQ/WxrGCJngqxH4KUVEy+g3W'
        b'LAPnhU4xlXzU/FG/LZJis0FDURwzBNgZg/oRTB86eoYtVm9qqNO1U47juwCcZ5YUXEMH+kb3d8E9eIsXK0Iug9ECtxaCbQKnuDRwBKnrNawA2I16y7hEHcE2C7zzC15Q'
        b'xpu/WK5psUQ8NMBmeEqK8gT9SNlSDMqTP4ev/6+Zrlf8zUuEuKCeW6s6Z7wfQnnGYrfWYFpjHpnH91OVskLWu1D6RjJPbngSP5b1tqG12CZGYiigDQVibQHGPxo9NHAe'
        b'NHAWuwRLDEJog5B6+SFdw4YlD3UdBnUdOtMkuu60rns9Z0jfuFnlob7ToL6T2DlIoj+H1p9TLzekbyTWjxZx21Ue8jwGeR7daRKeP83zRwcHwgeU8AWmIst2e7G+I/qN'
        b'54TFejGdhWKn6F4u7RMt5sfUcx+b8epVh8ysG1eJVhLPaKpD2rz6WJF2u5lE25XWdq1nPdbSHaYUNG2GDI0azRvDmgXSfWT5EmM32tit25U29pQYetGGXvWhQ7xZ9dH1'
        b'0Y8NjVrsmuyG9A0e6tsN6ttJ9B1ofYcRDttIF6PgdOtDh+Upc0tRcLs8utjUYphKYmsajZCwPmJoFr8joC2gdXb77PpYlBxRrETbpT727VnWopUd69vWt25s3yiZ5UXP'
        b'8hp/esjE+qGJ46CJY2fuheIzxejZLcpNyiKvdn+JvjOt74wPKDYpinSOzGiegf+j0qQiCmuPEVv6dnuJLcN6MyT64bR++JCxWaOCWD9EFNwR3RbdWdCdKXEKlliG0JYh'
        b'0lNh0lNF3eslTqESyzDaMuyxgYnYYI4oXWSIvrArtznDlLqB4UDu3cVg8ZC5ZWOG2CQA76zrLhrk40lmE9MB87v2wH6IZ9mu1Jk+yHMX82b3yot5UQPWqKBCWaaopFCI'
        b'CsrUQmziI0ptn9dtPWjlQ+7tze0v7ise4pl3cNu4o6fEVqG96WKruIGVEl48zYtH8QThaIJMhzVQLM3zOq0HTVzExgndudeWXFqCEmAJLAdWvuBwx0HilUB7JaDqa4wU'
        b'G2d3cmlbH/Tdm9Q/v2/+PdZr3Je591LpuCxJ1EI6aqEkMJsOzB4xUo9kGT6hcDhsShkYtqg1qYlWijZ16yB5txGwZMlLb89+aBU4aBXYu1hiFU1bRUt4MTQvZpjDtglj'
        b'PTazat700Mx70My7V1liFkqbhY7IcQxQvCgYVsTRyjfJDxmbtIQ1hSGxNKbN3STG7rSx+9DougIFE9PupGvzLs0b4lmLeYWdHl0BtP1s9GvA9a4P8LkX9iCWjs0W5+SL'
        b'c/NRSMcWSEIL6dDCx/jyYubyOejXQNLdDJBxL/VBJh2XJ84vEhcUoZCOWyQJL6bDi0nsMZ2uF7zPeHd79ATQ7mEDKQN5Aym0e7TEPoa2j8E5lm+TF1W0r6dt/CW8AJoX'
        b'MGRpJ1IW84pGJ2zwJymNTsqikwrRb4lzEe1cNKKm4IWqCgUjcqo49ygYNsS5R0Iszf2E2H0kPF+a54uq2ARXsYkpaVG49gI6WRfkzsh1FnQtldgG0LYBI0pyOEYUDKvi'
        b'GJWalHCMsU2xqL7FvAx0vdoZNSQTiy4t6i24WUrPThAnJomTU8WJqfTsNIlXOu2VLrHNoG0zkPCZL2Q9tnfGReY/zGHxs1idumJ+XHfwtchLkb1hN2PpgFiJRxztESfm'
        b'F4uTkh8mpQ8mpYszFtAZ+XTGIklSMZ1U/P1QcMhdXaArlSwkVgvoqAWS4Ew6OHNEgYtzhIIRjjxONwqQ+BqaNhqJtIaxVHSaX7A9YztkYi4TaJOI7qLusgE5sXHyvQgM'
        b'BQ5DsmcpmoFSxgvp9uoJQhJljyXK3nBkCcvXGSkhFIxQvqZ6T3BQHzG8kkWZWSE1xNLBagiFjWzGO2N589ojQc1BnbmDRs5iI+chL5+exUj+GuM7IzsjHzu6NsYPWdu2'
        b'L+7WbF/aGPlY35Q0gtyOpW1LcRlHNkXiWlNqU+q06LKW8Fxpnis+oNqm2pnclSF2DO9Vk/AiaF4EEa6oTrcuH/TVy+qX75PvLb+5WuITRftEjZUJqkFTS7FJTGdYpyL6'
        b'6tWmfWPEnjHDlKKJKaq0h4nzBxPnD5lbtRt0Fg2ae+D6sug177fvs8cubKO7dQctvcWWIb0RYsvYgSIkPf4WSHr8LbD0WHQotikOWVp1hLWFkU3AXhFiPvqk3vN44Cvm'
        b'LxTPXSixzKYts9Ft5vg2c3KbFc1zQVKEWuD8S/MHWHe5gDuQSoenSeak03PSJZ4ZtGfGyAzFJKzRcDg8kzLhES0mQprTg9Fnmv2GfYa4ZJTblFEL8zjj0c2lXeZI7INp'
        b'+2AJL4TmhaCn+mFR98OibmLaEt4ULrvBrcuXtg+/5/bAlxZkiZQlvIU0b+EIRxkXGgpQQ7KwFhl1aomNHcXGkd3m12wv2fa63fSXuEXSbpFDxqZInYiN81Cxq/SpDATf'
        b'DQNh92bS0TmSsFw6LFfik0f75KGrmgV44ROqBWZKVlqRQ1b2ouzOSrFlMipomz6bAYs79necJX7JtF+y2LJUnJ7xMH3BYPoCceZCOnMRnblEkl5Kp5eOFeIIh+uKa9fV'
        b'dFgZZyyiKUKmOpPbF9BWnhKeF83zGuJZtKvQPHek71CdsvqV+pSQbhFbLuos71pHOwejX+h1UwyK75U/WEcn5IrzCsX5hSikE4okEYvoiEWP8eWLmctD0S/U/BReVhAn'
        b'JtOJC+jEAnFhsbioGIV0YokkajEdtZjEH9e54sKqM6u6y3vW0d6R9zj3Zt7j0N6xEuc42jkOi0tEWwSqAX+kciWWQbRl0JCtkwi9VktGJyfxJy2DTsuh04rRb4l7Ce1e'
        b'gjSeL8o/CpDGwxWlSioK5T+mKUaa/wmx+0ssA2jLgAnlJmsVqNzMmgWoIyI2LmLEHRVFAShAIuFPCwokEYV0RKHEr4j2K8L1mCA2jkN1KH9JvnvFtYpLFb0hNxMk3rE4'
        b'Vy5xtEscbrpRTVFDPKdhSsXcotv1mtclL5yY2LbYIVv+Be4Z7pCD4wXBGcGQi+s17iVud/pF1R5VlDRHJ5Q0RyckoY7+Dx3CBx3CBwokDgLaQSB2yCINNH0wEanDTEli'
        b'Fp2YhVQz3w6pZr4dath8O6K3l0lsA2nbQNRkrKxRi7GyRg3GykFsGYFSrHZJrXeRxCWCdokY0VHxQOWAApxGr2FdytqmI6MtozNDYuWJhGbEQA2XDgpGVrGiWTZI/+Fw'
        b'BIUGRk9IOExC5siIJtZ6w0VoPGj4UIM3qMETaaJ+TlRb1JC2zuHI/ZGo55cg0XagtR3wgej90Y1LG5ceKWsuk2g70dpOsoMFokyJqatE243WdpMdKxKtl5i6S7Q9aG0P'
        b'fCxmfwzugHGbuI2pzZm0iZOsh2bcrErr8zstOl07LWh9x27tHgOxvt8wpWxgOuDZu4b8GHsZiliod8vvDOuKpR0Ce/N6V/Tm0Q7BtEXIQP6gRbTYIv1esdgiVzw/F9WG'
        b'lTUWJGnddaYgxcssRAwXO867p/3AmI6eJ7GdT9vOH7K1F9smd3N7VJH6Qb9QnyAdpN8LfyHrThZ6jeAqQcGIggIWQgUshEq4mFEwoqCmg94sKBhR0bKa+YRCwQilpan1'
        b'BAfDJLClNE3qVRtTJBrmtIY5XnWrZ3h47f612P/1RG9hSlPhC6cfwJB1S7Jlfszagx8x3HD64YqxPHaVTkmHK5Uu06ANpw3+NObhGjZhvBP0ZxIHAw3j4/lcFBBSwGnV'
        b'SWz08p8pgohMCY0KjwtPITR0AnJk4OiiUaI5zn/5TlyWOuXV/4px5VT1gMfEc6ZnltvhOpmCsUvhhZZn2ExljKLLuWw1DfR6RIEqZZHMGjLxHDJH/R77YSU5S1QJOFBn'
        b'TgQOmc+a8kQ4OWE28UQROuE4ZO7I3GGHT9iN3jHliRh0wpo83A+dcMYnnEdPeE51YgETFTrhhE7MwUJDQnXK2HFI121I13G4hOWprz5MoaA6angZi1LXHWYTrvWEANOm'
        b'dXfPZU6ZMqTqDLF9gnjugiEjs86UXq0BIeqIqsfiRcQofELCxxExQ8Hhwxx/tSjCpv6tcERu7N5hLjm+lkVpG9f7DGnYiDVshrTDhuXY2hEYea5NnNKjsDoMDVCYBHUW'
        b'dkd0LhzIv+cpTkoVp80Tz88SxywUh2cPGZp0uvfO6s0fsBxYLfZNHDJxRxGpe6J41D2f4ABppwgWKsfohGFOJFvNcJj6Z8MRhbG4ydFkbghHzXKY+jNDZsURmSQ+BOrg'
        b'frwssMIpJs6uANY4KMm2orGpgPnycBe8lDNhwamK9PubTIz81voN5DenQFH6W2ncb2X0W6VAlfxWQ7/VpcdnjPstxX83K42ivbWnRXtzxqG9daZAbJuPor0Np0F7G22j'
        b'Coy7TP63aO8u01NIJ5+Vn/BUi1Gwt1qRXIHZbyK9eROQ3sX8WY9mEBcJJeWF+RVhhXklFU+dn+N5jzv7T8C8fRiaqhuf/YgbmpAc/ogT4hZS7oLVsBsOPDi/n6rtw+AA'
        b'3f4Qilt6k88fx23LHkfog64Yt10eyKzuw2Ds8tmYjq2cHB6XkBpOMNuWkxDXKWFhyYUrJjJPXcrn4Az/nktdR1nUsoQ81Z8u1lFA9cQ085UmxIHroVyZO45yLSucclV0'
        b'tFwFn5ruGa7lsTjX/6ls6qLJbGo29fzydTlmXz9sCcVrSq7OKJejdPKJjzVwBOwlS0+NYCtoUfG1J36TsPenZijSLRm4GM8VYjctrrabhx9hbHXrAfNalnyy/uUjcyo0'
        b'U5RTXHbFunAWyVNHgdxDjc/5LGZa47A/aGS2BVJwawCzvMHV/nm6NQOd1p/U7CZSrXkUsxuswGfS/ideoyfjeEiD979BXU/71JkK4znXuT7/Ds51eSIWMjZK5ieW1P+F'
        b'HGskhu+ay/9ejnUBKXUM6sUYkz8TYi1r7r8BsZapi9+8wud3Q6wnaqDpINbTKbJfoUpPqZSmvv4PQKQnA6sYtkruMoxFwdypaShKo7dN5VzzOfD0hHqWwqbxy5ABSKMX'
        b'ot30wKPfojzLUvJHOM8lRf9FPP+/g3iWtbgpCMf43+8BLU9stL8TtDxlA/4vZvlPwizLxacSNAnYDjrlpqb6wv2wLpZhfkSNrS6xUgD9cKcKPAkaQkrmXrvKFWajaFKE'
        b'7KMvex5r3baPpe5n4Od7yNXVpauoqsZhzv7w5Lv0/b/df+P+W/cH779zv68B7jbp3GpiffdePRi6r/natsSjL6rm631zeLlFbHTufHmPDZ5v7bB+SXtHjvyrHtTM5RoX'
        b'im/z5RgcwA5wnSOFAcx0IziAtbCaWcbRBRvgQQzXnUTWjY3iuFpzyGINXXBEafLa41i4hRMWZ0SidwA98LwA3AAnpPRYliu8YksWLfitB11jEIeOyDFCLrgAe/jK/wuz'
        b'De5tTImUfb7HNJ4nW8L0075d7ktp6taXiSokGg60hsNDDc9BDc/uRb0VA+n30oa8gge87vlgmmwaocmmEZpsGotMntRzG9SG9Ewb1uFjUaznWKv4IHPq30danTbT+gpT'
        b'YFaX+vznYlbL8ziThi+/Tlct4rPiywsY/0NTklWfKxoZVjUEFc04rKrFNH2B51Cq8r+++ztfYVzaVSb0ieUm9olRj1hJ2idmSxGpahiRWqRC+sQKU/SJFUmfWOG5PrHi'
        b'c/1ehY2K0j7xlOcm4FE3TNUn/nU86nj7w/8TbNSJ/kqkHU0pMHQpejVjcuN/can/xaXy/otL/S8u9bdxqQ7TdkdL0fuEGSPKKuIP0FN/RWX8O+mp/3bm50ypbbAetsBj'
        b'Y8hPUMNiq3vPYlyX+OAXvzU8AWtj82B9DNydEgVrEhzTpRzFGFiHt8MJMrCfD8w15FJgP6hVAn2p4Dbj26Qqce4Uvk3YoCcY1oLmaAYg2rneV+YchYI37eE5TXCiEq9Q'
        b'V85aNroU/jknI7HgpNTPCBszEluU4M11xZUO6LaY5fD2mHMSWB3lwCA6YHUcGlCQHUbZNgspxWBwLK3SCd3gOVdHMGmUQTCLVXCbA9wTx+wVS1ZRQIdOwbbKYNxthE3o'
        b'obXSCNMSMxzTMzAsMiYuFpxOjQLnouKcHKPjUDzObHBJxQ3UJqdQpqAZdINL6qVg33IGCbAfNmYK3cpR3ssouLkMXAO7nUnWrWErvDopflgNtsLdDunL3cox9JBgSLlU'
        b'DqhVAAdD51a64givwFPRKczFDrJ6SkU3hINzyePyv6BIAZyEZ2AVIwQNavC0Srm6GrgED7EpjiYrEO6EXQzLYwfcPhdehtdWCeHFpRgX0s+yl4PdhHRgmM2lbHVQFHNy'
        b'HP4SHEmVvPfGGa6QhTqM6++8cnB/oApw0djhXHJ044Jm7gvhz8Kf6rFDstp1FE5vXfaR0/ljfU8S1m60jFssF6j4l3W31n1pdd/zNkthtySy413K8VxGQ/7L/g0JwoPs'
        b'G+99/f3dhjOV76jet7x2Y8/mtpU7FhvNP5deeFVFbc/r4vb0BH/3T9K7d+bt2vhRwtqjNte714X364V/WRLUlXdr3sb+23nXE8/MbdwVP5Dxo9PZrN1qi4ejz9Wdzn4t'
        b'Ny8ppMmUXymq4SzMPxkvSNERlh8tTn6ysuSb9zd9X9hyT6H6/ow7qes+cHvbzdevXPXjo1lVb3flt9ae/qnpU1V5ttytN7mhu106V4d6058umB/cy3v/Nufr6PgfNpnx'
        b'NZi9YO2wiz9xzxG45M4pRcJTT8aA6sE2oNYXnE2Y5D1lDrxBlpB7ZxlI3adgIO2RYHBWndnKdQCIdJEEdIFbo8NHBvO3KphE7KlcoSLQFzznQQVcyidr2t25oA3WWmSP'
        b'yoTKMjY8mgV6GZ8lh+ZbynyWsOCOXNdKLbKSXgH2LBBsKh23bQ7vmYvQIBsFckAdf9xuXhNwUfpgZjuviQoZui4Em60YOiFu3DXoEerwBrhVwokFItDPrLfvhJvRwLnW'
        b'ETXKXnCYQ3Fns8BZcDyVTDMYwcPFArcYrDAuUPAGPAuvocH1DXJnCGyENWQKQgi2yHZYwtPwGLM1ZStsy7OPiWPqA6Vey4YDag3hUXk3spJfHjSuHmP7GUSzXSJQvHh+'
        b't6BwNcP2gzWgeQq+n7wz7IDtfPU/aQkFdmrJm8DUGwetMps8/poKptfHuHkZDvP/52B6mMJmdnjT/k0SPVtaD6PKNMOZEXqoxDCMNgwTa4c91jId5dp59QQNFA66C8Tu'
        b'AnJViMQwlDYMFWuHDqtSRhbNzvUKhBTH0gwi5wMlhrNpw9li7dlDWoYN/uSEyLvdv9uyx4F2CxmcFSKeFUJ2DYy7Us/0oZ7NoJ6NRI9P6/HxPXnMzoIkceoCOjVHYpMj'
        b'McylDXPF2rkkWrGWndTAwNHJYIkq2td0hw/a+IptfN82tRPbh99TeKAqsU+VmKbRpmli/bQhE8vmBZj8lsHqTO2a12s16BgkdgwiF0fc03tgLLFPk5im06bpYv30x0YW'
        b'tJGD2Mi7W1dsFNzrVa/42GhWY6BoRb3iP/SMG7M7CyR67rSe+0O90EG90IHIe+nitEzxwryhsARx0jzxgvwRDku/EJtFUIgzUzjezqH+e/hov71EiojURBTaHxCpcGz0'
        b'OEeNGT2QZEX6sVjRxFbxZ4f/OsvHfxLibBGf/TTrNxFnU5kF/jS+mUU8sbm6+kZMCTfzWfmreDPMNlvmVDkLS6kyPDZGTgbdVJ7totBAjgplAbs4cBt6Cx4iPY0kEyCC'
        b'2xaNOnnDbLPr8BxDVGrIBzfAZTkcgxRaBvaaMeD5ORw8516sLZ9TukA3kyI9Ew8bcIKAyXAvNoIBk6G+6mkGjVQLb8Nb8AAnBLZRlDPlXA6amS7XwWxwRrgC7zXeg4Fm'
        b'oCYX1pJbIuGNAgwmk6NAby4hky3WI4neAM7AfVIuGdixmJLXZauCfTyGWSZapJEC6wiWDFyHWyj02jqgQU7FLoBXCZmMQ3ltYrhkHuAsk4hT4NxSFabH3MTHDDF4LbwS'
        b'15A7bAjAnLDb/AmoMBbsAbdgGykMq/l7KWMWZZvonqOeVuLIIK6ezrOgwigqyk4+x+Jje3XmYKBqFFVPUS4ny3Ls3t5g/u8Bhf1xNpTdZOUzPRiqD1sY6zhSCyPJ5JIi'
        b'VQqJw9zchTmq0EWZOSjnqUuhoYDLOoecgGytdRTjVaAD9Ec8h/w6oEuIX6hrsIfUjfMisJtgvTgUH97AWK9yUEciPT5THjshzPnJNsfhmOl6is8iRKmlXmWrwD684ZzZ'
        b'bQ6aDP/vL2gOynD5XllBM+3zCrgMrhCuFhs1o7UYq5U1nzSdPHCcp1JOkFrg/AwKHNFAA0CydXM7OAU2q8PDBK0lA2sZwZvkNrAFngb7VaglAElpEpUEjoKtpMWl61hK'
        b'0Vpw+yhaq0aTnPNML5ehtVjzKTlC1sqE+0tuVx1kC1ejhrg56Ztbc+elvB+hcajgFYX9herCxtd9D8Up3uDei1ZXfGX/EuF+/+6j+SEzg10Kk9dE1S1Mbp/Zsfpxof2M'
        b'NUlpZ569F/Blf+vX2Ve/EAXPWrXXMlkpzelR4E8b3nZ/I3bTiRvXs5sr3/+7Z+gSdS97x6zXHw3/8NFXnc9udXvWffL1xwlrL7+3q+x2q/mmB/Wuxw9RB2pyKs4/PDvT'
        b'aet7lzSbX4h15nxjdzmzwFLlnY05D+RN1zzz3vlZ3ZrqFe1d1k2ezvlH5unk7+uy9r711gshr48I9bW+/6axX67lapV7s+QVT3ujRyUrPnrwyjc3s6s/+kY5AKoEHRp4'
        b'mWprpJI+mLfwc4tLAR99pym8qNhf98Oadxzfdedu22o+t9Xm/O6irt6ftrztMnckcdEGt/2fXU03k3tGNd2t+uv98LMzG4O18+HTJzm8tYrnxCP22zbpFzrfvxk4L2Kw'
        b'+4Wnu9+LDbyZr2+68brdno/PS9yG9yocfxrQHdveFS9K++uVHJtrLy6Tvxrd9sbpgf/puKj44Z2uF1STNtR1/rxlYKWZpQ90nSGX/pOqj1nER6K/HrZ8oLPliNyD0lIT'
        b'i+MlXc8uBx9LD1xzPmaNac1fZr1nntDvlrDzK8nc29c1/k79RSFz74vlNZV73hj821/7/W74GQU4RVX/MPCo+vhdsc6jNvce0Ykr4Rlb559vveLzcyXo11jw4/urv7j3'
        b'zln23y1euBbWHfZZtvWn69nfhD7M3HLRRulBSpjjvbeGNM6K+y8++2I46r3Vft2GSzKXPJjzzqK8b5Rjt60xFL+2UHfDch2xvW3T9z/9rfvr3Sktsa+17p4VuOK1jtOK'
        b'z5w1fk51P/DGZy8OfHp66cHHmfDZp7Ntg+7z39B5Ev3mS3dvzj6uUFn45YM16ZHOwlc2KO0tOLHu7bfU7I0vq81+7X9iFArlf4Gz9u+wH5mdnHZO62ejbZs434R+eHT1'
        b'25uHLDWcFbxsOz8W2p3z7Pw27vRnF+waXtt0Qr5NuHZ74+tnt3xxe8faF/k/PJz72v3v/ZJ+cAS/yCfBoxZvLgBrjzbf9+fPfUetS7D4mKO2TtJrjr21V17c4DC43eG7'
        b'WwNfLu7/zjUiJnC75OWFesdv+dTudXvb9HuF7k1zCl5cp//yG3M/erTvBbW+lse97T9ZKj3d9KWN2cwjiy9+qxWTsSu6s8Iqln2y9u5d+yylw3M+eW/kcEbfzL/3p/Z9'
        b'73cg5trazHqNw2l9ZrlX2tP6kq1qGs6/Z/CjT/entfVfabXtmV9qUmVj/U2HRfZHXW9af916zHH3nr8d9rd9Z9lbWy++Gfaq/7Zf3MEva5oe/a23PKv0Pce/bzPOuED9'
        b'olf8QcEDk38IVF9cejKCX/mNq7bBXw/O/Lp76492mvE/F73grWL2enDK8Qctugk/f+i7Se/9IuuCnwyNWL94d/a/t7F2EWdbrfkciXrnO55279QXiq9l0TcuOhjeinxw'
        b'fsfT12/Pu947r8prRstpjStmQ0HF3wad1vrs2dLhjYqHN/8E8lI+8mZvjdtadTz6zVfeXbZU4Nuv0hVqf/8L5dQ1anftVy6MuKLV4O2wJlbi++TVl9VXuPfN6v3ELMfz'
        b'fsLHh9IDbs94UmdV+aY9v+wJ7grBW+DkzDJ4YDLWahRqtc+HGcBfgedBh4xqBTfDQzLMfpUXGayqgoNGk2D0vLI87kJw2ogMdfkZyQJYB47Ij0dbcRZlGzC72o/DdlM8'
        b'uTwBQwVbLLhqc2AVGUebybFkHKpc2IJGvBhDVZVFtuzzcsF+IaxZALdPIFFx5iCFXP+Ejx9wtMROyqHixzitiMawGhmGyh+2wmqwTR5cdof7yVS2vf48GYkKHoUdlHw2'
        b'226hHQM1Obxyvgw4le2FkrGXbYV6XLUMLqMG7IaXZbypU7BNypuK9GFOX3WnRmlSBdj1KkOb2r2UwRI1rQFH0XlwXWMicIoNb8Kz4Dp5fiE4AVoJbopDgT02BDcFDsAe'
        b'hhxwcZ6KjDYlAF1S3JRoLimkdT4Go7SpK6CbEKektCmzUoYRcd4N9ElpUwuyKDlMm5IDt8jdnqC2FOOmDiweI04R3hTYBRmSBuwEPSZCJ2P3ccQpTJuKhvVMHdcicepB'
        b'yZMLmoCc4mjBA6CFkbIdsA9ck1Gj4Hl4nMFGQRHcxbBmNpcaC+MJNQrs2ESBzjVwMym7lbawY4wbBS/BJsyOkpGjts5k8ldTai9d8KmmzBhbSNWRojsMG8BWlXhHVT6l'
        b'NhO9qU+w0PP3hzBEl12poAcv8zAGFydwZTgFvvAGsSbZGMGjE6lU8AZsl2KpQBVkTEVrwDnQLXSCZ9TGwak4QZH+T/CCSlSPXdl4IQZBU+FxDazhEzoVZcrlgotoEHOT'
        b'lFMkPLhRwAe98OR4ChUnAF1wnDxH3izI3ilFOAFCxSkDVxOIeBfAZjeMJmFTK+FeBloCaqSMmGOgfh6DW2KpOGEXWDc9NpHqDQWY7RELjs6eaE0DVULGCnbDDEl8LQNh'
        b'AV1gO2FQzYX7iOh7OcFujHHe6TOGodLg6MAmHslQAbwJbqjYgguwcZRDRSBUIbCBJJkT5M4QqAzgBSmAar4UkWZlniyjT8VFMfQpsG8pidYFHALb7JHS6IZN4xFUnDwq'
        b'hGTX2CaUoU/NqEBVjtlTLnA7Y3w7ogx3jLKn7MFF1BwIfOpMBoP52AI7CqSeOZAcgmuEPuUCbzIt/Qy8Bk8S/BQXr7vZwgCoVMEhIojmsF4giLXOkhGoMH3KADQSQXSF'
        b'R5yF8bDDegwdw1FSBrdJet2cbYlSoGAvxnJhxNJlXRJlwVw0/iL4KQ7lCNsY/lSHEmOCBH1yMmfQHtkMfsoCdjAssr2aMeAYbB03Iri2nBSeAdwBjgicQBtsmeT2eqs9'
        b'KSIj1HjOo/t2g80yPg6m46DhYg95t8iBq2C7EJNUJjOoYK8NBx4GLV6EhaMHb4Djz2Go3OFBgqGCO0EbKZi4CiRfMgyVnxklhylUsGkGEYI41MpvgVOlxFsLoVBhmjnJ'
        b'/VqVShmESgOeo7iarIWo9NqZJVG79FeD3Z74vAxCBbZFk9t8FhQxCCo2FZXFEKhAM7zIyPpheD1YiqBShvukCKpZ4AjRRbAZXkvB7UsZtRQ8jXEllpWQTOnDbq49PI5a'
        b'KFl93qjjJxs17DVkBg3g6goGPXdY3w8lf+eoSds1YSWzTGuHOuhViUeK6aY0ZtxQlcF+NuhCL3ESMRvUgH4VwtPhgqOJePxvsQLJHXl5HTMLtLcVho3CrxZxZsCDcCvR'
        b'YL6wSRFWwZ1C5gWpJMNfUSb+XLAvGOwlkr0RHrWUga9gRzmqZEy+Qgk5wcBzTlNmuLbBWddR+BUhX8FasJ1RwjvgmbVwO6wi+CsGfQUuzSH5S4Z73YRI0iZhrxxhKwe0'
        b'FK9naEKL1TH3ikNlwhqCvUIvDYb1VALPwSb88IjM8bwqjpUKEJHEhUWAqtEpOvTS2SfjVYHDqAywWxxtcFhjlFcFL4Y68J/jVWmXkIcFhoItTEkhYTqMS4uiNGAVpwIN'
        b'8YhUe4Gj+JWEWZ5KcBc/miER5aHehAHYwo1Uh9uIKNmAukXMVSi3ZQks1CVoZgfHwkOMFmq3W4XSAw4KxgOqOHGB8Ai5e/6SJKT1zEDdhGmRjeAgKWrNALiTTEtwMJ6O'
        b'mZVoBpdJzLl6mUL0yASV+MWomvfaI42rsYazHvVgWpmpoBakYHbYYxzQXkEcygtmZ8Ij7HWgdTV5J6JXoYYQO5TD/tRgG5M/FqWpw9mwChx44owuUV7tgSsZ9M4fT+2a'
        b'mtjlA/oYQNJ51HzqZMgrL3CJvKcY4pU3PEZyvQ4egvuF0XBvhYx/h+F38HoY03kDm9dhMh4a9ne5MHhFpNnJjfPAdXBSGB0I94/R/TiKoGUuqXywezE4PQnKxVkqGINy'
        b'oRduKxEkXVaFLIWx4CZ5FkMVAyLQLIVybQpFhdY/CcwlpXLB1gAiy/NtTVVIJyAE3GCQXLBxNqmeAnAjYozJtQPUS5lctWAXaclrQB+sViH8KrhrIQPlgmfAPqYMWyxg'
        b'F1FA44lcsDOeA6uT4bUn2MZib8RW4WMcF7w6i4LbS+KY5nttaZAUyAX3zSM6hAFyga3ghIy4egMrcgcnJzbmq56QUrkavRjVtSvGD56At1Ww0GEsF6xeTJpDImpvW5/j'
        b'ctUvZbBcoAN2kXwVo/dHKwPmApfBWUrelK2FWmcbeXZ+JLwlA3OBztxRLtcpZyZpt+E+eEwK5gL7I6VgruUox1guImcVyKhc4MRKSg5jubS0mZ53I2yxRg1pEpMLddaO'
        b'c2eCtmQiPImBbkIncDF+lMuFqVwQ9+xwc7AE131wWQuJM7MxMhfHFxwADK4SNOTLjVK5qBA3DOVKh7vJDGaB3mq4p1jgFMcwuVAXv4HpER+GItAgg281wF0y+JYTPMHX'
        b'+ffhtrC0TjTXj2dtMTvXdac22JEJvp+UpTuVUgP+VMqWkVjf/3meVr3csDzFM/8Xc7LsB/XtJfqOtL7jr3GyNrAwJwuH03Kypjv8O/lY2kfUm9X/dD6W9HFSsIYoqSO1'
        b'LbXTujWzPZMpHXxC0CToZBE+Q2rXvNMzumZIjH1oYx8pR0cU0Z4gMfagjT3+GKVqEvxIvUldtLJ900OboEGboAFliY2AthFI9GNp/Vicxv+ypv5/z5pSx+nGLUFXom9L'
        b'69tisVBrUhtXMFJM0jigSGpXJu0YKLGdTdvOxseUzihhQEzkmcjuiNMJXQmo6DDnBQUjcnKYIYKCEc4UDBGOCk4GCkaSWB4YVOWBQVUeGFTlQUBVpQyoKoSAqkL+eVDV'
        b'srZlfwxUNSLHwYlFwbDinwNyimmKEZW3r6FtggfK76yhI+c1xkiM59PG86VKAcem1qaGizyqLQolZwHtOId2DJdYRtCWEfiwoE3Qze5RoV1CaZeYhy4pgy4p4tSFEpds'
        b'2iVbYplDW+bIrlKQWPrQlj4jCnK47OVw2Svg7KBgWIMyMfs9ICgTs+YFzdliE+/u0G6FYUoO5Tqpf17fPGl5PbZ37PLvCkICa5XJEhWJyrrlxFYpva793n3eA253/O8E'
        b'SfxTaP8UsdVSccbchxmZgxmZ4qxsOquYziqVZCylM5Z+PzQn+K48kB9YcbcCVNyLk0TOpyPnS+YsoOcsQOWPk87BSZebjZKOAtTW/suN+i836s/mRs1j+WFslB+mRvlh'
        b'aJQfZkb5YWQUDjSx+hmO+k8lRv0XFPVHQFHTdLerFcZTouIC/k9TojAuoFyLK6VEcTAl6hleAaD970A8CfGYdCq6E1OOv+BynExbeRdjtrJ+k+zkMB3ZyWE6stP/x9x3'
        b'AER1pfvfmWHoVVCQ3mEYZihDL9KRjgKCIoJKE0UQBsTeC4gFVHRU1EFRB0QdBBUVy57jZtldk8yYmzgxMTHZtN3NJmRjevufMqCou2/zdt97/0jO3HtPP9855557zu/7'
        b'fS/0qKAeIo1D0kQCp5QJeYiwh+ifemCWJn/M0jSTI8AsTQLC0pRPWZp4Ji6jzARnnKUJPzAcI0WadtvtX+Bo8iAsTP+1O5GjiTzPmsjRFIY5miIwRVMEZmiK+O8QNOFy'
        b'5pBy5pC8cjiPklI1keh9HmOCIYq/zsVlHktnVIc8j+dWczGJ0n/SpUgVslW0c0qx0XJ4c47JsgbY4puWKa5LzYQ7fDmMN7jFXypqmACMM9X+fhmLemjH5GdZmAp1CHeR'
        b'wX7LCi5295tqr620v4b0t4pXwevjTeQ9KvMgmohYDxHrJRo3mzSbNps3T2q2qjAu03mOx4jPZcp1y/hbmDLdPr1nGJT0iJ8+8jN4zk+f+BkiP6Pn/AyInzHyM3nOz5D4'
        b'mSI/s+f8jIifOfKzeM7PmPhNQn6Wz/mZED8r5Df5OT9T4jcF+Vk/52dG/GyQ39Tn/MyJny3ys3vOz4L42SM/h+f8JhE/R+Tn9JyfJfFzRn4uz/lZNfMrOGWuW/QLJ5Mr'
        b'N3Q1pZlBsuQhSeo26zcbIUmaIUlaEEm6I3/rMi7BZHk+ME6Iy8xL1EI137vMfUYTFKtiPR2Ckk2NKxI11DovW1AvpWGCA33prwSrJJGroAmJjSFCpWLnuKd0HLUqe4Rb'
        b'QqsYiHwbyusx44Vz7fLyenQ3UUfxKbCv1Ne5fEHpIuf68mX15dLymqeSeEqJEuvyTkjhH2kpTcSlTrjJqsXKaakVqHYE9NpUXl/uLG1cuLSKqFtV1TxF2UH0v5D3AvR/'
        b'w6L68omZLy1vWFRbRlgMUJlrq5eXEwRtI35/V6/EemRPV1DsnFRFVLK84wRaDeXqiYpqWJ9Lq+pIBeGnlcNYi/s6e8cLxoItcJaWY5W7hvJ/JiQsQ+8EAeb5WPCUWqNW'
        b'obC2vqqyqmZBNSac0DIioibAZBrPVFQqXVBJqEbKMWlLNdbupbV3LitfhhYsUudaWnCim+it9YvHPWxprXSiilpp7dKlWBOb9L1n9CCzBNwHvBVLqx/oli5Y2hAcVMp7'
        b'ZtIkoMb9yOkwpmrYBxkyPPTQZMclath0wjNDQ8e8mVNhSsDVPC7T8owC9VodAq7mPQeu1nkOQM1bp6MFV7/QbwIx0fecf4GYaMJQ/Mf6dP9IxRK1D9WunJ2ZoVUPxINj'
        b'AUn3ieSRjIkKLRrYL9a79S6nHfIfjfp/QphDhBOBeU9KF6B5Yz4q0nyq5kgTG0/k6c67oObFGsplZVVUKVab74TOi7t5XWO5dgKQNqKROT4BvZgoZILqcNOiKhQDj98F'
        b'jQ21Sxc0VJWS7r60vL5Sq0L5TyhH6tG4XlZbU4ZbmM4KE0b0Pwe/j2NwnwK/O2ZJ8QHNNzVgQP2N0MZL0Nsg+L3gcqvgjYsbpUzVWv1TPa/TNQVWKgSbysBGMADb4RUh'
        b'2AN7BQAFhy0CcBm0CuABcBHQSOCUKJBs/+dRE9k3guAZcJbPMOtWZjDrgAJQEHfAei6jyCYfItUtVjoMCQxugEvGYAC9MSLB2WImMgPsr/72l19+UafzmcQmC6xml3Eh'
        b'rZ4h0FoDcDAJ7pOszvf3h/sl/lyGH86ZAQ7CbgGXQPLDihKkcIcpbPEB7U0Up5WRJTbw8eYwgXC/rpALB0imVmAn6DcyNsEe3ExOaBSUoxSIOtciuJ8mgeIHBqAUDHEy'
        b'HMY1gu8KNoAOgsddYQB3G+HnkZnYls01jJ46DU+gNLABX9AJtwDFeCq4FKk+dVkC2C9MTYcnwHUxxovlQ5m+fZlhIzlzGobH4H44gPyJn35wA9jDrQGbKwU8avP7UuHa'
        b'9CxsW6ld4h/MZYzXgj1gM3cJ6FpPGiYuM/6Jty5jvM4XdHOr4ZAzSR7usSt74s1hjNcbw63cpZGwrxGj2hqmTIGtWGvSHm5PyUvBAWemPG2OMdFMzxrcgocb8VnSUr1E'
        b'egA3UwQvw53p+tN4jCXYzQPH/ZMapzME/3ww7GndCm+C1JuBksxITxdx66LBUXt4A+yYDC/Ci+lWYEc6PAxuGWGTwa1pOblMeYV5aJIr6TIWq3QYXz+ibJnBzZ3LNBbh'
        b'6mysBC0vyADrr/qlzfKGLXBwTgrcmYsVRtNnQaVwrOMSvY7sVP4kD0O4FZzi8+HVJA/QI2CSmqzgUTgEdqL2Jjiuq8uhEg6YLasHN6xRH4FDHE/QD/eR3jPPLdJIv345'
        b'UMLrSPo6HB/+HIKib8qBfXDAuK6+CW7Hcfo47h4xxKcwDh6VLssC58F2uE8HG0mf7xxGTTBvhYfhdWkdvGgsjsORNnDcnYES9STsux5uB71SeLmufroe8gTDnCmwH7RS'
        b'BdaD09eR3OAABriR7MDJ6EZ64G8J+yZKHPYt4S6Fu50ag7F/8wJd7A1bc0qx4GFzpigte1bKeAxtk4INcICBx6uNgEJ/LhlhoLXWj8Yk8bbANm1chnFbrQP3h4HNpEOW'
        b'zFueqxULmokM4CbQyYE3VoKOqrQdBzlSDnqv1nKXXMqfu8QyzurYw8yLV6v3Vd8rOty762D+8Fy/SzlJv/mZY/H4t3/ZvPmgYP/exPZAo99eEcUdT1QarvxDutNPm4/1'
        b'vfLmoTdTr/DnzQ6TfHn08zXSV95887vCn5OrJ70Bs2Y7vLXF/vYPH//5EnyjWea4eGbkpzsdYiMX1lwYeP3wjqZFni3bFR3KhIHF7IZlky6XFC68awAvtScYm728i7N2'
        b'gyN71E3guPLlk+arYz/NqJYMTp9j+ZrNO5urboYv+Hz5ZM/7ih7F4r97Vo/EprMnJYM/QgPfml1//3PhG79/6SXpSNF8PdMmV6Flmd5XNq8avLpo8vruT3wPn1g29/U3'
        b'm66KPv9hVH/jzfMFMZXt5/4y+lu5R/npE8k/lsVlr/jkvfqDLzdbCI2Mgmb5Z2V9ZpAffOInwSeFk278bYls1STezgGwLat20x+SJ536zHjNYQUoP+e+7npX8ulZxx5u'
        b'FLcPjhg+yP16y+n9rbtdCr/RX/fltvA5sCXPxEsdsfUN0M/KbK4lB5/Jfb0z7q997e8V+cAT6tpUDbtV/Z2Mf5N9Ne7Yx5lvmhgOz+/LmPxRbuCr/l8eUQs0Z40dTxbF'
        b'/3SnoKPS+o5+kEg36ZO35hSXWf+2b/niN0Ikuu9ceyWyaObfDd9yEm2L3D371GyfdXo3PyxY3nn8Petjm9fM2zt8pPAjv5ONHof0fvqFW1QQfH5T+18ftA+dN5r72qCv'
        b'78gH38jvpH+qe/5h4l8PuLz0qd69t/jlkkfSyKviV+8l2wd0VSf9fai0+bW3d6puLM5zSHwNZIl6b6fd/a1/6U8feld6XN6xs2nf26qjgQuDW8L6fEb1Rsy+6bm4/Ter'
        b'3/6ke7HJucWypZcOsup+ofr76R2z90XdE25c1Hen8O5vle/+XOrhvy3PgB2tCby2fdGtb4zyHlqXfnl04+XX0263WKSclX7fYvFw+k/K0w+zbLtiVs1/v6B22uqfD/xy'
        b'sMvilRuXZx24afl9bV90zOMup2N8R+c/vp07Wcfxm93Xz/y86eKZ3Z0da1tf+ePOH954NeP9x1/d5n1p+Ml2cCzD9HjO37dkvAPeevfe3+w1j0YFcRSNOgwPGwrBTRdx'
        b'JheNcQUn3bGQ4AmM4BU0Y7SCC+CGBZ7b0IyHT+6NwDAa7GCPA0XeXQOyZULYV5GaoYdiN3Oiwb5gAhQwNJtNoc6guQZb3cVQZ1vYTnGqu8BhCWj1Az2+BeBICp/Rnc91'
        b'XQKbCcRh/TqMgoQtftmwcxpWC17H9Qmze4xXBLDLwAxFw6jYDDFoySYoX9Dsl+LrA3cXOaPXgR5TghYE50APQ+G6l8vhgWdMEWOcB68SbIYXSXaToHwqBjugCvYFiHQZ'
        b'3WKuW1EsxWKcCMpLzwYH40SpvhjAYwQGuXAYnARnCLxF4AC3Po0Wz7GmVpCBYhEFdKfBfUZPaYOjBcs2rUZ4TS7FX17wS9ZCPQjOA5yCfdyUSXAz9T0JTodQtAe4BuTY'
        b'DhuGe2RNoxC068i/TZgKznnHpnAYnUoO3Ab2UfNx8MwSZwxaIlgQ0KY3BgexhZ06ddjaHZG8C2gDJ+FABn/5mBnQ8mwCc5kH21F0v7TMdFEa6IDnUftlaVNwhx38SG8J'
        b'qd8S59lSuCsVSyPdNEu0wgYOpnMZx2QdcGpZIQV+3CwKwoDmPQZZIuJpkkRsr8Gr9dkE5GNiNhtllCXyzaR5NJqQXJwDdOApuKGGQrIPwE4jqRg1fMcE1Aq4WUoawnJ9'
        b'DWjNxqaLU9FyyHRRFLzGCxNQvC/oMLGjywWK1WFMgj0zeHr4zUwLeBy1xj5iknFnehp6G7bqMboGXGP0mrtFocQDcPsKKVrFoWVFN3rdLuGsmbVa24fh5vUUrAo3FGqN'
        b'pYrgDVKm/JRyirsEN/XGTX9esKa4y931TgQ2mMZHGe7kMXx4mAOvRTRoIZWN4JqROF0MdkbgmL0cVMaOOIrtugm7waFnwajwFrw1ZhQVtqynxnJBD1pIgu7MpzGh2+BZ'
        b'2nPOWYMrBE0KBrOIVVMLTnG6gPjFZC/A0MEdGVhRTBflf4QDdsenUEEMgpOzcbX2CGEn6qjId4ADzsBNcJDAfybNtME4YxG2Fk7s/rq50Ar3mC/RqkXAw7Mz+ajC17gc'
        b'eCaZtLAdGITHpC5GTynzwWGKADsJrzhh0YrAxcZx8O4kcJ4HWxeDQxTrtQlsKCX2NimuUB8cXoVmKdCC1rPnKB4drXngrQmqIeIlTyuHHIE7STGTYTvAi2C0WoM9sAfb'
        b'273EAeeNAmhPOi5Mp55kKafLoE9rKOMlzQaHH2NCE7Sw3pMHWpuWw0GTuieLQ0xB6Ad3p2SCW14iFCs3Sd90MThFZh4d9PFxVio0RMt0AYfRW+thzQ0qobhdeBLIi6XC'
        b'etrd9cpD0Ho80M2BVNnQpQRVOBVD+7KF2Oh2EjzKZybDXh2LuQyNvcFpmhFOlcYGvT5LudGN9hQSuQ+2ccfiox6qx5hmAQW8yIudFEnfB706k6RwwDMNGyPnwCsc8xqK'
        b'igMXRYuNBKAbbNIawATHqX1kX2+4leDtYBccpEYwtYA7l0zSMXTybaVZQnhqzFA2H16mwOVN8CbcjhaY5gTmik22wqMzCOzaEGyIQaVEhUhFIzOpjMw/finYTqYbPM0P'
        b'tQLXiVjEoeCCNEtQ1wiOUXWYdA5j7sCbCfrn0yyaQXe1VAB7Q8YsYMNeeJ50PHOwq0mKm6hsHZ/hga2cVU5giALfj8JTQC5ME6WLfLLQnGJWiebAW7wFcSFkGIbDDWhG'
        b'Hi8chUWi91WWHpfPCIr54AjYbfzYhzQZ7Mic2CkWxo91i+wQtDKOBOd1s2LgATpQrsGTFkS3A1yBx8aoNOIBxWsuhAPpRsSQ+eGIMf0mCzTXgXPYJDiJfzkJ3hSSNw56'
        b'kenD6/oruKAdHl1P34X7GfEEeKCu0ZjRzkvwuMDuf8NQyb9y2oXFOmFb4UWHXoQwcvLTO0kTKTJf5VMujsXxaGp0bIuQlcqD1ZYC1lIwyvAspnM0tvbHPQ97qlyih6S3'
        b'E9S2KaxtSltCW8KjsedRQwtvu6ltk1nb5LYEzZSpbaUyN1lDe83+mjaexsm1TWe/scbBubPg+LzD8xQStYMf6+Cn5LAOgfcdwu45hA1Zqh2iWYfooYWsQxwKbIjtxhVS'
        b'JBwNTB5aWrOWIpVlsCYkYnDx/ZDUeyGpIwJ1SB4bkqcKzGtLZK3Ej5wjNc7hGueEUT2dqZNGGeS08UcNGVevM3Yn7Locuh1GGQOLKOK0p7YlyKw0rp7t6ehiykNrR5lU'
        b'njBGI8Kf7Khxcutcdd8p6J5TkDJX7RTOOoWPMpypIo3AV5bYmfbQ0UNeimrj6Mc6+sl4D128FZaKCrVLMOsSLNPV2DjI+KNGKJmvTBk7D5VHhNo2krWNVFlFaqbad9q2'
        b'6WrcBN1RrFtQmw5r7qzxECriuud0F7EeIfiBq8bdRxHQncq6R7DuMSr3wtshIy53wtmEWWxCIQ7gonEWyU0UFX01rFiL2SE0pQ5unSWsQ4DKoVCZPxQ3OGdozUiFOiaP'
        b'DZ7FBhfStnWTx3XO6SxmHcSsg4R1CENhh5JvBwynDmexUZlsVA4bNYuNooHtXeUBnamdWay9H2sfwdpPY+0TVPbLbi8fWXBn5Z11LAa9lLPTl7DTl6HwBk8l7k8Tx6k8'
        b'cvFScLqndjuyLhLWBT8y1Tg6oR8jFB7jMSXEaUvS2Dl3RnRGtyVi0IBBp6nKJlLh3ifo82V9Im/r3DG8Z52msk4jLCez1Y5zWMc5Kps5GhfPbttRhjt5MYe6Mr6GoK0a'
        b'O9ep7cSsnVhpcc8uUGUX+NBVrPJbpHatYl2rVPZVozzGXvLIyqYtfX+6XIL+NXav6orpjlFbBeJHbekaZ0/Spq5+cpFSV1k3aMD6x7L+01n/jJEytWsu65qL/M20klDm'
        b'9C1mxTGsOJkVp4/kqZ1zWOccHP+RnYvcpTO8Mxp3OzFx0Cixtt2/nLX2Yq19WGs/lSRVZY3/NCKJIl+ZMDh9MOO22x2vEc87fmpRDivKkemwNj6oXp3RrJ1IOeWeXajK'
        b'LlRj76yyF7P2YqWr2j6IXuJeux730wqORhypWDqUMJw8nM5GZaiiilUzctkZ+eyMOeyMYtX8MrW4nBWXYwgI7a0mjE0aZ9Sc8RHjweT5oZ2bPFGeqJii5PbZ9jlSVJba'
        b'Lpy1C8eV8CPOszVRxqis49GfRhyEmiR3sGCw6LbkTuhIyJ0YtTiXFefiighfWBHUw/yUgWoM9MGXuCJrcUXKOBrfcEXmkNuw57CQjUhTRRSNlN6tuFt1t0ZVvFDtW8r6'
        b'lqJKZI5XIgFXQuiHK+GlcXCik8fUUcbIIpxYZrhvLbxnLVSkqa1DWetQTKOTzXno6KXyzlQ7ZrGOWSqbLI21CyElcldb+6FaYV4eH42L1xmHEw5dTt1OMl00wh28ZIUK'
        b'XaWVslxpTCcwnJSPxtVbboO8MQRQZ3I4cWQ8jaOPrPrJbIFmxc4V950C7zkFKiPUTtNYp2m4qiWch65CuWDE6u7UEfRPlVfA5hWp0J/vPLVrMetarLIv1gSHyXQ6DeWS'
        b'7mlqm0CVTeCoNaoYqd2o6ViGT4FPLCj4RIFRGT06/zoM5b948+A3yxOunn/1fZOqj41oMZSoB71ysuM5HI4ThqH8x53/FKyFwHFOGIQxQ6Zxurz/JFHxxCYaYyk+h6kt'
        b'nrAUB4wdyJITTV/n8kqxsw8+VBH7B0vGqOafJy3+teXs4f7acipxOfGpNC2nHS6n9vTPuapsQol+RWEWocL0cB7ol5TSw+FfV6YBXKZL423nQnhFCZlmhTNJELPj/jdL'
        b'tgWVTMB5YFIyfjRaUvUri3cZF09/vMk845wba6rqGstfQLL7b5XRuGTsIOxXF/EqLuKk8SL64BaUNqAmJIds4+dr/14xK3GPM/nVPW544sgQ59ZiAww1FbWE6Nh5wcLa'
        b'xoYJ9hz+nU5Yf4r5teW7NbF8dnkT7Q/8NwtDhmffry4MwIU5P14Y2yeFiU9N+Hf6V33/ry7Lbyc0TP0A8+vnJw/Or810BGfqyRlrAO+8F1ilGCP//jf6MRpuhoTFuARz'
        b'Cv+6Iv4Rvw3x2dkGRpbXWbLh6Y5DqIrp5PXvlU6flq6h9teV7ZWJU+lULe31v1WiRWNT6MIF1RjHUFK7rLzm1xVLPXEKDcPFwqnQY/fqp9E/z/Ko/5ulNh0vdWl1rbT8'
        b'1xWbxcW+x0woNk7m3yr2/72Zty3Pmnkbb8mngAy8rKqaVke+FO8Wqd74WmuuLW5nK0d309Sw1zieO7gfHHhbwCF7VB5gALSD1uwZZk/tUnJBywzY+gI7bV6YHNLqmZVm'
        b'dXmNdmPDjKEbG9XJHMbGfv9qlbnrrzTJ9o8zuI/HbiWjRV0vSeb8b9hj+/9M/M9Z+XuR+HWy8qrMTl7VkeI23nzeDcvfZWuAbKPEhDG9yf3p8Kzeh1Qgz8t3FecFXxIL'
        b'a2urtQI21gq4ngi4reFXSvefJP9ggnjr/g/EiyFseER8uZcZg7AhAetoIWz6zRytLREKYmOazbQANi4S/TP2QtbyDF4gzOchbUi83HU8rehf6PePRY9FIXlG9E5ZBKHh'
        b'A/pSMGwC7gCHjLXACaAEOwh4qDBKh0FtbfNT0vyMyXP9KXcm3ABbQbPUtB6eBl0GOMoJjhjcqCdAk+zFfBzD/5OE+cbe5QFMoz+Dd48DQSs56KGszZghfWc6usjCpOk5'
        b'M3JE+Vw9f6Y4Vg90wTNwA0FI2IpK0tNQ8G1AhvLbTQ/x8OEan/Ep5YOz4EQ2RX70gwNALl2WBc8V4mMVDAoBmxMJfmNamGicYULLLqEEx0CHDdhNqrJ0MdyPD6HSwQV8'
        b'VKvH6Ig44Jz+NAJPWeYEhoQCH79FmXyGUHq6+5EMRQvBVe2WOtzJEVsxZpW88qV1eQQi5ApOBZKNa1GqDmOgxwU94DDYDa6CdspXf3oNUKSn+uaZpqJEdTjgOJQtIAyJ'
        b'1oF5+AhWINJlDMK5YXAzOAVvhFOESo8+5jsSp9WA7Zk8hpJMnUgkNTAAt3xgqyiLnDbqzoNdS7mT4VawvZEcsw1bgv50uDsVnpuNTWJlwFbS5JR5WhjNh7tK+BP6tdFY'
        b'v96J+7XhhH49sVeP2cX53+nRlc/2aMMX9GhRFum07e46TJiPJcY6VU+tMmNoL7lgB29RliUeOFAMrnPAbtjjRjA28CS8FUY5KnhgPxzEFAqYwP8KpaHsS3V7Im4kbCuw'
        b'mVeeDk8SgZoUGEsJdQVvCTgC5BwkXniAdJ85OVAuzfCDHXZoiOhzHODQLEqFqYQ7GzExDrwMD1JyHEe4iQgzvR4MjDED8eBNsKOKA46EgxO0F+yuANvGGJ10HNNgJwec'
        b'yI8j/dwHnudoKdLImRU8AHcRQqduMcETNuK1Uy44FZrL4NPy4QrGBSrBTgGf1rA/be3TsaPBARy5zpz6DoNb4PQYt5KO72Ig44Br8FxjIz7LgefgZnshbH6azwl26vEW'
        b'wmPgDCm3oAFcqc+mdFFarig0INoIY20GGhwHhChfscAnUyzAlO0X3ThoEG3lh88MotkftQan0jO03ExQAa4RfibzQtool0GnSEv+wWHAGV9dfa51nLAR259FjTAIdgpf'
        b'xHGCMWhthENkozMZKfAaOA0PEqKZDHKEjicmsIOMKk+uQQF/iQhcbcQsKvB4UBUGdYwzqMxLfD79LLBRD2Ugg8OU6LcD7FpIcGt4emLgDc78eeAyhRS2poPtSxyenaU6'
        b'QuzJJAi31tNZkM6A4BBomTgLNmjn5JugU0hmMjqLwaNcNJF5BhKqVC/QuZKS9Og4FmG6qZNBerRce+ZItYw0OtPgSV8OOFsFD5OGjYF9oG18YikCO3XncSfXFlG7v7ZT'
        b'tZR3OiGrUJ8HPfqwj+RUuwB14PO1qA9zGE4YZknuL6OdfiO8uFqYKUJDTGdBImhDsynsMKajbz/sR6vKdjHqYiki30zMZHiAu0ZgQqyAFK+A159hbQF7vbTELVVQTmoP'
        b'9sRXjgXiM+C8L2FSOuhMrKvDg3ywH0+C2hkQbEp+dhIEWx21QEF4Kxq91VrhxeVNmToMByoYeAacY+jcfdkaXgyFzVLYr4u5oBnQtnI2GVmhYG8Q3Ice+oorGF/Uu+Xk'
        b'XbjO1YhRpYgYxnx+xncJPpRd2KeRyyxzxy/k+cbStBD68MZCPhMbMhlPWcaBi5zow0IdY2ZFRiDDzJhvvLLRmD5MjDVgUqZ44u1dX7NFcyeuSrhjkyJuuXQ0h+LPpXlo'
        b'wbmGs4xTxuQzBzkcZqdB2fiHO1mMcQn57wPOcimO70y/l743iKosrylfsax+2qqoZ3eLG8rrS0qeMP+SewKrfooNeCx2uQFaq+Hh+An6t4FRJc7Hf7l5t2fenjPirr19'
        b'6o+iprGZFHAeLRPOYoAkGpH7RGJ8RG1om+qbNnOGKD/liUDHpQkGuIYcfObdazwfXAdHKHFzLxqnx9EEbjZPIEKLHIqQwaPEfpYO6At1rZox/Jgjnc1jmFe7S28UpGe/'
        b'FWteHNl/9M7KW84bt4zqXzgwrWtZ7F+2Jnjs7vD5asOqT0IUyfEdbl9tWF4bzfosvZqXEv3hjA/3On5vGZn16aX7hzYknXLdWFl589Dnb735xbYf/fe0xJ9veS3cteD7'
        b'3xdkdX60YX5MwrcOLZMLOkNmvZJ3/3Jwb32H54r3owzWz5rtYdNvtTEzcKunneuV2ti8rwq+NjpQ5vO6+Lapf3787NQFVTe/6lqbvnv3t4kh92UfDfrCktXXUy7q8D4s'
        b'4jcKYnR9V23xEPUZ9/rWXA4/arI20PThx+s/0x89veadGcvzZ4dv6beKc7NRHEn+y0drW/+accVwUfFLL0d6vM0kqr9xat+39tjCnjbDrYc3T4pb98HKS0fu2uwPKBp6'
        b'YF6x3P2jfJeDej51fzl/ODb6kx7nHY1nI/526s04kw/Zc98HPXholPjRaEp2x+u/fTP4A4uKH18x6brn/fbDHz/IW7Sxp73l6nd3zy4yXff3pA8+2PzmEes3lu6bM6nQ'
        b'skll+/JvLh34nf2dSbFnBX38mTMruyZnDwzeeOlenMN1/muB1l8rg87pvJ0wVJn8/jvSB9YPZNf/Uue34w9TD/QXjuw2jr0fv09f6HclmjfvoOqrgIhSUVe07MsTDkER'
        b'nycdrPQPdj+9bXvxoY01aZ+c3l6cdMh6+BNb23mPT8wLevD37wfEJ+yaT5zYokkUXrqRNvfmniNnzq+v+jT03NL2xuzZ35wRfuH7xweRNcWqjVO/yQl5xc7xRr+7R+RN'
        b'/jcfiV/97cKX+YWfg/VX9QwdU4a/mz383foPtzbVplbsDXi/r/kr1Tf8ypeN+ja8si3ynENVYeT2dySjxYKvs0fWBx3NPhhzTe0XuG7U5i2Xee2Tv3T9tGrj5HK/edF2'
        b'Me99Jnj/RnfFYGTo69/xGj8pTHnLsq/ig9ceO3zQkBC+cGp26Qf2fwwP/Ovc1+c5Zf0475uWxcXf/FzwV/BOU+3HH3j8WPPpkr4P3t0uWSV577uolm0dr8R+7TZv52vt'
        b'99vFL/35R+nIm/r1ivD3Pg8tX99XaPLN0a4jx+UfTw+9WfIze7w2rHVzdF/gQ/BxybEfXNaAPXfODMeDd3krDnWcqzzBXZe93WIk+mXhBs30H2fl//ls32K7PtAbPTlv'
        b'6erKmM+DVv1hteq79O9Oj9q69X39Uaziwg3X+zu47+4U38r9+97u1es5P1qHgZAqQTjFmW2o8cfLDKBAy4gQNLqPc8AwPFdAoDcLQuE5I7hDYLAi1cAbfRmgZbAFOMMD'
        b'nbCzhkJZDhSCkwXghJGPAH2sYAScvh03Hy2Su7QYGDnYmJA7RseIJg9wsYyCDzejGWF4jIyRcN+VcuxywV6t2XlvEwI9xMDDLPRmhtvgRnCEZDmlFq1ztKSDPHgMnoAn'
        b'MfrtMtxLEpaC05hdany5FjodrdbAEDxPISwnA8B1XKPUugw/gS5jAncu0+N5RtdRLFdHBDywDFx/IR8jJmNshgpa7WvwJNiCMW5QBgfHEHDoaSuptgtQzhqjU2RspmD8'
        b'W9gaAlVaB7YvMvIGPbZBOgw3jzOtGNAY4Dg4ZQ13hoyxiqL1nUUW2d2pQbU5ZeQ9xviJFps3KeunRR6V30CYQMuhyYMtQXAzWkjAc2CA4g/PwJ1LpBlYNmguTkdv4R57'
        b'Q2MukGeA07ShL/nHYQ7CHb4YoLZXF/RxJfCUO0nZBGyFW7O8tEy9WpbefHCNYld3upqPM38y3uCUlvnzkojionrg0CrKGsossKGsobrGJGYk7IZbUQPvwFM+WqyEJ4Bd'
        b'HPS5OMyl9IttvgFNcGiMrVTLVbo5kUIE25ejvnWKKLGkpsIr6VxGr47rA28ByoAKDlkXVGdpKSMpX2QuvEGiusJtelK4U1RH4XWgf5lhARf1pNNgG8nXdik8ZAR6lhGo'
        b'WL4bHxzmwAtgwxSKTdsITnNx7Dx7iiMDvZQ1FC2Y9lUbpWUKddFHyjVwaR0HtFvDK6Si0+Y0oo8QPdgrNhCniw3xyswGXNIJrVxNQLScafAGWpR0aPnexpkkrcAuHtzn'
        b'Dc5T7uk9mFMa7AcXX8D5yEMfqi2pVB5npoAW9JE5xpKo5UiUgA7a7/vhRp8xZjdU1MME6guuhhDoVmwg2DHOuTxGqFwRiMHIctTjCT5x7wo3OiIoYWUGPEU5K2dEkRZa'
        b'BXcmGzWaGKAx6eKCVrNxU8FJknMg7KjHLKAEn7sWXuYnceAu9MFwkAgM7ovVsvvx4BWwCVzmAIU/h8rytFcDPAJ3aqmMGYwiRGImBHp7nRcYjQEB8zF5Z0w2aYX563JQ'
        b'mfePkwJSQkA015ylYwVlAPZSRkAeHFwHLnAwqWoP5Q1tQTncLFr4HCcgDy14tvDJ8E2Em1HXRJKM1xL39a4hiGbYiRpqK5IkGqxDE9j7KHXfukpSJeNJsIfy9qGFajih'
        b'7TsNeqmAbqJPv22wpwwrVqFuiCqtl851WUqB3KgwFxgtnyAPHkrENIgnUIHPaWHe8CxoGSP+ZqCMouGzrCki8wpade2Hrb5ZaAKHe1AACxMjNJTheZM6GmDzJDvivVMA'
        b'm1N0GHAi0gic58KT9aCLCqkdKMEQ/pzMqsXcqV2cGeCUEQENhqIKtwizfdFobiXw+CWYvfomF17JhRvpzHYrE2Dm9N3FAE/0mZwgcKOeYmt3wosBz6CnveEZnh48BK9R'
        b'nPk+MTiAVQSe0g9ohAqqIgD3wRMCl/97QOG/gvxwYZ5lBnwB+JCs8B8YPlm3rxL8y0t8srWbij4cvqUL+tHEFA7jGzzK1HIcfL8grlxP4+F7puhEUVdxd7Gcq3HzUgSe'
        b'iJBHaEQSebLGN1CeJE96NH6t8QlgfSLleo/cPOSLu6eNomGdzFEWDBbTK40wUBkylNwfwwoTWGEyK0xnhTNUwjWqvLmqooWq8iXqoiVsXjWbV8vmNbB5TWzeGnmixkuo'
        b'aOhbec8rTOUVpgmLHlqu5Ct0Nb4S1jdqKP92+dVi1jeD9S1gfeeyvvNHGUY0l6sqW8KWNagaV6Pb9ZxE7hcMsxz9PGaYck4S/ZlBf/Lpz1yunCsP7jLQiIKU+UMV/SWs'
        b'KIkVpbCiTFaUoxKtU+XPUxWXqSqXqouXsvk1bH4dm7+czV/J5q9DEUO6DEnEvhJCxpWAYqpEpSPTVXmFd7PZjGI2o1QbyidA6dnnx/rEoXb1D8V0OXHIJ7zLROODm9pX'
        b'0peNqd7iOdRFtff27TNQmClz7ntNu+c1Te0Vy3rFjjIcj3iOxtvvgmmvqbJhcKXaO471jlN5x32LUlWidMSKlX2ZGoF/nwMriERl65vHimI0QvGFsN4wFK/PlPWORMGH'
        b'6ifcjPJ5wZ5fMDxfr8fY+UaX8RadaOxq6m4a1eP5ho7qMpLQUWMmMHzUzjTA9QsGOY+xQ6sw6siEThuqHNFVT8tiQ7LZkFwWM9jNRTIIjeOqSipUlTWquiZ1ZRNbsoIt'
        b'WY0afj4nDjd8jNpZogmJHqoYrGVDUkjcPDakgA0pGvOMwubSyn+TzUblsVGz2ai5bBQWdXQSFrWqWqpavlpdvZotW8OWrddKWc5VuWGyvkeoFZxYwTRWEK8SzLxdeWeJ'
        b'HENCURu6FHMUFX1L6JVGEo76puew8PbykYo769SSfFaSr5ozTy2ZJ4+Xr+jKeOQl7l4j19GERrKh09nQDFVomWpGjiq3lJ1RhvOSqJ2DUEujdmZFiSpRzgh3JOSu4Vjv'
        b'CMB9I+7J3VxWFK29Ewf2Le6rVYkzbk+6Pf2OHXoa2mWEw2CZqUSZtwNvV9yJ0AamDIBR6C6oSx8HmtNXrPXyk/St6luPbsK6jB8FRw0WDZawwamq4LKRAkysWMJmonLK'
        b'p6mdA3HHcESt4B9IJYcGMC4Q6rfTWVGG3FDjJsKNksnRuHvKV3Zn3ncPu+ceNmR7Pzz1XniqOjydDU9Xu2ew7hkq9wyNXzDmQkvGMYjJeuTKp0+MaT1sfz88/R6KFZ7J'
        b'hmeq3bNY9ywV+cN5F9HcqItmkQlxJw+/OF+ctX+wkq9cODR1cKnaP5H1T9RWB1ePFUSjGoZGD64cXKcKnTcySZVRxKbOG5eUm4fKM4R1C/2CsXMp4QxpoZsz5qmi5qmj'
        b'5o2aM34BqoA4Vhx/X5xyT5wyYqkWZ7LiTPn0Rz4ihZuisse3z3fI4p5PhMonYmwk1qu9I1jvCJV3xCiPEYqfDYZ6kKKue9V9r/B7XuFqr0jWK3KU0UMj+bbeCOeO4f3Y'
        b'nHuxOerYPDY2jz5HAy6ek8oZsbhjO1KgmpV/t1DlPU2hp+T0GCqnD8X1p6ERrZAomnqi+qKGAu4Jo1TCKI0k4krkxcj+6MFoRSK6YSVJrCQNNa0IzRjRcUquMqTf8JGX'
        b'j1yqCO1a071GWUdn1qHcodzb1jirqyXDJaoZM+9Fz1RFz0TzyRBn0PC+f/w9/3jayKhu03I4mtQZqpk5d23vp869lzpXnToPNS71eRQQNmQxaDtUfy8gDjXh7YKRmXcK'
        b'7ycV3EsqUCfNYZPmoIeamMShRu0+0ewS5KoT57PIjZnPxsxXcFXCSLV3lMo76pG3GLesKnQuFiXhztMK8gseR1CCyYSQO0pdXUYY2CdG06hPQJ+wT8z6RKt8Cm5b37Fj'
        b'43LYuALiwfpEsD4x6NLNB3e3dI6ikv5qwmNve6nC0tBgX6t2D37kHaowU4WlqLyz0d9IPP2V8x/5h8r53SYaT6HcCP/rMhot4eEXJX1pPm2v8YFBw4qy8oYFVdXSB3ol'
        b'DSsWLpCW/zuYUK3lxqff/vR0NZ+PVtL/+lufh3fxDjMEGore+QkpHA7HGZ+x/vvOf+qQ9ksMBT1mEMQMmsZxeQIe2ZB2nT5Ta0EF20+JtubySiqo/nVHNWxJ16pdmsNT'
        b'43pXtuCkDloItsLhRrzenukJzqLbPWg5mwr7wR4R2JGtTdApUgfuDxcLuGQP2hXs138qK9AOeri8OthDNyG35aKvEm1uy8CxZ3ILbGwU4k/2UPQ1uSsdnPNOyRSnZs5c'
        b'hrVtZqZQ+ntfDtgxg5k/Wd8drWb7KdvBwcVxTymnSwSM8XruUnAQHmv0Rt6L0Wq3Ox3uEnmDnjySVgAcAEeCZ6ZoixnhrsssHzvWaAOD8Aw2qoJ3VdEauYDm7v3k2HUG'
        b'2MoUgcP6Zv7wAmlDF9hZ+6Rt8p9tGrgXbCImsuElf1fpM6nN0tqXxpXbBXYboK/+ivX64MTCKWQkVF3XydWROvIY5tMfXjqan1n7Wqz5w0b735W0WIZWHfZcWnizS/Xz'
        b'Rkdh3aPmLVsSXzc8t+laR/wHedF5f+UpJpn2zjCTF68a4dT92em9bWFuPxtZ/u761y8dcVZalTdFff7y3SNz3irxcfqxUv+kMOgvOXcuRDf0fP6LoUWCVfplJxfHczuD'
        b'u4du/ubz5E/jdy0ofBTZ++Xk3/wuIMLb/G8n33330J9mmRdHrGjM6gwyFfQGVOp+wLz5TvPOd0tHg/5+bHPEay95zDK50zZVlrxz3rf3VQrToopjwiUep/J7dT9Y79Zg'
        b'+13lb2Uvv310Yd/6P/zhD+XlHlEhV0yCN72zak56cubqXs9Hnd2Hg0etDucUbKz70JCZm7XwgPV7urN+f3LvN/pGdT+C6i1xVZPcZpkv73A/4TW7d0fz7g+6KkeLN11o'
        b'uX5zJL4yYl6O8uXP44Pvb11898Jr1078wVWoayoEPYuXzQ18bddVi8X1Wwz0Ens+7J095ezp2YL9nL7j8/muQZ5v5H343pIKne135UKjQxe/mfvLe1d7HxfJ1kalGkWv'
        b'irjgX7jjLzPdCncfnhn5l8SHI3tCVoXMiQiFe7uL5n4yH1idj/88YsdIyNtLJLmfvZRR6/vJp7bv8qc5F2YcXKubVGHxU9hHJn/7Of/T0nuNFv3C/B1eRncv9Vx89YMF'
        b'ksgVkkN7B8/IO1NDdXICji7snb/t4/etzmx+NSrv4itpdz+tmj7/hx0x76lmVr3UuTnz5rYfds0c2N7yR9+P2r5vdIm7drfss9+IPrsfkxewcfdrr0l/+KAnxSbsT77K'
        b'tLWqm3XnMkvvLvro6yuHwov+NPUnE5OpCwUJ2aucRK/ebJwf+Nnow2/FOUXdglLxF0qedFV2A1cS7TtwsbfpYJh/bMI3vfWP1h0WfurYPO/QtLsn2aJok7Y9U36IDZ67'
        b'Zu2OTZ+/ecO2PStv9kbTWZ+Uzmza/uofHR/8Yr+q7kz0nNauvs/SPjv6mdoLXLGT5NUPTPp40kjGuTmn10n+mPQ4qPbPPQ7rl+h8+76H9M8hV3Y3tb2/99ZG+Uu7Cvwv'
        b'LQju638QebTv4l/+/MF3n5+K8pX+fPFH32mV1kdWLH/wIDz6betPDEu/jbj+rcGtd3Wip7/xndPstabte34W+D/GTCn8ZYn/RGMTq2uugQewxiY8oVVcj16XhZVAU+F+'
        b'up+HFURhNzhCdy/22YCjeKt2ErxJd2s5YDgLKOnH9LHF8BjWVKRqijOhbExTsRXsI1/xHDRDNeNN1Rgj7zF97u18svVhM61Gq8BabvScdbO1OmQDyK0cXsZn6gbiEnj+'
        b'6e0snejH+LRttlUxsWpevYi7nBMHj4/pYN50Af1SsqkGDzuRrbP9sI/utl5OWaf9/D8Dt8F+ohk7SK2pwA4dMGgJ2skGRWQM2GqEJuHdVAFzMehljCy5cDPoAUfJLpwV'
        b'OFmJNeHrBByG3wS6nDiwE171Jn7JqLGOSAUccBHKtCqa4JQ2YT7cAi5LyU7knqwmAWcR6GQMm7jgbCygpm/cveAuqcAA7IrGmq5EiXMtlNEtwWugp9FIjIQIt5hyCziR'
        b'ifAIpSy4UtUkzeLAPtHYtlUfVNI9us4wcPZpJV+pgDEt4yUVcekmT58BaMbWx3aALjxdE6NTmzhwmAh4AbyRPmGPbpmJ1uwZR2s3C++ngm3jm3z8teDcMg7sqHImMg4G'
        b'u2H7RPMNYC/soRqaTaW0gNfypBP2n/DekQu4MGab4Sa8Ca+NbbzpTrEAZ7mua4vpjviealcpkuQe0D8da9HyQA8H7AGXUUuT7cOBeHxEi15kibATIxZ4YJADDsE2eJ5E'
        b'nwF2cI3EmfU4BOhpEJSg/C2seIsLS7Q22+BOeAFvz9LdW30TboRTWehKIsXZ4JwZtrqmNbkWPkdrdA3KUNPhcTi/2uUfsjqQTSvQWUNpHc4BqrdfCw+aPNkshh1gI0N3'
        b'i0+BIboRfaoWHh3fLuaDw3ADPMuBFwTwDCnwKngNbDZKy3SDZ+nWMAe0w0uQKhXDvfAiQQDR1YZuCepLh7k+oA00k20va6xBP2HXC16BvVpmDLgBHKe7fp1QicERaGWC'
        b'Wn0nHtPZHLghZTYpQHU2PI5VfdF005cypuoLlXx6LLDXGignGCIs8ibUEsvBTsLNkYiWJENjW3PeUaTHEd1nm3Id1zzQQnfqZdOSsJoyXVzoh3HhQWYhPNxA9q11sS1m'
        b'rW97IW7v8dWVk40O7I0A1AiY0G457bFI8pcyOAYNjGEGF7XE1sVEFxqehq2Tsf69AnbgNRVoeRpx5l+oawlOOlBd6Kuga9kz062+1XO60HBvFhkO6+ENeHVsmYTWSGCP'
        b'HtgLrjOmhbwAeNGM1CFVt4KQAW0C157J2Ac288FgHNhMNZ+754KNOK1s2IJ7GEoLXof7GVMez8V9FplIipPNKQkIYQAJl3LdUKp7/0e3L/9rgyX/5vblM5TB9AvGnfsi'
        b'RTbyBUP2KCfp4q8V7SblimQO4+jaOW+UKeRZuH9B3LYkrXbqHN5k9Ai7Mr7GxfuM/Qn7LsduR5kuVnmNYe38lCH37MJVduEaNw9ZoixR4+BK9HiV+fccIlUOkRo3d/z4'
        b'Q6zBOn3E464fm1as9itWu5awriUq+5JHkjBWkshKUlWSqpH8Vwv/UKiavUidWcVmVsl0VU5+aht/jTBAEaL0GBQMim973BGMJLPxuWphHivMUxXMVQvnynRlK9Q23hqB'
        b'mBVEsoJYlSD/dvLv0kDayHJ1Yj6bmI8CLD9kqhFL+paqxAlDDSpRJSqJiE0rUs2vuJdWgfxXqW18NMIwRfTQ5GG7YUc2HCvKCnNZYe5Y6q5e3SLWNZB1DVW55gwFD0ez'
        b'kZlsZI5MTyMIUTgom27rqAVJrCBJJZgzMkU1YzabOkebr9C/L5xsMqmEWbf5dwzumGrTfOTs0W3KOktQywrEeIclSiXIua37O0NgOBKijs1hY3O0SaCARqyzPwro5I7V'
        b'LcMUfKXVoNM971iVd6zG3edM2ok0RZPaPZR1D5UlaXz8ULymQ2aocQensZIUVpLFSmaykvyxJn2EhGtPVD3xpo1T6CijO9VxKJn8PHL27DYi5dLgK5QtumSdw57cRbDO'
        b'MfjOuNuMdQ5SOacP8YeNhk3ZsPRRA36YoywZbwnZB42aLuNMRd/x/1G3jMd4+HRnse7hMgONp0BeqvDoE7E+USqfrNs89C/1N6Z3TNWe2axntszokZ0TaxeMtenLOBov'
        b'obxBkdS1unu1yitJueR23MVaWYosZVSX8fZFPqmsbzTrm8D6Tmd9M1S+C1VY2XgeO2Oh2quU9SqVpTyycxtlrKemch6Jg5QFeIOx8PbUO45s3Cw2rlCWLA89lK0RSZTJ'
        b'fcUq0dyhlcPr2Jh8NmYu8gk5lKVx85GHKiKUK1Vu6ejvdjL9ReNF4KuwVMzpcexzxLr5GneJPFvj7D/K43pEa8KiRoQaUcAoH92MMsh5FBz55EaWNKrPiEJkSZ2ZskyN'
        b'g7MsVz71UHFnsaLunoO/ysH/Q3dvha3CVuMsQKn5JHA0AcFY57ffbtBO4xuK0kHPUELIfRQZ9/TtFyj1RM5j4sqSUDa6jKtwlNHDdcflUwUl4h3zAs5I4kiiamb+79Pv'
        b'pmti07FRigIO9dFkz3r6lqQhCqRFpXOB2jWFdU1R2WMBOLt3rrzvJLnnJFGmqZ1iWKeYLxjHqQV4B8rLl/UMVXnGDgXLpmucPDvXsk4BXzC2DigLP4mc322sCY6V81nn'
        b'wEfhscNObHjmSNPdtdjQRNhC/DgYNXx3NOsWPGQ1bKtyS0B/Gh9xn4+yYHAeGzyd9UmRJ2jEEYrSvmqVOBH9DeXT31HGkpQeuwquxi9QIVUG9jT1NeG9sVmch4HTVDG5'
        b'6sA8NjBP5Zs3asj4B7J+sairCYJpYEnPir4VQy69axRrHobEqxLmqkOK2JAilX/RKI/xj3ok8mNF04bqWFHc7bw7JfdEeSpRnsY36FFk7PC0+5HZ9yKz1ZEz2ciZSCSC'
        b'ORzq9qQrEpUeGr8gxdrbpqqcfFUs/tNMT72zWpVbwE6freQPmg41qP0Tv9V4ixT8r3QZv0hV5Cy1OJ8V56u88x85usmM8L9DRl9IdfGsPsrD0z2d+p/abDOnSgiz+c9p'
        b'Ivx3317mz222/Qsvq4dYmaFnfGutCWsz2OGdsf+48x9Th/gOV6kfK/3Z1G/G11uwsxU7PyPnweQSzGZb2kD3DkswdW1VTSVRPa/fhh051hHz5qGgelpV4gfGT2vuPjB6'
        b'Ske2PhCHxoD0+l+wsws7k1DuDwzGVfse6Gn16B4YP62+9sBkgloY0RgiiiVEIP8xi23/QtfA32svMHww1j9O66D+MYH8OxR3C/SBykwwe2CMzR5gx57xEKiMXR6ZWDUX'
        b'yDzkPJmdolyZMGQ11Hg7d2jJSLAqp0A1e65qZpGqeKGqrEq1eKmqtEYVVqsSLVOZ1KlN6liTulFuCcckfJT5n3KxTYN6zpOMEnkTjA1Mx8YGUvFMjNzHxG1ORNOhravM'
        b'RmMuUpmLNFb4vWArQUFsJY+x05yGAlg7tS3SmPuozH00VniOtw5HAazDH2OneToKYO8uQ7n4qcz9NFZRKID9NBTAftpj7DRnoAB2bjJvjblYZS7WWMWiAHbxuBjIfUzc'
        b'5nQU5umiJuKiJpOiJpOiJtOiPh0GF9UKF9UKF9VKQgJY2rWhjDxV5p4aK38UwDIQBbAMfIyd5oRnUsAvKCvyakLuY+KSRGyc21ZozIUqc6HGahoKYxOLwyD3MXGb8etl'
        b'qotMX2PuqzL3pSWZiksyFZdkqqQ59ZlG88ONFoAbLQA3WsBzjZaFG20GzgW5j4lL2s3BQ5aiMfdXmfvTMA4kjAMJg9zmzFF9jglaQrzA0eWY2OOr5xzduTxsheF/w6XY'
        b'YgJ22g+H4FXpcnAZbJu4a8ZhpkKFTnlg3ARk9TgH9CbkdOgRdT7M589o9b0MKvTGVft0/sdV+xa9SL/rWdW+qqzGLJwR6M+Q+AcFhgQES8AVoGxoqF9e1yhFn8FKOAgv'
        b'wsuwH16CA2Zgk6m+saGpgYkR2AOawU64F3bkzoDt8GA+H5uBvWpkNBv2kcZbi76RCXEtbBUSDr09cGsdbOUxlvAoD14DO+D5RjzprQbn9DEcPQA0T2EC7AWNhAtPCRXg'
        b'Ko7TipwmeJgHNtWjmBdwzO0ljXg6nAIPVkt0MKJrpy4TmAsu0Jh76+GBsUwd4FVtRJwlHICnSJZQnjJFgqZ2iRc4yEgCysnRzBSoqEd54Wg8DgOPF1p5oDhSU4LdB+fg'
        b'cX0JarcguLGeCQIbXIhmSgGUgyPjddzkg6JOQpm1ooieYDcpJTgCNsyQoF4S7FDABIPjjuRQJh7KZtDa+TkwKBaXsbJEkeaDazS7gYVOErTiCIFtdkwIOAMuEiWIWXPs'
        b'aFZ+IWArjcVBsbL8ySkWuAUvV0vQuyAUbgcnmVBwDlwi2jcpoQnaMuqBrnpMQ9dqCa7iBhkCw7SQHXMLJKj3hsHrSUyYCegmLWIHrsAbtJR6bgxodiS5rbalRdwHt/oC'
        b'zAMQXl/HhAuhkuRlstx0rPGhDBxHTeE6JrZhJ6IgAftRB2sBA0hyEVWgj4kAXeAkqZ7HFLBbiI3bb6p35jJlPlRqKWArLeOxlWAL1v6MnwnOMvEryolOEwf2UvQ/jujG'
        b'lIADtPn1wR4Sy3e+O1ZYSACtBsjZD9tJrCIvIBeSPskDXVEMauDdpP3hviwSi1udINXF205bJjOJYCPcRLi4eYvALtqQKDszeMxPbyFDG1JaQaLBzY3zsO5rEhLAXibJ'
        b'pY7SQzc3pJBWRLGAPN1PbxIV22p4pRGrNyfazpMiWSdXgENM8lLPRsriCPrAbm29SGO2hsDNdPSQxtwP2okY4Dl9cFiKhD4dXrZDTr8HEUNjUQ2OjJoSXgRns5EzjEYB'
        b'OIOi2qbRMbC1Eh6VIpmnBGUwKX5BVE9LWWpMJYBiXG7E0aK0OU6KoVIYLgAdEIs9NY7PpJrkkpbxgJsttYWFrYVJQtwwdMjtmk37pgL25WD0MZNWDLYyaaAbXidnnjmo'
        b'D+4db1Q/XNPeeFpPLMbaWEpbf0lXF2LW+nQ07fQx6TbwBBlGJpaQ9pjN8CLq2DvAHhotk0+p8ffA/TZwQBerkA3lMxlmQKlVKNs2bazPgM4AXNt6rSQzQTNpHrB/hgUc'
        b'QLLMzHdiMvMKSTw4OH3hWLeRg5s4XhSVJdgKjpL2KSxCU+IAEmdWYxCTBY7Wk4i+4MDa8UrCg6V64MSYOGzAQVrWg/CWGRxAksxemMNkg37Q1UgpW6eAvWPdR88F67Jt'
        b'pxKZLiIRi+JROQb08J51L7jMzIiGzWT01oChYBopHo2m3HAqkNlupJgpQLYca3HOhB0FyDm6hBRTBI7BTbTfbMRs8ahJlfCUJejAuRVR+fdZLzfSwXKTz2ByctBMgUdu'
        b'VryUNAqJFcUEL6SZLfAhcTxAO9xshKSXa7KAyZXC3fRs/Ti8CU+M9xos/RrQhrWtqAzh0QQiCRO4RWiERJgHz4uYPJ6EKHyB49n+TxoUjZCYIBKTyNAY0qkX7s2FW42Q'
        b'DGfZ6jKz9OFF0i7R1XVkjgeb65lI0E7Fh95cq0xn5SwzQpLLb1jM5Mc6kwGxFnTCQ3Q6Q7WrZ8xAh3YAbkOvOTKODsCthkZIbAWFTUzB/DKqIDbkBfpJb+bxGNA5xyoU'
        b'RclrpILuB6eLjZC8ZsMrM5jZoAd00BdXJ1CUahuDBxRzwQkyZunLssWdxI0Dl0SgFV3MgcpkZg5ogZfoZHwGlXIDaEWCKZxWzBTaG5DgjXCjO2hFDT83CA4yc9Fy5hQN'
        b'3gKvlcN9qK7i2a6MeCE8SNqrthG95/ehqvi5w92MHyeCPLXPriD6oJVgA+OCBHaIDujtKJEbcB9KXAi3hjDCWHCWpL3SBbTnojb3cIAtSPLn4C1a623gEuiC+1C9/XPg'
        b'DsbftICkk0NQFEQrDh4sRwOlYyzCQKVlLiqhJzgKzjCe8AoYElDzDc5W8+iMyBPDdtxKaAziV7VuFPGekuShXXHkgi1PXq2wn0unuBteSdqRvymZo50YSYcTgltUS7IZ'
        b'9gmJxLnOHGbyGhp9mM6QVWiwbdW+31rn4KmLt5BOAXCbKwkRJVihlaIQvejO6MFNY1MoGIymRZCBm9qVDQ9uxOX30qVJoCUKGYhgAL2qZLRro5CH8kg2NJXYleStkjgf'
        b'7h4fOk0L0SjX9pXkUNIMnnCoduytn8DAYTNaSdBdL+CQAKJy2JkOW3xhS4qIy6TCIX1wgQs2rgJbPiarxbb6WIEh0Sb0LEJ9Ih/rUs+vPrBuOVUxNM8wYX7Up3qHTQ3O'
        b'9GGkRJ/51NWL6B3m5wTSh1P9LZkNq/Eqc/6avfnah6oCHcZ4LdFlzEg1CKIPu8RmzGhVBOoi840fG5vSh6fSdZnBGiQY5/kZyxaspQ/fS7BgZs9NYphl8zNcMrW5Xy82'
        b'YgZNhFiTslo/yJI+fH2ZFWNfk4sziroYuYg+zPDlM28Xm+OHvk7Fc+hDv0wuk2FMqzl55iyGqInbGFozj4vm4tzXZFfpMQJuXjLxWJrKZxQBVkR/PFTPmYb+m7se82ml'
        b'HQ5tbMc1YT4+fAj/9/sYkoF4hR6TwSM1qc4LqWA+lpD/vqRvVnjKT4pffExt+lqmFvTOJdPLXDMjIRozK9bC48wKC3hIa/gFd6NJ4DrYM9bVYtKe7mjbI0iGJo7WzI9V'
        b'haTwaWjKIQ+/rJjM7PQmDbLG3Mt+om4oGnD0EyGKwYQkB5lKrBtqvZbTwpUzL/oPfbGg+GfH02jn7rTBLFNaOpAH/KqasvIVAh7RHq3HxaY7HdjS0ziJB+7yqxylpQtq'
        b'SqqWYtNTTxREq6ukDaW1S5dNM0OCkeL3xrcbGJVfLv27HaDkXzG6aDQU1286aDr+mHzBkcrOCZjNJBpWclCHtP0+rQqJLyurSuFhzJHifaX3eZN35b1Vkzvd6ujU39Wt'
        b'qf5dy5+WdMoiB1UHfvjJ9L03llUd0bk3xXqy3ybnnC3GZiMPvtTlurm5JjVbO97lrQzo+Jbz89aYjR/+SfNFXZbF9MMfSiSrL1yq+HraOodVB9aflJd88LnARudA0Pfm'
        b'7l+7JdrHyj5xjt/pmmyf2Bm2ZcFCrtsd95w7QYF3fOvvzPygpdTGa4py95CjXbNdf5VJdWpupeTyssuT32qOeTT9/eWfOv+85XjLrfleddbLLb+Z71fn9LWl2SPnL8xN'
        b'Lfc88v7CZrdl9iP3L6yyLF995FvH/fjA49W7vhza0Dq0pSSg5Y9Dm84ObXv3nYjPL81KnnW/wOj1/h96f/K1O2V7Onq1rHf365f+vrJ3a/n50IjVfoavxz/8Nsk15efY'
        b'1V+/13QhXvL5upLVy/f9NX9uwnm50/3A6SclA5zvS7x01+e5vv3lt/1rZYdntJ7WKOOSl5axDb+dmbbpXoFL05cOkqF3DoteKzn5J/XLq6t++NzHrl566eDq+Mmhb3IM'
        b'Xv/hp6i02O+TQueUy8HKmtdvbE86+6Di7WWXKqplhab7dwV9FRaSMmL3sP7WS7+bZdfRllgQXJ0Bypt2TXVsjBya716h5+HZvvKbvg83GS9/Z+D9b4/rvXbj5u8n9Rw1'
        b'1xvY83Lpvr/u6Luz34ef9pFN5aUlO2fMyL7uWl30/ldtx3dcucg2S77Jrq0ZePDZwzurP/vI78q2d743Sy3aNnpl7vauEVtrs8a/vXbyvVk/FWeVHD3y8rQlppFv9+z7'
        b'0645uV1Wwg8aClK2ffzw3YtxX2x8Kebled/cvDc0y+yHh5kXtmUq81/55u33myS757/h6eHiJt3m0NNqGrz3nOnF1LuaPFlRiKhl1Z09Zr+k/eGHeW/t7/YfqM+5MTp1'
        b'XwjseEtceqBW9Nn+sj+U//5a6KHRVYW/F6lnXX79p3lH8zubOv7w2tvCqxnhM79SfD7nkN/Vz77/U/6e+zvL/K8ChfXylMJAceXhT5f+buo60bt/n/rLgVf3vHap6eHD'
        b'r6Nizmz04u2tOPjq8tVHPulZkK33Ts+o3aWTe8//7sdXCl/+4ye//PTu/t/d7/0i6k97H7/08qG96t7VGT0PDibNaxUffmCyu8D+lwU1aVuPr+G/G+T+7hvmAlOtupKV'
        b'PT53z8zIRh/7V+FN/hoO7E73ocf/A2jpeAW2UtJynRR4ZiUHDPjDy1qjBuD0/HT0xtojTAed60U+HMYIHuFxM+EhmvQVT2eU9AC8gj6FeIZg93pOAGwD1ymQpBfcAheE'
        b'cDfoS+MzOmV+mNRiGN6MIiiQKdmoDNmi1FQwZO6bqsMYLefCIwXGJKbNbNA5ri8ILwE50RmsB70kphta9ilQsn6oNDqNUJ7BgS3WYJBiS06AveC8UAx38Zm0Qi4Y4OSj'
        b'lcpZqqDUb4+hK080BmEPUHJAP1rBNVMtvDPOUwgZSLXYJ4vPGOty4Q092EFqOh90V6cT5SSUqTWq2h4OOOEAz1Cszl54ejaBLcFtvhi3hBZZh2kbnJ9q8IxhD+spvMrU'
        b'KoHb/70+0a864CeT+IuVjyYc42vVj568FVY9dU3O7vV0tdxODZlonRbPaU4a5ZrbmGrM7WS5ozx85SpSSOlVUMxtS3L1iPjy8RXxJVfEF1+N6jIW9shfj167iVEI7XVw'
        b'LAcFIjf6NJABvSaBtNc0ELkxpIGM6DUJpL2mgciNMQ1kQq9JIHLN0Ac0JHliSkOa0WsSUntNA5EbcxrIgl6TQNprGojcTKKBLOk1CaS9poHIjRUNNJlek0DaaxqI3Eyh'
        b'gazpNQmkvaaByI0NDTR1vFo2jL/ktqXGwVkhnfgz6jQeBjvNKaOu42T23ZFqSz/W0g/vBntqptgdXLx3sdyyvXZ/bRtPM2nyQeFeoQyfgPu0CdWTgtlJwc0JGnunzpSW'
        b'zOakthDNZJuDc/fObZ+3f15z8iMLqzbLtnxZWfs8tYUba+HWHK+xRQlHmSRxviBumy4+YHCSTZYtly84tEKhq6jvMVA7BSgDlKVDrv0V6qnR7NToUSbcAsfAblucxta+'
        b'LUHj4CqbJQ8+VNSJFU8mhxFHxtHY2B03PGwoD1G4KJJ6vJRxPULWLURtE8rahKrIn0aIwgZPxslhV2amcXaV8TVuXjJ9jYunfLJcKpcqJF0rulcoXbrWqF2CWJegUcZo'
        b'qh9xZHEaVw/5gm5PWcIjJ/Eow3Pww/obdUqLHmlfmFxfrv9IKJbra5xc5YsOr5etV4YNrbgnma6STNc4e5wxPmGsmNll1m0mN9PgYCi0s4d8odxAbtBtgHxM8VUX+l/j'
        b'5q2wwP+6w1CxbJyPmxw2OWTWaYZK6yZUJChyFAnd0TKcjUxK2NhXdEV3RysD1W7BaqcQ1ilEpoMDJqJiJSsTlcGKDNYtHIf3wkgOD429+1e6DCqj96GlnUsVUoVUGdaz'
        b'tm/tkFTtF692TJDxnjRFcNeq7lVql0DWJRDHTeJQFzWEl69iJmoltxPrVF7RQ24qr8TblrIkucuhFFmKxsnleNPhJnnjoXWd61BhbByeqoKz6xm9E3oKfpdptylqeld3'
        b'mZ7GQ6AIlmeOMlOmYslgV5ao8RQpOV1LZNM1rm6yhFGupUMSR+PtI+drPH3OVJ2oUhoN5ao941jPODlP4+apsDgRKg/VuAs0Xj5yHY23ULGwRx8HFijiuir/H3XvAdBU'
        b'sv2P3xR6hwChh07oVaoUUQRCUQFRbHREEJRQ7L2gWCKiBkQJiBoVFTt2d0Z33Z6wUbPdLW4vuOv2t+/9ZuYmkeauvt233/9f4oXcmTt37twpZ87nnM9BWTy8ByhdZz9p'
        b'Xa+wV9gXemrx2cX9AfGygPgb2bfdZZMmv+h5c5Zs6vT+CdNlE6YrvQN6nY/wJYlKn5CTMUdj+th9OTdC+qZfMbltLvdJU/ik0W6Nwq6lkqVKLz+lb1Dv+CNpkgn4j3FH'
        b'UiUTBowoT59nuCOaO9z93vXx1wjX6HNb63bR7ZrbRa/ooy/ygCxFgMYMabrcZzrqaa5eh2O7Ynvd+3TPBshdxylcx2FfGNRQPoG9Fr0uvRY9Ub21vbV9E08tP7tc5jNe'
        b'5vbEz4AnbuGHupS790MT8iLiyEDRw+NuoJZBcXiimEGAvf5brPL5Zc+E1QvJpk+DyNObksPY92XQknMZO7dg9JosOcJ0BoNhhgHzZzv8bej6B6gmQ+Ll6qu3boSUTWdY'
        b'vFxdEiacJmajSvU1cXK1/+dxckeQso0WKdUhY3RezEX4WZg0L2Yju5T5f0mMyhql3loZZJsp12KSOgeOmWwfm1RHkUCfoBu0ktBuTbleAj0gpkkNvZJTspKx/JeiRYUv'
        b'1faCx8LLDz93iy3EO+7436/ufSkUc6uuD9rLYG9uibaxDsxnvbxq0R3TsPYXbk8CW0SCgrzndVtK1j3cy422weyr1MccvT2Ld/OZRPacM9tGQIfn0aK0YyJhC9ManASn'
        b'iCGv/lK4dXBkKC94fLBlvakznzloUGAZSy2GGRTNLSmqmEM280uc5uBY1HMwbffjnfqgDEQ4C6JoXs+5k9AItRQtbA4ThSk5lnsmNk/ckdKSIkp519ZD5jkopIo1V6Q7'
        b'aBhrvcUoH20QY6iEHqv0MD2Jh+mf1cgSKw8qKdXYLZuExq4JHo6jHv62IYpRYMJrZgzbIgS+Gdi6m01p2xaB1Uz96Uyi5pwBLsf6wGaLyAwmxTTDAedOkx7VPpZFelQ1'
        b'I983KFmX4jMIeDYBtnkK0jIyMMudbiZzkrYQnqeVS0ur9CkOEqybzfN9OUEFdHSHoDdWZRktCI9cyKKYUxnUcQnN12lP2DepO+PzDc0iS6lK7BM3J4RN4f0JlfTQ8c1p'
        b'TUUnKCFW567rN8zKqfuhgUWxtDo7GO4Rq8ndvuHQBJ6fpucb8iJtaA/CK0vf+Yj5lQHmhzRY10bytaZpE9j5snN+Wl+8Lp0vpXXKR1oh0Zgf1Xj+y4Ti99UX1370APUb'
        b'D6rDkvuvKiFWDdeFTs/KWTXLqN5oQTZFafsxWsr0hLg5T9/ZRozFj3ilhgvTWZTFKdbHiiay/xASbuYv9N4wedH3RTTCdBhM1++Cb94m971wf+kblLYIdS6Kv3J7Njm3'
        b'NHrlG+yzLRTlTXm3G5JTZcovmxgOoRQ1i5oVakiqd6v9QZMc/f6Qejh3feXv5Nzc3GlNcvSKPqKyCzZs+ZGojuvBUT/YlEKYxlB76oIm5gRWanV0eZlXkpYQQyAPfnBd'
        b'n32q6u1AU3f+iy7ub24zf2H+pfqqJsP3frX+vPl3U0lYPid1Fef5hbqirk552GdHX2wK+TTr17Fj+6cWpWb7JqyqXdLw7TfvOjidmXPL6cfAJV4n2ANLj9gEvpq+ODzE'
        b'M8xg1qGZwufHXPll9q5DPYt19bq2cl6xr/v9xajQrMa7a77qOvW62OqTs1ZfS38cN3mi829t+181WFmZcf3Wq/eyTnt0vLryek6Bfn7gz/zXZsf0X/xtzoM1zqzPy15q'
        b'5X/xceDJbVUblnrf5K7OK1333RdvnHogaSz3cinm/rYoznqfmGlxe/7MtB8rZCz7+KCGFXcUnRtmKKy+vhP91gfsLfvel/cnJf92Gpzdt2u3l/P+yz998UaF3gzLyY/6'
        b'k+ImWd9646WWXZWng16ryPGPlXSntOZ/sbRvy4Nt0ze0Tr72Uvkv10RT9GPqakt/eev7zfoH78hjozwzLD/eEjinXjx3TeorM3O0Pk+q7Hh36b71hT9n3SoPSVl//a7F'
        b'nRX761Yof4v+z7zwH/qWbCh669t/O+5bt+TjS76fVu05+kLsvoL+uzbfuVcsObrkN1ZWtl/sg0un9lWdnLrozNuTrnEj1iX+59/KnAnCj+vMPl5qsNNqTtyPhocYXwU2'
        b'Lr/X5nPse691X9XffS/WpKzpX2Ojy+49PP6z2azTM157033614Y5IW2vLBxwMy67G7np81qnjaJ3xbe/LWzLW+Hu/9m3Wlk//Yea3NCX/5oT35RmM2kF0rkCPvbA1Ka0'
        b'yyJCmd7wghZxRgiB+0Pwpp/mzNQFIia4ANZWg5Z0cmWZey32T0mH+yt80ZoZxAA98NAs2qOiC+yFe4ieAUf6bNJBV3cyQ8CRFYbjiUcF6IWb04W19fVGxmCbiQk8bRhC'
        b'LdSirOB+FtgHjzDJDVgFsIuoXYLtieIFa10uriRJlQswRVa6LrgKerD5yDrGxFkqbh+wVxfs9UlV6Ti0p4BTXCYHHlGpOMYtsiTVmjOVKEAYoGscoJmyFlFgi0+qn0rN'
        b'o2fAhFeCwU4LIKFL3QNWgQPoUr4fdu/QzgcHQQfT1Xg+rT86Cg5mqomjtFE7NEejp72YQbsRbYVdlT6p8zL9YGNKGloXDcApJtwHtpSRFTMrK1aQkq5q41lMcACcLoG7'
        b'xtB3bQPHywetp+BgBdMaXlG5x7HhXrCb0Hym8dG7i3YF15kcX9jIt/4/8JQg5NxP8IdQ6VIer5JLBv1NluvnWKrFsXQSg21kM0A96aBPWdo0TlCaWMhMnJTWdnuWNC+R'
        b'uMlx7ChPERufWNq8VBIut/ZRWPvgEzzRYglnx8qWlSL2fTMbEVfsJtGSm3kozDwGKF8jW6mLksPdk9KcIi7sKG8rb61or5AG9WYrwpJEKXLORAVnooihtOCIpogKRFNa'
        b'wsQT+y1cZRauSo6TSCBh7shsyRRlItFhT31z/Y5FLYtE7Hdt7MWTJWxJXaeh3MZPYeMn0lZaOYsqJM6HPbs8pV69SXKXaIVLtNwqRmEVI2IprazFLHFCq5a4SKzXUolO'
        b'WFiJ3ZtjRDGSBEmR1LmzRJrYyzgyQVLRndFb0u8WLXOLVto6o72+rYNEX27rLdJRcm06dNp0JDpSKzk3UMENFGkpLbjioOZIUaTS3lMskDJO6hzV6WX1VsoDx91IknsJ'
        b'FF4CuX2awj5NNEFp64QjcGHjW8twvEXPkzsF9LrJ8Xb55/v2zpJESaJUpzOtO01uH4izu4t9JAWHS7tKpVm97nKPCIVHhNw2UmEbiYqxsB6grM2ilXb24ixxtji7PVw0'
        b'ng6lVtsa2R4pZUlLjhjI7ULRWSSLJTcni7Ml41tnyDl8BYcv4/CVPDdJbaeBKEFUIioVle5IGSKyKe2cRONF4++j0nMkIeLp7TH37Pz67fzkdgEKuwCZXVhvMCrYmjdA'
        b'GVtG0xoMnjPZVbOk5UdM+qzkvHgFLx5Hd+NJgtuixFFKN/fDSV1J0tBeS9pno89Z7hYtnqB08cR7a7aDv9LDkzxrdm+I3CNc4RGOd9VukiypWWeONEQyvTumN6zfNULm'
        b'GoH32Opd9YAeuhT1VXcPCXp/kvLuNFSmG/9weld6r0efm9wtTuEW98RTaV1pvVw5jtsXhU6Ymu3RadbZodeiJ9IbmM5AnZb0XHJ4iA+PqCHnRjv8/PPPo6blMShTzgDF'
        b'MvIaMlJGGUfDR5oJR2bCQ6fFOSIcFAG9+UYBkX6eM04JE5iwXjZhCyx0XrZioCMtURu+xV5QUDv3LXZxQW3BW3plJbVzastrK5+NOYLw9Q8OGkZL4c+RzfLjOYWDBe7d'
        b'lCZIWAkWubGN5187/G2i+XRU3yLmoM2dZse5jKJ3nITSXAvtmqlSlobCfLjR5j9Ayq+p2JB4DGg7gLFUr+W2gkzsC0hwfLR+5XmagwssuAYch9Jyi5U3WIRUd8t7z+99'
        b'KWbf6k2dOzt3Htm50OijYA/tDd/suRNvyHjOsN2PWrBY6/TUo3Q3YQ1/43jfq1lDjHC3ebyMDP1KVhIsfpCN3xRVKNJiabnMIkJuEaGwiJAZRgza42nXAOxWcfMJvhXY'
        b'BE/lKUH3shdwLxt6yxzc0WootV9E2RTUzxxwX3ny4W/rRFgE+P9kJxqhuhitE7EyyoU7j1NCrKqwirAa0kFsLFhwHm8DlbSBsyFfu6j0NUNqgb9WxjSvp+oiwqFdRDii'
        b'izipukgV6iJG1o2polpxttzQRWHoIlN/RvYS+LS95CXSS4bcddrQXjIf9xIu7gxPPvwDvWQF7iUsVS9h0Hbipex/sJ+MUM1pzD8G9RN9OgIIbALr0wRgHTz+WJHB1E+t'
        b'J9v8B2GOzGVsatFA3BV7Ty3/SHLy91BaKUYVrPS9axZPG2R8MZHCZxf1hi+OmzC9kCJGYPBgDLyclZkFjuMv6yiwf2UByb3LSwerD0zzIxvSshapgzSsLfLI8oO7fRLh'
        b'muQUFqU9nckA5+zLIyIvM4T4eesTzy6fdNkYBJp+P8vRsuPG+4/s8kt6so+4Fv5eOO7F5821x9y0DSr+HHjW2LR55/CmdEec/9Y37geD58afzWiOtq4N3yKZIPD7Oj7l'
        b'35+CO7c/Kpx6HN7YtP7TD6cu7XnLbL/9a78/f6Di9U1n7p45IG3btOWjY1pdVad/nDO7eXnHbI+9uy98M+HsdfPa5z5mv/1m/4F9X605XLVYK6z5QLjDwG0jmdnlt627'
        b'bnruvXuer0t4G3THT/GpNfTzwkZY2qCN6QcPc2jEd78evErv/sAVA/UGsNrSj2YH3Ya2dWJiv9WENkbNcGsmDgqwBe3EQDOgtydh5ukE/N6DNnsawtw5UEQzIOyHu+EJ'
        b'cMwKXidbNbgJ7dVWMF2ApITeUa2Gx3hQ5KkKaqFCsYt06T3roTJ4wCeZANGUKTucAU44AhVQfcgOND0Gx6HUgx3JAKciA/g6TyNe4BGvoqGkZxNDPN0vKC6dg2WXJUO+'
        b'kblEoZpLavFyw90T1Ry1I6YlpnG80tRBZCQu7qhoq5B6yh2DFY7BctMQhWlIY8IDUyvRQrG73JSnMOVJzBSmro0JSgtLdI25BZbFgh5YO4gLaFlsB1vEEAUpTTl7DJoN'
        b'kLCc0Drtnr1vv72vdLKcxLiVmwYqiK/LgA5lQUS5oAFdyshse9rmtE0ZWzIaM5SGptsFmwViXUloq4nc0Eth6CUz9FJaOImCW8JbYiRsmYWvpBYd6A+qBpblBk2AOjWf'
        b'45Zg/yHNF2k5lVxGz4N38Dw4pMFm4GmwQTMNCp9iGvx750IsjAyZcPRUv79/noFGu9EeqoTKYxRTecxiRh6LSbWwWgxbdEqZPcyhVmaNFIEziE8NhjRKdYtZ63SHznV5'
        b'bCZVolXMXkcVa/VoH0Kd5ZhmFs7TJmk6KE13RJoOSdNDafoj0nRJmgFKMxyRpkfSjFCa8Yg0fZJmgtJMR6QZkDQzlGY+Is2QpFmgNM6INCOSZonSrEakGZM0a5TGHZFm'
        b'QtJsUJrtiDRT1KoYZrFbp5tnRvI5lqMJu8RsaNt2M7Yx8sxQXgwu6aE1yx7lNy92IBEjnN7SSS+owp6Wv/rpD1ZIZE2YlMCbTyfxSIQ8/yHpfAZZ6YcslriDkBWpER12'
        b'6Q4KNaR5+US80tMsm8MRrb9/2ZzLZ/66dkjN8b+UqvLa8oLK8iUlQhKYcsjTllcJa7GHqb/+iOuiFhTUFMzn4fEZxcNBBfFfvNpqXgFdxKTxSbzS8soS/xFXjhhJw5du'
        b'x4w6TEUCry4DZ8hsPQnuKk+GmzL9pqqI1dA+odHXn0FNZOiE24OrhOStAkjBfoMFC7NAXxlKVWfN1sWKeNiYDrcIUnzRclTE0zXMBafJmpwALsCddJAYPhRR7FgGOFYC'
        b'L9KhWzpzsnxwDI7tggiLdLxKtTKXwnOgiWxhQB9YC1t9UtP9/cC5QO9U4lxn4cmCe8HhetoS/EAhVxA8yTCVSTEw7fSFckeCqjjDtWA91s1thhvSGBSzkBFkAg/QoV76'
        b'JvkK/FPTfVPQ/QzATnC2mglbnVOJob0lXEP8DrZiehTYlJbOKIRNlDHsYI0DB0A3Xav98AjcKQDHk1G9UCHgMLhAmbiypoG1YC8dcWinGWxWaQbrA/BjgQvosTbkkApM'
        b'LV4oSEn3hpvgjsIAJgECwGqws4GYbsNusCpEE6zIAO4HV3GwIvQch+miL8IezKRDYgZ4wGYcNoAB9i6wowPMdIF9cL8AbgaXMtLoyFCz68hL0C9Bb4EO/eQIuym2IwN0'
        b'ecMt9EvYWJ83OHqTIdg3wZRlGbiIIEJRE0kEt4jLE/MroxxKKNrpZh2qxNosCohtUWNTzuBEJhHK+rII9jN39cT8tDwjOwxN4WbNhnvhvsFRmqKr0lVBmtA73ksuXWRF'
        b'RMJ4sV6+7844TzoqETiRE6YKHAXPL6bYvgxwCayHe4j7i9fypYPiRmFXMRw7ilWI3mEjHWYocDyJGjURXFUHjhJy6chOzfACvDRKZCfU4c7j6E6rtEr14VXySiKhiIM7'
        b'DNlHBzDBJnPUISSsWfDQlHKjijimEK89i9YfPZ49NhMGmo6Nznj7rPHnDVmmcRvev2Fyu9BZ0ZmYkPYN+CTDtzEsy+al7R/rb/5a0OaxJu9o7euf/rSsYflrSx8x7NOK'
        b'ncTdn38TeYOx8nqFhe1FLa3oi6+lrcypTHzt/s3gmu2/6ex9OwV8MD8i80XhvRLLA2/mbqj78aV2v89cA75bdOWVNyRrDl4Oew24JN1ilK5/eYr//q85pza8c+y1ywE9'
        b'C5Zsbc9YbxFWc8kyo+PHyfDLybMnlMhS3edN2nE8+1cj74Vm97wNvdt99kZ3dU/u/Ip36E27t7u9736lNaZj2kpp66Wa/fEtEY9umJmk1H/8i2f81zeO+T987dY37baX'
        b'I5z29wi7Dj2aUBV5925n1JwzU8IZxyfqvHn7+XeuW4YUBYR4tqak33mkUNzymP1mxpnpZse//Xd4+niDNVPW7H7vnYf7HL+a8cOn3+Tufv2Dm+MOfnkpgEqM/Xz+5PFx'
        b'VYLjSfverkr9z3YZ8936piqLu/PXvDKx5RPX28tuTr9w8L2LL/elh/alz1TM7zr3duVhywu/L25rtGIfZO8TzviiMHf61rdvLr5w/KvcfbWf17u/V6bFeSfx0c9GX5ad'
        b'tF75HN+Wtqc8C89yaDl1nBdF5NTcRUS8rclHYyjN25+WYQ3AhmWVTNhdStGy8aqliYSBHsvFW4EUy96wibkc9FkR7rMVTHAY87vxNdR0loWwGWxk64Jds2gC/g4e3DAY'
        b'akfZPGC3BmqfSMeeQF30ODyKow2R8FratvB6OFMfbIYSguIsgcfBRtAUQE+eZCq7aC5kwrYp8DLh/18eAM4LMistUc8nLHet8DCpYEwcGnJNAXhSVc2oVrAdiuF+dlR4'
        b'ErmyzHY6aMoMTmWCcxMoViVjqr8bAUOqzSlMb7UtjQF3WaKJp4MBRHCNMd0s7Y42KFE1r4I1oIsynsuKABuAlNxVewbYQiIn4ZnVVYueWynzcBboLOaSB1oMOwpRCXha'
        b'hR2zycxKmS9loWlr1XjatPYcbJ5HKoDnVfzEcN3YyeiJE8FF0mJlUGKE0sncilrTAO4a486EErB6Nr37aMmBBzWRB7TRLmn3IrSlOj6PEGOBdnh4JildPQ+CbQsoEz1W'
        b'LVqO6Igd02aGkwwkjJ227gQjpg1sS6BptdbXwzP4baDpCK5pUEWyM4cHWXD1OCfSQlPhzlpC7Uai2BmgBUqE+g28oAfpqAqO6NU2o/JVc78nbKOME1lJmWmPiMHIVbij'
        b'1CeD6PM0k1ady+OAcfF1OmbwINyp6hynXXFrq9djeABup4zLWFFgoz1d34OwPZ1+X/Aa2K6a2ijzCBa4klJHo4CbwMV8VOHkFFTSHtATQA8Hc2MWOAR74QG+8d9EbIFx'
        b'dSKzDGO0wGQfS0xV4iImO0FClIqZ62ua1WJgXpZajygZL7fgKyz4A5SeWTKDgBEaRMKhPbwjri1OGiq3C1TYBeIUfCq2LVbqRsMTGF+JZ7zr6CXjx8od4xSOcTJunNLO'
        b'SzxWypHb+Svs/ElxOFsyyuYt80mSO05UOE6UcScqHZwlHu0zRewWfaWTr3i5NLvXq2e23ClG4RSDThpiU2HPw15dXtJouUu4wiUcnTRR2vM6ktuSJTmtme2Z6ITeyBM8'
        b'P4mRtPjk3KNzexfL/RMU/gly3jgFbxxKNFI6+0scpLUnFx1d1KcvD0hUBCTKnccrnMejROM/TnRy7VjUtkiqK3cKUjgF4Qred3LFv5Q2Dh3cNq7ES27jo7DxEWkrLWwe'
        b'UnZmQUprniRJZu2NPvc9/SUNSgdXSVL7bOnU3gk9s2T20Up7F8mY9gz8K1Jh7/dQh+1l+4hCBzG73XDAmOIHSBcrvCL7XBReY+95JfZ7Jd5IvG1GA11iI6ULX+LZW99X'
        b'rghPlrmkyF1SFC4pYh2lT1AvX+ETI9ZRcL2UXmG9hagIsU67kdI3ss9Z4UsS+ErvwF4bhXd0X4LCOxalmigDw/FdFVw/GdfvaWo76GuUwt4f/45Q2Ps+NNLBD6GjeghT'
        b'ytKmJe0eJ7ifg2NJBChCUuUcgYIjkHEESl/Uo1rSFBz+fWd30sR2Th0RbRGSVLpviXSVFna4IUNxQybLrH3R5z4/UGqtdHCXlCoc/KSL+rR6Vsrs45T2bpKp6O7493SF'
        b'fQBqSm/clN64Fticmx+EHtcrum+cwivunteEfq8JN4puB8m90hVe6eqmXHRDTxGeKnMRyF0EChcBbsqQ3hSFT+yfNWVwb6TCe2xfgcI7njRlcCS+q4IbIOMGPF19B3/P'
        b'U9gH4t/TUKui1sTPoaN6DtKaGfc4of2c0N5pfdWKsAw5J1PByZRxMjHvFB+1Z4aC46mk21OEfgZpPAxp0iXwX5EuqSCqx3PNH001C7BKRESpVSKzsp5SJfI/15UI8Yau'
        b'XS+YOm2cQLGeIdY9CdmoxSTBuEcNb69pA3Vk+1f1sbkrTifWUy54E6reuGr4lobEsK/BTFTPUKcyVCc+4y2dOcLysqqS4qeumQzX7AfGkJqRalWX8nBRBbV1NUNr9gyV'
        b'WkdXij2nMLjwqWv0Bq7RCU1beSVVFpTxykt55bW8ciHaso8LHqdpu/+yXuQFfkQ9wwu8O7RS9riZimpKistrq2t45cX/bUXwW6v5nv0MFXkTV+ScpiKOqooU1JZXV/H+'
        b'SpuoOpDenPnVxeWl5c/Qhd7BVfLQdCFPXKXKAmEtjy6p6G+sW8mikqK62meo2/tD6+amqRtd0l+tWKl61BFas6ev1odDR523uo/XDpoXUGenS/2Lo09nTnFJIeqmT125'
        b'B0Mr50SmBFIEr6CoqLquqvYv1khvjnroPHWdPhv6Hp2HjL+/WKu56lqplfhPXasvh9bKfbBuEb9KtWJxaM0GVewxUllPYTx7D9XIbGSpjPApJrVpmFJ1OYOoWqkRqlbG'
        b'CHUqtYKhUrWOmvZkDqvRjPC1n+A8QGrNoJ0HShn/oOtAKZ/567QR6lr8jwylhrklqP1r0EtAo2jQgKpBg74GLba1PNRtqqprR2p8R2h9NX1nKLAvqbrPEOLtcuH+nL0v'
        b'RWCHgiaGNnEW8LDp2sT8KDSLz1DtADGHOmyDB4frC/azo8BuZ9TbTNW9TSVI3cAslU7q3qap9GPD+9KyklqyhcNm0liqKsxlUPa89jgZx3uQkMemhbyh8h0meCLm/c9w'
        b'r2+xDFdGqQwYZ+QiEc4cy2LDD38bjPUc8ykNP6hGxj9q+PFUwwX1j80HXmcJcTCZm0vjHht+ZGwtt3Elhh+rMp5fxN3pvN5ZvDrEiGrmaUnP3EEdhmgVdsAroHdwZ+GD'
        b'PlV/KbL/Y9OQmhf+9HUKVV3HVtV15qGu4+kjKZaGdVZ0V6BNQ6YI/QyxDiG9yIzxtDZET1OFH4fai5TjLmWD+9CTD3+rvQifSVOlbYWb4EUBdghPWkaxTRjgsCODYB8R'
        b'8Di4JPDJ8GPwMil2CAOcgSfB1vKfVhxgCzGZ3kctF7Aj0eqdnWv5W4MuXV1/av0Bq9tf5GcUpRYwT9tUcOdxs8SfBmqFLDjEop7bpDfBp1g9KEfbUeH+/bgJv0SHJWYj'
        b'mpC8t3T6vSnZugPTchlsM58BapSDMcMM+22OfrjPc5MWy6xD8Mc0ZMiEMdoLfqq6fYNfaIWqT03Hr1MPv7VRD3/vNDHqykSmCTZZmdgEQ6VUdj//zPpUhtan9BGLSyL2'
        b'lxLSgh5ajYbil0KesLa8spJXX1BZXvwnUORo1mbaGdlJBAJyjVtK6aJGMY1Osy3h35tdrgRObCEew9mOp/e+FIzWKne0Vm1uncJdm+CyJXCHSz1vu95ruN++HALrFjAX'
        b'+3K/W7CDOab4jXk2Ym5UawX6v5vx6sytgbndGwoYPiyrXsPG3BDeo4Zg/3zXnhMbOjc3rXZucng+s+C10oQ+k48nvtbPt6Liz9rpSbbydYlWORy0M3ywEpQoQHWhiKKM'
        b'wXnWxBWptC3MZrA2ioYwrYsEaghzbglNbdGHiSVoJLActmWooUA30EH0tGFgJ9fn8coKOuF1Gt80BKdI6WmG1hqgMR22MgjOCCUsoo92iIHbwaW5NOLKZjNAB9yvincB'
        b'T4aA9T5wU2YK6GFT2im1lUwX2Ax7CPIx1TVPt1CAUny1KbY9A5wGO2ErX+vJShNs+jXI7Ea3XDiHvOvHcqX6DBnnbaqxtATNz1z7luV45PKUdk7iUKW1XctS/NVZUtxd'
        b'Qf5Q2vHEYfj8CvJV6tbj9/j8fQ63JV3GCZRkd8/Atv4OoihxgYQrt/BWWHjT2bg2Hdpt2q267bqiBOwukNqcuiOtJU0SJOe4oUzS7H6LIJlFkPo2otohxjOjSBmj2s4M'
        b'sjqq4WsPlqjVT/4bnkXqKbUL8BMFjf+V3IHfegb9WBajUWoP4s7GFkM1X+A3ySoMLqzBYWdqmrTwi1XvoN/SVe9X39Kmt3JvadMbqbd01ZuXt3TVuw4ysZJm4Rv9dTjA'
        b'iBrGc023uhJbLKmNRypwY+cxh1FbMzG1NT5oU8aWjbnYsUHsLTNylxu5K4zcB5jTGUYeA9R/f8Rs1B6PS6pnDuFejsDcy1GYejkKMy9HEeJlK0fRNKUpX2bKpzNY4QxW'
        b'OINVVGPSMHpnzMxsQZiZLQgzMzoShufBeYJxnlCcJRTnCCUZBjMzh2Jm5jGYmXkMZmYeQ5iZB/M/j8X8z3GY/jkOsz/HEfLnwRmicIYYnCEGZ4ghGQY/COa7tiJ811aE'
        b'7xodybMMzhOG84TjLOE4RzjJMPgumHabi2m3uZh2mxs5oho4hgN3LM4wFmcYizLo6huFDlBPOlgRCmsZ0VdLIiWRndHd0fS3xpQBtilmi36GA830THDHs/7z4RkCpYWA'
        b'o3iu1QfbmOAybAKXh6xt5qrf32NxZ5fNCIM17RZuC9XDHGpWRayVjBrNGy1Ktf5OQzW6XLTD0FunqzJNsyXmWrqjmGvp0rXr0R9mSocFEANUM3axwYia6T3hGi20nTYc'
        b'kVtf9fzcHqOhNS22I/cwJ3cxWac37DoDch2Fr2zRQT/cHtNDaKI5pq3OoYd+iu0bGYRMm7b5Mmo0bjRtNGu0aOSWGhZbjCjTUF0X9KPbolfK6uEgSZc6pmFMKHYgJoRa'
        b'xIrMoNEQlWeCa9jIabRstGq0RuWaFluOKNdIUy4ptUWnx2pEuVqqEk1IaVaoJL1i6xElGavalju8bVErMYttRrSuSbEx0ek5vmWsmiHRr4KykpoPQtHFQySyBN7QHFiM'
        b'Q7+FvAIkwQ2W67ClWkEtr6AGK/oX1pWjaX9IQaXVNXT+YpRUVIsVbeW1vNqagiphQRHWTwqHGbSl1CI5sbpGdSvNXQqEGm0TEjCreAW8svL6kipVsdU1i4cV4+/Payio'
        b'qSqvKouKGmkxhxVZwx5QI5+Om5Cd4M8bX13lWcurE5aQJ1hQU11cR6rrPNTekEkjTB3MYVQaGoYKvJTu0tJQaTDVPO7E5FBHQ6Kh9U+QaHyQN/w1kwYfZnWoFtjnqxvm'
        b'vzI81LwXrKtCnWPwyxxVKYV7EHnxxf68FIKGFFejGlVVY112ubAWn2nA76dQBQiUjLKJUFVIpTCl6zRCjdpQjiuJUkrrUHEFxcWosz2hTlXF6D+vYMGC6vIqdMPBkMif'
        b'7GC0qZE7GKOMurEU8TRuTh4cATeZNhsDHWVoA4Dk761pJF7tlOS0DHWEOXAdbjSAB+dV1WFWDB+4ntCCqEoAfaWaQlAJ6DqVYWA93Ki3HHbBnWTHD1oKWXAn2vEnsykt'
        b'T0YFOA7F3DLaUG8NPAWaCU0o3D2RWmQOttORf5vAmTFZfvAQPA0PBlMsf8okJiif6bZoEW0fdynOEdP5+QjUzCTYQnTSFL+pTLCNRYXztcAOcCqSkJNamsA+HyYWyMA1'
        b'SlgMO8leLracSY03xVq+/MpUzwqKxCdetgzuFfjPgOs1TwQb0ybj2IG+cFs6HZxvcrUOXFUwn9TebCzoFi5cyNLCfN2Yw7u1snycmMsWmqL+zgjZv2vKqQwYyLlS5nnq'
        b'Deb64LpPDLg/m2srNt1ipbqLdKeYpe6uKp3Y0+rS/S+3TMvzv9q6rjmQHPvpN+9etl4pzlw0y7lnycMu11UH9q9azXzPTHgnYGbYh23eK74Ndtt9Ycr3Ves9Mivav7m4'
        b'0flH+TjpZn7GD4tn7Avf1wrcvH7uWv1y95dGefOkZ47Y+se1f27XUDvzja+dpu8YiLgOwr6oPDb7B9sZLj2/tLx+fTwIfvCm/WKF4GGDfvULy7/6zHNvSuneg8uWrNjY'
        b'eOkX9msvvm9flrvw/aP/Sf90wd2tb32VFffy5enbvjn0w4Pfy7NXy6fHzw7JY9+0eGnZ7H06/zpbeL1JPL/1pU9K+zNdTqywae2b8MuA0QKDrPPnsvgc4jQC9+stgidj'
        b'BNhOixi+loAu4hbiDQ6A6waCGnBhiHUaMU07hraGZN+4Du6PF6RlRaoNULHx6XRUAN43WtvXqPw6QCNYRyzm6jJo66/DDXCnIA2Il2us5rDJHOgF1+n0Q/AQ2PPY8wPT'
        b'xBPXD18POv0c2MAQ0AbH/GXwsjalx2Gi3XAr3ExTFjRFToZNSATLwP3GG8n34Ow4sI41GbRm0vEdW+EJM58AuBmLZ9pAyhwz0ResU18tDgUX1TZ7KfBCvdpk7wS8SB4s'
        b'Ib0C7cJRc6Gm6WA7M8C+aniGbg8pbEkYxB3AhGL3kDywmzTostBZPv5jucSgDG7CNlkCPySMg/PsZHAV3RtvKcOWweMq1QEqwIK5MNwInAVriX6duxxeBk2ZGQKwPRO0'
        b'LlER/5iBPSywHawF52gzwM5YP2wVppkwjLPMwX5W+kLbR6hKlK8bjkOKuTNx9M1tyelwG9gWIPAj4ULhdg/YyqImglM6YPvk2bRGgYvmIdp8mPKCZ2jzYU/QREfm3Q1W'
        b'gb0+/sF2g+JtkmibcKcpCYQLG0E3EnybAoAIHkZ1Auq7IvGfYsHrcBU8xdf/L7Z9mKKKN8xzmJhlWA9dzocagiXQe8CBpOkMiutE6xaSGe/ausnck+S2ExW2E2WciUpr'
        b'x5aVOCWBTomT28YrbONlnHiltU1Lw56VzSsltXJrX4W1r4hN24bFtMVI2dIyud0Yhd0YkS6db0XzCkkx7XWNdhyoNCXHao+gWSBhyznuCo67jOOutHEQc8RzpSy5ja8C'
        b'h+NjWI5j9DKVXNsO3TZdmXNwb+7ZGXLneDk3QcFNkHETBlg4B52PPj4kx0fU8PNPOhL38Sck3bexa7fucGxzlOrKbYIUNkEDlLa6FSL6QuWDmuL+yJrH45o78jrK2spa'
        b'y9vLO6rbquWOAQrHgHuOUf2OUXLHGIVjTN9khWOcmIWfI55BX0UfH5LjI2r4+ScdVc8xWtJ99AKXSor6rfkyaz6x0ouTO8YrHONl3HilgzMxvXPmE9srniexj3PxkLhJ'
        b'6hSecTLPghsTb6bdGz+jf/wM2cx8+fgCxfgCuUuhwqUQG+KJ0I+QRNVwdEzUZUFddqKhDjRhoONNw7gJ1qxb1uwJdjq3HBnoqCKRG2SAhMXDp7BCoknkNHZHT9G77QzQ'
        b'VRspjZO8cBqDwXDGKqNnO/xtJkd4Td+rF0SdMo57FosjFUSt9Yfw9PBGUKPUMQZDjI9CNILoSMlzkJT5l6yRcH1rTvyBhdST6hpnMNi8pcZMe5g321DaOhaNlzeyVRDg'
        b'P4OYj/Dp/f8FYr4O7cWuMoc15xPA7RfffY9J8EHFA281uD2XR+DtEMqjifng4HN8BgmYDMSgB/aghWzQItaChGH1QgYuJz4J3/YY1gWERZVzCKHcH8DcU/L+Esz9lLdM'
        b'NBiMdifm/R+i3UMc2AmM1cj4Rx3Yn4qjkZ1RF42+cfPDh0tR2LVtU5p3qi84mk17ueETmRbgchr2TADHwCYDJMHuKs/avZwljEOFTF2yhsaoLib37AzCONUvAvEH04Ls'
        b'N3CeL9liaHjMpuBfHkkeGzIkjtnyjEOLPPqMN+Rrv2ZFec4w0LEI4LMeYQ87uMobXvojkY7lXKyS6JCMKCbcjeBKpc0wh5IAZsEylT9JPBLucC7YC7aPwR0enBs/UnAD'
        b'jZP+AOB9vGq98LTdUY3Wj1WNgGloBHAxy4ZlGkOSo8DhefGfxJo+Ve4oUDgKZFyB0sP7DwB9nT8G9J/g7PwsVU43GOIGnZv35+j+3wvx4903n0nTKnRqwaME4Sf4/n4o'
        b'AofBWbieTrwAr6E9F4b5Cch/rBCcgWdBY/mri21YwjCUwz+lg9hv0Di/GuX/Jj+laGFfRgHzO+4gpL+Uou656CmU1SqCzT/BAh+37W3cttwntS3pANmUBvaPz2PoYpx/'
        b'lAOHhSH+PzzoUs7uo6P/Wk/uDc9U33H47S9QddiEvD80Bfh77QEwHyhabzA0N2Q+1bBurKJoswCVj7N2I6NRBy3EWpoZdbii8X8yo/56aIRybGJJLa9ALXoNViA/Wa04'
        b'v6aklFbhjTAlH0XzV1NSW1dTJYziJfCiiGd4VL7q/eXzqgvnlRSNYgz3pzYHWjgGG451dmguVixcJYyEKb4pOZNy/abmjuoHDVaF6s0D55bW4X33nGKmwD9oiVqPRev2'
        b'hiqyphjowK1wPdxafvqgEUtYha7yKn9970tRxKTq4s6DO/2a0pYztHcHBQX2lK55OM8marpZjQHXpneV7YaS+Id3Flws7DSfuq5Sv8hTYGnHamvzSJK8mvZZVIVNBfeM'
        b'uCBGcmxafuW6uWPEOTfngK3FOhaXPg/b8pxhuw21RGb1fq6Ur01UEEngQDnR21jCdop2dAQd4AJtoNCZCc/AJt9wuC5DpX8gqhHYnkoUAllwX7SBAPSmj1AZ1YEOWt10'
        b'1bGU1jWBLngY65tC6mlmxRbbGEFaJdyk0VwY5DHhiXx4hchfxfXw6og1iwJScIhetWBL7LOwggyiMjTAtBaqjrXEdthQH5RGJqdFqsFei1cnN9EyyXipWw9fbh2qsA7F'
        b'1Goj9v0MMwG9fx53I1vuniK3TVXYpso4qUpbZ7GnxK3Vr91PpKO0sG2Jlrh1+ypcgvstgmUWwYTReKzcNlZhGyvjxCqtHYc4tejSCxtB5v/YHEH38eqmmtIKsT3CHzxn'
        b'Np7UlmmWtJK8Z3Fj+dsmuMVPlBSXUPTGQkV1RKmMiP8xKfHXc6POabUjjcerS9XEC//7KS6BvudTTnFPsOXcQzmxhHi6Sq76jiYPL2ewxshe7NuyY/UrtQVhrlvmvDwJ'
        b'irQ+RSLAeYp655H20rJqPpMYc/ppgw5CIPfYjZSyhfs48Bx7iZDWJXoJvAVqb1tCY9AGz4PVhvNGt/TU2OE5MZ/QYVXtTAami2pgZs9gUHZO92y9+229paFy20CFbSAa'
        b'YNaOLStkpu5DZIAnDSGaFvzxjurP7l+MB8x8zYCZMOMPB8zfNkIi8FMwaT4fHWFBfcmcAmHGEOxRAz1h0x5aGCDYIy0M6DYy0eDR/geRRzR4PigcDXlUjx8M7BarwtE/'
        b'1ehJ0IDQJbUF2MGlgDZ+n19dj6SL0prq+epy/66hR1+jau4oDFAS+NkXo5Lz64S1GJWkpwJhbXkV7RGEdVCjwoq0XmqIAwVGn1Hho0GamlGP61pT0EA3F3rm/wKB1M+o'
        b'C6ZwZMxldQQo+QNZJhiKNOJMtQOB8HRyQY9PKpPybWAkU3DX8ljCFlr/e3RWjlG9u5bRAjbFbmXUZsUTaC8sjDCCTLuZke8bkx9CZdO2MvhgCNrqfDKZaEN5jjGFgm2w'
        b'Jbjc/shhSvgKSrz04OyuSaf0QaDp8obyfqvw8LLrN5577tsF3hHabB0dn+zU07rGv1ALX1UcjCv3Puvu3tRQ3Ld08bcLvz0em9/3Skru7MCpL8S//lHxB9/ZfL9uvE1t'
        b'wfuZ065ee9nmzsfFx3p//r77fo9h6Asrlk4L/njCS4cNTnZ4vGyb+MIyUHfulnHd3YHE7LmNk9ZP/Mbvud7XpxzN+8z3bsRDSdV6s9keNsHXbukfv5LqYXE2bPaV1upp'
        b'gUZ28n+fWHjr68DiD/X3eYa8uNPY3sf83+kPGr/7l5beD2Pu7bjF1yXIkXcmOEdkqxogUclW/Ewa0tq03J7GnMKRDPhYsLoIVtF8Ay2gbeZQooi8MhqMWw930QwVG0DT'
        b'CgxMja1AezwMS8E9HjQodAJsgFd9vDGZQV8F4TPQi2aCDu2xZKe/HG4pVhEdPMalIuAhAk3BXbCXhsWOwOuwQw3KgVPgAI5XxgCnvMBhIjh6gutTMaYGdrmqYTVfuD/l'
        b'r8A7vMGc0zoq/rElVqPMxeg8WQfWMOh1oGbGXxXQLG1E2WI3CVtu6a6wdMcZ3aXmSjuHjvC2cEyALBo/wELnSAI5PMSHR9SQc6MdaORiZJo25ejSMaNthtSmN0HuMEbh'
        b'MGaHvogtKsaEvUMxJ2vbPYuaF0nYksmSKZIp3bpya77Cmk+ofcXFO5aiPyxsByimmSeNL5WhSzUojacGXpJwWo3bjcXGGIvxJEnkgIEYz0fUkHOjHVQAzPDT963tRAYE'
        b'InnOwDLBl/WcLzshUOe5EAY6QkurxHAWDGcnRuvAWAY60mux3qC1eK72n8q0etQgdIReo2uxUPuEflGN1+c1lAYbmTHjmbGRv23RzqGInwnBgcjKrafxPabNYr21MT1f'
        b'ZUFVWXZSkc6gWdxcPYt348XckF7MN7I2sjdqbdRGizq2ZcPEn4bEns2k0RQt82aN5miRt0D7f6qR1cgpNSeLvQ5a7A2GLfa6ZLHXGbHY645Y0HVW6KoW+1HThiz2K9ij'
        b'LPYJxcXYu7mqpGGoXwC2saHteWjzo6LqmpoS4YLqquLyqrI/oC5DS3BUQW1tTVS+Ri+TT5ZRLFRU8/Lzs2vqSvLzfVV+1fUlNcRmmZirjSis4Inmabyigiq8uNdUYztn'
        b'teNjbUEN6mW8woKqiidLGEOskIbtEUa1QXqi3PFHsgpuCGwkJVxQUkSe0Jdu5VElj8e++FV18wtLap7aokrTXelqPPacb5hbXjR3iAhEnqiqYH7JqDWopp2A1e0wt7qy'
        b'GA3ZQQLVMBfh+QU1FcNMCjUvTcijyQD8eZnYG7KhXEjXAEmFc6uLeVGldVVFqHugPOpNbv6oBalrX1RQWYnecWFJabVKPtNQDdKdoA57K2N7wIJRyxnch57YkhqHoije'
        b'cM//x96b6vs+yYtTVVZhcOHIUgbzB/zJ9Xi+QcJsViZvTEikXxD5XofmUDQIi0vUr0pdFur6dC8Z3al0fElpQV1lrVA9RDRljfrGPYU88hXbbY6o3BCJV9Uz8aMsQFte'
        b'9NdTyOtDBGGLUQRhzwziHlcJNoF2YXANk2LM8aimwAVwHYqIsRy8ljfDoH4hg2JUwq2wkYLtSAzazad958aCrWyfDLiNQTGBFB4H2xiJofBQHXabM/QAu8A50IOunUxL'
        b'017+fl6wMcA7JR0J1kezF8DTtVOJiRwS7rz1IhID6gIpQpV3GR4ZZBUIjoEjucn0vvmxRV/RbF3Qibn9iIj9dbghjrjkFVj6U7ZeijFV54HlMTtLrKPT2OTR1F++fL9U'
        b'LWqsD+zS1oZtnHG0d+BJW3jRBzZrg7VwExJGKLA/NYWU/FEoibpkGlh/LXVWWTjNvPyrNaHt4wVqOxs7J9rTJ2My1YHLAqdsmTSRFvDzgBisgt3gADzAJMGcIngkJgm5'
        b'IttXl0ILemDg1LH5mXYOFMHW4DZ+LmF/zEomoFYKqv0WH7QhSQe9jx8GpSX7pqb5p/ihBRM28Q0XjgPn6zCMAS94g1NkTwP25Aze1mzhI9EYHMlWKWj52hRYDS/qgQOg'
        b'MSWJr0vzB+51c1VZO8ELISqyRC8gJtTS+fCCsQBuxkSJC6bMZgTAA/Ao6QU5bvCciixRH26gyRKtMondZDxoB5jakQMPPuZLNGVZ2k6m79cON8xRExZKY1WEhVe9CJHg'
        b'whTYqCEshIeMkExN8xWeN6Iv3gAkrtjYbLcN4QgjhIVB4ECdO26Gw3APXD8KY6EWxQNXCGFhnSnfgLz9haloy0EIN8GmaTThZkQloXpMAtfGYGc1sB0007RxxF3NbA5t'
        b'FHo22RuunzfII432RsubTXeq85bmgmBMtZkAWwjbpg24TFoywDxEZW8YCbYWMoLgAbCDtCQnDewT+C/1U9NtYqrNzGmERjM3c9Igok14CbaiDIRpcyFsJ+0Rn7lS7fwG'
        b'j2mn085vYN1yGv9aC88JiGedTVSAxrHOr5Y8SFY8aNFQNprAC2hzRSgbw4PJtXw+OCRISfcB2wfprlZPLKbfQjdY5ZwFRViyQz1iG9xHVaHGOkDIMJVpqoEyxkDbJWAZ'
        b'TTruhPZPR9Gz7MxkU8xwO0MKXkejpJ2vT7gvwa5poFdoXFMHTxnCUyZgM7xQi9p1Hn8OKwVunlqHJetseMJtaBYhPFunRcGeAFt4iAX3TYSrSMakOXooHw9u1GRtqF2o'
        b'V2NkrE15sdhwDRqX6+t4+K47wKUJ8EwdPCtcaLgQbDWpqWNRFvawE/SywtNhSx32+kJ70L3ggHBhnT4pygSe04On0I0NF8JLODKSqhZxs7W1VuTTD3Mm3VKTX51uURIB'
        b'm1gJU8H2OoJGH4JrZmkyqeuXHkA5ghNsD1twjZQ0NwUeGFRSbQ08iyo4ATZPYkXpwz2ki6ApbPbjgtD0qg33mFGm2kx4wiuBDClwxi6ybokBPF+LKmOoZ1SjRRmtYIIz'
        b'cLMZuYs5OO6VlQ53ZKGpflcWGtXH0ASP3ncbA54Hopnk9aFHXj8ja9Ikijiwd8C1VAE8AXfSNbgC+jg+sHPkHcCl5bTt9VoebBLC8yY1WkIbigkPMbz1wFoy8weHToBN'
        b'aLqLNhMEpKdl5uC1YYpKEeOL570tKWlwM5oFwJoc9FqDyFDygScyBXArC6xGK1QUhQZa4/Q64lzfk10C1rjDM8loDhD4oWGTwabMQDsL7G4ArXRgQBs7KpSidAMd92av'
        b'YDHoSfmMozeVjU+abTO2sLKlPqXXzp/jVH94xfPZdXgzMtMctMBVqOPgLcBianGEETntDI8tgpJScAytBUuoJR6grw5v2izKXEqKiF05tQicQy8Mb9vgOqt0eMQCNqG/'
        b'y6nyaD2yHSw3+E2bKbRmUdSc50OPTxVUvxFv+l6d/Qsn3ep+bZzxqXzMwRhvYx7DfJzuQ+s+2W+OvF1HXzqel/2mefaHvWN5/o2JTWd1WgS/utocrr365ZZNJhGphduv'
        b'//LJqTMhvx34fufAc+J3Zj2scNxyZNmS5+6tSxAJJjzMqAxcMr51YdZeaol32LbLnltnbmw9evfihNvs/Yem1CR8cJVf93Zb1XLj6H8FB+rO+TTxd6MzxlXL7/1gJ/xV'
        b'3vDrL+6Bvgn/qtt05gfd/Tta3MZPm2bsMbDvJU+5dNUp66IpbRN2Tfqk51PdV39SUDc9ll3+z7ign5ZleNi/sqLwM+mWH3J+zFzX9EHr4Y/KNzya1B2wTOFyx8b0mseh'
        b'w2Wbzd+z8GvpaPyx8PeunDG/ffZl5oud4S6Zt08tLl129OudIakvxiYz3vVt2nqx54c7XjP2vNw4sbfeJ6b/gc65ry5MOvd14Z01n3hvlxTucbv8SXXeR1f/tU93kklF'
        b'VMU78kr/h7rv7n25a+0py6P32N9ueFhVuPnBrbmnTnNZy9cPxH4b/8qxhtMP27bc6gGTjbSOOc2deqmhoa2lq99014kD/UbZtp39jt5fCzqi742pffWdrHMBOptzV38I'
        b'xggki0y96lm38iRv5798b3beC64Zfu9ciLjxILfll011E1bemWLwxeLExBf/PeezxUYxJ2+caw5Vzrv2dvB7ac11vTZLJ71Ufmx6a9CbwrQf/bJSfph+0OFEYHV+rpfN'
        b'2NP6Fa7fCn75ijnnxTZYNb0o/e7V+iydHwucvFeuenhq0qdrPytofs2lXvn8+++cM1j69q6dsaljHZ9/fbHXBu7lEw023w18vNW8ac+nP7dYXcrcvnHaT5HLjiYZRt+Z'
        b'HP3VygGQ//vL/T/FvPJtVtzDY6/8qghP/nD7he7Xo51SPvzXofe9AvsK7YqSl43JT7zbHn8ro+TOofQb2wNjtitLP9zW0L311cpPzvidXx7SdqO11Pv1sMCsWQtNzr1Z'
        b'PPvNnrbyrz/cbfbxcs6mHw3H/8b4YtbVRsUnbydmHw58v3/3oe9175R/HvVC9b6vak/lahmUrbtqFrm4w7U+OcZrUd6r3ldXvXGrc3FS1eu2ol0v5LiwZ8ijP1z2Myth'
        b'k8v2pXF8f2JPngJawTHMUTrUrto8hQUkcHch0cnBa/AQOK2SWopgJxJbwFlwmjYDOgMvYCFinUBtNZRJ8pnBjSywZQrsJYpHL7g6b4jeEbY7qLwAdqnjNFxEC94qQZoD'
        b'vDrYD8BtAalmuZvhdNCkNlwfYrWOpsvTRHUZYAl3EJP6ArBKpboUJRKn9Th9YyTizIRtGpP6kHB4gK7/CV+4a7jeEu4KUpnU75lGQ9aHCqEUHMOBKZpA9+PgFPCwC7nB'
        b'Mh446ZORDrdqg4PBFDuUAY7A7tmk8dy9s7A+kw2uaPSZ4KoKCUcrtgR2alwU6kEHrQwFWwV0mzQVgB4cYhAt9RdUYQaZro5ASlKT4GpwWOADToCtYaja2pT2YqYbWkGl'
        b'pOwa2J1KAhuC7VqDQi6u8ALnSJXroLiB9qyAq5xoLfIk0EXftmueG3GMmAlaiIxLHCMWA9qTf7EQbMPtEKBDMZE0BboYOYH6dD/ZB9YKCWiHNkIdNDsAEDMJqA+3U3aR'
        b'DrDJF4uhTahB0n2RQBLAgrvgnmyiX568EMlPabOhaCh27wsuEYLgEEGJStybDtuQuFcD1tK+BWB1jEraZoL1KmnbDV4kNSpbDjpUQjXcH0AL1eCaNnnKEmdwFZcINg8R'
        b'qkvyaG33evSUzSqpGuyvpaVqtIBfoFlnjsCt4NhjwfrCZLVgDfbDdro1dniCLajbaZk8FqwNURoWqRqmQcmoYjXogqeIXG2TSTtHtMNmeAwTihObBXjGGmUygatY1drw'
        b'PLkNA16Ap3HMxwB4PTcTB21ZwfSeXEwIfOFG0IYW8+0Bg4WyhfCcEexlBIM1DF/YpaUHrqEXS3yOT8NTSLptCgDH0aJMXpAubGOCzaBnOnnoZdGTSfyWrQKwKSAFSTkM'
        b'yi5JC3Sx0Ug7pK0qA22wNuEAoeAa3JgShgYRpQM7mbpg4zTyGtHecEMC3OSoXtonwTa6f5xOsJsMNqnYhlXRwyxcWXBbA1hNpoAKeEmHTvZPh5vRdgHdHYrh1TA2aLcD'
        b'qiAyndM9SJ5MXySsoLfDTJhEWYex48pjiQFIKGyKo8vI8EsGW/CoE+CRUQoPuMMOrfxs2EI3+z4nuFmAStgIL/niv/C7MQBbmbAzJJd2/mnL8MRQC7iM5oNNvqjZM5j2'
        b'4KopaQVeMpJONK5DcNVM2nuINRlc59LRcprAEXAYnjGBLWBzvQqK0YNHmKjpz8Bm2pblCNiLJ4cAP3gVbuJ74T5UxgSnnWfynf8eFuT/8UGI59dhqpRVI/6p7GcKiouf'
        b'aD8zKI3AMx7aNDyzYiYOsdMSi1GKaQxJGWb3wH8p7XiEezm8J7ovq2/WjRzZ2KzbJeI4uV2Owi4HAwzTaN7l5Nvhr0TL+VPljrkKx1wZN1fjtRNH0JxBtjMW9jILL2mW'
        b'NKvX5sjsntl9Bf1+cTI/Opsq3KWME6m0sN4Ro7RxFnMlbt3+vW5ym3CFTfgApWPp3xesdHLuaGhraF3cvrhjZdtKuVOgwinwnlN0v1O03GmswmmsmK10dpNYSLKlzt25'
        b'nfbd9mJtpYu7xFVSJCmSukkX9nh2VnZX9k6We4yhWZ3vuYztdxnbVyp3maBwmSBmiye36mBcBgf/ZLTqt+uL9TUwzWGbLhtpaKdTt5OcG6TgBsm4Qaq0oRnNccZOu247'
        b'OdePpjQeMEHVJ89ADg/x4RE15NxoBwLtjJJmStk7YvhLEiplSJ2lrO5IuZ2fws5PNP6+hbU4WhwtqZXb+SrsfPtJ+CHSwhPltskK22QZJ1lp7ToCj7OwbAnfE9scK3GT'
        b'W3gqLDz/AI+zctxT2Vy5o6qlSsS6b89TOnrKHMdJE08mH00+ktqTes83vt83Xu47TuE7TuaYeqNY6eyttHNU2jm1xyjsfJROLh3L25a3rmxfqeS5HjbqMuo06TZR8tyU'
        b'jq73eW7dhgpekNLJtX2ZwilAqf7u6tkdo3AN13x38+pOU7hFKl08sKlWmJLv12Ov4CcOmOk5Ww1Q+GBFOXt1GyqdPNqXKnme6C9X7+44+i83H4VbqNKF3+2v5Acq+LHo'
        b'Kid8FTrwHbnmAxQ6iNgDsZSzO7mbyAh1yZYYhQUhuJnBUAaGnjVUBKbKyOd2+u10mVueKB1VEr0Odo+hwitG7jpW4TpWZspThkacTVOEJsvoT2qebMYsRepsGfp4zkHp'
        b'EnO5qZvS2V3CQUOvWu48RuE8RmSsDI48G9CLfm7EyqZkKxJzZOjjPlVkLK6Rm7rcp1sjROkerPTyPal3VE8WPE7ulajwSkR1UPqGKHwTZL6Tb+TenImfOkbp4X24vKu8'
        b'11juEafwiKPPocf3kbmM6bVUOrsOWBpYocdGBxFzgEtxsLE3ngJCxlyIOR1zQ18eIlCECGTkc3v67ekyj1zRONHSHZlKK1tR8Y7SllIRS2ltK1ourpNZ+0u1cXeyRh3V'
        b'zA1Take1RbXGtMfgILJ2d1xDe7MVrlEya/wh80fSbY6cny53zFA4Zsi4GQMsihs9oE3Zu7bHSJlSMykT9Zl7dkH9dkFyuxCFXcgo5aDuIma/a+0l5SjQ7WtVADMJrrpj'
        b'Wcsy/MVFVNuyVGbthT6SKfRvdJpr12HSZiJlSyv6gvtq5NxxCu44kZbS1GKPfrO+OFQSLLXosew1P2LbK+wrFunLTRMVpoky00Scw6jZSFwiSWifKzf1VNBUMuisSbOJ'
        b'hC03dVeYustM3fEZ42ZjcS3uzYFy0yCFaZDMNAidvmfq3G/qjAab5mIrbkvZnurmakmx3MpHYeWDmxRj5Mubl0uyaFx5gNIycxlgsi1d8ERj0GYgSZRzvRRcLxn5/Pyu'
        b'nQuavC0HHdB02d6Ah5s0i+aNR2/WxkVp7zzAQr/JlwEWyofnGbTf4NDPTQdRw72XQMhYiwnMEsOSzFnPm7OTrHSet2Gg411jy6lu1F0391xD1j0DBjrSGLIljSFrkNWa'
        b'OgwkazDVmvo/xZWfenHEonQ+/W/oskhj0UdHM7ActBBuxni0kqLxaBUmPXkmg8Egfpj/h8e/zfkPPSB1VC+Bop6jjBOMWXzWW7pqs67HbFJFbOrxPw00I0GHXaZqdJsY'
        b'q+mosG0DFbbNJOg2xrYpworCarQstSDINptJbRqGSi/X0hvFMA2d0RqBXrNXaKmQ7VHTBjNjfpDFHAXZzlmg8i0cCmwTiLdABVFq7NueDBercwxl0qhVoa2DivBVga5F'
        b'BVWjInGFGFTnlc8n4FvNH0Do/w26jPH6Ue/qra6eN4+wZRAgUF0PGtalq4QxelT1KhpKHR3Z5SVWF5eERPIKC2oIFEk/cE3JgpoSYQkp+9ns9kgDqoD44eTvoyHoqPjR'
        b'mXNV+KwancaA8J8BmM8KV+pSI+FKp4y6cDwvrgfHstAmJ9Mfbk2fgzZmW30m/4Enwja+HjyZBw4Tmz8gcVk8GBdMxhgZbMzMGgIQLoGH4Rp4Wg9sXckmutra6EJs8gcO'
        b'sojNXwGLaIv7kwwoDkVxz5jmp41ZrEsJcda61sgso+imBQtZFHMqgzLJqZtIkQBF1+FGHyBdmIPVNY1wexY6bElPI1u53BH+c0N13qwcI3gIbARiAivGg9VT4RkGPAmv'
        b'UlQ6lc4CrTQlZEvcr5Qp8zOOTmB+CTclYzyttFa2xmeT5I11edQ7lFeYYf6qeYv860Pp5KQu2lDxyqwKhoJJTQrk50cLpllT5Lnnwl3xIWx4Ee6nqGAq2GFhXSJFQItG'
        b'IcajQG+Imr0FNvqlpsOdGJsMgFtTVKhvMnEVmZyc6ptKR/lBm/7tRqn5ywlK7APXBT7RALMC7hruT5IOVvEZRL8/xRM2CzLhFXB28LabDtkdPJmgd3FQ5OqjCfjkKKSj'
        b'5Z0E1+vG4Ee4UgxbRtxbhZKCNeBwtpfmWrAaXNNbDtdBCWmoRHcWgXo/Zuf7JpsGqDCC+Hl0MzKTcqmzlFSPGb9qiVJnY01NC3Z9xyl8LQIRgNVV8AI4RsXPIMBBLjhB'
        b'TjvAg7AHHGO7gzaiX2Aa0iDBhqpcHx24NodgB/B4LB3JbzVcj3fqVBY8RsCD2SUEyhuvi7pTE9wkBPtQ72nSpthjGOAkuAZpHhtfs3yBP+qHnZr4bDTSV1pKh8vbBLeA'
        b'Fqx2EoEOojkgeqe5FeUzwXUtoRWa9ZVfmG5tuVr1dqDpCymTT1+rFJx6NSKjyz/BSZJ44dqEw5SDiZ+IsunGgUc+T/p2Qm5GXnv453c9v5jc65d17ezufOXH7/6n4YWP'
        b'9q18bWXQmWX5v71QkxRzqHLhyqW9YWc+lTp+eoEZ/mDJTfG336/de3RH6TytCZUPz4ztGXPnjeD80gLv708Yycy/8qvb9lvuoe/e3Dvv01mGVxa+vuHTm4lfT28dW3/2'
        b'0sBrdoaZm9+c2Wa+ruPViYdaC39MXnxTd7n2+O37MoT53/yQ0j72QcNXrAqw5/7lvrKA9jNL33mQ9vCT7a2ht77/uHFs1MVNm7Ye8d3w01GWpXLdK+GxPyxL/ulYgPiI'
        b'VdS68RNT4y8da7t56ZUc3VbzL9tP1YV+ZZbdnRe/7ajp8/tTb4xfXy1lb5n8efbkqze3hHgXuWf/HMYtnV/8veMvPmG9fRaV3Y5HJvvtEO8ME++fdXxN45c/TVpcM7F/'
        b'G/+uRDirzn9L6L3fX/n1atdH/3n9zOb/RL5++/AnNq6vZxv+8uUr25XvrujK2nVjWZ1EEStMCFk4e3vUT8ezor/z/OnVL6OFFYdbQMuio88p8p8P95764ouhvye9rNze'
        b'efHD85LbvHff/vD6ramPDPsUrS/1TnS9V3Eiq+5EzbRvLkWs9bmQ1HSmYd+Wf7+zO5tt2aeb/HLBD0veLdx3/kCs+VH/5Jwvcs98377j3I51n7YXeyx4433nd368rgfW'
        b'eJjub360ZeP+pBWln1+4ruV9oTJBwrcimtmFU8Bmn+QcC8KDQrtO7QYnic4yEjTDEwKN7UEI3EBUs9OmEa3VOF/YO9S6VwscobXsO+cQrZWDDzj5mKG1Em7TZbqA3bCN'
        b'9qravqRUkFIKL2ioXSeXE51dgxeQ+KRGRWG2GqJXX2ROgsq5pULRSHcqKEpSeVMdrCIK4/mcUqxUbMtLhlvRkE9mgDORibTS7zjcqiMgFhoCP28coGwvvIwmHyb63U0e'
        b'eC6aLnag6ccbtIAetKKwixngCjgNdpHUcNgJj/mk+sFtJNE+Xs+ACXaywGmSOm46Wp9QlYgXCRrQB/UcmEAE+wyI3hTsB+cX+mjiXIMDBUw/sD+WkOSYoqkKk/fANvsR'
        b'6mpwFHbRxtSn4cZ0HAz7DLwYAKRpKlDCZAxrJlzPp8GFdtC6nOgb4fZ0sNsPzd5omfLRpuzAXjbYJ9Qi7cNhgzX44vS0TC1K254XwWTnJ9NqyI5qX58MeAI2j9CK5rJJ'
        b'DmtP0KhSiob5DFKLskF7pD2talwD1hUN1YlSY0AnVoqiCa2LqKODrMHx0dSi7uA67MF6UbhzGuk/AfC4G9ZIEm3kYl+ijwRb4Wm+0/+9uvHJWy3cDIMFpJFKSHVs78HW'
        b'fUvshnvsDkokesgvVBHhKvMZFNdWZRM+V24doLDG0d3MJtE6qMQbc+XuGXLbTIUtiTZl7YBdi0OUDs4deW15rTPbZ4qSRElKSydRnkRbypJb+iossZU1zuItniUdI3cI'
        b'VjgEoyyEi7gU3cIiQGFBbuGjdHDF5t6ts9pn4Qw24vEdqW2prWntaf0WXjILL1KDeLltgsI2QcZJoA3SvSTj5ZZ8hSUfFxEsnaIySJcEtUa1R0mt++0CRYnYLn0QCTq2'
        b'Sw9+9CSK9McHlV36CA51a9sByhZV146H9a9ZtAv+ZLnjFIXjFBl3itLWqcO7zVsyTW7rr7D1F2GGWTvHDp82H0mR3NZbYestSlS6eXYn70gXTRCPue/ggp7W2l5c27xM'
        b'tIzWmk6V1vXWHVkudx8rd45VOMeKtZU8N7GW0tkd/WXtIGE3LxctV/JcJSzJBGlO79Qjs+VuMXLeWAVvrDqXKiuuYaTS0bljXts8qXuvttRR7hihcIwQs+7jeHwsy2Cl'
        b'V7BUvzfkiEmPSauRmC0uU9oRjUSw0sX9sHeXtzSrM6A7QJx439Zh2DNY2+H2SKd7hkBum6awTZNx0oapfEbqOJ/B58DRRzxfOr5vvMwxQe6YoHBM2GEgYotKlBbWYl2s'
        b'LH/ihc6e95yD+p2D5M4hCucQdM20HcZKC6sBytTMXcmx3ZPZnClJlhbLOSEKToiME6LkOIvSJW5Stpzjp+D4ycjnvq2j2K3Vo90DPSzHmlyTIFko/X/tfQdcVFuSdzfd'
        b'ZJrYZCQJkhFBESSLgGQVkCxZAUkSFBEVRHIGJSfJQXKQIDJTNTs7OxHfsPMYZt/Mm7xhAr5138w3O7vz1b1teM+XZmff7sz37dL9O9zuPvfcc+pU/avq3HuqDJ4KLXeE'
        b'lttCy10NnSaPXQ3NDu9OmYGwpxrm9Eldo8Ou5VrTtV0d/Q7urs6BAfFO33GJpzrW9Ika8W3x7UgaODtuMH5lzmP1ZJPvU6HbjtBtW+jG/BrYEjhg/FRouiM03Raavrzo'
        b'qadCsx2h2bbQjPkmqCVo4Oi4zM5BuznvnYNOT4XOO0LnbaEz/fa20PgtoTHRVWixI7TYFlow9f1a/DrymWjeQqNtoZFoLYm1Og9rearyUJXvqSmJOlwqRQtHaqKFIyZE'
        b'7OvFic9npehjIY1p+aNLR6+Xj77CLB99GoDJyFErX+K8WD9iFo/iuVwuE9/8v7H43HZE3CUkNuOJKG/JzIGVxBtrQ0wOPtYPbqHivvQH1oZ4VZJVYi9yt4vWhzjMCtFF'
        b'uVerQW9mcP/8V4Mumon90OPjNjW+XA16ncD91R5Fdmvj57wnWHTOyzjsovM+JgGYtb6n6BF2tiuf8Gg+u4WYWTKiqr4hwQ72NkeYJZrMhHzmAey8/Ny0rEuf2AVRAPjX'
        b'j6O/mZpI9PufEINBKoj1W7GLvO6NT961iKNY+mYUhk1Db9HDmo9x66q/2uVXydjZZ0S1Xjwc+MQQXqZhZx4Q9YVF5hlR5rEDNrC38RktrIVV4QeyvYseQMUNp7S1sEl+'
        b'HsMk705s1gcdkb/jrtjj9L4iX1svsbhka182PDJiwF5CRvCNXe3vTaX+dnhKSfruqePfTbx49dLP+tziPf767nfl3zmqlppZaW7zy+V4myPGWj/93uzVCN3Y2SL8iU5S'
        b'ft6xLp1GNwvPZ+/fNXzftL7R/qu/fPte4sjbdjLqeNVr9Pc9tvlr0sanQgK131n59b/5Dmw6RHm95322yff7P9i6/buN9qGrX/f3wl9J6EYP/4vK6D9YtEU4mYmMWKhS'
        b'j3wRqJNclhMXYCYSn7BmeDg2XHoVCFOcI+UczsbBbDNnDVglB6z9gM8C6z4vgz0oQ5/oUYt+HI/90IMjhlD3whi35bGei5zLxWv2L59JYR5Ige6IzzlV8EeNRfkCVjZf'
        b'mYsH3kDbD//MGozvcUQG48nk/+y+QnWjppsDoU/VzXfUzZlbVtodBdsqRvTeNbFoOtWh9VSkt1RZU9N5V92gqWjAdNzzqbrNjroNY9847R60GXCZ03h68MTOwRMdUrsm'
        b'h982cXzLxPGpidOOidOLNsig3FYx3jVm2tRoDto9aDHmPOj8wHXY9e2DTm+RHmXvFZKlEPVUUX9X8UCTgM2KrGi2w4bkF70/sF9e4QN79F7h9J+oJtkwZ2/oQJHye8oo'
        b'v0+fjuuM+nvwAfWXnfQ5q7/PTbf9H4Zw3D3JorQcZuH9LzLPF5NgbuKjm/Ryk1LTrr6Ivf4iO+OHor1/jNryFK2JZ1xnF9HTMnMyUpjbACnJBp+o4l4Q5s2Y4fT1J9yp'
        b'+EwlwQ9iH1U3ScYG0SN0Y4qfsgMkUV0qLUKQ1pzyDbG8k3Taj0buMDGwRDnu1Gxs47m9AV8r+dHUD3O9Tho/lPqu8MtBo+b2EhKhxwLrjJMzfyF17Gslhcd4JxvsBJzv'
        b'nJUd8i8044uWKIbycYhAFWpIXb1cCzqkxT4ddMwSZ18vBElj+0E2eHEJNrNPIMkb3pa9ruL/0aDL1VjznBkbzhQYMlF4DuM81llhlS/WB2K9ha8dDAVeeXGGP0xJwpwe'
        b'3v30LGp7igmiiX4pXHmv8pm9unH5RgUWDV1foKF7CpcjVHvxCIfJ6zw7L6DP7QsmH4S+d9TMRDeZtxUtPpp27a1PwJOPpF3bk/hA2rVP6man3IfSrmUnE0Yw/tunFJ9r'
        b'bh12aLnzXGbROygo1Dso99+YsSp+Rq6d11FimchjbKweNv4Iu8GZvbPM+gcsTrKEMNP88y7QaHLeSL/zUYfGlpmvNxJNyDP3wO/z3sjII81k5GEKNVFGnoMD17YFh58K'
        b'Du8IDu+LHRAkcfc5f2zJZN+xeX2e64eS7/gyyXf8mZQ0VD5nSzb/zgcz4zAZZ9SZjDPqTMYZdccqn30pBSZ5zKcW+p+SVeZdgZAZ1LZA96lAd0eguy8mEOjtcz6tYEah'
        b'96qq7guyfKAFKSbb0IeK16cw3whfUjJvW2DxVGCxI7DYF9NgktZ8ZsE0ZPmq/lFRQ+HjdqsHd/UOjgvnmHUmeSIQFc+Z4l33U7vO7vu8Yi7TwH9V+Uz85fX2+ey3xTxR'
        b'z5LGeXMhq8LV1O2jPtuC008Fp3cEp/fFgtkz/7tLhna+3NcdiHnRyYPjKuOhc6bbpk5fOLUt8H0q8N0R+O6LqQkINv/0grmaH/dVS66ia4VsCwyeCgx2BAb7YjICSybr'
        b'0ZsFc6LhRyuIArQw9wlwGSsVX2QzsvSlT6uyzHEA87SyqYn4Ve+TBf9M8GRjBPegF1pcsrHbRhEqYA7r8RFuqB63h5IknJU4gVXQDC2MEuvFO3oCaMJyGICH0HrqFAzK'
        b'QgvUcLXxCTzCJwLoPIFL0AALCbCME6ECMZyBMpx1cYYnMHcanvhQrUasuQ6PYAIeWhfDUADMOBfjJo5J4hxM0mv9GIzAEI5eumJrjJ1HSLc+yII+vIsTuIDdxS5QC6NY'
        b'DfPqPlecg9Wg9iCWeN5Mt6NOb8KjNGesuOyjpZeg5X3CXzzS9oZ1MAxF6lhBKy47wxqOkV/YlAWT2EzNrJyGFcdMc2y0jcM6AY4m45wKuZAD0IKD9NrAtnhP7Dpjlw71'
        b'STgtwdy6wIpsmMdm7AvBaZi7lonD8OQmebTtodCsiYOXo7ENho+r4sxp2LCBOhp7MzQonYLZECgz8acOrGCXA8zexKmz0MnFUejCO3gPeuh/YyqMYxcMXtPlydKMLGG/'
        b'rSUO4Uqqg4wzLkNlkg6U+GTC3WRqtj0QHpsleWfreWNDGj7Bbj+8H6kB04UeuAoLNE1zLhLQcdYsjMZdC/ehXOZQKC5q4AMcpE+PAqESeiKIGPeh3RIfObgauxgJVXDh'
        b'PH3Rc8Mk2gI7cVJRBSuxCZZD8+jbZnkZQ9yiMyZxHmapO3McbLdLccLOGOi2hcfK2C+fGAgNl/JdseQctutCbZy9FG7Bqo4KrGbAljZUXKLTH+ZgNXYc0cHBZMPzUS6H'
        b'sZX4YBVG8xKI5dqwK1ROM6Yoy+kGLunEHoCuIBjUjMZZok87jkvRYJaIn7pw0B3rpKDSC9dtaBrbYMqRRvmQ+vcIyiJoBhqt3IgdagphQV0ba4g+Gzggf4uHj7Haxwga'
        b'HArqiO8DwmOh95wHNBDby8FjXFQtdqe5HfOCEl3owQ4ruaM4g0xOlT6eF4wmJRw0g6ZUPtTq3z4MIw4FRakKeJ8YcRDHia51OfHhsKkaAV3u0AXzMAxlCdhjju3QD30W'
        b'h3AV1+ERD+ak8Z42riSI52AvLIVFXnPD7pshGTCF3USKTVMaB3EITmf5O1EzfTrQjaVnIqj9lghoPw4dUJlIolcq5hiILTBnRXUWcBwmb0bfVFGMuJ141OcS9ihdP6qE'
        b'0zTYWmLlMpKKO8dIrKp99AKMrh8iZmuETnx4hJh8iphzFasSsCUDHtO4vHADqiVxxBVbbkB/gb9HGk6bYKUpVuFW8XHr21BxQToEVjXYdDE4puTAz8ateFwQw6ZCtQQv'
        b'vAuLMlB36zR0YKmODzREQgmWJysQBcaDQ8Jsk5QPaeKEh4+MUNnaRlzbLoxEqDcAq0JogjtwUgOqCFNKEnDUnmZyA+5gOQ9bgqAZ5/WxJwhrInASFvlKxHw16jBIw2Bg'
        b'qTzOlqEsVOFDWLpWqAn1unS9aeKp8UJih8oiJSkSh8WLeA/Xim2F0Eo0vEvzM0ewtSx1Sd4P+zVhBgeizuMUSV05PtKLhc1Af9iCMWkjaMkjQBiFCscUXMzE6gjYtNZi'
        b'brvGBMMjbWK5Kaw/By3+fkox1whgHxEyjWNfNJSSAG3RsEptcUrFJMRINRhKieDLkTiSQaQbD4YFM1wVh45EI3gAd/kFfyvGJmTpwgriSRdoZHiS+r1mAUsFjtgTw6d2'
        b'B/BuVgIMXJEluWw/dsYSRhXj/WHCFepwhaj1GNu1iY+eQA0NbQFmfaEimsS13BA3T7u6umCHHwwlK8pgOfHsCHHUI7h7ELr0rzJbgcRc4fF1jr21L7ZezregaVuEUfJy'
        b'amCdRKeFZK47MdoGu2OzCD8GLbE7nSi+wWF2UVCXJ2EI2vBejBfh4paFenh+7AUYCKRODmMTLpmSgDS7GdoWYp1QGtY+yLIkJG1nNKkry9ewzEr6NixlsZB5T/46dBJW'
        b'jnoE2BcZJMFc0I1iNd4FH6hVh9KLNLYtamCUsKnM3pUYuEMyE+phLA5aBTTLE/oCaHXAztMwkE9VSpEZDJMttQHGoERBDMtcCEVGVCXhkQOuaxwifliAdVt8IryGQ1mq'
        b'1/mpGVgC90lgK/CeAtFqmIY3io9h8QxN6KAS1kQeSCV2K8N5dxgmqj+OMSHVNBNZqEPs+yDTBZviSYG1m8HENZKIOmuajUEPW4K5amJMUpwxRy8fw2bTdBy/eVK+iDpY'
        b'BiXEzIOweETfNDkBFglzHskJsRXXsUwOq7yhzzaUWAIeXKcOVGOjKSwT00xBYxEOSmobEZE3cNg78jA8wR4Zb3MacAVh5ABp7e5TsOhz6RzN5SLcyYukGe0kfdgPG0VY'
        b'exU6YiVTsM3loo81q9Eb/cntxYoCAoUmqtPm7KMeQfDVfRlqxK5qQA8xOFGQGBz6otKpl1vYzzPO9vPG6iwBNqeESx64gNNa0M4w12ES6EFvJRjkFXyb4eyJeBJIAtss'
        b'1sR4jLMWuML10o2HAUnsPCfDhXlms3QDSU0HNOXDAocA10gVS44QfTt0buCMJKzDcIqPKXR5wpQKaYMuTareII89kpk66cQzXQokjR22ZvgkzPo0dJ+9gfd0oM5P9zhj'
        b'zMgQaZ5greQZoI6QtCRwc2JwORB7s3AWN2LDCS8Y+H1IQED2R7Y9dKu4W5xTxtlIaI4/BXe8YF0RB3xuRxNdBo7fUIG6kIBImDDGpdsHPOMJOCZpOqYyiShT0B19nYtt'
        b'3nawFmpzQ94TS6EbOlyTSC/foTke1FAiYlfgMA+2lLAlTF1RixRfjRCaYgMSQkl0N+3OnsggIW6NgFbr4xwoCxAeFuJ4Bjx0J9mrSod7h/COJxdLxM/AevJJuO+dBouu'
        b'zH6oqpOOnl63tLCTmJ+AcYSuWMnJJBUwiPMSMEBSUK1G0rJAxGrEHlvYhDpNEtIeY9i4iStXXIlpO0jZNWCb8xUc9CBMKUk+WwgVPtkkAAM3oe2mKrHVcvJ1nLikgR2E'
        b'gg8IKGqcsD5cyR6J35tw2IcMI+LoEf3j1IdeOhpyP17oo0iK8ZQWLIYwi/KwdP0oifwmTnpiHRGunFRe/3FdxiDLhbqL+iYMK2Kz0I2FgkHqZgn0pUFbolLR1UDsoass'
        b'kVi1Q0sa9WaCTIIyMWgoINLXad6g4XWT/pwitZkXAQ+ssQ+HNYIFIaQpxtLV8EEK3velGR7FjRjojacuzrjCDAlxlSPcRUbKN7EtjJqovJB6ldFBWJqpiYs5hC4LWG7k'
        b'HSWDc9pHvM8e4OFMQYsYG05gJoD4mobwyoqwwFVuJjaQFeHiYAGPbGDuqqyJo2QuoXuH93lsOUlDgQEPmuJNuvJiLhFphUGgCEOosMOyIwnQS5eugbmcGy5yuv6wibOJ'
        b'2E91Zgg82m/rQYnFeZrtVb4DwWAbrJnbu+FULJlo93EthczLBtJik6Sgl5FArey2Fd5TJq6tOhkLA37Yds6dNGtTijt0hpkzT/vAxgm6WgMZIwPwWIFkuxceKOLEaWg4'
        b'Uogt8oF6lzIJ6UolST76bsjEwZzxiVMBGi4CYrCHcF/e6gCfaNYro+yIS3qHpHjeeMeAyFhiTGw/oqTNRNWhNqdjsCwW7nmQb9HlSmqQoIkMBFyPwx7sc7pCcHUfxkiR'
        b'DJOZP0ezxD1jdR5qjbNITXfDw2Asi8LBmBNQE2AZSGQrg2rPdO1gn7OMCVMTCysGt2A00QzvJEGJyg19bCeF1RyNK7nEPG1ncSoeq6xsoF2MOK0/ACs9iL+2CNanL8WS'
        b'T9JE0F2tqUFUXorHVieshP5sB6L+uC1UuAKTAKv5SKTwor1jcCIMx+Nqdgzh8oCTgoyx3XGhpp0ZgfqSHFarnAoyIV24ZQw9YdRqi4B460km1Jw7T0KyHgMDh2BUmIzz'
        b'WXTBbhpp7wUShZHoFFXCnxaYtoZZWaJnDbZfgmo9WIjNuaDuBpMZVGkaOi8SQnTy0qlXJSHE8Ut20OgCmyakbdfw7m0hPuFkYLcF8cIKseXbxJZnSO/NM2xZmsVy5SZx'
        b'ZSFOpeD4dSkyfMpUbhARSw8dICt3ScdGGVsVyZQMP1d0Gppu6xnfKICKBI0zcXLnSIEPMS8oO0bY30ZAQqe5MIZTsaIAHhbS5K5j/3k3WVKWK7ClEI8j2JlOynZMHEsK'
        b'8H5oCmzeyKKfuhNjyZiZYY0HIONhAzbTiP0XEzWwPFcPR0yJMwZJeKZCs7C5WJ/goYcxd1OpA1UXTmRqyNIZzQQdbUSO2sBIMvUmTWHoZsjN8NRCQ7kgJKN1CEcMCb7H'
        b'YlwL5YnAtcCIbxOsZuW4KsOKQj6RpzSXbIqmiCA7aSOcSwzCO9AWQlVW4K4kTgpSsOqsBfNQ3R2ozIEuBXJW7kJfIS7EEb/OHZaz8COI6kxT9E6/7kru0+ABktNZApxa'
        b'bVM+kfO+DWm4JnUh3MvS1/MigX14ANd8CLvqyUNZIp28nsXs9MeWK8Y4epD820m8exO6TK0IAlcl6WJlOGrnk2JXaBBzkUS9lESirICkoUsGWo5gw2U77A4wplldVFHK'
        b'SyQIfIyTUTgZS7IzbMDEvzpORssjO6jE1ZwsZgF7iUyU7mJ1GyFBZrsb4fyi00HqdlMq1JPVII7jYaQvq4hXW10v43KYJpbz4R7OptB1e4nfujgHr7nkROWpnaEpnjc0'
        b'J4HphebkfOhxLYSag1gtHoO16dDpzGyDhiWyO9ux+jwpiloyTXqEAfLQ73fodjDx6EOcKYrMIFOxPcTV6zjjnU05wohHrnkMPCKuagyE+RtpwouEQp0KxOJLVjh0ttgH'
        b'W73NiSlm1A2x9HBAehg2nFEzk2CfKTbTwPWAUH9fcQ73MAdrrquyDyBf1lUyhkEmmooolIrwABtiBdsNGRfdy99CjMN152BnLDayP2iRkulRwSdMuFSuG/1An0Qxwx4Y'
        b'45wWqc9arOVyuH4cEiGoYZ9bdoEt21gNrLWk709zyKTsti3w5jF5XGLIf+olXVRPItHlLkfknr0loxctDW1O5xQSVEgym62JCwaJQPcZY/0Q3vX1DoSKdFc1M0KZRzii'
        b'WUSK6QH0+Sp6RBN2N0FPIjaSrUKyi/32zGILud3NhdYFnjCpxhh4N2EkJQErZeFBbgIJTCtsuUJJ+Fm8H0RTSL+TGJZ70eEwjHEIXSvDlMl66z5MM9VrG2VEDFd6gElA'
        b'ah5J7TZyguma5SkEqLNEl1aaYnJv0oqhwpoUa3MoNB0iL2GBGCGKbJfmQ4Ru09DiSD5SeX5cIDzxJy4fJhVRS/y0oEP+Uhn5ZFWOZsVQaUeG2zrhwxzpggGYMyA7eBw6'
        b'HVIcrvKwUTJFATtOX4YJe1zNtdDDtQs4FeWrChOSxQUpgblxBJ7NMCzNLBlAh44mlhJhpwiGSgkYR2OiqK06omdbpDCdZHWNutB0jIY66qIlEy6HfUnxrNPVxcMyW3Jh'
        b'Sogq00gQumULdTycizQPtsXyCIKzB044d4jkZczOApigEBPQ5ESWUCONpyRXvYDPpGPJozEMw+apaCYVC9SYQ58kPkzDptNw3w0HwsibqiOfZVNSFWvjDZLMPLXxoRTc'
        b'j4f7uSQfm2byBTiRlJuLo/RquSmg7lbbn48g93GaQLjZDhc8fYqVLibDsqkAVuSx/zTJ053jOH3Yl0R6AiqQWdSpViDPfQlKtaAnjsQf2txORwVF54ZHqZMpVEU6fE3d'
        b'Ae/lHrYjfFi4yiNYGIGHVmqwVZCKU8fJC2gyV8EudQbASdFV2twm4Vw+RnZiNbMMZRZ0kRQpPDoM3fnEUJXwKBoqs0h9D8PkKRLbaf/bMB1Hnl4fTem03wl25eUxj7RL'
        b'f/Ql8qJGoPG4uvYtC7I4l4IYBwKbL8IGDtpQsYWb+mrQlsLn5Vnma5CxNeWKqxcEWCrAx1zou3A72lmxYIJUF9WdJD55Y12G4HPGVd+d0KRT4So+VJPQuoYPkkk+ShMJ'
        b'lOfPRGONn1DNg/yWLWjPZQKzyQrFo+ICzhHsNNlpEfe0wawmjh7R8DdwhsUbTJCECI1gqyQPSVJpq2fPsws0C8F6dKEuaLUnujyWoXEsZBEiDZI62UzFlQJYMYNZqHW2'
        b'IOkYxZ4s+tB49Sh0kUojaG9iuHUI5s1hxiabbP2+E7iQHE20rgg8r86YmkgYPRLOJXvvMcl1qQ6J0LwPabg+vg6OWRDqLuKQynkYNyRIbYBu99wAMrL7LpHpWebOIOs8'
        b'lN7MIOte250MhSFNBWZhKwDHipQ9ZWAyM5ZAuE60CpCXRELQdNmYukW6DB/cIjBY0yFZ6CUPF8YCL3DSsfJkBqFOz4WTl0gpLGJPCvWwJZ+UcBmdQSY59iYlw2zGmeO4'
        b'pK4ITw5GET90CHHEw5qhiDlOqKfgWhqxDmPkT5Lj8DgXNy+IOytip/YRbAnOIVSrU8FBZXK/Wm+QGVUCW1fI1FlygwmlYFM3OyPSuwN4P1IKH/hkE9G7TU0KdM3S1M74'
        b'KCvhgMrtghMCqDgpFkRsP0k8WA2jtwgLHhScPw210YS0dyxgVZhCkvmYRGPlZngmqcksaOCRSb5A01cOawlXCW97XIojcCTSioCpC6fMYOPkBZjWM/YlXGhlJpgm4QlB'
        b'Wyfhw7QSDWMTt26dCaBGh49BS6aqTzBde12b6LHhCaseBMKVceKGbvnntQp2iFsNz8ZCbwjWvnJrw+nS9dB+VI/xbCPPyXJhWRmrgmBWwgqmoyXUYAIJApeOEQvMOp7H'
        b'TaixTnMk5mxm10omDa0IxZjluU4lSygnUCPurIA5cgvwybVgKzOaqyl87OoBEzrQqaCjRZSvg6VkktYhN2cOTGgSrkwaQ6cjlhgQ1i3AwwjsDyM1FUmwU+kLPcmRpBFm'
        b'zzN2ySA+iMw1EeelOmPbYRwpxGprWDgYimVZNjCcfpK0wjANd4wM1h5vAhxYC8Aay0jSG93mJM53rQzCU3HkuGpULj4JIk5rI81RflQoBf3pWTBH6NVHV5gLkiQB2MoJ'
        b'Joe9mZilDoaLaNCkq7Rw9DDcLyBt0h6UTqxELku7pSALymX0T+C0Yxp2+KllklKdKMBuR1j3yMV2ol0jzp3Xha1QjgPeFUjhFo96WRGoCmvizJrIkCOMXlI7DW1e2lqO'
        b'5G7V0JBw2olQ/DHxwywJwCNigs0r5HY+VCGidyYmMUJzMdWUQLVeLMbj0hU5WI7G0fTgoLSLF8hAXZCnLjBrclMyuOAPtUnQft5CHci1uIP16XIJ+DAUGlXc42NvYJ9f'
        b'4IEj2GyD8wdSY7DBTowxWAl+ysl97sfHAYXFNPraREXSXA/wiS7fGNpUzmFFUoTPhZOB3iTcdS54P88BxsKScc2Q0GiGCUJCbqFEHEHDQ9lIHRZeGOC+R7TsSDoK87hs'
        b'aEZy24FD10ncGmDOlMn3qyRJ+nEyJ0KVicGTjJtnrtD01COZB03SsKLsZE141ndd5baCCclWJ5NbzBKr4qDveCaJZJU8a9FcIie47EOsTX7tCk9MHcex2V0hF4aFEukm'
        b'hLe9NJ55QsO2I1y/UF/GcUrC1SRcFJBYLdPwH1g6yWOTTtQBPvF4F6nvOjLeHxYRwe8fDZUOgxl77Iog9u4i0F6XZZxxmNIJY6Lh03ga1LA8xJuxfFSosek4PRixxWkv'
        b'cyRzxu8AUajWEPqt9Ug67ztDtyqRpjuP1M5YCsxH6DARrsTOHdWGIU1HKEmE6sNk9LoQFuqFmWkTSrSkYpk0zKfk3ibNVQZLkfakTxZTGACvlcw/Q9BAtsuE3HEicyN2'
        b'asQRodaUcfCSKs5ImRZ5OF9Rh97jMBtQTLw1QupvGDs1cSXfDyeUydhpJE26kUq6oEjGM5fmsY8aaTF0yIdhJ/4RnHYzgnFXGezJx4eKF2M1YFRJ8Qq0qmKd/yVqqBTu'
        b'WUraBtKckq1BpFnl6wfmuB8/l44zhgQPEyRJPfGGuOVN6NUOvb4eLmTnklIYY2xvwq4WWJG9iJXHSEUTo9Z6wpyWNJfw4FFcDOHeCE3LKrVarqQaTpq8Hoak4G4qVDji'
        b'hBUpgKpbV6HFIQaZRfJBDixecNImVFmHijQTkrYxDXhgRaLeSYIxRx51T7y05jHcUIf2UAf/HB/Sn+NMMF0+nXIHFvWFjuRuDMGoB0yK65BA9cCWsaomWbP15thUjE0M'
        b'aaqvwQIv55ATfdvsDIMm4bhGihLblIycjbDPATpSIoh3qrAtlxTTZmE0zh51DoOyjHwCx3vWHHsYTSgUJiYS1TNScQPqE2HuCtnPzWTB1RO15k8QtpYbOZI7uIaVuSf8'
        b'L7oQFlRhzQ0rIu6CHJe4b1KOsY1pIjuT8wpvwmowfRyCrgDyzvthNuc0zoSzanEJN5yjXaHdlFQmeb4+LrjkRxbcrGzyETLlOiJJOrYkE8leKzGkaVgqEOexwUvnyTQj'
        b'WSollmaEaRM3LAiPO4hDVxxxSYPM3QhslUkjK6/eE6aMsNvzMDTzSMkNCJhaLopp5C8+vnHp9GmyCMr8whz1saIom8zsTRzzIB5YgH5pfGwvmUHaZ4qLD0Jw3fgmlJDn'
        b'd/+Qt4JsCLYls3fXppml/ts34B6sM2taQ7B2jgZK4jLKrBeRvTsCo6fVsPP6OZOowzTE+zjpjKW3sQGXdUhBVsVAfxjZW8tWEqnZthowd1qG5P8hVay3JepWZJAcbCrg'
        b'QCyUk1EwRzqm4Qg2aUvSOEekrXCmOJWsu4rEQrjrQpq5AQZ4uKAhjd3nNbw1iGkemoorHsBVtzBokneXYoKaYokPWTRTDLIdwxkO6fD72Ggjn3IGyqP9TR3y02VwUzG8'
        b'yISQnoxz18wz0JiDrbYh5FIz5uiiY2ox8Ui1CcwpnfAnOX6gDusysBJxPcMcx40JvR4RzJVfwPVCGazwCiHZKCfnZJywp5mE34CI3a6LvXIyvIvqWBuVnhYbZ4dd/vJc'
        b'LzU6bxqaJaBFSZ1krhUepcv5WhzGFV1m8ZP0dwk81oJHzN27MZ0D5PjVJbq50PT2HSVaPICZA1ZZ0BxwkCSjgfyfvALoPEpzUOGLy86yxCsbZB70eBWp46DcLXEaQYs3'
        b'dKlIF5PQtdCnZtiyyIq/Dn0G5FaWKTsEw7IG9Cged5G7hnf8sFwnThLHQqElFfpgipio4Vwks2CKYwXMehcwz18/JA1NTeGwNVbdijMgbU1m0Hmq2xtEg7kTjitF1mSb'
        b'kRO8RjKyCVWykYkFUSSU/cBoFDJJh+1pbFs34Z4utqSQ1b18hbhl+poGMdXUTay8DdUE52SA3ImA9tPYV/ADxrafIs+p6ZUkuDMLU43hpI0JxdLd9M8pGGGTTJpnuNEN'
        b'+rlH81KStAYOazoY0fRu4cwleCh5Op6uskKW0oiYPa5owxaOHU+XpSGV40A+MLeAS6OcoYUPbRoE6Y+vYac/DPLocBTWU0jnjN8isWwkYbpHk9Eso4tDfoSmU0T7Omwp'
        b'ZhIBOwux2h42rHDQKBBrM5jbXL7MSlXyGaJO+SHClWo5Pk6maBHfL13XJ1FfOxKcTQw3rGJLfWuxUcO2g3pm2H3IiwwHkg1P4oZNYSouy2GXkwGOCIgG5TFQ5olr7jAl'
        b'XUgQ00pW0H2C5yEOsfy6BPTqnIZ2WfIRRmwU4IHHEei0I5uhXCNUFccPHpWQwKqznlgti3c8z5BnvGFNhlalI84r5ODyYTl/Wxi0w1aPE+5ElEXo4pPUDxPeVxTF6yvC'
        b'uCXNaBuZW6X6xOvTXDLPbl89QuzWeg7KZVmuWIsjCN+6fIhZH8HKbKLaKAMDyzZkf7ReTIUhB+JnZgm+FWvUcdGeHJvmS1AlAYOp+jDOh1nXE7jC+OhYcpbQayngGmn1'
        b'J3YSZFoPQZ0pllkSYWbVYPAmtCsRW1YZMveSxYsl7C+FUsv3nOWxjQwIiWuMGVSmciyL/D0y6e8QQjTDqAp2nlIvZB6rCCHKdcH6havGMGkFj71hyEwcOg2gLvYydEfA'
        b'xGXyeqZhyCqOzCBS3fYnso/Cup/JFRw0hg4/GLWw8cJFcdIr7b4G5N324sIR0nITjJB0hiifsiNunbLGrTAjgrb2c/HycTdDtSKJdaqw5FgA2XIdB1303G8yN22rLuOE'
        b'Jq6ZibHrRxLYd1MUI5iJEKwrxzUnpTrBrh8V4nRanu1JfSZSPROn3gDvmfFEkYXJB0+jGR/zZ9aWHDg0R4OwyS5UyUdB/0ms9GfCUHJtOFjnC4/ZEN2aWGqPUzxmwzyf'
        b'w/WkcyKxmz2lkPi9DuvlX62R8WCEeseuh9WLX8FWZf9g6oIt/cLcRWdbu05T0RFH160NoJMcmY27dzXZU/jROgwtXi+t4Yzvi9ZkLR3ISu3AWjM6J5hDfW4UF11mAwck'
        b'ok5ibaBoda0ZWuNYEgiuYasvjL9ajoMlfTOuKLDAtLHgAkz4+1FTFhysijQU7epfIUSaJ8yq+sCCHKn2UjOuN5tvng1boJzDBjXI+ZZYvJxecgHHTBThYt6b/Tr1a7Lx'
        b'GW4ml0VBkvE8+6WDn0x8QNUJG06QmVgQNcUGOUg743NZPI9JsffdU/z79/46WPus4pd/8Kt1qy+v/vhOZo1z7T/87XPdokoj0zGdXHctx8CvGnj43X1X2WDzu4K3Tc9B'
        b'p+wfkp/EZn/HC/j+0U+u222Z/Xr6dpB/YNFw+O+G4ySGraOTz6x8tSmjNUGz+axm65XOJt/vWofYWtnZWjglB/0s5Yftvz0yIBumUev9h17DL7nMfLXxXmPXv/w+93yk'
        b'8bF/zvY9Wpje8PMjzv1v32j5+QPTr7U//hf7SrvCX0XdTe367rUf/tU7txM2Ja2F39s4lFT+G8fimbDrw2/bPbEo8pRf/EPIE1PhFKj//PtdX2n73Ve8v3n8l8u/nTyz'
        b'vSNXHzXd9XX7pH8s6/7Xr/N++t43i8/cChcvbAr+mnn5DO9i6ftrgt+lRA7tL2cd+gdOenP4g4PbZ79jKVAtv/Z3sbUexgPK70fpmHtXbv+yWK7XPVnygEf7Kk9NwTjB'
        b'd1P9otqK9Dffs3x4Id0nZsP8ff6NBD2v5H884Z7245/I9/7dxjsdF5L++tlCut6Pzjbk6vQom1yv+PmZbytnv2fQf2/oHtfgxpjhhYKxyn96ciKvcT7JefG6669+cuFX'
        b'eR3Gfd6xqnu2s89cq3x+qlFQ0nHZO+Pdf/2+jN0vfrY/kK5XeV3+337mYe5cuvOPNlHTkza9QV+6duyXVj/5yS9+oj948u8tM36jhkFhP7sPX5qM3Qv5sdg3PdvWPX49'
        b'Mdbtcek93RvnYx86LXbljB3Lbl3J/Gaao4fXmaL6+H+Ttw+dOH4muuvs1678I2/xD0oXa294F//C59c3s36d5Bz59jO1X3/374wEJU67+X23fjUfNKqyFf3+txW/mdHQ'
        b'sCb1rzaN+2K/sJhT+PFdn/1jglz+D74jFfrl63pep/qCBr58nbfhULG85MTNDvx1a49Hn+By+FcNtHwKVAKnZFfvZe1E5m81fDVozGPqV/+y/o1vXOlTcP/WGennf3Px'
        b'uYVHyNFAu6P+eUeDZR+5Rg0bR42qRo1cWrmwEfat/KjvqWXfijNbarj0zM+lcU3qysTO792yQ3+g995aaHjO1j+MfMMnIjo4PtMN9q6LXf6N0ne+/4fFrH9vKjR+fu02'
        b'92vvZZ0c+5GZDBsU4QhZvc1FjCcZIAKmBlIWE+wOd/Jy7qRnYZfsRx93J5VWywb+PIlPoFbWPJgshjfCFbyIVTB5S5SvvMoYKmVzBdICshlqFXIL5EjNP+JxdKwvFPGl'
        b'oCSd3ZJkkXpFNjfd6kWta7hy7YpAgqPhzoOZTNh8zgQdM4S2sLyrclcK8JEC1ECdgpRABucUrkJPgjjHTJ6PD89C03MbBlhKyfy4/3F1Fclwqn/ZeiBfAtZI262KIhob'
        b'XJBlaxUaKFxl0ryNiR0+G822hxM+0JsH9VJXqHd5pDarX7Zn5vSB5nBZgry6Aax5zmT/hv4LZD4vFpgzzsUnBIpNJtVy7s3nt6X+goo/e6SBP+9T9Oc4bJgD90/5+8SH'
        b'7D/5T7TFQyouLiM7ITkurujVEbuHo1/2dQS6j/0r4eyf53IEqvt8SWn1XQXlqrwm2+prddc6DGqKq4o78jryBmwHEoaPdRb1FI2f7brdcXvOiF65qwZLBatnlwrnrZes'
        b'v3DqC6e+ovzF0186/ZZtwLZtwDsaWh22HQk9xzqle6QH/J5qWM+pP9Vw2HYOeqoetH0udDvs/M658LfUw7fVw99R0x9QZuJ9bisaMfEZI7j7MhxlYZPHPdWqk1Unf7sv'
        b'yZX25e4q6zVZjchtW3k/1ffZ0fd5qnx6R/n0ttxpJpyBDEfdpUp2V1V/+6DfU1W/Kpl9knXzHfXjVXLvMjvlT21L6bIHTnSwL8GTdtrnfFIhoyh9YJ/z2YWRpLTNPuez'
        b'C2UdaY19zqcWzuJM5U8t5PnSR/c5n1rISTHtfXYhVJTWYYbwRxWHOJraVYJ9vjeX+eY/WJ4T05M23ef8cUVTyjPm3/PX357icmQU98WyxaQd9zl//vIZWz4XHfOoa3Vq'
        b'LzqXLE6fdqXV98Vu8ZjZ+Espn7Hlc9Ex9VijTvdlx/lsrZNSHB3dbSmNd6UV2O5fEpPW3Of86eUztnwuOn7jgmytUKKUxr6YISNsf1zxjCmes0eiBkVn+3GjxKWZgJb/'
        b'n/57Jvr3/MO/FcmwEhErKW20z/lLLAd0nrH/n7PlKylhK7grsJ0/J85U/ssqOzKesf+fs+WrbrMV0kU0d5dgKv/lls/Y8rno+OUA2J+95cK50vr7nP9EmSvmxmiPP604'
        b'KcZlIPRTCwmu9EHm6OMLCQHT1mcX+uxMxYkxCui/r3zGls9Fxy8pz/58SpztUJiEtOU+5/+98hlbPhcdvxwY+7O7wESSvx/KPUTlOa7o2JTK8y++YY7TJEjFiLGKSGz/'
        b'tJQZfRXxoapvlgUSp/hSdAJb+kv5Sx2gD0y5LaW5H6HIUTZg7Bcvrqis8thlMxELmC+Yson7jrnTqseOuetq/o75qb9VNBgw2FE0Gjj7VLQZVNXgv7C2zn+g9j6Prarw'
        b'eix5TOibAQ+3k2YcMNPy5L0IdX0sd4v78Xul/6cVeUzGx/iPDQv3x/hGuT9ltia/cossmBbjmQTijO8TwuVyFZmN4f9bvCw+twDhDF9/UVzaQ5vzRW15DzNemrAygZt3'
        b'lkj//jf/NrPheDDPQ7H82mGTSqd+nv1Zib/hcxekDH8va/4btaOPrJuMQ9wrj37r2wejwo/+3rftr+IjC8d++/3UH3R3PtL1XfjKocqY974yVnKyxnT0rl/oqEyY2Uhd'
        b'+r2QXq1fJ5pWDioe/lHk14cjnn35mydvp/71z/trW9NsF8NTKr5z7qtvmf3To1Y37QPW2us9mkUx316Sjfs/OuMlN1Vzsx5/3ShIaaLD5f6c07faHOwt8/5mDgRo/vax'
        b'dwzDNP3Dkr73203D8IKGuveXs3JMvcb9f+PxNNRqZVjjp7FHfnU46/uqjf9e3P3velXNdkrB77sH/MT0X3/++yf+lhv5tpZ7kzjRqaz6T+llFv9c3R1TfkrFKiKirN5e'
        b'J39OXl13Za7+wG+ltr2qXE79fYKeZNWVqoNGpj/UMHHw0kvpeXAnL+Zd5bDhr+SUa+XG/Fji0fjQlR/ofXmW6xTy86C7CnH70RmSPTFmemywHj9VGGaW+YODmRCRh6DV'
        b'X5IjCwtiOK6BvaKIlS2FOOsfbIXzTC1mg68SPlaEeR48iC1g187ycfoA1EKjKOMRrOFj5u64JEdemaerG8PGEpJXwUf+voHmgcm4JsmR4ItJXYB+NtAPNDE7R2oPS3CO'
        b'yXBDODiUD4ts4p8guAtDFthgaqWB9cz6HpcjbS0GXbikxgYhCqbvhkQLf+IcfhB03+TCHA2mlw2moWiRw+xMtmI2WeFdto481vCCvJ1FcTieQAk+YBNbcfh85sFZLvRn'
        b'e4rCa9bgbJGo4UBfrDfz5XOUsRXvneDBOkyZsReHaUuc9/ezDMIu6Dtmx+VIYouYBJQWs113gJ4gf1s7OtlfFNtZwSBVyHOCLbwjImkjrsEQU8M3UFRBHmdgg8M7chTW'
        b'2aicN4KwAmvNmTiqPA7/LKyKcWHjHNazK4UwrSlkYkwHWnI4/COwnsmFh04J7E8x+FDLwgrrmbCumRk3uETaGphjh6XoiCUWTNawAOaSgTR0Pkf7ZpISE6q0B/vZGCOG'
        b'WAK9/kynaPDR1F8iuqyZGDYdwg1R1rR+HPfKe1EBe6OYCjK+YjB38RC7RgqLulAmiwsKuJwH1fgoB5euQK2CgMPROQid0nxJGngd21Kx5jE2EIuFb+AN6lUDh9iuS4x5'
        b'rM5ZdKV5WIbSF2nAmBxg0KrOZbZS4Si7vFl0GZ/4w7SprykOWrH5nNhcd8G+UH84yMpMguPjJVns7M9S5RoMpcniHC5xOVxsDvXg4Cgs+4lSMo3QkGeYTaeBAcFRsEbg'
        b'VMzF4cNYwy4eF+MdYo5FNp7KYfOXUVS0CkKwgQ8VOObzMtHdcjCRvQarkw5jdYAYR/qQGNQGnmfnshgeQ6mFn5VloBWsXbHmcuRUeTKxuM7KjhGuuPrTtPhbE8ORBFHH'
        b'Vexw6TIP+6CEI6LEgKSpxWlLcya42OANdkqwSQxnsMJUFOR3Nt/Mwk+cmlrk+nOwAzah3sztz7GW+2fX+5+T9eBGxScsuv7H7AgmgAtjR6RlpeW/WF7V4X3i8ioZFzoc'
        b'cZWSIOa1KxC+LdB9S6DbW/hUYLojMC3x3uXLVAbcCdhWMhhxeMq33OFbbvMtd/mCEl/mtctXKglkXruM0mVeu3zb7U9+7/Ittj/u/YHTP3qgtv3yvcu33v649y7fePvD'
        b'712++faH3/tiEuKq+2I8ac1dOYPtj7x/+46CFuPIab4uduU0qgJevsggltZkKfZTWTX6mdp6VewqCqvEmRdVElelKu/ydbc//N7lG2x/+P2KhvsSZ0+IM1b2//777/53'
        b'MZ+AUUg2oA2DyqoSJ3U4oM09eYQDOvInrXhgLsYcW3KZYysec3xEzpPDAzculSL/x3yPl5GSlTtAcrYnnl+Qk5Gyx89Iy8vf4yenJVGZnZOStcfLy8/dE0+8np+St8dP'
        b'zM7O2OOlZeXviV8kW5/+5SZkXUrZE0/LyinI3+Mlpebu8bJzk/ckLqZl5KfQh8yEnD1eUVrOnnhCXlJa2h4vNaWQqlDzMml5aVl5+QlZSSl7EjkFiRlpSXtyXqJYZ4EJ'
        b'l+lkuZzclPz8tIvX4wozM/akArKTLnunUSelE+3sU7KYPCZ7grS87Lj8tMwUaigzZ4/vfeaU954gJyE3LyWOfmIibu4pZWYnOx6PS0pNSbocl5x2KS1/TzIhKSklJz9v'
        b'T8AOLC4/m1yXrEt7vIjAgD3ZvNS0i/lxKbm52bl7goKspNSEtKyU5LiUwqQ96bi4vBQiVVzcnnxWdlx24sWCvKQEJironvTLDzScgiwmkclrzzLPnPMq1dFn/unrvwZD'
        b'tpBmWijifsZtpg8DowKXmyHOOBv/s8vP19PSl/aw53zRXv4kn/c7qYskBilJqdZ7inFxL45f+L+/03rxWT8nIekyk6KHCeTH/JaSHGQmxcYq25OMi0vIyIiLE00zG83s'
        b'+zTFexIZ2UkJGXm5X2SWJqxITkUR0Ngwbwxb/E7Kmfi5ICPFNfeIJBOFkHjjFhWE31zuvhify9/nMIUcR1ZQIrnPLzjBFe5zPlDmFJBjoPS2lPZbUtodfk+lTHakTPY5'
        b'Ytxj25auXzj0hUNfNP2S6balH713pRR3ZdSqLLfV7Z7KHN2RObrNP7rLUdzmKDZpPOVo7XC0tl++2f79X+lC3SE='
    ))))
