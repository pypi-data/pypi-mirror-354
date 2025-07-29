import random
import string

from django.core.management.base import BaseCommand, CommandError


def generate_random_password(length):
  all_characters = string.ascii_letters + string.digits + string.punctuation
  password = "".join(random.choice(all_characters) for _ in range(length))
  return password


class Command(BaseCommand):
  help = "Create new meter user"

  def add_arguments(self, parser):
    parser.add_argument("username", type=str)
    parser.add_argument("email", type=str)

  def handle(self, *args, **options):
    from django.contrib.auth import get_user_model

    User = get_user_model()

    username = options["username"]
    email = options["email"]
    try:
      user = User.objects.create(username=username, email=email)
      pwd = generate_random_password(10)
      # seems not work
      user.set_password(pwd)
      user.save()
    except Exception as e:
      raise CommandError(e)

    self.stdout.write(f"Successfully create user: {username} with password: {pwd}")
