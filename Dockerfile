FROM python:3.10.12 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app


RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install -r requirements.txt
RUN .venv/bin/pip install fastapi[standard]
FROM python:3.10.12-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .

EXPOSE 8000

CMD [".venv/bin/python", "main.py"]