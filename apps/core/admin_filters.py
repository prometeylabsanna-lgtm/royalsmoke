"""Unfold changelist filters as top dropdowns without the «За …» prefix."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.core.validators import EMPTY_VALUES
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin.dropdown_filters import (
    ChoicesDropdownFilter,
    RelatedDropdownFilter,
)
from unfold.contrib.filters.admin.mixins import DropdownMixin, ValueMixin
from unfold.contrib.filters.forms import DropdownForm


def dropdown_filter_options(
    *field_paths: str,
    labels: dict[str, str] | None = None,
) -> dict[str, dict[str, Any]]:
    """Mark filters as horizontal (top bar); optional custom labels."""
    labels = labels or {}
    options: dict[str, dict[str, Any]] = {}
    for path in field_paths:
        item: dict[str, Any] = {'horizontal': True}
        if path in labels:
            item['label'] = labels[path]
        options[path] = item
    return options


class _PlainDropdownMixin:
    """Field title as label; keep «Усі» selected when nothing is filtered."""

    form_class = DropdownForm

    def _selected(self) -> str:
        value = self.value()
        return '' if value in EMPTY_VALUES else str(value)

    def _yield_form(self, name: str, choices: list) -> Iterator[dict]:
        yield {
            'form': self.form_class(
                label=str(self.title).strip(),
                name=name,
                choices=choices,
                data={name: self._selected()},
                multiple=bool(getattr(self, 'multiple', False)),
            ),
        }


class RsChoicesDropdownFilter(_PlainDropdownMixin, ChoicesDropdownFilter):
    def choices(self, changelist: ChangeList) -> Iterator[dict]:
        choices = [self.all_option] if self.all_option else []
        choices.extend(list(self.field.flatchoices))
        yield from self._yield_form(self.lookup_kwarg, choices)


class RsRelatedDropdownFilter(_PlainDropdownMixin, RelatedDropdownFilter):
    def choices(self, changelist: ChangeList) -> Iterator[dict]:
        choices = [self.all_option, *self.lookup_choices]
        yield from self._yield_form(self.lookup_kwarg, choices)


class RsBooleanDropdownFilter(
    _PlainDropdownMixin,
    ValueMixin,
    DropdownMixin,
    admin.BooleanFieldListFilter,
):
    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        if self.value() not in EMPTY_VALUES:
            return super().queryset(request, queryset)
        return queryset

    def choices(self, changelist: ChangeList) -> Iterator[dict]:
        choices = [
            self.all_option,
            ('1', _('Yes')),
            ('0', _('No')),
        ]
        yield from self._yield_form(self.lookup_kwarg, choices)


class RsAllValuesDropdownFilter(
    _PlainDropdownMixin,
    ValueMixin,
    DropdownMixin,
    admin.AllValuesFieldListFilter,
):
    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        if self.value() not in EMPTY_VALUES:
            return super().queryset(request, queryset)
        return queryset

    def choices(self, changelist: ChangeList) -> Iterator[dict]:
        choices = [self.all_option] if self.all_option else []
        for val in self.lookup_choices:
            if val in EMPTY_VALUES:
                continue
            choices.append((val, val))
        yield from self._yield_form(self.lookup_kwarg, choices)
