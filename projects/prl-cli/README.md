# PRL CLI

A thin, stdlib-only JSON-RPC client for Pearl nodes (`pearld`). Single file,
no dependencies — part of the 24/7 Pearl agent's **Build-half** roadmap.

## Quick start

```bash
# Against a local node (default: http://127.0.0.1:44107 mainnet;
# --testnet switches the default port to 44109). pearld only serves RPC
# when rpcuser/rpcpass are configured — pass them if your node requires them.
python prl status
python prl block 115000        # by height (resolved via getblockhash)
python prl block latest        # chain tip (via getbestblockhash)
python prl block <blockhash>   # by hash
python prl tx <txid>
python prl mempool --limit 10

# Against any node / socket / creds
python prl --rpc-url http://10.0.0.5:44107 --user U --pass P status
python prl --socket /var/run/pearld.sock block latest
python prl check prl1p62v09vuzyd8kdz9l23jaf3kph4wwx6jqcmhkkhg8lhr2qlxky8psu3zw9d

# Raw passthrough to any RPC method (args are JSON-parsed when possible)
python prl raw getblockchaininfo
python prl raw getblockhash 115000

# Machine-readable output from the built-in commands
python prl --json status
```

Environment overrides: `PRL_RPC_URL`, `PRL_RPC_SOCKET`, `PRL_RPC_USER`,
`PRL_RPC_PASS`.

## Features

- `status` — chain, tip height/hash, difficulty, median time, mempool size
- `block [height|hash|latest]` — decoded block + tx count (heights are
  resolved through `getblockhash`; `pearld`'s `getblock` takes a hash only)
- `tx <txid>` — inputs/outputs with the node's decoded addresses
- `mempool` — pending tx count + txid list (`--limit`, default 20)
- `check <addr>...` — offline strict Pearl address validation (mainnet/testnet):
  Taproot-only witness v1, 32-byte program, bech32m checksum, zero padding —
  a valid-checksum v0, short-program, or foreign-chain address is INVALID
- `raw <method> [args...]` — passthrough to any RPC method, JSON in/out
- `--json` on the built-in commands for machine-readable output

## Tests

```bash
python tests/test_prl_cli.py   # 21 tests, stdlib-only, mock node in-process
```

The mock node models a real `pearld`'s wire rules (e.g. `getblock` rejects a
numeric height; `getrawtransaction` returns the btcjson `Vin`/`Vout` shapes —
inline `txid`/`vout` or `coinbase` on inputs, `scriptPubKey` on outputs), so
argument- and response-shape bugs fail the suite instead of passing it.

## Built for the Pearl community

- Built by the [24/7 AI agent](https://github.com/Kshot3000/Hermes-Pearl-24-7-Ai-Agent-Builder)
  for Kshot3000 ([X](https://x.com/kshot9000) · [GitHub](https://github.com/Kshot3000))
- Upstream: [pearl-research-labs/pearl](https://github.com/pearl-research-labs/pearl)
- Explore: [explorer.pearlresearch.ai](https://explorer.pearlresearch.ai/?network=mainnet)
  · [prlscan.com](https://prlscan.com/)
- Community: [Pearl Forums](https://pearlforums.com/) ·
  [X @prlnet](https://x.com/prlnet) ·
  [Hugging Face](https://huggingface.co/pearl-ai) ·
  [YouTube](https://www.youtube.com/@PearlResearchLabs)
