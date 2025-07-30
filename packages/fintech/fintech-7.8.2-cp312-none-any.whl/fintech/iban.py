
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
        b'eJzVfAlYVEe2/+2Vbpp9axbFRkFo9t19QQTZEQWjRoUWGmhFwF4QNKJxo9lBXEBFwZVVWVxwT6omL5kkMwPBjEicecnMvJmX2R4mzpjJTCb/U3W7sVEzM/l/8//e9+8v'
        b'udxz695Tp07VOed3Tt3rLxmTH8/w98stcDjO5DDrmTxmPSeHc4BZz1XytoiZl3453G4Oe6YW5/C4jFLQbWgpYTTi17lwRZjDN96zjwO0mXLyGQ5TJhDnyYVf55rHL4tK'
        b'kW0rytEVKGVFuTJtvlK2skybX1Qoi1UVapXZ+bJiRfZWRZ4y0Nw8PV+lMd6bo8xVFSo1slxdYbZWVVSokWmLZNn5yuytMkVhjixbrVRolTLCXRNonj3NRPTp8L+EjPZD'
        b'OFQwFZwKbgWvgl8hqBBWmFWIKsQV5hWSCosKywqrCusKmwrbCrsK+wqHCscKpwpphXOFS4VrhVvFtOOM3k0v1dvpRXozvaWer7fWm+vt9RZ6sd5Rz+h5ehu9s95BL9Bb'
        b'6Z30Er2LXqjn6jl6V/00vW3udNCtaPd0LlPpZtTbbncxw2XemG6k4dzdeM5hyqeXu69mZr3i6g6mlLeO2cER58q5Kdmmc2QJ/9uTgfLptJYxcnFKgQjOF23gMuRa8JqC'
        b'xS0wNTpPIILwXidcjStTk9KwHtemynFtfMbKACGDbuu8Y/j4vjmupU8/KzFjLBjGJthJH1stcmJ0G8l6QEc24kGxZVoc8KiJz4hDvT5Y75+QjBtXi3BlXAbwrMP1fsAf'
        b'18Ul47o1PnFJuC4lKTXDBxr0QdBbWlxChk/xzoC4eH8O6uIzWlTpGInv415dOPSALuMLa4D5VC7AtjooLc4/EddAt0m4Kl7ArHMtQfXiDai5OJtjog4rozpK4XDUsgJU'
        b'QueJD3MkhDkUwcyZw0xZwGxa6a1zregcgXoq+ZNzxKVzxDGZI67JbHDKuYY5euHq5BzlvzhHkpfmqJOdo/e3CImW80/7ZyXNk4Yx9GJGLJ24pdOEWUl3VBr2YmehiLFh'
        b'mLmPVVkWOCacvRjrwmfgb+nq5VkFiXOsmE6mwBwu/41x5j+1Y5ZO2Jcpmiyvh0yLeJcpIOa9KKmZ0+dtbcEszQp9HPr2xjz28habL62PJGa4c1d+yvn72ndWHWbGGV0g'
        b'mY0h3JMCswHK9/HBVY4xQXEBuAp1pvvAlNf7B8YHJCRzmEJr8SJ0F9+WB+nIIDfjg8s0FjAnuFmuYtAxc3xU5wjXcSO+iLo1agGcVpeJGKR3xEP0iQ1RNhq1GVyuXezA'
        b'oCpcjfaxT1xwxAc0+Do5bUiLYlCNCA/onIhgHeiaiwbVgZpw++xMBrWi26hJ5wBNoag9Alq40HLWGp9n0GnBLsrNDA+s0GwnvdejM7gFOnoDn6QtmeV4UIP7hdB0lIjc'
        b'gA7hOsoMX0tFRzU68lDjcpCtGvWVU5Hzk8s0luSBM/iwjEEtqD2LsrIUo14NHiRyHUcHcTMws3ClrNDe2dYaVEOYnloynUEn8NEM+si6OFStkRB529LxEeCFD6BGtvfD'
        b'uNZXswMcNz62DRRWx8G3ae+4AldJNdbkrG2dmkHNO+U6Z0Ldh5EdxIOWpP9efCuGQWfAoiroQ4UePhKq/G7cVgTP5OB22ksuuotuomqYMY5ojYJY4LF1VDDUjgd8NXiA'
        b'TOVh37kMqo/D3bRlMTo0Dw/qiGBnZegug46gfnvaibtokQT3kV6u4KZCUL6PJe3EEu9P1uzg0jF14jZQfowZ20ljmkyDbxCBW1AdOg4XnOW0ZQ/qjNBY03lE1S6gMHQO'
        b'9dAWj4D1eFBEWs474R4GncQH8DnaTbw36ocm0v8lPBAO/c+yY7V/ADVNw4Na0tIyDwSrL+dQlaE+fBldwYMWZDIvoUZ0DxYT7nyNPpXoCyuDLuUOXFcM3MA7UgliJe54'
        b'EPcTqc9JESyyYxnovk5KZIMB1oGPJA9dxvfWEy2ex1dpGzqHB/B+aKT6ccAHGHQWNeazK7rXBtdCE9Fp38pccu8pUDGRImIu6oVTutrQHZjTxvAtVHZ7XIFOw2yTvvrw'
        b'NSLHWXQA99HOrNF5fBGEHCStXahhF+gpGbfSNnwN+qogjcTqetdA96eFYHREEIdw1ApTSOUHxbQRdVQto4JIwrBeIiIt1/ExBGv7QmQQbbDyQnUSPECYXQsRgxSbcT1t'
        b'iPYTSUrIaHvRBXwL1rYVGmQlGACbuS3B14kK+3G7PXTjB0bHqsI2GlrIeAdxHzpIFnGfPTtbvfi4PbQJ6BhacS+oF90AN0I6i8R9dhotEU/vizoYMOJr1nRRovve0RIN'
        b'6emKnMxvc4mcdoTvz3ORmJN+buI2XMOgi+gWqtS5UdPLyEfVkagCXccN6BqqETA8fJaTio6s1LmSoIq7Y1B1yXolPoJqUZWA4edz0JuoDWxNRnq8gm9aQzuqRPfIHaFG'
        b'JmJUy5XuKZDzdHbUemfgBlzNs09jmCKmKAjV6GzoYt2KaxL55V7gTJnN8Xz23pv4FjdRSKYcAjGTw3dlldWCe2YaRo2aYsioe3C1zps8cQPVvY6bsD4Jd6PuSNQpUCSj'
        b'Wnx+SzQ6tz6ZCdcI0NFodId1tdX4JmrQUPuodMP7GFThpKJcIkSwjoEJ4XAZH8VHsD51DRDhqBsf5TPTcC1fHIRvsML0rDfT4KtEmAZ0Hl0Dl4VPKXRy0sEtT9Ax5YOu'
        b'ow7CKA71uKDLk4zQXT4P9xaw4pzBrajLEEXwABcMbJNA50u6qMjA+4zy9LLyvIbrqEA9rECH+ULAE+fpmtBamoPTJa7idAoEEnQK3Y+k8qArMNc3cBMIAZph+SCihO7I'
        b'UCIeMArg4SEtn/XEx6zASavJEqrYnQUTlIiGdD6EzQWOA5GGh69SBVEVoztbJDKIYh1r7JkEmZkE3w5ifV2Vc4oh/uGG7RAAEfhrXRBpOQVP3SOM8kBvzzVNTq/gWvKn'
        b'i8gUoBZsx1VRrI6ag/EhQ9zEDeCdqpaB6ftDS2lJ+uTAavcoeZtZmcClnIDZR9Uw+XF4SAge46CKslrhh4+BoydM61ZtJGHuPKwLWH7MErw3CN8Bt2WiqDiYNP4qxg0P'
        b'8sDt7EMHWA9bjc7GacyJqpsdshl0FHV76eZCQ4ozqjCZeBgMuoQbJiePzlxHMuHekyzcnMxsR1dE6ObMbdRPbMQtuFODqvjU+e0lAfUUPuJM0cm6HegIkevy5ATygvAQ'
        b'Oowr8VF0KBcM7gQTgs8IYBG2gT8i7NaikxwjoEA3wJJQDd4PQ6Ur9LQNZ8rCisMHhXR9drHrs4mH76CbmI3N6OzuAI0VGe0J7WJYnqgPXaT2YgFjPPyCwcQV0VF2suuz'
        b'gm/mO42K44CG0C0jjCkmwa8VgFSTLgDa1P7c51xqnwvFWgzEvF7CLXyXALVkaFiRrkdojcgHQURFp2VqXTCVNTTOyKvz+cLqpmxB+euCCatQXC9AbWgvjIM4zQjUtNAA'
        b'l5Zg8MFV4mC6uGCg99CxqZaM9TEAdygvdoi9fBGEzNusl60V4WYjvMKV6BhgIoetVLDQZJhS4ASeav8U4YBxDztoatMB4GE1Gfgg5VeIbvsDO7LuW/B1VA3oIxXfZQ3s'
        b'lNUeA1rDt/Fpsia7YlmpT6Oz8aSrAtxksCaCtRrLyFJBh2ToLNhqMr5rFiqYybqyQQjjZ4wY7zYCj9iyfi2rTiLvm5MKNZo83r/eJxKA6X10lcisQWdEkK7cxax5LJhj'
        b'bcSFM0jYakC1TtT08R0/8OFEMmd2Ul40fIMGjgk0ACXO0HEusVmmYWN3K26ZDasPA26hLbPxjWUGMInbEACMFhtcyWL5PogCNyYX+GQsiJaBRjrAGbaCBlLxabNA1IRP'
        b'UJmdXi8xYDbUs4QAc4B5rAZOg0Zug+3hw2KDm5kiO7su+Ewgui3YshsEIAvKezuq1ewgk3M0gcxNbdoc6kJhSdTvMfiXLpbDDlRnEmG8eTCZQ6+xuOHctlwjXAQ7B3fQ'
        b'CAigWzcb2vxj8qe4qTdWUluhduKGr/MAZ5xCp1g2+0sx4PQbJL6c8iAQ4wh4iT7WrzbBaE4ZkKeVEoAnAx2EsIuoB0ScapWdJla5GzVSo9wuQM24E3VRfotwY4LGmvR0'
        b'HrfoiP/qQPvZAN2DTs8w9WBxsXgvEMYAxOMBih6wYpf2kYVuRtBriboBzAXDoidcUA1fZ5TpCqu/UkjSTKzxHN8sPIFFoAdx/+xJgNyEr8KYSmGFktQbLpxFZ181OnqF'
        b'jwYskqOWo97ZjHp2GD4qwg2qaXRid6GzuUZoHZUH0DoniXaWEwbedZCFA22wYO4QN3lzMTv043Cpc7IzWI1BNtSKomUCJhy1CQDz7UMGVNEMK+o4AHEy6xfipsHYnfBZ'
        b'uhATPGF6J0Pd1MAJfhvViIkGwvBJAToMbAZYVerzCPRlEf/sdQTgHnNkbaTfbu1zR1k76SjoFR4owHJLBCctTScwm4tuBbArSY/ezDMmCTvxNWIbN9AtilXcZm9IpHEN'
        b'eOgtMqbaHcVgq1CtmQfqVxjWNt67DiSjOPoCoMmzsPaCwtjgNIh7ZzwfKQnpdV4GRiSeh6FrEOfi0EmW07EyCR60InyuoOMkrpwDEbpYzTeXL5tiJuXg0cma62LtpB8W'
        b'XRiqopoq3AELZpANKQN+xAdedLCmdaQUtF8JsXZwSqAzAINpaB9YLIdPJ29+Ivjiwe2Ewym4GSytXouP6/zowkVHAUCYBqY4SAK7TCwAVfDwLXQqlZ23BtQ1H3iReWtN'
        b'gBSpIRzpdTOhZZqPFFKc4y+CFC4BKTfA7h13s5HodOmeybQNHY4k6/FyNnV183F/hDFrm1FKsoo7+awqqyBG9xtztni0H6KpPW5m+R0Mxv3GnA2fxEdBz6qVLLwcQsfm'
        b'TJXnAOqlXuIyq+c+0DO6sYHtpB7VA2gw5njVNDRtXcO2dcO6ADvSsWZ0DkPAO+zgS+eyHO0tMfiPLlZ9Q46EuPrcgVx1RldZdKAP3wpcyDDalRh8WtOeUNar7d/9wjwa'
        b'zMfgArpmQLADbiH4hAA8YEsEHfs0FUk98TVqRHifJ0Qa6J0Fs2chCel4aWWEs+APGHqpKL/XBKgBN/Pp3O4uxIcgkyXL5DJ3GwOJ1FHcw7q3i0uUU6MW8RJs1PILgJi1'
        b'Msls3uI1lMtC/KaHMR+OgpTyLM0DyCDx7TA0NNVTTMIpoi50Ip96CnRfgOohwLOlkV3ouhL4EZ31i3fA7EaDS6LsbtnvnsKNm20QzAbkGoq0RfoIDjoJln9xqXmKBbpC'
        b'dVbsiO5MZuT4UgKpXNzl0vWyAQzt/AvZSM9GEycu5+EbkDRfYus81WA5Byfzd9zuC24nA5J7CnUaxTTrU0W/Eu8Z8IROUIx72RIIBJmGBZDyCymvs+gIiVGt+A5V/5Lw'
        b'7BfMKvR5zuaGb/IgN2gA8EHtYQBXbDLWDqJQF3jWdADevhRN1hjBx3PQOB03myaS9/lWcyAyEsVbJOKjEhER6JpgLoPO4+v4Jo3xWbnoxFR5qsupv+hh5bnMw5ezSll3'
        b'cXMBPmEsV/SthVQNV5eyzvTQhvKX4JthSeGjq8ia8jebg26wZbByfAx1SrQ0+ODWKDAc3JFHWzYWrjNWPfB9dBLWWwG6TEMiJKDrDZUFHwRB9uJcO3o9B1UlSUoIq05Z'
        b'GM2R0g25x8Yyo0RdBq+8z9SSiSO8vxDgHy1LoUGppIRw7/ZazYDfu4ba6bLMhdR44NXrEg2uhzTxwBZ8bj2j1mi3QoqFK3nstB3HFeiKsU5zeCGYsh8gHpKECAhmesk3'
        b'BKNmMmsCO0OK1UPyhquvs1rvzIw1lnU2oEZYAgKYU7Iu15ZsIpyW60wy9+c5oTHBRU0C7Tw1G/cv5qNBYyEIDYGLOYPv5RlC+A7GWAYSIlIFKsTX2Uy9Gx9cJLEis34n'
        b'Ip0UiodiWZNtcHZ6lZebjPO3IM+lbq6dgI+9yynA4MMcHXs+M7Xw//WX/KRgewRnpcgsEu0vpIENgOmt52oz+hl0mwfGJ9gMM5HMhEoFqMYXH6Gawe2owpgjG1B0HDj6'
        b'ZnYBsFUNNMDno324gl0u1V7OL47l0hYqTC9rS1V8EVhcLbWZJG+8d6prsUbdJoa3gIfvLmLocN9YhQ+8nCk+99z4noDVUZMAnVqHzspFbDkUnQ6XWJEweE9BYF4X4PcD'
        b'dA65O9ElCe6nRgjg+CbMVCa+xi676ln4HLSRx4Y4EvCu6BS6QJvK8T50WyIm0eDOejTIoEuQI3bR+d0Wh+9LdLS+rVgBax+aTrNL4ngYajZU+cAaawA22syijywB1H5E'
        b'oqF26r4JPGUiYsugaN/aCAi21PHdRbdJbD+PD9tQNLxrN+DFavAI+hK2xId6DaaJ9JGkmsdHgyHoZDqqzmBe2yjEZzai83K+zoUmEODXD+HqJF5aAq7hMTx8D2JBGrhn'
        b'ml7cdML1ibgqSchwvT02cYJAV3tpTXEBOhqfiOuCcK2fVisne2MWNjxHQKe3WGnP4P3WfikA5Q4HxPEZ/lIO6LnTPZvsKRl/ZDeHbjRp4XBUaNz3PM7oOXTvi6tn6P4X'
        b'Ty/JFdOdLz6XqRRO7nwJ6M4X32TnS2Cyx8UvFxh2vl64OrnzlSfnfjYB02YuM/lFk/1ajUxRSDdqZblFalmJokCVo9KWBU65cQoRz24T+24tKtQW0S1fX+MmsUwF3EoU'
        b'qgLF5gKlP2W4QqneZuhAQ56bwmqzonCrLLsoR0k3jQlXyk+j22bcjFZkZxfpCrWyQt22zUq1TKE23KLMkSk0U3jtUBYUBJpPuTS/WKFWbJOpoJv5svR8dj+abFRvnuQS'
        b'+KoHNquy55Nh5qlKlIX+7FNEwGXx0VMkUBW+NCLyywbFKEu1ZAhKRXa+rAhuUr+yIzo2dZlpZ1qjmKDKf70fLdmaN3ALlCXrNFoyRqL31akBYSGRkbKopJVxUbLQVzDJ'
        b'Ub5SNo2yWEEF8yVnvjIlLA2dQqukO/1ZWelqnTIra4q8L/M2yM9qnC4tw1hkq1WFeQVKWYxOXSRbqSjbpizUamRRaqXiBVnUSq1OXaiZP9mjrKhwcpH6w9VYRYGGXiZK'
        b'3qHSvDCYKbu9AubF3V7blFga/u2z8E1SU9PtBsjPoKo8dITu425ydGbA/QZzC7Kmve9gxrCR7A7ZtkHVDG6EZ9cx69CbHHq31s6cgRucZXZZFoWeQnYr+IG3NTMNgmxI'
        b'cFbS+VILlsVruBsdIuWg/CyG7OS0oPpIuTUbXN/E+jTShM+J2DZ8D/exm2iFhWTTEV+Ph0SSAffUg67rbKEhyMqCbDqW2NAHmhOKWDkvJ6B7dM/RK4chpa0zM9jRBsxR'
        b'kQ1HdGwRRGW4Pw2xqDrODcJ6MY8R4T7ImcFxT0OVrAsfwMdKJNuh6wZ/QPAAjwNxE5U2COkNe5ToahFHRDYpGwGi0FjBR/vxoEYIuXIaRFJIjlAT4FHqMdt34Ba6gYkv'
        b'4ssMPgzJJz7lSx+bCTH+PN3DxCdwK4Mh1z6y24mKIQagdJLuYi5YA8EEAkYK+G4aSTbiIQlRzWGiHmhYBpqhTr1uiSUehMFCwnGUwQAFGxgzqoRZ8bhLs8OMScN3AGiB'
        b'ABs86RML8I0oUlzD5wEkEcmq8N4MOY9244zuutO2kyVsEzqkYietHZLpDtpRpDXbTTi+x4L4G2gvric9AUBuY7uCJPQ6fQ7UwKHVR7IhTpoaUB+uk3Ppk0txC+6hraDT'
        b'fkNzNQBZOrAGFb5Lt63nQ/spYK5Ed+mC06XRVxfWenpk+YfYhzHGfZshfDEsGO4liLuJ2bwWX1f9/j97GI0NYIDXEtbtbkxMwcE2h94t+Y8UV+6ynhMBcW+Js971WJtR'
        b'sKLrSJz/hs4LHYve0tbPXR74w7F4366Fd56U/vrLJVfO/F46VvhgU3+vg0XK6M+8Pxjf03daGb7gW9/5ue81FN468/cQXomjlcv1RbPKHusPtZ8f6d14X384/Zubw28d'
        b'isieUXn3U+E6+8MBnx2ouZd7qnead1fJb7piDn7U+0XR9lXZBSVvBx7YfTrnS8mfE8Zuy9fMX/3t/A/+ZjnL7E8L7626zk8/YrN7e/0fFjz9UfxvEp2Pn135X7O+/k3n'
        b'jM+Gf1389zWR6R/2/8/mD96I+uIXO2pWRq1d1lefUHLYPf0nH+kmfL9xKH9ccfdS9MdmE7Fvm/95i1lmrmDB0d5vGUFNWlpmvdzsKVmndrsAMFTgI34BPnEBXEaITnAD'
        b'UI/2Kd2IrA8M8wuM9/eVB+J6f1xJVu41Zxl/U1TZUxe6/HFnYmpA0QpUmUpBhSSNi+sWoqu0FdbEgHgBTHA1rvQNCOQA733csFXowlOS2xWhikV40PCuzQ72XZuSAF9c'
        b'FcRFe19nAtFdAb6aJn1KllDczmBUZY2rk/3jcR0kOOFcK9y88akMmoLR2ZBE9mkEvJIo6MGDXEd8gIeHPFVyyTjXR64m1vC9Dhry2oxMttf4+9pxYa66aKeyUJbLvjQW'
        b'SELu4nFzGgAyCbHT5JxLWDTCqvtqL/NkpYBxcB6TThuzlx6f3zi/aaF++SNruzEnl+OqRlXT1gbeI/vpbZ6XgtqD+jwfzJwzweU7eo25eT10CxhxC+jIGXUL69PcKOsv'
        b'e8vurdWjc+I/cosfm+UzwWOmJXCeiBjXWW1hHWYPXILH3GSPpO5j7h5tHm1RzfkNKx5ZO425epwJaAk4GdRgRnpf0rikLfyBvc+Y1H2C4Xiv5DxhOM4rOZ/O8BxzdDme'
        b'2ZjZlv7A0Rdah2dHjkgjx1663rZ1RBpCLrtMPzOjZUaH9IFLCOnXXtq8omPxyLR5hLB1bPZsVrdxmn06Akdc55KRO7k2hzZHNeTrV4xZOzWrRqy9yVWH6c15Iw6zHzr4'
        b'jzj4d6SPOoTqYx7ZE1U9snYZk3o8lPqPSEmDNHTYJvRTB+dm22a7hrjmHfBQh0OHoo/T4TLiENrAeST16bAdlfp1aEekYcM2YV9NxHCYabMfukWMuEV8wXAcvR7N8Jzg'
        b'wd+vNSSY3PZcHsn8INI6RsR7x4wDR7KTycgtxvlk8sZ5gI7GzQxYY5xPwMG4WWamWleYmTkuyczMLlAqCnXFcOUfryFwUUwW/IzrSE0crJr4KtO1cozcOg8Of9vLPFPx'
        b'OZzZTxk4fGYlrd66VzLBFXAcHknsqud9xrc+kDwmsn4ksv/qiYAR2BiprzXEJ54U+jHdkkge+HEC6DlbpyUm4Ou4Hdfg6hRclxovYKyKeXPDHNh3DI5r0P7EJGgIKofw'
        b'W+vHYSTrufhyMeRORPaMwuWGPIFsmUKmsCsv2/gSJ/nxjTgjn4B9Lgv2KdRnAOgLc/kU4PMA4E/C9d18CvB5JgCfbwLleeV8A8B/4arp64efjXFeBPj0NUwThK8u2iZT'
        b'GDH5VPQ9FWm/gKTT/wHgVyu361RqFuYVK9UA+rexeNT4buhURJZqBGogiO8q6FG1TRmjVhepfSkzBbTkvBrHE3mJuCyWf3EQrwSxhkGxT7w4wld1QZB/bIEiT6Zi84/s'
        b'IrVaqSkuKswBwEoTAE1+ka4ghwBaFpvSTMSQfbwausaoyJCfI2XIihSy0ACtrhgQsAEPU60BkPchd/iTjuTfC8gKUnSLGfq6QiU++OJrmpGom7ypWZnkm+CPutLZlzbJ'
        b'hdSk+GRAbt2oUjJvAbqdrno22sDTJACji1lhJyNc3g9tbW+61nz7QCPHfJXza9GPkmtae9Z9aOHc1nSzSX5QFZE++1Dlm+3H2o/1N13QXzjUfiikVt7cfsij+c0wHhO0'
        b'0+JOma+c+5TsBKzFQ8USX7AlXIm7cDOuSdaxAY2ZgQb5+EpBwtMZcJv1GjSQGJgAwQzVkoiFBgAZQtRyRVf5hSvC5cJ/4lWEk5GJ+pNxCfsmMhuDTAkahJYwbBCKNWMc'
        b'3B87zRyetWzUKXrYJnrMZdZDl6ARl6A+0ZD3W+GjLnGVCfrlDZ4kNEndmtMbdg7beEDQ0Cd+SeaD9ZBm4yLjEh03Myw2NYERauJz1G5TJTVj/R8RlnV9HsT1mYr4kNxG'
        b'Sh5/Bd+3VcjheH5ft3dU6MVckATzdAuBUKBefPilykknPooOgJZrUJs/b2NiOKrbjnrRRXTXnNmMD8dxLHErql5P3d6cnTmSEisOw0mIh/QDd+NBBbvNuLREUrIdrqML'
        b'2VgPYHSXlJZbHPEptFcDbnYA77UO5TNcfJjjhA/gSnbb42gOuqUJVXMZTrZ/EYNu4OOlbPlJv3O3pKREyHDwLVikB0keMGQHnpvi2NZVKwy+Nw2dIUWaE5AcEdUuRftR'
        b'p6FKs2rNZJUGZDhIc45FqAK3+4FP54AgtzejOk40rsd7pzhukdGuipnnVRpw3AK9sU4jBgduniuadODCf6sD/+a7KjTU80ytz3yn+yKujtz+z+sc31F+IA//r1cfsguo'
        b'WBql9uV6wwsCEr0UZWfrwFMXZr8sqLHiELMyShYN4ERNPPlyiFjZ2iJ1mb+sWLe5QKXJB0aby+idhsgSrYTxKApe4rcMbDzQRDYFmRQd/XzCd3V0uq8//Fm+nPyJTl0V'
        b'An9BPN9loctoQ3S0r/9LHE3GpCjQFL2ybkIGSfVczFZLgGsOCSplxS8okPz+pXA9ybGo+OUoTX7/WqSeMnn/1nLNJIyajHLWKbHUlYHzqvN7McqVc/95kLPGl2mO/Kdd'
        b'pK4z5mWelTXtcPlitlLzRbQ948mI3rBisqZ5r/JlE+e1EIduoGryngc+QYo9eD8+we7/3kfHvSEf1yM9wyxz59pzxGgf6qOscuNJ0WdiEzc4q+CRRRoDGT15KXy6U3YY'
        b'eeX6ABPChHCT6DulZnggOozP7HFiQpnQQHyNPn9vvi0jY/bu4hRnWfzIcRV5nr5efh714d4wooErhAVqmUXrPzb4eDDZctyC7jErmZUxCsrEM0nCODBz54htsvy9Vr3B'
        b'pKs2iVP4mneh6UcBfrtXhlihYIurTRdVPqJKwYhYLCx/S/rVsmdJnx9bE3A0K8o/d8XCs2c8LQNEjr/1urXgzE+eLNrJ9E/b6plrI/xY+z+1jVfN7Mo2TGwa7fl8mjR9'
        b'KdK3n/n5oryspZz4Ktc/b/791/zYbybi7L/9z/NnfrMjNsztg4JdG7Z8pQj/SUngPI+L+zOqD74refbXvxQftrr/UfOxn9sfbUisOLKiya6gW31buyFgT4+S+4N3C1v+'
        b'8PaC334urOp77UbWvGXmEWuKfyVP77iceswxyLn+C7mIpunoNmouNeToaF8sTdM3oYNPSUSNLJ5phB3PIQfqnMuiDtRQ/pS86gTpML5OggMk66kBqDIIbgsgjySakTeQ'
        b'7oXgNmF8Ejr2lHy9hHvdN0sScY18kp8jqnBFrXyRDlc9JbFtNb6LL0Lyz2EKUQO3hBOFL1vTBnvpMpLxB6WCpJ55wnKu70zeU7LM/ObsnEzhlwTQJH5A+JR8N4W75zGJ'
        b'uDZxssyAz6Lr1sG8PDdcJxd/v7yd7EJMpu0sQBKzuRZEjp3PTyk4+pkBHL0B4EhKMlI7x+PyRnmTnz4aYNAjqcdj19nD3rGjriuGHVZMcHm2HmPuPg/d5464zx2yH3Vf'
        b'1LDiiRBgVXN2W9gDe+8xt5lnFrQsaNNcKmsvO7frgVsYZMqf2rs/tPccsfdsW/3AXk5TW7uGsOrS5tCq8rZZbYr22R3RZwOGePctblq8lfFgbiIRA24JqSxpdhmxntmW'
        b'3eHRntsnHpk9jz7s1BzWvL3Ntnlu245Lu9t3n9vzkVskW1v4CmbOeSZku7Yej9xkkO3aerDZ7gXbZUsYtEQcLeFhcw4cWSwnYYEbKcON8yAYvQrCfWdp5KWsluzgmaj3'
        b'j4whqSXAbp0ZhzPjS0hqZ3xfdNcilDOdknCenEOTWnxhKTqHq5PwAKo12d7yQyenfIc16VWzGDY5pd9h8XO5k99b8f5t31vlyblf/3iKg1/FBojvyK1yaWpEoYjpxtH/'
        b'djL6nRGK91KEErJ5GL6Jz2mnBCgr1Gv4YO4fRyh0Fe2nnxXMT7TS4CsR7Iu+DKryWsi+RDLgg26Da8FVybhmNdYnce1iUCc6iC6glhgb3IU65cxKGzN0He13UsW7egto'
        b'Orfx4fGT74dDMtc/JZnzHmm1IOlcVsSRP25m3h/c/P6l4LeTmBMfWEmVsaHHQ6rtV2d685JiwNtImHM/snI6f0MueEpeP4cE4g6uM3hWAbr1Uj6H7qJ+Wp/0w/24xqSA'
        b'ihodApjSp+4MfW3zRIlJDfUqaiMOjhRR0a1c9pbbqEpt4mxx10LW3/JF6KLPU7rur6NTlrhiTSJx3Cal1vUBcq6JYRKfZnR6ZnlKLXV5xhPq8OINDq9c9GI2+Lw2aVoo'
        b'fOwkG/aYM+o0d9hm7pj99If2XiP2Xm05o/Z+wxZ+apL0sr5EoCZ6eGUSSBL5rOcp4HziJ4wyOXMM6d9f9jJ/2ibicOy+h4P4kjiIRqEH0y7x5/1T++frmf8n9p8P9t81'
        b'xXxWFxeotJpJI2d3DsGSZeRqrlqRR3cCXzB4o9NQyMJfWTWZcrNPdGpGSvqqdf6y6LiY6MTVGcn+MuglMTM6dXmMvywqmrZnpmQkL4tZJf9+tk1h1bpoIfsBrvCbwmF3'
        b'CaMjs4Y7Z+Hb5NtbP/IpbGVSWhybiZI8FB+Wg4UO4MvmqKUM/o9HlWUMahWaI30gHqJfc0ASfkRKH59TbGAApk29uDvu4KOz+B5uV61elCrQkM99W9Pms+Y8r7qRw+s5'
        b'9NHGD1s/lFvIa1ZZXLOIsGhNUtbEPPb6MDhDntTdvvOk84KWLc6eb/b4r0kand+i+O0Wl63O1evyGpOzYptX4uZ36j7xetvilIr5KbL9y4/0cj4FVfiQK2r2m4sbTfY+'
        b'lKiTIiDAxGfDiFVOc50CgviiAjT4lO56ndm2AMZzZ77ptkQfukcb88pXJwLCCkdXgwJ8hIzYmYva0ZuoRc5/ZUglEzBpI+PmkCBqDAUdk3NqwZmsBU9sEjMOzpMm+3J9'
        b'nVruklGnpcM2S7+r0A73tLmPOgUP2wSP2TsfX9i4sGnxsIXH/5VdRxO7NhHWx9S0k8Xfz7TVC0jnHB1Bt3aoCjx9twrCPiwWVI3rg1AV6wNd9/DzGYtXm34OMX2+MfST'
        b'D7ANNel/r/mTksbGF2vSpgiAFm8LFdto8vyKwE9SZ/KKQLESLgBAmBqK41knUKDQaiETzlZAFJ/KlOIBRQ5b9n6pBjCF12Q94J+VA9j0//8fQCIyAJIz+Aj4EEAkK3Dn'
        b'i5/w/xNE0upI/d5PLFzIuxArf1yQteEH2gD2RQZ03zteU4ruT8KUVfgKfa9UiM/h89+FUxZ7TcKUUBFlPiCnTpX5xD/L4sulAYzqUdohgYb8gxhpcztP0jp0Z/N/J5uC'
        b'lySL1g9bi8vNV1934EU3ZnmvdgrjCZd2SIQDg2tDMohTrFlaVpL0F4fcZvHSZ8UoZt3Kx3jfr9zXxMvWSbR7nOZcVEVYiJ4V5zKMw6iTzvueXEgr1QtS8O2XU0aKalps'
        b'8ZUZ+PpT8qK9fdIKk4QxNYFsJeE68InJAmZO1qwUYfkcIU3tViy2mYQ/N8HRgR+VBtAt5NW2+LIJ/OmfY0Q/u3ez4Kc/McEE+6Ba1Gb0s7jX5uksEozQedyQ+LIEM9Bh'
        b'fm45btWiOvBT35mtED9lUi23oNADFjgxn51TKOpfdzGGern5CwiJ5G0LRq1ntIV+ZO1FNydDR6ShfQtGpUuGbZZ86i5/6B404h406h7SIBmTznwoDRiRBnTkPJCGPXb1'
        b'HPZaMOq6cNhh4SM3r7ato26hfSEjbhENIsoncEQa2FE6KiUgy8T3mo1LiCPNLFITqPSPszO21G6yK6BOJv54yvDmm3jkZ9vBI7t832ysSTiLOScJ5Ml5KSmxck6snJsS'
        b'qzr0YyuehnzlGj6EDz54tno0y9lsYs7nbQ9Xq9b/2Vcveebu88c3O/S7qvd9ubXxFwd8V75utuakwynH7Z8u+13QH2Z8fiMo+Q8bd+XtfBb/84W/3P3RB8qz4RffeRyy'
        b'6NeVZd7vrG2Zna74afMFecx7vIQ93Tb7t4XtaP+6NEg6+MO1kmzLNRZ//ltNEt9qq9fgyX2PjtoIvjnlYRYgVl7e6BGT+155y/ucRfmDvu3rIs5VHfudfdAfHIcvHR2S'
        b'upemVQ3IX1/+VHzk3Mz2NruMq64RV510V90Xj++NnS9J1kb+evhm84rfnGsJfGvZLVH153b+Fz7oO3X5rYRb5t2fu/Yk+zzOa/39DfcALS/yozUFZ0+GbS94e80ty08+'
        b't/r9+dt9J6//8L/dr47eHVvx7Nx+96Xei3y+tP4seNG+c2KvlkefO9dpdnO9P5efuphXfOx0tHRRveSq26KnZ0/97fAbP/8gdKfgtc8j5lkWt349kljUVi8cTi36xZqS'
        b'S58M4T9tfHyO53w+6vEl6+DlFSHLokvj8BfzZ56rz3n33dJlZzYfWRx9ZPG7Etemb1s9Ls0JuxYvWPyDkEPb7/zA785/uN1pVXsdHSr87Zt2acXnB35TMjLqsfyG7/Ll'
        b'lR2KJ2ce3yq4HLDZupvTGzynQPLJ6t9+qFs+/dkjwc8PftwQNhj6O97ORvOPd9onL+op+GXZndHAD+ff+4vjxdS/+45WHln015//PfJ9yxvtbh/H9n72pwVPFnet+3Ld'
        b'b/SzrtwKXdT4/r0/xQ1cH7/yi+hG17wnnwerkqUPv7j9i1mLPwu7l/X+/yTt+dEfJt4dHlrheKk75I1Tf3z9s5TtNz72/uZnv21t/d2KBxnBr8WPFLQ+WiIZ/OXpDX/W'
        b'lhel/PLJJ0+64/Y81Oc7Jfx6waiz9lenx7dlfPvXBItPbv2g4WzMt9xvPpa+I/0v8HPELDblrQLYwGE4c5egdgbX2aMKWnCKNgs3OB3cssQU2+3BrdTzoRp8D9VOukh0'
        b'ErW/kPwlzqOZGTqGelAfrvYvw2/G49oAISPcxJ2FDuBLbOLWjY/jar+EAKyP93ZLShEwEtTPxa2LsyjILFuM2xNJBh1A3oveh2viyQ1XuLgLHwiXT/t+r62IvuvwvV9+'
        b'eaWHIXqbjMhLyW/vlB/rXkWZmQVFipzMzJ2TZ9StOgkZ5huArbEcxtJxgm8mlhJ/Glq9o9mj6o0WTVtom6I94uTOjrQTe/o9+9RDHv26obT+0sHAt5e/Z4fjPgpNeuxM'
        b'MK6iJeKkuC1hxDmwTzriPHd4YcqINGV4VfpwxpqRVa99JH2NYFq7psJhG88JHuO8ljNhztg5NEQ1OuqXfSEUuprrrSYcGDuXMVvnMVu3J2Z8F3O95YRVMsfRfMzCZtjO'
        b'a4JHzj+1sGkImhCQ0wkhY2kLhBklRCwhpoQ5S0goYQHEsJ3PhCWlrCjlOWFNKRtDmy2l7NjH7CnhQJsCJhwp5UQprwkppZzZG10o4coSbpSYZrhvOqXcDdQMSsnYGz0o'
        b'MZOV48ksSnmyTV6UmE2b5BPelPIxyCGnlK9BfD9K+RuoAEoFGp4LolSwoS2EUqFsB2GUCGeJCEpEGu6bQ6m5BonnUWo+e+MCSixkiUWUWGyQagmllnIMTKI4lF7GMbCJ'
        b'ZunlBvqLGJaO5RhEXcHScUY6nqUTjM8nsnQSh+07mSVTDGQqS640kGksucpArmbJdAOZwZJrDORrLLnWQK5jyfUG8nWW3GCUayNLbzI0Z7JkllFMBUtvNtLZLJ1jfFzJ'
        b'0rlGNeSxdD5Lh0yoWHqLgf1WliwwanUbSxcamotYsthAbmdJtYHUsKTW2LeOpUsMzTtYstRAlrHkTqPku1j6DUPzbpYs5ximew9LL+Uabo/isvPNNUgazdLLje0xLB3L'
        b'Nc43S8cZ6CfxLJ3AZexnjtl5jdnJ6dHD+J/XF+voHXrxxAYu4+Z5Jqgl6KeufpUJ+ugGxzFnr4fOfiPOfj91DmjkN3AaQsacp5+xbLFsU3TYjjr7NQrA07gEfuoQ2Oc4'
        b'4hCpjxmbPuPM+pb1HYLR6YH6+IbsqpQJMePmDz7B3OaR2KYhu1nTEd2X80C84Bl3kTj8CQOHL3mM+UJysJngA0lUQW9untWm6eM/EEf8iWsrdiY3RBruAhJMWOpyfEvj'
        b'lmGP9FGnDL3kU7E16WB126yO5X2OfbqhNW/FvOc17LfygTjtGXe22PkJM5vlsopjYAM0WdkGyR6IXZ9yLcT+pNHNcAeQ4G9Mb7ASzzS9AUhwOqy4qx+IPf7MtRPPI230'
        b'LpsnfCC/msgWccTxnEd2M85bDAfEjspWjNrFDVvEfU3fkquMco73YH7oYR8fbtidsBnnZmb+q1sS/0r8snmOkKfGLHUGgcqT4YqkHJrFBpgczeFwbJ4xcHhCDt8XMLcK'
        b'A5heyVye6qn7EE/zA7jS/1nSSd9Pfvzgx49/HNrqcTDkoEdF+7H2Qx7VLRzekb631na7eGgDsv9wzjLbacHF9x1me15Lsjlhu3l+ojTRPHqmn/eBd3/6zuMfnnqnXoW2'
        b'+LS+Z341yqb69aHhn6H3mPB45+rXm9PS9b+43r1WlH98rpP9WpvZxaHaYF1fSZ+uWCsqCd4h0ulL4kr6tO9p39O9d+nJxb5rxdoQXaggzCfsSNxbT7uDHSo5u38y/E7N'
        b'z4LkPaIvZ7nstPjAxbd5lsv7LvNGOR61vqMXLsotaeoGSfQhSLTJP+jnEZWK6+lOogQNcHGHF+6ib+fiNjxUTjLkfrgplewI4uv4kC2+w0Pt+DCuoiDIE1/ZtouDqlE9'
        b'+TaphnwzWG/GWNnx3Beg43RLMRP1hCTGJ1tF+iabMUI+V4SuLKcNVugWuuWXIGBCkZ6TyODmxajqKfl2cI+7/4t756guKBEQXB2kkPU8Bp14fQXqN0P1aWg/TYlxMz7l'
        b'YHgG7UNHJp8TMtLlfN/duJa+vAUCrk9MDc4gG6gm7NzQST66qAyh2wGlb1iQOmcirjZjUN1mfgAH9XK3UuAZL4AnWqEfOTAAlVWmQsyxTuNlzMFt7KbDJbh60djuD0Jv'
        b'28hWSzmMDF8TkK2APlb9l0pxr1+qP25Cg7iKdgjqx/e4+AY+5k/Vn1BOP9StsUCVADCDfLcbEKyrjo8OzcRn5DO/Gz7+W0Djv/GgmUnx50uw84XfJApVFaq0LAplzygK'
        b'vcfQDckvXRmB/Zilw0NL9xFL91Olo5Y+e2PH+OYVSW8mDdt6nJ/7gO//Cd8SkJ+r+zDfaYJrLljP+UTkAoDP3efh9LCR6WGj0yOGRa5jIqt6SaXkgcPsByLvMZHdQ5Hb'
        b'iMitOeqByH3M2uWh9ewR69kPrH3GLOzqUypTht3Wfmyx7plwK18w7xlDjhPscb2YsXDYm/rV0+1wIv2C4QqCxxxd9OYG9sMOgT8VARqFy4bXl/nLfBnkOy1azMMiDhxZ'
        b'lzljnFegLBznkxdmxgV0F2GcX6DSaMf5OapsOBYVQzNPo1WPCzaXaZWacf7moqKCcZ6qUDsuyAX3B3/UisI8eFpVWKzTjvOy89XjvCJ1zrgwV1WgVQKxTVE8ztupKh4X'
        b'KDTZKtU4L19ZCrcAe3OVRlWo0SoKs5XjQlpizKbvCCqLtZpx221FOfPmZLL7wzmqPJV2XKLJV+VqM5Wk9DduqSvMzleoCpU5mcrS7HFxZqZGqSWvWI8LdYU6jTLneSjQ'
        b'EDvM+kc/mYx17DnGA/mHKTWpcPj222/JW9a2HE4+j7j1qccJevw+Tp7ErrfNhFFS5m2pJGom72uR8fOAcZvMTMO5IbB87Zo79d+blRUWaWWkTZmTIheRN8xzirJhxHCi'
        b'KCiA6JdjWMukegPXzUG5aq1mh0qbPy4sKMpWFGjGLUwLqOr9jKF4xJaRWFtYyP57tovV1QwpXxt2ASd4ENqecPkcPmQuEsu9Zl8IY2HAE6vMGbGtYR0nwKoe9l/89mzs'
        b'M+KfMCayeWTuNCwNGzUPH+aHP2JsGpw/ZlxpV/8Hfqbqcw=='
    ))))
