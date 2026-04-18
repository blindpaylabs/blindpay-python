# Changelog

## [2.1.0](https://github.com/blindpaylabs/blindpay-python/compare/v2.0.1...v2.1.0) (2026-04-18)


### Features

* clear sync baseline when api-sync PR is merged ([729eb96](https://github.com/blindpaylabs/blindpay-python/commit/729eb96a7a683a28baa2dc1fd4c370e9e688d597))


### Bug Fixes

* restore TOS endpoints ([#43](https://github.com/blindpaylabs/blindpay-python/issues/43)) ([64d838e](https://github.com/blindpaylabs/blindpay-python/commit/64d838e60ef22643da31821f38469c3421528361))

## [2.0.1](https://github.com/blindpaylabs/blindpay-python/compare/v2.0.0...v2.0.1) (2026-04-17)


### Bug Fixes

* add upload resource, remove TOS, fix member role field ([#38](https://github.com/blindpaylabs/blindpay-python/issues/38)) ([a833f53](https://github.com/blindpaylabs/blindpay-python/commit/a833f533e1627890498943ace88f2dea1969604f))

## [2.0.0](https://github.com/blindpaylabs/blindpay-python/compare/v1.5.1...v2.0.0) (2026-04-17)


### ⚠ BREAKING CHANGES

* Transfer field names changed to match live API.
    - source_wallet_id → wallet_id
    - destination_wallet_id → removed
    - amount → request_amount
    - quote_id → transfer_quote_id
    - Transfer response completely restructured

### Features

* rewrite transfers to match current API spec ([#36](https://github.com/blindpaylabs/blindpay-python/issues/36)) ([14083a8](https://github.com/blindpaylabs/blindpay-python/commit/14083a890fee663cdee10066c4d1d1b33e8148e9))

## [1.5.1](https://github.com/blindpaylabs/blindpay-python/compare/v1.5.0...v1.5.1) (2026-04-16)


### Bug Fixes

* complete API sync — all endpoints, fields, and methods ([#34](https://github.com/blindpaylabs/blindpay-python/issues/34)) ([7a0bf9e](https://github.com/blindpaylabs/blindpay-python/commit/7a0bf9e48507bfb3bd8fa0b32e2f3f5d05cda896))

## [1.5.0](https://github.com/blindpaylabs/blindpay-python/compare/v1.4.0...v1.5.0) (2026-04-16)


### Features

* use detailed changelog instead of path list for SDK sync ([3228d34](https://github.com/blindpaylabs/blindpay-python/commit/3228d34fec7bc0c558fce8c56c04ae1ea95c1228))


### Bug Fixes

* correct receiver enum types to match API spec ([#32](https://github.com/blindpaylabs/blindpay-python/issues/32)) ([ff63746](https://github.com/blindpaylabs/blindpay-python/commit/ff63746d8177197ec4e0069d3a56ad3795b90540))
* remove openapi.json fetch from api-sync-data ([67a30a3](https://github.com/blindpaylabs/blindpay-python/commit/67a30a3d8399d9bd7265fb3e9f813cc1e2c0760c))
* remove openapi.json reference from prompt, use self-contained changelog only ([89d9389](https://github.com/blindpaylabs/blindpay-python/commit/89d9389f770318736c66e1175e75ac046e3ae9cb))

## [1.4.0](https://github.com/blindpaylabs/blindpay-python/compare/v1.3.0...v1.4.0) (2026-04-16)


### Features

* stricter prompt for lint/type checks + auto-fix CI failures on api-sync PRs ([599b5f8](https://github.com/blindpaylabs/blindpay-python/commit/599b5f84ac10102120432b505a669b2175abf934))
* sync SDK with API changes ([#22](https://github.com/blindpaylabs/blindpay-python/issues/22)) ([5e47aa8](https://github.com/blindpaylabs/blindpay-python/commit/5e47aa893be53e1fc2347073a265efd1e4c23858))
* upgrade to Opus model, additive-only prompt, spec extraction, validation gates ([ab52298](https://github.com/blindpaylabs/blindpay-python/commit/ab52298a1d1482eae48ce07666d95a13a7e0656b))


### Bug Fixes

* add id-token: write permission for claude-code-action ([80ba72f](https://github.com/blindpaylabs/blindpay-python/commit/80ba72f6cc9901e224ebcaa6883ead0fa2e0c765))
* allow bash/file tools and skip PR when no changes ([d8580c6](https://github.com/blindpaylabs/blindpay-python/commit/d8580c674ec1be8f3e88bc05e1edb744757273c3))
* exclude workflow files from api-sync commits ([5c2efeb](https://github.com/blindpaylabs/blindpay-python/commit/5c2efebac06dc389dd64a741c704ccf6b0a4dd48))
* fetch openapi.json from raw URL instead of artifact download ([048ebe3](https://github.com/blindpaylabs/blindpay-python/commit/048ebe3565bd1fafb6b266745a9bcd433337e021))
* improve prompt to implement all endpoints for affected resources ([cc6f947](https://github.com/blindpaylabs/blindpay-python/commit/cc6f9470a31c71101fd7085fbb06b6df3f431acc))
* read openapi spec from api-sync-data branch (no cross-repo auth) ([7dc51af](https://github.com/blindpaylabs/blindpay-python/commit/7dc51af4268275a529228697b604147c4e8b82f1))
* remove invalid model input from claude-code-action ([625cc91](https://github.com/blindpaylabs/blindpay-python/commit/625cc91255aa2637f42cb7536d69ecd8a0ae0008))
* remove needs-review label that may not exist ([255b4c9](https://github.com/blindpaylabs/blindpay-python/commit/255b4c928c4b5e112a7b5e369d3aa7a37a901df0))
* restore git remote auth before push ([8f2805a](https://github.com/blindpaylabs/blindpay-python/commit/8f2805a12dcf00e2b5fe343b0fdc6b07680940fe))
* use claude_code_oauth_token instead of anthropic_api_key ([23d0512](https://github.com/blindpaylabs/blindpay-python/commit/23d0512050f61e48e5f1a7e96e7bce2ec6004a67))
* use gh api with PAT to fetch openapi.json from private repo ([927d263](https://github.com/blindpaylabs/blindpay-python/commit/927d2633df52a2a086d8b4990e11e59d25c13a2d))
* use PAT for push and PR to trigger CI workflows ([40a773b](https://github.com/blindpaylabs/blindpay-python/commit/40a773baee41c3ad58d066e25950d8ddbd64d842))

## [1.2.0](https://github.com/blindpaylabs/blindpay-python/compare/v1.1.0...v1.2.0) (2025-11-12)


### Features

* add new tos and solana endpoints ([#10](https://github.com/blindpaylabs/blindpay-python/issues/10)) ([1a37f28](https://github.com/blindpaylabs/blindpay-python/commit/1a37f285464a0b23ebbe532c6f7b14d58b8a04ec))

## [1.1.0](https://github.com/blindpaylabs/blindpay-python/compare/v1.0.0...v1.1.0) (2025-11-11)


### Features

* add swift code check endpoint ([a260b26](https://github.com/blindpaylabs/blindpay-python/commit/a260b268230b43cbc3b29cd8065355af0f80d25e))

## [1.0.0](https://github.com/blindpaylabs/blindpay-python/compare/v0.1.0...v1.0.0) (2025-10-17)


### ⚠ BREAKING CHANGES

* Bumping to 1.0.0 for initial stable release

### Features

* add receivers limit increase endpoints ([#4](https://github.com/blindpaylabs/blindpay-python/issues/4)) ([482906a](https://github.com/blindpaylabs/blindpay-python/commit/482906aa464087219aee8eeb54eedf97af44585c))
* stable release ([69d8831](https://github.com/blindpaylabs/blindpay-python/commit/69d88310b1e91ce9c604a825a5824ef3587c8d76))

## 0.1.0 (2025-10-09)


### Documentation

* add readme ([0f2b0e8](https://github.com/blindpaylabs/blindpay-python/commit/0f2b0e84cb5074ecc4b2f16c79baa2ad0f547753))
