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


@app.route('/api/v1/send-email-notification', methods=['POST'])
def send_email_notification():
    for data in request.get_json():
        message = EmailMessage()
        message["Subject"] = "У вас новое задание"
        message["From"] = "Task Management System"
        message["To"] = data['receiverEmail']

        title = data['taskTitle']
        creatorName = data['creatorName']
        dueDate = datetime.datetime.fromisoformat(data['taskDueDate']).strftime('%X %d %b, %Y')

        html = f"""\
        <html>
          <body>
            <h3>Здравствуйте, вам было назначено новое задание: {title} от {creatorName} сроком до {dueDate}</h3>
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
