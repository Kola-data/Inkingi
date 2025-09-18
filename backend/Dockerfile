FROM python:3.11-slim

WORKDIR /app

COPY app /app/app
COPY pyproject.toml /app/

RUN pip install --upgrade pip setuptools wheel \
    && pip install -e .

ENV PORT=8000
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 