import os

#Clase para configurar la conexion a la base de datos completa
class Config:
    # Clave secreta para JWT y sesiones
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")

    # Configuración de SQLAlchemy para MySQL
    DB_USER = os.environ.get("DB_USER")          # usuario MySQL
    DB_PASSWORD = os.environ.get("DB_PASSWORD")      # Contraseña MySQL
    DB_HOST = os.environ.get("DB_HOST","localhost")     # servidor MySQL
    DB_PORT = os.environ.get("DB_PORT",3306)            # puerto MySQL
    DB_NAME = os.environ.get("DB_NAME")      # nombre de la base de datos

    #URL dinamica segun los datos
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

