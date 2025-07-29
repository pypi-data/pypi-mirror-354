import collections

from django.core.paginator import EmptyPage, PageNotAnInteger
from django.utils.translation import gettext_lazy as _


class CountlessPage(collections.abc.Sequence):
  def __init__(self, object_list, number, page_size):
    self.object_list = object_list
    self.number = number
    self.page_size = page_size

    if not isinstance(self.object_list, list):
      self.object_list = list(self.object_list)

    self._has_next = len(self.object_list) > len(self.object_list[: self.page_size])
    self._has_previous = self.number > 1

  def __repr__(self):
    return "<Page %s>" % self.number

  def __len__(self):
    return len(self.object_list)

  def __getitem__(self, index):
    if not isinstance(index, (int, slice)):
      raise TypeError
    return self.object_list[index]

  def has_next(self):
    return self._has_next

  def has_previous(self):
    return self._has_previous

  def has_other_pages(self):
    return self.has_next() or self.has_previous()

  def next_page_number(self):
    if self.has_next():
      return self.number + 1
    else:
      raise EmptyPage(_("Next page does not exist"))

  def previous_page_number(self):
    if self.has_previous():
      return self.number - 1
    else:
      raise EmptyPage(_("Previous page does not exist"))


class CountlessPaginator:
  def __init__(self, object_list, per_page) -> None:
    self.object_list = object_list
    self.per_page = per_page

  def validate_number(self, number):
    try:
      if isinstance(number, float) and not number.is_integer():
        raise ValueError
      number = int(number)
    except (TypeError, ValueError):
      raise PageNotAnInteger(_("Page number is not an integer"))
    if number < 1:
      raise EmptyPage(_("Page number is less than 1"))
    return number

  def get_page(self, number):
    try:
      number = self.validate_number(number)
    except (PageNotAnInteger, EmptyPage):
      number = 1
    return self.page(number)

  def page(self, number):
    number = self.validate_number(number)
    bottom = (number - 1) * self.per_page
    top = bottom + self.per_page + 1
    return CountlessPage(self.object_list[bottom:top], number, self.per_page)
