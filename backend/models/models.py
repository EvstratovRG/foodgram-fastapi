from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from backend.models.base import Base, TimeMixin


class User(TimeMixin, Base):
    __tablename__: str = "users"
    __table_args__ = (
        UniqueConstraint("username"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(length=150, nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    email: Mapped[str] = mapped_column(String(150), nullable=True)
    is_staff: Mapped[str] = mapped_column
