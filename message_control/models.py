from django.db import models


class GenericFileUpload(models.Model) :
    file_upload = models.FileField(upload_to="files/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.file_upload}'

    
class Message(models.Model) :
    sender = models.ForeignKey(
        'control_user.CustomUser', related_name="message_sender", on_delete=models.CASCADE)
    reciever = models.ForeignKey(
        'control_user.CustomUser', related_name="message_receiver", on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.sender.username} : {self.message[:10]}'

    class Meta :
        ordering = ('-created_at',)


class MessageAttachment(models.Model) :
    message = models.ForeignKey(Message, related_name="message_attachments", on_delete=models.CASCADE)
    attachment = models.ForeignKey(GenericFileUpload, related_name="message_uploads", on_delete=models.CASCADE)
    caption = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta :
        ordering = ('-created_at',)