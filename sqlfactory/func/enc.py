"""Encryption functions (https://mariadb.com/kb/en/encryption-hashing-and-compression-functions/)"""

from typing import Any, Literal, Optional, overload

from sqlfactory.func.base import Function
from sqlfactory.statement import Statement


class AesDecrypt(Function):
    """
    ``AES_DECRYPT(crypt_str, key_str[, iv[, mode]])`` — decrypts a string encrypted with :class:`AesEncrypt`.

    ``iv`` (initialization vector) and ``mode`` (e.g. ``"aes-256-cbc"``) are optional and available from MariaDB
    11.2; ``mode`` defaults to the ``block_encryption_mode`` system variable when omitted. Since the arguments are
    positional, ``mode`` can only be given together with ``iv`` — the overloads below make giving ``mode`` without
    ``iv`` a static type error; a caller that bypasses typing gets ``ValueError`` instead of a silently dropped
    argument.
    """

    @overload
    def __init__(self, value: Any, key: Any) -> None: ...
    @overload
    def __init__(self, value: Any, key: Any, iv: Any) -> None: ...
    @overload
    def __init__(self, value: Any, key: Any, iv: Any, mode: Any) -> None: ...

    def __init__(self, value: Any, key: Any, iv: Any = None, mode: Any = None):
        if mode is not None and iv is None:
            raise ValueError("AesDecrypt: iv must be given when mode is given (arguments are positional).")

        args = [value, key]

        if iv is not None:
            args.append(iv)

            if mode is not None:
                args.append(mode)

        super().__init__("AES_DECRYPT", *args)


class AesEncrypt(Function):
    """
    ``AES_ENCRYPT(str, key_str[, iv[, mode]])`` — encrypts a string using AES.

    ``iv`` (initialization vector) and ``mode`` (e.g. ``"aes-256-cbc"``) are optional and available from MariaDB
    11.2; ``mode`` defaults to the ``block_encryption_mode`` system variable when omitted. Since the arguments are
    positional, ``mode`` can only be given together with ``iv`` — the overloads below make giving ``mode`` without
    ``iv`` a static type error; a caller that bypasses typing gets ``ValueError`` instead of a silently dropped
    argument.
    """

    @overload
    def __init__(self, value: Any, key: Any) -> None: ...
    @overload
    def __init__(self, value: Any, key: Any, iv: Any) -> None: ...
    @overload
    def __init__(self, value: Any, key: Any, iv: Any, mode: Any) -> None: ...

    def __init__(self, value: Any, key: Any, iv: Any = None, mode: Any = None):
        if mode is not None and iv is None:
            raise ValueError("AesEncrypt: iv must be given when mode is given (arguments are positional).")

        args = [value, key]

        if iv is not None:
            args.append(iv)

            if mode is not None:
                args.append(mode)

        super().__init__("AES_ENCRYPT", *args)


class Compress(Function):
    """
    Compress a string.
    """

    def __init__(self, value: Any):
        super().__init__("COMPRESS", value)


class DesDecrypt(Function):
    """
    ``DES_DECRYPT(crypt_str[, key_str])`` — decrypts a string encrypted with :class:`DesEncrypt`. ``key_str`` is
    optional; when omitted, the key is read from the server's DES key file. Deprecated; removed in MariaDB 13.0 —
    use :class:`AesDecrypt` instead.
    """

    def __init__(self, value: Any, key: Any = None):
        if key is None:
            super().__init__("DES_DECRYPT", value)
        else:
            super().__init__("DES_DECRYPT", value, key)


class DesEncrypt(Function):
    """
    ``DES_ENCRYPT(str[, {key_num | key_str}])`` — encrypts a string using DES. The key argument is optional; when
    omitted, the first key from the server's DES key file is used. Deprecated; removed in MariaDB 13.0 — use
    :class:`AesEncrypt` instead.
    """

    def __init__(self, value: Any, key: Any = None):
        if key is None:
            super().__init__("DES_ENCRYPT", value)
        else:
            super().__init__("DES_ENCRYPT", value, key)


class Encode(Function):
    """
    ``ENCODE(str, pass_str)`` — encrypts a string using a password. Not cryptographically secure.
    """

    def __init__(self, value: Any, encoding: Any):
        super().__init__("ENCODE", value, encoding)


