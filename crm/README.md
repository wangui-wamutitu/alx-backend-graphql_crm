# CRM Celery Setup

This document explains how to set up and run Celery with Redis for the graphql CRM project.

---

## 1. Install Redis and Dependencies

### Install Redis

On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install redis-server -y
```

## Verify Redis is running:

```bash
redis-cli ping
# should return "PONG"
```

## 1.2. Install Python Dependencies

Make sure you have these in your virtual environment:

```bash
pip install celery redis gql
```

## 2. Run Migrations

Apply database migrations:

```bash
python manage.py migrate
```

## 3. Start Celery Worker

Run the Celery worker to process tasks:

```bash
celery -A crm worker -l info
```

## 4. Start Celery Beat

Run Celery Beat to schedule periodic tasks:

```bash
celery -A crm beat -l info
```

## 5. Verify Logs

The CRM report task will log output to:

/tmp/crm_report_log.txt

Check the file:

cat /tmp/crm_report_log.txt

You should see entries like:

2025-08-29 11:30:00 - Report: 10 customers, 25 orders, 12345.67 revenue

At this point, Celery + Redis + Celery Beat are working with our app.
