# DIKOROS — Runbook эксплуатации

## Локальный dev-запуск (Backend)

### Требования
- Windows 11 + WSL2 Ubuntu 24.04
- Node.js 22.x, pnpm 11.x (через corepack)
- Docker Desktop (с интеграцией WSL2)
- Tailscale должен быть остановлен перед стартом — он перехватывает DNS WSL2.
  Проверка: Get-Service Tailscale в PowerShell → Status: Stopped.

### Первый запуск (одноразово)
1. Клонировать репо:

       git clone git@github.com:katuz71/dikoros.git ~/projects/dikoros

2. Перейти в корень:

       cd ~/projects/dikoros

3. Установить зависимости (пониженная параллельность из-за WSL2 NAT):

       pnpm install --network-concurrency=1 --fetch-timeout=120000 --fetch-retries=5

4. Создать apps/backend/.env на основе apps/backend/.env.template.
   Сгенерировать секреты:

       echo "JWT_SECRET=$(openssl rand -hex 32)" >> apps/backend/.env
       echo "COOKIE_SECRET=$(openssl rand -hex 32)" >> apps/backend/.env

### Ежедневный запуск

    cd ~/projects/dikoros
    docker compose -f infra/docker/docker-compose.dev.yml up -d
    docker exec medusa_postgres_dev pg_isready -U medusa -d medusa_db
    pnpm --filter backend dev

Admin: http://localhost:9000/app
API:   http://localhost:9000

### Учётные данные dev-админа
- Email: admin@dikoros.local
- Password: ChangeMe123!
- Пересоздать: cd apps/backend && npx medusa user -e <email> -p <password>

### Остановка
- Ctrl+C в терминале с pnpm dev
- docker compose -f infra/docker/docker-compose.dev.yml down

Volumes docker_medusa_pg_data и docker_medusa_redis_data сохраняются — данные БД не теряются.

### Troubleshooting

pnpm install зависает с ERR_SOCKET_TIMEOUT:
- Проверить, что Tailscale остановлен: Get-Service Tailscale в PowerShell.
- Перезапустить WSL: wsl --shutdown в PowerShell, открыть Ubuntu заново.
- Запустить pnpm install с --network-concurrency=1.

Medusa не подключается к Redis (fake redis instance в логах):
- TODO: настроить модули cache-redis, event-bus-redis, workflow-engine-redis в medusa-config.ts.

git push → Permission denied (publickey):
- ssh -T git@github.com должен ответить "Hi katuz71!"
- Конфиг ключа в ~/.ssh/config: IdentityFile ~/.ssh/id_ed25519_github

---

## Дальнейшие разделы (план)
- Деплой staging
- Деплой production
- Бэкапы и восстановление
- Откат релиза
- Мониторинг и алерты
- Чек-лист инцидента

Полная версия — в Notion (страница «Runbook деплоя и эксплуатации»).
