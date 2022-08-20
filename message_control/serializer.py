from rest_framework import serializers
from .models import GenericFileUpload, Message, MessageAttachment
from control_user.serializer import UserSerializer

class GenericFileUploadSerializer(serializers.ModelSerializer) :

    class Meta :
        model = GenericFileUpload
        fields = "__all__"

class MessageAttachmentSerializer(serializers.ModelSerializer) :
    # attachment = GenericFileUploadSerializer(read_only = True ,many = True)

    class Meta :
        model = MessageAttachment
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer) :
    msg_sender = serializers.SerializerMethodField("get_sender_data")
    msg_reciever = serializers.SerializerMethodField("get_reciever_data")
    message_attachments_list = serializers.SerializerMethodField("get_messages_attachments")
    # message_attachments = MessageAttachmentSerializer(many = True)


    class Meta :
        model = Message
        fields = "__all__"

    
    def get_sender_data(self, obj) :
        return UserSerializer(obj.sender).data

    def get_reciever_data(self, obj) :
        return UserSerializer(obj.reciever).data
    def get_messages_attachments(self, obj) :
        return MessageAttachmentSerializer(obj.message_attachments.all(), many = True).data 