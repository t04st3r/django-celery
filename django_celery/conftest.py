import pytest

from django.db.models.signals import post_save


@pytest.fixture(autouse=True)  # Automatically use in tests.
def mute_signals(_):
    post_save.receivers = []
