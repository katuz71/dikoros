# Storefront API — контракт мобильного приложения

Все эндпоинты со статусом **USED** из `contract.md` — те, что вызываются из RN-приложения DIKOROS.
Это контракт, который должен сохраниться (или быть совместимо переписан) при миграции на Medusa.

Источник вызовов: 17 уникальных API-вызовов после нормализации, 9 файлов RN-фронта.
Всего: 17 операций.

## Auth

| Method | Path | Где зовётся в RN | Тело запроса / параметры | Что возвращает |
|--------|------|------------------|--------------------------|----------------|
| POST | /api/auth | `services/auth.ts`, `context/AuthContext.tsx` | `{ phone, otp? }` (точная схема — в openapi) | Профиль юзера, без токенов. **См. findings №2.** |

**Миграция в Medusa:** заменяется на `POST /store/auth` с JWT. Требует переписывания `AuthContext` в RN.

---

## Users

| Method | Path | Где зовётся в RN | Параметры | Что возвращает |
|--------|------|------------------|-----------|----------------|
| GET | /user/{phone} | `app/profile.tsx`, `services/userService.ts` | `phone` в URL | Профиль юзера |
| PUT | /api/user/info/{phone} | `app/profile/edit.tsx` | `phone` в URL, body — поля профиля | Обновлённый профиль |

**Миграция:** `GET /store/customers/me` + `POST /store/customers/me` (Medusa резолвит юзера по JWT, не по phone).

---

## Products

| Method | Path | Где зовётся в RN | Параметры | Что возвращает |
|--------|------|------------------|-----------|----------------|
| GET | /products | `app/(tabs)/index.tsx`, `app/category/[slug].tsx`, `store/productsStore.ts` | Без параметров или `?id={id}` (мобайл зовёт оба варианта — фактически одна и та же ручка) | Массив товаров с пагинацией |
| GET | /products/{id} | `app/product/[id].tsx` | `id` в URL | Один товар |

**Замечания:**
- Контракт `Product` в openapi отсутствует — восстанавливать из реальных ответов прода (см. findings №4).
- Категории строятся клиентски из `product.category` (см. findings №5).

**Миграция:** `GET /store/products`, `GET /store/products/{id}`. Категории — отдельные сущности `ProductCategory`.

---

## Orders

| Method | Path | Где зовётся в RN | Параметры | Что возвращает |
|--------|------|------------------|-----------|----------------|
| POST | /create_order | `app/checkout.tsx` | Body — корзина + доставка + контакты | Созданный заказ |
| GET | /api/client/orders/{phone} | `app/(tabs)/orders.tsx` | `phone` в URL | История заказов юзера |
| DELETE | /api/client/orders/{order_id} | `app/order/[id].tsx` | `order_id` в URL | Подтверждение удаления |
| DELETE | /api/client/orders/clear/{phone} | `app/(tabs)/orders.tsx` | `phone` в URL | Очистка всей истории. **Опасная ручка по phone без токена, см. findings №2.** |

**Миграция:** `POST /store/carts/{id}/complete`, `GET /store/customers/me/orders`. Удаление заказа клиентом — нестандартная фича для e-commerce (обычно только отмена), пересмотреть с Юрой бизнес-логику.

---

## Reviews

| Method | Path | Где зовётся в RN | Параметры | Что возвращает |
|--------|------|------------------|-----------|----------------|
| POST | /api/reviews | `app/product/[id].tsx`, `components/ReviewForm.tsx` | Body — текст, рейтинг, productId | Созданный отзыв |
| DELETE | /api/reviews/{id} | `app/profile/reviews.tsx` | `id` в URL | Подтверждение |
| GET | /api/reviews/{product_id} | `app/product/[id].tsx` | `product_id` в URL | Массив отзывов на товар |
| GET | /api/user/reviews/{phone} | `app/profile/reviews.tsx` | `phone` в URL | Отзывы юзера |

**Миграция:** в Medusa отзывов нет из коробки — нужен модуль (либо самописный через Module API, либо стороннее решение). Решение — отдельный ADR в Месяце 2.

---

## Promo codes

| Method | Path | Где зовётся в RN | Параметры | Что возвращает |
|--------|------|------------------|-----------|----------------|
| POST | /api/promo-codes/validate | `app/checkout.tsx` | Body — `{ code, cartTotal? }` | Валидность + размер скидки |

**Миграция:** Medusa использует механизм Promotions/Discounts через корзину — `POST /store/carts/{id}/promotions`. Логика «валидации без применения» — отдельным эндпоинтом или клиентской проверкой.

---

## Banners

| Method | Path | Где зовётся в RN | Параметры | Что возвращает |
|--------|------|------------------|-----------|----------------|
| GET | /banners | `app/(tabs)/index.tsx` | Без параметров | Массив баннеров для главной |

**Миграция:** баннеры — это контент, переезжают в **Payload CMS** как коллекция `banners`. Фронт зовёт `/api/cms/banners` через Next.js API route.

---

## Chat

| Method | Path | Где зовётся в RN | Параметры | Что возвращает |
|--------|------|------------------|-----------|----------------|
| POST | /chat | `app/chat.tsx` | Body — `{ message, sessionId? }` | Ответ бота |

**Миграция:** решение по чат-боту отложено до 3-го месяца (ADR №012, статус «Предложено»). На бэке три варианта одной ручки (`/chat`, `/api/chat`, `/api/v1/chat`) — мобайл зовёт версию без префикса.

---

## Внешние вызовы (минуя бэк)

Мобайл также делает прямые вызовы к **Новой Почте**:

- `POST https://api.novaposhta.ua/v2.0/json/` — города, отделения. Вызывается из `app/checkout.tsx`.

**Миграция:** все вызовы НП — только через бэк-прокси. См. findings №3 (утечка ключа).

---

## Сводка для миграции мобайла

Из 17 USED-операций после миграции на Medusa:
- **8 заменяются стандартными Medusa-ручками:** auth, users, products (×2), orders (×3), promo.
- **4 требуют доработки/модулей:** reviews (×4) — нужен модуль, либо вынести в Payload.
- **2 переезжают в Payload CMS:** banners, chat (если останется).
- **3 пересмотреть с Юрой:** удаление своих заказов клиентом (×2), история заказов (стандартный паттерн).

Это объём работы по API-слою RN на Месяц 3.
