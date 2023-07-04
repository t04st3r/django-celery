from django.db.models.signals import post_save
from django.utils import timezone
from unittest.mock import patch

from public_holiday.models import PublicHoliday
from public_holiday.serializers import PublicholidaySerializer


@patch("public_holiday.signals.send_public_holiday_email_task.delay")
def test_public_holiday_post_save_signal(mock_delay):
    # Create a sample PublicHoliday instance
    public_holiday = PublicHoliday(
        name="Test Holiday",
        local_name="Test Holiday",
        date=timezone.now().date(),
        country="IT",
    )

    # Trigger the post_save signal manually
    post_save.send(sender=PublicHoliday, instance=public_holiday, created=True)

    # Verify that the delay function was called with the correct arguments
    mock_delay.assert_called_once_with(
        PublicholidaySerializer(instance=public_holiday).data, True
    )
