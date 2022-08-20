from django.contrib import admin
from .models import GenericFileUpload, Message, MessageAttachment


admin.site.register(GenericFileUpload)
admin.site.register(Message)
admin.site.register(MessageAttachment)


# Register your models here.
