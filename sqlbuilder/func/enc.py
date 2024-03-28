"""Encryption functions (https://mariadb.com/kb/en/encryption-hashing-and-compression-functions/)"""

from typing import Any, Literal

from .base import Function
from .. import Statement


# pylint: disable=too-few-public-methods
class AesDecrypt(Function):
    """
    Decrypts an encrypted string using AES.
    """
    def __init__(self, value: Any, key: Any):
        super().__init__('AES_DECRYPT', value, key)


# pylint: disable=too-few-public-methods
class AesEncrypt(Function):
    """
    Encrypts a string using AES.
    """
    def __init__(self, value: Any, key: Any):
        super().__init__('AES_ENCRYPT', value, key)


# pylint: disable=too-few-public-methods
class Compress(Function):
    """
    Compress a string.
    """
    def __init__(self, value: Any):
        super().__init__('COMPRESS', value)


# pylint: disable=too-few-public-methods
class DesDecrypt(Function):
    """
    Decrypts an encrypted string using DES.
    """
    def __init__(self, value: Any, key: Any):
        super().__init__('DES_DECRYPT', value, key)


# pylint: disable=too-few-public-methods
class DesEncrypt(Function):
    """
    Encrypts a string using DES.
    """
    def __init__(self, value: Any, key: Any):
        super().__init__('DES_ENCRYPT', value, key)


# pylint: disable=too-few-public-methods
class Encode(Function):
    """
    Encode a string.
    """
    def __init__(self, value: Any, encoding: str):
        super().__init__('ENCODE', value, encoding)


# pylint: disable=too-few-public-methods
class Decode(Function):
    """
    Decode a string.
    """
    def __init__(self, value: Any, encoding: str):
        super().__init__('DECODE', value, encoding)


# pylint: disable=too-few-public-methods
class Encrypt(Function):
    """
    Encrypt a string using Unix crypt()
    """
    def __init__(self, value: Any, salt: Any = None):
        if salt is None:
            super().__init__('ENCRYPT', value)
        else:
            super().__init__('ENCRYPT', value, salt)


# pylint: disable=too-few-public-methods
class Kdf(Function):
    """
    Key derivation function.
    """
    # pylint: disable=too-many-arguments
    def __init__(
            self, key: Any, salt: Any, info_or_iterations: Any = None,
            kdf_name: Literal['hkdf', 'pbkdf2_hmac'] | Statement = None, width: Any = None
    ):
        args = [key, salt]

        if info_or_iterations is not None:
            args.append(info_or_iterations)

            if kdf_name is not None:
                args.append(kdf_name)

                if width is not None:
                    args.append(width)

        super().__init__('KDF', *args)


# pylint: disable=too-few-public-methods
class OldPassword(Function):
    """
    Hash a string using the old MySQL password hashing algorithm.
    """
    def __init__(self, value: Any):
        super().__init__('OLD_PASSWORD', value)


# pylint: disable=too-few-public-methods
class Password(Function):
    """
    Hash a string using the MySQL password hashing algorithm.
    """
    def __init__(self, value: Any):
        super().__init__('PASSWORD', value)


# pylint: disable=too-few-public-methods
class MD5(Function):
    """
    Calculate an MD5 128-bit checksum.
    """
    def __init__(self, value: Any):
        super().__init__('MD5', value)


# pylint: disable=too-few-public-methods
class RandomBytes(Function):
    """
    Generate a random byte string.
    """
    def __init__(self, length: Any):
        super().__init__('RANDOM_BYTES', length)


# pylint: disable=too-few-public-methods
class Sha1(Function):
    """
    Calculate an SHA-1 160-bit checksum.
    """
    def __init__(self, value: Any):
        super().__init__('SHA1', value)


# pylint: disable=too-few-public-methods
class Sha2(Function):
    """
    Calculate an SHA-2 checksum.
    """
    def __init__(self, value: Any, length: Any):
        super().__init__('SHA2', value, length)


# pylint: disable=too-few-public-methods
class Uncompress(Function):
    """
    Uncompress a compressed string.
    """
    def __init__(self, value: Any):
        super().__init__('UNCOMPRESS', value)


# pylint: disable=too-few-public-methods
class UncompressLength(Function):
    """
    Return the length of an uncompressed string.
    """
    def __init__(self, value: Any):
        super().__init__('UNCOMPRESS_LENGTH', value)
