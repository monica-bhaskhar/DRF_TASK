from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import  User

class Todo(models.Model):
    STATUS_CHOICES = [('TODO','TODO'),('WIP','WIP'),('DONE','DONE')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES)

    class Meta:
        verbose_name = _("Todo")
        verbose_name_plural = _("Todos")

    def __str__(self):
        return self.title
