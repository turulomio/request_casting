from django.urls import path, include
from testme import views
from rest_framework import routers

router = routers.DefaultRouter()
routers.DefaultRouter
router.register(r'records', views.RecordViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
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
