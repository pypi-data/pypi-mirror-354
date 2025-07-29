"""Django authentication backend for creating initial superuser."""

import warnings
from typing import Any, Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest


class CreateInitialSuperUserBackend(ModelBackend):
    """
    Authentication backend that creates a superuser on first login attempt
    if no superusers exist in the database.

    This backend is designed to simplify the initial setup of Django projects
    by automatically creating a superuser account when no superusers exist.

    Security Note:
        This backend should typically only be used in development environments.
        Consider disabling it in production by only adding it to
        AUTHENTICATION_BACKENDS when DEBUG=True.
    """

    def authenticate(
        self,
        request: Optional[HttpRequest],
        username: Optional[str] = "",
        password: Optional[str] = "",
        **kwargs: Any,
    ) -> Optional[User]:
        """
        Authenticate user and create initial superuser if needed.

        Args:
            request: The HTTP request object
            username: Username
            password: Password
            **kwargs: Additional keyword arguments

        Returns:
            User object if authentication successful, None otherwise
        """

        if not username or not password:
            return None

        UserModel = get_user_model()

        # Check if we should create an initial superuser
        if settings.DEBUG and not UserModel.objects.filter(is_superuser=True).exists():
            return self._create_initial_superuser(UserModel, username, password)
        else:
            # Fallback to the default ModelBackend authentication
            return super().authenticate(
                request, username=username, password=password, **kwargs
            )

    def _create_initial_superuser(
        self, UserModel: type, username: str, password: str
    ) -> AbstractUser:
        """
        Create the initial superuser account.

        Args:
            UserModel: The user model class
            username: Username for the new superuser
            password: Password for the new superuser

        Returns:
            The created user object
        """
        warnings.warn(
            f"django-create-initial-user: No superusers exist! "
            f"Creating initial superuser with username '{username}'",
            UserWarning,
            stacklevel=3,
        )

        hashed_password = make_password(password)
        user = UserModel.objects.create(
            username=username,
            password=hashed_password,
            is_staff=True,
            is_superuser=True,
        )

        # Set email if the username looks like an email
        if "@" in username and hasattr(user, "email"):
            user.email = username
            user.save(update_fields=["email"])

        return user
