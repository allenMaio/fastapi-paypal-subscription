import json
from base64 import b64decode
from binascii import crc32

import requests
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from fastapi import Request, Response

from app.core.config import settings


async def webhook_handler(request: Request):
    headers = request.headers
    event = await request.body()
    
    if verify_signature(headers, event):
        return Response(content=json.dumps({"message": "Webhook received successfully"}))

def verify_signature(headers, event):
    cert_url = headers.get("paypal-cert-url")
    transmission_id = headers.get("paypal-transmission-id")
    signature = headers.get("paypal-transmission-sig")
    timestamp = headers.get("paypal-transmission-time")
    webhook_id = settings.PAYPAL_WEBHOOK_ID
    crc = crc32(event)

    message = f"{transmission_id}|{timestamp}|{webhook_id}|{crc}"

    response = requests.get(cert_url)
    cert_pem = response.text
    rsakey = RSA.importKey(cert_pem)
    verifier = PKCS1_v1_5.new(rsakey)

    digest = SHA256.new()
    digest.update(message.encode())

    signature_decoded = b64decode(signature)

    verified_result = verifier.verify(digest, signature_decoded)
    return verified_result

    # ref https://gist.github.com/lkdocs/6519372