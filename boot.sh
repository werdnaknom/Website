#!/bin/bash
exec gunicorn -b :8000 --access-logfile - --error-logfile - flaskweb:app
