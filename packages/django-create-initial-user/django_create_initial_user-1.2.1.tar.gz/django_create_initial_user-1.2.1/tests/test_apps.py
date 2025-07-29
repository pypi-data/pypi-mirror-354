"""Tests for the Django app configuration."""

from django.test import TestCase

from create_initial_superuser.apps import CreateInitialSuperuserConfig


class AppConfigTests(TestCase):
    """Test cases for the app configuration."""

    def test_app_config(self):
        """Test that the app config is properly configured."""
        config = CreateInitialSuperuserConfig

        self.assertEqual(config.name, "create_initial_superuser")
        self.assertEqual(config.verbose_name, "Create Initial Superuser")
        self.assertEqual(config.default_auto_field, "django.db.models.BigAutoField")

    def test_app_config_instantiation(self):
        """Test that the app config can be instantiated."""
        config = CreateInitialSuperuserConfig("create_initial_superuser", None)

        self.assertEqual(config.name, "create_initial_superuser")
        self.assertEqual(config.verbose_name, "Create Initial Superuser")
