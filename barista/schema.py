from __future__ import annotations
from typing import Dict

from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout

from graphene import (
    Schema,
    ObjectType,
    Field,
    ResolveInfo,
    String,
    ID,
)
from graphene.relay import ClientIDMutation
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField as ConnectionField

from .models import User as UserModel, Member as MemberModel
from .schema_node import Node, NodeField


def is_authenticated(info: ResolveInfo, staff_only=False) -> bool:
    user: UserModel = info.context.user
    if not user.is_authenticated:
        return False
    if staff_only:
        return user.is_staff
    return True


class User(DjangoObjectType):
    "A registered UW Coffee N' Code user."

    class Meta:
        model = UserModel
        fields = ("id",)
        interfaces = (Node,)
        filter_fields = ()


class Member(DjangoObjectType):
    "A member of the UW Coffee N' Code community."

    class Meta:
        model = MemberModel
        interfaces = (Node,)
        filter_fields = ()

    name = String(required=True)
    last_name = String()
    last_initial = String(required=True)
    email = String()

    @staticmethod
    def resolve_name(parent: MemberModel, info: ResolveInfo):
        return f"{parent.first_name} {parent.last_name}"

    @staticmethod
    def resolve_last_name(parent: MemberModel, info: ResolveInfo):
        if not is_authenticated(info):
            return None
        return parent.last_name

    @staticmethod
    def resolve_last_initial(parent: MemberModel, info: ResolveInfo):
        return parent.last_name[0]

    @staticmethod
    def resolve_email(parent: MemberModel, info: ResolveInfo):
        if not is_authenticated(info, staff_only=True):
            return None
        return parent.email


class Login(ClientIDMutation):
    class Input:
        username = ID(required=True)
        password = String(required=True)

    user = Field(User, required=True)

    @staticmethod
    def mutate_and_get_payload(root, info: ResolveInfo, **input: Dict):
        request: HttpRequest = info.context
        user = authenticate(
            request,
            username=input.get("username"),
            password=input.get("password"),
        )
        if user is not None:
            login(request, user)
        else:
            raise Exception("User not found.")
        return Login(user=user)


class Logout(ClientIDMutation):
    @staticmethod
    def mutate_and_get_payload(root, info: ResolveInfo, **input: Dict):
        request: HttpRequest = info.context
        logout(request)
        return Logout()


class Query(ObjectType):
    node = NodeField(description="Get a node by its ID.")
    member = NodeField(Member, description="Fetch a member by their ID.")
    members = ConnectionField(Member, description="Look up members.")


class Mutation(ObjectType):
    login = Login.Field(description="Begin an authenticated session.")
    logout = Logout.Field(description="Clear current authenticated session.")


schema = Schema(query=Query, mutation=Mutation)
