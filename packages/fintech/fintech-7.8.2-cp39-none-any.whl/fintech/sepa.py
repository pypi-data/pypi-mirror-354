
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
        b'eJy0fQlAVMf5+Ly3J9eCgIiKul6RhWVBPGK8Ih4ILJccaoi6u/AWWF1Z3MMreEQxCyJiFO/beN+K9xHTmTRXkzS9fk237a9Nz6Tpr03PNLZN/t/Me7ssp5r2L/J4M2/e'
        b'zDcz33zXfPO9X6JO/2TwOw1+XZPhIqAyVIXKOIET+HpUxltlR+SC7CjnHCHIrYqNaDlyGZ7nrUpBsZHbwFlVVn4jxyFBWYxCKnWqh4tDi2cVZmiXOgSP3ap1VGrd1VZt'
        b'4Sp3taNGm2mrcVsrqrW1loolliqrITS0pNrm8pcVrJW2GqtLW+mpqXDbHDUuraVG0FbYLS4X5Lod2hUO5xLtCpu7WkubMIRWjArqQxL8JsJvGO3HS3DxIi/n5b0yr9yr'
        b'8Cq9Kq/aG+IN9YZ5w70RXo030hvl7eON9sZ4Y719vXHeft54b3/vAO9Ab4J3kHewd4hX6x3qHeYd7h3hHel9yjuqMpGNiHpNYoN8I1qjWx1dl7gRzUN1uo2IQ2sT1+qK'
        b'g+7TYBzZiMjyK4KHmoPfdPiNoWDK2XAXI11kvl0N90uWyhDNS8t8pXalUIo8IyExFR95mjSRxoLcOaSBNBfoSHN2aWEKacanlWjULDl5QDZH6WSeBCgL9+ercAt52Zit'
        b'z04hjWRLngJpyGZZvibNEwcF8CmyER+kT/GtyQokl3P4sHauZzA8WombCpLZK3nZpFmXLUfRZIcMX6jEdxbiszpebOA22bDSmD4GShjJ1oJsBYocKhPWTCIn8U7PANpA'
        b'80JSTwtk54nPNeSibGLR6IxqqGEgFBiML+P1LvoUWiJbOBSK71qyeXw5bqBnBG1hY85QcqRfGLkaSa67cCO5WUuuLcNNkREIJQyXq/A2skHHeeIZxHsSSFNuDtkyGb8s'
        b'QzLyKof3kx0z4DHFDNI0dLgRX0iEgdhsJFtwYwGFCDdryc3U/BSdEs2epaqbXyJVhu/aFpE2gCm3QEEukhakqOPI8QETpMfkUj45mpyTos9LMXAoPL26ryyUvEIOwWM6'
        b'Ltg7FB9OztInkcZc2qkw3ABzsY0nF9XzK7hOS22Mf/4PUDTtiKToP0VTb6JX503yJnv13hSvwZvqTfOO9qZXjpGQl2sIAeTlAXk5hrw8Q1huLV8cdN8T8lLgB3ZBXpOI'
        b'vP9XqUThCJnjhptztSlFiGUuS2cYHf8xMuc297GImWMGhqAohOZ/uticO2jkRDGzKFeB4G/hL6abc+dmu9AZZA+F7IuJ8fK/RqNpn8Ws4n4cfyX/vbg/cfYQePC0Zi93'
        b'WYW0abqxo3/iXDl/JWLZ6bK/RLZGcomfRY3r/+V89/w45EOeNHgwnpzCL8M6aiIX8N3UOYmJZHNqFmAGPlOSmJNHWvSG7JScPA7VRIZMwZfJfs9MeKlsNt7kcjuXL/O4'
        b'yE1ymVwjV8kNcoVcJ22R6vBQTUhEGHkFt8BPA96SnjY2ffzocWPwTXxZjvCrz4eQC+RitccIFc2HV+8Zc3PyYfmdy84zkhZYy1vIZlgFjaSZNKUm6pMMupRkfAmfxueL'
        b'oIqrZDd5mewk28gusoO0zkOoX1pEdAWp74BOdBJU8NvPT70Z1ZNVyqTp5htgUtfIYLp5Nt0yNsX8Wllx0L003fXd0Sp5l+mW5zspHtgqN/wBuZ6Bu1nHYic2Gy0LXvvg'
        b'G5e3Xdk1VPHWWcv8125FvfX8a9e2Hd11dKONc6kqIsj0k/q4bVlpsqoBKMceMYDbrlO46dJyasnWRVNgYjbDqGwBfHmGw1fwi8vdFNXwK2Q3PpRsgOFq1JPjCg4p8VY+'
        b'hRwgh9194XnsJHwrOSUxK6VwBA+P9vEpeFt/Vm0maZqaDGQydzS+j7cpkLKMg/m44GKv4YMrFpKmrEJ8Hl9AiF/DZQI503E+PlGnkzlpX4MuPFwe9p1c6XSsttZoK0Um'
        b'ZnBZay1TfTKPTaDPXUo6YjNCuWjOqfS/pJP7QmosS60uYHhWn9zirHL5VCaT01NjMvnCTKYKu9VS46k1mXR8e3NwT9eDk06rU0EvtD6KjS5KadCrUbyS4zklu/L/4nmY'
        b'Jw59SVOeWHj+PDlflEyaoyJyOcTjPdwMfHttZgXfDdKweZ1KkYZnaCOvlAfQRvbYaFPdHZUI7YI2MfkMujWkCb/sgrVe4ELkDOVHOyLYAwVpnWOEfHKLnOB0iHgrySb2'
        b'QMDHJ5K2AgUykyOcAuHruC3a04/Rd7KfHCdN8AifINe4WYjsxJvEQUgnL+I9YcD8ciCnDxD3ceS2pw88SHk+Jhmy8a14bg4i+7OrWG6dbUiyQYmy8GnueURODZvpocAr'
        b'Ry4iO+YAshzBO9FqlIcPDvVEQ340bsOHi9aRHTAxeqQnjX11IeyFVFz/VB9yZRIMNtkE/8me59kLaxeTs279CzT7BPzHh+0MyEq8i5yKIevxXaiI7Ib/udEeip3k8kz8'
        b'ygp8hbAHN+E/vpvIWnjq2Xh8ZgK+C2NMDsL/JLJHfGMb1NVQsYawJ/fhP9k5knF8oC7r8TV8Yia+GwmpI/Cfx7cYWGTDbDcQoOvkFZ7KTWFDxMHAu/Eroc9nFkNNo9Ao'
        b'fEbDCg8nL09S4Y1kB2BOGkrDt1eKk3DAYgH6tFtF+3UZ4RZkwhfIek9/eDZvJD5H2lykbTlgIjmND5Bj3AhocC8jIB3oGB9MaqgcUYXq0MKoNVwd1wASp1Nex73ML5NT'
        b'psRWFruc4X28Ic3HVZzh2hcqWzK+0Ml2m8td4VhaO3U+pP9C2/BQ+ggCgd4oCS+4GeSALNKK24AINxbkky06fEOWno6bjHg7AD5ueBg5j/A9cicMOEJruW3Ed4oVLi/U'
        b'Mqfk2yObJ2lwWtTMFaO4cvXhDW21G1rdR+tr5OO0J64mb/vwJy/iV3Ve5ZVPKn+T/Zfwb7/xQdhO8zf3jXn/tnnGm7/+oWL0zOx0/Ndl7+49d3z4hwOUuqarB8dvuTXk'
        b'3swRn/zq6rPDq6edXDQldMpzfZMvXhhbU/7vl885v/XTF/684s/f/dc/b/7tFzXPnmweNe/5PUBA6RSHFJBLyQYd2awnL4KUpMTn+TG2EDedgtljyNU67AXBhTRk5+Yr'
        b'QDC5wpODIQr2lGzPpzxRD9JcCn5xqBIpF/HDQT676dbC0yzVMMovU8kmvJlsBlmNNOLzOQoUM1ZGtheQNjcTfC7DtO4PJt5462hKv++SfV0oqU7embR2mrYwa02FQ7Ca'
        b'KG1lVJXCgbLknJxTww//pVKmhvtQuNfwUZyGC+fiOWefIHrLuXyhNQ6TC7SGaqvLSUUCJyVGXWHhnRTZnNEBMkuryQ6Q2dvRPZPZobTjzc+R+8GYRPaMTMmSowFku3wF'
        b'2YH3PoLkMj7dgeT+1zl1iCiYRWdFoxF1dDmbEz4YHy+KW+PDs9E27adyZDbnmCaNQpks95OcKKQVIjhUaw4fl86LRU+OCEWxJTBEUWa9rVyGGDlYvTBvTJocN2TBSOxA'
        b'5TJ81PbLA39UuJ6DZyMWvPSp+Xfm6spcy7uVibs+Xn9579XnNofcFYr2bOw/MT4uTS98LHxs1qfLrvafFN8vPW5/hlA0vyi+bO+IDP1LsXOjjAeo2HBbKfDPjy8GgUGJ'
        b'hn/Yd8NftDqe4XstOYCPZZP7jO9LXH+d1j2IYrQXhPIDyYZs0lKjT9IZQK4jjSB/auWLQpN03ONhYZ+KamvFElOF0yrY3A6nSeLwGjrSZfEMFzVwBcyLDcI8WYVN8Kkq'
        b'HJ4at3NV74hHKbYzLoB4jGsHEO9UL4inp4jnHUYOAtZlgQqFtxYYcvLwPhBNQTpqTIWF2gJsfwreryQnyc7aLqpHAAeZrMgBFrbLihzDwMdTDbpgIO3IyC4YOExSDWwx'
        b'aMTKzwAY8+TPYpMlZFuf2Qdpxw6lyJbrmTcHlbDcv2lAD8h9V4Gmme0lGRIKxi8HyrJyFUBvtg8IyRUzfRMiULx9A48KzfoHT0t43cLFosRc0C6mmesOrEuQdIu1g9AE'
        b'/SIllKz7KH2hmLlWrUXTsn5Cm58cOy1HzBxSMRJlrfyOEl6f/pGpTMy8wutQYVaWCtYKr3gmQ8y8GKJH8xNjZVDndGHKMjFz7DAVCp9wBCGtWZ+TKNW5Zk4Yis0V2Pqx'
        b'hEg6UNSyUSi3sIyDksPiV4eJmftQEiqp209LlvezrxIzn5kWj9Imr5NB63Xj0yWQDqeDClWXz0Gm/bbRKWauyI1ECeqPeJRmzh0uTBczr6oHorHaM3KoM+FIRT8x81rO'
        b'YDR55nollEx4a3iKmPmXhOFoZuLvAZ3N078fkyVmPgtChH7CPtqjBdcTHGLm7OhUtCCqiTY0bFziYjFzRuJYVD1znByGzrkzfrbUep90JEx7BhDCnO6rMYiZW1ekIXMd'
        b'iAy15mGXB9mQbgQTh/CrQ8hVqhuTO2T7aDSaPMBHPTCTaF4F3jEGqlCb0kGw2zKKSSlxUavGAKi4cfUYNIbsw5s9kfTVg2WxY0BoMrjGorFlOYxU4eZqvGsMIN84cmcc'
        b'GpdDtrNa8/CJNWMAbQVyZDwaP7SaZY4jx/C2MbBSRkY9jZ5ens0qKMP78ZExgHwp5PoENMGKLzJ4QXfcmI/baAvn8LFn0DOpuJWBtmSICbcBvBy+MBFNzCbXRWkLRIqR'
        b'dGkMg6mZTrbjA6zFcDne54KOmEj9DDTDsEgse24BaaUqBXkxeiaa2Q9fFls8gi/iAy6OjtVTs9AsfJBcYN221K11sa5sykSZWdFMVMRnyUvjXNAVOW6djWaTw/gkq3tu'
        b'AbnpUrHnF7NQFtk1nhUnD1aR04T2ZpUnG2XjS+SOOCsPQLjeQ2h/ELmSg3IiSZtY/2ZyqYq0UaF2F9lrREbTQhH2O+ReImkD4PEdWS7KjR0o1nPTTDaQNgZ7Qh7KI21k'
        b'M6snhrwKynEbgI8PjM5H+bhhqDReGXGkDeDHbfEFqIBcrGPFRw8ix0gbhf8a2VeICkPIERGcc6AZ3KPWP3x+4hw0B1+qZpMxXJYSBrC/gC8XoSLQJl9hAzaB1KvDAPRq'
        b'ZzEqjo0VR+BKX3w9jMJ9YXQJKsGt0giAxHpkeBgATvaRvaWoFN8hD1jVlVp8KExBp4UcnIvm2gay3BF4d1EYBXs/OTkPzXs2gfVmDN4yLQygnkwa56P55CC5wdoc9Aze'
        b'jJsY0OTOc+g5vN7FKgkD4o2bAG58ZWUZKhuULI4hCFvjcRMd8j2O59HzII7vs//jq6++ql0uR+oSjoe1lzsmbaW4zFT68cgub1DA0i360XMxyFYaM1/m+g48OV6Ut7Rl'
        b'Ur4sI2rmuaq4gX8ZrXwXf3YlZshre1Nfi1DrR7x1aOb6+vpl/L5G/fGhv0Tyuyt+Pu3Ahvg3uD5nT5tUpal37cnkD/8uX3+3aHz9Ok9Gc9mUvNOhS3a1nf/B/isZXsOh'
        b'vNX2K+9p7n51deoL4R/+dv2Ml+Jnfz/BNf3nrSD//mPPiO9k/x1/98LA2SeWWXffOfi/t361vWXr2gvfrLp2/o3ZPxvwy7IxI1+oa4nru+Yfd98ZVfrclVDrV4kf//A3'
        b'Sy7+YswPyeXvXl395fidCy59UvLNcys+ly2Z9MyByh+CIEy5f5mGiqL6fNxEDlFDXIueWuLO8eTiUHKH6f3k1WExIDbE4l0ByWHRIPcQSujwJRu5jM+DSAfac15Kjj5b'
        b'gaLJLRmIFA/wTmZSyMcnQa5tIluMkaQxm1oOlBP4/isHuJlAeGEJeVCF77rwhaz8lERqSSUtMtSHbJNRexK5q1N0K3fIuxMSgqQRjSSNeCpMVDZmogiVA5AQzslBCAZx'
        b'hI/l6E/4v5RKOYgJ8TRHpgExJQpE5XD46+znr1MnA0HFU9GbfMI54/2Ns/cE5BdNDvViengKng8lR/G1dtGEvDzOkEf/MkOwjqxX4B3kRtIjhBJqDUVBQgn32EJJ1eOJ'
        b'xSpRKKmbG4ESE4DfFJrDY3SZklDyzSWh6K1FKZQF2y1jBcS069n4Jn4JxF0m65JjQ8uBBJy3VW2wKVwz4PFC9YFPzWWvXd52dMeZjUc3ntk7etPo/Uezhm3Sxb9ltORb'
        b'qq3b5Vfii/Zk6Je9VPbSw0GaNwYoj0zcZT8y4P1w9O2/RRzJKdJxTLJ1zsQv451DgwXbWeSaX27tBUkGiEjicjs9FW4PCK4mp7XS6gR1SkSYcDoc6xCvBnRgkmv/IISQ'
        b'u6Bw7xgxIIAR9MUNAYxY3wtG0G2OMaQ+PoAQqQZdUp5BlwISa2NqTp4xJQfXA1dsNoJeCv3eHEpezO33SOzoKLI+PnZ0sVP5G+iIHcp8caPkAblQE0YNFfgu3kLNAHvx'
        b'3bUMReQhY3MJ/wEVMYvkqREo03ZiY5PC9TQ8ipr1h0/NC167rLgOuHBl4zKuIvSX098YdltzUvNG5RuxJ+27hp2I/Y35JY0y6tk9L46JQJotYaNmV0t6jQJfXOOf+nhy'
        b'kM4+uVXKzKB9asiroNXokxZjbwetJj1PmsWecSO+kzrTETNCRcwIUXNxgBnOgcF4UfFIvEgI4AV9sZFWOJjhBfqiF8yg9vjn4p7uoMT4FZjUnNR4ihoiWqzCZ0JIA96G'
        b'X36kOi3rZMH8D9Xp7jBDlF5DQMqGwU9TxioNZklMTqpluxfatExv2BcRw8XM9z3Sdt748X1+Pi8K2X54xCNz0e2A3BUnPzX/3vxWeXXleevH5tOWxAp9+sdGjXn+a7e2'
        b'DQXqwb1VmWPZbv5Y4L/7rnbt0YWqGSpXaPGYVybMGDVjaGEBM6LPEaJqriYB7lAijQ+Q4zZ8LjdPz5OdaiQ3cviqGt9nhpwEfAIfB75ItqYW5JFmfDgtPxufl6N+RfLx'
        b'+DQ++rh6cUSNdaXbJHisJsHiFrEnSsSeqFBgP8xCA5qxc1AAh+Q+OS3qC7FbLQK8teoRFhmKO84hAZyiFbUE4dRfelGNh0EJctrMkya654cbC3R5uLkgG7g43ka2oZHk'
        b'qqJs+VMVsqBpVgRj0XQRi+RsP07hVVYqJUySMVu4HDBJxjBJzrBHtlZeHHTfm1qs7IJJChGTnioA5Qi9VqgE5cg+LEJEmhEKiklvPa0GUe7Pq+OR7Ru6FrmrHJ58eN0x'
        b'aMuViPVp4fKfLS9Ky/iftzXXWnVR7jk5d3Mqbqj3l885uGjdxFOb+im/eUz7zOpBv68e+4W5IqbfrzfMjt192rvjJ7fnjfx286idn83+c+zzT6m+eqnqqwf9FcZ9y+2/'
        b'VU0p7T+oYLVkT4wYP58Z/lz4vgrx+BhXSi6QRjeVQPXk3ADjs7iVjqu4ezzewwjUSHIv10jXcBNpLuCQGhDuHtnC4/rJgxl+GvEteMaBXNaQCvRNnscBhT26jIlVeM9y'
        b'/CppysPnh+LbCFqs52aTLfhcbwKTssdHnbE2vMraCWkHiEjbHxCWl3NUTgIpied5NR/9L7nSqQ2gr4KiL+AsxUifssLjdlQG08Nu1wugNUVF59COqEwr3RuEyp/E9YzK'
        b'tCy+j1vxSWNBSjsmly6FMR+Cj8nJ/tyontnkNCQJUXRLGVUqvgar7ILGEfDbtwsaDxHReOGsd1Dr6Dd4EJmyhz/tFtHYWKhF09CfeNDxE16f2kfMdOWqUZQ9jRpS7FtK'
        b'F4iZ76WHotjJV5jEtTRUskWMmh2NRtRmwNIx1/2k2CRmfvZ8ApqQe4SaXBY0PxMqZtZoxqLq2HEccOP0+aM8YuYfa5UoPPabclB9wjPyhoqZr65KRIXTXmVmnFj7DMm4'
        b'mTsV1WmVMpRmjt4YO0vMXDB2MlqZdU8ODTmtk0ZIpoy6icgdL6dwOgtKasTMeRH9UVptIqxg8+RLxZIdZvAKPZo/P51KlsNujJJMQ6WoD9LKh8uoafVv6r5i5u/1GWh9'
        b'fIECMqOP5gti5kw9KHPyRmYB22kZI2auTApH8RPuURNWuCZ9vJipnj8AjZ3/UwpS3UW3NHSzdU+D2reG9r2IVEjdHBFViI7QbZZac9L9sPli5vpaK3orqj/VGivTB88T'
        b'M/8RVonenZ+vgtcr346aJGamJsQhvXkFVSUT1kwqFTM3PQuMcGW6HIZOfyxamo6fp7+A/jpTSc1NcVtUkqUuwToGCfEjqWXJeTKvQsx8d/RwNBNFwOowlxOUh2wfLIzi'
        b'XE8BXrdUfVH6ckYRSQuf9esPbb94fWReSPbiCaE3P+471vqd/pVvbdh57503fr+6/jf8gXpXrUb4ZaV5+IM/pr69LvrwqnFNkb/e2e+Pac2LVnrWD1+5CW+QvVsY7V7v'
        b'RCVxt34zx7EnNGz4hBd//dXgV3954fQLtdHj3tZkXS6+Mvf45Ruv/eD1Mm/N9lvXJz+7/lt/Kp6/9fuodYzj8kclv/u89J2VM77n/ali/LWj5fc+2V769r/3jf3D+4sf'
        b'/n3o/dDF9c/d+d0PXh+YPfH0Wyk32o6/Y9RXfSPk7Fv/9+4zrzyIXHv8Bf3c33333RkfN33/0tjzbcPfGfudXwzN+/AH7402/qHh7swfP3tpysXX//Ct//3BmV82tg1M'
        b'nzf/H5MO/3pWrkmo2XvwdsPNgrOXNrw7TJ5mDasf869vV01tOVLw7Lo/2y7LP9fJ2AbMmkRyKsTazt3bWXvNIkZ5CwV8KVZh1CdmgUhFKfM5fhVuHMwor4Bv4APJ8GYS'
        b'h+Qe0oT3cqC3nuqni3gEeX30pRfiHWxqp8S53FKzxFTtsNsosWUUeq5IoZ9Ry4BGw+8IJl5EcVq24RPFRI1oPlweCpSb50LFH1mnv+Ldb+UJ4UDjQRMG+g6a8PAAdQcB'
        b'd5XV4gwi6L3wG845IkDLaRUXg2j592N7puXJlERNc4qEPIdsgTHeSlrIWXyONMDfxlyYLr0STSFXlOTWqHVdFBSF9NdVCRcrdctDZbwQxkz3POhBvCCrDymTWeWCXFDU'
        b'o41cmQLuldK9Eu5V0r0K7tXSvdoqpyyikhdChNB6NeSEeEFULQtlWnS4T5UhCE6ry5VfoQyCRS39Mi6QSdmM6LEU8GCqVEvMRtmgBmajAmajZMxGxRiMcq2qOOi+J62d'
        b'crOuWrsinxnGDGSrohihcj0aiobis/ig6IzS+twF5PLA3Z+SbIM2X+mD06LkXxXsEk7Vvz4zNkPxfuJrjUr1lA2f9X15Qf+iU/ey//6b5X/X5e353dvH/6kptdQdblyd'
        b'7Nu57EFs1D+v//zFo3kt71+reOvBex5PzJ6Wz196cW9iuOmvb5nTP3jt7csj8d7+B8fscI3+iXXVv9Fbl4c8XfRbXSjbTsWbniNXAwstq5YtNXKU3HFTiYM0voB34aPW'
        b'zo4uXkEUghrIbnw02aDLxS+RzXppGzezH5OuyLWIacyVjdVMXiFb1eQujxvx5hq2xtXyqmRDCtmPG0S7wXE+Dd8gXjdF0AUq/CJuwi2kxZhCXZVUKCyOjyDniJecJlcY'
        b'DYkgZ8hd3FQAhIA0J+vwWTmKHBAZInMPxW0MOHKwDB9iBfDWtXp8Ro6Uar6/fjR7m6/CO3BTKgh2hviQbNHYE01OyMiLdYvZ29kZ5CoUMOhy8lI4FEaaeOtAcjNZ2VUD'
        b'UD82iWknISqTqca6wmTiAytyHYjr0i5xHNupo145SulndaSE2wbpPZEYqH2yCruLbcqB3mtzr/Kpax3Ug0Cw+pQut9NqdfvCPTXtBpbeFBmlk3qiOqkTorjNp6MX6qHq'
        b'TA5QEWow+1cQFXlpQI9UpAvMHaQ/TvotppUxyxZaLC4sLv8M51ObpD1JuJe7rPYgBwpxANWT7Zal5YJlagTU4qQa3eoof3v+R4/doI7zKUx0/JyGQCuBppxU8df4W3ms'
        b'OqvFOkNM/tnosd7IJ6q3XqxXZRLntsdao7qttYPAPRGJdimgpv8FmyX9x6PO1E+Wb1sfsYh3UTKjGNj/U/PH5nfLqyvDK3+eu3GnCsX8iSfvj5eMiEn60SHkMFutgaUq'
        b'qxXRnO92CUXYXEGmw3Z3tnXwE7e6rx8ZOpQSPXBkzlRaS/taCG7AEBjJsXCJ5vz+HOvh5zNNz9jefYPAAeg/XRhgtIl61ZlMvlCTSXQeh/twk2mZx2IXn7DVBUvY6ai1'
        b'OgEZ2Spki7J9KY5lXadeeBaXq8Jqt/tpQef1fIbin1gMirAO0a3uz+k40b0dtQJA/yq6TzjHfnhg+8wkc221ypWbrctJwFtTDEoUupgn3tmJXWY7TPrr2sIFsXiuTNYq'
        b'a41sjYLfiNZIG1/Jw530I/DNSkFPRYAgZ+EoYL9UCAgBdi63KkAIUNUjYPkhzTwIAgohlKXDWFoF6XCWjmBpNaQ1LB3J0iGQjmLpPiwdCulolo5h6TBIx7J0X5YOh3Qc'
        b'S/dj6QiALBQWRLzQv15dpqE9Eai4MaCZYzCHg+gyUEhgokckvDuIvmuNFAbD27KyKNbzSGFIMy+kSOYYmaAVhrK+9YHyw1hbw1lb0ZAewdIjWTpGfLtV1aqulLXKhaea'
        b'ZYKBCSniGQA6WhpvZGWIkCjoWI2xUEMSqyGZ1dBXkDESkQqCUAWjng9HhWqD/km54uGEDk90Sp/cBgKtT04RsTu8y69QBU0+XTka/3IvopRElKhC6ABKE+v3DtdUaiQK'
        b'o2LylRoojIpRGDWjKqq16uKge6AwMubFLf/oC8DrDmDSf9k1NrfNYretpqcrqq1ai9QpG3A5S00FPZ7R+ZWJtRanZamWdnCidpYN3nKyV7OnZ+RrHU6tRZue4vbU2q1Q'
        b'CXtQ6XAu1Toqu1RE/1nF9xPpy3rt9OwZOlpFYsaMGQWl+SWm/NK86bOK4EFGvtE0o2DmLJ2h22pKoBm7xe2GqlbY7HZtuVVb4ahZDsveKtBTIxSMCocTCEqto0aw1VR1'
        b'WwvrgcXjdiy1uG0VFrt9lUGbUSNm21xaZkKH+qA/2uUwZgJwuK7gSMNDZ34ig4ve+c/A+IcXFB3KxXp6WWLW4vtSAsaouCBlzOjx47UZuYVZGdp0Xadau+2T2JI20VFL'
        b'j9NY7N0MoL9R6I7UItx1D/Hj1ONn0mJd/tTXr09kzmJt4v3XqKuLab+rQTY8n509wScXkj3Ugqk30OMpxnmkwciO0KzD96nhDd+LKmS2i78vaEEJ3AQ3l2bWHB2kRh66'
        b'+UP2kgYDM2MWkgYqqaeSRrgrKBZrKc2iG8N5edl5HPWdOBZCzkwkN4bksQod01QoHK1MVmnN4X3DZiNPCgVnazK+SLebk8jGZCP1v8ydk9Uuo5PtOnwGFWeoyG5ycrDo'
        b'02SjOw5piTwy69vGL5EMbDY5qG3m2shpZvsn6VVi3ZFk31xatb9e0kDP0QCoqUVZZHOuEs0mJ5T4It4LKsI65nxQig9ku5Yt7EcdHlpoDxrxZduAW2Ey1wfw9Dvhr49s'
        b'mVQzfXTUrDf/fq/li3rtiaHJ5v6/f3F80YDkWdsSw0/Yyjf/c/m2P99+e+L8AT/Md2VGH5y6ou7Eixu/Xfnnz3bfPCff8V7LNwoXXh7V/MLEHx5oVq02XhrVL/KvC/+W'
        b'UbNh8OZxb6TuX5r7wQd/FMbP+kXfn9q/GLz8z46mg3+dPP3ZCV8UVM0Timp0Y0ff/9fVFefvZ//CtH3fz371r/ffM/yj/Beyn64wPRP5Qfli1a7DFdHbn94WNt/Z/+xz'
        b'4y4ONA14Ouo3mns7Foy9ePXt67++vtS+MeGbPzv82ys5M8P+qYsW/Qnrx+KTYTBGujxPShLZnPpUAY/6Yq9cbSLrmVo3xJlKmvTLpuZ3dDiYiE+42ZbEUXIEnzAacvBL'
        b'+HaePhs3kxY60jI0AF+T1+AbCaKCtQWvx9uC9n2n4PoUsj3RTW0NdI8mO7BZJr4Pd/Uy1JfUy8itZ6AtCiw+kdyPbRJKO4T4AN4h7hKSe/3dVJo1kuvpMOtbQfu7QlqS'
        b'CT0SJe3NGqF7W0WXhdn4igo0xU34nHgEY/dzkcYCfIDUUxsGQ46wOTy8dCeNjQDemtsfN/m7pSD7OHU6uQM9Oi7uatYWUVl0c659oBLJyH4Ob43B+8Q3940toW+Ki0xB'
        b'7vAwCm3cdHiTNjy7xNVRKSUX8Dmqllo5N9Wt8CWXjSqezTp2bE0cXFpXDG5WoGTcpiCbRpBm1tTgJLyTVZYLmu4DDgA5zOFt1LGJKdAV5FASPDbkrSNnKZQ3OLw/khxm'
        b'r04lu9MplHlAEdi+B24t0VTJJtZMFfX6neSVUniXSnpUzCOHyW7NDFmmbilTv0vJebKNvq6HQc6nHsL4cokGn5bNhAcX/Ftvmv/Y3tZZpgch2QYMXtKLs/zi/Gg1818N'
        b'59XMjCbnNHw4F8dTg1o4J/pWU6cRZacfnsrq9OdfSiVohyLxNfibyBfl5hBRGXiWXqYhv+7bSepuVxUeW9nXqcRK4jrWzupMDVTM5HK6izekg6Lxy6d6VjS6dOSxVdIz'
        b'VM2lYlCPiuP8IGVaasWvTD8cWRKQmSg3A/nCz84SnVaLkOKosa/SGaANmeCoeGx1lur3pnJbRY8gPe8H6eEICgBIXL22/yRGBgXTyHpseVGg5eTexaInB4D23En9oXps'
        b'3BJo3BAsU/0n7YdK7S/m/CYKHhacRVRbRWTtCRqh41D0Jm99XVCcBYHl0RMUVQEoUh9HUntySOqDIEnqDZLFAUhSHi3lfR3kOMOJUPQEwNIAAGklTHWBtoMNfVppWrV2'
        b'djq9Rxj+OzYhUfGUPzzWRYydQVUQl9bWacW6rNal7HQ86D1MM+nyIj0xL6ljxaD+QA9neZwObaFl1VJrjdulzYAedZWaE6Hb0Hl4cfl4Q7ohTde7XE3/KVBXo73/eDW5'
        b'gQ/i+8mUAa7Cl5F8GofPkg241Vbxzr85F3UVq3IVfmp+tzzLkmhNLPp4RLX5rfLfQ5ov/03sG7EnF/1G88ZKpbZlKHObev1PIeOG/UMnZ/bncWRreTuDHS0DFsv4K75K'
        b'XmUsOGvoVCo9zcgLkp/8spNlvmhg30nqqejPHuGbuEU6TT4OX3Az7+Lrc/A2I5N9+PSMRVzqwqreDGoqarnyn2GSPKzWoeWhXBy15UrsQCojMk/nuM61tVvP6G5YbQem'
        b'tr0X61nn+kHEmAavPcJ/itoYkJd7Yv8pP756u6BHsdUt2hU8drcNtGqJ7HtckhrNwkS4nZYalyUo3EP5qi4V0TomMkvLRHMelIGq4I+lyuo0P0LZo/+62lIl75tbsaDD'
        b'RU2mhxjyrw8dJulwd6IBbbrX4QaBntWdGndD77S98KMPZa4JUMHMop98as6xJBqLrPqiT8wfmxdX/l74nVn+Hd2WH+lnJY0M101bHlN4fOMzh0ZvAlxuAzl1cdjN92p1'
        b'PBPhC5eQU8HqBp9Bjov6Bj5ucVPGQtbXkPXdSr2iyLuskGwiB8hxyQHrUfuvLqvb5J8gxsOD3broD+cXDVf39yNWl3fy/Y0xaYxiW+9uXqxEagC/6QnN1R3wu6FnR69e'
        b'wHgSgUXT8dUeucNLHdnT4+KywX/Ki9K+np3O6ECIfjrUPhnw1XlclzMZY/nyj3K5bsx7gfXncNqqbDUWN8BpE3rirDXWFRKtH20Y3Y0RpWfLkSCaZ9gQ+H1MoSGDtsi6'
        b'zGNzSiMkwF2FWytYy21uV7fWKrr6AQKXY6lfRrMBu7XYXQ5WgVi1OMiVVqerZ1uWp0KEaMb0bGDktmUeWh/INomUaWudfqigrWy3hbLxRxORrs6g6nzPJLhfJeBrxny6'
        b'rU+aUuck5qfMyaIH8q5NEN1Zi0hD7pwsWZEOn8nWLip3OtfaFoWg6VWRS/NyPXT/gVwiG/H9YENMVsAXtggBKdpZCnyzDdjbTm4Zua6eRw6Wiwe+d9YSL2kLp8dSLvPk'
        b'NMKHRkzwZCB6Igo3jXBpPHOz6FZsKWnQz2WuBk34TEmWnrayJTuXbOaAeB3XxeHNK/GuEeRkCU9Pz98MLxwyVjxl+EpEEq7HLcGg1QYqLZyXMleFCtcp8XE5vmd7771b'
        b'yFUDb5kuXUh59y51UZw1Zx12cJmWqPj1byiOZWWYue9OvrE+7wrfbP3i4wHl7s/Ga89f+9ukgVVT+zu/NWP3/Nz1WsO+kREvpL3415IFxr4/PXt3/JoJzX/4qO27SXXf'
        b'OnDsZ8kf/+yLm7dffGhvfup3u/otXKDdL/uGLkRUwLfjLeQ0EO1Rk/0aelgNT/abSpgFZu2zU8KS6KEOSi09KaSpDyOsaAhuk8PwbyI72MmQqePJueQx+FyQ6/30ueIR'
        b'Zy8U2w0SxFyyK2CKCI+S9cWvRDGiPcWT0YFmo75WvJPR7NP4tGjeOYfSJOGCCRZT8Ut4/3Ryg9Ufgi87g802CMXj3Wu18kX4oIN1MHQFeSDaLiS7xQGyA28jXrybGVjw'
        b'QbKDZ8YL0XIxfD7eXxAueTA+lhMOpaTtVMJ/3nVYOxOIUYPuLzKCcIkdiCllJ3rcoZZ8PwyM1AfIYW+8QRZUrJ1BLIRLI+cHaT37+aJnp5teQHoSBV9uAuLWI2M4GmAM'
        b'o5ke1075elNenkB3qRR3qOX05E+PUBwPQDGpW5I3o3RG562CbuChrlBLndZKn9Jlq6qxCr4QINYepxPUg8wKeRCs1HIe7qeF+SLzag+thbxhki9QeGW4xMrkDQpgZQpg'
        b'ZXLGyhSMfcnXKoqD7iVWVgWsbG+vrEwMLSbKgIwrBKtCPe9X0b6JPMH/buAMRM9bD2wkxLfYKzCKNM9ClUKDdoalhmpcFulZ+WLgbt2yNborBpymuGDC+LTRbD+M7lUJ'
        b'VNEFZazH5gMTMFGbabdUaVdUW6XdNugw7XN7CX+nemq+xuHuphmnFTpS45qozegsXJul7jwGX+yq8YXme+iRKHIc71N0ZIykQTKglmZBVhHwOXwH36a8jkuPxjvwDtJm'
        b'JG05aCQ5riH7cpZ6pkA9HvIivmk0pCTlAOENriJQdVZOaSJwgOtShAuQysmJQeHktAafY2L+tklZaBsymyLN5hxH3XDkGY/oGc295OXuxfyUnLxiJuLjS4Ik5TcVh5AH'
        b'5JU+jOOTveQVO2lixQgok8nZlKMmUx67JWiTJkufk6HINWSnJCkRadKFL7OTk57RiJrgj+IbHRh+tj55OOXTBcWJ1DzdYtTrUnIUaDU5FYKb00t1MjE+2QM7OcLalSH5'
        b'CnxxKofPkU24mUVdKyaX7cniywCwmuzl8YPKF8htcp09riJtFck5A9fkSQPJoZhRMrKftJht38ofKnPRcztrCj8f9P7dCJIWLi8sMjVx6Zu8b0V98t0fN69HzpioQ9qc'
        b'b/x+23Tf2NZ9yYNrvTtK1l8aVXn+H5nZ3/xs4tX5i0rfK0k9Wn7D+8sff3J1f9zrmin6n/3gX2NHjdi9eOWOxJI/GYu3vGM8/YWmXJ404sPpqp8+rE59d/DHA65/mLEr'
        b'Yd2N37Ws6Z86eNuhdTv3J8+K+hC4OjuNeztnAfDcsFoaxqicG70YHxM3Q+6utAXzc+C4MI43AwwdN1YxjV5HzlfBDDN8IW0xfqEABu0OY8kevK/QmJ2XBIIWj9S4iU/P'
        b'xi/a8G3GksnhlaEdWHoa2SiqYZWiwx3ZaVwjihpyfB2fpAchAKVeYZLEkLnzk+dlksYC5omrtPPDKvBBdsYU347CD0iTHq8PBzGKhlbZnKeHyUiVkZ3k1hrG7C1kRzLb'
        b'bZii9UszdLOBtHIiNw3/L+0PhFHeKFEOxu4N7ex+rJKFuFAHmH2o9BvOjvjQrQD+36GK1THBfFaqS2L6SpF9U4rhFOjF2pHzhzyZM7FcrMkakAuEABusgsupTsLBj4f1'
        b'LBx0B/STMGS1/6UemfJbAaY8lHIPoK2MlwSYT7AJUSdnTk08/HKZujgnpU5OaolwUmsCdW4UHBUmE9vYcNJoa2wDxCejdv5pNNnNHotP5bdEU8sRU699ER3VXSpRBYla'
        b'Vewtf7/YBPb5L+1I9YSATkre+9N5q4MbNS+Xx3LKr+R0pr4aPJ6h2JdK2df8K9eEhnPRobwYM0geysXGdS4RzWmHiPdiYMvT48ktV24+2ZraF19hNDJ0NQ8E/iy53oXt'
        b'hUp/XV928tgS+DK5ICtT2FCZUpCXqeBXLSjKQgRlWaigKgtrVbSqW6NauUpZa5SgbuaFAhCYwrxRlTLmiE19kcKtEUKYEM48szTNfJkG0pEsHcXSkZDuw9LRLB3VqrH2'
        b'EWMJgSBG3YUivX0q1UKMEEu9q6DG6FYNtBsl9G1mTuOsXJ9K6q/VTyoRA3VSTy3qGh4LZajn1gBhYL26rC/AxgkJwiC4jxMGC0PqUVk/5omFyuKFYcJw+NtfemOEMBJK'
        b'DRCeEkZB7kDmXYXKEoQkIRn+DvIqoSa9kAJlBnsR3BuEVLgfIqQJo+G5luWlC2Mgb6gwVhgHecOkmscLT0PucGGC8AzkjpByJwqTIHeklJosTIHUU1JqqvAspEZJqWlC'
        b'BqQSWQvThRlwr2P3M4VZcJ/E7jOF2XCf7A2B+ywhG+71XjXc5whGuE8RCiUbjUzIE/LrQ8oMAotGppvjU2YsZS5iZzvIS3Tliw9ELzExcC2IgjR8YJXTQmVAUYCrWBVw'
        b'WOrkFtTR58wJFSy1um0VWurUaBFtphWiHAoZVLSEOkVDi32V1lEjCovdCXM63qc0LbfYPVZfiMkPhU82q7Qo/+Hkare7dmJq6ooVKwzWinKD1eN01FrgT6rLbXG7Umm6'
        b'ciUI0O13KYLFZl9lWLnUrlP6ZDNyC32yrNJMnyx7ZpFPllP4nE9mLJrnk5XOnp95hvcpxIbV/nY7mMc67KJQylDHu0IpAV7DN3B1/EZO4JbIXIPr+CPcUeRKcvMCX8fH'
        b'IRqKuIGvA2RewwmyOm45cpbVcdQdEt7ijshoAGNB2R/KxaNY9DRaw9Wo4bmK3jUg+l4dMsmhVsVRIPcmpaBmkxvykak7faSz55w0z+2Oc51f6EnKZyMh6hgWsQ6W04tt'
        b'Sxyyicw3rbggZWz66KeD0UgA1SS7kor8WlettcJWabMK+m4VA5ubqhHAA/0+cqxlv64ooixoKk5buacH1WIifTzRLFgrLcBcAmhkBl3FVlFNa7eJ4wTIKLUDCNa1b5/Q'
        b'OX/Y11bDtq/aezNqpGuUjzP4uLRPKNf45Cv491BmSEvL16l8UZ2bpXsuFntttcUXOpf2ZJbT6XD6FK5au83tXEb5m8JTC8vE6UTMzsCkCIpgzjWo1/PzjPX+L2VUsYz2'
        b'y4FpxEomEC1P5aLVkSICPLkbgY5joPUoSfwt4ETgbyLgQ5DSGWnY1K2qtWrNMCUVwOvthpniX7PZ4KTHdZ5ky9TZG1j/CAg4A5knQ/eI2KU53t9clNQcXcOL+bDA2QEZ'
        b'mxCf2uIyMS9Sn9q6stZRAzpuj6D8MwBKBfMs8CwtBy0ZhkIaA22t3VJBt20tbq3danG5tek6g7bUZWVoXu6x2d0pthoYMyeMpGA2Uyy1CIs9UJAW6FhL1w3fjsehOBae'
        b'IhBvPHAcimP2/Mfb/KVGkD90R3RKa6lwJhIc68qKaktNlVXrZFnlFroR4RD3eKGURVvrdCy30f3b8lU0s0tldAe41gq8YwYdXOjgdEvNEmaCd7kdIDoy8lDzWKRAIgN+'
        b'kEwMJDMdYw9b+iKhoRQpYHqHMaYutt3s9NFo8FZ3taOdj+m1LhvQVKka+hrdkg921O2pj1JFE2k8+YlmicV2s2XYq22k3OGgQXq1lcFGGA+bCqHTNHRLJFdYnbBMlwN/'
        b'tJRT34IezDEdREwWZAR1tqxo8kWn0LN4Lz6RnJIFam0j9VGlxgqyNQtuC0oTc/TZKUq0NHr5FDV5MDzCQxWDEnyqEDTKy+T6nMScFBpJuSU5H18nx4pSyEkejR2XOFtR'
        b'hVtKWHh2vAVfXe4y5OXg8zqyc4UyGkXi3TIDOUReZM0n4a2Tgq0XifkpScaUIg5v89dtVICoqsZ3M8jLYo2X8IMVLhoP6V4/0c8Pt3AAzX28SZS8N6hGFJN6M24mraWk'
        b'mewspSaMAo5cs2VlirFYdoatc+EbawAqBZLhPRxej49Fii/vcOtcWdSsEbOCNBvxRTnqA/Di8+RUmGg2OUNuzHcl5pCXyCGqSyvWcOQC3lNQYrukui5zvQVFSgfr+jZP'
        b'qpk+J3zm//3z1xnRp7f976KsNzVFwwc0ZWUrGhO3DVH8tP6Nb10+oR8VZn7mT/+XeWjMm2UR6kF9rvVf/DBr665B8mtlR1//uW6icOsVtLH0na0btpj++cfMX2999vSP'
        b'Jg7/Qf/Tq67OOr9j+f6EsYN2f7Qg+6Th14OOp/tiUhI+r/0wIixvTFZxw7UDb7a8/6NDt59xfvXublNZ9ke3lv2Ym/dC/wj8xRu6e59qv8yceFF1auSNgZHGD29+99ay'
        b'+7/49ej/uZTW8JeN3xqYe2pd+ulnNwyx6vqwU4g2sh0620S24suAE6RJheQpHL6w+gVxM+Mo3kzOJaeQzdT5c1tqFmmWofBMmZKcmCHGhN1PXh6Lm/Am0pYKpTgkT+Vw'
        b'Gz5kZXsNCweRV5PJBnIgJy8XHg3l8EHclM1CQ6SSu9XG7LyYkKQ8FVLKefV8coC9U4gbeGMqPsACZ8FL/Th8rHapmzpcT8JX8a5O1hxmyWlYIBpztuP1zJozdh7Zl7xU'
        b'a9AlJUpfNYgkV2Wr8G6ySYznfUgeaZxBTrTHpcAHh7L+hJCT8Crx+r+GIM/n8GV8DW8ULTKXE1KptSVbb8CNqXRRwfvalWSfVk5u5Frc9JwPeZkcI/eM7csMN6fmqMew'
        b'lZZE7inIBqhC9Gc9lWY2sm72NVCzYCOHwgSe7H9WyUxanmfJfWNBCof4GnJmOZeBz1eLRz/Px5AHRn2i0x10RBu6xOxd5CLZEWHMMxrzDKRRb8TNBakWBiWsRAWsrVvS'
        b'LpDu6XGkqez5fHxBr0TymRy+Dwvq/BM4WX6ds5d9RUpo6kj8mTmJepVI5qR1SEO9SkVDEvU+jWUepvSMpmhk0og+qVIu9UtlJzUTJJmn20by/We12CnLr+NVyomvMlFi'
        b'O1y+6mRE2tjLgcxeQYOaqUzZs8cNizXD4pyBqMAFxZrh2adFHs/rhm78/093gsIMkdNJh3pECZFKNcB4KPMKCGmSvECFB5ck93flS9IWQyeBo5N40b040ZXLlXQVXSyU'
        b'PXbg5n7m6qBcn+6vrKJySVfILBXV4i7+UutSh3MV2w6q9DhFBu1in5d5NKfvrFZ1FGeDPCLdFmcV6DD+kr1uqNQEdlRELPFvqPglKioHWV3BBoBHCATdn4hXi35MQyZF'
        b'jD8LSIEKzbm7Bs8Uz3z0WZUwfRpfSzPrNItWi5l3Rt1A6+M+A7Sctiz+hc8rRce8RnKTNOMbWldEBGA42Uq97A+TC+yzFfgiPksOGztJGP4NHLaZADy3hLoDzAPeT7dj'
        b'2j0MgEatxpsiBkdNJKfIHdvyjHPIdQYqrb0q5EnB06t+qImaOmhzw4S5q5OSp99qi9r5vW2Vtgncps/jEtZvtOx/6Q/vfdycOSHjT2bLlX5//sbJhIlXZOl/kY9+O/Gp'
        b'zepTP/kw68yclfWjvzf9o4/f3H2iwkES88psP7qhmlA8cP//hCb9tPJs5PurYxZtGlYTe+iHF5bk/C7teweHvfmLopbhV7/9gy/V8z5fuPDLMbffnPrCy9+7OFmt+23f'
        b'8kXvTz4yZR33wuYJb057X6dhvCUT71pOT2aQYyP9ngHSyffyZ0i9tDkF4/QyEz8i58rsuJVsdD/FmCk+s6gT5wC+sQzf8LMO0oIPMiZgJy+tIqfY1lBTqj/s0svkJost'
        b'aRwY04EF0O/3XCGtfiYQpWAcWEV2T2Wf9rk6UWKC/eeJp1hu4w24NdkfHoQ0OuQoDF/lybl0fFTczzhYUgwtN6SmlGb6ozOdwGcYZzGS/atF/rwQSfxzKNnCIovh5lHz'
        b'8JWKrhyUss8CqJu6kizHL4UweTUbIA+MBXDoI3Q8eHIVb+ZMqWp83Ia3MmBW4lsgotLtF57cAJatXMwPxqfVrCsG7VhpY4bsdfvdLZivxTHsZZMyBr+EdyXr80BGJY3j'
        b'YlnI+ki8Q+aMI9e6O6r/uLxOJWkQjLtNDuZu40W+pmTnJ8K/4vnQL3le/SUvi/o3L6e8jAYj0TBeJ3pQaLjVGomBSJV29KBb05Gl9RKWhBfLtrtKtMIlEepyjWhnZOuR'
        b'r+doU50h6aK1U+LDtHaqglOtHX6pfW2AwLl5uJdt5OKggMB3SPm/H/SQH2l7KB9pSK+EzlFYfeGmGodJ0qtdPpml3CWaYbrR8H1RpsCGuWiuzOH9Z9N5GEZ+dT+/5aVT'
        b'uS42xcBOdS5cGthnJTbyzsw6jvUHLZE5p9F+OZPquCO0H+got4ariXPLBK6OpWnJSploaYR7Of00BePCfP7DUQGeutTmAjAqqhk3GgnMgBqxmF5Nb2Am2RDE2JbW2m0V'
        b'NrdJHHSXzVHDZs4XUrKqVjRdsUGR7FQ+BWPdPrVo+HU4e3A71phqnVZgaVYTKz+Hlw6oIxYGVgkDRvGTYsHqvv6B6/BGt5PPho0SAoGaSmEoqLF0MVfJx4mGGxiAaLG2'
        b'RNpJvdhV5wuBSdV0hFJtMkGbTpNpAYWPCUnBJjTxWc9oGM0g8SOiBEUlhUJF0QxGPajpTvikMtGAAiZ2KMrfsibQMnvUQWqj93J/w/EM/48AJgjcUX4NG4Q6bklgELjJ'
        b'Z3jnYSSZFeGercqD3YChNJnsbpOpnJfYOYLZWR0RgIM+e2IwOD8Y/OQpzhO0qZM9tGw1mSp7atnaTcsBHDAEL51h/kWxhHdoRRgWc0uoRYvl0zu2YypOBoWlB6QFkKzL'
        b'TKbFvN9VniFrKJDRIMBoiS6ABeyJ4WxIaKPhflui2EAPQ1AD3awNQoH2dmq6G4BHDb08gAFTex35KphXVw8jX/V15lzhJ0D81N7nHDQT04qeWrZ2s9oCXvN0aP2rPuAa'
        b'F0Swu65tajEzmV7odm2Lzzr0s4NsO6Lbfvajmz+IkWF+I+9f7VzyGVn7cmOE1R+O5GAgtxN4sP4tgmAyrQ2wEaZ1BtEA9rjbJRCEaRTAo5yE4DAc13saekrqWI0buyd1'
        b'XVt7jOGI7zwcDAW4FCcN3u+81n23XZ5yk+mlHrvNHvfcbQ0DJKy94xQPnDd66zarsan7bndtTYaC6AyVnAN0RuNGjKZAOrYrHtBNA58m3+HOBo5qpeeZrEI7PrDB6OmI'
        b'jsm01APIuJWX9j8QE+I6jAor8ETIAKr/vd5GhdXY2v2odG2tAzJMDh4VbVe0GBgYp4GdxkmK6UmRJLUdSXoYlzCTye30WAXbcpNpdyeazMPoRAcADhT7+jAPCMA8oDuY'
        b'RX6W+migw4Gl2R0OJwPncDdQxwSgbi/39cGOC4Ad1x3Y4noc+UioVSx6kcl0qhuAg5DQ0ZlGyINhLUQdmXI7rG4KLd0TB7ja7xfwa/g1Mglm2UYKvUy8q+QDcjuf71PC'
        b'GEHTILUzGvs6Cia0fkWFElqfYkW1w26lPsNLLbYawdqTdBpqMol1mkyXeImoiD0O5+mZ89CvVvcJ9NpfsmeJlMqBImcKY5PBKEJ9QOLojjuxUHFVJtOtbsU/9uhx2gtt'
        b'b6/qUe3VOlwm091u22OPem4vlrXnFtviAjRP2ijd02E+emodlCuT6dVuW2ePHpvvs3G93EtLthoQYL7RbUvs0X+ppRC2gC1Q4etBbUUFr2760LkRdWN/7bC+6SpZgpxR'
        b'btBcmfcIJ8gEOWUy/QCQNXR1UE2Qb+CPiutFWiUMREX+J7TSh8PYrrGtpkpb61gh7juPThO9Lzy1tQ4agughn2bwcaNhxTT4p8ynXuax1Lhtq63Bi8mngpqqbG7Qia0r'
        b'a/3qX4/mCBgJ1rjJ9GY7+VCzKKma4BGRCom8iQ6LLrWTk6FzsVSfy+5w0whn9OvZPk1HmzakKyutFW7bcjGQNpBcu8XlNonWWp/c5HHanbtpbfvphVq4RXfFAI761AGl'
        b'P4yZR8X9WWZ6Z8qvk8bHFqnNUXp5hV5O0Qu1GjrP0ss5erlAL5fo5Qq9MOnrJr3cppc79MKY8H16eUAv36AXQi9v0gvd9XO+TS/v0Mu36OVdevm+f4x10f9/3B87uZY4'
        b'4PIu3Xag7hZqmVwh5+Vc0A/Qxdi+Pfg4Kqgj7uBR1McxXstzoUpNWLhMLVPL1XKNUvwbLgtXqNkvzdGo2U8I5Eo/7CuduHHRMBfZQppTmdejOp7Hd4Z58Lmugerk0l/X'
        b'h53cHv0RYCvlLB6tmoWfY/FoaRA6Kfwciz0rhLC0ioWjU7BwdCop/Fw4S0ewdAgLR6dg4ehUUvi5KJbuw9JhLBydgoWjU0nh52JZui9LR7BwdAoWjk7FnCgVQjxL92dp'
        b'GnJuAEsPZOkoSCew9CCWpiHmBrP0EJamIea0LD2UpWNYCDoFC0FH07EsBJ2ChaCj6b6QfoqlR7F0HKQTWVrH0v1YwDkFCzhH0/GQ1rN0Ckv3h7SBpVNZegCk01h6NEsP'
        b'hHQ6S49h6QRIj2XpcSw9CNLjWfpplhYdLqn7JHW4pI6TqEzLXCZR2VDmLInKhgnTGO/P8EXSYzYl7adZP7rceZvJf+AzqJAUC69TMeqywfxHKiw1lCyWWyUvObeNbfL4'
        b'vTxYsDW//xx19BB3U6wd932k3aaOjh1Uhwo6emumRNginhQSHBUeqhMEau5Qm8Ppr9DmFs1q4qv+zZsZGXklM6UazD0493VIZFdKXioWbTkzAkJ14p5b8NFgvdikv6+S'
        b'A6fbaaUD0qE+i4v5i1LgmO/IcqjJYrdrPVTIsq+ibKfDmeMOL3dguFTnowSHbnm7yjnK/ZxRlAP2Rw28h3PG+7mgm1k/j3JrZAJwPJN4lbOrgl2V7KpiVzW7hrBrKMif'
        b'9G8YS4WzawS7agQZXCPZfRS79mHXaHaNYddYdu3LrnHs2o9d49m1P7sOYNeB7JrAroPYdTC7DgHeLTNpBQ6uQ1nOsDr+yPCjaCZauABkXvkaRZ38CKzRo9w2zgW0p07e'
        b'D62R1wxguUqa6xwhqIDHj6yTU6PiGrn7KeD58o08lJ/sHiWo6+Si9dedSPPrFBtlHFr2+wbo3WJNA8fKLchBGwACpgOE5DvfozLCOHEBdFkuvS8IxiQyfZzJx5tMDxWm'
        b'ka6RrocjO1dSbaGeVe3OWaLpVecLLwLmb1sqOUEqxe1HMSaqzGQTfAqTx+p20pA14lkIX6QYhD1wLM45k7In+jVcJzWYO6nrjxhGpYwJBx1PVYIAKO4zQ421HicItlZo'
        b'ggkGKmaPd1t8StNSVxVregk9aagwWcU/7NxhhP819okzeKmimu6RsvC8FrfHBdKJ00oN5RY7jbtUU+kAiNm42iptFcwVGgQSkWYEHluWuts75Is12R0VFnvHY/80OHI1'
        b'3dl1AXxszUI17K8YNNmXYOo05CDOwnqUyirgfqnLFwpAOt0u6uDNRCufCuaFzolPk+GfGXEmVC6rmz7QKUXfA/YZU+WSFfTL8EHBE+rQo0M3sNn8GRX9ypjoF8W8KzrH'
        b'7VJ3yenhhxf/RjHDUDj7sjK9RnOr+3UagSeOQQ1y58cI9exNGg0qj+jkGt+5qYC36+QS5qlQs6T95KZeDL/gdkgnXqmroQCk2la5CghwEGF8AudXZrCe0Ruwff3APnyq'
        b'YxAvuq2/1OFuP2bL4po+QRQtZ1Zv7cYH2u0Yu6trszSQ6hOEzjL21urAjr0NjtvVqVkpquljez73HrJrcKBdXTchu/6DptkEF/fW9NBA0z/O0IqxbF2ecukIB3Nsp+1J'
        b'zjVSZKhe4WLCklgR25qksk0tvEblEhYep5tYUwZtcXtepc1KG5QEBagdCrS73gRov0ubJI1Tkh5ubW721x/ZK4ltQiaJ4bWSngA/nuttsBIDgzW2a3SUHvAzY/q8jFS4'
        b'zHqCtQEk5JPe4EgOwDG5w2F8GnjEWt7xWH5neGYUzZqZOnPW9JLHhEfy2/9db/AYAvAUsdkPYtmSQ5bfWb+Tp5BBO5NFSBH9ouwrLKtc0kl0bY21ykLV7yeJHuD8tDco'
        b'0wNQJvlR3e/tFASwxJm1icVz55U9UewC5+97a31coPVRjLg7HEuoRCuepwdBt7bWQY9KgUjkEU/gPxG6/F9vTU8INB1ZEjj58sRN/KG3JiZ1pGBLYc1aqqxBaFhbvcpF'
        b'Pd60hRnZ+bDG7U8wsWc45x97a3xqx6Ftb9TuqOrYpjbRWDQr88lW4me9NZ0RaFr09qsRUtyOFPjTzri1ibMev02pu3/qrc2ZgTYHdRvjQZuY9/gNSsv7z701ODvQ4FDR'
        b'pRFEwhp6SkRaKmLsjcLSosInG9m/9NZoTqDRaEbjmIQsHXh5omiIf++tlbx2mtCZclG5mjrZ0PvE6QUFxuz82SWz5j8u3RS/uOH8vLfWCwOt/7Fz6x2lfYM2E2jEbCvA'
        b'U8PkQldA9e4u/jwQr3nZmSU0irxeO3vuDL22sCg7LyO/oCRDr6V9MM56TqdnTjuZFGWqpTp7qm1mQR6sILG6zIy87NznxPvi0unByZKijPzijBkl2QWsLLTAzAErbC7q'
        b'2Vprt9B4V2IckCdBk3/0NoRzA0M4LIioi6qRiJgWthgtLhjFJ5m4v/bW6nOBVsd3njhRgzNoM9qPqWXnZxbAFMzMn00pPUWlJ+r/33qDZEEAkn4ljNuLaiNMoUBxx/GY'
        b'a0UME+f8V29NmdppvBSjhZ17FBuytpuBgnWRJ+nnF701Xt6R6LUTO+rqraW2q26Yit+phO2CzJUadOUzz7d4tkPIXKpqE+i9eDKW7nrAr3wjXE20vIJ5yinomyZ2PaKE'
        b'q+ooxwWB/3BSkegOTS1YARlHFLnabWndi2QGndr5W9rNJfTSKZo0s0HQiAbOpYhtrLaHnO60VRRGPy0nVWmV+fcbQc+NZ1+Doh6Zqwd2VjiD3ul5pqg1TfD7W5WITXY3'
        b'TXR3wiFr36bqot4GHGJ6PCkZL82RU0N3do8iupNb1b5RBv3/kvZVTo0S3Xq8qSWDhYl+J03y/aBmge6AEQv23O/YIGDEML8CJ20XM1OXHxqFqIf04IBnt9aYTCs6QdON'
        b'kYGVy9cN7263ihk/2P6ST9PJcPVsAHPakcbuxxdfREe7lVIyW6kkzs0+QOxTSiYrhWixkjODlZzaq1gUEl94B2OVUrJVyZndSdPJKhUWbJRSStYsdbsxSzQkaToaq5zD'
        b'OQl9nCPp3ShOGsTHiufm/AlcvkMtQ3Q7Sy2Th0WnP2H8DFVPcTX+w7gcPf1VPm5cj/BQtUytYB97nm2aG7a8H7kZURuuyyFbkvNzDdRJnX7AIKlagS9Xd93A8jsFu1ai'
        b'4A0sga9H7BOKMkEe+ISiQrpXss8pivcqQSWooazay1dy4qcTy0LEaB1loSx8Lk+jdkBuGCsRKUTBfbjQR4iGEhFCDFu2sb6YTtieawMlXR4EqDyYBlCcpHTYxHw2TBzd'
        b'iTbxVTROgUwIMGg5Uwl8IYFPHcPtUodgsdNv2Q3rbMakLZqCt01cfpcOA8e2av2VqP11dCZudId3vSzgOyV9XC+hm3ae7Fg8M4XRb4X1HJI1YC/strUn+mSdJO1P7K09'
        b'r7+9J6lxUm81NvRYY2DSqVeE3/fDr1DzzhG01sk9VU1pxeYgftPTZHRP5ntyyJCEkfZWO/JZRpyag1rtzFOlVhk5fwyeWv1onrrt0X2U+GrnUwAB5xoau9DvNeWKdkPT'
        b'kl8/8/BaInONhXvmIcXu6Z18icw52a0Q98kgrTyioo5/nN/nS5b/MCVY7l1KYwiUt4dlGNUJ0lEdiwsOq3hKXjw/wKLF+E/fMSYBUtEBJC1QxqecU+jdVHphriV0hoCj'
        b'1daCtu0/OBAW1AQr2oNvlswiCDtkQccF1JIPNj3G0g1/ZsMM7/SMRaESFgVwKGhOO2EQ/ebzgaA57d9dY93LZAFfzFi2XkRaXodmoo2c1LAsv4sEHHiJCgeUji4Mp6c5'
        b'qEjzMr+MenPXi9yWdybR0a0T7+m68HHuzhgZCZcjAZKU0h3sbofbYgfCRDegXFPhhtJ7x9LaqTrOJ3N5lnYrKinYW4cfNS6sVL5O01lMavfAYQjTjivtEgUTMGZw0gw4'
        b'MwNSRi/BUJ6BQmtk0oADL1aKnzxUy6jvCfUtYV88Jsfwjcyw5eHkYhfuTNpIox5AmkkuqHLx4YIuTDpO+uvaznVg0jC17Ed2QFEmo94l1LeEft5QCKUsmH7IUNBQliv0'
        b'OaApo983VgA7jhZigAUr2ElbNQ2N5Y329q9UCbFCX8hXWlUsDJb4TWSVEE/vhf7CAOaDohIGsnQCS4dCehBLD2bpMEgPYWktS4dDeihLD2PpCEgPZ+kRLK2B9EiWfoql'
        b'I0WIKmXCKCERYImyqiqRDVmjNqLj3FauLAqeR0MPdEISPO0DveGEZEEP99HsPkUwwH2M8IwU/IsGHWn/GKQG+hrFehvjjfX29cZ5+3njK/uyYFshZbGtqtY4Ib2ZEybS'
        b'VmBEZCzkFg1A1pd+OFEYD88msXaeFiaw/DhhDFtQk33hFA/9nhE+rtDHFegUPn72dB+fPcvHzyqGvyU+fkaWTzZ9dr5PNtNo9MlmTy/0ybKL4S6rCC4zsjJ9svwCuCvM'
        b'hSJFBXApnkUflBmdyxlJmp1dqNP4+OmzffxMozOHUjc+G+rOKvLxudk+Pr/Axxfm+vgi+Fs8y5nPCswogwKlAEx2h2Xvj7rOHCCkDx6I8bzkgZjr8seKue4n9o8RI1ye'
        b'76E76KSJnCDbw5ZH1LpJY4GBNOfRWKaR5Hh7EFMWPJSGDEgmjbn67Lw5WbBIcuhxT/oB16lkQyS+phthK/vVdbmLhvnb9qvUT82/MydaE6MTLe+EZVnslfZyvWXBa9//'
        b'xrVto9knMqrnKP94Nl4nE78Mdv95fDsMn9FnsRALeFtFKo/6kDsyfCHKIX7kayfeFUuaCvCrg8lmaJlGIdjPr8QbyHH2DY0++Mjczl+RxrfIQZ548R6D//Tio3eseT+x'
        b'DpyeFH8mUNfF1bHBmNXxA82K9h1zp5xSqm6/OQuki5UYFSgWaPkqpVo0PGLgVKT480Ev3xroFp4KddCsUwA6fr9TzRArVPomurgaxYBA7d/vVDeEALKFALKpGbKFMART'
        b'rw0pDrpPaz9F2QHZaD+7fsIwId9D6T7eg6/hHUYWyFAMmZuSYqBBcll8WYoBpeQVZeEKXJ+FT8sQ2VobRrbhe+ke+sUafDwV729/N6t/CCBsylzpZHcOaQYS3mKcl0ga'
        b'56kBneUI38aXwiJseDs7X/7zwfQjhrUzZVqzvSGuALFA9WUDp4sny3EbOSOeLm9bxorvMYWgKKSdHGk2537TaEAeOjmzyTl8r2M8/A7HzFXouaiaYtWqPBeLbIsf4GbS'
        b'ZMzOiyXHjHrSrONQWD5PTi4c4dHC4yjSmptMmvpk0TPpZMeYtDRcbzaiYfi6DL+KdxWwiLx4zzx8IDmfHktuzisNOsueaEjB91MSSUNqEo0D7NCpSRuM7y4xsMwh3Irv'
        b'G0lTNjkzNTdViZT9eA3eH8mwlX3/N20Y2ZMMIz5velYKPMZ3+PH4Pt7smQbPuOnkEH2Gj5CGrE5tSg3OSWTR4AsTRcjwpiwZGow3ReCbpLGINcDhPWNdy8lVOeJIK76O'
        b'9yLSMols8VDWP2YIvhT4kmUz/RyfcV4tlC1JhFSTXp9XKkbyF4/y+6ecQ+S4LByY9E18xUOX/Sp8erJR+gIf2ZybkkWOKVHMbBk5iA+T9Qxp+pmU7YOX0v6tgaCe0EZ4'
        b'vJlHAOR+fA4/CBsHEJ1jn5X0PE+ukh34qnoOJFajPLwDH2Nzl4nPukBYuLJiObmGG1eQq+4R+JASRQzk8V58Gt/y0C/mTCf15L4Lns2l3zlIzEkBHADCyVosYiO3jBMB'
        b'UyK8g9wKRbV4C3szFK/HD5LpYMAANaWSluLERKCNDan5dGRgPPcEvnMAJc+EIHKe3GSGB3IkG58JIzfINRe5uQw3r3CGLyM3YCAc/BgZrlfhq2zo8EHbCEBNsiUvxUAH'
        b'+NXBChSNd8rwRXIHn2IroFRGv8z5D3PENHP46Qly5GGBj+8tIi+6NLOWKaQPbS7U2PpMOalwLQFy9tHIqtIiY9HGaVEHByujp37xcuqX73GTN4x6K+fzyu/1HX6mKCxx'
        b'7o7m75x9f+vwtBdafjXaiQb++cw7v8n49j/dBbJxIVl2YUAlb5GZphVu6PPJ2B2Jn/ryh7zdcqGoz+vjQ6+tFUYU9r99/e2RL8iqL53/a+P/Y+89wKJKkzbQc7qbpqFJ'
        b'ImLWNtPkYM6KSAYJ5gQKKIqANMEsIkhWohEVJQiYRVAxjVWTx9mduDPj5J3spP2d7ATvF7qb1K3O7L9773OfXwQOfc75cqiqr+p9v3ol+n3lrwMu+B7/cVP8jLFNlUGe'
        b'f1sdNcz26ISxbxxv+lvPlg9mfZv8Td8FO3d9v+/VJfd+jO8XkDPo/uwzI0xiX81bN32H3GJoqfe9Z+7Ym3zs8vH5zV+seHv6hY+mLmtbeUPz/BcppoGLTYZbr4pYMCFy'
        b'1amvS3Ojv1j7whMePX5d9GnWL303Z0le6ful/Jlf/Dyah1e23C0aofEON/3s8w9+q5/31tih30R+Vz7t2xuTFkwb4/7jz2M/amjyvpE/7dueSTFTG3phP9/N024Wb5z/'
        b'UcTfsh23z7L6yMT/6cAq92WlK65lPvvp2eY33r02d8Oviz4cuPC1vG+Vv/SYN+mDdT67Hohx9Q5Hcq7+bDrj2O7wKQXqYQxOYLvTjPaN0w0yPXUbJ1ZbsAcW4A1Xium8'
        b'ezJWcoJHJZyVYB2cxONs6+wFp+G8csKWzhQRFLOADKkyDkN0PgTPQWGGlaV5CrZosDXVMhGuyQW79dIIuDKIoTtAJpb05fBB2NwjXZyxDQ8whCMyqRrjOrJLyOEyHDKF'
        b'EoZJtAmvUoLSENfeJHuy2NDinZFgzQwbjge1lyxBJ6HQOj00EVuTsSXNUi4oe0tWW0EWQ7/wxStJTi4Oo6BYz4th78lfPbLV2onsADWduStUsmUzbdirZN5ex9JAyksh'
        b'CYd9G8XJeNqLgV3MgSzSZlhAlgpSZtkEES5Zw3mz9ayiy4PIcs+ptuCy1zLRDauSUqmGBBdFMufSLdanIXm8AIqsFZbmeM46HYoXkXUCWzPWk8IHy+RwBTN5RrDXAk87'
        b'uWDxGtgT5CEK8oUingqFkwxnoh9eh11Y6AeniVyCJ5y3irPJzN/LYZcq8CpZigpDyVp2yi8YyMZHiVl2LKbErS2yjO2wn/fcNXLrDGPngIoQSsRUGERko+kS3Atn4QKT'
        b'vvrh+SlQaIEnOE8TWw5MBPsgmSUcD2Ml8ccDE6DQDRqtpM5+JoI8SjKUJJvLqclaoHkDuRkyLYOvsiaCMlSClYvhDIOngko8N1XLfxZKN2iSAdk45cJgrDXDOhk2S7CJ'
        b'pTRr7HD2nAnZhrRcpIwoLRhqWWMlwVVzkpELZiqwOIg0lr+kN5zCag71kTMEjjFgchfXkKBQxmOLFdtEUrsq2XqNCxvqsAP2JVMuVNK1J/V7ilWENBjPkkLQUTOAyp+F'
        b'oa5QgAUuRLwIlJIBWUCafyTm8eF8eQkeJE8EOPsTcYGIoTUTx0tW4FU7hqiyxBx26m5CHm31HVBKs/Eno9PRwQR3YCNpGLZO7yJdWEoeDnGGfDft4m4iDJ5F8eJNTJyw'
        b'gfUgFikYNaxezjDvLyML9RkpGaCH4EAqE4xIs0I1myVkB+4ox0M+7HHrrOE6ka2meJg52SBPQCaj3cUjuJeMB/K6C5zq/jo0Yl6QWi4ECWTvwGrMTmViSRbZhRmQWwem'
        b'3muCYbJevIRHGFIM7IqAbCKon4GDbqQDQMfwKyd6tRRvzhtuWEr/3yegZQYIJu0nU6G1s7Q/xVxUUM5ZiUzsQ8FUyW97sY/EguKnMG5aC9FGYkPum4v9aFDuA4XUlkUJ'
        b'WkjMpURel8g7+LrSkzx5h7+YIbpXF8mdW6BZ8RrNtfFWOudnGbXPpdAhkzKOKpHKldGpej9muWbl6th1sV0xWUwfozEaFSmrRW2iKYznkiXCMqKbOTe4x4sdW+ySES3l'
        b'hYfQ2Bqu659hQzNdrq2lUcRXvYGrc2Z/ytjOnC/XPcwwfl9/qO3AeFd08Ru8dCotVEonAP3Hd+7V1lW5XOuMtfwh7D6/6wvibMh9K17TXrY/TUqqdWliR9zG8qdKHs9/'
        b'UCTz26JeW3+ZpJefSVC3+rTUpLg4o7lK9bkyVljytAt5XEUjCdo9yGhJmCf2X6PqHfyw/pfrC+DIPCri47QuFOuo4wpp9dhEGgoT85ebwGJ5h7lttBhm+mIw/y7qzbGK'
        b'QszpXSH/Us2LHtbhFvosRxmHVO6ccYd82UKrhxek4a16tHpucBBoeM5WcZPtFoEZHERmZBC2iREdrt11UfddDA46m3lX+Dnj9LfjWQnixL9Afkvxj9NEA7CG9F8nKqTO'
        b'XiMalWZ1UlpCDOPBjU1hyOeq6FXR1NfEYFp6PinvhNho6oOlmsVib2hHa2F6mQujFsRc670UbxjmV4tvHhUVmZIWGxXFWXpjVY5rkxJTk1ZS5l5HVUL8ipRokjj1UtMB'
        b'AhtlQkztNusplL/WeYHjHnLvt40dnMoeDfQeFTU7OkFDStgdcZAFjQld/ondul0aEq/8V71EQwX88rP+X0Y9m3NnhSLuAyL1KvLF1sXD1SKTF7dLiRRS2FkGGQ5HuRhi'
        b'A5e5VU/sehAli1sVyyDWvmMnUdu7fA3aNLzT/qNZmbCcNW/76QpNoAOnLj9saifT3UKqZEMy1dAAhC6bbKZwz8LoNpvmK1BhkUL9dbHlYqlTx2oSSa8Z8x2IbpMfGkKU'
        b'LmjF8kCmuOE5vGTpDgVz/kNkvEZt0/pTuY62aUrAMgZKTbUiZiS1t2mrQK04+UGOAc7QFMntUvSD0CBGh3US8pUT8ChWxH/3+x1BQ4WYX696fBnlans36vYKB3vH6CBm'
        b'j/4q0zTq86jEuK+iClYFRNMhIhX2mit6FC1WS1PpW/NDLXnecAmu6EVcg/ItkeOrmVDfD04rOgIGh2BTJzrHJmsmBluRTrhJh18vPN1dCt6IOx7LYk1Go0Y7Gu0NjcYh'
        b'9Jz0MUYkSYRLnrIOtAPGWRB10GFb9IOWqFlCP6OD9nPjFmxmC0wzhbrHGbID7TqOWKcQOmLP97ecHJ2hljCDI+5dCc1kKGMJHCE3ZdYinMCd9szOK4GsAeSdFXCW3vES'
        b'oXkqlMdX/vKhiYYSnX5s27R2ld/KIDI21nzYELt61epVCasCVoZEh0SL9/qu7bOmT8SCz9xNvJLjBOEp5zdKzaI/m607hO1o3TeOh6BveKZ0GOwvewtzG9kme8P9xXtI'
        b'8pB+6bBlZ5EOsTbaId/ZGBfWjeT+H6CSN7iXG14NyKIe/c50Ew3Vv9eoqr8k8/b2itVxFmzO9vyXxHsJSHzIws504SuLsZXqspaUgbblcXXhGjzVrT+7eJGwjjO47Dt0'
        b'O4lh7iTtq7wR5nSa6hCj3fThQ1jUDeb3vy7wcNnQQBd133dlIZHxX/0qSjT04+dXJgRGW8Qpgj5IIJPNR5x916ZdqOy2qbKDfuN7qlM3BZJ7zxjfQ2l6w40263vG91Aj'
        b'Of332rW7GEuGvrDsvKChhrq8F2ucoj+PenbFkiculhw74LF/R/OeRBNhuL3M+vfhZNOi1smwmVOx0JlamwZMkk0XoQVOrU1lJ2+5rqCdF13nxOwNRmYF2daOcztls9lK'
        b'hngbAXnBLnJBgVclUKpYbqRDRzx0trh2twhwF2CjHUrTG2W0Q9/+Ex3a7mwsdDsnHaBrfEoVreWMtWCKis5fQZLbgwk/nbwWck1y+7Lz0365/XMHxA3Qn6Eq//oZKvXl'
        b'ses2FpxDON9EHV7rQ0/2gtyisIWf7M0ZzA/2VPTZYVioTMEWbLGmxz94IVUuSLDIBmol2JYOF9ixGNalB7ODKT/Sq6Fwip9OzV/d9XxKdzqFuzYoyWA6iGVqOdtQ3aA5'
        b'QUPPlSKxQcASAYqwKoNzfzdjfTA2p8kFC9gr4FEBSj3N2QbtikWQqcRWE3o8WSBgiwDHsG40O2jDG7gfmzWpouDrK2CeALuiJ7AbcDExVEkawRxqBTwrwH4V5rN8JmEV'
        b'XtdkSAQ1nBCwTIACOLeJHVxFBpgKFjG3BEEVZZHpoBFYs6nSA+l5nUzAE3hOwBp6tlA2k5e4bSwWscrAKTNemRED06izkgdcM2fN1OXsDs+lpuDFCD8nekjAj+9KLPA4'
        b'7DfbCtdxF0vVzyTDC0vmb/FypyegRwXMDMbLaXRU4+FR4ewQeR426TlZtRA3YXPmY6VXQISpMBf3y7Fl3sS0HuSVGZiT4kVbY+9wD1Iq0mj009XQZo3UMc4NGt0EN/mg'
        b'hJ8fPHgwea2JoJj1nihMj3Le7pQqMMpbOIDZmwL1uWCeHyNeL3ajBLX5JPsIBzXume/nT+WtomDchVlM1AqnlZMnWi6NmMmpc09DSTp1C2l/tEhNR9FGbCXLR75bqLaJ'
        b'Op6M0wF0Eq5a4AW8ArVpy+kaCpmxluSFUkvIdFeYYOZcPCLH3ZGWs237KSaHw1XSjkfwrM+qDWZxvdeb4zV5hgIKzEygJtQCzuFOrHXH65vVgzFvkiselMM+bzWR6Ubj'
        b'gT6wfxWeT5tLy3qCnuNSo/sOS8FDIYVzc+HCIqyU09MLqHSEbLxOxPvdkf3jt0EDZvaH62uG9ififhHkQGvcZsyWeoR6O5ByFA/G87N6BsM1rGaLBxtmo7b1E0eP3CsK'
        b'NlFTUnwHCmzELPeN6M7cu2RyaIfzW0rfq+XuPYOXlCvhOJxiCUpj/YUSGrUcFeUoC0oR0ih6HinMQdxJK3HATFBZkAtoGTpv2Voog1OkesdED8jCuklepE/Ko6AFT+HB'
        b'uaOwZhEpdWavSMiKhbxVWI2XTVfDNZuNaZtYKeH6dDL1DDAM+7kEmNi6w8le1LcHGtXkv0ApWczwkgdcjVSLaVR/ycDz4+kYIJsH7vZ3JusEnQEH8GxvhcydyFLlfI05'
        b'rxkSqGcihkNrjZMR66iIC9QW8dDolOZJXy9Z28voCXioDK50PgAfjs2kdHTiuZCm2U0ViJV2IhH8d4ve8/BoGjXEQkG/iU5+pN2KgvkkcAvwdwnX+p10dXDwI9plMp37'
        b'c8JHQY3LPImwMdJ6Ix7wSoukpbuIJ5Tc9wArl/iHab1QtAqqX1Aoq6prmCIdW8P8AoJDnF1C5nIOZ63bA3V5YIszFoX3gDoVVrNB0He6RJA5iGSURTnXzkwl2yvDwVoG'
        b'NVC/bmWgq/ZUSoHnJJC3ELPTwtjs7qWICFUHc/D9ufMN+NUIcAIukIHfBJmkb8uwaImK6MqXodZvCNz0G+IFZ8nSeAF32MIBOB7FdhI8tgguk0Wz2dpMgRessTl1fdo0'
        b'K1Gw00hDyeq5j3marIabeCgCK6djgVeAlKx0pwT6P4vTQZUthdOBapcxTkxlDyFlc+gaDrFUpYAsUqAa5jKDx2AHtm1wiYDiSCymZEsmjiIc9ILjfDcoUI9UphP9eQHZ'
        b'5JFsLydHJ7P2CYMzsJOU9SK2DtBgsynZ8k6LLp7QoO7B/RaujFyNhUGiEI654ngBdyfFsfzGqvBYYBAUTtKfByoXSfDMcLjJaqfBnJnkNTjqqj+/hkNwzoUtv9PlEnoS'
        b'vIRsdZJlolvGpDROlZBLR22gjR9n9BkkkgmeiXtYMbE8AHaQYeMuYU4r0CQTLGykvUzM0obT2jUMGk+GvJpZD5z9rbGGHmQGsnRGQqZJ3FIs4qxV5Suie2NtYAdgNNwv'
        b'gUozaGH38RKWYKaTgxyydQeLFquk1mRxKGdTJB6rFwf6k5VIT0g0APexPRoOJFLXHJcQ3BM0c40oyJdKekWQHZcV/sBoykvuinXYzIi+x4rQiPXkLu2asYtTAl1GwyV2'
        b'h1S6Rg1XWJKmS/E8SRHaMJvdY9zgxzPYEPPdZuekndZk7FKfH7g20EQYAuUmZmRe57NR5Gm/iqwCTPmHfLf29mGNEy9hzRMCO0yxZAbkcVPAHqzFIlWqk6u/s5qsTWYT'
        b'JFDnvCA+IatW0GwnopIycZpPxNXES5FvT7e5NmmQusA2drFbwLYn7w0LrU3/xNqvdKhfuLzR3tVvurvDrdd7uMPwBSY21Z45ynum4Z95SXo3fmfyhzD/wKTn/Ie8+/VX'
        b't7/6+r1S38aG4f7hLY6yLyNfPPOc1z8DPnb7dFD8oLpNDgG/+Jct95u1rV9J9QeF/Qpn7ngw7V6R57JPP3nj1MnZLimeR0r/dWVsQb8Dz3/2dI37zmlbDj29+OqFv2cd'
        b'D48b+sDq2lN/yAc3H91Vd+rga2dij6nH9lv20+z5PZ5qqbVyvP/OmG1q9bOpf/S/61IzeEnE+Lp1J/518s1NH/8UlfD27V3NaPZtyrczK9eM+E7zTco/r02e1TM5Y4DT'
        b'L9UFUaXJKKtb8txbm2PaxnoNXB/VK+rmh7WKhkt+9Qc3+URlOZ7xeb3RR9z1rvf7F5ac+tLx9yDvn3otk86vW/tu/Ocv9a/O9347L/HY6gcv/D4r8eLfbp0PXnlnqWPG'
        b'PxfH/Lhk5OzUZ/5ny5fPH/na6uepzxw64vvFjwGfrPqy/6Jvw3N+GJFUNyndevY+q71PxK2aM/XCm4smFV9e/sPn5/aGJ8tedApy/+fXr9ydlvLMin1J8ZLcqQNdXh96'
        b'8MeBK7/qM8G670/X8gb8I7WPJtLS/bBp3OqX33pxi98z31zc/K+Ar/rj8Nc+sZ54LOLXqeNvXcw6Ht3v2T1nEgbfTP7HM4esnsl78GaL4sSv/fd4/JER+Jw08p2aUS3O'
        b'aT3alh2NW/PJJ962PuVb737/FBzd1XDl6CCh9KtjBemrzr36cuPhZ4ds6/ljsPDJ2p2TbmQ+M2LZrZxZvWu+fzb7nbHBu9/9yfPYqu+3vOWS8OnlspFPbk488I/nD21d'
        b'aRL35M5Xmv3SVpw7W2lXH3tl5OTerXj3tdFfvRb8fcjoaQ9MHlTKx21rU4/gzCdF0AYl1D2jeTPdIzu4ZziOTaVLjNWGUYGhLkEryEaWLs4IwUrOJ7YvbildeTZjDl96'
        b'sBwuMXcBLzwT1okaXsAj0MLdeSowi/OAXQ2CK1gKN3SOcURchBZJukrDXCB8YJ8PWRGz8UbnJRGqIJu5gwzAqk2koBGqDkviRLI50JenQyXsIxpob7yhc+Lg/ka4y5LR'
        b'tQwlM7mG6ZLBKZDL2VNmL+bcbgVkfaokmqqTo6saC4iyZ7aQTNuNW9nd4HCsc6IUfvnOuGM5WZhgt8SFyG97WZ16kKW/hZLdwE5lgJZqj3LdjJZwkrTCUXLqHUJFltB2'
        b'uRVyN8uFwYEy0kaFmMsqNy0ajzqx7DdkCCSTUxIv3IdXuMdQpTKYUu24YO5qrbNRlJq5UPSgBDsaKFasn+BviRc01Cew3f1H7/tD1DW4QfS3FtZXobHrnTo7QdhCAxzx'
        b'l0I1WfqyuAPP8X6KQJ3hOZS5HfUIGYi5UiIW1ml9VqAWskKBiEgFbvEDGZFcoKlgHSpdDQct2DDbDJkrnUIxBzOdSRsXsvtKvCHBS/3hMvfiqcCqUFK0hi7yBZx1ZWaF'
        b'vuNDAv3Jm5f1+8XiIJZ3XIy8g/+ZhDTEtYHM/8wCT7P+7uUTxJx2ioOwxpU77eBF71S6rA8ZMxMKrTEbCgwYJTp7nVT2YHZzPDcnvKvTExyaoHV6WoNXeWcfCsGSTl44'
        b'dBTjefd2J5xTyXwmHLSIIp0d4GfppOfty5QmKaCNt0oOGbc3iJhM+pY0GuMOUiZK8JDPbFY3rPafQDa24ZCn39fGkL6lt/p6YTmRAbZ4tcsAa7CONdkErIAS0qfkq7mT'
        b'EAC5A1KpZziRHo6Tzbt9nyOqbxc5gHTFXpaYeoCMlK/d50kkQ93VHnfJbJNTU2nMDV6z7W3Y7NPF6OPgoTP7DIbrjBDQDi9EBgb52+MFsvqEi47r4Sx3gdrT1wcPWQQ6'
        b'O3QgBISbkK22+Hecc9QD/oOgtn/+R7vt3roLhiczbX1MfnQzbXlSk62CEdnYMEIl+QMJ/ZbI/2DfUgsJDUiiYHgcws6ePEuflIiSBzIphcij8OoyUU6pcBheshX/JunS'
        b'K1tyRd2MbBlNoQ11NyJpWGjpCclvcsf8gUxioXVgsqJ/SanjkrlEIaGQvPSrHcJXQlKRsN/8Sy5KvpHbUzIeC22KPIRRb0Lr0hTcAMg9lrg3EQtJc2LuQ8xZKXZDu0ND'
        b'e5RX+ylGr/9aj6oVHUo4RVfClF36QjnpnZ6Y1TGH/Olo1Or45syH0C8+rMnUIgt5C3nEISs9ZhUZZvGfO2TVOSm8JTHgpDAjLpVSLEYnJDB01g58xqSQ8bR00QmdQFs5'
        b'0FdMDEcyjFYlxmZ0S5S7wDhERc1Zl+qfGBcVpVqRkLRyrdpVC7Crc3tI08TGpSVQ34ONSWmqjGjO+xgTT6kau3MtdyxEfCJ7MI7hD2jjTWM1PAiVoyuqKE6UKj5G8/is'
        b'ihQ2YaLKn7kfkNGpiacgtiQf6ooQrVqZpklNWseT1VfNPyYqSk1hdox6bJD20bUHvYxPVKWPc6WU3jNJM2bQxkxdHZ2qL227U4jBFLV1Y8i6zMuJu16QBCjObqcm0oXz'
        b'rkpJSktm8HsGUyRVT41fmZYQncKdSzTJsSv1aBAalQMNqncmTUCyZWAtG5PJn7GpK13VrBOMOJfQBk2N1fWLtt+ZE1piV/pMbe/HJLFg4mSKyWwozU4d8Aj6SVEwRD9p'
        b'HsIVwQrY782N5WR7y55JjeUabOXWcuaGewzrwg2FS8C+HjReIs4zLYA8NnaoLZEbwuEENSWqFFJqr2xb744V/Qb59RyxfiueDYccOO0NFYtn+qcS/fYYnFNMCXEeiFUk'
        b'h6pZcHXwJmiycZ80nBl5EidRS58glK+NCkhMXCYw7R8LwqzI7h0QHEFZhPfQkJv8bXiSbPymwtA1Mjw5D66zt88paGCGoJjoH2WRvNVdiD87Yr+JhoYlHl793ojnr1vu'
        b'dLfz+fDXIy9+K/QdqnzpnElk/OrEHUE9Jzj0Gv3StYTopH7D2wr614Q+M1pllnMwzfTdXW4rkvqNnjrfd3vl9g8qvC2OvrfE0XPmgaaiwRbrL74QGn3+5/Fnxrzw65ab'
        b'ilcbPX5QuJy0KmgcIR/93eC84f1rf/VRK7kPdjYcxCrmbM5VGSLF1mvVGVKN00yo6IVZvtowgcMuRKXBQ/GpzCK5s/9yY3LK1v6Gj6fq8AjLGK9DZpiGmlVdHPgzcAFO'
        b'SYlSUCKFc0lRTGpxwkNwgcrb2Dilg9KT7MzujqVCJvXEp274WA+tzBUfr6xi4m8q3uij88QPwjNbxdlbp3FiyhozLGcqgYSIRXiO6QSJvZj0OLvHOmW3oAqo81JM3c58'
        b'RWZCAZzpKs1Kp+IuLs1CQSIjocbr9nC6mzSrE2WvJuCOoRu1R3CPdBgxoxGCbJoyGcbRkAyzXRjPJBcK9f+A/JRSCYVKJl18A/RJdSaHdO28vXdjtJTwJ9q32TzyZw3d'
        b'Zl0NbbOZwvsPCYA0UiLqTEp2m+Vku+mEsaALszXmhijNkz5WkK2O3/hnmYE9NiI2UYu/2hnkPU3D99xYtuqRJdpnpr93RAfgdmMbVeyK+JWa5SsT4kkqnAJYh1gVRxEo'
        b'V652ZU+4+tCf3uwxY3jwHVLVts9E5rTorPdapHjFmlhWzKSUGPoB2QIMLtFafHujZXCdPTcoimHWpSUnJEXH6GqvaxCDiVJQVD0GHd09tH69mrT4VI4yry+U4Y3jkaXy'
        b'9o6Mcv6rr879y6/6z/mrr85YsOgv5zpr1l9/deZffXWBj+dff9UrSmVEvHqMl0cb8Rv1j+OkN1zYiY1xVjlqh79jJ+fTzt6xzD/OsHRizOd1dko0g/5uH8N/xr11PpVn'
        b'+aqQ7uXq3mm2MLdcDrjLpxPJMD0++q+11MzIuQaK0E4RTtcYXg4+3eJjHiGCyYQOFLZ6EawnZwA/7y8XNvQfQE/jg16d7Suww4LhUBGJF7BMo5RQO4oAB5RD2emJN+yA'
        b'LGx2d3eHMjMTQeJPDZgVcIyd4eMBLIfjTiGucNCDHu3tFQOhcCQ731m41N0pJACbIFtCnf3E8an+adT9xAcrY51C/Mea0efzxMkjfdUyJhmOwStD2NkWZXjuayJI+4lT'
        b'oGocj54+NCWA3DuXipdmQAMNv6sUh7jCFXZ2Em6CJzSeKVgxmmxFSQJcgrOkeIyKeyFWE+HSOmUYlpOiY73o6LydnRTBHijx4Sf1zumC2wI7Vh3q01oFdeuY6wH3O5Bi'
        b'mdabcSrkxmnLNwFzefmwYhg7iHHBa5CjLSAWr9MW0AKrWOnnQQ1pWFoOG8zSlgNLcT9rj95YMpeUPlClLfwYU7WU5bcQy+C6NkNrS21+Vfbs3uJVG3S5ZQ7Q5gY1C7jj'
        b'xilsWqNMN9MMxyaZIDUT3ZLWsh4xGZumtEyxxv00Tk7qLE4zWcJemI7V7vSgTmk1v68oSC3EaZND0ihmYgJeHhZIJd8I5tBLT32JDEzRWsq2EOG6CLPhGhkKVZGQk4pX'
        b'oQKvYS2WEQG7Aq4R6bxyhYkl+RFMWqZosqonERJtraFhBWbHq6qeFDQUIPSu46y5L00KedLdRv7BgfU/lm6Vl5R83jDe5JIfirMLK1S9h023szJRPJdqV2EX8swQm9rA'
        b'XmPGmH5gF/mbf+ublYf+Z9zNZy4Mmx95vuxeedUc77CKxGdDpI2v3XMOu+3bNGvp17fX7hrzyvmQ9y58PHT+whcsTVudDtf3+PGjJ/rv8P94dHzj+tJXRvsln674+GZu'
        b'Y/pnN+d80jD1at+JV0ds9vHc806K//UXX96a+2J6gvhr5oum3/103XX9/d6vw7aXFid+VzHv7dd8ji56/d7MH02Xfxu0xPst89Xnt4/73mLTue2Tvh+wafznP5Tav3vo'
        b'amJ18aR6321PLN9bsfwPaYnD0ufTXlLbMWl0HLRha2CHSPr6acyqPx53c6NeA5734WG6i/GYzqzvC9XMUDoOWjc5dXB7dgy1cJaa4nm4zg3jV/vPIEI9NkApP6iAE5DL'
        b'PMfI5N2zkkIJ+MER3G8iyCBbxJ2b/Fiq8iXzdGG2RHeo4KG250kX7+Pm151w1R5PwcUu5xRwYgIrcpy9I+zGXCdq76fysAILJbCjD1axnNOIElasUWKLGxbRs+JCARsw'
        b'C3cyuX0GlI2HwuQxarxA5gHmkskHx+EqE/aTFiyht6L7yskdMvxKR8IZLuznLCXLD7k1Fs/QFPMFMvqyw/hJThucx1xtnKs+eNVXJp2Fl+L5mc0N3D1Wk27Vbyx5F+oF'
        b'PIS5ISxdKEscpoEiyBu9kBamhPoWHMRM9pZVHDSSl6aQBUqkbk5VuAPKeYdlYTVcJtPcgvxuoXALZwQ87AHFzP6chBehXpO+Hio1NLv99Kjp2nZWvw1h2ETuWOB5Cnux'
        b'l6idq8P5WUNTgksnLcoWd+qUKGj1NxKa+RCnZ5mGyMJM04gyrGlEUc2CWimZrkG+Zcxyyq2eEqZ16L4sWOikuURnl9R/kzfIsw8kDzb16Oy7TPIO0YGzsIhKi46SdEp+'
        b'J0WFuRySuhTplZN8feBjIbm69RAN5dZD/Km7l4noalQnYQFfIereXYCx7siWh/qH3FEu954bHu4T4u3vE8HRRPWAWXeUydHxibqISBqoece8Q8ggM3Hqg0U7xHVmdQbW'
        b'YjhbOaJWAWN15I3V7/9LtvcUX6od0qDTFeQvhamNlI4Fxe9yuZVJn+nUti6T/EVQT5mNjY3EihLNyYQHYzcqRLuBCpFBY6xKcugcj7AMC8iK2c9XFh8Ald2cdi20vzWO'
        b'YmfeOYoGxpHAqmRaLDB+TRHBzMgXvabIYBQXjH/efm1DYTljerJru5he+mv7mN7kug+77hvTL6Z/zIAqJWW0y5XHiTEDYwZlKygsaIVphRijrLCoUFTY0q+YwcWmMR65'
        b'FGlMTvTd4TEjGGqWKWOCG5UtxDjEqCnTHX2vQlkhiZOQt3qSb5sK23j+ly1JzbbCrMI8ThbjGONE0vOkKGY0xVyzXMtc21y7OAXD/aIpmzFPWTnznO0RJ49xi3HPVlAY'
        b'UpmwSMn0Z687tnRyeDM2DIYbFxebct+zk6TZ/QEtkVvHh+67ErF1YrwmaaImNYb99nR39/ScSKXfiRs0MRPphHF1d/cg30Su9lJL78hCQsOD78j8/H397sjmhvvOaRTv'
        b'SGb5kJ9mNMvloSFBCxtlKdRYcMeEaZt3zDhscDy5NIkjOrPmz2TrQbOVpVTQWVZJf+yl81bmHxLBwST/ZFoTyJLWOa2UapZgxKx5M+7PXJ2amjzRzS0jI8NVE7/BheoB'
        b'KTQm1mWlNpbQdWXSOreYWLcuJXQl2oK7pyvJTy1pT79RwsDLUpZTfEbSQEGh3jOClhP14P5IWmjvmf6shOT3nOiNdJkLp+ZjTSpJ1NV9NPlJVjyaWKOYEswhHg/SslpE'
        b'+If4Bvksnzkj0tvvMZPyICt0Racq3x/X5UXvlCSNZibTWzqnEZS0KliziqXkQVOStKdECthA07Lu0h73+xmv1P1eBhtPreyUCh1uKScNpD0h5TT9tEsiE1giXimn6D3j'
        b'mXvcd/oTNb1jGhMbF52WkMqan/Xl/7uRItzP7CIR2/ek405lupXOlW8qXo0/FfsWDyL5vtHdZgMNI6GxmzIHUd2w5iFBJHcUlEo2lYxt4/FV9MuXA8B2XlNcde8aD0G4'
        b'SCoyhVxp3A3LAJnCUw8JQ3hYno2mfM+ON7Bxr9Xv3nSsfkHLFBnSLXDBXNfG9KCCBS4IOspTDu0WZ64PSjB/rKAE3SFilqkBA6c/jziO3xTbwczJOY34mRRdpR9i1ozQ'
        b'cQ+rkhnDBBNkNBO7P+ii6jKTVA6zfNQPf4zOxEc+MUHl4KiJpwdc6eNcxzo+RpJ8cqscvP0e/bB2EtOHnVWPysf4AqNy8I/8U294POSNx10raBJdC23Mgqy1gnFzEQ8G'
        b'17JZ6ZgSjL1JN1T+Wtdhk5wSn5QSn7qRYxI7ONJtmvKE0Y3a0bBR0ZFu3/QZupk6UguyI90FHdWu7WewY109Xd0nah8xnEz7ca07e1SbavvHY9nHPGljFeMAFtqqGYCn'
        b'4O0zSsMQKow2DzvDmNgZTYBNMsNgE1o0AKNlakeUmKhnxu0OGkEBHPQn9gYO5Ok/co+RGlKjPjOmMm+B2OhUOqA0Osq3Dhgc9LzaCCQBNciSdDKiU7TOBR2YNljrqCJi'
        b'Y2ld0xI6sMgZTMp7RqSPb2j4wuWU0ig0wmc5ZbOJYKXUH+xzbjujjcQXId4+jH1KC+mi6zedAqc1JRs+B283L7MjC55Cu/XXscua4mjUk4D1UDKfpxrOjNdliXHktdM9'
        b'Ep9oGC+Bo3MQkVVH9Ls6OlHlMzfciJk8URWREZ+6KTYlgXVc6kMKzxdEI3OJTBj/1OiEjexF4yuco/Exq4UV4R3SjjZCR762S/TII/zEykiNUrljRAfQ8k7vdkKNMbpq'
        b'sZS6HSGQ5tHKVRrd8O2SruE+0ZJFtufLSDpXxCYkJa6iKT3C1E4lFLNuQpW1VqgqFsKwnPoWlkiF2dESrBEdbLCMWYXxJl7CGp0rhLz3TCiWWEHmzHZEUMjEQjjK4VBx'
        b'tzDKEU/jVTjLIn6wEWs3UK0Yikgyl7AZ8mVCIF6zxGwJFuKpiSw4LB5zNwR2jPua1y2qZjLe7IwcGmwSIBHGwE4rzMYqLFJLuKV/5wy4wa3EotB/KrUSr8LLzH4cDNd7'
        b'UsMyKfBpqKKGZT95GsW2xRo4FtgBH7a9IPpwmGRLy3CKD+vgEjLXwQELsMgNC5wpHCg0OuMFaPNjwXwi7uspzsLy2awsKRvxqBbIlIKYtq7CPXByMDvbsOsnp/q/jXtc'
        b'1NjUDCuBxT0NwtL+enDTosD5fhSaL59U2S0c84LC/KDIRxoO+TRaDq9A3cYRAtyUKXF/YO94uOUg01STNPpvPzii2MN853Qbn1Xpr78798vpd5ao16lejIpWZc89ZTfc'
        b'9ucvUmTXs0bdTnjF4tpPv2zfJLnlFhfbR2Z37tkPSpJ2v37p06+zP5QftH1rTM9h6V49nT4pezehasTgjdUbvlCqy3LW3t5hv80za7XX1NH/o9g+LnxcYObNtvd/eH7S'
        b'O/1q3xm/7ZtRfc7ub7Uruxu7+4uVdb8vXfru123hJ0yOeeV8qnR/2t1UOVltyUyXvfHyeidXF469WLsE8iTuWA8NHOvt+gQ45AoHOC4zxZJ2pv4cpoJVuNQDT0IZM9Om'
        b'OoY5hcBZuNnJxDthBfNulcDVWCjERq/QLt7xeHkLNzzXw6GZ3J0kXSQD5uAMbB2qQ47Mxn2Y69g+HrlHOOZz33u4CY3DlYH9cX834MuMQPbEWDIdLmBbz65WXeksuBrB'
        b'4P5IL1dJOoEbumObHt+QghtCMezhrsZVyxydXINndwWjHDWV28kzg+CoDiXTF0q5+T1kPjf1nsIzeI3kQ2feRamAx1ZJg8XZ1j24WboNj8JlMumDSCusEDWwzwMyYUcn'
        b'ZArzf8sIp8fKm25MrdpiS01xUu78SmFHZKLigVxCf0uoEwnjcLaSSMR+RpQhLSqcFhlnlWjIsJzQCYou+KHaWMugP6mN/RlYOs5UeMdkOUPmM4aZVUyuOCidoQz13NGu'
        b'jyEHdwWUoxasCL8Z4XdklBn2joySxKpNDTngcvdW6u16x1TLJZ5yVTQQ/W6t21MiBX30O1cjLbSKpCVHCc+1jrP+kzHuOn+ZBkPq5IyYGE1nRmzddmrA+KcXxLprpXGq'
        b'iVRMnBilBy2JMnC476wVa/QYXNSdsrv3aVd2R05uTDX2dmE1lbZmqlaUfywlSSve6vl/H6Uncfov/q4Bkt5ojSouISmaGhFUjI1WS7dpzLMmOrETtV1Xbl9jpeikPBii'
        b'3k2N3cAl41Q9W+067gpqxLeTPBMfQ8W69qZoJwjkdVA5MNZ6WjUmtg0Nn+3q6jpUbUTg5P4RzE85mo6mDpzV+pQ5KScXhNvvG0xP/047x6Z2CGh9tzozbhpMwyHcZ7YP'
        b'PcLxWR4yN3imT7izSqefcFpSo/5ezDHZOD1tUjJ31H5IChsMqXxGeGAfkhz9p9cIaQs/TGHT48JpR7XB1HSk44Z0OxVpFZ/wkBlB3fU4w77Mj6nb6cjCeFPo6ZrpgNWO'
        b'GzoviDocyxi5o6JCkhLpSvEQJ+8Nqe25MzJf2kbRCdSxmi4Q+qEbl5K0jjRVTLQRb+yENG5CWxWfHpuoG/lkasZQPx+HlUmJmnjSXDQl0nDx7FPSykYLxpPpaHhQd6ym'
        b'lrx6xZrYlal8PTCs6kSEjh/r7qHidLq8PrQMzlpkUW19mSWAzk2yKBpMJy4thc01Nts5La5RfY/vTBNVEVr9SkdmT/3VN5JcEhLI5ItO4VoWf9jw2qLRJK2MZ52g1/aS'
        b'U5IoJz1tRdK02s4mE4EPe8ON2YHqURVC9L7o5OSE+JXMA5Eq3mw+dfS/Nzx3vPmaEd1OLUs3bZUD+al2VtGtW+UQOjdcTTuDbuEqh5k+IUbmoWOHgIKxasfHCHPQu3PN'
        b'0C/1XRiaHuYm2knpVBhUOgeH8Ij9c9CKF9oVSwkFHbeCk7ifCURMT3prHOXeEPr4qqKCPHv6c31TBsehnqqbg6GcaZxE38zHutlcGd03Bc7oHKNm4TWKg1GDRfzeZQsi'
        b'mDMwF6L0Ecn4IhH3U2ZHMod+EW9AawdNtcmMK6taTbUJTqYF0hqkIpG3ORkEHpkcSRlDIrXYBIEujvP8nAPmGmW70DI2nPXpAYU2G5nvl1OMgqqrKXCTaqxUX4VSx7T5'
        b'tPEkcFqX02NmQ7TmS6RRtaQ7YQ56yAq1XJjobofncI838+ayWJmitNyOJ6g2TDXhQRFpGVSdx+opgQzDxyUglOrCPAUTLMMc8xF9odG8Xf2cjjuI3l2Gx20hB2ojoTom'
        b'DPJnboODkAUnyVcN+b1r7QYogfqZK5ZBwcyU+LCwNcuwenLKiCVwYO1qGwF3TxkAVf1XM205PBCuK7HVEyuSLSSCBK+JbljXi+GxEPWvEmoDKeOQaLhsmN8X8qdD6QrI'
        b'6VSoHDyOFfSaeoJFWWOuiihFYT36hOM51vpwDc9NUabjvmlmGu6EBjdHpUVTNQFLXPU2AfU8LWJPclpaJJYkW1pjWaS2zTuYC6iVgHYMVEzUwXoUabFtYAc0KNJpJlaY'
        b'Z4+nfYalUUpXbMCcgO54Sh0QgxTLoZm8F9mpL7EFci19pW4cnOQSyeNUYEfWpWI4NYeNGJJqIIMYWbqeDKRyE00AFNiScV2A5eFEvy4Q8eZ6S1/SZDfSKHcgVuDJVd1S'
        b'8muH36fFhEOmPE2aIuQoocJuBNb3ghNQZ99LKsCB4B5QRwZHNashXNkGmQagkCR4jORWhBcnw6lo0kFZmE1amPnkQdkKAXPDLcLXwVlWrIlwAms7GGiC/NUBLq7duVGc'
        b'hlBLCS+YZecJQ9rscJotlKaSjqeaiv3MzTpoiDDGE7N8wcPTfkjK4QF2pNDnOYoHHMfzeICZfQbgXm752TMAjzLnHY6Okkeqk+2kI++RLetE3zNQSZki4+PGrBE1dUTh'
        b'cn/QMzjsesg7023eG7j5+o1Jv2ZKrRRh5s9PloVO77UpZOYw88Vts8ZW2305snftjruDbn2jvqfIKzD/RHQI3ZidV5b0U9Gsjw58u+ppr2bPigWvZd1tdIhZuOO3f/i+'
        b'a7u2fnc/E7teHk67Ez+fPmbR1KFZaxaltL0aPHz9sfHpL5ss/fJuVXDPv98c/6K//+uhvglbP7ZLuHuxpuzgguNjv3jtp0/abIs+3BHxRlNbRv2Nmxcnz3qQ2mR/f9/s'
        b'sR/02PRbzo8KF+Wp9z46fXREfO7htpbvkm6V43fmf5+24elbKzfUFDU9eOLQoL/flL8/zz9w6cAJO7+V3Rm+oWbFxdd+6PGv9Adv/HTYbkvGE31POhVfS366xtN845s9'
        b'35pw+R3f3jWhO6ZO2nq06MW5n3/4W853czJMt77x5baCTb3WzPtw4rKlP7z62461d0LHyR9kXhb/MPtt2ftbT1/Lvr3WafWv1/e2Htry0i8Hlj81+rnJn4YGp1wZ8ZL9'
        b'ayEyt1HD/GNV/xhxeN2pPqtWvb31kyGOjRNvZUcOvLn8Ta+yFy6/+8W/JiZ/e//wz15nZr1+4P3kvbmH37htvf3kwk+/auz32zbp2MILHh5j1fYciOBc/ymBrv1wZ2fL'
        b'UZgVNxydhJx4KMzA012tUiPhEPOwi/PEq9QoRSZGA3OHDMcbzCiVgflwOBCv9AnqAq1wEk9yM1AWlg4kCTqP64itAOe1WABwfoOehmUjc/5LteQ0LLGYz3wmPcQ0MroP'
        b'Q7lzZ/iFeNzLKTCuBkO+NiwJjy3raPWCswNYGWIiVJ0cLjPgmCR9LnB4BFky5lJ3znWUCIQ7c8JlOM6Mcavh9DCKk+sPp2SCPEEibBi63ZQ1CNZbmjPOlGgo5XgVmRG8'
        b'OEfgYDA1oEGb0MXEtgdOsWh4BbmZp7Wxka2+sguJCDWyYSPksdqPwpyUQFsycXd3DqzPgYu8Y/OHYiY1jx+HM86Uu07mLEKbhZYIxZcIB0edGF0M1ENTRyvd1imsabbj'
        b'Tixvt3dKUuCAO0ntKgvUmrUM8gKD/CG/S2S9NGK94A6X5W5QI9P5iuaR9bEwFPaFMfSrUCJMWM2SToEdpBdpPhPw3ChdMJp8oTgY9uApIv8Uc3vfFVNKMuIW7KImpZgi'
        b'cXNVQSU2qxWPHQht/Z/x1cvRwT6WUZnRkJlwuzDVXLSQsJh3iYVIo+VtJHKpQrS1seA+oFIa/U6JN3gcPI1ipz6fcm08u420j6QP+U2/7Vl8PKXhsBMVJlY0Yk2iNUNK'
        b'rGg8vah4IJNYSXg0u1yyaagBM1yX4OyQRwW0t9vTUm50jnR7/ObvGId+w0AwuoE49BJq7KSgaAaNnZnCPQfj5s7HqLZxfyBqaWVWQO5KIsTJ9Z5B0j8Dmn8/qpuGER6b'
        b'SJRbzaNMfcyuoNVlqCYbrVEtCA56hMJCYy4GdVNYnEO4sFY6ZW1gB65LBk/XAZuucPym+Q7dIFGxCk5b9toCB9nmb2K2wAlPQptB6r6eeITJEGIGnuQHR9iGjVyEIHL0'
        b'5TRK4TQVT2I+vZvqStZg13TyI4B6sQ+nYDTLTMZBkztHPMtePIxmIBOgYJo4SICSlXM5uWCJg4f+sE+CNVBKj/vgEpQylcs2UULjcvzmi1FB6aELBBY4stgPrnlhiZc7'
        b'1ZMuYS0eoecgZzGbY6RVmJKPyqX2mCUIboIbXJzIRPo+RAU4pzQjog/sXC1iI1XUCrWRMkenknZSO1KQEwrys1EkEmMx7OB4YRegDnYE0t0mxIQU7Jggt5dYeOAFJrMP'
        b'x8s9IkyILlMsoyxhNH62cRB7b0AS2R8oCiaFk2uAiwxSDjKhhb0XjZl4nR8ASmfZEaUHc8kdujLGxW/XhqnQGJWykTRMBU85cZ2xHA5HaMNbTATp5hE03CfTlKU4jWxD'
        b'xUpGGSlNwz2C6OiOPC9snUeaVXsMKfVfTNS6BX4MYc0ammZEQDFWzKUAgHODxYwegiJUxIsBE1nzp0/cIwwQhfEjx0clHl7qw9Xgz+cPFWaR9pwkRK0YZe/HP7zgzWLB'
        b'F7wdGxXwvjBe6EYIrZ+MdOAxQmh7Mv2EamGLGCPEiDmSvsIxHTU05Sf/gmoTlDZnRkxKUHxibKOWHFqWQP7oym5N7f5L5dqTirRZNCt/OMv8n/mxpZlWQsa8LS5YxoIt'
        b'xPCxE/AKkWXyJ2BO+vTZcev9U7Ylwo6BwhZPGzg/F5pZxXCdpUDGiMOZ8KgE//UyXtul0+0FZ0GYfsktakmYdLDAT5evEnWzUos0COXDdGCDWqjBsjDWhXK4CoeIasn0'
        b'yhFE5aKqZcF81lHLiVbVSu6ttyRS01K4YCdO8khiGb7dj5ke5nzoHBV0cth4QS1hYz3SHYq0g2hKLzqIzttrT5fzI5RMwZNi0SCiSK6CnRzwFvdjEzaTd0wFqQccGSlO'
        b'Wa9Si3yO5gVBrSaECopDAyVKUYVZa/+tbowj3Zhyi+4DQH88KQrdaMlpx53WdxxtnxAvrCE6cKu1hJT9ElabiePxMh5i1YXjW2OUWGNK1RcyneDA4DQ2tS2th2GzBbaa'
        b'CsF9RCyn8+wY0bDo+omFMhMl0fvIWhMmhEFxPHcjaEyKVTo4OuF5T6gMEgVFgGQRtsIxtiTFw3WilboF4KUgEfaKggnsFHEvkVbq4tef9pdqZpOZvn/e+ti5gXvs5trd'
        b'uHTk94YvEvus/jx6/47oAfItXvds1m8pLph412H8UM+GDQNb/OoL1nh6fLpX2a/Fz72xz8qiIfVrfIuUvc8s6PdR1vsfuKmcF/S33/ZZZNoky8K30/7209a0v53W/P3K'
        b'4QX5r5a/+w+fYzGhy8ryP3rh9pzZrivD7oz8amrirbEXLXY3JzlOyj1tGfpkfYpicW+PoffnVV/sVbUzdmdzZf9J+ZGVR4refVIoqJqfvfflv/uXPjX39SWOl4ZVN3we'
        b'sGTp2lFDT0bN1ZR6zU5YElxlUnrHKeOfB8/Etix5Mu3rz+9H95jU+8vp16qGbrjz+iD3+fObezy5OmpM2otJn9j+Y+Tcjz6LixkUHBsZ8UPkriP3UhrrRoX3Ddrx7vHZ'
        b'qddd5G8OiVo813tz0VuNX7mumRGUUXrDtuDtORcDf5j/RGvjpxvL15WuW3Uz7b3pN9zmKn+5eCfyaf9Al8sfZKyetGDlg5Uvn20y+z1pjcZV89zPDmuTZl7aeXFNxX7P'
        b'71yO5Tg8/Yv6wuHY2vX/1Cjfy64f+P7rcWtmufxc3vD8mYRLd2YWvKZ4Zuz9DxptN9tE39meqQn91auxx2+WqW5D+95a+HTcW7Zv3YCImet+v/P5nMN+mvyXf0/I/+oW'
        b'7Ky/PkNjedv79mSLuMW3hM21z/o77kndvtVpXt2dMxP3Od2e3Jb53d++fifzR49Tz5y3cvca15Df4x3xvuylnU/4+a/auOCF14pGRg28tenCBt/ixoE+iZFoEeq1yW5i'
        b'1Zhtnx3b0vREwLKYZ+7/0S/trVcvms59bfG9Xw4uPeppcjPzwOCqpr5L6/LeTRr99ppRx5cOS/u+/GDU1U+n7VSkff9H3pljnxVXbv9o9oovdj1ICG3y372+/JrX7HeK'
        b'Fq+1HPHPkb9MHuUyBQ4/GPCP7xa4ZS78oOCG4ssRMZcDrz456FS15cexm7KmhIy9d/D2bw0e1793/nS/y/c/V186/cH3c5IWv+y56W3z0LAk67R7Z9KuDTxdbvmHsuXq'
        b'V5+sf/LnD2+EjAnzcLocdm/c+M+u9yt4EDD0t/nnP3rjN58/pjTU3/C6fHfez9ZHrz8VMcH6x7QPLB8Uv2a12uq92hsjj4Y2fuj2YcXXmY4/2P8k/2b/N3b1T+62eulA'
        b'b/OqKwPDrQd8+esnU99zrXF5ueJfGvnLifsiVpju63toRGF97b921T9pdcar7ajzwTLof9B20s/l9dkHNtfXPrswJH/gO/9Uv+UdAbefVk94+aht3KfPTx3xa8zdf734'
        b'098+WBuy9x3P/TXT36/rqbr52zcRbQcmvvzTuffw+LINg7+0eN//1d8Sez7o22D23p7MMw0HUiR/vztyYZvJp46/WacW/vaa2f/sKdn67JHb64cFBj2X82XvP54I/qM0'
        b'5dZhvN9nafUG06PD4842iO++EXL13BdH0gM3/3Cjf4JVy6HaO7d+tdv6hfzLO/d+Xvjarn9Fx/o2XP88adzE2riIcZOP//jDqoGH784OPPWHxW3PxUdffXHnhujBuT7L'
        b'k14Z96PF/bpXS4aeH/NHz7qXKm///SmzsKW/W9tenrX/7ofqtZwHs2H0Ri3fylbIZZQrnfhWsqGCK3670/GkVquNxp06N5P5pkwtjxbhjNNcuNiNKRQrFjG9spdEEUj2'
        b'Pd09vDBdsHaXriIC4A5OT14L57Z0dBNZasq1WG9bVkwFXoZmnZ+IZnF3DXZjME8nf01PKJSt6sbEGWXNIyL32UK2FgRRhEy8qkVBzMMzrCJY4QtnNe2irYinegqWeFM6'
        b'fVo4h5arsArQuJKcXVJC1HRnb2Z+OZgvhbzhwmg8KY+AXDjGWT/DoExLrixCg5MgXy5xxHoHhuICmZNXBAY5ysnOZy9ZKo5bRArAPFXqwl1IX7gRYVrEamtSvD1kpy6E'
        b'y9wHphbKoJzjxvXAyzrouCA8wiM2Z0KbEvNciP5eNCM1UCqY4kVJaOhwzoNZ5SrX3QzE5iDRF2oES8iT4DWoxixOU3B2CzQyBB0pkUavpFN4WsiDXXwIXIIW3MOTcBkV'
        b'4k8yN5fMh4LpTCf3H0KEccfwZf64O5lFpO4JMRVs4Jw01QVuMOuGerNzICf9HIb7BBO8LpGmp7J3VViGN7A5EC+EKqHRYStclwtmeElChN+yqazfpnjgKQ0FlTQjHQP1'
        b'ChPBHHfT04gSNbvvnQGHacnM1EQcLgqUjk0gVbsm7SmQrqBlH4R5wMwuzOiyBy4zwwvu8mC93mci1NKOHDPEyVVt7uBIDRu2faSYCbsW8nZvxFp3pWsgtqrxWCoWkqpb'
        b'SRZjBek02pmD4Gg/jRpraGQIlQ0a/AcwB66FUECE+WZ/qCGp76YNz4AxTYQe9lIKJ2/LUX8q+iwJZBymWAS5eh7T/pAlg3rcIfJx0eS2SONKBEsL8oAAORGClVw6zRYO'
        b'MyvQFtgLTcoAl6D1U7ACTvuR8alRi0LfSJmvBhu5o9exXlCoscIsNS3kDSKWYM0MPuZrpFsDdcjXJtCE+8nUq5BOxmOk8dikaiKaVjaFedSCPK6fwmEepy3mNrc8OAfn'
        b'Nf6OaiI3mS+HCpGI9U1YxCEeqwaRt5uxujcWmgiikp40nBjNM96zOEpvzIYLkKk15mEz7GUTaBycnMEptmmvFbpQEEi8PJTjlfbHw4F6M5UTtnFL1XasYreJslm7SulA'
        b'GmJ9kHr4TAkZLwclRPytC+BjORfasJ5WKTgUTriIgpmHBPb3wHqtu5gj7FG6qh3xvDO20nIr4iXx5lDAzZe7MFdwIp3k6k/hlk2gAVuINlMsXTFUi13pCjdDSN7rQ8Tx'
        b'qUSEOyHiUTixndV5EDZim1JN5kczSRfqoZrMhP0itmzRYsMSJe4QUa53c+vaAqihBjbXCH7v3BB7MguoVU7qF4r5IhlY58h7tMxJkLU2kNvsoQz3yQVlgARPOMFp9qYG'
        b'cjW0g1KCQlxF3zmCpZtUAdemMdtizOAYUpjiLUF0YFymkPonk7VrETtEa6ZMDURBnk9Wnxti/5GkYzmliS1RYXS01P3wBDO12tuxND3hZAIX56EEs6hAv8CF9cv6obC7'
        b'g0NhbzzOLMMxwLsNiBLuxQvqhrsTRcF8uoQsQaexkm0Dm+AotmngiDnFYKUz1omaF8haJtiRFRj3BSH3nMTa0VCswd1qczgzF6toJ5Ll/AJ5rq+NzBFuxPFxTU8Uq2nd'
        b'2b0wjWAyTyRr1wGynLIzsSqoc+FM1bg/g1pdJ8Bx1sGJvn3pSU46Nst88bAg6yEuWwp5OgP0KX7OIxeGQZ4IR6jN4rCKt9kVmTvFLM13IDMF8lR4hNz3hd287qSQi0mh'
        b'HQIySB/cdJQIplAumQBFJmzkJEzoTX1iQ6mZJZ+ODqd1grVEGkPNF6y7XGEfnNBhgeMlW45YDidi2SrjifUZGrplQR7WBZBlli+UQh84KfPYAkdYEqMgP5Av8EFkzOIR'
        b'MngPkYvejtzsWrFtMG90NWkvvIinSP9giwRuwGVf1i6wH/c50m2atPT4NZJ5Iln7cS/rEg8sWqKBbLhEOt4M8zMoBzjJReiJ5VI4Cpmj2Lixw9YJlPGAbj9n7SgG+pp1'
        b'bABnwA7KSsVstpNgJzXbqkIxhxvHG0ZOV6ZZmlGtbR9WDxFnTI3mHXhzJNEqsYjMb1vYJbETh5E1m8/hVshZyeviv54+MAZOkn2+UToC2kJZbwydNlgHDh+CbXp8+ESs'
        b'TXWgWjjRD1sY9hjRoIOd1f5E7XVjpwImcBNKhfGT5URjxFKWVghkDWOobtxUnQgXmbW6N1m9qZVyjss8Bq2sxWffLHRFaGcL4Fw8o3CjGAhsxbf1g3wl2Qp34VHyqMt6'
        b'tvj2IPMUakLhIB9PuTOwmpJ1645KfAIYVXfIdtaim6HYiQwIPtM2k570kUBTghNftHfaT6D3aIueDCKKKOyGAwHcLbgEi/EIf5GsJViF5wTLMVIzMlxuMis+HFsj0ULv'
        b'HoObXSrBsHfj+nKBpBTPQwmpBDYvYHVgGfbAVinUzsFC9oxSsZWPaDLn9QD3WnR7K6xm3T8sI1hJN0VBKl2Hl4iklQF8QvSAve5KykJONl6VLYVkFiRhsAsq2V16in6N'
        b'LPIBIqlkC57Gi2Qu4i44y9oXr5vhMQ1Wh5NCmQcE06FCErCDbCnmBav5sMvrheeVGyVqQRD7CZhD9P5dbHANxyqJJmQzaZrzbkSaYOu1zRopEQZ24T6+kFfDPhU2O7u6'
        b'khYethQPkI0tDppYslC3ZLiSzgAynW9K1OIgMqUY3B2cJNPriIas8ZRK8byZtmZ0DmOJbOIcsgzQ922S5itdaLXGkGEmHyTpOZjsW3Q8EKHYmpHmhLhAtakjHdFk7u6N'
        b'xqOsTGoi7uzVuDniOb9FA9V08bkm8Vu1mN3zXIfXsNklhJolvPGYYLJVxMrR1mxhWQwHY0iyO/BgJxRlBqGMh8mCzBa+A3OUGteANDWZ+m69ifQmkUDFUGxi7TXFZYVW'
        b'jPa3diALG+TjaTIZr0gnwIlV7PU5HuntzttSPOAbLM4m2soVJn0Nhj29Al2D5YJGKtkoTiaTIjeVunakOPbnPt1wabpkheiRtoT3O5TjQQ55QuRmPerJmFB1j/8Maq78'
        b'Efc5nAUPwpWnMJs+OwSaR+1fhg+BtguOCgZZzCGQzUVbBuJBoTzsGPAgPcRRMD9yhRYGmV7bk7t2kn6Uk/2BRGov9nsgUfQTVd9JrG1EmwcyifkfEhmFTbYSh0uGi/3I'
        b'1YD7kj8klhTo2IK8YfubRE6vh0vkDxxEq98l5H0bcZBo84fkBfkkcwaszICSKVyyaCP2+V0iH0B+09xk4gDys88vEjNbkhf9m3xq2YeUhYKXODwgaZk8JG9ydwB5lqbL'
        b'gZcVJA07Uh4FSdHqR7lS8b3kKYtAHdQJZ5pXkZ8jac5inz8ktLS/S36V2ynETX0NnOjwlu/ALPuojusQ3Pw06aoBctJnlArTyAlTpvCpvfEzJuMlIsVgcfatIo1dDglR'
        b'y8gP5oLeaNEF+yRljcACuSO8/XyCfSIY2gkLvObgJ/F6xBJa3hQaacNP6+z+K5gkk/TNVUpHNj2Qyxaod5dMrkXP/k1m+r94dVs+TiJaWSvYKSZp6Ad2U3TIJXTQSf6Q'
        b'Semng7YL5gw9NmQ61Bsw25MVYvIiOdl2sWBbcrfwfHPtb435w7FLpDEK7bVZh2tzcq2MsWDXluTaSvu5dYdrLY5JlZkeo8QuplcHjBJpB4wS+2LTmJF6jJL+MQP0GCUU'
        b'14RK+qo/gVEypFgeM0qPUGIZZxIzNGaYQWwSiobSEZskW+1wx5oB9zDK7VmxK+JT77t1AybpcPffQCUZz4PbPdWSOzLv0HCfO9KZnjNT9tEhfoD+OCQ+PjzIeB6d6fmn'
        b'MEW0L43/87ghuuxYMKgHxQ1JqeWROxThI6WOYROF+wSHRvowvJDhXbA6ImbNCo9d3zkE3T3lBK3w4zzqoQfV0BXkfh9jqeqRNjqXWW3WKQ3aDymvdYTr0DVOyj9ojV6n'
        b't4zl4ZHSTJ/5z4JsPCZjrgmnisRy+VYGBGgiBGMtAwJU4Q3uMXlmhZ0yLCJ9vchRzqqwHFvjHTFfoqH6zruTd2xq/TLq2RV+0bfjHP8ZGG0e97lwL6vv+MXChHzZS/f8'
        b'1CIT1zaOUGntUtuncXcgn7FGWEEv6txDqDRoVDKgXyq6S27q02WOPSZKh62ptoWNbmT0618PQeswnnEL7dvbFIqDrrj/VSiOIfLHheKIYSWnWAPU7/9/E4dDN0UegcOh'
        b'm2KPfGL8Y+NwdJ61xnA4jE3+hwBjGJzIhp//EzgYXSO8eDBCdCKNI6CBWkbCjvSvGQJc7Yad0amftXgZdAPhGBhkE3E0HiH0KKAKXUn+DFRFfNz/oVT8/welQjfjDIA0'
        b'0H+PgxXRedI+JlaEwQn8f0gRfwEpgv7rHrRjEhKZNkVggA7X5htGKcAyLA7Skvi2OypvcIGbmKvEOsjpFY9uz0k0FPGh9w+rKSf55x+sjlv0xJu3Xrv11q1/3Hrn1iu3'
        b'3rvVVnK4dEjO+Z3DjjTuVBdeebM6e0RO44Hz+R45Q/bvaDYJeF7Y8YZlWJBCbcKMNFPwPFzo4FsLx7HKffgSTvBQhBfMOI7AGDjaBUpgOxYz054cj0fyM9aywE6uxHFQ'
        b'yCwtZhsXBGKDhy5Q3sMba5ixLAaLsYD6RFNrbxcogH4zdR6h/45nrD6A3uFRos9sXSC93JAc8uej5Ps8ljR09yHR8kZL8Vih8nFqMSTlsqiT0gyEyc801fowdc9JHyM/'
        b'1Mh+1y0uXv5wn92Vpl3mhlI3P4KovGbaRWJTUpktTqmV2EyZxKYgEpspk9gUTEoz3aaI6HDdQWLbakhie3i0e0eN8v8Xoe6dAcG0YpA2/nsd2ThoIO7/Rb//X/S76v+i'
        b'3/8v+v3R0e/ORoWlBLITdORI+1PB8A9ZMv6bwfD/0RBuqUFp0JbbiaAFmi06RHCHQLaVYhhHBqPmeaxQJnJfiQg/zA/VwXr5BWDx8M3Umy1wPkXVUjAXeiiDQjNow9wx'
        b'LFLCG3MylBrY3QU7jIdjQ85aTtO2C66F6JDHoARuCng6GS/xzHfCcWjRU51TXC/cN8UQtJdEgHI8aobX8DA0p1HaRix1c2oPOMU8P2dW9PmYF6wldJ28TVg+SjEDS4ew'
        b'F6bNg8bALpIwDZ91xt3Bsdz9SwhXmmIx7DZLm05zuBoElyhFLEtu7pz5LvPm0xjggOAgaIz0g9N+wa4u/sEkETcJXFB6QmF4hDAIqqywLDwhEOpYGDdkjTDXUKutmOQ7'
        b'VYBLI0eneZCPV8ZBMRYuw4udUqchrcmeKTSOlcWUy4QoKDSFSsiflEbP4wPXYXOE7kFtR0UmW8Jx9o6u3sLiOFOow7a+zIHdEwuIbB8yPcWKNKK0hzjFUxvCMhD2YQPp'
        b'sdzheClDQ+NMbopOWLmYhzMEmVBoAPdRflEJP4qRQrzmjYlSzUtU+nth79w9U6zA3SLn69ovpqWu/NiuameO0n3D9Bkz5y7a/0qOa9wnsq+njPdf9eSzfZNnjXhyxc2f'
        b'N3/r/2HFsF3LxjjJw6702qrsb+rjtyZy4LlB3yterC/2+2mDT8HkJU+sm3Bh+qcN787zG6BYu/Zz2cTv3/zqk7LsQt/+kwbXp44ca38pKSLgZsKztT+5fhs04BfzT2fN'
        b'SJ49zuSTQWVO6n3veG956u8Zi0zfC/Kan2i77I8fnN8pt/+hcO/hFRE3G9sOpD/37Mazuwpafhv30f6eY5cVP2d1AU1z7wRseOmC2oYdvgaN69nB+wd2xTHvn62Yx4MZ'
        b'y50hS0t/hzsZJIIuMhQOL03lETY9NVq4MqgzE2fA5WHcl+ysPeynWs1uN6W8I2t2ERxmD4yTT6IaCp6w76KgYGsIT2FfFBzm4xAPYFY7VzGeVvGwwSLIg1wdTBicgSui'
        b'x3LYx926yLxpYfMEs5d0iEvFUjzJ3F8iBUutmy2NXd8L5zv72ZoN4gGqu2bDeV4LWtb8IBFKsEqwwqvSIGhKYE4t6/3XYaFK46JnTIZcaGN3NuIOLAj0DKBrwNklIQJZ'
        b'Ka5ncDIL66FOcNpS5/9IrcxO0MqcoKxwL1Y6zcZjAcG8Y0jRe46S4qHlgezVDZAZ30GpxOJp7lA9mIO31ZpDgcGATaxw5BGbW7GuO4Od8n8xUjLoUfpgMouXlCoYs69C'
        b'LqdHx6KdlhmYHlLTLyuJlUTBYh83De6qQxkOcDR7nADH9thGE+PH/6bGSXUNxDH6PJY6el1lXB19VAX/C6GMSx8ZymhIj/tLcYz0fKN7HOOwELb1rIHLPnOg9aGhjEYD'
        b'GW1gLwtDxCsJdnoMA3c4J6zwnuKB5VKlMBRPSTEbz2zRBvpRtE0odO6AhLkHT6nZ9u0C9bAba8mCwQIVWZRiMB7jUWC+ZKILmZOkQpTzwQnxAk8td2DSEijRhyKyMMQC'
        b'vMEZpRrwUDIly4LLUEzjELEpgp9ZnQvBcs16S9hBfT13C5AfgGd4nF5pPzwdaaMNRKRBiBu0YVtYtCIqMDAtgsUgsvhDqInTBnTtw7oILN48QqaNPzSDGh7jVGYFDXBx'
        b'uj4GkcYfrsIdvBDVaUrYidnaeEFBdITDiYw3BHZgc2KnmEABWmUsKHABXGaNcUi1WxggNtgp3aNcQxf35iFx+UnDhFmCe4xciJLY+oTxD0du8hNKhNXrrKKizNOXT/j3'
        b'ogKzHy+crE1niknzpRngzlgtD4ozWV3X+wdjgTOWaumWsAyaKSYKdfpTQ6vUk0g2gVCGzRolVi4jLeaNedaReGMeq034aguhj7A60nROVELfiQt4FTel0FDABXNNVVGT'
        b'n5o2UEije0gE7grXBgJqowBxf6A2EBCP+LEBsnHoOjwEZbpwPztxUi8vluLY7RSO9aUAK1WU89Q+cwS1yLtsl90crMRW7tLL4vNKkv/tMMvHaFCpQtegdC9SYos7EYF3'
        b'6WL0zMTxFsDHL+zFszJlyjw8oovPg/NWbGr1xcoQMruOa6P0eIzetlgmNsbCGbygJG0Gp1mIXqsde8VSFcMj9IKIALGbh+hB9noWtoot2Eza120hXGFReroQvV14OL4p'
        b'tcREU0kKcHezbVpkYLmdj82ZpjPfbPzB9YWV+w6b2NvYmDzZq/QHy8+bJs+3q3zD9UbAE/ITuct2Rvzw1Ix1xarjewYpjv+6p88RxZ5BFtZHxm/+wNRGfmvfwjFPnpHn'
        b'Vv3N7ebtxuefP9v0ks/oksCV75sPM703aeGs/FMVYS23c36S/vzK898LHz2xOioWJjvUzlh3Rmky2/rjUHj+q0Uf3p35akOd2VVJ32OW3zWMC8tzzBqzJkxT9OZkx+MT'
        b'wu4+ZboRxzbFudyrt0zQzPtYTFZejm1ZJ67tP3fdaxlR59cNH9aSPW7Nwd+W5sx95sK04JMP9sW/8WaS8yvbbZavm9g6YciWj5fP+sf+N1sdJNtdEgYmvPPB++NnXh3w'
        b'zPbTP22wdUpbmqZ+dVhU/c9OTZZTNQWeay0v9rhyqCne6+7acdiqWrn2XqTLL1dPR6pjEy99n3RpQuvOKWFTvi7pEff6T02Bk+qr3h/fVk4++cgm5em9n/xm+enCuPQd'
        b'C7/u82T61TFq5dX5jffDlpTFFS/c3Pzc7SMTgk5Yrc1557OozdF/9/LyHpj8d8e6z5V533gXeS7P/vrShci3JNf2Rf0/vF0HXFbHsj/nfIXeEbEhNuSjSVFUbFhQOkiz'
        b'CyigKE0+EBsKCNJRKSIoiiAoRUBAqWIyG5OYm26a5qaYeNNMTEy5qca35XwIltwk970XfhH2lN09s7O7Mzvzn1FbW7hq07Pv3Zjxzu/Txla5vf/KO3Uv2DiGbnd4Jf+L'
        b'sgl3CoVLnrvtjfacuCMNdbr986+9H7w3Btm07C7p2d+2OG7vhW8vOBi/dVHH0sv2/atzsi5W3frGtfJqU6O2o9vmhf/aNv/1MTMmHtToGL0s5tiMf5t8GfvO2KMpO8pS'
        b'bl5aIb93r39B1u/7k9LfdA09c7oszzU4URq8rGTjb32vJMW/9vO47Kq0qiVJ83cumH3l/v30ZePtrr0SHZBY+KvanUnN31lvGF9Sr/5d5tmoi9pHfv9w1edJo7+cOnf8'
        b'c5/ZPHtdzetH2x/uHbL40NTb9cczm4XFv2VqHL97+6WSAz/36dz+7c6M5muvzLq4f+7rbYutpzdfOzb2PQ+z6HdOjRj91ufjXrd3uv9a25prW1eeSVmFAk+HRx3Z+tOX'
        b'/ujFF7vN3lmQ7fnF7799HPfyzjuLRtUnfRp94OPM1A/yne1Qs9rXE78MNP3hx9mXR4zpdn723W6DT03rv8vZG+7886936wpXTZgU1sKN8boRFPnO5ZK7/PdlyZ5fvRGw'
        b'qOrtr9fd57++McUoo0+7T7i356U57nlhH76c9n7bU5dXfr8r+uvQex/86ri/49jpDknv9sWly3e9WKVxs2zUuvD6bWNqmmOdy5cvcF5z4Lvsi7Uxczbtk0S9/U3L8rlV'
        b'Y569ufxt/gdn/z0/2ssUmv1fSr6PQo0r8q/VJP9sMN7081ffma2IZ+mgT0EpHIGzeg/k8eGyuB50MKxYPtaj01WRXEaiNhHzNg+OidFODkCO9RDIWzRcYqi3KDhNPW5t'
        b'rAh65QHsjUtERwnsLcKeAX9OY838FLG4DILV0CVoY4C1jaiMah3qqHqptR102zDMGsOrrZpOe2AyEXKHgtXI4nSMotXQkZVJCiLtoG5OhKspPPEOZEU8hileLR51S7g5'
        b'kCnHu9BF1ELdbHfAmWgSDiGLYJFIfQSxBh0hDDJTho77Enrt30zRaQyaBpXz6N2xzlDAcGlecUS6oLg0LO6kMVf0/tkmg9gzODBFRKZhLYU5W7fCoVXDsGnc+kgGTYvB'
        b'+hNZ+mWLUe8GVKnCphFg2jg0wDrWiprRMRGX5rEDuhgwTTeVqlSx+ngUu1CN0upRZFoStNLKN0MnFHl5rpnFjicoNG18DHN3z/JF+x0IXEeFTlNB04ymsE/r2b0O6mIG'
        b'wWkqZFrCMoZDujRJORSYxqWMosA0Iw+GFukKGyHiyvIxXURcWfXWJIIfH7HZUenr7qAClenZ0w/Sd9fDm1s26vB4DKQsO5q5W5/cgWl12NB6qMa3GxUxPfYk1KRq+Uq2'
        b'22pjFpFBLY9aRsJZZicsQRk02N4QnAkH5+EEQZqMg5NMSz3hjI4zxBpDm/jbDeLV9LC6Tb/7SBAcegBY41C1DgGshaJOBhKo2gpFcBqaKWiN6vu5CgZaM5NKsQ58BB1m'
        b'k7DPG/oeoNM4VGhDwWl6kE3bmbzHdQgwjVsMxygyDS67MEBK9hIoCIdzIpiBIhlWb2ZkyKG4tA5M+IN2IjINaq3ZoHag1mgXqddDUaYc4Ch91dQVkySPaOoiNo0A0zTH'
        b'saT1avjOKTjo9VAIJUf85YShRk2GPshEnSps2iAyLR9q6Ni5orLtFJhmC4fURWAafiGDQbJyoCqBIdNQ/jJ0mSHTUKkRO8Kog3Z0bgg0jfNGmRSZtobFQQ9GjVCkZYmF'
        b'6zSCThOxaXi1oF1XEkSklsLbTESnicg06IE+xqx9cNoQL3p9g/A0gk1TWy3iz7qgCp2DbBVAjcLTAlEmfXUrnE/FIlKviFAT0WnJMfRmqLfBIJ6EHH52EDwJ5MfSAx8v'
        b'w814QYDzVip02ozRLHB+vAAXCSpBRKcRaJo16qF9mQKNKagJ00KFTqPQtLmYZQhP6KKDUIi5r+WBNDsCBhgirGoyahoa7x5lmNKQ9wccaE/1UP0MqPAWYTMiZmYPHGHH'
        b'IZ2oB8qVD0HTME0HVPA0IDBjchoUtQ/VifA0FTYNc1S3iE9DacvYLL5g70HQaSgjnIHXKDxNO5LhOZtQJWbY6vEMoEbQaTajGXgnR3OJErWvCaL4NApOQ6e3UqKF4AHq'
        b'DbRl6DQGTUMXIY9++3bUiAe4ApoHAWoUnYZqoZgS1Q2OaDB0mhUqRdkqdFrPVrpwmE1C1YQsmuQILMcHc00ulOMum6I2qXU4ukR75jEJZYmCdcosMfJFrQtDxBQSMMpJ'
        b'dHkwDL8DXtUZ1mmrPhxDPeiwlqpuwpuaUCxAcwrqp9TQ9N6pZRlowbA2WEediHqhh05lN8ywFVgNsh4E1hJUHP7SAwxUU4+15jSHUUq2PWoM4uLGzZHCYTSAiilxglAN'
        b'qsPrOFYjyik6TkTGBUMzm3mXUPuGjZgug/A4FTRuq4eY56HWH3NdnQiOo9C4/XCRAaEKt7ooh8Hi5IIKGIcGlPT9WRzm2BrUI4LjCDIOXUZn2bHpQTSwfCiYDa++CxiY'
        b'LQ0dZNtzwJzB8/8gPxWYbRfkUzDbWiAR4PL9UMnWx+DZGJaNHHpQgqaijFmoP/UBwfCWhDIkSbttKGuvgJ4QwrReCg2Up/Cg8kYTysMUHQXp0mUTQtiO34RHIJ89R9Ss'
        b'HMjmsUxwXFiIB6SNQfQy8IRpHopf4yajswTAhprM2Ww9DgMJqHHhoPFAdWDbs4KxG2aCs7NnoPwHZ6Uz4Txt3xlLM/vhEhQqcfN+mLEOWuOVWH+nZA+WEPrZzlPoMcca'
        b'MyOWznygBToJ0SqE3UBSNpMqNqIsB0dUqCTnublEkiSyC88ZjJCkQtOyJOKZgarRZZ3t+kPBfU+G9ilRL+WGvXCWzElo0aKPDoPFoZrNdGVY5oK6oQFKRaSsCJNd5kPn'
        b'ggn+SHQ0QsRjUzT2Ag+2raU7oOODMGAOlaMcAgTGu2XSFNLd/ajT0PqRDppDowq5B5cFJgFU+cAAyoU6VR+HwA9RWxKTbvPQoeAt0KWaeMPBe6NHUra2g0asuVdEiQA+'
        b'Ct9zhHY2ADXoEJSrAHxevuoMwIey0DmGvyscYxMzTYXgI+i9iRvpnEan0Ak4ohyC3MNCTY0KvQfdqJTSyQy1Qb0WHn9ULSL4QqGODq0E38nBW/JFpe/DED5/qGYb8VHU'
        b'i1pXkoTvDMVHMXyoM4qtZiV4Z9qP5bE8iuQjKD5ow9sEpUvdKizoUBSfCsK3BUpUKD53duoOZ1ApdGnZSnTp5xEYnzqqp4OISTZGhPFZBaAOFYwPHXZn0nA1FEAlw/Ep'
        b'lseLOD5U5k/rVUzURR22qNLHl51dUBxfMBvT5ikkoPMQEB+6ZCfi+OC0C5OG8bKJN7lWaFaB+UQoH17g6QNjLD2HQfkIhvwYhfLFjKfdi4CT3ui41RA0nw+/FJOKYRfx'
        b'2BagQ84zKZyPgPls4QxleBMoMBLPzRyhW4XZm7xKofv/D9Kj6ClqfPD/I4Qe+xmlwunpS56M0FMfROgZ0h8pr8vr47L5b4Jcn/+LiDw1dREhJ6UoOPX7+Pn79OcdufMj'
        b'GL3fBSnD4xnTN3SJaYTi+kx5E16Ka7Xjdcn78v8Sm/eG9tzh2DzTJ2HzTB62T/y3wLwcYjIhYLc/NJmkcb/8ATzvCZ3CPSFghsQbKmyehGDznuPFc0yF0f8fpu4qbvQm'
        b'gSDGcP9LmLp35NYCrysbgp+bOgQ/J14zXcjiz6Uv1tXaHhrw0GE3z1nCZVks6tF8xLFWV/ytzHgEOLdaWqpWqlFqFCWQf0t1xb+Nxd+a7He0JEoSISkUIqwGbVIk5Y52'
        b'tk62brY+TaatTQB4FLAmi5RHyCPUMjmSRLxQWK2Gy5q0rEXL6risTcs6tKyBy7q0rEfLmrisT8sGtKyFy4a0bETL2rhsTMsjaFkHl01oeSQt6+KyKS2PomU9XB5Ny2No'
        b'WR+Xx9LyOFo2wGUzWh5Py4a4bE7LE2jZCJcn0vIkWjbOlkXxIgxvBP2bJCVXX21CnTEl1F6nnq2FaaOHaWNAaWMZocBPjIwQqFXO+ob24oU+QUtEY9vNi8JDzpfE+2no'
        b'EwyxN+i7kxRPck0o2TMzHG3YbyeamYH8NX1YZSqbntLOfOEQt0LRS46CDURfPHw3KTKRJo6I307y4iYNdwscmkTCxjwyfONm88TIhMRIZWTckCqG+C0Sx9dhNTzJMWi4'
        b'ZXFYwTee+IN5RJnThLBK85TIxEhzZfKG2Gjq4RQdNwTDQV2u8O1w/H/S5sTI4Y3HRiZtjo+gbu24z/Ex2yOpDTSZrC4xO4nr1rAsGeZu0dQLynKhQnTnjRnuG0ZcqETv'
        b'QjYQ08RxUFHcxtxykUL1WLi5MpJ4uSVF/tEgkTG0XKwgwI/wIZ6Eog9ffGL0pui48BiCQBCRy5gEBF3x0IcqleGbKPYkkmUDwU+xrzePiEzAy6nSPJ51nLoDWor3FhEO'
        b'i41XDvcK2xgfG0vclinvPeR66KsQbkh2xMbckG8Mj02aMX2jZMiyIxOXHmqnIjkPRWSZWrYqZ5cWXUJ4vIgIUbqigVuSI9/PpUp3Ge6RUAO3lBq1JXulgUP+HuK5/Av/'
        b'J7BmwybTk53QnuSXiL+QuSSu9PEWfepoehZa74Oxw6NE/U7x1Hy8s6plJGOpJ83bP8BAUfK6ECjLxnA888Nwl8KYbyCrbLCSoez3hKQ54RER0cyTVGx3GPsRRt2WHClO'
        b'YWUynluDS8jjsR/D/G1ZLhwyA8OTk+Jjw5OiN1KGjY1M3DQk080TUCSJeGYmxMdFEAqzef3HmWuG7XU6ItMNd0AY56skOu5Tnk93vPajtaIxSeGSeFVxMV/xVnu6kotO'
        b'Va9bpc3sntZExLTHqnAHOoy6yHliksKC2I0VcBHyFegItAN7BeoM4BgVU4OYF8BJuIDaoQm3vheds+D2bkVt1Mj7/FyB095JOhYWo3CezdFgpVAwFXqgA6/6czTmcnPG'
        b'x8f8dP/+/cmLZFxaJL7vGqa9aYE+i4G819aGBmxGpU72AiebjSqglvdHJYYKgSaQMQ3aqkR5uig3hVgeJsMlW6JvalhZ8pwjKpVbr5nEgiWnR8zVIhcFlLHMh58pwElc'
        b'AU18WeXhOaQGW03yD89NdIHjqEI2cYc7dTIwWzZJi9yAw5BHNMBeHhpQIbTjSmzx7TlwYOnQShI9rLAqjc5be3jhooQLQeQE96j6WKzK5dLvkkIzVg472AM+CqxuzhDi'
        b'8McdUkio6XcFpiLJCWKLDjvZz8A0TEXnIUfYCuVT6PsRFujig/tyTnvvSlQoxMhX0NCuSehE0oO7PKe9Dx0dJcTCuZhkYqmBk35WLNnIGHTWPcidPLncfahxZ4me2kiU'
        b'4cEodAayE5gSuRxVEdPHRXpqZQRF5NAoYwl1QIAmdHjOUO8WmqklD+tkuSSXibeXl62wbR5UjUWXIG8EakftXsaQ56Wlidkm3zMgkIuM0p8pW0WZZqSxjJusMKSc8LZ8'
        b'Ppe8ijRw3N78kfpp9p3CaZ7BlijXHRVsCAokjpZewaiNcS9mXepZ4+chM5yiibKgTiZDPW5ToEHBuaUYoyoHaMUUJyq6xC4ZdeglJJpDPmGTbt5iLWqhJnorEmdLSz1x'
        b'O1Gz8ehLeSu0H6XTewHkIAN1aG9LnIrayXvN/GSoZDVOmoHalQm+0DIG9UtJlqEwVJ3KPAj2B2spt6F2behOIS+l8ZMt5JiXKKuho3BGiS5uS4TCBfgm9PMmsB/66Ivr'
        b'UKOctjbHT9XYcSUdcr/ZUDB8yKF2oRC7BHqZX2767vlDc8z42Hr6BbsPPi9SE9JQB57LeDZ3xmjB2Q3GlLunzUPlj7zrbxtiKQbYLOYi1sMA6lbnIDMhun7FKF6Zged2'
        b'de6U2JI5SiMH/eemVO0Z+K5qWm7JrG3qN312HMjMLgkr8b815tUDHh0b5RVXf3LTXLpllmbkgatr3dxu3h41n1vsttDN44p/QEDk0Teab+VvNMv613uXf+/7tcRm64qR'
        b'F4w6Xj5u972Gf1jvUZdfr7z3/Ce63yxsWZ699kXjw0vU5gQZPv2Lbrcia09W2K3wWyteNHs7/cN7a3eN7XM9UfKyVtMnpw69/uqX3fqu6m4577vked74MaDdzSw+1ulK'
        b'6aRxv31i9fZ3Uw6P/Vw3Jnlhe+l2g+oF7lEu479WbJiEPgl4/ff3538msze5Vn7AIWhnxUg3g/ArR5N0mky7ri85Urak9NUQxT8svnq/9N/nt6xe4nClueBuQXKs9lp7'
        b'O2VkRtzHVS9ZWb+T8nJv2JLZZT7Hxm85cyVj1sbU1vuvvrz6g55T29evbXvhyqnEq5+UTzh4uybp7sUTCr9dUUXf1p30uX9guXPwizOrMrfv/XfLU5mX9PzWXmmUBb+6'
        b'c5X+2xs06yyWPTfBxaJw0qmvFo9LmGjyWvqdoy2GS7ebLL9vue747nHxUU8pF//T+PBOg7N2q97s+uLcqd7js1ckfHJCM8I8Ln/OR3Z3/L46nJk8urJ6u9+SqKzPNc8H'
        b'B78Y8lpgnOP3/V3Tg795W2fZiFc6S9vurDg+MmfG+aKpUeemOa+fc+rUO5fuSRbo2E87d6Ov9VJB/JR6h3vZm579duy98jPO8HGSs42f7ccNE15J/CgpPPO56Nj7VzoK'
        b'5vr2Zc9dduTMv99oTn7J6H2H+wfV7gkv1hv3Xf481vXKb7o33ly7ccaWr6d/HV8fcfLrI+e++Lzt6Rd9fyz5xO+z+W+PfSVwxal6x4IGzcgdr5//VWvOyxWjlsa2OZ7/'
        b'2nxJXdELqHfCr9q3DO6G3pN7fGWw5XaoYiE76RnwIPEXfQROmI5Xm7O810Qls0AOQK4/5EMrWURIoKs8gdOC/ulwHk8tdCCUvh0Gh6Dd2sNbjRNCIA1y+HkeLK6jlgwu'
        b'qcK7cnK4DHXEXB4O59nZWBqU46VkGrOKyqES9YcJE+GQET1jikI96ADJhTTNjzi7ovIVewWrFXCZHeUehy7IxO8Sa6u3HeT6UV92yJnmbmNF8Z9qXCju4ADeh8/BfhZD'
        b'zscFSofZ//Xs11pLNkHnJtadcjgykhyVoUJbOSc3gwPrhUmoVRWEMl9i5+Vn62FDjn+1oDNUW0D9qAe66On4WjhE6EecD4zRhaEhd11QBYvWd5oEsWSJaqLgwFCX593W'
        b'rIWWUFQunhTOgEuqo8IaD3a3NAFdUgX94mRQs5kcFqKWRHp46mcPTdYecM4S9ZvynHQTjw6M2EMNAJZofzI58aYHiTKoUAUEG42OS7dBIzrEDjjryTLXwWJOkn0b9ybB'
        b'lZlkalDJfExpTx8vW3Lk5ytWMBmVWSplc1D5BBbjsVcLLihRoQcZETQw2kvX1xZ1egmc2VIp3uG697JTzV7USMyZHuighnhfx80E6gRMyQu4L4Tldq8izfna2vgsXTGk'
        b'PXMHKaqDGjF6GtQvgYGhp56QgbIEKJ2wjd3Ow5LYOcj3s/P0sfHw4TndzT6QJZm12IOeiy6As1DO9msxZpvOjN1QIFGbhI5Q5tOHDBdqJyjwQvlqmBlMNIijpUCPkz3x'
        b'DLmgxDIUqkUNeLPbyu+BAuhgRtnD2pio1ApqhApFQyhUbmBjWGyH+YTa81ZCzaBJr0WTHbCfRNlrqEGKWkllcAKyUCWPeheE0jEOH+WiZedltwulkTcbeTgZDd3UfK/h'
        b'AP0PDJ1wBJUNj8OJLkAtM2EeRBcDRHMjuowZnpocG+bRz3KzQemqMJpY+DqVaMCvF1T+A2eioJCYpPK84dBsOW7/GAlC2CUGqoReX1RPPuygdQRUke518HBGLkYaRl3m'
        b'hHVZwFmUpuSgf4yUvhcgmarytyHm7cwQ1CvwcAzVUFszDwd2iEbheIUWbz4BTyVzOhXwl54kg6uyDAsbpJwhtEgwDWohXVxcLJIpdoHYqsZpEheYSgFynSfTyKUbd6La'
        b'QYcjlA7lDzkdQacfpYklluorsAxKJCUtYkW/wENL6npmEcvajZesjkEpSs7pRqCmSRI3dBo6k4hUgMWeTsiF/JTtqFNn2wPBjGC9p6Eidx9b/FKgTN1NXXdhEm1v7Rgf'
        b'pbUmlpEVqBfV8JxaKl6PC7zY4DXiAatSWicSlofGxTJOLVJwXG9OaRIWitWFfOKUgccpD0740byAMm4EapQaBKNGShM91Ic6tEjtuIYgPVwBNArz9DEXkbuzF6IuVRWY'
        b'RdU4Xd+1cyWuZt7MjF20CTKVnsTTiNdYgrp4fZSJmYOO7xksj9Vq0cCLqMWExF48vYCZQo+itIghVhssYomGGyjBKzl52SUSepUsUjOeAMUcnpntMWxNqkQFdixcqIDF'
        b'ylZjftIyyGVh0o8Fj8ddxb3xIKYoskJMcyfTbRKqD0Olspmr45mRfP42pa9C9LPyWpDEc/rjJMsdUCflL9dFsUoWfjmIOF/3oI7d7FOzN6UqCYlQEyayBLL4XdDoyObB'
        b'AOqFRmtPWy9bK1+8rOhtgp7pknDImcd8DpoXjBrWL4KdyZ3mS/RFGadYL8O83W6ZZIUfdTTEUr7IGdC5eDhz+Dlj8XQOtMh9JaiIkkkHiqZS9yGDhSoHInOe0ngRqkrW'
        b'IncYB8dgHYczQL0SOIfq4SyzzJYtRyXWdO+xRW1QIOfUUZ8Ah9F+Q8rJe7wx8ZmpaQa0DQsZGb9IofPfm3P+l8xCj4tAQBKq/gejzz4uUpPXFwi+RM6P5bWJoUWgZ+r3'
        b'5DJ9auohObWIOUQuqNO/dPFzurwZb8Fb8oaCPsnXhX/G0mf1qblEzpvwJrhOQ/xbF/+o46c1Bblg8vAVnvzoUrMTeVcuYl2M+V0jhh45PRQMQSFjSJObxHjx0XD0ivZ/'
        b'NRYSVt2D2gfp6YEVS+VcQs8/tsykcT0WT7bNPP6r/lRwhc3/MbjCOZUD+kPNDEZWcFCdi9ODZRvzyE125lbkZMzOfoaTKgTMo4EW/nz3Ev6oe22q7v0yhvRDPGQ1j44Y'
        b'1uKfamwTbqyBv6EeupGdvj+xzY7BNidQRDSFAUeZ09cIrv9vtazgb+iEDp4th0Y/ufmLg81bLDRPjovelhz5GPj/3+yDdqjqnPGPutAz2AUrQgFlEiYBPakcPKT8b7qR'
        b'OOqPRrx/sG27wHgSeCguKp6GUDAP3xCfnDQsjtHfbJ+EpXli+5eHc9yQuDp/uTEa2sT9jxqDwcZGP2hskcfiv94WnUpef9TWFVVbiT7cX5mfBX9U6fODH2AZ9JhoSKqw'
        b'Hn+XXTVpZIJQEifgiV34x/ABo8EF2KT9WwOmIEsEbTUp/oltvjzY5igxEMXfbHGzamnYEB5DzCOh8QmRcU9s9rXBZmeRZsmz7Mw+Zqjx7+HIJX+bDrqDvdoYE6+MfGK3'
        b'3hjeLfLwf9Wt/61QmJsfFwqT5x62VUh8ox3e3CpVEqnQ1bORxLRUj/owBis49Xy4/rXXExQ81XHXogasx+TD5Sg/lcMeU4Hg0IQnRLScqvKkIUrlfxSq9nGbdhk/tNnH'
        b'RMaFhj45niVp4G0iZcwnDfwnKSONa/qDqJaPbfr/ZGCi/tzASH2DovOvu0mU5LJF1mGvcO2oD73VOKklH6ytkOc/4MVHKX+eY5RPzOQfkW1CQzfEx8f8EVnJ2zf+AlnP'
        b'/gFZH9/2MLqSvpMeUCd1arR9EBBUFXSKGW75bJ1Bo62QI8MUl2CKC5TiEkplYa8kcMjfIsUzH6Y4QQeSnI9Owyg+3pelwiyDzvHEViCgHG3RVgD1LtRitsBf5npNok/s'
        b'JN7T5f4cNXXNDkpQ6ibCkVUa5Oka3s5hJzWqvJIsMx3P0Ye1n9rnyCXTTa8WZS6gByssBgAJn1Hghf/wJRE1AvwDbEMEbr2rGpyBHDi1ypCikA300H4vcowTgvKh6MHZ'
        b'mYyz2iiDJiiG46zrdajfjxhALqE6ctBBLCCQ75lMnZg7oQz1D/oJMy9hT0coi0SHqQEMTkyFPnLs44UndRY5p5La8ljtqxMTkkK/dJa1wmovOqYCEcPJFGoJQYVQpyZq'
        b'sUSj19skgQLIiAyfFURNZ7i2ImilGqOth5TTUBPs9aFIjnqYJTNzlbmXh42vkQeuVsrDyXhoZyjotDE8OQRV2Mo5jdkCVKDzUBcBlSwmy0CAN8ELwcEJKsgQdGqwsL7d'
        b'YctQvq0vVTvla1DeOmFE7DwaBRxdmLPSCxV5ONuRuH64Akp2GtWAs54nQ4VzUN8jzKmlYk7vB8w5nDX5wShof4UtHwlWTDqv8Qhb2vlS1qs2lK1+XWDcpBkTK2JmR28e'
        b'BL/AWbhETtFapzLq1aMWKB70E565nYdCYjKkN6UboIwNGOpfpxqzyFVJdKB3oNOoUUmdiCVbHeAEvwfVxVBErTmqCFJy04hPMtZsx6WgEtoLXTi0ywtOQPsgWAGdhjOU'
        b'IxNQ5uQhQI1FcJ6HY+aj6D2/0biPgyAbuAjFPNSMnMuMawLm+Acgm4Uoj+JsXOAgtYEnE/iwctossndP4OahUxOm6yhkjM+PQrf3kFcnoVr6KsqAQ4wwRXAeFT1AufjD'
        b'cR5651jSdhfsHaNC2LhCN3FopggbY8RS6K5DHdYEvoOOQJaPKrGUuVsyOfbYDRXh1rhRO4WVj53CNiHO04fnJkKWbHYYqmEpiY+iPm0VSAaVoVIGlNmNLjO+rUGF/qLP'
        b'NR/ly8nVhZE6k6nRfSYcX/Co77aPvb3oui1PSaY+3j1wyY46+XvTw2aypEAecfYtC+c5ixWyrXDEIpms9LHomCGxhjzst77QfIjnui+kq6FDi6CbzlOrALhAjatkXUEF'
        b'ZnyYxIFO76hEAhoi68qaqYMrC5Q56rEICmVaKI0sXuLSpblx+OKlj85S0u5EOWvp6iOuPBvx2qMHhxllBgwTVNgIKEKZPNTCqTEsGEHNKEw3FQgA2tARHnN57Tzas+lo'
        b'P6pSLQVwWIeT46UA9UMTXbf3OvsPIg53jMMLiL4/5X9bJbTCMXKGhdcPfhaHilagQ/SOxRIDa5pXXhqOumeSXM416Cgb2iK89jZgpnK3DUW9NjSD4hFhD1zayDwoz8Bh'
        b'uDzMWZ4LHHSXhyPM9QLlqWkNIlkMUAkDs3RDGx3ckY5zyNIlLlyoPO7htQv3ukghUIIFwJlgyF+/HbVvl5Ik0aQD+ePYMj6AKlZpjlCi83IyOBwcgipjFmbpBMqPRCX4'
        b'sg3npmljBJl0G/t6oWbANIklx+mHxUSOt2bBCWCJEOEikL/CbMZ7hbOLPUtknqlsd9RevXMUuygbqz33OSz7cP5h2gWro9jFEFv1uY2COX47LEZ9Ysij4Ruo3Ej+J2O8'
        b'h1unm8rv4RO0I7gQvIZuEyIGFTQqAIkZnPntDwnoNzTmboqMi9yRkDg/UkMU05PXcRQCeAHKlEMP0qEX736F1ugwC6Rq42ELefiP8mFxHFCJBHVAiaEXFDvpb3BGDdCw'
        b'ExpGyNy248m9fATJhIcqaBb1SSgP82E+IlafEls7D4ph8Vzubxvi/mAQB0cQOgRNPhVlcphdG7XD9GKZH8hltH+xtecWOGersMX1PbAgjQ2WQvMWeXTYrQpe+RL+3m3P'
        b'6kcG9sS966pfta642PKLgZgX2m3f/fartS+vOut+c2Jqmnnh4ajwqdZPVUc/5da2Zrb9ysnp85+SyW6Nydiz/7Cee5lLcOMe16hN0VeKtA5/fWmnU8ecxVOuzDPt+/Xy'
        b'jMlxmkav2ijUnT+665rwUlZtVa0wf7bjsvSIG8He3ROOz1327Mc/vhC8doeTfkbSaetL7v/0T/zpu84z/ZOnfTfp4xTjT6tjLwguylvfRxoor93vdN31ju2CzDXr7OJT'
        b'Fm562mW59VXH3r2Rzd7L940+99nxF65aNVyZMDbj5UmtXz39u+vIoIW7Npr8sOTQW1Pto7a5/evageVTCyYsaJkc9u2ip45bvPX81SPfL1HETvrC/85WA/MTE2yWJDw1'
        b'9cW38jbwVtNeOOn9ad7sg2etfLuqjWonXaq/rny7/tPtt778vuUHm3d7Dt/7rjKqY8xnklEvtBxHP41/Rnljxe9Hn5v3r426A0ZRh751c8p0OmG8+pO9ti/c/rzG6oWd'
        b'H+dvXx6bbfFW/TtCw7RDKe5fVa8uzX8j+UDCyW9sbk5JPDlR7+q44l7vL5bdWhfQd7rF//2xN/mbZjeD4bs3Un1aAu9MuamTZ+MfEaiWXf/WxHbXuKuxPfs/CPMoe9b3'
        b'xUIz4U5HhPMGZ88Tc7p/bbHzq53V1/TTO7Ptaj61m20VuOxfBzZOvRt7qyCyauH7JWN6GxuTfKfm+X99bdyvi9t2fPnsSNPLB0Nfeb0h8vQZvWe+zfx89UcNN0YZWU/6'
        b'Un9f4IXOCRnNH2Q15vIuKVMt7rzVuj9mxHV0+0WXWZeyP+lxyWz+6EbOmtBf1O/f/SGm/I7Hsje/MjtTVfj1P+0Db58sTu6693LHnb7Ai2YZ6gXf3Xq+vWnlR/k653/m'
        b'/Tqy39wcMquw1rfYa3y+7RytOftz0YvaPXFnD+xZ5JRU25q57e3e3M8UA2sac9cNNJmE3D9V2Zgc5txfOPPDXOVT7988fbntFe+uEWf/fWxT4z1N07F9wvqM+/+eNvKX'
        b'mUrNLsVsBtx2hEKykcNZvE07u8fx0I+qF1AThIMNDGgRBJqGJRadsXxoAGfW60ngePQkMaGtAl3QslKgdsgzohZZ9TFCCKr3ZxambnRuRfRelYGaJEXMYLhTRbDzEMyp'
        b'DDr5MdAOjQxSPAAtcI6axYlN3AFl8OjAwtnUkOMOh0gcuEFopQRVEVPsRXSAQe8n4qn8QApChfpYCoLSGQzPGm1MP2WbN/RNnaaQczr4MQsHdIbay/V80YVY6HoYeDpo'
        b'i813ZUamU9AxS+m0cQj2U4rSGC0uoIZQlSV2FKqmmFG82onW1MrpKEsLCtQpoEcI4uej4gB6xxyVepqgyypLKwFQHxlHDTzGRM4YhDhDHbSKMGdUiZoprZZsEh4ghaEB'
        b'kwpqDaGGjp2FJepXeuOhIUufl0yOcjhNbQGq4XQAo3NXcDSFvdtwcHwdJ4dmwQn1M4CROZZWemkkggqUiYUIMRRB0iYR2L169mD2TUu0X4Q42yIGM4JeXVTCMneiNH8R'
        b'Hq0NJ5m5vHYmKsFEJiEE8ChJZ0M29PNwHnpH07oj8T5Js4ZimbWO4LNFcPZFSzFL6mh0WonyPDxQsS7q8hI4tW2ClcFielPXCB0hyFhokFB0KY0404tyGLi0AaUZErvk'
        b'Nmr13QSnOM0VAh6fg5DFrOH9KZCmBQ0JxHa5FFpwxyt51LrKlYHRMjBXZimxrF/ObJvG/CRXkWOhGpVEann6WMuxBtALJ+ZjGSgZztMxtEdZKE/pDT2oztdOw87LTpMI'
        b'QqZwQTpz3WTmglEOJ1G5bZyIZhvEzhpjgRiVzEB9zKOnfDWelufmKB+b+TF0FiXufDwX2hgeFEpN6H0KB90HIvA9H7XCYA66uNUMuoZOzmcI2i43dHkwgIQc1VL+ZxEk'
        b'5CiDmYZbUem4IfhcrGa3ixhdZxCdUo56QLmYSXICmcz8wl2ogk2RQlSoR+DPxIUE1c7mZG48lqearRjfpEHxlkEMIzqKyng4Ox9/P03odwoaNsZaKAezA4/B3EbZOA0u'
        b'zdBi6EJosaa4ZThjwxyZIGM3gz5O82WrE8ldWAdstYCWkZA7iHxEx1E5ntAClFNiLMLzqWs6alE+JnXhdsinffL1QelaUA7nVPBEZyilgzUF5aXiMW+C8qEARRU6cYkm'
        b'W0p64PgWlmRQDTMjQSeiTC3GUGenOxKvW2jwDErAX6zmJUywgk42A8q0Jz2AS6KGfTzxrsFUIh9spEQlKs8tVAwXWKATODuHeWDkYgmoFeXb+OLFHItePJaiajCRmgTM'
        b'1t2YR+g8SZ/hSx8pUKAcd6kDNOInWvBooYqVqn5fhibrBUux+IwFSDjF+y/FFCXvzqYpjv1s8OwmGoZagILTQgMC6opEJ9gonsBLV4uW+xIrVIRJ5sNP5yTM1l0fNEnl'
        b'2eMKNaJzj0TNDKXTSYKX8R694Q5teAE5RpzaiEdbZ7jC5P8aJfaQQfa/j794Q5OAckKpMzyVw/9JpPL/fH67jzNmiEcpxUCSf3V5C2oIt+GtiPmaogM1eUNen5wX0h+C'
        b'FtT+XVsiyIXvNPUseRPeUjDkdXlTgZrExRyI7Le2MJoYvAViXjckZnMsNJvy+gLJfWiqrisQM/lYyWhqHsc9Ecx5zftS8r+g+Tv9X0Jq1aYJBEwYclPQx1d2KR42MpPv'
        b'D7WbS01Syvl2D+jB9A3pDY2kHRGRSeHRMcobaqFJOzaEKyOHmNT/RjoErMPcI5bB3wZt6L/ivyS4TqUrIf9/PoZN4+4/OTBkMrGOjUZFUcqHnIf+lL6DuuOpysM5owo9'
        b'G7zztisk7MCxCKrHiHnfOZkZ7CfBdYJM6ZkFdPuhY+weOhIJOYN2g9FQK4X8ZCihj6HqUZIhXfATKxs/RwqZJqgUilxFnXY5uug82JR6NGkpFlWzOg6g4+bs3g509pGm'
        b'LFAajV4caWZhTRy8zlm6+9h5+CxPILSgmTxIVASeCxuhjr/t0GS0H5ro4cIa9Z3DPbwFd8iOXeRBDzYmrN3ghQptsdwURCtymLHcXeyey2R51BrOOJIetezE1e0fmkqE'
        b'NWs55BR3LVSqz0ZH9SZDHzszuYDfOP94qkhDUKkBqqIRkOE4qoMS5UP1BYtRjcl3FeLt4wQWk6L2qUONzfzofV9OkyhPYyZ+ofaFyMB/xF1zNa4qH/fueaOpsdfqbVuF'
        b'm+v0b7f4XxmtkSubGOGU98wSTd+AlS+55wS1Xw9af/6LiYf1t4bkRL69Z/FlfsIzaglRYydPdr76w+xPT+y+s2Pt5LyxxQHfV0yotMyr/HHfmNU/aV2cfCC6sduwuOid'
        b'709FjH9+R3xWgnl2AOdxcO7nwZuzX/x8d96NFRNLKm23vB4a8NLpfa6at0dYhu+LPOf1SbP5benaBNe0rM9++sxl0dsGLtMrU4/c+mHkmvCo6RvCvvimUdLQZLpybtfK'
        b'j97IdWtXrphRaj/WJW7Edb2mz29E65yJaQzKLY4aaJJ9U4/WNMZmmmx56fy88qnJOwO+WXQOvXltvceZgxdWTN6y8Rn/Bdt63yperXvjrReaap2/Gmsem51UEH/bTvH5'
        b'l8f+/Vpu6IV/Tf/35V/9LnzV+FKw726hxazln4mVHcc/nfjjt/YHv508dedG06szevaOPVp5bGBjxkTXT9Z9+k2HerL9GeWWRbcG/NujV7/RefRaceR53TpTDaPCrnTZ'
        b'FzW9ER8YHzU74X/K+nWDXb5fbX/+lfZlYXbvfrfyq3yjxJ+U2a2zx24KeWZ00eJ/a+b5fZ9Zuats8dtqKzTX71hs5bDu7X89qwhVbBj32Y62mXtXKQ4XhH/7Y23Ty7kh'
        b'DYe7lS806p7Of04vyb/9eusL3+3TWdug1ElYM/Mr2yuKtWvWlq/xWp1XcenYpeJNsbbeNUZ9KxT12tc/elrnVr7azPT3IaRojKN5V9Po+SnvGzZdDM5Kzo3+7MBeu945'
        b'k/f9OH/yPaNrzyz1OT7r5KXFeS2/hlR+YXZiZNjouBXLv/18Rdu7R8al2Ey7+emd0V1rr071fG7Lvm37cqd1Xb6fUfFGZ5JX8cyftm/6NHHZmefRmU2fvff2DuuQc3ft'
        b'Xt259HASNKtFfdkrveu06OrpeXen7PSEjxd02urGv5KssKcZtFER9Js80e0R9bqLno9u6rpwAdUyiTIXnYgl3pSoIp6pIcTVchQ0M1mlB9I0iWq5Bc4w7RLrlrA/gG75'
        b'WuZQ9cDNzw66vJifHzq5gMoZy3loIFogytC1FJ2jYSCFSgOGWx0eH3fOALpR6yYsiBJZVTsWz1mCmcKiXPMwyZtEmWWBsM9AJTojhsLm7RYvnK9gMk4bnINipUrSt0Pn'
        b'J6G2UOosGIIV0AaVqEJOvrHoSEPdoDIpXhMHoBMLKVksFZALOqCF1ZGjWCgvEiObaBkRr8hmA6ZI7Udp6BJxL9+m4DnZTpSdQnKBH4GztHe6Y41FT0cOMlOgx0OMiIdy'
        b'oN9fSVSo1BR00DcFP6OZIkCTmRgOLRuqJhFPyINbiJM19YREvaiahkPbDX0+WOaVc8IKPj51jsyOfq8BcflUydZKdBnOYtHwMP0IrPzGPuQui5Ucazd0FNKZRtdM4vko'
        b'rTwgHQt3ePGkAcIysF6XTzUghSkaGB6WjqgUC1aifjss3LHwbqjG/IGTfAykE7UEK4B5TOc4M4tEoXokMXZMmOE6dIz2X5vzZfKyKC2v15kQhC6xMwGslx8R9QNO7om6'
        b'SVyjDJRP2VcDlc9SkswBMDCJOKJKoIHHCmG3QPu1VWZKzgMKoQ16iNYugU4eKvB4H2Ze8UVYV+vQsvNJpA81JMF5dBq3b2As2UIi7tERPgGNcJJolYx46jqCHLIilqEy'
        b'JmxXQ7k/jYonMx8WF28BZgE6Jy+gviWPB0zAYdQ4CJoggIndiA3IroCphHNxb5qYrisqupdRF9PCKtwFlZ6LldwKzOxE0Z1tRkk5G0q2YF0WTjkxdRbrslNRD2OsNHRc'
        b'x0u158uhGVpDBSuHRZQaukELRfn8jMdQzAkRz8uw8k81rswoW5SPBQOUjc6SSe3Ho7TZaIDVnu8H9cRZ1tJyMNoe1mFqmdd277qdQ6NEUpQGnj4d6+PFoHvzoMWYTUsl'
        b'OiHyGp1xppHSiXqogHWgcDk5oVdt8+qzhIm7NsBAIHVPhjwe2lU3hwg3402lUA99qDElmvYlOgjrW5hbNVANVlPz0QUSpspboEdTXSwGULo1ysQ1EZkGcofake1Xy1EL'
        b'qjGC9PlJRFTCjFUGOY9fdAfdieGggS9c1KGTYTU6idfSoaKkGqe7WoIuGjiggw7sO+ogI5bIU5Dl/1DzVihHBp3uQSx8VAkqdSNV+WF10E7MZCaRRKKCCaPgPKNXRgT0'
        b'PwDXeKxi2JpCheH/oWb1vxWNZmi0mSkqH5k3/pyOFatNM74TDQj/j7UXE34s1mVGk9zvRAvCupApjTRD9B9DrAgQ7YhoYMa/qauZJWJNCZeNJaOxukWys5PnsKpwX8B6'
        b'mIB1JBL+Q53XxdobuSYXr2lK5FjnEu6Tq3KJuqAu0ZVoU/dnuUB0OeJ+jNuTsaD7hrwUXyX90cTPPurAS3UrUY9ifsP3/jcdkkU9atowEr/3F9xZ6v6KNzL9GOIwZvrY'
        b'bO0jQgl2f2MSUx5DCVCfJMqlCdtp/naatf0Q/ueGmuiZe0N7qKPsDa2hLquO5GliXUrcSv5xJf+kknY0Bj0Fb6iJ7ns3tId61d3QGe7NRlynqKMPJQ8bjRH/fycVD1yV'
        b'PsDNzySjs5ejkW10pYINb7FBjEUj+X/6LdWWaEuohwicxat3w0Nasj9db0ehs9JILLOdfLJb2BKOYyFZuMGMxmqDLmLC309jTbZPW+5hF7Flvsl+HN3vT29xsp/u6Oww'
        b'wwm6oC0pKXH7tmQl3gTasFDQji7ibecC3gTqUYeeuramroaOFhYmcqAAFaOyQH90GJWHyDi8/vdoaS1VMvh+1RxU4kTMA7qcA+cAmaiDXt8FpZDpJOXwJp/LOXKODqiU'
        b'XseaaCuccxK4KXCMc+Kc0IA2qyfPEcqc5KSPndx0bjq6tJ36biyfkejEc3pQxc3gZqhz1P4cjE7vdJIRU8Z5zplzhm5pMjHY6iu2OEk4qJZyM7mZgXCJBjQI0oODTmoc'
        b'dOpxs7hZFlBIa/AaDVXQQQI6lnOzudkT4Ti9nKSZhGVwDjV4cC6cC/7sAtq3zdMhBxMTSiCHW8Qtgk50nlnIi7C4cFkpEHjhWW4xtxh1QjNtdf7SOUo58dPo55ZwS7Dg'
        b'nywK68ehSclz+Gs4N84NSscze/p5uDxSKeOgy5Rbyi1FlRL6PWtcjJT4ey5M45Zxy1ygjtZhA0dHKvH3nEdlnDvnjn8fpnWMXUqARATsv4rz4Dz2oLP0MqofTaB/Um6R'
        b'jPPkPFHHVOqigbWeHOhCHQK3J5nz4rzQEZRJb0igBmpRB+57zkjOmyNxS0toZ+zjCbiO24vSOB/OZ+JkVk0fatVFHbjn5VDP+XK+gaiGNjsBlRIzlwSLarM4P87P3JN5'
        b'cJ3Yi7msQw3LF+acP+ePhYcLtHYNVAv9Whw3egYJwB9hRyuxgiZ0SAuPJmrnArgAGQww3yJ/6NDCNM9YhFk7EAtYufTydBd3Lcw+56COC+KC4DRUsC6SCH6tWjzJzVXC'
        b'BXPB21AjbRKOSPZq4Z6f3siFcCGCQKm7Bs+Kg1oSguO8jOfeilBoZ2Ex0gMgXUuNWx/KreRWQqsaq7tmXzTkE/AlOsmt4laho6iS9iXAHyuO+ZiR6my41dzqsaiP1oJl'
        b'3Z61kC9waxK4NdyasBG0TbkZVKESGWcN+zk7zg7TtJnVnrkM9dH0HemYu6Zx0zahCsZ2fVgHHQgk1hBo4CZgYuehk/SV5XCIHMUJWAPK5Kw5a3QStdJZNN0H1Qfy3JQA'
        b'bgo3RWMBq6YpELNBiRqBYg5w9pw9Oi3OXcyn/STnPf4/kLPhbFCbPyXZnAQoCpRxYV6cBWeBztopbGhmsgh/D+q/kG/tCmUEi0nyaUk4I1QlQb0KyKHeVlhvWUFv4H8k'
        b'kJGIWXCSEWrFTwQlUq8oKBuZTCuZpnqgWMGqsEZZLOdCpgk6gl+nT/Cc8RQoR934Puqdzmq4jPI2iz0hjxhycCzGCHcF9WqH0SeIogBHWDfIE5iL+t2MjfADULeCps3A'
        b'q1YVpgqtgj2BOuCcMU+aOQ9naH6SaQmQJjajBqcSOSM8807AQVJLB2QxR8bjWF05yhqKhCy1SRytYroN60YvVurEXuLuTeTgooLRAnWYMRfLs+t9REKZC4SS6EIgqT8L'
        b'tdP7UXAhldaAFb8qqJVM4th3+qM06mU0GbqdrelISODUXM7YCJpm4NsroZMOxuyl2uwDSB/UNuCV1Ax/BGmgUj1ZDLpZg47T/tNHDLnJIfQLpqbQc9QwuLBTbB816LLv'
        b'YGNOv+IQukw5A/LxhnKA3oIMElgE+vG4FkiN4Ax+bPFySvIEVOvBvpU9MZfEf6xmNa2BNEqxgMlwSdUepjrucUEQY46Z6Cg9CcVaaqlqWIh1diUdP9YnQpk96Bg9qRWS'
        b'42lj+zXHo/ZE8Saqd2Gjn744SWyGdieR00NFImVOQxclzbK5K1WUxU/M5UyWU8LgT71AuSNyOjo2SFw1qMEfXLiefbAWnsBkdOTrPFSkVZtAaIayU0gV+1OZlyw5uzjA'
        b'bi9iw29sh+97xDM2L9UwYyRNJwQj/Fe2Fq9m+DOKLSnZUTraD7W0i/SRuaQK3EHSB7xBZ9OHxkChtfitm4h7gDglRIqEe7Cj+TJUHaT6mjDUo5p9HCMKylpAexyAzsIJ'
        b'NnHrsKa5P5Gxeyz0UnZbgS5Ci2pmpxOity6EQ/iBTZimZFBMUdVUOl5wTFsi4YxnkrrToJgOCqpw2yiOPNmdMAehQ3PZ4EMLFLGUQcXrUak4ncgzmIdyTIynkEdOwQk6'
        b'blPRMRnrgzWd1+aomc38o8m0ClRoufXByJNmlGtE7uhAbXTFTI0ayZYNc7z6GMn88b1EDfpykB8UqeYzfmcDCf2ayVaNDDhIH7FEl7cMMjDKmEucSyoYl0NaLKVTDF6B'
        b'Re5D6eQjjHmojiOVHBvP5lPtJGKZtFatsRvIiUaRWEkV2s9Wl8Nr0WWxJcpCnMyekQsd8qXkXgbV+iKDJseoLRaH3G6ugqeLlxUf7EXzNpJsb+okzKuFAOlwaeanVMQ8'
        b'lOiq0KTOee5jBU7KqQfgLcHbYNUK5rG3XY+kKEpwkvqHxThrb2EXf7XV4PQ581Q+LMzmEzd1djFQAy8rnPtKTS5sbXOoLru4dD2ukbPXU3cNs5lv7M4uWi/S48Zyltoy'
        b'+zCbVKcQdnH3WDVOmwvbqWceFpOkMZldDNIz4My5BAt5Qph3kf84dvFlHS3OmPvGV1M/LOaozlZ20cB/BGfJbd7DuYaNfWOEC7s4wYJkYvzGkTgmTtMezS5GTiWfmeON'
        b'G9PWWYu7RLysM1NG4q3RPlIwD5vrbjcRq5NBS+mNb7aRKix9tHEVS0fGsadzTUhfu220zcNs9q6K4z6trCD/XV3AvsSd3K0eoYm/ZO2GldynTvS/7xbQTT0W80IrWcig'
        b'H2Vx8Vw8OpFCpYwx6GC0tRo3C4sgO/CG0gGZzOWZMMEOdCp0GLdBbZBqcR7BHDOdyQd0h+mah42duUSTfarnBkKU7vWY+mPfWy591N1yMIYZ4aNNosMlS+40mNQpSgSb'
        b'3JBFx0VE7kgkbvGPy+qkh5V45mlJ4pc6Q+YGa1/qZZzIHBh9vP1Q2ZOzYzUTX45KrYVOy2nXS5WruDbONEo3LGx0xMb1eEB8faMPcLskymDc7GrvKz4B1Ip1ycn3y2d2'
        b'Oid/OfeFprlada6asekmwi293sWlby63vnB2YvRImzvN2rDO/GfJyllr5tduHUiTac2XnMqbY5e3smCu8s7sH/+5O+KsUcaB/UJews1TmY57gvzddJKnv/rM2NVHl6U5'
        b'L1ryWXW+2S8rn5KtfWbK2mdH2Hxk1XLTJe5Di7hwja5tav/ozi9r/ceB4g0fTd5yckPq9xOWV3geb3DZZrgpdK0sJeHr/Jc/yJp5w7LWaKq179VZHukz7vyoCKlPU5vk'
        b'+YPvlrzcqZ9VL157a5HrOLAyu7Hmy1sFKc++N+ljDa8rW5bMmRe4YZryenh5sOvavLNegXWbfzM6mHjlgCIf1Co8P5pit/t8+z3lD1sDIw82rXOcYXdmS3t0qOk7ZvV7'
        b'V35Y2aAstFYreuOpH66/9Mpa7eZ8e6tsn3+fDzHWkd++9apF3ZZ+c9P0+dGfv/Hh0k98PN7RefqtV86fNu+YHnGk8CmLV2/JZ95d6bw5JKoxaFxV0StFXtb6R348eO+0'
        b'X6qj8meLvXtOPF0Tc/Nd2x13XPunXr47Pfjr+2HXan6efrmtrOz6SatrxddT5/xDu+K5So3uK9/1rf42YE5LgnAsXaNty413HCd0tWue2La70efYuytHjJy389gXdzWP'
        b'eE9+XhmecmtrcGzRaZdbRd7v5AW/PM7zfpHPOsddu6pfuW2q2feP0uDYsr7tW2Nylz1jcCTxrYYdv314aFL4gZrnU6XHnh9lVj7/Wgto9f+28iP/4nUd45ZGBD7ddMj7'
        b'IGo+ov/jl+MP7355Ze4n5iF9q70M75+Mba/6Kurjjrs/3p1ZcLGh/8eRd5a8nuU3VaFLzxi3haBCclTr452EWv1knGwPj04biCGr0THNCJRPokSgcyTXjtSdhw45FNKD'
        b'7k1YSmz2orkGvWytsI6Sba+FjkmEVLjEjFPN6MhOmp2kSxkPB2WcRJN3IA7J7Bg8C8/mU9aoCJqxdA35Mk4awUN/7Ch6d5wbqiOBgzxsPLDq2uamtV1Ax4ieRru1Bquq'
        b'R8VMPdQ3bhqqFHZqzKIn6POw+NCN651mFT+F56TJPMqF9mgWsOmSmY61FTpGU9wI0MGHuIkJcDKw9nNK5ReXQkLrSWfzcH4T6w26uAe1icgfGTcH8rXlArokR/XMXejC'
        b'GOj0Yk79lRNwkyN5qNFdyNyjGvFeetALK/tFopVrIdZda6n1YYU7NAyLrAT7oYykVopFlYox/7/+NE8+aFT7i2e9NzSVG8PjQqNjwzdF0iPfAbL6/hm3mn2cj1SM/PD4'
        b'H+lduQGLB6FJ3WM0JRPFMNwsaLcxviqnx7rGNCqFsXiIrM8bkvMviTH+y5yGKNekYcLVeakgpREmaMBv/GNB86pq0hIJMT4Rv+HIJ2oKqsNDyQ1JdOymIae4f5I8WoJq'
        b'7yB19WmImUj/xDkt+XnO9MkeL1T6aw9CXWz7oXvPRpSOtx8ZZ7Jeqp5i9EjsWE3VNujJDcaOldMgywzrJURpDsaMlf6pmLGPPc0jYAV17tGooU8+VyQBznE/hCjhbwBO'
        b'H2mf/Cc80r7Ml8kKXiQh6VF1PS4s5vc9i7lkkkMEimcQY2L+CkuoQIdF5KKlu0egO5ndHjJu5m65JZRYRfu4vS1Vkqimagfib4e5h78YZVn8Wdjap9oOpR8+9VJGpkNW'
        b'Q8X53PP7JxxN75Bx8XflP5k5KVgcLPVFUOXFAtzIoBarU3OFkTHQQQ3rYxc4P96wjtXkOtS6wUmFA3nMEfMNrY2bIzduDaVSC5149n9+4u3jLFn8/l3jQ0k05VASkeGB'
        b'Y9iQmlXTgI8eMgmEYbyuM8jr2vivEZrigfGf5PU07ivdJ3M7mTRwYhpeVvOn+UKrj607FIhwkUd8ughMyQcVySEP63WnQ/CLl0y1UFW8CJBDJegMap2wxcuGpOQpkHLy'
        b'0YKmDdSz46XyfXDAGhX7ooxJAicY8NxSlE4ZZ+4iIk/b78PytHeQ+x6SXZQMqwXuQJaXt28M5PmS3FDqfoLSDmUwCXm1Jpbgn9KWYQleI2U3pyTHafM+Gh+ok7BNwglr'
        b'R4dgjayVitpIn8jf1XFSLH/fnr6HiyFE1teScaTHT0WaaF9fGelYyylp4s9d08K0A4OTf0iRcBIZP2WbLW1tjiep4lWZOgl3G7meUxLhVfC78rHAWRzgtDgt50n0udp4'
        b'kib1p/VaWKrvtV7EnmvTifhYxmks5XQ53Xd/URJBV7ow9eN/4YG04L6PM7VJVZKNdOS0LYHBOtt1PqlPCMIsbMuXWl9Qks13UcQP1E7cYEm8PYw++Oy85FZnH90dKMIb'
        b'pW25pnfVv9zmKp5NarzguDSJtivvdrrGcQ2mnIJT1LjSS5PUw65Jub39nBVn9VkDvbR4/Nv5PJf4FreOW2c9kvbulNPJ/Nfw74+4A+eylIvotYS5BvmvYWb8mKvxPFDZ'
        b'yvCSRXBRjvI9bHRQF5leTlhRg3zBkxxcRKfMbxGUnXhZsvY3cAvwiXvTVfviJser3u/f1ssaOJ3jZB72dOOyz1ry8y4FB00Mnm5rqHUw09j/0wkT2j/krspmebx5LSHt'
        b'RsnUU+65P1z/4NNXir5+ad7a0YscP0iVZuRcNdjz9O+pjRbucc+e84pb1D7bqnjM9/kN9Rvsa3+OrfG4WRLudH3U8x5r/X/+R9yE3NHBC17UOPR1zAdO/qb6spP/1H7t'
        b'/bJb7wS8B2Ebns5b0fnRBmfJ0vK0cefW7GxaZNNz+tLL3+uN+iA+5Xrz3upZ4z6p3KTzjGdZd0DdZ9dLboc9s7cj6VBlrXz7usljFicWp3YllGwNu90Set7vRBPv9tKm'
        b'E58Wp35i88MHzyyr/ueCt67eDpnVFn8qq7v4l6eOrNB50aX149WlC4+732tofNOpOmaZy73g4/u/8G5atWfv78opO6yWXbtc/+m3M01emWbyys4Tr46oDF6R1NyyuSr1'
        b'C5u82Fnukc/rzvo+ef+qqsqX877eV9tztdsecmYevP/rsojjb73x+vm28p8ynft2HFz/8tH3vmz6UWtb6PNOKzNv13bZV77bMTPj9nd8UtS2n2Zcf+/CrJvTfgz0UfuH'
        b'j8MXZR5v+l3XW1+pvHl88U8/SQO3VytH2Sj06bq6BQtaTcuUXgrirCjn5JsEKxiAg1S8i9urQQQtVAc5LH2POhwS4tFh1EklRn31DcSFxMcGM3sianHgoRlKlcxDpNVm'
        b'GRXtUClkEseKfDX88ilhL5QFsjw91VCK2pRJ20dItuvoQpGeHmrXxkq0CTohwat2F2plEuQJVBPIhF0s6GqglgjqigUZVJ41gktYAs33geaJqIs4dWfyy6BCzDuJKgyh'
        b'CmXgbcGTypg8Jw8QjFGrmDkSzqJM1Osl3pLC+WQifqL0xcw7qFIKHVhyhYuQKbauoSVAiSNcpi3PghooQqWoHVegsCVOGfIwYVKClEn/mf5oAHXPFmEqDKMCF5nz1NIN'
        b'/rhelOPhiXq8sVSsRYKbVkEeOkO7tdkOL8AkfwbqEUm+TohE/WJ+QOg1Iu4P/qqNkO6CEaiXDofzPlTtT/we8FrurcBDOUcwnu/2X9rL/46v8jCp9sG+SDfXI39lc52q'
        b'K6OJc6jcqsub8PpiPDN9KpFKxThnJH0NkV+1acQzbepyQJ4k8dGIC7k+lX2lAnEVlzJXcfqeJY2PxlLTqPOJuoPSquyGNCE8afMNaUR4UvgNjU2RSaFJ0UkxkX9VfpUk'
        b'6pM6Dcg/eoO7O2nH+C/v7nfMnry7kwNTV9SJsmgoU7q1J7HcV3jamfhIjQP2bhSGSHekc4PCI4nBRk3SfJRkMEyB8KfDFDw2kIyUezReiYL1E28cnagf66iQO21eEj1x'
        b'xFxuCF0SlGGEGqLHXHQVlGQK+vI3b4d9FvZFmHf4l5GaUR++yJlZcmOKJUGuTw0JbiJ5ou/ADR0ybsO5z+qvcN/mRMNBjpCy8aMj+Xj5TXh4mMnLwX95mM/p//Ew26pv'
        b'ZbTzHSLCqS1Zyk1ZLAsynfp/NsyPDUsjeWSYJb7Ra+9GS2iCgxmJNWQAI375IiwmakOEe7h61IfeEm78dYn7b5F/cgiV/90Qbk00engI9f9oCPWHDyF5eeVfHsLGPxhC'
        b'arSqd0m29n1kDM3hEDcFnZSF7UZlTx5G4qWUTQaSz5ZGSf/GQD6i7pFBfDRJhaYvC1xQAjlQO1TURyfCNFGFKNT/NNNM2IPfObn35r5ZY15woxftkyVc0AQiUIZpv2oS'
        b'yM6YOQNesNwiV+cSwheMWuTOUW1BF9WgnkA4x6H62WTbxCoKF8gyDmyQc2tjsCRhHhazYpUWRzWPRdNRcaAtOmLt7iFB2SiXk68SeKiYGP1xdiWv3I6feF5fMu7FPh3B'
        b'QT/zZsXdeUsk7kmus9UDoEx3nXzi90t9j2SOjrG6lX0l5fMft1oEvfbNcvug6BibpP6ycKv2pIyN6U4fJ19Ptuz9x80Xmq8+2zzpi7DA214f7bzj4qy/u6r27Zcmnbvm'
        b'omYS9fuOKym7b+lkPzf+g6hx99eVK9TZmVXV9iBrW0tiP5FDpYCyLWxRGcqh27pa+FYqSZEtHZpQlihJndBgqfUuolqSNRgvhiT7Mj8RHePUUQGWZ2S27KjsHKofpTq4'
        b'26bBYK1uplRUmYVa0FFookIOysVSzl4BelD+RDjDEj+iapKBUjyFU6JaGUdP4eJQB8M95iajImt3epCGpbj0mTy0TGcB1aXQTaEpKtCr3Jic7VlD9SNTFk+ux22CDyay'
        b'NlmLEyKiQsm+KqgY+U/P4zjidahLjpuoGMBCmiYaD5nbhKVvSB8CWj3STSFxBHlno6pftIo1f3mGnzF88gynBtSM6ZZslXb3wFsyJm4/6iYEHo8ypagenVv7yFKqIf5W'
        b'jn4oJVqppFS7VC1KiBAKeXrWJDyILBSlHiGJkGaq7+dXSyNlEbIIeSYXoRahXiisluOyBi1r0rIaLmvRsjYtq+OyDi3r0rIGLuvRsj4ta+KyAS0b0rIWLhvRsjEta+Py'
        b'CFo2oWUdXB5Jy6a0rIvLo2h5NC3r4fIYWh5Ly/okbRv+qnERZpnqqw0iZVFcNBdpsJ87zRfxqw3wXXK2poGXuPER5vgJw4gJdBeaeEPNJzyOODH+Yjss+Q7J4GUey26x'
        b'9GTDk/NgqZQs7I+srBqqpY8Eo6Thm6hjHiUx2Sw1BtdY6Z9aY8U0UL/s/485oIb1+EEOqCdlXCIzhyV9In+R3E7hrAr/JUvNo6JjHpM+ahiXEX5/9FjRzJdloGnbHAP1'
        b'wXQdIOlh/GxDRJgYXnpybOx4bhmvNnMp7KcJSCJQQapWwrZAfEf1WJD6dp2EIJKhucDLQxFF8vFuNFfXNkMn6Eq/Ex2TOFgPzcZrDpXM6eSowVqs4KF01EnT7YqpdvHO'
        b'0KdySsmaY+3pY2e7F86SCOzWPGc0VYKO2c9hkb4KdFCGl6OngFcyaOFRK4e61u+hNtSJKMODpZSGepRO0koHz6Lv+EGthZcYrH/pNE4rXkAVoTOYM0gZOkaR/oXEvRzl'
        b'r4Zz3iSiPzopWYQuTaD70Fh0WeEF59xxnwywIkcic0+SrBSM6Y65F502I+pZDjpNVDTyPdAl7N4KJ+ltb3RW4eUBpTDgY4XvC/Q0BdI3QA2LPtUBJVqDMaD6bFkIqH0p'
        b'Yug5dG6ecsLwzOYLoymBN8AhYi8hEbbgtAEJsgXVesli5vZTztAE6cMy1rvspN1Rw9/aOCQc1jzIoOGwFsygx2pavMy1jcWo8/4ubBvLFoUOT1vFImuhPrsJqHEl3bEr'
        b'HGTek9mjNm94jCPne9RHo3Kk25CwVyToFcpgca+geDZ9c8EEQbjBs2BB78mVHP1WmQmcX4kuDss2bwuHmJ9UNhrYo4rDhbImD8bh2iEGSjqyCvVa28EB1KfwHIzDhU4k'
        b'0EBJ0I3SoeLRcFmQ46lKdey/m559LdqEThE2wfsyXNSgo6WLqiXr8IZYFn2xKl2gSWC39ExJLe4LQPb6bin/8rk16+su2eXDetWnz9Ruqz2VsPBmxNlb8kBLmff8p+N+'
        b'8g0Zc/co/3rznfeuv/nm3XdK3l4/o3H1znX7s2r3/vPn9Rq2u967uTw/ZOHXKdnPbNj/ymdGrWOan37693+7hmSdkBwz/Sb6te9S34qoXri9eU3s7nXysFcbPhv4LH2z'
        b'rct3nzZ0Lr4+aumCnL3GqSb3Vv7Tf/tU5wjfOqcv2pZmT21+/6t3bhq19f744au+3mcDJXp5r1R0z75sf3hd50bJ9vDqqut165IbQ8w2ptzLS048sd3DIcXqxfOr227k'
        b'rH72asea2QMdx022/p43srgnru6TAJ3LdePfN9z+rk5Ki3ZSzosWXbFZjiNf2Fo/ednU4EsOUxzqGuNm5U/O32DiYZK6/JPm+zWnx5cmHS7eu/yTw99+ENGypqHnDb8X'
        b'5n7pOCU18EjFP8vvXj5q8iyM014/n5NUHR27pkoxmsYXmRwAuahxkUoyIWKJ3mR2vFJhb+HlbWVH70Dack4rRkCn55qyY51GLgjl2yzz8xVNDyRbcCp0x1LsiB8qDBHT'
        b'oqB6aBiaFyUZyhgM5bAy/lFjAjoOF1myBkfUR0Wy7XIzYjSiC5p8NDSjUkETDfhReW4aHF6H930xgTgP/XGcllJAlXAMztKPg1a4CJUUwAedUEDMm2vG0h7aoyNKmv/E'
        b'zjYFlYvrnQk6IXXBa8ZBZo0tWmCyzxTy/ciiJ4nhQ0ajQiYlXuRR3RhtmojCm0SHOMnDIYM1VAokiUIOiilKnNAAy1IimYUuLKIwJP9pog2MLHuQD8dI+Cn8jOFMCZyC'
        b'To4hb06jivW4DrL0oYbNdrakFsPdEujCCsE58dwMlZrRDrDFb4zAaS3HX+4IvexcMJ8AxkniB7b8QZsjpzVFQNVQwVFxdNsKPDcfJPEpWjdZsI1Q0rrX7Q0czLGB+vZS'
        b'ZJyehiQJWlzoqy7of3j7Driq7rPhey97TxmKirjY0wEoiKLsoYCCkz1lb1EURPbeU5bsocgUAWmep013mzZJm6RNOvI2aZM0bdM2TdP27ff8z7kgKJrEvv3Cz3jlnvOf'
        b'z57lKdwDHMWQlg13FekeP8gXK5nHPpavZMGIxiZ46M7b1tSxn8VcldGtcJLy3LUULmmNEQ1zuCVQINjBOZhK47+uyoEi1pOeqDN04zhzVyg7S7hkmqYzlxYMw61zvF4H'
        b'NdC5Ua93pwwZNcyDMm47ivFHuVY5jGHCxBnGMZWjJeyxFRq47yPOX+Dv65wpZyUhKFS3lWDlXma425CDsQAmXJKEmQuDFjyeqCtLwACR+jwjqWebpeReNBtjtQ/CAyZQ'
        b'fFnh/YZAXp4r98AnJ8kKeZseSxLimmNzP6xILEsZkheJSLiXFkr/S1pGk0sYkuc6JKz+nv/5XFpWlfNaf9V35IU5qmIB8skmCOJ0I5X1BgLZL232FPGvWqw7ruSvrFzU'
        b'6T07weippX/5wu6bnldY/vsrQVmPZ1htcmDANRcQi6mPi+2/WFcDcfVsmeC02OjE5/QZeGVlQfz0K30G2Fuh6RmpL15NXDI4zDrsmdO+ujqtoUt8aLR+bJR+bDrf1fSY'
        b'9bHVU3ixaveXBM+5gZ+szqzH1QlPjYyITU9KfaFuDlzlw/eed99vrs62TTwb377hPyrULheckBQRGxX7nGv9+eq8e7ma/qFp6fr8S+H/yQJurSwgMjsyPON5/St+sbqA'
        b'XasL4F968dmjV2Cay5179ty/Xp3beAW40tegFkEZP8ALX4BMcERkGAHNM1fwm9UVbOewinv6P25EIBe8Aq3PnPi3qxPvWAfdLzz1Ksit2JSeOfWHq1PvXqs7s5NfUZzX'
        b'T79mdo7ZPRllI1yNshGUCAoEucIc9WsCziQg5MwAgutC/zWfn2U/Z0M/bT+XfU6UzwsWlZfgZpf8PGjDDsccJGbFRHJtoNNjWL/tx/CYGsk3reDaMCcmpT9tYXjKyrBy'
        b'aU+5BX6Ir/JtBH499qt1bQReeelV73eNhHzfwtKL6mLpd43oi7Nb7bFX9Ixq9tdWcqQZBHwFoeSGQCZn+wq3W93p4+CdqOjIdJ9nl8Fn0/6BMXfG+740c88T1D+7HH6G'
        b'g4Czd3Ra4xQnFpq6Y6PJ6mFg7ZOBOkyBgGYcFMCStAIsHYv4/+v+eTpIjO554pG7iHP/XFKSZ+6fuKiPQiqieedP/aSEwGBWol/xVSO+nRiMXlSDWux8+s7tYSzii9xD'
        b'qddf+OoVnn/1aZHp/DR5wifixvKFayf/9AUAoOI57iEWEn/6Et78kvdP2obQ+AjdvrEClh6GYSMRH4RVfNyCgw2BpDFOqQhhENrMOYuYj5UU95JAUgMXbIQw5QTzsUct'
        b'z0qlWTPQq390Odot3CvUKzTuV0ORMdEx0V7hHqE+ocJPdC7rTKTF6fgHvW8pZZMcJRBM3Jb9qbrvU3F1G8fYpUaKoYWb5itdlISijLIoR+2py+IHL3jyetZP+fELXE/D'
        b's6PoNljGs6k156jjuwEIVh11X5Vmez9FcJ1ZSGEaLzsQhV5vQ07TT0uPjY/XzwyNj434AnOwULAR/5H2CXDhjHK7duRoygqZP1Q/Myhhfnvs8pE/SaYF0zf++5U/DPlB'
        b'mOF7HqGKUb+lT6bqEnVeJ/yMvEIc0+5r1UQY/fjmJ2flvZxG3tgdp2vfEqdjr9PeWnY4TkdrwjxCUGZpGnL+WydR/6Wab3RCx/f9NGV+LGHdbKMk+PF7Oke0txrJ8i6x'
        b'xUM4ZsK5T65e5HVbZZiVcIURvMepx1ugCh+ZrJhYIrGFtxuzjEE+cujulTjPFTME1p3gzbCJWMPbKZrNAxlmQVOO2Vqjsib0c2/v1D7FW3jxId41WzHx2sID3me2dBFG'
        b'GHryLSkKL0EXtNrzNphCFQ8TwlF3GJOE0t0C6XiRASzr8981HYZWUvbHTKUFknpC+UswCX0wKWZpX+hDk41NC+ZulsOk418VkzT4aorcHxYEztUBkVyjU64Mv4bpPWNN'
        b'j7mgOT36jxfAsuJne9A2WJCRxkblM9bUyeAcehHskCSYeseIYOq/WdkM2RWV5C3ZFd3gLWlezH5Lmpd/35JdEUffkl2VJiNXNsdTuP+8K+UayqRFHy+zM2MLlhVJSigK'
        b'9c7/typXKCuoivgEwTK8Tz88Y/HCAga88lAlggU7mHiKtauL/04retIdKd2g0yCIEFUyB51MsVKxerFGlNSXd0Pyb5EMohCheEuWuSE5x5+s2PEny8aPUKoUcsH1CjS2'
        b'ZIRyhAo3ttzqd1IkBKtGqHG/ledWpBOhXimK2MW9o869pRmx6ZYcfa9A3wvYEw0y9KMToVUpHbGbK8IhJW7PolSsXKxarFasUawTpRihG7GZe0+RH5d+ZBvkaL1bKiUi'
        b'9nDuVynON8g6DikXq7DZijWLNxVrFWvT+6oRehFbufeVxO9zbzfIRGyj9/dyc7I3Vbi3tOgNOc7Byd5Q5va3g+2PdiCKMIjYye1QJUKDU7YM31IWYwb9FRodmfqrfXQ5'
        b'66j8Uf31TzDWQH+n6YcSV1jLK5gHMjRdPzSVmXRSMmIJA9YNFEUCP/d8BH0Vns5Uxdh0/fTU0MS00HCmK6c94ah0Tyfek5Qqnmp1ltC0VS2LmFaifqh+dGxmZKJ42KTU'
        b'K08MY26unxWayjq32ds/7QllCtwTG1zlecdOBBw11z+elLg3XT8jLZLbQXJqUkQGt9wd633BYlNdDJ3fU1ke66u1rFZqYVe/Wq1FokTiS+V3iJ3Bvzr35EVxR/aEP3iF'
        b'jSesbO2FXMKrJ8u0OrretdexofrGYIC7ughzfXfO3hWRRCsidU8/Mjs2LZ39JoudcJjYUBS5gWghXpBYn+fX9JSWnxXLFknfRGXQcKEREQQuz1hTYgT90Q9NTk6KTaQJ'
        b'19rDvkCuYdf5tJtbySeDCWTwEHv91hZbdePdeyQlYB1WenFVUf3cvHw4L0MMdpFcAMtYrID927GbL6pansHCazYYAvKwhr3MO28FmVgsl4sDmZzHWcMd+7DehAV8jelJ'
        b'CqT2CrFFMohzp1rADDSYENRlCxTwTrbmVT7f/wGWK/ub4QBOYr+1QMJcoHJY5AjFu0gLyOO7+TRGH1rbKcyQ893zHcIOGknttYTabcf46jvVnvDIRMRapmA51KbB/Wuc'
        b'jPe+kUj5rATnePXacS1AwPn2t5pgp+fqqfhhCdeDrNIUq7z56nOnkmSwAYswj/Wl4arNFFvqp9lvSiHkwWoBlLm7xvZkXxWmvUPfjT264V3j4CNhpVr4i8/2flv6k3LN'
        b'/ONHXxL+ck+t4cmRfeYGrm8ZWvXPhbb33Nz5hl2Acp2GZeamyqh9vkl/+f4bitWW/zJwdcjVwNE/mnqcjlz0KUoY2H7+6nd/8rsx+4D9hj4hB2KD7EUfykbn/PUfPz7V'
        b'ty/1THZQT3ZXsqX60h69e3+Q/ZNSQPjONz/3iO/9XtHUR9qfyv+mKPPisHPPozMf2O582/2d6Ac/0rDP8Ex8/9ijn9d9V+rU7//6O+PXBh5955OQQ6U19r/xi/YaMz//'
        b'z39WK1dbL7l5HvzBJ1t+fdj2Wveb/5L4d+jxead4I02u4OUpee2d2MdHGrAog7M4wWu3w+7wUMHLgXc4rnU24k0o4N2VPafx0Yq/n3P2V0biIN7V5eTM6Eg+IoOYNzzi'
        b'faAWUMyLt/PYdWXVC8pcoGlYSYtw4/My271gejVyyxKK+LRMuG3Efa2ONdDuyUd2GEkL5M4Eaoqgh366+HXPQS/MYDmJCj4MDoylSfaelsDlkFOKMMdLwHNH8J6JBZaZ'
        b'uruaSAmkYUhkaufFrSwXBtS4Suxi/yv0RjIXrK8e57wMwxZvEry9hHCbhOcd9Jf3Hj567iGUhvIR82oHxDHzWKzNLWiv2gGTi2a8V5BpwIR2ZtICbZiVdDMX12yFaqi4'
        b'ysdaleJdCxpAQ6QUiW2cMiHl6ydjzQoberKqgfy61KBZAqp9FHh1oB3nvZhrz2eleqKyv0SYt7c3dKYzYRcbdjrSeyxll5WIrHLzdqAnocqCtUir4pssucJ9GagmMlDH'
        b'D9kNc3STfKwGnXeZOF4Dbmpya9oERddMsM3lyeqQl3Sghq8MabwfyrEh1YLNxE+KVdICLRpnGW7izaej275MTPpG3rwARje/iiphx+Lmpbnoe2Uukl5RaMk+k1phzSkW'
        b'vMctR3s9s35G1/FVVrzG6/Yc76UE/+wGvrYtCuIwrq+giOQJ3n92kugzN/BVfF1Sz7dPH1YQ26efmmzVA2ezyuGfZulr2PcLuuQ472Da87xFR1aWmGrEIujWctt1BnLO'
        b'xsiFKK7aGL+KifypTIL/rybyW6TrXhU+sb2Vc3vKyimUihNy1uxt8REfhnyr57eP7dmviiqNhHxnknydQChPu7ghBpcbfYE9OzWXdWfd8wRQpIXHB3NppV/JUO38Qpix'
        b'/BxTNesTnqR+aMVQqRDjjjPso5evGdaZrN0wNm1kthbobFN2OB71BYHunPWsWPhCge4bJqY8bbKW5CVDRbjFtTddQ+KxigU3lnoZe5jCSAAf58h+4eu1B8uZSQhGoVTB'
        b'jl5pibUKlxGlMWqk2JX4YYi5+gch3wsz1DIO9QqNj4r/k3rYRyG/DUmM+iikLNpDnAbRJC+rlqtpJMHVS7aASRZ0GAKd6xewEYeBijAupsU2FwsUFKFjw8RnvOcmyeXZ'
        b'wW145Ep8pB0ebQSGDtC1EvzwfGaxYmpPvfFloXK9Df0pK37+OkO69wsB6Mxz4rDZYNAId6FvBUahUuIrAClnJtc5puyODQeNRHyZxBOWDHZh6qRQIMnM6gdhjDO447IJ'
        b'NrA3LE3pG2ZXt8HC2M9HPxWl7aOvf7as9aRdPT7aI9yHs6zrXtZZtavPKisKBN9wk8sd/t7TlvXn+EFuCl/UvB6oKK8qmaPzrOtcY2X/gumPvdAFfu3ZvpBnL4pIJsPr'
        b'Z5MOJwFnemekQ4qIh9Qq8ZD40hHcxA0+H3hK0XSNTCcNW8xt15pTnq2iJ6RGRvHq8FMhNBto0amR6RmpiWn2+kdXO8KLTyFEPyksjhT7L9B+N2aZUj4ZDDJIpg7lpHpm'
        b'uj59MtDsTCAL9d4BfU9Fe0PePrm4/bq8Rogz2p7m2ChYryqv1wr9FGSwEm5KxupMpkumsbqzf/+NzochH4V8EPLtsJiokUjmKQj6WhBO1NwP6r9lJGW48+VXvvfG1994'
        b'6aREn6HrZUKDqZb8uLOTLVOt5R0eQf4tTpP7K15S7NAV1JupXVG1MZLmFA8vrNtv4maM+Y/DQo9hJe8yuA39J8SaRx7p6KvRn1pQxT0QEoAVCivKGDQrP9bHZM7y/RMa'
        b'4AF0cYpcIo5wuhw0HOXF+UUjQnEvf4VVDUHhnAjvsjR4js6mnrfnokb3Exd5mhjDABasQ+Zny7drK1OwpBkx2HDobf9V0TuZD7GT5Yq25Gx+AqPWDM/LD8PiEDjOnP5Y'
        b'GN+QNwyL+Mcei+CHaYiAFyIDdzWfTQaes+hnU4CnQjW+rOCwkr0xsyHupz8dNJMUtZKG8d8nBUf5Ob8kKdjYwUey65lv75FIY/LpuW9ZfRhy4WuvvEQ42dRTtKPcqiXf'
        b'Rklg8dIHipI5FzWMRJwUa4+LuVwyE1arbBETDynBZrwtmQPNcJvTvgOtYcHT/XFGQ+oVEeTrw8iKa2tjF+3OF2ZbNwQskHMj0BDfi1gedhCtyMOOorWzRrwQmHY+xzX8'
        b'nLUY8ZjylkxaaGZkcGiaz7NNzkyLFfMtaU6Pkn4Bg3OUkeSvwjYyOK+AMLPIR4ir1H8pAD666j2ITA9lUXKhfHRQQlImMUJWV35l3P8r6OffER+YPbNLc34DU2aMTshI'
        b'S2fGaB4b09JjE/nYQaYhb2hN5rXmdRFfzG1Ag29kyV5FPLbW1NAs/rhoz1+Abwy4nzY8y/tk2DD2MakKj7DcRu8p7rsx65WFW1waDPGSZegy8SBQc+OLojVCF9zjasJk'
        b'/1mPKyaTLNkTL5BsFaYfM+TMumWZkgLZa2pcJs6kgqEggC+3yCTYvZdw1MSXBvMTXIAabIO72Bj7t4p/S6Z10rePcpwjK02URUdVj48uRGcVOP/pVT3Bx/nOquoRCpOi'
        b'lwyuKmrUZV4IfU8rxufliaoaj8Yhjw/sOhZ/V2sL/a57nHtCc8N3D+qqv/3tN7s7PpsviWjo1/9EWHay8VZya6LVRwe6T30z7l29gH2ajin/Y7hn/kcDJzUT0i5nnDqc'
        b'XZoUHm99r3rb3aR7wxd3j7v4RV8o+eM3Hzbn/Gvy05aOI5FvGr2//L9GsuLiGpo4ZxKIC2sSQ3BJXDov2BXaH9seY3GSFwDUL3DRZcdgBGdWBIDs82vssfIwKm6Jqgo9'
        b'JtiKY8xEydsnU2Gat7j2sd7yJsbi5ASHbIHcIRF0XbzKN6kshGp5k8cmyp031hgpU2GOFyIm6bEBLHcKeNxIlpllW3CB/34CGnHKBOdgjjOtig2rWIuNGzNhI+kva+17'
        b'S0acgcsRXLevTnBVV+pm7BGpcm08ZLlQAkNhjtYGpI8mWm/k42QFJ9EXyxWkaDx+do19j/6Z9EJUu17r2VT7GUunY+VsjBzZllsNOuejAghmBG9JxocmRge4hMusIQBs'
        b'Y+orBOAco+Qsi5TZw+Q5ny/zM4uKVYpViyWK1cRuRfUodTGFlymRIwovSxRehqPwshxVl7ku67/ms5jCxxCFvy65AYU/GhHBYtUTI7PWRwYxfxrvu+NdjeFJqamRaclJ'
        b'iRGxidHPSSAlumsfmp6eah+yqn2FcLSTcZIk/ZCQgNSMyJAQU3GUfGZkKhdswTmXnxos9JnOZP3w0ERG0VOTWIDGSnhuemgq3Yd+WGji5WezlXUexydksw39jc9kNs9j'
        b'UOwgmEM0LTkynNuhKX/KG7KbxzkSiRkJYZGpX9p7ugpo/DIeJztkxcSGx6zje9yOEkMTIjdcQRIfWb5yDjFJ8REE3Gu46BNx5wmhqZefCABYvbQ0fT5Vw1zfl8UIZ8Wm'
        b'8SsgUSAmKULfPiojMZzAg55ZEctDNhxoZfXhofHxdMdhkVFJYqa8mrTNA0EGC4Fn3vvQDcdZC0PPPMnV+Dx7/SfzOB7HNK/M+6zYZvFYYdZhT4+yNhvkC95nlIIkGH9f'
        b'/QM2dmZW3L8ziNoQEkZErlzVylgE+jyUbBxqfTwyKjQjPj1tBUVWx9rwxvem6XP/ZFEWTy1unZgjhky2lWRSNejTlxDS1kk/KmLCt1762evDSzGj2K+WZp0qIr08XyBM'
        b'Yh7GfOzibWc9OAO3FDJThPu1BEIsEWDHZSVxccBgLIdlZqcTErd8IBBBldDZEIc4ieocNNrTW6d46cnQ3MzwOKnjJRbG7t4kS40EJONk+hneGw4NxnK2MK+QwdL0zLDX'
        b'cJ37nldbOL+9LS5xftjwS7LQk+TNSVO/d1MSBGnQjCdDFLPS/PmCl6fxAQ4zIWPV+c4HIpoamXkoXpESOJhIY5sz3OF2GAe98SZYJy0Qqgn2Yg90whyWcGPX5sgIahR0'
        b'WZUTRS/na3yllPIgSYGOKSe+KSZFBvC/vGIoEvzcglUGDVFccjvAO95h2Oki3iF2pICV7gIFFyznCm9xL0QrygliUnbS8yFeA9qXBZyRG5uw05dLwvd34wzN7rT6ChMm'
        b'ga7uhL5wM/XAOpjyMnc3M5YWYLmRYgrX85bF4MFNqPRca0TCBrzLibIVRiQzwXCA26pfme54Xg7uREG+i5EsFwYRkQ19q+nrWZGcQ3TvOXFjEsg/ySWwB0OlgCWw46wf'
        b'37yBLj9vNXld1p2lr9PTPVwCuyb0iVby149jFcsJZfnr0JHOp4L3XIG81SRyXMBOlkiO/Yp8ccN7OOgpTiSftuFzQrlEcrjnyOfOj1spmPD5oDAPdXwieSgucb2gfO0U'
        b'12SRp5F0vproyWWRQwHMGynwCDDtQXOJqx/gtBQrgKAK83yJnR4sU14NZMU7WM1Hsua6cmuEEijVEAeBZ+18HKlK597EyfTbc7CE1T/APnUBX/5g5zUOPELxpjVny9pu'
        b'yZmyFC24PWUEB/O1D6AVOr2FfPUDvCngUusPBZxdqX0QiJ18DjBX+yAsi6/GUL8VH/GRsQm4sBoYi23Yyg1+UBC2GnR7Dpb4oFso2cS/3IGj0MwHlxwIMX2cUB8TzH8/'
        b'JYeNK2YEVhBCXBwhCO5yO3UJxxYWEuNHcrVEpDD74qErjtyLJ1xYYaAzWHP6JEnpZaznH11YJ23rPlfG4DUnKcFfAvkyBlKSJnw1IWjfA4W02Xpf1gA1XyBSFOAyDp42'
        b'kucCcOIU9NOUUzPwPt6yVMT7KlCGc+l09nES7t6buCovKZei+SfY167O7IE0nM5gtpEBCbztgYV8y7ABF63Hz0FZVnqKXKqSsrTAUEIy5zjehBmc40pPGBIEVeFUBk6n'
        b'pcgQzkGlSmqGhEBDT+IggdJtjnoZwSC0p6VkyHNDqeCMHC1wOoM9zM1ueInmP3JJWmqvMjemHxZe5x+HSehQebxGjUiJozcSMrjk6GmXQ6tDwrDa6gK3wV3JPVi2la9p'
        b'00Wo38w/R/rWPH8gqThNKzwhYe8EJXwXkkUiMg9XhzPBoSwixNICVWkR3rXC2zxMN8SmK+BsOi1GUU4HFpVIxle6LoIpGDvN4YRcCpbThZ48eXILDNB1SuG8EGqJUSzx'
        b'd0O0398ba/2xEvPVsdEfKllZ0jYhzh4Q8pg9mYCdq1PszF2dwQ7v8rU0FuEWNKThrAp9I8o+jwNCY2IvnJ18uw5pXOVEGz0tvL18CaZa1YiP+In1dFNGKCvcvbCMqAXc'
        b'PC2XppHKU7A2H5z2ZP1YhfYCzN+KDddwnO/gMbyb9Vx1I2rhaUb0ohbKvXwkBWrQIQFN0Xibo9jHhVsEsvZxAoFqyLXDu3x5Mv49gbHgmt0Q+6XBS/v9BHwzDsFnR8Qf'
        b'DJ2MJPkgrDm85w2jjFVYxAquHMFuvp1UMfaSmj9KHDlHAZsEORfxdo7yydPHuYAzN01Bto8zHyM24HEVy+lDLIxDryAWWwSxxbV/l0i7Rvzl7997lODnGbflqOr4x7ru'
        b'f258+ci33/2369/3/jL79yd+8maUmuiSloFugeXOQ6qvSrzk3D2T3CsRYyXh6Pwto0lZu2M+NRr/k1GtJ3srdGT0g6W7H9/Nedh86vpY5J6QQ637OjM/MdN6/5Dpm/O1'
        b'9e8qFF+s/4O/0V2pw1mfiOabKtUHPGu7PnDa2//LT3V/M/g1e63yvB95/c9Fs3SLy/cDv2MRKGU08tb+01v/ecn9vHfhK/nqHw0OXXJb6ltaKCkQxv/G5KxC/SGrQxLK'
        b'l3dUaKcGnPB4LUztm/vlfpzyeuEvRr8dEaxRX34vXbKy/v19f8+VrPr7O798/42P3s9b6IqQ/999P65N/N2QZrRyosPXD+V8ujXhf66e9fsO/CilKcDzO8NSOhYvuaVP'
        b'/7b8vNm7+80fyE3MfWf8zB/h9c1bbX/Ykh54aGiy6a/5+j8L2nNp8s38GXgr47L/5YNjb09nfvethEudV1vgaz/wuGn2UmOIxx93BU3+6o/fOWx6zvsbvW9/dPvbP//N'
        b'6y8H/r72I42aV142//wXv5p5L/71X133kD74jlz+TjOUkHjf6A8WH59dvHL2Zz/o8w//9D0tmyuO536e/LbBJbOPE5U/2qli+95fr5z87Let30uyOxGYmS0x9vWffHpF'
        b'Y2a4z+AVZZ3gNz/6x8vnTwzlfn15Ovj3P9n315kb9weh4Z3y1vqrLd+d/bR9vqL4veN/efOg//9ub88aKA9yzjrRZ3DHeyrqHztzis//vOyHopSTW4dKsq5Uv/uWWdim'
        b'iOJXPnP8yY4/qJSofFZTfNBsyGro4+EWfG1E9Ue5W80WZb5/WOtHzq9bd55+feedkd7L//rmiEKhXX1XYMno3j3WcdtULj7Mtk9z/GdMwD9V/vaP/QEOTa4DH9v4K2T/'
        b'peyfP9ouMP6Xw19Hjcx5K7Qxtjz22MIw1HNObHV3CejGO+FcbNk+J2zjJIh9UM9JEDBqxsWPXXfa4rniUPe9iM1cmRw1LJaAirOYz9tv2qEeqlaMQ/J4Z220Xj/c5ewz'
        b'UCfETj5aD5owTxyxNwhFcItzyUMdVsD9x4Fmp/HhmlgznPLhwgWvGNuY8OYlGVhkFqaIU3ws4BTk662tGYtz0GmDw4bc2JuJ/LasMTDB3ZA1FiYPWOYtSBWOdDbri8HN'
        b'ShjgIkzxBq62TJg38fHGSmkSRMZwYp8QhmXERebyLXHMZI3hyd7aVB0KuIhB4yy4taYS3GHsY4YrYuc9/Kuj21TXVsLFvl07oU2H+04Hbwd6msBdWi3x5SsifyzYBfUR'
        b'fBONKCeuAi9fIdjdm68RbOLIh/QNY5/8Sv0XVxxhlj54CI2cq+6MxoHVAMbT8gI5FsAYFMp95Z6OXEswCxlswVnSGnqFp01N+Lor466nxHk70G0pKYQubDLjOzX3ZO3C'
        b'clOSAelFLIMROW9T4vYWEtgYwccI0vV0qnqKIwQ99FY8gCSJtnHXqr/1HCdtkc4yzclbAnEs5gi0i1aFXjdo5sMAR4l7ckd364jxqnCL96KYdGuBVXzFkZv+x1aE2zSs'
        b'WRFucTiJN4UOheQ+lm3rSKdhsm2TEg8JHee38KJttOdaybYBbopLCh6BBrFsm6bBS7bQ7cvVwKFd568RbQ2x/gnR1l+JP7RROud+NojJXkLDUu4BFcyTSML8HH4HeTBE'
        b't1BOEp0vq4tI4EgCmvFuqOA6TpveIJGLl3g4eScFZ5RwQmgNN4Wm2LvbSEouSFxwGe/mOntyV0P3ctiMROQ2EZSdi+KIgzG2n+arIxpggyeUWrjDuKFQsMWFNQCYCOYG'
        b'2AndUdxB7Cd82XdDIIM9Ilkc5iN4/Sy9eB6JBTgpyIF6rOE2KA/tAr6kC6sBNRTO1arV2CmBVUZ0fVxNnCIsOck/ctnK3BvLSFKnmbFFEjqcJLlHgrADSrhHfE3NcCGI'
        b'zqmESIv2fskjKbQ7riZVBelK46tFQa/QLa3WBeWLgp6CUW4wH7hpxxWKLGMlq1pxwpuVkK4UkRo9TIvmjmoe78pwVvBSUzpyH5Kgc/W04cFKAZ4mKBLH9nr6PI7uPaXt'
        b'xadgj2lAG06pZDIH9mXspZXK4bCIpIJCvM9BjjZhN92EmZGhmRC7zgjkokUwmRlgpPKfJ0k9tgL/Fzt1r/Wwh0ZErPOwf8KEqq9mGD/AGqkoc+GwmnxhG1bORriNKzot'
        b'KzQVqouUV0NlZUUioRazQ4tDZOnTk61bPpNUkBSu+/lM8iPp7bLceHzTFt6iLUt/FLliOpKsT/en0orSQlbwWpVbi7JQWaQuVOaM9LJciZ3NXGkcZS5cV1nISuMoc3EB'
        b'G3hS1xyL2Iwvx9viV83iqc7MPr9qEE89vt60/58VHZfh53k8MDcjP9nq3JxbwI0+lSmIW7J8JbdAnuAz8y/vzl1zIEYSb8mueE8fJx6GSwoe/yctWGMMuyAQ8ElEvDdA'
        b'TuwNEHL+AOYNEBWrFasXSxRrRGmIfQGSJdIFglypHHXm2w0UXJPi7P+S16X813xe4wvwF23gCzidLA4QXu8K4IzioWKj7qob+NkG9pUn1ucZpYvt02uGMBWbqcNDEze0'
        b'XYYxN4Q+19+I2Rmf7XR4EXs883BsOKvxyvKM9blcIs50urIO3hDOL4l5NWjpibzxeWNbuL5zUkSkjZ1+WGgqZ7zlN5wamZwamRbJjf3V3NvcAYpdF09WONrI50DDb1yB'
        b'Q2zRXrHnMxP6F5l8v6qBd+OuRNt9MlhSrgMOQ7/nakN0k1NPubfVoeKxh7vKSA7vaeMo7xqfITl0dq0x1Y1ZFrHE13+NVVWKePOgHLRugcqLWzh1O5akklaTDCwVO8cb'
        b'4Tbe4VtM3pD3kRYaMqXZFDJP8X1jhh4c8VdKLmxinWPOCAV/d89gEfI5ajhjAkNMoi7Ban9mCPX24jhv4FOxvyRvrFf+JU4r4QDU4jLf5roP+jxZt2yBtwAWbbxhFtr5'
        b'XPqAzH8IVEUCnYlj72UGaQQn8Lr7G61OAdzX7XrnBT8XCCydTlxJt416WY3/2qXXifv227GXvf8qGpIS6Ids0fc9LuD7ctvirA1dgrXgNNRaK0tlHGdCxH1blrXz2LSN'
        b'JWYe3ljPTLokQrqLTeVcTyYZfOR5ys3D1IMXDXEOq5U84E4MfyMPVALWmHjpnEefH63gbiWu9imH9495+podx3leZFpT218W8ngj3x0j51VrJ5P3cYqr91oFcxksWBZ6'
        b'5bBwzezaUB64zr5suPoy5MMjuVx3nOZNJRYSssXibLaQUB+xqcQpjj/GbyoECqZJSHfaGpPwxnkzUao04yHMXG4kxRlQ1HwP8uYTAfb6XyFtZ5q3i7TuYdW1mWwogEdB'
        b'OTDny9veO3BKxGftQYNzti7e4h+fxzwz3o7CgglifVBc17XVLJFJwVhhkYrlpHsdEMI9vGXCGatcHEmaW025422iUCpzEYqhkq9x22xgyukI2J+wUsB19/bYHT1DwrRx'
        b'Aridee871C5Xveqk+nL0Tz88suXQjY7vFioUq27an64ZEGhgLy9pf6pS1aNP80+NU0qJe9Rl/ib7YVXZ+7/SzZZ/tH/HubNtt//+++8d7Jp5x2/fB9KvXnz7rMv0wDvX'
        b'9r+V+cPXX47vDl8IjusfN796Nbu/cnbJbjZ8j/N7lbM/2i3/t9pfzOPe9Mnw5lJ76b++G6vf02LzXvKjqZcW9+4pfvtbr0YXfVre/Fru1aNRh7f/sfSK5dvn97/9w4Wb'
        b'5ffrSyP9dMfeCEr5u8Vbn5/fMvnLB/LzER9Z/aO66dfZBm/uH5+Qi3OMuHDn4wdvzsukxThFHN6UZWCd6LTbwPWvup+/O/Pghwe+f1Jl90H7TR+lXa521PTLeyg8/eeP'
        b'xqKvRx0J+9s3ht74pvSj7O+//mG855JSf1WiwmsFATXjn9f/orDhwp8/eSfsjnH28Gdhzi1/UXjtA6+ZFPuTI0vbHOz/+ZMTHcPOrpfd3vfzeH3nWzcCPzDSsUr5QfPv'
        b'FP/Y+tNQA40UE4+Pb52Luy7p+lHo9wN/t0fXOFmq4U3zrw9k/fLyO3989x8G/2p8o2z793TM/nojXejw0y2/3rvFPvKM3+3e706bNPw963+W/ym1T6e1KbXaSIvPoJs2'
        b'VSXlFm5JPA5jWZDllKaETJhYk50Hi3CXqbfupGxzaSW3MM9BgTSV9g0SC8tSOB0g41jWShUKgXQ8FMCAyIDe4BvFnIf66ywevs9OXMCii4Zc5LPwKs5ZmHh4QzkOrMS/'
        b'4Az0clrhNujcsbYyKqkot9YGuXpAM7f8KKhmXXks3LgayJXi7pekq+RxZo6gGzprml8qYPu5OAkR6fW8JQHzoQkKuI4/vpIe4uaW0l7cwF6+gax1jrgdDzZAHmvJgzdp'
        b'7Wxbu/WSTGg5nHovty9sqwhqDDGfG9UEu+Dh49r8ltAqMsNFRb426LA6c0qZMucR3PZd0TF53R8XxMHFW1NwnKniMOQlTiBUOSCBFboXLtID+vSAhDavBmK1d4Yh0VXi'
        b'ISbSgi3QTjooKYBl3Dp2HuTdhlyXQWm9RGwSSWKrOzcA8cApYCnCWIkla8gnp246YC9399Cy4zKvJppj4+X16iaMn+JUxExYyDQhulq8onI+1jexw4W7ygvbcPqJFhRY'
        b'ufmxthkGExwYeWOezoqqRydeYsBUPezQ/g/le43/onL3hIanuDYygVPxRhhb+Goq3g2BuSKnasmLu2DKijtkmnL9heg3EvSNSJJTtCS55/i/WVci1pGI1SiV59SyFUVQ'
        b'lVPDFLl+RSzNilfU5Ln/a3HzqHP/z9nyZBrEmv2IdTNpXityX9WUmEKyRhlT/b8+XyPJNZNZrM7IaWQ+TBchYTHNi53zV9PISCezfLZO9ryTWIkas2LLshZtoI8x+ZWT'
        b'XX0EXGy4FGlgfJ1/EaeTSTCtLEpxVQOT/NIaGCvwcHSjeNsVDexxsf/V8Fku6vb/OGKcf2elzA3/3gYFLs31nflAG24pzwgg4gLMmZpGj7r7+9oesLRialFCaDoLE0lL'
        b'T41NjH7mEvj6Oo+DZp4sK8h//0KZLLI+vJBYAh1Jj4VEmHf+gnhab6h34QIC9pKm0iYu3i/2XuOia1COO+d3PAo3I1b915zzmohx41W8FcgXs+/zu/64NcCKb1wPKo8R'
        b'p2iJ7bJ/RzItj57bY65iVnZfCSw1j/+h67ZTd7Tg6zolu0ME8uUGUseK0n00Dn5T69MBHaPX33716oOvpX6wv+JbHT3fLwmTe/2dQZWC4SP6Pwv7ZPj38WG/vJUt56b1'
        b'c90f3tH5wwfHf2/zrvd5q581h6VkJNzK+/avPW98Wjn+WdnrWZVZw0tel9/ehO/KJHnu/MXP8o2keF7ahxN+TMYoT1uVMVJxiHc2LGQdWZulj+UiS6jIDdzHGQG3Yvdx'
        b'haekC2xVJ3k9kmMypCW1r7GXe/vg+ArPhMULnLHdi3V04OzwAs3DnBV+N9Ssy4L5j7jIGiKvnMFh2joy7/MiZP6GYPNKxgzf7HiF1DPCnrP1CQK0ftb1xHg9NVpDjL9a'
        b'8W2itNz7VuvJLUdpT9LvrrwwpS01eDalff5GWaXZnNhkZrz5r9SbXMnBGX46vDU1PCY2U1xjSFwsd11Vow1IqTNvG4m/whlTYhOS4yOZOSgyYsczya54c09W1qFff5k+'
        b'K4INCZekT4Ypfd6BlTd4j9dKBsCTYVPHgqUFYdqysf6SsUXJDVJcN+LyKa5katDX3nhpuua+W+8tI6lvqYfHRP3zaHyYaWhiVEyYlzireLBdNulGnZEk5w+1PcOXD8GC'
        b'GDH2b87kQ9krsdJxRcNItJPm3WdO2MZ7AAZxUFmM/Rdt12kXE+npLCNwEy7rk9pOiH8fK1gvS97q4+69b3+K+HlPGJWBCZq77AubvKmG8te6Al9pHP7avhj+2jHsXS3u'
        b'uWq+fWKG9RXfT63H0PXlLB8/wSEdM7W2Kq7Ql6+KdHmC3z0n4/WLVs3qSUj5+AS4+BiJfPg/ql9QGO9xbQ2WpMul6HEJUFw8PWc95wQ2jpZwe+MPRve/LaB/ScqeeoA+'
        b'KiuIywHIiiQV5IVa25+scaeqqiqSFWqqyAqV5en7zbJC6X9LsoP9957r6kLzRHWh/nZZIV80qZ80usbV8qqq0LiaES4SGO6VysT70J3xCc2KNYcV4TbUOSRhu6UqFOEc'
        b'Lmw6eADywvGetD1paLVQJ0vq3m28uV0JarAQumEM6o8fh14FqIMy4RZ8BHP4SAla7XEaqmAyFGZwOECJ+YwL8J7DYXgEE24sO3+O9K+yKzAHwzBmfg3ueMHdw9dwCQdl'
        b'cIJ00hF4uB/64Q4ORKdY78ZWK8zDnkToJKV9GCex/ZoDlMMAlsJ9bdeUw75aUL4T85xz42wIzZdgLvYwFl123bw9dLOLvafUWeur5r5w56yeGWnOM4dhHgdJN69JhBEW'
        b'lQSzbjBrl2CM1dbBWKGEAxE4oUHyUDfUYS9ryYRNIc7YdtImDirDcVwaOmEWi5LgPtZipz+Ow0RWAvbBo1xYwOYAqNXF3svnsQn6Dm7Cu26wQCIG7b0WqtSOwz1/KNjr'
        b'SQuYxTZbuJeLo6egVYgD0EYafQOps21YHQND2Aa9WdskFKABprHL2pSOqRzv4GyMrfxhnIHicD3Ic02AWxE0dLM3LBqFuyRtd8GqWHyE7R7YeFYHxrOP4gPSW2/jhIM0'
        b'tJwyOk17L4dGKJTfE4BTOtiDvfSvOW8oho4gOpBGaDbFOVvH3Q67NDVw8gz9ouPq3vMsMWhEVQOLsQZmAtLot7XK8gYsaJBO7z7co+VMCLDZJvIQtl6AdmtYVMcu5TBv'
        b'qIpOd8Q8P2zeBuXBB2RxGR7oacCDeFjeAkXR9PpYMlHKFis97I0wOHPOwQLrCRYewEBaKIFdE7YFKOpeyEk8dBWn9S5uhTYf6NU9j/fojJpxSJY2M00w1Ya9TlghC8Un'
        b'8KElXWUTjNrRLsdofXNQEES3UG12hECiLBsmtbdgGZ3PAnYrXyf5F0tdd23elFEpYnFx5+lSb/sdhSqCe0VYxKlN15zoggdPQN426MAWM8V9eJeu6D50SpyAgfDQnUZQ'
        b'EyMJ5fo3LKDfNiMnRgUbXWhlpdCLQ3S2FckhgbC0KQjanKAN7kMfFIRihzE2m+zBB/gQ5iRgQg4btuBsqFQy3obp02dJNm3P9Y+HUdaMC5YMaR8EJTie6HmIhujUg3bM'
        b'PxlEY9cFQfNBaIHiMEK/fJGdN9bBhBk9M4lDMJJ7PldDNehG2D7XaOxQu7JPDceR9UfuJiBcgpv7CbVKXbd77bqyhwCuGlpxzIoAfZQA9AGWhGJdPCzStk7gApTKYL8j'
        b'1l2FrgzPo7E4vheLDUnPWL520PwGFF2S84cHOttYNTYcVLOVTMLlEJwUYU22VugJvAVT8lBx3Q1aMF/PFarOQh4WRqhAFwz5+p+2Dlffo4vDR13lNdXNLaW22JwmNLrt'
        b'hSX+dMEtOKJDus4Y5IXiwAG6yQW4iYUSWOcDtXhfHzt8sCwIR2BKUo2Ar0wbemkbjDQVBluzk4USHIPprGxdqNxG840TTA1lEzgU56jJEjpMRWEDzl+z1oR6OsNbdDcT'
        b'RLpmZKOVPbBLF+5i97kzOEqYV4hz2y/CkrcnLMOg3C6oSyOiMABFdpE4lYClQbBkvplZBS/4wtwWArlRrPSDOk8PtQtZOEPzDRAgdJ6HfEKgZdpWvjWOauz137XJF/Lp'
        b'wGfOYn88Hd2QL0wa4QMpaAnbBT3QHpDxOiPEywTnEwSSDlDNQJLWPW8C0xl22HFBksbtxluJodCdokB42bz/pCkMqIZ4wrAjVOAsndYiNm8hOHoEZbS1SbjnDkXnCV0L'
        b'DXDJzdHRAVs84E6EqjwWErz2E0TNwa2d0KafSVyiWeQIi1cEB8zdsf5yugld2xQMkNRUBg8JdeoI59rDzl9MJOLRa4rtcXTcC6yEQBlB6gjcgSZsuHCCCOOyiXZg+sVL'
        b'0O1NK+zDGpw2JMyoPWJgnY0VmnIwvxZeCTuaTuqypIgsLDCTuwHTiRzNbFC+Aq1ELAeOeh3I2REOEz5Xr2lJXHKFcm3Ij6KNLdMAA0SYCg44EvS2yCRAJQwGQ70SXfGw'
        b'vhLU22KrG3Sn0yP5yHbShZ3ElQYhT0WEBQ5EQvo3ycCcLT7U2UPAMAkPrfGRZhY+OIl3EjddkYyJxzzilg+wCBtU6Kz6aIcDLK7sJF1orxqWnd0aQ+BWgPedoI9OffEC'
        b'qdp492y2HoFvT4ID1oQQE2s2guEswogKc7qN3qPWROZKCTCJeV7Yd3k/1hrG4VDuMeUcWmMB5BEw98KUlb5hRChMEcmZU9TEenyIBYpY4gKd1gEEEtBzhRZQitWGMENA'
        b'MwrVOdgrs2UXnfMC9rmctYBH2CHvYkx7LiIa2U2cu/04TLlG+9FdTsHNtLN0o63EE7tgIQfLM6HlokwkNjlEuZpzXL3aM53YTVEGEYUaeqbpsKt2EDZD+2UoE2XqQAcB'
        b'OB0iATh0noujVS5jl8TuJA8XLE1UwtrIQJmtl3B8MzQz4LIghO51UYNC24xXGa29zzpFEa1N5ESMRbxngrPCE9tCoFsGW/3khXCfBR1XEda0QE06TAqI3u7ahHlWdL4t'
        b'elfxrgw8hL5IV0Noc4ZRDaK5bbr0eJUydsgk6MUR2LSpEDa2WBvho9PmbtB+6io26EGFx7aDxAjm5OloHmG5zEkYDmHYEipMvsDEoduJeA8XLgYSvWDkd4wIAckgSQeg'
        b'XcPJxE8d752F2pDjcPMEPFTFbtcb5+lcug9e1YAKf6+zMLwbp29sdQ4hwjFC1zGaQIcyCu3nrwixycUG5gMsryo7Yz60Q4tjOPHlm3THvTpqdNhF2CcBy2pYd1pbdTMx'
        b'vjJNqLnoFRpAqLtkc8o+npC4PgjqzaHAS9NCE4fiYcyJkK8kDhr24E1nIeZJnYSHEceg0SUWphx9YAFKjtk5nziOZdc3YyshAFHGfpqyWJBAPKAX70tDN2FCqRZhzCSd'
        b'VjV2WMMSVOgSonbshoVcnE1xJKhtIWZXhU2HU7D3KBGVvIhT2VDkmkQY0J0LTbmbCK5mIq7gcLQOthAZ7CFKUXYIKwPVDiABfA32uZJ0RCDdr3+Q1nCbPt1xOpjtqkpc'
        b'8fhmmPInOJyD6Sv7CO2XcMQZK+jkConndR3cxqSyVKiI0t/LYBFrNY9w5KCXlpkHnbHQFKaWk+mNHTTLNOFVM9TF0mqGSSYoEEFVBp19he5V2l47MdBR4ptpQdBjjp3Y'
        b'p+Or5E+sYjBOC3sisdGdrngAFy7A7RBa4l1HrnBSiR3cQobmS9h0moYovhSTyZgQ5ifo4lQyUZhJLNzlck4eJ7ZYuZzamuyYUSfiUrrKZQmuaQerQoQJPhAmYBUJEQ62'
        b'JjBnCROZCnvtZFJJiG1xOYN1x2gn0H2UrniJVWxKpTOaZUQoyACKbLDAKhRu08xlMJF81UFxmycs4b0w7KJn7hLxaL6xHfJMztB9P5C0JUrYBPPGB47g6EUS0RpxPpJE'
        b'zCriYiPEoGeQ6FrBDTNsUCeoLTl2Ebo9sMnPiThrTaQTtJ42JpGjDxbsabYqEka6YVGFcPs29KjisBtUWWVjnbL39ugEonT5MoQfnVflg2Fit/1xLx0HJYKvMWhUNtsq'
        b'GUrK7xLelle3w+nte2QlXPDmDjrIvN0E+f1qW4jHV9Gw4xew4CI0HAUiTY7ECYk6kYyAD4OxAzsPpRDFaoRBYid9JO1P0D0JT5qdgfLdicSp22HMFwvOYe8FeyjzMvWm'
        b'kyuAUue4Lb6up5gUU3bxOgyEGeHNcMjTuKqPzcSwas/jbCrBTtMpHA3BEjNLaBYRoHV5YfFRAq9lIuvj0RdJL6kh0l2qq0OnPB2C9YewGLqSbOn0h6yhyJGgpg9rrc5q'
        b'Rh2w8w2DvhB8kHSB6HL3IRX53TYHNXVtjIioTytiqcZxn73EDpd3Q8dpGrVOiUDrUQKU+Z0hHHl4Abr3wIBmBN5PpAnbaZu3LxEm9J+P3ET0pw7GzeGeAp1nGTZHQ+l2'
        b'mLyYfEn7CIzE00Pj0BpFFKJVIo5WledPAD9tA9UOsLSXGO483rqhiY8E8dhuQtLzJHZn/JTAUtbckAFlfiIHk0sEk9k4GolDV2RJvCjQuErnl79nK4m403qW6livSoJk'
        b'oF+OG9Tc2L77agYUheqcDFb0Iw5+h/1AwX6i/E1EReg1ByY2XVNVgrFsuteH2HXmiAKxyllYVgkhlbM1jrjtoBTmZWBjQCQsXU2kr9rDLpIoc5eTHoCkhwVYiiXgnwrT'
        b'wcLU7dhvSEDRS6gzGpCItdf0Cak6mLAbQwsouWSfoKNAb9QS3Wiiwyj3PkuC3kiuf25gTLaBog+SvHoH+w2Icg9ecMxWprMtB4a4NfAgMdlRHWZV0glL8lNJoqgJ8rGR'
        b'24UTYT54E5r86ZFZuCWDI0qRWHKKtW6lXxcnQ5sK6Sm3oDMbJ4MJTicsFE08iDi1xqq6xF1xJM2pdyuh6D1Wt3iLoSSdZaMlSZs12prQkKi//QTh6thWnHclqlVJysk0'
        b'seOHiSycH+tSduPATlJvR/BWLrQZmhHxeyBDkxXggI1rpE32jgtRhOX5hAoFGYQFbfJQZ4VVl22w3Ws3IcKUhlpaGBG/RRw5hyMXCWf6dhD8dRwkeWXOBorxQXIi3Ekn'
        b'HbyEdGVtS00ils1HiMJPHdpJy66JgUoSGKRw6DSxyhIC03rHyzhzWhcLJaEB70UCCyyawzbBziyH5HNpWifpfu8bGBOu3IbaiHTocIQ5x2wo24mlUhewPA5aD9PjkzBN'
        b'UicpQWeIS5STYNKh6aUMXR57bvgShI7h3Zyz8SQrNvs7njjIdLNRO+g/mmp8AeYIqqq94f7VWM0ookGtKgTg02Z459Q1V6x3MSaguKttgPkWXnGniUBNYaeRNJ999Agn'
        b'YM7TXUogtBAEkS5Thg9y+FSnIUKhgZXEJJa6StuCBT5e5c6ui54mIoHQSYAtV7HVCIu50QxY+VqWXSA8QmjURxLIDAyvVCRp3MrM+kKB0EMAgweIL0xhMxcClaGBzJMu'
        b'5OKx6lKwUxrnMlwlWGdSBVIXbhNXqiT8aHNSpOO/d11++3k5aDrkpxKqQdyp1pygopdOq5HJ7XvwlruLNxTFOWoZEcGZw37dHGJRPdDprnr0PJHxGugIw2oSWwiRsesA'
        b's72QBl6bbZ7hDCNaTNbLhf7IUCxWgJ7UUMKeelh2hLzAU9joQ1dK3xNOFp6gj30wSPvA4tPqLLnOgq7ttvW5XQSA+VtJK7hvfJbGrRb40pyFkURY7xEbrqf7Jk0n9hoU'
        b'mdPuawOgZg8pDJMEGOdIjKndQ4RuHOrsSF0qTA/2hkeeBPV9rDYJwdekHp1FAalnJXZG16DYhmS4h3QpE8QTumFiB4nEQ9BqG2mbKYHVMpEq2OJ2GYYP4INUk+04fwlH'
        b'z7lvgmGZaxmR3qnBREdroU+OWQ+gRU8X8+lgR4km5RONHLhwjsaqoPNsOqsZR7g7T0uo2U9bHXDYLB+oiJ3hIZz+1SaBBdakzeTRqYwjUdNla6iQwImzxr7WWBhEtK3n'
        b'EE7sIfwZtDEBlgUyDDWHSCaqpv3kpWpnSBJ7qkmjPfTB0vHzJFPWQ5kxdMrgWCzWuEHjEew+TYpVBWkwSzKbsDxkR7iR8xYck4XGEGhMJWRZMlLOwOHw1FQcoJ+6XCVa'
        b'bumBM0GkSY4TRa61wUln12tqUREwY6gEs8rY5UbIdfMgjlu4E4oPQxEy+06pCgH+NORvho5gIgfQdMTtnM/51MBz2iQUlRA7n9e2ZSWVbYheTGZKEJnohzEzLVjOiMHR'
        b'g6QQ1BhrYJs2o+Y5NFwxFFveIGSd2U9CYykzTBn5RBFbhTkLaE8nmCqGufNQnEicvA9GjhMaj3vegPFgUv066VbHPew5O8yiBHGbrvPRpFb1Q/VB7S3XTQi9pn2YOoG1'
        b'UbCAvZb0v2Vc0teCpsg003QdkrtGHfHBJSXMV8JFIXReunH+hHLGALGxFEPHJ+0zREzvOuo7qWTimJb05qw9BJI9EYQc+WFEoe+fPI9lHppaR0nXWIbmVDrOIgVNqXPB'
        b'Xn5EgGpsNhPoNME9XRyw0vHccRimrhIpKQ7S8TULPypDzO3BqTOcoWbSdzvN0wb1B+hEFuVpB5OJRJt6ibcsxeBsBswawT0oP2xCqDGAHYn0j+rMfdBGzI3ofA0D1Ttw'
        b'3xjuWiaRzN9pj5MR5+mgi7zPaDOJE4lg9wcKSe5bJKTO1yP8ue9K5KRTUg8HTYgET+EdjTMwZEDEtQranVK9SNbujCYJtMCJ0dj7kJ8bT0L+Fieidnd0VZiBywsHc9Sd'
        b'5WEk4SJrs8xbA9LCCQNqLu+mZRFjw57rRAnm9QgRbmcRVx/0viSIw+Jj8URyOi4diyYOMYUdkbTCunRixwX0Bksavh0eAffiTx7EaW1VeLTzHEFCiyb2HzVnJ2KMw9qR'
        b'OB9LQMNk/RHSHxZTcemS1GFVbN1ihXW+yUTSKjSwV53UsPqrJE7lwXIKiTzTR2BYzdfwiM0uYsLd2HhWFntck1jjaMO9GduMYrVOuqqrYbfGjQx7JSg6JvIhIB0h6CuF'
        b'getECHoyzrhB+XkWE2UCDzQjCS0XCS9mcwMTiGcmQpUE3qd/j5GsNx+aScS2w+FaEPafNSOq1IajRrBw7BKMb9/tTkShnl0wXcIjomutRBzG1WgbS7h8/aQXDdq3H+oS'
        b'Nrn60twPt9B5LDjDg6NEgYuDpQyOpONCVsZPmILbkEO4fdsfy1c13ECavRKa921nSu5ZPwUhzKhjiQ/ckzaD8fPSWjCMRAKn9xMU3LM7g0tQZh5rR/BZy1lORgzMiIox'
        b'S12rmikUElEjAC2CCdIQ8FGWr5kRXdcoLjoehWE9aFXR20yHXwHTEYSqd44cFsCwLtGVkd3Qaod5O4jWTcJYEHadhnbrs0R2it2hI+IscYR7Z5ic0os9Z1P3SknEHMYm'
        b'C+zPxlJzmNwZgAWJltAXd4y4Qh/teJBk1w4XIjgw74VlpmeJb7QbEy7fMtsRGIP9BzedS8VHPgRsTcQ5CvdpykJXXCIpB81EInpxwkeGcGA52Zd091qClwroy6FNE6/a'
        b'jAMW0JhB3KTZJ46gibSXZlOlRCiU17fHcbtYbPHQSoBF4srYbgcPj6ZiM51dNU6c2QbLAQJbvKUki8sStMoi700wL8XMI3fsYCBayw2aTmzZbEeaVxltCccPERVfJJC4'
        b'RzgwR3CwlEIK6JgGHXprWDjDm6gYQyKqlaILR6NTFGHmPA7E+frERl0iaXVSmZbQRtx2VB4nPaE8HJrPmGgDaRk3sTJOMRTHAqBawynk4lXs9PDeaoW1lnh/a8wFrLIR'
        b'MemVKFAhKdJduOiVfY12Xx6mSpyrBx9tk9wNTRp+WBQe5HrpmLcL4XeFAzam2UbgvAFRo7tMyST1UDqYSMOYwlk9jrzMEB420EG2eDmE74P7OGNgRJjbgneuEMJVwYQh'
        b'KUHlajLEHkeSgzbRtOURuHQyhW6nEkk6qJGDWfVD5kTROq9o3FDZS9jVSuTmkSmWBEPnwQRCSlpaxnGSaJwJsYvXgTapuLMSIm0cwlonlVTo05SO28vMO7Sf+0QQm6yE'
        b'HgHuTIcKxwfhOKVEmDVD2+8xPaSMNXrntkoSjLcR+64gSX4shw68cV+A3Gm4ewDbggi824huP1RgajmM6p2mEyflGqq0sNDfhUk+GjTYePB26LfG8RPGSOKMx1Y6pHID'
        b'6DLfTgjaeBjaN9GK29OI5wxGwv0gPQL0NpHfvi1wR9cO8sKg1IKEYAcih9tPG20hQlEXgwVycD8y9QaxrQKYPnuAWMpUJKPh5TLpJ21gWPEgnXE1tuoE0ynNq2Nv9Ca8'
        b'K2uYc/RwijbcPgj3vK4RXPUT3yMJUhdn0z1wWJ0EnWpioQsxxApy5J1T6Ro7aZA6A9t06DskaYXjR3bBkKM8dqTjmGrURR0YUFNNgfpNWOEZTQPlQ4OpjLU3XSjJGXQs'
        b'DyT1vZOdDvrF4V0DIg3DhEUdIQa47ELEqxluux91EBBqlBFekhBOpKuOhNEoLN5PvJmAtNwZJjbLCYkWzAVfILLXz2rA0qiFapsCiYVXwh1ZuBUDRXY4bEb0v+R6JtTZ'
        b'XkBmK+8VwNSlQ1uIojyEoti9hGmDOtBjRmjeSkgxQYp1R4ic7n5c0IbmAFvPZFdin0MwhOOS9MpNmNLXtCPV4w4MHIURKT1Cpg5Y3r1JlyTZSmOsuYY17GhKs2BSInnP'
        b'Ifpt7WHo3RuoRbc6T6wSm9R2Hd6FnbbQEhlEoFOCTanEmpayz+O9fYdPQ0F8OtHGBnPBARgIzdYMC6ODj4/BBagMg4kUEp9rSYCrpAO7b0+ktXCXHWmH81icau8Z5UCk'
        b'oATLrprR+U4qCgn4RhSZaEx32RqRlp0LD3zpn3egzYv09C64l+yGdwM5xjiNC4fPO0KzITFN0oJdHVjhk3FS4yOsSJJrOUvIsSwTRuJangHMxGQIJVjqSPdhhkf5BM4M'
        b'kZZwwYRocQtB56wdTuuQqBuE9fKxzjC6C9udLaBWgvhbtxJ7wkE1lvTGxavRbm4kDBR4nLbTx6KcJBKvl3DwKN3/JHTJ4eIBmXjiOqNC7PHHh7tzIY80wMY9LioK/tgU'
        b'wTnYxpm1/8ZVaICHzKp1B+b9aIeEJgPMZERybj8MuGlh6xW/vecsaG+NOHIY82+QAjajR7yx5AJ0nSZRa8ZMOibJWgcm3OQJ78fowUprOtaieMKBJRXsvgiFRDYmiLdU'
        b'WWHNFhnaY7+cGd69FkPiX1FYNtxyIKZcBd0SOKkjh+1ndFx0CGDGDKVUt+KDI6ehRtlJlsjmQ8xzJWFmlJG0/XiXdD8S8qstlSNPQuF5T0Pb9Dh5XFINzNnLlEDsc0w4'
        b'CdXJWG/tT6o1k0Gn7GKuEXCU7oUJNXtPwuEebXgoTzrY4LGgK/HGOLSbCNccKXaFl/BhtjwWnfAn1CgkvWSIyE4t6Sw76Lybt+FtRXmJKG0sPxcXezHYBts8lYUntOi9'
        b'caiVhjo1bUK5epiLU3Q3scDZbcwCysLAYXEzzDEf3qDeVtL5KsKOOJD83rmPjqMH7m41S4Rar52EGFWk+qRlQOs+uoYid5w5rEAS/AJJBh0ncrSxV/G6FG2izgXaNOSu'
        b'Ec7V0b9qYdkkMeQKdO6g3RSo2/rCjA50qB50UMzCmx5YqBcsg4MBUBcDnTBKcFTld5ZZTXEwg1m96OoXiPpOEJcowD5zLLkevIMYNQlBZ+jZ2z60mZuBOJtjTpIZ9BO6'
        b'1BOvLlE4G5ZxjhCyCxg3IYG07wDtbTkXGrZhXSTJ3DMpBDDjWToEV6O5WHwDSomSk+xxMwiafQUZvyBJySiTYHIFC5yYdao6kLgwUbC4I/p+KruwhjAgcNdV+rpDNzpc'
        b'Tgf7dG130fUu491oGJNxC6EpZklC6hcdwNktsIyDB+MUaD+F2J0OzAucf+4w1ElCkw6R8sUsbPWEXgmWFwAPI4nXDF0nylhNyNRAN1Ervw3veBAlHaWDr8C6a7gMC4c1'
        b'sfQALJhh7y5vLI9nzi53Zq6KOElHU7iHCEqpoiSORG4muJ++ok84Pm/lm0QA16dhTWurs9TCpp3bjbB9zwkSGAg3nAkUljRjcEYR2w7twH4l0hoLL0CBM847wahcNtGW'
        b'epJ+Gok032GNux5Kw209N2hWIPWg31IFeo5aQasNMeRCnYBNOLRzn7Q0lpxyxlIFvOl8kjTiBXMSsIrt8L5KMs5YKHpaQ68N1h+1d6JDmYI2ScL6PqL1RTkh+qosBWye'
        b'CME85OsToI8LSSy7kWlFsFbvB4UKHEjMBxP5Xr68h8hBBxYn0akNMDIwY0miR31UDNyxJWBmRvh6LNPGqQOk09RGQ4k09Mbow5Ak3HO0x1mmm2PeKaJe015ZxM0f2UiT'
        b'VH0HKgyxwJQO5p4W9OZCsxrBZIkBcydLXZM+EB1AIzccVsYmEhyks5gEVKCxP5G0PZLmbxKFqIUBDWw9rp3Noiv86eTa4OGlzN0wYgaLLnDHSApad5B01R4Ew5dJ3RmH'
        b'O2bBJP0Q0z5gn7QPHnrsTcHe3awAADzygAETyxM4JUUspdl9Bym1t3HSinjcMMORVn/14zYkY4+a4/LpXUTcmv1ClINzAzafJeApwbz9XjRPy06H7U65LFGl5DJLS7cU'
        b'NybOgHvbV0ruOOxkJXd0YYC3Q/XjWHCa9SH1VBFfH+6yoZEEX8GmgwTXLk9mVLIVJFyk5TyU4744cgVZZS+BQGgpgF6GLWW+nIUqEos0WK6VpEDoLCA295Du9S428El6'
        b'j/CuothIhoM7SBxrzKTFsQRBFQcNT1Ya11pwmc69LNWWS72ygI4rWO5FL9gJWIgBIUkDLnJfYbsxzKzW+6kmXt6ApVY0Grehh9hsh+VG9KKvYI8f9mrZckeQpUzwXO7N'
        b'GdZggdmOnGGJyygzd9wstsTRSZKC4+NjJOReSYPRaE8PGsiEFahaolPuJk2PfUO6YPuqKe4YIUv7EVw2ErpwjYe4tLe5MBGLy7S9phwSX+qnLzCS4Du/HeB+rWOvEqI4'
        b'pBTH1xqaOsb9UvCGcoiXyfYEAYswc+FG4/LkYn8qHyWVNknE6n9/mpRbH+i75ahmYXTWRWFBguLL0sestnr9YSlLVs49T1Oub6ernLrHn/wlLc42LLQP/lNwPf4HVYF7'
        b'3tsxufjO1R/8K+oHmv/++POU33kdsvtZXkpC7pG/vRMapXnZ86cy/ZuFvmnKqtMZwaca/3HMqDD53I7JD2I/Wph9dFFL6XjCu4MpA4ltir/J7cDeUuOf/fE1hQz//R9U'
        b'//K9k783du3ZM/7zuOj/mcrY9Eub7E2/trm2qTbRzrylpOdTx18feLcywN/OOKhkZ8r2jHrbcAezPwfUDQ36mXzHP2jwFac9lz7dUht1O+RHnbdfua5hPfZhsk//pU+H'
        b'In70PbW25KO7LbxfE8UcNZl5be9vBoaV3c+9PCzzJ8WEvg+zGlpe+4f73J13HW8qR/9i9sKrZ3/qU3Op+i+e41//9nu7jcKtXzpsM2lwaDLYrVvDzs/uZ9NKP03+yW2p'
        b'1KZpt+L0z+MvudhFl7Y1nnjTYP68W6/C27sWHOrG/npqfr9jUnKUZ1zETburr3z37qVlk5F/DR3crPG3nq5Ly50LHmlm6j3nv9F6+S8/z/j5qN/HmvVHBl75XX9rdP03'
        b'BNJ23+lOeKi2FOf8flJjTdeNocWb7t73Yj99UAOqn+z6s8/XZ1v0A44W/9tV+wOrCrXJnY5bPv3bz+oEf85q+rPKt5JPfHD6zdeuSbhYuVz3uuegn/CO7ue3txRavmz1'
        b'0qvf/+X49Ku/a3Rs7bVxjVb3X1SxWryz7d3vd7ys+KHLcts39OZN35na1hD58Z8Oa/324GeXbf599vWJfamPIpMsFKxMw0qvNKV3dv/iXxXzb303ayhdWalvm2+Y+591'
        b'v/2dA67fDtE10Yv8xpbf+IRuuhz0TekD9wt/X6yaOVHu8NG7guKHjjmW93pt3wrYfv1tXdv3kj79galLktL/vtsVHfC73//kQsANUfC7tsN/DD78J9c/TcKR3F93/fJ0'
        b'4b8/L/134S9kXxsue+ffUpuvnJoo7TGS58u/LKYHEDJzpARZMEoVjm7j0ruCcWD/SsC7Z8CakFd9XOYypmDuRKTC+lY7pEnkrSa/YU8yn8XV5JWmkKokp0T8vVwlNUOR'
        b'uPKchGa0QC9HUnYrDPEPjVzds/pQFs5mpVjCQyVpgY6TBLGE8a3pu+ghU6zxSctUTMnAOVaXrUJFVs1YSR4nVDKlBEbKrHhPvhbfnK5bDorWP8k/B5Xc2ErSJOrcF3hL'
        b'SsO8uzsf/T+r76zAPXUNH7ABZXFQZHEDq9NZi0vM+3/NXW1sU9cZvl/+wonjOLCGkCaAKY3jODQJtNACLRnQ5sNOGR8FBrv44zq5xLGde20wgSgkCGhI09Ch0sJUMr5S'
        b'FghxUtKkGYLqHHVTtS3015iuNLXStE5bpUXTULd2P7bznuuEahU/Nk3KdOXH1/ccH997zvF932O/z/Puz1FRr7mVnJ9KzFz3txokBmuU8eIxI7EI/bgr8SQDef/ONeD3'
        b'ksTvuvsIPReDJYKGv522rmpug03nHFyF9P76/wJ6rnFRjMT8IVGksdifEGDcHMexK9mif3Ic0NYcnJkXWDNv5MjG2wwOh8NiL7Kb7EbHvPl5Aje/Jn8pqd/BVIHayWqI'
        b'zeYFDvaLOkhbbP4TG+GYyLFr9cjtIMc+C8+vzB4x5u8q2GDnbbzDzrFlHYyTYzfqJU6ulHORh5vgUeaGQGtzZfQIbEeZAQGirf9hnJUvBw5H/jceyrbZaGde+Qwu/GEE'
        b'eOXcT4o5m4ys3hk0+hq6CFQnVbhFMvfjj862BdzUfIWsfs4R77mHeMh9kCcNdaM+E2NbyD++CXfLOz4/alDzWYY51fTOqt41Pn6DfdP1xk8j9z5vyTIuWfY0G17wiwqz'
        b'/StzbuI5JWCtvDI9efwD+x8+y3+w8lhp6u6DPx28f2l5TfED36KR9B3h51+kgvfPTp398eSI7WDW3qmsdVOrWv7o7m9fkH63uvyXQ07ngveuOw5o0ZNOXP7kiXV/XjSw'
        b'Z/9k5dY1Z0r/Pr2i4ezgvYsf35nibcLQxE/D17dNdxYO5lo33Fs5XLj7tbc+7TpfMS3/tVpt/vVvOkeeH7racXm6etdPLO8O5H3sGfvVb99//vdFZj5ryVNdxysi297+'
        b'sLPHdSBtzVn/pX1f8RJb/FXnxtU/swSWrf5o4VRrp+3mJx+tisZ7ir4Xmvju69zfUh86ax+IK76Y8K3n37//Zd7x2N1LrXuqL/3FVUz5Fwtxmuo4dDc0UCUKE2PFF/eh'
        b'UQ5f21OtJ2g9vRe9WdfgwSNQCULXc/Ft3m1H8JvoSb3KJOptdEFoAAwGSHfBjz1kMBx80fbHKV+6mJiw2yC36jWpKM0YBc6MR16ielg5aKwA96wgXurWpaiPwZeLy3X1'
        b'qAEnPukmZvMDdL0EiMWvsYylnCPrllMmnVlyDE28oNtIsgYZNDCCj0XpcjSkM0veeZmsskbRMMTeezJ6YTZ8ivcVEtMM/vl60sAglDpKMtT08CJKfA7gAXRUb9hbg3td'
        b'NQLjwGd4dMOGJregEV34ahB3bamrxW/gwTLfqiqWMeEfcsaSJCWPP7YUXamrrCLvnZFDW8IfQf3PlRZQubQYurwXimu8eqkN3+TxoFqxG43rQmYXhVzcA6n4+shi+gzP'
        b'CFtY4r9fRa/Tj95XhK8BM9BLrHYNwwgVLFkGH8Pj1O0IV+Jzbg/ure+oZRmhhUUTy/B5ncp/AY2n3CB+Vw8fq+Z4yaULzKJ2AXX5UTft89Vk9X2zDs4LOpV0uLUK3XBx'
        b'+PRifIJWSK5Ffeo3yueRfrhTw6F0Gx6muals+EJlI+qy4tEcPKaibjwex7daiXuSzTCFTsFUvGOG9zOMj1F2khuaYxhryovOc/gS6mzUFfl60TVYvoCWXdWzfCajreCj'
        b'9r8JT0br0FAJGViqTQZCjQ01qFcuXeHzuIzMi5tMR9BtTh+pU5Boy4rT+Ba5h+A3mBfb8cBjeFTPery8FCKpgSOPb21jDEdYfIVZSx2nNjS5Dso8IPTdisYPZ9hGBUkB'
        b'nUB9i+lQ5aEfbXV7tuB++H8Dd9dzjGU5h3pweidt3lmLB921njKvp5xlsp5pW8DPw7ef0P2yfnwaXa0jA1JXTt5KvjjkvPOqeDx0GF9ox+foTJHQra3ul8pKgQMKo9EM'
        b'fABIBTb2QsbJxOfr3bBeq2tAkwx+m/TrhZlESCVzf4f/H9mJ78yBW/IwZXEcDJLNTEn0ZrrNp2pr5gxXE1hg4GvAniOTopjU5KP/OaNsZntKp1VRj6FU4yNSVJGJMdMM'
        b'iWQ8ImlCRFYTmhCSgwRjcSmq8WpC0QyBQwlJ1YRALBbReDma0Axh4lmRJ8UfbZQ0gxyNJxMaH2xSND6mhDRjWI4kJPKixR/X+DY5rhn8alCWNb5JSpEqpPl5sipH1YQ/'
        b'GpQ0YzwZiMhBLWuTzmv0+pvJm7PiipRIyOFDYqolopnrY8HmzTI5SUug6mkpCtpVWrasxsSE3CKRhlrimrD55Y2btey4X1ElkRQB41vLbYmF1jyj5/0QQ3KjnNBM/mBQ'
        b'iidULZtemJiIEUcx2qjxO731mlVtksMJUVKUmKJlJ6PBJr8clUKilApqFlFUJdJVoqjZojExFggn1SBN3KRZZl6Qy0lGQbzqoS+m93eJ0gzeWhygBSAJkAIAtqACWW2U'
        b'KMAegO8DJAD8ADspeRbgBwCNAPsA9gLIADGA7QCvAIQA4KOVQwBtlEUHsAsgANAKEAHYDwCOsnIAYDfADtoyEO0Owt5hKpY3SyKEiWSZ9au+2v1Iv4rW/NocJvNGCjaV'
        b'a3ZRzOxn3POvCzKvF8f9wWbQMQOWK5RJIZ/LTOmAmkkU/ZGIKOoTmBIGITucZtRztSq/gyPtM+7wv2WA1sxrySxIRqT1kFBOBdEsAVyF//6LtH0+FS/8F5gkp0g='
    ))))
