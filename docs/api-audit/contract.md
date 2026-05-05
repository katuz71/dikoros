# DIKOROS — API Contract

Полный контракт текущего API DIKOROS (FastAPI на app.dikoros.ua).
Источник: `openapi.json` (OpenAPI 3.1.0, снят 5 мая 2026).
Сверено с: 17 вызовами из RN-приложения и 24 уникальными вызовами из admin.html.

## Легенда статусов

- **USED** — вызывается из RN-приложения. Контракт критичен для миграции на Medusa: мобайл должен работать после переезда без изменений в клиенте либо с минимальными правками API-слоя.
- **ADMIN** — вызывается из admin.html (текущая веб-админка). После миграции заменяется на админку Medusa + Payload и в публичный API не выходит.
- **SERVICE** — инфраструктурные ручки: health, webhooks внешних систем, статические SEO-страницы. Сохраняем функцию при миграции, но реализация уезжает в другие места стека (Next.js, Payload, Caddy).
- **DEAD** — не вызывается ниоткуда. Дубли через префикс `/api/`, заброшенные фичи, legacy. При миграции не переносим.

## Сводка

- Всего операций: 89 (плюс 2 «невидимые» в admin.html, которых нет в openapi)
- USED: 17
- ADMIN: 34
- SERVICE: 7
- DEAD: 31

## Таблица

### Auth (1 USED, 1 DEAD)

| Method | Path | Status | Summary | Notes |
|--------|------|--------|---------|-------|
| POST | /api/auth | USED | Auth User | Авторизация мобайла. По телефону, без токенов в заголовках — security issue, см. findings. |
| POST | /api/auth/social-login | DEAD | Auth Social Login | Соцлогин на бэке готов, ни мобайл, ни админка не зовут. Заброшенная фича. |

### Users (2 USED, 5 ADMIN, 2 DEAD)

| Method | Path | Status | Summary | Notes |
|--------|------|--------|---------|-------|
| GET | /user/{phone} | USED | Get User Profile | Мобайл получает профиль по телефону. |
| PUT | /api/user/info/{phone} | USED | Update User Info | Мобайл обновляет профиль. |
| GET | /api/admin/users | ADMIN | Get Admin Users | Список юзеров для админки. |
| DELETE | /api/admin/user/{phone} | ADMIN | Delete Admin User | Удаление юзера из админки. |
| POST | /api/admin/users/delete-batch | ADMIN | Delete Users Batch | Массовое удаление юзеров. |
| GET | /api/users | ADMIN | Get Users | Альтернативный список юзеров. Возможно, дубль с /api/admin/users — проверить. |
| PUT | /api/users/{phone} | ADMIN | Update User | Админка обновляет юзера здесь, а мобайл — через /api/user/info/{phone}. Два пути обновления. |
| GET | /api/users/export | ADMIN | Export Users | Экспорт юзеров. |
| GET | /user/{identifier} | DEAD | Get User By Phone | Дубликат /user/{phone}. Идентификатор переименован, старый путь оставлен. |
| GET | /api/user/me | DEAD | Get Api User Me | Современный /me-эндпоинт по токену, никем не зовётся (потому что токенов нет). |

### Products (3 USED, 6 ADMIN, 7 DEAD)

| Method | Path | Status | Summary | Notes |
|--------|------|--------|---------|-------|
| GET | /products | USED | Get Products Paginated | Мобайл зовёт и `/products`, и `/products?id={id}` — обе ветки сюда. |
| GET | /products/{id} | USED | Get Product | Мобайл зовёт детали товара. |
| POST | /products | ADMIN | Create Product | Создание товара из админки. |
| PUT | /products/{id} | ADMIN | Update Product | Обновление товара из админки. |
| DELETE | /products/{id} | ADMIN | Delete Product | Удаление товара из админки. |
| GET | /api/products | ADMIN | Get Products Paginated | Админка зовёт версию с /api для своего листинга. Дубль /products. |
| GET | /products/by-external-id | ADMIN | Get Product By External Id Query | Поиск по external_id (интеграция с Хорошопом). |
| GET | /products/external | ADMIN | Get Product By External Query | Альтернативный путь поиска по external. Похоже на дубль предыдущего. |
| GET | /products/external/{external_id} | ADMIN | Get Product By External Id | Третий вариант поиска по external_id. |
| GET | /api/products/{id} | DEAD | Get Product | Дубль /products/{id}. |
| GET | /api/product/{id} | DEAD | Get Product | Дубль в единственном числе. |
| GET | /product/{id} | DEAD | Get Product | Ещё один дубль в единственном числе без /api. Итого 4 ручки одного товара. |
| GET | /api/clear_products | DEAD | Clear Products Db | GET, который очищает базу товаров. Опасно: префетчеры/кэш-пробы могут уронить каталог. См. findings. |
| GET | /api/image | DEAD | Get Resized Image | Самописный image-resizer. Заменяется на Cloudflare Images / next-image при миграции. |
| POST | /upload | ADMIN | Upload Image | Загрузка изображений из админки. Подтверждено вызовом в admin.html. |
| POST | /upload_csv | ADMIN | Upload Csv | Импорт товаров через CSV из админки. Подтверждено вызовом в admin.html. |

