from django.core.validators import validate_email
from django.db.models import Model, UUIDField, CharField
from uuid import uuid4


class Member(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = CharField(max_length=256)
    last_name = CharField(max_length=256)
    email = CharField(max_length=256, validators=[validate_email])
