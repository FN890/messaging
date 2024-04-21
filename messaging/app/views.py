from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from messaging.app.serializers import CustomUserSerializer, MessageSerializer
from messaging.app.models import CustomUser, Message

# Create your views here.


class GetUsers(APIView):
    """ Endpoint for retrieving users."""

    def get(self, request, format=None):
        queryset = CustomUser.objects.all().order_by('username')
        if queryset.exists():
            serializer = CustomUserSerializer(queryset, many=True)
            return Response(serializer.data)

        return Response({"error": "No users found."}, status=status.HTTP_404_NOT_FOUND)


class PostUser(APIView):
    """ Endpoint creating users."""

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUser(APIView):
    """ Endpoint for deleting users. """

    def delete(self, request):
        user_id = request.query_params.get("user_id")

        if not user_id:
            return Response({"error": "No user ID provided."}, status=status.HTTP_400_BAD_REQUEST)

        result = CustomUser.objects.filter(id=user_id).delete()
        deleted_count = result[0]

        if deleted_count == 0:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"success": "User deleted."}, status=status.HTTP_204_NO_CONTENT)


class PostMessage(APIView):
    """ Endpoint for sending messages."""

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetNewMessages(APIView):
    """ 
    Endpoint for retrieving new messages specific for a user.
    Example value for last_update = 2000-01-01T12:00:00+02:00.
    """

    def get(self, request, user_id, last_update, format=None):
        queryset = Message.objects.filter(
            recipient_id=user_id).order_by('created')

        last_update_parsed = parse_datetime(last_update)
        if last_update_parsed is None:
            return Response({'error': 'Invalid datetime format: ' + last_update}, status=status.HTTP_400_BAD_REQUEST)

        queryset = queryset.filter(created__gt=last_update_parsed)

        if queryset.exists():
            serializer = MessageSerializer(queryset, many=True)
            return Response(serializer.data)

        return Response({"error": "No messages found."}, status=status.HTTP_404_NOT_FOUND)


class GetMessagesByIndices(APIView):
    """ Endpoint for retrieving messages specific to a user using indices. Using pagination would be better for a production setting. """

    def get(self, request, user_id, start_index, end_index, format=None):
        queryset = Message.objects.filter(
            recipient_id=user_id).order_by('created')

        queryset = queryset[int(start_index):int(end_index)]

        if queryset.exists():
            serializer = MessageSerializer(queryset, many=True)
            return Response(serializer.data)

        return Response({"error": "No messages found."}, status=status.HTTP_404_NOT_FOUND)


class DeleteMessages(APIView):
    """ Endpoint for deleting messages. """

    def delete(self, request):
        message_ids = request.query_params.getlist('message_ids')

        if not message_ids:
            return Response({"error": "No message IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        deleted_count = Message.objects.filter(id__in=message_ids).delete()[0]

        if deleted_count == 0:
            return Response({"error": "Message(s) not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"success": "Message(s) deleted."}, status=status.HTTP_204_NO_CONTENT)
