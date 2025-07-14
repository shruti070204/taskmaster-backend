# Djano admin module
from django.contrib import admin #built-in admin site framework. use ro register and custom models apppear in interface
from .models import Task, Priority, AuditLog #from models.py to register with admin site

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin): #to custom your model apperance and behave in panel
    list_display = ('title', 'assigned_to', 'status', 'priority_level', 'due_date') #display these fields in a table for task in admin page
    list_filter = ('status', 'priority_level', 'due_date') #filters task, add filters in right
    search_fields = ('title', 'description') #search funtionality

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('id', 'level') #display priority field
    ordering = ['id'] # arrange by (auto incremented)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'action', 'timestamp') # these cols are shown
    ordering = ['-timestamp'] #most recent first(descending)