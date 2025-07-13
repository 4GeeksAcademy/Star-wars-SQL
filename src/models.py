from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    subscription_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    profile_picture: Mapped[str] = mapped_column(String(120), nullable=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship(back_populates="user")
    favorite_planets: Mapped[list["FavoritePlanet"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "subscription_date": self.subscription_date,
            "profile_picture": self.profile_picture
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    age: Mapped[int] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(String(120), nullable=True)
    species: Mapped[str] = mapped_column(String(120), nullable=False)
    homeworld_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    homeworld: Mapped["Planet"] = relationship("Planet", back_populates="character_residents")
    height: Mapped[str] = mapped_column(String(120), nullable=True)
    hostility: Mapped[bool] = mapped_column(Boolean(), nullable=True)
    favorite_by_users: Mapped[list["FavoriteCharacter"]] = relationship(back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "species": self.species,
            "homeworld_id": self.homeworld_id,
            "homeworld_name": self.homeworld.name if self.homeworld else None,
            "height": self.height,
            "hostility": self.hostility
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=True)
    terrain: Mapped[str] = mapped_column(String(120), nullable=True)
    population: Mapped[str] = mapped_column(String(120), nullable=True)
    character_residents: Mapped[list["Character"]] = relationship("Character", back_populates="homeworld")
    gravity: Mapped[str] = mapped_column(String(120), nullable=True)
    can_a_human_live: Mapped[bool] = mapped_column(Boolean(), nullable=True)
    favorite_by_users: Mapped[list["FavoritePlanet"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "gravity": self.gravity,
            "can_a_human_live": self.can_a_human_live
        }


class FavoriteCharacter(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="favorite_characters")
    character: Mapped["Character"] = relationship(back_populates="favorite_by_users")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }


class FavoritePlanet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship(back_populates="favorite_by_users")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }
