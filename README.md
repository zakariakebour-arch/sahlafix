  SahlaFix

SahlaFix es una aplicación MVP diseñada para conectar clientes con técnicos de confianza de forma rápida y sencilla. La plataforma centraliza la búsqueda de profesionales según necesidad y ubicación, eliminando la fricción de métodos tradicionales como Google, WhatsApp o recomendaciones informales.

Enfocada inicialmente en el público argelino.

Demo: https://sahlafix.es

Repo: https://lnkd.in/ewKK7izN

Problema que resuelve

Encontrar un técnico fiable cerca de ti suele ser un proceso lento e ineficiente:

Búsquedas poco precisas en Google
Dependencia de recomendaciones informales
Grupos de WhatsApp saturados

SahlaFix centraliza todo en una única plataforma donde puedes:

Buscar técnicos por categoría y zona
Comparar perfiles
Contactar directamente
  Funcionalidades principales
  Búsqueda de técnicos por nombre y categoría
  Geolocalización mediante latitud y longitud
  Sistema de roles:
Admin
Técnico
Cliente
  Subida de fotos de perfil (AWS S3)
  Autenticación stateless con JWT
  API versionada (/api/v1)
  Diseño completamente responsive
  Arquitectura

El backend sigue una arquitectura en capas, pensada para escalabilidad y mantenibilidad:

├── models     → Definición de entidades (SQLAlchemy ORM)
├── schemas    → Validación de datos (Pydantic)
├── services   → Lógica de negocio
├── routes     → Endpoints API (/api/v1)

Stack tecnológico
Backend
Python + Flask
SQLAlchemy (ORM)
Pydantic (validación)
JWT (autenticación)
Gunicorn
Frontend
HTML
CSS
JavaScript (Vanilla)

Sin frameworks: control total del flujo de datos y renderizado.

Infraestructura (AWS)
EC2 (Ubuntu Server) → servidor gestionado por SSH
S3 → almacenamiento de imágenes de perfil
Docker → contenedores:
MySQL
Nginx
Backend
Nginx → proxy inverso
Despliegue

El proyecto está completamente dockerizado:

docker-compose up --build

Incluye:

Base de datos MySQL
Backend Flask
Nginx como reverse proxy

Autenticación
Basada en JWT (JSON Web Tokens)
Stateless → escalable sin sesiones en servidor

API
Estructura versionada: /api/v1/
Endpoints organizados y desacoplados
Preparada para futuras versiones sin romper el cliente

Frontend
Comunicación asíncrona con API REST
Diseño responsive (mobile-first)
Sin dependencias externas
  Aprendizajes clave

Este proyecto no solo es funcional, también ha sido una experiencia completa de desarrollo real:

Diseño de arquitectura escalable
Gestión de servidores en producción
Debugging en entorno live
Despliegue completo en AWS
Pensar como producto, no solo como desarrollador
  Estado del proyecto

  MVP funcional en producción
  Mejoras futuras:

Sistema de valoraciones
Chat en tiempo real
Filtros avanzados
Panel admin más completo
  Contribuciones y feedback


Python Flask AWS Docker Backend WebDevelopment
