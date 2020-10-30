from __future__ import annotations
from secrets import token_hex
from typing import Dict, Union
from requests import post

from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from graphene import (
    Schema,
    GlobalID,
    ObjectType,
    Field,
    ResolveInfo,
    String,
    Boolean,
)
from graphene.relay import ClientIDMutation
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField as ConnectionField

from .slack import post_message as slack
from .models import User as UserModel
from .schema_node import Node, NodeField


def authenticated_user(info: ResolveInfo) -> UserModel:
    return info.context.user


def is_authenticated(info: ResolveInfo, staff_only=False) -> bool:
    user = authenticated_user(info)
    if not user.is_authenticated:
        return False
    if staff_only:
        return user.is_staff
    return True


class User(DjangoObjectType):
    "A registered UW Coffee N' Code user."

    class Meta:
        model = UserModel
        exclude = (
            "password",
            "is_active",
            "is_superuser",
            "date_joined",
            "last_login",
        )
        interfaces = (Node,)
        filter_fields = ()

    username = String(
        description="A unique username that acts as a handle for the user.",
    )
    email = String()

    name = String()
    last_name = String()
    last_initial = String()

    @staticmethod
    def resolve_name(user: UserModel, info: ResolveInfo):
        return user.name(redact=not is_authenticated(info, staff_only=True))

    @staticmethod
    def resolve_last_name(user: UserModel, info: ResolveInfo):
        if not is_authenticated(info):
            return None
        return user.last_name

    @staticmethod
    def resolve_last_initial(user: UserModel, info: ResolveInfo):
        return user.last_initial

    @staticmethod
    def resolve_username(user: UserModel, info: ResolveInfo):
        if not user.is_verified:
            return None
        return user.username

    @staticmethod
    def resolve_email(user: UserModel, info: ResolveInfo):
        if not is_authenticated(info, staff_only=True):
            return None
        return user.email


class Login(ClientIDMutation):
    class Input:
        username = String(required=True)
        password = String(required=True)

    user = Field(User, required=True)

    @staticmethod
    def mutate_and_get_payload(root, info: ResolveInfo, username: str, password: str):
        request: HttpRequest = info.context
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user is not None:
            login(request, user)
        else:
            raise Exception("User not found.")
        return Login(user=user)


class Logout(ClientIDMutation):
    @staticmethod
    def mutate_and_get_payload(root, info: ResolveInfo):
        request: HttpRequest = info.context
        logout(request)
        return Logout()


class Signup(ClientIDMutation):
    class Input:
        token = String(required=True)
        email = String(required=True)
        first_name = String(required=True)
        last_name = String(required=True)
        subscribe = Boolean()

    user = Field(User, required=True)

    @staticmethod
    def mutate_and_get_payload(
        root,
        info: ResolveInfo,
        token: str,
        email: str,
        first_name: str,
        last_name: str,
        subscribe: Union[bool, None],
    ):
        # Ensure ReCaptcha secret is available.
        secret = settings.RECAPTCHA_SECRET
        if not secret:
            raise Exception("Missing RECAPTCHA_SECRET.")

        # Verify ReCaptcha.
        captcha: Dict = post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": secret,
                "response": token,
            },
        ).json()
        if not captcha.get("success"):
            return Exception("Failed captcha.")

        # Generate a random, temporary username.
        temp = token_hex(12)

        # Create a new user and persist to DB.
        user = UserModel.objects.create_user(
            username=temp,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_subscribed=subscribe or False,
        )
        user.save()

        # Notify Slack.
        message = (
            f"*{first_name} {last_name}* ({email}) has joined UW Coffee 'N "
            "Code!  :tada:"
        )
        if user.is_subscribed:
            message += (
                "\n"
                f"@here We should add {email} to the newsletter mailing list. "
                " :email:"
            )
        slack(channel=settings.SLACK_CHANNEL, text=message)

        return Signup(user=user)


class Query(ObjectType):
    node = NodeField(description="Get a node by its ID.")
    viewer = Field(User, description="Get the currently authenticated user.")

    user = Field(
        User,
        description="Get a user by their ID.",
        args={
            "id": String(
                required=True,
                description="The ID of the user.",
            ),
        },
    )
    user_by_email = Field(
        User,
        description="Get a user by their email address.",
        args={
            "email": String(
                required=True,
                description="The email address of the user.",
            ),
        },
    )
    users = ConnectionField(
        User,
        description="Look up users.",
    )

    @staticmethod
    def resolve_viewer(root: Query, info: ResolveInfo):
        user = authenticated_user(info)
        return user if user.is_authenticated else None

    @staticmethod
    def resolve_user(root: Query, info: ResolveInfo, id: GlobalID):
        user: UserModel = Node.get_node_from_global_id(info, id, only_type=User)
        if not user:
            return None
        if not user.is_active:
            return None
        return user

    @staticmethod
    def resolve_user_by_email(root: Query, info: ResolveInfo, email: str):
        user: UserModel = UserModel.objects.get(email=email)
        if not user:
            return None
        if not user.is_active:
            return None
        return user


class Mutation(ObjectType):
    login = Login.Field(description="Begin an authenticated session.")
    logout = Logout.Field(description="Clear current authenticated session.")
    signup = Signup.Field(description="Create a new user.")


schema = Schema(query=Query, mutation=Mutation)
