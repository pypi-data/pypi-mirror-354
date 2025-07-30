
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
        b'eJy0vQdcHMf1OD67V2lHFUL91DngjqJiNUtCEogOAqGCZd0d7AEnAYeuSEJGVgHpQAj13iXL6pLVi4tkzySxndiO7diJfU7ixE4c2/E3sRM7ieXkm/+b2b3jDhDC/v7+'
        b'8GHYmd2dN+XNa/Pm7cfI70cGf9PhzzEFEgGVoSpUxgmcwDejMt4iOyYXZMc5+whBblE0oaVKh+Ex3qIUFE3ces6isvBNHIcEZQkKqtap7i8JLskoStfW2gRXjUVrq9Q6'
        b'qy3aogZnta1Om2mtc1oqqrX15oql5iqLITh4brXV4X1WsFRa6ywObaWrrsJptdU5tOY6QVtRY3Y4oNRp066w2ZdqV1id1VoKwhBcMVpqfwL8xcNfCO3DKkjcyM25ebfM'
        b'LXcr3Eq3yq12B7mD3SHuUHeYW+MOd0e4I91R7mh3jLuPO9bd1x3n7ufu7x7gHuge5B7sHuLWuoe6h7mHu0e4R7pHuUdXxrPRUK+Ob5E3odW6VcrG+CZUghp1TYhDT8Y/'
        b'qVsA48ZGQFZQ4R1WDv7S4C+aNkvOhrYE6cILatRwrR0qQ3J0OUOJTKFRw7OQawQUji0OJ22ktTBvDtlA1pEW0l6oI+3ZpUV6JRqdISf3huKNOplrADyaPGNybnYSPpaQ'
        b'rSetZHO+AmnIJlkBOYvPuPrAfdyKT0XDE9mKOj2Syzl8dBo57RoMd8ixGUmJ7J38SPxCNmnXZctRFNkpw8/OIjt0vGsQff0ZfIHsyU0bA/fxkUW5ZEthtgKFD5VNxk/n'
        b'u/rDE6uj8SZ6P5ucScgXb2vIJVmqbRVUMZBWcY8cCXNkwz0ARTZzyIbbg7N5fJmcqXCNpA3ZTprI3hByNZzccEB7t7nIrXpyfRluCw9DaOBwuWo6uabjGLSl5C65SNry'
        b'cshmGd6ONyAZucvhg3jbcHiAzr0Gnydnc/HF+Gx9Ab5NNuWSzbi1kLYLtycX6HVKNDtD1Ri5Bh6Po3OCD7nINWhYXiHZTy4qkKKRIydHyeF2LNwuWTI8MUeflK83AGqT'
        b'86F9ZMEZZJvUFt0SWWJWUgJpzaO9wnciQ8g2nlzC56dXcH4raox36rdRjAzER/R/xUh3vFvnTnAnupPcerfBnexOcae60yrHSHjKtQQBnvKApxzDU57hKfckL+FppT+e'
        b'0sYO6IKnRhFPf5mkQpeXDwGENSU9P3oQYoW2UB6lDIdJQqakPclRYuFIFIR+PXwUlJlqxgQvEQs9qXL0yvhIoC+mmtaVCnQW1QRD8c9K4uRfR6HpX0Y3cAe5Z1JfzEzm'
        b'aoLgxryCfdxlFdKm9KtraH/066hwxIrlY/4eviuci/8SrckbGbFl2SXkQa5kimS3sRswtY20Jc+Jj68mO8mm5Cw92YTPzo3PySdbkwzZ+px8DtWFBz3ajxxwzaB41xwf'
        b'5HDaly9zOcgtcplcJ1fJTXKF3CDXwtWhwZqgsBC8FbfgzWkpY9PGp47LbByDb+HLcoTvPhZELuItI1zZtJpnU+Jy83IKsvNzyVZYq5vJJkD1VtIObYlPSjDo9Imwis7g'
        b'C8Xw9lWyF9B9N9lG9kAbd1Go8xHqmxIWFRLrwxo69ir460snIsVLx2SVMmlW+RaYx9UymFWezaqMzSr/pKy7WeWkCgNnVV5gp9NtbWsdxjkmwtWEf2/KrX3OvOjFN1+6'
        b'vO3KnqGKV86ZF7x4O+KVx168vu34nuNNVs6hqggjM04lxW7LSpFVTUI5tWEDcj/UKZy0naumBMHob6iBzm+FtYnkEzl8Zb7JSREKv4Cbyc5EAwyOO5i0JnFIibfwenjw'
        b'vJOuMuJ+HO9J1MfjF/gsPQ83D/B6TaqzH331TgZpTdTDYG4jF/JSFUhZxpGLSrLBGQV3g415pC0LX0SIX83l2zKjc3Sch4/X6WR22lO/hIfkfp8plXbbKkudtlJkQAaH'
        b'pd481SNzWQV636Gk4zUzmIvi7ErvSzq5J6jOXGtxALOyeORme5XDozIa7a46o9ETYjRW1FjMda56o1HHd4CDa4r0djqJdgVNaH2zKAwNhXE3gldyPKdkKSM05CzQqav9'
        b'yM1E0p7HIR7v42bOsmdW8J1Qgs0iZSZARihSyCvlPqSQ9YgUVZ2XenAXpIguYCwjaQFZ78hTsEa142sInyZPTXJF0sfj8cFcuMPpyqth1uJzXDFQ6sKHiZtcK4RyBUd2'
        b'IHyjJIJVtBJfx1dIG72RQW4WIbIbXxjuioA74ybFhgCr4iLnhyD83CKti84mbnHOS6Slc8jTJYgcnDqCFWck4ZuJBiXiHksch8jpdLzHRZsdVkZuk51zKOqNG4DyyTPk'
        b'efY4rLzWqWQnDHgSItfLkwZbdUGsNZnkBr4+GQaUbEB4P3aTDZVkB+sAfvYRfPkJeudpZKsmT5N1+AU2K7hlEpCQ56AushcaRI6Qvan4KZGvNpMNuJ2we7cQOakktwwG'
        b'dmcZuaXDz8EIk8OInIMxPIyPDxAnuWUpeYqwWy/QCjaRF/DBGPYSudgAmefCKVtGM6rJMbKPrBVHpX3wNPIUT6WameRgCA/FdCqiUsm1EqhpNHRYN7qBnGEPRxU0kp2A'
        b'JylIhzel4LXkLgM8rcIO1GYv3ACCtoHsRkZyF/pB1+08fAq3kGsOcm05WZcCmEfOcCOGzGfUwUeQeH8aQllfFWpEj0es5hq5FhAE7fJGbju/TE4FH7ZoxJXDe3hDioer'
        b'0HEda5CthvvBU2qsDmeFrbZ+6gJaJb2jRK6p8G8F3kaezyXtuT6WnUV24Wt0VgsLyGYdvilLS8NtuXgHNDqEXED4efIsyA5B+HIebrce+fcfOMceusTeOj1yywua9UUx'
        b'TT//LEP+46MvvfTWy19y+9qDZK1vXUwdVfARRjtHHflOo9n7SJ/6pQeTa8N+/qMi9e5jFT96/VpQRcH+lD9+cfBmufrtVrfVNXDsnw6veuexyo1PLBp0P2//N7opg78r'
        b'/vzx4dzhP9jfP/TWkrZ11ddfyjqUk9p3YN/xqwwzv95+3v7jb5777/af5br/979Lhn72P6rfLdM98u4uiVgOADQ4mziLPG/QkU1J0Hd8gR8zO8NJhzaD7M0CmYO0LCZN'
        b'2XkFChSCr/DkMLmTzmhlUMk0oLNH4pNAIANpULmYH46frncCY0ZlqRrGAMkmELNIK76QsxIpUPRYGdmB1+HnGT11wIK8DE8xKs0HSXS6D362C8nUyTvT0MBJ9IRY6ips'
        b'gsVIiSgjn1SoRFlyTs6ppV85Fwy/EXwUF8GFcnGcXeNHVjmHJ7jOZnSAYF9tcdgpe7dTmtS1Jbyd0gx7uI+a0mqyfdT0TpQ/NaUjMR8fGOWHQ+RqGKCRHPUnO+QrYHR6'
        b'oKqM0QZQ1Z5ZbfPDWW2QKEBVaKIQle23BZkaXeP0olj0xmPZCMTClN/xtcFvZ/ZHmaIE9WQE0gJLro9ZkffX8hXio8cGBCMgVuoXn3CEHs6oQiKxO4oPZy6wjEkBaHgn'
        b'Kq8cY40Imy93LIR7t/8y7c+mz03VlXnm1yrj93y69vL+qws3CcX7mvpNiotNSRI+FT41JaXJrvabHNc3LfZgulC8oDiubP+IjyLSkzbGzIvIPUT5/h2lwD82voRx/OG/'
        b'6rPu7BUdL3Ft/Bw+0OACxu3j2tljGMNfibeHLEWJhuykBJ0BhC/SilCcVr4Y37VJxOCh2BVZUW2pWGqssFsEq9NmN0osmk14WRzDMQ2kgFORfjglq7AKHlWFzVXntDf0'
        b'jFJ0+OzRPpSitTzmg3A6AKWoXjmH3LUDPmXlh4H8tgVvKTSAWNkKPUvGsJaAZT+KDyrJKXx0aoDw78MuJsZxgF8dYhzHcKuXwjlt5MguuDVMxC1uSDTFrQUL1KbG1ugE'
        b'CY0cPEOjiIOrTHkDh/ZHc1npvEg5gv/1M2aaak7K7SJyFcbxFHMjzoEWumjJGrGwclkYAh2p6ESRKelv46LFwvqVfaiOPX1OgWngq2ilWGgaNQhNAISdMse0aEpFmFgY'
        b'Hq2l1gTToeWmRRMfXS29HjsCZUHhijxT+SUhTywsydehInj9+QpTeZBuilj4TmgSAuZgenOhadjCygax0L5AiUKhSS8nmJK+Gh0sFtb2YyujaGGsqebjwhKxUDt1FMpD'
        b'KH5moqk8eZ5KLFTPT0RzgUYl9TUN2waKGSv88Yg44JcoJb/KNLB/RppY+PasIARERzulxpR3bMAEsXBdigaBRhv300dNNZcWTJZeBzV8LIz98hjTolx1mVj4lGkImgK9'
        b'zXzUtKh4gvT6S6phVAZMmRBqmrHSnCEWHpH1BUEFxb2fYFr0i7zFYuEfi5LRImj8xRQT/83MR8TClx8dh6phlJpyTVFh0GJW+FxFGmACWnBXbrJ/o3eIhY9ZU5EJAK1s'
        b'MJXbFi9GuhFMzCH7dWTHGISbQEZDqSgVBJOzTJYg7aZVY+TAZK9TQ0XasrGi4HEcXxkzhg/JpyrsGHyRHBWFpQsl5OYYJTmOryLo+FhyDu9mMh0+OF4Yw5FL5SDeoXHD'
        b'MlmhHB+cOkYxAbB2PBqPNyawwkXkqn6MbDLg9iPoEfz8I6wwT/74GJWJnIIeogn4ynLWsn74SF+QQEtARJqIJi4jJ9ijdgu+jK/JFekITUKTIuWsMGN8ukM+Fh9FaAaa'
        b'gffPYIWjI8h2B78Cg0QwE80UHnFRHlI11upQClOoQD5rAt7OpMkIfJPcc3D4GWh9BvDgYyAB0gbMwdsVDgXZMBrkR5SJ24pZaQZZi7c4ZOTgeIRmo9n1ZlYKksshvNah'
        b'MowDFENZK/Xi4D7rXEOuoahoyrKyZ5MLDB7ZEoSPkmvyPmQ/QjkoB7eOYuVGoC1ryTUeHxmDUC7Kxc+VsY4YxuHz5JrSMgwGCuXJVohC4yFyj5wh1ziQhE8jlA9S8Mk0'
        b'NndjtOQOuabQ1iJUgArIJXxafOGp5cD5r8nwVnIPFj0qxGvxNrE9d3NAIL2mwuthIRahosXklFj+LIgq90LQBLIOBgPNGY+3ioynmWwcGyKfiJ9CqBgVK0CSZo9vwkfx'
        b'+RB+BIbHS1AJPq4Uy69BEw+FKBvxbgQrcC7erxJxbB05NCyEw22wrEpRKd4rjVkzvoMPhiiKYa3PQ/Ncc1npInLdGCKbTM4Ag0fzyVVRJ8HPVOIrIaoIDCOwAC3IThex'
        b'9AbeBU1pQ+FmhBaiheQg3staMhY34XbcJsdPAQ8rQ2XkbiJrSS5+FlT9Nn65hvKBx/COCTX/+u9///vHKQpKLYum5ZlC/2oYK66v9yfBkgRqsiLZlHbjsTnIuo17VeF4'
        b'C+6cqhxdu3VyHZ8a1/ynW69/l29qkg0NUx37mP/1Wj7408yxWdvfKxpxXrvj8eNZp/IPl/8zamBLSVHUU7uqz317Km51umJisOX0L8a/y6erP7dZtg99+eXmUVfz7Iea'
        b'FbELT1Tu7zNvYcXhdveFV2M/+OLyz0b/I/6LMb8fo7re+Pttw+/+b8GUBV//7cZ/Dg155z+OgdO2pr1c+ey8xQ3/E3Mw6O1rO9fmTT4c8mHUa7+z/PfjH71k/e7DPfX/'
        b'fP0gqqpxxj32736Pn3gr6q+PNjW9X/qL89pRb/c5sdDyhEy1f9LRF5aDwErNgGTtYjlpSyqgti5g53vwQQ7k0vPM2qV2MtTaF4sPJMbl+AkDNXFMLMW7yb1gkMZAs83X'
        b'4z1kb05StgJFkdsy4nbB6mAWgq14Mwa5FHjpObI5N5uq9MoJfD981OAcRmu/g++UOPDFrAI9qKCAkq0g4W6VoUiyTQa0oBWf0im6FSjk3XF/PzFDI4kZrgojFWaZjEHZ'
        b'PRJCOTkfQeUMPoajv1G8HGSB/jQviwDpI4JJIErOHuOTP2Qgf7gqehI7OHsfn8QRw5i4V+I4EmASGA4lU+NrmcAhShv5kCSkivZVHVmrwDsH4vYeRA1qZUR+ogbXo6jR'
        b'xV7dVYxViaLG2NJQFBcHfL3IVCMsipVEjfTHgAVP+ZcCRZhqLlROROIa3DIbbxjTZ4hXOMXX8QvWOckzeMdMuDv/3S//vIQ3lb14edvxnWebjjed3Z+6IfXg8axhG3Rx'
        b'r+SaC8zVlh3yK3HF+9KTlm0s26j5SX/lsUl7ao71f8OJfv512NEbpTqOaVOADPfwU4nkyjw/5GtM9kqaPcx+f3H2HU67q8LpAlHTaLdUWuyg2IiYEEqHYw3i1aC9MFkz'
        b'1m+u5Q54uOfJ7uubbPriet9krw2Y7PG0DztIEzngm+9kgy4h36DT5+Tj1uSc/Fx9DmgzBQoYwVsIb8ebgsk68ize2eP8B4qa32P+vRUGzr9SNA7pRjWGUOMA1bx3kLN4'
        b'P95PzjIccKGxYy/xb1ITb5p96gqUad173sU5HoFbE04f/7NpEZvpK03LuIrgj2f8ZNgdzSnNT9LuVv4k5lTNnmFPx3xi2qhRRkzbt26MDGm2hOg+eQwUDTqCmfjSPFHJ'
        b'CCFHxNnFL+DrImE6h3fM9yoaO5b56xpH1kgz9eD5j+ukZATOfrA4+0FqLhZm3x7nP/cVD537fr65py+20goj2NyjbwNmn6qdUWrc7LfWOzQLce7xgSo2/agBnw0iLXgj'
        b'3tujCivrZBj8nipsd3PPZjg3kcm/aP1YU+iA9BiRGaaGMw45/cV8U5I6XiPJqhPprhaqflNjSooC0c+KhTtyRwHc+WJC2vn6T01fmF4pr668YPnUdMb8SmVy2uemBS/e'
        b'3jb03V8ACeBeqcwx7zB9KvBvv6Z9EhWVqhzBJWOemjBz9MyhJRO2DXntxfd5dHhK5LT5r0sYUj2UXMHn8/KTQIvJxVt5Dl8l6/Eep5ZiyKbx+AbwLvICMKItyYX5pL0g'
        b'G1+Qo77F8vHTyVO9VUjD6iwrnUbBZTEKZqeIIFEigoTzXDAwCGrw4IEt2Pv7EEXukdOHPUE1FrMA7zU8xMxBWaF9oA9xaEVb/RDn7wFa6VBKYpvxvnTSRve7cGuhLh+3'
        b'F9KtPvRo/UhyVVFmjqqQSROr8MeT8SKeyNlulMKtrFRKuCJjRmQ54IqM4Yqc4YrsSfmDVFJlF1xRiLiSIR+DispfgytT1PqQUSJaDBkvRwtW92G7QK+rHkfWX/54Iu8A'
        b'kRsdP3Bp0OYrYWtTQuUfLi9OSf/lq5rru7ZvO9ZW7Cntfy3jvZi2z7++/4uJ+udT4mMVr771Z9Psp15VDTh4O/74U32nnLg9649vvJDQUDflbPO0HaffS5v4r0emfPff'
        b'1+MXvH29YvK0R+f2G3j/f0CSYRsK14B0tjM7mQrx+ARHTg0uJfvx08ymwWM3uUv2N7ANU3G7FLckMhGFHFaRDbnAa/YZk+D19kIOqclmHjfXFDMcLIoF8aVlCdxqSQYm'
        b'JM/n8D3cbmT3HIQaWdvy8QUKopkjN2fPxmsH9SSzKB94qzNihlZZOuFlnIiX/QAjQWjRAF4Gc6E8z6v5WN4+yIedCoqdgJIU4TzKCpfTVulP07pdEIC1VKazDw7EVFrp'
        b'fj9M/Sy2s0muwEZO5BbqvViqxRfZEA/BJ+TkYJWse042FkmSDN0vRZWKXnKzgK0OujvZpwuWDhGx1N33Z+hTg0EGcovVbBovYumlBi16cfZGUN9NjV9HpIqFW0PVaJZO'
        b'3NXUqCUjw0/zg1Fohh7UR1OS/ZFVYuGXoGcUKSitMzVmZEtP8s6BaHrqcio2LbLlGMTCL4xjkbzyLboc7I/FDxYLx0Yqkdw8kG601ijKM8VCYUQ8ilcep9D53WkjxMLM'
        b'vtPQr/Pug6Jvsqvn6sTCiSVTkJD/FQWU9pE5WyocNQnVVPyVtjOtVhMnFtYY4tArwyppnQOHPFEtFt5w6FFRyDX6+ox1oVaxMEkVifKsM+mAJKmiJPPOwEnTUWNfJQeF'
        b'aYeflKD3rVegT4dGsAXubJSYQcSQUDSrMpWJjO9MnSqZMyf0R2+OXEKb1PjbRsm4FLtwPDIJHtr3tMeXPCEW9smcg0x1mRRQcOuyJKnx8QL6g3k3B4CUr614VCwcPK0S'
        b'/TvtKAevj2rKkSYudkos+nX1Alpn44JpE8XCNenh6KTqUTp0oQvrTdKTuavQlKl/5qBJ498cNlIsnDdtDJqu/zmdTfu7CQqx8OLiYehYIyXNJn76moXI+rsXP5A59IDD'
        b'n/w9uXR7fgFJidjw8pW/f/yjkflB2f0X1EfUvZWRnBKVtX3bK5t+vHJ3+/vfqP8nbELQy78buLl9wEuV/3703v6vSj6KOh371fFD9vKffvJS0Ol/1KPTRZtNXPQuuf7Y'
        b'F9y76kW/ODbmVGMzd+HFj9aEf/jVvHcGLWg9IISMeE+3MLF4QfuL7zaXfVu343a/hruqgx+FnR0cb3nj8idzP/9nac7Kmb/59jcTf7lrztRFrpfO/e7J/P63dh64d7jw'
        b'mef7m7bfbBz3+8wd/0iob3p92FlnVFtG/fqCr9Lqr9W/8bu/Pj/k09i/7/ZMcPzpO96V+M2fv1ibVjD29tbojz8/tW/WihdrT75+9Fd/mV/+z4aq8+999eL7r383fP+Y'
        b'Rf/KLfzbiE+S0371zi8P/eiDP0WemRSS1nfolJF9vzz939OFjYOn3/s3Ghaz5Njt/+hkTkpHXOQsaUuZTXl0Z/5sJXfYpgh+IQffyE2KzwI5iENAv2+rQftswKeinZTY'
        b'EWDwZGcivJ7AIbmLbCzlSGshadaFPYSKPjzpgUb7W6spDS431y01VttqrJSqMkI8VyTEE9UyIMXwN4KJCRGclu2GRDCRIYoPldNdEp7tlcCvrNN/dqWRhcLzUVwwEHE1'
        b'Z9f6iDjIog0Ws92PbvfAVDj7UB/JplVc8iPZ78T4k2wDHfQdj4MuTmk2eRrvKcwBlbsNb2E+DltJax5MUpISPUquKMltvG1qgPqgkP47gLwgC/UiQ2W8EMIM4DxoJbwg'
        b'aw4qk1nkglxQNKMmrkwB10rpWgnXKulaBddq6VptkVNuUMkLQUJwsxpKgtwgZpYFMw0m1KNKFwS7xeEoqFBK8NXSHyP+kyjBF71ufF44lWqJpyhb1MBTVMBTlIynqBhP'
        b'UT6petD2eVcNWVHADFJTTLi95Mk1cDUUDcVn8VbR0+KyM5d3uODqLxfUgzZdicQpEfL/Fu4RTjf/aFZMuuKN+BdblcVbtY0ZEYv6FZ9+Pvsfnyz/hy5/3+evnvxOU2pu'
        b'PNy6auT0RM/uZfdiIr678bt1x/O3vnG94pV7r7tc0fu2/vNIfOiQr18xpb354quXR+L9/Q6P2elI/bXl2/9Fr7w2pOSMSRfMpJ/xMJOX6sge31Jiy4gcHMbuhkThc969'
        b'QQO543XiIOfY3TqyHR9J9NuxHI7vjsEH8U4mHj3O4yOpkueVWDN5jset+ArezexD43Dr6ESDXtTPT/J9w1PwyTnMPkSOL8I7cRveSrbmrsb79Hgr3qpCIbE8ceN2fFVU'
        b'857Gh0DJbyuEJU7aE3X4HH7aJUfhQTLnoLGMBCwfTnaz+0n4rBwp1TzZtagf3rGYvb4An12G25JBMjNkUxPKKryBWqCelpF180c7qRgTR25BV9pA7wa9eldOPtDyENLG'
        b'k1vzyY6ukrq61ySkg0SojMY6ywqjsWOrdA1I2myLlCqYGnYVxSml31XhEjIbpPfE5a72yCpqHGzfCpRQq7PBo6630a10weJROpx2i8XpCXXVdVg0elI4lHa6o2Snu5Li'
        b'TtgomlBvSnu8j05QU9S//ejExv5+dKJLK31yHCf9ldBX6RJsREvEdcQV6DiP2iht0sG13GGpqezwGxCHSz2lxlxbLpinhkEtf6c1rorwwvLeeiiwahGYwkhHCqhfgg+G'
        b'D5A9ERINvGwHrEa9rTHI6B31HmoN73Wt0qCojOIM9lBnRJc6AwRmSrap6QdIZO9E5ebOhh8edSZrsgLrq5cekTkoDdj2V8efTZ+aXiuvvvjTytDK3+WpUPRXPHlpnI4T'
        b'7bjnyQ0M65DsIlf91mK/SrxB8gnpXre2OvyMcB2+WGvgN3ZVH++8BzzlNe6wkepAcj6A3SX4Bo8axaI4r9K+Fn6/1PgjcvdAgKbTH10IIKyRuoEZjZ5go1H0VIbrUKNx'
        b'mctcI95hSwXWo91Wb7E7G8QlNTJwXaWw7lK3MbPDUWGpqfEu7K4WJEAy8TF4hHWBGsL/iSQbolqBuKiIUI798syVZ/KEdEceWZearcvRG5QoeAmloIcjA6Y3RPrv2Mz5'
        b'MWauTLZLtit8VwT8he0Kt/KVPFxJvwLfrhSSKOP2c1WNAMZJWXcQMGG5RQGsW9WMgFEHtfPAvhVCMMuHsLwK8qEsH8byashrWD6c5YMgH8HykSwfDPkolo9m+RDIx7B8'
        b'H5YPhXwsy/dl+TBoWTBgfJzQr1ldpqE9EaiQ0L+dY20OBYFjgDCQCQzh8O4g+q4lXBgMb8vKIljPw4Uh7bygl8whMkErDGV9i4TnhzFYwxmsKMiPYPmRLB8tvr1LtUtd'
        b'KdslF0a1ywQDEy9EZ3M6Whp3eGWQEC/oWI0xUEMCqyGR1dBHkDEKkAziSwUjivdHB2v9fqRS0QM+4I5O6ZFbQer0yCkCdodvBRUqacLpCtF413YmJROiHBREB0+aVK9f'
        b'sqZSI5EPFZOK1EA+VIx8qBn5UD2pBvIhY+RD/vtvAX8DmkV/suusTqu5xrqKuuxXW7RmqRNWYE3mugrq89/5lUn1Zru5Vks7NEmbYYW37OzV7BnpBVqbXWvWpumdrvoa'
        b'C1TCblTa7LVaW2WXiuiPRXw/nr6cpJ2RPVNHq4hPnzmzsLRgrrGgNH9GRjHcSC/INc4snJWhM3RbzVwAU2N2OqGqFdaaGm25RVthq1sOy9si0KMItBkVNjsQjnpbnWCt'
        b'q+q2FtYDs8tpqzU7rRXmmpoGgza9Tiy2OrTMCA31QX+0y2HMBGBWXZsjDQ+d6UmsXfTKe7DCO7ygfQgW+wNflniu+L6UgTEqKdSPSR0/XpueV5SVrk3Tdaq12z6JkLTx'
        b'tnp6RsNc080AeoFCdySIcNV9i3tTj5fjinV5cz+8PpHXirWJ1z+grgDDeVdjaGiBi1LtXLmMmgyTDPQMRO580pKHD+SywxrU/oWfH1PBzArPxGxBmxum8SjFZLgcuhy5'
        b'qGM22R5H9eN8fKGItGTjteQoiNfJpBVyhSWkhVZTmkV3RvPzs/M5hDeRE0HkJlknVllaokT/GtqPue2/tyIDuajsgHeR/WOhQZsT+9XnUlfBvDlZPsFaDgIvPotK0lVk'
        b'L7mUJm7tVMjQmZF0N8yUFKKfJBpBflkjR9WLmTE39OyTNuTSQ2FcAl7Papbqha6C3gjtTC7OIpvwVn2eEs0mTyvJFbJ5nOiV8vRQ/IxjmYK0pkFmK3TgiQZr7oF5Mseb'
        b'cHfVp9+ueW3k1sl1M1IjMl7+x/Nbv23WPj000dTvi3Xji/snZmyLD33aWr7pu+Xb/nbn1UkL+v+qwJE5dUXj0+uafl75ty/33jov3/n61peKHr88uv2JSb861K5alfvM'
        b'6L7hXz/+TXrd+sGbxv0k+WBt3ptv/lUYn/FRn9/UfDt4+d9sbYe/njJj2oRvC6vmC8V1urGpL/z76ooLL2R/ZNxx4MM//PuN1w3/Kv9I9psVxonhb5YvUe05WhG145Ft'
        b'IQvs/c4tHHdpgLH/IxGfaJ7fuWjspauv3vjjjdqapoE//vDon67kzKpcpItiCkk+2V0VAkOky3fpE8imZB5vWIj6YLdcnYG3MoVkxky807fj/gg5nuTdcCf3ENvXCMUb'
        b'8PZcQ05+UjZuJ1vZiRhQk3aj/vi6vC4rhGldeHt6X3HrDO+fK26dmYOc1AigRviCb8vJ+/p63IL6kGYZuc3PZfKcg2x4PMCND9/j2O5an3gnnW68Yc0MmG6oIJq0JFKb'
        b'i3cDMxf6tUXcpJ+Nr6jwVpOTaZEx5ECJaAcmm1L6AzaEzOHhhfa5zM5D7j1J9oD4KLanYDJSkAMcaGRH01l39Jk1VMfbNCEEXpSRgxze0j9YfPEWvjOcvsiWVRB+Ad58'
        b'lufIgWlsvFeHhXmVR3wXi3jOtEfIHXRSZYc8R3Yvpjpie/0wHTsVJY6ruEwT8TUF2YAv4HZxL+AGPg+aLa2RHA/O46AtRzm8DWZkLbP3902rh5sGcoIcz6cNvUmPKJ1Q'
        b'sJamqqfRduYDIXiSbGVGcE2VbBLeMkjUdO8A1M3wdl42qKKkiYlympmyTLKWPMsqqKnuSytIgkF24fPMsVWDz8hmpZi9W1ma/7PVq7OADtKvFTi6pL1memXzVDVzxAzl'
        b'RXcIOafhQ7lYnpq1QiX33wj4U3b65anYDb+hPOh0Iq01eAEUiOJwkCi6UwJop3abboXpDqm/1wq5TiVWEh1YO6szwVcxE7fpIcghARrDx6P8NYYuTX+omtfsVUepjNOD'
        b'krfAq+R1wPCqvPdHzvWJRJRZgfjg5VbxdotZ0Nvqahp0BoAiE2wVvVU85cZya0UPDXrM26D7Iyh4EKd6hN57vZzKMD3AXeyDm9izxPP9wIvzYNehDh2xG+BmH3CDv7j0'
        b'Q+EHS/CXcN5x52FZmUWtkyFlD20RAgeiJ0HqhzTEnuFdBD20ocrXhuTeCGA/vB2je27HEl879A8X3b4PWoiLgbWhB/C1PvApc5k2ApD9DW5aaUq1NewUc7ct+OE2Gxlb'
        b'PfL7J7pIojOpFuHQWjutS4fFUstOTYPqwpSLLi/Sk9SSRlUCGgz0KMNlt2mLzA21ljqnQ5sOPegq+MZDN6Gz8OLy8YY0Q4ruwaIx/VGgrtbyuTqOuRTVDJiUyNiYfPpA'
        b'fJXD50gz3mCVD7igYA4tzaPNfza9Vp5lfuWT+OJPTa+UfwE5vvyTmJ/EnFr8ieYnK5XarUOZ11BM/Y9OB427rdXJGSvFZ8gBnZdVFszA+3ysUodvi6bn56fUMyGooY+f'
        b'GCSJQGPNTGCZQDbis9KJY3ramLRg4PUHuXBRwDo8n5zPJZtAHuEXT8E7uWQdudqTqUtF7UveEzOSh9EatDyYi6XGVInaS88UfE8bVy4k9QEca4cm0FgbWD+8TLlfD75E'
        b'1CKA3FyvfIlkzD9Eft/dBRNKLE7RCuCqcVpBB5YoucshKb0sUoDTbq5zmP1O/Jc3dKmI1jGJ2UEmmfLhGagK/pmrLHZTD6oZ/elq1pT8VEJXbUEDQaZda7IYXhcGIRf1'
        b'V0shByN8KtdD1K1RZAPTuAaRK1bPzHjeMQEq+NdrP/uzKQcwNqn4M9OnpiWVXwifm+Rv6Ta/n5SRMDJUNz10+vLoopNNE4+kbgDcvQYSZnDIDdVAHc8wt54cI0/56wcG'
        b'3M6L+sGU4U5Kp3HbCDlIqxy5TtofJK4uC5W8kB62eemwOI3eqWEsmSFnhBc51yDOK9Gt6udFoS7vFHiBMXycFIix3fg6sSc6cDcfklUBuNvi7+3UA+DeCjmawNd6IPEb'
        b'AzlMb7HW4D1VRAlD945XzKGFObNQG6HPoaUntyvROij/PWgZXc1svpVls1urrHVmJ7TLKjyIGdZZVkgEO9WQ2o0x48EWHEE0k7Aue70lAZBBW2xZ5rLapRER4KrCqRUs'
        b'5Vano1urEV3X0AKHrdYrUFmBR5prHDZWgVi1OKiVFrvjwTYlV4XYopkzsoH7Wpe5aH0gjMRTTqu1e1sFsLKdZsp7eyYPXV0e1QWuR+k6u2bW5RbQnW8WWaBAPyfL656p'
        b'wZuSi0lL3pwsWbEOn83WLi6325+0Lg5CM6rCa8km4nalQg2L7PX+BpEsA2kZ5HXwLEb4KtldCjxqN7eM3FDPx8+Q9eyYQhS+vpBcCw2KhlknZxA+siCbxSxYTPbiZxwa'
        b'17wsuo9ZSlqS5rHt+DZ8dm5WEoWxOTuPbOIyHXgTOalbifeMIKfm8vTo9a3QInKeHGRmGnIuGD/v36x6TQnZ7621aL5+ngoVrVHik2QvuWqNeny4wlEHr9X9bKH+teeo'
        b'l17GnDXYxmWaI+LW/uQEEFMz//aUm2vzr/Dtlm8/7V9+3fXd2stv/3ZIzaFvhVf04Y/z629X7xk78CX52yXL9KXO83/xfP37sc+6f55z/kv9/DOOTU8+c2zNnz78RPn5'
        b'tXEHzjy2+LGfaHdHvKMLYvru2Pl4PxBjsrmOXBT98kLqeHIQtxU56YZLdB25FZJAjxdQKgjkEp7eT00qaAi+JifPkPahbIM4NxVf8juqCLr8TT25Q+6K+1ZPKYaBIJA8'
        b'nNySrGAoNELWB6jrIVFQOIM3kgMhudPIIT+jjUiRnyDbmKBg05d6xQQaRkIMTEIO4GdFvf4S2V2UaCAnx3U5FHnWJHomHsAXbcymAEu9jDwl2RS225hJYRI+s4zaFPKV'
        b'aDneKJkUzpdKnny98lGhlLODTnhPVA7rIPPRalDKRVIfKhF8MafsRH8DainwtoGRUx8B7In6y/we62AB9Cx/K2UBMV4WsBZ9G/NAJhDQiN6qnHIjELMeSP9xH+lPZYpW'
        b'B63rScP4XnonbYOrJ237pK8Nk7slcTNLZ3Y20XfTGuoZVGu3VHqUDmtVnUXwBAFxdtntINNnVsilllKLdaiX9s0QmVNHnCTkDpE8ZUIrQyVWJW9RAKtSAKuSM1alYKxK'
        b'/qTCb0dof4+sSowLJUpvjOr76ysP3heifRFpvvddn7f+g038rOfiW+wVGDVaZqaamkE701xH1SKzdK98CXCvbtkW3X0CTlJSOGF8Sirbd6J7QgLVPUFjeiB434BP0mbW'
        b'mKu0K6ot0q4WdJj2ueMJb6ceBL7O5uwGjN0CHalzTNKmdxaLTVJ3HsL3uqplwQUuejonHt8g7kDGR1qozRIIcGkWFBVLfHAC2cKlReGdeCe5lkuu5aCR5KSGHMjFe10s'
        b'iljuvFyDPiEHqGpABWfIHV/lWTml8TTgQXZeAUjU5OlBoUBuz+GrTD5/XZ/FTshHCabgPUnVyDWOktqF5EI38rk9ByR0fU5+ib+A3lYSRO6Rc+S6i0qcC/GxXNJGnzGT'
        b'vVnUcJ2YTZlmImWjHUwadMKknDxDtj5BiUibLnTZ4hoXld3IPXzeHMDOaXewqB3EA+UGCTxJp89RoFXkdBBux6Au6mRiKCny/BAGWYbkC0ZM5TDwYrKZBZICNnHLloh3'
        b'K8UK8qnz1H7+ifHkhhhAa1s/fDUxJ5+N41OJMJQcih4tIwen4+3Wb5PXyB30dEn6+yWD3ngujKSEyouKjW1c2gb3KzF5EZ+9/UH7WmSPjjiizXnpi20zPGN3HUgcXO/e'
        b'OXftM6MrL/wrM/vHX066umBx6etzk4+X33R//MFnVw/G/kjzaNKH7/577OgRe5es3Bk/96vcks0/zT3zrSZhxHszVL+5X5382uBP+994L33PwDU3P9+6ul/y4G1H1uw+'
        b'mJiR/TiwbXb66/wKfCKXMTO+3F7BpVbiC+JZvs0p5LkOjq0gO73sVGTYy51sA4QcwidIC2P8ufgM38H4yVGL6PTZZK3JjTZk5yeAJMUjNW7j8bo8ckN8++SEPn4KVBK+'
        b'7mXXk8az5g0n5yZKXv7YnUQd/SODWLVryNowaBneQW4XMj9UZQ0/DLfMZq6q5PSKEcxPtZDF2cC3ybn8JJiNZBnZbR4mihI7lzZ4Dfy0fnyBrGcWfm6SyChD/x/Z5EMo'
        b'E5TIBuPkSR2cfKySnU5U+/h4sPQXyg6p8KLxPdqfnUo1SdxcKXKneTSZT5MFgSw96Ps50crFmhb4GP58H8crg+R0J67/wTB/rt9dM3vL79XeF3rgt6/4+O1QyiiAjDK2'
        b'4eMzAYZ1OfMH4uGPy9TF2qmEb6emEjsN80ad/ARbhdHINg/slGKwTQaPrNxa8cB9DI/KawWmBhymCXvCAnRVJhr5yUxl7C2pfeKERf4/2vN5ELrZqV2kH52nxXChlsv5'
        b'GEAoxA0exzOhsdcprwkeHMJTwZIP5mJi/e9Ecdoh9IoFNlRPJxsdeXg7eapA3JvmUPAqnmxJI0cCWFiw9N/xv508mgS+TC7IyhRWVKYU5GUq+FMLirIgQVkWLKjKQnYp'
        b'dql3ReziKmW7IgR1Oy8UgrAT4o6olDH3YuqrE2oJE0KEUOa5pGnnyzSQD2f5CJYPh3wky0exfMQujSVSjCADQhR1qQl3R1aqhWghhnofQY1RuzQAN0Lo085codlzkZXU'
        b'n6mv9EQ01Ek9majDcww8Qz2b+gsDmtVlfaBtnDBQGATXscJgYUgzKuvLPJVQWZwwTBgO//tJb4wQRsJT/YVRwmgoHcC8j1DZQCFBSIT/g9xKqClJ0MMzg90Irg1CMlwP'
        b'EVKEVLivZWVpwhgoGyqMFcZB2TCp5vHCI1A6XJggTITSEVLpJGEylI6UclOERyE3SspNFaZBbrSUmy6kQy6eQZghzIRrHbueJWTAdQK7zhRmw3WiOwius4RsuE5yq+E6'
        b'R8iFa71QJNlPZEK+UNAcVGYQ5Mz4OMejTK9lLlTnAuQeuqzFG6IXlRg9FEQ6Ggeuym6mspwoiFU0+Bx8OrnRBPpk2aGCWovTWqGlzn5m0WpZIcqTUEBFRKhTNIjUNGht'
        b'daLQ151QpuM9SuNyc43L4gkyelvhkWWUFhfcn1LtdNZPSk5esWKFwVJRbrC47LZ6M/xLdjjNTkcyzVeuBEG440ovmK01DYaVtTU6pUc2M6/II8sqzfTIsmcVe2Q5RQs9'
        b'stzi+R5Z6ewFmQBZIQJWe+H6zFYBWxSNlK7yjmBKW1fzLVwj38QJ3FKZY3Ajf4w7jhwJTl7gG/lYRGPBtvCNgMirOUHWyC1V2ssaOeoqCG9xx2Q0gqyg7AfPxaEY9Aha'
        b'zdWp4b6KXrUg+l4jMsqhVsVxoORGpaBmExv0e2N3OkVnLzNpjjuczDq/8CBJnY2CqCeYxTpYSQ/2J3G4JjE/rpJC/di01Ef8UUgA9SK7kortWke9pcJaabUISd0K91Yn'
        b'VQWAtXn9yRhkr34noitoG3ZruesB6sEkenuSSbBUmoFr+FDIBPqGtaKa1m4VxwkQUYIDyNW1b5/ROb/fx1rH9ok6ejN6pGO0hzN4uJTPKDv47L/wc19mSEkp0Kk8EZ3B'
        b'0h0Oc019tdkTPI/2JMNut9k9Ckd9jdVpFyjjUrjqYYnYLahjb4Mal+w21ONpbcZTf+uTFILlwCliJCOFlqfizapwEQF6vyNfKW750Wb1ICB849uP9wLwbcfrO6MMm7iG'
        b'eovWBBNSASy8xjBL/G8yGQDGNNQLf3CpWZaem/Uvn9wygDkFdI+GAcB4L7AICRhdvUv4EJ+ZXMamwqM2O4zM19Kjtqyst9WBhtpDQ77zNaSCbdO7astBy4WBkEZAW19j'
        b'rqB7oWantsZidji1aTqDttRhYShe7rLWOPXWOhgxO4yjYDJRDDULS1zwIH0gsJbAXdTAwz0cC3vgC/bsO9zDMfv6g3dUqdHiL90RmNJ6KmGJxMWysqLaXFdl0dpZUbmZ'
        b'bgTYxI1TeMqsrbfbllvppmh5Ay3sUhndVq23AI+YCcNphw7NMNctZSZxh9MG8h8jBXW9WvbSkvc2yciaZKJj6mLLXCQqlPr4TOEwptT1tJs9NRp62+KstnXwqyStwwr0'
        b'U6qGvkb3tf0dWB/UR6miSTR49ySTxEq72Zzr0ZZRbrPRqKraSn+jiYtNhdBpGroliCssdliUy4EPmsvpBv0DzCc+MZIikRx1toRoCsRTcBvJ3b6JelD0qbqaO5/aFsiW'
        b'LHoyrjQ+JylbH5SgRLVRanIPHyW7XFSqD68CZZRcJjfmxOfoDVOzqIU+sQDfICeK9eQUj8bOVlTlK1n8aXw5cqnDkJ9Ddq9QRqGRtnC8V2YoxdeYnyY/2eFva4gv0Cfk'
        b'6ovjcyaQdXoaTHdrrgIkUTUNw2dkhgRyPA6fdcTThlaTE/kKpMBbOWhI6xox4vez+AreX4Lbya5Ccq2UtJPdpdTYUMiR643yTHaIgJwhL6TSFimQDO/jRizAa/Eecou9'
        b'H91ItjuyRHNOLr4kR5HQWnwGH8QX8GYL28t/FB8kex0wLso+oForVnPk4vIhc61zJo6SsQBJ5ut/6tM+uXh9ekTzE/94NTwhc+5/+n4Zsy9yf/+4hSNKykZGVk9POTj9'
        b'6sv7sqdsHf27pDcqH//Pv56tUuyMPN736cF312/PnDnz5wcmqJNWZq5PHKce6xi7ZMTXL3ynO3TJeXzwjeBlR1768XpD46BV7776Jnnys9dK2xY9dn/Wz/7Ud+gLH294'
        b'S/PXD176vTUzcdClPX9feTbqm8Wbtr8zc8p//nZu5LLCn8bu+MY84vi7zU89n77+2q9+++2AJfcGv/73ksK7a8aO/pac6qPbEf6Nc0Bz1eY3vvrkg683ffbxkKKy9KP5'
        b'sbpIUes/RJ4rpJOVS9pUSK7nyBZ8CV8kG8kh0XBwlxwjpxP1ZBNpTc4i7TKEnyEvhGbKlPgSaWOGhwnk8GO4LRke4ZA8mSNX8fP42hpyWrSmHC6KSszJz4NbQzm8IR0f'
        b'1lc5Kb4mKEbmZucnzA7NVyGlnFeTU2NYbQ58j1BTF7QI3unLjcWH8InZpIWZYLLwlaqAPROyaSi51bFlsm6C6EBxkBzDpxINuolkd0K8FF4+nFyVNWTiG2xXAh+14raO'
        b'YAnPk6346FTSKtpnttjxScnGg+QFHGmZiC/PwQdFI9AmwKqN1E6SnWTArclsfT1jhHq0Wjm5SS5WOalqTDaayLrcjhUHqHubHEqmy06JEsjzCrIeN2M3M/lE4hZ8Suwx'
        b'Nem1cog8ZwkReHJwiZ1Fi8b78cbE3ML6Kj2H+OVc+mOPsP0lO0zUVfFAJG4i97yHIufjk6yleGsuvpObn5ubbyCtSbkjnvDG2EjAWxT4GbzeKY5Ee2k1aSvAF5OUSD6L'
        b'G00O4BfIM49+D8/EH3KosI9IFY2BjIBZg2gwXckatAZpglkEViokUYfNGOaUSQ8fRjCbkEaKpymWRnHiPtCqgZK00y0Qn3PKCIR+mCsmJ77KxIgmSP7byQrUFHDSsMfG'
        b'QF1Ueuzek4VFO2HxsEAw4PyinfDsKw4P9mapBrHgl92JBTNFviYdbRGlPyqzAJuhrMongEnSARUVHJJE35ULSRsAncSLTsJE98JDV542t6ugYqbMMIB3e1mpjfJ4uvvR'
        b'QKWQri0zV1SLe+i1llqbvYFt1lS67CI7drAvdzycr3dWmAJFVT8HQqfZXgXaiffJHrc76nz7HSJWeLc7vPITlXosDn+1vgf23/1pbrXoH9THFobeKUijwStCP7MukyKj'
        b'Th+IajKdtHDg3ZhysXDC6ptoJYeKxnLTly3Ifj1GPN1wq3SIIyyMR3OjgSUgcjEPN7lm0xvrHeRObidZwruz4uWwc+lO/HxqBU+e47e7P6UAyM+qwRGTVqitA+YNVDjO'
        b'UHTPNOe3T9bgDdUpEbOqfqUZ2jgpJnLZha/nztt0+1r8I2FFSWGjj122vcRNiLtp/fS3m39bvWt41OALF5aP+vnx+ZOHjUkuis7HM9bXv9HeZ1P++tn70i5GDfzPyrpB'
        b'TwwYVfvRpN21K5rH3LiybOf0pz8wfPPSQhs+v+3FW79veP/OqZODH3l2x+WYvcpD21Zf+sfsO8/+9fO/HX1Vpnk/est3fzu2a8Iz2oaGjyN/85+QlScmvO+x6jRst5sc'
        b'xlfJpcQgss8vaBs5jbeJ8R524i34LNs5crokYSN8nqxGWOmkNIM8g/cOCmALyTnBg/yYArkzgsXzMeDzcinWD2nS03A/peRcFvMbIBtqyVMddB2oeio57UfY1wD9pzNo'
        b'moh35ZLd8zsiAkWMYG0MTsVHE8VwFYvJSbpTEIKv8uR85HDG/gqAfd8lbXgvbvaLCLSyjLVrOnELiZF8B3PEl/HeQnauYxjeFSnxxdXkksQafXzxTLp47qK1hJxgQmk2'
        b'2aiGtgeMBQ+ywybOmKzGJ8l58pQYrXkfPqhPnCJneyIKpFzCDybbp4myyfaRpCXgNArMw35xt2RetbidsjtOnpiUD7JoOV7LQouDIIB3yuzksKK7c+W95V8qSUNgHCvN'
        b'n2ONF3mVUjxWwMVKXInGw9CwnQ3RS0HDrdJIjEGqKtAPzRbInHqIjcGLz3a4I2yAJB7qcsR2sKS1yOMf2agz7ABdm5IVpmtTLYLq2vBH7WH9Bc7Jw7WsiYuFBwQ+IOeN'
        b'snWfH2m9Lx9pSKuErtCWeUKNdTajpAs7PDJzuYPp6t3r5Z4Io2+bWjQu5vDeU9U8DBu/qq/XVtLpuQALoG9/OA+SFhbuv4m3ZzZyrDdoqcw+nfbKntDIHaO9QMe51Vxd'
        b'rFMmcI0sT5+slIl2QbiW008GsB7yBfdH+/hkrdUBTaioZhxmJBB4anJimjG9gFljAxBtra2vsVZYnUZxuB1WWx2bJU/Q3IZ60dAkDoloVfIoGDv2qEUTrc3+AJdcjbHe'
        b'bgE2ZTGy5+fwXudHGjYLcE7Dy1lghlV9vEMW8HyXSWcDRpFGoCZNGARq1FzCVfKxopkFuh4l1hRPu5ckdhIa12EFE+e0y4cT6DkcAG03Ghfx0mcTkL/VS7zXPRZGsQZ5'
        b'8dC/MSqKZTDs3bSgM1apjPRwvJGdA/KC1/jAs1s+GYz+l3uhx7E1cAzwQeCO86vZgDRyS0WvGGgDNwWg0w8kiRPIi9C3dNMEpdFY4zQay3mJWSOYo1VhvjbQe9+rCZx3'
        b'GPgpj36fNliMxsoHtcHSqQ0+rDD4L6Nh3gWylLdpxdYAgeBLRGLBrkSXIf958WvVA9AZGmdZZjQu4SWboojGAQ2k9wMa6LMLhrJBosBDvR5LXm/2nkajDnpc74cTHaDq'
        b'Oo/Fw+ZD7p0Pbur3mI4qmHbHA6aj6vuihILJ/hQlpn4flABlxLjiQW2wdFqXPod0OuJeMtFh+vWj7N1SAWoiMxqf6JYKiPd8PQ4Qb0d02+O+dFcHMYrNN/G+CUgEQurr'
        b'vNc83zECdd02DkiEWRCMxid9/AZGItifTLDbXdaHH/rR5h3nOk7kHH/I2FOqyCpt6p4qBgLsxXjEdR4Pxq84/Q8cD4er3Gjc+MDxYLe7Hw8Na17IDxoRVm1b9yMSCFKG'
        b'/EgUNWD6SJTGiRg5gnxMVxyh+wUeTYHNmQ2M2UJPC1mEnsbmASdijMZaFyDsFn+CJQ8cIvZAr1BGOtt3uhcDxCrd1f0ABQIMQJkp/gOk7Yo8A3xDNqDTkAk+lssl9wKV'
        b'uh+uEKPRaXdZBOtyo3Ev7z1ExGh8MA+DFuXrhO+xH9aP/r5+9O+uHyKBTP7hHQkFBlpjs9lZE49205NoX086nvthXYn1dSW2u66Iq3vkD+6JikUEMhpPd9MJPxy2+VMh'
        b'uX/7i1CgWNDRfiftAd1Ph7Z2XC/iV/OrZVI/ZE20RzLxqtIfzTxKGDMACxoE69gzgb2Td/TOo1hRbauxUB/hWrO1TrA8SFYONhrFOo3GZ3hvhHRRwODpUe9Vkb7+ep/r'
        b'Xj6m4qjI9kLY1DR1K+08iAOyYGpVRuPtbuVQduthYIM7wFZ9D7D1NofR+Fy3YNmt7sHGMLBOESTnI6HN4pZra+C89AAdlD6j8W630NmtXokYzb0QMVR0Cx3kppe6hcVu'
        b'9QpWVS9gBbEFboYqf+QHLcJ/9dObdho8sfv1Q9c/XTFLkT3CCRo180LhBJkgp3yrLzRlNV0pVEflW/jj4tqRVgxrpKLgM1rp/WFsB9paV6Wtt60Q97BTU0QvDld9vY2G'
        b'/bnPpxg8XCqsnlXeafOol7nMdU7rKov/wvKooKYqqxN0dcvKeq9i+kBTCIwCA240vtxBRtQsXKjGfzSkh8RxpUOiS+7khWh/XKrPUWNz0uhhK2leE2gxh3xlpaXCaV0u'
        b'Bo4GclxjdjiNom3YIze67DX2FlrbZpp0+DP68NSj9hkjQpgxVtz7ZaZ8ppbbN9GEUZ4dNNlFE/ptPvs+mtB40fYDNDlEkyM0OUoTKtzYT9DkJE2epgnl53Zq5rSfo8kF'
        b'mtDopfarNLlGk+s0uUGTmzS5RZN73jHWRf3/4x/ZyUWlHJLXOCnuqVol5+S8nPP7BRoZ06eLS6SM57Tx8Dc0VKUJCZWpZWq5Wq5Riv9DZaEKNfujJRo1+w2CUunXxc4O'
        b'7Yq2Oshm0j6R3BN9JdVxvGseXhvgKimX/jve6+Qq6Y2HWilnkVnVLKQbi8xKA7tJId1YFFYhiOVVLMSbgoV4U0kh3UJZPozlg1iINwUL8aaSQrpFsHwky4ewEG8KFuJN'
        b'JYV0i2H5PiwfxkK8KViINxVzvFQIcSzfj+VpGLf+LD+A5SMgP5DlB7E8Dds2mOWHsDwN26Zl+aEsH83CuilYWDeaj2Fh3RQsrBvN94H8KJYfzfKxkI9neR3L92VB3BQs'
        b'iBvNx0E+ieX1LN8P8gaWT2b5/pBPYflUlh8A+TSWH8PyAyE/luXHsfwgyI9n+UdYXnTSpC6X1EmTOluiMi1zs0RlQ5mDJSobJkxnsky6J5wesZnbcTL195c7b2J5D3P6'
        b'PSTFl+v0GHX/YL4oFeY6SgbLLZJ3ndPKtpC8HiMsoJnX7446jYh7NZbAXSVpLyvQSYRqZ37HaE2U6JrFU0KCrcJF1QpfzQG12ezeCq1O0cAnvurdGpqZnj93llSD6QFO'
        b'gQGZ7ErJ48WsLWfmSKhO3NHzP+abJIL09lVy+nTaLXRAAuozO5iPKW0c80NZDjWZa2q0Lipg1TRQNhNwfjjgZR97pTojJS70HKKjkqOczh5BuV0/1MIvDbLHeTmek9lg'
        b'j3OrZQJwN6OYylmqYKmSpSqWqlkaxNJgkDvp/xCWC2VpGEs1ggzScHYdwdJIlkaxNJqlMSztw9JYlvZlaRxL+7G0P0sHsHQgSwexdDBLhwCflhm1AgfpUFYybGV1I39s'
        b'+HE0Cz2+CKRd+WpFo/wYrNDj3DbOAZSmUd4XrZbX9WelSlpqHyWogKOPbJRT2+ZquXMUcHh5Ew/PT3WOFtSNctEK7Yyn5Y2KJhmHlv1lPmqBHi7RtHDsSZNTtx5awWSC'
        b'oAL7bSoTjBMXQJfl0vOCYEwh08MZPbzReF9hHOkY6bg/snMl1WbqpdXh6CWaghM8ocXA7K21kvOkUtzcFOOLyoxWwaMwuixOO40fIx6N8ISL0cd9R+Ls9PCyfTpNZtCE'
        b'xroRo6sUMGEg8PQkiHviLjbUWO+ygyBrARBMEFCxXQGn2aM01jqqGOil9FShwmgR/7EzhmHe19hXtOClimq6A8si2pqdLgdII3YLNdmba2j4o7pKG7SYjau10lrB3KdB'
        b'ABFphu+2udbZ0SFPjLHGVmGuCTzET+MIV9N9Ywe0j61ZqIb9F+MLewYaOw05CK+wHqVnFXBd6/AEQyPtTgd1CmeilEcF80LnxKNJ986MOBMqh8Up3XA4LHZaIbuhU4q+'
        b'DOxT98qlK+hnwv0CIdShh4dhYLP7IRX9ypjoF8G8NTqHzlJ3KXnALy/+j2LGJrpPRk3ANIL8qr6dRqTXoZsl0+QvUI9eqVGg9IjOsnGdAfm8ZqfMZV4RdUs7znAmiYEV'
        b'nDbprCt1YhSAcFsrG4Ac+5HJXjvRSmrOoz03t4+3ufdHBUbWok4EtTZnxxFbFku099GlpvcMN84HNzCkVlewNHhpr4MXzegZ6oDA3voH1OoEVook2stzVg+LpTXYB1fX'
        b'TSyt/xvoh8RrGuoD/UG6Vowf63CVS8dAmIM8hSe58kihm3psFxOexIrYhimVderhNSqnsCA33QSDMmhLOsoqrRYKUBIcoHZ4oMPRx8cLHNoEaZwSkuDS6mT/vWG3Etj2'
        b'aIIY/Sqh14NV0PNgxfsGa2zXyCcPwM/0GfPTkyHJ6P3aeKfnViT6WjEl4BA+DTFiKQ88jt+5NTOLM2Ylz8qYMbcXrZEI2rs9t8bga00xm3k/9i25fnld/jv5JBm0s1gk'
        b'FNEDq2aFucEhnUjX1lmqzFT17nUbf9lzG9N8bUzwIrnXq8qvuRKP1saXzJtf1vvZ+lXPsMf5YI9mZN1mW0olW/FMPQi89fU2eswKRCOXeAq/14Df6xnwBB/g8Lm+czO9'
        b'AyBRy/d7BjA5kGrVwjo1V1n8kK++usFBfeq0RenZBbCua3oP2tMz6KmBg9oBssZWFQhRG59bnJHZ66CL9g96BpzuAyz6EtYJeqdND/86WLU2PuN7Qfx1zxBn+SAO6ja6'
        b'gzY+v3fgpJH9Tc/gZvvADRWdJUEcrKOnS6TFIcbYKCotLuo9BfltzyBzfCCjGD1jsrF0TKbX3fp9zzDyOyhAZypF5Wnq4kOv42cUFuZmF8yem7GgNxRSWogf9Qy7yAf7'
        b'r51hB8r4Bm0mUITZFmhNHZP/HD6Fu7vI7kCo5mdnzqXx2ZO0s+fNTNIWFWfnpxcUzk1P0tIe5GYs1CUxp6FMiirVUp0Pqm1WYT6sGrG6zPT87LyF4nVJ6Qz/7Nzi9IKS'
        b'9JlzswvZswCBGQFWWB3UW7a+xkwjWImRP3q7BD7ueQDn+QZwmB/5FtUhESHNbAGaHTCGvUWYD3uGudAHc3znSRN1NoM2veNIW3ZBZiEM/6yC2ZSmUyTq9eL4Xc/tWORr'
        b'R9+5jJ+LaiJMnkCxxtaLFSIB+lPPgIwd1FyKxsJOR4pgLB1GH39do7cL5A89gy4PJHEdpI06jWupnaoT86Cv+3Y35kngHAXM1y6O7QIyH676gfRaPDlLdzPgT94EqZE+'
        b'r2C+eQr6ppGlx5SQqo5znB+i3J9cLDpVU0uVT34RhakOm1n3wpZBp7a/TbtIIwJ0DtXMbA00lIHdhDq24iei7jaAQujX06RKLTLJ7QGBBhvH/O6ox+eqAZ2VSb93up8l'
        b'ajcTOMnBbK64C9D9FNFdB5usY+upi+Lq86np9ixlnDQ/dg3duT2O6E5tld/2F2+nm0seOTU8PMCvTi2ZJYz0W2GSlwg7gtFNU8QHu+9zjF9TxMi6gtfdkhmzvG1RsHF7'
        b'sJNfjaXOaFzRqS3dGA7YcwW64d3tQDGDBtsz8mg6Gacm+rCmA2GMXlzxhAXappSSaUolcWj2lVyPUjJLKUSrlJwZpeTUJsVCjXhCAwxSSskeJWe2JU0ny1OIv+FJKVms'
        b'1B0GK9FYpAk0SNlDOAl17PQTVXb2tSeGZL2JxmZ/GZK3qLWHbnSpQ+V8VFovgmcouobT+J7hN7qm8p7DdYQGq2VqBTvXiDfjW7Ehy8PqQ3U5ZHNiQZ4BPzuV+rDTKP8J'
        b'1Qp8Gd/Fe7sEVqQ/DroH2bHlJPDNiH3+TybIfZ//U0jXSvYpQPFaJagENTyrdvOVnPjZv7IgMSZHWTALTcvT2BxQGsKeCBci4DpUiBSi4IkwIZotwhhPdCfczbOCGu3d'
        b'D5P7r2bqEU+pqZF5Vxg5uk9s5KtoNAKZ4GOvcibAe4J8H96Fy1qbYK6hn2Qb1tnoSKEZ/Tc5HF7ni1iObaR6K1F76+hMouj+61qZz0FK+kbcwG7gfN9w9A/TRDb67Hnd'
        b'Qvue32KzD+N6hOb2Qust0x/ec30t3dbnm2zqreD1yujwPwmlS3nEgyum632TH7940DR0JdQPcZPwg9mFSzIC0+4HtTNHlKAykvz/giNue3gPJa7of2LA5/JCLU1enyZH'
        b'lBMAS2cAmE/WUpljLFwz/yV2Ta/kS2X2KU6FuJsFeeUxFfXq47wOZ7KC+3p/ObWWRggo7wi5MLpTK0cHPi7YLOKZePGsAYsB4z19x0g8yDPt3kUpfot9JL0aRRPm7EHn'
        b'B/hRfT3ow95DBiF+INijD/CckpkFYadPuJGCcYWy/104KxteeL573AmWcMeHOf4z2RVv6McND/nNZb/ugHWVo3wOljFsjYg0uxHNQk2c5KgsKwiQV30v0KMPlF4+HkpP'
        b'e1AxZDu/jLp1V3tdyemH+LwOdfSLdB7O2WWNQXLM22olWqXvrtVOm9NcAySIbgw5psIFpeq22vqp9PsXDlftAwQcBXvv6MPGhD1VoNN0Fm46fGEYonTgSIccwMSCRE4a'
        b'fbvBJxv0EN5kKDy0WiYNOPBcpfhpP7WMeoRQjw8XJWjkKD42VeTBUeSwxIZFHkyukdYkADWLXFTl4dYBAYw4Vvrv2MIFMGKYVvYrO6Qok1GfD+rxQT/kJwRTNks/2Sdo'
        b'KFsVIg9pyuj3dxXAcqOEaGCzCnaiVk2DXLmj3P0qVUKM0AfKlRYVC2glfrNXJcTRa6Gf0J95hqiEASw/kOWDIT+I5QezfAjkh7C8luVDIT+U5YexfBjkh7P8CJbXQH4k'
        b'y49i+XCxRZUyYbQQD22JsKgqkSWiCW3hyiLgXhS0XickwJ1I6AknJApJcB3FrvWCAa6jhYlSCC8aRqTjk4ca6GcE62m0O8bdxx3r7uuOq+zDQmYFlcXsUu2KFdLaOWES'
        b'hQKjIWOBs2gYsT7084DCeLg3mcF5RJjAymOFMYwYT/GEUvzz+ip4uCIPV6hTePjZMzx8doaHzyiB/3M9/Mwsj2zG7AKPbFZurkc2e0aRR5ZdAldZxZDMzMr0yAoK4aoo'
        b'Dx4pLoSkJIPeKMu1WxkJmp1dpNN4+BmzPfysXHsapWZ8NtSdVezh87I9fEGhhy/K8/DF8L8kwz6ePTCzDB4ohcZk+5a7N6Y5c0mQPhQgRuSS+yKayx8Y0dx7xO0hEbjl'
        b'Ba4suDaVkJsU352ktdBA2vNpJNEsX+xQGrVzOt6RaMiGlUBa85Ky8+dkwTLIoac66ddHp5L14fh6Otlhzd+ilTnoPtWJcUP/bPrc9Mon8VHx5ixzTWVNeZJ50YvvvHR9'
        b'W+q+dWPCUHU/5cDv/md/vE4mBn++Qo7gUyH4bFKWN1JlJHlWlpSJL+JduFn8/tSBgdGEfpoqJx8a1mKgQQQO8ivJ2SSxiq14P0jP4keOfV84Js/l88RdiFu9RxYfvkHM'
        b'eymy76Ck+DuBegquivFHo8APBys6NqjtX9Kk+89JyMQnRvge80G+SkkTPQvqOwop/r4ZEKa/2xZUqKVJpuACP0KpZngTLH2OW1xoYvSejo9QqluCAJeCAJfUDJeCGC6p'
        b'nwzq7tPcctTdd/gGFrhoFAANvtQ3N0+KJwi4g7cu0+sNNAAti99KZ7i0aAVuzsJnZIhsqQ8h2/D2iSxwrDA0teNNwLBC/TzpXHYOaQf665bBzM6PJ63z1YCscoTv4GdC'
        b'wkgzPskOh7sHqmig5ZVTRpryGgcMRuxweDy+MJQdDucqAZ/p6fBiHXv6vVQ1ikAoJbHSVHNzSSZyUS5Gno50BEaSDzgmrkILJ00oUTU4STOLGkvO4hfI/tzs/NwkaOAt'
        b'fEvHoZACnpySkX2uofCANhi6kkXPlJOdY3A72ZKSgptNuWgYviHDd/viFhf9WG3kcnw8sYCeLW7PZ4HhZ5Oj0on0eIM+nrQkJ9AwuzadGtjPGXKWxbqNzsctuaQtOy9Z'
        b'iZR9+SfIGc0CfIshIot6Q3aRm48l0uHWwwP4WR6fHTu+CN9y0aAVZaPxxkRxKjpOv3fAmhPPYqcXxdc3iM3CG7JkaDDeEIZv8eQ8C2IzJ4xsciwnV+WIm0524f10/V0m'
        b'bS7qN2DUTfZ+i3HIkzSgTz08ODcexqgtKSm/VIyAL57Dz/NFniQnZaFQx2ayzkUDoxT2JU250hcTyaY8PTk+SomiZ8vIYSu+xr7aaMVbl3uHzZFSWqTvCNPv1xUKhseb'
        b'eIRv4Hsh44BG3HBRD3WyYdw4spMG/VxlTUD5i2FYKRXJWog3wChfWbGcXMetK8hVJ3FnKlHYAB7vJ/e0LDQykKqNmQ64NY9+GyA+50l8Xg8IAASRQSuO980lDD3eSW4H'
        b'oxk2F6XhTrKRfsOvnX3Pry2ZbC2Jj9dPMiRAWwtK/T8MgNfis0GIHFK72Fn8ezULQshNct1Bbi3DO4Emtq+why4jNxHqO0aGm/FxfIINmmoE3k7a6AdK9AYYWry+QIGi'
        b'8G4ZvkReUDK0/zBIQWMxxZNsU82RQRNFXIGXtpM9jmUKRkW3kO0Ib4LJ3Gn9SbtF7lgKLOm1GS2lxdkFZHrEocG2r6J2TDj//quylXzyK0F/+cPbjaOHvbQHvR87+k8z'
        b'pn/+6383759c+FG/BvToG8P+WLy8UP+bX4y/oc66YIncy5vDjNOPTW8rL8vZlf8/MeExp/ZcDSpWKcqmpUVWL72z7JXRVWGfCvO+ytpif/+fr03de2h79fPpc3Y2LR/1'
        b'9x1jpnwd9dVXrRd3p7xrLR85IfW9o6r+84rSv/qZdariuevBu9q5jWWXRmSce/rHo06c4TdHbW/4dsjSD2LmfDks/De7t1b1/5v+n0Gb9H///9j7DrCorjTse2eGOjQB'
        b'sSuChaFjFyUWROkoxRYLXVGkDYhYqdKbgr2joIgCIiKgEr8vPaaXTTRlk2x64m5iqin+p8wMHU1293/+5382RBi49557+vnq+x6N8N8/a3lliPvOXZNyKtM+LWp203de'
        b'GhYVM2NceMeegy/8VuS2xPCpopQs3B45uWlce+z0YT6f7o7859Gq6/cO3/7St/ByxKc1Ce/vUDamLX3i7Y/vFJkFPbN9b8L7E99/dvsrNrsNSzbv3Dni3sWnnzmiN2zX'
        b'fMePZ3o9LT/ivGbPi1ueWruupn3n1C1Nzlt8LNK+WO3wQUST9P2lp34ZExpd8JHXz4W7FEdKXG99orBmxxkcSex2IMJRvMYPRbgwFjPYiSjB45FkSVHqJQfjQZ4UHaFe'
        b'gmeSoYBhC5nhDdinAh0ws+7Kp4D5mxgsARR7kpEuTB29zchQPwmblXgl2VBbME+UBm2Aq8mDyC0jh8I+nwAK5zPLbrM4LyacAw+dhsIJnIoBz8xhpE0iHPayZ0gGtlBI'
        b'ZQd7IkEoME+Yyyp2UYJVNniOITnFYitegUJjufZmvJKAzSnknfIhkvUbMZ0BKTzuYt2FRiIA9jrgKbjCyp6GtfM5WyaeHtWV4sEPKxlYUzjpqIs+lMNB8rhLmjgbTq9k'
        b'NXbFIropFZAdogiqI6WCbKYIjX6L2UN4aQLdTRnFlI/lGtFpgnuyE+2fEksoVm6GFrxqkJiCLcakt4qMdQ31scF4M1mEeCU1kdTdT6YNrYmQxyo/ZiLU2jlgsa+LKGiv'
        b'EMO8sQ6KV7LX6I5xxkJPuEBHrs5yh7gw1JMRheIJuEE6LWAk277qPP0gH0sdKYz5cGiWpS4fyUZ76rxgTodZSvb9WY/5EvFmrgT3TYEcjiSVCecWq+k5HVyd6AagJVj4'
        b'ygwh34mzfGAj2SkKneik0hK0QyXQjjesMBcyGFzIlGl4iFzlm5fXeD8tQR4gwcpJYQwPBNonWauIvgIwP4J2JNlkyCGpLYzBMzKyZ57nMF2hO0mDyY1uUMFnppoRzH0K'
        b'6x8re7zIMLiKfUkHeUkSVg2BkpEMlwPLsHIofTYEz5DC/X0DGO2qKAzHI7LEsRasnd7QAtdIR8DxSZ2Hh1GQ1A8K8ARriCwOqiiPhwMRIfQdfKRk9hVIsCYikE2E4J2Y'
        b'Sa5623thCVzBw2RYZkjCpz2WPJ5t7Vivo7max+lM7bwcpuN5iWBro0UWHt5g69NyJtaSG/3tSe+OwTIbB7aJa5HOaNHScpzIlteK5XSdBGiECMw3k5H9+CJlKs5KSaZw'
        b'z2OHQzlZCd2Fb8iHUidu/x3xmFr1tCNnSbG1PhzHE2SZ0NlphQ1k0PnDi+BUj+fhHOb5KrQFX0EHLkEuHk6msga2OOJhTifLuGQPkinXL58snjJh46ITjif5zID8gI3k'
        b'IGRPaBOFV4odWDOxb7H6P8+RyswCTDyP6y2eu+mLupQWVSITh1LQUvLTQhwqMRBlXMensZkSEwaJPZwicElMWT6dgURfSsRriXaXSFDqDdPu8hszBA/uIXZzCzCX/PVV'
        b'2UjqUGEZtZUl0WmSROlNb8sjwpI1Ub/ayoj1UZuieuKm6DwagFmAqCo0aQn9xgphLwqkvzJTzGKxa3+19KNUvNCNabXv1j0q75fOWt6mgZBUNTbu7q96ZOO2yn4bNLAx'
        b'+r7GDWzDGEnU2Q28fpYqSJMeRK5/Jtj1tnytKkhp7YAsN79rKmLfV2BTjLKzbn+FWJU6hQd4O9XR+NtHB7OIJhrP9Jd4ZDUjHJGSHB8dPcA7pZp3MvJScr8DecCSxth3'
        b'RlbRerCo5L9CG/qQ6ANtTQVsWfRBTLQq3GATDe8gPR4VR5NEIv9SBxis7bKGB6iEnqYSLPaJxj2so8BumsDAP/PuRwMpNtC8cmL/IMXdX6x6L9tMNSB+9HzQoL5zu4BA'
        b'01Z2iFu1twvMLiAyu4CwU1ze6TDoVlhfLG99c7Las7dFi4/IyEr5+VLEPoAC6X/dqH+6R1AoLZXr41NiIxk5a1QSQwm3DFsXRuMu+ixLw5/kHhsVRiOQLBewfBM6iCqY'
        b'Wxa2pwL8VsXvxPQNk6vCAg8NDU5KiQoN5dSxUZa2G+PjkuMjKJ2srWVsTHhSGCmcxmipAXX7ZfZL7rWaKeS9ypnPkQR57Fdal5Cqh4Oih4YuDItVkhr2xvBjiVJCl//E'
        b'XkMs9Y9ZaH1TVFJ0Wh2X/V+FDq54Nlw3+u+xoqBbLb7+628KkaOgHZ7so5Ejlul1EyP8bdUulh5OHVn0uigOXsZoK3f1+Bq9dVy380QZEbuWdWynz4IW0B/Pq6jGyewE'
        b'JaMw+CYylZu6x6GZLnxn0OXYZDCDMVhNNLXuEhyW2/FW8jbiPmgiUlx+AFWJiNC514epVNiALTaw19AZi/H8f4gitpe1Tr0ye1l+ZwmU4xT3O3URB1ltqR0l39c2eri3'
        b'PdQGc+MQ/VOAL2N7Og/58pkb3GMePMiSKakcGrze86tQR9MvQ2+F21jYhvmGxe6ojY4N/zr089C46K9DC9Z5h5HJQPSVfXJdU59chZRJr9gB6Yt6vlolhTa6dRdEIXs4'
        b'BxRsj1nRFVQXOmBPV16jFbCbCazQPhqzNTOtyzybiY3YMWLhIxmDycxTqmaeRV8zbyzzKz589pFC1O/rBOIfkLe18zY2IUPJhBze74T8vKtxmBGLbSTd+mfno50/nY+N'
        b'IzbbGs5ego0KCTOSee004DNVZjxxmwg1/qOYUXVrUBB/QDYZ67BVhKawlJgv1y6VMvLVpZ8YblznGeFLJsKGD89Grde1Wrd+Xew67wj/MP8w8bthG4duGBq0/DNnrckJ'
        b'1aLwlK3e2vt31F7LrlbyfsdFT9PL/Q+OhYG+iWyrRd+Do35b/4PQ5YQNI71v3G/v3zPpKkX3877/ACk5F/0euqzJTrx38wipkqrBNSM+/SrzebIIb4WvjzZgC9DsWwm+'
        b'1kR2Y2o/hZyRZGUNoHv6xuCRnsonnMbGXoPVI4Ki/83appfzgoVS9LM398fBTd8xtt8R+dBoIGdJ99CNvyqQ9Ole630uyvyDY5ZMbpcq6Z/tPt/q85UizIAdizIPcWHx'
        b'd53CXO+QguPCQB1p10th43Eij37K0fLH9duJ7xsMpBz2iNT8d3qx11HVW4Akc1qRekBUUuOP+/UauzBKUL/qictlJw/+dtCFsdJb35feCygmBwvji7+weA4W2nuNm0oR'
        b'YeeK0AxXPZKpgwkOwV68PuCUhwvQ1svg0qTF2WfhMF6xs1Myi6qDtqCL7RIot8a9/Qyh4YBrwbG3zs3DUx95CGn5E/sdwjsDDmFnKKzQzXU4Ut394QJzHVLfvAFTCtTe'
        b'eUnuICaQdPPR52rlDmMuxeG5I3JHRo/UuBXlA7oVu60hGq9l3mv07f2ZuwubIH2m2t8FNUu1h0iMhvP4KuZpCyYje0OehM3YbJxILbOXkrUFEzyzEk5LsA3ynBlVZhw0'
        b'Yjvz3HiSMQyAOuq+6ct3swDbufsGd2+RQzPuhxyFNmNfsIIsVyX1vAhhWINlAhQNglbmESNH6lUtbErRJh/PzcLj1K1yCa6yp/BiuEKOV8iw2bhiswAnsRza2JV1U6Bc'
        b'mSxS3yO0Yp4Au62hgfFTr5g/TE77ATMNsF6AA1gbxfGu68yGKykIIhTZ4x7qqmmdynw7d+21hZHryWSwDPXd4rJQYOX7moRTfxYpB9LDsUqAfdA6jZXjDA1pvCVDifxJ'
        b'WzIqmvu39nl6sE6yWebQvXewITkJLwd52lHzL3dvlcEBvR1S3MMwUvAg9VJNxrLJzrIRboJIOgHTIQurmJ+TyF7FsL+bf5XiqTB37+JlWDnZO0hHMDcPwQPa2DwL8pgI'
        b'YosXIJ/GBLlAOxwTXHbsYvOBlHMJqpFGezlhK54n3zPgcOzPDx48+EIiE7InmAjC3FAivawTGKk3ntkEdT7q1yVjNZFoPRmxd7GTd4gN5pOqBNkosHSZpxcVkIr8mGQU'
        b'SNuoHWe4euN4Vox8GJGWCrGQ3gV7jdU30ulE5SmnAFVHdXUc01l0HtoNSIUroTkllNa+ejieMyRPlBtCeuw8Z10tTA/BY9pYEmy40HS47uxA0tjr1BjtsW6LXvSQRH28'
        b'pp2qCwV6AQbQgFl42hmvb1OMwbxZjnhIG/a7K6DpsSl4cCiZJqexPiWQvqTRDiu1MAMzDAUXXSk0hMCllVipDfmYC5W2kI3XqbcveETMTjiL6SPg+garEdACRWMHQw5c'
        b'id6G2VIXG1KJ4jHYuMDMT8q3CzbV9LVHiA2R8TLBJHS1o621wJWJI3AKitSksbDfuAtvLHV0qtycXYhjL2KLPAKPYxYr9NgsT2FG0ERRCA3dUB8hF1Kod1ZCWttBW3FQ'
        b'T7A0IB+WrtkIe6AO2/Ck6AKZeGbWZDIie0PJNk9mMZFHD4VMxKqVpN7pg4MhMwry1uEJvKqzHq6ZpEVgQQo1u5N9IiuuD3rbIE8Hby3TwTSuBc4pyP9keWHJbDyvhy1T'
        b'8GqwQmS7DR6AE6l0HpCDA0u87MmeQUZ5CJYF6cqcydTM4cT2OZgDlT6MLffRaHALFAZYhZdiUvAaW4mkTZmY0dNh3Je72AIOM4/xZWwndaQrRAE3uNRP+rl8tgRKRHc4'
        b'a8nifTCTbD/Ndp6kF4v8eJiGk7eXQyCPzugVDeAJtVgJ7cEJdE9YHOiwVCKkBRunrRFSqL0KTsARrOaueq/lOktUIRsqVdLTN4A12nGJ7ma8ssTT28/f3sGfxYLQtUdD'
        b'BFiAANuvsShwEJyJcGaz4Z/kXPf0omdSqP2L3vbk6GP8O4PgcrgPc+2Qk7zKR0pO4QYJ5FlgSwqF+JNNWxMUoPDjBCIhyzCvV/CJQOZ/G+mbWoayvgeLVlkSlfYqnPYc'
        b'Cx2eYydDvUzAS5hhCgex0YEN92A4A1fJLtpkrId10KiLl4yxKTkxRRTMldIAqFJ50VshyzeIbmNSvJJGNr86slVj+zRGcSTD47DfR+HAVGt/UjUbRbfAQqlghEWrLXUh'
        b'E/LwFGtpInXrB0FxMBaHYOFksl60bEU4tAKK+XHTCm1D5ZuNyPA2Y4OI+8guEw9VHKvqNNa6kQpfVmKTzkQ8TFbRBdFBH8oUg9jRMhNLDLHQVxRE0XaGQIZgrx0nN7oa'
        b'PIqG4FwkQ6ryrMlXSvCibiQnUb6C6XiOu32lcMNR5fbdCtXsqIGKtdDMvahyLJOsEZ3goJx1jR2cseNxCVpkiR4WZKNFOIUtqYyFNAT269PpQ7a8DhrtAbUywcBEOtga'
        b'KlMoQQ0cIMflObIIFEzrt/eiTkFWljAB0rWwGcqjDfEop1+6ChUe6m0e9kIDhenCAxKoZAcuG6aOQc52NqQzOlQeO4N1UmMdyOJixsm15oxrByvknImAnF8HeUBNFp05'
        b'hQ7+zCMJBdbaqyWD8cwI/tzRNb5YSF22oeQklU0T4Rx2LOKXrmCNGd0EpJFYylpeNRky2aVNUJnE+aqxdqggY4TVR01SrOhTlVANF+3YYl+Dl5z8yYymC15LGAt7tfSg'
        b'KjmFGlHiw8iRW8gVech34n2Ub9ajm/whQ4f0e+42Tj+VT9S4POpEVwTSbUtvpgTOmOrG7Ph5sKjcQeQK94pNHkHtcXd21Mw1uTZrtKLANOpxp8ArZi+Uzi6/XTnH0qPA'
        b'0mvY6ZVXLcWbJ4JHi9a+mSGCaBt01XKXZcpj1gnlrmvLjBMqW/ceMX/tm5deuvX+N6NmvrjAwWvPhmDF8nUbdvodG5S2ePbaLadnvvj98uDvqsZ1VDz7m73lvJvrpg46'
        b'I3mw69NhUdfetbu44m8XFppHzrb+ULnJvDkpxL5oUZjRrp+vFLckRh3X8qi85fGt4Zbc3x0eC5sjt1vRcu7Os4FBsVOu3S26aF0wwsst+fvW+N+8A8u++mjIG7MWftAe'
        b'nfB8m/+Hf2v8webuE283VzqsKzV7/7ObZ2rfWGkx5N3PnkxLe7b673dnLv1uTeXNSR/u07Nt3Xcv9ez3m6L2JYUODu349LTB+gbf6EPaUaGZrnEL3tu4QG938cl/Lnd8'
        b'y29/2MWTv0rqy796reXulM2fG77y5MnVkS2Lkx+8ufPEvrgNCV+/lv3jsue/+dmiUrosv/z3D7c07m2Jlf1W9vE3B1+PTb1QcO9Fw02nfMN23Jz1zrHim5+/njW44ZeZ'
        b'FcYOV159yWr0W1LXDafNR867Z2pWtKXl0n3jd5vefnPEIQjzfMauuSja/ZkDMxbejHjazck6t3nU0yPftPb97Niwlck7m4a+nn/nG/Ga6a9PO+ul/HDU/4tbN4z9nS+c'
        b'iD1o8WXM6Ce+mPjj/fXbQO+7DzY74DsfvhWR+eB37+90Rxl/nmhtt3r33bqApOYfC1zyL7342A+7w794ef73s2+NFsq/Plm4eVvD668ePPrsoJ1BP/oJn9hlzbqR/czg'
        b'NTfPPKl47eu3s9+duqnkvZ8mnan5PvZNp02fnN434cltdw+8dPvwriit6Cernm/y3LHBZLq3/uuNq8zW6G6D+7cuf/2G3/dLL8/5XauxWXvYSxcU41kUgXyknAc7pJPF'
        b'TwMe1OEOksEslGItVQeoZWo7XKREU7vgIKMS2TqCElTRLQgPmNEtaAYe4PE0WWQF7OlGwSEM9iLF03CYDj0WIOGC56BdFVIWhCfIytGFZsnm4XCcRQ7A/rXxZHfUNuy2'
        b'Nw5RsmfNiZCRod4az3qotkaoh0J2OXUnuU5DdfC4M4+J4LE6q6YxnXWCsdRORRuCHYMZc8hFTuLiR3SPA3a2jgosgJLpRLvWW0GWK54zY1dTRkChHeWpy7cXBbywRRtK'
        b'JA7kcKtmwTKQCxlwllG8EBn5YheSl8kezJ7qALlkxyxkYSelAYroTtFXWxjjI8NjCXLOJHN5MR6zo3UgFYAaOKwNdZLJU6GC8XKRmtXOUQXsYJE2o5mBgrE8gqZmHh5R'
        b'QrFuoiGU7MBLShpW10cEDTZrw40J07j1tnwQXlDZK6GUnMUq+62plxROiNDAY0VOTzXzURmN9xBpsySAjfogzJVCEbQOZh0QuolIspRF3skBTssZuaCOYBwgXY9X09iw'
        b'+EQn2gXYBxBNroCxmpFJhjck2PKYM5uFRD4+Che5uAFnJ2qkjYWYxWabI14azY6LtbiXHxejt7MXhyRG8dgtaDbpEs8MFyZDKeuzUKmxJggGDmONtpdkSBieTGZ0iGV4'
        b'eQy1UkyG2t6Gim5xHYsxn0UQOZNNvZgumEKoc5D3DCDCettkmlyI17CeiJQsvMWODHvXCBdVeMsYPMTZaA5i+ywy4t52kNNJS5cujXeAa2wxmGHdSCJAY9Hj8ZycTh4n'
        b'wcNzpnMmnNOk7Cp+tD2WxE82K5FNJbiA2XBUJQwsTeWiANEij/AY78sWRkwWOIK5XWUBqwmcq+4MHsAz/YoCcFQ/mqhHJ5izaXIgkdkKu4URWcBVT9wtM3Un0tsMcssc'
        b'2EvO2YHMQZ2moA1EBuTWoI4w1kYidRVDjo+vFxnA63hVEijaQsVWvlwu4o0pKrq7KlM12x3kmCkM/p1AGMXI/yLA6p//1mmQN+6BL8mMXq+Qb72MXpOocVaX0b2YMIoh'
        b'E0qaJ+HAaboqCDULcp1epcYrCtBGQb5l5LNMxURsxP+RkugnU/KJlmHKSPdMaDgPKcGA5X5RWDbKeW/EftLgICNSNg0J0pfQtF7+1QkeKyElSNhP/kVTdyk9jYGqLJ6k'
        b'pzGj9Wh211ggHqfDkrDM6LchLAwoaosmhKBLTlOnkW/w/7XRU0cSmWrSq2gNGdEOr5SZJpyIo+6SX237tTW+Pb8bjeBAnaQQWUqX/wDuTurwFBlS7sPdnWpq4XckfYQG'
        b'zItOplSBYbGxDAe0CwsvqVQMrU1YbDd4UA4jFRnJUfLCLOOiUnsVykNKbEJDF29K9oqLDg21DI+Nj9iocFRBuaqDDVKUUdEpsdTjnxafYpkaxvkLI2Mo5WBvhuCulYiJ'
        b'YzdGsyx4Vd5klJInU3LkPkuKR2QZE6l8dHZAmrzvaunFnP5k/iljKFwqeQ8NAAizjEhRJsdv4sVqmuYVGRqqoNAu/cZJkP5R9wf9GBNnuXm6IyWenk+6MZV2ZvL6sGRN'
        b'bTtDMfosUdU2huHKooZ4wAMpgCK6dusidVrquqT4lAQG7NZniaTpyTERKbFhSTykQ8UTzzEJlJY2NCHcnnQBeS2DCklLIL9GJUc4Ktgg9BPSQTs0OUo9LqpxZwFdcT1p'
        b'IFWjHxnPkmITKPpvX2V2G4ABaBRFoS8aRX1/rvTXwgk4pLKR4w2iZlMjOe4z4VZyKu/FYx1kdGYSFKcmQe3CrokEGdtTKA0ZHnHyUlkOLXWl1DbZluiMFcNHe5qNT9yB'
        b'9YFErLrgDhWPz/dKJjrrSWjQTYAcN3/7UXgET+KRBdA+ZivUmjiLWMGMOYZrPIUyIqY4h0RqXVjvJjAdVycohunMQVTAKKVZKPn6RHIoJVKY1QYZnreOZs++aspSFiyd'
        b'p2WYvZMmFWI6NrtIlJvJlVsz549//rphlrO5x4e/Hiv+ZZile2TGlFhxsOGLDmUxZe4Hp5xMiw2LHz6ubewLVQHPTLGS56z8Xt5m/FbZ1tfPftE66/7536S5vz35r7sv'
        b'flJruXvVkCPOp191nJP95pevX51u8FOrX/YX7x7a+mTJD/KCVmvtyy+M2f3YiOPCVoWcSUi7oFbsjMdm6okeFhINBTM5bTDWJ8ZuItpIgIoLF1tns5BfqSll5WVChzsR'
        b'PB8id3ChYwpkMal38nisxd14SEmNqA42atvRICyTQoMWEc2o1BoN1aZUfMa9eIbmoajUGCIbHuQ8uqcxB7NUMeqLVtIodaxbN5hJtHMcITfSSR2lvkNcOA3LecR/FlRJ'
        b'uZC/HnNVXJLHYR+Ttca5Y0kP1YroVdgGpbpQtIlx/Ia74T4moJL5cbZ3jDucXMkDsNOJXHqwjwhsSeAyLqFizma1M+xhARx6NDWOLVMmkdj0JZHsEmZQKYJKF0TKkFLJ'
        b'g8ocPVz5moK6Ux9adD+++wjlsOh+jEaRX6voMWrZ1zGaLnxg2n84gaYONByTnC5ryfGiwQVQp4v2F8gnzZP2myyqDq/7WdbHGRoUFadC7uwOF56i5GdqFNvVyBbsMd/L'
        b'PagLBHh/B1FUeEyEcm1EbAwphVPVqjGRoimGYcR6R3aHowf97s5u6w9ZvEupqv5wZaGA9ppYQIp1q4xi1YxPiqR/IFt8n1uwCim93zo4LgzxDWU4aCkJsfFhkerWqzuk'
        b'z0IpoKYG14yeDqo4WGVKTDLHK9dUqu+D4aG1cncPDrX/q4+G/OVHvRb/1UfnLV/5l9+6YMFff3T+X310ucekv/7o5FDLfsSnR3h4Sj/RmF7RnC6FCzNRkfaWtqrpb9st'
        b'pLN7zCmLR+tb+ugvknRhUhiDje6cw38maHQZlVf5rrB5sqNzt9XCgl05XCtfTuSFm2PC/lpPzQ8O6aMKnVTWdI/h9eDLLSZyABFLJnShZNWIWGacqdpJ1BYMtnRoMw97'
        b'gBX3sEMNVuNppVxCE7mEcXgUDhosZfb9ICyfjk3Ozs5aj+MhQeJFM0ezNzHnOzmQrez8HUVsxwxBAvtEn9ETmGsG2odF2fl7S6b6kj9nijOgWYf9PQiuQYadv5cY7EQu'
        b'5ImzEx5TyLjcVwaFycw7hZe08BReFKTDRTdzvMquzsRy8rcmbEjGFgGadgkSrBTHQu1i7pw4mIalyklJEjzmJYjxArTAYWzi/qUraTOVeMU4SQsKcC95rFq0xbMLmVN+'
        b'ETmGLzPn+1o46yQ4RWzlPXF0w0YeUUDDCXK8oGgQ5ikk7E1rsXqqupIeyayKkO7Hqmg6Aq+ra7gAS1Q1bMB67q85MwareUUwH07yikAl5/42h1NetPqGkKeq/tEpChVf'
        b'Sx52TFC/MQFP81eWwlVWnVUrp6pfSQQz/koHK9bT4/DUcvlmPaXMLlWQ6olE/BjM/u4rXyE3TDIWsHS1ILUX50ihlFcwk1T/DPW2yY1EByDdbyDOeQxrUyhIGhTt1Peh'
        b'4m2QU+Iq6hulblwi6gp4CvZsJ2J0EWaTka2AI8Hklwq8RgTgPUSIroBrplpYGa5lSL75QQ4WzbY0I8KgqTGc3eYWU9MwQ1R+T8qP+VAS8oqb/5POJlp/P5g47fCkp7+O'
        b'txg3ztXW/6bDawnpr+o/9WyOR2OOuzh/0iit8TmvJ+ou8PB7UZyhNdjpOYv2pMl/fJpmPyvJ3dBOMee5mc3mHs9Z/GFVVlC5Lv+j1acXvrH846PRy81eTLm/b7xZ63Ou'
        b'cTMbOt608mt4WRqvNaH89ctVby3w9igLdT333I7SoN9f2nHSdsmOHycnRysfFEQOa/34kPbhql+NDo96W/KjeLj007s6qz/63qk258G8+NaXg1Z+E/Q39w1Rn+T8Nmb7'
        b'DudEw6i1885/3H5y/ysvfvvNK3afP3c2tWblD/F32zOufFo0+hdx14qgtHvGu0tXd5y5ozBnVjb78WY+nRmA27GImeOdIZ2bbi8FUE80s8fjXjirNsjXwCH29DRsXGXX'
        b'JeNt5uMG9lKd7VjD7PFT8JolFdzhHDQw4R1OwUUmB8+cjntY6rwWNswQZJAtYhYWYyPnVD9qSgeYZ5lKsS2SZ5kuxiv88jXICVCnrGvhUdzNJfMJhqxKqzAr2I5GjRBp'
        b'1w1aBF2iTkCGBE5yAfy6DjYq5dgsYn6oIGKhgGexGQtYfbevMYHChKkSzFxFLuWS9QcFSUzYH060szJ6TXsUWVoinXnleMiYPeUK1dH0kohnt5BL+QLu8RrHzb+HJ29Q'
        b'ZXuqMjgDsJomcWJ+GHt0EFSNVG42Es2JniBCNXlgDZxndtGN4d5KKII8SZw2KbOMhiTkqmqJV4mO2kEe0zJMJE/VED3TeB53rZyLxwayyA0EE/KISBYR6Z1m2M0trVdh'
        b'v4lyc6K4CCrJtQMCGbHLerzECl0XckWyFEvJlX0CFszFo9w/cAIPYFt3PckNz6tUpQnyfnIWBwg7limJKMwUiaV9KxKhVHWgJkbKZS1TGTQpxh8zYqq+DFg+ob5EbVLU'
        b'/CMKiK64dVD3CGLyRn81uAhLMTToKj4nRXfXP0R1G2I0Wke0JhdwPfl0cwDV42a3SObe9SClS9lL/On/Q3ogNt2WrQ3w8r8tX+seEhjo4e/u5RHEwSk1SE635QlhMXGq'
        b'REGWrXhbvzOTTpXXSG/ukdwY1h3xiQFAUWsk06VYq3gHDf9/ySSe5EQVPakKo01Xx0RKx95IaqQ1dK6EfHpk5EiJiYmBxIiykMmmbdEVzUfpigynAvZucusS47/C1o/t'
        b'gsMXyWKgFU93C6k1UP1U2ordOckoJhXHozoiUyFS8c8Ul0qPfNHPFJ+KolPxv3d+NqEAkJFm7LN55GDNZ4vIIeTzUPZ5WOTwyBGRI4/IKdtZrna0GDkqcnS2LgWgrNCp'
        b'ECPlFQYVuhWm9CtyTLFOpEsuxbvSJlrruMjxDL9Jh7GETcwWIm0iFZQFjT5XIa+QREvIU2bkn0mFaQz/zZSUZlqhV6EfLYu0jbQj5U2iWFq0xFy9XMNc01zzaF2GQEVL'
        b'1mNRrNosqnVQtHakU6Rzti4FvJQJK+UstW3ybVO6CtwZNwJDLouOSro/qZvs2PsGFclX15vuOxJB1DVGGe+qTI5kPyc5O0+a5ErlWdctykhXujIcnZ1dyD8iKU9WSG/L'
        b'/AMC/W7LPL0Wed6WhQQuWkyUfskCD/Jdj75ybYC/7wqyhVGV/7YW0x9v63EqixjyUSuaaMHKP/NaF/paWVIiXU5J9JuSLlCZl38QD7L9k2XNJPtV97KStrICgxYsnXd/'
        b'/vrk5ARXJ6fU1FRHZcwWByrZJ9GsUIcIVc6dY0T8JqfIKKceNXQk8r/zJEfyPoWks3zymcJoJS1iqcG39XwD3Of5riUC//0JtNLu871YDcnPxWFpdD8LpAZfZTIp1NF5'
        b'CvlOtrZEnlY8lRdHEw1vGwR5+S/y9Vg7f16wu+cjFuVCNt/Ebk2+P73Hg+5J8UrlfKaJdC/DN36dn3IdK8mFliTpLInULJ2WZdyjP+4P779R9wf32XkKebdS6HTrXWyP'
        b'P8zsp6yef57J/jxwrfq/5nLf7k90z22dyKjosJTYZDZmbAL8dxIS+krr4BqZlyULvxNxX8wmAc8vg6aYkkteIsv2WK31sk8YT7qR2VSjqHju+QGyPW7rUs7RZDLx+89o'
        b'ol+LOCJp9w3HUf3so2cOlJJGuZFPSqu+ZYF04alu2QMDvVWhw8/uxX0c4IGaU5xO5S8oLlmwf7d8A31171JYKpZvIKiZMjlIWbS+JpdAv99cArUXMFOnDwumF0/Ujdka'
        b'1cWOyQlvuFOJbtoD2C2D1LS0lgmMloAJMErX3jc6WPZYWJY2ZMce+Da6mB56x0xLG1tlDPVQbZ7uOM32EYrk69PSxt3z4TerVi292d7yYe/pf2Vb2ngF/6knXAZ44lF3'
        b'AVpEz0r3ZyJWmbm4PYjnUKuojtRg+/09Sc9X/ljPaZOQFBOfFJOcxsFxbWzpqU0ppOi5bdu31dCWnub0Hnq22lITsS09FG0Vjp1O1GmOkxydXVW39F1Mp7/Vmd2qKrXz'
        b'z9PYn3nR/TWMYzqomtYHXgPvn4lKBtnQb/cwp4Rr9yR8tsj6Rl9QJdH3W6dOmAVXDYlqbxwFimmgcbn34VGn/5FrjPGOWu2ZtZS5+6PCkumEUqrZwLqAUlCHcz+Z/NTi'
        b'SspJDUtSRQd0IWtgvWMZFBVF25oS24VgrM+i3OcFeywKCFyxljLgBAR5rKUUKEGslhrPPKc967eT+CbE+4fRFKnwTdTjplbcVLbivh3ZnfZj5pPgJXSad2177Cm2/YYC'
        b'sBFK4OtUyUnTemwxtrx16lti4vqGGeCAFUSCVXPCrg+Ls/QICezHDh5nGZQak7w1KimWDVzyAJXnG2I/a4ksGK/ksNg09mD/O5xt/3NWhbTBB6QTgIPOfNWQaMA4uEuq'
        b'nxYl88iGLujZ3Z7tBqPS767FSurlIyDdo5KYlOrp26PcvsdExSPY+V7G3xgeFRsft46WNIAtncojer3EJ2N/Zl8W4Yob7vXBkqAYLJMKEqwSbXSghJlURWyBAz5YCIUu'
        b'aoBLIyiBBh7JwAzXRVgOl33jOLYnA/acCHuYaiyH49pENcYGZQIUYQv5aoJ8mWCI2RIsdNjE8rhg/3g479M1SWupOu1Fild74WCqTXbeEmEqZBlh9nIPhYQH07eNxUpm'
        b'+4XGeUQYpLbfKbiHJ/01p+ApuWES7N9kLDCTcTLuY1kqWAC7MacL2GlnTTQZKwmGhoEU69TGwT/ExgYLsMhpciwW2FN4Sw7d6UANbPvNxLhpC3lOXLVPilaACpRTjch5'
        b'jjkuXJN1FnwlHcpSA/XSVvN8rRg4RDMaOrNwPB29/TB/XDBps1Mg5vku8ZQGkjvoVyucSRsvQIdMjgfwslfMolo3UUkNMotLnhlf7KMPc00W1Gzb88u4FfK463sev+lX'
        b'VZb+7LgXdG9aVswqLVs1duLlRdMN/zk4xG3o0OyDQyTWcPNU+qLWrYEffHdHfjP1bvlzjjkNb1eOOR3s/eo7U7xmBn72WkzCR5dyOv710q3vxy14Nbpto6nJg7gpv48b'
        b'9OHXu6bbxP/Lp2LDme9bRz2xafzj8xZ+OeSf955Z+evhtuoPks88Jw8vmbCmQ7HR6ftjfygMmX1xtR1ct3PEbDjvwGEFT0ucoRmPsNDwjVBpxnGDGWwhjcPQEYwCpVgc'
        b'7QJnApkZ1dLdnhpup2l1CaiA/BE8zPr4yIWqSJBU2NslVh0bY3mAdC22k27bjZc7g0Hq8CSzCY8KWNU5D1lwNrRicyxkLeYIjbWQOUEdWoGHsL0LiqOVMUdVuQEn8VR3'
        b'ay2cJdPYcoEzHuWBvzVQiyWd8H0Uuw/OLe0G33dqF2uMdTRmc4BFRye42gVg0QfyeABv+XQ4xgzrWYZYpIZ+xHSRm90vwG6gMRxk3cEFIAuD3OEnLlwIjdxgW4jNj82j'
        b'ITMlvqQnwkUXd2zrlumv/2/Z3TQIca796VDbTUV9VRAqBfCQMRutjP2jnL5GEok4vB+NR4WK5t870HNg5WeACJG/AOjmN6Di1jz6oYrbnwR301pLhdsB8KeKyScO7dbX'
        b'6zSMxI6PIED3hmWjtrAgz3mBt2WUcfS2jJKPqlXO7uG1PHiVxrLe1lExVidViD3y243Vx5GnoMlv5xqngUrnNOTQ2LnG0caPkMUuZZZC2Ydn+9I850VGKrszK6tP3j7M'
        b'hhqZrbcCG23pSiVK11ANokhoH45+e5UEpEG5oqGTvSNNe7IHcopcqsx3yrXJtPeSVVL/I+lTKklYwyP7MJWKE07xZ/ugew1TWkbHxodR+4Il4zZVUTn2F2UTFteNSK0n'
        b'S2x/teimZ/RF45octYUL0cka9tNNPOyznzhOck9MJJUAO7uik4qOt8HShnGh06YxCc8qcKGjo6OVoh/ZlMdKsJjkMDqbujAfa0rmpI9cZu683md5mmc6ORxVU0AVx9Wd'
        b'0bHPMmwCPRZ6UC+Px1r/EL/5HoH2lmpVhpNe9hv7xYKQ+yc9jU/gQdkDlLClL+2wH4bRAYqj/2mUR9rDA+l2GuQ11azuszQ1dXVfaqAl6RWPQP95vr1Vvr7jlh9RDVST'
        b'WvGu0JD/0gmrmjd0XRDNOYoxO4eG+sfH0Z1igIDuLcmdb2cksbSPwmJpEDXdIDRTNzopfhPpqsiwfiKvY1O4tW1dzOaoOPXMJ0szksb82ETExyljSHfRkkjHxbC/kl7u'
        b't2K8mK42CkXXZqqokMM3REUk8/2gb60oKGDGNGcXS07WyttD62CvQuRUtZcZDejaJJtin+VEpySxtcZWO6dd7Vc15CeRq2WQShVTU6LT2PQ08pbYWLL4wpK4QsZv7ntv'
        b'USrjI2LYIGgUw4SkeMpsTnuRdK1qsMlC4NO+787sQi5o6U9UxLCEhNiYCBaNSHV0tp66xtr3vXbcVczqnfSl9JC2tCHfFfaW9Ki2tAkICVTQwaBHtqXNfA//ftahbZfk'
        b'gWkK20dIadCEds3TbPU92IUGChnV6Ke6feqnY/yZDroGTtqogumhBSq5DroXDjLhhylV4cO1TX4VmVIVaxC0kyumOxyplD69i16KDVC7kCmEsZOxQ5mGbZoQqSKoSWVq'
        b'5HRLqCdqas5UhtTCYVryoCSYwQ/Q6B+4QL29VJ9dgY3dVdrI8BRKAor1uJ/I24UqCgRKkRGsAhnwcbBd6mnvHdIHw4NKs7XD3RzOpd5jEBSOTmZNsTWF89g0aSULbGKa'
        b'LR7BEyysaa4BRb8Y8FWRO3u+jOFeMBaZJTYa7AmFtuDqbE76KA/buVtlbZAc0v1ppBXTmbHq8RTKDIZnfbDNh2H0OGAxHvMOoJozL0gL92CO/vhhcE6/U1+dixmkvnvw'
        b'lCnkwOlgOBG5BPLn7yRKbyacJ19V5OfujVugDKrnh6+BgvlJMUuWbFiTNH4VHNy43kTAEreRcAQal3Bom2NwfSlRfol2diXBQCJI8JrohDfwEgPBGLbGWFW13tXC/GFY'
        b'+zjkz4XycDKUXauUg6ewgn6moWChxphrKUDdkkFDIR2LuAnhiBU0y7WgnsajsWg0qJqSEs4MD8tCfXz9feCAiiRjqQqVJyElJRjLEgyNcU+wquO7mBeoVYGOjxqlQw1b'
        b'QxOFddlLjDDPAi+MhDpG5UFUy/S1asQkY2mfmEn0ueBuI4rNkGu4CMtHp1AGGixNwBM+q+FaV0qhYqhbzCYOKdeHgYaQ2bRXS+kNBaZkdhfg3kCikxeI2JFouIjM6yo2'
        b'yfWgBjJ9epbjyTVaqs4u7VYc5Mihwnw8Vg+GmslwDc5YDJYKcNBvEJwZAmdZAzGL6OXXOdwRaxZkbFG3TIInsYIGG80mQ5SJ2aR/WWQe7AkXMDfQIHDDopQAUsbMHXCt'
        b'izHH10vh7eCoIgfpjp+kqpchbTjsx8zOVUM67WiKKZTj7kC2wrDSiixzFbTDEs8/XXqXkietFwK9zeEa1m5l63psLNbCfjjW1VIUsY1F96RY0lcfjZ6qYa2hjDUxcF5D'
        b'WoMnx1Bmw5jnngkRlWeIevXaiPl+S67HvTHX5P1R267/eHTH/lV7rDNsPLxHZ0701HKb6GGdfe21jK/NFW8ZTjztVbtN1h5w09rS1vZJ6enZ3+rajP/g7kzT4nU3jg97'
        b'+dbzCwKXjNiw/1RZ5dTv2k1SAuoOan9pvjiwpm7GL97ral//bo7V2eqJ9Trvjd/zVkHQ8e2W6w5vnLa67ca/Dk1e9OKFiVfGJhlN++n23irHytMva/8Q014vi7j6r+ej'
        b'Xsya/g0Wf6J3/zOf5lfXTrmUWfP5tyNuG6+Pitz0q8+lnZPOzmrfOcJt8OyAf/2Wsc7CbfdnjjF/SMbIru0ctSO35Epb6/faH2hd9vh+wg/J5+/4/L3q2/qXZ0X96z3p'
        b'/rpVGdd+nGC5/8nZd/O/Hr5q8KmAV2sWHv+4MeC5pz85mWs85OJ1afh7bt/vPZGruL267p2nvpKlTPe/Z3jxkxnvGfyW+uTMn4//fW3Rez89H3Er80rWZtcNabueWJe1'
        b'+49x1S+8pej4+tJh94wrJ3eO3TLzoLdjzvLjhleawq+tHlVcWb/Y68XBE05/+uK9HKl15a37H4v10p+83s5/OXH8hvdzDZeFvJv28najlpWV798IeuqZXRbujT+vv6Kw'
        b'4GF9uTvgck9zUzpUx0KtNbth3lCKm9otqUkyHOtw3w4sZ/lB3ngE9mDrok5D1o1ZvOg90/BCl3hM+UoJOa2q8CJWLOd2o/ZhlFvpIrSwmEyV3Wg0ZDIj1pZomh6U2klD'
        b'AtU7VEwkk6GWm5aOyozUbCcq/IR4ckCdscMDrIipeAAru2QhwUm4ojaVxfKQ0cUy3K2JvxR0sU6kdrzH8BSPsNy9Fqrs5Ks4P4YqtJOcvNyGV2SDhylQrRfUyZzGC9qx'
        b'EisomMI6Bc4ECmMwQ0UgsoacC0eW8k65Js7uZZgzw9IFWJDI0532wA1Jd7ucjntXsxxUQgFrvWwK2fhUW70qKx5PQ9ZgKPdmQZIbPLHDZ1wClthTSjaZvQhtUDeJMWZg'
        b'OVTAKZVRj7zKeLnappcKbcwqt2YsZNo5UtPoTituHE3BFmY5jLCAfT6+XpDvpIDjK3tAFjnDVW0nbFeNTwyZGuVs8pADJoAIE0YLpI9jrts0rOAToELurEo6I2duNk87'
        b'w3Lk4BrjKe4RFDr5OSjItgsVgrabxBLqdil0Hzml2fi/E8oXroZxzOvPpLhLeExfNJCwrHWJgUhz3E0k2lJd0dSE55rT/HVKTKH+pMsCQLVVOekm0qGSoeQn/WfBMtwp'
        b'TYW5qKtlRPPSJMxgKTESTVnpNBtdW7LVqg9TW49U6z7slP1ZzJL2d48kffRO75pHvr+PZPI+8sjLqAFzXH8GzHThO5uuJsxHaGjfgT+UjY5Z9ngkiRCtrQkBkg4INb9e'
        b'Ibsf2ktrCIyKIwqr8mHmO2YrUOknVDsNU1ou9/MdQAmhJEujeykh9v4pc+maOTF4kA/ZDqCsk5ixB5Rc4TKbXkmjZCVeMByMR2NZ1i80pcJ+OyKqX+p6qGtOdLigEjZX'
        b'hkJOp0zgjs1YGu/K0aiuO+NReinZEQucHDeP9iY/vCloyLg1WtPhMJZxp1wJXvKixZMSRgtwZAZZ5/u4+DwayjCXufvUzj6o0LNxgA4OJzhNIqTPobbZUPtIg00C04lC'
        b'R8JhBiVJ/YHHiH4Dh6FDXJNCO2wGXh/EwR8nzBacMH0bUx0iNoyR6xE5RsRzwkZronnt565GIvrsN7FT2JI9X5ZG8WCbiWrQMpY7zRqdsc6HnhpwKM5fS9C2kBgsG836'
        b'YxC2TwkiW1oTFstoxo4ApWY72JXUua4c6I2hvJlOoifkAv6qamxZIlcrL0QVbJgDu6GeZ6Tk6turk05YxgkcweNjQ5Fjtm2D40QiVOWr0GQVInq2usFFkafW5MExPC9n'
        b'vIfkrV4mtnhgDu/0C0YbVcknVEcjIzAHa+OZJ3QhXGIIclgRQuTaSm+sDPETBd0AES/jNTzLur5Mq0TInuAmEZxDjY5HxXPN9o/5VsIrY+h+F2oVFejK//i9tadgMmos'
        b'g2d8kGwgdGMm1qw6KkAyZmILss6EE8J2MVKIFHMkw4STao7idUSA/IIqBjSRdV5kkm9MXJSapVgWS3/pDaVLvq3W1lAVM5hzzNqGxSwGmrkt7fVUEu9yqQPuYXkUYuC0'
        b'mdiK+ZA/E3M2z10YneiVtDMOMkYJ2yeZQKNyGGuX6RhD4QlfFyIdhBpEhSbyxi4LsxDWT11OdfuRO1NTOMgslJKpXsmBADtBAOdjO8MB3AVZnBkR64PlnUqiLl50Imdx'
        b'Pdfn6qHZjlxMNCQCkLkYLpkFFd78hU7awgJjZkywnzhuo6CQsAeSoCFVM50gd9ocIkDtZ1eisUCQq9VCOAA1ROrYxnPLLjv5YBN5SkeQThCNoMltxFiFyC6ZjZij9KeC'
        b'n0Qu4gXYYwk3Fv9b45h0iIenHhY1TNNJR8Q+0ZDJtwtdhpDVtGQZnpBvxivGEtoK2eIZM4azxhngbrmcSKb1VCshSwwOEp2ZL7DdLkSKbDLAKzpk8e0VzKZjXShUsF0B'
        b'W+DQY7QKS6BhkrDEO4Q/kWsPh+U2tnbYOAIoDJCut2TllsVs0YXHEBW+yckbW5zMyBUtyBJxH5ZBU0zYlGypcglpQ6x9aFSIj9I8xPxGy/F7z9+aO9/SxHS0S3aecVFe'
        b'5qnwBU8uM5/y2J68reNun/M2drO3+WqaR9T2y/uW/pBZ6bHivT8EO/mQiytWOK76ecSqx/d5tCZ8kur/U7bMIvX+kX/+ev/dO58lTkw0ra9p/8auIDmg/osn5cnR5ZVf'
        b'La+8YtheOqvBoQqbPrrzj08bit9c3Og3OsJuTVFehtmeRDAOa/37qu8inF4N/uKLtwPsT7x9b2NU8vc7Ar/+KGjq3/5RamNjW226bFmuWWVIQ23r81oR0y5Wvx9yzeV8'
        b'YOq3H1yN3rDCYVnie1uqd6566v1K17KFLy0Z/vR0w9Ab56Klea8/ueHgyldemlq3KXjvZ5u/fuzAl2e9fghOvf3Gs82vGlZ+mfBPb9OvTQwP3G+4/YS/cGee3+smt/xS'
        b'Ul+yiW5T/nZm8W+GTyWcWyO9snel3ZW3be+M37ntKdj5t7PFv198/cqkl4oD5Y6/Dbs9qO691IbPJ26Y1+F/R3l0400dj19nJW9b7pN1q2LWA62nzs4OudJSNOX57Xef'
        b'GDHZtrnt+bfPDTa8OWbR0h+jfo3JG3zuzWF3vs6ak55iMmhC5q+R/8wPndQMH6SP/sgz8JP8UG/7ylGOswMvfyzfmH3vyUNOWkctfKJ+GjJ6Ch6eMuyANcwWotfdFLY1'
        b'vL03xPCt3+9Xtp2OGVK8fc2gT0+ueGNWqlJ+O7exJNzN6tathf51/5r2yqKM0dKnn3+moWTE0duDdn3w8fIA83++Enc76Ovi2LePjp8XMDd35cc/TamYKK/7R8iPkR+s'
        b'/cRxW8HLcz1uNL/xt7sXv/P/sDTUf1PwmyWBJW///nSe37ZBDhEpyXuffvKiVoD1/FG/zym7vWxUkPsHjxc+eOrFJ11e/PvBY9WJ+fd0tsmXvltw57xfYGLhjoP7rwwr'
        b'u7vLojDgj5EHVjz35b2Gl077P/Ph3o9G+s/Q/ofWzky3F6b9eCXnl5uhBb+suNW0/PN7xX9sPv1d6v07+fte+cD/M6ufftoX937LRxnXn57281eXO77+bMmTV9MCWm4/'
        b'e8jsfdtfHr/02XvDSx6En8pUzvjW5+YL320rMtq+zuvToy8dD9y16Mtd+l/bPXH45vlzI6alX3v6+os3gmuH3Tr5WtwWo8+/em3M1XVtrx8wn/7RO3NW2CxObVHu/ur9'
        b'n15QXluy8PDHXuWfjTv1nuPEpww7BscWOByrgDuTFHFXHT+f8vhsRU5LVOCqg9et4d2piqeOfXL66odzJil00gKz35mt+OzXvVa3fN85H7vW83rC8FuHR6xVnvzH+xJc'
        b'PeXlwaEdv91t8bP74WfHl9+/uXXIV251Wq37J/zjPYs/ZpWZXXsw7BWPQ/Y1Cc9dfnvSJufpf++Iv/11zZrcdZ+c2uL6zIU6F8X+v3325idrPx0c973xszovr/5pkGvG'
        b'P8zHTNxc/6z0gzvvJ4Td2/HN/h/PbIu7NOwf8Ufu6cQPu/5F7san593d3tpY+nzH698t/STvlPvniXNc/YLOfXDwDP5+cFHL/Vczz84Rg94tPP6dYfaW6lL8yODt3466'
        b'Fe5qtVo5/uLNB1VLq/dotbrW177wQLq4bVF+o5FiIwPEIPJYjXdXMpNOIpMQPI/1ck7aGL0EC1QqaxhoIAnxAJSzy07bQ+zsZmlUO7ViNwYqeWjKBTgK533IWahwhKoR'
        b'qjuMnaXrJtgxpc3BHwrVGupCqOpka4wcwxACh66G/O76aad2usIam8YTcYZpurVBflAYSvkENfSznH1y/CSuvTcx0BGOVQh19qLAsQqvQQe7PnkCtCp5MhOeXcazmQyx'
        b'QzrXbAqDfoMr0AjZSkfyeockfwU97JtYuA62BGG+VJiC57WDVizk+GvtcAwyuLYM+9eTkrTXSmzHQzrDZXGDVjjk42tLVPXVovP46RuQJ1guJH8/RgbDyctQgkW0fqWS'
        b'8ZCfyjuyAy9DA8d0IwJFiQbU7QCWcCV7HzlPj8kxzwEbscgLL/lIBR28LAnA87Cbs3yeJmd3nfqOwVBIDmly5hhCHhETSMe1Mj3eczTpJ4Yky2Bk6wbBOch2Z82yxJO7'
        b'+OMORIxu8CJV0Jcsw8uTWBRTrLat0tYLSxJY9mmpv45gAg1SalZPxnNEcqeFD9kCR3287b2gdhmWCIIWXpdIN/ix/leS07YGm3yMluOlADmcs9EW9LBFAmeGrOH0ooeg'
        b'0kXpaItHFVigR0ZJS9DHEgmZxR2wn5UwAU6No9XTU8xNxAYsIh1gCNekZgl4WZWJ2gDtdl2MK7sDMct0Be+9WgWcowNq56jQt7GlJgzTodJR5KRPt4rg1oPdeAxa5I4+'
        b'eEXhQpQZ0ngjyeNwMZoDDqanQIcS05P8RS4vnCWC+HnWLxGkkMvYRHqGdjsDsdQSBllIoTYNDio28yirPDiu48O4PNVEnqlThRGQKYNqO302O3xH6CsdvaDeAEo3kHsE'
        b'wUhbOgfqVYiV7bBvjdzbwTcRLniSGapUiBQhSRgWLFtElmAGh905QzSBCiXpyHIFreUNAVrN8SqfsRceN/dhsNURkM/gFI2gQjp7qS1fOzXb53IsxsoRXbEYXeEgb/0p'
        b'r0Sll62CCFFQIRqQpVK8Encz09SQHZOxCTJFLNQSRDnLQN7O3jgBywJ9fLEywb8bmqlbOCsxiqwKDtFIARqx2A1OuWAOh2g8ZDyELC0XbO9qixoMOZtYP0kk2nIbrNQl'
        b'vZDoS2qkj4ck0O5my5tZCMXbaUv8yBS94CAKei4SsoL2T2Id5DJ4ktxRYUuGqXY8ra9ujCQGMk3YW4m+k2lHBsbRa+ZwjoNsDMXScGfkEKRDpsjkNo6J0I6t/lSMqxHx'
        b'OJzhIKB4YfVkuYK8sIkspXRasBYeELGZvDiHT63DWC7x6bSckbV4GNpWw15e55NDYI/SkTVUivmigHlQRdboft4blyATj5CObBrL7PLagtxbgjVDVVS0mOOMlXRokrAm'
        b'2NffkSx3J6nuKjzOmUqOQs0QbEq08KXz4SrFw78ax3oxkdTgKlEvkmj8nARuiHgVa0dsjuHToRFrNqtS25kZlaj7GUQ5zsULbINbYzBZI+RDrZMlXnbj6ed5oZDOrb+n'
        b'FnUBg7UKY3XVGoTXlV5kjh4n1fV1EgX9uRI4J+BRtoweM1qrXLqagqTyZUrmId29zMnei/tXzGLLSKJjp8QShT5ctMcr1FxxyVfE3JXCMBOZ7bpY1jARWtaTAug1vDiH'
        b'itxLRSxQDmEVj4H9hhoj6iyZUyieYqO7eutk6qDZbIpnsYkM0SBxDZ4AnqlvEz1OycDjRTgmzMGTWJoGbXxoLpIVR6V7zLchKwOPiRsmk3OhmWxHLOW8wsWa1NbGOxVa'
        b'jGwlgg7slcz0hMusJSI2xtPI2ABqZ7msS48sMjeMJdJIMvIlrLts8Cget7MxgmyHLkDicG4d3+yPjYQTSnZOkc2Ub4eGuE8YCudlLlgNJ1gdfODkdL6je2At0z8Ok4kb'
        b'MZpvSo3L8BDtbCicTbct0plkNTWT2UC6IYc13gz3SOnpTEMpl4rhmO1Aeo/tSIP18bwSDo4jw6yH+ankBzaSu8xwrxSOB8EZ9rjXCj0GTE7X+FJogiqyybazHldg/mBm'
        b'jNWB42QRU1ssnsFSNkrJMZPlKYZ6pEvHimHO88jedyiZY3EUQq0Si6hjwFz0XGU9HApVu6sunOazxssI8hPZLYZ4TjoejpJlNJrrxXQZqYDbsWh5J257AZ5OpshdpJ3t'
        b'FMkggPIgFPjZK7z8yHZNDTc2UEL2qRmzteEU5MSwwRmSmKayRGMH5qut0W6eDsk0bX10CNkJqKusO246A5StojivalDZELyo67QM9/F95OK8OXJ2p0Mi22wHkcU5Cm9A'
        b'1c457IZtZNI3ktdSJwhUGXdhpm7hq9qf3FxMlma9lUK1wjwkUDt8M9tydfEQXCEzhu3i+0TpYihxAM6XvgzO4EV6KQmIEMK3kalSPSJwXOey0T48HdATFZeM5xkNMm40'
        b'6d4mto7xOJbhSXU72OsG4RXp4l1kiMogn93jCqVQYqc6CbsBz1tP0pvszs+cerg6Uc5OQim2iAvIsXZWL54vvCxSvBwLmJxDtuR2ipssSJaMmsgXXg5dU2Sn9xbJo5dF'
        b'TyM4RjrmDIdt2J+Ke5W4F+tJ1fTJOdHEBAlzyJYSybE1jc00bLKCdnlktIIs1OFkj8VMOM6mkTVlNlH6Y6MTESLYjm2yQUoEsD1QsAQusHpvnz8Hm+wdHemOcJBsPUvg'
        b'1Ba4xi65k/23VU7Xg0QhkhpVjIaLUM+WM2ldi7vS14t0mp6qYT5Sd2wUhmKZzHUWXOT7eUckXpM7OCpMfUjbtEdLzKByIZ87h2yxnjHf+DtgFhTY0ulNlvI+yHHlB8X1'
        b'KGhUOtlig+cyPwXdja5JPMk6V8Eil0O1FjY5+GML5oXTjWKHiJVQDns4/B60zcHCrVjXHe2YQh1D6SZWwkiohSqlIx71805RkB2BSG8SCVTA8TFM/pLhxWEqedoLK/CC'
        b'sQ3d7wyxVTpTOpntCGI4lPCwblVIt8HyhR5Yxdt9Hq7geR9HP7Jxp4mwe/vsTeQooiM1igjbmlBvV6h3WUn6mrbXVwkZHOtkFeY6SFRYJ1jvqRj038G71X7IdY5uwbNx'
        b'tZOYrZ85fXSpdaxvp88uwVaXwQxz0GJ90ZRheFAkD3MOKCihaCD8Hl2GAqJL7jMXzSXDxaGihcRCHKkzXLSSmKj4yg1EI3GcZJw4nHyy1KKAxEYScwn9OU4yV2YijhaH'
        b'yowY2DErm7qWRBNxuHQk+W5B/jZaMlxiymphYTCUvIEikdhL+yrXhDwzlD3PgY/1JRYSfbJrD5epUUo4b7ol+T6BlDBSnKCtK24d1ocvhvdVf/yqD+/2Tt/QUdLVI6mF'
        b'kDoe+/ENpQufWnT1DvVfI/Jqlj9fJtKkY39/hYx8YwHhCoMe4CVJqwWWgx3k7unh5xHE4EpYjjRHL1msgRyhNUyixDy8teb/N0BFSBdN03RRHJ2N1H0WTU8MmUymwqmW'
        b'/js/daUmJnSKCqL5bA46QqeONvl99C5BL4X6qdPcB8k3G5INp7GntZ2s3dkrtbEgFiu7pc3rq34q9QcGHZFG6qo+63X5rE8+yyMN2GdD8tlI9XfjLp9VACRH9DTgIuaR'
        b'g7uAi0i7gItYFOtETtCAi4yIHKkBF6GAJELkmEjLPwEuMrZYO3KiBlrEMFor0irSuk9QEQpj0hVUJFthc9uYQeswTukFUeExyfedeiGKdLn6b8CJzOBp6JMUktsy94BA'
        b'j9vS+ZPmk+mUzO3zFORCBSGStJlO7FT6bYv46GAfM3hy5aQ/hRCiemjGn0cBUb+O5XK6qFBAOpE/pKxFSTsZslCgh19AsAcDARnXA4AjaMGCwKjE7onkzirsj0e62UWD'
        b'j6Gu0f2h/ZWrgcjoXnmFXrcy6Cj1LtS4Z4/1XdYAL+/viktSCdvJ/rvIGb3pabV4aC1UQz6c55h+gsySQwvWYCFz/RBV10G+OZHiauTh6RkCHonEGzFPXzopU1JJLO6N'
        b'I1+FPhvuGXYr2vYjn7AdOfrRnwvfZQ6b8bgwM1/2SuBWhcikzASoi1UZmzADC3g0zwQ41w9XZ6k6yIMlVvV33tMvS3pmbh3aY5n+RRAOUx0KyzTQcUe//tUNjKPfVz8a'
        b'EscpisRBoy/+a0gcNB9qrPajInFEspZQqAEay/+fhOFQr6yHwHCoV9ND75jxyDAc3RdofzAc/S3bAXAx+lzMfd//J2AwemZt8QSDsDiaG0CTr/pJJdI81hegai/ojG7j'
        b'rILLoKcSh8AgJ5Nt/1k/D8OpUNfkzyBVxET/D6Ti/x+QCvWK6wOjgf73KFAR3RftI0JF9LmA/wcU8SeBIuh/vRNxtPyDGWvzzE2JvVEKKEYB7MZ9uAeLfVWku53Rx9CB'
        b'uXI8s8wn5le7LFFJw4XWTfeh1OGf/3199Mon3r75xs13br51892br918/2Zb2dHysTmNWdbHzmUpClvfPpE9PufcwcZ8l5yxv2UfyJg8SshoM5wCpxRaar6zth12jlCA'
        b'DZ1oAlYWzHQ2Amq8umMJ1ISo4ARcoIDb7yVSyOuMCo5XqF2umzCDGU088boZFo/tTJFfjc3cdteEl6K68SxA6WIe4AxXIUMd7vnvBLtq8ucnPEwOWsjz6LX7Ekj+30iU'
        b'H/pIwtWXowcWrh41Wz6bZcsn7RE7xbw+cuXnkzrxXPleb9Ikylv1c1z2kRyvPXBYb4ROl8UlVy+wuVTA0+kh4smpkBctV4l4OkzE0yUing4T8XSZiKezU7cL2NqOvkS8'
        b'gVPeu+q1/1/ku3cHEFPJTaok8E3kpKHZuP9Lgf9fCrzl/1Lg/5cC//AUePt+patYsvd3JUX7UxnxA2wZ/zcz4v9redzSPsVHUx78vwPrIF2VyC2EQinL467S41BilAUU'
        b'Koyn8WiKIE/MD1AjgXl600gvLPVZRlG4dFnkPewZswkK9aANi+Ecy5VcnwaV6szsLmnZcNZZgoXeWJmiEhiroJqmhGN7kCorHOoWpFDfA9bAyZ1qx7fdEovQfrDAJALs'
        b'xeN6eM1hVooDeS4Zy+1pul2WiiFrCeZ52vN8EMzzI3IyiyJaO1F3Hpb5syfg1OoVPmrZeQkedOKiM82htccSP8q3JQiBch3S7JyxLDd2dfQwRvFKywrHGyGLlzksXeZJ'
        b'xE9vP184F+wJFzz9HB28/EgZRBS9JJ8EhYFBwmg4YhRL+uIST1zYNz+SEYxcwfOcogNPLGYthzZHLU3xvGw4BzdoYmvCpCSazcrSy2Vk0Ap1oBJqsC2F+m2m43WtIHo3'
        b'vZPcVU7aQccrmD+lafvj0TpwBhsgl+WG4OGdQfIkI7gskK6UDhLdghx4/kexqwGRq1tSJ0ORkmamdIh20l0sJN9ju0zQFZ5dozU31OCNuWOFmJfvPSEqXyVXQv75t5DS'
        b'RkNwNvF4efPXT3pZrvauDi2ZYj838VTCuOwjFf7u9TMOVUVlRhpP8Cq2OZjRlJe9/u6Nf/7+YHzQQr2bNu2H0kPuLv/gI4u9CzKS9knLDr1h8N6NgMXFH9k6670y/IPF'
        b'Hwkp57fjkwvmP//FPNmro37Z87SPyUs/m0xMrX6pYdb3w6LXTltx9/q9O5es68P8zHUv/OAT/MfNVlPlS25vL/tt+2er//HepaQvhnz6ydqXn56TqEz7cHPZaaf4uri2'
        b'D/ac2F4R5FHwYONzi71dn53plu62Q8hs8I4HX4UJc1MPwdqZlO14N17tmiIai61YyVm0y/HEiC4JolCP+9RgZ3vwMlNfgvEsHKP5oVGYw1JEl8MRVroIpXBWk8EZAMfV'
        b'JNhwTZdHAV5Nwo7ePHJpeEB3wzCmOqXhftivmTSROiraYazEOk4VcQQq8RDTnCB9AlOesHgCe3QJ7IYGTYIqXMR2Vchb9AIWj7sR6jx6heNamrCAXKyHcsjjcZCteApv'
        b'sFZ4babhJ5hPtDQjbJf62qbycLJr0ATVlPwYikUaXEPZj6ENynkUYCk0wmGfSd4SbKX4ffUCtsTAUa5Y5iVAGzVa68IeTQZqaDJz4G/CQzF23n58cyAartlEwU2Kh2Px'
        b'OGv4SLiexDM4hXA8xjTSENjDUjiX4ik4p8rhZD67MMjukcMJNSt7a1zy/2DqpPfDtMkElkAp1WV0vbra2gyRzVxF96vPaIJpcqWRhF7fOqan7tR35qPeo2Q+duqcWv37'
        b'YHX6Z8vtI8HR45EUz+uWXRXPhzXpP5zjuE4hu7/6oTmOfelrfzrBkaJ+905wtOYJjlgFtfN8Okkw+0xv1MdLfWc4bghi3mlsx1rMopAFgzGDJzhCgxDu7iaVC1ZYJ8Xs'
        b'QZjHPU95cVDMcxwhCy5y7INZcIwfBWVD8CxPX8Tz9jSDsSwUjrOjYM0kqaBrS4k0QmOjZ67mCYpwFc6ZsQxFqSnPUYSOaCxnx82cEVDFExTJe04LTvG4j/3dy3eQj0xJ'
        b'AxPIaQv5cBmPs3cbYB2W0BRFzHRiWYqYMROLebUqffESy1Bk6YnQOE1ioBzO8qemQvFyaJMHdSYoTtPiuZOz8RDLUISTJjxJEeuGQzk/kXdjPQVITcDciSyZ0DYKT/L8'
        b'tn14GvPUCYPqbEEsgrM0Y7AeGnlfmJQIb+u40oxB/6OPreD5clo6VsIWE5YxGL5l5zT+x6q5XsKR8LE0Y9D71kqffy9j8M9lmrXpdGaaeQksfv8wZqoYU+zJPpro5YcF'
        b'9liuIlzCPdBEoVBoQKACrkgnTaLx+TfgNOzBJqWcdKA75hkHL53KGiZaGAgHhk2mKYOxEaHDeGuXxlgIM0xXsJRB+w3kvfS4MNsUj01ajt0zBlm6INYMY8ObhO3QzFIC'
        b'fa1ZUuAssiaushKnKLWFxTNGMNTWesetpKmMfW3uvAAe37telMhFSyXW/eWOzf7THSvV7exYtgguwUnMYzl8pniApfHN0ILjbHpizYRgEzgh1yTxBQOf7VgL6TGqJL6h'
        b'S2gaH9b5z2c5fJOcoIGl8OGBdeTMPu3CHpgIGZt4Ch85bD2hgabwrTFlSxor9AJ4Ch9P4Nu0SsR9S3B/TEPpRVF5lLz6W72MlGAf5WAP87t3097dppw4drZpEtpdG3Mq'
        b'O10WPHf8iWuSTJNBp2YfEsxurZpgf+nzc5euLjYKjnnR6UT08m99bPbtsyus3Djk4ur7R1/fcU72/FMHH/vgl5cO3n3s95TPdo7e/I/tD9xPRi16bE/a0BcCY0Ke853x'
        b'QZZTsa+R84+XjeuSy9Ja3zj74m+rMr6d9d0550nXj99pm/s323NZ++YuDM20PzLilscw2FB5dsbCWAuLm/Mrcs1O6VaHLJ3cfGlNfl3c7KAxQw7qvCvEDf1gSvoOs31u'
        b'Py8yszi48t3HvbbsaHvp40m33j3+x7kR30xvq4FD1uW/Zf2c9N6UH+aFWef4mofbJUcON8/qML2iP+3Et3NKXlmp86+WN42Mwy6+dee+lzPOLkgqfmFk9a3ndVYWvpvy'
        b'ydb3Ptsw/YmFZY0u7wd7jZ4+xPbk6liX71uGjLzz/DGblhWnc9b8uKB5/YsV9wqq7rxj9olRYdnrHTafOTnPOviOVnRrlMmvT7zktWL5de8vO/KGnVv2eWXpV7e+PvbE'
        b'sJB5Hqt/MflxUKzx5KrL0vebvH+0bhvyqsuTNsoxsR3lOUT0/HXo5ife+jxk6xMvrc7YNOezz2d8p18XeKa0LO2Vp0c6Pe++evbfdL7XuzDPOGnOJp05b55P++3WhbsJ'
        b'0wu/KnFONf+x1a3Du/W2rutXijfAJyjrxhvf36s7+Gv1sF2vlm9dv3TwmuGD2qov2Xx19KvXrSJutX091a3uslPYM6FmoSX3fCf+fUfIlm+sry3MGb3lOQO7zIXnq8/U'
        b'zg35bWqt/9M1P8+qfrwj0DgAX3riJSvXYccLX773oCPxc7AyXD3ObdnV/L/feGp2/aD2BW1Wt2oWTP04Z/qD3S+/ELA5/fqtdZHD5oxa8OD6L7uKM9fWBDX8H96+Ay6q'
        b'JPn/zZshDkmCgohiQoaooqKYUZQcBMwKSBIlKAOYEwpIBkWCiAhKRpEkAoq7Vbo5x1s3Rzen29t0G/4dZgjqert79/+tnwX6vX4dq7uruupbpef/cFJSTfDH7/0+L0Ph'
        b'+vaUT8offbr8jmFD5OLseVdOLXih3cMn5fNpN3amzN9zITK39ON/BGw+UVCxZ+Wjaf4kz09VJkapC3zdYmLaC2589ml5RVC/1vdtpkvd+3//7YvES3O/tCsftbzt+ddG'
        b'pf377JygURfkXx88/Kt2v0H/w1/dGnsp/2vvSx4Tjh776HrTq73zk59c3lq0ebri8pwLAaGyL6qPJFq2vBIzdepLP73zleKbd14reUjuel769a7wXTU1+67lzP3B7Yrh'
        b'd6f3fPlh7Zqndv32+b6vnrL92XX5r9K+xZajI9772X133Aqfj/91dVSE2wVX04h9awtTZgsHsj4xj/1d9lH4D88ELeh9Lh/PV+3rulHw3vzjJ4smPTr/7Yd/8w18JvS9'
        b'2q0LfjOMe+WzxyPnKpIYzgxrptreC4bDIgsV+92rcjJCmOdq9yEXLoHQyvFwrXCEs+d9mOmyCors74HEYboLR08cWQrtHBE3CIeLgaPS2LBoldk9ds7Cs2ZUQ3MXlE0O'
        b'RYxP3+WqoQKyMRQbVMJx0dFUg39eijVYqRziaBiMDdrtpEugbzkz1w5dF6XCsSm8yTlkh+1EqDjGwWzZUmE+HNOETuVSVtVsqF7ro9ZqaYY54SnRDvsmc6vgs3hCZIA1'
        b'FVwNMqBKnBoOZdzOukp+iAPWfCQClNkwvFoQEQrYKJxyxhw1Fs1HKmA9R6tBjxnrxrqNQ2C2QZzadjgj4jVoVnB3OeehCqoYVs17GUerNcFZPM3kEbe1C1VQNS+JsNGd'
        b'AtW08QwreiVm770PUm0ztKZAegoXhEpCY3y8+Y2EBl6HJkNRiv1+3JT66jQb7PQZQqnJpzGcGlRgFsuwjbAuLUqnIZga1MgZUk1ThVU0x1zI5Ei1IZyaArulJpN2s56F'
        b'20EJR5pRnBkcM6dQM7zuqhYxqwS8EKIcgppVqMzPlyTp3wdotgQuk7YVRPFB68SuQGaXNBu71SIedG5lLw/i9Xlyf0c9Bek1nE+B6xK8RMTqRk5Y3XhYfxCTogak7MQb'
        b'0qiVmMus1LWtcMAHz0LvCCSbCsdGqKWWyacrNaCbQ9lUODZjP+liKIVGthDHQwleZFA2yohjtoKh2QQ8CdXjZTJoj8ZsDogc2IbtHLKmxqtB5g7pAkKFmSyD8VQPhlkb'
        b'AqwRVqFRmkQGh1viy6BwKQU1jIVzHPIABSsJf0RfSaA0whRLyWANwtY6sY9Pf72EdHKYnykBq6kUjxkwwMn+Ip515+C1ydEMvga1WAeFnOwHLHeN8KJEVvtpI6nZXrzE'
        b'lpQWVi2Q2w5i1/YdZOg1wqc3MrpcBBkrGXzNkZBFARxh8DVP7lsqZTeeV8HXSKMxE+opfm0c5PNm3yC94wC2QfgadDlJt2D5DFZ0KOGwaymGjePXsH+zBKt9VE7Vb5CZ'
        b'aOQYNhV+Tcddgt2EnnmXb2ABEfEZgm15qMr7UxSW8JdtkIVnGIANzx/iGDY4n6rDGh0EtYt8fNXINaBOQkRswAvL+QZT4gUZDHeiwpwQZrhKqoPlprzkUryCTdhAKLNz'
        b'CMHWb8EBDW14Yh1HsPlgLwexWWI9FrGS5+PVaH7nSvaQrkEn8kfgOvcSfwYLZJzH9ZtGeVwiRKWzD5Oxh/R0hAczU21pPLZt5RC3PrItD/AmU3wNVptQiA227mHEvRq7'
        b'5xBqKFP+AY4Nqy3ZXRChtjZoUYaQHt4FZ2NYtvGExNm8ZGH1GBWajUHZyEjXSDAHimfzbvS7m3I8G9RKmF+ww8AnZYodNjJIG8ezEYmrWbJ5J5ZyOMXhmdDKQW07FRTW'
        b'hoUWgeyz/XBjAQe0+WzlkDay4R7DC3xruUwGlSPa7ERhERYxRJvdVo5QrdqLxUrMOURhNWTx0HvSbtJmc7wss8cuV343ddnJepDLhpKtlMu2I2ce5eWTXP24QYKMcPlb'
        b'JDPIptfL9iUnDyyVq0uk1KkLV0fBCRFaCW1cZ8vZx36zXIXH0Ry9EOrESWSWDvPLsuYkffvBnUrPBNopiO4aHuEY+T4YgH4lPyZ11Dg6AY4IVvNlULwIz/FZL3SbyU8b'
        b'jqHbSgGT1UhD9jJoc0iUClrMMXRwGE8yHF1QIocydTstVqHosIi0brXEES5EcNzPZRe4CLlAKOZ+QLoVzqyAeXhyLgXSYTbUMTAdkf1vRHBgW9FovKrCvg0C35Ac99Kp'
        b'UXCWbw3H9fD4oAaAtGHASgV9y1rM+IVoOEWxN/cC3xjqDRo2UeBb2WjG/0whBNE0NGCCYITp5OiEMymhWM1p+5onFpEWFZBFRpggHcxReKmYAAs4Ils5S87H9KK1MSVt'
        b'HwXrr99iLTwjLoWjqHLG12QYpoK6qXFuUCdI/aA2iZFS+DLfwWtaDUE+z41e00pXseHSsBDo7agfltMLSHY9isUGvNZey1AlqTGAUFShPdmCjfZI8VLC/l1TOYnnm7nY'
        b'EyoknJmfRHA/qI0V4r7phELZUJdZ71VSF6TZlI2kPZIIo8yk8+HCARlmpFC0RywWLb0H+HeeLONhuLkh4B/mk22fzVCrLjTcA5kLmAgXDk7kO+FlqA1hMF+266RAG4XO'
        b'jhuvcisIhfb0JRRjPodok4ryVzP63wWtcfxDDg7GU9Aq1YZM2xRqoosFa7CHAvvg6vx72shwfSk+bNpnYU7qPdhEOLoBzkPtVk7Jp2ZY3APpI8dmJYX16ezGYrb1bEmd'
        b'RzF9cDqVw/oIc1Myi49Bjy40ygexbxQ03URBfXiC7ANsszu33YKC+qZO4rA+OGtJ2CLauMl4Sbp5nfI+gD5/6GffroJWuLKBMKxqRB80wDWOqXSGjrsBfbOwEXISyGZJ'
        b'iUmLkB0D9O1ZzCF9ZC20HeBuGbMwx4Th+QzhkqiQjI+CAg7OLYNMPKmE2mV3Ifo4nG/7Ir4bnsDiqRTNx7B8WOIhmsAVMk6M+zmDRXtVeD47CQ2pfZbj+bBoJmuWawzh'
        b'mxicj0zGln0MzrfDkNGDAR7ZxLF8DMg3FwkLeEofati6CvWxdo8iK+ceIF/EbPax+wq8onQaxPCF4zEK45u4jAs/p6xJP1QwvkEIn+l+6TxtrOOnchOcs1fD+KAeMnh0'
        b'loPKFHqxhI32WMNgfN5J4h7JAndf1ia7PZipjksukL2rWAXWK4dahcH/PTyPobCYVkF8EDaP/7NQI/SMpH+EzdMexOYZk3+mLCKMEUlTXN5/wORJtVX4ORnDy1E5YSQ6'
        b'z5jh8UxZDgOK8pOZS0ZLZOKK/wqVZz4SlTf6btXB/xaSd1xLhQV5oDbjsPDzCGDeHzSK1E4BCMmdalSelP64LyAv+SzN+GexeCb/lzC8alL3uxSpuEr4+zA8bamRpgp2'
        b'Z6OG3RmTlPkS5rVRMRlPjrivJizpdXpnLRFs4YZGAl5xHWE/a6D6rUy/B3C3XlaiVaJTYhIj0p8lBqq/TVW/dfnvOGmMNEqaL0bZDWqUaHQcvSz9LIMsIxY9W48C9xjQ'
        b'TSNaM0ozSuuYQKOG54vrtUhal6XlLK1N0nosrc/SOiRtwNKGLK1L0kYsPYql5SRtzNImLK1H0qYsbcbS+iQ9mqXHsLQBSZuztAVLG5L0WJa2ZGkjkh7H0lYsPYqkx7P0'
        b'BJY2Jmlrlp7I0iYkPYmlJ7O0aZZGjEQF3zNjf9Mo5NrrRzOTSSnTtmlnycnYGJKxGcXGxjZKQXKMiRIZBsb+tt6ypX4hy1Vqs3eviHeZS1J7peE5ONJv0NomJYmGiFDy'
        b'PLNnOvDfLiygAv1r1ojC1No5pZP10mGGgCq7NoYnUFnPkbcp0cks3kNSGo18mzLSkG947AcH6+iIyK3WydE7kqOV0YnDihhmaUiNU0eU8EemPCN1hCMS/knUgssrxpqF'
        b'fFVa74pOjrZWpm5JiGM2SXGJw2AazEiKvI4g/6dsTY4eWXlCdMrWpChmuU7anBSfFs20mal084nfQ42tRgS3sPaIY3ZLtksVKpPb+JHWXNToSWUPyCfCWTUP6hF3sLZ1'
        b'V6izRVgro6ldWkr0gyaJzqHtMgXFdkQMs/1TWd0lJcfFxiVGxFOQgQrSTIaAAiju6qhSGRHL4CXRPIgHycV7bx0VvYPstkrrJN5wZsBnq3rnTiksIUk50o4rMikhgZoW'
        b'M9q7y1jQXyHelu5OiL+tGRmRkDJ7VqRUtdVoqLYdpm2iDj1VYDGtLHVoLTnbPiRkAxFjDFSqaelxzaPCAdlezf1SppqWMdW09KBsmG3xz5I/AR8bsXj+2EzsjywHSY+4'
        b'0eBaP1+V1RuLosLKHZorMivMMpQsxfubk9pGcxL6o3X6AFgTG043ik6JjCArPZw0KZxb7/HCBgsZTm5/ENsmIioqjtt6quodQW6UMHemRquWrDKVrKXBLeP+cI4RFrE8'
        b'ZA1dcRGpKUkJESlxkYxAE6KTY4cFpPkDYEgyWYk7khKj6AjzdfzgADOD55q+ishGmg5Y+Sspt9t907nz+R/sFdc3N6coHldcyVW80nFEKcQd0K6z0GY29tzs7RjWGUIn'
        b'YdF77BVQBelAsmO2Aq5ArgJLoQP4R1AH55cyLjOEKSLNzfACtJDaDwoLtx2E1rlMJauzUty4j+pAhXDfcrtgIZU6LZ6psQM6yfY+X4iZMz9SN/7H33///b3VsrT9opEg'
        b'LAnXO7jOVkil4m3QUshm7pexxGW6KGjMG4XnJIFEyKpWiOzQN4EqRyXmGGD2Ll8o5UoCIhnq2NlKhJlYommfZsx0+ClYhpVy8hSb4aog+klcF2EHKYNKNzuMElRFsO91'
        b'6Q+JMMlNA/JCJ0EvdjG1aRxWQKucvJuMZxypxNYngSbM9yWF0KHbCNVYMbyYZC+7naTxxf5EOrf38nGimorVWK49TjcilV0IdOMNOXaqXkER1gnas8VEzIVyhZS7Pz4f'
        b'D0U0docjFrtMny0KegfEdRO2H5jPvieDcGPf0FtNQe+gaInN8aPgFH/fNBVPD72XCHqHRHfoSkiBY6nUyskwxJ3HBPEM8aS5gjwx23X6kBJmuaHWmNi1PL5FJ7TZcWcu'
        b'QY6ToBavMNnPBAqkUA0Da1M9SKZxeIlaAAwZpvBYKnoCjTbi6+PjKO5cCFXj8DrkmGEHdviYQo6PXBc7INd7VbAQHWPkumURI5mnkmRTlgqcEkz3mAmp62l3Lkf531s6'
        b'DZGT7+wdaovZnpgXTE0gIzDDJxQv0+tqRrbMJobI7sZTdYmYXKehgb0eU6FJIXjsMsUqQywgo83UFFXG1FWx4Q7b6GSJIOJViQ2e3sPsB7Bvyy65dvJuivonUoSdySGm'
        b'yZ/tDEexU28nXoZi9kmrZAqWezFN/pppe5Q7/FcF0htXqZ4kHArhHK+mIzpcuRM71jrq0U8OS6YQ0TiPEBGlsQTIwQIlXtmJlZhLi4RrktHQ4sP19jVL8DytD4oS1dXB'
        b'Eehjs22GlS53TbYVNCbAWWhOpZE9ybBfhjPDA8H4OXoHhNKZ34+5/CvVmMJh7BSwOl5OKOwaVLM9AVsw79A9X0P1xkDH1fwrAU8IUXhVW1B4x017p1JQFpD1PcZ3f8LJ'
        b'JxNfXGKaeWf0owVWP5ydU1cy37HnhWSvDcZbM/q2hOpkxy95M0/0vWC3s+Pyc09p+mzta/pFcPi8LPzI2q+F1rXt7gvEJ53muaQu641/5M4vdxYrByxev/18qJ+J8dOf'
        b'eWfO/Wj5GuXewDcNE/znzX9m9sfXSowyprzw2/hSz6K85GmPXtu40qjXaE9qcOTtMQ72H05rx6BX899a2/2U/TwD31vvLjLcfSrrqyb4xiXbxXXl/I9vvX9n+SiPqRnT'
        b'gutqphVHPVR2+7ecKfPG7z9x8/MDq4IfW5H5zGsev3blZy6a4PP1hmUWjR0Ouc3aNZG+bpmr816Pr33MxqP8vbdSiv1eu931/bntK47pZLZqftOamjCh/8erDi8bXc3f'
        b'denjVhz45ysvz6s7o6h3zOvq3BJ0pnMAF3f985VdERc2mZa1Ju+5sLH9p9DNmamKgjrpDy8HX0p5esqHXm3lv1vVbrm09uMXTFcuznpyP7zheU3vy+3P9TTa9TnYv7c3'
        b'/aeosiN3tBcEP3Lyvd+CLN8atWyLzoJ3Ar52m7Q1Sceu+nVPt+m/a77x3IxX/Xb6HPvodSH1VvPZ0KTCl17+cdO7m44+XvxtnfOXx/vfGz+3vt/fu9Zz8nNf5j7Xur++'
        b'ID5M2pH69Ut9sgUTHIOO7qvMrJPEbvB6/B0t3+9uZf7j2MmTb7laJv3y0Wseik9WJtx82vXV44ZZhl0bjC5Nnfvw718/JRrmP3Zoz+mG3Vu/u/ntLPlZm69b61Oem39r'
        b'2b62395bpzH+9jSNgH92r9twus7h9LHfstZlPPuh+ffPZBbufvOa/Iut9TVjugxPR2+Y5xb+79ktfW4fGwVb7H/+86mLwr8piNlxtlR3VunS9FDro8+fjT8c/uwel1uN'
        b'VquWfW+4babOkrgjHW/OjArTfy34g9SDkpc+Mj6elq5Yym+vB+wg397JT8RCvESWWKPEBwqT2S3VgYXmkAttdFMhWw3miIIcrkWNI0tNx4a5cpvnM8Hey1cLOtaRD49L'
        b'FuLZyaory82JKg136Bq1p9ZWOMMq1JmCfZDrTHWYu0w0BM1wcdI86Oa3+acmwBUatMg5wNED00VB86Boh1lwNYWeKXb2mEk+pIpRXyfIDmAKXiwaD8edPR3sGLhTSwgj'
        b'J/FFM4HfsjVvj7lLUy+FYqyJxct72RWdFmR5M5dV+Y40uoCmoLlZnKwn41fJPVDp7hPg6OVAL2zl0GUOvVR73bmelb3FGA+rjASgaslwO4ESU3aZNhYqYgYDL19LGxZ3'
        b'GfPH8su0Syt3q+/4sIycw9xpV4svvxMe2LZGdc0XEqP22DVABoqO4RITuGDvBRfXbCAHuyxWgpk4AHlc53FyPpTQS+qhO0AoxHRfiTAWz8h2zgAOEsXupSsG1W5YPA0u'
        b'rfZm35vZQC8ZZW8/H0d6Z+evukScgqc0sBbL5zuOZXegenBkghLzvehs+Bj4O2KXjwg3JgnjV8igDk/gaTZKE6ywjqq0C3V4DkHfQyQsRxf2hk3jrS2Bq6GkOn9HB7+h'
        b'2sjGflmwniHDun3a3GzjKp7FY8MuLkUp1IlQEgM9fLLa4WgK5AY4efs5ePlJBIOtUnKOVM4l7De72s/BGjzLj2zVTa3+bOoQbkALr2lwXWUWXqUhhCjw1gdz54RpCZo6'
        b'oh7UGzNKhxbMtVH6+usFO5FDb7tk/8IEfmt9fq4J1VJaBKg9bVqG72a0pRNoyFRtmHPIVq1rg0ruzHgDVmE/Uxl5Y94EuCgVNPC0hCyLo46s1KV+VtR+4EwSczPXLIFq'
        b'M8xg4+VmA0eHaR+hynKEAtIWSlnl86Oxh2kA3QhZcRUgtEANo52D8yapVIczF3BnmHAWT/BBaML0IKopysEeOOyrSSqvlEABnj7ESHKWIaEz0qfCvVBpT1vWKYEGb6hk'
        b'I7Qtasegvj3JE64tgizWFHPrFWpTGPu9VPfcJ0oW4WXuStnXjGlpsUeDOhu1XolZHCZQsZmctWQ6h/S0xnBpFl6XYu5cqOeLux4uRjAoAVMgxWCboA2nRcJjlqkcZFcv'
        b'8rvHJMgdL6os8vE6vxEfZUGjFNor7LGdu2jtlsAlaAjjdHf4IKHlzkHuSVMwiJLGyj3w+mS2JU3YCzcgd1cadunvHOLG1synMeCdscDTz5F8EuyhbaBQadOxYTrWK+11'
        b'CVuskECPKGgdEGdh+jY+/K14gXDN9smMyOFMrKAVLc4kW3AHG5W9JoRpyaXmElQBcxqPsoB9GoTZaZaNSvJke4q2EzbIaeGshBvLyZ7SLC4MxCbVnmYRoy6BkKaWYOAv'
        b'xctLl2ibctOUE1iVrCQkKfGGFkGCPRIjrJczivTFIuhSq1d6yQrPMMNzHHRxIxYb7lKxQKFSCjkpeIMXW4fNJmpzF+YctxGOzmfFHoAGqGc+P6HPh7r9nIwNU3nI+dqo'
        b'YNJUb+oLO4/vC86emC8VJmM9tW9occWzcJL1asYYHaW/ghlCMaWdkRUOBEmD4pBH3ppAZIhTSpXLZLLsasn+lo3HeNNqxm9TKnSgC5rptiKFDMneSEO+O2dCl429t6OP'
        b'o50/2VEMY6VwDWsibH144K2+hFGseZcCB1tIUS3ZVA2t2KwBldg/O4WMlxDtgW1DJII1lmoqoTQSMIcwp/Phkqa/YzLf9a9i5ipq37NOfxDBQfaNUjbUBnQfk9ODU23g'
        b'Ngr7LC2kcHEcXGBDQR0GpNuzU8dRMw7OC9rYL0KxG+azfXAhFHuqlUN4JnW4fggrohT6//0t9/9In3M/jwJd5Md/0NYcEqJ1JUYiRXxoSsZJ9CjyQ2R35RQVwjQgmkwT'
        b'oilqs78MSC4DyXiJjcRWYiwasWfa5Bm9Vzcib8aSJ6Mlo8kbY/LbQEI1PuNJaZrsrn3EEwn9Z8C+pHgTXhLV2ew1G37RdLdzAw2uLemj2oj+kXgSvf9qJqS8uKHSB0fT'
        b'i5pgO9HRfLBC5rDQazNcJXP/fvyPHBtcJF9wxwYjqxn0ajBDfd/NLowdrKNjnazt6A2Y0/TZLmrvLfdzcvAfG7iVNzD0wQ28rG7gz5a0JarrU+u4qBF1/snKbmuHRfI7'
        b'9QfU2DlY40SGTWaA3Bhr9iFF2P+lemN5vfphg/fFYXEPqvzKYOU2S61TE+N2pkbfB4b/N1qgF6a+SXxwA3oHG2BHe69MId1nt5GDF5F/pxExfK7fFR4419cG63YKTqL+'
        b'ghJjkpgjA+uILUmpKSPcD/2t+hc+uP4bI2ltmDucv0FryUseXBkMVjZ2qDJ3r2V/q2PuD67r1mBd9rSuxIghd05qHxjcCcBfq1y1xUQ/uPLHBiu3DbmPsyN1A/5Gzbd1'
        b'mQ+BMIrof0ADnhw5rcwRAF/Wf28LYXWmJD2gxmcGa7RQuYz4+/Xph22JiKcqkrCkHdGJD6j0+cFK59JKaW5+cx8/XOV3t4eRv0Nutw0G2xQZn6SMfkCjXhrZKJr9bzfq'
        b'f+rlUiLcrZ+Q+seFa+yWKimD/O6u1M/C13Q/tkU75h1fqaB9XNJ9y0Mh4RJQqV/qkAAkQImxSgCqhaw/cFNpqDZ9odZh/5GZOiTE7jW969CPj04MC/vzTippha9SfmM6'
        b'rfA/8RuHhZYRrirvW/n/ZBq2/udpkPmHxIUZnROU9PHSMU/6ROjFvPOU8MUuQaaQ2D318xCV3TvO1cJfG+dt9zBXW5KS4v/KQNMab/+FgW7UexBrx2sfHGlaG1XUMmtY'
        b'pqgd8uupdgXFlbWSLP1BRa14XIPMgZTMgcjmQMrmQDwoVc1BzPA5oIoFio91GTEHE/w53q8cuhKpmoAqCfyhl+oJ1ugwPdnTczSEqxJjqh1x+MVut8BhujlEFMxSGiTr'
        b'UMVAbiTWSpywGHmw0PGWGkKJvwn9wtctdqGQ6kwe7jLELHalQg1pe3wxmzm2yKOxU/2pq7hVgascV4vC5iVaUIP1s3hc1AxSzwkfb6oGgIKhGzMNwS55baQGtGxIZK2X'
        b'EwH4nHIHM0eX4sVAPUk45o3hWqkrcGPWMNtd7TEu3HT31AaVzgvObKXXPT6Yq0XEwSueRFK+CJdDmBYvzgz7VGFJsTyFYn6xfBT7biX0wUkmvE71tfOn8B4iv0bPxp4Q'
        b'Xu0AlGE2kxMdvWSCjjkc0xKhAOqhh4eZvLJZl1veyrDdXCaBasgXmZJnOxzGLHrvqXDUFHTGWc0ToW4h1DMlz7pQE3XkqVl6FM2DxwL5dFRGUFSDoz8TNzXDIWuTaDYX'
        b'85niDRtXWPpggRd1z+eLuWy4uWsBezK8Aws1MB+vjx9BinI1KS4fIsWRhCgZ9ESmJkJdToRrCF09mBDZFfU9hOjkz6htqx116SFYT097aP4ji4wENlqRK4KV/jaT1JE3'
        b'yDiewmIObr2CmV5KLy1oUgdXgvx4qGTv5q5d5+qgul9QTxA2uHF6r8S8FKUvHsZif9V9IzRvYwDwQ9hioPSFPCtnQtraEisfPMw/oTbe5T6YYw8X1VHE2zgxILVXzydD'
        b'a3RwWOT0ddDJdMp4mAanoICXMqxQR2yCWkOs4K9b3TZTxMt0yB4ermk5Xme6btYmD2jGQjgJGfSUnihMxLY0hQb7GgawNI5+bhYy/Ou1hM4oYWwhS2iAxvTNgOahuOOz'
        b'DRn0mSyqLsjAxtV3wV6kW6ywgH2e4gyEFuEG5HFIDYPThGIb09ImQS1cssd8OAJn7Z3IKnFSOHr7SYRJkKExzwLL+foqhKxw6tviMNQPC78krmVj6gIZEpVVtGRysKCp'
        b'LY6B4o2caiv0IPPukClqs2o8aqARg9VwkXkXmIcnoZXZ3vuyy2XmeTKHLQWbNdi9R2P7GshiasWxu8ZT5UfYpnvDygwW7w9HtLAIcmMY6engsZnKHRNS/QcVq+2kVjZv'
        b'3Xg0kHwyTz64t7CdZVwEaxS0WOMRH2/oo8rre7YvunlBkyOnniMeU+gOBMcpOIzuQnQLOgg85vNKvGTk44g3pqvCAMH5hdjDab+FQt+poX6ct9qLSTTeYAM73X2yejsw'
        b'iRY0yW5AdpgS7l2gPjSV7CJYGagOYdc03iNVFSWklmz9uWTcJHPTNtFo0eVjUlVIwj5bez9ohcuOZJ3JIuhOmAe9fIozoJJuMHAZ0z0dHVgExFJxv+56RiVwcbahvS22'
        b'L71PsBodLE1k5Y/yjbe3dcTqccMCNWExFDFKMIFCLCblT8Vr99vD6P4VCOcVfPtc6Y1nIBc7oHZxmkyQYKOADZgfzXtRi23QqcR2TbqaPaFZgCIy8E1M5+6TBGeww5Lq'
        b'qAQHwQFK97OzrCVWLpCtV3t6zGar2dJo7kjAxlnKtsnpox8xd08exR9+r63Bdy6bJr+VfuH8YcJifYFUbTt9Tqf3TrvV/GH4Fh1qbTB9esxLUYc1U0Z6XWBMDf2fwYmE'
        b'TQYHJPslO/SihNVkS90pRql5c864qIIyS9Lu4sh/1lkQG50YvXtH8qJoHZU/AJmQupbWTpaV8q77dDLWzCWqg5cj5JA/ykb4WsCTUuyEk8Y+cMIFiycabZmDTdC0B5rM'
        b'NDzSBCgPMsNOu5k8HPpxLGNmHmQhnnR08mL4Eu+gQMfVnvecQJBnSDa1TlFXImAVNuuFz4HrzD5mMimliGzcCkfMgVy3GSqNkZYwLlRGFvr12LjvS56VKN8nnerf4xEd'
        b'Mj/pxUDTRQNXTOY/M99/fUPds11+wbaBZ5tnfqRlPfH5pvR3mz1cG71fnOr+w+rjaV+L3z700uPF5uVGN85LpTcOZzfdEGbs+LLdcr3bzd8Gvtp/Z+dX7cavTbZ/6l/W'
        b'HWmH7LUvmj9yLu+5d1dU679+RvGIX/T4uT9GPearA4Gls66aPRRkaGE53sdnZmLAUgFMSy9rtbUpLH557YnStHKz1wa+rzwxI9BrtlaVRXLfpKze6t9fXBAR2RM/JjHl'
        b'p4Odcreqm9nrN5s+l1rcIXq86dXVOHPmZO8LH/VdNrSbf3t53RtH3yxNvjD588fMHXY6X8qbODNz4KlHQi8W6Et/qrkhnfjxG8L0lszUmTBmzrOPpi7Xf+LgrYU3g4+9'
        b'vSOpMD//wu13HLUqPsww7NsX9OxNnxPPe23dlrK/t3ZqZ9m0zsote5Pf8j6dsPnJ31I9fDpaPpaOOl5f/vCPE266PHEq8Wam4ydbDAaWLZv8ybfrhWkOKfsPLKr+NibU'
        b'/6Objl9Yxp9fb5jS6t8+L7F/VfXEpKLbS2ZP+6jpM9N3NeDFY2MeP5C3wHrXkk+Nm6qLXL0STvT57nE5tuFYrE6b0YDHm2tujf3wN+s36h8b5/HKqZ627U9P/ufylfHH'
        b'X//R6qPoRTOz5l3UOmz59Gf5H1cVrH48VeuHt0MyvMYlffXCqIq9n50f/fOcx0PPXM15dePrPyZc9fr8puc0YeearlCv0q2blV8b/EvD7TP3Mcbj1mGS+Y2ssOe3LF6W'
        b'992Pi8LGWjYvOC1PWLdoxo/JE/r1no2edynZ+YufUrWiKnqeuz77lVNuj60uWnj1CWOt87vWLF7TV/TKxi86b45ZfPPQYe++NZ81TrZ/3H/a9e6vfF02fVZ9Ii3g56q6'
        b'N3ts4h2FL+PuPP/vY5secS/r+elnhf+LuC0lbPdkrfzpJovfq/pg0Yl95pWZAyvrmzvsxr+4cP1RJVzdFbrsO9nbA60RZdUvPPrpmA6bXxdm/mS5Wxx9et/a38/XfGoc'
        b'9euHwesOSTTHuc1/6N15VxsOSd5uW/hOzSOKeVxzf3INNXcqILxGlzM0ytjOfW0PnOP6vKrRcEOOOXgeGxReOraEqybs4yhokMKZBdjGNB+bVhyS2xHR9aoCO5iGVttS'
        b'XI39GhyKUxKlpdZWQ4O2AJeCEjjI5joNud2ZMgbSB2MdWs7ewJQ7S/GCwt5raQRcHFSSN6lwutiHuZOx0xkuzBiM7gdngQYwY6+rZwdQ72RHsGUYx0R2HlUkt3pyEnWT'
        b'3fqynKLfdvo6KzQFfZLRZpMnw11BPamgYEhPG4GtI4GiUMQNEJaa4WUlOQ6OYroqBCG1wjDgqqDihBQ1xnM0FvCwhYfhClOcmU3AdLkt3sA+yjaJIZJF+wjLyHj32nH6'
        b'akVs/AQBrpHdU9Wryl2YL7d10p84IrYm9E5jbdmwDy4onbBo7mCoSjiP53n4L3fIMFf6KnyxlEwO2Rx9NARdPRHOjQ7nePvL0+UMsO4gwNl5gia0ii5YJuWh9MZp+NAo'
        b'eukqTwLMjQA2QyHXV27E2kFgMl5ZpoqtOdGLU9V1yIN0jmqWwylVYM4JcFgdpveGLhnjnNQFdA8mh948CeF/eg6y2Z89SUPulJaoBlRTMPV2aOAfFmM1nlBijgte8PLC'
        b'Hh9R0Nop2hkb87ftEZgrt4USKFNBWSmOFW5MYBrhKVAkpwpLaEzYyTXCumtEIm0dgRL29QHsspVD0w6u04Qy0ubTEmyzCuLGNpW7iShIqKIXW3icw8mY5cqnOzMQmuTe'
        b'hHSK/Ow1ibDQJ4Hi9ciV3UYL4JSSGnI6+UDhViddyhuZQ7fMFS/FcUjamRCoVwWY8yH8oRrqakr4ZRoNL5nliiKll6ihqK5xI8GocAFaWBftsYUw+52Eda5ao4JvMvCm'
        b'G/CYpRYxNLYoB6BhCZxT2ab0IIfr4fEJjlbB9zh/EPGaO55XXVw5YwlbGGuDRwSmXAC1nIazoNVZngq5yao4kUsJy8mDjEIV9lOQMrM3yTQRNDwkmJ8C7Vy7fh2PeMtt'
        b'tbBQHVcQGomIzXW9c/ACNKjU0GmQSS1Gc7GBf1eCdVCgwhj7YrWgOVqchF1LWXdn2WMhWee7oUKN8mO4xSPQxIq12A8Vcic4naSORwhnKRqSqltDw6CMwxaJMNAwErq4'
        b'fHQKtRKOgKKDcu+5u3jQwPELkjjaujwyYDBaIPbsGwEvhJa9HObdiH0GHF94AC6wcIHeB/iyadrlSqgbzyoNCCWSHmv5iBMJC1XDFmsw6WsGdjq4+aijGEJtHHJ4PJwl'
        b'/Gmn2jkJkY4qufHWTO7f0XAWWfy5Dv5wnurLiTjjIBHkZD3jJU0ZI514qI6lGdYdIqwZHvekHhoviYQ/vxHJ9/Ey571EnBuDF50JLwk1kkArOfswwXu7fYDDJMIN57Dr'
        b'Di1BjgMi9sA1Q75wGuCMl9wO8jZggZQaLM8i89rLUYvnoBvOYcXmu+17tCBrLDt+9CA/hhuyHUodbsomYiuUwSnF6P/P2K+7VbP/vWfE27oUhBPGjOEZS/4EZdD/8z3j'
        b'IcGUgxZlDMRIfxpIbJhK3EFiJxnPVOQUIkihjKKEK7U5ZFDU1BNtJaMltqKxxEBiLjLFuCp0If+tJ45lMDSqZKd5xpK/xkqMRBq0kEMbjSTjpGOZklyX5LOWjCP/aElG'
        b'rDQGtBTpveRexd2qZtrbMKcFTDmlXOQ01HsuaMhu66TsjopOiYiLV97WCkvZvSVCGT3swvRvBDUgwssrVG3+8qDu/CXyl5SKKxRn+CeuWA8Lv3MXjbrsZ6qfwPx4HIf2'
        b'ewUcJXb9WRmHbGQVhg54GnIUUu4euMhvy6C3Gygja+i6KPXS4XeUbW5Qzl/CcSLbUkwzvw4YC+dlZANsdU+dxBdR57RhLQhQlTdhw4r5MrLJHzUhEixbiHmp1oOVhTvR'
        b'qrDImZWB7Z7uw6oiDW4ZXtVKbE6l99XbE3fbU6Oui7YT8Iynn5OXX9AOOh4sCAd1UCARws20p8DlORwYcHw5lqpsufduVltzJ5AjopTfxBRuoHcj+Y620BTCCpoxO8hT'
        b'1UK3KIcpmoI2ZrNLXhciyOUPhgJJx4s0HAiv23bY9cdGOK1tiOfGpFJWbjvhaOvuNzBQgWfo0MigmBWehhc8lXeVFapyBU07RnmfGKizPqRNmMfWyLiXP4vUUF4l1Lti'
        b'RUd0cH+iyVLTqrJX+z/rvu4/bloa2F8Lyxxb55th5O4OpuY+W6Nq2qPHzc/IrbBZcbsu+8r57CK/pV5VJybNfnvJw1qBHqamZypSjyzv3HfnDeWzC394JtEmZuf61VHV'
        b'UbX2eo//+HmhTc57T/Xf0PO7rrHBGGeFbtTx0or/1rPDMKqr331u0bRVQrahvKPovP7MhpWm7Q03dze+Vmt7ferLvnv3TeleP2D8vSLXb2asosnkg18Wig5Lbk1bM+pq'
        b'zkM1737XMuUr/4RjZ989PDE4fbWOp5fHQ7W9t54o2HTlsR8bcu28zQ3G9+R90/vhrISenMjVoa3LVzxqNkb+TmjWqy+dHrW+MbUsYf7i9n+aTHYOsWrW2PTYxx80OYUf'
        b'spRm/lj3/sulL3300MWLXWO3vfi9pOOjosxv4t+YYlF18MXxdt+EbCiIfPvpQ7WluXPWLPpCc+MbYU1TZ0XoBCxf5Zk+xfcJHS+7XwMvPfnzvrdNN/2Q8H7DogVfzc14'
        b'O+7cr/Oqgk0e+iEjz+/KC7Wjlafbd27SWqV3TGelY/hAX6PTa5Xu9fkmk0Iy3JY/Df5av8f/Yl7xZNqElj3tE7Nu7PyxD9s7Z70Q+Pn7BQVNig/HpzTtmvphXE1A9AXp'
        b'phOW0zZ2FpaOigtbef3N5z87o7NGb9ONCZtT7Wbt0uvJNyld89C6WXsbf83ze1b59O/zAuv8X360rC/uRmD8O7ff63tjvea/X/D1XRj/2YpHHtV39F1X9oVvRfnur0f/'
        b'KxHCXurX+G6OTfK8p4z/9eUHM1K+NFjw5JWggtnZTU8NfJzT9+q0tE8PvLBwTuhTwbcu/fSd9vjTXzo3Nf977qEV9e/ZmFlUn5n0esdrQfjR1JfeWPNIgtP7Wvja2YKQ'
        b'fd+EZy/uef3gLd/4bX02jz+U9Yph78XIH9896RLSMzvxZsfsLyXdsVbfPjWQZZXuNP+ZZd+lByY/92nR0cvLpuzxT+85JHlGZpzZXqOYnkKNiCAHu4zvtYGk1m0GISNs'
        b'IKlbY5UZIp6y5laVRNCAdKhlRpdT8SRjX4yhD2vopTGTI6FmIRUloQi5F+hd4+HwSHM/PJtgJQ0isuUNxt+kYgbUUONoKvVB5gQq+EFxLBPMVkAbXLjXT9wEvA6l3Cr0'
        b'YjxnYgucDVQMt9NyPD7EcEMVZDL2Kw2OwgB1Uy2IllCbJllKONMTjMmRQiW2qAKZb4B2wuOnrOFO6roId9OnZlNo98kTyqxYee7HUzLoMk5j4xMaAflyInsU7Jqn6qPc'
        b'RMSjy9QuoGui91LL8p0KiaCRiEd2SQjTdm0P55zzjSZwW8eOJBwQoBeKQeX4qncXdVzEXKYtwRr/XSSX7i4RWixVTLf7Dgslt66WaplQQ0jCFZdw4+de6J8vdyLTKGJT'
        b'+BrJ/CUSbkPe7B/HGepGbebJbD8eZh1Yhz1SldXs3E2DdrMeMwjLzPVBZLy7mQ83Mlop26nSJN0fMxmztgFyU9TCA/ROHS4/wEmoYAU4BlJsktoFBqE6KoBgYQArYCmU'
        b'h3MjR8iEzJFeMAKgjTVwJ2FJiyg8TcUfu8E5yiK3q81Cq5fgiUGXQz77iDQA9QouRLdgpY+SOvanxqhSzJwHTZRRzjbiBsMd0+ESFfzzqVxO+PwQIBJBBVwnJVO6sguG'
        b'o3Inv2SeI4XUPWopdppKt+EAVLIS3Ail36ASJB83bXL61OmLUUSi62ZChSEcnsb915ESmlU+7JgHOyIPl6Q4s/H1pAHq70JKwHFnvAIDd0ElsHQdl8mu7oIMSrQ7oRSb'
        b'h0u2Z/x5xztWw3m1ZEvE9DysZJLtUoUKrkDO++tyby671pElR+XX7ds4xZ7BEpshN4R4Y3aYaKenwWSdcWTmjg3CTHJMRrDn0+ASL6ALy+ww14cvauwMDJDg4XmW7N1W'
        b'e6xVReoky7OImcxiujufjkvmFgylIbcc6cyxeB2r3CoSO4eJDXA0hglpEsE8WjYJruxhPZ9OhNtz1NiXn/zahCNonStugauHuEOkI3B0gfo143x4NyeshTPmMmxetIjN'
        b'fDC0TleFYD+DZWT+qfssXV+RTHdTItucNKRI7bspqwPZKn1MRRLnSaav1zQhW8/hFAY/y8M+CtK4357LLYoPQQk1Kia1tPILuPLReFLNxcBVV8ZjagkG66UzSG+useoX'
        b'hhCZekTlXBkEA6SJxzWgC06H8p2kXBpPywogIuDYMU60VlKUVDrREnP4dVCTlHCWHFejKWimQPVmcfIia4Xx/0eZ6n/lSGa4oxh9tbXM1T8nXSVQCUebGRmT/0UjGqCd'
        b'yDVjach2KgMRScicuYmh0o8xk3u0mew1Tjo+mUhJJGUqHcuMi82Z23qRmhCL9H/mDIaUqUfTorbUQKrHjJw1iTRGDZVZmRrc2b2xRCbyGrWl2uK9ZrtMllLJTdyC5JX/'
        b'peGxSm6yGzGMb/4F05S6B1sds+ZT8y/z+4ZhNwujWPzIFC4ehlHgPQ2ry7y/MGcwzAVMAvlxW0tlg3tbb7hR7G35MAPV5LE09zz63Wb6g4JHWei42zqDFn+3tVSGeLf1'
        b'hlvI3dYfYZvGTKGYmQ4bED7+Zv93Nw9DxklXSfWudD62kJS2gUyUiQ4Smy3Mh4zkf/pT1JPqSZkYRbbXc4HDxV7Cb1VzZLUFNsqiyTlTe3/DLhpih7lMEQYDCWsNGnmJ'
        b'f97Wjh4HjsLdRl4r/VOD6P7YNx+rXabPmjlnxmwXwp5mkt3uckpKctrOVCXZsC8TPq0Dr5BOdGOnobaeroGOvpwc+schD0/gqeBALMay1cwfWq9cju1Qw4HSl+Ow3IXs'
        b'/P2CMEOYAXn6zDNAQiIcd5Ep/AVhpjATz2E5ewqN2LjbRVyM7dT2xMXfLdWIPF0MLVjvornwkCDMIv9MedZif9FFMgV6BGG2MBtqXdjTySvNXTQIy1MmCHOEOdDow32o'
        b'98F57HCREjaCZHcVXKFzDnM6gCWW01y09m8ThLnC3DAz1mBdrBwNnYSDzhOEecI8yIhmZZgeIF0i3PFpJlILbngNq1h+KN4C7UrZRrhA2EfBXQevs8dbxkKJUoRePC8I'
        b'y4RlppDNQ+i041moVGpqYo4gLBeWh2E+H6YSOAsFSkki1gqCh+Bx0Ji3PIuI68VKDThOZmuFsAJPwGk2JljkOFYphdOEmFcKK21WsYdaa7BUqWW2SBA8BU8oVvL2NYcu'
        b'wE7KpQmCl+CVhHmsIXp4lTDrnbIJeE0QvAVvOKrFux9JetYpTkTSHR/BJwyL+XCfhzxSjGYCqcdX8J0sskK08aI3dlIPu2cFwU/wgxpr1myomIOV2Em40lxB8Bf8SaKP'
        b'lT7ffCx2SskgnhCEACEAumL4qJwKwlbs1FoaIgiBQiBegGqWXeEJJ+QCtMJ1QQgSgvCyGx+Vq1CGLXIZHqHzuUpYZQ4lrJVzoHeUXAzERmosGzwLz7KnmBeNzXLNyJ2C'
        b'ECKEbIYTvJBcIhYck1O+tYaIG0LoFujnjeklfGajXAMrkNDsamG1gy9rjAMWbZZLCafTKwhrhDUhWM1Lr8Aic7mWPtwQhLXC2rFzeOmnsc8IcgUcIEtrHREGjkAmK2Uu'
        b'Zq6HXJk2qWm9sJ7w5XXcZb/TBMgVoRLyCfcvbBCDWFOWEha9HE9SvoN01ElwctytauJUTMeTUm8kbXEWnKHNhj2HqoQDwYRLpeuH2iBlYzrPfyZuNp4UoY2cPvaCPZUJ'
        b'WK2L3S2CJWR4Cc1NFabixUi2KrS0ffCklttewvUJ050s+Iwe8YFTeJI6yL7BrC8wcyYrQg7HVgdrBANhD2wEm0WYo3BgRiVKu5nMyCDX3jlwDBba00BUUsEEq6TYh6XY'
        b'xcybJqTCFfaG/CAycLKwIdUE20gOwms2p1KmzZnskdd5Maos2IuneTHWwN1wxKdAPymA5ZAI+6aaTiUv55DlybRGcHyeuiHkvbFgttqEtITQI9lzuEy4iVoxFaoyiOQ0'
        b'MDWhjcyFbm5FVL1nIf+evx+PraYSkmFtLPt+tNd2VflaUJMsQKelCfTS70/gALf8a4QLB2kF16NopskC+3rR+FQqyaTiMTKTqtaRdk0iK/GiagxKD/H6eyOdVeNjLRLa'
        b'38F7D+me7G5QH1qpbVJuLJGmSa7JAu8edMJR9rmL63h7Nv5SqFkgKOAo6x0hPD4FcCEFr/AO0EZobRE05vEOHCLtpwWsGgdtbHzYe2MBat1YDxw1+anWBXU27CWtpQ3O'
        b'OfO8dLJZN6qwlXUV+zywnL2BdOrtA64lC9p7TKCBZFocwrJYQ62Ud5VnWCBEQS0vJh6PsSyEWquxSVUfHc8twpJ1KrIq28vue7GQ7KWHB/uERwKdndXkR4dmNuTwmT+3'
        b'GI+RUpyp6u8odiSrh+48cuIbCxewSFUVa1Oy4IHX+ehAXQxrz5p9cEI9viTHAoEciAVsfEhLW7mvlOad0DzYHC2oTabeqLt4z42hkjVmDBzepx5lrYlEaIN03nEFOUjZ'
        b'ROVhDpOZyHt3QggzIFPV7Rayo9EcSxJJL9j4HqHDl0zEymITOEWbctyB5diKmdjCmspyLBBiVCsS8uA4v7/O0Y8dHFzsmaRaFaqRIULXOWb/EwJXNAZ7FGCtWnyCivIJ'
        b'W8MofxW0TrJ3hspRtMajyZzw4Yguv9MuN9+lXtZHkqkJpqrDDiHMZm0+XMI28rolmGaRCqau9ONecl4yYjp/cJKqlVKopaQ0Fs6p+lK7jttOFoexAtRZFgh4bR/bG7BQ'
        b'nzVhOmHBOngb7NnSDoNutjoOLWPzH4BtlGLVc0trgVxNFZGU2TJdgC72B/CNw1oi6Nmwz73MeAOaoHGTemWTj7YIULCaj8HlMWzSCa0URQ9SMqYvEGLX8kGYqsMyuOAp'
        b'I94AcoCQHsBpPMVKwBPhbBwURJztUq29QlbH2jW8BCwj+xctYz+2O6onlNKOYA5ZfKRs1rCRHuUCxfRdGjn3SIZlqslOcFVIeCu7TKl2gYY8pLHRCF2XaEObCEekmHeH'
        b'8ZVFyUsUusxwbuIGkdrdbf2HRrjDQdkibk1nt0qPmth51q4Od/Ceo7K7e86GmdiFL4oI19M1V8X/+W6+sUA2FfNKw/CNoXOS+cP1mszg2PZLj3CHz3z28odWBw0F0rjw'
        b'KTPCfUs0l/OHhbGa1IB+etS08PgDJqqHj60ZJZBluCN3X7jDid2qiqI3MqNB8+2m4Q5ZE6bzh35KU8GW5NziHz7uykIb/lA7gJs7h/qGO9gEmfCHjS7MvNAzh3Tzhkuq'
        b'wAyjv7UYTU5GUrtD+Lj9sQlECgxZwV50HGJ2h+aRS8N98wKm8dy/pLC2Gn3tHK53a5KOcOd0Bf3v8cWsgiZt/vYN+3C9gXAf4Y4L+++fi9lpvB0vbqBzVIt1gpAkJBEG'
        b'7Bw7jaeF43F7LTtoFYTdwu6DmMUNlOkuBE3QTud5GLGNxjIVrZzAI6zaLw+OoV3wTFOEb7SVBfLOvurBhkX7fd/wjd1jDo00hhx0LUYXfKzKHJJHShqMkKRSUEpua8Ql'
        b'RkXvVgdI0hP+KECSoe5QgCQKE4ywh0v2/tQgmDmeppYufr4BeOo+8aYGY01BG56WLzWCOtaH2i1rhctkPH8OD3fbMXoZmRt//7gF1eckyhRST+T65zxWPelvGmR0cd++'
        b'mL31dx5/7p83p9nlTPr03DvS/f4bLZbBFuPJrf4PLXEfZ12/7NNL6yM7p39iGP78yasfbd94NTluY2dU9JuPvFOrTAqtcgu980amm/XWuY9Z547b+EHQ4axJ3rbn0+22'
        b'mS+zev/r55eYOHY9v3SMydysf149nHv12JPlN8023prt+65bYvhY151yl6v5r6HFsqA5yZO6vWre0p90qvExiybptOQ50c0fWL3xU/2Lc/+52TI65YMpr42ymPbE5Ufe'
        b'1NE99fhNt7lwfdGtvf/qf9w7xbx31Rfd2Z1nvmnyK8cD++RVpt1JyZZRb4R777ALeeHZA+u/OL2g36vA6pn2b7P/6fjpc56Ksb9ZeK78eqzhC894BBf5G0blPJz2wYp5'
        b'acuip9U5fOWbvckp9bGSXqOWqp457s8mVzyRlvlkPUQ7Jc5b9e+bpzoryz54rvNFWdAbl9qzfmr97lzPEgPHVa2ZndITDkcGtr7bnDx758opPzZ/MNpfGbTiStMTcwwP'
        b'fOad37IRJz+/yv5s6q1tPzRcDv3+29E/Gf6+O93msTyN6yGFY866zVSsX9CS8eiV5T/5WwVs+fX5R2ufrp9fpaft43XkevHM1OffeS3/mZnvl7sebE0f9+qe/Zvk72ef'
        b'2/9Z5jczYsc+nORQYfPqyUlnkyMv+B21LPeJ/cLZpN7P573Y9MQn4/rHPqyV6PWv8tc7YheGKL5f++Pr32vcbJu24eeugjvpX02fOnXDhwUvF06teP690fXBL7VFv2fT'
        b'I3vVdL/btFfwHwPf70hw/v3UK2ab3/nwzgLXW+/vefK5aZ/pb579eEpvRcnk9y796nMs4YvFdi98nrVtU9sFX8XblUf+1TLz3LuGPxXc7PlN12zOb+K6mW9d/jRUYcDv'
        b'Ca9C7k564bpiEiFpDUFjvwQvGI/iN77HsWznZHPM5V4fZJ4S6HTDoyr7OwsOGyi096Hus8kBdViOlVIRimaxj0OwHPKmE5mNRmZVaghSXckMwjHzi+pzhBFoTzhgjwXQ'
        b'6q0hyKIkcG0THGEfOkP6Jurzx8vBS0a5UXmaiJW7bJhaagqexKrBgDj+2MMs2aB4Ly+2ELuhcQd2kXKdSZtkqRLqhI276yGCbBFht1g4GRE6JZYJq/fBRX5DnU6EqAps'
        b'0KSGbMPM2HxVujK8YT1ehRLRoMHSevU0RbxO43mwRgVDM7PcavNhZjOk3jHUg3nTNqagicWOGK6iSpO4YvNSKIBOVuqOPeN9MN8iaIRrpFjowkyF5f+tMcwf3yNq/cXr'
        b'2tu6ysiIxLC4hIjYaHZrO0D36T9jE3NI8JOpHDjc/5+uyJ066DLrFgOpDXPHTS1ZqA3NaOb+wYC5BqeuJag1DHcgYUytZ6Sm5Pck5g6COuY2YtY3IrOq0WW/qT2OLQtX'
        b'qr7xlZH8RhInSfL7gzeF0tvSuITYYZe0f3J4Phg0X6Fl9VPzFXoL+ieuYem/R82HXcUyhkhf22zoNKInkQbUxQmjN8u0tWNGOHbVVR+Oi4RBx66azPsxh2mJMbqDDl1l'
        b'f+jQ9R6sJj04743VbeV//8tDqqAmdYox4t/FhYr31KXhz07VDxIpt/exrVQIj6+dtUlIpaE2oHQf9lN+co0tD+0bZOvpFexJ16YizktDcN2naYvXDsZ5iwtFJYUlz5E+'
        b'9Vm4Z8RTMbYnPg7f+NDloiPFNcdmZDRVtGe3H51YfsTFSkh66eGfNV+3C1WIfGPMsYNrPkFj1M5mNBeIY9Kgjsd7uJAKbfdRbxOBuBfyZdhmAofVyIz73AzflkdujY7c'
        b'HsY4FbaEpv/5JXRIsOWe8PdOCKNOjMOo04Qhi61hJasJWhI3jJzFEVT70SDVfkj+MtNVhar9k1R7WPjCYDjdUqcE1oRhrGCOxjyJNEkhG1C1n8zL3XZWPtRiAQs0IQfq'
        b'4MJqaoNsLscqRzzDxDoxGTp8HGi4mv40zJMJmmNFXaiCa/yi6JqWtcTKHk/4i4I4SkKDdR1ltNK1kLLMjXs0hXDfpDgrGoiTatwl1qE+vv7+FHamTQ6lqgBRaWvAPsiO'
        b'oiz6P9bpGIXr/RTgLygpg7vXfm2w/o6d0sdIM1ZLhF37GC/d6UIZ7KJw+ZLw+B2bgoV4OqaaezWo1CEIK+J9j89KUE4QlPQCLqnkVHBo6r/Mlu+SClINydQPr7PaXKwo'
        b'mz93v3RJuJ6HzRRBSbG+34y2fF8UVl8U5IJcImH5/i1QxnyHmZZ1uG+DpgfPZ9L57fsaQlyiYCAY+M5R0ku0GblG7/e0fijSazHz764p6djoO/YZXwoO1U/T3xFC2uco'
        b'KQn8XUnPxvUVJ9o+ZjraJltqZWHSLv3A4gO2rTPkdfLN6hcNH3d4nKwereRiiTjzmc2s3qw3xr1IaHOLoBAU235gj8wl378oE8rWCXaC3fEC9uirjf65EmGyh7BJ2PSY'
        b'M2tdv/13uYu6aBj294SMwB727OXozFydl54n1Pe+kFkpY3c/XtuJmO/FsEAuZHyWQTfkit7YghVx63JmayibCGXqxJd6rHo48aUlet2xMx/3TXvd/cnEVS8VNu595+ZK'
        b'YWGJ4eXVdsXNc9wbtQpDFB5VC62/f0hryqHnDN996NEdn+rs6zAuy/vXL7/88vmPjy94+BGjE3u+G6U9yWblcxm/bWpe4ZkIF30Sl3fMszth+d2tkOAZ5Va/7c+2yXDO'
        b'fHrrNOtpO5d+aNifMWVbyAHXhiUDnQeeXRKxxHR/isnyf3dPebT009GaJvLV12o1xpy0mN4n+3zra0+sMdvy+FSrlPrfq77BtOqnP12Z82LLU3veXNIakm0fmnN2Ya9B'
        b'2j/a7hjAvMTwtz06ZkyZ9lpu75xezStffpR34NuN+rbbFr26x+k1Iqn9br1I/PC3dv/NPXDkgNzxZsbX0g2bZ03/5FrB9iDNnZN++aF5dcDhDqtPvmudq/WyxZiTP177'
        b'NdVxt92u+sUNJrNrfrLsvOPaeWdBwMe6Tzfbr2+yXx9TPfPJXz1WvDrumGXHyjcjXmmo73zvl6+y8rw9/vHum9X2P35lPen9qxdKV69a+GhD11uPan2XBp/fCXwzLPv3'
        b'wq91Fj25/73ME2+GZZp8tN/+5d2z3jY8v7nk8sDjTjsineo+Mob3Fz9dUV2w4jWFEec48+E6XvBRYL5jWJCtpqAZK9qFYQW3mm4Nj6XeIjkAUBvT8RIUiUkBaxgLt9sh'
        b'idps+DkIGk6CbIYEWrEE2hk7Spg+aGb8lxc1L9QStFfAANSIBy0gl2nfsT3RWZmSlqZvAAWGhv5+2KG3U4NIoGelUKWN9axl+mGQp2JJvSZwphS6CLfGWt2J1TPwPJVg'
        b'/ah4K8IxycpDC1i7rIQp9t4MaNK0mrB/mqtEU13o51btxzFfruILE7BbxRpe1OMoh044EkwYSxUXrEP2R7kIJ7encm62HW5IyKcKR08splofzXBxshyOsZeigTkDe0A5'
        b'tBCBmaE9oAQauG3X4TUB0IAVtOjjXjTypRzaRaxSxPFqc7EmwsfLTzXIkIGHN4nR2LeLfawPN6DFh51scBmvqE43yMZKtXn/FQuKkA3wxZJEBZm++aKpPfb8lwrrv2Mc'
        b'PILvHDrv2KFZ/lcOzWkGGiywDOMtDQgvaaQKWk9tCawZd0j5RBoChvKYesy1GHdORnNSblOTcZWUP6V8JbXHFslbZpHNrQZU5VMONPnOIEepcVu2IyJl621ZVERKxG2d'
        b'2OiUsJS4lPjov8pjSpM/oWV+Sn98PHhu03pM//K5/eX44ec2izvVRhZC1oiDmywxLIXTwmg/mWmEe6So4tRkwxk/yrgwnbEkRjroCUB8oDuKe1g/2T2sn8yfnNx0RacQ'
        b'2u8mkhUFadO7QSjyJ+RsDD1STId057gn3nKSKql4N19//GfhH4d/Gu4b8Xm0bsw78RLB8lLSCumOi5OG+Q+R/qGy/rY+nZeR9GX3V+hra/JngzMu4/Pz6Uhrj+Gcl3j3'
        b'NNKPQ//yNF40Gj6NVC9hh2cO8fEaMY90j2qYukwjBNPH/v+bSOk9Eyn1j3PsHydlcQD0uwv5FMXHbInyjNCOeWfrKDJNE36Qxuhm/8lJUv53k7Q9+fO7J+mTB03SJyMn'
        b'iX689i9PUvOISZoiUOx1U5i9/72TBBfFqVitEQ5lkHf/WaI2OFl0niRZshjZn5ynY8Pnic7RvaEadP05NL568iLOdROWewL2Uq4bj0MD40pjXceL+3cbGAg73j10VdNP'
        b'nz38xE7qrSMwOLvDtxPNhXja1IQJEpkJZXXJRJ3aylj2hDHSYLhI95lsHTxG8U/ZtqwAxQzNJedFUrl1eHyxhQH3KxOOR0j2bDzpiKX2nl5SQXOdKMGSMXELHSo1lHtJ'
        b'jitPfGX11HwDmG66/PmKnYue0Cz6h3upVMPP2774hSO2tmftXQszp1rvayjv+mHrI6GB35S+GGq+rqLi65KJdvaZLsZzpgzE4PvJ3zltD3I/0X7sH5X+tpvGbXvd+Ief'
        b'Ml/5t67D5+99/Xzl77dw0efnI+u+aQn496zNMxIWK8zG10W+rNBmvEIknsFce0dbqq3YsUgTTouOcAXOcIgt5Fj7jNIf4nEof7MJOKhVE4ocfCBvBt3PaJRg6jAij3Aa'
        b'NEIEO5znhmCJDxzGdIcRSM5reIa9DoZ+KIIWzotkU6ff6ZoHxUmO6mjSl7Dbh15kwZlUdpfF7rHCDrFGx/kE2nsyr/nVeFSQuUpI7jy4zjgGByJeNQ9ejrlBOb8fc518'
        b'z4IkS+d+h9TQMtWje+mOqJgweu6xVbror6zSRHo1Y6ACTZmzQ9pYkvzFsJW7mtYiuwt7dE8zxeQv6Ter1e1iRWz4y+u3wfjuTRaq4QZ28m3W04v6WC+BKjauZNEck2H9'
        b'QpMR+6KO6rdy9F0hv0qkJXolWjFilJgvYVc24pBvnRjtKGmU7Jj2Ucl6WbRGlEaU5jEhSitKO19cr0nSOiyty9JaJC1naT2W1iZpfZY2YGkdkjZkaSOW1iXpUSxtzNJy'
        b'kjZhaVOW1iNpM5YezdL6JD2Gpc1Z2oCkLVh6LEsbkrQlS49jaSMaloz0yipq/DHt9aOiNWKE6FFHhQLJ+lHkDb2e0iGb14Qoa/LWOGoisyCbdFvLLyKRGvj97Dgi0AyN'
        b'TmWdwF/x0FsjA9EQFpHu0CP2y8GLK2qNyBwXMYM2NrT0hNMZ3Dllf7hzqkIc/Xz0P8Y3GtHCofhGfxRNiC4KHtCI/kXjFkXwIgKXr7COiYu/T2ikQWqiZKx9z+493p/F'
        b'goGT0IlZbIHT4CcBjqtVsCi4iMcdsBranCTCSomWK7RZptLzHq8Qjuq0fMfOYPJenTlEO01fFy7sCKGBglVxYSOttfXgtBfbm8cSTpG5m4E2W7W/GezHc0zNu3ENVg8G'
        b'ft2M/QKL/ArZEibpx1vK7L39uLNxe4lgMg0HoECKlcFe7Jpmuburz0xv0QnzBQm2CdgD5/Ea93GTjYd3sLDG5K92gcY1xsNYyap0GYuH4RR0+Kh90suTRKxIxEamfl+9'
        b'nG1q+QF20ymQNteXOq3Haqn7xHHccOZSFGT4wEXPTTNJw+jnhpOlaxdasPaaBm/hQpK/n4RCVshO3EN6kwPt3FriLGZABRGy7EgWEWuxg2RgETcvw2mOGMxfI7XYPhS4'
        b'm/o8gjJT1u7VWES16r7eEXh2mO+DU9Yc/texEi+ymNRYCA3MzZQ9XOKFXiVtaWSR02dtVruRWmHMuiuH61C5dPWI0OlGUjMoxR52iWUURi+xPD21l4THn0yx4m6l4vEC'
        b'XAimoHk4Q026oD2ZHc2hMpq53EGDZH5n02J6m2ZNt1EikrfYk+KHnD1h7kTu74m06xT7dpkNvYkrN9USwvUmrdkg8Jb3W41n0c8b/AadUEFbEDfVSDfCOuqBKsVqhA8q'
        b'zIljA7Jj2TpVRHeoH8s9UGH2YsZOjQ2Lva+HKMhxYrF38TQhFVrHRIv1hEqwHk/5MWnCWSS0cE66SQrFcW0eT4hKarL82znPAyf6E3G6nodXRfu4O79euf32Y1opn791'
        b'MXdMjcaqc0dPBm3+1MNi/Qcmn9e9vS4naMKS1x1eui5raon8x8lXN89uXr9309GM8wff+vktg/Xf9eH50RfT30oyzL6lGfbctM2ua48eLX7m1y+OtOou1Joz453OjjvB'
        b'r0SdW5rWuiFh36bnKj4OSQnrGl3173+GvFLzuV7tVysX5y0qPDgl0bo/0nLmtBcs0taeR5PVX6V98LUiOvWrh2usKgOnaY43rQ7e6XIwYlL/1pWan7+xZH63vP/zkIsL'
        b'HvnyU7PPPljwxYnkj0LKI2fHdo/uPn4ytidl/53EVZd+tN/s+VFf8XrP2b+Uzro29fMr27/caPGxUYVf4uva0RNLXvX1KvBv3hvpvcU79M0do71G33I44fBzrcPa3z28'
        b'Ftt+Mmnqr7UOkz688fhG11XypuoSj39Ee/9c/8aHyWHP/L5l9Vj5rucO/SJ8H1n2rwZHxdgUlYu2vvF0b8qFHnpQMuZjiR9jidZjLdRCFnb5+No58XNUHi/iBbLGczhK'
        b'LH0cmdZcB392+aMB/dgk0OC2ByADC3jkiT7MmKIOAzIUAwQLNmm7wCXuSr4Ya73uubTH05CujlRwHLmrgaWLXanaxZFekxIWGBoP6iphgDXVkyo1tywhZ/5geGu5khaS'
        b'CRlMFbjMTJNqAvEkllFt4FKyKTdz4E9h6joW72Nw/xuNZ2W7Et0SyJc8MDPkQifkBsycHektCtJ4yerwGH5j1gs5jswDaSpDYkmxWgJFPpjJC87GzDgaxAG7sXkoLsdc'
        b'KMQedi0200rBtEj5AYNboLGrEzRJoYbsVUUcuFIJ9VtJIWQnVO2DxvuwEoulZLZOQyuPJd6CJ93nr2AN4ZuiIA8ifcdjG1gzR5H9+rSXJg18wLdEQT5VxHPx23gnjkP6'
        b'ErXHA+btwCrYkeJ9+Ay37jblBZ+H9sG9y1BHmkL2bfa9iy1ksxzMgZ2mtugK7RY0vBr35FBPBimPTsuQDztjrDOmgO4j65FHLxFJ9modD4bYYo7s5ISGsCcUC9nr2dBC'
        b'iskN8IXqdaod22CZdIUe4eqpzilorTFWunK57X7bzZJUrVE7kYfDhhOLoZ0Fh1lFY1jxU9QgVuqGx3UYvZLROEmonkVSUe9FxnP/H3PvAVbVmS2A7nMOvTcpgorY6CjY'
        b'wIpGelGKgo1epShFBRsISO+9Su+9iogka03J3MnUTOZmMklmkilpM8nclGmZ8ta/9wFB0STOve+98EXxnL3/sv7V1/rXOm4kgQe2UCx4M0niEDsvFFRMgSy01A5jtQS6'
        b'faDKTPbpriLF572ysNQEYPSbKOy3OCUlXl1X4SOyCiLB08buzvAtnfkfVm9AiY/xMq+ZnEhFRoe/RaPEtwdY/FT4URFr8LHeb/K8kihdQ6pBPl77X3r75v2Vpr7C13ZC'
        b'ioVXzVeA6eI3NiQqjJbft3lisV+3+vab3DOrb/+A1iUU+F+aYam2vwlfUV+qqT6qMv88xfylhaHlg5JjohKeWV7/x4sLEqZfLK/P3gtJSU36hkWypYXAZYJCbUOfMemr'
        b'S5OaOsWFRBnHRBrHpAgtO4/YHlmCwfOUXvd5Nvx/vjSzEV8AOykiPCYlMekbNzAQyvgnLTy7W8IvlmZbL51N6Fnw3NXHFYPiE8NjImOeeaRvLs26jS9lH5KcYiy8FvYf'
        b'Tx9xNSIs9dkNG361NP3mpemF155v7uxFXOYvkD1r5neXZjZfRKuUZSRF+CUM8Vx7lw8KjwglVHnG/L9bmn8DT0v8889XUT9yEeCLGPqMad9fmnbjCpx+romXTnrRQ/SM'
        b'iT9amnjLcoOZwXzRWl45uXRuXog9np0iWspO4fI4svtFZPdzvN0v4u1+7qZoNY8pG+pJz7bCUzJhvkF99EUPQ8Cq7Xh5/LoSHcH3LE6JZs2gH2FZUoTQVYHvGZyQmPKk'
        b'y2CF22DxOJ5wzn/QrCTm69/LvP3JRxaxwXz9+zgRp9AtejVoo5lI0K36oCl5meqKzVghVV8dsA1Kn1KbPWjxVi/fAufr6xK3OPn0DYuia2mjjzJcIqMiUry+fsF2toxP'
        b'lKQXHL+2rM7gKpcXbk9lEj8Bc+E+TnjuOi1odFj9yJuB5Y/nt/D5gDAvRyY5thr93wVdnkyconPdGv03MR90qVpvzoIusZF/CC6K4oMucRrZIs7kZxL8VQWdL69o9qcy'
        b'24M/3xsws8w6cYAGrPiqqExS8HMftPKzDzo5ImWFApew8rBXxmoePbG0qD8/x7EXrYjWsMRwfz19OnQchpavc+xkH7BjN1emjydxXlrNSVMZOwgjYIhv4iyjLoIeWLjO'
        b'f3UYb0M2vYYzZ9lXdiIasf5azLXr1WI+3NOzdeFClEuYR4hHSOw7vRHRUdFRHmFuIV4hok/1D924oB+r7xvw3nZZu4vTHDc6q/DZr3/2RObZ6lloSQFS7BHqbH2Tc5Oo'
        b'yKuJ0zWfOLvFmVc9o8dm/vg5DqdqebrZKvOvzpL5oJlQvZ5bCpp9FWOOIsbs+QRXPcqy65IFsU9seKXnN9k4OSUmLs74ckhcTPgznLgibjWBIufl5yTcOjFI51JSdAha'
        b'xpdf3yyyiimpUZMkB9E3t4cmPgr+Yajp791CVCLfp98stSQVHsd8zDyCDyaP6ZaFm/309qeBSh6H+2MNHOpi9R30G+sL9sfq645ah3MF2y2DD+088/JxNH6p7Nst0PQD'
        b'Hx35n0psaydkuVdl9M+lRZop8GbwORj3sFhmc7p4q8G0xBmnrKXVTbEH5hedvPuTRVIf74CX4CS4AwXnFr2mOIQNIsFriuNX+e+tmDN6GQENpjFHsAQbz6cJOecNkKnr'
        b'/sgNgXexlLlkoRpbhBzve/5OjAx9sVOWk+F7JkzAgFBO5r6srgURoysMynCxLnJxYpMorBTeqj5Ky6UvLIFVgJUxEsG4hfqivPiqgJZCTHIQf6o8ubzwTclFW6jtx//P'
        b'Zziz2hQyy0zAxeGfJtZWXd8KKSdPL375HBSVq7WqTbq0IDPt1Yo/LKvywEfXTjEgScgiS2LZj0mvs6IPCot2xBsKiyr9G3KCdvyGnKC4vqGwqEm+obCoDPK8gd+OAIv/'
        b'vFfiMr7zCS3sAoOSB/1LgZDH9Ox/XntBTVlFLNz17Au2Z5KiE24vunyUoEQMc9dwboXI1pL+nXz78XigXJV+FRcuLmZRMvlc1VytXO1I2a8fBxTeIl1COVwlW4HFASO5'
        b'CAU+8qbAxg5XLRbxCeLKNK5MuFq4Oj+u4tJ3sqS4aoRr8p8q8avRD9cqFodv5t/R4t/SCV+TrUjfK9P3HHuiSp5+9MN1i+XCt/AVJGSl3UFUc9VyNXI1c7Vz9SNVwg3C'
        b'1/LvqQjj0o9ClSKt1bBYEr6Vj33K8gE61t5GLVedzZark7smVzdXj97XCDcKX8e/ryp9n3+7Sj58Pb2/jZ+TvanOv6VLbyjyEUb2hhq/v41sf7QDcbhJ+CZ+h+rh2rxG'
        b'ZfqGmhTx6a+QqIikd3bSwaxg4I7GK59gXJ/+TjYOIYa/XAywkGBIinFIEnOwXEqNIQRfMVAkKez88+H0VVgKM+FiUoxTkkISkkPCmP2a/Fjk0DWFxEpiknSqpVlCkpcs'
        b'IJJHCcYhxlExlyMSpMMmJqU9Noy1tfGVkCTWIMzB4cnQJDOuHtvgkjg7cszP0dr4hcSEbSnGqckR/A4uJiWGp/LL3bgyGCt1lXmziOzyWwory4wslRhhx75UZkSSJ3nq'
        b'/QSpSH7n9OMHw4PosYDsokSOX9zKc8VklyDJrDA6zuXgX9XcYmfOH1W4tbEr728KT6QVkXlmHHE1JjmFfXKFQTRU6qiJWEVLkC5IalkLa3rC3r4SwxZJ30Sm0nAh4eGE'
        b'Hk9ZU0I4/W8ccvFiYkwCTbjcH/UMFYUd3ZO3P1S9eDvIDh5cXaruWeQuv/uUy5IXGyuw2IMvxOnj4uG11DJtAXOVsQvvyfJx5zDzHcveX/Y2vcM73qENW+S4y5ireAPv'
        b'YaOQmzQCNax5PCnYLjKc7DbLXSKsg3JrviqJN3YctlBdL89fSU2GJumdYrgNub5W2I3j2GXLSaA41ZpT3y/erG4s3CK5nQ79S92o2CWSUyF89FxoQrXHTBbK02FeKHtR'
        b'jnXqFlBqKmaNOZJxEOt5bW2DutAEhNOKsOyzC+b40qtqh1TcH20K8/gmV8WWWOLJapdZnua4E4nymKEFGXzge89prMRS7Em+JMsqC3BQ4IA9Mdst3xMlf5u+PvLJ5mOl'
        b'LNdJ5c6tHtX4tEOdbsYlsIVTfD3AZOOaPpeqHeeCdyif3TirlvuOyt5A/bi//eU3Ez/o/bFKYvj7jldC/foDC3xOdPm/6/PzlhaH7zRMuT6I1fTf5tdg2GOtrJmprVx5'
        b'8Gdzcd+r+H6x7nq37DfWy12Iu3h4vvDVnOrrn1WcA7P96Zp/fm3A5eXs0bzs4dyP8r844HHQeeBfVYenP2w6e+iI6btTDfu+m5nz143yh0JD/Yttgj5ovtf3QfrfTnxq'
        b'l2VV8Kr6Bjw0GXLDTEcIcnVtYTncJR4iTrzDM1S0A8imFqzQWh+ysWoSnwzi8dXzhHqH8ABqpOF0HD21GFEfhwIh6bkIZmCOT4CAahiWBhmhyVlQXIt8IX8xwkho1SyN'
        b'Mm4OE16+H3hrMf0JhyKl1wOxQWgSsHbbCeiE++58KgWr0KioI4Y2DU9ep/V3w3os9MQiL3bk5jivLcepwaTkhL/Qov4I3va3sMECphHIQa89lootfXGWf3cbTtGmhswe'
        b'RTelkc220MWC3ENYRQqzBw6eIPtwowiaN2ziv3LF5hRpNwCWHL4Nx8V2Gvv4AvR7MRPvQoWjNN7GTFSiNCs5Tg+mZVxgXk+IyfZCY/SSni+nHXdarKoK3dLq8qcusCJ5'
        b'7qz+HFvXTbEspwm1EigVK/Ar98EpexYtk1K5HnaKODVfiSf2nBIKlhZvhpwdUElvsxukrN4gf+UHSmzcrfjaiKycgzOMyUNpiBt/RDdJc3rAciLoJEugajEpwhP7+DXF'
        b'YzOWwiSO8NdYVhQaPBQu1AishblIoN2yRGaaanFOOU6XxlqAAccn08S+TvL1aiEyv29qBtgznVGOTzRX41PGVfje2SzZfD1vFAjBrHS9lZL4KZ2sl+TsMjvhGSFBifDs'
        b'KoEsQ2XajMM3MxsyuPeW31h86pK/rutd9qscwfuVpY7gJ6ZaCm7ZLYnvJ+X1Mtn8H0S7kn7KPTMYc2hxkV/HTb4oald4qrcL2hHTiiRf01cd9f+arzqS9K/U1fQv9t8K'
        b'd3VSRHxiylKnX1IkoxNT48KZ3nM5Iok3Co1DokKYWrbqWEtJdUfjIkKSWPvYF5Z0Mam/m9eLYgS9jzlcUpn/ZdXBkiNSmD4XHOyXlBoRHLwYsjG/kJiQksjfljQ3josJ'
        b'TQqhwVl88HJITFxIaFzEU9WplKXmzYvnSq8lJsVExSQwlY4p484RSYR5aZbGiQwcV2KSVx9NiEguLdApJC6ZVvi8vvy8X5QLvWy/994nHwXfcF7ey9Z9dtGXX7MLFpYz'
        b'R8hIf8Qfd675X/flB6VvfYxgk8Pigni4/0cu/aPPxbUWVjj1nTlWWkoPCpnVLvh2p9gvHt5WWHEUOi2WixCsWdXDr79e7QBW3XhGuj7vd8wVfe10/civ9vDLeKWyrcuf'
        b'1XpcuLIsznwPczdL6PfDPCWWqWnDlM98bw/mTYMByFe2d7eJ8RswlCSzGsbxP8//KNha68PgV0JNdc1DPELiIuNC/xBcL3k/OCHyD8EFUW4saOAhz9UoK2j912dmEl62'
        b'47x8wCpyPSb2CckOWZjDF+VOuIYPlrKvoJJbfmuaJV91QTsvwr1wEjIEDNWGqSckeAZ2L8YEni2nl6IS39i7Hcpk8ddC268IUKySkb5KlMLzuTB5akVWugvHa3PVx1bD'
        b'ZCvo+gpM5oMW+kfUXKEW58zE/I0NvYBz7n7QwyM5H7AwhC4+YAGNPmruClDKvyTEKybxXswhnyOyfMkDM53/eTxgERflFub1xQE+aGGwLGTRLeK+ba4Y9NaFJ0MWz4g3'
        b'hTz3yZ5SUdKQSdd/2sk+Gb74ilUcea6je3F5iOnpqyGWx5yrq3MWBmiWZU+cRZZ4i+wSb5F8ZUJ79xPyxZkkUMiierTcmfV0h0l8UkSk4Jx4Ip1oFZ9GUkRKalJCsoOx'
        b'41Ljd+mug40TQ2NJtD/DF7G6TiPrlbqL4yvWZbPUUCnW+x8/ZXXylAuX+kT6uzUxv4ydirFwD0f5JrCsQhoMk5lub7LCd7HcUicjR1kei9W9YmYM3cXJ3vTaFzFffhT8'
        b'h+APg78XGh3ZH8GiMAEvBuBo2VhAV7aZrOmm7/z4lde/9fpLxyWdFwjVJ+oyYwPH6ybqC5vcAnzrDo/vKnpJpSmGq7TQVPC5UvpDMzne+DTAVigTruZwMtCEBbzh2gKN'
        b'vFkU68KKXaywD22x/AYU20hzXxU3LFrNWI4Pl1nOHNzlOwvEY2mE1OoOFUGN6o4weyFa0wwV19w9vBy2LrpqlE+LyQzPw3GeactCLmavWuhCBvovsZRZ9RVU+3QDZHn1'
        b'C3Y9SIo2PB07fFM6vigkFirwLY7S1z5GQcuGX5kAeHIle149qiIWHnukbejREH7PRejDOssJ/RnLXJ3Gn0hbeZbmIOE92TJ/n1qVulOeTBZKjFy8d/J/T+yOwpxfg9hX'
        b'j42SduuRvUaUzPxEE3VrPwo+++KPXyKSq2m7s7FwR13mhCx3U9bmVzJ1s1lmYsERkAs9OMZf0cJSnjlgCw4yB8xabJZJx2ZO8HIMwALmL17h4CAbB4QrHDCIE4uq5+ox'
        b'bOXnlkK3OJasuho6SM/mmVgregqasvWEPxeatqh9FZpK1yWd9A355JDLEUEhyV6ru/hZUqxUMsnxpqzc13Twk3R6J3Q1A3MRhVnEI1xaov5rIbDjUnQmIiWEZQaGCNlT'
        b'8YmXSdSxovKL4/5vYb/wjhRADiwOwMdlLJmxF5+anMKMYIEak1OYwcgyFpnTYlWjT3BkrMh2YwYjDb5a5GCJ8Nhak0KuCOCiPT+D3hguPenoVxKE63kdoo7HRKtUsMIw'
        b'q770hHDtx3u8RzvcB/os3MT4EAo5kQuH1VCCuXyZmYt2vUJ1GplxeU6mXpTyaRHvR38pmC+BGT3jGuyReCiQ8+MdKUJl6btYrmLhLYZmW07kw2GDl1PMvtdauOR89sTg'
        b'sOcrQ2piRw3Jr73eu3l7o6lCi55YRuG3Mpe0yibu/GDLb/7U+9aeCMcQ8zc+V85+4dC2so12G1OOaDpXf/mxY2XZrvH9W97fHvmwxvVswcnNLcGv/ybDrqnLbmr4U/hW'
        b'53DXzEM3H8P/+nX8jlfefPeXe8/t+eO6t/64zio+7sMPe0p+aH771l/yvv2FxL9/64ZMU+m9YFxwgbuCJHeDCsED7Sy9f4DFFw4+kuMiKBZcvaZ4l5fjR9Xx/grvN7Ro'
        b'CWIcs3CWd/mm4JgJ8wWLsIHe5p3BO7GTT5w4gs2YZ2G+2FJyARo5xX1iuEvGWJNg+k/ob33cHxwA1YJLGDsupUjvtNXzrSGFa8A0TLu03es02XG8Q3oqIm7JmY3526FX'
        b'bGkv9xRhKvd13apvyEvvDPMs1eWbs1QNFWklDi3+LoAWfwtBRaQjStddhaHRRCu9qTwzNRB/Df1AsuzZR9zXkP6Z+Fzct1J3Ofd9ymIJkN6Ld5nfUFxKnReSJRTE7DZ0'
        b'XEhClJ9TmLyUsNk2tBYJ24txZHb9lbkWlfg4OYvNi3PVczVyJbma0nCsVqSWlFPL5ykSp1YgTi3Pc2oFnlPL31RY5gq8KbMKp3YMD2c59gkRV1YmRzHHmRDzFEK0YYlJ'
        b'SRHJFxMTwpl77+k3X4l/OoSkpCQ5BC/ZRcErnGaCV89S6ktbci+yIPwTg4U8NehuHBaSwDhzUiLLU1lMMU4JSSL4G4eGJFx4unhYEal9TMdaNU77VKHxLEHDAMECyckX'
        b'I8L4HVoKUF5VbDy62ZGQGh8akfS1o85LiCUs49EVjSvRMWHRK+QXv6OEkPjVPZuJgpN1EQ7RiXHhhMzLpOFjWfPxIUkXHkuUWDq0ZGPhiom1sfeiN1V4PSIlOjHc2CEy'
        b'NSGM0IOeWVSng1cdaHH1YSFxcRHMGR2ZKBWuS7fLBSRIZQn8LMshZNVxluPQUyG5lJLoYPz4/ZNHuduL8z4th1s6Vqht6JOjLL/F8hXvM85Amoivt/FuO3urHfy/U4m7'
        b'EBGGRywe1eJYhPoClqzuhn4hIjIkNS4leZFElsZa9cS3JRvz/2TZKE8sboW6IsVMtpWLZDLQb19D2VrSYtSljG6lFrPNi3dkBW7HmWRo8LUlhi9KZE0Rs8/ySgqWRWGx'
        b'snXK5UsiToR5HDaZQIa0ZCDcC8YsCxz29cISMpqhRHRUKSaVqfpQpRGqfPnSCcG5YGptZYp5NuaunqQK9ftdJLvZA4ZOCgkEUGWuuPe6r3A5/07wphVJD65QJubNjsWk'
        b'Bzku7LwCu5KZxitEP5Wocvqci4Hi8WBLRZtDXKopfah3k938fpSwgCW6pkImpqWZlZssd8BCDhsuwyyvN1nBhNgCK3Bwmxwn0mQd4y/wI89qsfKCV/fKGQd7fN8pRSjA'
        b'HePM9K+M0+yyt+KOE8KH759ntTd/vVaFC1Z51fW4oI4l4QgMYAdrUlHPihZqwjxfpIt/o/u6AqfB6Ytlg4PjXtY4xvEJI9hokMAqBnj6uvAuY1dafJEFc88sbYS+cLF0'
        b'87B2paHvW5nLcVhopnIJqq+nMmtiNzTh8BOaaJEZaULQ5yfooDCrx+LykImzitCBY9DrZKbAX+OHWqzEh9Kwcg9MLoaVTQL4euaJKRruSSrsqj1/zf5WHJ9uEgvtNBS7'
        b'ZO/pHCK9ZI/Z0J0q5ArA7UPskr1n1PJr9k6b+FejAqCNv+beB80npNfcWVsgoWhAIe0l32LZNdWgE8JF9xbo4f2rPnujpTfdOcUdEarsonsOzvE33eE+VF94/K471MXx'
        b'90/5u+6p682U+UVcwXmmvBPQoRrzFus0tEXyENkErXwVPOkNZgWsv4ld4mtYlCbcxc/EUU2Wo5t49FGtBgk2noMigXCmZOC++wsOtm5iaaUGLFHkae3wKTN3mCJ1Vepq'
        b'2rEFpwWIPeSQOdswX21ZlYY4eMBn6ohMtfkiDUv3k2kF2XyZhmvx/OtkPhQpL8sKVo9hOcFrsEboXlKEs9izVKqBJRxvwHHxNRltAeRlrpjhvuyi7WVo4e/9QyH2CQM8'
        b'hIo1S14ABTqjnhNiyPSEDKFuwdgeHz6NKN/Jx0qOk0SI9pE6LFS8wFGsNfclk2giAMv8j7M+fFYiaNm8ga+3ULmPlVD4k4bc4WCP19YSOfAa9ECaMm2X5sRKbxlOrEJG'
        b'g/YFMyW+4hkMnduZrJaUimMqOKYOBWQ6kHHVtVM7VuJqRftleUvYiX04t/KpZGx3xMlU5t/olvB5EqVC65QyRahe/uiVlEuKSVgfq6omx5lKZPB2uLVQu78GG1lzyVSc'
        b'TL5EpFesnpQq4XzgjraRZE8izvBOU2jdF5Z8KVWJH0kdpxRxjCZlTxOR1bBVsCUcOi8na0K/sWEx7wjeXnpl8QmcggLtCIljqKvQFXvqwpqlZ/gFqqo5YK8ctx6GZbZi'
        b'HfTzNepogZNwd9lgKUlI1IzFa7SPSRywertQya6dADv2aDhiyUFYK8dpyDHPZibmCXDudYRaZZxO4cuMzCWrKKqSJq96UwwTZK3e4c9WxRj72dE2uR0/zk5WFmdFUA4L'
        b'Er4txiGohCZfTyz3xWKs9oViGc4BaxRYs87pdVeFDiJDOIc9wixJOLp8kv3S3K8YTWhNxmn1JGxzkeXE2C0yNzuRasez7y6WPEPM0t3G08Pbn8kUH6lL25KxzSJXD1fi'
        b'bAXEQ+C2vyJpUTwNXoVMVrW9GJsMJZzIgcOqMy4CYIqIf+ThhAsxkDVw292KyM1LhtOEJgnU0Bf3hf4WRwy5ndz2NBWN4Ot5oWKBra/VMOf8uB9HiDSCQz8+vpETWnJw'
        b'fz0k/cX0sJmM0AmMuDmd1wDH6dtxaVxa/Hkhe26Y1VQfkCF2UcOlc+kwkSa0JKtcDwsW8pysJ0vcI/Trlxb4xbsmrK8X5sAkF8PFYHVazNo9H8gmXyBbZ0epbrzPvgQd'
        b'R42hj+vf+tsnJbfm1v/yr6V/26bbJinh5BQ32Vva11UPvva6oo/3u7J9617/g8jo84sK4m8Z7FUSaW4cufadF2R8P+t/+6MPP+z/KVb0H7VyFxlW/dTkj/6Glt2Nlr+Y'
        b'K9fLrV3/5e6D7fX3tA7/69sW30r/4ffrt55I7Q9r/pHMX7b5Nd9WNqq9rTxw6PT7Ib/4zcWtCx4XfML/rlrPBb1+3CplUMZZNum/fWze/9Pbv7mqcsFki2FImPOfw19x'
        b'3ZR9TLFnq3+7ZvPdXZtdoiK5/XEvO/1K+1VDh27td1+Jtf/9S1GBGXNeqf3XHJrz8/fovcatUT/37Rvfyo04WDnVM2G7R/m/Lsjo2LS9nPpG6ot7CnvfzN0tf2Xw+kT2'
        b'f1vu2an36hWP9NYD4YFmzsEa8VbaNvfefz3wnT/0T+RMXPjh8L65d/4gOf9A+SefjDUWZJ8+YtFW9WPX3vCBd7rmOj+eMvjo5jXd6n+++zvdgX/VG2nWfetvB9PX/cnt'
        b'2ozSVb+y31k5mER3+qoWZB//9cE1//rN0e/O2Hw09y951e64gbrvf/DRMPh/N7v43ojR2e+F/fDqF9bDmz73ODlzttWi8YGc/8dJzg9K3tzZ4fDz9Tp3/jg78uDENofb'
        b'//Z1jhxo+8jFufaX5mbRWsZ/N0xOa+24bP3el392+tx+3Pdfdxv2jOwLCvvuh35dl9X/uPCm/VHVGfHe3XPmv7N6+/eD//ORx7d/t353mvy/b7xtoP3Jp+s/+dXno6lj'
        b'ab22Xkoz8X9SS3mjzfmPlg6fjH0Y+NvdH+a/1Zv+6z/57nrxcpreoYOw50eDUTN//seLPd9/r/Lqx/6/klX80OvtgYVzP5F3qN22+zPlRtXrf69p974lGpv4R+6NRjNr'
        b'3nWC46w+mxBE9cK5pZC0lqsEWsWYJdw+aTFMdyeeML6kSkAzTPC5jUqsnBtf8RoaZFik3Jt/RhNzJVAUr8D7b6wNnJc7f7bj6GL2Y8UR3ntkAsOQ6+7hKsGaZeWESFL2'
        b'8mtUlYEZPmEvBYYWc/YWM/aI6+Xza1SGbJjnkwlrzaXJhJiTxH8VH72d1A5opCELFqvNKp/kHVMnrls85jgSQ7s0l3BvknCtJ5JIlS9K18x6bfOF6W6KTYiQB/myKImu'
        b'yhZensSUis7JcTI7RdDn6SuUBcmAehfmT8ImnJEmSIotj8GwtGsD3L246I1KhPzFrMxZAqy0zO1duMsK6MKUjNViAV0S70Id22LsCHa3gOGDBP8idxLNaeLNWHA5RWh7'
        b'lA/5K6oJQ5sNDIhvYkuwNFU1Mol35MVtXMwkvXOK9/HtvC63PBH0QoIY2uRgVKi/Nw69UE/Dsgq6NvJkOrSL/CFTn4cCVOvSnKTCephI7y5dv8wjiDZWbsNCS1IIsYf0'
        b'w0KCh6claV02EqwWQQUPi+Mp0OTu4YXVJitidXQu84Ln8SF0Y7c7jmD9kvrlhiMCJAauaQkK8EEcXqo1la3LAzGY5pwWVF0zLJHquqwsMo92JyBPla8n1aW6XNd1h05+'
        b'Vl1ST4sFbTcWZ6Tarskt4fRKb4Yu13QxE7J5XddAnkc5+42BjzRdbIJh0nWvmPPFVggvi1jHvcfqrMydfKTqYh1mCNNMwN0TbCAhSCnLmVxSxwxJIgxx/EGelN3Dihnb'
        b'wOwlbysxw0tzkQk/C+aGBS/XeC5BuSpOqeKoyBZuiyyxXVaR5i3j4eCkigxdpCejgA1Wu8RQQPQ+LLCIViVSQYWSjZBv48p30L6maegkQ1spxjke0mfWQx1fE3IXkQ4n'
        b'j23EWKbFCpp7U5ghsjcch5iM3KDERCTejebx9CDW6fNFZ9KshBq4BEjtTRJSdit28C7bKCcVoSiNtScWkNIu4oygzRDrZKDpXJwQ5ZrAvGT+GW9LEvp0Iuv2iDm9XTKH'
        b'YG4b39AgDhag5bGSpLrYwlcl5UuSrodWHgrmkLmTtek6sBYLhLI3ylAsxjafJGlGsaoQqg5jteUsCdheYqPzJ4RVZEMNtyxNmmy8Om0+TXot9vODb8HSqzihftnSUxpn'
        b'VsQ+MXGzcguh5PV8MOvKZ2NlZsowJop0nyIxjAdBq5n6f35L7JGH9/+wffbyKHhIePiKKPiHTJH6Zk7v3Sp8A2s5vqnJYjlrIZuYFa3WF2mJ1ZbyjRXEYr5ktViaZ0y/'
        b'PdaMRUkiI1r+oyZR4EdisyiJBD+1Al/6WoZ3ryvxRXpYYWwNfg1qIjWxFt+sZbExy1q+ZI8an+usxpfL1uBj9qvEP5eBQ+qaVxT860uO7yQj5nNfcnknrVvprv/PipPL'
        b'C/M8GpifkZ/MfGlu3tW/kX4rUJYWl/xGrv4M7q/Wzwq1LgOBmeQNhcVI56M7lmEygrrNyXHLHF7HOU64UCV4+BWlHn4R7+NnHn5xrmauVq4kVztSW+rfl8mTy+JuyKbL'
        b'sRisL3ddlvfvy9yUXebf9xWv4t/3vyjNp17p3ucd3SFSR+1SiPbpTvPFJ1beuUqR+pyXDWEpdT2HhSSs6o8MZaEFY74XEfMdPj2Q8Dw+dha1WHVW88XlmRvz96p4d+ji'
        b'OgTntrAkFqmgpScIDuXV/dvGRxPDI+zsjUNDkniHrLDhpIiLSRHJEfzY3yz0zANQGo54vNbSanEEGn71jGOpl3rRR8/c4l/lxv0mTtvVOwxt8EpluW1Xd6u4M8OY72HO'
        b'+pefWBF+Xhl6LjFTxBGRaiq7qbxp/S0s3G+0zLPIPIaY5+27wlGajj1MtN+GfKGV8hRMHGYB6xkbIV7tiZW84XvlopLW5xJTjtMIVlGVNxUaxHwarOR7+LesRQzfIOZb'
        b'G1Kd2BjjOAFZFtDLtOQ8LPVl/k3StEmURia4n1qRmLvCiOcteIm/KnYfkXbqVpPI4wRLDaWV4ENPI7wnlAbosP6S0xBzAaoHgiMCxHU+gvX9ev1hP/7rNvFp7k2O2y4f'
        b'nhF77+SfZISvndoP899+uu/CrV5JryxnHHwmQ1+X452fgeo4ZSfDOqQbY4etITTyTXwCz2DWcmc15lm5EUQisZw5akn5dJW6v/mOS+4nXNws3aQq3gyWqropWPOu8lh8'
        b'ePMp+QPLD5AMFyF9wNtJ2g3U9SZmu4c7PKr7v1T0X1uR925qJUDGkv8S26KEGgR70nnc2QKVdk91FpsuvnUCJzjmKVG8AZPYxEOoylK8s17EFzNXMb10WurlOBwrwK/4'
        b'5ElukuNMX3XMSK+7/rbsUltS3vttJiu0NoceGeb94NI4GLyQBlXG/MdbSOtmqh0pdo5m6QSk20LH8+ZDWGbB31q8ZnAVO5z4Tw/rQzVzfnAxrDVxzIadgqNxBJpVsDDp'
        b'ElNysZCsqN0iGMEmbd5l64ntmstdnMy/aQDd57DoAu/C1IFpqKLDmooTtDZexz+QGvNR0KhschOhmtNQ0IGyA8k6O1TubPnll++89eWnEdpJ2Q3mu446uh6T1zke3rvT'
        b'7ONInz90VRlO/2RNpoWp6fytnA0vebc5nS8x3DP+tvNPLVzncrLfdXoz6NDan76vJPePAq0/23x78z7YuH+wq8b4o5c+H4nYGvLi0Trbk3afbN5ca/ZP73/88Iugycr6'
        b'+zvfden75JzMHb+yH7aFRpncFN/+y59EByW/0fzLiMxfDq13N+8x9/C/rKPa6Of7hc0bf9+nHZ/i993bVmnNn50xv/yz0flMr3MDv+/oOpnqbPfav3sTYn74ceeZBrPK'
        b'L97Nu9Hx1lTNW/Pf0/7WQOmZ+gmHBTv5De7W1ff9+7u+/YsfbN/96SsPX7M6VRl0NzJdZJNzNTAuZPtYxQfDg29X/6Fa5V3vWqvZ9pqfezv9pa/jvQbr3a2VN81fa+4r'
        b'+/2m8D/+IKXtX7WDPz3SdHmnwvhvCz5y7MhNFEteCPdwv/9K4qRCyhrDhNdTyxK1zyR88IsfrvNUT2m+Fef/kwHTnF+uaTzbc93dMP1ffu1eHpn/zPOdrPn3T3L+PvsL'
        b'bv71F81evXSjwPqz4Q9fuSVz69963LnarabyZrq8cn0SenDE4uh2aZoob5GOk3XCzv8STLku2aSE0LXCBUXohibewNyLVRErckvIhB6V+hcGMFvI7Lhz8vBi+QzsdeJY'
        b'/QylTYItnBUf4Y7DvnxRA95wxcIIwersgm4dC2jEepaWInUplF3mrQplmISWR9mj2GiwMucfiqBNcAK0puEQYWc55C1rQ4ndCkJdURXHZU0olbHRLFgixhx6ly3gIhkc'
        b'9y2wVm15n0kjTWHcguNQvdR8R42lxLDmOw5KvFHs6QNVFrQctikRTnKK68RQBvnywr56sB+yhQL/WLKL4yv8a1vwtp4b2aqtWAizirzFvsJaJ9i38ScSlwDdzG6GXg+p'
        b'L0Z9tyQUis/qvcAP4rgVeixg5ICXkKJIDJQEhYUcRzyYTMYX/PgjicQCFjXk+/8FhXNyRmIZyLIXMnVGsFrb4pqz13ImyRuGsKAtmKR5l3HUAu+7rLQOBdNQgu28b+cY'
        b'2e99K2xD8c4A3jYkA7yZTwI+QbZc1grj0EpP2rGCtw0dpZlBKQbJi9aZkQXZZ2SbQf/l/1Av1/4/NMYes8hUlucQ8CZZP+Pw38wku8VZq/AGkpK0E6WC1BjS5/sH0ScS'
        b'+kbMftPgjazFv1nXIdZxiFU8VeLNqUXDTYM3n1T4fkTs/pKatKelDN+DSInPdmJ/phs+fpVg2X6kNpWcYM2YLFk4zKxYZkRp/G/D10xm2WTmSzPylhS7S6+kstge4ptZ'
        b'UmRLbV9uSz1r74s5W0psIcrix+wopofyOijTfIT7FNJmAWLelpIwaypSZclyknmm5RRNlpPjajmsi5bTo44BSympfCbr/3IWtvDOYuUd4b1VCmVaGx8Vkl74pTwlmYdP'
        b'2mbmFT3q6uu9d/f2HcyciQ9JYSkbySnsiuZTlyCU/HmUwPJ4KUPh+298/0PBS8jGaEnjlul6Wp5PtxL4BNWcYCdemzrA9MfysOUh5U2SACwxFcLNxVgmXownb7JdLGFV'
        b'7M7Hk7dhq5IZZqyMWPPRansoiQk9fUgmOZMeG5OoWxWMqbIWNZ8ENWkc/RGXt0PD/UVOx/q4ycZw02a5Pd/V/XO3vtlrb7167cOdL3u/fLb1B9mhiq+d/+6erJjXN/3y'
        b'u7/1+eW3v/ViWtF7GeFt+965pPEbz/ne+r3nIh/E6kzcMKsZHi7W2P7lX39291yYxXDoFzd+Ex9r8+rpK5kL/+YStmx6C/TMZIW4RBU+PGSuYLFMbYjAIkE+TusfWEpI'
        b'haJ0ae0BXcFtCOWQAfnK7utPPlGRYd0+oWZDL8zaumKD1HW9QhBuBiEsEpFMygHLFYZmGJX6wze7r7g18h9JiGUMXC2Vp7EVLNzreVj4LW7t4g0ToZnwIhtnzDp93WOs'
        b'ZuWsKxntSr6zjNF+sxLdxEX595VWslKei5rTZ2nPzUXzTZZz0WdvjdWoTY+5yBws/yv1LBdvpPU9mUaaFBYdc1la80haUndFlaVV2ORRwV8Rl8Y7OGLiL8ZFMBdNRPjG'
        b'p7JU6WYer/xDH39VIxZuVaYk45XK7tRiB/RAlRBbesz+9JKRpiux0FGonkJMONTE/PeOQREPu0/nmz4Kfjn0nZKAF19/abJszKU920z2Za2w6Mi4UMuQhMjoUI8QoUBr'
        b'z6xCsekfzWR47TwAZ/ctkrfzXkbgxtKM8zPBmLuiZslGzCeroBybhCr0nduxe+nqWA10LSPxDckpbEnQdhGakF0jxjEsYr0mBX+Mq+clYggDZKmyN9xhQB5GsRkXvrKH'
        b'm0aIcLaLSJXMk+ne5yNTe0akS0VEl/yoj82w8j6NxUpCXKWKqMWSr9eKfqtntHX4eWgrg/tgxVXPr1onKzIh6+Xl5+RlJvYS/tf4ivJ7j6qAhLA/9HhOw35jCem8q5rX'
        b'sngmwe9GAIXB/7VW/TVZdpI6/aqmLL3spqAsIzY2Xl5bT0NDRWykoausJNJdyzgxJ9p6Q0tknaAlMt7AZw7tcLB57MozoXGHB4vzmW6TvXwO81M/FbOMKUV5kj8VBxKx'
        b'cbsG3MEZnFuzZzdkhOGInAPmkairUCA7rBlvb1CFMjIuW2EQKl94AdqVoQIKRIb4EGbwoSrUO+AklMB4CExhn58qSynKwpED++EhjLrAQ2d6qhQL0mAG+mDQ+jqtBYb3'
        b'X8d57JHHUeinn/u7oAs6sDvqku0WrGeNjNoSoAWzsQ/HsfH6ASiEbqLSMT3nS/u9daFwE2YcvRFrh8U4DzMx+/HOBee1G0LWOjm4ywbaXrP2ho5AIyuoxKn9MIs9MAFl'
        b'CdBPpnQhTLvAtH28OZbaBmGRKnaH46g2KTWtUIHt9DOHNcFHdTdjw3G7WCgOwyE5aIFpvJMIY1iOLb44BKNX4rETHt6AOaz1g3IDbL9whgDcuWcNDrvA3Hay4LNoqhLN'
        b'F2DEF7K2udMSprFhL4zcwIETUC/CbmjA21gFTfR3aTT0YgO0X1kvUYYqspTv2lpiB05H71Xaj1OQG2YEGc7xkB1Ow9Z6wgOzMKfEDU5YEoMPsdENqwP1YeiqI96DcTqo'
        b'0QNyUHfCzJ/lSEE15Cht9cMJfWzDdvrXjCfkQlMAgaMaai1xZu/BLQc262jj+En6oOnatjMWWI/9GtqYi2Uw5ZdMn5arKZngAr3Rj2NkW0/BKIe1dhH7sP4sNNrCAy28'
        b'qxbqCSVRKQcxwwdr10Nh0G4FXIB7RtpwLw4WDOFOFL0+eJFlQO0wwvZwk5OnD9hgJWHCPehODiGkq8EGPxWDs+kJ+67hpNG5ddDgBe0GZ3CE4FOLvQq0mUnCqAZsP4xF'
        b'CpB7DO9vp4OsgQF72uUgrW8GsgLoBEqtDhFCFFyFcT1DLCD4zGGr2k0JPsB8582kcOWnFhLah56EbGj2cYQSQnsVeIATa64fptPtOQYZ64mt11mp7MRhOp8xaJEcg+6w'
        b'kE1mUBYtA4XGt2yga29qerQ6VhMytmMvQbboYvApmF8TAA2HoQHGoBOyQrDJHGsttuI9vA8zEhhVxCpDnA6RvYjNMOkfeOUQNt7wjYMBbCRAzJvSLgg/cCjBfR8N0WJE'
        b'S808HkBjVwRA7R6og9xQIr1Msb0nVsCoFT0zTkpm/40zN7Q1Am6F7nSOwibNtJ2aOMQKRREqZxFV3N5FZJXvvMFjc9pWQrVSqMfBHYTkA4Sa9zAvBCvi4AHt6RjOQb48'
        b'dh3EimtwN9XdMQaHtmGuKVkKC9f3WN+CO+cVfeGe/npWEw57NPfKJOJCMI6LseyqbsgxzIYJJSi66QJ1mGnkDCWBkIE54epwF3q9ff1tw7S2GkQRXvU5OivpaFlvlzW0'
        b'8ycaavbAPF864Trs14c8YisZIdi9m45yDm5jjgQrvEgejxljkxcWBGA/TMhosvRIPWinnTDOlBNky4ALeTgIk1euGkDxeppyiJCq9yrhQ266pgLRw0QkVuHsdVsdqCQw'
        b'ZtPxjBLnmlKIUnPDuwYwjK2nT5K8roIcnNlwDuY93WEBehQ3Q0Uy8YRuuGMfgRPxmB8A89Zrmb/urDfMGLJeX1jsAxXubppnr+AUzddNuNByBjJppwu0rUxbHNDe5rt5'
        b'jTdkEsynArErjqDX6w3jZnhPFupCN0Pb7uTU18S8DztrPyHkAShlCEmrnrWAyVR7bDorQ6O2YnZCCLReUiayrN113BK6NYLdoe8gFOE0Xxms1pAQ6SEU0MbGYcQV7pwh'
        b'as0xwXmXgwcPYJ0bdIRrKGEOIWwXodQMZG+CBuPLhMG14oPwII3bbe2KlRdSLOjcJqCb9KICuE+UU0Ek1xh65lwC60NliY2xrIwcR5hUQKjaDx1Qg1VnjxFPXLDQO5Vy'
        b'7jy0etIKO1kDN1MijfJDJrZXsUhHEWaXIyyRR81xA1rH1BXMslK8BZMJPLusUkuDeuKT3Y4eu9M3hsGo17XrupLzzlCoB5mRtLEFGqCb+FLW7oOEvnXy8VAMPUFQqUoH'
        b'3GesCpV7sd4FWlPokUxkO7mLLSSSeiBDXYxZB4iDdK2Rh5m9eF9/K6HCONy3xYc6V7AjYU2aTHQca5dH5HoHq9QJUJ20vW58ABPH6XDaNbHADFsD10UTsmXh2GHoJKg/'
        b'OLuNZNNw4FUjQt62+ANYFkwSrNYM+q4QSRRZ02m0O9oSl8sntCTJeXbnhV1YbhqLvTeOqKXTGrPIjiwldJ7YYWwaHgITxHBmVHSwEu9jlgrmOUGLrR+hBLSl0RrysdQU'
        b'pkhJHYDSdGyXN9xMcJ7DTqdAG3iITUpO5rTnO8QiW0lsN74AE85RPnSWE3A7OZBOtJ4E4l2YS8fCy1B3Tj4Caw5EOlvzIr3UPYWkzZ1U4gpl9EzNfme9AKyFxgtQIL6s'
        b'D02E3gREQm9oOR1Lq1wgk35LopsT5ieoYnnEKfl153FoLdQy5LIhcm530iR51pH6KmG2GcsAJk6bwOsXD3DEAqdFx9YHQ6s81vsoiWCMpe6WEM3UQVkKjHPEbTevwYwd'
        b'BN86o2s4LA/3oTPC2RQajsKANgmDBgN6vEQNm+TjjWIJbRrUiRbrbM3wob+1CzSeuIZVRlDktn4PyYEZJQLNQyyUPw59wYxaQkQXzzJ1qDkBR3Du3CniFoz/DhIbIAUk'
        b'cTc0ah+28NHCkUAoD34Bbh+D+xrY6nzrDMGldc81bSjy9QiEvi04eWvd0WBiG/10HAPxBJQBaDyTJsIaJzuY9dt+Te0oZkIj1B0MI7F8m864XV+TgH0HOyWwoIkV/noa'
        b'a0nuFehA2TmPED8i3Xm7Ew5xRMSVAVBpDVkeOjY62BsHg4eJ+PJioWor3j4qwgzZ43A//AhUO8XAxEEvmIO8I/ZHj91ci/WE/cQUu2i+XC6eJEA7jslBK5FBvi6RyziB'
        b'qhSbbGEeigyISpu2wNwNnL50kFC2juRcCdbsv8Ry5achI/zEVbjjnEgU0HoDam6sIaSaCk/Dvih9rCMO2EZsomAfFp/S3I2E7WXY6UxaEeFzl/EeWkMz/dZxeM9VZw2S'
        b'iS+shQlfQsIZmEzbSTQ/j/1HsYjAlkMS7+6e9UwfS4KiSONtDBGxXOcQzwvaaZkZ0BIDNaGa6Zc9sQlYU8hswrGKGFpNH+kDWWIoSSXAFxlco+01kvgcIKmZHABt1tiC'
        b'nfreqr4kJXpidbEtAqtd6Xy7ce4sNAfTEocPwjCRcJ49ZCMj83ms8achcs9HX2byBzPjDXDiIrGXcczZDH2WTqeVcNRwh9OJdRegN7WceUq3Xya0pj0saRAWeE8UjyWk'
        b'QRzYawEz22H0svI2e/kkUmDrnE5ixRHaC7Q60gnP09QTSQSlacaDAkzgjh1m7QgBshKJ8Y5evHZAZb07zONIKN6lZ4aJd9Te2gAZFifpuO/J7CVGWAOz5rsP4cA5UtCq'
        b'cTaClMsSqCKwFfOFW6eQWFvWLSus0iLEzTtyDlrdsMbnMInWsojDUO9vTmpHJ8w50IwlpJC0wgN1Iu9maNPAPhco2XEVK9Q8N0TFE7PLlCcSabmmFASjWxxe8NA/oEpY'
        b'NgjValbrZAhwzUpa9ji5YauCxAlvbyRYZmwhzO/SNCQJX0JjDp3FrHNQ5QjEmg6SHCTuREoC3g/CJmzZd4k4VjX0kDjpJFV/lI5KdNzqJBRuSSA53QiD3ph1GtvPOkCB'
        b'h6UngS4L8o/GGno7n2BqTMG5m9Adaoa3wyBD+5ox1pLAKj+D00kEh5oTOBCMeVbboVZMuHbXA3MdCcMWiLMPRZ0jo6SMWHe+gT6BeTIYK/dhLtxN3Evg77WFOwcJcTqx'
        b'fEegTuRue+9Q6AzGe4lniS+37lNX2mK3R8fAzoyY+qQK5mu/4LWNxOHCFmjyp1ErVAm7HsZDgc9JIpP7Z6F1K3TrhONYAk3YSNtsPk/E0HUmYg3xnwoYsoYRZQJmAdZG'
        b'Qf4GGD938bzeIeiPo4eGoD6SOES9JJZWleFLOD9pB6UHYH4bCdxZzL6lgw+5OGy0IGSYwurUnzN3V5A3w8rMBB4p5wkpr+JABPamKZDSk6V9jeCXuXUdKbiTRtu1sFKD'
        b'NMlTPukuUHZrw5ZrqXAnRP94kIoPSfAO9gNZu4jz1xAjodcOMKXpuoYqDF6lc72Pd08eUiZpOQ0L6sHYhfWxJG17ZDEjFav9ImD+WgJ91WgFE6HnSJsZ5hUIIAViDuZj'
        b'iAAmQvUxJ2kDdpkSXrQT+Qz4JWD5dWPiEE1M4Y2mNeSdd4jXV6Y3yol71BA8Cj0DSdPrv+F741T0VRMVLySdtQO7TIh595w9eFWN+VuBkW8Z3Eu4eFALptVTCDiZSaRU'
        b'lAV42SluxtFQL7wNNb70yDRky2O/agTmnWBNW+nj3IvQoE6WSja0XMXxIELVURsVCzdiUfUxGk6xaQfJdmpfR2Q6Qgyn0NBUhsBZvZ3UzTI9HahKMN5wjOh1cB3OOhPv'
        b'KibzZJIk8v0ElhyPFZe2YPcmMm/7MfsGNJhaEQu8J0+TZWG3nXOE3dWNZyOJ0jOJGrJSiRAalKBiB5ZcsMNGjy1ECxPamsmhxAIfYP9p7D9HZNO5kVCwaQ9pLTN2kIv3'
        b'LiZARwrZ4HlkK+tt1yGWWXuI+PzEvk207LJoKCadQRZ7/Ula5hGmVh68gFP+BpgjQ3xjJILmbSZsa+A2XTlw8XSy7nE64jETcyKXZigPT4Gmg1ehYBPmy57Fwlio30/P'
        b'jsMkaZ21mH+SBEUhKSZNOh5qcNdt6y1vwtBBHE4PjCNdsdb34LE9zDQbsIcuxyTzszBDWFXqCWPXYnQiiQHVqxOCT1phx4nrzljpZE4YMaxngpk2HrH+xJ3Gos3k+FyR'
        b'DThu6e4qG4slnMiGw4IdlkKKUkXCdXcsloRApXCrB+pS+Ls1vmdw0t1CnKLNiQ5zpGA0Qy3/ebQH5LhbyR1N5kSH2OfZkMPfODJjTTeZR16kDvOcyI3DRs6Qf8NFLQgL'
        b'LUV0uj18FlSLrnyqi4RVpMojKm8mYVRMNNFwWIXgPXJTacMZRajZ56Meok1Cqdya0KCdIFTNdPWtmO3q5Al3Yg/qmhGTmcEug3SSTG3Q4qrheIb4dhk0hWIpqSpEvHh3'
        b'N3O2kNFdftU69Sj06zL97gZ0RYRgrjK0JYUQuVTCwkHIOHUCq73oDOl7osOcY/RrJ/RwxFlz/bVIeWu0oaNqtj29mTAucx1ZAmPmgTRuKedNc+ZEEDMdIelbSWdMtk3M'
        b'dbhjTZK13A/KtpKRME6YcJpUl/KtxNyGoMKeDKSclCBPeOhOaN7JwhiEUONGZCxlkUGWZ292HXLtSG+7TwxilORAK4xuJDW4F+r3Ruy9LMFS+Qh1rHO5AH278V6SxQac'
        b'PY8Dp13XQJ/89dQIz6Qggmo5dCryV6bqjAwwkwA7QHwok/hi99nTNFYRwbMmUCeWiHWWllC2i7bafWCt0ikVbAkL5i2uBglm2ZIFk0FQGULioAu2UCTB0UBzb1vMCSB+'
        b'1rYPR7fSGfbYWQC7S9EHZftIFSql/WQk6aXKkEgqS6Y9dML8C2dIj6yEAnNokcfBGCxzgepD2OpPxlQRWS3z8muwMHhjmNlRQxxUgOpgqE4iApk3U0vFvrCkJOymn4ob'
        b'qpBtQqwsf/fJADIfh4gRl9vh+FHn65qR4TBlqgrTanjXhWjq9h4csnElsu6DO8i8OvnqZLxPQuZaaAoiFgA1h1xOe51JOnVaj9ShPMLtWb29WJVkY0c8YvyyhFhDFwxa'
        b'6cJCajQO7CE7oMxcGxv0GBMnUZe7/RYR6NQu0hXzmR/KzCuSRCnM2EBjCuFULsycgdwEkt6d0P8Cke6Q+y0YCiJzr4VOdcjNgXe9PJCQhLl7JopMqS4o3aNneNOCtM5J'
        b'L2ZCYHkkzGH7dvpjAeeNdaEmItkyRZ/VkTqI986rYqYqPhBBy/lbZ5RwLLVPzLLY9+HC404ZYqDDB40Pq1/GQV25tVewLZyIIzOUWPLY8TNY4Kaj60g2ywLUJhEs7yjr'
        b'yJ4O8vAhFlBmt5ZQpwZGDLB7h777xv0wcY1MgdwAfW+rMEd5Emj3TpzkvTPj3htokgao3E0QeaBEOxhPIH7UTsJkPhqnU2HaDEagcL8FkUY3NiXQP0ov74QGkmbE2MsY'
        b'qnbAmDkMb08kPb/FAcfDzxCU73ie1GOKJhKH7jolImXvARF1phHRz5gzCbcWGSPssSCeO4Ed2ieh14TdFYbGw0kepGK3RJHimXWY8dUxyLwRR0xqbvNew8OkJ3QYqDO3'
        b'lgf2pGsdVYL++HPEhYsEJ0ByGBFB2YUttDISZth2k5jBrBHRQvMVFnnxPM/FYu6ROOI6TeePRJFUmMCmCFpkRQqJ4Cx6I4ddUwoLh5G443twUk8DHm46TchQp4NdjtYM'
        b'KObYpxeBszGEN0zL7yfL4UESzp+X3a+B9YY7sML7InG1Im1s1yLrq/IaaVEZsHCJNJ3JQ9Cn6W16yG4zCd5WrA5UwDbnRIJ7o+m21PVmMbrHnbU0sVX7VqqDKtw5IvYi'
        b'nO8nBMyH7pvEC9pST7pA4RnitLct4J5OBFHmA6KL6Run4klOJkCJBMfo34Ok4s2GXCZ+23TgegB2BVoRY2rAATOYO3IehjZscWV3i9kZ0zk8JNZWT/xhSJO2MY8LN497'
        b'0KCdu6Aifo2zN81935DgMXcU7rFm1blBsiaHUui5xtSfEbau3ZsEzb5YuGTXnqLJi6F25wZm2gb6KItgSgvzvGBEzgqGzsjpQh8SE5zcRXgwYn8S56HAOsaeMLSc95f0'
        b'm1gRH2MOunpNS8ghtkYoegdGyTDAh1e8rczotAbwwUFH6DOCenWjtQT7IpgMJ2LtOLSfgz4DYoT9W6DeHjM2Ercbh8EAvOsPjbaBxHhyXaEpPJBkwshJppq0Y1tg0jZZ'
        b'SfR+rLHBrquYbw3jm/wwK2E7dMYeIbnQSRvuIY21yYn4Dcx6YIFlIEmORnOi5myrjaeisWvPmtNJ+NCLcK2GZEfOTh0FuBubAKPEvFpohlEveaKChYveZLGXE7oUQWc6'
        b'bZqk1VrstoHqVJIntV6xhExksNRaqiZAjpKxAw7Zx2Cdm248PIC+VGy0h/uOSVhLsCvF0ZPrYcGP24vZqgq4IKFV3vFcA7OyzCnSYQ/dUbouUHPMcK09GVwFtCUc2kd8'
        b'/AFhxAiRwAyhwfwlsjwHtQno9aFhjGwio02JpxaLzzpGXVKBqTPYHevtFRN5nhTUcTVaQgPJ2wElHHeHwjCoPWmhB2Rb3MbiWJUQHPSDUu3DweeuYYub57odWL4dx9ZF'
        b'n8USOzFTWIkH5ZAFfRcfeFy9zhpwh2qQ7GrDh+tltkCNtg/eCQtwPn/E04kovOgAVifvDcdZE+JHw3SkhWQVygURcxhUDjTiGQxj2lUEyLqwnTCGUyZmRLZ12JFG1FYC'
        b'o6Zk+BRqypN47L8YsIblIIbj/PFLdDbFSNpBmSJMa+2zJo7WkqZ9S30bkVY9sZuHtKB2S8wLgpY98TBtfDX1mIRdxSPtbGwFbpNpOy0R62Evlh9WT4JOHbnYbcR1m+n9'
        b'MeKJNTtEbn6uzHQKw3thOKFKlDVF+2+z3KeGZUan18kQkjeQBC8i7X0wnSBevdNP0R+Gd2NDAOF3A7Hu+8rMIIcBI38CORnVUKKLOb5OTPnRpsGGgjZAly0OHTNH0mjc'
        b'1rGiFyZw13oDEWj1fmhcQ+BpTCax0xMBYwFGhOkNYp+dhtBhYA8ZoZBvQ4rvAWKHG/zNDIlRVERjliKMRSTdIsmVBZOBu0mqTEQwNl4on3LcDvpU9hCYS7FeP4gANauF'
        b'7VFrcFjBNN1x/yU9aN4DIx7XCbG6SPR1Yr0BTqe4YZ8W6TqlJEXnokkapCsdTaJzbKFBKkz2pkDnPpkdOHRoM/QeVMKmFBzUiDynD92aGpegcg0WuUfRQJlQZSlv60ln'
        b'SqoGgeWejLHnxcN7fGJx2IR4Qx+RUVOwCS44EfOqhWZXxwMc0UYBESbp3sS6KmBaORJzd5F4JiwtPAqjaxVFxAxmgs4S2+uiI7lHo+ZorjlFUrwYOhQgOxru2GOfFfH/'
        b'vJuXoWLvWWQO8nYOJs7vMySWch/uxGwjUuvRhzYrovN6oopRsqebghUNduGcHtT67XW/6EwStBd6cUiGXrkNE8Y69mRudEC3I/TLGhE1NcHCljUGpMwWm2PZdSxjoMm/'
        b'AuOSi1v30afl+6F92ymcJVGJNZqb92/Glr1QFxFAeJOHNUkkl+avnsGRnfv9ISsuhThjlTW3G7pDruqEhhLU46JxDopDYfQSqc/lpMAVE7TGHIix5my2h5xAsghnMTfJ'
        b'wT3yAPGCPCy4ZkXwHVcREfL1qzDtmM6yPjz56g24503/7IAGDzLP78LIRRccPsULxkmc23/mINSaktAk49f5AE66kQI3ohy+gzS5ukAijgX5UFLXMkyccDhVTJR0kRSZ'
        b'UkZImYTPjJLmcc6CuHEdoee0PU7qk7obgJVKMUdhYDM2HrWBcgkJuFZV9sQBjRgyFh9ci3JxIYUgy83f3hjvpCeSij2PPY6EAONwVxEf7JaPI7kzIMI2X7y/5QZkkNlX'
        b'vdVJXdkXa8L5uNoQ8/LfugZVcJ85tDpg1oe22BPBrSfSnWCWGMtUdtHF+jSfbadtWJUH7N+PmbfI9JoyYiVvz8Jdf1K4pqzkohNt9WHURYlIf5AeLLYlyN6JIzKYV8fW'
        b'c5BDKsEoyZeSHVhmKE+77FK0wuHr0aQE3gm9CtkHSC6XQKsEx/UVsfGkvpM+4cygqazGOrx3yB/K1A4rEOu8jxnOpM8MMMa2C4c5kuDVWLpdLeI45JxxN92bEquE8xqn'
        b'0rcRlyfV/GD8cSi9iJW2vmRRM010wj76OqFI/jYY1XRwJzJu04P7SjAdkBZnjr1biHHNYCPknMf7V5XwzjFfIo0cMk16ie2Uk9mykcBdux6bVZQkkXpYeDo25lyQHTa4'
        b'q4mO6dJ7Q1AuBxWaekRylTATq+JqYYPT65nvk2R3BjxYCzMsdtdjtI7MvqLQQwdIf2/ZSbBog+F1VglQ7rGJCKOErJ/kVKjfSWdwxxWn9iuTBj9HqkHTsXQ9bFe5KUs7'
        b'qHCCBm3F60RzFfSvcliwSAhOg5aNZFRmae31hil9aNLYc0DlCt52wxyjIHns8YOKaGiBAUKjEp9A5i/FnlTm7KKTnyPuO0qCIgs7rTHvZtBGktSkBJ2kZ5u9aDO3T+F0'
        b'ujVpZtBF5FJJwjpPOTA09TTR5F1gAoV00s7dtLeFG1C1HisiSO2eukTYMnRFn9Bq4Abm3oJ84uSkfNwOgNpQmEl9izSljceYT1hKBYeZV6r0FMlhYmGxh4x91DdjGVHA'
        b'qc3X6Osmg6gwRX3sNNi7mQ53AYejYFDeJZjmmCYdqUu8G6cNYQF79sQq04ZysDUFWPA38/R+qJCBGn3i5Q+uYL07tEvo1264H0HCpvcmscZSIqYqOopypfXY4UasdIAg'
        b'X4QV18nkmNuvg/m7Yc4K2zd7YmEcC3K5Mh9V+HGCTc5WYir5KjLYH7GWsH4yzZiIfHaHdyKhW6e2La2tYrsu1mzaYIaNW4+RykCUcZRwYV4nGqdUsGHfRnZBvBJyzkLW'
        b'UZw9DAOKV4m5VJL+U028uYMjhL8vB81GLlCrTCZC13Z1aHPcAfV2pC3k6Putwd5NO+XkMO/EUcxXxttHj5NVPGdNKlauPY6pX8QpGxV3W2i3w0pHh8MElAlWSmGIVLh7'
        b'xDCCjTXYvatZYgSzkGlMmD4kIsXs1uUdhGyVPpCjzOPEbBDx74ULW4kZNGFuIkGtmzGBqe2kfFRGRkPHXsJm5n+vxAI9nNhNdk15FOTJQXu0MfTKwMhBB5xm9jlmnCDu'
        b'NelxhcT5Qzs5Upc7oMgUsywJMCO60H4DajUJKfNMWBxZ9rrc7ig/GrlqvxrWkOYgd4XpQFnauxLI3CN1/jbxh3Lo1sb6F/SusoQKX4JcA9w/f3kL9FvBAyfoMJOF+o2k'
        b'XzUGQN8FsneGoMMqiDQgktq7HRJ3wn23bZewfQvUuUG3xfZjOCFLIqXWdSMZtc04voMEXB8jkHpfrRfsSMMesMYF/83E1mp9gtWCbvitDSTEycOMXR40R92mAxss1Q7f'
        b'4EjDzLuAfTbYbibmXUcH4PaR5JsyrFyNtFbNBSgUahpNEaeug8ag5Edl1u6qmkl415Uxlqu7W5IZDOOcaC9HhzR+VGgl0EYa2pA7lnBOJIxF21klp24f/oYXSbBq5qTC'
        b'fJkNMMaJjtJrZPbV8DekrFWhyt1V1sda8JCF75f2LIB8P2x29xZjkSonsqVvNkINf/2JEK6D6YseshZYxonsOaKUXGwVvuunM+1lrjVaTqPgW/PGYhqSLz6b4e+BhWay'
        b'UZacyJvDdico4b10KmduYKGnnLsC710rhwFH/mOvTbwzbk+04IyDAjUzEb80zyCccneT3YjVnMiCI1g3Qqaw0S46hjzeH3cSegR/HOZBrpnIiW86xN8985EXcx7+rMxd'
        b'cFzBWl3OTCJcSTsv4VRclNnHKolH44VaPRleEu5NZ5bVHmwZGriBY4lkTvxo/EW1mH3qfZLkl4hjuW8zuVF5ytvQUScn6spbHwSHxRl/Hvri529fy9Wp0NcyyUz5rc7m'
        b'zs37NRQ7TQtTrnxW1bO/7R8/b1o34vHK0fCYqb+8+dlb9nYT//rF3/74Sn2KQ5zkOzlffPH6tdx6n0Grc5+siZXZ/4NfHP3xzx9a+H+e867SO51Hwn/x6vtzow+bzhnk'
        b'vfEd9U091oYqv/tn0z8ttHf88k8/00412PfnbffWmSZXdxxv8Uuot/v8ew7qfzLYr/4/BgdLXWqNfu/p1/qp9bu7352qOmH/8plepx+c+9nQsZIvOl/x6Tu2rtrtRAs4'
        b'lMjUfxi6sN7157sGL6QsiMx+7r+322fbPr+fRv82W67p+PfcJFNcw489rP51Yta1X1JRdeJDx/2Oyh/ct9qy9QuVD05OvnXsx7//wxs1FxwG7muHj5yx9TF7LXzCx2KT'
        b'7Xf2+45vPjPeOOK4z8El9fXu+Ht3Jj58pXyi0/WNzreiJmxf2aX8s8lXvi/3vT9et3L4ybHx72/63ulPqs98/JncqenOs9+pmzA8kPLFX4d7P3aej/F4s1DlmsH8ZY9k'
        b'T62QPd+p/v4Xb/jvHxj715GP91Ye6vzxB13lVyqdNvzdvutXu9/Ke3uq7bM97i//6NDxN1+6131q57W60jAusCJwW+gZDw3zNvx3x2ep+t/S+MXGu6pfvhfvmvG3Xxb+'
        b'7cvw0c1fjA9eOJgZUlS24SfX1F0Kr+Q+TLba8B3T71ydM3tQfvJyeuepra/Xh0QZaf9jvfmfatJlF15x9Rgb/stAzCtl7r+pSl2w/LQoasd3b8KvGv/2o2G5rpaPrNKj'
        b'6kde3K9bF+X4nuLfP972ymun/3FH6S9lxl9c1FZu8HY9vdt+S84xy0v/VbHndydDDCwCvr3252OZP/hSY3q0eN0fQtW/vH/w3p4fdfz3rYujw2//8+Gu4V9eennm86G0'
        b'NfM7/jpyq8EnZ8Yw+fw/la6XvKdz4Edu+3+0Ia176r1j+e+9X/6e37XzNVfPH/j0+o/SfhTg5biu7/3chf/59amtSbpmSsK9tfv8LSkPEdkTAzyDKYEeLz5BHXJ1sGPF'
        b'vbco6JDWVO7HZr5UvBHOey9vcaCHWcsvqSngKD+USuhG5SRVRVUS+4XqSakqJKtnJNx1qDVKl1HQ2SjcuJrCxqClp67gtA1UXLmkKsfpH5bA8OaLKVvoIcO12JOMsw6X'
        b'VS6l4ow6FECRuoKqEo6qX5blzNRkSLI2OqXwLSrKvVWSV3kMimloMoNy+bE9ZeRg9sY+/kqbGgwdVFZwjF0cTgF7xDbw8GwKS0ve5gg5yVCscIlWl0yyL3/lePmbheFw'
        b'So4AOZskVEipcrVeUSEFp1SdSKYvq5BC8v3uk61u7P6/zTD9//wPMyOe2/7/5Q+hjXlQUFxiSHhQEJ9y3U1/cBZisVi0U2TMXy/TEitIZEQKEjkx/UjUZLW0tBQ11mvI'
        b'a8hpKeloy4h1XPVNdt/idopFDiz5WkaG3jW+xVmu3frC/1PctcdGUYTxvdu73h1tj7bSastLaKWP611pS8HyKCC0cL27XhEQEXW9brd04V7sbqHY8obyqKVWEJIiDxVB'
        b'C2JbWiggGGdi1KhE/zAmE1//mPhWjMSoMXG+mfKI/2lMyOZ+t7OzO3f7zezN913m9/ugLE012fmybHkK31tWwcu2e5ZnzU0RnWJaimeTkFPFj/rM+eYCs4uiK6GY7bEt'
        b'yQpktqzbXprn5sJlUXsPbufW8u2SO9/Vd2yImbgx2EJqMBHkINSd0K2fxG/PDnUvPTIP0ZiwnTq+nXg/jYd3B/1oN+q0Cc5McSwEj2p61kxRH2MShOS7iso66Fw5N6Xt'
        b'1Epp37v+A+/WjUr9tLbYMzSzzXa9YtcT65wTDm7+fPvs6xnXOlpTxqMja487v5BaB5e8MNE7/tea0X0DVyxvf9csLztw9cCxnnPOk22edUmzrpZFvnEdHXpnQ3rvyQc8'
        b'75/Ozk4/eyptbfdn+7NxRm5b5MfMhk8/NpQFX/l7vnxDOvJ9z7idk/6c/lt5ykD3qyWf2bRj1Rlbx6kVaxrLW9szvtj6bcndgy0nLlxf8mf/tdkdJzedzJ1X/qB89f2H'
        b'cnJXta/4YEf++blfy8KWtIy23mJ0j/NRf1/H2Oaf+9qFFntfpzhmIkrdm5r9pqNmTZt+fGhO4sEhVEbe+fDNZG3U0Ftjf/yo8iflobeW/pLZe/nc+LzWv6z5PzzW/LUv'
        b'fzyfVvrRMUan3x0MAm3XZxMWz0hE/WamzvsSY089YkVXfEE37oNw5ulgEJakp+LXwcnsyeF5e15MW8e7JIIPAS0f/tChPZImjlPQaTa1lSThHaBLGliGL9mEBIvZToPU'
        b'bkb6oHHfs3gnbi9KEEy4t34xbc6Rw3WStuWmu/DePKDzHkrGT5kEh8eMupegw6zNJ5px17BS1sZxgqXGhHo3oX6eDqgrmunzFtL5xuse1tJy4j1iDT5azKlkJ6gT/RxL'
        b'bT/lMc4Dz0GdnAp2Dr+ELvB2A7rDSx1or0VIw/tEdLEQv8w41avQIL7oqy6sKatDZ0pNgg0/Y06YOpHJXCWtp+FdKb0M7UfnfVxMYuQEcQZ6Be3jNt9Lg9kjcI6X+vL7'
        b'AvwUJz4jFuMr+Bzns53B+x/G7ZCCrlPMahYsi0zoEtqO93Jxqj0bYekE7ggUCgsWC5ZiEw2qX/OwOjvqmuVy4w4/CHw+L1giJhpXDtazT/agbWtdoBHnh88M4EO11AAW'
        b'YfQGC9qKBkSuQXY4EW2mPQV6GQEwuYgvJuab8dPTF7LbA5LAKv22etyHXh/hNaPexS2MZO1FPXMScf9IPKjTB/My7sLn43hgDfU1kqmLkm2xueOclHcW9VoZtcgFrYE2'
        b'8vZE1G3GLzTgLbz7u+k4GuBqb6Ky6obYWzc+awC7JZNGzj0+9Gqe1w1LDpmMF0sNF/SijqIad36CsKDS1ppFTQqGyaWR8p5E3IsHQCS7S7BRu5yoXM6GQxwdzIWl0gF/'
        b'cGyLVbC2mvDxR8cwm43GO2kQfZYxhooK1rhbDO5TZTVZUNuK5TwdxiuP42PU6HtAVbAw3W8WHJPMqP1JdJxr1u0y462uandhwA30zdPoVFK6OMK8lJuhZ0OBj3aKz7MR'
        b'7aDX04eIfvG7SkV8RF3Ee+SpjZNcCwsLgKFJ7X0f3kUfQ9DL257LUmJNXpHqqrYKpgnosk+gwfzzNMgezq2Td+d/2/+nGSLjDrgZtzIkx2EqctoZfd3OtlFMl8w+zKQE'
        b'8hbokYEmWNqwShg9U4z+eyLYjW0y50YxX6GAiGElqtXSOY1YjaZ4WCGWsKobxFKvyhRjcSVKRN3QiLVuvaHoxFIXi4WJqEYNYm2gnhJ900LRlQqxqtF4k0FEuVEjYkyr'
        b'JwkNathQaCESihPxSTVOrCFdVlUiNirN9BTa/AhVhwS3oaiskIR4U11YlUlSJeckBkKr6cVJcU0xDLVhvdQcCRO7PyavrlLpl3TUlU5VoqAFRZJVPSYZakShDUXixFJV'
        b'O7+KJMdDmq5ItAqY2CQ1Eqsvn8ZzY0j16krVILaQLCtxQyfJ7MYkI0Ydv+hKIj4c8JNEvVFtMCRF02IaSW6Kyo0hNarUS0qzTBySpCvUVJJEnNGYFKtraNJllqSIOG4U'
        b'6O00RUEM6pYXxu2dp1WCn1YNsAAgCPAgQABgDsBCgKkAZQA1ADMASgBmAdwPMBdgOsA0gHkAXoAigGKACgA/AEiVaUsAHgAoBZgJ4AOoApgPUA5QCzAFYDIrAltuEewt'
        b'BZh9k/sHA8lx06P6/ZHbPCpW94e9gY4URW70kBRJGt4fdrD/yBou3xsPyatBCQw4qVCn1Nfk2xmLj9gkKRQOSxIfsozn9x0cT+D5RbWrcGTZDdf3HwmniX0m7femsFIB'
        b'JR0EqCxm6h/890dn6Sgm7/c3RcQRuw=='
    ))))
