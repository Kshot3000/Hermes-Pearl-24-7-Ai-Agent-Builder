"""Self-test for tools/verify_pearl_address.py.

Run: python tests/test_verify_pearl_address.py
No third-party deps (unittest + stdlib).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from verify_pearl_address import verify, decode  # noqa: E402

DONATION = "prl1p62v09vuzyd8kdz9l23jaf3kph4wwx6jqcmhkkhg8lhr2qlxky8psu3zw9d"

# Real mainnet addresses observed on the Pearl explorer (2026-09-19).
KNOWN_GOOD = [
    DONATION,
    "prl1p2sthhrtn3p08cunnusp7wpem9h0323lnua2pxht4nzdr8jylrqhsrnlt0p",
]

# Known-bad: corrupted checksums / wrong hrp / bad structure.
KNOWN_BAD = [
    "prl1p62v09vuzyd8kdz9l23jaf3kph4wwx6jqcmhkkhg8lhr2qlxky8psu3zw9e",  # last char flipped
    "prl1q62v09vuzyd8kdz9l23jaf3kph4wwx6jqcmhkkhg8lhr2qlxky8psu3zw9d",  # witness v0, not Taproot
    "tprl1p62v09vuzyd8kdz9l23jaf3kph4wwx6jqcmhkkhg8lhr2qlxky8psu3zw9d",  # testnet hrp
    "prl1",
    "not an address",
    "prl1p62v09VUZYD8K",  # mixed case
]

# BIP-173/350 decode vectors (hrp-agnostic decode()).
BIP_VECTORS_OK = {
    "BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4": ("bc", 0),
    "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx": ("tb", 0),
    "bc1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3qccfmv3": ("bc", 0),
    "bc1pw508d6qejxtdg4y5r3zarvary0c5xw7kw508d6qejxtdg4y5r3zarvary0c5xw7kt5nd6y": ("bc", 1),
}
BIP_VECTORS_BAD = [
    "BC130S3X4Q22",
    "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t5",
    "tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdce6vzfvpysxf3q0d0000",
    "bc1gmk9yu",
]


class TestPearlAddressValidator(unittest.TestCase):
    def test_known_good_addresses(self):
        for addr in KNOWN_GOOD:
            ok, msg = verify(addr)
            self.assertTrue(ok, f"{addr}: {msg}")
            hrp, version, prog = decode(addr)
            self.assertEqual(hrp, "prl")
            self.assertEqual(version, 1)
            self.assertEqual(len(prog), 32)

    def test_known_bad_addresses(self):
        for addr in KNOWN_BAD:
            ok, _msg = verify(addr)
            self.assertFalse(ok, f"expected invalid: {addr}")

    def test_bip_vectors_decode(self):
        for addr, (hrp, version) in BIP_VECTORS_OK.items():
            d = decode(addr)
            self.assertIsNotNone(d, addr)
            self.assertEqual(d[0], hrp)
            self.assertEqual(d[1], version)

    def test_bip_vectors_bad(self):
        for addr in BIP_VECTORS_BAD:
            self.assertIsNone(decode(addr), addr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
