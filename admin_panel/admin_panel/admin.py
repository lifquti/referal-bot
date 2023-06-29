from django.contrib import admin
from .models import Start_Task_List, Task_list


@admin.register(Start_Task_List)
class Url_list(admin.ModelAdmin):
    list_display = ('name_task', 'url')


@admin.register(Task_list)
class Task_list_for_user(admin.ModelAdmin):
    list_display = ('name', 'url', 'payment', 'status_of_task')
