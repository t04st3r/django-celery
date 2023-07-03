from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PublicHoliday
from .tasks import send_public_holiday_email_task
from .serializers import PublicholidaySerializer


@receiver(post_save, sender=PublicHoliday)
def public_holiday_post_save(sender, instance, created, **kwargs):
    dict_model = PublicholidaySerializer(instance).data
    send_public_holiday_email_task.delay(dict_model, created)
