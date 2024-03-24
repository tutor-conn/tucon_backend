from typing import Optional
from sqlalchemy import Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    last_view: Mapped[str] = mapped_column(String)

    profile = relationship("Profile", back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    profile_type: Mapped[str] = mapped_column(String)
    # optional fields
    bio: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    pay_rate1: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    pay_rate2: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    user = relationship("User", back_populates="profile")
    messages_sent = relationship(
        "Message",
        back_populates="sender",
        primaryjoin="Profile.id == Message.sender_id",
    )
    messages_received = relationship(
        "Message",
        back_populates="recipient",
        primaryjoin="Profile.id == Message.recipient_id",
    )

    __table_args__ = (UniqueConstraint("user_id", "profile_type"),)


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"))
    recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"))
    content: Mapped[str] = mapped_column(String)
    timestamp: Mapped[str] = mapped_column(String)

    sender = relationship(
        "Profile", back_populates="messages_sent", foreign_keys=[sender_id]
    )
    recipient = relationship(
        "Profile", back_populates="messages_received", foreign_keys=[recipient_id]
    )
