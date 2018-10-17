from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render

def index(request): 
    return  render(request, 'index_fo.html')
# Create your views here.
