# PRL CLI

A thin, stdlib-only JSON-RPC client for Pearl nodes (`pearld`). Single file,
no dependencies — part of the 24/7 Pearl agent's **Build-half** roadmap.

## Quick start

```bash
# Against a local node (default: http://127.0.0.1:8401, creds prl/prl)
python prl status
python prl block 115000
python prl tx <txid>
python prl mempool

# Against any node / socket / creds
python prl --rpc-url http://127.0.0.1:8401 --user U --pass P status
python prl --socket /var/run/pearld.sock block latest
python prl check prl1p62v09vuzyd8kdz9l23jaf3kph4wwx6jqcmhkkhg8lhr2qlxky8psu3zw9d

# Raw passthrough to any RPC method
python prl -j getblockchaininfo
python prl estimatefee
```

Environment overrides: `PRL_RPC_URL`, `PRL_RPC_SOCKET`, `PRL_RPC_USER`,
`PRL_RPC_PASS`.

## Features

- `status` — chain tip, difficulty, median time, sync state
- `block [height|hash|latest]` — decoded block + tx count
- `tx <txid>` — inputs/outputs with **decoded Pearl addresses**
- `mempool` — pending tx count + total fees
- `check <addr>...` — offline bech32m Taproot address validation (mainnet/testnet)
- `<method> [args...]` — raw passthrough to any RPC method, JSON in/out
- `--json` on any command for machine-readable output

## Tests

```bash
python tests/test_prl_cli.py   # 16 tests, stdlib-only, mock node in-process
```

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
