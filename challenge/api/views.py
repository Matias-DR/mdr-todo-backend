import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import (
    User,
    Task
)
from .serializers import (
    UserSerializer,
    TaskSerializer
)


logger = logging.getLogger(__name__)


class UserViewSet(ModelViewSet):
    '''
        ViewSet for User model. It allows to create, retrieve, update and delete the user.
        The user can only update and delete himself when is authenticated.

        Atributes:
            queryset (QuerySet): QuerySet of the User model.
            serializer_class (rest_framework.serializers.ModelSerializer): Serializer of the User model.
            action_permissions (dict): Dictionary that contains the permissions for each action.
    '''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    action_permissions = {
        'retrieve': [IsAuthenticated],
        'list': [IsAuthenticated],
        'destroy': [IsAuthenticated],
        'update': [IsAuthenticated],
    }

    def get_queryset(self):
        '''
            Returns the user's queryset if authenticated and never that of all users.
            Only superusers can get the queryset of all users.
        '''

        if not self.request.user.is_superuser:
            return self.queryset.filter(pk=self.request.user.pk)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        '''
            Adapt data before create the user.
            Compares the password whit de password confirmation and executes
            the super create method.
        '''

        logger.info(
            f'UserViewSet create -> User {request.data["username"]} created.'
        )
        logger.info(f'ESTO LLEGA COMO USUARIO A LA VIEW {request.data}')
        adapted_data = {
            'username': request.data['username'] if 'username' in request.data else request.data['userName'] if 'userName' in request.data else request.data['user_name'],
            'password': request.data['password'],
            'password_confirmation': request.data['password_confirmation'] if 'password_confirmation' in request.data else request.data['passwordConfirmation']
        }
        request.data.update(adapted_data)
        if request.data['password'] != request.data['password_confirmation']:
            return Response({'password': 'Passwords do not match.'}, 400)
        return super().create(request, *args, **kwargs)


class TaskViewSet(ModelViewSet):
    '''
        ViewSet for Task model. It allows to create, retrieve, update and delete the task.
        Only authenticated users can execute all actions on tasks.

        Atributes:
            queryset (QuerySet): QuerySet of the Task model.
            serializer_class (rest_framework.serializers.ModelSerializer): Serializer of the Task model.
            action_permissions (dict): Dictionary that contains the permissions for each action.
    '''

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter
    ]
    search_fields = [
        'description',
        'title'
    ]
    filterset_fields = [
        'completed',
        'created'
    ]

    def get_queryset(self):
        '''
            Returns the task's queryset if authenticated and never that of all tasks.
            Only superusers can get the queryset of all task.
        '''

        if not self.request.user.is_superuser:
            return self.queryset.filter(user=self.request.user.pk)
        return super().get_queryset()

    def perform_create(self, serializer) -> None:
        '''
            Sets the user of the task to the user who created it.
        '''

        logger.info(
            f'TaskViewSet perform_create -> Task created by {self.request.user.username}')
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=[
            'put',
            'patch'
        ]
    )
    def complete(
        self,
        request,
        pk=None
    ) -> Response:
        '''
            Allows to mark a task as complete.
            It receive the task id, marks as complete and returns the task data.
        '''

        logger.info(
            f'TaskViewSet complete -> Task {pk} from user {self.request.user.username} completed')
        task = self.get_object()
        serializer = self.get_serializer(task)
        task.complete()
        return Response(serializer.data, 200)

    @action(
        detail=True,
        methods=[
            'put',
            'patch'
        ]
    )
    def incomplete(
        self,
        request,
        pk=None
    ) -> Response:
        '''
            Allows to mark a task as incomplete.
            It receive the task id, marks as complete and returns the task data.
        '''

        logger.info(
            f'TaskViewSet incomplete -> Task {pk} from user {self.request.user.username} incomplete')
        task = self.get_object()
        serializer = self.get_serializer(task)
        task.incomplete()
        return Response(serializer.data, 200)
