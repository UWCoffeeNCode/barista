from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView


def index(request):
    return redirect("./graphql")


graphql = csrf_exempt(GraphQLView.as_view(graphiql=True))