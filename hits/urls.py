from django.urls import include, path
from rest_framework.routers import DefaultRouter

from hits import views

router = DefaultRouter()
router.register(r'hits', views.HitViewSet, basename='hits')

urlpatterns = [
    path('', include(router.urls))
]
