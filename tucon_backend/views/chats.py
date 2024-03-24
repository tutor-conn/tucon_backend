from flask_pydantic import validate
from pydantic import BaseModel
from tucon_backend import app
from datetime import datetime, timedelta

from tucon_backend.middlewares.auth import login_required
from tucon_backend.models import Message

now = datetime.now()
two_hours_ago = now - timedelta(hours=2)
four_hours_ago = now - timedelta(hours=4)
yesterday = now - timedelta(days=1)
last_week = now - timedelta(weeks=1)
eight_weeks_ago = now - timedelta(weeks=8)

contacts = [
    {
        "id": 1,
        "name": "Alice Freeman",
        "avatarUrl": "https://i.pravatar.cc/150?u=1",
        "timestamp": now.isoformat(),
    },
    {
        "id": 2,
        "name": "Timothy Reynold",
        "avatarUrl": "https://i.pravatar.cc/150?u=2",
        "timestamp": two_hours_ago.isoformat(),
    },
    {
        "id": 3,
        "name": "Charlotte Mack",
        "avatarUrl": "https://i.pravatar.cc/150?u=3",
        "timestamp": last_week.isoformat(),
    },
    {
        "id": 4,
        "name": "Isabella Fisher",
        "avatarUrl": "https://i.pravatar.cc/150?u=4",
        "timestamp": eight_weeks_ago.isoformat(),
    },
    {
        "id": 5,
        "name": "Kristopher Johnson",
        "avatarUrl": "https://i.pravatar.cc/150?u=5",
        "timestamp": yesterday.isoformat(),
    },
    {
        "id": 6,
        "name": "Amanda Young",
        "avatarUrl": "https://i.pravatar.cc/150?u=6",
        "timestamp": eight_weeks_ago.isoformat(),
    },
    {
        "id": 7,
        "name": "Evelyn Green",
        "avatarUrl": "https://i.pravatar.cc/150?u=7",
        "timestamp": eight_weeks_ago.isoformat(),
    },
    {
        "id": 8,
        "name": "Landon Rodriguez",
        "avatarUrl": "https://i.pravatar.cc/150?u=8",
        "timestamp": eight_weeks_ago.isoformat(),
    },
    {
        "id": 9,
        "name": "Dylan Russell",
        "avatarUrl": "https://i.pravatar.cc/150?u=9",
        "timestamp": eight_weeks_ago.isoformat(),
    },
    {
        "id": 10,
        "name": "Kaitlyn Anderson",
        "avatarUrl": "https://i.pravatar.cc/150?u=10",
        "timestamp": eight_weeks_ago.isoformat(),
    },
    {
        "id": 11,
        "name": "Lila White",
        "avatarUrl": "https://i.pravatar.cc/150?u=11",
        "timestamp": eight_weeks_ago.isoformat(),
    },
    {
        "id": 12,
        "name": "Jennifer Reid",
        "avatarUrl": "https://i.pravatar.cc/150?u=12",
        "timestamp": eight_weeks_ago.isoformat(),
    },
    {
        "id": 13,
        "name": "Suzanne Taylor",
        "avatarUrl": "https://i.pravatar.cc/150?u=13",
        "timestamp": eight_weeks_ago.isoformat(),
    },
    {
        "id": 14,
        "name": "John Ross",
        "avatarUrl": "https://i.pravatar.cc/150?u=14",
        "timestamp": eight_weeks_ago.isoformat(),
    },
    {
        "id": 15,
        "name": "Don Gordon",
        "avatarUrl": "https://i.pravatar.cc/150?u=15",
        "timestamp": eight_weeks_ago.isoformat(),
    },
    {
        "id": 16,
        "name": "Rebecca Stuart",
        "avatarUrl": "https://i.pravatar.cc/150?u=16",
        "timestamp": eight_weeks_ago.isoformat(),
    },
]

strings = [
    "Hi, I'm Alice! I teach Math and Computer Science at the University level. I'm available for tutoring on weekends.",
    "Tell me about yourself and what you're looking for.",
    "Hey Alice, I'm a student at the University of Guelph and I'm struggling with my Computer Science course. I'm looking for a tutor to help me with my assignments and prepare for my exams. I'm available on weekends too.",
    "Great! I can help you with that. What year are you in and what course are you struggling with?",
]

demo_messages = [
    # For demo, user has id=0
    Message(
        id=1,
        sender_id=1,
        recipient_id=0,
        content=strings[0],
        timestamp=four_hours_ago.isoformat(),
    ),
    Message(
        id=2,
        sender_id=1,
        recipient_id=0,
        content=strings[1],
        timestamp=four_hours_ago.isoformat(),
    ),
    Message(
        id=3,
        sender_id=0,
        recipient_id=1,
        content=strings[2],
        timestamp=two_hours_ago.isoformat(),
    ),
    Message(
        id=4, sender_id=0, recipient_id=1, content=strings[3], timestamp=now.isoformat()
    ),
]


@app.route("/chats", methods=["GET"])
@login_required
def get_chats(user_id: int):
    contacts_sorted_by_time = list(
        sorted(contacts, key=lambda chat: chat["timestamp"], reverse=True)
    )
    return contacts_sorted_by_time


@app.route("/chats/<recipient_id>/messages", methods=["GET"])
@login_required
@validate()
def get_chat_messages(user_id: int, recipient_id: int):
    # For demo, user has id=0
    user_id = 0

    def filter_message(message: Message):
        return (
            message.sender_id == user_id and message.recipient_id == recipient_id
        ) or (message.sender_id == recipient_id and message.recipient_id == user_id)

    def map_message(message: Message):
        return {
            "id": message.id,
            "from": "me" if message.sender_id == user_id else "them",
            "content": message.content,
            "timestamp": message.timestamp,
        }

    messages = demo_messages
    messages = list(filter(filter_message, messages))
    messages = list(map(map_message, messages))

    return messages


class CreateMessageBody(BaseModel):
    content: str


@app.route("/chats/<recipient_id>/messages", methods=["POST"])
@login_required
@validate()
def post_chat_messages(user_id: int, recipient_id: int, body: CreateMessageBody):
    # For demo, user has id=0
    user_id = 0

    now_timestamp = datetime.now().isoformat()
    demo_messages.append(
        Message(
            id=len(demo_messages) + 1,
            sender_id=user_id,
            recipient_id=recipient_id,
            content=body.content,
            timestamp=now_timestamp,
        )
    )
    contacts[recipient_id - 1]["timestamp"] = now_timestamp

    return {"message": "Message sent successfully"}, 201
