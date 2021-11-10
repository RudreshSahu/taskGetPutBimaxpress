from rest_framework_mongoengine import serializers

from .models import Users

class UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Users
        fields = '__all__'
