# handle errors.

from ninja_extra import NinjaExtraAPI

from spback.srv import errors


def register_error_handler(api: NinjaExtraAPI) -> NinjaExtraAPI:
  @api.exception_handler(errors.ResponseError)
  def handle_response_error(request, exc):
    return api.create_response(
      request,
      {
        "success": False,
        "data": exc.data,
        "errorMessage": exc.message,
      },
      status=400,
    )

  @api.exception_handler(errors.InternalError)
  def handle_internal_error(request, exc):
    return api.create_response(
      request,
      {
        "success": False,
        "data": None,
        "errorMessage": "internal error, please contact admin.",
      },
      status=500,
    )

  from ninja.errors import ValidationError

  @api.exception_handler(ValidationError)
  def validate_error(request, exc):
    return api.create_response(
      request,
      {
        "success": False,
        "data": exc.errors,
        "errorMessage": "Data validation error. Please contact admin.",
      },
      status=422,
    )

  return api
