import requests
from datetime import date, datetime, timedelta
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
            serializer = FieldSerializer(channel.fields.all().order_by('pk'), many=True)
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
            channel_entries = None;
            number_of_hours = request.query_params.get('number_of_hours')
            last_entry_param = request.query_params.get('last_entry')

            if number_of_hours is not None: 
                try:
                    number_of_hours = int(number_of_hours)
                except ValueError:
                    return Response({"error":"must be a number"}, status=status.HTTP_400_BAD_REQUEST)
                interval = timedelta(hours=number_of_hours)
                end_date = datetime.today()
                start_date = end_date - interval
                channel_entries = channel.channel_entries.filter(timestamp__range=[start_date, end_date])
                data = get_channel_entries_data(channel, channel_entries)
                return Response(data, status=status.HTTP_200_OK)

            elif last_entry_param is not None:
                last_timestamp = None;
                try:
                    last_timestamp = datetime.strptime(last_entry_param, "%B %d, %Y %I:%M:%S %p")
                except ValueError as e:
                    return Response({"error":"should be a valid timestamp"}, status=status.HTTP_400_BAD_REQUEST)

                start_date = last_timestamp + timedelta(seconds=1)
                channel_entries = channel.channel_entries.filter(timestamp__gte=start_date)
                data = get_channel_entries_data(channel, channel_entries)
                return Response(data, status=status.HTTP_200_OK)

            else:
                return Response({"error":"there cant more than 1 params"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"youve done goof"}, status=status.HTTP_400_BAD_REQUEST)

def get_channel_entries_data(channel, channel_entries):
    field_count = channel.fields.all().count()
    included_fields = ['timestamp']
    for i in range(1, field_count+1):
        included_fields.append(f'field{i}')
        channel_entries_serializer = ChannelEntrySerializer(channel_entries, many=True, fields=tuple(included_fields))
    return channel_entries_serializer.data;


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
        # the channel fields will be ordered by there creation time meaning the first field
        # created represents field1 on channel entry, meaning the second is field2
        channel_fields = channel.fields.all().order_by('pk')
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
        # print(validated_data)
        # d = [validated_data[field_name] for field_name in field_names]
        # basically order the validated data based the order of the field names
        d = [None]*8
        for i in range(len(field_names)):
            d[i] = validated_data[field_names[i]]

        # print(d)
        # we now have a clean data 
        # we're gonna create a new ChannelEntry
        # d[0] for field1
        channel_entry = ChannelEntry(channel=channel, field1=d[0], field2=d[1], field3=d[2], field4=d[3], field5=d[4], field6=d[5], field7=d[6], field8=d[7])

        # save
        channel_entry.save()
        return Response(request.data, status=status.HTTP_200_OK)

    def get(self, request, format=None):
        api_key = request.query_params.get('api_key')
        if api_key is None:
            return Response({"error": "api key is not provided"}, status=status.HTTP_400_BAD_REQUEST)
        channel = self.get_channel(api_key)
        if channel is None:
            return Response({"error": "invalid api key"}, status=status.HTTP_401_UNAUTHORIZED)

        specific_date_str = request.query_params.get('specific_date')
        request_all_records = request.query_params.get('request_all_records')

        if request_all_records is not None and request_all_records == 'true':
            channel_entries = channel.channel_entries.all()
            data = get_channel_entries_data(channel, channel_entries)
            return Response(data, status=status.HTTP_200_OK)

        if specific_date_str is None:
            specific_date = date.today()
        else:
            try:
                specific_date = datetime.strptime(specific_date_str, "%Y-%m-%d")
            except:
                return Response({'invalid_date_str': 'please provide a valid date str YYYY-mm-dd'})

        start_date = specific_date;
        end_date = start_date + timedelta(days=1);
        channel_entries = channel.channel_entries.filter(timestamp__range=[start_date, end_date])
        data = get_channel_entries_data(channel, channel_entries)
        return Response(data, status=status.HTTP_200_OK)

class WakeMeUpAPIView(APIView):
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
        urls = request.data.get('urls')
        if urls is None:
            return Response({"error": "provide urls"}, status=status.HTTP_400_BAD_REQUEST)
        failures = []
        for url in urls:
            try:
                requests.get(url)
            except Exception as e:
                print(e)
                failures.append(str(e))
        if len(failures) != 0:
            return Response({"error": failures}, status.HTTP_400_BAD_REQUEST)
        return Response({"success": "all urls successfully queried"})

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