from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_html_email(data, template_name, context):
    """
    data: dict có keys 'email_subject', 'to_email'
    template_name: đường dẫn đến file HTML template (ví dụ 'mail/normal_email.html')
    context: dict truyền vào template
    """
    subject = data['email_subject']
    from_email = f"{settings.EMAIL_SENDER_NAME} <{settings.EMAIL_HOST_USER}>"
    to = [data['to_email']]

    # 1. Render HTML với CSS inline (hoặc link style)
    html_content = render_to_string(template_name, context)

    # 2. Tạo bản text thuần (dự phòng) từ HTML
    text_content = strip_tags(html_content)

    # 3. Khởi tạo EmailMultiAlternatives
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)

    # 4. Đính kèm HTML vào email (chỉ định content_type)
    msg.attach_alternative(html_content, "text/html")

    # 5. Gửi mail
    msg.send()
