# API Changes (SDK-relevant)

## Removed Endpoints

- **POST /v1/instances/{instance_id}/vouchers**
- **GET /v1/instances/{instance_id}/vouchers**
- **GET /v1/instances/{instance_id}/vouchers/{id}**
- **PATCH /v1/instances/{instance_id}/vouchers/{id}**
- **DELETE /v1/instances/{instance_id}/vouchers/{id}**

## Modified Endpoints

### /v1/e/payins/{id}

  Response (PayinOut) [GET]:
  - ADDED field: partner_fee_id (string/null, optional)
  - ENUM payment_method: added 1 values: rtp

### /v1/e/payouts/{id}

  Response (PayoutOut) [GET]:
  - ADDED field: partner_fee_id (string/null, optional)

### /v1/instances/{id}

  Request body (UpdateInstanceIn) [PUT]:
  - REMOVED field: wallets_and_transfers

### /v1/instances/{instance_id}/payin-quotes

  Request body (CreatePayinQuoteIn) [POST]:
  - ENUM payment_method: added 1 values: rtp

### /v1/instances/{instance_id}/payins/evm

  Response (CreatePayinOut) [POST]:
  - ENUM payment_method: added 1 values: rtp

### /v1/instances/{instance_id}/payins/{id}

  Response (PayinOut) [GET]:
  - ADDED field: partner_fee_id (string/null, optional)
  - ENUM payment_method: added 1 values: rtp

### /v1/instances/{instance_id}/payouts/{id}

  Response (PayoutOut) [GET]:
  - ADDED field: partner_fee_id (string/null, optional)

## Enum Value Changes

These enum fields gained or lost values across all schemas:

  - actor_type: ADDED 2 values: api_key, user
  - client_type: REMOVED 2 values: domestic, foreign
  - currency: REMOVED 2 values: USDC, USDT
  - operation: ADDED 3 values: create, delete, update
  - payment_method: ADDED 1 values: rtp
  - status: REMOVED 4 values: authorized, error, redeemed, revoked

## New Schemas

- **AuditActor** (4 fields)
- **AuditLog** (17 fields)
- **AuditLogOut** (0 fields)

## Removed Schemas

- **CreateVoucherIn**
- **CreateVoucherOut**
- **GetNotasFiscaisSchemaOut**
- **NotaFiscalItem**
- **UpdateVoucherIn**
- **VoucherOut**
