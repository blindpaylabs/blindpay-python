# Changelog

## [4.1.1](https://github.com/blindpaylabs/blindpay-python/compare/v4.1.0...v4.1.1) (2026-11-12)


### Bug Fixes

* README snippets type-check in pyright, typed delete results, and a repeated-cursor guard for pagers ([#85](https://github.com/blindpaylabs/blindpay-python/issues/85)) ([6bca8a9](https://github.com/blindpaylabs/blindpay-python/commit/6bca8a9ffb11240a9a958d66a7f7837d87962e8b))

## [4.1.0](https://github.com/blindpaylabs/blindpay-python/compare/v4.0.1...v4.1.0) (2026-11-12)


### Features

* review_reason, typed error codes, GET request options and release hygiene ([#83](https://github.com/blindpaylabs/blindpay-python/issues/83)) ([0fc51fc](https://github.com/blindpaylabs/blindpay-python/commit/0fc51fccdd355958a43a356a51b7d8ad7242cf6d))

## [4.0.1](https://github.com/blindpaylabs/blindpay-python/compare/v4.0.0...v4.0.1) (2026-11-11)


### Bug Fixes

* restore the package exports the 4.0.0 release commit dropped ([#81](https://github.com/blindpaylabs/blindpay-python/issues/81)) ([3c5bbef](https://github.com/blindpaylabs/blindpay-python/commit/3c5bbeffc2565adfd34b875c555c9e81198211b5))

## [4.0.0](https://github.com/blindpaylabs/blindpay-python/compare/v3.4.1...v4.0.0) (2026-11-11)


### ⚠ BREAKING CHANGES

* complete the customers rename, remove receivers/api_keys ([#55](https://github.com/blindpaylabs/blindpay-python/issues/55))
* Transfer field names changed to match live API.
    - source_wallet_id → wallet_id
    - destination_wallet_id → removed
    - amount → request_amount
    - quote_id → transfer_quote_id
    - Transfer response completely restructured
* Bumping to 1.0.0 for initial stable release

### Features

* add customers resource, deprecate receivers (v2.3.0) ([#48](https://github.com/blindpaylabs/blindpay-python/issues/48)) ([28b8197](https://github.com/blindpaylabs/blindpay-python/commit/28b81975ded85fb572551e2e52eb3e19a13ce9da))
* add new tos and solana endpoints ([#10](https://github.com/blindpaylabs/blindpay-python/issues/10)) ([1a37f28](https://github.com/blindpaylabs/blindpay-python/commit/1a37f285464a0b23ebbe532c6f7b14d58b8a04ec))
* add receivers limit increase endpoints ([#4](https://github.com/blindpaylabs/blindpay-python/issues/4)) ([482906a](https://github.com/blindpaylabs/blindpay-python/commit/482906aa464087219aee8eeb54eedf97af44585c))
* add swift code check endpoint ([a260b26](https://github.com/blindpaylabs/blindpay-python/commit/a260b268230b43cbc3b29cd8065355af0f80d25e))
* **api-sync:** deterministic spec-sync patcher (Phase A) ([#58](https://github.com/blindpaylabs/blindpay-python/issues/58)) ([3f157fe](https://github.com/blindpaylabs/blindpay-python/commit/3f157fe9386386bb57d47a0b072ea825bae2da99))
* clear sync baseline when api-sync PR is merged ([729eb96](https://github.com/blindpaylabs/blindpay-python/commit/729eb96a7a683a28baa2dc1fd4c370e9e688d597))
* complete the customers rename, remove receivers/api_keys ([#55](https://github.com/blindpaylabs/blindpay-python/issues/55)) ([94ea954](https://github.com/blindpaylabs/blindpay-python/commit/94ea954cd720141d872e37c07ac5af5f4cefe085))
* **customers:** add customer.* webhook events and customer_id list filters ([#52](https://github.com/blindpaylabs/blindpay-python/issues/52)) ([562f219](https://github.com/blindpaylabs/blindpay-python/commit/562f2190dc53ecc6fc39a41a3d759b8ecb65cb39))
* rewrite transfers to match current API spec ([#36](https://github.com/blindpaylabs/blindpay-python/issues/36)) ([14083a8](https://github.com/blindpaylabs/blindpay-python/commit/14083a890fee663cdee10066c4d1d1b33e8148e9))
* stable release ([69d8831](https://github.com/blindpaylabs/blindpay-python/commit/69d88310b1e91ce9c604a825a5824ef3587c8d76))
* stricter prompt for lint/type checks + auto-fix CI failures on api-sync PRs ([599b5f8](https://github.com/blindpaylabs/blindpay-python/commit/599b5f84ac10102120432b505a669b2175abf934))
* sync SDK with API changes ([#22](https://github.com/blindpaylabs/blindpay-python/issues/22)) ([5e47aa8](https://github.com/blindpaylabs/blindpay-python/commit/5e47aa893be53e1fc2347073a265efd1e4c23858))
* sync SDK with API changes ([#41](https://github.com/blindpaylabs/blindpay-python/issues/41)) ([24c4e76](https://github.com/blindpaylabs/blindpay-python/commit/24c4e76a28874a90740ad7d06f7b2afd56a17f8f))
* sync SDK with API changes ([#46](https://github.com/blindpaylabs/blindpay-python/issues/46)) ([55310bc](https://github.com/blindpaylabs/blindpay-python/commit/55310bcc282c4c09a42056575b8cade95224407e))
* sync SDK with API changes ([#72](https://github.com/blindpaylabs/blindpay-python/issues/72)) ([e609971](https://github.com/blindpaylabs/blindpay-python/commit/e609971abcc1b8b0aef997b15a69bf15edd56915))
* **types:** fix pagination cursor, billing fee, account type and wallet-create types ([#64](https://github.com/blindpaylabs/blindpay-python/issues/64)) ([767dd62](https://github.com/blindpaylabs/blindpay-python/commit/767dd62c65ada5c2812507af6cbd92a6d39d2869))
* **types:** widen 291 nullable response fields to Optional ([#74](https://github.com/blindpaylabs/blindpay-python/issues/74)) ([2810f7f](https://github.com/blindpaylabs/blindpay-python/commit/2810f7f351af490e3fc994a335cd9d1bbf6e31df))
* update SDK to v1.3.0 ([#16](https://github.com/blindpaylabs/blindpay-python/issues/16)) ([02b9d2d](https://github.com/blindpaylabs/blindpay-python/commit/02b9d2d03b6ab9cefd2151e4e99f07ab5d5fc88d))
* upgrade to Opus model, additive-only prompt, spec extraction, validation gates ([ab52298](https://github.com/blindpaylabs/blindpay-python/commit/ab52298a1d1482eae48ce07666d95a13a7e0656b))
* use detailed changelog instead of path list for SDK sync ([3228d34](https://github.com/blindpaylabs/blindpay-python/commit/3228d34fec7bc0c558fce8c56c04ae1ea95c1228))


### Bug Fixes

* add id-token: write permission for claude-code-action ([80ba72f](https://github.com/blindpaylabs/blindpay-python/commit/80ba72f6cc9901e224ebcaa6883ead0fa2e0c765))
* add upload resource, remove TOS, fix member role field ([#38](https://github.com/blindpaylabs/blindpay-python/issues/38)) ([a833f53](https://github.com/blindpaylabs/blindpay-python/commit/a833f533e1627890498943ace88f2dea1969604f))
* allow bash/file tools and skip PR when no changes ([d8580c6](https://github.com/blindpaylabs/blindpay-python/commit/d8580c674ec1be8f3e88bc05e1edb744757273c3))
* **bank-accounts:** type bank_accounts.get's response as BankAccountOut ([48df625](https://github.com/blindpaylabs/blindpay-python/commit/48df625318eb8e423b3d16ab826f17b071e4f647))
* **ci:** merge the release PR from the push-triggered job ([#60](https://github.com/blindpaylabs/blindpay-python/issues/60)) ([a255d91](https://github.com/blindpaylabs/blindpay-python/commit/a255d91ddda3a1cbdd9d1ad6271dd414a0ed6296))
* complete API sync — all endpoints, fields, and methods ([#34](https://github.com/blindpaylabs/blindpay-python/issues/34)) ([7a0bf9e](https://github.com/blindpaylabs/blindpay-python/commit/7a0bf9e48507bfb3bd8fa0b32e2f3f5d05cda896))
* correct receiver enum types to match API spec ([#32](https://github.com/blindpaylabs/blindpay-python/issues/32)) ([ff63746](https://github.com/blindpaylabs/blindpay-python/commit/ff63746d8177197ec4e0069d3a56ad3795b90540))
* **customers:** EstimatedAnnualRevenue top band has an extra zero ([#66](https://github.com/blindpaylabs/blindpay-python/issues/66)) ([09892d9](https://github.com/blindpaylabs/blindpay-python/commit/09892d93c6f553ccaef9d1aaf7cf6cc6079116ee))
* **deps:** drop the unused pydantic runtime dependency ([93cffef](https://github.com/blindpaylabs/blindpay-python/commit/93cffef143c85bb051f12ac1c8f40bc121cde0e2))
* exclude workflow files from api-sync commits ([5c2efeb](https://github.com/blindpaylabs/blindpay-python/commit/5c2efebac06dc389dd64a741c704ccf6b0a4dd48))
* fetch openapi.json from raw URL instead of artifact download ([048ebe3](https://github.com/blindpaylabs/blindpay-python/commit/048ebe3565bd1fafb6b266745a9bcd433337e021))
* improve prompt to implement all endpoints for affected resources ([cc6f947](https://github.com/blindpaylabs/blindpay-python/commit/cc6f9470a31c71101fd7085fbb06b6df3f431acc))
* **packaging:** report the real SDK version in the User-Agent ([9b7ca97](https://github.com/blindpaylabs/blindpay-python/commit/9b7ca977753a1bdad828bda27ecd25d4413a4de7))
* **packaging:** ship py.typed inside the blindpay package ([2b69201](https://github.com/blindpaylabs/blindpay-python/commit/2b6920162f1549db2272dccdce428ab44d0fd6d0))
* **payouts,payins:** deprecate export(), which calls a route that doesn't exist ([241194e](https://github.com/blindpaylabs/blindpay-python/commit/241194e3183c7e2750593441c468bca1f13e09a3))
* read openapi spec from api-sync-data branch (no cross-repo auth) ([7dc51af](https://github.com/blindpaylabs/blindpay-python/commit/7dc51af4268275a529228697b604147c4e8b82f1))
* **release:** keep _version.py in step with the released version ([0079a6b](https://github.com/blindpaylabs/blindpay-python/commit/0079a6b7e071db2f6e58b58836250ee3034b6a8d))
* **release:** keep _version.py in step with the released version ([8accbbb](https://github.com/blindpaylabs/blindpay-python/commit/8accbbb77dba0e20c12345d3e40ac64d19486dcd))
* remove invalid model input from claude-code-action ([625cc91](https://github.com/blindpaylabs/blindpay-python/commit/625cc91255aa2637f42cb7536d69ecd8a0ae0008))
* remove needs-review label that may not exist ([255b4c9](https://github.com/blindpaylabs/blindpay-python/commit/255b4c928c4b5e112a7b5e369d3aa7a37a901df0))
* remove openapi.json fetch from api-sync-data ([67a30a3](https://github.com/blindpaylabs/blindpay-python/commit/67a30a3d8399d9bd7265fb3e9f813cc1e2c0760c))
* remove openapi.json reference from prompt, use self-contained changelog only ([89d9389](https://github.com/blindpaylabs/blindpay-python/commit/89d9389f770318736c66e1175e75ac046e3ae9cb))
* restore git remote auth before push ([8f2805a](https://github.com/blindpaylabs/blindpay-python/commit/8f2805a12dcf00e2b5fe343b0fdc6b07680940fe))
* restore TOS endpoints ([#43](https://github.com/blindpaylabs/blindpay-python/issues/43)) ([64d838e](https://github.com/blindpaylabs/blindpay-python/commit/64d838e60ef22643da31821f38469c3421528361))
* sanitize workflow inputs ([#44](https://github.com/blindpaylabs/blindpay-python/issues/44)) ([e4db01a](https://github.com/blindpaylabs/blindpay-python/commit/e4db01ac2b6094ba1bfc37e3c9fbb00b9c9bf087))
* **transfers:** type transfers.create's response as CreateTransferOut ([06b6853](https://github.com/blindpaylabs/blindpay-python/commit/06b6853e0e8073824862fffb72f53ed7b86a0509))
* **upload:** add required type and optional metadata to analyze input ([#68](https://github.com/blindpaylabs/blindpay-python/issues/68)) ([9f2acfe](https://github.com/blindpaylabs/blindpay-python/commit/9f2acfe21ab8ed3916fb256ae8cd74d9831c2f4d))
* **upload:** send upload and analyze as multipart/form-data ([eb3db4e](https://github.com/blindpaylabs/blindpay-python/commit/eb3db4e15977f7dbace242d42aec7e6a0c748585))
* use claude_code_oauth_token instead of anthropic_api_key ([23d0512](https://github.com/blindpaylabs/blindpay-python/commit/23d0512050f61e48e5f1a7e96e7bce2ec6004a67))
* use gh api with PAT to fetch openapi.json from private repo ([927d263](https://github.com/blindpaylabs/blindpay-python/commit/927d2633df52a2a086d8b4990e11e59d25c13a2d))
* use PAT for push and PR to trigger CI workflows ([40a773b](https://github.com/blindpaylabs/blindpay-python/commit/40a773baee41c3ad58d066e25950d8ddbd64d842))
* verify real Svix webhooks, send multipart uploads, fix packaging and response types ([a7d047c](https://github.com/blindpaylabs/blindpay-python/commit/a7d047c0db0c323211fd112f503c86547439d29a))
* **wallets:** key custodial wallet balances by uppercase token symbol ([deb273c](https://github.com/blindpaylabs/blindpay-python/commit/deb273c2e149d5d0d7ce5437da192afed6de44ce))
* **webhooks:** let verify_webhook_signature widen its timestamp tolerance ([5dce36e](https://github.com/blindpaylabs/blindpay-python/commit/5dce36e141eeee729b79c9428d5377d0157ca6b3))
* **webhooks:** verify real Svix signatures ([841e00a](https://github.com/blindpaylabs/blindpay-python/commit/841e00ae62d66fb22b6d21d7f1fc5b93b2cd4cc7))


### Documentation

* add readme ([0f2b0e8](https://github.com/blindpaylabs/blindpay-python/commit/0f2b0e84cb5074ecc4b2f16c79baa2ad0f547753))
* document webhook verification, multipart uploads and the version source ([6bda212](https://github.com/blindpaylabs/blindpay-python/commit/6bda21237091c004c2003a767aaa6c0b666dab2f))
* update emails ([499c1b9](https://github.com/blindpaylabs/blindpay-python/commit/499c1b999de7f8a7276d40116a4ba4a1f20d5f62))

## [3.4.1](https://github.com/blindpaylabs/blindpay-python/compare/v3.4.0...v3.4.1) (2026-11-11)


### Bug Fixes

* **bank-accounts:** type bank_accounts.get's response as BankAccountOut ([48df625](https://github.com/blindpaylabs/blindpay-python/commit/48df625318eb8e423b3d16ab826f17b071e4f647))
* **deps:** drop the unused pydantic runtime dependency ([93cffef](https://github.com/blindpaylabs/blindpay-python/commit/93cffef143c85bb051f12ac1c8f40bc121cde0e2))
* **packaging:** report the real SDK version in the User-Agent ([9b7ca97](https://github.com/blindpaylabs/blindpay-python/commit/9b7ca977753a1bdad828bda27ecd25d4413a4de7))
* **packaging:** ship py.typed inside the blindpay package ([2b69201](https://github.com/blindpaylabs/blindpay-python/commit/2b6920162f1549db2272dccdce428ab44d0fd6d0))
* **payouts,payins:** deprecate export(), which calls a route that doesn't exist ([241194e](https://github.com/blindpaylabs/blindpay-python/commit/241194e3183c7e2750593441c468bca1f13e09a3))
* **transfers:** type transfers.create's response as CreateTransferOut ([06b6853](https://github.com/blindpaylabs/blindpay-python/commit/06b6853e0e8073824862fffb72f53ed7b86a0509))
* **upload:** send upload and analyze as multipart/form-data ([eb3db4e](https://github.com/blindpaylabs/blindpay-python/commit/eb3db4e15977f7dbace242d42aec7e6a0c748585))
* verify real Svix webhooks, send multipart uploads, fix packaging and response types ([a7d047c](https://github.com/blindpaylabs/blindpay-python/commit/a7d047c0db0c323211fd112f503c86547439d29a))
* **wallets:** key custodial wallet balances by uppercase token symbol ([deb273c](https://github.com/blindpaylabs/blindpay-python/commit/deb273c2e149d5d0d7ce5437da192afed6de44ce))
* **webhooks:** let verify_webhook_signature widen its timestamp tolerance ([5dce36e](https://github.com/blindpaylabs/blindpay-python/commit/5dce36e141eeee729b79c9428d5377d0157ca6b3))
* **webhooks:** verify real Svix signatures ([841e00a](https://github.com/blindpaylabs/blindpay-python/commit/841e00ae62d66fb22b6d21d7f1fc5b93b2cd4cc7))


### Documentation

* document webhook verification, multipart uploads and the version source ([6bda212](https://github.com/blindpaylabs/blindpay-python/commit/6bda21237091c004c2003a767aaa6c0b666dab2f))

## [3.4.0](https://github.com/blindpaylabs/blindpay-python/compare/v3.3.0...v3.4.0) (2026-08-04)


### Features

* **types:** widen 291 nullable response fields to Optional ([#74](https://github.com/blindpaylabs/blindpay-python/issues/74)) ([2810f7f](https://github.com/blindpaylabs/blindpay-python/commit/2810f7f351af490e3fc994a335cd9d1bbf6e31df))

## [3.3.0](https://github.com/blindpaylabs/blindpay-python/compare/v3.2.2...v3.3.0) (2026-08-04)


### Features

* sync SDK with API changes ([#72](https://github.com/blindpaylabs/blindpay-python/issues/72)) ([e609971](https://github.com/blindpaylabs/blindpay-python/commit/e609971abcc1b8b0aef997b15a69bf15edd56915))

## [3.2.2](https://github.com/blindpaylabs/blindpay-python/compare/v3.2.1...v3.2.2) (2026-08-04)


### Bug Fixes

* **upload:** add required type and optional metadata to analyze input ([#68](https://github.com/blindpaylabs/blindpay-python/issues/68)) ([9f2acfe](https://github.com/blindpaylabs/blindpay-python/commit/9f2acfe21ab8ed3916fb256ae8cd74d9831c2f4d))

## [3.2.1](https://github.com/blindpaylabs/blindpay-python/compare/v3.2.0...v3.2.1) (2026-08-04)


### Bug Fixes

* **customers:** EstimatedAnnualRevenue top band has an extra zero ([#66](https://github.com/blindpaylabs/blindpay-python/issues/66)) ([09892d9](https://github.com/blindpaylabs/blindpay-python/commit/09892d93c6f553ccaef9d1aaf7cf6cc6079116ee))

## [3.2.0](https://github.com/blindpaylabs/blindpay-python/compare/v3.1.1...v3.2.0) (2026-08-04)


### Features

* **types:** fix pagination cursor, billing fee, account type and wallet-create types ([#64](https://github.com/blindpaylabs/blindpay-python/issues/64)) ([767dd62](https://github.com/blindpaylabs/blindpay-python/commit/767dd62c65ada5c2812507af6cbd92a6d39d2869))

## [3.1.1](https://github.com/blindpaylabs/blindpay-python/compare/v3.1.0...v3.1.1) (2026-08-04)


### Bug Fixes

* **ci:** merge the release PR from the push-triggered job ([#60](https://github.com/blindpaylabs/blindpay-python/issues/60)) ([a255d91](https://github.com/blindpaylabs/blindpay-python/commit/a255d91ddda3a1cbdd9d1ad6271dd414a0ed6296))

## [3.1.0](https://github.com/blindpaylabs/blindpay-python/compare/v3.0.0...v3.1.0) (2026-08-04)


### Features

* **api-sync:** deterministic spec-sync patcher (Phase A) ([#58](https://github.com/blindpaylabs/blindpay-python/issues/58)) ([3f157fe](https://github.com/blindpaylabs/blindpay-python/commit/3f157fe9386386bb57d47a0b072ea825bae2da99))

## [3.0.0](https://github.com/blindpaylabs/blindpay-python/compare/v2.5.0...v3.0.0) (2026-08-03)


### ⚠ BREAKING CHANGES

* complete the customers rename, remove receivers/api_keys ([#55](https://github.com/blindpaylabs/blindpay-python/issues/55))

### Features

* complete the customers rename, remove receivers/api_keys ([#55](https://github.com/blindpaylabs/blindpay-python/issues/55)) ([94ea954](https://github.com/blindpaylabs/blindpay-python/commit/94ea954cd720141d872e37c07ac5af5f4cefe085))

## [2.5.0](https://github.com/blindpaylabs/blindpay-python/compare/v2.4.0...v2.5.0) (2026-07-27)


### Features

* **customers:** add customer.* webhook events and customer_id list filters ([#52](https://github.com/blindpaylabs/blindpay-python/issues/52)) ([562f219](https://github.com/blindpaylabs/blindpay-python/commit/562f2190dc53ecc6fc39a41a3d759b8ecb65cb39))

## [2.4.0](https://github.com/blindpaylabs/blindpay-python/compare/v2.3.0...v2.4.0) (2026-06-16)


### Features

* add customers resource, deprecate receivers (v2.3.0) ([#48](https://github.com/blindpaylabs/blindpay-python/issues/48)) ([28b8197](https://github.com/blindpaylabs/blindpay-python/commit/28b81975ded85fb572551e2e52eb3e19a13ce9da))

## [2.3.0](https://github.com/blindpaylabs/blindpay-python/compare/v2.2.0...v2.3.0) (2026-06-16)


### Features

* sync SDK with API changes ([#46](https://github.com/blindpaylabs/blindpay-python/issues/46)) ([55310bc](https://github.com/blindpaylabs/blindpay-python/commit/55310bcc282c4c09a42056575b8cade95224407e))

## [2.2.0](https://github.com/blindpaylabs/blindpay-python/compare/v2.1.0...v2.2.0) (2026-05-07)


### Features

* sync SDK with API changes ([#41](https://github.com/blindpaylabs/blindpay-python/issues/41)) ([24c4e76](https://github.com/blindpaylabs/blindpay-python/commit/24c4e76a28874a90740ad7d06f7b2afd56a17f8f))


### Bug Fixes

* sanitize workflow inputs ([#44](https://github.com/blindpaylabs/blindpay-python/issues/44)) ([e4db01a](https://github.com/blindpaylabs/blindpay-python/commit/e4db01ac2b6094ba1bfc37e3c9fbb00b9c9bf087))

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
