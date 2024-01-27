from .views import (
    TaskViewSet,
    UserViewSet
)
from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'task', TaskViewSet, basename='task')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = router.urls
