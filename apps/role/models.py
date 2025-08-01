from django.db import models

# Create your models here.
class Role(models.Model):
  role_id = models.AutoField(primary_key=True)
  role_name = models.AutoField(max_length=50)
  
  class Meta:
    verbose_name = 'Rol'
    verbose_name_plural = 'Roles'
    db_table = 'role'
    managed = False
    
  def __str__(self):
    return self.role_name