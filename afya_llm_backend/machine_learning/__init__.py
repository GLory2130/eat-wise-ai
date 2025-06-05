from django.apps import AppConfig

class MachineLearningConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'machine_learning'

    def ready(self):
        """
        Initialize app when Django starts
        """
        import os
        from django.conf import settings

        # Check required environment variables
        required_vars = [
            "DEEPINFRA_API_TOKEN",
            "DEEPINFRA_LANG_MODEL",
            "DEEPINFRA_EMBEDDING_MODEL"
        ]

        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        if missing_vars:
            raise NameError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                "Please check your .env file."
            ) 