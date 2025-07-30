
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
        b'eJzVfAlYVNmV/3u1UFUU+75bqCjFviquLeACsgq4L8hSCIosVZSKK64UspWAgooKiIo7COKu3fcmPZ2tA4ZEhu5Om6QnmUknaZKYxH9P0vmfe28VFGqn0/P1zHxT4qPO'
        b'u/edu53ld869j19wJh+h4fcfj8Clmcvl1nCbuDV8Ln+IWyNQCdtE3Bs+uYKLPMdd5Y202iJXKOBU4ovw/epYrW2cxmKtAO6b5Yom1j/Aw12J6hUuPJcrTudkm5Rmn+eZ'
        b'x8dEJyu2FudqC1WK4jxFWb5KkVpell9cpFhcUFSmyslXlGTlbMnapAoyN8/IL9AY6+aq8gqKVBpFnrYop6yguEijKCtW5OSrcrYosopyFTlqVVaZSkG4a4LMczxMBuUJ'
        b'/+VkJj6BSyVXyVcKKoWVokpxpVmlpFJaKas0r5RXWlRaVlpVWlfaVNpW2lXaVzpUOlY6VTpXulS6VrpVuld6NHM6d52zzk4n1Ul0ljqRzlpnrrPXWehkOkcdpxPqbHQu'
        b'OgedWGelc9LJda46M51Ax+vcdB462zxPmHfpHk8BV+U+cS73eMk4Abfbc+JduOM18Q7P7fXc65XOTfnSsu3cDuFqbjsvy1cKknNMV9US/tuTCTAziEI6p5QlF0qB+rhc'
        b'yBFJ6NbkJoao0jitDxCoR42u42pchepRa0riMqzDtSlKXBu/PDXQjJu+SISfbJxPH7/oYMZZcJxNiWBL4anNyzjtBvJ4Pb69FvfKLJfFAZOa+OVx6Lov1gUsTcLH0lHv'
        b'PimuilsOPOtwvT+uSsF1cUm4boVvXCKuS05MWe4LBbpgaG1Z3NLlvoFx8QE8uiLiylCV4wxUH6oNgybmo7P2wLtu5bwJPIBpdfCyuIAEXAPtJuKj8WJuG6qXrXMsyOFN'
        b'JsTKOCF6uBy3rIRJoSsogtUzg9WVwpqawxpawDpb6azzrOjqgWxXiV5ZPQFdPf611RO8tkL8XoFh9d5YNrZ6m15dPfkbVu8KW73vzJXQ6Q/ZNjXLal42R28WLBfQJQ3J'
        b'+/MWZ18PdvOhu4yzgXshM46k9S3aym5mpIg4+K0IWayTz9+1mLvMFZrDbX93F9ELO26BjfiL6X8Q9Id2LNnMFcqgoMyvhf/r1lxrbsHGsA/Vc1bFs9tupX+0zncNniRI'
        b'fc5/4bJ5RgU3wmkDoGAWqrODVYIl8fXFR4PjAvFRdDkOH8zwBVGoDwiKD1yaxHNF1rJ51nOUwVo7eCR0dYLGgp+KdRyHWzh0IrhQ6wC3y9Eda41abIGuwf1qDun24EO0'
        b'AHXifguNWoLuRENJLYeO2gdqHaHAaR/u0OB+zl8B9/UcqsEH0Dla4rNgswbVifB93AhF7Rw6g9oWUGbuqHUlFAkyNkFBB4fO4g5rWrDSH7VqSsXoIr4FJfXQSowTa76p'
        b'GN/X4B6z9WIoOM4hffFqWmCFz87QaMUbUD/cP8ahatxXoHWGgjx0GNdqLM1wPX4IRec4dBKfQadpz3DrLF6De0W4HrUD1QzstvponUifUSVq16AaDgS7nlTk0Kml87RE'
        b'LPDl1KUauUAJ8o3bgJsNvkR7EIS68DXNdqGQTMwJDtVtQdfpA8ti8SONNWdB24cnWpwtaOux+PhS3GspytkN969z6BysVh/tMyj0BbxfrhYnIXAm+Co8gx+hFvrUMliB'
        b'w6jagl+EH3G8lEM38H5/2uccfHOOBt/i0X0BPNQAXFAHukr7hpuC83GvVshnsIluwg+WUm7bC23kuFuMKmhDN2EJ0tAJ2mvf2fs02wW4NYnxOopuTKWtoMoF+IYG3xGJ'
        b'UC8UneTQMUt0mDLzLkYHNdYCV/SAtXIKt+GjtGRTBnqEe6UCC3Qeijo5dBpfX0tLXN3RJSgRo+pFUHIJOoB6A2jJbPwQX8W9ZWJ8ZzFrqL64hAnBg3gz3Gth5oDusWfO'
        b'2Hqx9XyYBqvda8HjDtAr3AXc/CW0RIJ7UQXuxT0iW1AUfB4kPSyajjNt7kYwnfxCDdy+waH2XbhL60IaacTX8C0oEuNufIZNTge6OIMt0MHpIM69MuFuuM3hbg6dx92o'
        b'gzZVmI9vwlybLVnNxO0YakS99Cl8HN+2hBXnce8S9lQHcDlLpxVfjiyE/vXCsh4A6gpMkQdqoMPNmJVISiRa1MEE5exbW2mBBj2cCavHp+1lfT+zAj9ia3QG3YmQS3l8'
        b'GN+Gon4OXcB6Pzass+ghfiTHtyT4OAJrDBVgWN27adc9QYQfyLeJ0X6etXQSH17Nut6Im1GtHPeL4vBhIHugDXxNQMsykB6fgyIzuEVEopeI8t29dHbnlKIuKBLbzWdN'
        b'tSfuo/c9s3drynhUvRFu6zh0ZBnqZxNbjfrxYblGBLLM5rwF9+MO+kwSehQoNzeTgj/C9zh0UYIOaN3hvheuQXWoegbWo9uoBh7oFXNC3MGnLCnWepG+38YNoPLV23AT'
        b'qgVBrsGnxJwon0f7YYVPaxWk2ROoDt8wVAkjjPCtclQj5mSoVuA8bbJSSHughontRt37cDWAvWIOTFE6NaLocvJy3I+aEsANZHPZhfgBrY7u4w70MD4kARxJLpcLcqSj'
        b'02wDrVyG4TuBZWXDx3oVBQJCdNoeplqHrhZ7zUCXxVlJqBZ3bo5F59ckcREaMTruh65RHugAdP6hpkyMurcDkyrQS16pVZKSI+iqC2MyA4zDcdCIE7iJkhHoKj4u4jxw'
        b'rUjmPpVNeIUNPqPBfSArU5nhrsM9+IrWl5R1ecCSUk6oH0TjOGr2xU1x6MYYI/RIJNxqsAs63LEdXIkPSCJzJVD/AetRE67WGHt0HbSgDbeO9ega61GDyKx4Oe1ROD6N'
        b'L4PpFfhgYsvPcqgVN6IL2mlUwYOccGMcugaTg48XORm4hJHOAZdAIb6LHruwCToUk6tRi9ANVAHPVQK9GaafdCcOV0IvjBO0XktnGT3cLFfgatS1wp5bqpDI8T10hvKZ'
        b'JdkMjhAUqMrgCWHxblBvuzXKZnya+zBMtaE76CauJb+ukE4FqsWlCzaxLt3icTf4TtwC+sOc59Z12mAoiQR7f2BsYLXCbNYjsCqnYPlR9ZqkYjCocfiuGb6Nzi2k0rUi'
        b'FdWDueeKYoFXHWjOloXaqaSVU3Eg8WOTxBZMlMalJ7rjXiGYqXNgnciKrYJq1RpzwQ5qr2HFjgOca9POJjyuEUM4vvK1xpUjA7wHtpSsXFcSaeJakll2EleKbkrRvRDE'
        b'jJkrcL6uQUdF6Ao6xKxga76NNhCKYhbBDDaSLrHOWeNOrBOiBlwF4nIkDzT4FBeKz4lBo/uZi0LHIgIIsEjZYQAWqBXVUvnEJ9yEJmKFHs0ySucVJp2NQvywFB9mOnps'
        b'npnGSiADwIxPgXTyMVTjHAOLTXSlPHNMLi8zuawUSSKnUWvrNhNfIDhGPMuAYmzAU4ZAgSV+4jvOoxbG1zA2XSbKErFLjE6i+yA8VF0uAQ4g2Ac1zTWCn75obSgt2jom'
        b'WNALdFxmlKurdCEimLSH4XoxasMPUB3zfb1h0L9SMb4L4INhplAvrR9BZmCa+ieocV3g2DCZ4uDrIqkrPk/1LxYdQncJxCoCsMIwFoZaVE6XeOGT4107vMIo8sD3GhMS'
        b'qs6B6KhYgw6XMD8OBrcB+Emm8cyNN61BB9nK3pmK6gC0rUYNBtAWjSqpam3EFwEwGBq6gp+4k4ZgCcuJkKAjCtQBapqEH0nC8qzZdFagTgBslmbo5CYDykMXVtE+o3uo'
        b'WzLWaTF4gvMGhccH1/jOYDOgQeekAPUOgmRRd9cPxGECDdGBvQZkuBaAQRCU+aEOdyO7q/gWoJxX9d4wByfEGhuGpj38cQUwk+CmncDsDEif3I11uxsd8QUwCXjongFO'
        b'xuBuqiiAfS7iJ2PiLZ6Jnxi9QawCDCIxVCn4rCQIX0P11CBEL0SVANkio42IrTGWdngBPpxqtAezwJDVsp6PLx2dgSD0QLx5FbppwLJnV2q2i/HplUwCalFdJFO5VkdQ'
        b'WMYMlAzfy3rFtUwX4gdL8E3mWy4uwX0EKsahiwaoCBb2iXY6lOWja6vGjZRTsFFVrhMu7rhfCF7oIbpHZykxwAK48Pg8sKBQvAnMPJN6dBAd8wXMuZPifoI5C0GMiVaC'
        b'KrY5maglPH3FoFET1RLCjBbcPpWOe1NynMaaB+h3hcHUVlRhTrs7pQjdHjdbAbDElIfR8QiFgPl6AL0zKIcehxG0i+7vNaJd/SaqiugobsaPjb26iY9vw2dfVcXzIslO'
        b'1MzE40L0CgKOfcC+M3AMetGpnUGKHkN7h03NjnFs9I4I3bJIAoG4Po1T4+MSdFQKoKZuHeW6FDdLCK4GD/3EAKyD8GW6YrngGs8D2Ozj5+P7TCBP4AdrqO/1DMeHxtoT'
        b'g0m4ZFCjWIWYi0BtYnQuBNSXzsBBF4KBLUToZCFQF8gMPI6gwhiAr0jGHR06kW2wvGOzQE03YAAxaojbzOB+2wpXAvdL9xnQvhy3U0MJpk4HnMfsEZ2D7klUMBk7IUyD'
        b'5eZIfplYEoWPebBJPWRRRGOEbopUSJCQAeiTdA50oRPXJ1C3BjwMmmcKwnC1mktDtRJvWCGKpx3L8B2YMIDTV1EzG+spkM8GBqCad4OFHnfr9rgl28gMfDoXjm6Do1PF'
        b'MW05AigUYiErCa5WMex7fg1uZWrXqAbRGVOXmaAmBvm7wvSlBwTQEeu1rixE78YQ7IBzCaZqcQs0ER2HtSHwYC3qdjTxeGPwANYdIo4DoL6TgqlqqUC3TuLeUsFcNdO6'
        b'+kSkpwAK95r7mTqo3qUTtQFVCvF9CLcOMVt6Gj0Aqe8tNdtusH56QDWPtJOhLGv1tFeRiiCNmwVI5Q4xAFfxOSZPN3FLEo3e8Nl9hvBNEEG556CK+SR+A1TTY4jg8DF0'
        b'h610L37iSiI4M6kxfmuAImcW3XWBdYUIDh2fb4jgygApEF03DzXBmPBEs9Fe3GBz3U2UvaWUyeZDdCiQRHuL4w3RXspm1kALOhMKBXwOMoT9DagbtIw0gE96xxuMCSyf'
        b'E37AGkB949akD1+NYkM/AVjqIDASo+s7GfBojE+iOTl8YgfqMwX6tfjymBrdMIGgoRDwgOm4HsNmpX4VCGUvvm22dipTqJMO+D5zladDrUwZ1q8zDr3LlN1KMSxhNapg'
        b'y9uDmvIgqBWgi/gxW4G2zaiFyf8JX+24BwvwMRqMMQeWmiiZhU7E034JPWBJSHB8Ex01RMfoWh7t1xYQ565xPdq3aAK+Ms5bOHoiRvU8OsLwUEuJGbCDkKmcxavn0cPd'
        b'lJstRE77TWzQ1RmCHEPHAHehuzNskS6SR6cXbJlmnqzNYWHzLUxCBhKgz6RhCQnQ0ZUoqg/pIGh3xkVmAfEOE2y6UgjlF3Ef69gFGcgoCejl6YZ4fsty5rJOTwVVMSoW'
        b'uKfr49Diqim00IpLUBOERGT+d8Hwq+S422w2eBrKrhWizgMGgIzP5Zko2H7VBNfnju8J8S1v9IjCB/e0HJJMwBccDNkEMzvms7rnkNTdOFZYGv5qOPlEZAVhYx0T2EMQ'
        b'yXTLpWaorYjF/J3oCsfEoXIZZ6JZdVKj2bjGenNDCDH4GYBZdJoa0e1QuZTfiOoMKQzUsoiCQ1QN7r91HNF5oMuvC1aAZCbo5kMm8e0Q6uvlZSJ8JIOZ6MY8dJipaWcM'
        b'qibZEJjFC4ZsSDQYXdIDX3zIQW5uho9bGxIOEKRV05IEVOEv3yYCKFlJ3D1ETuj8Wq0/1QZvUMMx4HocNRqhwph2E+v4JBozEzXDAvfJt8FcQZxLE33N6CzqZt6tdTcY'
        b'wDeKKepdA4AGAtrzazj1lvlzIPRKRo2UYbYbrpZvE5OoypDCAX/0mCJKdBAfAxRkavvXgVcxrKTYzhB7XYOoYjeD7tkAeo6RpA+uiTAkfVaVUR1yTRgHH9fRodQJaNIk'
        b'+EWN4jIBYrOGTljsJmkifE1qyBKtwSxDjFp34XaSJnJNM6SJJKiKWReYD/xYbsWDqBH3+pBDXY74Nu3DYnzCwmQ029eaxG6mxq8dkAnqsKIeXgAQtG98fWpfRR83xKWR'
        b'60v5VKlkBu60pVJbvnuhae6iCV/Npet5TZwN65DEhTmLIcK5s5GagmR8YM54cHAcP4gZW32W6EC3RCKYMWYfyyDKaDI1uFc1Yz25zlTrqEgqXcH08DEEOX0m+tMJbnSi'
        b'Is4R4kcbQHxCqJ+/tNvESedAbD9ulEynp1GMWoPRLaWUJf7zfeVWQqRDfTDbjzl0ZSc6SePnjDAzOe7hJ9swbWwXFzLdqpkeC/eFqC6ZADICI46iDlZ0F1fiR3KZYKY3'
        b'W7lLUNRPW1mwOEWuFcWieiajzTDa/UwSbnhK5BrRVBp6kuwfegJIi4aRNlq5RgLIpoqJyFlYySbaTnERvgA2odsMN0ZC2SNicQ55a2cSdg8gmH0AhY1IZ0z/XWeRSxPS'
        b'0YyhCLejKtSbgaqXcyvXm+Fz+ICHUsSMfi8+qMXViUvD8D1cI+SE+DG4Ba/5TDJr8LGUBHw00YwTbIAYU8cH4xZ0VEs2Qv1xFW5LwHXBoKWV6Ky/kuynWdgIHXE/y2AD'
        b'Jrou8U8OTJkRJ+JEC3h0JSh9cY7pDjHZ56GbUDVwOW5m3EVt5nQ83S8T6Di6ZybUyfNkdLdMJOCqzF7ZLRPT3TLRa7tl4td2xER7xYbdsjeWme6W/WxUACBJYfKJJbvC'
        b'GkVWEd0OVuQVqxXbsgoLcgvKyoMmVJxAxLPNaL8txUVlxXRj2c+4Fa0oAG7bsgoKs7ILVQGU4RKVequhAQ15bgKr7KyiLYqc4lwV3ZomXCk/jXarccs7KyenWFtUpijS'
        b'bs1WqRVZakMVVa4iSzOB13ZVYWGQ+YRbs0uy1FlbFQXQzGxFRj7b9Sbb4dljXILe9EB2Qc5sMsxNBdtURQHsKdLBmPjYCT0oKHptROSTAxOj2lFGhqDKyslXFEMl9Rsb'
        b'omNTl5s2VmbsJkzlP99OGTkAYOAWpEjSasrIGMm8p6cEhofOmKGITkyNi1aEvYFJruqNfdOoSrJox/zINz+FCkRDm1WmoucJNm7MUGtVGzdO6O/rvA39ZzNORcswFkV6'
        b'QdGmQpVikVZdrEjNKt+qKirTKKLVqqxX+qJWlWnVRZrZYy0qiovGhDQA7i7OKtTQ22SStxdoXhnMhB1iMff6DrFt8mIWEXQHo2uadbi+VGxIwznvoJu/a5JdOTDMITbz'
        b'VLs38OEc2yK4k4Suoepl+CAQq7nVTuggrbze35wDbtKBpbsL562dzraP18ZZc2BeXCp8d1lklK7kDFjkCOrURK2UCwwJJLBCF5XWlPs8fNpZM2/KeNEhNbWY0fC1VoM6'
        b'47cLObZXCdHJXcpuDgSves1ab2uOPdMCuJntWoTjTrKFFi+3FDGrfQ7dExn3Iqoi5KgeHVCLGYpp8bamJRa50XKI0p+UCFmk3Qz447wh8wXOqVUOaPFGqZDB/dPus2lR'
        b'RDpEntUQQZ634A07nAdQD+W3ADem4d5tUzRmLBRqwDXoFDPH52XotmYOmO9bPMt/1eOj+ApdkkARVOyVWGiFLEfUFI+YtwnAl3CPvNgJd4uZuzmbacj6g57JcQs+Tyeo'
        b'nyReDkFDdH3PSl0gtr6soGM9DdGsDc9m4RE6vleDH+KD2yUsZVjP5dGSONRvowF31bzdsDF7NBJ3K4W0bCY6gKo1rujBWBnu2sj4PZSQDbUwdGqspSIWmU9CN4QacCyV'
        b'Yw2hq+aGzVl8cqZmOrjTXpEhbZmM7ioFhmUqRfc0m8H7jRVOWskwe/WsyRoISdpQDcdi/VO4UUhl7sgyduBEH6BN7Atdz6Q2HNehxvANi0JEJJIGmNg5p8A28cdCzSSY'
        b'e9XC3bVpj5JxiM38zN3b1ud/+4CNvfAhX/y2PCSk7XfTvZdVvXPcN+a3uufDtlsuBpTHt+pnaz+N63FYfe+zX71/7nf/8rcDLY63dkq3y+6lH75Zt+/jxQP7zOt+3rHq'
        b'7y67l9d9b9XhnZ6h+361oLBq1o2WJvfPnVf/8IDW0ePX/36rsPzxnp9978fafx+9tn3Ycsf1jbxl/5E72fyWw4rDbam/fuqz8Oplhf1p64e/yYyP+SIhP2NyREvcoSPz'
        b'4rD57z9Zrm382PrX6xbPrL3/QfRH8Yu3u2mdY+/rEzs+bSj9qTT+478EZPwy22VH/7nlP4x695THoiXr5H9aFf+vq636s+WnP5r7k3OV68NyMn4b8C399+M/C2zclPif'
        b'f7p4f+u23FvLLst/2Pzys1+e/YJzdMnV/+UDpeQFkdflW5f7B/rGBQo4M3RKADFDRSC6hE6/IBuayVtwnb97QVB8gJ8yCNcHEMjjohBtEOE7L9yoCAKwupKQEoiq/CJT'
        b'KASRLxPgul1BL0j+Z9JcTA8T+QUG8cD9gGAZbg7HD/D+FzT5UJtJxMpwGGg7O8izLdAPHw32cRBwQeiRGPft2UE76Q41K3F1UkA8SUCaRQhQa4LVWs8XCiibGuWXgM6m'
        b'such+qtPXEowkiM+JASN1+co5SMCX6Wabpt+nYuGHL9RKCqMn88d5+api3eqihR57LhaEHHD80fMqVPIJMROk+8CwmItXF9WcKOpYs7BZZTjLT2HnT302mF75+bZDbOP'
        b'zW2aq1s4bG03ysktpw87uTYXNBQc29K0RS8ctvcc5SS23m1TLwV3BHdPHZw8c2jyTHprVCBy9Bl293nmHvjUPbArd9A9fMg9vFtzp/xW+dt2b6cPzowfmhn/1D1+wD1+'
        b'eIpvW+SokPNYyr987u4z5B4JnXD0Gb8MT5raom3Rjgrh+8uXL5+7Tm5xbQvvkgy6hgy5hkAVW+9hd0VL5LCzFyGmD3t5t3m3RbdNac3XLxm2dhrlbGFMbt7nAk8Fngxu'
        b'DdZLyNjeanirLWLQ3nfI3heGBizo09NTebi6GK/PSdOjYnrDjHNya85syGzLGHT0G3L0owOFpwamzRhwJj+0nzAQl5nPHV0n1hTRmm1bBpxD4WesYthzV89zk05N6nIe'
        b'dA0dcg01GYu9MyValnTNH/CYBT/09sthW0e6RC1TW9RtfIu61bcraMAtCn7Yojm5tYS1RLeENeXryNBbCgasp8MPK3TwbNk05DDtmUPAU4eAroxBh7AhhzDdomF702W3'
        b'doXuWkYMO3s/cw546kzqOYcNOYcN2IQ9d3BpsW2xa7FrimvZPugwrcuhK6ub78q55gqs9Pyws++As2+X7aCz/5Czf1fZU+fwAZtwDYmH3pEGRkdx70SZx5gJkZiHqxqs'
        b'Mae0GBERORwRAvgbkRig1IiIYJ8RSWamWluUmTkiz8zMKVRlFWlL4M4/VgcwvtxG+BhVQk2ckJrYc1OxP0GqHoPLS/IB0S8Q8fw0mIP/8uW5lbOuoGpLzZYK+ahAzDsM'
        b'y+10M6tm1cx6LrKuSNifdCipImlYaj0stdfJX46KObHNxLsVKeyfhkQyZ2URXJ9VtEAIXo8ESDM1uCEB7AWuTsZ1KWTDIV7MWZUIo1biSi0xceIy3JuQCIWoyQWiKH+e'
        b'k68R4BvLkZ464dC85WOh1210ng9GnctyjAdwyUdkRGgVJHwSsPCJBk8chE5meSIaMgkhZHol3NkjoiGT8LWQSfRaWCTcKzKETG8smxAyDfOvhkz0+KxJzKQu3qrIMkY5'
        b'E+OZibHLK7FJxj8IodSqUm2BmgHnEpUawqitDOEbz/ROxLgpRugLHfFLgxYLtqoWqdXFaj/KLAtKct8cGZH+ku6y6OjVQbwxLDAMij3x6gjf1ASJpRYXZm1SFLCILqdY'
        b'rVZpSoqLciEEoCGVJr9YW5hLQgSG9mlsZ4jn3hwMLCogQx6PPSDOzFKEBZZpSyCmMEQYdNYgNPIlNQJIQ8qvGRqIk7VzSRHuysSN68kx2lcP0VYl+i0NQFcy2HlaciMl'
        b'MT6J59BVVCWfFYF6MgpmHj4h0CwDNj2c/vR3w860N95ueXLoGG+V5tLMl1/92eSkmjPX5Hr+7Ce2bY33GpWHC1zDUyPDEwOOVO1vP9F+oqfxgu7CkfYjobXKlvYj3i37'
        b'wy25n76wijn9gVJAHTq66DlFvsXbD7QNV+GaJC3FBAJAm70ifHP5Wy8mkUqXp85GPbg5IWgpoAKALQa374b6REW5bynNvsKamY05d2rHRuTsGDlz46YE9eOpHPPjiyWc'
        b'A3Fllgv5j5wmD0yJGXSKHXKKHbCJHXad8sw1+KlrcLf07vS3IwZd44Zc46qW6hbqp1IHz1tOHnZ2b8nQ7xyw8QYPpEv4I1klZqolI1Kj4I5IDCKoJrhHTUyQ2n1i1yXM'
        b'EJPeMxvsTWywaZ+fkWrbDUYYur3FjOenEmP6FZdvzNQSwN4iC+JuWM0VaueQ5bpUuJFlv9bhSyYJMJI+PIRuoRrUFiBcnxCB6krRdXQRPTLnsnGDJT7j4sgOPwFsbJFv'
        b's4I4DJ9AjVII7tLZaRjUZ4c75dtKSYmudD4EDb7mLKN+HjWu0OB+a9yBz4SJOAFu4J3m+bAIpGrBAk2YWsDxxeixIwS/+Aa+TEs2OnDybdvMOHJk8fEODp8CHbhgOHVn'
        b'gQ+ojdbeLB1sfVMmPfeHO9IBj9Ism32USY6tHTexHYROfBPd9QcnwnMCVOe4iY/d4DHBS0iNyqrjxpNs4CXEOmOaTQbewjxPOuYtXk2wffPe4hB4i799WYKNmrmJ6bUv'
        b'tZXErpLqX52m+pLsEXn4fz15lFNIu6VRlb2eLnqlg2ReinNytOAWinJe76gxYbQoNVoRC+BLTdzGQnCPOWXF6vIARYk2u7BAkw+MsstpTYMbi1XBeLIKX+MXA6YjyKRv'
        b'WWRRtPQdG7/02Ay/APi1cCH5FZuSFgq/oXt+MWExtCA21i/gNY4mY8oq1BS/Me1FBknnuYQlu4BrLvFg5SWvTCD5/FPYYIxjccnrkIB8/jlYMGHxvtFs2xiWM3Gp1smL'
        b'tfOIRTkHUfP+r3Kp+K7H617VUUwTHLtkLC0XMt9dmF0WyzJt63fZc+SwREjRX5Z9T23BMZN3PRffsEZtqJqjuTpUZdikskVnbVE1OfeHOxGYEoE9L5uC2ykn25UsZxcy'
        b'w8xcmxrKKQVaW2KbrkaJcLV/OHwN5UJT0Q22LfAYAu7zeag2HMYcxoWhI/g+5WIfbcOBj44KmbZ+1odzlIQLPdNYtRS1RqCbBja4Kpkyn4/upPmLcS94rFQudTe+THlI'
        b'FCylGLL4T5NvBW/mMgqu+IWKNR9BUVic7+FlPeYoxObRupHO6weiqq7efznvzP2PFVKry10Hgw7ge9VbLgb9LT5n7VpLXuj94Uff2xUcXP+JrMan4b2PCrz7/O58+vj+'
        b'lC29v7jb+pt/q/C+dii2KmWPo7KkMPRb/+L1Z8GD/7D78+YF195eKDDf8WA2incqcZB69PyyU92q/eGWn2zqXpa66IOXf9+y90zZLOnVmJl7Pg4c+X9pXxz6pL80/0SN'
        b'ww92mR198MX3Vddj3ToP1OlfOCeoK8I0j15cbfZ8u29VgVPRjMl7cNb7T4988jCi/wf1/XMj3vf+KOLmQy5y7ayLf6lQSl+Qud27d7J/oC++5GfMuQSGaV6QMyjiErnc'
        b'D91f8mbcg+rQ6Rf0Ha2be12JL0FVKSTxEgx1Akl9pJ+UIIG5bzOLj5nLgFQ3OYEjT8A1SgMzdATVCDhHVCmSRqDmF2TpLDPXJ6Rk49ZA8E3b+Gh8Y+ULkonbqFlFUjfA'
        b'3TmF9HOvwA/fTXxB3NmG6GySikFnwozZGKs1xTRfZI47l+Mb6FYCrk0YSxhZhwg3Fa1Syr5e8oUEa2O5FwbRZCzKBJ+yc/wrhWeJPINnuwGeOZvE23aOzcoG5TH/Jn9d'
        b'LEVhMksfCL5J9B/Hf+Q2bWD64kG3JUNuSwYclowKhLbew16+z7yinnpF3bUf9Jo35DVPv0S/5OVH7BGTC00YtESOCuE7SZvYe+pnt+S0hQ/aTx+ynz7KCWx9ht0nn5tz'
        b'ak6b5lJ5R3n7rs5dLE8znnV5bu/1zH7qU/upbemD9sohe6VposBOp9GHV+2o2dESdnSvbm/blLaszmldsR2BbYF3hU8s7lu8vXwwKmEoKqEt0PiEPrRmW4vrgPVk+GnL'
        b'6fLuzOuWDUybBT+GGk4suxHeUtpm26JpjWrbfmlPx572fZ37nrrPGHCfYUxN6SM0RHlvOEaLuHdE5tF2wndsebgyrCpnwJRsS44IwSu+CaJ+aTrttfQB2SA2Wc3fkYrV'
        b'48B1tYTnJxFo+l+4fKN5g1ZZGHfLKpoTKnlqaRfie1PJhuwin/H92BBcPeFdwzF3sYNjoT9911CUJxh7p/AVuPbf807h5+9P8GhpzCN+SeSaRwNPir1MNzr/t0P9L3XJ'
        b'wje4ZLNk7VscPXPUaf3Px7i4Ad0yemR8FTM/uBT343by/l+vo2EPLa2InoHAes+EhJRAfDQJ16RjXaLADl0KXoQuo8PoAjoJX5Rcqo0E9c/TFpzei0Q0Xo7SjJz+bgTE'
        b'yz0tTy4tfSVitpDrP7Hd6Gpz88gf77tU/Lql+3JCVkykbf6kOQ0B4Uf21MhXdZ/80XcqroRBvOzJpU6y/aDyfaX4BQn94nejWjmLlueGve43rkXRFDrqw0/mOuAqk2R/'
        b'ID5jSe32HAuJv2mSHz+JpXl+3KJ8Qd6hRhXrMk3diGBqNnMi6CKupal+1JOIemFCrELALY1vBMzzVwpMTAAx1kZrLtmkKqO23PiFWvJsjlnyvdIvDbQn5M5fTTbzlrM+'
        b'clIMeM8cdIoacooasIkatvd8Zu/z1N6nLXfQ3n/I3n/Awl9N3C0zZ2I18XZvjLNJBmXjeJRNXkcZ66wLKLpmCzVU0NutUp4nMf6bL9+UIfojAU9NMj/uilWU8CstjUjH'
        b'/Y9amnywNFcmKGp6SWFBmWbMnLA9dbAZCnI3T521ie6Rv2JajOYpSxHxxuzXhMq+sSnLkzPSVgcoYuMWxSakL08KUEArCZmxKQsXBSiiY2l5ZvLypJhFacqva0UoWH1a'
        b'yLYdu2dtLXRbJeG0UXBzVRmqJy+4o05/f/LGeVXisjga/tPgHzco0WVzdLIc/sejqnJygtEc6Sbjanbo9gE6SF54wjXGZ8F+0NwVbpB74S4R6kAPUUtBdtJBsSYfHvB2'
        b'eZfZjXJeOKPbQrcSl6///pnvKy2UNdcTG0p61hxxO5J8MezdyV/Y5R167HBRVbPgTE3IXvucZPn0dEthzDPBtMJ+bdj5X19RXcsKWBzZ7PrRh27vir9vsYq78r2DrlE/'
        b'4kbPOWUX71WKKD7NDksnNsICnTGaiRBfutu3KildnhCx0sQMMCMwe9YLekjpwMogtkXXhG4bgSGqLWfWpw5XzksIzsojaNXXjJO5CFC7XbFS9EaoQOR5TPFGzCEC1xgy'
        b'cybfqb3YZrAXG2Scg4uJXfiSvRpqG94adFow5LRgwGbBV+zahEL1Nq9Bp5Ahp5ABmxC42zy3Ye6x+U3zByy8/0s2JJbYEJMx+E4wI0my/wkzoib5OIAxxHVsxVdiCIwB'
        b'Ua7G9cHoKLPdGeiR2z5RPnqY9mYzs5uYGZER0JA/nWDYx/ifMTUkM7X+1X0MU1xDE/5FWVtpDuQNcIZkQMhBnRIV3ADYMxFgxDODU5hVVqZSK3KyAJtMZEpRTlYu2yp5'
        b'LZUzgddYWuersjosi/N/CWZJ2WYCvofaPb/mVsJte4KytpVTC3twpSsXsrCOBAfrtDbJHE0oZFqVAOziUGcGg10ea9nJ4XZ8DesnAq9F+KLV68BrGnpCub+zUcJZSO3F'
        b'nGKjRaQsnCtI/OEisaYESr4VdZZtX1x+dfsi0eLM98/kdygT/3XjtmP5038kmPqRtOLGFBffWxWy099VLXjo9v6n2aIrOe9eDDrs+uOFbQ9mHctd3X33tBh/dK2hxPP2'
        b'gifBG7+dB6b3/gezwrk/nPlWv0f+DkulGUVrU3Z6y41bG3NQ3atorWrTC/pmy4MlqM8kyk+he5SoG+txHXiNJDE3M9lsL4+aaLCObruiQ/4uVibQToROUWinxvo9E7Ad'
        b'l4r2E2znP/+FFzPMPbhjArjjtuE71LCX7npB3rcCb9SOmxJYNzLwY9ITYy8moQYRPgN4uRWs4JeGfsQKmuy1WFAQBfJOtGnnBIoa9QsGo77Y/EtBIA2Q5wxaTxqyntQW'
        b'9tTaZ8Dah26rhz11DuueM+j81pDzWwM2bz33Uj7zCn7qFTzoFTrkFaqXDztPfuYc+NSZHJxwDh9yJgG57byP3KYO+MwZdJs75DZ3wGHusLtPy+y2LYPuYUPuYd2hQ+6R'
        b'einlHvTUOahrx6Bz1JAzwZYmPkAyIicGPbNYTeDhPw6K2Q6Oye6TOon4hQkTMZt4Bq3RM5SCZ3AlXuArLt/oBs4JWQB3zWq2UClMTl6s5BcrBcmLC9wvLRFq2mGZUpc9'
        b'rW341Ur7ZTbf/rjI/F8ddsq/fUS867Phnhyhu7nfTsvJR82XhUxzWtjr3v1LhdOQbtreuC/iik/Y3LLtON37ZM9nP/jwXvis4oi3ukS/jV4y4FpWW/UzwaL3Yvx/9Iec'
        b'BpvSx43WnUXpf/jgWajr4d+cNa+6lpju11t1cvm7iS2b0n00WaFnL/x6aNePpsd8Utb/eUDu2eB7/f9v6rw5uPTWhuL9zyLWWx/tebetM7f80B92bf70UNNvuke2fCd1'
        b'pPa7v5ktvLhiMFhrHjWtUy9PvquvP1CavqBM5tDhG9Du4pOr/O576gz98ZLG5V3TtqQmvP/OOrXXLxvlqUuCvjVZHXpC/6dVS4OwWi1e0XC1+9S6g7ezquZ/+mLnpz37'
        b'P9QlfZJX6H1n2i+Gj/w2V7hNP6en+sPaeZ9smHffuvaTvR4K65/blLssee/8zr32dcf+pXRywKLG5OmlR/8zr09/qfTI3GrNJ+V9Dc4lxwpj55THf/bXW/M/c5w3sv/q'
        b'J5GP3J/P/o/o6eXC9Z8klTXeKZnzb0MH53z48bfn3XLe0+n8l+9I/n26ZFT/4me2//HsGT/v81U3X4pSvrPJZeq5HN3u/c25qX//LOPRrsDLtUtLphzKqnnuuOEXlj/9'
        b'+Ud3A/0Oe5ya0lC67+I5l4937HzmO3L6g1xvQdqCP1f/PSPjU/P0t3/TPOWXJx32Nn7skZO87uxs2XtTInd81rznJ5+suVqzKm/oO+9+cHnWX9OET6YErhF/pj32y5/s'
        b'+3ZVSc3j3/fN7Njcvnml5+bLa27cn7uixkr57o3aBxU+5zeU/jy2JurHmn/5Ue+Udzdf8HLN+XtX9pmtVrsj3rdNC/vbqOzc78W/ePnrnmmPVeV/X+F4v7mkIezHP4h/'
        b'/Kvfeeeeu9Kqc5mXHv5Xl1v/1uodXPnT6L8tLNrz3smf/P2vH5wLj5qX99fPl1jP0Dm17/iCezsrMOLefrC3JFtJXpZoBYzDY91Mjo/iwFHdLqFRLd7vYT/B8KFTFgzR'
        b'OuGDNCO7F6D42TFrnWQXM9FY26NLFBgrcAd5IweQb20gmOjjZpzZBsEU1IxvUxOMDuPOrf5LA7EOHd4an5gs5uSoR4DPoINF1ATboSrckEAcaCB+shEcZU08qXJTgK9E'
        b'4ptKj693dE36ZZevfQDujaaLHJoZwwgLyKdiwodZeGlmZmFxVm5m5s6xb9SyX5IYDgZR885zlo6jIonMmZnzsKrtNdtbvI/u1u1u0bRo2sLasjojT+5s3dm17NS+ln3d'
        b'U+Gf+q53n/busr4dPUF9QW8vfHvhe3bvxH0r7mlY4kBY4kcuBPVntUaelLXK2pYOugR1Ow+6RA3MTR50Th5IyxhYvmIobeVT55UDzisJtLc7VtRUNGAzlRwXW8WPmnN2'
        b'DvroJkddjC7m5aiEl8Xzw3aT9IEXLAYCFw8qlgwplgzaxQ3ZxQ1YxMEIRs3N3MxHOeNFZzXqwNm5Dtu6DNu6j0pErnAbLjrLUask3tF82MJmwM5nVEi+P7ew0QePisnX'
        b'UTPO0hYICSWkjJBRwpwRckpYADFg5ztqSSkrSk0dtaaUjaHMllJ27DF7SjjQosBRR0o5Ucpn1JlSLqyiKyXcGOFOCQ9DPU9KeRmoSZRSsIrelJhs6McUSnH0OpVV8KHE'
        b'NFpBOTqdUr6G3igp5Wd42J9SAQYqkFJBhueCKRViKAulVBhrIJwSEYyIpMQMQ72ZlIoy9HsWpWazinMoMZcR8ygx39Crtyi1gDcwieYpHcMb2MQyeqGRXsSbDJpdF/OG'
        b'bi9hZXFGOp7RS43PJjA6kWf9SGJksoFMYWSqgVzGyDQDmc7IDAO5nJErDORKRq4ykKsZucZArmXkOmO/1jN6g6E4k5Ebjd3MYnS2kc5hdK7xcRWj84zlm16fknxWFjpa'
        b'wMo2G5rawshC42xvZXSRobiYkSUGspSRagOpYWSZsR9aRm8zFG9n5A4DWc7IncZe7mL0bkPxHkbu5Q1isI/RCwSG6tECJgcCQ09jGb3QWL6I0YsFxrVndJyRjheYTMdS'
        b'AWc/edjOZ9hOSa/exh+f0dWCVydPJxtdJ+Dcp54LPhU86OY/5OYPFkUWTC9VS3WxesdhF59nLv5PXfwHXQKHXAIJVA6gl2MiPa8PHXbxPGd5yrItq8t20MV/yMVfL9aL'
        b'hx2Cuh0HHWboFg17Tjq35tSaLvGgZ9CQZ5AuXp9TlaxLBpNkbjMss9E563NaNF2x3bkDsjmDsjlDsjmjgnmyiFHua1x+L+TM58KT5LdNjdOoiBTAXBtaaJnSpukWDcgi'
        b'B2WRQ7LIUYGtzGWU+5IL4TEDao3xIgXTOGfX5s0Nmwe8Mwadlg85LdfJn8usWffT26Z0Lex27NbeXfH2ovd8BvxTB2TLBmXLhmTLRgXTCNevcSGtpvHw6FjzpCSVH5+s'
        b'AZnboMxtSOY2KrCQwTq8fiGPukOFMRakwOONHKxkk0e51y+vcSAFirHpTB+QeQ/KvIdk3qMCO9msUe4fXQiPyVB1jNeEUnretyr6rRg7Dtm5xQQYtv9sRgSZmf/snt8/'
        b'AyhsxmOhiSBCvZwERWP4YQrFD8aAKJbneRsS8nzjl29027BNNoPrt4oWCQsa7H/Ea35AZjD937X6BPmBBQ6HP3uYWOskjllUvyj6ra7jCVldSXd933G6L3/4/vyR++pf'
        b'nCtcsLTp07ff9oj61YNfvb9r7WiMwx+EpwruRlu5ZljoGt/73fq1S/64/d8Cco63hZ36S9qHF1+m9GzriEiL7Xy4Ytbipo5TqddGfvrLm5NVm+7npnx3775r04Xf+/N7'
        b'Zw+UfN7U+/HPbYed0ht8K7/1sqwi919n1ZVkfvAWN+XdGYOb35N6n1DOXSRVxtaZe5aV1gmcXZ6b+xSVVP7n9xLnBD8bbTj3zoO9vJtL6DuqO0rLFwQQRruIyGEBD3Qi'
        b'JQXX45oECeDXWwLc5YAb2GnNO/hydkIK7kT6QNyDq1JSyKECW/xQiNotUDWtsxY38qga1eN6klpAteRvT6L7Es7KTuiF2xJZouMMbspIiE/yS5K4owbOTCSQxmP9CyJI'
        b'Oetxi/9S3CAWc3wCh1veQvUv6J8v6svYRvIVG9aaJqhQXXACYPk68lc1hdwS1COB5vrnUtSPTqM+/JimtO6tMH3IjHNeKPJDjR4UtrtYTU9ICQxajapMWbmj0yJ0cc4m'
        b'mhL3XoUInxobfCgBV0s4USCPrsvxcfr8ImixHVcrAwH+15PkGO5CV3nOeplwOTogp0c9fHEtPmKsEgB9Rjp0l20a8BB13BZzHqiTxjIOuN3FPwUfwFUB+ChpkiwBfizA'
        b'd7xQP21u9xIR7sU1gdvKsC7Yr9QQyLhpRehIIb6knPzlIcQ3Ejh8gxfNZBqDvBZ6vPIZi0QKigrKWCTCvtFIpIAfO2TgxontK5LJv2FLh2eWXk8tvc7sGLT0HbL0rVg8'
        b'LDKvTDyQOGDrfSFqUBQwJAoYEAUMiywr4sk/8JVuXgMip1GBuXgNPyx1HTD+AHz38n3mGf7UM3zQM3LIM3JA6jYstaqXH5X/2GHaoHT6kHT6gHT6sNTumdT9qdS9JXpQ'
        b'6jUk9RqQeg1buz6znvbUetqgte+QNdnUlAFvC7v65KPJA+6rBi1WD1msHrBY/fLln2w5C+dRTiAOGb8MO7rqzA0tDTgEDUqDh6TBA8afUTFUIcGL0xaRGAz9f/N1jYyz'
        b'cABbSN9TEYtiZnBohnesmxC78nBlHmXSiLBQVTQiIicHR8R0z29EVFigKRsR5RbkwLW4BIqFmjL1iDi7vEylGRFlFxcXjggLispGxHngHeCXOqtoEzxdUFSiLRsR5uSr'
        b'R4TF6twRs7yCwjIVEFuzSkaEOwtKRsRZmpyCghFhvmoHVAH25gWagiJNWVZRjmrEjCbpc+gZbFVJmWbEdmtx7qyZmex8Sm7BpoKyEbkmvyCvLFNFkucjltqinPysgiJV'
        b'bqZqR86ILDNToyoj79KMmGmLtBpV7rin1BAbt/EffRQK5vdyjRfyJ5k1gbwxZP6SD0iwLc/nC4n3+r98/cYcLwEu75jLohXcOwqr6CDh51LjC3sjNpmZhu8GVPG5W97E'
        b'vz2vKCouU5AyVW6yUkpelMotzoH1hC9ZhYUAfXINVoUkaeG+OYiOukyzvaAsf8SssDgnq1AzYmG6waImL1RTSWfZYrLEn0vnsr9tP19NDjuRPTbNHriMCgHWjApEvAhA'
        b'PlwsOLllhWTUbDFMxyhnck0z52S2BsOxlBkTUH4+ciBg/tvT3p72ju+3fAcClsLPsNRm2NxJFzDgHD5oHjFkHjEgihjmbAY4G73LIOc2xLkNGH9o9/4/y1p9JA=='
    ))))
