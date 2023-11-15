from django.urls import path
from testme import views

urlpatterns = [
    path('bool/', views.bool),
    path('date/', views.date),
    path('decimal/', views.decimal),
    path('dtaware/', views.dtaware),
    path('integer/', views.integer),
    path('string/', views.string),
]
