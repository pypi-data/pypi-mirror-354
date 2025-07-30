
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


"""The Python Fintech package"""

__version__ = '7.8.2'

__all__ = ['register', 'LicenseManager', 'FintechLicenseError']

def register(name=None, keycode=None, users=None):
    """
    Registers the Fintech package.

    It is required to call this function once before any submodule
    can be imported. Without a valid license the functionality is
    restricted.

    :param name: The name of the licensee.
    :param keycode: The keycode of the licensed version.
    :param users: The licensed EBICS user ids (Teilnehmer-IDs).
        It must be a string or a list of user ids. Not applicable
        if a license is based on subscription.
    """
    ...


class LicenseManager:
    """
    The LicenseManager class

    The LicenseManager is used to dynamically add or remove EBICS users
    to or from the list of licensed users. Please note that the usage
    is not enabled by default. It is activated upon request only.
    Users that are licensed this way are verified remotely on each
    restricted EBICS request. The transfered data is limited to the
    information which is required to uniquely identify the user.
    """

    def __init__(self, password):
        """
        Initializes a LicenseManager instance.

        :param password: The assigned API password.
        """
        ...

    @property
    def licensee(self):
        """The name of the licensee."""
        ...

    @property
    def keycode(self):
        """The license keycode."""
        ...

    @property
    def userids(self):
        """The registered EBICS user ids (client-side)."""
        ...

    @property
    def expiration(self):
        """The expiration date of the license."""
        ...

    def change_password(self, password):
        """
        Changes the password of the LicenseManager API.

        :param password: The new password.
        """
        ...

    def add_ebics_user(self, hostid, partnerid, userid):
        """
        Adds a new EBICS user to the license.

        :param hostid: The HostID of the bank.
        :param partnerid: The PartnerID (Kunden-ID).
        :param userid: The UserID (Teilnehmer-ID).

        :returns: `True` if created, `False` if already existent.
        """
        ...

    def remove_ebics_user(self, hostid, partnerid, userid):
        """
        Removes an existing EBICS user from the license.

        :param hostid: The HostID of the bank.
        :param partnerid: The PartnerID (Kunden-ID).
        :param userid: The UserID (Teilnehmer-ID).

        :returns: The ISO formatted date of final deletion.
        """
        ...

    def count_ebics_users(self):
        """Returns the number of EBICS users that are currently registered."""
        ...

    def list_ebics_users(self):
        """Returns a list of EBICS users that are currently registered (*new in v6.4*)."""
        ...


class FintechLicenseError(Exception):
    """Exception concerning the license"""
    ...



