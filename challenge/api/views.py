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

        task = self.get_object()
        serializer = self.get_serializer(task)
        task.incomplete()
        return Response(serializer.data, 200)
