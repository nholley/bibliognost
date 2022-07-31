import math
from curses import A_STANDOUT, window
from dataclasses import dataclass
from typing import List


class _PagedList:
    def __init__(self, items, page_size: int):
        self._items = items
        self._current_page = 0
        self._page_size = page_size

    @property
    def total_pages(self) -> int:
        return math.ceil(len(self._items) / self._page_size)

    @property
    def current_page(self) -> int:
        """The current page number"""
        return self._current_page

    @current_page.setter
    def current_page(self, value: int):
        if value in range(self.total_pages):
            self._current_page = value

    @property
    def current_items(self) -> List:
        """Items on the current page"""
        low = self.current_page * self._page_size
        high = low + self._page_size
        return self._items[low:high]

    @property
    def has_next(self) -> bool:
        return self.current_page < (self.total_pages - 1)

    @property
    def has_previous(self) -> bool:
        return self.current_page > 0


class _PagedListView:
    def __init__(self, win: window, items, item_repr):
        self._win = win
        self._item_repr = item_repr
        self._paged_items = _PagedList(items, self.page_size)
        self._ix_relative = 0
        self._display_page()

    def _display_page(self):
        self._win.clear()
        for ix, item in enumerate(self._paged_items.current_items):
            self._win.addstr(ix, 0, self._item_repr(item))
        self._highlight_current()

    @property
    def current(self) -> int:
        """Index of the currently row"""
        return self._ix_relative

    @current.setter
    def current(self, value: int):
        if value != self._ix_relative:
            if value < 0:
                self._paged_items.current_page -= 1
                self._ix_relative = self._paged_items._page_size - 1
                self._display_page()
            elif value >= self.page_size:
                self._paged_items.current_page += 1
                self._ix_relative = 0
                self._display_page()
            else:
                self._reset_current()
                self._ix_relative = value
                self._highlight_current()

    @property
    def page_size(self) -> int:
        max_y, _ = self._win.getmaxyx()
        return max_y

    def _repr_for(self, ix: int) -> str:
        return self._item_repr(self._paged_items.current_items[ix])

    def _reset_current(self):
        """Remove highlighting from the current line"""
        if self._paged_items.total_pages == 0:
            return

        self._win.addstr(self.current, 0, self._repr_for(self.current))

    def _highlight_current(self):
        """Add highlighting to the current line"""
        if self._paged_items.total_pages == 0:
            return

        self._win.addstr(self.current, 0, self._repr_for(self.current), A_STANDOUT)

    @property
    def has_next(self) -> bool:
        return (
            self._ix_relative < (len(self._paged_items.current_items) - 1)
            or self._paged_items.has_next
        )

    @property
    def has_previous(self) -> bool:
        return self._ix_relative > 0 or self._paged_items.has_previous

    def refresh(self):
        self._win.refresh()

    def next(self):
        if self.has_next:
            self.current += 1

    def previous(self):
        if self.has_previous:
            self.current -= 1


@dataclass
class CollectionListItem:
    id: int
    title: str


class CollectionList:
    def __init__(self, win: window, works: List[CollectionListItem]):
        self._view = _PagedListView(win, works, lambda it: it.title)

    @property
    def has_next(self):
        return self._view.has_next

    @property
    def has_previous(self):
        return self._view.has_previous

    def refresh(self):
        self._view.refresh()

    def next(self):
        self._view.next()

    def previous(self):
        self._view.previous()


@dataclass
class WorkListItem:
    id: int
    title: str


class WorkList:
    def __init__(self, win: window, works: List[WorkListItem]):
        self._view = _PagedListView(win, works, lambda w: w.title)

    @property
    def has_next(self):
        return self._view.has_next

    @property
    def has_previous(self):
        return self._view.has_previous

    def refresh(self):
        self._view.refresh()

    def next(self):
        self._view.next()

    def next_page(self):
        self._view.next_page()

    def previous(self):
        self._view.previous()

    def previous_page(self):
        self._view.previous_page()
