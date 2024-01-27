from .models import (
    User,
    Task
)
from .serializers import (
    UserSerializer,
    TaskSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
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
        'list': [
            IsAuthenticated,
            IsAdminUser
        ],
        'destroy': [IsAuthenticated],
        'update': [IsAuthenticated],
    }

    def get_queryset(self):
        '''
            Returns the user's queryset if authenticated and never that of all users.
            Only superusers can get the queryset of all users.

            Returns:
                queryset (QuerySet): QuerySet of the User model.
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
