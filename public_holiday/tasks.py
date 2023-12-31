from django.core.mail import send_mail
from celery import shared_task


@shared_task()
def send_public_holiday_email_task(public_holiday, created=True):
    """Sends an email when the public_holiday model has been created/updated"""
    send_mail(
        f"Public holiday {public_holiday['name']} "
        + f"has been {'created' if created else 'updated'}",
        str(public_holiday),
        "support@example.com",
        ["recipient@example.com"],
        fail_silently=False,
    )
