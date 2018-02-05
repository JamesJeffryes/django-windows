from django.db import models
import uuid


class Donor(models.Model):
    donor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    init_class = models.CharField(max_length=50)
    email_address = models.CharField(max_length=100)
    donation_amount = models.IntegerField()
    invited = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Window(models.Model):
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    sponsor = models.ForeignKey(Donor, null=True, blank=True, on_delete=models.SET_NULL)
    plaque = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return "{}: {}".format(self.code, self.description)

