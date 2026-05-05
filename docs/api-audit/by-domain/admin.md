# Admin API — контракт текущей веб-админки

Все эндпоинты со статусом **ADMIN** из `contract.md` — те, что вызываются из `admin.html` (vanilla JS, 132 КБ, по тому же домену `app.dikoros.ua`).
После миграции функциональность переезжает в **Medusa Admin** (заказы, товары, юзеры, промо) + **Payload CMS** (баннеры, посты, статика).

Источник вызовов: 32 операции в admin.html, 24 уникальных пути.
Всего: 34 операции (включая `/api/import_xml`, отсутствующую в openapi).

## Products

| Method | Path | Что делает |
|--------|------|------------|
| GET | /api/products | Листинг товаров для админки (с пагинацией) |
| POST | /products | Создание товара |
| PUT | /products/{id} | Редактирование |
| DELETE | /products/{id} | Удаление |
| GET | /products/by-external-id | Поиск по external_id (интеграция Хорошоп) |
| GET | /products/external | Альтернативный путь поиска по external (вероятно дубль) |
| GET | /products/external/{external_id} | Третий вариант поиска по external_id |

**Миграция:** Medusa Admin покрывает CRUD из коробки. Поиск по external_id — стандартное поле `external_id` в Medusa Product, ищется через `?external_id=...`.

---

## Categories

| Method | Path | Что делает |
|--------|------|------------|
| GET | /all-categories | Дерево категорий для админки |
| POST | /categories | Создание категории |
| PUT | /categories/{id} | Редактирование |
| DELETE | /categories/{category_id} | Удаление |
| POST | /categories/{category_id}/banners | Загрузка баннера категории |
| DELETE | /categories/{category_id}/banners | Удаление баннера категории |

**Миграция:** Medusa Admin → ProductCategory. Баннеры категорий — либо в самой Medusa через metadata, либо в Payload как связь Category ↔ Banner.

---

## Banners (главная страница)

| Method | Path | Что делает |
|--------|------|------------|
| POST | /banners | Создание баннера для главной |
| DELETE | /banners/{id} | Удаление |

**Миграция:** в Payload CMS, коллекция `banners` с полями image, link, position, active.

---

## Orders

| Method | Path | Что делает |
|--------|------|------------|
| GET | /api/orders | Листинг всех заказов |
| GET | /api/orders/{order_id} | Детали заказа |
| DELETE | /api/orders/{id} | Удаление заказа |
| PUT | /api/orders/{id}/status | Смена статуса |
| POST | /api/orders/delete-batch | Массовое удаление |
| GET | /orders/export | Экспорт заказов в CSV/Excel |

**Миграция:** Medusa Admin покрывает всё, включая batch-операции через UI. Экспорт — кастомный endpoint в Medusa Admin (есть пример в документации).

---

## Users

| Method | Path | Что делает |
|--------|------|------------|
| GET | /api/admin/users | Листинг юзеров |
| GET | /api/users | Альтернативный листинг (возможно дубль) |
| PUT | /api/users/{phone} | Обновление юзера из админки |
| DELETE | /api/admin/user/{phone} | Удаление юзера |
| POST | /api/admin/users/delete-batch | Массовое удаление |
| GET | /api/users/export | Экспорт юзеров |

**Миграция:** Medusa Admin → Customers. Идентификация по `id`, не по `phone` (phone становится атрибутом).

---

## Posts (блог)

| Method | Path | Что делает |
|--------|------|------------|
| GET | /posts | Листинг постов |
| POST | /posts | Создание поста |
| GET | /posts/{post_id} | Детали поста |
| DELETE | /posts/{post_id} | Удаление |
| GET | /post/{post_id} | Single-форма для совместимости |

**Миграция:** в Payload CMS, коллекция `posts` с полями title, slug, body (rich text), cover, publishedAt.

---

## Promo codes

| Method | Path | Что делает |
|--------|------|------------|
| GET | /api/promo-codes | Листинг |
| POST | /api/promo-codes | Создание |
| DELETE | /api/promo-codes/{id} | Удаление |
| PUT | /api/promo-codes/{id}/toggle | Включение/выключение |

**Миграция:** Medusa Admin → Promotions. Toggle — через `is_active` поле.

---

## Sync / Integrations

| Method | Path | Что делает |
|--------|------|------------|
| POST | /api/import_xml | Импорт XML-фида товаров. **В openapi отсутствует, см. findings №9** |
| POST | /api/sync/catalog | Синхронизация с Хорошопом |

**Миграция:** определяется решением по CRM/PIM (ADR №011, статус «Под пересмотром»). Если уходим от Хорошопа полностью — ручки удаляются. Если остаётся импорт каталога из внешнего источника — переписывается под Medusa Admin кастомным эндпоинтом.

---

## Uploads

| Method | Path | Что делает |
|--------|------|------------|
| POST | /upload | Загрузка изображения (товар, баннер, пост) |
| POST | /upload_csv | Импорт товаров через CSV |

**Миграция:** загрузка файлов — Medusa File Module → Cloudflare R2 (стек проекта). CSV-импорт — отдельный admin-флоу в Medusa.

---

## Сводка для миграции админки

Из 34 ADMIN-операций после миграции:
- **~20 покрываются Medusa Admin из коробки:** products, categories (частично), orders, users, promo, uploads.
- **~8 переезжают в Payload CMS:** banners, posts, статика.
- **~4 требуют решения по интеграциям:** sync/catalog, import_xml, external-id endpoints.
- **2 «невидимые» в openapi:** import_xml, banner (single) — нужен анализ main.py.

Это объём работы на Месяцы 2–3.
