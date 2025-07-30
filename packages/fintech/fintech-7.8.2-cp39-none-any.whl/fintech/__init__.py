
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
        b'eJzcfXdck0ne+NNSCKGIimDB6FoIJAFBUcF1sVODigWxQCABIhAgRYUNShFDVexdwQpWsHfXmd1b3d7uzuX27nW9vbst7l7Z3bs9b8tvZp4khKbu3vv+8yMfnjyZZ8r3'
        b'mfn2+c7MH6lufxL0H43+TRXooqVSKS2dSmuZJkbH6jgdXck006mCbCpVqGW13HpKI9IKtEL0LS7xNIvM4kqqkqapxZQhmqN0bsUlNJUqoamSQK1IJ0lz14rRVUruPcjV'
        b'UyepoBdTSyitKFWyVGKQ8N+hVChKSabcsuRuj4dKFuToZHOLzTkFBtlsvcGsy8yRFWoyczXZOomc/UyEAP1MjC8MunTQqkza5X1Y9C+yf5smoYuNyqK16I3Wi0vpaqqS'
        b'KmVKfKx0JYLZylRSNLWWXssku9wjSCgESbacVWe6dhSudCL6748r5khnJVNymbqD+ho/XpCHQQocJ6DQtyx9gS7v7VFTqb/wZf/2QivVK5SksikYSsZG2dgs1gkp/cyQ'
        b'ru8OqaOBrpByaksouk+B28CRZCXcARsXwGrFIlgN60LmxSyICYINsF4eA67BGljPUjMXCuFZuH6W/uO98xhTMCr540DTF2M16Z+n52U9Sg/UKbYEaWI0j9LfyBiQmZOV'
        b'x5yr8J+0lKrYLrLc5+SMeQQqAa8Vg9vuAamo6mBca6JFGQRrQxhqODjPwbMo13CUKx20geOgDlSxYBPcFI+ygQawSUR5+rABcPM8oxvKI2c7mEC5ESMrf8GJj72nZBkL'
        b'SnQGWRaPJVM7PDUmk85oTsuw6PPMegNGEJMQ94e/lPakjVJH0Va2g8uyGDI7RGlpRoshLa3DPS0tM0+nMVgK09LkrEtL+NJKGz3xvTu+4EoG44qH4oo/9WaENEMLyZX5'
        b'nmHQ4NDUj/iXZRR6bgDli+IVKrUyCNQkoY5Ig3Wom/k+VoQLYGsxuJWHQYph7tFvCKjAEYUv0f/xezPuAUUwanaOhbmy7DNvKr08I0C8fa4dox68QJ72f34l/QFDeYcG'
        b'6aO8MnV8kQgjQ+FhDx1XIP2nfDKf+D9LRRSC3Lspd4001TSTsihQopdY5w5aFAiaargpOXQ+jwyBKmUgrA4Jik0ER+bQ1LKl4oTx8IyctuAxBedH5LqrlfA4OBQUr5QE'
        b'wlpwFrRw1GBwkwN7wPGJlgA88jtBswmN6aYQ9Mr4W0S5JzEGI9wCK2CjBfccmxOKH3SOuCXXPua3POWsZSCu5QioSIn3G6mUxyUKKGEy4wtvxFtw348Ep1bEE4yNjVUy'
        b'lDvYxXDjYQtoW2IZiYE8C0+D9bAuCdbGJapgTQI4yaEmNlM+oJKFZXBPHmoBAxEGNi+Oj1XEKgl6ggpYKaA8YS2rloNyyyCUYQi4DWrR22zCuQQUx9HgICxfQF4yFGwG'
        b'N3nEToyFDfJYzqqkfOBWFlwD51JQfw1DmTLA9Zz4sHD0PB5uTIoVwE1wB+U1go0Cu2ElyoOhgBX+0ThPbCLJshg2IiDOsOPgBXhIzpBuDwXlYJN7DBqqQoxA8fitB8B9'
        b'8BBsZOExeDLGEohy5cKL8Io73BiijFNbcL5YlFADd4OrSQm4xISlwlhU6WH09hg2UAtuwcuwTqGGG2MVKiHqx/MMqIuC52FFOMkBT0ZBWzDcmICGSSFXxglMsJrqH8DC'
        b'rbBuOgFscg6sjU9SxgajwaiJVcSNmxuiikkUUgpKAHcjyK6QNwSnQSWNAQpGD1U05Q4PMbBCBy+DTXMtcpRhGLwSH08y4E6YGxiPOMVGWI+wcq5SSM3g4C3QKoRlPuss'
        b'z+HqKj3w8MKGSFiTlDAvMCYBblQnJC3EeRWRgllgW2AXjsi48u4jRCjYaMRyWRtnE9iENpFNbHOzSWzuNqnNw+Zp87J52/rZfGz9bQNsA22+tkE2P5u/bbBtiG2obZgt'
        b'wDbcJrONsI20PWcbZRttG2Mbawu0yW1BtmCbwqa0qWwhtlDbOFuYLdw23jbBFpE10c7WqWoOsXUasXWKsHWasHLEzJNd7u1sPac7W/ey852ubL1CbRmNB6qpZIgrm+F5'
        b'zNYUJ5uB58ANiwznLIcb4CZCm2qlXAmq4S14AhOoTzoLzuRNJmiPsPQoopO6WFiBKmMpZh0dDSuDyTPPKFgRDFoV8MyoGEQRYD0NK4PAIYsfAWP62mC5ATYqYTUiFyE4'
        b'wQSDCtBCCoKdWgkatBpFKtiGcICLpcFNM7hOnslXwdZ4RKjwBriKn7nR4ChsGkMqXTECXER8KQY2wasYGC6GBufhRaXFF1d6HWHrjmAV2A7PyRmKAZfo1NJ8/iUOwlNJ'
        b'8eAEbF2FKFxICfOYQHAp1OKPnvlo4dl4WIve8wTCs02oxedohKQnwvlK14PNHMZGeCE3mEaVbqQTTF6WARjQ5WaEp+vCEeIpaEoYwQwKSiJldLBpWXAcbFyKqDMJvXo0'
        b'46kDWwkf8/fshyszIFIKVKJCa5hxyVYC4kq4D9QhxgCug8ZABL2BnooIcjupEDaMAgfQe4MqOg7DsIuerYANliH40QXQGkDIRR4LbqUjyhaD2wyw+YBzfNHj4Gg6rEsE'
        b'l8AexOcZK/1CDtxPYIn0mAJOIqbdjgUAA87TCxbBU3x3lVMT4hWSOWpMeBwlHMxI4Bl4hh+6veDqIlgXA08j9eE0KlhKz4blFv7ZcRW8hHgt2A6OqjCgtfQcCth4aVG1'
        b'CNxEDAZXGayKRV2jFlCDYCVsyOHC4C7YTAYDbI0fFB+MJUmcJ0E3NyEDtvuCm5mMC/5jlO+qMyGNyUY7dSamGmlGpSwiLoYQF0sIilnLJrvc/zydiVXrvb9K50xTUUKR'
        b'YvQX6a9lfJpenf0p+ubeq4/e4xbzp6ZwWp8l83h5icI9pXzKjqr6eumw6H9nNUZe8tyQLnxLSr3/mec6wQ65yIwZVwA4BCpXwwpe8sGGJDlsiOXVHd/RHAtPgV1EJ4qN'
        b'BjtJnlq4v7tOtBReNmOSzw3n6wlRJMJ6yThY05ltOEbfzQifK0htoA3e8MNZkxDWgo2mKTiPBDai4UcYdsqMhdlUeCyRtLgeHkHZElSghjTIsiNAXaJ5CBEXWnABCdaK'
        b'YGUMkYZieIFBfPgW2EHUvTB4UkoAIvJijJBIDB6g0UGCpJU+dlWum3JFUolq1cHla0y5RGnD6ha1VkzzH09aQhv7O/LKuQ5WazJ3sCZjphFzRaM3TmU6q0T3mFaNAx01'
        b'k8LrKIfSVvkEpQ1zHGBbCvcg+lEMQNi7UUhxCsQc/OCxvnX4SB4fmSzmF2jwPVi9A917YOOZN68yJqzhcIs2fpG+7KV37jS+cv9O468uNG7ud9cz60ECSzW8Gj2Re7xt'
        b'GdKusbQYGgVq4hXgItgTGIN0EBpxipNMMdgFys1EGpwODOyqhoH94DqPaKAe7uM7nOl9tCxmfV6nir2OEnvTRl+qU8VmCzJW9j5ASKH2c44NLlKNq8F4SJVRjz37Hh08'
        b'rHMmmIKRwqY0wXrEt400uJ0a2mVkaPt/sgM2K0/ztJqH3t/5Hp0v42koSCvIyLKYMjVmfYGhHhcl3IexjEXXaWDzaMRvSU8lxQUr1WqsNdfnIjTZxFLB4LwA7gkFTc8A'
        b'RvYTwXBzwKBrdIGAKIknFuYgLsu3jRTcBkSAPrCSBTc9MvvGS8y5kKqD7Us2i/vfsC5pqjdOKeiaycGrhzthILzaxjlh+Dncugd9YBgkvdHHo9xvOFMCSvgtNeGkz6fp'
        b'j9Lvaj8d8VN6Krj/qt9b3m+8BOaCuZ+9dHfu6+h/9Lt3lsF33kh5fS58h9vWoI2ha3877pOiaTmsLIH+/GNES7OHeo1UDJHThEPOnD3TBE7HqJWBUngTDz4e+X5I/wZt'
        b'6yBCLp7zcN25WzeiEaRlavJ4qpHyVOPL0N6Iw4npksGmHH2WOU1nNBYYVVPyClBO01QVKeBgfJzGmG3qEOauxt8utNXDYmWMWH83BjipDOPQDhcqe+TTN5VFoBxeyCwv'
        b'Q6o/rE4IRjolsdzhFqR41SAhokaaB7gEt4K6RYhbzJ+MZMMLbvCyfol+1cV5jAlr9N9banOzc7LzstWZm86rNQmalR+36D5NP6H5ND0vS5L1II+mdG8KX49czb/aM3af'
        b'u0sXubKegd5Co8yZ1aO3LjH2c/YFzrnNpS++ekJf4LwmcDO2W1cwyDS8Ng7WcaDFIO6b/np4oJ6d8rJ6kwpMD6zn1Av0Aw6+w5qwt+HNlzriNVhFidFwW+rlsoj+u7Rf'
        b'pQ+rECPRIKKy7wvXvfKRnOOdMyeRaXt9VCnRC9QKpZqX1P3ABRZsBOfAMTP2ECD9YKMPEeoqZWBgnFIFNiZhhTk4FpwO5FWElDShWpzlA/eaMQRWZFDU8rpG12yD4XbO'
        b'IxJULAK1pH13pEu0kZrlhtK4BHViHDLiUMso66jnBMNyra544YIBHhZDZo5Gb9Bp03RrMl0JabiQ5j/GEY4iciSEUK5OQmm14xltHOnEBpz7gAs2fCLtGxuwEjdgHjwS'
        b'TOz5GMQE6uMTEU4gxiCkRpcIQN3UJHjMs8u4ORACK8sOZkhsz1/EkHswQ47qTVkQq/Pwy1XPE4u1symZbt2bxXmGR4NXZEek3Z5FfCiTYSVoDQbtcKsyFlHyRQpZ7Ido'
        b'cDFwOPFHqTVfe23zogP/Ftrh+WNK+PSJvB/p6hKaobi2WZJCTdrw0hA+MTvFhxpF+aFa06ccLTJS+n8dW8qYDOjJrfyX4zVaTYuuRfcovVBTrWzRfY54wOfphqyg+a2a'
        b'1JcawYXGfkG/Eg9wP6FhTmxp1Z3RnNL4ij5n3pOOTI+s+pCOGTR44D8+CB34d+qV3fNThvq1tdKvtXWEfxA2UEj/OuzeDmF4YRaii7Rhr4X/BnFqIiqrkE24Od7hckEq'
        b'TyMTCc8VgBPgRu8c5ql8h8vRmHIIssl4ZBuL9VIJ+fA6qpThaCl/RxtHdSIgz4c7OXXv7dN8NoKPuPAxF3z86AnciRjdVQqkqtXFKMCFxXAjQoaByHgeDq88xeNMd/M4'
        b'M7/cN447xq0HCkrVFsxyleNWw62o+RAK3J4eAm5YCcr8R86teciiHolOl9YnW3k8Kk5lxlxm8V269LmQVMqIuXtvlw46Ta9328WYatGPioxRyjfGeYJQ75nv7r64/+UB'
        b'H3zCfDBZMCimvCVnkbxiJq2PVs/KLJL859j9kR0PB0Y9/mvptrv+zy/aV/RCimKZdstvN7esLs94uazsw1PShEWtW2YlbqreW7zv89sDlq384MTr8/MifvfmmcHFFt2/'
        b'zl74PPzg/8z/couXze2NUTuWR6d/8mrbN7O/+0w0+eRz3v3EcnfC2grhDk13C2/7UoeRVwTPEE6JGOU5eMikkMthbUKQMpY4x0EZaECyJWipAHHn80N4860ZscpWeF4N'
        b'TpvtsscDliFjEW4bD1unkjzCfohl1/VwoIPrcHtAGrxkxryn/5p+wSpYDarMsAb7LsBGRmmAt8yYE87JmgLq1sXarcmetmS4xUwMo7ag4cFx2LmToB4aIkBMvJ2B+5eO'
        b'MhN34pU5WcjIVwTJVXCTAnH9C7CGovxk3ApQ5k1UqHHw9BBeNqAmsFgA+5bZLdFL3kOIvQLOh4Id8fA2PKToYrBcyzBjO8Fz/phgtTIWddoMuJWhpGJWDLdGdbH9nmBf'
        b'CgstGXl6XmgoeDqOZJDu5Y2oVkgPoDl05X7iGO5HjuV+4Djue6FAiChciml6jLOuQb024+8kYJzzqgsB33uCuYk7LhvcBEeDAxORtV+DTPLaBCEyrdsYhAt7wS3SZKbQ'
        b'hdp80L/YQW2BLLYrrLQ/VSqsFlmF1VQlUyqyikwJJZ5WtomyCpvpUvFiyuDDUWa6OIImbS+hDL6hSNG2inE5qxDXMIXS0rik8UeroHCRnioVWAVNTDM1k1q+axlT6lYq'
        b'wfVb3SoZYzppiUN3LVZhE9tM6mjiSF6/UvdqFuVztzJZrJ6ySo7QG2maKqo3zCSlpAg+abWbVVhJI4gl1WJ8V0mTkmJSUtyt5K+sUuOjailfwgErSn9clN7IGEaRWt0r'
        b'mUY0RNV0NbWKwncIHoGWaab53I204XuSjzYLsxiSd261uz3v3GoG1+3M+R7JKSS5VlUL7LnQXZdcp7Rsk0jLaQXrkfE6k6qkUT97aIVNIqtHk1gr0oqbGZxi9UBlT2jd'
        b'rB6+VKmHTWRzR+ogq5WgcmIri8uVeqI+8KykteJc3OJ9q6fWHY2Kp2GkM51D6f/USnGLVs9m2hc/5bQepZ5WppExRiN4aQIvYwzQelpRiUGIaWcxKJ+XQWalrUwui55F'
        b'aL3wvT1drPW28ncjXcqnavvx5Z15cGteVi+tz0T87YHyVFs9ydVL29/qafXA9eFnBk+rF35SuMXqgX+b+TH2Rm/hjd5iAHoLxviN1Ru/nXYg6lPG+DL/C5X5A7oTO9M/'
        b'4n/hdPSW/bS+6DelHVTF+FPWfgR+b9S6X7UHbmGlxOrtgMHKNrLGwWba6lVJV9AGsdmdv7Mr1P7qBY9FecjANyjHPWYUsi4SkrFLSWKuYz9DNiKs5ZJS2kqvpDYzRRxW'
        b'vuxKaYc4Lc2gydelpcmZDkYV2kGbu1vykil5epM5syC/cOp3OBEL35KhmTm6zFxku3Wad53ZHrOyAuNjWvEZhuqxpCBLZi4u1MlGm3qAKXBQv8wBpi+e3LZiIc6YuGoE'
        b'ciVtBzm7EzDEJoOI8Fz1BCZpxIzxewfEn+EmH3tpZKs0eRadDMEUONokJzL4sZ9JV2TRGTJ1Mr1Zly8brcePx442jX3cjyTgW2cSR679XXI6Sj92k+VbTGZZhk722Eun'
        b'N+fojOidUVeg62e84+gxPfYxPfKx22jTUpVKtRylY5X/cT+FLLvA7OilSPQvl3YI9Aatbk2HZBEGeBa2E1ESatXUwWUWFBZ3cLm6YmRBo5YLtLoOt4xis05jNGrQg5UF'
        b'ekOH0GgqzNObOzijrtBoxIZsh9sC1ACpSe7T4ZZZYDBj88PYwaKaOjiMBh1C0j2mDgGGxdQhNlky+DsBeYAT9GZNRp6ug9Z3sOhRh9DEZ6BzO8R6U5rZUogecmaT2djB'
        b'rcJXNt+UjYpjMDoERZYCs07u0auS+nMuSM9McmKo2IGMb2JU2kCQC+u0HI1lopQWslib5dBHjCQkr+lKaT9GQn77knSUn/GlfejBJMVbOADdC1GqL/HZIsnKYJkqRano'
        b'F4MlqSfD68g+jCfx7PrRA35CLf7EMANQKSRtGX7mcS/cBQ5hGysRblQr4kSwGeyjPNPYyfDojC7zAlgUCh0E8RBdkOhirFQTRcTRW0h0saWclTUNLpKakW6L//VI1O1j'
        b'sYCzMlZ2CiIc41wkDOlVFPpGYsOfamIQq2T9qWYkgJBQ4pAY4LDgMGmtXDaN6uNQ3XORAGOxUEGCcA8iPyweBFpcn0DLoTpY/At9I8GI6ynK4QWN8ZiWK2zRYjEtsIpI'
        b'W0L7cwHfOqmHmUKR35z9NzeFKpJaGaJ/C9SIgtV4JMlwzsUXtfMOp8kFxul4kFmTztzBarTaDqGlUKsx64wz8VNxhwjjX76msEOs1WVpLHlmhLY4SavPNBsTHRV2iHVr'
        b'CnWZZp3WOA+nYd+aXPgUTHPxquJADG2ao94AxMhMYwiicQhhMKJ588iAEEFIDCqMYN40/vjQZGZzvARusE/1g5oQ0KpACFGTAK4vVdFUMLgsgDvgkcge1ghuHc9ZkNZ6'
        b'zPVSeLY3y91h+lhph1HT3WJyqlladKnGI03XIHG/kir0RliGChrHI8zwQCk0FqKVtDsyfYiYQjiBhB9dzVa74/saHN/DIUBw8xIEjjRL7PSEulkZjEO9WVYYsXGfEkfq'
        b'NxgIzop1BqrkBGqYxfdEd1qAUJ5BjSHQKulcCoGF7qwIkFLW4EvAEyLkno3vUAqHkC3PypI032qs0yAywDpXtRAjvV3v8rXimqeWslZSL8pbWy1EyMoivYYzSPE9Sie/'
        b'rJyxEEsdRESkHitnr6MQaZ6hSPPkzIIspvghjbRKmioZgDpLgOUyCQVDaWsFBgn/jUPBEJkgErXSuA67xxzhHOYKHaJVGiNxgbLZCK8RdzXmrjZOw/gWx2Nmp9cTy3Ee'
        b'kbWEEHSInYufmVt24rA0jfDJQtRwvmmaE4MRtjKMN2GUiCEymBkOJuxTykgRZg9G+BtAl4RqMjN1hWZTp7zX6jILjBpzVw9vZwNIRmfgpvF7IBonYUckYSVOcP+lfJ/t'
        b'EOFuQ6TMV5npfD03J0CTaMfEG8uLgQDEjAf7lwzu+x0caoUGV5eH7yW/SChpnOCI7I1NoO2uBIqVPcfPErdOATXxCWq1MlDuBzcIKXcVA4+AAz49nKRu9m9TDLroqFSk'
        b'/qUy20S8xwOxAHGWgKe9SjqVJekk+s7OINwQZeJYR/yUs1EclSrgeW5HP3s04mx9ni6hQKPVGfueoMbMl3AdAYk1EWYJneTOPfPERw8XcO+TLyI1mSEauXitM4TmtABu'
        b'hI0s5QlOsN4J4ByJ/csCNR54EovE+3UG28Bqh5uiKhNcnE9RywJFcJsWXLeoUCGvVZ64DLwJb4TMCwyEtSExSlgLWhcExiUiM18Vq4xLpCmDl9vz4Bo8a8G0AbemJyYr'
        b'F8XAenlcYgLKCqtXgEs4VCcWZR0PdghHDYKN+gu7rghMmEo/Djj8Rfq9jBZdiyblpV3gSmN7yrH18qrWDdP2Ne9ur2mvbE1h72YL23P9IlNe96vNK7PuGCwc16ZWWd1M'
        b'ohkiU/j7zA7PHVX1d6T7/Kl/lPj89bpMLiDugsFgQxysw84MAZU6gAugwSGwQUccDbIoIXZWzCvm3RUOV8VssI/4cMC2KHAZnof1ShwKV0T8LmthLUMNtnBgA9j8PKl/'
        b'6ES4M1iljFEyFDgFbwrBESZU40FmVtf118er4hIVsaDB6QcSwJs6avQcQSpsn+aY8Xh2YeqRadQhAZ6WX6C15OmIEwObKdQ69MkmbgqGszsgS4b3QFVVl9LO+SSTLi8L'
        b'XTFj6PRRCvqmVcZYiO+LHFAZCzAW0g7HaBn6HPDt093xVLh6EJRzmi/OQVCuYpxG1CpxEpbglxOWgHKxqpyE5akmumjhPHAWUVYq3GUnGSdlhYMaQlngKDzpR+aHLyj7'
        b'pC4naRUaCGWBkyJ4AmU8oiZRl08ireng7JOnlrVdppaRgUpndTdIxVPyNPkZWs3UF2m7cWdZgIn1TDE8YHLCW+gMG8Qhg3BLPDgdkwg28ig8gkHvAbd3mQRkw3xMYOt8'
        b'H3gak8CGfqBsxiALcVuelqqJS7KRQaXrYZ3CHlIynx0Ht3WN2hZQLvPFhHXy2hKDx9rJOtlqNI6lHBphlowwR0aVXYvM3M77J81bO9U5V9YZxY/fVng2Hs/qqPip3eSY'
        b'YBwethBRv1IONybEhmoWOodSQIEmnQTeQl2xnTiuYwNQjakDsDdbkTTXRPHjuyUCbupSJx9fC6vts/iov2+E01T+Oje/hUWWMFykCl6A1+Lj8bxSbOK8QFizGJXBMY58'
        b'2xNUqPWFCI1guwiehZvBDn2laStjykdlv33zzZPGz0iI0r0slY9ck6DJy8rLeJSuMH6e/mbGaxlvZcRqtmjvZpzWfRr98Neh1MIoemF45QJb+Cf32kO3tS0cMy6sTDZ3'
        b'39HKWfvoUYPuNb6qpT743Z3Ge+/cuTH87vr2TeN2lYcPo7jR/jLfRXIRcRvHwR2DeLcz2ACP94hnSoeXid9Xn7/UzkozixzM1M5JQ2Ed4bfDwTHY2JNhUsnFmF+KwVUy'
        b'szNr/Dz73GLSWrG9IQ94jvWDZ2WkpclR4DqOpyPTj5dWw03BKrmQ8lnLwvoSsJ+EMQnBuWGOLHh2yB00RU5EiA2bBaSKkex0fp4fHoVXA7tO9C/K/vls2xPP36cVGpEF'
        b'j+0owrcHO/j2OkrMEMMa2UOMD3E0+9AlE3pySd0aXaadR3bqYV1r5klfwCt4nXrw06ae7DNUns4ChK2b0aUKs/WRDrZeRv3QN2O3LEO5xoJqb8RJ5OD4szCTnqwEh05v'
        b'mQzbBbPg1WhwcTRolVMj4fYBK2HZ2DwM6/lIf+4bHyq6cOTjsf9gLo3707IRFJmsPBa/i26b850E0V/YR0Yb9wc++V8hX3ttm3PZn5n7gP7RrzJ9CKX3+fKhwHQCPasZ'
        b'VD+wPorMGq3OG/vjkVlxkJ4kXP2AOpIyC4yuaXkonPOP9wo3zHzYNOmVmK+LBxdtnjrqQnl7ZuTbtdvnJvkXVO9XTfgCnv84a3TR6ueHlH936tLsjzw/MLzzMGNvzAfT'
        b'31109VTQh8alL/4EwsN+37LrPd+gtePzPjytaj4z8w8jFhrF7r4THk57L+budx/XHfmLOk/4n/5Fn8p3v5bTXvfxV3GHX5OYbzz+1svHS/llwA9yKT8NdBq0lWDsp+DV'
        b'7jGBoFZOcBe0F84NVoFqsNcxDeOcgmmFt3jFpswCr3RVbOCGxQ5yBA0eZuwjDAJ7kW5NSM0hGUA1Gjc0kJiLZ40TURFa4fJouI3MC3khK7ydKELw1HMMRfQguB/uJi1y'
        b'4Lik28gv6IcIb8gEDtTBG+AYCY0EN8EJGW7xRcRINvEYA2rxCw6E5Sy8MAHYzNgMgJvhpQiHTgds8AbR6mD5aDLHNSIZNAfHkLceBa5wE2lwBp6xhzjCk3AfILEJ6qHd'
        b'Qhx1oJUH4iJoAlU4CzhM5u+6ia0y2GTGQYVLEhGQdQngRgqigEkU6py9oPJJatMvM4uETibi7kL/hIMEOjiI2an5MRLsU0HE6Y3uOMbHS4iuA5CNWjLsifzErgsSxa5D'
        b'aE/r5BrPbDMj3XAVvi90MhELuhR10Q03B/StGz4ZSsRxiTdWkmZPSEtDpnlakUWTx3viiSZKmuzwwIt5NCZTpg7xxzT+/dx+Vue30h1u9kpQBeRlcDhDBn4ZLPDFDEP7'
        b'ShHfU2LE2gJuaftSoZBlcAQ2RQJkHOxGQvJwD2tVbP82YZ3BYa3qkAVqd1thTUiAdCBGy65362KTZrnYpHM1ZtRxBtRp6kzOpXaMQs6peWwPO/Vnoj2TuEA3u37FVYuR'
        b'fiVA+hVH9CsB0am4taitzvsn6Vc9NWihmuiCqId2+MfDZqQh1nXXoYfBS5YXUJ6C0FQkdwNjElVI8+G1nljlfKQsJQdir99Ccdd1LXQ8ouYjFBXW38sNNoHNcoYs/YHX'
        b'4TWLwwyeCW24ISTtYQ1HDZ7JxaTBKhKYLgDnwGmntXwc7sH5goNihNRgE7cwF+zVHxS2CUwrUNaSf9cPu6f0KZMNmP3uv9iWIcYRkZkXG6vv7mqr/nip8NGC8R8t9cwb'
        b'/XbDH3f4SZOPSBTC+sSQ1wYMupIwbcSsjZP9Q6oKNnxbYpz4WHH/pzMxx5aHPh9++pMX3/+a2fLGoNN/moYUKSx+Y1fAms65czvThofh3hUaUEFYzgKwfTXmsHBLltLO'
        b'YZfEEr7mjXjV3ni4dzVZGQRq+AU4PjoWnFoBdxGmGQY3IAO+zo6R8MRUSgyOMmsYDR8KVg6PeTtFAtgB67qoaKt0hMfD5mCkJteFgDM87yV8NxKuJ3y3OBrsCB4D6nnW'
        b'S/gu0gJuOrSln0d8rvGwWQin07B5Srier4PrraNGSqR4wl5Ki1kxM4AuGdKDEFTOsjwHEHawmXmmDnGWJY+wjA6uEOXtEJo1xmyd2YXjPUW3Q6xyLb7H8eTGMnwpd3K8'
        b'UnQ52E1t+uPQvnnek6CWM2q1nesZV+PLGtwj7oQp5evMOQVa0pyx2NFlTxBAxhIniFZ02e/wrmE+RhZgwd1ws3cnDxN3XWo2Tx4lE4LjYDs8T+ydEbksts69C5l0aX8v'
        b'LdXD/+70g+HZhq6rrbJEztVQ9DOvhurBbrrwNSe78VdbQtA9uAY2rzUhjL7gXmSBl5Dmchm2m1d5z4YX3VeBBq9CKWynqOfhMQFsgwdmWXBQXhJoyUIlahLUsCEY7AJb'
        b'1QuJFR+LvmqSlI6FsuA0rFaoQPt8vNYMXADXJPB2FNz61NW9LJn2//nhfj1mBKhe+ayA57Ng0wx4JRi0JDgHkqJyIvsvYNHvzfAMCWZVjknEnIC8pxpuDwatgTQ1GEf5'
        b'XCgygiu++u1//oQzYcd58oF/fJH+2l8+T099qa2xeWtrZevd1spxdUV048XGfndF7bujEg/vmu+XvMs3rPKTKL/X/OoeRfr5tpUtCA0zhwrCj4Ry4YXHWOq9D312/E0r'
        b'FxBGgSTAgXhklMFaBUW5i4TgFBPeD9zmVbuLq2FLMOrhLa5sZD9oJ7ZfigqzHzQImomwVsnn8ALl7Eov2GbmV0VlwCpYh7TfWrKyqx7h6GQatIOt0aRpQy44F0+iihi4'
        b'xxFYNFL71FUp7prCQh2iScwtunrd1lGxUsKDvMncVUkQ4iNpefpMncGkS8syFuSnZeld7TWXihytEv7Rdxw3YqBlTsqtRJdXuzGX60+ILcLzgPB8/7z4JCWowTo1P+ag'
        b'IYn4NtA3bEdcmsjT7pYY31FYmvA9rQUHvPO56fxqzh1w5/Jg3MPhEUi9qQD7BPAAjYihAlbyy75OgBtgC7g8BhFU++pVCLGk4sIiaRFH+Uax2bBhBpnZA5vBVlhpghdg'
        b'u5vHKg+J53SRGJ5bjcm2SECN8uFK58NTxPU/BdkiN+ORdMRt5s1n0dC1MWBDupcFUxeoGSoAJ+FWROQ1CUFxCnACblutCMQqRAK/TANuShbbFzXT4AY8glQycN59xkJY'
        b'ZpmMKpiMTKvmJ5fPBYc6q0AdkCeBVf4SsogaWVa1yHCqKywCm1bDS/AyYjzgFjxsRgbEZcRfLlvQyyRzoBy0jSLxw7B+ELyC6GALAXon1k6QOVeXIEJm1GZ2PtgJ9hE3'
        b'unr1i11rhbXDzfhXu1QipEbFcqA2ER4lRoIFI09YyVpwnpmARiiKinKDR8hSwWRwuhRuTRoCDilj4Q5wNiZWREmfZ+AB9jniuYRbR4KL7sq0AXiJXvxi/qUxlti5H7hI'
        b'ON1yWC4CN2bCKxaMq2BbuGeyMA6xoVHUqPhFRCSIRrtRCApxv/x0xaWSRD6gc/QiIV51nnNBni79S/FAZCKQ5Do/skI9/T2P9LzfzhjD5w1KI3n9boSkS9/VWyjLBCyf'
        b'VsBWhE3bsHYSjN1iNcQV1iuMBaBMXAouwCb9/I4o2jQLUcqSy4rEue1qGDrA+rb6vWOJ7gNaHoz1zpMO7J+RfuLlMr/7B1o+iNu8Jy4hJD65Nat8bcVN2a2yEE3Gw/DI'
        b'fzw6tlD34dX3f3/9uykVE0Pv+Sl8IhXlzVf6nzmV9bcpD+7+8cOXZkaMeeWdQRsaL0vvr2dXnBit2Doocc+hWednvu83MfBAS8ZbKcfHegYXfbUmE349Zc3ehz9I95xL'
        b'jLu8YqXg7R8MJ27ufHihaf+HG3670nZN/eE2z6F/AKYx+Y13vng/7V7kNznc0TDZ5/9ZezlD+ftU84UvszJe+FfRopW/ufRlU31AuWzLQv3VpL9KFk26fpWTfhEbMSfC'
        b'NPVfh+onXxq2e/NfJXXNbapvh0pUiyYNO7dlcd0PaVPcj+8+05C1cMSwpG3f3Up5997k+x+Uz2Hvns394ZuF37/y9ltffngwaVRL/9tfvyH7tnSr5C93P6ffe+WF6W8X'
        b'vwMYuRdvPl8EtZJ4vJVDnQKzD5Zyh+dYeAiWMXC30ozlUTrcuBbuj0L8hqaYVfS0aLCfcF7YAreBYwmlwS58HV7R8KsKd4JtYFN8QpCKf+iex2SPhUfgVaS6Eq5epwLn'
        b'yBp1PNT54Bped1jHlA6E5/hg74pseDo4CYOEtRURguoWA6oD4eXUuUSqgDo/2GpnZ8tAhSOgtCaZFEc8aw/S/GH1jEmxilgkXWCtgPKawmbB45OJZg6PruwXD04jGkQ1'
        b'1MfLlWqkDw1K4KIR07DxIq123iAcWEuiapeCchJYG+tGnr2gN4PLswlksE5EcUq8yvjsi3y5XePhengVHA+OS0ygKW4EDfZPh9W8St4+Ba9qjook1WLOjGpAOD4IXOJi'
        b'EPfYwgfL2tBnr0OawkqwmcjT/qCW9wZdB3tR36hgy6zu7qBMePypaq7o5zopBvYq/ojInN8pMl/AApMjrk5vRsJ4S9A/40Pjq4T1Rml+zgl1KYkiCiRx9T6ojCdK92Rw'
        b'sAiOLJIyxvUOSd3KuAjRZwHcJeANV3Kzm1h9xa9vsUrY5nVxxhPEKhrvGeB0rIBaYRaD7WC3n5wla6Wlkc8R1xWsAcccJpQBbOZ3Y2hctwbWqcHpBOyXhpuRVKXcwUUG'
        b'HoUN/nyg/3HQEBCsDIZb1MogIbIBm5hwJFbWZ7LddENfh36IIwd67HJAOfc5oLvsdMDYBmb5OqdaBM801cIS3Zz7eBQaZYnM5W++LltvMuuMJpk5R9d9Gx+VpEveWLNM'
        b'b5IZdUUWvVGnlZkLZNixjQqiVLxLC16QKSvAgYYZuqwCo06mMRTLTJYM3g/UpapMjQEHEurzCwuMZp1WJVusR4aSxSwjEYx6rcyOngQqR93ogbkYgdClJqPOZDbqsV+9'
        b'G7SRJFBDhi3ISBneqgjf4YBGXKW9evSGvRTJ1RXjoEO+lP1Ht4Ja2SrUZwimXiuwmNBDvrgz/6zpsTOSyROZXmuSBS7Q6fMMupx8nVEZO9Mk71qPvbcd8ZYaGX5HQzYO'
        b'ttTIcCAqBsdRl0qmLkAdV1iI2sKxiz1q0meRUnyHorHK0GCA0FihsTFlGvWF5h4v0sNl5El1N2Xc1WT9IWgaA/YmhzhmQucvjkGqaXJMnGD+5MmgVS6BV4sng+3RIycP'
        b'9PKgYCNskfr7IjusOyl4O+pf1JUUKDsx0E5iYGxeWd6/YKaxx4IszFl6btShVKN8hOv0DDPrGTXCg0k5pz7/6yW7PVeICezLkDH/1icP/I4x4Un92S8XD6tv96iMHjDj'
        b'S/fhm/udmy4Z06RlI0dFbvtiZNXVVnFQy5lxS186Vni7/fTY51//8dd3PYO0NUGz/1wf8/16wftL37BeLpDXrQ4W7x51ye/zN28ODLkyxCdb/fzHm97y2ndr8PeDP7zT'
        b'f33Av5th+IoDS4f9MLBZzpBIioRJcGuwMUcZGEO8W3sYJagD54jna1l0YjDciPVuzkKDKyZYEwDO//x5OEHaaqOmkEijgE5ptI4ahiNckczBjnN6AC1EkkZMl8iNdgbm'
        b'EqZlR3WXFFyjfbU7Hx/5zE6kVpovQCSQDWMMgoys4bRLoDLq0ydMt0VjcbATmW9Hgx0U0svi3E7hNMtHHhKHdITZoBUpXC1eeg/4hN01pvK0Qv3iFds9vBa9x1eI1JbZ'
        b'mNS3wCtZ4aHjwyLGTQgHl0Gb2WxcVWQxEfPpAjwHToFyZAK1w4vwvJdYKvF083AHm5CdX0+c65fd4Gkp2E2MiGk58Xhlrzh09LcjL4XF8pYF5R5LNVJUaOis13KuRPWz'
        b'o7xu7kTatBzdXYt7d+CrIzzLQr25l37/hb9C+J2EecWr7cGe6Aqm9PjKx/X/PD5gwu6YV92yPZeEbT016c/Ll03R7poZ+570NrssMfPKt8v3hP2YLVCV3zFPH/33b+a5'
        b'N2wfcu0L9srxAdmvnEHojZXQ+bC5KN65omkd3EV00P3gJtHj0Itdg0jJdbotoizEcbE+8ElzSk9bsyhOMxaY0zKwjY463c8V54MxzvsgbBeTWO4SxTNhu706x3yRMyD4'
        b'Sf4Lhs/Rieu16BLYA9c7nrDGcQbKF5tk7R3REY409ILssDYE1CSFRbDUKlDnrQLVsIKgwsRh9r3RhAH5v1+xmLLgxVSIjE6Ci2kxcCtCURWl0hSSvP0MxCD1Do3YEBH3'
        b'nN2idffhd/gLFV6Ien2CD49L5Mm7rBhLm9DQiPxonWwkn7gozY6PExTeB3PG2fFxjDclo6hJoRHvy8XcKorsJga2ghtjkmED3LZwQiis5SjhfBo2IxQ5BdtAPSnnVjqE'
        b'Go8r87wT/eNqd76yhNXtdNkL2BZ/sPr+on/ya3th+ThQkQxwZbBBAG5mU2w6PRVJye1EtvoshTaHD9CNwXY0OB0IqxVx2M2JjJ1AEm4CNwVjcwHUBEvk8AbcS6bUX1wl'
        b'pIYu2MtS0ZT0Q78MN/RKeC1G1uCxYrGgKpROT4g3ZionFs59KyJrtoEhK0AV8ChnXAXPIzmUSCWi+gngkmGRlBm/jb7AY9eoXP5tXnWbSq0vfCSk5pYZUwYvU5LExUNe'
        b'oKzIbgl1ez9yVhTH5zw6SEmnZ/1JRMnKTH7PLQkjiYmjf0NfyO1gKe/ygpSw9/hxfDtkDr0trAANe3luSt4gjmcUmQPp0NlNKLGsNGXeZTVJvDnXQv0t8D7qy7JV92dn'
        b'RJLEDxYspFsYKqZN92PJw7V2NADjN9OB8SohlV6Wfd/9jRKSeDFtCXUl5z0WgVRyf2adiCTuHP8cnbAImQKFZaW7xIGzSOIfxw+nZi4byqHXtPoN2xBIEmsGJdBNq2Jx'
        b'8dz71oYhJPHPob60gqG821Zs9EkRJvOtb+//Lt3EUoVtqwuitCtG84kLQl6hqmlK1saFD88NU/CJa1HHfYcILjT+P5lKuZBP9Bv2EXWFpgLb8nKM3wdY+MQhoVLKD+f0'
        b'/WPoo+kD+USPaYVUmb4YDdyDjG1Riqn6WWM+ZE2H0W/x2o0L571u+CDa+9EB2/APT60e8eCV16O8xNUzppZl3ip7Xub9UdxeGBfc/mef8aawu1vd/zFuzl6vh7mTnisZ'
        b'un797Pd/v/BM62cBthsHRMHXW/7yYODFD8bkd6g7flh1Td3UdDtr6rlj+09PkJ5K/+q71y8ebpxo3W4bGjtr8dUH0wtHfBh36c7sW2OPwOqS2RFti9sH3829t1I25tWJ'
        b'cTX/9jtf6/tBy91bYx59e2josPrMQR+6fbr3xMzyH2bXpH0yq/KzdTdWDf5wS4Yi9l7pH7h38xNe/XbZNzeaUwSzz82buP1ln5rf/s4r8JOP8mJ3hRyCp0Z94p56cr51'
        b'36RHq6Z9m9X0h4c73tDuXxVx7dEfbKeSCl9M3/36jzfzo9YeXRN0zXYz/cjSz/qJrryfc5BruB7Y/tLzC1IeTg14MCLg43Fj/nbggdyzaNTWYVFV/Ys/y37vTVN2Ycm8'
        b'qoei281//eT9+/N+6P/e75Z2BAx5vG+V9d91ctXfD0Q8Sr4XMmrsX3NOvhWY8LdzH5sep3ynyNk5e9arB9def/nokN+3Pv51yru3XzOvXC1Mfbd6W5Pp34P+EZd789Dd'
        b'vwxaR00asil1TLtcTESPErQGOtwTc2ALv+4XHgOniXKlA2dXB8PqELwZ2GkNaKbn5oIdZL4vdya4FBynjFcGqQWUVMh4wHJ4E1Qt5CXWWbBF6yKwYBU4jkVWyAjetdHk'
        b'nYuYR1IsOMUtB7V467WRsGkEX/Ty6PBglTyO7Jw4Bu5GdrAXLGML3OYTf0tiCbjdw52zE7H5yyWwkkTWloK9AfadWJzRWWnwPAnQAu3w2s+cbZR7//zYjGdWOsUOMUpk'
        b'cIarDPaX0hzj6+kt4WjXfa7wdwD69kMfH3oUEolDkU7qSdZfDaA51of2Rd+SHxmG+VHMCkkpMVmGIEXlODwNMbhvac4rqwKyLqJDZLdBOwTEsHQR4//9SjOkEDfge7IA'
        b'Y6NT+tehy8Ae0v/LoL6lP/bww9tIBl7qRQEYDsp6UXZxXBBAWuENeBwc4DfGLIYHyJSY04Xs8LMIqBBwQYDE7EF46kVffhJteyKe6ORrGwH3B6tJ6K43rGID4AktYYzV'
        b'KcyKpSR0I13hs9y+fcHMoZzxKL+ngcJrvF0D0IqEa/MwZ5Wl500Wp1B69Z1/MKaD6MnC/YeG4Qi0aOnML/Om7k0EE8VFYyNTj4xf5BkdWF4xa/BflQ8k+7y3Poz953fF'
        b'45d1BLvNWXvuTOOdEXNqJBMGX0hJr/G4dL9hv/bhiqn/2H9h78bPG/4QOHL/8s+3JP3wpurzi5tUr/66SqTfNXv0vb/8+Z9vzv80tXKbqPbGca/zH+48W5Kp3m5748fi'
        b'wt/cmXGm4U+//p9Lp9s+fFstNx8q+Z7+ig5ZdtDDvmVdEAsPuXfu4AvPr+2yiS/q6Qrex3vEF1yWeXR1dS7WkDpmww3whmOEnoMneHcZ3JSAJx4PcAVwPR8zrwTloNmR'
        b'D5RNwPkQe/AJYkEL3AYvEI/t6ESwG+fhR3BODh5DT3CGnQluBtg9xvngJqgLUaqViIscCkpAcs9rKJsGd/FvBI+WDgZ1SUTlmQZOKeIUDjYyBGzmwOEssNNhXfr+r7OG'
        b'Z2YcDhomjCPIlXEMwLFeDD1mtpQQPYMXYjK+ZO2RkLAKI947zG7d443M5P3/r+He5CRw3PRP3ZyplRF9kzdGncQ4XydtM5FplFcEmwWbhvU67Y3/TFK6M1JKS6eyWiaV'
        b'07KpAi2XKkT/IvQvzqZS3dC3ZBu7jdMKGvg90HD4AacVakVkdY+7TqoVa93WU1qJ1r2BSfVAv6Xktwf57Yl+e5LfXuS3F/rtTX73I7+9UY3EqYrq9NH2Xy9O7edsjXa2'
        b'NkA7kLTmg56J8Ufr24D3QsN7BQ7S+pFn/Xt55q8dTJ4NsP8eoh2KWhho/zVMG4B++WrJqnT58A7PBJ7BJ2oMmmyd8WNRd4csdhp2zSMjkSRdMj2thN6EvYPERastNmjy'
        b'9dhRWyzTaLXYhWjU5Res0rl4JLtWjgqhTHhewO7x5N2NTk8mKaGSzc3TaUw6maHAjL20GjPJbDHh3d+7OB9NOItMZ8CuSa0so1hmX8eqsvuTNZlm/SqNGVdcWGAg7mUd'
        b'btGQV9zVJ7nQxLupUVMao4tnlfifV2uKSeoqnVGfpUep+CXNOvTSqE6dJjOnD6exvRfsrapIZ5qNGoMpS4d93FqNWYOBzNPn6818h6LX7PqChqwCYz7ZjVC2OkefmdPd'
        b'SW4x6FHlCBK9Vmcw67OK7T2F5H6Xih4PyzGbC02RISGaQr1qZUGBQW9SaXUh9l3TH49xPM5Cg5mhycztmUeVma1X420PChHGrC4wavv2HUVTxIXJ8QvfHCvtShniUX26'
        b'94gl+Mw9rurptzbozXpNnr5Eh8a2B2IaTGaNIbP7zAL+s/vOHZDz7nP0Q59tQP04bW6s81FPX/kz7Mop5EOOcsFGpG/U9b2SB+6GLfbVPAPhNrI3fP8o2OSqlQTGKFQq'
        b'uGmQX0gcTUWAncIXg9fatxEX5sEreH/kJCVeS9KQRFMB8IwP2MfC8qn99Y8ffECZ8NLv1xZ+hFfSBT78DF0Vvp+lx9jXgKgWBWriNMx5/0Ghq0NDtMteOtfYvPVqpbzu'
        b'YuXVvxsqx9Upq67ubK0cfeD5qhG7ysM9qIrl/fbXfYtMCCIxb8CWmE4NKxJu7Cq/l8GD/BTx9UhwBucbBVo6FSwinPvBJn669qIyzx29r9x+GIAMtDLUQGDjxJOj+DDD'
        b'U/AWrAiGG2PGcxSsKGbhddqQDzaSh0vGgxbUDSzchnuCJjt7gXJ2Apl9hueGsrAuPjRcKSJbNscXphIDKBpeAk2oQrB7Ucz4sAksJSqh4R4NqOMngG+CI+AieblqCbya'
        b'mCCkBPAUDa8GgtNPjapzVfTT9AhB09K6xynij1RKVnhgNb1kUFfMVTnK8fK6lQ/DNm6nqKeu3Ghl+Gyd8dY70aWCcaxQLnN+qAF9RyD2BU/f682wVmulVvLr6GjMFtwc'
        b'5oWulebB6br2zGhCl80IMH4XlO5NOhamPfbvczoNNcJqCzKfCahsHihxmt28Me7tA6JtDogeD3CZUnPMzKmeqbEcR2OY7+q1pj4b2+lsTIEbc6h3vczgZebpET9XmhBb'
        b'lz8bEOt5INzTdGsK9UYiMvqEY48TjucwHJ0lsEzq3vFdm3fwebKRYTTVuaurTeDC5/+LWYIue9u4cljsqViVtCYZNqwB7Rxep0GBTci6O0H8t6MUcBs4iSAtpeBp0F46'
        b'PIR3gp6Cu8JhXSxR78M5xCzqZoNLTFzeCH3G2yco01Lcm2/kDqu751EWKuVW7y88Qg8+XCU+8sGDGw8+DtunHlf8Zc6FzHtHrjV9/PGbnlXvh949eOS9c8fLM/cEHZjQ'
        b'Alv+vmn7pe8i32n9Rll789idJe+//s20nfsC/yryDveXfSmSS8gSObz//GBX69SFccbOKYC3U3i+WA0bSrDrNZafIoDXkY27mwE18Gox7zapAFVwd7zLrmjwRDRTDK9m'
        b'EfMrDjVwsQiU82aagOLUNGgbo+UjYDYv1lvgThd3DXbVwPUSPgBnOzxs5flfYgLYBq86GKDKi3iIYJXat78xHm4Mwed8cBE0uJHJgwQOgpPgsstu4LASrGfA+kI+YBwc'
        b'Xf5cl00Y6VKmIBfu5EXFpZiBsC4GnI7hpRoNz82jfMBJFm7Qga1dNnR7Rv6rM2QaiwvNhP+SXb47+e8IvEeDD3GuSEisZk+uZy/tuhbm2XZutG+028mE8fkS+3thwn/6'
        b'OUzYDs7/qZqV1auaNSNHY8jW8WEbDsXIwRW6KV1Id3pWfcugW/2sahZ+5Z4LdTnE4Ej4MoOwbkNXVYjoQTtBOSxPA0f05jesArL3aOu+9/g90m80tiNdR0dnir5mjlVJ'
        b'3f1z/SP9IlPO7drr/5+jK/1z/c6nrPR77OfnD/zn+6WUte3evXlE0kuNzffvUYGSis3RH93Z9opkfHn+iBmiTN8XJbF3MkOSRfFT5khmhLLZkdS/tvkqVQ/lbmQee8gY'
        b'sIEoLzJwm6OI8rIMbiaEtiSfAXVJOCQWLwkGJxSBNOUJG1hdVBIhCc69tAtF8OSwCymWG4BtICGpSLBjOPZsIN3yXAxNcSH4JIx2sIMcCAD3RigRsYXBShyolgQaQnh9'
        b'EmuTobBJOBnVU2nGwcs+GhFSlJCaBM6CSqIqzZ7A+23Xz1bGO5pPXsqrVyN4PgHXwwvgOnk3rESBDbOJHoW48Dn++TVQDVodjIRnItJx8KoaHvz55OyVSdAwzYEz3eOu'
        b'8SdMQtyegXRJQDfy6VbY7grZ1ScRG3c7qRdvvNrSC/V2PIF6n9K8nO0Q5hSYzHpthxuiDbMBKwodQl5h6LFYqyuFc461E04K50hk1tMXadkp/OPpdDdHAP6bptViIwpT'
        b'pYv2wRuhTtnfJ2nzL8MTdgy6j53pYBAZGkNuT/J2cgT7u/Ml5/I/UeHAeIsBmbDK2Jm9hCu5hD45SmKDHRfrEuok7w1eo85sMRpMkbL0BUaLLh1HLPHbTWgVsvTZmjwT'
        b'n6bJQ4naYqQMYZ3MYP5FHIpV64cHfcqSlROTZ7zxRfoKxHru3/ngzrnGqzuaK5srJ9e1725PO7GjfcO4utYNzZtG7CuvGVFVLhB/n7J3t79/hb/Uv1Yp9fO7E+pTnVyW'
        b'sU9PJSR5RFD95CzREBgPAyKug7A2qRv7AG1CXsxXl4IazB38wTVY6+AO62EdseGKJOBWfEIsqKZBTVIirE1QgY0hJJhVDuoF4LQMHvv5ZOqp0WrTdBn6TBPRfwmVenel'
        b'0hmYRkuGdSORruXsto+Ql6LH8aUFX1q7CmDXAyQ4l2yFzryEhE+iy8VeSPjNJ5Dwk+H7PyXSHESkc3oj0vnEnYbo1MAjJg7Uc6FWF0fa/3/0iovFJifJeBeYmfeYEesk'
        b'S2/Q5Mm0ujxdz+jCZ6fUr5vP85Q6f7v3z6BUB53uPt+FUv2phHkek0QSRKlELy5Pfw5LegeZRobwhOrhx+vF1wPhZVCXAK5jQe6g04vLzWPJQ3hjRnAcbAgcABtC4kFD'
        b'V1p9AWwU+YwFm34+qfbjvbNPodb5hFq7KXqqHkXtEvVUN6o0nnYS4Vl0ebkXIrz1BCJ8arNPOX+HtlEu5+88237mDn9jRi/kR3CR0InBkp+BSA6hn4tzu9NlnGkxGpHY'
        b'yCt2Met/KWZmrjnEmOaghLEvZGD1ta2xmeDkuN5x8oeETqysbegiPe6r3Gs//gvCSRJdvhOenO6KlFHgPI+VafA0ER9r/eFholseRRqnAy3BFrjdjGdQ4b7RZKlSCF4d'
        b'2UWArIAtQUKEmFdFMrjBvdsxTL1iYmaBxWB2GVZTb5iYKu4NE3sUVTvCLwv7lBW8K4RgZTu6vN8LVp7t+8ihp4Pwf4SV2QgrDX1iZWe49jNjpCwwCCt8eoNsVYRqfFAv'
        b'vPvZMPT2SiFLMPTO6hnPgKF94Odn1P0Q93cNdcn1CEOx/SDHJxN2Ymi/+Q79ZnU2wc/n4W5yYMg+eMOFb/rDnWTDEnACNMHT5HhBVVf8DBLCgypqErAJEZc9BTY+A4Z6'
        b'4759GoJm8ButdcOO7iXtnPJc3zh5AV1+1wtOHn8CTj6tVfmg7svGRWlp2oLMtLQOLs1izOvwwNc0x4RPh7tz2Y5ea9yDC+EDUYxN+HKIsnuWO8SFxoJCndFc3CF2OGZJ'
        b'kEeHyO787JC4OCCxH4SYU0QhIwKB0B95Yd7P8gt2RXHxZm5Gl3zccTiGWMxw7hzt8mHE9AAP1H0086OQ7eOb83FHuaRS2tsT/3uKybQMKFvdz7kSXA0vJiJrOiHJFwem'
        b'B4JywTpk6PbcxQPzgGiMJdgh2XVumvd0dvS3L4KxDx3ZUPqxbNYavN0ldr9m4hUuRgPW8ly0OjWyWLsOpfGisxu6uXdvossfGefKfo62YMqYVgROkYX9CxX8xhttjldz'
        b'HMccJxHhZaVHLJioQTuyMmqeEI2NI7FXgvonBGODW/B4D6bo7mAlOB7YvsaB6nr6aueOvP/NAnncWE8nslQtZ0k8ztaB7hQWaN4RX+ffn3okj0S1iteKKGRjxXiQqNYZ'
        b'yS9ReVg5pFY+L/jM72r2T7OGyK/mzk07Mbwl91pKReAe9a8mjV/SoNifdDrqaOTyYe8HHcr4QfE4cZ3Hn4d4lN5Y2Ba4fsaEuL+oi6d9HCAcLBn6Ucr01MMzXypdlThp'
        b'9LrA/lGBC9e8cIlL8zlaeHZ4Rtrv9BdEIxceSddNist9w+3L2OeDPQblpBgFZSP/PHOV5HPTqsLAQR/OOuHu73Ft3U/I/ohOvUqRZdEjYJMbGtj9M1xd3EzcjGXkRS15'
        b'fKjzA0NWwqw5o/hopGHq/hTG8ZdkmVO8Z7J84smpgygF6hHZIMuUSd6rKEs4xoOTsyJhXaJShQ/WdWxEBzfFi+Bm0FoMa2aB7YLRFFg/xg0chodgM9w6gVS2bSwfIC1b'
        b'YpGuNqTzLWydwodSF6bkKcRT4/ltZu+88KvMA5MJ7dCPLuhHpIoFJrwS4qPfzhndcN2DHSedIb/3ryLfSUOWjInSCkYkXpsRd71miM79xffv+l64Mvvl5wTzW4Fv/+sT'
        b'pm6Ntf2j6WBK4Nx77xTOORx3ac/4oCPxIGrfJq/POj794q3toz7dMffDK4WHT77yz6/G/zBNlOC5JuTNgt/mPHRfuuF/nj9c8+Lv3rj2XdzQR/X3kl7+7fCTG8dsYW7J'
        b'OSKWVsBt4GI8OImowvU8oYIxoJafG62LXuTe/YRzcHC1PT4KB64RBYxGVewKBtfAVWUcDpFCfSmg3OE1Bl5eNZPYBSMAMu6DYW2Q8gV4QUWT9X2Th4LrPYPqf+k2wK6b'
        b'GhhNmi4ucxKv0yndzByJOMQbcYsZb1qG2Sm6N952VIOPUMdRDC461y8Fq5U23nEyMdzAV72Iw22yvoOI8IpZJTgKbgQHqUG9i39kCNhfCE5z4OQoeLMHR+q6LVIPjuTc'
        b'Fum/OrSt9yktiYMbRQZLeG7ke6L0fmqrO+FGfxQLMTeS/S3CH3Gj36VBnht9uYTnRsPn/NV94nzj4uapC1+Yu9gyTjBv/LCGopywIUsihy9dHWe5Fnls4cxZ/1nyzZCf'
        b'Br8xcXBJcbBmnliUO+DtYV8z8Hnp+AGTroyrGv/q/xI3okSfismrrFtsX1ox+xv2WFwgT/jvvMjzm1DVsPGGsHh+5pE8GR7H8QspFr3Qf1v4DD5x4VD+lPrQrJ0jZhrH'
        b'UGQLgxfALrPrNF4GOIjZHLgAd+trfuXJHzQ2e8Fw5evtHjBUyr10fMW5ff3WX/jwbrB34ea3Fkqu+zDWS20TPQRXRty5ffx39LRH/zw8/exr96OmTJh0cI3pxeIVTeb/'
        b'KDbs2LAreUa29v38hd+0FXy/Kkqx589+i1N8dc/nD//7+t/mfnP1QfuP9AT1sF0Nf5TTfMzjRmiDW+Lt57ZT4inJyxldqbWLhvmLtz4iFKrVdVLoqK4Uuo4S4ZCCAbyq'
        b'Q6hUSmjWCJ0VvfQLIABOUoR2SulOihV9b2jEB9BuABUv8KQYm+igxHRwHG7hQDNt7rFYEv+TnV8XIBKtFvAb3FvpJgoTYDNTypB7Vsuhe9ZM4+czqUZ6uXQZU8qV4m3w'
        b'BdWUmcHnMxgNJZ5WQROrFTTTpYLFlGEo3ny+eCV/7BF5gg9EEiyhDIhkDS9Z8ZE7KlIDLt1mZY21KJegmT/+SEjOkBiM2hGWiqppqwhvlK8VNaD8VuEUqmiLYS0pK0Bl'
        b'H6Gyv8InNiDoBQhKAdmYH5cV9ygrRmXfMkwnZfmDhlQ9Sg7tq2QjXSSuFvK5UQplxSdDBPIHA9gPEVJbKa2bP+I09pNvJWrErHW6wtlGvJhqwWOBxZylnGTEDieErC/j'
        b'wcYPjDiSyYg3opWLjNkYCd10Bku+zojPjcBadocQb/2u1XVIFxr0+IZosXzZ6TyudW482lkt2YqfLAHDq3CN43BN9MqfuU6/Q4rPajGF8UuWfVi7fY03q5faj5Dgzy3B'
        b'J5BI7KeW+LrcSe3fYnIyiZifTiwIAA3xCEVjlRFBeB8FWF8Aa+NFlCyAg+1g/4we8RfO7dexyLZSJrGWTqbwuVOk+xlyjANegUu60RjpeAW8JbOpD3PTg7xYmrkgLa/A'
        b'kB3OOo41ZbEhQ3a1W5zH8UAikxbWkJ0piS5GjQFVgmmiYu8BPc4IckaqjSdwaulc2ijFxoiWteLTnWgt10ThM4MQ1AJfqpm20oMoLOtwCtGrhfZ3IMEizOg1/E4PHP8y'
        b'gpIsfV6enOmgDR10Tl8vht8Hvxd5wUj8YhL7kHHkkBiyzw2yJU7C/dh0R6+Ejw9HL5hE3lZIjQkQgGa4r3gR/ZRF03Svi6af/UzDXrfadzbhsmK1c8GfOq6QSi95maYK'
        b'02cXv1jEJ8ZNfpmamdyfpaLTY39SifjENE8RdTdyGF4DkNCxkKb0pTlvceRMkXF/8vgifTl2oUx6fuvFytbKi7vfrRrxmxM7mjc0VzbXt8ecrLTQmR4zJH+cfkz9m+nl'
        b'gzcIEtz9awWyQ8MUw96YIH2zXp7gE+1ziAn8lThsdNUSaeClsslVuhGZoWy2OzVllv/WiodIkcXCajloCA+GlWCLyxrrRNhMlNx58BRoth/sB5vGqx0n+8ENMfwmKC16'
        b'vGJQoUamI9zkB84oaJTjJAPPgFtGUvvAmAyk4F4VxmFLE9Yg7XUtM/KFQT9/mXa//ALt5In8kRhpWn223tx9x2T7zltiQtCYkAfTxveclVQ/S3M1juZIwRmsY0PVMpfP'
        b'7Scsvyb7Pm0fGIhetiEJtI8nm0njk4rw8bi4i1D/gEPjJoHjwrVgPdzRNxfBijPPO7C4a6YJKjLqDoHGlKnXI834Vcohk5/r2lGiHN2aPH1WcSKGnsSJsCRUVDHDjYQR'
        b'kG2SwMnSlRwyM6oYeA1shTv7BgSzbHwUDJGDA/D5SRicUjtwxEvOqI3vU0Rdn+UA6kn7prlZDHYQ53eyNKygEMYLt4ILumDY0AlrCbIsT3IU3q1uf8Gqn91lBDbjB311'
        b'l1tGxHj+0K8lLh2G0WolbC+ODwuP5e27jFykyXmNYKO8YeN/0VvrnRD95pn6CkHHi9YV3foKQ5gBdogxhETRnDAMx9TCM+w42J7QIz7PeYIdXuerpRGbx/oTZQw0YyHA'
        b'VjJIq6BKWf50KyuDWD5TJLYyhWFWGp80RcZZoO4YFTouLHz8hIiJkyZPmz5j5qzZc2Ji4+ITEtVJc+fNT16wcNHilCWphBV+htVSXmegkXqgX4XoV851CPkpkw5BZo7G'
        b'aOoQ4r1BwiN4TcCt+7uHR/Ajo8PvTk5zZnkvHt7oh/RACTyeFB8WYQ8nU0jwGA1iI2Gboe8xktrxRMufrUTw93eOphFj+n2vWBIewY9DgQuWYBYplQ3AAJAhgK3gBhmE'
        b'I2woPD6h790vyfHftPP4bwTOM+942evx3z3PfuHUhBnlwMMpZL032A6rFiKq2r4w0W0evAja5qPLxfkeYCNDBcIrXH56if7kJSNtInramx9/kZ6CpI+GzkQS5lfpwrd8'
        b'qbH/5qSm+V8l23cuyINn5wUrY6MMyNipCxFRbuEMksg2sIMIhjh4ADQEL4O7HQs6Has5QSvY2tcJ3npTQZpZn68zmTX5/IYc5NQhV+5eYnzoLFRF9eWoJ5nMvXLvjU85'
        b'xBvshrs88E5mG4nGgQBXqmJhvZKixhgFWnhtXUrc7B7Rd119mKw9+s7Fg4nG2v0XBML22LEFKw1ePca6n9qCQ8ySFwgF4GA8EsYbYT1HCQczEj24QRSN+wG+lGLBGiFS'
        b'NJZ9FevOuwnh6edgY3gYaA8r8A+lRlIiNQ32giqwieA1tAWBzejppTBwFm+DwKEMYCeNfkdYcMCVCNTnkY0RQA2sVVEquBdWkbZgmD8Vig+rTE9fJlF68ppOe3IgNddP'
        b'xaHEjF3PZVEW/AbgUjrcAM6j3gSHFVFUVAS8RTIf8RdT3pOOsihzQuzMEXwN94TIkBYHCvHB0M1JCxD+kL2vpsLj4Eh8LCiPAqcUQoobSoNzYAfYRsp8MT6aKgv1YJAm'
        b'Fracy+Mr+tJvKmVdUMpRoelh50f34xMPI51ZGvOOCGtiH8TFU/qYjg2sCXMC38+ks+beiXs5WpoY9v7uiEVvL/feFPCK199CplQ/GNdy5Z0Z3x7Sqjyn/7PpO7cvD+45'
        b'93rcmk0vvf66+7i1+QLDncGZlXHvX1VI/i6tcP/qPjDrFLJvZg25//f71zf4jFJ9svLSbx7enrp1vPuiEykvbSma1axMfHuD4NX4wxUS06RrWz6pPPn7674zv0v/tnX4'
        b'la/rRt54Jc16Ozol/o7p2q//7i3ZPvdQ8xYzmLDr/D7rH6mQRP2RxbZ9AYWPAv6zZbzeOyCdHZ37wY1v1+vfefS7/9fet4BHVV2Nntc8M5k8CUmAECBAJi+Q9xtECCSB'
        b'RAVBUBySnAkkmUzCmUmAOKEq6szwVERABASsBR+oiIiiYv9z+KutVvtXf2vHR21tVVqtr2otaLlrrX3OZEISqr29/+13v0s+zpx9zj77vdde7/WKb/k9e99959Xpe+ec'
        b'vPXL8W+/OnD/szN/VvRXl5nZVhzUNnQQCKtTnySOBfIr1O3M++pm7T7BCO5sAryYoYDLStind2jHl5nmxvzckRV5icb8l0xdOZxUl9WbFxjay6i5vFN9hMmeH0zUdseM'
        b'PkoGkNCBbD7UQ0NIa1I9pm0eX4HW4kCBneCEBn56qXr4e7ie/xdwRBNb4KDyuAE4TRg38hICS5MuBEvrJJ7xReFoEh18f4ySKUj8YF4gmjKVz6RnLFKm8p5Rge4sJWqv'
        b'a1ZqPW4Kw9jJNv1nYgMIyu85Lt6tCta1pkdIuOEijFOkLa/jtS2Fc4sKSDEd4eGJkaNHSlweL1V44DQ5rB4gJx4TtE0NCzhtOyyVQdygYYBKGuaY+K+LUtRKDpEjDMAZ'
        b'ARIMgyaGkeI0BSWlKGiC/xIcy6ZMLh1y9YU8QWE/T1rMupg8LMqi8d16kcVWhlyiUhOW9sPzoHhAgJIZ4idVdiN9Y9FAEUuj8LjpjLANQoF9KT5jr8FxCUPp5bTBg3av'
        b'qFPE7bk13mYgUZiGUk/xfBlSJEZNrS0tHkVB4VpUIqrZHJUCnjUBwDawCH99uydq83tQcSqA4WpX18uBlcr7mF+UPd2D9ULzPsT7D2Jr1xHfljtFQ1dWtOpMD4nPOS+J'
        b'6HSRPO9ePk67vwKjjVcxigW9XmJ0jsOwsQdq+yTtce1UajfUMjasOL+IWhICzAECnEkMOox3DfO9HwcaDixZxIEm9p2g1MAcC7IEOcSgiBHDMShqh4hzSSUshacUrxvf'
        b'Q244JWUTIW3myrP5U66dvqbJW1I4ndDEet+KqdcMHr4s/5rr4FrowvuSgunXTp9GCPcZbCzjZP0nR7QgUitRs99TrdSujJpWKM2tLVETspHgx9u8GubmedqkURFqiVpa'
        b'UOFM8UVNMJbwgdWo9GL4ezK6voSv3Ubme0XD55IoGb4bKLwpgx4ST34J1i0tIS+S6iNo/6FGqhh+u0DdRQ4/LdwEl1ndObRfF0yki4BzO80FIO9COofIPCNAlABaBil5'
        b'eN3PH+D8JUFBBmQ/yLnRZkhQpuGV3swKAnnghv+zuGWpHUTUQGliX5gVnls1l3J7Y7m3sNy+7CCvbKF34Qvf6U7xpMoobz8r5ObSVMDY0Wr9jDZBoLreCxtD8ng9TTAF'
        b'njaP9yL7LupoUTwBNHDFET7WObAOPTBxMsWOZaKqdIbeedWj6tbC/PJiFxHB6iYc4auv1Dbz3CD1oCnfrW7r3bwc43V3ivABInFLRY9EQSFhbJeatosN5gbLUis8M8lm'
        b'embxWBpsssVIAV5oAWiGxuXWpXZ5MAaYhHSC7LjZtjRBHqKnE2UnpB16AEqJAlMmycnwTWKXZylyKjxzxp5IcpqcDk+SuuTqI2fAs2QyKueWpsh5IREoDzQbty1NlYdS'
        b'KkceCKk0eRh8Y4YW5MqDIJ1OIUX60LwNjybMhmnx+AIzgWTrsvAMtuICA7Z28ugpzjEnS8Y9i04CS6CDpv/Mefh3lp8ExAAK2+7XowheEZvnuJ3kpp1J4dX9LdW1nhdi'
        b'hJjQ3j+uaSUXZuyREqS2InmBNDosVcYvIBNBQRF5BLGB6hU9WctFbS3e6nqfG16/FNeEPvFNiOXoVrdg1J3KMTO9ZqexGXWDvfuFqMmNxwBtih7t9XDLvNpJh7Ynx9eN'
        b'n3abnli1Dpoe3O+yYaZ4P69YMPSfwPdc0xudvexG+cS4yd7YtBO05xkHmQQWc1FQw2IOB0VZaBSUMTIyGoQpGEsYdk8b58+QTUERfwHe8yiKgScW9lUGZ+SVeQy/rTN2'
        b'rJVn+RFRvuCsUDICpox40LhTFR4nj7/+rOn6go6hfjxnWeR2O5CVSsC/uh7OUDxzDWuuGzj9dI/yLb3xq90AaeAY9pCL/rdEQ+lLtxrDCEvZQirfntVlGcZ/U9nFAakY'
        b'P3I5xiKkkQswiYFAgcZh0xiLUlRSsF8mfyvgDIgu+GRDuRE7ELXHlnsv0gQlDb7/UNTpRmx612WDJf5rGqmkYkstWGC116uk870iThnw6qMuTUq7sElQQo+whlqFkZHC'
        b'sJTCEiIbYVrYDbAENwvURt5oI0ZRDxr8wPv5qMnnb6pugeZmxpprZjEY9DimUYuHteM76VArWVDCp6Jue8uxAPd8e2p8X1jxvQ/wSNYVIdYVIdYVIb4rONzQGcFgJfbl'
        b'6RCN60g9unMKuPTFMQMv2fx31AZX+kHOr7r2JPWCnrDyu01KjAWFjpnC0NKwCD0pMGCCkou4CAuC3gG9QWwQd3JA0JeSGDRAsAg7ewbDDiQlCTuGIkfWuwS3GzCq+oCn'
        b'ye02Tot53D92eqkMgK+/iQmaCNtCnKu9b5ct21l47zN1XfyiK7lY/9hc+Qpi81qqzyschTSvoj6vkpE3hiMp/XkDWe3LJo8GAuuOm2sYDb/RYGPCY241v9uED+QREzVY'
        b'bfq4OAU7uSToOjaxqv5ByFk2i0LlQlZNT0eo1e2uaW72ut2JUucJmt61OpaBcPWFXWbDoDmQS0UWvRTTnqtDbJdHfHYPnDOxGPFiZSkMzVdcDF9cC4C53heIJiFaLntq'
        b'vdVMMRWt9QPNTIpsnA34mTIYx5sk1xcwhc2KByMzpUixZeXghfMS/O+6Y1i20h47QUsqN9YJmZaNLGyWiCDimXaDgTVJtZeM8aHZIAvzFLV51tR6W/31bZ5oIp5rbqAv'
        b'sVb/F9jIXOigzz918GCiSwGyDSG4DKeSF44Jo4vDsXf5ePmiexeVofCijxQHD4TzZqHrwYFt6gINcChidMjLcKnnUNSAdD9gA9exjtFBIsH6B8r9AErI+SzuWqHD1GEO'
        b'moJCGwc0Pe4VUxZGgxL8V7L7FTz+TtHfAMwwI2hf5Qia2XO44xokVNOAmnKgPEuHFWo2By1QmyVoxaENWvpykLMNclo6bEGb8kSQ9x8GWvSxoA3ei1M4nxS0Ic7iV4OC'
        b'X5Wp9Q3wbT1v7E6Sf+MWPWsagviWyxZ1wN4AOrLeK8N0Ry2BZrdcXxsg7Qc6H+CECcDaqonaMCNuJD/hmYz+MfHE8KGzx17b7PMzg8MoL6OkBAqN8rWKhMUItTJznkdI'
        b'8gdcr4drMeTOlgzOD0VWsJNnXxYlwc6n0i43k56QneIqSBccwHonyIsE4sW0F11CaamLL3VlXKh/TL15yuiN8nejfYRdIp2N5DPDEBAXodOfhoZOHYLQBI6UXLzk8fry'
        b'o47EBTP7zsy/uNhm2Jb/NDSWrKJVEni7hM7S7BJQ36LTkSwlS+nmdHOqJd1ulZyS00TOd8cM1o74MSDt5vna5sJV5UWVJi5rRrJFKlXD6vaFLqaooD2kPVVdWD5yiLZZ'
        b't83SKKIpfuMyc6Nk80LtgWzITA4dDs0vq4gVqT6ymOcS1gnag1pEvbubwAihBGlApcYgRD1gMjpwM9x7NFU3enR8RRnYA5yy6HM6sRPYEotfvSsjv7N3tQ08Z1f3CdpG'
        b'7Z6MHiVM+M+PscFjRHAyRZ9EbXYgeYG4lIB85ZkftaUmZv1YJ+rkrhm9qUEei+yQE+HXKjvlpJvRGxvDzFKijlmtTU1r9cb2jDHHRJiMhoHTl48jNPlOQpNxHOAqEvdB'
        b'0nXCTZXKec44WfHcInIBjkrcW0SDssX7AY2bG/F3XwyXov1nZs8uJJTQEOLSTkBp5nPgf3uf+B59Pxc6zIGMMpHv5Qi1AarCmjInNq18e0aXCmNZesfWdGEo4SHxoeIN'
        b'5Gp+D+uJIWEIztzu8rjKMy/obSxT79VPo6mUeSAKHaiTRogjAHwlL0wDgZQ5NgwmWkA2oDIKJzKuwXUxlar+DBOmiaRRI4wph7+ogJ2gzvxO/MdK3Dgn8eJ66s93RoAI'
        b'OR8Vq6unGbS43V6Pz+1eFDeE6RdUSRl6ZyJgZwLcCm59jHnBRyU8X3rDuvCd270krsZuS5RyfEcUr7TX3hEQv/Yi9TD0Dptsv/Agwb2kTMbZmxo7GKbhZUbsdNCj5PU6'
        b'rRMg0zRjWq2i3WwVHWKyDUC/SJxubc9IdZ/fhQBbPRIwYKCrtpDnctSnJG2ndpu2vXcgiD7VDCC4XWwQG6SlJg9TL0M+n+SRGiyAuukpkvQjgLQutTLOHABFBiRtxGGz'
        b'03Bao6lVNQ2e2gA5FNRH6nsykGj/mnuBGQTV6mJzIrb37V7f92MfoZ8vxXox5lFj55nznYHQSgMIKVP47igpronmuIWV00MnLgZ7YraLGJS6PTXA6UQYoaSLoVcSEKVr'
        b'xzDNYIJCYpDEEusFM7eEvTet9emaw/x+M5F/yyGPpZMEPMCzvEavWCouMkwngQcITaqxzKP2MiAV1jDtWYJkuA2izksJdWwN6Hq1nUTxdwFvqJqp86sEoOYdgAQiKphx'
        b'kaHTScqEC3fmpTGE1RJD9sZ23aidiFq3ZnXiY1jO8tj2jMPEHCJFnc1QD6kPaceqtA3l81PWlqDq3MZ581fFcBWem6kesgyZmdD7Fs2O26KElZAIETAV3QFKtJ/ReQMo'
        b'XYZuT+c1Nze2tnSRYZr0hZMW23X6gRWGydTxCgD22TG4ZGJ4vBRY2+JR9uKtLcad6/FANXup1hukGCvMyrcPvkj7StgHPRgBzontwwu2zSx40WFsG4CCkzlUVSzw4Cjf'
        b'o4ZwpEtIJhLoxHe1LWVFJdoTqICrbS0pxg9W2bXdGCumm+Qpxh9B4Tgc4xxxPPrT5uIZ/RdEOR6MnlIURgqQC5uRtA1zdG/SyVwiNEgyJ149fx4sIiRLownNnSuVqPLv'
        b'G8xtLnQ/IsXUyJjLLxJ8khO1H6qRXHWj9qj27GjtOGxs7SinPaYd7EEaZDYW2HVxC0zulMuY60wkEbItFUkTyAywHqVBVjgHJJL/iLJFtiKCLNtkOyDA5jgpkHWphU4E'
        b'K4EJZ9Shz/18QPGVytJuDkdio45WtTIQB2E4nPeIQFkbHKo8wIL5elT4A+qZOPGINwtKOMaVmhYU9DeAYmVxgDtLSAUHRb8P7ygtZUHpSHdDXxiPSwgKs1CAboLvTEYe'
        b'osEVg1/ZINQhuSIhucIbGk1mZBOX4iolPtY4vBCe1PmMCQajdjexad3IRCYIiXiBS3cGQxn7EBOsRfHU1a9xoyYhWRlEBZ//uzG/sMBdkmFCA0AI/r41m3BxoMdsiTxn'
        b'o5Q8WQ81GJPy0Hx0IvTxm8HCxak8oJ3zCpiSgzjAArJAeEijniUM3q2MAYKCbv8oYopIxM7IDAhBCYXhRF1xsrQZh3qRwR7ZL6EVixKgL2BpsQmBLWdeDxNNJZTCcwuA'
        b'qE2Yh73Rn9PGQyuV9QJ7siozKOoCFQCKpgUoJImKs31yVKrEYOimRdXe1u4ytBhGwGRoyL6RhbbY6UYqDoJShbN0RQww8j3peZL3yadQNk/qE8VdR7i22dfmUQLEh/DH'
        b'a1Mw16BQJDE8O9mlhUTPIZsLI+Z5dN6Ln8L+MW4Mnp4APghGi37PqqipWZE9CrLz/K3eACHQTZ08louJ951d23dEMgwmKVwDslTsgp0XBLQrN//dKdqF/miQZce49Bfp'
        b'ZzcxW4xTWErrCTcrrIhxHSLgF6QSQzZORbjCiPUsHmDzbQ2KMt/GK1ZUs8Cn9EzQjyxE4JGbCBifB+bb6q7zooqDj8bM4A+i7ZWyCC+L/wGusRTev9RJSjG/tqmk8nTh'
        b'vtEr6vEQoVWF2vpxll5wDWI/MoOkErsf8SzxAOoswzvGUm/DHYF3ItzNDQA4CgoZcPTcxJMiAoCtAzzhcrBXYGfIyNbzJRtPMA8KGWUTu4MnMKYZnGHwQkJFwe2mNXY2'
        b'4ypfo695tS83dqznDh7qH3zWfP1QP8oczUoBDpiTlh6DYkoFPrmU0xE3g6VAq2x+d9w5muj2odIOurWGAv4bh5WcB/PMZXCyzqnP4M1CMt+e3XV44z/tBptiPKU6Ll6m'
        b'R+sGD2g8qgV2Vw8YA1PL0S3WEP7gF2RFFzQHJQL4BQGJCXEa4DBAFu1B/soY4DdYGWbFzeuLRLkaL7QXSYwBdCn6iweE0xLHaLEazFSlBJM2xj6FHsVtzZ45n8sh/3ud'
        b'SC+MlIj8TTZm3UC4XrVYCZvB1iMpenWs4dSF5V3R3O+EiHSivuXw9XZDYmCVMvokDwS61Em2ypXl5k5+nHZ0vrapUjuiHiwWuJy+kvr01dk9+h3HfxRIN4aNJBHFaWAh'
        b'LDCAgYPgmwvxD0SPdeyDdE+QOccmLjlqnddc21ha7/VUKoj7dsFAumgAlHOMRckIKX96QJB52n6MXBToHUn5MpAvBwsLribizpmJU2dBCzS3VScspcqzaRgmOFdu9ugu'
        b'/dHZ2VnLUH8JKrXhZN3AkcDTj/lob0Ut1TV+lLdHraT4JtcrUQuqlDe3BqImdxMFtaHow1GLG3N45Hg1gKiEOZT6HqhOXAhfdq4pB6EIqYQmmPn2FGOQeubxIWizc3Ga'
        b'WUwLEplbaFvXnhzGLQegCAH0Ys5XQ8apN/AAoniuvTwIGwsoDlGZdBN+Y1YqFwM5iQBsHWlV6aXxjZJSE7DIAo46PLPKenlG3lVO9jsSCVGJjfsCDp/qAqYzKQTdaptb'
        b'vTINeXUthRXIxaH6YPdd+O/+6QtdNqBtYFBpoKKmpkYYZmUlCZeqFhCFGjV5FAWgkBcfOq5s9WF2/Y3f6/G06PAvaoGDhxXV63aOSlj7eckw9uKdcJwmE49OoLAmOBeo'
        b'y9qeGJsF/KJ3A5AijnFOlGEyrU1Ymbwx/sowmAvJmAt9ZPCcNFFn2DIx1ftjXTYpTXhP7JYLybpWHzYk2RTHFsYGtyfFGspy/CPsiuGNchxb+Pre2MLoz8cD8CzD1Mkh'
        b'SY5bnfSy96EpiKsPl6fOhxUYH5bY6TA0uv0wMRwlZQ22pcEYHKUx1rQLbWjcbgC7yF3MMsUkplbCsGHyUuMaqWfrpsCL/xdzOr5OM5hh8L5weJgWI8oTY9QGKaU00jzV'
        b'epsBHcSBM5Q8JLdnTW0PTFIANLCDc+OnzX7hLmd5kO5HqNjLwUEjQ1MVxEsHjdF3YV9izz8zqFWr5LQ7UxzIwrSQVAoDPwbRE1GVtqUN7SrLTCOXc4kNol3brP6o2xlh'
        b'0X/JsDTGEkHNaglo0RhbBLUYl0pycoiFxBFD5pC1zkx8ShucFSmMeqWgNijAscG5wVyYoRgnnm5d4UqNSqWXzyrtBgNjqAcKWgKcjjTACQHIgsCoRGP+4BfaFhYaJLRB'
        b'prRJFgJmltLPC4PcOJtw+VqscFRu21D/2URI6HHFIWmw15inKvTf2VK9whN1+D0Bd4vSLLfWAurvwK/di2ZfuaCsqjKagO/IHyzAqwS3Ww+97XYzbWw3RmAxELiYWfvF'
        b'phPrLuxc8xmklQpwIBGr7ZmK7I3rqssWzqYsgJbkNlX7yP8lOlxBsBDpXN3MdcqFWCX2LNaHUTEYIbSnUlO6vK7s0iDkgsVYp3vi5g93H/oXDwqMz9MgKNeFgXzFO9Tb'
        b'BvJTBJIVzv31TMub7jtEQOnFvhxqFNNTwAT2m5m6AyGhvLIjDOikbFovbM0GNFTabwkK7DyTYSFJ3HqR53zJl3D+TSM5xoxdwumaUagdTjrfX1BA0aFDF8y+/NLcL3AI'
        b'mBbgGsVTZydcPiqsrtGXSNQMWEJLa4BGMWqSW5ta/MyiFdUFSTgYNa1G0b3O4WPwjsaZPhHqVn53g2ZlK3wyzmQoLZPBshl1bwivTyXeVD7fnkDzwhoWtc31eNs8gfra'
        b'agUFZ8zOEiem1uBK4T+0IIn5sEG4HCT8AFB8nuYKUXjSX4Z5EPWdRuNO90A2AVov4pswHzABAWlK51CTE11OsHQ/lrbK5g6bbOmwMwZDRwKsgQTS+Py8AzUyHFlcR2LQ'
        b'ppw28gUTYYatcMbukm0dib4cStsh/YScAG+Nuq1Y96qWrm0JOoKAoWZyjZzyFpYtO/pyWVzLO1CSM+i8jVemyIlBZxuPd0Enqwfuc4IOuGLZFh2qQJmyM2jBMmWxwwat'
        b'cLJW0JfwHjWtWZ34HjU/ZEvQFEwM2gFPsDXgNaHBIadsNkN5dqUFc0FrzbQxUyvPoIXFGZyDhWdwxj8IZfz65b8u+HJ6KTFFzopTp06liYuKboAo/EJGUvK5UX5m1HJZ'
        b'c6tSDwCJL3MJUZPPs9q9hv2sdSUyJXk7abN6630ePwNUTdXKinqfP5qGierWQDMBOHcNwK/GqBUf1jX7APtVmlt9MhMd3IyrVar1eL1R6erLm/1Rad7s0oVRaQndV86+'
        b'eqEria1wkoNLVIBE9igmf2AtYM8J2AD3Sk/9ipVQNGuNHTO4vdAcj34PhC9UYVI80IqouYaxWWy+1iY3fcG0biW8h6eeNQF6/A/jVycwXUrSkZ5l0q0uOT1QpoN0L5PJ'
        b'lMKqE8uSzskj8yx0BiL0J44eC5LJNh1uN8d5NNqCgz6ZNl1cNT0yZOgkW8N13V8kDOpP4mqkgsplIcKheVFAJCoLT1krMm/W6/41stA6g5fNQT6D6Q1KsgWhXMCk81DN'
        b'XUhqUeelWmm12c5mz6xW0Co5d3Rz3cRc1AHLJQ8J/tYmxQ6zfLbwuxhsF5fk5o0oHNoN34ppcSGIIoMpZwf0hbEMdFOpOoO1N4PrNJYa3QMFhVg3amgzNt9AGmJs+uiJ'
        b'PRlJnSnEXSEVDPUX0L6pBDr7D1hCEvEGYGJIkzsqQk+jTlrl9UDH1zZ7mxUdmrPCDfqOpFadp3W8KyZeeSfWyh/Dp16TwcRCD0pkx4fSAh0W68US6nsHiaYNUKxs53tF'
        b'BTfyOshXnuT1auJ4CN/TFVMnN+FGKGe4KcZNSLZYpUxnej6FT8zXbtF2+hNatBPqtlUiJ2i7+UH9tTDqr8XQAlLsEisrK1GjSySDvpQ5ExZgvJxnyaBvufosviQj2TcH'
        b'kSevlr+ZlzveWNAPBq60/oh9l+jfAMjd1+s65i/82+K0Fel7fyrflffRuZz0VYt35O6vOT1rXMR8esb10Ve/nPTaa0vfvLLxzR9+O2jiB89+8+PzN5y//6/nvq78029b'
        b'7lr7yalvnZ9+WZd+2bwVkRszIqum5g17vHxeQ2TXL6dc8lpTzdLC05teTjnWvvGNA6aaQyVpTz8+76PXLadz9g7/6o/Oo1WfJJ9rXT9h/5zTlz57af9fnjtd/fbgLR9O'
        b'WrVw8b1vfLby+vK6P2T95vmR79jfHBK8+3dvSsOuqdYevH7XzIf/MPbbW1/5oP7aR185enLOO+F5s/iSmh/1GfftV08enT2tpPr1U1UfTpjof6zkzvwtLz5Zc0SUlx3s'
        b'uOf2xat+/kb2pW8/f4/cVvHI7z1L7Jtc5WU/u/L2B/qX7n3yxruPjLn3+p9+U3Hyhfa5lWUPXJF6ouXNsyf/eN3bh175/ZON783ZVT1zy0HH+yObC26/8+3P81yjP8od'
        b'8eCovPcee2Xtq1f/uKbw9MGXx6xv+6Uy88WlW1NfqI2cGvrsDPfh68d+8tLzAxKnnw5WXfn79D8c9b6Y9uuNV179E/uJNyyPTF2YNObBPucW/KG5rPCRmrc++mP9Dc9l'
        b'7az7/dglt03Levf07K+urNm37Ksp66aNn/zJ88veGv3qqorP2h/1/HGZfO2ON08ObxxV+j7/wdNbx7Y9+fqmVerjv/0tby9OuuWOq0fvL74l1PTOL6/74YJ2+Z2P1+xa'
        b'9snn05Y89N7tb/5i13utj5Zurf34hZLVC2ed2fPq3DeW3b3xD28feWDPt5eMu3aL708D0+/91XzvxMatxzM8215v+mjCn0b2qX5t4fIdA77adjrto6XL8orPF4y96icL'
        b'ns95/Ik/LbqK33fgdx/d8fq6W96a+tHkaw4dX9b21gcTWr5y1j6fsHDzjiXDPWtNP8n53QvzM5feMuKxV1/59KmPh83/9ldHDvaVP5u+2fdCwp/PJwTrH37thTdeSmz/'
        b'2ed7xj6n/urP7UtOHG1dW35u/Nevf/nL5iF/rz6d39gR+uSVv338XydfaXw+77b7zj93a7706bad6+6vOP7j68a9u6B/ypaqb9sq/Stsp4aP/XHSob9bfjN+rH/Pn/o0'
        b'fPWnjb9+6NSZfcu+Cf/qpS+jD/xk9b5N3l9+kfbOL74oHd/oSty96uzo1++pfviez3acOvFQ2m5n9oB7AiOPvLoi0j7n1WPHfy6ff+z8uspHy+57X95d8DfTcyf3vnHu'
        b'Ddd7bc8umjP03utHrdNshXs+/HhpdOHyL5+s3f3IRzd8++2W1fIzo/eOrtr5xbDDH09c8tvA1iePNrkWHPvBu1Pv+qT1vh2rnvr6/KJDX6+2v3Pjzml/t7ryjj6XP8yV'
        b'QEFztXu17X3RU2eZumnE3CLtlHpYi3BcqnqrqD6uPlHHXNJvK0igUIOVxWpoRQGaaB8X1B156nZWxuZBBXEhtYdCVoyqTSG1tQPq3cwJ0Kncgu5Kku6RUqlZ93Gp3j1Q'
        b'fYjEq8dtZFH86FXFApekPie6p48JjIUcE7Vj6iPYCDR1NHQjkb4tKypRtzC3VtrWEi00oxjO20l2SQtpj9GX6mPqHm1bXP1l8yuKtM2uVdqWgPajC+TXP6iwc9pt6m3k'
        b'GnqSdgiGhCkZLNdCvWoZlE8KoK+sxsn5/hKKLbS1tTcRuRqugVpWa7tt6hPaY9q+AHJ1r5+v3nYhW3dkvsHUldWN5ChpprZf2wTQ+ir1oAGs1YPa3YCIfa+j4aIX1/h/'
        b'YWH/r1xcg9jh/e9+MbhT3uZqWQ8niXgOV20mG/7v8fe+NMBpc6IOtMj+p9oAKbYIfHoq3KcJfP7lAp+dgeLwwYV5k/v3c5oyZ0iCwGfy47wCP6wVclklEpfnJeM1l679'
        b'B+I11URXKC3ThnfJIl7TTRfeO6zGE/w/uD+mMhz03klXKHNYswNR9/MS5MD2Zg4S+BzImWkBZJ3KyqE6hl2D1+wxeC2oVP4jJk+75f8v+l4unXg5jtZyTjel4Q6u6d0r'
        b'BCLO6k1mDFLCXA1WzVMj6tZlVRbOmSUOUB+S6nNaXYJ/OCzOUelvFm/7qe/Nkcm3lpXteOb5c38+vSVt8t3vectP5px1PPvVwuSSgo07x3xc9vIB56d+X8fNXye2f3jv'
        b'X26cVCPy30x7eWXpZTPvuWVbyvT03Zf/dPMP/T/SikYvq7vxzCWhlxzHfvqXu8YP+6Zg19i0dWVP3fP6nHqPbXX+oGtPFlz+60NFf7hqi5B2+BvLAXvrf0wb8x+lD99i'
        b'Sz2qPPftE+kj/rKrWh3w80+fnlf7wK73F/6XVPjJ37cWXPFp/sKyyBv33bJk1r6C1lsKHtlz7rmkrOPHnjx6+/T7fn62sf7zyKavK8Yc2+F5s/r9D1/78xfPDByZ8Nq7'
        b'x+dantnx4evv/2zPi0ve2/LasUXVdyuflF/732O3XfnGyr33Xv96tnfO67u9w19f6q1tbJp29N4H6j5764p3FpW+PfCmaORYSuP4VVcdKXzhuP+vH77xWNXil9qn/OKy'
        b'B/60rOCPUydtP/PTfp/N3Xr4gecX/te5QPH53/zk5pLipMOetXOHvOjau+Tlw41rZ3XUjZ72+vDtR48Xf7Xg8+vO7jkydd+vNr4/5anmj/cUv/hU2zO/6Jv3l6ETv3q7'
        b'MnjfI/WLf/OLa0Ov/fbcrjknHnha+cHEv96zff9TH68+8XLeXR8svmaQ6Yvjq05sG1b3+TelX+a843sq7dzk//5gzR83fjh12YwZ6o0vnr895AhKLwwOTbHnH9w0YOHl'
        b'sxNbx/xiVkJT4BezkzocI0+XfDVSzTy3610utKvm1iH935MOTdD6f3D1u8LOJ9WxvuTfta09ZG74evuyc5Hnfusa2DF02oa3Ph/42/ff+NWRxa5phGfUzlK364tqk7ax'
        b'CFdVrnoCltWV4iXaA3COIq19tfaYEzMZWIG61SLmcynqM6J6R7H2MIuGGRmj7ZG1Oy6IaTlZ28BiVh6evrJQfbjIPF99CM7YG/nl2tFqCpJ3lXb7gsKK4gJ1g/o4+k/S'
        b'tlLEuk0V2kYLN2iBKVWLqDdR4M75Qe0+cuw9UXsq3re37thbvbOMWqudhPvDFZBR2+TCfIXqKfUOM5c0XmxU79b9BJ/MLddOVWobR8zVNkNT52LAn8faKRZf+2xtQ4W2'
        b'JV8YnMoJPn4aNGg/+wjwij6F6g3a7egvvMrEmWcITo+LhRA6BWO4Udt4XQnUl1/Mc+Y1wiXaqXpy5piZqR6rQGTPVQbIh1V9Tn1Su11QQ9qTlgAKMdaZ8gBdLOKuWMYJ'
        b'QX66dmopjdmcMQPUB7UNRdzyWZygHuMXatvVY9SSVu3mqgr1Li7e45S6YxY1P8XNghZy6iH1Nk7o4EunT2AufXZo+zK1jVUlvKDdDwVu4OdoO6oDKNEZsboUagoD8lYw'
        b'V9sBnYcxP6TunUeo2NAxpllauI3G9rqB6p0JlcWXDimoKLbnaxvURzAEabb6rKTuLtQeZOP/bIL2CDnygqFAF14VgJb2XblaOyGNmqCepK7NqlafhcEv57VtudCUXXyp'
        b'dvdg6tpadR/Ghg6PsMCYwqvD/GJts3qIuqbtbF2nbQR0TtS2ZHPCD/gZy5IpUCN88xQOMUJGmBuXmUtQbxS042nafdoWFsuxHFDF3erGqqrissJy9IpWpO3nUieL0G+Y'
        b'DoZO36w+Y69gkWGrKqGYRO2wmXOuE2epd46kIdR2ao9OhXabOX5BgnYCMf1n1SPUbpv2zPxJ6h1dor2uVG+hd5O0u4ea5mob1ftxjHlOquHVU5NqKUb27I6cCvXxtmJX'
        b'OXxlXiBk1LLgK5MHzmNLuAzXTIK6S1BPqke1w+qRRtq46uYRY2AyO7VH0bX9ViAy1ovaDUsBBe/PxmVnWkVZUVkxNUu7tQV95G0QK7PUbdSh3DHacfXOPhUUL1aSePUe'
        b'ba92nJBnba+6XtvJ+jMfxtxVJmmb1G1cqnaHqJ6s1rYxMmbvNPWewjL1SL5rRHnRzHkcl6TdK6o3JFhoxqqrRmmbFlQUzi2DTZbNqwfUncuYb6uby7Q7KwHP3liAJlvw'
        b'9gpefVq9ZyoNinqr31lYbuL4Cu1x9UectqthFU3iNAASz8DqxrWFDiphYILCNO1+bQ9QJQfY+umvHhxOe5FiXkrJvLpbPTKFNulkdaf6UAWQSWNH85xF26be9gPBvEB9'
        b'iHriLkno9DlZZtK2qAfI62RROlsct2l3whIzfD6WmdSDQ3Wnj7dfRjOWM2UFuvDZpPuB03atljinul+8rOoSFmB3e0t5vB9Q5gV0AkzqSfXBCQThtO127WQXF5yQbbp2'
        b'iLngBEpudwB51lXaYysQnBTDNimACQLyaRsAkHk4KuqG5dCEYvUBiZuvPmjRblyZS9MZUO/U1ifAyEVa8NMKXFXp2h6LekjUfgSt3UeAQHt6jvZUgrZlRHF5ZSsJOLXj'
        b'WsT2g6p5mH/sNeaySWsZYXlf0yAiX0vmzi/hoScHBSAyn9ZOAOy9kWY4WdvTTg5q8czADXlMaCnVjolr2HDuLFH3FWpb5mlbK4pcxeWmwUlcWo6IPkhhIhGMeCY0V+Bm'
        b'hdGIlBWVD18yAqoyc0WcSbtL3bqYNkHaJert+um1ucoFlJ66Gc4mLmOotmOFJLqr2Sa4d9xA9GVcVUXHigWa8piQPU87rG1rpqGZAq1+EJaFC6Ziy7w2XI8AredZuCzt'
        b'mLREi+TQ9M5Vd9dBg7SjWFJVsZDTBuQ4nIAHxiXQ+klXn1Hv05DY3qgfXlIxD7N493VUyTX5k7ClI9yj4KwzzjlsbL88SV2fp+6g1VulhtUTFZer68vmF8y3cGZJsKq7'
        b'tJtoyArHAgTfqHe0GEZUu09QD10Dq+dJLfKdlKEM37/j/w2Iqn+7S0xeTATeA3DhEgTByl/4ZxeSTRLJNzKBQAKEnf0XJB5zO1keXerByD47UxkU7PodlABIvpXKTifD'
        b'4M4/B5VMechaRBJYefBcMItrfsB1/xti5hmnm+k2oLaH3xNobXG7O13aGaIClY/vKd4w4uOvvTvnpJxdVBsS4T86AEHFAv9puNZwMt8Af5FF4UWoehYZDr8C/ArwK8Jv'
        b'BvxK8HtVeFE9B7/28CI0nYsMxPwNmJMP8aFFhrJcB4eKcl6xSYokNZk6+CZzh9Bk6UDBoEW2ea1Ntg6J7u1ee1NCh4nuE7yOpsQOM907vM6mpA4Lih0DyVB6H/hNgd80'
        b'+E2F3xz4TYNfeI8C1MigIBdOgt+kIDnPiSQE0R85H0mGfOnwmwq/feDXCb8Z8DsUNbnh1xKUIoNlS6SvLEYy5cRIluyM9JOTIv3l5MgAOaXDKqd22OS0SHZQlLlwFmqL'
        b'R4bI6RGX3CdSImdEquS+kflyZuRyOSsyR86OlMn9IgVy/0iRPCBSKOdE8uWBkVI5NzJKHhSZJA+OTJOHRKbLeZEJ8tDIGHlYZKw8PDJVzo/MkF2RcXJBZIpcGBkvF0Um'
        b'y8WRiXJJZLQ8InKJPDJSIV8SGSGPipTLoyML5DGRufLYyGx5XORSeXykWJ4QuUKeGLlSnhSpDNvXc5E8eXJkZqAv3KXIUyLz5KmRy+RpkYXy9MhImY/MClrgTW5YCFqD'
        b'tjocpfSQM9Q3NDA0v06SZ8iXwvzZg/aIg5RZOl2xOkNJofRQBuTMDGWFskP9QjnwzaDQ8FBJaERoZOjS0OxQaWhuqDxUEVoQWhi6CtbDIHlmrDxr2Bm2hl3rhYgtxAKt'
        b's3IdVHJyKCWUGuqjlz4Ayh4cGhoaFnKFCkJFoVGh0aExobGhcaHxoQmhiaFJocmhKaGpoWmh6aEZoZmhWVBzWWheqArqLJEvi9VpgjpNVKcZ6mM1YfnDQoXwxZxQWV2C'
        b'PCuWOzEkkr/7RMiXGkrTW5MbyoOWDIeWXAY1VIYur0uTZxvfdCSEncEEqmEYfZsAtSTSeGbCCPWHr4fQ9/nwfWGoOHQJtLeUyrkidGVdllwaq12EtopUkrTOjvPY4QgP'
        b'DTvCBWFH0BEuWy+g2gY9KaInRezJOkcwgRQ35jBH+iQkZAr9CDN6V1jD85fZGIW5Vl7JDqALDa6BN1S/dVPcs32G+vNdufVMk7Q6t6a13huo97kEpRVhEUnsUF7ZqwMo'
        b'd52POG+ol7bJpNvBciQ6Vk4bNiwuCcDeCk+gTkHLCatnTS0p0pCtNgrEm+uiDkOZiJSIeHTl0QRwEu7s6F+6qUXx+P2QEr3NK9CYF1XOKLbCGezyGdL4wHadQdHiGdTD'
        b'OcMZOtTNsgegLXlUQP3zqNjS3BK1Q+myp64aLRusdW4maWXGg50eF2IQOmquo3KiCbXN7mplBQW1xMic7sbVzT7v2tgjOzzyscKiDrj3B6p1j5VWSNV5q1f4oxa4o8Js'
        b'dOPzB/z0lrTmqYa2aqUzgWq5mKLv6MZJTxU/qTv4mqkcL0xgdQ37QPF42tCLOCZQm4ESplqvp1qJmr3VMMGXRMWa+hWka47eXVjAiagdYySze6bg87w+yQGlutaDkQ/d'
        b'bshe42YTaYE7VE+ISm7FUxd1uuV6f3WN1+Oura5dyTSJYWHIzP0YMhPOCvmubrHncBIRuWKungQWzQZVqNBREjo1RfH/LBSxC2Q1KqwHqnlVdtDw9NCz0uA/dHyEi/P9'
        b'mO6Zjhs42KLt0kZUMjMbbXwG3oYtAOkcsLGysCVBHmCQUId2FjkyRZAh6wsxnEuKX1JQCttbOeWmsKPDFBTCCY2CMhfuzb58SnHKdWFHAtdhCnNMUSxsD6fCGyf03dEX'
        b'x8IctkB6wHohaA73gRoF3w+DgrINnuWEM+rQJcwOVO6CetKgnocpdyZ83R9L862B5wPDKZTv/XAKwB0LGahldlghpyWcDjklOCtgrNejFczpoAQnCE/lmVu521Dx1wxf'
        b'2ajcfpDLcCFjhxL0L4M2uLPjHUXbgfQCjvU/zFMZ6+DbpHBigmEiJ4aT6W1iJjq6BSpR5oIJ+C4oALxN7Msx2y1y0GljXvdjinQ0nlDmPpgHezgbahdwXIKmdLRcyWTj'
        b'AO+foBb3NUZCdw1mrBfH/6Zo5P8+p/p7MbNxVX+Kq72SwLOT4a6CYY1lFqyk9ZMKf8kiCwDE9IBY+B8zYLuZvCQ6BSdgvv3xO9FOwYKcQpfNkqKfP7RZXhP0zeKEqXbp'
        b'myU9frPAWxEnLyzBGTWyy/bBySuEbyS6w4VvCkr+DylQvDmMfxkw6SLq3wUtyk1BC5nhWINQG1s8sF2yp3A+OdwvPCQ8DDZBVp0J/RrB8r28wx5G3TU7lJoQtIf7waZ8'
        b'HRZeUgKXhQezCPdOvA86aNtBOcEEQBGT9AVMGn3sXdA+hVu13ecL54UTw/1kPjwE/g+D/wPD+XV8OAXrCQ/EzZUOKCY8zw7z4eRwMqJm9Rba3CZcxLCZUoJW6E0iLHj4'
        b'DcLWCDszuQ5nOBUQAnzi7MvBtkkkRCEBviqiQFhrqAS4J5tSM+pBdZh8H8FTc7gAyk0KJoUzKQ8ABWhxUjiXUrl6Ko9SeXpqKKWG6qkcSuXoqWyjrZTqR6l+emoIpYbo'
        b'qWGUGqan+lOqv54aTKnBemoApQboqUGUGqSnBsbGDlNZlMrCVF0SHBDFiOIHuS0IOhEQQF/Dw8OJ0OPkYPJtgv+BoERXC15pvfTF9QJlwPjXoa9svTd9OTQShDFNw3UG'
        b'pYrk3kDC0UcATs8LgxI+D0pG8JROP9gp/0f2rqvk3wB+/M/DKBectP4NnTAKNRAFq+4E2iw6CVqlSmSRjH/nJCu+RU+j6WhVaTaiGaP7aMfXkgNtltGFlUPIEO0AvZx8'
        b'r3+fSqkOMZlPFa0ocv27ZHKISO93gW+GZRfBN+bRESAYEM9hqw7fzGEuDr6JYRMd6oC2hG2A9gNcY9reXQ6jHnGVf4GPfhrSnWbDup8NqYgD0q1TVqNTz2CnJNgkiIEI'
        b'AJZTWUfWkyInYAMm6GQyurCk51KQckIXE8NmPKFhKJIAUCUi2MYUqrGH7VtH8lhqQjgVNyEOFgEx0QRANmwbD4jglO4K7BviFdgBCAI4BYAv6vfJUAopY2NsHiov5nnl'
        b'IoOa9j+7nn9kNng4tJLRykmy2Pn+Ilr3lIi4wuxdV5g9fjLaEN0E1DCchKhwbDIkfTLyaTL6AIIm+ovoDaYzME1e5GfBqnOg2S+9s2/No6FDo3hLJlkXYKqHgW/rMvCA'
        b'8oUtWWjyKsF50xIU/fsMRJzHGiVAK/F0Nil/xKCMCGfhXDPB+QOT3WFptyNLguz3UiUuwK19yygbQ0rSF5n4/arDRKA7Q8lAnKeH+tZZ9Mgw1rg6rAj1b8OeJ+Iz42t2'
        b'JgKmYasTGlkrTXiNlW5Ddgh9WQNfwjN4Y4t9GWsDIK/jYtYzPZrpxJzSxkIZIqUC3YUhp5gJ6DoCg9mgs8bmIsRa2wxXKKUGD1AI1Ci/QvryXf57e+yIOuv97uaaOvdq'
        b'BRWxlc/NMfsZSXdmyCApTyT8PxUtI+vf6Uj4CXZwVtwWSoargw4HVFEfBqDfjD5yBDwi7KKdYosA8mpziJkWfJpqceps3lTelcm4Etdj6RRhQvSv9Sv/ic9+gpfn8fIC'
        b'05NGPzV+5adkFNDura9Rfka3TdWBlcqLZHsNN55qDF+gvESGLvWykkeFAsUeFatrgNZfWe1HC+2oRfe8FLX4jZsV3uaaaq/flfivGTLX4n8DPv3/v/wzgg1ckx1InkVx'
        b'nQuCdKFQw2nKJOEDChq6Cz2suluN7n+OHp/+839m/X8sbXaIqRZJnDcW915dA15zHZI4sj/eTbkM96VgNRNhKQjUz0o0ojnOUegCdzzXz+3Wd2RTdQtsy4CihHlmuUue'
        b'CJgU5TTtu9lraj0t6JxYQbksylRqq1v9Hrc7mu52+1tbiFuIrDU0UoGnCe7OhPJRV7cScSauU5qa5VavB33qsTiwEgCWZAFQpp4kO0H96WAMo+uMqRr+Lz/CVPc='
    ))))
