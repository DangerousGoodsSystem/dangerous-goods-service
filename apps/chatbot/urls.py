from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, ConversationViewSet, MyConversationViewSet

router = DefaultRouter()
router.register(r'chat', ChatViewSet, basename='chat')
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'my-conversations', MyConversationViewSet, basename='my-conversations')

urlpatterns = [
    path('', include(router.urls)),
]