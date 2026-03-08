from app.models import Conversation, ConversationParticipant, Message, User
from app.extensions import db
from datetime import datetime
from app.schemas.message_schema import MessageCreateSchema
from pydantic import ValidationError
from sqlalchemy import func


class MessageService:

    #Mensaje para enviar mensaje
    @staticmethod
    def send_message(data):

        try:
            validated_data = MessageCreateSchema(**data)
        except ValidationError as e:
            return {"error":"Datos invalidos"},400
        
        message = Message(
            conversation_id=validated_data.conversation_id,
            sender_id=validated_data.sender_id,
            content=validated_data.content
        )

        try:
            db.session.add(message)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error":str(e)},500
        
        return message,201


    #Metodo para obtener los mensajes
    @staticmethod
    def get_messages(conversation_id):

        return Message.query.filter_by(
            conversation_id=conversation_id
        ).order_by(Message.created_at.asc()).all()


    #Metodo para marcar como leido
    @staticmethod
    def mark_as_read(message_id):

        message = Message.query.get(message_id)

        if not message:
            return None,404

        message.read_at = datetime.utcnow()
        db.session.commit()

        return message,200


    # Crear u obtener conversación
    @staticmethod
    def get_or_create_conversation(user_id, technician_id):

        existing = (
            db.session.query(ConversationParticipant.conversation_id)
            .filter(
                ConversationParticipant.user_id.in_([user_id, technician_id])
            )
            .group_by(
                ConversationParticipant.conversation_id
            )
            .having(
                func.count(func.distinct(ConversationParticipant.user_id)) == 2
            )
            .first()
        )

        if existing:
            return Conversation.query.get(existing.conversation_id)

        new_conversation = Conversation()

        db.session.add(new_conversation)
        db.session.flush()

        participant1 = ConversationParticipant(
            conversation_id=new_conversation.id,
            user_id=user_id
        )

        participant2 = ConversationParticipant(
            conversation_id=new_conversation.id,
            user_id=technician_id
        )

        db.session.add(participant1)
        db.session.add(participant2)
        db.session.commit()

        return new_conversation


    #Metodo para obtener las conversaciones del usuario
    @staticmethod
    def get_user_conversations(user_id):

        conversations = (
            db.session.query(
                Conversation.id.label("conversation_id"),
                func.max(Message.created_at).label("last_message_time")
            )
            .join(
                ConversationParticipant,
                ConversationParticipant.conversation_id == Conversation.id
            )
            .outerjoin(
                Message,
                Message.conversation_id == Conversation.id
            )
            .filter(
                ConversationParticipant.user_id == user_id
            )
            .group_by(
                Conversation.id
            )
            .order_by(
                func.max(Message.created_at).desc()
            )
            .all()
        )

        result = []

        for conv in conversations:

            # obtener ultimo mensaje
            last_message = Message.query.filter_by(
                conversation_id=conv.conversation_id
            ).order_by(
                Message.created_at.desc()
            ).first()

            # obtener el otro participante (no el usuario actual)
            participants = ConversationParticipant.query.filter(
                ConversationParticipant.conversation_id == conv.conversation_id,
                ConversationParticipant.user_id != user_id
            ).first()

            # obtener datos del otro usuario
            other_user = User.query.get(participants.user_id) if participants else None

            result.append({

                "conversation_id": conv.conversation_id,
                "other_user_id": participants.user_id if participants else None,
                "other_user_name": other_user.full_name if other_user else None,
                "last_message": last_message.content if last_message else None,
                "last_message_time": conv.last_message_time

            })

        return result


    #Obtener una conversación
    @staticmethod
    def get_conversation(conversation_id):

        return Conversation.query.get(conversation_id)