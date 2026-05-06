# Site Audit (Хорошоп → Next.js)

SEO-разведка публичной витрины dikoros-ua.com. Дата снимка: 5 мая 2026.

## Контекст

Хорошоп генерит SEO-метатеги (title, description, og:*) на рендере по шаблону. В API эти поля отдаются пустыми. Чтобы при миграции в Next.js не потерять индексацию и трафик, метатеги сняты с публичной витрины как мастер-данные.

## Артефакты

- urls.csv — 723 URL из sitemap-index (42x3 page + 102x3 news + 97x3 catalog).
- pages.csv — полный snapshot SEO-метатегов: 23 колонки на каждый URL (title, description, h1, canonical, og:*, hreflang, robots, http_status, content_length, last_modified, elapsed_ms и т.д.).
- probe-urls.csv — выборка из 9 URL для валидации парсера (по type x lang).
- meta-summary.txt — ручная сверка парсера на 9 URL.
- analyze-report.txt — сводный отчёт по 723 страницам (статусы, пустые поля, hreflang, og:locale, canonical mismatch, тайминги).
- analyze2-report.txt — детализация аномалий (24 страницы без h1, 133 без og:description, 30 без og:image — все объяснены).
- crawl.py — Python-скрипт, которым снимался snapshot. Стек: httpx (HTTP/2 + brotli) + selectolax + tqdm, throttling 1 req/sec.

## Ключевые выводы

- 723/723 страниц вернули 200 OK. Битых URL в sitemap нет.
- Распределение чистое: 241 уникальная страница x 3 языка (ua/en/ru).
- robots: all на всех страницах, hreflang_count=3 на всех страницах, og_locale симметричен (ua_UA / en_US / ru_RU по 241).
- 15 URL имеют canonical, отличный от final_url — это варианты товара с числовым суффиксом (/1053/, /1071/ и т.д.). При миграции на Medusa варианты сводятся к одному product, со старых URL ставим 301-редиректы.

## Аномалии для миграции (Месяц 4)

- 24 статьи блога без h1 — h1 рендерится как картинка-обложка. При миграции восстановить h1 из title.
- 1 статья без og:title — взять из h1.
- 133 страницы без og:description — генерить из первого абзаца контента (на каталоге из description, на блоге из контента, на категориях из шаблона).
- 30 страниц юридической статики без og:image — общий fallback на логотип.

## Перезапуск краулера

cd <site-audit-folder>
.\.venv\Scripts\Activate.ps1
python crawl.py --input urls.csv --output pages.csv

Требует Python 3.10+, пакеты: httpx[http2], selectolax, tqdm, brotli.
