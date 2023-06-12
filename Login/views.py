from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from .serializers import LoginSerializer,RegistrationSerializer



jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
#        payload = jwt_payload_handler(user)
#        token = jwt_encode_handler(payload)
        return Response({'Registration Sucessfull'})


class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email_or_mobile = serializer.validated_data['email_or_mobile']
            password = serializer.validated_data['password']

            # Check if the email_or_mobile is a valid email address
            is_email = '@' in email_or_mobile

            # Authenticate the user
            user = None
            if is_email:
                print(email_or_mobile,password)
                user = authenticate(request,email=email_or_mobile, password=password)
            else:
                # Assuming the mobile number field is 'phone_number' in the User model
                user = authenticate(request, mobile_number=email_or_mobile, password=password)

            if user:
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                return Response({'token': token})
            else:
                return Response({'error': 'Invalid credentials'}, status=400)
