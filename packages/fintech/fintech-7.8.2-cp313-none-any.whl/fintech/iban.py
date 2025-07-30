
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
        b'eJzNfAlclEe279crTTf7vgg2Ckizby64gqiAbC60CyrYQiOtyNILikbjLjsoKouK4AqCCuKCe1KVyZ3MzeRCSAIyvoyZvLnJvJnJYPSOmcySd6qqG0GTmcl7c9/vkfjR'
        b'56v6Tp2qOsv/nPqaz7kxPwLj72fb4HKMW85puRBOy1vOc+O0/LWCZebcaz/L+VN57JOf8Y5KBncFa0WTuKnGO7PgXzY8G8tfK57ELReanlDz1ppN4taOcpBzG0Xm+xXi'
        b'b3OkCfNjUuRbCrINeWp5QY5cn6uWLynR5xbkyxdp8vXqrFx5oSprs2qjOlgqTcvV6Ex9s9U5mny1Tp5jyM/SawrydXJ9gTwrV521Wa7Kz5ZnadUqvVpOuOuCpVkTxkzE'
        b'A/7JyNw/gEsGl8HL4GcIMoQZogxxhlmGJMM8Q5ohy7DIsMywyrDOsMmwzbDLsM9wyHDMcMpwznDJcM1wy3DPmHCMU7ornZV2SonSTGmpFCqtlVKlvdJCaa50VHJKgdJG'
        b'6aJ0UIqUVkonpUzpqhQr+Uqe0k05QWkb6UFWepMk3yPN/eXq5Xt6ckqPl7TS8+VnORfjEePpzXl9z90cbo5gIpfDM89R8FOyxu6ZJfyzJ1MV0m3eyCnMU/Ik8PlnMwUc'
        b'3AvluPV5GxYmc4ZJcDPVE9/FFbgsNWmpxQJciqtSFbgqQbkkSMxNWSjED7NU9NlmazPOgls1xVy+3qJs5kzOkAk30d0gfBT3mFsujcd7ZcClMkEZjy774dLAxcn48HIJ'
        b'LotXAs9qXBMAI+Dq+GRcvcIvPglXpySlKv2goTQERlsav1jpFxSfEMhDl4ScHpU5TsPN+JyBzBi1y9BVYM14xOAOExvgWxGyND4wEVfCuEm4PEHEFaMa87XoTkoWb8x6'
        b'WJnWYztc5lpmwJrQrRLCNolhGyWweVLYLAvYUCuldaSVcZt4acIx28SHbeKN2Sb+uA3hxfDpNr1294e3SfbaNrWzbfoykiw1ZxPq6xDVqFrA0Zur59C940KLXwi/iUpn'
        b'N3M3STgbuBfqOy3q1gIXdjM+WMTBb3lojsDHWTyLa+fypHC7Z62rsM37Sx+O+2zK1/ybYWkTUnh5xOIXrG3kdZl1beOi14c/1lasq+fo7Yyor62PWrfOlC55wvvbKtcN'
        b'KdwwZwiCBnwen0H1sCOw+n5+uDwkPgiXo/Y0P9jymsDghKL4oMXJPC7f2nxOoEgRYrCDZ9aGRugsCvBu2BbcwKHj0UqDA2F1E18u0mnlcSL4XMGhUhnaa3CCBttFuFKn'
        b'xQ3olBm0VHGoHDXiBwZHaJqE7uzU4ZvTNOT5Wg5VohpUTR9Cu9E1fEaHqvEdESwVbuXQqXmZrOkAbl9GWlpz+NByhkPNqGquwZnwaMfH8R5dUShuI1LUwFj4Bm5mjx1D'
        b'+811uHsBOieGtmMcql2Oz1LRndAlVKYzLFlHHjrMoYq5uJzKh0/64xadJT4aRx45zaHGAHyIctuIL+I6He5BPWoiXj1wQ+2W9CGZ7xYdmckMyoBDTaDTJ+k4zq7ouk7m'
        b'iDuJ3C3ADe/1YONcRud4uq2oA50Dv46Pc6h6TS6T+jbuRQ911viOF8ceasBNGeyhOnw6CvdY5qFuIsJlDp3eNZG2oCZ0FN+UaYPxaTKjDnhojpaxu+GAjqMKC3QNneJx'
        b'PAmHrkThI7TJNw7X6/A1N9xJNvYIh2rwHlzB+NXjngTcY7C0ELAFP5qB99IZuc+NlOEu/HA7Gecq7EQYPkwb0IV0tEe3VYMO8xm38hUc3aIoO3RWh2/hMtROpG7k0GH8'
        b'EJ1g21eLz6NynTU68qZxZ5vwUXSPte3BVfg67pEU80nbOQ6dQHtBdDKYfB14mB5JBD5FxLgIYriHselWLsvEPXp0Gd0WscFqglAXndN8fJeHeyzwcXRZzB46VTyFtiTN'
        b'nk4a7uDDZCHagJsenaHscMNk3I17cHd+NJH9LCg/Li1h8+3ZmAfOMxxdIg9d4VDrdncqd8482Kcec3wNXTSu0RkwhRtsXY+AZJehtSSRLGwXh876+LPZ1oEiV8GSowMi'
        b'o+odLkZX6VPOqCIUtt2NWSA8dCYG5uRC+HXjmmiQrwcc7HnSeAlWyRp1Mpb30G58jLSiA5vNmMI0z1tDpV9qOwe2UYBqjMKfCkHX2MqiypUyiTOqJg03OXQeHZAybrd2'
        b'ouMyfG0F7iW8boAUqAK2ii7TfXRcIisG+XeL2DiNk9Bpym+rJkGGb07cRpavG8Yhs6cNOS4x0AAKUEqm2wO6HLmdMetEtfgstCXiUhEbqVU1n3mch5H4hk7vxBHhSjl0'
        b'cAc+RldoChhAh0yH2tEeIVvzBlWSwZZo34pImXTpejLGbdDRNdsNrnBXnY+7UcU0XItuoEoRJ8BnxJt5qSCCgSCNOOIdUEUxqGIVKhdxwlwMMYyH9iBQEQM1y6P4jjs6'
        b'iW4Ze4WbOJmjKr4z6g1RCKjnxDen4FL7fFwBu13AFaA79lQofMQeXZZtTARZN3AbXPB+A8QBLgzdMsft0xJB1mwue5cPnZklqMxZnR7t8zfNGVUHGXzJzFC5NWhNKeqY'
        b'htpFqAd1q5JRFT63KRadTU/mInUidCw/yUCC1IIVC3T6ybiOLGcZhw6h62sMCiLHXXwijfDA7XMJmyugLkcpx0jUgY8JuQm4Smjugh9SURxQXYkOX98czGO+uxqfwtUG'
        b'f6KGtTt2UjYH0X5waTdRG2EUj66M8kH3hQLwAAeoOFHuQToLsOVKU0BRpRgCiDj7QLQbdE4X8G4i0OUxAnUygY4IxXg3c/6RqDeVON4OdIp4iGYOdqQW1xqmEF4nQFxc'
        b'Fy+Tok5Yn1E+4UQ24BMkwL349AamVtdRl1qndfAhunOIQ/uDcZuBIOZ5uDXQtMRXRGR50b1NMjmuQG0r7LnFcrcdZjKIW9VGLrFCndY1xBQNUQO6bAiGhsX4Pii6ic2o'
        b'JICLqsivS0SeIC1qXykqQtVFjFdTESi6NkFoCqAeuMwQAg3FxXg/zCoKd7BpVQk2MKnQWdwEe48qYOvjca8YouAVvJtZ7nV8UQOOHrzQHUJWQ7xDNRKqROghuocfAsfR'
        b'VSK7JlwGqoYeuuMeAe5CNxLorm1LS9dJ56NzfLZpxwIhZJKIt8trHZsc3feqV7etLZmw7gzHe5PFG5K5InRVgm7DLu9jIe00OuelQ+WzfYXM6Z0sQbfoquEWS1si15XR'
        b'3ROgI7gMH0MHc3A5/LqBmrgwiHeghxWzmEtu9rMGcJG7ehRcNCbSfeRlzaDqeUo3Kh1TzktMOesE4CsP4dsshByajpp1VvhEOJlpE3H5Lfg8VarEeFBMYJSJL75qLu1M'
        b'Ow8JzQKS6Mwm4078EEALeviGCc64m1MIhvblRbxUh6pXROpAD+cQXpE7RKgxfzOdmC9+uBZYheK9JvyjTjeEEoHs5o26gJeK1UGZwtKjHhVhFY5rRKgF38ZnmD7A7uN2'
        b'XRGqzRzFTL3gSIklB6HjjpTjIVjhUUs2bSWb42WhJBFdpJNUEq0CiIXu25gglvcWun070UV0/jXZgGEnmzG15iBUnpot0k0pocxKPHEH8MIP5GYsdB/FpwrZxtZp0AWd'
        b'AXfbmfCaQzgdBR1ToIOmUS6RUSBslhAdQQfl6AwYaTLEpgNvmIWDEVyiIROD98NndZaoFx83YTywDObILH2lL12q0d7xvnS/aagtm+6KDp2W4MoSVEdXEp0G668EUBiz'
        b'3YQJYZwqaqnochQeFa3jNas3zv+4WbBIB5igmvKbgx/M0tGAXU2W4BToHjzaxsJiqSVu0slwJbpmApPRuJK53/NZdqaRLotMUSBWjutQ21x8GFYhFTebBU9BjBO6AHtz'
        b'DcDnYX8TVEOXNhrCSFMDqsSHRt1B1TjZmTYIuWB0Fz0AvL0J37ZkCtWA29AR3dYC3CViWlCFTuMr1GQA/NzxB4YRAYTlpdcCzBQBBm7BVAF8DaidIMWmTaNA8aqWGjB6'
        b'IPUAJoAb949zVJHEcoScO74pwN2TwadQ57nbGoEi3Yp34TE8ftRhKpv4PXQ9XGe9C9eawCYEjA5qk2rUafmKTY4ZpMMykJpkkQg1TEP76KTjYSe7AKb3EFxN4elJfA9A'
        b'MvGq6zfhS0Tcw2D+V8ZwMgUfgQBfLWE+K3c2PgFINh03mECux0IWm1vwST0V6eYUpjevGeJZoZkjvkOlkaPuDGADGPaGCREDjuo2hBMjTd8yOjVF7JjJ0XtCdM0iOWYB'
        b'uuzLafExCQCZ4zkUu8xyVQCSjtllwtH+8RQ6QWA5Dlbfg6/boZM8pomQYKCjLJ7cQ5VMF8/gG+PCZqxcBAG7RYROx9owLNy4zQCwG7K0JrLd52Hqazyp6djgzvjxOjjW'
        b'017aBWAX5h+BT4jQkXzcRNdx19zlBMMf4kzYfh16QJnl06hR57PV5IqqRn0FvSOA+VtumspbKjKbgR9EU9FSwfXAFC1s4kwJwVZURiFKaiguTUSd5iXUgl81OQq8lqEq'
        b'My98Ukv3JTYH9LwHmJ2cbsYm2QQrs5eabQaAzDMv50kjOeVSge6jSuAUgW5AdFuOa6hQjllv4h4rvBcfNmMQ9yzes4lhnTObESSn8SHrxxlHOAtv7rgb1C0MHaMCLQNU'
        b'tI84GNdsonDXwBvgs+iswYfaMejrnXFIxYgGFiVOQHvBUu3BXIgsWxURuKcIYAafWVgNPomaqaXCZNujKIuT/uOsyKT76JAA3ynKY9G/CR9bD4xyFGLm7mpzYLKTSXaA'
        b'761/FZXwl3HCCHd8C0wdgv8x5hXr0uxIfiZEx0cTtJMWzNrL8WmIeT3m29ARU4pmY6BQRoYvukCDws+UoE3mUyWK8YwjmdsxXGvKzvRatsK1+IwvyBMc9Yr7ucJWuAtW'
        b'GNXKKRMtvgfMDdu8TGmcA2Iq6orrl0IDfhBlNJsjGydTU3fHZ3ErmW0tBKsrRuWkyOf6S4dx3ceYDYpQbzZh0/umiOGKOtgCigZC189+HWZGmvzZpfUQ+IBZGG4SgXeo'
        b'xjfYCt7EB8kS3sjZYjSdxl3oII2uElS+/TVtiDSBvEv4JKYKFrZShGqF4WxHO+fPhFQ1HHXz2ZK3rEbHqbarUMuc8UGKOAUWpDaiGxCkliSZRUGO9ZCKFZKGLwAjVI8P'
        b'mJJeSOypWPk5BE6PdQ+Xxy6YeQj1DuihCNWgo0Kq9YmIwOEeSwu8X8QS0bOQ+3TRVUNX5+pM7FLAvAhHfpZRPhsQr3eaLSqdykMnoqUpenzUhCLO4g6aeVfiB6bMe60L'
        b'3c8VqBRCIvj/OtjPcdmHyXUrBBDmesMZiOhAXbAbwEowy5Sl4+srGb45MxEafgjhGUGEIT9RVIibAEPQkgDJSpsguZ+NusSM3UlwxbtZHD2wC5SsLn6i+hU97mB6fFuA'
        b'r6ETJpzYEoBrabEH9ZrKBPhmJItOzYAua4hkb5i9hhONqeNDoVXybObq9wTvlElmoLNils+fAxSzn8GDnh3JZKU6LF5xXZ1MoCsCfMUPXWAosBK3LpZJbOJNpQlX3Ehn'
        b'JY1c/xpqM2qWmwVRrECz6bDdTVSWiCh0VaaHae4zRp26cHSb8a/gyWTQ0Ck0FTh8zZlSN7sFyaS43NtURYA0tZTGyOzZcbJitwTCqR3AKK40p1ECPZgIeBtEsmdB8HWD'
        b'Jl7wIQDPo8wG22FJmmTFEKiukTE6OFRvG2uIIAEE/HWtST3R9YLx6ol60nEV3r8Jn03ntJtJYnUQnTdWmnA93iMrniU1VWQglWHpRwfe5/Z9fqJDZAeItc2YWHVCyrDN'
        b'jnk0tNtBhm8u05mKOK6ok8bWlNg1oyY9DiWOSWxRnT2qF+lh/GYjjrXHbcBtxzpT3QfS/l4qM5+/ipSE2tFuU90HHbahDhsdQC3eMiuH7WTr73GobUI6FSAaN0Ns/Z65'
        b'mMK8/1bm8loBd6Tp6fxnTKWzh5Snm0n5GsK4IiqaylsiMZs2zcMQCE8sRdcg4xw7UbqXnaINqAedQNchVIc7iyDd7EaXqHVAEK3JIA/Y4v2jENq4/6yMga4JhfgIj8H3'
        b'BshFukh3A7r0qiyXmS2VCyVz8B7GvAf+O0xUomLnq96FWd4sAfida3EU/JHU7/jrHuSlFw9A+9gS1YnAUdzGpxUSpkD3VWkyK1TjRELhAw4k68YXmIe5E4rqZbB699AD'
        b'oym2gm1eYFG3AaDAVWjVC8mDveBpnUzFz+O4fJXMHODNGT7bxotpcUwnjoDiHZAZYPgjxsp2/XZ7uvO4Ys4umW7eBFNZzx23M5usiUN3ZTroZzTWZh4+zVzzfTD8u6gC'
        b'd6FzIUTH7oPDmYMPGyKJDDdjtdBUh0qL/Waz+h66bDRQVEoLgkLUk4YqlNzKdWJ8GkE2ohBSvhZxy3BF0mJcKSBAqVwAbh+dcMSdzHfUbMpPxOVJYm41KuVn8EK2oVqD'
        b'G5GmciqqScTVIbgqdVGAgpyQWdgIHNH+aOb8u/Edz4CUoHghB4lspTCahy7F4PIsclhk+iHnOfSoqRguc8Wm489jnJJHz7/4So6egQmUskhz4+mXME085vRL5Mkpx5yG'
        b'KUXjzrmEMSJ6+vXa3bGnX6rZsGfSWHJYq5Or8ukprTynQCsvVuVpsjX6kmCpNIGdBftvLsjXF9BzXX/TSbBcA08VqzR5qg156kD6YJxau8XISEeek25Q5W+WZxVkq+lp'
        b'MOFEeegMW0ynzKqsrAJDvl6eb9iyQa2Vq7TGLupsuUon3arOywMpZhaqtKotcg2wmylPy2UHyuSkecNo72BTpw2arJlyEHujplidH8h6ksHnJ8SO467JpxLK4ScLJqfe'
        b'piciqVVZufICaNCOMqTyaUvGMtWbRIAl+Pv89OSs3MghWJ5s0OmJzGSNlqcGRYRNmyaPSVoSHyMPNz6YrR4dV6cuVNFB/cknf7katsWg0qvpEfv69Wlag3r9+nGyMB5G'
        b'edjq0K00yiZfrsnfmKeWLzRoC+RLVCVb1Pl6nTxGq1bBmFq13qDN180c5SwvyB9VhEC4u0iVp6O3yeJs1ehA0HGnpyLu1dNT25RFRv8BTuyqrkgEmG8dK05logZ6NGqW'
        b'50pOv0NDrUK3fZdeyNEIvByfCyoC51QBn1dzq5W4l/Y9nSnlwC4loYvyVO9FhrKz1SFfa24Cx7mEOt1do9w5lTFwy8rTyfjcxnTjAV1ricKa1e73LLYkLTIRawkPZtWF'
        b'8+gBOqTbKuCCPNjBnb8TcwG7LcN01sQZrWbHdvNRC2t4aAFooMdSyEXnsVO7XHYIg++gUrFMK+Iy0WV2aJchpENvnhUiKxRwSlRGs896OVsbH/CPe2VFAoCsqIpi4hO4'
        b'eic70IRAuBtVWPC4jbiZnvLZhDE/uQfdX4h7dGJIvvfTdOFI6i6WyB9ATbhKh6/xwLNCyKcngBBaWGJltg2ypx6DgNuOS9kJID5vrNk6raGwUMQRQMIOAaO1bLDe1W/K'
        b'YGUWoys0LDSDwKxaAhltqwb3wFxB0AYOn4BcbyLkRRRnnoH/ynRbzbh1qIZW0WrwPUgnWS0HX7TUbeVzS/WsUoXbdigEbLDj6PJq0oRqhKxtKSTWhGEqeuDOxrpIBCFj'
        b'QZhuowxT+biTDAWev5ON5a9kincGnZPocI+QsyGLS893z89S8FnjZfQwkDaugnSXNfbE0MEccCPq0qFKcmjqZjz+3Y+aqcJ95Slm7wIsypiV/IY1RyPaIu/QiFCQuJyc'
        b'EtRxG4rwJc07nn8Q6uQQTH/P6965rHsZDrU4Zv/vKen8wbLLBzwFsqzjWn3O58HL5sm33kcfero/fBt9t+FG928r6raVBd5/8bV3SWr0mr/xTmzsPXmf/01anpvovfa7'
        b'f+gv/M+nv5/Obaz7snJLdIHHcGRJ+YXOryL5n4gS1/9ifXnO5/1f/bI4OmjKuo312559fv2DdTsfFz0otliU+VtD1WfVZ5LiF2Hbq3/64+Cvi66tmfCb//D9q+OZhT/p'
        b'kP4td/+a6sKNtrc8P/sgrne67YtdDb/9z48+L9b57zvu6PBvc52WGnxPTGpZHFv5NKox8Ld+V13Vj37+xluJQ9+YF++cN/jiBlcS9rHDdwmzvfY82x/yhVS53817riL4'
        b'k67lnom3TmxVzS7fdPhSeu7/eOy5/tdrJzwJynw75ljmd+8mzPY4FaUwe073oz16TkCQH0CqgiA+J0ZN/KBEfPs5O7yrnRkQnBAIQOuovyIY1wTiMrB5uTADl0XSHrgD'
        b'ssF7ialBqAy1pafSqC1bysfVAJ/3PXcnPTonAayuwGX+QZCF3gvmwRB7+RHgmS49J1lLTEQkPXIl77RsxdXT0XXyTktxkD8uD+Fzwei+CF8Pxh1M1E6tN65IDkxYp8TV'
        b'HCeO5Fs5ohvPycs7pBAzKZG8EJPzJowO/Bi8cMT7BbgXkNRdhWyY76fQEp/woy468nqKXL7b9DPsODtHW7BdnS/PYW9oBZPwOHdYSgNAJiG0xDr45NmboIff7Ob+uETE'
        b'ObgMOU8Ysneun3l4Zt3s0gWfWtsNObnWaw5r6jbXCj6192jxvhjSGtLlPThpev+k6SN8oaPPkLvPoHtQv3tQW/aAe0SX7lZJd8lbdm8tH5ieMOCeMDTZb0TATVjMeyrh'
        b'3Ca3RLSZDbqG9ruGDrnLP3X2HPL0avFqiWnIrY371NppyM3rdFBj0ImQWjMiw7zD81oiB+39+u39hpw9RzjelCW8ZxzPZQnvyUTvERH5MCLmnNzqMw9ntqQNOvr3O/pD'
        b'xz7faQPO04agi4Bzmf7E0fWV9pbNA85hxubwJ64epyc2TmxzHnQN63cNI1LZOzfEtc0dmBAFxDef2jo2eDdoW3gNfm3BA24zyPI4uTWEN8TU5pbGDVk7NWgGrKeQuw4e'
        b'DRv7HXwHHQL7HQLb0gYcwksXfmpP1vNTa9chZ69B58B+Z9LgHN5nE/7EwaXBtsGuNr5hKzzU5tCm6uK1ufY7hNfyHjn7tdkOOAe06fudI/psIr4ZWcjjJvgOuk/td58K'
        b'83f0eUSEh9/f6sjev23ts8iOe9fOZpGP4F1vHly1AJE5hcWwkOzzsABAz7CZEWYMCwleGDbLzNQa8jMzh2WZmVl5alW+oRDu/H0VA8fGrYcfk5ppiXOjWkQvx0mfKLj8'
        b'ZTf3QiPk8Xz/i4PLZ1bOFZt3y0b4Ip7DI5ldRdRnQuv9yUMS60cS+2+eijiRjYn6Vkdc6ElxINcpmy4Ap0/g9JuQXZROtE4EO8EVKbg6NUHEWRUKZuRMMVDDLUVlSxOT'
        b'oAHVhAPkDuBxsnQ+voIuFbEwdBw9wNUMqKMjNgSoo6PoYJbp3UryIzRhk00EbvMZ3KZgmwOoLY4UGiG2IG0MYM4XAsQWjIHYwnFgWhAjpBD7tbujEHsjQOxtPAKx6VuQ'
        b'YzC2tmCLXGVCy+Mx8ng8TN+2/GH4rVUXGTRaBvYK1VqA4FsY4jS9jhksTTXBNRjQfxlw1mxRL9RqC7T+lIEKWrJfImwiCxGFoexXBRyFpkYhWa9XJR6LwwGqbZRrGNLP'
        b'KtBq1brCgvxsgKEUjutyCwx52QSmMvRJMb+cYf6XgHShhkzhJc6FPEMlDw/SGwoByxqRLZ05wG0/0iOQMFf8Q3gqSjHMovoVkzv6NiN5lTF6uvFlxrIk/8WB6FIae6+R'
        b'3EhNSkjmkepemSwqA59L06wSr+TrUoBL8ZfKnqzGn9mgS29zPMVji+cai/7KJVaxoWcVR0/9zAW5vfP+bt78htiGvY1JreHnkywsRJVegaEDdnt+ZVvpm+Rv0Wrhb3Ey'
        b'iOv9VrJniljBf04q5ujOonkyf1B5XIYrkw00Fu3E3XxuIuoR4quAA488l3PkhHcPKk0MXgwRCVWZIo47PuaGrgvzJfiqQvwP7F48GlqoxQ/L2Hu7LIhMNAURslokiCwy'
        b'4xw8HztN6ps8f8Apts8mdsh18qBrSL9rSJekd8pbkQOu8WWLWWBxdq/d3mfjBa6+NPEZ2Qbmt8yGJSZNGzYz6o+WRFYtQbFat/HSmTGvRARkDmmi6TJockh/Boe0Wczj'
        b'eUMI4Xn/WId0XOzLXZCFCQzzGJQ4j7uMBQVTOQFfQPdorQXtR9dQJWoJFKxLjETVRYAiL6D7Um4DPmKJT5HyD4W/bfgivi8rtuJx4Wg/D1IK3LEVsSrHxmm4QlZcBGp0'
        b'0pdHgPhJdFPKSia33SALwTetw4XcLn8+MHPCXV4U4mpw1U5duJYPEHMer4BDt9A1T4aY9+EHEllxsZjDdSk8fIDDTTPcTWh6t/Vm5hdBVxqJY9yEzrMKxrEIfJ9VMIJR'
        b'2csSRuRmYwVjHe4JAI8LaUQZ7uGjal4sLksZ51IlJnvSci8rGOBSRUpTDcMcXKs0UjLqWsX/QteaC65VNbZ6Qf3JK7WLsY6IOCrS5ftrBj+Q4pMH/lsz/Kw8OqROrX89'
        b'p39lcDK3gqwsA/jQ/CwmhCmrX7gkRh4LEV5L/OoCiAdZ+gIt5OyFhg15Gl0uPLyhhPY0+vNYyPu1qjzKYz6YYfAYGVRkAQ30OwD+y2PT/APh14IF5Fds6rIw+A1i+M8P'
        b'n08bYmP9AymXMfKq8nQF31uDIBOga1XIKg/AKZu49ZJCWBDC5J8KdKNcCgpZfCNP/nMx7v++xDEKI0ZjiHXKIhpEUG1B6rgg8g9DCL46gUSRbXNpVnllkwsXukovBD/3'
        b'RtIs43vjG96w57wLfw2DrV/7y1VJLNUMJ2+yksoIOlCymluN6/EdViKtgWTjEKpApaiUmyPi+PY8c7wHV1NOYdHW3ASX6wIudH3eIRd7DlJg8nbiG3wZOY/gbMK4MAzp'
        b'MC1UkKTZNgIGFaDT4Vw4vh5NWTwttuHkFl/wuML1eRbxOwgL8tpjHrpOeeDOImAiRV2MxymFNe4Bvx2CS5dwS9KN1Z68WTLOId4cBlyf9Dg9jUvTvPvtc5HuI+JOJlXt'
        b'PJxstTfU5kDmmha5W/2drw+9846s6+0vvYbDmromPS04uyb1VzvPH7AToLyme3/69LdJOyTz5A8WKp3Fj12LftLXfn3u6ZPnPq+wj971efWetTmRMzKeXU+5fW1hguLh'
        b'iQTLZ/wS8/hlDV8v1nw1xMW1fVmz5lLvmyn1j4er2t/rmxA0M37X9vTsL7TNxz67sfGT/gfKnEVLB/KvWG3X3j7+ycSvKp0evfNT/8lnHRx9mqY3rJn0yYeCstZfvvfp'
        b'BzsnXj1sdiVk6dF5Peja7x53OSc+XvX8G/4nTZM2KDYoJM+JG47HVzYFxKJ7kNuaEluZgcb3xa6okcb3SPxwTIg3xXd0FnU+J29g7EAHNcQdo7LCjakkxw2BXkHkiUQz'
        b'2LkWcQJqxSefk2/XeCr9ZIm4UpFsmBJlZOaIDgkl+Ca6T3NX3LsBXYBEmYfO4Sscv5gXA2Ht+nOiQjPxAVQLWnxvDS4LSSWy7uL7oyNraONaVB0Lbc14D6AMU9Y7EXfR'
        b'UVXosCERVyUq0G7UYsrPrUMFG9HDyQrzH5fmktL4aJbL4Ig5S2nBkWuDTGDkN0Yw8gaAEWeSnNk51isOK+oCSmMBeHzq7PXYzbdvyqIBt7g+h7gRvsDWa8jTb9BzRr/n'
        b'jF77Ac85tXFPxQBjGrJaIgbtp/TbTxlyn3R6VuOsFt3FktaSszsG3SP63SMgh3xi7zlo791v792yfNBe0W+vgMEeWdvVRlRsawiv2NUyuUXV6tsWezaoV/DQ4rbFW8rB'
        b'GYn9MxKJSNArrKy4wXXAelJLVptXa06X+YBvFE0XnRoiGopabBtmtGy9uLN159k3B9ynsbz8m+cenMskSAJtvR65yyEJtPX6VkdM7bptbDCHg6WxswR4Jg+uDEvJGHAi'
        b'cXtYABHl+yDUD9YTXsv1gkyXr8ZCq9VmPN7E5wCtJv5YaNUk9ucuyaYKFDwKPN5AXajTdOSShB+yExfciO+O+4LQqKPdwLF8jX5BSBjJH/0ikOBf+0Wg7c3SZSw6/ECq'
        b'kkOzDooNxp5y/L/Kz8aFIcFrYUjMUpkQfC3pn4lC4pLxqUw4wEKCMlfjQ96kTA/BBO/ewqHySNRIzyeXRKBG8Bm4PBlXyh2X49Ikvt1C1I4OoPOoET4ouCU2Zuhmorfm'
        b'P28d5+mWkDj1i2k9WU2QELWxhGh8OmRD0qGkVn2wYEmz4/K5DeY5/HLL3xWW5Hi7u+ybERY6OVmi2t2+RPUkj8fpHpurzesVIprqrFOsGM2IrNNedZi3l1GPiy6um41b'
        b'VgWM8bjRMc89OfpmzGXcTGqJ/gp0bu7YUiJ4N9oFXcAnPYw+FJ/eOc6Jntr5nGgxOj1hYaJ8GfHEY0uN51G3gj/GwIifMrkws41qPXVg00wOLMnowHZJXs2mXtbmXimR'
        b'PXaS93lNH3Ca0WczY8jeY9Dep9/epyV7wD6gzyJAS5aHuQSRlqzC9+ZSJA0ek0lNM13Ie5U6cpr6JxBpi4THs/sRlv6MWPoRwPdnZEGCf2jIQiX332TIkBVs3y5dXpin'
        b'0etGrZWdjYF5ysndHK1qIz33Ass1WbxKHvm91QSpX2yqMiVt2epAeWz8wtjE5crkQDlwS8yMTV2wMFAeE0vbM1OUyfMXLlP8YyOlIOj+XOOXCVd8GDRBH80ZiJPFrUmo'
        b'jHxdMyDRPw5XgsUujafpGc3N8BEFapeixhL4l4DKSgBfiaWoFJ8AyEZe8pvngJvYw+xRsE92pl2JmjxxmxAg3Zn1mv95apCvIzJG965gpjnhnZ8yK9RJdKGxC98LnSyL'
        b'9Yz1i5XUTV2yZdJ0QWxkRJI6tE6R9qZ/lmS5nyCg1vGdcs0GSUTSOs8sv7PitEjRx4E5+1e3Vsb8rvd/nEdvPeJz316ysHC8qhA+p4nkIbmYWCE+i86YLHEOOkBL9lb8'
        b'+dTKIFNuHrVjambu6Aorsz/EJyJonX2jhwlxFNpTC8wkq5VIYZAfpLc30WVzFz6AoH0lCuH3BjuyC6NqPyyF/EtnLG/MNRlkJjPIkQxzzsFl1AJfrwRTK5w34BTdZxP9'
        b'QyVh6NPiOeAU2mcTOmTvUj/78Oy6uX0WXv9HNjrXdPEba6PJ5j/ORrXTyag8A5Eg3CaJxWBUgWtCUDlzYvigi9ubwlxcnfX9JpxDTFhoisXkq7qjddN/eTxWOZK66diQ'
        b'TIuQ+aotNDX9nkhMElNysF2ohhsQsYOlCcyY81R6PeSZWSoIseMZ0QCtymbl2NcyaeloJv2PEmmWRP//gQQkKYY58Fk9L2QsEEDn8Z1/nJISKACJyD7qpuxULsaT+eiJ'
        b'+83Ws4P19K0OuuxlRS+/YrKUvky1DJ+CnAI3rzRChB8ECOjKHMq8N854iJpzKUu5dhan+ezDIZ6uAFqmG7xZHfXc98GGznds+F+YRaxeHRbqLQ3n/kscFrGe27/YUT6r'
        b'1HH5AcXRD9TCn/Vk/cwsAidFF7kH/XnK2mbRe1sC/fKzRKvrzbSu0y/cbrWQ1Bfd5LhfHbZ6Mv+wQsxO7XoSlK8WWvn8OaY6aweufE5ftaxA9/F9lonRPCyVnlmQ04fK'
        b'ZBE3PUUcH7BrFjr2nICpjJ3RYwDI9q1BqEdAHR+6jip5AUk+FISMO8w8gbopBFHjBnRSBhn5IQZDxjrHbYbn3tAlG1d7Jb4mAtqTCzIfEcJ+XEN3wcf8IPgnPmZMwdeC'
        b'whNQY2IY2jiTS9zFGSu+0lcwCkmAZg1YT2wJH7D2oSdf4f3O4V2zBpzn9dnMe+KpGPQM6fcMGfAMq5UNOU8adA7qdw5qyx50juh3jnjs5t3nM2vAbXafw+xH7j4tmwfc'
        b'w7vC+t2n1kooq+B+5+C2bQPOBOaM8ZhmwzLisDMLtBRI/d00h9WMx5S06ZzoZSbPmNiAF31RBF7UldSMXX9sYnNU7M2dk4UIFIKUlEUK3iIFP2WRxk2fx9MdgqX7Ky/+'
        b'wEeH1tipJpiNvLCKecI5Tkmf4XZzSUBXV6S7/mdHV6/4+n7Av+8NjFtda9kzZ8sfVDuuPuz5w31tbkzqvz1746tP/1z1YusLzuPB/oDPUnLNU9Esn5kVe+eHFNjcCTkj'
        b'KYnWnLDZEOob/qJ1uGS6+433cgPOfhyx1OH9D8Imd60JaJzocGZej9PtOR5ewUtdwq+e8lqY89PqnN/vfjf9hFJWr5x6TthzatmDHN7llQkln+1xnusw9dGHZxa2uPgk'
        b'iHYd/TD86IA07UN/Ye7UTV9OeP98zEcfzvxoQPz+2Wfdu4MXTF63/yd68+MfqiX9vpEDToGp/o83HvjdLTuVW0zAugMfR256t//gVH3QsMbsk/6Uzovu2frJ0/pdpg0E'
        b'fXlmTX/yrff+8vsvW2d1RbS/8/6p4tb6386INrjop/+xb+7vzv+5L/XF51zyT9+r+7rE+mdfclb9WNsUY9GvquybPGNxXFGlZ5x/z3K3Kb2eOGG79OJvXCsHehpavihs'
        b'znhr4faEjMzj/QHXPleuPTtYtO/Td7zvH/jF8+o3tm799fMX7w837OW++pzn+Stbz8/Nm3+1ui7iwrnIdRXO5ScnH4mqL78S7PWu0uvdvxz8JjVnoW9EXlvRyvyczBln'
        b'UjLPf9zs7xW5dMrI4yWxVs+qMxwHtZstpv55y6DF+cNfNH/1m8X3l4V8FjJZPm/XvVKnJ4eW5vVa/twvwt+iYGhP/ccbPoq6tMo+/YvrO1dcnrh8qfuua9cCO3/18Tz/'
        b'CX+6iDdvvnP0tzXNBSNOfxjxnDjjJ3F//E7d2xurmBIwnX/vheK7uYpbH4tOn12ccyEkJ/+DBQfeVG96/y9NIRG/fi9n14mv3nOd/Rn/jf/4xWDUpP/181trBuTf/v7R'
        b'F/o1/xH17GpffocjLt/89XQr0SeLl9aAe6MmsXwBxHvXrTyON4MD53VEzjKd2/gYrpON8TGobYHRzWQKnpMvRaus8MHXHCOkSEXMM+6YSGEePrGNjysCE3BVkJgTZ6Bb'
        b'+BZ/8hIHWhrCda4FAYuDIM4cR/cSklJEnAx188FB3can2asbFT74WCKJVUE7MqFbZQLpcpWPL6Emd8WEH/eihOSHLj/6dYvv9SpkQnLTTzT52T3uhzlTSWZmXoEqOzNT'
        b'm2pypOSrlH8FbLmIx1k6jgjNzJ2JBw2v2NrgVfFGo64lvEXVOvXE9ralJ97s9u7S9np1G3qXdm/rCX57wU/tcPxAeNJjFwJEVY1TT5i3LO53Ce5y7neZ0Tc7pd85pW9Z'
        b'Wp9yRf+ylQPOKwnwtKvL77Oh7z6s4o1IOTuH2pjDjqXzvxaL3aSlViMOnJ3rkK3LkK37UzOhq7TUcsQqmecoHbKw6bPzGRGQz08sbGpDRkTk44iYs7QFwowSEkaYU0LK'
        b'CBklLIDos/MbsaSUFaW8R6wpZWNss6WUHXvMnhIOtCloxJFSTpTyGXGmlAvr6EoJN0a4U2KCsZ8HpTyN1ERKyVlHL0pMYnI8nUwpb9bkQwlf2qQYmUIpP6McCkr5G8UP'
        b'oFSgkQqiVLDxuRBKhRrbwigVzgaIoEQkI6ZSYpqx33RKzTBKHEWpmazjLErMZsQcSsw1SjWPUtE8I5MYHqXn84xsYhm9wEh/vZDRi3hGUeMYHW+iExi92PR8IqOTeGzs'
        b'ZEamGMlURi4xkksZucxILmdkmpFUMnKFkVzJyFVGcjUj043kGkauNcm1jtEZxuZMRq43iali9AYTncXobNPjakbnmJZhI6NzGR02omH0JiP7zYzMM63qFkbnG5sLGFlo'
        b'JIsYqTWSOkbqTWMbGF1sbN7KyG1GsoSR202S72D0G8bmnYzcxTNu95uMjuYbu8fw2X7zjZLGMnqBqX0hoxfxTfvN6Hgj/TSB0Yv5nP2kITufITsFvXqZ/vf5ejXtUWo+'
        b'spbPuXufDmkM+cQtoGxxaeyQi8+gS0C/S8AnLkGHhbW8IReP05aNli2qAZeAI6KnAs41+IlDcJdjv8O00oVDHhNPpzemt4kGPIJLE2qzKlKemnPugeANpDaPzG1qsxp0'
        b'bbFd2f3ms17w55hHPuPIRcBJZ5OLzYgQSLIItHPD5BZdl7DffOoLvq25C+kwzdgLSDBeZ9f6TYc39XmlDTgpS2VPzK3JAMtbJrct6HLsMvSueGvhT336Apb0my99wfcF'
        b'Bpwv47KMZ2QDNNFpo2T95m7/xbcwDySN7sYeQIKnGdvBynzS2A5Agrth4i7vN/d6wbczjyJttJfNUyGQ34xkSXjmCbxHdhPPWfQFLRqQxw3YxfdZxH9L37Yqi5mQ4MG9'
        b'52GfEGqs59sM8yFy/JNF/H8maNm8hMLjAxUNT/RCDqN0c42YOJbH49m8AExs8zW5/Fhg3CwO5q7IogSan1ilC3U/gTv+to8MtT+X7o12OPCHv7SLbB3/GNceU/HHX1/L'
        b'kOd+tm3lXpv9MaF7rQf+PC2y/NhA3gcWJ3c8iHhx/QPNB9q/CRO8T7YK9++P+SL73u2fvJObUOudP6j4zaF6t6qkmSvXzvfhP9M6JK4O/53vOzdWzLdfdDz4r78Mtv3y'
        b'XNl52Z+133y3+m56QdPF9ohEp4Ke2jPRZnMmeOGwb3ujqwMsQmdbnOvZf+hirpPd4ltde/I+ff9u4akH03nlj77zWZgo+exayJOfzveL/8Pf+K5fe1acLFFYMsx0HHe4'
        b'0L/Olopr6PmbDF3jZ9jiNtSKzj8nL6WgZkh7m0i5vBuX7cJVqankLM0W3xNAl4N2rE8Hbl1F/mQHMLlpS3I3VIVqzDgrO4EnvulCq9i4cosoMWEnbkr2TzbjxEK+ZBY+'
        b'xloa0d2VAYtFHA91oluJ5Mv6XVHP6RcfK9ENENGU+qMLO4zHAKg6JBHQWzUkizUCLg51m6EadM6Fgjx0BqS4MPrQqs3GZ8Sc8wKhfya6SCvvE9cX0oRzLB93dEK4QIMu'
        b'4Ae4g75lC0yPoQpSi0zEFWb4Pi7lhEE8dBm1OlCw5wrNdbhCETRtKSqDUctSIehYLxUoURk6/Jx+YbkuBp0mPUg76kgMJJLTsiaPk5NvwsMisreCA9FFXBuQGkjeumY7'
        b'gR/wVegmvoXrPanIqG3iFvJtTkCfIf5FRvDqZhAu2YUOwg4cUEz6Yej4LwGM/8KLbhLFnq9Bzld+RhGoJl+jBz+SYUKgb3P0KO+ZGyeyH7J0GLT07Lf0PLltwNJv96Ih'
        b'ofRQ0p6kPluvczM+Egb+QmgJqM/Ns0/oNMKXitJ5v5C4Atjz9Bv0iOj3iBjwmNoncRuSWNXIymQfOfh+JJkyJLEblLj3S9wbYj6SeA5Zuw5a+/Zb+w5a+/Vb+w1Z2NWk'
        b'lKX0ua/6yGL1C/FmoSjqBUeuT+l1JN2cs3DYnfrN8yL44PyM44tChxxdS6XGEfocgj+RABiF2+wc9K5wfgiHQjxirQXYigdX5jcnDgvy1PnDQvJCybCI1vOHhXkanX5Y'
        b'mK3JgmtBITQLdHrtsGhDiV6tGxZuKCjIGxZo8vXDohxA7PBLq8rfCE9r8gsN+mFBVq52WFCgzR4W52jy9GogtqgKhwXbNYXDIpUuS6MZFuSqt0EXYC/V6DT5Or0qP0s9'
        b'LKYFwyz6apu6UK8btt1SkB01PZMdY2drNmr0wzJdriZHn6kmBb5hS0N+Vq5Kk6/OzlRvyxo2z8zUqfXkfd1hsSHfoFNnv4wHOuI+1v+9H7mcefcM04X8sUEdcfPfffcd'
        b'eXPXlsfLFRAHP/76lF5/jLsnAextiTjGhXvbRRYzWfCtxPQq+rBNZqbxszEX+tYtZ/wfEpXnF+jlpE2dnaKQkNeVswuyYMbwQZWXZ1RdosmkJAX3pbC4Wr1uq0afOyzO'
        b'K8hS5emGLcaWSbU7OWOpiBWNmCXMZn+odK72AJCkrk0P3kYEEOSe8oU8ISQuMsvdZl+LF8GER5ZJOXNboyovHpRM6ZdM6Quc+7Yv9hsIXDwksXkkdepzjhiQRvYJIx9x'
        b'NrUuH3NudLT/DQRUYNM='
    ))))
