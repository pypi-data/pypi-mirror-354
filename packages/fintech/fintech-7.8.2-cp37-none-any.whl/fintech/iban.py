
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
        b'eJzNfAlc1Ne1/29WlmFTEVFRxzUMm4JojLsihh0RxSUqjDDIKALOb8Y9bgjDDoKiiAvIIosgiwiuJOe0eW2a9p82L6995LVpX9OmbdIlyXt9L+n2P/f+hgGUtOn/38/n'
        b'PfzMMPzuveeee+4537PcO/5UGPWjoNdaeokr6S1N2CnsE3bK0mRp8vPCTrlBUadMU9TLTPPSlAZVrnBALQa9Ijeo01S5snMyg4NBniuTCWnqRMEpQ+fwRbpz5Pp1cdqD'
        b'2WmWTIM2O11rzjBoNx0zZ2RnaTcas8yG1Axtjj71gH6fIcjZeUuGURzum2ZIN2YZRG26JSvVbMzOErXmbG1qhiH1gFaflaZNNRn0ZoOWUReDnFN9bLzPotcMemkY/2n0'
        b'ZhWsMqvcqrAqrSqr2upgdbQ6WZ2tGquL1dXqZnW3elgnWCdaJ1k9rZOtXtYpVm/rVOs063SrT/oMvmbHV2cUCLnCqzOPq0/OyBUShZMzcwWZcGrGqZnbSTq0zvM6RVzq'
        b'sPDk9HKl1yTGgJILMFHQOcdlOtLnTzPlglI46igXUmJappkFywJ6CA1QAvewGAvjYxKwAEvjdVgauXVTYAL0qoUXwpU4eAiKLUuoK57FJ1BOXcuw3J/6Y1lELJYl0aDi'
        b'heuhNyEiIBpLsCQyBosiVcJhKHfadXIOn7nfTy24CGdCnbUpmd+XrRYsuxm56j1G7HVyTYggkiWRWyOgwxcLAqJi8UKiIxZGbCXCY2fyjYjBsriY+K2+0OpNbQULidWE'
        b'iKitvoERkQEyaFMKZiicvBQueKfKRqmT27BENv6NLUl3swldViAnoctJ6DIudDkXuuyU3Cb09NFCd6JX7HNCvyoJPWu+WrgTP00QaOlG8zKBP4ybKxd+EcnGpWQ2TI+X'
        b'Hl5PcBR2rdXSs5RMhf6U9HDKPpXQuNmDTCIls3JTgNAqZDrT4yD/qcr/mCis/d2kY7L3tq+O9578hZDJ6E1LviJ7fHqvO/UP+TdThstvpMfTfT51157wmyXf9GPZn7d/'
        b'6PttYUiwBLNN6MAbWEMbULwwwdcXi+AJXlgYEUgfWrf40laUBwRFBkbFyoQsd6dVUIetFk8aZcabWCgePuhCUsYrAlQrIc8ymWnTGWyGChEaXE0qaioWoMBollrOU0uR'
        b'aISHJgdqKRWgaNpk3oKF0VPErXAR77M/KgQowfqpvGUWlMNVcXI4lJFUsV6A6yl4wTKFUSuGXGgWqesDKCOlx1sC3Di1mjOH9/Fitrjm4CHGQTnNA+dmWrzZoEpowpsi'
        b'3MY67FZT4yUBKuB6jjQqNwpuiDigtrBhF2gG/STe4ESc9Yjz8aErG3JTgBrLUs7dHqzOFFdBP/Yy7i4TLScosnhRy+pMuCjCwFooYYSvCXAVqqGdU1Mm4z0R74RqGNN1'
        b'RGwXXOVjJmAVPBWhP+aIgpmGAGV4Ac7xpt0wgPkiDkKBuyCNurICrbwJn3rSVvRC8T5XxkSHADe3Yx4XEV7D7p0auAGP+Va00yi0YoWFaan/2g0kwVrIpw2UOQrQ6aXg'
        b'3Fle8hbxKU3dwza2UoDy00HSPEUzaHAvNB61KCRpXzTSlrMx8+H2qxq8loBdbJq7tA+xr0oM9EMVDIhYv+uIXKJWBNfhprTnpVA9SVx3EPsZ2zUCXJhN5BhrhsWQK056'
        b'xd22qVexdBUfMfVkMPbiXex3ZC2NAtTi2UTOG1Rq6Xnv3HRHxsBtYgDvwyPOm3syaXbvLIVZJc1SfhJvSqpQDj0ZRC8fbrmopVHXaZd6bIuFPFKR3v1eXL9biKIPtPA1'
        b'GbAJb2PvYVfsZow3kOqTOnVIayrCSqjB3iBHJzasU4B6sxsnGASPg7A3HfudbCK6BQNQy5drwcqF2Kub4sTE2kVorFgsEXvqtZ3AEe9ZbFp3gZSJj0gI8cDeAztdZdKA'
        b'W4tRMr2VcEGkFZ3Pxl7W1EYSMuokYyl0IsvthYsR2OsgackNbF/OJQTXZ4RpNrpjl43l61H4lE8DXTPlmvjTjuz5fQGaNqOkp/DQDzs1YJ2MPYxWH1tM3m7edACunNQw'
        b'6zuskmapgUK4JVl/D1RoNZ5wDe8zuXXTRCfn83kWxeBNjdsxvM/W2Uv6++oMTswVbhs0G6EX76ukaepxEB9KMjuC3eJOeGBmvBUIkB94QlpLzxFs1XgtZRjMpHxFg/2S'
        b'MAtOkyV0QKUzm+SBAM1w76hlGhvSDk9iktKgeClWQB+UqAQF3pLFR2GjZQaHJrSSqgzSxhYfxotQCkUqQZkhg7PJ2GaZzfAbirHT1hiCD7FqmI4TlMqnwN09OgXnGfug'
        b'cwIW0y5nk551CdkTEi0TGAO3zNAYTQzvxQenhb2zD1omsqcFL3hEE69pcH8DvV2CLosvPfaGvmyaoQDal0KrSh8LpXgWrNi4PwwadsYKoaKKuhZBB+8MF3ZAxXDvTryE'
        b'F/nH7VAfCu14SSn4YKnSaZnZoqPOi6Fzn9QX7kML6xwBnUtFfDTcF54oFeSPL1peYKQHZhwdptxhp3wYbofCHYlypVKtyuTxRcB6aMaqCLhDLNu7umFpCJuGugYqcGCX'
        b'N++65MgCO798dfB4P7bLNVoshpakSUKU1kGzfY0lgLoeh7O0K88tDu7uMBO00Ic2RjzQpDq0fK3k56xQdYQg9iw22ngpVeyVpoAGvEoyhGISYQQ5AOzDC2TS89hCq+Bx'
        b'zGjumVSUm4XpUDgFexXYhX2rLS8y8rUe5ItGBEg8eE0cLZxQaIllVO7EqvfGCofgriM8ENMtgWzZhEJn2SSddhEpoJJU7xLkp5MyXRWC8aY5TUWw3Lydy38BXpeNkT8b'
        b'ewhrQ6Vl+0CVAh9nOln8uEOFs2HPS0qJVaFsNrZZVqUDNMKAJYStuIg0tReqcWBkTOmYeWwaEXpCRWBXBg2SeC/gTbfZ2GPXzpEtaefjQ6XtDsFyFWGRNYprHVzNnDpW'
        b'6/iQNXDG1t0HO5SO2BzL5WTynPoceRp3Z98uiUOueoFkoSL0Lbf404j13ieGR7SxEWQTx/DSBhqUD/lauEU6FYtPHEIwN4trFTxRZ8Jg+FgTY0qYu9N3qcSRCDcdsSSL'
        b'3FgQW3Y73Ns63L19lBrCmbgxTFWrxMzFnCeop469iR72/ZPsmGw4TEv6yfQ8Hm84BE3GcstC6v8KVmKeXQVLRyZqxfMjklOSj3mk2h97gJs+5qeobEPa7Ezh5aPDxvyC'
        b'Ah9BF0UkvHPDkhefVXEi2x/KtlwpTMf7CuzG5ml8wYemw8Wj8KxutD6rG4dUcCWeAqX5jH431KhHqzf7FCgbtn+FAu9OWCepahHcxP5h2nftnL8MF+360KB0mIp9llAm'
        b'yf5pIeMxIuk39LjErtsAHQsEE15aic2OWPEqdnKcmUOxQ+6zSIPN3vvDtCohFOpUxMa9NZZFbI4r2RHwAHrGbkDnKLPmFrcYa1VksveXS4PKl0HjiKqW2vWPP1EQZ677'
        b'RSxaIktQOSzDppe5dsOFE3A9mgyqi8MEdX9GPTjEb4ZSh9kRy6SNuw5W/QhjHM54RwZki6FP50+QMQeu884p8BTuP7vNK6AmRFrAdOymfQjFZg57yYSu98dghg33fFZQ'
        b'dHiOtOflJZxqYDg+GmOTfJdzVcObC1YF+cT6JE4Va8C641kW5ASmCx2xn+lYI9ZzqkuSIP/ZfuT8m0IZL4zXLuL1CNRzDMHbmmSbdrXZObhHsfO9EQW7R4ZVy+EN63wJ'
        b'p89g/fOIGDqsRFwgwXhVBTcOwF0Ob3Ae6qDWH0ufE0qoBPbDo7apKKMoxwcSnJSQ16mAB25jbZ0AZcTWN8U4vIS3IZcrzm6i0o21lKWMUbeOkXVJa1oMgyoo3zedD9pp'
        b'plGj+8tTbZMQxsDA0glQsEQGtWuxDnqc41J3cxOIwsGDz3llrJ47bGc6BfafOs0BazIO5IwH61tXjUY4iypndxh3TrOS8PFzeFK90QYN0/GBAnugaKe0eQ8PUMb4vAd4'
        b'AS7bg5RBpVv0IsldNGHvpGdJz4KzIRIP07FTgZ2kKF0cTaBy+R536HsOzEfJPsDhRXyAVdz+sIxU+fYYd8H17ik22lWJqfMgJRelkqtsmQoPxpc89O4kXTm/Hxt2CqYD'
        b'2JTgyEBkJtcKbJySOZ72tasm2pz9HbBOJC8pQjff4HjIkz8XbTFxzaNIZVSwA1UqM7bCNT5IhXnkaZp1483UOkbP6wnu4l6UMOj+mhSsWrViWAbPgV2n6tAS2SZHh6V4'
        b'XpQ8LGUcec+FInBHtZdEECuETEnGVhWU0Orvc9NOgDvyMf6SdZ+8hyQsBY7Qo1RSNFYhacdFiqrHCWETwGpzTj5YpHR0XsX1zrTQ+zmNhl7DsB6tUOATyCOfxBE6PzqA'
        b'Uotzz+v1M/aMVSq4dvqELkbKYlqwCYpFr9X2zAPOq6SsKI9YrRTxKrTzXLNQAKsQw2N5t5eXiFnBeE8mFTfKPI7xDJSyxTN4W6RI64m9ikIg083JbTwxW4TLxHAJS3Zv'
        b'CHCN+CnnicTEVErRSwNMLMexMmBqDpPqF+1Yt0OM09vrLj5whdPKpqhsUMQBqLMXXuCpK2/a6wnnRchzwx5uAALlMlYok3LGms2Muwdw2VkucXcJb2IBb9tEiUCuiE/3'
        b'Q5FSSk6vwUVolHLnErw3SaQE68FIOWeNG5de8E44KxLDg26M4lW23k69JNfOQ9AjRmDuSKHn1Co+1fqN2CBSIHxmpMpDfraKC9bLlCmu3Gav8igoZ+PJXttUGBDh0qKR'
        b'Gs+G5bxlv+dWEbuSsNtBqgZcJBzo58KbEx0jkqNqttd+8FwmHxKVvEfEDsyz134oUr/CW3SkLgVion6k+pNIuMDrHucodmkQ4e5pKd2+zlaaG8h3T4vN/sRDrL3845HN'
        b'nwdss4gJlKEMF0qwa5+0q2fg7kzxFWg4opLWUhpwVFK4q6/CTVIEr5EKCtR6S02De7CRpl+I/TKp/HRxKYXprGku9sJ1cQVWjiqvoNR0hDClTLRAmbtMqq9cIxi/Le1p'
        b'HfTuw95Xoclee4khx8iaHLGBELJ3BpSMFF/OBXABRVLSXIi9a6DKXn1xDJa2+3roTOy1xEs2UcfEcy1JYr2aILAWe9fhoAtbVhNNFXxSYqIYSsKx90U4O1KwGVjPm1JJ'
        b'3fpoZT0z7PUabN4mqfGNfaSsvS+kStWKJlaKK8AnfJgn5pO76LVAr5uDVDBoiCQV4MY5iB3xBG3dFI1xxesRoHkn3LGpONSuYrWoVYfkknzLoWs9364JG8lMev3jDqml'
        b'fa+Yg4VSvakofCoNacTyUYWjh/hIItjruAt7Q+CavW4EHXCbE5zmQgqmhgf2whHe1/EGv1W0PcRghr1wlDBFEu5TVyI4Y89I3egG3uCy2IB562hIJRZZbHKvpLTNxkIh'
        b'tBupsXAzNwGywKrZWMuHzXOC8yTcJwuxzyb4GgoC+3jbCYqUSbwwuM9VLrFehy3kgRjJpXj3KFG8Ah32UhU+jZO2uQQfH8FeEVpcVVI1qAHPb5eMpwQuU9O6+JEqFl4e'
        b'NqzOfeSjexPw8qg61l2zBIvzDJpNeAW71FLDNcc9tjpaYKQmggzaXuCCmulSgavOFfo1bhsc1VJ9qVHczZ+fXH1c45Jpr3uRmDu5xDPMWKo5lWK26WUVdNuqvQGUBVZr'
        b'skNGCmIUItRJFaleHJylgbZl9sJTpD9vSFbv0uBg0mFGrJWwFS6TRNnsK0Wo1SjmHGb92wW4nEkayTeokbCnRjMFCuzFtQnQKun4XfKYlzRw/cBIcQ2fhPHlb18NjRrI'
        b'Cx4pr0FNgqQnHdjlpcGBuSMFtll6ztsJGqLZij1uTASPyel5YikfMicO72ngKTa5MZ17KkBbJDy0FQWJhQcaVQh22+RWP5e0ji1o37YozXKyuW42ZoB2OvaIxDWF1PM1'
        b'UAhNTnJpntukBRcl3tr2Q4/msMpiq2lfpuTlDOdtDZ45oIE7LvYSHzZJaINX5mK9Zj0MirZNuBGKko5inwEfQDE0+EvK8YS2GqqVUgrZRupqJe2oIrlK9T3o4L4/2Zn+'
        b'LOBVQSX0boHircK23Wq8meWsU3Ky8snQjcUxUViiEBT4VJawkTS1bYW0uzggRmNRjFqQ78GrW2QL8XGQZTobRG6xhpK8hVjqr2PHVS4eXpMVkyn7lGyGrKUrwD8uMEIp'
        b'KNfKaMfLoW2dw8ZUdqjEfoh/ftrET5rY+ahV4IdY7ECLHWQprE7pTrYjLGWBMld4VXVcfVLJj7BU/AhLeUq1XUhT8HND5U9+R6J31o76CWMnnKJWn8WPNrXp2SbtYX2m'
        b'Mc1oPhY0puOYPyKlg1W/A9lZ5mx+SOo3fKyqNRK1w3pjpn5vpiGAE3zZYDpom0Bk48aQ2qvPOqBNzU4z8GNWRpXTEy0Hh49v9amp2ZYsszbLcnCvwaTVm2xdDGlavTiG'
        b'1hFDZmaQ85hHy3P0Jv1BrZGmWa7dkiGd4LKj3b12KkHjDdhrTF3OlrnPeNiQFSCNYgyujwwbw4Ex67kVsZ9UEozhqJktwaBPzdBmUyfTuBPxtZmOjZ7MPMwmifKrz2Nm'
        b'h9k2akHaWItoZmtkck+MD1wcvHSpdl3Mpoh12pBxiKQZxuVNNOToOWN+7JOf1kCqYdGbDfxsPCVli8liSEkZw+/ztG38SxLnqmVbizbRmLUv06ANt5iytZv0xw4assyi'
        b'dp3JoH+GF5PBbDFlicvtM2qzs+xKGkBPN+ozRf6YCfmIUXxmMWPOyh2FZ49tJ8RtlADl8nyyYh5dPp7LA8yN2MmPZOOdvYVFoQschJSUk2mG1YLFQ+CwsgqK6cPRiTuE'
        b'HdEneM+ps50Fz6NvCoJHSoyv4yLpRPcX3u6Cz5YwB2FRSuavYgzSoc7EWVAjsqAw/WUeFmK1WefOseRACt7hLbso0GJNs9AqMdiAudgvsuNC6BT5iWHUft5ihEGsFt25'
        b'a0jmx4Vb4B4nFinux152UmiAfn5YmA0lUpxZMytRw1OHmyeko8LKKRKy35hGuJqj4KHoeRZbXV6J92znXfFYpTlETdtoQvLvFBU9kAY1TMAGKGaHi4TqT9kB4zxs5YNm'
        b'Q50DeX41q5K5szijEvLWcREsxfYDIj943JDBjx5VnnzEMhik0IkdO5on8INHfIJtfMTsAI2GnzqGp/Jzx8MoOWQKOyugVcMkEwvNzBvdgIuvcGIZFJ8VYy9b6eF4rKUI'
        b'7Sh0ST6nCe/7ikfIe2yjuJDi+XILPpYChcI9q0UWmTsGSbF5q7dOwTOQdadX8oaDp6SGJ4v5/H54ab40B+1RG58lDC5zWgc3vsjngEbKN9kksol8SCDcYekjyyWgZQtP'
        b'J6D6mE7OXY0XDMIdW+NVck6sdTLF5tyNNkALtIjSSfNtrOCnzS6uXNOA4lqXlXOVgjYlYEnkKUHa6Zvu6xcv4tkjhc1Vwl64ssj47ksNgsjCtOrzP15VERynWOcS/utP'
        b'3sqa+I2ioKLzvrplSpXKIUXT4jtn2x3PvBpn3YUKeeU7P3N8NPGffux97czcDT7CewUZVz/5w+//Uj2/ekKqZuIJ75Qpqk/bz/xl3eY9vi+7KX7+9W/lNa6O8Nlk2fvv'
        b'y86XfdoR+z5+5rf/L4kfL/h8wus3PnHYvvTWn9a/tynpRlj4n1469J8zf941t/6Pcz849sGOvvRXHT9paf+sPzbg7vXyS6f9bvp83vTZpJ8lvxlf/jg4KDTlk52/Oukx'
        b'8bMVA6eC/nPmZzUb1DeGvJqnfv4I1/T9cN6A6WdRHlfDbn4sn74dZ36r9LPGGUeO177peSTC5TfRi18wtzdfu3P1dXXTzp96Pfjleo1LYMn7p2QJGYZPQzp1DmYeQNRN'
        b'TvcP9IUSl4hAuaCGq/JASrZbzOzSz2onuOMfFBng54O3dEFYHkCZv+CtVe5JxKe8A97QYGd0fCAUxmMRlAELCjQJcizDJj8zP4HsxEYju37jR5FmS2CQjGY4J1+cCl1m'
        b'XhN/BHksp+A3YaBvGxYekS7DHA70w6KFciEInqjwHgzMNk/lWgx3Z2NxbAAUwK1ISukFdajcbSJFyeywcjUWbYiWhm+ipJpISvHLZDyvwIEt2KWTD8l9dUxzBZ0T//WV'
        b'3xiafjF5Zbop+7ghS5suXa4KYo529ZAzh/1k9gfrJiYx+D0t6JQypcyRv9xkcpkX/fagl7OMPXfhz51ljnI1e5eNvLM2tcyb/2Z/udFfStYi95GxEocQx5nRqYeUbMYh'
        b'BTnvIQebKxxSMt815JCcbLJkJScPaZKTUzMN+ixLTnKyTv3X16hTmljwZWIXcEzMwEzsnpeJBWV83mq2NuYMhDPCxz7Et1ym5u+WuQI76T/HYz8mfUn0cGX7iPQJKC4R'
        b'rDCdUcB9h2jaGCyOwzYCsLL4SJXglqNYFgK3LGyXdy/Kio6Jk8JImaDZCRV75dipw3NS0lEJ57B9OP4MiZUtnDEzVWFzemwdDsNOL0SwX4dSpittcaOiQEFxo5LiRgWP'
        b'G5U8blScUtrixn0UN/5A9mzcyO/DjQocTdkHtfrhUG9sUDc2gHsmQNvyV+JIk+GQxWiSooccg4liyYNSmDN8SW+so48f9v/EiN9mmtF40BBuMmWb/DgxPbWkjR8eMn4Z'
        b'u1KI+Owixo2NbIuSRjy7wvGmYAHlxkz9Pq1RCmtTs00mg5iTnZVGcRCPK8WMbEtmGouTpJCHB7i2oHb8iCjcyJY8EoBRsK3XhgSaLTkUWNnCLC41ig99WY8ANpHur8RH'
        b'qufiI1WcZQV99seHmePdBCyM8YsKgLYt/FIgu09YGB8TGQulXjJ216JQ89JM0xajLiZMJa5i8Ygs8KOUoJ/r9BH6zA2vpWfu/Thlz2s/eP0Hr1fAvYqX8lur66u7c1sj'
        b'2vPr84NLdVfq82dfObtYIQQ4aZr8V+rk5rncO+ZGafzIErAQS2ItgYuhRULGWdCrxLtwB1vNWmYWA1gCg9FBOUlRsQGRUDoMftPgnjLLB8/o5GMs/cswjpv7kEa6ADoC'
        b'aW4SpKUx0JrIocvkPgJFqiHHYZ0acrBph4QlLuyN3dgcM73CxO6GmBiWSN04xjCC3x+FMe0TR2MMWyNl4e2e0UHPLJCigi62yD17LKsFFt+URj2X8raSPzgPPVACdQGK'
        b'3dGh5KouQNkh6KAg4YmzsBcrXfE6CVAqS+2BhnWaw24U32E1VqwUsD1KqkKHiNCkOXyINRSE40MBr53cImXhVwKxSsT77iFKQY6Vshew3WsaZeg89KqB+6vFEBKVLPvw'
        b'dgH64Sw+4S3TTVrN4cNqopYXjPfY8u5ih066q4ZdSYZhkDNAvWwh1MVabB61J2Fskq2FRsVkMYmPM2C7gz+Bp4yy8TLoSpKFOZnGwKM9J1jO4FHBAVK6KSq3OqY72mFS'
        b'+VdhMp1g8k9fll5z+x6bXH8pSDBAYd3/dpL6JbkjG/w/njqmZnK2RIP5+WTxGQaZXLJTUy2Eh1mpzzM6nC6Gb1qnDSPXbWJ4uYH8Qqo520QJYI5lb6ZRzCBCe4/xnjb8'
        b'DqOE0qTPfI7eejLMoFG86dmmWPhtcb/EsC1+AfRrwwb2Kyx+czD9Jvb81oes5w1hYX4Bz1EctSZKRbPHTXrZIrmcc6RUl6imMeg+lvOMANnPV3KKdorZOc/7Qvbz1fzh'
        b'mM37h+XaMmG8XNudcm1WxVp/iPDoKzsT5kmCoJs5E1fo4plO6lZKyVNKVJSSrzyrOiol2ut2ThTmuXyPTDpl1/aZRlv600QhchXP1OW7KVOnUKmYA1QwZcSUs1LcXEBN'
        b'86F2kswJu6ZJ19cT3ASfZe8qWcre776SsJrf3fODIr/F9Ht/UjANfwDt0o2+2gWei1mqNugfIoRASQYn8Yb3BEHr2awUclICNq9cPEwiag7eZiTwzGaigbfjpOt/d+Gx'
        b'hte44/HWJmGTg7SgoYUawTPF20HwSHHRzdcLW4xnkpMUYjc1dZS9ML8s2A0WUd42L3bo3JXtDw95db4te8PNK7rRLXLKvO0FFW/9SDFvhcLhl/URO48de//9978oebrg'
        b'47PB68+59xxW+J++WrHhtSk/cr9zKyXmv89rSl5WVd3rWDH3ou6b/l1p317g+OJKrd+/dEdVvO3+UXLBw8Y/DbQVBWsj/f/trYg2RdvSsnzz06v9QWk9ia/8erCm9q2O'
        b'x79/9zf9xyHwWP/cz7x2JzX1XcrSzfz1iYys0x/4LMEdF3SOZl4phUszKLfSivbU6oSRe2vsn7jS7tV3rSe/Ptqpuyw0s1sMeDkZOxiWU3bFUqyF1CWQDYh2EIJ1h7FO'
        b'HRmDzWb2rQzIxYKtlPI+0kRjic5ObjJYlY5w/ahZ0g28goWUrJFrwPrsw7J1wTk8q9qPT3ewFG0htEFJPOP0lNwPLmAHzw93ReFNnnJd2GPPuKBjv5T+lVK3hmgsjdZN'
        b'TRjOD90XKfbNh3ydTHL2jn9XjiXFH05SRkUOgkcfi6To47QgDKdU7F1OqZEbT5ncZEo5S5Xm0Mvb9jJNGhWfjCQ2QwrC6lFhyd/KiRSjciJPe6jCaP9mVKhycdqzocos'
        b'uD+fZ0PHKNGhhCieu/IJaFVQDPIQenQyfnCWjRWK0WX2cC3U0l5WjPl+hz2hYVfUyF/L0+X273HIvvR7HLZk5ovvjIGszRLkfUlMns5Dau5cR9ex/6eTmHExd1g6YzFX'
        b'HceDQOzAfuhjoBsOFV8ddxnowq01UtjWnbFZtB2/O7Avd2ArNvJbIfPg0VEyIyyKxZJELIiRTwyHVsgj5O3Dp1BDf+iETR4OcP9kjvHypg8FkWUUu/7o/FFKgJQL8Exg'
        b'+2sDFfVVsojFTYsC0wKS/PVxevW3FgWl/DJl+ze8b8W/9VqNTEh8wdVhjYNOxTFj0cpjoxMBd81oyNiPVWZ+xNITvpsQh/AGLvtJkOMHZ7mxQvtx7OLVHF3QgrBRxRw4'
        b'78EnOEkrrBoGEByA4lEggpchz8zOeKKhBfp4xecEnpO0mhd8oHOVZGzycS3aYZ/BbLdnj2F7ns3smJdBZCavEXtVSOWH8ZMHmdTI7ZCN8SZTESdKdnhG+JXbaEtkDGux'
        b'dupwhYozC7UurEBVi11/xcrkVuHvsrK2MUqamJNpNIt2U5KOC8hetOxpukm/j5f/nzGrYdPUa0PHzWnHdPYNi98at2XzjgBtWER4WHTi1lhKdtfFRSeHxW8ID9CuC+Pt'
        b'yXFbY9eHb9Z9eQY8ngVxb3xgLftOm+CxSP255bP5BwXLS0y7buJ1yqWKscSffReuMCYhQkpEVkxiqQhW6qDVGWqO0SsSCo8JcF3tDAXZeJ/fkAxegHWjx5Ll9eA5Cfxm'
        b'YosSbiUlGgNPpsjFBOqd7pH6Ucqu17rISLpzg/Nm53Vfiqysr67Pr8+dXfskoul8cF5rTXdht8L31M/mfLPrTGvuodmpgamuqd0zNuVPnZeIA2eOzQ4jX6QRildPeMsn'
        b'S6fkFjKJ4PcxMxFKuYa9svdR7kXJys/NesaDHsZ27kRvQ4WZIbb73rnMG0ZCIzQNu0Nyg4XcOF6lGKs5mvtpX7XghOcx31sO9ZgHXWN0eHwbcaZkQhyVdHsOm0mwo8yF'
        b'G4qblHp7/z+YChvjO8ZUhsaYyky+fuyN8o8I8IuT0us9iWxrvOCRcjLm7tZJnm2+1lvyWBTUli+EIsmsplEOelqZgecWjG9Utloc/2KivRb3FQzrJ7ufrcWN9mC8aJWl'
        b'P8jTmXEcF0tm2IlbjoEekIMb60oiJfPK1JvNlJuk6skLjSXK/Zk+TSr3PZeVjaFlz9D+VoImJWT/Gx2qbFw4cIyzsFIWFEeY/moO04Rt4/tTrNVzQKkSvIV7x/ay73/6'
        b'RE5NFvjB0CrsxjbxEDTOtH+b8TEWSNeLL8PtCdHxeDFpPE87ysvCfQc+wc7DDkLJqensq6gu9d46wfgrr4/l4g5qCTfMHet7f5WSkR6jfzM9YPOvCGJ+8HpXRfCV+ly9'
        b'7J31+XEe374Gjyu6f9B8fn6e6s6NqXduZP9wKwGPrOVGn/rO6jypRvcf73s5NDfq1LxGB3UzMX+0b5awA5qMknOegw95QA/dq/aMiufjeREcy6LlDBVjVcKLcepTsRnS'
        b'SUcVdEEjO5epwBv27MEDbpln8AnVaLW5cu7Ij8MdyZfjjd1mZspwFvpeGg1l0LjX5son4xnOdRLejYkewwdnYhsWzoJKJV7fgZ3DMfzfqhe6cO9Ois3MhmOX1zB2hTPE'
        b'cpE5yyU37yIzTRuFXkMahnbJ2SYWG4xCsXEnJG6m2/GMUVk+Bs++MaZeyL6bsUMNdSMrbKfNsa9SWiLUYbdOERe3USfbqJPHbTQe+5c0pfgFkf2hVbP1wvcTJyV4Wn/7'
        b'5FHrvTPerwX9vujJLfkbZUW31J6e/7m4Tuu8wfXhCr/C3wRN+/rqn/6u4vEfXj5++eNFy/f95q3P3/0sZx++E5bVN/3N6A9agt/98LctXvXd3Wc+8vd+58N/O37vnQ97'
        b'9353SlZXpeeGq8rvut1852lCqsnXv/BnPyuJKf4kXffHQ9N7io7u+SJz0Lv8v1Suewr82lrrq5dP/Od3Xps4bUdU5YKrRv3Ub+14PSqp++qSO02XLHf2Kab/69fS73dd'
        b'Opi5z2GFMXXKo3/FPb/vvqnw+cDDan1vZdVcn6brqZ/lBy77jtPyXzQWVzUu+7rxOznV4rUP5T/c9UFlUtA7OPnJ7qbLB3Z9/z3X7/3Hd+9+EpsV/Jq2/wF6HHlwu/f6'
        b'8Ud3f/i7My5Y8ruKl0tC3kh949it968k3Qh5fV7iF2/W/fzhNz4t+fCx9p9CFx5b8v6vW3eVt0dt3NH4tZT9a//1e0kPkqKVMZsX5x/c2Za2M99Qfanj5x987ea913q2'
        b'bP7Bmx3+eQFbqzt70h69PfTbezkHfthSu/2K9+HvfmCddKix4Zrf7TeCF+v3fNbs8dlfvu4WeDz1ceC0P/7zd9pK9uaf/LHjH6b4Xmx64c+fPP3pKregG1m17z5ILnv7'
        b'mwNPN/16Xuh/nS2/9PgFf11R+FTz6X8XZz98e8bn8Yk7a38aHf5Zydo/7PzmL/fMTf209Lfrlhb9YnL3hcENi99d5K0im+b35F7B61ictCpGJsiWCSzK6eJR9LJY91Fm'
        b'BTVwaThEjj3OzWodnPUYwQK8CM1jk3voOCpF6rf8nOIsWBwQiaWBakG9Rz43Ewv5oWkUXII2/6hALIiMiVMJGujeSCHrdXjkL4UpT4KgPpphMfXAkkjW4+4WqJQTBN+E'
        b'7r/zaFPn9vedhH4pHZWJeY9x3zhIOCYnZ2br05KTOUD8OzPbuXK5XBYq0/Ijz4lyR6WXTPrnrJKTETvy9/99/xzlE2Xsn6PMU8GqED5r5LQCz0nOtBpvmY+vXDbNnV4T'
        b'5DKTzzBQEtbJk5NHQZzr/7/EZaYZdjxkEzH1k45q3l8wGgvZ4TjpaksGFEM5ljP/DIVQ7sBu4lS6TVXMgCdYYmzLMMnEGup6t0kWWLzKGdZ6nv/w4NLBjZ4Byu++Meno'
        b'FE2qbuWGTZszps3+5flv/mjOicQj4c01n6/eGP7Ja2dmVpnf+Jb2SUzh1bdL1zb0fcc36JeP/tzx1jedfv2jW9/67bu9E77mu+uPk68enXDtuzOnlYRcWv3HOb/93jcU'
        b'rf/85/fe+ukS9baP/s+EmIyaQ+t+UunfaRz4SfWjj3bdrl/87TV5WDD3zfemzHhb9/42o85VKp718stB7P/0iKfVlFAWcSbagYygR44tYXCdO0AsgLYElqV3s26sqjUB'
        b'HyugQgX18XiTe1HjAnY5kkmE+QQoZRJxDnWbqJiJl9O5ja6n4L80OjLWL9ZhNhQJaqXcETs2m1l5YAPkQ7t/FBRAg0qQRbO7jc1rzOwrjbK58IA5mo1wdnS0BGULowkI'
        b'yojfcoXwMnQ70Mz1kCstqW7H7GfDq8mEClM2KP2gBLrN/Btm7K5wG62+hOx+od8hG6xMs0AfheiQj5eggecos3AAO1lMEY3FPhoHQRkogw7I3cDxaRc8PcKd4mh2pkMt'
        b'VGG7EpopxbskCbB7IVixWEc9JZWRCdgKNe4Jiq0heJ4z5KplCZ3UI4DWB3ehW8rtZJR296kEbFFI0cgD6MBi//gALGJsrYM7bL/wqRz7U7B3TM4y4x+DRv/AN8qxvgTO'
        b'jFlGsw3OWHgnuLIYhzI1hVLGAIFlax487mGRj7NiHouHFppm2iFh1pAi05A1pGTHIkMqnvMPKSl5MA8p04yp9E6JS9aQQjSbhlR7j5kN4pByb3Z25pDCmGUeUqUTmtIv'
        b'kz5rH402ZuVYzEOK1AzTkCLblDakTjdmUlozpDiozxlSHDfmDKn0YqrROKTIMBylLkTe2Sgas0SzPivVMKTmaUsqP7415JjFoQkHs9NeejFZKsSmGfcZzUMaMcOYbk42'
        b'sHRiyJXSjwy9McuQlmw4mjrklJwsUmKWk5w8pLZkWSjLGIE6abEzTOzA0bSUvbEvHZr4t5qY3Ews3Dcx3TSx2ouJfTnKxBJGE6u2mdgXq0zsOrOJOT/THPbG7MzEvplu'
        b'YscLJqaMJv4lavYf+ZjYzSLTMvbGokATgz8TszITq2GYWDXOtMgOnGw7nO3A+d8bRgEnb/vCcfi2z5BHcrLts82TfTEtfex/s6TNyjZrWZshLU7nyO7hpGWnkkzogz4z'
        b'k/B/pk11WKBMz51J/CazeMRozhhSZ2an6jPFIZfRaZtp1bAAR71J+rdS+r+cVjMd5SU1pVypcGQ6Fu3JnJTs/wIDzR5W'
    ))))