class Decode(Function):
    """
    ``DECODE(crypt_str, pass_str)`` — decrypts a string encrypted with :class:`Encode`.
    """

    def __init__(self, value: Any, encoding: Any):
        super().__init__("DECODE", value, encoding)


class Encrypt(Function):
    """
    Encrypt a string using Unix crypt()
    """

    def __init__(self, value: Any, salt: Any = None):
        if salt is None:
            super().__init__("ENCRYPT", value)
        else:
            super().__init__("ENCRYPT", value, salt)


class Kdf(Function):
    """
    ``KDF(key_str, salt[, {info | iterations}[, kdf_name[, width]]])`` — key derivation function. MariaDB 11.3+.
    ``kdf_name`` defaults to ``"pbkdf2_hmac"``. Since the arguments are positional, ``kdf_name`` can only be given
    together with ``info_or_iterations``, and ``width`` only together with ``kdf_name`` — the overloads below make
    giving one without the other a static type error; a caller that bypasses typing gets ``ValueError`` instead of
    a silently dropped argument.
    """

    @overload
    def __init__(self, key: Any, salt: Any) -> None: ...
    @overload
    def __init__(self, key: Any, salt: Any, info_or_iterations: Any) -> None: ...
    @overload
    def __init__(
        self,
        key: Any,
        salt: Any,
        info_or_iterations: Any,
        kdf_name: Optional[Literal["hkdf", "pbkdf2_hmac"] | Statement],
    ) -> None: ...
    @overload
    def __init__(
        self,
        key: Any,
        salt: Any,
        info_or_iterations: Any,
        kdf_name: Optional[Literal["hkdf", "pbkdf2_hmac"] | Statement],
        width: Any,
    ) -> None: ...

    def __init__(
        self,
        key: Any,
        salt: Any,
        info_or_iterations: Any = None,
        kdf_name: Optional[Literal["hkdf", "pbkdf2_hmac"] | Statement] = None,
        width: Any = None,
    ):
        if kdf_name is not None and info_or_iterations is None:
            raise ValueError("Kdf: info_or_iterations must be given when kdf_name is given (arguments are positional).")
        if width is not None and kdf_name is None:
            raise ValueError("Kdf: kdf_name must be given when width is given (arguments are positional).")

        args = [key, salt]

        if info_or_iterations is not None:
            args.append(info_or_iterations)

            if kdf_name is not None:
                args.append(kdf_name)

                if width is not None:
                    args.append(width)

        super().__init__("KDF", *args)


class OldPassword(Function):
    """
    Hash a string using the old MySQL password hashing algorithm.
    """

    def __init__(self, value: Any):
        super().__init__("OLD_PASSWORD", value)


class Password(Function):
    """
    Hash a string using the MySQL password hashing algorithm.
    """

    def __init__(self, value: Any):
        super().__init__("PASSWORD", value)


class MD5(Function):
    """
    Calculate an MD5 128-bit checksum.
    """

    def __init__(self, value: Any):
        super().__init__("MD5", value)


class RandomBytes(Function):
    """
    Generate a random byte string.
    """

    def __init__(self, length: Any):
        super().__init__("RANDOM_BYTES", length)


class Sha1(Function):
    """
    Calculate an SHA-1 160-bit checksum.
    """

    def __init__(self, value: Any):
        super().__init__("SHA1", value)


class Sha(Sha1):
    """``SHA(str)`` — synonym for :class:`Sha1`."""

    def __init__(self, value: Any) -> None:
        super().__init__(value)
        self.function = "SHA"


class Sha2(Function):
    """
    Calculate an SHA-2 checksum.
    """

    def __init__(self, value: Any, length: Any):
        super().__init__("SHA2", value, length)


class Uncompress(Function):
    """
    Uncompress a compressed string.
    """

    def __init__(self, value: Any):
        super().__init__("UNCOMPRESS", value)


class UncompressedLength(Function):
    """
    ``UNCOMPRESSED_LENGTH(compressed_string)`` — returns the length that ``compressed_string`` had before it was
    compressed with :class:`Compress`.
    """

    def __init__(self, value: Any):
        super().__init__("UNCOMPRESSED_LENGTH", value)


class UncompressLength(UncompressedLength):
    """
    Alias of :class:`UncompressedLength`. Previously rendered the nonexistent ``UNCOMPRESS_LENGTH`` (MariaDB error
    1305: ``FUNCTION ... does not exist``); fixed to render the real function, ``UNCOMPRESSED_LENGTH``.
    """
