from pydantic_settings import BaseSettings, SettingsConfigDict


'''При DEBUG = True, будут исопльзоваться мок сервера для внешних апи сервисов.
Смотри в mock_api/...'''

DEBUG = True


class Settings(BaseSettings):
    '''
    Конфигурация приложения:
    
    COMPLAINT_API_KEY: str
        Внутренний апи ключ. Используется для обращения из внешних сервисов. Пример:
        n8n отправляет запрос на закрытие заявки.

    API_LAYER_KEY: str
        Ключ api для Sentiment Analysis by APILayer - https://apilayer.com/marketplace/sentiment-analysis-api

    API_OPENAI_KEY: str
        Ключ api для Sentiment Analysis by OpenAI - https://platform.openai.com/docs/overview

    LAYER_ENDPOINT_URL, OPENAI_ENDPOINT_URL: str
        Эндпоинты сторонних апи сервисов
    '''
    COMPLAINT_API_KEY: str
    API_LAYER_KEY: str
    API_OPENAI_KEY: str
    LAYER_ENDPOINT_URL: str
    OPENAI_ENDPOINT_URL: str

    model_config = SettingsConfigDict(env_file=".env.debug")
    

def get_settings() -> Settings:

    env = 'prod' if not DEBUG else 'debug'
    env_file = f".env.{env}"
    
    class DynamicSettings(Settings):
        model_config = SettingsConfigDict(env_file=env_file)
    
    settings = DynamicSettings()
    return settings


settings = get_settings()