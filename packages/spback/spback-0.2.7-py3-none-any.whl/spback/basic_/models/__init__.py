from django.db import models

from .soft_delete import SoftDeleteModel  # noqa


class TimeModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True, verbose_name=("created_at"))
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True
