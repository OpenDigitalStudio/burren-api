import binascii
import hashlib
import os


def salted_hash(passwd: str):
    """Salt-n-hash password provided"""
    salt = hashlib.sha224(os.urandom(72)).hexdigest().encode('ascii')
    phash = hashlib.pbkdf2_hmac('sha512',
                                passwd.encode('utf-8'),
                                salt,
                                5000)
    phash = binascii.hexlify(phash)
    return (salt + phash).decode('ascii')


def check_passwd(passwd: str, phash: str):
    """Time to see if our passwords match"""
    salt = phash[:56]
    passh = phash[56:]
    nhash = hashlib.pbkdf2_hmac('sha512',
                                passwd.encode('utf-8'),
                                salt.encode('ascii'),
                                5000)
    nhash = binascii.hexlify(nhash).decode('ascii')
    return passh == nhash
