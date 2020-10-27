from django.contrib.auth.models import AbstractUser as BaseUser
from django.db.models import Model, UUIDField, DateTimeField, CharField, EmailField
from django.core.validators import MinLengthValidator
from uuid import uuid4


class Member(Model):
    id = UUIDField("ID", primary_key=True, editable=False, default=uuid4)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    first_name = CharField(max_length=150, validators=[MinLengthValidator(2)])
    last_name = CharField(max_length=150, validators=[MinLengthValidator(2)])
    email = EmailField("email address", unique=True, max_length=254)

    def name(self, redact: bool = False) -> str:
        last_name = self.last_name if not redact else f"{self.last_initial}."
        return f"{self.first_name} {last_name}"

    @property
    def last_initial(self) -> str:
        return self.last_name[0]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class User(BaseUser):
    id = UUIDField("ID", primary_key=True, editable=False, default=uuid4)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    email = EmailField("email address", unique=True, max_length=254)
