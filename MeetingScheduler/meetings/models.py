from django.db import models

class clients(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    def _str_(self):
        return self.name
