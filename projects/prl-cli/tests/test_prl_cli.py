#!/usr/bin/env python3
"""End-to-end tests for prl-cli against a mock pearld (HTTP + Unix socket).

Run:  python -m pytest tests/test_prl_cli.py   (or)  python tests/test_prl_cli.py
Stdlib-only.
"""
import http.server
import json
import os
import socket
import subprocess
import sys
import threading
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PRL = os.path.join(ROOT, "projects", "prl-cli", "prl")
PY = sys.executable

DONATION_ADDR = "prl1p62v09vuzyd8kdz9l23jaf3kph4wwx6jqcmhkkhg8lhr2qlxky8psu3zw9d"

FAKE_BLOCK = {
    "height": 115681, "hash": "a" * 64, "previousblockhash": "b" * 64,
    "version": 2, "versionbit": 2, "merkleroot": "c" * 64,
    "time": 1768848000, "mediantime": 1768847900, "nonce": 42,
    "bits": "207fffff", "difficulty": 4398046511104.0,
    "chainwork": "0000" + "1" * 40, "transactions": 1, "size": 58740,
    "weight": 234960, "strippedsize": 200, "tx": [
        {"txid": "d" * 64, "hash": "d" * 64, "size": 100, "vin": [
            {"prevout": {"txid": "e" * 64, "vout": 0}, "scriptSig": {
                "asm": "", "hex": ""}, "sequence": 4294967295}],
         "vout": [{"value": 1.23456789, "n": 0,
                   "scriptpubkey": {"asm": "OP_1 " + "f" * 64,
                                    "hex": "5120" + "f" * 64,
                                    "address": DONATION_ADDR,
                                    "type": "witness_v1_taproot"}}]},
    ],
}

FAKE_TX = {
    "txid": "d" * 64, "hash": "d" * 64, "version": 2,
    "locktime": 0, "size": 100, "vin": [
        {"prevout": {"txid": "e" * 64, "vout": 0}, "scriptSig": {
            "asm": "", "hex": ""}, "sequence": 4294967295}],
    "vout": [{"value": 1.23456789, "n": 0,
              "scriptpubkey": {"asm": "OP_1 " + "f" * 64,
                               "hex": "5120" + "f" * 64,
                               "address": DONATION_ADDR,
                               "type": "witness_v1_taproot"}}],
    "blockhash": "a" * 64, "confirmations": 10, "time": 1768848000,
    "blocktime": 1768848000,
}

RESPONSES = {
    "getblockchaininfo": {"chain": "main", "blocks": 115681,
                          "bestblockhash": "a" * 64, "difficulty": 4398046511104.0,
                          "mediantime": 1768847900, "verificationprogress": 0.999,
                          "pruned": False},
    "getdifficulty": 4398046511104.0,
    "getmempoolinfo": {"size": 12, "bytes": 14520, "usage": 18432,
                       "maxmempool": 33554432},
    "getrawmempool": ["1" * 64, "2" * 64, "3" * 64],
    "getnetworkinfo": {"version": "1.4.6", "subversion": "/pearl:1.4.6/",
                       "protocolversion": 70015, "connections": 8},
}


def make_handler():
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(n) or b"{}")
            auth = self.headers.get("Authorization", "")
            if "Basic " not in auth:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'{"error":"401 Unauthorized"}')
                return
            method = body.get("method")
            params = body.get("params", [])
            if method in RESPONSES:
                result = RESPONSES[method]
            elif method == "getblock":
                ref = params[0]
                if ref in (115681, "a" * 64):
                    result = FAKE_BLOCK
                else:
                    self._reply(1, "Block not found")
                    return
            elif method == "getrawtransaction":
                result = FAKE_TX
            elif method == "getblockhash":
                result = "a" * 64
            else:
                self._reply(-32601, f"Method not found: {method}")
                return
            self._reply(0, None, result=result)

        def _reply(self, code, message, result=None):
            payload = {"jsonrpc": "2.0", "id": 1}
            if code:
                payload["error"] = {"code": code, "message": message or ""}
            else:
                payload["result"] = result
            data = json.dumps(payload).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *a):
            pass

    return Handler


def make_sock_server(path):
    """Minimal single-threaded Unix-socket JSON-RPC server (raw accept loop).

    socketserver has no UnixStreamServer on Windows; a plain accept loop is
    enough because the test client runs one request at a time.
    """
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass
    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    srv.bind(path)
    srv.listen(8)
    srv.settimeout(30.0)

    def serve():
        while True:
            try:
                conn, _ = srv.accept()
            except socket.timeout:
                continue
            except OSError:
                return
            try:
                # Read the header block first...
                data = b""
                while b"\r\n\r\n" not in data:
                    chunk = conn.recv(65536)
                    if not chunk:
                        break
                    data += chunk
                head, _, body = data.partition(b"\r\n\r\n")
                n = 0
                for l in head.split(b"\r\n"):
                    if l.lower().startswith(b"content-length"):
                        n = int(l.split(b":")[1])
                # ...then read exactly Content-Length more bytes. Do NOT wait
                # for EOF: real HTTP/1.0 clients (including this CLI) keep the
                # socket open while waiting for the response.
                while len(body) < n:
                    chunk = conn.recv(65536)
                    if not chunk:
                        break
                    body += chunk
                msg = json.loads(body[:n] or b"{}")
                method = msg.get("method")
                if method in RESPONSES:
                    out = json.dumps({"jsonrpc": "2.0", "id": 1,
                                      "result": RESPONSES[method]}).encode()
                elif method == "getblock":
                    out = json.dumps({"jsonrpc": "2.0", "id": 1,
                                      "result": FAKE_BLOCK}).encode()
                else:
                    out = json.dumps({"jsonrpc": "2.0", "id": 1,
                                      "error": {"code": -32601,
                                                "message": "Method not found"}}).encode()
                conn.sendall((b"HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n"
                              b"Content-Length: " + str(len(out)).encode() +
                              b"\r\n\r\n" + out))
            except Exception:
                pass
            finally:
                conn.close()

    t = threading.Thread(target=serve, daemon=True)
    t.start()
    return srv, t


