from curses import A_STANDOUT, window
from dataclasses import dataclass
from typing import List


@dataclass
class CollectionListItem:
    id: int
    title: str


class CollectionList:
    def __init__(self, win: window, collections: List[CollectionListItem]):
        self._win = win
        self._collections = collections
        self.__current_ix = 0
        max_y, _ = self._win.getmaxyx()
        for ix, item in enumerate(self._collections):
            self._win.addstr(ix, 0, item.title)
            if ix >= max_y - 1:
                break
        self._highlight_current()

    @property
    def _current(self):
        return self.__current_ix

    @_current.setter
    def _current(self, value: int):
        if value != self.__current_ix:
            self._reset_current()
            self.__current_ix = value
            self._highlight_current()

    @property
    def _maxy(self) -> int:
        max_y, _ = self._win.getmaxyx()
        return max_y

    def _reset_current(self):
        if len(self._collections) == 0:
            return

        self._win.addstr(self.__current_ix, 0, self._collections[self._current].title)

    def _highlight_current(self):
        if len(self._collections) == 0:
            return

        self._win.addstr(
            self.__current_ix, 0, self._collections[self._current].title, A_STANDOUT
        )

    @property
    def has_next(self):
        return self._current < len(self._collections) - 1

    @property
    def has_previous(self):
        return self._current > 0

    def refresh(self):
        self._win.refresh()

    def next(self):
        if self.has_next:
            self._current += 1

    def previous(self):
        if self.has_previous:
            self._current -= 1
