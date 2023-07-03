from unittest.mock import patch
from public_holiday.tasks import send_public_holiday_email_task


@patch("public_holiday.tasks.send_mail")
def test_send_public_holiday_email_task(mock_send_mail):
    # Test when created=True
    public_holiday = {
        "name": "New Year",
        "date": "2023-01-01",
        "country": "USA",
    }
    send_public_holiday_email_task(public_holiday, created=True)

    mock_send_mail.assert_called_once_with(
        "Public holiday New Year has been created",
        str(public_holiday),
        "support@example.com",
        ["recipient@example.com"],
        fail_silently=False,
    )

    # Test when created=False
    send_public_holiday_email_task(public_holiday, created=False)

    mock_send_mail.assert_called_with(
        "Public holiday New Year has been updated",
        str(public_holiday),
        "support@example.com",
        ["recipient@example.com"],
        fail_silently=False,
    )
