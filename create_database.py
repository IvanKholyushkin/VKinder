import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    found_user_id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    user_id = sq.Column(sq.Integer, nullable=False)
    first_name = sq.Column(sq.String(length=40), nullable=False)
    last_name = sq.Column(sq.String(length=40), nullable=False)
    gender = sq.Column(sq.String(length=10))
    age = sq.Column(sq.Integer, nullable=False)
    city = sq.Column(sq.String(length=40))


class LikedUsers(Base):
    __tablename__ = "liked_users"

    liked_users_id = sq.Column(
        sq.Integer, sq.ForeignKey("users.found_user_id"), primary_key=True
    )
    user_id = sq.Column(sq.Integer, nullable=False)
    first_name = sq.Column(sq.String(length=40), nullable=False)
    last_name = sq.Column(sq.String(length=40), nullable=False)
    age = sq.Column(sq.Integer, nullable=False)
    city = sq.Column(sq.String(length=40))

    user = relationship(Users, backref="liked_users")


class Photos(Base):
    __tablename__ = "photos"

    id = sq.Column(sq.Integer, primary_key=True)
    liked_users_id = sq.Column(
        sq.Integer, sq.ForeignKey("liked_users.liked_users_id"), nullable=False
    )
    photo_link_1 = sq.Column(sq.String(length=200), nullable=False)
    photo_link_2 = sq.Column(sq.String(length=200), nullable=False)
    photo_link_3 = sq.Column(sq.String(length=200), nullable=False)

    liked_user = relationship("LikedUsers", backref="photos")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
