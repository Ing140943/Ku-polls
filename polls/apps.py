"""This module is about configure the polls."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """PollsConfig class config the polls by specific field."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
