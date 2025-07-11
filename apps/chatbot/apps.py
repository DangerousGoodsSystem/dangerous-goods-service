from django.apps import AppConfig


class ChatbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.chatbot'

    def ready(self):
        from .rag.chatbot import Chatbot
        self.chatbot = Chatbot()
        self.chatbot.setup_workflow()
