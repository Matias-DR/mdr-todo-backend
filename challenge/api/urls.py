from .views import (
    TaskViewSet,
    UserViewSet
)
from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()

router.register(r'task', TaskViewSet, basename='task')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path(
        '',
        include(router.urls)
    ),
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
