from django.db import models
from django.contrib.auth import get_user_model
from apps.projects.models import Project


User = get_user_model()

class Task(models.Model):
    id = models.BigAutoField(primary_key=True)

    class TaskStatus(models.TextChoices):
        TODO = 'TODO', 'To Do'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        DONE = 'DONE', 'Done'

    class TaskPriority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    status = models.CharField(
        max_length = 20,
        choices = TaskStatus.choices,
        default = TaskStatus.TODO,
        verbose_name = "Статус"
    )
    priority = models.CharField(
        max_length = 20,
        choices = TaskPriority.choices,
        default = TaskPriority.MEDIUM,
        verbose_name = "Приоритет"
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name="Проект"
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name="Исполнитель"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['-created_at']

    def __str__(self):
        return self.title