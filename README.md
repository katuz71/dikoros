# DIKOROS

Единая цифровая инфраструктура для бренда DIKOROS: сайт, мобильное приложение и операционные процессы на одном бэкенде.

## Стек

- **Backend:** Medusa.js 2.x
- **Web:** Next.js 15 (App Router, TS, Tailwind) + Payload CMS 3.x (встроен)
- **Mobile:** React Native
- **DB:** PostgreSQL 16 (схемы `medusa`, `payload`)
- **Infra:** Hetzner Cloud + Docker Compose + Caddy
- **Storage:** Cloudflare R2
- **Email:** Resend
- **Monitoring:** Sentry + UptimeRobot

Подробности — в [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Структура

```
apps/backend   — Medusa API
apps/web       — Next.js + Payload CMS
apps/mobile    — React Native
packages/      — общий код
infra/         — Docker, Caddy, скрипты
docs/          — документация и ADR
```

## Локальная разработка

> Заглушка. Будет заполнено на Неделе 3, когда поднимем Medusa локально.

```bash
# TODO: docker compose -f infra/docker/docker-compose.dev.yml up -d
# TODO: pnpm install
# TODO: pnpm dev
```

## Документация

- [`docs/CONTEXT.md`](docs/CONTEXT.md) — контекст проекта (для AI и новых участников)
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — архитектурные решения
- [`docs/RUNBOOK.md`](docs/RUNBOOK.md) — эксплуатация (заполнится позже)

## Команда

- **Архитектор и разработчик:** Роман
- **Клиент:** Юра Велигура (DIKOROS)

## Лицензия

Proprietary. All rights reserved.
