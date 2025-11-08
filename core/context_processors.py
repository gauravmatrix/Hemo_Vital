# core/context_processors.py

from .models import GlobalSetting

def global_settings(request):
    """
    Make global settings available in all templates
    """
    try:
        settings = GlobalSetting.load()
        return {
            'global_settings': settings,
        }
    except Exception as e:
        # Return empty dict if settings not available
        return {
            'global_settings': None,
        }