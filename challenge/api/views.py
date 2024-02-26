import logging

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django_filters.rest_framework import DjangoFilterBackend
from dotenv import load_dotenv
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from challenge.settings import (
    FRONT_HOST,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    DEFAULT_FROM_EMAIL,
)

from .filters import TaskFilter
from .models import Task, User
from .serializers import TaskSerializer, UserSerializer
from .utils import password_reset_token_generator

logger = logging.getLogger(__name__)
load_dotenv()


class UserViewSet(ModelViewSet):
    """
    ViewSet for User model. It allows to create, retrieve, update and delete the user.
    The user can only update and delete himself when is authenticated.

    Atributes:
        queryset (QuerySet): QuerySet of the User model.
        serializer_class (rest_framework.serializers.ModelSerializer): Serializer of the User model.
        action_permissions (dict): Dictionary that contains the permissions for each action.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    action_permissions = {
        "retrieve": [IsAuthenticated],
        "list": [IsAuthenticated],
        "destroy": [IsAuthenticated],
        "update": [IsAuthenticated],
    }

    def get_queryset(self):
        """
        Returns the user's queryset if authenticated and never that of all users.
        Only superusers can get the queryset of all users.
        """

        if not self.request.user.is_superuser:
            return self.queryset.filter(pk=self.request.user.pk)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        """
        Adapt data before creates the user.
        Compares the password whit de password confirmation and executes
        the super create method.
        """

        logger.info(f'UserViewSet create -> User {request.data["username"]}.')
        adapted_data = {
            "username": request.data["username"]
            if "username" in request.data
            else request.data["userName"]
            if "userName" in request.data
            else request.data["user_name"],
            "password": request.data["password"],
            "password_confirmation": request.data["password_confirmation"]
            if "password_confirmation" in request.data
            else request.data["passwordConfirmation"],
        }
        request.data.update(adapted_data)
        if request.data["password"] != request.data["password_confirmation"]:
            return Response(
                {"password": "Las contraseñas no coinciden."}, HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Adapt data before updates the user.
        Update the user's data by identifying a new email and password.

        si hay nueva contrsaseña -> compararla con su confirmación
        """

        logger.info(f'UserViewSet update -> {request.data["username"]}.')
        adapted_data = {
            "email": request.data.get("email")
            or request.data.get("new_email")
            or request.data.get("newEmail"),
            "password": request.data.get("new_password")
            or request.data.get("newPassword"),
        }
        password = request.data.get("current_password") or request.data.get(
            "currentPassword"
        )
        password_confirmation = request.data.get(
            "new_password_confirmation"
        ) or request.data.get("newPasswordConfirmation")

        # If the new password is the same as the new password confirmation
        if adapted_data.get("password") == password_confirmation:
            current_user = self.queryset.filter(email=adapted_data.get("email")).first()

            # If password is the same as the current password
            if current_user.check_password(password):
                request.data.update(adapted_data)
                return super().update(request, *args, **kwargs)
            else:
                return Response(
                    {"password": "Contraseña incorrecta"}, HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"password": "Las contraseñas no coinciden."}, HTTP_400_BAD_REQUEST
            )


