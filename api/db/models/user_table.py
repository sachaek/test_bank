from sqlalchemy import Column, Integer, String, DateTime
from api.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    deleted_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}', deleted_at='{self.deleted_at}')>"
