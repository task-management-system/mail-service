import datetime
import locale
import logging
import smtplib
import ssl
from email.message import EmailMessage

import flask
from decouple import config
from flask import request

# Flask Config
app = flask.Flask(__name__)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)

# SMTP Config
sender_email = config('TMS_MS_EMAIL')
sender_password = config('TMS_MS_PASSWORD')

context = ssl.create_default_context()

# Locale Config
locale.setlocale(locale.LC_TIME, "ru_RU")


@app.route('/api/v1/test')
def test():
    return ('Service is up', 200)


@app.route('/api/v1/notification/new-task', methods=['POST'])
def new_task():
    for data in request.get_json():
        message = EmailMessage()
        message["Subject"] = "У вас новое задание!"
        message["From"] = "Task Management System"
        message["To"] = data['receiverEmail']

        title = data['taskTitle']
        creatorName = data['creatorName']
        dueDate = datetime.datetime.fromisoformat(data['taskDueDate']).strftime('%X %d %b, %Y')

        html = f"""\
        <html>
          <body>
            <p>Здравствуйте, Вам было назначено новое задание.</p>
            <br>
            Наименование: {title}.
            <br>
            Отправитель: {creatorName}.
            <br>
            Cрок: {dueDate}.</p>
          </body>
        </html>
        """
        message.add_alternative(html, "html")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(message)

    return ('', 204)

@app.route('/api/v1/notification/close-task', methods=['POST'])
def close_task():
    data = request.get_json()
    message = EmailMessage()
    message["Subject"] = "Задание завершено!"
    message["From"] = "Task Management System"
    message["To"] = data['receiverEmail']

    title = data['taskTitle']
    executorNames = data['executorNames']
    executorPrefix = ''
    if (len(executorNames) > 1): 
        executorPrefix = 'Исполнители' 
    else:
        executorPrefix = 'Исполнитель'
    plainExecutorNames = ', '.join(data['executorNames'])
    createdDate = datetime.datetime.fromisoformat(data['taskCreatedDate']).strftime('%X %d %b, %Y')
    dueDate = datetime.datetime.fromisoformat(data['taskDueDate']).strftime('%X %d %b, %Y')

    html = f"""\
    <html>
      <body>
        <p>Здравствуйте, созданное Вами задание было завершено.</p>
        <br>
        Наименование: {title}.
        <br>
        {executorPrefix}: {plainExecutorNames}.
        <br>
        Начало - {createdDate}, конец - {dueDate}.</p>
      </body>
    </html>
    """
    message.add_alternative(html, "html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(message)

    return ('', 204)

    
@app.route('/api/v1/notification/delete-task', methods=['POST'])
def delete_task():
    for data in request.get_json():
        message = EmailMessage()
        message["Subject"] = "Задание было удалено!"
        message["From"] = "Task Management System"
        message["To"] = data['receiverEmail']

        title = data['taskTitle']
        creatorName = data['creatorName']

        html = f"""\
        <html>
          <body>
            <p>Здравствуйте, назначенное Вам задание было удалено.</p>
            <br>
            Наименование: {title}.
            <br>
            Отправитель: {creatorName}.
          </body>
        </html>
        """
        message.add_alternative(html, "html")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(message)

    return ('', 204)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=7200)
