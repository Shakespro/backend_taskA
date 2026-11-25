# Titan Task API

A shared task-management demo built with Python, Django REST Framework, and PostgreSQL. The live backend runs on Render and connects to Neon. Local development uses a separate SQLite database.

[Try the API](https://backend-taska-5.onrender.com/api/tasks/) · [React frontend source](https://github.com/Shakespro/frontend_task)

## API

| Method | Route | Action |
| --- | --- | --- |
| GET | `/api/tasks/` | List tasks |
| POST | `/api/tasks/` | Create a task |
| GET | `/api/tasks/{id}/` | Read a task |
| PUT / PATCH | `/api/tasks/{id}/` | Update a task |
| DELETE | `/api/tasks/{id}/` | Delete a task |

Tasks have a title, description, and completion status. Invalid input returns HTTP 400; missing records return 404.

## Demo limits

This is a public, shared workspace. Visitors can change or delete any task. Use sample data only, never personal or confidential information. The free host may need about a minute to wake up.

The service allows 120 requests and 30 writes per minute per process, with a total cap of 1,000 tasks. Throttling is a basic usage limit, not DDoS protection. Multiple workers or instances require a shared throttle store. The PostgreSQL task cap is checked under a table lock to prevent concurrent creates from exceeding it.

## Local development

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

## Checks

```sh
.venv/bin/python manage.py check
.venv/bin/python manage.py test
```

## Deployment

Configure `DATABASE_URL` and `DJANGO_SECRET_KEY` in the hosting environment. `start.sh` applies migrations, collects static assets, and starts Gunicorn. `.env.example` lists configuration names without credentials.

Do not commit databases, environment files, credentials, or virtual environments. Legacy Git history contains an old development database and credentials; deleting them from the current tree does not revoke secrets or remove historical copies.
