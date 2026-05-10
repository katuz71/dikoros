# DIKOROS — Roadmap

> **Источник истины по задачам:** Notion → база «✅ Задачи».
> Здесь — только высокоуровневый помесячный план для быстрой ориентации.
> Детализация (49 задач, статусы, зависимости, часы) живёт в Notion и синхронизируется скриптом `infra/scripts/notion-sync/notion-sync.py`.
>
> Последнее обновление: 9 мая 2026.

## Месяц 1 — Май 2026 (фундамент)

- **Неделя 1 (5–11 мая):** discovery, аудит Хорошопа, OpenAPI-снапшот, SEO-краул, GSC-экспорт, сбор доступов, ТЗ-черновик, bootstrap Medusa 2.14.2. ✅ Закрыто (этапы 1–10).
- **Неделя 2 (12–18 мая):** реальный Redis, seed-скрипт, storefront starter (Next.js 15), brand-guide, ADR 014 (платежи), синк документации, weekly report, клиентский созвон.
- **Неделя 3 (19–25 мая):** скелет cashback-модуля, payment-provider (LiqPay sandbox), Nova Poshta интеграция, ngrok-вебхуки, weekly report.
- **Неделя 4 (26 мая – 1 июня):** брендинг витрины, i18n setup, embed Payload CMS, **украинский перевод Medusa Admin** (i18n JSON), демо клиенту, weekly report.

## Месяц 2 — Июнь 2026 (контент и миграция)

Payload-схемы, наполнение витрины, миграция данных Хорошоп → Medusa, скелет cashback/loyalty.

## Месяц 3 — Июль 2026 (mobile и платежи в prod)

Bootstrap React Native + Expo, продовые ключи LiqPay/Fondy/Monobank, push-уведомления.

## Месяц 4 — Август 2026 (инфраструктура)

Hetzner CX22 deploy, Caddy + SSL, staging Medusa, CI/CD (GitHub Actions), Sentry, UptimeRobot, бэкапы Postgres → Cloudflare R2 (30 дней), нагрузочное тестирование, SEO-редиректы (301).

## Месяц 5 — Сентябрь 2026 (запуск)

Финальная вычитка украинского перевода админки, финальная миграция, cut-over домена, 30-дневный hyper-care, hand-over клиенту.

## Ссылки

- Notion (задачи): см. `infra/scripts/notion-sync/.env` → `NOTION_TASKS_DATA_SOURCE_ID`
- Скрипт синхронизации: `infra/scripts/notion-sync/notion-sync.py`
- ADR: `docs/adr/`
- Контекст: `docs/CONTEXT.md`
- Архитектура: `docs/ARCHITECTURE.md`
- Runbook (dev-окружение): `docs/RUNBOOK.md`
