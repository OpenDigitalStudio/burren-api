# Copyright (c) 2020 Erno Kuvaja OpenDigitalStudio.net
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
