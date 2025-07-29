from django.db import models


class SoftDeleteModel(models.Model):
  is_hidden = models.BooleanField(default=False)

  class Meta:
    abstract = True

  def soft_delete(self):
    self.is_hidden = True
    self.save()
