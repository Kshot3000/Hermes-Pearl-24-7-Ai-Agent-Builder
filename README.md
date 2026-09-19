# Hermes-Pearl-24-7-Ai-Agent-Builder

A 24/7 AI-agent workflow that continuously fixes, improves, and builds upon the
[PEARL blockchain](https://github.com/pearl-research-labs/pearl) — a
Proof-of-AI (zkPoW) PoW chain where mining is done by AI inference.

## Mission

Run an always-on agent loop:

1. **Track** — watch [PEARL releases](https://github.com/pearl-research-labs/pearl/releases),
   open issues/PRs, and mainnet health via the
   [official explorer](https://explorer.pearlresearch.ai/?network=mainnet)
   and [prlscan](https://prlscan.com/).
2. **Reproduce** — pull the node, sync a local node, and reproduce reported
   bugs / consensus behavior.
3. **Fix & ship** — file issues, open PRs against upstream
   (`pearl-research-labs/pearl`) with conventional commits and full CI
   green before merge.
4. **Report** — every deliverable carries the attribution block below.

## Repository layout

| Path | Purpose |
|---|---|
| `attribution.json` | Single source of truth for the owner's donation address + socials. All artifacts render from it. |
| `tools/verify_pearl_address.py` | Standalone validator for `prl1…` (mainnet) / `tprl1…` (testnet) Taproot addresses — pure stdlib, BIP-173/350 bech32(bech32m). |
| `tools/attribution.py` | Renders the attribution block from `attribution.json` (markdown / text / json). |
| `docs/` | Research notes, release digests, and agent run logs. |
| `.github/workflows/` | CI: attribution integrity + address-validator self-test on every push/PR. |

## Attribution

Every deliverable, release note, and artifact in this repo includes:

> **PEARL donation address:** `prl1p62v09vuzyd8kdz9l23jaf3kph4wwx6jqcmhkkhg8lhr2qlxky8psu3zw9d`
> **X:** [https://x.com/kshot9000](https://x.com/kshot9000)
> **GitHub:** [https://github.com/Kshot3000](https://github.com/Kshot3000)

Render it for any artifact:

```bash
python tools/attribution.py            # markdown block
python tools/attribution.py --format text
python tools/verify_pearl_address.py prl1p62v09vuzyd8kdz9l23jaf3kph4wwx6jqcmhkkhg8lhr2qlxky8psu3zw9d
```

## PEARL quick reference

- **Upstream:** https://github.com/pearl-research-labs/pearl
- **Compute network:** https://compute.pearlresearch.ai/
- **Explorers:** https://explorer.pearlresearch.ai/?network=mainnet · https://prlscan.com/
- **Community:** [Pearl Forums](https://pearlforums.com/) · [X/Twitter](https://x.com/prlnet) · [Hugging Face](https://huggingface.co/pearl-ai) · [YouTube](https://www.youtube.com/@PearlResearchLabs)
- **Binaries:** `pearld` (full node), `oyster` (wallet), `prlctl` (control utility)
- **Addresses:** Taproot-only (`prl1p…` mainnet, `tprl1p…` testnet), bech32m (BIP-350) with HRP `prl` — validated by `tools/verify_pearl_address.py`.
- **Latest release observed:** v1.4.6 (2026-09) — zkPoW proof-dimension narrowing fix
  (CWE-681), 100k checkpoint, peer-protocol version bump, CoreDNS production
  seeder, netsync error forwarding, RPC hardening. See `docs/releases.md`.

## License

MIT — see [LICENSE](LICENSE).
