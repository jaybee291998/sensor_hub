import random, string

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Channel(models.Model):
    name             = models.CharField(max_length=64)
    description      = models.TextField()
    api_key          = models.CharField(max_length=32)
    latitude         = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude        = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    timestamp        = models.DateTimeField(auto_now_add=True)
    account          = models.ForeignKey(User, related_name="channel", on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        # generate 32 alphanumeric character
        self.api_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.account.email})"

class Field(models.Model):
    name              = models.CharField(max_length=64)
    channel           = models.ForeignKey(Channel, related_name="fields", on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        # current number of fields of the channel
        current_number_of_fields = self.channel.fields.all().count()
        # print(f'current count: {current_number_of_fields}')
        if current_number_of_fields <= 7:
            # make sure that a channel only has 8 fields
            super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name} - {self.channel.name}";

class ChannelEntry(models.Model):
    field1            = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    field2            = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    field3            = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    field4            = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    field5            = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    field6            = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    field7            = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    field8            = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    channel           = models.ForeignKey(Channel, related_name="channel_entries", on_delete=models.CASCADE, null=True)
    timestamp         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.channel.name} - {self.timestamp}'

class FieldEntry(models.Model):
    field             = models.ForeignKey(Field, related_name="field_entries", on_delete=models.CASCADE, null=True)
    value             = models.DecimalField(max_digits=20, decimal_places=10)
    channel_entry     = models.ForeignKey(ChannelEntry, related_name="field_entries", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.field.name} - {self.value}'
