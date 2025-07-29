import typing as t


class UserError(Exception):
  pass


class ResponseError(Exception):
  """Raise this error, and views or services handle it automaticly."""

  def __init__(self, message: str, data: t.Optional[dict]):
    self.message = message
    self.data = data

  def generate_response(self):
    return {
      "success": False,
      "data": self.data,
      "errorMessage": self.message,
    }


class InternalError(ResponseError):
  """when meeting internal error"""

  def generate_response(self):
    return {
      "success": False,
      "data": None,
      "errorMessage": "internal error, please contact admin.",
    }
