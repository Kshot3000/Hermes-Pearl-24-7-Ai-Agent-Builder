#!/usr/bin/env python3
"""Verify Pearl (prl1p...) addresses.

Pearl addresses are bech32m-encoded Taproot (witness v1, 32-byte program)
addresses with HRP "prl" (mainnet; testnet uses "tprl").

Usage:
    python verify_pearl_address.py <address> [more_addresses...]
    python verify_pearl_address.py --file paths.txt

Exit code 0 = all valid, 1 = at least one invalid.
Pure stdlib — no dependencies.
"""
import sys

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
GEN = [
    0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3,
    0x2DE1C860, 0x2B9E9F5F, 0x15E1FC23, 0x162EFCF6, 0x1CF410EF,
    0x100B6840, 0x1B35664A, 0x18800582, 0x1FD28580, 0x10F83232,
    0x14C800CF, 0x1B63835D, 0x13A2C9AD, 0x15C5D320, 0x10F033D7,
    0x14A70125, 0x11F64723, 0x13F3A537,
]
BECH32M_CONST = 0x2BC830A3  # BIP-350 bech32m (matches pearl node/btcutil/bech32 version.go)
BECH32_CONST = 0x00000001   # original bech32 (v0)

# Witness version -> charset char is the identity: version N is the N-th
# char of CHARSET (BIP-173: version 0='q', 1='p', 2='z', 3='r', ... 16='s').
# BIP-350 (bech32m) extends legal versions to 0-20.
WITNESS_VERSIONS = {c: i for i, c in enumerate(CHARSET[:21])}


def _polymod(values):
    chk = 1
    for v in values:
        top = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ v
        for i in range(5):
            chk ^= GEN[i] if (top >> i) & 1 else 0
    return chk


def _hrp_expand(hrp):
    return [ord(c) >> 5 for c in hrp] + [0] + [
        (ord(c) & 31) for c in hrp
    ]


def _verify_checksum(hrp, data):
    return _polymod(_hrp_expand(hrp) + data) in (BECH32M_CONST, BECH32_CONST)


def decode(address):
    """Decode a bech32m address -> (hrp, witness_version, program_bytes) or None."""
    if not isinstance(address, str):
        return None
    addr = address.lower()
    if not (address == address.lower() or address == address.upper()):
        return None  # mixed case is illegal (BIP-173)
    if "1" not in addr:
        return None
    # Last '1' is the separator (bech32 uses the last occurrence).
    pos = addr.rfind("1")
    if pos < 1 or pos + 7 > len(addr):
        return None
    hrp = addr[:pos]
    if not hrp.isalpha():
        return None
    data = []
    for c in addr[pos + 1:]:
        idx = CHARSET.find(c)
        if idx < 0:
            return None
        data.append(idx)
    if not _verify_checksum(hrp, data):
        return None
    # Strip the 6-char checksum; first symbol is the witness version.
    payload = data[:-6]
    if not payload:
        return None
    version_char = CHARSET[payload[0]]
    if version_char not in WITNESS_VERSIONS:
        return None
    # Expand remaining 5-bit groups into bytes.
    bits = 0
    acc = 0
    out = bytearray()
    for value in payload[1:]:
        acc = (acc << 5) | value
        bits += 5
        if bits >= 8:
            out.append((acc >> (bits - 8)) & 0xFF)
            bits -= 8
    if bits >= 5:  # leftover bits must be zero
        return None
    return hrp, WITNESS_VERSIONS[version_char], bytes(out)


def verify(address, hrp="prl"):
    """Return (bool, reason)."""
    dec = decode(address)
    if dec is None:
        return False, "not a valid bech32m string (bad checksum or encoding)"
    a_hrp, version, program = dec
    if a_hrp != hrp:
        return False, f"HRP '{a_hrp}' != expected '{hrp}' (testnet uses 'tprl')"
    if version != 1:
        return False, f"witness version {version} != 1 (Pearl is Taproot-only)"
    if len(program) != 32:
        return False, f"program length {len(program)} != 32 bytes"
    return True, "valid"


def main(argv):
    addresses = []
    i = 0
    while i < len(argv):
        if argv[i] == "--file":
            i += 1
            with open(argv[i], encoding="utf-8") as f:
                addresses.extend(
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith("#")
                )
        else:
            addresses.append(argv[i])
        i += 1
    if not addresses:
        print(__doc__)
        return 2
    ok = True
    for addr in addresses:
        valid, reason = verify(addr)
        status = "OK  " if valid else "FAIL"
        print(f"{status} {addr}  ({reason})")
        ok = ok and valid
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