### Categories (1 ADMIN, 5 DEAD)

| Method | Path | Status | Summary | Notes |
|--------|------|--------|---------|-------|
| POST | /categories | ADMIN | Add Category | Создание категории из админки. |
| PUT | /categories/{id} | ADMIN | Update Category | Обновление категории. |
| DELETE | /categories/{category_id} | ADMIN | Delete Category | Удаление категории. |
| POST | /categories/{category_id}/banners | ADMIN | Upload Category Banner | Загрузка баннера категории. |
| DELETE | /categories/{category_id}/banners | ADMIN | Delete Category Banner | Удаление баннера категории. |
| GET | /all-categories | ADMIN | Get Categories | Админка зовёт для дерева категорий. Мобайл строит категории клиентски из product.category. |
| GET | /api/all-categories | DEAD | Get Categories | Дубль /all-categories. |
| GET | /api/categories | DEAD | Get Categories Api | Третий вариант листинга категорий, никем не зовётся. |

### Orders (3 USED, 7 ADMIN, 4 DEAD)

| Method | Path | Status | Summary | Notes |
|--------|------|--------|---------|-------|
| POST | /create_order | USED | Create Order | Мобайл создаёт заказ. Ручка снаружи иерархии /orders. |
| GET | /api/client/orders/{phone} | USED | Get Client Orders | Мобайл получает историю заказов юзера. |
| DELETE | /api/client/orders/{order_id} | USED | Delete Client Order | Мобайл удаляет свой заказ. |
| DELETE | /api/client/orders/clear/{phone} | USED | Clear Client Orders | Мобайл очищает историю. Опасная ручка по {phone} без токена. |
| GET | /api/orders | ADMIN | Get Orders Api | Список заказов в админке. Зовётся с `?t=Date.now()` для кеш-бастинга. |
| GET | /api/orders/{order_id} | ADMIN | Get Order By Id | Детали заказа в админке. |
| DELETE | /api/orders/{id} | ADMIN | Delete Order Api | Удаление заказа из админки. |
| PUT | /api/orders/{id}/status | ADMIN | Update Order Status Api | Смена статуса. |
| POST | /api/orders/delete-batch | ADMIN | Delete Orders Batch Api | Массовое удаление. |
| GET | /orders/export | ADMIN | Export Orders | Экспорт заказов в CSV/Excel. |
| DELETE | /orders/{id} | DEAD | Delete Order | Дубль /api/orders/{id}. |
| PUT | /orders/{id}/status | DEAD | Update Order Status | Дубль /api/orders/{id}/status. |
| POST | /orders/delete-batch | DEAD | Delete Orders Batch | Дубль /api/orders/delete-batch. |

### Reviews (3 USED)

| Method | Path | Status | Summary | Notes |
|--------|------|--------|---------|-------|
| POST | /api/reviews | USED | Create Review | Мобайл создаёт отзыв. |
| DELETE | /api/reviews/{id} | USED | Delete Review | Мобайл удаляет свой отзыв. |
| GET | /api/reviews/{product_id} | USED | Get Product Reviews | Список отзывов на товар. |
| GET | /api/user/reviews/{phone} | USED | Get User Reviews | Отзывы юзера по телефону. |

### Promo codes (1 USED, 4 ADMIN)

| Method | Path | Status | Summary | Notes |
|--------|------|--------|---------|-------|
| POST | /api/promo-codes/validate | USED | Validate Promo Code | Мобайл проверяет промокод на чекауте. |
| GET | /api/promo-codes | ADMIN | Get Promo Codes | Список промокодов в админке. |
| POST | /api/promo-codes | ADMIN | Create Promo Code | Создание промокода. |
| DELETE | /api/promo-codes/{id} | ADMIN | Delete Promo Code | Удаление. |
| PUT | /api/promo-codes/{id}/toggle | ADMIN | Toggle Promo Code | Включить/выключить. |

### Banners (1 USED, 2 ADMIN, 1 DEAD)

| Method | Path | Status | Summary | Notes |
|--------|------|--------|---------|-------|
| GET | /banners | USED | Get Banners | Мобайл получает баннеры на главной. |
| POST | /banners | ADMIN | Create Banner | Создание баннера. |
| DELETE | /banners/{id} | ADMIN | Delete Banner | Удаление баннера. |
| GET | /api/banners | DEAD | Get Banners | Дубль /banners. |

### Posts / Blog (5 ADMIN, 5 DEAD)

