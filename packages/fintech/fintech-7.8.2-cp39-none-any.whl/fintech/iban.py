
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
        b'eJzNfAlclOe19zsrywCCouIWx51hE8F9FwRBNvctKgwwwCgwMAvuRgUddhAFF0RAFAVkERBFQZNzknRLv7Zf8t3mR5f0pl+btsltbprm3rbpvb3ned4BBsEk/b7+fvfC'
        b'b94Z3mc/zzn/8z/neYdfCi/8yOi1nl6m1XRJFvYJqcI+SbIkWZon7JPqZHXyZFm9xDg3Wa5T5Ao5gingValOmazIlZyT6Bx00lyJREhWbhecUjUOf0lxjgzZEKvOMCRb'
        b'0nVqQ4ranKZTbzlmTjNkqsP1mWZdUpo6S5t0WJuqC3B23pGmNw3WTdal6DN1JnWKJTPJrDdkmtRmgzopTZd0WK3NTFYnGXVas07NejcFOCdNt5v/THrNoJeKrSGLLlbB'
        b'KrFKrTKr3KqwKq0OVkerk9XZqrK6WF2tbtZxVnerh3W8dYLV0zrROsk62eplnWKdap1mnZ4yg6/b8dSMfCFXOPXK8fEnZ+QKu4WTr+QKEuH0jNOvbLf7HEjSonWnaWSx'
        b'SfYCldLLlV4T2ITkXKjbBY1zbLojfb4RKRUuz3eiTwl+xf7HBcsc+rgN7s3AIiyIi96K+VgSp8GSyJ3z12zxVwoLwuT4fApUW5ZSPayFanhCNUvhznEs86UWWBoRg6W7'
        b'qFnRwq0RflFYjMWR0VgYqRByoMxpPxYf4+Mu0zsIyakkK3WCX9bcCYLlAOvvbAbexS4n160R1Glx5M4IaPXGfL/NMXhxuyMWROykfktHDOQdEY2lsdFxO72pIH8hTXRr'
        b'xOad3v4RkX6yBAk0ywUzFExc6od9SZIXlMxtUCbbvmaTUtxs2yDJl9I2SGkbJHwbpFz0ktPS7XafX7YNTMYxo7YhXdyGZ0eUgosgbKn0SXBx2xAv8Ju7LFKBKnr5uCZE'
        b'fyJMFG82yxwFd0HIijyc4PI4JEi8OTNQLtB71mfrE6K9NkYITUK6M91+lD5F/sfxwvq66X9d8Adpz6LSpesk6Wwes5OvSTocBHXglIAMCFrmlCzw2+8t+3zc5XES738V'
        b'amf9cU96gEQYECyBVAAt2AultCe0qd7eWLgwwj8Ae7EQmnZ40+aU+QVE+m+OkQiZ45zWYBvWaxZaJvH9xOfQiw+cTS4kfLwqQJUfdPGiTdiBj/DhIZNRQSVFAuRjFfTx'
        b'opPYj2egCupNRgcqKxGgEJ8KFk8qCp6DFROw2YQ9rPdyAYoPmywT6bM7Nu7BDkcTlJLAsF6AmlTssTBRHzfALR8zFZAZ4C0Bbp46xO+nbz+Bt0+bstnwZWyIuyv46NBP'
        b'mrQt0YQPlFRSKUA5Tc3Ki44egBK4CfkmC2t0UYAi7IYC3hs+TMXHmw6YXFmjWgGuHZ3I5+WU7a+BQhN2sWldYZ31YAkvwTvZJL0EExSzP24IcB27jlgmsxm0Yg92Qh0+'
        b'NanYpOuou61wmY8zD7oj92eZjpD+YpVAW3J7idjbWbyTMBvvm8YJYour2LmSl1jw4VFPrMEuVzaFVgFq4YmLuDtt8FQGNxer+Ba0UBuoxhZepIMS2saqWVBEGydxFKAN'
        b'n+ItcXY36Y8ObNxhwk62qRUClEHbJD5WaCCe16/ALotMlPVl6qSVlyy0YDUUy1XYwcZqZ73kKviW4mUa9XLIGtMRqdhboZuBN9EcUkAB9pjwEZv4NQEuQs0BLgS4gxeO'
        b'Sraaxtm29Prp13iLeJpkxzR8gF2OrOS2QDAVI4rnksEda52pgA1/l4ZPgvN8+IXCri0J2GVWiGOU4QMqYE1UqVjhCJ3Y5aIUm9TEYi4XTiI20uY8MFARE8A96i0W73Hh'
        b'OEMtngnCh9iFD9isG0jj58AlUdwtUOkLZ3MI31izNgHq8dY+sagGzuKN+dBAZTb53Npmm3kNlsyP9qACJtMOARo2w33eaO5+aMQ6mkmXxaZ0FzeQzvM9OpOC9eOwmTZd'
        b'Ira6he3YzZupF+NduAvPaYpdrLCZpLRnFh8LzuTsPezGChxEVbmpw6dcSnB18Xq85kXbZ5t6zbLp4vTuxuDlrXhb5cgKemhrvKHEMoWV3Cbv0ERrbFFhJ+vvIZvFE7gh'
        b'WtkVLHgNb8MjVY5CHOsatB/nXS7ZeZgsrkSFPUyCD2isI1jPl7Ude6fhFXxCRWzFXaTL2Ay9oghvY4crFO2mMoU4WH0SNHB1eTVwCbZ4mcxshvkCXHDB57y7SfCUvE0t'
        b'dKsYHDOhX4UGasPXdQ6rs7EaG1TObKheARoPnLJM5/o/3gOKlmI5PIRimmirQpDhLUkcdGAVXzi0WrAAinJIsUugMO6YQpCnSeBsgszCmMGc/ST+opxZ2MTKg8RuFIIT'
        b'lEgnu8FZjcwynvXRESPBIhk8OSgIBsGALZEWD2bLO6EnSo4Fh0gJhcRkvMArY/EyvBSlhAtbmU9Jxpb1lvkM42OxFS9hPrQsha610KTQxpBV3z4UCg37YoTFJgVULoYH'
        b'Fh82XDF2YvereHmwfhtW0h/s42KC/kq5MB1L5E7weJxlAVX3XLI+9IhYFXrgHqsbAW1DVaFfLoPL0G3RsK57oS5tMWmxredWu57viz1XyJUH4YrFm8O4lZSknAz8UgTc'
        b'XwpNQ7WD2DhU21+Gj0/kiF0Xw5PYoRnz5UHfIZUai+DeLtKHOxOEzWoH1TadJYBJqcNp7+jlQTuWsLdmrCSVLJQL/kZFNjausvhTkyi8s3poIiWyRHEAstLrJMZofygi'
        b'OUbgYyXZ+50MTpwORh8ZbAD9eGNQMvJtwjTskpGG4hXLCoY6+OQ1OwGWDEqmF+8MSedeDOvnfowyMUbIhnZH6D2Cly2+1Hpp3EI2StuQfGRQgQW0ggsppE3XtduERVir'
        b'IOdwwcSlis+WQ8l8uDtiD8QdaxZ37JIM+yb58M2Vm9evPjaWHjSJu2WVO1CrZssiqruXih8O1y2Bh4TyIwfgKrH4hILsuxbbLQuZR4byuYONqFPodRrcjBYuicXiVgdh'
        b'mQLqLJP5XuvhDlw9BedGat2gpMSZtcodt0TyeZEcG/Gq3RhiVWp2X5Q1aZ4JW2i3oVBhOkF44MdBzoTlg42aWSOC1GNMrHBBDbd2wbVTE4QY7HcImrOKN5Bj89GhQRSx'
        b'0GNTQczd571UnJUJah2x2A0KuQ5KsXvnYIOWUTpIk5oOZ9ikqhSm2YTy3DQrIG/B0MYpFuGVQTMOVeMlUvQJQhzedAhwj+QjZHj5DGvsiGFsMrtHNCAAnioO0VKruXYc'
        b'h0f4REeAJ7ZrHmX6C2T4dBYWc+1Aq8LjdLy9dYrb3MpqTsMeGXnfXqjk5rNXgoV2ypFFWN0yopGoG9kKuBp7gEMW9vvswHtz7ZWbfRq0fZkM29XExTQcoOFiHFgPDA7Q'
        b'PlofGuQO2OUuBirdYCXPYaep9nqxVA6dLjEbiIFd2wit8wUjVjpiuZ+Frxi69MTaWiF3FNKEqhXCYqhTEKOqmcb1Lg77DtuJ/ymcfdGIuL0FY7WCLPYu3OL2MB3O+wzr'
        b'asmQ9vE7C7FPRrNzPbREslXhsNwHe7ls4YEHPIniAEFVbcoxBPAPN3GM3wYlDrOg9zUusDRXIjcjwYzXJRDDm+T8guEhQUY45lnmcWzVzVxnfnGfg8T5E8Windg5j0Pe'
        b'/Cj/YbleSbKDvOlwjjRHBvW8R699x6TqESZpv7VgleGTRb68Jj73IGc6BKNEjWyVpQxGH5GKQf9EEdg6ZOSxq/HWaIVsEyfaQRM9spsr1+ZZxJaql9qUq3mwKnQPa1f3'
        b'cl9LEFt9PVzCBjsQhI6VQ1vYNrRFcsLZ6wq4ic9CxCjpLlbgOftmlZLB+dyzb7VbAeVmbOBgHgfPqNWQgS/A8kH1GjLwLdEOK6APrnIL35ZkslOxpvAReDu4mGB4rqDt'
        b'rk0S53WH6haOwAVpkm0Qdxrj8dI1aR6Qv0QC1eudY1Onc9nOycaLcAVqRnniQfvSyPBRMNE57lyt8CxiFN4OAjrX0bMehGwWRRbc9uD9m0laz7A+dfTWtYhb1yujIKgz'
        b'VLT2ergyNTtwTPS38ZPncrcdRN6YyUYlYCleGoVSQSLhmIZtMmzbBaUiiXg6LnwYw7fivdHS93NYhk/CRBfRBXlYj1XYN8JPjNAjpsrPSYc5IqzFCxQljil56NqHJZg3'
        b'U3MIG/YJxsPk4KOJHjDrJt27uXhMLqYYzzw8Vm0k1btP7hEK5vMN2JNIZPVFijXMLWiWoXiXuZZLCrPnbq4VWCaDVrtBvFLtXL29itczhHu8mWMVUVtyrUNrL3lxgm1Q'
        b'nqTIXiLZ4uiwVEoOxpdTQHxErxfJB9xXJJIMYqBzsRA0WQHFU0nDuY/JjXSFpsQRjtImYZExQqdcvieDG3WGEjv8NowlqlZRLQrljs4BvOpc+Wo8YxlDnUUFWiXD/j00'
        b'Yy6aS9AeaKfOTvR5WPntZXNJATeWTdREW7xYsyZa6DOSkHU42MArcJMHKOPhBnHSIigy8VizQCCP1JrOoysp5uZg/SwTdkvErEbppkzeJolg6AwZYeNw/mQhNPMARboc'
        b'6hxnmKCYRbo3BbhBe9TBwx0JQUW/JMhkZEGNVYC8LYfFkKaIopXmPf7DGRco1YpxX5sL1uxaMpxuIZVtFEvuQKPTnIkU6rMOSlnG49leHnSsIuaUssTkLBXnVbnEg894'
        b'C+ZinQTyTVAoF4NSmphFjNAuwMUJcHepXfLmFDznnUW5SbA6y+TGOrtOi5Qe4i2W4X2oOXrULqlDnuqhGD/e2UbO9TJ02CV2gj3FhELeog2zoXQ4s7OffCYreJWlVaRx'
        b'dpmdV73EcPkWC4kXQx4VOYh5gMvziGewRr4EUjd8Vg6nfBZAtZjrOE1yasP+4ZTPVLgozq1t9mtwdp990ucSuXougzLyuo9SLCYxxK6htR6GIr5tcq/4HKgazvhMgxZx'
        b'OZVzsA57A4bzIyu3iH1VYR7mzsdm0xGFuJ6SCUQa2dymbsgitb1tlzo5SBvKGinxevJsaKISiZh1ugydhIQ8q2I9GB6KV4ezKkkqcQJNIVA0mdqMk4hJlRvBm8SCRwmx'
        b'WHbCLtviJYgzK/Zei9YYu2wLtmGHWPTkBN5fBpftMi7Qu5xP+jicjdqGF7BLNAOSQVVAOi85cAKv6DOwy4Wt5g6Nw6Jmceeew2Oo9Mi2y9LgY8y3hfBroCcy0S5LEwTX'
        b'xUnUbvLa4UwD8bwEdXgdnuBdXiSBxkio1WCXm4OYEmiAShBzYrviqEU79GGXqHKdAjTu2cyLFmDTNHi2CruypaJUy6iq2Ap7pyzfRODRla0UN7wcrxMjYkUHog5g2R77'
        b'VBGUQhcX7QYznNkClXapItUW0SALKeB64JVllyhymcW3b1tyst94uzQRtu4XxfDs8AHsP2KXJYJHr/Hx3eBMNt6gHrssNoFXzMGrfPwtJrwJBfOoRCFa3qWdk7nAY/A8'
        b'PN9FkNmFD20Sv+YAl8W55R5Nhcu0T65ScdJ1WdDD7Xu653FVtl0yapun2KAUz4TsPkAFCjHT04CNr4j7esEJOyKwwz5JBV1zeKs0rFy0jRTKLk01KZQvaLsBrhEGW1XY'
        b'oRRLbuCz06JNXoX+Zdk5dgksUrw6LriNXseo80sqR6WYN7o9aSGf9ET3jXB5wnBia6tU1PrW9dA1L1VltinjpWB8JM65xInwqg8f2OW7ggj8+Uo7CBfPZPoMZ5OwUsxZ'
        b'mohO3JmM+aoc1l8TISlc2SLmgOrcjk+dpsphLVoEuJK1mU/X9zTe98Lzw3mzw+G8o80ZUiwKt8uakefI4yWECnDZeMo+a9Zjy3U37Cd1Oq+xS5rhhd18GH2ilzs+Vbmx'
        b'1fcJcC8ZK3hnW01wfTEWqNyYnj0ToJkQ5Kro/doXkTlexzwVPrDJrB768bZY+Bwv4lMiPqVUypo+psHXQbtoI/nYO5F2qEblJBWHuwvdTjzjtdJ/no9BZbGlrq94Smyu'
        b'BO+exmeRdom7TqwT1b1AeYzWe0Zlsu3BTS1W8o0b574GOzeSB+PK0U8bPX2qZTEHCizdwlga5OckkAR43g5abdwO8nmuTw5dO6Bop7D7gBJrt5s0cp7r0xHPxqLozVgc'
        b'hgUyQYbPJBydurgM50PNa1FuAhZGKwXpQclCvBhtmcb0FDpOR2HpQixZBzW+GnZI5eIum0h098wgcmX6xvpHQOFcuSBfL4HmVfg4PImdGQ3+0BL4gRI/TIoQ+PkVO7di'
        b'Z1js7EpmdUpxsp1ayfPlucIpxfHxJ+X81ErBT6rkpxXb7T4HCskyfmol/+d/pU1wVtv9hLJjT5Nam8nPO9UpBqM6R5uuT9abjwWMqDjij0jxtNXnsCHTbOAnpz6DZ61q'
        b'PfWWo9WnaxPTdX68w006Y4ZtABNrN6KrRG3mYXWSIVnHz15Zr7w/kyVj8ExXm5RksGSa1ZmWjESdUa012qroktVa04i+jujS0wOcR9xamaU1ajPUehpmpXpHmnisy857'
        b'E4d6CRirQaI+aSVbZqo+R5fpJ7ZiEwyJDB0xA33mqBWxnyQSjO6omS1Bp01KUxuoknHMgfjajMfsBzMPTpNE+c3HMbMTbltvAeoYi8nM1sjkvj3OP3jR0qXqDdFbIjao'
        b'g8boJFk35txMuiwtn5gP++Sj1pFqWLRmHT8wT0jYYbToEhJGzHd037b5ixLnqmVbi3q7PjM1XacOsxgN6i3aYxm6TLNJvcGo074wF6PObDFmmlYOjag2ZA4pqR/dDdem'
        b'm/htJuQjetMLixl1YO4ovHhS6xEbLoLmmfBU7IHOYYJJoF/Oj2Gd9k6J+KE0QRASEvbfTz8tcBzfDHnroIg+7CU3sGYv3vPjdc+sdg5UyCgSdk9wico22g53fcbtmiNb'
        b'LgiBCdFn43WC6FieUhhQNh0LhskhIWuzZpyNH56aOxV7h8uw3ZOjzxLI1UZB+fBZoc8xETxb8aIRzo04K8x34sATAJelUBRmd1Y4k8ghd2C1HlhKGNk3fFi45oDY3Tno'
        b'lFDc81CVJRN51hWsT+ONwnPgRjR2qbJtnKSaeMNTcUlX4Z4zthBQDx8wXiOKOpljahuxkqr92GVSiuSjAhuJJLMeo+OgCh/42R89PtLxVniRSh5Cf5bd6eNqaBLLKvCi'
        b'mZbdZXf8iFUiB8Hre6HSuEDFpdTDziW7KQjnJXVY4LhqKnbxFVezcAHOcZFrglQh+Nx0xEGk92X4BKq4yNctnoyt0D5M1ZN1GpnY2aMQvJIOrcNF8EiM8SAPq11ogY/s'
        b'BtoaZTs+30f7lAf9dkPdmcKnsA3yU9Yftw8xCqM0Uj6U1z6sj8EOu7JDIDLicGzymjzJ7sQZrHCG653e18FFK3ixpzFcvrc2Rzxsp1C2dokG+4MDqSO4JCRiwSK9e8oy'
        b'uYkRucSna9aUL4qVbXAJ+5fP3smUJquue29z9vFxjl0ftuF5hMeM876zwxLDQ5w3T5VWvPsrx6eu3/qF140zcza+9354QeODD2o/NexNnBLYo36Q+0rPVvVzp6OuFUG+'
        b'm9zWpJzuL39PUbCmOTZ6+peBd08uk33+g1+s2GRZ/dav5pzrd/joxx1pG2eEVG/pXLD1R/LY/afynNIjvf/mfGz2sX2t+tqQ1Uff+GtS6Vsln9f/YeGvFmw6/du/7vjz'
        b'oz90zTEUq77Y03dl5afn3/z1vxyo3dyPJwMunt3Uc14f/p8Ls+t6quW72/Y7hUz4TcXPElx939f2Wm7+8Vv9B+8GvbVgrrI2Kunj8Bv3p+HUO/v+Wdl7zTrJa5/Xs79J'
        b'VhX8xDvlVZWXxsHMNiwZbs/2nYPn/L0j/KWCEq5L/SE32/wKlzd0uVAoX+YbEOnnownAMj8soM1Syw8egSYzowULoRieRcX5Q0EcpwyqrRkUr5LZlcaaGYcKxn6iJEWx'
        b'Uizw8Q+QUP/npMFQG2xmSZPsELhLlFh8OOYIWjeKz8fk+Ptg4UIpWXa/Arv3ufCOyE6KorGIqHxvjF8khfWCcrHU7cRK82zO4sNVUBcQJbYnil7G6I1MmIh5MoqtLmC1'
        b'Rjog9dYwZRU0TvztG18Ysv5l4uoUo+G4LlOdIj6BFcAc79oBZ+4G4tkfrJppF4Pi1wSNXCKXOPKXm0QqmSRxpndn+mX3Xfh9Z4mjVMmukuErK1NKvPg7+8uN/pKzEul0'
        b'CctzCLF8MhrlgJyNOCAjZz7gYHONA3LmywYc4uONlsz4+AFVfHxSuk6bacmKj9cov3qNGrmRETMje/7GyGzLyB4EMzLCxsetYmtjGiGcET6ZTvOWSpT8Kv2rVEpkTCL8'
        b'J/vLMottVAk2+Llue8leBGIJoQvTnNnQClVRm2cew2LSDyyNi1QIblmy5Vi8mZf7S+Kjouk+1uI1Yp2+EkG1T4pt0G+LELAPmrA/KnnVEFUNg9tJMjuXyFbmMOgS1wpD'
        b'z0vJU+Q2linLlxHLlBPLlHGWKefMUnZavt3us41l5hHLfF/yIsvkj9TZ0UyjIUOtHSSGIyngSLr3Ap3b8RWs06jLtuiNItfI0hmJeWaIpGjwOb+RtCBukC3QRHy20Yj6'
        b'DF2Y0Wgw+vDOtFSSPDaZZPNl0xUJ5YuLGJNJ2RYltnhxhWMNwehneLo2Va0XSXCSwWjUmbIMmcnEmjgLNaUZLOnJjFWJBInTYRsFHps/henZkofpGlFzrTrI32zJIhpm'
        b'I2VcasQmvVkNPzaQ5mvYlGIUm1LEWlbS5z3SDPb44NAjfetibU8PFkT7bPaD5h3ig4TsRlx0ZIxEgBYoUK1QQccOvevMWRLTGupE/vHtjxMCfq3RRmjTv69JSU/8JOHg'
        b'6++/8f4b5dBdvuJCU1V91YPcpoiWC/UXFpVortZfmHX1bLCr4Oegatj/XCPlsBdxaIbKh0wDC7A4xuJPUVyJiJwzoUuO7WCNMHOLzMeyI1EBmwk3oYSb4421zCKnQrc8'
        b'E/KxTSMdAQUvA0GOBwMq8THSYcxzEzEvmaHaeI5txnHDWKUYcBxUqwEHm4KIYOPCLuwZzxHDy4wshDa6s4vTEAixDn9sB0It418OQuyJFWKU3Xv5kvF20OCqB5ccreXb'
        b'mL5+vC2AHo6e2dF+HnSSU6vzkx2IWnyUuGQ2AVUj9DsTl6hwxRosFR/1gqq0eSqoichxo6GJq2JLKojh/EwtFqigZ1ZONivJJzd6Ap9xcpQKV8aZsGdckAMWyAUpVkgm'
        b'ORA/Ex/hw440E17zDyK5SQwCcasaIp4c6W54Lletcs/JUVJ354n9kUO7SCjK+I5cjr1R0Hh4CAT3EeucIVK0MswTI3aogwfDITv0yEWGWYt38IxvcCqBrESQQqkkFG/h'
        b's1EQOhRVhDMIlXEQFR83lVodUxyHoFT+jaGUBez/8bKAnWPAyHD9pUDCQIdV//qw9yXRKGv83x6MJqXzaZl05tHh5wsTZHIxJCVZCDMzk0ZPdDAADduyQR1Kzt/IMHUj'
        b'+Y4ks8FIIWWWJTFdb0qjjhKP8Zo2jA+lENWoTR/VXwhZboDd3LRsUyz8oXSf7aE7fPzobeNG9hYat20RvdP0fEKCQnhBaKiP36ge7dZEwa1hzDCaLZLLOUsMnqnXZAbv'
        b'x7JeECD7+UaOc6hHQ9Zof8l+vpnPHLF5/9DoXSKMFb2Po+h9NUczN7w/wuV8pcNRTB50OXJs5aHSBfkUIZAC9MAs83TPDSli3N7iMF6Yy0c/fvJKxlox8CekazoGRccY'
        b'7uwV9i6HWjH2bca7QLE05EM+eUcdtk+QOKUoeT/vSNyE6RQVJCw7Gh3gqiY451nQpNPJwZiLTfRxkbDIHdv4XWjPwr7gV6NpjUFCEPaJeYUfZ7sLakFY3pF90sW4KnKw'
        b'i1nwGDqD006JXSzGcjF5UH4SiilsaMBCYndbhC1QPYn30papEqiCY0JAtt9d16nCDr3pz6gwPaQi3a7KeaWL3M6tdw/7m9/3pIfup/9m9bnUf3X2fLs0cbxqfOGBxFs/'
        b'Ck8M+rfpCb/1X+1oNU4O+v6Xn38U96z8e9d8HI8V/6nc69WinC9L93zxx1tf7upO9NwdMmdNdsjTd39T8ZOL7h8VX129fvyiii+++0/jjvq/fXdOuPGLv07++Zvdh1Mr'
        b'nb94M7LhE/WbT+R3VV8WxzyeWhVwQ7HgOZySTT67e/f7H3yiWXX+Z9e7HvnkFrZWvxn7o1/GnP/wDw5vfLGkwt1P42hmsg+D+1N8/fHiIrsArRAbxMDnvGIEBbC5fw8W'
        b'uRED8IXbZrbFDvoJvoTyFKSxSG0hVfJnDaKizA7CIqxTRmLdejP3m8UKyFVFYTFJuFEz1OFEsModsU9jZiqyHLqwnUI+8hlr9uZINsSsMfNnZ2tJ59rYNzDwpnJhHJvq'
        b'aakPngnk4RucDcYmLIpZCO3D0Ru2njRPpUJ3Q1LUQbyBJVFDMea4QFlqCtzSSERW4Ph3RWsiUXESYzNyFJymBIo05TXymbbgjF2lFGS58HDMTSKXsqBrNr28bC/jBDsi'
        b'MxwiDcgIs+34y9dFVzK76MpziNOwvn9vx2kuT305p1EzEV45HipGVZ1wlkVWYsTtgVYZ7db5dRoJZwvpc5eL2f216YPJfQfvUd8jGYqLGBMily5NkQ59X0Tyjb4vwhx5'
        b'ikb+l/81AtW2iaj4Emqfwpk597/2yfP/7ljopbA8KK2RsKyMtTAGD0VhRDNfhsoB+PylkUAaXBIp5AMLtvOULLSFiFnZglT+BKV3JjSSiWFhDBZvx/xo6fgwaFpjgfNw'
        b'B67RR42wxd0BeqDsuP5nAaEy0yo2Sa/ajxP8xIiCxxN7Xn9cXn9JEhF8J9A/2W+XrzZWu6JK+b3AgITfJuz5ttc7r19zE7bPd1V+OlGjMLPH4tzxAZaOghMZ1tkCCgP2'
        b'cERa7bTCdyhdhI2Yx1JG0G7mj5pXQV7cC/kijatafhAqvHnGyCP+OAMYO3A5MovDi3UNBwOono7NQxmliVDPkkpSLF28TLRD6ZjG7pCqMw+Zuvugqc9iJs5zLRLjpCFT'
        b'bpKJOY4xA5AmiVjITZS18SLTMalFEz0j/M7t5UYqPmlPGnGfTx+ehAzmxGj6idj0NUYotQr/z0bYPEKHt2el682mIUsTjzDInNTsbopRm8qPJF6wukHL1aoXjxk5j6js'
        b'HRq3M3bHtr1+6tCIsNCo7TtjKKTeEBsVHxq3McxPvSGUl8fH7owJCdum+eo4eywD4/788hQHIT18KkvwpkesdxZ41IZ90G8gGT+ZjMW+7Jt6BdFbI3iUwyMcrNBAkzNc'
        b'O0avSCg4JkCN0plYSx0RGfZAFTynHapgX9QbbEzWtTkTL7Ho8BW8J4dbEdinl/yfeIVpC9VvLP1s4nceuJ5Re4b96Ei9UX78owSn3Wq3urd/925a9LNXX29MPFH67ntf'
        b'fOg58Wb5Dp2xJv3zDU7LJq+d26S4u33Rv62e/59J3e8/TNvXWbOueJJHV9psjVx0h21QiXW+/qnYM+zVx2ETN6HAlXEqExSPNBJmIlGYz1O2rxyGi+RLvaFw2Je+MpFb'
        b'Dz5bjdYo7uFPwFVvpeDkJYV6eECQYR9lj21EzhSQmOwie89BO1rkyJ0ky2by+H7qkC0ZJ7/YndeQ9bBa3iOsZ+ArrIcFrbQjLanHj/hG+PnEDgftk+CpfOLWPRoxvwh3'
        b'VnmIDg6KVhKnKFsIhaKdTX1NnoaVXi83M1sOkH9jcigH+PeYWioFrgdezAHauzyeLMvUZvAQaQxPxwIkdi6YpaMb5BFH+p5I0eDStWYzxTtJWnJbIzvlDlCbLKYZR0V6'
        b'I/oaivq+LugTg7z/qR5YMiZAOMZa2F7CFSd49JVxUR970HwsFxwLBRxj2j2mCI+1Kez0c3V02FLxEOlQKBbYTkrTMZe55XYzd8tYu8dp0C3LoXnIM7/ol9U7eefzVimF'
        b'HRFTGIBFfzbxiKC/6eKnMO2lkouX3/o4Yd6b9t76dwlpKdHa76b4bftdwv7X33+jo3zR1fpcreTdkAux7t+/AX3lD95vzJt3XnH/5pT7N3dW1FdJ7t18qLy/9jzLDMqE'
        b'P34wyWHPmxolJ/xQgc+xd8iVGyBvODgQc4NXQsz8afRq7FTaxQZxm7F7NsvIYynhT4xCWBarPA2XZopnMA/wDBYOu34p3MYWf8f93K9nYk3Ai+dE2XhefnC/gh8mabdg'
        b'pepFTCMqe0vuOA6fcv5BG9kQE2WbRpPefhozoUKONS5LBgOCr8tSunA+QJrN7IaD2aRBMAtjEOYicZaKxMBFYpw+BGca2YCKwV+8wcjYhB1FGHNAms2MIbhjvawcAXff'
        b'/oosJdslLDzuObhcca3wEG7YrReqFmpksbHhGkm4Rhobrl//p7UKE3vSsOVH83eW742bsNXzW5/2Bx9o9P9hiP8vnn3qXPh0T/OHpV5hCs/u3/1gQ0jIrX/7zjt9eyqu'
        b'LdJ/6PCL+i8uHW8MnnX9UvWNvx2v+NL3y4YpVRD9asOy+59GfVY6ZffSXeda17bN9Vr1a3D+sPjPVQOf6VoKf3pv9gf5Kz7L2PPBdf+Sd/9p3Re3Bqa/63Mz67HOu9vy'
        b'TkDL9yF5wF33T55vrVvZqVn0ujr0J1Xt3tu1Vz2aP7n1tndScVf1mk90M79c8fqGrW7ZV+d0zviV17dWzPpJZGz29eBzPzCWfh4d+B1FQNBb875T+u2cvT/d/fi7S9pM'
        b'udXRpqKVwYsf+7cHfHfG74O+t6Y3aNb+yi9X/2JW2dF3Jvz66JM1k6/90Nx68/rOlpKJvzz8wVGft5a8UWU40Xj4RFXqvxcbTn/c/vk7JxobT05wswTf/O1vf3j0+L6C'
        b'beMc8OSe35dhV+n395WrzAnnEgPd38+s+qjvfeOH8Z8HrzpoPV/61uTsSQcw6uCd0vSf/uDjm6Xvrft5WNWeX7sa7mSEGT8+W5G8IeDyuc6slr6oP1yM3db36W+6n37H'
        b'2nry+ap/r03Z+OW3724sur9jznci2381cPLtmK5j750z/vT5wK3GTw4byTSZDs6BfDwLj+E5OTFSh+VM6xs3chOJJS04C3mRo8yE2HFuqGgiNeFTRjB0qN5rZ9bYidUi'
        b'wejfPA2LiB6U+E/ALqWgPCidAxVQKpKE+wdW+m72x/wQ7IuMjlUIKnggxRoj1vJpUL0qUxRDVX+scCHkLI5kVdql2AzW7L/z+FTj9vedtr60H4WR+YExL9ziHePj0w3a'
        b'5Ph4bu2/ZjY4RyqVShZLXvmbVMoOVsdLHWWOzlJmi/+hdOTv//N+u5Wx7hL26ygZL2PZienrpIRRnhOcaS1ekuneUlbixq/u7Gp8ZRD5CLyk8fF2mOX6/y91iXHmEMCx'
        b'gZgOmvh/Dvlg/svBjWvRUyjCNiiCMixjvpcCojIHwW2KYZxsxnSL/mimg8J0hepFrr7rX7TGGdZ75n2UsfS1qVs73De+Mef/BpxL1Kx+M+R/Xw2PXJnd+ejbP3/vZ+p3'
        b'3zk5s+HW0bpN1q37fnnnSqzf5bc3xvwmvO5H+1I9f/zHAzG+JmO4qSPt8x9HujdkfbYz7cOwrA3bf+yV7HfqaNjPGy86BG3/0mAq+2jZ480LNgXW696ed963rbf+n6tW'
        b'/d6g+v7iv3m6yUq9P133+kPNRvMmjauYEHsIF6Cc/1+ROFrHUwsWRzmQMXRK8Z4Lnhcfk3iGnYTjFI4/9CcXSTVZ9suDfQmu3nEer5INVzeJomDuDEq4KMbjNXgkeyVs'
        b'PscFKNgE+VGRMT4xDoJSLg3FUsc5cMbMiI9XNN4LDfPdrBAkUQJeZf8nwcy+2AKVR8kh2/OfiXifH7ovjCLwKCU4KZMJm+CBA5RpsJwfBh6CS1g3og22Lqc2SmHyRrnP'
        b'EnzE84pEEC5gCXZhMaEENnks9Mm2odFUi5yKiqfxnN/OrSkslMJurI7CIgdB7i+BVniCjWb+fbxOvA+dYizcic32c5oG1XJohAK8wLlDKtQzmqahmqKySIRxW90cZTun'
        b'uYp0pj5KQsVQA428ih9bIQ/fJIIaHyqE41Bi5gFEJzZE+sb5YSEWzXtV3Ct8JsVH7B8ZjIiAZvxjYOkfeNHIXoZr+ky92YZrLIYVXBlzoYBMJpcwbGAPlLhzNsP4jLNs'
        b'LmM5C43qIVyYOSBL12UOyNkJyoCCB/cDcooJzAPyZH0SXSkeyRyQmczGAUXiMbPONCBPNBjSB2T6TPOAIoVgld6M2sxUaq3PzLKYB2RJacYBmcGYPKBM0adTtDIgy9Bm'
        b'DciO67MGFFpTkl4/IEvTHaUq1L2z3qTPNJm1mUm6ASWPRpL4UbAuy2wa8MgwJK9YFi/mapP1qXrzgMqUpk8xx+tYlDDgSlFFmlafqUuO1x1NGnCKjzdRvJUVHz+gtGRa'
        b'KHgYxjtxsTOM7MjEuJxdgtmFfWPOyLiukX3pzMg008iSwUb2PS8je5jayL6/ZmQE38i+eGtkdmJkemdkX4czsi+/G5ewC5O+kVmecRm7sG/XGVlSwsieZjIybDQy6zGy'
        b'dJyR5QiNQUPoybbDeQg9/7TxpejJa/7FcfBBowH3+HjbZ5uD+8vUlJH/BkqdaTCrWZkuOVbjyB4BSjYkkYTogzY9nVyC2qZIjAzTfWfaDKPZdERvThtQphuStOmmARf7'
        b'2My4blCcdhdRG1eL/2tqLQvMeKJNrpTLHJnGRXlKmD/6L5XP6hE='
    ))))
