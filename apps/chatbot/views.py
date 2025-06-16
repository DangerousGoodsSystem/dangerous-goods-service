from django.apps import apps
from django.db.models import Subquery, OuterRef 
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import IsUser, IsStaffUser, DjangoModelPermissionsWithView
from .pagination import CustomPagination
from .models import Conversation, Message
from .serializers import ChatRequestSerializer, ChatResponseSerializer, ConversationSerializer, MessageSerializer
from .tasks import save_chat_history

chatbot = apps.get_app_config('apps.chatbot').chatbot

class ChatViewSet(viewsets.ViewSet):
    permission_classes = [IsUser]

    def post(self, request):
        request_serializer = ChatRequestSerializer(data=request.data)
        if request_serializer.is_valid():
            thread_id = request_serializer.validated_data['thread_id']
            message = request_serializer.validated_data['message']
            user_id = request.user.id
            config = {'configurable': {'thread_id': thread_id, 'stream_mode': 'updates'}}
            
            try:
                response = chatbot.ask(message, config=config)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            response_data = {
                'response': response['answer'],
                'context': [
                                {
                                    'id': str(doc.id),
                                    'metadata': doc.metadata,
                                    'page_content': doc.page_content
                                } for doc in response['documents']
                ]
            }

            save_chat_history.delay(
                user_id=user_id,
                thread_id=thread_id,
                user_message=message,
                bot_response=response['answer'],
                relevant_documents=response_data['context']
            )

            response_serializer = ChatResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                print(response_serializer.errors)
                return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ConversationViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.all()
    
    def list(self, request):
        queryset  = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        conversation = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(conversation, context={'request': request})
        return Response(serializer.data)

class MyConversationViewSet(viewsets.ViewSet):
    permission_classes = [IsUser]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        first_message_subquery = Subquery(
            Message.objects.filter(
                conversation=OuterRef('pk'),
                is_user=True
            ).order_by('timestamp').values('content')[:1]
        ) 
        queryset = Conversation.objects.filter(
            user_id=user.id,
            is_hidden=False
        ).annotate(
            first_user_message=first_message_subquery
        )
        return queryset
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        conversation = get_object_or_404(queryset, pk=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(conversation) 
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        conversation = get_object_or_404(queryset, pk=pk)
        conversation.is_hidden = True
        conversation.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
