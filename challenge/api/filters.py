from django_filters.rest_framework import BooleanFilter, DateTimeFilter, FilterSet

from .models import Task


class TaskFilter(FilterSet):
    created_to = DateTimeFilter(field_name="created", lookup_expr="lte")
    created_from = DateTimeFilter(field_name="created", lookup_expr="gte")
    completed = BooleanFilter(field_name="completed")

    class Meta:
        model = Task
        fields = ["created", "completed"]
