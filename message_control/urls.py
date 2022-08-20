from rest_framework.routers import DefaultRouter
from .views import GenericFileUploadView, MessageView, MessageAttachmentView, ReadMultipleMessages
from django.urls import path, include
router = DefaultRouter()

router.register("file-upload", GenericFileUploadView)
router.register("messages", MessageView)
router.register("attach", MessageAttachmentView)

urlpatterns = [
    path("", include(router.urls)),
    path("read-messages/", ReadMultipleMessages.as_view()),
]
