from django.urls import path
from testme import views

urlpatterns = [
    path('integer/', views.integer),
    path('string/', views.string),
    path('bool/', views.string),
    path('date/', views.string),
]
