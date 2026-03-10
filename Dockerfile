#Imagen base python ligera
FROM python:3.11-slim

#Directorio de trabajo dentro del cotenedor
WORKDIR /app

#Copiar e instalar dependencias primero
COPY back/app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copiamos el codigo del backend
COPY back/ .

#Puerto interno de Flask
EXPOSE 5000

#Arrancamos la aplicacion
CMD ["python","run.py"]


