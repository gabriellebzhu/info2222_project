import hashlib
import os
from base64 import b64decode, b64encode

COOKIE_SECRET = b64encode(os.urandom(16)).decode('utf-8')


def hash_the_pass(password, salt):
    salted_pass = password.encode() + salt

    hasher = hashlib.new('sha256')
    hasher.update(salted_pass)
    return hasher.hexdigest()


def salt_to_string(salt):
    return b64encode(salt).decode('utf-8')


def string_to_salt(string):
    return b64decode(string.encode('utf-8'))
