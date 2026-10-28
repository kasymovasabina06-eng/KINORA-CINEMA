# Структура Django и MTV

- `manage.py` — команды управления Django, запуск сервера.
- `config/settings.py` — настройки проекта, приложения, шаблоны, статика.
- `config/urls.py` — корневая маршрутизация через `include()`.
- `config/wsgi.py` — WSGI-точка входа для веб-сервера.
- `config/asgi.py` — ASGI-точка входа.
- **Model** — пока данные в `movies/data.py`; во втором модуле будут `movies/models.py`.
- **Template** — HTML-шаблоны в `templates/`.
- **View** — обработчики в `pages/views.py`, `movies/views.py`.
