# PRL Dashboard — Pearl mainnet, live

A single-file, zero-dependency live dashboard for the Pearl (zkPoW) mainnet.
Served at **https://kshot3000.github.io/Hermes-Pearl-24-7-Ai-Agent-Builder/**
(GitHub Pages, deployed from the `prl-dashboard` branch).

## What it shows

- **Block height** + tip hash (indexer status)
- **Block time** — mean interval over the last 30 canonical blocks
- **Difficulty** + bits of the newest block
- **Latest blocks** feed (height, txs, size, mining pool, link to prlscan)
- **Pool leaderboard** — 24h hashrate, network share, blocks, fee, worker counts
- **PRL/USD market** — price, 24h change, exchange + OTC volume (CoinMarketCap via prlscan)
- **Indexer health** — mempool size, indexer lag, healthy flag

Auto-refreshes every 60 seconds. No build step, no framework, no API keys.

## Data source

All data comes from the public prlscan API (`https://api.prlscan.com/v1/...`) —
endpoints used: `/status`, `/blocks?limit=30`, `/pools`, `/market/prl`.
CORS reflects the requesting origin, so the static page fetches directly.
Grain→PRL conversion uses `GrainPerPearl = 1e8` from the Pearl node
(`node/btcutil/const.go`).

## Files

| File | Purpose |
|---|---|
| `index.html` | The entire dashboard (HTML + CSS + JS, one file) |

## Attribution

Built by the 24/7 Pearl agent for Kshot3000 —
GitHub: https://github.com/Kshot3000 · X: https://x.com/kshot9000

Pearl community:
- X: https://x.com/prlnet
- Hugging Face: https://huggingface.co/pearl-ai
- YouTube: https://www.youtube.com/@PearlResearchLabs
- Forums: https://pearlforums.com/
- Explorer: https://prlscan.com/

If this work helped, a donation to the Pearl project is appreciated:
`prl1p62v09vuzyd8kdz9l23jaf3kph4wwx6jqcmhkkhg8lhr2qlxky8psu3zw9d`
