from django.db import models


class Programme(models.Model):
    '''Students programme model'''

    name = models.CharField(max_length=64, unique=True)
    code = models.CharField(
        max_length=16,
        unique=True,
        blank=True,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name
