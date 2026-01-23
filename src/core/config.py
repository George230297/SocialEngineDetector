from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "social-eng-detector"
    API_VERSION: str = "v1"
    
    # Simulación de API Keys (pueden venir de variables de entorno)
    VIRUSTOTAL_API_KEY: str = "vt-simulated-key-12345"
    OPENAI_API_KEY: str = "sk-simulated-key-abcde"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8", 
        case_sensitive=True
    )

settings = Settings()
