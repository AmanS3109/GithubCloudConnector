from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # github_pat: str

    github_client_id: str
    github_client_secret: str

    class Config:
        env_file = ".env"

# We create a single instance of these settings to use throughout our app
settings = Settings()