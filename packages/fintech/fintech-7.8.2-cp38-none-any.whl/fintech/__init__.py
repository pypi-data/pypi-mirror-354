
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
        b'eJzcvXdcVMfaOD6nbAGWIiKCCq6dBRYQ7BU7dVFs2AILu8DKssAWFVwUpSxd7F3BClbsPZqZ9JvkTS/cJDftppmbN8lteb33Jr+ZObvLUoya9/3+82M/nD07Z/o8fZ5n'
        b'zueg2587/o/F/6YyfNGA5UDDLGc0bDOr5bS8lilnW5jlohywXKzhNHwFUEs0Io0Yf0tLvMwSs7QclDMMWAoM03igdctzN65jwHJ3BpTINRKte7qHRoqvMnrvSa9eWvfN'
        b'zFIwFmgky91XuKeBZcDApuFfC4FbhcLtwSD3Rbla+fxic26BQT5XZzBrs3LlheqsPHWO1l3BfSPB3fxGSi4svnQwEVmMy2g4/C+xf5ui8MUGshkNHk+FtJSpBuWglC1x'
        b'tzLluMdH2IXAypYDBmxgNpAeANyDHAWnynKdHlLZePzfl1TI0ylaCBRyVQf4K3m8SE+6MmyOCEiBdKgkNkOf+VQQ+Eoo+8P0NtBr72hlY0jvWBuwcdmcs4fMk/fQUXHX'
        b'HvIqSwS+75eJ9i5Uol2oaRGqDl+CqlFd5IK4RXGhqAHVK1ANqsdFE2YvFqPz8LZBZ5t0H5jCcLm3H6juZ3yboc/+LuPFL8O3harj1N9lvJLpl5Xbtjpbz17cHDghBmye'
        b'IVkatlPBmofjEvCOgvHA1YbhSivRDVSfbFGGotpIFgyGl3h0Hp2Bd83BJOMlVDUX1sEtaEsizgUb4BYJ8MqF13254KdKjW44i4LrYEMURgKawoUkPvCZkm0sKNEa5NkC'
        b'VEzr8FKbTFqjOT3TotObdQYCECYxmY9AGePFGGWOom1cB59tMWR1SNLTjRZDenqHR3p6ll6rNlgK09MVnEtL5NLGGL3IvQe5kEoGkIpJEvjahxUzLONOr5YROAVdh/vh'
        b'ncTwCJUyFNakuE4suhkfHiNCbavS9KQXn6peZF4RgQmfgD7e/0oLSxsKKPCwegtrloLC2NEp/etYf4sdeD6ZTp9qTHnM22zIRCDPmJwaOFsocsiXBTyQh3iADL2ZGy8k'
        b'bs6TABloVXvLM/T69RywRJLJboAXBnjA1nDco2q0ZWFUqgACIRHKEFQdGRqfzAB0FLWsXCFNWoNuKhiLHJdasg5WeeDxJCrdQ+CmIagWnoetPBgA7/BwHzo7zxKEM/WH'
        b'23HteB0j8ZjJtwR4pLBefdC2vnCHZTBpvBxehLe6LzU8EOOFl3rqUwrO4k9ytcC9aFOiUpGQ7B4gAuKFrD86NNsykMzt5jyfRDqj8fFKFnjAPeyUFNQK96PLtIF1s+Fm'
        b'VJeCahOSI1BNEjzNA3gctvnCcg6VhUhxA6Sj8BzaxSTGh8crybIkiwDajcq9UC2nQk0mS3+cYzYHa0gGEYC16ATPM/Aw2g43WSi43giVhNGCyfGoQRHPg7HTfNF2Dt6E'
        b'9bAGTxgBDj9SZWJ0DM6RiBpTcEWyjd5DuMnD5TgDGcmCeevJ4/hk4Sk8DE95oXPcaHjJTcFahtKxDkI2dAjVecThxSpEdag+kQzaDx3g0Al0Fx21jCSYjq6P8ECNkcoE'
        b'lYXkiUdXUE1KUrwSVq9kwdgV4nhog7fwyEm3BsEzPKoLV6HG+PAIMZ6/S2ypEl1S4OkjQ0O7oG1IGGpMwssTrlAm4Jk5CfoGc3jse+ExyzCSZZsJ3UpMUcaH4VWoiQ9P'
        b'iIyISxYDWAOvhgMR2guPptHxKdFZ2Er6E4afRzDAAx1hg2aja7Ngq2UUfj5QA1sS6XMyBfOnF4YkYurQiOoxTM5XisEsXozKMtcIGHUFnkcXcWY8rgUhcUmoUZWUspjk'
        b'gtfg5fBJojm+8GYXEsi6EukDlOrbGExbORtvE9nENolNanOzuds8bDKbp83L5m3zsfWx+dr62vxs/Wz+tv62AFugbYBtoG2QLcgWbBtsk9uG2IbahtmG20bYRtpG2UJs'
        b'CluoLcwWblPaImyRtijbaFu0LcY2xjbWNi57vJ1+g2oe028G02/gpN8Mpd+Ygtvpd253+u1tJzBd6fdmlYVQVdQCqxb1SlwwZSlcitqGwjLLIJzRWjCY4qJKqcCgQPDM'
        b'N4NDl2TwnF5s6UdWAJ4tQXUYQDlMqtEediMTO2u6JYC0cXMNvBoG28LjRICHFUxGDCqHu2E1xU5MyTfrwxRKVB0v8l0JxPAUGzYkg2INqh+XQFYpHK83H8/As6HwDiyX'
        b'0Tqn6tCORIyS5JEbAw/CE/A4pjwttM7VEydjGhRHusLHMYXwOrwEjy2w+OFHSXB7aViEggVeehZeZZZjUKwVyqBT5kR4CiOxeGEfINazIegctFkC8aMEdAhWJqJahMkM'
        b'bm4YMx/ehmfjMREi47Z4lFC4Y8DQtSxsZJJgGyqjVaom+yZSKAtnFgcB8Ti2PyxDQmvZQag1LAFjYIoIM7PTQBzLevmK6chCl0+l9YUoGQymx4B4HTsaNsM9tPvorB5t'
        b'xRQghAXw9iDWwExLjqRzBY+i06PxoBMYAHegrSzcw8wtQK20RnhwzgyKGwqC71J4l001QNsohUAd76IGPFvJ4bjyNtTIWpnpM+BlYd2uw81wCzyNasnDzaiehZeYReML'
        b'aLloVDEukWA+qucj0FkgHsC6xyrofOEqt6EzqC4OnsXl9sFatpSZC8tgDZ0vtM1/NaapeOH8FCysZeah05gWUHK+vx/ue104qTMsIh7PjkqkQntB/1w+egaqonQgCl1G'
        b'2xPDCMdIIOvrJmaLrHAnvIgqs1gXoCdw3lUSwnKQjXFKQmw1lntKOYxJrBOTOIpJ7AbuYZhE/npKQpxK1/zfKSLTNMIjw5T3M17O/DqjOudr/M2/WR+7zy0vNi6G0WXL'
        b'PZ9dFu6RtmnKrsr6ellQ7P9kN0266lWVIX7NH7wt8to/ASgkZkKpV2Aw4/HUU76GGlIUqCFeYG3+I3gO3USHqJyTJY/qIeX4wmuYdQTDXeHmUZS3YEJatQEdoKgbnozJ'
        b'YU1n7sFwK4+2oivBZsKTc+diaouzpWCARccwW20kedxRE151eBKeMxMqgMrQdj97rqQIXDlplJsZxQ0JDjLTtT+5IgVeXxWmjKPsToous7ACbUf7qQyHagfDM7QvmCms'
        b'X21nC0JvRoSKUuA5WGMX0LqJTDSVCkwdfL7alEdFMSoxbZAywseLcWeMfR15FXwHpzGZOziTMctISKDRh6SynVXie4JSxn6Ommnhjc6Ky7uIYhQhGuDh1QRXUKMY8OEM'
        b'JolnsQRy9eEyeLQAeWw2+wQSeK9wx/cGd598PJg1EZAZJZ90P2PlvdefaXru/Weanr/ctLXPi17Zn+gZELtY9F1rwFv9sBRNaUGDDlYkhodg4pjIgOFovxSeZosHTqUQ'
        b'lYvh4yQ6lNYTrLhgaZQwrWzva2Ix6/Sd4vFGIPVhjP6gUzzmCjJX974MWBgOcK4AKVJNqiG5QBl44OW6BoSLoasLYXkYlbQwLTYy6BgG1rvoabSryyow9v+Fjj5Zycxm'
        b'KxiV0OtAZ/87B+FlKEgvyMy2mLLUZl2BoZ4UpTSFpZKRbA0msIhOTUpCmFKlIjIvli84EAYvifQYVfcNhOf+171wc3RB2+TSAUL7glH5OEw5hbYxcvmicm4tpq93ohc+'
        b'HALHEQhkCAxiPZB/Aiis6A6FDOiN+om6ZnLQ3cHOtindtfHOth+H8mb31rZ7bxjwOTRzpkScsMhkPv3ZNxnfZXyd8W2WLEeanaEOUb/4ZejFTE2rNkPT6vt1xjl1bvYZ'
        b'bas6l315f/QxMPed5+4HDA0YGvjTnqFltzEZHgPe+7dn47z5CsY8hEDaFXQR2iZGm+DZOBXWZuyL3Qc1cbAdyw23FYxAR/jutKobcojSs9R6ATtkAnb4s4yM8cE0q2SA'
        b'KVeXbU7XGo0Fxogp+gKc0zQtghZwkDFebcwxdYjz1pJvFxzqoVWyRqKNGIOd2EQo9i4XbPrO1xWbyOqgS5kAC+ioOikMi3/K0GGwCavUaBvWoWswH1BhmQFexWOtk6RO'
        b'xLrLdDd0DVYs0XnnR/AmBS5vnrkmLyc3R5+jylKpk9SrP23Vfp1xSv31wtexau+e/UmSBGjbxeea/y0M5jEnzMNlUlyJSj8fsVHuzOrZ2yQY+zhHT3LucBn9911GT6hm'
        b'KjrrLYwetRqFCaAGhYHwJo+1jc2o/eF41cP282iM6gHV5I/tAdW8apGO9ZjGmQjHXPDZ2EQ1ESfi1Py2eoV8XN89mu8zpE37KHHP+bv4gKpZwVMGjnZnocuUN89FF1Th'
        b'SpVAvPvAyxxsnAYPmIm9Bh1GW7CyTVhwhBdQhoQkKCNgYwqehC1h8fBsiMDS09Kl2VhCb6HiSHqAVuD4Lnn2FJJsA9BOLKeMHGgmmly8Hh6i9SoSklTJCVirohKEFO4E'
        b'w4eJgtBOdN4VCFyW29NiyMpV6wxaTbp2XZYrngwWM8LHOMRRRIF5Cc7ViQdtdqBijEOdS09yH3JZ+i9krktP9c5bukFhVJmOw2hdn6j2T8brjzFdDEaUYEHkDNzfZakc'
        b'a09kbQddo/rfE9HUHrY1HvTG2aUqPZmAETPdpJq5QD6HeXnDftMHK5/KGWfpr2MAlUWmLSwJU8Zj1LwiQ0cAVpWPMPDKKlRBLUFZ/E/eO7yZkB/Ar2lvBfwU9qpgwdkz'
        b'jyF2nXUgXZf+kkd/IbFjoS8gkCaPMq48MVkDdAG/nOdNBpxSMnJDolqjbtW2ar/LKFRXK1u132Lk/jbDkB2a2qZefq8JXm7qE/q81M/jlJo9ta1Ne059VXNG7S/5ln1T'
        b'NjRjUuUHTFz/Af1+ejuq34/gub2paYMC2tuYl9s7Yt6O7idm3okWxxRmYxRID3r5xrOY6lJjyhl4C0v4dGnQUXSFWDOksInFygw80TvleCQ94XPVplwKV3IBrkYRedGd'
        b'fgTZUcbymCLTO8Y4vBPWBIraSXN7b58RslHQI4VPuIDeh77dpcj+ybAeK0dYiMRr348JgDZ4HJPdXY+w5DLdLLnsk0MbmQK3HtAmU1lIAmocilW97Vh7b8oDkSASVkZS'
        b'+JiymgdSEGB1i82QfZleKACNZjVWrUFUGgcywtdFLgRGQqF7u3Qw6bqRJ0dxplr8Y/LlPypfmewFo3wqPg2cvm2CqHQCMy/+MNuau0Q6wndOYeWB2udFtvaCWuUR5dOZ'
        b'8379l8/iL+qZga+tuxMW7Dnlzs3Tx9NTZt8J4/tGSPf8/fl7moojF32nyjPfuJ/263H1wmFz9Uuey7720V9ObR2/Ys2vCWERf/278p2IG/eS4D+ZTVsHv/rm/k+Cp2/L'
        b'H9YesE3hQWkW2rIEHuzUs0x4GbqoWqfRRUpa4Q4zLDOF6yQKBapNClXGO0zPoStE8O66EVQ3grcLctElFTxrtj/UoJOeqIwbMw21CbWcGQbv9LBW7kG1RL6eDSupAqVF'
        b'ZfBkWASqLipBNeEMEMNGVolVqEozMV3BbRhWDnbT5vLXuOpzyeuE3hzGuvTRsARiWElSiYAHbMiGF1h0EG7tJyDansVoB1azw0MVmNxFoC1YnAUgQM4/hbatowLQeKwM'
        b'7BFIP25J4AzuyBZGVMKr8ChsNlOBvGEI3OHUKLA6EY7q2GJUBU/Q8UjRcdQcplLGhysULJD1gTVSTgrvwrouqthvqHviQkumXiewhTEC+k5isbLni5FVzPgxPL6ygP2V'
        b'Z/H1F57D1//wPL7+WywSYwSXEZQe6ayzf6/NBTrxl+S84YK/L3XRAkk+n8C1YSHJqBZrwGI8vHY2Fl2BZah1DG0gS+yCcL5kAhwIN5Qj8r+VCQSl4mqJVVwNytlSiVVi'
        b'UpV4WblmYBW3MKXSpcDgxwMzk+dunMAA8lkGDP5pWEa2SklJq5jUMQVoGFLW+LNVVJimA6Uiq6iZbQGzwaqmlWypW6k7acHqVs4aM2lbPL47YRU3cy20jmae5vUr9ajm'
        b'cD4PK5vNWd0bGQYUNRpiaQkZ7p2s2s0qLmdwf92rpeSunKGlpLSU1KXUs1aZ8ctqmZDb0Uec/reizCbWMJzW6FHONjFGeTVTDfLE5A73Q6RhWxghdxNj+DfNx5jF2SzN'
        b'm1DtYc+bUM2Sup0536Q5xTRXYbXIngvfdcl1RsM1SzS8RlSBtcrZoJzBM+ypETdLrJ7NUo1EI21hSYrVE5c9pnGzevqDUk+bxOaBJTtO447LSa0cKVfqhcfvVc5opHmk'
        b'xTetXhoPvBpehqHOdB6n/6CRkRatXi2MP3nKazxLvaxsE2uchPvL0P6yxgCNlxWX6I8pdjaL83kb5FbGyuZx+FmUxpvc29OlGh+rcDfUpfwiTR+hvDMPac3b6q3xHU++'
        b'PXGezVYvevXW9LV6WT1JfeSZwcvqTZ4U1ls9yW+zsL4+eBQ+eBR+eBSs8XurDxmdph+eU9b4tPALl3kf30md6e8Kv0g6HmUfjT/+DTT9K9lAYO1D+++DWw+o9iQtrHa3'
        b'+jj6YOWaOKOfmbF6lzObGYPU7CHc2WXkQNWiBxI91sANytEP2HB5F7bI2lkjVaiJ9SYHo9Qq91LGyqwGW9kinrA9u5jZIU1PN6jztenpCraDjYjqYMzddW33KXqdyZxV'
        b'kF847WcHTxTjRkoGZeVqs/KwwtWpk3VmfcDJC4wPmPBvSM8euBdky83FhVr5CFOProocuC93dNWf7BJbCfdmTXw17nY506XbDiNLKOWda36DMBrD8eXfwK4dkV67g29I'
        b'ww+81fI1ar1FK8c9CxlhUlBG/CDApC2yaA1ZWrnOrM2Xj9CRx6NGmEY96EMTyK0ziafXvi45HaUfuMnzLSazPFMrf+Ct1ZlztUY8cjwh+PqNYNt5wIx6wAx94DbCtCIi'
        b'ImIVTifS7IM+4fKcArNjribhf4WsQ6QzaLTrOtyXkA7PIQofTsKtmjr4rILC4g4+T1uMlV/ccoFG2+GWWWzWqo1GNX6wukBn6BAbTYV6nbmDN2oLjUaikXa4LcIN0JoU'
        b'vh1uWQUGM1EtjB0crqmDJwDRIabTY+oQkb6YOqQmS6ZwJ6IPSILOrM7UazsYXQeHH3WITUIGJq9DqjOlmy2F+CFvNpmNHfwacuXyTTm4OOlGh6jIUmDWKjx7lUqf5IIF'
        b'yxQnrEodIPkqWfMqCmJEiOUZwg29GDFHxFcef6SMj120lTF+rDv97UvTcX7WH98PwCn+jI/YD9+Lcao/NZ56MT4s4aYynIp/sYR3erGCUOzLelETawDj9ytu8VeW9cOl'
        b'MH8VTFPoDDqIbESbSkaNqvAEiW8S8ErnJubAPV3M8lIKqnak+AxfMOtiraAZUHb0GmZdXClv5UwDimRmLNiSfx1mdQc4wuCsrJWbgpHHOB8zQyZPjL8x+wgEzSwmmVwg'
        b'aMGMCDMmHrMDnjAQk8bK5zC4Ph7XPR8zMY4wF8wI92EUJGxCpCH1iTQ8roMjv/A3ZoyknqJcgeEYT2j4wlYNYdQiq4S2JbY/Fwmt03rYKYD+5u2/+SmgSGZlqRlNpMJY'
        b'rCLrSBdzPrmonHckTSEyziRLzJm05g5OrdF0iC2FGrVZa5xNnko7JAT68tWFHVKNNltt0Zsx0JIkjS7LbEx2VNgh1a4r1GaZtRrjApKWRAqLHwFnLuZP4uWgSXfUG4yJ'
        b'mWkkBTMegwsBMx8BFAiwUf1JxgSwPowPBS+6mxjlucC+nQ5rIsmGX7KwRRcGr4nQLlSJdsXN6KGRkMYJDNHGemyrArKxmu3hUHusjEOx6a4tOeUsDb5Uk4VmajDXXw0K'
        b'fTCQ4YLGMRgwPHEKQ3hpOeOB1R/KrTBIYB7IVHPVHuS+hvjM8LgjpHl33B1ZttRpu3SzsgSEerPmELgmU0pNn1+STvBWIjqAkiO4YY7cU/FpPoZ4FjeGu1bO5AHcLXxn'
        b'xR0p5Qz+tHtiDNtzyR1O4QmsWTma5l9NRBuMBdn4N4F4Knr5W0mtk0o5K60T56uqFmM45bBowxtk5B6n019W3qgnTAfjD67DytPyeixyRmCRkzeLslksdr7PYHGSASUy'
        b'PE0iwpipMxVO2yByOFNh3MDT1shQ+GZUGMiIRtEhWaM2UmMll4MBGRNTY95a4wwCYAkCKHbaJwkDFyBXQyFfi6m39LGJYyfQytIpWSzEDeebZjhBFoMni0HTC4Mopn8s'
        b'oX3+lFrKWBkGZX+sNwxgSqLUWVnaQrOpk8lrtFkFRrW5qy22swHMmDNJ02QcGKmpEw9NWE0SPH4vmec6JGTaMO4KVWY5h+fm7NAExrEvxQlUPxjT3gGBJQMePgaHLKEm'
        b'1enJvfvv4kFqZ3ck9sbGMnZhCXDyYYJRY1BBItqJtiepVMoQhRh4RLDoGKry62HvdLN/m+LwRQuWY7FvObtDIpg3MM5Ls0UCspUzyzmaTl3Y7BTBDaMicRMkT3kb4MFy'
        b'kUBjO/rYXfnm6vTapAK1Rmt8+H7wJAAE652I+nGIs8VO/OZ/395Ez30RiYr6BqWiJksisSM4fVNQEwe84CnOpz9jIduDhfCUG6qDd1G73XWu04sFVTt2f6+kArAyRIJ2'
        b'oGPwoEUJiLtFOSwn+1H9YXPkgpAQVBsZp0S1sG1RSEIyVuYj4pUJyQwweLtNHaqk+1crEgYtVC6B+0RxqF6RkJyEs+IGiG8PzjcG7hIPR+3wkO7Tj68yJoKeMxXt9zNe'
        b'ymxd8xdtqzrt3h54velC2okKRWVb1YwDLXsv1Fwob0vjXswRX8gLmJR26YNafZl11wDx6Harm0kyS2KKeYvd5bWrsv4Z2QEl+PHLvuKEUoWImgzgmWgMHHXEdiGCt+FJ'
        b'wAcz8AishAfNhHhOg1fR7TDYDluodaKLaaIFPU2N0mjbPHgKXYI7MlG9kjiaFdmNLgMsPKzCnKbKTNSDEQHqsAhlHKycrGSBGB5jo3w4avkJgJf4xIiE5HB0C+2Mhw3O'
        b'jXYRGDFPtBzuRXsduxWPz0E9s4xazLXT8ws0Fr2WWixIJ8BG/MmhtgiWtxsZSwb3gNeILqWduz8mrT4bXwlx6LRDih6Or6yxkNwXOXplLCAgSRCWWCNAGf4c8nexaTyy'
        b'Jz3wyLkRN9OBR67smsFI6u7EJ9GTe1mIgIvi5MQnLxV1KYtHtZPsfl6odZYrOsErcKtlNAGNu6genSOo8RB0QjcXumDUonQL2ctRoKNwk1CoJzLBMtjuglDwADz+2/u8'
        b'mi77vFgXZbK7657SKXp1fqZGPW09LmkktMmyCF8mJcDzJmefC7u44KFtifBsXDJsdEIr2tllp46L9jXB7am+6Gx/WIbRDFX1gWVDsqnPZQw6j5rsts56VKcpCre7b6Ry'
        b'o/GDE10GJAIu27iUXAoiEUsW2kkuuWq8mKU8Xl7Oubw8XV5uA/8wIzRpximruZLLiWSm+sKmRLIvEyFsty6MC0O1qHkD2rIYI7lSgRqT4hc7yaIIwGatO3oa1Y2lVulf'
        b'V/FAGvsmALEZ+jjGHVAP5THoINzUpU7BQxVVCzvp+mXhhADmb3QLgMcXU6fW1dP7JCaSbaH45AUhqGapQCYX0HbdPUjLizHwoAsSdB4eQK06380+jCmPQOes/5w2fkMd'
        b'gF7KjvBVqJPU+mx95ncZ4cZvM17NfDnztcx49TbNi5lntV/HfvZOFFg8mVkcU77IFvOFoj1qR7vW1O94VHSZfH7V8fI5B5jhA19qesGPefujZ15/5sMXxs8NeOXeXga8'
        b'cybgrHSb3VcoB96Ap8mqDofVvTkLbQugpueRaCu6hD9daGXmZIFaxsGdAk29je7CA3iabkkwYexJFGfMFPyr91vt+4yoMXJmir01T3SRCwhCNmpbRmeD0LUBU7E+6Ng3'
        b'jMAyge8GDtVvKKLm6QzUiqrIFs/ZRTQL2ebxGM+ihnx4QNh9r0Cb4Bm4F57udf9dO+DJybMX2VVPLzRi5ZwoSZQ+D3DQ541AylKdGSs7rC/RfLFSUzK2J23UrtNm2Slj'
        b'p8zVtWYB6UWCMNcp8z5qG8m+2+TlLEDJtxlfKhkHKymjn/+4EnDLU2RR2hi44zfoBuaIrb9NO4jL8baJ6IJoDroRC6+MgG0KMBTt9Fu9Et3Uk/69oQng/+YLYmNj/zzq'
        b'J/bq6KyUfYDuNrrL9zIvZmi9MdpFfxjtlfqGkJy15ifv2UNDB7PzP2F+SVuyfCbQxbQFikxkdyxnwEf96m95oijZ7PiEq9MM3PWXQOCwyZqy6/KVIau+S109lMvc90pG'
        b'QenAATcnfPL9R58+O+rnzfca6yUR7+3cw89t/XlG0R+SL02cuuL7cT6/jjndb8d83X8/O7j65ZHDpv1dVBE9/ORPO80fmM5Puf3h5NFTmj94d3yu+up37xc83Xz1wtfG'
        b'2sCYV0MOPls7PTw76NnFXxQyjcP8Tt/ps1vpvXZPmy/8n4Cr0+eXhndcjlbIqDwCq4whzm0bHdrm4hWF2uBtCs9uE9CesIh4LrGbwAI3oy0Cch2Gt9CJ7igIb+QLOLgQ'
        b'HjETg95AeA5uE5ALryBs2kCXk+I2XkqBYo/TiFfBLfCsmexl9AmBm4iIo0RXUZVdxkHXRBSH3FB5QXeOIcJi0yEwcCwP61IXUFFo/FLBPxBtkcAWu693LWmnH9rEocsY'
        b'68qp65gFXR3uENquol12oe2MRPArO4hOwmthxLUchKMGwI9n4Lks+DQlBxPWLHL4DKLWSU63QW4IPIpzEPoEr6OL+IeTOy0f5cKdYONMOlTYCC/jHtYlMZg07QXMBIAa'
        b'56LLvyUM/T6FR+wkGR4u2E7pRYiDXpid8hzrTswjGBV98B3P+nqL8dUHa58lQb9JPewSHhXXOsT2tE4a8djaMJb41pD7QifJsOBLUReJb2uwq8T32/3CFJUaUt3T7Qnp'
        b'6VjNTi+yqPWCOZ1KlLSRDk8S5qI2mbK0mP6lCyNye6LpbmM63OyV4Apo94nvQSbpPuHpUpZl/GWYyhGLuBfcj07DptyHEToWTIJ3xHDvvD499E6p/dtEZAKH3qnFuqTd'
        b'4kTkGxGWbFgNV+HWRbvMddEu56vNeNYMeMZUWbxL7QRinDvrsfjiFImpQEyd79zsUhNfLcVSkwhLTbxTahJRqYknFpbehWIiNfUUisUq6psPLxZOtQvF8JrRVSiOc7dM'
        b'J8RnE6pdhvloSFxyBJZp7GqfMhXLQAtDiJ1usbRryAeTAo8kAhDd19sN7jYrWAshJ4njJia6qLGJ+Wgf/q7hwYDZfByqhIeohB6GdsxxzRYmSw2NE4MBJn5xBKrSrTob'
        b'wZnScb7jX5QHvTTRq0zuN+eN6VFfV62sHnl13PCR7w8ZMe7N29p7qpCIoNr1+7k/hhR+dTlbjIhP1JaW+3Mq35QtDQk99vJEbd9jP73aPsP71wGl/n/ZuPT46ycq/d0L'
        b'Pv8FbP21f11EApaPyNTkwSMJYV3VSHQwjxDmFn9KVGSWQZR8sgBL9dsF8nkGbhUI/9NYD7wcy9DhJMIaITbFV8thyfo2vGkmVkusNBwmQUIOAJSiTYXwOLsOnlVSGjwR'
        b'XoK1rmQf1hR3Kqpwd6KZ+Lwmw3NYzhWIa46/QFpnSukjnL69r0BYJXCXQFg98hzSz5Mhm6ubaTYG43SiVlK65u+gaxvBUHcZ2VWXMVJOyvoxJQN7wH6Es6yA8eIOLktv'
        b'6pBmW/SURHTwhThvh9isNuZozS407RGyGiaGG8g98cE2lpHLJidNK8WXw93EoM8HuVK13+qnglWp7HTNuJZc1pE58KBkJ19rzi3Q0AaMxY5J+g2mYixxdsqKLwcdtjBC'
        b'qSykBXgBXpu7Gp7rpFLSriFXk+VieDIenaFKy5yxxJUG5Hp6ZyStZBaBHvZxp9lqCugeeJQtcQYGMY8MDOqhiTkM1l1pSqBKCOzbA3eGmpZjyeESuuxRhJk/FkKuoQvm'
        b'NeiKxxrY4F0oQxcAmIpOiFD7qPmUzMBj8Fgczl+TpEINYarFVPdG12FFPL6tSVE6wkPhWVQdHgEvpNKYq8vwpju6G4xOPDKUlaPb8v9LR/qeVFQkmBY8tehgGGxNcq4a'
        b'zqdCuxdxxDoXTx1G4Xm4CV4sNRB0F8aIdobBthAGDIBbeWM+atS5q9xEJmLYfhncvJ+x/ueXv/o2Y/m99qaW7W3lbS+2lY+uK2KarjT1eVFyYe/kPakBC/f4R5d/MTng'
        b'4gd1300K8G8vWxQVbY4SxRyL4qlz3JsrfbcNvKgQCRLQuUW40QgFjcgRYyp0MJWNKZlJ6UQYPCUJi3OD2ymVo2RiI9wkaGwN6LiW2DZ8UUMkqlVSYgK84SZudSm6KwR2'
        b'XMdq9C2cp1aHThMZDAPlRAZewGT9PPXjydFn2p184F10mzr6sMXoCNz6yHgND3VhoRbjIaEJXW1iG0G8jFIaH7qdVBKKqUW6XpelNZi06dnGgvz0bJ2rluVSkaNVSiUe'
        b'7hONyWSZE1vL8eWFbiTkVhf3nlQyE5fRLdiWmKKENUToTsIs4BRdatiQQowRW/C3wCW760+O+amJFCZYAw/55KPzvBC3cA1LuEfCyNTGjGOBHzwkQocYeLn/PGqdQXfg'
        b'Nqx/X0IX1q5Bl4tkYwqkhUWyIh74T+ZyRsA7dHtNCy+uNuH+XXDzXOPp7iVFF9eiS5GoGRcQgeG+fCmqEiKwUPmSOYmY6dGFHO6GF6udhVWZ6K6F2HLcYBNu7jTajvtU'
        b'kxSa1DchHCsFO9aGhxDBIMkR17BQao/hZQhiX/KYlZdlmUzIBrSh/Y7Cjy66C96Cx/XuqDIKNlhI6LcK2VAVrCssglvWYqXlmgldMmO5/xpq90F30DULHspCntrimoWp'
        b'eXoDruI0LBuLG91NbAZYD6tLkgBvtJVLHe5BjdvB84f1qHItuqCGF2TuYjA8noe109FRKtlTb0d4EZ1bCy9heJwM4JVxk1ehJmqvx3z9IAbw7SnKeLQLno+LlwDZVFYM'
        b'y9GhuAxqKPTy6+ehJCFqiUuFMXeSOmJVJCRtFdokWQRvwtvoBKyyEI/0qMlwy0Lc+HCs6YQMR3cmU9J/P8ttKGDxGDMywr/0swiulVt8xSFSFutU8gzZrLnZWLynyUNF'
        b'3KAWKsVm6D8NWCnkHWGVZP7I0LxJry81A8tY8hwrUofRpVRUhukYMWPVUNNVrz0tgGXSUqxpbdb131nEmMZj7BC9HpjcNFXFjfap/NO6jduSd/0wuCbx9SEtISOONHPu'
        b'Ic0D+yi2Lnn5zfmvjHNLTZrzrNt3VVmFoPFefGp069yP9UfG/GN9yZ+mFE+BEv2kqmEjU/rxf75S8vnQGT9caSzfENTx/gg9X2qpOJL1aWrb32F4e1z60MYJGwqWalZ8'
        b'7j+q78LXKvb94+23Vr50tuBs6YK39Ss++O9JMede/aDqz6pXP9SfvDlZuemV956O/+f1rxr+sO5Pb/U7ZPqoih9y+BfdezPmD1v0/My3rn300cs7v3/3U/SqYZyb6fCd'
        b'0G0vWqae+pnpf/25oOAhF/5QmjvhvG/8h4dOlES2DWq9/+PWUe+kJO7zevbrX4e3RF5/EH4ybGDN3r6DU+qN6Zk/fyGL+Kt0dfVnF19KGdX25fQVy0/+4U+vv5g7YNXW'
        b'FZ9tWPfXA9nDvwz+4OvB36SvqQy4pvCmIiMqg7vQ1kTYCreSowrqwgnF4IAHusixyNbfTIBBh5pkmL4wgF3DLWNm6DVmEoJWilqywuD1uXGd9DtiguBhWT4HVSdiqbQ2'
        b'KTRCeOyhZ9ExZqOwm3J43kAahE3WVYQuxGIZtI4tnQurBMpeE2UMg6dHp5CuEAlEgnvzNIuuJcJ2qrqjux7ogsOBMx01C6R97DpK9sdOQVVhqDo+PB5zblQrAt5TuOVD'
        b's1OyBDvfPrgDHU8kigWuWIEq+itVWL7pn8TH+gDaufGYdBwm7qzUmdUDbaP+rOgGvE6rn5uJjqM6Hh7HxVGdBPBKBgsHp9EZM1Fd1+UrwhQrEpKTGMAPYeDBmCnUlAJ3'
        b'jEU37XUSAoy1mx24PAbn/vAqHwefXksZ4mq4Q+fglatXY27JxvijOjon41FFiV0rSJ3iur10GlPQRwmpkic1IvTrla1RVpjayQqnE0bIU3dVH9ad9XHH/6wvQ67unA9O'
        b'C3BuZcuou44v9Vgnjj1eON2L9aVuQD6sjDVWODhwG+vCHB+n4y7+ZaSSO93Y5XMBruySbF8Ow6TxnJ1b5qBWB5npzixF4CmzFO6E2+BRBUcjluf0T7MrPETdGY82wSPw'
        b'OLwrHBxQiaXC26iuELao4Nkku3kYXmHRccw3hVjMcswiasMwvIWK4Q54HLOlZjYmz5jFdZP1/B3y3nJ86RGxD5wx+0yXqH3W1i/b37nNIfrNbQ6Oipr8p8NZYgt1+UvV'
        b'5uhMZq3RJDfnarufNRPh3iVvvFmuM8mN2iKLzqjVyM0FcmJTxgVxKjlahEQkyguI+16mNrvAqJWrDcVykyVTMNF0qSpLbSDuebr8wgKjWauJkC/VYQ3HYpZTv0CdRm6H'
        b'RdorR934gbkYd6FLTUatyWzUEZN2t95Oov4QcqLsTZKT83TIHXETJFXaq8cj7KVInraYuPIJpew/uhXUyNfgOcN96rUCiwk/FIo788+ZGT9rIX0i12lM8pBFWp3eoM3N'
        b'1xqV8bNNiq712Gfb4cWolpMxGnKIC6NaTpw8SXccdUXIVQV44goLcVvEI7BHTbpsWkqYULxWmWrSIbxWeG1MWUZdobnHQHoYdrxAd5XEQ0XD8+Cx6QkLI+FWjWNLP3Vp'
        b'HJY2F8YliFInToRtCnd0o3gi3Bk7dGI/gJpQqywQtrr1QAEfR/2qrigA7EjAOJGAtXln+zzB7l4PDYuQj56HTShVOB8lLT39tnp6ZQjdA85txt8VWUWa6RlZJbIH3hLi'
        b'rBP99VPeZMR3YyZOuZ+h/DJOLcv+OuObjPzs7zLi1fzWb2Sv1uuSPtDPWR5UL/9R9e6Uq17vmuUfPfO2Ne8Z4KvLNqur3zktun9a3aQB97Wrs1/5Mrw2UwP2S/3T77X7'
        b'vHJRHXL5m4xV9643bdraUh6omRnF5XiAA8OD+7bPs0djo02psDlMGULMT1HwthjuY5VY/txKH2ajC6giDDUSKZqHRzkLg2qgDZ548o0vUfpao7qQMpzgToazEQQRb9EA'
        b'Ss19GD9GTGMqShRGO9ly8YGyA7hLCqnRHtwteBs+tpWnjREKUCZjI/DCOgxQZfbP1132t6biJ76r0PawPNToQIReQlSptkaZzxxfRWQC5vpzYau3zgvVPdwTaJyAEOB/'
        b'H6Hcu9eCRGWZBcjWyS20MyZqTPS40WNj4DUseJmNa4osJnRt6GLUjjW6i1hruYCuoEveUpm7l5unB9wCq2E9iykAuuaGzs4rpPL+isgEsGM4KwE+GavrhwYLSsAK9zjQ'
        b'FHWEaBGrg4xD7MAdDueITKvwXcuz6n4vDPEqi/Lh7310PzBc/LM7+5x3+yf7YjezpSdXP6j/x0m/sXvjXnDL8VoWvf3MhC9XrZyi2TM7/k3ZXW5lctb1v6/a91qf6F9y'
        b'Nj1jnjnix78t8GjYOfDmfe76Sb+clhkYjsnCmYeMzHZzjQFii93QRSEOqR3dwEOrQ7WwGau4nZaFbLjnt3ZuHhXTJ003FpjTM4kujSc8wBWswwhY+2KAllLX55LwxwJo'
        b'e3WOXRmnB+1vWRdYIUcnONfiS0gPcO7oEgNIACIfbQoMexQsw1Z0zAHPqDYS1qREj+PAGljnE4E2pdC1rxvEUoD2iTaET/bzFnRbdFCej7ZHQhuGxwgQgYXtKzRzRRI5'
        b'wAv4NKWUJG0oYgXoecGbhPcBuU+0VTbYMEyAHvok38uNcI4oUGIKHzaPERInj0wkQdVSeYgmISHfXsfaJB8gB2DC69LS8J8nLAH2TQl4NmohasCy+RbYtHhsFKrlgTiV'
        b'gWdEq2ipy5MGgDG4qqal66eYU9KFqnxntjNlmC38sCJrbYDleIlwgM1meEezEOKqFqMGLElO4zKYaejMICGE/QxqdOs0yC2Ow9oIqg5PINbG5dOIbkIdN9CWMCLlw5ow'
        b'd6ynFNMd6g8LJQB3VQ7myma+E7AZfAZo3G1iwkipdBmIOjHiRm5WlnJ84fzXxr02/w3GQnQSTJ6PpqNL8JAJc5hkkDx7Lu3318snATMeTFnxGiMKHSwMJsl3OsBSdEis'
        b'Yrxpz4o/c4LOvnY6sGJ1o2x2cWpUqT2eslgTzmSwwOdeYIL+/ZjcQJpYUPAec5kDcffWNmW/P+PT2TRRlDOP2cGC2HuL/5WdBoZYhKUy+TFRGOzueely0rhDwslu22PM'
        b'4Af8HbteZHpf/9kImjiycBHTyoK4+Yn5Hiu8QoXWvZc2MSEciLqX9UHp+xOV6TSxaPYycB1DS2zQK+YAs0pME6NThjFJLJhwL/gLzZ60+wJVWuYxGMwmw9www5qW5yXk'
        b'HBqZxDSTEYnSrHsyqkQ00eDpz4TjxIzhG0q5OHvryumvM80cKLwXsrZg37p+QmJ4/rOgmgHy9gij4nDxLCHRkF8KfiYNmTf6x3pHC4lzpnwErjMgpLl0Y3HtdHvOGdGe'
        b'AENOyOurNfrz/vacrXOLQBletcIZcWa/pySTdQtG3WRMLTil8tq9xQteMrwd63P2qfz/0kxBvt7B/1CGvzxkcFPWLxleDH9tlMdLb8bVT2z5fvuM71c2pQza+p/pVtVr'
        b'C04FVVSEL31n/Yb/nDoVdDG7n+xu8aXN76fOO/iXbYaPg8x1L8+cWZpSqrFcO+M3Rpb1Rl3B3UGVZ/r1X/ZiRuLNFwO+qje9VnXJbeRP3JDAUWOkx47+EL1kWPFzyxqH'
        b'v1gzcMQL+lpdfN5qrSbF7dKmndvL18A5a7weDElc8knzzu/6F7+b8ePg8wdm3mwJ8Nj24X/dv3dz+T+PLLvw1Nt+p+UZecULi8Iz7nSUzn7tq10D4eqgoF2iISsONi8c'
        b'4fGPou/a/ySZ+PVWcfmK29uLXt779cVffd585rN/hKyL/Ou1PxoeJPy4yOx9qbl4+aE+awuvLf5YXDnLL+3z4AR94WDvH3y2/BCQ8oPff/1wYPz6T4c/9VPy4B/HnD/w'
        b'/P1Tsv8p+J/tVt+vdL+UjZp88qOtJ87HT/38qd2bP0Mf1y35ueKvA1/7x9S/fDHZ3XQ7/7nA0pdLB+xIPHKkf/q5A5b4syUfDErp95/T5sh/jmpWJsdFT/p84zPXFrUp'
        b'50z7l9Vzft6WvRviFVLBEnJdDOuc1oQ58JgQHXsO3qLenilxk8JgC0b3SABY2MLMR6dLqZmBg82oksTCbp+TqAxViYBMzKI749ERWmseah9LGJSdOaEDsIUwKHhdMIHM'
        b'g0/DQ5h4pMTDMzyAl+aL9exQzLGPCvt/20ZNCVsLT0YoEsLsx/95ozKuQAqrhOfbZeh4WEp4bGY380vCAGowEk+BWzo9nE6iQ65eTpacJ9zgU/g8ucPDY4uRUgfXpCzX'
        b'6spyA2UMz/p7+bjzjOtxTOQ7GH8H4I8vM5wRs4OwlOlFo5P8GJ7zZfxJ7G73T2faLyzL/iLmxJSRS6k/vwzXyJPdggEPZ+uCYCqiAQYdEruW2SGiqqMLP//fR2hh4beB'
        b'3NNIhkanGFCHL/16iAF/CXUVA4i6MwIdRi2PlAMoXxMBLPtfg2Xwphu6PXk13WgMhHeCCUyZ0alOQ2+nwSQSXhZh7ngR7RFM2ycUCWRzLm+g3URDXGB9UCUXXATvUgIZ'
        b'HEqlCamHNCN8bWqSQDX/PUJEBYTI5IykmDERQuJNg5iIEhnjwzNkuvmTgO7jl8+KTIfxk/IPyoPqp3rBKNncv4zMf+vyn19tHy8tGjVuybGIJd6vR7Ncm+Yr/0KRqvql'
        b'H4b/669/HbXhW0NswI+VFz/d7Lni3PUvq1Z8v+65vI9/POSdlSLa+9wca9nf/rrsgO+OaPjOsWk3/L4v6TNqyL4vDss3BIte/PLL7xsWvbxkyuJR1esqvI90vLX0wLaF'
        b'z7S8vnFQ/ZpPMo6/c/uXP97cOenWd4v4/rm7Bn8/OLJE7KaQCIH/u6bFOg6T7TxIFp0aaT9LdhMqFzbc2j1iyQxnaTvNk16wjZohs+DdAJcVWoQOqIjLZBLZDDzEF8Aj'
        b'/ejmG2ocOIlkg8dXO9YS0wjfUA6Ld9X9Be+nS+g2vEEzXYDNnQvoBc9xs9GpQZRKYYowBtZFBi1SqpSoNkkhBt6DuHQsXZ0QjKKX4A0lrEuxSz+zlzpPpxoIt2L1UeXv'
        b'0Bv9/89JxGMTEAfGUgIS6kpA/IgjFcuMnCujKM6ScEVWCNkRU5JhJKdh2bV3cjKXou//635vcaIzafrXbpbQ8nGuyEwovQrtQdVOZGaRDe0D3uO47HXoSq+b0OTPJGM6'
        b'vZE0zHJOwy7nNdxykYZfLsb/EvwvzQHL3fC3+w5uB68RNQiHeZHdf14j1khoLIyHVqaRatwqgMZd49HALvfEv2X0tyf97YV/e9Hf3vS3N/7tQ3/3ob99cI3UJIrr9NX0'
        b'rZAu7+NsjXG25qfpR1vzxc+k5KPxbyCHe5Hj7fprAuizvr08C9QMoM/87L8HagbhFvrZfwVpgvEvfw1PI3kGd3glCUQ8WW1Q52iNn0q6m1WJ6a9rHjl15OiS6VEldCZi'
        b'46OGVk2xQZ2vI+bWYrlaoyGGQKM2v2CN1sWu2LVyXAhnIqZ8u91SMBo67ZG0RIR8vl6rNmnlhgIzsbWqzTSzxUQOGu9iQjSRLHKtgRgYNfLMYrk9yjPCbhVWZ5l1a9Rm'
        b'UnFhgYEaibWkRYO+uKtlcbFJMDbjptRGF/sotSKvVRfT1DVaoy5bh1PJIM1aPGhcp1adlfsQ0699FuytRtDJNBvVBlO2lliqNWqzmnRSr8vXmYUJxcPsOkBDdoExnx6q'
        b'J1+bq8vK7W7qthh0uHLcE51GazDrsovtM4V5e5eKHgTlms2FpkmRkepCXcTqggKDzhSh0UbaD+x+MNLxOBsvZqY6K69nnoisHJ2KHA5QiCFmbYFR83Dj0ARADZK8ECbm'
        b'iEsrZald9OHmIY7CMf+gsqfV2aAz69R6XYkWr2kPgDSYzGpDVvd9AfJnt3w7eiwYv/EPXY4Bz9+M+fHORz0t3Y9xkKRYOMod7UV7hzwkAmZcqWtAGbyFjluIJyy8Ag+R'
        b'DbzOjeaQuPCICLSFnkN7G1WOg7vF62N9FAw94BU1I9sccmpvCjqIapUkHqMhhQG+8ACHNg016A6kZHAmEhW9686bJPQs5LNv8PWVg+H+32TE2SMpIpaEqBPU7KXA/lFr'
        b'oyI1K+9dbGrZfqNcUXel/Eb56Dpl5Y3dbeUjDk2tHLJnU0wQ2PxUn0PS97H6QHzxShdJXEUqyq3h02l2hj0G7qIM2w9exhoFYcZXvbrxYrg7nWYZi7ZP9MAjVjhFB3gS'
        b'bu4Hbby0ENUIB6FewfN5LAw1xo1JR7t5wKFbjAGdQ8cFRWYLPDGCzgS8Cw8rIxh6xhXcpI2hikwMalqN6hKVkikpgJwpnBgNqwU36xq4vw+tFJUvjx7LAUkJg/YljqSV'
        b'zgtA1+j4qpOTxCAfXsHSH4NuTIG1j3RpcxXy03UYTNPTu7sFko9MRgMkiCBe0r8r/EY4ygk8uk3wazbuBOCRgQ9trJCt04F5N75sZh12vTLnB/i5Ovw9rAcPD80ioqsV'
        b'rHYEZymI77Fjt6qNETrQNUzLaMKXrbgrNEKrR5OOGK4HgQ/dBMONcJqCrCfplDTdrrIY9z+kRzscPXrg57IR5thPi3isxnIdjRE6q9OYHtrYbmdj4aQxhxDXy75bll6H'
        b'6bfShMm44vE6kSN0wiNdu65QZ6Qs4qH92OfsxzDSj84ShAd1n/iuzTvoOj2+j9J1+7GkNpELXf8dZv8up7y4UlSCOSno+rCFqGEZusATggDgFrQNnaRmRFQxYxo8jbtY'
        b'6omOgFJ4boFFEPK3wRuoLt4kpeJ7DI/pQh2bsA6d0A3VvsHRPWyPQ01BdS953pPL+LWeE3PlDcdFfsNXR523rqz6ZozX+aCGNeF7zbf1g+ZP8Nz+7/hQ5fp913e1fbas'
        b'XFw/4Ne0byTP7f/vvuUJ049MyNu3cuyd8MF/e7HhzWk+/oGc5p8Kd6oclcCjI13opBme6KLYoKvoGKU3a+BhtCkRng1dHxIvGP7RLRbWJMM9VHfKQw3rE8Ph+QTXbYHR'
        b'WkGv2oQaWax8iaYKDgAqBrZHwQrBYeUibIPV1CBzB1522TGIR43ClkILJoNn4W60v5PaCaRu3SDBZfpqkCERNYYtiyRvleDHMZgVXR0u7Lgd81aGKWFFtOv51PBqLH0Y'
        b'A3etTEQNQ2lkmvPgQd1M2mraYE9UFzcKHYdn4wjhJkTbF57mUJXEo8tZZo9JZrWGLGNxoZmSWVK/C5kdIqPuHe7UK5IeE9uD1NlLu8aQPN5ZhfZDYjtp7TF8OdgLrf3z'
        b'b9Naewf+n0hP2b1KT7Ny1YYcreBL4ZB3HEjfTZbCItHjilEG7drHlZ56Pz6Rx/SLOq1MQGeDKUtXToRtXWWblbBFVxAzkzUtw/m+OfAXz5fvMLFRAfzrt6w/vrfseXnI'
        b'12Paomct8jt5z/2lE7cf1ARehH/4Ykp1jPaDfn7f+3xxNMj6r4M1b4yaIveXBYxWV64888uq/tUX3G4f/Pe74le+fs275ZpfvShC4UahPzgDPk1FBD4fNgtyB2xMpzC8'
        b'CjWrYR1A51JIOCw8FR7CAC/UwGnXw6NCxEN9XyykkZP744g10uIK5rBlJZVsUBvGmOOwLhLLhww8oAV8JAMvoacj6QmFQRPchUNVE1NgAzlJ+EqnRBiFmsUTsaTUahbe'
        b'PADb4Rkq5oC0LCrmKFGb0ERDiinRgWRUMqrFCL9phZSi6aJJsJYO0C4A8dPRPrgZbRWox7FBGEW70AV4JwDdQGfRtSdHU+8sCnTpDgjp7r9MPtHu1C7px5QEd0OSboXt'
        b'1os9D0VO414nVpIgydZesLKjC1Y+okEF1yHOLTCZdZoONwz7ZgPh8x1igd/3iF/qirm8I9LAibk8dYN6eNwSR9k5/+lMppu+Tv5maDRE5yHY5iI0CLqik2U/FGWFQQgI'
        b'G4fv42c7ED9TbcjribZOTLePWSg5X/iJC4ckWgxY01TGz+7FN8jFz8hRkujVpFgXvyJFb/01as0Wo8E0SZ6xyGjRZhD3IOEwBU24PGOuWm8S0tR6nKgpxjIMEaUM5seg'
        b'PO49KA+n0r1RtUZkIodEvb5pwf2Mp+69/sz7z7z9zMWmG7taylvKJ9Zd2Hsh/ciuC1Wj69qqWrYMObCp5pkdQ5qGVKtHz4ra05gRx1yc8BZ4YZXn3FOq+ScUHMUgs8wP'
        b'1nUjEOgAPK9FZYAy71B3REI1z6AmSgIE/E/ZILzhYctG2JSIDoxOioc1KcmoNikCNkZSr1AFrBdhLD7DPDkaeqk1mnRtpi7LRIVVioU+XbFwFsHBkqBuCNG1nF01EQvc'
        b'7yS5tJJLW1fG6fpyAt4lW6EzL0XR0/hypRcUfbULiv52j/6fIeG83pAwlVq1MB4aBMAjXm8u2Ohiz/r/Hz6SYvELU+SCJcosGK6o0pCtM6j1co1Wr+3pqvf4mPjLe0kC'
        b'JkbHSh6BiZNPPgwXV4AX1nvqy+sxJtJT9Y6bZwqoCC8tc2XXOesoI5ShJqzxN+XZebGAiOPgZvrul0UR6HpYAmpADZGJsMEFFeFRFmPjdNgo8R0Htz05MvYRjKOPwMdU'
        b'io/dBLOIHkXtPPFMN7wznnWi2Xl8ebYXNHu6C5o9sqFHvKOFsQGXd7T89tnadn/fB5m9IBiFNooJBkt+JkYqDGAuVuRO22yWxWjEhF9f7KJP/17Y27O3kqOvH3r33kjy'
        b'Gpj2phYKdaN/i/7vW9nJAXIqPVr/E2On/0XwIioXwM4y1BXqxsFKKrgNgacGOUAuQy5Ifw0Scwgl/2hPNJb/ItFuEqnWlQWEijHU3ZDILeh6t/fw9ApmWQUWg9llBU29'
        b'gdlyaW9g1qOoyuGqWPhQUi+YHSjIXcCXt3oBufNevwVyPRr9PwY5YlM2PBTkOl2XHxvc5CGhRB7TGeRrxkWMCe2F9D4e+B0+t56n4AfrRncDv1mWRwsgMSDH5nEq/jAG'
        b'P6qCXMLQt7WnBHISntaiHcME/aACHsESiACDA1GFQPlGwbNmEgvWN3ae8Nq4ruCXBK9hCJwAbWJ4KRSdfwwQ9CFT+igIzBSO8+oGDN1L2uncxYcD3WV8+WMvQHeyC9A9'
        b'qh1F/+5BzpL0dE1BVnp6B59uMeo7PMk13bE/0uHhDEzRaYz7SCHy3gxjM7kcAXZTbIe00FhQqDWaizukDrsm9XvokNhthx3uLvY7YlGgCgwVkSgBpyhFhyhYLH7HuRwu'
        b'xsCt+JJPpmouIGHXvAfPuHxYKePnyZJT4X8Rcw/55n09cC6ZjPHxIv9eUhpEiEXaO5Gd8cvoSjJWY7ESyoIQuIkcnHJ1I4DtPXZUCJrHAvtxG103c4X3KHX0tcd+2BeP'
        b'nk78QD5nHTlMkdgvs0hgh9FA5DEX+UuFtcSui2m84pyIbvbRO/jyOeuMROeF8zI2hMG9nVHoqN0xMseuRYK7BJ3JgVs4YJlD0GqrHB3p1U3ZxUn5esBv+CmjBm0Pqufh'
        b'oBlEOrI7+IOur83sPN/197xGhzTS0wYrUykEh8tnde6A8KZ29ST9ngFXhHfl7h8uBoOAvJCNBbIPAh4MjAB64sMzInSq6JuAGzm/zhmouJE3P/3U4Na8m2mbQ/apnp8w'
        b'ZllD+MGUs5OPT1oV9Fbokcz/hD9I3uj55UDP0tuL20MqZo1N+EpVPOPTYPEA90Efps1c/vm0WyMPpE5fVBO0I/T24BUzI+NT173nfaHgL2M6uK2hb1r3Z2gnJOS94vaX'
        b'+Klhnv1z04yisqFfzl7j/q1pTWFI/w/mnPII9Ly58VesF9xL/iOg5uGkVLgd1cXDu7ldzMN6eJiOtH694A0c5X9gSliqTnDVqcLzQs/mDW5csXHyfCHxs+D+IBwAn6hp'
        b'Ie7BY0cCGsqFdsNNw1BdsjKCvA/VcfDZ2oloS6IEbYVtxahmDtwpGgFgxUg31OKHLtO6/jBNcBCK8h8b+b56mdDAj/MFX+OokTlKDyZJOLo0KOMF7StZFGOYqe/qjK/2'
        b'400kAKBo1rQRDbc8udGyWYqX/lnkP2HgspGTNaIhyTdnJdyqGaj1WP/Wi9fnPjtMlNoG/fveGjtte7ztp+bDaSHzX3q9cN7RhKv7xoQeS4STD2zx/qbj6/uv7Rz+9a75'
        b'H1wvPHr6uX98P+Y/MyRJXusiXy14L/czjxVVf5p6tGb9H1+5WbXo54RB39W/lPLse4NPN47cdmmvgqdStQke3ZiIGqzOV+1SKzBbKDgOtWfBmz09h+BOWC24Dg2fRCMj'
        b'5ej4oDAlecMnzrdFBDzQzVRUwWJMuoWlemJBCgbpYag21G88sXGR4LWJqz17epj/3jNlXePvjSZ1F2szcRdyYWBmnvrjkWOcpawPIyf0E98b7zqqIW+3Jrv8LnLT7+1W'
        b'G2N8xkmzSAPf98LxdshdXWuITJA1YWNYqArWSwwuUsFAeJCHp1EjrOhBcroexdOD5DiP4vld5Kb3LR93B7kpHO8hT+XILrZc/77q8GBKbhojBU/ze4EBsg/Sfgh6USA3'
        b'c8On/Da5ibsXvGJtguXmpBOLZ8/517K/Dfx1wCvjB5QUh6kXSCV5fv8V9FcWTZWN8ZtwfXTlmBdK1yRPGLExpO/kkMXrpl/l032PF54fnJn+R91lydDFxx6b3LRqnnan'
        b'Q3l/Kaf6N0djzmWhbgvsEQDrfSNeBuT03oyVG6O8hB05+gSsFqV5k5CB2Izw/+o7TEj8frokrU0IUddvWDsACMfFn0O7iN9AfHgIJmgulMwQobu78DxDXz/1SctG5R8u'
        b'kDPi+Hsnn7p4oE/F5Q9eDGuPanptsfstX9Z6tX28bqqn6PqQZ+6e/CMz47t/HH35/clTxk44vM60vvipZvO/wqt2Ve1ZOCtH81b+4r+1F/x7zeTwfV8GLE3z107NH/xj'
        b'xXt5f7vxyYVfmLEpQXtHrVYw1LblQ14inBifPA+LAQLyr2K1E5d3ERZ/95k7FBM12k5MHN4VEzcCCdlc9xNkGIqNMoqbRuSs6N7v6AF0ohyyY0h3lNvsepIOPexpOToN'
        b'6ynSoYOoLCU+2YF1GTxsQTfRlh5hf+Sfnhe6BKNjtUg4+9zKNAOCbC1sKUvvOQ2P7zkzQ57PBk3MKq+VbClfSk5IF1UDM0tO7jcWlnhZRc2cRtTClIqWAkMwOZ88z92o'
        b'F16JQ5+R1+WIhPPIDfes5LUsUbQOUv6ilTPW41yiFuHVOGL6foEBuCVxqaSasUrIKeoaSQPObxVPAUU7DBtoWVE5ef0JZ3yRnOaP+y/C/RTRU9tJWWmPslJc9nXDTFpW'
        b'eBlNVI+Sgx5Wsokpcq8WC7lxCrCStwaECKfG2180M98KNG6BmL5YhR17dxUmxVpt4VwjiSJa9EBkMWcrJxiJvQeD6LNkickDIznBx0h4ukJizCGg56Y1WPK1RvJOASI0'
        b'd4jJKeEabYdssUFHbqhIKpSdKUBY57mVndXSU9tptNMSciGn7XYwq58wsLxDRt7iYYoWwm59OXvoJznXXGZ/vYDwRgvybgp3+/ss/F3uZPZvKX1nhZShp4TAqhh0SXiB'
        b't0o3LpTE/VNne3kwjy7ACs8e3gjOI7sJKliBSaphFgLybiI6/Sw9459EldJpNE5yDIGc5Wt6iL7oSQeWbi5I1xcYcmI4x5srOaKX0BNclvWD24VOYp0UE74mOT3xsIaI'
        b'WGAkrBQVG717vEXG6bE1hvZUw+QxRhnRLTSclbwDiNHwzYC8VQb3W+QPWhgr0x8Q3kZSKAcT20dBnSfYEeuEwwl4YTiikmydXq9gOxhDB5P7sKGREZGR0SFOIkNzty8a'
        b'PVxfeKuiBW4iO3p0POQlzzVwy+qCFOGt6mBksKh4QPEj4n+ZXuN/f8e77hjXql3iMV3i29yLwCcgrcS7MGPuu8PUQuKHUc9hICg0u8VmKD70n2F3ge9HhNkyfw/Mw/w1'
        b'K4Bu3a+RDH3PREzB9fsZq+jxTlfK28qv7H2jcsi7p3a1VLWUD9l/J+50uYXJ8pzl/vnME6p3Z24aUCVK8gisFcmPBIUHvTJW9mq9Isk31vcIG3Ll5PPS6BGVy2QhV8sm'
        b'VmqHZNFY4UkosPHXSCyWUqeGS6jWRGKFuRn0LHMSKnwriZpDJkjTOl/0Fgs3edAXvXnB84K7xHUvdIIeEFKThLaEMwC1hXjA0yw6l5RCeV6geSA8nUDUxAJYjmqwNLqB'
        b'HcplPXmccZ/8As3E8cILE9I1uhydufsZu/ZTn6QUhwnuDmCMbzorqX6c5moczdGCszhHA2Uun7td4ofJuaqwDp5ILpyMB9mQAi+MoWcOk3fVkHef2qdlAjwp3gDL4N2H'
        b'kwoi+woEgnC1FuFdJKyqQ6Q2Zel0WLh9ATjY7bCuUyPJ1a7T67KLk0l/qc8EJ5Cta3p0GtXBO/AiPRaNhH2e5rG6UMliJntt0MP7QkgzeR8I5Xd+5B06pEel9v5RwwOr'
        b'Mr4FqNA9x9Gv3zqoy81isPcytZN0EfGDyuB6fkAYaqC+Ac5u9l3EwdNidNCCap9o0pxdM779sAlzyxw3Rnjr0zKXKSPCY9qMuYnRMfFO9cx7CAevw8bJsLXv/8VsGd99'
        b'rLnC3RNY6FPd5oqi3Im56BrpJDG7UO9RdI6Du9NHz0BP9/BLc77PjESzahhMzomsBIwhZkLsuXIWyw+glBPecWRlMWlni6RWtjDaypD3DVEYFKk6hkeNjo4ZM3bc+AkT'
        b'Z8ycNXvO3Hlx8QmJScmqlPkLUhcuWrxkadqy5ZT6fUM4kSAdMFgQ0K3BaKvgO8TCjkWHKCtXbTR1iMlJFjHjBJ7v1n30MeOExdGS0dO39XKC+Y0wbrpM8MhsfWL0uMTO'
        b'derPjVJNgsdQ28OXSWaHFQ1j5794Uf7oaBsTpI96hZSYccJSFLhACqEJ7JqNpAedi3CM06HtUahO8fBDFul7nRnne51xbx55sGKvxwz2fCMIr6LHn3no4a2FsGFANo1m'
        b'RjsXJ7stQFdgeyq+XEn1hI0sCEHX+Xy0eaqOHXyVMxFBbLns9fsZaZjPqJks9/CKz2c+nyF+TQZGfcSPW3xfwdLdQiOWeDaFKTGt3xKPGlEdVjndYljYAhsUAh/Yh6nM'
        b'3TCXQMXCuTRUEZ3KetibmXWmgnSzLl9rMqvzhQMk6CtoXIl5ifEzZ6FK8DBbOs1k7pVYN3Z5OTOBTazV1/iTs7MaqRCB+zoJHlRGxKN6JQAjjaKN8Ix2bg/Ps652Rs7u'
        b'eeZiZcTL6vEEvp49RAoaKt1jWfsIvp7y4Vj8xDy2EdXzhfAaEA9g3ZcIIdt9EvqXrMLAglXgKZWTMoX3N8Pd06bERMML0VEFyAaGAomKgfvhwXB6fl/i7Fn42dVoeEWL'
        b'jvL4IdzNwKtzUb2FnBRWhKrhJrSdRvejA2hXBKxA5bQl28TA1WYmgxwFsfLjuDWC9KKVhPi9yTWTxJmfz54JBP/TY97wmv38u2x0cLLbIpp3uFG6iOfkJG/S7WiRUMHu'
        b'gSL2DEv1etl7uXoMJ3TE6GxOemI8PBMungQvAn4QAy8WwDJaQt0vNuNdoqgVZhhlRfZAwhN508DfuZ8BiMrw/XPQOiHxf4ol0Wc54bS72eo1QDdjV6DI9DF+cgSVzZl/'
        b'IYGfIUuOvhRzq+jK0309whLv3rvbPv+Z6Bc/hf6nd2oGSIYsDdkAm1///vC+Pzdu/yF40+7d/TP//a77h+VjnxfvPBH2eSDf/8NLld+8mxb7dd3V9q8urPUcEbfyxXf0'
        b'Z5/bWDpS539m0YWyEZ/XzuSSJ6PNnzcsmFE58cDK+J/eeCd4pcdQa/uDt72n/Dynz8ef37s7YdWwM8c/if/o22KvyoSQN+bHT/p0wCvLXnu6iDufrDu21HZgcNG3Tz3Y'
        b'Nkbn8/E9/4R3W4urDxW2fXAt/cNnhkx9ZvtXGydt+Zv0/tqbHw0O3zRL+5FVIaaiVxgqQ/sFAtVvo93asARVUHwWoaNo81Potus7fIlcNwTtEmIBdv9/7X0JeBRVtnBt'
        b'Xb2k01kJSQgh7GRjEZR9ETAsgYCCIKA0SaoTknTSobrD2nHDsbtZAooCKirgBiqigiKrM1WuI09nRke0dVZ1FLfRmdFx4oz+55xb1emQhMF5879/vv975KO6btWtu99z'
        b'z37Glpu20N1LjEDBm/Wj9LEX9s6z6PwAzkn9VE1MOXeU9jjxJ6uaxYRE7bZ2Ngxkv6Ad1E+Q87WUJVWlZPEs1PI2bd9E+7gf4JL838C2TGyEU8jjBgg06pKhwwj2jDkX'
        b'9lwr8Yx5CeeO6ORzAK2UBYnvg+CEotJl0jMWClF9z6zAcO8RdVT51EqPmyLttfE2/xWf8YL6PsfFOwLBulZ3Cu42tONu4lmWd5mrcHpRASlZF2lHtftg7o4MHT5U4vrx'
        b'kna7tk97gPmsDGs3587jtEP5HNeb662f1B+vNA0J8V87/aHlHCI8GFgxAvQTRsMLI61oCUpqUdAC/yU4Zy2ZXDrk6g55gsJunhR1DZF0WFRE87v1IoudC7lEtSIs7Ybn'
        b'QXGPACUz+lIq60C0xqI8IuZFoU/TGUkahAK7U+A9I/DpTR0CnxLO0cU5gsj83SIXF6s1r8LrA3qDKfZ0Fq+VoTpi1NLU2OhR1Wk49RLRvHJUCnhWBwCFwCL8NWs9Ubvf'
        b'g/pGAQxEuqpGCSxXMZRfVFQ8HYOxQhM/wvsPY4vWGd+W20VTWVS0GUwLic/9XhLRy18TKsvqJxbpD5ZiKGmMkrKnBKkRdLM4G8iRXvo9kn54qba9A8IYG1qcY0QYCbHl'
        b'ALHNJBYbxjSGOd+Ngw1nlCLiYBMDTlArYJ4FRYIcYlDEaNAY8LJZxPmkEhbDU4rJjO8htziPU1iINbmsddC4qyeurvcOLpxIyF9NQ/X4JX0GXjNoyVK4Fubj/eCCiVdP'
        b'nECI9FlsLONEPc8RYYdUSFT2e8rVyuVRS7Xqa2qMWpANBD9e3yqYmxdpd0ZFqCVqbUQ9LbUhaoGxhA9sZqXnw8uT0dcifO02M98X43aKkul3gEJXMrAhGeThtpn6feTF'
        b'EOBfWN+sReYwvBWxj1JrpbaVG5Uvazu0J/Vb2iEe7WSPt9F8AFoupHOIpjPiQg2grYvaD6+7+T2cf3BQUACND3JutIIR1Al4pTdTg4D4u+H/VO6a1GYiWKA0sTvMDM+t'
        b'mE65vbHcLSx3Q3aQV1voXfjcd4YEQyqL8o5WIS+PpgPGj1bsl7QRAuU1XtgcksfrqYdp8Kz0eM+z/6LORtUTQBNNHOVDbYPrNMLOJvPMWQMKk9J55jU7sqyocNDM4nzt'
        b'gEKEo7aJjTLP9db2WgaNreraPhrDMreJ1AEwcYtFj0QxAGFoF1tuE2vlWutiGzyzKDI9s3qstXbFaqYAC7QCUEPraNtih9IH4wlCOkFx3mRfnKD0NdKJigvSTiPeoERx'
        b'CJOUZPgmsd2zFCUVnrliTyQlTUmHJ0ntcnVTMuBZMllFc4tTlH4hEUgKtHu2L05V+lMqV+kFqTRlAHwjQwvylN6QTqe4E90I/xwYTbgMZsXTEJgMtFi7dWfyBeeZILaN'
        b'0U5hbDlFMu9pBQCByDfT7J/9Hv618mMA20chzn4jXtzlsWmO20xu2pwURdvfWF7peSlGYAlrc+KaNvjcjJ1SeNRWpB+Q/IaVajJQ+DJYayKPUDZQXt2Z+VfU3ugtr2lw'
        b'w+vTcU3oFt+EWI4OdQtm3akcszvzucy9aNjc7ReiFjeeBLQnOjVAwx3zeht9uTY5vm78tMP0xKp10vTgdo+FhdvPq1YM+ybwndf0VlsvO9A5MXawNzbtBPB5xgImmcN0'
        b'lLawmLJBURHqBHWEghwEYRzGi4XdUyf7MxRLUMRfAPk8SlPgiZV9lcGZeRUeoysbE2Ura+WHRPmCVmHwEJgyYiLjTlV5nDx+XatlXUFzfz8etSwstwPoRjXgX1UDxyge'
        b'u6al0vWccchH+cauGM5uADRwEnvI3fu7oql4ZVhEYdSdbCGVX5vVbhnGf1PWzg+mGD9yueYipJELMKa/QHGkYdOYUW1FNQX7ZfE3AdqAGEODYmoQYgeijthy70IgoKbB'
        b'9x+ZyAo2vf2ywRL/PY1UU7GlViyw3OtV0/ku8acMePVpuyalndskKKFTWEOtQkvxMCylsIT4RpgWdi0swc0CtZE324hBsoMMOxRguUctDf768kZobmasuTLz529ErIxa'
        b'PawdF6SFrGZBCV+IhjEpx6KX82tT4/vCiu96gIeyrgixrgixrgjxXcHhhs4IJpewO09naFxHatDnUCDfWByT8JLNX6A+tdoDcn7dviep5/SEld9hUmI8JowMEoaWhkXo'
        b'SYEJE9Q8REVYkOtm6A0ihLiTA4KxlERjZ6OKQys/iSEHkpqEHUOpIetdgtsNSFVNwFPvdpunxSzun7toVHvC13+PSYoI4UK0a233dlu2rfCuZ2pp/KIbfL7+sblqKIjN'
        b'a4kxr3AU0ryKxrxKZl6DhSeVqTm8ia92Z5NHA4F1x801jIbfbLA54TEnkBc24b14REZNXpoxLi7BQVb17ccmVtU/CTdqbrT5rJrOjlCb213h83nd7kSp7QRNb18dy0Do'
        b'+vx2s2GSHRSnHZmJFLOcq0Jkl0d0dhecMzuEFnM1lcDQfM3F0MU1AJhrGgLRJMTMFU+lt5ypiqL5ecDHBMHm2YCfqX1wvEn4fA6zV1Y9GNknRYotKycvfC/B//Y7hmUr'
        b'6bQTtKTyYp1QaNkowmaJaCKeqSiYWJNUOWxEAxrSsTBBUbtndaW3yV+z0hNNxHPNDSQm1ur/MzYyDzrY4B/fpw+JWgGy9SW4DKeSF44Js4sDsXeD8PLnjl1U+8OLblIc'
        b'PBC+l4X2Bwe2qR00wKGIkSGvwqWGQxkCkv+ADSxlHaODRIL1DwT8HhRy81nc1UKzpVkOWoJCnQykPe4VSxZGExL8V7D7ah5/xxlvAGbICNpXOIMyew53XK2EmhZQUy6U'
        b'Z222Qc1y0Aq1WYM2HNqgtTsHOVdCTmuzPWhXnw7y/n1B1NOww3txHNcgBe2Is/i1oODXFGp9LXxbYzIYmAAbt2irpS/iW/n2qBP2BpCSNV4FpjtqDfjcSk1lgBQY6HyA'
        b'EyYAa6siaseMuJH8hGcy8sfCE7OHzh5Hpa/Bz0zxoryCIhAoNMpXqhIWI1QqzMMbIckfcl0ersWQOxunjsIEkjd/B/mhZZ75HXwq7XKZFHwc5MtfOucANjpBbhEQL6a9'
        b'mC+UlOTzJfkZ5+oDU2+Omr1RvzPbR9glktpIQTMMAXEROv1paOjUIQhN4EjNw0s/3lh+1JG4YFgXzPiLi42FbXkeoT9qVttEmyTwDgl9fDkkIMBFlzNZSpbS5XQ51Zru'
        b'sEkuyWUhxSMgvu/VN/sxQOlm7TFt32x9c+GKmUVlFi5rklSi3zhwfj5P2trdA+MLZ2pP63fFbJx0CnOJH+TL3EWKPF+7Mw8ys4i0V48q1Q5rh6lczMJzCdcK+iPas9r9'
        b'HaRBCDVIlckVgxJB3gBuzF9FfXmdx8BX1F6dwCmrMaej24AttUOLLNGf8Gu3j49rh0O7R9A3DtC3dSpEwn9+jAwdI4OTKUgh6pcD0QvkpQQELM9cgS1mEe2FKtEgeGV0'
        b'CAZ5rIpTSYRfm+JSkm5Ch2JM6JkSdU5tqq9fYzS3c5w5Jp1kVAycv3wcqcm3kZqM5QBXkdgPEp2tN6HX9e8582zFk4sIBjgscXcRFcqW74c0cm7E4Bti2BTtQJk9O5dU'
        b'QuOES9tApcznwv+13eJ79MO8wjB3JOpovotD1A7ICmvKtNjE8msz2lUYy9I1vmaIOQkTiQ8UbqJXsztZUQwNQ4Dmds+MqzzznN7GMnVd/QSaSoUHstCJimWEOgLIV/uF'
        b'aSCQNl9Pks7dAvIC1YtwIuMafFNMLyqH4cI0kTRqhDPl8ueVnhPcmd2GAdmIJecihlxn/blgFIjkxRfF6upsBq1ut9fT4HYviBvC9HOqpAxdsxGwMwGumlsfBxAkPGG6'
        b'wrvwndu9KK7GDkuUclxgD0u67B2B8avPUw9D8LDJjnOPEtxL6licvfGxo2ECXibFzgc6C84zraMg0wRzWm2iQ7aJTjHZDsBfJEFH9hLthD8fwbV2QH/IF4iDgbnaUUnf'
        b'MWJ21yAQNapNEHibWCvWSostHqYihnw+ySPVWgF1M1IkwkfwaFtsY5w5AIkMRNqJw+ZgHI1o6pyKWk9lgDziGeP0AxlI6EdJlbuAGATTqmIzIq7t3rG+H8Y+oups52Me'
        b'1bWdORcMgm4yQZA6ju+IkuKK8MUtq9xOOnE+yGMza0X0YG1qgDOIMEJJF0KvJCBK6xzqJUy9l6CQGCTZxHpB5haxHBbIoRoKwPxumUhABXJZ28jAPTzLbfaMpQyBPkGt'
        b'GJEHSE2qudCjjhlALqxmSrAEy3AjRF2XEvrYFDDUY9sI4wsBcKhfafCsBNJqTScQl3Ge4TPIyoRz9+alMaTVGkP4Lm6/VduQtQ7NasPJsJxlsQ0ah405RSYGeVy7Rz+k'
        b'H5qjb5g5ezAqxm2cNbuyz4q4jTpZe8jaV3tUf7jrnZodt1MJNSGBIqArhnOCaA+z/yZkmoLuO2f5fHVNje0kmhZj/aTFNp9xaoVhPo3dABA/OwacLAydlwJrGj3q3Xhr'
        b'jzHpOj1VZS/Ver0U44jZ+LV9ztO+weyDTmzzpsW24zm7Zyq8aDZ3D4BCDKKo35Krb4sbaO2RNmi4QtuntegtM4oG60+jKq2+ZXAxzM3tKxz6nfp+Zwf5U4xNgvJxOMs5'
        b'Ynzk0B7jGRkYRIkejJ5aFEZCkAvLSOGGObq3ELW7nNEbJKMTr5o9C9YRUqfRBF/bYiXi/IfGEZsO3Y9IMTUx5tWKRKDkkOtWfVe+tlF/XH+K54ZzvP4Epz9Zpe/usLxk'
        b'c3ktjVteSptwRq6ykFjIvlgk5R8ZAD6KhGxwGEgkBBIVq2JDHFmxKw7AgeU4UZBtsZWOBRvBCVfUacz8bMDz1bKSDn46YmO+m0M9oBoYS4XfJQJ5bbKp+gEizNegOh+Q'
        b'0MSOR9RZUMMx1tSEoGC8ASwriwP0WUJSOCj6G/CO0lIWlI7EN/SFMbqEoDAVhekW+M5i5iFCXDWZlrVCFTxv4XlT4CAjn7gE1ycxsi7BC6FJbc+YYDDqcBOf1o1cZAKP'
        b'iBbkGx5TKGM34oI1qp6qmtVu1BEkS4Go0OC/MO4XFrhTMo1fAALB3z9kCy4L9PQskcdnlJQnG/HtYmIemos2fD5+G1i5ONWHh3FK8EiA5VAt4YAhH4QHjA21KGHwbmZc'
        b'EBR4+y8hzohEPI2cgBCUUCjOZImKdTMO9QKTR7JbUmxw5KymL3AR0YTAhpPXw0RTCTPhuQMA1FbMw94Yz2nbobXJeoE9WZETZPAwoSxqmYdykqh4WYMSlcowgrZlQbm3'
        b'qaMYLYYUMDEacnAUoU42lBCZooOgzsF5ujwGFPnOdDjJo+JRlNCTY8vi9mNc6WtY6VEDxIrwx+tUMHeXUCTxPNs4poVE0CGnC2O3eQz2i58C0DGGDB6eADoIPot+z4qo'
        b'xacqHhU5ev4mb4Aw6Po2Nsv5hPyu9u07IJlGjbzpn9QhOHhBQGNv+TuX6BBy0JjKgcHMz9PPDpK2GLMQTWaqcevh6rmkWQT0gpRjyFapCNcXcZ/FPWy2bUERjimrakNl'
        b'C3xKzwTjuEIMHhmKgPR5YL5t7iovKjo00JiZLML5OLJoSKUu/CeoxmJ4f7qNlmLeWVNJ4+ncnWNU1OkBQqsKFfDjLLbgGsR+ZKIgh6h+2FN7UB8Z3jGuOrwN0J0Id9MD'
        b'AIyCQgYcOzfypIoAQGsPT8gc7BTYFwpy9hqSzSeYB+WMioXdwRMY0wzOUDhhckXB7aY11ppxZUNdg29VQ17sSM/r09/fp1Ve19+PYkdZLcABc9HSY3BMLcUnl3IG3mby'
        b'FGiVze6IPkcT3Q2ouoMumqGAX+KwZsQtrGSDWZ/By0Iyvza7/fDGf9oBOuEYE0tpGRcv1qN1g4czHtMCu6sBbIEp5xh2Zwh98AuyhgvKQYnAfUFAYnKcWjgKqqCUewQE'
        b'+uZRLqtu3lge6lV4oV1IMgwgSdHbOWCa1jgei83kpKqDMWlnvFPoS9ym7JztuQzyv9eG7cIYicjcZKPVAXwbVYtlsA3snVKhV8UaTl1Y1h6/vSD0ow3nnQlf32aKC2xS'
        b'RrfkXkCSuphmSlg/pj/FeI2za9ahVfcTs/VN6K0st7ukHU+e3Kn7bPxHoVtjaEgS0Zsm+sH82pvIB745F/FArNhAO0jzBBlzjLxPjtpm+SrrSmq8njIVUd52qEc7+f9M'
        b'jjEnGRnlTw8ICk87jxGLAr0jGV8G8uRgTcHVQpw5mbh0VjQgc9tiSkKtaRiYNk/xeQyP9OgkrNXa3z8Ytdpwtq7nSNzpx3y0raLW8go/StujNtJ8U2rUqBU1xn1NgajF'
        b'XU9xVyjebdTqxhweJV4JICphDrWmE5oTV8JXbYvKSfhBKuEIMr82xRykzvl7CNUc5jhhXBamComMLTSNW5scxt0GUAhh80Ku4WrDvnQtD/CJ59YCalZrARguquNuxK9k'
        b'ddZCICX3DiBGGCuLr5PUZQGrIuCYwzObYpR2MYdQDk3TFnErXEB8SmzE50FKMe01zqYQSKv0NXkVGuzySvKHn4eD9OGdd+C//RPn59uBmIHhpCGKWurrYIDV5SRUmjOP'
        b'qNKoxaOqAHq8+NB5RVMDZjfe+L0eT6MB9KJWOG1YUV3u5KiEtX8vmXqrvAvO0GTayAIZY+IsoKnw2sTY+OMXXRt0FHGMY6IOUGhVwprkzZFXB8AsSOYsGKsQD0cLdYYt'
        b'EEuNP9Zli1qP98RmOZeOa2rAhiRb4pjBGDZkbVKsoSzHP0OpGKoY47QAprOuK2YwetbxACjLsLRxRpLj1iW97HpoCuLqw4VpcF8Fxn0lJjoMjWH6S2xGSV2Nbak1B0et'
        b'izXtXJsYtxsgLvIUsywxSamNEGuYvNS4RhrZOujv4v+FnIGm0wxmmDwvHB6mvIhyRL5NqwlWWh3NU6XXBzggDpyp3CG5PasrO2GNAoiBvZsXP22Oc/c3y4OEPsLDLs4M'
        b'GhmaqiBemmmMLoRpiT3/0iRPbZLL4UpxIuPSSvKa0hH6M+gRaI7espIFsp5bzyXWig7tlHZLh8PBavySbWiMBYJ61RJQnzE2CCovLpaU5BAL5SKG5JCtSib2pB0OiRRG'
        b'r1IwFpTa2OHAYM7CUHbTnlJNjUolc6eWdAB+MXQDjWECnIEokKQb6UJz6uAX2hUWaiW0G6a0RRECMksZh4TpBaM1Ye4arOyivJX9/a2JkDAiWkPS5KYxd1Ho5LKxvNoT'
        b'dfo9AXej6lOaKgHVd+LX7gWXXTFvxpyyaAK+I+eoAKoS3G4j6LPbzXSw3Rg1xETYYsbo55tJrLuwbbmnkh4qgIBErLZzurErRqvBam9NmQctyasvbyBnkegEBSFCpG1h'
        b'M3cm52KR2LNYHy6KgQdhbSo1pd3rsnYNQo5XzHtJOG7ucOOh8+ygwHg6tYK6NAzEKt6htjYQmyIQqHDYr2e63XTfLAIKL3bnUIeYnsLxv1tmGg6EdPLqjWFAHxXLemFL'
        b'MqCd0m5rUDCPscu5K7irOINwkZl55J9xmzr695932dxL8/6M3WVKfqtVT5WD8PSosKrCWA5RGdCAxqYAjVjUojTVN/qZLSpqA5LkL2pZhZJ5g3PHwBqNKX0iVC2/cPtj'
        b'dQt8conFVEkm+2IZVWvo4EolnhOQgAk0B6xhUft0j3elJ1BTWa6iVIzZR+IkVJr8JvyXFD8rCH6DhAIA+s7TvCB6TurJMOaisatojOkeSCJA2UV8E+YDFiAOLekcKmqi'
        b'UwiW7sHSNkVutivWZgdjHTQnwHwnkELnn5pR4cKZxTUnBu3qc2a+YCLMJjIldir25sSGXEo7IP20kgBvzbptWPeKxvZtCTqDgIJmcnWc+i6WrTi7c1lc46+hJFfQtZVX'
        b'xymJQVedFe+CLlYP3OcGnXDFsq0GBIEyFVfQimUqYrMdWuFiraAv4T0qUrM68T0qdijWoCWYGHQAOmCvxWtCrVNJ2SxDeQ61EXNBa2UG4crOog3FWZyD+Wdxxj8MZbz9'
        b'6l/nfTWxhBgereL48eNp4qKiG6AHP5+Ri3xelJ8ctU7xNak1AHz4GflC1NLgWeVezX7W5CcyFXgHKat6axo8fgaU6svV6poGfzQNE+VNAR8BM3cFwKq6qA0fVvkaAL1V'
        b'fU0NCpMK3ISrVar0eL1R6aq5Pn9UmnVZyfyotIjuyy67an5+ElvhJOSWqACJLE4s/sAaQI8TsAHu5Z6a6uVQNGuNAzO4vdAcj3EPRC1UYVE90IqoXMFYKPaGpno3fcGU'
        b'aiW8h6ee1QF6/E+DKScwVUlSgZ6KG6iMNpDNCLnoIhxQIt4CI4Qlg09HllforkPIIX6dTF+wTYfbTebk79EiC070ZNp2cRV1ym6hM0vl2u8wkvTkkDQaCZ2ZihDh0Iwo'
        b'IBIhheepDVkz6w0PGFlofcErcpDPYIqBkmJFmBawGPxROUYwi8QlZWepvTV7crmKhsR5w31Vo/NQvSuPnBn4m+pVB8xwa+GFGFkXD87rN6SwfweUKqagheCJTKJczdAL'
        b'xgowjKGqTZbdJK7NHGp4J+QRItaofN1mB9WLBhibP3x0Z2ZQZ9H6uFUq6O8voH1TBpT0B5zBmUPrGoUUtaMi9DbqolVeA5R6pc/rUw1ozgo3CTgSSLWdzPEuknj117GW'
        b'/hg+9VpMBhV6NiITPZQCGLDYKJYw3G0kdzZBsXob3yXGt5E3QL76DG9UE8cl+IEuktr4BTdAOQMtMX5BstUmZbrSBzWhueY12mbtlD+hcYXICfqdvL5LP9rbrT2L6mkx'
        b'FID0tsSysjJU2BKbkMzrNX/MPO5S7VFmtndK24Ivyfz1V1kiLv2h4+VlRXwfHwxcSU1dzmmLfwMgcfK6yOz5f1uYVp1+98vKHf0+/TY3fcX+hEeu3zBswJP27GTxs5o5'
        b'Zz65al5dfemB+oGfJb08+o8fWL+z/n3Oyd+8uCqa69pxx18/f+ePnNs31d4vsD1z+R073+hbMbPuucMLwlnX9Ln52OzTtbfvfH10xVJf6tjD0z99o1vFjs9Tjn814Ylp'
        b'H0ZOHpvy6evvPHftr/JcHw1bMfdgWugvuSuuOhLuu7hPy8eLb1s9OnrPrYvW/PSvwzYd0b62/ebBby654eUFb31RkTRv0OETD/7mi7+N25zw9eiUde9vfmlq+m/7VC0u'
        b'f923pceS999Lrfrs25tatg0f2H9/yYyrX+hW1zPvk9TPrJtObKh74U1bRa/rtr5dfPLJfoVXKLMWFTw58Mr9L1/+RuSTZ37+04uO7Tg98YGNj1rfn39/xgMr0o48erDw'
        b'64p7J2x7r2Vzr/Kb7aNb1J36if1TF1z7yrbDpx9f33/Rtt5ZO8RX73peyFjSO6PpwazDr29PW7wgf2a5/ZW/FH9iaZ38q4Prqic01H3T+3frbu39UNEWZUnuK9fe9hPH'
        b'gqPPT1j92Z5RPzux4LM5m5/tduDUzMZDdQ/x31Vcvf2WM8qlrcr1aTveLv3RmpVv//mbv7376YleqxrPzHqxuP97y1554/hLz4w70rTwTc+m01NeXZX0yaeNJ+/47U2L'
        b'dL05fUnuhoGRqklL5KToiQdOTn/oLy+deOfLocd//UHznwb9bs87P9v5XtPjJVsqP3tp8Kr5JR/sen3629fctbH46JJfjvq2r/eZnF+9OXFQycG73lLfzK0rfqXfgXfe'
        b'WvFmeYG2b/9LRWM/7b/5xbeeOjZ9yXdX1tYmzclZ97PohCcednyRfmX1vYe/Lnz/8/d+/PaYA589+d4Efc+hVZlj77mv6vDpMVmvFF70te3FBu1nBcFb7r52w2vekYs+'
        b'nvj0hqVbn7/u4mO9Xzv6/Wtf/ujoFX2rh4/86O1t1Y/+rf8p9cwrxzff/r79M/d7Pc6UPrv5m7tS7nv0q+JTYz88Mq3y3jNl0/Ne+b458XLbby1D/jF5xyc3nPT++KF+'
        b'fU6M++odS/GuB765503uN/e29gr+5o2ixscW7nvn4JDyQ60Prlv5pbh0+Jm6R7J/s0Z9csZrW1ZPea3Hrx6tHrF8wNnXFl3XcvRabUnrr58sWz5meeDvB8ep62vunlD6'
        b'fM/Zr715ybZ/6N99O/onA25fvLXm4fer//77lRV/rHxo1uKeV276/OVvug18tHHvkY8Xzbvhl9taak49OeXrv/b49S1fvhp4ddw1r9619+kPldtfH//+C097ttz5j55/'
        b'fDl48JGvdr3y/PdHxjz/7LwvXCe9n/TNv/SJd7tx+QkU9k3bpu0bjQ4yZ2ibhkwvwnjyqdrN4tX6zdrhkssoJpK2qWoYOVwtKy5Am+unBP1Ig7a9j3YDRaCjsNFt4Z7b'
        b'Qj0fcWiPA2R4mIyz5+lPDmZMyUHave31H2fNYr4cDg6vZUJTO1oOFwtckvasuLin+1r9UADdcs1cOg2aQGaMhlQZ71GmrLUwh1NMqhwc46iYIum7fAF0LjVRu1Xb7W8T'
        b'RM+YXVqkb9bC2s78FR0E0teVOjhRuzlQSO3R79HWn6M4oD/u7aA5AJTCxZj/Ae14N/9gCgG4pamtwg6VrNLvtGfpT2lPa3sUcsA5EwZ7vdHE8frxDixbVTvG3CUd1u/1'
        b'tIFq7b7q3tpdaYCE/aBj4byX/JH/xsL+f7nk92YH93/6xWRAeX3lihHsEHEcrlzmZUHmf8DfH6SeLrsL1ZtF9j/VDgixVeDTU+E+TeAHzRX47AwUdPcp7Dc2p4fLkjlJ'
        b'EgQ+k7/EK/ADmiCXTSJBeL9kvObRNacXXlMtdIXSMu14lyziNd1y7r3TZj7B/31yMJXhpPcuukKZA3xORNu/lyAHtjezt8DnQs5Mq5N3Ulm5VMeAJXjNHoHXgjL1JzE5'
        b'2Y/+d9F3cWnDy3G0lnEmtrt3dbyzBzxDLrpqoraROf2bM0uLaFusnHZXT1eW2FPbpD9b8+Prr5b8A2A5Oq89Xnzryw3vDE2+ecaM7Sde/PbztyLbRm3c4Z15LLfVefLr'
        b'+cn5BRt3jJg2OhT98WtHv0r5/ciP9mz5hfXjcKL0xbej7stKtDd3m1ny97nLJ/cfeWvGrNCiqmOnhdcrXXdkVW07O9w3+5trhtYN+Pv2Pw09sOUXP039/PLJ3/z24Ume'
        b'I4t++kiOZcDcv82Z3O3jG5uX37j56oS0fhUffPdNff7Ss8P0m8be+buCHS/MH/Zf+/faF/z6vV5X7v3ton23pj5RWnpo07grP3ZcuXT0luvuvajW1/e6mXd9deYX76dl'
        b'fbljeW3xK0+/ePrnP/rVh2smLsvY95O6W1pWF//87v+6ffSOQy/03F99QFupnSxcceWZ6TPL72tqaXn04rfKDlz89jWnXz3w1FuuR5/623MtD9/5Qem0NWOzmhZOeCqt'
        b'uu+bDb9/ePHCrXUffv7zOzz3PnbHV6t3h+af+Xb+G33HbD/7co8vr9qy/+GkfXuTzpZ89+xm+zWLci9/5U87X9g+cMShXVec+dNtraergg++ll9Zt+TT7u+f/PqOA+Pv'
        b'ObPxD+OO+up/sv2Dq8cu/bg0tXVDzrcNA0+9OfLwQV/NY1M+/qL59H1jf3nN0Wd3vThk5s/e/fq4u/rW06/cdffWG//25jNjZ6QNX7PmobVz/rjq3cg/1n/sH/eV5y+3'
        b'DO6d97sff/D9S1PkCYJyy5RcS/rlL+QW7Nt785js5Xt/dMmYj/aGJsiZFb36blpx/ZRZjTdV7lq2Yd6u3+V031neYtn+zHPdHluxfslNz6x7ZqF48btVZ679vW/1T6vd'
        b'kdf6HPmH9Y3oW5+viORPoADyxdoO7WZjWW3SNxaxdaXfobe4rhCH2fwUWGGydrIa85hoAGXZPi1FOyFq25arhL5kNgNWgZEXKeoinOo3UOTFCu32AFKuS/MXFmqPDdVO'
        b'FAHFqd/AL1Ny6VDWdurh/MJSDAhVgB6Q9C0UgW1Tqb7RyvWeZ0mdOJ7lO9io7U0o0A5oJ871oM28Z6/mCb2pWKXtLi3QN+ub8jFToczpB+uSRop12sEgix23Pd+ubxwy'
        b'Xd8scrnak9J0Xjs0cjC18aoJ5aXQhv3aqUECJzTwE1awsHVaZLX2cCF65J6jH9YiFk6eJLi0o9pBcsQzPHgZoW2Digdqt/CcvFoYpt2v30iDUqgfzCzFt/kzAMvQWxba'
        b'tGcFLaRtXBBAd0wT9YP6M4AV2hYCTS4E+Yn6Xu1+5qHnAcAYH9Qe0Tcs1bfiS+0QP1/f56KXDkgYDqMAxdotkccobcMy6l9DUD+Grva2wlAdgA+b+ZJG7TFqaTf9Fou+'
        b'cQ7OzWAeitzAT9P3609T5Av9qTr9fqgvrG/OL5iuby/VnkiECgAdQwSs/wjLVH0PtA1XQ/VcbX8CIKmlxY5B2i6rvkE7iMEys7WTknanMoeWlf6Yfv0EXjtGrrhgcNAD'
        b'Vykgot2XSxdpe7XD1J5xgLYeRK8lD10xE9uzky/RHtMO0dAsLtSPFOrhKdrdQ6zwah+/UHtkNHVwhH5okb5xhr5XfwrnULiOn7TUjEHYskR/rJQAJMxWvswlaDcI+i7A'
        b'Wx/QQ0b85KHLpmgb58wpnoETOtvCeZypY0Xtkf7aFkKgtV36zRWlLIbpnDIqpETf4rpWnJquPULe1/UHRknLtL3Qbpnj53H6ffoBmZbJNdpJDNvMHKTp67XjFJu0GNB2'
        b'8te0vJ++UdvPnFd4ekgVvHZKPz5qceqwtSNKi/Nnzvb1h4U1T8jI9VI7a3wpbB3PwKWToO0UirRD+r5Z2rM0wFpLnn4nTGabFqjE6ffqe1K19aJ+fR+BNkM3baNYOqNo'
        b'RrHRqG7asy59g1imn9IjbJmd0tfrO0opoOlqrUWSeO1e/bi2k2iWofoR/XrWn9mAM+fPgBp2yan6NlE7lpzFyJpnoB2FM7QDg/KHzIRlqt2hbUvS7xO16/Wt2pNGQOqT'
        b'aaWF02eI3CKflM1re1Zox6nuyfqOufpG3PRAyYyYJV3Oa8dhpp6grxJE7bZS7ZbCmRaOL+X0ndoT2oM0P5USYO4bp+OqQleSMDJBQTs6iCb5CK2cIYv0PbDlKIZjzwop'
        b'mdfuXDKE3gzrObYUyKGLh/PcVP1pq36rIC+y0WDL9sJ2jiG1E9lJvcWx+iYbdXM0LLV2Thn1bdoxdMw4TLtDv5eGOuPySaXkN9hw5AYAa45L2y1O0a9PZTviPm3P0vY+'
        b'MNFVp7azh34MoO8zjMg7pD94VQdfmUs8afNF/W4AytcH0PK8Jrs7wpRiPTykAKYH9uitkN4qzp5Fo7KptFh7WOJma49Y9Rv0G2HX0oK526Ef0R7VTyQg+dmIBZTiykrX'
        b'd4n6g/wICsE5Stuj7UzQW4YUzyxrIqEl9BywjRnFOdodAnfxEnlGjpcFy3ykbDiBvcHTZwMwSdD3CvpDsJuPaC2Gz8BTy5LJdSweGbgTDwlA6N2vH+oN0AhncojeosHy'
        b'apmlbyktyi+GmZ42NS1XhKG9S98QIB2bIzBooVLcqzAkkRlFM4dAbTKX5i3iLDAaeyto0EZqt+pb12FcUTrFNs/JBxpP24yHVEZ/SawrYA2+27YY/QvPmUPHixVa9KRw'
        b'lazv03esodr0Z7TN62B9QItWkjng4xKA7llWLks/JC3SH4FlS0v+Jj2UBG3Sn8CyMMKLHqpJ0eEk3DNIu5PFGAo1XUHji2eYvkN7WirmtQM52maq55rezdjSIaXswLtC'
        b'34lnHra2Rz9JW6/d1od2QFMfW+mM2QWztWPVVk6WBJu2SaAG2LSH9NvJGy32sxiGVn9AgKV3RD82Qv/RBek4mf55R/4HUFP/cZeYQJgou4c5hEaCYOPP/XMIyRaJhBqZ'
        b'QBkJvMz+CxKPuV0sjyHqYPSeg+kACg7jDkoA7N5GZaeTsW/bn5NKpjzwxklmvzaSRjoFWVx9Hdfxr6/MM/Y201tATQ6/J9DU6Ha3uagzZQQaH99TvGFUx1/jPWrSu3aa'
        b'Cokceo5kegL+5+BawSl8LfxFFoQXoApZZCD8CvArwK8IvxnwK8HvleEFNRz8OsIL0Pwt0gvz12JOPsSHFphKb80cKrx5xXopklRvaebr5Wah3tqM8j+rYvfa6u3NEt07'
        b'vI76hGYL3Sd4nfWJzTLdO72u+qRmK0oXA8lQejf4TYHfNPhNhd9c+E2DX7TLleG3d5ALJ8FvUpBc4EQSgughnI8kQ750+E2F327w64LfDPjtj6rY8GsNSpE+ijXSXREj'
        b'mUpiJEtxRXooSZEcJTnSU0lptimpzXYlLZIdFBUunIXq3pG+SnokX+kWGaxkROYo3SOzlczIXCUrMk3JjsxQekQKlJxIkdIzUqjkRgYpvSIlSl7kIqV3ZIzSJzJB6RuZ'
        b'qPSLjFL6R0YoAyIXKwMj45VBkUlKfuQSpSAyTimMjFSKImOV4shoZXBkuDIkMkwZGilVhkWGKBdFZirDI/OUEZHpysWRy5RLIpcqIyPFyqjI5croyBXKmEhZ2LGei/RT'
        b'xkYmB7rDXYoyLjJLGR+ZokyIzFcmRoYqfGRq0Apv8sJC0Ba0V+EopYdcoe6hXqHZVZIySbkU5s8RdEScpJvS5j7VFUoKpYcyIGdmKCuUHeoRyoVveocGhgaHhoSGhi4N'
        b'XRYqCU0PzQyVhuaF5oeuhPXQW5kcK88WdoVt4fz1QsQeYoHBWblOKjk5lBJKDXUzSu8JZfcJ9Q8NCOWHCkJFoYtCw0MjQheHLgmNDI0KjQ6NCY0NjQuND00ITQxNCk0O'
        b'TYWaZ4RmheZAnYOVKbE6LVCnheqUoT5WE5Y/IFQIX0wLzahKUKbGcieGRPI8nwj5UkNpRmvyQv2gJQOhJVOghrLQ3Ko05TLzm+aEsCuYQDUMoG8ToJZEGs9MGKEc+Lov'
        b'fT8Ivi8MFYeGQXtLqJzLQ1dUZSklsdpFaKtIJUnXOnAem53h/mFnuCDsDDrDM9YL61F/AJ8U0ZMi9uRaZzCBlFWmMdf2pM7PdPIRSnStfoboBDMRCnN1djU7gI4wuFre'
        b'1N42vN20duvvH5SfV8M0QsvzKppqvIGahnxBbULoQ4I5JO26dOPkrmogJhtqmW2yGLasHEmI1edMQ5R8CQBdtSdQpaLxg82zupJ0Y8jeGuXevqqo09QPIr0gHh1y1ANk'
        b'hDsHen+ub1Q9fj+kRK+vGg1yUYGMQhycxS6fJcUObNdZlCCe3YUXzlSG9ikegK/kFwFVyKNio68x6oDSFU9VORon2KrcTKDKzP/a/CbEYHJUrqJyogmVPne5Wk3RIDGI'
        b'pbtula/Buyb2yAGPGlhhUSfc+wPlhutJG6SqvOXV/qgV7qgwO900+AN+ekuK71TDynK1LYHqtZii7+jGRU9VP2k1NPioHC9MYHkF+0D1eFaik29MoNICJSyVXk+5GpW9'
        b'5TDBw6JiRU01KY2jjxYW9yHqwBjB7J7p8bxoTHJALa/0YERBtxuyV7jZRFrhDrUQopJb9VRFXW6lxl9e4fW4K8srlzONYFgYCnMihqhrqzCovW9uU5cNiS/msElggWVQ'
        b'KwrdHaGHUpTxT0VpukB2n8J6oJdXZAdNVfjOVQD/qfsiXJx/iKmTGdiAky3adm1EvTHZbOMJeBu2AqRzwsbKwpYEeYBBQhWaSuQqFMqFDCjEcB7pcklBKeyos6k3hp3N'
        b'lqAQTqgT1OlwLzcMohSnLg07E7hmS5hjul9hRzgV3rig787uOBZy2ArpnuuFoBzuBjUKDfcHBfVWeJYbzqhCxy7bUYcL6kmDeh6j3JnwdQ6W1rAanvcKp1C+P4RTAO5Y'
        b'ycIss9kGOa3hdMgpwVkBY70eDVmeC0pwgvBUnlxn24pqvDJ8Zadye0Au0xGMA0owvgza4c6BdxT2BtLzONb/ME9lXAvfJoUTE0wbNzGcTG8TM9FrLZCHChdMwHdBAeBt'
        b'YneOGV+Rl007c4of042j8YQy74F5cISzoXYBxyVoSUfjk0w2DvD+aWpxd3Mkgu1cMeQ7/5tSkP/3TOkfxLfGVf1Fm+qPi2GrhK+i2o8s2Ei5JxX+kkUWiYep+7A4PDLg'
        b't5m8JLoEF+C6Ofid6KCoPS6h3WZJMc4f2iw/E4zN4oKpzjc2S3r8ZoG3Ik5eWIIzami77YOTVwjfSHSHC98SlPwfUYB0OYx/GTDpIqrZBa3qjUErWdLYglAbWzywXbLH'
        b'cQ1KuEe4b3gAbIKsKgt6J4LlO7fZEUYVNQeUmhB0hHvApnwTFl5SApeFB7MI9y68Dzpp20E5wQRAEZOMBUyKe+xd0EHxpRrC/cKJ4R4KH+4L/wfA/17hQVV8OAXrCffC'
        b'zZUOKCY8zw7z4eRwMqJmNVba3BZcxLCZUoI26E0iLHj4DcLWCLsyuWZXOBUQAnzi6s7BtkkkRCEBviqiiFQBKgHuq6DHLXyzpeFTeCKHC6DMpGBSOJPeA0CA1iaF8yiV'
        b'Z6T6UaqfkepPqf5GKpdSuUYq22wnpXpQqoeR6kupvkZqAKUGGKkcSuUYqT6U6mOkelKqp5HqTaneRqpXbNwwlUWpLExVJcHhUIzofZBrQbCJQAD6Gh4YToQeJweTtwr+'
        b'B4MSXa14pbXSHdcKlAFjX4VOr43edOfQxg/GMw3XGJQqknsCCUcegTc9LwxK+DwomQbpbQ6tU/6v7Nv8wf8BsON/Hj7lwynr39kGn1DJULAZnpxl0UWQKlUik2L8+1ay'
        b'4Vv0FYq+F1JlgYOnbf8FgUs17h3fSE40QUaXVE4hVXQAHHPxXf59IaU6xWQ+VbShnPU7yeIUkdZvB+lMWy2CdMxDI8AyIKPDNgPSyWEuDtKJYQsd74DAhO1AAACEY6rc'
        b'hl8i03V9Z+vhv+9vnwZ4h2ya6bMBFnFAOnTKbnZqH3ZKgi2DuIgAADqVdWQ96W0CXmCBTiajS0p6LgUpJ3QxMSzjWQ1DkQQgKxEBOKZQRz3s2DKAx1ITwqm4JXGwCJyJ'
        b'FgC3YftIQAnHxWmnA+gDIApgHjcm3ifDF6RpjQFz6FvuAgYw7X92JT8oG34UOVrDaKkkWR18jogWOtkiriZH+9XkiB94BZFMQAjDSYgAxwZeMgZ+EA18N0DLRH8RvcF0'
        b'BqbJCfxUWGFOtNeld44t2TR0aMtuzSQzAUy1G2RA6sLWLLRLleBEWRoU/RtMVJvH0iVAHPH8tahvYfxDhKZwclnglIFJbLaudSDTgSzt0iUuwNU51J8yRy4sfiN9k4kl'
        b'rLiNiHBXKBkI8PRQ9yqrEbHFFleLDaE7tCMjnIjPzK/ZuQfYhB12FWunBa+x0u3I8qAv58KX8Aze2GNfxtoACGq/mMOYTi1rYu5jY3EDkRqBDsMAU5AD9O+AQWbQraKv'
        b'CDHTOtkgqEtMzp4QqFDPIA35W/4HO9WIumr8bl9FlXuVihrV6p/kmNmLZLgdZBCTJzL9X4ppkfWfBPpfkA1bJnPDJMPVSYcAapujX0UZPdkIeBQ4RAdFAHHxst0pZlrx'
        b'aarVZTBvU/n8TMZ5WIelUzgI0b/Grz6Pz17Ay4t4eYmpPKMrGb/6Mun3r/XWVODKRbvV8sBy9RUylIYbTznGGlBPk81KjaL2o0KBKo+K5RVAzy8v96M5ddRq+EiKWv3m'
        b'TbXXV1Hu9ecn/nuGLH/hfwD3/X8v/4q4AtdkM5JgUVzngiCdK6pwWTJJpIDig46iDPYndfLn7PTpv/4nG/9jadkpplolcdbFuPeqavGa55TEoTl4N24K7kvBJhPxKAjU'
        b'zzK0h3mKoyAD7njOnttt7Mj68kbYlgFVDfPM1pbcBjDZyHO07y5bXelpRDfCKkrkUFJSWd7k97jd0XS329/USBxBZJ+htQk8TXC3JdRP23t/iDNKHVfvU5q8HvR9x0Ku'
        b'SgBYkgVAhjqT1wSNp30EcvFqagX+H/oMnmE='
    ))))
