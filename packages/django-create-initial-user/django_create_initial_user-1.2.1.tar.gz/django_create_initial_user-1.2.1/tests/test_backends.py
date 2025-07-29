"""Tests for CreateInitialSuperUserBackend."""

import warnings
from unittest.mock import patch

from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase, override_settings

from create_initial_superuser.backends import CreateInitialSuperUserBackend


class CreateInitialSuperUserBackendTests(TestCase):
    """Test cases for CreateInitialSuperUserBackend."""

    def setUp(self):
        """Set up test fixtures."""
        self.User = get_user_model()
        self.backend = CreateInitialSuperUserBackend()
        self.test_username = "testuser"
        self.test_password = "testpassword123"
        self.test_email = "test@example.com"

    def test_authenticate_with_existing_superuser(self):
        """Test authentication when superuser already exists."""
        # Create an existing superuser
        existing_superuser = self.User.objects.create_user(
            username="admin", password="adminpass", is_superuser=True, is_staff=True
        )

        # Create a regular user for testing
        regular_user = self.User.objects.create_user(
            username=self.test_username, password=self.test_password
        )

        # Authenticate should use normal Django authentication
        authenticated_user = authenticate(
            username=self.test_username,
            password=self.test_password,
            backend="create_initial_superuser.backends.CreateInitialSuperUserBackend",
        )

        self.assertEqual(authenticated_user, regular_user)
        self.assertFalse(authenticated_user.is_superuser)

    @override_settings(DEBUG=True)
    def test_authenticate_creates_initial_superuser_when_none_exist(self):
        """Test that initial superuser is created when none exist."""
        # Ensure no superusers exist
        self.assertFalse(self.User.objects.filter(is_superuser=True).exists())

        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter("always")

            # Authenticate should create a new superuser
            authenticated_user = authenticate(
                username=self.test_username,
                password=self.test_password,
                backend="create_initial_superuser.backends.CreateInitialSuperUserBackend",
            )

        # Check that user was created and is a superuser
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.username, self.test_username)
        self.assertTrue(authenticated_user.is_superuser)
        self.assertTrue(authenticated_user.is_staff)
        self.assertTrue(authenticated_user.check_password(self.test_password))

        # Check that warning was issued
        self.assertEqual(len(warning_list), 1)
        self.assertIn("No superusers exist", str(warning_list[0].message))
        self.assertIn(self.test_username, str(warning_list[0].message))

    @override_settings(DEBUG=True)
    def test_authenticate_creates_superuser_with_email_username(self):
        """Test that superuser is created with email when username looks like email."""
        email_username = self.test_email

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")

            authenticated_user = authenticate(
                username=email_username,
                password=self.test_password,
                backend="create_initial_superuser.backends.CreateInitialSuperUserBackend",
            )

        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.username, email_username)
        self.assertEqual(authenticated_user.email, email_username)
        self.assertTrue(authenticated_user.is_superuser)
        self.assertTrue(authenticated_user.is_staff)

    @override_settings(DEBUG=False)
    def test_authenticate_does_not_create_superuser_when_debug_false(self):
        """Test that superuser is not created when DEBUG=False."""
        # Ensure no superusers exist
        self.assertFalse(self.User.objects.filter(is_superuser=True).exists())

        # Authenticate should not create a superuser when DEBUG=False
        authenticated_user = authenticate(
            username=self.test_username,
            password=self.test_password,
            backend="create_initial_superuser.backends.CreateInitialSuperUserBackend",
        )

        self.assertIsNone(authenticated_user)
        # Verify no superuser was created
        self.assertFalse(self.User.objects.filter(is_superuser=True).exists())

    def test_authenticate_invalid_credentials(self):
        """Test authentication with invalid credentials."""
        # Create a user
        self.User.objects.create_user(
            username=self.test_username, password=self.test_password
        )

        # Try to authenticate with wrong password
        authenticated_user = authenticate(
            username=self.test_username,
            password="wrongpassword",
            backend="create_initial_superuser.backends.CreateInitialSuperUserBackend",
        )

        self.assertIsNone(authenticated_user)

    def test_authenticate_empty_credentials(self):
        """Test authentication with empty credentials."""
        # Test with empty username
        user = authenticate(
            username="",
            password=self.test_password,
            backend="create_initial_superuser.backends.CreateInitialSuperUserBackend",
        )
        self.assertIsNone(user)

        # Test with empty password
        user = authenticate(
            username=self.test_username,
            password="",
            backend="create_initial_superuser.backends.CreateInitialSuperUserBackend",
        )
        self.assertIsNone(user)

        # Test with both empty
        user = authenticate(
            username="",
            password="",
            backend="create_initial_superuser.backends.CreateInitialSuperUserBackend",
        )
        self.assertIsNone(user)

    def test_authenticate_none_credentials(self):
        """Test authentication with None credentials."""
        # Test with None username
        user = authenticate(
            username=None,
            password=self.test_password,
            backend="create_initial_superuser.backends.CreateInitialSuperUserBackend",
        )
        self.assertIsNone(user)

        # Test with None password
        user = authenticate(
            username=self.test_username,
            password=None,
            backend="create_initial_superuser.backends.CreateInitialSuperUserBackend",
        )
        self.assertIsNone(user)

    def test_get_user_valid_id(self):
        """Test get_user with valid user ID."""
        user = self.User.objects.create_user(
            username=self.test_username, password=self.test_password
        )

        retrieved_user = self.backend.get_user(user.id)
        self.assertEqual(retrieved_user, user)

    def test_get_user_invalid_id(self):
        """Test get_user with invalid user ID."""
        retrieved_user = self.backend.get_user(999999)
        self.assertIsNone(retrieved_user)

    def test_get_user_none_id(self):
        """Test get_user with None as ID."""
        retrieved_user = self.backend.get_user(None)
        self.assertIsNone(retrieved_user)

    @override_settings(DEBUG=True)
    def test_create_initial_superuser_method(self):
        """Test the _create_initial_superuser method directly."""
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter("always")

            user = self.backend._create_initial_superuser(
                self.User, self.test_username, self.test_password
            )

        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.test_username)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password(self.test_password))

        # Verify user exists in database
        db_user = self.User.objects.get(username=self.test_username)
        self.assertEqual(db_user, user)

        # Check warning was issued
        self.assertEqual(len(warning_list), 1)
        self.assertIn("No superusers exist", str(warning_list[0].message))

    @override_settings(DEBUG=True)
    def test_create_initial_superuser_with_email_in_username(self):
        """Test _create_initial_superuser with email-like username."""
        email_username = self.test_email

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")

            user = self.backend._create_initial_superuser(
                self.User, email_username, self.test_password
            )

        self.assertEqual(user.username, email_username)
        self.assertEqual(user.email, email_username)

    @patch("create_initial_superuser.backends.get_user_model")
    def test_authenticate_with_custom_user_model(self, mock_get_user_model):
        """Test authentication works with custom user model."""
        mock_get_user_model.return_value = self.User

        # Create a superuser to avoid initial creation
        self.User.objects.create_user(
            username="admin", password="adminpass", is_superuser=True
        )

        # Create regular user
        user = self.User.objects.create_user(
            username=self.test_username, password=self.test_password
        )

        authenticated_user = authenticate(
            username=self.test_username,
            password=self.test_password,
            backend="create_initial_superuser.backends.CreateInitialSuperUserBackend",
        )

        self.assertEqual(authenticated_user, user)
        mock_get_user_model.assert_called()

    @override_settings(DEBUG=True)
    def test_multiple_authentication_attempts_only_create_one_superuser(self):
        """Test that multiple auth attempts don't create multiple superusers."""
        # First authentication should create superuser
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")

            user1 = authenticate(
                username=self.test_username,
                password=self.test_password,
                backend="create_initial_superuser.backends.CreateInitialSuperUserBackend",
            )

        # Second authentication should not create another superuser
        user2 = authenticate(
            username="anotheruser",
            password="anotherpass",
            backend="create_initial_superuser.backends.CreateInitialSuperUserBackend",
        )

        # Only one superuser should exist
        superusers = self.User.objects.filter(is_superuser=True)
        self.assertEqual(superusers.count(), 1)
        self.assertEqual(superusers.first(), user1)

        # Second authentication should fail (no matching user)
        self.assertIsNone(user2)
