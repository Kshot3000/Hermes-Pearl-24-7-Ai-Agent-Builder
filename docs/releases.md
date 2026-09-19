# Pearl upstream release tracker
<!-- Maintained by the 24/7 agent. Newest first. Every entry verified against
     https://github.com/pearl-research-labs/pearl/releases -->

## v1.4.6 (current, observed 2026-09-19)
- **feat(consensus):** raise minimum peer protocol version; add checkpoints (incl. block 100,000) — #283, #288
- **feat(coredns-dnsseed):** production CoreDNS seeder — #278
- **fix(zkpow):** pin Merkle tree leaf counts to declared dimensions — #281
- **fix(zkpow):** reject usize→u32/u16 narrowing of proof dimensions (CWE-681) — #299
- **fix(netsync):** forward ProcessBlock error in the reply — #291
- **fix(rpc):** bound searchrawtransactions count; recover WS panics — #294
- **fix(rpcserver):** remove state-mutating methods from limited-user allowlist — #304
- **fix(txscript):** bound HashCache and SigCache with random eviction — #298
- **fix(peer):** preserve addresses in PushAddrV2Msg shuffle — #295
- **chore:** bump pearl-desktop-wallet to 2.0.5 — #284; Go 1.26.6; CoinMarketCap verification code refresh — #289
- **docs(security):** identity verification now required in bug bounty terms — #290

## v1.4.1 — Salted Noise-seed hardfork
- Consensus hardfork: salted noise-seed (full changelog: v1.3.1…v1.4.1)

## v1.3.1
- **fix(chaincfg):** reschedule testnet2 dense-only fork above MoE blocks — #276

## v1.3.0 — Rank penalty softfork
- **feat(consensus):** rank-penalty softfork — #275
- **fix(blockchain):** validate witness commitment regardless of BFFastAdd — #266
- **fix(wallet):** roll back orphaned blocks left by unapplied reorgs — #274
- **fix(deps):** resolve critical Dependabot alerts (vitest, protobufjs) — #267
- **docs(security):** discretionary bug-bounty reward tiers — #271, #273

## v1.2.1 — Dense-only softfork
- **fix(consensus):** treat only larger-than-dense proofs as MoE; postpone dense-only fork — #261

## v1.2.0 / wallet v2.0.3
- **feat(wallet):** DNS seeders for peer discovery, optional custom peer — #250
- **fix(desktop-wallet):** single-instance lock to prevent RPC 401 after duplicate launch — #239

## v1.1.5
- **feat(zkpow):** export VerifyZKProofFFI for external callers — #186
- **feat(miner):** MoE mining consistency fixes; f8 down-proj quantization — #182, #188
- **feat(miner):** Hadamard-quantized model support — #202, #207
- **refactor(rpc):** overhaul node/wallet RPC servers, clients, TLS — #220
- **feat(node,wallet):** configurable log rotation size (`--logsize`) — #205
- **fix(wallet):** raise RPC client timeout; stale-daemon cleanup; default-peer selection — #210
- **fix:** mempool RBF conflict traversal bounded — #216; wire script-count validation — #218
- **feat(rpc):** ProofCommitment in getblock verbose — #89
- **chore(chaincfg):** activate testnet MoE fork at block 1; refresh genesis — #227

## Binaries (all releases)
`pearld` (full node) · `oyster` (wallet) · `prlctl` (control utility)
Desktop wallet: Windows .exe / macOS .dmg (Intel+ARM) / Linux .deb.

---
PEARL donation address: prl1p62v09vuzyd8kdz9l23jaf3kph4wwx6jqcmhkkhg8lhr2qlxky8psu3zw9d
X: https://x.com/kshot9000 · GitHub: https://github.com/Kshot3000
