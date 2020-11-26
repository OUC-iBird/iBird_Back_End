import threading

from django.core.mail import send_mail

from iBird import settings


def send(target, message, html_message=None, title='iBird'):
    thread = threading.Thread(
        target=send_mail,
        args=(
            title,
            message,
            settings.EMAIL_FROM,
            [target],
        ),
        kwargs={
            'html_message': html_message
        }
    )
    thread.start()
