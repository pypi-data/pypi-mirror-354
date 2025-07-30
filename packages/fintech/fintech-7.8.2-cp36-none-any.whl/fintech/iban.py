
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
        b'eJzNfAlYVFeW/6sdKATccNdyp1gV1KhRo6KGHfe4RKGAAkqxwHpVuMQtgBY7Cm4sgriBLCrgLurknHTS6U4yPZnehpnu6XRPd2fsJN2dnsnky/Qy5977QFDSyfz/830z'
        b'+NWrqnfvPffcc8/yO+e+8hdSvz81vZbSS15ElzRpi5QhbVGlqdLUBdIWtVWzQ5umyVdlT0nTWnX50k69HLpVbdWn6fJVeSqrwarOV6mkNP06yTPdbPgy3St6+bIE067s'
        b'NFeW1ZSdbnJmWk2r9zkzs+2mVTa705qaacqxpO60ZFhDvbzWZ9rk3r5p1nSb3Sqb0l32VKct2y6bnNmm1Exr6k6TxZ5mSnVYLU6riVGXQ71Sxyu8T6LXBHoZGf9pdHFL'
        b'bpVb7da4tW6dW+82uD3cnm4vt9Ht7R7i9nH7uv3cQ93D3MPdI9wj3f7uUe7R7jHuse5x7vHpE/iaPQ5OKJTypYMT9+sPTMiX1kkHJuZLKunQhEMTN5F0+Do1Can9hTeS'
        b'XsMZA1ouwHWS2Sshy4M+n0zSSOzekcPpcY4gb8k1jb7AmU3ZWIJFiXFrsBDLEs1YFr1hdYhemrkSO4xafIyXJrsiqOO8/SOoXzlWBFFnLI+Kx/KNNKIkbE1UcCyWYml0'
        b'HBZH66RcqFgBRZ6vzsXbfNY9iw2StyT5HUmUg0eM3CW5ktmsZ6EG72CX55A1UViyBu7T8A1R0B6AhcEx8XhinQcWRW0g8gPnC4iKw/KEuMQNAdRQGEasromK2RAQEhUd'
        b'rIIWreSEopHz8B6eTVUpAtHQy6dXIKu+ZkfSfRSZqwrVJHM1yVzFZa7mMlcdUisyz+gvc096rXtO5tVC5sPS9Gz1Hh9PT457OXOSxG9+OJdvxN72IcnBcbE6cXPCKE/J'
        b'j+QUtCM57tHUbeLmHGql9+Thq5KD66W1UpYX3UzfOXraLa+PphOhmZ+pb8/e7RetymJczBxaHXtMSvaVliaH/5OjwHe5xG+fXP8H1XfHB0xSr/6Z6s+jfz7iidQjucLY'
        b'LlzF8ytoU2kPAwKweBIcC4sKwWK4uj6ANqEiODQ6JCZeJdl9PRfDRTzhGkZjFm+HG7K3KtxfkvCsBKenr3ExhcMLUIE3ZYdu1Uz6UiJBoQ9UuUZwBZueIDsMO+ECNZRJ'
        b'UAztB3gDdu0Pl/G2BNcj6ctxCUpjhriIrJQCV6BIhnItdlqopVGCc1PxgSB2JXMvtagnYDObU4L64QvE/HVr8a68W/dKCn2uoFlId7pFS3UE5snYoXdE05dTEhyHBw5O'
        b'TAeXvGWXDq5spIYTEpQE4D3BWdkib3mIfgmU0+cGCarRne4axRquDQW3jF3al7GOvp1hxIrgMR/0Chw5IEOpNBLyGDsS1Lwyw8V0IgyvpclGtWUl3T5PxOKhgd/Pmpwk'
        b'79FgdQjdPy1B+RjM4xL2iAiVfSW8u1H0Pzvcj6/DDqd2Y9cQrY6WJ2G7BA3YtITPvEiNZUaHzjiO7rcy0zqLjwW7+ViL7VDirYJyOC2pPCS4poZ8IcmKiXBTxk7VglDq'
        b'WEnfY/34IKiHU1CFXS4NXhgihHwSq5Jco7nC0C4XGfEGiS6L2q5Tb/IQrZxvlXqVvEc9HSoEveLoVM43GfrFkTLeod1cx3ZDghNhExUFgLZw2VeN12aIeWosO8SWXcF6'
        b'E3Z5qOEuBQG8JEHt/ClcNUKhZQM16NKhiRqaGLOX8BGnlmrZil1OHdx/RcxS8QKe5HLeOzQXu7z16+PEiHMTiV8+y8nti6lBNZOsjtSJSJUqW5loXYtd2KHFm2wPLpKW'
        b'Z4SJ9d/HhijyWiqsADdTBwka4QYcE/S68LaRGnXSaCGaC3jDKvahCE/hBWrS4GP6jjckuDgJG1xjGMk75K+Ok7j1cBwLhL6dwBps4hNi0WY8QbuuwntQJEZewIfQwhc2'
        b'LIN4wS7V6KnU0kJCSt7EB63D69DCWgxwWyN0pR7PgDCHdePxFG2gahqWiwWcw2M+fNXz8Ooko4cKrjCZk1leHo8PBfuPsNTfiJ0GbCUzkfAWY6I7m2+6NjLXmKvDk0Yx'
        b'T3XiEiGoJitcMeJtLTxEZvcdbJ5qLOKbuBzLtlObHksY412kyeRd8oQMK3PWUpMOb8F9MVOjXxAfhJ14A5plp+oFuEvfCiU4hp3jOeNzwQ0lRln78moh97NRUM0FBAUv'
        b'phq99LsZc/fId+CpKS4WqqEFLsMDKJmHx+EWlOokUnUVFEiJUKnnHcZAK9yHklw8CWVQrJO0mSp4lACvYzMec5nYEuAM7bvoEK5QGUOG6Qll6lGh0GDWcAYmRoRiiYZ2'
        b'8JwkZUvZ2ADn+H10Q91LsVo4RgJIkVLwAZa5SAulnfuhLlbvkcViSBoWLOIROmAt3sIqLITWeXBVZ4mHMry0IxIubon32S7NkXVwauY4VwCjWvNCruiIzXB+HlwjrTvJ'
        b'x82hW6e00ngs03quHys6FwU6RefN+ABuQzPrHAXX+vrCQ60mGttdZhZBXybxC8rtWDgP2vtRbhOUK7X6/XjWNYM7vFa8hFVR0Oazglju6xvOJqG+IRq8G7WZE8abtI1F'
        b'vau7xlcH3TuMJiyB5o3DpRiTYQRcMtpWuWaxfbsOj2ju3t59hOE6lrG3FkY+xKGDI/BwNzz0coUwLBlH1sSYYayUaVL4DAfDdpDO1ZAgoWRLvBSFd/V4axe5RibwJcuX'
        b'9g1QhKJdK40jd3UaL2pIDa+TYSxkgR7LlgpuuACJBzyG9waKpzmeEWqL16fES7vhugfcIzs/wjkzLAXa2KgYrKIZeuWkgUrmLuBYOilVjTQbG3TkvG+vEeIqxerFykZU'
        b'OJWJxKa1iE2r0mA3dMXx3uDGGqV3ABYN1IerYtfcWgOec7hCWRSB85OfipbLs4/82B2KVsx5TQfVFA/O8iEJUkCfYj7djFY+ePr4OWK7w7FCB+ehaZcriEeQpBeUBTwm'
        b'n6ToXa+sBFPtWialBr7lWL8g47k5aFib4JArXwiZ6EvQIONZrHAFs0mO0fgHvcNa2DByqvuYVOGYCS6QYsXjQ8NLL4cH+/EBdmiZPtDESAkxf0uACs7ME2zJ0OCBpWF4'
        b'hq98Azxc0zug9Tk9VLg6rcMCqJWz4/gcQyiovt47pr3PjiNNtL0NpAJM3ROx3hAKza8IbX8gQfdTzR0wlRCcluLhAx3ef2kH6eYZvueTCY+c5oOww19Z+wAXMFND5n4V'
        b'z3EnIGMeKQnvfflwP3Wfw7ZeSyp/W4MdXujmaBFPpRG9gRrSNwJOobtXR3br4OxLScIVREEBo3/NM6pf515HoNFQpKrHNs75YTwBip/D6nQmy+cU46LWMB8aXXOZcKqh'
        b'CCsG44bf0UKnd/yyFdA+Q3LgKQ84NwuPOy3CKjopvtYqZnsa3P3cTqRJJ82B8zoKSMfhmms2630TWycN3ISnZoSVSYrhRWCtDiqhFsq4qMKgeutTrS3r00J+R4NH4oi9'
        b'ITvmqtboDPPxfAjnK3l+eCx3FdSxV0f09n7eXloLZYbJuWmuQOEJ2vTEF16Bu/1dG+/MXFoE3CLHgY8W8o2eBCehli8jfPWAjWgR+9zBduIKoRBKKqQZZChNA7ys4gLH'
        b'Q95mLCYFwuplnOyhXb0qTaizcJAdBrcG78e+xMnCIzu5vmccq5o51jtToJsUjRg45qL0QQrG7njecTh0DtDKa4LbG8QtXnqNswCXQimRZCpGAEgRM1fIm0+V7CbUyXxf'
        b'QteQeJ8LH3OE/ujClQgyG2t0UH8AWvmYFcnY8Jww5gh3D+5ZvWNe0dHiSqFZeLlT2GwZaOtMvSJNhMiPK7a+Os6wQA3FfI5J2JI7UMn6XC+WefQuJQIe66DCBve4Zh6Y'
        b'QOz0H6NOVabxoxnuzhsKhXNVULvUi7rdSsCC5VxvEkhx6vgwolnZ32R6rcyswTvQhde405oXtf0rPbzi5lw6MtyjOVPn8u3YTunjDUGfvO2AzWsVm3dPg505PlxMSIyP'
        b'EvTDngsGCmJ5rPVBBvG56ZaNEXvdBhdtA7StTdC+psFrlPpd51rkm7L9OZ9OWxBq6t2AYMMLZrjCxQIPg7FA9E6bOZgWMUV+TEp+n7vmOMk8uOihawuWYcEOvLhFcuz0'
        b'sFBafC8ICvhqZ62Eo2yKoaOfVb9W3TAl2LdRqBxOPLENpqXm2/uUaIDn74d2oEoXhHed8JgCAHdYdfPx7mA6zjnFc5v6lLyR/BwFZxFmG61PvWlLPz8HRyf12ohu91zV'
        b'ag/DPLxLCU+Q8KTlQ9ggfB1ODFBaaNOlkCjipfBROsqqjkwQkLM2fZ0COaFLCWaKkAWIhE6tNpdyMG7XN1/wUFxLA3Mt/ZfSLlSjWOsRkca3+kDUfmU/agaqtFCiFzX4'
        b'EFvIuczmvtkd/bxOKwZtgLo++VTpoI7ykHJznMhWi9bDRZZ/zOhNP04vFw0tL+I52ak7GMg6EeqKhFsiZWk4BG0y3lRB3lRR4Sjfhq/zBCAb6rNlb9XGCUoVhXARH0KG'
        b'd2aqDKXqjRsY9qHdpDzuGM+0sDJrtuzQDnmJpQ+U2kyRecakhoKVskP3IjxW6i5QB22uoQxwWIbLDsO2jUrZxTSWczsKqtZQ2i95zqf75RKUwEmzSJaOLBole6lHjRcs'
        b'ncKuMWIV9QQorshQrIX6FJGf1s2cxodYY6axAs720Ur9xg+VVVwnIzwh+6ijGbEaWh/cxvO8aTRW72OlnSm0ZlHagWq8LSZqo6hbx6o7h9RKcQfOR/ImFyXeR2XCFR34'
        b'WKnvwIX9In8uhMv4gNV3CMsc7a3wnIJSLp2NeNpBbYahU0RR4CT58k7O+6tY7SOT7yqaoBR/wvz4/RcCVslD9K/CVaX0AwUpoixylNxcC6v9YEeMUvtRw1E+S0AC3KIW'
        b'AyXF1HKO1uuBF0Q+25QSKRvVWMGXy6o/amzm++AXBCXyHjUWxCvlEsybzYfEQw2ckffo4EGoWE0ZlsbzITFQvZ0VUrZRXiwKKfI+Ibl72HqYWlTQtELUnk7itQliKx5C'
        b'BdbLvuoAzFeKLFPhJG+aRos7JvuqKJlvElWWOjyWwRerJqDcygswjWalAIN52Mq5eJUg0WNWg7FOUEowgUZRUbq9iYJLl1O3eINSgdkVwaktjaSssYvsADtXCSmchi5y'
        b'crw61GWzYpe3NnEbtVxm85zHk0J0pbSxFaxyszBEqdy8KLjD2/6EmLu8VVCT2lu66cJbYpvKsYTCShd2GhYuECRroN3EKS6ExzOxy8cgcT25LsHFMCjho0KxOZ0gdDlJ'
        b'6RwrNbBawVGlTDRsDfnTrt3qvbwAQ7Kt2A/lXFViMidTg34l1xXa9eOhr/ARI5O9RPmI4JdSP1ryslKlpNT0KCsg7V+llI8Wx/CWJQtIt7s8dXPgUm/x6Eosb9mKdatY'
        b'6YjG5Sm1o7FKkaUGuuJ55eg+nFQqRxSGGoVOPMol+XW5VDZoE0KvnNVbFqzFJraFLp03lAkrrIImXz7bTE0Q8X5LjxcjhdCr4fUFfHv37Cdn2TVEvSFMcH5+OUUcPlNp'
        b'egArUZH61CklKsg3c2rjoldQiw4rPUQN6CLlQG2ch4QoAv6seIWnfZTqFQngkZBSTTIvbBnCoVUpX1mmcR6cM4YZ8YY+i7SL36/DpjG9JSWoZmWt+V69Va0GvCtqLfmx'
        b'UGX00EdrRUHp0tyXOC07XsNGo4fKc7dS7rLDaT69J7bDWaNTGztD6E8VnsBK3jIKj2zldbA7dqUMBvf8eYv3TiwxeulJsqVKrckX2rnbXo3dU4252qHM3V4lt5qylQ+Y'
        b'AZeCjLl6qHFIvGh7hrKyQsFvB5Tajbm60EVKSc2+i4/YvAkfs4paLBcKK6iNhSrekkGY6wEvqFVFKQW1mROF9VepIY/V0+CisvpGNdYJJWiAJmgy+qhovpv0tVuiCFgh'
        b'CaO8E5dg9CEcSAGFFEmCFg0ZA69HVtkYwQ7aNgLcXG6NFKHbhe1dJVoN1KqBB9up8S5t+CFKHhlJL2xzGj3VFJwuismaFmGT2O2rFF2MLm0gb2lnojgxju/QeDLlk6yu'
        b'x/0TK+wFRIqJul/DbqNsgG7oEMuqx048Kjg8tpycSwlpCUVoJqmHtOUR2M3PsNbsjKKmKih81abU9qBdQXuEMVgdTwtd66Fkg/TKNj1pUBucNmtdY9mUbXBjI5bExWCp'
        b'Bhp3Sxp8ROCaoudFwVEZGdu5WCyO00vq7SryW21heymms6GroWx5LJaHQftOLAsys3Mqbz/NyCXYIIaSY4XOoISQKO088rTapSpoOYx5q1LZURL70zPxScr5EjsUdUv8'
        b'6IodY7HjK43bM91TObjSFmrzpYO6/foDWn5wpeMHV9pDuk1Smmad5Flg1n74O4quXqZ+f5HsWFM2Wez8PNOUnu0w5VqybGk2577QAR0HfIkWp6mBO7Ptzmx+MhrYe5Zq'
        b'shG1XIsty5KSZQ3mBF+2OnYpE8hs3ABSKRb7TlNqdpqVn60yqpye7NrVe2ZrSU3NdtmdJrtrV4rVYbI4lC7WNJNFHkBrjzUrK9RrwK2FORaHZZfJRtMsNK3PFMe27Dw3'
        b'pY9K6GADUmypC9kyM2y5VnuwGMUYXB4dOYADm/25FbG/VBKMda+TLcFqSc00ZVMnx6AT8bU59vWfzNnLJonym8/jZCfYCrVQU7xLdrI1MrmvSwyJmD1vnmlZ3OqoZabw'
        b'QYikWQflTbbmWDhjgexToMlKquGyOK38QDw5eb3DZU1OHsDv87QV/oXEuWopazGts9kzsqymlS5Htmm1Zd8uq90pm5Y5rJZneHFYnS6HXV7YN6Mp296npMF0d5UlS+a3'
        b'mZD32ORnFjPggHy09OxhrSlhFfdFq1dALcFMKY5AqzhFfIQd/CB2qf8YraRKlqTk5APfmuUncYQNzdFroIT5Zilr6WZ/rOBdK32MCS0S5TB+ycEVqePFQe77e339/kFF'
        b'QWBWclxRgEHiDi4Z3VsIHVLAglMCHc6cohyAmTPlPRoJbrjE2SCFYSV2n6ds6ajsyybHWnFAGKcEYsqRWhPZESGFrWHKEeEtER/JxzVDp9Ghk7xkcUiITVDE480OaJxk'
        b'zKG56pZwLHVmuZ3fn2EYY9ytkSZDJY/ptXA3VeQhr/tFsyNFaWomP1A8HCcCGt7Yjl2ynp0En+aYojImVDkLIv4L2FGjFAEF4qyRQux1PsuiWdPYUaO0zkOcNDqhljMc'
        b'OxROsHNGEgEWiIPG6crJ5aShq40kG3wE53kAqodbL4mJ6vEYRY8uWiVeofBE8oHjBmwUYfXhuiB5j0FK3caxewXe3iuyt4eE9wiIS3E7BA5fCtc4Bw64gwzVa1lSdlUA'
        b'fmsmb4qgDKODnfVK0VPEUS9hlxt8n/3HG1Y3Mw0zJQe/N3eNEk/vEa49GTFLK23BOxSUpZQUvGb25fPPwatwlSnB0n1CBeCmnQ/algH1TAfwPh4RSoD3JwsdKM7BKq4C'
        b'bRS6uQpAHiiHmkf9krgKpOB9oQKecJdPlAO3NjAFSCUcK46JbwrIR5px059rwBG10IBMyiB5yyl4eJApAZStE0qwFNt5iw88JNDBtMADbnA18KE0laPBdjw7VihCIw3h'
        b'ihCdI1RkzWKuBXiO0hquBttRIBiDDG1cDabDZaEHGygp5NHx8VCo5YqAr+PrQhEWQxkfZdVAGdMEuEQQgGvCLMLzjIngSVgv9ODuGqEGFMpFruYg+7nPFCGaqQ/XhMcL'
        b'zBreNt0JjUwV8P4YJSe7CjVCS068auAEQxYIegFwXxhWGSGhekZv+UFBjqzwiFktGovHeAkNqqOUg2vQNjwtxHQfLm3iKpQDxxUdcofbplW2qeQhKkn609T8+OMdMdrZ'
        b'fscywt/51DZ5Y2hra2LyJ8MLL7/nv2Xb7rjdWT+bXxVzVzPZQ/7JkoIvRvw8/wuPJUerlq3+IO5Rdvhf/H6/7435eV94eo3vXrp/6I2x0y6dcqS9Mqu9/vq0uIQDy/79'
        b'zTcf3Y3612uPDh1pav/Rn995+xc3VzQ3ffbyj+sKPzeOPHPndOTmX8s/+9UP/j3H1Dimam3stNidcz/ZVhiWUvvTJ7Xvtf8+4pcZIQ3fMfxy0lvXy/boMqKSdoSmtv7g'
        b'zr2/fzLnlW3zprTPGLK8s3Dj5h/9Lnax5j9cF//yecUPF3+r+t7sXxTsP7v8T2WLP05+60D2osy31/6l8epbM7T62thtD/99/JP2/MUxXZh3YOJPPLynjm8/LN3fkBpw'
        b'6BOzwcl0YS/WYW1QSMA6OBEVopYIPKtDsGGak4EsNTZsCQqNDh4zK9AcihXBSMnaaJN2+7QY3pxGOncsNjEEihIZRtMtkoxr1JSfXZvMm7EYa+B19hhU4Aq8FRKqIuJ5'
        b'6ogUKHayU4w5cSMpHxGPIu0RjyLlhgRO34LFYWopFB7q8OZGrHGO4bA6mTLlkvhgLMiMZkfs+jlqH1K/Ouc0kbFdxQexjMRi6MRysukKDimlkVigoTyzA7rN6h51gNnB'
        b'YpPZk79908tV6cuRi9Id2futdlO6eLotlIGeJT1ePAQnsS8sAMqbWCg8LJm1Kq3Kg798VGqVP7370ctLxe57q/T8s5re9fTuQVdvemdXLfXTq0bzXqy3D33Tsl7q8SqH'
        b'gaV3ZCrEv75Hy+bs0RCU6jEowKRHy5BEjyEpyeGyJyX1GJOSUrOsFrsrJynJrP/rSzRrHeyJJgfDww7mbx3sUTsHg8h83tNsdewkXToifTxerWfc86trCtucrnRnrNi/'
        b'PslDxaZe4efBOXIE7Pz/RTyG3bHUjCUJWJ4Yrcshp+STo5k/FW+62AN+WiyA47FxCeSBTxO0J1yvkoxb1Lz6/EiU045C9Yt9CYFHWJhxSqpGASG6/og+XOp7KE2brlVw'
        b'vKZQQzheSzhew3G8luN4zSGtguPTCcf/WPUsjucPJfYD8o7sXSZLL/QeCLIHAupnAPP6v4LrHdbdLptDoLkcq4Ow/S4BO3uflBwIvBJ78RgxEriWZrTtsq50OLIdgZyY'
        b'hVrSBofrjF/GroDszy5iUKyqLEqMeHaFg03BAP6qLEuGySbSjNRsh8Mq52Tb0wiXcpwvZ2a7stIYbhUQlCccSpIxOEJdaWNLfgqIKfmxmMJDnK4cAroK7OVSI7wewHoE'
        b's4nMfwWvap/Dq7oE14v0OXCc7blHMn0p9yzEorjAmGBoWS8e0GQ3EuOi41US5epFxgV40X+97dUfB+nkxUSl7vEPf5Mc+iuzJcqSlZ6V8nHy+/T6ODnKsiO93NJibbZ+'
        b'nBz4QYul2bLojbhUr/Rmi0f6z+IM0uTvGVf7zzarnZMZAIY8lzEwai0ZAhaxemVIIHeOk6BLi9eHwSPeCy9ugabY0Jj44GiKm4rnGws3tZgXaSdAesusHmDqg3kBXa+9'
        b'9xjFQ7hPvZqP8GppzJ8N417N4fvUF+l6PHpVqsegKIdwJt7sMoT16T+9xsEgvoM5E9GNOxlG8Ef9nEzrsP5Ohi0Sul6GS4Ms8iC0au0E5ppci0VAgtdFLaJfJeIqIa6C'
        b'Zf7QCaVwPlizLXYOlO+GdrgCD70I0VUOoTBWC8c5Dj84a44x10clqQgbhsrYqo7lwGIcXLYZc3ez+4UEigj418G9AI6lzBugUsbbvuFaPBtHEbNS5Y83laIXntSr5XCH'
        b'WlJlE1oZC3egRckPRuwbY8zN1RO9o9JuUq6arHEKXErZ9drTikcndoTBfbjN/ecKKIBbvOZxGar6Fz2gcqkoviXA0SByrSpJDeUqaPWJzJo2uHtkz9m4NdxBiud11W6P'
        b'dI8+N6n9Wjf5p68qd3D7Hljs+EonwRwK6/71RYOvyOXZ4P/1VD41i7MlW53PJ+/PMMjkkp2a6iJ/aE99ntHe9H3l6mWmSAreDuYvV1BcSHVmOyghz3GlZNnkTCKUso/3'
        b'VPx3JCX4DkvWc/SWk2WG9uPNwjbFxR/ZD1wXuT4wmN5WrGBvkYlrZ9M7sRe4PHw5b4iMDAx+jmK/NVmy5OxBixBskVzOOaL0QFTTmOvel/OMANnfNwqKfRSzc56Phezv'
        b'm8XDAZv3P1b7YM/EG5+LJcMSVrmWMA9QPof81SBP+PfGEoodxYPHk0g4xpPfLfGjpbqINFYkWXRiVqCofNRPGSatmJVIn5LHL5iZJYlsvB6PvyBKJ4YwaTPmKyWMITnY'
        b'CiVQCIUU+taOHa7yxAt4hdPxzvWVMkOXsAqK94ep00QFBa/hJSxhpd3ZUDCSLvfgHH+SctG89RG0xHA4pZLC8cE6TmKlbaj0x4BllHMlB5+S1ogizmjfLdhlYGXa09gg'
        b'rR42iXcNyDFKd+VgVsTJ8t+yS1pPKR0v+dQtwBt8vuGHaLqilaImchcK5/D5IqCZJm2QqTtHgUXsUV7efzoW0IAHM8X6mydilZiWBP5YWv1ioi3o9n2N3EGNDwzS9PLZ'
        b'PjDLe+Un0+LPB1ot//rW5rvLDaNf3Lu06PtvWJblHfV459Xzbyf/zLR4eHRQ2G//cj374Bt3J3+87HuReb7Fv1wWt+inx9fDqJ9unb3dc8YBGPNW/uu1PnMb/L5z6le6'
        b'FSUjz4zw9f3dqrbrw6aV4mejukM+mR/aEhi3MKBe+45z6Q++89MT8T+WEn8z1rFgZ37ZP7/r+tXBG3/cGv4t+fOxjuwfWDfkGt6TNUffyfwRfv6lYfLnEedbhpk9nLzM'
        b'cWW+PSgd7oQE9KVnM+c42aM/2EBAudsY+Dw8OJrDEQK24gMnO8kPpVh3h0UGytRYuhZG/UKgdhMbFmuQZuN5fTSNck5kVNtMsjEWS8299CAfH0ojwa31wILZTqYfBjiV'
        b'SGkfhZl5eCVXtYzC1FmeSyZs3oQlpGkPsSgskXF7SB0Ij008h4OLa5glwBGooCDem8RhZZaY9SLkT47FslhzKJyFUiXX9J2lyWCbbVYJ9ODxjTO3p4DGU2RpFHA4nJkl'
        b'4MxhAoBKmsauakq2fHhC5qPSqlnyNY1eo5WXY3g/wPM0VerRkO/vh3O+LsvS9MuyRvRhH0b7037Y5+TY/tjHRPf2EJCpVjKsAB8o58m2NBTdGgI0ZXjErHKNo26pcA+v'
        b'9B6m1GK1cppCm1414Ic7fSCAPXJJEECdru77gY7qK3+gowT+L98f4AXXCi/6FTA/naN0Hq/7H1X8b+dFg7px9qd+zo3rE7gXHwL5W/s7cXLV9c868sGdONTCWeVHLngL'
        b'HrAyuISX+KEgFJMV8Kdy0uI2kzlhcTyWrsPCOPWwlXB142TKdS9DNX00S6v9DHD71f22c7/+R4HdbrWM/k1ycL/s4tspWekfpUkfxJnj3iv91o7p75rfTR7zVvBpn2Pp'
        b'byXr33emH5QWeXl7eRaZdc6pEku1q7HmOddB2UKnkl14D+EWPcULrgYx14MnsE1xP1uwTdjsfTyCp1l9qF91CMpeMWm3T1Ccyc5cKBzgTKSR+AjyuTOplpxMbfHccLjc'
        b'V0SCkza9qCLFYpWwOPWgZm3IsDr7jNqv16gnM2P24HUVh/9To9WIqsbgKYlKNHJj5A/TkLHIw4QxHpGe+PQ3R8Yw5L2ylfiVoVupewl+4SoU/RU7U7ulb2xnGWRnLQPU'
        b'dF1Ols0p9xmTOBMiizGxu+kOSwY/43nGsHqN02KaM2iiPKBzQGTihoT1azcHmyKjVkbGrtsQTxn0soTYpMjEFSuDTcsieXtSwob45SvXmr86rdYMYkM89u9cI36x+DdD'
        b'M727xm6SXPNY/PYOJrsqDWI/dSyKW7Pz1ShR92GpDVaa4aoXVO+jVzQU7ZPgnN4LCvFiCH8IGi764sn+g8lyeFaITYsmYrMWLhDgcdui7pep5dXU/w/f++I3ye+mZJKZ'
        b'fJwcxwzHWpm2cVuztdnyUfK308PWmi1xlJyTMUnFUeFps12z5kX8MPyHs/z/UWU9uyx8bunmd9/zfsO7boyUecHv5pt/MGud/HikDC7iLW4iaq9QpXyaBx1O9qtVqIJq'
        b'bOwzgHlkMdwGmP4HkonwuHjUH8+y2iaLiVBN8I0XN2syuP1BA1xdFsvjdYBe2jTac7QaGjPsAxR4cAPxovRE7pfHj+i1kdkeKm9uJT4imx/9/2AnbEzAADvpGWAnbPFY'
        b'PAqOB0UFByb0ZezqCMkfHmhHwnFoNIvEfgJeyxJBi/L2ijAoFiY19vAIKNFmTsa2wW1Kqe/xn5z21fe+gV19uO3Z+l7/EMYLYXbLLp4iDRK5WILETlVzrHSDItzAWBIt'
        b'rCvL4nRSvpNqoTA0kCgPaJY0UUJ8LtMbQKsv6/u6pE8kef8XI6pq0IjqIYpseFIVN0hatBPKvyagxr3Cvcnv/EdL79rTeVL0+7WR4kQQHyI7QlyDVTzMshC7MUo8VFtg'
        b'jukfYj2xkUfZZ2MsnDjIySeZ9dKKXRP5geO9bamS7d6wWK28ka0o+uOBkfdJcmZ6nOU76cFrn5B70f4+b8zC0Z1na8YsXDZH9pIjUjviPWO9jJsWv/6niE2LW6dFhmhW'
        b'L945ZNNBr0gCt3rp0fARdx63m/UC0RdDXi6LytgOFwer+VE2VeLkT/3ehO7Efog+kZfVWdQsjddJLyToMW/dIWjZz30UXoOLHkFPEwi4ujIEmzGfx98Rajj/NIYHQ0fv'
        b'IY8jhIdwDdT49QvhY+FcrwcjJmv5AYwV2sOYdB9A+bOcTIJKLZ7bAbW9EP7r6o/ePK6TTjOL4Y7Lv9dxrWTuylvlpRYB3lvlGNvPdfUYmatLynYwVNDPhQ06IXEzrs+Z'
        b'MSoLBzizbw979pADavC2X+zzkmbrG7oSz00MMGsSElaZVavM6oRVthf9bDr5C6L5n41LNpywrRu+zO9YRvoLkz/Un8Ct3YndiSNWd69Z8/0jeReW6ONG6C7kfbr/xkef'
        b'Xliz6KVNf9QevvQwuviDJzVXP/2PJ76LRzVM9AnMP9v0d5t3dr70ZHZITHrrrB+NzPjYw/jkg89e3psQ8iRlSPHeqgttEbDizK0Zx+SagqYMZ0zZ3J0jN6xuiJi2eEKj'
        b'Zkdb9+OTfm8FNOXFtDRfObblSXOG55Dgyydm1NgsY767+Y2YjR01c9sun3K1ZWjG/cOb6bdvnNqVlWF40ZY66sE/4PbPOxo04//le1FbM+WzU8dfPviGY+Tb8xMM55y7'
        b'86qccvHf130Y/Ov5f6vbfzfg3emhfx/0k5HXPnh77r9ek/NH/CncN6dqq3f4m7s+nfXutt/nxuxJ/P5/vG64NMZy0p327c8K3y5957tefyhoKo2YvFWv+01K5fi/3fu+'
        b'8crZX/1yeWLmlf2aqo5FP2g/dt9Q1rot4gdPmod9EFD4y57yd35c/ssf1+9+r3viX6rWdjviLjriV1cVLVj1adr4n1wr+M9za5e5jnvsMJ56851//OPvvnvgk3GP4fpn'
        b'nzjrftRdHfJP3yoL2VHV/d7WP46wruz5XXl15ZSJu/7mD87mP//d+5/V+57f+oW20r/4t2euv7k5dFzgn7a88asvNv2b+/5HP1+3/UznHw7Ux4/o/O6ff1Gak3Q2zNG4'
        b'4eeP/A9W7ry869HvH/5L/Pkv1zv+LeyM+oOPttrIoLnl1cAVvErxTUXJ+gNJNV8il1eFRdyyoPrQkoGZdtEWxbIe4QknU7twKJ03WILfpY1MYb9Hhlt8GqsXurGEEERZ'
        b'iF7Sb1fDCWibisUTnexUDdwLsSooJgTqKEEsjI5L0ElG6FDjOXRDp5MVlh1wZkMs88XrsTGEHG5pNOtyXY0t0yL/m6elZp//VvevpqNzMOMf9ML9hEdSUla2JS0pifuI'
        b'nzPLnapWq1VzVCZ+yDpM7aH1V4l/Xjo12bEHv/7f++ehHqZi/zxUIzSsDjH+JTWtYMRwL1rNaNX4ALVqrC+9hqpVjvG9vpLcnTopqZ+XG/L/L3GVY0KfS2QTsTRRnP78'
        b'84xnSxJQT2kcq/RUYAWLz1AEFSpoNEg+YzQTKBrY3gq4pJLPMMT29h9DSh54wdIRK35tn5c41cs/L/MXo74I8+88/Nbau5tWRDfaCi5tsXQe/sR+3Jb+vmX9iMTS0d+L'
        b'ya4rDY+qbfb8icecLb8p+/npQ0/2WbeHflTuf/DPzdvLTKs+/MX1771Z9LPiT7+fXHnb+eGofQ2rJkZd/vyf/X1+a767JePlWY3Wt0Ye3Wm/e/nD8tcmfhr73py/+E8c'
        b'/n7Ab1+aHjlzMdwzDxEp7IWdrGZCS0ikhbBamBE6sXOxGpvhxGwnX2oHtOIDFt46WDdW1hqK3dCClzXQCIVTBJ1quLlFiIPFBUoKKrbhDRLHMM3EoTGijvfoxdzY6PjA'
        b'eAM2+Up6rdojCh46GTiaNnxrUIxOUsXCNXws4dlx+MDJfxpaH05G+gxIgvKwWHID5RSEKjTSy9DxGl42QAWc9OcOw4R1UPl0DCVBt8U4vTRqhTZwKBbwRZkWH8AuLCVj'
        b'DwvcrTif21AtjXVp4dhwbBapTUtuBkuwYrHEIGlD5mOxCtrx/CFOYdr+HB4O+3GzHIqkcVCrhSuRWM1dzyQoOowl5hD+q1KmJreWqyTfNZoNcAMfc34hf/040UMVTfCD'
        b'rY5ncypayS2d9Cpe5h4KKrTJQYnBWMz5oV0iD3kXz6vxzt7XBiQpE/5n3M//4IWSqq/wXza7zan4L5bQSkMYrqHUTKNVMQ/A0jM/jnUY2vHSTGMYKMwxsc8HTOrRZFnt'
        b'PVp2stKj4xl+j5ZyBWePNs2WSlfKU+w9Gtnp6NGl7HNa5R5tSnZ2Vo/GZnf26NLJfdKbw2LPoNE2e47L2aNJzXT0aLIdaT36dFsWZTE9ml2WnB7NfltOj84ip9psPZpM'
        b'617qQuS9bLLNLjst9lRrj55nKan8CNia45R7hu7KTlvwQpKovabZMmzOHqOcaUt3JllZ9tAzhLKNTIvNbk1Lsu5N7fFMSpIpD8tJSurRu+wuSiqe+jax2AkOVvdysKKB'
        b'g/3gzMHq2g4mNwf7SaWDeSsHq7Q42G8aHSw/dDDk72Bo2TGHXVhS6mBK52DW5XiBXdghgoNhWAf7vwMc7EfQDvbTRcd8dmGY3MGyVAdTeccCdmHZi2NWn6dk2+HV5ym/'
        b'WNHPU/K2Lz16Hxrq8UtKUj4roevLsekD/7sskz3baWJt1rQEswd7mCctO5VkQh8sWVnk8CcqqsPAMd33IvE7nPIemzOzR5+VnWrJknu8+2dpjsW9Aux3Efq3SPyfXEvY'
        b'LV5A06q1Gg+mY7EjWFRS/ReMfLU8'
    ))))
