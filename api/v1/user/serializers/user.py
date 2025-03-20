from rest_framework import serializers
from api.v1.user.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Handler serialization of User model
    """
    class Meta:
        model = User
        exclude = ('password',)
