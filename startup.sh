#!/usr/bin/env bash
export PYTHONUNBUFFERED=1
alembic upgrade head
uvicorn main:app --workers $PULSE_WORKERS --host 0.0.0.0 --port 5000
