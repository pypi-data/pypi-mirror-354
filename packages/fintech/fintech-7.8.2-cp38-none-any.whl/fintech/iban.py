
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
        b'eJzNfAdYlOm1/zeVMjTFLui4NoYqiNgLYgFpFqyrwjAMMIqUKfa1gQwdpKioIAhKUwRBwYLunpO+aZt//tm95Gazyd7dZFM2N3tzb5Ldm+z/vO83g7TNJs8/z3MvPPPN'
        b'8L3tvKf8Tnm/4X1h1I+MXuvoZVpFlxRhn5Am7JOkSFKkecI+qV7WIE+RNUqM81LkekWucFhpCnxVqlemKHIlFyR6B700VyIRUpQ7BKd0jcOnqc5R68Pj1EeyUiwZenVW'
        b'qtqcrldvPWFOz8pUbzJkmvW6dHW2VndYm6YPdHZOSDeY7H1T9KmGTL1JnWrJ1JkNWZkmtTlLrUvX6w6rtZkpap1RrzXr1Wx2U6CzzmsY/bPp5U0vFdtDOl2sglVilVpl'
        b'VrlVYVVaHayOViers1VldbG6Wt2s7lYP6wTrRKundZJ1snWKdap1mnW6dYZ1ptUr1Zvv2/E17wIhV3ht1knn0965wm7hlnSHcHpWriARznifmbWHuET7zdPI4nTDGSml'
        b'lyu9PBkhcs7MHYLGOS7DkT7XG6WC3LFRKQhJMWFOzoLFh25CB1yDaizGwviYbViAN6AOS+M1WBq1c2uAUli4UY4voBHbLEtY53NwASuocxmW+9EILIuMxbJdNKw4aFuk'
        b'fzSWYElUDBZFKYQl+PwolDvtD4rna1+aqxRc9vxSLqiTYt5WnBQs++lmGvROxR4n122RNGVJ1M5IuOeDBf5bYvHSDkcsjNxJE49cyScyBsviYuJ3+lBDQRBRuS1yy06f'
        b'gMgofwm0O5nlghkKJ4fJoU0nGaVfbna2bPkS+aS62SQgKZCSBKQkAcmQBKRcApIzUpsEUkdLwIlesWMkcE2UwPQc4sK2mQJxweX9tEyB3+w7JBX+O4JJLSmjTusp3lwj'
        b'OArzvObRvST/mxtTxJveyQphWTTNvC4p5k+h0UKbkOFMt3MCp8n/MFFY9++etQf/LH0UXDn3nJDB6JgcVSvpchDUi5Y/WPuvxhDfSPH2jcRP3KvdJT7/Lnzm9Ndp/xX5'
        b'I2FQsAQx8VpxAJ+QLEiaPj5YhPlQFxQZgEXQluBDUin3D4wK2BIrETLdnVbPcbJMojFe2yabXIjXeBUewTkBLsNDb94wGVux02RUUFMxdh0ToODkRgvjCjZDaYDJ6ECf'
        b'Sr0nClAUoLBMY6v30Yg8Ez5ifSp2wh0BSqAP+i1TWOOzOHhugjLiKJI2rhGgzh1bLJOpKQE6j1ELqT7emgldAtTDhbO8BVqhT2/KYSSUT4TntJQrNogtjyE/3ITdZAtY'
        b's8xDgIr58IxTt3UmNposbMilDVArQLExgo/wgzKsMrmyATeFlQLUYik85xudDWWxJuxhlF1xgCaa68Q6cUPV0ImFJihhG7qBBRKBTC0Pci0T6caWBL1JxWhuWAX1NF3G'
        b'Qn47WZdqOkbqipe1zgKUTYc+TtWZaJXJnU3TEE/TwVXo1Vmmsr8v66Ebe1zZ4vfmYoUAN6EC6/kYuOiTouL871g+lcYshHJO76Q0LIZikpnEERp8BehMwMu8IWgCseQB'
        b'k2Ul22E5yb1C5FZZ0hHssTCybkGDmjaWCfd4y77j4SrsYmvch4ubifXYj+f56glrJpuOsf1VquAqcR5rlvP766F7qQn7GMG1k/wFuBS/1SarLXjN5M6lmHyQOIW5WCzu'
        b'sd0PKrHHkTU141NPAa6jFbv4KOrUo6Q2RkELPnYkCnRKrjDL8QH0Y4+ZtdQmQRXt5xXo4U2pUDoBe1yYKFugbT2pEqlZKV8rGntJDXu4QreiVc+UyQotfJieJIk92M1I'
        b'b4KLBtJ1BdaKxJfo8SYhGRvWOT1ZgEa4a+CDsA2LdlMLZxE+VghwC59YRNpvQ9UpamJs7ZqUIUCTAtp4y2K8S7vpsXBlWwgDxCXjapEXVdhB2+9xZSt17YYLNB/Uyri6'
        b'eXoRW3qwhzW1I0mCGEXI3cnpOLUdG1gjs7p7pP2kpvUyBy52/72eJENOOrYQ7XWH8bbIwiU4oHJkDY/gAjwR4DY2YStX09Pa1Sp8wCZ7uGEp0bBrr4080vkB1VG223uE'
        b'JVZS7A2k8NyC70Iz1qvwEeNfty/epZUyJolMql0CddTC9tszF2pIi/HmYT4jsfwe3qM2NuVDyLcQb92xiRMOlfA01GRmBBYsnCBA/ivQK2p+9al1Kga+pJXXXiPVTz7G'
        b'+ToFz0tVzmyVx/DEQYA7xKfbFubId0A7dkJxGFYkQRE8hBKFIMNbkngSRIVlJvPs+AwHoPgoVjtSh1IoUgjydAmc18BDyxy25G24u5e3Q2kIVohTOFHH+yukU+ESFmtk'
        b'Is0XoYtUpZiEngWVbkIWDkRZJnBLhq4J0XKGANgoJE+eyflME5yDqmgiOQUrFwgpoest85nIjkEBqQK9cqAjDNoU2lgoxeZDEdC0L1YINSmgJmOCxZdNcBObvFlX1q8T'
        b'a7Caf1TguVDowBq54IWlcie612jRMCpa950QexOat7LukdAZthmq7b1hQC6DPLxiWcA0brvKPvW9oamnbg+Fu+LMlXIlVjtZFlLXGf7UsyoS7hK1Q12hWR7CVqG+ATLs'
        b'D8EiHpIEn6U+dpL51uDZIZUai6XYAK27PIUtagcVtktEn9UB52Fg7A7hPgE0vTWtJ9HSCgFGRU4E3OdjXsN6/yFiSmXJ4grQhNdisZDYCMXExUjsV+JDrMNLnOVQCw8w'
        b'b/gWGGegLkq+XZiJPTLsiiG8WkY9V8PD/cN4SFRAz8rhHAqF1lg2y91YZXKskAP3HeExVodbFnFAI4NuZsvQ5G2T0TZKRghYiDWQn0qadU0IxpsKKINzmC9K7QYOHBsh'
        b'CTZ8PjwMFffuBVUy0t9mVy6KXdCAV8YyTBobyvbF5GaVO8TEcnKIi/l4aw4NHupfOmIRm16EnlJA7QEyP8Zer5S1a7HDPmKYuDv44FBR5CFYroAGKEjkMt8Dt40jFY8P'
        b'wRuJtu5eeE/uGLfKEsioql/sOmZ6GneXzx80U9S/ADJSE1yWWgJoyCZyBs/tY9rZGALVE4yjkK8myXYRhnkKsTjgEHLwhMWPRmSosC9l5tAydj3E3H0+YSJJJrjpSBFv'
        b'x1mRVQ+ghxausm91tCL2ednJuqwweeMNvoia2Hseyl4ZEt6QJUeoCUyZssdjvUPgJHwuLmKFrukvVXfESsSAlg0iZYHwVHGIHFk3Vw8K77sSbIPaX9J1Ay/arXqhDJ8u'
        b'wmfcqA/ixcwxat58LJTJXE6q/kiG3YoELugscjBtTDVHKkfbaOXIUcBVJbkBpn0pWymutKm3vR9WHLXjgExGbrIFrvG+OZCfbZ/7/hDhwXhvSCea5A4rc8TUpIEGdrLe'
        b'cctG08KHyeGBS2z4Bri3QDBijSOlMU9S+IbhHsW97aMBBy5vPRShVgih0KCAm7Pmc/YvwJtbQvDCSAF0DjNsbm6L8bqCRSzkOpjqWWLh6kttpSGHvYfLQUZ0uR5aItmm'
        b'cFh2NJSPgBa0LonmEEHdRigG9njZUH47lDrMicdr3Hw2HIWLdqoOHrFhGncIDMoWw0OCC8Yd0SeUwOWIMSLuxTshIv0zsZukAE3QwaWAj0hi7SMAgw04CYUEfV5wgXSH'
        b'3GQf12cCira4EabJ5VsND+wCBqsMn0AzaQNzm+s1q0cTYjgiZYjaR2qGN5xEBS7A626j+y3ExlBGDaO3i9F7FUReQA1eXWNTsfah7d06Db0vdazXgs1coq8GHMY8ik7H'
        b'wGGoXYM4S4LxmgLq51Bsy0GaYpcqvE4cHs2UUBHw7aN2K6AilAI5H1HxC/1dRxo64clLQ98a47AcWqdZgjmiQxvZb4tmpKrdeyktcS+L4YUCyuFCojiqLZLZOSFKx8tB'
        b'Up1tIQ9apz9sAhQskcD1dc5x2B4leo9L5D8axzrnDuiw25lGRvI9znUTX2Dp8i/EdpcoG8hZFNnTcIDrjzM0uI8WHrb52cBhJj6WUahujeZMyiFCasfxA69GDoUrL+Ru'
        b'+2fxzmp85jlm4kfwOESkYSZ2yiioq97CNdMCd9diKanqaEAfJgB/h6VwBQo5V05C/kulH1KjSTSkd5gmv9ist4SwUBkazzJSnlLKOZbz0LOPls47hE37BONh8vYOlHEx'
        b'orYKyUMqRJHz42Ha16GYaHP1d8lNCps44E6dR6g9OuKyRxlh2LXPFutAlcIMFe6iy7iM7XH+WDCeireNUPFGAjrDWq5JZEOPKPQe2v4ooCN3WUwGoshZItnq6BAGXUtF'
        b'Tbp2NO0leXn4ZEhd7yqSiQmxQshUBZQYN4m988n9N4xwmFyC3WeIxWIECQ/k8sXJXNgLAommMVvAlh02x+SFRXJHuOHDVQ56l04bo9BHsduuRCtlOBCHV8Vgoney9yTD'
        b'WI0eZcpYpYAbp85qYnhcnr3FbEs8pJQH5mNjEr+98MAcE884CzV+5Kt3U0DEkpjIWOg0YS/rXwEF8JQSajhPzpnlJCHYu8pWQPFkmd5lYLkty4ocIBfzKOdkeW+9ghU2'
        b'biTDRZ5FUES/wWRkCY51EVDSn4elh/hs0dAyxVZzIYRqIOQ8hS/EKgVFsk22qsshPE8ZubezmGFdgRdYQIk/E0nZOpZ9FUNxjpjPPYHbXiZnKS/vtEId04tqWwkFS5dg'
        b'swmKGBU3Q6cTdfAgnLckwvVoexkHi08xf1O3UEzMrgRBtcmNzXctbhltdn4wJy6BdKHRXt2ZfYYywzNzxMzwwuK19toO5p1hBYZCcku8yUqw0Wmr7sClfbSjM9AnbqkT'
        b'63T26s567BCgAmrgAR82CXqmURPjQy35pSsCy23OizNep/y2w1b8OQvFxAgNXOFbCsJ+KLRVf2Jns+pPP9ziLRvxsou9+nMAL7KlKtP4dI4maDGJGXfdGWxihngeC8V6'
        b'QTdec7OVf8KwhOZzgTwxP3yBd2JthRPFSdrTVCznQ86QBG6bjjHayDY3scywJoQPWb55gr2ggnXbKKz1wod8yC5PD2qQiPmBioWB92yyOw59MlutRYHXWbFlgFI6psEz'
        b'kiJN7mxI8/x0JtInu/kAOT5YPFSCubKTVRaq40QV6YujxMlegXmEz0lGUcQbnvJ3sCKgrQazF+8JUJ5BDGVN20/Qkj2iTTTM9GB6nwv3xLJZG+QasMdFzkskT6CcrVZJ'
        b'1so5V/pahL12o3ZhpZtucspcH1vh6QF76QauLic6wjeLLTV4QU6L8XrFbU027dd5Fl9qK6UpRdjj5sCrM0+wT6Co5w6K9Z7FhyZhj6h7DwiRali94OoOPqM+DsuxJ4c1'
        b'3XBjBJavwqeiDt0kiKmlNkZhnVnP9OG83DKdc4o5l6EKEgmln+nEtYmcjxNWU5RoqyBhM5xnNaQyaOBtchLdZXsRiZLdMlZFur5L5HH3Cqy0V5G2YR7tYKWNx9A9l0DA'
        b'VkaKwiJSDexbJTbVbyYd7rFw9mPfZAEqT0C9yK12HFhGTQpeaR2Ip1Dn7H7eclbhSNQ/5LzHgvksJb4ykU83e78n9rhKOe3dDKka8Bo84ywOxceUeNkKVuRoq1jF6haW'
        b'cDzwiF1CTWyl7olKxvsrCXxQGLaz4p2tlqXGa0wFmrCdL7Y2JWOokoWVQEys94FyPo78Ei2vwi4lL3PV4QvS4YWEtHzP16Fq7VClqwfzSXtydopSy9u/WeWo5CWmbiBG'
        b'NROJVnHKAqiCHnsZ7DrcZaUeK4X2fMpmCk3rVWauqiTQFmLWNg+xMnoM79tLZEQlYf4taYq4WBclnbdtdaiJvAzVQHbJTHk3VO1XHWWztZ1m9NXo4RJn1Cu06CPVUTak'
        b'QxVGOGqK4avM0WOnrdwGl9cwXKqHod1ewhp7uQ2fbafdRp8QCXiBuZBrr7dNXcGKxkXuonl1nqbN2qptcnhEWuip4KTh0z1Qr3KT8Bh/wFuA1qnHeeFqtfMWlRvTvucM'
        b'GNtdt4pF5jPuKuwWmXaRlSkb3ebxBh1UeFMLG9CvP0Ay11HYzvWukHzWDZUT06Jn6dBIWVD0JD5kGSlTtcrCa9wxKbT5AJuqQpcGym2FvokbWVm8Ga6L1D7Gx6tVJs59'
        b'f7xMKpKYycUZQotch2JRQwbgfBDJkKw8j0dxa+HFa9RWBQW8jgdFcM8W+0FBGCvqTVglh54EKN4p7D6gxJsRMzRyywwxXG9VY3EM1J3agiUyQYbPKcamxLKE02lIw9Zo'
        b'LKJA/UqMUpAelASlQj8vK8JzrFRHY1kQ5m/AUj8NtMsFFw/ZZOgJ46KKwovQ6xfn7RcQKRfk6yRETTvWbdKxgyX7D+2EnzrxE6d1Aj/cYoda7ICLHWzJrE6pTrYjLXmB'
        b'PFd4TXHS+bR86EhLwY+05GcUe4QUGT/Skv/s30kKzuphPxHsGNSk1mby8091apZRfVSbYUgxmE8Ejug44o8o8fTV93BWpjmLn6T62s9e1Qaa7ajWkKFNztD78wk3641H'
        b'bAuY2LgRUyVrMw+rdVkpen4Wy2bl85ksR+xnvFqdLsuSaVZnWo4k641qrdHWRZ+i1ppGzHVMn5ER6Dzi1opsrVF7RG2gZVaoE9LFY152/ps8NEvgeAOSDboVbJtphqP6'
        b'TH9xFCNwfVTECAoMmWN2xH50xBj9cTPbgl6rS1dnUSfjuAvxvRlPDF/MbCeTWPn3r2NmJ9622QLVsRaTme2R8X1HfMDi4LAwdXjM1shwdcg4k6Tox6XNpM/WcsJ82Sdf'
        b'tZ5Uw6I16/kBelJSgtGiT0oaQe/YuW30ixznqmXbi3qHITMtQ6/eaDFmqbdqTxzRZ5pN6nCjXjuKFqPebDFmmlYMrajOyhxSUn+6u0mbYeK3GZOPGUyjNjPmIN1RGH2M'
        b'OyFuk4igz+E+nqPYE6rTWfhJcVoqXuRntD+KmCYsEhpOypKSVu0zLRA4fB/HK9BHAaUQQlC4V9ibAs28894sZ2GS0J8meCTF/Mv8lbaj35NugpfwpwC3RUkusbO0goiO'
        b'zQR+FDHiFWfmspnvbXTSuNvxvBsfUiOUhNsbm9ViOPkEOmJMx2T+7BCS4WDZUjFsg67D0GNyZ9B/URxD0QfBFQ9FyF/dZ4eK8ACaGOhSr3UonsOGQhfmqowKzD/DfBHD'
        b'3Ero4aFjOOSuV2XLTgayAIxQ2jfZdrCHNQdVOTKoY5RTbHB9OwyIe3qE1YnsJDIG7wsSR3I+Bygv5mPq13hgj0mZivUsChFYNU0j0l2vxH52SomN0MmCZIq9/KDO5ljd'
        b'vdkxJeXRrSy0ZRFviZhgzHEmqrFLISGXRs6CplFMEx3FHUrI+lTHZKEnGEHUIIgHd9ByEJ5hj1EBletYakCB3DKKq/mYUsVK0zEHqFWzoJ8I2APFvCECrNspdo9NFgkr'
        b'orzkhkYm7qgKapKoDUqn2RutZj5oKpzfzNbx2GlbhuJVPiQmFVtoGT+6Iy5DIWolp83dAe6wnAMeUzjC2yomYJ9GanPUJ4+xRucAWxOWz+DzBRsEdhZ9Cq3MYbGz6AI8'
        b'zzXux35KwUWocHVRJ8X8edpGgYtzCdw5vXiRfCrxkagXkucsMnh+3iiYWCT3QPbV1RXBcbJwl42//f23Myd+Y1fktnlFCdVe5ye+dX9Dw8ZdzruKvpLR7tM2cV7LmxOO'
        b'rix7I3iZZHOBT3dpwZ3un978Xdbe5JVJd8OTHVZ73Vr3ruq4a+Un65cbfxkc9KPFUQcq3mk6vuRXX/lKt7vrB9blV8+6ZXW0lr39TsknqgsDabvrk/YWnsw72njgxJSH'
        b'194oLP7joosypw9mz/nevO/5LfldRIFDbO2L73Q/M61J+GvbafOHS78bVH1W82LVf3yrf2v5vT9u/7Cq4p1nVb9+e/us4MSolPe6j2ivXXrx6n/v+HHsBb++TnmjxvzN'
        b'zq6Lrl7dA8fq//D1pndbFn114TzlzWjPX3/txt3rr0+5/c57bo8PrXd1WeLyxxfffCP188+XaxzMTCgZOZ7r8IFfgE9kgFRQwjVpAGXMbWb2WNAsigXu+wVG5UCDv68m'
        b'EMv9sVAQpqnlB5VQYBaffUjwjY43rw6AwngsoiBBtU2KZRlneCPmZu9cjVXsGR3fgEAJTX5BuvgEtppZCQnOQUscRbNllJE0QKMfFh4Tn5U5GuCLRUFSIRAGFNhLKUWf'
        b'OFmFcQJeYYl5rH8UZRKCMlTqBreOm19hjcVYsIHCkUiKUJtpDqBZY3hEMxnzZNifdlQjHZT6aFiFQdA48be/+8Ig9dPJq1KNWSf1mepU8VGsQOZx1ww6c/xPZH+wbqZd'
        b'DIPPChq5RC5x5C83iVQyReIs8aCXs4Tdd+H3nSWOUiW7Sl5eWZtSMo2/s7/c6C85a5F6SVgFRIjjxGiUg3K24qCMvPigg80nDsqZExt0SEw0WjITEwdViYm6DL0205Kd'
        b'mKhR/u09auRGFokZ2VM5RmZZRvZEmJFFaHzdy2xvHmxv54TfeBHdUqKJXXkxPB16vKJF4Y1gvA7vEu/h3BLCEhZtnlmPxdHUiMVxWBYfpRDcsrEqVrZsUQRvNk6H29Ex'
        b'cfhsHYsrS/0kgmqfFDvh+lYR2PIJltopHMXuDbZoFGsFnWyY82NbcbA7vzBh6HEpearcFkfKCmQUR8opjpQNxZFyHkfKzsiHxZHvSEbHkfwhumGBpDHriFprD/1GBnkj'
        b'A7pRAVvC34grjfoci8EoRhPZeiPFlkfEsMf+ZN9Ixx9vjweIEN/ttKLhiH6j0Zhl9OWTaaklZfxwkdHLyBVDxtGbGDdWsm1KHDF6h+MtwQLMTRnaNLVBDHN1WUaj3pSd'
        b'lZlCcRGPM03pWZaMFBY3iSEQD3htQe74EdJGA9vyy4CMgm+tOiTAbMmmQMsWdnGuUbzow3r4s4U0XxIvKcbES4o4y0r6vNUChUMPDWpdhj02WBjju8Uf2hPEJwjZjfiY'
        b'qFgJO9UvVC3PgroEw4V3pkpMq2mWGz/5wa+TAj98Y7NGG6nNSM1I/k3SwdffeeOdNyqgt2J5ftvlxsvduW2RHfmN+cGlmquN+XOunl/sKvg7qJpWfF8jNc9jhu8JF1S+'
        b'ZBRwBVoo4yyJtdhgcjb0yMnBtmGvmdy6EE3xRXN04BYCSSi12yLeXjcDeuWZWB6skY6w+i/CO276gyrx0dGX8OYmwlsKA7CJHMaM7i9hSTHoaFesQQebioi44sIu7EnB'
        b'EcvLjCwPNzJcEbtxvGETvj0MbzomDscb9sSqyuI3fIdQQiyhXfItWjDXsoo7ps1b7ClxPbx4mRa3YQ3kUYBYQj5NdiA6FMpyKN+9AwPOQjJWumLdSRcejkyxqFRH8ekC'
        b'N4kgoQAUO7BgqljmK4cefEFtT/BxDmssYGn0sxVimPcEunaa8NE+eOAeIhekWCmZAuW7+Yyv7oZaU8isecQsSRZ7avAqtHFk86fxRaqjh/HxUSXNd1HAa9gUbQvADnhg'
        b'OQO9m2C1oZ4PNHC8TMQOH56C36PcelgOfvgoH7glYa5fHNyHR1gmEaRQJonYC3Vj4HIoV1jD4FLGAVN8slRqdUx1HIJN+ZfCZjrB5l++KP3m9j4y+f5C0GAAw7p/eRL7'
        b'BbklG/w/nlrqMjhZJr15bDI5ikDGlyydzkL4mKkbS6g9ndy4NVwdQR7dyPBzA/kJnTnLSAlitiU5w2BKp4mST/CeNjyPoITTqM0YM996stHAYbRpmVAs/JFz3x0RCb7+'
        b'9LZhA3uLiN8eTO9Enu/6kPW8ISLC13/MjMP2RKlq1rhJMdsk53O2mArTrCkMyk9kj2Ig+/m7nOTQjFnZY30j+/n7/OMI4f1Tc3GJMF4u7k65OHMuSzYNcy7juJZlPuM7'
        b'F2jfzpOfawHThOrsNPak9f55EbbHr+ULJgqvK9iT4kn7f3IkXeDAsxKbQlgSL+ylpKpa2ItP0cohYnPSUiimPLKA/KCnJD7LiXLiK3ye75xwE8xm8l6Lkvy/kxxJuG1h'
        b'uDwra8Ziegs+qBSCsSaB30tdc2AxbS7Ec5MQAiVHxUfDCdkbZkQIQnZSzDqFmg1nUA/XDh7n4yPxuRA8lfJFRt7xUHjAy+Jb4Tz0ClspHWjhs/wm0lmo2K0RBI+kjAPh'
        b'U4QEw0e37yhMvSwgjd8wvyzYDRZRIjcvdvDCtEtPcqZlfl+yx694/sT1US3OU3znmc5/95uKacsiv7fhB99687O//vVHaX+Yr1WVSF45XfHw13v+HFE+b9PpzBU/69JN'
        b'luu+svDGe492fz/61adz19er/u030/c8SF3s/PZqtc+PGgs83jr2Zprjil/85bVtivcL5t3L9pzbpmzds3zaDz46tO/HFVFxhoefL+ic+Paupz/9udPSlp/kf/vV0KgP'
        b'3t31ZPmp3iONT/4qWRsbtjTuLY2jmbmIV/GmlrItrIQXLzOu5xt5HuOansC9/FgPX0e+7n4YnDPzY+Krnqv8KIampCsam+Ip+QqingFsVLQDSaZBGQXPsJDncPAUurFR'
        b'FY0lGnHGTXtozslglTueCjAzqWw5vjw6PoB8xFGJ/Fg4ti7k+dZpfDGJZW5BJ6E/ntF5RupLrrPfzI+E2KM1/SwVw9uuL7Oxgd18SazFC1gYjaXRmsDV9IeYNrovkqU5'
        b'whONRHT+jv9Q/iXGI05itkVegkcji8Ro5CypvS3dYlcppU1uPMFyk8ilLI16hV7TbC+j57B45WXSMygjwB4WpnxZviQbli9NGgpd2NwfDwtdqmeMDl3wmiqKfDapeL+Y'
        b'LolZ8wS0yqDEf7ZGIp5NNgYswuKY1PRhRfnVcHPMV0OGch12CECuW5oqHfoKiORvfgWEOew0jfzT745Ar+0i+n1BuJ7Ko23uZ4eXvP+n85svhF87l0bCrzLOspax+AFe'
        b'2va34NcGvi1wYTQAYz4+FmtjuYF4xZQDDdCtsFVTPabwJ9Ww15MMID4Ai2KxZAcWxEjnOE3cCG1wEW5DLX3QCFs9HOBR6mxD0eWnMhPzB2Hub/w6yf/Dl0nCntf7Kxqr'
        b'JJGLby8KSPHf5aeN0yrfXBSY9FHSnm9M+/brtRJhx8JcD1eHZ7c1CjPLw2es3TMuemzGAZYiXNwo2u5FrIX2l/UeqIZGQqCSNWb2QDkWU0DrFxg1VO85oxMrPqugz8w0'
        b'mOLJ81gxDE+CErDRBiibsEQEgHvQDTej44dVhbACeqRYthkfirYnHdfAHdL05iHz9rCb9xxm1rxiIjFOGTLfNplYqRg3t2iTiI3cLNmYaWQ7pomiWZ4TfuU23DBZMJ2U'
        b'4Mbo7XYcUciCHrj2JVYntQr/sNW1j1DaHdkZBrNpyLTEkwayHzW7m2rUpvGTg1FmZjdVrTp03PR3RGefiPidcQnb9/qrIyI3RkTv2BlLeXF4XHRiRPyGjf7q8Ajenhi3'
        b'M3b9xu2av50sj2dR3Fuf0DsIq+aL3xErCN8pWJbTzSXJlMsUY4kf+4pdYcy2SLG0w3IVrNRAmzPUYoXxBL1FQeEJAeqUzlCA1Vhrmcv0qG95KhbPVr0cT6bEMXEWtsrh'
        b'VhA+Nux8NiAxbaPOX/X7r18n7X+9i2ymOzd4SsrFORe7a6IqGy835jfmzrk+EHk7L/hiW213YbfM55Vvdp1ry82ZowvQueq6vbfmT5+3A/vPnZgTQU5qhlCsntBZ8gON'
        b'3MygPTs91C/p1PDy6O0p3BIWUtpZKxqCH1jt9sYNAXrxOXf20/E6dhIDmuKHVS23neVtp03YG30Im7jv9lEKTtOk0DhdNiJFHt9MnCnHMA1LyyfZLSXYUeLCbcVNTM5n'
        b'DFmLcero6aYN2Qfr5TPCPgZH2Acz6anQP8sv0t837mVVYQo8jUqXT8YGN3JbrEixA0rI2xezVkq9y4OgiEwJ7uENMqcZZ+XpeBtKvtiabPU6/uXGoXrd32lRPzswul43'
        b'3JXxwlam9ghPccbxYCzBYad02Xq6QZ5upE+JEu0qQ2s2U76i05I7Gjkpd2zaFLEkOCZTGzHXUNb2ZUmbmKT9b/WsknFxwDHOwspdJPIuij5F1wqVTn/Lu47yrC5eHEni'
        b'Q6YLixJII5OSTk/dH2Q7SKyau8KUg83L7a4WHkIZd7anoGfLCF+7Ae6P52x3nuCzx510EFxS4pWEU/7rNi8WDBeeuMtMe5jmL63x/lb3hHNqD/nrK3fcmCVNS3/9hyt+'
        b'c2HKmsWe62O/8t5vpSt2Fobt1ZUpvvWt4g9dan4V9nFx91vfr01K73z/z5Nrvvtsyv0zp6ev/fay3/8lu+R+5NWPp/7hsylzv5OtUfIaHlbiedrlcA8dC7eGF/HuxvDw'
        b'fgJ7IMQv7jBe4iE+d6O8bI5lhDaxCmFpnPJMtk48FinB+3DZLyAFbr1EqBXYzJ05VC0U/AKnYGvUqOMbiie5oz7ivE4VrUXrS2duAzBy1xc40STJ8wnRI0iYnMSJmA2V'
        b'LC3pxMf2kP7Lyoku3LuTYjOz4cA1xQ5cGxlcuRDgiG7eRWL0GoIujWxQxaAuMcvIYoNhDn/cBYka7yFoY7OsGAFt3xhRTmTfkMIBqIWC6Hg4Jx/DaXGTodimkcXFbdJI'
        b'NmmkcZsMcQN9UtPvadrOD+7vvPT2Ds9tk6y/G3j60abqannwuYFjXz24TZb89aItW7/fejPc9da6jP6VvoUfB8746scy929eP3vnWJVLk+nD795IXO1+bMGympyZ/7ou'
        b'/BXT11IGf7rNe72uqchzSclHpkzpb//w52dX/6h4VdEYFr7sA9PglcULQk5ENatbPjg37fAVmN03/37BlObvuRV1pz959z1FwVvr5saGei4MV6nS9XOiBtNbcjf6pzpF'
        b'7/2acVdX5c67qa6H9379ZFjXpdiMVNWr/7Jp4Y//5Y24o93XV/9GP/uz5Yt+8FGt1795HPCqX5zxxoSyylvXZ5W99WZOXHbljhsfuqR99L7XLx4azxfv/8GP9Z8+hp0D'
        b'B3TnQnNnJP5CGeFiqno1pf873nW//dGPD/w2/1TK9J+tcT8eWbZtVvDXdH/Z9PCTvJwFV3+4O3/J2xH1LaveXx50/JuT7n/46aoP2h9smzCQvGxJc4bBL/qHOdt1GBaw'
        b'MywAQ/y+tavH+N/ul29Xwq5M0/KktiJzzfynebvOPI3NfKd098ILB0L+/LM8r498Fn4YuiI17BuH3500969n3zl/Iiuvb37uzcHpb/re0fzQO/zFzeSNJ38++3cr333/'
        b'vZ9/9Gh63WcfONaV/ErlGrffNPtPe9489eDyrYTK//w4/nRgfsdPGj8Pvf1w7/Mfhn6v9XDi4eU/OZwS+/z3A/Wucz/dOO+zqX+4+n8mlxaTKfMyby+UQyu5OokgWQY1'
        b'UCxgWQJ2caNLCwofHh1zg/LCKrnjZDIpFqa/IviqfNVYPm6efx+uTuGGHbSdkuhi/yh4/CqWBigF5UHpXMo8eszMW2/HLorStwQcwqtYEBUTpxBU0C3Fujnh3KzTsBrq'
        b'WZpZfhRrAwhlS6JYj/tSbE9z/wePPzVu/9hp6RfOozAylzHuhaODY2JiRpY2JTGRI8MG5mPmSqVSSahk1udSKTsYnSh1lEuFcX4l/6S7n8md6ZNE+helI3//3/fbq4zz'
        b'kLBfR8lEGat0eK2VElpO8nQmTk2TePlIWYsbv3qwq3GWHYMJRqWJicPQ0/X/X6YS4+whqGULsaBdPCT66YLRESRcz46HYignxS+csjw+Bgqh3EFwmy7zxvx9hk9/Ga8w'
        b'1VK37GeJAcWrnWHdpLxfHAl7sWmSv/ytr3ken6rSaVZt2Lo93TdqhfZB3zfe/eGBS4bU5+Xbtq1a1PD1eXW/D4kM2nFrgXnu99PvLS6K/rTzrJ/JuP5p3y8/OfWfGfJg'
        b'56lnLy44KE/rtSqbYm67v/jG09BP1vk+/DzsP46XvvF/PzXJPfel7t/a/29Fh2dk9n/w8Yq3Y/4j/meLfl7wyV79fylm7dG8t9SgceVRP/ZhC9zg/3cknrZSosXL0Q5k'
        b'XA+k2LoVa7j97SSv2M5Ckm7Wi1XP8FL6BHwmg8YAQcyiS05DrsiN6ClYSigApZwdE2WzsCmYgwx27MKq6KhY31gHQSmXarDYEa1w3syirpjli/y2JECeQpBECwQCxVBl'
        b'ZuWwk5jLH7go20TQMqyyAWVB0QQzZeTbymXCZuh2IAArgTqRmDwLpWGjaiEHVyiFqRvkvqY0DlqEdkVwDXuwhPAk6GCgb44NtWZY5JCfCXkcl/BpDPv3B1gSjcUOAp7D'
        b'RnmABO4dgWf8cHIllMzksUTQGd0wcmbCdTnc0UOjmT1aGn2KwK1YQ72WMpCkAFEiuG+T7YQXejNPChu9sFXsQBENbQxuR4rZoURQ40OFMF8EwYVQp/CL98ciRg/chKdM'
        b'TPhcin3QYBmRZHn/cxDun3jRyL4IIg2ZBrMNItl3QAVXFjBRzieTSxgQsLzPgwdRLIxyls1jwVWQUT0EArMHZRn6zEE5O3cZVPDKwaCcMhHzoDzFoKMrZUGZgzKT2Tio'
        b'SD5h1psG5clZWRmDMkOmeVCRSghNb0ZtZhqNNmRmW8yDMl26cVCWZUwZVKYaMihHGpQd0WYPyk4asgcVWpPOYBiUpeuPUxea3tlgMmSazNpMnX5QyXMgHT8q1mebTYMT'
        b'jmSlLF+aKBZ5UwxpBvOgypRuSDUn6lluMuhKuUy61pCpT0nUH9cNOiUmmijLy05MHFRaMi2UsrwEN3Gz3kZ2FGxkX243snMHI/v6lpF9K8vIvkFlZNGfkZmNkT2RZAxl'
        b'F/ZdQSNLK4wsITUy3TeyQNjIvl5mZDUNI/varpFx38i+22Zcyi7+7LKCXVgEb2SKamQVfSMr7RlZXmQMGYJKJg7nIaj804ZhUMnbPnW0P2U06JGYaPts846fzkgd+c+g'
        b'1JlZZjVr06fEaRzZ8z8pWTriCX3QZmQQ4qttqsOibrrvTOw3mk3HDOb0QWVGlk6bYRp0GZ4DGtfaGTjsIurfKvE/Tq1hzpnX5+RKucyR6Vj0JAlzN/8PEnsFJw=='
    ))))
