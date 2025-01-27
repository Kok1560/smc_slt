from django.db import models

class Members(models.Model):
    email = models.EmailField('User Email')

    def __str__(self):
        return self.email