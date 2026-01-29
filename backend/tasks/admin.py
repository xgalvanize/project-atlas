from django.contrib import admin
from .models import Task, Action


class ActionInline(admin.TabularInline):
    model = Action
    extra = 1
    fields = ("description", "created_by", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "project", "created_by", "created_at")
    list_filter = ("status",)
    search_fields = ("title",)
    inlines = [ActionInline]


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "description", "created_by", "created_at")
    search_fields = ("description",)
    readonly_fields = ("created_at",)
