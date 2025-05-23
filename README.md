# Roshan News Project

Roshan News is a Django-based web platform for managing and aggregating news, featuring background task processing, REST API support, and news scraping capabilities.

---

## Features

- **Django 5.2.1** web application (see `roshan_news/`)
- REST API with Django REST Framework
- Tag support via django-taggit
- Advanced filtering with django-filter
- Asynchronous task processing using Celery and Redis
- Periodic tasks with Celery Beat
- Monitoring with Flower
- Integrated web scraping pipeline (see `news_scraper/`)
- Dockerized for easy deployment

---

## Quick Start

### Prerequisites

- Docker & Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/hiddenSm/roshan_new_project.git
cd roshan_new_project
```

### 2. Build and run the stack

```bash
docker-compose up --build
```

- Web app: [http://localhost:8000/](http://localhost:8000/)
- Flower dashboard: [http://localhost:5555/](http://localhost:5555/)

### 3. Django management

Apply migrations and create an admin user:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## Project Structure

```
.
├── roshan_news/              # Main Django project (settings, URLs, etc.)
├── news/                     # Django app for news management
├── news_scraper/             # Web scraping pipeline (Scrapy)
│   └── news_scraper/spiders/ # Scrapy spiders
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Multi-service orchestration
```

---

## Configuration

- **Database**: SQLite by default (see `roshan_news/settings.py`)
- **Celery/Redis**: Preconfigured for Dockerized services
- **Static & Media Files**: Served from `/static/` and `/media/`
- **Allowed Hosts**: All (`*`) by default; change for production

---

## Dependencies

Main dependencies (see `requirements.txt`):

- Django, djangorestframework, django-taggit, django-filter, django-celery-beat
- Celery, redis, flower, gunicorn
- Scrapy, beautifulsoup4, lxml, etc.

---

## News Scraper

The `news_scraper/` directory contains a Scrapy-based pipeline for collecting news from external sources.

- Define spiders in `news_scraper/news_scraper/spiders/`
- Integrate scraped data with the Django backend as needed

---

## Environment Variables

- `CELERY_BROKER_URL=redis://redis:6379/0`
- `CELERY_RESULT_BACKEND=redis://redis:6379/0`
- Others can be added/overridden in `docker-compose.yml`

---

## License

MIT License

---

## Contributing

Feel free to open issues or pull requests to improve the project!
