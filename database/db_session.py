import sqlalchemy as sa
from sqlalchemy import text, String, ForeignKey, select
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase

session = None


class DataBase(DeclarativeBase):
	pass


class User(DataBase):
	__tablename__ = "users"
	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column()
	token: Mapped[str] = mapped_column(String(40))

	repositories: Mapped[List["Repository"]] = relationship(back_populates="user")


class Repository(DataBase):
	__tablename__ = "repositories"
	id: Mapped[int] = mapped_column(primary_key=True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	repository_id: Mapped[int] = mapped_column()
	repository_name: Mapped[str] = mapped_column()
	owner_name: Mapped[str] = mapped_column()
	files: Mapped[str] = mapped_column()

	user: Mapped[User] = relationship(back_populates="repositories")


DBNAME = "database.sqlite"


def get_session() -> Session:
	global session
	if session is None:
		engine = sa.create_engine(f'sqlite+pysqlite:///{DBNAME}')
		DataBase.metadata.create_all(engine)
		session = Session(engine)
	return session


get_session()
