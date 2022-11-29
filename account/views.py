from django.contrib.auth import authenticate, get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .serializers import CustomUSerSerializer

User = get_user_model()

class UserList(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = CustomUSerSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = CustomUSerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', ])
def login(request):
    context = {}
    email = request.POST.get('email')
    password = request.POST.get('password')
    print(f'email: {email}')
    print(f'password: {password}')
    user = authenticate(email=email, password=password)
    if user:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        context['response'] = "successfully authenticated"
        context['token'] = token.key
    else:
        context['response'] = "Error"
        context['error_message'] = "invalid ceredentials"
    
    return Response(context)

@api_view(["POST", ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def secret(request):
    data = request.POST.get('data')
    return Response({'email': request.user.email, 'data': data})

@api_view(['POST', ])
def public(request):
    sensor = request.POST.get('sensor')
    return Response({'sensor': sensor})