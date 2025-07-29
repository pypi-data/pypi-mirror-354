"""create superuser for django

python manage.py script_file <username> <email> <password>
"""


def main():
  from .use_django import use_django

  use_django()

  from django.contrib.auth import get_user_model

  User = get_user_model()
  from spback.funcs import random_string

  # default values
  username = "svtter"
  pwd = random_string(10)
  email = "svtter@163.com"

  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument("username", help="username", default=username, nargs="?")
  parser.add_argument("password", help="password", default=pwd, nargs="?")
  parser.add_argument("email", help="email", default=email, nargs="?")

  args = parser.parse_args()

  u = User.objects.create_superuser(username=args.username, email=args.email)
  u.set_password(args.password)
  u.save()
  print("user: {username} created, password: {pwd}".format(pwd=pwd, username=username))
