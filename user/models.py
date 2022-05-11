from django.db import models

# Create your models here.

class Account(models.Model):
    uid = models.CharField(max_length=200, null=False, blank=False, unique=True)
    email = models.EmailField(max_length=100, null=True)
    nickname = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user'
        verbose_name_plural = "회원"

    def __str__(self):
        return f'{self.nickname}'
