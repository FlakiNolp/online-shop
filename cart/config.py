import os


DB_USER: str = 'postgres'#os.getenv("DB_USER")
DB_PORT: int = 5432#int(os.getenv("DB_PORT"))
DB_HOST: str = 'localhost'#os.getenv("DB_HOST")
DB_PASSWORD: str = 'postgres'#os.getenv("DB_PASSWORD")
DB_NAME: str = 'masha'
SECRET_KEY: str = 'ok'
ALGORITHM: str = 'HS256'
MONGO_USER = ''#getenv("MONGO_USER")
MONGO_PASSWORD = ''#getenv("MONGO_PASSWORD")
MONGO_HOST = 'localhost'#getenv("MONGO_HOST", "192.168.151.68")
MONGO_PORT = 27017#getenv("MONGO_PORT", 27017)