from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_false
from datetime import date


class User(Base):
    id: Mapped[int_pk]
    username: Mapped[str_uniq]
    password: Mapped[str_null_false]
    coins: Mapped[int] = mapped_column(nullable=False, server_default=text('1000'))

    inventory: Mapped[list["UserItem"]] = relationship()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'coins': self.coins,
        }

class UserItem(Base):
    """Ассоциативная таблица многие-ко-многим"""
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)
    item: Mapped["Item"] = relationship()

    def to_dict(self):
        return {}

class Transfer(Base):
    """Модель для обмена монетами между пользователями многие-ко-многим"""
    id: Mapped[int_pk]
    from_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    to_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)

class Item(Base):
    """Модель товара мерча"""
    id: Mapped[int_pk]
    type: Mapped[str_null_false]
    cost: Mapped[int]

class Purchase(Base):
    """Модель для покупки товара"""
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False)

