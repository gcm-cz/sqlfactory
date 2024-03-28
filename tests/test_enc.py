import pytest
from sqlbuilder.func.enc import AesDecrypt, AesEncrypt, Compress, DesDecrypt, DesEncrypt, Encode, Decode, Encrypt, Kdf, OldPassword, Password, MD5, RandomBytes, Sha1, Sha2, Uncompress, UncompressLength


def test_aes_decrypt():
    aes_decrypt_func = AesDecrypt('encrypted_value', 'key')
    assert str(aes_decrypt_func) == "AES_DECRYPT(%s, %s)"
    assert aes_decrypt_func.args == ['encrypted_value', 'key']


def test_aes_encrypt():
    aes_encrypt_func = AesEncrypt('value', 'key')
    assert str(aes_encrypt_func) == "AES_ENCRYPT(%s, %s)"
    assert aes_encrypt_func.args == ['value', 'key']


def test_compress():
    compress_func = Compress('value')
    assert str(compress_func) == "COMPRESS(%s)"
    assert compress_func.args == ['value']


def test_des_decrypt():
    des_decrypt_func = DesDecrypt('encrypted_value', 'key')
    assert str(des_decrypt_func) == "DES_DECRYPT(%s, %s)"
    assert des_decrypt_func.args == ['encrypted_value', 'key']


def test_des_encrypt():
    des_encrypt_func = DesEncrypt('value', 'key')
    assert str(des_encrypt_func) == "DES_ENCRYPT(%s, %s)"
    assert des_encrypt_func.args == ['value', 'key']


def test_encode():
    encode_func = Encode('value', 'encoding')
    assert str(encode_func) == "ENCODE(%s, %s)"
    assert encode_func.args == ['value', 'encoding']


def test_decode():
    decode_func = Decode('value', 'encoding')
    assert str(decode_func) == "DECODE(%s, %s)"
    assert decode_func.args == ['value', 'encoding']


def test_encrypt():
    encrypt_func = Encrypt('value', 'salt')
    assert str(encrypt_func) == "ENCRYPT(%s, %s)"
    assert encrypt_func.args == ['value', 'salt']

    encrypt_func = Encrypt('value')
    assert str(encrypt_func) == "ENCRYPT(%s)"
    assert encrypt_func.args == ["value"]


def test_kdf():
    kdf_func = Kdf('key', 'salt', 'info_or_iterations', 'kdf_name', 'width')
    assert str(kdf_func) == "KDF(%s, %s, %s, %s, %s)"
    assert kdf_func.args == ['key', 'salt', 'info_or_iterations', 'kdf_name', 'width']


def test_old_password():
    old_password_func = OldPassword('value')
    assert str(old_password_func) == "OLD_PASSWORD(%s)"
    assert old_password_func.args == ['value']


def test_password():
    password_func = Password('value')
    assert str(password_func) == "PASSWORD(%s)"
    assert password_func.args == ['value']


def test_md5():
    md5_func = MD5('value')
    assert str(md5_func) == "MD5(%s)"
    assert md5_func.args == ['value']


def test_random_bytes():
    random_bytes_func = RandomBytes(10)
    assert str(random_bytes_func) == "RANDOM_BYTES(%s)"
    assert random_bytes_func.args == [10]


def test_sha1():
    sha1_func = Sha1('value')
    assert str(sha1_func) == "SHA1(%s)"
    assert sha1_func.args == ['value']


def test_sha2():
    sha2_func = Sha2('value', 256)
    assert str(sha2_func) == "SHA2(%s, %s)"
    assert sha2_func.args == ['value', 256]


def test_uncompress():
    uncompress_func = Uncompress('value')
    assert str(uncompress_func) == "UNCOMPRESS(%s)"
    assert uncompress_func.args == ['value']


def test_uncompress_length():
    uncompress_length_func = UncompressLength('value')
    assert str(uncompress_length_func) == "UNCOMPRESS_LENGTH(%s)"
    assert uncompress_length_func.args == ['value']
