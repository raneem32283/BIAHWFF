from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=10)
    x = models.DecimalField(max_digits=100,decimal_places=10)
    y = models.DecimalField(max_digits=100,decimal_places=10)
class Box(models.Model):
  id = models.AutoField(primary_key=True)
  weight = models.IntegerField()
  value = models.IntegerField()
  destination = models.ForeignKey(City, on_delete=models.CASCADE)

class Car(models.Model):
  id = models.AutoField(primary_key=True)
  capacity = models.IntegerField()
  weight_of_trak = models.IntegerField()

class Route(models.Model):
  car = models.ForeignKey(Car, on_delete=models.CASCADE)
  city = models.ForeignKey(City, on_delete=models.CASCADE)
  order = models.IntegerField()

class Meta:
  ordering = ['order']

class Fitness(models.Model):
  individual = models.CharField(max_length=255)
  fitness_value = models.FloatField()


