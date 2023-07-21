FROM python:3.11-bookworm
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN apt update

EXPOSE 80

COPY . .

ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]