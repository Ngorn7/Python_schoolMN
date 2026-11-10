# School Management

A Django project with three apps — `app_student`, `app_subject`, `app_teacher` —
each with a model, full CRUD (create / show / update / delete / search), and
AdminLTE-styled templates.

## Setup (Docker + PostgreSQL)

The project now runs against PostgreSQL via Docker Compose (previously SQLite).

Default local dev credentials (set in `.env`, override as you like):

| Variable            | Default             |
|---------------------|----------------------|
| `POSTGRES_DB`        | `school_management` |
| `POSTGRES_USER`      | `school_admin`       |
| `POSTGRES_PASSWORD`  | `school_pass123`     |
| `POSTGRES_HOST`      | `db` (the compose service name) |
| `POSTGRES_PORT`      | `5432`               |

```bash
docker compose up --build          # builds the web image, starts Postgres + Django

# in a second terminal, once containers are up:
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser   # optional, for /admin/
```

Visit http://127.0.0.1:8000/ (redirects to the student list).
Admin panel: http://127.0.0.1:8000/admin/
Postgres is also exposed on `localhost:5432` if you want to connect with a GUI client (e.g. TablePlus, DBeaver, psql) using the credentials above.

Stop everything with `docker compose down` (add `-v` to also wipe the database volume).

### Setup (without Docker, using SQLite)

If you'd rather not use Docker/Postgres, revert `DATABASES` in `school_management/settings.py` back to the `sqlite3` engine, then:

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

## Structure

```
school_management/
├── manage.py
├── requirements.txt
├── templates/
│   └── base.html              # AdminLTE 3 layout (sidebar + navbar), extend this
├── school_management/         # project settings/urls
├── app_student/
│   ├── models.py              # Student model: id, last_name, first_name, gender, dob, address
│   │                           #   + create_category / show_category / delete_category /
│   │                           #     update_category / search_category classmethods
│   ├── views.py                # matching CRUD views
│   ├── urls.py
│   └── templates/app_student/  # student_list.html, student_form.html
├── app_subject/
│   ├── models.py               # Subject model: id, subject_name
│   │                           #   + create_subject / show_subject / delete_subject /
│   │                           #     update_subject / search_subject classmethods
│   └── ...
└── app_teacher/
    ├── models.py                # Teacher model: id, last_name, first_name, gender, dob, address, salary
    │                           #   + create_teacher / show_teacher / delete_teacher /
    │                           #     update_teacher / search_teacher classmethods
    └── ...
```

## Routes

| App     | List / Search           | Create               | Update                    | Delete                    |
|---------|--------------------------|-----------------------|----------------------------|----------------------------|
| Student | `/students/`, `/students/search/?q=` | `/students/create/` | `/students/update/<id>/`  | `/students/delete/<id>/`  |
| Subject | `/subjects/`, `/subjects/search/?q=` | `/subjects/create/` | `/subjects/update/<id>/`  | `/subjects/delete/<id>/`  |
| Teacher | `/teachers/`, `/teachers/search/?q=` | `/teachers/create/` | `/teachers/update/<id>/`  | `/teachers/delete/<id>/`  |

## Layout template (AdminLTE)

`templates/base.html` pulls AdminLTE 3, Bootstrap 4, and Font Awesome from CDNs
and defines a sidebar with links to Students / Subjects / Teachers, plus
`{% block content %}` for page content. Customize colors, logo, and the
sidebar menu in that file to match your desired look — that's the
"Customize Layout template AdminLTE" step from the plan.

## Notes

- `ALLOWED_HOSTS = ['*']` is set for local development — restrict this in `settings.py` before deploying.
- All model CRUD is implemented both as classmethods on the models (matching your naming:
  `create_category`, `show_category`, etc. for Student) and wired into views/templates
  for a working browser UI.
- Migrations for all three apps are already generated and applied.
