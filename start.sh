#!/bin/bash

# Убедитесь, что зависимости установлены
pip install -r requirements.txt

# Запуск Uvicorn с указанием хоста и порта
uvicorn main:app --host 0.0.0.0 --port $PORT
