from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    api_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title   