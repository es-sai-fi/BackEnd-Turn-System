from django.db import models

# Create your models here.
class Place(models.Model):
  place_id = models.AutoField(primary_key=True)
  place_name = models.CharField(max_length=50)
  
  class Meta:
    verbose_name = 'Punto de atención'
    verbose_name_plural = 'Puntos de atención'
    db_table = 'place'
    managed = False
    
  def __str__(self):
    return self.place_name