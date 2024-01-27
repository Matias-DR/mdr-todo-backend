from rest_framework.serializers import ModelSerializer
from .models import (
    User,
    Task
)


class UserSerializer(ModelSerializer):
    '''
        Serializer for the User model. It only serializes the username.

        Attributes:
            username (str): Username of the user.
    '''
    class Meta:
        model = User
        fields = ['username']


class TaskSerializer(ModelSerializer):
    '''
        Serializer for the Task model. Serializes all fields except the user.

        Attributes:
            completed (bool): Determines if the user marked the task as completed.
            description (str): User-entered descriptive colloquial text for the task.
            title (str): Title of the task.
    '''
    class Meta:
        model = Task
        fields = '__all__'