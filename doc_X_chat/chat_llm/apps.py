from django.apps import AppConfig


class LlmAiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chat_llm"

    def ready(self):
        import chat_llm.signals