from flask import Blueprint, request, jsonify
from app.services.message_service import MessageService
from app.utils.helpers import jwt_required
from app.models.technician import Technician  # IMPORTANTE: para convertir technician_id -> user_id

# Creamos el endpoint base
message_bp = Blueprint("message_v1", __name__, url_prefix="/api/v1/message")

# Ruta para enviar mensaje
@message_bp.route("/messages", methods=["POST"])
@jwt_required
def send_message():

    data = request.json

    result = MessageService.send_message(data)

    # Si el service devolvió error
    if isinstance(result, tuple) and isinstance(result[0], dict):
        return jsonify(result[0]), result[1]

    message, status = result

    return jsonify({
        "id": message.id,
        "conversation_id": message.conversation_id,
        "sender_id": message.sender_id,
        "content": message.content,
        "created_at": message.created_at.isoformat()
    }), status


# Ruta para obtener mensajes de una conversacion
@message_bp.route("/conversations/<int:conversation_id>/messages", methods=["GET"])
@jwt_required
def get_messages(conversation_id):

    messages = MessageService.get_messages(conversation_id)

    result = []

    for m in messages:
        result.append({
            "id": m.id,
            "conversation_id": m.conversation_id,
            "sender_id": m.sender_id,
            "content": m.content,
            "created_at": m.created_at.isoformat(),
            "read_at": m.read_at.isoformat() if m.read_at else None
        })

    return jsonify(result), 200


# Ruta para marcar mensaje como leido
@message_bp.route("/messages/<int:message_id>/read", methods=["PATCH"])
@jwt_required
def mark_as_read(message_id):

    message, status = MessageService.mark_as_read(message_id)

    if not message:
        return jsonify({"error": "Mensaje no encontrado"}), 404

    return jsonify({
        "message": "Mensaje marcado como leido"
    }), status


# Ruta para crear o obtener conversacion
@message_bp.route("/conversations", methods=["POST"])
@jwt_required
def get_conversation():

    data = request.json
    user_id = data.get("user_id")
    technician_id = data.get("technician_id")

    technician = Technician.query.get(technician_id)
    if not technician:
        return jsonify({"error": "Tecnico no encontrado"}), 404

    technician_user_id = technician.user_id

    # Evitar que el usuario se contacte a si mismo
    if str(user_id) == str(technician_user_id):
        return jsonify({"error": "No puedes contactarte a ti mismo"}), 403

    result = MessageService.get_or_create_conversation(
        user_id,
        technician_user_id,
        technician
    )

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"conversation_id": result.id}), 200


# Ruta para obtener conversaciones de un usuario
@message_bp.route("/conversations/user/<int:user_id>", methods=["GET"])
def get_conversations(user_id):

    conversations = MessageService.get_user_conversations(user_id)

    result = []

    for c in conversations:
        result.append({
            "conversation_id": c["conversation_id"],
            "other_user_id": c["other_user_id"],
            "other_user_name": c["other_user_name"],
             "other_user_image": c.get("other_user_image"),
            "last_message": c["last_message"],
            "last_message_time": c["last_message_time"].isoformat() if c["last_message_time"] else None
        })

    return jsonify(result), 200


# Ruta para obtener conversacion especifica
@message_bp.route("/conversations/<int:conversation_id>", methods=["GET"])
@jwt_required
def get_conversation_by_id(conversation_id):

    conversation = MessageService.get_conversation(conversation_id)

    if not conversation:
        return jsonify({"error": "Conversacion no encontrada"}), 404

    return jsonify({
        "conversation_id": conversation.id,
        "created_at": conversation.created_at.isoformat()
    }), 200

