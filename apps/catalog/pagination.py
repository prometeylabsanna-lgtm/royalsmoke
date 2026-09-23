"""Stable catalog pagination: out-of-range page → empty list (not 404)."""

from __future__ import annotations

from django.core.paginator import Paginator

CATALOG_PAGE_SIZE = 24


class OutOfRangePage:
    """Page-like object when ?page=N is beyond current result set."""

    def __init__(self, paginator: Paginator, number: int):
        self.paginator = paginator
        self.number = number
        self.object_list = []
        self.out_of_range = True

    def __len__(self):
        return 0

    def __getitem__(self, index):
        return self.object_list[index]

    def has_other_pages(self):
        return self.paginator.num_pages > 1

    def has_previous(self):
        return self.paginator.num_pages >= 1

    def has_next(self):
        return False

    def previous_page_number(self):
        return self.paginator.num_pages if self.paginator.num_pages else 1

    def next_page_number(self):
        return self.number

    @property
    def start_index(self):
        return 0

    @property
    def end_index(self):
        return 0


def parse_page_number(raw) -> int:
    try:
        page = int(str(raw).strip())
    except (TypeError, ValueError, AttributeError):
        return 1
    return page if page >= 1 else 1


def paginate_catalog(queryset, page_raw, *, per_page: int = CATALOG_PAGE_SIZE):
    """Return (products_list, page_obj). Out-of-range → empty products, no exception."""
    page_number = parse_page_number(page_raw)
    paginator = Paginator(queryset, per_page)
    if paginator.count == 0:
        return [], OutOfRangePage(paginator, 1)
    if page_number > paginator.num_pages:
        return [], OutOfRangePage(paginator, page_number)
    page_obj = paginator.page(page_number)
    page_obj.out_of_range = False  # type: ignore[attr-defined]
    return list(page_obj.object_list), page_obj
