# Infrastructure — SERVICE и DEAD эндпоинты

Эндпоинты, которые **не относятся** ни к мобайлу, ни к админке.

- **SERVICE** — инфраструктурные ручки, которые сохраняем при миграции (функцию, не реализацию).
- **DEAD** — мёртвые дубли, заброшенные фичи, legacy. Не переносим.

Всего: 7 SERVICE + 31 DEAD = 38 операций.

---

## SERVICE — сохраняем при миграции

### Health

| Method | Path | Назначение | Куда переезжает |
|--------|------|------------|-----------------|
| GET | /health | Health check для UptimeRobot | Сохраняется в Medusa (стандартный `/health`) |

### Payments

| Method | Path | Назначение | Куда переезжает |
|--------|------|------------|-----------------|
| POST | /api/payment/callback | Webhook от Монобанка | Medusa Payment Provider для Монобанка → отдельный модуль, webhook-эндпоинт сохраняется |

### Delivery (прокси НП)

| Method | Path | Назначение | Куда переезжает |
|--------|------|------------|-----------------|
| GET | /api/delivery/cities | Прокси к Новой Почте: список городов | Кастомный route в Medusa Admin (или Next.js API route) с серверным ключом НП |
| GET | /api/delivery/popular-cities | Кэш популярных городов | Аналогично |
| GET | /api/delivery/warehouses | Прокси отделений НП | Аналогично |

**См. findings №3** — про утечку ключа НП в RN.

### Static / SEO pages

| Method | Path | Назначение | Куда переезжает |
|--------|------|------------|-----------------|
| GET | /about | О компании | Payload CMS, коллекция `static-pages`, отдаётся через Next.js |
| GET | /privacy-policy | Политика конфиденциальности | То же |
| GET | /returns | Возвраты | То же |
| GET | /delivery-payment | Доставка и оплата | То же |

**Миграция SEO:** статические страницы — это не ручки, а контент. URL должны сохраниться 1:1 для сохранения позиций (требование ADR — SEO-миграция, Месяц 4).

---

## DEAD — не переносим

Группировка по причине «смерти».

### Дубли через префикс /api

Те же ручки, что есть в основной версии без префикса (или наоборот). При миграции — выбираем одну версию (Medusa-конвенцию), остальные не существуют.

- `GET /api/banners` (дубль `/banners`)
- `GET /api/categories` (дубль `/all-categories`)
- `GET /api/all-categories` (дубль `/all-categories`)
- `GET /api/products/{id}` (дубль `/products/{id}`)
- `GET /api/product/{id}` (дубль в единственном числе)
- `GET /product/{id}` (ещё один дубль)
- `DELETE /orders/{id}` (дубль `/api/orders/{id}`)
- `PUT /orders/{id}/status` (дубль `/api/orders/{id}/status`)
- `POST /orders/delete-batch` (дубль `/api/orders/delete-batch`)
- `GET /api/post`, `/api/posts`, `/api/post/{post_id}`, `/api/posts/{post_id}` (дубли постов)
- `GET /post` (single-форма листинга)
- `POST /api/chat`, `POST /api/v1/chat` (дубли `/chat`, см. findings №11)
- `GET /user/{identifier}` (дубль `/user/{phone}`)

### Заброшенные фичи

Реализованы на бэке, но не используются ни мобайлом, ни админкой.

- `POST /api/auth/social-login` — соцлогин
- `GET /api/user/me` — современный /me-эндпоинт по токену (токенов нет)
- `POST /api/user/push-token` — регистрация push-токенов (см. findings №6)
- `POST /api/track` — событийная аналитика
- `POST /api/recalculate-cashback` — кешбек
- `GET /delete-account` — статичная страница удаления аккаунта (см. findings №7 — критично, должна быть **рабочей** ручкой в Medusa)

### Опасные / служебные legacy

- `GET /api/clear_products` — GET, который очищает каталог (см. findings №8)
- `GET /api/image` — самописный image-resizer, заменяется на Cloudflare/next-image
- `GET /admin` — отдаёт admin.html, после миграции вся админка в Medusa Admin

---

## Что отсюда уходит в риски и открытые вопросы

В **риски** (HIGH severity):
- `GET /api/clear_products` — потенциальная потеря каталога.
- `/delete-account` — блокер для App Store / Google Play.

В **открытые вопросы** клиенту:
- Push-уведомления — нужны или отказываемся.
- Кешбек — была живая фича или эксперимент.
- Соцлогин — планируется или забываем.
- `shop.db` (SQLite на проде) — что это и нужно ли мигрировать.
