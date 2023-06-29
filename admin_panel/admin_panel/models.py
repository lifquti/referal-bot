from django.db import models


class Start_Task_List(models.Model):
    name_task = models.CharField(max_length=50, primary_key=True)
    url = models.CharField(max_length=50)

    class Meta:
        db_table = "start_task"
        verbose_name_plural = 'Початкові завдання для юзерів'

    def Task_url(self):
        return self.url

class Task_list(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    url = models.CharField(max_length=100)
    payment = models.IntegerField()
    status_of_task = models.BooleanField()

    class Meta:
        db_table = 'task_list_db'
        verbose_name_plural = 'Всі завдання для юзерів'

    def task_name(self):
        return self.name

    def Pay_for_work(self):
        return f"{self.payment} UAH"

    def Task_url(self):
        return self.url




