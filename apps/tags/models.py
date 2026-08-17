from django.db import models
from django.conf import settings

class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название тега"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tags",
        verbose_name="Создатель"
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]
    def __str__(self):
        return self.name