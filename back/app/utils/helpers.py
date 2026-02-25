# app/utils/helper.py (o donde lo tengas)
from functools import wraps
from flask import request, jsonify, g
from app.utils.security import decode_token
from app.models.user import User
from app.extensions import db  # si usas session.get en SQLAlchemy 2.x
from app.models.user import User

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        # Validar esquema Bearer
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Token requerido (esquema Bearer)"}), 401

        token = parts[1]

        # Decodificar y validar el JWT
        payload = None
        try:
            payload = decode_token(token)  # debe validar exp, nbf, firma, etc.
        except Exception:
            # Si decode_token lanza, devuelve 401
            return jsonify({"error": "Token inválido o expirado"}), 401

        if not payload:
            return jsonify({"error": "Token inválido o expirado"}), 401

        # --- IMPORTANTE: alinear el claim con tu generate_token ---
        # Si en el token guardaste el id como 'sub' (recomendado por RFC7519):
        user_id = payload.get("user_id")
        # Si prefieres 'user_id', usa esta línea en su lugar:
        # user_id = payload.get("user_id")

        if not user_id:
            return jsonify({"error": "Token sin subject"}), 401

        # Recuperar usuario (elige una forma según tu stack)
        # Forma Flask-SQLAlchemy clásica:
        user = User.query.get(user_id)
        # Forma SQLAlchemy 2.x con session:
        # user = db.session.get(User, user_id)

        if user is None:
            return jsonify({"error": "Usuario no encontrado"}), 401

        # Dejar el usuario en el contexto global
        g.current_user = user

        # (Opcional) Inyectar también como kwarg:
        # kwargs["current_user"] = user

        return f(*args, **kwargs)

    return decorated

#Decorador para roles
def roles_required(*roles):
    #Gracias a este decorador el usuario solo puede hacer una accion si tiene el rol especifico
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = getattr(g, "current_user", None)

            if not user:
                return jsonify({"error": "Usuario no autenticado"}), 401

            if user.role not in roles:
                return jsonify({"error": "No autorizado"}), 403

            return f(*args, **kwargs)
        return decorated
    return wrapper
