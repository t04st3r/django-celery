import pytest
import requests
import time

from django.conf import settings
from .factories import PublicHolidayFactory
from public_holiday.serializers import PublicholidaySerializer


def delete_mail_list():
    """Helper function to clean all the mail from maildev container"""
    url = f"http://{settings.EMAIL_HOST}:{settings.MAILDEV_REST_API_PORT}/email/all"

    try:
        response = requests.delete(url)
        return response.status_code == 200
    except Exception:
        return False


def get_mail_list():
    """Helper function to fetch sent mail list from maildev container"""
    url = f"http://{settings.EMAIL_HOST}:{settings.MAILDEV_REST_API_PORT}/email"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        results = response.json()
        return results
    except Exception:
        return None


@pytest.mark.django_db
def test_public_holiday_model_signal():
    # clean eventual mail sent previously
    clean = delete_mail_list()
    assert clean is True
    time.sleep(2)
    # create a model it will implicitly call save() and trigger the post_save signal
    model = PublicHolidayFactory()
    # let's wait some seconds for the email to be sent
    time.sleep(2)
    # Get the sent mail list
    mail_list = get_mail_list()
    # Assert model creation
    assert type(mail_list) == list
    assert len(mail_list) == 1
    sent_mail = mail_list[0]
    body = PublicholidaySerializer(model).data
    assert str(body) in sent_mail["text"]
    assert f"Public holiday {model.name} has been created" in sent_mail["subject"]
    assert sent_mail["from"][0]["address"] == "support@example.com"
    assert sent_mail["to"][0]["address"] == "recipient@example.com"
    # Clean again the sent mail list
    clean = delete_mail_list()
    time.sleep(2)
    assert clean is True
    # let's update the model and assert mail is sent again
    model.name = "Some junkie funky celebration"
    model.save()
    # let's wait some seconds for the email to be sent
    time.sleep(2)
    # Get the sent mail list
    mail_list = get_mail_list()
    # Assert model update
    assert type(mail_list) == list
    assert len(mail_list) == 1
    sent_mail = mail_list[0]
    body = PublicholidaySerializer(model).data
    assert str(body) in sent_mail["text"]
    assert f"Public holiday {model.name} has been updated" in sent_mail["subject"]
    assert sent_mail["from"][0]["address"] == "support@example.com"
    assert sent_mail["to"][0]["address"] == "recipient@example.com"
