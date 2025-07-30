
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
        b'eJy0vQdgFMfVOD67e03tJFRA9KPrVE5CdCGKEEXSqaECWJS7k/YkHZx04goCLDAGzCGEEKZjMM1U07sBY+wZf47TE+cr9iVfHMex45L2JU4xduz/m9m906kCye+P0Gpn'
        b'dnbelDevzZu3H6JO/wT4nQm/rky4iKgC1aAKTuREfjOq4K3CMYUoHOecI0WFVbkJrVC5DIt5q0pUbuI2cla1ld/EcUhUlaKQGr364fLQ0jnFWbo6h+ixW3WOap271qor'
        b'XuOuddTr5trq3daqWl2DpWqFpcZqCA0tq7W5/GVFa7Wt3urSVXvqq9w2R71LZ6kXdVV2i8sFuW6HrtHhXKFrtLlrdRSEIbRqTFAfEuE3AX7DaD/Ww8WLvJyX9wpehVfp'
        b'VXnVXo03xBvqDfOGeyO8Wm+kN8rbxxvtjfHGeuO8fb39vPHe/t4B3oHeQd7B3iHeoV6dd5h3uHeEd6R3lHe0d0x1AhsRzbqErYpNaJ1+bWhTwia0EJ3gS1GTfhPi0PqE'
        b'9fpFMH4wEtV6obAqeIg5+E2H3xjaPAUb5lKkjyy0a+D+mTlCSTyid2b7U085kGc03OKtA8hJ0kKai/Lnk62ktUhPWnEzvpdbXpyiQmPmKMgDstekFzyDaOF9FauNucm5'
        b'KaQZ3ykl2wuUSEu2CYV4J77g6UcLtJKz+NXCJbSQEikUHD5KXiT3PUNo20iLOYk0w1sFuaRVn6sgB8g1FE12C/huklLPewZDoWx8e4oxfRwUMJIdRblKcgm/iCKHCVPx'
        b'82Q3awPZbVpCS+QWSAV24i3QiEvC2BTyKlQyEIpUkt12F30OsMj24fgwh0JzeXyF3PV4RsDzUcvJqTByLZLcdOFmcruB3FiJWyIjEBpEWgpHKNQCPqjnPPEU2F7yILvI'
        b'QFry88h2AQnkNQ4fwjs98FgPj+26JiO+mADjsc1ItuPmIrwFhguahVtTC1P0KjRvjroJH8XHoDwdnjUDRuJdSeQ6tCu/SImUTRw56SD74ekACuwSfoFcScpLSS5IMeD9'
        b'CzkUHieE4v1kJxSgg0OOLcHHknKSE0lzPtlOtq3lUBjZycN7d8jeKq7TUhvnx4M9FE07Iin6d9HUm+DVexO9Sd5kb4rX4E31pnnHetOrx8nIy20NAeTlAXm5APLyDHm5'
        b'9XxPyEsbPbAL8pok5E17Wo3CEap9PskcnplegVjm9/IEBAWLv9aYk8eUVkqZGZUhKAoh3dU6s311SJOUOSVTQTFfE1pgtv+zdhA6h+yhkG2L76/4IhrN/FPMU+5f8LfG'
        b'RoU8y9lD4MGrdQe4K2qkS+tfP2X8lPeXT0Asu7Txz5F7IrmEP6Fn7A/nbaq7hXzIk0wR/5QwB1ZRS+r8hMyEBLItNQdwAp8rS8grIG3JhtyUvAIO1UeGTCshL3iy6Qs3'
        b'yNbZLrdz1UqPi9wmV6YWkhvkGrlFrpKb5HqkJjxUGxIRhtvwVrw9PW18+sSxE8bh2/iKAuHXFoeQiyPxDk8e1KOAFXbbmJ9XmFtgJG2wggEvAPGbSSs0JiEZ7xyXaNCn'
        b'JOHL+Cy+UAI1XCP7yfOA1zvJPrKb7FmIUL+0iGgDOd0Bgejwq+GXYq1rvJ/OCdWCPMH8VpjOdQJMMB+YYIFNML9ekCe4tjvqpOgywYpCJ515252DDxWuKXC30PtfRsuS'
        b'13/yxpWdV/cNU779smXR60U/fiXq7cWv39h5fN/xTTbOpa6KILNOJ/fdmZMm1GSgvLqIgdt365Vuuo7wNnIT1nULDEQbXbWKpuwpHL5KWrPcdE0Pwq/hl5MMMFTNyRxS'
        b'4R28Jy6FbFK7aV9TyWvupJSEnBQenrzAl+OWFHKcHHPHwrO509YnpZDW/LFKpKrgsqeRi1mj2UvZZCNMXksOvojICXIe8eu4uU+Rw3rOxyfo9YKTdjXowsPlYVxmtdOx'
        b'1lqvq5a4lcFlbbBM9wkem0ifu1R0wLJDuWjOqfK/pFf4QuotdVYXcDarT2Fx1rh8apPJ6ak3mXxhJlOV3Wqp9zSYTHq+HRzc0wXgpLPpVNILrW82haGlMF6L4lUcz4Wy'
        b'q4dOjQdv05uWJEFPOcTjA1x2euncKr4b5GDzOJEiB8/QQ1GtCKCH8Ej06Hb9h3ZBj5hCTx+4Txwx0pUPzY+fSM4hfGbiIg+dEnIeH1YaIZ9biO/oEfEaYHn1pZ3Eu/Eu'
        b'ch2ILKfFV5UI34QFt4t1Dx+pLyUt9ImQOgcofAg564ljXOP56jDgaBzwpUN9EL6HT5Gt7I21GfhsEntyZ+h8RA4txHfZG6Mm45NJBhXi8A5yazEiZ8hmcsITTWFsGLeU'
        b'7J7PiHrpWlRQpmbNxbcbMBTBz5LdMAnJKJl43foQBoPcDSWtQ4ZNhXEmz8F/vGUC6/eyGTV42+inafYp+F83kXUPqMTLsfh0Gb4H9ZD98J9cJiel7u3BG0tK0wh7chv+'
        b'V9ilVzbiw/jKAvwSvgcDTV6E/0ZykzXLRk5qyJlkwh7ch/998H7WwQHkmgnfJrvxvUjKfeA/Pm6XOvhgWnEVPkNe4qksFDYBN3uA5qKlKXVqfK0U6hmDxuDWHNYFx2Jy'
        b'dBRHdgPKpKE0M94siQp3a6DNu8l+yIbxexG3IRNpq2TPVi/DJ8h1F7m+CjCQnOWm4ysjy/FhRic6kCk+mKLQtV+DmtDSqHVcE7cVREinool7nl+poNjGVhC7nON9vCHN'
        b'x1Wd49oXJFsavtBMu83lrnLUNUxf5F+FKoCiQZ4ZtM13yB5yzSgLJ4zJ55A9+DqIQztHgwhVSLbr8S0hPR23GCn6ucLIBYRfJXfD8BV8zmX737P/g1xeqGg5ih7VOjUa'
        b'p0VlN34UFa05uvF6w8Y97uObC3dvCa19MbR60fvP4tf0Vz8deb//NHJ9bPisUZ8sWvnGC8aJ9jsPb+2OPzEyJG3dYefHGTY0lVw0tFw7NEnxi7Zlw3d94Zy2JO3TzZ/8'
        b'Pf/+2ti1E/sNnrRgwO2rD98++4uV3x755/1Xx3/7Td2mGx9GnrwyZv4/6oBgUooYRm6NSTLoyTbgZCp8AXtn8OPIabLDTblxiYOcBpmEbM3NL1SiMHyVJ0eAfbxI9ta6'
        b'KV7hrUvwBdKSDCIbCIyqZeZifsTMae5h9NEOHgQiyhWBFB/Fh0AYg5G6kKdEMeMFsivhGUau5+Lbw4KI9RSuERD1KnkJH+pCOvWKzrS00/yFWeurHKLVRIkpI6NUxEU5'
        b'Ck7BaTgesR+O/0YlaCAnFPK0fBSn5cK5eM4ZFURmOZcvtN5hcoFWUGt1OSnrd1LS1LVFvJMuB2efAHWl1eQGqOud6GDqSoW42sboYATqG5WSo4CFtkvRiO8uewSZZTy4'
        b'A5l9NBeueTwuHCKJWXPTo9FIlNAnFJmX3CuKlISnk9octBOtTlSbzaGf11rQXJYbvSoK6dCxrIgGc/KmmFSp6CpVGIpFixK0Ueb8hJnJiBGLVXO149IAEt6NFpOLlQPJ'
        b'LZvX+Afe9RQ8izvX8rn5M3Ntdb7lB9UJ+z7ZcOXgtae2iSUHNvXPiO+blix+In5iTj65NF241n9qfL/0voeyxJJFJfEVB0dmJW+JXRBlPExFgjsqkV88sRSEgTA04ou4'
        b'I8se6nnGm8kLs6ZShk5OkR0yU08h2/u76VTkDcdbkwy5yYl6QzS+CHIaaQYGo1MsA4l6j557PJTrU1VrrVphqnJaRZvb4TTJ/JvNfkU8QzwtXAHBYoIQTKiyiT51lcNT'
        b'73au6R2/KIV2xgXwi9ayOADhTAf8SqL0USSXALtyQP3BO4oMeaB+bCsAUYc0p4Jg1AY8fRo+pILlvX10F5UhgG1M4uMA39olPo7h2hOK9LTFo7rg2nAJ1777TAzg2gbA'
        b'EHPTbxYZZLRabadoFf+0GtDq0xELURnLjVxC5ffX67QzzcnJjYskZKuPpeJ/zlMKZM7vmzVHyhwaE47i0U4tX2y2Hw2RdQJHThyo7QfiFDPNg9YkL5Uyf+oehCajnHRU'
        b'bG7iJiZLmZYIHZqJ3u6vbDBn1iyxS5lfzBiJctCV8tCZ5llD582WMkOi9agYvZ2rMJv5DcNnSJkt2cloEVo0SlFsHp5oapQyE2tUoLsUTw7RmcPvrM2WMp8qD4WVslXN'
        b'RZmTNwoTpUzj0jEoH602Cjpz5a6E4VLmLxcnoTKUNlaIMs+axmVImerE/sBNi9fAmlwydHBfKfP8VA2oPv+ICDWb81MUZilzmFOLBqFFZRFpZvv4hGIp8+/mgWg8jDKK'
        b'MmcuHFQtZS7rNxRlouJETZq5qZxbKWXOKB5OpcVnYJBnZS8OlTIv6/uB+PKPmZzOvKQmOkXKnDXSgJagDcvD08zD5zSskTJz6yegWjR5HgxdSWNpjpT5QDkOMOFYrBqZ'
        b'08mQdVLmN5PHIjPaUK9oMM+6pUlH+pFMeli6Dt8DVZbci0Vj0Vhyh2dSTiHg8oZxoAxdxa0oHaXjl6ZJcskNsn/IOB4BC9kPGvC43KWSUHTWRU6MUwEFIm3Q7/HTyfOs'
        b'+MQ1w8ZxILTjm2gCmgCK+T6p+HGQep4bp0RPzUUT0UTcjF+W5LeT+BS+P05A+BB+EU1Ck8i9Aib3GAvJhXFqNHI0INRkctEo1XJmCLmFr8ONF99DU9CU2iiW7yKn1+Hr'
        b'0PZjZC/KQBlLyUVJBNzWRM7DKsEb8Bk0C83CZ6JZ5f3ySbOLR4P7oWyUjVuXsZaTg/giPgACis0C0zM7l2xjo0WuTIx1cSBJvYrmoDl4f5yUezatnwuE4M3kIJqL5kZN'
        b'ZfVyuGWVS0CjxqN5aN7TuNUDQh5a06ByqVEsPgQInxOfzmCNI9fxcXKdSpqFwNtySyUZsIjcx3cJdKT2KZSH8sizHkkm3z4PbyDXeZSINyEjMpI7+AprRWaYg1xXoTXk'
        b'MuB4fjiIjKz4PtwG7P86TMP1XFSACvLwKWkqD+C78AI0e9d4VIgK1y6Xyp/AL+NN5DpMwn18GxWhIk0RG75i/GJ/cl0NYvhSWJfFgAmHpc5fm4efDwNOA3L1fDQ/JVMa'
        b'v1N4c30YDPZpIypBJSvJASbxwsSeJxvDeEReI0eAVpWCeNfGRms6aSsOU6EVMDdlqMzdIBXfjvfio2EcwpfITVSOykHMeV6a/M2ggVwKU6IJeDNagBY0gc7AWrMbbxPD'
        b'BJS0BojowmhySyrdVoO3hEHbj5KLlH5MIudZ/RwMwh3cwnTaB+gp9BRuJa3S6JwZFYZbFGgwuYMqUAV5kCw16Nw8aEILLICzuBn4xGLsJbvt//j222/5SkpBG9KAguZ/'
        b'5pLp4hfxQHjQ2RFAmdJ/sTAZ2RJuf09wvQNP/vJOS13b1EIhK2r2+RrVpoj4vyxeNH3Vr4WdK7n6meaduqe5XaNG9p1XO/razi3bhajf/fJZYWX4rHj17LMn1g8ueybt'
        b'/u+upUQc+qp6870FEzc/47lZ4Vl7JDp0xcWfHbo6t82TOfCL/le+2/fn314bNnX7u9a2ddo07bnJvz7wQkzhlA+/rnphdup7YWG3lw/a/9appZ9+8+sfjdrf5A5PmnD0'
        b'p9cqhq6ryU9cmvjez56+cfaTzx+cbyp5e9txw1ffubm+7rXqxOnjpi3IakkbOv7907t+Hvdg/tjPZ3yNfn0pY9K0tSDsUjMkjORLILG3JBdSK1pbMof3l4BYe54nl8jL'
        b'g5k8DMv/OUdSCn6OnAtYAlLi8Q43tT9OIbufBgEO1OOClLzkeHwiV4miySsC8Zb0cfenBAs/iw8BRm+PJNuNufgiyNST+f6p+LB7KDx1G8g+F76YU5iSQG2hAMpL2gTU'
        b'h+wU8BVFll7Zrbih6E42CBJCtLIQ4qkyUfmXSSB2yoDFcE4BIi5IIbws/gb/cP9C3tcqlQJkjXioMVbQgnQTBYI0/evsG5BvBJBvPFW9iTWcs19AounL5AK/RHOkgz2C'
        b'2t5TefJSkERTAEr/Gbhh5l+kJxuUQNV34XuPkGao+RMFSTPck0sz3UvOakmamVoZgSjy5FWYw/uN1MvSzPs6Kg+jYt8Qs71BaEASCdsTju/KEvFYfA1VkqvDbRPjmwQX'
        b'tQzuPjXtc3PF61d2Ht99btPI549vOndw7HNjDx3PGf6cPv5to6XQUmvdpbgaX3IgK3nlloot2rcGqI5l7LMfG/AjN/rxFxFHX35Dz7kla3xcKci+GfhgAIsBN3f5Jdte'
        b'8GmAhE8ut9NT5faAaGtyWqutTtCuJNwKp8PxDOI1oDox2TY+aO4VLijc++T3D0w+fXFjYPI3dJj8VMhZMNwYmPtUgz6xwKBPySvAzalTU/MKjCl5oEqBWoqfx9tCybP2'
        b'uEciQUeR9tFIsLkzEvgr7ogEqkJGfuvxObIvndwMo6YKqvsfxMfjGSIcHTBeY+Z/ghDIQYdCQNi1HTgazbkmwaOL//efn5uXsAm/umklVxX64ay3ht/Rnta+Vf3ngW/F'
        b'nrbvG34q9mPzFq0qasaBZ8cNRtrWsIS/tcoKDr5aincwDecY2eWf5uyBjFatI5fWygoOaZuPD7UrOK8p5NnqGQfiOyk2HTEgVMKAEA3XFzDAOSB4/qseOf8DA/NPX2ym'
        b'FUax+UdfdsCAsZA3kGxyBis0A/HOgD4TjANr8LkQsrWQXH2kEi10slU+WonulhR0hwXSXE/WojeLMxACiduyQCex2uQxShQ1KIYiQPjKp2XR/r2ZPPpVfzpU5uTjAzOQ'
        b'7d79qZzLCOkV+tLPzb8zv11ZW33B+onlF+azlrerU9M/MS96/ZWdw4AecG9X51l2mT8R+Xd+oFt/fKk6W+0KLR330uTsMdnDiouYWbx4ftTyk/sBUZih5sE0fBOfx21D'
        b'8guSeaQwcvhapJvhyZASsgM4ItmRWlRAWgtz8QVFzDzUr0Qxsa/4uHpwRL11tdskeqwm0eKWcCRKwpGoUC4W+IMGJlTLOQcFMEXhU9CivhC71SLCW2seYWihKrtzSABz'
        b'aEVtQZjzlw6qMN3nG4H3kX2kJQJfoLt0uLlIX4Bbi9jW5ChyTVlBjlZWCUGTqgzGlQwJVxRs50zpVVWrZHwRmG1bAfgiBPBFwfBFWK/oTRFWdcEXpYQvb1ioOoSKf4HM'
        b'JYrGAgk1/iNTSXesFuVlme0ZaCWyvWn7JwK5DaGXMicN3t4w4GrEhrRwxfurStKy/vu72ht7nt95rKXEVz7g+px3Y1s+++Lhz6akvJqW0Ff53Z9+bp730nfVAw+9ktAv'
        b'88Qrsz/60f3ENfWZ5zbP2HXm3fQp/5iU+dW3P0xY9M6NqqkzppX1HxT7OohKDGOOkeu11H63eHqqGvH4BFdOWqqkR/fw+YV0lzfT4t/n3UuOMKsK8SJ8x0hXaAtpLQKx'
        b'/jh+WUO283jzKHxDssm0DMiFh1tTU4TlgIgFHH4AKtIlJns9Q+4RkJ4K8C68H19AAHUzN09LrvcmGKl6fNQZScNrrJ1wdICEo/0BP3kFk2NCuXCe5zV89NcKlXNoAFuV'
        b'FFsBRSkC+lRVHrejOpjIdbs8AIupHdSp64i5tNKDQZj7ad9gzKWF+1WmG4tS/BgLmsQdhrVD8QkFOVSLz/TM5iYjWdahW72oWvkErK6LpTACfuO6IO1QCWnV4vfRHg5p'
        b'SmPMuT8tkU0qxnnUeoJyxj1jbvreoIVS5sgaapVAtcerzPnDFsjmD6GYmj8QuhdtTn5jYJ2UedZArY8obb7KnLmx7zjZUKIeDFo10nxRam76Y5y881uhGo9qgWrOyTY7'
        b'vVWilPnhUGpnQVFXRpvt2pzJUuZ3JieAOogSoleYh6/Sr5IySwdPR03QpN9PMDvPjJbNNOnx09BqhFbvLTNHf9fQT8qMWzsVuaFHf4szp/fNHSPbL9LjURpkHhDNmd8k'
        b'hEmZ15dR0w+KSi0xDx+/YL4MqJ5as1Dx6iazfX1pppR5umEmzDpKwB5zSV3UTCmzKITtUMdXgH72YIK8bd3YSI1ZKG14mTl80RqZMnyuprYbpPnjIPOS4Q0jpMyVFZNA'
        b'k0Orw0aYo7eMKJJNVDPmo2NAQxI95uVXlLlS5uvPiOht+PujuebqY9FxUuZz9mr0AwD08wTz3I/MsintZDS18qCoaIN5yd6lsoU3b0AkoqQ3fYY53GCqlzJfTn8afQGA'
        b'tseaJ/qWyZajitGMrMUf1ppLdOULpMyCphHUnBQ1K8zMJwxMQLa+//cG7xoF+Lzl29Ly5wsKSVrUc9+5+pcP3xxVEFKwfHLo7U/i5vL66Oin2ha+d2Bp20+WbNjdoP3R'
        b'G+++0sf+1vt/OdR/xqjpf1neZ+j3klJPVw65/6fPFDV/Cn1OqT5wfOQn3EfobHLDD18yHMgLGzH52YUz/uvbIa99ePFs269GLt81baf5TPXFHEvVs+ebb4b878iVNWvW'
        b'o/0fDj7HJdQYrnxU9tnfy7+3Ovvp8HtG+7ljzlc/3Vb+H/98Yfwfxkx45qudy5QT8PCl/6z+devIwWW/0d6bU/L7UQtafqXw/Kb+g8M/naGY8c60fQP/avt42BdzMurH'
        b'26+P+N74n36gL3j3hz8ca/zD1q9m35txeVr9m3/4/hsTzn3YfH1g+sJFX04t+vPwj1PTb//gR0ve/GrMhIVZ1XH8gWtxuP83vx13tOYnl2es2mG7uPRdveCm9AFvG4DP'
        b'Bjj2RdA3Ja7NeHYo2c9oNGkbVmtMbjSBaNhqhJUKOu4abjR7NH3V4iR4N5FDCg/Ijfs40EVfytVHPIKQPvrSC5kOtplTMlxpqV9hqnXYbZSsMlq8QKLFUzQCUGP4Hcnk'
        b'hihOxzZoopgMEc2HK0KBRgO5lH6ETn+lu98qBoUDNQfdFCg56KbDA3Qc5NM1VosziHT3wlk454gA1aZVXAqi2v8Z29n07pzIS1Q7j2wnLXhHjJp5ZLSR5nyYnGQVmkau'
        b'qsgroPWf66JSKOW/rmq4WKljHKrgxTBmhOdBY+FFYXNIhWBViApRuRlt4iqUcK+S71Vwr5bv1XCvke81VgVlBtW8GCKGbtZATogXROKKUOaeEe5TZ4mi0+pyFVapgtqi'
        b'kX8Z3Z9OGYrkMxTwIarWyGxFtVUDbEUNbEUVYCtqxlZU69U9sRXKr7qq0cpCycT6vBUfLoWbYYjcJCeGkZu4RfIP+Yb/TOECUowW5EwZvO1qH5wWpfi2aN/mUu+bs2Oz'
        b'lD9K2DC76syQrH9sy7kUfq70lyOfdk29Z4w5ffeA+/3jidv/mDR/6Jx76UNu879+pZ893vfF7/Knhtzd8vXPlyyc9OyXTUeb8Z/mtIWPFiIOh1+ePXncS3/BvzkcUXTw'
        b'70Pfvjx0ovhXfSiz7eC9Efi+MXkguRC8qPD9+WwnM4fsJtf8W5nL8X22m4mvzsKbpJebx5HbQfusPD6Md44bRnYxwSdmfi5IqYViQq5UMbnH42YrOS1JTPdcq5IMKZIa'
        b'f5LHd8mdNHzLwYR3smvmGNyC20hbKNlrTMFtuE2NwvryxFtqYsSC3MBnyGHcUgQrnrQmAdS7evyyAkWGCG5yFt+TnGYugeq6mxVKxucUSKXh8Z7B/fG5YWwrl2yjhkTc'
        b'kgpSmyFXMr1Ek1MCeamcPAtKxQnWw5L+mVDEUIv36PMKUqh3WgtPbi/EL3YV5zWPTVbayYbaZKq3NppMjFgMkYjFOoW8k9uXbbNRhxmV/LM2UsZug/yeRAA0PqHK7mI7'
        b'aqCq2txrfJoGB930F60+lcvttFrdvnBPfbvtozetROWkFion3WaW9uioc6iT+gY6EwOUg+6AfR1EObYMCKIcXVrZQbbj5F+6Ilx0TTah5ZJvFVd4jvNpTPIWItwrXFZ7'
        b'kJeDNGSaTLulrlK0TI+AWv5Ca1wb5Yfnf/RYAKsBoJ7zKU10xJwpASgBUE5qrdHCq06QjNBjdwLqDDH5x7/HeiOfqN7NUr1qkzSbPdYa1W2tHcRp6kxLrUZAQf9NmxGP'
        b'OlM8odAmKP9LcNGV8/Xrv/vc/In5B6mhoPCHV/8KZLGYP/NvJuv0HFuepfhmP7Y4yS38nH+BwurEuySk5rtdMBE2V5ANr92v7Bn46bs2zo8IHUpJLjKC00Bracf8YAAp'
        b'gVGkRrVoGDxXtITZG9CftMG43T0IoPX0nz4M8NdEHdpMJl+oySQ5aMN9uMm00mOxS0/Y6oEl6nQ0WJ2AemyVsUXXvtTGs85SBziLy1Vltdv9a73zej1HsU0qBkVYF0Df'
        b'QH+nI0O5j0bJEOrb6D7hHPvheckReAU+GOrKz9XnpRhUiJzIC10O9HUAudZlmsPkv67tXBAf5yqEPcKeyD1R8BuxJ9LGV/NwJ/+IfKtKTKZ8PsgnNwp4LOX0IcCzFVYl'
        b'cHr1ZgR8PaSVB26vFENZOoyl1ZAOZ+kIltZAWsvSkSwdAukolu7D0qGQjmbpGJYOg3QsS8exdDik+7J0P5aOgJaFwgqIF/tv1lRoaU9EKlMMaOVYm8NBPhkoDmLyRSS8'
        b'O5i+a40Uh8DbQkUU63mkOLSVF1NkW4og6sRhrG99oPxwBmsEgxUN6ZEsPYqlY6S396j3aKqFPQpxdKsgGpgkIrna09HSeiOrQ8QEUc9qjIUaElkNSayGOFFgtCYVpJ0q'
        b'Ri4fjgnVBf2Tc6UzAB2e6FU+hQ3kVJ+C4mJ3qFdYpQ6afLpctP51Tr1zZbEphA6gPLF+J2xttVYmKWomRGmApKgDJEXDSIp6vQZIisBIiuKDLwGlOzSP/sutt7ltFrtt'
        b'LT28UGvVWeTO2ICBWeqr6OmHzq9kNFicljod7ViGbo4N3nKyV3NnZRXqHE6dRZee4vY02K1QCXtQ7XDW6RzVXSqi/6zS+wn05WTdrNxsPa0iISs7u6i8sMxUWF4wa04J'
        b'PMgqNJqyi2bP0Ru6raYMwNgtbjdU1Wiz23WVVl2Vo34VrHirSA9l0GZUOZxASxoc9aKtvqbbWlgPLB63o87itlVZ7PY1Bl1WvZRtc+mYQRvqg/7oVsGYicDKujZHHh46'
        b'4xmsXfTOf8TEP7ygtwC76vFlmStL78sJGKPSopRxYydO1GXlF+dk6dL1nWrttk8SJF2Co4GeVrHYuxlAP1DojgwR7rpv8ePU4+fGUl3+1L9en8SFpdqk+3+hri7W967W'
        b'1PBCD+UVxAsa7QFqfEw20CMgCnzIuJBsNbLjKtSChl99OovZIp62tqFB3LtaZZpZ63RYkYcaz/ArlfTtAnyhmGylsngqaYa7olKpCrxpYXkO3b8tKMgt4Ohu8okQcsuI'
        b'z7MaEzKpBepXqZzOHP51Zrl0NkCxnLxE94OTjNT/MX9+jiSHUxmc7NKXk2Z8DpVmqcl+vKVesgdHU7+mtCwNMiefHRUr24OnUvvQFaVipjn/t5HRUtWjyN3E6cx/IlA7'
        b'2UrPqkBrU0tyyLZ8FZpHTqnI1ZKnJf+APeT4eNdKslOhpAYC2v59ibbE9Vc410/g8c/+e8eotqn1s8ZGzfnO315t+3Kz7tSwJHP/3z07sWRA0pydCeGnbJXbvlr102k7'
        b'/3znuxmLBvxPoWvu9MamU89u+nH1n/+0//Z5xe4ftr1RvPTKmNanM/7ncKt6rfHymH6RXyz9a1b9xiHbJryVeqgu/yc/+aM4cc6v4/7X/uWQVX92tLz4ReasGZO/LKpZ'
        b'KJbU68ePvf/1tcYL93N/bdr1wvu/+fpHPzT8o/LXwv82mqZE/qRyuXrf0aroXZN2hi1y9n/5qQmXBpoGTIr6WPvq7iXjL1377s2PbtbZNw36j/eP/vZq3uxD7+mjmYpU'
        b'by8Ng+HRF3hSEsm2VLyVbORRHPYqNJp85uQ6coyJtCRP7ev3CZAdAvDz5KqbWgBwK76OjxgNeQXJ5BQ5motbSZt0JGgAvqGoB43vBLOr5OB7qfLxgfhMydfwODnkpqYD'
        b'G96QEdjGkt7GzdkCiiObBfIK6FZnJev5BXwjJrBnlwzI0Ub2Spt2MYluKqyC8neK7IIph1qSSHNRYHfUCJ0DfCdtaeSOgObhq2rQBe8MZR3EV9fh08aiVLKb2icYXoTN'
        b'58mOFXgfA4tfIy/jA7jF3y28BV9Ukhc4crePbJgnp5aQE7V6KoTStwVyiLq9v9zIFL8EeHc/fVtaZUvwHSW5y3Oj06TK7+CL9oD+yXTPAeRZqn6WkJtuqjuR5/FL9VS7'
        b'bNWzE2LJMMKK8f7qkvB1JXkuYyVThVULyK5F1CoA1eVz0I6jHN75VJakYZ/EzeQw2WeFp4YC2shbHD7Uh+xjMjS5M0ZL21hA/TKoOX15lLZGyIglO1gHy+wz4LWAjNdM'
        b'XtBmC3PXD2XvLo7Cl+m7yTDOhdRjN3SQFp8VZsct8++Paf9t21ln6R2EYxtwd1nfzfEL7mM1zKk0nNcwk5iC0/LhXF+eGsfCOcmvmbpkqDr98PDD7r5WqUAHlCivwQ+i'
        b'UJKXQySxn/q6O2civ07bSdpuVwoeW4nXq6VK4jrWzuo0BCpm8vgsuAztoFJ8ODpYpejS9CfRl5UmKvX0qBAu8iuE7VD8SvLDUWUBEYkyLxAn/NwrwWm1iCmOevsavQFg'
        b'CKKj6rHaVCO1SWGqtFX12KTF/iY9HEkbAAJWr/CfbDCYVNsT5GUByEm9S0FP3gCqoDuZxbQn4JYAcEOwCPXvwA+V4S/n5LHX87DELJKCKqFnT60ROw5Fb+LVv9oUZ1Fg'
        b'QfTUippAK1IfRzB78pbUBrVE31tLlgdakvJooe5fQY5znNSKnhpQF2hAWhnTVAB2sMlOJ0+rzs7OevfYhn/P1iMwu5ji4Yku0mo21TRcOlunleqyWuvYGXNQb5gC0uVF'
        b'eu5c1rpKQcuBns3xOB26YsuaOmu926XLgp50FY4ToLvQaXhx1URDuiFN37v4TP8pUVcDfJleOgA4cL4niTE5xcwl5AyHXy4rtH3yvecVbIQOxrR+bv5BZY7l7Y8TSj4x'
        b'v135O0jxlR/HvhV7etnH2rdWq3SLv9M2jDkqvXk6ZPzNfXoFc7xsxC+T/TIPJZvJEYmPMi5KTk1nlupCctYdLCONH82EEUlESiJHmQDwdHhx0HlsgWygR7Kfz2dHNPGt'
        b'cXiDkQko/LIMfIZLzV7Sm4FMTe1S/rNCskvTM2hVKNeX2mVlFiCXkVikc0Ln2tqtYXT/qqED69ql7Wjp7VgjiA4zoeAj/JWowQB5ucf2VxIYTVE89HZBglKrWzISeOxu'
        b'G6jIMlH3uGSdmIVUcDst9S5LUGiEyjVdKqJ1ZDBzSYa5AMpAVfDHUmN1mh+hudF/XS2hsh/MteodoI99MjM0zVxoFJqQh/Z/SHRmz9pYsCrWgHfJ2tgQ8qxt8nfSBeYM'
        b'Mcq64XNzHmBrcsmn5k/My6t/J35mVvxUv/295DmJo8L1M1fFFJ/cNOXI2JWznwOsvQ7iZmjYzfd26Hlpd+WFtc6A7qAlW0F9kFWHJOSmTCNxHdkbLLkWkgdMPQgWXU3k'
        b'luzy9KiNUZfVbfLPDmPPwY5U9Ifzy3lr+/uxqcs7hX5gTLSiKNa7YxUrYQigMT35uLYDGm8Ndq3qBfAT0HeftuOrPZL6LR15zeOirsF/coqSjJ69vJi7DHOVoTbFgLvM'
        b'o3y8JIui4gNQQLqa5ALLzOG01djqLW5on03siT3WWxtlwj3WMLYbw0fP1h5RMqmwrvu9NAGQQVdiXemxOeWREeGuyq0TrZU2t6tbCxNd5NACl6POL2jZgGda7C4Hq0Cq'
        b'WhrcaqvT1bP9yVMltSh7Vi5wY9tKD60PBJQEynl1Tn+rAFau20J58aNpRVcfS02hZyrcG8iRGmMh3WdnQRcKU+bngHYu+YWWkK0DluTPzxFK9Phcrm5ZpdO53rYsBM2q'
        b'iazD92weysZAgzxY3sEq0/46wtfI3nLc0tCf7OVWkpuaheQQftlvP2nOINfDycE8jp6rQfhIzVJ2NnjO4uEu7dPkpGdBDt0eLSdbkxewzf8WfK4sJ5lC2Z6bT7ZxQKRO'
        b'6lfjfSPJ6TIeAfG4HV6s0zIHgnKRdSjQpgatv7bihSkL1PjCRFT8jAqfjCTXbZXr1wmuenhpyqhxKT+4R50B58x/Bju4uZao+A1vnQCqauHfyby1oeAq32r98pMBlTc8'
        b'X2248s4vh9oPfym+nRK5lN/4Su2+8YPeULxTujKl3H3+D74vPhh/1/vjvPN/SnFtW3/52DO/ff+nCR+rPrs+4YWzi5ctfku39/W1+hCmaZOL5PoQoMt+VTqsvm8yTw5V'
        b'DWTmEnIJe2vDEulm8+YRjCxKhhceDcXXFeRyBvFKXoRH+pBjQeEWyF1LSpNFsoM8wMf7GYMsBuFRkLVPiMPn8VnpIMfWKaOBMj9wtxt2ZMqMb+Gbks3iVU8KyApkhzMo'
        b'fAt5EMsoey7xNiUZ8BlNu61FsrMsgjrZ20ey8CXcUrS6IsjSYIOmU5KyCN/F9+Fh1IB2QwN5MFD2FXwsJxhKPttJhP/g6PB2Wh+jAX1dovfhMtWXUqpORLhDLYX+NjCK'
        b'HqCBvbEAIahYOx9YCpdmTt4ZY3xgA/oytkdO0KERT6YAAy3rkf4fD9D/sUz3aid0vSkcT6hv6FkrPD2r4ScDrZjaLYXLLs/ubM3vpj3U+ajOaa32qVy2mnqr6AsB2uxx'
        b'OkG0n1ulCGorNW6H+0nfXIlHtQeXQt4w2RcnvDpc5liKrUrgWErgWIoAx1IyjqVYrwziWAd75VhSUC1JomPEP1h96XkrifZJIv3+dwOHBXreFWAjIL3FXoHRo3kWqsAZ'
        b'dNmWeqolWeRnlcuBiXXLveiGFTCU0qLJE9PGsq0quo0kUqUUFKgewQcGPkM3126p0TXWWuWNMOgw7XN7CX+negJf73B3A8ZphY7UuzJ0WZ1FZbPcncdgf121tNBCD7WQ'
        b'kS0Nyo7sj2yViXF5DmTNGl0iMzQuPRrvxrvJdSO5nodGkZNa8gI5T3YwLopPkoNkv9GQkpgHdDa4jkDdUxty8soT5AAQIGaTU4PDydl4SWJ/bXEuEpeP4pDZnDet0oQ8'
        b'9DwLuYB3AJ/cQuOKdSe4p+QVlAZvobSUhpAHk8d5aFg43Ey24U2khZVhFu5cyjiTKCsN3kDJSc7LN+SmkMvWRBUiLfrwlXMmSnz9JXtkEAudh4/Mz6EdoqATgI6DYJ6s'
        b'T8lTorXkTAhuzcLH9AKLj1KODykpXHJoUYGAFNM5YDSvlrF4YrH42cYk+u7z+Aa8X0C9sw7yT5MT+KAUl+sOPkrOJ+UVOPE+eSg5FDNGAKnhBGe7XPIN76JHXPI/OTz4'
        b'R/ciSFq4orjE1MIN6Z/+nPftqE/f+Xnrtpn1PI6ZrT8wuCTn0JYS138If2jYFfqnv765Pe79hHPxy+b1/f75lw9+NqrsB39raJq6dNXPNr573PvRvReOfrz5NyURjujn'
        b'Etfbts1fEzLh/aznFIs/ObZ46O+fe09Y+lLfqW/v+vDHC/55NfXD/xDe+Uvk3sNJc2O+BB7OZJlNtVYjY2088LkHldxYvLEf49+5T+HDjH135N1kE3mV8W89ucSkgJiY'
        b'VPJKVAcxAIQAyGI28zwHDFZuAd5C9ieCWMUjDW7h8bOktYHxb3Iyujp4V0Zi3mV4v4bcx9tZC/MAVR9AzQ58yh9ObqKT8ealZDMPiEv3P5jfq8rOD8decluq+TRuw68w'
        b'99iluUUs/EhBMsxIqkD2Ji1g+yHkDD6a498M0Ius8XQzgByVHGD04f+PjPhhlDXKBITxd0M7fx+vYsEhNAHuHir/hrPDMtRez/8zVLk2JpjNynXJXF4l8WtKOJwivVg7'
        b'svqQJ/PeVUg1WQOCgBjggjVwOdNJGvj58GBpoLtmPolvmcb/Uo9c+O0AFx5G2QYQVcZEAlwn2M6nVzAfIx5+ubn6vk5qS3BS8uSkOh/1JRQdVSYT229w0rBjbF/CJ1Bj'
        b'/Eya7Gbrw6f2m4upqYcpyr6IjmosFZqCpKka9pa/X2zK+vw/2ijqCeWc0+DSn87UFrjR8ApFrHR+91sFj6Tp+HbIRIZc36iEf/GvQhsazkWHQkoKqKMI5WL7di4TzemG'
        b'SvdS5MY2cmy4K79QEuqB8J/AG0PX8mTHVHK+C+cLlf+6vunkRyXyFQpRqFDaUIVKVFSo4VcjKitCRFVFqKiuCNuj3KPZE7WHqxb2RImaVl4sAlkpzBtVLTAfaOohFG6N'
        b'EMPEcOYvpW3lK7SQjmTpKJaOhHQflo5m6ag9WmsfKfQOyGDUiSfS26daI8aIsdTnCWqM3qMFuFFiXCvz12bl+lRTL6p+cokYqJP6T1Gv7FgoQ/2pBogDN2sq4qBtnDhI'
        b'HAz3fcUh4tDNqKIf849CFfHicHEE/O0vvzFSHAWlBoijxTGQO5D5PKGKQWKimAR/B3tVUFOymAJlhngR3BvEVLgfKqaJY+G5juWli+Mgb5g4XpwAecPlmieKkyB3hDhZ'
        b'nAK5I+XcDHEq5I6SU5niNEiNllPTxRmQGiOnZopZkEpgEGaJ2XCvZ/ezxTlwn8ju54rz4D7JGwL3OWIu3Cd7NXCfJxrhPkUslq0wglggFm4OqTCICiafz/epsuqY49bL'
        b'HUQmSgOkB5LvlhS1FaRBGlKvxmmhYqAkw1WtCbgTdXLa6egJ5oQK6qxuW5WOehtaJCNolSSKQgaVLqFOyaRiX6Nz1EvyYnfynJ73qUyrLHaP1Rdi8rfCJ8wpLyl8mFnr'
        b'djdkpKY2NjYarFWVBqvH6WiwwJ9Ul9vidqXSdPVqkKHb71JEi82+xrC6zq5X+YTs/GKfkFM+1yfkzi7xCXnFT/kEY8lCn1A+b9Hcc7xPKQHW+OF2MIB12PRoomSYd4VS'
        b'UryO38o18Zs4kVshuIY08ce448iV6OZFvonvi2gc3q18EyDzOk4UmrgVKmdFE0edFOEt7phAo/eKqv5QLh7FokloHVevgedqercV0feakEkBtSqPA+E3qUQNm9yQD0zd'
        b'qSSd/drkeW53a+v8Qk+CPhsJSc2wSHWwnF6sWNKQZTDPsdKilPHpYycFo5EI2kluNZX6da4Ga5Wt2mYVk7vVDWxuqkkAN/R7sDHIfjVRQllQVpy2Sk8P2kUGfZxhFq3V'
        b'FmAzATQyg7piq6qltdukcQJklOEAgnXt26d0zh/G2erZrlN7b8aMco3xcQYfl/Yp5R+ffgv/HgqGtLRCvdoX1Rks3S6x2BtqLb7QBbQnc5xOh9OndDXYbW7nSsrplJ4G'
        b'WCZOJ2JGBSZBUARzrkO9njVnTPiXAeEiVAFMI1a2d+h4KhOtjZQQ4Ml2/SXBgjWtR5nir4E9fz+IwJZ/SmekYVO3psGqM8OUVAHXtxtmS3/NZoOT6ulPYPdgo9Rjs/4R'
        b'EHUGMseD7hGxCzjeDy5KBkfX8HI+zA8WJoFOiE9jcZmYj6dPY13d4KgHNbfHpnwVaEoVcwTw1FWCogxDIY+BrsFuqaK7rBa3zm61uNy6dL1BV+6yMjSv9Njs7hRbPYyZ'
        b'E0ZSNJspllrE5R4oSAt0rKXr/mzHk0gci+EQCLYdOInEMYt973u11P7xh+6ITXkDFc8kQmNdXVVrqa+x6pwsq9JCtxgc0pYslLLoGpyOVTa63Vq5hmZ2qYxu2DZYgWdk'
        b'00GFjs2y1K9gRnaX2wHCIyML9Y9FAuTl72+SiTXJTMfWw5a8RGAoJQoY12FsqeNrN1t2NAS61V3raOdfyTqXDWipXA19je6cB7vP9tRHuaIMGkQ9wyyz1m72/no1i1Q6'
        b'HDRgra462P7iYVMhdpqGboljo9UJy3MV8EVLJXUB6MES00G0pMikQJ2NKtpCD0X+0Sn41aSUnNxkqvYaF1IbBdmRA7dF5Ql5NOr5dbJPheqiNeQBMrEA4PhBVglokVcS'
        b'1pKb8xPyUmhU4bakQnyTnChJIad5NH6esoa8hK+xQwTz7eS8y4BPKwvyyN5GVTSKxPsFQ1WOhxLK9fhKQrDtP6EwJdGYUuKv1KjEG8kVkFA1+B7Z6/BQ9XssuU0uulgc'
        b'oQJlGb6BlLiNI1fWJXvoCXPyAj5FmktxK9lTTlrJ3vICjjTbkaaIIzfI/hlz2X6GaUqty1BAzpnzlEjABzi8AZ8qYtL6cFe0K0eyZhjLJ+FLCtQHWosvALSj0lbI4eIw'
        b'Fx0XJd5RiJTrOHJxuK7MNu8rzLu+A89zj4TFtU6tnzU/fPbvv/ooK7pk2P37O3cMLh4xwNg8S5kb917E+GVbUqxTkjd89Kuft2bW7Lg5ICpjeO24//zixUEpUzW1N2c1'
        b'v1Hqfrshm5v2uer8nsHK/s+setD6vYjLZ9/LGPFf/c+uuTbnwu5VhwaNH7z/gyW5pw0fxZxM94WlDGpseFcbVjAup3TrjcPfafvRe8vuTHHO+Oj7My6ebPjFK3XPnr/f'
        b'qvrg6+/oX/1c94cRg/9n08+if94YaXx30juvrJz21+9XXZhhjvqtev+0fFNR+sQZz3zxjL4Ps/c3Ds+is2PEF5tIixopUjh8kTSPkhwLr5ADlqSU2fh5so00p+aQVgGF'
        b'zxVU66VYCYMME3FLagrxkstkG4cUqRy+PnO+WwpTfC86Ka+AHCR38+HJMA6/mIjbpNO7gAWNxtyCxAJ1LDmAVApeQzYpmdmlguwgN4y0OeQiftkIL/bj8IkGspEZb9bj'
        b'FnzBb715EZ/psvsyV7K/JJAH+EiSQZ8oIxDeT3agSHJNWIMP4ItSG/ZNCTPCcrjSLxDN/wQ+zQwwNuKtZuYhfA7vKICnhRy+gvfHSIFfr0YvoMaV3GQDacGv4OZUuqqg'
        b'Dp1OQW7hV/q4qaN24mpyAsYzBxD6vrzOcGsqXWgqlEheVZKN4/EeyYF073warbhlDtlPLU10aDgUJvLk0Cxy3E23qfND6OspHFpQwK/isnKIdCCRHK6dZ0wOOquJr+FX'
        b'1kwnF6Vtqivk1cnGAiM5udhYYCDNyUZ/eJBEvEOJL5OtGinEzv6ZI0hLIb6oDElWIcVsDt8nz+ONT+D++K+cdoyTSKGpI/Xn/ZxQtiE9g7TU31OyHlG/0Fjm+0lPRUqW'
        b'Ja3kLSrnUo9RdjZykCzsdAuk0H96ip1r/Ff8PTnpVSZD7ILLt50sR5s6HIHstTFQFxUfe/aSYZFaWHgvkAq4oEgtPPuERu+eMtUgE/x3dzJBtsTU5FM1khBIBRfgMZRP'
        b'BeQwWTSgcoJLFu27siB5I6GTbNFJkuhecujK0Mq6SikWygk7MG4/H3VQBk93UdZQEaRryyxVtdKWfJ21zuFcwzZ9qj1OiRe72OdTHs3UO2tOHSXWIB9Ft8VZA2qKv2Sv'
        b'2yb1gX0TCTv82yZ+4YmKPFZXsI7/CN7f/blzjbSTMT6ahm+rVSuKzclLIgqlMxf/F0VDjxzIEorNmeaqZVLmP4ffRqsBY45Njl8V73hhPmOGWfjF0a6ICB5x0cBwdyBy'
        b'MR/f9FCfbUvuOErkBLw3WJZgmzQlfv6KL5XRDf6FwOhbUucHOQsAKVo7JCoDKOsD20+XgFZ+FmpMj9EXtE7V4rSo2TX/ox3WlBHbZ+WFL8oWbHvlesKkiOLkiDHHrjje'
        b'4CbH37J98svtv6zdMyJ6yIULq0b/+PjCqcPHpRbHFOBZGxt+1Bq3rWDjvAPpF6MH/bNUvbp+8NMDR9f9OmNvXePmcTevrtw989TPDX994ykHPr/z9dsfrHnvzumTQybd'
        b'3XUldr/q8M51l/42787dP37256PfFbTvxez46s/H9ky+rFuz5sM+//vPsNUnJr/3u6/0Wima4h2g2hdJyzNBG/0p5FyGxDq3R+F9RkNKGj4sj4QCRS4Q7MkaxiLIYXw4'
        b'24j3zWoXxTqxCHJXJW3Wv0IuJ7IdKxqpaBswxhNceX+8hfEjDz7XZKzNLDB2S+aXkBcYt3OTV4nXSF4qbP94zVryLNsumESu5ycFYmOh9NIwfI0n5/EB4pX6eCUb7wRW'
        b'582gUY3kmEZp+JTEhPZVLEnCbVReYD5hEqu8js8wn8cEfGChzCuD+OQEfJKxylOT3ezzIq+txVuYaJpL4wHRwaghG/zjwZNreBtnStXQ0AAX2c5JiWYhuUSuJLH9FSVS'
        b'LeeH5K+RQoccIUfwrjDcTHZ12XzRkI1NkvfFdVNZUnIBvkKugkQqB22PxLsFZxZ+ubtT8I/L1NSyrsDYWGYwG5soMTAVO8IQ/i3Ph37D85pveCHqn7yCMq1QFmdSG3CI'
        b'0HJrtTLfkCvt6Pe2riPv6iXKBy+Vbfd8oF/MSYC6XH3bOdYG5AsO09QZdhdNnFIbponTaqkmDr/UZjZA5Nw83AubuL5QQOQ7pPzBwx7yo2wPFaMM6cCfWOt84aZ6h0nW'
        b'lV0+wVLpkkwr3WjtvihTYB9cMkHm8f6j3zwMHL+2n9+a0qlcFzthYAM6Hy5b2WcVNvHOuU0c6w9aIThn0n45E5u4Y7Qf6Di3jqvv6xZEromlaclqQbIewr2CfpqB2f34'
        b'wodjAky0zuaCZlTVMvYzCqg/NUwxnZnewNyxIYix1TXYbVU2t0kadJfNUc/myhdStqZBMkexQZFtTz4l49U+jWTMdTh78ALWmhqcVuBhVhMrP5/3+z7SWGCAeVqeYqQK'
        b'5n1tnH/gOrzR7eSzYWOxTan5E4aCGkCXc9V8X+kMBgxAtFRbAu1kstRV59OBSdV2bKXGZAKYTpNpCW0fk4aCzWLSs57RMJq1xI+Iwa1QUzSDUQ8C3Qmf1CZ6et/ETiL5'
        b'IWsDkNmjDuIZvVf4Accz/D8GmCByx/l1bBCauBUSpgN4LvMc7zyKZFMh3LN1+GI3zVCZTHa3yVTJy/wbweysjQi0gz574mYEkJHPnOY8RUGd7gGy1WSq7gmytRvIARww'
        b'BC+d4f5FsYJ36KQ2AFmgkinLp3fMbClNBm1LD0gLTbKuNJmW837PdYasoUA4gxpGS3RpWMBGGM6GhAIND5zK4XsZgnroZkMQCrTDqe9uAB419Ar/0HPTex35GphXVw8j'
        b'X/OvzLnSj/n89N7nHFQQU2NPkK3drLaAazsdWv+qb7f4thPsrmubWsNMpqe7XdvSsw797CDMjuy2n/3ohg5iZJjfxPv7zCWdE9qXGyOs/mgfLwZyOzUP1r9FFE2m9QE2'
        b'whTKIBrAHne7BIIwjTbwONd+xOdmT0NPSR2rcVP3pK4rtMcYjvjOwyFRnxTndQr3RvfddnkqTaYtPXabPe6521rWkLD2jlM8cN7qrdusxpbuu90VmoCC6AzVuAN0RutG'
        b'jKZAOrZzx6WNAJ+20OHOBY5qpUeLrGI7PrDB6OnEjMlU5wFk3MHLexqIiW0dRoUVeGxkqJE2aV7tbVRYjXu6H5Wu0DogQ2bwqOi6osXAwDgN7DROYoBDcqntSNLDuISZ'
        b'TG6nxyraVplM+zvRZB5GJzrQ4ECxf73NAwJtHtBdm2sYbUt9dKPDgaXZHQ4na87RblodE2h1e7l/vdl9A83u212zJV4w6pGtVrNQQSbTmW4aHISEjs40QhHc1mLUkSm3'
        b't9VNW0v3uaFd7fdL+HX8OkFus7CJtl6Q7qqDUcWngjEC0CC1Mxr7JgomtH7VhBJan7Kx1mG3UhfgOoutXrT2JJ2GmkxSnSbTZd4fKJ31OJynB71Dv13bJ9Brf8meJVIq'
        b'B0qcKYxNhswZ/BJHd9yJxV2rMZle6Vb8Y48eB15oO7zNj4LX4HCZTPe6hcce9QwvlsFzS7C4IN7HNj8PdJiPnqCDcmUyvdYtdPbosfk+k+Su9ALJVg8CzBvdQmKPnkjC'
        b'6BlSCFvAFqjwzSBYUcGrmz50bkLdGFo7rG+6SlYgZ5QbNFfmEcKJgqigTKYfNGQdXR1UE+S38sel9SKvEjbpysJPaaUPh7OdYFt9ja7B0SjtJY9NkzwqPA0NDhr05yGf'
        b'ZvBxY2HFbPVPmU+z0mOpd9vWWoMXk08NNdXY3KATW1c3+NW/Hg0QMBIMuMn0nXbyoWFhRrXBIyIXkngTHRZ9aicXQudyuT6X3eGm4cSou51P29F4DenqamuV27ZKijkN'
        b'JNducblNknnWpzB5nHbnflrbIXqhfhCSM2IAR32agNIfxuyh0t4rs6oz5ddJQ0lL1OY4vbxEL2fo5Ry9vEwv5+nlIr1cpper9MKkr9v0code7tILY8L36eUBvbxBL4Re'
        b'6Iaek0YNdn6XXr5HL9+nlx/Qy3/6x1gf/f+Pc2MndxEHXH5AdxSoC4VGUCgVvIIL+gG6GBvXg+eikjrWDhnDw5TH63guVKUNCxc0gkahUWhV0t9wIVypYb80R6thPyGQ'
        b'K/8wp3ByFV8jl1xkO2mV3Bk1+AzZFs97ZoR0cWZUyH9d73ZyZvSHVK1WsACvGhbqjQV4pQHf5FBvLJirGMLSahb6TclCv6nlUG/hLB3B0iEs9JuShX5Ty6Heoli6D0uH'
        b'sdBvShb6TS2Heotl6TiWjmCh35Qs9JuauUYqxXiW7s/SNLzbAJYeyNJRkB7E0oNZmoZzG8LSQ1mahnPTsfQwlo5h4d6ULNwbTceycG9KFu6NpuMgPZqlx7B0X0gnsLSe'
        b'pfux4G5KFtyNpuMhnczSKSzdH9IGlk5l6QGQTmPpsSw9ENLpLD2OpQdBejxLT2DpwZCeyNKTWFpyo6ROkdSNkrpDogodc4REFcOYCySqGC7OZAQ4yxdJz8+UtZ9C/eBK'
        b'550l/4HNoEJy3LlOxahDBvMOqbLUU8JYaZV939w2tq/j9+FgAc78XnHUjUPaQLF23OqRN5g6um1QLSroyKyZkmGLdARIdFR5qFYQqLlDbQ6nv0KbWzKsSa/692uyswrK'
        b'Zss1mHtw2euQyK2WfVAsukpmBoTqpG224CO9yRJIf19lt0y300oHpEN9FhfzAqWNY54hq6Ami92u81Axy76GMp4OZ4U7vNyB5VKtj5Ic6lDhquQo/3NGUR7YH23lV4Q4'
        b'4/180M3sn8e5dYIIPM8kXRXsqmRXFbuq2VXDriHsGgoSKP0bxlLh7BrBrlpRgGsku49i1z7sGs2uMeway65x7NqXXfuxazy79mfXAew6kF0Hsetgdh3CrkOBewsmncjB'
        b'dRjLGd7EHxtxHM1GS5eA1KtYp2xSHIM1epzbybmA9jQp+qF1ivoBLFdFc50jRTVw+VFNCmpWXKdwjwaur9jEQ/lM9xhR06SQ7L/uBJrfpNwkcGjl77ZC75Zrt3Ks3BK3'
        b'fiO0gIlMIYXOH1IpYYK0ALosl94XBGMTc32cycebTA+VplGuUa6HozpXUmuhflPtrleS8TXRF14C7N9WJ7s2qqQdRykEqWCyiT6lyWN1O2ncGOmsgy9SimMeOO/mnE0Z'
        b'FP0ArJOazJ1090aKZVLBxIOOxyRBBJS2lqHGBo8TRFsrgGCigZpZ5N0Wn8pU56phoFfQo4NKk1X6ww4SRvhfY9/9gpeqaum2KIt9a3F7XCCfOK3UVG6x0+BH9dUOaDEb'
        b'V1u1rYo5OINIItGMwGNLnbu9Q75Yk91RZbF3PK5PIw/X0s1cF7SPrVmohv2VIhL7Bpk6DTkItLAe5bJKuK9z+UKhkU63i7ptM+HKp4Z5oXPi02b5Z0aaCbXL6pYfuFxW'
        b'J62QPdCrJEcDaonwqVY00m+iB4U9aEKPDrrAZvd9KgxWMGEwirlSdA6fpemS08MPL/2NYqaicPZxYXqN5tb26zQiTxTwWTql6vwEoZ59RqNBCZJcWeM7gwr4tGaWMWeF'
        b'+hXtRzSTpTAKbod8pJU6FopAum3Va4AgBxHKJ3RxdWb31tg4f2Mfju4YWYvu7Nc53O3naFls0ScIbeXM6Q1ufABux4BaXcHSYKZPEM/K2BvUgR17GxxMqxNYObLo449y'
        b'r3G0hgTg6ruJo/Xvgi7tDfSwAOifZ+mkeLIuT6V8UIO5r1N4sn+NHK6p13Yx4UmqiG1WUlmnAV6jcgqLatNNACiDrrQ9r9pmpQBlwQFqhwLt3jcBXuDSJcrjlJgMtzY3'
        b'++sPt5XItiUTpZhXiU+AlU/1NlgJgcEa3zXKSQ/4mTVrYVYqXOY80UF356e9tSMp0I7MDqftaSARa2XHc/ed25NdMmd26uw5s8qeYK1Cez7rrT2GQHtK2OwHsXDZJ8vv'
        b'kt/JWcigm80inkiuUfZGyxqXfORcV2+tsVCF/Ila+XlvrUwPtDLRj+p+h6egBsucWpdQumBhxZON0e96gz4hAH0MI+4Oxwoq4UoH50HwbWhw0ANRICJ5pKP2TwT6972B'
        b'nhwAHVkWON/yxCD+0BuIqR0pWB2sWUuNNQgNG2rXuKjTm644K7cQ1rj9MYFXS5tQf+wN+PSOQ9sO1O6o6QhTl2AsmTP3yVbin3oDnRUALTn81YspbkcK/Gln3LqEOU8G'
        b'E7r7f73BnB2AObjbYA66hILHByhP7p97AzgvAHCY5NUIImI9PQsiLxUpuEZxeUnxYwKVN5P+0hvQvADQaEbjmMQsH2t5ItT5W29QCtppQmfKReVs6nZD7xNmFRUZcwvn'
        b'lc1Z9IR08++9QS8OQP9jZ+gdpX+Dbi7QiHlWaE89kwtdAVW8uxjwQLwW5s4to5Hck3XzFmQn64pLcguyCovKspJ1tA/GOU/pk5kbz1yKMrVynT3VNruoAFaQVN3crILc'
        b'/Kek+9LyWcHJspKswtKs7LLcIlYWIDDzQKPNRZ1bG+wWGr9KCvjxJAvwH70N4YLAEA4PIuqSqiQhpoUtRosLRvFJkPOL3qA+FYA6sfPESRqdQZfVfhgtt3BuEUzB7MJ5'
        b'lNJTVHoiFPprby1ZEmhJvzLG7SU1EqZQpLjjeLK18nVvoEztNF4OxsJON0qArO1moWBd5Enm+cvegFd2JHrtxI56e+uoLasbpuJ3M2H7IgtkgK5C5gsXz/YMmZNVwyB6'
        b'L51/pfsg8KvYBFcTLa9kvnNK+qaJXY+p4Ko+znFBCPNwaonkEU0tWgEZRxK52m1r3YtkBr3G+VvazRX00imoM7NJ0AgGzjrEtlrbIz932jwKo19rk6u0Cv4dSNBz49nH'
        b'lqhX5tqBnRXOoHd6nilqXRP9HlhlEsjuponuVziE9o2rLuptwEWmx/OQ8fIcObV0r/c4onu7NdLWmRz29hvaVwU1UnTrA6eRDRgm+jUy2RuEmgW6a4xUsOd+xwY1Roq9'
        b'K3LyBjIzfflbo5T0kB5c8uzWepOpsVNrujEysHKF+hHd7V8x4wfbcfJpOxmyZgQwpx1p7H588UV0tGOpZDOWWubc7GO9PpVswlJKFiwFM2ApqP2KxRnxhXcwXqlk25WC'
        b'2aG0naxUYcFGKpVs3dK0G7ckw5K2o/HKOZKT0cc5mt4lcPIgPlaINucv4PJTahmiG1waQREWnf6EcTLUPcXP+Dfjb/T0V/W48TvCQzWCRumhrlJ9cxPCVkU0hOvzyPYk'
        b'vIMcLsw3UFd10iagxFolvoI3LOo2MCP951qNgre0RH4zYl8pFERF4CuFSvlexb5YKN2rRbWogbIaL1/NSV8nrAiRonJUhLJ4tzyNzgG5YaxEpBgF9+FiHzEaSkSIMYw8'
        b'xvpiOuF7vg3UdEVQQxXBVICee6OU2MT8OEwc3Z028TU0HoEgBhijgikFvpDAl4Lhts4hWuz0Y3HDOxs2KURT8EaKy+/mkcqx7Vt/JRp/HZ3JG9313SAE/Knkr9cN6gbO'
        b'kwe9d8ZwvfC+LQGLYbfQnugLcbJ0M7U3eF4/vCfh3pm91bi1xxoDk049Jfz+IP6gALyTfnLWOa2nqim12BbEcXqajO4JfW9OGtChdqgdOS0jT61BUDtzVRkqI+iPwVVr'
        b'H81Vdz66jzJn7XwyIOBwU4jaPalc0W4ALfv6M6+vFYJrPNwzryl2T+8UKwRnplsp7ZxBWnVMTZ0BufbP5z1MCZZ862isgMr28AtjOrV0TMfiosMqnYqXzhSwqDD+I3iM'
        b'TYBcdBjJC1T6rPx0ejeDXpi7CZ0h4GkNDaBv+w8ThAWBYEV78NcSLKK4Wwg6QqCR/bLpYZZuODQbZninZywKlbGo3aWofU47YdAYePFw0Jz27w5Y91JZwD8zlq0XiZY3'
        b'odloEyeLSUJhFxk48BI96EDp6NJwesKDCjXP8yuZh7fEb3lnEh3dJumergsf5+6MkZFwOSbI/tYqALA2pbv2ux1uix2IE92Wck2HG0rzHXUN0/WcT3B56roVmJTsraOP'
        b'GhtWqlCv7SwstXvmMKRpx5d2uYKJGbM5eRac8wKyRi+BTzKg0DpBHnTgyCrpq4MagfqkUJ8TD/2MKN43Ut/OosPJ5gCHJtdJc7KBQ7PJRXV+Mn61C5/uK/917eA68GmY'
        b'XfYjHFZWCNTlhDqc0O8LiqGUC9MvCYpaynXFPoe1FfQrwkrgyNFiDHBhJTtpq6FRsLzR3v7VajFWjIN8lVXNIl5JXx5Wi/H0XuwvDmCOKWpxIEsPYulQSA9m6SEsHQbp'
        b'oSytY+lwSA9j6eEsHQHpESw9kqW1kB7F0qNZOlJqUbUgjhEToC1RVnU1skZtQju4iih4Fg2t14uJ8KQP9IQTk8RkuI9m9ymiAe5jxClyjC8aW6T9S4xa6GcU62mMN9Yb'
        b'5+3r7eeNr45jMbVCKmL3qPf0FdNbOTGDQoHREFhkLRpnLI5+tVCcCM+mMjiTxMksv684jpG5TF84RUG/q4SPK/ZxRXqlj583y8fnzvHxc0rhb5mPz87xCbPmFfqE2Uaj'
        b'T5g3q9gn5JbCXU4JXLJz5vqEwiK4K86HIiVFcCmdQx9UGJ2rGEWal1us1/r4WfN8/Gyj00iJG58LdeeU+Pj8XB9fWOTji/N9fAn8LZ3jLGIFsiugQDk0JrfDqveHT2ce'
        b'EfIHCqSwXYpA8HRFr8HT/TT+MYJ9KwrZGdp++CQ+SBeAmzQXGUhrAQ1W2h6ilGxVZ8G6MOSys4r5ybkF83NgWeTRw570U6nTycZIfKMcH7DddUxUumjgjn9ExHxu/sz8'
        b'9scJ0QmWHIu92l5ZPzDZsuT1/3zjxs6xB54dF4Fq+6t+/9s6vSAdiDzSb3IYPpec4z8uuZzc6kPuCvgiOTODnfJ0YK9AWopysZdsA8jUH+wQv7oYvyAFqz5gzsa36BeU'
        b'6YeaO3ylOY0c9J9bfPQ+Ne8n0IFzk9LPZOrCuDY2GJ06fvVY2b5P7lRSytTtp12BVLESowPFApCvUSpFA4MEzkNKPz/p8G2AbltQpQmaZAqy4zcyNQx/QuWPi0uLTgrv'
        b'0/6NTM3WEMCpEMApTQCnQhhOadaHLPL7X3fCKYmLdMapQYVSlNrmVfiw0R+NEHAoJcUwPydPChRLZ7q8uBFvzsFnBUR2kCNrG8LITnw+jkWpJSfxc+Sl9pcB24pSFqzG'
        b'V+QD3HmkFchzm3FhAmleqAG8VdBvoF0OixiNL7Mz5H9dp0Lh8ckI6cz5H+U2IhaBlpyZiK+6yNXx7Bw5O0Q+Gb/Iyh+ZHoKiFjXTOLv5XxgyEIsYQy7PxttgBRwle4PD'
        b'2Hc4Uq5GT5Wq15AW/LKHHrceMwSfMuYWGBeQncmkVc+hsEKenMZ78R0WMmZC47CkHHr2nOwel5aG78MAmI1oOL4p4Nem4Bc9VOAmx8h9fd3gpEJ6Hru1oDzo4HqCISWB'
        b'bE1NpFF9HXoNuY4v9mGn49PzyUEjacnNT1Uh11BVP15LtkvRMNnj2dkVSXTEU1QojRxW4bv8xBEzPDTIxejK1exJOrnfPaD5CSxwe3GC1Bz8XI6AhuDnIvBtcnoqG9VM'
        b'fGyZK45cX0WuKRCHDyLStoDsYEGU8T1ysJB+KJI8N076VqRxYQOUK0uArJbk5IJyKfi+dFa/PXAlOSmEkzbQlI966Np2FOFd/kj1ZFsKvp4PHYmZJ5AX8Xl80kOFBvJq'
        b'AXmpfchS2r8MENQVCgZvDeXxNh7hm/hB2ITZ0vd4ZprJMSAYL5Dd8yG1FhVE9GPTlaCYD/z/auMqcgM3N5Jb5BK55lahiIE8Poh3jGeQgdwcwjtc8GAB/SJBQl4KTDyQ'
        b'RgatJKG9SSqEd9MQQ+SVUPoJzY2ecbTdD8hVcnTS6CQ6IDBALamkrTQhAWjg1tTC8qBPEyC8AZ8LQQPwTQ/7XuLeFOwNgxbdcJHbK3FrozNcS5pXkltAy8cJeDM+wbMg'
        b'Q/PJRjNpoZ9KSTHkVDflFypRNN4r4Ev4hSaG+B+MVSJN7H0FjEH4IN0ACV/Ivow6aOJJ10ql/BHL2eSU7d3yZbxrBdAs03dOlJcYSzbNjHpxSLzm6Ndv9/v2YzTkjRjx'
        b'1NPXP31HU76c+2j5tbEV//XeSkX1H5/PnKs1Z08vfy/zkzVH/2A71pdrvvmDl2bpLnwQpklM+7xp+NG4aGvp+a+PbHzzZfvG2cdnfj7vLb7u/2PvPcCiurb34XPODMPA'
        b'0EXEPnaGjl3sCkhHAXuhSBdpw2BXVESqIoICYhcBBUUQEUWMeyWmGW96MZp2E2OaqTfFxPjtMjMMZdTk3vt7vuf/XEeGYc45u5e11l7rfYdNyJsSvGpG6ZLfRLUvRXzY'
        b'6/cBwStfW/uwbfiODPumbWOWpa/8/vvc+tKa0294OE187cPDv0sWHBny6LOxu/9YXpH9ktdg0bCFxehU9LMjT8wVZZ/zvvP17ubVxi9u2bfzfunOgaL39v3+62/7frvv'
        b'Vv38QMfVpUV3DvpHVCVtun5r2m+287deMBlglXok+kvX6bFBi2ZNi73znevg9244vuh8K+B6cavlexs+X/vtHycz3nIb+sXbP4Y03Lsy6d0p41x//m383otnhrX7NNha'
        b'JEe5JVoflzw/efrVgLUL9668WZKwxd/sn319risrR68oemXti2Gx1ZfX13//oOp6/8YXApL8fhv01uSPVj+X/YiPibEbtKPlD0PFwV2TfZwVw+juONQWzmh2R3QymG6Q'
        b'bHdcjw7TO8bhPsfDh9AnQruSMj/J0FkBqlAJOpVO4aqa8cfDWkBodHaKDqHDlQH0niHToRLlrzEzNU6DBpQNzUq4kG4q4axTRSGoeFm6Jb4n0VzqN3EkgQIiQEBQnMhw'
        b'JnbiRTIT8v2HjdOlgsiFUnoZtYfLcemwROHqrYAcWrozAhwfrUaLrhw5H+WbZ+ABXTIxBZpVOE9ZHyEOHbJhPBaVy6ar0S3QlV4U4AJVDaYsEyPxjt+o5fOE4gQtzcSY'
        b'4ZSyCrZDttJvIhQRHglhHT/FDF1iiBaZK9fjSZeXMQA/h4ssnsSjc+jqnHSyJKS6GviNQY1qpiveBY71TSd7Atq+Al1QZpikeo1SQYs5ykMF5lJTY2gwz8CzEC6sScVF'
        b'DxBLUCteUppY3StRBSp3cIJCfze8tjWZShbzUIfzrGJ1O4JOQhaepFHeqB4LIJt4rxFwhuEnNUP+ckLEmY/qvAOg3RrhTc/ZN4CwojaL10A1XnVIGwxBh/wZef3upXAR'
        b'bwT+WPSZIcC+meg4I1m6uiFNwx6KFwIhjSwENv5iU9ibwfA1zmCxqhXh9REPMgPOK1kSLgztBxX06RGQOQNfwksZ7INsspwZcLIgAXd469B0YuDcgPauVhOPBZF9GeeB'
        b'rnjg3VLCDYYqMTQNgHwm5bXhV4P61qmoXIeiTOzEOqXWz4WCeRX647Y65C/xEfrgsVVPoTUWwcVEiinu5BwIJ0X+QZQmluf6QaU4dQuuK8WyOglnTQjRaCCcwjertxSz'
        b'EFEAHjbsjh1YUjxBKEydUPsGLFr4ifBwzBOgehMcpYBUsxVD8GVfR3QIb6pYUOCkE4XIyI20siMs4DK9iC+gHDXnqi+0++DBaW9nAFvN0BlKSAvF06Aa3xnoiHJd6JKO'
        b'6tB5F9zyg6HFwAAVTadzDtUmzaVlIWLFSlRHIVqs0Bks7KJjuN0oZ3KeBWonE4RK6JCHLmukdJSLdrtQrVWrsjrgnaZwmDE6LFqQTgWKg7jRD9GnA+GsrohPH0a1kOOv'
        b'kHD+nCFqnI0a6DPGQIgL9FDgEsQ7Zr1mHLgubhQEBvbDjv5snCD6CI9a8FMSrCKL4KojtPQsgP/niV2pLYEK8mndBfmpxryUcLkKYt6WYKDi3za8rWBCQFEo56sJbyFY'
        b'4OvGfD/8ncBJH0lFVjQU0EQwFmFhXJDouK+SwzmJzl/Usty7i5DOTMq0gLXG6qAqjX+zmBjc0kj7pU0kaqFsZUS61lVZolwZF706uivUiuFTNEetNC2eVyeaRnZtlgjN'
        b'KJH8SS3oCbxum7XoUUFe7kQQ23Pt/gohjWGYul56wVm1ZvPOmf0lezk15CU9zrb9QHsybUdZUjRBGax0cjUCSifU+78KQntLFqb2qAp7DAfPQ21BHHvywYpXdpTt79J9'
        b'0nNqffkTTY7lPyiUOl8R16u/TX/LrPDEV16VnhwTozdXkTZXyreK73bCt8tJeECHGxgpCXWn/nskuPLH9b9EWwB76hYRH6P2g1hNvE9wq0cnkfiWqL/HAIybwCRMZzbr'
        b'LYaRthjUSYu4ZMQSqDitP+Pf6YC0gsd1uIk2y1H60Y87Z6yTL11ctfCAY/GbFlieWRM4EnOziV9vvJHTWhN4ak3gNvP6rAkac3dX+Dj9hLKuNOcY/i/QyRKIYhXfAxwh'
        b'+deJqKizq4dSroxLViVGUWbZ6DQKSi6PiI0gDiI9pqVle5qdGB1BHKfkHjSAhnSsGkmX+h2q8cXVLkfxPSPxqqHHw8ND01TR4eGM9zZabr8qOSk9eSXhwrWXJ8ZHpkXg'
        b'xIlrmQazVy8dYXq3WU5Q9tUeBwyvkLmsrdPxBHsyBnt4uFdEohKXsDtSII384rr847t1tygwPu67RSIlUUNrXfd/Ff5C5JqvpDEf4S1LepJ/Y0mqgmfCVYELqtYVNrD2'
        b'c7ZD2kAXejGzHN/19EgcExtN0dF+pMdHW7q8Bq0f3mnHUa5MDKMN3HEcQhLQ4aplJ0QdJLWbcKUsxOqz8C4baSb3g4nOVkptr5CNdYWrXYyvsMdBW7MAInejJizc5QZh'
        b'BUpBzJx+E6CNwrFCA7SYuqKjqPk/zHKr14isPTXTNSITWxIWq4+MpjLjyWhdsZHYYnL97bE0fSqUmZfIF0H+lJvqNMqVTcJ61un4PiqloCRr02v9lV+FO1t9GX7DdEyk'
        b'nY19hD81H38dfi88Kebr8LxY3wg8IPxF3D5jqeXbvgpROlkHsLCfg2r0iawd4irUoCq0e8p0qmChUxxUdyFi6o+OaZF8IXszVTygBY4Z6Yy21XDAu2OwGW54KvsyHnpK'
        b'9dCz6WnoDSEnmU8x/HAiTJQU6xAA6Ccf1AB+bdSO0C14hPbTO0Lv6dqbVSTEaAhqC/ur43NgukMgGZ7n+ptOCYBahaCiQL/5BOrQj45csTnWDyaSSSyl4N2rsFLR5kef'
        b'Eo/h0Tb8aoJGuBw/RniDbTIDH0pXxXqv9McDIuHjmui42LjYxFjflYERgRGN3/A/9F1lm2AbsuhzV4MxKTEc95yjUcSvnOZwVNcCr7eDjLTNTbWHHnvJxsTYQrzepude'
        b'Yv0iPKY3dPbh7bgbzPV2w48WujK3nvz+g1zrGmDEp5jveI0+XT1NUJJTmf0T4Cs8MW9ExsWY0FXa+pKxmfDRM854naaa60W0a4xWc32S1joO7SeK60LU2q3funhx0A7q'
        b'cQW363ZGQt05OhZsPeTiJNUhervjY7PHncJ0dxj5d+QUvUtv9+1SHBgar0p6IFaSr/9x4WM/B3kE7gd/Q05sxyum3OuQ/brthPQ4Xf9G6NBNz2N+Kvo3PpLecL0N+IHJ'
        b'43TIHrxL/90WjH26E1A8mP9RIjdQEsNQ7x9+dIi4h0WOZetXP3O+6Gg5OagUccMeiH5UjcT7DFnCxkIFbIV8R2LuEaOqQTN41IwKe6WTswCrEdD+tGOd2AeplQblo2x6'
        b'wLl5GTrF8GSdJJwULguQRRDvK9fr6b+Rj50Gzt31dOZdq7f/SHqj9Pbf+4/tvw7PXa7bYeQATZvHcPQwkpz8m1CFQXP2L+y0pPJJJw+AnQY7+9JDyn47++8cEDNAe1Ap'
        b'e+JBZbfJQ9xhrLt1vWMgPe1wz0AHNYdnaJ+UnJ7NSGCHZ3KOAPHXDZalQTM0m5ODFpQTSw+BLNAJAS5BjZeKwKML82LoEZA37r4gVKdzDhQKlT0cBUH2WhkeN6XQopDQ'
        b'UzRUhk6o4BjUKMkZDgdFHCqYFEbLZ70YTvUaDU0qCf7+MIeHRAsU04cUcFaBTqJMGVwgBzXNHJYDyx3YWWcWKg1HTeiiMh13K+RwKDsWlbDTnSYLdFWMGmSkJeAszlqF'
        b'EydNgwpMbdxXKAkiIxRzKE8FRfSQqIKXkCa0sEhO8I8d7s7RvRxOwIVJFtBGTshIQsdx45mhWnYtC7CQBZmmOrWBQ1PpuXAcKocc2lhdzsqgIT0Nzod4O0Ae7MatpPTG'
        b'/VGEyow2QTW0Uhkh1B72j4GiMa7QivaJOR43B2TCQUeVGyl9FVxY1IlxXIMdM2/uQigd4xtiiL/Yx82HMgnuzvplKsLhg47ApeQxsaT6bpxbUF8VGSeoYSAchb1oK2rG'
        b'Q9qFc0FnhMRfHz165GBvQChO5EdGRjimKRI5eswZA6dVftq8IMebEpMXuvjOt4Ncb9jVDwpC7BSwe6G3D5GVCgKokBRMxoEkyXQ55IxVzcDJLIpcQtwtdO9agM4tJ7XA'
        b'opVLkLqZdA+gyUg6jS6bQKMrnFGtIE1dBu3JpviBPaYo01VqAJnz4ZAEdoWaeln1k04JRpcXBqMrcAjOesauNYrpk2oMbZI1UpRnFGSCGmA7nHCFKxsUgyFnsjNUSND+'
        b'2QrUNG0slNuisum+KhKJgcWyJsEAL4JbTTk3qQg1zEeNS6BUgnJhJyq1R1lwhRzehvaP34wF8sz+6ErC0P6oBRUQu3vMBsgSudnBIVSCUygcDOc8egVACcqkawcdbZ+5'
        b'9efHCpz0u+A1m7zdTDl2zFqMjngzutuxlp0JbzuOS3U4b89Ai2wlKoKjNMkRm324Io5zfbVfuO/L4UmciqDTQeuQ6aQa5Uac3AR/WLBiFc6lDk/qo4SpFaomj8H9sTcc'
        b'NUMdVMwfBTtw4x5fgtsus3co2hZNVoIjcNEwDrVZrIPtCczrIQvVoKtdeHkTYmhBvZ18Dax6E5cZVKvA//EMg9NGeDZnzwpV8Cqq1jbCUcKsCvl404BdPo6wawYcJwf3'
        b'faRiV6zs1TNV6xA6C5l+T0Pii/bBFWcfJ8Lim6cwiUf1cISePKM83FGFXc6dTSz0njyjvcNwGenkuALV/Yn4z7skcQLaxc9eHKaaQy60QXa6gzduwoIANhNcfH2cgpmz'
        b'RzfHAm+sDqaQZWBusNMCT6gTuHWh5uvg8GYVMWfJ0TYpO/P3Iepi/swIF1ojok96+wfR6jrPk2bAhXnevgGBjk6B8xn5MV5QNJ4GdJ2GgmBLrPFloxo6Es5liKhy/NGE'
        b'OMe6sCF4W6ULVnBYuJ+zE+6a7WvIaZAUGgSUkzhcRfwB4CLkyEKCFAEM1X7+wh5cWQiv8imUCbnz4TIqhoJlcqzZXkQnvIegq95DxqCzYtK1W61QOWocRLcVaEsPCcML'
        b'Pp5M5kZSaDSHpvRUFZaflaIg1Ir2UwIiOG/nFUKWLnQYTxu83tUR8ufLeGUm2zY0zxzgp3Ci6nUgLphdZylDhKuzn1sul2JNqjqFpocOOC4MQYWhUDgRsubjeWJgz6OK'
        b'jXj5p3vGftSISmUZZvyMBTivfXhtmYeKqV8LylyHtuKynleS3eOIISdAPe+Ev8pRWNJBIbYNgbNoJ+T78xw/kYNdFqiCwnhNhtrxGkcevFYddeA52RIBzsDxXtRDAS86'
        b'uVgtzPfHZYd22KY9Oj6O9tKU4XwvVOhHDmLXr2JHsWWD6WawBZWZM98GdA61GnDiQTw6hrc5lmw1ltMqNF4j6OgAdErMmViIepuhUupBYTgNcvDoV1DFn6D+R+PZSA9I'
        b'DbiRKNMgZsoCllDxWCIe0NX9BE6TIpFBmYBKTYNpBVEZh846sDUIV6Ql0IAziRXh7oQ2tt1WJaPThL05GlrUrAfcfDrofPBMwVPPKZAeYrrKJcuF3s7oHO2LRNxW+yDf'
        b'2TcAHeiPh+x4HtWuGUN36SFQxpGp77lOROt8fPkQ2lAZ6LgVJfY2G6Pm15ZvVNGDuZxFqJmUcAIqJLMbj2MyvQ2wYr/XwEiMy+lGRxOqxSt3PtPiUa6LbuOwloGcAQZc'
        b'INpqCEWofTmtw7gZqJacvjvggSjhjCYJeK5dQWfiJzaP4ZWbsCBxI7u3Z8jlpPdnWLRNHqTIs4pe6hJ8odfLu6fsuVU6Xe6ZJ/fpe2LJRTl/7UjoIH6Y/7b5HG8fclG+'
        b'Ra6aNixlj3tYkXlKaeveSuvXv7l588YH3wyc9IqHk09xQqhiUWzC5oBDluvmTglbe2LSKz8tCv3h+PCrJS/84SifeS12nGWV8GjL3b7Rbbcdzix+p97LOmrKsI+Vq62b'
        b'0+Y7FsyJMNvy64XCltTowwaepTc8vzddu/Oh07SI6TKHxS21778QHJI4tu1+wZlhef19pqb/1Jr8h29w0Vef9HlzsteHl2NSXroU+PE75/5ld/+Zd5tLnWJ39/rg82tV'
        b'p95cYtPn9ufPrlv3wsmP7k9a8MOK0mujP95nZN+678c1NT+tjt6XFt47/OrdEyZxDbMN/WMqJNHh29yTPO6s8jDKLjz67SLntwP2R5w5+rtwds9Xr7fcH5txz/TVZ48u'
        b'j2qZm/7orc1H9iUlpHz9etbPC1/65lebUtHC3D0PP157bm9LoviPon9+U/5G4pr6vB9fMV19zD9i07XJ7x0qvHbvje29G36bVGLudOG1m0MHvS1yTzhhPWDmj1a9Cta2'
        b'ND4wv9307lv9K1CE9/MOzQUxs58vm+h1beX1qS7DdjYPvD7grWH+nx/quyR9c5PtG7nvf8O3Wf1+3dVI9a+DgV/caDcPdK0/klhu82X8oGe+GPXzg7gNyOiHDzOc4L2P'
        b'31657dFD3x+kA83vpQ5zWJ59vy4orfnnPLfcxlem/Ss78ot/zPppyo1B3J6vj+ZnbGh447Xygy9Ybg75OYD7zGH75Pas53uvuFb1rOL1r9/Nuj1u9a47v4yuqv4p8S2X'
        b'1Z+d2Dfy2Q33y27eOrAl2iDm2eMvNXlvSrCY4Gv8xrllvVZIN6AHN85//WbATwvOT39ocK5Z0vf6EsUI5nawPRiLJsxBAkv6M+C8xkHCBnZQJ5EUdBYdIWYpR1fm1rIP'
        b'6uiFgNlpdO3B0/kSXX2i4Sg7tm8Mhx0d3jR7oLzDnSYcjjFnhj2JadQpzQROU68JKWoWMpaLmM9LUSRc0qyMfcI06yIW4bcxl4x2LDOVsoVxurtmWVy7iTl05DiRxZa4'
        b'+wQ6wf4UrbtPXyii/CQRvaBGQ05ibEnoSdD5gaxQdVDo4WDvrIAjUshz5DijxXjSGi1lhbqECkQOhBAv15HniGggQbsEJ3QK6qkvSxLa7eynFUA9tzAyGSwr51HfiCFw'
        b'agtx0CDiC16UDwV1iLISbrCfGA5Zu7F8LmJRs8wBF4KUALdekQTVCWNQDuynTjGyzei02uEnGNVQhx8lKmSG3hPo9HT8hzTVFBqVcH4tltNze/DBgWYJah8BpbS35Mlo'
        b'L7NYoga0W221lHBWPiJ0BC9gzMjbiA7a+5FLw9AJYjoOot4/lrBThGXXOmPa8GOnkZHkgvvaiZIY2qMLhpx5kCgOiuaxsXbYHdU5BDkC8RwtMEaZfnioQbsALSg3kLah'
        b'KZQYU2EDatCVDmkDzqfQ/lmDK3ie7BcoH2WpNwy0F05TN2doGg1HqSfY8NkaT2m1m3QpKqE9v3G8udaBRjmA+M8sRY3UqWMBauQ05olMVPE4PxAswzD2HAGKJcSfUOOE'
        b'1NkDycCPmdGvTFtEXWKS0FVdrxitS4yDEe31KKgwwX3uy6ztuCYGnDlkipK94BQbFU3JsBfLzoSDznH0BLxDyZIEOIDK4CAj+jmDJ0U53ePgJDqq3uXgQiwb2OfjsexO'
        b'BYLxcEAtD4TATtroCzOgw4e0EbZrxAGrjenEFxurJrtXdhIHiA6rKw5gLWAvHUoZ+N4iXEgn50DigLQRKwVk+7aBbLEVFIcwq+derLJu05qCUOaIp/HXcfdgDmvHMsjC'
        b'4MP3HcsJwbw9TqiM1sEDtuJFytHOG7fBDi3j3rpRcFlh8u94zigG/BdBZf/6W4c93rwLgia1dhE4o27WrtHEPCulRDIWlMJI8kggP4LkT/ojMhFI4A+BnmOAcTb4XnKn'
        b'wAuPxCICSEfgzcW8hFDRULxiM/aD0yWfrPAn4gFkRRkALYgnEE7DRM38h3/jKySgCqcmmKg9jMyo95BYRHyLjAWpQIBxyasDSFfAaQn0N3tJeOG+xIZQ4pio02VBg1pL'
        b'W5cGYZZB5lLE3H1oEJgjeXOl3kTRazv8DzpiqjrOJ3r/n/WrQqpTwmmaEqbt1BbKUeuVRM2R2fhPe73myHdndeI3fFwjKXgaUhb4hANSckTKU6Tgpzsg1ZAbvif04E0w'
        b'MyadcBhGJCZSLFQdbmBcuHhSqojEThCpDEYrKorhBEbIk6LXdEuU+abYhYfPXZ3ukxQTHi6PTExeuUrhrIaz1fgnqJTRMapE4iSwLlklXxPBiBWj4gkXYnfeYt1CxCfR'
        b'G2NodL86ljNayQI8GXahnKAwyeOjlE9PW0hACdzlPtRPAI9DZTyBjMX5EJ+BCPlKlTI9eTVLVls1n6jwcAUBsdHrWoHbR9Me5GN8kjxjgjOhxZ6Fm3ENacz0uIh0bWk7'
        b'vDd6TFFdN4pjS92PmI8EToCg2nZqIk2obGxasiqFgtv1mCKuenr8SlViRBrzAlEz2TOsBaXcjgSsO+ImwNlSKJR1KfjP6PSVzgraCXq8QEiDpkdr+kXd79Q7LKkrP6W6'
        b'96OSaaBuCkFA7inNTh3wBH5HnuuJ39E4kJl8T6MCqNbY0SV9QuC4YDanP7OjE9kQXcIS4QXdmAXU3DvNpCNmAbZGqQikaxxUm6jNi3KpiBgwL6W6Qkm/Qd69RqRugrPB'
        b'eAOun41Kls7ySUen0Sk5HEUN0qmBjgOhEkuilR7o8uD16JSFqwKdoTafJBcfrkjsLOLCwxP+iFzCqUi4FWqaYEb0a3RpfUAIYejdTWJfSFCRITc0QYyrsw2doI/vc8SC'
        b'e+hGgZsRnmgyaDIXf2/INpGSBP7JX1k+4qXLlttdLTxfa3EYMs3gonTCR1nO8qFD1u3xtp0ZN+r6tdd3vFlbPmRYxmXl3QqvqKNz8zfP+OW6VXByv3FT18zZUrrlo6Kz'
        b'thc+WHbGOPIF1TWj2f2++WH2IqdphRsg5fBXHmU362vnfL3o6pGyyZEzfv9dlL2k/+XIEwoZi3i7DKewHq7VaphKg866wD5UPJg6saOc8SjXT+2qrzKaORgaqHiyiPit'
        b'6z+nSobq7sIJOgsXGPfwZTg2TElMrU6U2Hg4Okd8KyyhSIQaoAXOUFllKWxL08TjGHByKKOqDypGlxnjbwkqUGhc4iWLh6DzPNRNjWMO8ZlTDSFf4wyPBb0zXrDXkD1W'
        b'CLmeHTSXaO8kwWk1qmG8i3tRiUyrkMER3Jsd8Q0HsDpHCh+EtsNFHWF2KmrTlWclwVSNQTugEhe1w8nbeVoXgXaUmfo87olOH0YkQo9OWCq92PckvWzhJlKZhYDsP8Lv'
        b'IiKbEJmky7m/NqnORIwunbf0buyRArujY2vNxX8eJ1urvKetNZP70Eq/74G2DMTDE+80YXir6YRdoIlf1ecbKMoRPTZ6VeOl96u4h301JDpJjWjaGUZdpWT7bDRd6fCy'
        b'7DnLZ3aIDjS6vs0pOjJ+pTJsZWI8ToXx6mowoGIIpuPKOGd6h7MneZ9Nb9OHuK6Tqrpd3KlHoaPWpZAgACujaTGT06LIF3jZ73FZViPI6y2Ds9d8/3CKAqdKSUyOiNLU'
        b'XtMgPSZKYEa1qG5kx1A72SpV8ekMx11bqJ43iyeWavbs0HDHv/vo/L/9qM/cv/vozEVL/nauHh5//9FZf/fRRZ6j//6jY8LlekSqp3h4rB6nTp8YRizDBJzoKEe5vXr4'
        b'23fyDO3sukq92XqWSPQ5pHqlRVAw7Y4x/Fd8TxcSGZatChljnF07zRbqM8sgbNl0whlmxEf8vZaaFTq/hyJ08G6TNYaVg023+KgniF1iTocmVit29WK02hY+hvRofsbq'
        b'eP9Jaas4ehIwPA7tU8oEbiCq5eAIh8rRuRB6qjAE2vAe3eTqbOfqasAJPhwcQtku9BkHKDdzCHTm7aGdE9A+3m8eqqLHDVCNtto4BPoKOAUBbeMnbuhPH5g1UuIQ6MOj'
        b'ragaf5/DT4GahQqxikXWoSYfcrKFqlGNOTQacKJ+/NRR4+kZlD3swZJiEzQkQ046tBATUyk/ZDk6wvwg9tpPUY5OE6AZneL4ZA61kJNjKmHOg7rFSiw+bkPbzPE+JsBJ'
        b'3l6CWmhhhsJ+qIW9kIvq2YG9HNTp7UFVsI+6IYwm3p7EEyElRuOOeG4tnCXlFG/RlnICHKIPugePIoWcbNdRxhHACuIDu+ECTjIEndUWRIEq6WnPGlQHLaQCqMJaXf69'
        b'BgoRfa4PbBtBcoMqVKvNL6APO+k74I7KSIZo98KOHKG9NzuZa4dSQZYBZxyN8AgQGfEuqBHKaIYqdMRHZmoNBwm4i8iRn44uwSkmke90gcPkzA7K5sjMeE5kwk9fDpdU'
        b'BJNwDto7zA9yB6GDsDuEOuSSM2AsAXNwDBVvxBJ2AWShNiymVYbiP0qgDU5AMZavS1CblQGURhqY4rcALCgVTJH3wnKZlTmqcUOl8XWm7mIlAeA8mDlz/quTA591tZB8'
        b'VJ46/sDXY2RWVgN7V39kEz/xmbh829YGuwspdmu9Tx4/ciLF3WxrTU3tJK76yCdBjc+duV1w9bep+wa2Hs0uLTn8aeWSvGNRsi2W3s+91OTxvXPwsIS67wPH1OXedd/0'
        b'cnHu7aiBLQPe/TBuz8h3P9/aIux9If7WvFVDq4Z6ux5889P252s3f94+t7Rm2u993Ztat3g2FtxODdj+ymubdr5ilsj/nvnKHOWa7c6pD/q8hR4dabn9uaL+59qvhjQ3'
        b'/jDrT/P2aWUXsxvPHnnr+zuv+t27+2vGxDfu9f4p6s33Q+ofTPjlzoylSi/zjbuv1tVu/MMw+/Ty9/8VpLCmhshgPsWvI5hdtkRw9YUzqKY3C5TNQefJobs/npV5OqGy'
        b'ZkOoiXM2yoQmBx2fZRNH0Zz+hmM2U4E+AipdiDwP5dBKzyn6OlKReRiUxTqg2tBAErwpRlk8bIeSJHaMsKPfShLlKkYndMJcw8T04pQZA6iQjioMO84n4JIBLcpkdAga'
        b'HIilfwY6RCRfKeQLaKvhSialH16GJ4EMmnlUvpDjIZ+DmjGr6SVvrF1gITtlnBA1FV/ZiWedKeykts2wuEhyQZKMzuMreLTtiZ1DrdZptpvIBX5LOP4+l4NitAtlUos7'
        b'Kl/grY4YJeGiPnBaHTEaCluZvTR/VB9lhhkPRzI4Hp3EU2nSSmYuPuiPWpSoAOUIUIDKcMJFHJ4NFQsYGz26AOfwcwZwDrXiB6s5qAxYRguDctYZ4vltwkEZnsToDE5p'
        b'5Vh6BfL7TlNmpPLoCDqMr5RxUDBzKb0Sj7XbPfiSYOeNL+zjIA9dWkEVE6sAyNPqS1iRymQdyxSmBahMT1jkY/yUxUosBlN1IrJndSKcqA/EAEkCGIVHEqxWiKlplJk1'
        b'BapcaF4mNGzRWNCYHLU/+Al87yPh0XrLzu7HOPdADeoJjWY00RWj0/I66SPUzRDXplCrg+Rpgw4L8Kdrj1FErnVygu5eCqyEEdWDBlsFKvp0wZS6JQ4L8gm8JQubPT84'
        b'2DNwto9nCIPj1GJN3ZKlRMQnaaIRSVjkLWOdcD1qr9SGZupEUW7vjElFIaqIvZJqVrRWrHn6/f/JnJ7mTdQ+kRpSUmpoIRI49Yvv9umhRGJmYDuDGNHFwt/EyhRbWJgI'
        b'ZoTRTcw9Gr9OylsPlPLU+QXP5/K5OiEFS9CxALpY9psjjkeZpt38dk3Uv5X2fGeCN4KwxdC1KsVqfC32maBsGeEX+UzQtgjWFvu+47MFQbuM6kU/W0f11n62ieqDP9vS'
        b'z32j+kX1jxpQKSPUcTslMXzUwKhBWVKCtlliWMJHyUpMSqQlVuQVNbjQMMptJ0HvkmB1d3jUCIpGZUgp10ZlcVF2UQpCKUeeK5GVCDECfqoX/rEosYpnf1nh1KxKjEqM'
        b'Y8RR9lEOOL3RBBmMpLjTaKfpTqud1jFSiqdFUjaiXrMS6kVrGSOJcolyzZISdE8xt0RGzdNjblmRSTOb0kxQKLaY6LQHozsJnN1vUDOm6d70wBlLr+7xymR3ZXoU/T3a'
        b'1XX0aHciBLuvVUa5k4nk7Orqhn+weD1GIbolDgwKDrgl9vaZ431LPD94ztxa/pbg4YnfjUiWYUGB/otrxWnEVnDLgCqdt4wYHm88/mgQg1Vn5V/J1o1kK04rJbNvH3nb'
        b'T+az2CcwhGE0/sW0JuHFrXNaaUdpgiEeC2Y+mBWXnp7i7uKyZs0aZ2X8WieiDqSROFWnlep4P+eVyatdoqJdupTQGSsNrqOdcX4KoSP9WoGCgqWFE9hD3ED+QbNn+odh'
        b'LeHBSFLo2bN8aAnx77kR68jyF0wsx8p0nKiz61j8jldCklgtnxbIkBMPkLKahPgEzvH3DJs1M3S291Mm5YbX6tJOVX4wocuDs9OSlcpZVH3pnIZ/cmyAMpam5EZSEjpS'
        b'wgWsJWmZd2mPB/30V+pB7x4bTyHrlAoZbml1PaQ9Ke0M+bZLIpNoImPS6sk1/Zm7PXD4CzW9ZRgVHROhSkynzU/78r8fzNBTOAhV2eaMgKsGtsSRT+3GJzGIP5SwQqBR'
        b'Iq3Ld/jRGJEhD7AwOIq34555TJTILSlhak3H41l/SBR5zWFYqp3XEWfNs/qDDppxJabiT8qhPUsAmdxznQIPHpdLrSHbsRN62LYTtXs3GZFfkFKEBnYLVTDWtCiREGio'
        b'AqdhEGWIaTHG2jAE48eGIWhOB7cZ9mDF9GExv/Hro3VsmYwKiB02kTX4MbbLEA2JrzyFEjNQ8UXp3v1GJ3mXeSK38/BUPP42Ms+eeMckuZ29Mp6cXGVMcB5v/xRJsqkr'
        b't5vt/eSb1VOU3Owof1I++pcPuZ1P6F96wu0xTzztSkCS6FpofWZitamL2YRYOLaaBEpDMKDvSbJdsse6DpuUtPjktPj0dQzI186ebMKEXotsw/Y9Ww7tyeZM7iFbpT0x'
        b'E9uTPc5e4dxxuDreebSzq7v6lp6T6TiHdaW3qlPt+Ho8/Zolra9iDDJCXbUeACFY+4xSUkwIvc1DDyjcO8fz00nWM7yDOh5fb5k6MBzctQSz3WEaCGSC9ii+h5N28g9f'
        b'o1yAxHJPLabUDSA6Ip0MKKWGKU0H9YIcROsBBSBWV5zOmog0tdeADkEFbR15SHQ0qasqUYd8rcekZs8M9ZwTFLw4jDABBYV4hhESmBBaSu2JPaOE09tIbBFi7UNJm9Qg'
        b'Kpp+06htantxzwfcHTZkei7BUugw8dp3WVPs9boI0B5KYfNUyQjluiwx9qx2mlvik3pGLGB4GFgg1fDlxkUkyT3nB+uxhSfJQ9bEp6/HuiTtuPTHFJ4tiHrmEp4wPukR'
        b'ievog/pXOHv9Y1YN5ME6pAPfg4x8dZdosT7YsZSeGqUzjwcdpO9Oz3bCadG7atGUup0T4OZRS01KzfDtkm7PfaLmWOzIl3JbRkYnJifFkpSeYE8nsohRN9HJPJAFFUA2'
        b'OgJ7/WAXFIk4YUoCHOftJqNCZobdAVvhfIePQz8nwWyAirk4kOtSqEV1SjW6KJTIOKhHuR7MB799MJwgGi8qgBb8OkQC51CumDOFLAHyhTU00h5Oy0Zq3GtHQTkN8Vrw'
        b'BEjOAANfgRuHtptBFjqG2jSm7eP9BhPbLzX8QgVqM+GnB8EhFpHQ3guyZKbUYKyEfEd+ehI6oCJ8Nah4nEIHdbUj0kwb8pJiahpMQFftnALn29lBHhS4QJ4jwdlEtehC'
        b'GEF1dZLg6u/vxc9e5UVt84GpQUoNOKgKGjjYbTmVnl3cnM7CCtMcw02+7D+CU00mvbJZRRBD16J2TRyPt7NvAOTiGrsEQ47/PG9RMMolEXHQiqrWjeDQVbEMyqAZFcW7'
        b'rTzDKQ/jRKY+2j6icKrx9hkWO9bEqLa86V40fqFvf+8xi+yyGpbYZ3l/VPWy5U/Gh1ybfMZ8t2n3LzFjXaWys2KvrO2e/O60H0+0/7Olz7Zv71S+eGZHw7uFscH2VfdW'
        b'r79h4D1p3revR6d/0rgj+bdwm/VWx+LG3BlnlLNlQvnHQyw//nLLBLtvv1tVknD8p9aDzywf4fVln8E/Pr/k98uXYt5VVb0oi7w58kKYIsHlx9EHFKbUAgmVAYsdnJ2Y'
        b'M8MJKEJZgusCE+bMcBG1zGBYxgSE2ZE4ZxgmwwHOLFjkhrJsqSl5M7oE5xxQwxatnwW1325EO6k37QSon9ThHtJLqfF554E5CqPTeBSWqt1DgmEnP9MaimjCU0ONO5y8'
        b'xSgL6xDEzXsmOkYtspsyzGT9UKbW1ULrZgHlccxkewk1oss6RlvxJhdms51tzBwsDgWv0gUMTEB7A5ycdQADR6HzDKpvJ1xF2xwg20qD8KiFd4yNoy4hUJnmypzkRZxo'
        b'0mRqSx+KtjPbd/5yqCExOfh1Hl9ejAoDeC+VIbWlJ0HxLDzN/XHtI1H5XN5tkmEnnAjjf8vWpoWg89CnMW20Yra2R2IRc10l8B9iXvpIIpDfAnEEoXzHZoLA99Oj+ajB'
        b'19RwNHF8T3bj1Z0w3gIeq2w1D3qisvVX8N4Y9tgtgzAKcqcPjKrQgFOjvfWUoZZZ2fkpxN2uSG3EDBXiPTP4lpjwpt4SEwpVhWFPrrLMEZX4pd4yVDNvp7XxPYSzm2u2'
        b'Dn9OG87OtEQTtZ5oyrC1d5rHmD9l0LqItpX445qetMWZUVHKzjzRmt2yB8udVs7qrnTGyN2JFOgeroUPCe/hgN5RLbVoQa6IG2R3r9GunIeM8pco4h2yaDppxXS1pP5U'
        b'OpBaetWy4j5JDWKkWOzZHqhrI5TymMTkCGIbkFOOVjUJpT7vmIikToRvXRlv9ZWik27QEyFtevRaJvimazlcVzMXTj0+mfie+CgitXU0RQdtHquD3I5yu5OqUalsaLCX'
        b's7PzUIUeeZL5OFD/4ggymnSYnLUpM6pKJud2XO8xPe0zHcyT6iGg9r/qzEPZYxp2wZ5enuRcxjMscH7ALM9gR7lG/WBknXp9tqhDsX7S1uQU5mD9mBTW9qTR6WFHfUxy'
        b'5J9W4SMt/Dh9TAu8ph7VPaamoeLuSXWT41bxDA6c6d9dTevZB/kpVTcNgRZrCi2JMRmw6nFD5gXWdqMpT3V4eGByElkpHuOcvTa9I3dKcUvaKCKROESTBUI7dGPSklfj'
        b'poqK0ONFnahiFrLY+IzoJM3Ix1Mzivjq2K1MTlLG4+YiKeGGi6ff4lbWWzCWjK5dQaFbTTWlc2RC9Mp0th70rMmEBE0c7+omZySzrD6kDI5qqE51famiT+YmXhR7TCdG'
        b'lUbnGp3tjCxWrzrHdiR3eYhafdJQvBM/83U4l8REPPki0pgSxW7ueW1RKpNXxtNO0CpzKWnJhKmdtCJuWnVn44nAhn3PjalDgCgPxGpdREpKYvxK6kVI9Go6n3T95nue'
        b'O7PVTPEdhKtks5bb4XeFo5xs2XK7oPnBCtIZZOuW283yDNQzD+11AgHGK+yfIjxB65I1U7vUd2EsepyrZyedUtqjTjk4kKqFRpvReWOsyWj1RsEMLqylQhDVgxQZRA/K'
        b'6W8oD08c7NtLTVbR1sdRo0oSOIuTUA+njLyYZ8+VWDhAfZpQBbHvE6cmY9ROn1sMp2Anw2SBwl4MliUkMlRFpOnEtEVMBR1tQ2ViHQU0xk1FuEKgLJFgojPqBEKsEaoG'
        b'FfBzsl/g7eg7X68aum6mmuTgrKclyrdNZN5X1a5QPDRZq4hiJXQtOqZaSC5th8LNfzErCm9BWWjm2XmjugG9GNCEQsK5u1pDA07pIlVw+6FKaIYTqWodlzhFFa1SkVNv'
        b'tBdVDfOjcDxOvkFEybWjeBUGUAw7jEf0RbXGHcrlDKztV+ILx6zQDnQiFB2JmodyZ21GFWgbOo1fx/Hv7FVrURE6OStyBcqblRY/b17CirQJRiOWofJVcRYc7Jo6AFVa'
        b'oyLabbY4tYuw20oGF1JMsOQPbbwL1GyheBfrDNAuveWC3C0hfVHuDLQnkrim6xRpBxyDEvKZ+GyFm8NOOYfq5lnaEpc/qnyHxGAlsXa+LEPjOLYaTqrC8IUIqa9W01cs'
        b'UIPuhAxNUalCoSjF1ByKQ9WtrmMGINo/6Ro1DYsWmQZtRTVSmoUZ5NhAvZVcRdhNUeZAEz2wSAzLBuurafixUDstaAjuS6zK7zSdk4pyKTwmKkRNcNJPh4sIClHdXDpg'
        b'cLJ+86ANFZDy4JG010Dpi/Ks8LjOg73BWH3O4+FqqukcPCEqVAFkeBfbQHm3tLzVmPVY/1zAklQnh3bIUIn1CDjZGxWNQ9Woyqa3iEPlAZaoygrtUs2kKc6D4g40o2NQ'
        b'3lE9AY5SoPTzU3AHbYMs3MTUgQ4VR3KwM9gkGOVAKw15SZrurmN28fdR+Do590QnoimYaefpgtus3BUOqqzQnqnOqlCc4BRzwTZKg+Uwz/vfSjvY1xqXudqajqfxa3tp'
        b'jTlcBqqH3ZEe1AeHWrnQKahRMoYbXOHdjOWmg+Im3JAQJsZ7nFkqKKuwblU96E7AvCuBt2dYfDBww5WfD256ht9f5KGw+9FiCj//9c+Hj/X9uNR5T8CeyDufWsUfuTSn'
        b'YYPxIL7q2Kwp3GeK3Rbz7r4/dVjV9zd+GfPP8sXl3vYJAd/Msm5s9Nrc+9j93HFvzDgo+H5Z0nvU1XseqiV/zhG/9dOn/zpy2eP1Jalf7nX5NFF57aTfwm+v3L0x78c7'
        b'vd63mGR4YMM3L87b7/t67PYHl96bH9e2zW3Z2s8a714/8PPd138QP/xxx5KvBvdbfC3kp7VZP/df0nfx+9O83w6SqKIXDj5eve3zvoemf3fj2PPfHfKruPrM7/zZaR4f'
        b'bj1emBR45doas9WDrvhMvXPvZ+tfU/746uXAvhvfeWaEw0L52StGL4xw271h6GVu4Y57IT/VvvZ53Nchjanr7n0MO04vWmP6cOK9iLyM/qsufO8+886uN26jZtvqA1uv'
        b'zr4t2mL+51vvbqqe8pxj3NK4s3Ocvv3lt6hXXz38XPp79p9NWJ6xTv7q22/+w8BlVMiLVRZfNV3LWFDQ8jKc+8HJvnbS81lvVl5ZNtE1+MW66f2+c08ZvPPgrwPPeLzy'
        b'ecPHjXmTvy1L/njBy6+/H3Tq19/MbcIarV+NUtgwFouT6OhwHasQtzqe2IQsUCU1NqGmjWu6xCJZ2QmwD2VbUSe9kU5QpolEQk3TZkIdKlXHfJugqk7ukqgqleDDtA2g'
        b'9p0lAbZzM7QGHmrewYtbCQUBRu14/l7UEJaoyUrgNFRQwhLYBvuZOao4mkRsa2xRBCkB1aDtAlStn03rtqj/aho4FJjc2Z7lNopeHgm1qKQjmAm2DaB2tgnoAHUzTF+E'
        b'a30OtTkw7gzmfokOwy5mg2qCQ3jiH/AkoLQ+qE7MSRKFoZJRtFU8V0X6aShGYDfa54KORTJ8hx0zXXTtZ9x6B2o/Q/tRS/ookmwzXETnOpFuwBEo6mREg6OxtID8ipla'
        b'IBwa9g5VXqLe01E+K+CejSlwGZ3FtzgSMjexI48uoTMjaNUD0eGZBN7FfXpn49u8FNo5UShnbhLs6jBiCq54Xy9JpwF2VRvEfv4+KLdLuLuI0Jq0u6KLEpexC2kJLJYh'
        b'hs6Bt5YgLEKMsTDzEE112EitlGJPdM59dEeoGA91actYwWsgezOcI5xvLgFOCpz/VEGOzsYqpE8dkmz+33G0y9YgM+4jsmFPxr8t3DRj3kSgMeiCCU+i1y0EiUjKW1mQ'
        b'aHHxI4mIRKMTlgoWl04iyomLpkQdW24hshVs8W/yY0Pj1QlnhTUvNTAjcWSCjnGRxKE/IoZFsWAmsNhyibB+aA+mti6B04FPCi/vsJmlXe0cg/b0XaAbFX61h9DwHqLC'
        b'i4gJk5iRezRhZnI/2OkaMZ+iovpddQi2I7XtMf8PLkaiddoRPRFrPlYhfhDeTW8Ijk7CKqvySQY8ai1QayhEP41QyhcF+D9BDSH8TIO6qSGOgRRfEJVYjPPT5XeEXZsX'
        b'dcKOy19o1w2aAipRvWlvVIdaGUDdKciKIju8Eh3S0Nh1bPBoHxxg2kstOj2CCQrx0xgpHOQYMeqyUyjHgFxKd8YrrXMGfvMl3uXDVxig49A4Ac7MpUL8SoKAh9PHesyF'
        b'OH4Qh4pC0FYKRjYYlcHVjjM6OM4vgXo7yEPZVJ16c5lAYmbklwzCTX5QhnIsvqJx+XCKHImXQziEtwTYhq5CGy4uQU+FksjVsFdEbPUunAtO6ST1o1oLrd4yIyzezDfk'
        b'oZaD+jHJVAhShqICB4U93gvE6/j53rAVXfFnp26V6+GMH91KDDiJDTpuI5j0RvW0Pn2MUGYIFIrRieVk+ebQbm+4wsqWh0qhneK8MYw39ylQB5ehnpYt2CJFq8eg3KDp'
        b'JtNZjM0B4p/fBA3aaJENwUNQDos0QSc3TqDIcuookwUof2oyVNNKDYWWZBmlTMSZGW+094I8dip4aeJwHUUNnR09PTSaqo3BKFsRQkh/5kMhlM4P4GEPyuKkQTyc39SX'
        b'Nrl8xW5uAM95p4wNT/rRM42ptbdChnK4RVNWmYfPej0yg33ZFkuRGOfejQ/3Hec1letGeKydenJOTXhsgycbd4TbyEdxUfwOoS93VEt9jMXJL4iZn3DKzIxK849Piq5V'
        b'kx+LE/EfXdmbie1+uUSH/5jid46c35f6IrNzRiON6AvFNPiBDx4/CVohF+VOgh0ZM7xEljGpPmmbk9DWgdzG0RboXDJqoVUbGWjK4Z6ZKw0JT3zGqzer75FeNpwjx3k/'
        b'rwifYhHXl6MNKkxxgyblmB6Q/4JgO+3AGahxso6aiPfHVhd0cA3DX8xx34SvpZpieciaj4mfjFVWmtfvRjQWjFuiCE+MlnpxCoEp4SVo7+yOIXQEsqdDfgJLah+ckGh1'
        b'wz5hLv1RNR0MqCEIZUETfsqQE43kN6qmwvEINf6jiamfMpBIgGgXnBdkvNwfNf1b3RiLuzENkXUeyNtzPNeNdpt0XH2njiOtNBxVoUJZBlwwF0j5oRyVT4SzGawGu6Ad'
        b'nZClidZNIJhXWG2zgDY6c9DRdVg/bDKBC4bc5JE87CWQWCVwgkW7taNWfxkhZdvJcfO4eWkoj645W1ArypfZ2TvAOX+ek/oK6AoqXYLfyukU3rwRlUOTiy+04KsGvtFo'
        b'Ow/7IAtdiYdRIkHpKSYswauj5/vttp5v3d5y6GHF/eyt2X2z+9pej3hmwjBzy+ffqak5vmvbsKHb8+a8WhF1qnbks2VLnePeHH3tRGSBW3bZqYFuzssuRsYXyDZvv5rZ'
        b'EL560a8HQ94aJsp/X3Xzl02bbtYr/9FaOjH3nXeu/GzgeemsyxfPytJj9pR+taj0gumGzMkNTsfh+Cfvf3q3ofCtuecCBq10WFGQs7VXcSoa07Asxfm3c/vjTv2k+nqU'
        b'zdxP/1jQd+DDSuvFG0/drfjD0sDzudBPvkwYNW+xwemK08tcY/6Z8Mkrp99c3j7wHX+n05/Zn+n/jzfNT717ea7h6y9MmgW/nuRvTHgrUepWscgpRHarNbt5a8IPt3Nu'
        b'QO2uhNAgVcvMwmX978ytNRt1LenYkJBva8Z9zTW88uZY02u3Q3+xKYg82fJMstFzTnbuVQ/8wpfWNEfm1zfWf9Ky0PHT37fdeiE2bnbfUU7NH6EPjw681u/h4PzNVTY/'
        b'XX3t+rLPl3wX8doHmUn9V8WXlY/+McDu+qe1jd9En3C7qzT84OLHAz90y0jwXP1rr5qXdiWOWh3pmaCa8+3P15QjMoag0O8yPz1kfDLE4Y/+95I8GtEb217JqWqcumNO'
        b'3vgt0YUpBxcpfV69Eln79TW0/aRy/137sp1Z62xv7NvG/+y9Z+9807cf/qvQ/XS8Q+GyM9If7025OXmNUnbr+YZBz98adePrJQF1341/dVTmfcPrvtNe3u5VnTHW7CuL'
        b't/c+tyWu5ELv1nmmlzcEvwqvflz3/WTDz0IMFvxgP3n0dwtbXz50d+rceclOn6/6Rbhp/acQk/RN6Df3jOd8vWn1sye/yckofeu1oLHOGU5rJZZf3ns4JGT2P5a+/Oj6'
        b'K8+6vfLRe+0njXJTt18JWXA77/3TAcGp+ZvK917oW3xzi9lX6+r6PHPDzzMs619Wo29/vDzSPPBd/ofR068Niu6/bnXE5rFlKzbbKB1t1m+sbzn43aeXPsg4NuKnC29M'
        b'vXblypm9a+rWhrs0mv6pvLX45x9sI/9ICau+VVPWa4XLb18V/7jC9PktI+ZdO/3u96v4sGvb/rhf/eK3jrWX3ng45+YHe2orRb+7fxfzndeX2VMMk9PCmlyq3zSxSX0p'
        b'6YXS9X7rRWv8k61CPvH6/dcbMoObt79JMx/Q99fPpn3gfNzph5IXlP1eSyoN+SR7v8GBiPzqE9+9HZDbf0WvdJelU0bsaEnyvf1d0CGriPvlxUNjJ41IWhtyMqpPUK7r'
        b'mqAXz10rkY5Z+rPi/edDgpLa17z9wd21LzptnWTy0/Jp/M8v/zItYkltn03mX011vL/jl3OBLx4cO+LR6o8PbK346JHlq9EVzqO+Ox9/LvpW+JlnHj1z/r2gK87t0vd2'
        b'fvLFgAmN10sqr2b8aX7708F7zO+bvP38PaF44Mbidx8ek2wM23AQ3d1wy+Wbpl/uhDfV3BG/Y/bBpJ+qBq8Ya/Zlduy8/tffcZhj/Y3Xlt9f4yt8Ht4fcmtMmSr91GCn'
        b'vAchrn6Rm65PMP9EZTjRcfOGAx+eS/7e5XD2gtxV3wW8+VJoo3zh86H/ur3l/Wc88l7JU6yi/hM+sBPlqnlLUBYWmwq0iisjLgmDbUy7zsOygEMn/xBUBUczekMp9a8Y'
        b'iQ4hYlI1MeziXQFlqJkhzlXCAbTVD2+Emuv9oIYzdxXFokqURROZi7XrBl1tNRWdZO4e0ZBLyzsXKi20umobnOwwuGl01aXLKbjaGlSGaihTZTqqZWSVGqpKtAftpOqs'
        b'bV84roUolMjhFEEohELUyjxGCmCrkbJDzOXhwELOFK6KZlhCHVVMeXQO2pXOOHentEAF2e6bqI8N5Iq4sYHj4LQkRJRBc8KFaZ7lp7FMSAi4TJhgjxpi04lgNhUOo11+'
        b'/vYSzjFZWM5PEC1mUYdVKBsu4Y5xwYI1eSq/D9otjJg5jYHUHcBXcwiImxbAbdKsdWoby5bx3jLIccI6bYGfiDPEuytkWQbBMainVZNAm432OjT582j3SM6URDe2hfdh'
        b'eTehU8S0SRFNxOP5ZHQYN+MllM307Nmb2eNOPjhnYwHOoaKFHnCRwck0oFMLlPY+sCuFmIJhd6AhZ4EaRMrF6RNQCfVX6o+Kh/hRSBSOM0i1hSuCCJX40HE2azBUQ5Mf'
        b'NAbJUK2dhDOCFnRxFB5rvaLp9YFQD41KAvdohPvFgDOGXeMFAfJRNfN3whmWov2kdEYKaCDVh7OQiSvXJuoFRWpTStRc1KxjZEGZqAW2Q4WC9fuhDCDyMB7NCmM7e2LJ'
        b'sLIVwSE/yBxhxixYxXAInZI5+8EFBeTjFjATYJvtUmfURm0x/VALKlEG8uikMxMYavgRDOnzFOxaD00+xMpDk4c8A87SRoQKTVC5xwiKK2MRAfV+uDDbOsg+CdFnf7RN'
        b'jE7CbtwBpATLcN9fVDr7oLMm+BYOXUUtnJlENN3SkDaSjcEwGTrL+zr5p6J6bzw+lQqe6xsqnjN4FoPzabdfh7+ajC4ROYVDrauGsZDiA+mufhp4agPDZDz3SkRTyDxn'
        b'l1tWBHWgLhqgbf4MdTHQgo3Ik+goqlH62CuwEIVK8HyZgmX9ipHMu6oNjz4SIp9vgOpRJcdj0agtfBBbW7aPQ62dLHeDoJxY7urjWHsXoBoNICNFYwyDInQMXYQcVqy9'
        b'UG/f2S411UPUG7WvZUO5wXi8zA43Qqo/LpgxVAxIFNDlUNjBynUhMprUKcCJ54zciJ3xIiobt16NA2ljIHNW2OPeysdLXryADqbHR6OTDF3TKd0B942zD0VAHhTImaNC'
        b'UWTkcuaQ1462S3GmqYFYiFsrQ9U8HPbdzOybJdItMgUepqQpOAOUZwplPDTjjPfSAi1DhxU6FjQsTxajS30tabKR6KoUj31SRxHk8rAVK4bem+ml4YuT/JhJXsLJfM2G'
        b'ClC9GHYz21pvJemUNP9AZ6y/beVMXUTSqegiNYoJJn3I/IcKdJxgqXLoTCheHEmCy4KnYnUijbi7CagdN3lWf9Rmxuxlx0YTUNIOS+p8F3RgKZxlgc1X4URvJtZLUT6R'
        b'6l1xOrTmmdPhqI7hV5RBnQHRASihHSVBu+SsoC48ZzxjLRwU8JpzEJVSE6052hmoJEioqHIwm514FOKic9Z4uYX9aPtGZsmtsoxR4p2sGHYpjNEZR7hAVu9GfF9fC7E9'
        b'nID9bFCc7I0qcDLqawb9+y7gIU9AB1j3VcNRdJoZVCET2ghc75AFbLzUJFuQU5oMaML9g3un0JJfYWnPrjWOQwVKCha/GY7z6BBZjRrN2A7QYIJ31yYXyLXDswMO8RuG'
        b'Y637IhynVw0IK4gSdtn5rrEXOEO0V5iHdkxS4BWVIsHmwcE5xJc1iFhYcsnQSF7KmQuiKLi6mPbI0qVw1EG7WJjE4q1vn8h8wBT2+N61/ZScL92h8KLKVkXOFp0Wuy1Z'
        b'TbNfBEdj2YJO2gIqndABPGBhnyWzeu8bP1y9HtLGMsaFvYrK8KgI7MWaK88XXSJ7LWFQlgoLeCcohdNsOT4EeahCiTt87DQjyF2DP9BMesFeETpsG0wXzPAoOE1wyCkK'
        b'+RK4jI5v9qDrlJ2Jn9Yku9ZxqiB34un35nO8ZCpTI9yQQ3goMJ65BZ2hHdALr7D7lVBA+MIqUZFgzQ/Da3EWXSXC0IkQVgufVHLHzLl4M68VjTCfRC/PG52iZd5Q47KX'
        b'p6NSqLNIt2ObWjVehgjelwvkBTgqfALw8qyGRZ4oR+emSNAxY8hnNvdW2INnVIchGk6P5YglOgPvf5Rg5CzavYHCG3eCSJ+GGjqhpBtw8+GM1MUC7WACVA4ql8nonU6p'
        b'dJW1xLNzImkvyBJoLfgNRLsM0i6lMyIoX7UPnGQD9ORsS2WgQj3DPOGikYBOmXnTayPgCJwjF8nivY83xQvsLnR5PlsImyDbhz2I1xBUPpgzHScyspBRkSwK8lM1gLcL'
        b'obpT+Sng7VRUScs/FdXbaYpP87GECyJ0DE6gE5vQLob/WwhbUSsbyYNRQVeEebwlsCUNq8tVaIeM7H14MrXwaKsTqsmYSkdj6JR0GeRpZB8pJxjMmZeynj12CXbH4BXd'
        b'l7iyn+fRQUd0aBLaTkfqIIKYjeuIR+wBhbFvABkr+HlrlCXCEmJdFB144oE4VwU3HLZzfD8OdkhRGZMZLgVBuTIQzrlgiYGuzxYJotHuKA8PwxLWhG3ovDU0OTo7k+lf'
        b'zqN9UI2OOY1jwBMV0IiqZWQGLEsTFPwgqJ/IeNvP4fG7QzkeavHaDrlGHfWyhSKxO9RAA62YC15cZE60YhJohMZBQi+8btWz6Vs0BBVQNptAJ3sytJsFLEPtRvtQaxgt'
        b'2gxrOKt0sYcGbwVZe9qEYNTq3RsvlH3YTnZuBTQ5BTKDxKp1m3gojV/J5JlzJl4Ev9gGWhiEsQ5+cbNaVBRQgbPS2VelwLMfS2vCHD8BlUC1O90R5m70V4vMPuZ2eFWb'
        b'uwnPyVbRJCiZzgSDnBlYHO9wuw7gURZs88KznIGtE6XlhJ9zgITzcBXW8VNwvXawTagBnfFgPtmw202IJDQsDBR7whpTaozTwpBUo9Noa2ykwvK/g1UrecJ1hjvBImQl'
        b'adSiTw98FhA7WM8HPls4eymFC2bww8a8FcXXICgb1hT6T0KAiKkXuFQNQUw+2+Cr1kI/Qlb+SBDZ8P0eCdJ+vPxHwdyCt3gkFoz/FMQEstiMHy4M5/vhTwMeCH8KpgRe'
        b'2AQ/YfWHICGfhwuSR3a82UMBP2/BD+It/hRelkw2pqDGFJ6YgBTzFrztQ0EyAP8muYn5Afjd9jfByArnRf7G35ra4rIQZBG7Rzgtg8fkja8OwPeSdBncsRSnYY3LI8Up'
        b'mv0skUl/Ep4z8dOgkDAKdjl+H0ly5m3/FEhpHwq/S6yl/Pq+PZzjsJbXIWN9UsfpRB4/j7tqADEpEvxvPSdJmdxdG92zJP1lwBnTUPcWngQWBwYqxPiNOpDXmnSBJUlL'
        b'4Ghcdchsb88AzxAKRELjoBkuSYIWTISUMI2cQLFzOOv/E7iQydoGKiZj2UB9iikVxBI1SvUfYsP/4KcbkgkCb2Yu1QCP4CHNMWPyI+upGiARW3rVGH8WizRXB23hjCmw'
        b'LGzzGNNhvzc37rDgC9yUJRLIW4VausXOG6t/K40fDygiipKqPxvpfDbGn2VRJvSzKf5spv7eXOezGlyk0kgLHGId1VsHOESkAxxiU2gYNVILHNI/aoAWOISAjXBRg6Pk'
        b'fwE4ZEihJGqUFjbENMYgamjUsB4BQwhEiS5gSKzC7pY5RdmhXNUe0ZHx6Q9cuqGF6Fz9N6BCJrKY9NEK4ZZ4dlCw5y3RrNGz0srIoK8gb5X802N2TGRBlaP/EtCH+qGJ'
        b'fx3MQ5MdjeF0I2AeaVUs9obAbqSdpEBCwZ4BQaGeFMRjeBcAjRAPj+Do1M6R465pNaTCT3OrmxbpQlOQB7b6UtXCX3Qus8KoUxqkH9Le0sXQ0DRO2jukRm+TS/rycEs7'
        b'T+757yBfdKOJJ/+6c9IaMBTqIbOGKVErwefTIvOhIrSbnlvZYPE+V5YxaHwqz7DHKjf1if8QtoqVxIIz+/deX4W/8MLGSO+IGzH2n/hFGMfc437Y1nfiG9ykVeLG0IcK'
        b'nkpWdqg9zGEoqtR19oFqcz0cnc0aTxAacaVPMCAvOdkk19t2mV5PiaBhZaiBFta3j5HXd52QNPRndYF05CsEJoMsr/91mAwC9jtE8rQwGVG0xAQHgDjt/ycxMjTz4AkY'
        b'GZp59MQ7Jj41RkbnqakPI0PfDH8MaEWPs7Xn+/8CRkXX8CwWSRCRRIIASJSVnpgh7WM9IZ52w7Xo1M9qLAuySzB8CrxT2OsP73kSiISmJH8FRiI+5n8IEv/vIEhoZlwP'
        b'AArk39PgOHSetE+J49DjBP4fisPfQHEg/7pH3BgEhjJftwY4i5qJ8bU7igAUQ6H/PO+Z6ASl0+04wEBXYacMqtA2VBD/3IeXxEoCyfDO6BbCCX7vo7iYJc+8e+3Na+9d'
        b'e/va7WuvX/vg2iWTnKKDe4bsOLd92KHa7Yr81nePZI3YUVt+Ltdtx5CyrU0G3NZ3TOetTFcYUOuG5zhUrPGUHYBqibOsqje19djFLe0a6x+7jIb6e29gxqAKKAzWPWFF'
        b'V/3ZCeuCYYzuDfagcj9cgRx1RDvvFruB2rgGeaKLjBVhHNrTOVq/JUrj4PnvOLtqI90dnyTieOlGvEt6kkD+eji77VNJPl8Oerzk81dj2tNaeY0M1kM8+yxDTh3P3i0n'
        b'bTD7UD17XLcAdsnjHW9XGnaZDzLNnCDOjDsNu0hnMiKfxcjU0pkhlc6kWDoz1EpnUiqdGW6W6oCYbepJOnt8WLquivj/REx6Z2AutcijDtRejTcJEjH7vzD1/4Wpy/8X'
        b'pv6/MPUnh6k76hWMEvEOoEtC9pei1h+zZPxfRq3/V2OtRT1KflaBzIu9DTWs04m07ptsFmfIELqInd0YrqIrarLxEmgO8YbcIA3ClrcvFFICsIUE4EpKXeQJC5QRutTH'
        b'j4F4laJLXAeIlw8064ZQB6JiamcaEphIArfRoV40dhvqUYGRagyR4g4oCAmp+riawGulD+0JYEsg/KGHjaDNJ5rxvGe5OXeEh0KOtyMtMVxKWAg5jCzVx4ALGyWdCful'
        b'KiJ4oMwN6IhfJ4kX1+SQP414dYRdAcyJK1hmiKtcACdotC5sh7peGvZVn/lzFy6f57RgIQnd9Q3wR7Wh3qjeO8DZyScAp+IioEbZaJQfHMINQpVmiajAkbpPhyQpKHvH'
        b'QdTC2C+ChtMC4W7JjNdNG6dMYlBTRqeRwNPdozeQMHAxF47yDVHpgADKSD4YFcOxEPWtsB3t1XRUKHtMW/WlMYaoCpWnUnd3+y3osiwNclGJGW5JkSU/FRpxDYnDhCXk'
        b'IOLM1GKN8tYoSejIVd4BnYc91H0+X2pA4vjlruNrfL6fbcrFZxtY8srX8JVVsrfn7z5nilwtPP+R8fWzPvLlvifDd411nJF6LGV4VmVJ4OyK49HbosxH+hTalW9tysmK'
        b'u9/+7cNHI0K8jK7ZXa7InH9/0Yef2Oz12Jq2T1RU8abJnfaguYWf2Lsavdrvw7mfcKrTG+FZj1kvfTFT/NrA34qv+1nc/NVi1JqTNxsm/9Q3Jmz84vtXfny/cdjZiABr'
        b'af2//EL/vNZqpbw59d2Ff2z8fPmndxrTvuhz97Owf1yfnqpc93FG0QmX5LqkSx8WH9lYEuKZ92jVi2/2mevr/sKkqZlTN3HbGnyTXw5QWFC/g0G4ZWqGBetGdVLXnrMB'
        b'7KD4NDTgZu8U1UkigQmIGKqYSJ0gXcJgF4nrRPkplJDClcUvYl2lbrNuyGVoAqWnhjzIY2fEu6Qb1GRtS1x0tZJpM5h32BUFKtEOGANOBtmjCBdwioye6C9NQNn0oHjO'
        b'OqrsoNPr2WPnxy7XdUmLM6Cc2ntQHTuY3wlb1zK/2QZf6g7X2W3WFA4xn41qrItVwsHhrApkzuZitcoMLov811tSjavf0NWQ76TyoP4vhIYYK19ZDFetbRAc8xvtK0zz'
        b'xAvAWQ5aBqDjzANrO9ZKCxxQrVKqYzyuVbEmuwzV/g6+AaQzpsygxe81SgQH8Pg8R9PtDa0oVyfUkp/i6uBLq8V7TNZEWg6K6hxrSeMsl6Lq7qxwsv9gnOPcJ6l+KTTa'
        b'USSlPLlSiYQcBvPWap5dcuxMXmaCmSDVRi6uH9xVeeo5PNHoacITOyITDfQf6hvqJ6jtIQrR86k0zytyXc3zSVX6LwUiYh3uwfInBiL2pLL9rShEckDRPQpxGItChAN8'
        b'aJcoRD0xiNAW0zUMEaqG0o14rf8Ih02pFGeAhAiiBi5y9lSRjBsKdSLIgu29qCzg0duGhiCOhAJOHYNYE8vi486a2tHYQnSW0EyR4EIsGBTTbcDQQEQpt7jkLf77+1uy'
        b'SCPYi3Y7j4E9G3RCCK9OG00D9JaOCsWXT7oy4im8DLRTMcBWjBqVKBsdSuXJcsehXFt7Wiy8Nzk49IJGTQAhbPWGJrp1OSyw7QgeFLDgUGmiQEX0IWsVqg5B9W5QKFZH'
        b'D46G86wuF1HBlhDYY9wRPwh1MyPoduwUiI7IpAmaaD971OSjoj6dl1K9Q+TmujF9LJ7PI4G2gVhB4/lsuQXrzcYsTWChbKfm0Hg+LnzW6lnZy9K4RDI4l6+k8XyuH/lG'
        b'Jvyx5P8iDOySoW4Y2Bz8wQtdGKImE3H0DciAfOdUnwDIc4Q9ap8hKEZNBKmEeO0p0AXRaCy5+GHhokkpw601G3LMQ1H9FFpJs1gTEsRnN0Oa4P99PwdW84CkPiSIz6LI'
        b'ffOA1kmBnIqMbnvYaU5iLGdFdIviQw3LWBTsPqiFY1jI2qoN15vsa8FaOJFhnz4TkWpyykLJKXjazYvhOHHnwzsxXuy3ccQPN27Bv9WqMU/XqiKpbqvSwudCY4wMS0wH'
        b'tAF2EzdOoUPbxwt2yWDXJOIERUPr0GknOhZVUG3IIuvgcganDq3LTqTTpBecQNtkqIp4v8zj5jlAKxu+hSGbZJCZoBNat8QL9tKgu+DeqLEjqg5t51GRQNv0Sjx/+wCn'
        b'LMX5V+67oAr1U/b2tL5//4vy3yuyvvN+wdRi7grhmOWeX73Gyo9I1im8P2l6buK1yftzPzsV+0/PgbWNCfsc7RLu7l50xnG/o12fukVNHxku2vfZmsBfmq2c+nx+87eb'
        b'a25+M21T+/1ZfV6bcaZgk1PBgBeSoy1HNAZ7vTW6zwfmH/k5vDGsQHR8a6nRj0eKJM2tzta2U4umGzs0rdpxWhZwfN/Ir42jssbfOP6Bx5BT0rdrPF9xi/yxJueuR22f'
        b'Ry/0vzBv3Ko9E1aHH2gaap659Bmn06tli96vSTjeLspfPaxv7Yi2eW98+q17nfu+O2Pq//z25PKVV895Dx7a/kF6onLWry8czkl0Pbd6nvhPr3dHvnvx2tXUrIxJux7d'
        b'+vr74Qu+vPRl8MlR1/y/Xxi6dONd6+i3+8U5pLXMfyPmzXeSdn4z4/rKF//Z/Om3N4OrSlpffv3qnbvvJv3s0fz8kGE3Ln0buj/Df9LVlHSXDcfWoyGfFtS/1GoeM3jM'
        b'79fq1phEGt6uKNlx53ToQ/kZ36ZriW2vRd19cZJ/tdmqHbe3N1SHB40ZM3tgyj/sq+6NyRk0q2D04R0DLzSGvie0fR4+Z1nhe1HX79wa9+6fTrtuDv12ZEbt6Pwbny+/'
        b'8eOx9RE5/x9x7wEX5bH9Dz/Ps4WyNGkqNiwoy9IEUYoFLEhHRLChFCkinQXELlJEigiCAoIoiIIg0hTBQnLGNGNMu2mkx/SYbm5yTWLeKUuz5Cb33v/vlY+7O0+Zembm'
        b'nDnne86OBlebVybfFNedcXny6M3o+9fubP35hm3hVxujvjG/4zCvf92/BsZpxr0tLW80/vbj2sVv+6XGm77wcadFts+YdSu21ZTcdS9+dhO0Pj3m7ejiqzo7RHPVPnU8'
        b'nyq8dyzqpUU3fw38fJHH2DXad9O91rWorzKbFZBu4fRC/36fn2c5z3+uvycsCb3nlrbQ6fCV5//Y83qDsuWu8nh5yO37WZf3pu92vzMttsDWP39L9PNhn1i/6HXm1bD3'
        b'b//L0T1m9q2Fa7ZFNn/bv1k4+KQ4bU/BTNvrf9hn/fz79h9Phd//5rpz/zbtr+5uOvj1zJI5d14ywb+ly38uW26Ssbk4L337/jk3b/bPufP6XZPXvzjf+qH8FVv7Foed'
        b'sU3h0dEhundC3c3S/3hy0bsh/3ynws7ni1uvaj2j8eu1sQkheWt139vfXhL2j/dn/RYc/+HAuKTbwTWbKm9Nv9f81qffPhMzNzq3aO9aYe6R7uYb7X9ov/TZ6/ILgd4a'
        b'6Rv3JP++40rcal/1b2Rv6t/90exbU/m+LBfRdiT8EfHyV41X+3+r+zlKGjPPM0YtLcHJouFut4sBxNn3gc/tuUvXvh1v07A7PkPrM92E5W9Z37qvefP+hxsaMp3nFaGG'
        b'NtGXCSd++SZcc6Vh5ltqn7+QF3Te+LNlcV8kTYz74qbIRZ5EkVYEYITOqXBqw8w27IMTKoY7EfUzkEHrUjijgJrA0a6MURNqpPct06YrxqKeh5wAJ8IZyjwnoyI9byWq'
        b'HgFTYxi1VnSFcvSpSjgFhVCHrjIj5xHAslWojtn6n0CnUO4wsgwOCtBvYRWnTYUhdJz41FLiHBpHgMsYsiwGXUojVoSoxMRSBSyTe1mvCEjxJCCUQWyZC+RIoWvSFBWA'
        b'RR42jCwLFdAZicU2dICKCZqr4dQwfgxKBJS70Ay1b6Y3eTiLTnonwMmRELJteyKZVHXGBapksxJHg8j8USd0sUZc1UO5MnU4MBJFpoKQLUJZzNr6QLw7FsYrlw2CyKCZ'
        b'IGloF03HgtFhGeRpjoSRrfZVAR6ga+VKpRVqeRhEljbVWWUAvnTsEIIMXRVQ/VrRSiwckcXeXQy9qMt7vNlIEJkAjZt96Ajbh81QWkMBnBqJISMIslzIZ9JqJVxDe2VY'
        b'pD0zAkamgpB1WDFIUvM4qJGlo6yRILD1mAm8wmIaHkE1IiXai/KILRPFgAWjWiYR9mCpt8tj0sMosKpNKJd2jhe6ADkKdEwYZRrUgy7Spke4Q7HMz0pLjlsODTzsRxdQ'
        b'2+4JDHt3AfqCiFXz5ZFgEQoV2Y0qaPM3Gsu8/dTtHoEuS/Zi6IVzqMwN1x2ODuHLKLYMS+JltBDHxdtkBFpG+G10QE7RZQbjuMliMSbrnSyPyigszUMnlAyhyVRYshOh'
        b'9AG8AWMRNBwdHYaTMSxZJupksm+35hjlFNQ+BEiAg1MXMbSIMgZ1uesT9BQFkUE/lFKanYMZ2P3ePjpwdWTITNSGLimYCX6uwUo8zHnQNgQkg3po3k77fBbKD8HTCM5t'
        b'HQEjExmFTaN3zRRQIjOPmDYCRUb7WJ+OSJQb6lKga0uHYWSYhPKXM0q4YinIIoNGoshiJzEYYYbmcoUFXB0GkTEI2WYoornORLUoaxBDBmf4qOWozh562ATJgQ7xCBQZ'
        b'gZAdxmvcBeiBZtbYS2t0vCfAmZG+mFC9Cm5EnBQsUkIjOjsMJoMGVLCKvmqLOsZ5+0A9yhrCk+FVJYxVeg6qmaaEctQ2iAahUBAog5Osufmoaj3qWq/hw6vwZOgI9NP2'
        b'7ETEx2AXZzcMKpswHxXQCsWhKujGY3MImkf655oXwJa4fKgDxsyORxWUl0VVqJkO+g44ggcdT49LD5w9LZTSnOehq5pKPyIODsFeBDgbjxjog9+jrkRZqQQd8QhM2fLN'
        b'lN7tXfyUmDLOJDwCUOaaQbtsvMnCEWCyYB7LgAdwdyYzUr4K1aYUTCaHPuKgywaaotg45KL28cNosjE8nByzEVXirYoe8rRaQSOFk0ngKKeCk52DRgaWk+BB6IIKtWFE'
        b'GRyHUjwVyKsa6+AoGd/8kZAyJ6k9hZiiVuspuDMboFku18RThZx/XsD1HofaxQRRwYZkI+7YbBmmqNyRDHU0FLJxbiQ4aXpwthaV05Mz1LaKLXDVLqhR5meDG8eyJhSq'
        b'CWUCtELLCrZ69uKp2ilTQWWwhApZ6MQ0OA0n2P6ZB0e0FOaYJs4PQ9pEupN30DGzTUe1Srwr4j1RYxDNFosKuEkuYihNQYzYpi1MGQa0wTFM/ONQ3RIRq+BJyAYSPbnI'
        b'Cq6MALVhiozDGyejuPmogSHaoBo1cgTTBjnBrPsOoatOSqiWYWJ7GNIWBocZJu6kFOq8UenMQVwbNHDoNCXZ+QiX06UUD2PRGBJNDm20d8LdF2OZcs0DaLQKK9RLeQMl'
        b'KkN9j0OizZdOR7VQP85V5a8O7dujDNMa6i0sJ6J9ojREoLOkLzeuTyV0iw5N9ZZroAK5p2qzHw9Z4uVGcE2FCtbG9dXEKxXmiWhT1VCN4KahAsIuiXGGwllrh0FnFHI2'
        b'Vk7bOnkXlKBCXyjBC8PgASw5fbVFV9k+vg+ysZydiSqths8/G6zpu7qoQ00pRw24TH+ZHypR4IVXb5topy7U03czYK+7Yo42pkHMiZFzB1Ql7FhhyMJe7Id+HaUD5uOK'
        b'fPGcxmwjaRjPjTES7cI0fSSN6hK60X69h2F4FIMXhvIegOHtYVvbVDzJ+mW7oh4Csp0yNGLTtnkhKld6ouKAISgr3shj7GmdDbeieuVUaB8CSQNRmxxj/ZwFJycroRvO'
        b'DKJ1KVRXjJtLsXF1qNhesWXNcB0fwNkFSWgFF843kInh4oM4QWhIgBbK3+xxh/2DYNFBfF0GamMQuwQf1oh9cA0uysLQhWGMXVMAOsyWrUKxp2wF9IxC2QWgTiml/I2R'
        b'mFNHTSbDMLvjtnhaUc7qJDoKZ5XbUCfutgcxdoa2dHuHfjtDGcpDZZi/oRg7dHU6420Ko6BBiXnrkw/g7KDAGg6xTa/WYgHO8xKcHcbZ1Usx40VBduc84TDB2C2DcxwB'
        b'2VnDRTqh4YQvXlF8XFHjozB2cDKFreJHJtgNQuwmC5YJBqgVWJATa8Ebb13nyUo0DLGDI5MQO6tHrajJUam2aSTCzsMFmui7q/FS1DgMr9vF43xOowoPzOuRfX7Zbjw5'
        b'UO58LGU8ALDzwqsBGYst0AVdSmsX52GInQDlcIzRggfmDptQ14yUESA7BrHTNVVhrnuJOOMINSNAdu7+cIC1OQcK/Ai+bho6yxGAHd7V2tkKfghdtlRAj/MoLF0W5CfK'
        b'df7vkXMU4MT0B38Gm2N/4wfBc3qix8Pm1Idgc/r0T8zr8Ho4bfqbINXj/yZMTk1dBVsTU2ia+h/4+T/o35vSuQ8B5+4LYgaSM6Rv6BDtBgXbjeONeTHO1ZrXIe9L/0vA'
        b'3D+05o8GzI17HGDO+EFlw3+LlstXG7Ty+zONx17u3ijM3GOqgcsmEIPUtwcBcyICmHuWV51Myg3+74BuN3ChHxIk4E7ufwR0e1OqEHgdySNBbbMeALUN3vtjnFs6PTTp'
        b'hHNwdPg8G7VDu+pAm+fMoV+SAEdDHjKF1VF9K/c9hGdbJy5XK9coN4gWyGe5juq3oepbk33HiqJFkaJiIdJiSM1EItto7dfer7Nfjwae1iK4OIojk0RJI6WRajkcCbhd'
        b'LKxTw2lNmpbRtDpOa9G0Nk1r4LQOTevStCZO69H0GJqW4bQ+TRvQtBZOG9K0EU1r47QxTY+laR2cHkfT42laF6dNaHoCTevh9ESankTTY3B6Mk1PoWl9nDal6ak0bYDT'
        b'02h6Ok0b7pdE8yp0nBH9TQJ4q68zpqaUIqqCU98vw32ji/tmDO0b80g5fmJspEBVGYoBrSVuvqsGo9V/eFF4wISS2DCNfIIB6YYscNKSSGgHJXvGwc6SfdvTQAjk15xR'
        b'mQ2q65TWpm4jjANVtm4UHqCyqMN306JSaZyGpAwSZTZttHHfyJgNlqZR4Zs2m6ZGJadGKaMSR2QxwvqQmK2OyuFx5j2jlYajEn5JxKrLM9qUhldVmm6NSo0yVaZHJMRS'
        b'O6XYxBGoC2o4hW+H4/9pm1OjRheeEJW2OSmSGqLjOifFZ0RR9WY6WXHitxEDrFFBKUyXxVJbJnM3ucoYN360hRcxhFLZCLKBsFGNw2CPW5qaL5YPPhZuqowitmppUX82'
        b'SGQMzZfICVQjfIQ9oMoSLyk1NiY2MTyeYAZUEGPcBQQP8UBDlcrwGIoWiWLBN/BTrPWmkVHJeIlVmiaxilOjPnPVvcWEwhKSlKNtuzYlJSQQo2NKew8YEPrJhQFRZkL8'
        b'gHRTeEKaw5xNohHLjkS19FBtFAkgocKAqe0fDI0lo0sIjxcRIVpHpbMW5UuzuV3i7Zo7RUM6azHVWYt2i0eEw7rH/wVU2KhJ9HgTssdZFeKWMYPCNb4+Kos4GgWF5js8'
        b'Znh0qNUonpKPNjU1j2Kk9Lj5+idoJdqtzgR0sikcz/gwXKUwZtnHMhvKZCTZPSY2TXhkZCyzA1WVO4rsCIGmpEeppq4yHc+poaXj0SiNUdayLOQMmXnh6WlJCeFpsZso'
        b'oSZEpcaMCCjzGLxHKp6RyUmJkaSH2Xz+8wAxo/Y4bRWxjbYpmOSnpPz2vVldL/+skJ9Nkz8nv1gof70zS8nFLv14l3rjOw3UEj+dsC3uWg7QhUpRDzkoTMNCgxwuQqEc'
        b'HYFOIC+gCnRylzpm7CvQMcqlrmJOUpvwpYvQIuFQlyO3m9sNLXOpDneLGXE0/J2xDhfmUz9vA0fVnErYnwldApYn3TkXzgUdUY//5Y8//nhOlxiXjZsucw3TmmG4h6P6'
        b'TbgyzZi6UEbl9rYCJ8E1uebEr4CW8XKBQtt1QuGkEhXooANbmVoBi5caFuY8Zwf7UCMqlyrUoqmi3z3WVWZhjvpQFs8Jvvw86JHhLKgb9lJoRudGZqJJPrDUcInnpjlL'
        b'puFfndQvatQStE8GLaiW3CcyYB85+i8xxBlhoY5zS7AZVRVPC5QTgQVp1KHw9LYmCo5gVKk+0XQz82ncZu2OugbvqG9DeQ5CImShi3IRve+IunaTQBwa0GyFSu1tHQRO'
        b'a5cQtymWdgyW4s9CA7k/3ZDdlnJau4V4sVY6PSBpc0a55C6chD52n+e09ggJy1BVuoKjcnDpBhbjw2OVB37QKsAcHfMYqbhZqqs2FstFZcyws2URylZSZy0BVugiFSMN'
        b'/NFxOCgijvxhXzrBYtihgqkjTVfMUQkqD6AhUtABH29vKyFlAdRORFehwIi4c/E2hAJvmSZm6Aq9VgZyUdF688ajs8zW0IyQQ6W2FiYHF7f1XPp6UuvmOdpQyj9QhCrw'
        b'TbGNV5A5OuCBigKJwaR3EGofImNqN+PvKdE300S50CiRoN5lZtAs55ZtNUS1qA+u4V4nkuGUWXHURWC7bnIqJhRMAjNTdbaPmT81WWburZ6agUddzFtMUqcGADtRtTHq'
        b'mgZntVLow638jLmQw1wK15sTx1dVqD6ZugwTafFh40OoPt8Z7VMoiaupFNSpRV7by8+AfGNVWFrct1fggtIRVaKLNFe4whvbGrF5Vjt3LeqyThguzmY2He4odBZVkOHe'
        b'iqpGjjaemFXpRI6xSIPmkVFdfK28/IPosNOnVb0Ie1EXh+rGzImXQZOGLJ1AdUzgMFx78NX1qDZohVUwe4tDZVwkuqTOwSmUFbvA8bKg3Id5ufefmZ5w2CXJwE3vma0/'
        b'v/6Zy/v/KnM8YHBM772cGI9MR425Osuu8QkrqkvHxBk+pRtw4t28hjc9zPsKCuCN6Qu5+voT9acWl5evGuP1wp17H1Uu//Cnm3vud/349k/rLvc11Vamt/TZmrpmfRHx'
        b'5Z2xW6cfc3lif6/7pNTZgUv1J91Z4Sme4PjBacMfjPaV7i8Nne3QJnpSrfeuY0ZW99VvZC2fnjz0ykurQtRNc6YtTZq0zGxSpvytaSU9F6sibpTq7FZWfPVrmcfBNLWL'
        b'l03Xeu2YMsPeZcobhh2l4Ur5Fzu/nXhXVJn/hTcad/bKzcL6/PZNi/vygnwG4i2e95rm9flG+fOnExLcf33TQVFfGRH8dOatvuolY31uhFSdeDvzs65bmt+sv2A9LtAv'
        b'6lVj94HYDvNba97/alF31+tbE0/Vjh3bmppyKqTzX1HP3u6bseHKuZgbh49XNez8IubV/vByXyNZwqyT79b9rrCN+hYZrO6ICzBK22h8/ULl4uYXXk7JPxh722PzZyvU'
        b'avLN0k64nI7LKa01+8cir7GfbXzm2Pgf3tGbtyxyo/js88E/ndsed6ot8lZQzb9CJHZ6PU9NShn7lX3CvPB3j8xsetegdG34xcXxq7W7HO6Wv6214FsrX+3ftFEAsrea'
        b'1fqz0WeSiA3xHxx4672xE87XvbSirP2W7m/dT1zpXvfHtX/aXXut8um7U447Pa+8G3r83riSVxPWHd/+dODy4xXXv3hyXElXz+9jX9T8wbF24Q8T1x6/F9g1d45/5hu/'
        b'LZqspWlbt/Kd3337E5CG0Y8um1cri99tuvrqzvaqsl3X1l88ewYZ21e8N+uFupd2tTkdP3NysW/UuECjG99FPvOezTsdW6LHXXjqxvVr2XoVUgvdCXl37A8tv77npwkO'
        b'VWM2ruyQu7Ez77zd0KSw9kWXUSWWJ6GJ94ZzqI4d3LXu8ARyxpVPLNv9UYHAyVA3qoMreHpxmsyp5Dn5LIWnTyzap4bfzucXLHVnR0XX4PL6YWV4AGqgblYrQaUlPj5B'
        b'FwptmKpTag/XwoRpUOfODtGzPJaQ2EM2/sRS1WHhbsECzgtp5DBBcxYWbgttiPbUxxoO+BNdcMVsvMLm23hYWlCkphoXijfhc6jfgekky9MCifdZ1ICOj1LtO6NCWhNf'
        b'yS5ySIaKraScFJ2FIxuF6ehyMDvEO2ga6+1v5WlJjntlcHoxdAvoivtipo27EpmpGG1RAA2ozVS8cQbKo0+k4k64IBsd59gXlRIzZbkZPYhzQvvg0LAXrrkG5JQQVass'
        b'CrZCruvwKSHKhk7ihguaPVkXnoKDkKPYEegJ5/CWLo7hUZ4mqqcH4RL/yStJZBvqJnf4DNEE1YhToBcV06PRVKjkqN6Li1SjSjuoCaBHozLznbiTvXy9rcg5nx992Rbq'
        b'eG4GqpC4oBwjphEpCEGNSlTsuSWKjIe3jp8V6vYWuMnuYmiEk+gwU7u0Z0It8X5agvahDg3VM9rLBNSLekXMqrp+F95VCm38xFBmZek7VCTPmc4WYzblDGIa/mhUjjpG'
        b'eBVDNZvJqWcAMPe2eDPPRrVQiDe/XCjy8rX09OU5nc0iRziMLqviSpMIcHifjoMScprOznu1HURqi1ZS3cN4VM9cGtJoe2qcFO/w2RqCFjoRyhyMnZuHWpVQYkyP6UVx'
        b'/E5U4UBpdiq0zyc6lYkj1JyKhUylhqqAxMor1R6ptLPCE4HW6QR0uFCdE9WASgzxdKvm8Z5bjUrYyXiWRppMNMnamx5tn+WhbmsSHeMQuOyvfFiHGTqVajHTfWmNo6F+'
        b'MlEmpsAlqUqZaLaFTdAaVG01wqflUagYw2/E0zubWdQUofOoF1esEPL9qUtMETrGw8EwxDy88XOAqKG7oNcGlShI1bp4ODN2AavzeXRiE1NS89pKoq5ftoJFY1o9nnpn'
        b'puoLSTQe5j6BXzCTriQpzsx0Uc9STJW9mahiUH2Qi2uHx9XKwsvCSaXs1Yc2ESqMgqustn128RRoMKg6q4uBagEOJKMi6h90cQK6TOyIIBcuKh5huB/pRRu1eBpmMbtQ'
        b'bqhCpSC/wENbILQxh5ptAcScEN86AIdUnJOU04kULZsAxWlEQFDfTHi1rRmoWztliAmbEacgiGwbdNDD1wq/ELhMXQdq7NgUzneUKxWamCeW85wa9C3eJcxZCt30nuYc'
        b'X6UilZG6GmaVTkcJdnA0k049V9g/FTfXkyiD/GnoPQlnhI6jU+iseAy6BlfoCKfvhioZyVuVx6GFcFZYgM4D8xCIutxnk0xQNWSRjDB1qnE6fiLXIHSa0s5yqNymJEin'
        b'+kTi8aaH10MNsXSo0LHwCBnR1MRPJ7oaOAbMXTjUanIqf4gTNEdoagxRI6ULRziKSpTEOMY0hJrHzIFcmmEQusoRD55wcBPm3Qz56Ssk1MvkNChahuuIK+GJpyRdFmw8'
        b'8DB2jRVx09FpyTyUu5s1pmk3Oqv0k6d4WkRDjkrtpzdJFAB1vnSCGkTBEeIPGQ8j3iaI92PMSTLftcHz4bgyEopYP4kgl98+PZW+ZDVpp8LLysfN28rCDy8mujGicBM8'
        b'P0jNxGjvXCjc6TuibgTncoCoreUbJXAMTzBKFC5YAjjyEFVQmvCfizlRl/XoDLRJ/aADahlRdMbDOcX2UWZA0JBJV9M0WzghIzfSrSBPk1HwGNQnwrtiOV7kCA0HQ7O+'
        b'gu45eENTN0M56LIApTJ9Npd6bNBp4rxxlGKpFLPVeWJ9YaFc+79X4PyPFEGP8hBwEX/8GzXPHi5Kk9cTCChEyk/ktYhqRaBn6r9LJXpUuUNCWBEFiFRQp7908HM6/GR+'
        b'Jm/O6wt6JEQW/ptIn9WjChIpb8wb4zz18bcO/lPHT2sKUsH4wSs8+dOhiibyrlQFUDHktxuNPGZ6wFGBXMKgIR8R5cXt0XATrf9qLEQsu+Hch/rTk9hrk+v/Rhezl+ud'
        b'OVIb8+h2/CXHBzH/1vHBOXVO5fhgdDFDXg9mD55602NjS9OoGGtTC3L+ZW3rYD/okuVhJwh/vXopf1a99sHq3ZtA6qE6QjWNjRxV4l8qbDMurJkfUA/dxM7WH1tm11CZ'
        b'UylqmUJ1o03pawR7/7dLJs2U8wPaoUMnx6Gxjy/+4lDxM91M0xNjU9KjHgHR/7t1iGZ10AodPE38syr0DlXBgvSAMg13AT2PHDqK/E+rQQYh1eTPRvzKUNnWgUnEEVBi'
        b'dBJ1c2AaHpGUnjbKr9DfL596AiE+Yh5bfv9oihvh5+Y/6vNUjz8rDIYKMxkubLHnkv+wYd5/VtZTg2WlkrC6f31+Fv1Zps8ONcB81SO8Ew263vhPyVWTeg8IJVj+x1bh'
        b'+dEDRh0AsEn7n05UdVZqWtJjy7w1VOZ4lbOI/7DEnMGlISI8nihBQpOSoxIfW+zLQ8U6kmLJs+xkPn6kau9B7yL/2SzFtdIZqtWm+CRl1GOr9Y/R1SIP/1fV+n/if5Ln'
        b'HtREiPxiF7waLlYSftTnZZuvwp6NUI/+wEfEqYfZ5fMXPCLlPLMWa4PmDVDoKhuWdaigs8vtMR4kzQdtZAjT+m+Zpz1czHbDB7b4+KjE0NDH+48kBbyhruqcf8tN7OVa'
        b'RnmRfGRh/38MgNhvVWzPzCUiJbn8o84r3uFaE7/FI6DGic15+ZhDw7T2cB93cKyPU3P5h3iX0NCIpKT4P+tA8vbA3+jAJq0/Y8hYaaN6kNSWlEkkNKZkHXa1OejiiSla'
        b'+f3aQ0pWIV+C+1aE+1YY6lsR7Vtht0jVtzEP9i3RYJEQgvaj+nYKc65qDFlQpGTn+qh1ET3aR6fmU/0WHgDqPGFvcrRP92IHToXtg27Up9RJ1eC5WVAhoHreWoHOUw3I'
        b'2DnsBT3HaEt/x6Uc81uRg0oU9DiEQe6Jv4oib/zDj7ixWLlipVUwqvQXuI2uanASlYyjAUUlqAoOeBM5txAO2ixNGzr3knAWmyTQogd1DNB4GC6jfCXTWMCZIKK0cJPR'
        b'gIywD11C/aMjSWA5s0yACpNYps/KgiNE8lIdLFnJxVY8nEMNLI5iICpD+1lE0DWGFNIbFM80VXlqqBCLoEQARUXE/I5KoVGkZ1ZRrduybdBGxT0rTzGnoSZCJwQ4uEoF'
        b'CB6HGiGL2d+OQ1ViMY9l0b2ydOahP28+Ob2UYylRw8kONQvQCPtRPfOC0jZ7nCoKlGIGhfBADc/Chu4LJX7vrPyo6Ij6JNINghEU7EonNsqLF+t4o4OexGUeli3P+qBC'
        b'2vHMk4BigQQL7geh4CHalA3S5tJh2hxNmfyQy7G/QpXRD1Il6QqNh6jS2o9S3ikT5rbj0JbtPnsstjPwKu+/nASFOLZmCIYCR+AC011lR2xXelpooOYhW97lKJt2jt1O'
        b'dEaxwn9wuNhQKaCdqa7ysSjervTxg4OmqsNDOAN5VOm7DVXySmI0LKgnzOAnzYMqptE6ZuQ9GN9bDCW8DZzazEJQNowhEcl9vByI/5VB3ERGOCW1DFSH5XkSNgnlou5B'
        b'xMtUdIGpRg+4KkZFTYJL1noio52ogqqsaXXgGDrmEGgOe/HvqdxUQyiSS+jLM6FCOerlLWb4XdQBrar5akAIwHKn4XAg8Hxoo6/Gy2GvInrOg7AXK8imlYbOBahTgfZC'
        b'/ig4TYULxUrroXNQrsClWuM5sgIdsZZbefny3DTIlTgt92W68LNwas5wLCRoEhP4CpSiItpjNqhlLYlCgmtUS9XTUnVhbCw0sJDC2UE2iscYWE/ANB5tsYEGLw7d6EjN'
        b'733oATFZUqCAzoOZq9e5SuLgUDxdhYxNUTbRXzxoXT4enR2Rtx9kqaFDqFNFHj7oCmTjxQU145dUKlF0laOrAKpHlWLvsZIHsQF40ami+mezgJShBWxw+UJtOwZXMHVn'
        b'itpfgleZq2wJqkctZBlii9BZyKfkpo5qJfjdpbJB6MJ0dI123gboxUtDoZUXZKMzg/b6aniNUdmvX4B8siSMUwUDokvCUTjMSLUdjo8nawmBbw8CAncPrjMHUM9aXKML'
        b'kI3f4x05dHCNNVtsq1LRVYWvVQh042kmDsdLImrVZSN9zcHeGzVALjroYWVJoZ5HhJ24FW2UVuLXThwyc6/iRkeSMVajxDYRk0XHiMBJsC8+RqSrA3vpKBss3j24ig2v'
        b'YNN8h9Ywu/WqwLjG02W4xZ0ZYo5HTfbQyKEzoegAvRUP/VCohGp11CElfp84ODQLytNJfG2/kO3o8I5MfNmSs8R0XUe3s1/2aHJ4DNTbl8VpdWo4Mr8BPyfQSNRcu9WO'
        b'+B+FFeyi4XS2Xj2xLlqr0V/ELj7tw9wOnLBVaoVYBrCL13ZrcHocZ/vdrCRLbmvAw7GSKV9I/pOB2slt0NnF7+STtSK5YLygpgiRQ0IyZXtUgZH5jAfY7gGN+TFRiVGZ'
        b'yakLozRUC6yYeAEIxj+2rnJSPnDyiUqZs1JLTysowD+OjnKugA6LUBcc1veGMnu9iLmoGZrHrt0GzUaSZRkcVAYYoa7ooHQ3umlmo1NE745n42Era3II64mpoNzSK2CF'
        b'VbDHQ0OISqBL0MSbVi06qxWG6uPSTTkCeKpD2QqvMUlWcitUMEL3MzFIDK2ZK2LdnnpNpHwWt7YYgqICexPfdtWr3VBWZv7ltfgbnVZv//B1yK21TR4fTtu117S4NDpc'
        b'pHjiUKzpMtv1TrZrZmQtfELyk4HbtSefVTvlNenULbXIDA9FRkj+zm9fOFb17ngL68lPXF/wW4JphkHlvjEpbgdKi6ReJs0Tb9cYfi4/4KS+btzY3NQljjs8fdynvLSs'
        b'+YqTupvLwGvvrXl3ZerdH4v2b6x541+lP7mYm1V2r8uqccq41+fR+9yedScWfHlkCtRar956+VDXIWdPxRd2vbujWm8G7DE+13WucuKnaRWvfaR38MmPD7yh80FymOaa'
        b'l95bWrTDwuPLwMr8pn3/OhX+WrPedX/F7Dev6Jmf8XRI7WtcEOQ1kONc82uwJOezcQqjic81e8QVT5dUrv7kxYvKp44vDwr4weqX6x97JG7+ojeuS+myfXfGG9uPfP3O'
        b'jfvblnh3TfhYNOnLto0nfpkCsqeX75nWMPle+ZJv16zJubYlL9n69uLn3zv/1LYFgdfrN3Zf+35h89cvPT0wcX3ET0bf67RMWlm4veryrdnf2B+PuQLf/Hx9Scb+1rbO'
        b'ewcyj75m3RJX0/NE5hOXnsms/X7a1vdfOlaz46nMwuneE9+a+2THuQs+li+5bF/97cvz1sAr1w+cem3JiV1H7rjfcX9LWZLxvsMna8ujt06qczyz7Id3YpZHfdr0Tuqd'
        b'p3abOI1dG/OS7t0jzREVL35R9Mypn/918PeppzI/cj9quMcj9MUb5s8U/fRx6bpazcDCBa21sgtz63Ventdqpm0U+bt1x2npx+/UDVhMivjq+uT3I5uX/LBjc91XS561'
        b'SCyK/NL7+EuLrh3/+pUFX4UtePd2a9dPG9ZEx/0e2PlNbH9h66/3ixLyTghfzXfxfCvd8p+vHRm473HG6cSW+Yrqpz1n3TLzf83PuTBNGrj8zfFerz6Rt/tp+7RnQse/'
        b'2uZ7+CXl9p52zw3XNhWe/eOJmRcP3snb+oXULuNg0/2x4QPqb+7+WXg7yfWJ5pYPHH55Zg8/MWnu+iJtuRPVephGkb3aBq5Ow3slXZavpO2kSgZjvBUdlRFcmIY55p0x'
        b'gzgGcyrNu0RQg1pZ6Dh0yCtKhhniDgs56mRYoAlCsBlcYuqhJs4PdWmsHEKD6i6nmo010EXcnKTC+UlDSlJoXc+U/pd1nBSecA5zl3WD2uyYJQwYWGuDjtAgeihr1ZAC'
        b'FRXMpS8mrwshnFCa/TAjpIYqqCrEIThDZgEHSUtSfGzkUk4bPzPTgIXcDMI8XZbS0+0xKNAoXaaMOTITLrLgfqTMYmjlUEkUi8W6FHpk5JYtah1Ecm6EbihjIJqqlIUy'
        b'CrwRVsF5lMcvRLWhDERZqo+34S51v2EscxliGECrjLCRMSt78T5NEMdQHk7fTFuSobSWh2C+aAi9u0EFGbLDvM4JpQ8ZDbzUeRPteH+0lgAn0CEVOBSLUnuBcFBwyRMV'
        b'WBIQUKtgv2ANUwafmwMFZFPNGuUWAGot2W3M5qwnwOPN00dAjy+gBhblEF2GKgNccaiG2kHcMqozhB4GfIQyB9zJOAu4hnsCj5LYicTQPYzO01a5pyyQoY6EUVjpmam0'
        b'3DWYvT2uJAs2KvD0RD3eAqeWIlgshG5WLmYC9GW7Uc1IrCoqRSeYM4OaBRFEp5jCFLWamIOvXC1A3yoooh1ivclIBs3JK7HwRsCYEqjm0XnI28LIsR9zZiUsqKBgiFqs'
        b'+emoOIVZzPRkogsyL19UZaOQYgmgj4dSXeinakjfiPFKH2O46metYe1trUkEqHFwQTwPM0nFVGk/Jww1KVFbMgvsNhSW0RDzwuiwOjBtNZSPQweUeHOreSTYdAq00AaE'
        b'e+igrrXo2GiA5oZ4WsuxBmrEdMQfzxwVxgxVOKBqZrlxADNyFbJgLCY87McB9aFu2n9xqNN6VABIk6UULTsRNawbM2nJDlm6tsFkFo3RLSGRvmIKJdBJAlricTtPDT0k'
        b'y3j8uxhlq0JGOqTIzK0MvYfAhXhJucJMK3I10WElHBQPuU5wQ8dpS6aifh+ZuQVUo+5B4PA0VLlYBUiDJlQt25P8ACgxL51hRbEgIrMmwf1yh1CJcJQF/I1AxVuVWnDi'
        b'EZjE7QlsGavcBJ00PJ8gd9zBT56HSqgSVQEX5EofqF/9KOCguyUjkv5MJ5mVNVTAJRV20ABTa44qHmGKlxJal6MCHUx/uL1q3sJUNxdK0juhEp0kAQOhL3IIy4gngApU'
        b'eHoV2kuMqoxNhnyMYCbKhNJeiiuRCS398JKNmSueky3ETHgLcV94dQUzkGlEvQr6RJEc5ROvitNwd7QJqCEcyukgrEelq0l4W3I8cNLJn1+BqlFumuqE4wocVPhbkhCw'
        b'1MpKtt0XXRNQjwbaR3X7WnixOiKzQAdxd/laWvJz0FldBgaG3IVKuLqOkvwIm5uVqIxS41QsVT5kZdaCVwtiZYaXlHa58f9rLNcDatP/3rXhgCaByYRSM3XKZb9HeO5/'
        b'f/q6hzNkSEQxxSaSTx1+JlVXW/IWRMlMUXuavD6vxws8UzgTFJ/WfS2RIBV+1NQ15415c0Gf1+HHCVRxrQoYyL61BBOilhaIElyfKLcxRzyO1xNIoMBx6joCUWZPFJlQ'
        b'JTauiWDKa/4hJv8Fzfv0v4jkKuWk1Am/McNUCuREcrv8QdUw6YFQ6/lUkaRcaD3cI0yeEA9opGVGRqWFx8YrB9RC0zIjwpVRI1Tf/0FYASyj3Cf6vN+HdN2/4V8iIpXY'
        b'kQH494ere7k/RnpcTCcasz2oUNNu1n8uxnBzUZWuZdwYlek66lRsHHRig1moZuLIRoTqoYBFozsCpxfg23ARcjyJYePQQb8JNIhxkdmohYqpkegSsfAbqoK/l+UuXZrp'
        b'FBcxKp8EpVhMJYuGOhb7a4cKrFen5QVDA81lCRyG0/hmWswjCzsLRyn0YRFuYpuCmF6dM/fwtfb0DUgm3RHgoXJHgDeNXJ4LM1KfIUmkjbSHNifvIQtqRytmcY36Qymo'
        b'YAo6Nc0bFVth/mgVzWi2Q4CHqobOMzbCWSk3bzctWB0VbRgZhoMVaz50Rqu1WsKFYDlb1wOK6VFIBFzwH90rwdLhXhEgi7oGxpxIe6bygbyC8ArUPJ0a/ZNmES4oeo86'
        b'1MMx1B2b8XWBSFmHCbfp03VRgZcTDdwMa6smnd/69U8K3Vl+oHDNVFtaq7nsHx4ehvlhGsUhRWa3l2sWVEmXDzQeuLjPUH4nTz/gU9kvgtdCftk/2hx/bpPNqP7pe6ef'
        b'j+/45mZicNdHKz5+8mWQzWqN/O3t5y1rmnu/u+E5YU1CZGhxnclPnloZR324T1/abPvC7TK5Ufx6n0+Wa0xct2CO3ws3ZtZ4n/HJNLX7oaD19Bn51uuroiJ8XQt1xJfG'
        b'Tarrnf7pwcq3bnzcMubbfgO46RXq1gwtmqe3GCQ/V37JZPUb+ePvR6zqGVBrkjVFZHo6TKoO/uxGXsK62ufDn12TnWT7PiZUl4TVa9+9Pd/31qs5bV+bhHi3lT//vXL1'
        b'jS0ZV8/vDU3eEGftuSQh7ovXLk6Yo3ZT0z5hiv43+SF+1iH5fvO/nvnGS0mfTel+avOmqsN+e1OSvjhyY1Wj29lXV5qcqeg+UtD9XktlUFeG/r/s/N//Z4Dx1B91XH57'
        b'LmKs7yer7o3rPf/xlndu3vDzj2rLO1BY/E1c6Pj4rMI7QTuKEzVvTL7Pn2z5yOJzp4avD4Vq17n1+n3W8c7YWdd/i/t0ddUzVVEHsjfpbk2z2HXh2Q/Ovjth7aGK7a+E'
        b'dbZU/zThix+faLZZVXrpWbN3333y7Xr9ZsPT9x2vPWfd6VHU/bUyKM10rV3mR/UhvtayF/+I+8DiLQc41ueWZO73wet3Lr5V8/z8SsvkdTu22ba6fB3X5u7yyZOZWfGe'
        b'P+v8YPbu5bBvw6e/3u79ytXQsF/mf75/lW/TB87wxoZ3F97RGPjXiom196QXY31iX1eb8fl3815pL/nuDy2v2p9PVb1/IrHUefPhxA+e+naN67rJRe/1Xv/mxckvfv/U'
        b'5K/7A659sb4taumifa/6d31dXfOJcPVXnR6313S27r0l83xRsi3saZ1ZHhs15O6Khpfyj05b+C9ZeoneEatiuS01lHaAVv3RRmfO6OKg3dkoW0R0MpVxJSekSmrdiFms'
        b'OFTNbB9tmV1kMDqBuqi0iEVFTThFpcWVKJ/yHbN2ByuhDR2lxncjLO9QD+SqAqQvQ4cVzEoZNRlT0Q6d12C2v62obcIoD29weMoIw8wNsJcW4ofqVyt9/NbMeICxxivt'
        b'Xlb9DpQDNd6Yg8/yJzx7Bu8GnVBIWZOlqNdcqY72qrh5fvo02EdLd4F9C5UqvoS0HHXD8YmUQZmEKsREYtpMWZjFKGuXzEJhgsWpg6oWygwElI1qoinfJItGNEhOihwv'
        b'GcskW3lUYzqZsbXVYzOY2eE11AtXiA+c/PHMVvIy9DooqZuzvoWoxI+YgGpuFaAlQ4sJN02Y/c9RMqNEzDuepIaJsaiY+s3WCETlskmowRqPorCad/FWY9b4x7ahUiVj'
        b'oRemYibahRUmVcON6xoC/CxEvcxydR26wAq7smuW0oKuk5jPbqYqj32oAMsjhPmbiXp3y0aICujA5kFpwWg8E9E70dXUIVP18aiDyhs20EsZ5gnWkKMyOkxE10Y5tIDT'
        b'qJeOnxZq2KwcwRFL0XFhavIWFp3Izn3QaxD0Tib8fzw6y+p9zAr2KonXfVSM5UpfETTzWAYpYqcUa02gjFhIFxMxPBJKRIAFgKpdKut8ewN0QjYV7bX2TWXPpOGCxxiK'
        b'tmB2tJjWaTeu9nkiIzIJUl07UCxE+gj07XAoNSFzonMzXBzlbw5L2ZfoFJw4xXUUVAH60EVLz0diFfavZMr9dsz99xOh02nSoNRKJFZNS2aA3IAf6CD1oYSMyfskE1oR'
        b'cR1O5ulcW2jAAgvxd3yWWIUS0RTz0MxjD9S7Ud9NbINH/bHSUMHCDeooEz4LU1i/igtvwTLVECdOuXDUsop190lLwPy/N5vKNXBG7M/j9nalM+nuUtg6BbNaXYf6mOGq'
        b'81qGAuheAscYWEITToz0wIhn7Unmj6UtaiyeiwaQPygmUJmM58ZFiaehCuhghHY1cjExCGa8grrjAqgWIvBuns9WkzzII45N2H3GzjgItL1TxonRWXtUyPwYlo3HvU7I'
        b'9TCegD1EA0EEXB8BS1D7UT8VwifbuOD+OLWCMHRWcMBmhFrYdp3UAC6mpxH7SVzJOtwTf2LfC21wFB2R+kELFr9JZyzHi0D3KObReYcap7NONBtaoZNaFxujSyHeqoKh'
        b'bMtIlTTKl+CFqQnLooQmEmagayQrfyz1WZMycQeU48xEoqlxkxlR9WAK6B+CuKBu1C/dKExfjZrl+v8PZaj/lT+Ykf5eZg7asrz+16SpBC0aCJ3IOvi/oCcY8xOxzGJC'
        b'QqITeQdLPeOorxci6ehjhp/IQUTWMvxNXW1yKpaJcNpQZIIFKxa0XJMYEv8hEMcbJJa0QNxwqPM6WFIjV6Wqa5oiKZavhD/IValIXVAX6Yi0qEGyVCByG/Mpoy5hvuv1'
        b'eTG+SmqkiZ992MCWSlEqiYlZ8t7/X5oIqyQm61Gd/O7fMEdp/HP7YFp9YsI17pFhzI1CCWZ+UxoTDEMJQJ6EkKWRzGlgcxrOvBR/DKipbGUHtEaarg7IRhqR2pOnSTCS'
        b'1Djy4Uo+dpFyNIZs9wbUVAZ1A1oj7dwGtEfblxGzJmqaQzuE9b/R/905xLBx0Qe4+HlkPHZz1LuMjliw5GdGqLzAiP6PvsVaIi0RFbAM4aznSFk4EWUzRPR41CSOQhed'
        b'H2+9NZ/jmP8TbijQr9qQJZfwby25HrLrIJyNFfegJddyv3QSTwKdGwNX7G3n2M2dDVegxMEeeqA9LS01IyVdidfEdrwQdqKLeKO5gLp01bU0dTS0ZcRhHRRhebkicAUq'
        b'RUeDJQQu0iuTeUArVd5mYDbqIjEjmc3xKbMToYzaS8TDNVd7XL4dBz2o1C4NaujDHkFq9gKxOoEuOG8PHWZUy443/kNQay/luDmYXYNTc7zgGLO6KEPVBoSAHfD+FOVg'
        b'irIoNB9yPaHcHpPCXHLamTtXCu3MOKQeb9R19riD53EpqGUeqocK+gLq3w6N9rjTHTFDgTod/VAle2FfIjoMXfiXEyeCOifMj7TTF9SgHTe8CzfAmdOF484C3tv0SEbH'
        b'XH1Jty7m1qQvlqOTLPfqLVCsxM1awqEKdHaJN6pltT+OO/OoEjdrKYd6haXqvlTDj/emBrimJPEuOHQZHV+G+YcLNPcpqBGdUuJ2uXPWIe5zguhFG+dZStyi5Rw6MmX5'
        b'ZFRDs5aNgw4lbo8H8TPajz87aE0WbcWMCWmOJwdH4bznPFB12BVDuET0MZwXB3njvaDSjlWlGLowy4ar7k1G9ZA3Oo1O0AJQ1fxk1IWr7sMthnM+Aqqjl5cRnQrqwnX3'
        b'5ZwifVFFDMvnAtqHzqAuXHU/DtNPCf6sYPk0w1nCZ+MW+HN+jv6blazLWjFZ5KMu3IQV3A7MUixYwLqsWjqH2D4FYLJZGIBq4Vw6caW/21xPhiu/ElOBzcoQJe0X3dXp'
        b'MoHYxkIddAbGT6f0BbULVstwrVdxeqhw1Xh0mj6aNG6iDFc5CFOddVA4nKAXDd3nyXB9gzlzaTA5DVcRBOqEXBmu7WrMVylWY+azhNZgArdGhiu7hgvxXxOJLtPK2qM+'
        b'2AeF+Ndabo3v2qXQwqi5Dx0DzP7gCq/jYG/cOnR1FX1+DlzVgkJc5/VcDKpdvwj20r6YjqddHzqM62KNefmZ1qjCmfVFh28wOkxDYKz2Iuq+U7TeysQgYg88lcP8efbU'
        b'5Rk0D33cx4fRYZy3goOsnQrU606rDcfs/QJx0824FdZm69Npvt7QrY0O48bY4vG3s92CDrORarcnCFVqhLEbaiydjOllJ9Q+KRDXbSYmHN2ZmLM9Irekx2QTFqtMDQoV'
        b'BO6IxY1CEWeAatGFBBFxy4kJiUip0+dm0nv4QwT7UvET50XQtRm3OC+YGQpWoQtmg9moHqkVLc7EefTrpTO0aD/04PfpA/xiaOEMzXARxjw1bkF9tnjUhioi0sfvF4pQ'
        b'AS5iGVxi9jiXoFed1YI8IXCGBqJZi1HfTh9agymYxb/C3lfd5kXQhIW+vjhoomZCRqgzQlWEGpxMdVjOGUAvrsI2dJDZ3zTCxRRcAJyJI49MJzng+l+GbmpQAVfhMBZJ'
        b'VDXEtZvGuqEdsnA/1JixSubjpemoqptMhTTamTiXYH16WwtO7yA5QB5PnpnOWtkHZ+xpDTfDBchW0HEQwcn50KVNGolzP6pgoTWw1NPOmkBqoRZBWwBHN6I+H3SNlrDe'
        b'TEr7iN7XJ01YhfJwCfVKOt6oFxU607tsJMhPUsfzUD4XF7QF9tG2rsUy/SF6j8wlPJuu4AGFM6LoBbgyBXAqnWLu6s20WEvZI/Npf6Bj+K8PGiOZnedlf3RIVR7p1Aja'
        b'H866qC9wEm3SLrvJww2yGaS/wjQfXJuV02mTMifACfx6EFwWQTbqTFV1GqqLoAO/ciEWVAoHaZPeJ8N6TQ31LY+jZQDeC50HuxU/MZ90ywYstvThjecgzQTl2Y4Zqoca'
        b'1LPmrsRLeZ+dCa3FohSDwY5Vmxqkxtrah45g6iRDt9GNdZhCbbGpsBJ1qMYdz4t2VkBOOhSyHs0i3ZUqwCVcRgV+JkmTdWchtKNLtI70ifl4PW5UZeOMDtDhwwJs67yh'
        b'7lTNBNIfkeggfmwWqqbDp5nhOtQY1YwjnQIlU0mVi13p8fk6vAxkK2zg2HJSZHYqI/fgWbQ56CiqwmuRajpnpU51UDXYeRfdKwJj0/Gtml3ktogznIfvzE5gMzkHuv1U'
        b'FRRBPaUc0oZ8HdyVW1lfYMF0hWoSkSfmk6UAqmahPi/oY4aB++N3Di1JbKqjK7gv+9CFFTSLVf54Zg8NOSukULTICD/RmE6bp6YJNWyhMOX9xrJ5BKVwgeYfDc1TB+cx'
        b'fi+CtN0MVaI+PbwH0/XsIOwPH6JatE9F21lz8HqTQbNIhdNyVgOUhZuABdda1YKR50azcFVHJ1n/04ZG0ByC4Azqc8ETiHZVkcX64aFUW0w7yhbVE5A8nKRU5wuNeM8g'
        b'I3nUmDyzREX8a5fKefqAM+YBi71pOEMPKwEVyzh1OC9Altf6zygreSjVVa5Jrea4RYKer0B+hVkuMnNjpnQ2jtrJz/JYIloRFu+jsZtdfMNE3WKZCBNSWJhl8a44djHL'
        b'xUBdU0TURmHzE00k7CLvJLZ4m9jiuYZZ3t3qzC7KtXWW/sBjUcg2zHKTiSu7+LWRdOVNHg+MaZjlB2PF7OITu/V0VnGuHJccZnmbVwUVuuYr0xEJ5hynF6b1o507u6jt'
        b'YhgxwK8gBYW8JJ/FLjbNF89wE7HSC5O3sYvjTYWMdTxr5mLvJRy1hdbdMzbMAbPbuPT5P05IxdLhKnd6Y1mSxNaBZaGl4Z7EnjZxVstcIKJ11boyewf3WXUV+ffcIlrA'
        b'qWVqG9VYS+KbtyZyn9nTfz8uYkzaVUzdh8kqxiVx81BZUpgG5WlQ0yQLBd6uMzlTdCwTFasxq2RCSaIovMw8SGpw2gv1uS2nJeZsHxvvzmof0rFhKWtnpbeR9TSO9sj8'
        b'aifbh40gh7yCkdkQozKDZMGQhoIgqTSW/IAkNjEyKjOVcG2PioKkqzkyChKJuYbOSFwVfsQQmFoWJqT4+vijij8LJ0X8P8jclOq09vP01jorRGE8JjETDUMBD4ifX+zy'
        b'zHSJMgiXXOn8ku/K5xMN3PTuVG34duCrmJoLb5R8p/miq/oHrvoegvQ3td6pN5sjT4mXvflc1pIXY93idTzuczpfKepK7UOfyBLVZU3MWbH0Renaie4ugRtee23DuiaD'
        b'fXmisU6Z35Uu5/kC85NFmmebwvl0y2lLRb5LN58s1ulbA5KQ62YhTxtZ3rZo+9A58YOZieGSnhS1lkuFF8635JWFfDRjS13ErrtTA5q9aqqcU/RjQkMkW5O/Lbz13jdx'
        b'CeUvHzj8aXRkzfWo4l83FFSkfB/mGrigpjrkI9lA3JjP3tRuXrbmmSU7CmuLvr+VmfTcL7Cyw+Sl9k0/3Dkz2eVOh+aBH8dciD1tWLzno4DTb9pJAsSmgT6/Xd+0KPji'
        b'ntO7o7zuKJt9T9/Mba6+8+bY7Rf3N0/sC5lrZK38/olSk0t2/ZLm/cfTx7h/3/40Pze13i3p8MSBk80mNhruJ/zXOQf1Vt+z188Ian9BaZkSdeTszU6jAfGWkE9MJj8v'
        b'vfBRiEPQ8jO3u25f+eT3TYu+WHn05uKLnnp1Me2W68UZso2Oet8+lxTv/9qvi97s2Dz3BZs7pyU60Tf+EfXPJ27ZLTfuCF/c9uNHHt4bt3yuMat7fKXeV6ezNrz68fZ1'
        b'1wMTb3bHJou++qh+VtLp7VfyjAw0fvB50+pf64Kypzf/s9fM4PVNFSm/vtIfFXi06KLu3W2TdoX3VL1Sdi717cTiDd/nO4LX085GJVPe+dij0jcgcuE+34/vlvxYF3vq'
        b'u4k2Cz/tlT+X+KaOqLP5g6jDPvuPxTpN/ebNRdN+rOnSfyG81X2dt/4fdQs6a7+Ovt31/c/fz9P6Z5PtPdk3S17Jidgp16Fn33Gr8GLahem2dzkmWQkn2cmjU77r6Eny'
        b'enRJhAptPGags/TY3YPHBL0fSlReWnog15tG5fMmbrFl6JgIlWgKrkzNhJp2xxG/ISSwiSMW/0Sa/Gwoj2In1MVwXKlAB6F1vNRLwokjebiCuaTz9Oa6CFRAfPF4WnqK'
        b'OVmGAEexwHksMJEeC2+bQwzymekaZgp6mflauMolAuZvj6EaBTn67k7AVRKn83j+nd1OlQuWqBJI1J5iCSdA10p0hQ825pi1TdGuCcxwzRTlDNmtOfjTdrjv0FDhciSc'
        b'llTY7oSu4oxq6L30ZSjbm5jJQE6MNy5uLA/1NqiDamjWotJZ3kxDBVmhvJstqmHWan0OcMb7gfhDmXAxJs1EPuH/1v7l8YeFan/zxHZAU7kpPDE0NiE8Jooe3P5CVt2/'
        b'Ygazh/MVC9T3Mf8///xeOob5Z9CkhjCaomkqR9jMbbYhviqlh7qG1EuEoeoQWY/XJ2dhIkP8y5Q6CdekjrrVebEgph4fqMtt/DeTBifVpCni5HsafsOOTyUSPNtIRAOi'
        b'2ISYEWe4f7FjtYTB3YbkdZnYtcwhPfpX7Fr2cs+MG2nZQnjpeNScqVgMl4c3KDrXjTeK1cnR1EOuWjUH90pyPjsCQ8irsFpCtOaQi1bxn7pofeR5HsEXPByZe5Lf408U'
        b'iVUPLl+IFv4GIvShcsk/4aFyJX50C3bSwhN/vgOuQpiP6+IELt2cozDcNlROGM7V5iqoobmHZ6AHmfSeEm6ezZQdUvNglBu7tuxzXklcSn7V8/1XYR7hN6PNyz4PC3mi'
        b'/VBW6cmc2bnNVUVVHQc6sqdWZnVJuKTvpb9MHycXWCQg37VkGW2azJzKSOcLY/GqVUuVU0k7lxKlOToM3Y9yZ7QbnR7EbDziSHlAtmlz1Ka4UMrL0Glp+9en5R7OnHnJ'
        b'3z4llHgrDiU+EYaNvEbkPEjqfOwIQhdG0bPOED1r419GhHua+9fpeS/3tc5IiiZEiQ77mRFXYlYeUKSCcjxkmeVNzB/QQSkUQCOcCuZQswvmR8fJUC26DD0UjaUH+yy8'
        b'LadAJQmUUyTmpCaCJjq9ikGTOqGGSCtlfgKc8eOEMTyHzm+jtNK1G9OKK7H4C4v/ll9JonLSN7JX63j7+PlZWUtD4BSn7i8ooXwzfeO5ZBlnuPMe4eJ9LtnFcUrCBO9/'
        b'dWOgdnKKKKGXhKDhbq2i7HajsZhTj2wREx58zhJzLp70arm/mAB/wi7i2fPWGrN5azklOcjyn/J2YFBpZPpPW0WcSMKbNbvR0nY4SDh1WwMeZxEvxEdwSsLD3p3x4m1c'
        b'4/NzZZxsiiN9bsJ4KacVuZFKIesFbfZcU2D2bTxWhS46nM61fCXhdzNss29/Ily9TE7MxpnNVpITwecTnwkM0s7QTq5ZugozwlZ8+WY1JekFz1+UVAPcbO7lK9JcyBl0'
        b'iD4+sYluFhR0ffak5FXd5yyf85R0fcep8YLdtv20XI8jrq/iL7ef5Jzc1Jtekk1IfxWTkNVvFpzFJy/TSz/ceLUQz1H3nRu4DV+E0to95ZRb+DLntp/jPuJyF79BrynT'
        b'nih8Wfwdliduc3m5HVSwCIT+HajQk4KE7MVQC42YfSgUvLDg3xfbcuS6SHka59x7/PyylW6Jr7lqXYixe87nfpL3+nuHgxeIZDPW/KTfKFuz+vWjm2csbbBeoL/Stbbf'
        b'NfJJvkyWXFbwavvn+jt+aEy0e/3HH3/sur38R/X1Szw+vVziqjfbaZ/13W8DHdxS7b8JSTUoeyGg9J0TNqerC54s+uUrp2rDb7SOPXfL1e+jfTfqMtQ8/9F0L/xW1s6Y'
        b'X49nwV7zXz6Ozv/nyRnPHPnSWGogC75SbzS2a7xtn/jO5ndvrDaKeM5sUtrpPTd+Cb/8YvRP05/6IujTifP0FEEfeVXUx/i3ZY/59YVX3Bxnad+57DE37+MZv2Y0+7Zl'
        b'1f6a+tzCbW1SQ4e6r+YfvaN8Af6YuVD45H6H38YeyNols7pe8Z1o/UYH26+uHIwLkKZM+00R1BLj+tbBtHsNjmqvVQV3/fLbvV+7Pmie6PtHnt8nSZbHQ22O/zj/pGJO'
        b'S9vnPhtedv71H2sN307Wi35WJz17bW31rYJv9zT0vnhpVc6Yb/+4drfkWcdzzY32zRs/Ug7cuS3qq5x92WnVt1M+nBSC1H6Z8eqBo29H/rz1w5zeEC+HSVZvoKafZ7Sq'
        b'nVryljjxheJ/vOP65n21okPHPyn/RK7HDBUOQh7K85YT/GaxlbmUk8YIFgRaSVnUVV6ok/qEJMhA1B2Eh/uQkARlcJSZEl1AjXuISYivJWcBJZx4Ng+tm1wZm1ZmDpWU'
        b't/PEy2+hmpYRfvmksFsG/cyKYR9k2yrTMjK0deCgri7q1EqRbJ3EGaPjIkxY+dAwCFzII4BWzOl6SdAxOMF4XSe5KohUipJET2rFHCicwVxpDr98nj+zd2+HenRU4QUV'
        b'gdQMm+ekKwVDqIE+xrFmu6Kj3uwOdIxjnCfkO9Cbs5M5zLGyMqcYcRoyAQ7DXuihZSZE7CDhbHqhXG5FLCukYcJ0h3Uq8y2Uu0hhvT5GPgwbsUZ5zO3aKTgJF0i2+Z4+'
        b'qXPwNiWDDgEvpM2Y3aVgl07okXh7+tKutk3i1DcIUSt0WSccRV3QgAdhJ3QMb3E7UQFrSomSnuccQPvguL+PHA+hi2CoueO/VHf/J0bFoxja4U2P7pxH/s7OOUtHQmPP'
        b'UMZThzfm9VQOwvQoSylWOQ4jEWAIA6pFXYhpqSwG1HnicIxYe+tR5lUsEKtuMbPqpu/pU4djLLqLOp+qO8RuSgbEyeFpmwfEkeFp4QMaMVFpoWmxafFRf5cBFaWOIXnq'
        b'kw+9oa2blGP4t7fubyaP3Lrp1OmbhQW1QjgYMWr7VuOMfcWG0IdObhJG8GukQkNsIGGCqVqZjxYNOQoQ/r77isGMH3QNImfal2RPOI9lNzggd7GhR4mY1dOHHhEm0R50'
        b'JPbTqC6xkiwSn31Q/lXY52FfhvmE34nSjP4gfvF4npvQJko22znCjYjosTr/AW0yRKMJzeLvENrmVIOhwRezoaKD9mg+THhwRMnLQX97RM/pjRxRwqWO3YjyvdH+ANJl'
        b'D4yp2RLJKnRa/D8f0pxHDanooSEV+cV+ptQWUe//z027wkYrPjoi0iNcPfqD5PU+atyUAZGn7dN/cbyU/914xaUaPjheY/5svMaMHi/y8pq/PV5nR43XDI74Xu8KUqCT'
        b'qNfvEQOG6iRhK+HK40eMFL6fjBm/Xxwt/htj9pCHHjJeDwdr0PRjniIOojw44Y2OhliOZM5LJZRznes5Wdgp5jK/W/TOtIqJwWPoxSgxZsu5NeEk0IKWier4fW4cL3Di'
        b'zSslyeGLltpEcVSdnQktytgxgXCOIxoaYtTQtZY+HbheDYunlUpN0zAfhds2lX+anNlrAq3QEYWHp4hLXCRdK/B4Q82JPTHNkVdm4Ac++E190s3L2sJsvZwPq75fsFTk'
        b'keY6uc7J41SO4pC1aMz26QaWGmaml1/9ccO936s1gubsNNIKMpkgm5QUVVlgWftB5hNV3/fdcTZ89+PkqNcjN70+Jr29+Sez7+dvnTQh/+qtl7/6tPRIbJVoa/T9n96+'
        b'n/nUh13CqQuTnnrVUa7O9u0jWosVxCWElbkHcaQN1YLVMqhR+STeazvEAXHaupQBQnVQxUyTr86LpboSzAP58xxUoGp1VIT5EHdDZoR5EnpR3+B5G7cFTtPjNr9wdvd0'
        b'AKqEFjwyXhRbewAzKbuFaUtWqiyFzdCxESdnqGuOgK5aQT7d9c2haL7Cgx5/wQnUJ57HYzm7F3Uz61a8PbSzAzlyGmckoedxcyc+NDPxHHrUHjY8X7XI+pocGR1KtkU6'
        b'XRf+nemaSGz+dMhxD93FyQ6uz6cajZjChJwHxA8Amh6qppBqTN7ZNFgvmsX6vz2Rz+iPnMim+E0XdN6EblQ2Hp5YGg63Y106BeWI0WkO6h9aITVU30rjB8J/lYvKtcrV'
        b'ooVIoZinBz3CsFueaPVIUaQ4Rz2bXyeOkkRKIqU5XKRapHqxsE6K0xo0rUnTajgto2ktmlbHaW2a1qFpDZzWpWk9mtbE6TE0rU/TMpw2oGlDmtbCaSOaNqZpbZweS9Pj'
        b'aFoHp8fTtAlN6+L0BJqeSNN6JEQZbtWkyMk56uvGREmiuagx2dxBft0YfIccamngJWxKpCm+qx85lW4s0wbUfMMTifHgPatRwWZIpCrTBHaLheEaHYwGM5BkrX5o5Rw6'
        b'6nLlVH6PqE0c7V6y72kMraHiP11DRXQNFd/L/rexjkbVdDjW0eMiC5HZwYIbkV8khlE4y2LFUnfT6Nj4R4RJGkVZhKbVH1rHJ/ulk81RgRrQKTrXSfgTfysahMQmwAPO'
        b'oXxLaz+4xHPLebV5aJ+QTu2sO+DqQllySiC+G+wOlaqnV6lnaCevIgGHVXFmN5mqa8Xo02OXyTtTiNMa5rAGVUE2tISjbrqJpKAzFopRIWTxKlOzY4oF1eq7QBU6r/Dy'
        b'ZbGlFTxnMEvk4ILltGur2XlOIxSgY952q2d7CRyPznOoRw0K6QaiCZ22NKC4uw/P4iN3bmQWL1ekcNXbWuWWXoZa/JIEVIX6ETOsWKJF9dfF/rp4/z1AnJYQ5/WoTrQY'
        b'dRvSDBJwx1zwhnMecA2O46qRbHSni9ZYWbFtsW8ravFmHqhJk6BHkDnvCIEr9O4i1AQFWAyzwLcFerqxVhuyULEfs2I4A+egbdh50hbUTZwnoTY4wBCLh4wx/104HKMb'
        b'dXjBsamolTnEOgLnUa83Xpb3z6Wuqnibyeg8NS7YAWWrqScq5oUKNcRi8TUXSmiDxK46o3xJoXbUqCcygmxHetyVoEEcvCVPE1zDtMomhDHPVCnQ4hVIkNlQSzxThUIJ'
        b'3Z3fdiTPukpIOJyYGSJy7kaOtzVw1boG3UYRn1GodPug2yioGEdfRYQL4EwDNLiw+I9TlzD3X+OhbI33cAx1lD0F+tbNZ311BR1ClQQkvSZjlCcr7UjmIO003vL6FMNe'
        b'rNDhEKj0iKIO0tAJVLD2kZ6m4Czqo+F8HaCIWQTVo72RmF5QI7rkS4UNPHA66IRog55PbNfsAIkS78zcbm7brrLLichWa5lnVcfEz36/OPD+s2ppd947Vzh26hLNtGS7'
        b'G95XzZcU7tx39a6L9+wvRZuP5fYdNU1P19rxw0CLe5D3+bj25FdeXP/+20sKN25tup75Sn3QS/u/nt3x5geye9e/ksYlJ19aVBZ08rMnZkp3Bv9z541qrTnPHkxvSTgv'
        b'czaoLfim8PV65Z6qG87ltW53f/98/8ufvVxyXTtya/yST5c6I524tMynv3z34MSFja2TFzh2bzL48voTft87Gc27PXZmZ2FG5BO3tLsDL7c/7/fajU132jZ2+Fm/ai2P'
        b'8ct1ClYGxwUUOm5L8X5m6zezPino/6gism1Cc+4qlOSJ1kPi5U9vFWfplL718cXiFcaLtz1f/vHnrWfnnZ5xetVrk2JKIwNuTnuu3ubGvp9Cy+9ml7WtfMXmxrSV94/d'
        b'TJ9+4dA9z7U5G06fSrqxy/rnT36ziW7s+I77/V21f0YcvbvPUW7CDmBy4MRMFRuCWZDtq6FtNrrI0BRF6zHn42Nhze7KUL8kXiCurZLZeUg29AoUYs8UASQ+7gRUuguV'
        b'Qj0DwuBZMplAxVDh8hFRQUhIEDW0n57tG+F5t3cUJA6/dN576HDfdSk7WWkz54jOJlCXLnGECYZGVgs4D7WYSS60GVrhZJFQpBRQ9XI5VUIaoVJ02tsfHV2kgsotCGMo'
        b'/0O6RiTyxyKoGF78jNFxsTN0mDO3JtUJqBwK/e3wyieK5xdDcfCWSJVbDDt0msZg8CGuFur4FUo4lDmPHea0CBwJ4LBiz4iwHKhxGwXjpM6AVqp8KvYfWvn054nU0AXA'
        b'okgA40ivoF4nnANe/lRLn/4OUUQy9ATvYhU/itqsaeGq9U8G9dIAgbgvQNlsZPahHigj8Q5Ui6BMAufNBHQiEOWy46j27ZwC57FxMGQN9a1wHlShQyo1JTT/iOlDK5au'
        b'hiiNrDCs+Wd0DfADPitVy4ZUXRgP+zbS2k2bB/VkNIZ93+mjRlGULsqKgkO08CQ4LqVgMbpqyKZDDyYc1OOURIlu1zLimcrfB7VpqpZonSUid/j/mHsPuCrPZH/8FHpv'
        b'AioqdroKigKiItKbUlRs1EMT6VhAFER6L9JBeu9NQZFk5mY3W5LdzbYkN1uSbEk2u9lfdnOz2ezuzW+e9z0cQdEk7r3/3z98onjO+z51ynfmmZmnBbvS2GGUuQveNedM'
        b'tqclizvMyAuOpCtqizCfW8kTOixBCit8TkUvqUyNaLE9tEEHv5KP/C+xrfKUCR2dA2Il2tmHusCnL8ECVvjRYDloybOBjoYY6m2hF2ZEpvLP9h8pv2gOBDvZ4WD6fQYr'
        b'vi5MvylQUeFKKPBpQEpC3vnGknG4i6C5H1a6gKXmqIhEBOMVhAr/UlDU4xJzVLi7AWSf8z9fKChpcefD3/QdFWGGlhQ+Pln+X5rWo7XS4lf62v5JEf+q1YrlSvrGZkS1'
        b'0fJEnqcG+/WrjOs/r6T6azQuvsa/rAdZef8tXFl9KTx9XGb+xer5S6t2K4akxkYnPKfC/g+XBsR3v1Rhn70Vlpae8gJ1tKUVq+VCwq3Dn9ntj2XdmrjGh0Ubx0YZx6bx'
        b't3YetT4qW4UXq/N+QfCcHfiZrGcjrkJ2iiQyNi0x5YXuMeB6+/3z9vstWW8bpb3xFxf8WyXKlUMuJUbGRsU+Z1vfkfW7k6tmH5aaZsy/FPHvDCB6aQCSq5KI9Ofd3PAr'
        b'2QC2yQbAv/Tivccs0TSXo/bsvt+T9W22RFxpy1iLqIxv4IU3QDEkUhJORPPMEfxWNoJNHFdxT794CX7Zsi9R6zM7/kDW8eYV1P3CXctIbslf9MyuP5J1vX25zcxWfslg'
        b'Xtn9st459fZkWItQFtYiKBTkCrKEGSrXBTIXgJBzAQhuCJ8V1sKafNr1rfSccJpvWF5des/yF6dXvbGXo7wrMRLuWuO0GHZv9GP6S5Hw1zNw1wonJKY97Ul4ypuwtElP'
        b'efJfc97OF85/p+MiVzh/ejbq1/FkA/cKfxzzJ1Mhnzy/YLWBu9TuMa6F+3CXYVuJ6TPqumct5RtzF+V8fdhxU6CYsWlJu8lm+jhIJipakub77ILwrNs/M/XN0mS/tvrO'
        b'FtQsLwyfzrJgsTALa3FK6hzBO+Y4CHmyJSCj5InAGC4wERYUVAnj1WPJ//jpzNeMvKI9VbL4DznudMZG7RN2OhMX9cfQ0uiew9z5jLdYsGVW3OP1snRvD0Gttmxvodhn'
        b'mdnSFP5VhzcpN194l1Wfv8upkjS+mxzhE6FYt4TLO//sBfa6dMXhDUusxQHrJ/a64OhztpoMBrbVZqpYZOYhLWjsQ5t+nycCOU2hHZnBfYbYyCeyWEAj/46cDSv50ApT'
        b'obtju07pizhh9ftX1S9Gu0d4h3mHxb3bL4mJjon2jvjkvz3DfMOEfzG8aBhnGHD697vlbZJ6xYLxFqWfrb/yVHza6rFqKRIphfAFvL7J7ojVFDVEGdpP7RDf+O0n92Rl'
        b'lx+/wJ7ULo9GW6XjZ8td7uiML3wvkB2dfR3py9y+Pk+JTmcWhJfKa32StSu9vqnGqWmx8fHGl8PiYyO/woErFKymQRR8A10539nozUyBEj2jlVl73fDStdjYMAtN+dQQ'
        b'9oJG7Uehr4eb/M4zTC3qA/rNQkdc7e3ib+odeih1Qr8y0vSNW38JVvE+Mhi31r4hztDesLmx+GCcof64VaSgeLdF6NlXj6Pxy5WvtEHLa/56im+Irevd/G3UBW/8zvCw'
        b'hq2pEmfL6m/ZYC61QqHnGjNENWBW7AaLMMcb7d04iTNSPy8W7Za6ejOhGDt4v0SBO05LnaYeG6Ru08ybfN3CnUr4aLkTWA2LdXeKsTlAekFjMNae9JI6JGx2S72xwXpc'
        b'eR4TA00v6yzOuuZuXdBw5vsbt2clGIv8PDScYVhOoBAv2kLGeBdXpSjw6iGvgzDsAcMWCgI5IyFMHlWW6qSvPNBSik0N4TaUY5Vj35RVdPkigtz/LCKaK4oht8wIXGp+'
        b'mdZ6xpgeq7Fd9Og/XoCNCnRWtUNlQzDVXa2SxLKSEdx5WiRbFjGzwLirbpkMeVtpyWp4W2kJvr+twCPhtxV4iPq20hJifFtJBvgkS9Phhda/f0niMmFjQL9eZKvEBqwk'
        b'khOrCY3O/m8VcdBQVRPxXuxxXbwtUxbyggDIVoFyETw46veUftaR/p1668mzQYVaw1pBpKiMnZgpFqgX6BToRsl//TNB/i0CEKqRareV2JlglECixJ3CKbG2I9XLhFyI'
        b'uSq1KxepEanJtass+06ekKpWpDb3qQo3GsNInTJR5DbuHR3uLb3INbeV6XtV+l7AnqhVpB/DSP0yhcjtXDEKeeklI+oFGgVaBdoFugWGUWqRayPXce+p8e3Sj1KtMo11'
        b'fZk4cgd3DirPHdSxa3M0CjRZbwV6BWsK9AsM6H2tSKPIDdz76tL3ubdrFSM30vs7uT7Zm5rcW/r0hjJ32sje0ODmt5nNj2YgitwSuZWboWakLifxTd7WkPIE/RUWLUl5'
        b'dy9tzApB7mS88gkm/envVOMwEvzL1QE7FgxLMw5LYf6W5PRYov0VDUUROueej6SvItKYHRebZpyWEpaQGhbBDNnUJ04PPdJIvSSmSLuS9RKWKjOBSC8lGIcZR8deliRI'
        b'm01MufZEM1ZWxlfCUtiFYvb2Tx9PMuvqiQnK1NpRl0AnK+NjiQk704zTUyXcDJJSEiPTueFuXnkwK/WcxdL6PZXrsLJqiaxiCdt6WdUScaH4uVkOUgPp3TNPbhC3VE8c'
        b'zi5p6EtLU3qh81nZijLTi7Z1+TasamOxvee2LNLK2INzQkUm0ojIJjOWXI1NTWOfXGErGy713khWQQ3SAUmNbH5MT5neV2LZIOmbqHRqLiwyksjkGWNKiKT/jcOSkhJj'
        b'E6jD5U6qr4AsbBufziFR9+UwctpG7FteTdRd5ubGaizz5up++rt7+y4VSYNFLFD1P4896ZCbzsq+YD8Oc/npqzQBBVBDL0s99JexQDkL22GSr5lQdYZeqiEAjTk45y4n'
        b'kN8pxAaowT7uWNMS566bK0LVAZb4ehXmIJ+T0muh40yA5UYcwl4CMj3WArGVQPOgaJslzKTvFLAyCVOuy2+7MuFO09ktVyLBflO8HyoPVYexmku43U8P9puLzmAxu/Mj'
        b'Fbshl8Nwr13j7hgJbVQPVcu4Zi29R2uCjIV5L9nU/LGQluI+d59WmQWW+/Dl104kKmI23sFu7uh7KwzCo9RkeQE2agmwQgDFB4Njb//GQZT6LbYXEqFLhYMG7FbL7xLc'
        b'7PPpOPhdr0G599bFnxNVZpdtD6g60ln6oUgtKsd828/f3d0i3Kmaa/nljeuza9f84T3P/I/Ttrr2/GHOZE3Qme1Wkj99OBAxHNz8H0MKJyQd/iF26SNa2gcmdn94fuF7'
        b'+RZzsz8C56Lj/xmWs+Znb74/XfbjuTvX/1V9Hky1P2utq/qhDljo2G8cNf/ZX3f/yXTdf/XJTQZ9+zd/0T66ceynLRu+0H9PVePGS/8xuK5t8Q2HlIgff/KXrt/sVFj/'
        b'm4pNf/ve4dSXy031OKimC53xXjDrwJ11sVN+aD/ClXfHbpzZyo73TOEh1K0838My5GvY4UIA3n582o5jUM6O27c5ced6J7DPaSkEKt+Zi4CC0Uw+dmomGkaWHT6aYBM7'
        b'fFTezB9NTm+LexwdBc3YwcVH+UrPtzbjRKIXF1yxGfNZ2UhlPRF03MRsDuyKIFeRxZzXrsdSX7brZgoEpqfFJ/bp8o33Yp2b+S4stiAWWCTEoAD9IguYgAHu6wyip7v8'
        b'uae+jezkM8sDb0mTHu8qEpSmxdodLbdZCK1Zsdxct2LeDVZevvi4zVJkOTxM4gPpW40wl5U6xyJtKGS5GexeA0sFgQHMyrnrwCSHwUUwZ8DhfzlsZEuioCtSN8dpzisQ'
        b'ALfMoeTcVj9fL1Yfjz+Q1YZ6MVQc9+PLehpjDpT4KZ15zPEaAWIfyKVhM2dA5A5W7ZBLZVVjLOHHJw5B+S4vS66AIysY4QYTilCBTVv5vW2VsArpfKjERhYbzC6kwH57'
        b'/hizKfQSy4HZBSVmpsurIOoc5MlnQFmPZS9heQbMwFJ/CgJ9gRgX5WDx6RCyrxO3vdpBWiCTld/ERLBjseUKXIS6BhdtrsZdr82i1DdyBgN/2JVhsFIxP+Oqa5naXXbg'
        b'9ZyDQzH/7CrHXOtVaTIs0f4bGBjZgt8vz4R85pC/iUte/vmu4YOqUtfwU53JDr9sZHr8acW9TEm/4GkYdyVv2vMOag4vDTHFjAWrLdepK3zTnOuPiwSUuf6+jnf6qSDf'
        b'/0+809FkpV4XPjGdpXV6yum4x1JDyDmSVWb+uewG1kLhzeiZl6xMhRyPum3cBiWwKGBc+iSLwhDc/QpfcsoNdkfojieoIDUiPoRLnfxGTmLnFyL+xRVuYhd6O4tMv8ee'
        b'wxn2i7efJVab+0rsl00S61b1Fxtu1HCEvvivCAznfFsFwn8vMHyJbp7Mz0h3FLAIwTM2UmktE9UsqLDI28zTIoEU1GAgHzTIPvPzZkEktF9FqnY4Cq2xDnnu4lTuzu9Q'
        b'g49CrXT+EPr9cBN9szDvsPio+PA/hn4QmhD1x9DiDUrRnpwLWlFQp6qk8/aPTMVcsV/MNgvgO4/BJvPnqgrbg/wlL3k4mrg8zMc+aHkKLy5e5MhNAe/a8irhMbFBebiU'
        b'3goOL4UQPF/uL/m4U7K/LvWtdF4/5T5f6cH2eSFCnFkRt+wh4MoJEQ+tTorQo/dcWuSc04ZHNTwwDx6ZivhSfT04ul7q0HaJ1hRCnw6BVfaNCHPUpf5sLIMcGyFMKVyJ'
        b'fbdyrZgTcJXr7KX+7J+GyDza8dGeEb6cR3vtMo92lEDwioVymFPN0x7t5xw65Apf1K19Sk1FSy7D8FlbuMy7/RXdH32hTXtp+cHDs4dBApBx7rOFAnPcsSBsEgryJBbk'
        b'ZWJB/JWxzlGmcl/0PmUFuknSyPyVKsnlPo5n28+XUiRRvK36VNDJKiZuiiQtPSUh1d7YSXZ7uHT2ocaJ4XFkdX+Fabq6xpP3TWfyHfrIfJonCM6TftDxU5Ywh/knT60S'
        b'HE2CK3uvctxua95YG1TDQa8nLFmuwF7ecmPNX1WRKL0Pc2PfrSsXpvrRm786rPJR6B9D/xD6nfCYqEEJ89Offuk0jldOnO65bSpvsvVbP/z+m//x5svHxd0XieSnGnLi'
        b'gicbphpLWjxPBzQcmdxX+rLanqMtawU1ltrXjqWYKnCgPgEW95EBAwsJ0vhJGDWSJpbcgDsEhqXhkTDqvGQnbAEeskO+OjaqQt05ZkGttJ726qTxV+I63WQO+2wok5pe'
        b'1yScr/8E9mCtGhR7PcbyqmdEOIqDUM7L21vHfZ6IqtyFvTJ5a4OFK3j32Wh0eSEFlkcipR2Om+2/KTcn8bFoSlwdkYx1T7DTsuZ5KDAgjRXjXNyPofOq4n9AxD/2GDA7'
        b'UhOBL8T1o3rLuf45w3w2wz8V0/BVCGCJ1WdWZfW0p6NKEqOW8hP+9znfie/za3L+6udohDiP/yNcmMqCYD/7zvqPQs+99MOXifnqOvI3l+xpOPuvHBt1wa6X5TJUdU1F'
        b'vFFciS1Qz2X2kJU/elXmv1+HrXIZXtjG2aBu6TDNYv2joF8W7g85yTCydJq0+rHnthdWSTcFLLxxNaqQbo0Uxx4SLeHYw6LlvUa+EE22aXwVTUp7N+UZ4W3F1LDLkpCw'
        b'VN9n+3rZIKQ6SYEzcRS+gaeXjI13w1fz9C7RK3OBR0pro38tanWSueslaWEsZiyMj525lHiZlByrZr7U7v8UqfPvSBfKnjmEOUe9BfMCX0pPTWNeYJ71UtNiE/hIOma0'
        b'rurG5Q3ZFfFPzE9Pja/mQpZxGRtrStgVfrlozl/BXIyMn/b4qvimMyC3MR7KVyjVxwoVqqHjaaXqgQ08dCyC0ihzlt9DQH3WXYB3ruNtrk7JZxe/FfCzR1yJEzmBXKMw'
        b'TVvCl1m8KS94VVmHVRr0ntINEgRy1jRXxtjQ/Ka5HzVlkukvwKaNrrF53y8VprJiysWaIT7ft9Q46qQl/rXv7/8l53xc6+CpXxtnC3JajNvkfjMc5mytUfH2gqmqSsCP'
        b'ekOMt32h3KjcoVt8YPAd2ytNty2qfrvZqWDPX/f5vec/veWTQsvLb74vF/2h98jQSMNBmz0DFz8cGav+Sb711bNqfqOfXGoZHfqs/OMvyutsbdM/CXCLXvPyYuZLf/yL'
        b'8MiF7S+/oWeqxBdLq4BxeEQK3BxyZArcACrTpDeR9+EAluzHihU5Dlna2Mlr8KnMy5z/0wdGLFYo8BvQxQfKd8MDbDD39ImFYVLhnDsQ7t/gJNdGfAht5sf3m1lJg/CV'
        b'HURwF+ZFnAZnl4BE8y5BC5jReMIliPeRzyFV36IqdYN2wLisbJuDrTRM/xhX77SYSU0FnE1lbsxzW1bXoKYKX9ex9raiNKOUE6Du31yAai2VcdARaXGlHJS403g9YYb+'
        b'KoKNOlrpT+MUvZPoq0EBGQWPn32MDJzpn4kvJIVr9JdL4WcMlhaSc+BxYlhZFlrNH6zvZkfzcvFhCdGBrhGKyxibTUVnibH9mWRmuZHM9aTCHZ6yA1tRgWaBVoG4QFt6'
        b'PqcTpSOV2IqFyiSxlUhiK8okthInsRVvKC2T2DfkVpHYTpGRLBI7QXJlZfQMO5jiD8H4M7uIxJQUSWpSYkJkbEL0c9IiSY7ah6WlpdiHyiykUE4WMs2QaBwaGpiSLgkN'
        b'tZDGgF+WpHBxCtzp7FONhT3zNNY4IiyBSeiURBbbsBR8mhaWQvtgHB6WcPHZamLF0d0TwGrVg7tnKo/nKRy2EOxkMTVJEsHN0IJf5VXVx+MMgIT0S+GSlK99DCkjMH4Y'
        b'j0P5r8TERsSs0GPcjBLCLklWHUEiHze9tA4xifGRRNTLtOITUdWXwlIuPnGCLtu0VGM+EcHK2I9FxF6JTeVHQKo9JjHS2D4qPSGCyIOeWcLSoas2tDT6iLD4eNrjcElU'
        b'olTJylKQeSJIZwHe7Pg7bNV2ltPQM1dSFrtmb/xklsLjCN6lfp8VySttK9w6/OlWluc6fMX7TEIQIgnwM7a1sbPcw/07naQMMWGkZGmrltoi0uepZPXA4mOSqLD0+LTU'
        b'JRaRtbXqju9MNeb+ycIUnhrcCtgipUw2lSSyE+i3rwG6VqAZTanAW4lmdvryicdDRlcwF4pSrUn6CxPZdSMlMMTjlVFTGDqAJaqXk4UCIRYKsGXPUWn9OYUQmMNK6DIn'
        b'05iMZigXOuOMD4eP7KmBGnrnBO9gMLGyNMHCXWYePgKcJWQ0GJiEk2kn+SNlqDVTPgCNalw+tgeMkcZdfhDuwe7e4pLrHp+CR1xQgg4aGgeQ/qqoJjAUFMorHA/1bnEL'
        b'llZSLBBxV7DLzrD5aD0LU0tPeYGjeRj2KGDTdZjhJ9mb6WiO1dCKYwoCobYA2lShgWv7xk1Wn0PJQmgcGm/moc+X+NhrQ+hE8GacypHQeM01J/gPp9LYgXc7KwZi8ZrD'
        b'GT6vGBphBiqwSyRQVBSoClQDr3A1n7gXgsOVBVqCz93UST6Xx8oL0h1YfyGEGllyeYA753H2wH68SzMoNWeuGtls6Et3C09vKw9LMwUBlpiqJV/R5wIJInEam58CpqVZ'
        b'SaaePt4wECgFpaYKAkJhc8rQJZJ3NVXiY7d6oRYeYom3CwzKMrKhmT7K5zKQYQQeQQP2wH0vLJYmZEM99HIlS3BBG6axxOvU6aWkbOiE3hN8CnmvsZrXXr/lOdla4jXJ'
        b'UMA160EjqvDC8t3QvZQXDfMmeJvPVu7BHmw3X5bh6AkzXFq0tQJPuSVmdnxSdPB1Li0aGoTwkLsMNpEQ3r0nkqLDYvm0aC4lGuvxjqkq18xWR9qlEkscOyVN64chLNrB'
        b'58djGzQt5fQbwz1prOf+pVL5d7BcaUVOP44osHBOnLLni7mUhcAUlm7zspYl9UML8ln9l1W0sdff6/Fx/yTe4Zesmt4Z9vJTkyX2c1n99y9ySf2ZQUe5nH5ZWivMYBmX'
        b'1O+K/fyoemnUU16P01qhU5OFkRLULeE2eydNPn8prR96LkpDVGkPi7kBnLc757UsV1MTxrgc8c323Jr4Y4exNOsfclyXPAFQDrf4KY/GHwuwpJlBL84TjhZLhA5Yyl/B'
        b'AY04Da0B2w+SqVQZdJy+VbAUQpspPOKy84evMNYqVFY6Emoxc9hDwLGnFbbvMz/NAl385AQiNQEuQuFaUxX+cok2nahUjZR0nFDDCTLBNKEY76XRNsSJPYJ8OUIgsq6G'
        b'PtlD3BOYK0zF6XTm4egVY+taE65QEfTu2sCeiwxcevJKWrJyirqGgsBELIe36Kee24HIFEecSsfp1GS1ZGpsBMo0U9LFAl0j8X6RMJ3VZXU6fzg1OV2Fa0QTZ5RxgrpT'
        b'uwhjyUSH9/i+D19QkL+EZfz1Jl0JcE/2BlTvW3pIVyJ28qTf2D2ECVgPd1OTcQG6pQ/KxrcRRuV2OEEff7NBB1ZslzV2QYVWJAWnaXwuYnsFW55CyrzlUpN1Ti+1Q+JY'
        b'QaClIMLR3de5IgfYCQNwWxVn02gkasrqBOjVsQarbohgChqVOSo6G4fDAaQ4pi1PHj/O9lIe59jVkCPYxd+p0QxTHgE+WBWAZXgnAMrkBBEwrcQul5zFUgNe7DwSY9HK'
        b'btzjWScbtHnJUo23YCGVXhgL0KRvRdgrNLNX5LQMFCeTFV3iQdJul4+3XxDTJ/4kJzsPcQa4BZOWpR7eWEyCA24FKZNVpsox3gUdzPGiMTW7iAVCewHWYr0Kt7Hbtp7H'
        b'KXcSGl6WxF2+cgJtmIqFFjHUQSFf6/TYrvWCvQL3zWKt0HOPMtdLr1fwNhMECu6rqGmFbrlgkiXgL38QfH5Y+ovJEVM57h6CjBskF4do5AUpgmuCazaX+VIX2diNQzAk'
        b'x+o8PhBkCDJI55XzFxf0RcGwuSLJGX8WwxXnwl/91OpB1m4JKykyI4gVxIbBrVjRT38qlxpPRk9Y2keX/B0S/vOIVut5//dCOv9Z5f2lxOH1xT3Vr7uUVx4QviewUrQy'
        b'OaIVc+rlyQmd0PNv/kh4rtLuWLFx9Ksn/Ls9G+952QepaPzq+5kODg4283cDkrslVqEL59Z1t4bXvBLfvN1h/1/e++CNsJ//R8Feg1OiVxeu5p3+dobpj7eZvJ7W/+O5'
        b'X398u9gmqe234Uk3PnFT/cUPHP74g9/WB3sUDyb43Cn4wdiAnn3grVy1Oa8BxbcX/3bA6OWTOdUzuyciUq1/068P7YXvm53s1B+5+5Nt7juDNO+H1BQ96qv/NN/3g9oD'
        b'e85ozP0tOOrXoxEbPiov/334exbHfuT8StbZZINPbrS9Lvnwg21+QzkpccJXVE38N9zbkDS0PfDjo823HE4kzJT+fPgn01pTV7zn+zZEBr9WEKp1yUJXMz4tcmT88mtv'
        b'f//t9Iv7h38xfbmk/uPrn2ZG9m3pqPuhp8n2NB2zt2Ku/t3KzMHnW5P/2eIiWbza8/JgplWB3I7JRyUXMh++/c7IwY1RkVdzy5XXxa45pHff7+9fXv3VX1773vzslxfK'
        b'TJvN9FM+mx9Jes36huXH5or1fy3UvfBA9XsCx5pXLKM/+K7tmPOdt98RJhrvf21AbUbs8srv3jn1S4utG176ciA3rq/3oyOK9Q/Mvhvz3uYv1qe+9YaTTf2HOXPaWRrf'
        b'r/2y73d/+uhnP39zwvrkxFvOf/3Bt3/f/+5JQcFP24qvFVyxG/iF9YmwRxU+G9+/+dL72p9s/PNfX/ZRPGtwUjMQTkTdU/9lR/nZT8cbXT5y9N+Q+0dXR9v1QZ9Z3OjM'
        b'eNPq9+992+3znwa83zjSunE+7e/xOlYt7z0wdvrTdzL/6575F563jwRci7M+vP+tl76daPr5pwYmbv8Mfuvvplace0bBENrMVwYu6JjCuIcY2g8e4G8QHsfqRDm5x9DB'
        b'XMx5fo46JXstnWn7cV9qb76CBWIodbrGlQVQJgRQp+q1A0afOrs5AxVc8Ygk+QSvtM2ywDcW9Hb8EH8hay4u3oCSlaFaMZu4YC3IM+feXpsEDeaecFfDZ8ltlAGFfMHW'
        b'aZ2TXBiZJs7K4shum3LDCgo9a2610YVzGj3pMeqP5sPq2kwPwBBXrMwBOpbqlUGeP994L7Z405rNbvfBMgWB3F4hDKzFAu6oawfWqnPOJOizXYqJ22XNu9FyVYKZGypm'
        b'Dx+Px8fiQRE3FbcT3l6EBi0vZy3VWsUGZa63EOw54mXO1hCnPb1I6V4TbXPFWt75lkNg4/bj4rNiT0W++Cw81OTTSzqxf5u5uzm0Wcg8d5AHk3wyTC/2waiXFFdC3wZp'
        b'BCA8gB5uMt44FIJNtqzq6i5FshI6hUGQ7c4RxY3kcC+P62JZOssJmOeCE6AeZ6ATSywI89FbWOxjQRpdG2/vEhPeqvLil3dQV+iF3Z5PHMxZnOJ63Y614WRKFC8DV4PS'
        b'InUE8yt0CTjtwIFlOBcHBNxKHbJXYTcRVxEWkyFZM7zFRyt2wcwRLyhzfgLLOgdxr/q7sDPEdTD9GMhCJZTx1S1y4BE+WI5kMV+HQ7JYQLNm40ohtFvMg1mCUrNSOIvl'
        b'4WlcjZ9+7lqnFXA2EWeW4VnoxmLuOFQMM4asHf5IknoaiNTEbHGiFUxw+2mPs5GsBO4uPzK1FlkNvxsisyOEABhaOohThzlsg30qDN4QtEnGGXUcF1rDLaEFdsorr3Xl'
        b'xiu5cN1Lujs4xPJisUkExXtgjDtTIrNlYZO0lh8UYbX6Lv6m9vWurBT2DN7l92J2TxRXLXAfzEIpjsoJFLFDpGR4jDuV9YGS9Uwr4gLmMK1IUOsuv5oFsVAnrU0iLZiq'
        b'C2UxW8WEaBf38P0/CsZO/hErH0KdTVhMKJ36xwY5AuDj6znBZXHWx9wXbmMLPednQTqfNkgkMNgndxja93F3P4sxd4v58sKV2oQfl9WupL3mWvKGwRgv7BSy8RTzu6IK'
        b'ZSLsoH3v4+aqTip7ijulLoI5Zwtadl+REVld/LeKnps5u20pSvbYBS5ONtyf21K3HRvp3QEY1LwslYDKOCCCkUQY5kjvpCpLrN1laWpiecWAKCdaBJNbYdhU89/PKXrs'
        b'4/1fvNd5+eF3WGTkisPvvzAE9c3c3rZq3L3KCtyFGUu1kPmIUlbx2FCoI9KQxZwqiURCfXYDszTWlH4TKQhX/HwupyonXPHzudwfFTYpce3xV3zw/mol+l+NKwgjx251'
        b'/kxBTUHIqitrcWPREGqIdIQanAuev/pjHVfeRYOLe9UQirhxanDlZJ46eVy2LFInvTLvaZe5wFOOMe+7zPmd4rLScf/vVbhW5Pt53DDXI9eZlaxvzunvQb8Vq0ozXL6R'
        b'0z9b8LnV8w5fly2BqfhtpaUzz8eZeRFygsf/KQiWubxYYDLny+d9/cpSX7+Q8/YzX7+oQLtAp0BcoBulK/X0yxUq5Aqy5DNU2Ims1NMvz3n65W7IPw4keDdAtIqnPyhJ'
        b'GmG70tHPubzDpC5b2aHts93nS0+sTMdJk3qflzVhIXVCR4QlrOqZDGeHDMbcjTnMi/jsI4UX8baz84tVezVbGp6ZMZdywzlGl8bBu7n5IbEzCxp6Au9aXt3TbeycGCmx'
        b'sTMOD0vhXLP8hFMkSSmSVAnX9jc7jOYWUHow8WR1ntVOFKj51atJSP3VS9565iD/KofuN3Xfrn6FzSbfdJatCoVYo+PFX5vtk0zGbJn5iRVH0iuPo8tNlXEMBuU5h6Hp'
        b'KbLWl/lJ3ZnbEAv9AlY4TDOwD+dxQBnKzHGeN1lLCW7ksoNsUu5zQnaQjSNmnDH8TxdVwadXuBsE47+8EsvfPWIY+RJ394jgP7/L7h7BwnQWY75PDWrNoZ8h6EKsCGAu'
        b'Th/qFSs0mOt3KchWFmG70qIXB6mT9izHXt6HOwS90MVfq8yCwAQ+pjjI55OfPvMPgZaoQai2O1TyZvCUHG+Uv9l4JJD72u3CGcE7gv59GqHZcZ/vvmHOf+3aeYT7Ntsw'
        b'TmgcOSgvMA7NdNp4mffr4qg8VnNXc8PUJvrjvn+6M1NSUG243HeNhZaePlidgDXMY0uQ0UPqD+cu9PE64e5p4SkFg/ewQt0Tu/z4oL378HDXM8ILpHupQVj+cXQBVEOe'
        b'tJi8P7Rc4Wv0YlEMTi6vJh8GRZzvxxi6abUISK8sVZqJt2EinUXpQK36taedyFIXMkcYI4r8ewzWKmetucQtlWWmWPBmJAvECY2PckyTekGOxPELeTD9lGBaUBiueSQ7'
        b'481rycdTFJnGYO5wU3luUXdBt4D5RgTXoNlBcC0Zb3MfO8bjOAOBgowD+4gQp7CHc4HsJhPhFnelYzxmC65iLxEme/w6d78u/RK7JUkQCwXQwvkdHZNYVAYDxFiiIMCe'
        b'fXK2QrIPWrGd95jlYyVULnd5amA7ZuOo+DzeseZdzWPbFZaKjmLRWs4wCMuKLd3hK5/aRlT3r+16jpWOqbpOavk9v1ioWPjrz+3qtXTjBqd369UGpm1z8Y/s36v3mXdx'
        b'quclPPGqy0suKt9dWISKX/d1l3+2u+3SdMYmj7Ft/7VuS/H6pMz/DnXvsvngEwfPqSzzHW8LL7/2L3/P2Mi3mj/O9e7+MPnnpWuHGn/wxrH6fcEm/6r457fSQ2Zq1j4I'
        b'fM99IOSSIL+h6vWO+AjRL19y+Fx0Kkm1NPOdRwbvHHL8TW1FkGHJb0wMbSe63wuZ/uzKjjd/3a+29uxf7H8/pvfH/vBM4cj8ydcUvWb+UL5j8PBQQux3P24/22RS82l8'
        b'xfmeX8zU/WJ/zY7CU5vqrSXpN6IvH/pNi3n6QKDPVFfz36v+1X3WynXxkO+nogvWn1ifdU48uvn988EL5m+ZvlV4+Jzt72/FnTm07hd9am1e9sE5vl+MBGZ2Nx3YYBy7'
        b'6duq6TcjtaPfm+5yqrQzOPfZul98qffBZuOIlh/HZuS6tE8dT35lNC+t+Xiqz5htQqJ9+18/jRgqvuBiem7Xm932v7145kcffdsoPTz+Tc0Drl5/39Taf7dkzQ+b1xhZ'
        b'W9YXfLD3T4Ov/3Pf55t2DSjVr1mrb6rPm7Iz2APlS3lwEyd5W3biEm8Id5Fh0Hsc2r1kpyScKYuLUkvZPQImVVfEkIbCXc4VkXyNb74Bi0PJ7NoA834eS5UYkqCUL/+Z'
        b'7Qo1fFydmjln70IL8Lf3HYe+ZD6R7aYv54Lw0+ZDUxqttWXBpcfFT1zHBYtkO3D5XzVkrhWzqxPZvYlQiTXc3YlkRY7zVtbiIeWlqxOxWk16e6JoOx8dg93YfVh6aQwx'
        b'wnXuzhhi7Gnevh/BsZO0bA9kl7zwV7xgJ+ZwnaeStK0kiTViTkPjZqe8QURj6IdG3tFRD1OK5pbYhvcfF4xXF/OGfh/07Hhs55eSEcPb+szQN4UCrgM7rD/CKvpCv7fU'
        b'haNpa5klPgeDZryld4uMuxrORsMKny2BJFMrSKEpCNZDM9mans78TTQOmMdevwrF3GV0CkYiuXO6nOl23RWmloxJbHKQ2pPMmDTF23wCXdFByJEak/thzGeFLZkF5byz'
        b'aQ5vGXAPPbYkoR/mOWtyMCSNnTBg30HSmk/fg3ASy3lzEnvPc8PNEOCs0ERq0kkNOgWHfxPD6/4vGnBPWHFqyyMOODNukCmDb2bG3RRYqXHmlIr0XkQlqeFkyF1YQ5+I'
        b'6RsR+01Leksi/ze75oZdccNqaapwpteSsafFmVpq3AU4LGGJN8ZUuD/1uX50uD8z1j+ZgrBsPlL7S4G3fDxl1hAzQZYZXFr/0+trKresMytZj5zV5cesELWlKwe+mdVF'
        b'dtfu5XbX8+a+FOllzQZiI1rF5mJYlcOpDOHxeRjS+vMizu4SM8srSk1mZcl9pZXFah04rRYBu2RlPS5CLwto5eJg/4cDtvl3lmq88O+tUoDRytiZD5XhhvKMECAuvpuZ'
        b'YvSoR4DfAdvde5jpcyksjQV6pKalxCZEP3MIfHGZx2EvT5bB479/obwRJT7AFSuicYJlbvdseg4KXQ5B7we58gd6rdAAD6Rnzxewe6mgPA7G8yfA08wTy4rZN1gtqyqf'
        b'eSaYv52+GYdJosvOtw/HykrWrzeO1SnQE6dm02N//6DGsnhCHXbrHftzSIuW8w8EhXu0vF4S6I3qWOoqb3b+cG/De2/CL/W29sxnZvi1KvxduVF1uvG4Rcfbf/08fLd6'
        b'ZmRm87m4Bw2GByo+Maq0SNv5jmb4wwGDme+VnioLn931yhs/ndEWRW3a9MXUxfhXgoYfJT70+ZPkzEdW/+fupgSnrX//1Q9N5TmP+9Y0MmB4NGGLdzg0kaXCX6k2u0aO'
        b'NJsm3FkR0Ap5TpzOOUlmgaqXHZY9daphLvUYG6nD4BMucDm4y2lGaDvJKYkLp4KXudUxB2qD9sG9Ffkm/5bCWCbPNdI5Vlsh0X1fRKLfFKxbyk3hb7pdkupMdmdseELy'
        b'rOx1pdxdKYaWyd1vVg+ahCr3vvVKycoJ1RP02bUXFqpFW5YL1edPjRU/zYhNYj6Z/9HyiEu1NAeejkVNiYiJvSytqCOt27qihs8qUtOZd3XEX+N8I7GXkuIlzLsjidz8'
        b'TAkrndST9WTo469z1YdgVRkl55vOJcc2qeAgf271hJF6dO2ySKdwA6XYfftjg42r5blc71ZbpY/evhz6avjpl958ebpywr3ztqn8qzoRMVHx4RZhCVEx4d7SapB9zUqJ'
        b'xrmmchyrb/KzW6rdj5NJnN0wrcoD6EXo8ZHaDElqS1aDPrbysHARSiKXWQ0iLJOV7mjHmTSWHIwLME3od4px+gSWsmsPsYzVm/TwSbY0g+JrnHjwgiFFGIfxTV95cZhW'
        b'GL+5S9SVyvHrgRfjVzvGrbKSlDJf7BM9rCw67r+SI1fWY3z8BMdkgfRbo5r0vppvzGTZgg9XpI5+1ThZXQV5X99AV19TkS//v9ZXFH57XFWC5bdy6W5cfhEX3s65uzn0'
        b'xUkLbjb8Uqz930bbX1N2p+ynXzVUpYBMSSSnqiLU3/RkDTctLTWRklBPU0mooULfr1PiLzb/Uk4k4CsnfLnjho7QKkFHaLxJSciFIyVindaKpOoSXT6vWiQw2Sl/GW5D'
        b'TfqnIhZeehXvQitUOyZi824tyMd7+GDNflvIjsAxBXsshCqoViLrrRVvbVIn0zEP2mEYao4dg05VqIZi4Xp8BPfwkTo02uM0mbWTYTCDA4HqIhyFXBxzPAiPYNwdHrnR'
        b'UxVYfA3uwQAMW12HLm8YPXgdF7BPEccJdwzC/D7ogS7sjU623o6NezAbOxKgDW/jAE5i83VHKIFeLIIJA7fkg376ULIVs52z4mxIUS/AvdiDmH/Rbd2msHWu9l7ywdaZ'
        b'Vn7QFWxkSebwzEGYwz4yuisTSG9XUTOz7jBrd8kMK6xDsFQdeyNZdbxybIdqsp078QHWhTpj03GbOCiLwBEFaINZzE+ECazCtgAcIU6fxM4rl7AbHmXBA6wPhKq12Hnx'
        b'LNZB9/41OOoOD3ZDKc2/Csq1j8FYAOTu9KJBzGLTARjLwqET0CjEXmgiOFULLfR3RQz0YxN0XtkoVoVaEjl3rS2wC2djDqgcxBkoiDCCbLdLcDuSmq33gYemEa6Jm1yx'
        b'PBYfYbMn3gk2hJGrTnifBtaK444K0HDCNIjmXgJ3IE9lRyBOGWIHdtK/7vkwz9tpWpA7UG+B9w4c2u64TU8XJ0/SBy2ZO8+aYyMOauliAVbCTGAqfVqlobIFF+mNQZyA'
        b'MRrOuADrbSQO2HgOmq3hoQ7e1Qj3gfLotEOY7Y/1G6EkxFaJpOt9I124Hw+L6yE/ml4fTiLbu2GPEXZGbjl5xnEX1hAt3Ife1DAiuzpsClRbey4jwSETp43Ob4AmX+hc'
        b'exbHaH3qsV+J86SM0lJ1HsFSJShwwfndtJV1MGRHsxym8d2D3NO0AxWWh4kkiq/CpMF6LKb1eYDtGjfE+BCL3LYJYTa9lDEd3raAVn8nKCe6V4OHOLXm+hHa4D4XyN4I'
        b'LdhgqbYXR2l7JqBN7AK9EWFbTaEyRg5KjG/ugp4D6RkxmniHqLET+2lhS5NCT8HCmtPQdASaYAK6ITcMW8yw3nwH3sd5uCeGcWWsXY+zYfJJBMOng4KvHMbmrIB4GCJY'
        b'XQMLJjQJIg8cSfByoCbajKAZc46fprarT0P9fgLuBeHEezkiOx+shnFLemYS+2Ew62yWrtbpm+F73aKxRfvaXm0coZmWEC3nElvc2kd8VeS2yXvbtR1EaRXQiMN7iMqH'
        b'iDLvY2EYVsfDQ5qTCz6AIkXsOYTVmXA33cspFkd2YoEJmROL1/db3YT8C8oBcN+QHXWXYp/2AblEXAzFSRFWXtUPc8HbMKUCpTfcoQFzjNygPBiyMS9SE+5Cv19AkHWE'
        b'zo61OODkpqKnY7Vbfr1NEPFQqzcWBtDuNuCgIRSSUMkOw15b2sYHcAvzxFjtC1U4YYwtvlhMFgpMyWkT5RUbQCdNg8mlvBBrtrJQiMMwfeXqWijbSP2NwH1FLIX+q0QO'
        b'BRnaSsQOU1FYi3PXrfWghpbxNm3POImuGaVoDU+8uxZGsf3MSRwirsvDe5vOwwIBhkXoU94G1akkFHoh306CU5ew6DQsWK1j7r5zfnBvPZHcEJb5Q7WXp/a5KzhD/fUS'
        b'LbSdhRzulq8xyLHGId2dAdvW+EEOrflMMPbE0+r1+8GkKd6Xh4bwbdABU3rpP2WSeECdWmj1Z+HORJE07DlzmE63w5ZzctRsO95OCIP2ZFViy/p9xy2gVyvUCwYOQSnO'
        b'0no9xPr1REmPWHwqTMKYB+SfJW7N24IL7ocOOWKDJ3RFaqlgHlFsD9HUPbi9FZqMLxMJ14sOwcNrAlsrD6y5mGZOGzcFvYSYimGeOKeaWK45/Oz5BJIdnRbYHEeTLqdF'
        b'fyAgciomeh2ELqjD2nMuJBsXzQ1OpZ2/AO0+NMpurMRpE+KPqsNbrK9iqZ4yzC2nWuKRuuNraSwzVzDXUvkmTCdwIrNW4xo0kqzsdfK2zdgcAeO+mdf1xRfcoMQAcqJo'
        b'covUQC/JplzbQ0TDDYqXoAz6QqBGnXZ5wFgdag5gozu0p9EjOchmcxfbSDH1QbamCHMdSYr0rFGEewdw3nAH0cMkzFvjI70r2JWw5ppcTDxmwx3i2Xys1aTF6qbp9eJD'
        b'mDpOG9qpjcXBG2KI4nJx4gh007I/PLeT1NNo8FUjouCOS45YGUpKrN4UBq4QU5Ra0XZ0OlmTmCsi2iTleW7vxX1YZRKH/VlHNTJogLmQTfTcCVN7jE0iw2CK3Vqkpoc1'
        b'OI+5aljoCm3WgUQT0HGNBlCEFSYwQ0QzBBUZ2Km4fhst8gPsdg3eBY+wRcXVjCacTzKynTR38zGYcov2p82cglupwbSljaQT78KDDCy5DA3nFSVY5xjlZsVp9QqvNFI3'
        b'+ekkFyrpmbqDbgansR6aL0Kx6LIhtBCB0woSgUPbmTga5SJZ/dsTPV2xKEEdqySnFDdcwJF1UM+oaxfxdKerNjQ6p/+IKNt13ykmaRM4gPEQx5Jh3BxnhS4bQ6FdERv9'
        b'VYQwwUKDy4ltGqAyDSYFJHC3rcHsPbTADUaZOKoI89AtcTOBJmcY0iV10LSWHi/XwBbFS0ZxRDRNmsSODdam+CjIyh2aT2RirRGUem7cT5rgngqtzSMsUTwOA6GMX8KE'
        b'SecYJmpNwDF8cP4UyQwmgoeBlY6YT7SFZt0j5v46OBYMVaHH4JYLzGthu9vNs7Qw7fszdaE0wDsYBrbj9M0NzqEkOQZpP4Yu0aoMQfPZa0Ksc7WBucDdmRrOZPg3Q8Oh'
        b'CFLMt2iTOw21abXzsVsMi9pYHWSgtY40X7EeVJ73Dgsk5l2wOWEfT2xccxpqrCDXW2+XHvbHw/ARYr/COKjdgbechZgtfxzmI4/CHddYmDrkCw+g8Kids8uNddhItE+i'
        b'sYf6KxBcIiXQiRMK0E5MUKRPzDJJS1WBLdawAKVriUdbtsODLJxNPkQ020CqrhzrDiZjpxPJlOzIE1ch3y2R6L89C+qy1hBVzURew4FoQ2wgIdhBgqLYActOadsikXsl'
        b'drsRNiKC7jHeT2Nopd+6juy/6qZFavHYOpgKICq8B9PX9hLHL+CgM8noQRYhDnf3b2SYLAVKo4x3MkrEKr3DnCTopGFmQ1ss1IVrZ1z2wRbqZZq4qh6qY2k0A4QIckVQ'
        b'ns6SONZm0vSaSYMOkeJMPQ0dVtiG3YZ+6gGkK/ri9LFDgnc8aH978cE5aA2lIY4eIjuxGwvt4DYyJl/AuiBqouBCzGWmhTDn0lqcSiLhMol521zPqOD4+j2uJzbIX0yv'
        b'JKq+DG0JRNbstt0lBGGO94WXsJwQhOMBc7i3G8Yvq+60U0whBNvgehKrj9JEoN2JtneB+p1KoSWaZeLn9BbIt8HcPWHQSh0Xw3hSpqPaRi9YwLFwvEvPjELecRLZ9Tc3'
        b'Qbb5Sdru+3IHSAzWwZyZ7WEcOk8Q7Q7OSQhelpMWGyQdPYMk1HJvWmKtDhFt4dHz0O6Jdf5HSLlWSo5AY5AZoY5ueGDPrqMkPNIODzWJt1uhQwsH3KF8z1Ws1vDZFH2J'
        b'JF2OIrFHW6ZKCIxvtz/mbeioThQ2DHc0LDfI0aK1qujY4fSmHUpiV7y1mdYxeztRfY/2etLx5dTmyDnMPQ+1TkBy6RCpQRJNhBFwPgRbsM0hmcTVHegjRdJNUH+ctkl4'
        b'3PIklGxPIDXdDMN+mHsGO8/ZQ7G3hQ+tXC4UOcet93M7wVBM8fkb0BtuirciIFs30xjrSV1VncXZFCKduhM4FIqFlruhXkR0dtcbC5yIuhZJpo9EnyejpJLkdtFaQ1rl'
        b'6VCsccACuJt4gFa/3xryDxHRdGPVnmC9KFs7v3DoDsX7iedIKLc7aKpst9mvt9bGlCT6tBoW6R7z3UmKcHE7tARRq9XqRFmPLkGx/0likflz0L4DevUicSKBOmymabZe'
        b'IEboOStZQ7KnGkasYEyVFrMY66OhaBNMnk+6YHAYBuPpoRFojCLp0CiOo1FlBxC9T9tAhSMs7CRVO4e3b+rhI0E8NptjnQDL099iIKI9iF4jqsxJ4IhygRi/Yq/5VRyS'
        b'YP81JcI9ubqZtIY5OzYQxp022q2DNVoEJk/5Z7hD5c1N2zPTIT/M8HiImj/p7y72A7n7SPTXkSCh1xwZbrqupQ7DV2lv5/HuycOqpCtnYVEzFHuwMY50bZ88ZqfjnUAJ'
        b'LGQm0FfN4ecJzIxy+AGa44h6F2KJAabCDTEvZRP2mBBhdBL7DAUmYNV1YxIPLQzwxtAACi/YXzJUpTeqSHTU0cxKfIIJ7A1mBWSdirm6Rc0XCbN2Yc8Wktx95w5d1aD1'
        b'LQHGu5VwPyHpkA7MaqYRm+SksGzI0742yttwPNwXb0FdAD0yC7cVcVBdgoUn2JWh9HFBEjRpkqFyG9qu4mQI0er4LjVzT5JPjbFarnHXDpHp1LmBJSOStClZbyJHa3ln'
        b'N5kwlQZ6UJtgvMmF+HV4A865keAqI+tkmvTxfAKLvsfq5O3Yu5Xs20G8nQVNJpYk/wiq9pGg67Vxk9hc3Xwuijg9h9ghN504oUkFqvdg+UUbbPbeTswwpaudGk7y7yEO'
        b'nsHB88Q33ZuJBlv2E2C5ZwMFeD8pAbrSyAgvJGPZYLceKxxzmIT8lMNWGnZlDJQRYpDH/iBSlYVEqjWHLuJM0FrMk4NaHJNQv61Ebk2CrVcck86k6h+n/Z3YYkb80gpV'
        b'kWnQcugqFG/FIvlzWBIHjQfp2UmYJtBZj0UnSUuUECxp0fPWgLueO276EYkO42hGcDzBxPqAQy77mWU2ZAc9Tilm5+AekVSFD0xkxupFkQRq1CQKn7bErhPX3bDG1Ywo'
        b'YtRgC+bs8o4LIvHUAj2mfE4hFKVCAcsOqvGQFwh3CRhj4CwXZKTsDve8IN+YHbNzeUM0wxkuHOWaZaYXCYsBc5FAeERAIGM0nvucaKrpmBfcC7BUEAgP0xf7DfhoElrj'
        b'44yODmGJUCD0FGBzIFZzXznSWvezrKYRC/rGXUDAsg1z013FAoGnwjpaqBosI8ZoOqJG6z52Q2XTWWWoc/DXDNMlzVRlReTQSSt1h0H2HXjbw9UH8uMO6ZuStLmHPWsz'
        b'SD11QJuHltNZEuCV0BKOFYRXiIlZRcBhsl7GsOqqVbozDOozlJcFPZIwLFCFjpQwYpsaGjFknzqBd3xpL+l7YsY8F/q1G/oEJGILgnQIwjXvoi1rtT6zjSgvZwMZBBNm'
        b'wdRuhcCP+syT0EKNkQquob0mGyf2OuRbkXqtCoTKHWQrTBJFnCH8UrWDpNwIVNuRoZSXFuIDj7yI3LtZpS9a9kkWOp1Ltlmhnel1KLAh8DZPUmKcFEI7jG8mMNwPjQck'
        b'By6LsUJRookN7hdhwBbvp5hvwrkLOHTGYw0MKF5Pl/ikhJAQrYJuZeY3gAajtZhDCztEwiiHBGTvuTPUVimtZ12wXhwx7RwNoXIfTbXXcZ3KKTVsiwjlLK8mMeZasztW'
        b'aVVGkETpojWUinE82MzPGvNOs7IwDji+gxinz8YcWCWRAah0IDxUQfPJTjFIl6NtrkylOXTDwrGzBCZroNgM2hRxOBYr3eHOYRK8pKBLyXBZUFyDJaGbI0yd1+OwEtwJ'
        b'hTspxCgLphrpOBCRkoK99FOdpU7DLbI9eZrMqRESxVU2OOnsdl07KlKF5jBjog6zGnjXnXjr1n4c2eVB7D0A+cicO0WaXKJmzjpoCSFRAHWH3c/4nk05dcaAMFEh6fI5'
        b'gwNYm7LLhuh48rKYREQPDFvqw2J6DA7tJ2ug0kwXmwyYJCedV7D7JjHqzD4CjEXMHWXqG0U6Fe7tguY0oqkCuHcWChJIjXfD4DFi4RGvmzASQhZfG+3qiKc954F5KCZN'
        b'c/dsNFlTPVCx32D9DXOCntO+zJDAqih4gJ276Y9FXDDWhzpJqkWaIWGuoUN4/4I65qjjQyG0Xbh5No7s3T7SYhLojHzSN8MCvg4ZH9G8jMP6CuuuYEck8UZOOEnmieNn'
        b'sdhTT9+JDJdFqE+h1cxX1ZM/E+LtT0Kg0mYdUU4djK3F3j2GXpsPwlQmmQMFpw39LCOcFEmp3T9xknPSTPptok6aoMaWFuShCivknkDypZN0ykIMCRmYNYUxKDloTpzR'
        b'iy0J9I+Ky3uhiZQayfdKRqldMGEGo7sTCeu32eNk5Fla5HyfkwYMbCIJ6p5TQsJ8D4mnc4yIfSbcSMe1yRlhnzmJ3ins0j0J/VtIrpZD85EUb4LZbdEkuZsJgOYeYSJ2'
        b'AnKy4gnjrz9CgKFrrSbzbnljX4aOswoMXjpP0riU9wWkRhATVF7cTkMjpYYdN0gYzBkRL7SSmQt9PhcEcVhwNJ6kTsuFo6yPKWyR0Cir00gV59IbLB6nNSISxuKP78dp'
        b'Ay14tPUMEUODHvY4WbFVMcMBAwnOxRLdMKg/SObDwxRcuCB/UAsb1+/Bar8kkmqlutipw8R1JsGpbFhMJsgzfRgGtP1MDttsIwXcjneClbDDLZEWvtlkZ/pG01j94246'
        b'2tiuezPdXh3yj4p8ieYHiQCLoPcGyYKO9JPuUHKWJO0tc7ivJyHOfEh8MZt16hLpywQoF+ME/XuYsN5c2GWSty2O109jT7AlCaYmHDKFB0cvwMim7R4kF2rYJrPkeRJt'
        b'pBZgRJumsYCLN457U6Pd+6D60ho3P+p7fj2txwNnuO9EQrggRH7L4bST29N/JuKuf24kBdUagCUyA/cU9V4G9Xs3MQM32F9VCDM6WOgLYwqWMHJWQR8GkKTg9D6ihDG7'
        b'k7gAxVaxdkSjVZzPZHCLJQky5qlr1N593gLySLJRL/kwTjYCPrriZ2lKGzaEDw85wYARNGoaraPlL4XpSOLXrsMHBTCwloTL4HZotMPszSTwJmH4NN4NgmbrYJI9BR7Q'
        b'EhlMamHsJEMpndgRnLJTXhxzEOt2Yc9VLLKCya2BmJuwG7rjjpJq6KY597E6dK4kcmDOG4stgkl5NJsRQ9+23HwqBnv2rzmTgo98idzqSH3k7dVTgrtxCTBO8quNehj3'
        b'VSROWEzyI8u9iiimFLozaNqksNZh7y64k04qpd43juiJjJd6C/UEyFMxtscRu1hs8NS/BA9hIB2b7WDeKQXrafUqcPzkRlgMFBzA2+pKuCimUeb7rIE5eeYd6bKD3mh9'
        b'd6hzWb/OjmyvYpoSjjiQKH9IRDFGXECKHxeSyQId1qVlbwyPYJwTFWNCYrVMdM4pOlkNZs5ib5yfb2zUBcKqkxo0hCZSuUMqOOkFJRFQf9LcAMjOuIVlcWphOBwIFbpH'
        b'Qs9nYpunz4Y9WLUbJzbEnMNyGxHDriSH8siSvosPva9ep9mXhGuR+urARxvltkOdrj/mR5x2u3DUx5U4vNQR76QeiMS5LSSTRmlLS8hAVAghATGsGmzECRkmt2tpIRsi'
        b'9sIEzmwxJc5twK5rxHDlMG5CRlCJtiJpyMGk02tYjf5IXDieTHtThgQQKpVhVsfBiqRa2zXdm5o7ibsaSeQ8ssDCEGjbf4mASkNCujMhGuH+7SvomuzbWbHIAPux6ohm'
        b'CnTrKcTtJJnbSlOZIIlYt0foGejBDKgIvB+BU+rEVjM08w4LBw2sNDqzQY4IvInUdylB+OEMWus7ewOVg2DUFptOE2U3keCeV2UmOQwZBbHLzGk25fqYF+DKkI8uNTYS'
        b'sgl6rHHExQwJznhuoPUp2QJ3rTYRd945yJqF5jW0OM2ppHf6JDBx2ojovEnkv3c9dK21g+xwKNpFCNiR5OGmINP1JCmqYzBXGSYkKTdJdeXCdLAt6ZUpCRPkJYppx21g'
        b'QG0/LXIFNhqG0DLN6WBn9BocVTLJcDqYbACt+2HM+zqRVQ/pvm5sXIuzaZ44oENgp4LU6IMY0gcZKs4ptItt1Ej1lgNp0O0gtwdHDm+D/kMq2JKGw1pR5w2hV1srGWrW'
        b'YKlXNDWUA7UWitY+tKOENWhp7ssZ+yQd2e8fh6NbSDYMEBO1hG7BRVeSXvXQ6uHkKCDOKCa2JBBOsqsaZlWjsGAf6WcWseMM4+uUhSQK7oWcI7nXQ9tyn1rN015zitR4'
        b'GXQpwe0YyLfDAUtSAIU3LkP1gXMs5hw6BTB1wWE9CZR5yI/dSYzWZwgdlsTljcQT42RZt4Qqr92HDwygPvCAV5Ib6dB+wsgjcvTKLZgy1rMju6MLep1gUN6IeKkFFrev'
        b'WUs7VWaGldexki1N0RWYFCftcKBPqw5C585TOLef5RZrbzu4DdsOQIPkNNFOIdalkGJauHoWx/YeDILc+DSSi7VWAlvoDbuqFx5Oqx4fgw+gLBzGkwk/VxGCK6PVmrAn'
        b'wZq3zY7swjksSLH3inIkMVCIxZmWtLiTakKivkE1ho1pIxsjU69mwX0/+mcXNHmTlX4XxpLccfQUpxan8cHBs4eg3oRUJtm/bo447UkIbkw1cg9BuYZgdleGYjiBtewt'
        b'8jCRziIkfA3jGB+xIhyMkRZYrmkvgZI7MGuH04YEdU9jjUqsMwxtw2bnXVAlJuXWrs6ecNSKJYPxYWa0uzuhgVzPIDtjzM9IJHi9gH1OtPeTcFcZH9oqxpPKGRJiRwDO'
        b'b88im6gF7uxw1VQNwLpI7mhthDn6b2ZCLcwzj1YXzPnTBIlFepmziHBuD/S662PjNf+dZ3bR1O7g4EHMuUnG14wRKcbCc3A3iLDWjKVCTKK1IYy7qxDfD9ODZda0qvnx'
        b'RP8Lmth+HvIIDIyTWinfg5XrFWmOPcqWOHo9huBffvhVuO1IGrkc2sU4aaiMzScNXQ2JWIZN5LU24H3ntYeDoFLjiBLJzHnMdiMsM8Qk2j4cFZD2voMVuzUkxyHvrJfJ'
        b'gbQ4FVzQOpWxk8Q7wfJDl45DRRLWWAeQVc1Q6JRdzHVWN2knjGvbexEHdxjAvArMnr4Wb4b920lu3cNmyLuA81dVMN8lgLgij8ySfpI6VWSybKblrt+IrWoq4igDLDkT'
        b'F3s+xAabvDSELvr03ghUKUC1tgFxWw3ci1PzMN+FsxuZ85PUdjY8XAf32Pldn9EGFjwSftiRsHvbXlqNDhjdYJkAVd5biSfKyfJJTYfGvbQL+R44c1CV0PsDQgUtLhkG'
        b'2Kl2Q55mUO0KTbrK14ndqulfVbBonhB6Ddo2k5zO1TngBzOG0KK131HtCt7yxDyjEEXsC4TqGGiDISKjcv9g5jDFvnTm8aKdf0BScpw0RC52W2HhjZDNpKIJAJ2kZ1t9'
        b'aTK3TuFshhWhMughZqkhLV2oGhyefobY8S4wTUJgtNuW5raYBbUbsVpCmHsmmWUYXTEkshrKwoKbUESCnFDHrdMkm27Hpf+ScJIOO5Bd4oIjzDNVcYoUMEmvuMPG/prb'
        b'sJI44NS2TPq6ZW10hLIhdq89sI02dxFHo2FY0T2U+pgleNQjssXZ9bCIffvjVKFsKwHcPGxPA3YEnHPmIFTLQZ0hSfKHV7DRCzrF9GsvzEtI3fTfIMFYQfxUS7tRpbIR'
        b'uzxJkA7R4pdi9XVchAcH9bDIFh5YYuc2HyyJZ8dcHsxVFXmclidvB4mUIjU5HJSsI9KfvmZMXD63xy+RKK5b15qGV71bH+u2bjLF5h0uBBeIPZyJHBb0YnBGDZscNmOP'
        b'OhmOeecg1xnnjsCQ8lWSLjWEfe6QZO4SEM3PK0CrkTvUq5KJ0LNbEzqc9kCjDSGFPMPANdi/da+CAhaecGZVWW45Hyej+IEVwasCO5zQTMKZXWpe1tBpgzVO9kdoUaag'
        b'SY4Yv5tEfX5GqLEWS+aaI1kwBznGROwjQgJlNy/vIXqr8Yc8VY4s5kJIei9e3EESoQULEmnVepkkmNlNwKMmKga6DhBBMx98DRYb4JQt2TVV0VCoAJ0xxtAvB2OH7HGW'
        b'meeYfYIE2LT3FVLoj2wUCFV3QakJ5lrQwozpQ2cW1GsTXRZuYcfJ8tcVbKMDqeXagxpYR9hB4QrDP7m6+xLI3CM0f4uERBX06mLjMYOrLKwigFauCeYvXN4Og5bw0BW6'
        b'TOWhcTNhq+bTMHCRzJ0R6LIMIfRDOtvWPnEvzHvuTMbO7dDgCb3mu11wSp4USr3HZrJpW3FyD6m3AcYjjQE6x2wIXQ9Z4WLQNpJt9f6hGiFZgeuCiXAKMXufN/XRsNVx'
        b'05EsAWHLwotEBF2RpiK+utIdlyupOLtUCweGT5pBO8FbznV1D/v3iLHpcSE3+sk2FXNFb6z9cMiLoHINcysdEGDdDlzkvFokTEa2eolZDoJAuFtAi1UH/HUGWlDijCXp'
        b'hIqK5ARCZ3oHSg9xjUFxJkx6rcMFmY+syZgGyL7ahrlrvDZBNatMa03fMADF+cJs993EkmAY8qZX7ASEVLLT0/lrnBrXeV2g7VzyqoU7SC9awAFsukS4qzHFlN7xE9Da'
        b'Yjv3zUUVWpgSdseCD+9YqyJdzycCZqdirRcxxZIrjgkxUyGft3dfS+KF90M9qTVzARaaXuI+lvcWY8nxTJknzibKVOjKXcDDZa6dUBKzOMwDkQqh8eYxBwSmYu7jsVju'
        b'ijPDA8JQb3tdB74SUMxG7sOrnhqh3vEbMgUswsyVa41LdYv95OiPxKnjJKsMc+Szak75rXfSy4u+8os9r4QmCY/+ueGXmX/W0qkWmOq4u5XrbKt9r0/pwuTJjxPa/iL+'
        b'fMLO4UJjQ8Grf8n4s93fmu0C/vngH9++Y/N+2lsKpes/+kfe3zRsuk6fnT9k8VOlq02phe0j/1AZfMfA0+x2gErVPr+IX5X9158GQ43j1h8uS01vtq39W3K5yo7w2XcH'
        b'6v9ge/ndil9f7vhuUPnRgz3vmEV/OpW+4dc2Vze8Z3N9Q9VGu+8097v67HnP9v2ywBN2r5/td+40TP8o+fUMV/3+n3TleJaZ+IW1HtvaOD/5q9t6H8l9dPuzH786PvqK'
        b'/B2Ft/qqXWzc3N+v9vR94yeiGCfzmd/s/G1vv4aX545+xU/ULnWvv3yn4SeK7ve6ugydClJDz45+GB+z033slEK36x9e/V33hW9Jqq9FSYIu/9b47pGd8+7pb/Veup8/'
        b'9a5F9VS3i333j6NTrb9l5/WTFovv2H5n4brj/I+cJ7+99TtnNt1Z/7druTZndeo9fvdHl00PvvjnaP9nXb+M8X6nQpghzvi44Xdnth3d/63G9zM+PvNxkOmV6u9sCvjg'
        b'0ze+P/WdcC1nI8mrtr8ovDDT8dd7nq/+4PC5Cy/X9v58X2a1X7ihXbXdzvCz3lqD7fhl11/VDV82eevEXfV//OOSR/bfHb73d0VJ95b/aoqPfaQdYbjz8OjPN1ba/lnt'
        b'Xz73X3/tuqFuw28+jPo/J9/+8FOPRe8fN/bZ5MX+siDuYdeF15rtcoN/5nNjX8G1lOCH0Y7bzN95X97ijcRPfx7131OD2rHvXTf/5YXfDU3clvwu+GfXbt34m83v4nb9'
        b'quMNu73VGQeLJK9FbzN3MNqeu2Y4pTYosTYzb99whLj5TbC9vPHom69s/Cw529nowy8+f/lh+XtXvbI+T0/89e3FtzKntBZsPq+42Xai555Dqse/lK+PYGzel+8VHc6v'
        b'X/Pfb+l+qTdm9s+f+/1z1z9d218PnP7c4NFbJ970jjdV4ULOCY017CU0XcqS1ZgUKSfr8T4X0i6x1lIlsZ399CUL0CHHZT9B5RmYWH5ZAlRsX5HQ1oKt/KUKpWfgvqol'
        b'LKaoK6uTki/RTElXI818TywwyqD2Sly4tKw4KNJQXXrkCn0/K7qSrK4gMDwiJp1xNzKN3WZIMJUwduplNSccSU7He6y8WqmmkroKjmtelheYasiREq1N5OJwYeEUlNGj'
        b'suc8sWTpUSijHrjmfeQUYI7w7zyXnsaOsaFGVdYglm5Wwj7Rrs04kMbCjTFvAw6mQplSMg0zlZRdkS/OrNIozijAI1Iz3KAlB0kPLFWYgzJNwmX1T5ZhgYo9T1/cZvP/'
        b'Nuj0//kfpkacnP3/yx/8LdohIfGJYZEhIVwU9g9ZMK25SCQS7hVu/FIkYrloOiIlsZxQSawgoh+xhryOjo6y1kYtRS0FHRU9XTmRnofhFnr+psCGlSk5wKKyxXIi9vvG'
        b'm9SW0HD7sf9b3LXHRlGE8X3dq0dLW0pFWnmKtnd9QGuxKhCr0NJer+URKE/Xu+uWW7nebXf3aHkTQJDWUlCoPEx5CCgFasVWMEXUGcUYjZoQo4zGaFAk6h9qokbwNd9s'
        b'W4z/aUzI5n53u7M7N/PNtPN9l/n9PrgmC/wUa892SODvhfeawSv2EQtHliSLSWJqssDnrOfGC/x0q2S84BGy6ctLcQN3UmJ3CznsChwbuGMS7LO+bh9UFXcyEZUbL33e'
        b'4K5nUf8cOn5j73fBzZ8UN20y8pYx2C5sMBEoQxpAkOc+0v6epAp4AnNwO08DjDbqF22rrqSeDWznanNwSbeKt0n4UXXj5TabkcFzXH7PrqLWsiqxJHnGiTvL3v/48sSk'
        b'EZt3zBQ2u8ZlbrJ1j37h0Cfud7zuFe3nv02/Upq5+cEPLg7pfPP60ZpDqcPLrx0ZSpqP/jSh+LM3FvedNl+S5vXGi4vMl+uvNpRdbD//46UafnX7b54v0bv3FsyZ1OcJ'
        b'PHvJf09BpCG4p+H9iV93HfN+0omPJPxx/au3u75pCJ9+3jgglpy45Plo7RhHZ+3Yq3uvDNvajn8J/5D7XJ4xu69m3+L83vyMPy82XWtcVbBrfNGVTyMz9MMrzn64ZI9u'
        b'f2C06NzVPXFza8oF7fNg89LvXt/UtlYqvv+xBzO/GJFSpTWPcL2nbXcvGffm8EVnLyRGd44ty2i8evC1qaO+fyxvVexFT9cT8dd+vrDusPa72/vW0vZLxdmjGXVqbkYa'
        b'cP2rqy167Xnc4eDc6LQAYQc+wGjNt+BDhb7qXAzpN6urc4Vp07kUfE6ksfPxMlbHgnHDrNEAxn8SjXRb2WCkiqNAmtViNm8JNOHt6BhIofodnF0SnDQmeNXSu+tZOAm3'
        b'5Os69U7nArP8maBFC9vvR0978fYsYAg/znOuPHwmWUD7JgeZ4tWataWZswZ0u6QqHnUnjGLtrcCd6ATss6fPoVfyWHkSbhar8CmXlcHopRwtXm3Ryxm5HL+cwhbJyTQM'
        b'fsqq0l+OW7PLJRqcnaWx8pMiDQb3P8AoLDRmxkd8FTlVRYU856Ax2jl0SrDjzmK2slMLbjR9BYX0cSbWZaOL315u6FjxPrw/bC2C50pQD9xR7mc3pDXQ1nWJk2ai48xU'
        b'09EW1OHQcAskrWuj7vRsHvWlz2dllTSM7EZHQJKs1Z/DcdIkGtSEfYxQX4H3Avc8y5uLITGTVM/TQLOHegnQs8pG3O4FxbpK+E4/7boEsSSXsVZCG6eiJyxS/+5StNEH'
        b'zaIGgI2xc3jOnS3QIP/Fcazpt+CtC43Bcu9cnksoF2ic+gpqYU6LD53R3Pj0UNxroG34jIZ7Gqg/kshxmagja7wEjJw9bMbg3ttRL6MjeaE61JXN0Vm3T8CHUR+dFUwf'
        b'oG0Rbrlr9kAi137luc4VpgcKjydN9aFTWXSIQUAMtBTPU0PTrqHW/KrcbDtXNsOxBm1Hbayu9fTJY+711BrduAe0uXeC7O/uRksm8MxKQ0etsJGasd1ta3gaox/MYYyk'
        b'9FGwZ4fRjPI9DZajNmEpNzIu0VHammaZrbUQbaJWbwZxw0qBc93hRDsE1EK9qW3MEbwVbyrxVuTm+HPzpqCdPDdkuJgwNZUZIn34GB8dF18ehnRCbdl2fLKIG1Yo4g68'
        b'Gx21lPT22Jq8M3M8QPF8PCCCIMEOyKr1tJNxrXC3DXd4K+AnUxqp+UBXYW/KQJqhrJv/j/1/Wh7Sb4I3ciNXrwbrUJKTEeKd7Ehj6mjOfjIm0L7AxQBFstR+jTJ6pxj9'
        b'9xSygWOixapijoKHiBElqj9CVzRiM+NaRCFSRDVMItWqIYoxTYkS0TB1YguuNBWDSMFYLEJENWoSWx11qOibHoguU4hNjWpxk4ihsE7EmF5L7HVqxFToSX1AI+IqVSO2'
        b'gBFSVSKGlSZ6C60+QTXUqGEGoiGF2LV4MKKGyJAZFp3RH1hOHx6i6YppqnUr5ab6CHFWxkLLS1XaSFewcLISBQUqkqgaMdlU6xVaUb1GpNJZ00tJohbQDUWmRcDpJin1'
        b'sdp77rZyc8i16jLVJI5AKKRopkESWcdkM0b9w+gyIi7wVxK3EVbrTFnR9ZhOEuPRUDigRpVaWWkKEZcsGwo1lSyTpGhMjgXr4kaIJUsiroET2p14FCSobrhglr2zdBAH'
        b'1hsAogArAFYCmADLAGIASwGWAMQBggALAWoBwIvVwwABgIcAHgHQAOYDLGA6dABAPNRXAaxmJDqARYxoCwAN0+sBlgM8DNAIsBightUMPLsm+LQGoG6QNQgTyTXoTv26'
        b'6G/uFCu75qyjM0UJhfNIsiz3f+73w6+N7D8fowVCy0F/DOisUKbUVmU7Gf+POGQ5EInIsjVlGUMQmHDEbuUy1S/DlXUDfu8/Uh8T5xQ67vGIMg3Ic4x4J4F/8N//dOal'
        b'MXnBvwDzXa8i'
    ))))
