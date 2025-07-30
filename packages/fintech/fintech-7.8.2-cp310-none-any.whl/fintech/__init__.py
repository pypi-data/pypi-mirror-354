
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
        b'eJzcfXdclEfe+DxlC8tSBKTZVmwsXbFgDXbqipTYZRd2gZVlwS0oZFEUcelijV0w9o4Fe4wzMT2X3KVcwrW0S0y7u7xJ7hJT/M3Ms7tUo8m97z8//fDsU6bPt8/3O/Mh'
        b'6PFPhv/i8Z/Zgi9asBhomcWMlm1hdZyO1zFVbCuzWJQPFou1nJbfADQSrUgrxr/ScqlFYpFWgSqGAQuAVpIBeKBzK4tjwGIZA8o9tRKdLNtdK8VXOb33oFdPnWw9o5Us'
        b'li2RrWJWAbcNSrd7A2WZBTpFWpmloNiomKM3WnS5BYoSTW6hJl8nU3KfSnDTPpWSC4svHUxULtOlBxz+kzh+zWPxxQ7yGC3uwwZpBVMDqkAFW+5mY6pwK21sFWDAGmYN'
        b'm9HlHrciT8mpcrsOCylwAv7zJYXydGgygFKh6gBfk8+ZBtIcWwEPpMOncyBeHXG33AY+EfL+67HjoM8W0sLiSAtZO7BzeZyrlcwjtTK/ZyudhXdvJa+yRuJ7L4UpIxLt'
        b'QM2ZqCbicVSD6qPnJ2QmhKFG1KBE2/NRLWrgwKwsMTpb4KN/frUfYw7H2V4b98Ln6s/Uhrwv1KG6iA8iNQmaL9SvLAnL8cstyDOw59cHxS0B6zZICvizStYSgnOYeLTP'
        b'He6GjbjocFJqqjUyDNVFs2AIvMCjs2OWW4bgZOhmMNoA6+EmtCkZp4GNcJMEePpwsNYyGJ4NN7nhNEqugw1VmghQChfy8p73lDxTcbnOqMgTYGNah6fGbNaZLNk5Vr3B'
        b'ojcSsDCL8UUe5MnwjEnuzHqc6+DzrMbcDkl2tslqzM7ucM/OzjXoNEZrSXa2kutSE7kcZ0ye5N6dXEghwaRgP3zxvitmWUbMkCvPiH8mV+sw/AHWJWckM3ERUarIMFg7'
        b'zzG6dGgjYkXoOLzBGUhL+CEvMIaEPe6g5Bnmh4X52j8BCkLvAwtridvjA9TrcvZnpZsdIPTeY/Trf3xXMG+yFglQqJeIpFYhy+l5LODj/4EBTC3/2osTXuZkiYFcvViE'
        b'U0YMnFMKrFFkxI+moBp3eCwCt6cGbcqISRegIDQqMhTVRIclpjJg6Sh0aIk0ZQC6oGSsCtKhw2uecMedSY6UhaI6eBYe41egWhAMb/JwNzoz2zqQlHxqGdxF5jIadxjW'
        b'T0okc+k+j0VblnvSUhbBC7Cm12THwOs+3GC4EbYrOSsZVrR57jR4Pi85UpmUKgLiDNZ/NKAVwBuPo0PJdDQTE9FlSSQL3OFOFh2DN8VWAk3wSc8iVK+dOw/VJaVGodoU'
        b'eJIHPrCKQ5VwP2rC5ZNiIuBBdCI5MSIxksKlCHiiy+gKquNUAxKt/XECA7qOrifPIUlEgOcZeAC19hMqOD0qKBy2MDRjaiJqVCbiCtBWDl6Ddjpag3GqFcgOryTDNtg+'
        b'JhanSUZN83BBXkO5yegmtONEpBUDUc3I5Dh4EydJTBVSeKIz3Gi0F+5XsnS8Useh6+4JeKJK0OUFqB41JCfiLvuhvRw6go6j09aRZLS2wkOwyR01RUcmqawkVSK6FDcd'
        b'1c5LIanHLREnroQXcdcJ2E6Y6YfqI1SoKTECXkiIEuPxu8CiCya00ToIfx6LDvuGo/OZqCkFT1GEMjJJBHwHc7iKzfCqdSgZgCOoZWIybHSfF5kYjieiNjEiKToqIVUM'
        b'IoAI7coLtQ4gqbbAA2rSlHD8KTkvigHu6CCLLrujKmsYQSO4HdYn0wSk72mhyZg2NKFteKAbMEimRYrBTF6MKhOktNKJgVqcFnfIF7bMD01IQU2qlHlZJFXEJNFstLei'
        b'G/1ju1LpFkr67Qwmrpydt4vsYrvELrW72WV2d7vc7mH3tHvZve397D52X7ufvb/d3x5gD7QH2YPtA+wD7YPsg+1D7Ar7UHuIfZh9uH2EfaR9lD3UrrSH2cPtEfZIe5Q9'
        b'2h5jH20fY4+1j7WPs4/Pm+Ag4KCGxwScwQQcUALOUKKNyXZGl3vK7HoQcC8HjelOwNeprCPw/Vp4A25J7puywNoKTFzyUDOdzNE6tJNioypSGYnxDuOajzrAn4Nn5OiK'
        b'1R+nCMf4WInqYe1cDKUcYNcy8ehIPAUUWAsr4ZlweDwiAaMA3IBn5jiDqtCucGsAAbojT6Dr4cpITDrqOAy5YniCDbdqaalaWDeZTFcEnnY+0WcSA2/OhmcoYs0pHpaM'
        b'sZJ8cIObVjDw8BwMV+QL3DarBFOhBNIOPmGODwMvFI0VvtQHLA9HW9ClKCULWNjOLC6EB+mXsrlsMjwRkQgPo50YFsQGNjRUaw3CX2R4kKqTUR3ClAbXNWwW2sHA056w'
        b'1RpISryM2gl0Xi/F8MfgMpuYFHQNPUU/oitu6GgyBTd4PCSCAeLxbMBi2E5rXIK2Z4UnYTxkUubhTseznuhWFq1xEC7gKAXo0HK4NxJnW82OhtfhSUrRYKMB7UoeClBT'
        b'KO6DkZkGT6+hBfZDO1biCbjuE51EGrKTmbMUHaAoVNYf7qMYoiRYLIW34CUDi2nMEbSLFhmpgadxziNZqREY5G3MY/DmIlpkLLzgAU8ugRdQHfkCLzCZ7sl00uAtdGZk'
        b'MsH+pALUwANxMCuLQjuFCV0Hd8I6VD8UXUqAp3G+CmYO2rRCyNcsRXtQvRG1zosiraxj5qLdcK9AD87jUW7HNAWjL8b2RDw2KnRTLQIBBfwYTCzaKDRNwVXvSg4nnCOJ'
        b'zLCbOGc0i2lATUAu2wXwCax3F4mwQGRnXCIRW4MFnwoOYxRLMYqjWMSu4TK63PcluJF/vUUiTqXvyH6WM0/DL4awdz9Xv5RzV12Tfxf/8n9oiN/tlhDL6PMUHs8uqkiJ'
        b'cF+4bsqO6oYG+aD47/OaJ7V7blSLf2cBb9z1XPNSiVJCZR60KXeuwN5Q4zwlakwkHC4TPiUB/iN4Dl6CNVTmwcgC13WywXHwqEvsGYwuT7QMx2nGTI0gKWDTpOiIVEwU'
        b'azsZ5hC4mUebS2GVhbCRErh7kFFN0s4jINtEUshQM573sGwLYUZr0U2d43NKFNyRjjGb1MVxQ9F+VGuhyN4MT6ID4ZFovTmB8jwpusjCDeiaykI4DFyPrsMDlJTAHRgk'
        b'XcxBaM+IMNE8dETuENV6CE/0LRWdOvgijbmQCmVEnJKukTLkvycjI8KZrzOtku/gtGZLB2c25ZoIJTR5k7dsZ5H4niCAqb+zZJp5LXAKZVV9CGUERX0w9lxD9akYVMWA'
        b'j0AnHsM0AY/BpQeL5eMFGGTz2P8NoZzvCwLj2Q5gJsDzN+vQz9VLn3n9dvOdd243P3exeXO/Fzzz3kuRgGz/+Dj+h1m7sGRNyVezcnlyRCgmlckMJgw1UniSLQuDlRS2'
        b'YC1qDnLAFrw0rKtIPRg2TRCGmO17fqwWvcElNIO13lI8L/6gU2jminNW9D0lWEQOdM0GyVJDiiE3YJ3n933MB+3HZhHcE05lMEyjTWgf3MvAW5qibtPBOP4ynO2y4Vs8'
        b'vIxKaHmQqw+dHfE0FmcX5+RZzbkai77Y2IDffU36xbPWUPwjQ/sxJNQjOkjzksIjVSoiC2PBg6Mc8fxKEdqdjXb/1+1wczZC10zeEapOGfN4dIGQTEfVGN18MGO9iRnz'
        b'TUwnHwyMkwgwMgQcsZbI/0qA7EUSGdAXSRR1T+QkyENc9VOCbOdd9T8qSe6FEKR+WV8IkXJRyppn4RefVt0/+cFd9RfqF7R31YvhqY53ng/8nfcrz8A0mKa880Lay8+8'
        b'kHbn7dtL0euvLHw5Db3+7E7W72RuaH5E/nsGBmhOyec/U6ZkKA2EDbzNDE8nqLCK45hpWCvph5o5eG5GkZIR6Arfk3b1QBBRdq7GIGCIN8UQ1t8b0y8pBmhpJftzebC5'
        b'QJ9nydaZTMWmqCmGYpzaPC2KZnKSNl5jyjd3iAtXkd8uuNRL52RNpN2mIS6sIoCzoxOrfD7vA6sIuYKXfdH2cMyNa4ZMSQnHIiLVutEWLA/UYgahwgIFbMcCfb0kfSLW'
        b'Ux9zw7rPTrN+4suvcmYlzv/t79YV5hfkG/JVuapFAZoUzYr3j+nuqk9o7mLtX4bpEQd0Z8Wn3b4TuvSIQ+feZWi6kpj+MrFpqCupR19DYernGgOScluXMfjyAeo3Oo/5'
        b'2Q06CCnp812DwIIB8BoPj6GrcMOD0ayXsejREKyXFE/+sb0AnFdl6l/ZZ+bNhMkPX/mHZA0RORI0/JYGpWK8707tP9TSvPdeAeDp/+S/K658yqTkLQqctADuzoR70B7K'
        b'yVURkSqBrPeDFznYhC5MsBDjzmx0xZeyaazKhyZFRsGmeXgMNoUnou358HSowPkXZkvz4D50hIoZ8EgQelKQDpqGF5OkrnTBaDsP18PqUlp/nFswLVmZlKJKTcIamCBp'
        b'DMea4zDRoBk+XaGhy7x7WI25BRq9UafN1q2msp5ZTmdePERMZo6w/hBnFiVmMThVJ1ocd0AXYxrmggGSen8nDMg/7AMGqCx2wH9R5vRwqn0nYJRvSE7FcIBpgBiMKBfN'
        b'm4/s3WbLCQJE3nVSOqoy/veUlgd9sX6pykBG4tUsN6l2DlDo1nrwdvO7S5fnj/c6wLOAis0BaN+s8MhEjK2XANauDzKwaQS8hDX/U9R69B/ma69tXkxoZew95ueFx5b9'
        b'QbD6/CuCWeGDZThQohlybEWW8DJhoE/8RpCA79QD97hHAP3wgtm8uRg/L1zyWrJGqzmmO6b7Ql2iqbl0SvcZRvfP1Ma8MJ8TmsXPNMOLzf3CnpP6vXFKw5744KTujOaU'
        b'xv+D7ZLP2D/IQ9STqt9lEgKS/M+/FdP/Xe7OrvSFAwPPHWdeOtcR+yb7asTb4hN5cgrRcr9BbZ4spsiEV3qYgrC6sSXZZR2Rwma2GDWV9k1KHkpg+AKNuYDC10gKX9JR'
        b'UixYkv+CmClj2J94kdzxxP/IVvIi04hOyBPIbSdB7rsVjJCMAiLJfKQLMfrTA8ScJRFoF6pPwFInBoP+aB+DtV5MgfY8xBjM9DAGs7+NCpEhcesFfHKV1YfgSENYJtqK'
        b'645G1RIQDVtiKawwYSLwTjTuVrw64u35YgGA7gzjQKacFKWWRwTMBiZCwfu6dDDZ+qeS3HhzLX7QH78T+cpoTxjjPev3uy4NGlXT9E1u2Lj893mld/9X60IS/NRu6/bK'
        b'ZEPQ08r2mvbVd5p+/tOoxL2jc273u3x6trq5/kbprOu+fr77a3a+Cl8wbA+b/WZDwpXdPzz9U+Htv6tOXwt5y/jW2X+/+uyFk9fX3vk87bu4N1ccsL8wI8QQEuL72MZL'
        b'EzTf/QxGjwj5pHyQ0p3SO3QNXkMOEyTmEru76GmCkoZa3agqtwhtHm6OUCpRXUpYZKLDdI32zQdhS0RYmd0HD1LtC7aNmo8uqOBpS+RiuFdgMh6okhuL9gAqjyvgMZNL'
        b'1UONaF0XeXwAqrYQJWb4kFHhUSMMqAbVEnsDbGIji0osBL5EDDxDyW4PHRAdQucceuD0qVSFMw9Gu8OTMGRVR6KaxBSVCLjDNtzgQKOFSA7wPDwE7Vg/XwwvRYQpo9Am'
        b'LPICEKjgly8cQAm8eDK8RaqKgrvmkboEJkA1yXbUjOop1sJWJtCpekyAGwBVPeA69CT9KoIX4elwFU7fHpmIx44FciknjYaHumlvv6AhikusOQa9wCZCKRqzkzwZb4xV'
        b'7H0x64cxincgMEFhsUjGyPF/zEJGucoJ6LOKIBfWkpRXO7HW+4U+sJaMJ8ujuvDQVFSHtWYx1ofPzYY3WFiJ7INpPbniLjhGUEnqxDEfjugGNiYIVIhrJDZxDahiKyQ2'
        b'iXlkucTGtQCbuJWpkC4ARjceWJiyAQwg/xcBo/sqLDHbpCSfTUxKmAK0DMlpqrSJSsL1oEJkE7WwrWAWWJa6lK1wq5CR8m1uVaypgtbE47tMm7iFa6VltPA0rbzCvYbD'
        b'6dxtbB6nBzbZIaaJYcDKOcYQmkuO2yevcbOJqxjcYlmNlNxVMTSnlOaU9siZa5ObSmvkQg5nWxlKWVbGkCst1x23ZksNUwNKgWkLbo1Iy7Yyjn450zAWcR6L0x2ucafp'
        b'DtewpNQeqcQ4RXuNiKbAv91TaLkWiZbXijZgnXMWqGLw6HpoxS0Sm0eLVCvRSltZ8sbmYXpN62bz8AcVHnaJ3R0LeJxWhnNJbRzJVeGJ++1ZxWilhazp7zZPrTueB0+j'
        b't+stb/paKyd12TxbGX/yjdV6VHja2Gas+uJWMqSV+F6i9bTh9AGYLOexOJ2XMcTG2NhCDn/z1XqRe8d7f623Tbjr1yX/CG0/IT/9wuM0pDYvm5fWZwL59cBpptg86dVL'
        b'62vztHmQ8sg3o8TmRb6UTLd5kGeLMKekD964D36FPM5lsnmTvmn7lwL8tFh4wnny8Z3U+b5YKzyR97iX/bT++BloA6rZIGDrR9vvjWsPrPEgNayQ2bydbbCRfm6wMDav'
        b'KmY9Y3EXfrFMFKTKvCcxYH3cGDn6Hhuh6Mb9WAcHpMo1seHkYxRaJqpgbMwKsJldibmcW55DwuyQZmcbNUW67Gwl28FGxXQwlp56t2yKQW+25BYXlUz7jpTIUhwtH5hb'
        b'oMstxIpXp27WmfAepyg23WMiPiXtuicrzlNYykp0ihHmXg0VOTFd4WyoO1lRthEWzZrZGtzoKqZbo51Gl3DKHUt/gQKaiBT/o7PNg8GnpNJ7XhpFqcZg1Slwq0JHmJWU'
        b'zd4LNOtWWnXGXJ1Cb9EVKUboyedRI8yj7vWjL8it6xVPr75dUjpz33NTFFnNFkWOTnHPS6e3FOhMuNd4MPD1U8HOc48ZdY8Juec2wrwkKipqGX5PJNd7/SIU+cUW5zhN'
        b'wn9KeYdIb9TqVnfIHicNnk3UPfwK12ru4HOLS8o6+EJdGVaAcc3FWl2HW06ZRacxmTT4w4pivbFDbDKXGPSWDt6kKzGZyFJRh1smroCWpPTpcMstNlqIPmHq4HBJHTwB'
        b'hQ4xHR5zh4i0xdwhNVtzhDsR/UBe6C2aHIOug9F3cPhTh9gsJGAKO6R6c7bFWoI/8hazxdTBl5IrV2TOx9lJMzpEK63FFp3So08R9NdcsPyY5oJSqRMcXyXz3UR4CEtM'
        b'oSzjSZkae1/KSx0sz9shycoZf/xexpE3/g5miJnj1/x9H28f/Mab8cF/fmIf+s0fpycs0pvhWTH+9cFPnoyMlROjBSulbzxZYoINZDBzvc/isv1Yf1wiLpd1GO43omqi'
        b'QaWiJlVEkgTI4RnPbG7i5DXdDPeE+4mdePEBvmBuxdpAC6AcKB9zK66Ct3Fmj5ViCxZgyZ8ec7e9HOFpNtbGTcH4YwrF/I/BND7UhnlFEGhhMbXkgkAr5jmYD/GYA/CE'
        b'W5jH2Ph8BpfH47JDMc/iCCfBPCIVYyHhDSItKU+k5XEZHHnCv5gXknJWjhU4jClDy5dkaglnFtkktC6x47tIqJ2Ww04B9Jl3PPNTwEqxjWB2gVKkwog8j0wnndP55DLP'
        b'dUfeKUWmmWSmObPO0sFptNoOsbVEq7HoTLPJV2mHhABhkaakQ6rV5WmsBguGXfJKq8+1mFTOAjukutUlulyLTmtKJ+9SSWbxQ8CtizWUuENos53lDmYcOhLPelNo82Yc'
        b'kEDnncBLIOONvxFYwsIQkZpD4cZ4x7I7rI0ma4KpwipeOLwcmihCO0bDQ720DlI5MXnSynotwAKyBJvn7lRvbEyGw0bYUytyCVZafKkhE83UYla/ApRIMZDhjKZgDBge'
        b'+A1D2GgV447FAsqoMEhg9sfUcDXu5L6WuNfwuCGkehlujjxP6jJiutlYAkJ0YntoUASuyZBSG+hd0gjeRiQGUJ6FK+bIPZWWwjDEs7gy3LQqphDgZuE7G25IBWd0p80T'
        b'Y9geRu7wG5YBxn42jr4bV0PkGYwFRMqqEROYd0hauOG45CEVnI2Wi9POrhFjWOWwTMMbxeQev6dPNt60gPAejEO0HBvvKCMOy5o+WNbkLaI8tqyQwXIkA8p5PFgiwpu1'
        b'+HmNiHhdYczAWGljSD46EIwKgxlReDskpRoTtVxy+RiUMVU1Fa4yzSAgliwAY6exMpNcKOzqKOzrTCal9JGpZCfYyrMpfSzBFReZpxOgjSHQQACW9aSEDRNHTLwCGbaS'
        b'EE6sCbA8JmNYsb/nI5ESi+x9T7Y8RpObqyuxmDt5vlaXW2zSWLqbaDurwnyaTD/tEUZw6vlDXxSSF+6/lfJzHRIygBiPhSK1ro66uRoUxzjXxjjCCAbjPgazsqDy4Af3'
        b'wSla5JDiisi97DexpRxXcySOysYxDoOBguOHCes12+HJjOQUlSpyFKoMVYqBexSLDi2v6GX1dHP8mom5SQcWYxhbzG6TCCYNjP/SPJGAeFXMYo6+p55vDurghtGSeBWS'
        b'r7wd8GCxiEhSSlFHP4cX4By9QZdSrNHqTA9ePSZrupTkiKj3hzhP7MJ1/rcvWPReMJGoqMcP2ooOOdbrw2FdAXFqQc0c8IQnOO/yOOsYkuR8OLpBlp2ow12n7wtW+4kR'
        b'YjNqI4aIS5jELw2VoG3LUR112PNF1+KFXKGhqC46IRLVweOZoUmpWIWPSoxMSg1A1zEt8XKbGgtbqENQIjw/ISPy8QTUoExKTcGJiWFhXkoiqvRLZcBYuEM8PA/t1d/7'
        b'PpgxE4l7W1PR5+oXc47p3jhzTLPwmZ3wSnPbzrMblNXHN07f27qrrbat6vhC/oV8cVth4KSFLwfWfVRp2xEsHn3O5maWzJSYY99gd3juqG64Ld+rB59c8Tn9QbZSZCGK'
        b'eHLIQlSfTF2sYE0hP5iBB9FxeNBC2EJa9vLwqESXLSIXbRDMEWXwNDWcBPCoGl1ADZHEJ22lw34fbOXRaTXc6F5iIfp7AryBC4lMWD0tkgVieIiNwRXUWoixOHIw3J4c'
        b'lZQakQgb4DHY6FqSF4ERc0WL4Vm0xbl28eis1CPXpMPsO7uoWGs16KiZgmgrYC1YK84nJIgQJCmVuMqH9ALWqG65XStCZp0hD18JZeg0P4oejKysaSW5NzlbZSohsEiw'
        b'lSApWAfW+e/tbdR4aHt6oZJrcW6OE5W6cm8G46nMhVKiR0KpXqxVBLqoUy6U8lRR57cwdAvtgYfgtk4/MRdKwQNoh4BUR+BBeAg9NfXBiNUVqdCRbIpU6OKyib+IVAzA'
        b'6HiLYJWv/JfXgUmT3TY414Gxfsrk9dRHpVMMmqIcrWbaE4xDs+OBdQFphh1dQWeWoiqzq9UlDgc+wX0PbUmGpxNSYZMLfNH2bgt53BgfM9ya7oNOA3gKbewHK0PRTeqp'
        b'+ESsG9qy0GHpbED1EQ6/j3RuNGqHO7p1SgS6LPNSyilISiyZcBfl5GrwZFbweJo5Os08nVpuDZ/R5f5BS80uMa4r5SReestiMN0kyzRRwspsRkI48dvKwmgfqURNiQNT'
        b'ErNcM4npSItOhp42qalN+tJKsswBFDGlQwa+VjELWImIsAaeQQ20xP6wxVmo4OKKapxr7niCi9a6BcLr6JA1lszERnQUbUsmNtqGxNT5oah2gUA157vqRpuiszAYoTYJ'
        b'Oota0Cm9zjdHZNbjzP+Z73Uy/TPiPVS7Tv1iXtQHYZoUjSHPkPOFOiL9C/WrOS/l/C4nUbNF+0LOad3d+A/eigFZ4WxWbFWmPfajr87HbDuX9VnsmEpF2t7DVbP3MsMX'
        b'eL75x9vNL75++8aGtk2jd66LHQRWNwV8cfwfSgldzQ4elefyMgoE3e3XJh0lf+gi2of7guknanHvSUKxTteAdlKrryoY2h1ksgeJlEYvRntjqfF4NroFdzsWCefhhCM5'
        b'UpsHOs8FBjjW1y8MQFVYTaRJ0KbwKCwd+KyRR3KogUUXqYF64qxiZwKy3OM+gU3BzWssgScs1I9sKzof02OJvh9qxjlucPDcLFj766m1J1l4zy4xYd2dKE+UXA92kGuw'
        b'lpVSCZKoOZho85XEkkwlxnG9CaVutS7XQSY7ZbDupQvYLxKEu05p+GELSo51J09XBkrRrfhSTWhFsIOiY5p+rw9D9XJA3P2uxKAd6PJvJiHEeXnLRNQmmo2uxsNLI+Bx'
        b'JQhB2/1WYMi/ZSCt1GQF8d/4gPh/+X4/+e9s++ipc54DdAHyxZxdzDkJxr8gY9lurz9b1cJr63BhXfJfYK1hxeKXQ+8Cfc3TF3nzcfxt/o8X+zdMlqEY71mrhr97LzA9'
        b'yLTlm9x3rs709A6oHxqVuzVpRUjV+NTfqWd6Bl8N3Pla7rOp3wxt9WgY9LV+/qkNv9v21cZ3rp5dNGS/x4Tw2uuf35E+m39p3AelLaVV/hMu1c6avduw/eUTWyIvX/pP'
        b'9JTolAlhRy5W1w3xWFJ6MvlYYcL2gTNmZQ4bPLxxQ8OQpxPKP30279w/a9GuLccb/Ad4rFoQnPV4y4dvnV17d2LkDssipZyKIfHoKXQsFjb3EaIweBzcQ/EDtbpT30dB'
        b'mJkjcy2twKtIgG50De2F+wbE9iXQYGw8/riFLHdwvIeAZc6ZhDV40vAsFgKBeI/XipcZ0SnqBYbOwZ1wG5Z+ULtvglP8QSd9KVo/Aa/mxqIbPWdeBAaM42F9xky6xOUx'
        b'NNVBRgRAqZ4L60gt/dE6DtOPQ/AWFeLg1iRY46ZyCnKCFLczhQpgUzGGnumvDE+gXeYnkOWqvVohsOMIPKlDG4s7XQ9dfofwSXiBNhPVaNCpYNjaN5e6kWGhvrMts3zh'
        b'Jj9Un8IAJg5g+lK19Jfko9+mAIldZMO9C7Z3WYnCIp7FKeLJqOlEjK8yrHP6sGIvrHmy3qw/Uz7oF6mHQ+ijElyH2PGuk0Y8sp6MhcBV5H6li2SU4svKrkLg4E19CIG/'
        b'3DpMW6nFVZbteJGdjdXw7JVWjUGwuFNRk1bV4UEiZjRmc64OU8FsoV9uv2rQjzMdbo5CcAG0E8QdIYd0QkYlBhYPKCsfzliJ4XwYWg8POohc2tReZI4Fk+BNMdwFt8Hz'
        b'vRRSqePXTOJfnAqpDiuZDrMUkXZEWM5htdwGt25qZ0EXtTNNY8EDZ8SDpsrlu5ROQMe1xE4c11yCMhWTqbuem0OG4mukWIYSYRmKpzKUiMpN/BpcV+d9X+v4RIbqLSqL'
        b'VTSUpLgMbhcP6UNODkH7rdMJot2Am1jMXUMTUqOweONQCCPTsUCUEUrseVnS7vEjTDJGvEq0c4yvlxvcgVqVrODt3Zzj3bUazNFRLQ8wQTgaPItP8BtPU6XBpwd1TRUe'
        b'liAGqBLdCjbzWbANPaW3LFksMmtw0uengs/Vy55pJjpnwvUNbVVtVYd36ZkMSaHkCcnzMz5evDF4Y8irnu3BGyM+9jySdyTnU58dfkfynhv5nOfbfh+PmdNSaR7IJUTV'
        b'9085Py72rZhnY/8Yw8ceAqPzJ4GV2f7flRPPbLpO3xAwlFDoIeh099VvdGGWQE5bo+FJQk1r0XEXOYW1KULuU0ssuEOwGmDJEtYK8S4+Og6e0g4WXHKPaAxChAqBRHiV'
        b'lcLD7GqfYYJXeB1WQE/1Iv2KUIH4P41qhLX1anhqJqayEDOcTkq7Bu2mVBhtYtGB8ATM6Z/upLXTVE6p6NehXlcf1TwM0dlE+6S0LtBB68BaWYifnGeowwznh6kc/3n5'
        b'gF6IEOXKLVAAcQeXazB3SPOsBkoyOvgSnLZDbNGY8nWWLpTuIVIcJpHEn9tUSS7ryGW9i9KtwZcD3YWjge/1Qet+qbVKVqVyUDvTanIpI2PhTolRkc5SUKyl1ZjKnYP1'
        b'CwzH9ISraRX4so9xKIaEfoUw1ON4KTqPKh20K28txgmpENTljOiarBDDo8tQI1Vqjj/BYeoTn+MF1CmHvd1BL8O6y8YVD3rGNuVJXLFHzCPFHvVp7e7tLxQkBI+ivdL5'
        b'ZgzIF91XWrESWYMuozZLKbrkXgobvUp8J8pRG5EJjojQucLR1imArBzYi3CG2hQVagxXZVHtPBH/1M6LdASfFsCnE+BpVBMRBdvSSUgXvAivydCt6LCHRstydBX/f8Ex'
        b'vzdhFQlmPdjGSOE2JhweS3HRM5w0k0P1q1AN1bPzl0QRzBc6iLaHw+OhDAiGm/kQeMrkOUn/pW40Z07BCQNOvti/7rZHZYz82agFq2NEOUfOeLvVeqUP2ff+OyHvbv/9'
        b'to/zX/b/2zL58Gl1H26Z6l//hx0BE37/6q7T12KK9s4wWAOf9Zz7/Mr7z+/1mb9Y6rCvhaEd8BZWtkikjz9swETrFBv7+GSBoD2JbkoFwQwdhRcFgoE22gR3oN3QXkIN'
        b'IKguMiEiNYaQFC+4jlshRtXUPId2oSripE5jqBo4uFMP+IkMbJPAg5Ra4cm7pu4ShXAjjrgCZaPGh4aBuGtKSnQYDwlloDTH30Vz5Ik8NZ5JaUwI/0N5GKYa2QZ9rs5o'
        b'1mXnmYqLsvP0XXWwLkU566XU4sGO1ZhgrnPh6wZ8eb47KfG+0oeeRVbh0Da4f0XyvEhYSwRmYbph4zxqrMC/At/srlkNCkJbHUOEmYYgI2vhfu8iuG26YFE/BbdEqMaE'
        b'kyGOHc8CEdrPwIuqNCHktm4g3INxp21VKbq4El6Ll0tLVspX8sB/MpefCnfRaEDMV7ZozVhab3PzKPWQeUrR+VUEQVeKo0RguA9fgeexhUa/RKhGJmMNhVQ1Gj3J4Sk7'
        b'x8KNJWgbxdO5pegCPJmOUXorRuralLCkCHgCbVsVEUpkhRRngESG1BEkzAB4CF5wn4mvl6gZJxedXPOwvGuWdubeYZCh6rJESh7RPh90GdaXrISbVmGYw6rsBQtWCC6j'
        b'c+iyNUWBO5LBw3ULJlB8C1qJR/kkrupJInxsWjgAM+YUCfBCm7n0HHiMjsp42O7bq7xVqE0uiywUg+GJPKwbIDgrUjfIaJMBXhgFD2BonAwmwxvwHI3AM6KLuEvzIhMx'
        b'lp1NSBwhlQD5VBbth7unWqPx98HwfJp7JIl7S14g9LQLjYOXMDGDW5PFYBlaJ4E31sywEgqD+fcN1JKxGLbg2oeD4fFoJyX6WwqkAMNrjJotS9lYXCq4XN7WiIEcAO+0'
        b'2eaI+f0mYqmfvvYYzFID7eshhRHcXJGQ9oybkPY9xhAxXD4eWIkb+zJ4bDSRO8KJXauWQRupOauPhopBMayUVsBWdFa/XPMya34MY8XfJnyRmjZZxY32s722/J+jHpu2'
        b'LiFzbAkICw4OMQKfgy1PhKQ3P96xzC34umbYncyBzPWXRS0fyQZWDl4p379qa5a2bOqF2OKPVopjV4sGvHZ7aOtcLvgl349hose6CXGyK5PaN2cMH5uyc+hHL62vt1Y9'
        b'meP28nfTtxwq2Bx88cUpQ78Nfen4c9byL9ry8p/fuuOTTxon6P6Z+pTbk+ntX6Wf/WpvacZPp7e9N/Ci7bSn/qPqlwue/7D/n5//8xPLxeP4my9MLJzQEhSoWffWy18a'
        b'/x6w6vPf//XInizNP4rUh3ac+eftWZfjvb86MeJvo6ZWffbTrgrNX756e/OA75onjU8Kn/CR27SXvZ4b1vHJj6/lHBbd2iH79E5d7LmYx1fMH9Z49YfL/pYSPupr79dF'
        b'a89qTg+ZNv37P5a1/uiR+OZfL/yw5KexvglbX299LuAV//vGWdaFtmalF5Ud48GSZLIDAlZtty0ixIID7ug8x2I6cstCQMJ9DmzHdIUB7Fi4tZSZPh+2UQI+Bu4KdSjW'
        b'qAVuEJTrC+gIJb9eaAM8l5wSFpVQ+BhN4m5gscZ+3kTJ+xB0hsZkqgSqVA8vkJC+erYCnodNlLzDa/CoJXxeBG5Qff/VGIIluFVPs+jyggBqrSMwf91Ju5rQQUZw9cxF'
        b'mwSLxwXcgHBUkxiRSHkIuoJwFV5TuDx4yES7jWrTFiUThQOXrYxUYSEnIGXcUj4eKxPXBXG3xhMdKfINj+rq9grPokpaPzqjxvhP5CNULwHoMKrjIxl4uhg9JUjDDZnw'
        b'dHhSagqmJNfRZn4oA/cNh2cEcbsVXh/uKJYQY1wGhu8A2A6rUQ2fwOCOE6dbOToatkjpYJ4C55wQJbC+p6JmdF2aIorC6Cx+eX909qFyq+TXWhv698nhKF9cii8sI3BG'
        b'fhpxCZJT7ihjvVmZzJv1YWUMvmO9OW8mkHWuh8tpRKWMGXhfTl17WMGZ6D9yd2+Wl8jvUZeg+7xI/rOp2smYj7NdOOajdKGLxxop5GZ3HhoI++ChdLXmNKye252HYvXn'
        b'ei8+KgLLLVK4HZ56TMnRkPLxjz3RaX+atpxYoCrheRpMh5qy4TlUr4KnU1BTFNxNjcvwEosOh8BbQmjzvrDF4RgE4V6/MDGe6RY2Ft5CDblcDwnQ3ykFErNqr90CgGu/'
        b'AKbbjgGsvX+ev2uFRPRIKyRYCH1/OJ5jmaLLv3Rdvt5s0ZnMCkuBrueGN1GybmkTLQq9WWHSrbTqTTqtwlKsINZonBG/JTubkLBHRTHxDczR5RWbdAqNsUxhtuYIZp1u'
        b'ReVqjMT3T19UUmyy6LRRigV6rP9YLQrqdKjXKhzASVvlLBt/sJThJnQryaQzW0x6Ygzv0dpJ1LNCQRTCSQqyqQ+5Iz6IpEhH8biHfWQp1JURP0Ehl+OhR0atohSPGW5T'
        b'nwVYzfijkN2VfvaMxJkZ9ItCrzUrQjN1eoNRV1CkM0UmzjIru5fjGG2ni6RGQfpozCf+kRoF8R4lzXGWFaVQFeOBKynBdRF3w14l6fNoLmFA8VzlaEiD8FzhuTHnmvQl'
        b'll4d6WUF8gQ9lRV3YSUNXfJFjRnRdBET1sNTUYmR6QsSsCiakZAkSp84ER5XytDVsolwe3zIxP4ANaNj8qBhoBceeDsrSO+OB8CBCYwLE1i7V573r1wd7GXZIqSk924X'
        b'kSqcjpKZ3i5hvZ08hCYC11LlfxUV2ztWS+QI8iVkW//nJcEiMzG8Bm8c/Lk6Mi9RI8+7q/5UXZT3BTg/XTtpZmxucEbQzM0FkmEJN7aO23S1atyghFUx1pjKWbuDlgXm'
        b'3Cm8fW9F4PCgZ8p37Q5KDqq3BAU9M3L9nYCYCP6CIVD290kLA2IyI6K0au1dtXiX9yvP7GLABvGgyqfqlCzlXKgKZIZHhibAbWOooWo3Gxmnpl9gVdp0EvV40J/I2LyV'
        b'QbX583/9wpkoe5VJU9JjvQzzoEE8E4i5B7F7+2Hy7kPdT8uVJgfh6uJP5QDxLm9IiY44csGL8ZFtQccZIQPlNiSuPBi3zDzQxW3AOv+P+uA3j+Hvg2SwKdy5qN9HCGyn'
        b'JjfbRxmdhOUAeBTtmgOPeenxx20P9i6aJGAG+E2h0I/oBiFRWYmHXRG8OD02ZuyY8aPHxcLL8JzFYipdaTVT7egiOo/lvDZ0CctjUrnM080jtr873ARrYAOLFTR02Q2d'
        b'zs6n+sHnS5LANr5BBLzVSWnZ0YLScKIkETSnpPNArV7Rf4y7A8APHRNzVPjYna/rf+rL51v7VcZ4889cf21PJpBuzLsL3KM4VnQv+86hhkMZ6zvenfW8KN9ttuzCqbiP'
        b'ly2d4rdz+It/8LjFLU3NuPLtsmtjfs6vvm2ZMeyrZw9tf+45j69+BCdP+CleWYphmfDbnNH5LiNCOTpAhUzfkVT+XcX2d5kfwFjUQs0PaLvxl9Z+HhYlKM02FVuyc4iu'
        b'3c3YiYE7nMcA7UdBmnhbl0c8Elg7inOu67j8c3/JAsEKKTqBuh5fQnsCtc/bfQA1seWPHDLqkWEa1UVjWeta9Lwx4zlQCuu9o4bDS3Tq7fOJlREk3PVQp4Ss4gHVTkPg'
        b'QbgVbRXp4BEAokAUrBT8LG6YqHJZkKlUp/ygiRSAZ6+EJwsrgZ8kqSO0+f4C8NAvb09xI0xE+q5WbciQ+wovk8OTSOx2wtsD1UlXs4YJL0vj+wEFAHF+JeoUb1EkEPRu'
        b'eAhWZqBGtC1rXAwW/IE4PXUWA08Fwe0006bIAQBrt/G2Qeqlpe6PCyWhoW1MJWYO6mX/WRWY2MZT73UG9+Z4BiQloUYRsCA7p2amYY3hBmWYsE6LWjqNd1kJWF9BNRFJ'
        b'xDRJdBfq+4E2haNaMTpLttYIlylFqJKucS8cIAZ4uhRgjkHxQaBXgAXQcN6nRo2SSheBkhM5Kcmm3MgJJWm/G3+iol2wM8AjuiB0gVmEtgOQClJL4Wba9Odsk4AFgJJw'
        b'H/WYzYsdwyUunwY2YLBQGzeZAgPKxwspox4DNgDScqaox2itZULKvw6OZNQs8I6p2GneCf6ZQl9K8t9mLnIgobl8Q/FC1WvB9OWXsjnMNhbEV4o2F75je2YZfZkY68fE'
        b'YOBrjthRsTN/vZB9cooF/Av/xlc0li70CRJSLsvNZI6xIKbfYE3y+cCJQu2FkZuZUA7E/EtSnb9zmZeevowLXASuYEEifvzu8oWPr5ovWDMmDGNSWBCnyF5XEZj2gUoI'
        b'Ne03BMzC3ax032zbOeGnmfSlWZrCtOAegcIdhe+UpUylL2VzA5gIFqQ9MVJdcWKeTai9ePzrTAsH4gq0mmjJEnfhZdKKO6AGK6y/m67WTzIEOl4WVoDvcMv+mKkef6+I'
        b'EV4+mfdncIUBgcOWq8tmDhgivKzVegBMGQoWLFcb5qvGCC/Tp6wElQwZkL/nbItbHqDf/T/TWPMe/Kb89dtZacnGN+O9T3924MvvV/tMGzzFxjLsR/KIicyF+Ih3pu6q'
        b'Prw5cNjQtCf+Xjl5wLZh70QsnHOV++Q9uSEOvDVnxozIP578z72r107MePvQ7ZeenKBcnTz12zPz7pXduvvk9qr105L/dGz3mix94ML3f/zUfrTZattfLT9z6OuU1VFT'
        b'Ai6uH//OMa8N2r3vPJMw15j1ypwVl1qCa1/8Ovvos4Y6fWLhZ5mZB3zzquKOyp67sOmzgd8s2v7BMwcz0qM/++D2/zy27IlGy8zR/oc2XB5Zc3Z86ijjmeOfsuitsJyv'
        b'RWfeup7x0QfZRVLJ5999ckKhLTyROfSn8gu3ZCtihnn428fUftvxp8Vf3rJbSq6MP/9KztGAqKMDOrLvnND4N1hGTX1/ktFyzTr9w5GyUyvdR4y/0jj5Sv0TcbBiyjOj'
        b'B780fNMNmPtu5Ngvai1fPTtgSsWSjT8OuHXo7Jsj/zr2saGDbh78S2vrf158Pjvlq4S/6J4vCvku5fWbRwatbYl5Xv989N3GwjdaKnwG/XPNE59sXZxdErtnzL0nd7n/'
        b'NTp+ye6dPo+/8LYuevtf09+88JlXwt/q/uArU0qF3Y0uLoO7XXYGuBfuoLYG1GCitoQB8BLaHA5byUJcNNkwq5VJgzVLKQ8Kw5QgPCkyOTJMJQJy8cQlLLqJtsPdjjXF'
        b'dLQFXYP7O9mUwKNq0DZasruhHNOOeYnwFA+mw3NiAxuCtqLNQuYDcINPeBQ87KNMCndsQ+iFKrniceiKYEA5gI7BjQ4TjdNAw2ey6HLCMOo8AS/MjuruMDUUPQWEPU3Q'
        b'XnTtV64JKr1/vd/EI0uUUifrpHy3oAvflQfxjD/r7cnKnIG9no6YfeL+Hoj/+zADMRscyPJ0qxUZiWZifDh/zKtlDPszy0p/5jmeOnAR4wf7s5yT4bw8NYLw98uDH8zH'
        b'BXlURKMVOiQO9bJDRHXGLgz8v4/7wjIvie8SwiI2ufg+2Ziof0++H/ZpH3x/IkkeZHXwfXQMHXwI7xcBaIdY/LshQbusZFsXeH4wOkTXsKgtmBiCBZOJG7xFTCbR8KII'
        b'nfKC7XTdq1yLscG1bEf9Z71R9Rp4kBuMjqykFNGvnHv8MPWsUBv+kNxfIJNPB/DGDwjvj1cbQlNnCS89JkjWDGIxOinUBpQ2G+g//ttK1vwUaVRE8riGVM/18fI5S8Qb'
        b'NWDt6OfcVzObPkj32CP+z3vpy+JGfvnnGcUr7lxZnfjDt9/6/u1P7t5iW8srcRqkXPK7q+9tCd//r20BNz7KWpAx4+NP2b/Gf6YJV+m/KdkW8czvn5107Z2l34aodqsP'
        b'3qr6TjMq/tN3lt5sHrOrftT1dZWFq4ed+MuQZ789mh32zsh7m07/3tOQoRz32q12467fGS0Rtwf/7PeJ11cfRVvarysl1IHLd6bRva+NbNH1Yh6dhQ0zBFepM+MmuYyW'
        b'fGSEioGn18LrtIR+s9CVLjM0TqQiHpcpZK1wP1+M2tyF7btOzo/rOo+YKviEwU1oBwePocoCwfhqX1pO0gjzh3YX0a1D4Rlu1nDUSC2Yc+GBAlgfHakifs03DSlKMfAa'
        b'yGWj87CZ7oIwwssf1s9zSDvwDNzl2v9qANzMw6fQdbJLqUAW/P/XycIjEw0n5lKiEdGFaPB+UoZlRzLyOdRrUwh2ZEkUENlSxpMQih9Mm12lNZJ++P5fN7zZhdek5vtM'
        b'D7wef/8B+4PIpy53yfMsQPVjvcZzeXDdqD5Xqck/s5zp9GLSMos5LbuY13KLRVp+sRj/SfCfNB8sdsO/sm3cNl4rahS2DSMeArxWrJXQ4Bp3nVwr1bptAFqZ1r2RXeyB'
        b'n+X02YM+e+JnT/rsRZ+98LM3fe5Hn71xidQ6isv00fpukC7u56qNcdXmp+1Pa/PB36Tkv9a/kWwhRvbUC9AG0m++fXwL0gbTb36O5wHagbiG/o6nQdrB+Mlfy1Pn+yEd'
        b'nikCSU/VGDX5OtP7kp7WVWIB7J5GQb09uiV6WA69mZj6qL1VW2bUFOmJ1bVModFqiT3QpCsqLtV1MS92LxxnwomIid9hvhRshy6zJM0RpUgz6DRmncJYbCEmV42FJraa'
        b'yabn3SyJZpJEoTMSO6NWkVOmcISQRjmMw5pci75UYyEFlxQbqa1YR2o0Gsq6GxizzILNGVelMXUxk1Jj8ipNGX1bqjPp8/T4LemkRYc7jcvUaXILHmABdoyCo9YoOpgW'
        b'k8ZoztMRg7VWY9GQRhr0RXqLMKC4m907aMwrNhXRDfwUqwr0uQU9Ld5Wox4Xjlui1+qMFn1emWOkMKfvVtC9QQUWS4l5UnS0pkQftaK42Kg3R2l10Y5tw++NdH7Ow5OZ'
        b'o8kt7J0mKjdfryJbD5RgiFlVbNI+2DJEFtMx7PNC3Jkz0K2CpdbRh9uGNii5e9W9DdBGvUWvMejLdXheewGl0WzRGHN7LhGQfw4juLPVgh0cP+jzjXgMp6cluj71Nno/'
        b'wu6VYhXdUBxegQfRmT7DaaRrOgNqSDCNFR2iK/7wmAJtWUb9S1wCSWhCRFQU2kQ2wh0PnxQ/AU+gFsd+2pPL4S6yb/C8SBLP0TiPAT5wrxe8waF1aPt4/Q77fpGZBFyn'
        b'nbxPItlCc8g14uPP1AmOMIwo/1BNkoa9EBQQsyomWrv0mfPNrVuvVinrL1VdrRpdH1l99cnjVSP2T60eunPdztbYQeCJ3f3WfHgBKxBkRdEIN83uZMrw6ZLw7ry7ei0N'
        b'gpgBm707+TJhyqhxOOXL8DKqE9h7/VzY5o47rEy1whPOXen6QzsvxSPYRE1icPvjYeGoKWEsDzh0HV1BVxnjrEhBk9mKRYFqx0iQJdlmeCSVhevCrULOfcvFqB6eQluT'
        b'IyV0W+NkuDFUWE/djjbBK7TYMeM4IClHm0UM2r0K7qOfMzJhg4jEeOBO1qSmiAGWBRl0Fa4f/1Dvt65CfrYeA2p2dg+vHirmy+kuiZgz+zPlAd0hOMqZT5DHBe9oE9nr'
        b'8GHhE8dZIVmnG/ROfFnPOg3X65z//X7ow0HwQc14cLwXPd4BrADO6GjiwexcvzrOCM3oHvtlIgdobGYdG5CKQa9KnaFh94IeuDCGq+G0xbmP1KwNQrOk2Q5txrT3AW3a'
        b'httj2odv7vl1WRxzrrFF/brKCNHVa80PrOxJV2URpDKnXNfHWlyuQY+JeaQZ03TlozUiT2iEe7ZudYneRPnFA9ux29WOYaQdnTkIQ+o58N2rdxJ5uj8gJfKOnVDtoi5E'
        b'/jcuAHTbVqYreSWLOp4lFRmoEb+Fl8AoeBJTgM1om+BMdBO1wS3wJAOK5aACVKDNjt33z6MLs1F9IpXqY3kjqsekop5N0sJK/dEddta8BCc6/c/zg+pf7FcZI+dGjBqo'
        b'r3yuYCiXsiJhuW3pxr8oR0Z/+UXBmx3jjo+9cWPi65rMuO+3Zq5o/yjuyPGcqxKP0Cd+zD0c2T5JPLmoPufsixMLF++adneL79+/B94BQfzbWqVMiEHbOgk2dlVmBKKJ'
        b'2iocdLMhQPC3OIVp3wlicCVnJTCPwYNAiq6zsFaVL7gaPrUwz7lIAC+hpx27jl3wEPxI1sNzKU4LCq9iitBheA6TLiHqDF1FVwK62WcUs2Ab1ttaaNUjcO6LTqoHD6A2'
        b'J+UbGCEUvkEzMBk1RcNjPODH4/foFryB9bg6ofC2QnQwPJJumQ33zHLsmg2PoEuCk0rdgmDX/oZly4QdDhcvprwiHW5VoPoEeDohD9Y56bkPPMmhjejy4G77pT0i7dUZ'
        b'c01lJRZKe6ne0Ul7h8ro1i+C8YSu2fUifY7cXeNTHm1HRMc+tZ0UmGyJuK8PCtyXi/aDmvF/Jl7l9SlezSzQGPN1gt+FUyByEoMewhaWmR5VzjLqVj2qeEW62ztAllc5'
        b'Dl8xoMvwVBf5xwz3CSIQkX/WoW36i2+8BMxk94d3Wz/r/8pQTxJd9/ugf7avjPfcPOybCCYrreZwknioaISbbFfesfXtC84VBy+Yd2BNW/zj348vaz21oe6lQeun/On2'
        b'386Zc//tke29avhqc2DbcwP2f1j/7N/+nP7Ck6VXHq+5mvwj/72P78hvNvl+Z/d/7NJNpZuAnhcxQjR3SixWtIMxwia0h5oxCyvgVgkmU/XzSIgvPBERygBP1Mjp4M4Y'
        b'asbsD5/Ckh5FBdpDuCHKhQoY125QyaYg1EjsGaiOAXw03J3GwAsL0C5qyyiGZ2G1sMdr8jzYGO2QIifB41iQjEEt4okZocLiuD0kD9U7JSPRxGR0Fj1NezBXoXPJVPAK'
        b'ukIQFa6D60pp3dkrp7vkplT0tKQcy02BiYJ5OG0OIR6TUWNXqWnQ3F+Pv165FAaznQDThwglG+NJHcAG3g9mywf3wJwe2YWSdz0QbU27Xfh6DF+O9YGvb/WBrw+pVcl1'
        b'iAuKzRa9tsMNY4TFSKSCDrEgHfQKmeqO07wzkMGF0zx1pnqkUKn3ZzA91H3yb7pWS9QlgoddxAxB1XQx+Qcis9ARAZUT8H3iLCdJyNEYC3sjtIsGOPot5EwTHnHm0GSr'
        b'ESuqkYmz+vAw6uKt5MxJ1HKSrZt3krKv9pp0FqvJaJ6kUGearDo1cTISdnbQRijUczQGs/BOY8AvtWVY6iHCl9Hym2gSp9I/t+AL1kws2adey/1cvfyZ128v/fmd22/e'
        b'Pt98dUdrVWvVxPq2XW0HLu9o2zi6/vjG1k1D966rHVq9TiTdsysoaH2QPKhO91JQUFB8jE9NRmXOXj1IedUjy0+n5KhxM8Mb7etJLJbBdkwvDqDTFB/Dxvh00oLIsZgU'
        b'wC1oPaUFU9AFdCA5JRHWzktFdSlRsCmaup4qYQNqDBHB0+hw2q/HTU+NVputy9HnmqmgS1HTpxtqes4kiw/D75cP6oEg3XMK+o1YYJYkGNp0glxOduezXY9V4LskW+lK'
        b'S/H2NL5c6gNv+9jQ9CHN+j/FzLl9YWY6tZRh5DQK0Egc6rqgaBcb2f9/SEqyJWbMUwjWLYtgDKO6R57eqDEotDqDrrcX4KOj56iydwBFT88v/iWg53+BnEEg5S+3XvNY'
        b'0KbH6EkDorahFrSfIuj8Id34OToE9woyc+UAdB6zxZvohBNLMY5GoisWug51ESPyVVzM2fAkzDYbo5NhY3dkfQw2SXzkbr8eT/sJBtiHoGq6A1V7SHZRvTILJZ/pgZKm'
        b'sy4MbMOXZ/vAwKt9YOBDa3vIGTSMHXQ5g+bR9gLHaua9nD5wjwIiRRKjtSgH4xuGvS5G605TcK7VZMKMwlDWRWP/rWB5ufUlnu4H5v3PdnLMzbnmVgqQox8GkH/R1o14'
        b'uRtIvvOJ+xm/zzFAEg3OdxhaR8ERq3Ld4DHaXwiDq1HD6w5+kTZEgEW0F50SgLENVgUR/Q5rp915Bv5SGybGsHhVoohDlT2OH+oT+nKLrUZLlxk19wF90sUPgL5emZ2+'
        b'kisfyBwEKweFxAv48kZvSPQ88QiQ2Kvm/yNIND4QEjv9qB8ZChWhYUSs0xsVpeOjxob1QawfDSr/sbtdgMrZVWUYKn3aHx0uu0Plp+Cdj91P+453SDHwFGzOF8QYtDWx'
        b'K1jy8IxgHDhUANd3yjHsJCLHVC2xkP3J/eFTvsIBemifW3e4xDAZB+1ieKEEtj4CUHqTkX0YTOY4YHJID8jomVco9+KDwbAdX/7UBxge7Gs7sodUpgzoGZ0tyc7WFudm'
        b'Z3fw2VaTocODXLOdazYd7q4gGr3WtIdkaiGXg+RyCDgswx3SElNxic5kKeuQOs2r1DOjQ+IwYXbIupgRiSmD6kdU2KL0nqIa7ahgKvkNm410sUluwZci1rFRohTwLO/O'
        b'M53/pawfw3qIGZYMGtf3rw8vdfdj5HJvRu7pzXh6+kjpHoAZ6Bzc2unBgS6lYvUYa7gsCMWabS3aLlqLNs/ptcZDUD/eCSLdl5iFrVE7fB2BKY7po/sy31PMXk32jCSG'
        b'1FwSdWIyEomuiwSnwmpo9+k0XXYNRQ9D7S18+ZB1BdHjQWFo8LkSbUC3Onc5QuccnYMtOSqnR0aSTAI3oUOolbpOe69EW7q6Tgfrf9l5uqfrNFjUixa6O6kImTFH6AHo'
        b'fqpo56a2vzUknVTU2xwsVyk56k/TMMUdhPIdOJXCsND3jcepP+rWGS5/VIPEzb3iEDAQL+MvRFNEnwZezb8/e4DyamFa9okhxwqvLVwfulv1XNzYRR6lxYsmDVmyKsl6'
        b'bdKRrFmzf1j0zYD7wa9MCC4vC9fMl0oK/V4b9DWLpsrH+sVdGV099vmK0tS4EWtDfSeHZq1+rJ3P9jlccnZITvaf9BclIVmH1Lq4pMJX3L5MnBruEVCw0CSqDPl4Vqns'
        b'M3NpSWjAu7NPuAd5XFt7H+sYBcsjGGqpngDP41lwWaqBdCzcSyzV/vAs7ervF7GAD11L/HrlMR7zBX+iFSYfMHzpInLU8ZQmy0qHe3E/fxAx5VsxUKgHrs2zAWFXt62D'
        b'YSuqT42MIufFOjd1Q5uSJWgzPF6Game7wSfhdtEIADeMdEOtyC6lhbkVioBU0cGAeHXKv0PShRpuxUmA3DaXuDGlZGndhJ1av/Y/QqbOP4oBTN7L+sYvv2HNJEYhtjJq'
        b'RGObJ1LIZ722c0Oa1etY8v3jt95rTb98bFiEbuV99uexcxbZyle9vS+tOuql8sJ/XAlfVTPgm/xvRTDogyEFmYkL/j6nWpv43Xcffj9i0YCfXrm6hXdze+t4+Jnfv3Vw'
        b'yYTdP7cMemnyqSc/vqzPbK9u1qx6ucCwKGz5zkX5S2pRUO7/uH9Vwe7YMLJg51+VvLBweBBWw/1dDtvp158Yo2H1RLrAOQ2eQIe7+jcFeXQ9qnsSukxlLSs6jG6FR5Lz'
        b'Tw2JZBxFwB1dY9HlVQMoT5sRPhpeQQfCUV0YMaWRSLuJcF1cbw/437qLbtddBExmTTebN+lHJ1PjLTJq7Sb2bm9WQUkpuTfddhZDDgEnbghdhKvf2qzjjAm5yBep4B+9'
        b'maCij+2YaDw72sbCbeFhKtgQK+li9hgA9/HwpKdbLwrUfaehXhTItdPQo1KfR1yMkjmpT+Vc2cJpDFltVxgCgycFU+oTlCgRqE/eLP7dwPcXDxSoz7fuv0R9GiP2zTs9'
        b'+fCkZYPeCDuY81PEvdS1Hh8P8Ki4kXUudMPMcUmfqMqmvz9YHCwb+OeFMxZ/OO36yL3pj2XWDtoWdmPIkhnRiemr/+jVVvzl2A5uc1h6yZiBh8d9POvf2v1ZG93HRlxl'
        b'4/uZQyaLvp04OW5b8hchb81uEMcrBeqzerrNjXYlUkUD6eNf5dUGxrhaQPPtM3zBcAACUxn1QFVoBTAR8Zd+WTSaBjyEfjZHbagNKBJe/k1CQyMW+irVES1MMBDOEN6Y'
        b'mtyVqmGSttQ/KXC5Pj/kU95sxCn+aJ0R+XKbB4qR888cXX7+g/H73ss6X71A8Z40LmRf4XUf1tZeM8FDdGXo7VtH/+Q2/Yt/H37pHcmUcXEBN64+NvVs2rWfhm7csXFn'
        b'xsx87RtFWd+cm/dj6eTI3R8HLljor5v6ZfRXkrN/vGu+c+MnJuzQoKSsx5UMxU/O7JXsPGpcuozF/PSGDp4zdZMjf/NGQhQhtbpOhBzeDSExSkqk5JQBiooEKeWChy5j'
        b'uuMqCP6GFjzrwrw7DhShB3N0Yh5YN/DHB+CeFG1HJyjurUBH5yWmOnFPzWO2sSeoV5gi+aN7pCZgrKwRCdvA25gWQHCula1g6T2n5fE9Z2HI91lg2fqlbAVfQbaKF9UA'
        b'C0sPvBlXLrGJWjitqJWpEC0AxkKyQXvZWOEwIPqFHBMkWgSMy1dhfDVtoblJziwbZ5qBU4hahQOBxPSIBQ9ch7hCUsPYJGQjea2kEae3iaeQY36m0rwinNeM86rJgQa4'
        b'3SLcPhFtH8kr7ZVXivNqjUNoXjE9yufR81XWiIW0+BnYyKEJfsKm+fR4nVYb0LoFYaJiExwpZCpMiXW6kjkmQtIy74mslrzIOBPxE8Kg+RyZWvLBRDZ3NRG2rpSYiAt5'
        b'h5vOaC3SmciBCnPJs5hsi67VdcizjHpyQ4VTIe9MAbI6N+bsLJZuWE+DsciWvCYSp97BrPiVYfAdcnKSiXmMEB1MzoCiuzNJOSFk39Nxqgf+vc/TUz5IlJkfOcuD7Xov'
        b'3AmnMBCHGbqd2pxQdICecx45PoxsVwD3wC00IEAxmMfy69E5vfwkXNuUE2Jkw1Rcy2QAchQTnQOWnnNAQl/paJomO3tCNi82P0CT9KD9y7YUZxuKjfmxnEM+J673ngxV'
        b'OeDNwXDzQvS00FSsrqJaYXNJIm+BkbBaVJaAjvU6TsflVjaWtlXLFDImMVE3tJyNHILEaPkWQI7XwS0X+YNWxsYEAMLdyBvqhCJ29IMQ6nvsiNXC7gq80CFReZ7eYFCy'
        b'HYyxgyl4UOdIn0jfaCcncc4dCDnhFBUpQ3eVQfvRzSEDxhDNnByuvIl2cB7trRiMHCwqw6rE9ocEKzN9Biv/xrP9mK7Fd4kb7YzEOzeoBLyw4A4DStRzPhijFV5ulN0B'
        b'3uP7c1i61Wf0ixVefpwkAfyKIUS6lZ+dkA30ezNPsfTMjX/siSNb9J1rbt16qep41aVdv68e+nj7jtaNrVWtDW0JF6usTK7HTNmHM46o3p7RFLxRlOIeVJc19OCgiEGv'
        b'1PwwTv5qgzLFJ97nIBv6nHTMiOpF8tD2yonVuqG5MVx+MIhKD0qYcxGLqWSrT9tCbxLYTKKaUStPApvnllGbcgXcXzZ2enhS97PtpsEd1Chdgiekmm4+RLY8qU1BmyIY'
        b'nOQki86o0BVqBlQP08OTSUR5RLVYMkXbUtawIQp489cHR/crKtZOnCCcGJGt1efr+3K5AGuliXLq7iYcUOHPmN50FVP7KBXWOSukGWf2xdb8+zA0W4mWPXfOdNzTxnmw'
        b'bSysQS10z2VygA85DtYxOnHwqHjNqswHUw4iEAv0gnC3VoZSDFbVIdKYc/V6LPG+CJzMd3j3AZIU6FYb9HllqZzD682TE/ZSOzZgBl3npzrY9kUp8CSP9YdqFl0rRrse'
        b'3BKSlxyQQrmfjBwqRNpT4WgdPTaGVZneAlQOn+Ns1S/tQOZmNTramE7aSA944Yh/DCW3qGZcUDhqdDWVttM3E56GOzm0D24q/9WDRhtnevtBA+aWM36scB7WIlyS6R38'
        b'jkavapLQxeQxsYkurc1rqAme4SaPrvgvBmuDqz3vPtJQ4bYJXHU5adufSNtodNpJ9DQ8TlrnFCg90Zm5S7nRi3ocrcyDLke7kX37tAwm6URUAqb+FkLwuSoWCxKgghNO'
        b'e7KxAfTsKLPYxpYE2xhy9hKdZJGqY3jM6DGxY8eNnxA3cfqMmbNmz5mbkJiUnJKqmpc2Pz0jM+vxBQsXLabU71M6xlRYYLBcoC/FWKvkO8TCikeHKLdAYzJ3iMn+G7Hj'
        b'BRHArWfPY8cLs6LjHMey0Dgz4XSun+UcNWCgGxpz8pjxnZq1V0CClZuErsL9D54kuQNMtMKJQxR+/+asHVOk9/sEktjxwkQUc45DBGQc3QCH0cNNpAmdE3EIXUfHuBjc'
        b'iN0P3jySHnPNuI65xg16pA0j+zzmuvexKLzKSgJ2+qFdcJ0zABttz0p1m48uwXPp+HIpvQTt9YBNLAhFV/giabS+ZbtIZCbC2ezKxA+1d9ULMc/RMLmYszynfmeS+HcW'
        b'EFrJT4u5pGQF77s9Af3J4chNsGYyqo+WALdYFovtreikECVVvxpWhUc5oyvhOXTREWEJjzrPauglB+jNxdkWfZHObNEUlbgOenduwuRYQSwzfezKthE8yPZOE1n6otvy'
        b'mgccWb3KgjblrMFMjOyTH02bHRmViBoiARhpEq1dia7N6eUZ190gyTk847qYI/Ecu/9K/9ReBkkiIHj1muN+Krq9UjI8yydjvtuEGnggDg6Fm1hZGjxNpYrFZn+A4cA7'
        b'Zk7hwAD5NEAzDJKis7FjYNuYGHimGIQAiYqBe4aNpZpz1HBUib+1j4GXFs3h8Tf4JAPbhxcK8fN7l5ANCsdmiejuBAZH/PyrGUEA6wYxJSs0S7ml4YI8I1umBGn4ZbOP'
        b'dka/OSuEAHx0ZdAceMEAzwo7/aXBUzRt+Vxh872Y0Sa5cf4ooQB5AtX2Fc3LTPLGqNUYWoSdqFL0yYnwFGyE9ggx4Acy8PwaKGzcutBrOqgEIO4ZwxrTFk8PoZgfbdNI'
        b'yH6gd/naMWhwsUMC44TN+kpEJoNpdj7Qj1O5ceY38JdlIxNnq15N4qbLf96y691Pmy4FeLX/8/3fX/6XYv3z792e4XVSseOVw081h92TXy/OenJFUvII29B//XTnpWS/'
        b'P9/e0n/mhxqNbsPrs37I0VxpD/H++aP+/9a9MXGuz3DVF4b2XXfWrtEm+o4zZmrOGIbf+Pj954794eOXrmzJkecvGPX9R7sHLfPt15647Nv6J+6HfjDu6bW+nk/96/+1'
        b'9yXgUVTZwrX1mk5nIWRhScISoAkJq7KDCARCSCKLOCzaJqkOJOl0QnWHJXQURO1u2VRAQAUBRUDFDRdUhJkqR53RcRwXlHbGdUaGcR19Ok4c5T/n3KpOhySOzpv//fP9'
        b'3yMf1XWrbt313HPPOfcst3y/92rH9rpDv5u5sNlVsLPhiW/25e2ZVzristCSPY0n9nz46Ktl67flLTi08M4Pm3qdGLXm6/fTn3vbmfT2ca1n65bJZX+/6PNxX7jMpLbz'
        b's5xGhqJmamuZ/MGj3t1MOoJ9tBvVg4y4U/erD7QReH5tB3OvvHFp73hHcerGOUKBetclJJWsW6M+rSsPX6Hdjs5ISXlY3aGFmaX1/tIqZnJhzmuKt7iwqOvIAd/cy8aU'
        b'kI22UMtrh5ZNFtTrfoIn9n+DLDOxETYjjxuQz5gLhw0ntIOaN+2EJ1fpBs24/Yi9YAsy85LQF9hKOwXvy+R7MV/NZA8pfKOcMarQvZJE7dUNSpXHTeEH20Se/4qzfEHB'
        b'KHhx/kuwrlWdYbrcazvBdBSGO6I9UaSd0O7LnzlkMOmFI857fNjIYRLXn5fU7TO0R5iK+3H1sPYgEA/a/gDXByGld5VhB4n/2qkroVAgzGPQyQjwVBgpMIwcpCkoKelB'
        b'E/yXYNc1ZXJpkCsD8gSFvTypEevn2WFRFo3v1ossmDDkEpXhYWkvBnYV9wlQMqM5pbIOrGwsAiZSYRQZ1s4Y1SAUmEFBCbuMC0s0SBc7CZ5+7TZ2/V5cc26ltwGYD6ZB'
        b'1FkwW0b4iFFTU2OjR1Fwa4hKxAebo1LAsyoA5AQW4a9p9kRtfg8qNgUwUuvKGjmwTPkL5hdlT8dItdDAj/H+oxjsOuLbsl3UI2Kh3MNKlvrZvHROEtEFIfHQVw9zlGBM'
        b'7XLGjZDvyLvVdaWwrnO0PZL2iLZOu6sDARkbWJxhJCCJxOWAxHWQxA1DPMOM78Whhr1JFnGoSR4nKMNhlgVZghxiUMTQ2BgKtEXE2aQSCuAphabG95AbNkPZRDNsLmsd'
        b'NGHJ5FX13sL8yUQK1viWTlzcd+DlgxZfAdd8F94XDp68ZPIkIqnPYmOZmOo5jng8ZEeiZr+nQqlaFjUtVRqaGqMmlBHBj7dhJczNr2iJRkWoJWppRIUwxRc1wVjCB1aj'
        b'0h+i0JPRgSR87TYy3ynqgh9JRIyRRq4QDGGrZPCIU3prR5knxk2D1AfQ0Y0aKWdULLnMtHBjXGbAofcWtyM52h1N7qfZABJdSOOQaGdMhjIRLXOUVLzu5fdx/oygIANR'
        b'H+TcaLMjKDl4pTd9g0Dou+H/NO5yWwsxLlCamAHzwnPL+1PuC2O5x7PcFPQbpYe8MptyzIjlKGufQ2b2QVJZlLe3Crm5NDUwlgS9X9GiCFTUeGGhSB6vpx6mxLPC4/2B'
        b'lRh1NCqeANqa4ogfFXW+3yEyn1HJFEE1me6lc2nIUp4jwq7QUZs/aFaBi5hJdaP6wAD1fhxynuuj7jcNWqKe7NrYGyNYt53EA5riFokeiSIkwmAvMm0Ta821lkVWeGaS'
        b'zfTM4rHU2mSLkQKK0AIoDk29rYvscl+MtgjpBNlxrW1RQiydKDsh7dCjMUoUpTFJToZvEts9S5FT4Zkz9kSSu8lp8CSpXa7ucjo8SyYTb25RitwvJAKvgUbctkWpcn9K'
        b'Zcs5kOom58E3ZmhBrtwH0mkUfKM78aoDognTYWY8vsDFwKm1g0RDdjjPQLhtcngK+MvJknFvsI98C0HA2XPwr5UfB/R/MUdGhKRkNTc21XGLy02LlQKO+xsrqjzPx9Cw'
        b'0NwrrmmF52fslPujtiIniYw5QK0hIuDLAN4sPGLdQMXSzszXorZGb0WNzw2vXzSa4BCau8c3IZajQ92CUXcqx+zmGizG6tRNGQ8LUZMbdwZaF50a0OGqedWQ6SSLzcnx'
        b'deOnHaYnVq2DpgcRgByrkFcSoGmKme+8pjeNmuxCB54nJjL2xqadNgCeiYnpcKI/Hsaw6LtBURbqBKWHjBIGYQJG1YXVs4LzD5VNQRF/YQvg8cAFnljYV+mckVfmMQ71'
        b'PhYR11rWyg+N8oNbhcKhMGUkaDbRBSePX9NqWjO4Jc+PWy+LY24HTlIJ+FfWwLaK27BhW0U+6BHRRPnGroTSbkA2sDN7yL3970V9+gwbLrvQg08WhLV2vjmrHSDGf1XW'
        b'zrmnGD922QYY0tgF2OGAQDG3YdnQkuExwnUG9szkbwJCAmkIn2woJWIXovYYwHdxcKBkwfd/xsmkmJJAqrYHHCzx39NIJRNbasECK7xepQffJT3VG159jOKsXui/q9v5'
        b'zYGvO8U01CI0eA8DIIUlpD7CBNa1AICbBGofb7QPg4kHDYHbYT5q8vnrKxqhqTmxpppZ9AI9oGfU4mHt+FHKzkoulPC5qJvCYlh3JLaaU+P7worvenCHsa4Isa4Isa4I'
        b'8V3BoYbOCIY0EyOIt+9IDTpTCrh0wEAnhUof/keqbSt9IefX8T1J7dATVn6HSYmJnZBbCkNLwyL0pLuBEZRkJE1YMPAW6A2Sh7iOA4IORmLQQMAirOuLGHkgKd2xY0hp'
        b'st4luN1AYtUEPPVut7FXlHL/3Nmk0h++/odxlmTXibBkvjmj3XJtK7zrmboyHugyf6h/bK4Qy8Zmtr8+s7AV0syK+sxK8bmJTFL68Qb9ms2mj4bCjQ/aZhvGw2802Zjy'
        b'mEPLHzflA3gMdqfvhWxk0K05cw7QfnRiVf2TKKzGUpvPqulsC7W63ZUNDV63OxHJdBQdNKe1r4y9JuJ9frvZMJgQimePJB/Fdueqkfjlkby9HXYZPW46QlMRDEwrFyMY'
        b'VwNSrvEFoklIp8ueKm8F0zBF4/lAAzszNnYG/Exx4WjTOfV5YmCz4sFIRimSDlbk/egc8Njn2q8Ylq2o004QSOXGOiET2MjCJok4JJ7pL7CQ22VRqWr4KB8a9rGwSFGb'
        b'Z1WVt8lfs8ITTcRdzQ0MJ9bq/xIbmQsd9Pkn9u1Lh7GA2QYTToYdyQtbhNHFQuzdULz8rWMXFWAFue5SDB9g34DSabdpYJvaYQMcihhb8hJcaugMAUUBQAsMZR2jTUQC'
        b'6Admfh8ehPNZ3BKhxdRiDpqCwgoO2HxcKaYsDJ4k+F3sfimPvxP0N4AzzIjal5uDZvYc7rhaCdUxoKYkKM/SYoWazUEL1GYJWnFog5YMDnKOh5yWFlvQpiwO8v75wJwu'
        b'DNrgvTiB8wlBG1Is/oqg4K+QqfW18G0Nb6xNOuLGBdpq6ofUlssWdcDKAMayxivDdEctgQa3XFMVIF0H2h9ghwkAbFVGbZgRl5GfqEzGANl4kv/Q3mOvavD5mVlglJfx'
        b'eAQKjfJVihWLEapk5rqOSOSPuC431lGQuwdOHepuSITv0ugU1EnrO5XWuJl0gOwUrABZ0/YbsN6Jw0QS00J0CUVFLr7IlX6+BjF15SmjK4oQ61kCz7huZKYZaYBECG37'
        b'NC605RB6JkykDMRLPq/DHvUiLvLXjxYFxgUCw7b8UtQHwspZRUECZlASsNtw5xSTHclSmpRmTjWnWax2p+SUMk10SlqpPaI+6ccorZvmWUq1TfnLZw0pM3FZF0lF2qHu'
        b'811MjHKhVBlnPoVxcNTd2hPaJvzAZeZGyOb5JWkupmM7frxYQuWVzlKvgfc8l3CVoN2r7lAf7HA6hCiCFJxSY+ihBsgYHbPpPk8S6ivqPDqxouR2gqQs+oSOlXROJVmg'
        b'kyp1g/pgNetbqXaH+gQ1xq7uEbQNBZ5OD5Xwnx/J5BgHnExBGlEjHfhd4Cwl4F155tJskYlZKlaLOq9rRsdmkMciO+RE+LXKTjnpWnSMxlZVStQxram+frXe3M6JZdpi'
        b'0PKFMTCw+fJxXCbfxmUyyQNcRZJCSHpgcFOZIsa2VYnXeQXYJ3FpEQPKwPcjGjk3ku6+GClFy8/Mnp3PJaFBwxQDT5r5bFhYsJi6x/fop7m0IVqaV6bwXeyfNqBUWFNm'
        b'GBNr5pvT21UYy9I1saaffhIRogOVEYSE+lzWCUQxGgyxmds9SzI4Q74587zexjJ1Xf0kmkqZB47QjApoRDcCvldSwzQQyJZjw2CiBRQLKllETcU3WIzDxjBTNJE0akQu'
        b'5fE/eKROeKfUIH4YCnSSbK7z/vwk6oe1q0sKyOJ2ez0+t3uBMYRAaKedVyVl6FqCgJ0JcEsNZQJCCBJuL12RXPjO7V5oQIy1ExClHD+ih8ugh0Vd9o7Q+BIk7VA7s0Mt'
        b'Om03ge16520luJaUqTh702NbA1ouK7Ni+wPtBT8wrRdBpkmSfmJs5eyi1ewQk0WrzSo6RBarbfvV2nG/C9G2eiSgo8FjzYQFs9UnJG2HtrVv12gQVa4NNLhNrBVrpUUm'
        b'D9MhQzGf5JFqLUC76Sk62kcUaV1kZYI5QIsMTdpIwGanFW+NppZX1nqqAuTdTx+tf0F+pNi7wBqE16pxVtBrZXNGx9p+uuxISfwhyVEdVuaElz8aBV1roCBlGt+RHkWI'
        b'aMAyi7AD2Z104IfwTszsUIFLsy3A6dwXUaOXQY8k4EdX92CKv4SBxCAdUawXzNxC9t60erSuGMzvNRPnNwzyWNq4v308y2v0iaV05f42rg5ImUwDvKP2YuAQVjEVWcJg'
        b'CP5R5xSiGJsCuvJsGy/8Y9AaKl0SjAjAxDuA9kMKMB21Xr/reuB0TjLh/DVZ0o6eY4TexPZLtI1I69CwNloMy7mybWG2UWEOMVOksxD18QSXdrRcu2FWaSEqyG2Y3aze'
        b'XrpcX6G4PC9WD1r6mdS9Xa/OHnGrk0gSOlEEMkUkoJWiPY3+GzhpKrofnd3QUNfU2O5I06RDTrfYgtN3q7BxpIF4kAQshnM+ouGlwOpGj3IH3tpiUrlOd1Ozl2pdKxlG'
        b'dngsdK657w+0sJB90okd35zYMjxv3ZTBixZJVxixcsliEyoaa0e0E9q1bLSDapgGXL03EBvr5drm4iGF2mOoY6ttKSxAtLncrt2qHhnT4SAqJh/BcCywj3Mk73DSCuMZ'
        b'/xfEgz08KkoPIwfIhc3I2oY5ujftM1Y/8Bp0VCf+rHQ2wBKypdGEhjaAJa78p0ZGmwsDEJF0dAP7AW3yqA9OWjDBWb3VDY1LtAe1R2Fpaw9x2sPqHdpjHSDMbEDYFXEQ'
        b'JrcdyZirTXQYZFskkvqPGfA8HgRZYQ+Q6OhHlC2yFclj2Sbbgfw1xx0AWRdZaDewEkHsjDr0qS8FEl8pK+rgGiQ25GhTKwNzEIat+XYR2GpDPJUKNDBfg0p+wDqTEB6p'
        b'ZkGZFhNI5QQF/Q0QWFkcUM4SssBB0T8a7ygtZUHpyHRDX5iASwgK0/BA3QTfmYw8xICPNYSVtYJsBnZFQnZFF2stdVlQPnwJyVPwMgkvRCW1PRvWhkaidjcJat0oQiZk'
        b'iaSBS/fZQrl7khCsUfFU16xyowIhWRVEBZ//xwm/sMCdkm4gIwgCSji+s5us5LsaqUAzyXKTSZ8jle/Bx055aFLaaPr45WDh4vQg0G55KczLfhxlAYUgPKRRwRJGcCoT'
        b'geDZtz+LxCISCTQcASEo4fk4MVicLG3C8c43BCR7JbRVUcbRFwBfbFZg0ZnXw2xTCf3guQUQVRHmYW/057T00B5lvcCeLHfgOTtAnBUwStQ0Dw9JouJ0nxyVyjBsuGlB'
        b'hbep4xlajChgZ2gowJGFFYzP0olyWMloGaosjqFHvjP1TnIH+YRBlDq45oL2Y1zV4FvhUQIki/DHq1gwb51QKIk82wSmI4ipQ1EXhqPz6PIXP8XUYxIZ3EoBhRCuFv2e'
        b'5VFTgyJ7FBTp+Zu8AaKi69vkLD905u9s374jBjRZeeZl1c7bEa4E8ob+vV3shYYlQqpd+FTq1tzzB3ra4agtJi8sIpjCVQtQ0bNFBFKDdGXImikdoYwE0OI+NudSUJT5'
        b'FTyu9b0CPqVngs6mIB2PMkUg/Dww51Z3tRc1H3w0aoaU8Aoc2yvxUvFPSA8Z3r9o7PDMy2wqjYKwVuqwevSqOt1MCLbQfDfOpguuQeyJI0iqsHuR6BL3ocoyvGOC9RW4'
        b'LvBOhLv+AcBMQSEdtqBreNJMAAy2jyfCDlYMrI8RKN7zWY0nmAePGmUTu4MnMKrpnGHbQkeLArAuCGet6Zf66nwNK325sS0+t2+ev2+reU2eH08ezcpwHLI0Aj+Gy5RL'
        b'8QkaxBMlZ8gWCNIu60hERxPdPtTmQXfTUMDrku6JjlkkJfNMXp+OaEpI5Zt7tB/e+E87YKiYeKmaiz/XI8jBjRq3bIHd1QDtwPR1dEszxEL4BVnMBc1BiXB/94DEDnNq'
        b'YV9AUe1+fi5n7AHG5m5WangdTJRKInWxr3SYAQwq+nAH+tMSJ3GxGkJV5QJM2pgYFXoUtzw7l4DWQv4PDFDEkbKLksDGLLsjIterFstgOdg65UkrYw2nLtS2p3p/FEHS'
        b'RgnPh6+3GQSJlUuXkrsn51ht6U6ye1A35Czyx+gw7aFSbWPWOHTIlJ0hqU/lqDd16hEc/1GgyBhpkkSsp0GSMHf9BkGCb84nRpBY1kkR0kFBOR2buuSodXZDVV1RjddT'
        b'piAl3I4caacJMItj8krGV/ntAUHmaQEyzlGgd3Tel44iOgAtuJpIUGcmoZ0Fzc3c1thZWGs3jMObKzd4dEf76Kes1ZLnL0R9N5yudRwdffoxH62uqKWi0o+n7lEr6cTJ'
        b'NUrUgtrkDU2BqMldT8FlKLxv1OLGHB45Xh0gKmEOxd8JC4qg8JUBVbgOMfiimf7sfHOKMUidi/sQudmNcUKPI0xFEuVcaEhn45qtYVx2gI4QTV/G+YaTMeoUHtAUzzXn'
        b'BWFxyUKdqGRfg1+ZlUGXAX+JSOwqUrXSy+PrJGVEAMYRxx2eWWWJlWfk9dnZ70p+JR460cjP45ZbSUg6/2wKobeqhiavTCNeUUW+/nNxpM7cugv/HZ7ssgGfA0NKwxQ1'
        b'1dfBICsK3lvK5xHLGjV5FAWw0Ap86Jjb5MPs+hu/1+Np1PFf1AJbDxVV2+VyjkpY+TlJdy+AVpwCWXPSsRRZgpB94Frh72abxAtfNifG5gK/7NoEhBk71gJVQCOBsMsb'
        b'c6BkwHxIxny0U2ZbSjuniTrHgMZU448NgUmpx3uSwpzP8jX5sEHJJn31szgpQGd+JwnNSbFGs1z/jO5iFKUcJzO+riuZMTrt8QCOSzcZpBbfnBwHr/Sy62EaHFcfAqwu'
        b'pBWYkJZk7TBMuiUxtUVSrsG2BIwBUppiTTvfosbtBlSMoscsk2HwSbS3mfQP4hqpZ+ug74v/0WaYaC+azQRDLIbDwxQe8awxdsZOyipNNFdV3gYgE3HgDAUQye1ZVdWJ'
        b'BBVQD6zpXFNM1I8sgqP9umd5UC6AeLKLzYRGhqbqeryE8HLDj5Ft1kOmv8ZE1pxTctodKSjfdFiYD4vH1Qe1u9HdULm2eYUewlvbPDexVrRrN/o6bBwW/ZfsS2NSE9TF'
        b'loBbjUlOUMVxkSQnh1j0GjFkDlmrzSTFtMEGksL4W4o/gwc8NthMmHcyPOaJ52yXuVKjUtEl04o6IMYYRYLKWQFOpyVg2wAaQmB8pDGF8AttCwu1ElohUxrQYsDMUvom'
        b'wuBQLGtNuGQ1Vjgid0WevzUREno8b0gaYjjmkQp9cTZWLPVEHX5PwN2oNMhNVcAVOPBr94Lpc+cVl5dFE/AdOXUFNJbgdushr91upr3txmApBl0Xs3H/oRnFuvMNsE8n'
        b'rVXEas2JWG3nLGZXUln97KE1ZR60JLe+wkf+LNG1CmKGrW0AzpyknE9sYs9ifRgBTSLZbXMqNaTdy7J2zTFxccLVPXGzh8sPHYIHBSYEqhWUoWHgbPEOtbyBMxWBmwVS'
        b'YD3TCaf7FhHofDGDQ+1jegrEwV4z04UgypRXZoeBxpRN64UtTqBNpb2WoMA2OBnASOLWi0xJajjnn7GSZwLbhZyuOLUMKXnUEf+StBry8uZNv2RK7pc4BExFcJXiqbYT'
        b'iR8VVlbqIBI1A+nQ2BSgUYya5Kb6Rj8zcUVwpcPDqGklnuzrQkCG8mic6ROhetmPN21WdsEnF5p0tTsnkRkOAgsH6WSh6Mp+DsjZ72HPSKD5Yc2L2mZ6vCs8gZqqCgXD'
        b'LjMLTJygKkN6hf/Q6iTmvQYZuyARDkD/8zRnSN+TijPMh6ivNxp/ugeeCmh+Ed+E+YAJ+EtTGofKnuiBgqV7srRVNrfYZEuLnckgWhIAFhJIKTTQ4gDOwZHFtSQGbUql'
        b'kS+YCDNthY13tmxrSfQlUdoO6cVyQos9VrcV614+pn1bgo4gEK+ZXB2n+LBs2ZHBZXGNDVCSM+hUdsmJQSdwhbuCTr2ODUGHsg7F9zpOgbJkZ9CCZclii83npJxY+y58'
        b'iyrYrCZ8i0ohsiVoCiYG7UAy2GrxmlDrkFM2maE0u3If5oI2mmlRppadRWuMszjy88/ibJ8JpZ9+6W/zvppcRNKSVnHixIk0XVHRDdiEn8+4TD43yl8ctUxtaFJqABnx'
        b'xS4havJ5VrpXsZ/VrkSmQG8nNVdvjc/jZ0iqvkJZWuPzR7thoqIp0EDIzV0JuKsuasWH1Q0+IIeVhiafzI4XNiOkSlUerzcq/eySBn9Umj29aH5UWkj3ZdN/Nt+VxKCb'
        b'zsglKkAi2xWTP7AayOkEbIB7madm6TIomrXGjhncXmiOR78HXhiqMCkeaEXUXMmkLzZfU72bvmDquBLew1PPqgA9/qchpROYmiUpT0/DxYMsIotj6SASK5n58tM9eki6'
        b'iI+ZcqFXkF7kCYeJLcx0GMyWmvkcur4jEUYyLba4ijqV09A+toprv67ouMhJh9nIGOXJQoRDc6SASIwX7rFWlOms1/1rZKElBy+bg3w6UyqUZAtiuYBJl7Ga2/HZoi5r'
        b'ZbusrbXHxRUKGinnjmyoHpuLCmK55CnB31SvJMM8t+b/GBPugsLc/kPz8zoQXDEVLzRvIQMrSwv0hckRdNOqaw2p3xSuzbhqXCdMFVpVKQZZms4159AgY+NHju3MqOos'
        b'ltQqDc7zD6a1Uwbs91ksozuJDGBqSM07KkJfo06C9Bpg76savA2Kjs1Z4QbTR2dbbbt1vBcmXnk/1s5fw6dek0F8CWlk94fSrb68joVZsexoW1J2Y19jaFjZw3dJD27n'
        b'daSvqLxeUZxw4Sf6YWoTM2yAcgaaYmKGZMlqyZTSnOmDKJxNonb3KH9C43KRE7RbgWg8yPcZJ6OCW4wwKCMyuaysDLW+xCbkCy+blYI2gA9rd6IRoHqrGV+SKe3vbejD'
        b'a9k4B3el99ZRAldzT2K66N8AtN2Y+y8unf/3y7otTdv9K3lX/4/HS9YbjuXfu/aGlG6npcQwvyb66lfjTr226K25dW8VX1380uqhkz+f/O7V0W9bggc/ea9x1+rPTnzn'
        b'XJh04u2NqTP/7Bj+8ojhh2c8s+1UuOZI8sgnZzqabtv5+uDhB48+c/ztviuWRd48/MIzhX/ot+IjsXLLSylrmkJvHlwZ/u7JKb1ernp/79u5zrMt7z/oS5kR2D3mnnvn'
        b'vP/VsjVzq/+Y9c5zlyy77pOUE6Vf1PfqduTB936ZPWCOd3Xpyfe+XG3P+Njf9+vne97010E/nz77cfXudwozF//xg9Tqj789lv78ru1Nh4uKlzzbva537kepn1g2Hr+h'
        b'7tlT1sqcq288XfD0w4NemFs5e+HghwdeevhXc16L9Dx2+tcjntzx4uQDG+4L/XH+XekHlic8fuSB/K8r75i09YP7N+VUXL987GZl5y9vPzxtwVUvbH1k9tH10xdu7+N6'
        b'nj/zm8rshCPJCeP+4IjWvGArqJs4qyKl5L8KzppaL/7DA2uWTvp02Teu99bc3OfgkC2exXuev2rbL0YsOPbLSas+2Tfm5eMLPinfdLL7kRPFjUfvPch/X7nklpvekK9o'
        b'ldd223G65LrVK0773wv6Vry95aljS+/+4Jablz/o+cvl8pI9bz05sG5E0Yd9zjy15YIVx07NblTve+89flZB0oGt00buLVgfqn/7lSvumtcsv/TJqp2Xf/bFpNX3fXDT'
        b'Wy/v/KDpwaItVZ88X7hyftGfbn915unLb9tQ8OTi18d8W+U91usPpyYPKnrgtjeVU9l1BS9IR956c/mpisHqocPPDBn/cd6mgW8++uTMxd9fWlubVN57zcvR+xdfalp1'
        b'/T1Hy3/2bXflb8vf9e4+teL08js+ePn0+I29h14yclH17o1/2p655tqq0RXLup/4eZn7/ZFvld7SuuXI/jOe99ybfM8nfHrOH6y4/7XnT7+Y2Pz1H8fWXRV54PdffeGr'
        b'+uiLbV8/8NdNHx14p+gfvwnPOdWa/s7uL9+686Hf1g3sf+OBcyeuHyR9fsOOqw6UfPXzKy58d15qyhV3tH6yP/23c4PldWs/K/+u/ERDbfrYN3q+9skbOx5c2PLqxKe+'
        b'4Rt2fXTk0k2fTRh7+q4zM47feWa379TIHqO2/teZ+yY/t2TyexNbPls4cFTvUeO+f+MX28p2H3h/891L6277VeXX7/zWduHh1/bPnpM3+YOMx7utyRnveeUvhyoD5c8+'
        b'MKbium5PX/7bW9fX2u/bE5j95fbeD5985/N1G5Pu9n94Vnk77dGJ+fm3f5oy+rGCNa99/Nk3Mz+ccfnhM0sKvz/5evH3u69d+WfP4nPcwl8/9P473V0J5KdnTIYVnXEW'
        b'qxuHzhyiRTguVb1+hHpcVB/RTmr7WSyoLdrO7uTjtaxgMJpyP1qsbRfUW7RbLmBBr29U70prH/UaQ167ajDo9RZ1I0XZ49WtU5kkU71Xaa9DCd9v1YN3m/qpG/D01YYm'
        b'yAUCl6SezNVuFt3TpgTQB5i6Lq0QGkFWkbpMFO/xdFrdzNxasfPp4LiRPruk3eEMDEeyWd1X1iZFXV5cWjJE2+Q6/1S7j7ad464usXP1CQH0kzFB2wt/7VQQtD3q9R11'
        b'ENTHJgZQdtRfe8TuL6RwQFuafuDwfKV2q7pnsE19TD2eR64+c13TzhPyqo+rT8bEvOr6EgqWM0y9XrsnhqbVzQv5PrkmIMN+0pbwgxfX6H9jYf+/XFx92Kb9n34xRFPe'
        b'hgpZj/eIJ04Cb74Srf3N/I//kz509nbaUD9aEPF/Ki/YgDC2pPFCKtx3G8QLl/TghXQB6J3++b3GO3tmmqSLBCGTv5AXvAN4oQl4Uyueo/fnhWSBz6VrL17IQSUkwURX'
        b'SyaUiqJbQRTQ1Z6p/b2DF6zsCf7vywu9BD6dFxz03knX5AG8o0Eiw15BhPZJUGKfbMiZyTssDiorm+qAFi0WeGjxKIEfzDvKlBdiR2zX/y/Yd3Fpo8pxtK7kdDcCqzrx'
        b'HE8R0fpqh7Vt6gbmX7B8thpRt1gA9d7ZlCX21q7T7qrxXH+R4O8DgPnNiNyCm3/le2tY8vXFJbccf+7bT58pOS4/tLu0+I2pd+zbsf+5a2bOWXj8rppyxdm09g7/R/2e'
        b'aYim9LS++7flRSN7pLYO2Ob4+76fS7M+7X9kp6s6cnbYl7N3jL3y7l2Jdz93fPgvkn5x363vrlGXz80ZsH367/eF3317zolfT1g66ODDf+zp/tMk2/YHbF+v++tKJX9j'
        b'zoZNX3654cCqAy84Kj9dZj4pp867rv9B+7PvHEtyX3rTPwbuu2HWNOeR34wLXPpQv/k1W5utOa/+5cqB52be9tVjr/yxMuuLHct8BdqKn7/4yq4/nFn1ztIPD79Ut27z'
        b'6oJXjvxm+5gdjz7b+3DdkRcv/ODtPx3af2//Aw/+rseMLfe9fjr9VA/vwVO3evvVFUxaPuvSF1sPHPn9047xJ02Pvv9amXf3m3Ne35z73Et/ONDthezLh9fNcScdujvp'
        b'8N4tywZv3frGnfuy507fcui+5wIF59559trCgi2Ha8Ye2PenjS8VnHntoSWXbDkdLvsv14H6+q3fbfz9G5POLN5xpknLK/904eKHPGPeuOFU6zXXnrhrW8vjvS8/Wzfu'
        b'tdGPvMY/+vdJt7x35C/e209+UXFAKqg/+VT9uLKTx08nuHY2bDq6Y9TwrTtW3vPtN1f9dvebkw9lP9fNHco5KwiprjH/yHliprZ+i+Ph5/tsEWaNuSir+/w5U3snjvrd'
        b'xT17B978xe+m5oi93rdO3TjsWem5nZXXj00f8wvXS42b8xb87ANhxzH1Al/yu19/X/bV6++OPfpVZcNz8yatnhVMP33m6lsnn5pV+6prUgBPP7Ub1Xu1kzpIbdQ2DNFh'
        b'SntcOzRXHG7pR7unepN2owfIhs3aXeRVj4gBzJeCZMxW9VAWC4m3Sd3EaRvUvf3iAk+qD7VMpL1Vu0nbNTRfvX+IGfbWdX7tDv5Kz3iKX6Xdntg7v6RgMPpSAmrmYfVh'
        b'ik25sUTbYOH6zDOlaofyAqRKfAD27TiP3X7tGsO1DXPZrd6k3k4EVaP2+OwSyKdtdGHOfDPQOQe50WKdIJFP4GTthlRtQ562Y+hMbRO0cyavHg2qR+idert2j3a4RNs8'
        b'SOAEn7pDXctPcmoh6kSptq2hZXA++gIvN3HmiwTnHG0zOeu5tA+M5DagkZCKG1TAc+ZVwnD1UA2RXdpB9c7yEnUfUGvw2oUR763qSUENrdFuIzdBSdoOLQRUIlBFQlDd'
        b'Vs9P1raq97NRvSFVvQ3KvgHfqUe1a7R1/Hz1iHYNNWhV2eXWmjg/VIJdO7mSdWOj+qC6m/z5wYct2skxfNEM9Th7d5+2Qw1rG8oLeSjzBvXYZfyMJm1dgIJUb9AOqwgW'
        b'YaDgBs/UbgFu9U4YDaTPkCDLG2Wapl2v7mTws1ZWn0gAorWkwD5Iu0F9QD0kqXfncD3UpyX1Vu2eMhY+6drLLib/XjA02v4R6NyrBCjTjGXSCO3+JeSNaNaMBdoGDIIt'
        b'qDsvVx/nixJbqH9lS7SH87XwUAxfeEjbP4S/TH3oAhqyYqDgHtE2FOP8CVdnaXv4i9QTF1B92jH1UW1tCWFJmCr1tkqXmUtQ1wnagSrtKGvSQW3fVOjq/gvKywuKcUJL'
        b'TVzqeBH6fa96HblSU9SdWSUskGt5GcyaGVDtEXXrVeI07cRsFs3kUe0xnPGhZo4fr22Yx2l3akfVx6l53eQl+dDhnW0hWtUHXXUsOM/mIujLBm6mepi5w5AqefUEP586'
        b'PA2o0V3qztKSAtcs+M48T0ifxMJg+5dNZyBdXFypbgQQSlB3Ctoh9eRVNBXqgau1rQBed2l3xQhq9OGYqq4XtbWV2s1Ud/rKypLiIcUFerOcNlgJYtkFbqp7tEV7ukRQ'
        b'H8LIrpwk8eod6p31xIBoN2vrL87Xjs2h70ph0F3FULS2VVSfhKG8lbmmuyO7Or9YPTLINXQWAGvSIHW/dqeorl2wjNyczpubUaLdPyp/ZjEsuB68uq+fdpxxP09q+6uh'
        b'5U+ptyEOAN5GmsOrT2kHtUP0obZL29Izf5aJ4y93l3AwpE+o62lZWbTrrgYAR8AKaxG+cDaMSVDQble3aTeyCdozMhsQ0gGogSJVSsm8euu0QhbgMlBVoq5fBTzSBSN5'
        b'KOpmwaxtmUQdKV2p3laSM7K9E0px/CDtAPOxdzPA1JMl5S3t/UCKw9X7tWMsEM5dy5ejw5+NsZXpBDS5Vd0rThWmEbOm3To7K87X5nVauM0v6FDtSRr01Fztxvw1gBc6'
        b'eOUUtd3l6qMBFFpr21NhqACrFMAqGQzTA8v0ZsAks2lQNvbXrikpUO+RuFL1Xou2btp4Quja9do67eYEZEcbtd0wovB9CWKlNO12Edb7xlQWynhdbf8EbfPQglllTXS8'
        b'qT06YQRSHpj1gsXm4p5jGHpbm43xLGB1F84shR3kYUArCdp+QXt8wYUsw56MPuSlFrYO7RZ1fSEux6MCLJZdTQQC1lWL8rWnW7TNs7UtJUNcBTDZ3bJFgOftbgbcT6gP'
        b'5pVMuBjXKgxHpHjIrKFQl5kbwpm0XeqRIaxbj2r7MZw77WabyscmuoDnUzfhTpWeJ8H83MLGfk/DRejOuLycNr371BtKLNCeh3Ex7dD2sQo3z1UjJbMAtGavQJiEvWi2'
        b'ZZV2N5elHZUWagcWExbJUPeqR0vU+xPLC7SHsEAMNZOiwaa4r7uOai/VboMB3TAuWd/PpAJePTJYZhvfnVXqWmzu0LbdD1IW7aZMrmd/SV0/WruXYBWIu3v5bG1/SXHp'
        b'4FILZ5YEq7p9GQPGk6vUEPm9xc6u0Z4ogLHVDgAY+bVHfpSqlOEMePR/AIf1H3eJHRsTt7cXbxKsgpVv/2fnkwXJ5CC3x72AWhd4q+DU37BjD0NtSXeIINj1+2TBjKUJ'
        b'GCQgrV2ZDjo6YXnQpESiXHZ2SCKsEuP95Bl/5n5mngm5db1uG7kSaGp0u9u83xknBS/y8f3DG+I+HH/ryH1Qjnb6DIkcOqNk2gT+Z+Baycl8LfxFFoQXoBJaZCD8CvAr'
        b'wK8Iv+nwK8HvpeEFNRz82sML0J4ukoP5azEnH+JDCwy1uRYOVea8Yr0USao3tfD15hah3tKCJ4IW2ea11ttaJLq3e+31CS0muk/wOuoTW8x07/A665NaLHjaGEiG0rvD'
        b'bwr8doPfVPjNht9u8Avv8bw00ifIhZPgNylI7nQiCUH0Q85HkiFfGvymwm93+HXCbzr85qFuN/xaglKkr2yJZMhiJFNOjGTJzkhPOSnSS06O9JZTWqxyaotN7hbpERRl'
        b'LpyF+uORfnJaxCV3jxTK6ZFyOSNSKmdGLpGzIjPkHpFiuWdksNwrMkTuHcmXsyOD5JxIkZwbGSH3iYyT+0Ymyf0ik+X+kTFyXmSUPCBygTwwMlEeFLlIdkUulAdHJsj5'
        b'kdHykMh4uSAyVi6MjJSHRobLwyIl8vDIUHlEZJY8MjJPHhWZKV8QmS5fGJkij44UyGMic+SxkbnyuEhZ2L6ei/SXx0cuDmTAXYo8ITJbnhiZKk+KzJcnR4bJfGRa0AJv'
        b'csNC0Bq0VeMopYWcoYxQTqi0WpIvkqfA/NmD9oiDNFja3LI6Q0mhtFA65MwMZYV6hHqGsuGbPqGBocLQ0NCw0JTQ9FBRaGZoVqgkNC80P3QpwEMf+eJYedawM2wNu9YL'
        b'EVuIBURn5Tqo5ORQSig11F0vvTeU3TeUFxoQcoUGh4aERoRGhkaFLghdGBodGhMaGxoXGh+aEJoYmhSaHLoodHFoGtRcHJodKoc6C+WpsTpNUKeJ6jRDfawmLH9AKB++'
        b'mBEqrk6Qp8VyJ4ZE8nOfCPlSQ9301uSG+kNLBkJLpkINZaFLqrvJ041vWhLCzmAC1TCAvk2AWhJpPDNhhHrB1/3o+0HwfX6oIDQc2ltE5cwJza3OkotitYvQVpFKkq6y'
        b'4zy2OMJ5YUd4cNgRdISL1wuorUFPhtCTIezJVY5gAilqzWBO9MmNRZt9SNeKakilMLujMNfEK4kB0nCs5Q01cF3xvbV7nn+QK7eG6ZRW5FY21XgDNT6XoFyNOGgwVoT7'
        b'YZcuodzVPhK6oT7aRpNuv+WgM2PlJcO0xSUBulvqCVQraEth9ayqIv0ZMuDGk/CG6qjD0CAizSEe3XvUA36EOzt6ma5vVDx+P6REb8NStPBFVTMKqXAWu3yWFDywXWfx'
        b'SPEsqted5Qx96gbZA1iWHC2gLnpUbGxojNqhdNlTXYGWDtZqNzteZZaFbY4YYpg5aq6mcqIJVQ3uCmUpBanEEJvuupUNPu/q2CM7PPKxwqIOuPcHKnS3llZIVXsrlvqj'
        b'Frijwmx04/MH/PSWNOiphhUVSlsCFXQxRd/RjZOeKn7Sc/A1UDlemMCKSvaB4vGsQHfimEA1BkqYqryeCiVq9lbABA+PipU1S0nvHD2+sDgTUTsGOmb3TKvnV/okB5SK'
        b'Kg+GNXS7IXulm02kBe5QLyEquRVPddTplmv8FZVej7uqomoZ0ykGwJCZQzKMyNEqDHJ1CCyHk4jkGHP/JLAYNqg5hc6T0PcpnvpPw5N1gcxJhfVCC788McjHG8p2dAz6'
        b'z5whIXB+GNOzJJrAYQBtuzaSdqrRxkfgbdgCmM4BCysLWxLkAQcJ1WhzkUReIDmyxBDDuaTvJQWlsL2JU6aEHS2moBBOqEMHSI4Wsy+NUpwyNOxI4FpMYY7ph4Xt4VR4'
        b'44S+OzJwLMxhC6R7rxeC5nB3qFHwXRIUlGJ4lh1Or0Y3MSWo0QX1dIN6LqPcmfB1LyzNNw6e54RTKJ8/nAJ4x0J2a44WK+S0hNMgpwR7BYz1erSJqQxKsIPwVJ4Zyrsp'
        b'bIZvbFRqT8iDM+GEHtrhe/27oA3u7HiHkXaCtnkc63uYh++Pw3dJ4cQEw2ZODCfTu8RM9IQLPKHMBRPwXVAATJuYwTE7LvLeaWOu92Oac2wkX4Txt4d7QL0CjkfQlEa2'
        b'eLEReIPammGMQNDwysbgxPHfPA35fy+a/knSa4Tmz026sb7ToFUFZpVlhnsz2fSlolIQOQ11kMvQdKJzzUD3pqPyj+gUkoVeROVaxTRekqzfAYIX2i2TFH3noWXyiqAv'
        b'EydMtUtfJmnxywTeijh9YQl2p8x2CwenLx++kegOQd4UlPwBivFuDuNfOky7iIp2QYsyJWghYxxrEGpjwAMLpccEzlcb7hnuFx4A4J9VbUIvRwC6g1rsYVRXs0OpCUF7'
        b'uCcsxzoAvKQELgu3ZBHunXgfdNCCg3KCCUAcJukATKp77F3QDuA+yzc63D+cGO4p8+F+8H8A/M8JD6rmwylYTzgHl1UaEJfwvEeYDyeHk5Eoq7HQsjYhGMNCSglaoTeJ'
        b'APDwG4SlEXZmci3OcCqQAvjEmcHBskkkEiEBvgLiQHmKvoc7GVWDzaj21GLyrYCn5vBgKDUpmBTOpDyADKC9SeFcSuXqqf6U6q+n8iiVp6eyKZWtp3oYLaVUT0r11FP9'
        b'KNVPTw2g1AA91YtSvfRUX0r11VO9KdVbT/WhVB89lRMbOUxlUSoLU9VJsDEUIGkf5DYjykREAH0NDwwnQo+Tg8k3ohcria4WvBK0ZCC0QBkw+tXoSlvvTQaHpoIwot0Q'
        b'yqBUkfwdSDj2iLjpeX5QIjVayQiL0eYmO+X/ytp1Ff4H4I//eRzlgh3WvzGGo5y6Sy5UQzTzTgp7lcoLksCzP+lbq9VOPkfTSKVR+LuUyFQZ0wRUVpS+sTsodJlkN6cL'
        b'dsBf8Md39Sd97khNFlMBt+Epq/S9w+QgB+Ht8Jth3UX4jfl3BAwGbHPYquM3c5iLw29i2ETbORAsYRsQ/IDXmHq3bndh+MLvDAb++y78aVB3mHWdNx3xi4DkpQ6dshqd'
        b'Oo6dkmCZIO0hAFq2sY6sJ81NpRtqm4eT0aElPZeClBO6mBg24w4NQ5EEiCoR0TamUG89bN+SyWOpCeFUXIY4WITERBMg2bBtNJCAE9pprPuswzn/9Hh9dUCCgE4B4Yv6'
        b'fTKUQlrXGKCHyuPa7fGdD2q3/1mIvtsc01sHGBbwarf04s0wCal8L4Ix+/kwZo+fjmYkNYEsDCchGRybDkmfjjSaju5Anon+dHqD6XRMk5v5vgB3DjT/pXf2Lak0eGgi'
        b'b8kkgwJMdTL049sNPRB8YUsWmr5KymNB0V9mkOA81icBQYm7s0lpwmCMiGlhXzPBDgST3WJpNqEwgiz4bBIX4FbXGyX7+JUcfZHJvvdfSsy5M5QMjHlaKKPaokeIscbV'
        b'YkXMr2wNJ+IT42u2JwKlYasW6iTlGLTlyVjJNhSCwDdH4Bt4As9tsW/ia78t3qZN92gilnVqmxNzVBuLYoicCnQahp1CK6BHCQxsgw4cG9KRdl1hMNtFhuxPCFQq7yF/'
        b'+Rf+J3vxiDpr/O6Gymr3SgX1r5UvzDoPI/GS7tCVYVSeWPh/KaBG1n/S1vCsWTfoZQsJtdcdgoM2Buxur+/tkkTuczByJdo3sxAkEsavtEufZabZLVYhlXdY8C1uI3D9'
        b'h/SKVCDxrkwmowhiXRSUQvSv9iu/xWcv4+V3eHmFqUqjNxu/8irZBjR7ayqV1+i2viKwTHmdrLLhxlOBEQ+UU2TrUiMreVQo8O9RsaISOP9lFX603Y5adAdNUYvfuFnq'
        b'bais8Ppdif+eAXRd9h8go//fy79yqIEw2YJMW5RDhyxWqf2BhlPINDl49tfxwIP9SZ38OTp9+q//mfX/bWmHOVWULLNF6QI7Xy1KtXY+V5Qcw0Spl52fIEpT7egCxIrs'
        b'JpBwAvWzDG1pHucotIE7Xgbodusrsr6iEZZlQFFu5pn9LvkoYGcpL9G6m76qytOI7osVPBrFk5Wqiia/x+2Oprnd/qZGkh2ioA0tVeBpgrstoXzd3uFEnKHrhPoGucnr'
        b'QQc9zKMT7JNSMrqJ7fSExxpkv0JfNF00dA4lNMZu/T+pTfcd'
    ))))
