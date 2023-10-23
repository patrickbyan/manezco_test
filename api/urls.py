from django.urls import path
from .content import views as contentViews
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def intro(req):
    return Response("Manezco Test API Framework")

urlpatterns = [
    path('', intro),
    path('api/questions/', contentViews.fetchQuestions),
    path('api/answer/check', contentViews.fetchCorrectAnswer),
]