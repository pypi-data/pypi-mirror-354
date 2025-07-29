# coding: utf-8

import pytest

from spback.basic_.views.page import CountlessPaginator


def apply_countless_page(model, page_number, page_size):
  obj = model.objects.all()
  paginator = CountlessPaginator(obj, page_size)
  page_obj = paginator.page(page_number)
  assert page_obj.number == page_number
  assert page_obj.page_size == page_size
  assert page_obj.has_next() == (len(obj) > len(obj[:page_size]))
