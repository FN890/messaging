from rest_framework import serializers

from messaging.app.models import CustomUser, Message


class CustomUserSerializer(serializers.ModelSerializer):
    """ Serializer for the  CustomUser class. """
    class Meta:
        model = CustomUser
        fields = ["id", "username"]


class MessageSerializer(serializers.ModelSerializer):
    """ Serializer for the message class. """
    class Meta:
        model = Message
        fields = ["id", "created", "recipient", 
                  "sender", "message"]
