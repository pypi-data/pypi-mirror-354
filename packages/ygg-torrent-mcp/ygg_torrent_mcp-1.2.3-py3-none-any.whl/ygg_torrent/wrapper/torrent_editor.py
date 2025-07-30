from base64 import b32encode
from hashlib import sha1
from os import getenv
from urllib import parse

from bencodepy import decode, encode
from dotenv import load_dotenv

load_dotenv()

DUMMY_PASSKEY = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
YGG_PASSKEY = getenv("YGG_PASSKEY")
if not YGG_PASSKEY:
    print("YGG_PASSKEY not found in .env file.\nFallbacking to dummy passkey.")
    YGG_PASSKEY = DUMMY_PASSKEY


def make_magnet_from_torrent_bytes(file_bytes: bytes) -> str:
    metadata = decode(file_bytes)
    subj = metadata[b"info"]
    hashcontents = encode(subj)
    digest = sha1(hashcontents).digest()
    b32hash = b32encode(digest).decode()

    if b"files" in subj:
        total_length = sum(f[b"length"] for f in subj[b"files"])
    else:
        total_length = subj[b"length"]

    tracker = "http://tracker.p2p-world.net:8080/" + YGG_PASSKEY + "/announce"
    tracker2 = "http://connect.maxp2p.org:8080/" + YGG_PASSKEY + "/announce"
    return (
        "magnet:?xt=urn:btih:"
        + b32hash
        + "&dn="
        + parse.quote(subj[b"name"].decode())
        + "&tr="
        + tracker
        + "&tr="
        + tracker2
        + "&xl="
        + str(total_length)
    )


def edit_torrent_bytes(file_bytes: bytes) -> bytes:
    metadata = decode(file_bytes)
    metadata[b"announce"] = (
        b"http://tracker.p2p-world.net:8080/" + YGG_PASSKEY.encode() + b"/announce"
    )
    return encode(metadata)
