from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ResetPasswordView, TaskViewSet, UserViewSet

router = DefaultRouter()

router.register(r"task", TaskViewSet, basename="task")
router.register(r"user", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("reset-password/<b64pk>/<token>", ResetPasswordView.as_view(), name="reset_password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]
