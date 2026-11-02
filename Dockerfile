FROM python:3.14-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY trabalho-pos-graduacao-fase-2/src ./src

CMD ["python", "-m", "src.main"]
