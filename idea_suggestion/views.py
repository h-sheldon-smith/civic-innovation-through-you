from django.shortcuts import render
from django.http import HttpResponse

# Create your views here (http request/response)
def index (request):
    return HttpResponse("Idea Suggestion Placeholder")