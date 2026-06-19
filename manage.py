# AI Content Moderation API

A Django + Django REST Framework API that accepts text or image content and
returns a moderation decision (flagged / not flagged, a reason, and a
confidence score). Every request is logged to the database for auditing.

> Note: This project uses **Django**, not FastAPI. There is nothing to install
> for FastAPI.


## Frontend console

A ready-to-use web UI ships with the project. After running the server, just open:

    http://127.0.0.1:8000/

You get a dashboard to moderate text and images, with live results, a confidence
meter, raw JSON view, and a recent-checks history. It calls the same API endpoints,
served from the same origin (so there are no CORS issues).

## Endpoints

| Method | URL                       | Purpose                          |
|--------|---------------------------|----------------------------------|
| POST   | `/api/moderate/text/`     | Moderate a text message          |
| POST   | `/api/moderate/image/`    | Moderate an image by URL         |
| GET    | `/swagger/`               | Interactive Swagger UI           |
| GET    | `/redoc/`                 | ReDoc documentation              |
| GET    | `/`                       | Web console (frontend UI)        |
| GET    | `/admin/`                 | Django admin (view moderation logs) |

## How to run (terminal)

```bash
# 1. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. (optional) create an admin user to browse logs at /admin/
python manage.py createsuperuser

# 5. Start the development server
python manage.py runserver
```

The API is then available at http://127.0.0.1:8000/

## Example requests

```bash
# Clean text (not flagged)
curl -X POST http://127.0.0.1:8000/api/moderate/text/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "u123", "text": "Hello, have a great day!"}'

# Toxic text (flagged)
curl -X POST http://127.0.0.1:8000/api/moderate/text/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "u123", "text": "I will attack you with hate"}'

# Image by URL (flagged if url contains "nsfw" or "weapon")
curl -X POST http://127.0.0.1:8000/api/moderate/image/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "u999", "image_url": "https://example.com/nsfw.jpg"}'
```

## Notes

- The moderation logic in `moderator/utils.py` is a keyword-based simulation.
  Swap those functions for a real model/API call (e.g. an LLM or a vision
  service) when you are ready to go to production.
- `DEBUG = True` and a placeholder `SECRET_KEY` are set in `core/settings.py`
  for local development only. Change both before deploying.
