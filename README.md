# School Management System

Django project with AdminLTE-styled UI, three apps (`app_student`, `app_subject`, `app_teacher`),
full CRUD + search on each model, login-protected views, and PostgreSQL — all wired up to run
with a single `docker compose up`.

## Option A — Run everything with Docker Compose (recommended)

This spins up two containers: `db` (Postgres) and `web` (Django), networked together.

```bash
cp .env.example .env       # adjust values if you want, defaults already work
docker compose up --build
```

What happens automatically:
- Postgres starts on **host port 5433** (container port 5432), with a persistent volume
  (`postgres_data`) so data survives restarts.
- The `web` container waits for Postgres to be healthy, then runs `migrate` and
  `collectstatic` before starting the dev server (see `docker-entrypoint.sh`).
- Django is served at **http://localhost:8000/**.

Create your login (in a second terminal, while `docker compose up` is running):

```bash
docker compose exec web python manage.py createsuperuser
```

Then visit http://localhost:8000/, log in, and use the sidebar for Students / Subjects / Teachers.
Django admin is at http://localhost:8000/admin/.

To stop:
```bash
docker compose down          # keeps data (volumes preserved)
docker compose down -v       # also wipes the Postgres volume
```

### Connect pgAdmin to the dockerized Postgres

Same as connecting to any local Postgres, since port 5433 is published to your host:

- Host: `localhost`
- Port: `5433`
- Maintenance database: `postgres`
- Username: `postgres`
- Password: `Password123@` (or whatever you set in `.env`)

The `school_management` database is created automatically by the `db` container on first boot
(via `POSTGRES_DB`), so it'll already be there — no manual `CREATE DATABASE` needed with Compose.

> If pgAdmin is *also* running in Docker, it can't reach `localhost:5433` (that's pgAdmin's own
> container). Either put pgAdmin on the same docker-compose network and use host `db` instead
> of `localhost`, or use `host.docker.internal` as the host from a pgAdmin container.

### Compose file layout

```yaml
services:
  db:    # postgres:16, published on host port 5433
  web:   # this Django app, built from ./Dockerfile, published on host port 8000
```

Environment variables (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`) are shared between
both services via `.env`, so they always match — no more typos like `posgres`.

---

## Option B — Run Postgres in Docker, Django locally

If you'd rather run Django directly on your machine (not in a container) but still use Docker
for Postgres — e.g. your original:

```bash
docker run --name some-postgres -p 5433:5432 -e POSTGRES_PASSWORD=Password123@ -d postgres
```

then create the database once:

```bash
docker exec -it some-postgres psql -U postgres -c "CREATE DATABASE school_management;"
```

and run Django with:

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

export POSTGRES_HOST=localhost POSTGRES_PORT=5433   # matches -p 5433:5432 above
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Project structure

```
school_management/
├── Dockerfile
├── docker-compose.yml
├── docker-entrypoint.sh      # waits for postgres, runs migrate + collectstatic
├── .dockerignore
├── .env.example
├── manage.py
├── requirements.txt
├── school_management/        # project settings, root urls, dashboard view
├── app_student/               # Student model + CRUD views/templates
├── app_subject/                # Subject model + CRUD views/templates
├── app_teacher/                # Teacher model + CRUD views/templates
├── templates/                  # base.html (AdminLTE layout), dashboard, login
└── media/                      # uploaded photos (docker volume: media_data)
```

## Models

- **Student**: id, last_name, first_name, gender, dob, address, photo
  + `create_category()`, `show_category()`, `update_category()`, `delete_category()`, `search_category()`
- **Subject**: id, subject_name
  + `create_subject()`, `show_subject()`, `update_subject()`, `delete_subject()`, `search_subject()`
- **Teacher**: id, last_name, first_name, gender, dob, address, salary, photo (+ subjects M2M)
  + `create_teacher()`, `show_teacher()`, `update_teacher()`, `delete_teacher()`, `search_teacher()`

These methods are implemented as model classmethods/instance methods and called from the
corresponding views, matching the naming from the original spec.

## Authentication & Authorization

- All app views are wrapped with `@login_required` (redirects to `/accounts/login/`).
- Django's built-in `auth` app handles login/logout.
- Use `docker compose exec web python manage.py createsuperuser` (or the local equivalent) for
  an admin account, or create regular users via `/admin/` (staff users see a "Django Admin" link
  in the sidebar).
- For role-based permissions (e.g. teachers can't delete students), use Django's built-in
  Groups & Permissions in `/admin/` and swap `@login_required` for
  `@permission_required('app_student.delete_student')` on the relevant views as needed.

## Troubleshooting

- **`web` container exits immediately / can't connect to db**: make sure `db` is healthy first —
  `docker compose ps` should show `db` as `healthy`. The entrypoint script already waits for
  this, but if you override `command:` in compose you'll skip that wait.
- **Static files look unstyled**: AdminLTE/Bootstrap are loaded from CDN, so you need internet
  access from your browser (not the container) for the theme to render.
- **Port already in use**: if `5433` or `8000` are taken on your machine, change the left-hand
  side of the `ports:` mapping in `docker-compose.yml` (e.g. `"5434:5432"`), and update
  `POSTGRES_PORT` in `.env` to match if you connect from outside Compose.
