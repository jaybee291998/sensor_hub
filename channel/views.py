from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .models import Channel, Field, ChannelEntry, FieldEntry
from .serializers import ChannelSerializer, FieldSerializer, ChannelEntrySerializer, FieldEntrySerializer

# Create your views here.
class ChannelListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        channels = Channel.objects.filter(account=request.user)
        serializer = ChannelSerializer(channels, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ChannelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(account=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FieldListAPIView(APIView):
    authentication_classes =[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, channel_id, user):
        # retrieve channel if it exists
        try:
            channel = Channel.objects.get(id=channel_id)
            # check if user is the owner of channel
            if user != channel.account: channel = None
        except Channel.DoesNotExist:
            channel = None
        return channel

    def get(self, request, channel_id, format=None):
        channel = self.get_object(channel_id, request.user)
        if channel is not None:
            serializer = FieldSerializer(channel.fields.all(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # channel doesnt exists or have no access
        context = {
            "error": "You have no permission to access this channel or it doesnt exists"
        }
        return Response(context, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, channel_id, format=None):
        channel = self.get_object(channel_id, request.user)
        if channel is not None:
            
            param = request.query_params.get('bulk');
            bulk = False
            if param is not None:
                bulk = param == 'true'
            serializer = FieldSerializer(data=request.data)
            if bulk:
                serializer = FieldSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save(channel=channel)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        context = {
            "error": "You have no permission to access this channel or it doesnt exists"
        }
        return Response(context, status=status.HTTP_401_UNAUTHORIZED)

class ChannelEntryListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # get channel
    def get_object(self, channel_id, user):
        # retrieve channel if it exists
        try:
            channel = Channel.objects.get(id=channel_id)
            # check if user is the owner of channel
            if user != channel.account: channel = None
        except Channel.DoesNotExist:
            channel = None
        return channel

    def get(self, request, channel_id, format=None):
        channel = self.get_object(channel_id, request.user)
        if channel is not None:
            context = {}
            channel_entries = channel.channel_entries.all()
            channel_entries_serializer = ChannelEntrySerializer(channel_entries, many=True)
            for channel_entry, serialized in zip(channel_entries, channel_entries_serializer.data):
                field_entries = channel_entry.field_entries.all()
                field_entries_serialized = FieldEntrySerializer(field_entries, many=True, fields=('value', 'field')).data
                # context[serialized['timestamp']] = field_entries_serialized
            return Response(context, status=status.HTTP_200_OK)
        return Response({"error":"youve done goof"}, status=status.HTTP_400_BAD_REQUEST)

class ChannelEntryAPIView(APIView):
    # get channel
    def get_channel(self, api_key):
        # retrieve channel if it exists
        try:
            channel = Channel.objects.get(api_key=api_key)
        except Channel.DoesNotExist:
            channel = None
        return channel

    def post(self, request, format=None):
        api_key = request.data.get('api_key')
        if api_key is None:
            return Response({"error": "api key is not provided"}, status=status.HTTP_400_BAD_REQUEST)
        channel = self.get_channel(api_key)
        if channel is None:
            return Response({"error": "invalid api key"}, status=status.HTTP_401_UNAUTHORIZED)
        # data validation, will refactor later
        channel_fields = channel.fields.all()
        field_names = [field.name for field in channel_fields]
        # make sure that every field is present on the request
        field_validation = {}
        validated_data = {}
        for name in field_names:
            value = request.data.get(name)
            if value is None:
                field_validation[name] = f'{name} must be present'
                print(f'{name} must be present')
            else:
                # convert values to float
                try:
                    validated_data[name] = float(value)
                except ValueError as e:
                    field_validation[name] = f'{name} must be a number'
                    print(f'{name} must be a number')
        # check if field valdiation is empty
        if field_validation:
            return Response(field_validation, status=status.HTTP_400_BAD_REQUEST)
        print(validated_data)

        # we now have a clean data 
        # we're gonna create a new ChannelEntry
        channel_entry = ChannelEntry(channel=channel)
        # save
        channel_entry.save()
        for field in channel_fields:
            new_field_entry = FieldEntry(field=field, value=validated_data[field.name], channel_entry=channel_entry)
            new_field_entry.save()
        return Response(request.data, status=status.HTTP_200_OK)

def validate_sensor_data(sensor_data, channel):
    channel_fields = channel.fields.all()
    field_names = [field.name for field in channel_fields]
    # make sure that every field is present on the request
    field_validation = {}
    validated_data = {}
    for name in field_names:
        value = request.data.get(name)
        if value is None:
            field_validation[name] = f'{name} must be present'
        else:
            # convert values to float
            try:
                validated_data[name] = float(value)
            except ValueError as e:
                field_validation[name] = f'{name} must be a number'
    # check if field valdiation is empty
    if field_validation:
        return Response(field_validation, status=status.HTTP_400_BAD_REQUEST)
    print(validated_data)