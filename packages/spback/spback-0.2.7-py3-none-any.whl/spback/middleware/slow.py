import time

from django.conf import settings


class SlowDownMiddleware(object):
  def __init__(self, get_response):
    self.get_response = get_response
    # One-time configuration and initialization.

  def __call__(self, request):
    response = self.get_response(request)
    slowdown = getattr(settings, "SLOWDOWN", 1000)
    time.sleep(slowdown / 1000)
    return response
