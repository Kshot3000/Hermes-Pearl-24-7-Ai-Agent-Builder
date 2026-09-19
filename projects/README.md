# projects/

Brand-new code, apps, and websites built for the Pearl ecosystem — the
"Build" half of the 50/50 workload split. Each project gets its own
directory with its own README (mission, run instructions, attribution).

Rules:

- Every project's README ends with the attribution block
  (`python ../tools/attribution.py --md`).
- Address handling uses `../tools/verify_pearl_address.py` (stdlib-only).
- Projects that touch funds are strictly read-only against the chain by
  default; any sending capability is opt-in and never automated.

## Roadmap candidates

- `prl-dashboard/` — lightweight mainnet health dashboard (block height,
  latest blocks/txs, pool stats) fed by the public explorer APIs.
  **LIVE** at https://kshot3000.github.io/Hermes-Pearl-24-7-Ai-Agent-Builder/
- `prl-cli/` — thin RPC client (`getblockcount`, `getblock`,
  `listunspent` against a local `pearld`, address verification baked in).
  **DONE** — 16-test suite (mock node), stdlib-only, HTTP + Unix socket.
- `zkpow-bench/` — local benchmark harness for zkPoW proof verification
  (times VerifyZKProofFFI paths against known-good proofs).
- `prl-watcher/` — release/changelog diff monitor: alerts when upstream
  `pearl-research-labs/pearl` cuts a release, summarizes breaking
  consensus changes.
