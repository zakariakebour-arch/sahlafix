# app/utils/security.py
import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app
# from uuid import uuid4  # si quieres jti

ALGORITHM = "HS256"

def _utcnow():
    # Usar tiempo "aware" en UTC
    return datetime.now(timezone.utc)

def generate_token(user):
    """Genera un access token con claims mínimos y expiración."""
    exp_hours = current_app.config.get("JWT_EXPIRATION_HOURS", 24)
    now = _utcnow()
    payload = {
        "user_id": user.id,           # si prefieres estándar, usa "sub": str(user.id)
        "role": user.role,            # útil para RBAC simple
        "iat": now,                   # issued at
        "nbf": now,                   # not before (válido desde ahora)
        "exp": now + timedelta(hours=exp_hours),
        # "jti": str(uuid4()),        # opcional: para listas de revocación
        # "iss": "tu-api",            # opcional: issuer
        # "aud": "tu-frontend",       # opcional: audience
    }

    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm=ALGORITHM)
    # En PyJWT>=2, token ya es str. Si fuera bytes (versiones muy antiguas), decodifica:
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token

def decode_token(token: str):
    """Decodifica y valida el JWT. Devuelve el payload o None si no es válido."""
    try:
        # Permite pequeño margen por desfase horario
        leeway_seconds = current_app.config.get("JWT_LEEWAY_SECONDS", 10)

        options = {
            "require": ["exp", "iat"],  # exige que existan exp e iat
        }

        payload = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=[ALGORITHM],
            options=options,
            leeway=leeway_seconds,
            # audience="tu-frontend",  # si usas aud en generate_token
            # issuer="tu-api",         # si usas iss en generate_token
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None