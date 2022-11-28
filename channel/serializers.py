from rest_framework import serializers
from .models import Channel

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'
        read_only_fields = ['account', 'api_key', 'timestamp']