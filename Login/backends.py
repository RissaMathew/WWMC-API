from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.db.models import Q
from rest_framework.serializers import Serializer

User = get_user_model()


class EmailMobileBackend(BaseBackend):
    def authenticate(self, request, email=None, mobile_number=None, password=None, **kwargs):
        try:
            # mobile_number = Serializer.data.get('')
            if mobile_number is not None:
                user_profile = UserProfile.objects.filter(mobile_number=mobile_number).last()
                if user_profile.user.check_password(password):
                    return user_profile.user
            elif email is not None:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
