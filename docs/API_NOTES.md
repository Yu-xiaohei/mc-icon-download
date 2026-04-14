# API Notes

This file records the remote behavior the script depends on.

## Site

- `https://ccvaults.com/`

## Auth Flow

The site first exchanges an API key for a bearer token:

```http
POST /api/token
Host: ccvaults.com
x-api-key: mcicons-apikey-0201osaiudx-24493534
Origin: https://ccvaults.com
Referer: https://ccvaults.com/
Content-Type: application/json
```

Body:

```json
{}
```

Response:

```json
{"token":"..."}
```

Important:

- Without the expected `Origin` and `Referer`, the server returns `Forbidden: Invalid domain`.

## Metadata Endpoints

- `GET /api/categories`
- `GET /api/assets/all`
- `GET /api/assets/{category}`
- `GET /api/textures`

These endpoints require:

```http
Authorization: Bearer <token>
Accept: application/json
Origin: https://ccvaults.com
Referer: https://ccvaults.com/
```

## Direct File URL Rules

### Icons

With subcategory:

```text
https://ccvaults.com/assets/{category}/{subcategory}/{file}
```

Without subcategory:

```text
https://ccvaults.com/assets/{category}/{file}
```

### Icon thumbnails

With subcategory:

```text
https://ccvaults.com/thumbnails/{category}/{subcategory}/{file}
```

Without subcategory:

```text
https://ccvaults.com/thumbnails/{category}/{file}
```

### Textures

```text
https://ccvaults.com/textures/{file}
```

## Current Script Assumptions

- URL path segments are encoded independently.
- Icon and texture indexes are cached separately.
- Actual downloads use the public file URLs and do not require the bearer token.

## What To Re-check If The Site Changes

1. Whether `/api/token` still exists
2. Whether the API key changed
3. Whether the `Origin` and `Referer` checks changed
4. Whether `/api/assets/all` still returns the same shape
5. Whether the public file prefixes are still `/assets/`, `/thumbnails/`, and `/textures/`
