import logging

from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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

        logger.info(
            f'UserSerializer create -> User {validated_data["username"]} created.')
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model = User
        fields = [
            'pk',
            'password',
            'username',
            'email'
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
            'pk',
            'completed',
            'description',
            'title',
            'created'
        ]


class TokenSerializer(TokenObtainPairSerializer):
    '''
        Custom token serializer for the JWT token.
    '''

    @classmethod
    def get_token(cls, user):
        '''
            Adds pk, username and email fields of the current user to the super
            get_token method.

            Args:
                user (api.models.User): User to get the token for.
        '''

        logger.info(
            f'TokenSerializer get_token -> Token for user {user.username}.'
        )
        token = super().get_token(user)
        token['pk'] = user.pk
        token['username'] = user.get_username()
        token['email'] = user.get_email_field_name()
        logger.info(f'ESTO QUEDA COMO TOKEN EN EL SERIALIZER {token}')
        return token
