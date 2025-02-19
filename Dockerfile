FROM python:3.11

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD alembic upgrade head; uvicorn app.main:app --host 0.0.0.0 --reload