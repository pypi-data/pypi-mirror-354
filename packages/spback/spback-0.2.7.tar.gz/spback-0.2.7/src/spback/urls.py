import typing as t

from django.urls import path
from ninja.throttling import AnonRateThrottle, AuthRateThrottle
from ninja_extra import NinjaExtraAPI


def create_api(*args, **kwargs) -> NinjaExtraAPI:
  """create ninja api to use."""
  # from ninja import NinjaAPI

  return NinjaExtraAPI(
    *args,
    **kwargs,
    throttle=[
      AnonRateThrottle("10/s"),
      AuthRateThrottle("100/s"),
    ],
  )


def get_urlspatterns(api) -> t.List[t.Any]:
  return [
    path("", api.urls),
  ]
