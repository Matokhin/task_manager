from django.db import models
from django.conf import settings
# from pytils.translit import slugify

class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название тега"
    )
    # slug = models.SlugField(
    #     max_length=50,
    #     unique=True,
    #     blank=True,  # Разрешаем оставлять пустым в формах, так как генерируем сами
    #     verbose_name="Слаг"
    # )
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

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name