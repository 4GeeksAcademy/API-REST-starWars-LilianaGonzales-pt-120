from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import List

db = SQLAlchemy()

# class User(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
#     password: Mapped[str] = mapped_column(nullable=False)
#     is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }


user_character = db.Table('users_characters',
                          db.Column('id', db.Integer, primary_key=True),
                          db.Column('user_id', db.Integer, db.ForeignKey(
                              "users.id"), nullable=False),
                          db.Column('character_id', db.Integer, db.ForeignKey(
                              "characters.id"), nullable=False),
                          db.Column('favorite', db.Boolean(), default=False)
                          )

user_vehicle = db.Table('users_vehicles',
                        db.Column('id', db.Integer, primary_key=True),
                        db.Column('user_id', db.Integer, db.ForeignKey(
                            "users.id"), nullable=False),
                        db.Column('vehicle_id', db.Integer, db.ForeignKey(
                            "vehicles.id"), nullable=False),
                        db.Column('favorite', db.Boolean(), default=False)
                        )

user_planet = db.Table('users_planets',
                       db.Column('id', db.Integer, primary_key=True),
                       db.Column('user_id', db.Integer, db.ForeignKey(
                           "users.id"), nullable=False),
                       db.Column('planet_id', db.Integer, db.ForeignKey(
                           "planets.id"), nullable=False),
                       db.Column('favorite', db.Boolean(), default=False)
                       )


class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    # subscription: Mapped[datetime] = mapped_column(DateTime,nullable=False)
    subscription: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc))

    characteres: Mapped[List["Character"]] = relationship(
        back_populates="users", secondary=user_character)
    vehicles:  Mapped[List["Vehicle"]] = relationship(
        back_populates="users", secondary=user_vehicle)
    planets: Mapped[List["Planet"]] = relationship(
        back_populates="users", secondary=user_planet)

    @classmethod
    def create(self, username, email, password):
        user = self(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
    
    def to_dict_all_data(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'characteres':[character.to_dict() for character in self.characteres]
        }


class Character (db.Model):
    __tablename__ = 'characters'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    # created_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc))

    list_vehicle: Mapped[List["Vehicle"]] = relationship(
        back_populates="character")

    users: Mapped[List["User"]] = relationship(
        back_populates="characteres", secondary=user_character)

    @classmethod
    def create(self, name, gender, height):
        character = self(name=name, gender=gender, height=height)
        db.session.add(character)
        db.session.commit()
        return character

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'height': self.height
        }
    
    def to_dict_all_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'height': self.height,
            'list_vehicle':[vehicle.to_dict() for vehicle in self.list_vehicle]
        }


class Planet (db.Model):
    __tablename__ = 'planets'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    climate: Mapped[str] = mapped_column(String(20), nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc))

    users: Mapped[List["User"]] = relationship(
        back_populates="planets", secondary=user_planet)


class Vehicle (db.Model):
    __tablename__ = 'vehicles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(20), nullable=False)
    passengers: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc))

    character_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("characters.id"), nullable=False)

    character: Mapped["Character"] = relationship(
        back_populates="list_vehicle")
    users: Mapped[List["User"]] = relationship(
        back_populates="vehicles", secondary=user_vehicle)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'passengers': self.passengers
        }
