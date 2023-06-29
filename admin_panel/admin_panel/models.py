from django.db import models


class Start_Task_List(models.Model):
    name_task = models.CharField(max_length=50, primary_key=True)
    url = models.CharField(max_length=50)

    class Meta:
        db_table = "start_task"
        verbose_name_plural = 'Початкові завдання для юзерів'


class Task_list(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    url = models.CharField(max_length=100)
    payment = models.IntegerField()
    status_of_task = models.BooleanField()

    class Meta:
        db_table = 'task_list_db'
        verbose_name_plural = 'Всі завдання для юзерів'




