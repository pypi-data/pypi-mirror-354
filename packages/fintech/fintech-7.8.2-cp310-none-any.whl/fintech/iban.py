
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
IBAN module of the Python Fintech package.

This module defines functions to check and create IBANs.
"""

__all__ = ['check_iban', 'create_iban', 'check_bic', 'get_bic', 'parse_iban', 'get_bankname']

def check_iban(iban, bic=None, country=None, sepa=False):
    """
    Checks an IBAN for validity.

    If the *kontocheck* package is available, for German IBANs the
    bank code and the checksum of the account number are checked as
    well.

    :param iban: The IBAN to be checked.
    :param bic: If given, IBAN and BIC are checked in the
        context of each other.
    :param country: If given, the IBAN is checked in the
        context of this country. Must be an ISO-3166 ALPHA 2
        code.
    :param sepa: If *sepa* evaluates to ``True``, the IBAN is
        checked to be valid in the Single Euro Payments Area.
    :returns: ``True`` on validity, ``False`` otherwise.
    """
    ...


def create_iban(bankcode, account, bic=False):
    """
    Creates an IBAN from a German bank code and account number.

    The *kontocheck* package is required to perform this function.
    Otherwise a *RuntimeError* is raised.

    :param bankcode: The German bank code.
    :param account: The account number.
    :param bic: Flag if the corresponding BIC should be returned as well.
    :returns: Either the IBAN or a 2-tuple in the form of (IBAN, BIC).
    """
    ...


def check_bic(bic, country=None, scl=False):
    """
    Checks a BIC for validity.

    :param bic: The BIC to be checked.
    :param country: If given, the BIC is checked in the
        context of this country. Must be an ISO-3166 ALPHA 2
        code.
    :param scl: If set to ``True``, the BIC is checked for occurrence
        in the SEPA Clearing Directory, published by the German Central
        Bank. If set to a value of *SCT*, *SDD*, *COR1*, or *B2B*, *SCC*,
        the BIC is also checked to be valid for this payment order type.
        The *kontocheck* package is required for this option.
        Otherwise a *RuntimeError* is raised.
    :returns: ``True`` on validity, ``False`` otherwise.
    """
    ...


def get_bic(iban):
    """
    Returns the corresponding BIC for a given German IBAN.

    The *kontocheck* package is required to perform this function.
    Otherwise a *RuntimeError* is raised.
    """
    ...


def parse_iban(iban):
    """
    Splits a given IBAN into its fragments.

    Returns a 4-tuple in the form of
    (COUNTRY, CHECKSUM, BANK_CODE, ACCOUNT_NUMBER)
    """
    ...


def get_bankname(iban_or_bic):
    """
    Returns the bank name of a given German IBAN or European BIC.
    In the latter case the bank name is read from the SEPA Clearing
    Directory published by the German Central Bank.

    The *kontocheck* package is required to perform this function.
    Otherwise a *RuntimeError* is raised.
    """
    ...



from typing import TYPE_CHECKING
if not TYPE_CHECKING:
    import marshal, zlib, base64
    exec(marshal.loads(zlib.decompress(base64.b64decode(
        b'eJzNfAlYVFe27qlTp4qhkEEccC6NGgoZBJyHKCIKMioajUOgmKSUyRpAiTMo8yAgAgoIKoKiIiiOaLJWujudznx7SNPJTXen+3bS6Zvul+EmN+l07tr7VCEg6eS+d7/v'
        b'PvyoKs4+Z521917rX/+/9ynfF4b9KOl3Jf2altFLkrBV2ClsVSQpksR8YauYrDwrJSlbFMbRSVKyKk/IFkzjt4nJ6iRVnuKoItkuWcxTKIQkdazgkKKz+yrFMWxVUJQ2'
        b'PTPJkpaszUzRmlOTtTH7zKmZGdo1hgxzcmKqNkufuFu/M9nX0XFjqsFkOzcpOcWQkWzSplgyEs2GzAyT1pypTUxNTtyt1WckaRONyXpzspZZN/k6Jk4e5P80+p1CvxrW'
        b'hzR6KRAKFAVigbJAKlAVqAvsCuwLHAocCzQFTgWjCpwLXApcC9wKRhe4F4wpGFswrmB8gUfBhIKJBZMKJqdM4f22PzClUMgTDkzNddg/JU/YLOyfmicohINTDk6NHfQ5'
        b'R3DI1ymjEgcPpki/o+jXnTkj8QGNFXSOUWn29PmlDUqBHXM1GSKkrMmC5Un6AxuxEh9iCRZFR6zHQiyL1mFZ2KYYyMdqH7XwZIhErYfNlgA61yUQ6unMcqyYQ6djeWgk'
        b'lj9N15T4rQ/1DsdSLA2LwGKHbWEqIRsqHLY/p+P3jU5QC050W9e9+9MuOE8TLPF0MAvvwXHscRi1PpRMloZtCoUrnljovS4ST8TaY1HoJjI89E6eoRFYHhURvcmTGgr9'
        b'4BbeJFfXh67b5OkTGuatgEuSYIaisQugENsTFcNizNk2LFHfM0cpztZZUBSKNAsizYKCz4LIR15xUIwd9DmHRd6wWXCgX8fHZqFLngXLNHk05mYn+8+d5inwgwuNIp+a'
        b'ubM/1U1aN0o+uD/UQXClY3PV2/QO8dvlgxsXqwR6187N/tHa9duihA4hjd0qeNsE6bPRgjZa+N2Tn4i9/kcWBwlpzA+jsl7RZeeZqlwZH/CO8RNViHz4C8OnLjUuHWuE'
        b'mN8q/rHlww0rhH7B4svioVAZThNCU+rpicV+oT5YDB1QDX0bPWlqKrx9w3zWRSqEDBeH5SFQqfOzjKOL4AaewZMmJziCF2ncsU6AWpWfZSxrKl2Ph01GvKBSUUOJAIXh'
        b'WCm3dMGDpSYj1CXZUUuZAMXYvZqbw24lnjdhrxHusb8qyQje0lvGs4s6oSjYBOUSHqXxwhYBGuE0HpO96N0MZ6htJXZRHmCrAE3Y48PvhV3boNm0B89EMS8q2L16TbxF'
        b'g6fmmvB6HHaqqeWkAJXzsM8yhlrS9+WYLNiF99klJwQogaMLLWxKA0PjTKPwYQa7oFmA+gg4LPt2i7w7YcIebPNlzp0iY/ugUPbtMlw+YILSQ5OYN2cEaMAj2GHxYH9V'
        b'Ua41mzTYBYXM77NkEtrIJnNi9P5cUw7ew3wKYawVoFwFJZbRLIzcx5lcloQI8gV1eNaZ3ydxMuZhzyhowQbmwhUBmqFGzd1Wh23VGLEPjrD+XKZrtjrw43Bs4hoocUoN'
        b'VAgKewGuxsF52a9TcA66TNhNs3+XzWqVABWTaXB44wWyVI49Fizdr5QHuwaL8TC36D1vN/Um2I3d6BrNggmb5Fm4C1V2phxHX1G2VoznoYG3pMBhrDbhLbgWx9yuF+DE'
        b'igT5mjMUgGdMLrOh3jqpDR67eEsElh3AHnu4l8IazgtwOgsq+aDFbqHB7bHHnrHMg4vkwVKlHHJ3tA7YY4ZehUq+S0UqNnCXt0dDH/Y4GaPV8hWNhlh53vKwdwU1QLWG'
        b'DUE7i6nLydxYEtYuprm+jo0xzOdzFPPZWtnn43gYygjcDBPYRVcFaNk3md+GAC6Tjs8ZYx2a1jnPyVecNI2j43gKi9lodglwLtqFt6jwJJyjcZ4tWMPthAJrua0d2Z40'
        b'0+MTFPIFrVCxk4fhMpqJEnKsZzPksbZLNDKYN03uznWnDNYETWPt5PBo0kCj3HQnBYpo2rAh0+p0YxZU8fHE86NSNfYhUM0aegW4oIFS2e0OqPXXYLf2SWbtJnPigjw4'
        b'eAlLcjTZDnBSJd+nfi/ek1uOJVJ09GJDFBu163QbvJbAYwpqAqCemijejrLO9rDg7YCb3Ad4ELCS2lIElXynFqwNkf1+gK2JJjP2ujPvCgWqKvk0XvxWh1OxWmOCU7Mk'
        b'ebjr4Mgk3iJCvlrjiC1h7D53BGjDdqi2sLIejBfxCJQswEq4CaUqqM8SlNiqiIareISfgKWaHCjJxhoog2IVXCK7UqqCkK8Qui2MDEwIMMI1KLaeE2A1JDhAmTheCzd0'
        b'Sj57hyjdC3ZSDSuhCc8UMhfAcYsLHQ9dIkW6hpO/CUIC3twt9/0MXl5Pk3YyXM1qSRJU4RnekEhhQl0/tdvWdTjypGUWNYS4H8Bq8ujyAuhQ6SMpGM9D0XO7guHc1khh'
        b'nkkFJ/HB0/LwHYX7S8lGMRSykS0SoACvhVt0rOlhZrbNylU8iTX84zy4jCclYTKWYWWs5EAdled1+zQ4Z8IbE2mwZMwuxxMrLZ6sS5MoIrkd6IV2ZigUrg7Ygb5deyUl'
        b'9MEtbsYJTvqZnLDO01ZHsAnvcKayHCt22dy5MsidTtmdqnX4UFK7TuFW1oSNJ7AdjScZNDTRAJIHDZRDLAzg/GqsDoVOGpoBKwHML7LiI7oo8XaSPZ8iP7y6w2SMnMaC'
        b'p0CA/Glwg4/LTriItwcGRgUN0MyGGO7v0mixBNqfdhfWae004lQ5CHuxGc+ajDl7bAUQOpwtPhxb0olPPRrgufOt3sA1LGNvl5hPPkbVHonuzCbrabiA3SZjLuYNlMx6'
        b'vMyN7cUHm6lbW+PljpUpE2SXCDwa8PwuKKGJD8Xbarw5C+rlmT+LR/E44fto7GZ+llOJC0y3PEGfM6h/NYMHiSZMibULpA3CJOxRYpfGiY9QOhQ+aXLEnumiPFknt6yz'
        b'LKLjK7EFTg2a8rJBc3ZQy2etPZIZ74xUJ0QKe+CaPdzZjvXygN30XW2isLo0QZIR78whaLZ4U8uuMTSY1Sx4bFOnpFQoIoQ8nrI/l9KsQfDHZhWUQ0mQ3MUThB9Ufnqj'
        b'/G1EArpjeFAG+VPKDo4mOSYvyTFZvQtKlXgfO924S7u3EV1wxqIxrJ8NFJRQCa0WL7k+FK4bKUk65KgswA4HyY7cviMzm3MGuEEUZfFiG3uhtD4iE6+LK1kRZJcH7Ge2'
        b'yoa5xtNl3nMESXhmCwfMZVgL+WSNKnXlAOMpxRJO1okct/vI9rbg6cHBTpbK5DlgFgOwQgVnKbDaeVdj8Ooc0x64DydsTCkA6/iIpcOlHUPT2NpVOXXwyhKDZJ8EvRyZ'
        b'AlakE6vClgU2VhWJNyxzmVv3w9YOQBOenIp3ZDtks1PuMs9nH8JWExGqfO6UlpLmMtlbKNrJdbsGLyfJ0Hg7CFtMltxDNpI2k2KFJ1cXniWSYr0TTSsWuWINRcQ+Fi5w'
        b'XAutlKeR2GcXMNZFpm8l2KIwjYKL0GJjduRcp8WPtdUG4RVr5/sw34aqlF+Yt9VzgTwEJmi2x1JogS5ubxWehevEBuEenLfRwf1YLY/CMYqMHpt3NLNYsnxY8luHoVZl'
        b'CqJR4MHThJ1TyeAW7GDD0EheRcEDuUL3wHm6mSY03sYgPbfJ8XltHT6Q75MUR+FkLQa7goO1WM2hKhqb7HwxbydnlUl2m005cVBlI2iRm7m7cM8N7g7gQRnFWJHN75pH'
        b'ASEJvnBPtSsXLnN39+7ANlMODVKTSo6BMhrQRh5KUDkbblrtXXqssjw5BYuUxHkLVvG+RUcgkepbU6DGRg23rOQFAc5anIeBFNm4wmxMwt5FeFpJEXg9h0eQPZx8goxE'
        b'BSlk+l1D97zDWw4ewKMmF7gCR2z8EtoP8knHviS9PHTYjVcGUrJjeEruUUGdAeQEp9YOHzJ3VxZC51npORdgmUlNdrmTBoMX+2QrO8pZcUq8FolXuEdro/AG0dfdUGsj'
        b'tnjRzAEQqqhOPrSFzbXHc/AcIc1DwpvLIGPpWDyNJ8hWwFobE3alYJrPOle/IvARbj3qGD8iQbdTZNBquDJbgPt424gn7bEST3vLYVibQaf1mLE7zsaioTSFA1Is5VAt'
        b'xfUNqGb6mwViLbbhfT7p07AVrz0qm9b8CdaqhHlUinqhVUV0r45O9pBpfwFjsUS8JTbtF9godGM+z+2suWo+786xPByHQy/H8EA8rYIqJ4pFTi2bSBFUMXNH8b6N4kP+'
        b'dD7PK7DT2XXyI1Cy1V6rQSUNxqhd8xXrVXaLSKvJWnMeFfU7ZG+1wiYLqOv3ZSC/MxUKwil/8+AoT2NrkRlIPU7CNkCZ3fRxxClZiE9fe4hGrfuJbXZyVxugx4+zld0J'
        b'0Pwo73hN5xZKVm8jG4Fwk4pd3BQZCRuxdy32OBs32slk99zUaD7uW6Ayc3iaBMiDNIkSpG2CknEiOMf75YRntQQm5ePwHAu+bkaN70mcU6aRqDkzpNSRpYgsRgomw1FK'
        b'WLgN9+UKngc307Bnz+LZopxtFdik5dTpqZCMQeA/NAmIeBbiKSWJxF4rf8+C+xKZgXbg4pwAr1KM57mkwvOJw/qEp3ULRMZPbrG0z8c83h8ff+zkIq0O82wqLXkmt/7M'
        b'ISaVHaIX2jQaTahMswJI11ykpmfhjk2nxeNNftHUBMq/HgcJqmw6DasTORpN3k019DE0uioPcxec30nDnA0VfK5mYHMQ9RFKXW2ibo4gj9yteT7UMH6sNXuqqFC08JHD'
        b'diyJsuLHJZt9uGEDEOpwjZLyrnieDEM166GB3aF9m0omGtWQ/5xcyvoyZlpRrW3e0MS5Ooh2+mODCprcV8kpXwEPD9Iw3vSzWJOnHprTLP68yjVAtdVeKeQ/igwOSoPs'
        b'bVYx0gQP5VrbjleALVQcxDuiPPxn8VoaL1kRKjhhNdgBZ2yJw6BioGbFRNgtxqooOe6v6RaQoZneNh2MhUm8aI3D5jg+IXBm8kBaXxk+dIHwUEUA1oZHZcc68EoKmaMi'
        b'16OS9ek5POLHRy48d+yjXCRjYqLVL1dy6/YCNyicr8AqNzi90jEKy2fKE3F4hisT3DT3Ni2+EG/xvMTzqST/hisRG5TroNVOibdmEAGZwOw0w4WV3FAePrBJdwrqcssc'
        b'ao1PeG5QWiUQVRnC9KxcwqLKWjFL9qpt0jSS+iK0qWVTZ0j/dsmirx07ofDxQL4sB/KdOK0Su0lIy2t4kxYtZksG3bNsSwZUoYrkeO3I2TMiW7Sqx4dYnyQ5O6MVMR74'
        b'Y6/GPgTr1bK8P++MzbI/lwiyDz+OX52yP1ehDfKUeDV1tcyDWvbAcY393Km2lQqse46bcZ9IF8tB1QhXBvG3QUHlbbdwuhzv0EMQfE5jnuthrT3V2AbFciWpIBi8pKEx'
        b'uCerMLbqgdfWyaLeFQ5rHLE917assHqHHKOnlrposgPHMWsdJJOoWlTwGFi62BbrI2U1FOSGKvGhJ2Ezs0Loji2a7BBoYOYvk9WV8y2BDHooEOpHDk3o2UqhnL8Lz22l'
        b'TMGHxt2ktPB6jLzy1+UXp8k2pdiWaDZBLc/AiXDVNKLwV43WP22VWZ0kGnLH8ZwhzlG0nq3bXEwYWNI5TODDmWMRqaimQULLd/EgyjhI5UK1yozXg2W46cF7q9ga0UVf'
        b'2zoQdm6WV/Bq8P52dq+OBbaFoJR0+aIyuL5G44yNPmzu7wusalB5ZYk760CE7EGQw3CRNhjwWhgBuYJtvIq7mWicqllFIlTl5zzGM66q9sxXxNjbLZjnwGPMBY+FPCYp'
        b'oVOVAD1boJjqdcB4FQnQS668tCuh4cBgAWCbenk5A7p14yTJbjGPknU0YSPNxxU5lYr3Qp9kv5h0JDs52IOozuOoIqfdUmwF0u99WOrP0RsfEjuXTY/HuuE4NHhwqlVw'
        b'ZgLc0dnL03ALj2dqnJfCOVYGH1CWYnWwnMkVznhGg9eXQ401B1ueyrUuMFIxa6MmuPwUu+o2QevaaXLa3tofrXEInS/KM3eRYveMbO1oGORpLHYy96cYPbWPCjG3dt+Y'
        b'pTFhH5wdWNurgzJuzXVaLlv0g8PW9GzCRlEO1LJA4vklBFjtkM8iq4+AJjzWsoDnwoFAaqqGQuvSHkMJnpJQyBcDJeihzD+yEUo2CZt3qLGZrSbqJI7O8yiaz40jIV4S'
        b'sQ5LlYISHyiIr96wLgefgYaMcCyOUAveKeKzCj+4S2phIrtpvgu2h2O5H5bNmR+tYxtYTq7Ksdgs74McmkCU6iyenhPlEyoJ0koFgWFt2ppEtlNk+6Fu8P0mvte0WuBb'
        b'W2xLi21vsW0tZYFDioN1Q0sqlPKEA6pch/0S39BS8U0s6aAqdtDnHMEhVaf83d9oLhy1g36C2WaoSavP4Lug2pRMozZbn2ZIMpj3+Q45ccgfYfIerNfuzAxzJt9P9bLt'
        b'wGoNZC1bb0jTJ6Qle3ODa5ON6dYbmNh1Q0wl6DN2axMzk5L5jiyzyu2ZLOm2nV59YmKmJcOszbCkJyQbtXqj9ZTkJK3eNMRWTnJamq/jkENLsvRGfbrWQLdZot2YKm/2'
        b'sl3ghAErviNdkGBIXMK6udOQnZzhLV/FHFwVFjzEA0PGYz1iP4k0MMl7zawLyfrEVG0mnWQc8Ua8b8Z9g29mtrlJQ/nD72Nm+95Wa77aSIvJzPrIxj022ifQf8ECbVBE'
        b'TGiQNmAEI0nJI/pmSs7Sc8e82CcvbTKFhkVvTubb6PHxG42W5Pj4If4+btvqvzziPLSsfdHGGjJ2piVrQyzGTG2Mfl96cobZpA0yJuuH+WJMNluMGaYlA3fUZmYMBKk3'
        b'HV2jTzPxw2yQcwymYZ15bCvdXhi+iesWtUbeyGmBW26mPfIaWfg8KDbO5duzH+2dIMwVtDEO8fHbEyakCnKdLR/H1iTZltVd4RnhmU14lp/8c7WjMEaIiXZxjU9LT50s'
        b'b/DeW+UsTBbs1U5z4522rl8uyATi7MTNJo28tjML+qAe85br5A0iEqLXEm1tznAO6rV4V66I9wgEO0058tbhk3iTAKohSL7oatYaE9tuoGuwazZB2UW8xluy8eo44r8y'
        b'3MY8QRXxLFzlPizBAnuNUd48fIZL9SOZcjG4DkVEibKUXAl7kwun5qTzS9IWQK9mj6yU1hwgRGzHDt6wC0qxGEqc+JbjgmVU1XrWyfuXY5leM6ll0VJPcF0FPVG8aT4x'
        b'FxN2W3cib/gRa68nksg8cJ9NTK/HIm9E4h0XqLFYtxzhwn5fYqiyjHNJpVpwBy/LM1jqpdXwseklKn4AmtYFyoWlItAFe3g/T7OljStQqcMq3rSUmNtpU44dX8yLJOZZ'
        b'AdexUF7vhIdLTTnyshmxk5NQnBWnU/I1tdAoPGNrMo2G4pQ18hW5NB4D92ndDJU+K3jDuvEm2z2gaQvxzWbrtuasHYtM2CMvJS54jtRUMTToRO5ZMJH2voFGbFwBlXh8'
        b'tFz0ziZguwlKeSES2O5nA9HbfDnWvO0EJyF0j0ob7102eaHA/Q1+VgicS4agWpgE5xMS8bYhs6pZZaL6IPxMHTb/jevrlEGu6t/WN7679FxR4bjpJ8tc4peExwXFSiVb'
        b'RhU6SO+o/rhqAyn0m+MzXrCzpKzuvfNNys5/9J3cMuN9p5n/EfM7D9UnfYcP5Z1ftmmt89hPzabpHS6j5+xqrFv0y67W/YF2HzXjVwG7fhKQfcu+t+mdFSs/u//GUzVL'
        b'X29p/XTxnk8nzM6a2XLf7ZNln3Q+3TP12Jd/mPJpnqXz2rt2f379zxf/rPlizheBn1/4KuabX/TNH39py78uu/5qY+Xb919b+dpHwSfzVqun/nrKfeOXz+Ud6nkuLOZb'
        b'o8sq9w+qv/nauTfmwY7Yf7w53hDRt9D/y2UTf5Px4k+zE99umbftnSear4GT2u/hpfQdrUf/oLMz8zG9BXey5vh4Qj5UhvqIghoaRJ/s7Wa2ue8+A7rn+IZ5e+l8scIb'
        b'iwTBQyv57n92Jp7l7XhqCxaHR/tAUTSnBIvhlma9iOXwcIWZcQkF3CFBUYJFXmPhtI+vgowfFQOXYbN5Nqf6LRuIHssPxuTID8ZMXJ7t44XFfqLgC30qvDFxr1mWjO54'
        b'A0sivUlol4RhOXGFeaIz1k0ysy2eQKI6NeGyAcKFCpm4jMV8JUmJHrw9E8t0Yr/oqWMRKugc+NsPfmHg+dXYZSnGzNzkDG2K/OiVL6utT/U7cqSPY3+w00wJDG0PSTpJ'
        b'Ya9gv84KUTFOoVZI3zqLaoX4raMo0XEn3ubIzhHFfzgq2bmszfYunyEeHsPPZUedFRL/56iYLDopjHY2v3TqfondvF9JpbvfzloI+yVWufrt4uKMloy4uH5NXFxiWrI+'
        b'w5IVF6dT//Pu6iQjf9SGPYhjZHllZA+DGRk147etZd1kaSocmfyRWhSpc+xVUqj/wV4t0zmfJUF5atiEaLOsU3J71BpCExY+pBebn4P7OeHr2E5PFJZHh6kE5yzlolkh'
        b'FvYYGt6GPiwPj4hirPIBVhGzVAiarSJejcOTHBJzsHOHzEZXQS+no7WQn6gcVPpYn+xspW+JMPC4lJQiWZmkslBJTFIiJqnkTFLi7FF5UIod9NnKJN9WDGeS/GG6QVTS'
        b'mJmu1dvI31CaN5TSDaNsG/8JszQm77EYjDKfyEo2ErtMl4mP7Qm/oaU/2sYIyBGvDXRHQ3pyiNGYafTixvTUkjQyYWT+Mndl0ji8EyOyJWun5CuG93CkWzCKuSZNv1Nr'
        b'kIluYqbRmGzKysxIImbEmaYpNdOSlsSYk0yCOOW10tyROVKIgXX5ESUj+q3XBviYLVlEtazEi48aMUZPdoY3u5HuexiT6jHGpIqyLGWfMw8+9uigN94mgV0U4bXOGy5t'
        b'lB8kZAeiI8IiFeyRqSLNYl+8ttHQteZXgmk5WXGt3/BRvG/KHH2oPi0lLeEv8c8+//YLb79QCTcqFx9/+JOO2pba63kdoTeOtxz3L9PVtRyfXnekRyXo3tG0vXNLJ3Lk'
        b'g3MaOKvxosTAIiyNtEDTVCt8ToMeCa9hwzoze47DD44/Ee4bCI3rIr3DoMwGkRPhhpQBF+bpxCEA8F0oyFGgXyM/QPoI9Jxl0EuyV4xWyMBndBkAKFW/vS2q+u2s8SEj'
        b'jBN7YQ94Drm70ujGPruyF4cB5GH2fvUIeUZfGgF5tAwxLjxLItR3oJfz4fyjjgZAvoUNPNbB0emP6eMOPEklsBtK4ay3cgfR4PI9xJfaoM9RSJhGer9qFDZ62Z4VujM+'
        b'XJPtTIxvk4LoKF7GY3BU5qm3sHmXJnuPQtg6ToGFbO/nJp7iq20L4X4AUefjJux1CZAEEasU40hr13Gi4umCp00BNGQ79ygyBbhlNHOatHPNPE12tpoq3FEFHhOwYQK2'
        b'E3jy1d0KKm5tMvhhPnYy9FuC57gWT/TBB1Ypvn36Iylegrdl99uxdPwcQlWFMH2fCOUKolzpj6HmgGBYxVBTyXFTfsBULLBPsR9AT+kHoWcKoec336XDedoPVeHfiR0M'
        b'Z9jp369mv0Nksov/1zVmYhp3y5RsflxVDnOQjUtmYqKFYDIj8XFHbboyJCZIG0xV3shgdDWVi0RzppGUYpYlIc1gSiVDCfv4mVZYDybladSnPWZvFWWr7yDf9GxSLPwJ'
        b'dK/Y4I1e3vS2ejV7C47e4E/v5J7XqoBVvCE42Mv7MYuD+kSaNXNEdcw6ycc5S9bEZDWJIfq+rGEDyH5+UK0csJiZ9XiJZD8/rEwOmbz/UVGuEEYS5S4kytm3B7BwPFSN'
        b'9ID6PysxeCpds3j7Pq6HutM8hL0TdgpCfPyy5UtzZUFeK7kL8zLZU+Px++8njZVFkgN0JDNFLzyD57FNeGaF/DRxyka8DiVQuGouFFJBdFc4xEArt9I431mIcVgkCCTr'
        b'P9nkQADO7axwGs1W8P2hGq7T6028xA9jNwna/ECJCcvCyULAgXRu5G68m6DNCRGErHinMoOFGWHIDx1wcjk3My5I8N8CTdzGhq3R2EM0LiYMaoQYvI4PuA3jXEchzcWP'
        b'amm89/Y50cJGg+ZFD9F0lZn/j7GzyvucYa5T/uuGhjfg+ZdfmmR+f8rdp3+/89bdjQmhl2a4eo+Z+em4D09X3fjkk8bXdzZW/ipiVL44+++hpZdXf50e3bkm91+w2Hld'
        b'auv4qNu1Ew9kv+f+1vbKqoWhs9f8pX3756vfSFj1lH5G3KtdjofcItZ9jZ3GlhOLPqq5fGzLX5//T3ihu2jz528dSzc/rfy7v9HtzuTfvtZzcfuknN29cTdLvG5+HPCr'
        b'2RULRxW/Pu29pwNO5KzV2ZvZkLti/UTofJrU2IAS2+NtZpvE2IlX9YMKPavySrjwqNDfxcNmtrNt3IpHGbSTJPOCY0ya+REf8GFXhdsJ/nhWHTYhwjyVmbyCN5M14Viq'
        b'k835iXgCu4SxUCDZP5Vu5mvZVG/qwqPxgruPQhCzFUF4bK2Z7xwVYRtWhxMpJ3HnF82cPSh6bXTnjWa8AcfgBnYxwTYg1rYtN7NHTudjvks4loWTouwkt2VV6TJXuRNL'
        b'zDqFzAHs/1vaTGYlDrISoxLBOclcmZMckvkIexVJRDkpZBHG5BSTWTPo3cP6S6zF/RFreSSC+pUE1oPIyvfpJ+Ug/TRmgMAw0x8/IjATq79LOpXvwytW5YTtu6BcFtZu'
        b'WKCEUuzDezoFr/Cb4SKN72mHoav07Oncx74sMqB+2NYAVXExRRz4UojiB30pZKdO+dVrQ4BsgwyE30HgUzj/5iV38DL4/7bi+U4kto3UUCRWR1lWsBw4Tsy+6fuROBga'
        b'h/N9rIISeaO1FVrgFF9ihfPwUP7Sxj24yTe8nzU6hEf7YHHkOvbYQSwWRoijQwgGj8EFqKcPOiHG1Q56sQh6DLPO/0gwMQlS91rNR/Heg8TDludvV7ZUK0IDL8z1SfIe'
        b'56uP0qt/Ntc34Ez8h/FbXvJ45fl6tRCz3+kvZ7/Sqcws0iZDTdAwQIGSOQOAsi6Urw6NwctuBEd4FM4PQBJ0JvBUXkLIfoYvD7nDxcErRM8u9eQIczARmmWAGQXFVoyR'
        b'8QUP41m+sJODNfaDFpA06+FCrIjlwRY5D8URc91uZ7J5INNdeaZTrk+3ty6qOCqM42wXdCjlRYwRxUaHQm7kGcou8aDcMXnwDBWOOH8wQo7yp+bbaKKqZK+34zmr4+S1'
        b'E3R/T/aJBcL/VfZdGhK8sVlpBrNpIMXkXQjKIy07mmLU7+S7CsPSzZayeu28EYXxkJM9g6M3RW3c8Iy3Njg0JDg8dlMkKeagqPC44OjVId7aoGDeHhe1KXJVyAbdP5fR'
        b'I2UWr97hbvK3x95I3Ou0eFauwB+3xgbDNvYlujnsO3hFEetDZRnDRAxW6aDDEer3OW7FCqgPg6J9AjSqHaFwNRTyx7rgEtTl8qtFPGc1QPnEEXIqtkvQuhEKDV+031WZ'
        b'oun0T2OSxv50+ujD2jEhb+ZMfyZ95rg/jrNPsUQ0t77/Ss74rtjrTe/Ps/QtCjn25C++nLmpfvuTv9kfA68ecwnb9cKHG0uXVxR96+GT7dPwS5fjLW75AV/qJJ4yVIGP'
        b'2Sr4FOhjGUNBcsKs5Q4SJtyxFV08Ezs4J+7hKbP8NbOtCx+Vzqf3UfE8sIBni8+G+HAq53gKy/x8PNWCg4dIwFIHd4dI6JGTxpGUh2mQah9jzRt7f7bEaM+XGNm7ceLA'
        b'deOHW/MYyBZ2kueQbHn7uyQ5YSfcmBPq7RVlW3hY5a8UxsE9aSwRuWNU0GYIjPpcgW65mpE0r/CD4ujNWMBza+IhKRV7Ld+dWtZlPf4dyIFlvR+aXmxZb8fwZb3B9Y2v'
        b'f2Xo07kEGqGsMQHEtvOykukAlb+hhSZMTrI0vdlMeiZRTzVqqFFe7fRJ8srhY0puiK0BVfd9ok4Wcf+/llvFiKBgL5dbyMNT+wZV23tU+X6Q9tEsJvYjy4KXxnqM/rUY'
        b'z6TP5NL1odZtx/oZC017xuIl23cB1mMBfwKXWGjrIbkCW8tvOD4csQJfgEZuPyjWTp0nUuRr4yPic50FQ3HXZpVpE7X8eMG0oWX5z/GpKRH6l1O8R/8lfvvzb7/QVelf'
        b'15KnV/zLquNRrq+egfuV17dczZ91TNXZNKGzaVNVS21DpKK96aa6sylQKVR/PHbSA6NOzQu2jjJmWMG2VusQJgCaXM38IfnjeARue0OLVQTwKsXX17GcYCdSJSyMUh/E'
        b'Wmg0s4q3Ervgppf7YMUBR+x5ecdbhLIPBm//jI6Xy3uwOy/v0IZX8fZgBWFaZMUyOKPiaiSS5u9O+OM+TIMqgsJSCRufgSIb7f++hUcnXvYpslnecAwbZ6v9IfbE7an2'
        b'i6z+s0/GybZrdcp+DQO9uEwj4wyDmMCI9yNnpgygHGc5g1Fu9I9HQDmuzy55w+EROpqBp6mv1M+lUKlTRkWt0SnW6MSoNQbHNn+VaQ052LNUsektu1j3IA/1b9/tCw+1'
        b'3yFdT8hsb397/frrOeuvH/58/mFPxxeP57TOzM1JHfPq2+vd52V/e+6v6QGlr726zBT3bl/E8Tzl5xknJhWGv5Rx7uFrhwouuZWOmnLqTwl1B1/zsVv6zf6I0i9Uc1SO'
        b'l1SrIg+WH3h3TdyBiBmTTwV3b/os/8Lfpt2a0RbjcerggoUfqZZIMxLfClyfn1Bz1vzzrpBTKye8HDt6bN3KOf4nnm5piFo1qrFUZ/Zqe/PDuqDd/tWvQdoSO9OHy165'
        b'qOmq9IWErQWzzLraN3O9o8Oaelb9dVuR+q7j5Q8ndl746O9LfpmoTH9xzV2H0wb33jeu3L076lXz0uw3Gt8OyUl0effy11/oVyw/nKer/zx6ST6WVpw9NvVH/rmTr3wm'
        b'Rb0VuyjyN29Evf7B6eZfvPdc1ObX3xf72jOV21vXm9+IMr/5sw/aNmfNP7TB5ap/rPig/Nn+goMTcVSu+60P0t9pUd4O9/km46M/L+/b4/rFh0qnNxeN/mz61PVrv82+'
        b'+qDvT6+nzNo1t/Qne4/ObPr9hDV/2z+v5mSTcVP/S4Upbz77m7Y0w5zwP7xvn4gLfE4u8MGAwJeffqL7lsLPe9OstD/WtilrXw7d/Ez3+q4Nf6q9Pf1WxAr9+arZBxer'
        b'ys017nuKpwROfDH8/rr8b76tnuLx11HvW956PjN7Tatj5t8WvOf22Rfv71iT+/vmf/3C40d2+198MiPc9HHFE4ueecm9+EzAvwV4/OzV5wIWHns9rP69b1S/Xh36V98v'
        b'r7Vt+bo4807Dzj/sfs9kemf36si/P//639PsW0Pyl34rHj3vttB8hTCCr7Vc9dJREXV3VAiKRQKWj3fjqQxlQfMH5ymWelkTdYsT30dIYMn+OLjYQ5+sBnKxi3MbuOY3'
        b'D0uImZT5qL2gVlA/Kz4RiUf4ZrAYFjVnnQ8WhmE71EREqQQNXBexkbC5mLcfUuSGM1inU9KJ/5eGsTOuiXjJ1e2/uSWrc/7v7eB+px2VkdWhEV844tjHxaVl6pPi4jja'
        b'ZBESiE+I4jyFlq0qfKsWiTmJ9krRUVQQKHwj2rHtW7alKynFbyRJ/LukEr+W1OJXkp34n5K9+KXkIH4hOYr/IWnEzyUn8TNplPip5Cx+IrmI/0dyFf8muUl/lUaLH0vu'
        b'4r9LY8S/SGPFj6Rx4p+l8eKHkof4gTRB/JM0Ufw3aZL4R2my+Adpivi+NFX8vTRN/J2kFX8rTRffk2ao/1V6QnxXmim+I80SfyPNFvulJ8VfS57i25JO/JXkJf5SmiP+'
        b'QvIWfy75iP8i+YpvSX7im9Jc8Q3JX3xdChBfkwLVr0rzxFek+eLPpAXiy9JC8afSIvElabH4E2mJ+GNpqfgjaZn4orRcROkpEaQV4gvSSvF5KUh8KK0SH0jBYp+0Wrov'
        b'hrCRefTP/oZrlKvCVcF2ikSls2KyQlzhpBijcHQXRQ/2lydvceavrvaKiQrj1EE4LsbFDYLvUf/v868wThvAenYjlgqcGM9+bwScZ2eEbIUHUAKdWAMVWMH4BxRBhZ3g'
        b'PEE5ZbSv4d9HPRRN9XResjjWpyTSEeaOyf/TBUP/V3mq8cUfOCw7vjZruu+xgozzkzStN5bqG7bNWzjfrf7VV77w9ypemmv2uDA/KPfDpFd+/mKG1ND5+Zo9P33v41tn'
        b'Trk39Lf6PPtcUDFc3NzxjOsLE179qijox14vbv59etPeme43v10wSr1x7+TW0x++7vZK6oe3z3b9W9WciRm3//jxks0Xf3TxM4+s1ZavxQurPT9+2UM3im8IwmGo3sf/'
        b'p5Ro6kYpFGNXuB3lY7dI2Xs61sxq4MwkLGW86Do7KxpKVhFDcMP7SvYfMkzlcgY7nlnC/i8JOMJGg1U8KOOjMVo5leRMr9n6/YhyVXgY/7qPV6SdoJZEe6xZwBcYocQT'
        b'KuesUwmKPVQxBaxbDg/N7JHlseHKARKIp+FmtO1hAr9wwqZyKrEVSmEtXLeDiilwRtZWD+Gq1/B1GrUwXpW6WvLajBc4iYI6+1DsgdsM5giI/Lz2WKFuokWC41A7kSsw'
        b'7Zg4piLDNxKY2gmSjwKuGALMTKY44n1oCIc7c/nK6iBfJsFpiQhRfhYHXF+sDcUS8yYdnSWHiUJwWa/cxL4QxIkRXtkK17BEbvdm3eJqVSFo8aYKz44X4CT2cVPbd4hz'
        b'or1J9JFDWPcsmyV8IBJe18HDIbJvyv8MKP4PvuiU34WqhgyD2Yqq7Dlv+1GO8oMuSpHenfgDL+I/7CVH63rOTCVneX5G7QAaTOtXpiVn9Etsh6hfxRc0+iXSROZ+KcmQ'
        b'SK+kxzL6lSazsV+VsM+cbOqXEjIz0/qVhgxzvyqFYJ3ejPqMnXS1ISPLYu5XJqYa+5WZxqR+dYohjdRavzJdn9WvzDVk9av0pkSDoV+ZmryXTiHzjgaTIcNk1mckJver'
        b'uRpL5NvbyVlmU79bembS4oVx8op0kmGnwdyvMaUaUsxxyUwl9Y8iVZWqN2QkJ8Ul703sd4iLM5HezIqL61dbMiwknh6hnNzZKUa2JWRk6yNGtjdiZI/oG9nIGVmyGPnC'
        b'P1vyNrIFReM89sKkjZEpAiNbeTKy4Dcypmpkz8obF7MX9t1JI3sSy8i+WWBcyF7YVzONTFAb2RfBjAwRjSzwjWzV0ci2z40BA5jJpsPRhpmrv3wcM/kZX9nbHprqd42L'
        b's362FtavJqYM/b+stBmZZi1rS06K0tmzZ5iSMhNpZOiDPi2NCoDWGkJMBNBxR5oEo9mUYzCn9qvTMhP1aaZ+p8Ga1LjCNoyDXuQ4XCb/h1lPMUFqYvRJEiS1PY+1MeEi'
        b'VxL/Be83f1c='
    ))))
