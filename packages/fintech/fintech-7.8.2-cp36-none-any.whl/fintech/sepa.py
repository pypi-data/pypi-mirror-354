
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
        b'eJy0fQd8U9f18BtatmTZGNuYLbZlywOzN2YYbxsPhhmS7CfZAtkyGmwIwYBsjIGwNwTCCnsTCNDcm6Rpm6ZN2rSJMpqkaZvVNv2nK7T/5Dv3vidZ8oqT7/vsn6/fve+9'
        b'e+4496x77nm/Z4J+OPibCn+uiZAITDlTxZSzAitwm5hyzsIvkQl8PesYKMgs8npmqcKVsoCzKAR5PbuRtSgtXD3LMoKihAmz6pWPl4SXzCzK0NU4BI/donNYde5qi65o'
        b'lbvaUavLtNW6LZXVujpz5VJzlSUlPLy02ubyPytYrLZai0tn9dRWum2OWpfOXCvoKu1mlwtK3Q7dCodzqW6FzV2tIyBSwiuHSe1PhL8E+FOTPqyGxMt4WS/n5b0yr9yr'
        b'8Cq9Km+YN9yr9mq8EV6tN9Ib5e3mjfZ298Z4Y71x3h7eeG9Pby9vb28fb19vP29/r847wDvQO8g72DvEO9Q7zJpAR0O1LqFBVs+s069WrE2oZ0qYtfp6hmXWJ6zXz4Nx'
        b'gxGo0vMFlf5hZaVh7U6aJaNDW8LoIwvsKrhWRHLjn+fIlSlvs24u4xkMl/hKtx64CTcW5s3GDbi5UI+bs8uK1qNdyQpm2EwZfoQujtbznt7waBx+gC/kZhuyk3Ej3pYv'
        b'Z7R4Kz9UX4D31nniSFXbBuODcB+fxJez5YxMxqLjeYs9OnKrHl9LT6Kv5WfjZj0+gp7JljHReDeP7uGzWj3n6QmPjUaXnLnpI+CJXLy9cGpvqCVyAD+hOMvTC+4mL0Vb'
        b'yd3sfLjZy5xNGnCZH94Hn4fX+xAoB9PRTRe5DXDwNpYJ74Ofz+bQVbxZTjubijaii2p8fSU+FolvuVAjvlOHby5DTZERDNNnkEyJb5r1LAWG76LrqAk35eXkTsPbeIbH'
        b'D1l0GF9F++ABggXVGeh6LrqUAKOxNRdvQ42F0Kps1JxakIzvztQrmFkzlWurVfB0PDyNdqGrq/ENaFdeoZyRr0XHNSx+Jp1AIx3HO/F+tC8pJ9mQn5zCMpoqdD6WD0e3'
        b'w+B+X/L6lWh8PynLkIgb80jH1AJ6Eu/k8GV8Gl+sZKXZ5+FvhH/2dxKkDEVJ5v8WKb0JXr030ZvkNXiTvSneVG+ad7g33TpCQlW2IQxQlQNUZSmqchRV2fWchKqbglGV'
        b'NHZAG1S1iaj6dqaS0bhHKhidyZ41JJWhhSUWjpHN2KME/DXsWjRcLGS6q5go0zdyxmTSvKofIxb2nSdnVDETWWaqSXMkuT9jD4fCn1f3lP09mpn65aD+Cf/D3R6+IG8f'
        b'Yw8jTzsPsFdH/EwFT6e/mx5Tul4s3rD+q8g9hWv7cUUfsN/EX1I3Mz7Gkwo31uBtk2HJNKXOTkjAW1OzAAHQ+dKEHLQbXcnHOwwp2ck5+SxTGxk2Cd1ARzzT4Z3SuGqX'
        b'27l8mceF7+Cr+Ca+jm/ja/gWvhGp0oRrwyLUaAdqQNvS00amjx4+agS6g67KGPQQHcMPF4ThS3jjek821JO/AN/MzcspyM7PxTtgwW7DWwHbG3EzNCfBkJiiT05C+/Xo'
        b'CjqHLhZDJdfxfvwU3gv4tQ/vxnvmMkyPtIhodMsSQBoy9GR4epB5SPNTMt7KS5PKNcA0ruNhUjk6qTydVG49L02qtTX94dtMqqzASei97e7LfeSusXA165u/5JpfrfjE'
        b'VG29duqiJYu9viT+evzhJ583nLFuKd+iPWP4o/blXlusZwxxO7PS+Co1E/eReurpx3q5m67N3XjbtGloP0zCVhgFWJ2ycSy6pkcH3KQXg/P0SSkwNo0GllGg7RzaoEwu'
        b'RM1uQqPQHXypOik5ISuZg3uHuGHoQfJKK30Nb4kZlpSMm/OGyxlFOYuvoBv4ksPiJn1ZiC/1wU1Z6BJwrnWL5rKZPUv1rI9L0Ot5J+lvS3KeeRw70ep0rLbU6qwi80lx'
        b'WerMk328xyaQYXApyEhND2ejWSe5dJJx0st8YbXmGosLGJXFJzM7q1w+pdHo9NQajT610Vhpt5hrPXVGo55rgQXXBNudSpLISULqm0FgaAmMh1GcguVYBU1FEg1YkJEE'
        b'fWQZLg+dRAfY6VPwjcxKrhUy0PlLJ8jAUXSQWWUBdOA7RYc2azxQXQAduhfQtgDCn0PHXHlyBj8wMvg8g87iXSs95NnaQtSYCzdM6CarZ7AXXbaLr3jxASDKN4CE9nCz'
        b'cgbdwvvQU55Y0rOn4tJxE9yAtXKZncngvei+xhMNd8bCGrqjBnZVqGW7Meh+UXdPFBT3qp6aBIUOBzubwYfz51DAc6ZzSSkKBl+1sgsYfBY9ix55YgjgzUZ8Be+ezTDT'
        b'8BZmNZOvR/vEAW3Eu/AhvBsG3oBPoe2MAR1GO/RhFHKep9sEGFm8GV8Lg3QVuiS+cw6fwg1ryJ3T6egMpGgLPkXh4HsRyeg+VAbsYMcCkp7V0YahcwUOTG/cGYCPQjpm'
        b'kfjChhnA0+7DQOOjaFsvSCtLKOxY9zhMix+Y8WVI1R76/BB8GB9G9yPhxokecyFBFyMpAHxhLrqMT0Gj1OiUjlHX4gZPN4JNeEN2CdQzDN2UM8Pw/jD6dCI6Cn3YDYiX'
        b'lo6uMmno7DgPWUMCOhEDq3O/kkENeD9MMWOEMTxGu21dQ6bOhW8sxyfcgH/4HDvYvZpShgAx4iQcpAhDlnoVs5ZZFLWOXcs2gBjolK1ln+KWyQie0WUjrh3Ox6Wk+dhK'
        b'PSuuDZl/PTwOn2i3udyVjpq6yfNIlaR+BeOZAP/S1qfminKGyLSz8B5Y8I0gCRXgbfrEZeg2n56OmnLRLmi0Gl9k0PP4nhpkiWdkNlnves61hwB4++dDtj/QbiyKqf+F'
        b'vmHhS8dfeOH1H3/JHmgO4xtfv/TUx+Mb1Xzeb1/EE/59laut+er0pQ/39gp/OnpbvOvlTa4z7oVrFw1TpGasPvCbP8129bw560aVdeXgf9he2fP2zpM//mpejqv6pUFZ'
        b'KXfeiz26PL5xzoK8F0/HNK29v/rFvfnHlvZ/4uPL79b9p9/6j6PdX3x7Je6jZ/unaYbue3OwRCTR4Sp8OilFj7caoM/oIrCIK9wIYEj73UTiKMUPZoO8gRuyK/DevAI5'
        b'TPs1Dh+NW+QmaCIfHYebDCCHgRSoWFwxihuUyrmJBIXuoTPAvwj3w1tBxsKN6GKOnOk+kscH0Ta8C23CNyg1zeiT6yfPxv4SgZ6BNrehl3pZq4JWU+hTW2orHYLFSIgo'
        b'JZ/9CKJkyVgZq5J+ZWw4/EZx0WwUq2HjWac2iKyyLl94rcPoAqG+2uJyEs7uJDSpbUs4J6ELzsgANSXVZAeo6XPRwdR0IFkzF2eh+xIS4WfRKQmRZEwvvEu2Atj7/k4I'
        b'K+WyIYT1e/LZwDoJENYwUXgatyKaGUwx/O5iHDZXFIluFWcxIBKmpc28VF2dlMpk0tLxmVGMDkhkWubrs/bIx4mPriwLZwAJVGnLMwY9mVbG0BUfIUcXRqQBKLQbiF52'
        b'hRLdtE3pG8m6FsDNuT/f/7npM+DmeeZXrQn7Ptlw9eD1+VuF4gP1PccDYz/Uczz8bzJssL+sfdma2W/LQHXDwvDc8OlJuwc3vLQThVc0XvvXiF+nu9N+u+FV08+s4dYP'
        b'XgUCPTLm09Teeo6i0+QqdJmwbbQHn5BYd7IWHXMTsb873oiaklKyDYn6FBC/cCPDxOtkMrR78ZoFEkn4TizrVlltqVxqrHRaBJvb4TRKrJpOfHk8xbUoSAG3ugXhFl9p'
        b'E3zKSoen1u1c1TlqEZrs7B5ALVLLggCEsyGoZSDr7EI/tB/wKguUGbS9MCUnH8QZ3JiKYEXlAcM4zzKT0GEFPoMPTQmR/wNIRkU5FtCsRZRjKYp1LJ9XB6MYaeaQNig2'
        b'SESxYeXdF7/JZMGVaWLfsLUSNk3J7TZvPDeVYepM9pnDbUwpLX2tSLZyAQdLa6rJfnfNdBHHYqq4xScYqosaJunGioVDajUTrzHQ8CJT3h/mVouFnDxmfDRbRF5feMIj'
        b'YfMnRX1Mu7k68uTaQ+G1YqFl5gDD2/wGAr6PrfcEsdCVO7hORTB/qmnagKxpYmGjOWF5LHcCgJumHVzgEgvP2ZMrYvmrpM5pb65aLhZOyVHE/4oFDU5n0jyx0CQWvhOt'
        b'TvwzUf+jTIZxK8rEwt9EDV38b/4AeXKamZMUkSfHJw3+CXuOPDkw3yx1M8YS3+8ubyLQ1z6ckiQWLhsTFjeK1ZFCe0mGQywc0DvSfZIBiTnNlJdcHSYWHpneu/w3fDWp'
        b's88dg00qrOkvXGFXkif77MpMFAt3zxw07w98AxnkiuNTFWLhwKQeU18CogLtXBg71i4Wrp2aMu8Wd5e8PvCFgQVioW3sqOoI9pdk6IrfXSy1U+gzYmUm+wqpM92S30ss'
        b'/E962tjH7I/IyHNL+s1m9IOpDIIejUSNRCEdDpIAvjDcbqCkpARfRKdHAEqlg7AGKo8TnaHlAr6J6kdwRIdFN0tG4I14HxVB8LMjJo8A0Wckg65VjUR3RbEOn5xbMQIw'
        b'fxQzHd8cBTLVLSrW4QbUxI4A5B3NLFs0emS8+OwhM947ApbHGLjfbwx+ttJDqHxuxsIRIMKMBUlv3di6bqIc9BAY3Hl0g9BRJhxfGtcvklaRgDaAuHoDWj2eKUeHxhcP'
        b'ER+vx3snk+UxjQFB8OA0OTpIq+ZwYyWRNqYzjhXTe08QW3Gwoi8R/meAuq+fgS6hLbTFCwehjS7oyEzGoZ6JzleJfd4Zo3FBLzKZDLwhEzcXiDXcLMLbXdCPWczKSbPQ'
        b'MXSD1jCnwuGCfmQxZnQoC9f3pS2LRPeqMelGNgwbPpUNrF6UGK/ivVGYdCSHAdpyJGcIvkxfiMIHtfgGtDmXMeKjueg8bqRAZ8JTD/ANaHgeU7okj8Mb6ePd8DHQK29A'
        b'w/MZfMuej3ZF08fNI0AhvQFNL2DQxbkFFnSCdohHx5z4BjS9EKTtAYVVxbQxk0A5PYhvQOOLYJLQvqJp6KGIOlcz5xPb2mymDJ+fjZtBjSbFBYY6NbS8mCgP94tBYD1P'
        b'B0CHHsjU0PISZpmuJBOfoxDRIXySV0OzSxkHulUqVNCJWZQUroY2lzFPrCsbjC7S19E+dKi/Gpo8h1k5Zo6jlvZvHd5erYb2gpB8Bd2ciy7g50RJfAveMkMNLZ4HOsac'
        b'eeh5dJoqIGgDvgEz0gSX8xkQfc7Md0kjjp5B+0FuaoKGlzPQlQPlgogQPdDlUaiJI5wAb5yyAO2OoqvpTf1oQx77Flmh0ZrcLMb+72+//XZ5P1nOv1hKRTWNsfFi4c+S'
        b'ZbV5jEhaf540lrENWP0C5/o11PGTq5NqdkwqmJYRs/kXR3t+HSvbM6yeizNs2B5xlQ9PuDrh2srBgycn6A6e7zd0+qyLi7xqZ8/S9E27jny2/s7YP6kTs1L2nH6tV2mJ'
        b'bMC5R3tmbu3z+YB84fzHY1V/fUY5z/TUoSH75pv3/uvie4Jn8tUXhi5Y+3H3zTVD11q9+xY9/HLvg+NPK9WLl/d/5yeZi8Yrr43YH/b+LPUf9v624Nox3X880TuXnP1F'
        b'0n/CXv7yf77+84sv2NY8sNbtPz6Gfe2tT760Lhv9uClzxMXo+ub5c7a/UrDxwCt/aqj9w/9OeV05fs7F90CwJex+DTr9BAinBcQUtgNUfPTcHDW6wOHLI0GvoIr8tWlr'
        b'kvClIS1afjK+jI+5ieCIvOgs2gYyGyjB+dn4ueQcQ7acicZ3eeyNqqSSMXp2YTRu6oZP4m252UTjV4zleqKj6LRbR0kJKJiHXehSVkEyOuhMIDZNvIOH5bCTR1enWfTy'
        b'diUNvj2xIEj+0Eryh6fSSKRdKnwQGzMjaFgZR0QPFRfDkt9oTgZCQi+S56OoWEL+FKwzxl+jngfBxFPZmTzCOmP9oOl7AuMXRY6F2AyIAPDEvDAiiPREByRZJB8SojbJ'
        b'GT3eIEe70UN8qhMZhFggmSAZhO26DNK+mKsUZZBrLk16vCgtaMYXd5dkkJUx6or7HOXNeb9cvJShK3CcAj9HhFd8fBmRXyvQdXzOZnC/zbmIbe7W+FGfm35aMXtstfUT'
        b'4TPTJ6Ylohy7K8scrvif4gMl8eUHB2cYtsRYo3KPPL3v6fprW9hz24f0PrcFyNzzRyOqh87Ss24yoCPQBmUSPjgmCPPmzPOLoJ3Mfi9x9l1up6fS7QEZ1Oi0WC1O0HxE'
        b'TNCQwXiC4VSg3lAhNC5ormUueLjzye4RmGzy4sbAZG8ImezhUFKDzuYGxM7UFH1ifoo+Occ4Kh81pubk5ybngLYDyiJ6Cm0Nx0/iR7ZOJz5U+Ox84kP0G/LDtZl4hcgF'
        b'0ZU4Vu3kw3KIBsagg+wTdOYfFoxkTtipuBL9Uu8yJtM24UQv3jWGtCus1+emVyvI/H5hetXJVeSZ7daPzQlzPjF9xlwvPgDKSqmorEz9r0nxmpv59jfhT1XqQPcg49Ud'
        b'7YmQTIar0FaRnjTEUnKCb+JTU0JUD3QTHyXqx2L8vEaaoY7nPb6V1hE66+HirIepWKKAOOOD57zyO+e8Z2DOyYuNpMIoOufM1yGzTpRRvGkB9pJpx7sq2igcwfO+Cp0P'
        b'ww3L8NVOFVu+lcWwc8V203cbkBXiiv9ghJYBDlD9p8mmvP/mSOLw5x4Z0SN06ZkmzWdpOrFwYRFPWpYwJMxk1+awjM1+JIl35cGdQ9NXXaj7xPSF6RVAh4uWT0znzK9Y'
        b'U9O5/+l5uGdx/I2eG+xnYoaGbSkYqvu55iMlU+ZJO5s2asTWEe70sHdi0jfzX7+gOfIps+2rqNfUMYAflPNvjLcyLnQhL9/AMbJcFl2fga67yd4G2o+fRkeBWeHtqYX5'
        b'IMVlo4syYtU72qNYNtqATndVPY2otax0GwWPxSiY3SJ2RIvYEcmx4cAViBmEAz7g7BXAEplPRh72hdktZgHeW/Udxg+yxefsE8AaUtGOIKz5KkRHHQRlU0B0O4ybyCYY'
        b'aizU56PmwmxDNj6SLGeG4Ovy8lrcXMlL8yoPRpPRIprI6PaU3KuwKiRU4alxWQaowlNUkVFU4dfLOlJQFW1QRS6iSknUiJg3GFFNcXZbK2LFlmJ55u95Ki4Z7pRFM7Yd'
        b'ows4lxHu7J2H+m4bF/6jNI3M89bMxR/89d+RtpJeXHbVwpy9h35+ZdDCiJ9p+fUJr/zkkw8H11uNXK8+zsampF8/8/pZ27lPF1SNyewb/e4bRvmQO1sm9Bm8go/9T5Nh'
        b'5TXnG8u+/VfPeJ06ByQXar4+jhrLqO1MyXDoZMIotgx5p1EcKsBb0EmytypnZPi5cLJ1OrSQijsDh5GlCWuxCTcXsln4GKPC2zi0CRSdZjfdWnw6FW2Euw2pQKBkLrQn'
        b'n0WPhqF9FGRv/AzajZvy0UUgqGhTBDrGzhJGdiakKDq81RopNVWWVjgZL+JkT8BGkFK0gJPhrIbjOBUXxzn7BjBTTjAT0JF0z6eo9Lgd1mBi1u5iAIztT677hWIpqfRg'
        b'EJZ+GheMpWQNgvR+q0duYXIQisqZ/nhnFDopw4cnot3tc7CRjCS6kM1Txir/IVwsAv5i22BofxFDix0/ZfawUxM1Uabsz8bNEjF01AIdM5XJ6qOuMy2c55ghFn4zXwUy'
        b'/peTZCaTYdlct2REqCRGuleGRESZ7CcrJGtF6jBi+fuAi2RME4fHS3YNxbw+oOK+opIVmRaeLyoUC93ZI5lqZmcyN9Xk/GSaRSx8tkjBaJhzDpnOpHl5mGSDmK9MAOXs'
        b'AEdsJZqeBrHwd9bJzFrAqIg0k1PIktp5bPUkZiUzzxxZZEq/p1eLhW+kTmDczLlB2iiTs65Sgv7rHkRwy+rLm0x9fjJ6iViotBpApzoxS1lkGliUKVkWvlnVjdExpjqu'
        b'zpR3cugCsfBmTAZM9d3ekXWm4icSe4iFv9AQPnBgVBgoSOsyBouF9+UaJp4551SAjJialSMWzs3rxYxkNkzmokx9+FW5YmHtlNGMnXnLJNeZnC8Ol4buvKqIOcFMTVfW'
        b'mXJG64eJhfeUAhCWt1SyqSbrHxNmi4WDVlUxrzJRE0BnGxqrGCgWJup6MAbmR8O0OlOfSWVOaUCyCBN7q0iRZtK8M7lGLLxSvpr5O1NnB2RYflvFiYWXEtMBY3ZODQMa'
        b'lpIhcbbo8EHMDKa6EAor7KCR24rfG8u7EgCHT636oOyp/AKsqkqL2vzja1/9ddeZTS9HGMaq7nxyskf8+eJBA56KbfrbT3vf+Hz22LAff9BnW3PvF6z/nfTo4N9KPhpx'
        b'5ci/ixavGt6j6W/oAt/nhaSY7vN+pBnyApMwa+oo9rcTP9t4/siPNsTO+9+/fjjh/a3/6HfxxUMfM4Pfss1LKn6r4EdlP/Ztqd119+DK9bLDv+97vltCVcrV35d+9q+y'
        b'n66cfifyfu4X50688a77pWc/+ubQkndfW/L1Pwc8CP/pht23V735t8zivqUf91sz7PzfopOGjc3o/tyKIyMe3/9g1r0fO08P+PnETQ+z/rP3Zc9vTuR1n9TvjRdv3htn'
        b'/cmou/k3v/7K9/ucL46tuJ3ft/DIokdTdj/c8PvUST+7MO9h1u+KF6yLdRwfduKfA7MmDOAsWtTzm0/Vx2ed+8WUb0baTh0/oOep6FYDMixwL8MIfDGEOxPOvLAXpaxr'
        b'8X20KdeANw1PyAL5h2VUoGeu8tRRyroI7cQPk/D2eWNSE1lG5mFBEzwo10d8B/n87qQT4hxssCbEt8Jcu9RY7bDbCDmlFLhUpMDjVDzQYPgbTGWDKFZHN0aiqJwQzWlk'
        b'ZMOEo9sm8Mu3+k+vtLwGno9mw4F6q1inLkC9QfpcZTE7gwh2J9yEdQ4I0GpSxeUgWv3rmGBanUQen1ghUuocUKqb0Hbq4rADFH2YGQP2liiYSfiaAt/FZ5whqoJc+u+y'
        b'QmIhnmRMOSeoqfmbAw2EE/hNYeW8RSbIBPkmpp4tl8O1QrpWwLVSulbCtUq6VllkhANYOSFMCN+kgpIwL0iV5eHU60rjU2YIgtPichVUKiT4qmAOMp5wENHtJuCGY1VJ'
        b'fETRoAI+ogQ+oqB8REn5iGK9sqNt9LZCsbxANHNdHV1SwhBfmifwpQHD0SbR12LxqY2sywVXTx39R9+tw7XccI3szz8f8mF5zpLEfi+oP1nJ5L+Yfb7gyTfOv/vFjb+9'
        b'/uqSWTd+ErNv2ehPr11OfPW4evhf8u+n//W3iopHo57/cPw/PsmbsPCbmr470hr/sfJ3m9HH2xd+cvAnLw5/4aUvE2dcTVcWGl5488s9nv+w4+70nXxogD6c2mH6oqfx'
        b'llxDy9opHM6tmjKZGlmyYvGtYPeNwTksuobOoRN04RlBBgreujyB73Aj3HiTm8io6DI6grZQ1yuxYnwfb9NxqDGtgu5dhmnXJqUkiwr4MxF6Ls2KH4q2nz340njUhHas'
        b'R414R24y2oF2KBl1HIe9vdADKmzhowljUFMhEARiIXoqU4+elTGRYbzbhK7RPvUeNZHeN6DzMkYBkpiD64mOZ4rK4J0la1FTKghiKdmifSQan1ahuzx+ch6+Qts+Gt0H'
        b'6b8p1YVvp+hz8pNZRo2bOHwHnxnUViRXdZlstJAFpdFYa1lhNLbslD4BAjXdIVWxcSCSkatoViH9ro6UcDhFek9c4iofX2l30e0qUDVt7lU+VZ2D7KMLFp/C5XZaLG6f'
        b'xlPbYq/oTLNQOIkVyUl2JMUNsKEkIS50zoQAbSD6xH+DaMOWXkG0oU0rAyIbK/2RBeCiGxnMEnH5sAV61qcySntzcC1zWezWFqcBcbhUE+3mmgrBPDkCaiGrhVkd5Yfl'
        b'v/WdwKpEYHIjGSmgeIkBGAFATkLdtH4YXW1+mNE/6p3UGtnlWqvFWpVGcQY7qTOqTZ0hsnEKI1p3gDL+AKMe+Wlr2+ELbBMuvMW7CHGY+xbzuekTarDR0K3g7v/D9fv8'
        b'xdKrepa6NkRORzdQE96JN7SsRFiG99BpyR+kfR3a5gqysLV4Yj0Bv3GrY/3THvKU34JDB6oFx7kQDpcYGDviHRjN+pXzDfD7pTYYj9sHApSc/OjVgK9G4gRmNPrCjUbR'
        b'RxmuNUbjMo/ZLt6hKwWWo9NRZ3G6V4krakjoskql3SVOY2aXq9Jit/vXdVszEeCY+Bg8QrtA/Br+xUgGQpWcYaOjNCz95agjKz7XN8+Vl63PSU5RMOFLgOzKsBc/owmZ'
        b'XrX037WNDeLHbDm/h98TuScK/iL2RNo4KwdX0q/ANSsEA+HXQS6qUcAvCccOA94rs8iBYys3McCfw5o54NpyIZzm1TSvhLyG5iNoXgV5Lc1H0nwY5KNovhvNh0M+mua7'
        b'07wa8jE0H0vzGsjH0XwPmo+AloUDxscLPTepyrWkJwKRDXo1s7TNGpAzegt9qJwQCe/2Je9aIoV+8DZfHkV7Hin0b+aEZMnqwQs6YQDtWzd4fiCFNYjCiob8YJofQvPd'
        b'xbf3KPeorPwemTC0mRdSqFQh+pmT0dJ6I61hQoKgpzXGQA2JtIYkWkOswFPtNBWklkpKFB8PC9cF/UilovN7yB29wiezgaTpkxEMbA/hCiqV0oSTJaL1r+1MQiZE8SeM'
        b'DJ40qX5/ZK1VK5EPJRWGVEA+lJR8qCj5UK5XAfngKYGVffg1LNiQZpGf7Fqb22a221YTb/1qi84sdcIGrMlcW0nc/Vu/Mr7O7DTX6EiHxutm2uAtJ301e1pGgc7h1Jl1'
        b'6cluT53dApXQG1aHs0bnsLapiPxYxPcTyMsG3bTs6XpSRULG9OmFZQWlxoKy/Gkzi+FGRkGucXrhjJn6lHarKQUwdrPbDVWtsNntugqLrtJRuxzWt0UgpxBIMyodTqAc'
        b'dY5awVZb1W4ttAdmj9tRY3bbKs12+6oUXUatWGxz6aipGeqD/uiWw5gJwKzaNkcaHjLT42m7yJX/TIV/eEHjECzODl+WeK74vpSBMSopTB4xfPRoXUZeUVaGLl3fqtZ2'
        b'+yRC0iU46sjxDLO9nQH0A4XuSBDhqv0Wd6UeP8cV6/Lnfnh9Iq8VaxOvf0BdIebxtjZPTYF4lGMH3rWAmAkNKeQERG4+apiLG3LpUY3+6KQMPc9XUxuCeeZ2ps8on5xJ'
        b'M2nvD41mPMQnG10bRfThfHSxCD+LbuAGIl2n4sYi3FBYIlZTlkW2PfPzs/NZBm3FJ8Pwbf1IWmO4iliOXuAZnSlv19DlDNXm8NM1xNq5LSmX+Anm4VN9Z2eJkjURq/Eu'
        b'PTrPlGQo8X5HP1qJvg/HyFT50D+T/c9rJGvLxr4yRtVHpiRb3CNHxzKeZCKW4FNzg2qejRvyQGOEVqYWZ+GteT3wbQUzC59W4Gt40xK6Oz8DXcXPuZbJySgxdXgX2urE'
        b't2x3FvbiXa+S24cuD9kxYTs3PGrGO8t/seMXXHTYGm77C31HL7J1X1qfMfDLqEObhp57jh32QZ81I3/6/sfz1y9Kea5b2oHDSs2vvkl8/eD9Ce6XZj7xG/cz6je/dp/8'
        b'199Xaz+d8buY/n8YWv30vFPf/uOPJVte/qfu1IMHI7Lnjjz1pwcTXnk0asrnp73rv/p4Qt/6n1zM0490jZ/09jv73zd8uvf0qw7n18L1xv+WPK68femLE3/MUe6bsi5u'
        b'14Sd6pXOnk3zyy4nTUkcE/Uaf3fYc+cWHrzxxvVLjYv2pPbs53h6y6x//+Lf+miqjViGoU1qGB99vid5DGpMxFtTOSYWeWUq1IgaqLZjjjbhvaOC99LFjXR8BNXT/Qu8'
        b'F0bwZm5KTr4hGzXjHWSUeaYXuolvoDuyWj6N6kT90WYr2R/DZzz+XU/0JD7sJpIKbqxEhwMbioCht2aLlcTiTTwo8k2omTYFXR4q8++jXUN3W9z4Fi9f6SbyDN6EH6bA'
        b'nEMdSZictVmIrki7lLnJiQTfyS78LHRNiXbgDetEF9hbtfhJR6xoUgC8UDDq2Rw8em2um9iN8TF8E3lBkIR+WfFV0io5PsTie+ghOkOt8klpo4i2R97k8WE2LgdtjxxA'
        b'q1bhRvSIvAoj7EqABSbH9zgW3US3RFWwGXS6uwFNUlQjR+GNoEkm4AbqSZs7eiBRFpv19FSUOL7iWk1CN+TVS/DmGC0dXjO+jW7RqvJYaMZxdu0UtHNkf9HV4Z4iDG6l'
        b'5JMG3mYX4lvocBjeTXVNfBzfXkuamE8cGQz0uNQ+roofv7Q7VbJroLWX4WW/MKftXTGdz5xYQ8cGHUIP6sjLBhhg6tOqRQ/QeXSOnzGih3/XSvt/betqLaODAGwDni7p'
        b'r5l+8Xy4inpgajjR3UHGajkNG8cRY5ZG8v+Ngj9Fq1+OSN7wq+FAqxOpbYofQIEoEYeJ0jshgM5xjF9DbSVPtwj+XVbJ9Uqxku6htdM6EwMVU4mbOKP3D1Eafj80WGlo'
        b'0/SuK6REyulEzZsXpPRKMPxK7+MhpQGhiLArECD8/CrBaTELyY5a+yp9CkDhBUfld7bIKrZIZqywVXbSoAX+Bj0eTMCDQNUp9K5qvHKqVXUCd3EAblLnMs/3Ay+q8U49'
        b'06ImtgPcHACeEiww/VD44RL8JawfEzhYVmZR8aRI2UlbhNCB6EyU+n4NoQjAOWf4F0EnbagKtCG1KyLYD2/HsM7bsSTQjuTvFt6+D1qIi4G2oRPwNQHwaaVUHwHIwSY3'
        b'nTSlOjs9wtxuC3641UZSux6fbCOLTid6hEtna7UuXRZLDT0yDcoLVS/avEiOUUs6VQnoMNCjmR6nQ1dkXlVjqXW7dBnQg7aibwJ0EzoLLy4fnZKekqbvWDgmP3KmrZm8'
        b'VM9SL7CCHuh6UsFoJeFmsqksejYN37atjYnhqd9K/YUs4iOUZX7ljwnFn0T/zvRKxReQ5yr+GPNyzJnFf9S+vFKh2zHgwJM35MyLOGz2O6/rZZLZF/jiYcIr5fhAELsE'
        b'Volu9qNOg8usk4JkIFEAwhtXiDIQuj+FmsRz0QYQm5ry0HPmnJYTx2PQZZHTn3ChU7lUFMEH8HZuMZuKmtH5zgxeSmJl8p+akZyJnmCWh7NxxKIqEXzpmYLvaenKgaQu'
        b'hGnt0oZabEPrh5cJA+zEbYiYBRgv2yW3IZ4SV9ljbxtkKLG4RVOAx+62gSIsEXOPS9J8aaQAt9Nc6zIHnfivWNWmIlLHeGoMGW/Kh2egKvhnrrI4TZ3oZ+SnrW1T8knZ'
        b'zuyQsexYDtSulH+WD2A8xDVtfB26ImldQRrXUHyzE6ULHxhme+6jv3D0LO0XU6Z9bsoBrDUUf0p9F78QPjPJXtdve9swM3HIE6c1+qnLuxc9Uz/u2PDNIvYmhatv/fG+'
        b'nqNS4oTlTr+WACpCeIZfSZgEKgCZbrwFe9FzgN3PVXUorOLNaC/aJ3kdfde+pcviNvonh/Jlip5RfvR8gmH9Yt3qnn4kavNOgR8YxchxoTjbjm8TfaIFe4kj2OoQ7G0I'
        b'9m7qBHBXRQ5t6Gud0PktoWymq3ib4j9TRPSU9t2sqAsLdV8hpsKAC0tnTlbSwvoQNI221rbA2nI4bVW2WrMb2mUTOuKItZYVEtUenjK8HZtGx4YcQbSW0C77XSMBUIqu'
        b'2LLMY3NKIyLAVaVbJ1gqbG5Xu8YjsrKhBS5HjV+qsgGjNNtdDlqBWLU4qFaL09WxaclTKbZo+rRsYMG2ZR5SH0gkCYTd6pz+VgGsbLeZMODOCUTbrVxVgYfEQUFPGUpz'
        b'C8jWNw0uUJA8Oyvgh1mMG/JmZ/HFenQ+W7e4wulcvwLdsS0OY6ZVRdagy31pZAJranSwWSTobQZdr1qH95bBQt7LLsO3VHPRzip6niFMmYNvaFhi2WdW4QPoWMo0zxQo'
        b'L8Mbh7u0njlZZCuzDDcY5tC9+CZ0vjTLQABsy87DW1kgSc/oV6J9K4YOxmdKOXLu+o6mKDXDQ4nHhifW4yY1utPSprpAlUVzk+comaInFOgZxWjb3EUTONdSMiD/jEje'
        b'dj9iQ1rU9L92X68W9mg4/pdHEjbu4Q5sGGldWvDky9f/+3fNcN/ZQQOE8R+99PJexxbh/N9/8bxK9dGMC0c+DR+6M6t56Y2tN1L+dWbvL95e9e95rtj316Y+XPHL3311'
        b'x7Nh9fZMdf476h6v9T8YvUkfJtoBzqO7+AEQYb+erK5FW8dz+DDyon2iFeNIGTqvHo5PJpJtYUICKbUEWtkf3ZDhK+jQOMqk0bkMdIm6CivQfr8p5OnJojFisxrvzg2y'
        b'B2ii0M40PnZGlShFPIXuo1t+UoxvTw0y2Mw20drt6Oli3LQQ38kLkg96zxXtJxd643rJgIJOJAfZT0qnU21/GnqUg5qy8ckWOwLaORKLEROS69BJ1ISO4KcDpgR0uC5Z'
        b'8tbrkjsKoZQtdMF/fnJgC1nvrgJNXCTtGonAizlFK3obUkuBvw2UfAYIXmfUng96rIXkF0HSSEhtjJ/kb2C+jumQ6Ic0oqsKt8wIxKsTUv90gNQPp9pVC23rTK3oolbR'
        b'0gZPZyr2M4E2TGiXpE0vm97aMt9Oa4gTUI3TYvUpXLaqWovgCwNi7HE6QZDPrJRJLSWGao2f1k0TmVFLZCTGq5b8YjRWjcSaZA1yYE1yYE0yyprklDXJ1ssl1mQF1nSw'
        b'U9YkRoIS5TVK5YOVlI63g0hfRBrvfzfgit+xZZ/2XHyLvgKjRsrMRD1L0U031xJdyCzdq1gC3KpdNkU2nYBzlBSOHZ02nG43ka0ggSicoCZ1CD4w4ON1mXZzlW5FtUXa'
        b'zIIOkz63POHvVEfgax3udsA4LdCRWtd4XUZrQdgkdec7+FxbXSy8wJNBiNWpEi6Iz5UVAafDDRL5LcuCwmKJdbHp0Wg32o1v5OIbOcwQ/IwWH0KP1DSAA76MGktyU5LR'
        b'QSYxB4hqcBWByrNyyhJolIO8ApCf8em+GnyODxNP3K7MZp6XDWYZkym8YVESQ09CqHQlraVxZ3dxByQ5J78kWBZvKgnDjxLNlHPnoKPQbPoEtVBn421V5ABZEmGaLfwY'
        b'dEBDTl5KdnIiaHFNes0yYDxX6bkbvbwkhHOTXhCwCWgXugYUG8Rtgz45R86sxmfDUHPVMD1PA26gm/jWQAJ55eJ8npFNZtEFfAZdpkGlZqrxs0niu/nETeogh3asXpOM'
        b'9okhpe7gjf2ScvJTksnooT1obxLLdB/G48NadNbmyrjAubbAYxMWzu772v0ILkMjK1rz6E7mya1JGwe+8sqA+Ys+yN3piTVxv8KxTSt2hx0beeray7rf8hMS1/+yl3L+'
        b'LOeeNz/OHZX38zkxa97d/e72X//qZsWyT/r94S/7zg4ZdL9659myQS/1zw9LcQx6LTxFeGXmC3cevp90Q/kwc2Gs/dN/bPtsyuKfrfzbhtv/y9r/mZj13hjg1ISea9KH'
        b'5lL2xVWwqAHtH45O4lOUQwv4GNqpbpc9z4aSK+hkphg66MLoPn5OT/wIKbcHVm/Kpbdt+BK+n5udnwgyE8eoUBM3Fd9CT87Cz1AmPRSflhEWjQ6iffoAEMqjK/Fd6haK'
        b'b+eiQ1D5+iH+EGgwtGJIjB7oSdCk6nPI/gV1NVXYuYHCGNHevhntd9CDIoViaI1+UQaYjlQe79VwlIHbpvb1G/PdNaI5v4ofv2aAyCA1/48M8GrC/CRyQTm4oYWDjyT8'
        b'Wyvxbg117hf/NPTwCSda2rsHs1GpJomLK0SuVEaSOSSZG8rKw76fn6xMrGlugNHPCXC6+ZCcbcXt3xkYzO3ba2ZXlTuV/4VO+OwrAT47gDAIIJ+UXQT4S4gVXUb9fzj4'
        b'YzP1cU5yes5JqIKTkCTi0yc4Ko1GulPgJOfp6Y6Cj6+wVXa4aeFT+k2+xFRDNV5fRIhOSkWiIFlpPn1Lap84Yd3+H23wdIRuTnISqCcZqcWE9spkXAwgFMP2G8VRYbHL'
        b'KacN76fmiEDJhbMxccF3olldf3JFIwQC1cDXXXkFohjOMuGruaH4OSDZh9G2EN4VLv13fdPKg0koK5cJsnK5jSlXCPJyJfypBEV5mDCnPFyIKFfvke9R7Ynaw1r5PVGC'
        b'tpkT5oKUo/ZGWXkhUoiivjkaS4TQTYimnkcxzVy5FvKxNB9H85GQ70Hz8TQftUdr6SZGiwHpibjQRHq7WVVCT6EX8TaCGqP3aAFulNC7mXo80+e6gcLfR+grPdEd6uwn'
        b'9Kd+zTHwDPFkIt5HqvJYaBsrDBQGwXWcMFgYsokp7yEMFYbB/3jqT8SU95TeSBSS4KlegkFIhtLeQoqQCv/7CGnCcPjf16uAmtKFEfBMPy8D1yOFUXDdXxgtjIH7Olo2'
        b'VhgHZaC7CROgbKBU80RhEpQOEiYLU6B0sFQ6VciA0iFSbpowHXJDpdwMYSbkhkm5TGEW5BIohCwhG6719DpHyIXrRHqdJ+TDdZI3DK4LhEK4NnhVcF0kzIbrZGGeZCjh'
        b'hRKhdFNYeYogp+aQ+T5FRg11mXo2ROAh61q8IXpNiYFCQZYjYd+qnGYixIkSWOWqgENPK7eZUB8sJ1RQY3HbKnXEu88sGigrRUESCohsCHWKlg/7Kp2jVpT22pPGfArj'
        b'crPdY/GFGf1t8PEzy4oLHk+sdrvrxqemrlixIsVSWZFi8TgddWb4l+pym92uVJK3rgT5t+UqWTDb7KtSVtbYffz0vCIfn1WW6eOzZxT7+Jyi+T4+t3iujy+bNS9Tz/nk'
        b'IliVH2rANkX+B3xX1hOiyrnCCWFdxzWwa7l6VmCX8i7dWm4JWw96g9Pg5gRuLRfHkKCvDdxaQON1rMCvZZcqnAvXssQxEN5jl/AkVKwQ1hOei2dimDHMOrZWBfeV5KqB'
        b'Ie+tZYwyqBfUCbhSCCqqSoR/aGxPlWjtUybNcItLWesXOhLQ6TiI6oFZrIOWdGJmEgdsPPXaKilMHpk+fEwwAgmgVWRbibSuc9VZKm1Wm0UwtCvT29xEAwDO5vceo5D9'
        b'ap2IrKBkOG0Vng60gvHk9niTYLGagWkEUMgEaoatsprUbhPHCdBQggPI1bZvn5JZfxxrq6V7Qi29GTbENczHpvjYtE+JmPEp4baP+ZS0tIJPv4UfvdIX1Ro22c8w2+uq'
        b'zb7wOaQ7M51Oh9Mnd9XZbW56HMQn99TBKnGSYAb+nYwaktQynR7Dpnz1/YC0EC4DbhEnGSh0HBFxVkeKWPB9t+BpszoREv4R2ID3Awjsvye3xhs6e6vqLDoTzEolsHF7'
        b'ygzxv8mUAjAmM112ARdHqONm/Tsgu/SmXgDt42L7wKIY/25rPbOEUwe2wXk6FT6V2WWk7pU+lWVlnaMWtNNOGvKfQEMq6b68p6YCNFwYCGkEdHV2cyXZ/DS7dXaL2eXW'
        b'petTdGUuC8XzCo/N7k621cKIOWEcBZOJoKlZWOKBB8kDobV0sG1Kj/GwNJhBILRz4BgPS23pHW+hElv6X9qjMmV1RMoSKYxlZWW1ubbKonPSogozMfo7xJ1SeMqsq3M6'
        b'ltvILmjFKlLYpjKyj1pnATYxHYbTCR2aZq5dSs3fLrcDZEBKD2q7tPalde9vkpE2yUTG1EPXukhZCAkKmL1hTIm3aTs7aCTQtsVd7WhhWQadywZEVKqGvEY2soN9Vjvq'
        b'o1TReBKqe7xJ4qbtbMV1aseocDhIHFWdNdhg4qFTIbSahnap4gqLExblcmCG5gqyI9+B6SQgSZKV1zZ+ibbAQ/bi8Z2F+FFSMqj6RGXNnUtsCyQEw7bcwrKEnKRqQ3ay'
        b'gqmJVuFHyItviB6V9/EOvBvUwKv41uyEnGQS5XZHUgG6hU8WJ+MzHDNylnwt2lk1Bz1DLQDd0PMrXCReC76Wg/euUEQzkWg/nxIxjHpRmtARfD3Y6pBQkJyYm1zsrzgX'
        b'P+mSM0KUCt131NCg2OFoyyQXPoMvJkgRwOVoB4uvRqOzNEC42hNTgprxnjLcjPeW5a9Eh1hGVcjim4OtmfTwAIufngjtyZEz6Aw6xqMDLImqhS9Qg8RqxunKItYIdA/f'
        b'wM256LIMOrCfRxfN+JgYRHs3foQvuvDmgQk0bI98HYsvPYEaS20n6/qzrtfgkZUvD+zbPKl4WkbUpjX/3K9MzJzzQL0y/JWGrIhthl36S70G/nKDafSyXZMa//Q32ZHN'
        b'809+eugv39yrYnd3e7rH0/0Gx2ePHPl3Q2M92rjm4/29YnaNuzfw9F/fK/xQ+HvupJyyjybWN8nnr5zw98TdT3vxGwcvxD13+++b96WuGbLqg82va/sffuFDW2bSi7jv'
        b'5X1fzTvf6w+zm576TeXEb//27JB/HN8XMfJnv6pTDVvnVVRdmfTVlF+bJ+3a/9tjz39rv5v6/M2TM7+6duxK/dWXXjly+f18x4HJjrvnJ105vU7fTdw62IA2TyUTlYub'
        b'lAxuRA2yZBZdGod3iLb/u3gP2peUjLfirWgvbkzNws08o8nkFbkWcVviaFEJakqFB1gGHZ4lS2XRjSR8g56Wy09DF5Ny8vPgzj2bbACLjk7LoCGPh45AZ3MXWbPzE/OV'
        b'jELGqXROauAYr0PncmljWGZqN1kPFp1Em8OpESYRbdYDLu5p3w6Dr6DbM6mngxE/qU1K0SeKWETQIRJf51dZisTW7sR3kbQTE6UVTSgX8VYxgsKGFUuTJNxDtwVZAYuu'
        b'Ro2jvqoL0RE3CW9MjCTZhhTUmEqWFtSh08nwbXTOI8YvPekan+tfaAvQ5txC1JyaQ5daIn5ejjeuw4dFg8y+bt1oN5eiZ3OzyfogUdc5fBjfxMfpyOGN6FYmfqoutzCZ'
        b'ZbjlbIYOnRU7sGVJqXTsET3pkk4Ny3PdNGTo9XURufm5ufkp6GgpbjTk+iMSJKLtcnRlDjpJ+7k6ZhZuKkCXDAoG30NbZDNY9GBIzfdwP/whZwdjRUpoDCX+1ApEhAvJ'
        b'CvQEow2ncVaJYES8MmOo5yU5YxhFbUFaWqqVSqNZcd9ndR9JwmkXSMD9hJ4S/CH+lqz4KhUd6iH5tpX1pz7kQGGnjYG6iMTYvq8KjV1CQ1qBMMAGxS7h6HcaOvZXIXsX'
        b'v2lPFJgu8jLpBIso8RE5BVgLYU8BoUuSCIh44JJE+bacRzL4txIpWgkQ7QsMbflYaVvhxEwYYAi/9rNPB+HrZLdjFZE82rbMXFkt7pHXWGoczlV0c8bqcYos2EW/zfHd'
        b'vLy1phQqngZ5CbrNzipQS/xPdrq9URvY3xCxwr+94ZeZiKRjcQVr852wfJ5pf4Ofbjk05EcwwMgS0pY/ter5uVKIiz/K+5IQnwlp2p8OzVgrRSjdNfUOsxKw5URCs3Pe'
        b'pB/1oRG0R+ONhMLHuyIiOOCl2xl8qQyf8JAwrOiCGm3PDZEgDCn2wGYKtfEDRy0lm+5zgbmTrZGWXXygP6v7RY1HG0ptL6waybvOQo0fPfttfvNwLUqLkv3rNe2AqPEx'
        b'3f52ce0GNO2p93rmnP3JqFk/Vq9URX6w6K04+XtfLJlz4YsBK69eLy988vcnlk+zLj7xcu8XpoVNqt3/7tszHnaTvTjuV5kffPLjS783/f5i8+9y5q8YNrak9+cruMT3'
        b'1p/v/5qiu3Fz9LTex//1/qghEVHl+mWJKc1jB/1n4Z/3zdvh9PzuzT9M2T2rz439b/X/af2uusUD/nD6y01/eSyf5Ri9/cL/6kUn+bSh6CTdeEcn8GZp572/FB+4CO8F'
        b'Qi+NQTR6mggWkXN4O3qAtrqHUq7ijAoaO9SMnkNHQ7gCOclOdyDm4s2aiPCWGD5sWT6+JXKWUzPRMZG0E7oOTOpuKG3H58Xz6RETe0mBfmQs3luMjuNDSdQVKwsfXZPU'
        b'EohCja5noSYOX+DxRdrHUVHofCDOTz6LmpahR/jUQLo7gDf3xyf8nJGwxfPx6KoNHaR8GW2cj54K5ovoALoQxBsvw0BR8fL4vHgqkGZDywPjgW/ZCZPk8HW0lTWmqtAz'
        b'NeiyGLSoAm9Ioh4LcW45o1jC9UMnkin3nGNIUaMmtKvFs8y/T5KKToj+Dgd6r04y5IPwSUKIo434MBED0G7eiQ+iLe2dIu8qG1NKygFlXOnBjGu0yLIUlCVpQccXmROJ'
        b'eKGlGxuic4KWXa2V+INUVai7WW0oj+ok+gUnPtvihbAZkgRomCuuhTNtYHzBQYtaww5Rs0mtVM0mCgRRs+GP2MN6Caybg2u+no2DBwQuJOcPTPSYG2J7LBuSkg68iLbM'
        b'pzHWOoySGuzy8eYKF1XT21fJfVHGwO60aFzM4fyHqDkYNm51D7+ZpNVzITbAwLYw2ZNooJH96zln5lqW9oZZyjunkl45E6GE9IIhdr/aODcvsGtpnjxp5UW7IFzLyNcB'
        b'qMmFK3g8LMAua2wuaEJlNWU0Q4DOE5MTVYrJBcwaHYDutpo6u63S5jaKw+2yOWrpLPnCSlfViTYmcUhEg5JPTrmyTyUaaB3ODnxvtcY6pwW4lcVIn5/N+X0cSUQsgn2c'
        b'jIZhWB3rH7KQ59tMOh0wgjQCMWnSQSGDZOXixMmFrkeLNSWQ7hnETkLjWgxg4py2+UYCOXMDoJ1G40JO+kICE2zwEu+1j4XRtEF+PJQas4k0RkmwDIa9nRa0xiqlkZyF'
        b'N9IzP37w2gB4eisginHB0OP9a4AV2HpuHR2QtezSQBvYiQCdfAZJnEBOhL69nSYojEa722is4CSezcAcrY4ItIHc+15NCKAjN3HS92mDxWi0dtQGSzttCPj1B5bRQP8C'
        b'Wco5dGJrgEBwJVIryZVojwuel6BWdYDO0DjLMqNxCSeZE0U0DmkguR/SQM4/SBo6SAS4xm8O9LutdzYatdDjuiCcaAFV295YdDYfsgBKTP4e01EF0+7qYDqqvi9KyKn1'
        b'laDE5O+DEqCTGFd01AZLq3UZ8DwnI+4nEy1W3yDK3i4VINYxo3FNu1RAvBfocYiUO7jdHvcg+zoMpdhcPedfEGwSENJA5/2W+ZYRqGm3cUAizIJgNK4P8BsYifBgMkFv'
        b'd4Z+S+hGUMvpm6e/Y+wJVaSV1rdPFUMBdmE84luPh4iQyT9wPFyeCqNxS4fjQW+3Px5a2jx1y4hUd31EaLVN7Y9IKMiQESFCdoBEad0MJUeQj2k9JrQpvE9b4HBnA2O2'
        b'kJNBFqGzseng6IvRWOMBhN0eTLBkoUNEH/g+KHO2CwNEK93T/gCFAgwZoInBA6Rrizy9A0PWu9WQSd+AJKiU2gVUan+41Eaj2+mxCLblRuN+zn9aiNL4cA4GLTrQicBj'
        b'P6wfvQL96NVeP+iS4FJ/eEc0wEDtDoeTNvF4Oz3pHuhJy3M/rCtxga7EddgVdsgP7omSBgAyGs+204kgHHYEUyEZE7TdUMS0FQvE9rtJD8h+OrS15Xoht45bx0v94OtJ'
        b'j3jxyhrcJ58CxgzAggZBO3YltHeylt755CuqHXYLcQ2uMdtqBUtHsnK40SjWaTRe4aTVJwkYHDnWvbpboL/+59qXj4k4KrI9NZ0aSlKsraWdjjggDZ1WZTTebVcOpbe+'
        b'C2z4DwNb53AZjffbBUtvtQ82hoJ1iyDZIDZLd1sbQ+elE+ig9BmND9uFTm91ScTY1AURQ0l2z0FueqFdWPRWl2BZuwArjC5wM1T5YhC0qODVT2463UwrQ29g/ZD1T1bM'
        b'UsYZ5QaNmnqhsAIvyAjf6kG0UrJSiI5KjiqKa0daMZSTyQs+JZU+Hkg3n221Vbo6xwpx+3p4mujF4amrc5AgP4+5tBQfOxxWz2r/tPlUyzzmWrdttSV4YfmUUFOVzQ26'
        b'umVlnV8x7dAUAqNAgRuNP24hIyoaEFQbPBrSQ4CvxI4pugconFXkupokNpIsIQk5oeO00yEnc0CGT5/aymHRuVCC7bI73CSw2EqS14Ya2SFvtVoq3bblYvxoIN12s8tt'
        b'FM3JPpnR47Q7yaeLnNtI0uL6GMBpnypguFBT+624RUyt/1SFd24lCaVSu0hCPtjn3EeSAyQhYaOdh0hyhCTHSHKcJEQQcp4kyTMkOU0Swvud50jyLEkukoTEMnVeJwn5'
        b'zI7zJklukeQ2Se6Q5JF/PvTR/39cKVt5spgheZXsfJBAqCqljJVxMjboF+hpTGwb70meY3UJ8DdAo9SqNbyKV8lUMq1C/K/hNXIV/SMlWhX9DYNS6ZduDKOT1fhpF96G'
        b'm834luhaqYrnPPhUcYhXpf9kiOutVl6V/gipVhmN1aqi0d5orFYS802K9kbjsgphNK+k0d/kNPqbUor2pqH5CJoPo9Hf5DT6m1KK9hZF891oXk2jv8mpD6ZSivYWQ/Ox'
        b'NB9Bo7/JafQ3JfXRlAvxNN+T5kmEt14035vmoyzE25Lk+9I8iejWj+b70zyJ6Kaj+QE0351GfJPTiG8kH0MjvslpxDeSj4X8UJofRvNxkE+geT3N96Dx3eQ0vhvJx0Pe'
        b'QPPJNN8T8ik0n0rzvSCfRvPDab435NNpfgTN94H8SJofRfN9IT+a5sfQfL8g383+ku+mjnptMuUDJK/NgcJUyn8yfJHkGE5py2nVD6+23vjyH/AMekgKPdfqMeImQn1W'
        b'Ks21hGZWWCRXPLeNbjv5PUtorDO/kx5xLhH3dyyhO1HS/leoMwlR5YKO1poIhTaLJ4kER6WH6CCBmkNqczj9FdrcojVQfNW/nTQ9I790hlSDqQMPwpBMtlXyjDHrKqjt'
        b'EqoTdwGDj/4aRJD+vkr+oW6nhQxISH1mF3VHJY2j/irLoSaz3a7zEGnMvorwpJAzxSEvB3gxUTAJdSHx913VLGGLGpB6CHPsyTRwS8OcvfwM0k1NtsAaeQGYoVFMZTSV'
        b'01RBUyVNVTQNo2k4iKnkv5rmNDSNoKnWStJIeh1F0240jaZpd5rG0DSWpnE07UHTeJr2pGkvmvamaR+a9qVpP5r2F3hIdQIL6QBaMnBl9VpuyaB6ZgazaCEIx7J18rWy'
        b'JYMFWT27k3VpQQyQ9WDWyWp70VI5KXUmCAoQAIaslRFT6DqZeygIBLJ6Dp6f6oZ1vFYmGq3dCaR8rbyeZ5llX85lGgD2Em0DS5+scOs3QivoSlIVOO8SEWKUuATaLJjO'
        b'l0SmjzX6OKPxsdw4xDXE9XhI6/erzcSVq8UbTDQaJ/o0xSAW2GokD0uFuBsqBh7ljTbBJzd6LG4niSojnqHwRYqRyANn5pxEeHKSU8ROct6LRsARY67kU1Eg9HglCIbi'
        b'tjfUWOdxgshrARBUDFDS/QO32acw1riqKOil5Nih3GgR/9FDiBH+1+i3s+ClymqyZUsj3ZrdHhfIIk4LMe6b7SQoUq3VAS2mQ2qz2iqpmzWIHyLBCNw217hbOuSLMdod'
        b'lWZ76Kl+El+4mmw0u6B9dMFCNfS/GHfY18fYashBzIXFKD0rh+saly8cGul0u4jzOBWkfEqYFzInPm2Gf2bEmVC6LG7phstlcZIK6Q2Q1ajzAzF0+BRLV5CvhwdFRqhh'
        b'vjsuA53d3xEhsZwKidHUvaN1QC1Vm5IOfjnxfzQ1S5EdNWIsJtHkV/doNSJdDuksSf2/Yjp1XY3m/R618a0BBVxrJ5ZSN4rapS2HPA1ipAW3QzoMSzwdBaDaNusqoMVB'
        b'NLLLnrZScyd23txYf3MfDw2Nt0W8Dmoc7pYzuDTGaNeDC03pHG58AG5ooK22YElQ064ePqaLvROovUN7GxxmqxVYKcJoV+F+R4StfgG4+nYibP1A0F2L4jQgAPqdDJ0Y'
        b'V9blqZCOi1BXegJP8v2RAjp12i4qOYkV0a1VIujUwWtESKFxb9oJEZWiK2kps9osBKAkNUDt8ECLZ1CAF7h0idI4JRrg0uam//3BuBLpRmqiGBMrscuR0PI7H6yEwGCN'
        b'bBsKpQP8zJg2NyMVkpldj8f2685bkRRoxcSQU/ok5oilIvS8fuvWTC+eOSN1xsxppV1vzZudtyYl0JpiOvNB7FvyFfOfC2jlxJSim0FDo4guW/YV5lUu6ci6rtZSZSaK'
        b'd1cD6Dl/03kb0wNtTPQjud8NK6i5Eo/WJZTMmVvedZry285hjwrAHkbJusOxlIi14qF7kHbr6hzkOBZIRR7xmH6XO/1W54DHBgBHlgZO2HQNgDTzb3cOYEIo1aqBdWqu'
        b'sgQhX131KhdxwtMVZWQXwLq2dwG0RLV8nYOeHDqoLSDtjqpQiLqE3OKZmV0Oxeh8p3PAGQHAovNhrZDsdiTDvxZWrUuY2TWIUlff7RzijADEvu2Gf9Al5HcNnISu73UO'
        b'blYA3ADRuxLEwVpyBEVaHGIQjqKy4qKuU5D3OweZEwAZTekZlY2lszRdHsUPO4eR30IBWlMpIk8TZyBynTCtsDA3u2BW6cx5XaGQ0pB+1DnsogDsv7aGHSrjp+gygSLM'
        b'skBraqn85wpo2+1FfAdCNTc7s5TEbTfoZs2ZbtAVFWfnZxQUlmYYdKQHuTPn6w3UvSiToEq1VGdHtc0ozIdVI1aXmZGfnTdfvC4pmxacLS3OKCjJmF6aXUifBQjUArDC'
        b'5iLutXV2MwlpJYYG6SqC/L7zAZwTGMCBQeRbVIdEhDTTBWh2wRh2daH/rnOY8wMwR7eeNFFnS9FltJx7yy7ILIThn1Ewi9B0gkRdRp4POm/HwkA7epRSfi6qiTB5AsEa'
        b'R9dl0D91DsjYQs2lcC30HKUIxtJi8QnWNbo61h93DroilMS1kDbiZa4jRqpWzIPshwT2QeZI4FwF1Csvnu4XUm+vuj7kWjxjS/Y94E9WD6mRPC+nXnxy8qaRpkuIaURZ'
        b'z7JB4/Z4QrHohU3MVAH5RRSmWgxm7QtbKXqV8w3SxUUkaRXAmdoaiH+hk3zd079pP5Zpb6tITb6kJlVq4SUHCQY02HjqoUd8Q1f3bq1MBr3T/iwRo5ng9wMrFfcA2p8i'
        b'sufg4Fs2qdoorgHvm9abYyH+Rk4t3SBjyJ5uVdBGGeck21A+GTE8dOCBp5LMEkYyNJI/CT2z0U5TxAfb73NMSFNIvF2BldyeqB3L3xY5HbeO3QHtllqjcUWrtrRjOKDP'
        b'FegHtbf/RA0adMfIp21lnBobwJoWhFnsxxVfRKhtSiGZppQSh6afyfUpJLOUXLRKyahRSkZsUjQmiU8TYpBSSPYoGbUtaVtZntTBhieFZLFStRisRGORNtQg5VSzEuo4'
        b'yaernOQrUF0P1+b8MSSvE2sP2eZSaWRcdHoXomzI28bd+J5xOtqmss7jemjCVbxKLn7eosGID6uXR9Rp9Dl4W1JBXgpxdydR/xNXyKvl6GokagrZbfI7HbvI/mPLbpPA'
        b'bWLotwB5QRb4FqBculbQ7wKK10pBKajgWZWXs7LiNwDLwwS1oIGycBqrlhMiBC2UqukTJL6HqlwjxvYojxC609Uf4+veCnPzbKBE+7fCZMFrmTjGE1pqpF4YRpbsJxu5'
        b'KhK1gBcCBF9GxXdfWODbu3BZ4xDMdvKhtoGtTY4EmjF4f8Pld9KIY+kmqr8Slb+O1gSK7L1u4AOOVNKX4/q0A6fr5+O7podsCVjz2oXW5S+0SXLQQLZTaF4/tK7y3UGd'
        b'19fQbn0hTmZ+7w1/nZyTROJ0Du64YrLatwZxi46moS2Z/g53iiCYbXgkJS/NQVBb80MJKiXI38EPN3WFH+787h5KPNG/yEN8twqYFt8nV7QbAEtnBajv1lLeNVI6W8DT'
        b'a3IlW8o7J7rl4jYW5BVLlMT7j/U72PEFj5ODpdQaEkSgoiUqw7BWrRwW+rjgsIjH5sUzCTRSjP+wHiXwIM00+xel+Cn2IeRqKEmoUwiZH+BGdXWgDfsPI6iDQNBHO/Cw'
        b'4s2CsDsg2kgxuzT0fxu+SocXnm8fd8Il3AmgbPBMtsUb8snDI0Fz2bM9YG2lqIAzdQxdIyLNXsvMYOr9a4UvCJFWAy+QIxKEXi7SkFMhRAh5iltG3L+tfpdz8n0+v+Md'
        b'+U6dj3W3WWOQnPC3WsGsTm6v1W6H22wHEkS2hVyT4YJQdUdN3WTyTQyXp6YD8UZO3zv+XWNCnyrQa1uLNi1+MBRRWnCkRQqgQkESK42+MyUgGXQSAWUAPLSOlwYcOK5C'
        b'/OKfiifeIMTbg4bzTTX1CfBfdCm6hQXjG7jRAIBm4EvKPPQcvh3Ch+Ok/67tbAgfhlmlv/wReTlPvD2Irwf5up8QTrgs+Y6foCVcVeh2RFtOvsUrB44bLXQHLiun529V'
        b'JBKWN9rb06oUYoRYKFdYlEKc0EP6fq9SiCfXJFIW9QlRCr1pvg/Nh0O+L833o3k15PvTvI7mNZAfQPMDaT4C8oNofjDNayE/hOaH0nyk2CIrLwwTEqAtURallbFE1TPb'
        b'2fIouBcNrdcLiXCnG/SEFZIEA1xH0+tkIQWuuwvjpDhfJNBIy3cQtdDPKNrT7t4Yb6w3ztvDG2+NpXG3wspj9ij3xAnpzawwnkCB0eBp5C0SayyWfDNQGA33JlA4Y4Sx'
        b'tDxOGEHX0USfhqCf30vBxxb52EK93MfNmubjsmf6uJkl8L/Ux03P8vHTZhX4+Bm5uT5+1rQiH59dAldZxZBMz8r08QWFcFWUB48UF0JSMpPcKM+lHmTwRnaRXuvjps3y'
        b'cTNynemEmHHZUHdWsY/Ly/ZxBYU+rijPxxXD/5KZztH0genl8EAZNCY7sNr9Ec6pM4L04QAxbJcsEN9c1mF8cz8tD8HPtgH7ZQWebIYEbNyLbhGMd+PGwhTcnE+ijPpj'
        b'i7LRqbNpcM+UbHqIMc+QnT87C9ZBDjkASj5KOhlvjEQ30VV01PbfXrPkLrJLVX9l/+emz0yv/DEhOsGcZbZbN16xVxjMr1Z8ZlpCPnZqZxlLleKOcbn0lfI61ITOqNF5'
        b'Q5Z4ihIdq+KYbvgejy4l4x3id56ewvVz0CN0EpNPVQF0EnHgMLdyPHqGnsUsr0PbyFeP86e2+ugxOoEOiJShK5vDnJ8eB45Tir9jiT/h6phgLAr9mLC8ZXPa+SVJ2v+6'
        b'BC8+MTjwWADydUKYyEFeZkPI7y9DYva324JKlTTHBFzohylVFG3CpS9zi+tMDO/T8mFKVUMYoFIYoJKKolIYRSXV+rD2UEnGtBfytneBZxRcmyLQtlx/3EHAm+TkFBKb'
        b'Vgzxet6A9w7NKitagTZloXM8g7fXqfHOuigPiT3UGzWvankTEKwweY50gDsHNy+dhMm3rOcm4Ma5KsBUGYOeQ1fUEegsOkkPkt/MUZIgzFG6vOWGh5qhDI0ai2860WZ0'
        b'B50OOkmOj66nL2yKDWOiGCZt6pS6PNv0EdKn/M6OGRAaWb7lRDm6jrbRUO7zS5SrBqlFAGfDanOz81Xrcg24Wc8y6gIOnxlr9egIe0FX9UlZCxDhHNvw7hFpaWiTKZcZ'
        b'iG7x6OE6fJJGskcNydakAnIAuTm/LOjQekJKcgJuSEW3zYkkCK9Dr8I3KvFeEeiTcdibi5uy81IVjKIHNxMd1k7Bz1IHRRIhBV1IIgspGW6ie9xydHk0akB3aERifAzd'
        b'Qpvp7XagAajZCTSkelGC2Ca0OQs/hx7xTD+0OQLdUQynHxmcip7L9uAtruX4uoxh0UEG75iQ4iHuAhOZOUEfZpxbB0+UJuBm3GQw5JeJ4fDXzxLP6rcEp8TP8Bq8Ywp6'
        b'4CHEDm1fji7648fjrXnQje7oGro7i8dHWXyDfsMxFR/JaBm15JaI/dCRWQv8XSFwOLSVY6DPj9Sj8vAj+iEAdAptXYB3z84kPgurmfwqGBsyX3jLArQXOPy1FcvxTdS4'
        b'Al93K5gI6M5TvTl0cKjbM4I+NGOJC+7MIR8KSMhJhmkHQkhBFScUTIwLtElBovjcDWdc5XRd4JP4KtqTRIYChqYpFe8oSUgASteQWiCNS9FSdI+iF9qAzocx6B7e6BkA'
        b'by6LdK5D59X4Nr7pwneWoeYVTs0yfBuo9ggebWLQkx5CP+PxPh1uIp8qSU6BoSWfZG8gMRR4dLkXaqQInzhGRgI16XYONhk29OnD0G8FDSqa6lqGr+DnxS9Goq2oscaW'
        b'PuQU56oFTvTh/SVlxdkFeGrUFz0djX/eudmuXfP+jw4W7lwz9ia3bUj0290++mBh/ADPYG23yA+zJz6prDv5haE4ZdSv3it7873K3Pw9O99cVZV98eLquSe3Xd+zY/8h'
        b'T+yar4/OeHl4SmK/7hP6jx+w/NLiNcU9fpH4z+Jhxxuq1uYOt0QWPf7oH+eLvV/vX/nFmfFrNuf+KGNa05jLl85t2z5J/eo17Yqvf/ns3sTSbyLu3Nu04M60nvtxz5VJ'
        b'ydfOzy//cXSPrac2vaH7D9vj2qYRD/5a+9m7V5d80zTZnNf7p9/8aNy4laNef0l/pPmntTuGLnvjxKtPvrNr5ztDE/tc+Ofld/Xuz05NfnLolqRa07G/nI3pcXDz3Z9l'
        b'/uH61EtJfyl45x3blNP/h733AIvyzNrH3ykMZWgiYEfExtDBhigWEKWjFLvSBgRF2oAKNkSQJooIKIpdAQuC0lRQk3OSTTNrym6K2d2UzZq6STbJppj2f8rM0AZi8u1+'
        b'1+/6X1+IMPC+T2/nnOec+44NdapNvFm46NXXyu7/eZV9zJg5/z7s8VnMqSSjtBibA51xXzt8mvbvGyZfxO3de39p4E67eemTRm/7Q0zw/af11r/juDnnyP3J671rtjkf'
        b'kD5MPPfBuS+tvkj0LdstqnZ/1fvPp34WTZ5T8peGpxQT2Tlmi4VLe52E9Bg858lOQmg0YjhJCybhLbKk4MC4KZyESQ7NYryQBd3sLIVTeMNYHkQpFPqjEszC04yoaRvl'
        b'Z4KyraYmRpnYrsKOLBOZYJmDHRmSCDgPXQz2YCJ0Y+FGLNYC/5AjvpWhMMDp9PWUwakCCnpRNExZlcUW8FncR5ejUyg04ylSBSxmVbwqxnNT4S6DqlBhEUUwMtuCHenY'
        b'nm0yFWtkgnyEOAkPyBgw0IxA7GQ4FxzjAurHOeOFKI5YdBJrFju6YDde4TyaPRwQKS4M0skdDsPR9IAgyvEgzhHNDYK9rN82YLUhWX+lUIkXSA1JxaWzRXBtLjazZMYb'
        b'oGEcXuXkU5R4yi6dUXJCyUKsUm0xzsjGTjOyQvabGZgYYYvZFrIWsWNrhgnciZcJIVIZ1QjI3kD3aFMHinmG5cHuIkG2SkSOqQq84rea9asZ7oEKEzyGZf7QRASOnaLF'
        b'kxLYsMgW7qIEmGVwxT+EnBsHXQJDJMLoKHNol24l+3AFa/9ivJzFaDLXYykFLysLJnLOAjHWwF7MZ5KSm2weRcGIh5u9NgTrYKnJAmeOLpU/3AzKXOkc0xNkMWIbGzu8'
        b'uIoNDLYuH0UehcIVOMP3Mj1BHibGatxnmEWRl6EZDuGBkUlqzswweiyTIshhKRPG4wUptnrCZS6vFRkv6MWsaYwlaraw8FQ+iY7HEbmTwnWVB5NOChAnYNEIOD+SzWGx'
        b'kMFQwJ1dQoPDGCWrSBi9LRPrpGTv283yzzUxp6ye6mNkClaLBNMISQgZ2lI+T8jAnqOkoVAAVc5EngiSkFlYKsYGrFrHahBOJsEh8kagUwAesCXSg4GnOM4IjzCwFAMi'
        b'QV6j/XyRCJv0BShWs5wGkEnpYK+HezZBI4PkCvLCK3CJUouEhTpBiat6Y9cjHdKpp7cZCviy7PKmFdZKFFLBgghIcFWCZcPgahY91zAPO/EsXRd9ZHEogYOu3BhsT4Zb'
        b'rYw6kiOmfKIRnHL35cyxZ0jiLt2JHbASLmJxsEImBAv6cN0Wi1kaD7xBdotebLP9qWZ3Q6uGbRbK5JwstyGIrK8y1x14gfQ9aFLJiP4rwbtw20i3mP2fZ1FlRgImrqcO'
        b'FNe9jUQGlDhVLBWNpCin5Ke1aKTYWCTlGj/10xRbMhzt0RS+i3ymUXjGYiMJEbfFsl5eofRmTNbrN2YWtuonhnN7MNcEjNQxTBq3YSm1nGXSvTGTEqA+kMfHZmk9gGWq'
        b'+KSEzQn90Vb0Hw/9LEykzjRzGf3GMmEFhdNfmWFmqah3f3UOomS80IeLVXfrHhc3Xj+at2ko6FWtxbtvUY9t6lZbcyOGNk0/0l4J2zP6Ek2YA6+frRoIpR/V629xfH0g'
        b'j1Y7LEUPSYnzk7YiTrqcnJJVPXX7PdSr9IJ4iNKpzsZLt4lk3k3Ut+l3Mc1u0IxwfHZWWmLiEGVKtGUyelPyvjNJYEv97Xu8rGg9mIfy76C7/TVPBJm2Ag7MEyE5Ue16'
        b'sJm6epAeT0il0SLK39UBxtG91vAQlTDUVoL5QVEfiA0UFU7rJPg7CFWVQ7fbWFvk1MFRjfsWrC6XbaZaBEBqkdUixXM7gUCjV3aKcmU72AU8BQMWCbuEXSJddoI+4C1a'
        b'O4FBj0Fb0rs0J1ZaoujxOVvfzRbpQBmk//XhCerrTaGyVSWlZacoGX1rQibDFreN3RBLfTB05qUlW/JNSYil3ki2i1jYCR1ENS4uc+FTw4SrfXmSdePqqhHEY2IiM7MT'
        b'YmI4uWyCrcOmtNSstHhKOOtgm5IclxlLMqf+WhoE3kFp/7IGrGYKk6++2OcwhNwPLKeXe9WvQ6nHxCyOTVGRGg4EAGQRU0Kv/0QDhlgSmvx8UL2gorKuMhk+iXk2ziDx'
        b'nZRn7ogEg3rRqwstFSIm7eItuOxKhc1eUgQWuagFCdNszZVLv0seaeKGBA56xlgtd/f7ssmd1OdEUcWnRLOu7bnDoBkMRgQr0sBs9oCZUfh8c6n62rrfsZknfGnc6+DM'
        b'XkIT4Amo0JhTsQ7a1ZIYHnLs09QaaCWSXElYKNGRoAMPBzFFC1uw08RNCS3/IQ5Zfko8jimYkU0dtJ3ZXx6k5pWSYIdAJ7gUORLPcpMR/VtYMCOIugwl8tmOTskPFp6Q'
        b'qugVjmrljU9iXCw+irkX906svcW7hYrY4NiUxJS4T2M+jElN/DSmdENgLJkS9wTheLeB3YVLCkkWRXfywovThhJGoRbOa6RR2TKGMzsWu9doYXiHQ0N/JN6DXmyqBUXJ'
        b'+000osseUs80vLvksczDZOap1DPPWtfMm8DIXH999pFMNOX1YPcPSeva8xqbkDFkQo4edEJ+2NtcnO1L3jDdaaCZjlEGjzsZHUPpZLw2xmQu0UgOKcTM8od7ErCWz1Pp'
        b'WjszotcSlY8ZJbdTaxNPJM3BM9NE0Ar10Jw86pMvOUPrJ8l6mzb4xweTqbDx3caEpA1JG1I2BMaHxt72CY0VfTlq08iNIyNWfuCmNy29XiI87WgY45KpucvsbT0fdHQM'
        b'tX09+BBZGxuZS3OtdQ+RprTBh6J3BDoZA7NBx+Ar897S9CDl/QfoyzWIh7+yuMmO/MaxOrGKglLfXfxo0Z1PyEK8F5dEb2KCJcLwL8RQWUh2ZaqDwmW8tHkoFZTqnxMn'
        b'9tFA8SjsHzBW/dwqBt+x7QfcaTD/ikE26MGYumkZEwYdkHdNh7pD6evP8XvlEp2DMfB4lIZGJq9svCNW0T9Pn/x+UKxxolEq3QylCpHD3217ZLqBfganhKE60nGA3sad'
        b'Rx7/qKP5Txq0E/9mPJSO2M958z/aizqndL7dD2IVtfR8EXfYMfbDGPekZ+PuxW1M1Exr208lJ059T84WOu3xMOzDfZR5rn0HNeBIF4igHUsxjxteztv76pzzZF8sce3r'
        b'h9cz6y9xQ5R4LTZyeFhnOILlMsEAu8RwCI/BlUGG0WTI9eAyUP3mXquPPYw0/6mDDuNbQw6juixavT63imM1QxAnsFtFemtvzPQDzb29uGgYk0z63N4X6RWNYreNo4vG'
        b'FI1NHKu9cZQ//o0jdeSyHDADPEI5WcJ1bMezQVgGl/CO5krMdONqdnkCDZvwkDyTvNFuhlel9PaEXeuYw3kx3jLHG+zq0U4CeexSx58MYhhc0XGz03Ovg0fWC7hvm5zM'
        b'nr127A5FCnslKnojI4jDsUKA/VgczR64+83H1mwZZT0ciacEMiW67BjANdzGDjgoxw4yWnOtsV2AM7l4LpvOhsBAE1UWGb71yVgskCl7JZtdWjkQWaZLThsfbI7NAhx1'
        b'jmdFxELlLhUFTvSA41gpQKkR1rHbnvAxMtJvT5iJbWOMozbPENjxneqMF+kNF8lm5Qg8J0CNI3ZlU6h3OAwnslkf9Gs6tmRlYluEvyM1NrN7LQGvQwUcNdypP5ZlOn/W'
        b'5mlrZmDFNDepICLNxDysX8WIN5b7u/W5TKW4Kex2d+m8zBVYPS0wQl+IwqMybF+HF7LNaDU6o8KnCcIoI8FdcHeZm02hZP1He+FhiRBlJrgKrnh2GmveO/PoZdZLUr0F'
        b'MSkzlusL7HYzahR2BGkLwWJ/xuVd7hoYZY8lpPQIewUeXDEBr/sHUJFnfwiTdcJpo2SpJutCvbIpey/kGQGlCylb0es1OjWofOQapu4X9c0w3Epil8MkC7wMXcZ4Hc+a'
        b'Z9MlQnKoghMmJNEhE8hzM9DDvCg8KcMDkSaLLUYbzA2HLjINTmKz34ZthokjMoywW7bVAEoNw4yhBffieTe8vV0xHovnuGSTVhyTwRFfBbTOm461I+EomdFN2ZG0mIZp'
        b'sEcP9+AeE8HdQAItUXB9NVbLoASLoNoBCvA2EZwPRI5J3gWNmDcGbm8kqffbjYFO2A+F0JG4HQsk7vakJuXj8dqi4SHzg9jiZ9385rQxouliTy+Recw4letIIZt6kkMz'
        b'XsVz/elj2RW/9koTmvwdx2kYZK9ipzweaiUsy4jUAKFCiHGWxMRs3Bi+Q8gOo63YBzesaCtqDQVbY/Jh+fpNUAlX8BaeEblDPl6YQzWDwzFk1V3BY1FT8dxqE0dS5zyr'
        b'SMhPgOINeBpv6CdBt3kO1oxmU9odT83pXUmScJ+mov7OgXoWVtR9BS4qyP9k4eBlQ+xc4hWpELHbYCjHG2l0FhC5Bw9EQGmAE9kDyDCPMJC64f45bONwxHyLoD5suGoq'
        b'3LLcwdhwSxXGyVAby8hwpYZ4ss+VsBsU9L8V7nUlvGs0qRtdcQHQEk2ld5EghgN4eqzIFzvGMNUTi3PgmKM/6bj9IXwNuAYGOIfbswv/fnf9YzaQqUxUunS66peGOy8X'
        b'CzmRZjmksy9lU8uT6QQKik5vPAKWqR0x1Pqgf3AYa6nLMoMt2LHMPzAk1Mk5NIrTB2tu/8ksORS0Ip1tt7g/fBhcmJDDJkD2CglRaV+SGAsxKQfC4snJxT0XarEWioOw'
        b'1NhFfVljgC1iKE6bkL2MrUo4MiciTBHCweajVvT2LYHOqRG8jQKZ95cgj4xsJe5fa0t00xtw3n8C3PWfMA2apWTvwj0WUIvFXvzO/zy0Z5MdsdXM0ACvm2Fr1jbMy8gW'
        b'CZYqSRjeCGbdHeGIVyOSEumGJSE73BUBr+jlMHcRc2lAkMKZqcehpE72XFCIw/oen/11tgaQPxVKWBsjsWRGxDgogvJILI8iS0PPQQTHyGqqZ8fCZGs8Ld9iKiKF1CyF'
        b'FrKj4BHcx30+6vSMsFU+jzoBtOoLYmwSOefiDcUwrpY1Y9t0LAsmKddhmaeAB6bBEeYXAG2UP1jrVyOCE1AoyFeLSZl5UMmplas2LsSydeOCe13lQqE9yzhjIRzW3Idi'
        b'RYjIlajg59ix6wWHyR5E3a2COBa/DSXIuRXJYbIOY0OwxocDLknJeWZsLrGCGh8W4bAL95PFW65gMP4UhJ9eYzKqm+OyKZCnl+hORoXdRh7yg86gIKJlqjd1Su98VAzV'
        b'5shrkbsebzpqrtuS5ILxBokZyfUCOzPX4tE5QXbbNBwEcGpRDmtU5pIpWOa82CiU3SrK1omt1mA545HCJkq0TNZjJd5hd6/SmSK4SHZFdtYmjxsbNAm7ndkD0txzq+Aa'
        b'68HhULiEJDqZwh8xcuoOaGEzbCXWp2pqCI2zyeyl61pPmACH9QxtoIixcUMVlLJ7OKZ/E7nzjJOrrv4JhT36WEGGJ5+1fjOegCpHqJvkEuCkIFuT4WwxXIDjsxUyNp2w'
        b'2MmTyyVw2YwLJjehkwsgraQHuGwiW8BEE3IW3WG9ZjF9FxdMnOKZYILtM1jroUbPnEkmi/AYE02WYBF7gPXpm5lk4kw2USqawJ4t7EEkHrRmsgmcN2CyiQ9cSvnul19+'
        b'uS3okcP7nZ0GC2KCQybPF9gfg2bSP35haLQgxmnSlBVCcmFrkVSVS4N3Qp/2i7iZOsbdfPLNouWX162pmdz0/sR5qtkrjjgUXv5xQbh0z7sbT+fL7f8QOHmWX6Nwziev'
        b'1DbqY9u3KzzefjfsWf3z9ya2hxq5bPhbdw6Oysw5X1gzaSpcWp3e+OeUhc8Xe1x1eSjSm/vKu0tXfh/wSutqKMsKzn/l/kanjXo/73Z1e16asNQ5r+PKs0+lxIknnmlz'
        b'K/W68MhtlqjwwvOL2vO2JOaXeyxxsu+8bvnnWe+sGTvju6MTT6y8+Fbb5oRx4a8XJHTXRCX5nAh/PTD3wK1h3wZL5zjjx9bfew//20cfmy5/7f1FXlu9/ijb9LrfmL+Z'
        b'juh+pmt4gtXZ5pvPFL4uf+em4mvvyzfCs7udbiTENXh0LVa+Y/fqsGdcJJ9+u/ZP7iZHnp5+Pnbc8ZUfLP/Q2XGjW135jwf+Hvd2pOJ585xNSeU7qk9GNFxbclfy16+S'
        b'ZJ9bj3rz7huuT30zy90+MWtBkeM/wj5NTL+/JHPbbs9TaUecN4jmv9f9Uc75rk1R61I/u3TN8psj3U1b60wWHzywIrHzicQjz87NeGPK1mOZ0Z+/crE6PP3YhO3fWE8L'
        b'vrnpRP5D59DXP3547I+nX274qnp1/at3Nuz3/vtEs9lPG4cfbPf+pjDC+4kdnx0t8d0w/6Hvrc/vd5k1we1Z93z++uN5/a9fuj3cxa35Rmqt9XsT/9L25U/zN+aOxV/+'
        b'+Y1Xrc300fE73KNsTr83z7vjlX3Z73Xdtv+zV2NowJ82H/jQL9rpXHL+Mf1H5sXvC1E+u2WzTi19G73A6+GzTz27Y0P6C8OT/rI29siHcefDgqE2WfXZLyfic33CVtx+'
        b'4BfaPn3bX7OfyXrtyU8dHd0ibN54YsKje55rAmK9DmyqXAHZjfdDXnjxr+fTFm3/csTiseJp359QTOYeLe3kFKlnPhdqhws4ulrtc9GMZZwl68x0KFN7yuDtGNHCZXiS'
        b'eXuMhjbcq9lDZ+N+kSsW6TOjJDTABV85UxzJBn6jj6MOnMRi7iWxb+0WR3NxqMYZwwDaxVvmQiVTaocnh/ds7Tud+MZOXXFZ0pV4jIiq2/FWn5395mTm6BFNlvwe5kTE'
        b'XIjwBl5TuxGtS+YF74X2WMcgKMabtIZq3pMjMzn1V3UqNjvuMHNwUWApUe4NV5GdZ0kkf9bhluLoshPv0nPRiWywcEDsHCtiqnIK6ci6IBfndG+tEwRjqLmOV5nTBZZu'
        b'hKvU8YOeLGEBIVKyH6slcJkwPkiKJ8lWeYEr9GV+2OLoIsWbvAoyuCKehqfwOKtEkpg8dMaKtVoXImeohutZVOzywzqsVUG5QYYJXldRX78ehx5bKOI+PTIhBNtlcIcM'
        b'0iXmvmFKtjDHTXinr8+DRYAETuNeGed6OekNXUELdmgs12Fs1IdhkQT2m2axV7yp4gdE2CvFDqWrM2NE1BfMwiRJeAEqOM1diylecAxzIq9Q9jn94FhBjnfE2Inl8cyN'
        b'KQUKrYJ2Y35fOQmroZ559xARpyo0yDuh59wj4mAHd4nJj5ohJ+J/fl/3MupblmvF+s04YDatXQ2e07rljFgFd7KoOod3oGCObsug2rlEHyq4f8mmcM4CV4Onx/X1aEqA'
        b'g8ypibo0GWEj8ynyJcPaCGVQaBE2iKcNtk1hTd+MjYscXRQj7AI1HEBmmCdJ88RKTiBYhN2+ROZHTqs3MUGQp4rxuBxqec/UQa0+6dR2u56Devx6NtvNt5NCyuAC1RN6'
        b'xJn8Edwp6nx8Ui9phgiVN7k804DtWVPZkBEFpl2nSEPG+yKTaaAxiGVmnr6c1NDZJdQQ9mtdm6xxn9TCximL6i1hgVAzsJerFvUzwfYxRUVJmQfb6kgsDgoOIHtQ+BYo'
        b'Ejng3tmsX+KJNJwfBJczOVufmqqPtLZKYfw/8cVRjP0vor3+DzyDHpj1w7pkxraXyLcBxjYPahg2YDw15owbyYKiuYk5jpuRGtFtNHlOn1KjGcWLo+jkUvJZqmZPNuX/'
        b'xDJ1DgbMk8iCkQaai40klmqeZY4SZ0CemLKf1D/JlORNvZKMxDTKmH/1INmKSQ5i9pN/0UhiyqtjrM6LRw1qzXf9mt3bHYm7CrGosOH02wjmiZSwTevF0CvIqse4aPW/'
        b'NnoaZyYLbbwXrSFjCOKVGq71aGI2zjjyq8OgNs43fPrQIA7VSQoRizELHeK+ld64ihhq76/ft2rokN8U6/BOWJiYRakOY1NSGCZpL+ZgUqlkWpvYlD5QpRzVSqnkoH2x'
        b'tqkJWwdkyr1a7GNilm7OCkhNjImxjUtJi9+kcFHDymr8HbJVCYnZKdTpICct23ZrLOdfVCZTysSBrMa9K5Gcyl5MZEH56kDOBBWP7uRAgrYUHsk2Wal6fHZDiiXgZRvA'
        b'/A7I/FMlU+hWUg71QYi1jc9WZaVt5tlqmxagjIlRUKSZQV01SP9o+oN+TE613TLLhZJl+5Bu3Eo7MyspNktb2x5vEJ05qtvG8GSZ4xL3uSAZUHTZPl2kiZPdkJmWnc5w'
        b'5nTmSJqelRyfnRKbyb1K1AT3HCJBZWtPI9SdSBeQYhlySU46+TUhK95FwQZhEK8S2qFZCZpxUY878ylL7U9jqR59ZRqL0k2nSMS68uwzAEPQQGqiWPua5g1DudGi0BpO'
        b'qgNVRmEhM8wb4TVmmV+HZ4ZrghqgVdQ/rsFLL5uC6NlAFzaprZu2BhJqQr2V4YZVo238h0/O2InN4VAITb5QtcYnIIto3WfISbzfzcA71GkcEfLOYN0i6BqfC5fM3fDq'
        b'amZ90kv297ggthUJMTFGixb6C9kTyR/tpm/HMqLwR1Cm3oM0KIYGG63bpS/YbZTiZaiA8yzxPblU6icyFwSio/5t4VQh+URbtkiVSZ5kn/168vNdJgULjP1e3nDfbYfR'
        b'6eLNMcNv5RUrLcqemJRUY16ZHXdLVvLpxx96OVbJvi6wHnnKfF5LvYen45H7NpPmWm0f+dNz/xozNynhpfPt7+afC/75xqGnZtQkp53Pvb/Z2vOD12b7zAmIdsucOvJl'
        b'l1meH42ueyVYIeciXTnpotreugkR42+aUt3E25ppJl54Hu9w15KrWED9+K02ZVE7Lt6CvXh0kKtevJ2uW9RYRqRBqhQ5w9lhKmjyD3UmfZ5vr7F3DcMKCbSsCGVyh0Eu'
        b'5qvjdObBHY32QiSwViZsGsAZqFV7yUPLZuooj1e2+7Jn2Iin8ZraRT5nJ3WSh+sa4uH2ZMjn0QGjV3HhHm/CcVYt3AOlRvJ+fIytUMmUqvPDuVhaSrS5goGe9tA0gcml'
        b'y9dzZeQ4XHfk7uFwF6t0yaVwXaa5f/s15xFDGqjHVigTRux1CSO7BU8qQFDBgggYEip0UHGjnwOBNqO+dI3WfU9uHW4k1n1P0ATy6zl6gtrqOkHzhLctBndi0NaBOoOS'
        b'gyWanCxajAJN7OpgboSSYsmgkasS5t8pffc7qY7jMyIhVY0h2he1PFvFj9MEtqGR3dfPJ8A3ohcS+WBnUEJccrwqOj4lmeTCWXY16EyJFE0xPsmFveHiR7/7stcGAzjv'
        b'lau6P7yYI6KT1hORou6qElg10zKV9A9kd9e5+6oB2wetg8viqOAYhsiWnZ6SFqvUtF7TITozpdCeWoQ1ejCovXBV2clZHDZdWyndZ8Kv1srXNzLG6fcmjfrdSQOW/t6k'
        b'C1eu/t2lLlr0+5P6/N6kK/08fn/SaTG2g0hOj5F4+iC+oAGJnOKFyzEJSidbB/X0d+jjUNrX45X5wukWPAbzY12cGcsArHvm8G9xWV1BRVW+K2yZ5uLWZ7UwV1sOHMuX'
        b'EylwS3Ls7+spn8goHVXoYeGmewyvB19uycohpCupoCvU2pqTbAdZ8ohnty1fWL+3arTAbf7X4Rg0quTkjMHTgi1WQi1csWPS2Fhn6MZWNzc3PYFaCS8FCHhyO5HG2AXS'
        b'Ibg9yzHUHe660EvFGlGQGzQwI34i1KxyDN2GBwPF5EG+yNMf92QPIw/0EyMdQz2V1NgAxaK5xlEKKbuUwMOzR7AbNbyuJ0g2wvHRIm8acsurVyJ2JQ9bsrBTEMQrLbFa'
        b'NME2nIflXnFLVXkYbcsUC6I0ATrh7EZ+PZUHJ/GECjvMyKklNozGepEDlpswZ4lhZlPwMtZT9wDqHDAJLvGsKuxj+cUHVgjrg2G/+0KW1TI4sq6natOhllRtBxSzq5+x'
        b'rsE9FYNSuEGrBnVwkjeqczVc19QBOvAUq8WRTNYoXyyAqyqP5XBcU3ci4RxkvbeA+nzItxiSwZOkRBuKXJPgMKsiHtBzkJtkmhHpGS/lOonmW7iygYBbUDWMVKRNbioS'
        b'JD5TjUXzHVOyV5Enq7AO8ind9sEI5n1Lr4yJpCrgWajcQaTg/aQW3VAFdZHklyrsJlJfJZGBq6DbQg+r4/RMFNBEfoZAIe6fazucSHMWZtCI7VYKMW/iSbyT1dM7eCeJ'
        b'9M5W0n7axIjNs3t6R5FD+2YnHlVIsqlRF/KhDKt7kkIZHKGDXginWdca4oWEntTrsIEmx0Is52Molqk7yBpvkR5KVSUXlX8rVf2LPJv6xDtRL3mHopul/hffnnx1+p6a'
        b'+qaCp/7wlOKGn7XpF5GTur6McXfzHLdxQm35nkOSdIOnnrp3T+SpN/yXSeNW5+T8fNv1zVrnVcvDd1U6fmxfVnkZsidZTb1fOfm74OV/8hzebe053Dn70fKVh9+0Lplz'
        b'YGzH6jcNP0t4v/wJ6b+mL9vw0hq/kikBQT9vrxtt89OIs6Nf3jDfd8VV4+bGK9Ompia3jLr+eUvrxOM4L+aDc9//9fSmrF/sjhWOX73+/YdFuddHFF3qOrPx3fcLYfyO'
        b'jOnX9mQmnX7xo9QPTbJybo3Lla8rf9TyWsIvD+eNSSZq3b9sdr8ZvvMXswcWqw5mhCoseehk3nyoYpb90b782pNb9o9jG7N9r4Eaah1W2/V3Qj0z7YfgcWbLjITjMY5B'
        b'zg6h7txtWiIYO0n0h0czE6EyHfcFhUGVmTqml8xpLlOXjvBz5BGh0kg8DQUi3OsP+5gYj01ETeigkbPqqFm9rTRuFvMT+eM7W7HTsc8NRThc2jJMbahPxgqscKTmfio2'
        b'G2CZeAm0wJ5Ra3i5+5bCEZUc75D82unNdxkR/X2WcLL3qpmroSwdG6FoBoVvKCLrGa/jMX4/UUDk80LyGPZB1QwZeUzWwqHMEczSK51lRxMWGM+gWZYIZCkcVNvASUlN'
        b'sp64VNi7218dl+oC3Tw89lpEuGqLA+TTm3ioJ3oAtkEHr9EVbzMV7IersAeKaZUqBPLsRAJvSsU4qFdtmQKXTfVIwgZqbz6JF7k6c3kWEFW3A04Zkj1bBFcFPJFJ1CC2'
        b'Kd4VYbtqCxw0zKAFHhVw/w44zXS3zeMmq7ZgERZmkMKghmguZvPZ3dEkuIJnifq1E4uJBtZP+4IjVoPEYA7hPi1VEeGaqSbLdasmMVQZofZKyuhNraXc7ilmKormy5jF'
        b'RxqJNfZJ7T+i0hiIcof19YQmJYZqwFNYyKRxb4E8M7GvRiPStCFZq8ckamMbKV/Pk0MoM0/28cgeWA+Su1hQ072FKkb0w6N6II0OCwh9II/2jQoP9wv1DfCL4MCbWpyq'
        b'B/L02ORUdeAji758YNQTGaiO06Qv9wvWjO2LZ8Xgrahpk2lnrFW8g0b/v2Rfz3SlqqNEjUBnoG8uoWNvKjHVG7lATD49Niqm2NzcWGxK+dWkM7cZiCzHGYgYCIgtNHv2'
        b'AyQSCaOx2GaJNFmJ7X18g43VP1UOor5ka0qx0kXpqnRTGtRJlYZK90RB6cE+y5XTEgXyG/1sQiGklDPVf59Fqb/Y52GU/Es5l322VHpT6i/22Uq5QLlQ6cM+WytHKEcq'
        b'R9XJKY1bkSxRpBytHFNgQOE1q/SrRErfKuMqgyoL+qUcW66vXFRE4bxkRA+2VU5g8FT6jB5tIoPamkzp3Wi6KnmVOFFMUg0n/8yrLJL5bxYkN4sqwyqjRKnST6kg+S2m'
        b'UGE0xyLDIpMiiyLLRAOlg9KR5WzIXHFlzDV3WKJM6aR0LjCgcJ5SYbWcuVgveWBBV4Ev431guGyJCZmPPPpIowNfULOX9X7pkQsRbb2SVWleqiwl++nh5ubh4UUlZK9t'
        b'KqUXXRkubm7u5B+Rvac9kIaGhYc8kPoHLPF/II0KX7L0gXiR3wNDWlh0WGjwKrJ56QsMQ47qog8MOUFHMvmol0g0atVvKdCdFRgQGhH5G1PNfiCNWLR84SOfpKysdC9X'
        b'161bt7qokrc5U8k/k8asOserIwJd4tM2uyoTXPuV6kL0AzcPF5IzQ/nKXEL3BMPgMN+FwdFEAXg0hVbH1yeAlU1+Lo3NobtROLX9qrJIJi5u08n3zBk0nXFEQOiSYL9o'
        b'n4WRvv6PmdT90ax+7/lmpqlUPkzx6JskOG1DiGoDS+hOE5r1a8uj0YNX8JGVzoYr5H1yoQM/MNt+f5g9SF79/zyb/XnoWg3+zP2R42/oiwf6yoTE2OyULDYQbCj/9yJF'
        b'uNLUbInlGr9AIvZUEmnCZ1eyg+yPPIbk3rTxNIaER5A8dUnk0GA1RAzJAwNKg5pF5u3gYVL0awkHP+27+l00aR8/FuEgaZc3+aSy030w5wlP94lHGKpUhT4/SJfqOE3D'
        b'NUfqRxT/LDK0T/CCdpBoaD8LXhA0VJwcDC3RSBuYYDRoYILmai9fX4dtMoAHACfnJvSyUHJSHX5TRDfPISySERqSXNt0Rn3ABAmV18AXnW37LStb+0V+iqFfo0vpV9+Y'
        b'bWvvoEqm105bZrnMdHiMLPnqtLX39f/1l9Vrlr7sZPtr5Qy+rm3tAyJ/Uwr3IVI87h5As+hf6cGMv2oDFrf08NhsNZ2SBtB/sJT0tOPJ+k+b9MzktMzkrBwOwWvvQM9P'
        b'SlNFT1AH3fZAB3qu0nfo0edAjb8O9DhzULj03IzOdPFwcfNSv6I7m55LVDf2qjrXnj/PZH/mWQ/WMI4VoW6aDhwI3j9TVQwKYtDuYdcNXn2D+9ki043qoA7OH7ROPfAN'
        b'XlqW1oH4DBQrQXuPruOanP5HnjFWPWqPZ3ZQdoefEJtFJ5RKwzjWC+yC3iIPghBAbakkn62xmeor/16EEKx3bCMSEmhbs1N6kZjpzMp3YaTfkrDwVdGUZScswi+a0qxE'
        b'sFpqr9s5tdqgncQ3Id4/jApJjZuiGTeNAqW2Auu+ne6xDLPbBp5Dj+HWod+e4jDo/T4boXS+TlWcmK3fFuPAW6d5JTlVN3wBB8Ig8qSGdDYpNtXWLyp8EAt3qm3E1uSs'
        b'3ITMFDZwWUNUnm+Ig6wlsmACsmJTcljCwXc4h8HnrBrBgw9ID7AHnfnqIdGCfPDLpkFalMXdFXphdPdJ2weeZdBdi+U0wPpPukctL6k007dfvrrHRM1V2FMu44iMS0hJ'
        b'S91AcxrCSk7lGIMBwpN5KDM+6uNJs0wW0I4HsEIiiPGcyB664RozeqaRT3d6QWliOZ4yhTJ9ZovdAQXhKhOT4AgNdCgchkrm1D8H78BpvLaCqqiwHzvJVyuUSAUTLBCT'
        b'zGxYNJrYBLuCeuGHauBMB4BtJs/QwG2G6AWKhRmw1xQLoG4jE/5iYK8K8+Ci1iZsLJpvuo4ZlyV6WK2HVWozspNovjmWsMgdrGa24h4w1Z5aaKNm0k1Mwu3xdDCWrLB3'
        b'Do2yt8dS3O+KpU4URZPjgzpTo9qR4SI8h22LuXW6Grt3UtjPiYIG+NNbzC4jHFWyBR+ISZfaxqRMGrNM4GASh1dhY288UH+XwBAsIU12Dcfi4GURa/wl4VBC4+rwJlzI'
        b'mSzAXakcj8IRPbVRGorxJCn+5trezYfuzNxh2xzGT7PvaXpAeHLc7IV6Kspuf+FPjZPLnzQCN/NFW2dtPtz2b4dLrdu+PdhttL7GTlH8lM0ae1ls9/fuPy0Yftupe9a9'
        b'TxfZ3pi0Z8IXSTFLnzwbWtNq9mXH8y3xrZYeZ8JH2T8HtRtnnCu5vHzawZC5YeWvPQ2m1xueCtv3+rrQz2ZnfLF71qvxUWZbr939xCOt5clNxz13pS7xT6pu2/7cmR2f'
        b'Zu5+4ernitScBtcxgVO/fN3VuNLV9N31ChNu9GsdP8LRxZl7J58Xz4e9bl54iwOsVZljJUUyptZW6qJ9bi71ydAXTMMl7tgC+cys6jMPajVGV2wfrvatgEOu3Im4OwNu'
        b'arxChm/qAQnUw5tZ9PpmtTgxKMw5EY9xM7BNNDPlOkGXvXrO7k7pcc/uwjZmO3W0XCQPgla8PABYEk+N4O4XbXidrCmNedUaS5w15lW8gqezqNEsCu7OHAgfCNcjNAiC'
        b'ETNYaW760O3oAhdz+8M8YjPmc3Nse4LXbtintYQzM/g26GIdBAfwRhQU25Gi6AJtI89DRIsXwRFmWZ0zcTXZEYKxC66THogTuWPtvD7YAkb/IwOZFprOazD9aoeFyEjt'
        b'ekr5CaTMmCpl/yixsKlYLBo7iDakhmMLHejeOaRiNJRzyO9AkgsZUqlrt/lVpe5xUeXUkFt60VT6HQL4qlxPgymnqzgtLbLLY0jYA/HgHkgj/BeGP5BS0tMHUsp/qlFG'
        b'+7rUcodV6r/6QF9Nmt1HEzXTHFT+gjaMnuuixmpt1ISDcxeZJZo9RrC8xl+mUZdOulCpZDx9vQg61GeyDsOeVpobqNom2npRWdMrRotdEqPjct9JLRtpcbWop+RAx9L+'
        b'3IWcoJdq+D0SbxbtuCy1PvBYmpZaRtay2P6assXprnhaHWSzsSrbxJS0WGp0sGXMqmoiycE8a2JT+9C49eeoHawWfTQQXSSyWQnbuHidpeVe3cy9PAdx2yTvJCupbNjT'
        b'FT1EeLwNtvaMiZ02jcl+duGLXVxc7BSDSK3cP4K5IMfS2dSLd1mbM6ec5NJ0z3Od+WnT9DBIqqeA2nerL5+kzjzsw/0W+9F7GL/o0KgQH79wJ1uNksMpNwf192I+x4NT'
        b'rqalcx/sIXLYpktvHITfdIjs6H9atZL28FBanxbrTT2rdeamIc7WpSDakl7xCw9dGDxQGdTtpvyYCqKGVIt3hZZ6mE5Y9byh64Lo1AmMVzomJjQtle4UQ/hvb8vqKZ1R'
        b'1NI+ik2hPtN0g9BO3cTMtM2kq5Sxgzhap2RzO9yG5C0JqZqZT5amkvr52MenpaqSSXfRnEjHJbO/kl4etGI8m97WC0XvZqqJmOM2JsRn8f1At74UEeY5083dllPF8vbQ'
        b'OjipMUDV7WXmBLo2yaaoM5/E7Ey21thq56SvgyqN/BDyso1QK2kaQnbqip5DSklJIYsvNpOravxl3XuLSpUWn8wGQasypmemUV512ouka9WDTRYCn/a6O7MXtaFtKFEe'
        b'Y9PTU5LjmQci1d7ZeurtWq977fiqed17yFPp+WxrT74rnGzpKW1rHxYVrqCDQU9rW3sfv9BB1qFDr1iBmQqHx4hg0LpzLdRu9f3YjYZyE9VqrgY6NdfxoUy9S3LdwTVT'
        b'+8kc0wbOmjBda7qYQrsICxY7xjj5rpBxaBc8KYVuSnPhHqchuujIWczcnsZDKVYQjfCI1icK9qdhHUs2Ck9AobFEDQrDIGEyAiOzqVgXAPlrqIKLNUTbHaDk4mk8xFz0'
        b'4RYURGOZmoCBcnNEqnEQgpwdlvs7jVoTGDUov4SaKaHZbxjRd2rxBPdEasRbUMg1vunJXOfD43gleyV56ArlWNe3OMiH+j5F6iqwh8Jmmb0WH0MhE7zcLLElHW6w3ojG'
        b'K+ZUpxwBLVytJHr3zWxGq4hlyiAGBeQcGEZ1ap6J3lQsx0osNJo8Ci4a9aiyC3APqWUlnrWAQjgfCaeVy6DEZxccI3W9TL7OkZ/7Nm2DCqj3iVsPpT6ZycuWbVyfOXkt'
        b'1G5KMhfwgPdYqNsMNbxDCvEC0fOxI914NjaLBTF2i1zhSnI25eB0xlsBrGbQDA39aseqhiWjoGQBHIojfdq7ToV4FqvoZ+o+FmOGRbYCXFk2bCTp2nIe2L9HlU5ds/B4'
        b'kFSQGIpc7aAhO5Y8CJuAl7XWBcVyNTZQenZ2JFakm5hhZaS60/1d3KFDa3ugJgc6OBowEQ2gDuyBRgPmAmaKxdbYNCEkez4t/kQSXB0SlokmiuRNddVTjye2Q5HJksV4'
        b'LduPqaNwBA4GqamMmN9cOVxZyqYNyTWIAZuQBh/2gKN6qkAotSBzvBQPh5PpWCrCuxkmSyZbZVOCXTyWvprnAzd8emXl36PBLu+TIxTKocpyMtZb0ThvayuJALUhw+AC'
        b'VM1kVCnYAbUbePOkfdslxjNYRUpqm0sGJx8LSO8yPz6ojBOwKNw4HG9L2dIbP2FTLyNPcIAi0Nll+VxBBzWJplImfZcn6a4T2RZwCDvhVvYKWqmrUDxLg0OxzL9P5tC5'
        b'hOb/W3IPD7SEbjw8ikcD1evjAcYZA02uauvRdqxlbjccjOUq3hUc/bV0OZsX9iLMEUMpJVSk/5KLQ1aLVGeIijVsvCJkmffBP7mZt4+bE7rl8O3P/2FqPuO9hpfsTlxd'
        b'Y1ge+uyhb5Y/Z2V5WCZPvvqC683xC8obX/6pwFHxzVTbk7dFL29L/Nv2rz4d9YLPlcakfe32ypAFP1ecNd33tfOlZWcc8if7Pbx8M/xczS+Oktf00Ovja+ZjLK3W/uXY'
        b'H78d/9yBLT/sm3Hzj1+fenNprV3OaatNM0+Mcu5+vvGzet+p5kusLl/9dPybMy7t7v428u/7NjY1vX/257OH/tyW98Lwrnfn3EhY/NMXEc+3FH/8ZFpza/1H984/envp'
        b'T/mXXnRYcvnq0axfrJ9d5tPx+fVvRq4+/Wn6+vw5z31s5zTVe9I/P9rx1dvPBX445U8mF68uvhN/5NKnt+cEz/lojvi1+met5835ru7FeSZvXg20qfvmLw/vGP6Y896r'
        b'f2r8NuWDo99UWf7wvd/bp7uPRt/I/8XsqYnvhD3x+lcm+g9nbyh5a+92d1WUZ/0LjVNfHZMRf7M9a0bNt1PFLsfSHb7zXRU4uX2by7nxtz2/Od5686uEz7qfa56OP+zu'
        b'kk1pugI5T81fuPvQlHMr3qj+yPeY6tWHz0VvKHj1DzNNfjC79PPX+i9YNh/Q+1JhzcxKy7AtJcgFz8117hP2jxVLeHz1uclk4vUKYVqWxY1VeDYoi/qIxuAVPRrBNH42'
        b'5yG5s4rHPpVhF5zsQUDAhkg1ts1h4OgJ4nlh3DgE1+G0xkCEXZxtA2vFUDmABCUDLmCTJMIdjrG6+W7Eyz0wCdAwXY2SgAVwnlu8zsNRM23AUQbZDnqMYtXQyarhMwba'
        b'mK0OGqx6UBzE7gwgYmruTOZ4qZqlJ0iZ36UPXGVP4ITNKoqEGwBXtg2TCrIUsZ1dJrNejcbOaQxTAlrMGFXJJtzLIQj2QelYalyDG9CoqTW3vznBFWZ+84LDAWrz25jl'
        b'Ovg7IqGWOaFO2woHekW941m4wqLe8XY0a9To6VPIYye4CEV4VipInUREFMiDuxwy4xTZwu6QA5eb7khvndGa76ZhKTOBTgiDBmYChb3zuRXUbRGcZqFX0AFlaUHBAQPA'
        b'FyVQaym4wQ2ZK9y1ZdWEm3gml0weO+hgQFthRKAwXSTxhtsxrBNzt6zkIWa+ChGPMIP8YLUHqR4ZvDLXEGcFtOFtUgVvse1uOKYweOyYZbP/jntdnAYfsphKibqsh7uF'
        b'eUYiYzELSxcbi2gQu7lYJjEQWZibsmByGqBOyS+MWHA5pbmgn2TqoHNzyUjxSPKT/hvNQtjNySdLkYGeKY0+EzPbpNhUZMlyp+HmMnGunQ6rWr9Yah0mycHMY5lH+np3'
        b'Pn6n9w4UP6IjWlxHoHgFNQ1S6Cmdtso84Uv73tbKx2iobhcgCt/AbHncq0RIlGmdgSRDwtknKqSPYgboCeEJqURFVf2awY5ZB9QaCdVHY1W2K0OCh1A7qP3feoDa4Rya'
        b'vYB8tsikMbu9eCBh/5L+6HYr7AfgUBD9osnEyh2L2VG+IAPbsBGu9zrNe53lKencr6kS7y7Uksi5BAp0n5jMAnIp2RHus8Xb9HGWC9lSXbaQb4HUg3zSer1Z0DyHaz37'
        b'1pF95jCDnrRZv0KAiulwikkbAeMmYmlQ32s/WzzNFKhNayQstOYlyzhjSc5UzhU4bg6ck5OsKJClQFSokwLchT2jWYwC7nPyxsPbPHmYCVzDfawBYavgmtwwk4LCXcTD'
        b'S+gNYQFeZBXzNpHCbSCihgMFE8kREX2gcAuH3irG4o1B9LwI1RMgP1NmLTaOmswE7uluRFq6MzICy6U0yFWAg05reZpO7DaN1o/oDUFnnc4DSW5ZyKct6bkImwRHOZRZ'
        b'PRHqzsIR557ICxp2sTWANXYY3IHCYVDZE7QxWuQdkMaqnrA0Cy7hXjljWSSlOZChPM5SOcGhQDwV2ucurgDqGFTbXOdZEUQ1q4oiClF1VAgUZIkEgzARSXsyiXX6UwsO'
        b'CGNFwsiXxDkusx2ncnzJdQ52wiLy0803XvznSXb8j9/PogiRgptguMnBJCNX6MOALNPMWzrNGAOyNVldwkZhh0gpKEWF4lHCXg0XMqXg/oiSYNIg1YXKzODk1AQNG7I0'
        b'hf4yEJmXVkqmpURmSgS0GtMgHpP0LH59acgnf3xikDNWssAGUfjM2XgTS6BkNhnmBYsTMwIyd6XCnnHCDg9zuEZOpmOsZdJcY4GcPPaCj8pYvmY7b65vygjBSRDMK8Sb'
        b'50rSyGyk5+eCHVjEcQmhzUQNTajBJfTDLn45mkehpUZAPtMM1WphDBTysKkOOLQL2yLJswwTIvlYiubATchjJe62YAYE89M705ympKXwyDGia1wYT1SBM+poHKLvYcFI'
        b'9mgOWdzHoR2asZVMNH1BMkXkvXWXQsQmreUsbFSFUpFOLJfaimzJtLv2u0dsAxmxzGMi5kJ4XKTlrs6sE+mEUSbfmnoNFm33VLhMdqhLKfIt2GEmps3wxFvQzJtYD114'
        b'cgqcldOcyCqCWmhbz/ei7tRgJOPcoU+W1+Fw7CaPozxYoBt2KuCCfBaRfoggKywbP4WVswNqVsrtHRzh7Fy8FkzmeqB4NZ5M5fCHBzF/B7a6BmIneZKBdXqwV4Q1IXBO'
        b'Ieal3dgNV7F7eM+yJZvFcdadm/H6IiLS3OgZhfCc5JYTHwqqJaThTW7vJkQFqSyjLO90nvrq+XsLYIHtJLF7wbDxI4fp+T1dXNxsn7Rj0rB/G2yLqLbJXbn0tc2lgT8k'
        b'OTd9rOdYdt1+d151ofz1K04jXH40uer8wtm1N76c07DdR1zt9eoHO95+/YO/3fmg7vi9F/Ijv33riNVHkc0fO7k98Hz/vNeyC5/D+Hdsdjzz8YdVT7l8r9jxyfTI98Kf'
        b'eCOzwvbcv+yur/962NzxdWGxFspjDtvm3Bt7euVXmxKyf9y5/IpF+Iw/Wx5wsHfoqIxc4VXrYbVyhrN74uGNNmufHNPq8O2IX0I2diRuvBj48cyWf090MHR5fc/098v3'
        b'mWyWrEy6nGiQc6zF+o0tl97dfObY3M64f7+79pmQSx/cer1+8aWm1Ma1SyJiliQ9+9qcjePmGKWMmbHZ123+6z/Nvnz0o/v/OuLzr1mWJ8JvG6XMaa9Z96/qNydkbH/z'
        b'ydwVF8v/ffXlGo/7/w6Xuzwa9WDZG3+cs/LH4e2no881KS5N+q4laXdR6ohNyUdrM/9x9/TIww0eXS8Ex99rsDmbcTmzofnK8Tn/MnjPsO75nYlm5S12W3P/Pib+i+2x'
        b'P1TEvvIX101hxy7+pWSX5NapaQHVU19s2/b8WHu78LZ/yos+URxz1ftnacM9iZ80ZMPeh1OO7oW5BonbnxS2N648HGXy2k+Pqr2ak/XLd60f9vDdVR+Gz88+vVO6xeCb'
        b'Rrdpn2x4b1Hnnnmyr93cls8znROX/dkfftwZ9sRJp7+dOdF2eeWYhne/qZF6G43bWP728KU2ji2VKx5eXNgN676Z/vme0q9eC4/uvAuOfvPzZ99ZHzXrj7PjfxnjOO+f'
        b'izuOXzmQ9tKN72Z8Zezxp5df9L25/enWGV/fbv0u+pV7c9+afj8ubsqk++PHOnsGOCY3Tw+Y7HwgYf2DLf63fpk98vMfc9xaMy+5PjGndrv3wa2lO7e97Fkx4nvDbyx/'
        b'WPmW1UP9MsXDDe733ztz//Uf3jr8/Nsfpbmu99m9/bbqL28fv3Wza2ze7efnfbepreHTD9zfv5ER1nnLc4brragvO5Uvds2o+2XyG8mffpfwVemPNvW3356d+eX6z8Mu'
        b'3p36zJP/nm/6TdQ7IV+t/myJiW2zKk3lVL3x2OzIBwdDJTt9H0m+Db5bFvCv+JM/xReKs7/dPvXmZ3tv/OWZ4wkds09a5oROeOufmeE/frjmyfo3/x6gOBty+L0lm/K3'
        b'aD6/8Ok4y4dXAxSvOU19+uDPhwLefOaw3b0/BMyedtQyNvH59Qm/pNgsWueW1rT7xTcrt48x3vry3BV5f/+y6+1rTXPf6fpLt3y72TfzUhZ+diEgp7Pwl3Gew7t/GfWS'
        b'3zGHhvTnOt5o3ez2+rDdMW+N/WDhwQ3/qFvk9XTTFXfFkdce/vlC9EOr1K/NFNL7675199qjHHFKmbq6TvL2Wwsbvvj+jmnQLz96z3rT+I9p+ffNXtb7OnFk02qzDSOe'
        b'L9/p//OcdW9cGRvVNt7b5g9Tk7zMtrdmxbh99eFrbuvN/+3n9vTt7xRvL3h2g77n3HmiI3eH7/6xrDSp+vsOeDvZ8Q/nP95/af2P483mT3wpu0axiWmCeHa4k5Y8pTdz'
        b'ykrYQ8lTrsNhDrXXFj2Pqa+2RG/Uqq+BWMe18ApHqMdCuKXV9rSa3oZErt8XrMeqIHJOqh9CDeYJgpmbZMO8edxbJS/bohdVpDfVJ7nPyJ35WVRsx7vQbDcI5SRWuxGt'
        b'dfQIpv8qoW4NUdiL6bv9yC+hLZorjIfgPFxxdFHDE8KBcIZQCJVE92QK/d4NWKHqhYdyFMnxY4J3JQuIUFWaRZE7QmZDpcqFVME5M1RB5YFW5qmDJRKitEPVdLwsi8B6'
        b'aOHxkd1wHGuCtHTHzVgpixY7QKWCGTfgIubNCQp2kAnidaoQ0ayEcUw7HU5k4FYyMq5E7hYJdjtkcFA82RoaOdBd9Vg4GkTR3IpSegG6dcANTq9KjvpTcix2xmsb8Tju'
        b'D5II+tgmDoNqNYcoXB6dxZ9TjOfWYDyeQJoIxUSESAngQZB1u0XzsJrB4qhxcK3wIPe6yd++QJ24DdudA0jpRuIV1s48vPLyJnuVQwAeSGfRogdD9WdFCObQIsmaBXt5'
        b'8iY8i2eDGNIfhXHcqUd0b0msKRucSAOswdYgvB4mh4v2MsHQwgI7Gaot51rAdls4r6Kok4ZkePQEI4/leIBeR7SsY8VbYfsSWjdDBbbQpjVhgYQ0rFsy3I2MBj245REJ'
        b'sB8bNbGuzODignd55SuxZQUdS0cXhZG9A1yUivCgYDFSgnk+ct7xhUS+yZe7BGEHNG1UYBlpvKl4zRI4xWlrsQOPksl6UxUq4hJGI16IYdYmFZlHB7GVNJp2uiNtgh5c'
        b'DxCGWUugNgIa2MD5Wy8LohSiiZE9JKJjIF8K9fPX8qV4Eq/iUZVLADQbkzeM7QTBVCaZvyyVW39uZkO7PNA52HZdBjT5k/mpUoiEUZHSJWQWHGTmEDyFl33XwkX6QMA7'
        b'AtwMhxLOT9oBJ+FCkAZhGwspKbQpVEnm4iW8wBdyHTREk6qr0RcV0KkGYISKlSz33V7RpnBdFeCgIKIXVImg3B1Ps26fS/LbO49UvhXL9ASRXCCqzg1SJ9qpO0cE9Bjx'
        b'BDkeWcWinY/hLdap8XbpcJY0oKwXNKOhii+tFqNlvWxUgjFeTDeXWKUBH08ogUMZcnvSDxnBpEZGUA778JgYukhbr7LJOAfLN9MGQStWhziLBEN3MRwdA/tZZ0+diufk'
        b'LgoKot9CsYjIxpcsToY7SWwqOkAVdjmSMXIJoJDOeM6FdAaUS+LClvN5XrycCNP2LhlkKiihTQ8aRHgqGJpY4hl4BhvlCjojaL7Qmq2HR0XYro8HWJtHQrnrVCzmBja1'
        b'cS12OM/3DHQT0b8mlywD2mYJlojgnCyI27QOuCUF8ZsAGWW7XRooxga4FcrGYJnElg5NZnCoiz4cIQveVWKA+7bxeVESv36tHdkK6LS4QTH7q5AbLydDKVbSgWylTBBE'
        b'lYY7ojFw14c9NMObjm70Qq63B54K7zArJRwYD1Ua3cDAk+gGhetYxzpi47Ae11iBbvfUHrwhiM/xSrw6i1fUVSQYYZvrAjHZJK8vZIfWVLhFjpui3SqKjsrXKpmMtN6W'
        b'ZPvFI3BOxb0oC6BlkwoPKIzmkxPnqhNZmWQ7v07eG2UudYBLO7mT4KWxFJtA/YSUsl9vuQhLl0bwqO18X6zXYPeSbugUucJhOMlSyomie4fe32zBVqmAtVAgHSZaD3tj'
        b'eMq7C8epGPa9CE46Q52AB4kWWMkH8ITFSNJlpPKuWGJPFgqeJC/NCuMb3C28i6Wk3vaBuXhwq4NY0IfD4tnYgFfZlM5ZAe3UpTaMmmNKyOTALgnpPbFEiTeXsjWhJLP8'
        b'rBYUnSyJI5hPYdFPJrNlHmk/S0XOrNV4UxFI9li2TUrIfLssdR9PJh9Hu7Cx4xs87VUDPThOZq6CHB00fRTuITs73yNZpxnBPrIrtpNpgU2RfBIWYSclVmbQpuLlqdgs'
        b'ciZrrp2Py5HtWLIRmlVk7A2xZCtFXKXlDMfDEjjlhnvY1EmhY9mxLKgHbN15BLeJVyzFRm60FQumTtRkG2LOPWqLiXZXRuSBC/JsE0PSrRNEC/0NGOhBjhXWq3A/hTyw'
        b'HLdINBGPm7LO3IZHVLwpARnkMeSTlpKT/qJkMjaJ1Iv84jpOKTKbbOU9APTQ6c2RXw9CM7QxKDFXLA1xUgSEQIlrEEdMVm31nCuDs2RD5IJHLeYxvmm1nXraSrWlul6V'
        b'RcPN6T027Gfox2oceAoCP33cAEzZKLxq4Lp9HpdWCqDNQc6QZ50z6L5LzuyLwjCyUOGcKVxgM0IKxxJ6UWVn2HGmbLg5iQ1X3FaoIFNCvdzm40E/MVzC0jWsvxM88To2'
        b'OdDndEuvEcGBmfP5Mr1kjq08XajLYjhFem6GxBBuJ3IL/imsVOlAxCUd0KEnMERcLF/Bm1BrEK1pAS2GHNp3SAs6JFROw2v8rqZ4/DwtjH4vDP0tJCNDaEzO4naKI9ie'
        b'g3ly8iIFVukUQeOa0XxKXghwkWMpmdLTyG5OZ7yBIF42fBmfOZfxrOl6b7LVB4pIsjayGqFuBz9BCratIacJbaZRYAidKySpJRRIsNjDgDlSY5V5ziI7uUIQRKMFLBwV'
        b'x7rcywLJzofXXIkYQXdpxRjBfKMESp392PYQiHmb4bgztjq5uNANoJaiDd8dz+XBhs1WcjrtxYpF20Q2u7Ccg9adJCLHfhXZ26dQU5Mhawxfu1gh9doBVXzjuROA++TO'
        b'rCmQh3kyG/HwWOhmnZC4nOyclJAnVJjv7ECnMlm1NcOc+HB245EMlasDtozS81fQbadb7E/G/i7LVqLvja3OocygscVFb6cIq8kR0cR2BBHeHoWnhnNU476QxtFYwEsO'
        b'mapyCcxWkAVPZDZozhCLocqAnMFsy2u0mqYWoAPM7OHi+CnUyeSmZLZdmhqJnAgDRV6r+zpyWxqx3sKLyhFBLiFkg86ZayWaCy2GfEhPYdU26uBNnbsVWC9yh3YiFNCG'
        b'mlhBCbPaiYdpAEkomgdeUgz77wDbyn7lOUee4MG5skxm82eXPwbUiqb78me34GDA8ITpl7XISGTB8DUoyoYlhw8UU6QO/o4BQ+gwIO9ZiizFoykfuthaNFZ/tMhObC6y'
        b'ZNzoxiJT0STxJNFo8slWjyIPm4otxfTnJPECqbnIRjRSaspQjVne9IpJZC4aLRlLvluTv9mIR4stWC2sjUeSEugllJNEV77mJM1Ilp4jHBuJrcVGYkvRaKkGQYRztNuS'
        b'71NIDmNFU2QGotxROu5keF8NxuT6693ec0d0gnT1WGpJpFvXIHdEecJD6963RIPXiNQlg95BZdJvKm66zOI/KGexQtrvcWZur4d6uh5m7uDGUO0j8lkLKkBS7nqMxyL2'
        b'mPyYwV+gpWXmiVjXZfSvyoB3xD3vaB6L+JMhKizjjypENCA7NJQUVEV/r6bfalhPkL+yvymM+yGuZK4VWKx6hK+/X4hfBMNYYbHkHHJlqRYnhQ5dJiUY5dPA8n8DCYX2'
        b'gHbupNJlSu8XE8lPA6lUqkbqlvxPfhpIzM3p2hVElnM5UgpdUzLyu81uwTCbwZN2eML+gdcS2BQaRLa1uatlREw7n9IHYsBI/VNlNBAqZarSXqlQ6tdJlQZKh0RB6cg+'
        b'GyqdyGdn9tlIDadCP5sp3ZUeymns8zA1hAr9bKEcrrRUWtUZaiFRrJUjekGizOoFiTKyXF/pqYVEGascp4VEsVGOLxAoSMpvgESxK5cpZ2sBUUwS9ZQTlZN0QqFMVk7p'
        b'A4WSpPB6YMYAgRiz96KEuOSsR64DcFB6Pf0fgKB48qB9jwdS37BwvwcSHw8ftjdodgYKfJK5hf5hK/22jXz7LVm7U7SM3/a+52+HONGUxMJd3ftCnLDN5oFRuF9IWKQf'
        b'AzqZ1A+FJGLRovCEjL4h9hzm5LFe7UEn0TZ45GC5aoFD+tZYYdgnDzoeAzM1699NuvMaovDBnrhnHqAd9V/GExnImaqnxhOpwdNwW+W/S41nSLEMN67h9+mNCSPkeAJP'
        b'bKFQZBRRrS5gZ/Kbk8wkKqq7bV3kQdnc/WPvJTq8FxRrlPih8OWj/fmjPF8VzU6Rtj6wVYiY0jAbTk1wHOPa28S2ZPogXKgHNb4uLJRsMHGHftlSkSF3ZL+1+DshSSz0'
        b'KWLUUKc9/fqiDzTJoEU/Hi4JNWT/13BJaAzYBNnj4pIoWSMo8AKNX/hPgpJo1tOvgJJo1tCvvuH52KAkfZflYKAkgy3WIVBCdC5h3e//BlCQ/pFqPKgiNpXGQ9CAs0HC'
        b'p7TJdAHHDgAS6TPOavAQeu5wQBBy9jgMHun0a6gdmpr8FtyO5MT/g+z4/w9kh2bF6UCsoP89DnBG30X7mMAZOhfw/8Fm/EbYDPrfwOAjvdBIFp6QCcV4WDd2A1ZiebCa'
        b'BTk41B5vaW5u4C4WyfEClJgmN02fLFJRNmWPiwu7AvSevGaVZ2vs9/KPeeK3bpRJ3jj/xUsgrc+J3/75zP0n5xVO81REjl4yc1Xxz57zXri1xSRsp1HX5u75WXuN3918'
        b'SqHHDb9nonaoARN2YBv3Fub0fBkqWyizwMoewIQetIRbUMLseEl4Lg3K8LaZ9pJZc8N8EVuYjdghBruD8MAW72COBwBnR3ML4B0oze5HKDHThrp3O+MZjbvrfwQqYMqv'
        b'CUCLOWSATJck8v8GJsDIx5KqPrYZWqp6XGCAJAYMkFkp6pHvdMAC+OhrYAEGlKTFBLAb5LAciAOgkA3t1hyvr6407Vi5ZnktoOKdfj8BT05FvES5WsDTZwKeARHw9JmA'
        b'Z8AEPP1dBj0uwu/u1CXgDR3k31tr/f9FhH9fMDW11KQOe99Mzhkaf/x/Qf//F/Rv+39B//8X9P/rQf9Og8pWKWTv78369pswAIbYMv43MQD+a5HrEp3C4zBuYJoAxVOD'
        b'grN7YNVMoQL3ZFPOMaieAfuptwhcDsb9Ef5YEqbBRfMPxHLGu7bCHktWGLDwAxqfZwi38OgOFlZCJLymcdPDdcOuQVEM86BOSMnFTjsaCq8OhDfDE9nUXB+Id/2CNEzy'
        b'HBQN9mDtQGA0MSWwP2WI3cFwN5sy32Zgq3tPpC0W+zvxMBgsplSzUIfXGdlu9FSDhUunZVPDnT5cWBekkZihPkgtNNOgYSc8EMJ938Ll+lieLTC0uFF4eZiWuTZq6Qrn'
        b'5Sto2HNgSDBcjPSHJjwBpf4hLs4BISQTVzFcl3tAWXiEYAN1pil4GFpZNMiGldAWgFdVHhomkpXzstm9ypQx/TLHYqcMKF6e7pFJw3dZNL1UiIEyfah2xg6WyCMQz0fw'
        b'd7Eh0EkzTJE8jYZkV1iTSBqL5/EW6/3FKjwmzzQ1EWPdXEEyTOQ9EuuYw7ypnYCt2LlVJcE8PC2I8a7IcR4Ws4CEGA+psMhrBOPVKzOaKyRLfk4Qq+6RJ9Ev3I866G0K'
        b'bsaFJ84HHP/5mrvK4I8vF8rdVhpfLLjUFn/LXNaaedLmwrS49w08wyc/VTn37rffB9Tne+TbP+MtuvzKtV3noz1L3oNXjc/XlbrZNBgnWM7a47AgbceSWsm93H/MCc0K'
        b'PPqnVoO4ua3xlcMLps07f2SOasNR04g939es+mznl2tbXL5tuWnlk/bTsarobc2LX9guV/3jYJdN+Pq90bN8HlWXfNx88V+uV7qfKJo1s3WS946WnR9enLwwoSp1Salr'
        b'h9J+6jjlvbCYz6NHpAT4S+0V5uy62w67iKZBZ18WXOsVDTsOLqh9M/E4NvQKh42Hm2rwtumj2J33XOukYLysJhsXLYQzc7gvU+XsidpQ1XlbpepI1Vnu3MuiEvLgAlVk'
        b'8Myafuhty6GKeS3MhDq4oZ0ofpP0OH8ytAncJ3Q/dIspM4/mYl3kvhVKuW/LUaxZq10ieAfOqzlLtugxry3o9knq7WqMx7BL624sxeaJeI41fhyeIoona0TQXDLr92MJ'
        b'KckUuyTBzruYJ8IuyNPDMuoXhHexipM4Y4ErJ2G/PsF/2aIgj0C69Jtp5AYe4l1zHTrGc5fPSLitNkmT5nRxL8ITce7DlY6BIdwljWiyw6dKSLPzInniorlY64i34XYP'
        b'Xp8bXIUDHM1ut0u/QNWCGA0dBwtUXRQ0ULWS/wdjRAN/TW1MZ5GiEgNGPGwgkzGUOUs1cTG9xjcXWYhMxaZi+jx3fH8lSXeIp+HjhHj2KJd6g9+l6g/O+6sjktPvsTTM'
        b'27a9Ncxfa9J/OJizQCF9tO5Xgzl1KWa/OZKTQp0PjOScyCM5sXSNH1RN6BPM+diRnNg5L5teWITgqdksirMqgQdyQosQ5+stkZN97IoEC/AIdHF4h8N42YCGa0L1Yg04'
        b'KJ4ZwXFDz1LnQJraZSGN1BSgIt2N7fxdoWJhxzza5zEpfknjBY53coksInUgJtTDDR6MuXYmO+KysAXbOePXcmwVXLE6lge8dWI1HFWRQ42Sk5DjFUrwBNbwG6+qqUt5'
        b'KCY0xrFoTLJ823myG8bYpAnHlLn5WouN8SryGFJoI1tMTQSWy2ZoAjLxNNzhwXftWD1MHZC53YSHZOIFOMnb27EW7vIAShmcYjGUJTbZzMm6He6G9A6UpFGSBpgnwrZU'
        b'aGBd8kbqQWHl1nliwS0mNHyyDQ8STMixE26wcPAY8TIjJf/jplh/4Y1djMvWIW7XxN8fKPnbw+5u6feE3VEkw3BswDY1Y4sT2UgzAkKw1AkPqXmfyOHTStFeqFujAjok'
        b'HkR4CaLhpyo56TkxdvpisVkktkaxdpWbGwtPLJ0lCEtjjN8x9+GN/TlwhOCfs5oizM79w6SNPExyA7aRr1ZstYRzZob94iQzrHk8K5bHqKMgs+EoDYRcAfksywcT9AVz'
        b'0XiapfHVnN2kqXy2UMGyifote8FJ6rossrXGs7+7c5N+c+dKDPrGNC7F2mR1PCNex24a0wgFRKhlU60QatPlmVPwqiakcRmRKWkzcrFqNgtp3C1mQY10gtZtYvHM0GRu'
        b'ReuwjCzaDmEZdIewOe2EjeNpTCNeC4Y6PXVMYyOc4ixvZ4cRwU0T1KhHZJS9LKrRG/Ylb5y5S09VQSow+vrt7MgAldUs85rpL2y/n5ZyLy7++IufTprwlHvZnkmTRK1K'
        b'FVR6SseK7UMrnvxqpOqLhRF+ExqNIw8di35iz/C7Bc+7P614WvHBWE/V+5/U2CT4/uOlcz8/+sQmoCns0nsO2Zlnfql56ZXn5lwPLJ8e6Dg1aNiPBnfaPOY/4fmKe8sr'
        b'AaOiws917HfUk738Azz/Xu4/PrH4a3r4VBSPKgl5PmtXi8WUwhlri4etqc++fjTqo/ONh0dFzUzB6Sfsj8+8/qLhssVPOL9TU75Z7tlx8aMn5z9oMV7bfPiLR1mHn7E6'
        b'evPud0s6ve5nH8Rj0w7dXbDjQupbD09/cWj1Q6NrUV6tzqVPRpuskYx56bvxS5KaJN+99SCvyO31Lz55pHCbONeo1UV5YGl92Z7XJm7d+2bjDz7/nPKGvcfM486hX95o'
        b'Xz77n3HHL9z1fvjGlm8K3nz3kHXu095+f/17XcPYvz530q1rrk/oL5V1u5/sxntdMctzZde+/bGuqvDPl7u/LzpanVu9fmfnc/c+C3j/5lPLVvyt6J97dj5xb+Q/8769'
        b'8uXO4l3FH3rGVd0c0XH/+dVWK975Z9G4L2bkltt8oZrTcmLJ2BML1pdHXXrP1MPs0cp3Cmf/6emvdi4oSjbJrfjhoznfHVr/wt+fic0+ldV64zMD1SmY99UHH0Q2vni6'
        b'9eRq53nXTD4MenGuw1tRKW89VNmrkpLMQv+87NCwW43PX/n0xOevnlXeu/Vpu/eVtnMt8S0Bbs/k1A//IvS1ZR8YNC87o79s3gulp1++nHzTofFjy0t33KK/3LrWbP55'
        b'm116P4z+5v/j7Tvgojq2/+/eLZSliTRFEFCUpVkQxY4dWMCCoGIBlAVR+oIFGyhIk45IR5oiNpoiRcybE2NMM6aH9PKiiUlMeb68JC/Jf8ruAmp8Sd77/+InwNwyM3fm'
        b'zJlz5pzvOfoNAZ9t/N4qstbg7gvG+jX28+e+uzT+ztRbIVkHVvbavXB6qfvo5K5vqm85vbQ77Ze0W8+6JUzL+nWFdMr5wx80BXyj52/7dXRjwN2Pf5ud8fnUD0w+L79x'
        b'vvzOhpcTqi3zYyYXJH15e7rVjR/rxr3nbf35W42KOfnfT27aFvH+y+11bnc9XvotwqqgML9iQ+sn4/vmRES8cD/tl++Ti1/9+lDK1arv0/q4CJPbuUm70mEgMjpo8nW7'
        b'/rqwE6HXnnL9fl97/k63/uJ7t29MPL334l39j/I3XRrj1GTuKzjn8nnA6953Zr588Y2zl75qSp8T9+ssl9gF5WZ7PopI5n+d9db9l19235Jxxu7Oz54XN5hscU25/vGH'
        b't64+eOlY/aElry08eU8ZVfNZ/ZT0E5F60qujZtm5HP3HqTlfHbt7+4Lk5P0uiztfWoYa7Lo/7vr3bu95zBvc+3T3ym/NJ9suy9hd+8/I0W73n95wu/KAuOn2M/c8umRx'
        b'1Ofewmzcwzg/OcpWy97ojDeVcyWoHLWpQ0oHL1dHlM5micadJ/LDAX549VepojGno1SqA4xCPTOHofwowg/qhZGQN5XWEDOLJN0ehsuDCjcVNO9qAvX0nYry/TTAPIl0'
        b'PcXlVcNRBhI862ilHJ4PTB/vzqlCoSdK1UkiB/1QD5WoWgXLk/ngPciReEircHmT4dhclC7B+1AN3iNoABtUCIc1sDwJlFuF8I6OqJU5HV9dnqxB30kWQROB38EVA6oI'
        b'Bc9DdRR9lyffs1wFvts3hQ7CFCywFGigdagGBlTYO1sbBtHqWDl7OPKOwu7WhvHQjzn5UZZH8OpkLxXuzg/lUugdyoCTTAUrXKXHXnfxDpnJkHcpwdRFHlVhIeuEBnvX'
        b'jU4w/B1D382OZLrMid2oS429E7tAM8HeoWKUTod4GspB3ebTRwDwGPyu3YM+EByJclHx7uEAPAa/y0XH6Bxv24byh+HvKPZuJpwSjsaCz3nag5TN0yl8TobfaoFahp/D'
        b'+tlhaoWDNn+50j/FQ6BCz22FEqq9ppCshkPoOThiSQF0DD1nbUhrjoUrqFmF67NBzSol7wicYaCWdFQFxVJ/Fz0Z/nLUoECNAriQ6EO/i9+1ZASohiBqvEcLw9FpuMK0'
        b'5yKssfbI/VescMaq3kPYvAkCqkbugRp7DTKP4PL2oDLhQmiFa3QRolPeUETAeQlECIdsGUHnwQVvAWctEqF25/FMke7fA0UaEB4F4Emx9jtvJ2TRAfbERH9qCIJH8Xfo'
        b'CCoQxqFLCxjltmJRuJUBNsajUwyzgUpcqIasXBhLEGco1VoNwmvWpiNwAM5Aty06PxyIR1F4/aiQUl7Q0jA1Ag/1TaUgvL1Qzfpc5wmts3G3hyPxjISmK2GAwQbrN2LJ'
        b'uQzVDoPiURieGJXSusNXURCenwsqmqnC4G3H5EKRA7M9CQSPwO9QNipUQfCq4mnDWgHLhgB4FH2Hn6kSboUMCa3XdBlKUyHwxOj8XIrAM95IJ8tFMn4IficGgosg+Dtj'
        b'lMnwAw0+S9Xgux1SCr+DDEdGSLmroVeFvTNKYug71AH5dO0GJeqJUMcQAo/A7+JRHoNmdKOTemrADEHLTLMT6kwwZe3VoOZ1mB3I4ZpADcDLjqO3luuGqqF30BdK0XfQ'
        b'50G74oBKVqqhd+bQytB3c9BlupQ2z0DNRIhdi04xIXYsT79cYo/ODoHvyNmTHmoSRsNpN9rLECsotkf9Q4AgggZa7kNh2OjMFJT5MPAOru5QY+/wHA+owHeQCfjJfCMX'
        b'me4j4DtoXcfOXdJQvucQ+k68xZtg77DE2UU/AHWaign4LkUuoTHO0LXJDKnSB5fQKQ30TrQXHSPIu6O6jENmR6F6cnPfFgq+I2poI0dfdHCarcbcoSK8NinuDgpVKVrd'
        b'4fIoirvb7Thpsgp2p427Qnir8ZYwPJQ1qFQm08Xrg5x+XsI9toA2kRM6hzpUvBmd0lPJz1sCmPi8dQG71YOOzSOnZugkORkjJ2excJUuaBk6ik5ob5KqqyX0qIuKeXRu'
        b'N5TScVghMZcyFBEnWb3IjLfz06Ed9oMq832Bw5B+kUJDF1SvYjaHUJmSbYI6KpSf3z4hZzVXhD/9GrRQ+lkgRh0aoJ84Bl1kSD/mVkH3j3To2DcC7EeBfqgZCthWVY/O'
        b'Qh5F+kGaiID9BC6jIY0RSwaqRGkjYX6YnxxWQ/1wry4w2j+K9+10BvUzsKFgPx9UQBe48ybMtIcAehScJ9kjtEclK+h9E9QUoTnSR+0L1fA8OO1NUWgxUD1zGDgPzq4Z'
        b'js+j6Lxg1MDEiya8xRxlQ7YIUsmocZwRHBYmjd1MxyMMSj0IsQYHy2U6kCPzVsGvxqA00YrIQNofS5TlTJ6Ry/DHrkeFArz3V/OL8GJmjUCvCz8MiUdweK5wUeiHKlVQ'
        b'aK1FKG9GiOYIVn0AmwnFdKh0UbOQHX7ijaGDnn2ijk20avcNcAXvJ+0rpf5SvAEUOGEua7RXuB9P/TU62Ru3Qq0TSXlRIPebjo6Toarg95nasf2twMVTSeB52URMPIZ3'
        b'ZvJxAm6UqfCAB9RTfCLeAWv94/HEPYRQfDw+MXoqo6IzmCX3qeF9qHsv3ZcYug+yt9GPlkIZ5h2XMWvRgH4p4vfofkZkZ6EBtTNQ+didDFa+CC7Se7rWh9SQZoJn5jEn'
        b'00bHD1ACHIM6sTxLWu4d+0gfKQJxgZz1MScetWi62IeO0qYYhjIZ9bAD7BOQBscfgiBOQCUUhSjWwZyPCWibg8k2R/b/jdMZAhGLDjls8rPwU5lSNXAPFUM7gyGiXjvV'
        b'JhC0lIEQoQ2lMiDirLlMbCyeu3E4CBFKo9Q4RHR+BguSaZwgleE5VgER0cBYtjnnuC1XIREXSRkXoUhEaFDByXshPVEFRAxFFQyLqI0FQuoP3oFlwwKpj5/iEMEjCqzh'
        b'ApbGyZhtQqnoitJ3mru37FEw4uwE5rJ10W2JCoooMd1nzY/GFHOezvgWO18GRHRxxLRdqoYieqGztE/j5oVRJKKXbBykqqCIWIBsolx8Emr21mARxZh5lFA0Yp0dHSgz'
        b'SFWMQCLq7FZhEaEb81NSu9+a2dGoaBgekYAR4/EXU1ooRo12w9GIFIuIO9klnI26pLSCFMwBq4fQiJK5BI+YiFroR69HWahU7uoH3XsIKFEwD0sH/QzneBaPWab6RAxz'
        b'PzX4MNFTZvB/jzWkyClqQeDJ0daTLAiHuDFquKGR8PeAhtoaoKEx/mdCM9oY4TIBGf4HgKFQWwUGFFHwn4X2w1BDYwouNKFPkKiUeiILgZlAxC//ryCGFiMhhmYPmwn+'
        b't/jCLC0VqOOJlotU7qcRKMPf6ZSMT2wgxpFGwSPowpF3/sil4WBBIcP8ERBP4ulH33X/3Vp/746E/d2pwQCSH49F+yXWkgf/KNBv9P8lxq8Ot/0RwYeu4f46xk9baCRR'
        b'YfomqTF9xrhk4ZlMRbYrCdJHTtAFnMN4LGBdE8eEcyM8dw1Uv5WHH4HyBYtKtUp1SkdH8ORnqYHqbxPVb132O0oYIQwX5vHhjhojF8lFpJepn2mQaUSzieuFi8LFFEIn'
        b'VkjCJeFa6Vy4drhOHh+shcu6tCylZW1c1qNlfVrWwWUDWjakZV1cNqLlUbQsxWVjWh5Ny3q4bELLprSsj8tmtGxOywa4bEHLY2jZEJfH0rIlLRvh8jhatqLlUbhsTcvj'
        b'adkYl21o2ZaWR+OyHS1PoGWTTHGEgORgT9cONqV/TwqfjP82o+6aQmoA1M6U4rExxGMzio6NQ7gMP2EezlPnTKdBvSWL/NYuVVnyPrrMP+SqSXylhj/BMIQaT5+kOJKQ'
        b'Q8mecZ/uzH670fQV5K8ZIypTGwyVrjaLhjkhqnzqKJJB5bmH7yYpEml2jbhdJANx0kgnwuGZNpxtFGHbttskKuITFUpF7LAqhnk5EsfYETX8nhvRSLPliIJ/HPEe846w'
        b'oal3lTa7FYkKG2Xy1pgo6g8VFTsMIEIdtPDtMPx/0vZExcjGYxRJ2+PCqc887nNc9C4FNbAmEx4ZvZc4eo1IJWKzLIr6TDkskqncfaNHepIRhyuVLyKbiCmqeVCPuLON'
        b'w2KZ+rEwG6WC+MQlKZ40SWQOHZbICKokbJjfocrjLy4xKjIqNiyawBtUMHI8BAS68dCHKpVhkRTYomApU/BT7OttwhXxeFNQ2sSxjlPnQQfVvcWEwmLilCN9yLbFxcQQ'
        b't2ZKew85KvrL+EHhnpjoQcm2sJgk9xnbhCpWI1axHWr4ImFVVTA1rUx1IjMpZR8CzED4CAOVtVyYJTnCHRClSPYLqbVcRK3lwoMilbU8Uib66CfBHwCujVg8v++i9nte'
        b'i/iLmMPiej9flccdzVlD6x2aKzwr1CsVL8XHu7I6KBgJ/d46fQKgig7nHIKL2RaGV3oo7lIo8xxklWkqGU5uv5NJKCw8PIr5maraHUFuhDATkhWqJatMxmtJwzIeDyQZ'
        b'4Y3LEgSRFReWnBQXE5YUtY0SaIwiMXJY+p/fgaQk4pUYHxcbTkaYreMnp/PR7Gv6KiIb6c3g5K8k5yRJyW2dt39wkrVGFCbJbsou58re6EhTclEHtJtf8vmevJ5MjACz'
        b'jYxRJ1a5uskxJOqD9iSsn8hIPHkZ1r46EHsFNaO09VQUXsuiKJ92RqcgzQOdxe0f5A6iJktqIV6tw9NI0VN3LdP9Vm8fRx8OGU/8BstRJ35/LjcX+uEYfdh4nYj4RNpM'
        b'lUhlv8X6MF+GydC7gca/hlK3qeg4blM8W7AqamuyPdnye8ygUQk5BpC921U2lxousCar4+gg4KZDqcSJxKqhbc7bD4exhpwlJbd4P8GsoECapAerf7VQqa7CdbMxrkKX'
        b'1CPg7OaI7aBxBo1IC8dWwUkpu45yUZoQegVYwW6Ei8lESHXYBt0prppaSDe8HRP8ZdDu5C13JdaTICjXHhcARay2qv0HoQROQ6f6trY7H4tVwzyZkAaf3jp3jvUUki3F'
        b'BYrcprrznN4BfidqRyU0VDRUwiXUASeth56QcHoH+eilqDWZhuFLhQIoFqHmoQcEnN4hPgZq4UyyjIhgqGcNy+jitdaLPLQaZft5DTcOLTXUMrdEbbQ+frshiZsD2atd'
        b'4PIWEuQLK6qjUb4Q1ZlbJxNOBplTPIb7yajz10D2KJTrK5e78AnzUc04uIpyTKEDOuQmKEcu1cXqca7PmgBOEWE0C9KMkjdyNPJM58TH1EVcP6f4BDpAthccCyA+l/JA'
        b'aCNUmiSTwilMpNQhZ6W32NheF6vvzWIx9CyzR2dk3LLdJlCDenSYd0LPPLgMnYbxiQIueRwPVwSToG0U9QVYhK6hKqk2CR+Aql2xYuO4E3KoB4G2zljo1EvAr+CWOnk4'
        b'J5iILqpSQKFe6FuvjKdh2kaFC/UEoaiRZd89AIfRCWUCdGCZFV1FDTykCibqo2vstZpFY5RwmdQ5BzXzqF9gtt+Zzm8yXm2lqFLyyOyVolPJxKtq82o8euqcPKhn12rI'
        b'8nPxWRnopXlBNWgoFTrxgEZLUcseV+qJi6+cWDXbbnhGH/rqKpcg9goHxVw4XNHmoNo4+l+//fabg4+YrcoIhY5u8kKsnNDoGVhLvwq1apIPQ6WPLr4I1dpziIdrqN9Q'
        b's/SmQBquhKy+xPUkgJhq1aArUPjQ6kuTM9eo0ztNVItvTzBbepgT1eBKiDq4fCqUoMbo/7j6UB26RKclGE5iVnBCMXL5ae+mn3t/uooJTWqIdfL2xAodo5rT6LyJimps'
        b'UR8lm3Bbdusq6oJyRjZwQkrIBiqsmJNTK1xZpSIcVGjB6KYOqmlLM9aoBjaofGbzygUcvfhGoqp5s5+4LGMfTpXHeRPKIWEBKbWgFpRByQXyQ+jwhO6AUlUja6CeNoJV'
        b'nnxa3yqpqhGzqUs8k3ZyUXdfjRAo8zDnjb7xSUxJX+zoRSZH73z2YHCLZaKbR/q7ozM3as+a/DeJXWmOo7FxrGfUckF+87Nb+tbXVxxdtP2VpT9zJvPE4oYPBS0tLUYF'
        b'nhXFbiV5Oici9r906Fe3O1UVl/Sj306Ej703iuzOhF+O/teivdc+VrpeT4hdfWI2zFj9dNmuM3ZPpT7/1KqKi6OOLT4WsePCpGgd0acveI/zekXnk3VbXny+ob7orCgx'
        b'6KWbe2d/l7+zct5qk8VLLt/szFxZEVHplH9t8R2JeFmp58BrP5ibunX95j2t+wdvv9HjZ/eGZv7jlZljSj9tqb9opWj63tFQ0RJ6Y4zpnsHOBZY3O1a3NHXNrVVsG5gZ'
        b'K33LXWC6ZNrZrftf6rucvznR9++tovde2rfg3rmPBkrev7Tbp6fQr2rsDvOwsRH9978xjHnj58+ODs5z3qNIaHH+cf+GzxLOT87W/Wagd87a+qomaWvhi7/lr55pfmrO'
        b'vOZvb/0tZ9zuWcXnTv5s/E+/ew0vnrXb9MxupyRRSv7Lbh/Nk31ldenbPFHanJSX4+7OCQvvzj9+K6aBrz4kjrtbfs9x05Gcn2eu2vzgi8PrLhq+funTmM+uppVs27zG'
        b'/opO94cz55jNXfTcx28Zv/a15/XzHUETBtIrLqa9PSdl0ly9+ePnr17iGjOnTFIb4674ZbxHu8iyLXty5HtxC97/14udS9a8kfvO0t64C0XjDL4eNNpQZpVbf/RXCFhh'
        b'bd3523czVn77zb+K7kQ9Z3rr1aW1l0p/6Du9Z88P10Pm7XwW9jl/EjWQtPP5nLVPN751yDAn8blV7/78y4cD/XffR5Kg9V8u++qI6TdPFQrbQx7s2N44/zPHX6YEzTut'
        b'Zff2Zf7Wq68UNTtOX7vCcezXsp9EP1TvCqjuvdH69G9L7NYGt0RfGvf2uhX/LDd5/9/8pU+NzDYtli1iB55HUReq2uHl5OrHczxqEcihUkHtMZMIXgHvvBfJNoA3B8jB'
        b'm9xpnpOifkzwhiiPHuHOtt0fON7J21cLv5wlmI/qltNzYaHXHLVXRGwQx6IVp1nTW8moNBzlskgbQWJOEsrbBcExZl3DzBPv0bkkx5oLbwx9nOQg7whnUX8SYTuRWli4'
        b'yFuBXyaWdF9XlL2SugWgrClezo4U86vFhWBR6fzOSSw+7CU4PAY1wfGHfTwiSeRF2hvM8XTIuSnkuUiCN3KSLfwEKGLJduDczH3ylS7ezjIZ9CwmH97FQ79sATsZbRRy'
        b'Q7mCyg9oAkj7uNGT8w2mMzUI3N3oyJDjugBO09pXL/eGtrmqM2P1gXEWqmBNX3SG4+oT43Eoi6Ph66YupV1euUTfyRudx6wd0ueIIgVwFLVBFos5mCldSG0dFdAzIrTd'
        b'WKgWJYxyZGf2V6Fl8yHMQYcip8agSmYAy0YZHnh8ffzkLj5eqAoPm7+qholwXDwX5aN65rmRx1vYwTkl5HmTuZAb+LtAl5znrJdjGcgMWhksoGEiFFrvIT4QBTqqB/SX'
        b'8dCDLqABGiEQb2hFS1ENtOI2/V2c/Ya1ZzNNBM3Tg9hgX0QXktWn31BPRF56Ah4CNXS4Fo3agfono9yVrj5+zt5+As5guxALxg50JnwgHVpNIZfJU6ozf313oRa6ZkDf'
        b'nghXdtFBOyaHXC1bY06iw+vBma10fSzfs0BJLTXQi0qFOwX7MU0xXxyoQk0OajM3yoR0aue2ZXUug2oygcxyG4OJhRpuPaJVEZnXTqMGSGIFR6fGcGKoFBCLTyqzvBZs'
        b't5a6yl15zhJVCaFVgOrGAJsfvEBOHRxhzUad4cMjyaZDOW1fmxhMY9BRTUBXEs21BfpZ++kLoUltjEZHUBFH48CeRkXUQKVAl9yJBZLEkJXPE0IVccbIms6ccQYwG2gj'
        b'H1bgxHOoc6UQOgXotBlb2lb4dvN0Ik5qIia74RGiFvDzqMBQ7UolhjYd/NG9vODAJDrKMjiDaSAdctShdwU2o4zZEr6IKiaRmXVx9LFYrrL/G6MLQsjdgXopdSjnQe8c'
        b'fYo+YRZKbVTJo2y4gpumRF1iHoS5yrnHxo0nzmRXIIfN6BFUFoFFFGpxShYI4ZIAXYCCTYwG++Is4bQBu001NAlnEC5cBgNjKHMyiceE27wZ5e7eBV36CcOCsWejgimQ'
        b'7+Xngt8IWKZtoM1iBksxVzgOTei40kkXS1EyAad1gJ/hhM6ygb7iAzkoX6Z0SmQmHy0FPx3S8F1qW0tdshd/sDcxD6502jOHBC4Xc6bQKhoVAwNswE+bxcVDjZRUzSpA'
        b'rfx8OBtGF8UWqFq4FVLVdWA61eIM/IWe0KeKZmsWb4ROrlL6EF8yAXQLjOC4GwOs1EKvYhyq1IQPnYF5ljXTItKROoIoOr1zmOEOle9im83xWOiGqqihUOOobxmlnMmo'
        b'CBpRJXSoY94KJlhCfhLVOEvEUtxP3BNvskKroYiyiClekCfkJsAp8ayl0MxM6zI7pb8swdsRZe9VGYONrISrMTNsoV0/gAqXQ+WYoTjiKG2RKj61O0pXsmHCYm6BEGUI'
        b'UuDiOjaQZSg1ElN0uZOPi9zF0R+zF8NIYZijB+vdxeVLhnrHrKx4+yKJktpQpmyLGFXNMqIEgrXhiliUb/R4Clk5E6scc9EFiT86B0foOjwwFXpVvmGhKFvlG5ah8nSo'
        b'3YHOScnNZBfo92PkPAp6heg86oMMZkbNCyBZCMqd6D7kIuG0oY8n4wwnmXH33JZVQ3ZHz8ChGKjKeJn+f2+N+B8ZCB8Xd6IL//gP5r9DnEJXYMQTuJBEME6gR2BDPLVp'
        b'EEgRNalJqGlNwmvTvwzwUwYCa8EkgYPAmDei17TxNWL/MMJ3xuIrZgIznkCPzHCZmBCtcW0SahMZcUVA/hnQNwlYidVEjIAppsOPBB8OgSFm5rdeYjXqGwlG0vuvZkLI'
        b'qhuqXTOa3sRv35WM5pMtfKlcz6ThNr7Hf8d/DH+R/ofCX5zXVoe/GNmMJvbFNLVlgh7tO9soIl1tHMlZpetUdzd1hJ/HhcL4ox0MfHIH29Qd/MmS9ER10G0TFT6izf/Y'
        b'WCRtbFA7ZBuzfjyhxU5Ni7YUwU5h2xE29EUSh+FPtcs+clA/RHOyHxL1pMYvaxqftMgmOTYqIVnxmGANf6YHEawHeiHqM98nd6BH0wFH8vXKJPz59NxYc2T8VzrBhj/x'
        b'I+6Jc92vads1II7ElIqNiKPhLmzCtsYlJ40IUfWX2p/35PavjaS1YSGT/kpjC5/cGNI0NnaoscXeS/5SW4ue3NZ1TVtOpK3YsKGQX+pIKSxUxJ9rXBVhJ/zJjT+radxh'
        b'7WMCYqk78FeWsy6NNBFC4j48oQPPj5xWGi6CLeu/xkJom0lxT2jxJU2LY1SBRf5CexFq1rE1LJoYs0Li4hWxT2j0tqZRD9IoeZrZWKKHG2cfjkPzl8bAQNOnbdFxSsUT'
        b'OvXayE6Rx/9yp0bgb//b+KcC7mFLktA/6lDrv0VKIj0//6s/CWWqHfGhrxannS3IC75842UZc+SPi/UZUoBQ8QKVDoTyBb8Tw9RQ7UlFNKT/KEod4iJTTB7a8qMVsSEh'
        b'fzyCKWnwTTLwxI3mP0obqdzZEXFMH9v4/2QStv/nSRD5r41KeWAoUJLLlUvj5GHXNupFfPgCx4lkAsc+/SEae3Sc67g/N847HhGttsbFRf+ZgSYtDv6JgW7Re5Jgx1rX'
        b'jDTpBTGoU72bGtSHIr+qw4Uxo7ogU19jUOezxHgOhHgOeDoHQjoH/EGhag4ih88BOVXUw/+7jZiD8f7MLpEL3duZfQeqR3PUvAOXFrPMrFb04N3LfVFodCQ3mVk+D4qg'
        b'SGmQqCOwH4ufbhC4musxq8zFSAt6hiKnARtImBOsXGb7+pNwgWtWrXEJ4qf6c1s8tVC9pwlN8BsIfd5yH2LEQfnsgIycVokXomOc4zYxOosuLWXGiZJdUMmMU/MiSMbZ'
        b'UGhHJ6lVzwYafTS+3wLUDOnq3CyF6BR92VAeR053yEEUOinnRC4CdH5dMrNslMNlOEEx4SgbOliK3pnQRM2XKM/CUqWfYo09BZURHVWBagPXJqvyubWGUj3QxVsEqRJO'
        b'R4tH+XABdSezI9mTqI86b0MaVHAikQDV7fRmkFyUE0TOOWUuEgszTmc2j5oXwQU6FymoxIOBvqLQUZZvDa5AJZunTFd/yHWBC5DhT/VKyWbedMVqZscqH0dOZPO9SZxG'
        b'X8ilY06jT4yGSs5pvhjypkLNCJKTqklu6RDJjSQ4gSYqnZrYdBmxrcP08wjBjVj05DO1HyG4qf6UqO44UutQ6EbvUF8TVwlLPOsAp/cqZ0HLsAwzqHoJCwTQmQDHlI5Q'
        b'PyyhGJxA/fRmkEw+NEmJKJNO0lxUzAJZd2Ld/KRyKrTT80Zy1rhoNqVhr3gjJXEx51E9qtYWWAWgUjbItVCK0lTJnmZBGgGcZKE8RhAlCagTcsegnuFpriBzDL27DXKg'
        b'AxPakeRhCcpQNZRR3PQMOE1ySDFkVBIqV4OjQqkzACYXCsjuxs1nBXArgjnOlrNF3aEyMaU1X1OUrn4ZjkOv+u0VbrTT89E5aJZDm9vwPGFJWizUQCuqmTIMHgWHCSGT'
        b'BGUoDVXSodeFK7EMeCXgdIwdCO4KXZpLkfXk+6464WZd8Rpxlbn4+Ak4O5SZjDLEsyHHmc6AGx7CAoZ1glM6arjTIhN6Mxb1cSqfekyw2nAVZfDmmOCZ40PfLlRPXPN1'
        b'ofrxrvmo15fS935EUoET/AYcRam+9GCZcBWUQ1fCpHXinZNRYfIUUmkxpC8j9o4nQBMOhPujNC0ohNJdlBo279RXbkDZzPpN2MsYCzpriyDHaIi5YMZyPJbyFn84Ry2/'
        b'2lA2A3O48Y+yMMa/9i9hWcihfi4JreTJuBBjQctGsezheO5a5XDKYSjHFZwyYYEnstajdsKdp7F7BOehA9fovX1eUIaZgZoRmMfypnAN1bP3juxFdZC7ClUOZW10Rcfo'
        b'iliI2VI55g/kBLJutwcH+SKUynhhL75V6gSFATSpliiMZCtvgV52M1cPyjEFerk4k8SfMh6V8ftHQyElsTGrPR5NyuTmSwARYrwcSJcS3GJVj6A2KFChlGZ60Ln1PQTn'
        b'5HAOyh/HvhjvQq1OLHqUOcWddOwScYJQS2jh8KpqR+fZV9dAD3QroV2C9zp0Fo5TJNZm5tjTivo2Q4kE85R+jnPmnBdaUU50I1rKmXCcR5JlaPTtiHksxMTH82le+FVL'
        b'xaG+IbZj2UWX8fokZ7eRy6ZQvecXSdnFaS7anBHHrV+8MzQ6LtByZOQNKqGQ/8n47ec2GxwQ7BfE64VzQZhvJvDhatGfSSGqfOSCXQ8J1z/pzItUxCr2xCcuUOio4kGI'
        b'OOpiYo+uwTXlQ+eeJLMYiYDr7O2CcvAfJ0ZE3IASIWaJZ6EClRjLUbGb0daZcAad2YvOmIqX7cK7yGpT6JyBztHYv3BxBSKxf4kZp8TFNUbkTdFIPqtXuQR5PWauUCev'
        b'K+CgBlr1Qg3k1JlZgZpTnHxgYIaLzAVyhgxC3LhAEab7Hmtq3b8bzvaD5EWhvj8smEe8BciELke9EvVko/N4GyTTvTiRxheLDbVkM40uYIIiU+1wKGpZYCavfB+P0LgH'
        b'HyvWUqeAmor3Lu2+uuvfwXM3TJ5om2B8Yy/30ZlnmxdyOtlrR5k0ijY3PpswVvri0qzmtyRd4sAduo5P7246+aG0peU7cdbhubtnTbLN2H1r9g/v3nh3w+yEZ3Ztutv5'
        b'9Pu/nd8QLcwt/6zdaZbW1teKFkujou49e/20Z4RMsumdHPnc8MkHwrcmtUbbN7m9uFhi9taHeiGbAxL/pexqrPYw/DHt240+2qde3eE6R/npP06m9tT99ur++LaNAzdi'
        b'k3482Cmd895r2cGjfO72Prs+u+H9iXOalY5aijXS+bueTTrYn+fTfOuf7wwGunrojHf1Ht86Sv4vh1V7W8a4fzzux4S2G1sjEpcc3ZB8ruQIN25DuqRhksJm9LXSBR9H'
        b'oYvNh2zsaoMsB4p8/674/MjnCxQRxQr7uxNnuM8Z2HT7lbedSt52Ka+o7q5UbHyz49Dm2698OfYni/SXD2849tuieWfn/91+62tB1p99OPcziWzlG0vMst/Sf+FH/rmq'
        b'V8WBqRufmfXuskujKtcf2fp904Jl70+8lL1DYNZyb8ZHy5BbelzJzyZ7vb4ufM1+zULbuKJBu+SK7yJ0unVujdpiuz+39yIa+/dfbd6tf3besjcuHdq+w8Xm+3qpZVv2'
        b'B2GrTUfvXDt1ztenTuV8tvyFmvx1Ny9l/PDBK83e47p3f+7lrLz3ycyfLt90d0/w26z86uPuj5rbsyJHT70itNocpKh8c+zAsgNFL/W+tU3m/+XtWcc+uH5x+87CCcvn'
        b'vFvy/Kg3j3+7/8sWn6cV+1I3L7/Tyrt/Hjn/2tfTAouc7r6f7dvsOj3/y18Dy+aIru777OY+57M9c4zOGFp/uNDTvW/dz01nWz+v8U+x/KAi7NQbC+3v1f5z7vO9933f'
        b'Cn62Ka568v01u8bkzn+76N79hMoFQY0HPlqeX5lgYP1cbG9BkmHR9RetMy6cGTuvYf4gKNGe+735d6cNCANvuC4MTH19ytrNYi3++1nfiOwuG7T9uuKCZc6ZZ3Int35b'
        b'nbDry6+n3ayddv+bKSZ7Zn7y08ey2cyw3wulMCCHI3jF5U9BLSLK6PvhuDY1HfmR9ItSAlDUcYB8ayyGu0i4Uei0EFVvQteYzTIVnRJKHWVYbKGp8NBxSLPkg9AlC2Yz'
        b'rYKmzcygvQ6qqE0bZQRSo1No8nro5FHPsFSg8mnMEF6KGUqNU/gmZk2npvR1PrS5aLL5Y/ZzRTA84SXers+xqA+GcI2gu6F3uHRlZktvunDj6Lck+E6RSWbP4PTxE5Pg'
        b'yiFq8Xbxn6+x30Ih6nwoFSikebABa8EdOKO23hZhTklRwRdQkyr8G7oC1UN44lFQ7STYgm830k8OxNJCnZQiwfiDoWsFC+AsqGJEZMwkTpDUPAvFqIKYaDHX7WYGobNQ'
        b'NVsFeIdqOw3mHX92EUORwTV35VI4PzyLK1ShiwyNesVkhdKXTBDmsNugVy7mdPV4dBLOoQY23NmoVEGzCDuTyB3ntofwbpPjVHE8zrqoolMQyaUQC0Nn+b1BcIKZXq+i'
        b'E/Lh0Pdyd1QjgEuoIYZW7HAI1Wgw8/jriLgwfjPtsfG0ADxPuRY0szOeKNFsAWpHjVNU6W5dU9RIfSwohKJTUXwUZMcygutElYFKyPH2hm45z2nhGWlN4B3FcJXZZy9g'
        b'dp+mgk6TPnegdh8+WHspfdlKC8qIJTMBi3NroVgm4XTX8ahXD/qZ9RUPerMUnYmnxk4xqsRj1CiAi1gGZ7l058ClDSpLKFTCSRPBBNzeYdbpJkhHh6UboNXHz0mCNYxe'
        b'TB+TMSVQC6irVOmLV9lJf1cdV7mrLhGpLNAl0axgMfXp0XcNVrlBXIRiNciaoDLzhFCCMM1R5w4sMSapQNCo3eOhdKdQMIaNTyHK9tIAhwWcVhh0E+DwnmkqoDycSRjC'
        b'PB5Al/HCw+pA7URm1j/sAFUjgoqs2aPK5o2uiZn3SDuU6WqA3FC3SoPlnozSqO/RJu+pUndI06ROtXVnPevAmnUzwcVTjxPxMltvAeRhVbSFYXOvTZJJMUMqHJZyMw7O'
        b'UgvxDEtUQY3TRGmjBupN7gy4juqhUgNpN0MXIZ23c55PZyQMFaBq6RCeVHuHAcevNtBVZXVMQEelwXBtWKZOqyUs4kAtHt9mCpHFM9H6UK7OZKhleNYmjwSWWxMTSSbB'
        b's9ZBAwPMV3EypS8q9HscnhVziMu0A2GYNWarIa3WqGoZPxpyVJmECyBjP3HixJToT3DfxahSztvqTqKfFYkpogSzwF6jYRk/ZSrvAmtMs/1DcW9Q/jY4yrugfBFzBeiD'
        b'YpJh2dkfs3IomBGLn5HiFY0ZFNaI1Mjiion0iWMyyJKiVC8S/PMCD43J0+lUrJtIA2Vg2TQZ61P1glXxePFQuqjUhTSnlc54SWM+ir/hqlwLq20DPHS7CShdpMCFqVJH'
        b'yMdjJpznJ5ixeAN9cTJeON3DvYAwwTdQT6DVqIzFTJgFmcM83iSYCnLUDm/4X6vM7P8zgu9/H3RzUJeAqUIoqIFK+c8Rmf8/n0Me4kwYRlZEMbPkp4FgEjWYOwscBdbU'
        b'gE4QqQQ5ywuYyZshVHmJHu8gMBM48MYCA4EFT83mqrSf7LceP5aCCYkJnjwzFv81VmDEk4SfDElrJBgnHEtN6Lr4ORvBOPyP1GREa6O4Xp6cW6bIHjZEk68NcZ1HTVfK'
        b'Ba5DX890F9GgTtKecEVSWFS0clArJGnP1jClYtiB6l9IjIH1oTeJUf0NjWX9dfyXkGhABCj6B45gU7nfWPRPXfozWU4WSCucR/X/UWWytHiM0sQUJm4mVBg6w5UAmZDq'
        b'xfO0UIbcB6uemapYSjSQUno0PR1wwHvPYbmPc6A3dajU+FKNRY0ivNOdglZ6CIoqoH88yrWbpenESlVkpvFzRVCK6tElrBFRiawaVevKfbREwxoL35Osygt8wYVEdHJ9'
        b'XFt4YymmXubQaoXOORGXr/MOXn6u3n6r48lo0DQuJDYGOXU7xYWaak/0P0iPV1Eh9KCrw3z4neAMc+M/C7nJDviJHZ7QJIc8FywaraWVTXNf7cU+AEt3WdyciRLyiens'
        b'iPgcatEank+GNe8wdHASBJe4TahS2zAokn7YLrg4DeX6YfXy8aNzWT+Z+FokuzspH6oqUBWpmnwaloH2QykXcUgbz8mxGVTt7DKkZ9seYqx2zkhM4qJK5n4hVhI4j7l1'
        b'mSJgftyrnhYH7+/3j77x445Xu/yfX/fjr7pZo5K/zFplP9HOdnFZQLqrg4d3pt4d8YTosucs5dfT50x3Swq/+0Lc3ZWeellpd14aU7j+yzdvfd9/a/7993qMnvffsq5r'
        b'ZYZFik6t/JUmi4Gaj26l/930eoDPlYjnVi/u0KlbWDZ3fFRv3+JxNisnar0yJ6nZ4bZr85dWSzavtjvY2NPqM0tRKd9dkPjJ32WN/wi3byi985pt/Ovz+c8aP+n86pvo'
        b'zMjbod8GvvJO3ClU+Wv6EZ0PA4VrAmzbgne0vdx6T5J9K+b1VXYJJ5XH7H5VzCjacD72uN/raxpCE+ANfg98HHOpTNvltV7FzzNXvvpZ1GHzVuG6dX22ptEJJzd/+eEz'
        b'6ebRvyLHjTI359fOH9+4LqbyeGqXyyt+jqfyn/V44do9nx/XbgxSvH97YeCtoKqz507f7X6w5+8n2o9F+k+aPuv7TpuzkaXuz6RtKrl3/2rTjjc/8O9/d8nXVve+mfyD'
        b'+y5z2YGJ11Z986P/ltftFOKC7q4pPy6d+LcurRcCzF+3VwaHWn8kNe3lrU7eya2YYjd15d82zdzXUWnRF/5t+/U3XfIPPL9E/8a0lz7Psr80/ciFvAuf+n+dX3EuKuTN'
        b'8Dtv3f53yer0wVc/2r77p9a1dqY3WhcaXAw2D5q0fDBv25ZdNhs8DrRcPTzl4Ina33Z++Ny5s5nvDLp3m8yN99t8oqp8izP/5Rt5KHtf8MTkzbPcTLda22z06M3e/9Fd'
        b's5ffKX82sdx+3Huynf96t2btscG19marX1lfe/do76xJbg8W6BcUT/rsb5sdq69rhb/Vccgn4L0bP+iUH61Za/LSv02iw9+KevOb4hXh9yu2XUEV15+fb9U6kFL48X2r'
        b'f4Z813S8K3njK08febPny8/NvvP43i3pB3f/51rcX9K6GimcM/X+Hs/1incitOtGVyoaN8R5doZ6FtcW/fbTlHHdhl0LN8imJrnS5eoSO9IZDh2PeqzHJF6JJSwe1end'
        b'9ioHTVS5m2MemjqRTLU5F4Jq5Uy9RKdRBVMxJ3mqI5SnwQXmHchcA6E6jnoHop4NTK4+vhb1Mb9qVAaZTBuEOkuWyTxjd4TUCl3+HQ/SWHSKSbXlyahY6esPdajuIQEc'
        b'8hdQ2WS5wlFuqq2Og45ZfA2V8pTQu1SJcn013o9YFrtEm1auQ9lKB7FKbCGfDl1UzLOC4yLUhZksladmogsbpFgZyVcFaonEEtdoHo4QBY0N3TV0Ri6V78J7xLEEGRbJ'
        b'd+MhsJhNOxXmi8dGJlg+VeUX6TiJDpo9akUEqEeD8u2WYQm6Covgu3l0diF0sUo70KVE5jiJTqHTHHWcTDyocvaEDDgjhVqJK55Gfp1gLhyJUjugV6IaLGdDFonISOXs'
        b'1Yuo7O6TEDXcwxZVLqVOtuux7Efai1uCymi4QE7mzwwvh1EjFt7I4M+Gum0jNIqVcFKtUpRYM9G/wBTL8Z0u9mPUaglWSSzNmet8CbRZEHdI1IzyH04KL1PruM1YrK3U'
        b'iMx4c+jntLDITELOsHOIK8GoTepgg06pVQXebr8q1n0BKsJqVTYezTyh3Xrc/TMCEp15Nr1rNYkEnsKbDVbaURnqwLexqlARbsZiHaWPg3Spq18ieyLJnxwynuVGmQh3'
        b'4DE8wzSu8/hWNtEq2dA1wAVOW58Pj5zDVkCHNwwMhUkMSVEHSsSqUCZdj1CQglpGgCumoeOPx1dAlzPtteNaKFTruTK7BSo1F9XuZo7kO5JwU0rUp9FzsY67zJLRQJrJ'
        b'OinRYC1QhkqJhWw5fU28FWvckG+qCXMZwjtaQDPzey1HZaNHgFLC7dUSuhWcpoR3AE6Mg1wiNQjmTOZEKwWQGr6HdtcTTqJO5lKLzqA+VVD9pVCsiqPjCiedXL1RPpRp'
        b'goaqAoZ2QwF9ZnoUOo1ViDEBaiWC6mwCzkIhsjuEuQCd6H5UICI+wXTrh9o1nLYHvxXVRrGoTGexIHAG5VqvUoNXNPLPeAsRlvq65Wy+rkKrhCnQeNIv+erCcbz4fHks'
        b'5FxbSDmDqbk/boVIOyh7mDUHFU/hpgZLRs+Co0nEKwBzuAO/73PssZx5HcNx1Mh0t8vLt42QMbVQsx5nECycho5g3Y00vGHcDvmjzV4J5BwhS4xZUoce/QIh1vmJOlWw'
        b'EmuBrjTDnfsozkAotIX+NXSkQlEWpqpc5/VwhgJwGPzmDKYl4/+PStX/KnDR8MBE+mp3mit/TL2KISqONvVBxv/zRrwZVnDMsBJkgv9hJQirQhY05QFRf4yxVmDMa1Pl'
        b'a5zQOhGrSbhkIhxLfY8taEoEnngY8+R/GnwI16lHyry20ECoR32gJVgdI37MxqROMUukYCwQ8axFbaE2/6hXL1WmVIoTczF583/pl6xSnBxHDON7f8J3pfnJTsm0+8Q7'
        b'zOJxwXsGTUNIUIVtSUw/DCERFEhSZhrEh8b0oZF8YvCPQS2Vi+6g3nCf2UHpMP/VxLHkaQ/y3mbyg+QOovkHB3U0DoGDWio/vUG94Q50g/ojXNeorxT146EDwsbf9P/u'
        b'6GHIe+kKbn4WmY+tuKRtIOJFvLNg0lYaCkjwP/3J6wn1hNQOFwLdWIh6iF0JuDGOY6FFpHAfFtZ+hNsXGXga+IbTJKLW0riA8U90AUsf7g1CjlFduIddwNb4J6/Cf0+B'
        b'C+iY29QZ02dOc3dDneg86kZtSUmJuxKSlZhPt2HRrAMu443hEnQaauvpGujoS/G+n4WOQTEcD1gFRXAiSMxhSapHKkV5a5JHEU5fMx1VuylI/dO4aaGokfpXzEGn1rtB'
        b'9QLchencdFx1Hns4a9Zyt0DUxxN/FdwFRbIRvroSyra6+c6XcNwMboYFdDMPjb5QlO+G0hCJZuXOuSs20BpGoRPRblA6FU/wTG7mGminD680R2Vu6DQU4UGdxc2C7Dh6'
        b'GW+ydWjAbSbJkunBeaBOd2qj1kLte1EnlBLVlpvNzfZHnbQfdnNMUeeWENznOdwcaDamDc6GSyhTKUdF+PJibvEGLXoVzqFzYiVUheIvWcItsfSi7c3HYkCbEnWRtJFL'
        b'uaXQGMNs4hlQCUeVAijCn7KMWwZFe1n3ulD3eCU6OQp/zHJuuSmqpN2wmrJAiefmOP6WFdyKiHg2cp0LoFbptRR/iRfnNQXO0pqn4d2axOvsJxubN+etC33s6Wves6Bz'
        b'3jrcZx/OZz7ksH4UoNOO0Ikq4SzutpyTJx6i183WY52hE51Eebjfvhze7Vpo/zwxyRIjNQkT5kdCYweymSlFDR7Q6Ynycb/9OX9HG9pmABrYBZ0zt+Jur8RT2uhGzceo'
        b'G9pluPJmaMFdX8WtQg2RDOS/AhqlqBKV4L9X422+G7po7TuxUJEvjYNe3Pc13JqVKJ8OCrRM8JU6QRFPPGgDDgppHVtRIbFEZAXhfq/l1uIvqGefP4COrJGi0ySTaiAX'
        b'OHU6G+4W6POWouOOuNtBXJCXquZRqGer1MsFd3sdtw7VrGPPlluhemkQHMadXs+tt0VX2OV8Z3eU6wrH8d8buA3oajhtbyJcCUe563bgLgdzwVPhML3qYyREueGoBHd5'
        b'I7fRCdrYgHQaG0IJGoBq3A1XzhUL7MyDCvf+GJYeSoRwDvdlCkm0giroK/hqFcoKgNadHPVWgpNQwurqgaJJuLLD6DBuxIlzQgXWqvmfCBUBCYiEUbPn7LduYI8fQTmY'
        b'WEpQ6yr8WVO5qZOhkjVwdDr0Q0kkHJVQnw3cYCajmMv6qCwAS3B9uLOTuEkob6/MmZ2CtaIsAXVZyHUicEqS0UzIjY5ZBDVCLJMXYBKikUUGUPloehP/EOpBOzqcyI2G'
        b'i/gZR3N27HUt6YC6FiFkoIvsCVKLy17m/tczAxXi1+kTAs4EKxgl9vh2zHxaQYIN1gw0HcFD0io0xhXk4idsbKhvkSV0LWV9wA9AWaKQ50xG49vosAu9H2jmy14nt4vE'
        b'5LaAfEQZ1NP4GgexBp+pakIL1ePu6aBU1IMfGb2duau1KKGLtaA1gbyMyf0s9G7fQTuoxNzzirp/kBucIrRTDQHKZ35dsQfXkeHBX27Dc6PXmtCvF0ABfd0QGtA5+jp+'
        b'ZAL7sjY4gt/uQlfpAI1HXQFOdA6EqH4eHqD2KPJ5LpBFu5+Azlix3pMuGB/Q2sqNpr1HVYb0+z03ojO09+Q+yoYLWsZsBMZH0bm2jMEXWQfYJ9Cphh7Uxb6iaTRNFrgR'
        b'qrFmQ26iwyRmC9RjguvHo4VO46eWWrDpbrXYx76VPILybFD/PNVo7I+n1UAjptFmVXv4B247m3SZDgpqmUm32fmQ7jX0TVNU1DdmHZ12rOVmsMA3JzFZZ9DmjkBHIh27'
        b'GKx79cIJO9qbHdw+9ciiw97oJH2Ijs1adJYRcJ6hi3psD+MNsgQ65rHBmYx5AjVkHdGHQk1ftKAZc58G9VfjdrvYd6dC7yL1IGvZcqMXoRI2eqV4rVGjlBExEJO7iwkV'
        b'TA9iK6lbSd8PlKFGNrZpZOBI/WkL8R6Bn2gIoh/r5pxMe0nvkzFtn8CG7DjKoD6AWMXuQkc1A6tacvjBfnSGjVsdaqATjtK9V2i+SLXwcINlmNGQsfGCKuYZp+NMb6Ej'
        b'iXRIevZArzPekem4FaK6eFUTKI10NzuFfi+chhpKdXhyquEYnTyhkDOZhfkeHpJeuAonqEPkCmgivnWMs5CzZBLXVc0aNtnTZ7BaVolOMKIkz7ShOkJPJoQ9oI6prJ3K'
        b'0AMaJoXFE/Xq3wDpdNymoPQtahKADr3ZrBEyHvsn0dVpjQm5gn4Ib4PZj5MLeXsTfpuB+5eFqFc2/ndirHArIw+FhN6PhbZdakrWStwEh9XUPns7o4s0rMOz5iGN9h3T'
        b'fgapIEq1/rV1iT+mk4rH6mMZZ6uafZSsYo6nPXDCamhWoStUa7F6vWRvYY69RdoT1BS6hH7e7n3QG54oEySr7Jk9S+U0dyZJuKeN8lEfushjWsofe4cKloWJntQR7/AE'
        b'FqCr0C9S7+rm0cw7b7KBHnHZc7AJ2eUcZG/ALj5YSF32pn6jneD7ta/Kj2/XeGOOYAlS3fbvV+6IYheXLmExZ55auNN5SlIyu3guyIDDXbOY6r/D+azfbHbxw0Qt4l1v'
        b'5DkuUW/9IQd2UdtyFIcZh8fJRRHORTO12MWwadTfUJuzUjoHrFf1c7rEhHMgwW2mK+cd2uLELq7yMMd7HmdUKFXO819izq1dfqeygvx3c+EdN/rf9wvZ5n8KygwhVxGG'
        b't+c4Lg6dTWDiUBZc3u4EtRF4T93D7ZFAD3MzJnO3wQEaNLOPsjcMTb8VahnhwyhSC+3UeK3yYmQJrjSJrdJVKI1BcVRsuGKPOq+VHvd7ea0MdYfyWs2lrHX9FCd/4qxL'
        b'/QP9fFdiGeNxecJWiVSZwjBDr5Qu2oNa6VDZWm7g2ojkoKUIXuO7j5Pp0suXldSNk/tmWphv8KhJqpm2YDTBmcY5zwpWzXRGMqOJk7Fxej+FGLOLNjMZTdj4xcybtko1'
        b'/Vu2sLhGhXMVzlywL7t4yprRhJF4j7OnZQK7OMpeQmmCM9vrvHiXCbvYxTGaiD8Y7/uzXEV8tmaMJtqsk6ILps1kF//tYEpp4sMlO+Y9tWMri6qUqcdo4uX5keP+HZWM'
        b'df21y+kNqwMqUl2z1Vl7xWb29FYlo0pujNL52v4QdvF9jj35zYZw3+8tnNjFT2NVrzvHRgsXO7CLp83YxdQl251325PG/P2j3qts55RJeO6E3+fOX+O30mSR0fmv337v'
        b'7ftWZW+/vdns2jdSE1PfmRN9TBKux038qC27KB2kxba2rvHlSx5EzTDQKsmO/OR247c39nz36c1/CT3GGAYZHoWmvtb39wU+SDlpoDPWIPHZRs58Wemq5eLA11atEFo/'
        b'8/LTHvu7jE7mGfSW+8d6GpZ4ZLzqcaTTI1NWfUO86Wn7Tc/MiIgXr5uWu/PKr1FvrCpeWb00w+TeL17+xz3a5yQZTy69YDz3yreLIhO+Pj7zue09f9823b94W16P9fXn'
        b'Pl1jdQBA0JzySe5N+T9mJzQP3je6M/tOQObUghX/NJs7JsfvI/cxsyrNqnNeT505ya/ovbanDMzX//j09ZnJyzau9mn8YMlHS532VCeY+3lfURSeWdqXXWXyVt7xr45/'
        b'3j8jcFfPoH3AJ2ta//lGdPpAoNuD98a96Vuzc9PbCU1mCb98GmQgvfvOwcMtX6ZseqakP/7lEJtMM1lgY4+td5nn/a7t7ldG9U7TGbDtOX2jZ+LkV2eEV84deHD9E8m+'
        b'9YUx/c/pOAX+vHDpi3Mdgj899O/3rB88e2zZrM4Dz33bPjmgQ/7212jb3I4fawua117Tib8V0Vnxq4HO82E3p/sG7HJ4J9t/+id7Iv69dpk49rt/lZldX3j4u/OWz9zo'
        b'j1p2rS2ajz1q+u6doHN+uRvLb6V8OzbsmS77AZe7+dVlr+dc7nF5fcLXz1a/uF7x1oTb998yN7pWtusfCVbdog8UumcvP7e5b2FZ84qqd8pvrlr4ZpYwVupqtP+Nya83'
        b'Fvzz0ooqres/dDVPfepI9zKDpz+5ExTm+YblOVH4JA/tnTrfpv+ycmmM25LzwWsb3i54vWzLrdLpV1+vf/C85St3+/aHXO82v7d28Fct+xfffbHjF5kBc0XKASw5dlJG'
        b'IebE+wVTSN5hcmxAT6pXHQyEXBbIQoROyL0EqHMGSxMjwvvygJymvpS72EQ6CjgpVAl5lIf6qLVqCSrAG30nSU+sFHNCqEHluoJph7bSA3S75ST5az465yPmRFCEzoUL'
        b'UH+4jFls+ufuJ0GNvJ2d5d4iTrqLhyroC6Zn8p6+O4ac8MS2xAUPtZvTnoavQZgJ50/BHRGZRCQLiAeZvjpPyFVLJ5pYid+It8tOQRCcX6QytwStxRum2vXuoAtxvlto'
        b'y6wVx+A41DE0DLp8iHjZS3gsuWQZsrBMy6bIKRAKt7cSjpgLUIMfOsrsSk1YnB9gqYShbxOxoqXNpwfOUIS1n345VO59JNzTqTiZ5f+t787vn3pq/cnD5UFd5baw2JCo'
        b'mLBIBT1jHiBb3h9x4TnE+YlU0Sge/0+XZxEqdKkzjoFwEg1WT+JgEJcfMxrLwoAGzidxMojzDouGYUycfYQm+LcdjW1BwtYbUWchnjoB6dLfxH3IQXWKzc6nRfh5I4Gr'
        b'IPFTzbmmcFAYFRM57Ej5Dw7P3zXeNqSuPuJtQyKt/yFvm1TuhsWwg2MmRjYvDR+5s4s5sy0ii93acHLTiIDCmiNHAjwYhn4UqOBofISuJpCw6HcDCT8CQ9NT/T/y4NHa'
        b'//HHncRgh9vkI/g/iHONfBjnyj/SlphB3urseJObAprk3PfFRVjwIZ4zm+AolBPpd52DCjHp4OUdQDTIY95iDuVPmLVP4pCCjkTd5Z/hlARlHb5X716oV9gLEQ7Fd0Nf'
        b'2Lo9IjTcIcw3bEdE9FajDV+GEhizkIs6JDm6fZeMZxb87sUoQ66Jn3N0pmQeb+6B0pjdrMFkliaCkw70PxzE6Si6pkanPOYke1C6bbti284QKvbRRTT1jy+iQ5wDyxSR'
        b'Mj6ERM8OITEghlzMhtWsJmlB1DCC5kfQ7R0N3X6G/zLVVaVt/oN0m8p9ZTCcckmMhQhtVErjp3mhYyrQyiNQGgKH8kA1fpAvQTmoGTUFEQujhRRq5gADDEKWLyqWO5Oc'
        b'TsfQSVQh4iRjed0FqI2K6LOcxjpBsT/PoZYD/CgBJ2eQ25X+RG5NjZRyoXpXNu0j6WiprpSNKhzkvv7+JKGY9koeSqFfiWrH0ncqR+tiGXKVo5ZRqF7SzBROSY7bqqw2'
        b'B+jHJwhJOqbWKm4fMCATDU98RST2DPV9y3sPF00GNWSDGIvFNiTvtt7bFtU7b3NK0sNbBb8EBCY/2D2uRcgJxQL7f5cpCVB5esbYT3iuJoWTctK7vzB1ZQMRNgtJDl3n'
        b'Xyc7cPS5CZctPxFzbUmcAWfwySdKQ3zplx83fPJ3npzaXbazuL1XSc75ph46GRCov+vNE/rxa7FS4CIoLbdQkg3ryG9NNBzgGQfi8jG6XWjT9alARpk4hY1XCTxeNbzp'
        b'fBMvFi0B3xEy/aXrtF1ZbcWrHGf2gJNxsiodemm/IO9VETdjHufIOdq/Qy/l3no3V8Bte4/bzG0+cob2rql2dO5t/PtjLiYj464FvfbrlY25tzEJfsKB1dHDWnRe47Sm'
        b'QK43hT254dFEufwquOZjDheo5Lx/HBnh0J06eIRFE1SC90tJ5OL2cXjY9Z6VanNR69IGOeVJPODPCc8vK5b7f+qpd/Sr1rVrjp/a+wKnU7DExuych6hArOTONns3jVqq'
        b'3R7v7SVuSEm7K9b6yMbZ47N3XjgXkXHWeFrVsz/F/Pbrl691phzNsJv4YPt8oz3Hjp7cDd7n5mRN+vCVpa/afj7OtORw+ym7FtOBX7937PVv/yKJm25svnbgrv3ShMYv'
        b'vL8SvL3FUCj8Smvp7bmjn7r3TrHeztaN2s+ZV/8jJ8L5guBq9lNHNzl98OmHcteo8+tgxRt3vip98et73qfzNnW+nXqxePS6mzc3Xg5PWf9R21z/wsrzklOy4geuY29a'
        b'F1y9PaNtxiGDt5c/H+iZ0NlzK/HmzB+OPTBEHznc+iG563PHL9+6/PLhOu+r217slHw3cHRngsS26KdXPw3S8uzJ901ZOafv01dfPBy/5dovZvPLnNzH3Tb80XLC97eK'
        b'Zt9Xvmwuq2rZPnd10fPVHc//khC0+y3v888f+/zo23W79rl8euhWh6NVbMasunXf1D01YVv3cv0Y+Q8W3V1u15WDJV+NvpXScM34V+WV1JCOupdXvfZBnGLB1eOt71i4'
        b'P/OPhqYv/GPTpMmy+Sc+NAvJaC//xGiXzIhKT96QsUYuI36OhqhewkkiecfNau/pfJQJWSQeJsM+aqNCHktix+JQLahgGnn6FsTNxA+rb6JpgrGoA50zjmFAjF44bE/l'
        b'Mm/II9A4bVTPH7Q+eAi6qWPAVCybNSmTdu3SHwdpBijf0BA69BLwPgq1QlQDbXCYyoUpcArVagTUcEEwqkD9E5YzmTEHVXtCrh86R06GoIxH6YIVbgnUXWA0ykQtTj5U'
        b'LkTpkCXgJGt4Ew9UReXCvVP2aURGc8EmLJc2GLJuW9qhaixpqhrUkfK44gpUAu1QpYq26QNH8bsy/Ag0Yo4sCeUnjEGVtFE9LB93MdQKHIEBilzh3VDNPCZy1qNr00jd'
        b'WVAPtd6+eN+SonYey+PZatRLcZCP3NtPNdqb+QPoqELHn4WtRPUE5Ev3O9SOSsUc2fAsF9LPkSTZUWCwr2zKXDyFc3mTxZD2X9rb/4pz8whBdGj7o4yt/M/soZMNxDQP'
        b'ExU2DbBwaUT3VJJxyUhgQ8VFIjiSjElE6NSjgdNY6DXyJBE/JVTMJAIrETSJPzmP71KPcub0oKqfiKSJdzUipnhQFB+WtH1QFB6WFDaoE6lICkmKSopW/FmhU5j4Banz'
        b'HvnxuWYbJ+2Y/Olt/Gvr4ds4OYm13Gr60C6uxZn5iaZCuwlqgextvEpuEw0XA4kUQ23eggihJv4B/8RgG49EndEcnGkEQZE/3sjpyfwFVGeGVS0CTSdHm1jzOonJ2Bh1'
        b'C+EwqoOaqOsXinglWWQpqbvvhd4N/SLUN+xLhW7Eh+PvRws4ywvC+I9fGhYfRfi7vgaD+mReRtKX45+hr+2JX2pmXMTm595IZ5Xhghj/8DSSlwP/9DSeNxo+jWTI7FC6'
        b'ko3Y8KkMgCYtzn6JeK3Ohv9/Eyl8ZCKF/lH8+EQhzUZxq+FnNkHREVvDvcK0I157moSwGf+O0OenL//gFCn/uynamfjVw1P0xZOm6IuRU0ReXv+np6h1xBQRVQK6IC/S'
        b'yf/hOUJHluM5gjpx6PzfmSTiOpRJpkmQKYoQ/cFpGqHkCR87TbosuM0cdAUamQhevxyOMQl8hgMVWv/hZc3vF3F7vjl0Ptxjy6FD9GKRmOdenkw1Nb3FKxax49iSNRz/'
        b'7hahNoenKSXWkkUssYKO2ADogQx0ngxAOoE7nE+kz3+xUYt72sSSiMPRgUbeLAcIlMCpyQEuUObk5S3kJJDlt4EXeMO1qJuKt0TK3WT4/XmrY336/Go90Zs/fz1hrGdD'
        b'hpMWb7z4XmF1mrb2l89mezukBe/dPRi9vHPZko+huCHb55/iLUkOJYP+2u+O+m7LuFvfv5T5aV7ayVx3q5oVb518NUjX+nnTmgKdv3195wX7Lw66vR7d0dOW83zBB79+'
        b'nvi3sF+E5Trjzv3yjkybiQlH4IqWk4uDFxy2deHxnlzJu/igKyzuaQfqXzJMwoFKVI+lnLjdcJk58bajNiimthqSQFvAac+CHDiGJY21frTyaXAB6odOwqIPkJOwdXsZ'
        b'bq3QBpWhs1QIQVexapUtIEHK7UhqULqphwbaqWO81M1Vn2p1I4Y9jNBBpU5e9FhKhM5C5iwB5rBdM+iLwbHUxq0+LUtcSE7LlkDWIwsSL50nem0N6hFOGh8eEUJ2PbpK'
        b'F/yZVRpLTmoMVJAvC7pFGwsSvx62cgNJK6KHkFOPdJNPvE/eCVT3i1ax8U+v39PGD69fCaqC04zHennjPZMN6HhIJVG4RXBKH1WN4Is6qt9Ks4cSz5UKS/VKtSL4cD5P'
        b'QA9w+KGIQhHa4cJwUbr2EUGwSCEOF4dL0rlwrXDtPD5Ygss6tKxLy1q4LKVlPVrWxmV9WjagZR1cNqRlI1rWxeVRtGxMy1JcHk3LJrSsh8umtGxGy/q4bE7LFrRsgMtj'
        b'aHksLRvisiUtj6NlI5IcD3+VVbh1unbwKIU4glOMOsLlC4JH4TvksEoHc6/x4Tb4rnG4Ld1K7Aa1/MJiiXfiTy4j0h2RHGk2MewWSwA3Mh0SFhAJh348wySxLWm4JuqQ'
        b'R4eW7HA6GtYp+l3WKaTdEv105D9m2RrRw6EsW7+X04osCpZWi/xFsmeFsSpWLV1uExEV/ZgEXRpqImSs/Qj7tvWneZzgDKqIoKt7FeqGapLbxyVIhetC5yHL2VXArRBo'
        b'zULnNrHgP93oso40PiEA31I/t1Z7l378WlQeQBJrq/Ipb7PR1kM5m1ngmEJn4jFNYuxMdWZRdrAm1kc1fWVosCpZMqoz9VMlS4ZS1EMN1P4oC844+fi5uuii4ySTupOA'
        b'Gz1ZCFWoV496Ty1HNXPl0+NgwIfnBHCRg25t6FdlYoGa2ZibogG44MtSgU+GHNqmPapD7XJ12H1pXDzJhlKBaqcwF4YMVICuUi5LgMC5viQ0P9QJ+R2Lg6X0/YM2bnJ0'
        b'3gv3irxvOEGI9dPG9ag+hu1CA5aLVPpRlCf5ItSNv6hcmzk1XTbfghUrRyyVNjlM4enRBkpDhegiO8/qi4YLw7La68MlHk6jVHt2Nxc1z1TloZ/ipYrfgN89Tr25Fu9A'
        b'nXLISYKrviyPexiwaEUJcG4/5NK4TONRGgubBV0GrMri5f7quFcs5lVKmNBUAqeZ3TZBxAuERhznGer7o98BFpxuOWoPINEsbTnoh3ZbSEMVWPC2IZUdIQD64cGsUD86'
        b'RQNaZYhnO7oxp4GVvPPnQnZQu0NsxDEKaQhVyllsrTVYXaXhtaBtHKUBg7iYYdG1aGQtVAhVW6FaFY0JKqFqBw2vZeBBAmzR8FoNRskT8T1ez8dpRHyqftQ1Iv5VEK6E'
        b'znrvFtRFaIKqDHhmDOCkEO9qxzdDoy89YHpzt2hHPRsM5xV7LNipU882sac3x0YoeXESu7hpomh6g+pis5GYXbyzQOQ4mV3Uc4uQcFE/7pQIlcRZWyt71oHiuWtgqtHR'
        b'3YrrHTU/vPNxcs641OLa/GdeNIDyMbqTm9/9cLksNFH3pZs7JtgskVQ++GHnxK8Ojt33Vd66mh1m73d5ts2aYvnB2frlcXPetQwz3dP3tn261UDDysWxf/vbP2NPe2e4'
        b'a5Wu/2bD69/LOi+/bDv5s8FVKz1G+2cowyZs+tcnF84tuflL+fflWtPMpxnaP8hYYZKSr1A85VYPwpnjZyT9q3r6/D3xXhMsv3gLNX58f+krpZN9P3V+5WV+c3DL5Bmn'
        b'N5wO/vu0C67vt/nl921e41fT4FQ/5tU12613W7+Kvq15cCX4O6dfX6245/NF8I6bnU1hZfGXt3ybo38/88tJ3eevd5g8L738mv/4td+/VFbpEqh8/mrXP15pP1G25ad3'
        b'OsINArb81vHa5LKfnv7usxfW1G0ou/3drZc2rVvz5pprzs/Hl1V/5PKgQLH52QPi33I3KHS+tj30k+jKjRLbZB3ZWBb9IAZlMrEFXdTlRERqgTpUy9Aux5avl/s6urJN'
        b'WBo9EdXx0AQtCVQW2wGHLSjKn4Q86UKnqDyWyx/QQ6fY+Umxm0yTJwVyFkCZOk/KQZRNcVmHFux7KHGDfI/m1B/ax9MOBkLqdJTrCS1QQMOPEcGZRxdU4p5OBBYSVGnk'
        b'MZNSTkG9JKxGIcpnBsVrkIfK5Suhwl8Fy9sE+bR3utCjQ7OhkOwTmM9WrXMigLBa0Rw4OYG9eyREhnJXTvfhYWA2J4wWBKE+ayrOzYtGbTQkK0ngko85TJ0Ar7XSNdT6'
        b'GYZq94xMV2IMjR54RbVTDM6yedrUCkXYJpwwV3FO41lCVD8VHWFyaO7uWbgGwjvHQC9jn8b/j7n3gKvyPPvHz2DvoQxFxYFsRHCBoiIKyFSGipMDHJbs4QBREGWDbGTK'
        b'liV7CIg019WRNm36Nk1H8na3GW2Tpk132vzyv+7nOecIiiaxfT+ff/k0wjnPc89rfK9xX3e2mHRK4W5uXyQwuJfrn0lPNu3jF+No1j5p3L5oYx10s9sfmPyk5dS0OGAv'
        b'wnb64W9UsTwHxbYEnOeXlHgQ2R+w5Ve0iHBvp6LeLCftdNXFpuczVlvwVyb0XIASKIW7GYGyKn8qaiJTD1zg+nYU2rP9IDnkc0AmiQywR4x5x315L+P0MTa2bbIqf5pE'
        b'O03wQIQzwZH89yXYDo3UvVy463iIDx/ypNWbyrCk76+yZDXOunuqnN7ZCE5YHcxU1Q8jtM7asiFj4CZba4W21YkRmx5whTx1mX9Ph1A+t1N74Z5coBnsEcOjHD7obKyD'
        b'+QyDEhBdfVAGRQ10xNCLDVBgrfx8b5L6yx7KUNyCMPplUP0NgYYGh+m1uCiumpB3xrHTQdwl6dwPK6mgwcWFmWNNRailtIo7J6TB3Y8g/5T/0RLpcfHhL/O8hjBLTwYz'
        b'n778QHa+6LfL/QFqX9hPKeJftVm2TClf2tqoNlt6ouiZwX7R2uc/Ebyw/Ph3NOQ3HCh6UFxusIm7UkAGZ5+U2X/52wzeVr2QHheT9ML7Bf5HPiC+e/n9Auw9SUZm2stV'
        b'JVe6EOEU8YJOv6/o1MozQRJjHhdtHpfB3y57yOmQYg1epvz78Rev/w8VPZtxFcDTpFFxGclpL3mDQ9pXhC/s7S1Fb+tlvfGXNnz52ck2VP1CYnJUXHTcC7f0J4peLbla'
        b'/pL0DHP+tciX7T5W3r30ijQy88U3Vvxc0f0WRff8ay/Xd7Sclrkjci/q+VeKnm3kZJWxhKWIvvgmXrL/KGkEkcoL+n9H0f8Gjpe451/uSgHFgssp9AXdvq/oduMymn6p'
        b'jhWEJncjvaDj3ys6tlhqVbM1l5vUyzuX9c0psacTWoSKhBZBkSBfkCPMUrkm4JwDQs45ILguXMn9zZp61q+q9pzkmS9RIl7MLYbSJ6dWvDmao6/LsVLueu2MWHZv+RMq'
        b'S5Py10pw11snJWc861dY5luQb8czHvzm15zE3AUAme0LsgsAvi0QqJUIs/9nxkLPWsgf2x7CjotLsKqtEHLDeKyagLPPKU5/QX5qmbsB6IsjiRsC1awNcsWlmOaTjJjo'
        b'GGlGwBevWM+G8ZGG7AznF9bUuYKapZXrufRsaDK2xAnCciLsYnAO62wVC4JVT+fEcDmEsKCiCQurLv3XwjJfINGKNjV8clyZC8scsxtlYZn46A/CU8PLYlhg5hcJZOe/'
        b'KcY/7ZdtLjyGh9ga6Lpsf2WGSIfr54Vt0sJfeps1X7zN6dKMZeAtcflWLw/mPHlCMai/vcSmly0L57BD1hd8D3N7HuL8+VtuG8BtuY0mFqeetxZx3p6IQ9jBaMEgSyhQ'
        b'0hXCfXzMF8zC5iPQz16Bu9BM3zkLYQLqoSrufzBNxAWDJlyUfr3jYox3pB/LbPtlnzQ2JjbGL9JHEiARfmxy0STeJPjUe47KzinTAsHorNqfrf72TI7ayvlqaSdlhMOX'
        b'EPsyeybWUtURZek/s2/ynlfcn6d6/sNLbEzt0sS0FfpfWRRzITW+oL9AEVL7PIEcSwLZ/xlp6sHy8NJ5dU/id7lbON08PSMuIcH8kiQhLuoFHl6hYCVFohIQ4sm53D4M'
        b'zha8ut6Idsb80im1Jt243sMxyuns7V1R7/4+/PUIq3cPHfaRaEW/T7//RmJVL3jD74iTtV+4fvT6gk1u5t8J6lZdLbEeFfQPSd8PH5C8H54QbfNxv+TViMRoQYlj1NhO'
        b'5zcdvenf+44xE6ss8v6S++13SRr8Itr4HX8fazXO4txPBvCC7ZLIhw5Mwwgsir2wfQ+XcyKyuiHzBPsHZ8kcwbYXOM+DGMZINMq8Ang3Xu5UbeTrpeon7LZdImIMXeOY'
        b'i9h9L5+f2RsAw8vctTl+4lMifVlBFx8D36OXcZgZ0dwNEtgtu9A0M/uiLRbD4K7AozCkJFBJEG2CwrOc42YL5N7wPQq5UAtDdioCJTMhjB+AXLmW+LxIl1pc+gVuRzlW'
        b'OfxlWcVQhct35v7PZUKrsYoYS8w+efPPU2Yrjm+ZblOjkf3rJbip0GBFO1QxIGvDlUpaLKldwYXdTrBFEpMVlsZSJNPeYqUs1OS2w9tqchj/tgqPiN9W4cHq22py9Pi2'
        b'mhwAcnKBmw6/Fv/5BZFLZM4faWAX2Sr50V9qRD1WZ//zihI6mloiziG9OgIHOQ3Be3g0oEIEN1mZfRzHhWWq2kD2b/rNpyOFKrUmtYIoUTmLn6kWahcaFBpGK3/xCCH/'
        b'FmEIzSitW2osQhgtkKpxMTk11naUdrmQSyTXpHaVonSidLl21RXfKRNa1YvS5z7V4EZjEmVQLorawr1jwL21Kmr1LXX6XpO+F7AnalXpxyTKqFwlyoKrjaEsuy1Fu1Cn'
        b'UK9Qv9Cw0CRaK8o0ag33nhbfLv2o1arTWNeWi6O2clFRZS50x6710SnUZb0VripcXWhUaEzv60WZRa3j3teWvc+9XasatZ7et+T6ZG/qcm8Z0RvqXOyRvaHDzW8jmx/N'
        b'QBS1KWozN0PdKENOzFu9rSOjfPpHEiNN++UO2phl0tvdfPkTTOTTv+nmEpL2S3UACxZKMswlacyrkpoZRxS+rKFoQunc81H0VWQGs9viMswz0iRJ6ZJIZrSmPxVTPJpB'
        b'OiU5TdaVohdJusLsIWWUZC4xj4m7JE2SNZucdvWpZhwczC9L0ti1aK6uzwYtmUX11AQVuuzQkRB3B/PDyUmWGeaZ6VJuBilpyVGZ3HA3Lg/TyvxjgSxWK5aR+bLTDFwB'
        b'FUXxFLbtigIq4iLxc88xyAykX55+emO4JXoqVCtXx4nyqbxUtFaxksz0ou1cuvwr2lhsz7mtinIwP8o5maKSaURkk5lLr8SlZ7BPLrMVjZB5Z6QrQATZgGTmND+mZ4zs'
        b'y3FskPRNdCY1J4mKIvJ4zpiSouj/5pKUlOS4JOpwqRPqBfhkGXhS4BPtgEw3poMXscNsacVSb0UUDquxPNPIj6swGuTtFyCvOQaLWKiJPRLozmT6JAIKsWFZC5Lzijbo'
        b'PZnH/RIWqudAI5RzkeOjOSewxhbL9wfYeysJlC2FePeQO18voxUK8K4tO9cbiHmCK/AI6/ngbfsJzAu2x14SwT27pE4CsYNAd59oy9kg7pqVqK1YuPR2Lisuqs7dyiXY'
        b'ba181h2qMHcNV6jDER9BoS2ppfTkVYL0LBzicNqvTUSCYzosJz7cbvVOewFXd/XIehzydfChIU3KZ4RF3NVf5XZY4c9Xaj2erIq59DPNX8o0ii0h6X44mqrMqr+w9OTc'
        b'63HFm34pTn+FMdBUypE7LjrgqHfksz2pu8wTDAyKulLUD4pc1xi/6u2+qTbAcLeH+O+/cmyZC84bW1ti+umB1yYKJd/7oa7Tb/otC0I/PN1S4jBV7B+WnfW7vp0Xa678'
        b'YOOcXcbbhe/vsxJZ6mz96+8W3n+1yr7MaL2R2sJmrekf//LWu3ozvpZ//ZtFsrrlt//yZsKmjcZgY2Cju7fSJOtuRHHAp9Z5H7y5c/bGrWNf/3n8669vVv3mzsJ90RFS'
        b'y5mRbwd8+O2Q80m1n/wk/M7HH4slBvsSI8B6FZ9O1WjGnRFh0X3sht4I4XYCbHzNQ4M1bksidFYwL4/QQa4mn2/Viw+w1tfv6HkokUfbRXgf78jSveGhO1bLs552C8Ph'
        b'HgwbwxgHKW0h39vXz+ZwoCJ+yPovD+ew6kEsh7IlKVEuQlYJHMZcI/gjhO3QkuHLZ1ZYs2qGDy+tYldkNR7iAofUzW127p/0PiHdfmYH2tmoEFieFB+HKajn4nc+lzNt'
        b'tzlIsYQBAxXoE9kdgwaudVeoWC2PXHJ58q3EKqWinD0B3IseZtBOSJkWTGmjELphDlot+cvEIVfdxdYBetYoLjoQOcMizPI123OvwoCsbjobEbsaCkrtVQTGMK3kjTMp'
        b'3Iqdy9JkEbKbzvyiqBiKtLEcH3M59vAY56m50sAAX1ZZj8vFv3VemZV1EsMd2ot5PkY3CTXYzIJkxOrHBDyz6wSL/XHamqv2GH/Nnl5mB0xZGcUKb3+sZsUKoGKbrz1X'
        b'65FVrPCCMVW4g1Vn+Zl1xCfKcia4jIn1NI7m69DNd7ioDDPcERju5OUZGJcXT9x3ki93344lG1iGM3XC93iBZIyKwIjaIiEEg89mkH2RrOyVAmMhX9YQcGGoUYXLQNfh'
        b'csm1uCvDWRb6es4s4ENYWcbLVfFzLvBWKNollsILAoFi/tkVwldrNWkyrl/OcMgVvLf0bONzh/xFHd7Kn+f+3acpj2U93ZUipOWs0N/PKuwlyvmlYlz8MNPeELwwBHNA'
        b'80s4x+W6dpl/2pGHRwwWif9/56GOIQCWuRIAY/9b5qROkyYmZyguOCYkGZucmRDFgM8laRpnFppLYiQMl63YliLfziNBKkljt+YeVoAxmZebA0ZxPPBj7pZM5n1ZsbF0'
        b'aQYDdOHhIWmZ0vBweaDG5mJyUkYyd6rSxjwhLiJNQo2zqOAlSVyCJCJB+lw8laG4s1q+r/RaclpcTFwSw3QMjXtJ04jyrtqZJ7PluByXvnJrfBxSMUBPSUI6jfBlPfh/'
        b'H/cVcR78V6yVOQ9+3jtyH/7MT45YCzl9dRCrhUvEI/bCoLe/QkBGbviv+/AvZG19imHTIxMucOv+H7nyPV5Kai0uc+YzV46llF3mIzPbcYr94hdoT1DiiQahZapfyavv'
        b'HCYwWa/jpmb2gjx+zuVYKPzCefy3Pt+vrxTARSH0sT/zKd1awRI8i/1sfOxgIITP9WQfBPoxP5qDEAahWNNFANVxuSkipXTm1BkK2/z7cAeD34Z/O+IXEisDa4mfJCE6'
        b'IeKD8PfD3fyToj8IL4nxkfCHqJvn1MwnjazFGSyrFJv87XCSVu6pAayo2HPPc6r5unHAbizVfE51c2Us4StkD2/GKbyVvUyHKwj00F55KODFSloRjPjSju0IlrfyhWj2'
        b'c+ISK2SqrxCc8H8pMp5alq1+hN4OgVEceAk6ZqGKM0ECk0M6R7enykIVRyxTib6jLO3lkYopzOfslISt0ElvYJ7QXhao0IP7cZHfnlLiqiIMPxyRRykM35bHKRJifCID'
        b'uEiF6fJIxde81XMm9Z+NVLwgxCR56V09qaWhp5Rl8rxdfTZq8TmjOPRS2/aVpVGl54+GZB3zq64sVdhCs8x7kirKJFeUFXJF/MIkd9Ldn/Q+o1i8SPVI5LhoqRvr+a6S'
        b'xDRpNO+WeCZ7aAVvRpo0IzMtKd3V3F1x0b1s1uHmyRHxpNNf4IVYGcwoB2SyNYAebNvJ2V2M4EOPnYyFXPsTJ1fMh4fcHerxB+BxJmNAi+22LG3Y+eQTl8XT1nmQpiqW'
        b'61jEnfd9TSndn9458wsSkx+E/y68Yfs3I2KjB6Qs8PJqxJAkNtruhLXER/itIuFb/mXrtMzHTn99zdftottP19u9m/DupvsGP1y1tTJBO9JRHKMiyDuib/HrUmsVPqmz'
        b'FgdjZAarQINLd3U9zxmF/rvOLLUJ6d8HUCnK0cUhzhI+E6W2xFTm7WTvHCW1bDLKOHdIFxZe9D3rwxvazMguMuQSJlXxVpIvs9T01/KWmuZpdllWpwtv8rViRfAy6SxU'
        b'XVr6ospmGZs+39RYWg+DnRGS0QnHuK5flnFT+MRBNe6Wpqw1T7HMkuaXJ/iFLpfFK0dQRPxjT3CFCY0x5KU4e3jVUs5+wTBXZupn0lJeBBPkZ1amVmTnjGeTgZKj5YdP'
        b'/u+5253v8wtwt1DwnKSFj9/4iiidnVX2L/vb7wmYvB8eGz0kbVrXJ3k1QougiKrA5hMly/44axEHGCKwRR1HsJA7qrUkxXYNtiplReI07z0axUENX3keMst7rodpdpCj'
        b'ap0cYK4cp9Z8aZVzQ8ASUVciBdm+vJBihc8hUTaeqJci0TadzyNR2bhknb6tmi65JL0gSQ9Y2ZPPEl5lakiFM1hVvqAfn5mRESuZkXLyZYGNKFmB/S9EvO6KIIw0Q8Ky'
        b'/iR8ZlRi8iXSa6wkvrzd/xbl8+/IFsiVufu58IsdM+kSM9MzmKnLc2J6BjMLWTYic02saNrx7oplmWzMLKTGVwoQKJiOjTVNcplfLprzC3iNEZreM7ymEZDJqNoiy3Kp'
        b'HuWVKM7g1HMUqb+ErzmdC7VRtj4igfkqobcA6wyhjKtBc8X6fup5Vr5GO0VJoNQozFBt55zlqTuUBVf8+UM29WuPCELSFogIuKbs0uG2baBIgA9MhEFkW8DIjjilwbXK'
        b'6QX05YCy0L+sQ+fQcS2P+T+4nXdUUn7lzx65gryzh5zUXz2Hh5wK37s42+7o//2atkNHyyuiPPrRojLtf38WFzT+u083fi13+z9P71BP9d+xXvJjyR3Dm/vvvl25b2Is'
        b'ru/Ort4dU43f7TTEmrXXGsLfn1u8+PDx4H3/n879O+zsmfvhJb/4efZX/v2xcOzsFqvJg9ZqfB26SSMNW2+4je1yRzMMXzLkz0rUQDtMQte25bpblHMa2rj8qqRA7OAU'
        b'N7RC5VLlraQG1Zmc6t5vhR20pI5yj28rdhjypxEqYQiaYAombW3khyXU94rgnv0RTghaYVcI7/A9B4Vyn6/c4ZuKHbwruwonWB3lEhNqeMlFtWMX+aJ9vVgF/bbbsMTO'
        b'6qLcUb3N4TnKU+WLOkzfVpUdFObEqPeXF6N6WrLiGwZcbr8Bd6pAS7hKmGW0ghCjjpb7STkBukb0BfCAeMmzTySuGf2Z/FISt8ZoqcR9zmBpIQPlB5jfVlekwvOJEOoi'
        b'dgQ6QZIUE+IZqSpjZjYNAzkzBzApzM68MqehBhcCZ2F3UaFuoV6huFBfFmk1iDaQSWfVInWSzmoknVU56azGSWfV62pPkMUvryutIJ3do6JYznyS9PLypCfmEuPDmXz0'
        b'NTI5LU2anpKcFMUcd88/7koy01WSkZHmGq4wfMKXucN4f52dzEumcByy+PozjUmeG083j5QkMWmclsxyUOQpwxmSNFp/8whJ0sXnq4RlQdinMNWKIdjnKooXKRe2ECxG'
        b'nJ4ijeRmaMev8oqq4slJjaTMxAhp2hcOKCsIix/GkyMXl2PjImOX6SxuRkmSxJV9lsm8+1S+DrHJCVFEzEs04FNZ8ImStItP5UAoNi3dnD8y4mAeKPeT8q9LM2KTo8xd'
        b'ozOTIok86Bk5fA5fsSH56CMlCQlS5maOTpYpVMWRcp4IMllCPktgkKzYzlIaeu5KKlINXc2fPk/yJBdb3u/zcrJlbUU4RTzbytJTKZ/zPpMMhD6CA813ObvYb+f+ziTp'
        b'QkwYJZVvlbwtIn2eSlZ2MB+WRksyEzLS5SyiaGvFHbdMN+f+ZIkmzwxuGUSRUSabSgqZCPTbFwBYCuTCgutrnkEuNgH8VRx9YnyU7pQmEgiTBcehD2bYRd3cN0XGapqX'
        b'UoUCIRYJsNoPW5Kw1lrIoQ0z4RnmFCPbGCqE2qkesBDAZSXEXwynV47zkMfKwd4Ki7bZpPod9Sf8MxCSguMZJ/jcAKi1Ud9z1Z2L9uPUHnywLJWBNzKCfLFLkcgQeV4N'
        b'OliVXg4I/dRNm6u4HR6XnnA7+rwg05o+XA2tFxloUOQicJmVOIZFvnbW9j7KAjdbFWw6AB3c9Awxn9U2q1ZZQ1aGPiuzUoElXOPCq3yN6/+5cc3vn3Y2fLGWLbp8kW5H'
        b'pZSEY+ss+A8HQ/lq4ILES1pRIhGPxBzglhp2JeAQKR5NgSbmYRNXmYsvAO7PVwUXuEf4qZsGCDKZRtyNo8pcqYBgb6yAfinesT1KUyizZdhRMR36ztvOx8/hqL2NigBL'
        b'rbVSz+pksgzC8G2nngGfZdY+/n7QH0KwMxPaZIF3yGPHZLuwItPTWo07Zw51WAhzslAx3sd78gP27XiPvxx4Hidg0BdL+PP1hw22wQL2cV9thwoW9OfOle88wx+x1zjM'
        b'nbD3xWpnbAxdfshevDoklW+z9YaZ7OA7DIn5g+8+6nxt1w68h0W2ooNPHX6PgEaY5A6+H/XRtpWdN1XfLoolxHiXFmmBq+gUb6b75OD7lmP8WdInx95zzlhr8ofny40t'
        b'+dIMWA7DfHEGDajkUsmNj7ALWORHkFlCrighG5vcuXkF21zikm4PqS+ry9CYwqegPMRZD18nWVUGF1/C/9WOfHbNTRjx8ZU7k1KvbA/DJq7BC1BFVN0DDUsqM4iw0S2S'
        b'u+wAiz2wltUIPf90XYZDprQJrIHjeEvie4k2cWlphlNYbsLf2NANizDsqzhazDKI4aFeNg6d477fIsISXy1se6oEwDmsc+GSf07jPRhaavKLIgzJ4B/ENr6CwcgWeBhs'
        b'Dv322BtESFksFe7dhPxFLfAI8uEu9NoGkwVUGXqM3RloL4S2NencMusTYXXQ1GoClQQiLUE8PMJFnMRcaw2uqgLkYgk2puukZeKYFo7pEuPPZAjjMgSG8eKjCdjIVZfZ'
        b'tNFO8QTM7eQeSsfJTOa36BVj60ko5+ohhF5bn04N1i5p7XJGqnqato6KwEqshDex7jJ/ucRIznqcyMTJ9FStVCjXTcsUR2CPwNBMvDsDq7mrptld9gfSUzM1uGZ0cUqd'
        b'5MtkpjVWszfk/R84r6IMpZkci5lftlc8L/teR1lgKBW7r5JwVKtiAoOKJ+QDw+50wXoYVtoqhGK+zkQN1ocvaSgjDSfFOIGdAsMjYlctb/7mFHx4gp4JuiprjOStikBP'
        b'RYTDZ2ktOJJqhjZvTZzOoKGw+yLVtQmha18XAbsTK4/bOUdctMZWuEUbd+wY2zdlnBUSnc4FcS0cM04PhrK1/lgVjOVYFwzlrFhpkxCnyaQb5aZ8KdRI1gWNumtJH/tw'
        b'jOMUdWw7n47TumnK9gYCEfYKbdSgMJN5Q7CIqIvWmOSf7zZ/v8BQpi6CZCa0HZOEZXrYfNQPS1gx45uh6rSgUMI1qoeL0OqL5eKNcE8gdBUQ69RocUO23mCEE94kGXxT'
        b'cNqeGClAiQiwRQz1OAsdnFwecFgj2CEQqJmvunZtjYvsDo1/nbEVhNCHB09d2aRiKBHw14MI/nFA9ovVQWsljr/Tj2IDjbsM8+mPq4KrWI9FPOPPR5LBOUjcT2oiS5CF'
        b'I8iX6YWOLH1bKArjL9IgcdvJ6Q7TzdiFpWtwkH6PE8SRwVrGFdJo1eK1T26gxM80+jhfXaNng+zeiNQoLbWgzfyHHx7gPxQcy0nYfPUY/6HWYf7ahdHN1+z+EGQpiKt5'
        b'5W9K6azi1DmVxsSgvUlrt+utSzv5xvWevwaOJ7xV/9k/d3n6GLsc+pVSkfih2R6Bshq8XS5MitwkOPfj7wnPKrkcLjGPefV4ULdPo9cfBnzHJv78rptOoXNkdsm3DG3r'
        b'cj+0+u2+tbWbjSYS681+8tpgze9zPYw/qtGfEZ2/8tc1Y/Veyt/f4rAtIUJz80O3jo9FZ7+Rbvqw7/99+O+Ltz/sN/LyvN4Y2n10Srtf5/GrxywSOpW/4fGb4e5z498T'
        b'pTrlho7Vez78cf/expT4Wynnv9X4rUnHzldmN7rvOnnuH24eDp/k3f3ZG6athu8FvKZ++YBvw78cJhoT3/p20VFHY6nx6r9f+1riV7MHHMc1KgeP+bo6ikpOHlu166Kr'
        b'3oA0ZP2hM7l7v99x+pWLJ7S/87UP3Go+fFsQ9sOQDVqdU9JfWWxYd8X20bm/X3r/w4KZ5p9VPPrpr975htqn6//R791nMWngo956y+eHa85f9Rs80ToW/6OY428ln3+Q'
        b'89PHtTmimiyzzh+tOz/40Q/X7Tep/vUv17UZ7HjDdpNVyr2Kf/T9cvN+lQuLQx/+645Ll2ZfhENMcpPGj9wMTcf6zFp+tf+9fVf8Bkzcat4Rj3TZ/u++WwN/nI382cGk'
        b'QxcM1x78U91PZ5MfhfXsUvl/0sipyPcdpv/011P3PZoy9D7Nny1LOPtdadYvkg7fi9z9zmf9V38//IrR3hNS1/Ts9z+bb+j7pftXAt9se/1K8+U9uyV14o8ia77xjw1/'
        b'vHLw0WvZj278HH5o8btj77XofDotXDdb/vHPUt1KVdy+Z//eP8uzfrdr4HdZnzX+IWL+5uC93ToHLr+a+OFfrLp/b1wTtb72gJJ6fIDDmz9P/u1m/3dmX/v3G1LxvYWu'
        b'f3z/gP8bf/qa5c+sHTgfixahiQp5OHVOTR6XNjgqJvHTA9WcBwdv2mxWII692L4Nx27wce1OEg3Fvvxb2mZQEcg9pY+FYig7jo2cDynBcA3nIcJ566ccRHdv8Mlx5UbY'
        b'vd57ScUhEd43xjt8BOf+HtJbfM4eAcKpQJkXik/aw1Ec5s/Q5GOxJ5dVqIldvJtJDeo4F1A4lK62VYfHDkuzCiv1uUuJ7V1dmIcJqgOeZBUqUgo7bbjhHTupS6KkWZMr'
        b'XCcvWoczYu7LMCiDFtsAfyxXicZegdIOIfQTcr3L+6Z6vLHEFluwatuSNEmshgHef19CMKRckaWZvI93XeEIDHFz0jHDft9EnOPL6/K1dQMlvFtrVj/OF+dzbGGYRkya'
        b'/KpoS4rMI2aABRuerjSME3uvKx3gS/b2YzPm8jE6rEjl3X0wlMi16w3345bkha4SaatDx1V1vlzNNC1PPStkv02VzIxOISm7glAPaOAG6w9FMMkFKa4Gyg4xDWIPTyXF'
        b'V6EbS+0IPdLbRdhFq+FvR1htmxjrzuBdfjFuaWyH5mjfJ/nVfCBvDvt5InlAcrtFAdnoj9ntUA1l/JyKoMNEBprDTskgsx5U8TeJ9GApjMpwMU6TguaQMX3OTSvClha8'
        b'JvhpaByVzk+6H6b2yLDxZpjisTG0wByfuTmwA8pt7WHyaXTMvJPc63OkAzuW4GOcO0r4uFnKFebHkVRceAKQT2U+DZDF9vzajECnny3Ue1M7fCCTusFccXJOOBd1PYOP'
        b'T2DpWT0ChYGspON1kU2AJ1fQhfqfC16CoLA2SzcVp7RxVOgEN4V22KmsDhPx3DplYh3UEeHIdkcNm0TQvANKNjhwmS5BWAK3ZaUdoXjbUXZJOAGMWsFaTyVoTccK3mFc'
        b'AqPQwdWP3ElMJFBlVc2GNqkRD9/OYHo2ZS/OEDs12cv0b99R/pr2OpjFPlntmWoiM8aOtJqGm8VY4azCPaOGs7RD3CMO/lhCuF941kWwFu8qQQve0uIPc9/CQqyhh7Da'
        b'n0SaHYEL2huRwHin0oFNGzmJkrNnm7yCaThx6JKawVwFUwk85Mt9N0DFYRNWzYyGUsJviiaUiwgl92jwm1tO9htL+S/YbsfkB618gMgMa7L5k8c92EGYuhTq4D6fSP0k'
        b'ifr0RX5f2685J2IfTuhekslFdewXwYN9WMsXA6qFaXbqwN7ailFPjAgL1sM4jl+31v3Pj5A9cRH/H94YvjRsLomKWhY2/x1DbF/Oa75Li7uzW4W7GUVeAptPNGaFrk2E'
        b'BiIdRSqymkjElbkWyVKQ6benbnTRECsJl/7oiNW4llgvGkLe0a3GlctW4vzzGlzVHlZMW48bg45QR2TAnYKU3+6yhqvho8OlQetwJbb1uCD/CkHTJcsh8+2r8w56hec8'
        b'bR1z2it85mnrl/v7/7OC5qqyNGtFw1yPXGc2ir65WMEm+q1EU1aS8kvFCnIF/3B4UXx2yRJYi99Wk4dHnxzAjFTicb1ARcB7yziPGbvumQsB8CECdVmIQMgFCViIQFSo'
        b'X2hQKC40jDaUBQiUilTyBTnKWSoscBssuKbMBQiUrisvCRAEi1YIEISmyFKtl8cHOE+5RObpVcR1n+91lz+x/DxWhsxpvaQJO5nvOlKStKJDM4LFJsy5C42Y8/H5kYiX'
        b'cdKzsMeKvdrIh2djzp254vyp8nHw3nF+SCzUQUNP4j3SKzvIzT2So6TOLuYRkjTOo8tPOE2akiZNl3Jtf7l4NbeAsnjG08WXVgpEUPMrJyPL3NxyJz/zq3+eH/jLeH3Z'
        b'DUW6gqe9vhsCMncLuDDmHejzfXJt+3F50Dpwm/ezIesKa3UcOQbTnI/X+FTkUi+rN/M6YlFgMO9ulblacSwjC++rQ7meE2cIn3GHfBboFh7HLhbpJqu9kbOx38vQEHxw'
        b'wZbM9/CEes8L/CUzH8NHwdopOTH8NTMC7WouzVj/5DVb6GO4uQjvBDPXqL8fp0xPPpOyK3MVHMX5g7yrQByqjb1wP5MzvqXrCBRNsMxRf6glKDm7j68ZcOnwvwR6h3qE'
        b'AsdwqUkYXuTN/B83Hgzhvi7PPiP4ycFukSA8N/5KnFTIf+3Zyd8Wui7jovBs6JCywDx8rzTHQsDfnV5o4eRMi+8EhZAncDp2NNODfdocE7HU341F9j7+WMM8vAQKj8rc'
        b'59yVTb7HvX3sfODuIR7t4Qze0fbBeS/O8bsX82OeTTtYmnIA85pLsg6gLcVayHu6mnT8fAPtNQkvyC4MUFwWgA3WnIduu/aZJX7Qq5tZaQKC/7OZOwXcnfCL3s91OnOU'
        b'8JDMJ+5dyIPH6jkawDvXSwNFgqjt3Hk/LT+LvTKfysF4fhGTXU4KJsNDhIKDuVmnNFKOKy5k5Tzo1sr8opZqHQfmIbmKt3cJrq6L410tnQTkOmCQAb1UT4J6C9DAXXoO'
        b'tcGB3MHGXZaCK1hmyTla1lgSECqlX+IwFxsEcTuxknN+pYRiK7vNg6inBJuwVEWgtEsII6FYx1dMXUwS8QVT4SEML/GYEkFNcV4ob/0QDvtvhWFCcBz0z3GKszf3Uk5v'
        b'IIq7pdfrVjmfFrJdq8Dif9/7Vfrf3v3ON6XqO0PjtypbrF537GBVxxvdf3y9e09zUNKvPM8oTbf/4uoVtfW3XT+WvJW6+fefbfm0+i/6m0peeziftaP7e8pR1w6pz++O'
        b'6PzOqK7uxTiLV12b/3Qi2sDpD1g71vRP841zh35741czSf/ubf32mz2GXj6fmhg4frUkQyf0TM0fNfWu3Qr842oT3YfZtg//9c9TwW6hkoSSrqgff7W+KfI3H/mNf/N4'
        b's830by6nZr6+Ie7Hx7/xtzUqmQ+aAuuzfrDuOyGfDc71uMx3JcX1+n1vUFzR+rc3T1/6e6+f3sj+pKjXP5l3zr4XP1w3d3zg/te++Z2Pv/r4R/Ynay5siMkSbqu7Enb4'
        b'1a07nX5a94P56q5q93//aXzn7je//8lb7+9P/Pgnb7ylkvHGtp4Cw9W/2ufxvZ/5G6+58ZqNw1fjvPLNfZMe2n8PL+dpqZv+uvr1114zynMI+sa6eeG3EoO+63Yu6aev'
        b'lB08+c43TqxeKAkyOZng0/qxW+L7P0gvd92u8jfT+7H2n3U5/zV9QZi1kBcZfcz4s84/jw+6/vneKz9fFAxZVNZ/tM/aiD8AOXMNhslWVSXrQJ6agjMGvHX9CCvclxir'
        b'+6GXHWJMwwLeEilwufZUSilX41NJbe0J3mi8A/d8WXWNAbUn1TU24UPOpFpP8H+OWAlKN8qLcphd4b7B2u3qtj7+MCOQ57McgAL+nrUC6LqwNNkUSyKWngZIwGJuUnb6'
        b'LIiwzdsCa7j7K9nllXjXlZuUzUYd2d2VzBFgL7+90gvbuTGzGNkQd/8PFuTwVwDBI7x1mvvy+BH7JXf1HIabmiKoScR7XKfaQWG2NBYui1Ad2qBnnQgqd2/hs3bb0+Ce'
        b'rX3QRitv+Y0AWpr8ycPHcAubOdudBGZpoMI65Gz383IzuA0WVzMDGvr8dprIHDS6u8RnfWEwg93+zfJ8cBRI3nOWF97xt/NhisJWRbAWmsl8hEko5k2eWVggM495WkrX'
        b'cTcJqpiJlLDqAtdR3B4t1kC56RIhyVmILjjOmYi7NzMPPDsgsNRKlNmIa4Q8YfQexwnugSXmodEhMhADd/JmeR4+uGC7V/jMNRcyCxFndPj8pbq9kPvEPGNXUMSIyD6r'
        b'hZH/EJwb/h9aZE+ZZVpLMxE4u2yASfgvZ5fdEDhocVaShuxOSzWZRWTCXTxEn4jpGxH7TY+ztOT/suuK2FVFrA6qBmdTya03Pc6G0uIuMmLnm3Rkt2MqcZcXaXA5U+y/'
        b'WWufPnGwZD4yw0qFN2k2K8wcZlsssaT0/tvra620pDMbRY+cOWXNzAwt+c0SX86cIoPKcalB9aK5yzO/NNlAtERPGVOK6zIPCbgsbWUyn/h7BkScQSVmJlW0lsJ8Unqh'
        b'+cSyX91Xyn6Vm09PLhtQJLNyObD/5dxt/h15bR7+vRXKZzqYe/CpM9xQnpMSxKV6MxuLHj0aHLhnl+N2ZtMkSjJY4kd6BjvC+dwh8EWBnqTBPF3gkP/+Sx8TUQvgYGYS'
        b'LmDbi3EmU4p457wMZ3obe/LB6TSclVWh2gWP5MFpVejkY/3jeJ8Q6gTcWR6gzoYZzOWeMIQ6xyd3EiQJFNFvGIP8uJ8k/Uk5PYce29hUYF+yndV2UProhwFFHe8Ji2IO'
        b'X7u5LxfqNm+Msmot8B37d1NpbVL0ZZMfO6/ebgceVZ3+fj//1es/0h0fP7D3Rl3q/xpZOL3b8bPxHd+R1L53u0/3klJggWuqud8Nc5/RhY6oxuCc1D+/P2zR9MGN964n'
        b'BKj89Q8OcZ+KzZU39c+8a63M6TtS6W2ygyikcKY55EB6hBfcjdexQnXf0zmtcBMrOdefHfSvWQ4doMSEC1mkYinn3PN2IDAt82hvW09K5IlSNIMmziGeciOO85VjATTx'
        b'/vLQqzi17LjJf6QklshwnUyOzZZJ8YCXkeI3BGvkR1P4m4nlkpzJ66x1T0mb5b0ul7XLRc8SWfvlaneTIOXe11wuTfnD6fTZ1ZcWpMWblgrSF0+NFa/Nikthjpb/Sq1L'
        b'eSG+/mfzUdMiY+MuyeoiyWrtLqvEtIKk9OD9FglXOUdHXGJKgpS5aqRRG58rVWWTebo6EH38ede4CFaUS0p8shkOQxMU87GnFfKeSCbFYjnD6hHGanHm2B4nsP+LOJ0d'
        b'vf25ahY73f1qxAfh8dF21VYSH+H4V02aTJtNfO82mzaZBJvcDHA03XNG0Dqm5uJVaq3EsVjqAWyw9faC0Sd561gj4MNF/aJDvG3gGCkLZUHHdqjmgw0DWLnlAs48c+JM'
        b'SY3MgbwMNhdYhEIdApOlUM3A5hiW2WPRUd43c9Q/VfYOAVxVGIU5KP3cG+D0JPzeyokqnWPTPS/Hpi6MSRUVRhX+1Kd6WH4Yx245I65QYtRO4fN1oN8aGW8dfBneyhX8'
        b'dtmh0M8bJ6tDoRwQEOIZYC0K4P+v9zk1+p4UCpGw/5hwQoL9xjLbOZc1B7Q4IcHNhl8K0/9rYP0FRXaaHg1JR1N2Sk5NU0lkbr60AJ+enpbITM9IU0NotIZJYoFwa46B'
        b'0CHJQGi+IZMLi5cGJ3AnowNhdNnhaJHAylL50nqYyfwLdWGfCbfJuqp2S8ZmRz0owBmcX717F+RG4oiKKxZBFVSrkX5sxZsbtKESb0M72Wo1hw9DpyYRfolwLVmAM/hY'
        b'GxpdcRIqYFwCU9gfos1Cs/k44rYPHsOoNzz2oqfuYMlVsrD7YcjhGnT5wfC+awRU7quS5TdAP3M7oQe6sDcm1ckCG7djLnYkQRvewn4cx+ZrblAKvcR+Y8ZeqfsCjaB0'
        b'M+Z65MQ7YzkuwEzcPiy46LVmg2SNp6uvcphTtkMgdIWZ2UMNTu2DWQIuE1CZBANYRc1Me8O0S6IN3nG6gGXa2BuFo4aEaNqhmmzDTpzH+nAPbDrmHA/lkfhAhczXaSxI'
        b'JoO7CtuC8QGMXk7EbnicA/PYEAJVpth58QzWQ/fu1TjsDfOOUEZzr4IK/cMwEgz5lr40gGls2gMjOTh4HBqF2Ev27k0yBFvo3zux0IdN0Hl5vVgTamES7znZYRdOx+7R'
        b'2IdTUBhpBrleiXAriuzMBnqnwR8eWUd6Jm/wxIo4fIzNPlgXZgIPrrjjQ4JorTjqpgJ3j1uH0txZdPG2xtYQnDDBDuykv2b8yVBvOUULUgcNdjizZ7+F25ZVhjh+gj5o'
        b'ybY8Y4uNOKBniIVYCVMh6fRplY7GJlykNwZwDEZoSKMCbHCW7sXGs9DsBI8M8J5OhD9UxGTsx9wgbFgPpRd2qeEiPDQzhIcJsLgWCmLo9aEUAkJ3t5thZ9SmE6fdtmEN'
        b'0cJD6E2XENnVY1OIlunZrKS92Thpdm4dNAVAp+kZHKE1asA+NZrMJNMf2HkQy9Sg8AjOOdJW1sOgC81yiMY3A/mnaBfu2B8gkii5AuPGa7GE1mce23Wui/ERFnttIRIe'
        b'zSwXsSSI1jXQGuROMK3ZUQse4cTqawdph+8fgdz10IJ37bV2UHd1tPM3adZt4iPQGynZbA2VsUpQan5jG/TsycyK1cU6IslO7KPVLUsJPwkLq09B00FSc2PQDfkSbLEh'
        b'FbQVH+IczIhhVB1r1+K0RDkFW2EyNOzyAWzOCU5g6SO0GAtWNBOiE3yQ5LuXmmgzg2bMO3aK2q4+BQ274S4URrCsP5ELKyk1ak/PjGMfDOScyTHUO3UjYodXDLboX92h'
        b'jw9ouqVE0PnEGzd3EnMVe23w23J1K5HPHWjEIdJ0OEgk+hCLJFidAI9oTkdwHopVsWc/VmfDvUxf9zh8YImFVmQzLF7b7XADCs6rB8NDk/WsfBze19+jlIyL4Tguwsor'
        b'RpIjeAsmNKDsujfcxTwzL6gIg1y8HaUL96AvMDjUKdJgqyn2u3tprDJwcFRe6xxKjNTqh0XBtMV3ccAEikiy5Eqwdxft5Txh7dtirA6AKhwzx5YALDmFAzChpE/kV2IM'
        b'nTQNJpxuX3BiKwtFOASTl6+YQvl66u8BUVXfFSKIwix9NWKIiWisxdlrTqughtbwFrulkoTXlFqMjg/eMyVQ0H76BA4S793GmQ3nYMHfl7T7ffUtUJ3OVYspcJHiRCIW'
        b'n4IFhzXMd3c2EGbWEtENYnkQVPv66J+9jFPUXy8RQtsZyCMWWqRp5TnhoKFl8JbVgZBHCz4Vhj0JtHR9gTBujQ+V4W7EFuhIJVH8faLIi1CLd4kk3eAOI0ka9qwtTGa6'
        b'YMtZJWq2HW8lSaA9VZMYs2HnMTvo1Qv3hf79JBSmabEeYcNaIqPHUEIzG4eRo1Bwhvj19iZc8N6/3w3v+kBXlJ4G3iZy7SGCmoFbm6HJ/BLRb4NoPzy6KtjlcBRrLmbY'
        b'0q5NQC9BoxKYI96pJi5ojjhzLomkR6cdNsfTas+zzAPmbR+ALqjH2rNHSDIu2hqfzDh3Htr9aYTdWImTVsQYVQc2OV3BslXqMLuUXIk56o+Z0jimLmO+vfoNmEzihGat'
        b'zlVoJGnZ6+63K2tjJIwGZF8zEp/3glJjyIumiS1SA70kmfJ37SfivauaCOVw/wLUaNMO95trQ80ebPSG9gx6JA/ZTO5hG6ml+5CrK8J8N5IhPatVYWYPzplsJVoYhzkn'
        b'fLzqMnYlrb6qFJuAZIISsxZgrS4tVDdNrxcfwcQx2sxOfSwJWxdLpJaPYwehm5b80VlLUk7DYVfMiHQ7Et2wMpylhltD/2XihjIH2opOdycScsVcxbz2szsu7sQqq3js'
        b'yzmkk0UDzIdcIuROmNhubhUlgQmSNTNaq7AG5zBfC4s8oc0phOgBOq7SAIrxjhVMQQcMwp0s7FRdu4UWeR67PcO2wWNs0fC0oQmTMUmkUgTNh2HCKyaINnICbqaH0XY2'
        b'kka8B/NZWHoJ7p5TlWK9W7SXA6fT7/hmkMIpyCSBUEnP1O/zMj6FDdB8EUpEl0yghYibVpCIG9pOx9MoF8mkt0j28cTiJG2skp5UXXdeeg0frIEGRlvbiJ07PfUdSIb8'
        b'UMRdCTzEavgFuSdxGOMRjtjitPDI+nBoV8XGIA0hjLF84QpimrtQmQHjApK1W1Zj7nZa4rtYAffMsnFYldrolnpZQZMHDBqSSmgypVcqdLBFNdEsnkinSZcY8q6TNT4O'
        b'dfCG5uPZWGsGZT7rd5M2mNGgFXqMparHoD+ccYxEmHKWQaLWJBzB+XMnSWQwCTxEsoCASPIuaDY8aBtkgCNhUBV+GG4egTk9bPe6cYaWp313tiGUBfuFQb8FTt5Y5xFO'
        b'smOAdmUwkdZmEJrPXBVivaczzIY4Zut4YB40w939kaScb9JWd5ro05oXYLcYFvWxOtRYbw1pv5JVUHnOTxJC7LvgfNw1gRi55hTUOEC+36ptq7AvAYYOEgMWxUPtVrzp'
        b'IcRc5WMwF3UI6jzjYGJ/AMxD0SEXjyPX12AjcQBJxh7qr1CQSDqgE8dUoJ1YodiIWGacluoOtjjBApSZEqe2WMB8Dk6n7ifKvUuargLr96VipztJldyo41egwCuZuKA9'
        b'B+pzVhNtTUVdxf4YE9qXYuxgSf97sfyk/i4koq/Ebi/CR0TWPea7aQyt9FvXwd1XvPRIKx5eAxPBRIszMHl1B/H9Ag54YBkt223Sefd2r2e4LA3Kos0tGT1i1aoDnDzo'
        b'pGHmQlsc1EfoZ13yxxbqZZJ4qwGq42g0/YQK8kVQkUkLX2aaTdNrJgU6SHoz/RR0OGAbdpsEageTqrgfb4QdUqw7Svvbi/NnoTWchji8H4aJk4tc4BYyVl/A+lBqovB8'
        b'7CWmhDAv0RQnUkjEjOPtLZ6nNXB07XbP4+ugeWNmlYjV9sT2y0TZNAUFjLDFh8JErCAY4bbHFmYcYfSSpqWLahrh2LueJ7D6EE0F2t1pgxeo54k0qEmjdZpmkujUJihw'
        b'xvztEmil3ktgNCXbTWu9LyzgSATeo2eGSYg03NgAubYnaMMfKu0hcVgPsza7DuDgOcIqdTgrJaBZQZpsgJT0FJJwy79hj7UGRLZFh85Buw/WBx0k7VopPQiNoTYEO7ph'
        b'3pV6qyBA0g6PdInHW6FDD/u9oWL7FazW8d8Qk8iuzFQlBmnL1rgAoxauh/1M3LSJxoagTsd+nRItW6uGgQtObtiqJvbEmxtpJXMtiO579NeSkq+gNh+cxfxzUOsOJJ/2'
        b'kyokEUUgAecuYAu27U0lsVUH90mhdBPgH6WNEh6zPwGlFkmkqpthKBDzT2PnWVco8bPzp5XLh2KP+LWBXscZjCk5dx16I6zxZiTkGmabE0SuxqozOJ1GxFN/HAfDscje'
        b'ERpERGn3/LDQnehrkWT7g5hzZJpUsuqlpia0xJPhWLMXC+Fe8h5a+j4nKNhPZNONVdvDVkXvcgmMgO5wfJh8loRz+15dDQvn3atMna1Jsk9qYbHh4QBLUoiLFtASSq1W'
        b'axNtPU6EkqATxCRzZ6F9K/SuisKxJHYnKE2z9TyxQs8Z6WqSPtXwwAFGNGkxS7AhBoo3wPi5lPPGB2AggR56AI3RJB8axfE0qtxgovhJZ7jjBguWpHJn8daNVfhYkIDN'
        b'tgSgC/Uzf8wBiU6aI1FlXhJHlAtElFdwUIp9V9UI+OQbZtMC5m1dRyh30szRAGv0CEqeDMryhsobGyyyM6FAYnLsglYQKfEu9gP5O0n+11Or9JobA07X9LRh6Apt7Bze'
        b'O3FAkxTmNCzqhmMPNsaTwr2vjLmZWBcihYXsJPqqOeIcoZlhDkAAAYh5WIgj6p+IMMHbaRuwx4qoopN4ZzAkCauumZN0aGFwN5YGUHTeNdFEk96oIslRT6tR6h9G6mQg'
        b'JzjnZOyVTVoBSIi1C3s2keC+f3b/FR2WAgCMdSvhYVLKfgOY1s0gHslLI1BReSrAWX0LjkYE4E2oD6ZHpuGWKg5oS7HoOLsQlj4uTIEmXbJVbkHbFRy/QIQ6uk3L1ofE'
        b'U2Ocnmf81f1kPXWuIwYdIWFTutZKidayzpHwZqXxKqhNMt9whDh1aB3OepHcKicDZZKU8lwS8Vc1i2FidaoF9m4mM3cAb+VAk5U9icCHqtRhPvY6e0mdr2w8G018nkf8'
        b'kJ9JrNCkAdXbseKiMzb7WRA3TBjqp0eQCHyEA6dx4BwxTvdGIsKW3YRcZpyhEB+mJEFXBtniRWQzGzuuIpHZcICVfN67mYZeGQvlBB2UsS+UtGUR0WrN/os4FWqKt5UI'
        b'f45Iqd9WorcmwebLbimn042O0R6PbbIhhmmFqqgMaNl/BUo2Y7HyWSyNh8Z99Ow4TWyQ2K74BCmKUsInLav8dOCez9YbgUSjQzicFZbAzNbg/Ud2MwNt0AV63NNszsIM'
        b'kdUdfxjLjlsVTSKoUZdIfNIeu45f88IaTxuiimHjTZi3zS8+FCtyrKxV+LSRFpxw9T2qLBBuE5wj9FmC5UZchsgJew12mIg7SdR6Fmud8Q6XPJSeDcW+tiKB8KDghhaB'
        b'jD5X7vHUrK0slV94QIDj9vTxPHRzZ+Q2XmLViLFUKBD6CEiIkU4h2h3lzyFOZxCSKrWj77wFhLrnkImrvMyjYvqulQi0g5apBsuJNZoOatGqj1zX2HBGHer3BulKDEk1'
        b'VTkQQXTSOtUx1L4Vbx319IeC+P1G1iRsZrDHNIv0Uwe0HdVzP0PyuxJaIvAOARbiYby3i7leyACvuuKQ6QEDRgzs5UCPVIKFmtCRJiHGqYHF/ZB78jjWBdBO0vfEjreP'
        b'ALuR9L6AJGxhqAEhueZttGGtTqe3EN3lrSObYMwmjNq9IwikPm9LSaiOkA6uoZ0mMyfuGhQ4kH6tCoHKrWQujBM9nCYAU7WVhNwDqHYhW+l2xgV/eOxLBN9NaqKUyGrc'
        b'jOymfLLNilysr0GhM6G3OZITo6QP2mF0I2HiPmjcI91zSYx3VKW6eNf7IvTvwoeiE2m2G3D2PA6eProa+lWvZUr90y6QFK2CbnXmPoC7ZqaYR0s7SAIpjyRk79nT1FoZ'
        b'rWh92Kp4YtxZGkTlTppsr9sajZNa2BYZzplfTWLMdyJrJpfW5QGSLF10gjIxjobZBDrh7VMk2Dr24uhWYpz7zrbATl30Q+VegkR3aEa5acaZSqScKtNpFt2wcPgM4cka'
        b'KLGBNlUcisNKb6g7gO2hZFiVkQWzoLoaS8M3Rlp7rMUhNagLh7o0YpQFa51M7I9MS8Ne+qnO0abhFu86cYoMyQdE11XOOO7hdU0/OgqmrLRhWgfveRNj3dyND7YdJd7u'
        b'hwJkDp5iXUIek5C3BloukByA+gPepwPOpJ08bUyYqIgIcdZ4D9ambXMmQTF+SUzyoQeG7I1gMTMWB3eTTVBpY4hNxkyUk8YrdLxBXDq1kwBjMXNLWQdEk0aFmW3QnEEk'
        b'VQgzZ6AwiZR4NwwcJv594HsDHlwgzmujTX3g48p5YR6JSc/cOxNDNlUP3NltvPa6LUHPyQBmTmBVNMxjpyP9ZxEXzI2gXppul2FCmGtwPz48r4152vhICG3nb5yhRZ/J'
        b'7GNWQyEjq6c9NCRLh/ebH9S9hENGKmsuY0cUcUdeBEnnsWP0rs8qI3eyYBahIY1Ws0BzlfLpC35BJHsqndcQ5dTDiCn2bjfx3bgPJrLJIig8ZRJoH+muSort4fETnJtm'
        b'PHADddIENbtoTR5p0BzGk0gsdZJeWYjF6UyYtoYRKN1nS7zRiy1J9MedSzugiRQb4a5KRqldMGYDw47JBPfbXHE86gytc4H/CWOGN5EEdc9JISG+R8TVeWbEQGNepOfa'
        b'lMzwvi2J3gnsMjwBfZtIrlZA88E0P0LabTGEP/MPMvE6Bnk5CQTx1x4ktNBlqsscXH54P8vAQwMGEs+RJC7DqmDeH5AeSTxQedGCRkZ6DTuukzSYNSNWaCVzF+77nxfE'
        b'Y+GhBBI7LecPxZBymMAWKQ2yOoO0cT69QdAcWyOjYCTh2G6cNNaDx5tP077cXYU97g5sUWyw31iKs3FEOQzsD5AB8SgNF84r79PDxrXbsTowhcRamSF2GpARVpNNcCoX'
        b'FlOZKjwA/fqBVgect5AObse6MDXs8EqmdW+2ssxcbx1ndMzLQB/bDW9kumpDwSFRAFH9AJFgMfReZyewM094Q+kZErU3beHhKikx5iPijOmck4mkLpOgQoxj9PcQ4aBZ'
        b'ySUSuC1u105hT5g9SaYmHLSG+UPn4cEGi6MkFmrYHtM+PCbZ1kji4YE+TWMBF68f86NGu3dCdeJqr0Dqe24trce8Bzx0JylceEF504GMDSGcibuLhPoItAZjqcLEPUmd'
        b'l0PDjg3Myg0L0hTClAEWBcCIij08OKNiBP1IUnByJ9HBiMsJXIAShzgXdgMa5zoZ2GRPYox56hr17eA2STUi0QIYJesAH18OtLem3RrER/vdod8MGnXN1tDal8FkFLFr'
        b'14F9Aug3JcEyYAGNLpi7kYTdOAydwnuh0OwURnKn8Ci0RIWRUhg5wVBKJ3aEpVkqi2P3Yf027LmCxQ4wvjkE85McoTv+ECmGbprwfYKuLZ4kcWDWD0vswkh1NNsQP9+y'
        b'33gyFnt2rz6dho8DiNbqaSlu71ilBvfik2CUxFcb9TAaoEpcsJgSSIZ7FZFLGXSzfE9SV2uwdxvUZZJCaQiIJ2Iiy6XBTjsJbmuYu+IDlzi862OUCI+gPxObXWDOPQ0b'
        b'aO3u4OiJ9bAYItiDt7TVcFFMoyzwXw2zysxF0uUCvTFG3lB/ZO0aFzK8SmhK+GAvifFHRBEjxAIzRAYLqWSADhnSojdGRDLOiY61IqlaLjrrHpOqBVNnsDc+MCAu+jxh'
        b'1XEdGkITKdxBDRz3hdJIaDhhawxkZNzE8ngtCQ6FwB3Dg+HnsrHNx3/ddqxyxLF1sWexwlnEsCvJoNtkSN/DR35XrtHsSyP0SHV14OP1ShZQbxiEBZGnvM4f8vckDi9z'
        b'w7r0PVE4u4nk0TA7dB9Gkn/ulMoFkg9DmmFmnIxhkruW1vJu5A4Yw6lN1sS5d7HrKjFcBYxakRFUqq9KCnIg5dRq6rc0CheOpdL2lCMhhEp1mDbY60BCre2q4Q1dS+Ku'
        b'RpI4j+2w6AK07U6E6WiYyTwsZqWzF2lBl5I2WbjTYpEx9mHVQd006F6lEm9JQreV5jNGIrF+u9An5CgzoSLxYSROaBNjTdH0O+z26mCl2el1SkTjTaS/ywjHD2XRgtft'
        b'CFEPheFd2HSKyLuJJPecJjPLYdAslFacbGuoMMLbwZ4M/BhSYw8ubIAeJ3xwxAYJ0fiso0Uq3QT3HDYQf9btg+bVtDTN6aR37kth7JQZEXqTKGjHWugydYHcCCjeRvDX'
        b'jaThhlDrtSQnqmMxXx3GpGk3SHXlw2TYLlIqE1ImxUtVM445Q7/WblriO9hocoEWadYAO2NW47CaVZb7vlRjaN0NI37XiK56SPd1Y6MpgUQf7DcgrHOH1Oh8LCmDLA2P'
        b'NKK+NmqketOeDOjeq7QdHxzYAn37NbAlA4f0os+ZQK++XirUrMYy3xhqKA9q7VSd2LFJAhq0LA+VzP1TDu4OisfhTSQa+omLWsI34aInya4GaD3q7iYg1ighviQETpKr'
        b'GqY1o7FwJ+lnItJSDxhdoy4kWTBz4SxJvR7akofU6m391SdJjZdDlxrcioUCF+y3J/FfdP0SVO85i8xX3imAifN715JEmYOCOEvitPsm0GFPbN5ITDFKdnVLuLrpTpw3'
        b'hoaQPb6uMJbiRTq0D/rwgRK9dRMmzFe5kN3RBb3uMKBsRvzUAosWq00Jz5bbYOU1rGSrU3wZxsUpW/fSp1X7oNPyJM6SssR6/S37tmDbHrgrPUWkU4T1aaSZFq6cwZEd'
        b'+0IhPyGDZGOtAwnhXsmVVRERtPAJsYTmyyNgNJUQdBUhuHJasDFXEq23t7iQbTiLhWmuvtFuJAqKsCTbntZ3XEtIxDegxdAx7WVjVPqVHHgYSH92QZMfmen3YCTFG4dP'
        b'cnpxEuf3ndkPDVakM8kG9nLDSR9CcCOaUdsJyt0NI+ZYVI0grs3dBHPbM1lGhDd07Gd8lEfkzBhpAedtSRbfZSEmF5w0Iax7Cms04jxgcAs2e2yDKjGpt3Zt9oSbXhxZ'
        b'jI+yY7y9CQ7k+4S6mGNBVjIh7AW87077Pw731PHRLtUE0jqDQuwIxjmLHMgl269uq6euZjDWR3EhtgfM3X8jG2phjnm1umA2iGZIbNLL3EUEdHug19sIG68GWZ7eRnOr'
        b'w4F9mHeDrNcpM1KNRWfhXiiBrSl7ldhkJxMY9dYgvh+iB8udaFkLEogHFnSx/RwhtzwcJd1SsR0r16rSHHvU7XH4WixBwIKIK3DLjXRyBbSLcdxEHZtPmHiaELUMWSnr'
        b'rcOHB0KhUuegGitggblehGUGmUTbicPsstY6vOOoIz0Gt8/4Wu3JiNfABb2TWZYk4QmV7088BndSsMYpmIxqhkMnXGKvEXEUW8KovitLmO4whjkNmD51NcEG+yxIas1g'
        b'M9w+j3NXNLDgSDDxxW2yS/pI5lSRzbKRFrthPbZqaYijjbH0dHzcuQvO2OSrIzxiRO89gCoVqNY3Jn6rgZl4raO223B6PXN/kt7OhUdrYIYF8O6bWSqtI4BQFnHAjfB7'
        b'2w5ajQ4YXmefBFV+m4kpKsj4Sc+Exh20CwVHcWqfJiH4eQIGLUeyjLFT67oyzaHaE5oM1a8Ry1XTX1WwaJsUfhXaNpJNmW+wJxCmTKBFb7eb1mW86YO3zS6o4v0QqI6F'
        b'NhgkMqoICmNOU7yfyXxetPPzJHxHSUfkY7cDFl2/sJH0NEGgE/RsawBN5+ZJnM5yIFwGPcQtNaSqizTDIjJPEz/eA6ZLCJF276LZLeZA7XqslhLonkolenlw2YTIajAH'
        b'C29AMQlygh43T5HtvzrzFwzVzzKVpmCDg8w5deckqWESYfEHzIN0t2AlscDJLdn0dYtpTKS6CXab7tlC+7uIwzEwpOodTp1ME0TqEe3C6bVkqt/fHa9JM7qN7RnAAsF5'
        b'p/dBtRLUm5Asf3QZG32hU0y/9sKclJRN33USjXeIm2ppL6o01mOXD4nSQVr6Mqy+Rspuft8qLN4F8/bYucUfSxNYuOso81ZFHaPFub2VJEqxlhIOSNcQ4U9eNScmn90e'
        b'mEwU123oRGOrdjTC+s0brLF56xFCDMQcHkQOC6ticUoLm/ZuxB5tshtvn4V8D5w9CIPqV0i41BD8qSPZ3MUdyFaBVjNvaNAkLN/jqAsd7tuh0ZnAwm2TkNXYt3mHigoW'
        b'HffAYk286XGMbOJ5B0JYhS44ppuCU9u0fJ2g0xlr3F0P0qJMQJMSsX03CfuCrHBzPXYcaxZZGZU8cyL2B0LCZTcubSdqqwmC25ocUcxeIOG9eHEryYMWLEymVetlcmDK'
        b'kYBHTXQsdO0hcmZe+BosMcaJXWTWVMVAkQp0xppDnxKM7HfFaWadY+5xEl+TfpdJnT92ViFU3QVlVphvRwszYgSdOdCgT1RZtInFk5WvqeyKCaGWa/fpYD0hB5XLDALl'
        b'G+5MImuP0PxNEhFV0GuIjYeNr7AEi2BauSaYO3/JAgbs4ZEndFkrQ+NGglfNp6D/Ipk7D6DLnhTaBQJApLh3uSbvgDkfy1TstIC7PtBr63gEJ5RJpTQc3UiGbSuObycd'
        b'18+YpDHY4LAzYexBB1wM3ULCrSEoXOdCTsiaMKKdIszd6Ufd3N3stuFgDjtTXnSR6KCX3SXAnRwZc4ImVi4HJ2+kKfP1cggOPOL8TtmpYXz1NpjFnmQBzJinc36tqzEX'
        b'2SsecYo37l/m/FcqWy35F5RWscdFUM/7wap1sc2XuaL2CIhju7BeLZOvUVvpxd1DKxAIHQUnDmPZTjOuihfO+hCZlWKxkkDoIcD+MJryzDbuDJSQeLVK5lNzJR4voT2f'
        b'5RoLgR4d30Dq3EkAt3fTFy0b+NJZC2tZ9Qg/esVFoEbS4A4MCfhiYSVpOKpwxA2EIqFUGOWGrIaVW7HUmt4JFOCiNnZaQS7XmsdB0s2l/pw3Tkx6qwq7sI37JgeKjWXO'
        b'O9JUPVxoq5if5qJkva8PtWUrwGaitSIrR74K3k24dUThwIulb5q1E62FntxlRtyZtbZ0kUDp2DqhQBCeoJ5+TWAt5qvIicUCpcMfCNjFdlO6qnxFoSBd+vDsX9mzWqFH'
        b'1AQs+8yTa40/4Cbi+5w6spFtngpOyHfPWIX7JoQYYJbfvkRntn0MuFuLuRnoC+Nk+8fczMSUNTH82vZD0xX5Bq4naVcWiKM8YY3SIrQr9vA6SZZ6EqVtNAzWIJQLs2Wb'
        b'JSaeLcEm/qQdsWyofK+g2xTvrIdu+SvD+1XkWwKVZCor+XKfn1lvKd8Qt1jajwpsshbyPtABIpYC+crXksRgnsvhuDvaJ4Tpi7Qof7s8mFPzVqDhcZOvffTtDNVbh3xr'
        b'IO6t1x5/9K/HIx+3bz+i3JNl1rlli43u3YMRdt/c/euawP36n5347k8CSt55Zcds40fX3rv80azvjUvX96b3tlbcFP4aPsn6IAf9bH9YP6xbslPU9q7Zj83cPvWpu/bK'
        b'rUNWPXrn/7rjE4ehbTEnVTYp/7qwKrhBu+Dj66//sq449pU/vtnwO6dLH3z3F5fM37Xx6tjU8xONmN/U1OmmaL3rYYb/LMr4ZlVip0HoZf0Z/ZGem98K/t9DO+P/0Jlk'
        b'H3Aq8LV9dXvi+/fpv2M99PtK8+Dg31ke/67r667D/7LeMTr8des617e6qj0LnHf8QrtuY1y70cHNTX0W+212H8k8FuQU4FYUPVk5/L/HI4I+2vzTkul5tbdbPr35TtPr'
        b'c39Qeuv39fuvbtoZVdh94utRN69GRx25FPXziq51YUFv3QxzPIthl41eDXtjy4fVf31ro+k7TUfiTxhJS38zfK5UJ6P6g794j/9wNs0252e/+FZ9yLeU0i91NA8n/Xz1'
        b'Dz7t273W8O/tDQvnFy75pfsbSHZ/vc72r2//YN9gxB+Uag50/89ve6ou17hv+MTF98YrGZuzflTw+s/tNh74LDxOtabp/Pc/qGr9ikDlqI5r1c2vKXU4uf77wNvDqFfw'
        b'TZ1/Jfz4QLKv6Nv37N/5qOGX428Ojvf/c4uno8/1kI/czB/8bN0nr2vvLdte9udL379im0ijG/Ebc/7G60pb/7l+IMVzoWRbusb3h37/abzKxG+cXp1YXylt+5PZu28F'
        b'fpLt/NlbPxh9M31B+pHdhzZ24VVXjTLb2j9KkgxPv7HW5mce1W+iv13cfnvTt961i7OTNE7YZU/8xGYofPXFU99Q2TWWuQF2XRotdfvg1wd/VPj36P1Zn6p+tOsHv/3o'
        b'zK9dS//+72/9pOnk99bmf/ZJTFzov+e2G/9g5CvvHQ74Xr7Td0u92sI+/Oexd12u/8ble+vnv/3n3/1/zV17bBTHGd/b3btbv+3DScAYcA1NfD6fDRgbYx7lYTv4zStx'
        b'KE635/Pa3nK+O9/DwQZCcBIcv7EhNTiEBFMghAIO+Jk4bjKDQkgrilRFRCsi0UgRUpM/UrVFKm1Fv2/WBjf0n1aVXK38u53bmbnZmd2d71vP7/d139l9fa5zhfEv5bm/'
        b'vc+/90VZlS/LGqrT+F6OAe+yrUi/P4/AY6SzNnsy+uFi2vzo0mBcsCUh/Y4R4+SA698E/XGTQcb0o00KkxrJgsd2V5gvIiQC7KS2KF8wHO72EbCdBC6+UZSgtM6y602p'
        b'fpDrBTr8Ql2EiZsNnsb+tQJMvsMhAYzsmRlDD/jrw+uCdCSKtJL2KCkilA5EgZ0zVm/krJEiGCPNRhahcCHYwt/LC54Yy15POqZ+oVg0kbG55DAjHqpkf0GYXmM98iHO'
        b'8LvJW2ngwZzRYyOdJs17/aRDqoNGosRbS5SU4H6kRjpkIhMN9DgTn4H5p981Xb7vX5RnumCy6jeGqDseDSqUPrOrdGccrPFs8vl/AT1evCy7PI5KWWbL1k8DcDae5w3L'
        b'DAmMpWfhJUE0SIKJh02INFoslpDo+dHmaJMlNHaWyMfmz07M3Mct4w3ZuIBdFKFswj4uJe7JHEzLmQZJX9ruXKbvla3R0+bZ2+PWRQuRgiU6dR+3KE//tpC38sm8DdBm'
        b'WsL22BZuRE5g3LQ/X9qDxd+C79d4Og+XwC+d+aGesUvMoHcGW4yOXYShHv2ROKw3vdPjcDFxgqPgd8GjCRyGLoy8RlpIl5mLnCNYPfOi7WrDUxdEfxyYUCM9Ixkd1wqE'
        b'ddEHzlXLh64V/fxaRWLi6ImKcm9DeNQf9ka3fLliY6phtfXvZ0f+tG6PtFvrzt6z74+fb2lpXbT3xkr7lc/uxcZ7vnr1+e3ZO5re1bKPxb1/a8mfs24Onrq45+4zHx0P'
        b'HVt8ubN9228uFHyh1m/tfPnF8B3HZg+PVR+pK/vd6/NeTz/bdP/FhkvnGuP7vv3m1p21NxonrgcWfLo/ebvU+PbXV058/l1G498e39Y79s6Xs+znr2q9HffVVf9YuXrO'
        b'Z91x/qrhxBWbd9z6WWrRWMT6BYJ0eGDxKx0xn3hvV7TOGf79x1cj+W8Tr8y/W/eS1Jy1vl28mvWx9frBr+Lt5bctZTULN5hvfrr5tmlkdMMTH95peKzsWtlHdz+ZOPPd'
        b'108s7ym/kfSadQEjlsWBy4f/dWkpLWWUYjMXlqmQSzx9Zzcd1FWnTi0k3YWldvoeZirNzbPzXAwdF8gJPzkW0BUPUPcVhwI1qfDVFwyFRUjJmU+GMvR4DqPklBlFYovN'
        b'nEmkE7Sbl+rn6kp+vRVG2lZOx9LA9NvK0ZPb6Ct6raPkaIqNdibZaQt4Pidou4ELSeXBkYNpT2dmn03YYtN1GMgBVFIoMZAB8MA+ZOV/St/eizwE+6Q8WSRtFcDLPIsv'
        b'G4ZYq1ahKYuM+vaGKUZ9JelkfJwfeukxfSYtzqcdGAQ3X+Qs9JAA3vJx0s2KF9HxhsKClJIMOsanGzgz7eFNnEUndJ+kb5DxwqXpUBiVx1wq0s9/IKwMQuOQ72etpD14'
        b'OL8YjpK+2Hxs3wVhSQYd1hXiJuhLMGm3JdPOdKisC1yCzQbyATllYGeOL+XQKO8oziHjKRwnLjHA/fA+HdBVwFrpefKuzU47yDjtQk2AWgMZ3Upf1aMWt9GxOhtzpVAw'
        b'pBi6SOTm7gVjYlwkTcvJBb1vj+QuKsTWQRdgz4clLLfy9ODadNa8xtVl/mkHQ+kE6cnnycCiJJ1cfwTc73Nh9JKXTkTRIT+Y7yNeOlgHBkcEx8UvFM0xMARskC/Si3ZG'
        b'z7JhfRwXJpKDpI+n/R7ar5/MOL08jwnpDZHmqWDF5I01SWxCX2mYXUjOJ8Egox4aC8BXmk860krs5DI9ajVxT+ea9zRuYePlXNYQBk7PoAG8lnoD7cZIHIef17u7n57e'
        b'hYvMGb/fuIe8GWYA/7CJvsbsr+T50MLLjG+VljxFtIoLhqINdkCFTFiHj4yugz5vRc3GglVFPBfyJA93xWU4D/YTv6whH9gK7CnF9lQDF0576a8eE0LBufoFo282onBd'
        b'IQxLYSpUALdS2Xxo/ax0gR6PIn2sBvtPkm0bU5KR6IoDQt900oNIeulK0yUTztGTiTbw1Q6ho1SIFmTfs1MBjpJm/vn+P5olHp8BU+NhMGovTkeRElMCkNgWy3TepElG'
        b'KpLgUN8NNdYsk6prkFNw/+eEuqltsc4xY/ZCsia4FLdvE8xsmjEQ9LoUTXSp/oAmVqpOQI9XcWuCP+DTjBUNAcWviRUej0sTVHdAM1aBtQQfPoe7WtGMqtsbDGiCs8an'
        b'CR5fpWaqUl0BBRK1Dq8mNKpezejwO1VVE2qUXZAFqg9V/RhL2OF2KprJG6xwqU4tPFfndhY7dkLhcK9PCQTUqgZ5V61Lk4o8zp15KjQypCI9U3GjtpYWofo9ckCtVaCi'
        b'Wq8m5m3KydMivA6fX5HhEJLatZhaT+WK5XqwErlSrVYDmtnhdCregF+LYCcmBzxg/LmrNeG54iItzF+jVgVkxefz+LSIoNtZ41DdSqWs7HJqIbLsV6CrZFmLdHtkT0VV'
        b'0O9kkaK0kKkEnE7QjeJaDy0xvb+TfHloqxUibETYhICybL4ShHUI+QjLETIRShFWIaQjrEFYgbAeYSVCFkIOQgHCYoSlCD9CKEbYxujFCBsQliGsRihCeBohFyEbYTNC'
        b'BsIS1khkHW7BvWcR1j7gUOKFFPLAqvrrj6dZVezYPakKrhTFWZOqRcvy5P6kkX0vbjKd4HU4d6KyGnJ78ZhSWWKVGBtSM8uyw+WSZf2SZXzJb/B7kx7N1Xcdv3luyvz9'
        b'XmxvTVoF4x50KWsw5c8DEHmRl/77W+eZWCaX+E997JG/'
    ))))