class TaskViewSet(ModelViewSet):
    """
    ViewSet for Task model. It allows to create, retrieve, update and delete the task.
    Only authenticated users can execute all actions on tasks.

    Atributes:
        queryset (QuerySet): QuerySet of the Task model.
        serializer_class (rest_framework.serializers.ModelSerializer): Serializer of the Task model.
        action_permissions (dict): Dictionary that contains the permissions for each action.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["description", "title"]
    filterset_class = TaskFilter
    ordering_fields = ["created"]

    def get_queryset(self):
        """
        Returns the task's queryset if authenticated and never that of all tasks.
        Only superusers can get the queryset of all task.
        """

        if not self.request.user.is_superuser:
            return self.queryset.filter(user=self.request.user.pk)
        return super().get_queryset()

    def perform_create(self, serializer) -> None:
        """
        Sets the user of the task to the user who created it.
        """

        logger.info(
            f"TaskViewSet perform_create -> Task created by {self.request.user.username}"
        )
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["put", "patch"])
    def complete(self, request, pk=None) -> Response:
        """
        Allows to mark a task as complete.
        It receive the task id, marks as complete and returns the task data.
        """

        logger.info(
            f"TaskViewSet complete -> Task {pk} from user {self.request.user.username} completed"
        )
        task = self.get_object()
        serializer = self.get_serializer(task)
        task.complete()
        return Response(serializer.data, 200)

    @action(detail=True, methods=["put", "patch"])
    def incomplete(self, request, pk=None) -> Response:
        """
        Allows to mark a task as incomplete.
        It receive the task id, marks as complete and returns the task data.
        """

        logger.info(
            f"TaskViewSet incomplete -> Task {pk} from user {self.request.user.username} incomplete"
        )
        task = self.get_object()
        serializer = self.get_serializer(task)
        task.incomplete()
        return Response(serializer.data, 200)


class ResetPasswordView(APIView):
    """
    View for reset password. It allows to send an email to the user with the reset
    password link.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request: dict, b64pk: bytes | str, token: str) -> Response:
        """
        Verifies that the token is valid and has not been used.
        """
        try:
            pk = force_str(urlsafe_base64_decode(b64pk))
            user = User.objects.get(pk=pk)
            if not password_reset_token_generator.check_token(user, token):
                # User has already used the token.
                return Response(
                    status=HTTP_400_BAD_REQUEST,
                    data={"detail": "El enlace expiró o ya se utilizó."},
                )
        except User.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        logger.info(f"ResetPasswordView get -> Token for {user.username} is valid.")
        return Response(status=HTTP_200_OK)

    def post(self, request: dict) -> Response:
        """
        Sends an email with the reset password link to the email address provided.
        """

        email = request.data.get("email")
        try:
            validate_email(email)
        except Exception:
            return Response(status=HTTP_400_BAD_REQUEST, data="Email inválido")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={"detail": "Email inexistente."},
            )

        b64pk = urlsafe_base64_encode(force_bytes(user.pk))
        token = password_reset_token_generator.make_token(user)
        link = f"{FRONT_HOST}/reset-password/{b64pk}/{token}"
        subject = "Restablezca su contraseña de ToDo"
        body = (
            f"Esto es un email para la recuperación de su contraseña.\n"
            f"Para restablecerla, ingrese en el siguiente enlace:\n"
            f"{link}\n\n"
            f"Saludos\nToDo"
        )

        send_mail(
            subject,
            body,
            recipient_list=[user.email],
            from_email=DEFAULT_FROM_EMAIL,
            auth_user=EMAIL_HOST_USER,
            auth_password=EMAIL_HOST_PASSWORD,
        )

        # email = EmailMessage(
        #     subject,
        #     body,
        #     to=[user.email],
        # )
        # email.send()

        logger.info(f"ResetPasswordView post -> Email {email} sent.")
        return Response(status=HTTP_204_NO_CONTENT)

    def patch(self, request, b64pk: bytes | str, token: str) -> Response:
        """
        Verifies that the token is valid and has not been used.
        If the token is valid, it updates the user's password.
        """

        try:
            pk = force_str(urlsafe_base64_decode(b64pk))
            user = User.objects.get(pk=pk)
            if not password_reset_token_generator.check_token(user, token):
                # User has already used the token.
                return Response(
                    status=HTTP_400_BAD_REQUEST,
                    data={"detail": "El enlace expiró o ya se utilizó."},
                )
            else:
                new_password = (
                    request.data.get("new_password") or request.data.get("newPassword")
                )
                new_password_confirmation = (
                    request.data.get("new_password_confirmation")
                    or request.data.get("newPasswordConfirmation")
                )
                if new_password != new_password_confirmation:
                    return Response(
                        status=HTTP_400_BAD_REQUEST,
                        data={"detail": "Las contraseñas no coinciden."},
                    )
                new_password = make_password(new_password)
                user.set_password(new_password)
                user.save()
        except User.DoesNotExist:
            return Response(
                status=HTTP_404_NOT_FOUND, data={"detail": "Usuario inexistente."}
            )

        logger.info(
            f"ResetPasswordView patch -> Password for {user.username} has reset."
        )
        return Response(status=HTTP_204_NO_CONTENT)
