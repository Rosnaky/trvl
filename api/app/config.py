import os
import dotenv

dotenv.load_dotenv()

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

class Config:
    print("IN_DOCKER", os.environ.get("IN_DOCKER"))
    if os.environ.get("IN_DOCKER") == "TRUE":
        SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:{POSTGRES_PORT}/{POSTGRES_DB}"
    else:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@0.0.0.0:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    # disable to avoid overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False