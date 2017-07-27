import hmac
import base64

from hashlib import sha1

def make_digest(message, key):
    digester = hmac.new(key, message, sha1)
    signature = base64.b64encode(digester.digest())

    return str(signature, 'UTF-8')