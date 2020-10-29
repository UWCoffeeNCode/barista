from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from slack_bolt.adapter.django import SlackRequestHandler
from graphene_django.views import GraphQLView

from .slack import ROBOT


def index(request: HttpRequest):
    return redirect("./graphql")


def healthz(request: HttpRequest):
    return HttpResponse("ok")


graphql = csrf_exempt(GraphQLView.as_view(graphiql=True))

__slack_handler = SlackRequestHandler(app=ROBOT)


@csrf_exempt
def slack(request: HttpRequest):
    return __slack_handler.handle(request)
