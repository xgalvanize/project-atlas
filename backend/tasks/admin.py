from django.contrib import admin
from .models import Task, Action


class ActionInline(admin.TabularInline):
    model = Action
    extra = 1
    fields = ("description", "createdBy", "createdAt")
    readonly_fields = ("createdAt",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "project", "createdBy", "createdAt")
    list_filter = ("status",)
    search_fields = ("title",)
    inlines = [ActionInline]


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "description", "createdBy", "createdAt")
    search_fields = ("description",)
    readonly_fields = ("createdAt",)