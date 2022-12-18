from django.contrib import admin

from .models import Channel, Field, ChannelEntry, FieldEntry

# Register your models here.
admin.site.register(Channel)
admin.site.register(Field)
admin.site.register(ChannelEntry)
admin.site.register(FieldEntry)