| Method | Path | Status | Summary | Notes |
|--------|------|--------|---------|-------|
| GET | /posts | ADMIN | Get Posts | Зовёт админка через `fetch(url)` динамически — пометить как ADMIN с пометкой «вероятно». |
| POST | /posts | ADMIN | Create Post | Создание поста в админке. |
| GET | /posts/{post_id} | ADMIN | Get Post | Детали поста. |
| DELETE | /posts/{post_id} | ADMIN | Delete Post | Удаление. |
| GET | /post/{post_id} | ADMIN | Get Post | Single-форма для совместимости со старым клиентом. |
| GET | /post | DEAD | Get Posts | Single-форма листинга. Никто не зовёт. |
| GET | /api/post | DEAD | Get Posts | /api/-дубль. |
| GET | /api/posts | DEAD | Get Posts | /api/-дубль. |
| GET | /api/post/{post_id} | DEAD | Get Post | /api/-дубль. |
| GET | /api/posts/{post_id} | DEAD | Get Post | /api/-дубль. |

### Chat (1 USED, 2 DEAD)

| Method | Path | Status | Summary | Notes |
|--------|------|--------|---------|-------|
| POST | /chat | USED | Chat Endpoint | Мобайл зовёт чат-бота. |
| POST | /api/chat | DEAD | Chat Endpoint Api | Дубль. Проверить в main.py — какая из трёх реально обрабатывает запросы. |
| POST | /api/v1/chat | DEAD | Chat Endpoint Api V1 | Версионированный вариант, никто не зовёт. Единственный случай /v1/ во всём API — попытка упорядочивания, заброшенная. |

### Delivery (3 SERVICE)

| Method | Path | Status | Summary | Notes |
|--------|------|--------|---------|-------|
| GET | /api/delivery/cities | SERVICE | Get Np Cities | Прокси к Новой Почте. Мобайл частично ходит напрямую на api.novaposhta.ua — см. findings. |
| GET | /api/delivery/popular-cities | SERVICE | Get Popular Cities | Прокси/кэш популярных городов НП. |
| GET | /api/delivery/warehouses | SERVICE | Get Np Warehouses | Прокси отделений НП. |

### Payments (1 SERVICE)

| Method | Path | Status | Summary | Notes |
|--------|------|--------|---------|-------|
| POST | /api/payment/callback | SERVICE | Payment Callback Monobank | Webhook от Монобанка. Server-to-server, фронт не зовёт. |

### Sync / Integrations (1 ADMIN, 2 DEAD)

| Method | Path | Status | Summary | Notes |
|--------|------|--------|---------|-------|
| POST | /api/import_xml | ADMIN* | Import XML (нет в openapi) | Зовётся из admin.html, но **в openapi отсутствует**. Реализация в main.py обходит FastAPI schema. См. findings — третья «невидимая» ручка. |
| POST | /api/sync/catalog | ADMIN | Sync Catalog Horoshop | Синхронизация с Хорошопом. После миграции — либо удаляем, либо переписываем под Medusa. |
| POST | /api/track | DEAD | Track Event Endpoint | Аналитика, никем не зовётся. |
| POST | /api/recalculate-cashback | DEAD | Recalculate All Cashback | Кешбек на бэке готов, фронт не использует. Заброшенная фича. |
| POST | /api/user/push-token | DEAD | Save Push Token | Push готов на бэке, мобайл не регистрирует токены. **Push-уведомления не работают.** |
| GET | /delete-account | DEAD | Get Delete Account | Обязательная ручка для App Store / Google Play (требование сторов с 2022). Мобайл не зовёт. **Блокер для публикации обновлений в сторах. Записать в риски.** |

### Static / SEO pages (4 SERVICE)

| Method | Path | Status | Summary | Notes |
|--------|------|--------|---------|-------|
| GET | /about | SERVICE | Get About Page | Статика. При миграции — Payload CMS как контент-страница. |
| GET | /privacy-policy | SERVICE | Get Privacy Page | Аналогично. |
| GET | /returns | SERVICE | Get Returns Page | Аналогично. |
| GET | /delivery-payment | SERVICE | Get Delivery Page | Аналогично. |

### Misc / Infrastructure (1 SERVICE, 1 DEAD)

| Method | Path | Status | Summary | Notes |
|--------|------|--------|---------|-------|
| GET | /health | SERVICE | Health Check | Health для UptimeRobot. Сохраняем. |
| GET | /admin | DEAD | Read Admin | Отдаёт admin.html. После миграции вся админка переезжает в Medusa Admin + Payload, эта ручка не нужна. |

## Что не вошло в таблицу

- `POST /categories/{id}/banner` (единственное число) — admin.html вызывает, но в openapi нет. Либо мёртвая ветка кода в админке, либо ручка существует в main.py и не отражена в openapi (что для FastAPI странно). Деталь — в findings.md.
- `GET /api/orders?t=...` — это не отдельный путь, а `/api/orders` с кеш-бастером. Учтено в строке /api/orders.
