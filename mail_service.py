# coding=utf-8

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yaml

PATH_SETTINGS_VAR = "settings.yaml"


def send_mail(subject, body, receiver_mail, filename):
    settings = yaml.safe_load(open(PATH_SETTINGS_VAR))

    port = settings["email"]["port"]
    smtp_server = settings["email"]["smtp_server"]
    sender_email = settings["email"]["sender_email"]
    password = settings["email"]["password"]

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_mail
    message.attach(MIMEText(body, "plain"))

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= yourfile.txt",
    )

    message.attach(part)
    text = message.as_string()

    server = smtplib.SMTP_SSL(smtp_server, port)
    server.ehlo()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_mail, text)
    server.quit()
