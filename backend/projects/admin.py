from django.contrib import admin
from .models import Project, Action

# Register your models here.
class ActionInline(admin.TabularInline):
    model = Action
    extra = 1
    fields = ("action_type", "status", "actor")
    ordering = ("status",)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [ActionInline]

@admin.register(Action)    
class ActionAdmin(admin.ModelAdmin):
    list_display = ("action_type", "status", "project", "actor")
    list_filter = ("status", "action_type")
    search_fields = ("project__name",)
