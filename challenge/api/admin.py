from django.contrib import admin

from .models import Task, User


class TaskAdmin(admin.ModelAdmin):
    list_display = ["pk", "completed", "description", "title", "created"]
    search_fields = ["description", "title"]
    list_filter = ["completed", "created"]


admin.site.register(Task, TaskAdmin)
admin.site.register(User)
