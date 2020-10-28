from django.contrib.auth.models import AbstractUser as BaseUser
from django.db.models import (
    UUIDField,
    DateTimeField,
    CharField,
    EmailField,
    BooleanField,
)
from django.core.validators import MinLengthValidator
from uuid import uuid4


class User(BaseUser):
    "A member of the UW Coffee N' Code community."

    first_name_validator = MinLengthValidator(2)
    last_name_validator = MinLengthValidator(2)

    id = UUIDField("ID", primary_key=True, editable=False, default=uuid4)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    email = EmailField("email address", unique=True, max_length=254)
    is_verified = BooleanField(
        default=False,
        help_text=(
            "Designates that this user has verified their email address and set "
            "a password."
        ),
    )

    first_name = CharField(
        "first name",
        max_length=150,
        validators=[first_name_validator],
    )

    last_name = CharField(
        "last name",
        max_length=150,
        validators=[last_name_validator],
    )

    @property
    def last_initial(self) -> str:
        return self.last_name[0]

    def get_name(self, redact: bool = False) -> str:
        last_name = self.last_name if not redact else f"{self.last_initial}."
        return f"{self.first_name} {last_name}"
