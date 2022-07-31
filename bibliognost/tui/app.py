from curses import window, curs_set

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bibliognost.persistence import Collection
from bibliognost.tui import views


class Application:
    def __init__(self, Session: sessionmaker):
        self._session = Session

    def __call__(self, stdscr: window):
        stdscr.clear()
        curs_set(0)

        stdscr.box()
        stdscr.refresh()

        max_y, max_x = stdscr.getmaxyx()
        viewport = stdscr.derwin(max_y - 2, max_x - 2, 1, 1)
        view = self._open_collections_list(viewport)
        view.refresh()

        while True:
            key = stdscr.getkey()
            if key == "q":
                exit(0)
            if key == "j":
                view.next()
            if key == "k":
                view.previous()
            view.refresh()

    def _open_collections_list(self, stdscr: window) -> views.CollectionList:
        query = select(Collection).order_by(Collection.title)
        with self._session.begin() as session:
            collections = [
                views.CollectionListItem(id=c.collection_id, title=c.title)
                for c in session.execute(query).scalars().all()
            ]
            return views.CollectionList(stdscr, collections)
