from django.urls import include, path
from rest_framework.routers import DefaultRouter

from hits import views

router = DefaultRouter()
router.register(r'hits', views.HitViewSet, basename='hits')

urlpatterns = [
    path('hits/<int:pk>/change-status/', views.HitViewSet.as_view({"put": "change_status"}, name='change_status')),
    path('', include(router.urls)),
]
