FROM python:3.10.12 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app


RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install -r requirements.txt
FROM python:3.10.12-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .

RUN pip install "fastapi[standard]"

CMD ["/app/.venv/bin/fastapi", "run"]
