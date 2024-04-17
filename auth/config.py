import os


DB_USER: str = 'postgres'#os.getenv("DB_USER")
DB_PORT: int = 5432#int(os.getenv("DB_PORT"))
DB_HOST: str = 'localhost'#os.getenv("DB_HOST")
DB_PASSWORD: str = 'postgres'#os.getenv("DB_PASSWORD")
DB_NAME: str = 'masha'
SECRET_KEY: str = 'ok'
ALGORITHM: str = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
REFRESH_TOKEN_EXPIRE_HOURS: int = 24