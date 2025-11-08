
# HemoVital - Starter Django Project (Boilerplate)

This is a minimal, ready-to-run boilerplate for the HemoVital project.

**How to use**:

1. Create a virtual env and install requirements:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Run migrations and start server:

```bash
python manage.py migrate
python manage.py runserver
```

Note: Update `.env` with a secure SECRET_KEY and set DEBUG=False for production.
