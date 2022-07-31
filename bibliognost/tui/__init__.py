from curses import wrapper

from sqlalchemy.orm import sessionmaker

from bibliognost.tui.app import Application


def run(Session: sessionmaker):
    main = Application(Session)
    wrapper(main)
