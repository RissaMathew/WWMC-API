from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class RegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    nationality = serializers.CharField(max_length=100)
    mobile_number = serializers.IntegerField(required=True,
                                             validators=[UniqueValidator(queryset=UserProfile.objects.all())]
                                            )

    class Meta:
        model = UserProfile
        fields = ('user', 'nationality', 'mobile_number')

    def create(self, validated_data):
        profile_data = validated_data.pop('user')
        user = User.objects.create(**profile_data)
        UserProfile.objects.create(user=user, **validated_data)
        user.set_password(profile_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email_or_mobile = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email_or_mobile', 'password')
