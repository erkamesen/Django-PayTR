FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "manage.py" ]

CMD [ "runserver", "0.0.0.0:8000" ]