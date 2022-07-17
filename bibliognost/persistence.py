from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


work_collection_table = Table(
    "work_collection",
    Base.metadata,
    Column("work_id", ForeignKey("work.work_id"), primary_key=True),
    Column("collection_id", ForeignKey("collection.collection_id"), primary_key=True),
)


class Work(Base):
    __tablename__ = "work"

    work_id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    type = Column(String)

    publications = relationship(
        "Collection", secondary=work_collection_table, back_populates="contents"
    )


class Collection(Base):
    __tablename__ = "collection"

    collection_id = Column(Integer, primary_key=True)
    title = Column(String)
    format = Column(String)

    contents = relationship(
        "Work", secondary=work_collection_table, back_populates="publications"
    )
