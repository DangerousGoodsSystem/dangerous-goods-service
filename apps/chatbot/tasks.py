from celery import shared_task
from .models import Conversation, Message

@shared_task
def save_chat_history(user_id, thread_id, user_message, bot_response, relevant_documents):
    conversation, created = Conversation.objects.get_or_create(
        user_id=user_id,
        thread_id=thread_id
    )
    
    Message.objects.create(
        conversation=conversation,
        content=user_message,
        is_user=True 
    )

    Message.objects.create(
        conversation=conversation,
        content=bot_response,
        is_user=False,
        relevant_chunks=relevant_documents
    )
    
    return f"Saved chat history for user {user_id} in thread {thread_id}"