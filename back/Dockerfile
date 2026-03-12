#Imagen base python ligera
FROM python:3.11-slim

#Directorio de trabajo dentro del cotenedor
WORKDIR /app

#Copiar e instalar dependencias primero
COPY back/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copiamos el codigo del backend
COPY back/ .

#Exponemos el puerto 8000
EXPOSE 8000

#Arrancamos la aplicacion con gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "run:app"]


