import logging

from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    TextField,
    EmailField,
)
from django.core.validators import validate_email, RegexValidator

logger = logging.getLogger(__name__)


class User(AbstractUser):
    """
    Entity/Model for the users

    Attributes:
        password (str): User's password.
        username (str): User's username.
        email (str): User's email.
    """

    username = CharField(
        unique=True,
        db_index=True,
        max_length=25,
        error_messages={
            "unique": "Nombre de usuario en uso.",
            "invalid": "Nombre de usuario inválido.",
            "max_length": "Nombre de usuario demasiado largo.",
        }
    )
    email = EmailField(
        unique=True,
        db_index=True,
        validators=[validate_email],
        error_messages={"unique": "Email en uso.", "invalid": "Email inválido."}
    )
    password = CharField(
        validators=[RegexValidator(regex=r"^(?=.*.)(?=.*\d).{8,}$")],
        error_messages={"invalid": "Contraseña inválida."}
    )

    def get_email(self) -> str:
        """
        Returns the user's email.
        """

        logger.info("UserModel get_email.")
        return self.email

    def get_password(self) -> str:
        """
        Returns the user's hashed password
        """

        logger.info("UserModel get_password.")
        return self.password

    def __str__(self) -> str:
        return f"Username: {self.username}, Email: {self.email}"


class Task(Model):
    """
    Entity/Model for the tasks

    Attributes:
        completed (bool): Determines if the user marked the task as completed.
        description (str): User-entered descriptive colloquial text for the task.
        title (str): Title of the task.
        user (django.contrib.auth.models.User): Task owner.
        created (datetime.datetime): Date and time of task creation.
    """

    completed = BooleanField(default=False)
    description = TextField()
    title = CharField(max_length=100)
    user = ForeignKey(User, on_delete=CASCADE)
    created = DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Title: {self.title}. {self.user.__str__()}"

    def complete(self, save: bool = True) -> None:
        """
        Marks the task as complete.

        Args:
            save (bool): Determines if the task is saved in the database.
        """

        logger.info(f"Task complete -> Task {self.pk} completed.")
        self.completed = True
        if save:
            self.save()

    def incomplete(self, save: bool = True) -> None:
        """
        Marks the task as incomplete.

        Args:
            save (bool): Determines if the task is saved in the database.
        """

        logger.info(f"Task incomplete -> Task {self.pk} incomplete.")
        self.completed = False
        if save:
            self.save()
