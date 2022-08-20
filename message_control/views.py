from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializer import GenericFileUploadSerializer, MessageAttachmentSerializer, MessageSerializer
from .models import GenericFileUpload, MessageAttachment, Message
from django.db.models import Q
from rest_framework.response import Response




class GenericFileUploadView(ModelViewSet) :
    queryset = GenericFileUpload.objects.all()
    serializer_class = GenericFileUploadSerializer



class MessageView(ModelViewSet) :

    queryset = Message.objects.select_related("sender", 'reciever').prefetch_related("message_attachments")

    serializer_class = MessageSerializer

    def get_queryset(self):
        data = self.request.query_params.dict()
        user_id = data.get("id", None)
        if user_id :
            active_user_id = self.request.user.id
            return self.queryset.filter( Q(sender = user_id, reciever = active_user_id)  | Q(
                sender=active_user_id, reciever=user_id) ).distinct()
            
        return self.queryset

    def create(self, request, *args, **kwargs) :
        try :
            request.data._mutable = True
        except :
            pass
        attachments = request.data.pop("attachments", None)
        print(attachments)

        if str(request.user.id) != str(request.data.get("sender", None)) :
            raise ValueError("only sender can create a message")
        
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if attachments :
            MessageAttachment.objects.bulk_create([MessageAttachment(**attachment, message_id = serializer.data['id']) for attachment in attachments])

            message_data = self.queryset().get(id = serializer.data['id'])

            return Response(self.serializer_class(message_data).data, status = 201)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):

        try :
            request.data_mutable = True
        except :
            pass


        attachments = request.data.get("attachments", None)
        instance = self.get_object()

        serializer = self.serializer_class(data = request.data, instance=instance, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        MessageAttachment.objects.filter(message = instance.id).delete()

        if attachments :
            MessageAttachment.objects.bulk_create([MessageAttachment(**attachment, message = instance.id) for attachment in attachments])

            message_data = self.get_object()
            return Response(self.serializer_class(message_data), status = 201)

        return Response(serializer.data, status=201)


class MessageAttachmentView(ModelViewSet) :
    queryset = MessageAttachment.objects.all()
    serializer_class = MessageAttachmentSerializer


    

class ReadMultipleMessages(APIView) :
    http_method_names = ("get")
    def post(self, request) :

        data = request.data.get("messages_ids", None)
        Message.objects.filter(id__in = data).update(is_read = True)

        return Response("success")