from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_HOST: str
    MONGODB_DATABASE: str
    JWT_SECRET: str
    AWS_ENDPOINT_URL_S3: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_ENDPOINT_URL_S3: str
    AWS_ENDPOINT_URL_IAM: str
    AWS_REGION: str
    BUCKET_PHOTO: str
    JSON_LOG: bool
    # Gera a URL de conexão automaticamente
    @property
    def mongodb_url(self) -> str:
        return f"mongodb+srv://{self.MONGODB_USER}:{self.MONGODB_PASSWORD}@{self.MONGODB_HOST}"

    class Config:
        # Carrega o arquivo .env automaticamente
        env_file = ".env"
        extra = 'allow'


settings = Settings()
