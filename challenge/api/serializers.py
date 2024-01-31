import logging

from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from .models import (
    User,
    Task
)


logger = logging.getLogger(__name__)


class UserSerializer(ModelSerializer):
    '''
        Serializer for the User model. It only serializes the username.

        Attributes:
            username (str): Username of the user.
    '''

    def create(
        self,
        validated_data: dict
    ) -> User:
        '''
            Overrides the create method to hash the password.

            Args:
                validated_data (dict): Dictionary with the validated data.
        '''

        logger.info(f'UserSerializer create -> User {validated_data["username"]} created.')
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model = User
        fields = [
            'password',
            'username'
        ]


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
        fields = [
            'completed',
            'description',
            'title',
            'created'
        ]
