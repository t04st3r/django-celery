from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import PublicHoliday
from .tasks import send_public_holiday_email_task


@receiver(pre_save, sender=PublicHoliday)
def order_pre_save(sender, instance, **kwargs):
    created = instance.pk is None
    send_public_holiday_email_task.delay(instance, created)
