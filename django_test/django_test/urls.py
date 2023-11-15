from django.urls import path
from testme import views

urlpatterns = [
    path('bool/', views.bool),
    path('date/', views.date),
    path('decimal/', views.decimal),
    path('dtaware/', views.dtaware),
    path('integer/', views.integer),
    path('list/bools/', views.list_of_bools),
    path('list/integers/', views.list_of_integers),
    path('list/strings/', views.list_of_strings),
    path('list/urls/', views.list_of_urls),
    path('string/', views.string),
    path('url/', views.url),
]
