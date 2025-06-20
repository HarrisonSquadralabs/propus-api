from pydantic_settings import BaseSettings, SettingsConfigDict
## Define the .env file settings for the application
class Settings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int
    ALGORITHM: str
    PROJECT_NAME: str 
    USER_DB: str
    HOST_DB: str
    PORT_DB: int
    USER_PASSWORD: str
    NAME_DB: str
    emails_enabled: bool 
    EMAILS_FROM_NAME: str          
    EMAILS_FROM_EMAIL: str                        
    SMTP_HOST: str                                
    SMTP_PORT: int                                
    SMTP_TLS: bool                          
    SMTP_SSL: bool                     
    SMTP_USER: str                                
    SMTP_PASSWORD: str    
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str  
    
    model_config = SettingsConfigDict(env_file=".env")
settings = Settings()
