import pytest

from sqlfactory import Eq, Select
from sqlfactory.func.enc import (
    MD5,
    AesDecrypt,
    AesEncrypt,
    Compress,
    Decode,
    DesDecrypt,
    DesEncrypt,
    Encode,
    Encrypt,
    Kdf,
    OldPassword,
    Password,
    RandomBytes,
    Sha,
    Sha1,
    Sha2,
    Uncompress,
    UncompressedLength,
    UncompressLength,
)


def test_aes_decrypt():
    aes_decrypt_func = AesDecrypt("encrypted_value", "key")
    assert str(aes_decrypt_func) == "AES_DECRYPT(%s, %s)"
    assert aes_decrypt_func.args == ["encrypted_value", "key"]


def test_aes_decrypt_with_iv():
    aes_decrypt_func = AesDecrypt("encrypted_value", "key", "iv")
    assert str(aes_decrypt_func) == "AES_DECRYPT(%s, %s, %s)"
    assert aes_decrypt_func.args == ["encrypted_value", "key", "iv"]


def test_aes_decrypt_with_iv_and_mode():
    aes_decrypt_func = AesDecrypt("encrypted_value", "key", "iv", "aes-256-cbc")
    assert str(aes_decrypt_func) == "AES_DECRYPT(%s, %s, %s, %s)"
    assert aes_decrypt_func.args == ["encrypted_value", "key", "iv", "aes-256-cbc"]


def test_aes_decrypt_mode_without_iv_raises():
    with pytest.raises(ValueError):
        AesDecrypt("encrypted_value", "key", mode="aes-256-cbc")


def test_aes_encrypt():
    aes_encrypt_func = AesEncrypt("value", "key")
    assert str(aes_encrypt_func) == "AES_ENCRYPT(%s, %s)"
    assert aes_encrypt_func.args == ["value", "key"]


def test_aes_encrypt_with_iv():
    aes_encrypt_func = AesEncrypt("value", "key", "iv")
    assert str(aes_encrypt_func) == "AES_ENCRYPT(%s, %s, %s)"
    assert aes_encrypt_func.args == ["value", "key", "iv"]


def test_aes_encrypt_with_iv_and_mode():
    aes_encrypt_func = AesEncrypt("value", "key", "iv", "aes-256-cbc")
    assert str(aes_encrypt_func) == "AES_ENCRYPT(%s, %s, %s, %s)"
    assert aes_encrypt_func.args == ["value", "key", "iv", "aes-256-cbc"]


def test_aes_encrypt_mode_without_iv_raises():
    with pytest.raises(ValueError):
        AesEncrypt("value", "key", mode="aes-256-cbc")


def test_compress():
    compress_func = Compress("value")
    assert str(compress_func) == "COMPRESS(%s)"
    assert compress_func.args == ["value"]


def test_des_decrypt():
    des_decrypt_func = DesDecrypt("encrypted_value", "key")
    assert str(des_decrypt_func) == "DES_DECRYPT(%s, %s)"
    assert des_decrypt_func.args == ["encrypted_value", "key"]


def test_des_decrypt_without_key():
    des_decrypt_func = DesDecrypt("encrypted_value")
    assert str(des_decrypt_func) == "DES_DECRYPT(%s)"
    assert des_decrypt_func.args == ["encrypted_value"]


def test_des_encrypt():
    des_encrypt_func = DesEncrypt("value", "key")
    assert str(des_encrypt_func) == "DES_ENCRYPT(%s, %s)"
    assert des_encrypt_func.args == ["value", "key"]


def test_des_encrypt_without_key():
    des_encrypt_func = DesEncrypt("value")
    assert str(des_encrypt_func) == "DES_ENCRYPT(%s)"
    assert des_encrypt_func.args == ["value"]


def test_encode():
    encode_func = Encode("value", "password")
    assert str(encode_func) == "ENCODE(%s, %s)"
    assert encode_func.args == ["value", "password"]


def test_decode():
    decode_func = Decode("value", "password")
    assert str(decode_func) == "DECODE(%s, %s)"
    assert decode_func.args == ["value", "password"]


def test_encrypt():
    encrypt_func = Encrypt("value", "salt")
    assert str(encrypt_func) == "ENCRYPT(%s, %s)"
    assert encrypt_func.args == ["value", "salt"]

    encrypt_func = Encrypt("value")
    assert str(encrypt_func) == "ENCRYPT(%s)"
    assert encrypt_func.args == ["value"]


