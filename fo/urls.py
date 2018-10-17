from django.urls import path,include

from . import views

from .routers import router

from django.views.generic import TemplateView

app_name = 'fo'
urlpatterns = [
    #path('', views.index, name='index'),
    path('',TemplateView.as_view(template_name='index_fo.html')),
    path('api/', include(router.urls))
]