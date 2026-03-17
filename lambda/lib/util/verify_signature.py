import base64

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


def verify_signature(event, public_key) -> bool:
    headers = event.get("headers") or {}
    signature = headers.get('x-signature-ed25519')
    timestamp = headers.get('x-signature-timestamp')

    body = event.get("body", "")

    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8")

    if not signature or not timestamp:
        return False, body

    verify_key = VerifyKey(bytes.fromhex(public_key))
    try:
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
        return True, body
    except BadSignatureError:
        return False, body
