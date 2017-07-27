import hmac
import base64

from hashlib import sha1

def make_digest(message, key):
    key = bytes(key, 'UTF-8')
    message = bytes(message, 'UTF-8')

    digester = hmac.new(key, message, sha1)
    signature = base64.urlsafe_b64encode(digester.digest())

    return str(signature, 'UTF-8')