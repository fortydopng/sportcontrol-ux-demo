# Исходники эскизов и сайта

Эти скрипты рисуют кадры и собирают демонстрационный сайт. Данные вымышленные.

- `mock_access.py` — кадры экранов в стиле Access 2024: HTML → PNG через Playwright (Chromium), размер 1440×960 при двойной плотности; бланк A4 — 1122×794. Пишет в `/home/claude/site/frames/`. Аргументы — имена кадров, чтобы перерисовать только их: `python3 mock_access.py start newsession prepared nextday`. Кадры: `start`, `newsession`, `prepared`, `nextday` (сценарий «Начало работы»); `blank`, `entry`, `confirmed` (сеанс); `history`; `report_params`, `report_preview`.
- `build_site.py` — собирает сайт из кадров: `index.html`, `style.css`, `app.js`, `img/` (полные кадры и увеличенные фрагменты). Пишет в `/home/claude/site/web/`.

Порядок: `python3 mock_access.py && python3 build_site.py`, затем скопировать содержимое `web/` в корень репозитория и опубликовать. Если перерисовываются не все кадры, перед сборкой скопировать существующие полные кадры из `img/` (без `_z`) в `frames/`. Папки `frames/` и `web/` в репозиторий не входят. Автор коммитов — SportControl.

Целевой экран врача: 2880×1920 (3:2). При масштабе Windows 200% рабочая область 1440×960 — формы ввода должны помещаться без прокрутки вправо.
