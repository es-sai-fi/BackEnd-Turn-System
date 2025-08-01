from ..place.models import Place
from django.db import models
from ..custom_user.models import CustomUser


# Create your models here.
class Turn(models.Model):
    turn_id = models.AutoField(primary_key=True)
    turn_name = models.CharField(max_length=5)
    turn_priority = models.CharField(max_length=1)
    active = models.BooleanField(default=True)
    canceled = models.BooleanField(default=False)
    attended_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, db_column='attended_by', null=True, related_name='attended_turns')
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, db_column='owner', null=True, related_name='owned_turns')
    place_id = models.ForeignKey(
        Place, on_delete=models.CASCADE, db_column='place_id')
    date_created = models.DateTimeField(auto_now_add=True)
    date_closed = models.DateTimeField(null=True)

    @property
    def turn_attended_time(self):
        if self.date_closed and self.date_created:
            delta = self.date_closed - self.date_created
            return delta.total_seconds() / 60
        return 0.0

    class Meta:
        db_table = 'turn'
        managed = False

    def __str__(self):
        return self.turn_name
