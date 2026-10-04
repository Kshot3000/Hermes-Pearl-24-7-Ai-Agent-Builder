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

# Valid-checksum strings that are still NOT valid Pearl addresses.
# Each was generated from the donation address's real program; verify()
# must reject every one (a bare checksum pass is not Pearl validity).
STRICT_BAD = [
    # witness v0 with a valid bech32 checksum — Pearl is Taproot-only and
    # upstream decodeSegWitAddress rejects v0 outright.
    "prl1q62v09vuzyd8kdz9l23jaf3kph4wwx6jqcmhkkhg8lhr2qlxky8pskxz8a3",
    # witness v1, bech32m, but a 20-byte program — Pearl requires 32.
    "prl1p62v09vuzyd8kdz9l23jaf3kph4wwx6jqmu48ck",
    # witness v1, 32-byte program, but checksummed with the bech32 (v0)
    # constant — BIP-350 requires bech32m for v1+.
    "prl1p62v09vuzyd8kdz9l23jaf3kph4wwx6jqcmhkkhg8lhr2qlxky8psfdjzq0",
    # Donation address with a padding bit flipped: same program, different
    # string. Non-zero padding is malleability — BIP-173 forbids it.
    "prl1p62v09vuzyd8kdz9l23jaf3kph4wwx6jqcmhkkhg8lhr2qlxky8p3p8kmcl",
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

    def test_strict_bad_addresses(self):
        for addr in STRICT_BAD:
            ok, _msg = verify(addr)
            self.assertFalse(ok, f"expected invalid: {addr}")

    def test_decode_rejects_nonzero_padding(self):
        # The padding-flipped string must not decode at all (malleability),
        # while the untouched donation address still decodes to 32 bytes.
        self.assertIsNone(decode(STRICT_BAD[3]))
        self.assertEqual(len(decode(DONATION)[2]), 32)

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
