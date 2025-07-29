import spback.funcs as f
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser


User = get_user_model()


def create_user():
  u, username, passwd = create_withpasswd()

  def login(client):
    assert client.login(username=username, password=passwd), "password incorrect"
    return client

  return u, login


def create_withpasswd() -> tuple[AbstractBaseUser, str, str]:
  passwd = f.random_string(16)
  username = f.random_string(8)
  email = f"{username}@temp.com"
  u = User.objects.create(email=email, username=username)
  u.set_password(passwd)
  u.save()
  assert u.check_password(passwd), "passwd must be checked."
  return u, username, passwd


def create_unique(email: str):
  u = User.objects.create(email=email, username=email)
  return u
