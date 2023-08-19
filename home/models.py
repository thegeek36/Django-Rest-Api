from django.db import models

# Create your models here.

class Color(models.Model):
    color_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.color_name

class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    color = models.ForeignKey(Color, null=True,blank = True,on_delete=models.CASCADE , related_name = "color")

