from django.db import models
from fbbot.models import Message


class CestLheure(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    exact_date = models.DateTimeField()

    def __str__(self):
        return str(self.message)

    class Meta:
        get_latest_by = "exact_date"
        ordering = ["-exact_date"]


class CestLheureIndex(models.Model):
    last_listened = models.ForeignKey(Message, on_delete=models.CASCADE)