FROM python:3.11-bookworm

RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt update
EXPOSE 80
COPY . .
WORKDIR /app/src

CMD alembic --config ./alembic/alembic.ini upgrade head && uvicorn main:app --host 0.0.0.0 --port 80 --reload
