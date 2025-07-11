from django.db import models

class Customer(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-date_joined']
        db_table = 'customer'