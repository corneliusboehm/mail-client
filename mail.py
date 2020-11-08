import smtplib
import ssl
import yaml
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from flask import Flask, request
from getpass import getpass


SETTINGS_FILE = 'settings.yaml'
SUBJECT = '[COVID-Dashboard] Contact Form'


# Start app
app = Flask(__name__)


def check_smtp_connection():
    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        # Connect to the server and confirm credentials
        server = smtplib.SMTP(settings['server'], settings['port'])
        server.starttls(context=context) # Secure the connection
        server.login(settings['login'], password)
        print('SMTP connection successful')
    except Exception as e:
        print(e)
    finally:
        server.quit()


# Load settings file
with open(SETTINGS_FILE, 'r') as f:
    settings = yaml.safe_load(f)


# Get password from user input
password = getpass(f'Password for {settings["login"]}: ')
check_smtp_connection()


@app.route('/mail', methods=['POST'])
def mail():
    # Receive a message via HTML form
    sender = request.form['sender']
    message_content = request.form['message']

    print(f'Received message from {sender}: {message_content}')

    send_mail(sender, message_content)

    return 'OK', 200


def send_mail(sender, message_content):
    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(settings['server'], settings['port'])
        server.starttls(context=context) # Secure the connection
        server.login(settings['login'], password)

        # Create email message and add headers (most of them are required to pass spam filters)
        message = EmailMessage()
        message.add_header('From', settings['fromaddr'])
        message.add_header('To', settings['toaddr'])
        message.add_header('Subject', SUBJECT)
        message.add_header('Date', formatdate())
        message.add_header('Message-ID', make_msgid())

        # Add optional Reply-To address
        if sender:
            message.add_header('Reply-To', sender)

        # Add message content
        message.set_content(message_content)

        # Send message
        server.send_message(message, from_addr=settings['fromaddr'], to_addrs=settings['toaddr'])

        print('Email sent successfully')

    except Exception as e:
        print(e)
    finally:
        server.quit()
