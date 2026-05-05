from django.conf import settings
from django.db import models
from django.utils import timezone


class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes")
    date = models.DateField()
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_edited_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "date")
        ordering = ["date"]

    def save(self, *args, **kwargs):
        if self.pk:
            self.last_edited_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def last_edited_display(self):
        return self.last_edited_at.isoformat() if self.last_edited_at else "---"
