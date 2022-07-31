#!/usr/bin/env python3
import argparse
import os

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bibliognost import tui
from bibliognost.persistence import Collection, Work


library_path = os.getenv("BIBLIOGNOST_LIBRARY")
if library_path is None:
    raise RuntimeError("BIBLIOGNOST_LIBRARY environment variable must be set")
engine = create_engine(f"sqlite:///{library_path}")
Session = sessionmaker(engine)


def input_work() -> Work:
    title = input("Title: ")
    author = input("Author: ")
    type = input("Type: ")
    return Work(title=title, author=author, type=type)


def add_work():
    work = input_work()
    with Session.begin() as session:
        session.add(work)


def input_collection() -> Collection:
    title = input("Title: ")
    format = input("Format: ")
    return Collection(title=title, format=format)


def add_collection():
    collection = input_collection()
    with Session.begin() as session:
        session.add(collection)


def publish():
    work_id = int(input("Work id: "))
    collection_id = int(input("Collection id: "))
    with Session.begin() as session:
        work = session.execute(select(Work).where(Work.work_id == work_id)).scalar()
        collection = session.execute(
            select(Collection).where(Collection.collection_id == collection_id)
        ).scalar()
        work.publications.append(collection)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", choices=["add-work", "add-collection", "publish", "tui"]
    )
    args = parser.parse_args()

    if args.command == "add-work":
        add_work()
    elif args.command == "add-collection":
        add_collection()
    elif args.command == "publish":
        publish()
    elif args.command == "tui":
        tui.run(Session)


if __name__ == "__main__":
    main()
