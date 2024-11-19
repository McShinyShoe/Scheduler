#!/bin/bash


if [ "$PRODUCTION" != "false" ]; then
    echo "Running as production"
    make .venv
    source .venv/bin/activate
    pip install flask
    python src/app.py
else 
    echo "Running as production"
    python src/app.py
fi
