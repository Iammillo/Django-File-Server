from django.urls import path
from . import views


urlpatterns = [
                path('',views.index),
                path('upload/',views.upload),
                path('delete/',views.delete),
                path('search/',views.search),
                path('register/',views.register),
                path('validate/',views.validate),
                ]
