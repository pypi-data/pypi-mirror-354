
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
        b'eJy8fQlclMf5/7x7cZ+73NdyCcuxnIriiYByo4AXHrCwCywi4C6rgnhGZRHFRWIAiXHxBE+8jSaazCRpmqQtiKlIbX8mTY+kbarRHLVt8p+ZdxcXQaNp++ej7877vPPO'
        b'+cwz3+eZZ+b9PTD54xp+H5TjSxuQg3xQCvIZObMF5HMU3HILMOpPzjnOsCGVhZzLAQr+ccOTVUBtsZiDKQI5zxhnM4PvzRTD7zCglm9RKhE8KrfMTZ6TIF5RJddUKMRV'
        b'JeKaMoV4Tm1NWVWleJayskZRXCaulhUvl5UqpJaWeWVKtTGuXFGirFSoxSWayuIaZVWlWiyrlIuLK2RqNabWVIlXV6mWi1cra8rEJAupZXGQSfGD8X8rUuPv8KUBNDAN'
        b'nAZuA6+B3yBoMGswb7BosGywarBusGmwbbBrsG9waHBsEDaIGpwanBtcGlwb3BrcGzwaPBu8GrwbfBrEDb4Nfg3+DQENgQ3jGoLagNZF66l10/pqA7Q+Wketu9Zca6YV'
        b'a220PK2d1lIr1FprLbROWg8t0HK19lpvbaB2nFak5WtttV5aV62z1krrpxVoOVpG668N0jqUBOO+MF8XzAGNAcZ2XiexABxQH2y8x2GJMcyA9cHrJbnAfwzqarCGuwis'
        b'Ziy2SDhZxaZ9Go3/C0mj8Cgb1AKJbVaFOQ4Xr+UCTCs7b12Y8Ts7W6Dxx0S4FR0zR02oMTtjLtL6rkM7syVoZ+q8OeECEJTMQ9fD1kq4Gm8SsxmehtvTU9FF9GpYajhq'
        b'RDsy+cAWbedmoe41GpKlk2BKempYKh/ELufxGLhfibQaH0yvgI2uofSFzFS0Ewd2SlJ5wBG1cuEVdC5SwtF4kgy60fGI9OgYHCW9pBY1Z+OE7Hy5k1E7ukIjoO3SMvI8'
        b'NRMeyGGf26JT3Ci0FR4ypIG2+8FjsDNPnZqJmnF+aAcDLFM5sNcfHdOMwxHq0Cl4xQo2wTPorB26oIaN6FI1Or8SNtnZAODpzzNDu+HrEkbjiiO7w2MK1JSRhnZwQRE6'
        b'zUXXGNhphkvPaEJIZr1CuDUdngzGrbEdboFH0tEO2JhNSgZ3RmSFSwRgdrJZfTU6hl9wwS8UQW0mOoeLlZHNB/z6NGcGHULnFIbcNqA9BXAnfDM0LTwsM1zKAGsnruV4'
        b'eBE/JlXLxgU7BvfbhKaEhaDGDFIzK6Tj4PrsrChmTBggxsgAEF/2RDdgJsD8ycN8KcD8a455FmDutcLca4M51Q5zrgPmbiHmXCfMsy6Yc90wr3tg3vfCPO2DOd4X87E/'
        b'HgWEv4O0wVqJNkQbqg3Thmul2ghtpDZKG62N0caWxFD+xlKi0WqYvzmUvxkT/uaYcDKznmPg7yeow/xd9iR/e47i72yWvz90NgPWANiLJ6y1Dt8QCSjxiD9levBW+Kqw'
        b'JEEdSyyzMQf2AET2xlZWXMyPYYl2Sj7Av+LewrKKW3NTQA+osMTkszlu1jYWfw4E4JOgrzgXo+4mTWAqiCidM7Wd6TUDwTC9MPqO6q5XL6DkVWu/snvZjpnBzLnLfL/w'
        b'2PQMMAQ0oeTB8jV4nDVFzA0ORtsjUgjL9OQFp2WiXUmlYdLU8LRMBlTaWUyNg22aGTi+T8gCdY1q1UqNGl1Cveg8OotH3hl0AZ2zM7e2tLWwqQBWcBfUwh3RkbHRE6LG'
        b'x8BLsJcH4LXFFuhklq8mjbDotXB4ID0jLSs1Mx3tQlq0A23HAwOPQFyS4LAQuA+1SCXhoXhod8MTOTiFs6gNtaA9SIdeQa3o5QUAuETaOAauH8FipEUJQz+QExbjENGL'
        b'mYzBjMUv4VImwFNHI2+YCbgWI7oYh7km3c1ZzzUwwRPUpzMBbxQT8LJUpBeVzVPVfHUKDt2Y8F3nB1P2+W6NamphuDXRp7Zt//Wnc+Yi3bs7JFfcZyVq5Gc+nZ/7Yd/P'
        b'X323+d3KI+7bPs6Y82/P9q/Woe8+si65m8EF0jdtFi3skPAfuuPknOGFatx/23ErYmnAm5SPzjBYiJxBjQ/J4MUSpQNdD5XiJm4MY4AANnNsEsL9lA9JM6XB/fBcaHhw'
        b'SjgHP9nLgRc14avRpofO+FkKb1FoONqZEcUHgnwGNcGN6GRG+EMnNs3jsBk1pcCTuM3WMXnZs5askfCGOMESFWZf8PiiJs0g3rhx4yOnKSWqqjpFpbiEnXelakW1bNoQ'
        b'V6OU15ELh8Segy/fbQT3ZnGAyLktriWuPbZ1qjZpUOjE3uyP74jvnDIgDL4llPYLpQPCSPLQpS2+Jb5d2S0aEEpvCaP7hdG3hBP7hRMHhPF91vEPSLeozPBFIhiyqJSt'
        b'UKjxlK8Y4slUpeohs4IClaayoGDIqqCguEIhq9RUY8rj8gvwpbBQjKugciBERyKqSXmTyNNYfHm0EXyTzGEYr09sXZqWb7S6x+EzottWjk2TPuHZbckcNLe7bS787j6W'
        b'q/bGu0cPCEe0CvzBQSspt5gzFv+UEAbmGhiYR1lYUMIbZmH+/46FLUexsEOWhtTbRSpRZ/D5U/Ho7QHwKNo6mU6u8CDsiUnP4GeoACMBqAHudNCIMH0q3LoEncvm45n8'
        b'KmD4AF6w89QQ9mFQNx7qTdn8SngeMMkA7YEnEmlSxZivzltl8mtyAeMA4FXUUKQhvAh3BqELoZl8pINbATMXoE6IJQbNBfWg6+hgqFQQYweYxQAdnQm7aWlRoxc8jlrn'
        b'Ak8MPOpAJreQxoct8Bq8jFpxx4ahqzi5sKA8iQXNHe3gSyfjzkBbk8vwBYuizRrS6XniRWsJ+XA8OoyvoRY0fbhx2gp4FSeD2vLX4gs3k22Nw1MmI0q+5DkZXySom61C'
        b'lxd6A17FWBjt06AufEUn4Gs0pUkaeBHRJ2/mReCL0o02k/9sdBBetcNkPXotHF/hRriXFmhDBXoTHcRFslqNTgGrGY6Uig7BNpdcnEwQMxsEVcJmmng23LcctWL2j4Sb'
        b'4SEQGcWjMz66BC9gGdGK2szQiRxcvF2gAJ0epyESBTbAbfAYOqdG5xxg8yoGcFA3E4BeQ5tZSab+xJOvfhOH/vWWep0uyhZGWid7BWV65C8M/fKtqLrfn3npVM2xwDk/'
        b'm785cNLGuQHvbFx4OSEidcuM5Ni776IN33//zbzfbvx644nl4oSU3aLAQ5LDO6zDv3yP/6Yw8vj9j7P3tq4Xlgb7vNt5YPPXzKNoXfRM503vRsz/7sbMtn/9bmlCLqcC'
        b'vSq0/f0v5y989dV/5zNHl7qn9sr/3VL4ccckdGXzuYqVZuETElbfSJtv5rrlVyfe0P9q3pxXXz31/Q9X4/s+nbSSd24D2Lkp4ujm+1h8Uvm4eRx8I7s6VCpB28MAloIn'
        b'ODHwCNQ+dCMjvwaex6gHaVMzVLApi48ntjMctG9WEH1ahA56YAH6BmoKw9AQ41LBMo4/mQkf+uGnszCzttKJFW3HcA81whNpfCCMha9N56LdaD88RRPxXgF7WPENd2OZ'
        b'SkU4lt+B3hLzJ2TpUy9q0itiMRFSBjE1ZKWoLK6SKwqIkK0zvaFidoAVs/fnYDHrNOjiqjMf9PLtFvXmvSV6HPD0uc/nuPhqZ98TAAfHNrMWs1YLbcJtO7dBkVPb7JbZ'
        b'7YmtGTpm0Nm9XdaiHHR122/RYaEP6OYOuIbpEu5xgYtHu2y3Er/sHbh/acfS1wpaLHQ8XTF5O7UltV2uTxwQBbcwOKZ3+F17j1v2gf32gfqSbtmAfaQ2YdCeZtmVMOA6'
        b'qSuhfWW3Q3f5MZ+9DvqEftdJA/bxOIZQRCaF1kl91p7/+IoL3OLV1qQ/PSwSgTkM5OErK/XNhhj1kGVlVYEaa29lCrWKDEeVyxjtaDYs7A3SXkykvWnzpZpI/W+zsdT3'
        b'eFGp/7IgAByyingeqU+AC3+E1P/vAZdR2tlo4GLBotevix1BAP6NrLwfX6ocz2LSPrMUoMO0yMBrNeLC9WAWpf5jkj3ATTYxcsKtjFBuPRv17zOtABa85pHO/DUrC4WA'
        b'lcL70ZXKmEjeJHQR37SCogK4SfmXBbWMmtgImn67tvOD6H2bGrtaX29dOd6f63oosiQmKlKkPtgYrbgaGSmKms9596y+6P3C8S9/WfRXeYgj55jsvbyBn/NiTrpWZFmm'
        b'W74k4upKUmR73nQq6uZsv7X5DsxB4NKe8MUvbfJt3xTDBbN7nC6UIQmHAppKeEXJwiDRCgqEwn3hpYek99Eb6AjcGypNDQuRSNGuMNQI4D5cYFcxbxl8FYt3/tOHJR+w'
        b'2McwJh2KyxTFywuKVQq5sqZKVYCBz2gSHZ+FhvFZwwH2Ql1M05p23+31HWp9TOeabr+96wZdPAcdndokLZLWUG3ibTvndvX+9R3ru0tv+kwgz/A7CbqZOrN2//ai9pXt'
        b'Qf32vnjgCgP0cweEQd2x/cKIPusIFels4wDhFivlQ2bFVZrKGlXtC4wPYucYoxKLTUeJGo8S9xcYJSqi/Y8C9ZQ1iwyjg+qNjyE9M2Jk/Kd6XemTI4M/amQksSNj3TSh'
        b'oIlLIH2hJ1ydZxgEtePsZ6ZwZwBQXRj27+A4kMeikWPFTkT/jQIYjm+PgscCaeS/lPD9NjG4cWcUWu90iwcshGhXopMxPGIxwVrP0WhPuJVGXhXFsS0kqiAorPhLmQbQ'
        b'WX8cnjgux3CIdl3gHiODJ2nU3861qZnNjcTKYGHGjmo1GxW18apjMDKJBfDl0lj0ii1LbSezfQxu8PEgLnC8bD1NwGeqk+AdzhxSMM95eQyglViPTqNdMbg9JgAbeGIC'
        b'uhxB415Te+Z/yVSTzJZM2hDMxoXtcHcdHmcgDriI49BmuI3GbbISr/8L2Ehap/5v9fVswTZEwPYYzFwTATwln4hOxdGok9YFlhzg6kgRZq7JLWKjZs6Ax+A58hQjLYdJ'
        b'c/k0qrIuuFIN9IQ7/R66G0qbn8OH53ArxhMsp40PR7tpXOvV4euXcHtJaf3aeS5AQ1gbHpyYQ3SVmWB8zkwv2ESJsSv91bhhEwHaCV9LXLSErVcXbLAmakESCClOQlvh'
        b'K3W2i4WJatx+yWBKeTK/nO3vVoxqO4kImIUh5/JZTgpa/IlQb6bGjTIbqOGm2ai5gu2CTeoKMrhSMPRan7IC7qTUVegVZ0SqmgrGoxOppRvYhA+IrRGpVhpAp2akwYNc'
        b'lg0wEDmLzuHipgOvdekW+TSyA9bUMJDDpc0AdmhfxuI02gRpUYJlai5GP+LCCquZKSzXTTYjNh9cjUwAz8A9mVPgcbYb3CyLHjB4pNsXVtgpKg0s2obB+VF0DtcvC0Qu'
        b'yIJvymhklwnj6iWcdpKyn415MaBAFjagRjN0Dlc7G3cwej0bXYYHaPTGhFDQzXSTtDl/D4lj+y0VHvRA53BzzME1tJgDX7alcU8Eu4FAbiHp4yWfCsax7DC9EOqJoXUu'
        b'yIP758LD9TTqDH+L8iaumETN6J1caihyAxdut8INlwPQS6g9B8BrNPIPpbbzfZmJeDIrDBtKX2Hg3uPwSqYVbs1cAE+jM7m5SkpeAvXwshVuzjwQsi4PHoX7aRJxle41'
        b'bzFlpBpLMnhrWJaqFcEuK9yc80Bt/jzYMZnGrK/wrinkriGZ1XOW2LOVEKPL6IwVbsr5YM76+VXwII06PtHfO4mjJaOdY89JYstlhnWBE1a4JRfgaShxQTnaQuNGiZ0F'
        b'C8FC0uye5jYGMRKHXkWHrHA7LgTwtaULsQbPdugdB6lfNPcyKcPMnRP82AkZ7YOHFLAJhxaBCHhkEVaS9tLYVvzxSzxBHxmFOXXxjuycPn9WTEkq531SNsf7U51Y4nsh'
        b'keLx4C0ytGdeTsZikkPbYfWs8bAJN3s+cEev5UfmslzcgnriYBNu4MUgDx1e7Kus+O6HH35IDeF5WgMqDitibCaw6V4FE6wDwCCpnOOhCfFAGfmKgKeegZt294cfafp/'
        b'nsVJsBfcPfZ5x6a5KwvAarO4d9a97ZVRb+H45r8bHapSNifWeRfuiCt6Y80f3knPj7WOivrmk78cuvr9lzVfH33k13Qg6bNV7R+B66LGcs+FLVabP8i5cP3B2ppHD0LN'
        b'Vn02/+MfnP7+Zczbm35TFKATTbVuRHM+Nc/5NPi9d1ZmaFvbHY9G+f+yKCujs+K9KaXyc+MmV521Gne17Gz6b0/cOVdxI3Tcm+U3lt971/PX79pUbF886Pxg0MFq0Onb'
        b'3gjvje8mejb+bKJD9spxziuly+7mvAE1Tb/Z4XHnwMMVFyYFBCR+0/3lO3+fsDS0VPLln6ZO/WOjd9iBPss9F+/GLf28Kl/9WZ5wwz+PfHw36Msre37xcsA/0K0TiojE'
        b'l/Zszty7dnyX16ShXz6sjFj9p+/splpW7P/i59899PxYlLuVczyh6thMm29eWw/mrZMVbhrAKpAHbuAVHLgL6zBZq8uJ+XZXGIPVnOMcdMoanqaWIA90PRtusTWxE4VH'
        b'o8MPvfCjIPQKbE5HO0PRzszwNGJhd0SXJxZzUUM1PEr1q3XoFTcfeB6rODvSU4m9SDCR4wZPTXroix/GwG5LNTyZkhUeTKzwaBcXOGC1qQNe58JeuAdqf4ISNIxOhmwN'
        b'wERTXEAAfN0T9xRqLeCwUCuFa4RaUdsJwLordNap2hldXNv0luk3hQGDLh4mmAvjGDdbgrPm3uOSkKtHuyEk9tcbQsGh3YZQZEyvITRx8uUcNpSQ9FYRG0rLfF/FhnLn'
        b'9y3MZ4NLCvpkxTR4l+bCJyGaCw3RXGiI5kJDNBcaornQEMnlPg3RXGiIzYUG2VxIkOh4IpyPGRt282wfDvsG6HOM4ZDw7iJjOGZCr8oYnjL9LcYYTmJmM+8P32Uw2Uzf'
        b'nOHE8pgFDMnecLuUKWRIEeitOSlCzj0LNuzu1V5kDPuP06uM4bCIXs59Qzh+ylt+X5GwNvWeNXBy1ibf41jbeN3xCe4Wdud2F3W7/tonumU2RsM1WMttj9qtuevqpfe4'
        b'5Rvd7xvdGzvgO/EyDk3td53awSe19ta7dcd2+fS7RuJ7GyCOuWcLvPz0MzvSdBaDQu/22n6hpDu317FnwQ1h7KCHGOuuovG4HCLX7x7ygcjrK8DYeN128bzHxb+P1HTW'
        b'CUiwSowGKNoicRoXTWXw1WiL5GJGfDrWpoZHE6hNVs+e5GBi5KY4+x/EBsllGIcX1UZ3C/zAAatw7o/ibbJKA0zwNve/hrefQxM1Y/H2u2HWAIuUYO2CwoqXM30MeLt5'
        b'PNUvq4VOhdarYnINkOOkMzyM9UuiXM6E10ERfA3plOPWljLqXPy4oJ5HTPBdrZOICf7Ethuz45d+lGG9b8e+j453lee4nutwdd3uGtoR35Hbnut6aOOjXNec9sOuxzae'
        b'vWA94+OM8dbVH4fddre2ftv61XDwjt42o91SwlBxNx3joleGJeX+FCIsUTM8IOGNKbSM5nFWYLmz3auuUWmKazRYnypQKUoUKkVlsaLuGc+oIEsGrOl8Jg+zIzGIt07R'
        b'Jt22c9TFNtUaZNqgPR7iuhydeXusnqN3aJ/Yb+//TMVQMMRT41yen0knEiZ9Rkk3mzJsAo9hHF9EMSQvPgejjlQM/4eMyh3FqALWUC6PjIEnp1upiEn3BFb4lBrKqb68'
        b'WFCW9K4AoxvVFqc5YJay+upevjoBP/q9xodlyCgDQy7dMaO2JOMfovc+brg5Z2nyHcycGfuq11vmXrSa8/KZ3W7Bv9xob0cXg1Yutg4pOyzh0KkanpleSbmvGrUZpmp4'
        b'dN5Dskw+yQFugvtQxwhbBmvHuAYvS7hP9i2p3TBnuj6h4z/my6c+oVw53sCVc0y5kqzY4FlVH3tTGNyT2Ms7nnqZcywLM+htYXi3fEAY02cdM5ILi1+IC6cRLnxquRpN'
        b'eTD7J/Hg85ju+Frmf2S6e441RwErMPkZthNXAqraZGz3TmLhdEgCP/ofHNbkkJOazBKXW3MrMznUtGD9s2luQNkN/Bj1Mnzv88iP2uJaiTWuB/MnIzxRsqXvgvW+Q2U7'
        b'xlsrdiRbztB8tPBmwuei9yrGCbb5/S7rj6IjIVLBNmmJuMkt7L2PLGL9XbWbLp45FPl2xinOp9L3vIN+WQM0NxwdL/3KwLboPNqMFdjjGZlhHMBLd57GwLPOyyjChEeE'
        b'szE4Rc0R2ZloZ5a5RSo8wQMuObwJaN/KF7C+2VQq1tQUyDWKArmsRlE38pbyar6BV5fwgNDltkdYd97pRT2LBjzidOaYY9vX9GMZmXQ6uyd7IGzqW8yNsIRBsaQ7octG'
        b'lzroItZH7V436Op1V+iiTcewwNWzQ9nNdFb0u4ToeBhKCF1G2Nt4JNMhiwqFTI7zr30RkzRZd3yi9LuAibltMe/FliJZc5vRRYv8CYzsVEE4mse6L2Ge5mgF1CRtpjUv'
        b'EVC+5o5YiORZjOBaHOaZcDB3Pc/A109Qn87XFqP4ms/ydUBYNMDYp/rvgsLonztPYln4j5U8YhsrnJdeWOEVwANKnZ8fT01mnGU5Vzo/mICFazgVrk5Xt924YD3eetFH'
        b'az5zm7yo6WHaQtmn+05IdhzvEP/VVbz0w7wP7/x8Lsrjf7Z6JfhFEYo9vm3S5G2burRXt7XgMRC6VTn+5tR5hQ/SJ8q+2Hj21fE79nlGPni7/o1T3I5bP2+u8N5hE3Pw'
        b'lcPbAqmZ+SUXz6zdiVjRIqgE7U6wLIQ76aKQGeDAA8y8uEj2Sc8auIV1UUIX0qiPkk3YQx/6DtwFd+KXtqejxjD86s5sBpijHRy4Bev3V+gyvjkW8viJNgKDDrgzg5fJ'
        b'wOsh6FX6LBBtQ1fgS/AV1JQJT+BugVuY2evzJFbPq1g9yZHE3GLUs4ZHl3WpwmRwjbijY+slw9iqxmPLoy2sJaxVqk0cFDq3TWyZ2BqvTfrEzumOi1d7ib5owEXSwtMx'
        b'uqhBz8BupiOTIG8arX3l7qmDHj5deMwdDOv3kOqSPnNx/8Teq12uTx2wl5JQ8f6yjrLO8p5JvXnHp/d7xw/YT35gwXe11aZg9UDkqc02GYQWZBDikTeLFF9QrKmpKnn6'
        b'FMPW3IKOxUKTdTZVFhmNI6rbQWJOwpd/4sFYhQdj4H2ALy8KzNsEQeCoVfRIYD5siaZzDX8YmBP3KVDC/x9gnlFj0nnUmPRhx+TJNR+ClzFnzskvtbgxbxU7JhNnisEM'
        b'siCkUC35Fd9gPGowY52c7gaWhpktMYzemwy7SqSvqK8wq1rNEo+uMyw9rVMtWSNJYIlqdy8ypQWDJRVLvOMXs8SZieNBGebLOStKVAUiJUvcvEhA/a50a5QZ3A3LWOKh'
        b'6RIwByd5z660iFm8hiXuL5gG6jEYisyrypkSOI4l/hA7BazBGfX51+W0pzuzxE71ZFCDy9nLUznGTjC4bWVUuIFInKY4t8LTTzCfJX4jDScWuWDA1PjtrM1jiVEKB7pC'
        b'NkNTnzErJpUldq2aQSziE++m1uX8n9lklngnn/X6qnatyIgM1bDEDUWsBjTHe3lYOW8dS2ys8gBY+puDRaopn7hJDQ0yNw5g+W0PqldGuwb7ssSUlDnESD4xckaZ5ZH8'
        b'eQY8sE4O3scZ3ctTlaSnGdJUFJSAj/DrkWmKcS5e1oZy+jiDMEzsXVlXv9u2hCX6edgSzzfXahtZRdkENUt00NSBh7hIhcr180U+7izxcz8qtUFfWI3qzEJbljid5wfI'
        b'lKaLXTkzJSAFKC98q+eq52Cuny28v7N1ciWKtN6m/PCrf3Zc231xRnP/4eIqXah9sA54fXk5uibyzyebtp9Ktvsk/ZU8eVDvUv034i/8f9jvaLPhLz733s478vnU3l+V'
        b'FrvnXkNzO2/EeoybHGlTd9Kuj3nUbZ5vs/HYHzwFcMUhL7u/Sc9OUexsuH9glmra5KAV77fALS/f1JUuz0nnWka2li9TXyp5aa/IecKvjwpr3NMtA/xWfOv71ZuX0ZpZ'
        b'X51cHfi7ixu2OG0VpdYnFJec0aQEv/3oHqc6rDZt6xqLlmPL9v3x48NVPR9K0n55M2q92SxYvqMh9TeTDzU3P2i7lnU1frnX67Bs1qmg7+Paspp/K+29urV5eZ7wB0Gc'
        b'8Id/8vfN2nBgcfFU33fhCu8Sed6bp65U5E1rVv9C8n9Xv2/L/vv8vIag7/MXf/Cn3H8f/fU/h3IuLngQ/4FZnN3lmT/8LaD2H2tfS97zN/E/vuO3fLB5+vwQCZfiqay8'
        b'WgOcEqAOgqiG8RRsXU89EuLy4fn0sOAUtDOdzDS70GF4nFMrR68/JIZidTm8FsqU4wRCGMDTMKgxWiFx/ImTyfPMN47G+cb4ZzLtOBDJWySrXF5QVlWhJPK8bjSJTkAL'
        b'DXa+aj4QuehqWidpk+4JAFaI1/XbBQy6BOjzMFTrsw8hhjCndm6LFXVB0MnafVsUxMFBn9DvRBwUuh265/Y49Tr2uF/m9AfH91NPBHsH3dx2h5Z57XNbFumj+kUB/fYB'
        b'hCzSqVoscMBBqJO1OOOk3NtVdDGWvJHTYtYeped0xOnndvt1Lej3COt16C0649LvPqnfftKIt7QzBx0cdfL2PP3cjkX9zuO6HfqdQ7pl/U4R/Q4R7MOi9uiWUr1Dy9J+'
        b'Bz9McSRZB+GAnYNu5vbVt93INJmgV3XP7Fo94BbRIvjESBlwC9EJ7pvjWuvy2qPaZQP24kF75w43fVSnJ64vDpve3sZ1MkZjw9HtqgF7P9MwaUIX/EZ0p1e//Tj27dFh'
        b'4xsrB+x97wtGZ28aK6q9CMcaKz/Tt8coSYw7mfzvTzSNgFvWUchCEH3CDcfAQZFTh4Xet9Ma95uOuKMIRcanA46Bd61Fu7Ibs9sTblp7k3BmY+aO7Lt+IdrM9oB+a59B'
        b'occIVGE+xKtVyFTPBhKP7dWFptysWkDAxGj+PWVEFFhh/XYRHyus98ALaq0U45tO4zzD74PtwGg5UZAtGSAfIwYLIDejDoccakexyCcbMHhyzhZg3GCRz6cUrglFQCk8'
        b'E4oZpfBNKOYKHtYiuCUcuWCLuRFx5FtowRom3zIXWJTi9jNLkMtVCrW6WGBSXHMj6lgFjEq2cUcFhkDEc5xDVRPqTV5iToEQLlCj5TAQMqNASGAChMxMII9gvZkBCD1B'
        b'HQZCJT/uFcBnjT8RaNfiXIDOoQsA+AJf+JKc9Zoz53AZdTMOSU+LOz+I2ue7r+uVrtZzKb3bfKkfsOrUtu3R0TUqUYzmrPOiw5ElUcVzfz737YUfvfO+jpPHLT4c9XbN'
        b'reiiuOvbopqccmvG75g1+Av+Kt/Jzmtftz+WNvHugY/2Vbz56Yy9J7fJxgtv2mTs++v4jPsV1eNPzPC+806Wrdiua/9JifD932+5uluCVRMvMH+pz4WjdhJLqibEwYOO'
        b'w0I/0MqciHx0XEOfwe6M1UYPY7MUg4Na0kw6WcBj3uhcqHQpPGXqP/cyOkh9k+GhKniSbkSg6aJj/uboKgc2+qhY37tmtAVtDpWug1vDWYPpIU4kA7sfElf6Qo0KNsFd'
        b'aFd6ONaAdpkBq3x4ypmDGmDbBJp1eWUIbMr2I1MR2hkqgcd4wM6CWzOlnKbti/bH4cdVsBE1h8EeHhCYc9xy0VVWqdqDjqJjsCkC60zSVHbHhiM6zF3rhDbBK3U0f3Qe'
        b'HYDdOI5UkpYZTvY0dMF9qImDLhUG/8fa08aNptqTWUFBpWJ1QUGdnYH5pQYCnbqIek90pzVmwMNLZ3Zb6DYo8mjLasnST7gpCrkt9OioGfTw3j+xY6J+4YFlvY69eWfz'
        b'L+f0BcwY8EjQJRnjxh6N74o/OOWmKPK20MdIJLd3XDzbF+iL+12ie2Mumw24zNDxBsVBOt7LNoNevvjHctBXgn9sB30C8Y/1oIuHzspE4lkNcYsr1Cqy7WSIV6ysqR0y'
        b'r65S15DliSGBukalUNQMWWsqH1uDn27rIG1TSP9M7B2lRCg+2S7/ItEn48v3WCRqzBhmBvMAkOsLCEUqgF8VhIETVnEj1SzGOLQ96dCuB+Vg9B8VV0xWDzNkXmBwnJIw'
        b'Qzy1oqKE+IIAMdu15lMqZCuK5LJpdfbGOhgpNoxhFtgIupNOZx7LpK36k0pSgkuCc+cXkA6QMKpq0j6PS6FaSRpxVAFscYwHhgKITrsfc//pBdjCFsCiwNj3z10IO5NC'
        b'5J1edmzZf9wKZgUs2z13EexNOiL29JRjU0YXYdjEWgjYfSXsSgOeyf77OveoqWb0OgM3Sznw+z8ANfEz9kv+sPODWOosSZYPmI/7qYH2betX3cCK9Tzv8jMShgrj8Fh4'
        b'FktEKg7RdXSRFYmwB56RcExGIZE5w0ZTpdpkHafOydhyI8hUSBEjFsHXZebA1bM9aX9aR9qAS1CffZCJqODT/hhr/FNjrckui3Wkn8bOzZF5bL7/Wmb+YkCIMlqLwBd0'
        b'WYVx8YRN/rAEM8diRbZCUVAwZFlQwG4AxWHrgoKVGlkF+4TKISzaVFXVClVNLZV3KiW5EGZULTeWesiG7CORYfyiqKgoKJDw8JhgCabbSh4v/s0YFnTE/FxnRD/fkuc5'
        b'pJZbwD1LMINJYgajJ3zLtbPxvO8HXHz6fSYNOMdrZ2Pp3+8ZMyCM1SbdxlTx5AGXKdqU205e/d5xA04TtbPu2jg95HBtgh9wga0zDdEOoVsSFDiPjFRJGrw2P1wqAJbl'
        b'eHLd4DeC9awMvw9icS/vcXiMEuUMQYULQC8X/7fD/+0NvzbkV8kp4RjuR/w/wTlugHUUZQYSjInBm3HTnz2GbrwtFsPIkEc2/hIEKRecMDtuWHWhSJMvN8dUCxOqGaVa'
        b'YqqVCdWcUq0x1caEakGptphqZ0K1pFR7THUwoVpRqiOmCk2o1pQqwlQnE6oNro0llgnOW8zzbR+3jhwj3hMuRhRMa2yNkbWrCQa2o+m5bQEKO7k7TtFgj8+3H9HGdic8'
        b'jHnJx+F0iHM4V+5p0mIONB0vXC5vk3I5UqoPpopNqMKRaeP/Zvi/eQmh8E74GssgD8LAmmPYoEn6yVZrV2Ih9zPJVUTT98fpB5ik71TLxVNkMEb0xXSCfBRkaarGG6js'
        b'nuoRT8iKnxKrQEM8MvbGGmpZxWYmTGoLDPJxC77sMR+53xoLagssqrm46MzwzlLSdEArwAxnSwW42QhdwdxihCaAw+YmotpsvblBgD9BNRXgn/wDt8KISpG/1EpljVJW'
        b'oawjW8jLFGKZoQmUGB7JKovJHvQnX4mvlqlkK8SkOeLFyUr8loq+mjozIUtcpRLLxNHhNZrqCgVOhD4oqVKtEFeVjEqI/CnY94PJy2HimamJEpJEcEJiYva8rLyCrHmZ'
        b'M5Nz8IOErPSCxOykZIl0zGTycDYVspoanNRqZUWFuEghLq6qXIXlokJOtsaTYhRXqbAcq66qlCsrS8dMhdZApqmpWiGrURbLKipqpeKESpasVIvp8i1OD9dHvAq3mRwj'
        b'm9HFMTQP4ZN4Wi4SMm70NzYvVqTlCtVTXzagN/Z9ww1uo9zs8JioCRPECRlzUhLE0ZInUh2zTmxO4uCqanJmgKxijAY0ZoqrY8gRh8Yu8fOkY8RbbFrGu5+eHgud2NTY'
        b'8E9Ia8QUMqy7D6MX6ywNserD42hTIVnQCpOi5lR/tCN9AdKm0837PvAAD76BWudRG/EvgpuBJwNc7ZfWVv4wzhpoiJuJlw3S0SWtOUhLtMsI1IhD2blsEvNS0GbUSTwL'
        b'MzNTMxkAt6MDFugi1E6gKR4Qszuy7ReXVlycOwFoJESy5AmJl2JoOtmslTE3BeuV09cYNEu0WwJ7QG6CGWqTuNAketZyKCrszVlVETajgrVmr7Kja5DiyA21YTIzJ6AJ'
        b'x0SknYgukZRnwovGxJGWbN7HhY3ISUHbMwRgNjosQGcWS6j3EmpA56eoV/LRGaysol249BHohHKtWSdHbYFnkV/lXFy3e2rllkj7rWYv/SNq+qK9e4K/sWy5OGT1mWtL'
        b'2YmkokDL0s49+tS4h/3em9NLIgff2fTOzn/Xvrb//wqvbTeLfAu8++dN3i/NuN/yO2eO7rWe+rpDOxYclt9yAV/n/uV0/sOP5/7lb69Zn2orqLv2ReDD3N3mk5zb3zjT'
        b'8gsnzSwp2j5/p11nlPTcsciK7y5mlR4sf+1Cw0qvNR+2XD+r/Dj3QuP333hPrA1a+7t9X6uvLXxj1cebQiZ/96s3G77p+DL7kmWHq4/mAO/2/K60oQ1D6SXNAVlZb8rm'
        b'/+zIDablb3x+S+9nwtueqpwS2z/YOtneFj3c9vCbR/uLxm09crPrTp9r2KXSr99eGWbzW9/aHwRnV6bO/UOfxJFq6pPhBZ4VblhJpiY8BG2P4KxaBJxgA898KWpjVfnD'
        b'WJWnLq7KqpEursmB1CjuxZuSLk3LDEuFO9Eu9lgFd3g+PohXic7MYO0cDVALNz52gUWt8BAnPAodpruEhKXJ6ag5JRM1w2ZDAmJ0GTihLVx02Q6eoG626MC4cSM3Eu11'
        b'pv43TiEPw/DzSnSgBLMJTiAUkcMa2OSmhUak41o1s96xs+EZM7irKp4Cem90cG56dvh01E0OdyBcZDWXg5onGnxz4+AOpIVNxgrx0V7YgK4z6ArqRftY80wnyY3oBORl'
        b'rj/ahToZ2DwZHqeP0TnUUkQSYAclH7/ZPJ/DmKMG1jNjE9o7Fz/egw5mP2GDSeI/JLM2bJ8NW4iVZaeEHrKBXoaX2TZmUwyF5/hoK1nhZvO7DnfAQ1RFyWAAFx6Rof0M'
        b'1KEDa6iTCM8hCj+TZuKSLsZVuMjATrg5jRYlX4HO4JIchCfQrkziaEwW0m1LufHwdaSj/VeH9pGiME7ZBPESuGubyJ0Fr6to11iHwjbYJEBv4o6BzRFZ4Sk8YAu7uUnj'
        b'5BK7/+Zihh0wOKU8/jPYCQoKlBgdFBRg9ZQVtFIjhepXuQyrXy2zAK7++tgBl2Ad77aLxx33AP2yAffYPlHsbaEzWddoV+2e9pl7QF/gzAH3xD5R4m2he4daH9dZ373y'
        b'hk/kHfJk8oD7lD7RlEFndx33tpCsA8zrjtVn3BRG3XXxaE9oWd22oWXDTZfgQZ+AWz6R/T6RvaJe2RmXywGXV74eNOAzs4N3NyC4w6Kd11486OLRVtdS11qv4w26eN5y'
        b'Cep3CermdRffdImmWcUPuE/uE03GZRt099ov6ZB0hrYkDjq5tRW0FOjzbjqFdGtuRcy+ETF70N1nf3hHeDdvwD1cl2i0PHn64B8L453BKjUuRMe7ae8/6CmmDw0/4gDy'
        b'8LY4aFDkcVvko+cNiALJr/mASEJ+BQOioAcWfF9HEu2eNfAN1PH22Jhopw6sdko2XKiIj9iYKt6P2/Wf7HHSu4UmVi0Te/9+QK0RT3S3D1FwiQvbDxvBt2uxgjv9W4Av'
        b'xItg+ouatw4KYsA5q2k/zbxVxpq3+AUEfD7dmGIovtGYsvCxPac9b3/+3nzaxI8C84ZBK4ETGOAZ8USwSiGTh1dVVtRKpDg7rryq+CeboPD7vIIiZfFzl3bxiNIu2ruI'
        b'LW0AKS3Gx88s7E+2UdFGJUD1uYu5DMdQHSTPafFCn410/zulVFXi8HOXUDaiIZfuXcqWVGqKqX9qYSOfUdhyzmiawTQr4WCpKmPtKXQcP3dl5GQI2g5XpmPpLa+IG14R'
        b'Jo3/LND+v6uP6jwwSKPnrkrp6KrE3PBi3WsfRTyPzvC/qM4Wk+osf5HqlI+uTtQNryi2OuE/rrT8pwODFTK04M9d5hVk8J4BxsEbmUfVdVxA01URsYFRxRX02LmnFvT/'
        b'pyF6i4Tz6MAo5S6RKOZqsfIJyahWKFbQg/GKFKy+PupFcliewUiRq6wsxW2QrFFViefIalcoKmvU4gRc59G6ZDBuGNw8+MVVE6TR0kjJs7XNsZZl8yQMuynkldqFoRTb'
        b'8WbALegUA49lOSp7eXO4aqJR/l30OjGkUyO6MPbPq6LlUcXbufPOFTopkChnWaZsCTq/1+2In/ei8c4eL7lNXAw87C0nLHOV8Kh/PdyIsWsbgcumEHItus5N8saInGx3'
        b'y0SvxZGj5J5QFQx6ArzELqmiNhVqMZ7uxkXXJs0mSPcQ0rOu0nq4BXamU8TOWcag8+hixDLVUy34ZsR4Tg4BsTOypYFAUSVZQiNLi2VWxD1/asvUPmHwYIDkVkBsf0Bs'
        b'b96lRWcWvcX7mfnb5u/X9AXEDgTk6ZJeziSYb13Luj77gJ9k238H0AW9kaWpNrXqL7V6QfeG9exwJKjtOXzzib8kg4fM/8g3/1HDKA7NVdSwBj9NRY1yhazGMHlr1Ab7'
        b'Fj2kskYlq1TLTA6bLKodlRBJI54aTOMLM3EcnBT+kZUqVIU/YoUZvYZk8KVOWcIaVwonKqTWKUlAQzxNsLZ7Fh1jzSvwSObYFpZR1hUv2KD8TeJqnno6TqLz1wlk30BX'
        b'a8/c5sYuYcrpEjl4STpOvN/h7WzZR6tkhcGfSjd9tcmv+vVx+itZU+r/uOZyRiC31AqUp1hvqf5CwqGDijcFbR2h2tfDY6xuD69jNZScuYn2ZsJWEyXzSQWzzAOrmCes'
        b'nrEBy8SfTK2oKTB2EoVodW5GTh31aMQGl3oygvqE/rc9xulrBjzCdEm3XdzbY1tr9dG719/xDu6TzBrwnt3nOpuqLx/b+5vuB2DHTuNTBtBTNgJ8QMbR00tXZxxRZFPA'
        b'SjyiXP+jMzheEIXbjizMc8+V2wiMJAeQkfn9llfkDa9Ik7n9eYePFItDatEjJ26M2NswPD2Ug8eORG2AelCTVQ6jF/V/d2cDnkg/yWDGWBAYFgxVKmWpslJWg2ujlD8N'
        b'vFQqVhvmwShp1Bhm16fbmuWsQZc2lHFHFM5IKs5RrNQoVYZ2lONQcY1YrihS1qjHtG8TsYRLoK5aYUT1SgxWZBXqKpoAmzTbFSUKlfrp1m9NMVuixJmpGAYpV2pIehiD'
        b'BhPII1YZS4XzSq2RERD0bOk2egeUeZZmKhEO3Wg7vJaehXYYjrjMCp+bIk3LJFspGiNykDYDts2Zm8LNkcCeVPGyIpVqvXKZBZhZarciq1xD9tzCfZXoKmqym2piGX6c'
        b'ADmgZc88YgRjVqIL5gugFnVSrJELdy1C54JQuzVDSgHgaxPRm5pEkuArUnhQbauZn0L8jubBwzykDZuPtGgXaoI9eSlhJJcdqRloO4Pl6iHJGvhKADqSxyHH5F2ynoMO'
        b'oWZqVoYXcNW0wxbrgxgJ4LJVDyc8Z0H4fDMwZ4MAHqq2VDrIGvhqYtvY97ay84N4Ipf7D7YGYqQjWtkWiQYlO467+Z4Y917WkbD5GR8f76pxEQoTg/ry9B0VC/OiEv5c'
        b'dM0x6/LtjH0Z82ZcSLm7ekJk3CPwtVr2xa8+fVeULtv2edgfZ0Xv4d+e8oa0RHDFtVtQaXn2Nwsnd/TfETxcNGVyxrVWt/d/v/F+CEFNlQHio17XJBaszU+bPR22k84Z'
        b'tttZVXJQpyyDHqIGX8+EXVYh5ICBRmd0BQt1wzwAfOA5HjqdXEW3z2QmCI2m2bwyuuX2AtpNTb/w2gJ0HW5GV9NNTJTW9lynGthJTYcr0GZghVo2mE4y7AyDWtypJxk6'
        b'yvcwgWNMGTwOO5EW0NfRfrgPvh6qQJtGbasMXUFfd4MbiXHSYNRE+xn0ugXUrUqlrnWoF+60NFo10UXGcSbstIR7f2xf28YnpqzH4oOcKjViUhjxiE5Z+wxTVqE1cYWe'
        b'TuBc/e76O94hfaHzB7wX9LkuGLbV6RLJPrjc3oBLYWfCbnpMpxNZ4lvF/ZLUAe+0Pte0QaEzTsHDZ/+kjkm3PCL6PSJ6eTc9xtN4WQPe2X2u2SMSk3T73/SQ0scz3orp'
        b'H54UDYY+8rPHwtSflp0ah4X50+dH6k47YoK8M2qCHNEWjYzJRp1sa4bxJG61ni/qTfKKYBw4YhX1H5nYeAVYRD/3HNlF9MljwKhPRlF7xGOh/izV9z/QfMtY5yoeOXzg'
        b'uYt6aGRRJ48p8hPnJT65uDpGoSXcId4KlaJkSKBWllYq5EMWeLLSqFRYdSzmmRTV2lifOnzZY2F0BqBzvPmwrwmjtaFHiHG0tiXWdMbn4Rl/eMl/Hd9ixHyOw3yTuZ23'
        b'nm+Y8Z+gmh4i9knHM2d89mB6FsPTydNUm366IwBpAnbqNL47vLH56Wu6tMHYt+gruLEJTUYsD1JxoqySKO0yw7OicgwCxpz9ibsBnpBzsydOiIyijgbECUBOTC5Yn39q'
        b'9sP9FC+eVSErFa8uUxjcGHCFSZ0fxzBW6mnZV1bVjJGNSoErUqmOFyc8qRwVGqrzI/BheMfrMHywzNLMJMwU4jMSOyCtYZqal4JJOQQJwPNoDzlaOdoRqyGt6Fw6OpcG'
        b'AtEhW7R3FjysicfJBNdinUkaHpKGJyDTJIaTTkmbF8weM5qF1Sl0eB3q8LJG3enVVEWTupHDFu8mmxUWlrvNmgs0EwA5Capt0djr3+FpmbnDyhnGBZgPYVOuBbruiU5o'
        b'puBXoXYRHzXRaHS1MRXt8CW+3aEEhZiuf6eEpWVIU8NDBAA1SaxXol1wk4ZIYTyfHdKMWCuH24SkRqQAwXiiw/pXmCQ8jQ/q0FELuHMu3C3hUpezVRPQSzRrLuDhCkxj'
        b'4PEcuJWeMu9RvCiUfRU3gTkP63cdnLXr4XV6xnwt2oxn2bRMQyMyQDg3JIiLOmEXvKCcVxrOUxPr+OrO850fxGBsE/MkrpmlL3cOO+Z0pqk0AJxxiOywkEVjeLM8yGPH'
        b'fvjq3zjzP7RY8OHmzywn6MtLtnxRoY69cCL4j2drVBrV6ZLNQ79iRLK/f7a558+fbj5WuPm4/Z8/++DT92r+US5ot9WXvxe27E5I5J1fbvvUe1vWBL3Nvy5/vVp1qPdX'
        b'GBN9/tmOP23secv7l/SYkIj14d5uxzHsoedfnl7DSaeIgJNpW8REofPwyEOidEXB09MMeGcE2OmpongHHoIv0RXLjFKM/4yYKRRdNsAmTHyVGpEK0Ik16amZIRikcoA5'
        b'6naATRy4CW6Ts7aq1knwGKtXp8JdI1BPAtpFIdWEOtjM4jGeTyjZjwz3oR2sBUqnVpMV6lR4QgqJF2kFxy84lKaLdjtNprvLstljb8NwR62FuyO4aE82PEsLvgF1xhEj'
        b'WSbaCF83XaqND5dY/0drq0Tyj15YtSITv0Gs1AlN0YCBSDHREGAxUZENMYRN3D3xjvu4vqA5A+5z+0RzyXkVU3ZP0ScdzejKuBUQdyMgjj5OH3DP6BNlmCy83jFZeMVv'
        b'dUymtoAbwjD6YPaAe0qfKIUsuZboi28KQ257hXRPGPCK1s1iaWU3hRGDXv77F3cs7lyqmzUodGM9aTszbgiDaRIzBtwT+kQJZJnTUzzoHXDLW9rvLR3wjhz0DblvxpM4'
        b'PgA8XyFd4rQErp5t9S31fSNsDXYsoPoDufyRXP4Efsqy5uPV7JELmwbo9ZCggbEa+6gRdP0Lg650G4YJJYuboS8Kul4TSMEpq0k/DXQZ3MTNjWV6bjTz/khDvi+ZT/Fs'
        b'Q2fX4enY1HIv4REH4x5OFs5vlsRZtYG8u5FcNgF224e8qriggC4Eq8hJBXT1eYhbpCx+6hL0kJlxSYsYUqkVaMhmhLGFAl8TyPyQvmWsrMP/ZpemwxODz4QZtgHq2Mw2'
        b'phthgFbizLAF3OdxbOy/Mge2Th0xXfyu4p6AHnWfT0yfe+zrMT/n3nb36uGeSXzIZWwn3Y2JG4yf9i031ibwASAXPibe4+HQ/QoGiDxv2wcNiiY/5HNEU7VJ9wVA6HHb'
        b'ftygKB5ThFO0iZhiiJNA4iQyNJKLz237kEFREia5zGK0sw2xIkbGchXfto8ZFCVjkutsRpuCSc7et+2jBkWJmOSczGhnPU5rFkkrBaf1tbm5TeBXIlo1Pa899KbNuK85'
        b'FjahxA076B4J3RcBr8Db9pF90YlsUl44qUy2NYRd/viFbzhONmLDCzh0P8xYrdmkWqkMrZeBNJeQcjGJTcC/S90Te8a8b9ykt/Nu2qR9y/G2CXgI8IUkl87cI/f3pxlL'
        b'HUdKPalxNusZTuZil4QEdUYW1pgFcCedbi3rOKjZLWbUdwIAHW/EN9xxpG+4nJPPk3Pz+UqQL5Dz8s3wf3M5P99CLsi3lJsRr+oFoJdP/I0NvuMM9Tu2P2E+7OEcgVG6'
        b'lda+hCu3MPE1Jp7XNgY/b+thX2NbSrXBVFsTqh2l2mGqvQmV5GarcDBsFzSjTsF2WocSc7nDY4/s4fwcSezh0tqfcBz24ybaA3nfoYQvF47xphDnLdry+F5EPm9TwpE7'
        b'bTHPd8L1YqifuLPcZQvId5G74qsr8QDPdzPEc8dP3eUemOIh98RXT+LXne+lFeA3vfEzby3AIR8c8pGL8RMxvffF975yP3zvZ0jHH1P85QGYEmCgBGJKoCE8DofHGcJB'
        b'OBxkCAfjcDBNUYJDEhoKwaEQGgrFoVCtBQ6F4VCY1hyHwnEoXB5JN2KSnaPSLRb50loe1oWihgQJK6gL+LERQJwIUPYB6wXOfk8L6xjkEyGlKhlRLljNoLh22MX4CUfe'
        b'kT7lKpzACkWNslhM9mnI2MWUYlbBwQSis+A0WUNnRa24qpLVQsbSEiScIUHBKlmFRjFkUWAsxRA3eV5O1qMpZTU11fEREatXr5YqioukCo2qqlqGfyLUNbIadQS5L1mD'
        b'NbPHoXC5TFlRK12zooIc/ZeYMWeImzJv1hA3NSlniJs2Z9EQNz1nwRB33uyFs3o4Q3w2Y3NjviOM2MMetQEMMWLjqY6jth57umOXt+qHv4wmZ5bHYQFsX88p546ObWRV'
        b'tW0N30iTc+o5dVhBMv3WWiO/njHer2Pk3HpmFVAF1DNynpxP82PKzcCoPzl3uBQCAlGNd3VYkNTxyalGJLVKnLbcjA2T1ezHOdWDgmFFH5ffCoz6M5YfxxzePVxrblEm'
        b'sfikYCxl/El/fAMvPnbHf/KFp6m4tLdYBVvGpkEpz7B/s90aTz3ec7PDY6Oj4kxZXY718tQSou+K1dWKYmWJUiEPG1MrVtYQHRpDLKPnPc3ZaE9hhxVW01XKIs1T9Op4'
        b'8ji+UK4okWEcMczqhVhRVxaXkdSVbDvhAWPIBw+C0XX7nHDUIydlJV3+f1yboEB10BAjHWIiPyci+PMf8N8jrjQyMktiNmT/ZLZkxVpWUV0mG7KcT2qSrFJVqYb46uoK'
        b'ZY2Kg3txiK+pxkNZxWXI2XAsnCVbKVVkO+OTsISwgdjEJkhd7uzYfh72uPsdwSQvA9bBUoRn/EEf/1s+sf0+sboUAu7XtE7VJ9wQBnYvvBU+tT986s3w6RSMT7m8pn8Y'
        b'1Lt6tCd3Wur4g0Ln9sCWKYMit/ZcfUIPtzv5dHpP+mXuQNiUyzn9YTMGghP6AxL6vWb2i2a2JN/F0ea1ZOmSb3sH6hWdlRi5Ww36So56d3kP+EbpeHts/9M9mbTNngZx'
        b'jS1hRLhfj/DiWrx3scnimyljU/aqrVaICzHbFGPoWSFNYn8LC6Wqwz+1xOyGWrZnn7PE340o8bK97PbRRx7U3XDsgTWiaBxj0bKeUbRnycpy3uhnVsNqBpey5pC5TF1A'
        b'd+kMmSvWVFdVKiqfujv1yQr+kzCnO1tB+f7yjvJb3lH93lED3jG3vKf0439e7HbVR8XUKVCzokihIt1j6BdxdYWsmDgUyWrEFQqZukYcLZGK56kVVDwUaZQVNeHKStyP'
        b'KpyrHKtyeHTL5OUaHJFEGJnKyKYbnoboOXHmw5/zA8Of87M0HMXAjFhN/S+4JX3y5VjifF410XBYUa5YU1wmqyxViFWUVCQji8VVrPcRjiUTV6uqVimJZ1FRLSGOSoz4'
        b'JlUrMHJIxJ2lwk0wU1a5nC6AqmuqsP5FBW/lcwlZg4A1FqmAFqmQ9IKGClVWhBNZP7zwiXuBbIkawwGEfKJUUVNW9RjFhInVSjxbGZIhrxF3MtONVU+royGhePKR0/hC'
        b'A8Aaw5PkmSbXoqoq8t00cYmpbVdDu0L+RDeMOf2sVqiwcFmF0ZGsiPjFPcXK+yNeXrZZmggcdqxGr4aGp6SGEfNZ+gJiBkXNKTiYPS84LSw1HDajwwKwwtEcXYf7ULeG'
        b'OJDErs+ETagXXZgbnBZOvpO3y8knNAteQAdywtERDoidzS9FDe4a6puly9iglmbCCxlpaM9qgSOwg21cKdRFsUuyZ+BVtMXUMBqcFR6SHp5jTDidD2ot5Pbm8KrNcvZT'
        b'W1csYLc62PDNUr47Ogl3Mbgsh63o90nRQUf4Zi7WwV6eh3aiPfOIr82r6A3zbAadn4LOzKKf8oIHcGWu4lKlBSzkAy5sZ+DG8bCBfhsVbYXbs9UprNk0HZ7iAQdc4MXw'
        b'MjyBNk+jK9WT4pBOHUzPbueno4Z1DDqZvDRPefPDXwO1GR5mg/qL6+Z8mMaLsv/rL+XRrR3rxFbQz3L9Vhcnu+83ld5On/PnN1//tEd937n9+HcO/2w9civT3jGuLWDp'
        b'vKVL//3xhsR24cyVnl/umrelV39EvmVTzaLMkC9CBu9/86ky9LXtstO7j28unPTtg7dmFCcPyAXRX773be2smpnTonacD7uw49RSq4GABfGToy5Ypuf/e1eDLGbG+oHa'
        b'nz/c+Zc31vP/L/rGld2Hs4XT4YN/V/mVbv1z5p1ZPhte+pfq02aPK92fRTe+/dtvBHczX+9f3lwx4VLOis+/etlSVtf3VsiRyyG1Dc030+b3Zf6u5+Eu4S8/nXLrsN+K'
        b'P2df6ZAXob+ZfVn9heLs1cQ2pcO+r4WDbT7xl6YJ/pQjcWCPWoQvLaRn2aMmuMvJDPDCGXjSooCaNuFpeBldCw1H2+ehN1BjRArayQXWs7iC+nnUcLq8NhE2RZDvazYj'
        b'HQN4EQw8x/emjxLgSXgyNC0zIw/q8RNfBu6rQRfYI32baxyIJTfTDAjgUXiSxzGHu0tZT0Hy0czGdEN50Cb8pgsDDyyYTE3JcnS00CoEHXQdbU2mpuRt6Awtdg7aDw+G'
        b'SiUhRjasRi/ZobPcWkEUa6veoxESM+1cNz6gJ1OizewRK5iLDhrTLgrDD7MY2FsBe+iWKNgQvpDYeZfB5tQwKWyMIKMS85hYzEMXYUsIXd6P5irT6RCFV+zpKIU7I8gw'
        b'FYAQ9AYfbV40h91p9FLiSlpL2IoupqeSocUAKzkHdWZD9lQy9GrxpPTsiVAXzgDOKiYB7oSbaBONQ13w1eGDbdCVafRkG3jajzpkioXwUHpmerp7faYUNYalw53ZtJAh'
        b'sJkPT4fC3bSeCXDLeNSUBU+GwY2oQwB4SQx8Uw5bJfb/dTMauRgl3kg7thMrUgtGziJ1nga4MOZTatpOYXcO3cuzBw4ubVYtVn2e42/aTxh09mqraqnSFx8t6yobcI64'
        b'5Rzb7xw74DxBxx20d26zbrHu84ruTbxpP/G2s1u7f2sZpru4t61pWaO3GnAJM+w+GtcXNH3AfUafaMagZ8Atz/B+z/BueW9cz4rL+QOeKbc8M/s9Mwc8s3UWg/5BRyd1'
        b'TTo4Wce9aS8edPW45RrS7xqC8bKbt04w6O6pMxv0FO/P6Mjodv61Z6QuCWNwfXq/TySG4B5++thus66pAx5RmO7i2VbbUqt3HXAJ6ZbfcIke9A1sFxCvuuT24JZs48k2'
        b'Ez8Whd2zAV5R92yByEvPvSWO7hdH3xBGD0qidYk3RePIpqJZt8UB+nlH87vyDy75tThalzLo4qNffcNFOujpqw9uz8ZJdwjumQHfmHvmwNVbZ7pdyEpVBn6K5Zw95ebJ'
        b'rUBTcCc9uy9/MFrOySlga+0YxoGcePMiB/6r5gKKq4meNMJNdnj5kzrF8Ye/Ocqnh/2C4eN+iS1B8F9zlSW75H89FoxLZHGIYYs8q3UQVIphAYEWw2DegOYItFMb9N3R'
        b'qMGwrvwEHHwC/I0N9kZjkLzRwFJGwMsIrGWEPlUEk5FF9VqCGkeXTFZcxnq4rVCsqFLVUh+AEo2KhU9q+kX6H8dhT5oTRqo9Jrs6amSqUqy7G2M+cxW9cngZnWVI4yq6'
        b'Ee8SlKpQmxrnfoJ7Hl3Z5lba0PNMI9cVWktXGg6NPaD0pAe8VlevmFKZZDj19ZHHJbAGc4t+4l8nTVPssGW/qbobtknVNuUuNhzAoGaATqKrsFdDvsjmJYab059Af8Y1'
        b'eyMYyiMucgswLiMr8I/d7rD8r/O2RwfQofiMLKVrahlH/XucYuCU25qWqeRjp1v3nVdaOTmJN333OvD3qAh7daP3xsO5Z5O1XWku7xStese3LvVOd/LM1LNJH/zzd+eK'
        b'r7fa6XXWrw588226/q08VducyeAXUeGbHg5+7PFW0pFPPtvm1rfgqxJpcftHKCv5t3+2imqNzI1K36cNWXLs0y8yvvCOmWRVOqdKveDkzz7bdWJD2jt+fy1dCm987PHl'
        b'/jKn49zD3v8+tmnywPHfPJpt9k1O0M2E6/1mMXc27v/L5i/urPJ/9IGH6GLa/QXJa0IjHLdqmn654vKdK59/v7/4zlcygWdkdN7aNRLZw39xKszjF3lFSGzZBd4ueGlt'
        b'KNo80+SDPwl5rDtdLzwEj6QPNyHaBvfxgN18bkWC4mEgjjChCp00aXfUAV9/Yk63gtdZ17fdoXAvcX+AlycYT8OGR/MfkqMBimEj8QNIT6fTMkEcT0zN8DC7Jxg1e8JG'
        b'wzI1D7UuJuvULcXspm8dOo/aQ7ONZ5wu5QEreJaDjqMGCxY9bY9E54zHZvMyMerezcDr6LIHLZ5/BdSHGgARLwttm4mxDboQx34U8ugSF4Jt5nHGgDZb0Sm6nRu9LkJH'
        b'qS6SistubJI16GWKcjjoLNzOFESY4/a8yvoZxqG9cFsoegm9Thfm+UBQzvGehdpYOPU6xh76YVf4IHTUxFHxGNzF7jA/n2IWGpaJ1Q/6tVlnGz7WT1q5KrTTR2LxYkDE'
        b'ApicU2fYSmJQEOtsDfOU4Z6ijBADypA7AM+A/dM6pg14hJJz8z3aa/av61h3Qxg26OGjSx909bzlGtrvGoonfmfvtoqWitZKHfe2i+fwg+7i02U9ZcfLb7hOHPT02Z/e'
        b'kd6Z2Z1wwzO81/9S8JngyzlnwwlQSO1I7UzvDrgVMrkf//OcfLn4hmfCoMj1lkjaL5LeFEXiBPdbdlCDnAvZ2aJPviGUGLaudCf3u0RRJ8SFfYsLbi0u68f/JGUD3so+'
        b'VyWZ+5O7A06H94T3B0zs95yoSybV0NwgH4Hy0Wv6XcKMrxb3S4oHvOV9rnL2peCu7H7PGBzf1Wu/bYetvuZoXVdd79QB1wQd/7aLV7tCv3DARdpnLzU9h5y1YFLj5XOc'
        b'GsqeQT7i2NAsgh2e6JNgjgEtEO//TAeG8bz/gs6Nqt+Cp52B9jJ4uqmsfswtf6uAylXOPF5UwLEEo2MNLwgIiDVQznmx+BZlEm7WI06g8hEvUBpdIuHRNh2yLqisKjCY'
        b'sdRDXFmRmprkRpvfhuwLhl3a2HWfOhejofiJB2mkdYlj10Zw18BdSbcCxvfjf8LxmM8P+evlR8u7yg9G9HtE9Ymi7nr4Hkrs5p227LE8mN3vEdMnYjdgjljVGf7agTlZ'
        b'1eG0AXYlpZFrXLhUrapnntLkY1DJOo9q7tjdofLEKfFH08dO6fFKT6WkZnhdR87UczoZOWfsdzrpqtBTnvD2mT1eTcKxzEfHWofp1CDMz6pzHkZ8K5Rq3A3FZRQr1XHj'
        b'xUF1ZkHUJhc0xARJ+GyPC5UrqiuUxcqaAnYwqJVVlXSQDFnk1VazCwosD7Cb1ob4FFgOmbNLhvjhSGdr8fDetSHbgmqVAmMuRQF9pc7JyCAjyHMJe5C6Y4FIHHsU+vk3'
        b'sfzDisv6lvXdotNePV43XCZgPrnlEXPDI2YwQHI0syuzN+BS+JnwgYAZHcl/8Asdioi7LLruddXrff6vbD+0vcdlwheSMy79FzH3AOO1iLnr6UuEIxY2Lp4669GrBMMm'
        b'sgx82YMBvZxYYZlnd7GhQ8dgGdKh+/h0lPGy6szZegcH1fGCwnAvcIIkKrLRQcJhpdnwNkTx4+MtcAup6BGnxsUXlrCEY7Bvf7cJ3I6I7o29FH8m/uSGt3g/s0E2fS5Z'
        b'ffZZoys3vJuNDEJStRcRRiUcg8AgBy0+MiPCQhyoZss/WiqYFZDDB3HBbYcLTu8LOMN2efL5l6SjaV1pvbxLNmds+vyn9btM67OfxpZ7zA2Js4BBhDKjigfqGTljHPPr'
        b'mLHrUM8s5xiWTDhZQ8yUHo6KHGXAsrWhExYxxk4wVEVQUFBBThixGa4JuS3CUR74sxUZnoSTe2MGXOPw5Mme76HHE6akz17yv62Ru0GM417hTJmqKv6xuihG1gXfloxd'
        b'l9gB14mP6zKPPen9GXV5DQxLYCzFGjnDEjj2KXw2pqRbHgywyqJyY57Ch/itMajkrdynTa4M+5Q647MMy3vcPk/sanwstXBbKVaOaCtySzJXE1VppJTy8t2f35HfPf70'
        b'5J7J/V4TvsLCZiYz6Bt41KvLqzfwkvSMtN93BhZHTonM3R9r0OHFNVIowhxsBayNq5MsAnpGF1eO7GJyW80xOB7iLvbw0Y/vmNrnEtxnH/y/Zc0kw4oqGWzTfpQzS0eO'
        b'MnJLoqgUjMF38H9WziUmQ2jajw+h0pHtS25Xk4Iqhws6ptQlbolkSvnxCeXxkQk2PzI9kGWkEdMDS1jLMXwCgnCpi8eok2XHbslKQwH/k7Yk+0eoyYtbT+bEMZZ5jWkY'
        b'WnyICe3hPhbDFIyMGJ82zMjxaaw9nmJkcvmIKYberyfSLJat+xiimVVw8OgjZlRWvcg7urRr6YBLTJ99zOjWGe6+ceBZfGbSdez2JFXds7iIzOxs6U1mdkp4iRSf+oUC'
        b'usespV6fPPBjove/0nOWL9xz4araF+gttaZoJCAg99vIwFk75ggfbvlgQ8tb/XjbE18I1bofa3m2JCYtTwnku9r067O45d282vnkPC+9ZsAlvM/+/zH3HgBRJNn/ePck'
        b'4gASHDJDEoYwgIAKRpAcBiToGgGZAVEEnABiTqsgBhQDGMEIiooRdU1b9b3b8N27A3FP5PZu9e6+l+936Lq7d176V1X3JBhcxb3v/2vo6a6urn79Kr1X9Xnvhb6G93hB'
        b'26TiIVDrMueOOJlhCNcbc51gU7gDNrJKdSqS1hXYA4hCbtBv+KZqwqRMjupjuabcqD7I9S7MBGzBazS/feEm6XGU/C/1HSRObvuuGmRoN6hBkrAPN6b1r58uDKQU4+ry'
        b'fqfOY/XaSrZ6q0rGXSuM6VpvXqFWBQVqpUYhL6tGjLHXMUaXdhCPK5nUUMHFXfzYPazXPayL36Xqc5+MFCM3r+OxLbHt/F630B7H0KfuYjx3tDv1uksbE5+4ebf6M7pY'
        b'n9vEHseJ//uM5ryW0Zy3HMNeccLemtPWSGIur6xUMqx20LFan3gcd6LX8lrd5z5Fz2unXjdpj6NUy2t/lOf/BK8Fr+W14K0btf/bstqMOJY3HqXw9Vnc0Xea7Og6Df43'
        b'ep7wEU94Op4EvglP1LpFJtPftobWf92b511A2ifxk8EjXDO1PsfmJXm4r89TwmEV8gEBaniINWguJqLUfmN5SqDn+AC/ZklluQIbAi8vKquQKwwXbljgp47/lgUFTLmo'
        b'CsboqkCbdAk3c2xdM2IzX9nnPqMx8QvUkv3OBrUFtSv63LDTzV8HhLbLLy3tWHrTvy9gBo4gldgc88TdpzWaWUHuc5+Er2JQpuUdy1FXQZqT+7RBinaa9pogE9j09PXy'
        b'tdUIjdmgoZbqdMSRpG4SdqbUqE2S65t4gHVluYHmRvXxVS2rmpe1R12a2jG1TxTTYxfzTsRf4H8n8SVvQnxVpcqIeHL9Ae5Qh03qL7oOlWNAolqXYwSidOjzNxJplLnG'
        b'7fU15BctNiafXN/DLdFdx/sjxUx7O1zZrr60tmNtn2hqj93U70s1I1zWfAeZZRVqIzLJ9Ycc1uaLkOnaHIVH/6b1PXbjvk+18fW0WZCJqojxmWswdeGU/zJSG92xJ9KW'
        b'eX0jLBTo2kUrxdpToAEUr68prfStQ87Rr1njgVjOlfMYoXeVAeFrR1g+NbnazqkX6IZp7psMkmSq58t+j89f+RDEbllFqbiqsobB/EaEMxYDmqqqSuyM/xUnXDpAR6Ch'
        b'1FXbKgfMV2iKKtRlqxRM+2R8Tw2YoZJKy9SqAa5iZdWQqUzvf4oZUPXsJxQYsZ9N+QizP5thf7+Da/OsvZMJYj61zzWtxzHtyVjsdLi4Pbltea9nVN/Y6EYuK5GzOu7M'
        b'Lo8+5+kjSeYdRLJ2wuSHDbGpVL5iSVOVV6pxyBVn/M02xlAadF1SoihWl1UzIXuRHFRepFIXMMiNAV6BRlmuzME8mIMPeutMXbceMNftKFkRqASDpCUwHrLVoMzDBzKB'
        b'LcSHQnzAbkWVS/BhGT4Qv5DY8Z0Srzcrq/EBq9rKdfiwCR+24ANWIZTYW4lyBz404gO2oFQ248MhfDhK6MSHNnw4iQ+dmD//6cCcw0w+2T1JDPlfxRp9fYbVnkqaMfkU'
        b'8IR2g5aUS3hd6lMvvx5r934PrzpZv4c3Orh51WX0O8yqS+h3S0RnPgE91l6/FDq2JLb5tpX2uElvOTwSTv2G4yAcj80Ypw3is+dBlJPHE7tAxobSKZGuS2SNNoP7HSOw'
        b'0WYksdnEKVMGOfTYbPoln+ucgy05LSkbUb/Q+VuOv9DzBYUOuFgXfBAN8tDlc1STNqIBREHxI6EPNqIMwzd92RzocnAGyjH2OYcnjCIBdgbx2dfWFkKPl2NpYRb9QkAL'
        b'p78QcIRBL8w5wuCvzXnC4BfWtFCiT3tpTgsDXwq4wqgXljS61J5Jv0asisKZg78WCISTvrbTH8yE017a08LYlwL2MA0fAvBB8q2AL4wapNBBb86Zp5Sq4A64M4zYcpo7'
        b'g3p4mqOxtjEdEhIvou/nG5tzEudo3DpeCQ4Dac4G5uFuoeS8Tv6QwDwClGpmkGpmEK5Hn2puEK5Hn2phEK5Hn2ppEK5Hn2plEK5Hn2ptEK5Hnyo0CNejT7UhqWNRqsgg'
        b'lQnF44xSXQxS7UiqK0p1M0hlwu24o1QPg1Qm3I4nSvUySHUgqWKU6m2QyoTO8UGpvgapTiTVD6X6G6SOJanjUGqAQaqIpAaiVIlBqjNJDUKpwQapLiQ1BKWGGqS6klQp'
        b'Sg0zSHUjqeEoNcIg1Z2kjkepkQapHiQ1CqVGG6QyBqoTiIHqRGygKp+Ejt7yGGycWhuLJNTJA7bYD06e3nffsy56CCRQ67jOIBMbM2hINmz8QCwxiosq8DS4WMFa8qnL'
        b'CCBPay9BwsxobfywyQSDfFMYY/RYZKCxiQRe1zRwNFiIJ90ixpWPvLJYg1exdCUblVap1BZYpmY2mZlHtUC7mXGZeQlsCYUjGCAaXaSWsPYeReLFZEscFcfgIw0dIYYw'
        b'r9R+K2sIq1YqMEOMyitSEbtbTByxwqhGJRWVl4s1WK8qr8VihpGHRaOHjcQ9LL9g24WvZiDBbz8PS1NKMyxRYcxVvbmGHkmqUuvkJtPYBJ2MxZVTa7gFOlWVXPGMrvhG'
        b'VwKjKzOjK3OjKwujK62BO2WIe0XpVka5rI2uhEZXNrorLrqyNbpnZ3Q1xujK3ujKwejK0ejKyehqrNGVyOjK2ejKxejK1ejKzejK3ejKw+jK0+jKS3eFJNkCse6KRlfe'
        b'Rjl9tFdrOEuTqWF/tLxOoBYq2KUG3lr+Gt7S1OF55Xxtu1AJ5CgP2bbhVfiMkFugza0cI8dqaNrwPIfpNbzD9FHuWp46U0cnd41u2UVlo87SlWeG3mhkHa2eZfjMGr42'
        b'jBpN7Sjl4ZZksYa7VMdT/Z96XeA0FScN42K4TEBkmfI0KvtVNDO0DRsIXz/UkQ3WpAG6YIBTUPDKf+jTS4qw2Zneco2Y6kokA9Y5SGwrW87a3goY9C8TAZFbUCYf4Bdo'
        b'FGol9q7POPUYsGUiVutckSlPYA534AOOXq2sxAfi7f1HFIHRGHniQ1omA/NGJVZplEiNV6BXEFncjACu1EUDgoLlqlLy6mXYCRy/QMH8EJdwQu1jBSTsrFlB8RIMUSaR'
        b'QIvUGhVSCJQKjAQqKsfhLCpKKhHFhKFlJWXFxEsA0gGYaUB3u2i5Wv9BA44F5ZXFReXGbm1x6NclGFitQvSRYRgVQ36ZkLAD7gVDWI7UZzTEsnn56Hy5asASEalUq7Dv'
        b'A6LNDJihesF1MmATp60ZpibMVAo1viGxZIwPcOcfECyrQSSoDHwIm1DfGIkdD2jMiK2X1El8XdEQMrVxdr/EetwxWrf7qm6Na6npkU7r9ZpGbD8W9bkW9DgWfCHywNCm'
        b'1uI+UVAjDwM9efvMdVFbSGCW/oBgHLXFTxfZRWwU2UUbvOWkhVGIF+2vly8JPSz2MQxLzCZ6+hCjaTbR+Mdfgp/30WZlf3Dol3022jxawvwC8a+37jokHP9KWNqeevqS'
        b'1/j5M7m0uX0lZ6e0TTkzbU96Y0KzP14Gn94yvT3ykVtYv5dPa17LqhZev4vHca8Wr3bHz12k/UGhl0LOhdzi9XhNbeZ9QSxbHIlHzJCe0LyeOfN7Q+f3eS7ocV7whaNb'
        b'c0KrXzv/c0fpoC3lN/65HeXs0+p3NqQtpEvwSDSxx25ij2iiPhzzO3h1VAJ6ZItr56FtQ2uZbM818tWsj8MwJY+YZVQs0/smDGG8NasrWdeP2OpVjmSdspJaJMEYSBbv'
        b'YD1OQDFt1Ci+xIlLGYZXGWccqwYbPCyvVOudU5L4ie8QQELZPhoinTGRel+axiFqhtOIozuOjkSycHxhNCS6meCjYZiaITSycRlHT+TrItSMSKQnJlLvxUtiIkLN90gn'
        b'WWL9YDR0ehvT+bM4MRPnU6VZzDrLIe45MHGsqRQbQeS1H0HUKaYgAmXG2k8VegxrLiRCgYmYJFJxrj6tpEyBX8iqEqh0lEFvSKUTJVTiIJapQSHotExNfrWxZoIIaDeI'
        b'idUS9A496bPRcDYQc/bHOs5GDXctP0KfioufExeGDonv5ENXCUcz2gYbEz3FyOsvdt6uWGzs/3co8TNzEhPCEhLj895h5EJU/9doiJdyDb10LDi0gPmIHNIYDQRS1tpP'
        b'611kiBmaVJxAXNMzRnflNUW1Kta3rbhCUVqE13Pf6dN+MJpPG2/cTYO03VRrd2fwdayQKg7MnT1n3rvVwg9HQ2q08fAcQKbpysplWLlnfP8inb+qqhJ730I6hIbxFjz6'
        b'8RkR+NFo6JyE6Xyu3cJ7ZZun82o0enpYvn08GnomY3o8aaMZYzka9opKFQb9rWpJrQqbgIqz41JlaJgsfwdKO2jlJ6OhdJqJGtZTWF5ZakygODA9JzHpHWLEIQI/HQ2d'
        b'ccZ0Moa1FfJQdWUo+tGLjeLAxNETyKIX/3s0BCYYE+hh0uG2ODBz9NSxHeSz0VCXbCx562PTeTMWykjFrMBOe9jxhnGznp2fk/1utP5oNLSmGXdmezJvEfWcdVY0epJQ'
        b'5faMhqRM48oNGjoL4RUAbO+FzwPjs7LSU2XJeYnvvePE2TsaUrMxqU913PvLUFKNFzGk4iQ0hCcrEPEVRAFT6RaJTcWIRxPRnNSkPBzpPUScPHtmiDg7JzUzTpaVFxci'
        b'xh+cnjhXEkKMrZJwg1/CljlSaQlZmWhkYYpListMzZjLnOfmxxte5uXEyXLjZualZpG86A1k4bqmTIXt5avKi3CEGcal/Lvw++Fo+D3buGdJH3owtpqvfAzmdWahiOlW'
        b'RWS4KlKhMt6la/14NMTONe5aE4Y2DmbxSyqO0zttS5UlZaFqTpAl48ket+13kmR/MhqyF2CyfXRki/KIsMosz6E2JceNuXKUwwI7ef50NHQVDJnm2WAFxAciQ5VCv91i'
        b'uGTxLhXfNxpKFxuPCh4MB7WzEvaVIcYbSiaEEB3UZQ2tw9mboE910jSMZSWNARUjYANHMLZbSausR3qGeIbjrKFNw15QqgnTUO2C+hqqwDCn5fCcSjfT6aa/uYD/+vtL'
        b'hcPTUE6b4anazQD6tf3n1eQcxuMG3njTaTqMtqbfAjStzUkl5soPcf3/HX/mkJDVZJ0d+wVX/hMdJFyDuNZkFRjzT2fNYFWqUGuX8Ve5DW1wBjcV6DEVXp7+6wYKG36t'
        b'3bsWr3ZOapn00G1qu+Mllw6XroTulMspPYFTH7qlPXD8yOVDl8aEJ37B7Qldft2Sy5KbefcX3FrQ55emCyKJioiI7va47NHMOy5sET5ylvY7Oh/M3JP52DGy1zGyK+Fx'
        b'VFJvVNIjx+QhMSeN2jT+Q9o0bkIHqVoShVGWxxiXDe9aGGczvGtp7Y0q8QRAQixho5XXgNlyqJG7t9LONDBXu69lCLQtHQrIk3CU/ShlgId3CkwYpJqzewgFpj6CuaPE'
        b'dcWaQTqIHjv4Yd8F2Nw4pNctpI8gtL8QuTXHN61stH3N2nHa6z5x7NsE/K0lEXGYrSzt9/FJszJtcVuuqEDfZ2JXgtyowZ8nHuHzHruN73Ub3+M4vl/kTL5NJvE1BRIj'
        b'Gx8E1jVgM2TzinQV0rP0neofFNufBoTGe1cCduvKjJW2lYk4k4DdtuIzu1Y8smnFw3tWJPTCgLXRhpWA3a/ikb0nmyE7U1aGG1MCdkfLXL+hxWwm2RhvWCndOGxbV4rx'
        b'mS+HwNVHBHMZRxVT3sCdZCg2oxfvBmEXsQTIZSG0+3asVOj+XE5TnuOIR/ycl3yOZx5dJ9M73J+CXelPe71TfoM8rEf66dgjfRzjk58kDXJ4TmEv+QJROEqzYTzn9zum'
        b'Ybf5GXRdJsrGJmESPPKYJOynXzLIoZ1iXvK5Y2Prkp6ba18wA78gXu/0H1ExFVMxnVBBHux39McO/gOIf38WY4bpcopjMGbDH2NTJuCUSYYpkTglmqS4+5EIA9jlvntM'
        b'XYb+ZYH4ZUHkZexTmEbHeCYKAWHwIIfrNIt+yed75mAeW1Nuvk/s0JA5CWV0i61L1xeWgQuTMaEJWCxcKMbChREsnImPYSsQE+oZXSd7yYQvoIXuLwRcofgrS67QhYGT'
        b'YR8/8A48ArqtxOBitbDKWpIGdwTLMqTYVw7czaWClvBBl8fEYdFn8Z+vcKRejLDVY8u2UPO4HEqBcWW6kXAen6RwDVIEJIVnkGIm56Nnzes4JbRcsMV8noXcDF1bYvfz'
        b'JRy5OUqxIvcs0Jk1RprNE9ZaoWHIesBhSLvOKFMZxxDjaEfAacwISBvJGhx0pRsvMWS3QDfmlWKpRDe017K6CI8s5gxYFMg1LODUAht/FJWXqWsHfIZuEWNqCgxRRiqt'
        b'WWIQhyBPtYWYa8vQGiiKDXxcu5soVefwegMeQL2YAZTdBfWWkD1R9mdcoD5G7egX5//xGtnWJH26KLBYvsU2h6MngBWvJ3FGScI2TELN90FCzGhJqBuZBJ0UIiUkvKkN'
        b'g17C8MJzQqxpyvB8MWL7IfLFdq7OvhTLEQmMlUyfKLzHLvz7xP8j4giNI1gAkEltmNDKUkokhZ2YUAyY0popPHaT9rpJ+0RhPXZhbyJJlnynJDkCoxhpshFXoQdHW4WG'
        b'7n509jL/okxbvKkMYXK0HmBk2m2E6YonwR4C0ROm9TUTOhd5wpZYdJnQvYhTISu1HgBnAN9DT1gPf2Kp7fA0vZ0sjcfIUuy3KdRw4WI5dj++WO9lPmAIjwOMs8srFYz7'
        b'bMY5EAkionX8SIQjpC29R7MDKJHPlJPx2RR8IJYRuJUhSa6qSlEh13oFsjJ4BZN1ROM+bpFcPkxaJQ0B3WjCbRDHcCJt0Ls1uH39I9H0L1x9e/xy+1zzehzz+h08Hzv4'
        b'9jr4tqrP1rbVPnQI73cb99gtuNctmLH6eeg2pd8N313bhs6jiClFXp9rfo9jfr+d42M7314738d2Qb12Qe2TP7eb+JouiAGC+i441BTI0B3HsM7mgzubi6mPJIL8EfyZ'
        b'Qkrf1Zpqe+zEw0nRORvFCCbjoSuB2k0Xc0qpYs5CZ8YFlElTGhNteQ9nhysPPbfWwAK7mEOTlBp2tYo7wFVplivH4Zo0cEYxQKuNbLL56kp1UbnpDyW3juMPxX7D8eDn'
        b'ejmhzy3mckL7iua44yktKcdlh2VdCb1uMX2i2B672L89dIshs/N2D6m5TGIzVBHRm5aQpqlvlTqZnRHhUzhsBSgzOUSlHyK94/rVye4TcEWZknHWYsoxKBLJ7y8EPKEE'
        b'iZCO7r3ukX0OUXUJT0ReveLJfaIpdSkGpy94tDACGxaEY1sG968FZsJJ2PbA+yt0OZmRCXGosYgpCiutNMgHN/QCIbwK60OkNJUAL5hlgG6+kVyoxat+9Uu8HOVqKBei'
        b'vxzyl3uEP4+LI8vIBXIzubncQm4pt5Jby4XozEZuK7eTjzliM49Xx6njI7nPHkl7fCQD8uvMcVCnOvs6lxIzHJ6JSJBmJCCTVoI0JylOWyj52E6RkQ2CGYv/FxnZIJix'
        b'+H+RkQ2CGYv/FxnZIJix+H+RkQ2CGYv/FxnZIJix+H99qi1DfwlX7ocotyN5pGWo1yrstGsIp+hd9Dw7lM+eDeg0Bn0/TcI52ZMzHMzJwYIJo8Ul3nwFuvC3wjobxB07'
        b'wh+HOsc6p7qxdaI65xIneeAWC2yTMIfqMkP/x3ZKdDF7wvG7EDe58mCDcFxOurzmnSGGeUlAKH2+sbVBaIyJGLDG7VKLdB+gswfoLAl/gJMcP8BJTRzgJOai37wBzsyU'
        b'AW58smyAm5CePsBNjs8e4KbmorOUHHSYmZI0wJVlobPsDJQlJwsdchPxjXnpSuyyHj2Rmi2xGeDEJw9wEtKVOXh456SislNyBjgZqQMcWdYAJztjgJODfnMTlbNJhpnz'
        b'UIZ8REzqMMtWAmhn/GMwEYUPUsQ9MoVUDB5xjsw1co7MszByfWwYS5im1nHX8VjnyENSdc6R8QrWMA2KDJs6F7o8mQb3ZdgNti7CXU8N67OkcGcmjjGrjyxLIrpKU4lL'
        b'UPg+OJgRkpo5KwV1yTTsWhV08KhpcJMtuCZwKDvxu1/zVNGoyNpJKw5/Oh6HiG9q29dW98GWPbRljvOcmU8yd/hnhPdq9oTMFlj3fMLLdfnswRMO1TjNfEp3v4RLvK6u'
        b'BMeSrUBHSIrW2XxO4Bh4mwsuzAIfMD5KN4G6FNiQFQS3we2ICJoyB4c5K+FN2EgKsFwa4Ah3gwawG+5ODwW7wW4zymosB+W+KkWKkKm1C8ySIYBWR8NmpkWz4t6lwoMV'
        b'ifTpQTmKmkN6HcaRqTirzzW7xzHbEMmqdVTDTItmesitEgcMMuWskxhJsvEwv4uYK3gwxs59cPjxIg+a9nrbIJj7Bf7UaatwbrGhoGajbSc46uJ+M2346228bfxtgm1m'
        b'qNlaombLQ2MAv84MjQvMSCAgwezsSmxIU0bjYr2VrilbkKZsbtCULQwarfk6C7YpD0k1DNdi3JR1cWN0TdlLpsGcyIkqTC8rJ3EHmUDJoaFSHBqZRBXGbSo/uwZsSQHt'
        b'XAruqrKCjeCGORPQ+Ao8a5muexA17+XgelbobNa1cxrcCbE/4TmBsH6OOeoqPOxO95KVEB6Dh4h36fgJZjhwuF2jsLp8YH4cRQJjzIVbwTVVGjwu1LmXnmFHsq9fa0Gh'
        b'+g5vjFCUfxNnQWmwv99aHGvZMCayFG4sNHI1bUbNzTWrRQ27mcQ0hvfDQEd6amZ6CKJvJ7gpoSkrGQeegSfgVRL9A9zxmRycgt1Sw6bI8HCwpTCd8gHXuaA5AtxLEWiw'
        b'8jctwilYhj0L78zMN3BnHSgNDYR1YUGpmeD+cpqqlJijefjSCiZeSDc8Ci6kV3JgQ2pGmIASiDg2sHsmaeYaNq7DGbglGIdmRkwPRTnAbc6E1GxyE54DzeODmdowgxtA'
        b'G2W+gmOZlqPB3mbBPrAdHs0FjeD2MEJmBcLdIbA+O1BHrhkFjoAmyznwRq4G9xZfeHB1bhKSEygqkAqMgBcZcjeBHX4qVOSpaniFR9GghYK7Y/JIfG54IBfeR0zfGSKF'
        b'u3DAlyqUJy8Q8bMhJCQzPwXuytJ6/da2DpqCp+AdT641Ek06wX6G0ehz4bV0sMecySOB2zPQZzskc+FR2DGXRGrxgvvztJwGN1blU5RVOgccWAtvktqHV0G9PBfHeIEN'
        b'oCPP4LPx62EHOJRDUVl2ZlVwS6AGt35weg04DJuwtcgqSu2DRuPtGm+cfhxeAJvgVQ64DS/XVMNroL4GXlELKKEbB7SAM+s1k3ALRE33AxVqShfQPdTOQ2YHpoWidoSG'
        b'dfLCHD2X0YeAJnjTkoK3wQ4NdogET8yfHox5hHiGaNudGxiIBuu6MBnLMNyOwPtwM6qfDaDDgoqs1mCDnTJwpsSKBlfhDXhNBbtXgJ01SusV8AZFiSK5YAs8pCYhZ1BN'
        b'XUqCDeWoicEdmaFSxHk+ZQ/2c8HFyXAH6T917/HwKCDeMHVFyL6odEqDVXRbcB40qVYg1QrupgSWYDu4XVJma32dq8K7zOm8BfvzplaCcLvrDpwIL9lfx82Y/6hjYWOs'
        b'pnK9ecPpc0l/aBQ/ml3Ucdt99ef0c6u/Nt3NLt8bewrM3Fv65c9X1/z2C9G/x43dGDspe2Cu/P6JgU17ob265q//an2acth5WfK1gyfvdu4TNVR82KToyx2vso0595uL'
        b'YuBp3+Z00WVpBZUbAlq+PMnxai53DPy15H1F4V/aJaebknc/SChbN/PjYOHUtOzon/TmWKQsHjN3n3mNBvzhiy/Gf7P4hOpXpQm/Tvv39h9GNXlxj/0o7EztmIT8R45f'
        b'fcopmJDpln//uu26jMSpn6xPhbO3X6D/tdXSxv34L36aOif/huq9tYox31wO8ujzUR0+9O+S3oearuLJd4I7r+0cCOj43Z/v/mHX7z6993uHnwW92FqRnuxxQjQ/3d5m'
        b'T1njyWk/r//Xl7INbt88WGi9n/+H1J/ZPvjRQEPhT6LfP3Mn/FZeza9P185+lDlYcm9gdUed9S7Jid+MqS8a/GNvzuqnvg+P8u9cjfz5D9Z2Vgi+vqYoslnSsXrD+g+j'
        b'Ak5+dfXRPz90+e2PODvP1altW3csORW9227n1y0NKed/6JL72VmnaQG/S2s7y8t0BH/L33hoTbjvsz+59Dpc9fm2wPX84RO/+Fh1Qfal+d//Qf85Zse4BRkSXyawS/da'
        b'8L7VOrDNUGJg5IUCDREXVsA98B7qzWBXmCy0YF0KduJ+iQNP54JuEnE8EvXmJp1bdJ1P9Cp4xRzcj2GCnV+qQuJEQ42N0FIJry+yUcEbaqGAclzBzQW7FjIhbo6Crcr0'
        b'YtcsbfiY8+DMS9zr4VlrcB51lDvwSAbSbLgUF96jwWFwy47QvywB3ELEIWlLAuss4A1C3kUOPAlOgY3MF54Dl9D/BlgHrthWwxtV8LoGvdxKxFmSXklc2HPAoZnBoB1e'
        b'NvC2v2Q88/CpRHAUSW8hQRIpGTwpylnMg5tXLAqDh15iI0F4SlGUngKvSzMFFKeWnpIwl5A9fRG8i8ahIwK4HQ1IiGxeDA0ugxPwContHuojSYfNiLPbM9Bji+gweALs'
        b'eInjZ9XAYypVtfUKDey2RT1wh6250BJ22aJiGqpRf4c3alYg6jN5AjSB1sMbxG89vBEEb6DxJCwU7syIoCnBXBp2wu4xL/Ewp5jrCxuc4dUUcAF96lo6ydOFRP6ZDe/7'
        b'goYsRGRnSiaoR9+PdEVpWiaXcgXXeTVgz3TCAbhzCRYGs9BItRtHADoK9mYgeXAGBx6IUzC1exRuhqexN36D4WZsBq9UJPQGFxgC76rAXdBgAzaH4XbGpwSFHJ9CcJWw'
        b'Koi/CDSEMaNlBTicyaessjhwfwxiCKYTnCwMBg0JLoj9YFcWFiPQO9D0LkATwmkevOoURaiIQWLtXoAH1B0kJ2qsqC3YIFElwR5cJC8CB8F1iMhAkm4HYRXiVCpHtBje'
        b'eklCfV2oXYa/AhUvywB19llgJ9yN8rjCI7wV8etJZ7CygMdRU766Lks/m9nkcjOXwm7yivJUeBYxSxqKVAEN3JPORa1xOweezZcTPnii6Xorup8WkoqkGX4ZZT6Js3gZ'
        b'PPoSr2Yg5taDM9q7oC6LvAC0wkvBqahZBgXy4UZ4QUpoTclHE1oD2Lo4SxYC6sPY2YOPWNLN55svJzXnDK6rUZ7bs7MMgo8hXnBhwxyLl0RYOBTqjb54K2y2NVZfUHPY'
        b'HWa8rRSMJrGdvpbgONgMG15iwSdyKqbW1JOgA9ZlLAaHJAIqgzJDsuFh0EQemQgvVZJJbzdShtD3geteKZnoZ1dYOvqCXcz2VTK4bAZ218J9TPVvgGfmMu0D4EdwfgE1'
        b'lsLz3S14XwLP/sddbGjN9Ya62CDbPE5DVAtmf4coOtc4TEDTcg9sNxbQPvGRKJKoOmzE0qciT+wX8pEokKwnJvW5Jvc4Jj8TeZHop2G9XmGPvSJ7vSK7krszLmc8sH/g'
        b'3ROV8EDR55Xx5lFRn4k8+r0C2qN7vcIfesq65N3LLy9/kNo7QfbQs7gnp7gxGbsbXtiy8LGHtNdD2l5zaU3HmpvxN2f1hE1/IOrzSG1MeuricdyjxeOxS1CvS1D7hD6X'
        b'8Y2CJyIP8qYZDyb0al3K9Hv5Yy9V7QFd4/u8JjRas76Jm9Y08vodRM3VraUt63sdpD939XuYO+fh3IIe/8I+16Iex6KnDi6PHfx6Hfxa8x85BKOPTb+STkpP63NN73FM'
        b'f+rug13Zta7uc49stHji4N4qOuve5t6+uH1Fj3fETZde73hU6IB/cHvepbkdc7tqH4XGDXLpcTOxt3a3BOyt3Qkd0Xzj1Yq0TWlXTffqK6vJGxIeVPf6Z/a5ynocZc8c'
        b'PFsnP5qQ0eubwX7b5F5/WZ9rVo9j1lMH79YFvQ4RqJDAEBxS4uSaxwETewMmPg6Y2hswtS9gemPC545+TwOCGxMeoV8vf2Lm6BPY7tbrE43ObXUmk8wdrfEia5rJuHw+'
        b'vIBk8Q04G9sWe3Za27THvhN7fSf2+cbgzOJ+cQDJzBbBmkOOC2AMNP3CmBINQtey24jEfBO/3fqJz7hWzeOA6b0B0x8GFD1I/ijjw4zHCfN7E+b3LCjsSyjq81ncyNtv'
        b'a6Bzj2GdE2nNjHl4N0CJ/QopI/GKjVVxkVpnMSxQFS9RLFe8aSQNg16Gu1Mh+0fX176zk3VjBR4rIf9GvezbZUiDz6K/pfDxOTm+hTqvwkLxKUEUdc1qOnfUYPwOGhs8'
        b'EyaMtN9o/CW6GLpGONLR7/cef81Op+k3vzJGsAZiIKPOkQbzKWI2goM4UKkokodWVpTXSt7RSBQxyqqANeAoKJO/Hcn/NEYIhz70YFzqvgoxZRZSptJ/j+EHvItBw4ev'
        b'2VY3TTNewjSwUfLMI8Yg2BREZx32rrQx27XY9F6jriwpeTv6uDyjZhBGbAQ06lBUkBj7IdAbsGCaiWXx90Kw0umtW6wAk6oHCQcRkHBZCYsKXo4h4ajOFRXYi4r8e2Or'
        b'dYHBSPd2BFtggm20W9CMhQiGMpfimHM6i7Tvo2kqvd+6YVpj4vRQ8ICRo3Ybk2j4dt1GeiHFYItYT1VcspaJdzp1MQrX0mQtkzJYy6QNVi2pdTS7ljkk9W2W5QUy024x'
        b'F2HqaBIkG3tF0obF5n6vYbGxv0STQZaTDIMzG2OJVWLVkkpNuRxvuKOxtqykDFv+lhZhBLLJstSsQybxzHJFETbTECcQdyO4QbHRm4lBF54my1B/ZYwPykxHf1YpSHDH'
        b'wsI8pUaBpt8ypqcHLausUFeiCaB4WZC4vGyxsggVjg1ZtHGiTRaGjTHUw8Y29JgWsskEXGQMZGoN7E5MlsaYzugITCoqVyEKh4c6JB6QDBuFrtPoGgVXVrZB5MpTYSXu'
        b'92kzD3866Whbk3cD7cCLrLqB6jpr8nMu/d4/JTSJSgv3RcEj8BC8YUrxgPezClAns9N2MhaCwCspVahX+Rn1MlVxeQFhIepvmCOqaVKci2gH+Hm8DVIuptzF2GdFj6Ph'
        b'bgeLODMWo8hGS6EWOq7Enlbf7I12PHav428bqJcLxTRt/7Z7HY0CMdVqFcw17TS6hPR8Nm4pn+xm0Oy2HHbrzPveYpYO28swuS03mcKhKVXFel3Tew5Tg3hHoj4jKC0E'
        b'nMtj1sdxQlZGKg7sfR7UW8UUgzNlT9/n8UnwtsDF7cxG3K2UO00RqLk4qg6Gw37JjvMu3p3jksZtlbVKne83SY5ZnDm3d2Mkl1qX2plvsYDaKOEShdcLtmWBS3CbodI7'
        b'ksabsI4ovHbwrKtVEBvVeTa8PjRodNdist4RCHc6xSeYbp9T1r3JPh1qsao3arEqtsUGMi32uVJMOXu05j/2n/rQf+oXnkE9wWl9nuk9zulPxgW1R59c1piwP8to3460'
        b'ZOHrtAJ2307v3FQJ3qxtI9pctW0bR9pbgdq2y9sE2cMgfQmH7HOsSoJX0tPxCiQP3AT1tjQ4C1rALrIVBRqnOaYHy/C9cMtIvAZ/EN4ss11uxyEbtrtevX/40ylHNza1'
        b'bZbsjHi1/f3L758c+/EfCv9fYWqxrIjzwnmZ81Ln3ObfhvPJcPN4msWg01yGPd8BCTf096pjwKqxphlDqsmTqaZ+nvnLeWLzMcHfOHLHjB80p7z92+W9eh+u2rePWCXG'
        b'b1dCXCEjvNdWWwXovd/MR1Vg8TZVgCHJpqfsQorZ7yfBkKkSzn9g0n4DgQLNHRc/d+SqcO/85kjM4U+jjm6sb2uSf9RGhoTOki09H1ofcaGWr+N5bliKphC8PwQvK8AW'
        b'08tjwxfWji9g1tbc4TUJx6AKOKS/GkAth25kE4wlqXUR2zlneFPObiZgltrqNjGr6KvbYN985Nd5G8wlX69/y7nkNZX9vyGfGVc1NayqebK8smldv+SqcJ//yraJyAl7'
        b'96CBvfym5QmOy+ZYLRR1yPTPQFGHrlMwGFRSPxZM/Qwmofpxf8t5/jVl+xlO7Ineb1kZdzj/v1XGsH43PEQ16nd/+mMnlwBGPhH96b/vktrAWJhYlyvNzuEzxgaf6V/q'
        b'LPzc7bMHLTT1RSHfp6QRTbyYjQmFcCtsCMEL54thK28GDa6DDtj+ciKFuybYbKXrmiXg+psse9eUMNtRR2E9OIERBpJY98xQAWUOP+CAPfBgvIk2QXDcw9auCICbtAkx'
        b'0yZeZuA2oQVxP3af0Os+oc99koGf/zdvKq95ZYBhU0kfVVMxxLm4a+sLexrc72QS54KRbjbEc7EW6yaocyBIOB3irc6lzrXOrM4NaYxUnXudR51nibsOAyP83jAww5rb'
        b'cAzMFBmZ6SPg+RXpBJgBG9wZbEYWA8wle/BIL7g4w0oJr4M6Ibxui/fgCTjADpziwNvgIGwgOIzFPkkqDAxIQQ0lC3S+Hh0At660AhvhCXCdUykRkL14uNk3VgVvUPDs'
        b'ehxImwI7xOtJxHW4rRreglc1AnB3Nbo6TqHGd2wiodxXAxus4A1+IERMgNcp0DYBbCV34El4Ax5SqekSeBpd1VFga3Q8856T8Fy0lYoHb81DF5co0Bw9l6AjaHjVV1XD'
        b'WYxfv5cC2+GdiQQ50L9GQFlTdkttxIXlW1avpBiirsFGP3gVXuYVRuAyKXAANlYyt1qtwA38JTWgjv2S+fCcZgK+1eYOD2MuwduWQ/kDu9RKeC03JRjvnzIQikbQbLG2'
        b'Vq0hkcOv2MLOSNgYCS6DU+E8RO1xCm6A22M06P1UImiB3UZIIK3v7VnZc+D+yDR0tz7XjMqHzQJUkfdiGTzIPni1OpLAJ65QEVTEUriDgGLsp4ObsIlLxZZQYVSYHbxf'
        b'/td///vfJdMwgiIwkj+j0PrvC+ZRmgRcRIcX3JGuexmsSwmZDS9MQirGzrC0/EBYjwjJDZTA3XNSUjOx9J+Jmge4kYO/T1AhXAh2g2OaOFzQATlsxfhBw4y4MaFRqR6e'
        b'HhOWxfIpRaoHOOGWdB58YA2vFC/UYHOpcdGgRYjy7xGCDeHmfLghHx4TwF15wiR7V/MpOeADcBceg5cSS1dalIhWWMI7ghpzsB1sSbXIsgZdcDM8FQ7vrpZ4wbrJUnhI'
        b'AA7OlICr06JgizNoBmcFmnxMaSvohtfw1uRGIRVhzgVd+eDKPLhfAOrhNrA/CGyBd+FusCsPNIjcytaBdrjBDdxd6uMGusEO8D64UbIabuFGBCJCdnrBywkOmRlgrxK3'
        b'NNLceFNd6ShO+EJzu8KpBbGulAbHmwW74MUlsCETdGbDulT09WGwPhtcCCIwNR2SBlxIkWVmEsXuIuy2KoZdgMGaWRSmUo1Uo7V5YWFabF4JpcHOZGOWwi78FS0WlNga'
        b'ncxetAzsBZ3wNmyjI8AmeHpyJKqPtiWwqRBch53wUH4APDkPUb3BKQ9sUoC6UlRhN82WgDt2tRx4WoMnmmAlPD+UTExjSmga394Jgz9BhwRNS5tjJbiHnbeA3eA2uJIn'
        b'oQmOB96XjMFtAOweD1vC4K7UEDRmoEoWmfPCpVVkmJkB21PSQ9Myc1OIfpmKoWrBswnkVNf0d6WEpGWvypCmhgahBrJdYl2mgrdIPwF34LWC78IhOS3RopCywxBhZNA4'
        b'lpIaLKucCnfRFAfsomeCeh8NDmSKlKIuy+AUxLYdmUwHCEtLDc1hoIOsun0c7jXEZiE9vAoPlNk5obM5VG2ebW0i2KPJRYXZWmSnw11hoG0N3Jk6i0USslp8SkYW+VTp'
        b'LPNqeGNWSlqmLCRURnCKuLPpwGhkaIY7csaA06ghdpPq9zfnImEjcKKAKswoUqxAwhyBl4Hra+DVdLJzn85F03oXx14F6uAtsE+DIWI+TqjrZkkywc6s1JDU/DkmsJEU'
        b'avLnwAZUr3vhjgVicB5pkadSvMH9FO9IcImHBi240R4eN0NK5TZwnVQxH55FPeLqqnXwqq2FOR7VrqpXaGjKUcXNmjqJQd8dGb80Fw1a/hFpXDTOdVKo8d0E2zWh6F46'
        b'bAMn0iWhZFFDhsgKNJRe0CC8Dy8vLBSbg02lrhoC/m0FN+DhXLAzD+7MR12DH0TDuhJwCO6sYIbrM2UTrKrhIbDDhkZvO4BGFHhuHqMCt4FNqCM0ZNBIBKEnUXBXOqop'
        b'DGvwGxOZrsdDWM3jiFEXufheEuErmtY6VeipNNgCD+gBPBQa6cjU1AmOgJPpcLssk4XCTAMN5MPXwGPxsAE1Y3AN3MvkUzxPGpwYZ0mQm+A0vA/b0lmwIDjHo6ztuHBL'
        b'oVMAPKTBEQJhExp0TqK2LcGcyAxJTV+C4RwYocKnxoEN/BLEm3oGBdqRDFrTDaIzwGbOOnAA7EcjI5lsnCvBzmAdxMK6lAv3gVu28OgY8gFj0TDWko77piwVEcmjwXGX'
        b'5cwk1Va7EDaEyuDuDNgOt9KUYCHHCVF+hXA6qzAYNkjT0PS9IxM1yAk06LBBE6MT0y8vO6BuDe7G4Fvou09GChhg6L3lqP4aQtPQjHsZ35tGg/PwwAqNmHnsKNyspRQ1'
        b'VNSHzdwRUd6giW+xtoLAVcHGdfAShppkyRBn68P0HNLzRwY2Bi8yg40pk5kW2CiA2zEISoIGH4sYjvla1Jt2FjBg1KMTktDEf02FRtfb8KoZxYEX6FD7aWWbB+byVdhB'
        b'7YSCHe/Pzsz62Qy7n1/3+Cj1420WzpNn/LXqr0Hv56RZXTh341zjuWOr/+fm9keZ+zdvDoz/Y3olbBPlfZ28xevJ5eLJ1dUzVf2TvvrFZ/dcpl/6qvTPYRs9A15s+6Ny'
        b'x6wzO69/oklp/YGwJfLVJ+q4ipSniw5encL9tkv+/46mftwsu7h+1mxLyYtzlqFWlqFbWjzsl7YvnnbOKvN3m1Xxm3778bJP76x44eEcL4rKCY2a7fmn4lN+6pLEOSeT'
        b'LjZt72k49+FPzUO6lrq6PF2zaU2S8E+LBS9qHvwm9P1DW+DPtu8amxMV9d5C53ZNoPW9zsKf5o5btnLM/S2TqxMlDYc2/7fLzsyiz6p/4HFrfNLCmO1pNgn1l6advvV0'
        b'64Hbt6NOawaLRBNetfx206/aHQZVRxO+vXHg/PLfrhq8FB4W9Ze1ny21ikxMOuq+/nLXr355rTqbMz1q7t9/4bW00+MQyNM0v9p26ScfxTv846yyeG1w39Ffffk36cFf'
        b'/n3/X5S3Wm9P/vPOGPsa/4ljJra0/p335Y++KlZIv/Kc/PupjePuHfrV6o3cX2gm/qBiyYeKZU9/dLPzo4n/c4s3/V9fdS7qyDr21LdTWbDr/JObNVn3U3dNu3h27S4b'
        b'5acf/ME18uflL6a2wAk5Av+nvP39j206Fce+CX9I//bArqi0/nF/GJjzu4G0v3374x7Z0j/Jo0N2lG9uivk41fm/XaBgm9enmkjbWHjar1RyeMafXwX+cfEHT29OzasN'
        b'mZN7/AdPx939W+fEGKsPkz865BAV0jB+9uQ9X1Vsn/YzyV9/k/cbM41myrWtpV9Ff3R2xe7jn6Tc9ip/9qcfK478+cyOy3v+36lqp581fBk41reIX/7Tm8HP/uvPbZu/'
        b'ut345B9HT2z7eKJmyTe/rwHfJP5t4xXukmevMqaqEmw+P5bot0p0b45Pct2abJ+P6tbk+IQ9+OHXCc3dUeGBY1YOfB1951exr37+l9z/WrRp8x8lP/7N1SsguOjZKoH0'
        b'4qVE/uOJT5+tmvbbLzfM+4i/+u8z1vd1bZ97cHvID/7tUqT4y6ND7TvPTfrV1q5Bl37XP/ZN+veJjzvjv0lY/JPor4+B7T/srJ7473NPD54tfb99ne/+f03POmVzbW6+'
        b'xJ/gsxxg3Xg9sI4B1YH74Bw8ALbGEmyhDJyuSc+CR1JYUGSG+0tmyFwxAw2Y8HwAO2KicfkuA2E7De/ZYyymLThuDMc0R4L+bQJhWwyOwXtaHDWfMkdKx2qwuxrsB60v'
        b'8aiVYg3vGo/moIELL6bHkXfnz6PxWL5mpX4kL0pgoJL3QB2Suxt02DsCE70CdsDTwpkEZ7kSnHchmnOmj5pPCZZyPJGgwAAEM8H+pOAgqQRuD0Hy2VxOMRqb0EBZyeD2'
        b'riGl61ywFM9yIeBeIhpIwS5OqAd4nxAMt8Y4onkbdM3QodxsZ3PL6QVkOX2uugSD+rAUlaUTpWflSwSUVzoPHgM3HQhtKQnWweT18BhSdAWgkxNZCI4x7D5vtzwYQ0N5'
        b'ySw4dDk4RFb3/R1kKrDTPAxsXyGEV1QYKc7CNQ2hmvC6ANwLgA1k2X5sEGwP1i/Zj0E1tktA2adykRzdlk4qsQB+MDldu02QBbcvBldRPY+B27iIl7tiSSVGeuUAJLBt'
        b'h3WrwkLx+J1uRtlmcZfAbaXEhscWyRLBWSEYNUruWcF7nNUzkdrTApsJ00BjvMpI2IkHZ5G0s9mHYEYnjUlGM1oYuKed0ZbaEeqRinW9Wm9cFA826tDC4JCA1CS4M8EF'
        b'kYbhleAMOMFALEVg28tQIrjnoEYyMmaQAQxKwE5w5b2yl76MvLJtPmiYBQ7okKqGKFV4B7a89EP5bJRIjGjISgPtjoboST1ysgRsJY2pejG8gWo6HFxJIzssqAvYwg3c'
        b'ypB55LYvODgJieyIaUjK41NWFRwv0AwPF8GzzNftI1BkNAGDTY7a+dcMXCBrTlI0l3cQiSUzQSuvwM2zGJDsXrAZbhsisIC74LoTbIQXXxKRpQ0cA20GIgs8YzNEZgHd'
        b'YaSJxMOu+YjKULDHVSrL0AJVx8KtPHuwFTS/xNp10qT1DKfh+RVvCO3kg+MEjA23wtMB6RngeEIqGnhy6CCkUZBmh5i/ETXTkEA0dqRju7HzHGzLUgvO5UgC/3MozP/d'
        b'A9nnMtxaHh5ibQgSdMB2SFgixieBbgVuyF2y9mfDZ9aD87wpsd/xNS1rGMRnl9lN+z6vKRg+6Xlw9d7V/SLf1jW9osgvPAN7JBkfq3+y+pPVvZJ5fZ7ze5znPw3M6HH0'
        b'7/cLPJvRlvHYL7rXL7prcdeKHr+Yxsx+/5CzC9oWdPl0RfT4RzfK+kV+7TYPRRNwekFbwSP/CTelPRkLe2MX9vuP75I/9I+9ua5nVv7D6fnkVSkfT+uVzO3znNfjPO+p'
        b'g0tLcmvS4ayHDsEswLS61z+xzzWpxzHpiYe4dSzGY/Z5SB97RPd6RHcV93nENlr2O4xtDup18Ov3krCfxu3ziurK6fWa1JiC7dMnNa1tXfFQFEjel92Tu7BXsrDPc1GP'
        b'86J+kQcGxraPexw0tRf9E019EPiR9ENpz6y8R/EMfbKeWXMezyrsRf8khX2eRT3ORc8cPJpL2/nt8tY1jxyi8BsmNq3RvmGQQ3sk0l9xOV5J9CDFcUnCgNCwCb2OwY2y'
        b'1uQnbtFdFY/cEknRi/o8C3qcC56JUGU8Ek3ql4Q32/T7+LWYPZUEozPvsMfe0b3e0X3eEx97T+31ntrnPb3Rpt/V+3hoS+jhsEazJ67+raV9rlJ05jC2saZpSqvvQwd/'
        b'wjgtz1D6uj6Hce32Wo7m9Lnm9jjmPnMQsZb7reP3riPUJPV5Jvc4Y/drLavbo24mPPKKeyiKI7fS+zwzepwzXg9cFR2ctndaa+nZyrbKR+Mm9rOtysvv+PqW9e01l1Z3'
        b'rH7A+0j4obB5/SMv2Rc+IT2h83sWKR4vKutF/0LL+nyW9rgvfersedymxaYnYP4j5wXEo1FbbPuSm9xHvlOeeAW3p5zLvEk/8Pso+MNgVMielCdOXq3m7b6PnKRPvELa'
        b'38Nw4BQc1HdJu/kjh4h+r4Dja1vWHl6PMrr4tqa0yx+5MLjo+X2uC3ocFzzThjNtrTm7pm1NV97D6LSbC/vdvFuTWqa3J3ct+opLOyfSjTz0dSjjlJYpvQ4BTMPsc53a'
        b'4zj1KfZJhpjuS3ySYS8OexKeuXkyYXQ7ItvVj8Pie8Pi+4JnYmy082NJbK8k9uakPkkCKtk9iW5MwGhh54NT90xtTXzoIMHxVBL6PXxbF7fM35P01M0HwzUeu4X1uoU1'
        b'JjxzDuh39HvBdXCxfyZyG+SjX+wMy2/QDJ0NmlOoYbgfch+0wFeWlIv4uNUhq0ErfGWtvSfEVzbomeNZh7IGbfGVHeUb9Nhn4kOfiYNjcIn2lLvPoAO+40h5BD90T+my'
        b'eWDWE5by0H32x3M+TvvroBPONZZy9RkU4VzOlJvX8bBDYYMuON2VcvUcdMNn7vjMA5954jMvfCamfEIHvfFTPpQk9JJ1h/XjwPiHgfGDvviuH36zPzpr5A+GoGceu4T0'
        b'uoQ8dgnvdQnvcuxzmUDg4E880EXXygfOfR5pjUn9dmMPWu6xbI5uDXxkF9wfMr6Rx/jIaE3otZP02zketN5jrU3BIV5E7o3WBjsdXsxOxyEMmiPuIgLwIZggjhUrdTg8'
        b'A3cNbwM3/p6mCTwRDwMtm7IT+FrnzmekGSEIb83gBTSCZJ7lTdO5BMlsfHwbPDN2EHNFEMehPuRYxQm5Epr4t5C9AXqHrsPeGwT/EfTOEgnn2ROOCYRcXIlaoRQXF5WX'
        b'kzh3GLXLxv1DnCrDLCoqNwp/x0QgkMuZkDZF4gpFzbBCGURoYGFh9nJ1akUJqqXF5ZXFyyRSNlShFnOnUSlKNOUY+FZbqRHXFFUQvJm8rLpMPhyXZkREWQXJWEJc/rGu'
        b'bhQqxv8NE2ZHjP27i8vkquGotWEJsVVFyqLlYuypMFacSrBvqJWrynA4QPQejIMrEhdrVOrK5Uyxuk9LlRcWSrAb6BHhgog/Wn7g07IKcfVE6XjEinjExhrMTPWSIrWO'
        b'Wj0i0WSJ7LeRGIUEHszg/lABOGKhEYu0noRKlZWaKhKmxGSJ6NPVZcWa8iIlg2xUVSmKdQ4YVeJA7G8tBLEAvZZ42K2tQpcKdbFUQiphBGQjZqhaoa0Xtt4JIrwC0axB'
        b'jETl41ZXq619eSXxY1SFo1uaKtOoAobX6XfsaFsyW4xpEbAtG55INzD/TsxgthixLgNuygHeyDM08k1CMrnWzhdcARs0ODAeOI5U4lvs3ot4xlRzLt7iub0iHO5z9Uxx'
        b'8F+xFl7KAe+DCzPBvvnxqWpwHukYXeZTZSEeSKNug0cSwAdeq8A5u3BncIesjadNSin/iBLTaGAL2lYhoshaKlI72/xhgxSeBrfTMnMDsQ0eNi7HFv1mlM9SHjwP96wg'
        b'z//SnEdNpdHwOKMw47ImmCpzCBrDUR3FY0ffGAZJF9NAO8gjirefDj8TfqFkU9cyl5zmZc6fOm//x4ZXc8M/H5u6rwt+fZn6vKrwXMfi4sL3fmReNDGievzYZeorf2qX'
        b'ryg+N1+ocrAdW/PiV7O/5EddTdlRj91kjCnJslx2w6pH84X/pqrHl70/aNt0ubl+jzffOej5kXCno5857Zjr0/zNqa45z8eH+0X+QPVhQpDLpEgqt9oz8s4CiRXRmqPh'
        b'PhfDFRkPcJSxdIR7zMiCTCI8mJielQkOsQsyi3OJHd0UuClsiFZ7AF78DmUL7gGnX4oxe7tzwQEV3q0KdZkbqHXiOAY2ckEXbIJXib7OTU8wXrNBBdRXg/NcsnqRJgdn'
        b'5fBasKH9p58nY1h7ZkoBbEiporXmn4HgKFnWsMoCbXC3Q7CB0WveDKJd5sM9cD9eRQI7QoauIl2A1wjR8LbLFAPrUUYntwWXGbV8XDyj0d4HJxm1fKhOHgSvMGo5uGX1'
        b'nQg4vZ5lgR13kN48BImmSye6FY4sgHWrRf6mdat+1pwLCdWPRUEPRUG/9gwYpGjJDLo/PglLsc+5tESGzce8srD5mEsW/czNC8mEqDQkQR5eo7XOi+71iu7zmtjMQ4J7'
        b'y8xW3uHUds4hGRJFWwv6XKN7HKP7fQNOTGmPYuy3iKOwh0jkWdFrF/hT1rmjEUYy6HWizHCMJJ87DJKnY8RJQ1TkTH+adn5rVCQ9YIamxgI0N5r2m0fEBlrnjYfxxcPV'
        b'+eLhf2++eEqR2PBXngmxIVdRwYbeMo4ArFExYoSCDORo1kmMT52ZaxDVd6S5V7G4rFhVUFxehkqJJRh6rV/wEhyTp3iJlOSQJuLjTJJtpGDBBqWyXIwlRgAhOisAHItP'
        b'pSBkVirlOAHNaiZnHTb48Yg0SJPyMwpJmAhNVXllkVz79VqGmCwUR63ShX3AEyJr46PSlKmZEMQ6okzPhd9J1cyZeYUho300f9SPpmaP9tG49+aN+q0JCaN/NH60j76X'
        b'OH70j0YWikeQGN/g4agR7DBSS4gAxcpvCnmIOIht/kFGxhzG1iYEz21a4BrJhiRJWUTCWurb8NuYi8zBIjozKlRHSsONegsxc2GCmzHdCb2wuqxodJyKz8s3QUIs41Fc'
        b'xYwxDB1MdyuTf4dUORy45iQjspd7DONCSWxXZi2vUFIE1ATbZG4qKw5ZSN8+hQItNROZPd0z7uAuvBpuD46Hh/MpTioFj6WB98k9uB3chluCZVKM7jgwDm6g08EleIpA'
        b'P3zg/opgWRoH3dm0MIaeBDvAaXKj0B42BcvwejGomwOb6CmOcJeEx+wR765cDa/Cq+AE3G0Lr/Apris9dSLsZGAXjWA7OIxud5mDzWrYjaYHuJ/25iJayObLPSTvHlON'
        b'V3IoutIe3kPS0ip/Bqlw0h52qeCN5ZStEn0APEMHRcPLGiymzQEdJbDpPRGatcKoMCT1bmbKOgL3gpMYi4aBaG4OSLANKZdwSGlITDmnxkROH6Mj0dmNIb87CHRjAn3A'
        b'ST2B3kqmzMM0D5UYADp1VCQtIAwBTeB0DUv4WLgBER4slnAJg2uClhN+3IN1upeth9sIaAB0Wafgl8GT4LD+bfZwF6nOvJxYq2pw18tCxaO4FnQYvBTFInJmgBNWwsnw'
        b'itIWCYsh9PQxU5l6bofX4TW8Qz/H2sqGprjW9PQ0cFeDY37nu9akYyE+lxjBYAQQ2DYJCfYYsrF3DdIbdsAt4A7YB47koYt98A48BfciJu4Dd+z5FDyASH2vFJGNCauO'
        b'gZtyYSM6WwoOzqJSPWEzYV4keL8aNmFTmx258MxiRBuop+MCFGW7LGt5KuwqMKW9E5tOtDVFE8WgCCkGp8LTIh6NV1+J7vopOlcsCw9XX9ZccXKqviK/XDjrJ0eW//hB'
        b'9r59gLOlU1Iu+ZPqvSv9EZ/TCx9slNw+NCb+8fifhssKQ9LSn338yx+eO2iWe21rxE6Li8ct2rd6Nfwt+/YBl9+tigspCf88/NLWrfHh3M/uJ2Y4OH/luGGKLDzM84Of'
        b'5T5fexNpI7yNv7EsVkV8pvhw0ppjQDjB7VTBvpB/Tin8Z+nGVz/45OFPrNR3PbNlnFybPwWVcc5ckX+yVxHm9cWXL+S//+22P87xS5/u88V+lI37+NL2gvX1sQt2U984'
        b'TjkckWj3QegMlzZXccxBYckiB99SAZWqmXN8S5bEkdlh2QBOgQvpjlFGO7BImdg8jdkL/QBeAXVIOZkADhm4w5kMDhINBh5cAC4Gg8u1BtZF1iFcM6ShHSU7e7kquDmd'
        b'cbIDj8HLdFyCF9EgwAlxVTDokIVi7yw8sIWGm+FtS2Z/9fYacAY2oFGhW2jgy2aaOSG4FFzDHd9ANUEktnOqJ8MTDGB6TwxsCMYbs3grzhw2JMO9HLCxAB4nhbthT1sq'
        b'K3gdo40a4HWwi4LtoI3dUUP9dRdoBg1V0dj/27YZFqjf0mADc+/QUtQS0S0BulW3fhJ6E2iBu8jXVHARtegWLrQ+Evsr2wvvl5GNOB5ozcMbwuw2NTwJu1k3MUjhPk2e'
        b'Rs0cdQdVNUZAgTOaGNTJV8NOcqsQ3CtRgR2gDtPT+J6Agtc48CChB1xxhk3oIT566Cy8OR8NN2jAu8tw99Yq2I6GCTQ80+BiTRYFj2bCY6RCFomXq6pX4Dc1j02i4I4F'
        b'8DZbIWawDt1BLwIH4CGM3IMXxrG6lw+4zyiMSF0EZ9OMNMZLAqRNvMHyJdYm8OSiNwdTIWl61RhjCx+URFQqHB4Lq1QV43QqVXivV3iXfZd3j1cUVqlcG6f3ewW3q3u9'
        b'IhuTnzm4Nq9hvZdUP/Sa2u8f1JXY7yfpikaqlUfsl7FTb/nelN8vu1X2gXSQSzm5/lLk3u877uyktknteZfmd8y/6d8TMqPPN67ZvN/L9/jqltWH1zbzUPmsJmd+06/P'
        b'a3qP8/R+J+/WvIdOkieOztpTHKmmdk9tj19UryhK/wivzyu6xzkaxwJ3aXFpLXnoEjLiTcVDl+DhN51cDs7dM7fHJ7bXKVYbPWdopqcjPNU67qFTYL9bAOtUOqHPLaLH'
        b'MeLdb/o/dAoYdvN/xnr1R07snnx18gPeRxbQ4knk9EE+xzsOabQ45sYgxRkTTxtonwLGy4e1ofajFHCH2xoIKK13TUYBxZGcTbSYD7W65983UN+sR7qn5G11T62VDZZr'
        b'lBewVbtoiOfmAV5BVqpswKpgZn5OTqJsZmpiLhNQRufRecCqqqisgvXHoTyKNw8s9T4nmM2FbJwZezJRHsEH4rkEGnt+Jo6g8RI+UbfJJ0tc/w/sUuPB9Tv2pZVZeOfB'
        b'yOHvSewzZQ4TQWbQhnLzbM3t4t6MfFDc65BWh7e9RO6t0V38m/kf+/ePdRt2+tyM52ZTl/61NVcY/K3lNGEx/YLCx+czOCQWiuQrLu0WXJf+DEc4kfQ7TsNhUGYwYVBc'
        b'fZ7YhfY7xqMk1wS6Lk0fbCYKx4KZQELBsOFTEvFzybRh5BccjMUpngmWwoZdwTFc3GJI2BU2xgqOBeM8vS7lG3NbYdRzMeXi3esc1hZzcjL6qUv9mkcLw7ErbXd8iB00'
        b'p+LomfS33Bpa6PEtpT8+J8cXSi5l49Ti+0jo+Q3HTYg+jbLxGsRnL2LxjbxHQp+XnMnCeBrf8X1OThl/3ASLdbIctGC3wLXmBvALmnJN5pVNBueNZHqt2/6vtmAv3I7Y'
        b'7Ervh3seF/vgZvxvH+GxHriZc+yH2wL9xefYHzf2xs2k68/t5GPk9nIHcu4od9Kdj5WL0LkzOXeRu8rd5O5HrObxFPw6QQkt99iis7XBfrtZD9O03AodrbGvafTfXvu/'
        b'0/O8GZPXAv2VB7A7SFy5l4H/aTMOpeCz3rd9dH62zfVlo/+4dE4Jhy3Xgf21w79l+nR7lgb8a4H+W5bw5L6dfkY0BGJv5JiKOos6YZ19nWOJudzfgBoL4pFbQHzvjikR'
        b'EK/dlnXUSnqeFXGmIRmwx91mJonvTby4lyiUr8YbqWbDMzDRQI0yvZIiPS+2TFUZq1LLye/48PDx42Oxuhi7UiWPxYOUNDw8Av1HimikhDvAk2XlZA7wUlKTUwZ4+TnJ'
        b'2R30ACchER0t8CsLsmQZczt4Siz3D/DJ8syABRPqvQyd8kvKi0pVb/PaCPxanpIEZZfgQxAXj6+pslwm8MZblhUj4Q8pSxlFCsxNmB33Kn6JWl0VGxZWU1MjVZWtDMWK'
        b'sxI7lAktZp1ZSIsrl4fJFWFDKJQi9Tp8vBS9T8LRl9/BIa7DlaXEj8yARUbWzLiMAqRPvxqHiZ4Zn0ooRL/ZRbV4AMzBW0gqNSpUGh6FjmiSwYV10Mp8JtAJjpQ+YJ2b'
        b'KkvOSCyIj8ubmfKGRUVIuAxduk9+NXHIgzOVlSpVPFH0jcvIqCzNVJWSkiJwSRx9SYjAKbgs2yH8eOU68ke9cjLJPImVUSm4uSmnmyg7RonDQw8tJIYUEqmcge+N/PKI'
        b'V8Fv8aUDZnJFSZGmXE3YT+ry/7J1MLPycD9kslU1Yx9hgb1Sn4cdcGfZD/P+wCN2w78KHqu1G/agLNsURznOrQtGsBseMC9QVmrUqNkzYXSMxxOp9qaRCfEqCeXs8ZZ2'
        b'oTgI9GvfMJVvYB1aIxmFdWiHGSNTHTYhWB3VSldGJqSWWg4zQclGMCGlicEodpVOnKSXWOrMQ62/TxfpzzaZmdhhSGVc6JStUhjsMxQTFjL73HjUf82+Qq6mqqpSiZcs'
        b'q0hUZSKMqmKHZwwVD+mZ4sCERMnrs+Ge/Z05YsSBQaoyvGlePVE6IegNimQGC3HgzJTvzswOCjhziPi73jPygCUOTM17qyciXvPEm449uIihRI+0hcMuQzPrtYx3I7li'
        b'sbpSqQsIO9KTeIJmHhvabKqUZZXKMnUtE2IpMAhP+0GIIDzxB5le1Q/C4gDOgyfnILyFE4Rn1SCJVI/rmCAdLw2PZbOYLkYPAQknWdlS9ckTSDJT9EgfxviZYz/NhK84'
        b'hj8BKuIubkT2kM3KWGP3WKSTmfbnxrq3GpEmvZM2hjCmvw71tob9melQQCZAPvgPuqfBW4d4V43sZhAEkqJIjRsU+qjaoQ7xMAZmBB9beEcElVNTpGQBSwYBhQl3xLkK'
        b'Bf5WTblCXKRGgtxijdo0WTPj8hKTs3LmFmTn52Rn5SYW4AjuuYRKHViI+PsygThimcQMQgx/suNSZVo/j9p606ry7F6OaWyNfn+H7BkyJei3X4KGjClBI6KTSA1VMf1U'
        b'RZg45NmYIObrtFnKKkw7AGOc1SERmNkSwnikCnFifs4I+1QV4tyaMvUqhbKcVJz6NcQzA+IIfQl1mFR1UXkteXDkES5o5DbLetljKkTvfA+3fLZKdI74mC3jEb5IzYCt'
        b'DGKwGT1r5MJxxFGLlDRsDw+xh5XTVNrmO6Rc03VCtBLDnpIaHycTL1aUV1aU4pK+Y6/LYpgIZicjuyR5q+Eh2JQOd8FGLgWugG4OPEkHwo55jJVkHTwVyKKr4CnQShBW'
        b'E2E9A7HCItqqSnhVJRRyQD08yEYWec+TMaLcAw8GWyWsQoo72AG70d+roJ5HCeEWDmwArcuYCAvdsF2QDrpi9Nb3FGUPT3DBjjXwLgnxYB9ekPudATgoOdhKgZ2w29Ii'
        b'YTLrhQpJk+cn4A0bvF0Dmgrxjo0cvM9IntvhzgIrId7jAQfhDrzPIwIHiP06uFXmZhCARU+YzlC5SijMwfFXAkNl+YGBqKgdYXB7COiQTc5jY7uE4qX0gw40OLQuidnd'
        b'OpaUoMJBP+CBEDbuR3oh2WxUWWE3EFTKDf9C63l8IUWs0VcWWhiGAkmRpmXCevTBYaHgbg6sy5iVws0B9cSFwS1wutafAvd5VrA5NbLsUPZhjuozVITvjmXLGzMtQbjd'
        b'+6VLB6LqnRL2nDBb8efUL+RONcsleQM7b7p8ePpm4LHWg1GnX5rtfeIX+eVqWDzthRV/RyL9ycTuMN/EiPcd94h/8XyjT2OU9ZFVFjv90pas8rz1hXnNGe7dP2x69mXr'
        b'16m7t/78x9STxG3RBxqPbpf77Pmy98Rv/Ob947LNtk+4qb/vvx0rmGjVLdZ0x5RmCv+WlL53zrSyV1LPyf/d7ffZj5tm7Zw/vvNPP//sFyfpu9O+6Y65+dm49AvBmtSL'
        b'Y+ubYpbxnep+63Xyblhf4pcSIbNR0Ql35QdLQ1NCOXAnOE0JwClOuPNKArUKB2fhQRxqCezMx3sr2HyuHgdcssnhRpTaMDZH9+PWGW2wpEk41a7gOLPhc8sHbMRArL0z'
        b'jQwJ4YEJ7gT/JVgHuvGGjy/cTSBr8DhoYrZ1NhQlpktDF4caWc2NAedIuX5OlGFMh/nghhYB1slYL4JOzlS8j2IFLxl724cX4H3Gn30TvA6PsHst6HSjCef94IQrY1h2'
        b'ANxxNoyzALpSSKiFRaADdhN6k+FW1O0amCAQyWpm3wuVsI35mqtw20T0Ltxhr3EpuA92cjPppHlcgnUr4WOzrF0ZNHZJQXEW0xGwca7E+p3WX/GanSHs28BdtUk9y9Az'
        b'PIfZTXkpD6bGjO0ZG9ju12s36abogd/Hgp7s/P6YhAclHy95yaXHvIfNVFw9j7u1uDUK+l28Wif0uEga+XhPxITJkINIb7Ig8mkt7xWN/7lnYP+kKfeFHwg/rB7k0kFZ'
        b'BNWWTVBt2fRTkVsPKkMUhi1kKDqIAOCeo2zJJFsKyZZCP3MT9weGNvOOCPtDIpp5j5wlzxycm5Meu4f2uoe2Kx65Rz3F2y/uBxfsWdDq0xrR4+Tf7njJpcOl12n8zYn3'
        b'J9+ebOjgfpBLTUmme5zGG6iwQgPA/2v1x5HRcTjypREc/w0rJBMrvjiGFcHezwnCnsO/flv/4cRFZqsgnOqymvxO/sP5BVgZGMmHr6nv0Hry3Ym+Q4mRj4wnX+kbaBxD'
        b'/XnjtcfclLicAV5CYnzeAG9mTmKCxMyUGYbyG220zAGz4iVFylKFykizt9V+dR067Dcf0TkUdg1lVmeDNHus49sSJ1B2dWNKbP8DLqBKkI7fbkrHj5PLkeBpCFvXyjgm'
        b'Vnh10vHwpYIScSyW3WMLdX4RC01AnkJYWVPn6Rfj5oebGaC3GxJUjGTZxUhnqNSo9RqEGjNezepXb6S5sjoH0y7eQHktWq5/1pAcJl1cpBKXlFcW4fUjpH2UoZQKzfLF'
        b'CtOCPn5dhW6tBIuNWmxlHCnNFEyKocJIozMkQ6vPqRUrGXUFc4XxdrycwfyPAOJHecrkWNbWs0KpIFYciDLmG8SBiFAl+TQiS/vkJEmlUh/JCFoAgxojBilFuDWp1EpN'
        b'sVqDSteXLBUnaUGXBvdNlqd7hrRMTVW5QtsEWEQrUjvwxyLNaDlipckyAnMSkxLx3mhigSw/Mz4xJ0SsVRrzEt/Lk4zIbwWxQMHMVlTIQ9WVoejHgD+BlVWMRc5rSlhp'
        b'Sg9HqQoltuQx1MNfWxz+o1PTMYdfp0XrvE+zrdpkaUsqy+Vo1DSpcIsRVxJzZHEZw5Vr00Yrb6hwyzWKAmzAwrACXYnxFWmwbLvB/UKtKEXtAjWQwkJZZQUeKV5jzbNS'
        b'rX87LgyXgvQrbEGDBwhd0y1RVi5HrJIXjWB2U65h1jVLy6oVFdqWj7qmHKMfA4srK1RliF24JMS4MpKKuDwiYUwxhqtBEsPPZEitXLxUUaxmxgPT+mdu1qQJ4RGkcaPK'
        b'Id+DaQhh4zmw30uWZ3DfRIOiyXJKNErS10hvJ5ZEIyvhzCQWK85llV6VuGZJGdKjsWFSLXpLeTnqfEVKRvVlMpseW1SqyuIyUgk6FbxKWYk6MsGkI9aylY06AtPsTTPz'
        b'/2PvPeCiuraG7zMz9KEpRUDAAWkDDKBIE5Tem3RpItIVEBiwxo7SFEFFQURARUBFQFTAArh3EjXRyDDqoDHG3BRTjYolMcn13XufAcFoynPv7z7v937XezPM7HPOPruf'
        b'tddZ679erXIWnCC0GU/MycnMSCJ22VgbQubTeEerN88dd3rNSBQviuju+PnOMUGfXHMOfspzTIIjQrm4M/DTnmPi5hn0lnloOs5zzJZr+hf82caMXF3HlvrXgmL/kfH8'
        b'n2gCptG+VHkzQYX/vNjxkTSLIolQSfap6bZon6pqLElxFgb42q+md/+geR3chbb/oDZrNK6oepAXbbVZCnvSiYmoUwRNK2Sn0YaUjQXwCEEcUsr5NOIQVMLt4eRdv2am'
        b'HHuCwgC0e47pDI7kEGetSbAPrIdl4vCUOAhquJjW5c8zjfQx94sQKwqsQOEbg3ViBmK75yS0W2wvINqAGHAE7aaJpmASaKZtO83tCubj0lYvB01vvxk4n/fqfuNu9ipW'
        b'cYjJGMWNK0XNtlKFHfAsrKONTUvheQeshWCH0ramoCasYCU+0L9yiT+hW/L8grEags5EEu6Am+UMNUGr3KvdvwvcgO1x4YHJYDM4FA4akkNAidtasBdsBEfR/w6iv1uW'
        b'rAAV4LDbogWg1C0vIyRk8YI8Q0dQEwdqlqQrU7B8jjbYBzphK604aYB1Bmx4OkceHl3BpJjwHMMSnFUmLLk81Pjnflc0rSmjhYMlmqDEBVQuApsnlGozPAB34e/YHnah'
        b'EizioI1vyCSNdbCYVpA0rLNnL5PlowI30ha5SXBTwULcA3t1ZozpY7iRYpBlTkFBOKzIUfAyV4I7wsWtPk5Zg3U0eCiM0u4I79EyOBDt8VtklmGrX0VYrA7b5vgWOOO9'
        b'ATyg8IeYUXSNKWjjh0/oTXgKFCl4gyLDAi9c0CbQ6e5PwlVrgBNiIv42cGweGTUoY3/C3kNDaack3w+UTkbjuxTuDEXjsJQB+3MVvFEbtRQEUBibsx6e8x8f+Rrn4/Nq'
        b'2x85ITuwmQ12qRrCw2qgGTSpqy0AaOcOagIngaYM+QIX3LzH7a1J/caqBVrhXlI1JmxEm/yt8KQT6p2NsBA1L7FMBjsWUbAoVD4U7gMniGZsOtiaQ3oCbrGklWMBvlw/'
        b'nsWbgraOFk1h4oxBbVZXMBnN90PwQEEkynOKrcEoQy3E55XW7a9kDDvcXss71E8VnEOlrydDKgZuc8Y6N1lweDTWrocbMYQrwHqXBH0LOiKxx/TXYhL3LbfiMoPCMw4d'
        b'u0Hxb6Cto5Vm3rbwD4OglfLJurTaQ9/UDu2WU5auuHdl27R7l6TDfdSLwo9weBGb97GKy8xyPd7xWLtjW2yRxNntcUMPrnz00e2zPyuuU3Y9d3nNg8MSJWk3NxazK5cV'
        b'Xvc+EakZFO504rrGe7sunZNw3d92mW+zslhrza6FD35wkf06QmnkQk6pnYX8g+/OHDSy3n+JeVHq1GT+7eTq2zv9v5QsXLRn0rfFCVIFjE6NVINf6qvvWcyrGrq6uuRz'
        b'5YNZNwo3eprJ8+bdSbt5zE6Jf1Ku7saNY3b2c25dlJYKCjv4vWx7c8PXaqq/uS2wX/3VqZauT3423Vfe3SLt9tsX9avaGnQHc/LY+84yF3z63Rm9fMtqtSkFtZudLL89'
        b'stJwSluoWpX5jxrvbV//PPzX37ZEr/LIn/VB2gGpY30flMpa+5ffNvTWil98PrV76bdPPW4cWHA/WCl7oewN9UVa1nc/ZBhf59XdnyfcoPRIoFt1MDTqzLab3OXdOc8j'
        b'vqs6knFaf3ZY0pP5qe9JKU1e7Zfu3Hn//uT7anf/eaaoWzrhrHr7iJRSTd3sJbNyVwzsyzVLm7ZgeYXo/JZoxeXZAqrvtM7dbcfDt9zxaJXKfrzmxjU5HRDneMtg2yZm'
        b'mB1/iVHAi+E9M75yavjgvmVif/X37iZcdVr9dhgWrfJHCwdoBWXjFXjwJKyjiUN9qUmv4cVgP9jGhLvBIdBJ3FlngdOgwz+Yp7mMdmedKUdMtsOWw70TCGCL4REmPO4B'
        b'DtLoqPNoad5Fa+Lk4OFRE/QAVxpB1gE6QC0d7BWUSufBU+OivUpK0YXfC6sUJpLCULH3MCF6KpynY9Tv0E8j+sfJshMdUJfYEfUkqARFoBv0gcaJXrHL9OAJojRdBcrc'
        b'SIxs0A0LRy3arWAPORgDiuA+s1C0upcE+4JjEpRUJlMfdOrQdtzVeBnxh6UBKrBfzFerBFtJ5RJhBQkyijWa6Pl6drza8zgof2KIrz9ki9qn7PVwpaBVYVTpOR+W05Wo'
        b'B0fhoYlMKFCizVIrEIdNXQm3wUJ03Bx1cjkslqAkzBngzHQW6aVZWtpYYQr7p02ITbvAdxVtP74X9M80y5Miemda5ww6vUkJUUOAUv8AX1Dymm8yi7JydAU9Upag1UFs'
        b'+h9gS8aQzxrK3C8YSSCKHqw5iuAsHdW10RBsNUNiwb7xfscyEbSlPNyhBMryQatlII+LCjCHyXEFtdwp/xumsrhbR6XKtxM69N+gXHsTuQlbAONIC6k8HNbTqMXo+pQZ'
        b't3SmN3i1eLQHtgZi+JHXvTcraDkGzfKN8iLODAFnBiEzcWwqFIb1TMbFs6xQvGdgIjKYJTCYJTKwFxjY9+gIDbwHlfWGVTT3OFc6t9gMznQfNPUQqHjc0zeu9B9W029I'
        b'HlIzbVk7oDpk6XlP36jS/6EUZTCjI0gw3a3CH4OJLGsshVpmQ1o+HVLdSp1KAzYCK58K6Yec0YiYncvvaBk8pBhGtlhXzO5lP2IxjDxI+ExPEj7Tk0EDcRwqHRqkhlSM'
        b'bk3VF2uMXYmi2I0oit0Yn02dLg5fedCpRubeOAP2V1dEkiuiyBVRjHtTdNFxMQRqFGs1/ropuuLrPMl1XuQ6LwaG8DjudaTZUULdkEGNkFH1d8Sg+ZxBg7kClbmo0Bra'
        b'e9ZUrhmcYtURRXOOhmwC73F4HapDHJseA9Fs/6HZ/oJ5sQR8FCHUjxzUjsSBS9E1LZKCKbwOswFVkWuowDV0aGYouZmYifXZFN3G1R1rLikO2UUOjytLgFA3cFAjcFh7'
        b'Omb5dEh3y5+QF1fAjVTAnVTAnXFPm1MfUBMg0rYa0rbqCO+O64wT2XgN2Xi98eyHcrj5HSsdRSpcgQq3xfC6itXwNKNKn3vT9Cp8vlDTGpzKa8kXqHkMRF1KHYyMH0xI'
        b'GvacNxgaMxiXPMJiqKcyKpioNaYZVTB3sXFDjWU1aOp4XcXplp4JGr2+rb496kPmzrem6TfMontROM2qwm2XDyEq4RitLfIClVnDJtY4zqnhsLjFAwSoNAZmFR67Au9N'
        b'0ayQHafYn/xWks8rFXJe8u9dDf7KtMaPsN8DeP7ejK6QHB9DNN6cwQgltJ1QxmPy+XfeAeA9apOUDXWK7UpNfAkgNbp7TUcfVVLEipG2P5YulimmUqXG7Bkl/532jC8W'
        b'/m5THZqSnZySx/8z7TZRpYm371h5k8jnzA8M+JM9ui71+h6dG0TEeDvQj2knY0bwIa/TysuixsDVtnPGOBlIgm9TUJsE9xaQmGwH8qRpyXdM7gUNYL1Y9gUtPmRPLO8N'
        b'j5M31lT+LFp4Rg/CnWSTDg5PccSH5iXkWyCBwmIZ+vDDTmkGCyTtApl0CAXvApy7BAXboxi6FKhAhTtMdpf8WLiRWBxkq2GbA9reoH4OUTLMW8Sae4c45i4013RypGj6'
        b'81F9sJ+EKNgF91rhgAr7KdA/B24hQQXADj48haMKUJaUFNeSPYfc3sMonS2bx6LwS1oGbKVgG6zMLRD7pK1fY8Y1dYD1GC25kgE3gO5ZpGSOi5L9sagUJElJqTPBBlgo'
        b'D5vBYVqdsQGe0A6D2ySiVmHCOQW2h9nS6oxutG/CWHG41XWMK+7qInYm5fPR9n4NOCz2JYX7VYhdxTuhaI/dBTvy4fn0MddUsDlEzClXisJerUqwHYkEYq9WTwOS4ywm'
        b'3MVepjAF7M9Bu2S0usHCQLqRKtHOp5zoMECLntg/FbSDFpry3SUVHwa2wV0RSBCqwrhymWDGZHgGnlxrQRre07E8iEXZMymrhYo9lBmt8uk3ni71Gwu/eFroFsExoBPz'
        b'9Hz0a1kEbCOnnM2nE2PmKmgFMlDfzFuY+f4CYzrxdJT6wlPUfCQxLHynLcSUIgYfk7Ikcd3mg9bfYdp9QBFd/1OwWharH8BueFBerH+YnUd6b4027ESHcpEguUcBCcyq'
        b'DEe4cSm5XWSUtJcbSwPfLnNaHAvHIsNzyHHKTNQFsE5vtAs20DE+9K1hJXuZLDykJfYARrvf7bQHcwNoYsAutgI8pYfWXpYRYw6s8ucyyGUq4BDs5QfhTcJCUMRkMzjL'
        b'QSFd7ObpoIu9DJ4Gp2G9EhPnaT8NjXmcpTo4ncDOY6HRtB+bMaC9OdgPm4jbti2acjtglzw8LY3DKxxnwJ0Y5V4Oq8nw1kAzpw4zyEIosF45RNaSHsT7EwzZJqZmsDMA'
        b'daUfM0IhBomYZGjNXrYSdln6wW50RBJsYsTBo3A3XE9l1DaNUHwPtEr/qr/5fPQvS7QjVPuWPzvfVbvmi/OdRreNTpduTK9Vn8Q+He6R3rjRxKtiq0e2wT8Ov99ibSJZ'
        b'5XO9eHdpcQPnwNGNqpPUKvVN5Q4U3/tU/6dNaQ8+Qv9+fjBbePN7S2v+g5/7Rj65eGf1R9/3/roysaStpK21XPVFd3a97IPCnORrqyKzA7n+HfUf5NYmPZ2332fDB4Ut'
        b'szpP6H2Q9+XhzGu+YVeYLvdXpbulHsppK304M0jXOlPG0p/nedfta6nGrvy2r39KeeB+xaH53pcZJ73rFrWccbmWVNiS4/F1WH7KL7P9ezzdry1uSGvSvc0N8O71y75s'
        b'1v4Dv+zIhZBkHcnZ/1hVfPDDb6u6D5eX6Kz+RvmTj4+3vX81vf0fX33ygXXEmQ/ra+Sn31482/XdI7E5R7Vicz5cLGX6Kauta2DxUQflsC3V58/d4Hrfvr/S8eoVZvfQ'
        b'qo5DOd8H9j5IMNMrOvZTVtJQmiN1ICLj0ONJgSEvp65/KbMt6Don09l70m9q3HfunMkNzP5A55b63qded7U82jKeBHIWZxWEPM91tb4j7y352bdHf4GdrdJJQo3Bueap'
        b'U1bPu3hOssXiyKaSquv6fos37EgN9v1x8UC51LBDW/KM1slpsz6atnUk8ZP7UNs1S/SdRnfT17x7JRd/SHYv/5jR9XV5Ua3s558yzmUW7Iq9UXfnq63vfa7ycus5c6mh'
        b'fO100yMqd/yS8qYU8+26Pb/S0Xvwme1vule/nTFb9slP1ivC9/4UpNf3bO3VZXu7DdNyC63vfrv9Ro7ac8WQ3IRFaus3hwe8G54f/WPwlRdUcl2mp+hC6CJbq3VrCl4E'
        b'OiVrNxX1/FC9Iiv5VsykD28OSdQFTz/0ZeKDL8vlP3r/u5vPwndb3fUxvrR4duTwnpT1lke8Gwo2xyrcnvalLQyadfB+mtpMZ9vCpk83XWy8abz+xrVb6gXnCopXTj7i'
        b'M+yc9kFNdueCob6RA7lb7Hra1vi1317Z9vibd1dRYR4Xcq8++75qYWytodH27s9tPj857KCcINm78P6eT3Q2rdi/aXZRXcvKW86ux+4V1jWmORddlrwWVcBXmc3Yb/f8'
        b'eJLS3NU2osP7rLuf2H0i+u32e21Hu1LPdV2Mun48qV064+oqhfbemzlfl67ZGNf9zU35mvvswReTT2YzlsSfz7wZXB3F+SoiW2Fm9c2B7NUuL+46XnJcIfx0/a/UpI98'
        b'jcCnT9LCf5wawf/BvS2h9vGV+KsWls5p51a5Fxbopivpf7TRPM+Of/au/M8/PizRq/lyUtKzdV/aPL1/Tzt5rtKxgqfq3Ue6VVZvHPl2Z+9d3/eWn7v0s/Qzp9JHit1b'
        b'zAueWixVSPtpzoC0dcQV6NV5/O79BV/v40hmtd1jtVB1HwjufLrigWGUssPzrwLvL1hl23F8rsS5wzO8BFvCWVLvGkaxpPp23XDJU49T0HjIPbrhC/OMIwzWd4aRrMv3'
        b't6OD3z8IZ01jvFO6eKBhjqvNw2lmL5OyDwrORFz7qnle/OPnyjmsiHpXyU8+ecZvofbFV0t/z5tCnXZ9dPf6o771j/oKb7Y3PK09VFq3pPqM1K+2a7O++G6Z+9Ff1Vf8'
        b'IPn04+Uu/pt+tnG/WzbQr/lcqc9X/cZz9/OrRR/c6zq0b90v9ceGO7u3J2+OjXRe36da/JvxwIJwZ75ZCq8/Z0ny++u+bAtfuvVif9DU/s++ku67vLfvjvqiBf2uv728'
        b'P4UX7hD2yfXHv627nzX75W+Cl/3uP26f0pToLPfPTko+o+Cnp3u6LHeIrklHP3Pb+0HUfaDy/gcvlbIPmqS+dO5te6nTFLu8qWTWFwpX3/300Ip/as29GKT0TbvIt/v6'
        b'uqI7O16wv1Y83vyN/I4X2qtM86Jifp4SUBok4C3kZpLwtuDkPB1xiNEoUAu3vhZiNNeAbO+9QTNjonbFw2FZKGgmKhx4ApTnjjfYohKQRID1D0pwI31GpTZAQt82/zHt'
        b'hJIVC5bKpIEjcBNR8sRg47VXrvi0IiVb2QPs86PZ38VMg1FFilXC743HosEJ2h/+MNiMQ/XSqGyehU9AkKQxKKTUAyQU4ElYTmutDoAWOzFDngbI54JDPG/YTWukmgLd'
        b'+OO9NBVgPwueAZ0usF6HWLOBY7AOdvMtUAF4eUFcWSSvdhF7PVjCombBo1LgbFwYX5WokPRAub3/qPpMKoGpCneZasF9NI/tBNwu5R+AVcpH4XlmPMNORYZcxAJbpVCH'
        b'WCKpGJdvOxMcizZMj6Q1LWcdAiZQt+ERrZXxsIZGRmzyXMOGxTzYCbf6syhpeJIJGtYGo0f1XqIItIObnceOwy70gFUAxUxYCuvhORUOjbg/qCSHg5FIq4+GIoF1cTRv'
        b'YiuSn8vpy3m+6OZyTHAUbogyz6K1fZ2gDYmypr6wPAe/4IDb3bODpCll0MHKXwgKScU04Dlwzp8g4HDAm/PMAg2WK+gl2eerJ8Auf3hitXYwG7SaSFGysJsJmvzgWdJp'
        b'C1XgHr4FNzYAlsqirpGk5GA5E5bNX0sbDTaCQiYumiwXdpC6K4BzLHgE7lSBu32JFspXYQnWAsLKuWNYC2nYQ3d5ITw8HfehmQVXzsT0nVjQKkFN1mDB9bPFgQXAMQ6H'
        b'beEPT3NhGaq5IhMcDoxFzdFMwA3waJ4VP4iRYEeLRi0W4DRpkqlgNybroNriBkeZT4cbYKkkNUmdBWo0NGndbCds8vUPMl5rDkosxyLLTAUbJcDhlWvphi9Ng818C1/Q'
        b'Lo9OoChFKZYWOOYM9kuQ0tuAQ7JsP7Qr6OcF5II2HzQs+VwGpRku4R0wmZQv1SQOpVjDdgzRoUCvHtxC13vjAljuPxrISBJNul0sNCh3O4EtsJa2KT0wdxEq9wQ+Pqhd'
        b'uxTugA1kDLtyuXxfU7BrNhfJi2AXA2yTt6eVjs1gH9iJGrVMUhN2UAw2Bc7NW07qs8YBlGOl8nbQNQFs4mlIBslseG4ZQefDZuNRdr6JeOqGs8B+PJ1Ms8ex89Xgfm9x'
        b'dAhjHtvEYsEiWJIbgAokB/cywVm0UdlAipQIGkJxZQJ5DEp2BnOuCqgGuyXJqF9g5Mq24JqibipD61sG00snY/4kMqXyJoF9ZqhTLHxxGCzUAmAbC60vpxeF2JP5mA/7'
        b'4X5009wgLK02MxJAEayfLC5uAWgOZXPRXMDNgAZ8NcNxPjy1DLbT1rxV78B2rNOFNVZ4xBGVbiA8TY+4PnjSAA14DujB1WTBEgY4iMTvPtJGQXOjsdb20Bz8kkmKYvsx'
        b'YTOsXkj32RbVXH4AFxXyFDxBAkKgySKPFgJY50KvEufBTrATdRs3LwCTnRQskVyvJwP2AxpRAs8mrcKLwzTQi370IKEetMFDNMKlExajYnTl58EKdMeTaPcL+hhTFcAh'
        b'WklcCJphFX4fYCL5ikgD6qRII6s4wyZ64wFrF+GNB6gUq+inJMz2t5hgfcyDdZnzoshBXbS/PY5Kmwu3owJbMig5FyZodVhBgj3AkwEsPo5sQU9fVF1UcFgLzlGqaDWG'
        b'e0A/2E4edHzUdqf4sBz0wB6uHDhuDk/jBf4EWgM1lSVMVeNJBRJhEziAshIfkYxkZMyFpWDDLHrBLofnQRd+HyBFLUrFrwNyV9KdtQcN93r8enIZ7EIdOYmxOnsB3Aiq'
        b'6CW1SmY5n4QfSwhgoP0T3G4Ht5HrdB1BFdrroFI3wxMmaAbB/egEL7iDfv1QB/b7oSKb+C03ZVLSYCczgHJYGk46OQc96cqwhX0wVp2UmOPxo8Rkqa9MjtElF5vZF5iZ'
        b'8GB/6qtYVUoJYA95StrBsxH8IIj2avjhhVZb8ZqpAY5KzFAHlXRfnrTRpBd7sg+rZbig8+pnox4j+/HjixeSJocbPCy4pLHk4Ck0GOBZUzKIlFHNmvCDGB2ZDI4wIxk8'
        b'CVBOyxwHF4ESPuprWViyHP3Bd1gM2igVuJMF6kFhMt3YRx1hiz/Pz4w/GviKYtDNsgnuAl2gbOxtwkq4npNEkddYOavnsQsUYMciWdSYegzXVcqkB1wjbPhwK5r2oBu0'
        b'MVUZ05HgUUu/Xdrk4EAPHd9ccoYCbGX5LjO0FJvGJzBBx2sBwXQmg6qYOU9waAi0vu/TIuxTS1gaaM71DUSLOLGVl6TsnaTU4F40mtajYYDnztwV4DD9BmXs/UkobJ4D'
        b'WyY/mUkeYWigNZMANSVwX8IfxOSKgMdlLPlgI+mIvJWglE3O4uX6miapcXEUlpMscDAbLfJkOTiCGgs1V/Cr13iKYaw808BgsI20Z6Z2Ej+IC0vNxLPLkwmO2MIO0nCK'
        b'sDkKHQx1Jcv7bgYoXw12kaus4Hl3dGR0CbFhFaDHUGwoPSm32cDi0eglBvYTCk8HL9kWQQuG5UiWahwtfhA3QoMU/zQLHJJZRsYKPB8PjtJxzFxB12gos9FAZrBbnl6W'
        b'qmANKGSj8b4e7EJPSBbsZoAWWIgmEj6sD+pgBRuWjspFMhQTnlIPcUZyGB6qSbA6Bq3+YEO6HwNdehJNwfngAHk6z4P1YBOuppxfIB4m/qylFpQqKGRh2rICGac5oBO0'
        b'srlY6bKBYmhRcPNsCdLwpopgN5plnZZIpODC01Z4GVdezAKloIb2BgnV58Iucwsku7Ra4Llfg4PEbPAkDQ+KkVCyjY2j25iBEiaXoctFMh4RhfdFw+P8AHAQnPFFzSb7'
        b'qloasEJiNtwNaGoU3KWNRgYPPe+QDKnLnANqVZYAWkyEPRZyJCZqEM8Uj+lTTFR5sBueRZcS85mdRk58S1PY4cPF6845JqyO8FkdQCZE+gx4Bnbxgmj1zBpGENgOq5C8'
        b'UC4GGLvCvTgczatYNGvgCXE4mjpQT7rDEHSp8S2Q0AwaC7hoDUCPJyYT7IKHgsmgWK1MTJmwQO2rZIIXNgXYy3KA5x3AaToKFGqxTvRQIi4eoGglfgxhDw85sJ5uu6N+'
        b'aNJaBEphneIG5kqGE9xkRB+pAydYxPsDLdn2xPljl3gEbQaFpuPZZEywNRu706hwNf934T640d9ggjc+5oxUHlHlr9J8w0sO+hB5W5nDpt9WvmNF4sLvWnlHy2jQ2E+o'
        b'5T+o6o95V1Nrpoo0LQWaloNWrkJNtwqpYXWtPUsql4jUzQXq5i0RQnXrCtawhnY9u4Yt0rAQaFgMWjoLNVwqJIc1pg5p+DZINLMb2SLOLAFnVkeEkOOI0gY8B2Txcd0G'
        b'g2azRrNBDR76Rb9WG5ri15IyZOHbIyGy9xXY+w5y/Sok7k3jVMjfmmbUsKx2HfqiymlQbZ7WOE2oOqOC8ZmK+i2tqdUe9f41/mKPkySh9syOGQJtG6GWbYX7MGd6pe89'
        b'ran1pjWmwxqaIg1TgYapUMN8hMWcql7h/lCK0jNocG2UqvD9Qle/wmt4OrfZqdHp4NyKgGF0owCBqlVFwJ3p6N442MjBtcLptuOPDOsYiXR4Ah1eS2J7ems6ukG9XI1c'
        b'g22zY6OjUMMS/5apkWlQq1XCX1EbNXg0+zX6DRk4dNgOGXj0RAk1PIe1p1VLD2m4Nbg2+zb6tiR3xAksXIUGbuJ0D3F6asc7Agt3oYHHPU2dIU2XhsgGLfQHRytxEVi6'
        b'jFCKmloDiRcXX1g8rGdQHTWk40Q72XSkCrhOjymmju6AHoZXD3MMmmUbZVsiBRzrIc7cHqkhjs+AEWoNd4Yuagxd/SEd+4bw5ujG6A4jgaE9ubInsT+9N32Yo9cs0Sgx'
        b'7uCQoXtP5JBh4MAyIScIZeGs+1AZ5VAfXRPdYiTQsRrSDu5I7F7SuQTd2uCCwcAyaC60DUY9Uu09pJ3QIiEysReY2KOvPSH9Mb0xlxjXJC5LXAoXBcYLAuOFPguEcxJG'
        b'pip6M7Qe6lKaWvUKNQoNyw6s61B7TDGM/Rmj5YnEEYtEhnMEhnN6FgsNfYUcv8csprEH4940QxzHRjTNTjDNrkdOOM19RJKlqfVQBmcmVSM1rK1T71HjgUaTdqO2SG+m'
        b'QG+mUNt6eOzVq0DbaoSS1tHtCOmO7owe5hgNcVJaZrU7tTqJzOYKzOainwMzLtpfsL/kcS3gcoAoIEEQkDC4MGkwMWkwIFnonnIPX5I+eomLwMwF/RwIuRh1IepS+LW4'
        b'y3GiwEWCwEWDSamDyamDgWlCz3RyF7+WGe12rXYds7qdOp1E1h4Ca4+BsIFFg9a+QjM/XG2pRqmGfDwgRcaOAmNHIcdp2MC0QW6IkzoYEiEKiReExItCUoZCUoSWqYKQ'
        b'lEuqHYxu2U7ZHoMe/gCzh3vDymMwJEVgmTqiIG2rOyIpjxpFCzcKGrviRnntLvYCY3shxwH1sY4umTK4B51aGO2SrZItye1ZrVlCE6cRWUmUkTzOSLZGFmeE2hH19hAn'
        b'Cp2p0KqABkNaZ1pPcn9mb6ZobrBgbvDgvJDB0PDBuRFC20ihSRQabXoLGPfMLOkWcxwyc3zIokythriBHa7d3p3ePR79Ab0BIqcAgVOAcFbgEDd9MCRUFBIpCIkcjIoV'
        b'RSUJopJEUWmCqLTrIenDrm4X1S+oi4cVGlCxQte4EWkJHd0RlhQqqTKlpbt3aoPKYwqNiha9dpNWk2EdvVejV8erI/XE0gHJIe3QS15ozOl4oDFncECpRX2I49Zh2+3c'
        b'6YwGlJnWyBKGg6X6COWgO6XC68kyBjXNsJqJIwrlER68c0vi0FTLYVv77sWdiwXa1tVBrd73eDOqg4aNTJoXNy7umNSYVe2NgyjhAZ7YnNWYhdvOu8YbdwKeq/rtRq1G'
        b'Qs4M/Fu+Ub4ltD2qNWqI59mjIOR4kRHj0zKz3b7VHn3pYfRL9Ur15PWv6F0htPch1UV9omswpOPX4tEig/70qIoc/AQOfoM2fo8pGR1d1AmieTGCeTHDeobNmo2aLakC'
        b'vVm4K/R79PrNes1wCDG0AnWoCwzshgzceryGDAIGUtFYcNTHY0G/WaZRZtjAsNmj0YNecwZtvQa5XkPc8EuzrjlcdhjiLhicv0BokIAu0SOXGIo4VgKOFRoYaG7FdMYM'
        b'MC5KXJAYCBd5Rgg8I4QukUKbqBElmRC0JE2mdDhkEWrwoO1e6BVpUr9WrxZuD7lGOTRbZrXO6pAQWbkIrFyEZq5Cjhu61Ww8UnV06z1rPEdPnNnu0OogMvMUmHlemomL'
        b'JvKPF/jHN8gJOQtGWHKopbQofaMDU1tUBrV5Q9reHXrdJp0mPTP7HXsdhTO9h7V1RdrWqAuHtBehdmb3sgdcL3pc8Lg0WeS7UOC7UOiRKLRfhM7CT6P64JrgxxRqfXru'
        b'iftu2NDsQEJLwZBBKGpb417jAX28KF+0vGApnB06ZJA5GBkliowVRMYOxi0QxaUJ4tJEcUsEcUuEkZmk9UZYEjN0H8rhennVeI0ugaHNsY2xIkMbgaGNkGM7zNGnH7rW'
        b'aI1HKxjqR0a/bK8sWiOGDNJa8nBYL5Glq8DSFf1Ez4z0C+mX8nDoOFFwoiA4cXBRymBSymBwqtAr7R6+ZPHoJe4CS3f0E00o6cvSg/NCRfNiBfNiRfOSBfOSB1PSB1PT'
        b'B+dlCH0WkxsFtuS2L29d3pHXvbpztcjOW2DnfYl1afKgXYDQMhAPF69GL9Qhjq2O9GoqNHAeNrFoQM/GjMGIKFHEQkHEQlFE+lBEutA6QxCRfikcLQG+nb49yQPWA249'
        b'GTdm+QxGpAusM9Ai5qCPFjHSe6hd/Gr8xO3y2l0cBWaOQgOn0XbUIe04jZYcbJC8MKSdSg941CbJF5LRCHG87CjyTxb4Jwu9UoSzU3HPol4d0g5EfSrVKdWR253fmd/j'
        b'1h/cGyxE9bIKxBPXp8ZnmGPxmGLr6XfM6LbttMXFCGgMGDbhtku0Sgyb89r9W/2HrWZ0S3RKdER2yaMC8SzQWOU5isw9BeaeA8lCc/8h83gyLyMF89DSFiecF4+WV64p'
        b'mspcU7LqZgtN5qA5YmiEpoih+ZCBFyqTQqdCT5rQymtEjT1LH5fA9qE6ZWTcHNUY1RIlNLQZ0VRAi99yhi/DWOsZ5cvQnPp4ElqtHroyqWnTH6ZKUJO0RMocgTKnYRKS'
        b'OnwafYZV1fZ4V3oj+QrVW6hqjn/7VvrWZNUuFapaiH9VJzfECXRnCFVnjiakNrwj0LUWqs7CCX6Vflj4kaiRqA6vj6uJE+lYCHQsiHSkXS9fIy/S4Ao0uC36LTOQJNih'
        b'2q3ZqTmoMfsxJaepO2DTs5J8ET+VbnH0kMzIbeS2eLQHtAaIzOcIzOf0LOrJHTR3Fei7DSQJ9H2H9CMvpQ/pJw7GJKI2NTTCI0Dc9C1haNEctabyFNh4DvGiL6le076s'
        b'LfKNFvhGC01ihk3MhkxCOyS65Tvl6fUE/USP7MgLkZc8YTxa7w2NRqSl8QCSRU0praCmPsJWMZz8hFKZpPLIhJqkUx12XVlveIrWnlWVq3a+M6g8/efH7hKUVRrj58cL'
        b'mdSsxQziGz5kMHWFjMW3ZlNXKFjRtlCyb+J0vX0PgM2JFk6Q+fMeYIrX2wV+bSl0GQYx/Lyeel5gxWBMfkT9TZBXPpPwYDF97htFrHsNCgriSqCPvERMyZN/jcKa94Ii'
        b'DLMwdx/PQM8wwl0lrDEaw1o7xk7FJc/bhFtBLa/wP7WLwrs/l7fTUQ1xa74B80hhm7B1DNSMhdQjCaaCMpqS+qGMYR2bYT0kP5g9kpU0wPH6SNqcYb3pr6d5krRpY2mp'
        b'KI03rMejzzMdO+/1ND+UZkTuMRulWY6l2byWFktfi9IsUJoLAydq84bVZw6r8x5lMGw0FIt9HmYzKEX1ESZDQQfjSdUf4m+PdTG4NGrQLFgwP/bW1GmtYb0qF/hPWAzF'
        b'AMY9L79hV89nLEcFH8aIJE55KIG/P1rFoFS1bykbD6t6PJFkqnoxij0ey5B8WlM6vVoWXEi6bCMICRdERAti4gf9Fgx6JtzS0mm17p3em3TB4MKKQYd5wzrW6FJFGzRd'
        b'vRioRr7Bz1neTAWtEYp8SpND+OvzUAk3loLBUwp/0ixVgpKohPunYg+rfBopIjvqPcGknGJgPyyVgqVwh9QEazS2+O9IMmaqqvwJU5WVLCP+Ljvuuxz6zk6WJ98V0HdF'
        b'cbrSuO9ivuo+2TF2qupb2KmsN7JT1SZwS3XG2Knqv2OnTimkkjWOaf672anHtI5KjSuB7hg5VSFVMnnqHzBTtScwU9O4024rEdRwRl5KUr5HyqKM/BeWvwOmjjv6L9BS'
        b'7WlI3kwu87aEe3Co522W20y3PDO8yPDwhyXrr2NL7WnK08y/xToVX2T/93mmo7cjUKkZmGeaZ48xnyxCHs1zwPhRuVDPwOBwT8IxNXiNIRrm4RGakjsRZWeV54gr/FdO'
        b'nTEG+xwtyAuNt+U6RgCdWGau7IQ8cD/k/XM8RnS0cfIwvjPvJT70tnvMyPPGtf6/Dv7JpF63ZZUMoqOB7E8LhC1gHx+eHov4AQ6CQ8SYLhDuVWEvy4XlsAjTQYuxCesx'
        b'cCwjf0+6BB8vZAOGrQQNulOvjKFyyCp1iZWV6ozImdMVEvcopd67QlHX/SX7Dt3mMujX/rvhdu0EsIc4soy+vwYVMr/HiNJ8T43XJthEfCh+OY3xocn24035h6dyRoH5'
        b'ypz/CVT0rTedLD2OKJpo/z8giub5s/6vJYbiUKZ6Un+VGJpM2gcjEbEn/L8TFzo6A/8EFzo6g//0DPu/jAuduCi8DRf6trXlD/idb1wn3nz+38B1vs48od3zE7OxZz1G'
        b'l7wFxDF22ZsCM/0O8Tmhn8VYT/x8olGd6Bll+nZmxp/xNEdL8neImhmp/4Vp/r8D0xydcW9gSeJ/fwVpOXHS/kWk5Rsn8H+Blv8WoKVkUHjBXIoYVNa4vJmeCHe4vAO3'
        b'BdCO5D6v3uiDfljEhk1gO6jN+P7KbxL8IJRP1w7d2g9s6hoLGVKzNWc7rLq1YVaYcZpxrDHf2N94tfF3i5cVm093l0sy9nZSibMJU5/KkjL5yuKzws6w6khrt4FP5wdu'
        b'rZLf9w21PEHhjEYUV5K8VmbD3ZZmrzxJ80CzVR7Y90Qfl7sVFs/GBMNx+EJYBY7QCEO4F26gLd66vEHf+LhLheDUqOdshzsxWEuiFvm7oVPwi1r8lhac8X5C++3AfbBk'
        b'PI2QSRlOJt7A6FAbV+5/oBnAcsQb0X2/l2bGc/u8aBHqSY4DNUm9YmlDvkDZpiOtJ38g8lLEsK3rgO0le0zti2AQFXiFxC6F4Sm6e1bvWP0a/05j+n+OfffWGmlIjwff'
        b'Zdn/j8B3eXGs14T2vwq8S+MygvIW0AEO3gi7+13BR0l3bqjg40h3+m958P6Obif1x26ISdLjCsieIGhKThQ0kZgpKxY0mWJ0nQJG16WyiaApPUHQlCGCpvQ4QVNmnEgp'
        b'vVZGLGi+ljoh+O2aNwmaf4ytG7/P/n+CWTcRty6W3sQgtyz0vMNErf9i7P6LseP8F2P3X4zdn2PszN8q42Wi5wa98RrtiL9BtfuDJeM/SbX7D7PYJgcR9Zc2rAXH/cdQ'
        b'bJmGTEVQBbpp7LodFhbPha2lwTFhWaDEB5YE8yLFqCs/uA17+PhHYUQ5Rk9JUBi1IgvOSKcR/2+wC4mBh9mvcdmXu4gpa2dpT1tFX9iPwe7YlrKLRrstBmcKsBoK1sFq'
        b'9TGz3t8h0nPTxZB0dO1OWC8Lz4GSuAJzdOH8mOXYc+Ec7BRznmCxjznttg6LA5GsTvwoEoxlXBemFfDwnY6wlf3Hie/ggBKW3zEPyxyWB9KeMKFsabiNAzuJ9D/Hbjos'
        b'E2cVMS+KFxmFiV5+gQGgNdwHtPkEWvB8A1EGegGWTHCCPROUhYZRumCfYiboR9UjZo67QSfcRAIOS09iLMUe3rCUoOjZcBsOGTsue3AsLzIKU6pyZuZhNBXBxGHX4DJp'
        b'1GGHpQoscVOCE/wwXBR0ojpsGu2ocPqasXrHpkqDJnA6njh6W8IasI0ta5qniJqRNYkxRxmcJWrTSNQKOAxxlQfsXs7H/vP9DDNteJr4QLtMkqRkqPnWSi4LA/rZWlTG'
        b'c3krCf5LdESQerVux7VSYKU8P/j9tNAfXpoeKC5+/vSLG5/PfbfPbf6hu6GTKp81dE9yKlUS7LkT8nHM8hMd1R8WWn66tM/3kuGZjczSS9Obw3MSblWoFVUZSPYuFn2z'
        b'7PgXK29X7fVqW3ycygu7NtR9JPqkrNZH3EedjgcefNEhaW14zbbqwfE91OGrZ4J3q7hfVq3+3H/vc4O8gCTf6s3x9/d87Xvjq2OHtWfV/NP/q3mTr54NiAkfuFv55EH8'
        b's+5ftjXdf5gluir96SL9Ap27adnN3j82p61rvrKu6d2XATV+1xS3uQ1eVuyK/UGt9NfFnzr/XBv9w0FFw/vBxy1ePqtmyl2+FhH920eWMpHOIZ97byl05irT1tw9sCHM'
        b'34JnBOsnwNpRr1US215HP5cJqCfbZQQBD+pANzFXXpoE95Cov7qglEDgy0ERuXCRosM4DhM8AsvYoJ0JmxLAaWKWGwdq3UZ3XnBr4jgQUxqsps2KD8JjaA9YNjYegvPY'
        b'2Uy0EDSzya2DYImp2Pi2kEm2dUdSad8usD9tHGVKXYKOc7xx5hMjPJqb4C64UeykCA+B8t95KcJDcDvZWobAbbGkEqDLEtvhwxJ0M0V4lhUASuEZYgIctZQHy8LgBh42'
        b'rZaYywBHp8FWWsV+Dp6EO/xn+jGpcLCBAdsp2A0KxZ48cAvoAHVmnmiPPU4Bbws7yVEL23lmfoH0KoIqsNxRxZiF6t2YRLbM0bATnHm1Z46zZ1pNBntoV8INi+HpN/OX'
        b'wkCNFQYwweOgiav4b3oNjt/jcyaQj8YxUqa9vst6E/Ioj+bVP/Jw/LvII4zgmbZnXeW661NMyCbYXajlMajqcU9Fl6CHaCO7gZQha39y2E2o5T6o6v5Qnpqqj7lFFdKY'
        b'AISPzBFqzR1UnTusorXHcYdjgx02wO0w6DbvNBfNdBPMdBua7kZMm0fPm6IrmmIsmGJ8fQqXpIcMhseKwhcK0P+NFwq1EgdVE0lelY6DKqbibXpDfvPKxpUdnkPGDnd0'
        b'TQfNPC9JX5O/LC8wCxfqRgxqRAzrGNTH7o1tCW+Pbo3uMRziOZPTvC5NwSYmArMIoW7koEbkvan6oqnmgqnmQ1PtOtSHprr22FbI3Js6fe+chtwKmS+maFcntCQLprgP'
        b'eF+KHIyIG1ywaNgjeDAkejA2aYTF0EjB0J9JKeMj9Cr+FYzOnxuWkKEwkZjzN4aCJ1YYOKLTX66nnnvPZjB8Gc8o/Pkv6Qv+N9g4aE/9Iv5P2Thv2kL/m8A4nKACV7zA'
        b'FIEK2DqejFMw+Q/YOK+RcUBlcgHhuZV6gnIzH9gPz47icUAHtch9DotN6cNjLKxrSybSka02bMUInPnmo2hJcAIcoDkgG2DPYnypPdiBDhL2TR04S8NT0Kq5XgmrRBYG'
        b'sFQCKXLBHCXQhPE2VsQ84zCNt1kiX4A9stAaWuJH021cNClLLthIbq8H2wz4uSjjwwzsBkSBEvQg6ieCg18EOG7GNQ2UpKbDgwRvIxNPl+sIPJmF+TawS0eMuJEHLTOJ'
        b'yMPxhOvDkHBTZy0hptvMh0XkyDJYNhPTbfxYVPxaGm4zi0+LSTvBbjU2LV+2xhIWzUYOHdTnANjv/TpuBrTCXgY8uYBDGqLWr5xq8JxDeDMf8kJoYExuoD5lIFuGW4dZ'
        b'zbenE79M9aXy0wwxb8Y00NiNTvw6V56aLz0D82YCmkLS6EQj1SmUBCcBA2C0F9n7U0TYDQIb4WZC05mAm4HdnnxWMJJMW4hQFQFOYt/s07kKBBlUg7kyoAWcI/lWcaWp'
        b'60u0cL4BznP8KC6DgGXS50Zid0zYYi9BEXfMUx50u9QmwX7MgVHCz6tOjIHxTKHBMk3O8DQ7DzbAFpYYA5MDGkkBfMGOaAKBAbvAIWmKhsA4g6OEAYMHwRLCgEGPOypE'
        b'yYZckhIBO8UMGHAUVhIOTAyszCbAHxMktW/HHBhwCuwbY8HA3XATOJUR+k0pi9+EevqDH3rPz/+l7E646kdXA1JT7/cKP7m1LI1nlp5x1MTkvRjXdzpM5UqHNm60OLCt'
        b'PTYuJfKHI3alSrsubD4+X21SmZx6QYyHqqrHoWL0z6RY/6f2FXnGl5P5fVOXLl6y1vfxJ/y+kU+e9z5/+kFt+XfyaVvOV+Y86bq9wvxFnnbCu1+PLBreeRzqfpN7ZXlS'
        b'+wD3XoTfucLJSxZ1cALuRtyLDzoX/ynbL7w5o3/HwpQXP06O3bbayHb/5E11xw86uV+XKo7Zdn7N0rlXI0KqGs7k9T1OLls96TZj9olVxUlXtMKLzhumHew79vXZw4tP'
        b'LHmmeDjcN3COZ8imydEffTH/ZkT0jVMp0REpSt/ekROsXH8zedq7k0uuLVvwrSj0y7Jz+158Flc+dCln8+fBbSU3HsYH23tYm9eq6X28khOz6XbTjqFdpz9lfF97fXZV'
        b'YMHw5TaZTxQEbEaS2Vd+uQuSvwtsy53hzfjccH2nkaXNL1683N79S1f36FTFN8RmLGW0rTc+WhAeZP/M9WpUTviCyzP6FWI+M215qtXyNEY5rSRpxtkLn68qbytRmDH/'
        b'etby6YMqp7+/Ad5drvKPqd8PZdqNzFyt/ukjx998Y7882mPo/V7WTVOK3Vr9UYtG14Pu1DlU9Nnfntj3fLJX4cmnHnX79fZoxn6jWM5z8NaS/kR636YHj7XbOhWG8oy7'
        b'Q7ddPf/oyNm+toC5rkmqP1ROt2v9cObD5198ony+6KDUD8/ztl5tfiTX2fDL/bmX3lmn+OEhKSXXtiJKK5VaXXCuqPHa9HmbU377lffPgPobO5bt2rN1zq8mF6W6vw05'
        b'63407tRNVnWo3HFh5vZ62dNVnotmX/nwUfWjtFsvrkTdMN6QYBnxz5NZs9xYxTHf2Zy8aK3t/81qxRP9AyF9URcPDg/7Xb360jXshsmSkd3bBcvNrnRG+PelR96/pnPb'
        b'M2mxVuwnnoJNywajv3nx5H3bkNPDIYHuts9nehQpr5Fs4PVm3wye691wTcr74J2s3W3Knx3r1zNWumV8ZeVwzUdBRk9XKVh1fxFS/oHdMd6FVSsXLVnc9A7bauXjrOI+'
        b'1kFdVsinksO/aPvf+G3Ty3fXaC88rXnHe8Di8jPvpq1r/Nde+WHnlacGlvAW56vEb3PY609Ve63yffeX+0UxHxrPY99mtR2UV2xJD+LaLRUFe59IO3mrsrSrbrPON2GX'
        b'tqxWb716eURBt7nu/tSf5L76+Zm5/TW7n6ZcGfkhuvSLn6VuCtG3X7bf/1nq05fG117K/zTl0ojCbd7jX9dp/lzP3xqzZPuDq5YNs39ZKdOz4Yhl48ZHWi/Vwqln666w'
        b'bu5u37C09h86Nx71bXgU5Poktnht2tHhT9+/fuoznW9/Tf5EN//UBz9uiJi278paKub2leM7H/5T5nvH6NW357x/0/nLmIs/vv/VOtdbIy9Wp6BZ8s/MWyERP1u3lHl/'
        b'308tC/7nByEf/Lr28/QjF9fdb9rVu/Ty3ataSzX8a6a6v9M+/6P5vzGe1l89a5pvdFjFx/nky5175kwqbw4DHXKey78aaE9/8vDXf1gW3m/4evfzfV8f6jjvc7cheBL/'
        b'/Z2/JmgfNEn95ZxKikbG8k4fh5ETu+qcv7+i+TLtmfyk8qHoiJor2hGV61ifCFY7/+Dk9uPcorCEMKV/sn5qlpjruZabQxw3Qb0/ODC6jRndwkTmj21iasER2j3/BOh0'
        b'HaWtwKJpYpwtrIebaB/LSrgFnjOzgEfBkXHQFUJcgZWgnfasrbOGpa8hV2LhBlYaPCY+A22r1gfi13DTl75ipRBQCk/MxgVblDMwJgXUTBojpfAUYTvtAF4LN2LTp4mg'
        b'lDQdlstiI7K10fSYJEakcP0scn1BEazAfIVRToojKJQCXc6mxOFUHTb6E0rKhjWjoBTTWXAv7Vtf7CiJYSjRoGeMh2IImkEJvS8rUzUW41DAZniKRqKsdIBVdCtsQVvB'
        b'tlfEk71wE01FCdaHx8kbxdnwSMzviChg4ztM9GQ9A8poV3oekqbKLPCGEZSCUgJFAWVzyN5Ow3nBKBEF9vEJFCUq0o1m0WyCjaBhFIiCRJ1tGIoyikSZS2994R540MTf'
        b'zxw9ADvHqCgsUL6Q3lHXvCNBoChiJAonjoai+MAdpH6xKN/9fAvuKBMFHHGksSjwpNg9nAF2xbzORQmHB1gq80ET2Q8HmGSNgk2UkgjaJHaZE+0FXD8V7uEHwQqwkyEG'
        b'm4CzYD3ZaEvBfWi3P0Y2UdbHZRCDTWblkstzwB5fsbXafHCC3i9z0LYXH3NfBw+wg3hOKfJcVGNwkIF2+ydAOamzjj04+DuwgQGPlawZRW4dAIrD/YMm0lLYaM5gYApT'
        b'hgzcxbAX7p0ATMmJZDnLypO31CngXALbjxeATfO2wxIupqWATicGpSshATrhMTS+cTGkFoNNE9EooBtWsJxA5SpaEXMM9Mm/hkYBJ/NYS1fBMqLtmG8GW7DnOJOydqNd'
        b'5+3saX7BAViqjIkgoEpJkgajoMxoDhIqUe/ScaoQeADUEmVIxhIy3PIjTQkaBd3PV5+QUdBMqCAjScURoxReAaQD4VHMRjGzpReVmggPtomFGIwC69fSbBRQBWvpcVhk'
        b'60WzUeB+UE74KKAazYCtpEEDYH/6KB8FdOQTREoGQOslvtQ91PQ1QEpmAGuRLewntV2sARrwjetA2SgiBdYrm5BsJZxcMB2Ft/YVHwWegucS6Xl/OB300MRrCTQRQCPB'
        b'oyBJkS7vDjO4BY18XFOwGTTQfBTQGCC+dhlo9qcR/FK4fUsIIcUwke66Ithkxw/gjtFRNIMIHwUcg2105lWwagLcAHTyWbJo50JqtBR0wANoqeBgkVXMRymGhfRyAM85'
        b'EjrKSRalbUrYKDNgHw2nOSCJg37QQQunw/XiqIXb0bAnQncvbIrC4riyDS2No0LUk9Ko2k6ZCEcBe9B+KtNWj3ZcP7Mqji6qJYMofgm/ARWomzx0WGjX0oQBKeWwcSIk'
        b'RQxIsV9LcxY2gd1wBx+Wv85GgWUrlCVMFzqQDuPCo7CQ4FFM1owCUmCpDUWMNkB7qBVmo/iF0Kh0X7REk/F+MhsjTk/k6y0fpaMsoEAHybAAPbCO4mOoD3dJUTQdBe5W'
        b'orthbz5aZjAexYRJSYB2mo6iDw/QR+udQbOYjgLKwmlAikMk3EPTqEoNNAm3AQd7KA6Ep1BhNWDfctghYaYIKklnuYE6Srz/MImgdx+gfRkNH9lokIVVlRoFYgOUWlBF'
        b't9MBtLTuZY/mioctWuXr5MAOJho+Z8FOeumsA71gN8ob9oeSIYq2qvrRAaTKSnCjr9nY0gX7IzCZBdQ6k2KvhGfS+OR5aSorxrJMga0sSsdRAlROSqCncjd6NnXjRR3U'
        b'5I/RWWC9gZgzslJnnphlRboIHF9Ok1l89WkaTcVSDuGywCIeqlwkg2cON9CCxW6wmcGH25wWjCeziLEsQfAgjZU4D6tBrz9Rn8IDcwmYxT6SnlcHQXvi6zAVtRiWITxJ'
        b'T2m1COmxly7TQAWNUwFVyVq0nnezrsQbWCrg9HQxTgUtnJtX0IO+JGMF3Uywbh1uKYpShhtZ+Rr+pCLTzNAA7sLCjyws5fqK8RiaCWhebJDwXihJ8lidLEmfgyoJ21DN'
        b'kWCwj+kKumNIZbIjcOiCCdAU0DeXFUhmFhGA9oDDhuOU3cngLNF2wyrQSloqzxn1YBlpKLAzm6ia4e5ouguP+qvw0Y2D2UFgrzfcbobWZOWVrHfg5niahQYOgT1maPzB'
        b'7f6B72TjhqphroZHQA0ZJRqoE5DotTUQzWQkTe7UJTVkUJPUWGvgScsn1ugcBXgYbqBpMn+AkgEnwQ6Ck4H98Az9BGpYKzsKZFnrQ55fNJDFPp7Wku+EVTNodhRacODu'
        b'JYTGNF2Clhg3g9OwER9lou8hNBAsH9IMNSewWXI8dAp06LJkkNDWTZgx68BZeNgMyUhdwb8vJoHGZHmT57+zDdwzWkAXsJ7ciybewGq4kTYT6w9PH51iYmAMWjrFzBg1'
        b'FdI73GR4hE2kg7WglObFgPosugl2OYETY7gYcNiIEGNCQAnYRzfBQS9wik3AKmAjOEQTY2DvVBpu1IoeNxvRQr4+Yhw1ZpQZ04qkLrxWhkXCg2wukol7KJoZoxxPBDo3'
        b'9EBuFkNjQOUKU+4YNMYYVtOPkd0omy2YG2OBxgzspLExYDt6AJFFuAH2hrD9AjXgERaFsTHRKaRJ3MOM+QGv82LMkJxUITHbCdCvRkAbmlhsnoXLDDEzRiUZ1VibKHc2'
        b'oUeVmBizFsuDGBqDinIA9tIL3hmf2WJiTLgDzYzxATtzSHPNQqNvN0bGMJGwK6bGwCoZf9Kb2RmWaA6h7PvHIWNoXkwWkjXx9bG5AAlzfmJUzIpcAosBRwNJg82zhm2/'
        b'g8XAkxYsh5Wwklw+bwk8NS4acJ8MRsWAfU6kysqgDWz0twiE62E7emqtZKC20COj1R7sWiLmwYAOPTESZgM4osVV/w8DYPBofV2n/DtPUPXXFfbjuC+6cvQrm3Cnf437'
        b'MnVIw/F3iJcKyYdoX6L3b2S2mAk0zIQavL/DbHlz4l/DtajWKv77cC3im4g9wxtCmsMbw1uMDsahGuM01AYtDOKcTF4bHVUSatuL8Q8NXs3BjcFC7Vl/j5jyisKhWKPY'
        b'sKx5XeM6kbGzwNh5QE5o7C/UCMAl+i/+5P/3+BNFXFI83NWFGiZ4TCjUKIyrvhjqMc57Prw9rjVOxJsj4M0RmszFqbKtshhn4N3q3eF1NBg1D9d0RFLS0GiENeYhz2Jr'
        b'ao2EMGZhQMosAkjJ/FcBKdmN2X8HkDIiyUK9JvMvc0T8avwa8vAbYJGxq8DYdSDv4soLK0Xe0QLv6Go/oXaMeDbjzBQaFXDb+TT6oKLEtsaKeC4CnouI5yngeQoNvPAx'
        b'/0b/DmY3u5MtsnIXWLmLrPwEVn4iqzCBVdhg+AKhVYLQYOHoedJCA/sRaUncpGg+PlSmdKb9FQ6JzrT62JrY+oSahCEduw73DunHlCSqckh/dG+0uKXumfEwG6Pd+Ygz'
        b'GmnGvANLOySHDMN6ZvTb9doNzLzoeMHxovMFZ6Fj2JBh1mDUfFFUnCAqbjA+QRSfLohPF8VnCuIzr0dlDbu4XpS6IDWQezH/Qv6lQKF3jNAlFjU8LrLkXAyg+S+w5L/A'
        b'kv8psCSaMRvzSmaP4kqWMzCuZC3r/zZcyf+3KSUFLJpSEvqKUvKR1VS+k8VXBlPzGRb/VkrJW2TTYulxiJJAp38BUfIMI0rwJpIgSlgYUfIQe5Oo/if4InysL3oTWoRu'
        b'gRHcAq/DED7DdJagN2BFzN+AFTF/A1bk9bRUOo03rOM5hhDxmZAf721pmBZihWkhIQwuoYVE0rQQloKemBaCvj2WI5SPlrkXpr+FFWI4jhWCvz8KGmOF2GNWyOy/jwrB'
        b'Nwhl3PP0HXZ0fs5yVsDGUPgT3yYU3QZ/f+7GzGRiSgj+pCkhWMnvBPfBMrZeBOaEwBJzv0CLXN9AWGrOoExAv2QWqJefYJWjKP478gIDQtRex4PESIzhNTAoQ4UgNGTF'
        b'aA3FCamqE37JvfqVwUplHWONAjuSDYnDEHYXwu5D8sUKxYrFysWTi1VT5ZMlxoE2JJlUilSyZCGVLHVMegz3IU1SZVCq7LhUGZIqh1LZ41JlSao8SlUYlypHUhVRqtK4'
        b'VDZJVUapk8alypPUyShVZVyqAklVRalq41IVSao6Sp0yLlWJpGqgVM1xqcokVQulTh2XOomkaqNUnXGpk0mqLkqdNi5VhaRyUKreuFTVYslURrJ+oUyMGvk2HX1TL6ZQ'
        b'i7NQe0sVyxSzUXsrofaeRNrbAB2fspIpm8Y1ui3v7hoY7iG28PrsNPM1Zyvs7TD+DJpbMmarn78UB4nn0+fYzDSn/1qTkOr426wJmY0akvEtOK7j3IjEXjHEJ1rse4OO'
        b'5qfkkYjvS5el5KFfE92Axkd/N+ekJCalc/JScvJS+CnZ47IY56eE3eIm5PA2R4CJ5mwTfgQtxf4fvqmodsRWbnlKXgqHX7AoK4N4NGRkj3M1Jy4W6HAi+i8/PS9l4s2z'
        b'UvLTlyYT71tU5qWZy1KI4V0BfkpkrsSuGhPC23M8M4jXg4krV+zslznRFwS7TIi9ieiOsBT3w2iLm3NM3LijpyVy+CnYqyU/5Y86CfehiTsX+6cnjvMcEvvsLM3LSMvI'
        b'TszEjtJidBRqAuwE/lpF+fzENOIin4JhA5nYgY6uPSc5JQc9FvmcpXTBifuPifiYGx5hWUv5E71AkpZmZWGnRjL2XnM1CuIyb7NWZGXelkpKzMq3mZXEem25I0aI76CP'
        b'Knnao3EPRSaHNFqQmMSjkV6UlNDEUS5mpCoS20sWkyoZ805cI0FsL1njbC8lxllZstZKiG0vX0ud4M+IV9w/BWdMmHJvd015m7cSagfaUWl+YIDY0wZPgkSS76seRn1J'
        b'vNHQBH6zC5tJCj3w3ja7/wDoQDphNvbLT0pE68NCVKSFtMcQndlYJuMHaWL2m539kpMzaP8y8X0nDFI8nHMLUsQTnV+AZuDYQvNmR/YJXnjL0zPQFXieJhbkL81KzM9I'
        b'IsM6KyUvTeyN9Acu8Xlo/uYszU7GLUzP/gkz949tY6Wp121jdYP4WMkreviwS/DcjHskn3uZe7qMe/PEgawNfCpjjUyTRSb90DejiGHMIUnQBSthN34Fns+FJVxwGpRx'
        b'4W5wQhmUAPoa0OQ8mQRRD6dtE0uUjcBRSdiJvq+l1soZE5PJp34szBzySZRfaH5Xay5FDCMNYSE4CbqYsB8epyhHyhF0wJOZP718+fLZLAkc9NHlmufCzOGgdDrso3FA'
        b'BolPCXdZWzHN4UZK0oExDzSBI1xmAZZWQcc82M2HpYqwZDltKRMQZCFrOt/RhEHNhLukzFigj47C2Ad6bNmmKJkZyMgItgNt4DjKg7xuaI7Jgu2p43ORwx8MSn+2pD44'
        b'q0YsZ2EX7J7GptNZ8Awj3hG08uAmlAdutzRpsHVcBjZyvDxf09wgLuw08/W3wMY6kbBaRhuikhO7TanFsA92jR6TsWGmwDPZ4Kg7l0WHatwAeuBu/yC4lQcrra1smLAR'
        b'NlHya5hLvBULyNuvJgtQ/uq4FNy3hpJfy8wELXxyfA0sgpteHWfwQD0lv46ZBfZlFJji67fAWrgNltE+SD74xBCf8YZIHkrSstFT3MD+Ag4+vR/s06FffoTw4Gn86oMD'
        b'1lMqoJwF6uFWnQLsyg+KQZH2eOtrE2I2NQ/lG+Dvz2PmzgF12vA8KFWDJ+AJfz8DVVDqz5aDJ0CZX2gYlZKqbAdadMnQMVYnY0GG7bUwoE/RhSqIx/m3gFq4+Q03wJ5g'
        b'ln4RJrDEB24Nww5Y/hGwAx6yGxvCxPI72FdysqEc3AyaJCVhr6chaOVSnstVYR2qUB9qeDxMLKaDTtillJOHxgnsYVAWRpLKxAYbnMydy5bJW4Y6X4LhYm0amEmsea0S'
        b'58Mu+Vxy+jEGbJtsAApBCzmUyYe9/BwSq4Ulz4CbCxbCRlBFJsEcxyX8XHhCHl+1nmECdhnwYRkaSXREm0B0HTxN8gTnGLDSXx1sgi20+XYRH5SOv+ExOwN9uIEeMx3q'
        b'sH9cl4MzoJL0OaxeR9wFwSHYvgSfQHc7LA7k+QVH+IxdIW7O+UlgPeyiYH0mG7X4QV8yR7KVdeAZWPG7qylq+moJuEsinYSxnA8a5oaJOwWtRbIMUOKLOrwWFGdMPX2S'
        b'4hujJyhDwvlq1NVsoYvy3YI79tl3Tmav3SuhyPtHMKdRrlGd4aZtqqhtGpLr0jLPY0/oaRO3wBa/k+pqdlHn9RU3G19i5bifU2i/8G7yxePL4rLKTCu1FwWn9v2c+tXH'
        b'T1/4f2nGnx+37eNH1wcSL6edVb/m89HW7fdAycebwKdnf1vWvPfzKOXsm0oPjT8/rSH8aVKYefbxxEOLhmxCDnlzpkgfNPns1ON3/L7+XGkNR+XAxcBo/ZlVgR9T08s9'
        b'pA/fvxun+K3Bhaw4PnvLJc+Tezw5Rh5fxur9o/RDq/prk1f3gWHT/Jl5BzaaGkRlz7p5dHHwe7uOOn7ypfRV7WUFwsPaV49/xzWOddimq3OqeYSXd1M27mbthRdGNo/T'
        b'FIXZe3unB688EfjQaent9ZrPItW8/apPlb/3YNH3nmeH4+9mPZr17YmC9/f2bakaXD+7/Zbnt/sZbiyH1Y+32Hy86oPIgNbOuV+3VV2b3LxR7a7BzKuTT8fe3Kr+82XB'
        b'FPPfvj4yuCrzrmPhD7qJZ5fuER0I/Xir0vcz3Zr4L14Mn/Mv/KGxQDGOe/GrFcnbipb4rMhZbuhZtOaB8fdyhhEnbvh+YfZSwm/f5p9/enmYt/Ljk9k8MNJ1Z/WxHz2r'
        b'b/3sl/fe1vV+ltQvucNTFy+OmztjzsOVtudP7fr+mzb5tTbvLd8gtNjzoZHbxsBUkeA32fdv1uUzpfvjqplXvlgldXBD2LrF+pfTCrd9HbtKkcq/86HX12stXpSFNVxb'
        b'YvZ4bYqXy8t17i8/PGIuWZm0qSMrJq/1B/lmG6VTgdSZk2UH5niuueQc9rHb+/1Jl5s7C9SuRweHPy7/6dMfg41NXTIHfzryjSg+6HDE7h9Lzn28LM7LrOL9hsybfhu7'
        b'vC+n/MNn+6ppT9Ss2g9+JGPz9dOGddfm6VintZSf1XwpbEkq+inhKKvTVccysP9lqE6PSvL1DQXndO5+1mWn2L3OJWWNPjs3VT2wTXVY8PTp9JOnh+IdVp6V+zzjHfQx'
        b'b+3Myiey65y/D/ea8bTn1Gf3ovuUi5b+NNdjk5HIdSdjRUR4g7XnBrmgj86s5sIzgaI1l95z0PqlYt1y62vd1D+WB1oWf2LdBrdMO7fslvdPL2rXUdN6VJ4G5HJdyctV'
        b'7Ryw1cwikImWghYGPJ7jDw/CM+RtdKAUA5SBdrz2oRURljLRU7uIYuNII8ecwAHaTuUM2AMPmfkGSKPrixlZenPmgBbyatY41J2O3oeWu0OjdqljZhfwrF88KLMErebR'
        b'OT6S/4e594CL8kr3x98p9CaC0nsdhhnKSO/SOwKCgBSVIjZEEHvvYkGxDDYGURlsDGIBK56TRNy0eUEzgzEb0zbZTcPExE12k/xPGRST7L3r3vzu/eeTD77zvqc/pz3n'
        b'fJ/vw2iXcZ1na9zP1cCbhmgG2OaTOaUO2+Kt5nqhFUDxRIwnmC5wFR5EETGSMU2MdguygkziqQ5s9Uny9iJMPDpMKdo/nJtmTvEu5+bB82Mxtq6wHXs2rJoOeqgPNPmC'
        b'5fhiGu4cVyzSZrRLuC658AKpAw8tYXtSM0XJ3gIBNyMf1f0ihpzukhAEgns1lL/gUdGMR+C9PuACufWuBOdg8ws0OFqTqC0mPOJLEXB7Vvq+4MIF1e9sUjHYTxoiBF4r'
        b'ok5crNJHL+S5cBMt9M7cKcJkcA7tNvhVHNgM2uBmN1OKbTgdA89iTMlY/y6MNTziDM7ya+HWORTvdRV24g1CGgc2lo8C5G45EThaQinYAjrrUDOnpKeK8PV6hiYVV7hf'
        b'Kwzug9sodvYilMXUwZ3JWBqpxhkieDGVy9gn8KFsFThZuIY6/WtxqccY1N169DvsBI2MUTwX9sHdoI+W+MKcYJRZhsg7fUxejn58cAJcgSe51gRTUQDOgovPIAYL4XHq'
        b'kAY0U391WWAXtqkVp6R7J6ejdRJ0McazecERGiAQ2ly1gja6waDICtgyD3tE0uFNJNL0ArvBegLF2ZGKkcSwUYfR1uOirijQ9HQ/cL6OoGJ4czngWNxKsGcy+eI8zWUU'
        b'TYixhJOSbeABU4pB6YtZNAqNw7i4WtgDjoHdqyhc034lQXilGKAhtIPHaMFDHHh1tS2N2YW2oIcMxKnE59BpDmgZB1oL4C4CjgUtdoW/cacGziwZ9aamWEzK5Q93RVKP'
        b'ZhixB05NgrsDCygC6ODKWcQPGlifPgr2Q41yhvQMkUkIBnhh92mo/3Ngy2qwC7aupB32mG4OrtBuIS5WDwfNDL2gA/SMp51yXSjYRFCiNkINZLYXtFFAzP6SfI3Dz0qw'
        b'Kx3DSK9yOWiLrnFmdxhe1ade57gGnAbQ6og2OXspTOimVhSW63Ns5XhwngcVItQAe9BsQjYmR8E+uIVYVGs8gIFD3CjQCratjiW4JbBXD275Napfg+nfDk6ivTk4S1om'
        b'zgH1vh6KzeXBSxznWXhYoFISQFuTYTL9SLZ82iuMGONyXjw8kPkEswhwUsEN0LikAV40qkUTJmgBTZptJObY8oG7ktJFAm0mJ17XePVMmmBHFNxeJ9RHe3oBh9FZxYWt'
        b'8PwkcBoeJ5JYJVxaJ1xEETU6Feijhz/sBk0UOnkADaDNqMrJGIKVKcTOPLW4aH6Bp/mmOUkai+3NPAOcNk0BnOYmgesRJvA6abQE2K4/Gh91UR3QCdsY4wxetDc4QlBK'
        b'GQXcuhQM5ufAK5wUeGqc4zI6EjaFgFPYl9YupC0RXBRYa0DGkKc96H3mTEsDikrWRfvJfdOI47d60/i6DA7cGKtBquf40wSPoklBSn2/cc05IXC7S00MRRvKUOKnyjGS'
        b'PxMVJRmNTTI9+CTBnRife0orCDaHk7yTwdnIugxBbbKXBmc3zo4H1oKmKYa5dMK75gnX1wk44CxWC4mHTXBF46gR7DIdX0dbiQc2ccBJm+VoQ9xNQVNXTMBGYYooVeSV'
        b'kc5BC5JJFW9GgOkTNzLC2jF8b0zRsE3/NgwZFZRogYvp4LBF2ROiDcnASb8xnQN3DAu0PtC+kRkYwEF66nntjFgBLVDjQqcxJLLgjB7cAK4WkGXFKw0eMMDfRnuxKbzK'
        b'C+UjdfMCvEy6VTmayrYLycKDFjRdeI0LO5KR3n1gDUWQbgTbUSu84P8L9i2ieC54xEJg87+LnfrXlzZYri+cRPze3Q0hTZsw9vDpRQ64I1oUWDVnMocxt5fOkgXcMxOo'
        b'rW1b3VvclU4RvXX9sUPWSXtiH42+Cu+d2e8yZJ3QFDs80UrqIq1vXtDEUzs4N/H3GartHFvzW/Jbi1uK5ZIhOx8Fh7XzV9kFs3bBvWZDdhG9M1m7GBRQH7utKWwppNgm'
        b'FJC8M7NQmYlYM5HSLEAdGIqxFarAZDYweUAwFJir9M9tirtnLn7kGKZ2DFE7xj7W4VuNb9Ia0WecPTps2mxO2e1JboqVmqud3fekooeJDy3spXWy2PsWnmoHF4zbUDlM'
        b'Yh0mKXLuOYSoBd7SuCMpD+3dZLNQSe19pLyHTp5yM3nlkFOAVHvY0m7EhHH2QcPSxk3pFjpkHaY0D1Nb2bZat1g3aWugWiqXSazLpCb+vXGOajehPKatoGN623SVWyDr'
        b'FojfOqtdveR+bckq11DWNVTlGsW6Rg26FvYHDjjdDlHFTmVjp6piC9nYQhzYadhRJK/sWtC5QCWOwQAtx8mEcM/OBeMhVHZ+rJ3foF2hIq83prugd+VAJRuVywZMVQUU'
        b'sgGFtEldZDEtBa0lLSX0BlhlJ2HtJLT1UczehH6/vuRbGX0ZqvB0NjxdFZ7Nhmerwqey4VNV4YVsOE3F1lnm15LcmtGSobL1YW19VLahrG2oyjaStY1U2caytrGDtgv7'
        b'GwZm3F52Z/Xt1arEQjaxUJVYwSZWqBLnsolzVYkL2cSFKC29F0rky9r5ji0RzuyRk4ec02bVYd9mr3KSsE4SlVMw64Q/GavtHdA/Bu/auTTFq20cW0NbQlsjWiKa4vCl'
        b'tl6LHoaKDVqGyV27BJ2CLu9Ob5VXGOsV1s+/o39bf9AihRAZTBuyL1BaFqid3DusT1hLtYZt7KWLW1e3rB6yEStMh2z8HzqLlT6zh5yrlbbVI1qMs/eINjPB6mDq3tQ2'
        b'iWxxx/K25e1RrLn/gVTUG+xdR8YxTh5YKMPOPgptRW23Hr3KVvkmsr6JKt801jdtoHzIOQeFMSHiVGR3zlGJo1hxlEqcwIoTVOJUVpw6kDvkmI3TeWTjJHNqCWmNOBLR'
        b'FIvvthv2NFCWB5WFF2vhpbLwYS18lJLkQYvkYZFEEYshVVfSutP6Xe543PYYcL/tMyTKlvLvWXqpbexx+6hsRKyNCJM0BKltHVW24kFbscKZtZ1031aMR8GaQ2uGxWG9'
        b'sbcS+hJupfalUmTWYHiJMiuHIiFUWQVsVoEqq4TNKlGWlQ+JK9BAyaQDwlYwMp7xEuNx6P6xjUtbnHyigttp3WXfaT/kGvyOTch/UQtF1KDF5GExGn5X8rvzMVagX3In'
        b'6HbQQODtqCFxDq6E8F9UwmfQ1kfhz9oG3Lf1wZVYdWjVsHdIr8st9z53DCZRhaawoSmDodMHZr1debfy7eq71W8vuLtAWTJzyHsWKn26pvShqPRCH1x6D7Ud7l76w2ZW'
        b'GrZwlYWQtRDKU+5ZBD2091B6pg/ZZygtM4YtnGTuctd7Fj5qJ48Ouza7docW7WE7D7m2wlxRoTC8ZxehdvaUWUq133Vwk/KG7b00swmaEFuXtixVOfizDv6K0HsOke85'
        b'CwfM37Z63UqZm6/KnT6YO13pXTzkXKK0LVEHBEv5BNgp6Yhsixy09H+sxzi6ozKbW49hzTClUIbDmIX+CP/fBzX8N8sIXiaeE2j8u4tHsi6KGoW+/2Mt8zRzMofDcXjK'
        b'oD8Y/+DwEviHOnzc2Krtw3QZhPL+I+bNjf8d8+aLFRil3TyHMh5Du+k3ei1K7hW9HSuqxI5e+MpD7BsgGSUq/i0L53/OFXqC+7IlVuASn+KOltgGl1hzG+dYXf5C2f7j'
        b'YnVyHuiWzqLXti9Xuh5cuu5n7elESPUIk1ylI0kQU0P+j8tYicoo4DwwKn12fVla/ZIFvYwLyn/WjO4xjosXVNcurvgdrsk/okVRaQ1LR6+zXrqwfbiwxs8K64Vbta4e'
        b'NSu5Knt2S/ZHFZiMJb2X7pnXXxxL4pwaTPi9oLKGcIA6zphZs7j+Bf7w/3lJZ+OStjEvW9JbL5bUJvdF5us/pgHlL10sgIt1+lmxrJ8Xa3Jy7B/TDxede+lSvfpCYy3q'
        b'Yv7D+Y40ihPnZbMfwNk7c0YbxTP3d9jSR/lz/5D+hIaqPqEELcUEnS9X2NfxeojXsrWMNLe19FDpmA5GeD/pZPiHdDABnqRJOetrXq6Ub704SVtp2GT/oLI9m5xnzpiH'
        b'0Q2lNQsrFrxcAdkXJ+dgXECcCr2MnzcW+/NrouI/rG2Nn5V/1ryauoqXq8A9XIG3mBcqgJP5H1Xgf89zUNWvPQc9a7tngAZeRnXRw1YtcvxwJCz+uQMgvmRhJWPfyYTd'
        b'537yLZpyKFP+FbgJyp8fPoIz08n5I9gGusG533H944K528x/teecV7FAc16Bw2C3P/MSOIyl7cEVe1Yoxzm/pKOff52FCo/iAIY6+ZmbwPkPvPz8Hwmu8teCY34jOH5G'
        b'bnXR3+N4xJGgzDSMSG7vHgmP0bfef5xrNXuYNuFvZdLA+R09YGZNzTyNUPQ1QllEhPKS0vgvEn8wVhy1/3NxYNAY7rbfLmdGQWNIIHwNaEx3K0dDhE9hY8xWEw1kjItE'
        b'9YzyfhVP7wVBjIWPIaFwV/M0ovrV238tKoxcl7wgKgfKQLwGjZ0zFKngAY4RsIIrOBJA4Dq5PMwyO9uSG13mva7GmqJ7ZsEtoLnOeJEeR1+Mgh/niA3BFoLoKLbAiI6s'
        b'ZQYouJpjyRAqXbgdnidm5juE4AJUULZRTOy7IxU9ZGC63+ysbFEelymJ1gFt4NYiAvpJgwpwKzUFQxHArue3YFrgFmxnvGZpgTM+/hQucQMN/14KwoCXizEOo6wI7l9M'
        b'eG32wVPpz0zpNXb0u1HK+ytAI8EewcMGUfgeJxU26oDD4BTDF3HAuRLYQqo6HnbBPYRjLwcoGMKxl1RP4vlE2AlTRHDvGnwojU/oTap4FWAHkOaSQk2wAe3k+FeUzGf0'
        b'dLiwfTrYVRRDyeEOgbWgjxjDp4BNDJ/PAa0hqSTaypx5+DpTINJm9EK44DLsACfBJlMSzRNVs5vS61j5M4RcxwxeJtGmAumsSglsFGWQazvtYu4EeA0eWYxvEm0aTFPh'
        b'rmTsIiUNNpL2Jryp8PAsRhihBXeucH2h+xqMdt963H31X+i+L3beUd8Nf2zH/c3iYPCbjivKIJ3zxySCH3L0DV5sWB01k3ZOHmwbT9lkeKuyCZsMPJxAvdCdBD3gNLW5'
        b'51mAq8TmHm5bQMRZDk+kCvPASXrJMCpPJ3iCEACmgG3JmnvHYHhkLmelxRraPdDycr6OEIo0QQVXl2OXAqQkBuiNyUklF3jx/pjjYwE4QIE/h7VWjnKb8OBO2ELITfSX'
        b'04+7S8CmUdoaPtwPT2LimgUxBOxlCVvA6TG8NXFwM4N5axxgIwHpURLJG6AV7sopxhOmE+ME1kUItEhs2G0JpWNiw2O5JDbcX0wb52o0vhmkJDJ8sM4Ic8iEgh0EdITv'
        b'9g8LYeOkF9lreDPhxWAauwVch0cJLY4xvCDSsOIkpy/G12QGFeCWEGUrFsBO2OuVLhaIUtI5jDPYpBUCD/IJpgj2gc1QPkpEYwjlDOGhWQn6SPpzwVlzSmUAjhI2Dm1d'
        b'rkUYalJ8QTUBtlsJf4ezAewF5ykhAjgKDlHWzxsOiwhtRhq5Y8ZTD9hO716mMe75WnPhdrBxsR8KaQr3V2EExH9BCZGBBHQcrNOBTeAS2E9H9kbYnjEKB4O7YB+aigwp'
        b'TSM4wYcdozMRPAQuj85G+y3cyXw3CZw0+J3pjvGCG2Annu5qNPCwHHg0d3TGYvgTOXi+gjsowWgOuA5klHOED7bGYM4RcAKcJp01ytpaw7LB54GbhGXjeDTp/IvBTiCn'
        b's0cGIR4gE8h2ICPxymz0NKReaHpdiqcdI7iXdHIrJDLY6LUIxeAEM3BXJbhJYkAZPAekwnQRGmn85TNmoFnTQUx7eBs4lou6WZLIu7Y6HRO2HeCuFIKrBH9YCfpgB6Wj'
        b'iIe3njFSaOgoTEo0YwQenPaMFgZunsJgWpiFoWSuC4p1/925jhH6wD481znnCbikoXTDULs0wgsNfNQRL3NQh4MdeWAngQemhUypw/jFbm3McISGtiE8RhCwEblgP2yG'
        b'Z8rRB2/G27eBLHq39fUZFE13rUF52qFlrpSh1CuHwGIZ35Xz07a65NGX00y0yIQl811jODPPgb6cWG3IoIp5+s5blJZbmU1f/iNcl0G7GN/o7DneZ8tWvLjB4I1OiPhW'
        b'MxXNn1jbKEbbo1WclZylnDouhylnDnAOcjjMDkM+mjDP8ciGAOnHZL/EfcAV+z7gNNThWcKRahsP9MKrKhZULF24KHJ5+K/PYusrFpWWIuUDnxXURYrJbwJafv7uWewK'
        b'PbSbwkP6M7xZU8aVsdNKlTm5/VNAwYArLEC/fiBbs/XjxnMIn+8KcBXTA0EM+2gWoellB+gKQYtjypQsUV7S70gT9HD1OfjC+rRhGVTAg0TyaLC3w1toRRaIUMfVQEga'
        b's8FVHcZ2Kh8zDmVXL4tex6trQK33JPLq/fyiuWYx5seG33s4NOnNc+mHXlPPnXfS3NRU72RK1hTTPc6FZ7fb2YTuiZzXn9qy7Fu3cSd8HkQ9KnoStbxScnjwq2TpxZvS'
        b'LV989cbTVZ+GVb39hmvU+N16bh4ncuY3ffTZV85Oe+tTjuzt7+jo2tvgtePynI29TpXJjcODkfWP3l3vUTRugVbfoOm+kPjeuR6cD/imC1KDwcw2l978YHvjmUvNrRp1'
        b'7txUfq/tpr08udwQOvmVJ20MrQufcOSx10e6RdEBJ7SGT22wXDjRPvh1R9O6SnH9KYvGKb6NnBpxdr7ql7/9tPZz+dcPhlpjlrrNuhW//HT5AFenW2L8p5gdho2+XZaf'
        b'v7q/pHlAV3E6Jm7DF9zohPj6pIkT3bxvW6yv+/nBgqGvrm8dcXMNPT089A++23vpW6adyMkST738aOGwb5dvV4tTwd6utn9+XrnyFrd/msPu7pofWnadPpZgZvpDBGtQ'
        b'vWTfyR+L+903BXz2/euLZ7UcU0m+vvuk5dgreUPa/g19+4MD5Gt/2i0sK5Vxrd42+iBo3Gvp5V9M/JvjX7+8NnBkxzZpkZmf99WizQH+O9/eZvn66bTlP/7zi9xdk4+9'
        b'f+T7FTbbJljUrtZ5vCNfFLe/5M9FrQvvX/3O7wetN32W/jP4/Ukf8WYVSi7vsJIcqq1J2x3/Zbf8h51+P7i96VP986pZd3oOPVZKp7yzI/G1HSE//eWY446OSq+m6v3G'
        b'Q0srvzhx/Gi4yVt/istxOr90K//9hEmljrN83pz5+omkq9+mvF/0k3rbfttL+a3Hpsde/5J/59HKTXWxGTt2hK7rC6gbfG/hvsOqWJeOhISMYrH/F2n5K1etqRz5WXfN'
        b'htkuq5w9Xv3YMkJdOn/qjQenF6+a+vade6u0Cr9+46L6fub27k96frBf3/L0273VAw15J36quqxcX6w6alZ99oJ3baFgX+K1/vLGkocmMTdLa5boZKXanw7hftef+MOh'
        b'FQeunnmaeODed0caK76OumNdntgbZXle2PHG0x8bktJ+CFvpOGvC56vWXPz664cPv5dNbL9wPUz+qnz7Od6c+LZpk6uv9Pz8bVJe3nf+Z1ZtWB7Afe+rp8MfzOl4oyhm'
        b'QsOb1z//54LPh3+qqkmM//m9P+0YGNm99S9LrwWcn9Fb9Lr3iIlRd8ie+UXOnybE5X38vWigbupTkNbRm2ni+G3pk7D9y2Lifv7y0cFtA7+c8Ni396PZS151Kr3r8A/J'
        b'zoBfuF9MCDi4NEwQomHAccWTtA+Q443GzoloQbk+HW6mNJRrS+A+A6Qw3IgSJOt5IvUAbYRNQQcPHJlfRPA0pmijsdfAC1PS7QCnZqfyGF0bbh6QWRA2MmvzYthTCeRp'
        b'z/jmNk8m4CbPZO4zfJgF2I7p5jjwIvnkAQ9GPYPxgaYqDtwMb1lpsEFABm89R4+dgGsJs1q2HwEqSbioMKN7uSXgGtnKaYGjlHXt2px8gxlo7d4uSK5N8xFoM0YonDsz'
        b'l8D7YDu4HPIr/Bjcu/AZ2VwkWEdBKDdBXyAFkIHDJG8G7rafT4FgzeAA2E4wZC6poxAy0APbKCIObEgwIDw/cC+4ys3lRGbDVvJlRiqQwp6i+ZiSjSDEMF8jRYi1VYEN'
        b'z8gP9XwZyn0YBRpJS7nDA7UaJkFeKYaVot2FlS4VXLc3uDyGKRBpfGcZwhUIb6wiNfFLtMU7wO1o3m71ZhhtcJYrCYc7aE2a3GEfJSeFGwpSNdykBlBGvkbN08Lkh7DH'
        b'E0nmGfvhIo0zCnAD6TmozLWwue4ZbSK8NYPSh20D+7VQK2/H6wHeEm1zDOGgPXszaCORJySAzZSuMSkWJ03YGg+C7RT/d34q3FgHtycnwysRoC2Vy+jUcr3S1tBe3AV2'
        b'LqOceMK0NA0n3qE5NNcev1iMpKolCDWk+p5n9PO5SOHoriPNHAwugHMGoHMhxuT3iXChD3GQonlEj7JLXfCDZykSqxS1vznHBSjiaTtdBFJwxSAlXajN8MAleAxc5YA9'
        b'cF8NZeO66QavYC1FT5wq1k9JdyzhMZbgEj8ocD7BHPmZF2mYrShhHtqNbyaEWzt5sHk5oHSAAeDi8jq08XzGaycpfMZsB6WrNZS5cBM4P8oJBy+BljQNJ1wlXE8KWhUF'
        b'pRQ2C9vcRnGzKIFbFDcnRXvcwwbp+b+mk+XC63HwCoWsXkU6x8Ex9HxceJGh9HxW8CgZ7BHwjJ/BYiM9NDLnuztxYpASoqHobDYCuzHhIbxoBo8juWnFc+BONJBINGfn'
        b'1ZTODPXhTYTObFYiFek6tC1fVwdugE0Zozyui8BZ+q0DVfMakrcA7Zs1NIVwQyGdJS4uWj1KggavpqRqSNAOQYptXuYXQSnQeOBEOWVAuwR3UhTYRbB2MiFfpPRn8Miy'
        b'5wxo7Wh+IprkfrC/0ABvvw1cMU8Z2FtFCRbbQc+yX1GVuYGjSOaYqqwADR5c26ng1iIDkVhQmK1hKlsIemkjna8CB7ExE+qH/ApUYZ1UrhPSaCjiLqMeCZlSp/FyQTOh'
        b'TkuEl+mIa040pbByBhwfRZXHAjmtUivYgaG73hlo8oa7vTlo0uxjDNB4RlNCF7ikQWVvKydBdgjg1iQ+muRaUZDzXNheivLAxZ6NtDfMlcoweVFc0MbJ4gPKNhuF9K89'
        b'wkxvNKSxCqSjg1013eQirWUu9VoDj8BrBl5wF49pAHJuOmeSK9Cgj0+K4Z46eBr2jQEgE/Rxiph0y1yDql9h7XfN0EDtwWZwXeD0f4/G+3eQFk7Mb1nQfoPco3t+/ec7'
        b'+eWCf3vTTw5ji1HD/51s8Z/EJXEY7wCZjtrNG0PT2ktkXLWLh9z/eKhaJJElqL392+IfaZ5k8WovP4qikuk8cnGTzTkeqci/UnKhRC30VwT2JnRHscJYlTCBFSaohKms'
        b'MFUlzGKFWYPClcrcIuX0mcqKuez0uWzuPFVuDZtbo8qtZ3PrVblL2NwlqtyVbO5KWZzaQyiv71rWuWzQI1gdHNHboNCSa6u9JSrvcNY7vDevv6KvhPVOU3nns975Ku8i'
        b'1rtI5V3Gepd9wzCiIq6yfK6qvJ4tr1cuXjHCMGs4cdzHDNNA/6ngxHOf4n+y6K8s+iuP/sqjv4roryKujCsLaNNTiyYp8noru0tZUbxKlMSKklSidFaUrhJls6LsQdFq'
        b'ZV6xsqRcWTWfLZnP5i1Q5dWyebWqvAY2r0GVt4zNW6bKW83mrUapBbbpk9Q6S0e5k2JZUSxNdFA0ayBRmVt4N1OVVsKmlajSZrFpszSRvPwU7p0+Kq8Y1isGSco3iHKk'
        b'xLC+MShESJuR2ssbvfeWdGWezURN6OmNWaxOmyiyVR6RrEfkfY9otadPl3GnsaL+yrLuZfc9Y0a0GFH4Y23GL1jtLZYv60xXC3y77DrtVIIwVhCGitlV3FmsEkWxoii1'
        b'UNwV3BmsSUHlGcZ6hg16xvQu+u2bES1egPu3DM/b46k24ylqW9y+5BsdnnfQiDYjCRoxZPxDntgY+znTQo/YM0GRvVUD2mxkBhuYqQrMYQNzVIF5bGCeKrCIDSxCEg2K'
        b'4SpLK5VVC5S1S9iqJWzpUlXpCrZ0BZJUGScGSwr/g9KLYh0l6sAIJKgaVWASG5ikCswkieaygbmqwHw2MF8VOJ0NnD4aNhz7Iqq4ncmG56rCp7Hh01ThRWx4kSq8jA3H'
        b'fSkiHvcl5bw6ZcMKdt4KtnylqnwNW77mKe1Gmt4k4ypdglnHkEeo9Rw6HVSCSFYQqRJMZgWTBwVT+qvuzL09V6Y97CKQV3bNPT13WBLSS/Bo/Q0DlbdXD0nylAXFrKRY'
        b'Nlm2tC3tkYcYU7PJ+OqgMMrVpApKY4PSBoPKlVnZypxZbFY5zlDCOk5CEqLSUYniWFHcoCh7gDsQeFd/tJv5dZXibhbDimKevyKsXZjqTPNK7N81p3NOV01nzaA4rX98'
        b'f+JtG/QlqM0AB34m/0FRer9/f+XtUE2sUSq3cFYYjl5NatPFwQs6C7pKOks0YXwkXcs7l3et6VyDXgS3GT4KCMd4viul3aWqgGQ2IHkwoHwgn/LllbLppar0cjYdVU4W'
        b'yTr6465o32kv01b7+tOugiYgWng6YBJZUaJKlMaK0mT6wy4itau7bFlbuso1mHUN7rVWhSSzIclDIan3XNPUPgGUNSvhnk+CLPHFkBa3bPtsVSGpbEjqUEj6fdeMER7j'
        b'm4g9WYsndU0/Ox1Ndy+En4B51Z6lft81DYUXh37gG6CY2WvVPX/IN05TWlp+lSCCFUSgWgRF4EF3ZXX36sGg4oHxyrTpbHLxM0G6uCndA4dcgnrHoC2VWcWD4cUj4xgf'
        b'P6VfDCuerBInseKkAbMhcbos8QMvkbzqjHev6aBX6Oi4XnTPM/QxjxGK6Zchr1DUm+S1bctVHiGsR8g9j7B+nQHObX1VdDYbnX0vOhfVcjInmTNgett6IF85Ne9uodIz'
        b'Uq6j4HTqKxJ7Y7pThlFaS86E9/oNCsPVktArYd1hPRHyOPSoksSzkniVJGVQkqKOiFFwFYHd+h94eMmD2lcqatG83ZfTb4ETvlaqzJoyGDEFzVi9nG59le9k1nfyPd+4'
        b'AQvllOy71qrkIja56F5ysdovuNe027p30aBfTH/+wJTbhar4fDY+/158wXBUHEtOoYbiyoaiyuRcpRBNNeGPPMW42sqgIty6z7nNNI37hMcRlGJBCv27xJ1iNDd6+XUJ'
        b'O4X4h8orgvWKGPTK77e4Y3PbRhWTzcZkq2Ly2Zh8Ek7lFcp6haq8olivKJnOsItXZ5U6JLrfQxmcgobpKtY14APPIGVwEuuZOTAZ/ZFpPfINkmmdMFK7C08YPC7loeX0'
        b'B8KWtCFJq8yHM6CXbY3+eeCaYID+0Tg3e6BXv7S8on5G9by6Bzql9Utnzqir+J9gNTVuzsbuEujNaYoWw7zE7oCHz/9CUcQf1zJPY5M4HI4jdnjm+BJXqt8St1HaQuaM'
        b'QSBPwCPHvq7wBOiAe8DW1BTv5+4fMoTk4BieNuekakwQn9kfWcPDXNCOibJdyQkhvJIfjPZ3u9GmFBNdbxeB7ZmatBzC+HAf2lBrzobRRvzcfLjH5IWsqhwJXxLSXW7G'
        b'/TYvICsmecXCm8Ty3syvRojVp/ap4JxnUro4OX3KQmx3MiVJw9rNYcom6LqCRnNyOxMAtoDrxOy6a47GsJsa8h/2JPcW9ZMqU+FOEVLnc0kyfgFTkjSFC3XVhjfhAcbR'
        b'hrhR5YaBNuwUwhv0xIiJKWY+zdhzzJXCdHBI1wTcDCFG326rakebxQRTpb/YKp7gAL3EXY9U+7Y6khRYy3ue2lSNi1Ncr51Ida9cowuOw8NwN+mn1U87Wrl1cTyGKbk8'
        b'7kb+e3OHssxvBaVfvZgepVo8N/9K6Cs7nZydvfw3m/B0zBz48eXt61XHlyi3lKfZecicpSl7bnwW/f1n744U/HPWP0vDk+t69j3sPWPzVZvVpw/f/3pl68OV4lXy+eNS'
        b'jAfKjjV//L718NsLQjb28nVV2U8yszJ1JA+T/rYbdJzhfDJ84tjhZKv2d1M3qq1OrTr7Xf4v3IN6taEfTmzQ3/Mw61M1rEusf/JL2PbgVKOn20OnpkR/VLGttOC2rvXr'
        b'5x/luGwIXZR/r/cTj+E4szW7wSHDOSsS+mvO7xh3STISZvFtmMU375y0tXYzbG1oPnVkzzvCr1UGfQYzMt5yurwp1On2W57fFDjbDBQY/jT/pzCH1+63VdvODzAOMntl'
        b'f8j3RgVG1kvVtssK9SOONvs27IuYr5xkXJBYfda2sLjJUZz0oTLmU4v9N5K/7kw52+G1ziS0NPujxUa+X/hb9nYeaH5Q9v0ZQd4ZcPrtdQfOrNn68964hgLnz+XLdr4z'
        b'py1Ar+fwd9+t9giOcpr7y1rvW4v0ixY9uf8LWJre8th8eEflN+a2EcX3Xjn85G9/3qcaOXWjoOvLN1cEdA293nP36amwPYN2qmZ/1StWNTMc3s/ddfvEzzcPa+U8qbjX'
        b'GvLFV0XJO4pvf5uufLVvYePH0ps3NstXrolQHl4Z/yE8HXfq71/pBTV2Lo/c7mKy7B87o6rTx0998+Mrbt7bhxzSRV/tNAuZELRfHSO9FiJlejpuRA8H/bjt6qbHP0a3'
        b'rSiRZUkCpF9NqYwx1j+7WqrnN1Fatrj9/F/ft/m0v/CHsNM36j6VChQpd+Y2Tj0aei/hyJTIcz87SzNS1RmJMov6Nxonf+F+L/jmu2Wt51IvXNyzr7t63YOOtyRHGq/d'
        b'lbSHMZ8tMN1+esJ7Hd97/UX5N7G+3l+G/pYwu/xq12snFvR0tG367Mu2XXBeRFrKkm0/pZ6fUvX9imHRDI99f28/ceBSfOL5Pee6ll6wfZJbkPvKtvwl7g11om/vJAd2'
        b'mMpSu3e98uUMn1eDD3nU+r73NPgTu5W84c9GONNW5oxfFSQwe1/H0u4vc82+Tlrw6rnJ3527XZg17GZsN5E10bPhF0Uv0FvfaS/+/O8VQ1fqxzfWBE5s/W6Tfdb2Ul/Y'
        b'cfWXa2eaVR+v+IvbmxG/GE183fDv87MFvk+wb2VzM+NfmbERG7YacO5XJo6w0Yae6zXCdnBGY1MJby0iZpXgvBu4Tg83NprAds2RbJ0jQRZc9wTUw0cOPFpLTPosDMYY'
        b'9U3hptAjsj1QCs7S01NL0E3soDdbIIWbHFCc4lZq7D3BzTm/8UVbv4qeWm0LsR9zaMVjLA24+NBKD1wlxx/wJGwpIn54oyyxG958cI2+PwTW2dJTsvx8fEjmWUQMc0XV'
        b'0+mhCLjkDrtxjeFFounbwf18cBEcn0HOl+zgEXDIwEtI/fKAreA0qpmBGZe49zhDK7cNbp0MD43H5uO1Ag6jtYSDIl0Kpacy+0pi6gQcYsVoORn0FQHNEeqmJbC7jhw4'
        b'7s5Y4u6Mgugv4YIzC+o1TiHswX5q5hhcRQwdl8NDmhRv2JgbiJHk5sIubj4nDCoC6Pv1FovrNAdSpUFADveU01PGi6vhaSzT8opRY1hqCnvVkh7hVIJO4lOJme3LEL86'
        b'64EUbCenNO5Apke8MR0F3b8+gQPn4UZ62njdUIcDm+g53rNDvD54lhynBGjZjpovwmPaY+noy6xI86UWG2iOl+jhElwLFE5zYCc5pvEEx+BBg1ADjY0qPk4roVwB9mAT'
        b'UNRht+ZwJw82gYPYMwsHrU/NUOP5Zy08NhUfne8EnXx4GWxDAS5yQAvc5kUOl/hgI2gxEKcvgo1OoB2HqkcFMDXnzZkGOumBndQMtuLzV9poukbcQnCuHKzTHBTNxb4F'
        b'Rn1JBYIeT22GOpMqgwefYBqgysU6Y+gPRrkPrHV+zX5gBM+T/MLmgi2j58HwxhSUJTkOhqfF9HwbbAZHeKBVcyI8ehy8cgE5CbNZ5UAOfEONUD3Jce9+Z9KVhFwduE6Q'
        b'OroFwZ7AwIEZRLwie3hgzFEWuAGPw+1czVkWlE2h/WcD2IoatTEVD17QA68z/EwOatwLoJXIr1IMzlP7V3jMSuPGGRyG5yjgcj9oAzs1zAuT4MYxntWiQRtlJtjrCjeM'
        b'MfYn/h04jCW4WVHBd441J5l4rrTAtrt0w6EbzAWdoGsmaPQnFuMmaCuzl37Whbde2HA5WPJR57+A5gIssfHLUE3pcXMjvATXwbWoL+qncUHTPAdy3ZKJ/VWhlDALDtg2'
        b'Fl0BOsJ8C7XNRJwnnnhbnQYUvze1jjEPHl+f4eJLOpq58wS6cQKXHLyT0cYJ7NZhjAt5fqAZTazkUroF7k1M/U2mEUDGeMGtWqjbalH7+kNiPk4qE26GW+A2QqqB0+Lx'
        b'nIAMXCLDeYUXPBiLTz0xS4aGIwOsnfP/9FRS9//1qeSv2GCpwuHI/T17MKJwkKPHFqSQ/ECOHkeWJnAYe+fW4qPFTfHEAPOktVRL7eSJufvb7aXa2KgzqiVKZePD2vgo'
        b'AgdtQpCy3BKntnN+bu+qyBu0C1O7uLbEfYwNNRMH3N72ueujSilh0f8+JUPOpUrb0keSYEq5r5Iks5LkQUn1QN7bhUjjnTZ7KL1aqq108GEtfYeFfgq3K4JuwRVxt7jf'
        b'7Y7gtmAggZ2cMyTMVeYXscIiqbZ0KWvpqRaI6SmZShDNCqIHBXn9CXdSbqcMNAzF5aEwDS3GarEEE+gPimN76wdFVahQorsiVcp0NmW6sqySTalEwZazll7DQnyqYNNn'
        b'c8u+z14VksaGYOtQYc5oTs4eHaI2kcrZn3X2VzkHsc5Bg87ZvQG3IvoiVGHpbFi6KiybDcuW6gwLAhVL+vlDgvhBQcHARGXWNDa5QFMWoW9XSGfI8zObQWFGv9Ydvdt6'
        b'd4xvG2tyeuTo1mHcZkzZypEQBGJ6ghHOCsIHBdn92thmdiBwKDpbkygKT9jNfVlHX6nWsIOrXEthfsWh22HQM1rt6oU9TMiXDLkGSePVXj4ozpIWEySFK5HdkSpJEitJ'
        b'UkkyWEmGSjKFlUxRSfJYSd6oGB6hnoA6ABK/Az4ZGXQI6kt45OiOs3teRDV9QfOnr1SOwaxj8K8+hLKOoSrHKNYxCn8wbDPsMGkzoW49Bh1Te7Uwz/wt4z5jVXAqG5w6'
        b'oqcVbC9NwAcztpOeGi/kWHl/x+C/I+U8xs2rI6MtQ+UawrqGSPWG3QVyty5Rp0jlFc56hQ96Zdzm9SdD4yH3TKnBIxsHlU3AoE3AsIdQHt++YtAjXjG3P6a7piXpsTbj'
        b'6S1PpvzZKu9Y1jtW5Z3IeieqvNNY77RB75lKbFpbzGYVq7JmslkzhzxmSZM+sHF5JJ6kyMcHdYX9Vnfsb9urYqayMVNVMYVsTKE0QRbUkqkWSRQJnSWDoqLeZbdW961W'
        b'ReWxUXmqqCI2qgiFCGzJGHbxkocqlrEuqf0J6I80bljgLS84Y4/t3IddUaP6jvC4bhHq4PABoVrk91gL/XgUEEb+lcaP6DKiQGn80fRhO0eZ1eESee2gne/Hrp6d1mpH'
        b'AYroFcsZ9gtQVPTYqL2DUBz0+1FYDH34luG6xXFa4lH1nYUfuEqUk+JGGI5bPudunHJK3uup6ujUxzz8W505lT6g/LQZkT/Oj47sIeckpW0S9sLi2rqsZZnKQcI6SBQp'
        b'9x2i0DsPb5V7EOseNOge3RsgTVQ7uLeualmlcvAbcvBT+0hkWicM1QHRMq17jv6PQqJvOfQ5qELS2ZD0gSVvr7q7SkO5HzwTBwhQu3h1RLRFqFwCWJeAXnN86Me6xKq9'
        b'xF1enV6K/CvF3cWqgEQW/e+VJItVi0Pls7rmdc5jxXG9effEcXLusI+/wv/skof+kcqonCH/XKV37og+4+uv8oke9InGXyVnlvY6nV75MHCyMrZoKHC60ne6WuSjEkWy'
        b'osjeWlYU0597p/R26aAoV+096VFY9K3IvkhVWCYblvlO2JTOVHmcwk3tM0m+qt9YmZ03GJ2nTky+s+L2CmVOPps4TaF1xbjbGE08vnEjWkx4Ngc1ukA84sT4xHOeuDM+'
        b'YcqwqUPiPKVn3iN7lyMG39QhmXg/5jH2wh8IQfrGAqNCPc7w+CD0lx5XjaMQ/TSt3+D0/9MFZdxvjqv+jfXjvVF7Ynw4tQRD/W2wPbENtie2eRnQ/3c4o3PY2Mxy0Rr8'
        b'vBb/WYf//Ij+PJhQitlTZ9XTM7FSTJVavaCKmDovWo//HMbWRy48FFRHYwj7wHCstekDgzHWnIvEOPRWHO8f+M82/MeYg1F7zwzJHuhobLUeGI41jHpg9IKZEbFKIcYQ'
        b'pJkEE/737iXxtv93yN9HpdbCR1J7gVQ6CAtrFSrq3zH3u6HRuBFbxk2gNHT60Mi8xa2NJ7XprOiO7TPvW3w7p3fu3QA2O5+dVqScMp0tmcmWV7Nz5itnLVAG1yhFC+8Z'
        b'1T7llnKMQp4y+C+ma1/EGSFvHsfxRunXEzH9ejJnaxzq7tbOw+NEanM/9MpasjUFvbFwGB7npTYPQm8sQrYmoje2rsPjfNTm4eiNbeTWNPTGxmV4nFhtHo3e2EzmbE1F'
        b'rzRpx+G0E2jamlc4bXMJeWNmMzzOXW3ui96Y+W+NfR4mBoeJpdEsHYfHCdXmkeiVZTRnK14IrJyGx3nTlKwkW5Ofl9IHl9JvbCkzcCmzOKSYdm7D43zpKzv0Kv2JLsfI'
        b'5Yk2x8j2qXYRz8j1KYP/jpC/z6ni4SG7ZeQA0Aleqx3LImoF5Xykg8JzL6BUn5HUYju4/TrEKgnTijMaMxi9Sp1nFkr8P8xCafbvmb28aKFUlbE4Az2D7bawReI7yT/Q'
        b'L0ACrgBFff0ieKy8oXZxHdIjFPAivAAvY3gL7DHRNdQ31jMyALvBVrAD7oX7c7LgHngwT4uB52GfgcGycRSEetRoOUGyNgp90H7+KtwtRGpsI48xg0d58Co4DuWL8VhY'
        b'ZibA+F0/Bmyb7BcPthNTFXAIZbsZRViig+LD3TywfhGK2IUiJlZSdtIdoMlDgurhz4Tr+IMLGhuXCrgfqW0oU+Mkoc+zeDjDPNhMcNp1q8ANCReDhsE1eFECboF1BHUP'
        b'TmmDQygrHC0GXuNxGHM3FC0Gnif5GYLt8JpEm2EmMeAkODypImYx1v1MUfy9OL/FYBuuKcpyPMqwEcUsRHXBMbXgrkoJ6gwBDFLM2gJCwTlyzO0Y5Ydy08VYcxKNy5ib'
        b'4XbZDdpIObXBMbhPgtaIQGy4cyhwDthEjRdk1oAwkrr5Cn00ETkoYgXooszEjflwowRNpkGMP+wMql1JbX86wfoqjTh0wBGwBbShhgF9KCI3nNIFn4I3wSUJ6qnBmMyr'
        b'NzgXnKTmCCeBFN4gwhPykCrmQvMD+2aQ/CxgVzboQQ8hjKAoBG4qo/ldgOfSSH63bHH1UIs4awQYG0bqZwRuwTbQgyQYilTSE6F+8DSt3xF72KERuS5oQjMzlZ82amPi'
        b'ZLUd7IKNGDY9mdC0TbaA6ylB8Kk5qBs0kv4CmmbzXDRySEffSY/ZCjbwMcw7lgEXjWLhJnqZUuQGpELSOXkcAWgLp2LITySVqxLBFrSgM3HMCng1TghPEqH7gk0Y7Ih9'
        b'MZfQDq4zU9OY4CxDpXAM9qRig754Jhpsig8qJk1pCQ8loYymwxOaaONpW/INlhs7pujUIWknMLrTE0pnkUlmIjyOebFIjYQlUEHakQ4h3JCwOZ+MIHu4t7YOCTyRqUIq'
        b'tnY0pXhuR/XtJIU8Di6ixsQMxOA6FnoHiusUQU1kdlqCPXVI5kkM7JqUtAxeIxXUKwQtWODHUCONxgzX5FroT2O2g805EMs9mSlITganVxP7lhQ9NABxpt3gKO0yuGmI'
        b'AOFh0EokOBOcw0cUSIIpDDgBmlIK4W5S3+BK0E37KIo3Axzz8RmdMRpJ08K9tAdcg9vSYQ8X4/2BAm5KDQByalbSAS5PJ11nA1wPj8ILizRR4Q19Wuiz/vAs7EECTWMc'
        b'ndKgwo1U18AnhWR6cintdyQiESf2W0vyDCoHfbAHyTMdWzdtSwf74SmSZxlcB2S4phdNRiOHU6GmiUg/h8cFqJA9SLQZDLyilWENzpCWAm1C2lROsZpReXxUOEABbpG4'
        b'oWjkn4M9SLaZzGxwILMOjRHcj8ocwB4h7QzCshodJ41oAkAj7emHwMZA2IPEmsXMnZ0FNnjQGa6jpoJmNTkJdj8bWODUksUm6LOPI7iFzcumMDNnT6nVI8N4Cti5inQ5'
        b'sA5eEKP2IC2zH8XygFtpk96El40MkCyzMWbwVrb5VNIsk/3gOtIeKJ4QzfUXwjW5lSNZ43ixoA1cMeBiK3B4EG7IyZKQblsG1jlrejxsrAc9mslxtAtc8SGRizzhLgMk'
        b'xVyc583cOHiW9B+wO3ZMBwIXwUU6nfM00rSZSMZmKpSuMUCinMrUwl1TweEGctEZORGspUtG01KwYRGVYaoFiZEOj+YZIAnmMc6wNw+s45AJxxtstNCUzxNuAetGVyh4'
        b'rZRK/ig4ZmiAhJfPTIAb88E1DU12OVCkkKl7ggUP7beCcJTLOVRym8ABuNYASW4aMxdcmxZK73RN4Ok4XKMt2EALS+M4GclUfHvhQVLIMNDBBY3ooYApCC8IQf0TvwWd'
        b'jiLQiORTyMT7F4aA0+Sta0oEaESNX8Q0wMtFZbCDFDgnBGyBzaieYnzte0u8DOwkE4yXhTdsRvXwYRbCjT7VM+kM11frkcNgyzpwwNmpAW6m3WFHcjxsRikLGTQUFMKs'
        b'BBJ4BdxcmIOa3I1BK7wbODGTBj4KzyfBZlRbXyav3hfsziXFKMxBvaaZmBWBM3C/tzc8Q4PLF8CmHFQ8dwZuTHcHFxcJ9OluoQP0gG1Cn0nzn7VOOF29M8EOIiofeDMJ'
        b'NaBZrQ+d6TWLLWZ8JSmMs8WSFMJWzRCmzYu7nB08R7pHNVw3g67TsMnYkUPjOxmS2Cvg8QAUvRzsHZ2hZ9Lug+b502Q4RILGFViAxxbRORGuH51OVxbSxWsvOJNKtzpo'
        b'QjmURWqAkyhwIlMUaInQxgl0I3FrNlIzNSmA1kISxBoNsy4UZikaA7s143y0j1y0IDPAEn1KZo6++RrqxI6Oqk1gn4BD1/oj4ERCKtzmjYnle41FXEYXdHHBOs+ln5IN'
        b'ZNOiaIE+McoKm8lzVfLwU9m8fYFTqaVWQ5Bh2ldcXzTvlBmKtJ3oy3ALPUMjriPWUNO+cl1FX1rPGa+r4Cbh6LZHSlbQlz/7aOXO4qAeF102794KffqyQ8uEL+AFoz5S'
        b'lnYtfDx9uSpJZ6YeFy3fjmXenZEBGjuxOabhtkw0wywsSysw1tHYntkbTNvH80QiLvNuKZpBX76iPWH2CCcLZxS+PNSUvvxkKn/hNS7N3XBZMn2Zac+dl8ch1Uyzibdh'
        b'iK1tuvNEcyFvGs59+k8OVoyAm5tAPswo0yr/K48mEWVhREObVSENhkPKapizKo759FAL/u9uFMngHEe7/C5Da7J12XTmUwn579soMhQmgxNGeAVkahi0CeutAeeN6PiF'
        b'u6KFaNwsZczhnqVwSyy1esXdwBh2V+OO1G74664GpfA8yTM9wmJiPkPLvy9Ul9b0nYIJ0a9yaZtk1Ijoy689CrwVvDIOkl1hcNpiVNOMjOqQJB1+nRcq1MefZm7ad7eu'
        b'w9Em3vy1a0V7z715oHzZpMJ5wre4nPGXmzad5R++P25g5sIk84mr9vf3eumETK3N7co8su+Q18T87QaqI2+UvrJfOPWfBiuH2qfkJq09/ZegG9effqfqWvGk/HsLrfn3'
        b'l+hrd0bsnOT/sWHlXe9F5fZaF7aGLLJ3u7BDv2+tV5/u7rO3PT6f3ZR+ccDNu1k4u1lHkWL/SlvEm4uNP9Jd8fYHy77xLHEsfSX1Yz9bj9LXhB+fWbpzpZ3HQNDCveGb'
        b'hj62up587NWQb8LFTRa121YaHLx7pTvh/EdHI37K/aj4+panjzmRr2hHgju96zNH/tr1Q8eDOe3aZzZ8XxaS1XxrldmtJV5HMtPfMnnwj9AFEQtMHsRU+nOtKt9K2/VL'
        b'QwDb0DJ8d+u7R668diq4SPrhvL9frv4xylEw/XOJV+0sSe/N86snHa2b97bvh+NcFjz5NuXujvIfn1hd6t729od//nlhjbhqU0jP031vXg1vnn3+zFvjqxbtNfqL+09J'
        b'hZWvxhXu/bzn/ay3H86ecP7EhMiOq1/9M3ln+H2DrMuW5/o/lZU3q9WfqA8dtIzyKGhpNP/y+scr+uR3ej/wulz//sB10d3r5lcyhffnJlWrC/eBSV29j9+wkjR+oCco'
        b'm6v64lDCF2tD3stVHanyuX4k78jUrPSK17ONU35ZPTFXKPmm0tzq6PZ3C5Zd7PGZfrLZ7HRSgVfvJ155AsP7S+r//u2GP8lPtT9c4/nerrdCl38B5Os3lTecbTh2ptjp'
        b'/FHved8mfPm3Y6z+0eIbZje+jutZ0BqZ+dnrstBPyhP/dPlPy5f/cumXX6ZOe+XAdye8GpcY/fTTB5Nu/N373Jb0otenwB+zjf6ZbLfS7dLHZ7oDOmdIHkzJ3JKomPH5'
        b'F2u+rLee9+r2gM6nC1Lg/Y5DSxeG5H/WZvp+wJK/HP2y3bb4I3WQuEcQOjttWK/nxPCJO3t2X73X/cGF736CH6a+98k/clMe3lvxc67Jq5329b0TV0c16Kz8s/yce+a3'
        b'W/JUD3OKh2Zsmp+aqzz0Ydf+syPNejcmtX85m/9e5C9bvtj799vf7EtzS/3o/Xlvp+ad+nbC472Pr516fYXk5+n5H3xdvXr4g9ITevl2Pqfuu7xievm7rE9u/mRz5IJp'
        b'SHu/wOSJxjT83Fx895eepj0vU4vRWolNAja7kI8TkY7cDBsJlTDau19g+Ekc0JPmQe5F7XLB+lS4K24hmv1TRV4cxgAe5nHrQTMFLWzRC0XJ9sArdVpgpxHD0+f4gUZ7'
        b'esHbBW7gHeoucDZFax5EyZZzwHVwCVIibHge7U4bUzPh6QJRcrJ3Mp8xaOCirfrxhSTlSfAcuEGtkaZmjBojLSsk31YiXfU6StjHi6NVxPAXc+A2pDFIKYXyoUVo8hHP'
        b'qYc7tRgu6OHkaYMrFBRwaw7c9cwMCdyayfCxGVIMuEw9qCOdbit2oT6NkA9oMYbaXHijAJ6nHOVgl1cqMXbgoK3KeoZvwQHHI2EjuR1GSsUxeCM1E5yOwcTNDZwYZxd6'
        b'eb+hnFjV7khNhi0G4BxSroO5VvDMeHr3uwMe1R1LyI/Z+Hn2VaAzQuD6f2/D8B+cLuL74t+3enjR+EFj+FA3a8aC0ur5M6oqlo95JteLn/ApzUx9OoeZMJmzNX6EO87S'
        b'WD3ORpozwsNPziJ5HX2aFNVvRp4eka9a+Il8JU/kK34a0WZMbdF3HfrsIkYhNM8B0RwUiPzQpYH06DMJpHmmgcgPfRrIgD6TQJpnGoj8MKSBjOgzDvRY80wDkR/GNJAJ'
        b'fSYpaZ5pIPJjHA1kSp9JIM0zDUR+jKeBzOgzCaR5poHID3MaaAJ9JoE0zzQQ+TGRBrKgzySQ5pkGIj8sSaDHVvTZV9JvprZzlNe9+M83DuOwi87Hzhq6aezK/p6Zj3qi'
        b'zcE5e+bIzJprmnjq8RMOCvcIpbPkbvhepkk4ND5ga6za1gG7/t2WvjW+KVA9wfJg0Z6i5uKtCR+YmjflScv3FA+Zumyd/NDap0kbHxM7SBtkM1qWyrXlizr1WAc/hZ9i'
        b'Vq9zd6XKKqIpRm1t2xQ7bOcsCzg2XcpRW9oQ+tVAuZM8vtNDEdMpZF0C71sGjfAYe6+PhcFSE7Wjs1RL7eIh1R12cm+rk0valyqc2la+4zRJGqN2dpPNaHOXxn7gIFYL'
        b'xfJahWlnXWdwm+4joVimq3Zwls0+tEYR3Lt0UJKIL1exx+8pJ0xQUBTE0U02s11PPqXN+ITeiAXjHICazlXQaSoLluqqLR2xC/EjJmoXoTxWni2LQNk7OLdJZEvbIxT+'
        b'rEvAkEOglI+/xqE8ExRxigClSwgO5KG2dX2izaC8PQ/P76xTBJ9Z1VvH+kxm7WOlPFqFgPbl7zj5o+J7eKPslypc2lYPekT0ugx6xPWbSeNlToeSUP2dJY8cnFqXtCyR'
        b'LT68GuVlaacpkqNzh06bjlyr3Rg1jLOrVEftJkBppkvj1O4iBadtrjRR7ewijVU7u6s9vWRaanevjuq2aoVBb86Qe4yMp3Zxl5seD1K7CtQeXjK+2lMon9mpi8MJ5DFt'
        b'VTLesLuXfHF3Xe+knmWDPtH9uQNuyqwpdz1uFyvzCgbjC9RePgqnToEsVi2U4AvwXn7v1H5Jr8nA+CFhGrU1qju+Qu0pUnv7KeI602Tx+GFyZ4os/rERg77+q7SH4gvQ'
        b'MHITPRSKB7QGZg0suqs/5JNzV7/fT6GFHaD3xlwyHtBnfSh4oIAVFiAhu3hi6l6FW69ut889l8lqoa/CTOEsD+2u703sWaUUxqlc45SucSMejIvHNzqMm/83UYx3yDd6'
        b'jHXkiA5j4zuyHGlxjj+gT765HHzIx7xuapnmOY5e0uk/4FXPr3qp+zlCylX24uy66BBGjI+ZVq+NQsKx/+K6dA6HY/oNg/68zIXbeyj6C64ZccbkXJ/QFOn8yjWjLvEa'
        b'S6mKmEr9Zy4Ztf8wl4y/uWj4rVM+24zfp2krwyXmUpq2rfxK7v8Gwx7vN6XTyiDqjm0Sl5SsbHbFvC+rapjFAoao5hfpGX++ZyrcsQJcx5RdnknJOUl4T5GsxQSt0PYE'
        b'u6ZUe93fza/Dfsf83/n28J8mYZK+TX6Ht61rS7ra7Ne4h8M7u3lwh6HbG77d5qfuZ+1P33HU8LbhkdDSaiZjRNek7qGASzY59d7waOqo3wbtKHAxnGsBN8KzFEa1ASly'
        b'x+CJwn/hPaSrsFrAHdMn8TI+utIbzJpdMWtuafWC8oqlyx1KsQPTUswZ+9x0YUwAsv5jHBhe/2dnobEyoal2b4DGf/q+5IfW7kqPUZ5+C8sm3TEkdFoPONW/N3TwATcd'
        b'IXRwHMeD478ryAT955R031VloRFj8jKDZTWKSanR2mvB+bjMVO8MjEvkM9rWXP0CoKAkPdc9YLcQ7s3gMlxTzjRt7HlvJ+kSocW0S0SXLDVsDhEyAg45wxsHToWlpmVk'
        b'iMTajG4mFxzMrgPHyygFzkxKgRMdtHheHN+dEigmfJeYY7Swlsdw8zg7tzAnrpGjAavFlLQrWnuJoTqxjJmHnaHfDOTPuYgPURjGcHhaSokTU4dPv+5Nj0zozZm6+Lsl'
        b'PIanxXErkZHcImppEgr7ed53a4TUdOWGduBHuvh8z4AxiN1E/QvO1MHXf+OUzOI0R/ckGm7GyeiPoldqYZo+Y8WGOnwKfCWs7qNPuB7H8Cmb5d+SiOXNOcX8nKlGDUYL'
        b'c9HOWXRnKWdf2dU63AqKXTEE9tjpicHKZt28120+tvuMnEXU4d7w6EfhkMld77tojOhwuOkZ/ls/Jvn2HL05xOLDQwEj+CWZvJpZETTUb4da2ovxqr9FQ8XFN/oUolmj'
        b'mCmOXUFK18Gzb2SZFNQtP2Q2/agm73IS8htZftsmhvmI2VxdRK+fmkEzGjKNyYQmR4KaCDRyVyMNCLSB69Wvj7/Iq3uKEn6UGLI4Nz3z3ehxR4vffRza8KOLq7vePtlp'
        b'nWDHe6kmUzNvyH7mZTxMlC92NT7l5XkownGql03t6dzHLm/s/uIL98OW88K+uS2pef/6Msnwmr+2/tPK/qn9t3O3fXhlcK1sk8D+rTdPmCuXp02pOX4GmFcoE2QPnVyl'
        b'td/y15i8ydG+ND0xcsOByryE+RP3Vjzc9c7NhIGO3LBfxt+3iT/z8GPdYCnvtUYfZv/e6LV/mmta9o3/512yDa1wfqKTltQ7560F9Z8rL/hBefsv+ybv/vZ+ffmi7b49'
        b'tuZvxpjMXvvDhzsW7yyu7H3rrOnZZW9/4rrLdtH1i7a1SyK2L/nuovOmD9bfOt2zetMb06a9Znx0ZYnHKXnkj6dfc8p/9U297g2VKd13QtPn5Jz87PTk06/W9Pn0fsTv'
        b'Sz1a+Np7q7Mm/+n7mtKjfp+f2BAgmzdc9nHIxH2hJ0OeGt/Je/Psqrfenjqyui7oUnyO/5ZvFA4rfBacXOvQMPT0zK3et39pjIzy6Pqpvi6rsSZ8S+l7Xz2q/9S4MnXk'
        b'zx4RCz7csVe04kPb6TVmT9fqLICvvtkfb/fhX+8tkWtt+0a+4fG4jqLXIt8IO3ID2C4p23V56NLP12tcDv353daqiz1n3lqmk1CzYP95r51Fm2pOmcyPa97wSuzACqfz'
        b'n7jd8fmAH3n7XO9H1SW1UzmZpV9vEPaa3X36y0/ZRzZ1eAjGER213C3FblKqANsSaTPaVVwvcAJS0oRUeAF0YJWQUm7pgiaug3/NAnicgI2doxMx4jrdGy1jfhxw1Bmc'
        b'ZcAh6vip3c+X6KfJ2NWoDorZhpRf29WwDWwmdgCZYA+8Vlff0GBkDHaZmMALhrVazER4jJcDzoKjYDtFAruORzow1diJun7DAGnsrYDqwPDaSqS9N6ajXJFmvZEDpaAp'
        b'UQgOkrLVguPV09OFKVRHZrSzueZw/zKiridDWaxGd8Z6M9wOdoHjlhWUAGEr2FyHKRxpnnoGXLEQjaDmGfR44UxeEOjyQZEFIoxN1i7jupiDi+SbN9wXAHbWETqTUSqT'
        b'MNBDW6MFdMEmnOzW5DS0lhmA7qjJXHgUracUVR82BZxJTU7XtHIxF+4FxyrwuQCt6BVwEFyFh+c/XwzRSsg3oGDpGQCFCya0dGkCJL8wVNPzYLvA4v8A5VuHW+JfYHk1'
        b'SvbzRW75mGeyyN7i0rWtMovDN7JC6usEq63xahMzpYkD9pWxfM9ymeuQhUcTH/9asWeFLGjIQtjEH7ZwlJk3r2nif2BqJXWVad0zdZc7q80tDybvSZbObK1uqT48V+6n'
        b'yFUFJLABCU3JQ+aJTRy1mXlTdtOMpgBp4qCZy7C5g4y7LxMt39iFSPPSJv5DK1vpFBlftrjNcMhK1KQ9PNFJ5tTh0eYh91QkDDmHDU0MR8riRAspTxrToiWd1TQP/TSb'
        b'KHXbGy6Lkc2SO7VVyGMVnM54WYaiYtA1TG3t1BSrtraT6bPWXk06akurVp0WHZmOfOKQpW+TltrMUuq3N2TY1kPO6dLp1FHwFPNY38n9CUOeqUO2aU3xamsHpDVa2GCV'
        b'rpB18FG4sg6BLfxHtk5tsXKd9jTW1rcpftgaaYMdlW2V8hyF25B78JB1CIpkZqG2QcqxNFca1BSHHdHUHw6R8+QVnQaszaSmOLyRSdqTJM2VxbUU3TMXqB1dZfVtBk0x'
        b'TRVNlU3Jz/Y5ahuHPXGPUEpTZRJpOPWUMmTjM2gToPBH6Vo4Uj3V0YnoZjx5dadJ78Qhx2j0zsZR5n8oVO3q1pHQliCfpJgw5BrU68S6hknj1c4eVE9z9yAFz1VIhtyD'
        b'sIrmKsuRm7ZNlUtk4YqAQZdgrK2N6mcjekiXQR3EzV2GmlmWhtJxFXSkt6Ur3Htdh1yjfv93WluawnLINRT9Gmd6UGePzj69pwUcZrzHY7S4jjN/1o9e7F6/6nom5koT'
        b'R/ROOrUJ8z+rzSy2pj6twqkoTd1/rDPCGx8mMShZwrsr0UoO16EbQcMH/IUz6mc/4JfPqJ/xQK+qor60vrp+3ssZ5xIY5Vh/KXTzeJFoVs/Hkrm+RrPC/lEq8D7R5Tuk'
        b'Wbm8zGYxHaU5iztGVXimp5QzVE8hBLBaSKNiKnnPCF/5/++Yip8VYAypNNqDkjvBmxPAltRMbE9BbuzQHGqWNR5c4cH18GxU9Q/Dr3PJUeCyY3sP/yn86Lptbc1tzZ3N'
        b'tUYfzZn5gbu2r27lo3kcJmOWlv5frlFx8X7d8lhTejaHGWHxPZ/GXvxJZjK8WcSuzWZnE9dm5fLqe2bBSsPgMaqB9qJLGPd65V+AX4keXjZGRbiKpfxiVlNHFYIf1zLf'
        b'V2UjQdu9jIzx6vH/dxnzMqotv+jQIuL7oSfkBfEFmPHeSbf09c/1X3gZKRZ/4W/8bOW/Jb66F8VX9xvxaZjeHy9A4jOyaKqX5t43dP6t7C7/u7K7QWT3Qj7TxspuPpad'
        b'5R8ju0osO55GdhwKrazk/29IT+s30tPPIDpidj7YgLRNC6fn+iY4bUK0Md4ce+5KPrN0xGTRnGDfmiKqosUiVTPtfdyI3v8feW8eF9WR9Q/fXtj3fYdmp2l2UAQB2WRf'
        b'VEBwp2UTRUB2URRXFrcGVLoFpMGtARUQFRSXpCoxySwZWsgAeTIZYzKTzJIZzWaWmcmvqm43NoKJ5nHe549XPzRN3XvrVp2qOnXqnO8551dx2bQFtnM1g0kVAHWqmG9z'
        b'OTCIIpi1rWAvGE4BZ0AbNmZQcD8FTiOxqZc88WMGOum5MZWxvbl6gwN9+DXXK00Bt+zd4UleTCyLUl7FZEAJ3J8fVvGYKm1HN1S2/6ftVz4dXS0LZIqKdRcTNDvcQhf8'
        b'Rrh5hWl6RDn4bPVB/ZXCAq0I9fHNTpK43NiBgsAI9199laUV0cRtdDUW9po6CU6tPm9+z63C7frg773SBr29srdtbMqKqFSzH/vE7p51injVByM1KqkH/uDxTdJKwTrV'
        b'8dqu106+ua/H55BOysWWgI7Bg9v0Pl59PUSw22yf2aJxxmWJrenkO1xVItsuhc2wm+fuArr1YnAiZnCK6c6jaCvW8Y2gKx6cj5klsxfBdmU6yFot3Ae648E5cA5zSiS8'
        b'J+OAw4eR+AxvwzraLrUP3A6NhwdCiLFLbupCImwDebnOlgDQh8TqjO04ZDsDp4G2S9ShheemRNCGM3JuC3xqsQJ34SkiIK/MhG28GGJXYvszwDUkyV8GV+n8pOmJqEFP'
        b'I/IFYNfOTjCI5OObXJUX2RnxspTZc+hFrok5ZXF27ga87VbP+oss8fOUzKCDObRpa2BTYEtQfeS0rpUwu3OLaIvEedzaZ1zXtz7sE11jwTah47guR6wn1bWvD5syMEI3'
        b'6ht8YmIl5GOBoYktYAi8p3QNWzWaNJAYFSbKmLR0k1q6SZaPW3pO6Hp9oUIZGD5SpbT0jiU0JBxOmtLUPRbfEC9UFfuJdCY0XaYMbAQ+rf5N/q1BTUFi9piBm7jsvoFb'
        b'fSQRLhT4jkrJn3Df2D8Z1oPQQiYk0Oznbcx+ZpFgjQL3eVL60twH699mLX012e8vsRPBCa1WKodazcimVjOzGatZTCqdGmChH030o5LLvMjsk2lA6ymikSXAb6yVzVXN'
        b'Zu1XlfOb1WwmlaOUzd5PZStdVO6TcbvVyqRUBZWqKpSqkFI1VKquUKpKSjVQqaZCqRop1UKl2gql6qRUB5XqKpRqkFI9VKqvUKpJSg1QqaFCqRYpNUKlxgql2qTUBJWa'
        b'KpTqkFIzVGquUKqLqIF1vxb7VVfrkTus8xEPztGT0+Qs4yhjtR66C2u01RBft0R36m+3QtzY5n2VRH4h9vf43l1d8QyWsnRZGGcrfYlD8r54zLrOZZDtbNZ2oibn5cXo'
        b'44SqQrz/mcEiYoHazMai/Mo2lv1c5vf7ZrUQ/4stzC/L5xfkV+eUkvRLs3qVX1hahv1ZPNTnPBdYzC/hb+XgWR/IwSlx8DdOWRGHT1exLDKKk5tfkOMx58k5M3z25mad'
        b'VI61wnBvbCbPDx7AnG1ZDDqEu6+UBT/B6F43DwYVzVDx11xQ7klh94IdsEGjeFsKuiK/LVUVKxRhfSI2y7shjp3FWQ16VDVNwTE6tvlBeIdwxzooogO14yjtvDwSpD0C'
        b'njbi4UjYx+ITEae2RRKviLnDEtTT2r/D4BQQ8OISPdxdt4PmOOKYYeDMgm3ZUEL0vZ5gxDLeJ45JMYLhEOyn4PBOKKJh8EJ4WxntIQkMirm1eiPDOxUMkx3U184U1IbF'
        b'y/K5UxpFTChSggJaEr/lDkmkmWQc6PFQgq4PukMbdrLC4S3YQhCAsBHcBnfiwaUY1KpYMAgb0S069qwMcHg5gd7thHtgl0zTgfvkgraKYeYOXTBIyLEIDFjHxya6ossY'
        b'lHfBERxigj1O3uRi0m5vcBQ0yFMG0PkC4IEcWu89qh8GD2Xmy/Ms4MC8oF2fiCgF4CA4SqdmYKKt7vJ6hqcZ6KLp31CM8eOp8KYsBQNOv7ADNhO4YgEQL4LHgWISBTqD'
        b'wmgCUWwvV6WDu3sZr9iwd105RZN2DxSBK+DgQho2isUiCZFYPKpkuSuc3o2OXWFDyc438By4UkEnS3iaKCGYjVMlZIMr5MmtxrLI8soHCoIMHSkyOcBJ0A7a4+PAHnkK'
        b'B5y/QQMeo8GinagNAzx59oYs0CpP4ABadMplsYTrwEmSwAFnb1gOWnEChwTQRKdNkFjD8/OlWMDpFaLgAaVc2KxDRjQYdmXj+UIOZ9U1aNy0oZi1zghcyHc88Dt2aTva'
        b'Dm6G3zmXNpoEvQyvGThvPXX23Na4NQKBqZnr4wUXV7kJgspUVdXe4WeWVr4Rfdxz458jRpK2vjVRmBJ2cO2n37b/8Ci27cknLKUYBzuD21trT/U1Rq60b1w4/X2SpmmJ'
        b'p/FN4dvXq4bff+P9bJVUqfd7Wd9PjLu8aV4Dx9bdzXmvPj53ozDs15/UH4wX+XomOi67UGvQsMXp729Vd9ovLBntbnrz88rirENtZcU7jCsfjUZ73u3/7qRHcFhrVdm0'
        b'2s090a2Vvzm++oOusD+NSyKmbzYGXL6z6d3Hvr3ru+7WZwUePx1m+U6VzWt/TbD9+N5vx1K3/i3z1K+DA5sqKz7vCTh3YNfv/ka5vrn6ywDfP+y/qazz68F3rP5+hblw'
        b'cKD0QGKH9VdJ/IrwpiHe8IWS8+l/axvPrVuUvq3r4ZWAlqlgg92J10u83y7h/5jktUmnLGiy796nB9558OS7++1uH539Xrmz4bFIsqpBdAJ9fFy6pu5fr+c9fCz6F8wr'
        b'mfh0ze96Pv/hg4DFb9xo1DB6UrMw72H/X74WjYQMgT9ZCcG/il73t/ds/f4vSo46S7Z/LOoOreKa09rPLrjHhRcO658KcZdt4B4i+nkjUW0IXEqKT3D1oC9rFDDhWU4A'
        b'uWqwPYhEdqWthKrbcKxfZg28vYiETNgKGsFdDZIV3clEbsNDJ3q2KmzTJ+FbfMDZrHnMfKawlVj61sJmWv48CppgH47zT/iksvkm2MlUh7Vq5DVAFAH64DE07Q95znBM'
        b'jVImPFUNhF8R0Pn+IHiRRJVh2mlVMMIWJdCRjW/Ze6BnEBeFEnV3V5qLGsPT7EDY7UUAV9U2O8GhCngxGXNSVgHGeN2kSXbSqQAcWpCeTPgoC3YygAC0+xGZl4uW9U1w'
        b'KJkwUngEHMKschNrEeg2Jhpya1i3k+QsoJnpUYyJS0D36PuzQBe8CBtJ45zhLdCFaiH8FLNwd8yU9XewwHBYIXlPxgawrwLtBDgPmoynaixHvQZ3gujQKef0vWAf7EE3'
        b'yNmqhiMTir1gB+nDIni1ko7sS4f1Bf16TPetpnT43L6ogJkEa1xwowrzPx01VhkUZtKhyo8x0REN30EYkLLqyk1MMy1ZgIt9+UvwWBAGNJBAH1f04TkM/D4DztJDOgA6'
        b'2RUOJLIK4UIaaObA4Yg8+rRzwwltDoeSCbvXgYOI42tHsKJgLfcrZ7L9+ZjxktznZmrJ1iV8KrRcRS9BHv7ltAk4jclNb8PZ6agt2nmswITlJLTJWtCAZhcZLFTRXh03'
        b'Qif9RSxwaz04QAenvuJqjtoZE4v7tA+eoJeBvjYLnF8IWrjarwjThg2Citi1WQmTdWUS4EyuZHLWWcai1RmbU2htlDhywoA7ZWEjiJTpdK06/UX+OCaGxG/cwgsX0yUh'
        b'ohCJw4SF5wfWLmPckHHrJWOmS6YtXCSG4xYeWJVsQ3KdR41bR4+ZRk9Z2YqdRGtJcmsbN0nqgEvP+nGbIPS3Jsa3OV9w6XKRLB6388c5yqcsORhQJU5rSyb52mf/iTOY'
        b'Z/dv6tk0sH18Jh/9tK2HpKy/qqdqRH3cM2LcNhIna5+3EGfqrhJVSVTHbbzx6x/Y2ONfU2ZWnaYiU7HLuBlPoEwScHPEUVIT14+cPXDC+CjResnKgaU968YsF+Nk9AtF'
        b'SfhXgNTS/UsVtou5kN2u+Uib4npKtktdAkbspC7Bky4RUpeI1yLe1ht3iRdqTdtxBypG8qX+MRN2sUKVKZ73AFfKCxKqTJi6TLksGNiInhOqtGtNuQWM2ErdyAXulKvX'
        b'gJnUdfFImNQ1BF3VmfLyF7I7NUWa75m6/3zTFP4MlFp64N+L0NnzSy0VWYt1cV75hKaESUMfqSEOp+wp9Y2bMIyfckMjjS9MGHIf2DoSwlnYdC4SLRLHjVt4ClSnDSww'
        b'hWKkJm4fcb2mrBzFuVIrd0nViFLP7jHLJVOWDuKV6E349yqppSeikSt+I0YLcr1Rl1wWj4RLXZZMuiyVuix9Lett73GXRJpGVa+pSf3jJuziMY18B2KlvJCfo5HPQIDU'
        b'NXiEL3UNJTTyCUA00hZpv2fq+SKNU/x7tdTSC//OQORCZJI1mpApqSlp0tBPaug3kDFSJF2QNGGYjAM0cHu4iFToIs7fjkl1QlvhVK5JhzG49ovCGMh0+k+X80+t5mK5'
        b'Zh8f29el4GP7V9TLnd1JoliRMpfq0fD7ZUnPSUZfxk8kap5ptjwx6W9RsxUyH9uR7OGyk9vTzNevJsG5LJGqyobS/LzC5ycSn9PGMdzGx4xZbZTnEMdV8cvKS15BnlpZ'
        b'rl/2ho0+G1+4beO4bU9TNLtEFfDzOPm5nPwyTn4pOseG+4TP0PPVZLfGutcXbt7vZzfPkuSdLcnJzi8rKnll2eFL/sx+iSZN4yY9TTZsLWsSnQn+1dEJjaTahq1F2fm5'
        b'+S8x1T7AjXuaXNqZZNzml5Zx6JqyXmUrc+WtzKnKySove4lW/nF2Kx1mWknX9MoJqULHInnxBj6cvWJd5auiTIG7oOVB1/pqJiFpZnbORjSxX7iZf5rdTBvCWEgVry6D'
        b'eJ58lOXL7oVb99nsUbadtXZfWftmZqFc//zC7fvb7PY5Kirw8EDLtXez26j4+tl5kDEYmFnPksFrKSbVMKOnrGEQvSWloLdkKGgoqV0Mmd7ymdLng3/nwmuVnwP+/f8i'
        b'R/P3GXM0nPgfWTaVm3IQNUsQSdGKUVg8JTl01vsyDpoOhUVlc5WkcxSl82btfvzpb5gka/fxnrOzsnarJudSJGu3vwOXQZ+2+102oHOYBNR5Er2lwnHbqmSeBNGjOLCT'
        b'jXzezDT4KYI2Ny+nbFb+7o3pDMqShAAcM3R9yYzRL/S2fyoAdb9ak/6Lcke/iF2eqmf8V+zyLzCR0Zj+fcmf2aVYEXg15IjcLr9P0NWSv8CeZVrmc8/3tVBHVp4Glf05'
        b'+6NlQllOdiiExyJoZYp8aEFrFBndFNj004b7EvCzxC+VDbU+JTvxoqF25kkWnNkiiDyRPMuCT8Zai/GCFvwXevU3ijb9fDzuZi9r0+cyiVoe1JrHxhNNFGwCp9k6DHAh'
        b'LoBcMYLHquN5SejK6p1sXwYYAt2gK7/kvDezFEcPStgxjQH3e1q69nGPeB8YPHDG+O2/frkrMykrjs+8YrbFdLNpivBTLyXfYrTuXm9Ui/pVknzyz3c4weP9lAjY9b1a'
        b'bw4RCMWtaIpPsVW/ykhnsPV4X2sz9HwecBwk2VIT3zFd31kLbT6Sv9C7/iEnMXrX16swidX+V2nZZy8tNuHAdFZrSgaaeLV8GNu2Eucw0QgM8i+lhRfEdWebtko5pWX5'
        b'BQWcCn5BfvbPWKnmAmiUk1KjiIXgQfoOSpVBmYYpcyqmLH6jkv9x59vM0hJ0ZduW92jEgyPiyYa+K32YOUKvnMaq2oduGW+Y8US1PgUZv3mo1Fj6YGLP0vN7B4V1TYzR'
        b'f1/TTNDs+M0CTeW0joS+ritLmQs0V30gdE2H5WU+uY8fnuznSx5uzHz7IUxtAu2fM7flOdojZmC0z3T18B6uKtEeusJb5TyiLwPCDFpdpg2us6JhJ6B9ctPBdR62boFr'
        b'u2UGLmzdAsPgAlEubqwKJXairQG0pQibieC+eAKLLQjZyYtLVOPMsBli9lL1orWKDaZAQJuggqqJwhQboFwAnR2NFQe642Pd/LVjleg07N6y7GjxUKzGgw3JseAiG4hA'
        b'J6VcwLQDp+FVGqV7Jgn2x6NrWlDopkyxLRngCtrGurhKzz/8Y8iMAmhBNb90Axnmp4KQvIQsskp64j+qRmzN1LK1prlmyoJAY3c07xBnX9jSvWXKAmMTW3c175I49Lv3'
        b'uqO/HxiatiY2Jd439BKnXljTtUbAmDbAyAXTCQNXDENVFim3qQrCMGA2rimuJUHsLTV0mDRwlRq4SlLvG3jTVc5CIcyzT84LQlAAZJRYKivKd/Ju/aCwVT4pfemtktj8'
        b'6FYZzBdyUSG2IkZOlPwZU5mFzt4l2KGpZLcSJrr8APe+qvyQ9L4yfWp4X5mW1N9XlcvE76vKRVjCoUivuFr/e60uho3OE//w1xi5ITfrb8G0MpaHPmRq6X6hTGkbiXxF'
        b'ZULXCS3HJ8xVDC2nLyj8iWMZOj0iBY8rmPK4gYtw3MBAEjbQ2Hpal0uXGAfWRz2NNogDCRqEMki4QVmRDy7yIyWyQIJ+OJDgQhJIUBZ/MBjHH1xCwg/KSgJxSRApkb0M'
        b'B0A0DmeQt8mKFuAif1IiewxHUjQNUKxoMS4Jro/5WlVdy++xMWVmKzX17Ao4sxj9qo99wtbVsnxEoQ86JiGB2x8FveFwiGjy48FpbFNXB0eZYBTc4c5il/qy31+GoOV1'
        b'wmwe2Ioy+jFFP9RFphykQTAQWvX69Qa5Sr8crkLXgsQ3tf2qMpiKKYF6qM6Ceqg+bcVF9RnYDN6hNND72dkaCu9Xm/deJXSe0FS4S31Wv0wvasnblG1GatUn9ersV5t5'
        b'QmPmCUr+FAbyyH5ML+r2KdN3qqH/2eb1DBLRkcaIaNVr1+vW69Ub1JvmambrKdSqObsdsh9V9KOWy7qo3ydz68y2IBAhJYI60ajXRPXp4DbWG9Yb1RvXm6B6dbMNFOrV'
        b'mlOvrE7c3ouGCvUqyWrUIbUZo5rUso0UatJWoKfxU3oi+jCzTRQoqrNdG4nMlu9ry9Yp+sXPyyn5yA89Mmu7DuPMvgPv8eh3KYePtnfFTR8jXPhlHH4J1o9uK89HzGdW'
        b'RbnoNEbuz0aXssqwPiG/jFNWwi8s5Wdh1UzpM0CY2DIkRBSVyF418xZ+6cwBGkkfhRw+Jy+/IqdQVm1RyfZnqvHw4FTySwrzC/MCA+cibfDZ/JkOzggv4UtTwzw4kUWF'
        b'zmWc8tIc0oPikqLsctJc29l4JCatSz/FfMa7d8aZthB9nFCa8e5lyoOHEkiSyoxfr9Ir8+vN4zI/Wv3scBLCPoNKkkttW+UE+EXApBn644M5mgSKgzbvCRzPFDLA2R6c'
        b'WKIYzi5CLUIndk5OVX5pGS6pxOOwUaYHzZlHkpQ1SKb1ods0RxdUmY8bia7klqPq+NnZaFI9p02F2eiHwy8uLsovRC9U1An/jBirTD0rxmollQdRWMayqyCJrGRZrGLk'
        b'qBJP2AyPJJCEUytiEpLkGSHAXVinEbkCngP9OgSAZam7nH4+Cpx7tgr0oAw2VAHr1HC4v1MEG7R021bYwnNkJrnHsCklZ+xndhTcJQHhEnM4PBVDcA4HoKqC3WtphNNJ'
        b'b9CQ4h6kA8/DK/CcD8XyoHSCmA7wCGgpJ3bpk/nBoB/sJ4mM4zGMFrtRY/zYshXuK5mUP1cJNBXx6EB4+2Er6OIxt4OraPenSmNo3HRzMvHGVQ1VztT8MWoTVY5TkHiY'
        b'7ox/2htYn7Ac5/oAQ7pu8GginU1jeZEKrC0BZ2kc0pEaBri6pXQbWm3wGAUa4ZHN+eIH36PzM5rrb/72D22/CkHHggB8LCht9YJT3MN9ZrYXnaLEm42ZvSJB6lDeIL/3'
        b'3YdvGP7tk9q//PXha12HLNouG/75vQTdCneWds2tbwt4Fcy/Pnzrwt4mrB24dND2gFJuCzfCPUsr6yTn/GXDlX/vWqVUZgJuGXrtF917WzC5F/4JCDcuKC5t/E4A2i+1'
        b'sKaPOkVJ2qalH7g15j/cLNz6sOoTh22/Pldc67BFNFZzINjhr6IrvzUzbRSMazivqP7ofbPPPjlc91a6FkvwlsrH5T6s7Y+EzO+PnWtZEM8YP6h+zy5/4PM4YcmqXuFG'
        b'7lqvH/h+Y9ZVb6f7uPia+hj6nvT19olk1rz59pjB2tct31n2br3tejW9TxNUqB89oh5MJ3IN6XQ9Q/AYaJJB4zYywEGGdwgcpdUbBzbD2yoVNJhlFpQFXJflVbKuWBGv'
        b'AppnIdSCwVlyrcwYiAhEGvYvlwFs4Gl4hpyFtOEo6IzPXjcbYIPmIp2SCVwBZ03kEGp4LoBGUQ+arqTRDY3gdFk8ASRqgR6cT0jNkAm6QAudtASeWI4jxiaGgJvwcBKe'
        b'QK5ItARXWcsDwV5ZMnZD0MbzBHtAP2zEApUykDDdCuF+Un0sHxUTgA+riob4EHzPKBwm/qXFZeAAOowlALTgGBTblgE6WD6ElDbgKrzA80hTU3Ca9PSnE0XdBUdyWGjq'
        b'09ATRBOcQ94dyaDgOjsG7mPRJ7nT8AZoRydIdzBAk0XZgKkFOtRouPtZ2KGBM7zEw/0MnEmFBiDpgVYWOJbhQ0NYmsB1e4xQObHhKd/QTmElloPrXxHM5j6+NnrwKA43'
        b'2JCMM2nBo+CoZzwa3aNaoAlR+xiLigaDKjgKFDxIN+vsbkwRjDQ0BJ0zYMMbTrQ7qBgcqQQXi2WZchTS5OitI+2OM4DXQJcW6hZqEZC/FEnNqKK7jou46r/ghIFDY3Ce'
        b'8RwjVmaT2Xv2bOjIcgZ94oxahU6cNvic+YG5w5hj1Lh59Jhh9JSJdevu5t2kaMm4eeiYYeiUiVlrZVNl6+6m3eKycRM3AVsOJgkSBUnYkrxxi4UCVfldu5p2ibMnTJCU'
        b'b9wa3xQvZk8YOk6bWQk3SVgTZm4DzClT805VkeqYrc9A+vCawTVS29AJ07AnLMrcfczM7YGZRaeJyKTTWmQtUZ0w8ybtWDTiJ5U35iPFqqw5nXmivLb8ziJR0bi156R1'
        b'oNQ6cNw6aGS51HqJkEUqfYA6hD3/su6bcAnoZcm4deiYaeiUlS3GtUzZcglMguNMACl2TuLySeclUucl9535r0W/lfB6wmTkGmnkmrG1meOR/HG7jQL2CZ0nZnRrv3+i'
        b'LvtSSmClljZR+iy40CvKmnVPXynKQuWetVKUs8xfUF0BU4DloBcAFtBRV2agBC8wwhYaCo6CpRno8G2LQ7DYviycQKjsQkk0fH85nIDLeF/pJ+1Cz/ZAbh4K0piFLPCd'
        b'EaPmyk0KMtIrghpgq1ZJz08AIZ7X6iUaitbpErbyM94Us2PCsGiTVT1bpuv//4/RCkndJSPMZ4gzr32pJsydTexL/1MXNmNfys3EFqbrFLX4MYvh1cBlECwpOAOugYNz'
        b'WWsBPIC5Kzy0/HlGJqdnhrM0q2ADCc/yE7amFav/l7amF3xphIaCySli9aszOc1yJyR68XrGf8Wd8AWCE7Flh4AueGnt7B3ZEbbDo9ihoiHBNc4N9KbSvhW4IDkB63dB'
        b'H2jQCMhwyO9c1cAuDUC1KCVO01rvGzG3WrzniLhOB5PEHqZ3W7in1aoTz/c27xlSoi5uU6v69jsuixYLrqzUeJ5YoCAT1CEp61giaCQxi1KhBDVjNpCZB4dnQhaBvfZk'
        b'jqL74In5dn/Qi0Sau9qg4yfsNU+ZP3jRCSQ3m3HpWfs4A81aUytx2qRj8H3HYALyjBu3jh8zjceB0eZa01R+2pr2HLe0l2leosZT09qT9NUva1rDxOcyyWkOdu2Ee2jb'
        b'GlsnHzYywAVwk0tsa8vAXnSJGNfYvuGgjQGG1qTlS9ZuYJFXR/v9ev1eYumcZV3L/EdmbFYSn/mFqYJ17TyDmuSo3S/8QBYH6mdMAE+JAjFRTJ9HFDJKNtSMqS10NUNV'
        b'j/eNIUvP55EqZes4j7FN6fkj8lKvDtd4ann7Jmz1y1recPQpxFixFn4Wo5lxGt5E0QY4maOZcj2jXgXtK0ozrEbpVbKa78/P0UBE55Rx+HIJQVEb93zdzdaSnFxaTzIH'
        b'zjiPeqUkp6y8pLA0kBPGCSRueIGZMmJncoo2bs7Jmgde8TPWPaUkOg+3xAkxRJkDWdqydPeV6THupvP5ooFaP7XN6qCbpAUHZzRWxD+jQcEaA6wugJ3utMZghYYKPALu'
        b'xOb/07uNVYpFoepbSm2/CiT2/hst51rcEe+8mLt37Jpmx8WpT4aE3m9uNl3pG57x5k7Hi15Sw3tJJ13f+nKh8shaA/ux9U773199z/ye28KE8dp/PHxto6fxiek/a2ou'
        b'/cDxg2ILkW7Fe17KxDSd12fQwVnJVSbHYk4SToHTBOoUHE/gRW/ae+GMJl/RtwS7B/SB1pqNUEzOWkGbuHNP40pgRBUOKNGn+QvZ3ugsD+7CC/R53hux3g46IO5F2AHa'
        b'4/GxMBjspU+GGquZ8LJ/PGHTceDWyme4+abEp8z8Drz4Ms7LCkFyNLCvrmxKVZs/syIVrhF2sEnGtMsw03YQR0ocMF553MQPhy6ZfcwiB6Tw11KljrHj5nFjhnHT5rZi'
        b'hzZ3gcqUgXnr4qbFYocLbl1udGLI+wY+JLRd8Lh5yJhhCDrrCRRRz6o0zydmtZ82Bao+ZfwyTpOGbYE/0a9U+cEEc/sczGtMH70kzrmk7LkizUaKlltlERIoGRjslYsz'
        b'31+bl8eUzQUAFuXKvVH/+ywnjH7nC7KceZE/2gvcmERWeGsfgw7vyMWxEsp8Lh9s/L3PhFe2N79XNfdBwtvfqlC/91La944ml0my/wb7AhGJ0yJ3s4mtBiNKlDnsYFfD'
        b'PfAc0Z3kLd0cHwvv8GZcPLF/JxiEJ+dHB80gRiyYz5lUMiqTxWJLL5ZHqWsYlIXNpLmr1NxV4jdu7oWWADr7o4Uypus4a/d83iynQzg+ldZ/7vXZChLM10vXvKzLvR9u'
        b'DZP2/1cp5VfkbOCXJs2yjswozQso+U5KrCP0TqqKzpBUrvJ/wTaCTpAfbZzPNiKf7NjElC1L3/dCUz1sxhyWU8bHKGM+jUXcWlSBtmac11Be76taJ/QzMrIGYhMKMYS5'
        b'YbvJ1vLSMmw3oddtaVl+IQ3QxnqGeQ0ftO5hFjoV28FQ5fMZXWaWKG5rCb+SJhfq80vbSNRpYaDcBucFmy0MEFHABwzPJw3w1WjI2SATXOJhT/AYCoyCG2gXvJxLglfq'
        b'fumakqZ16YsKrWI2xRYxyt79E7FB+LgpaU7SWUrcStViqVTaAk/S09+1g728ZFTZCmo1uApPbUnIV7nXySx9A6+cS3e3JoepAy/d9j/45R+SVPY/ZAV9q5+sdCzgT+eN'
        b'XJs59a216Y/1/n02cYvh+w77tYaGhnw9v1aGeeu/v59Zvdq6d9/vUmrszwuZZkvjYf/69pzIBdu3p3379T8mPk8zPvXxUSvLVT7bwZvDgb9X9U/SLSz4FXeDRsfSd/fA'
        b'doOVwlV7uWdsnK/6fBl5Kik+68CS310xmvzwiGdSmwCYBNqcy3A6vmiz7r0At3/+MHzPeMGCBEng8UdB6yMPHLxX9UC744vHjLoVniyVY1xVotl2BkfgZd6icgXBhLGO'
        b'yA4Jnthp3C0JnAKdCrJJTSEUErkk1he0yAWTHfCggqUgYxtBIRWvgtd4lrApLjFBpjPfZkKU7QvhDTjEc/VIAWdlTplqi5mgE/StIbpjX1gXpqAz35ShoDW3gh00VOmo'
        b'FtgDDyklKEZcGUzKoV0267lQwvOk1fyOrkTR7wIP/W+UzhzFCIAqskAk1cbzMEtUTvi0lObTj0vW/AKhxgiHAWRPGDlK9GXK57YAQeQTFmXs9EgZpwZfI1ojMRsIG7da'
        b'2KQuYAuyMWRKQWFtYt5a1VQlZouXi1eIVcdNuCQInDC7aYeAPW1gjhXUeeIyRQW12LBdW6ZAthBoCMoEGk+M0NvGjBy/f6IrL6b1vq+r6EWosoCrfoQhC6oqReipQEOl'
        b'CGuZ3ldNYb9Zo/yzopUapaDypfehPCxbPYe0RYoK3zV4D7J9/JIK35LlFIHPEqU02Y3UZtyjaEiUlTIOUVPAL8zLUlHgV/pyfnUYb0+a9PZUx6pj1ynVKaNtCuNFcLgq'
        b'TYIZ0anXRRuXXr0+2rYM0HEQZwk1zNUn25cK2r40ZrYvVbJ9qShsX6oKG5XKLlXZ9vVMqSIi86Nd7Hm2r7DsbOxcVZhTORuQie3atA2dNvlnFZWU5JQWFxVm5xfm/UQ4'
        b'EbSpBPLLykoCM2fO1JlkY8DbZBEnMzO1pDwnM9NN5tZVkVNCUGkECjKnMv5zoR+cLH4h3q5KijCSTe4nUcYvQXOAs5FfuOX5e+Ysy/8zIuq8dv/n7qQ/tftiQmBgQmlx'
        b'ThbpoRtN5Xn30qfugYXlWzfmlLwwimFmUtLNeOrCV7kpP2vTrE2d9KiQvzVn3hYU0R5FcjpsKirIRgtKQUR4xt9oK79kyzNwnZlBK+XQXokenGTsblGZX0q3AMk5m4qy'
        b'OYG55YVZaHqge+Qnocx5K5K3PotfUIDGeGNObpFM4pgJ80NPgnLs+oSxNvx561GcQ8+l5Az2OpDzrOPhU/cQ+Xuf5yYiq2ujz8a5tSi6L/7M85irIPEsJZmz0DfA3Zv8'
        b'XY44HFqE2TnyoZLXhaY+PUvm91qJzMnllxeUlcqXyExd8464cymH/IkxUXMaN0uGk81M3JVidOJC315AAp0l2hnMEe2ckwhgIzMa3Cz1KQG1K5FkVUSB4UBwhoS2ga2g'
        b'F8kTFdtU4FkGxYD1FGyH3a6yGO2loeA0D+uSr8J+BsUERxkRbuBkOT5SlLIj0FPLabnQxcPdBdZ7usYmIhGxN7UYXilbCTpgA41KAcdd1RaBm1BY7oGlBCwgXpiFxaGj'
        b'R2AUTQo8QaMbstargi6w15/Ii+FOmpSppb8KtSwzwXVXhiypwIgFvI0FpBkgDInNAXp48W5c9zglKpinDE8ZwR4iV67UiObBZmd1ZYqhh0P93YJHSdXHi1UoTRcRDvVX'
        b'UMsvpyMGdq1CMpfDlwwkn2p2GMoy8/HcmRS77JQKTtdn4L2KokE2rfBmNDyDtrS1UKBBaVQnk/jH5AGJgxqlyzFjon3WbekGC6p8MSq0A1eS4CH3uMSUGGIBiEVtP8zD'
        b'yraZfuSCO+hajFtcgkesu6syhSQozW2wN6ocnwHhHdjIIkI6OGKpKKcf5mKcRE+qTETnKlNIULuhBs6kgd4orioZzm3hGnllNLhAjizYDc+QS+AiuOmMwxiBA87KFHM9'
        b'wxM9PkLk+8LFNbvRoB1SCGIUHUPC87iCBnBidgAj0MRkGbmlkzqLFrls14tXjCAET8M7dLinbnge1pIQQlGgKZaO4EGHEOoAw3T0pLpgAzqCELwJBpGsikMILYEnSAgh'
        b'0JCCZiY8wgVNQfNFEVLKtYCnuRp0slw3OFoURIguC4GVxiFv8IU3DOUhsNbtkPkIKMEjNBZLAJtAG2hV4yl4HBFXgM0J9LHnPGwDPfE+cas2oDVFImDpsGh0lCB+Wzyp'
        b'N4vWC+qiLmGCuKtoKkS/As1VTCiyWEpIiXYRWfSrII8EOlwLiX61ZbcsXGXzSuJ24AVGPWb8DoLpzJfwAuwBYnngK1hbLfdoOLyJXN+RFoxfC65AMa2wlYVRygQtJFpT'
        b'8CIgkQXGAiMsueIE1kfR41ALB0BLChSkgYNEZdxBFaL39ZEoVVrhaKUUi9g4XeNn27dQ8rm0Dyf2aEn2ANfYFFOTgnc37eCq0yGphn3gyVLtknI4qOm9Gg7qgEY4XIZI'
        b'u5kVu4Nf7oSfH6qCInRLKLiM75LdUwqvlmONz3kW7ADXoYBOIn9tXY2sMnJbZdk2tRJ7dy1tZcqFxYZ7HTzJSxdWsuBQObxauk0zFl7fBo7olJSzKANLlj+sQxcIW+rM'
        b'AZdLt5Wrk3p04DU1OIjeqIlulr97yXp4TEtZCfbBUySnLDjuC4Zkj8TAG08baZDDCjMAApKOF14HR2pm6kXt48WrleD2WYPLbKcQICFVWYFLYI/8rjpLQpMSeBW1cSkr'
        b'ENx1pzu7DxwGl0q3gUOIMLL6EKdVpnSVmThwO+gkw23EDF5WqgGvl6HmaKpplShRWruYYAicgvtI2mR4AO4tTUmETSmJoB8egSdSwBGc3uEUA16HA2VkcmvCVlbKsmVQ'
        b'iEPkoxdTfHiDxiiGw9HiaDAyt34NMEgeNTFZAi7VlMLrOugKE55nuMJulXLsYgbPbg+EhxDHAwMF8Z6JCclpeH9YIVMtuGH2dzgWnSwRKwB709RKoaiKTi3ShZb4yXhs'
        b'TGCwKEYgBY+b8cm4blBeCs95wKEYxAni3RHzTGJTeqCdBU7CE7JYrvuXm1N+xV44e+laP98lNGv+frkrleq2DBeGr0A30KlZqW+XyL64hHLZBKbJtnACWPxPXbGd2r4B'
        b'ttBZdFv1U0EfGwfYM6umqj3BKLkX9PvY44yi4FRuFVUVpUtnML62VA/ilMI54Eg+lQ9boICc1/L3Nr7BKDVjUdTjXHHHyj8kT4Tq/vHzmmu3Pww71v+h0Wd/4WveM12w'
        b'S9deKjT1u6cbcVh/w5Ow1mFrvfD3Jbfcbe+ZfMx6lLsz4D8LflS5cO5zo4rrXOuA99v+/dt/+vuOdrz7u3c97YwDmpb8J55fqjXY37hqfcvni1aXVfT0LwefeVhFpX9+'
        b'1SeuOCJvtOlhhtGTP/YZ+HTnPfnB0OvmYbOFpUHXLN//YWGfntRo/easr93HHn35bZT2P3f9W+PbWEkdt88r+MgPIWqxoVXx9w438zpdMobe22J75KGWi+/N7PZKyZ5r'
        b'On+8cYj3mw9+/e+HKT6l4nN9Tf/8+LO4bzWb1/m+KVX1ruO4fbj02/y/Vr77x7RPYxqEn2qoGnx0+v0tv3n34d0yzweVGof+ppHjtOWJz11W+siy1/M/On/yUp1JEnjj'
        b'WweqJGqkWPv7mMiGkow9QYLykNCSvrMf7Fp8YRH3A41PdzRuiDBs2ZJxQBhUddq4617arnVHPvn1X699EuCwMayMAy1ilP2bNHuXtr/ZN7DhevhfThakcAZbb3+4176o'
        b'NepD9yO30s2/E/uVnPP7oqkgqyPL6qbtyiW3dP5n07qCq8oLT/Uf+XPume1TvcLpiW2+F0/88cbA+jtOd9ZY74gUGU0c+yzW8SIc/zClyq6o7SLP/1edrsvatM0Lzlv8'
        b'sTO1+weJyVu/+myxe4r0cXCj2deWZ3bdq2pwvnn5s8+mLfRuat08Nhbm1huyvD6t62xeXOuid2J/PJXjvrCy4ODBR//y+KozLfK92O+6VnspvVHuk+HZ86/I36cn5sdt'
        b'g+eL/5Xz0SNnn6K/Vj5Qzfsh/2Sib9xj36/TS6x2rV90n70vW93q/mdNP47dnwJ7sk2Svlpyldm3SVvN/Qj10Ez/t/ed9U3v/qVS3dJpt4c985C7z7FrUe/t71MaWWDm'
        b'vPb3dSdM6qOWnFo7ZVTxdZlX3PnYqj7Rv4y6f7/xt/+aMPh4fdbmT3X/ptpd9seAt75SbuhZGOXy51qtN3htLHAd/M394XtJtw9a2a/Ykb6/wf4/y85q6Y1aZIf+Q2D7'
        b'hz3jd9SM43al6vz495UL39G2Enz+pGdS/3FwzsE3B+/XZIas/R/bvIv33tpd4M2+rh/L9SBwziC0AbUh1neGNxvUoB/LAmLQAGuJMc4Hdqwl4ss+cJuWX9Bmd4PYDnaC'
        b'7mxQtypejrRIJsEa9WAdCxyGV2AdDWQVgCtgj0Z8LmcOAHe5HtGepaaDMwrhIdGmeBmHiLwBbxEAb1ViJRzyJ5DRZ/Gi8XCI6MeM4H4kLx4z4z3VzKEe0ADelSawE0k7'
        b'ysuewlnBWdhLOmAMj8ERngfYHzAfoNVDhVQQGupGoisXLH0aXXmFrHJPeHcFGFrLQ8LBEWWK7ccAPfAqbKI1emIkQ2GlnbPrDDoXEaOdXHSrhod1c2bHVx6MhqfpJyXl'
        b'8DLOaAIb9GaSmoB6P/LKStgJT8TzwGUNE9RWZUp5O9MBHl5Oo1iHskHL0xwvWBKk87zs2rD0KzqmpkQnNYCnaLS9Aq7RVtsDoM4hXibjpsMmGR4Z7b5XyaO8dWhEDqEN'
        b'RQ00qaATSzcjDd7ZRlSu+ojcV0C7Nx0rlfhn6i0jgx8OxWB0MQ8eckOCKHoWNia6IYnEkwVPcELo6YHj/12Lf4rz1VgNBmAP3nb3LvwKM/r1mk5Y5guIlpmC98ArhEqW'
        b'oIkPBopnS91wTzm5qB4EjmzDKccVZGvUtxtkwmmCYzufEa5vrGAZ5cNW8mwlOLQbtMNrswRsM3iYDll4ER6zIeI1GIZXZ8nXPXQuG3AZjCbQ8vXiNJl0HQD3E7SRaRYO'
        b'73mE6xQ+v2ztAa+SFnqB46Ab17HYnLZko3fAWlaRiz6xx7nCERx6ECMEGuGNZBxwfBfT1Qq20TH2LrlgRwZaKsMi2TZ4TQsOMHzAXoabbiDsVlKDEnCLjix+GQ6g6SQb'
        b'ms1ZWFY/xQSNWzfTaG1BuBmdYTe+VAU0eMaCSy4MyiKKjUb8JhwgE8cR3kVyOSbEAnBdCZxlUyqwi6mK5IQWEsIR3uV50Zv6NSBEu7p6Ko3Lb4Oj6i7gkiwaoDxJhD0L'
        b'HlUDB8nyhEfQoYC+7qEFxYmwEZ0Y0OuhkA3ak8Fhuol70MntOi8J7OOjG5PdkLCCRodJmSxgL0kCPYTsG8EteBJX1FmI6kpyj0H8CS27eJwGyRF2KmWqMej108FTJRnm'
        b'G+kx0UDDcw0MMmHXRkd6ZbYiEbmVGBEEaGDcEOGTmJZbNcnUyPUAveQAmQTqoxUR+/C0fI01FEfCIZ0KGRNUgz01aKqDS+7wDpk6+fASOpR6unNd3LdooqmTxwRXnGAv'
        b'1/bVBCr8L38QS+4zSpTaOf9kcAp+dvZz4RQK14jlwUSJthDvWksCw4c0h4jzZJ7VJEKif//insUjKTfXvZZ2Pzjl7RzhkgmLNIIVj3nb/3eL31ks5a4ct04fM01XRMfL'
        b'QRQGlmMGLj0pA2Z960f4992X0JD1cfOAMcOAKQMTQdC0ma3Y4YJHl8eAw4SZ/4jPFJ0BtW17527R7nEbr0mbxVKbxeM2wUL2tK2DOFVi25V+xlKoPG3n2JUlcZBs63E+'
        b'UzCwXOq0cNzOf9IuWGoXPJI7brdUyBYuF6lgcwVOO8RoV5+xXFww6zKT+J2xmTD1lpU9vaiPL56xmDB1f6JDmS96pEtZWmN7ithPwpDYigPGLdwFkQ8MTESLxWXjFm73'
        b'DdxIh6LHzWPGDGOmTexnW24MjEiU+5CmELHDhIHzHMvNlLF1a0FTQUuhgPXAkjNl7XzfOlwS0R/TE9MXN+kWKnULHXcLv28d91r2lK3rlIU1jlcYJAqatOBJLXhTNnad'
        b'NaKatt1THPsLWl1aZ3SmOA5T1vYPOA447e0kx1vK8cahIXeKdk7aeEptPKdmXbF3vhDUFTRp7y+19599xcEFpw6adAiQOgRM2TnREJkFUrsFU1z3fssey0luhJQb8VhP'
        b'zdb4kTFl64IfnbJx6twh2jHFcSZ/2bteWNK1RP6XA2/SwU/q4Ddlx8VDPcX1muSGSLkhqAob48dca1N9AftRCGXr+LQRAi00PXB+gEkD9/sG7lNefsOag5qTXnHjXnHv'
        b'JI45rBYkTts7S9j9mj2aky5BUpegcfvgMV3OlN+i4YTBhEm/mHG/mLG41WNr1t2PWz/mvAFdE+tLdR2mbR3RBC/qKhq3XSjQnvIJGPYc8nwtZGxF6v2ItDHHlQJtYYlU'
        b'1+6BnDy+UnvfKUefKRe3frUetTGf8HGXCES7KTffSbcwqVvYfbflr6W/tfb1tbjP6Al57l3tcacl8iLUbV4X777dwgGjKVv7x0YaxvoC5mNTytBqynfhcNBg0Gvq7/nG'
        b'v7NqzCldEC7Y0ZQ8bWzekitgTZmYN9cIy++beEiUsSnOBE+AQFFgW5AgcsrEYsLebyBVah8oNQkkCzLqbUMpN3HcOmnMNOmBhR3xQGFK9MYseJMW3lIL73EL32efQ/ND'
        b'yP7AxEViKEUvKZPSBkeSAKplJ/5qJyjDHiJSExfxCvSBikwtOnVEOhK2ZMuIz0jJuGm4QGlK16BVvUld6Cf2kRj0G/UYDej3mA+UjmQL1Cd0I/BVrSYtYY44TLRpQtcZ'
        b'/63TpCNmT+g64u/aTdrCMnqWekltvCZ0vVHppK6tVBexBny/sWlrXlNea1FTkTh73JiH6UKbRGuaasQpEybcR0y2kR1ewxoiDXHEhKkLziNuSDdpQheHcxBoPNnNRCta'
        b'aub/w1cVTMrS/guKiZ6huQ1eR5KUCRvvKUvbxyyK4/OIhS5+T5CnwCI8JD2YNWmml6FOTQYrZaioTKk7ZviwprwZ6JM2YxrRZswZI2HJJmzLnDEPluT/rGnzhfcBLBNm'
        b'0v9m7wC0ObRjPqiZAs9vxCbRcHTnj7XUk+VrGQxGOOMJhT+/Jp8v4wuDrbEXlP2pYY0wJovLel9Vjnp5Gnwii009/Tej569HHyd05SZRgtlRkRlENWQGUSYxiWKDKEXc'
        b'1Vn1RrkGxBzKZlINM8bNGiW1WVgd9F1JwfDJ3qUkM4c+UzoLzZPCnMccmlYsc6OZbQ0ldkG+zK41A/N5vo1Rfsdsl+cymYlOoQo3maUui184r/lmI7bEckgqaWxqeb7d'
        b'9ZeYJLGRd963usqb58ohbs3EeiRvB20LpJuEDbuo6YW0/W1+cyAnoig7xzeAs5FfQuxXdIdLcopLckpzSN0vB18iBJRZb58NXTqf2RVVP388N5lRT27SxFbEn7N6vayN'
        b'S5V61sZlk0RMI2bbwCkkFid7wCPonMtbrgBggvVJRrPxS0e5aujcdSKd2LIK4EVwVdGUFIMNK7A+OYW2KaE778qMStXwghoSt4VORBMYVK5HA5/A/hwKngBnthP14k6+'
        b'ut8ilgtWL7r9W2sh7dQTajgmz198UZlBLdIoX4oZEJTADh6Q4FN9PTyWgg1BiQlE7E+XeaVEBDz1S5mtJWWlaaHDs3AF0TTqgeNI7h9iUFQilcZJRCfm03T8ph/yv6fe'
        b'3mbHprwyc4TV/9lC6zinRKGptEN45mrq1upbDCqzdvOIwYoU+nJUdyi52r1ts+cthkSJ4mRa9PNLqHLcFTCgoeuLyO+DzsVFPuXgVHkUPjYMwBZwUNGwB+vd4xJhy/IY'
        b'coqNXY49ZmX9IFlUl8fEucXRZ1M4DI9pxcEDS4im2AG243zh80DRFHFoBX5yJBrcm8Nl0LkpBLvACYWMfmoVODQ8yehXup62lrTCKzg2FJCAuwkKwaEsIW3YBCMrK+a8'
        b'Wm5do+dDPDrPdmPfoD3gjloNC3QQUl3JYarzWQSz7KbPXSNTKodupgn5TVo6dThlK4MKra3OqFy+qaQee2jiK1wl2mo0BC/BXqJt3k6xwKXt4HgAuQBOgUOwk5xNqyk2'
        b'vFQdjFqKh2EVPAXOYY1zFQUv765KDSJzMhoMxBKNcz6VCC7nu4OrxNC7cHkJPoqj2XNImWIvBHfzGKB/cxohiSVshq0yPH8KOrLPWIjKjYkJCB5eDu48VVKAM+7YBogq'
        b'f/dP3zBLVZnY20t8pCWxaMJL9+Dni/44fczhf8pG/3BeNU1V11n7g0Vf6CxKe7jJ9pM4y+a4pX2DKx/+2UjFo96myfq7PYeHykOKXQrOJvps/3PH5MePj72X3P37vVNL'
        b'Xv+7MM6iemevyfDphpLe+x3J9d99c6L3yrsT4ezr4V8WLzne6VsnMUjr/fW9gHu9uvZ5vX6BdV/syaiI7I3TCz7f+NWZ8qIPu+J8Hv3jq8uD7/fEBfi+96FubG39Gys/'
        b'vvzOww9/qxHu8KfIDU4tzcGXdvds7/jg3VHL3WOdNzLe762pPMc6+rbTX5Xt7YYbdD4L9fnLF8uqX6uauOz/1olLr/3Je8Dqcu6nX+84kO1gliyo+K4g1DdEZbLbrJN/'
        b'8PztzQe01f+H4VW8JPB2ctpEq2Rkj8f5YGvPIvW/7NuQIxk8nfHpw86OjKOumpV+Vl/d0LVYPNx2klmT07vs05Qvi75Zofzj7hCOMMgmI2tnyEChNiP5H6Up5/4wvCxK'
        b'94sT19dqfZn8n9+8lTLw7x9uXr23puZCWo9HZH6L69ILf7jY3ebO1v1GL+3WpFS0/LihpGrj3x6Fb9Dy3f6v1Hu6/1wX7PtDxe+zmWobhkuNvvT990Hf+g3Hhg74GSVv'
        b'/cPtM+W29z747b+3f2xRc7a/wNxuXHSyauHghxsjgzrHVL9b+aRjw2c/6v27pNFar9+pXuxc5t//9pYV44vrmrccXvbFH747uZs/+cnRqM5drM9+3fb6F5pcY1pvCM6D'
        b'1hn9HWwAowysb1KjQwpchbdgTzy4FOcjs1TTIQX6VhJ1CrgAT0PhHNcLbJBkq6rD2+QFYB+ogw0kpFp5MLjIJgHVHOEVOnfGuVR4Ra7lg/vgDQbohIJcoh9MRy3rlCtg'
        b'Qe92rIO9VE77d97WMNVwhSJ4cU6+EOKWkRpDe+j3RcERxIRi4BEWxUacP4EBhtDiPUk6twzUY00zPMZLAUfi3V1x3ok2FhOc1ift9i8Ax5+mpQajuG234Pn15GI8HPbh'
        b'xTGqFXJIgxZ4J5Xu8cUdTB5sBH0sT9IzNSsmEKgBmRL3LrwBRDx3lxg4lCxP7LcEXCMqrErQDkcVdZvb4LBcvWnkSW4B5wKwRvaoJ5AkwENFaACw9lpnIWstqAUdhDrO'
        b'iIadvCT37UwCwkd8G+1RPGXKArSxQQfcCwYIdcpAHyRbKWKXvaA+WYlStmSyYYc60T2pVcD9Cpo0cHqVXJkGLhsQPVkqaES0S3Jf5oDVabN1aaDekNQSBJtZpBZFNRq8'
        b'7Mle4gLFpLHcVWhykPfM1qItg3uIIm0HnTwQbTon0Xgf8gS9cBSrs2TKLHtwg2vzf6+pev7RBVNKUUCaq7+SJzNUhIRVWzzroqdwkaiw3mTSKqyCTAZlaj4Dlt00YeJJ'
        b'VC4Rr22SOiaNmyePGSZPm1hNWdl2rhatblvbFDVtZCNWlrAmjNymrVwlC8etfARROFpgLnrYwHPKyh5DZ9vWCaKmDMyEkZ1xori2hPsGLqTW0HHzsDHDMIy+dRFHThhx'
        b'JStk6Fuxd1ugxERq4SWIwCBc149MzKctOMStdPm49Yox0xVT5jadriJXcca4uYcg4hGaj9adPBFPnDVu7iqImHJwvhDTFdOUKFgqXPjAyg693sRSWNa8E2vAVkrKB8p7'
        b'aqSOweO2IULlKY6DUGnK1hF9M7ESs5trpjn24qWStIGVPeulDkHjnGD5ZfyBe29t27lZtFniOKAssR63XiRkfWRhM+3iM+DbpyPSErKFedMWdlN2jhdcu1wlKWc8hREP'
        b'zK0UGjdtYkG6Hz9unjBmmKCgLJij/vpZ4LI1TxI5EjlhHdakIWALcqYMTISqzSFz1WS2zpO23lJb73FbX3RfRpP2tIHxlKF5a3JTsjhGkj1h6DttaCt2kLAnDN0fWVOm'
        b'lgKNxxaUhU2bEyKmoQm5L0y8TWI7Yeg2ha6GTZmaCaNE6uI0qakr+svEVOjbXDllyREypiytxEqiWImy1NID/YUexlnVs8TLJbaSbQNhI+GC2AnDJbg8sSlR7Dhh6CJ/'
        b'QSTOJY6+JzUlif0k6lJ734Eoqf3iCcMgVDpp6Cg1dERkMOThe+Ka4oRlE4YOtGZiGwNNEqkR93uSHAPoGMX5sX7lpxQXIgNJG9PahdPKlEJYx1ejTph3neKa5+oXnuoY'
        b'RrGO4adWpTrqR+kSdOu/sJIhk8FguGIdg+s3+OOlvGhZJLsx6bQN7j5H+RmdAqYYOVdVo48Tago6BVa9Sj1TlryR1itQWLOQqzmjRVB+ZVoEHC8tbD6fILkW4WkGxxkX'
        b'H+IZ9Ir93+hn5GE96efmSWLgwYmg8bKkKc/BARN3OaxqQLfGpiQvWujljY/2W/llGO1ZWlaSX5j33CbQ8USfYl+fDbROX39p/19Vmf/vAR/Lnz1nxWySn7O2gitRBDIG'
        b'9+j7yzMxEjCaCtzPygC3SukjVoszHMSusX2gVZ6MEQPSQIcrjQG7BI+ZKiR7pMFusN+EFQ46d+ffP2PGKsXxZ4R37x446q0PvDTZOWuSClRv7f3IKKjw9FsRH+0FoYyP'
        b'Dc8urj4Y/UmL6t6uGNOJjMrmd3ds+cdZNWPtL2M+/uvXj66zlyw4lvv3nL++N/Z5q8qaD8QP3jWqye1o3t33z8K+18JsuGl7rqjn2n9YqJXEm+57PcPw5CdviPb8+k8n'
        b'Xh88nekZ9E+/zw4dMH7TM6f7x5ovnX8XYrC/+51u9dZug+8+Z/3+DfuxfRFc2g94adkOmaiLpNI2Yq4GA+60rw7cg/PXgROgR9HPuAbcBrSddqs1EGnEa4PuuWG/7tLJ'
        b'57TAvu3PGKYL9IjsBs8k08LfCYgxpeiyCjorwj7a6H0g6BUnDpsrXGiXkzU5I15YPcPIZl8mAsYARXvnhGf/Au8cEwdx6riJKzYHWQjLpQYOU848QaTQ/L6hw7SR1bSJ'
        b'rdhFEjFh4jVt7zVgOm4fKFSdcvacdA6QOgeMOy/Gd0rRRmFgNmbgOOWInzRtSpqy52HDwpmQSfvFaI8Ztw9G++JqqS6HJHQWR76ny1Vw6tRRcLKZ4aK/cP8o1Zm7OdC7'
        b'wht4V/hpYm7XlPnj4H2hKGtmX3iZLeFr3CPG+yrV+cVY//l/nTjg+565jjQlWZvyK2SxR2XpWGZFO52H20fQKsiC7URnmb+1uCAHa11zsm2fuzPICPBsLE1U/CL5fefy'
        b'VnYSQZRWw85IGuXyPIw26HRRpjaaqOaHgXP5cS6QKsVRaq4sfAfHCqEzXWR7ZzWW+1zK3T/Q+G1cBr+be7gjIa1AU2yn6XXD6Z5+hfCDzcpC0zxz6u8Stcq6Yi6bsITF'
        b'6bKM6eAo2CuD0KB3ziS7PEKCmJM27DSXnb+5voRludQEKp69Y8FdeUpNSfJXOPbDsgJYi467iBkNwsPusD4WHrGCN7DGNTZxm4yDxYM+FTCgATp+Oi/D+7p8eoTl07p0'
        b'JlPCjMHlmRsIF/Gmucij0BwGZWg8Yxl2njBwpSPKveY8wzU+MOaOG/PGdHlzczi8+ZzFOyeHw2+VFXI4PK9lIk2FHA5F2WhJWrxsQHLSupJLDKwTTEpKjUoq+Q43V/dn'
        b'ApQ/jfWGA7GQGAnEqZx49BE7FhE0CV8hfeGa/d8eX82oZ2KWz5WMHTHJn4mLrI0tbunyMOZqWrpfGOMw5vZdlRNank+YVlpZDBy+3OsR+fo4RB69PBZHL49nkPDlsjjk'
        b'OFi4SUB99DeqOlp+jznPhAZ/qGUosp/Qsv6GqaVlg6u0eYS/fWFNXocufMlUpUOlowvo2xeGdDtKJ7R4T5imWpb4ktsj/O0LP3wpvcf3hv20jX2P4WDEVyyGdsCD0Mip'
        b'oNAnrJ0MLcsnFP78UgkVP2Ljr1/sZOGHsnpYgyk3DG9sGvOLntCKecJMJjfjzy/pT3RbLOMRKf9iLXnGvsegJ3XQZcxl8euRE1qxT5jGWq5fUegD3xuH7kVfvwjBd6ZM'
        b'aNl+xVTXcsNX7B7jb7QXNobHhOcvk0VBd4uF1/CXBKxWcnEGe2G3UkX5uvLHaH6t9/EDHaA5uAi2eemCg3AYjhr5LwS1WbBfORDWgybQrAoaYAfca6MFBPAAEIOLoCUy'
        b'EnRrgGbQyLCAd8AwvKMFRIHwKuJUV/jgGuxJ1cKoun2wPzgI3AEDMeBONLrrGGzcDoZBD7josROcSQCXg3bC2/CCChwAvej/zQXgHDgDz+dt83GEIm/EoboKwWm4H/bA'
        b'K7BtZzA4BM4jbjhoEr0tKNkYHLKHtRE1m33hEXgbDOcHwYNbos1t+OZRgfFKq3x2eCSDM6ss3UELvBYEbsALYAgICkEvbELVXI8B1wO2usJjPhvgYS14PhsOGMCjUAya'
        b'YTf6PwpPZkbAU8t8N4MjWfCSMjgNrsODRWAQNsHTKfASGKjcCs+COzVgFLamgiYz2L1lDTwJzvobwcsxYNQLHEZ9bwJH9SJBfwrY5xyPGnAdnloE+mtg33IgYsDzSMjb'
        b'C4+DdvT72CYggadAd6U1SwMcB1dhp48bPAOvb1qkHgSvgbosS1AbvRXsz0bVtiaCW9ysqCKbKHg0H96BbXHwxCpTcKkqDI6AK2iYBoKVgXA5Nw31+xASWQ+oO6XCIVPY'
        b'BbvRX8OJoA60ZyBinACtbnB4UYhjsIOhAbyyEhW073Bew4Mi2KtrAOugAFxLLUWlTdpgqFjdDt5FD/XCQdCPWjRAwVbfnMVQtBa0+YBb+rBTe2MiOJpXFgJrV8BWa3Bo'
        b'w0JVeBeMWBqAkQJw1wIczEOPXyyGDVDobQm7s+1Wrg72hC1oKoyA86V8osM7lapptra6cPEOeNVynRU4lQS6zdbAfkSiVihRRf25iqbUKdgdCg+rgrql8KYXGsmToC8A'
        b'dfQiat8w2JeBBuGY+xI0IxqrwBUTC9iISDQKxdq7WPAWbIh2yACd5UeZWBGbHw06VoSBo2jaa4JbcMhoZyga3wtLQa01aIdCd00/eBmN0CA4zVoKzmfx7blAsIkNDnF2'
        b'e4Jzi8qrN+kgkb0ByfwSRNvDxZnp4LZRBjgVCk6BQXAW7OPDdlfYynOCI/AmGGaBATV43AJe5ysVww5wNW1V5RLYVpNSAPpgG6LDbRfUCTRD4KXC+MWoitOWGF+6LAPV'
        b'3ZwBWv2BENRtREtvDzMgETajkwm6B6cX6a1ZU2Ogm7F7o190HmzX2+6nh2bnfjSFbyGZRYwm4W2wdwFaWg3RNgkO253QhDsGRPCiN5rofWiCjsB6PmwuALdQv5bCUdCg'
        b'As+FwOYdiErxYfnwkjOsc0GHyLs7/T12g4Pr1VLAiKk1jlsNL+gtYhfBu5nwChMKqoz5S+F+MKQODu+KAUK4xzIaHF0FauGBbB3QCSTJKWk+WfpOZrAnLFrdUN/DS8nC'
        b'Nw01tCMB1qegERbCXlNQj/hKLR+eX4iGchSxqAMs2JwEmuAgB7YnwcYM2AuG2Hpo9jWagG7UDcyaDmzwwdQF9dj2W1llBo5Yo/ddQpNKUoXmQ121nipaEkO58Di8sdPH'
        b'ELQgOu5H4zOAWNc11TztONhpBi5D8eqVsA+tvANw2GYduJ0YD+6CC2oOoLkUMYXz4GBADhzaChsywG0Pc2xTWJsMhi3QnOuDR1aA5vg4vbWV8Bp633k0GU6vAXvQIrqL'
        b'urXHB/YZOKc4GCWDPYjg11bBcwWIdJJkcIULR5SAcKMD6AJnwGj5BJ6SbUAQjOZkMDiG5yRq9w0euFoeANvXslG9Yri/kA/E2zTQ2mxdsMwNnNfNjAc9IeAwvI6odQu2'
        b'WqC5dAc0oq5dAf2x4OAatF4P2MHbMSEhwVAYB85k66rDA2jOnkOzahjstwenOBVoErcyQ8Ct7dRCj1jYsqWMh4ZtCJxHgmUjuInWTjNadG0b16wrRAyk2w22bUbkHqXQ'
        b'RGpEs7UXtf4kPL52KWKMd3km6WXr1gNxImrhWSiAV13Q6mhaYudTBQ8bqoEbinMWrZCTy8xQO65Vwn3uarvB1ULCM49rbwcixCzPhyUsrLbNAgNJO3Yas9ZHg0MmYE8u'
        b'6thdVMF5xJz2wS6nhSFoAgtVtiJJ+MIG0KKFRrmHowVaFkFRDBCXobv2YCkXdMLTaGO6AGp1mHBfMGIj54xUwPAieNPUCc2HK+CmD7xjWAnPFBptZ29CgjE4gRbtQXhc'
        b'B9HqLOrheXgLDC1DA9qtBxtXWW1C020fHAwFZxHVb611RtvT5VVVlmj6dm0NhoJMtIm1ckFPJVoRhz3QaHSH+SA+14AmJto81/ptWQCbXDZDSU24djVq4D5QiyZzNxjy'
        b'5rhk88EQ4jnDmoawBd6E+zRhfRQ47ZOKpgTo2o4a0ACPuYBr2MwGjlXDbhULB0TnUXg2apUnuAPb1aNcUYcPIiYpRjt3WyQYis5bgcZyCOwtXYVGVIT2xE4wWg0PVQDh'
        b'OpUceDI4N9qD7OrH4svQlnOwHDEFAbrnZFC0SQZsBW1bQCOzwhS0owmOKIgmODi9ejNq5V3YyXIsiouCDYVasCknXcVqPbxkDlrx5PJEC7o7Sg/21pSPo4mdkgNGMa8t'
        b'JBLGLdjPg9cZS60zgVgFilaoM8Ag9h47ihaNEAjKwBUK8VsHI1jrjcgrtNwBL6uAm+BsTrQLOBUB+gzQbnDKDN1+VBu2q2y13IymwikdtBiFPlx4J80jBrQt3wGPW4LD'
        b'cdb+aCMYVkeUuQMPqSwDPZl4sfAZxWuxONRRCPvh6Lp0xC4wB76I+AASQYoWgjaDUN4Kfdi/CjRlRoK9S8FNXSiO3r0GkUXsv8MAHE5JWAV6HOHV3VYRmYhv9KLR6NuK'
        b'aNIH2tZsZ8CTUb7gRqrXDu0IuActamFIFtqa96Ih7jbVQ7Q+CM+ywF092JxmomuONr5GQyBYl8BPRSv3tu/ywAK0hlsyQIsH2Jdg6GkIJQXgYihae/WbwXEnuDeCAWuV'
        b'loGb2eHgRFQ+GApJQsStDw+IWLrLHIrQzEdc8Rx6Xx21FfH/bjioDMRoCTQYo6VyBZHqGGz3wYorM7RI2x3BaA28vi0EzVgh2umOwpNB22B3GGIotdnLq8DB6CI0+8U1'
        b'4GSNEZpT17K3w548UyhELLALcYnGxfBIut5CiCa7AJ6NRpIRms7nOP6oDR3o25lQ/6poXbQrRpqDoRQ0B4fB1e1+aMnfhr0RaLuvhYcR6Q6gfa/T3xpLZSXgcC7HGc9F'
        b'2GS4hLCDbtTUWnA6H5zcqFddkQjb0ZuuYgcc0JyPWtSDhIJ9THC0HBH/sNkO1MU2tIn2ob2zNAN0ecDT8KxpslYK2ioubDaGXTnwRCwa4/NwdC3oyETNvByCTtRnYX0A'
        b'2jLxMr8NT6ahKurWb6rAmxDcs9UMDhUj9nIFHnCIWq0OByy8o5ZbWUeXNzNxMsNixGI6VqAezEgRPDjC2AqPIikieBEPDHuBgQoN5wCVEiTECqNWwuZw1BMgDkNjfBu9'
        b'eKgE0ek65kAZduCgL9znzQcd6M2NYKB4R7CmdTy4Dfs3wk50z2XEPFp324Ba3ko04CPsRYgTngQ3XBcugX3rkJh2At7IQSLmUbSL9aIN+hpETG3fbnd4XB9N2/rwdUAc'
        b'B0+uCEU7qyAnFIjSXJHYcRaMBqK3HYXYg+mWDlrbHaBLF/bEgKPeVbBZO9EmbyvidHtU0AL5f+V9B1QUWdZ/Nd2EJktGQIKgZBSUIFmUHBTJqC2hEZDYgCKigkhWSZIR'
        b'yRIlShJk5979ZnfcpBNWh9nZMJu+TbM4OuN+Mxv+t6qdnd05s/vtnvM/Z//n/NHzurrq1at69937u7/7ut6t3guKIpixOHAoVM9ThXRsElpV7YwEJLJbihpuuGC8S4Hv'
        b'j1dMSYplFqT3w9sMyMHfoDanjmPFCbjpC4RLXuQGCZqIIOCqCHuw1z2f4IrNJNBFd9OLMzRIvCN2MVBvkUNuuhsmI7AiAQeOH4C6UNswElsF1PplGkQEHGUpTN2JSzCS'
        b'bIVXUqBM84IRNppgOzmspkRclJDutB3FiVNYY7cH2mVI0W6HYrUvqdcGwfrU6RMUlzQSdNfq65GUF05hiztWw+1cV5L+qCNUeZHWDGHT3nitNGe3iGQYOoXLuccJl/vc'
        b'1RQtnFy09J2sCNQXlLFW81D4bnKHGxbQE02tNquQaj3IhrrIGLKT1ePQtwtGtFJxNocu2E09vXWSrGE4UaxNANQMU/YwrUTyrMP201BrDHMn8k7qesN4FlWags40gohO'
        b'fibdVdkxUvgFJ2jwhPXd5HBX8OplLXzAZGG3DdnTfWguesLmMNhOciOtLM/hlHKdlLIYJ8Q4el6BeE+F5gWSYfkuIyK5C4Z7NLBFndhkbGRJIDReNra4UARVSXpHRMqR'
        b'5MIH2X9QsZ+gv42ghE7zZHlTqboKTBbT2K7i7RhvJfKVi7ChdgqHsTOTfO0dWSwrwtYoMaxfyKFD3ckniMvc5egDEH24D+sZpP3zyXpYKTHGYUtSjAGynYmoHGwqNSGA'
        b'6GEZbzrdQM3JA9l6SnRGE4FHG0mjPiyemN74xWMXY9OLzZTDkQjrIA6bEXbfOe5VrErCrQfWchthOSfPSwMW1QrJTMolRCka48KdhOY4kxyOV6DtGFVZhKvyOK4ixpqj'
        b'NuzTIlegOg+61ChSuQq9xTgnIl2dcVC2CSZ06sxQ988870Xh04AR2eg0YU29gaWAZNm6h+hmo64W3MwxMT5MxjpphCsBBFvXKTxZIJhbzWGXPGJzvgWO7KT4dhyvXoQu'
        b'SztCv2V5ulgFjjgFiJ2KTY+nkZmXkzlUFJEldClC8168ccYJu0MtyBjmNaErYltBMvfkzXgCjp8g0xkyJR3scSHOsuQE1biclwODhRSH11C8rLtHiwCz3ZtdHe++k+68'
        b'MR2uE2mQxdFo8pc1pKotXmfwXrQ+VgrgJk6L6dK3SN26mJ3nPPMSCnSO0BDPmlmTvdyCptRC6PEqhrqdWCt7HOszodOD6s7BAtHOdqyNIVdRT8ykRytUFW4H77ocQSo6'
        b'iXdL4rOILLYf8zrswkZnE24w7CuxPg5LpFUNYTB7IUMrjUCoU400fMEOB4+WBmCLvzUpxV1dMyx3CM2MxhuJOGklxz0uVyx2DQmSZXgOjD+DdSlYIU3jMIEtZ0PYZ3l4'
        b'B3DpINHTA1DPPXenhhPyITYyDM8Hmv0YMsx2HJKu/y7zsWKXX/K83bGfDiSkSFOplFOXRtgfYngML9jHlSF/cBemuLayyOTIX9nSkUAHH/blI8NhRYF8OqmZ+HQlCakF'
        b'r5NddPkok8ynLykaJwqhzT1SLUmT3FKTPWnDAEmplSXsu/BqkH8YVGV66VgR0izhsH4J+aZ+6A1S900k/G6EnmRsIMJCBoy3ndlJF4q9m4rti/xgXIcleRdhWJyE1UrQ'
        b'L0kiq2mBDS8oiz2KreE0jlVc5rnKw7Q5BHfY57GqozWIwXU7kKxuOSaYk+KVG1F3Zq3jqd0GJoKuWSkmUJ0m/9tC40whTkYpVNmTb22KgsZd7C9UpA0JRGCadpEgp6DZ'
        b'jeKkykJRGDwIIW0fIjdRT0o1Z0gxUwXFZTVuVqVQ7UTsbZVAYob8QR/MmBIXHoVOV7HrWT42yIvVsCPwTIQWjDnjssTGGFdO4kRCkDaMyZcWicMkIoLQJhgSsjMH0GGo'
        b'T+NTTURrgFwMRSnHE6i1ayTRtnitTLLaFbqJxv3U2RHP7YqxytibcooLvbr4WOFIgUwZyWUKCUg3HOEaH2firSMcsTKOUK3fHWd2kdnccbIBdqXsGDS6EyVqoB6VSXSL'
        b'BOScGguoF0OwfiiR+GQL1FlDrzxOZmBjILR6Y1806cA1Cl7W5bWx/pRpipWfAU4qQOspaJWQTq1bqRbhWIpEgiP0r/miCt1urXNMHAWRU4TFTU445xdQui0tFe5ZqsCi'
        b'Kt4OJLO64oJTDkFk2WNQhez0Tq0axe8LUL4dekSEAtDmHZgQniiJTdAlPlRDnnxF1xVvShycCCbmzvIJHYZh0k4HNorSccKFYoFGa03s0mVxnNxd9Z7LZKP39hNhrGUn'
        b'pKzC08ijwpIDdBeSSlXDUiJU55ATH4LxQ2S9UyGXYUpEIV8vDepU8AFuAmaNT07mduJpiqWGocFF1+CSDVHPhXA2jMCmNLiPA3uo2MB1Ex1oExfYFuoR35rwwuWTKliu'
        b'gms86D15OdEG+ovusLRqhUa67MuTM4Sjd71MfNTO4qSO3PZz2J9KxlGeTMg8eyQR64K1dHwpcNmAdgkJs0pJSzZBFBpJwNPotJ2aa4NpfRzZqxdi6gHzFyggqI7Ti7BL'
        b'8ZUnp7Z8NIabpZmLMKaLdEGLM4lkTZG6MJdDmDRAPmU9HReLYNEKpqHew4ZMYwR7cuhLw9l90EVOjfC9kVXUQZi1hrt7cont9x7AudREEnNVWIwuSzWRUHo4lkeEb42M'
        b'utyQ7Gc2gHxcr8AQ79gQ7s7joGYMjJoRqN6Abh9JKBHt3tNEPSt8WGydhfKLWcTwDXyIKQzqq7FTW6F4p0TDTxHGs08QDF+TTgMUpJD+N56xoNsih4b9lwgJVgzJDG5R'
        b'iAt3wk4ymVh9MIsgp+fkwdPkFuaxR0x32FxIbph9IpMgDm+lpMJ01hEXXNBVhwc7E0gVOrRw2NeelYg1jumKcSWDtIYl+uMUPKxJcP2krIc6dhrsxeaIPIK0a5o4oEEB'
        b'WMsF4lFlsJFPXGfBG8a2RVh6O5mT8+3D1ngF7A/IJaF3W+4u2mGVoXMkQGMb9mleLjqgAlUHZcJJ48fZtybAyCVokvUmFYkJhPpEAtorNrCsJeaSQM3h4sXYbPKWOXCD'
        b'j7P0fZJo3krSWYLbHs/SOByOtyNc6sIJK7h/8CRMGVsEESi0sENMw/CAkK2TwGFqG3VkHTcuHQmlRof2Q3O2dkAEXX3VgCRy3w+WfQmDq0WyZt6FrvpF3ydd9cLKMLh1'
        b'DOv/GtvGsg+eQvs+Yza8jY9U4sE9DawJh2k5O5hKlNOBMSQIXNhPWjDtFoPrUGef4Ub62cRNmYyb2RGGsVN0ndtsoZIgjRS0CmYoNMAH5yLsrGi4JnDNyxfGDKFTzXA7'
        b'Cf8aLKSSrQ56ezAwpk+oMm4BnW5YZkpINweTcXg7Grod4wl0qoOgJzWePMJ0DMtPBrA/XrJblp/ugW0OOFyMtfYwtzMKK3L2wFDmQfIKQ9TfO0Rae/wJbmAlFOts48lv'
        b'dFuTMV+1M41Nx2EX7QQJPggnZWsjz1G5T0sBbmfmwAxhVy9dYSZcnmxgIy+C/G4T6cs1GCqhTpOv2o4jDtBaRN6kPTyTtInClnZblRyoVDQ5gFNuGdgRrJMNazBWhN1u'
        b'sOorwXaSXQPOxOyAjSjGFa+qKOAGn+6yKkwbVmTZeZFBNxg5rRMIbYcNtrtRyFVHXcIpd8LwNVKIabKBJdKC9XyKPCc1SeidySms3aSlWxKkXpc57ns6XxnuJeJIZkR4'
        b'RtpJYqlzqnQLXeRtJxRxLgTqU6A9xkYXKLy4gtczlZNwMgoaNH1OnbiAvcFhRnuxaQ/OGqUfxxtOMixrJQSqpCj6Nq6FFpdS7+uT1clv9eODHQILaNOMxKqUuICTB8P8'
        b'yb6veWJrgWsqrpgRGt2lIR2lCKmeYkM5EcHDpFK8IQcxLG7fJGF2pOyDWbxnZkW224GD58nkbsCMJXGR+m3y5B7H8+K02eSzqbh+JJ/G5zoSP2gUwqKGuz1hWu95zctq'
        b'u8m+OglwHthijQh6XbJh0RHuFR1iOU19QOjfqTbFtot8GV26qyYfNQkMacll7ibIvUX9mSVAbNvLC44KYoOnFFxOwXkVsqt71P1+W3dVbDRMMBKQjneR875GDH6yhATe'
        b'ui9KGA13nbErjtS7i3B7VYmNx2HCMJokTlE13NDBymP+LPPRpMamRMYw7IhTh62R6EywEQmp3gxu2xuTebZ6QLc2Saa7gJzOHTHMxhmSonfJRO4zgEF9NyhLhloHYr6e'
        b'BIfG0VYGBBPN6VghhFmx5DL5rQpYiHcmlzIvZjG8Xr7wiBOMKbuQhBuwU09EMlrRwIHT2nhXwbLE1yNfF265wHRoKenVMDm+IezUx8XCYBzTIKLTAAsZ5Ebvp5M3KFH0'
        b'k9Ao9lI7zWauhTDkLtiLU97mMOqliD2FOKmedkIPRrap50OLNl4LOU1tlcNNW3nHMBpRIhokmWWBSViej0tkJt41I3QYI0PqOWWGG/6EXu1wK8jXk00BWEemSfybsKsZ'
        b'FpXSsHo/+WfS03o/mNku5BEcLImOE+4N06gsU6uV27RjyY1fh0EFuJoOVW44ZkcuoObSWWh2PY7sPPkAA/Mn3Q0IVFahKmM3GdsdPei3I0vvJLuYoaC655RQfz/e14X2'
        b'KNeQvADyoKMwilMCOuUKzJtouVHIMQgjvjAua0j21AMbFtr6RGavW2NjKTayoqk9B3P8vF3utLfJAwZ2x+IKuUps22buYY69rtAhjiPVqcE2Cbmm9eJEnN7nEQ0VWYWE'
        b'jTftGWcYSSrWSk4mwWelUxR8PRlm8ok+NxF9u07Smj1A0Fpp7kZR4QpWSw6EpLFv36zBugt2JNw5ZR4p37gyS41pLDtTC4ovwnIEfR2ErlAK0G/DdF4g3o3lHOMC3vdI'
        b'9IJ2S3KaFP0GeOJCMNG3aaXUvcTjOuLJODbkk4mslZlRjfUiAWtItTSeLawplZNGs7a0HkQGe9+GXfVFOrrohgt6RHfjsEUxww8mzLHbzwGa+OTj+lTYGp7qGRQ1rl04'
        b'HRhIlKAiONrNBKtKcolkr+MdX1KBObgtxDVn+SzyPRM87D+GqxYXoYyCv9Zd/mpKx7AtlfuBbYqd7L98AW7CKjupNQgrkdRPMpYRdsaIuO4wjATqYOf5yN0JDnT/rTju'
        b'geWX8QbeMyT/WHMcbkcT4bpnJ5ee66gHM4GKZP2TVPG6Iwm3KossYV0N+05QKFSOM+RhbuzFRgN56uOw0A7vlqYTC6xKLoarnuSYb0AfH+f0hNgdo+evRzozaSmrboTL'
        b'3tHQqOqjQOC5imUBRGkmWFjbj3cZcuGt2LBHVXwEKhNDLF0LMxVxXT22ZDfhPBFzr+wj0JCHLY7HKLBmqei8W3opqUjtbpjZdiCELLlfF1YVYTHufJY1jloQdi1RcFd5'
        b'EleLFbHq8DEyjUoKTUYJeZoobDElYbfvwFvKivw0XaxPyMw4IXLCrhBV3mEdOm8KmuSgeZsu+xpNWMpUDrJxwMUd7Awoee8yWNsOS+xveHcMjSjsu5bs7UkEvncfyaIf'
        b'7hrZ5UBT6E4yjBsU/RQUQec+GoOqILznoUQU/j6Rg57DJbo4oHxJlnrQ7A9dmsJSsrlm+tYEGzY5p85DrykFlRUarhFwTw961F08lc/hlWCsNBTJ450oaE6HXpggJboR'
        b'Gc+lLLpTxM540bjfJwCeITdRgUP2WHNJZEq+mlhQDNW9FU6duRKLiyX2RM5gmCymhdx1jVJ8clEC2eRtYN0JcdIhZ+rbxkW4uQObxUS77+WTtkyd0yOlmriI1ZehlsCc'
        b'6MeVOGgvghtFP2Z/4LpHYzn4V0PwYeemGmLJFxOIZXqbRKqZYyNZQKz5BTrco386RaiHQ/qu5jS8G3j3NEzKB56iqywSTxqWccZFA/alLS6ZStSlSuwrBPZX4PIED2gW'
        b'QJseAfraOewMgQE+bY7Aqpg8zuglAscGMqabNBhNijtwMJjAdIJkfw2bS3ED7ntoYa0z3LfDAfMwrM9if+sKYierUo+QdCp3EazUKgtwXLyd9H7hvAlZ+sreiFxSuCFN'
        b'R7q35j062LbT2Aq7dx0m2kC24UfasK6VjveUscvdFIdVKHKsPA4VfrjiAxPCYkKYFuJArYTOgwyp/Koc3DIMhHYlChKG96hBv+9e6HQixlCpF6WNozv3yclhzVE/rFXC'
        b'K35HCFvu2xPNqnbDWbU8vOegHOIIA07Y4nvAh4QyD10CsvohgvuqklMm6uwK1RUCghUoNyFdn+IRObt8di+pW0skVCpxWrEiIgTfOLOL4KAHq3NJaiMsDNzbQ+SjJS0d'
        b'Bl1Jn9k5+Bas08V5Z4psmk5DjRwMpJvAqACmvQ7gIhufY9lRQq+F0HPk0x84yRGzHoRrllhhS4KZ1oGBi9C+jdSyxoz9NVm2VM75dBS1fNNDFduIPsidY3lQheb+HAr4'
        b'iNFfIYRoghFN7DykW8w+XHGMJNcFqyfPWsC4Haz5w6CVLHSaEsfqjoOxMxT0TFkQBA3aiYgEkfd2PpC7D1aDd+fjgAV0BMOIzZ7DOC9LfqU9yJRC21s4t5e83BhrJZ3H'
        b'NA45EdGesMeNaHPCtvbIU6qii1Hb40l3arBsfyhdpmOnp7HPRYZoZs0ZHDuF1VYy0hmkCdaXfJE6MQnqedZKl7gZJG929rfAUSLjc0mawfccrFnxX+VHPARtIezckisp'
        b'4jyDbUegTHpkNKQwhE3NxdtzHBsZEtc4tnBHtGhMWtkFoQKG5xeHs3TSKVfpGxjWPHdI58lc2Tw/dXg7nW6PvQVT6IPGEPbdDI55WE6HtLGHa+wYiwP1oXSOG1H3dQYb'
        b'ZPAad0QbFs+8mlwjCV1l8CaRO2qOm3kbxt4YrLei0yJI0JMMDiTZSVe8VikfxPowdobNH8YZbEqEm9LMohVwJ086J0d0sY8hBjqAV6x4XP7Fw37FIcHUmE2KBYM1xTs5'
        b'kZ5QIu/7akqOJN/LTsp1wrIVz597eyi3NPc7wXzuKc7Go5m28lnZjBWf232dJ939SJKt/Fw9Xpo5MjuIe302M7PjnPJKxjEm3EomnJriFvJm/GL+oUzB7wmv4tCmMuqN'
        b'yPd8tAzfm8t6t3jpNSXn+ndj56eTftRubljwzfLx2GCLFYuog5aSoKP7IxSfRNn/sfyyo128hiBly3f4w5erH5ekeVxOS/WxdrSM1m9OGnuj5tpDZ/2W/M7GoM7mjM6m'
        b'+M6W3835/ULsqyMOOvtwbvKP2hvy+3+i+3rz3iMvhZ8FPPie0sHS9zNnfuZQ9jyTd9+5fvPMkv9DVJ046Kv77vs/V5IXPv7ZnZOyz5RPxP/+Jza330/6LP6hw+P6sgnz'
        b'77zzx48yehvcfI46nRKMfkey56evv9gdve9P39XeatpdrF36R6HXt/1KRz6zOqvpbLPwvfwfL5WUfeDSFtHVOcjvs7gk28OE538NfIIKT68lKFoq3bx3JqNvn5HM0nNh'
        b'ntxDDSPek2WBf79tx40GsL3S/TOz75WrRKqunt14qmso8JYTfxbWceDaW6vzjmmPnhb9+vtvo8frVt/9Wv/rbr0/Px86/+3E0q/fKan76JHOr/9cNffh0H7tlCdx855R'
        b'H37g9eG50kyPCqvtqjZr35XPc/v+W1FXQ341W//LkUvqaVAQtaf9obA3oC38vx/aFWXfGPjOp2aSmEfvv7PvzLfzf/eB5YGUjn1J3+t6/YCL4zmTj//09lnJ3VMu9W+r'
        b'fGPHk8fXDvxm5OnY/fiCyIiSFd2sBqP3fhL6vUiHF9E7f313zaXlk29afdTT0tvv9YcX3j/RfHY28ufqb3584Vevn//1Ruh7a7kXfp7OnKwIm9D64ORvFly7PD0P+bkG'
        b'3Cr8dvTWTo+H9T+OfU3tp29b5EO1a+1zL5movB8G9Fu+JXwkyE32fv3Ity4EVag5hufzfvTuwvcTGh677upK77L8rdWFPYnvuE9c9/wW/uTSE+es6XD756aGSvuE39hM'
        b'+cbtKyPpXWnpbb9I79X5MCphyCJhRDthONb55P3nt88sLO784WW/jYbvP2v7RvdfzH7357emL36ispjkaTz/5M/RHrn1dX3faXs4pXvzPbtWdwfLc4nWL3tjf3jS+oPq'
        b'UcXbRbobKwqrF7Xycx991v3CcSu89GXGp96WKfFznyVaKXILIYwItCnsDGWByB672QeNr0Art4phuzPUvnqsmAKwub9d6HC+lEvzCM2nL3CvREvw/Iq1t0kwKF2j24Bj'
        b'iUoSFaEKMYR6NUmRMjn1JT6DXfGGJQIFXPPhqunAOE6w1ZCidq7qOVw8l68ix+j58MnttKpxKejgDp29UHBWOb8Il9SgDq6pGcCIgooizqidlWWsVAXkh5eEL9inuXHY'
        b'duff1XxVDa5Lm6a2rsoxYQI5WBFAJbcOOWwv1ihx1dx92PYU8I6MQ3g09xS1ZQkOF8B1hXy6uwLylLVfbm/3XmoN78nBA69Sab68Nok+ueX7+786Yx6XL28Dlqwiv/zI'
        b'rcL/Q8V/fOnsf/bB50iGW7fr80/+/uFz0f/4T/osvYJIlJWblCoSlfx1i3tY/jcUSP7lL3/5YxmzFcNjVLS3BPJC3XfVNBod6891mNaVdhb0OfYl9e/vLhk92nV51nxG'
        b'smw6W7R8dLZ43v61Q9/UwMA3HUN/oLe9w7EjqXN/t7Av+LGe/YzuYz3XRx7hj3XDH0VGPYqOeRwZ+6Zu7A90TPo0WnIeqZtv8Rm9ON6WIqOh1ejbpF1zcEuO0fWsUXqq'
        b'bfJoZ/Bj7eAaRdqjZ/1E1+WxrkuN8o9NnZ6YHnpseuiRwg5u2/2xqTttfyzHF7q/VFQXGr00lxfu+UTDUKj3iYcsbakKhPteKisI9V5qqQsNtxi22MXoG9SovBT489g9'
        b'bPkyUsZYaLnFUNEofsF+bB3iMYrqL2VyZYRuL5kvyo+48jmfDm5xB7dSZWn7qVD3pcwlPl2L+aJ8Li2prp70BAH7feugAmO445GC3o+Fatxpp2WE+p8wbPm3VdnvW1HU'
        b'tt5LGTOh+wuGCu74Fvv1ZTAvQVbIppL6io8X0o+tEkWuCyfkheYvmS/KZ1zZZ/ic+3zVFXZzy0eNOyFSlq36RbnFlR1Zz7nPVydwBzKlV/CRY6t+UX7Cla8qcrv9lWN5'
        b'QpOPGLZ8KZHxFuo9Z6j45KAMT+j2sRxPuPOlnIpQb8uEa08kQ0PCsOUnXPmqJXZz65AsVyVaTmj7kvly+RFXvqrObm75qOyWF2xF8XZRGcmTbltSGfNqD20/y5CjcZHZ'
        b'ClSwol1xf1fpS+WzIrlDAgWZZyEKIQpGMo8U9J/HqTMapjW+72nvbuT9wNp92fextddy4WPrQ2+rm/aZPlY37zv6pvpu0nMdy59qm/5vdcz+tTqG/6zOM6pj9EyNbusP'
        b'W36FPJ4wiPeuhvGQ8iM7/7dMAt7SCHykHChd+dznqxeqyHxbUTPU6FVetf2S+//sHcv/HxXcGp1TX5kz4V/BWclTdmXKXyHW5nNY/58y5uUxHo+nzq7D+8qCXbOt/u9k'
        b'hWNH8jUZOV8N5jUNJV8jfsaHh6MFBUE0ju38m+LGN4L5vupVFz7xnDd3qg36Qc3B40eE9strlfJvXFT4oNLsLV3h1yt+ePXTY8XaxtBe+Ftzk5HPtv4UdvmdE2//snHf'
        b'm2+YtNjOvWHa7vGRVV+jWeaRUOHwzaMtCTePPbMIntJqLdac/uAN9TNnMu++ubRoUv186414l5A/NUw4jNqddFnpT88fSS+YHznq9mZS7OpvAxsSH+63EcllfatxSpz9'
        b'9fLkip3/1aH0X1efd8W0Pry2/91Uv/85+06z22fW7kX2T9+6Gvv7T38bk/1u0on3z0fHfuIa/e70p5KWn/78cmKPj5+B0X8/LSu3D33xqFrW4L2nr9kbLut9Db1KlfPL'
        b'/ASusPfgIdfXrL675yD/lzX55SHHTX3rlJ+kD1Qa/OADVbe6N0aVf3jC+Ze/WNer+VX6/hXPZ7+1dR+7YFTfUN1ZvPf15JE/zV/65c6bz5Yd195Qk3XOPOhea2UszfK7'
        b'4eJtyf5ij7UREVy2EHlGCeZkcJRC+n5plVvHuFeQ4izVsXKPYNfDbMM1PvQTob0izfFbh+vmUA8NUHFami+ZnUWWZ1Q1+Dtg4SKXhBpr/SiGDgqzDpNn5AS+sCajcCjt'
        b'xatwuPws1jtQ1Hus0JnBQbiJi9Lk0w/SscUGb1jacfmbZqGZxwjtZaCLYvhb3JI+GA1w/TwDMzTCmCCcBzNQA43ckj68hwu6IUFquGQbZPeqlirW8cPjcZoj7lB2JlGa'
        b'Lwf6sIrLjK2F1dLMMOuFMtKWw4IiYAavWwUJGA1s4cOqDjZIkzO34gOsCgm2Dd/vBDf38Bh5bJaRwzIc5pKs6Oni/RBHpyC8HrIbal9lojblu+OIL9c7e5J7M1shKCwA'
        b'BqTHVfEufy+76ITr3VGYhCGst2bT6vAZe7wpOMqD+8pQL+17LXRgB7uaPMyW+lqdLtjLg0m8rSZNc71csNPGDq9TUHIW2gXZPFjGW9DLZRqSvcj+MnWdIhaKVFqwLSIo'
        b'jIQgYAwuCuAKDsVwt38EW2A+0JaGjM1pFobXeIySlQw24qy7NNP2CpTB+HGYK/ibGopBMjBjQcPHvqtGyw+uKrGLYnBODe8VkAyW8nAhn8IXFYYx3CmQx7uwIB3oeqjE'
        b'0UNQzS0btWEbZEgPu2RwQEbCjZRxoPDzTOLa/Fe5xO/rvWDfmoLVjlkhMGVJQ1y3vZC0j8uVHxEE1x3C7azkmIDD8qU2J6QJkjZCDZRwBhcoUrPPxiYGR3ACqjlxusA8'
        b'm0aOTeATQXBUaqrDwyGcIWFzUdr0SVhhj9phjcN2LLf+fMXn9iIBVB3EDk4j9NlndkjqdWyq+tCQQBlGuEuGfWtJCnf57IspZ6DCJtjONszOnscoa/MVsQ6qpDa0qGwU'
        b'QoMSYo+1MELD0IANdPOaTnzsTSCNMpJqO9yB8jibQFtrNoEAOyTYyK4aa8YlLhm7cxB22bBzQSG78QGDHRpYbuX9n4iG/uPe7v+Sz2RTkPyDsOXf857sqlXWe2bkZBS+'
        b'ClC+xbAByp/LmOeGjKzmUxWtJyo7Hqvs6Cl+S8WyzP+pQLE6tDz00TbTIde3BbbvCVTeE2x7T6D2I4HjY4HjjwQ2tP35f50fCezfF1i8L7DekpGT1d6S4Qv131c2/ViR'
        b'kTV+X2BK576UO3pA9jDR6f/142Ppx1ZaIWmoVlnEH16cpy11g48YHtuo3hafPj/7mZIO7ZDVfqquVSdLu2S1Py2wZlVUSc5Pn0F9FT8rPu6S8bNl0JLHblvx2W1bJb8D'
        b'fHTjUSmlZ9ab/CxxjqSbBLIpW1iUlyXeFGRlFBRuClIzUqjMzRPnbPILCiWbssnnC8UFm4Lk3NysTX5GTuGmbBpREfqQJOWcFm/KZuTkFRVu8lPSJZv8XEnqplxaRlah'
        b'mL5kJ+Vt8ksy8jZlkwpSMjI2+eniYqpCzStmFGTkFBQm5aSIN+XyipKzMlI2lQ9LF86HJZ2hk5XzJOLCwoy086Li7KxNhdDclDP+GXSTwmQnZ3EOm4N0UyWjIFdUmJEt'
        b'poay8zYF/kcO+W+q5CVJCsQiOsRmPdnclp2b6uYifYWlKDXjdEbhpnxSSoo4r7BgU4XrmKgwl5hVzulNflxY6KZSQXpGWqFILJHkSjZVinJS0pMycsSpInFxyqZQJCoQ'
        b'k6hEok3VnFxRbnJaUUEK94LlTeHnX6g7RTlsEtIviC83PKf+xT8Tky+0livYRL0FMZzC0h9RPjUeL0uWpXdfVT7nyn+b8hnJ+doxr9kp+bryP1VIoyEWp6Tbb6qLRK+2'
        b'X1HPT7e/+m6Sl5Ryhk0dy2Y8YI+JU8OtFLhV4pvyIlFSVpZIJO0Ct458kwjkplxWbkpSVoFknY0KTEgHpWvPuTXy0ukEDxqroiyxl8Rcnk3XQP0OpoJ0nMd7JiPgCbaU'
        b'GSWVMvmPBEUHeFpbeUXESbY9UTB4rGDQEfy2wu5Htl6v7ULLx7bBTxXU31XUeaTr9JbivkeCfe8y6o167zDbuWv9H+r/YJ8='
    ))))
