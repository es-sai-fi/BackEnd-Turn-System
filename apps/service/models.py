from django.db import models

# Create your models here.
class Service(models.Model):
  service_id = models.AutoField(primary_key=True)
  service_name = models.CharField(max_length=50)
  service_desc = models.TextField()
  
  class Meta:
    verbose_name = 'Servicio'
    verbose_name_plural = 'Servicios'
    db_table = 'service'
    managed = False