def run_prl(*args, env=None):
    e = dict(os.environ)
    e.pop("PRL_RPC_URL", None)
    e.pop("PRL_RPC_SOCKET", None)
    if env:
        e.update(env)
    return subprocess.run([PY, PRL, *map(str, args)], capture_output=True, text=True,
                          timeout=30, env=e, cwd=ROOT)


class TestPrlCli(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # HTTP server on a random port, Basic auth required by the handler
        port = _free_port()
        cls.httpd = make_server(port)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{port}"
        # Unix socket server (not available on Windows Python)
        if hasattr(socket, "AF_UNIX"):
            cls.sock = os.path.join(os.environ.get("TMPDIR", "/tmp"), "prl-test.sock")
            cls.sock_srv, cls.sock_thread = make_sock_server(cls.sock)
        else:
            cls.sock = None
            cls.sock_srv = None

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        if cls.sock_srv is not None:
            try:
                cls.sock_srv.close()
            except OSError:
                pass

    def test_version_and_help(self):
        r = run_prl("-V")
        self.assertEqual(r.returncode, 0)
        self.assertIn("prl-cli", r.stdout)
        r = run_prl()
        self.assertEqual(r.returncode, 2)  # no subcommand -> usage

    def test_status(self):
        r = run_prl("--rpc-url", self.url, "--user", "prl", "--pass", "prl", "status")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("blocks         115681", r.stdout)
        self.assertIn("best block     " + "a" * 64, r.stdout)
        self.assertIn("mempool        12 tx", r.stdout)

    def test_status_json(self):
        r = run_prl("--rpc-url", self.url, "--user", "prl", "--pass", "prl",
                    "--json", "status")
        self.assertEqual(r.returncode, 0, r.stderr)
        data = json.loads(r.stdout)
        self.assertEqual(data["blockchain"]["blocks"], 115681)
        self.assertEqual(data["mempool"]["size"], 12)

    def test_block_by_height(self):
        r = run_prl("--rpc-url", self.url, "--user", "prl", "--pass", "prl",
                    "block", "115681")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("height     115681", r.stdout)
        self.assertIn("txs        1", r.stdout)

    def test_block_by_hash(self):
        r = run_prl("--rpc-url", self.url, "--user", "prl", "--pass", "prl",
                    "block", "a" * 64)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("height     115681", r.stdout)

    def test_block_missing(self):
        r = run_prl("--rpc-url", self.url, "--user", "prl", "--pass", "prl",
                    "block", 42)
        self.assertEqual(r.returncode, 1)
        self.assertIn("Block not found", r.stderr)

    def test_tx(self):
        r = run_prl("--rpc-url", self.url, "--user", "prl", "--pass", "prl",
                    "tx", "d" * 64)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("1.23456789", r.stdout)
        self.assertIn(DONATION_ADDR, r.stdout)
        self.assertIn("5120", r.stdout)

    def test_mempool(self):
        r = run_prl("--rpc-url", self.url, "--user", "prl", "--pass", "prl",
                    "mempool")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("mempool: 3 tx", r.stdout)
        self.assertIn("1" * 64, r.stdout)

    def test_raw_passthrough(self):
        r = run_prl("--rpc-url", self.url, "--user", "prl", "--pass", "prl",
                    "raw", "getblockhash", "115681")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("a" * 64, r.stdout)

    def test_unknown_method(self):
        r = run_prl("--rpc-url", self.url, "--user", "prl", "--pass", "prl",
                    "raw", "frobnicate")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Method not found", r.stderr)

    def test_auth_required(self):
        r = run_prl("--rpc-url", self.url, "status")
        self.assertEqual(r.returncode, 1)
        self.assertIn("401", r.stderr)

    @unittest.skipUnless(hasattr(socket, "AF_UNIX"), "AF_UNIX unavailable on this platform")
    def test_unix_socket(self):
        r = run_prl("--socket", self.sock, "status")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("blocks         115681", r.stdout)
        r = run_prl("--socket", self.sock, "block", "115681")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_env_vars(self):
        r = run_prl("status", env={"PRL_RPC_URL": self.url,
                                   "PRL_RPC_USER": "prl",
                                   "PRL_RPC_PASS": "prl"})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("blocks         115681", r.stdout)

    def test_check_valid(self):
        r = run_prl("check", DONATION_ADDR)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("OK", r.stdout)
        self.assertIn("mainnet", r.stdout)

    def test_check_invalid(self):
        r = run_prl("check", "prl1badaddress")
        self.assertEqual(r.returncode, 2)
        self.assertIn("INVALID", r.stdout)

    def test_check_mixed_case(self):
        r = run_prl("check", DONATION_ADDR[:-1].lower() + DONATION_ADDR[-1].upper())
        self.assertEqual(r.returncode, 2)


def make_server(port):
    """ThreadingHTTPServer requiring Basic auth prl/prl."""
    handler = make_handler()
    return http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)


def _free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


if __name__ == "__main__":
    unittest.main(verbosity=2)
