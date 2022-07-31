from curses import window, curs_set

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bibliognost.persistence import Collection, Work
from bibliognost.tui import views


class Application:
    def __init__(self, Session: sessionmaker):
        self._session = Session
        self._viewport = None

    def __call__(self, stdscr: window):
        stdscr.clear()
        curs_set(0)

        stdscr.box()
        stdscr.refresh()

        max_y, max_x = stdscr.getmaxyx()
        self._viewport = stdscr.derwin(max_y - 2, max_x - 2, 1, 1)
        view = self._open_collections_list()
        view.refresh()

        while True:
            key = stdscr.getkey()
            if key == "q":
                break
            elif key == "j":
                view.next()
            elif key == "k":
                view.previous()
            elif key == "c":
                view = self._open_collections_list()
            elif key == "w":
                view = self._open_works_list()
            view.refresh()

    def _open_collections_list(self) -> views.CollectionList:
        query = select(Collection).order_by(Collection.title)
        with self._session.begin() as session:
            collections = [
                views.CollectionListItem(id=c.collection_id, title=c.title)
                for c in session.execute(query).scalars().all()
            ]
            return views.CollectionList(self._viewport, collections)

    def _open_works_list(self) -> views.WorkList:
        query = select(Work).order_by(Work.title)
        with self._session.begin() as session:
            works = [
                views.WorkListItem(id=w.work_id, title=w.title)
                for w in session.execute(query).scalars().all()
            ]
            return views.WorkList(self._viewport, works)
