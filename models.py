#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry, relationship


mapper_registry = registry()


@mapper_registry.mapped
class Palette:
    __tablename__ = "palette"

    id = Column(Integer, primary_key=True)
    original_id = Column(String)

    tags = relationship("Tag", back_populates="palette")


@mapper_registry.mapped
class Tag:
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    palette_id = Column(Integer, ForeignKey("palette.id"))

    palette = relationship("Palette", back_populates="palette")


if __name__ == "__main__":
    from sqlalchemy import create_engine

    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
    mapper_registry.metadata.create_all(engine)
