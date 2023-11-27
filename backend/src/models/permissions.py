# from sqlalchemy import ForeignKey, Integer, String
# from backend.src.models.base import Base
# from sqlalchemy.orm import mapped_column, Mapped


# class Permission(Base):
#     __tablename__ = 'permissions'

#     id: Mapped[int] = mapped_column(autoincrement=True)
#     name: Mapped[str] = mapped_column(String)
#     code_name: Mapped[int] = mapped_column(Integer)


# class UserPermissions(Base):
#     __tablename__ = 'user_permissions'

#     id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, unique=True)
#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
#     permission_id: Mapped[int] = mapped_column(Integer, ForeignKey('permissions.id'))
