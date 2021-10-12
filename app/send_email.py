import os
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME', ""),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD', ""),
    MAIL_FROM=os.getenv('MAIL_FROM', "linka@planeteers.org"),
    MAIL_PORT=os.getenv('MAIL_PORT', 25),
    MAIL_SERVER=os.getenv('MAIL_SERVER', "localhost"),
    MAIL_FROM_NAME=os.getenv('MAIL_FROM_NAME', "Linka"),
    MAIL_TLS=os.getenv('MAIL_TLS', False),
    MAIL_SSL=os.getenv('MAIL_SSL', False),
    USE_CREDENTIALS=os.getenv('USE_CREDENTIALS', False),
    TEMPLATE_FOLDER='app/templates/email'
)


async def send_email_async(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html',
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')


def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html',
    )
    fm = FastMail(conf)
    background_tasks.add_task(
       fm.send_message, message, template_name='email.html')

