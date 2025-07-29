import typing as t
from ninja_jwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractBaseUser


class HasAccess(t.Protocol):
  @property
  def access_token(self) -> str: ...


def get_token(u: AbstractBaseUser):
  refresh = RefreshToken.for_user(u)
  refresh = t.cast(HasAccess, refresh)

  return {
    "refresh": str(refresh),
    "access": str(refresh.access_token),
  }