from typing import TYPE_CHECKING
if not TYPE_CHECKING:
    import marshal, zlib, base64
    exec(marshal.loads(zlib.decompress(base64.b64decode(
        b'eJzcvXlck0f+APxcOQjhEBXxjhaVQAIIirfiWSAQFG88SCAJBCFADgQNiiICcogH3hee4Anet3am3bXnttv+dm2222u7rb2P3e22brd9Z+ZJQgKote++/7zw4eE55vjO'
        b'zPee78z8jfL4kaC/ePRnKUcXHZVO6eh0WsccYvSsntPTFUwznS7IptKFOlbHbaC0Ip1AJ0T/xaX+VpFVXEFV0DS1kDJN5ii9zwqJuYSm0iU0tUqmE+klGb46MbpKyb0f'
        b'ufrrJevphZROpBOlS5ZIFlGLKROzCD3PpXyy5T4PB0jm5ehls0utOQUm2SyjyarPypEVarNWaLP1Ejn7qQiB+akYXxh0cdCRWbSzJSz6Ezn/WxToUkUZaB1qywZxGV1N'
        b'VVBlzCqhna6g5lJ2poKiqTX0GlwzevYxyFl1lqtLcCFj0F9PXBBHumUuJZepHdQ/8Od5ebj6TekCCv2XRceJhq/yX0B9wuf9Zkor1QUiUlA0hoipoqpYA+uGin4sVNme'
        b'ULkK9IaKU9uU6H6tLm6uEu6AjfNgtWIBrIa1UXMS5iWEw3pYJ4c1sI6l1oTOmC+E55LBMeOIkdG0JQJl+7dkzOeazzR5hi809z5WbA3XJmi/0LyS2Ssr59jbhjzm/Pq+'
        b'Y5dQ65eJLMMPyxnrUJQDtAyCe31RuRGwZgCohXUpNmU43BTFUIPBBQ6eC1tiHYiS5RakgVqwGW4GN+EZFUoF6sFmEeUfxA6a5W/2QSnkrIMJk5sx+vEX/PJh4ESDuWCV'
        b'3iQz8CM/2eGvtVj0ZmtGps2YZzWa8KBbhLgv+kppf9osdWVF5XEGmynLIcrIMNtMGRkO34yMrDy91mQrzMiQsx414YucNvvhe198wYX0wwX744IfBDJCmqGF5Gobht7A'
        b'JrgJrlMpItXKcFCT6tGrQbCdUsQKYGtmQh6GYoruHv2KgBr7fnxZcnDOYIWNIsgSEmUzDRM9CKQ06zLf9aksdSLL+1PI1+3xK+i3GCqwbWCbcKF8NZ9FLGUoPMrRxfLh'
        b'3y/N5F9+HiekELCB0YYffX2GjKFseBBnDwj3BS0KBE813Dw3m4lO48c/LFIZBqujwhNTaGrpEnFyLrgmp22DUY5Jo0t9UVNUSgkHKsLgJnAOtHBUP3CLA3tWgHO2/ihN'
        b'r0QDHsEozXLUXHwnonxTGbgVbmFteITBbnh5JT/G/PgmhLhGOHOKnLX1Isjis1ql9AM35EkpAko4lwnO1ZPCLUa4X4XLvRgE6xITlQzlC3YxsAU0yW1D0PdYcLgPaIZ1'
        b'sDYVbkpKiYQ1yeAURwWBChaWI5RahyrA5fhkBqoSFYlKPBbwai9UiT/cxKrBbdhm642+9waHwWmcQjAc7KU4jgYHl+WTGkBdJjgM98DaCJw3JSUR1ssTUQ1wGwuuo8J2'
        b'o64agNJxAtAEt4BKVUwsSqKCDamJAipgCDtBiTLQfE9cgnXgDlzH4DSJKXwSf3iWHQm2ieQM6fGZqJR63wQ0SIUQEY0KN7kX3MeOLIDHS+EJWyge6SFTfGFDlDJJbcNp'
        b'EuElWJO6OCsZpx29RJgIGuBpOd/5CAH3wTOwVqH2BedhQ6IiUoh68AIDL8C6nrZBKIUStsCLeoCa15CMRkghVyYJqJ6DWLgN7gJ3bJiU4fk18apUZWIEKq0mUZEUFZmQ'
        b'IgTbwC5KQQngbg40kR6Ae0FrDAYoAmwfipJE0pQvPMzAK7BpOsE/uB6eLVaRFLj1s8NUiCM0oD7cDPfCbXNnK4XUdE4Iy2HjckJNoAbcmAZuoGy1qIHJc8ISkmGDOjl1'
        b'Pk6pGC+YCfaAI262x3gy412Eq1fRiI+yVVyVoEpYJaoSV/lUSap8q6RVflX+VQFVgVU9qoKqelb1qupdFVzVpyqkqm9Vv6r+VQOqBlYNqhpcJasaUjW06pmq0KphVcOr'
        b'RlSFVcmrwqsiqhRVyqrIqqiq6KqRVTFVsVWjqkZXxRnGOHk1Vc0hXk0jXk0RXk0TXo24dXcSJMDJULx59Xq1bQRufys4MMWbmQCEiE42TbgJOAHayDCqYS3YB2pHTUeU'
        b'qFbKlaAaE1mQhgVnn3HieBk8WgprEXKyFLNWAnfR8fB0DPmSAFpsETOGg1ZFgoDiwAYaVsynbX0wCMdBC9gaIVfC6kRhACJNcJKJ0Izgvx0Dl+FORBhGWKNAg80l0uBW'
        b'fCL5lgMq4Q0V3NcXEST+5EOj1GezbSEYDSrBHYDyqcOjEjAwXAINLuTDXYQTiOEWuDciUs5QDLgMKuPpdDtl68t3xgXYqgInERUPgHVCSpjHhIFj8LotmOB5kFjVcxri'
        b'vojNoPqeocEZ/6V8devAGSR/MNbRqNCGHFhPJ8P6aFLqeAGsVBH0UiCQTtKUMI7pAw7Ac3wLK+FpcDQiCdFhqh2eRs2PZ/wVEh6eM7AdbCDFhilng7MoawkzEhyM4+E5'
        b'Mh9sQEwgDLXDBK+G0ZNBC7zKF3oN3FqF2G4ShmYXgq6cnjUaHCFsCpTrwH5CIXJEzGJwnBKDOwyoAnXFpFiwH6yfDGtTkNLC2DF7o6eMAQcJPPAOvA5vgVNwE/4ILoDz'
        b'fvQ8eBb1D65UAQ4tUinUmNrAOrCBo4T9GInaSEbfCuoAIrEEcAZlLDOY6FmrwTUyGPPgPhnirJEY0k2yufSzweCQTYYr2wJb+yGugsuLiEwEzajeOpVaQPXJ4WIWgxME'
        b'otgJclUElhlJaJQHgirKR8iAphR4OotxYj/XRe1BSk8V7VZ7mGqk6JSxiJQYQkosISVmDdsdKXWv9rBq4yvDYmjLZPRCcrjoc81LmQ801dkP0H/uj3Xxe3wSYmnjv1Yb'
        b'ZH7PL1b4Llo3cUdlXZ10YPyPhsbxl/03aoSvBVNvCfz3vrlGLiJ6DTwbgoiCiDNYnyqH9Ym8xrII3ggexrF2cNZKeqgKHhrvKfV4mYd46lF2EDi62BpGZAusLCbCU5GC'
        b'2GANSYmYIZ96MNjCIYlyB2y0YkEEN8CDcD1OnYrQFTTgJBLYyMAacAiRxs7+VsyE8waAK840yZGIgeJaWXB1FjtkwjgrIYeqfgkRyoREcHI5knaI3i4yCI2vZlmfwQAd'
        b'5pBsxQB1SAMemGUZw8IFqeBKplOH6qQlkbdER3Jw+VrLCsatJK0R0/yvPy2hzT3cWhjnYHUWq4O1mLPMOKEZs0I546F4MeYgfN/TVTLJvNZdcIWX9kVI4HgOOImIpx62'
        b'piDUFFKcArGBtfB693p2JI9wjIH5rVo21x26/euX7xkLxpSVB8d+rll69/XnGl+4/1zdh42/u9i4pcc9f8P7eTQVP18Q8s5cpCpjApyxZpFKPEgRhrihikYUf4opteit'
        b'mKuP0y7shEPwANhAdCd4wMB3JNP9KNisxrwOHXgtJQ6kzb2oDh2YLcjMfUTH0+be7j7HWapxMYG4mHLqoX+XXq9BGLcxAm6JINoVYr5mGtzhQJu712nn31wXOHbcmxvk'
        b'tJoHxlmfj3cL/E0FGQWZBpslS2s1FpjqcGbCOBhemTiA2CLSbCDpn9SkCKVarUDa1RWi4m1mqQhwQYD0tovw/BMAyXkCID4uKPSNHjDg4YE3wSUOgbAdnHYCgCgqCFaw'
        b'4BbYreoe62Iw1tEY75B9x/1KzMvxxDya6o7RCToSuNjqYHd9hK1Wce76nsRYszvXJ+kO048NfpuyJKEXu/I+PvXRZ5ovNA80n2VJDRptmPbex+HnS7drdC169Bf0QHNW'
        b'm2M4rW/R5mRKs5G8T984fqN4Y8LGicfFsqhd62IHIlnrl3m7t5wm3LMUGVI3LOBMghpZJmg85yA9Aw1pD9jIgraRoBKNFMFUrjMb6kQFgowsbR5PBlKeDIIZxIYCETta'
        b'1c+SYzRYM/Rmc4E5cmJeAUppmRxJMrg4FKc1Z1scwhUr8X8PYuliIzJmTAnmfm6ywZx2hwfZfBHkSTZYTQVX4c5pSOmG1ckRSLsjtjHcihh5DeLuaqQAIOVqG6gVGcGm'
        b'tHEU2DTFB6H21iHG+QuyOYscVzrmyorsnOy8bHWWWpuszf2gRf9Ac1L7QJO38CuDhHAZ/avCl6kZLtz+VT3m69Ernuyjd6DQ3L+DffA28WN6xNNqxvm2e3TGV16dgWUb'
        b'M3VJp65gQkAN1R9c55D+eRhe7p6WuvhuHk9FXdQFpgtWc+p5xv/8VMVZsJ2V9q5KpcXaQoKW27pvYp1cFtdzl+4rjdjwfrKIyr4vXDtyuJyzYjIDl58Fp4ncVSuUal5k'
        b'9mAGgIssEtSXIqyYY/WeA9qIbA0ajwzusCRlJGhIRa3eHJEIzoTxsnpRhtgAt4dacfXxAiTYiSj3TiMe3Q82cUhlOwgaiGYANif5kILlScnqlCRkJBn1vH4Q+oxgIFw/'
        b'yhMDPMbaz2bKytEaTXpdhr4ky5NKBgtp/tc8oGPMHSxK5THmtGukB7pHGqc+4DHSH0k9RxprGM+Mzowg5nEC4tJ1qhQ03ojMhX5wEzVsFVIw2kCde4hcY93Hg48Re+63'
        b'8U2O6k5ii9V5uNHlOrFYs/glKR3/0pq9lreXLs+OK2rTCyiilmuQjXw5QpmICPIS6u5zYK8AHqbBpVWgmjhz/j3oHwHbA+iwb6jB5hcXfZ53h3fCPDefYmZYGDFVqJ1y'
        b'fep0/uXPfj2pd4Yn4FKXHhlppoyLJuzgLKXoGYYeV2l12hZ9i/50zpcPHmgKtdVnWvSfIaL+TGMyhKed0qbfbQQXG3uE/07cq7ZF3KplTm5r1Z/VntYGiz7j/igdqhlf'
        b'+Tad0GdPZWyv7+Y/eCu69yXq77vSFg0IaWtlX2pzxL4V03vWureqYt+KFsYWGijKZ8SQP0hPIaaLOdeaaeCIiowNOAHPYN+EGDQyBeCmvXuu8URewuVoLTkErWQ8Wo0Q'
        b'I+br+iU6IUIMKblD2skgD/bS15u9dF8/zScjmIczH/fAvHe8eAxmx1NBNbwGayXwegJSDhEq9MY2afOKxzhh6U5OWObXq4e42T5dkE2qtmGdFpb7muA2VF8U2OFPRSnB'
        b'QYIat+MEVPlIlCNeI82YncHji60PS8WH4fZq8l6dn0KZMUPu7uKgM4yiL/NYSw16GLlin/KVkf4gOnDGG7sv7X9e3vKiYKykTwI98NVNQ7eEre8femI9+LDX9ylFMy6+'
        b'EFH8z4yq0JqewtNX3y+6KJaad17LUD9fvKnHwhnJBr3ucpJvWtPQXGHoK4ZxBb+kF16bc+pswqW381feePX5vadurD02P+OHn/6Uu7NMN6THw+p7z1/Rfln/zcHBC398'
        b'Jvf6Kbkvb1iUg93TPK2meHjUaThhqwkchftJOtg+BGyxKORyuCk5XJnodBkXwCNU+BIB0u6Og2Zi5oyAW0PhBTU4Y1WCeniSdyz7wXJ2lNJOGDLcC6tD3LqzAVZ6OJaz'
        b'4C2C8Mj8Ogeak0BrRCSshjUKZMKDBkb5LLhtHY4+F8rg5c7GGS4DSe4rTuOsFF6zYgYBzwwFtRFJ2EuSjKxgX3gTGW7tDNxvyyF6PEK0mihkKCvC5ZHgLDwKNysgGqYQ'
        b'GbfcAm8SlScQXC/iuT2qi2f0ErhtKDLwkCLQAuusRNc+NRLuUDktBbAO3uGthRILsSPAmYnPRKiViaj7GEoany1mxT2zvTT7x5htwkJbZp6RlwKhPLmOZ5DRFkTkQC+a'
        b'Q1fekJOgOwkiWyltlnmQbG9vku1GI+iwKnC+ax7U+mIXW67vFHA7IiwFbkJ2rLBfX2SntjGgfDjcQqrLEjrJDFOT2EVmkSzW6O10X6pMWC2yC6upCqZMZBdZ1KX+dvYQ'
        b'ZRc202XihZSpF0dZ6RUS81iawr+LKVPwIqQE28U4p12Iy5hI6Wict5E2c3ZBYbqRKhOUHLYLDjHN1Axq2Y6lTJlPmQTXYvepYMwGUh+H7s7ahYfYZlROiQHdcSR1rzLf'
        b'ahal9LUzBtYuaaBpqmg7gmMGySVFUEqrfezCChrlCq2WVIvxfQVNcopJTrFHztcWUnap+btqKZ/DBe9sqsiwkGpkTKGkVN8KBsGuqKarqRVCfIegEeiYZppP3UibfiLp'
        b'aKvQwJC0C6p9nWkXVDO4bHfKP5KUQpLKXi1wpkJ3XqlO69hDIh2nE2xAFuMMqoJGve2nEx4S2f0OiXUinbiZwW/sfihvm87H7hdMlflViap8kQrH6iQon9jO4nxl/qgH'
        b'/CtonXgFrvFdu7/OF42Mv2mo+z2H3v+kk+Ia7f7NdDD+yun8yvztTCNjnoXgpQm8jDlU529HOfogfm1gULoAk8xO25kVLPo2UReA753vxbpAO3831CO/RteDz+9Og2sL'
        b'sAfogsbg/34oTYPdn1wDdD3t/nY/XB7+ZvK3B+AvhbvsfvjZyo9xIGpFIGpFL9QKxvzQHohbp+uN+pQxv8Q/oTwfoTux+/2H/BN+j1rZQxeMnildn0qmL2XvQeAPRLWH'
        b'VPvhGnIl9kAXDHa2kTXLrLQ9oIJeT5vEVl/+zqke9VXPeyjKQwa2STnyIaOQuYUh4xSIxFTGToBsRFrLJGW0nc6ltjBFHLbgnXqlQ5yRYdLm6zMy5IyDiYx20NZONvRD'
        b'ycQ8o8WaVZBfOPkHymlEC6lVA7Jy9FkrkHXVYYB1JHzIygrMD2nFpzQpocAgs5YW6mXDLF5AClzUL3MBGYwnce1YWjMWrhoBXEE7Ac7pAAuxxVAiNIsfwxTNWAz81AHv'
        b'p7jShwFaWbE2z6aXIYjChlnkRPo+DLHoi2x6U5ZeZrTq82XDjPjziGGWEQ97kBf41v2KI9eeHilduR/6yPJtFqssUy97GKA3WnP0ZtRi1BHo+mkgAfwhPeIhPfShzzDL'
        b'ksjIyGXoPVZgH/ZQyLILrK4+Go/+5FKHwGjS6UsckgUY4JnYqEOvUK0WB5dVUFjq4FboS5GFi2ou0OkdPpmlVr3WbNaiD7kFRpNDaLYU5hmtDs6sLzSbsYB2+MxDFZCS'
        b'5EEOn6wCkxVbEGYHi0pycBgNHELSPRaHAMNicYgttkz+TkA+4BdGqzYzT++gjQ4WfXIILXwCeoVDbLRkWG2F6CNntVjNDq4YX9l8SzbKjsFwCIpsBVa93K9b7fNpLkgk'
        b'Jbrln9iFiq9SzhgHisGyjqOxFPSnhSyWfbwUDHIqsP50MCMhz1g+EtnIBKOnfkidDaYDhb2I9BSje+z89KcDGZxfSvL7M1iG+jM4F3rD+JPyQugBqKxgLGEZfs5wF2yC'
        b't7G9lILMwL3wtFqRhLSYDHacDmx0O9LFBD2dhPAZuiBxxZS8a6cOUUQA/RGJK7aMs7OWAUX+VqS+4j8jEnH72DKBXWBn7OxERDLmNCQE6RVC9B+Jir7UIQaxR7Yv1YzE'
        b'DhJDHGL9HBYWFoOdy6bLuJJFdg6VPhuJWxaLEiT+DiDSw0JBoMMlCnQcKoXFT+g/Eoa4pKI8XryYT+q4wtM6LKIFdhGpTch/X0gh0UIgICUxE/lnzvnMTaSK/JEQZAgL'
        b'E6gRBWN7ih9M7I/iH5Nc7+QC80Q8xKxFb3WwWp3OIbQV6rRWvRnPCsjFDhHGvnxtoUOs0xu0tjwrQlr8SmfMspqfdRXoEOtLCvVZVr3OrMLvZuHMwifgmYc/Ewcm6DJc'
        b'5Q5CTMwynKAZhxACo1kgjwoY2QiCSekQJhA9ByKUIBOCcF/wNBWZB0xE+iSerkuBR0AVP8cWAa4I4A64D5z3MkJw3WQmHdfVZUKUwlOiBl+XhWOnXXaMp1HkVrB06FKN'
        b'x5muQSI+lyoMRHiGMplHIczwQ29oLDgraF9k7RDRhDACCTy6mq32xfc1OKqFQ0DgqiUIFKlB7PZI+tgZjEGdrXaM1rgniTPzCwwAZ8c6AlXaUrIcVcviJ6IrqcsYVASL'
        b'AaugV1DmOHxnR2CUsaZeBDghQu0EfIfeMLORxkfehFRjHQaRgAE9Y3QnWlbIQqpkmh2XO76MtZNSUdpN1UKEpizSYziTFN+j9+TJzpkLsaxBBITKsXOkjMKFOOApEmmb'
        b'nFVgYJDG+S6N9EiaWiVFHSXAcngh6ioderdG4ApwQsSBOq6BdrrIEYZhfdghKtaaiTuSzUZYjDipecVK8wSMXTN4POzwQKbgC0Hb5QTt9WazXPyrOWMHxkozCE8sRBXn'
        b'W6a68RVhKcNgLJViJsgw6DmEIfjKSBEehyBs7UevitZmZekLrZYOya7TZxWYtVZvb2tHBUgiL8VV43a4HIzkBcY6ue9v5fGsQ4S7DREuX+Qyd/N83ACNpV2TSizP8gch'
        b'9tuv76p+j26DS4lYgosz4HvJbxJAS9zgiJyVjaadHgOKlT1jwwMKT8BL8KoqWa1WhsnhnqVCyjeSgUeDwFEvb6aP878FMys9lY50vHRmu4j3YiB6FxsEPLFV0OkseU+C'
        b'zJzcwAeRIg7cw1+5Koqj0gXEZSpw9HAG180y5umTC7Q6vbn7Cdw4iuL9cwISeSE0CN20zT3dbEPX2Q2RmkhDgxE0wUOgqSOIBDaylD84yQauzLdhn40c7pcHDsHTQiSu'
        b'rSPYBFn4zunaS2kUtTRMBLfDM2CTDfuQZ8NzcXyWsDC4KSpBCTeB1lxYOy8sKQWZ6pGJyqQUmjIF+EwabCeRKXHw/Ny5ygUJsE6elJIMWufB6mAOx6jgEKpRYIcwFN7I'
        b'Md7/tpGxYAV6cPmFzzUvZrboW7SL7u4CVxvbFx3fIK9s3Th1X/Pu9pr2itZF7L1sYfuKkPGLLry9Ka/cvqOfcGSb3ccimi6yxI7NeJPZ4b+jsu456T4j9e29oAd7PpAL'
        b'yGwu2AOOgTZYi50TAoobtBrcosHh6TbiJFkzP8zpc4Cb58CNbpcDuABPEZ9DBNgK9uBQICUO/ypSglss70npZ+PARtVCK445mCeEtyNQHW2RygQlQwnBUSZ6eSyZC58L'
        b't4FdqsikOHAxRZEI6t1T4gJq2LOCdAHc6XIS/3ox6Zdl1iPRnJFfoLPl6Yk7Apsf1Fr0m00cDwyvaknpVYO7YGakV273PI5Fn2dAV8wEOjwUgkfTJWPOxfcrXFCZjRgR'
        b'MWFihwNVjn4PBHu4LJ4IiRfFuCfTJrsoxlMg04gUJW7KEfx6yhFQHtaQm3L8ecoBR+LGelINKAetTsrJCLVFYS7TzsY+gW7gVr2TdAoybHj6HFzLhi1dKKcz2cBdYKfP'
        b'pAWhj56H1XWah3XQhs6zsOKJedr8TJ128mqU04yZjg1nL1mcYXEDm11W2BEQl5yohFtV4ExCCmhwIyZs8pphY2OCLGBbWhA8Q4HTcGMPUM6CChKHB/fAXXanw7IO1iqw'
        b'Rw7WYtU7jR25vMDdFAHlMddKOCCv4TB4RN0ckK1GI1fGoXFkyThyZBzZNdyj5nfdKpcnBxyH4Wr0U6nwDEokP889NyECBz3NRwSslMOG5MT5HQO2F9QIKHBIL0EE3Ic4'
        b'k1tD+FhkymBLfq84nOIHvgahwyavQnFcqB7cjpoDq10T22gk89f6hPhYbaPwwLfAVrBDpcKTOIkpc8JQT22DNQuxGzU1eY4bhPkIXWC7CJ5DvXvYSOXdYi2YpnrOnvbl'
        b't6esn5JgnBcNkUFybbI2z5CX+YVGYf5M82rmS5mvZSZqt+ruZZ7RP4j/8P+iqfkT6PmxFfOqYj+St0Vvb9Nbeh+LjimXzd54rGLmPjq0/4uNv+9Fv/XX515/7p3fh7xy'
        b'd7c/9X/jQk69PdkZtQP2KcCB+Nhu4naw+xkeBLv4GJtdeQh3Ohgi5oaZ8IKTIcbDJuJb7geurCwYivhed0yvpB/v8d2dEeOcvEslNc0GN0SUHzzPhkwHO0noc8bCZFCN'
        b'OhE2uOb4IuVCKmgNC+sWLiUOanh59GDX59REgRDuoHzHMLA+ehaBww7bwcYw0O4xUd4xSx4ieHre648nvzMKzci8xmYOYb79XMx3LSVmiNXLITs2CNuuyDRZNbor49OX'
        b'6LOcbK9DcfIumSdzAa+RdSiuT5rwcc4L+bkzEN5sQpdK2iUnysnvfz25sw2rkdMGFnUwiqdkEzjWd+s42C6YCa/Fg0vDQCtic9Vyaihs6pULD+rzMHQ/9+vL/XPaLKQe'
        b'fDDiO+byyM973KfI7KAwZhetmZgZQMVrYt4xF9Af8a+jI74LOJ0mH8zMfp/+OaRg/D7KmPvhIMaCZ7E+rU7vXXfDD0ZLZyQmXZ5sYq++SPV9ZoKu/KpsadiyL9Jyh7KZ'
        b'e17RFPS7Pvb9r/76wfMjflh/t6FOFPnnpl3crJYfpha9nHJh3KQlX8UF/jLqVO/ts41fPz+4+qXhz0z+l2BDTOiJ75qsb1vOTbz5zoSREw+9/acxOdrLX9wvuH3ocvsD'
        b'86a+sa+G7X9+0xSFYeDz8z8qpBue6XXqVo+dyoCVu1qDwI8hl6fMLrvaqHDoh8mlBNXnCW3eQUpIR6t2hvCD3WR+ZFUEPORWRZAe4h/EayIZsIYoIn3yhnVQHayAN5Qe'
        b'egioV5H587XgBNzI0xQ/jiOiEG1Uo0FDo8jPmMTphMuQRnOFTJaABrATnI5wqi0BoAJrLqAV7CGkvlQAajyGvWekk4b7j+ZQHU1wpxUrevPhYYQLPNcguAI2ofur4JSI'
        b'6g3XsfAi2A0uWfEEdSa4HczrYfowrIkhNQzUwJNES5sLTsLTETioG2yHu5ASMIYGZ4Vgr3NuaOQ0r4g9sAGcxlF77BC4L5TAOhxZAFs7CSOwuz8vjMApeIkoavAUPNwb'
        b'1iYngfM0RY+lEEupgmcep+b8NpNF6OYXvh6kTphFmItZWN2aGoPDbThEh4HojmOCAoToGsgE0qsGPpZ1OHU3oog5hM53HQziV9uzSJcrxPe5bn5RgC5FXrrclkGeutzj'
        b'4ULslPhBJRnOFxkZyFDOKLJp83gfONEVSSUOP7ywRGuxZOkR88vgW+TzlN3t8HEWggog4OdgZHPZiGImxI8Ph6tFZNM0I+hRPI6hxoNbQoStd1ReRqPY+Z9EQ7qMRj0y'
        b'BJ2uIqzNCJAew+jYDT6PNA1na62ou0yoq9RZnLNEjCbuGXDsf3NruUTHJfFvPk79iKsWI/1IgPQjjuhHAqIfcdgpouNjBTvpR131XCGv56qHCHk1F9bDHV4GIgWbbVNw'
        b'T12SrUYSMywhJRJpLrzGkqhMQ5rO3DDsUpsvhg1R0+FBj+UVtIqiYnoG+CC+f0POkIglzUywzVOfVoGKSeh/DUf1m8ElyOEVokUiNalpjWeyiJCY8AQh1c/CzV8JDxmr'
        b'k2I4C3bSLM7VDnzxWo9yWa+Zb9xpy5kefDj2+PA62pBQXRN6TvrgrWFXx4xrq2dWqlcYopObhrd9E3J9+bywVwsrD087uW9u3NTw96T9//nNuTey3/h55XxJfnpO8zdx'
        b'QPNVwJaf+2w6vR4pQdgeHAkPwKtuNtwz1G0Qwr3P8LHBt+wM4pfwPDzlNvWQXldPtA1uJbhEmqICNXgFCNwA1iN1Rc+C04gxryd8XoA43FXQFsUv2MBYJwbHmBKwH2lO'
        b'uNeGSOANT/VKD4908Hl4GNTys9yH4H5wnWemy8FOFzetz+XZXKVxNeGlhVFOTgqvIintVHaejrw8ozwNCH8zsIlIOFmwi5OtpYZKpNi9L6XFrJjpRa/q3wXpI915eRoX'
        b'OtisPItDbLDlEabg4ApRWofQqjVn660eXOwJqhlifyvxfQm+4BAh8yo3FytGl4OdtJ6/DfDkY4+DU86o1U5OZi7CFzPh54TR5OutOQU6UoHZ4uqkx4kR2mx1g2VDl/0d'
        b'3AkpX1gmwC19woWgroM5ib1XOE2QCcGJqeAOMVJeRbIkfjnuH01y7mIl5eXOdnubxlKdV/gYRO4VOPRjV+Bs6M6/7M1N+qptOOAsCJTDjRaEsRd9i2zwMlI2rsB2K6wC'
        b'+4rhJd9iUB9QKIXtFDUJHhfANnAZnLBNQtnCVyASQgpkshrWR6hHF80n9nQi+leTqnQtugRnYLUiErSn4dVM4CK4LoF3wFFw57GLQlkyV/4bwx27Mk2Bmo9jvugHayJA'
        b'S7J7fLABk9BzHgtrlT34ZXBnxpowVfNNgk0RoDWMRpbQltyFnBlpHtXGQ1uvMBbsep6Rf+lzzUuffKZprU2/29bYvK21ovVea8XI2iK68VJjj3ui9t0TdqWFzN0VHFPx'
        b'0YSQ82/XfjE+JLitfF50jDVaEHs0mostPE5Tf0wPanyvVS4gRK/PAG0Dc5GBRJa3CMFpJhZumUWiXpbAO2mEH6CGgd2EIRiUhN9lL4kivgm4SZkwB1SSJAFgHZsL9iwk'
        b'9lUu3AauoSR41VAdS6EhK+fG0aA9WEdUOm6ywhVrQ4G9USTUBlaYnrgCwldbWKhHhIaJ3tuBtZZKlBJWEkjiaFaFI3aQkWfM0pss+gyDuSA/w2D0tJo8CnLVStjAY8Ns'
        b'St3EaEeX33fiETe8Qm1m46FtQprydVWqEumrm10jDOpTiWMB/eeFoNMioke4bSJn3yBpwPe+DhwIzE8FrSRkEjbD25QRbIrAXRsbxyDRcIBGWF4LLzv9K9ERqL/bVxbD'
        b'i0VSuC1VXFgkLeKo4Als9kDYQNY5gnW5Kgu8CNt9/Ir9JP5ieH4lJsUiARUaBHfO48pCkJjF4xgAm4epksAZJNn4kRSDNgZs7AkqbFjxAAet05GWvA2vDUgOT1IgbXz7'
        b'SkUYFv3JaqyUNywmXg+xcx0sGu2j4ILvdPSywjYeF7AfXolFuHJx6aOK6Jx/R54EVoLz8YT7gRNF+aC2sAhsXgkvwyuIn1iRKn8FtiHwUVvmxsIWDqyjAkiALDIwjqDO'
        b'xuDuVMEN8Cb2DCC5myxCzdzCpinAXuKCHpVr7FLmStgulQip0MSlCg6Vsy6S6OpkkRfYAraB/eACwscJ4CA8Q03IgIeIxhS4FDVmW6oyEe4AFUZwLiFRREknMfAAqIS3'
        b'iE89AJ4Ft3yVeLGXKi5uId9ojCROvgYuER62DK4TgZsieITEOPZEzPLUXFR/6ALYQoXCBhFh7oVlYmpRCGqARpP34bDRfIxj2HQhdTEfaSAyjTR4Rk+ks5PXslSWCiWY'
        b'rMmThs7l0zpmiKiW8f1w2uRPhgkpWyxu3V5wXIYViwjskaohHigvGEFzvAvMAlAuLitaaUz8OJsls1r3g5tTGm8ksVNDKv8wZXVi3Jiv6dWqb+nQ+YGqb9NO1/81lZlx'
        b'z0ehy7+8S5C4oa7pTwti6ysDMj+I/UHx3Nq4vY25r31gt+yKzbr53PM9F2Wa50175k7wubxDH5Qdm37uoGj4xR4R9bfHTvtTTFv72X+mKdvrnqVFA27HqWLqEyuOtL70'
        b'yZ7Pvr//xrR7ZwpOl+1YmDf3/rnwuZdffHHj3xe88E5ewaWV6RPfXvyfD0+/duMdy0vDb37yQJI68O3p/Q7s+u+x2wXvfT4yaf7NEPGcLyJfWXi+7QXR3srh3618b7X+'
        b'EPuX4jDYq27CO3/r8cIx//zf/9hQG/PHLV8mRX4i+vv0okmTraF7puTEvZX0s/y7+nePXX0hrwlw6crqzceTrqae+eGHXnFF3+SW583+ZMSbi75770P7yyrVz3+b0Nf2'
        b'ycpNp7Oq//Pz3333bFsQkDDrl6B3VoW9WyYPIP6sLNgKLqrwgv9aBWYdLOULz0ci1ZsphmetmAX1gWdGID5DU+hNI9xLTwWNobxOtw0cjXIyccTBTaAdnE0O4n1gF0PB'
        b'QVVyeCT/1TcP1oJWBh6dmE94fOQ8eAu92QEaFGqCjHhJWy1TBk/DcwQqeLQsJyIVA4SVDRGC6fY4xMjhFWREHyeV+/QeqIKX+nqtv5q6iOizvYeoImB1oiIRHEEUiSWJ'
        b'gAqYyBoWgFa+8L3w6DAVNiZQ2XKlOgC2IG2mTzIXD+9EEpWaSQJ7i+BF7whTcDyc91Ach9eEBC5YK6I4JR0HD4Iza0AL6S0hvLg6Iiklmaa4ITTcOwbs72UhWnQyKAcn'
        b'nSVinoxV8vLxCLX7gMtcAtw0k0ivLES118aAPV5CMzOB9BpsSA3u8Mf0z3IbAhXw1BOVUtHTugl6dyvliGRM65CMU7Bc5EhcaSAjYQIl6I8JovFVwgaid/2wCs5wJDAC'
        b'x9PgKWgxCZ0IROLMn0xJB9JBjJQxl7kEMrL+O2TlrwHcI/gLF3Krk/R8IcRTemLveQ7cF/UI2RmIFEWn+BRQy61i0PRshpwlwehmeHIE+rBhgGviDhs4++A2fiH9+f6D'
        b'Ya0anEnGbt/0/gLKF1xi4DGwDu4lq3lTOHgmQqlWhg8Ee4RoYA8xsYi312SxHopesEvZW4A1x86L4Cn3MnjaayE8U9XbEOyetBA8ctKCJfol90EoGkWJzOMnTZ9ttFj1'
        b'ZovMmqPvvC1LpMQrbaJVZrTIzPoim9Gs18msBTLsJUYZ0Vu8Qwde9icrwCF1mXpDgVkv05pKZRZbJu938SoqS2vCIXPG/MICs1Wvi5QtNCIjxmaVkVg9o07mRD8Clats'
        b'9MFaikDwKsmst1jNRuyk7gTteBKmIMP23HgZ3noG3+HQPVyks3jUwm6yrNCX4vA6PpfzoVNGnawY9RmCqdsCbBb0kc/uTj9zWuL0ueSLzKizyMLm6Y15Jn1Ovt6sTJxh'
        b'kXuX4+xtV2ShVobbaMrGYYVaGQ64xOC4yoqUqQtQxxUWorpwlF6XkowGkovvUDRWmVoMEBorNDaWLLOx0NqlIV7OG/8udoiv2obtOaT3nAZ35ka5pg/TFiYgZXNuQpIg'
        b'bdw40CqXwGul40BT/NBx8Iq9N4VkSIu071ywwwvxA12lJ3kjPuVEfdqN+kxVgCHwV87QedmMmEd03bVBqUZpCP9Qd2/DuQMkeJAo9/TgU1lyuOiuy5gEfM2E6xodt1+l'
        b'Ldh0Z1q++1yzuFX5cYJWanig+VSTb/hCk6jltnwqfbXOmPx23sz0gXWyb9V/mnjZ/09W2TLtm8+99RwVtMJg1Vb/X6vg89PaRh31uSHX8MrHik3MXnHwsrttga+c14Zd'
        b'9BWdD46O1Gl0DzTC3YGv3N1NUz8pBtOb+skZIlSRTrlrWIQyjPcj7QGnAxmlYiQx2HLgOXggAjZEhc/jkGyz0bBGPuXpJ6sEGSvN2kIiRQZ1SJG11ECOBCFJEIvm4zJ7'
        b'4dWecrOTMXkEHzlR2OMNLtFlaJEYv1/vqqH5DERy4EXq/RiXF6nc+fvAa04KGyal8OSCCBeyd7P4s0OkzAySRyUhIb7UPAu0BBjBjuHdx+DE8DhPPdVq35wnRxGI1Lbp'
        b'6D4vEZyOjR4VEzdydCy4AtqsVnNxkc1CbJmL8DyyRNrx/GmAWCrx9wENo/18wWZQDeoYZFHBKz7wzMQQosRf91dR26nXBwQEanLpHOfeR+9nJFKNVMtqTqMJT0wMdeLy'
        b'mdi7AosW3UW8PLP375uD4+MDBa//23DiwWvPnUtYf8hXkh8wdahPbOLbf3g/9Yz1D/XWvMLl0yWJQQWftl+8cLUkIbrGrIr7aUHh6DnF9do/X3g56b8HA6TH/ZYHPTtu'
        b'yGfT//Zyjxce0qGHepcHbUWYS/bgOAUaQZsKqXZ7vVRCKTjqnJQtXIJE9+6BLrcBcRnAS+D843xkT1orJ84wF1gzMrGljPo9xBOhIziCxL1I1EsQvUrxq1DZWZxrGsUd'
        b'sfr4ZcwkRQcil6NLWBdEdnitrcM+9eDxab8aj+GmKFBjolNj4liqGNQGRi7jceJyGUtw+a5pjTQ6Zg1lwxiItKKWNLhtigWhZCQVCQ6BsyRxUo6I7G91V1qiWK51ItBX'
        b'izkS3SCL0ii257M8ApEv66xiLBeiA2OtyS8OWMO/HDoVIyElvjvAGK6LeIZ/ebFnICWjqLGva7Kkm6ZNp/hdlI7DFtVcWA+3zx8dDTdxFDxcJkyjkbA6Bm+SbO10P2oU'
        b'Kit6zuqJbdxavqxDM9vpciQBXg94sPJ++O0x/HYJp2wRcwEuCtaDE8MEFKuhJ4MKUEckIKgCrYiOajusV3Bm2powWK1Iwo5DbGqQ6Aq4OQLr7KAmQiIH18FWMqP8M+ID'
        b'5f6T8TZ90rdDaOY9iixt/dl/hFi8mIo+Puxa0Y4lmyYUzn4tbviAlxjSwXATuAW2IdP5Wk8kWFKolLQJBPaeAeMpK54eWmVJ+6kwim/QrcmTqQ0IIzQLdpsXJW/Wk5dL'
        b'YqdQdmQ+fBNri/k6wsinpI0KWsNQgdHTKi27xMl9yctZsX+mL7JUQuGgxoJdk18czo/C4ln0doaKl+kPrtg1Y/0Q8vIDQ286GuHdXfvOskUjE1Q8goTZqG/Q/9nT64rv'
        b'T1rmS16OKp5PtzCozL5a39AkGV/76IItdBhLRd8dV5+9aNVilrw8rVtMXUUo0/js/lUheS3jyMvvc5+hkxlq7N2p1WUhUyv4tt/PGUzNQM2URW6xLwreEExevjcjmT6E'
        b'WjR7adOK+yVb1pKXy8KDaQV6WTh8TVm6bgFf+/Khr9OHWKqwMbs44Hf2ZfxLueUFqpqmZIGpa4yvrl3Kv9w+qYz6AVXUVoBk5qRk/uWkyL9SV2kqLDo5r7RqcoRz1fBa'
        b'KRWCU2qMeW8McKb8/ahCqhyN2uyIf2S+Zbu51Cj5wzzWchS9abtrmT/nRsNb8YFflDrevfWvSFHJt9+teefbarHYx+femLHxjU37FqXXVDwY/dyQV2dM/ujaRx9Vf6P7'
        b'JeAgFL3+t5kJ98wLV147fn31gPOG3tI7pRfW3097dv+XW03vDrTVvjRt2rKjk89fX7JA0m/jijdqv54ysPJ0752L72lU11+5+tq11/r6HfEZ/h07pO+J3MCEZz/QvzLr'
        b'u01zGkLv1VRszYp74eLR0Zdizhf4XFjXtK2iGMws9n84RLXg/ZamL/qU/knz7eBz+6Zdbw7x3frOHz6/ez3934cXty9/q9cFmWZF6b2xwW3Lv5z8zCeWl/20lxr8X17f'
        b'eKZ1q+A/Y4vvf10x4J8JFc/5vfvi2L8nW99eK/lUUzRR8u7LP315ee/ttIm9/woVOQd2ZD+f8k5u05WpH8RJTheJhsVdrV19dbOopPrZkroRJS/tnWQJGmF/88TEVy0n'
        b'vj0cPn2N8ty9EUUHPu5Tcj7WsT/34Y63Yr/615LZ9vur35AcjL6tuzjYOGLK6z8Of+Xbk72/fqD66s1DS4NG3/opKfuj06rc/3v5439tf+NO8r/NvwgvTgoLXfj1j2u/'
        b'SZmfq9ryh8ifKfX9zW1Fb8jFfATnPlg5xGnMr4LHnR6CMUv5j8cQN70TAauj8J5OzfmwmZ4NNsKrxHuQB48nRSQpVcpwtQBPIJyVChl4yx808otbK0AbDhbgpVQerHQK'
        b'qjllxDsgAxfKEAtJRQIdNK7i8G5aQ8GtOF7C3ZlqioiUJ/E73oHzSwVUACxnC9YaiPPAhizRZk+XSuoCX3ibgVcGwcP82tvNvuAECUoaOKJzWBK4onvaKfDAp49S+NVK'
        b'pNglOYnYXeopdvtKaY4J9g+UcLTnFkb4/yD0PwT9BtGhSAoOoIXkiwRrm2wQHUyEtZAsaheTtUP+KAf2W6zq92jR7Zplw3H7DpHTSnQIiOnnIbP/B6ueWPN6fE8WCFS4'
        b'Rf06dOndRdR/Ge4p6vFyA3AeoeQRIu1T4a0nCnwBFmlI87sJrxhteNuSMHAcbiHzTG5XLfZ0gDvwKr8hYhS4KICn9XP4aadyeCGtYyqNxG4HIlq5iPB5EGgFRwgjPObP'
        b'UDOewWFhGkVxxjCeO/5fvID659pgvJo++V++xfxL40oh9cXCQdh7rDDmL6KQuRvEWQ6iL/tExwbWTfIH0dJZXw43vnnx72PERSPiFhyNXPDCOzEMO/W8xfcqM+J5a8nW'
        b'//7447boywtlyT/MWFz03EblzqVFr/pdufn+sIKSl280H1n/yssjblZY35xzM6j3zvfzzDvLGsbcqt65K9k/oDHaj9F98vH39R/plOteYkPfgaI5X34bsXz33Oduv772'
        b'i/piTcF9v2Nv3Hz4l+vj9v/3i+3ciJaoKV+xUcsP1TjjGNXw7LPOTVVhHdhc2GlTVSm4wk/k7wYNEtzJfqDZ5VsEZ9hcfo39eexK8hwkHMSYjGfzDnDgGFVgSifOzbJg'
        b's2eiFAEVFD8unAUtYBc4RjiBdDaes4ebXa4qAeUPzo4oZmdEw72EReXDsxpQG6VUK+GmZLmQChgwHm5jM57lAckDFbNBbSrSabB+o3Axiv54af0peAQcyZ/qMguD/+c8'
        b'4FdzCBfJegc44d9eOLwp7Fkp8VkyeAUgE8zw6+MxRzBvwAPmSdc84RGa66Donv8ft+UR9I6B+6WTd7MirvMyfKStR/OaPaybEYmn6gPiWAO8MLTLxDL+sUjpjiAiHZ3O'
        b'6ph0TsemC3RcuhD9idCfOJtK90H/JdvZ7ZxOUM9vhYWn7zmdUCci60989VKdWOezgdJJdL71TLofepaSZz/y7I+e/clzAHkOQM+B5LkHeQ5EJRJPJyozSNdzgzi9h7s2'
        b'2l1bL11vUlsQ+ibGv7rgerxNFt4Qro8uhHzr2c23vrp+5Fsv53N/3QBUQ2/n00DdIPQUrCPrjeWDHf7JPH9P0Zq02XrzB6LOHlPs1fNOIyNhGF6JnpTDaMHuO+JD1ZWa'
        b'tPlG7EktlWl1OuzjM+vzC4r1Hi5D78JRJpQIO+adLkneH+h2NZIckbLZeXqtRS8zFVixG1VrJYltFrzdtpd30IKTyPQm7DvUyTJLZc5FlZFOh682y2os1lpxwYUFJuL/'
        b'1eMaTXml3k7D+Rbej4yq0po9XJ/EQbxSW0reFuvNRoMRvcWNtOpRo1GZem1WziO8us5ecNYaSTrTataaLAY9dkLrtFYtBjLPmG+08h2KmundQJOhwJxPNqWTrcwxZuV0'
        b'9mLbTEZUOILEqNObrEZDqbOnkNj3KujhwByrtdAyPipKW2iMzC0oMBktkTp9lHNL64fDXZ8NaDAztVkruqaJzMo2qvEK/EKEMSsLzLru3UI4ZB/hPccvzXKtAytjiNOz'
        b'e8cQS5aXcA8ruzqSTUarUZtnXKVHY9kFEU0Wq9aU1dnVj3+czmwXpLw/Gz0Ys02o36bOTnR/6uq8fsK2i0I1mYtZBY4sePRqFNAEK9wLuUA9OMeHJjWD7Sme+khYgiIy'
        b'EhwFe+FmvEdrHNgpXD0cnnXt4bxpyKLFoFGFUqYq8XKJ+lSaCgL7WLhOk2OMLXHQFhxTcTXegVd8hX34Kboqgj/VJDjXN0QuCNMmaZkLfftEr4yO0i29e76xedu1Cnnt'
        b'D1WXKq5VjKxVVl7b2Vox7MCkyiFkX7z1y3scUN1FxgKWmCvBNe0jBLcUHC6AlaCS+LCmgmaLl2Aek45FMztjTCH5Prpoti9qLrgmlLs1iN6gihMnSfi5Q7ALNkfAhoRR'
        b'3FhwjmLhDdo0Fhzg/WPb4d5C3H7YBLegPqDJNlFIoVgnIe5duDVlKKxVKUUUA4+FgAZaVQavE21gKNgN9uBSY4eNihnNUqJVNNwDzoIt5GtysRGD7A9Ow+qUZCGFlEAa'
        b'XgO7Yp8Uf+alzmcYEXZmZHSO4cO/UilZvIBV8lV9vNE20pVP7Rl2bK7xltTdL0pg+GS5bslaiy7rGZcXr9z9S/XyjM57FATdL5LCuqudynUtkyJhwa45J6Qj5bq7oWP6'
        b'Mh9dtiAwyFqpLtW5VlM97PvIqSxUCasryHoiQAYeIHGG02h5DDzbXfA87OUxmeWaE4t8YlUbXFVhZop098dUtdNdlQJX5dLiupk5y8ozIjattCBuLX8yCM7W+mboSwqN'
        b'ZiIFHgPFHjcUz2AoOvJgQdO5yzsqdzHvPm7m7dzBs0rgwbyfwqvvtVOKJ9vEL2KjwK65zyCrgsN71FNgs1HF+wbXgZ1mcAoBNVlbRpXBCniZTD+L50lhLTspkWjssRyi'
        b'/1omKU5l9NkzjbWkowQFU38YWPui312ZlFvpNy5HVn9MMCM0N/qcfenGT0f5nxtYX6zYbb1pH3vo3muF/Yb/uG1e+vejipRzX7gg9AsZ/XP7H8e8N0LYtGZG0Z9GXctd'
        b'tXhyy4v1f5wc2LsvU/2dXEK2RgQnwe4hXRgh2A0reGZYMAmc5plVKzyQo5ohRzZGIu/KhzcYUANvwztOVwe85KNCDT3h5evvA/aSWazJcKOF94IIKC5KoqZB21J4hJhY'
        b'4+ER/47QQQ4eicLelbGJfGDH+b4TCXhXJ3sysznPkqxxYI9IBRui8FkKHNwDK+JocHMO2EmyrpLBdRFgJ9ijTEjs2KA5BN5wrWmpBOtUy83uIwbIHn3ypcTxkg1vKMlG'
        b'3glYPI0DpzB3DgKnWLgRCbR2r63AfiU/1ZuyzKWFVsJPB3jz0yFSEoQhIaGMZEvVLjzNmduLqf6qrf2cG6p2MNUmdNnfDVP9++OZqhOA/6lWZOhWK5qeozVl6/mwB5ce'
        b'46LvTjoSUnV+rXpk0q/8NVpR97sNcohRke3adeAWvOytssAz4DavtoCro433f/qYtSxCKQ+Lv/Z7KSK4XNaLe71vyc97lsytiPN9DvaTLf7dIRNdfHK7dkxGe/zt7747'
        b'P+3HD8PDY7nF/xzx3sjYkemAzZx5d0Pf/h9l/uPry9Pqlr3/pW714DbN2MktY3odNIyU+xB6SgFn4Sler0CK1yyiV4zWEUocAa+kr8XuALwMFZxUhNGUP6xn9X79CWoP'
        b'WVnUgdkYrRELaOZRG7aDep44zoBW4m6Am2ikfNRwUTS4AK6DFsIzSm2wnN93VJUK6qOwloc0PKMS6XjR8JBwHKLXPfzU9a7F4DzSYCzwAFZisAYD6iMIkJPAZVClcoEA'
        b'yyfwqg9smEkASESgHCfNw+oNCxqIhhMBtxJeZFoBzhOm4OYIMWAn0nBOwX1PT5kBWQTfMlzI0TnOGP/GSMgmHb3oVYM60UWnzP8LrWcnurR0Q6AOLwJ9AiBy1iHMKbBY'
        b'jTqHDyIHqwlLeYeQl/ZeK4u8iZhzrQRwEzFHgpe6X1HEEunIfTCN7mSK45+pOh02azDheSgKvBnoFtSPpF4eeJ52E9B94gwXD8jUmlZ0pWA30TvbyueczT+izGEqmwkZ'
        b'kcrEGd1E9HhEB7lyYpMZZ/OKBpJ3B69Zb7WZTZbxMs08s02vwUE9/I4FOoVMM0ubZ+HfafPQS10p0lyw+mSyPjUTYtXGyzdlDFkB9sFc/eea5Xdff+7+c289d77x2o7m'
        b'iuaKcbXtu9sPntjRvnFkbevG5s1Ddg1pHFI9ZP0Qwb0PX6GONFBxAb6Ftw/JWX6j5cPwKCx3swmwF9xyswq4x0aslymgaRnPBhaA7TTFs4ENPsSBOnYmov/kRFCTmgI3'
        b'JUeCBuycDJjPUHJQJwBn4J1FT0+L/lqdLkOfacyyEL2UkGKgNylOx4S4amAn7PfO56RCIU9U+AQb82582eNNj57gcR7Jct1pCT3uQ5dL3dDjq170+HiI/qcUh8MFn+2O'
        b'4tKIdwoRnYnHMhyY5kF6Hn6p//8RH86WODdVxnuUrLwDitgFBqNJmyfT6fP0XaPpfh3ZKXyX0YTsCgMEXclu29nHEx4huyuHEdmRCIjt4EQ29tU3ZXaSz/CCL5GaWfB6'
        b'Lk90YO9KJ9ElZJNjTpD2uR8ptUmwHtZHIVnqSXoMolYkk4+LgjJSnp7yevCezScQXxohvk5aWGSXrP9b+sPboD/fDf3d9qK/JwL1mKNL6CrK4+iSR+9NzRLDmXuY2Q3l'
        b'ETQkJGKy5WciakOY5+Em7nC+ZtnMZsT+80o9LOnfgpT2SV9xJBByHcXi01HaGpsROspnNFeMfAw65tHUZ1Kfj98/g9ARWyHpU8FND1VxItjoxMaxSNfCHS4ER+AFhI7L'
        b'4BmiDRJ07A+ukEX94GqZENtfsF7WP8JbEoQLET5eE8kS8jsdRdMt9mUV2ExWj8GydId96eLusK9LVrUr7jD30ehGe+hbh9DlzW7w65z/4/CrS7X/I/zCnmLTI/GrI8b4'
        b'V+OWLCwcq2BGk6w4LnJUeDcM+Mm41jvHQhNcuzv00qkfO7Dt8biGWN+n3/i8tOc7F+trh7vKCLJNhae9Wd8tf4Jsq2eOQXr9CbA9qgPXYCus5M94WocXOdfiI9KcqIYe'
        b'1neg21hQJQQXJqp+Bb4F4l58Erpl8jtjdRr3zjmfFtsOo8tfusG2E17Y9qRa5X06rzgWZWToCrIyMhxchs2c5/DD1wzXdIfD171qxKgz4wOAzJvxZQu+bKOcrlaHuNBc'
        b'UKg3W0sdYpfvksx4OkROL6FD0uF3I44EYqwQDYmwaUJLpIl8r/yGbTE83H6V6JLPOMO9xb4cg8M33b/MAH+GxIZ0uTJBvgP8BgQMCPAX85t91oE74EBH7AO8lIIX+lx5'
        b'BhmfDBUG1gnWgiMep2XgH0zM8ZRzawvviVg+jNzR07kkwzlSZCPfh7KZJXjrQeyWzMLrLcwmrIN56FxqJOm8R858xN3qTm7PU+jyN8a9ApyjybmzYP/CyI7l37CNtOok'
        b'rMAtc81AJElEYDPE5+ThMFR4VQavPyLYGOz06xpv3CXYGO6G+7z4m6+LS+A+ckbiU96HQ3bshfqEmHyvBQG48K7uValazoce+uX7UpgXzC4YlXc/43gGidbMHiikBuC9'
        b'uGZJh/wn5Oth/6Dy8OrpguiJgk9DrmX/MrO//NqK2RknB7esuL5ofdge9e/Gjlpcr9ifembCsfHLBr4Zfjjzv4qHKWv9Pu7vV3ZzflvYhumjkz5Rl079YJCwn2TAO4um'
        b'pf9t8o3h+9KmzKsZuD385uAl06IS00r+HNBe8OUoB7slPK0wZsCx0R/P+F53YP5G31GKa0x8D8vQCYJ/jZswdrvqi6G20v2+ff2ur/0FidNG83UxWZukmAmbYK2n6xcf'
        b'JsskoWc+FmfLHBzGu6hEQmkURt9APuwmITeICqVKlvhRmokJwc5o0kxNMKWgysf6yzRLZb2iKbLWlNVMgrUpykh8zGeYc0cxuFklgltAaymsyQH1M0GTYBgFNgz3gc1R'
        b'4fya0NE48Fec7RuvUaQancV/OBWHCL9u4WSavItDOH6Dzzc2NKJBq7yJ9/1vv20cevFT2lKF3k+nqWH1N/zYkdLp8hf/XRQ8tv/i4RN0Atun/vIvh6ub87QF/fr++dUe'
        b'1SVH48Pn38/MvPK77JhPZw/6Z09fQXjffl/lzHtxwbZZldbEksp/fDt8Wf+yd65t5f4aFN6/j8l66f67+49PeVD+Iv31sR+/7Jdi1778zY3sUUUFexf3yaip2D/yx5of'
        b'/sueOj28zfKTnOOPkziRAG6oPF28a+BNpgBUgPX8aRrHkXJz3h0HRKbw9i/ziAMS+JGthQrgEXA5ApT7K/ERlrgj8dkU1/GRrFfBMSK7WLAPz/RtCg+HR7BPCy8mG2cH'
        b'FV2Dw3/rDqyeC+PNFq2XR3mot+yyciSMLhB7k5lAWsaI6V74ZJgzbtbMOjg8Q+8hsX7zxrC0+aybZ+EKvupGvG2XeQbEyNA3E2iBGyPC1aCuw1E5DbRR/cF+DpyKnuDF'
        b'b7y3v+nCb9zb3zzVMUbdT+VIXLxmqIjnNYHCddZFUyoXEV5z3eLiNXmq+yEJU4bwvEYXNKlbXpO7avzA+qKcmP6Lxw9esjLJdn388fkzZv5n8T/7/9LvlTH9VpVGaOeI'
        b'RSt6/WHgPxg4STqq19irIytH/b6sOGXssLVhPSeEzS+ZcpnLCDpWeG5wZsZfjBdFQ+cf1ejHJq14xefLxEkRfn1yFpkF5UM/nlEs+cxSXBjW5+2ZJ928psX3ooQ05cYC'
        b'fLL1+yt8ECsJjB3Lk7XKtydiJYEFNGIlNweF8LNr5EusD97csI0WxmuS+2b48C/zbfgg7PJSH5lG+u2wkfx5TmPAJhy8KlnrPYUFL4FTxtYVgzgL3lJu5HezlS+34z3Y'
        b'uLsnlhtund/XY8PFt+9FBBZueW2+5EYQY7/cNsZPcHXIc3dO/IWe+sX3R166P2Hi6LEHSyyrS5cfsv5HsXHHxl1zp2fr3syf/8+2gp+KJyj2fByycFGwflL+4G83/HnF'
        b'P6+93/4zPVo9cFfzt3KakGOPUHwK+u1U1+nQ4mWMHmmWJ7wUs9+8xw2hP52+g/5CvelvLSXC8+O9kJqCr5gGpYQizec6KJAnmw4CfNoNrTzI7pyTUDqT3foBnckO7BoO'
        b'G3iyS0zhqW4s3Ef113CgGQ3lRa+lefiP7MeZg4ixWsBvF26nD1GY3JqZMobcszoO3bONdEmYlcZpZlCN9LJ+S5kyrgxvKy6opqwM3u0eaZb+dsEhVidopssECynTILyh'
        b'9wqJuZA/PoZ8w0fLCPgNvE2v2PGxJfGkDJz/up01N6JUgmZ8iMxZdCcku/LjuoRlomraLsLbj+tE9SiHXTiRKtqDatlI8gsq8BEhrPl1vAM+aoegxISgFZANz3F+cZf8'
        b'YpTfgfLPIvn5Q1vi3bnD3LkHPCp3I403P68W8jnQO8qOd9xXLHRuve48liXTTul8+mJ2xbMoiRrxZr2+cJYZb4Ez76HAZjUox7pPF0EY3IbHHH8040BgM955WS4y47Vd'
        b'Dh+9yZavN+M9+ePxsxBvtK3TO6TzTUZ8Q/RUPu9EHuk6do3sKJZsfE5WL+EYHDPeF81B5z7lum+HFJ+CYYnhl8gGYfQcT/BUTOI88VkO/IkQQWSbfo4sygrxuJM6/4vJ'
        b'OnUxTc5QT0ea6VH+9Oq4cHgIbMCr8kn0vGwQB9vBkRSvyAP3DtiYMuyURayj51L4LB8yAEyFU51Xk040j3JTJ+2gLY+wHv1IszKsBRl5BabsWNZ1tiOL7RKypcgCsNvE'
        b'g4isU1jDb3pIlK8mIzUcVApKF4N2r8NX3JFYowiYOnoFbZZiW0PH2vGBObSOO0Thw1gQ0IJgqpm2030oLO7wG4I1QmcTSIwEM6yE3zaA49siWGUw5uXJGQdtctA5j2oX'
        b'bg5uFmnfeNwuiXO8OHL2BtlWJXvpdGyEo9bgw41R21JJQ4Xgch41fJCgdCA89phFu3S3i3Yffxxclz193UV6rKrsWKL2wfCi0LPUXZoq1AxPnVjKvwwc9IKsjgpkqXiN'
        b'T+XSSfzLvcnCiUqK7JaSPLJsEGVcUZfFWLLRl+PZgz/XLCN7Ll0CZypaKy7tfqNyyJ9O7mje2FwxZO+thBMVNjrLb7rkb9OOq/80rbnfRkGyb99NlbLDAxUDXxktfbVO'
        b'nhwUH3R46IDQl8Qxt58dUblYGna9fFylfkhWNJvtS11t73cqrB1pqWTTjs3geLzHEt8bVka5nN83IwjUgqsRSeCY3X0kGjkObSyoID6VHuDoYryP5VG4S40jyTYraJTi'
        b'FAPPgiMjeBX4NLgNToJTSdhmhDVIMV1j1TJDwQ7Y+vRLhXvkF+jGjeEPG8jQGbON1s5b2zo3ZxLT/DEsYnoAbb7jpqr/V4uBcTHTWVd15R6/d7wWBGNuVQKvgMMR8Bw+'
        b'xDoVtI8iO//ik1/wSaHOfhoLTgjXzFzSPbvAziCeSWBp18wf58GoHQKtJctoRHBdpNwyuOuBoKIcfUme0VCawjqPPKJYsj/Y0AV4kxWyYxmCAk+67+OQIVHJwOsyeLN7'
        b'SHA+fLAGkYC98Ek0GJ4yJ3SEPhi1+S4PxxQPqB6zsZaPzeSEMK2DfWH9hN9S6qAhOgJeXg3rPWHlKLyN2f4ePX91hxk8AHtsd/lkxo3iT05a7NFheJgNSzkVPNo/JjbR'
        b'bcQFDGEnwFO239hZht/QWQg6Xoou79RZmL5GLAenVKuTEYQuVdMfnmVHglZwyisKzX0GGJaBOhpxdKQ/lQy1U+ZwK+b4bAWD9AiqjOVPCrIziL8zRRJ8Ok9hnJ3GZ/bw'
        b'e4WqHaHRI2NiR42OGzN23NRp02fMnPVsQmKSKjlFnTp7TtrcefMXLFy0OJ0wxE+xXsrrBzRSBYzFiH7lnEPIz1E4BFk5WrPFIcT7TsTG8VLfp3PjY+P4odHjxpNjbYmg'
        b'E5JNYmz8Ft1gCziE5IEuJq7D2A7ow46H20BN9wMldaKLjj+pBtOW+XduPkGb7z0CUWLj+KEo8EAUstXLdnBSrrLCJgRCx0AcZaPB7cHd73tIzjym3WceI2geu9dhTudN'
        b'ALuercGpeQ/dVXhE7lqZDJvmp/jMQQZRWxq6XErzAw0MFQavcvDKpHwKXjBWbfgvbcGsvGLHzM81i5DM0dJZSK78TiN8LZgasRT+yKW9xcoZEjYTD7aDWnx+bgOsjRJR'
        b'PrEM3BsAmsPgbZ7Xt4mLI3LAVfeSQ+d6Q3Bt5aNOLjZaCjKsxny9xarN5/eAIMe3eDLzVeZX3QPDdO/i9vBa4rTWbrl0g9cZxhgz4c1V+DAABd6ZPYoArIxMhHVKCm5S'
        b'UcPNgrWz4Z5ZXiFn3o5H1hly5uF2RCPq+1vOZsf6QECXEe2hJnGaPolgM7i+WqVQ463bOErYj5EshYeJEnFpMHa+UYFUkcFuTUuhyGofJHKr4mNjQHtMNDWUEqnpTBJh'
        b'sXUxYRngUg+4Dn29HAMucegz2ElPhDvB5TS4hV+r36RZgijnGGjkF+vDy/NIVUpdXyqaoqJfDyxZ+r45n1diBnNyCinp0W2rLdO2LZtI2TAj1mUkggv9Z+I96qgJc5xL'
        b'62uG8Gv33x9kSH7Z33kq7rhUfql/Y7FO8WZaGEIRG1ZJdIPAFlUiOB0M9iuEFDeABuc18Cq/HFA0Fcdgj5UFrDDf0UmcK6gVk8nadVm+JsanaCH/csgaIdlb4JuYVdI/'
        b'PjuVMo54Syuw/AV9+X5wy8zG55Kej5du/EV3vOHg/rgFqavv9/7DoDLmPVC7/veyzOaqz2beW3p62veHfhB/uXf8C7ZhodzP9h+nLz3Q/wW/m+ai5InLr74yOz0natDv'
        b'IvpUfif6um1nc0Q/4+tXC+dsGzPol3/tvpSe82FNzM3i3QnXPvn2DfmbhZ/uezG66pn5K8bPfjXqUuAHl9pj/jX/q5qSmlv2N0vUi+Bsu6PpasBuy703Xly0pEle0rrq'
        b'u8QlE+df++NrSZ99OmTzX6fvXHFK2ZLXPl0drPxX+9g8RdOX2X/+4R9r4EDh7Rce7vz+v6KjX0+7aciVC0nwPj3KqPLwPcDLlN43jcS2IXo1uk64BRf6uDS65VH8gsPa'
        b'JHDEgojca5+zkWPIx4lDpCqvAFx4lgY14nyiChaD6/F4LQJeiAB2F3isRSgAF8k+aOAyaLThUeWo3MVMLj0lCh5+iv2//wd+S79CJG/0GYjpjI37f9r7EvAoqmzh2npN'
        b'p7MQQhIwhC1kZxNQhAAKgRCSKEEQBNsk1YEknU5S3YEQOm6o3S2rqAiICCLuqAi4gMK8Kv6RGWfGGfVXpl1HRx1GHEd96gxu75xzq7o7EByc/y3z/d8jH111q27d5dx7'
        b'zz3n3LOMHEXoZsLp6OYaiWfSS4l3ig6gHx2AMiR+MC+QIXAqhfZz6AbEym+iqIm55ojYG1qVereLotLFcNU/46BdUF7iuHgnHlhXZ6+o7Zac01GburtM3Vc4s6iANKoR'
        b'wz09csxISdukHuSG8pJ6R6m2vQObNuOq/kgWDEoYzg2q1DbWGyaAPTSF0FV5iMcYhGHgljBuXAi5QlNAUooCJvgvwV5qyuDSIFc/yBMQdvCkiqsfO4dEWTS+WyWykLKQ'
        b'S1TqQtIOeB4QdwpQMiOQpKoerGk0HCJu9RQXNI0xngEorB+Fp+sRxjQ+KiiRFGfZKDAE2t3GLm7munLqPK3AVTAFnt7CmDI6RoyYOtra3IoyFUdbIr7WHJH87k4/kAdY'
        b'hK+xyx2x+dyoV+THOJ3LG2X/UuV3mF+U3WfGKYUGvoL3L0fnqSO+LXeIhot7klzgJITpKKCHvQ7shHpI235FBQZYrmb8xTptFbk4rITlO1DbLmn7V2oP9SAGozDFgUVi'
        b'kGhWDmjWDBKpYXxfGOgdCGWMaycilEngJih1MLiCLEEOMSBihGQMB9kt4iBSCQvhKcUnxveQW6zhZBOds5mrTuVNXDS5s8VTUjiZiLpG75JJVw4evjjvyqvgtzAf70sK'
        b'Ji+aXEo08glsLMmYdCEU8GtINEfMPnetUr80YlqitHa0RUwo4oGLp3U5DAyR+lJEhHoiljZUxlK8ERMAEj6wGtX+GMGdjG4O4WuXkXlXVLQpSoZ/APJeyNCExHxj1wDm'
        b'JAeC6uO5K9G3ixquZtQoeXa0cNB89c7aWAipHoeNm2kkgNAW0jgkvRnHoHSitYoyFH938Ds5X0lAkIE0D3AutGMRlFL8pTfTAgI8FTqzAiiSTO0mPgTKE/vBqPBc+6z5'
        b'7Iu26Bcb2RferACvbKR3a05/p5+QSlUR3n5KyMmhwQDY0VR9i1aAv7bRg8c5bo+7BYbAvczt+ZFlF3G0KW4/2lIihPfFAMsmNp4ZmckaAU+O0pg4S71JvU7bXJg3qzgf'
        b'OcGt6n3qI+oa9XGEMc8NUu815WUN792OGWMUx47PARVxC0W3RPHxALoLTbeLTeYmy0IrPDPJZnpmcVuabLLFSAGBZwE0hlbM1oV2eTDG2oN0guy40bYwQR6ipxNlJ6Qd'
        b'eiw+iWL0JcnJ8E1ij2cpcio8c0afSHIfOQ2eJPXI1VdOh2fJZL3MLUyRhwZFYBTQPtm2MFUeRqlseSCk+si58I0ZWpAjD4J0GoV16EsMw/BIwnQYFLfXfzEwWNFpZ8j7'
        b'agykGpOoU3RXTpaMexp84Pj4bhr4Ez/Av1P8BKDjL+Zi0dUqoiMct4ZctCYpnLSvrbbefSzKMAldA+KaVXJ6xjP4NWonbqXITsMEZcw9Wc8Jyl8Iq/prl/RuuxWxtXlq'
        b'G70uyPCruAb0jW9ANEePmgWj5lSOmYy1Oo1FSLQ71h4xuRDv00I4i+0YLpRXYrxiV3J8zfhxj2GJVuqgYcFVLker45XPfhzoVNnxWDd7cC5RCW9bdMQRyXdeQcJoXg+9'
        b'OhPPVFio1YAoC82CMk5GiYAwkWvPgCdSs9mXIZsCIl4B0fN4XgJPLOyrdM7IOx/Kx6jDO1n4U2vVKX5EhC84JZSMgB6QbBgXqfIJDhK/8pRpZUH3MB/urixQtR0YQsXv'
        b'W94IO+dULmbTQD7RK+mjtrPJkV2AYmDzdZO79TdFQ7WK0IqVAtlkYfiHzB6zMP6bqqgfSjEectnGHCTI+ZkQX6DYyrBeDKtGUTmFrTD5OoBKQALBKxvqWdj4iD06088i'
        b'4FcwUPmfRJ0PxGb3nDVY4j/ZwIZYA5VvsDEWLKwWSJi4FirfcWclmr6Hn5M9mtbn9KZBaWegmqguYggmU0hCOiNE87sJpslagdrKG23F0NEBQ7CIhwdeX0ttG7Twh2iz'
        b'zcyfvr4WIhY3a8M56RoruLz/KurGoByL5813pcb3gxXfO5BHsm4I0W4I0W4I8d1AkPMstvUS6gi1v2c3GtFfkN8APrIiCnT+3HSmFSid+6pnP1JP6wcrv8dwRMVGePwW'
        b'gnaGROhHgYERlBwkQVjU527oC5KAuIb9gj6ZxOiaFmFNT2EEgaTgRksngKxnCS4XEFEYoN7lMjBWGfeP3ScqEnTq2+jRjx49G6ZZvx6LNVZ472N0VfxUK/mxvrFR8hZE'
        b'R7RMH1HY/2hERX1EJSOvjpClKkXkderUGFsTAwPa38WNMsDCF4WFGIMFofBzG2oTj6SnIRzToYKB551nQCZa1Y8E6WTjJ1TNNaRyve2cVperrrXV43IlSrGNM61nZSyD'
        b'TpzPjY6FwWJQuHKUjlIAb64ByVseCdhtsLvcKazjdblmGYDlPS5KHK4AZNzo9UeSkAaX3fWeWsM8O2L1t7LjXGM/eI8ajQORxfUmYDQrbgyYkyJFcZbjtDXCMpSd0Xia'
        b'SDnRxss0WWRhrUR8D8/UDgyRuFQ/6nwvGr2xmDsRm7uz3tPha1zmjiTiHuYCDhJr9H2BTcuBjnl9kwYPptNSRLU8YjHYgTywLRhdc2KvkvDnnd66pqCPnr6ScSJAAome'
        b'GwW2Kbr28eMos/Ea/DQCk9HZhNsF6TBcxbpFW4cEcx748p14RM1ncouEblO3OWAKCM1mRab1YcrE2DyCby67X8LjdaL+BnCEGZF4uzNgZs/bnfO5ziJYVRLqTkBt2VCm'
        b'pdsKtZsDFqjRErAicAOWfhzkDhCrYum2BWzK4QDveyKAuhc2yCFO5LxSwIZUiu+XAcH3Sxl6AXnh60ZDesDOoXFxnjINQRIr3xZxwJoAhrHRI8NwRyz+VpfcWO8nFQTa'
        b'D2BH8cO8qovYMCMuIB+RlozRQWeV+Xa219jrW70+ZkIX4WU8woBCI3y98im+Fepl5p+pwvj4LBtpGlSaJRmOqFDWRGwlczOXLDj4NIHxQqjBY6dIydJpm63eCSINkRS2'
        b'QJFz84Wysny+LD/9dDVf6s0DRm+UP0c79xnHGGrkkxllgPQH7fQEGtpnCC8TGlLM+JPA6xOQOhIXXercxXnxwaawNf9H1NebVbRKDpNVcJicktORLCVLaeY0c6olzW6V'
        b'4ImJnfncqe3y+jDC59pKbW1h+6yiKlNVOZc5RSrT9syfm89YcnWveli9P85gSaMYkfhFvpkbLY9Wd5nnOtT7dZ8w2hZtb2dFtFD1VvV+nku4RtAe6Y7TzzZ2UdJMckYR'
        b'RIBfF+VL+EhCS22z2yBLhJiSSy9ntfqYXhhDs0xKv3ns8FgHi2bynF3dLmirtUOFZ5wD4T/fXC6O102mQH+oMA6cLfCQEnCpPPPLtZCFdRcaRJ2rNaN3LshjkR1yIlyt'
        b'slNOuhG9e7GNIiXimNbR0rJCb+iZ1DHtLKhfwVgW2G/5OH6Sj/GTTKQAvyKJFyR9LzVVKR9z+l6qnOR0tgC2RlxTxGqySfsywcuFdLo3SjXRujOzZ6czRGhWMFWKkkhm'
        b'Phv+d/WN7825+2thDkOUHP6sW6YNyBLWkBnRweS70ntUF83SO1Wmn0sSzaFzFIZAk2qc0escYuQWojCXa1Zc1Rmn9TSaqffKS2kIZR7YPgcqgxF5CGheGRoiICDzjc2C'
        b'ARZQwqeMxgGMa+7SqCYTol8YIRpAhBhRRj0owbML4AjZVMbIHStJ25wka+utS+dE79DBe5FRz1kG0OJyedxel2teHAzTTquQMvQuKsBu+Lkl7KRfd3Ej4YZydhIL37pc'
        b'C+LqO2N2Uo5z6F3Zj/SMsPaiH6mFUXLYZPvpOwcuImUwjuGQ6E4wFH9yo9uB7R8M6EB0PWMMqFW0m62iQ0y2AaYXmQj76RL1gC8f0bS6xw+X7eN0vMdz2eqzknanukc9'
        b'2DvaQw1BA+3dLjaJTdJCk5vpdqEAT3JLTRYg1vQUnbgjSrQutDKRG6BBhhZtJDqzM3lFJLW6rsld7yeXdDqYfoJ8qIFtybi3/iPpUEN0VMSufmdW+l8iJGqO7TXnhIYa'
        b'zgkN0fxojZtk2b1052xIyGpU7YGfFcl+Tue7dP5TAg602a6MZJq6hI7EAB09YAPhrQneyroeL7/DTPzeQshhifF8WE6sU3F6FXGcnJV4NprkEXs5cAadTGP1U2MRRJxT'
        b'iVLs8Ou6rFHO96dgN1SM1KVSApB5TvqP8qmzw0xnIBNOX57D+XhKjpF4A3qu1hh51kuUwRgVhiVdLel4zCoxCswhkrdfdVOSGtL2VWu3zKos0cJTq2Zrq2dXtkfpE567'
        b'WH3AMiTF2vsizYpbpESJ0LEgUCe6C49If6PbBk66BF1nzm5tbe5oi55JmvS50ie67vTNKgQjqY8mYHk+ipJMjGaX/Cva3Mo6vLVFpW9n2UrNHqrzuhjDCGzV4B9pXQn7'
        b'oBfLuuJoO85YKQXwqttYKYAEUfSjPaM9lx4D8Wz1EX8UvN217dq68qIS7SlUfdXWlxSjmka7Xduq7laf6nGiFBWCYJmwg3Mk1hhAy4lHZmkHsGk7SZFeKQohy8eFzMjJ'
        b'hji6N8VEmQI7bROvqJwNMwe50EhCa2x6EvP9U4NxlUDPw1JUlYs5naKzTPKTvu6CanW19oR2ABaytvcyLcxpT6qHhB6zymzMqqviZpUcO2cxN5johMe2UCQVHTOgeDzd'
        b'sQL6l+g8R5QtshUpYdkm24HSNced6lgXWmgjsBIUnBGHPuSVQNArVWU9XGlEYX0fhxo7jQBDmd8mAgNtCJ+GArnLN6K6HTDJJFxHAllQ1kQFTqUBQX8DNFUmB0SyhGxu'
        b'QPR58Y7SUiaUjuw19IOJr4TOAQFhGp6Fm+BLk5GLmG3/fM4QRDYJDfBmHc8b8YfMKP8twolJAqrz8I6ootgzdsQXsbtI7uqq9XgYTkQ6wHCqQBm/ownRprgbGjtdqMNH'
        b'bE5E8PrOTaqFBW6WDOsxQUANCwEnBLpdlsj9cjIFhXMQbxw9taGRiNHtxuS3cHEaC0/igCDmh4mwRMKDa5Rz8ECcdYudGwN41nELk3PgobXvApJ9SCS1yO70+oWAhEfb'
        b'7FBQtqxFUM8z5CA7JNkKu0uAvsEpREMCS828CoaayqiC53bATLdjHvZGf04LDq1DVgnsyXyocT4XYM4dEqoipho8+YiI071yRKrCoNOmebWeDnfv1Ac7F0MpjSw0m3Wt'
        b'MqapIChjcUzHx2GhXjQsybvhs3jOTu4li3vCuL7Vu8yt+EnQ4ItXimBOJ6FIkmRG909D4mJCaRZGQnPr4hUfhXNjApe/MbRBqFn0udsjplZFdisoq/N1ePxEMrfExCg/'
        b'dlTv7NnCPZIuQ+B4h8422GFGCQLqi6bB/QC0hbJn8F39f6SfPc7NoqLAWRyqn8DCK6XZM65bBFqCtFrItqgEZxjJlMWdbKztARF2J0CPqDCBT/HZfHYiQEcbAgo+I2aA'
        b'lxvG2upq8KCygpcgZggBL0LITsKfUv7HyYqp8P5XMaZJ0g8EyEvqaStHr+iMbYNmVIiLPxFGPeEA9iIDj2SIs4c1tRN1heEdk5TDWz/diXA30w+IKCCkw2ZzA0/qBICy'
        b'dvJEr8EqgTUho8zOm2w8wTx4Ziib2B08AYimM4rWXMVOCAWXi82v9Mu9zd7W5d6c6D6eM3iYb/Ap88phPjxANCspCKyv8SMzw2DKKHyCIQ8YmSbGSFhlDH/Ggogkuryo'
        b'd4N+kaGA/4sgTY+bUsm6+D2dNwvJfFdWT9DGf9oDMyF8SWIkc/GHdDRjcDvGjVlgd41AGnTmMuUa3ToM8Q5+Q5ZrAXNAIkRfBIheYucyTbANNEBJ2wVE94YcyqyU8frU'
        b'UCbjD60/OpUA3hNdiwNFaYmTo1gNGanSF5etjUlFoS9xy7F3gSZ6hHo/RtUCjEQUW6YSrM5A3XrVYhUsAVuvDOfkaMOpCzN60rHnGLo0RtsC48DdHqNt0/smDwT+00km'
        b'RZNk7WBM0qbdpB3Q9lZqa9CnUXY/ST2kbfGc4bYa/1HQ0yj9kUSspUF3MB/yBtWBb06nOJAK1ukN0h5BuRtj5ZMj1tmt9c1ljR531UesqncnR+mOHof5iJRCxHbidPKl'
        b'+QWZp4XH2EKB3tGRXTqK3aQAME0uEwnfzCSIs6CBl8sa1fM51QdDuubIrW7d+zs68jplGeYrQY00HCw6xDY3+jAfraqIpbbOh8fmEStprcmNSsSCOt2tHf6IydVC4U8o'
        b'UmzE4sIcbjn+ND8iYQ7lMr43OhmnwpexWeUg4iCVCAQz35VigOlMIR6iNLsBJfQ4wtQXUYKFhmudy1Ykh3DBARJCxDyf887TjUGX8YCeeK7rggAsKkDgolJ6A35nVmaS'
        b'tIuVwzdLyiK/RRYQ2vDMKuvlyByiNzQeW8C1JwOTKTFY10BqvkGFmapOpBA2q2/t8MgE6Np68jufgwD6aOsW/PfQ5Ln5NmBeAJQEnoippRmAq1xKp0XVNcR/RkxuRQGs'
        b'MxcfOuZ0eDG7/sbncbvbdHwXscAmQ0XVn3URRySs/QdJP7XjyEJSIDN+O/k2kWgE0Ki3KzEKe/ymdyOLIo6JRpRcmeYjzEbegLmSC/CXDPhHmbcyIB2xK2xqmBp90Q6b'
        b'lBa41wUpvfBtHV5sSLIpTtqLNiJdSdGGshw/RkcxGjFemlJ/dmkvurxxAxZLN8UkHslxM5Je9g6YgrjacErqAlaBCVhJPg6AiVrk8shcXo1QmWOARqmJNawXOxWXC5At'
        b'yg0zTdGzdCvR0zB0qXGN1LP10LjF//OxmUON8Us3RFsIHKZ7iMeDUa6CtEpqaJTqPa26tzNDO0NyuTvrexF9AmqBFZsTP2D201c1y4NMfQVP1sK9bRUEGawRBUCc4saf'
        b'pecilpwFmT4zeFGr5LQ7UxwomrSQGdp0dau6Bd32VGvrlmkPjdDjPyc2iXZ1d5ylOv6z6Ffa3aOCDtSBloDZjAo7UO1woSQnB1mwFDFoDlobzCR/tMHWkMLYUwp3gkcx'
        b'NtgmmPMuPJDpyZimRqSyS6eV9UB4URpjGoeCaJ0yoINrZAGNQYMrtCkkNEloyUtpkyz4zSylbwtGuNpTCZeuwIpG5ywb5juVCAk9FDQkDWkZ896ELifbape4Iw6f2+9q'
        b'U1rljnqg6h34tWve9Dk15dVVkQR8R/5JAUEluFx6tGSXi2lMuzAmh0GhxQ7NfmQMse7C2CRPJTVSWPaJWO2ZTOLZBKi6vtGplBpoRU5LrZfcN6KLEsQC7bHpzLwenE4y'
        b'Yq+i7R8dRQhCVyo1o8frqmhjUJ4VdS0SihszXGrovjogMJFNk6BcFQKOFO9QsRo4ShG4UNjWVzE1bLrvFoFWF/txqPJLT2Gj32FmigpEYfLKDSGgE2XTKmF9crcEPK4l'
        b'IBjb1mXcHO4Kxp2gqjYpYH+BC9M+bFjN9Eun5nyBXWV6eZ3A89uJII8Iy+v0aRAxw4bf1uEnaEVMckdLm48ESKTAR8d4EdNyPFzX5XIMkRE86ROhYem52wIry+GTcSZD'
        b'f5hsfc16QHkHBZMnh8kJBH/WsIhtptuzzO1vrK9VMEYnM1HEQag3REpJ8SPSxjNOaCdqC/E0JkiFkyIxwFvUVxLBl+6B7wHKXMQ3Id5vAv7PlMahZiV6Z2Dp/ixtlc3d'
        b'NtnSbWeyge6EDVzn9zDeCaSF+Xm3A2h8RybXnRiwKceMvIFEGE2UPGyTbd2J3mxK2yF9UE6At0b9Vqy/3d+zPQFHAIjNDK6ZU97FsmVHPy6Ta3sPSnIGnOhZQk4MOJst'
        b'eBdwsnrgfnDAAb9OlKPrmAPKlJ0BC5Ypi902aIWTtYK+hPeo9szqxPeomyFbAqZAYsAO27+tCX8TmhxyylozlGdX/JgLRVYBJr1IrTqBtkIncCTmnsAx/yiY/vvffF3z'
        b'5eQykmucEidNmkRDFxFdgDf4uYwz5HMi/MURyyWtHUojoB2+HPVzve7lrk52WZGfyDTW7aRh6mn0un0MHbXUKksavb5IH0zUdvhbCY256gBLNUes+LCh1QukrNLa4ZWZ'
        b'vN+D81Wqd3s8EemKS1t9EWn29LK5EWkB3VdNv2JufhKb43RmLVEBElmGmHz+FUAKJ2ADXEvdjUuWQtGsNXbM4PJAc9z6PfCvUIVJcUMrIuY6JiexeTtaXPQF04SV8B6e'
        b'ujv99PgfxihOYPqNpLw8zaSzEZweGdFBpxHJZNfAIh8yj3d23UsGec0QBpBYzkxfsGUn6csOtZBo0cVVcoZEhXYpheu5vujMZgAdLiMzM0sWwhwa+fhFYpZw97Si7GWV'
        b'7oUiEw0leNkc4NOZPp8kWxCb+U268NMc5YlFEoFaCcnbTmVdXKugEW/OmNaGC3NQPyuHXAr4OlqUL3AuFZ6LhXNxSc7QEYXDepBOUQ0rREpkrOTshh4wbl83U1pqSONQ'
        b'QG8YKmX1yv7g2ahi7CZmrmsgARabPubC3kyUTqDvgVNSwTBfAa2VKmCUf8vpIjc0fpFJozoiQk8jTprZjcCI17d6WhUdh7PCDQbt5Z77cE+vkr+ItvNBaL3HZMie0OcQ'
        b'WcyhaF/HwHqxRMmuRNosioCVwNkpOx+vI3plB69XEycE+MkOi2LigEYoabgpKg5ItlilDGdaXgeaThZrD2ibfOodroS2dpETtK38IH4R6pVFN31SuBKrqqpQ00pkIVbu'
        b'03ard5ElnbZLfY4blBfA12SH6pomcL9tRGLjak+fIcnQkrJGy7420XcLEG1P3PBvlXP/Pr/PkrS7fyFvGXrym+y09vmbcnbUHZ02Lmw+OmVl5JUvJ7z66sI35jS/cd93'
        b'gy786Plvf/bDdT889PU3f6v6+A9tW1Z8evg751+/bEi7ZPaS8PXp4fZJQ3P3z5rdFN788sRRr7bULSw8uuY3Kfu6Vh/faap7oKTPof2zT75mOZp99/Cv/uzcW/1p8jcd'
        b'qy7YMePo1OenDnj5m6O1bw1e96cJ7XPn7zr+2dKVsxo+yHznhZFv298YErjrvTek3CtrtUdWbr74sQ/GfnfzSx81Lnripb0HZ7wdmj2NL6m7v++47756Zu/00pLa1w5X'
        b'/+mCC31PltyRt+7FZ+r2iPLie7vvuXV++6+PZ01964V75GUVj//RvcC+Jn9W+S/n3PrwgLK7n7n+rj3n71r5i28rDh7rmllV/vBlqU+3vXHq4J+veuuBl/74TPP7MzbX'
        b'XrzuXseHI1sLbr3jrc+H5o85mTPikdFD33/ypRWvXPGzusKj9/7m/FXLXlYufnHh+tRj9eHDw56f4npw5dhPf/XCeYmTjwaq5/wx7YO9nhf7/H71nCt+bn/6uOXxSXOT'
        b'zn+k7zc1H7SWFz5e9+bJPzdedyTzzoY/jl2woTTz3aPTv5pTt33xVxOvKR1/0acvLH5zzCvtFZ91PeH+82J50aY3Dg5vHl32If/RofVjlz3z2pp2df8f/sDbi5Nuuu2K'
        b'MTuKbwq2vP3yVffVdMlvf9K5efGnn5cuePT9W9/47eb3O54oW1//ybGS5XOnndj2yszji+9a/cFbex7e9t2ocYvWeT8emLbr9UrPhc3rD6S7N77WcvKCj0f2rX117tWb'
        b'zvtq49E+JxcuHlr8Q8HYy39e80L2/qc+nnc5v33neydve+2am96cdPKiKx84sHjZmx9d0PaVs/6FhLlrNy0Y7l5h+nn2e8cqMxbeNOLJV17667Of5FZ+9/qee/vJn01e'
        b'6z2W8JcfEgKNj7167PivErt++fm2sUfU1//SteDpvR0rZn0z/m+vffly65Dva4/mNXcHP33p75/87uBLzS8M3bD7hyM350l/3XjnNQ9VHPjZVePerRmQsq76u2VVviW2'
        b'w8PH/izpge8t74wf69v2cd+mrz5e/ftHD5/Yvvjb0Ou/+jLy8M+Xb1/jefmLPm//9ouy8c35iVvbT4157Z7ax+75bNPhpx/ts9WZdd49/pF7XlkS7prxyr4Dv5Z/ePKH'
        b'a6qeKN/9oby14LsP/m46cvDu498cz39/3oxhu1aOvkazFW770ycLI3Ov/vKZ+q2Pn7zuu+/WLZefG3P3mOo7v8h98JMLF/zBv/6ZvS35NfuufXfSlk87dm9qf/ZvP8x7'
        b'4G/L7W9ff2fp99b8oXuP3PP7/ATytZiq7rQAq3dYe6CyuFxdM2JmEQZoT1VvFtX9idOYGwTtFjVIPlCrigt47f48zqodENRNiydSaAPTvKt86kH1MAZOPiNs8t5GFv5g'
        b'62TtptP0F88rIf1F9ZB6PbUkUb1NvUtdrd2zEg9EbWjMi3E71SOiS9ta5x+DxTw0bnihuttZVUzGhobiIrKs5UUl6jrm+ImdFwcm2KVybbV/NKKrx/p6orVrt2YXtpdX'
        b'VhRpa/PPPGa+tsLO5Ws3+nE/uUp7RrszdkR9qXaodzUAbaMW8qMrqWs59RafGu4uoXg16ztiHT6jnuXaVpv6lEe71Z+DG2hnZQw6g9XHekpka7tZhLqgtsbh67sihqgt'
        b'2rNAeP2UbeEfbBrj/xML+//lJ38Q27j/1X8MQZOntVbWIwm+CT9crZks5c/9zy46bU7JAX9p9mRrep+0NIHPu1Tgs9IFfmjR0IsG9HeaMqZIgsBn8OM8ecscvNWKqdwU'
        b'gR8M/7NzBD7NDP+tWXaBT5UEPt0cuzpteI+pwQNQ3JrugP9JeJeWnM3bWx1IdAvJpqzBabxjQDJvtzh4h4jvs+HLAbzjSvgdK/A5vKNKeSgq94p3lfK/s7iXnxiZjUC7'
        b'mjPI13s7450pICJu0ta51dXMjV71bDUM6O12db2Fc2aK51kmNLr2TOJ9w2B+vX7P1OKNv/C+MTL55vLyTc+98M1fjob3df36/vs+3vnShuZq0607nuws993ue1D8dtuV'
        b'Awddsyr7VF73jnXHp3BH1o/Z+rsNvx2/Uz6adFPuXGVI47/5N7vvf7Fo5KQPN2ypHbel9IvIje+Y9jWowdstjd23z9vUtjpVXTnfVPDNxt3P/fKyq4U7fhg8d2fJ8WDu'
        b'8WMHRk4dPO8v69/Z9N7a7DGzn9mV+ZjSOLvvK9sKtl79waTvLxtm335TQX7Kof3nv3isZvdjl35wxxd/+zp/17Jxnz+wf8G1xZWlt6ZcG6561P37ZZsv3Brp3v612HB9'
        b'1nPpJza8nvrW8UVbfBc2v3lr12sFnhfePJQ6v2PtfWnjFn70p+0HzG88dCD3jaMLV7e8s/Cu6pMPPrzg8LLbn77jsuUf1FzUPq7uk9zHHu4wPbvsL9l3L/jqxMYF6y1d'
        b'Mzuer5j+/IwZoyetGJJ9IuXyL0sv/3d+8S9+eHrU/QkvXtK0IPt3xz7f3LBp+KsHJu4u3Zd5zwmb29OyunvW21fe8/vI+yueX/qb2755Ld2z4DcH3t9dOnzniGN7P132'
        b'XkX39EOntn444T7nOy9MPHjZW3d88+KKbx+Wft1y5I2O3F88d/gNe/7mT9ceuuP8ce+/nvTw1//e/uLdxyc/VPpCjavsnhMDhFTnou/XT5TfHTIl/cI/XjYlxX1yxw0F'
        b'TQ/uuj534dJdq0q6/lR/3aBle4MpX7VfN8rZfmP9tnfTlmy++pbMD6+4Ouxb9G7q/GfKQnd9c+XYS7U7T0aqv02s/vvJwna1YbiS9AP36vPHf3cwN7+U3KXYeJc+pdag'
        b'A73wBStpRs0RR3Vod/kHQQ7tVm1T2wTtMGYz9nPMk6I+J6q35avPUoyky6cRKcLCFybM4SSMXljtZQ5Xtoyy+cRC9bEiM2yP1/NXazcWscAZ+7QN2qHCiuICdCikrcdo'
        b'Zte60LX0ags3qMaUqt2tPsQ8VG8ua4r3T63uV0PxgeoLtZ0suMLuvAkVkE9bk08R7a9Xnyo0c0njxeY69U4/U+3S7tYe1VaPmKmtFRep2zhpJq/uy7mYdvJp2iNa0OOt'
        b'0NblCZzg5UvV59Uj7LNnu9U9heiW/FEM+GbizFMEp7Z5GnVe3ecciXRYfX5hXjHPmTuFUeoN2lPkjGrSFF8F+Ry8Sb0uHwOeW9UjghpU16gb/ag7OM2thpyJ2upKIGyE'
        b'AD+5oZScIVYM1m5T93vVR7Rb8IW6j5+7QrudXokzFlcUqYe12+PcMLlW+JH9m9+SO117kNzVwUfdfNmMRvokQ92KDhVHa6urS3go7RZ+hvpkNYWxW6RtLIVaQkB0FczU'
        b'NmnbtFXQfXQOiGTUsPNN0+qdFOlK22PXNiQApVlRbF+gbsgD4vNxjDiZpT4vQeE3aetoBBabl5IrK6BK0YlVRZWJ67dUytNuHA2UJgH52vHaEW2nugnGYBY2ZjNfVsy8'
        b'BambmtR7ZaFQC43AQHkP8vPz1OfozYz+2hF1n0lbDaQY0FjX8lPq4A2eDvYdqR2sQIw4WnuwehaMu5lLUK8XgA3eNoIyTJ6rrlnEqaurq4vLYQDRG1jqRaL6iAqMMtG3'
        b'2kH1iakVLPpndRWM1DYtDKU4rxGnqXefTzO49Er0Uj/CzPE1QEDfre0qVbewEIEH1ZvVG3UvY0u02zgJY3pqR5bRpOlbrsJgqA+Rh4ix+ZxUx6uH29RbmbvLG9R1AMtp'
        b'2kP5s6BN5hohvUk9RDC8Vr1HvQOn8eXqXdqacpw1CepmAUZ2I/Q6B3L4tRu054ZpO2FAY3qaErAHq0TtugHaGuqYpK3S7q4oLyovprWwSXu8Er3B3SJWoaM6guv52tNO'
        b'zGHqp93KSRKv3lOvHiDO4PwU7Wb1eu0J1rdKgHt+OVSg3SaqB7Xbiwi02mFJvb6wXN2Tlz9ilnakEGZqkrZLVK/T9l9AxS81jagonFkuaofUDZyUxas7tRuziHfJhVK2'
        b'aatx4a8Xa9THOekyXj2kbQDg4ETOUp/Sni2cZeL4Ck59skTbPGcW1Thf3atuh/ldpD57LXyKLhkBNgFB22ZpIpCjTzh0d4kxEbWHvZyUzMPkXDeUQD4hs6JiVpF6u/pI'
        b'1dgxPGfRNgpm3xUE8gnqKvVGAPsTFWc4WVztpKoBlzyorpniqDjdxyHwZWwe7UKdjQpyw4su0uaOxNXpVHeIl4zVHiCgwsQ/ZGPeJG+6KupQknm+VO9KZ/h2r3q4qKWs'
        b'sFe3k+p16n7iuPppD2nbEa8Uw2IpgDGCBbsRsMhsgsqaimL1YQm9tXGV6iMW7XrAWluokTPU6wYkIC/Zhh9X4NRK07aJyTDR7k+/iLDyZa0pCdq6EcWzqjrorFE7gGeP'
        b'W7TtszH32CvN5ZdAdyh4+X3qc53EgKob1UdKZlYCcknQ7sV4ADuuZDPkPm0XoMaiKlG9hfYOXJ37BG2fun08occ+2k3zRi8p1NbN1tZXFOUXw5D3yRYB9x2soYleY9Me'
        b'r8CVC+AIlxfNGgG1mNV7+3JFnEnbkmGlTMPHqpv0XWxtdT7wa+pa3KHSh0kXlYjauhkE+0oAxxb02VutbVafrsaNqsICrXkS1pUEy5nY4Q02dS9MEWjOMm3dZAnaBIyl'
        b'hcvU9kkLxg0jCE7XVmdqh2qgUdpeKKwao6ekaLAX7lSfhrWD+8GlI9oJurCNqXct56RiXt1TqT1DO5m2R33Gjo0dQdveiHq28WF7+w+V1FVN6n20dKq1xy6vKL9Yfbay'
        b'oNLCmSXBOkdbTzCdPmop+XPVHlYfwc4WA0y13TCD2tTt56qRpDOV//PM0b/cT/Q0lxi1HfDDJQiClT/9zw6sENNDQUdsEo95nOyNfkahM21MT0+w63fwnYDReazkGD+t'
        b'R5kOKo/ywBsHGd1a6SDRIZjFzmu5M/+GmHkmo2ZKBqhy4XP7O9pcrhjfZQj6H+bj+4c3jNP4Ot4jJb2LKhUkcuh6kR3r+47Cbx0n803wF54Xmoc6XuHhcBXgKsBVhGs6'
        b'XCW4Xh6a18jB1R6ah5Zo4YGYvwlz8kE+OM/QSuvmUCPNI7ZI4aQWUzffYu4WWizdeGxnkW0ea4utW6J7u8fektBtovsEj6MlsdtM9w6PsyWp24KHgv5kKL0vXFPg2geu'
        b'qXDNhmsfuKJprBmugwJcKAmuSQFyNxNOCKCrbT6cDPnS4JoK175wdcI1Ha7DUE0arpaAFB4sW8L9ZDGcISeGM2VnuL+cFB4gJ4fPk1O6rXJqt03uE84KiDIXykRV7PAQ'
        b'OS2cL/cNl8jp4Wq5X7hSzghfKmeGZ8hZ4XK5f7hAHhAuks8LF8rZ4Tx5YLhMzgmPlgeFJ8iDw6XykPBkeWj4AnlY+Hw5NzxWHh6eJOeFp8j54XFyQXiiXBgeLxeFL5KL'
        b'wxfKJeEx8ojwKHlkuEIeFR4hjw7PkseEa+TzwzPlseHp8rjwVHl8uFi+IHyZfGF4jjwhXBWyr+LCQ+WLwhf7+8FdijwxPFueFL5ELg3PlSeHR8p8eFrAAm9yQkLAGrA1'
        b'IJTSgs5gv+DAYGWDJE+Rp8L42QP2sIPUSGLuR53BpGBaMB1yZgQzg1nB/sFs+GZQcHiwJDgiODI4NTg9WBacGZwVrAjWBOcGL4f5MEi+OFqeNeQMWUP5q4SwLcgiarNy'
        b'HVRycjAlmBrsq5d+HpQ9ODgsmBvMDxYEi4Kjg2OC5wfHBscFxwcvCF4YnBC8KDgxOClYGpwcnBK8ODgNai4Pzg5WQ50l8iXROk1Qp4nqNEN9rCYsPzdYCF/MCJY3JMjT'
        b'orkTgyK5b0+EfKnBPnprcoJDoSXDoSWXQA1VwUsb+sjTjW+6E0LOQALVkEvfJkAtiQTPDIDQAPh6CH2fB98XBouDo6C9ZVTOZcE5DZlyWbR2EdoqUknSNXYcx25HaFjI'
        b'ESoIOQKOUPkqYRUe/eOTInpSxJ5c4wgkkFrFDOYnnlTtmbUzYojedcRwf2VGOyGu2aZk+dEFBdfEG5rVul+ZU32H+fLycxqZumZtTl1Ho8ff6M0XlMVkBBa37ZzNXZKr'
        b'wUsyMlQEW2OKOpTAQ13lUcNAJF8CFLfE7W9Q0CTB6u6sJ2UWsnnGo+rWhojDUOYhJR4enWG0AE6EOzs6TW5pU9w+H6RET+sStIxFPS+KEHACO32CtDGwXSc68Qejup0g'
        b'4wFUVW6V3YBZyR8BKnhHxLbWtogdSpfdDbVoNGBtcLHzUOaFJuavIIqNI+YGKieSUN/qqlWWUAhFjP3oal7e6vWsiD6ywyMvKyzigHufv1b36miFVIOndokvYoE7KsxG'
        b'N16f30dvSS2dalhWq8QSqP2KKfqObpz0VPGRIoK3lcrxwBDW1rEPFLd7GTrHxgTqGVDCVO9x1yoRM4XiGBUR6xqXkEo3+kVhYRMidgyzy+6Z8s1+fZD9Sm29G6PxuVyQ'
        b'vc7FBtICd6g4EJFcirsh4nTJjb7aOo/bVV9bv5Qp7MLEkJmzLqTUTgl5+T3CpeEAIu1FoSPQ3myV7u8cHQuhy89uvjOdfBI6yashD1gfOOT2AfOZl6eYbekZxon/yFkQ'
        b'Ts4Po7pfRAfYjUkbbSOeu5qNNh6FNyEL4DgHLKtMbEeAB+wjNKARQ7ZMQVDItEEM5ZDylRSQQvZmq3JDyNFtCgihhGZBmQn3Zm8epTjlqpAjges2hTimrBWyh1LhjRP6'
        b'7uiHsDCHLJA+b5UQMIf6Qo2C99GAoGyEZ9mh9AZ0qbIJla6gnj5Qz2OUOwO+HoClea+D5wNDKZTvz6EUwDiWzhyy/MrotkJeSygN8kqwTwC0V6GJyc8BrhLsHzyVaW62'
        b'buCVkpAZvrR1llDp/SGn4YTFDqXoXwdscGfHOwodY4VybDUcg0OIp3Juhq+TQokJug1aQAwl09vEDHQHC+ygzAUS8F1AAIyb2I9jplHkz9LGXMpHldoIrlDm/TAe9lAW'
        b'1C8gfAKmNDQPyWDwgPeHqc39DIjo5jPGnHH8Px5k/M+LoX+SpBpn9l9xxlcRinYyWpWoVdS8MQtW0slJRQeaItPfcRAtnEH0rJlP57N4SXQKTqB0B+B3oh2ewaqJmVim'
        b'6DsQLZhXBX3BOGGY8/UFkxa/YOCtiAMXkmCXGtljCeHAFcI3Et3h5DcFJN9Jii9uDuFfOgy4iPpxAYtyQ8BCli7WANTGJg4smayJnHdpqH9oSCgXFkJmgwmm8bGADabv'
        b'pd32EGqW2aHchIA91B+W5nGYdkkJXCZuzCLcO/E+4KDFByUFEoBETNKnbwLmYO8C9olc+6b5nNcbGhpKDPWX+dAQ+J8L/weG8hr4UArWFBqISywNiEx4nhXiQ8mhZCTO'
        b'Gi20yE04iWE5pQSs0KNEmPBwDcDSCDkzuG5nKBVIAnzi7MfBskkkUiEBviqiyE6dVALcN0Cv1/HdJu9JeGIOFUCZSYGkUAa9B8QA7U0K5VAqR08NpdRQPTWMUsP0VDal'
        b'svVUltFOSvWnVH89NYRSQ/RULqVy9dQASg3QU4MpNVhPnUep8/TUIEoN0lMDo3DDVCalMjHVkASbRDES+AFuHaJPRALQ19DwUCL0ODmQvEHwPRyQ6NeCvzRf+uF8gTIA'
        b'9g3oTVrvTT8ObfAAnn1wnkGpIvkIkBDyiMTpeWFAwucByfAGEvMWnfJfsm7zS/4FcMd/P37Kh93Wd0MMP6FuoGDVfSWbRSeLryUJPPszUywTNPxNg5xpZiO+LvpYTpbQ'
        b'HBgdQDmEVNEOWMvJn+0vVXCIyXyqiFF4s0SHiDx9FKcZRlOE05jnQ8BawC6HrDpOM4e4OJwmhky0mQOxErIBoQ+4jGla99h8eqVP/hP81BMY7zQbRvIMjCICokeHbEaH'
        b'HsQOSbAokOoQAA2nsk6sIsVKJReVvkPJ6OaRnksBygndSwxhcApcSEmAlBIRTWMK1cdD9vW5PJaaEErFRYeAIoQlmgClhmzjgfibGKc4DsgN0CQgc1x6eJ8MX5AiNAaU'
        b'oW+5Hg6Negden//euXq/Oc7WSRLQYEiy2PkBIprKsFlkj80iezzQUQUYSEcUasA8iQJd0oGeR0DvC4SX6CuiN5hOxzS5UZ8GM8uB9rL0zr4+i8CGduSWDNLex1QPAAPR'
        b'FrLAvgUkKewXDQHRd4tBTvNYugTkIeyfnWUBkxLBOIGILWFnMsEuAkPYbVlhR7ECGbulSZyfa7Yrv2IeU1i8Q/omA8vAvZAYbScw/X2CacF+DRY9qok1VhOQjbBKoC1Z'
        b'oUR8ZnzPdjagGWywoqitnRMDJrjK0RpsKNigb+fBt/AM3tii30bbAWRowfy4MM2nG7tEHbJGI+sh3wFdBiBTjAD0sICBWNB1YWsR0p5kJH9jzF2SGBH8dcoR5BSP8T/Z'
        b'nUXE2ehztdY1uJYrqO6sfG6OWqJIpBFtZ9wIsODIjv9TcSAy/5WQ+8/NunmRsWCS4ddBaB7VwFMBjZsliazuUW8GzQaRJTPbnGKGBZ+mWpy6qDaVz89g8gXSy0UjkYjo'
        b'W+FT9uCzx/Dncfx5ghwI1KMPF5+ylxTvuzyNdcqTdNtS61+q7CNjZbhx16K/fmU/mZM0yko2FQq8d0SsrQOufWmtD02aIxbdCVHE4jNulnha64Djz0/8zwFZ/vx/AZn6'
        b'//78M4cQOCe7kcmK4DwXBOn0AwinKYOODPB44MwDCvYn9fLn6PXpP/9n1v9H02aHmGqRxNljYQWKDU34m+OQxJED8G7iJbguBauZ2ENBoH5WoaHKLo489rvi5Xcul74i'
        b'W2rbYFn6FYySS0avZLrPzj4epXU3vbPe3YYOehU8m8STkPraDp/b5YqkuVy+jjaS+6GQDE1B4GmCK5ZQXu3pgSHOQnRiS6vc4XGX0hEICpckAShCAQih3s5jAvrTwQI5'
        b'UDVU9/4DUjzjXQ=='
    ))))
