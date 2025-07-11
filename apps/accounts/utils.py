from django.core.mail import EmailMessage
from django.conf import settings

def send_normal_email(data):
    from_email = f'{settings.EMAIL_SENDER_NAME} <{settings.EMAIL_HOST_USER}>'
    email = EmailMessage(
        subject = data['email_subject'],
        body = data['email_body'],
        from_email = from_email,
        to = [data['to_email']]
    )
    email.send()