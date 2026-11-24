# Titan backend recovery — 7 October 2026

## Recovery status recorded in October 2026

The Django API and React frontend now work together locally. Production has not been changed. No existing database could be found. I created `titan-demo-db` on Render’s free plan as an isolated deployment target. Its recorded expiry date was 6 November 2026. The deployment status below reflects the October recovery work; database availability needs to be checked before deployment.

The original Render web service exists, but has no configured environment variables. The previous code hard-coded its database connection. A read-only connection check against that old database failed because the SSL connection was closed. Render's recent application logs showed process lifecycle messages without a database traceback, so the exact production failure has not been established from a trace.

## Local development

Backend:

```sh
cd "/Users/sakhilefihlela/Local Files/code/backend_taskA"
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

Frontend, in another terminal:

```sh
cd "/Users/sakhilefihlela/Local Files/code/frontend_task"
npm ci
npm run dev
```

The frontend's ignored `.env.development.local` sets `REACT_APP_API_URL=http://127.0.0.1:8000/api`. This connects the browser to the local backend. Restart the frontend after changing environment variables. Its production build still uses the hosted API unless `REACT_APP_API_URL` is configured for that build.

The local backend uses a new database at `.local-data/db.sqlite3`. The original tracked `db.sqlite3` was not modified. Both virtual environment and new development data are ignored by Git.

## Request lifecycle

1. A user fills in the React form and presses Save.
2. The modal prevents the browser's default form navigation and passes the task to `handleSubmit`.
3. `handleSubmit` sets saving state and calls `saveTask` from `src/taskApi.js`.
4. `saveTask` uses POST for a new task or PUT for an existing task. Returning after PUT prevents duplicate creation.
5. Django's router in `backend/urls.py` maps `/api/tasks/` and `/api/tasks/<id>/` to `TodoView`.
6. `TodoView`, a Django REST Framework `ModelViewSet`, supplies the standard list, create, retrieve, update, and delete actions.
7. `TodoSerializer` validates the incoming data and converts model objects to JSON. Invalid input produces HTTP 400 rather than being saved.
8. The `Todo` model defines the stored fields: title, description, and completed.
9. Django's ORM writes the record to the configured database. SQLite is used locally; the production database will be the selected PostgreSQL database.
10. The API returns a response. React refreshes its list after success, or keeps the editor and input visible after failure.

The API returns HTTP 200 for reads and updates, 201 for creation, and 204 for deletion. Validation failures return 400, missing records return 404, and unexpected server errors return 500.

## Configuration changes

`backend/settings.py` now reads `DATABASE_URL` from the environment instead of embedding a database password in source. Production requires both `DATABASE_URL` and `DJANGO_SECRET_KEY`; it fails clearly if either is missing. Local development uses an isolated SQLite database and a clearly marked development-only secret.

Production is detected with `RENDER=true` or `DJANGO_ENV=production`. Debug mode is off in production. Allowed hostnames are configured instead of accepting every host. CORS allows the configured frontend origins, including the local React server. CORS is a browser-origin policy, not user authentication.

Django request errors are now directed to the console so hosting logs can expose the cause of future HTTP 500 responses. No secret values are printed by the recovery checks.

`requirements.in` lists intentional runtime dependencies. `requirements.txt` records the exact versions installed and tested on this machine, replacing the old UTF-16 dependency file. Django 5.2 was selected for compatibility with this machine's Python 3.14; support begins with Django 5.2.8 according to the [official release notes](https://docs.djangoproject.com/en/5.2/releases/5.2/).

The Dockerfile uses the matching Python runtime, respects the host's PORT value, and emits Gunicorn request/error logs. `.dockerignore` prevents old virtual environments, local databases, environment files, and Git metadata from entering the image. Docker is not installed here, so the container build itself is not yet verified.

The legacy Pipfile/Pipfile.lock remain historical files. Use `requirements.txt` for the recovered runtime. No migration changes were necessary because the task schema was preserved.

## Validation recorded during recovery

- Django system checks pass.
- Five backend tests pass: CRUD, blank-title validation, missing record, allowed CORS origin, rejected CORS origin.
- The four frontend regression tests from the earlier repair pass.
- Browser check: create task, edit title, mark complete, switch filters, refresh, and find the saved record again.
- A direct local API check confirms there was exactly one updated task, not a duplicate.
- DELETE returns 204 and a subsequent GET confirms the temporary test record was removed.
- The original tracked SQLite database was preserved.

Tests use an isolated test database; the browser check used only a newly created temporary local task.

## Before restoring the hosted service

1. Confirm that the isolated Titan PostgreSQL database is available, or provision a replacement if it has expired. Verify the migration target before deployment.
2. Configure its connection securely in Render as `DATABASE_URL`, with a production Django secret and allowed hosts/origins. `.env.example` documents names, not live credentials.
3. Old embedded credentials remain in repository history. Any still-valid exposed credentials should be replaced before production reuse.
4. Review and deploy the recovered source, then run migrations against the confirmed target database and collect static files. Do not reset or drop an existing database.
5. Verify hosted create, read, update, delete, and persistence before marking the deployment operational.

The task API currently supports a shared demo workspace. Per-user authentication and task ownership are outside the implemented scope; the demo is intended for non-sensitive sample data.

## Implementation decisions

I separated runtime configuration from source code so local development and production use independent databases. The existing task schema remains unchanged, with regression coverage for CRUD, validation, and CORS. Browser checks covered the complete React-to-Django persistence workflow.

The deployment startup script applies pending migrations, collects static assets, and starts Gunicorn. Its database target is configured through `DATABASE_URL`. Hosted API behaviour and database persistence require separate verification from the frontend build.
