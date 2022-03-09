from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username']

class UserSignUpSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
    )

    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)
    company = serializers.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = (
            'email', 
            'first_name', 
            'last_name',
            'company')