from django.apps import AppConfig #base class for configuraing app. allows to custom specific behaviour(auto-importing signals,setting app name)

class ApiConfig(AppConfig): #app name and default field types
    
    default_auto_field = 'django.db.models.BigAutoField' #default pk field for all models
    name = 'api' # app name. should match the app's folder name. uses to register and refer app internally

    def ready(self): #runs when jango starts the app
        import api.signals #ensures signal.py loaded when app starts