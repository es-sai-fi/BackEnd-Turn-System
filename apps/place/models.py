from django.db import models
from ..service.models import Service
from ..custom_user.models import CustomUser


class Place(models.Model):
    place_id = models.AutoField(primary_key=True)
    service_id = models.OneToOneField(
        Service, on_delete=models.CASCADE, db_column='service_id', unique=True)
    place_name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "place"
        managed = False

    def __str__(self):
        return self.place_name


class PlaceCustomUser(models.Model):
    place_custom_user_id = models.AutoField(
        primary_key=True, db_column='place_custom_user_id', unique=True)
    custom_user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, db_column='custom_user_id')
    place_id = models.ForeignKey(
        Place, on_delete=models.CASCADE, db_column='place_id')

    class Meta:
        db_table = 'place_custom_user'
        managed = False

    def __str__(self):
        return f'{self.place_id}:{self.custom_user_id}'
