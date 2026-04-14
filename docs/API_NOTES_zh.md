# API 说明

这份文档记录当前脚本依赖的站点行为，方便后续维护。

## 站点

- `https://ccvaults.com/`

## 认证流程

先换 token：

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

返回：

```json
{"token":"..."}
```

注意：

- 如果不带正确的 `Origin` 和 `Referer`，服务端会返回 `Forbidden: Invalid domain`

## 元数据接口

获取分类：

- `GET /api/categories`

获取全部图标素材：

- `GET /api/assets/all`

获取单个分类：

- `GET /api/assets/{category}`

获取纹理列表：

- `GET /api/textures`

这些接口都需要：

```http
Authorization: Bearer <token>
Accept: application/json
Origin: https://ccvaults.com
Referer: https://ccvaults.com/
```

## 原图直链规则

### 图标

有子分类时：

```text
https://ccvaults.com/assets/{category}/{subcategory}/{file}
```

无子分类时：

```text
https://ccvaults.com/assets/{category}/{file}
```

### 图标缩略图

有子分类时：

```text
https://ccvaults.com/thumbnails/{category}/{subcategory}/{file}
```

无子分类时：

```text
https://ccvaults.com/thumbnails/{category}/{file}
```

### 纹理

```text
https://ccvaults.com/textures/{file}
```

## 当前脚本的实现约束

- 路径段会逐段做 URL 编码
- 图标和纹理索引分开缓存
- 下载时直接请求公开图片 URL，不再带 token

## 如果站点后续改版

优先检查这几项：

1. `/api/token` 是否还存在
2. `x-api-key` 是否变化
3. `Origin` / `Referer` 校验是否变化
4. `/api/assets/all` 返回结构是否变化
5. 原图路径前缀是否仍为 `/assets/` 和 `/textures/`
