from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(verbose_name='username', max_length=40)
    password = models.CharField(verbose_name='password', max_length=30)
    age = models.IntegerField(verbose_name='age')
    gender = models.CharField(verbose_name='gender', max_length=30)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering =['username']
