
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
        b'eJzcvQdclEcaOPy2LSxLERERLGtnYXdBsSBYoxjqYsOusLC7sJQFtiDgoiDo0sWOxt67WLCXZOZyMYnJpdxdEi53F3O5RI3Xkmvxkst/Zt7dZReImnz3/77f75Of775l'
        b'+jx9nmfmD5TbP3/0fzr6b65CFy21lNJ6L6W1XB6jY3Wcjq5hauilghxqqVAr0AprKY1IK9KK0a+43NcisohrqBqaphZRxqkcpfPKl5jKaGqphKYqhmm9dJIMb60EXaXk'
        b'3odcfXWSdfQiagml9dJ6LZUskyymjMxi9DSf8sqRS58MlCzI1cnmlFtyi4yy2QajRZedKyvWZOdrcnSShyLUyIdifGHQpZNWZdOOfrDov8Txa1agi53S01pay9SKK+k6'
        b'qoaqZCqENrqGmk/ZmBqKptbQa3C96NmrVs6qs50DgquYiP73xQVxZFDmU/Ih6k7qa/x5QQGuvp4WUOhX9tf5+pT8mLHUF3zev07r0R5STBRuD2On7KyedbWJfv42OQv0'
        b'bBOntirRfXz22vlKuB00amDrAlinWAjrYGPk3IQFCeGwGTbJYT1sYqlZ6UJ4TsUZHnx2XmCOQNn+PnrWl5mPMgv0jzPvfq7YrJ8brknQPM68lxWYnasvYC6sGxCzjFq3'
        b'QmQ258kZywiUA54EJ0Z7o0IjcJGpVmU4bIiEB+E6hhoCLnLwnA1usgxGCctGga2gEWyEG5NROtAMNooo3wAj2MsOhlv0Jyg528mEyU14ePiLF7o88Z+sNxVV6IwyPT/r'
        b'Uzt9NWazzmTJyLIaCiwGI55ysxCPxQAp7UubpM6sqDxObzVmd4oyMkxWY0ZGp3dGRnaBTmO0FmdkyFm3mvBFTpt88L03vuBCQnDBvrjgB/6MkGZoIblaR6I382HD5GSF'
        b'Sq0MB/VpZEDhDtDqGFRFtACekICWAtwKc+zr9D0BFfPJ9Eqpv2bL5HsUAZWqOZbZvxE88Kcyq7NWrtbIHaDyyTTydWxlPv1LhvKfrtas/tuIfD7LKyEshWeZMmkVLQPn'
        b'8i9T00QUaqx/O2OQbpMzlDUSvQT14AS87g2OK1CD6uDG+VHz+NkPU8EtoEMZBusiwxNTaWr5MnFKVoSctg5FucRL4GZv1CO4B25KVkrCYAM4B45zVAi4xYFd4Ppy6xBc'
        b'9u1RQXgWI1Gv8a+IQr2/6p3GwM2gCuyw4pmWww1jQWNBfPe5RhN9Dm6Ts1YMsdlFiclKeVKqgBLq4M35TJAtwjoQw1M1bINHk8mgJiYqGSoINniDNgYelxVYZbgF++CF'
        b'gbAxDTYkpaoGw/WwPgWc4qgAUMPCKnCgEJWPy6HBhXHJ8CI4nahIVBLQFFC+sIFVgx1h1kBczpk8eC45X4m+CyiOo8G+SeHWQfjDlSV5PDCnJvaFe2GzPBEVD7ew4Hpo'
        b'CRosnEYKb4EzyWOjE2Fz8jRwGLakoUL8hrJxoAkeQ2kw8MjSjDhFYuqMJfx3X3iWHQNugdNyhow4bK0EG70T0CwVw0bYBGrKk3GHA+FuFh4Fx+AJK0YwmRDu9YYtkcok'
        b'tRUnS4QdsD4tBaccr5i6TJgYDvY6+pwPWsBu2KhQw5ZEhUpIgY0Gb3CRgRfhKSNpdgY4h7rWkoLmRRELtsqVSQKq72AWboFH4RnSpgi4bVJymjIxAo1/faIiKRLsiVMl'
        b'pAopBSWAO+FOGaloJTw2D7clAn1S0RTYBi56w4MMvLIcnLaGY2CCxyKTSYrEVNgyJywZwVULwpKNUnBo/hylkJrJCWEVrAYdpI8L4B0GpUbdmhuWkAJb1Clp6XOUcCts'
        b'QBXHCuLhabDHRfcYd1rcRoi6nUaElLVzdoFdaBfZxXYvu8TubZfafey+dj+7v72PPcDe1x5o72cPsve3B9sH2EPsofaB9kH2wfYhdpl9qH2Yfbh9hH2kfZR9tD3MLreH'
        b'2yPsCrvSrrJH2qPsY+xj7dH2cfbx9gn6iQ5iTdVxiFjTiFhThFjThFgjct0bsfZzUBRPYl2lJuQEXswCJz3pCdj/gjs5AbUZPGxeBNVmgn9qpXyWTAnqMGoFZLLgbHA8'
        b'AWt4IS0SNiK4BGeFLMWspafnT7QG46zX4EuGCLhjOTihSEAQD2ppWBMH71gH4I/rwGWwP0KuBFdZWIdgVQhOMhErwA2SdUksgsZGETgK6xVourlEGkHxVviStR/6qIwG'
        b'15NXgiMID/E3LxocWdLH2h99SUJIcgM2RsgiE2AzIl4JNGr+qTKSC2yaMjFCJYcn4TWGYsBleqkVVJNcYD/lkwxOKhA8HExEkCIsYMLgZTX55q32Sl7IwAaIKAuqazgN'
        b'zsBLkG/kIHgNkS4McmCfmkZlttApcD/qH/44AzXlBAbIenl8moKmhBOY/nAvuERKhWdCpkQkIejcNSg5DXV9OuML94Bt/LctC1JIoUOzw5QoXxkzBqyDtYSErV4Rlwxb'
        b'wgrBFdQFIz0V1LxoDcJ5NoGWqYjeJoFj/XFD2ujZsCWU0AQWXAFXCGIEj5djFBaDOwyww+uVJGc6uIK+NaYqwNFFCNBt9DSwCdaQTyFGcBCcgg0KBTyCPoGL9AK4Q04K'
        b'BcfAHbg/WaE2wjsYyzhKGMJIUM5jZKjnwKujYGMCHirUaqaSni2DW3gSeD0uFFFS1aKxuJkN9Ivg0BwCZsvBviBER3BhEapEuRg2JasFVP9cbiwLNhCAgbtmwX3JEbAh'
        b'WAjOJeHp9RIyYFupIptxQDzXQ9ZBko6ddsk6TB2SbipZhD4MQR+WoA+zhnWgT053WYfpgT6s2jB94EzaPAW9eDxS3++NV3womZSZfvxXP/tm4MvHQHriB3+FH35as1wc'
        b'JgEbDuYa4IbCX584/eftO2pv/v77UAAm+90L9A2PeyAXWYbj8WhRwk1wHWJkRE6BzWly2JzIs6+gkRw7BNYRUQbUW8CR7rLMqjWYw/nCRssolGRREWgjeKpIRYBV35Vs'
        b'CNiEJrmaQ0CyeYUFk1wkFtkRwqPEaYgCIhKOUklgK7hTjGYZ7IdXSZ2wLVjkSJOiQhwec95G2O7LskNZcNmCgXwqaviuCGVC4upxmKeJ4SUG1BaDQ6SWilngEGmQg/wj'
        b'2g+aVwzB5YwMF6TpAh1CUzexiLwlQlEnV6gx5zMuqWiNmOb/fGkJberjEru4TlZrtnSyZlO2CSc0YdInZ9wkLcYUgO/7Oksmmde6Cq7xELcIQu2dtAQ2psOdqQgkhRSn'
        b'QHivjOtdqlbxkMbomeeUqXvAWU+ZGsFZkriDNuNxbJkd+yWShx9k3s16nJmQnac/ekbLXagZEBNNxf6KO+4bieRiTDimFIUmK8IQ4UsGN6NphOenmPJ4cNQSir7FmPWT'
        b'BvWUhdnBi2byY8j0PgFWi6GgS95dS4n9aVMg1SXvskVZeT8w5rSpn2u4cZY6XAxW86gq6omv+4ATGtwBT4H6iL4SIjkhSmuiwZ0VK10jTjv+z3c2xoZHMldOq/mmOGrz'
        b'8my/r7EooyhLbzVnayyGImMTzkyoBWMNw7Pc8EI2pn54WNKSIpRqtQIJg2dxC+BGlooAFwVwVw488IxW5DyjFV7OJuha3RpAUGwXkvbaEEHElcPbM9QYiwJgDQtuWWBL'
        b'7+A2FoMbjQEOqXHcc4JcrjvI0b2CnKArgZOQDnHVRwipnXPV9yxSWtu9Pv/eQHz9YIPAnIRe7OIGnvrsUebjzAeZj7Kl+kxNmObu5+EXMrVVm47rMrXHAx5lntXk6k/r'
        b'jmtys6Q5dVrE2JduiN0g3jD5qFgW11YdzVIg0Ee3TCinLTI8sPVwu8EMziTAdXCHGukfjintA1tZ0C6UoJkiQMp1Jz7dEECQka0p4DFAymNAEIOIjz8iQhUh5lyD3pKh'
        b'M5mKTKrJBUUopXmqimRw0iVOY8oxdwrzV+FfNzzpoQoyJsziTCEujMHUdbsbxjwOcMcYLIzCWnAHnEKyNawDW1JSIpAcx2vCm8FF1N36NDVSusFlpH81iuZNokDDNC94'
        b'JT3UMHrDBwKzHBXwxzP5+Tm5OQU56my1JkWTd/+47kHmyfcKNQ+QNi7Rf5IionTtwrMfWZyw/Vwj5u02Ku6Uo5+/0BTaRTl41fcpI+KuHON8W90G488eg0E4WgcHTpCx'
        b'6BoIhgoF1+E+lkNq6ZjecamHgeZHEu6eAgKnXmB41GcZbcZKhiHgvWQ0mnU5CZoPO7jNTXLZhL5t2j9nisng5nwoXLvQLOcIwK4F7dmE2aoVSjVPnvuAS95wDwta4GVw'
        b'yoK5DDybgvQSzFJVyrCwJKUKtKShPm+MSARnwngOvThDBDrEetAAtlhGoyzjwF64gRQMdsJT3RKHwG0cksPXQTsRRuBl2KonxcuTUtSpSUgtwrIBvMiKqBHDBYOWwTvu'
        b'oOA26T5WY3auxmDUaTN0Zdnu6DJESPN/poFdk9/JolRuk087p3yQa8px6r1uU/6ZtPuUS+XgEtIZkTycgHC7KTkVzTtC+JWThNTICkHayvGumXJOeX83ckaUt+cmnx4T'
        b'zzn+e068WF2AuzxomJdYO5uS6da+VV6gOhf955kT/PTThBQRm+EOFTgSodTCm4nYLEIhBfcgDTqWgHpiuek/6Cu/Om34EGbOJ/R/F0+fVclbXD5aRTOowrJMQ8XaOQgr'
        b'yMuv1/alMIi1JlUs/zq6kDKkv/EVay5Db943fpis0WqO647rTuc+yCzW1J05rnuUeVLzKNOoD593SvNGVoImT1/bMIZ5dVj4C3ltVY+0eTvzg/PbXq2OrR5XI25Ta0qp'
        b'99br7wfJpOtt/WLHp8Qrp086GhgkEhY8qhp7+p/SjpT1c2X/uC8d3/SKdPcA6rOwoatvDEeUF+MpOJ0KtySDPQvI1GAjhBi0MkWwBl7snXY8k6JwuRpzLoEpGQ9To8WI'
        b'BDv/iDyIoEJK7pB4MtiNyAzwJDK910/zyQjY4cxH3cDuYw9Kg4nyCqT7XIaNSfBoAhINEST0Q+qnFd55isWV7mZxZZ4f1nC3pT1gTaom2iC8ATrmwS0s1v8MkVQkPKAn'
        b'sPHhCo4SK06z1PRM6YQRUh5gPlUgIIrxR63MVIhQI02YLvd26aQzDMMDtzPmDehhkrdReW+ML4jyn/Xuzo49P5Mff10QI+mfQA96qwFsClsXOuKYSdI4P7sxt3HR4wdr'
        b'1fESdlTB1fvWy3VNT5Z+tVW3PHJW3KtNcQHrPmoLPj1vZOMuL0HjknN/yvBWWfJ+pTtRav/u/jsK29Xr/1lU8Y+dfyk64/vKaH1ASUqC4t6GjonwL9Pu+g4dfG623JvQ'
        b'p3mwKYyXYcExWNtDV0IKzGkLFllGToXrzAq5HDakhPfLUSZaHewgfJkAyZThFmLWuLmoCF5UgzMWx0cfpNZ3wCp2HFg/gBch9oOzYFsPmRm92onk5vEKInNPk8dHqBDT'
        b'wRYyrOSDFka5FJwldmpwLA5e6F0jo1aDTUgfm5FlwXROkwTPRSQpER9vAIcTU5De6w3OM3APPAMukQTGYQBrxaBeoAiXq+BGBaynqGAZtxJsSCQ9nrqEt42mwabhSNer'
        b'58k7UukYcHk5uMoj5k5weCBSEJDU0ISVBIeGgASk0xai8rQmwmMRamXiVD80dgwlFbPitQs9RPqnqGrCYmtWgYEn/SN4NI1lkKIWQIh/IM2hK6+8SdCdBKGrlDbJ3FC1'
        b'nyeq9iIPdKkTON81Nyx93UN/I521jzZFhKX2RcpsA1JfhUg1bWdAFdwBt2ULHbiFVUJfJ26pWCzM2+gBVKWwTmQT1lE1TKXIJjKry31tbB5lE9bQleJFlDGQoyx0vsQU'
        b'Q1P4bwllDFqM5F+bGOe0CXEZkyktjfO20ibOJiheaqAqBWUHbYI8hOqzqBXblzOVXpUSXIvNq4Yx6Ul9HLo7axPmIUm6UlimR3ccSR1Y6V3HopTeNkbP2iQtNE2VbEXt'
        b'mEVySVErpXVepHXCshF1kjoxvq+hSU4xySl2y/n2IsomNX1VJ+VzONs7hyrRL6JaGeMIUqp3DYParqij66h8Ib5DrRFomRqaT91KG78l6WiLUM+QtAvrvB1pF9YxuGxX'
        b'yvdISiFJZasTOFKhO49Up7VsnkjLaQW1SE+cReEeVPpohXkim0+eGC/14QXASh+bD8rbrvWy+QRRlT52kd0bSW+sVoLyiW0szlfpi0bAt4bWivNxjb+z+Wq90cz4Goe5'
        b'3nPo/bdaKa4RvwnCXzmtT6WvjWllTLNRe2nSXsY0QutrQzn6IyKtZ1A6P6PMRtuYfBZ9m6z1w/eO92Ktv42/G+aWP1Pbh8/vSoNr87P5aQMm4l8flKbF5kuuftq+Nl+b'
        b'Dy4PfzP62vzwl+I2mw9+tvBz7I964Y96EYh6wZie2Pxx77QhaEwZ0xv8E8rzGbpD8KgNJe8/5Z/we9TLPtr+6JnSBq9nBlC2PqT9/qj2AXU+uIY8ic3f2QYb28qaZBba'
        b'5ldDr6ONYos3f+fQ8AaqFzwRFSDF2qgc84RRyFwckHFwQaIlY9U/B6HWCkklbaPzqE1MCYcVUock2SnOyDBqCnUZGXKmk1FFddKWburzE8nkAoPZkl1UWDz135RDfxZS'
        b'FQOzc3XZ+Uix6tK9uhI+YWVFpie04iFNSijSyyzlxTrZSLNHIwVO7Jc5GxmEF2ltmEUzZq4ONbiGdjRY39UsRBNHEEZZ+hSKaMI2uW+72vsQV/rETyMr1RRYdTLUorCR'
        b'ZjnhuE+CzboSq86YrZMZLLpC2UgD/jx6pHn0kz7kBb51veLIta9bSmfuJ16yQqvZIsvSyZ746QyWXJ0J9RgNBLo+xKTyCT36CT3siddI8zKVSrUCvcWyxZM+CllOkcU5'
        b'QrHoP+rheNyHCXxvu+6lnQKDUasr65QsxN2Ix1oeeoXaYu7ksouKyzu5fF05UnlRe4q0uk6vrHKLTmMyadCHvCKDsVNoMhcXGCydnElXbDJhrt7ptQBVTEqSB3R6ZRcZ'
        b'LViTMHWyqKRODgNHp5AMmrlTgNto7hSbrVn8nYB8wC8MFk1Wga6TNnSy6FOn0MwnoPM7xQZzhsVajD5yFrPF1MmV4itbaM5B2XEzOgUl1iKLTu7TqyD6Yy6ISyW6WKLY'
        b'CaBvUQ6/BorB7I+jMWP0pYUsZoc8YwxwyLK+dBAjIc+YZRJ2yQShpxAk2QbR/sJAwlDF6B7bQH1pfwbnl5L8vgxmq74MzoXeML6kvGB6ICorCDNdhl/utDOgFWtNqbBF'
        b'rUgSjQIHKN8MdhI4D1tcpnSxO3Y8QhfEw5iy39moPIpwpfcQD2MrORtrHljia0GCLP5vQHxvN1spsAlsjI2djPDINA9xRjpfiH4R/xhA5TGIZrIDiLMG4k0c4gcc5iBm'
        b'vY3LoSu5ssU2DpU+B/FgFvMXxBP31hHei/LjEgVaDpXC4if0y/FuHyUFPM8xndRyxae1mG8LbCJSm5D/vohC/Ia0gJTETOafOcczN5kq8UWckSF0TaBGaJ2Ap5HMJbZP'
        b'8Y9JzndygWkynmHWrLN0shqttlNoLdZqLDrTVPxV3CnCwFeoKe4Ua3V6jbXAgmAWv9Iasi2mF50Fdop1ZcW6bItOa0rG72bjzMJngJmbcRP7I2gznOUORpTNPIpAGYfg'
        b'AUOZPw8JGNYIfEnpYMYfPfsjiLBi60B/cANscKx8g/pIvE6X6g0P8AtrEeCKAG4HL8GNHuoIrhuLWKSuHsugFF4I1Xs7dR0b7dRo3NUjsROytOhSh+eZrkd8P48q9kdw'
        b'hjKZxiHI8EFvaMxNa2hvpPcQfkUcgRCNZuu88X09dmbhUCNw1RLUFKle7LJQetkYDEHdVSpMcbH5nxg3H+MGcDYsOFDlx8tWompZG+UQoNSVDCqCxQ2rofMRBcR3NtSM'
        b'StYYSBonRKCdgO/QG2YOEgPJm+A6LNggFNCjZwzuRPQKXkSVvWDD5cZWsjZSKkrbUCdEYMqi+jmjFN+j9+TJxpmKMQNCCITKsXGkjOJF2MdJhURQziLQM0gM/R2NhEua'
        b'qvBFAyXAzJn4NKG/SsEaAe/ThJADDVwLngm9nFYjCMP6bqeoVGMi5kk2B0ExIqSm/FWmOAxds3g47LJIpuILAduVBOx1JpNc/NyEsQtipRmEJBajigvNM1zwiqCUYTCU'
        b'SjENZBj0HMwQeGWkCI6DEbSG0BVRmuxsXbHF3MXutbrsIpPG4ml97aoAMa7luGrcD6fBkbzAUCf3/qkknu0U4WFDiMsXucLVPS9Xg2Jo59ISy1P8wYj6hgyoCPnhPjgl'
        b'i2W4OD2+l/wk/rPM1RyRo7LxtMN2QLGy4cSGkQ8aE5NT1GrlWnAiTC6kvFUMPAw2ST1sm16OXzMmVTpqKRL7ljJbRbw1A2G7WC/gUa2GXsqS98SzzEELvBAislqOfOXs'
        b'FEctFfDEtbOPw5tutqFAl1Kk0epMvS/gYnmDEBcB8bYQ6oUuzOaefxm397UOkZq4FsHtsB2c6/Iaga0sUvBPsmAd2OefEktcmxbGm/ESEXFk63IvgXVO80PHPIpaHiaC'
        b'+wPg1llwF+8OtQWeBFv5bGFhsCEyQQkbwIkFYUmpSHlXJSqTUmnK6AeP9fWaMhpcIA4pK21F85ULE2CTPHBuUmoKSo3qwF43KOk4sF04AjFowzRFOmvGYvXowV99mfl6'
        b'1nHdcc3drBRNgV6xXa5J0pzU+Ofk6guyHmeGh674NfXVzhmPQzb4/rrg8rBQ2b4jG2ZIFRng41feeeXje1tffe+V9+4F33t5p5D6sCxgevGncgGxaMA7sWhYGrGxQuA/'
        b'muIG0+AgaJxI7BCgVv1ihCrR0wgBDsITK6VGYoeA14qnwouwSYn9vUqUPuAob1wJsXJgw/TVpIJh4CRYF6FSJigZyhdeFILDTBRopSzDcP5G76hkVVKqIhE0O1fD0Wgm'
        b'CqiRLwqWghNwn9NW/Pxs0ifbpEOsOaOwSGst0BEDBdZJqLXoL4eYIhhe0pLSFUN6wKbKI7drXcesK9CjKyYCXTYLwQ/jJWPKw/f5zlaZDBgUMWJiKwRVhf72BrkZMZ7Z'
        b'kt5xZqoTZ9wZMo2QUeLCHcFTccdjnVBAuQmBLtzxVfN+QWc1U90xB9aAfTz2+Ff4WbHdE5wBVTOegTuFI3js2ToOXLTiJQ5wHV5MfwrmRIDbPPJ4TRGCDT+8MEt6o+9a'
        b'mO2k9d2XZcWTCzSFWVrN1NV4HnAp1gXosjpzkNnVWP3qYg8POLg5GZxJSAUtLl8NuM1juY0dG2AGW+YFwDMUOA039AFV8CLoIG6EgSPgIYebRxNsVGAbHbw4VET5zmPH'
        b'wNOwydUZAeW2/ErIIC/kMHhSXWSQrcOmIg5NJUumkiNTya7hfmjJ17s3MhiLse7m2oxkvJSi4pdJ5ydEYIendITESjlsSUlM75qy9bBDQIH9Ogm8DY8yxLK8PIlDEl1V'
        b'vHR6pnRSCkMRb2C4bQrc5VEocQiNlc+FdY6ldkzZCtd6BYvDeXDZ3mdscjJeyklMnRsG6xfx9G+uq+50bPGGB5bD8yJ4bobIEDP+K8qMMeo7/fhTloeZb2Q9yHxdrwqQ'
        b'azBBxERQYXqU+VbWG1lvZyVqNmtvV97NOqN7MP3TX0VR6XF0enTNAnv0Z/L2qK3tOnO/I1Fjq2RzNhypid9Njwh9vfW1QPqXv8Wk8jVEJD9iqF8tDL57ZJtcRGzDjBRs'
        b'9/DYWcV02aFN4BDv27MNnkX/u8ghpoU6RO54cgiOgfOksLIYeLA70UsUJMgIzYMbtCTRQHgCcSVi4m1Jcxi9waWJPvACGwxq4BlCfsEOWJWPVDuSCm6sBHURKsTeA9aw'
        b'sAkc0RIz8HBwu8KZBK/OeE+ElxYzsDkd1BOvnVBwpAgvnONF8zZ4xnPhHLSC+h9PgX3xknhGsQnp2FjZISQ4xEmC11Jihqi+HFJmA7ACixSUivE9yZ+uTJftIH5d4pNn'
        b'yTyuC3i5rEt8fdYCkGOdyMeVgVBoI7qsp53coor8fedOo61Y1AJHB8/sIhc/klhgD9/Nk+B5QTy8Nh10jAQnwK1EOTUMbgvMm0kVEBoQMID7e1Y6gqf7o79iLo/pG/g3'
        b'miwW/sGwk/4sTeNHTc8c+7HpcUglRV7X6r7ye4cO49cQg2/GHKEMEmajwHwQl7X4P/2a4nxhlHTmyI/+FplfrZgyfeO7cY9L/k69JSsrvjLq0K0F9GnVFPOeauqbhDkz'
        b'qyPDArWBH5+NGyNXyP494x+/KdSaKy5PHrT/vqH01PG5x1NCuJL2X+WGna2et/5T+7p3FseW1ry2Y23/DSLLb1bYB1/U/eK+2OfFlzoXnz2RdaQp1hDwrSb6P6dXtv5B'
        b'EKN85/GD5id55bdnjhpa+/WYz6c9ilEENv5dLuUXZzrSJ3guvMCLQby/UuIaIonAKnh6vrsoAs9n80siq7359XRl3y7MA1dhvdJNEoH1iy3huJ4GsH8ej1SOGdyCsALU'
        b'oflCE8gvokzQClcoFxLJBeyQw50OyUUIzsG9WHRZVE4kF29wU+I226C2jEdjKnQ8h2q4Apv42IXbCAAuO0gHARLUho3xBhHVD1az8BI4DteR1ZilFeDWIoVDDuOlMNii'
        b'JZ+04TOWg9aIBCKAcRNpcBaV2UIGDl6SjPJw2YPHh6FxY9mhg+Ep4tQ3DV5J7caEwNkZPBPSSXgJ0A6vwkuwMQWsBw00RcdQsCUWnnmaePPTVBWhi0J4uyE3IQ9hTvJg'
        b'cUloDHa74RDm+aM7jgnwE6KrP+NPVwx6KrFwyGxEAOsUOt51kYTn1mORDFeM7/NcFKIIXUo8ZLhNg91luKe3CxFQYv6UZDheZGQgBTmjxKop4A3iREYklXT64DgSjdmc'
        b'rUPkLoPvkdePHO5OL0chqADS/Fx0yXLqhmIm2MeKvYLS18CNPQjaoRe6QgBiwS0h2Jk9x0NZFDt+iTOkU1nUIQXQYSDCAowAiS6Mlq31+kGVcI7GggbLiAZKnc05SsRA'
        b'4pJvsdXNJdsSyZZ4wXk5RCKuToxEIgESiTgiEgmISMRhQ0jvmmFvbhzESCry75cMt8h7aIb+8Fy0dQZGkqtIYz6HGGVYQqoKCSwOZU05D4k388OwIS1d7AqhANuCCVug'
        b'kylqbF8/L3gd2IkPS07eSncZOhnYY9FvPUeFzOISEDc/RtTUtebF7qkiwJHo8AQhFWLm0pG4fFjOWDEFWpIO73gUNgVc6ioMkZYNfDDLHh285lHcxHJnabAarDOMfrKC'
        b'NmPWtvuFpYNeHxpQFSUVvDuiMGx5Xc3L0qC+6ctPKDbI/nteXrfi6/07m/a8uXBA04PNgobad2F88xvrDsz19d9hPvvuz77RH3+46fq7OUu+91Otrmr+5zu5I79M/YX3'
        b'iif9Gf18JEZhWaQf3JnhIOLzQa3burZuAaF0YH1fb0RvwfYonuQicsvBazyL2D8N1pJuJIP6SFXCYNCSiiQdHQtOLzbz693rwSZM45xwKwZHGNhYXJYB2omgswLuRwKO'
        b'm3Q2sMSNQ+wBmy14wVkHr+cTKjwtykmHgyLJF4VmNqbBxxe5yPAQeNwpHP045HT3FdUj+M/AiiWhg0FOOriWGiaR4jUBKS1mxUwgXRHaA2lUrrw8hRB2stkF5k6x3lpA'
        b'SEonV4zSdgotGlOOzuJGA58hyiHiuQrfY+8iUzm+VLhoYCm67OsmJf1hoDsVfFo75Yxa7aCDphJ8MRFuQMhUoc6SW6QlFZjMzkF6GhOiTRZXs6zosqeLtiFhDdM2PNfn'
        b'uoibGLNQuKOQEDkSCBUnE4JjM+B1otdssmC3KyosXpSpeKIIoTys4C6SFEN1DwfSi1zhOvRTw3V6mKV7amghal43uiIBO80IWC95I7WoxIpEiDp4BZ63lMIO71LQ7Fcs'
        b'hecpago8KoDtoeCoFRsCEIs/DKpRpvoUNWyOUKcTHTwR/dSnKZ3RmeAMrFOowHlm1DwcJAUugesSeEcMdz81gpQly+4/wfWY6pXoCtSENM2E7XBrBDwqAcdTXJOE0i5g'
        b'0dNNcJWQOaSZ3gAErXGv4AVhhBpuiwAnwmgqBGziTLNjDPoINWtOQWkXbFv/ZeYbXzxCqmGu/oH2UWY4UgjvZd1jLuwasOpJtc3/pWs18vVj1p/YOWDE719pfWul9oNX'
        b'Wl9l5r1y951XAu+1Av97L++kqV1X+7wgPC0XkIiHVWBXRYQqHuyXwwYFmjVwmomGB+AdQq/MEcDukMvgFY7QhDy4i8hdQWNiiFUDNigTUBcaSSI/UM3mwQPgNi/Tni0n'
        b'wTg41qiJRRQOVnOTaHAe7oHnSPEDhuOYrTCX885EKVPeV/HMKApvTXGxDiEcRn5P89daKlFKSIo/8cupCEdkIaPAkK0zmnUZelNRYYbe4K5tuRXkrJWQg6e67ZS7kNKG'
        b'Lq91oxU3PFx35lDE76rjheQ0JajHIjIPuqA5jZgk0C8vkHTXo5yBD/Vwc3YkPwNasNe/MB9eIsFD+YuiI/CwRk9gKAHcS8ObCxF3vAbP8G74h5b0R3hyflUpvFQiFReX'
        b'SEs4CjbHB8WxOV5CPlSgHfGTo2bERreCffC8l0+pj8RXDC+swkhZIqBGBHCVcAtoJt5HwwtRWxIXolkO5+dSDNoZxFQawGYrFmFAbQysAafgFoTD9SnhSQpwcgHSG7au'
        b'UoRhOSJFrXDYTMQqPnSWpsBhcNF7JmL91kmogHlx8LB77qdkrURiBwW2F0jgenBqMiGDg+BlNWgsDgYHSsDGVfAyvIJIiwXpBFcQAl6xos7M5xDh2LGYFxhqSuNIW3ck'
        b'Y6MC4rkpIsoPbmLhzuHzKHiNFAmOwqPgDip0LjzoWegqeF4qEVIjEjmk6dyOJUK/FQvMAxHpQZoLs0BNUXFUXBm4QGZq8HAV0sLSMpSJcDs4l5AooqRTGLh3VqkVe+7C'
        b'DeAlYPdWhgDsy9yUvIjvtBt5Ax2EkK2A1SJwcwaSs7DjQ5/+0+cLQTu4QlEjqBHKZELf/zJPjMMSwgLzM6W0pA/vJjmgLwlvjtk2IjNlzcTpjkDoISQQ2j/aL1PRsXAV'
        b'ZR2Hm/LSQnACyw8R2GhVTwxVfFNgNbzVrTlFoEpcmRco5y1moTLCWRbH0pnSqEFT+UoW5wpxzZnSUZnSxGHhlOGy6gZnfgHhS67fsNTWW2oYFbj+F9b/7pqgvBOelaP9'
        b'hB67sKlu31BFwaLAa/MOH00W2g+cPb7z7vCoMV/LpJOpX8zTjDb86vUv/m2bev2D+TdhbcDmtnHpc8LOnun/3vzi2+/efr/xl/8em3kg6nJL6798tMdDbgXln4Y5G6f8'
        b'c9GthpQRw331BxeHP+qcmdry8TfH/1H+bvuUN9eM39k6peWK4l+hn+v/lde+sOiDT+8e/scf43f4lR9e3/TN9Pe5tPrf2ju9vli788s4S0VD0tYi4fay3/6+ffb583H/'
        b'/Cb3xiGvj7977fhXW0eLQrbtqy6xr558MGVbZN8/LT17crrAlGtePeq4Ycz5NT977fKWhh27Pu878nGG4Oz716RXjo/5vTZqb8Cuf2tHKb45we3bO/PnIeojd99XTXtp'
        b'/YTvlZGrbv5JvmZ5xKH8795uHb2h7GP1nREjB/uf+y9t3WSB8aFyPyISTvGhk/H8NGaDdQpMT1jKG15gmRnggIVEJzaDvQsR6UHUFe5jSukZoH4NofpIYN8JjhPSDu4E'
        b'O8S9fqCGlOoPdoFLySnhKlibw5Me7wK8nnYErCPfEVzsH4F17ev+agITOFCukakMgkcJ3S9HgN4ekYYaZLQRSUSEWnWbgVfAulVEIddVBiYrEBc4Gebmtzk3khS+GrQl'
        b'RmATKRKjEwl/EVB+k1k9vKmz8AHaV8C1ZKymoIJngStypRrJOf1TuOlBIaRrZePABezC6vJfhR1gs3JtoAUjYxq8NI40CV02wr0iilPiANgLLxB+VAHvwD0RSakp8EgU'
        b'TXFDaaxb7OAtkfakPEepiB7VTMJEKRnhQX9wmUsYaiCFgxuIJB3EIblOTgqb50Yb4FZ+1LbGTuZ1A9Ax2t3nNSXymfKq6MfaH/r1yvgIs5zXxSynYVbJEddVf0bC+EvQ'
        b'fyaAxlcJ64/ehWDpnOGIZw72z8Fr2mLiyYMYLONL1rj96QBGypgqnTxazrixz+dpuJuLGS7kVjeG+mqwO0MdQ0DkPDjRg6HCO/mePFVArbSIwbYF4KCcJSF5JnASySCN'
        b'6WvcbFAD4A4SyTCpJBc2qsGZFNgyJ4SYkUEHA4/MATtI1lRYGx6hVOfDjcpwIZra/Uw0gsNj2axDBMQrHEFOMXAhlim7h9JTrmB62iOcnrH30we5VkAEP7gCwhLJk7s/'
        b'Ak2iROb2b54ux2C26ExmmSVX131nF5XEI22iRWYwy0y6EqvBpNPKLEUybG9GGdFbvNEHjimUFWG/vSydvsikk2mM5TKzNYu353gUla0xYr88Q2Fxkcmi06pkiwxIvbFa'
        b'ZMQh0KCVOaCPtMpZNvpgKUdN8CjJpDNbTAZs7u7W2lji9iDDml6sDO9eg++wfyAu0lE86mEvWfJ15dhbj8/leOiWUSsrRWOG2tRrAVYz+shnd6WPfyFx5nzyRWbQmmVh'
        b'C3SGAqMut1BnUibOMss9y3GMttN9USPDfTTmYN9FjQx7deLmOMtSydRFaOCKi1Fd2OmvR0kGPcnFDyiaqywNbhCaKzQ35myTodjSoyMeZiGXV7hLQ/FWk5i7SATFm+dH'
        b'Ohcj5y1KQALo/IQkPagSzJs0CZyQS+C18klg2/Rhk/pRsBUelw6Ihp5w74qETPKEe8oB+bQL8hm7n97/OVf7PHRJTCFkPfqgUPeu07kcLfiWUK4Vxh8dVNpTs+PUhMoa'
        b'dn/Xwpqx+fTS7je+zFR+npAt1j/IfJhZqH+cmZhNbXo4fWyz/KUzCadq+oz43eu7Xvv1K7t8D0cUxLbFBk/PeqtJJT0f25G5Z7x0c2alfPq7BW8fDGuvz3xXsUEf9eaG'
        b'A++oBt59I6tAn6l9kCnc6U+W6/70YPDdjasefi1nCKuywY6wCGUYMSPBcwzYxShBezFv7j4Nb4VGwJbI8Egr4mJWGvGqO2D9j1/mEmSsMmmKCdMY3MU01lKDOOLEJEEU'
        b'mXfrDMTRo3KTgxC5OS85QNbtDS7RqWoRH8HnN9rQfAbCKHCoewjjtCdVOf4eeKxmTUNfQF0OvBjhBO9eIkm7OEh8gDwyCfFtcHLcbHDczwD2gBO9OyWM5eGc+lEBxM/h'
        b'iCBSW+MxezPBG0gQORodNW7shDHjMaNpt1hMpSVWM1FoLsELSBs5DzvgRT+xVOLr5eMNNoI60MQgpQpe8YJnEGfk46ZGJeEwU3GU9fqC3BeX82J5sE8i1UpRUVHpe0O/'
        b'XyPjY6QMneOErDkD3Z17/HW/1w4ETJ8eKHhn9e9vH3zplXMJ6/Z7Swpz2rYlgNWGN9dMeG9n34cf3rcdDWgI1A84/49TV8vCouo3/zH62wliXfH45vu/XP3vrf+c1ld6'
        b'dNDY+lMr/ce/2zbpUOzKAZsDO9f7IvAlwtBl1Il9DiUX7odVDiEQXI+0kMDCPaABaR0O20HaJKSuYMuBFex6msHsWYF34gxTkSUjC+vMaNyD3WE6giNwHEgcZwLoCsVz'
        b'QbOjOOeKjMvp9emR0SRFFyxXoUtYD1ju9AjUwxb62CS4vRdQNqT2DsywIRLUp42dwFKloNFfpYLXyPRfYfg9sIrHalKGVSyirNh1dHGYH9wiALcRTKooFWwJJUlf8CUK'
        b'nP+cYkPK3VXpPPj4DufIDm1zpPkFLZphPPiQL2PmEPUz6q/iQqltBuvYXWtqMgHB/SH6pI9eiOJfHl7eB5PzmOlxBSkxhYUUvy3WZbgX3JgPm+HW9PFR4DA4CRs4SjiP'
        b'BqfBcXiAb3xuCDUOl1ZWNvlemjdfWlFJO127TCCiqE9WBQ8JH0U8AsfB2+DkfIALg80CitXAbZn01GSNFZs3wRW4CS8IdmnaSJ+AdYokbEXEugVSfcGuGNSUjRFYSgf1'
        b'ERI53LeELEiPDRZxm6gYvLuf9KPFwSIRReJkzyweJRYvKRvok5mSbMpWTiye8/YE4YpTNNklxguB+GZ4ERyAuxFbSaVSObCftP2LIbGUBXWoSl0YMCvYMTynSqdSk6Ol'
        b'NDWnytQWnF3MK/eGaZQNYa+/WD/2XwVz+JRfZCvo1skvc5SsyrxYXGIiL2XiD2jLwEIR5V9dFDw3Tk1eru3zIk0lhKEJrs5vm3l+EXmZsyKQHueXg8ChqvJD00k5ebm0'
        b'2ELJ1t5H7awqDV4wU0VeLgteQB9nqIT9qor8r4sn8LXTqa304VELhFRmVc6H/e9Fk5e7+y+hpItKadSkirakF/uTl6+VDKOXL9rNUcWooqGv8+D11oTBVKthI4W6aftQ'
        b'Ustn1+Sn0H9XzhKg7Plts9nBfDsX96cVDOXfPiN/RYQgnq89Kvldej9LFcsStZGFi2fzL4f4/4yqQ3XLhmq9+jKOUZoVZ6P+jXDsnQTTwv5LdfzLNOpj6ipNhb3sn7Ok'
        b'I6eIf3lxhJRC0BMmCy5L6Td5DP+yJK6EagsSIhHjk6xA376zDAs/38uYT6ABym77Jn1eatEvo/wHbfxTzEe/Pbp1Y8HF6QeOXPqrX8zf7/pNf3RA9opgSnzYpoXtjf4L'
        b'3n59/9X+W4cf+2/4Gl/Rz2/0C2h4vLO8vPzrUaWKqeqD29LPRsyZeeHvk3zGaWtCj8KCDw1jw/76r5tpxweUhvr4DO8I+dWVjL1ZfX6Z3sf7w11nJSeSTyTXLzzYPOG+'
        b'cuhvFp5Z533yi62CRx2zfA/fPaWc/0/bxRu7Pg+MOZBTe/BXEyt+HrHvHa8Hog/Ay+PaH4xcHtP2nT3/3P2grf9sWPzkH6Mk56IPLf2Ld4Z164XjmXG/00fPWChqv7Xy'
        b'9qsttiUq8Y2vD89dWGtT+yw6+Fl8tnXAtfHVSxuXjd32j84iy8K/ZP9O/6F30qiLE7+7XfC7Uf948/Dg0e/WZZTU/+ZqX8u++OYbV+0S8+NDP2f+9TfKr6TqxbKmmQNf'
        b'L0ib/IfF//3H/BLzpz7ql2K3f/Dtlood355eO3P3ine++tkHd97J+SD18AdD4h/2+dPOGEvAvsR7v3tnc8b7H8Tv/rR8TuTDFR99Mfc/lgnGz9K+EXxz74Z64801519/'
        b'kKGfvXJP9dtXpNsfbdud8NB6fZJX5NRvBfsLW3KWRMvFRDKaWarpsgzAM7AGR7eOYHmp6RZirnciYF0k3hrqAG0BdXPmgipiUsjTgFMRSUq8A9utxWoBJRUy8NYSh7UD'
        b'bpuEt/ZyWbm3wcuEV4FGsJsv+fxAUIPoSFoiOI0IWh94qYAZ9qKWZJ4PtsJTESp5Er9bHhLd6gSUH6xiiyJyiJndOAhsJaYUrNLCKrDOZUyB1WAj8QyphJf6Oh2cHM5N'
        b'cH++w7+pGl74sQvr/j/e9+G5RUqxk4kSDrzcnQMPkOLQIF9/CUe7b4uEfwej32D0F0CPQgxxIC0kXyRY9mQD6CDCt4UkWF5MDBW+KAc2WlSE/DAXd66+4SiATpFDR+wU'
        b'EMXPjX3/D0KoWNM6fE/CDWpcXL8aXfr14Pp/Cnfn+jh4IQ1ui+rG9UErEp56F2IFFLADJALehLvgMSvejhScAjsQNzs9hSxAuSy7vKkDGzoiwSUBPA12gSrehXwPOJzk'
        b'WmODe2aoiUe4P1zPDgaHwghF/FscMfdSUUGrQiL1gTyZBBQvGESNCvAdvbov//KFeH5zzahR//LJLZpCGfI7XxeYD1B4+8H0QU1xvmC6dNafCqa+lAomiksGqKe/mJXR'
        b'uFW/LWFB2AFOEvT6xQ/u17YFpl147RfsxF+v+mrgv99anDhs9rzXj7TOCz+hG5r80d2FpZV/6Fs0dcJft7zzcUt7UtyeVsH1tg9nhf7GvjLzXWHf3zZ+cnTwZ+9fu3b7'
        b'wi/aN3z9TTXzl34LV38Lws2SPwd898XbuaJV8vC3Gu+cWXb04p49H7+/8437op/dVn2xb45jQzO4fwZo7b45K0MNCQAvkb1ZQ2AbUch8RvaFjfkKYlp0mBUrwB4+bn43'
        b'PDXKMUuI5mx0Gqw2puAlvr1cEWjO5jdFqwH2yV3TKZgSoU4VUAHhLBKAjsSRJLqpcCtO4Zg/pKQ04G0xwVl2Fmwy807tO8E1JP00RirVStiQUgzuyIWU30A2oxwcIY4C'
        b'L+SHg8Y0JOYUjsBCj8JJNULBJg4cGgEuOFXFoP85JXhuOuFEXE/nKfwXiF2nwl6UErMlg4MKmSCGj8LHdMFUi9Kq3bGbRz+CeV143ff/cl9+AOtx477vZuCsmdB9Sw5o'
        b'l5lcOM+AbTTlN4HVWzI9Vp0Fjl8zEhRdHkpaeimrZZZyWnapQMstFaL/IvRfnEMt9UK/kq3sVk4raOZ328JL+5xWqBWRoBZvnVQr1nrVUlqJ1ruZWeqDnqXk2Yc8+6Jn'
        b'X/LsR5790LM/ee5Dnv1RicTYicoM0PatFS/t46qNdtUWqO1HagtA38T4TxvUjHfiwpvN9dcGk299e/k2QBtCvgU6nkO1A1EN/RxPg7SD0VOQlsQ1y4d0+qbwRD5VY9Tk'
        b'6Ez3Rd2Nptiw55lGRnw0PBI9K4fBjC14xIyqLTdqCg3YmFou02i12Mxn0hUWlercrIaehaNMKBE2zTuskrxJ0GVtJDlUsjkFOo1ZJzMWWbAlVWMhia1mvGm3h4HQjJPI'
        b'dEZsPtTKsspljjhNlcPmq8m2GEo1FlxwcZGRmIB1uEZjQbmn3TDdzJuSUVUak5v1k9iIV2nKydtSncmgN6C3uJMWHeo0KlOnyc79AcOuYxQctarIYFpMGqNZr8N2aK3G'
        b'osGNLDAUGiz8gKJuenbQqC8yFZJN72Srcg3Zud0N2VajARWOWmLQ6owWg77cMVKI93sU9GRQrsVSbI6NjNQUG1R5RUVGg1ml1UU6Nsd+Msr5WY8mM0uTnd8zjSo7x6DG'
        b'kf7FCGJWFZm0vZuJ8JoqgnuOj/dyBpdVMsTw2buhiCWGT+7J+p62ZKPBYtAUGCp0aC57AKLRbNEYs7tb+/E/hz3b2VLepI0eDDlGNG4z5iS6PvW0Xz/DyUWo5gNc9kUF'
        b'854gR6c8LTjMawrcDe0kShc0RXuII2EJCpUKboxMoqkJYMdKWC1cDW7BO3KaX6+vWgzPJKN0aeDGGiWOvmhOo6kAsJuF1XADqDL8/eYp2qxGKQ0Lq3EQ2d0vHqGrIuhh'
        b'ZoIjbkK1cNKhME2Shrk44GJbXNtLAy4u3jUgdmdc24XFcW3VWQXye7dSBin+9lgufUW6W0kVTOvjO3oBUhpw9XDLSpW7iAWaB6V0se5hWfzWortLl+FEI+CmLsmK58qN'
        b'4DrP3G+DfSLvZCy0HernkiP6ATsnhidpIkPkgxNTImBLwjhvgHRlFt6gjWD3QGIQQ4L8JQU/CPUxShVNNqEC1cNBG9ExCmDDItiYrBThTXuxyEcng2ZwkPfyvj5iNSl1'
        b'Etw0djxLiSpouEsxmyxZroXVU0nn6lJThBSSA2caaHgN7it+lnOah0yfYUDQmZHR3cEP/0mlJBICy+UV/T3BVuXMp3b3aDbVezLq3iMcGD5ZnouxNqLLOsZp1aty/VGB'
        b'7q57P9SC3sOusACLNwhwxhljj2PnshMSkfJcw9C1gFmILpsYR/RVj+qc8VlPBvzgahaqhNUWZT+zQTl8g8QZDs3lKe3Z6mzPk0C39SznspjqmVXlOqvCxNSgNT+lqh2u'
        b'qhS4KqcQ18viWXaBAZFppRlRa/mzm1DLN8E7Q1dWbDARLvCUVuxytWI4bkVXHsxoug95V+VO4t3fRbwdm4TaBW7E+0dY+Z3bxvQgm9jbduroIfNhMweOvYjDQyiwEWxB'
        b'GhhOWgTPwVZwCjWrkkoeVwnugL3EkSgK7p8MGxOJuB6NdC3QyISJksRgoyE/qZYzL0JJPv4+Rvnmmz5VUdKa+zHKjaqXs07Pqf5swHvzY7QFL7wqT399n+K7uS/IW0Jn'
        b'ptQl/GFL6SxdyaTP39/2q3kzme/D+59VsULjkse3YvQ+l785pppyZEpk07dBVe9WyiV8rEcb+qv3pIWIEsIauM5BDReP5jWQdWB7AbajJvLuHfAGMwKcA/XwNtzPu58c'
        b'Hghb3T3/GHBEXr5ES2gS3AbWwVsRjgMHONAxQ02Ddi+4l//6EnjJv8vcwvWFh7G1ZXkQv65wG1GvJjeKpvCBpxFFCwV3SG4LrAXY7SsSH8vAobLuTKDBTV94iXwtBWdh'
        b'Pd792bX3875IUAtqxvA12+GuyGSPXQCj5xaB8xWETYBtoMMP7xHeDA7gbVoRpcZkOgCcYhGTqlV77Dv2nHRVZ8w2lRdbCF0d6ElXh0qJO4aE+DmS3Vt70DZHbg/i+lz7'
        b'Bzr2bu0irtvQZU8vxPWPTyeujgb8vyAdzczVGHN0vAeEU55x4nk3WQmJPM8rJhl1q55HOnLuIdJ9oRiJL2Rd4wzC7VvJPEBg4QXeHOaSXzR5hrglM1mCvMqYeJ83Inyr'
        b'ogJnvbvz8rcDl7FcTErfzVc2LJwSLc58c8HvtkSEBO5ZtWBs+NLimIgxotpfv3Xn2oV35r3infXiz9f1EwWezl/1F//Cu7Z1703SF7SdHbJU2Ff9qVruxVshq0FtGBYD'
        b'hsGd45zCRbM3j68HIzWgMQ3HtoKTijCa8oXNLNybrhsFb/LizebkXLL/PQ/XsbDNBdrw+iJSvhmsZ7HNAW4zwgaa4iJpcLEQVFvw4QygDtwYwu9rmpwGmiO7xD1E04Rw'
        b'R8gkUB3Mu1CtQzh5gJdk4AW4Cx9BkIwoYx0fAdEGzmiTnahFJKCmPCQZ7YGnCVlhYUMCkXScYo4dnIC7JGa+6PMxMz1EneRKRBg04NyPx0y/bAJvGU7g6O6EjP/GSsj+'
        b'H4F0xeBueNEt8/9C+tmBLsd7QdBODwR9RkPkbKcwt8hsMWg7vRA6WIyY23cKea7fe/gSQWLOGS3gQmKO+DH1HrbkQOL72A+0B07N0GqxeoMRz01g4NVBF8P+QezlG8/j'
        b'bgK6T5zlpAFZGmN+Twx2Ib2jr3zOOfwjyhyWbDUiZVKZOKsX5x43RyFnTqw642wejkHy3tpr0lmsJqM5Vpa5wGTVZWL/Hn4zBK1CljlbU2Dm32kK0EttOZJgsBhltDyD'
        b'CHn1IEKs2pB9N5EzY0Pyk6E3v8x8+7fVWQ8yH2c+yjToz+oeZD7IfDurQP/4ixO605p7WSc1D7LFerFWnFWXmUBfiFlGhbHeMeL5cpYPUVo3ZHkPMgFOgrM60DSFEIFZ'
        b'4MJg0DgfbkF0wEkEYHsGMaQumA73Jqckgvq0VNiQogItkXCPiDhvykGTAJwJBC0/HhN9NVpthi7LkG0m0ilBRH9PRJyJ0bBiUDfY98znwEEhj1L4QBzTTnzZ5YmN7s3j'
        b'3JLludISbNyNLh29YONbHtj49Bb9z/Htxd7wbR6xUSGUM/Iwhj3U3BDPzTr1/z/Uw9kS56fJeLuShTdDEe1AbzBqCmRaXYGup1vd8yHd3mVKhiDd9ID9COl6Qbn3X3g6'
        b'0u2wO5Hu3Fp4pzvWmcAmVpcEm3j9fvMYsIuwXoRylJUgnQjcJruli8mW+klI6GiOTAbNLtRTqv2WI8ybBlpEAXBn1o9HvD68efMZuDeP4F43EUzVI+v/Fv3wLus/6wX9'
        b'bnug3zMb9ZSzUWg75XY2yg/vfu0UWLN6QTwChQRDjNbCLIRsCPDcbMVdFthsq8mEaH9BuZs6/VNgsvTLWM6MN748y03Cx6/sSc7VHyfweO8pLOB96rcSL8uZ/QgasaQY'
        b'UJKCl442wXWeXEAHW1leSTq8BIlrp2CdEyAJOILWdAuJV6yGjWqsfiGAPAw7ItyYAeIE4UIEkNdEstngYLfDbnqFwOwiq9HiNmHm3iBwqbg3COyRVe30Scz7YZCj3QSu'
        b'/ejyfi8wds73aTDWo9r/EYzpEYwZfxDGuvyNnxu+ZGHhWAYzGGWlE1Tjwnuhwc+Gt2/7T2MJvDGv3cTw1ju0PXngCW/R1G+lXqVjrjqp3+3KkTzxA0fhNg+AOxnBU78a'
        b'WBXuBDbY4UfgbZ7MAW4SHHdZr1C5Sx1VYA8PbDHALkSwuRdUPQe4+eNBfBa0ZfGbbnWb9u45fyyw4a1OftMLsB3zALZn1Srv3z0sWZSRoS3Kzsjo5DKspoJOH3zNcC57'
        b'dHq74kcMWhM+aMi0EV824csWymFy7RQXm4qKdSZLeafYacMkC5+dIoe1sFPSZX8jhgSirBAZiVBqgkqki/yo/ISdN9zMf+vRpZBx+ICLvTkGu3W6/piBvgxxFOlxZQK8'
        b'B/oM9Bvo5yu24i0cl4GN8FJXpDHsSMVx+afBZaR6MlQYqBasBS2e67EYladTjs0zPNdj+fODOvs6gjMcE0V2CH4iiy/Dmxpi62Q2jrwwGbEQ5iZ0qRGv85w40yFXp7tZ'
        b'P0+hyx8YV5Q4x0eJjx2S2RUjDttxp0BtBO6XcxUiSSICGwuzrdgzFVSB6/COm/Nx66wf638MD073oGwu6wgeH4dnPuV50GTXDqvP8NHXu1tYceE9/aj9eJfHs2oJFUZR'
        b'waN9ZAVtmrslxHvz2EwRdW+K03tzTdocqgBvBpqTPkXwMPhazvfxofJr+XMyTg45nq+fUjpGMHfcoOaS3LGhS2KHLFuVZL0eezR9Vvx/lvw99PuQexNDKsojNHPFovzA'
        b'Xwz6moFTpOMCY66OWT/utcrS1JiRa8P6xoWll027zGUEHCk+NyQr4zeGS6Jh6YczdTFJ+fe8/pQ4JcKnf+5ik6Bq2OezSiWPzKXFYf0/ij/pPcDn+trvkejfvpoRE9Pv'
        b'DC240GX6BevExPqbJB5POno/hnfHyZxqLogbsJr3vJkiCSDnqbQbCpfPi0/lX1ZM7k8pKMq/lc4daAzTUyQEtQI2WmBjaihsVqrwqaHOrcrgxmQR3AROlMP6eLBNMJIC'
        b'taO84AF4aCzvFlnAH9XcnllQoC5I4StoHsf7+7zsV6Qw0wZ+z9CK6b7ZhWEERWjtb+Us71G6zBvPTlSKN5qduHG5ZHZWJQupqL6T+dkJHm76jJ+dW0Mn95idvRNK/j+e'
        b'nTmrZggMfUMP0+RgEe+HG0c283tRyd/8JuZPg0NvpfzlnQhx2CfGGS+uPhH0j19v2hT/s+GCeX8eNGHAb47ev/vzfgHb/ltwfsZRZueQOY+0F8/PG75k7NS/la1JXHhk'
        b'X9yizUPlh0TeyrAVyssLj92P+FPU7+7fGnd7xZbz27ZFHmbuLKu+sPrNu+H/eSO1Jlp4p/V3o+cHj9S+vk/O8e7zL8FLRpepehY4zZ9ZMxqe5A35dWA/2NTl1AT3xLn8'
        b'mohTkxa2EvabpwS7IuAxsFOZhB2bEEgIKG94HYdybk7m5b0OuBcciYAN4dgkJwTnbGA/MwleVPV0fP+pG9S6R/6bzBoPqzjeQMGN/1o44hfoT8IT/WkZg4MV/WnTGRd7'
        b'YTs57G3gxnV/8r65tOmsi/DiCv7cC4veKut+yhPc6cVEhKtBk5tGFwr2xME6DpwCW+DW3mXCyb1STtdGQT/q1HOPkwJcVNOHp5oflWK8nCBEmF0QHNwvkeDltLUi6p00'
        b'J9XMXrubx0tqeE+qeX3xurBd6p/HjFvSrNiTdibuSOyKQe+HH8z6TvEkda3P56E+lTfT28Nqh4dM/L+Fl3XLX/UlXZkxlQ91aOVM0iM+A3gKVRPJnzNVPE8z+Y0FyykT'
        b'PpeefLkUwzswvjPDKtV5qfiXuUF8DER7dq4iPjyeP/aKAdfGwUbQMc1jMS5JDA86iFtEFBrE4J+L8CB+OL45kAxi2xQRNWu+YxCDz+dP4Qex7/yfPIjZvr7/twaxeLpM'
        b'ZPjtteUc2ZDyX6Is5RuEuLFz3rj3i2vV73ZMfKPfOO7h5ydmjh0g+HDZIvnNOv8hlbdkdW/d/mXZF15DJDbbJ68++buhZt6AM/+Kl+7x/lQlaH439bf6d+FUecUNxfbP'
        b'r95pn7G1Y8HvP6V/8f2UiZ99J5q0ZtDy/f3kNL9CuFeXm7wMXMAiC1ltW8Ho4A5w3UNI/smbEhE6otV10ZERnnRkLSXi+EBnQkEwLZESymI610VJePTvIiQ/dv8yN/Jx'
        b'zoHv3cnHOveNh3hnmNtwixdPPxJTneQjExxZyYEDoBXe9AiZxHEpZM/VXERT6gT8rvD4zBJMNWqYSobcs1oO3bOtdFmYhcZpZlGt9IqQ5UwlV4l3jxfUURYGH2qApHxf'
        b'myCP1QpQOYJFlHEw3rc9X2Iq5o8OIt/woS6CJWSfduM9Gz6yZjopA+e/bmNNrSgVsVaWnUV3QnL4Aq5LWCmqo20ivMu8VtSMctiEk6mSXaiWDSS/oAYfD8Oa3sEHHeA6'
        b'yoyotQKyrz3OL+6RX4zyd6L8s0l+/sCe6a7cYa7cA38odyuN97ivE/I50DvKhg9WUCxy7LDvOJIny0ZpvQZgqsvLpxI14jE6XfFsEz5UecETgdWiV8a4TpZBENyO5xx/'
        b'NGHx3IQPbZSLTBoMmV46o7VQZ8JHL0zHz0K8n7pW1ylNNxrwDVEa+LyTeaDr2ha0q1iyvz2JMMMb0JiwH3gnnfcjo/E7pfisE/NYPnI5AINnLIFTMXG9xSd28Od+BJDT'
        b'GDgSOBfsdid1/IrJJqhifjl0LltCjiY/KU1UTgjHeyWQDSJkgzl4Huyf5uEK4nKewGhho8xiLT2fwoc4kdFnyFEIWB8gI2ga50JNupM2/4Aa70P6lGEpyigoMuZEs47d'
        b'lSkWK4jkJPkl4AZpYaISGwvq+Y0tkSwcCetE1CiwXlAO9ll7HA3kMs8jYKDzaZMUa31a1oZPSqK1XB6FT+FBjRYE4RM66P4UZtn4DTERCh1dwLzoCTOyjN/JgeP7IqjQ'
        b'GwoK5Ewnbeykc3+oX7g7uFukf7G4XxLHZHHkeBWi1oLL4HQotoig/uBzrOvxMZq4q1qwU0iNGiwoh7Xg8FOiquleo6qffv5fj6hqIdUz8rUrjHDrkmLqE4qKedlo1Ncq'
        b'JvEviy2vkriuzDHlXjs1Dlb+pYnnzS/H5ihWrMymDAEhIoEZHzWwqf2VLzPfIntknSn+MvNRZqHeoqnrOKk7rnmQeVcf+d5D9PW0BrsHPtIqA09q7mbl6cOC1tWVtp9b'
        b'ZIn6IGpc9NGoRCqxrqG4NWz43d2B+jH7c4PMkuTo7Cg2x5tafmCA6NwrSNgm58xdlkc7Q7F1oTgSG24BDXxs0PFVoJ6chJeImNcut5Pwrgbx+8s3wN3wImxUqJFWDl4C'
        b'G+BGBY3SnGLg2RdBG2GFIg2SDJNI/E89ErEFsGoNM8wXnvrxAd19Cou0kybyR0pkaA05Bkv3rYsdm2iJaf6sHTE9kDbdceHV/6OQbVzMTNZZXZXb3x2PsG282TbYBo/C'
        b'G6jLzWng/DiytTM+3SddgM+HrU8hgxQDjgnXgDNgiwfJcB1giy1zPKHA7K6GPyyEUXcKNOZsgwG17BLlYsI9z38V5erKCgz68lTWcd4VxZKNtfoE4FgvsskcQqKdYE8K'
        b'OMUhlWg9A69XzuudeOF8+AAVwgIDsUcbbk+lo3UEQRi16WW+HdPcWvWULdC8rEZHC+d1kTAsoPBbyrWDjeURsNnZ0h3wEgYv1FK89dyecHjxucfMvW1PHTGvrAnj+DOy'
        b'lriNGUGCyzRoSx4bjZ3BwGa4mRfo/IaycSLFTxwx/U8YMdQ+npeu7DZi2LNkgQ7sx01E4ubpXIf3LjzLjoG1ag//QNcpcJgTamlE2pEUVTbMRpnCLZj0szUMkiaoSpY/'
        b'FsrGIELPlEjwUUzFE2w0PqDJcSRT54ioMWOjx42fMDFm0owXZs6Kn/1iQmJSckqqOm3O3HnzF6QvXLR4yVJCFh9i6ZSXEmgkEBhKERrLuU4hv3DUKcjO1ZjMnUK8KUj0'
        b'BJ73e3XvfPQEfnJ0uPPkKGPC8YRkAx8C2qARNOYkj51AzAZHwDnHNPVnYxEeHux9oqQOgNHSDl6MpuXnLnJBm+7+AKhET+CnosgNVIiXc1XWQtyExNSwhc5ZOMxGxcKr'
        b've9VSY67pl3HXaO2PP/+lM7Curttkag5bvgsR/D4JXgZIdK29FSvubADtM9Dl455PqCFocLgVa5wTZlB+raNMxNryd3bX2beRVynbhR/holU/0kBYlpvsScX7XRsfDBa'
        b'CF+KUCbCFnATIkoSKaK8ohkkujfB3fz2V5PwyajOeFABBTflknBQuGXaDx1VbTAXZVgMhTqzRVPI79ZBDupxJ+gVprdcs8L0vuLgZkXGaS29UuoWj0OrsVU6F28I2KjA'
        b'++9HkiYrVYmwSZmwjKJGmQRrQQPcMNvDAdDTFsw6HADdLMFoPr2f09vWYz6xRBDQYz77qPn9m2i4IRkx2RbYxFFCuEUYwkjA/jgiRpSr+1OKBdFIV88cGDQ60XGy9S54'
        b'B+yOHgtaA8D5sVHUMEqkphGDrl7IH8daNX5m9Fi4AWwAl8eCDg59BjtocHkNPEAC/uE1eDQQbhHgjd1TVZQKNIPLvIF0zQAqivpCSGVmTh4zpYIXZPKXyak5tjgKvcz6'
        b'q66E4ovYvRRUg4sMNtetiKPi4CF4hqT+V7qY8rc9ZFHqgseC+XwRBVlIR+ZQt6dnKt4qZBGckH7DNm94NDkRnFYIKX+4lRtIgwsqcIlk2UFNp6oWRCHhKtP0cILWEbAZ'
        b'O42yKYRCKirTtL1yMv9yahoStCbLOTRCCoV4JGVYqPqEMn+I0XZrbHzr+SRuhnTD91r9qtI/5OlKVi1e9oS7vb55nc7/o/XKhaFD3/847DPJqy+WBv1iS6v/v7/+o19J'
        b'+cPAVX/9+atzy64l/tE04MCCB7LB20P7r/9KVFTSWn48xPDO4qsnX4/b+P2Tu52B4cvD4LIdL7zRN/IX6p2f53+RsmHM7uML39/0aM2JF2qvvP3ol4tujf50vPqr1Ddb'
        b'2jccePL3iL8Fj/2i9dCW8/8MH1l2puKfiaFNqUZL+66KNffm/2vcZ79e6h0eWrBpS3zy/NO+O7Y/+mfjsm/L//K3qp1/Of/fI2u/p5MVM4KXZsqFZEvkmXFgX3Li6Nlu'
        b'RgivyQRPQ0FrSgQSykqxbOcm1+0FN4hdtBCuB8dcweal8DY5SXkWOMc7XL4EDy5NRsJLG9zg5iQN6uH6acThMmoVvE1iRVKt4P+09yXgUZVXw3ebO2smCyGEECDshCys'
        b'sq8CkRAS1CAILmOSOwnZJuHOBEKccQHq3GEvuCBuRVRUFsviXsXeS9VWq1+1VTtVa9uvrbjVpWpL/ex/znnvnZlAsNi///f1+Z+PPMy9773vfdfznvec855lr35TqrFI'
        b'l76ZyEJ9s34U9tVy46B+HA3LhSZ+lrHO2P0tHMD/CySyae2w9/h9gIMmTxwzlrDP1NOxzzUSz+SyEu8VPUBSegCDSPxgXiCb7SwK6egxbb3VlxKYijlUibvq29Q6v4/C'
        b'ESZR1z/joV9QX+a4VNcrWFdnj5huYzfBLRFVt8xdWbSgeBQpvSPCe3TM+DH6uvMlbigvAcF6A3OlktZk3FrNVQY4bhA3CNDDnXWWoabMpbA+6Kte4zH4ZAz4JwwYqCGr'
        b'aAtLanHYBv8l2FdtuVw25OoDecIwvaQobeoEaKIiWt+tF1mAYcglqrWa1ATPAVcKUDIjlqSqbvxqohEIaRQlNptxo2EorA/FJTRjxG44I0YskRdn2TeQw7zD2tFlrqug'
        b'tqUNGA2mYNVTUFtG04hxW0d7u19V0clNXCJmV45LIX9nCEgFLCLY2OWPO4N+1PsKYXzWNY1KaKX6M8wvKv4zo9ZCA1/F+1cScOpJbctNohXjgGQZCIQAjgJ6QiQRgL7B'
        b'NrsC42wb+/WnMYAGcB3oibISlvJA407JONag39GNLkyI03FekS4k8pUD8jWXZGwsyCPMIQwyRjMUcZBJAieotTC3giJBDjEsYrjsJgoHh3NIJayApxSsGt9DbrGaU2w0'
        b'r3LVqZHTL5/V2dpSWjSL6LvGQMOMywaPuGLkZVfCb1Eh3peOmnX5rJlELp/ExpLQyZRKAQeH9HNcDvpr1LqVcVuD2tbRHrehzAcuLW1rYF6I7pfiItQTt7ejrpwaiNtg'
        b'HOEDh1XtN9HeGeiNEr72WZn3JmSdomR5cqBwngxLSIwLNK7TH9Sfqlhc4jV+oMeAItWMLXpsMTvWIgecdg56oN8CPMVtCSKj25nw/TQdQHgL2RyS4oyDUDcgT+HhgiPx'
        b'2gRkoodTx4UFBcj1MOdDqyMB3pbh1Xy7KCzAG6EzL4wCy6wI8SdQrtgHpojnVl28zPoqnPLV3eyrwIAwD/fs/e1nvjeJGakqzrtOCQUFNEMwoAS+b9GqCNU0tuDhlb/F'
        b'3wrz4l/tb/mGpRj3tKv+EFrB4rAfTY62h6TaLvKX4SLvbQ4hlwH9VP0J4+6ikQt5Y09JIbGLsMPQmPOAyO62jdQf1Q/1bIGOUayTGg+AnrgVol+icIkw2itsN4pNcpN9'
        b'hQOe2RSZntn99ianYrdSQATaAbWh/bljhUsZjKEXIe1WPBucK9zKEDOdpngh7TFDM0oUsjFdyYBv0ro9y1Sy4Jk38URSeinZ8CS9W67eSg48yyC7c25FpjI0KgIrgZbl'
        b'zhVZyjBKDVAGQqqXMhy+kaEFBcogSGdTtI/etAhHxN3zYVL8gdD5wIAlwLBbzHBEtEm5O4X8Rbk73tv6cuZajvMRtjT5qSf/Dv/UDzmi98/nkvH2KhLTnLK6fLRaKep4'
        b'sL2mzv98gqsSuvJT2lZ6esYzpADUWNxjcV2EcWXwlvWdoH5E6DZU09Cz6V3c2d5S0xjwQYYXUxrQO7UBiRw9W/xlmTW3ea11aZleCnGbDzcEWg1nMf3D1fJqkqHsykit'
        b'GT/uNjeJ7npobnDZJ0LsQQWffPOgU2VvJLvZjcVJmEq3J6Yd0X/npSS65s1gvAvw+IUF3w0DKDQL6kQFxQbCdG5VLjxxNsvtVYocFvEKWwCv2NfzwVzFwb7K4ay8y6B8'
        b'jENtzpWr6hQ/Os6POiWUjmZyZFynKgYGjvNXn7JdPSpC8dATr3ADZjHMXcBCqqHgmkbYXHEztoxSyON9JRXQfjb5sw8wDuzPfnKm/6Zo6cYRlnFQsKM8DPLRtxs8pn5T'
        b'lXAqKnKnyYIIGmkMQ0z4L1DcbesAgMf41qewFbZgBxASSEMEFEu/DhsfdyVg/iwHAypGtn9XNFlHbHZ3+MES/8kGbkg2UP0bNsaOhdUAlZPSQvW/uLPSVV/Dzwfdmtbr'
        b'9KZBad2gOwGCqEuqAVhpEtIiGkE6AuQWgdrKW23FsOJhS7SGhw6BYGtNO7Tw74lmyyxagrkq4nY/a8M56YuruMg/Fk2rXo6Feue7slL7wYrvNsiJboxh3RAS3RAS3RBS'
        b'u4FDzrO45w3UEWp/9240ovenkDX4yK2o0Plz03tXoXTui+79yDqtH6z8MzaChBqHBu3UgDxXR1m4QS1ACoVFBI/gBJknQyHBBCYxbEljRVjdsxl9IKm479KxIeuZ2+cD'
        b'Qqsx5G/1+SzcVcb9Y7+YqgSd+ipxZGRGVgcw69NtsSYL73mOrkwFtdJv6hubpcCoxIyWmTMqKCLNqGjOqGTlTVBIqsibFKw1tzY2DJfiz99TxyKYGAsxORaEzM9tqm08'
        b'kqeWOM0cFa/gIlcG3UcmUdU3xG+1pOlLLDleT3uow+erbWtr8fnSpOQWmt29MpbBJOCXJOYC5wErolD2KGSg4O5cPVK/PNK2t8M+c4uwlTfVgcpgWH7LJWjFtYCMGwOh'
        b'eDrS6Yq/rqXGsrOPO0Jt7AzY2g9+S43GicjjehJJyqofwyJlSgmc5TltjbAMZWc0ngCpINF4hYBFEbZIxBvxTFeBQMFWFZfqxk4IoNUii6wUd/o761o6go2r/fE03MN8'
        b'wGRijcHPyH80dCwQnDF4MJ2yIqrlEYvBDtQC24LVNS/2Kh1/ft1T11R0ttRbsg4QSGbRfaPANiXWPn6c4EXi8NMIPEhnE+IuUny4knWLtg4JYB5Y9/V4tM335S4XIraI'
        b'HLaFhWZZVWh9AKkIDL8QXMLuG3i8TjffAI6QEYmv8oZl9nyVdxnXWQx1SahwAbUNgDLtEQc8kcNAS0TsYQcObtjeh4PcYeJg7BFn2Kk+HeaD3w+jwoYTcojTuYAUdiK9'
        b'AjzLS2EBfxXoCeSHEhotIQM7w8YFeso2BAmuQmfcA+sCGMvGFgWmPG4PtfmUxroQ6S7QngC7SghgqzbuxIy4iIJEaDLe52OOJD2037jq2gJBZgcZ5xU89YBC43yd+id8'
        b'K9QpzNdWhfXxWTbTbKg0T7KciqFIitgh5jgwQ/Dw2RSXUSbVH5fAIiR033DNThChiISxHYpcUiiUlRXyZYU5pytrU2/2Wb1R30t07hOOMd7ITzPqAGkQ2u1paGivIdxM'
        b'qEiV8cfNm0BIHUmJI3buUr/UsGLYmh+J5ppziA7JY3MIHptX8noypAwpW86Ws+zZLocET2ykgGTcpd9eEcTQr1sqjS1FqxYWV9m4vrOX6HukMuO48Z0lhTyFf+/DLU2x'
        b'OzO2Ti/EMKL4SaHMjVPkJUFjTyE7fGse5K1gBep3ADO/pYjn3NcIxv5Zxk1n+NIgdSZvAkGE+a180kWJu7Wm2W+RJUJSM6aH811zPqck0SydVVbq+6aandMfMB6ltrj0'
        b'OwVj05wJ3XhfC3EFMcJ2gvfNoHiQqPMPnC7wlBJwrTzzsLbCxsw260WTy5XRzxrksSseJQ2uDsWrpG9AP22sR5lxz7yO1ta1ZkvPJI9pa0GtDMa9wIbLp/CXfJK/ZCIG'
        b'+BVJ3CCZGqFylfo+Z26mxB4Qw8m4ThutKmI9Gdi+QqPmQ2o9kKCdaOXJ7NnpDBJah8yREoSSzA+A/129U7t07u53mP8XtYA/68bpBOKENeSCxJTyXTndqktk6Zk2Mw8z'
        b'ifIwYcqSfFKNF/QISYzoQiTm8y1MqTr3tJ4mMvVc+UyaR4UHNtCDemREJAKyV4dqSWZcwDNNIJIEIKvG4SymNLchoQeFCBhmiCYQR4zoo2704NlFdYRuKpNEj4NnwV9Q'
        b'KtdTl86J6kFKnDXtGygfu8/X4g/4fEtTxjD7tAopQ89CC+xGiGvgTIUqQgcSbilnJ7Twrc+3PKW+M6CTcpwDTVf2DT0jvH35N9TC6Dlssuv0vQMXkToY53BIYi8Yij/D'
        b'ExuC8x9M6EDINNOaUIfokh2iR8xwAq4XCU8b9xi3TAkWGlu4TmOLfjCUwOw8N0B/XDJucRrf6RnzoWqhhfluFJvEJmmFzc+UwlCmJ/mlJjsiIZaiY3rEio4VDiaFA0zI'
        b'MKOTpGkuGktHPGtxbZO/LkT+Bc1B+hbSoga2JePe+o9kRfWJORG7+pxZ6bmLjFaeu8ioObnfnBMS2nBOSIigoy0FxAb00J2zoaDEgXwL/KzNCHEm72XyoBJwoc0udQxT'
        b'8SVkJIbpiAIbCG9t8FYxFYD5Jpl4vhVISSb5Piwn2akUQ64Ubs5BfBuBeNxVDtxBJ1N1/ZO1BOLeOUQpdoRMJdgE9/ttcBsqVZqSKQHIPC/9RxnV2cfMZCLdpy/OEXwq'
        b'JcdIvPzuazVJnvUQRzJJhWFJV0kmFnNIjALziGS8l7Nav804utjYuLCyFFXfNi2qXEVrVO1kq/R8fZ99iKFd3PMizUtZpESM0OkhEChmPKl4P6vbFkaai35QF7W1NXe0'
        b'J44ubVyKrgytO3Or0mAmTXICcDyfQEg2RrNLobXtfnUr3joTErizbKRyC9V5XZJpBNZq8De0rpR90IN9ZEmiHWeslFHoVs1aKYACMfjk8C7jPhriAfpDbJT1/Uk8uMrY'
        b'Wl5cajyCSrPGttIS1E5c5TJ2609M6nbmlFjCKFGC7ZsjyUY+rSaeeCVUjSUFfLVYQ66PQ6V0XBl0b0tQHQDPdCgnXlq5CAAHGdG4uy0JncR/f9vQaqXQ8ZiUUP5ijsPo'
        b'xBNPhhb11ffrm4zvGw8bO6fDUjYOc8aROv26bkAlW0B1ZQpQKcmTF7neRmc+zhUiKfbIgOHxvMcB2F+iEx5RsSsOpIUVp+ICWldOOedxrLDTPuAgLO6Ne8wZrwSaXq0q'
        b'6+YQJSFzuodDPZ9GGEOFv10EHtqSPw0FgpdvRAU94JNJ0o4ksqBuTsicZoYF8w0QVH05IJMl5HTDYjCAd5QGQlrhkMOGfjAJltCZHxbm4Ym5Db60WbmI3w4t45KyyHp4'
        b's5XnrR1CRhFwMcIlyaj64x2RRMln7NAv7vKR6NVX09LCUCISAZZvDMr4XwQQ7aq/vrHTh1p/xOnEhUDw3ARbWOAuybKeEwTUwxAQINCDtkSetDMoxJ+HWOPEEQ7NRJJo'
        b't4DfzqXIbo7ghCDiB0BokPB8G0UdPFBmEbFzRxgPPjYyUQeebQcnk/hDIsHFgM5ASAhLeALOjgkV+xYc6qWWKKRJUhywuYTpGwQhmhJYavJ6mGoqowqeuwAx3Yh52Bvz'
        b'OS04tCpZL7Any6DGZVyY4UF3VdxWjYcfcXF+QIlLVRhd3La0pqXDf4bmY8ohGQpqFKlZpjJsJpF7Hs7oJJ72pcS9hY560M4kn5WP43xgLV0l3Ue7ri2w2q+GSOIQTFWi'
        b'YK5EoUgSayY2Ukv0YkPRFoa485tyliDF6WOSl78wBEI4Wgz6V8VtbariV1FwF+xoCRHl3JqUp3zT2b63ewsPSqYwgeM9JvfgAtgSBNQ1zYb7fLSmcuXyXf2+oZ/djtMS'
        b'ArSFHKqrwBKcSXA0MSICUUFaMGSdVIqwRgJm0Zx1Fx2sAaJEDQt8is+WWccDKAIVUAwal2HA/DDtDl99C6o3BGjILJHgNBzaGfgzk/9mAmMOvH8xyTxJ5vEAOb89bRGZ'
        b'FZ2xgxBwaVzqcTEqGYd56EYuHtAQmy+YisbwjsnN4W2I7kS4WxACnBQW0NJkHU/aBoC91vNEucGCgeWhoPQukGE9wTx4lqjY2B08gSHN4SzbFDo7FHw+BmA5lwSaA21r'
        b'AgWJHb1g8LDg4FPy1cOCeLQoq5k4WF/iRzJDZupYfIIOkRjBJiaJWXU8f8aKiKf5Aqiog+6uoYBf4JDmpMBUhimMz+FlIYPvyus+tKmfdkNSCEwkP1K41CM7AhnB3KMF'
        b'dtcIRELncKaOYxqYIQrCb5gxmByWCOcXA86XzFMa2BHqoaQ7BcT8Fi8iq2W8CRrqLPyhBUhnFMCDosd4oC3tKfIUhyUtVXvjunUy+Sj0JWU99izaRBdfv0vStzBGIgow'
        b's2iszsDiZtViFSwBZ4+M56xEw6kLF3SnaM8xJm2SygUWgrsxSeXm9M4YCHyol9SI9W39jR0oeNP3TWBkl3G40tiM3uEG9JH0J/Xr087wRo7/KJptghRJJybTIkFYaACL'
        b'AME3pxMfSA+bpAeplqAQjk1cRtyxqK2uuayxxV/1R1bVO7MSJIhlCZDAShoxoAhOweyQgCzQOt5kEAV6Rwd4OSiDk8LAPvlsJImTSSpnRzMxn8Mko6WqU70wVm+B0uY3'
        b'nfqjZ7ZT9mHBUlRhw8miI225MYj5aFXF7TW1QTxEjztIzU1pVON21Alv6wjFbb5WCm1DIYDjdh/m8CupZ/txCXOoF/E9UcwICp8nocpDdEIW0Qoy35VpDdOZwjwcoURs'
        b'UHQgw/Qdcbmh+Vvn6rUZGi44GB3EzMu4wFLTnnQ1D+iJ57qmhhF18c2iOnMdfierC0jqxcrhmyX18pAdpWHrgOxqcihmOctRww5KQAu0VRnAbkpsrKshtcxiPm1VJzMJ'
        b'm9W1dbQoNNA1dRROoAAH6I+7b8V/D8xaUugENgaGkoYnbmtthsFVL6Szo8XVxInGbX5VBayzBB96Lu4IYHbzTbDF72838V3cDpsMFVV31kUcl7D2v0vmGR5HRpYCeTRw'
        b'kasaiWYA7YK70hJjj9/0bNJTbKI6dbhC8IjMhjXm6nBISdb4m0esuCPaqCsMNGyNwUSHbWor3JsilR44uI4ANiTDliL1RQOTrvREQ1mOnuU5lt4RkotK0sc5OWI7u9BQ'
        b'8QMWy7ElZR8ZKRBJL3s2XRmVUhuCpCloFZiglYTlMDCmUS/JnyX1KhyVi62hUauTDevByMXnA2SL8sO+tsTJuoNIa5i6rJRGmtm6qejif/QJTIbpNH85lpALB8dSUkwM'
        b'1UqmY1JNs1TX0mb6r7N0NSSfv7OuBxEooBZYsQWpE+Y6fVWzPMjeV/BkcNzTVkEjgzWiKIhT/fiz8lzEkwsh0ycWW+qQvC5vpgdFlHaySTIeb78QvTAtNrauZjG99ev1'
        b'73NpTaJL39jcbUewm1fa3BMSD9SZloDtTEg9UCVxhaRkRFkIHDEqRx31MgkinbAzZDJGlYLY4LGME3YJ5okND2dSWdSVhVlxqezCeWXd8F3iiGoeh/JokzCgU2xkBq05'
        b'Q9BSUB9YQiKN0jZFCMksZe4KlpDslPvCtVjRuILVw4Kn0iBhxviGpCU2Y7640IVoe02DP+4J+kO+drVN6agDqt6DX/uWzr+4unxxVdyN78jbLOAnt89nhsH2+ZiGtQ8j'
        b'rVgEWvIE7RumEOsuSsJ4FulTw6pPw2rPZBfPJkk1lY9OZVZDKwpaawLkjhOdtSASWJWEZuY34XSKEXuVaP+4BD4QurKoGd1eVyUag7yF00IJWrc5Q5tmFBZYhKF6pSaR'
        b'6JM0sYG3FIEfJWU+OsSn+wjwG2GxD4dqwfQU9vkmmWktUDm8uk4DMlGxrRe2ZUQk4HbtYYHtWgp3EXcxdynjTlBgQBrbn+G6dA0bVj3/wjkFn2FXmZJeJ3D/LqLH48Ka'
        b'WhMM4jLs9+0dIRqtuE3paG0PkiiJtPnoNC9uW4On7KaAjuExGk/6RKhfee7mxOoa+GSizdItJnNhmUz9kd7Mop0qm+9y0/izhsWdC/wtq/2hxroaFQOxMvNGnIQ6S7iU'
        b'njojLTxjhNCqDxkfuMqkJoQsEL9eNFcSjS/dA9sDhLmIbzQ+ZAP+z5ZNthHo34Gl+7G0Q5EjTsUecTEpQcTd+RXMtptUMz+OeIDA9/TlImlhp/qslTOcBnOJEojdijOS'
        b'FhhAaRekH1Pc8Naq3YG1r1K7tybsCQOlmcs1c+rbWLbi6cP15drfgZK8YW/bB0pa2Nts386r08NeVgvcDwh74BdLtptYA0pUvGE7lqiIESe0wcvaQF/Ce1SHZjXie1TQ'
        b'UOxhWzgt7IK93tmEv+4mj5K5RYbyXKqKuVapwBPLtOFmVZ1E27OTOAtLTuJ8/zGa88uXvqz+fFYZSTdOiTNmzKBpi4s+wBn8ElNnuSDOnx+3z23rUBsB5fDlqLIb8K/x'
        b'dbLL2sI0psnuIlXTlsaAP8hQUWuN2tAYCMZ7YaKmI9RGKMxXCxiqOe7Ah/VtAaBi1baOgMKE/ggWcanO39ISly69sC0YlxbNL1sSl5bTfdX8S5cUpjP4pmNriQqQyIrE'
        b'FgytBSrYjQ3wrfQ3NqyEollrXJjB1wLN8Zv3wLpCFTbVD62Iy7VMRuIMdLT66AumEivhPTz1d4bo8T+MQu1mio6kzzzPZnIQnBnw0kNHEhlkBMEs8JnvQpfpY4N8bgj5'
        b'lFOmHGzJSeaSQ3UkWnAplXSTpsjWDqVy3dcW4q+2PDpfRj5moSLEODQIConEJ+HO6UC5y3rTjUVfNKjgFTnM5zDFPgkVlHkuZDNFoHKCHRZJEOogBO88lXd+jYrGvwXj'
        b'2+qnFKCiVgF5JAh2tKqfISwVnYtldElpwdDRRcO6UU0JsTAiJDJs8kZ4zWT0TZOmeksSh2J6y6gpr0fOB+2ZVGsnkbmugTSw2PTxU3oyZzqJlsOnpFHDgqNorVQBj/wf'
        b'nCluQ0sZhVSr4yL0NO4lyG4EHryuraVNNfE3K9zizV7pvgd39w/640Q774fWt9gssRN6LCLrOhTwm9jXLJaI2KuRLEsgXzV8dqIuyJtIXv0eb1aTwv9/a3dHSUlAI5Q0'
        b'wpaQBGTYHVKuN3tkB8p4xuk3rQnqjxh73O2rRE4wdvOD5hq7iLytqqpCDSuxA0+g9Ifss6vRk93jZGkX0ffjWzJXXTOS/H4tUOSrPI72C6DussZb5tSLQQ3Is78Nu69y'
        b'SeOy6mXZkbk33LJh7Q2zZ2c2+B3CxnmLlKwJBfLlqzvejvz80ubLHl69YOaw5jt2pn/1x4+ufnz/h11F06rS/nTn0ZfDH61/6NHfcde/lDm3pFevrvMXNW3Z9Ypr7MH5'
        b'tfc8eWLz0tjyO0b84c/ewxUVJwJXDPriXf7wskla5InZH7w+47fXvT3E+17OqgWLY0bXpsl3v3/iorcGbT05fNXlr//2nZYfVG+fsvalz6RPP7x//LPV1+8rX/Tw3vte'
        b'//jCZ0K/av5r5V1/Gv+Y8uv1N1zw9q5Fzw4qrXuk/8NfVb39fO3AZWMaXt65e0TDlRPvzRvR3vv1AyHtQNGNA3/26dRA7vLxLX/5uHbmCamk617fxiODh8Vvvnew/eKb'
        b'dt9+4q3HYpd96Hnqz6/+Nv3koPczp/R+4EeFbz7bf//7jZ1pd0393e+efnjg3mj5lC1HH9u0ttd3D7y5dUThrf7h85fvzPzxC5nvv3QVv+lDx6apv3JNK3whVtw8vqrW'
        b'Of+9jV2xJxakv3/lW88dKTv4zJdDK6uW3/n8oek3GZO3XH1pzST7Ox1leXv+cKzprrxrex982vnGb37xWca1r5TOfaHfkZHiuBMbX3jx3vNn/e3FKddeNGn8wBN5H932'
        b'3hsH5w15c+wnpa+WPheYsT06bs4fxr5/9XUd9Y+97bq05tmPP87o15reb+D6pQuW593rbWga8WpJ5Mg7XdN/cuDLKfvyB9S82rFS/+SJ3L0vH/5CuWtG1+ZPbftuPfbU'
        b'xF5FTyz/xaVX2xbfvu3K/QNzjj562RurX5lZVPJC9r3T3uh45aLADb98MOupD8bekv3Fxz//6IKffPpQ8NEvVr3zhrF09auBZVpD50f/Wb30mi1vjvLeceBXPzk09aPM'
        b'KyevveW7v8sd/dOq8VXxTxceO/ibE5fk/rLSV3vfvk7/0R9/POAr/6SrL7r567d+VrL2x18ff7ZP/cKfHvj8q0nn2T9dN/b4iWWBrimvH65cW/bX1//y7O/HrSzJO5bb'
        b'cKDtk7dsx8e//fGUD2efv/zrP008kfm0fXLju+qMYzvT/nrzM+nay//10rGq13dO3zfhxC+nPPWX4X+Y8P6pzLYPSjwHlv1aebn4vc4KX9uHr/2laudNrU3X6NOa3j65'
        b'esbBmqI5kdfeO/rnz8e/Xf3lnasG75xz9P1r+7747qIZv3y3ae3ERx448OOv7Mt/OHFSx4r6x4Ydf2fZ672mDbzMr3900Y8+mNH3+G/EIeH/ePLzzbFn3nU+N+HRD3b9'
        b'NXJixLiZt754ct9zjTvf/HDtcn/Htl8evmLKOy99vfVl5ZrXftH12l9/u2aZ+6vRz0z7YlzD3zm+3+Frf/iLQjc5wLlGv9G41dhUWVKubx59rX7zgmIjxnFZ+g2ifkzf'
        b'10K21Ev7iuS+VjaerCoZhabSDwv6zSONo2QqLRh3jzDDX9dfZoWyNaNf31LLYjPdqT/QdabOonG/fqtUNlF/iHxdDhuJXvTxCNS5oDjjklEoe0zXj4s+/UFjfQgdWa/W'
        b'93BFVSVkgmgWhfd4PKxvZV6ijPX6RnZIHJ7qkvR7jK2hCdSAxfrdKQ0or6woNrYUnna0bKzT74Yvr61wcRH9UAglFEqFvqXH039jz1Upx//6PTOphcZmfdvyYCnFGdrW'
        b'0eMRdiYOEDZwjbHbCXh2r5O5BN1dmkkNfFLf16MA9qC+PYSkYY7xWGvQ2L08iZ7n9wdq69vsBf9gp5j0Lyzs/5efwkFst/53/7EESy1tNYoZEPJN+OFqZDKlP/c/l+h1'
        b'eiUP/GW7Mhw5vbKzBX7MhQKflyPwQ4uHTsvv57XlzpYEgc/lJ7aMXO3hHQ5MDc8U+MHwf0CBwGfL8N+R5xL4LEngc+Tk1evEe0wNzkfxao4H/qfjXXbGAN7VhjrfXiHD'
        b'ljc4m/fkZ/Auu4f3iPh+AHyZz3sug9/zBL6A91SpDyTkXKmuVf4Xinv4SdLWOGhXcRbNendnqrcFipr2uP7EGkDHWyYwB3yLF+kxfZud8/YV++vbJaDnJtmCgwDAfm/f'
        b'UrLjx4Ffjcm4obz85h88+7fAc1s/fGP5D5TqVz7/j4bnH963bsFly39wz5QdD/1kys/5a146uO2VuQPvTf95Zj/HO1+uuiE/zXlN5sKyry5aef6wL3e8tii69pnQrbb7'
        b'nssfN/7F+5wDpc+e3fDr6tcW/eW83w99a+C90yoem+v8zfr94d4/UAofOpK9a/bvZzpvesj9xR7nF+qIRdu1g3/73aP3dt77nKfXoZU3/OryvOrvTNjnGv5G17Zrl3x3'
        b'XcOejQtPlLa+OPzTJYeLljS+P/3ryE/uX//UV4Wtr/26fOdi5cS1d3/n4eLLbr11b3Day5+Fnym+cP1zg3/aWfyzgz9d1f8ny4uOfn7gkjf+cPmT+cs6ttyTPXHFH999'
        b'fsX6D0+s2Pnhiys2ffj8itsWf3C/a82b5X8a/14g0jTipSs/ePPEJb84VPD6F2/trX5h5hVjmz+Znf7AofQH7r8gVPzqztd/d3hA9SUDL5q/+N0VXx/fUnjFipfu969d'
        b'VPfClJKSPj9/ePqemUcz73pv/E/eeKryi+CnV75fvGbAl+/PL/rozUcfqX9BPdS77c82Z6R86xW/2vrQn8/r/16/FSe3Tw0P3P/u0o5HPhr9x0+OZh078vlHq28d2uup'
        b'X7oLd7VVnrrvvvq8p6rf2vfl1YdOfD3n88l3nhp+akGfjO3t73w67dPt12/jlv/n9gv4+fnf2+x68P49W+XdK/ds8T7x7p5t/A2TTzjq8mvWFdZPfjbfffs72Q2Tn8sq'
        b'OnD4h7bSVd9pfrPgxIfGHe/t/2HF6j+OuCb++6MPnXjq+cjf7IN//NrXC48XziQyYUqtpG/iLiRo2mxsKjbB6WJxrPG4roUGQRbjiH5gur6J3M2VF1+oH4BtHTNl6j8Q'
        b'9Z3TjbuYx+tdk42DxqYZYxIhKDH+pH59CW2PxrFp/mb9oSL9ULEM2+P1/FX9ZodQz6a+kiuqKBmFHoiMbRiHTtf6o0/tTXZuULUtSz/iDSG/aRwyDuu3JV1zd5QYNxnb'
        b'U31zG/cYN5ETmTnV+tMVg/XbIK+xuRBzF8lc+iSx+RL9fgqNkWYcdwPh9ODloxcYW6CdCzAa1xOtIWSR9XuLxq0wohXG1pECJwT4mbOvoN7N0O/QbyxCb9+LbZxsXG8c'
        b'mi149d1AAVGwjQcmTiBSbGQJz8n9J3QKY43v6cxXuK4ZDxjXVeBr/cGWwnKgHBz6cUGP6seMB2hs9K0LjAf5YqD2gDsWwvwszriN3OwMNo5fOugyfb+xEV/oR/klK/Wn'
        b'yMnNGP2QfnfScVMv/Vie4Go0jtFn+iPTbWsyyMkdfBbhy4D6uo5cMup3L2+DL+81Ni0u5aHEjfwFacY9ROiM4q/S9+uPBtGxQeGoBcbNMARIWSEtNWyCbZ7+MJBeCA1h'
        b'407jCTcQnFdNqihxjTQ26g9h0NA8/SkJxuMB47ssqnNUP1JDDrBgVErLO2HENlcAddlnpTSuuIUac41xTL/bZ+w1NmHEQ0HfxZcN1Xewdm6YN1pfp99XZGijMXTz/fyy'
        b'VuMhenWlse2iCTqQxuU4d8K1/Gz9uL6FaGZ9vXGLfqCC0CLMVKHMLTN2uPXrBeNe47i+m+UBKk5/VN+0eHFJeZHH2LuQvIllTRNhlB8xtrAZu8u4fWKFcdjYwWK6Lq6i'
        b'wrzXiPPmzyMoQXJxF7Rb5lA6P8vYu6yK+R66VehfVGncb8VoxQCt+hH9VnKNNFx/BJ0kXmbcpD/A3EdItbz+tH6TsYEKLck0dlSUFC6ED+WLwtVCjtNB37n0g6UVBMzl'
        b'5RQV7ia3vkuASjYW0oTkGfv0wzCjRAwvNG42XRpm6etFjOmiH2Sd2m5sqKnQ79PvKi8uLzEb6DU2ilUjjG0ENnP0h90Vq/TrKcqrJPH6XXP0IzSZOVI7W3WV5UDxbgMA'
        b'KYfyjZ2i/oRxrBd51h+X6ypaZOwp1w+OLBy9EMA13dgr6te5AJIRxDv1p407K6oiRQvKYcHl8fqesaNo5Qw2duUbm+bq+xEDAIMiXcTrT6b5QyjKMDZlXFy00MbxFVxf'
        b'/XZj1+X9zJ7MgLybFiBsadBZgRs/xh0WjNv1x4wjNA3txi7o7ib9riksqKWUweu7L9avZ/EuN8PCu6FiYbFxt7Gj6rzxPGc3dghyjkCF9zaebLN8Mh7X70j6ZNRvs3xU'
        b'3SCcz1wiQjnrUnwilpkL3rhzpL6jQnKTB19riXr174lzjRvm03hevKQ14SyT5ko/btzBnGVKsFILCA8ZG6YmXVWO1I+keqr09AqNxpoe03fmGZsmAHyWwEoZBXMEK3YH'
        b'IJJFNDabK0r0ByWuUt9vN66/ZhFbAIf657iRm2wnjLRhXgUCVbZxu2jcZ9w2gOKSVvEj3MbW0SULqzrodNF4GAkNzHfeAgBguRzay5a5HWD6acJ8pQsqAaXoe/WjbuNu'
        b'wXgUvrmHhR7+jvFEOXlyRWZLBhZ0s1s/KhhHR7TReLbW67uKjK2LjG0VxZMDhSUw4b0GiMZOpHQYC7YzQ19fgesVhiNWXrxwtL7DeBrqk7lizmbcCovqAEVSBBSljcN9'
        b'Ci3qFhfCQt+r31Kub8G9KmeYJBpaHk3QFOPJYnT2u3gxblQVds74ntOtH4Elpd8o0aYEK//OqxBEtuoP6vcvWo2wCRh8kZ3raxyVlus3tDBIjOmw2qBpgCtii+cWLMYg'
        b'OJkG7Ip71rJtQ9+0At3YGpu95p4mlfD6wSmwKmhTW2fcqe/CFo+ucBpPJHdBbHG/oRIhtBjD6bv1vYsryitHVdo5ea2xQxIcM4pofH3GI1eSR1jocHmJDHtHodu4F0Bp'
        b'ef256iKZ7OX/PJv0b/eTOMgllu178MO5BcHBn/7nAqaIaaCgzzaJxzxe9sY8ojDZN6ahJ7jMO/hOwDBLDvI/lN2tTA+VR3ngjYcMbx10hugRZLHzWu7MvyEyz0TUTL0A'
        b'lS2C/lBHu8+X5MAsOf+DfGr/8IbxHF+m+rKkdwl9gjT4j44z8DQ/eAJ+a9HFCvzFlmpL8XQkNgKuAlwFuIpwzdGW1nNwvURb2ohXl7YUbdFiAzE/nhjH+CgfXVovMBOo'
        b'CIcaBy1iqxRLb7VF+FY5IrTaI3hqJyuOFkerMyLRvbPF1eqO2Oje1eJpTYvIdO9u8bamR+x4JhjKgNJ7wzUTrr3gmgXXAXDtBVc0kZXhOijMaelwTQ/TWUjMHSZjhFgG'
        b'5MuGaxZce8PVC9ccuA4Lk6JjzB6WYoMVOdZHEWO5iifWV0mL9VO8sXwlPdZfyYg4lMyIU8mK5YVFhdP6oj52bIjSK1aoZMdKld6xxUpOrFLpE7tQyY1doPSNlSt5sVFK'
        b'v1ixkh8rUvrHRioDYmXKwNg4pSA2VRkUm6kMjs1ShsQmK0NjE5RhsfOU4bEZyojYbGVkbKJSGJuujIpNUopi05Ti2BSlJDZeKY2NVUbHKpQxsdHK2NhCZVysWhkfW6BM'
        b'iM1XzovNUSbGSpRJsYuUybGLlSmxKs21nosNVabGzg/1gbtMZVpskTI9NleZEVuizIyNUfjYvLAd3hRoQtgRdtbjKGVHvdE+0YHRynpJmaXMhvlzhV0xD2mQJD2XeqPp'
        b'0exoDuTMjfaN5kX7RQfAN4OiI6Kl0dHRMdE50fnRsuiC6MJoRbQ6uiR6CcDDIGVOojyH5tUcWuF6IeaMstDorFwPlZwRzYxmRXubpfeHsgdHh0WHRwujo6LF0XHR8dEJ'
        b'0fOiE6OTopOjU6JTo9Oi06MzojOjs6Kzo+dH50HN5dFF0cVQZ6lyfqJOG9RpozplqI/VhOUPjxbBFxdEy+vdytxE7rSoSL7f0yBfVrSX2ZqC6FBoyQhoyVyooSp6YX0v'
        b'ZZ71TcStecNuqmE4feuGWtJoPHNhhPLh6yH0/Uj4vihaEh0L7S2jci6KXlzfV5mfqF2EtopUknSNC+cx4tGGaR5tlOYJe7Ty9QKd+uOTYnpSzJ5c4wm76Wy7jDmZJ/cP'
        b'dGjds2IYUiXMaEfjmp1qXgi9UHBNvKVObWrJneo9LDiysKCR6WjWFNR2NLaEGgOFgnoF2YCl7Dhn85jkqw+QoAy1vzbbEj4l8DhXPWAZiBRKgN0a/KF6FU0SHP7OOlJh'
        b'IYNnPKRuq497LBUeUt3h0R9GK6BDuHOhm+XWdtUfDEJKbGlrQLNYVO6i4AInsdMnSQcD23WyE38wMt9JMhlA/eQ2xQ9IldwRoFZ3XGxva4+7oHTFX1+DpgKOeh87CWWO'
        b'aJLuChKIOC7XUzlxd12br0ZtoCiYGL7T17ymLdCyNvHIBY8CrLC4B+6DoRrT96MDUvUtNQ3BuB3uqDAn3QSCoSC9JV10qmF1jZpMoMorpug7uvHSUzVIKgiBNiqnBaaw'
        b'ppZ9oPr9q9GdNiZQw4AStroWf40alymEx9i4WNvYQHrc6BqFRVyIuzBYMrtnKjfHzEkOqTV1foyo6PNB9lofm0g73KHKQFzyqf76uNenNAZralv8vrqaupVMSxcAQ2G+'
        b'u5CePSWMLOwW9w4nEDkLijqB9maWh3T0LaQxj2M55K3QS34PyZNOhF+Vv8xy9MRX9aye9w/9BSFw/iGh8UUkgMsC2kQbUbVLttr4LLzR7IDePLCs+mI7wjwgHqEeLRcG'
        b'KBQ8hewZRK2AVK6ksKS5mh3qOs0TsYUFzd0sqAvgXg6MpBSnXql53FzEpjGrOkFzaVnwxgt99/TBsZA1O6T7rxfCstYbXW0GDqHnkuCN8HSAllOPflV2obIV1NQLavo+'
        b'5c+F7/OxvMB18Hyglkn5PtAyAd3YOwvI9is34oC8di0b8kqwSYimSdHzMLISelahMuVmx3ZeHaPJ8KWzs5RK7wc5LU8sLijF/DrshDsX3lHQGTRRcVZzbCQ0nsrR4Ot0'
        b'Lc1tWqGFRS2D3qblottYYAsVLuzGd2EB0G1aH44ZR5HPSydzQ59QZqORhTLvhxlxaXlQv4AjFLZlo1VILhsPeP8MtbmPNSKm2YwFNZ7/y/OM/3lp9LcSWCNsf4wwX0VI'
        b'2ssIVSJVUetGFhykj5OFf6JEOpAeIoRziZiV+Rw+j5dEr+AFMjcfvxNd8AzWjZBYMpnmHkRL5ueCuWS8MM2F5pLJTl0y8FbEidMk2KfGdFtEOHFF8I1Edwj+trAU/IDi'
        b'xMsa/uWsJ4uoCACyui5sJwMXRxhqY4ADiyZvOhdYqfXThmjDYSH0rbcBGD8fdgL4XhhxaahV5oJy3WGX1g8W5xsAduluri/uyiLce/E+7KHlByWF3UAfppvg68Yc7F3Y'
        b'NZ1bdfMyLhDQhmppWr96ThsC/4fD/4HayHpey8SatIG4xLKBwoTneRqvZWgZSJk12mmZ2xCIYTllhh3QozQAeLiGYWlo3lwu4tWygB7AJ94+HCybNKIT3PBVMcWE6qQS'
        b'4L4eer2Vj9gCH8ATWRsFZaaH07Vceg+IAdqbrhVQqsBMDaXUUDM1jFLDzNQASg0wU3lWOynVj1L9zNQQSg0xU8MpNdxM5VMq30wNptRgM9WfUv3N1CBKDTJTAxPjhqm+'
        b'lOqLqfp02CZKkLoPc1sRgSISgL5qI7Q06HFGOGO70L4uLNGvfbsQfJDgpQ/CC5QBY1+PXqfN3vTh6slBm9YL4QxKFclJgIQjT06t8HlRWCIdSKmbR4PM/ydLtrD03wBt'
        b'/PejpkLYaoPrkqgJVQIFh+lPWRa9LCiXJPDsT6bQJ2j1mw05s2UrQDL6Yc6Q0BYYnT95hCzRBQjLy5/tL0vwiBmA8DCMcp7oEZGXT6AzyxcqoTPm+RAQlgTA4zDRmaxx'
        b'KehM1Gy0kwOlojmBwAc0xpSru3nj6ZE4+Re4sqdhvEW2LOTZMIo4EN065LY69CB2SIL1gCSHABg4i3WC6VOic2nU9NYy1gtqMb2RwpQXOpimYUQLXEXpgJHSNDtLoc64'
        b'5to2nMdy3VoWrjgcKsJWog3wqeacBLTf9BRtccBsgCNNjWe8z9AcTPs5TD7gcTV2I/Z6Hr5e/73Qep+cYt8kCWRvbnfx+SLeMThyJeEIC8iyhj2AlCRQfVo6UrmJYZfY'
        b'sLcNp0HvDVSXGGTDjukcTCMFQ169gUIEmFtIb13b8mjg0JDcnktK+5jqNsRAs2l22LaAJoXtYmVYDG626Gkey5eAOoTts7MsbFPfxACDiCxhY7LBJgKTGLGvdYVJgRu2'
        b'uWyJC3HNLvUl5jGFBUqkb3KxjFW7lnHEZHuB4e8VzY72qbebwVAcyZqAarSRyne+lobPrO/ZxgYkgxNWFbW1c3rYBtf6RA1OFGrQt5fCt/AM3jgT3ybaAVRo8bKU0LGp'
        b'Ni7dnLImovIh4wFdhmGmUALoYgHjt6D7wrZiJD3JSn5D0lmSGBdCtepxZBWf57+1P4u4tzHoa6ut961RUdNZ/VROGKBIpAztYuwI8ODIj/9T4SL6/jsh+Gdl06ooZckI'
        b'TPMbNcCzAJXLkkTG9qg9g8aCyJPJTq+Ya8enWXavKabN4gtzmYCBVHLRNiQuBtcG1YP47BD+PIQ/3ye/AXXowyWoHiad+66Wxlr1CN221oRWqkfJRBlu/DXo1189RlYk'
        b'jYo6gAoF5jsu1tQC276yJoiGzHG76YQobg9aNw0tbbXA8hem/WuGrHDZv4E8/X9//pkDCITJiM10lcoJgnT64YPXlkvHBXg0cObhBPuTevjz9Pj0n/+Tzf+JtOwRs+yS'
        b'uOg8WIFifRP+FngkcUw+3k2fi+tScMjEHQoC9bNqSaGo4mmLijiVxfpMV/dy5NDflyrR8/nMJdpa0w7rNKRivF2yfSULfnYQcoAW4vzOOn87eu1V8dgOj0XqajqCfp8v'
        b'nu3zBTvaSRKIYjM0C4Gnbl8yof68uyOGFEPR6a1tSkeLfyadh6C4SRKATBSAOurpcCZsPh0skEdVS6Pv/wBX8z7P'
    ))))