def test_kdf():
    kdf_func = Kdf("key", "salt", "info_or_iterations", "kdf_name", "width")
    assert str(kdf_func) == "KDF(%s, %s, %s, %s, %s)"
    assert kdf_func.args == ["key", "salt", "info_or_iterations", "kdf_name", "width"]


def test_kdf_without_optional_args():
    kdf_func = Kdf("key", "salt")
    assert str(kdf_func) == "KDF(%s, %s)"
    assert kdf_func.args == ["key", "salt"]


def test_kdf_with_info_or_iterations_only():
    kdf_func = Kdf("key", "salt", "info_or_iterations")
    assert str(kdf_func) == "KDF(%s, %s, %s)"
    assert kdf_func.args == ["key", "salt", "info_or_iterations"]


def test_kdf_with_info_or_iterations_and_kdf_name():
    kdf_func = Kdf("key", "salt", "info_or_iterations", "hkdf")
    assert str(kdf_func) == "KDF(%s, %s, %s, %s)"
    assert kdf_func.args == ["key", "salt", "info_or_iterations", "hkdf"]


def test_kdf_name_without_info_or_iterations_raises():
    with pytest.raises(ValueError):
        Kdf("key", "salt", kdf_name="hkdf")


def test_kdf_width_without_kdf_name_raises():
    with pytest.raises(ValueError):
        Kdf("key", "salt", "info_or_iterations", width=32)


def test_old_password():
    old_password_func = OldPassword("value")
    assert str(old_password_func) == "OLD_PASSWORD(%s)"
    assert old_password_func.args == ["value"]


def test_password():
    password_func = Password("value")
    assert str(password_func) == "PASSWORD(%s)"
    assert password_func.args == ["value"]


def test_md5():
    md5_func = MD5("value")
    assert str(md5_func) == "MD5(%s)"
    assert md5_func.args == ["value"]


def test_random_bytes():
    random_bytes_func = RandomBytes(10)
    assert str(random_bytes_func) == "RANDOM_BYTES(%s)"
    assert random_bytes_func.args == [10]


def test_sha1():
    sha1_func = Sha1("value")
    assert str(sha1_func) == "SHA1(%s)"
    assert sha1_func.args == ["value"]


def test_sha():
    sha_func = Sha("value")
    assert str(sha_func) == "SHA(%s)"
    assert sha_func.args == ["value"]


def test_sha2():
    sha2_func = Sha2("value", 256)
    assert str(sha2_func) == "SHA2(%s, %s)"
    assert sha2_func.args == ["value", 256]


def test_uncompress():
    uncompress_func = Uncompress("value")
    assert str(uncompress_func) == "UNCOMPRESS(%s)"
    assert uncompress_func.args == ["value"]


def test_uncompressed_length():
    uncompressed_length_func = UncompressedLength("value")
    assert str(uncompressed_length_func) == "UNCOMPRESSED_LENGTH(%s)"
    assert uncompressed_length_func.args == ["value"]


def test_uncompress_length_is_alias_of_uncompressed_length():
    uncompress_length_func = UncompressLength("value")
    assert str(uncompress_length_func) == "UNCOMPRESSED_LENGTH(%s)"
    assert uncompress_length_func.args == ["value"]
    assert isinstance(uncompress_length_func, UncompressedLength)


def test_encryption_functions_compose_in_select():
    select = Select(
        "id",
        AesEncrypt("value", "key", "iv", "aes-256-cbc"),
        MD5("value"),
        table="t",
        where=Eq("hash", Sha2("value", 256)),
    )

    assert str(select) == ("SELECT `id`, AES_ENCRYPT(%s, %s, %s, %s), MD5(%s) FROM `t` WHERE `hash` = SHA2(%s, %s)")
    assert select.args == ["value", "key", "iv", "aes-256-cbc", "value", "value", 256]


def test_aes_decrypt_operand_parenthesised_as_subquery():
    subquery = Select(AesDecrypt("data", "key"), table="secrets")
    select = Select("id", table="t", where=Eq("value", subquery))

    assert str(select) == "SELECT `id` FROM `t` WHERE `value` = (SELECT AES_DECRYPT(%s, %s) FROM `secrets`)"
    assert select.args == ["data", "key"]
