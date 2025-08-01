from django.db import models


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=50, unique=True)
    service_desc = models.TextField()

    class Meta:
        db_table = "service"
        managed = False

    def __str__(self):
        return self.service_name
