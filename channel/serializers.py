from rest_framework import serializers
from .models import Channel, Field, ChannelEntry, FieldEntry

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'
        read_only_fields = ['account', 'api_key', 'timestamp']

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field 
        fields = '__all__'
        read_only_fields = ['channel']

class ChannelEntrySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ChannelEntry
        fields = '__all__'
        read_only_fields = ['timestamp']

class FieldEntrySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = FieldEntry
        fields = '__all__'