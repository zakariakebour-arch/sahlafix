from app.extensions import db
from datetime import datetime

class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    #Relacion con participantes
    participants = db.relationship(
        "ConversationParticipant",
        backref="conversation",
        cascade="all, delete-orphan"
    )
       
    # Relación con mensajes
    messages = db.relationship(
        "Message",
        backref="conversation",
        cascade="all, delete-orphan"
    )