from ninja_extra import NinjaExtraAPI, api_controller
from ninja_jwt.controller import TokenObtainPairController


@api_controller("token", tags=["Auth"])
class MyCustomController(TokenObtainPairController):
  """obtain_token and refresh_token only"""


def register_controller(api) -> NinjaExtraAPI:
  api.register_controllers(MyCustomController)
  return api


def avoid_bandcrupt():
  """防止多次攻击窃取用户名密码"""
  pass
