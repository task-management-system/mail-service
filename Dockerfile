FROM python:3

RUN mkdir /app

WORKDIR /app

COPY . /app/

RUN pip install -r /app/resources/requirements.txt

EXPOSE 7200

ENTRYPOINT ['python']

CMD ['src/application.py']
