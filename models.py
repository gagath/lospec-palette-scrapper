#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2022 Agathe Porte <microjoe@microjoe.org>
#
# SPDX-License-Identifier: MIT

from xmlrpc.client import Boolean, DateTime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
import sqlalchemy
from sqlalchemy.orm import registry, relationship


mapper_registry = registry()


@mapper_registry.mapped
class Palette:
    __tablename__ = "palette"

    hashtag = Column(String, primary_key=True)
    lospec_id = Column(String)
    likes = Column(Integer)
    downloads = Column(Integer)
    # featured = Column(Boolean)
    # comments = relationship(...)
    title = Column(String, nullable=False)
    description = Column(String)
    creator = Column(Boolean)
    slug = Column(String)
    published_at = Column(DateTime)
    # user = relationship(...)
    number_of_colors = Column(Integer)
    created_at = Column(DateTime)
    is_new = Column(Boolean)
    # sort_newest = Column(DateTime)
    # examples = relationship(...)

    tags = relationship("Tag", back_populates="palette")


@mapper_registry.mapped
class Tag:
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    palette_hashtag = Column(String, ForeignKey("palette.hashtag"))
    name = Column(String)

    palette = relationship("Palette", back_populates="tags")


def create_db_memory(echo=False):
    from sqlalchemy import create_engine

    engine = create_engine("sqlite+pysqlite:///:memory:", echo=echo, future=True)
    mapper_registry.metadata.create_all(engine)

    return engine


def create_db(echo=False):
    from sqlalchemy import create_engine

    engine = create_engine(
        f"sqlite+pysqlite:///lospec-palettes.sqlite", echo=echo, future=True
    )
    mapper_registry.metadata.create_all(engine)

    return engine


def import_palette(session, path):
    import json

    with path.open() as f:
        doc = json.load(f)

    assert doc["hashtag"] == path.stem

    print(f"IMPORT {path.stem}")

    from dateutil.parser import isoparse

    tmp = dict(
        hashtag=doc["hashtag"],
        lospec_id=doc["_id"],
        likes=doc["likes"],
        title=doc["title"],
        description=doc["description"],
        creator=bool(doc.get("creator")),  # sometimes, creator=1
        slug=doc["slug"],
        published_at=isoparse(doc["publishedAt"]),
        number_of_colors=doc["numberOfColors"],
        created_at=isoparse(doc["createdAt"]),
        is_new=doc["isNew"],
        downloads=int(doc["downloads"].replace(",", ""))
        # sort_newest=doc["sortNewest"],
    )

    try:
        obj = Palette(**tmp)
        session.merge(obj)
    except sqlalchemy.exc.StatementError:
        import pprint

        pprint.pprint(tmp)
        raise


def populate_db(engine, sample=False):
    from sqlalchemy.orm import Session
    from pathlib import Path

    session = Session(engine)

    for path in Path("./palettes").glob("**/*.json"):
        import_palette(session, path)
        if sample:
            break

    session.commit()


if __name__ == "__main__":
    engine = create_db()
    populate_db(engine)
