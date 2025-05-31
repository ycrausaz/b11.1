import logging
import os
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger('b11_1')

def send_simple_email(subject, message, recipient_list, from_email=None, html_message=None):
    """
    Send a simple email using Django's send_mail function.
    
    Args:
        subject (str): Email subject
        message (str): Plain text email content
        recipient_list (list): List of recipient email addresses
        from_email (str, optional): Sender email address. Defaults to DEFAULT_FROM_EMAIL.
        html_message (str, optional): HTML content for the email.
    
    Returns:
        int: Number of successfully sent messages
    """
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL

    # Debug output
    print(f"DEBUG - EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"DEBUG - EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"DEBUG - EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEBUG - EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
    print(f"DEBUG - DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    try:
        sent = send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False
        )
        logger.info(f"Email sent to {', '.join(recipient_list)}")
        return sent
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        print(f"Full error details: {e}")
        return 0


def send_template_email(subject, template_name, context, recipient_list, from_email=None):
    """
    Send an email using a template.
    
    Args:
        subject (str): Email subject
        template_name (str): Name of the template without extension (will look for template_name.txt and template_name.html)
        context (dict): Context variables for the template
        recipient_list (list): List of recipient email addresses
        from_email (str, optional): Sender email address. Defaults to DEFAULT_FROM_EMAIL.
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL
    
    # Render text and HTML templates
    text_content = render_to_string(f'{template_name}.txt', context)
    html_content = render_to_string(f'{template_name}.html', context)
    
    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=recipient_list
        )
        msg.attach_alternative(html_content, "text/html")
        sent = msg.send()
        logger.info(f"Template email sent to {', '.join(recipient_list)}")
        return True
    except Exception as e:
        logger.error(f"Failed to send template email: {e}")
        return False
