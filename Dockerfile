# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13.1
FROM python:${PYTHON_VERSION}-slim AS base

ARG WORK_DIR=/app
WORKDIR ${WORK_DIR}

COPY requirements.txt ${WORK_DIR}
RUN pip install --no-cache-dir -r requirements.txt

COPY . ${WORK_DIR}

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]