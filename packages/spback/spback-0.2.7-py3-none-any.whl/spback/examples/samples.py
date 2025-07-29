from typing import Optional
from ninja_extra import api_controller, http_get


@api_controller("/", tags=["Math"], permissions=[])
class MathAPI:
  @http_get(
    "/subtract",
  )
  def subtract(self, a: int, b: int):
    """Subtracts a from b"""
    return {"result": a - b}

  @http_get(
    "/divide",
  )
  def divide(self, a: int, b: int):
    """Divides a by b"""
    return {"result": a / b}

  @http_get(
    "/multiple",
  )
  def multiple(self, a: int, b: int):
    """Multiples a with b"""
    return {"result": a * b}


def register_controller(api):
  api.register_controllers(MathAPI)
  test_post(api)


def test_post(api):
  from ninja import Schema

  class FormSample(Schema):
    name: str
    optional_gender: Optional[str] = None  # assign as None, to make it optional

  @api.post("/test_params")
  def test_post(request, FormSample: FormSample):
    return {"success": True, "data": {"name": FormSample.name}}
